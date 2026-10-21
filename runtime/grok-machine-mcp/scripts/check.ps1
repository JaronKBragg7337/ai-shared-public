$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

npm run check
$localNodeModules = Join-Path $env:LOCALAPPDATA 'grok-machine-mcp-runtime\node_modules'
if (-not (Test-Path -LiteralPath (Join-Path (Get-Location) 'node_modules\@modelcontextprotocol\sdk')) -and (Test-Path -LiteralPath (Join-Path $localNodeModules '@modelcontextprotocol\sdk'))) {
  $env:GROK_MACHINE_NODE_MODULES = $localNodeModules
} elseif (-not (Test-Path -LiteralPath (Join-Path (Get-Location) 'node_modules\@modelcontextprotocol\sdk'))) {
  npm install
}
npm run smoke

try {
  $local = Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:3001/healthz' -TimeoutSec 5
  Write-Host "Local health: $($local.StatusCode) $($local.Content)"
} catch {
  Write-Host 'Local health: server is not currently running.' -ForegroundColor Yellow
}

try {
  $public = Invoke-WebRequest -UseBasicParsing -Uri 'https://mcp.heartbeatobservatory.com/healthz' -TimeoutSec 15
  Write-Host "Public health: $($public.StatusCode) $($public.Content)"
} catch {
  Write-Host "Public health: $($_.Exception.Message)" -ForegroundColor Yellow
}
