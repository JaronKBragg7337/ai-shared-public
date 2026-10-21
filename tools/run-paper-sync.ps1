# Keeps /live-systems/paper/ current. Reads the local paper simulator and mirrors it
# to Supabase every 2 minutes. Read-only against paper.db; touches nothing live.
$ErrorActionPreference = 'Continue'
$logDir = 'C:\Users\lilli\AI-Shared\logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir ('paper-sync-' + (Get-Date -Format 'yyyy-MM-dd') + '.log')
Set-Location 'C:\Users\lilli\AI-Shared'
& 'C:\Users\lilli\scoop\apps\python312\current\python.exe' 'tools\paper-sync.py' --loop 120 *>&1 |
  Tee-Object -FilePath $log -Append
exit $LASTEXITCODE
