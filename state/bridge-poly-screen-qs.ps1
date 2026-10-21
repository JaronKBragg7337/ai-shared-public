$ErrorActionPreference = 'Stop'
$slugs = @(
  'cbpac-usfed-2026-cut',
  'tec-nba-eastconf-2027-05-19-w-mia',
  'tec-nba-champ-2027-06-18-w-phi',
  'aachc-nfl-2027-01-10-lastundefeated-chi',
  'usmayewc-usmayor-oaklan-2026-11-03-barlee',
  'aachc-nfl-wk1-2026-09-14-mostpasstds-jusher'
)
function Invoke-McpJson([string]$json, [string]$sessionId) {
  $headers = @{ 'Content-Type' = 'application/json'; 'Accept' = 'application/json, text/event-stream' }
  if ($sessionId) { $headers['Mcp-Session-Id'] = $sessionId }
  $resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8765/mcp' -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($json)) -UseBasicParsing
  $sid = $resp.Headers['Mcp-Session-Id']; if (-not $sid) { $sid = $resp.Headers['mcp-session-id'] }
  $data = New-Object System.Collections.Generic.List[string]
  foreach ($line in ($resp.Content -split "`n")) { if ($line.StartsWith('data: ')) { [void]$data.Add($line.Substring(6).Trim()) } }
  return @{ SessionId = $sid; Raw = if ($data.Count -eq 0) { $resp.Content } else { $data[$data.Count-1] } }
}
function Call-Tool([string]$sid, [int]$id, [string]$name, [hashtable]$arguments) {
  $obj = @{ jsonrpc='2.0'; id=$id; method='tools/call'; params=@{ name=$name; arguments=$arguments } }
  return Invoke-McpJson (($obj | ConvertTo-Json -Depth 12 -Compress)) $sid
}
function T([string]$raw) { ($raw | ConvertFrom-Json).result.content[0].text }
$initObj = @{ jsonrpc='2.0'; id=1; method='initialize'; params=@{ protocolVersion='2024-11-05'; capabilities=@{}; clientInfo=@{ name='bridge'; version='1.0' } } }
$sid = (Invoke-McpJson (($initObj | ConvertTo-Json -Depth 8 -Compress)) $null).SessionId
try { Invoke-WebRequest -Uri 'http://127.0.0.1:8765/mcp' -Method POST -Headers @{ 'Content-Type'='application/json'; 'Accept'='application/json, text/event-stream'; 'Mcp-Session-Id'=$sid } -Body ([Text.Encoding]::UTF8.GetBytes('{"jsonrpc":"2.0","method":"notifications/initialized"}')) -UseBasicParsing | Out-Null } catch {}
$today = T (Call-Tool $sid 2 'today' @{}).Raw
$i = 10
$rows = @()
foreach ($slug in $slugs) {
  $i++
  $mktText = T (Call-Tool $sid $i 'polymarket_market' @{ slug = $slug }).Raw
  $bboText = T (Call-Tool $sid ($i+100) 'polymarket_bbo' @{ slug = $slug }).Raw
  $m = $mktText | ConvertFrom-Json
  $b = $bboText | ConvertFrom-Json
  $market = $m.market
  $md = $b.marketData
  $bid = $null; $ask = $null
  if ($md.bestBid -and $md.bestBid.value) { $bid = [double]$md.bestBid.value }
  if ($md.bestAsk -and $md.bestAsk.value) { $ask = [double]$md.bestAsk.value }
  $spread = if ($bid -ne $null -and $ask -ne $null) { [math]::Round($ask - $bid, 4) } else { $null }
  $sides = @()
  if ($market.marketSides) {
    foreach ($s in @($market.marketSides)) { $sides += [string]$s.description }
  }
  $rows += [pscustomobject]@{
    slug = $slug
    question = [string]$market.question
    description = [string]$market.description
    endDate = [string]$market.endDate
    gameStartTime = [string]$market.gameStartTime
    marketType = [string]$market.marketType
    sides = ($sides -join ' | ')
    longSide = if ($market.marketSides) { (@($market.marketSides) | Where-Object { $_.long } | Select-Object -First 1).description } else { $null }
    bid = $bid
    ask = $ask
    spread = $spread
    tradeable = ($spread -ne $null -and $spread -le 0.02 -and $bid -ge 0.10 -and $ask -le 0.90)
  }
}
$out = 'C:\Users\lilli\AI-Shared\state\bridge-poly-screen.json'
($rows | ConvertTo-Json -Depth 5) | Set-Content $out -Encoding utf8
Write-Output ('TODAY=' + $today)
foreach ($r in $rows) {
  Write-Output ('---')
  Write-Output ('SLUG=' + $r.slug)
  Write-Output ('Q=' + $r.question)
  Write-Output ('SIDES=' + $r.sides)
  Write-Output ('LONG=' + $r.longSide)
  Write-Output ('END=' + $r.endDate + ' START=' + $r.gameStartTime)
  Write-Output ('BID=' + $r.bid + ' ASK=' + $r.ask + ' SPREAD=' + $r.spread)
  Write-Output ('DESC=' + $r.description.Substring(0, [Math]::Min(280, $r.description.Length)))
}
