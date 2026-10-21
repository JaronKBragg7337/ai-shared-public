$ErrorActionPreference = 'Stop'
$slugs = @('rdc-usfed-fomc-2026-09-16-nochng','rdc-usfed-fomc-2026-09-16-hike25')
function Invoke-McpJson([string]$json, [string]$sessionId) {
  $headers = @{ 'Content-Type' = 'application/json'; 'Accept' = 'application/json, text/event-stream' }
  if ($sessionId) { $headers['Mcp-Session-Id'] = $sessionId }
  $resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8765/mcp' -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($json)) -UseBasicParsing
  $sid = $resp.Headers['Mcp-Session-Id']; if (-not $sid) { $sid = $resp.Headers['mcp-session-id'] }
  $data = New-Object System.Collections.Generic.List[string]
  foreach ($line in ($resp.Content -split "`n")) { if ($line.StartsWith('data: ')) { [void]$data.Add($line.Substring(6).Trim()) } }
  return @{ SessionId = $sid; Raw = if ($data.Count -eq 0) { $resp.Content } else { $data[$data.Count-1] } }
}
function Call-Tool([string]$sid,[int]$id,[string]$name,[hashtable]$arguments) {
  $obj = @{ jsonrpc='2.0'; id=$id; method='tools/call'; params=@{ name=$name; arguments=$arguments } }
  return Invoke-McpJson (($obj | ConvertTo-Json -Depth 12 -Compress)) $sid
}
function T([string]$raw){ ($raw | ConvertFrom-Json).result.content[0].text }
$initObj = @{ jsonrpc='2.0'; id=1; method='initialize'; params=@{ protocolVersion='2024-11-05'; capabilities=@{}; clientInfo=@{ name='bridge'; version='1.0' } } }
$sid = (Invoke-McpJson (($initObj | ConvertTo-Json -Depth 8 -Compress)) $null).SessionId
try { Invoke-WebRequest -Uri 'http://127.0.0.1:8765/mcp' -Method POST -Headers @{ 'Content-Type'='application/json'; 'Accept'='application/json, text/event-stream'; 'Mcp-Session-Id'=$sid } -Body ([Text.Encoding]::UTF8.GetBytes('{"jsonrpc":"2.0","method":"notifications/initialized"}')) -UseBasicParsing | Out-Null } catch {}
Write-Output ('TODAY=' + (T (Call-Tool $sid 2 'today' @{}).Raw))
$i=10
foreach($slug in $slugs){
  $i++
  Write-Output ('=== ' + $slug + ' ===')
  Write-Output (T (Call-Tool $sid $i 'polymarket_bbo' @{slug=$slug}).Raw)
}
