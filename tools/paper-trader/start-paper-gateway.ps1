$ErrorActionPreference = 'Stop'
# Explicitly isolated process/config/session state; never restart the live gateway.
$env:OPENCLAW_STATE_DIR = 'C:\Users\lilli\.openclaw-polymarket-paper'
$env:OPENCLAW_CONFIG_PATH = 'C:\Users\lilli\.openclaw-polymarket-paper\openclaw.json'
$env:OPENCLAW_GATEWAY_PORT = '19789'
$env:OPENCLAW_WINDOWS_TASK_NAME = 'OpenClaw Paper Gateway'
$env:PM_TRADER_HOME = 'C:\Users\lilli\AI-Shared\tools\paper-trader\data'
foreach ($item in Get-ChildItem Env:) {
    if ($item.Name -match '(TOKEN|SECRET|PASSWORD|API_KEY|APIKEY|PRIVATE_KEY)') {
        Remove-Item -LiteralPath ('Env:' + $item.Name)
    }
}
$deadline = [DateTime]::UtcNow.AddMinutes(5)
$ready = $false
do {
    try {
        $reply = Invoke-RestMethod 'http://127.0.0.1:11434/api/tags' -TimeoutSec 5
        if ($null -eq $reply.models) { throw 'Invalid Ollama response' }
        $ready = $true
        break
    } catch { Start-Sleep -Seconds 2 }
} while ([DateTime]::UtcNow -lt $deadline)
if (-not $ready) { Write-Error 'PAPER ONLY: Ollama unavailable'; exit 1 }
$root = 'C:\Users\lilli\AI-Shared\tools\paper-trader'
try {
    while ($true) {
        $process = Start-Process -FilePath 'C:\Program Files\nodejs\node.exe' -ArgumentList @('C:\Users\lilli\AppData\Roaming\npm\node_modules\openclaw\dist\index.js','--profile','polymarket-paper','gateway','--port','19789') -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput (Join-Path $root 'paper-gateway.stdout.log') -RedirectStandardError (Join-Path $root 'paper-gateway.stderr.log') -PassThru -Wait
        if ($process.ExitCode -ne 0) { exit $process.ExitCode }
        # OpenClaw requests supervisor restarts with a clean process exit.
        # A one-shot task would otherwise stay Ready with no gateway listening.
        Start-Sleep -Seconds 5
    }
} catch { Write-Error 'PAPER ONLY gateway launch failed'; exit 1 }
