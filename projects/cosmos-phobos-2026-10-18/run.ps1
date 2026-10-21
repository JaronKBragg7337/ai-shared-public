# One-time Codex job (Jaron 10/17: "set one for five hours after when usage should be reset"). Codex fixes Phobos for iPhone;
# this runner pushes ONLY if the phone check passes afterwards (a rule, not an approval). Then the task deletes itself.
$Repo = "C:\Users\lilli\Projects\heartbeat-observatory"; $Dir = "C:\Users\lilli\AI-Shared\projects\cosmos-phobos-2026-10-18"
$Log = "$Dir\run.log"; function Say($m) { Add-Content $Log "$(Get-Date -Format 'yyyy-MM-dd HH:mm') $m" }
Say "start"
$before = (git -C $Repo rev-parse HEAD)
Get-Content "$Dir\PROMPT.txt" -Raw | & codex exec -m gpt-6.1-sol -c model_reasoning_effort=medium -s workspace-write --skip-git-repo-check -C $Repo - > "$Dir\codex-output.txt" 2>&1
Say "codex exit $LASTEXITCODE"
$after = (git -C $Repo rev-parse HEAD)
if ($after -eq $before) { Say "no commit from Codex - nothing to push" }
else {
  Push-Location $Repo; node games/the-cosmos/test/phone-check.mjs > "$Dir\phone-check.txt" 2>&1; $pc = $LASTEXITCODE; Pop-Location
  if ($pc -eq 0) { git -C $Repo pull --rebase -q origin main; git -C $Repo push -q origin main; Say "phone check PASSED - pushed $after" }
  else { Say "phone check FAILED ($pc) - NOT pushed; commit $after stays local for Claude to review" }
}
schtasks /Delete /TN "HB Cosmos Phobos Codex" /F | Out-Null
Say "done"
