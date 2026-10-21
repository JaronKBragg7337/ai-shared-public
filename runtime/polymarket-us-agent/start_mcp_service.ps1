$ErrorActionPreference = 'Stop'
$basePython = 'C:\Users\lilli\scoop\apps\python312\current'
$runtime = 'C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent'
$legacyRuntime = 'C:\Users\lilli\AppData\Local\polymarket-us-agent-runtime'
$venvPython = 'C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent-venv\Scripts\python.exe'
# Jaron keeps the credential on Google Drive, where he can find it. Look there first and
# fall back to the runtime dir, so this works whichever location is populated.
# Confirmed 2026-09-09: G:\My Drive\Secrets.Env.APIKeys\Polymarket.txt is present and valid
# (2 whitespace-separated tokens, as this script requires). Values were never read or copied.
# C: paths come FIRST on purpose. Google Drive mounted 46 seconds AFTER the logon tasks fired
# on 2026-09-09 - the same race that fails 'Grok Machine MCP' with 0x8007010B every boot. A
# service that must start at logon cannot depend on G: being mounted yet. G: stays last as a
# fallback so nothing breaks while the file is being moved.
$credentialCandidates = @(
    'C:\Users\lilli\.secrets\Polymarket.txt',
    'C:\Users\lilli\Secrets.Env.APIKeys\Polymarket.txt',
    (Join-Path $runtime 'Polymarket.txt'),
    (Join-Path $legacyRuntime 'Polymarket.txt'),
    'G:\My Drive\Secrets.Env.APIKeys\Polymarket.txt'
)
$credentialsFile = $credentialCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $credentialsFile) {
    throw "Polymarket credential file not found. Looked in: $($credentialCandidates -join ' ; ')"
}

$env:PATH = "$basePython;$env:PATH"
$env:SUPABASE_URL = 'https://ygjpnvrwhkrowkrskftk.supabase.co'
$env:SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_Y-duV64ayMMEvVwMs5PWuw_6kvzbOrN'
$env:QWEN_BRIDGE_TOKEN_FILE = Join-Path $runtime 'QwenBridge.token'
$credentialParts = @()
if (Test-Path -LiteralPath $credentialsFile) {
    $credentialText = (Get-Content -Raw -LiteralPath $credentialsFile).Trim()
    $credentialParts = @($credentialText -split '\s+', 2)
}
if ($credentialParts.Count -lt 2) {
    throw 'Polymarket credential file is missing the expected key ID and secret lines.'
}
$env:POLYMARKET_KEY_ID = $credentialParts[0]
$env:POLYMARKET_SECRET_KEY = $credentialParts[1]
$entrypoint = Join-Path $runtime 'http_server.py'
$stdout = Join-Path $runtime 'mcp-service.stdout.log'
$stderr = Join-Path $runtime 'mcp-service.stderr.log'
try {
    $process = Start-Process -FilePath $venvPython -ArgumentList @($entrypoint) -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru -Wait
    exit $process.ExitCode
} catch {
    @(
        ('type=' + $_.Exception.GetType().FullName),
        ('message=' + $_.Exception.Message),
        ('venv_exists=' + (Test-Path -LiteralPath $venvPython)),
        ('entrypoint_exists=' + (Test-Path -LiteralPath $entrypoint)),
        ('stdout_parent_exists=' + (Test-Path -LiteralPath $runtime))
    ) | Set-Content -LiteralPath (Join-Path $runtime 'mcp-launcher.error.log') -Encoding UTF8
    exit 1
}
