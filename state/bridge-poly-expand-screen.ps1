$ErrorActionPreference = 'Stop'
$out = 'C:\Users\lilli\AI-Shared\state\bridge-poly-screen-next.json'
$queries = @('Fed','NBA','NFL','mayor','election','President','Oscar','championship','Week 1','undefeated')
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
$today = T (Call-Tool $sid 2 'today' @{}).Raw | ConvertFrom-Json
$id = 10
$seen = @{}
$hits = @()
foreach ($q in $queries) {
  $id++
  try { $search = T (Call-Tool $sid $id 'polymarket_search' @{ query = $q }).Raw | ConvertFrom-Json } catch { continue }
  foreach ($ev in @($search.events)) {
    $et = [string]$ev.title
    if ($et -match '(?i)bitcoin|crypto|ethereum|solana|dogecoin|xrp|btc|eth') { continue }
    foreach ($mk in @($ev.markets)) {
      if (-not $mk.tradeable) { continue }
      $slug = [string]$mk.slug
      if (-not $slug -or $seen.ContainsKey($slug)) { continue }
      $bid=$null;$ask=$null
      if ($mk.bestBidQuote -and $mk.bestBidQuote.value) { $bid=[double]$mk.bestBidQuote.value }
      if ($mk.bestAskQuote -and $mk.bestAskQuote.value) { $ask=[double]$mk.bestAskQuote.value }
      if ($null -eq $bid -or $null -eq $ask) { continue }
      $spread = [math]::Round($ask - $bid, 4)
      if ($spread -lt 0.005 -or $spread -gt 0.02) { continue }
      if ($ask -lt 0.10 -or $bid -gt 0.90) { continue }
      $seen[$slug] = $true
      $question = if ($mk.question) { [string]$mk.question } else { $et }
      $desc = [string]$mk.description
      # researchability heuristic: near-term end or concrete named entity / election / rate / week
      $score = 0
      if ($question -match '(?i)fed|rate cut|FOMC|mayor|election|Week 1|Week 2|undefeated|champion') { $score += 2 }
      if ($desc -match '(?i)Federal Reserve|election|Week 1|regular season') { $score += 1 }
      try {
        $end = [datetime]$mk.endDate
        $days = ($end - [datetime]$today.utc.Replace(' UTC','')).TotalDays
        if ($days -ge 0 -and $days -le 45) { $score += 2 }
        elseif ($days -le 120) { $score += 1 }
      } catch {}
      $hits += [pscustomobject]@{
        slug=$slug; question=$question; event=$et; bid=$bid; ask=$ask; spread=$spread
        reason=[string]$mk.tradeable_reason; endDate=[string]$mk.endDate; score=$score
        description= if ($desc.Length -gt 220) { $desc.Substring(0,220) } else { $desc }
      }
    }
  }
}
$ranked = @($hits | Sort-Object @{Expression='score';Descending=$true}, spread, ask)
$top = @($ranked | Select-Object -First 40)
$summary = [ordered]@{
  today = $today
  query_count = $queries.Count
  hit_count = $hits.Count
  top = $top
  already_sent_scout = @('cbpac-usfed-2026-cut','aachc-nfl-wk1-2026-09-14-mostpasstds-jusher','usmayewc-usmayor-oaklan-2026-11-03-barlee')
}
($summary | ConvertTo-Json -Depth 6) | Set-Content $out -Encoding utf8
Write-Output ('HITS=' + $hits.Count + ' TOP=' + $top.Count)
$top | Select-Object -First 25 | ForEach-Object {
  Write-Output ('{0} | {1} | bid={2} ask={3} spr={4} score={5}' -f $_.slug, $_.question, $_.bid, $_.ask, $_.spread, $_.score)
}
