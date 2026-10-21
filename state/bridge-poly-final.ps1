$ErrorActionPreference = 'Stop'
$out = 'C:\Users\lilli\AI-Shared\state\bridge-poly-pick.json'
function Invoke-McpJson([string]$json, [string]$sessionId) {
  $headers = @{ 'Content-Type' = 'application/json'; 'Accept' = 'application/json, text/event-stream' }
  if ($sessionId) { $headers['Mcp-Session-Id'] = $sessionId }
  $resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8765/mcp' -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($json)) -UseBasicParsing
  $sid = $resp.Headers['Mcp-Session-Id']; if (-not $sid) { $sid = $resp.Headers['mcp-session-id'] }
  $dataLines = New-Object System.Collections.Generic.List[string]
  foreach ($line in ($resp.Content -split "`n")) { if ($line.StartsWith('data: ')) { [void]$dataLines.Add($line.Substring(6).Trim()) } }
  $payload = if ($dataLines.Count -eq 0) { $resp.Content } else { $dataLines[$dataLines.Count - 1] }
  return @{ SessionId = $sid; Raw = $payload }
}
function ToolText([string]$raw) { ($raw | ConvertFrom-Json).result.content[0].text }
function Call-Tool([string]$sid, [int]$id, [string]$name, [hashtable]$arguments) {
  $obj = @{ jsonrpc='2.0'; id=$id; method='tools/call'; params=@{ name=$name; arguments=$arguments } }
  return Invoke-McpJson (($obj | ConvertTo-Json -Depth 20 -Compress)) $sid
}
$initObj = @{ jsonrpc='2.0'; id=1; method='initialize'; params=@{ protocolVersion='2024-11-05'; capabilities=@{}; clientInfo=@{ name='bridge'; version='1.0' } } }
$sid = (Invoke-McpJson (($initObj | ConvertTo-Json -Depth 10 -Compress)) $null).SessionId
try { Invoke-WebRequest -Uri 'http://127.0.0.1:8765/mcp' -Method POST -Headers @{ 'Content-Type'='application/json'; 'Accept'='application/json, text/event-stream'; 'Mcp-Session-Id'=$sid } -Body ([Text.Encoding]::UTF8.GetBytes('{"jsonrpc":"2.0","method":"notifications/initialized"}')) -UseBasicParsing | Out-Null } catch {}

$today = ToolText (Call-Tool $sid 2 'today' @{}).Raw | ConvertFrom-Json
$bal = ToolText (Call-Tool $sid 3 'polymarket_account_balances' @{}).Raw | ConvertFrom-Json
$search = ToolText (Call-Tool $sid 4 'polymarket_search' @{ query = 'Atlanta vs. Green Bay' }).Raw | ConvertFrom-Json
$ev = @($search.events) | Where-Object { $_.title -eq 'Atlanta vs. Green Bay' } | Select-Object -First 1

$around = @()
$filtered = @()
foreach ($mk in @($ev.markets)) {
  $bid=$null; $ask=$null
  if ($mk.bestBidQuote -and $mk.bestBidQuote.value) { $bid = [double]$mk.bestBidQuote.value }
  if ($mk.bestAskQuote -and $mk.bestAskQuote.value) { $ask = [double]$mk.bestAskQuote.value }
  $q = [string]$mk.question
  $row = [ordered]@{ q=$q; slug=[string]$mk.slug; id=[string]$mk.id; tradeable=[bool]$mk.tradeable; reason=[string]$mk.tradeable_reason; bid=$bid; ask=$ask }
  if ($bid -ne $null -and $ask -ne $null -and $bid -ge 0.40 -and $bid -le 0.46 -and $ask -ge 0.40 -and $ask -le 0.48) { $around += [pscustomobject]$row }
  if ($q -notmatch '(?i)quarter|half|touchdown|points|margin|race to|highest|exact|first team|tied|over|under|spread|yard') { $filtered += [pscustomobject]$row }
}

# Prove slug orderbook on a known tradeable prop
$prop = @($ev.markets) | Where-Object { $_.id -eq 779858 -or [string]$_.id -eq '779858' -or $_.question -eq 'Will Atlanta Falcons win the fourth quarter?' } | Select-Object -First 1
$slug = [string]$prop.slug
$ob = $null; $bbo = $null; $news = $null
if ($slug) {
  $ob = ToolText (Call-Tool $sid 5 'polymarket_orderbook' @{ slug = $slug }).Raw
  $bbo = ToolText (Call-Tool $sid 6 'polymarket_bbo' @{ slug = $slug }).Raw
  $news = ToolText (Call-Tool $sid 7 'research_news' @{ query = 'Falcons Packers NFL preview September 2026' }).Raw
}

$summary = [ordered]@{
  today = $today
  balance = $bal.balances[0].currentBalance
  buyingPower = $bal.balances[0].buyingPower
  event_markets = @($ev.markets).Count
  tradeable_market_count = $ev.tradeable_market_count
  filtered_non_prop_count = $filtered.Count
  filtered = $filtered
  around_043 = $around
  prop = [ordered]@{
    question = [string]$prop.question
    id = [string]$prop.id
    slug = $slug
    bid = if ($prop.bestBidQuote) { $prop.bestBidQuote.value } else { $null }
    ask = if ($prop.bestAskQuote) { $prop.bestAskQuote.value } else { $null }
    tradeable = [bool]$prop.tradeable
    reason = [string]$prop.tradeable_reason
  }
  orderbook_preview = if ($ob) { $ob.Substring(0, [Math]::Min(1500, $ob.Length)) } else { $null }
  bbo_preview = if ($bbo) { $bbo.Substring(0, [Math]::Min(800, $bbo.Length)) } else { $null }
  news_preview = if ($news) { $news.Substring(0, [Math]::Min(2000, $news.Length)) } else { $null }
}
($summary | ConvertTo-Json -Depth 6) | Set-Content $out -Encoding utf8
Write-Output ("FILTERED=" + $filtered.Count)
$filtered | ForEach-Object { Write-Output ("F [{0}] slug={1} bid={2} ask={3}" -f $_.q, $_.slug, $_.bid, $_.ask) }
Write-Output ("AROUND=" + $around.Count)
$around | Select-Object -First 20 | ForEach-Object { Write-Output ("A [{0}] slug={1} bid={2} ask={3}" -f $_.q, $_.slug, $_.bid, $_.ask) }
Write-Output ("PROP slug=$slug bid=$($summary.prop.bid) ask=$($summary.prop.ask)")
if ($bbo) { Write-Output ("BBO=" + $bbo.Substring(0, [Math]::Min(400, $bbo.Length))) }
Write-Output ("SIZE=" + (Get-Item $out).Length)
