$ErrorActionPreference = 'Stop'
$basePython = 'C:\Users\lilli\scoop\apps\python312\current'
$runtime = 'C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent'
$venvPython = 'C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent-venv\Scripts\python.exe'
$env:PATH = "$basePython;$env:PATH"
$env:PYTHONUTF8 = '1'
$env:SUPABASE_URL = 'https://ygjpnvrwhkrowkrskftk.supabase.co'
$env:SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_Y-duV64ayMMEvVwMs5PWuw_6kvzbOrN'
$env:QWEN_BRIDGE_TOKEN_FILE = Join-Path $runtime 'QwenBridge.token'
$env:QWEN_ID = 'polymarket-qwen'
$env:OPENCLAW_AGENT_ID = 'polymarket'
$env:OPENCLAW_SESSION_KEY = 'agent:polymarket:qwen-remote'
$env:POLYMARKET_MCP_URL = 'http://127.0.0.1:8765/mcp'

function Wait-ForPort {
    param(
        [string]$TargetHost,
        [int]$Port,
        [int]$TimeoutSeconds = 300
    )

    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    do {
        $client = [System.Net.Sockets.TcpClient]::new()
        try {
            $connect = $client.ConnectAsync($TargetHost, $Port)
            if ($connect.Wait(1000) -and $client.Connected) {
                return
            }
        } catch {
            # The dependency is still starting; retry until the deadline.
        } finally {
            $client.Dispose()
        }
        Start-Sleep -Seconds 2
    } while ([DateTime]::UtcNow -lt $deadline)

    throw ('Timed out waiting for ' + $TargetHost + ':' + $Port)
}

# Both services are logon-started. Wait here so task order and the 46-second
# Google Drive mount race cannot strand the bridge after a reboot.
Wait-ForPort -TargetHost '127.0.0.1' -Port 8765
Wait-ForPort -TargetHost '127.0.0.1' -Port 18789

# A running gateway is not proof that its model dependency is ready.
$modelDeadline = [DateTime]::UtcNow.AddMinutes(5)
$modelReady = $false
do {
    try {
        $modelReply = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 5 -ErrorAction Stop
        if ($null -eq $modelReply.models) { throw 'Missing models field' }
        $modelReady = $true
        break
    } catch {
        Write-Warning 'Qwen bridge dependency unavailable: Ollama API. Retrying.'
    }
    Start-Sleep -Seconds 2
} while ([DateTime]::UtcNow -lt $modelDeadline)
if (-not $modelReady) {
    'Ollama API unavailable after five minutes; task must retry.' | Set-Content -LiteralPath (Join-Path $runtime 'qwen-bridge-launcher.error.log')
    exit 1
}

$entrypoint = Join-Path $runtime 'remote_bridge.py'
$stdout = Join-Path $runtime 'qwen-bridge.stdout.log'
$stderr = Join-Path $runtime 'qwen-bridge.stderr.log'
try {
    $process = Start-Process -FilePath $venvPython -ArgumentList @($entrypoint) -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru -Wait
    exit $process.ExitCode
} catch {
    @(
        ('type=' + $_.Exception.GetType().FullName),
        ('message=' + $_.Exception.Message)
    ) | Set-Content -LiteralPath (Join-Path $runtime 'qwen-bridge-launcher.error.log') -Encoding UTF8
    exit 1
}
