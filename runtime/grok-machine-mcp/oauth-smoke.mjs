import { createHash, randomBytes } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = (process.env.MCP_BASE_URL || `http://127.0.0.1:${process.env.MCP_PORT || 3001}`).replace(/\/$/, '');
const issuer = (process.env.MCP_OAUTH_ISSUER || 'https://mcp.heartbeatobservatory.com').replace(/\/$/, '');
const resource = (process.env.MCP_RESOURCE_IDENTIFIER || `${issuer}/mcp`).replace(/\/$/, '');
const clientId = process.env.MCP_OAUTH_CLIENT_ID || 'grok-machine-ios';
const redirectUri = process.env.MCP_TEST_REDIRECT_URI || 'https://grok.com/connectors-oauth-exchange-code/';
const scope = 'mcp:tools';
const tokenFile = process.env.OAUTH_SMOKE_TOKEN_FILE || '';
const resumeFile = process.env.OAUTH_SMOKE_RESUME_FILE || '';

function base64Url(buffer) {
  return Buffer.from(buffer).toString('base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
}

function createVerifier() {
  return base64Url(randomBytes(32));
}

function createChallenge(verifier) {
  return base64Url(createHash('sha256').update(verifier, 'ascii').digest());
}

function assertCondition(condition, message) {
  if (!condition) throw new Error(message);
}

async function fetchResponse(pathname, options = {}) {
  const response = await fetch(`${baseUrl}${pathname}`, { redirect: 'manual', ...options });
  const text = await response.text();
  return { response, text };
}

function parseJson(text, label) {
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`${label} was not JSON: ${text.slice(0, 500)}`);
  }
}

function parseMcpBody(text, label) {
  const dataLines = text
    .split(/\r?\n/)
    .filter((line) => line.startsWith('data:'))
    .map((line) => line.slice(5).trim())
    .filter(Boolean);
  for (const candidate of [...dataLines.reverse(), text.trim()]) {
    try { return JSON.parse(candidate); } catch { /* try the next framing shape */ }
  }
  throw new Error(`${label} was not valid MCP JSON: ${text.slice(0, 700)}`);
}

async function metadataChecks() {
  const unauthenticated = await fetchResponse('/mcp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: '{}',
  });
  const challenge = unauthenticated.response.headers.get('www-authenticate') || '';
  assertCondition(unauthenticated.response.status === 401, `Unauthenticated MCP request returned ${unauthenticated.response.status}.`);
  assertCondition(challenge.includes('resource_metadata="' + issuer + '/.well-known/oauth-protected-resource/mcp"'), `OAuth resource metadata reference missing from WWW-Authenticate: ${challenge}`);
  assertCondition(challenge.includes('scope="mcp:tools"'), `Required scope missing from WWW-Authenticate: ${challenge}`);

  const protectedRoot = await fetchResponse('/.well-known/oauth-protected-resource');
  assertCondition(protectedRoot.response.ok, `Protected-resource root metadata returned ${protectedRoot.response.status}: ${protectedRoot.text}`);
  const protectedPath = await fetchResponse('/.well-known/oauth-protected-resource/mcp');
  assertCondition(protectedPath.response.ok, `Protected-resource path metadata returned ${protectedPath.response.status}: ${protectedPath.text}`);
  const protectedMetadata = parseJson(protectedPath.text, 'Protected-resource metadata');
  assertCondition(protectedMetadata.resource === resource, `Protected-resource metadata has the wrong resource: ${protectedPath.text}`);
  assertCondition(protectedMetadata.authorization_servers?.includes(issuer), `Protected-resource metadata does not advertise ${issuer}.`);

  const authorizationMetadata = await fetchResponse('/.well-known/oauth-authorization-server');
  assertCondition(authorizationMetadata.response.ok, `Authorization-server metadata returned ${authorizationMetadata.response.status}: ${authorizationMetadata.text}`);
  const authorizationServer = parseJson(authorizationMetadata.text, 'Authorization-server metadata');
  assertCondition(authorizationServer.issuer === issuer, `Authorization-server issuer mismatch: ${authorizationMetadata.text}`);
  assertCondition(authorizationServer.authorization_endpoint === `${issuer}/oauth/authorize`, 'Authorization endpoint metadata mismatch.');
  assertCondition(authorizationServer.token_endpoint === `${issuer}/oauth/token`, 'Token endpoint metadata mismatch.');
  assertCondition(authorizationServer.code_challenge_methods_supported?.includes('S256'), 'S256 is not advertised.');
  assertCondition(authorizationServer.token_endpoint_auth_methods_supported?.includes('none'), 'Public token authentication is not advertised.');

  return { challenge, protectedMetadata, authorizationServer };
}

async function beginAuthorization() {
  const verifier = createVerifier();
  const stateValue = `oauth-smoke-${base64Url(randomBytes(12))}`;
  const query = new URLSearchParams({
    client_id: clientId,
    response_type: 'code',
    redirect_uri: redirectUri,
    scope,
    state: stateValue,
    code_challenge: createChallenge(verifier),
    code_challenge_method: 'S256',
    resource,
  });
  const authorization = await fetchResponse(`/oauth/authorize?${query}`);
  assertCondition(authorization.response.status === 200, `Authorization endpoint rejected a valid PKCE request: ${authorization.response.status} ${authorization.text}`);
  const requestId = authorization.text.match(/name="request_id" value="([^"]+)"/)?.[1];
  const csrf = authorization.text.match(/name="csrf" value="([^"]+)"/)?.[1];
  assertCondition(requestId && csrf, 'Authorization consent page did not contain its CSRF/request fields.');

  const approval = await fetchResponse('/oauth/authorize/approve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ request_id: requestId, csrf }).toString(),
  });
  assertCondition(approval.response.status === 302, `Authorization approval did not redirect: ${approval.response.status} ${approval.text}`);
  const locationHeader = approval.response.headers.get('location');
  assertCondition(locationHeader, 'Authorization approval did not return a redirect location.');
  const redirect = new URL(locationHeader);
  assertCondition(redirect.origin + redirect.pathname === new URL(redirectUri).origin + new URL(redirectUri).pathname, `Authorization redirected to an unexpected URI: ${locationHeader}`);
  assertCondition(redirect.searchParams.get('state') === stateValue, 'Authorization state was not returned unchanged.');
  assertCondition(redirect.searchParams.get('iss') === issuer, 'Authorization issuer response parameter was not returned.');
  const code = redirect.searchParams.get('code');
  assertCondition(code, 'Authorization redirect did not contain a code.');
  return { verifier, stateValue, code };
}

async function exchangeToken(fields) {
  const token = await fetchResponse('/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(fields).toString(),
  });
  return { ...token, json: parseJson(token.text, 'Token response') };
}

async function issueTokens() {
  const authorization = await beginAuthorization();
  const invalid = await exchangeToken({
    grant_type: 'authorization_code',
    client_id: clientId,
    code: authorization.code,
    redirect_uri: redirectUri,
    code_verifier: `${authorization.verifier.slice(0, -1)}${authorization.verifier.endsWith('A') ? 'B' : 'A'}`,
    resource,
  });
  assertCondition(invalid.response.status === 400 && invalid.json.error === 'invalid_grant', `Invalid PKCE verifier did not fail as invalid_grant: ${invalid.response.status} ${invalid.text}`);

  const exchanged = await exchangeToken({
    grant_type: 'authorization_code',
    client_id: clientId,
    code: authorization.code,
    redirect_uri: redirectUri,
    code_verifier: authorization.verifier,
    resource,
  });
  assertCondition(exchanged.response.ok, `Valid authorization-code exchange failed: ${exchanged.response.status} ${exchanged.text}`);
  assertCondition(exchanged.json.token_type === 'Bearer' && exchanged.json.access_token && exchanged.json.refresh_token, `Token response did not contain bearer access and refresh tokens: ${exchanged.text}`);
  return exchanged.json;
}

async function mcpRequest(accessToken, method, body, sessionId = '') {
  const headers = {
    Authorization: `Bearer ${accessToken}`,
    Accept: 'application/json, text/event-stream',
  };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (sessionId) headers['MCP-Session-Id'] = sessionId;
  if (method !== 'DELETE') headers['MCP-Protocol-Version'] = '2025-06-18';
  const result = await fetchResponse('/mcp', {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  return { ...result, json: result.text ? parseMcpBody(result.text, `MCP ${method}`) : null };
}

function toolValue(response, label) {
  const text = response.json?.result?.content?.find((item) => item.type === 'text')?.text;
  assertCondition(text, `${label} did not return MCP text content: ${response.text}`);
  try { return JSON.parse(text); } catch { throw new Error(`${label} did not return JSON content: ${text.slice(0, 500)}`); }
}

async function authenticatedMcpChecks(tokens, { exerciseOllamaChat = false } = {}) {
  const initialize = await mcpRequest(tokens.access_token, 'POST', {
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: {
      protocolVersion: '2025-06-18',
      capabilities: {},
      clientInfo: { name: 'grok-machine-oauth-smoke', version: '0.1.0' },
    },
  });
  assertCondition(initialize.response.ok, `Authenticated MCP initialize failed: ${initialize.response.status} ${initialize.text}`);
  const sessionId = initialize.response.headers.get('mcp-session-id');
  assertCondition(sessionId && initialize.json?.result?.serverInfo, `Authenticated MCP initialize was incomplete: ${initialize.text}`);

  const listed = await mcpRequest(tokens.access_token, 'POST', {
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/list',
    params: {},
  }, sessionId);
  assertCondition(listed.response.ok, `Authenticated tools/list failed: ${listed.response.status} ${listed.text}`);
  const tools = listed.json?.result?.tools || [];
  const toolNames = tools.map((tool) => tool.name);
  assertCondition(tools.length >= 27, `Expected at least the 27 existing tools, but tools/list returned ${tools.length}: ${toolNames.join(', ')}`);
  for (const expected of ['shell_exec', 'screen_capture', 'mouse_click', 'type_text', 'system_info']) {
    assertCondition(toolNames.includes(expected), `Existing tool ${expected} was not advertised.`);
  }
  for (const expected of ['task_start', 'task_status', 'verify_file_exists', 'verify_port_open', 'ollama_models', 'ollama_chat', 'registry_list']) {
    assertCondition(toolNames.includes(expected), `Foundation tool ${expected} was not advertised.`);
  }

  const called = await mcpRequest(tokens.access_token, 'POST', {
    jsonrpc: '2.0',
    id: 3,
    method: 'tools/call',
    params: { name: 'shell_exec', arguments: { command: 'Write-Output grok-machine-oauth-smoke-ok' } },
  }, sessionId);
  assertCondition(called.response.ok, `Authenticated shell_exec failed: ${called.response.status} ${called.text}`);
  assertCondition(JSON.stringify(called.json).includes('grok-machine-oauth-smoke-ok'), `Authenticated shell_exec did not return expected output: ${called.text}`);

  const windowCall = await mcpRequest(tokens.access_token, 'POST', {
    jsonrpc: '2.0',
    id: 4,
    method: 'tools/call',
    params: { name: 'active_window', arguments: {} },
  }, sessionId);
  assertCondition(windowCall.response.ok && windowCall.json?.result, `Authenticated active_window failed: ${windowCall.response.status} ${windowCall.text}`);

  const fileCheck = await mcpRequest(tokens.access_token, 'POST', {
    jsonrpc: '2.0',
    id: 5,
    method: 'tools/call',
    params: { name: 'verify_file_exists', arguments: { path: path.join(projectRoot, 'server.mjs') } },
  }, sessionId);
  assertCondition(fileCheck.response.ok && toolValue(fileCheck, 'verify_file_exists').ok, `verify_file_exists failed: ${fileCheck.text}`);

  const portCheck = await mcpRequest(tokens.access_token, 'POST', {
    jsonrpc: '2.0',
    id: 6,
    method: 'tools/call',
    params: { name: 'verify_port_open', arguments: { host: '127.0.0.1', port: 3001 } },
  }, sessionId);
  assertCondition(portCheck.response.ok && toolValue(portCheck, 'verify_port_open').ok, `verify_port_open failed: ${portCheck.text}`);

  const modelsCall = await mcpRequest(tokens.access_token, 'POST', {
    jsonrpc: '2.0',
    id: 7,
    method: 'tools/call',
    params: { name: 'ollama_models', arguments: {} },
  }, sessionId);
  const models = toolValue(modelsCall, 'ollama_models');
  assertCondition(modelsCall.response.ok && models.models?.length >= 1, `ollama_models did not return installed models: ${modelsCall.text}`);

  if (exerciseOllamaChat) {
    const model = models.models[0]?.name;
    const chatCall = await mcpRequest(tokens.access_token, 'POST', {
      jsonrpc: '2.0',
      id: 71,
      method: 'tools/call',
      params: { name: 'ollama_chat', arguments: {
        model,
        messages: [{ role: 'user', content: 'Reply with exactly: grok-machine-ollama-smoke-ok' }],
        temperature: 0,
      } },
    }, sessionId);
    const chat = toolValue(chatCall, 'ollama_chat');
    assertCondition(chatCall.response.ok && chat.message?.content, `ollama_chat failed: ${chatCall.text}`);
  }

  const registryCall = await mcpRequest(tokens.access_token, 'POST', {
    jsonrpc: '2.0',
    id: 8,
    method: 'tools/call',
    params: { name: 'registry_list', arguments: {} },
  }, sessionId);
  const registry = toolValue(registryCall, 'registry_list');
  assertCondition(registryCall.response.ok && registry.projects?.some((project) => project.id === 'grok-machine-mcp'), `registry_list did not contain grok-machine-mcp: ${registryCall.text}`);

  const taskCall = await mcpRequest(tokens.access_token, 'POST', {
    jsonrpc: '2.0',
    id: 9,
    method: 'tools/call',
    params: { name: 'task_start', arguments: { objective: 'OAuth smoke task', command: 'Write-Output grok-machine-task-smoke-ok' } },
  }, sessionId);
  const task = toolValue(taskCall, 'task_start');
  assertCondition(taskCall.response.ok && task.id, `task_start did not return a task: ${taskCall.text}`);

  let taskStatus;
  for (let attempt = 0; attempt < 20; attempt += 1) {
    await new Promise((resolve) => setTimeout(resolve, 250));
    const statusCall = await mcpRequest(tokens.access_token, 'POST', {
      jsonrpc: '2.0',
      id: 10 + attempt,
      method: 'tools/call',
      params: { name: 'task_status', arguments: { id: task.id } },
    }, sessionId);
    taskStatus = toolValue(statusCall, 'task_status');
    if (['completed', 'failed', 'cancelled'].includes(taskStatus.status)) break;
  }
  assertCondition(taskStatus?.status === 'completed', `task did not complete: ${JSON.stringify(taskStatus)}`);

  const taskLogsCall = await mcpRequest(tokens.access_token, 'POST', {
    jsonrpc: '2.0',
    id: 31,
    method: 'tools/call',
    params: { name: 'task_logs', arguments: { id: task.id } },
  }, sessionId);
  const taskLogs = toolValue(taskLogsCall, 'task_logs');
  assertCondition(taskLogs.output?.includes('grok-machine-task-smoke-ok'), `task_logs did not contain task output: ${taskLogsCall.text}`);
  return { sessionId, toolNames };
}

async function refreshTokens(tokens) {
  const refreshed = await exchangeToken({
    grant_type: 'refresh_token',
    client_id: clientId,
    refresh_token: tokens.refresh_token,
    resource,
  });
  assertCondition(refreshed.response.ok, `Refresh-token exchange failed: ${refreshed.response.status} ${refreshed.text}`);
  assertCondition(refreshed.json.access_token && refreshed.json.refresh_token, `Refresh response did not rotate bearer tokens: ${refreshed.text}`);
  return refreshed.json;
}

let tokens;
const metadata = await metadataChecks();
if (resumeFile) {
  tokens = JSON.parse(await readFile(resumeFile, 'utf8'));
  assertCondition(tokens.access_token && tokens.refresh_token, `Resume file ${resumeFile} does not contain OAuth tokens.`);
  console.log('Using persisted OAuth tokens from the resume file.');
} else {
  tokens = await issueTokens();
}

const firstMcp = await authenticatedMcpChecks(tokens, { exerciseOllamaChat: true });
const refreshedTokens = await refreshTokens(tokens);
const refreshedMcp = await authenticatedMcpChecks(refreshedTokens);
if (tokenFile) await writeFile(tokenFile, JSON.stringify(refreshedTokens), { encoding: 'utf8', mode: 0o600 });

console.log(`OAuth smoke passed through ${baseUrl}: metadata, OAuth challenge, valid PKCE authorization, invalid-verifier rejection, token exchange, ${firstMcp.toolNames.length} tools/list tools, legacy controls, verification, durable task, Ollama chat, registry, refresh-token rotation, and post-refresh MCP initialize.`);
if (tokenFile) console.log(`OAuth smoke tokens saved for an optional restart-persistence check at ${tokenFile}.`);
void metadata;
