# Heartbeat News - the rendered (Unreal) show, every morning, start to finish on the MSI. No human steps.
# Waits for today's episode JSON (the writer publishes ~3:45 AM; task starts 3:50 AM), then: voices (Vex eSpeak chain, Joe Kokoro Onyx + Studio knobs)
# -> plan (timing, cameras, wall graphics, soundtrack) -> Unreal render (lip-sync, cuts, Vex mouth, walls) -> mp4 -> Supabase Storage.
# Log: projects/news-show/rendered-runs.log. Run by hand:  powershell -File run_rendered_news.ps1 [-Date 2026-09-27]
param([string]$Date = (Get-Date -Format "yyyy-MM-dd"), [switch]$RenderOnly, [switch]$Fast)
# NEWS DEADLINE RULE (Jaron 10/18): the day's show must be live by 8 AM, never after noon. Running late = use the FASTEST way
# we have (-Fast = fewer render samples, ~several x quicker), never the slow full-quality path. Fast is automatic after 5:15 AM.   # -RenderOnly: voices + plan already made, just render + publish
$ErrorActionPreference = "Stop"
$Log = "C:\Users\lilli\AI-Shared\projects\news-show\rendered-runs.log"
function Say($m) { $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Date $m"; Add-Content $Log $line; Write-Host $line }
$Out = "C:/Users/lilli/Projects/necklace-unreal/NewsAudio/$Date"
$Site = "C:\Users\lilli\Projects\heartbeat-observatory"
$Pipe = "C:\Users\lilli\AI-Shared\projects\news-show\pipeline"
$UE = "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
try {
  if (-not $RenderOnly) {
  # 1. wait for the day's episode (up to 3 h)
  $deadline = (Get-Date).AddHours(3)
  while ($true) {
    try { $r = Invoke-WebRequest "https://www.heartbeatobservatory.com/news/episodes/$Date.json" -UseBasicParsing -TimeoutSec 20; if ($r.StatusCode -eq 200) { break } } catch {}
    if ((Get-Date) -gt $deadline) { Say "no episode published - stopping"; exit 1 }
    Start-Sleep -Seconds 120
  }
  Say "episode found"
  if (Get-Process UnrealEditor -ErrorAction SilentlyContinue) { Say "Unreal already open - waiting up to 1 h"; $w = (Get-Date).AddHours(1); while ((Get-Process UnrealEditor -ErrorAction SilentlyContinue) -and (Get-Date) -lt $w) { Start-Sleep 60 } }
  New-Item -ItemType Directory -Force $Out | Out-Null
  # 2. the full running order: stories + the house commercials + the wires, laid out the way the page does it
  python "$Pipe\episode_script.py" $Date $Out; if ($LASTEXITCODE) { throw "script failed" }
  # 3. voices
  Push-Location $Site
  node news/tools/render-voices.mjs --episode $Date --who vex --out $Out; if ($LASTEXITCODE) { throw "vex voices failed" }
  & "C:\Users\lilli\Projects\necklace-voices\.venv\Scripts\python.exe" "C:\Users\lilli\Projects\necklace-voices\joe_voice.py" $Date $Out; if ($LASTEXITCODE) { throw "joe voices failed" }
  node news/tools/render-voices.mjs --episode $Date --who joe --input "$Out/dry" --out $Out; if ($LASTEXITCODE) { throw "joe chain failed" }
  Pop-Location
  Say "voices done"
  # 4. plan (timing, cameras, wall graphics, soundtrack)
  python "$Pipe\episode_plan.py" $Date $Out; if ($LASTEXITCODE) { throw "plan failed" }
  }
  # 4b. Sapling gives the GPU to the render (Jaron 10/15: heartbeat + Unreal on one 8 GB card froze both); restarted after
  $Sap = "C:\Users\lilli\Projects\sapling"; $Py = "C:\Users\lilli\scoop\apps\python312\current\python.exe"
  $sapOut = & $Py "$Sap\tools\gpu_yield.py" stop "news render (run_rendered_news.ps1)" 2>&1; Say "sapling: $sapOut"
  # 5. render in Unreal (the editor quits itself when Movie Render Queue finishes)
  $tag = $Date -replace "-", ""; $Frames = "C:\Users\lilli\Projects\necklace-unreal\Saved\MovieRenders\Ep_$tag"
  if (Test-Path $Frames) { Remove-Item -Recurse -Force $Frames }
  $env:EP_DIR = $Out; if ($Fast -or (Get-Date).Hour -ge 6 -or ((Get-Date).Hour -eq 5 -and (Get-Date).Minute -ge 15)) { $env:EP_SPATIAL = "1"; $env:EP_TEMPORAL = "1"; Say "FAST render (deadline rule)" } else { $env:EP_SPATIAL = "2"; $env:EP_TEMPORAL = "4" }; $env:NEWS_REIMPORT = "0"; $env:NEWS_VEX_LEVELS = ""
  $p = Start-Process $UE -ArgumentList "`"C:\Users\lilli\Projects\necklace-unreal\NecklaceFilm.uproject`" -ExecCmds=`"py C:/Users/lilli/Projects/necklace-unreal/episode_render.py`"" -PassThru
  # deadline rule by PACE (10/19: a 29-min show at full quality from 4:03 was heading for ~8:15). Every 5 min project the finish;
  # if the full-quality render would end after 7:15 AM, stop it - the fast retry below re-films it (~5x quicker).
  $planFrames = (Get-Content "$Out/plan.json" | ConvertFrom-Json).frames; $t0 = Get-Date
  while (-not $p.WaitForExit(300000)) {
    if ($env:EP_SPATIAL -eq "1") { continue }
    $done = (Get-ChildItem $Frames -Filter "f_*.png" -ErrorAction SilentlyContinue).Count
    $mins = ((Get-Date) - $t0).TotalMinutes
    if ($done -gt 500 -and $mins -gt 10) {
      $eta = (Get-Date).AddMinutes(($planFrames - $done) / ($done / $mins))
      if ($eta -gt (Get-Date -Hour 7 -Minute 15 -Second 0)) { Say "pace check: full quality would finish $($eta.ToString('HH:mm')) - switching to FAST (deadline rule)"; Stop-Process -Id $p.Id -Force; break }
    }
    if ($mins -gt 240) { break }
  }
  # 10/15 (Grok Build review): always ask for the restart; --if-ours arms the parole only if the heartbeat is down because a
  # GPU job stopped it (this render, or a training run that had it stopped) - a self-stop stays the owner's parole (D6).
  & $Py "$Sap\tools\gpu_yield.py" start "news render finished (run_rendered_news.ps1)" --if-ours | Out-Null
  $plan = Get-Content "$Out/plan.json" | ConvertFrom-Json
  $n = (Get-ChildItem $Frames -Filter "f_*.png" -ErrorAction SilentlyContinue).Count
  # deadline rule (Jaron 10/18): an incomplete render is retried ONCE right away in fast mode, Sapling kept paused for it
  if ($n -lt $plan.frames -and -not $Fast -and (Get-Date).Hour -lt 12) {
    Say "render incomplete ($n of $($plan.frames)) - retrying in FAST mode (deadline rule)"
    & $Py "$Sap\tools\gpu_yield.py" stop "news fast retry (run_rendered_news.ps1)" | Out-Null
    if (Test-Path $Frames) { Remove-Item -Recurse -Force $Frames }
    $env:EP_SPATIAL = "1"; $env:EP_TEMPORAL = "1"
    $p = Start-Process $UE -ArgumentList "`"C:\Users\lilli\Projects\necklace-unreal\NecklaceFilm.uproject`" -ExecCmds=`"py C:/Users/lilli/Projects/necklace-unreal/episode_render.py`"" -PassThru
    $p.WaitForExit(2 * 3600 * 1000) | Out-Null
    & $Py "$Sap\tools\gpu_yield.py" start "news fast retry finished (run_rendered_news.ps1)" --if-ours | Out-Null
    $n = (Get-ChildItem $Frames -Filter "f_*.png" -ErrorAction SilentlyContinue).Count
  }
  if ($n -lt $plan.frames) { throw "render incomplete: $n of $($plan.frames) frames" }
  Say "render done ($n frames)"
  # 6. encode + poster + publish
  $mp4 = "C:\Users\lilli\Projects\necklace-unreal\Saved\MovieRenders\Ep_$tag.mp4"
  ffmpeg -y -loglevel error -framerate 24 -start_number 0 -i "$Frames\f_%04d.png" -i "$Out/episode.wav" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart $mp4
  if ($LASTEXITCODE) { throw "encode failed" }
  ffmpeg -y -loglevel error -i "$Frames\f_0012.png" -vf scale=1280:-1 -q:v 3 "$Out/poster.jpg"
  # 6b. the 9:16 cuts for phones + social (Jaron 10/17); a failure here never stops the main show from publishing
  # 10/19: the full 9:16 + YouTube cuts of a 29-min show took 40+ min and held the publish past 7:10. Now: short only (~1 min),
  # publish, THEN the long cuts, then publish again to add them (deadline rule: the show never waits on extras).
  $Vert = "$Out/vertical"; python "$Pipe\make_vertical.py" $mp4 $Out $Vert --short-only; if ($LASTEXITCODE) { Say "short cut FAILED (main show still publishes)"; $Vert = "" }
  # 10/18: the frames (50-60 GB a day) go as soon as the mp4 is encoded - a later failure must not leave them behind (the
  # disk filled on 10/18 from 5 days of leftovers). The mp4 + plan + voices can always rebuild anything.
  if ((Test-Path $mp4) -and (Get-Item $mp4).Length -gt 10MB) { Remove-Item -Recurse -Force $Frames; Say "frames removed" }
  $pub = python "$Pipe\publish_video.py" $Date $mp4 "$Out/poster.jpg" "$Out/plan.json" $Vert 2>&1; $pubExit = $LASTEXITCODE
  $pub | Select-Object -Last 4 | ForEach-Object { Say "publish: $_" }
  if ($pubExit) { throw "publish failed" }
  Say "PUBLISHED $([math]::Round((Get-Item $mp4).Length / 1MB, 1)) MB"
  # 6c. the long extras after the show is live: full 9:16 cut + YouTube version, then re-publish to add the vertical
  python "$Pipe\make_vertical.py" $mp4 $Out "$Out/vertical"
  if ($LASTEXITCODE) { Say "long vertical/youtube cuts FAILED (show already live)" } else {
    python "$Pipe\publish_video.py" $Date $mp4 "$Out/poster.jpg" "$Out/plan.json" "$Out/vertical" 2>&1 | Select-Object -Last 1 | ForEach-Object { Say "publish extras: $_" } }
} catch {
  Say "FAILED: $_"
  exit 1
}
