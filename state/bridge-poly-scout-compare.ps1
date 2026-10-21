$ErrorActionPreference = 'Stop'
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
$slug = 'aec-nfl-atl-gb-2026-09-24'
$mkt = T (Call-Tool $sid 3 'polymarket_market' @{ slug = $slug }).Raw
$bbo = T (Call-Tool $sid 4 'polymarket_bbo' @{ slug = $slug }).Raw
$ob = T (Call-Tool $sid 5 'polymarket_orderbook' @{ slug = $slug }).Raw
$search = T (Call-Tool $sid 6 'polymarket_search' @{ query = 'Atlanta Falcons vs Green Bay Packers' }).Raw | ConvertFrom-Json

# Find related winner / moneyline markets with sides
$related = @()
foreach ($ev in @($search.events)) {
  foreach ($mk in @($ev.markets)) {
    $q = [string]$mk.question
    if ($q -match '(?i)who will win|Falcons win\?$|Packers win\?$|beat|moneyline|winner' -and $q -notmatch '(?i)quarter|half|points|touchdown|margin|race|cover|total') {
      $bid=$null;$ask=$null
      if ($mk.bestBidQuote -and $mk.bestBidQuote.value) { $bid = $mk.bestBidQuote.value }
      if ($mk.bestAskQuote -and $mk.bestAskQuote.value) { $ask = $mk.bestAskQuote.value }
      $related += [pscustomobject]@{ event=[string]$ev.title; q=$q; slug=[string]$mk.slug; id=[string]$mk.id; tradeable=[bool]$mk.tradeable; reason=[string]$mk.tradeable_reason; bid=$bid; ask=$ask; outcomes=($mk.outcomes | ConvertTo-Json -Compress) }
    }
  }
}

$out = 'C:\Users\lilli\AI-Shared\state\bridge-poly-scout-compare.json'
$summary = [ordered]@{
  today = ($today | ConvertFrom-Json)
  moneyline_slug = $slug
  market = ($mkt.Substring(0, [Math]::Min(4000, $mkt.Length)))
  bbo = ($bbo.Substring(0, [Math]::Min(2000, $bbo.Length)))
  orderbook = ($ob.Substring(0, [Math]::Min(2500, $ob.Length)))
  related = $related
}
($summary | ConvertTo-Json -Depth 8) | Set-Content $out -Encoding utf8
Write-Output ('TODAY=' + $today)
Write-Output '---BBO---'
Write-Output $bbo
Write-Output '---MARKET_HEAD---'
Write-Output $mkt.Substring(0, [Math]::Min(2500, $mkt.Length))
Write-Output '---RELATED---'
$related | ForEach-Object { Write-Output ("{0} | slug={1} bid={2} ask={3} t={4} outcomes={5}" -f $_.q, $_.slug, $_.bid, $_.ask, $_.tradeable, $_.outcomes) }
Write-Output ('SIZE=' + (Get-Item $out).Length)
