Set-Location C:\Users\lilli\AI-Shared
$d = Get-Date -Format "yyyy-MM-dd"
$p = "You are Atlas. Today is $d. Read the file C:\Users\lilli\AI-Shared\agents\atlas\BRIEF.md and follow it exactly, using $d wherever it says DATE."
& "C:\Users\lilli\.grok\bin\grok.exe" -p $p --always-approve --max-turns 50 *> "agents\atlas\last-run.out"
