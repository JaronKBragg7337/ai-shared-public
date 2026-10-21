$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$taskName = 'Grok Machine MCP'
$node = (Get-Command node.exe -ErrorAction Stop).Source
$serverFile = Join-Path $projectRoot 'server.mjs'

$action = New-ScheduledTaskAction -Execute $node -Argument "`"$serverFile`"" -WorkingDirectory $projectRoot
$trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit ([TimeSpan]::Zero)

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
Write-Host "Installed '$taskName' to start at interactive logon."

$listener = Get-NetTCPConnection -LocalPort 3001 -State Listen -ErrorAction SilentlyContinue
if (-not $listener) {
  Start-ScheduledTask -TaskName $taskName
  Write-Host 'Started the task now.'
} else {
  Write-Host 'The MCP port is already listening; leaving the current server running.'
}
