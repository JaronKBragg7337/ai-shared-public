$ErrorActionPreference = 'Stop'
$slimPath = 'C:\Users\lilli\AI-Shared\state\bridge-poly-slim.json'

function Invoke-McpJson([string]$json, [string]$sessionId) {
  $headers = @{ 'Content-Type' = 'application/json'; 'Accept' = 'application/json, text/event-stream' }
  if ($sessionId) { $headers['Mcp-Session-Id'] = $sessionId }
  $resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8765/mcp' -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($json)) -UseBasicParsing
  $sid = $resp.Headers['Mcp-Session-Id']
  if (-not $sid) { $sid = $resp.Headers['mcp-session-id'] }
  $text = $resp.Content
  $dataLines = New-Object System.Collections.Generic.List[string]
  foreach ($line in ($text -split "`n")) {
    if ($line.StartsWith('data: ')) { [void]$dataLines.Add($line.Substring(6).Trim()) }
  }
  $payload = if ($dataLines.Count -eq 0) { $text } else { $dataLines[$dataLines.Count - 1] }
  return @{ SessionId = $sid; Raw = $payload }
}

function Get-ToolPayload([string]$raw) {
  $rpc = $raw | ConvertFrom-Json
  if ($rpc.error) { return @{ isError = $true; text = ($rpc.error | ConvertTo-Json -Compress) } }
  $text = $rpc.result.content[0].text
  return @{ isError = [bool]$rpc.result.isError; text = $text }
}

function Call-Tool([string]$sid, [int]$id, [string]$name, [hashtable]$arguments) {
  $obj = @{ jsonrpc = '2.0'; id = $id; method = 'tools/call'; params = @{ name = $name; arguments = $arguments } }
  $json = $obj | ConvertTo-Json -Depth 20 -Compress
  return Invoke-McpJson $json $sid
}

$initObj = @{ jsonrpc='2.0'; id=1; method='initialize'; params=@{ protocolVersion='2024-11-05'; capabilities=@{}; clientInfo=@{ name='bridge'; version='1.0' } } }
$init = Invoke-McpJson (($initObj | ConvertTo-Json -Depth 10 -Compress)) $null
$sid = $init.SessionId
try {
  $h = @{ 'Content-Type'='application/json'; 'Accept'='application/json, text/event-stream'; 'Mcp-Session-Id'=$sid }
  Invoke-WebRequest -Uri 'http://127.0.0.1:8765/mcp' -Method POST -Headers $h -Body ([System.Text.Encoding]::UTF8.GetBytes('{"jsonrpc":"2.0","method":"notifications/initialized"}')) -UseBasicParsing | Out-Null
} catch {}

$toolsRaw = Invoke-McpJson '{"jsonrpc":"2.0","id":99,"method":"tools/list","params":{}}' $sid
$tools = ($toolsRaw.Raw | ConvertFrom-Json).result.tools
$wanted = @('polymarket_orderbook','polymarket_bbo','polymarket_market','polymarket_search')
$schemaOut = @{}
foreach ($t in $tools) {
  if ($wanted -contains $t.name) { $schemaOut[$t.name] = ($t.inputSchema | ConvertTo-Json -Compress -Depth 8) }
}

$today = (Get-ToolPayload (Call-Tool $sid 2 'today' @{}).Raw).text | ConvertFrom-Json
$bal = (Get-ToolPayload (Call-Tool $sid 3 'polymarket_account_balances' @{}).Raw).text | ConvertFrom-Json
$search = (Get-ToolPayload (Call-Tool $sid 4 'polymarket_search' @{ query = 'Atlanta Green Bay'; limit = 5 }).Raw).text | ConvertFrom-Json

$rows = @()
foreach ($ev in @($search.events)) {
  foreach ($mk in @($ev.markets)) {
    if (-not $mk.tradeable) { continue }
    $bid = $null; $ask = $null
    if ($mk.bestBidQuote -and $mk.bestBidQuote.PSObject.Properties.Name -contains 'value') { $bid = [double]$mk.bestBidQuote.value }
    elseif ($mk.bestBidQuote) { try { $bid = [double]$mk.bestBidQuote } catch {} }
    if ($mk.bestAskQuote -and $mk.bestAskQuote.PSObject.Properties.Name -contains 'value') { $ask = [double]$mk.bestAskQuote.value }
    elseif ($mk.bestAskQuote) { try { $ask = [double]$mk.bestAskQuote } catch {} }
    if ($null -eq $bid -or $null -eq $ask) { continue }
    $q = if ($mk.question) { [string]$mk.question } elseif ($mk.title) { [string]$mk.title } else { [string]$ev.title }
    $rows += [pscustomobject]@{
      event = [string]$ev.title
      question = $q
      id = [string]$mk.id
      bid = $bid
      ask = $ask
      spread = [math]::Round($ask - $bid, 4)
      reason = [string]$mk.tradeable_reason
      endDate = [string]$mk.endDate
      mid = [math]::Round(($bid+$ask)/2, 4)
    }
  }
}

$money = @($rows | Where-Object {
  $_.spread -le 0.05 -and $_.ask -gt 0.05 -and $_.bid -lt 0.95 -and
  $_.question -match '(?i)winner|moneyline|beat|to win|Falcons win|Packers win|Atlanta win|Green Bay win'
} | Sort-Object spread, @{Expression={ [math]::Abs($_.mid - 0.5) }})
if ($money.Count -eq 0) {
  $money = @($rows | Where-Object { $_.spread -le 0.03 -and $_.ask -gt 0.1 -and $_.bid -lt 0.9 } | Sort-Object spread, @{Expression={ [math]::Abs($_.mid - 0.5) }})
}
$picked = @($money | Select-Object -First 15)
if ($picked.Count -eq 0) { $picked = @($rows | Sort-Object spread | Select-Object -First 15) }
$top = $picked | Select-Object -First 1

$detail = $null
if ($top) {
  $attempts = @()
  foreach ($argName in @('marketId','market_id','id','slug')) {
    $args = @{}; $args[$argName] = $top.id
    $obP = Get-ToolPayload (Call-Tool $sid 5 'polymarket_orderbook' $args).Raw
    $preview = if ($obP.text) { $obP.text.Substring(0, [Math]::Min(300, $obP.text.Length)) } else { '' }
    $attempts += [ordered]@{ tool='orderbook'; arg=$argName; isError=$obP.isError; preview=$preview }
    $looksBad = $obP.isError -or ($obP.text -match '^(Error|Invalid|Unknown)')
    if (-not $looksBad) {
      $bboP = Get-ToolPayload (Call-Tool $sid 6 'polymarket_bbo' $args).Raw
      $mktP = Get-ToolPayload (Call-Tool $sid 7 'polymarket_market' $args).Raw
      $newsP = Get-ToolPayload (Call-Tool $sid 8 'research_news' @{ query = 'Atlanta Falcons vs Green Bay Packers NFL preview' }).Raw
      $detail = [ordered]@{
        candidate = $top
        argName = $argName
        orderbook_preview = $obP.text.Substring(0, [Math]::Min(1500, $obP.text.Length))
        bbo_preview = $bboP.text.Substring(0, [Math]::Min(800, $bboP.text.Length))
        market_preview = $mktP.text.Substring(0, [Math]::Min(1500, $mktP.text.Length))
        news_preview = $newsP.text.Substring(0, [Math]::Min(2000, $newsP.text.Length))
      }
      break
    }
  }
  if (-not $detail) { $detail = [ordered]@{ candidate = $top; attempts = $attempts } }
}

$summary = [ordered]@{
  today = $today
  balance = $bal.balances[0].currentBalance
  buyingPower = $bal.balances[0].buyingPower
  tradeable_with_quotes = $rows.Count
  schemas = $schemaOut
  candidates = $picked
  detail = $detail
}
($summary | ConvertTo-Json -Depth 8) | Set-Content -Path $slimPath -Encoding utf8
Write-Output ("OK quotes={0} picked={1}" -f $rows.Count, $picked.Count)
if ($top) { Write-Output ("TOP [{0}] bid={1} ask={2} spread={3} id={4}" -f $top.question, $top.bid, $top.ask, $top.spread, $top.id) }
Write-Output ("SIZE=" + (Get-Item $slimPath).Length)
