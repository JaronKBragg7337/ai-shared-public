# Save the Anthropic API key from the clipboard into C:\Users\lilli\.secrets\keys.env (never shown on screen).
Add-Type -AssemblyName PresentationFramework
$k = (Get-Clipboard -Raw)
if ($k) { $k = $k.Trim() }
if (-not $k -or $k -notmatch '^sk-ant-[a-z]+\d*-?[A-Za-z0-9_\-]{20,}$') {
  [System.Windows.MessageBox]::Show("The clipboard doesn't hold a Claude API key yet.`n`nIn the console, press the Copy button next to the new key, then double-click this again.", "Save Claude key") | Out-Null; exit }
$f = 'C:\Users\lilli\.secrets\keys.env'
$lines = Get-Content $f
$found = $false
$lines = $lines | ForEach-Object { if ($_ -match '^ANTHROPIC_API_KEY=') { $found = $true; "ANTHROPIC_API_KEY=$k" } else { $_ } }
if (-not $found) { $lines += "ANTHROPIC_API_KEY=$k" }
Set-Content -Path $f -Value $lines -Encoding UTF8
Set-Clipboard -Value ' '
try { $r = Invoke-RestMethod -Uri 'https://api.anthropic.com/v1/models' -Headers @{ 'x-api-key' = $k; 'anthropic-version' = '2023-06-01' } -TimeoutSec 20; $ok = "and it works (Claude answered)." }
catch { $ok = "but the test call failed: $($_.Exception.Message). Claude will look at it." }
Add-Content 'C:\Users\lilli\AI-Shared\state\timeline.md' ("- " + (Get-Date -Format 'yyyy-MM-dd HH:mm') + " Anthropic API key saved to keys.env by Jaron (ends ..." + $k.Substring($k.Length-4) + ")")
[System.Windows.MessageBox]::Show("Saved. Key ending ..." + $k.Substring($k.Length-4) + " is in the safe file, $ok`n`nYour clipboard was cleared. You can close the console now.", "Save Claude key") | Out-Null
