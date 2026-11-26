# Heartbeat News - the rendered (Unreal) show, every morning, start to finish on the MSI. No human steps.
# Waits for today's episode JSON (the writer publishes ~3:45 AM; task starts 3:50 AM), then: voices (Vex eSpeak chain, Joe Kokoro Onyx + Studio knobs)
# -> plan (timing, cameras, wall graphics, soundtrack) -> Unreal render (lip-sync, cuts, Vex mouth, walls) -> mp4 -> Supabase Storage.
# Log: projects/news-show/rendered-runs.log. Run by hand:  powershell -File run_rendered_news.ps1 [-Date 2026-09-27]
param([string]$Date = (Get-Date -Format "yyyy-MM-dd"), [switch]$RenderOnly, [switch]$Fast)
# 11/24 (Fable's hunt, state/msi-data-hunt.md): one fast core (logical 10+11 of the i9-14900HX) gives wrong answers at top speed -
# bad PNG reads, silent video damage. Keep this script and everything it starts (Unreal, ffmpeg, Python) off those two.
try { (Get-Process -Id $PID).ProcessorAffinity = [IntPtr]4294964223 } catch {}   # FFFFF3FF = all 32 except 10 and 11
# NEWS DEADLINE RULE (Jaron 10/18): the day's show must be live by 8 AM, never after noon. Running late = use the FASTEST way
# we have (-Fast = fewer render samples, ~several x quicker), never the slow full-quality path. Fast is automatic after 5:15 AM.   # -RenderOnly: voices + plan already made, just render + publish
$ErrorActionPreference = "Stop"
$Log = "C:\Users\lilli\AI-Shared\projects\news-show\rendered-runs.log"
# 11/25: the 3:50 AM run died silently at 3:52: a log line failed to write (file briefly held by a reader), the error handler's
# own log line failed too, and the show never rendered. Logging can never stop the show now: retry, then give up quietly.
function Say($m) {
  $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Date $m"
  for ($i = 0; $i -lt 10; $i++) {
    try { $fs = [System.IO.File]::Open($Log, 'Append', 'Write', 'ReadWrite'); $b = [System.Text.Encoding]::UTF8.GetBytes($line + "`r`n"); $fs.Write($b, 0, $b.Length); $fs.Close(); break }
    catch { Start-Sleep -Milliseconds 300 }
  }
  try { Write-Host $line } catch {}
}
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
  node news/tools/render-voices.mjs --episode $Date --who vex --out $Out
  # 11/13: the voice page dies at a random line; a fresh Chrome resumes from the lines already made. Up to 4 fresh restarts.
  for ($vr = 1; $LASTEXITCODE -and $vr -le 4; $vr++) { Say "vex voices stopped - fresh restart $vr (resume)"; Start-Sleep 5; node news/tools/render-voices.mjs --episode $Date --who vex --out $Out }
  if ($LASTEXITCODE) { throw "vex voices failed" }
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
  # 11/4: a crashed or failed run leaves its 50-60 GB of frames behind (10/31's sat there for 4 days and filled the disk,
  # so the health alert kept repeating). Before rendering, clear any OLD Ep_* frame folder whose finished mp4 exists.
  Get-ChildItem "C:\Users\lilli\Projects\necklace-unreal\Saved\MovieRenders" -Directory -Filter "Ep_2*" | Where-Object { $_.Name -ne "Ep_$tag" } | ForEach-Object {
    $done = "$($_.FullName).mp4"
    if ((Test-Path $done) -and (Get-Item $done).Length -gt 10MB) { Remove-Item -Recurse -Force $_.FullName; Say "cleared leftover frames $($_.Name) (its mp4 exists)" }
  }
  if (Test-Path $Frames) { Remove-Item -Recurse -Force $Frames }
  # 11/23 (Claude, reviewed by two agents): full quality has not finished a show since 10/18 - 37 nights it stalled (Unreal hung,
  # 0 frames after 15 min) or the pace check stopped it, and the fast retry made the show. Full quality's best measured speed is
  # ~2.8 frames/s (10/16-10/19 full runs, 165-174 frames/min incl. startup; fast is ~11/s). If the plan can't finish by 7:15 even at
  # that speed (+10 min startup), the full attempt is certain to be stopped, so start FAST right away and treat the run exactly
  # like -Fast. Shorter shows still try full quality as before. $env:NEWS_FULL_FPS overrides 2.8.
  if (-not $Fast) {
    try {
      $pf = [double](Get-Content "$Out/plan.json" -Raw | ConvertFrom-Json).frames
      $fps = if ($env:NEWS_FULL_FPS) { [double]$env:NEWS_FULL_FPS } else { 2.8 }
      $fullEnd = (Get-Date).AddMinutes(10 + $pf / $fps / 60)   # ~10 min for Unreal to load and start writing frames
      if ($pf -gt 0 -and $fullEnd -gt (Get-Date -Hour 7 -Minute 15 -Second 0)) {
        Say "full quality would need ~$([math]::Round($pf / $fps / 3600, 1)) h for $([int]$pf) frames (ends ~$($fullEnd.ToString('ddd HH:mm'))) - FAST from the start (deadline rule)"
        $Fast = $true
      }
    } catch { Say "full-quality time check skipped: $($_.Exception.Message)" }
  }
  $env:EP_DIR = $Out; if ($Fast -or (Get-Date).Hour -ge 6 -or ((Get-Date).Hour -eq 5 -and (Get-Date).Minute -ge 15)) { $env:EP_SPATIAL = "1"; $env:EP_TEMPORAL = "1"; Say "FAST render (deadline rule)" } else { $env:EP_SPATIAL = "2"; $env:EP_TEMPORAL = "4" }; $env:NEWS_REIMPORT = "0"; $env:NEWS_VEX_LEVELS = ""
  $p = Start-Process $UE -ArgumentList "`"C:\Users\lilli\Projects\necklace-unreal\NecklaceFilm.uproject`" -ExecCmds=`"py C:/Users/lilli/Projects/necklace-unreal/episode_render.py`"" -PassThru
  # deadline rule by PACE (10/19: a 29-min show at full quality from 4:03 was heading for ~8:15). Every 5 min project the finish;
  # if the full-quality render would end after 7:15 AM, stop it - the fast retry below re-films it (~5x quicker).
  $planFrames = (Get-Content "$Out/plan.json" | ConvertFrom-Json).frames; $t0 = Get-Date; $lastDone = -1; $stuck = 0
  while (-not $p.WaitForExit(300000)) {
    $done = (Get-ChildItem $Frames -Filter "f_*.png" -ErrorAction SilentlyContinue).Count
    $mins = ((Get-Date) - $t0).TotalMinutes
    # 11/1 stall rule: Unreal hung 80 min on 'Waiting for ZenServer to be ready' with 0 frames. No frames after 15 min = stuck:
    # kill it and the zen cache server so the fast retry below starts fresh.
    if ($done -eq 0 -and $mins -gt 15) { Say "stall: 0 frames after $([int]$mins) min - restarting Unreal (deadline rule)"; Stop-Process -Id $p.Id -Force; Get-Process zenserver -ErrorAction SilentlyContinue | Stop-Process -Force; break }
    # 11/23 review: in FAST mode this loop had no way out except Unreal quitting or the 0-frame stall above, so a mid-render hang
    # (or Unreal never quitting after the last frame) would wait forever: no show, and IgnoreNew skips the next nights. Full quality
    # only got out at 7:15 via the pace check. A healthy render adds ~840 (full) to ~3,300 (fast) frames per 5-min check, so no new
    # frames for two checks (10 min) = stuck: end it; the retry / tail render / encode below take over from the frames on disk.
    if ($done -gt 0 -and $done -eq $lastDone) { $stuck++ } else { $stuck = 0 }
    $lastDone = $done
    if ($stuck -ge 2) { Say "render made no new frames for 10 min (at $done of $planFrames) - ending it (deadline rule)"; Stop-Process -Id $p.Id -Force; Get-Process zenserver -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep -Seconds 10; break }
    if ($env:EP_SPATIAL -eq "1") { continue }
    if ($done -gt 500 -and $mins -gt 10) {
      $eta = (Get-Date).AddMinutes(($planFrames - $done) / ($done / $mins))
      if ($eta -gt (Get-Date -Hour 7 -Minute 15 -Second 0)) { Say "pace check: full quality would finish $($eta.ToString('HH:mm')) - switching to FAST (deadline rule)"; Stop-Process -Id $p.Id -Force; break }
    }
    if ($mins -gt 240) { Say "full-quality render still running after 4 h - ending it (deadline rule)"; Stop-Process -Id $p.Id -Force; Start-Sleep -Seconds 10; break }   # 11/23 review: end it first, or the retry starts a 2nd Unreal beside it
  }
  # 10/15 (Grok Build review): always ask for the restart; --if-ours arms the parole only if the heartbeat is down because a
  # GPU job stopped it (this render, or a training run that had it stopped) - a self-stop stays the owner's parole (D6).
  # 11/18: Sapling is restarted ONCE, after the last render attempt (below), not between attempts. On 11/18 the parole
  # restarted it at 5:25:43, 4 s before the fast retry asked it to stop (a race), and it shared the GPU with the fast render.
  $plan = Get-Content "$Out/plan.json" | ConvertFrom-Json
  $n = (Get-ChildItem $Frames -Filter "f_*.png" -ErrorAction SilentlyContinue).Count
  # deadline rule (Jaron 10/18): an incomplete render is retried ONCE right away in fast mode, Sapling kept paused for it
  if ($n -lt $plan.frames -and ((-not $Fast) -or $n -lt 500) -and (Get-Date).Hour -lt 12) {   # 11/13: a 0-frame stall retries once even in -Fast; 11/23: so does any run under 500 frames (too few for the tail render below)
    Say "render incomplete ($n of $($plan.frames)) - retrying in FAST mode (deadline rule)"
    & $Py "$Sap\tools\gpu_yield.py" stop "news fast retry (run_rendered_news.ps1)" | Out-Null
    if (Test-Path $Frames) { Remove-Item -Recurse -Force $Frames }
    $env:EP_SPATIAL = "1"; $env:EP_TEMPORAL = "1"
    Get-Process zenserver -ErrorAction SilentlyContinue | Stop-Process -Force   # 11/1: a stale zen server can hang Unreal at startup
    $p = Start-Process $UE -ArgumentList "`"C:\Users\lilli\Projects\necklace-unreal\NecklaceFilm.uproject`" -ExecCmds=`"py C:/Users/lilli/Projects/necklace-unreal/episode_render.py`"" -PassThru
    # 11/24: the retry itself hung 55 min at 'Waiting for ZenServer' with 0 frames (it only had the 2 h cap). Same stall rule
    # as the first attempt: 0 frames after 15 min = restart Unreal + zen ONCE; 0 again = give up so the failure is reported early.
    $t1 = Get-Date; $relaunched = $false
    while (-not $p.WaitForExit(60000)) {
      $rm = ((Get-Date) - $t1).TotalMinutes; $rc = (Get-ChildItem $Frames -Filter "f_*.png" -ErrorAction SilentlyContinue).Count
      if ($rc -eq 0 -and $rm -gt 15) {
        Stop-Process -Id $p.Id -Force; Get-Process zenserver -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep -Seconds 10
        if ($relaunched) { Say "fast retry: 0 frames again after 15 min - giving up"; break }
        Say "fast retry: 0 frames after 15 min (stall) - restarting Unreal once"
        $p = Start-Process $UE -ArgumentList "`"C:\Users\lilli\Projects\necklace-unreal\NecklaceFilm.uproject`" -ExecCmds=`"py C:/Users/lilli/Projects/necklace-unreal/episode_render.py`"" -PassThru
        $t1 = Get-Date; $relaunched = $true; continue
      }
      if ($rm -gt 120) { break }
    }
    # 11/18: if the fast retry is still running after 2 h, end it (by PID) so the auto-resume below never starts a SECOND
    # Unreal next to it on the 8 GB card (it also kills zenserver). The frames on disk are kept; the tail render resumes from them.
    if (-not $p.HasExited) { Say "fast retry still running after 2 h - ending it so the tail render can resume"; Stop-Process -Id $p.Id -Force; Start-Sleep -Seconds 10 }
    $n = (Get-ChildItem $Frames -Filter "f_*.png" -ErrorAction SilentlyContinue).Count
  }
  # 11/14 auto-resume: on 11/13 and 11/14 Unreal quit partway (63,453/69,320 and 56,759/64,534) and Claude rendered the
  # tail by hand with EP_START. Now the pipeline does it: render only the missing frames, up to 3 tries, stop if no progress.
  for ($tr = 1; $n -lt $plan.frames -and $n -ge 500 -and $tr -le 3 -and (Get-Date).Hour -lt 12; $tr++) {
    $before = $n
    Say "render stopped at $n of $($plan.frames) - rendering the tail from frame $n (auto-resume $tr)"
    & $Py "$Sap\tools\gpu_yield.py" stop "news tail render (run_rendered_news.ps1)" | Out-Null
    $env:EP_SPATIAL = "1"; $env:EP_TEMPORAL = "1"; $env:EP_START = "$n"
    Get-Process zenserver -ErrorAction SilentlyContinue | Stop-Process -Force
    $p = Start-Process $UE -ArgumentList "`"C:\Users\lilli\Projects\necklace-unreal\NecklaceFilm.uproject`" -ExecCmds=`"py C:/Users/lilli/Projects/necklace-unreal/episode_render.py`"" -PassThru
    # 11/24: a tail render that adds no frames in 15 min is stuck (zen hang) - end it instead of waiting the full 90 min
    $t1 = Get-Date
    while (-not $p.WaitForExit(60000)) {
      $tm = ((Get-Date) - $t1).TotalMinutes
      if ($tm -gt 90 -or ($tm -gt 15 -and (Get-ChildItem $Frames -Filter "f_*.png" -ErrorAction SilentlyContinue).Count -le $before)) { break }
    }
    if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force }
    Remove-Item Env:EP_START -ErrorAction SilentlyContinue
    $n = (Get-ChildItem $Frames -Filter "f_*.png" -ErrorAction SilentlyContinue).Count
    if ($n -le $before) { Say "tail render made no progress ($n) - stopping auto-resume"; break }
  }
  # all render attempts are over: now Sapling may have the GPU back (the parole waits for Unreal to exit first)
  & $Py "$Sap\tools\gpu_yield.py" start "news render finished (run_rendered_news.ps1)" --if-ours | Out-Null
  # 11/4: the fast retry ended 433 frames (18 s) short and the whole show failed. If under 2% is missing at the END,
  # hold the last good frame for the rest instead of failing (the audio still plays to the end).
  $hold = 0
  if ($n -lt $plan.frames -and $n -ge [math]::Floor($plan.frames * 0.98)) { $hold = $plan.frames - $n; Say "render $n of $($plan.frames): holding the last frame for $hold frames" }
  elseif ($n -lt $plan.frames) { throw "render incomplete: $n of $($plan.frames) frames" }
  Say "render done ($n frames)"
  # 6. encode + poster + publish
  $mp4 = "C:\Users\lilli\Projects\necklace-unreal\Saved\MovieRenders\Ep_$tag.mp4"
  $vf = @(); if ($hold -gt 0) { $vf = @("-vf", "tpad=stop_mode=clone:stop=$hold") }
  ffmpeg -y -loglevel error -framerate 24 -start_number 0 -i "$Frames\f_%04d.png" -i "$Out/episode.wav" @vf -c:v libx264 -preset veryfast -crf 21 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart $mp4  # 10/31: was -preset slow; the long all-core encode right after the Unreal render froze the MSI (CLOCK_WATCHDOG_TIMEOUT 5:14 AM). veryfast = ~3.5 min
  # 11/22: ffmpeg's PNG reader failed on the frames (inflate error -3, then a crash) though every frame decoded in PIL.
  # Fall back to reading them with PIL and piping raw frames into the same x264 settings (pipe_encode.py) so the show publishes.
  if ($LASTEXITCODE) { Say "encode failed - retrying through the PIL pipe (pipe_encode.py)"; & $Py "$Pipe\pipe_encode.py" $Frames "$Out/episode.wav" $mp4 $hold; if ($LASTEXITCODE) { throw "encode failed" } }
  ffmpeg -y -loglevel error -i "$Frames\f_0012.png" -vf scale=1280:-1 -q:v 3 "$Out/poster.jpg"
  if ($LASTEXITCODE -or -not (Test-Path "$Out/poster.jpg")) { & $Py -c "from PIL import Image; im=Image.open(r'$Frames\f_0012.png').convert('RGB'); w,h=im.size; im.resize((1280,round(h*1280/w))).save(r'$Out/poster.jpg',quality=88)" }
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
  $env:PYTHONUNBUFFERED = "1"; cmd /c "python `"$Pipe\make_vertical.py`" `"$mp4`" `"$Out`" `"$Out/vertical`" > `"$Out/vertical-long.log`" 2>&1"   # 11/17: via cmd so stderr can never trip ErrorActionPreference=Stop (the 11/17 *> version did); the log keeps the real error
  if ($LASTEXITCODE) { Say "long vertical/youtube cuts FAILED (show already live) - see $Out/vertical-long.log" } else {
    python "$Pipe\publish_video.py" $Date $mp4 "$Out/poster.jpg" "$Out/plan.json" "$Out/vertical" 2>&1 | Select-Object -Last 1 | ForEach-Object { Say "publish extras: $_" } }
} catch {
  Say "FAILED: $_"
  exit 1
}
