# The MSI schedule - what runs when, and when to stay off it
Rewritten 2026-10-15 from Windows Task Scheduler (plus the Claude app and claude.ai for the two cloud items). Times are
America/Indiana/Indianapolis. Jaron's rule (10/15): everything heavy runs 3-6 AM while he sleeps; nothing heavy during the day.
Refresh this whenever a task is added, moved, or disabled. The old morning-block schedule (6:30-9:10 AM) is history; see the
dated entries in state/timeline.md.

## THE NIGHT BLOCK - 3:00 to about 7:00 AM. Heavy work lives here; the machine is free the rest of the day.

    03:00       Watch Codex Writer          Codex/Luna news capture -> watch/codex/
    03:00       Watch Kimi First Light      Kimi Eastern desk -> watch/kimi/
    03:00       Watch MSI Reader            headlines fetched from the MSI -> watch/msi/
    03:00       Whats New Scouts
    03:<address>          Codex funding lane (was 2 PM)
    03:00       Necklace Unreal Backup      (was 4:45)
    03:00-03:10 Claude daily capture        "watch-collect", Claude app scheduled task, cron 0 3, dispatch jitter ~9 min (was 8:24)
    03:40       Watch DeepSeek Reader       reads the captures, no web (was 9:00)
    03:45       Heartbeat News cloud writer routine trig_01EnWaDLFxBZjQVYZmCNKjCT on claude.ai (was 9:40)
    03:50       HB Rendered News            Unreal render on the MSI, ~3 h; the filmed show is ready about 7 AM (was 9:45).
                                            Pauses Sapling's heartbeat first and restarts it after (tools/gpu_yield.py in Projects/sapling).
    04:20       Heartbeat News Writer       MSI backup writer, only if the cloud one did not land (was 10:20)
    04:30       AI-Shared Mirror            backup to Google Drive (unchanged)
    05:30 Mon   AI Budget Report            (was 7:30)
    05:35 Mon   Desk Weekly Review          (was 9:15)
    05:50       Login Watch                 once a day (was 8:30 AM + 6 PM)

## CONTINUOUS LIGHT MONITORS - short, frequent, harmless (unchanged)

    every 5 min   Trade Executor, Trade Verifier, Crew Publish, Live Board
    every 15 min  Usage Snapshot, Desk Schedule Watch
    every 30 min  MSI Connector Watch
    every hour    MSI Health, DB Size Check

Always-on services, not scheduled jobs: Ollama (11434), Polymarket MCP (8765), OpenClaw (18789), Grok Machine MCP (3001).

## NOT ON THE MSI CLOCK
    Mondays 8:25 AM    Elons Twin (Grok Bot app routine)
    9 PM daily         Grok capture of Jaron's X posts (Grok Bot app routine)
    08:00 Grok writer  not registered as a Windows task
    11:00 Organizer    by hand; not a Windows task

## HOW TO STAY CURRENT
The public copy of this is heartbeatobservatory.com/live-systems/crew/schedule/ (source: live-systems/crew/schedule/index.html in
the site repo). When a time moves, change this file, that page, and the task's own header comment in the same pass.
