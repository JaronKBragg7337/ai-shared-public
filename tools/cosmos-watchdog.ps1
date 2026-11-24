# cosmos-watchdog.ps1 — no-admin crash restart for The Cosmos authority.
#
# Windows refused a scheduled task (no admin). The HKCU Run entry starts this
# hidden loop instead of the server. This process starts the server itself.
# Every 30s it checks http://127.0.0.1:8390/health. Three failures in a row:
# stop whatever is listening on 8390, then start start-authority.ps1 hidden.
# A healthy server is left alone. One instance only (exclusive lock file).
# The log gets time and reason. It never gets environment, keys, or response bodies.

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
if (Test-Path -Path 'variable:PSNativeCommandUseErrorActionPreference') {
    $PSNativeCommandUseErrorActionPreference = $false
}

$HealthUrl = 'http://127.0.0.1:8390/health'
$IntervalSec = 30
$FailLimit = 3
# A fresh authority loads the world from Supabase and catches up before it listens. Under load that took longer than three failed checks (90 s),
# so the watchdog killed it mid-start, again and again (about 40 restarts between 7 and 9 PM on 2026-10-02). Failures do not count during this grace.
$StartGraceSec = 240
$StartScript = 'C:\Users\lilli\Projects\heartbeat-observatory\games\the-cosmos\server\start-authority.ps1'
$LogPath = 'C:\Users\lilli\AI-Shared\state\cosmos-watchdog.log'
$LockPath = 'C:\Users\lilli\AI-Shared\state\cosmos-watchdog.lock'

function Write-WatchdogLog {
    param([Parameter(Mandatory = $true)][string]$Message)
    $dir = Split-Path -Parent $LogPath
    if (-not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    $line = '{0}  {1}{2}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message, [Environment]::NewLine
    $utf8 = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::AppendAllText($LogPath, $line, $utf8)
}

function Get-HealthState {
    # Fixed words only. Exception text and the body stay out of the log.
    try {
        $resp = Invoke-WebRequest -Uri $HealthUrl -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        $code = [int]$resp.StatusCode
        if ($code -ne 200) { return ('http-' + $code) }
        $json = $resp.Content | ConvertFrom-Json
        if ($json.ok -eq $true) { return 'ok' }
        return 'not-ok'
    } catch {
        $code = 0
        try {
            if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode }
        } catch {
            $code = 0
        }
        if ($code -gt 0) { return ('http-' + $code) }
        $kind = [string]$_.Exception.Message
        if ($kind -match 'timed out|timeout') { return 'timeout' }
        if ($kind -match 'refused') { return 'connection-refused' }
        return 'no-response'
    }
}

function Get-ListenPids {
    # One integer per pipeline object. Do not return an array: PowerShell unwraps it
    # and the caller then treats the whole list as a single process id.
    $seen = @{}
    $netstat = @(& netstat.exe -ano -p tcp)
    foreach ($line in $netstat) {
        if ($line -match '^\s*TCP\s+\S+:8390\s+\S+\s+LISTENING\s+(\d+)\s*$') {
            $procId = [int]$Matches[1]
            if ($procId -gt 4 -and $procId -ne $PID -and -not $seen.ContainsKey($procId)) {
                $seen[$procId] = $true
                Write-Output $procId
            }
        }
    }
}

function Get-PortStopNote {
    $ids = @(Get-ListenPids)
    if ($ids.Count -eq 0) { return 'nothing held port 8390' }
    $stopped = New-Object System.Collections.Generic.List[int]
    foreach ($procId in $ids) {
        $id = [int]$procId
        try {
            Stop-Process -Id $id -Force -ErrorAction Stop
        } catch {
            & taskkill.exe /PID $id /F *> $null
        }
        $stopped.Add($id)
    }
    $deadline = (Get-Date).AddSeconds(15)
    do {
        $left = @(Get-ListenPids)
        if ($left.Count -eq 0) { break }
        Start-Sleep -Milliseconds 300
    } while ((Get-Date) -lt $deadline)
    $left = @(Get-ListenPids)
    if ($left.Count -gt 0) { return 'port 8390 still listening after stop' }
    return ('stopped pid ' + (($stopped.ToArray()) -join ','))
}

function Start-AuthorityHidden {
    # Same PowerShell that is running this watchdog. WindowsApps often fails Test-Path.
    $shell = Join-Path $PSHOME 'pwsh.exe'; if (-not (Test-Path -LiteralPath $shell)) { $shell = (Get-Command pwsh.exe -ErrorAction SilentlyContinue).Source }; if (-not $shell) { $shell = Join-Path $PSHOME 'powershell.exe' }   # 10/26: started from Windows PowerShell, PSHOME has no pwsh.exe -> launch failed
    $null = Start-Process -FilePath $shell -ArgumentList @(
        '-NoProfile',
        '-WindowStyle', 'Hidden',
        '-ExecutionPolicy', 'Bypass',
        '-File', $StartScript
    ) -WindowStyle Hidden -PassThru
}

function Restart-Authority {
    param([Parameter(Mandatory = $true)][string]$LastState)
    $stoppedNote = 'port stop failed'
    try {
        $stoppedNote = [string](Get-PortStopNote)
    } catch {
        $stoppedNote = 'port stop failed (' + $_.Exception.GetType().Name + ')'
    }
    $launchNote = 'launch failed'
    try {
        if (-not (Test-Path -LiteralPath $StartScript)) {
            $launchNote = 'start script missing'
        } else {
            Start-AuthorityHidden
            $launchNote = 'launched start-authority.ps1'
        }
    } catch {
        $launchNote = 'launch failed (' + $_.Exception.GetType().Name + ')'
    }
    Write-WatchdogLog ('restart  reason=3 consecutive health failures (last: {0}); {1}; {2}' -f $LastState, $stoppedNote, $launchNote)
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
        Write-WatchdogLog 'skip  reason=another watchdog already running'
        exit 0
    }

    $script:LockStream.SetLength(0)
    $pidBytes = [System.Text.Encoding]::ASCII.GetBytes([string]$PID)
    $script:LockStream.Write($pidBytes, 0, $pidBytes.Length)
    $script:LockStream.Flush()

    $failures = 0
    $graceUntil = (Get-Date).AddSeconds(0)
    $first = $true
    while ($true) {
        try {
            $state = Get-HealthState
            if ($first) {
                Write-WatchdogLog ('watching  pid={0}  health={1}' -f $PID, $state)
                $first = $false
            }
            if ($state -eq 'ok') {
                $failures = 0
            } elseif ((Get-Date) -lt $graceUntil) {
                $failures = 0
            } else {
                $failures++
                if ($failures -ge $FailLimit) {
                    Restart-Authority -LastState $state
                    $failures = 0
                    $graceUntil = (Get-Date).AddSeconds($StartGraceSec)
                }
            }
        } catch {
            if ($first) {
                Write-WatchdogLog ('watching  pid={0}  health=check-error' -f $PID)
                $first = $false
            }
            $failures++
            if ($failures -ge $FailLimit) {
                Restart-Authority -LastState 'check-error'
                $failures = 0
            }
        }
        Start-Sleep -Seconds $IntervalSec
    }
} finally {
    if ($null -ne $script:LockStream) {
        $script:LockStream.Dispose()
    }
}
