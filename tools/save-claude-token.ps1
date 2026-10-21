# Save the Claude Code login token (from `claude setup-token`) from the clipboard into C:\Users\lilli\.secrets\keys.env.
# Lets the MSI's scheduled jobs (the Anthropic scout) use Claude for a year without logging in. Never shown on screen.
Add-Type -AssemblyName PresentationFramework
$k = (Get-Clipboard -Raw)
if ($k) { $k = ($k -replace '\s', '') }
if (-not $k -or $k -notmatch '^sk-ant-oat\d*-[A-Za-z0-9_\-]{20,}$') {
  [System.Windows.MessageBox]::Show("The clipboard doesn't hold the Claude token yet.`n`nIn the black window, highlight the long line that starts with sk-ant-oat, press Ctrl+C, then double-click this again.", "Save Claude token") | Out-Null; exit }
$f = 'C:\Users\lilli\.secrets\keys.env'
$lines = Get-Content $f
$found = $false
$lines = $lines | ForEach-Object { if ($_ -match '^CLAUDE_CODE_OAUTH_TOKEN=') { $found = $true; "CLAUDE_CODE_OAUTH_TOKEN=$k" } else { $_ } }
if (-not $found) { $lines += "CLAUDE_CODE_OAUTH_TOKEN=$k" }
Set-Content -Path $f -Value $lines -Encoding UTF8
Set-Clipboard -Value ' '
$env:CLAUDE_CODE_OAUTH_TOKEN = $k
$out = (& claude -p "Reply with just: ok" 2>&1 | Out-String).Trim()
if ($out -match '(?i)\bok\b' -and $out -notmatch '(?i)error|expired|401') { $ok = "and it works (Claude answered)." } else { $ok = "but the test didn't answer right ($out). Claude will look at it." }
Add-Content 'C:\Users\lilli\AI-Shared\state\timeline.md' ("- " + (Get-Date -Format 'yyyy-MM-dd HH:mm') + " Claude Code token saved to keys.env by Jaron (ends ..." + $k.Substring($k.Length-4) + ")")
[System.Windows.MessageBox]::Show("Saved. Token ending ..." + $k.Substring($k.Length-4) + " is in the safe file, $ok`n`nYour clipboard was cleared. You can close the black window now.", "Save Claude token") | Out-Null
