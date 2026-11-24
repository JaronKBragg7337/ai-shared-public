# publish_from_frames.ps1 - encode + publish a show whose frames already exist (11/13/2026: used after a tail-only re-render).
# Same steps as run_rendered_news.ps1 step 6; frames folder is removed only after a good mp4 exists.
param([string]$Date = (Get-Date -Format "yyyy-MM-dd"))
$ErrorActionPreference = "Stop"
$Log = "C:\Users\lilli\AI-Shared\projects\news-show\rendered-runs.log"
function Say($m) { $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Date $m"; Add-Content $Log $line; Write-Host $line }
$Out = "C:/Users/lilli/Projects/necklace-unreal/NewsAudio/$Date"
$Pipe = "C:\Users\lilli\AI-Shared\projects\news-show\pipeline"
$tag = $Date -replace "-", ""; $Frames = "C:\Users\lilli\Projects\necklace-unreal\Saved\MovieRenders\Ep_$tag"
try {
  $plan = Get-Content "$Out/plan.json" | ConvertFrom-Json
  $n = (Get-ChildItem $Frames -Filter "f_*.png").Count
  $hold = 0
  if ($n -lt $plan.frames -and $n -ge [math]::Floor($plan.frames * 0.98)) { $hold = $plan.frames - $n; Say "publish-from-frames: $n of $($plan.frames), holding last frame $hold" }
  elseif ($n -lt $plan.frames) { throw "still incomplete: $n of $($plan.frames)" }
  $mp4 = "C:\Users\lilli\Projects\necklace-unreal\Saved\MovieRenders\Ep_$tag.mp4"
  $vf = @(); if ($hold -gt 0) { $vf = @("-vf", "tpad=stop_mode=clone:stop=$hold") }
  ffmpeg -y -loglevel error -framerate 24 -start_number 0 -i "$Frames\f_%04d.png" -i "$Out/episode.wav" @vf -c:v libx264 -preset veryfast -crf 21 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart $mp4
  if ($LASTEXITCODE) { throw "encode failed" }
  ffmpeg -y -loglevel error -i "$Frames\f_0012.png" -vf scale=1280:-1 -q:v 3 "$Out/poster.jpg"
  $Vert = "$Out/vertical"; python "$Pipe\make_vertical.py" $mp4 $Out $Vert --short-only; if ($LASTEXITCODE) { Say "short cut FAILED (main show still publishes)"; $Vert = "" }
  if ((Test-Path $mp4) -and (Get-Item $mp4).Length -gt 10MB) { Remove-Item -Recurse -Force $Frames; Say "frames removed" }
  $pub = python "$Pipe\publish_video.py" $Date $mp4 "$Out/poster.jpg" "$Out/plan.json" $Vert 2>&1; $pubExit = $LASTEXITCODE
  $pub | Select-Object -Last 4 | ForEach-Object { Say "publish: $_" }
  if ($pubExit) { throw "publish failed" }
  Say "PUBLISHED $([math]::Round((Get-Item $mp4).Length / 1MB, 1)) MB"
  python "$Pipe\make_vertical.py" $mp4 $Out "$Out/vertical"
  if (-not $LASTEXITCODE) { python "$Pipe\publish_video.py" $Date $mp4 "$Out/poster.jpg" "$Out/plan.json" "$Out/vertical" 2>&1 | Select-Object -Last 1 | ForEach-Object { Say "publish extras: $_" } }
} catch { Say "FAILED (publish-from-frames): $_"; exit 1 }
