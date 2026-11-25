# postboot-check.ps1 — run this right after a reboot, BEFORE funding anything.
# Answers one question with a yes or a no: did the whole stack come back on its own?
#
# Nothing here starts, stops, changes or trades anything. It only looks.
# Run it by double-clicking, or: powershell -ExecutionPolicy Bypass -File this-file

$ErrorActionPreference = 'Continue'
$fail = 0
function Ok($m)   { Write-Host "  PASS  $m" -ForegroundColor Green }
function Bad($m)  { Write-Host "  FAIL  $m" -ForegroundColor Red; $script:fail++ }
function Note($m) { Write-Host "        $m" -ForegroundColor DarkGray }

Write-Host ""
Write-Host "POST-REBOOT CHECK" -ForegroundColor Cyan
$boot = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
$mins = [math]::Round(((Get-Date) - $boot).TotalMinutes)
Write-Host "Booted $boot  ($mins min ago)"
if ($mins -gt 180) { Write-Host "  NOTE: that was a while ago - is this actually a fresh boot?" -ForegroundColor Yellow }
Write-Host ""

Write-Host "1. Services listening" -ForegroundColor Cyan
foreach ($p in @(@{n='Ollama (the model)';port=11434}, @{n='Heartbeat MCP';port=3001})) {
    if (Get-NetTCPConnection -State Listen -LocalPort $p.port -ErrorAction SilentlyContinue) { Ok "$($p.n) - port $($p.port)" }
    else { Bad "$($p.n) - port $($p.port) NOT listening" }
}

Write-Host ""
Write-Host "2. Scheduled tasks came back" -ForegroundColor Cyan
foreach ($n in @('Ollama Server','Polymarket MCP','Qwen Remote Bridge','Revenue Desk Daily')) {
    $t = Get-ScheduledTask -TaskName $n -ErrorAction SilentlyContinue
    if (-not $t) { Bad "$n - task MISSING"; continue }
    $i = $t | Get-ScheduledTaskInfo
    Note "$n last start: $($i.LastRunTime); last result: $($i.LastTaskResult). Running is process state, NOT dependency health."
    if ($n -ne 'Revenue Desk Daily' -and $i.LastRunTime -lt $boot) { Bad "$n has not started since this boot" }
    # 267009 = currently running, 0 = last run succeeded. Both are fine.
    $expectedStates = if ($n -in 'Polymarket MCP','Qwen Remote Bridge') { @('Running') } else { @('Running','Ready') }
    if ($t.State -in $expectedStates -and $i.LastTaskResult -in 0,267009) { Ok "$n - $($t.State)" }
    else { Bad "$n - State=$($t.State) LastResult=$($i.LastTaskResult)" }
}

Write-Host ""
Write-Host "3. Model API metadata (generation is not tested)" -ForegroundColor Cyan
try {
    $r = Invoke-RestMethod -Uri 'http://localhost:11434/api/tags' -TimeoutSec 20
    if ($null -eq $r.models) { throw 'Ollama response missing models field' }
    Ok "Ollama API responded - $($r.models.Count) models installed (generation not tested)"
    Note (($r.models | ForEach-Object { $_.name }) -join ', ')
} catch { Bad "Ollama did not answer: $_" }

Write-Host ""
Write-Host "4. Polymarket MCP is serving, not just holding a socket" -ForegroundColor Cyan
# Root 404 is expected; a 5xx is a responding but unhealthy service, never a pass.
$code = $null; $connErr = $null
try   { $code = (Invoke-WebRequest -Uri 'http://127.0.0.1:8765/' -TimeoutSec 20 -UseBasicParsing).StatusCode }
catch { if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode } else { $connErr = $_.Exception.Message } }
if ($code -in 200,404) { Ok "MCP root probe answered expected HTTP $code (RPC not tested)" }
elseif ($code)   { Bad "MCP root probe returned unexpected HTTP $code" }
elseif ($connErr) { Bad "MCP service did not answer: $connErr" }
else              { Bad "MCP service did not answer (no response, no error)" }

Write-Host ""
Write-Host "5. Credential the launcher needs is reachable on C:" -ForegroundColor Cyan
$cands = @(
  'C:\Users\lilli\.secrets\Polymarket.txt',
  'C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent\Polymarket.txt',
  'C:\Users\lilli\AppData\Local\polymarket-us-agent-runtime\Polymarket.txt'
)
$found = $cands | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if ($found) {
    Ok "credential found on C: (no Google Drive dependency at boot)"
    Note $found
} else { Bad "credential NOT found on any C: path - the service cannot start unattended" }

Write-Host ""
Write-Host "6. Periodic jobs and fresh output" -ForegroundColor Cyan
$root = Split-Path $PSScriptRoot -Parent
foreach ($job in @(
    @{Name='Trade Proposer'; Minutes=160; File='state/proposer.md'},
    @{Name='Trade Verifier'; Minutes=15; File='state/verifier.md'},
    @{Name='Trade Executor'; Minutes=15; File='state/executor.md'},
    @{Name='Scout Scorer'; Minutes=1560; File='state/scout-scores.md'},
    @{Name='Usage Snapshot'; Minutes=35; File='state/usage-live.json'},
    @{Name='AI-Shared Mirror'; Minutes=1560; File='state/mirror.log'}
)) {
    $t = Get-ScheduledTask -TaskName $job.Name -ErrorAction SilentlyContinue
    if (-not $t) { Bad "$($job.Name) - task MISSING"; continue }
    $i = $t | Get-ScheduledTaskInfo
    $age = ((Get-Date) - $i.LastRunTime).TotalMinutes
    $valid = if ($job.Name -eq 'AI-Shared Mirror') { @(0,1,2,3,4,5,6,7) } else { @(0) }
    if ($t.State -eq 'Running') { Note "$($job.Name) is running; completion not verified" }
    elseif ($t.State -eq 'Ready' -and $i.LastTaskResult -in $valid -and $age -le $job.Minutes) { Ok "$($job.Name) last completed successfully; $([int]$age) minutes ago" }
    else { Bad "$($job.Name) State=$($t.State) Result=$($i.LastTaskResult) LastRunAge=$([int]$age) minutes" }
    $f = Get-Item -LiteralPath (Join-Path $root $job.File) -ErrorAction SilentlyContinue
    if (-not $f -or ((Get-Date) - $f.LastWriteTime).TotalMinutes -gt $job.Minutes) { Bad "$($job.Name) output missing or stale: $($job.File)" }
}
foreach ($n in @('Grok Machine MCP','Desktop Commander Remote','Fly Brain')) {
    $t = Get-ScheduledTask -TaskName $n -ErrorAction SilentlyContinue
    if ($t -and $t.State -eq 'Running') { Ok "$n running (historical duplicate-start result is not a process failure)" }
    else { Bad "$n is not running" }
}
foreach ($n in @('Paper Sync','OpenClaw Paper Gateway')) {
    $t = Get-ScheduledTask -TaskName $n -ErrorAction SilentlyContinue
    if ($t -and $t.State -eq 'Disabled') { Ok "$n remains intentionally disabled" }
    else { Bad "$n differs from the recorded paused state" }
}
foreach ($entry in @(@{File='state/bridge-health.md'; Minutes=100}, @{File='state/fly-brain/log.md'; Minutes=10})) {
    $f = Get-Item -LiteralPath (Join-Path $root $entry.File) -ErrorAction SilentlyContinue
    if ($f -and ((Get-Date) - $f.LastWriteTime).TotalMinutes -le $entry.Minutes) { Ok "$($entry.File) recently updated (content/outcome not validated)" }
    else { Bad "$($entry.File) missing or stale" }
}
Write-Host ""
if ($fail -eq 0) {
    Write-Host "RESULT: all checked endpoints and task states pass RIGHT NOW; model generation and end-to-end work are unverified." -ForegroundColor Green
    Write-Host ""
    Write-Host "  IMPORTANT: this proves the stack is UP. It cannot prove it came up BY ITSELF." -ForegroundColor Yellow
    Write-Host "  If anyone started a service by hand since boot, this still shows green." -ForegroundColor Yellow
    Write-Host "  For a true autostart test: reboot, then run this FIRST, before touching anything." -ForegroundColor Yellow
    Write-Host "  (On 2026-09-10 Ollama did NOT autostart. Everything else did.)" -ForegroundColor Yellow
} else {
    Write-Host "RESULT: $fail check(s) failed. Investigate the failures above." -ForegroundColor Red
    Write-Host "Send this output to Claude or Codex - a failure here is exactly what this test is for." -ForegroundColor Yellow
}
Write-Host ""
if ($fail -gt 0) { exit 1 }
