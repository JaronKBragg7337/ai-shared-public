$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

$localNodeModules = Join-Path $env:LOCALAPPDATA 'grok-machine-mcp-runtime\node_modules'
if (Test-Path -LiteralPath (Join-Path (Get-Location) 'node_modules\@modelcontextprotocol\sdk')) {
  Remove-Item Env:GROK_MACHINE_NODE_MODULES -ErrorAction SilentlyContinue
} elseif (Test-Path -LiteralPath (Join-Path $localNodeModules '@modelcontextprotocol\sdk')) {
  $env:GROK_MACHINE_NODE_MODULES = $localNodeModules
} else {
  npm install
}

if (-not (Test-Path -LiteralPath '.env')) {
  $token = node -e "console.log(require('node:crypto').randomBytes(48).toString('base64url'))"
  $defaultCwd = (Resolve-Path (Join-Path $projectRoot '..\..')).Path
  @(
    'MCP_PUBLIC_HOST=mcp.heartbeatobservatory.com'
    'MCP_HOST=127.0.0.1'
    'MCP_PORT=3001'
    "MCP_AUTH_TOKEN=$token"
    'MCP_OAUTH_ISSUER=https://mcp.heartbeatobservatory.com'
    'MCP_RESOURCE_IDENTIFIER=https://mcp.heartbeatobservatory.com/mcp'
    'MCP_OAUTH_CLIENT_ID=grok-machine-ios'
    'MCP_ALLOWED_ORIGINS=https://grok.com,https://www.grok.com,https://x.com,https://www.x.com'
    "MCP_DEFAULT_CWD=$defaultCwd"
    'MCP_MAX_COMMAND_TIMEOUT_MS=120000'
    'MCP_MAX_OUTPUT_CHARS=200000'
  ) | Set-Content -LiteralPath '.env' -Encoding utf8NoBOM
  Write-Host 'Created .env with a new MCP_AUTH_TOKEN.' -ForegroundColor Green
  Write-Host 'The Grok iOS connector uses the pre-registered OAuth PKCE client shown in README.md.' -ForegroundColor Yellow
}

node server.mjs
