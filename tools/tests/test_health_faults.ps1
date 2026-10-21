param([ValidateSet('healthy','http500','proposer-failed','stale')][string]$Scenario='healthy')
# Isolated function mocks. No services, orders or task definitions are changed.
function Get-CimInstance { [pscustomobject]@{LastBootUpTime=(Get-Date).AddHours(-1)} }
function Get-NetTCPConnection { [pscustomobject]@{LocalPort=1} }
function Get-ScheduledTask {
    param($TaskName)
    $state = if ($TaskName -in 'Paper Sync','OpenClaw Paper Gateway') {'Disabled'}
        elseif ($TaskName -in 'Grok Machine MCP','Desktop Commander Remote','Fly Brain','Polymarket MCP','Qwen Remote Bridge') {'Running'} else {'Ready'}
    [pscustomobject]@{TaskName=$TaskName;State=$state}
}
function Get-ScheduledTaskInfo {
    param([Parameter(ValueFromPipeline)]$Task)
    process {
        $result = if ($Scenario -eq 'proposer-failed' -and $Task.TaskName -eq 'Trade Proposer') {1} else {0}
        [pscustomobject]@{LastRunTime=(Get-Date).AddMinutes(-2);LastTaskResult=$result}
    }
}
function Invoke-RestMethod { [pscustomobject]@{models=@([pscustomobject]@{name='fixture'})} }
function Invoke-WebRequest { [pscustomobject]@{StatusCode=$(if($Scenario -eq 'http500'){500}else{404})} }
function Test-Path { $true }
function Get-Item {
    param($LiteralPath)
    $age = if ($Scenario -eq 'stale' -and $LiteralPath -like '*verifier.md') {60} else {1}
    [pscustomobject]@{LastWriteTime=(Get-Date).AddMinutes(-$age)}
}
& (Join-Path (Split-Path $PSScriptRoot -Parent) 'postboot-check.ps1')
exit $LASTEXITCODE
