# Install only when ready. Run in the signed-in desktop account; this script does not start it.
$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $PSScriptRoot 'remote\.venv\Scripts\pythonw.exe'
$agent = Join-Path $PSScriptRoot 'remote_agent.py'
$action = New-ScheduledTaskAction -Execute $python -Argument ('"' + $agent + '"') -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName 'HB Remote Screen' -Action $action -Trigger $trigger -Principal $principal -Description 'Off until state/remote.enable exists; remove it or create state/remote.disable to stop.'
