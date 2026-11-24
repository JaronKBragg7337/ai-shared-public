# Pioneer studio scenes: take UNREAL.lock, rebuild the wall atlas, run build_studio.py in Unreal, release the lock. (Fable 11/15)
#   .\run_studio.ps1 -Scenes "s01,s02,s10,s15" -Res 1920x1080 -Sp 2 -Tp 4 -Tag ""
param([string]$Scenes = "s01,s02,s10,s15", [string]$Res = "960x540", [string]$Sp = "1", [string]$Tp = "1", [string]$Tag = "_fast")
$ep = "C:\Users\lilli\AI-Shared\projects\heartbeat-tv\pioneer-episode"; $lock = "$ep\UNREAL.lock"; $root = "C:\Users\lilli\Projects\necklace-unreal\Saved\MovieRenders"
$got = $false
for ($i = 0; $i -lt 240 -and -not $got; $i++) {
    try { $fs = [System.IO.File]::Open($lock, [System.IO.FileMode]::CreateNew); $b = [Text.Encoding]::UTF8.GetBytes("Fable (studio scenes $Scenes) " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")); $fs.Write($b, 0, $b.Length); $fs.Close(); $got = $true }
    catch {
        $age = ((Get-Date) - (Get-Item $lock).LastWriteTime).TotalMinutes
        if ($age -gt 90 -and -not (Get-Process UnrealEditor, UnrealEditor-Cmd -ErrorAction SilentlyContinue)) { Remove-Item $lock -Force; continue }
        if ($i % 4 -eq 0) { Write-Output ("waiting for UNREAL.lock (" + (Get-Content $lock -Raw) + ", " + [int]$age + " min old)") }
        Start-Sleep -Seconds 30
    }
}
if (-not $got) { Write-Output "could not get UNREAL.lock"; exit 2 }
try {
    if (Get-Process UnrealEditor, UnrealEditor-Cmd -ErrorAction SilentlyContinue) { Write-Output "an Unreal process is running without a lock - not starting"; exit 3 }
    python "$ep\studio\make_atlas.py"
    $env:PIO_SCENES = $Scenes; $env:PIO_RES = $Res; $env:PIO_SPATIAL = $Sp; $env:PIO_TEMPORAL = $Tp; $env:PIO_TAG = $Tag
    foreach ($s in $Scenes.Split(",")) { $d = "$root\Pioneer_$s$Tag"; if (Test-Path $d) { Remove-Item "$d\*.png" -Force -ErrorAction SilentlyContinue } }
    $p = Start-Process "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe" -ArgumentList '"C:\Users\lilli\Projects\necklace-unreal\NecklaceFilm.uproject" -ExecCmds="py C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode/studio/build_studio.py"' -PassThru
    $p.WaitForExit(3000000) | Out-Null
    if (-not $p.HasExited) { Write-Output "TIMEOUT - closing my Unreal"; $p.Kill() }
    Write-Output ("unreal exit " + $p.ExitCode)
    foreach ($s in $Scenes.Split(",")) { $d = "$root\Pioneer_$s$Tag"; Write-Output ("$s frames " + (Get-ChildItem $d -Filter *.png -ErrorAction SilentlyContinue).Count) }
    Select-String -Path "C:\Users\lilli\Projects\necklace-unreal\Saved\Logs\NecklaceFilm.log" -Pattern "PIOSTUDIO", "LogPython: Error", "Traceback" | Select-Object -Last 30 | ForEach-Object { $_.Line.Substring(0, [Math]::Min(240, $_.Line.Length)) }
} finally { Remove-Item $lock -Force -ErrorAction SilentlyContinue }
exit 0
