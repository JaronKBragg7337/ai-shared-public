$ErrorActionPreference = 'Stop'
$out = 'C:\Users\lilli\AI-Shared\state\bridge-poly-pick.json'

function Invoke-McpJson([string]$json, [string]$sessionId) {
  $headers = @{ 'Content-Type' = 'application/json'; 'Accept' = 'application/json, text/event-stream' }
  if ($sessionId) { $headers['Mcp-Session-Id'] = $sessionId }
  $resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8765/mcp' -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($json)) -UseBasicParsing
  $sid = $resp.Headers['Mcp-Session-Id']; if (-not $sid) { $sid = $resp.Headers['mcp-session-id'] }
  $text = $resp.Content
  $dataLines = New-Object System.Collections.Generic.List[string]
  foreach ($line in ($text -split "`n")) { if ($line.StartsWith('data: ')) { [void]$dataLines.Add($line.Substring(6).Trim()) } }
  $payload = if ($dataLines.Count -eq 0) { $text } else { $dataLines[$dataLines.Count - 1] }
  return @{ SessionId = $sid; Raw = $payload }
}
function ToolText([string]$raw) { ($raw | ConvertFrom-Json).result.content[0].text }
function Call-Tool([string]$sid, [int]$id, [string]$name, [hashtable]$arguments) {
  $obj = @{ jsonrpc='2.0'; id=$id; method='tools/call'; params=@{ name=$name; arguments=$arguments } }
  return Invoke-McpJson (($obj | ConvertTo-Json -Depth 20 -Compress)) $sid
}

$init = Invoke-McpJson ((@{ jsonrpc='2.0'; id=1; method='initialize'; params=@{ protocolVersion='2024-11-05'; capabilities=@{}; clientInfo=@{ name='bridge'; version='1.0' } } } | ConvertTo-Json -Depth 10 -Compress)) $null
$sid = $init.SessionId
try { Invoke-WebRequest -Uri 'http://127.0.0.1:8765/mcp' -Method POST -Headers @{ 'Content-Type'='application/json'; 'Accept'='application/json, text/event-stream'; 'Mcp-Session-Id'=$sid } -Body ([Text.Encoding]::UTF8.GetBytes('{"jsonrpc":"2.0","method":"notifications/initialized"}')) -UseBasicParsing | Out-Null } catch {}

$today = ToolText (Call-Tool $sid 2 'today' @{}).Raw | ConvertFrom-Json
$search = ToolText (Call-Tool $sid 3 'polymarket_search' @{ query = 'Atlanta vs. Green Bay' }).Raw | ConvertFrom-Json

$mains = @()
$props = @()
foreach ($ev in @($search.events)) {
  if ($ev.title -ne 'Atlanta vs. Green Bay') { continue }
  foreach ($mk in @($ev.markets)) {
    $bid=$null;$ask=$null
    if ($mk.bestBidQuote -and $mk.bestBidQuote.value) { $bid=[double]$mk.bestBidQuote.value }
    if ($mk.bestAskQuote -and $mk.bestAskQuote.value) { $ask=[double]$mk.bestAskQuote.value }
    $q = [string]$mk.question
    $row = [ordered]@{
      question=$q; id=[string]$mk.id; slug=[string]$mk.slug; tradeable=[bool]$mk.tradeable; reason=[string]$mk.tradeable_reason
      bid=$bid; ask=$ask; spread= if ($bid -ne $null -and $ask -ne $null) { [math]::Round($ask-$bid,4) } else { $null }
      endDate=[string]$mk.endDate
    }
    if ($q -match '(?i)^Will (Atlanta Falcons|Green Bay Packers) win\?$') { $mains += [pscustomobject]$row }
    elseif ($q -match '(?i)win the (game|matchup)|^Atlanta|^Green Bay' -and $q -notmatch '(?i)quarter|half|spread|yard|touchdown|points') { $mains += [pscustomobject]$row }
    else { $props += [pscustomobject]$row }
  }
}

# Also catch exact winner phrasing variations
if ($mains.Count -eq 0) {
  foreach ($ev in @($search.events)) {
    if ($ev.title -ne 'Atlanta vs. Green Bay') { continue }
    foreach ($mk in @($ev.markets)) {
      $q=[string]$mk.question
      if ($q -match '(?i)(Falcons|Packers).*(win the game|to win)|moneyline|Winner') {
        $bid=$null;$ask=$null
        if ($mk.bestBidQuote -and $mk.bestBidQuote.value) { $bid=[double]$mk.bestBidQuote.value }
        if ($mk.bestAskQuote -and $mk.bestAskQuote.value) { $ask=[double]$mk.bestAskQuote.value }
        $mains += [pscustomobject]@{ question=$q; id=[string]$mk.id; slug=[string]$mk.slug; tradeable=[bool]$mk.tradeable; reason=[string]$mk.tradeable_reason; bid=$bid; ask=$ask; spread=if($bid-ne$null-and$ask-ne$null){[math]::Round($ask-$bid,4)}else{$null}; endDate=[string]$mk.endDate }
      }
    }
  }
}

# List first 30 market questions for diagnosis if needed
$sampleQs = @()
foreach ($ev in @($search.events)) {
  if ($ev.title -ne 'Atlanta vs. Green Bay') { continue }
  foreach ($mk in @($ev.markets | Select-Object -First 40)) {
    $sampleQs += [string]$mk.question
  }
}

$pick = @($mains | Where-Object { $_.tradeable -and $_.bid -ne $null -and $_.ask -ne $null } | Sort-Object spread) | Select-Object -First 2
$detail = @()
foreach ($p in @($pick)) {
  if (-not $p.slug) { continue }
  $ob = ToolText (Call-Tool $sid 10 'polymarket_orderbook' @{ slug = $p.slug }).Raw
  $bbo = ToolText (Call-Tool $sid 11 'polymarket_bbo' @{ slug = $p.slug }).Raw
  $mkt = ToolText (Call-Tool $sid 12 'polymarket_market' @{ slug = $p.slug }).Raw
  $detail += [ordered]@{
    market = $p
    bbo = ($bbo.Substring(0, [Math]::Min(500, $bbo.Length)))
    orderbook = ($ob.Substring(0, [Math]::Min(1200, $ob.Length)))
    market_tool = ($mkt.Substring(0, [Math]::Min(1200, $mkt.Length)))
  }
}
$news = ToolText (Call-Tool $sid 13 'research_news' @{ query = 'Falcons vs Packers NFL odds preview' }).Raw

$summary = [ordered]@{
  today = $today
  mains = $mains
  sample_questions = $sampleQs
  details = $detail
  news_preview = $news.Substring(0, [Math]::Min(2500, $news.Length))
}
($summary | ConvertTo-Json -Depth 8) | Set-Content $out -Encoding utf8
Write-Output ("MAINS=" + $mains.Count)
foreach ($m in $mains) { Write-Output ("MAIN [{0}] slug={1} bid={2} ask={3} tradeable={4}" -f $m.question, $m.slug, $m.bid, $m.ask, $m.tradeable) }
Write-Output ("SAMPLE_N=" + $sampleQs.Count)
$sampleQs | Select-Object -First 25 | ForEach-Object { Write-Output ("Q: " + $_) }
Write-Output ("SIZE=" + (Get-Item $out).Length)
