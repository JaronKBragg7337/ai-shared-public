$ErrorActionPreference = 'Stop'
& python 'C:\Users\lilli\AI-Shared\tools\desk-trade.py' `
  --by 'grok-bot/live-wire' `
  --slug 'aec-cfb-flam-alast-2026-10-10' `
  --side 'yes' `
  --size '10' `
  --why 'FAMU28-ALST27 4:07 4Q ESPN FAMU WP81 vs ask0.615 ~20c after comeback' `
  --kill 'ALST takes lead or FAMU WP under ask'
Write-Host "exit=$LASTEXITCODE"
