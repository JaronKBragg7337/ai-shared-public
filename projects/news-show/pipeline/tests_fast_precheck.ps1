# Test harness for the 11/23 "FAST from the start" pre-check in run_rendered_news.ps1.
# Pulls the block straight out of the real file, then runs it with fake times / plans. Prints one line per case.
param([string]$File = 'C:\Users\lilli\AI-Shared\projects\news-show\pipeline\run_rendered_news.ps1')
$ErrorActionPreference = "Stop"
$src = Get-Content $File -Raw
$m = [regex]::Match($src, '(?s)(  if \(-not \$Fast\) \{\r?\n    try \{.*?\r?\n  \})\r?\n  \$env:EP_DIR')
if (-not $m.Success) { "BLOCK NOT FOUND"; exit 1 }
$block = $m.Groups[1].Value
$tmp = Join-Path $env:TEMP "fastcheck_$PID"; New-Item -ItemType Directory -Force $tmp | Out-Null

function Run-Case($name, $now, $frames, [bool]$fastIn, $fpsEnv) {
    $script:said = @()
    $Out = $tmp
    if ($null -eq $frames) { Remove-Item "$tmp/plan.json" -ErrorAction SilentlyContinue } else { '{"frames": ' + $frames + '}' | Set-Content "$tmp/plan.json" }
    if ($fpsEnv) { $env:NEWS_FULL_FPS = $fpsEnv } else { Remove-Item Env:NEWS_FULL_FPS -ErrorAction SilentlyContinue }
    [switch]$Fast = $fastIn
    function Say($m) { $script:said += $m }
    $fixed = [datetime]$now
    function Get-Date { param($Hour, $Minute, $Second)
        if ($PSBoundParameters.ContainsKey('Hour')) { return $fixed.Date.AddHours($Hour).AddMinutes($Minute).AddSeconds($Second) }
        return $fixed }
    . ([scriptblock]::Create($block))
    "{0,-46} -> Fast={1,-5} retry-if-partial={2,-5} said: {3}" -f $name, [bool]$Fast, [bool](-not $Fast), (($script:said -join ' | ') -replace '\s+', ' ')
}

Run-Case "a) 26,975 frames at 3:52 AM (today's show)" "2026-11-23 03:52" 26975 $false $null
Run-Case "b) 2,000 frames at 3:52 AM (short special)" "2026-11-23 03:52" 2000 $false $null
Run-Case "c) plan.json missing" "2026-11-23 03:52" $null $false $null
Run-Case "d) already -Fast" "2026-11-23 03:52" 26975 $true $null
Run-Case "e) 26,975 frames, NEWS_FULL_FPS=20" "2026-11-23 03:52" 26975 $false "20"
Run-Case "f) 78,567 frames at 3:52 (longest, 11/18)" "2026-11-23 03:52" 78567 $false $null
Remove-Item -Recurse -Force $tmp
