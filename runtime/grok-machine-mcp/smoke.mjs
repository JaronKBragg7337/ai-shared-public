import { spawn } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = process.env.MCP_BASE_URL || `http://127.0.0.1:${process.env.MCP_PORT || 3001}`;

function envValue(name) {
  const text = requireEnvFile();
  const line = text.split(/\r?\n/).find((candidate) => candidate.startsWith(`${name}=`));
  return line ? line.slice(name.length + 1).trim() : '';
}

function requireEnvFile() {
  try {
    return requireEnvFile.cache;
  } catch {
    throw new Error('The .env file is missing. Run scripts\\start.ps1 first so it can create an MCP_AUTH_TOKEN.');
  }
}

requireEnvFile.cache = await readFile(path.join(projectRoot, '.env'), 'utf8');
const token = envValue('MCP_AUTH_TOKEN');
if (!token || token.length < 32) throw new Error('MCP_AUTH_TOKEN in .env is missing or too short.');

async function getHealth() {
  try {
    const response = await fetch(`${baseUrl}/healthz`);
    return response.ok;
  } catch {
    return false;
  }
}

let child = null;
if (!(await getHealth())) {
  child = spawn(process.execPath, ['server.mjs'], {
    cwd: projectRoot,
    env: { ...process.env },
    stdio: ['ignore', 'pipe', 'pipe'],
    windowsHide: true,
  });
  child.stdout.on('data', (chunk) => process.stdout.write(`[server] ${chunk}`));
  child.stderr.on('data', (chunk) => process.stderr.write(`[server] ${chunk}`));
  for (let attempt = 0; attempt < 50 && !(await getHealth()); attempt += 1) {
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
}

if (!(await getHealth())) throw new Error('Local server did not become healthy.');

async function request(method, body, sessionId = '') {
  const headers = {
    Authorization: `Bearer ${token}`,
    Accept: 'application/json, text/event-stream',
  };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (sessionId) headers['MCP-Session-Id'] = sessionId;
  if (method !== 'DELETE') headers['MCP-Protocol-Version'] = '2025-06-18';
  const response = await fetch(`${baseUrl}/mcp`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  return { response, text };
}

function parseMcpBody(text) {
  const dataLines = text
    .split(/\r?\n/)
    .filter((line) => line.startsWith('data:'))
    .map((line) => line.slice(5).trim())
    .filter(Boolean);
  for (const candidate of [...dataLines.reverse(), text.trim()]) {
    try { return JSON.parse(candidate); } catch { /* try the next framing shape */ }
  }
  return null;
}

const unauthorized = await fetch(`${baseUrl}/mcp`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
if (unauthorized.status !== 401) throw new Error(`Expected unauthorized MCP request to return 401, got ${unauthorized.status}.`);

const initBody = {
  jsonrpc: '2.0',
  id: 1,
  method: 'initialize',
  params: {
    protocolVersion: '2025-06-18',
    capabilities: {},
    clientInfo: { name: 'grok-machine-smoke', version: '0.1.0' },
  },
};
const initialized = await request('POST', initBody);
if (!initialized.response.ok) throw new Error(`MCP initialize failed: ${initialized.response.status} ${initialized.text}`);
const sessionId = initialized.response.headers.get('mcp-session-id');
const initJson = parseMcpBody(initialized.text);
if (!sessionId || !initJson?.result?.serverInfo) throw new Error(`MCP initialize response was incomplete: ${initialized.text}`);

const listed = await request('POST', { jsonrpc: '2.0', id: 2, method: 'tools/list', params: {} }, sessionId);
if (!listed.response.ok) throw new Error(`tools/list failed: ${listed.response.status} ${listed.text}`);
const listJson = parseMcpBody(listed.text);
const toolNames = (listJson?.result?.tools || []).map((tool) => tool.name);
if (!toolNames.includes('shell_exec') || !toolNames.includes('screen_capture')) {
  throw new Error(`Expected full-control tools were not advertised: ${toolNames.join(', ')}`);
}

const called = await request('POST', {
  jsonrpc: '2.0',
  id: 3,
  method: 'tools/call',
  params: { name: 'shell_exec', arguments: { command: 'Write-Output grok-machine-smoke-ok' } },
}, sessionId);
if (!called.response.ok) throw new Error(`tools/call failed: ${called.response.status} ${called.text}`);
const callJson = parseMcpBody(called.text);
const callText = JSON.stringify(callJson);
if (!callJson?.result || !callText.includes('grok-machine-smoke-ok')) throw new Error(`Tool call did not return expected output: ${called.text}`);

const windowCall = await request('POST', {
  jsonrpc: '2.0',
  id: 4,
  method: 'tools/call',
  params: { name: 'active_window', arguments: {} },
}, sessionId);
const windowJson = parseMcpBody(await windowCall.text);
if (!windowJson?.result) throw new Error(`active_window did not return a result: ${JSON.stringify(windowJson)}`);

const screenCall = await request('POST', {
  jsonrpc: '2.0',
  id: 5,
  method: 'tools/call',
  params: { name: 'screen_capture', arguments: {} },
}, sessionId);
const screenJson = parseMcpBody(await screenCall.text);
const image = screenJson?.result?.content?.find((item) => item.type === 'image');
if (!image?.data || image.mimeType !== 'image/png' || image.data.length < 1000) {
  throw new Error(`screen_capture did not return a PNG image: ${JSON.stringify(screenJson)?.slice(0, 500)}`);
}

await request('DELETE', undefined, sessionId).catch(() => {});
console.log(`MCP smoke passed: ${toolNames.length} tools advertised, authenticated session ${sessionId}, active window and screen capture verified.`);

if (child) {
  child.kill();
  await new Promise((resolve) => child.once('close', resolve));
}
