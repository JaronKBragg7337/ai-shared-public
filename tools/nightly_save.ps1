# Nightly save of AI-Shared to the private GitHub repo (Jaron 10/21). Runs 11:55 PM. Text + code only (.gitignore keeps
# secrets, media and huge logs out). A quick key check stops the push if a real key ever lands in a file.
Set-Location "C:\Users\lilli\AI-Shared"
git add -A 2>$null
$hits = git diff --cached -U0 | Select-String -Pattern '(sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sb_secret_[A-Za-z0-9_-]{20,}|xai-[A-Za-z0-9]{30,}|BEGIN (RSA )?PRIVATE KEY)'
if ($hits) { git reset -q; Add-Content state/nightly-save.log "$(Get-Date -Format s) STOPPED: something that looks like a real key is in a changed file"; exit 1 }
git commit -q -m "nightly save $(Get-Date -Format yyyy-MM-dd)" -m "Co-Authored-By: Claude Opus 5.5 <<email>>" 2>$null
git push -q 2>&1 | Out-Null
Add-Content state/nightly-save.log "$(Get-Date -Format s) saved $(git rev-parse --short HEAD)"

# then refresh the cleaned public copy (Jaron 10/21: public so any AI chat can read it)
python C:\Users\lilli\AI-Shared\tools\public_export.py --push 2>&1 | Select-Object -Last 2 | ForEach-Object { Add-Content state/nightly-save.log "$(Get-Date -Format s) public: $_" }
