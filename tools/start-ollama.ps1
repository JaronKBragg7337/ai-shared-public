# start-ollama.ps1 — starts Ollama at logon, and confirms it actually came up.
#
# WHY THIS EXISTS: Ollama shipped with a Startup-folder shortcut. On the 2026-09-10 reboot
# that shortcut silently did not start it — every other service came back via its AtLogOn
# scheduled task, and Ollama alone was dead, which meant Qwen was dead. Nothing reported it.
# Startup-folder items are staggered, can be skipped, and cannot retry. A scheduled task can.
#
# Ollama is the dependency the Polymarket MCP and the Qwen bridge both need, so this waits
# for the port to actually answer rather than assuming the launch worked.

$exe = "$env:LOCALAPPDATA\Programs\Ollama\ollama app.exe"
$log = "C:\Users\lilli\AI-Shared\logs\ollama-start.log"
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
function Log($m) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $m" | Tee-Object -FilePath $log -Append }

try {
    $r = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 5 -ErrorAction Stop
    if ($null -eq $r.models) { throw 'Missing models field' }
    Log 'Ollama API already answering - nothing to do'; exit 0
} catch { }
if (Get-NetTCPConnection -State Listen -LocalPort 11434 -ErrorAction SilentlyContinue) {
    Log 'FAILED: port 11434 occupied but Ollama API unhealthy'; exit 1
}
if (-not (Test-Path -LiteralPath $exe)) { Log "FAILED: $exe not found"; exit 1 }

Log "starting $exe"
Start-Process -FilePath $exe -WindowStyle Hidden

# Wait up to 90s for it to actually answer, not just for the process to exist.
for ($i = 0; $i -lt 18; $i++) {
    Start-Sleep -Seconds 5
    try {
        $r = Invoke-RestMethod -Uri 'http://localhost:11434/api/tags' -TimeoutSec 5
        if ($null -eq $r.models) { throw 'Missing models field' }
        Log "UP after $(($i+1)*5)s polling delay - $($r.models.Count) models available"
        exit 0
    } catch { }
}
Log "FAILED: started but port 11434 never answered within 90s"
exit 1
