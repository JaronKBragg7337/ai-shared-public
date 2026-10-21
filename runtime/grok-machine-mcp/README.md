# Grok Machine MCP

Standalone Streamable HTTP MCP server for connecting the Grok app to this
Windows computer through the existing Cloudflare Tunnel route.

The server listens only on `127.0.0.1:3001`. Cloudflare Tunnel is expected to
publish `https://mcp.heartbeatobservatory.com` to that local address. Grok's
connector URL is:

```text
https://mcp.heartbeatobservatory.com/mcp
```

The server exposes the existing full current-user capability set:

- arbitrary PowerShell and command execution;
- file and directory read/write/copy/move/delete/search;
- process and application launch/stop/list;
- active-window inspection and focus;
- mouse movement, clicks, and drags;
- keyboard keys, hotkeys, and text typing;
- clipboard read/write;
- full-screen capture returned as an MCP image;
- browser URL opening and basic system information.

It also exposes the modular foundation added on top of those original tools:

- durable background tasks with persisted status, logs, cancellation, and continuation;
- verification for files, processes, ports, HTTP responses, Git status, and visible windows;
- local Ollama model listing, chat, generation, embeddings, pulls, and loaded-model status;
- a persistent project/machine registry for projects, known ports, launch commands, and local models.

The original 27 machine-control tools remain registered unchanged; the current
server advertises 49 tools in total.

It does not elevate privileges. Commands run as the Windows user that starts
the process.

## Start

From PowerShell:

```powershell
cd 'G:\My Drive\Codex Active\projects\grok-machine-mcp'
npm install
Copy-Item .env.example .env
node -e "console.log(require('node:crypto').randomBytes(48).toString('base64url'))"
# Paste that value after MCP_AUTH_TOKEN= in .env
npm start
```

The included `scripts\start.ps1` creates `.env` with a random token on first
run and starts the server.

To start it automatically when this Windows user logs in:

```powershell
.\scripts\install-task.ps1
```

That task runs at the normal interactive-user privilege level so the UI tools
can see and control the desktop. Remove it with
`.\scripts\uninstall-task.ps1`.

## Grok iOS connector

Use the Grok custom connector URL:

- Name: `Grok Machine`
- Server URL: `https://mcp.heartbeatobservatory.com/mcp`

When Grok asks for OAuth credentials, enter:

```text
Client ID: grok-machine-ios
Client Secret: LEAVE BLANK
Authorization Endpoint: https://mcp.heartbeatobservatory.com/oauth/authorize
Token Endpoint: https://mcp.heartbeatobservatory.com/oauth/token
Scopes: mcp:tools
Token Auth Method: none (PKCE only, recommended)
```

The client is pre-registered as a public PKCE client. Grok should open the
authorization page, where you approve access, then return to the connector.
The server validates the exact redirect URI, S256 code verifier, resource
audience, one-time authorization code, and bearer access token. Refresh tokens
are issued for reconnection and OAuth state is persisted under
`%LOCALAPPDATA%\GrokMachineMcp` by default.

The standards discovery endpoints are:

- Protected-resource metadata:
  `https://mcp.heartbeatobservatory.com/.well-known/oauth-protected-resource/mcp`
- Authorization-server metadata:
  `https://mcp.heartbeatobservatory.com/.well-known/oauth-authorization-server`

The legacy `MCP_AUTH_TOKEN` bearer path remains available for xAI API/CLI
clients and regression checks; it does not remove or change any MCP tools.

Grok should discover the tools after the local server and Cloudflare Tunnel are
both running.

## Local checks

```powershell
npm run check
npm run smoke
npm run oauth-smoke
Invoke-WebRequest http://127.0.0.1:3001/healthz
Invoke-WebRequest https://mcp.heartbeatobservatory.com/healthz
```

`oauth-smoke` runs the authorization-code + PKCE exchange, invalid-verifier
check, authenticated MCP initialize, complete tools/list check, legacy and
foundation-tool calls (including a real durable task and local Ollama chat),
and refresh-token reconnection. Set `MCP_BASE_URL` to the public Cloudflare URL
to run it through the tunnel. The public health check may return `502` until
the local server is running.
