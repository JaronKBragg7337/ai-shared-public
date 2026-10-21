# crew-publish-loop.ps1 — no-admin publisher for the public crew page.
#
# Preferred path is the "Crew Publish" scheduled task (every 5 minutes).
# Windows sometimes refuses a new task without admin. HKCU Run can start
# this hidden loop instead. It runs tools/publish-crew.py every 5 minutes.
# No AI. One instance (exclusive lock file).
# The log gets time and ok/fail only. It never gets environment, keys, or response bodies.

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
if (Test-Path -Path 'variable:PSNativeCommandUseErrorActionPreference') {
    $PSNativeCommandUseErrorActionPreference = $false
}

$IntervalSec = 300
$Python = 'C:\Users\lilli\scoop\apps\python312\current\python.exe'
$Script = 'C:\Users\lilli\AI-Shared\tools\publish-crew.py'
$WorkDir = 'C:\Users\lilli\AI-Shared'
$LogPath = 'C:\Users\lilli\AI-Shared\state\crew-publish.log'
$LockPath = 'C:\Users\lilli\AI-Shared\state\crew-publish.lock'

function Write-PublishLog {
    param([Parameter(Mandatory = $true)][string]$Message)
    $dir = Split-Path -Parent $LogPath
    if (-not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    $line = '{0}  {1}{2}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message, [Environment]::NewLine
    $utf8 = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::AppendAllText($LogPath, $line, $utf8)
}

function Invoke-CrewPublish {
    if (-not (Test-Path -LiteralPath $Python) -or -not (Test-Path -LiteralPath $Script)) {
        Write-PublishLog 'fail  reason=publisher missing'
        return
    }
    $out = Join-Path $env:TEMP 'crew-publish-out.txt'
    $err = Join-Path $env:TEMP 'crew-publish-err.txt'
    try {
        $proc = Start-Process -FilePath $Python -ArgumentList @($Script) -WorkingDirectory $WorkDir -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput $out -RedirectStandardError $err
        $code = $proc.ExitCode
        if ($code -eq 0) { Write-PublishLog 'ok' } else { Write-PublishLog ('fail  exit=' + $code) }
    } catch {
        Write-PublishLog ('fail  reason=' + $_.Exception.GetType().Name)
    } finally {
        Remove-Item -LiteralPath $out, $err -Force -ErrorAction SilentlyContinue
    }
}

$script:LockStream = $null
try {
    try {
        $script:LockStream = [System.IO.File]::Open(
            $LockPath,
            [System.IO.FileMode]::OpenOrCreate,
            [System.IO.FileAccess]::ReadWrite,
            [System.IO.FileShare]::None)
    } catch {
        Write-PublishLog 'skip  reason=another publisher already running'
        exit 0
    }

    $script:LockStream.SetLength(0)
    $pidBytes = [System.Text.Encoding]::ASCII.GetBytes([string]$PID)
    $script:LockStream.Write($pidBytes, 0, $pidBytes.Length)
    $script:LockStream.Flush()
    Write-PublishLog ('watching  pid=' + $PID)

    while ($true) {
        Invoke-CrewPublish
        Start-Sleep -Seconds $IntervalSec
    }
} finally {
    if ($null -ne $script:LockStream) {
        $script:LockStream.Dispose()
    }
}
