$D="C:\Users\lilli\AI-Shared\projects\lost-places\ep1-gobekli"; $t0=Get-Date
Add-Content "$D\timing.txt" "start $($t0.ToString('yyyy-MM-dd HH:mm:ss'))"
Get-Content "$D\CODEX-TASK.txt" -Raw | & codex exec -m gpt-6.1-sol -c model_reasoning_effort=medium -s danger-full-access --skip-git-repo-check -C $D - > "$D\codex-output.txt" 2>&1
$t1=Get-Date; Add-Content "$D\timing.txt" "end $($t1.ToString('yyyy-MM-dd HH:mm:ss')) exit $LASTEXITCODE minutes $([math]::Round(($t1-$t0).TotalMinutes,1))"
