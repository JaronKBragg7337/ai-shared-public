$sum = Invoke-RestMethod -Uri 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401868329' -TimeoutSec 25
$last = $sum.winprobability | Select-Object -Last 1
$famu = [math]::Round(1 - $last.homeWinPercentage, 4)
$detail = $sum.header.competitions[0].status.type.detail
$scores = ($sum.header.competitions[0].competitors | ForEach-Object { $_.team.abbreviation + '=' + $_.score }) -join ' '
Set-Content 'C:\Users\lilli\AI-Shared\state\_espn-famu-tmp.txt' "homeWP=$($last.homeWinPercentage) famuWP=$famu detail=$detail scores=$scores"
