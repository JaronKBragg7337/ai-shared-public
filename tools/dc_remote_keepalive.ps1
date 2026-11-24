# dc_remote_keepalive.ps1 - keeps ChatGPT's way into the MSI (Desktop Commander "remote") alive. (Claude, 11/16)
# Run by the "Desktop Commander Remote" scheduled task at logon and every 10 minutes.
# If a desktop-commander "remote" process is already running, it does nothing. Otherwise it starts one the same way
# that worked by hand on 11/12 (npx ... remote) and appends the output to scratch/dc-remote.out.
$ErrorActionPreference = 'SilentlyContinue'
$log = 'C:\Users\lilli\AI-Shared\scratch\dc-keepalive.log'
$running = Get-CimInstance Win32_Process -Filter "Name='node.exe'" |
    Where-Object { $_.CommandLine -match 'desktop-commander' -and $_.CommandLine -match '\sremote' }
if ($running) { exit 0 }
Add-Content $log "$(Get-Date -Format s) not running -> starting"
$out = 'C:\Users\lilli\AI-Shared\scratch\dc-remote.out'
Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', "npx -y @wonderwhy-er/desktop-commander@latest remote >> `"$out`" 2>&1" `
    -WorkingDirectory 'C:\Users\lilli' -WindowStyle Hidden
Start-Sleep -Seconds 45
$ok = Get-CimInstance Win32_Process -Filter "Name='node.exe'" |
    Where-Object { $_.CommandLine -match 'desktop-commander' -and $_.CommandLine -match '\sremote' }
if ($ok) { Add-Content $log "$(Get-Date -Format s) started OK" } else { Add-Content $log "$(Get-Date -Format s) START FAILED, see dc-remote.out" }
