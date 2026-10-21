# Heartbeat News - backup daily writer on the MSI. Registered as Windows task "Heartbeat News Writer", daily 4:20 AM local (moved from 10:20 on 2026-10-15).
# The main writer is a Claude cloud routine at 3:45 AM (trig_01EnWaDLFxBZjQVYZmCNKjCT). This script costs nothing when that one
# already shipped today's episode: it checks origin/main first and only calls Claude Code if the file is missing.
# Written 2026-09-24 by Claude (cloud session) through the Heartbeat MAI connector.
$ErrorActionPreference = "Continue"
$repo  = "C:\Users\lilli\Projects\heartbeat-observatory"
$watch = "C:\Users\lilli\Projects\watch"
$log   = "C:\Users\lilli\AI-Shared\projects\news-show\runs.log"
$day   = (Get-Date).ToString("yyyy-MM-dd")
function Note($t) { Add-Content -Path $log -Value ("{0} | {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $t) }

Set-Location $repo
git checkout main 2>&1 | Out-Null
git pull --rebase origin main 2>&1 | Out-Null
if (Test-Path "news\episodes\$day.json") { Note "episode $day already on main (cloud routine wrote it); nothing to do"; exit 0 }

Set-Location $watch
git pull --rebase 2>&1 | Out-Null
$caps = @("codex", "deepseek", "claude", "msi") | Where-Object { Test-Path "$watch\$_\$day.md" }
if (-not $caps) { Note "no watch captures for $day yet; the page keeps looping the last show"; exit 0 }

Set-Location $repo
$prompt = @"
Write today's Heartbeat News episode. Today is $day (America/Indiana/Indianapolis).
Read news/WRITER.md in this repository and follow it. The watch repo is already on this machine at $watch, so read the captures
there instead of cloning: $(($caps | ForEach-Object { "$watch\$_\$day.md" }) -join ", ").
Also read watch/msi/$day.md (headlines fetched from the MSI) as an extra source; cite its links.
Write news/episodes/$day.json and update news/episodes/index.json, then run: node news/tools/check-episode.mjs news/episodes/$day.json
and fix every ERROR. Do not commit or push; the script that called you does that. Set writer to "Claude, daily news job (MSI backup)".
"@
$out = Join-Path $env:TEMP "heartbeat-news-run.log"
& claude -p $prompt --permission-mode acceptEdits --add-dir $watch --allowedTools "Read,Write,Edit,Glob,Grep,Bash(node news/tools/check-episode.mjs:*)" > $out 2>&1

# Second writer (added 2026-09-25 after the claude CLI login expired and nothing ran): Codex on Jaron's ChatGPT plan, no login
# to keep alive. Only runs if Claude did not write the file.
if (-not (Test-Path "news\episodes\$day.json")) {
  Note ("claude CLI wrote nothing (" + ((Get-Content $out -Tail 1) -join " ") + "); trying Codex")
  $cprompt = $prompt -replace 'Set writer to "Claude, daily news job \(MSI backup\)"', 'Set writer to "Codex (GPT-6 Luna), daily news job (MSI backup)"'
  $cprompt | & codex exec -m gpt-6-luna -c model_reasoning_effort=high -s workspace-write --skip-git-repo-check -C $repo --add-dir $watch - > "$out.codex" 2>&1
}

if (-not (Test-Path "news\episodes\$day.json")) { Note ("NO EPISODE written by Claude or Codex; last line: " + ((Get-Content "$out.codex" -Tail 1) -join " ")); exit 1 }
node news/tools/check-episode.mjs "news/episodes/$day.json" > "$out.check" 2>&1
if ($LASTEXITCODE -ne 0) { Note ("episode $day FAILED the check, not pushed: " + ((Get-Content "$out.check" | Select-String ERROR | Select-Object -First 2) -join " / ")); git checkout -- news/episodes/index.json 2>&1 | Out-Null; exit 1 }
git add "news/episodes/$day.json" news/episodes/index.json
git commit -m "news: episode $day" -m "Written by the MSI backup writer (AI-Shared/projects/news-show/run_news.ps1)." 2>&1 | Out-Null
$pushed = $false
foreach ($wait in 2, 4, 8, 16, 0) { git push origin HEAD:main 2>&1 | Out-Null; if ($LASTEXITCODE -eq 0) { $pushed = $true; break }; if ($wait) { Start-Sleep -Seconds $wait; git pull --rebase origin main 2>&1 | Out-Null } }
Note ("episode $day written from " + ($caps -join "+") + $(if ($pushed) { "; pushed to main" } else { "; PUSH FAILED" }))
