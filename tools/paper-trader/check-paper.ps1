$ErrorActionPreference = 'Stop'
$failures = 0
Write-Host 'PAPER ONLY health check (no trades or repairs)'
foreach ($endpoint in @('http://127.0.0.1:11434/api/tags','http://127.0.0.1:19789/healthz')) {
    try {
        $response = Invoke-WebRequest -Uri $endpoint -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -ne 200) { throw 'Non-200 response' }
        Write-Host "PASS $endpoint"
    } catch { Write-Host "FAIL $endpoint"; $failures++ }
}
$task = Get-ScheduledTask -TaskName 'OpenClaw Paper Gateway'
$info = $task | Get-ScheduledTaskInfo
Write-Host "Task state: $($task.State); last result: $($info.LastTaskResult); last start: $($info.LastRunTime)"
if ($task.State -ne 'Running') { $failures++ }
Write-Host 'This checks availability, not inference, paper performance, or cold-boot provenance.'
if ($failures) { exit 1 }
