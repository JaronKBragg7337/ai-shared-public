$ErrorActionPreference = 'Stop'
$taskName = 'Grok Machine MCP'
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
Write-Host "Removed '$taskName' scheduled startup task."
