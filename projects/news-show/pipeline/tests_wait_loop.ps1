# Simulates the REAL render wait loop from run_rendered_news.ps1 (extracted verbatim) with a fake clock, fake Unreal process,
# fake frame counts and fake kills. Nothing real is started, stopped or written (only a temp plan.json).
param([string]$File = 'C:\Users\lilli\AI-Shared\projects\news-show\pipeline\run_rendered_news.ps1')
$ErrorActionPreference = "Stop"
$src = Get-Content $File -Raw
$m = [regex]::Match($src, '(?s)(  \$planFrames = .*?\r?\n  \})\r?\n  # 10/15')
if (-not $m.Success) { "LOOP NOT FOUND"; exit 1 }
$loop = [scriptblock]::Create($m.Groups[1].Value)

$tmp = Join-Path $env:TEMP "waitloop_$PID"; New-Item -ItemType Directory -Force $tmp | Out-Null
$Out = $tmp; $Frames = Join-Path $tmp "frames"

# ---- mocks (functions win over cmdlets) ----
function Get-Date { param($Hour, $Minute, $Second, $Format)
    if ($PSBoundParameters.ContainsKey('Hour')) { return $script:now.Date.AddHours($Hour).AddMinutes($Minute).AddSeconds($Second) }
    return $script:now }
function Get-ChildItem { param($Path, $Filter, $ErrorAction, [switch]$Directory)
    $mins = ($script:now - $script:start).TotalMinutes
    return [pscustomobject]@{ Count = [int](& $script:frameFn $mins) } }
function Stop-Process { param([Parameter(ValueFromPipeline = $true)]$InputObject, $Id, [switch]$Force)
    process { $script:kills += [math]::Round(($script:now - $script:start).TotalMinutes); $script:exitAt = $script:now; $script:p.HasExited = $true } }
function Get-Process { param($Name, $ErrorAction) return $null }
function Start-Sleep { param($Seconds) $script:now = $script:now.AddSeconds($Seconds) }
function Say($msg) { $script:said += ("[{0:N0} min] {1}" -f ($script:now - $script:start).TotalMinutes, $msg) }

function Run-Scenario($name, $spatial, $plan, $frameFn, $exitAfterMin) {
    '{"frames": ' + $plan + '}' | Set-Content "$tmp/plan.json"
    $env:EP_SPATIAL = $spatial
    $script:start = [datetime]"2026-11-24 03:52"; $script:now = $script:start
    $script:frameFn = $frameFn; $script:kills = @(); $script:said = @()
    $script:exitAt = if ($null -ne $exitAfterMin) { $script:start.AddMinutes($exitAfterMin) } else { $null }
    $script:p = [pscustomobject]@{ Id = 4242; HasExited = $false }
    $script:p | Add-Member -MemberType ScriptMethod -Name WaitForExit -Value {
        param($ms)
        $until = $script:now.AddMilliseconds($ms)
        if ($null -ne $script:exitAt -and $script:exitAt -le $until) { $script:now = $script:exitAt; $this.HasExited = $true; return $true }
        $script:now = $until; return $false }
    $p = $script:p
    . $loop
    $endMin = [math]::Round(($script:now - $script:start).TotalMinutes)
    $n = [int](& $frameFn (($script:now - $script:start).TotalMinutes))
    "{0,-44} loop ended at {1,4} min | frames {2,6} of {3} | killed at: {4} | said: {5}" -f $name, $endMin, $n, $plan,
        ($(if ($script:kills.Count) { ($script:kills -join ',') + ' min' } else { 'never' })), ($script:said -join ' / ')
}

$fastRate = 690   # frames/min (~11.5/s), after 2 min startup
$fullRate = 168   # frames/min (~2.8/s), after 10 min startup
Run-Scenario "S1 FAST healthy, quits at the end" "1" 26975 { param($m) [math]::Min(26975, [math]::Max(0, ($m - 2) * $fastRate)) } (2 + 26975 / $fastRate)
Run-Scenario "S2 FAST hangs at 600 frames, never quits" "1" 26975 { param($m) [math]::Min(600, [math]::Max(0, ($m - 2) * $fastRate)) } $null
Run-Scenario "S3 FAST all frames, never quits" "1" 26975 { param($m) [math]::Min(26975, [math]::Max(0, ($m - 2) * $fastRate)) } $null
Run-Scenario "S4 FAST 0 frames forever (zen hang)" "1" 26975 { param($m) 0 } $null
Run-Scenario "S5 FULL 26,975 frames (pace check)" "2" 26975 { param($m) [math]::Min(26975, [math]::Max(0, ($m - 10) * $fullRate)) } $null
Run-Scenario "S6 FULL 2,000 frames done, never quits" "2" 2000 { param($m) [math]::Min(2000, [math]::Max(0, ($m - 10) * $fullRate)) } $null
Run-Scenario "S7 FAST slow but moving (GPU throttled)" "1" 26975 { param($m) [math]::Min(26975, [math]::Max(0, ($m - 2) * 60)) } (2 + 26975 / 60)
Remove-Item -Recurse -Force $tmp
