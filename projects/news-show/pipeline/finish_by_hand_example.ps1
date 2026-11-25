# One-time finish for 2026-11-24: frames are complete (33,432) but the pipeline process exited before encoding.
# Same steps as run_rendered_news.ps1 section 6 (encode, poster, short cut, publish), then the long extras.
$Date = "2026-11-24"; $tag = "20261124"
$Log = "C:\Users\lilli\AI-Shared\projects\news-show\rendered-runs.log"
function Say($m) { $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Date $m"; Add-Content $Log $line; Write-Host $line }
$Out = "C:/Users/lilli/Projects/necklace-unreal/NewsAudio/$Date"
$Pipe = "C:\Users\lilli\AI-Shared\projects\news-show\pipeline"
$Py = "C:\Users\lilli\scoop\apps\python312\current\python.exe"
$Frames = "C:\Users\lilli\Projects\necklace-unreal\Saved\MovieRenders\Ep_$tag"
$mp4 = "C:\Users\lilli\Projects\necklace-unreal\Saved\MovieRenders\Ep_$tag.mp4"
Say "Claude: render done (33432 frames) but the pipeline process had exited - finishing encode + publish by hand"
ffmpeg -y -loglevel error -framerate 24 -start_number 0 -i "$Frames\f_%04d.png" -i "$Out/episode.wav" -c:v libx264 -preset veryfast -crf 21 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart $mp4
if ($LASTEXITCODE) { Say "encode failed - retrying through the PIL pipe"; & $Py "$Pipe\pipe_encode.py" $Frames "$Out/episode.wav" $mp4 0; if ($LASTEXITCODE) { Say "FAILED: encode failed"; exit 1 } }
ffmpeg -y -loglevel error -i "$Frames\f_0012.png" -vf scale=1280:-1 -q:v 3 "$Out/poster.jpg"
$Vert = "$Out/vertical"; python "$Pipe\make_vertical.py" $mp4 $Out $Vert --short-only; if ($LASTEXITCODE) { Say "short cut FAILED (main show still publishes)"; $Vert = "" }
if ((Test-Path $mp4) -and (Get-Item $mp4).Length -gt 10MB) { Remove-Item -Recurse -Force $Frames; Say "frames removed" }
$pub = python "$Pipe\publish_video.py" $Date $mp4 "$Out/poster.jpg" "$Out/plan.json" $Vert 2>&1; $pubExit = $LASTEXITCODE
$pub | Select-Object -Last 4 | ForEach-Object { Say "publish: $_" }
if ($pubExit) { Say "FAILED: publish failed"; exit 1 }
Say "PUBLISHED $([math]::Round((Get-Item $mp4).Length / 1MB, 1)) MB"
& $Py "C:\Users\lilli\Projects\sapling\tools\gpu_yield.py" start "news render finished (finish_news_1124)" --if-ours | Out-Null
$env:PYTHONUNBUFFERED = "1"; cmd /c "python `"$Pipe\make_vertical.py`" `"$mp4`" `"$Out`" `"$Out/vertical`" > `"$Out/vertical-long.log`" 2>&1"
if ($LASTEXITCODE) { Say "long vertical/youtube cuts FAILED (show already live)" } else {
  python "$Pipe\publish_video.py" $Date $mp4 "$Out/poster.jpg" "$Out/plan.json" "$Out/vertical" 2>&1 | Select-Object -Last 1 | ForEach-Object { Say "publish extras: $_" } }
