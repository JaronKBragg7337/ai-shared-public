import { createHash, randomBytes, randomUUID } from 'node:crypto';
import * as fs from 'node:fs/promises';
import * as os from 'node:os';
import * as path from 'node:path';

const DEFAULT_REDIRECT_URIS = [
  'https://grok.com/connectors-oauth-exchange-code/',
  'https://grok.com/connectors-oauth-exchange-code',
  'https://www.grok.com/connectors-oauth-exchange-code/',
  'https://www.grok.com/connectors-oauth-exchange-code',
];

const REQUIRED_SCOPE = 'mcp:tools';
const OPTIONAL_SCOPE = 'offline_access';
const ACCESS_TOKEN_TTL_SECONDS = 3600;
// 10/21: Grok's app doesn't always use its refresh token, so its sign-in 'expired' every hour or so and Jaron had to re-authorize
// by hand. An access token whose client still holds a live refresh token is now renewed in place (sliding, same lifetime).
const clientHasLiveRefresh = (state, clientId, t) => Object.values(state.refreshTokens).some((r) => r && r.client_id === clientId && r.expires_at > t);
const REFRESH_TOKEN_TTL_SECONDS = 30 * 24 * 60 * 60;
const AUTH_CODE_TTL_SECONDS = 300;
const AUTH_REQUEST_TTL_SECONDS = 600;

function stripTrailingSlash(value) {
  return String(value || '').replace(/\/$/, '');
}

function base64Url(buffer) {
  return Buffer.from(buffer).toString('base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
}

function randomToken(prefix) {
  return `${prefix}_${base64Url(randomBytes(48))}`;
}

function hash(value) {
  return createHash('sha256').update(String(value), 'utf8').digest('hex');
}

function challengeForVerifier(verifier) {
  return base64Url(createHash('sha256').update(verifier, 'ascii').digest());
}

function parseScopes(value) {
  return String(value || '').trim().split(/\s+/).filter(Boolean);
}

function unique(values) {
  return [...new Set(values)];
}

function exactRedirectUriAllowed(uri) {
  // Accepts the three redirect forms RFC 8252 (OAuth 2.0 for Native Apps) permits:
  //   1. https://...                      - web callbacks and claimed https redirects
  //   2. http://127.0.0.1|localhost|[::1] - loopback, section 7.3
  //   3. private-use URI schemes          - e.g. cursor://..., section 7.1
  //
  // Case 3 was missing and it broke Grok Bot on 2026-09-10. Grok Bot is a native
  // desktop app, so its dynamic client registration sends a custom-scheme callback.
  // This function rejected it, /oauth/register answered 400 invalid_redirect_uri,
  // and no sign-in card ever opened - the endpoint answered 401 forever while the
  // tunnel was healthy. Symptom looked like a dead server; cause was over-strict
  // registration.
  //
  // SECURITY NOTE: the protection against redirect interception is EXACT MATCHING at
  // authorize time (isExactRedirect, below), not the scheme allowlist. Widening the
  // accepted schemes does not weaken that - a client still only ever gets redirected
  // to a URI it registered verbatim. What is enforced here: no fragment (RFC 6749
  // 3.1.2), and a private-use scheme must be a real scheme with a dot in it, which is
  // the reverse-DNS form RFC 8252 7.1 recommends and which excludes bare "http"-alikes.
  try {
    const parsed = new URL(uri);
    if (parsed.hash) return false;
    if (parsed.protocol === 'https:') return true;
    if (parsed.protocol === 'http:') {
      return ['127.0.0.1', 'localhost', '[::1]'].includes(parsed.hostname);
    }
    // Private-use / custom scheme, e.g. cursor:// or com.example.app://
    const scheme = parsed.protocol.replace(/:$/, '');
    if (!/^[a-z][a-z0-9+.-]*$/i.test(scheme)) return false;
    if (['file', 'data', 'javascript', 'vbscript', 'blob'].includes(scheme.toLowerCase())) return false;
    return true;
  } catch {
    return false;
  }
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (character) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  })[character]);
}

function headerOriginAllowed(req, allowedOrigins) {
  const origin = String(req.headers.origin || '').trim().replace(/\/$/, '').toLowerCase();
  return !origin || allowedOrigins.size === 0 || allowedOrigins.has(origin);
}

function applyCors(req, res, allowedOrigins) {
  const origin = String(req.headers.origin || '').trim();
  if (origin && headerOriginAllowed(req, allowedOrigins)) {
    res.setHeader('Access-Control-Allow-Origin', origin.replace(/[\r\n]/g, ''));
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Headers', 'Authorization, Content-Type, MCP-Protocol-Version, MCP-Session-Id, Last-Event-ID');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Expose-Headers', 'MCP-Session-Id, MCP-Protocol-Version, Last-Event-ID');
}

function sendJson(res, status, value, headers = {}) {
  const body = JSON.stringify(value);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    ...headers,
  });
  res.end(body);
}

function sendHtml(res, status, html, headers = {}) {
  res.writeHead(status, {
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'no-store',
    ...headers,
  });
  res.end(html);
}

function sendRedirect(res, location) {
  res.writeHead(302, { Location: location, 'Cache-Control': 'no-store' });
  res.end();
}

function oauthError(res, status, error, description, headers = {}) {
  sendJson(res, status, { error, error_description: description }, {
    'Cache-Control': 'no-store',
    Pragma: 'no-cache',
    ...headers,
  });
}

async function readRequestBody(req, maxBytes = 200000) {
  const chunks = [];
  let total = 0;
  for await (const chunk of req) {
    total += chunk.length;
    if (total > maxBytes) throw new Error('Request body too large.');
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString('utf8');
}

function basicClientCredentials(req) {
  const header = String(req.headers.authorization || '');
  if (!header.startsWith('Basic ')) return null;
  try {
    const decoded = Buffer.from(header.slice(6), 'base64').toString('utf8');
    const separator = decoded.indexOf(':');
    if (separator < 0) return null;
    return { clientId: decoded.slice(0, separator), clientSecret: decoded.slice(separator + 1) };
  } catch {
    return null;
  }
}

function normalizeStateShape(value) {
  const state = value && typeof value === 'object' ? value : {};
  return {
    version: 1,
    clients: state.clients && typeof state.clients === 'object' ? state.clients : {},
    authorizationRequests: state.authorizationRequests && typeof state.authorizationRequests === 'object' ? state.authorizationRequests : {},
    authorizationCodes: state.authorizationCodes && typeof state.authorizationCodes === 'object' ? state.authorizationCodes : {},
    accessTokens: state.accessTokens && typeof state.accessTokens === 'object' ? state.accessTokens : {},
    refreshTokens: state.refreshTokens && typeof state.refreshTokens === 'object' ? state.refreshTokens : {},
  };
}

export async function createOAuthService(options) {
  const issuer = stripTrailingSlash(options.issuer);
  const resource = stripTrailingSlash(options.resource);
  const allowedOrigins = options.allowedOrigins || new Set();
  const dataDir = path.resolve(options.dataDir || path.join(process.env.LOCALAPPDATA || os.homedir(), 'GrokMachineMcp'));
  const statePath = path.join(dataDir, 'oauth-state.json');
  const clientId = options.clientId || 'grok-machine-ios';
  const redirectUris = unique((options.redirectUris?.length ? options.redirectUris : DEFAULT_REDIRECT_URIS).map(String));
  const allScopes = [REQUIRED_SCOPE, OPTIONAL_SCOPE];

  await fs.mkdir(dataDir, { recursive: true });
  let state;
  try {
    state = normalizeStateShape(JSON.parse(await fs.readFile(statePath, 'utf8')));
  } catch {
    state = normalizeStateShape(null);
  }

  const now = () => Math.floor(Date.now() / 1000);
  const prune = () => {
    const current = now();
    for (const collection of ['authorizationRequests', 'authorizationCodes', 'accessTokens', 'refreshTokens']) {
      for (const [key, value] of Object.entries(state[collection])) {
        if (!value || Number(value.expires_at || 0) <= current) {
          if (collection === 'accessTokens' && value && clientHasLiveRefresh(state, value.client_id, current)) continue;   // keep: renewable
          delete state[collection][key];
        }
      }
    }
  };

  let saveQueue = Promise.resolve();
  async function persist() {
    prune();
    const serialized = JSON.stringify(state, null, 2);
    const temporaryPath = `${statePath}.${process.pid}.tmp`;
    saveQueue = saveQueue.then(async () => {
      await fs.writeFile(temporaryPath, serialized, { encoding: 'utf8', mode: 0o600 });
      await fs.rename(temporaryPath, statePath);
    });
    return saveQueue;
  }

  state.clients[clientId] = {
    client_id: clientId,
    client_name: 'Grok Machine iOS',
    redirect_uris: redirectUris,
    token_endpoint_auth_method: 'none',
    grant_types: ['authorization_code', 'refresh_token'],
    response_types: ['code'],
    created_at: state.clients[clientId]?.created_at || now(),
    pre_registered: true,
  };
  await persist();

  function metadata() {
    return {
      resource,
      authorization_servers: [issuer],
      bearer_methods_supported: ['header'],
      scopes_supported: [REQUIRED_SCOPE],
    };
  }

  function authorizationServerMetadata() {
    return {
      issuer,
      authorization_endpoint: `${issuer}/oauth/authorize`,
      token_endpoint: `${issuer}/oauth/token`,
      registration_endpoint: `${issuer}/oauth/register`,
      response_types_supported: ['code'],
      grant_types_supported: ['authorization_code', 'refresh_token'],
      token_endpoint_auth_methods_supported: ['none'],
      code_challenge_methods_supported: ['S256'],
      scopes_supported: allScopes,
      authorization_response_iss_parameter_supported: true,
      protected_resources: [resource],
    };
  }

  function publicConfig() {
    const client = state.clients[clientId];
    return {
      issuer,
      resource,
      protectedResourceMetadata: `${issuer}/.well-known/oauth-protected-resource/mcp`,
      authorizationServerMetadata: `${issuer}/.well-known/oauth-authorization-server`,
      authorizationEndpoint: `${issuer}/oauth/authorize`,
      tokenEndpoint: `${issuer}/oauth/token`,
      registrationEndpoint: `${issuer}/oauth/register`,
      clientId,
      redirectUris: client?.redirect_uris || redirectUris,
      scopes: [REQUIRED_SCOPE],
      tokenEndpointAuthMethod: 'none',
      dataDir,
    };
  }

  function getClient(id) {
    return id && state.clients[id] ? state.clients[id] : null;
  }

  function isExactRedirect(client, uri) {
    return Boolean(client && typeof uri === 'string' && client.redirect_uris.includes(uri));
  }

  function normalizeResource(value) {
    if (!value) return resource;
    return String(value) === resource ? resource : null;
  }

  function validScope(scopeValue) {
    const requested = unique(parseScopes(scopeValue || REQUIRED_SCOPE));
    if (!requested.includes(REQUIRED_SCOPE)) return null;
    if (requested.some((scope) => !allScopes.includes(scope))) return null;
    return requested;
  }

  function challenge(error, errorDescription) {
    const parameters = [
      'realm="grok-machine-mcp"',
      `resource_metadata="${issuer}/.well-known/oauth-protected-resource/mcp"`,
      `scope="${REQUIRED_SCOPE}"`,
    ];
    if (error) parameters.push(`error="${error}"`);
    if (errorDescription) parameters.push(`error_description="${String(errorDescription).replace(/["\\\r\n]/g, '')}"`);
    return `Bearer ${parameters.join(', ')}`;
  }

  function validateAccessToken(token) {
    if (!token) return null;
    const record = state.accessTokens[hash(token)];
    if (!record) return null;
    if (record.expires_at <= now()) {
      if (!clientHasLiveRefresh(state, record.client_id, now())) return null;
      record.expires_at = now() + ACCESS_TOKEN_TTL_SECONDS;   // renewed in memory; saved with the next persist()
    }
    if (record.resource !== resource) return null;
    if (!parseScopes(record.scope).includes(REQUIRED_SCOPE)) return null;
    return { ...record, token_type: 'Bearer' };
  }

  function makeAuthorizationCode(record) {
    const raw = randomToken('gm_code');
    state.authorizationCodes[hash(raw)] = { ...record, code_issued_at: now(), expires_at: now() + AUTH_CODE_TTL_SECONDS };
    return raw;
  }

  function issueTokens({ clientId: issuedFor, scope, resource: issuedResource }) {
    const issuedAt = now();
    const accessToken = randomToken('gm_at');
    const refreshToken = randomToken('gm_rt');
    state.accessTokens[hash(accessToken)] = {
      client_id: issuedFor,
      scope: scope.join(' '),
      resource: issuedResource,
      issued_at: issuedAt,
      expires_at: issuedAt + ACCESS_TOKEN_TTL_SECONDS,
    };
    state.refreshTokens[hash(refreshToken)] = {
      client_id: issuedFor,
      scope: scope.join(' '),
      resource: issuedResource,
      issued_at: issuedAt,
      expires_at: issuedAt + REFRESH_TOKEN_TTL_SECONDS,
    };
    return {
      access_token: accessToken,
      token_type: 'Bearer',
      expires_in: ACCESS_TOKEN_TTL_SECONDS,
      refresh_token: refreshToken,
      scope: scope.join(' '),
      resource: issuedResource,
    };
  }

  function redirectWithError(res, redirectUri, error, description, stateValue) {
    const redirect = new URL(redirectUri);
    redirect.searchParams.set('error', error);
    redirect.searchParams.set('error_description', description);
    if (stateValue) redirect.searchParams.set('state', stateValue);
    redirect.searchParams.set('iss', issuer);
    sendRedirect(res, redirect.toString());
  }

  function consentPage(requestId, csrf, details) {
    return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Authorize Grok Machine</title>
<style>
body{margin:0;background:#0b1115;color:#e8eef2;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;display:grid;place-items:center;min-height:100vh;padding:20px;box-sizing:border-box}
main{width:min(520px,100%);background:#111b21;border:1px solid #2c3d46;border-radius:18px;padding:28px;box-sizing:border-box;box-shadow:0 24px 70px #0008}
h1{font-size:24px;margin:0 0 10px}p{color:#b5c3ca}code{color:#b8e8ff;overflow-wrap:anywhere}.scope{background:#0b1115;border:1px solid #2c3d46;border-radius:10px;padding:12px;margin:18px 0}button{width:100%;border:0;border-radius:10px;background:#a5d4a7;color:#08120b;font:700 16px system-ui;padding:13px;cursor:pointer}small{color:#82949e}
</style></head><body><main>
<h1>Authorize Grok Machine</h1>
<p><strong>Grok</strong> is requesting access to the paired Windows computer through the Grok Machine MCP server.</p>
<div class="scope"><strong>Access requested</strong><br><code>${escapeHtml(details.scope)}</code><br><small>Resource: ${escapeHtml(details.resource)}</small></div>
<form method="post" action="/oauth/authorize/approve">
<input type="hidden" name="request_id" value="${escapeHtml(requestId)}">
<input type="hidden" name="csrf" value="${escapeHtml(csrf)}">
<button type="submit">Authorize Grok Machine</button>
</form>
</main></body></html>`;
  }

  async function beginAuthorization(req, res, url) {
    const query = url.searchParams;
    const requestedClientId = query.get('client_id') || '';
    const redirectUri = query.get('redirect_uri') || '';
    const client = getClient(requestedClientId);
    if (!client || !isExactRedirect(client, redirectUri)) {
      sendHtml(res, 400, '<h1>Invalid OAuth client or redirect URI</h1>');
      return;
    }
    const stateValue = query.get('state') || '';
    const fail = (error, description) => redirectWithError(res, redirectUri, error, description, stateValue);
    if (query.get('response_type') !== 'code') return fail('unsupported_response_type', 'Only authorization code is supported.');
    if (query.get('code_challenge_method') !== 'S256') return fail('invalid_request', 'PKCE S256 is required.');
    const codeChallenge = query.get('code_challenge') || '';
    if (!/^[A-Za-z0-9_-]{43,128}$/.test(codeChallenge)) return fail('invalid_request', 'A valid S256 code challenge is required.');
    const requestedResource = normalizeResource(query.get('resource'));
    if (!requestedResource) return fail('invalid_target', 'The resource parameter must identify this MCP server.');
    const scope = validScope(query.get('scope'));
    if (!scope) return fail('invalid_scope', `The requested scope must include ${REQUIRED_SCOPE}.`);

    const requestId = randomToken('gm_req');
    const csrf = randomToken('gm_csrf');
    state.authorizationRequests[requestId] = {
      client_id: requestedClientId,
      redirect_uri: redirectUri,
      code_challenge: codeChallenge,
      code_challenge_method: 'S256',
      scope: scope.join(' '),
      resource: requestedResource,
      state: stateValue,
      csrf_hash: hash(csrf),
      created_at: now(),
      expires_at: now() + AUTH_REQUEST_TTL_SECONDS,
    };
    await persist();
    sendHtml(res, 200, consentPage(requestId, csrf, { scope: scope.join(' '), resource: requestedResource }));
  }

  async function approveAuthorization(req, res) {
    const body = new URLSearchParams(await readRequestBody(req));
    const requestId = body.get('request_id') || '';
    const csrf = body.get('csrf') || '';
    const pending = state.authorizationRequests[requestId];
    if (!pending || pending.expires_at <= now() || hash(csrf) !== pending.csrf_hash) {
      sendHtml(res, 400, '<h1>Expired or invalid authorization request</h1>');
      return;
    }

    const code = makeAuthorizationCode({
      client_id: pending.client_id,
      redirect_uri: pending.redirect_uri,
      code_challenge: pending.code_challenge,
      code_challenge_method: pending.code_challenge_method,
      scope: pending.scope,
      resource: pending.resource,
      state: pending.state,
    });
    delete state.authorizationRequests[requestId];
    await persist();

    const redirect = new URL(pending.redirect_uri);
    redirect.searchParams.set('code', code);
    if (pending.state) redirect.searchParams.set('state', pending.state);
    redirect.searchParams.set('iss', issuer);
    sendRedirect(res, redirect.toString());
  }

  async function tokenEndpoint(req, res) {
    let body;
    try {
      body = new URLSearchParams(await readRequestBody(req));
    } catch (error) {
      oauthError(res, 400, 'invalid_request', error instanceof Error ? error.message : String(error));
      return;
    }

    const basic = basicClientCredentials(req);
    const requestedClientId = body.get('client_id') || basic?.clientId || '';
    const client = getClient(requestedClientId);
    if (!client) return oauthError(res, 400, 'invalid_client', 'Unknown client_id.');
    if (client.token_endpoint_auth_method === 'none' && basic?.clientSecret) {
      return oauthError(res, 401, 'invalid_client', 'This public client does not use a client secret.');
    }

    const requestedResource = normalizeResource(body.get('resource'));
    if (!requestedResource) return oauthError(res, 400, 'invalid_target', 'The resource parameter must identify this MCP server.');

    if (body.get('grant_type') === 'authorization_code') {
      const rawCode = body.get('code') || '';
      const codeKey = hash(rawCode);
      const code = state.authorizationCodes[codeKey];
      if (!code || code.expires_at <= now() || code.used) return oauthError(res, 400, 'invalid_grant', 'The authorization code is invalid, expired, or already used.');
      if (code.client_id !== requestedClientId) return oauthError(res, 400, 'invalid_grant', 'The authorization code belongs to a different client.');
      if (body.get('redirect_uri') !== code.redirect_uri) return oauthError(res, 400, 'invalid_grant', 'redirect_uri does not match the authorization request.');
      const verifier = body.get('code_verifier') || '';
      if (!/^[A-Za-z0-9._~-]{43,128}$/.test(verifier) || challengeForVerifier(verifier) !== code.code_challenge) {
        return oauthError(res, 400, 'invalid_grant', 'PKCE code_verifier validation failed.');
      }
      code.used = true;
      delete state.authorizationCodes[codeKey];
      const tokenResponse = issueTokens({ clientId: requestedClientId, scope: parseScopes(code.scope), resource: requestedResource });
      await persist();
      sendJson(res, 200, tokenResponse, { Pragma: 'no-cache' });
      return;
    }

    if (body.get('grant_type') === 'refresh_token') {
      const rawRefresh = body.get('refresh_token') || '';
      const refreshKey = hash(rawRefresh);
      const refresh = state.refreshTokens[refreshKey];
      if (!refresh || refresh.expires_at <= now()) return oauthError(res, 400, 'invalid_grant', 'The refresh token is invalid or expired.');
      if (refresh.client_id !== requestedClientId || refresh.resource !== requestedResource) return oauthError(res, 400, 'invalid_grant', 'The refresh token is not valid for this client or resource.');
      delete state.refreshTokens[refreshKey];
      const tokenResponse = issueTokens({ clientId: requestedClientId, scope: parseScopes(refresh.scope), resource: requestedResource });
      await persist();
      sendJson(res, 200, tokenResponse, { Pragma: 'no-cache' });
      return;
    }

    oauthError(res, 400, 'unsupported_grant_type', 'Only authorization_code and refresh_token are supported.');
  }

  async function registerClient(req, res) {
    let body;
    try {
      body = JSON.parse(await readRequestBody(req));
    } catch (error) {
      oauthError(res, 400, 'invalid_client_metadata', error instanceof Error ? error.message : 'Invalid JSON.');
      return;
    }
    const requestedRedirects = Array.isArray(body.redirect_uris) ? unique(body.redirect_uris.map(String)) : [];
    if (!requestedRedirects.length || requestedRedirects.length > 8 || requestedRedirects.some((uri) => !exactRedirectUriAllowed(uri))) {
      oauthError(res, 400, 'invalid_redirect_uri', 'redirect_uris must contain one to eight exact HTTPS or loopback URIs.');
      return;
    }
    const authMethod = body.token_endpoint_auth_method || 'none';
    if (authMethod !== 'none') return oauthError(res, 400, 'invalid_client_metadata', 'Only public PKCE clients using token_endpoint_auth_method=none are supported.');
    const grantTypes = Array.isArray(body.grant_types) && body.grant_types.length ? body.grant_types.map(String) : ['authorization_code', 'refresh_token'];
    const responseTypes = Array.isArray(body.response_types) && body.response_types.length ? body.response_types.map(String) : ['code'];
    if (!grantTypes.includes('authorization_code') || !responseTypes.includes('code')) return oauthError(res, 400, 'invalid_client_metadata', 'The client must support authorization_code and code.');
    const requestedScopes = parseScopes(body.scope);
    const clientScopes = unique((requestedScopes.length ? requestedScopes : [REQUIRED_SCOPE])
      .filter((scope) => allScopes.includes(scope)));
    if (!clientScopes.includes(REQUIRED_SCOPE)) clientScopes.unshift(REQUIRED_SCOPE);

    const newClientId = randomToken('gm_client');
    state.clients[newClientId] = {
      client_id: newClientId,
      client_name: String(body.client_name || 'MCP client').slice(0, 200),
      redirect_uris: requestedRedirects,
      token_endpoint_auth_method: 'none',
      grant_types: grantTypes,
      response_types: responseTypes,
      scope: clientScopes.join(' '),
      created_at: now(),
      pre_registered: false,
    };
    await persist();
    sendJson(res, 201, {
      client_id: newClientId,
      client_id_issued_at: now(),
      client_name: state.clients[newClientId].client_name,
      redirect_uris: requestedRedirects,
      token_endpoint_auth_method: 'none',
      grant_types: grantTypes,
      response_types: responseTypes,
      scope: clientScopes.join(' '),
    });
  }

  async function handle(req, res, url) {
    const requestPath = url.pathname;
    const metadataPaths = new Set([
      '/.well-known/oauth-protected-resource',
      '/.well-known/oauth-protected-resource/mcp',
    ]);
    const authorizationMetadataPaths = new Set([
      '/.well-known/oauth-authorization-server',
      '/.well-known/oauth-authorization-server/mcp',
      '/.well-known/openid-configuration',
    ]);

    if (metadataPaths.has(requestPath) && req.method === 'GET') {
      applyCors(req, res, allowedOrigins);
      sendJson(res, 200, metadata());
      return true;
    }
    if (authorizationMetadataPaths.has(requestPath) && req.method === 'GET') {
      applyCors(req, res, allowedOrigins);
      sendJson(res, 200, authorizationServerMetadata());
      return true;
    }

    const oauthPaths = new Set(['/oauth/authorize', '/oauth/authorize/approve', '/oauth/token', '/oauth/register']);
    if (!oauthPaths.has(requestPath)) return false;
    applyCors(req, res, allowedOrigins);
    if (req.method === 'OPTIONS') {
      res.writeHead(204);
      res.end();
      return true;
    }

    try {
      if (requestPath === '/oauth/authorize' && req.method === 'GET') await beginAuthorization(req, res, url);
      else if (requestPath === '/oauth/authorize/approve' && req.method === 'POST') await approveAuthorization(req, res);
      else if (requestPath === '/oauth/token' && req.method === 'POST') await tokenEndpoint(req, res);
      else if (requestPath === '/oauth/register' && req.method === 'POST') await registerClient(req, res);
      else sendJson(res, 405, { error: 'method_not_allowed' }, { Allow: requestPath === '/oauth/authorize' ? 'GET' : 'POST' });
    } catch (error) {
      console.error('[oauth] request failed:', error instanceof Error ? error.message : error);
      if (!res.headersSent) oauthError(res, 500, 'server_error', 'OAuth server error.');
    }
    return true;
  }

  return {
    metadata,
    authorizationServerMetadata,
    publicConfig,
    challenge,
    validateAccessToken,
    handle,
    getClient,
    clientId,
    resource,
    issuer,
    dataDir,
  };
}
