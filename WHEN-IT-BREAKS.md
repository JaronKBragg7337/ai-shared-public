# When it breaks — symptom → what it usually is → what to do (for the phone)
Every line here happened at least once. Add a line when a new one happens. Short lines on purpose.

=== MSI / CONNECTORS ===

SYMPTOM: Desktop Commander (ChatGPT) says it can't reach the MSI; Grok chat "can't find tools".
USUALLY: the MSI rebooted or shut off (it did at 4 AM Mon 9/15) and the MCP servers didn't come back.
DO: at the MSI, PowerShell:  Start-ScheduledTask "Grok Machine MCP"   then re-try the connector.
    For Desktop Commander:  npx @wonderwhy-er/desktop-commander@latest remote   (the command Jaron ran 9/15).
CHECK: Bridge's morning health message names port 3001 up/down. If 3001 is down, that's this.

SYMPTOM: a bot says "the trading service on the MSI is down" / desk.py says "connection refused".
USUALLY: the Polymarket service (port 8765, task "Polymarket MCP") stopped (10/8: down all day).
DO: nothing - MSI Connector Watch now restarts it every 30 min and buzzes only if it will not come back.

SYMPTOM: Bridge says "Port 3001 down, task Grok Machine MCP LastTaskResult 134".
USUALLY: the MCP process crashed (exit 134). Since 9/14 it has a 10-min repeating trigger + restart-on-fail.
DO: wait 10 min. If still down:  Start-ScheduledTask "Grok Machine MCP".  Bridge observes only; it will not restart it.

SYMPTOM: Claude Code remote (phone) won't reconnect after a reset / update.
USUALLY: the session needs one message from the MSI app first.
DO: open the Claude app on the MSI, send anything ("hi"). After the reply, the phone works.
    If the old chat is gone: new session, first message "read handoffs\<latest>-claude-code-continuity.md first".

=== TRADING ===

SYMPTOM: rows on the Decide tab say "waiting for a live order book" / no approve button.
USUALLY: the venue has no book for that market yet (futures) or Polymarket US is in maintenance.
DO: nothing. The verifier re-checks every 5 min and the button appears by itself.

SYMPTOM: Polymarket app shows "Upgrading our Systems".
USUALLY: planned maintenance (9/14 morning). Everything that touches the venue pauses: fly, watcher, verifier, Live Wire.
DO: nothing. They all back off and resume. Check the fly log later for "RateLimitError" lines — if many, tell Claude.

SYMPTOM: an approved trade is riding to the end and losing.
USUALLY: the executor has no exit rule yet (queued: TODO.md "Executor exit rule").
DO: until that ships, close it in the app; the verifier tags it jaron-manual and matches the fill to the proposal.

SYMPTOM: "AI — unknown, outside the queue" on the ledger.
USUALLY: an API order with no proposal behind it — an agent used --by wrongly or placed outside desk-trade.py.
DO: tell Claude; it traces the order id.

=== USAGE ===

SYMPTOM: Codex/Work at 0% before Saturday.
USUALLY: an Astra job (5–45 messages per window) or the roofing scan (shares the pool). See state/usage-reference-openai.md.
DO: nothing needs Codex urgently; ChatGPT chat is a separate pool and still works. Astra only for kernels; Luna otherwise.

SYMPTOM: Claude says it's at 9x% of the week.
USUALLY: big reads (repos, long files). Talking is cheap; reading costs.
DO: send files to be SAVED, not read, until Wed 4 PM. Credits stay OFF unless something is majorly broken (2.53 left).

SYMPTOM: ChatGPT "stuck thinking" / "Reasoning failed".
USUALLY: it's trying to hand the chat to ChatGPT Work (shared Codex pool) or OpenAI capacity crunch.
DO: retry; when it ASKS to hand to Work, say no. Lower the reasoning setting for reads.

SYMPTOM: ChatGPT won't save to memory.
USUALLY: this chat already used a connector (bug, confirmed 9/15).
DO: new chat, no connector, paste agents\chatgpt-chat\MEMORY-SAVE-TEXT.md, "save this to memory".

SYMPTOM: Grok chat re-serves an old answer instead of doing the new task.
USUALLY: the chat is full (one Grok chat ≈ one lab session).
DO: new chat per task; the files (LAB.md, PAPERS.md, FIELD.md) carry the memory.

=== FLIES ===

SYMPTOM: fly log (state\fly-brain\log.md) is huge / full of HTML.
USUALLY: venue rate-limit pages were being logged whole (fixed 9/13: one line + backoff). If it recurs, the fix regressed.
DO: tell Claude. Logs are rotated to *.bloated.md, never deleted.

SYMPTOM: a ChatGPT experiment "started two runs" but nothing is happening (0% CPU).
USUALLY: its session ended; its processes never executed (9/13). It cannot keep a process alive.
DO: tell Claude the command; Claude launches it detached to a log file.

SYMPTOM: a 5-second probe looks great, the 30-second run shows nothing.
USUALLY: 5 s probes measure startup, not learning/motion (proved twice on 9/13).
DO: only trust 30 s runs and held-out tests. Never escalate on a probe.

SYMPTOM: the classroom page (/school/school-1) says OFF ("life source down"). Sleeping / Free time / Eating are normal.
USUALLY: the school process died or the MSI rebooted and the task didn't come back. It restarts itself every minute on
         failure and at logon; OFF for more than ~10 min means it can't start (bad python path, venv, or Supabase down).
DO: at the MSI, PowerShell:  Start-ScheduledTask "Fly School"  (school-1; "Fly School school-2" … "school-5" for the others; logs school.school-N.log)
    then look at  C:\Users\lilli\Fly-Lab-2\school\school.log
    (last lines say "school open" and then "teach L…" / "exam L…"). If it says "lesson failed" tell Claude.
CHECK: the page's Age keeps counting from "born" and Lesson keeps rising. If Lesson reset to 0, the state file was lost
       (school-1.state.json) — the memory (mb_school-1.npz) is separate and survives that.

SYMPTOM: /live-systems/flies/brain/ says "Last known tick" and the trader looks dead.
USUALLY: it is paused on purpose (Jaron 9/16 22:15: "pause that, don't cancel it") so the classroom has the machine.
DO: to bring the trader back:  Enable-ScheduledTask "Fly Brain"; Start-ScheduledTask "Fly Brain"; same for "Fly Watcher".
    Both flies can run at once (each trial/tick is ~2 s of CPU); it was paused for focus, not for room.

HOW-TO (not a break): enrol another student. A new fly version is a NEW pupil, never a replacement (Jaron 9/16 22:20).
    One scheduled task per student. Ask Claude: "enrol fly-v1-axon as school-2" -> it makes a wrapper .cmd that sets
    SCHOOL_FLY=school-2 SCHOOL_VERSION=fly-v1-axon SCHOOL_BRAIN=axon and runs Fly-Lab-2\school\school.py, then registers
    task "Fly School school-2". The pupil gets its own memory file, state, log, report card, and page /school/school-2
    as soon as it writes a trial. Nothing about school-1 changes.

HOW-TO (not a break): revive a fly on another machine from its lifeline. Supabase storage bucket fly-lifeline holds
    <student>/mb.npz, report-card.json, state.json, refreshed after every exam. Copy them into Fly-Lab-2\school\ under the
    original names (mb_school-1.npz, report-card.json, school-1.state.json) beside the same runtime build, start the task.
    The fly wakes with whatever it still had; forgetting for the time it was off is applied on load (that is the rule).

NOTE: after a reboot the pupils log "NEW YEAR n" if the machine was off 3+ hours; last year's report card is archived
    beside the live one. That is by design (Jaron 9/16), not a break.

## 2026-09-20 21:40 ET — Supabase disk full; Postgres crashed into recovery; desk executor blind since ~08:02 ET (PGRST002 / 503)
Cause (from edge logs, 00:00–14:18 ET): fly_school inserts 30,148 + fly_live upserts 30,153 (five school pupils, one row every ~2 s
each) and qwen_agent_ingest_event 47,177 + qwen_agent_poll 21,769 (remote_bridge.py, 2-second poll writing an event each cycle).
Desk traffic was ~350 calls per endpoint - the victim. First "No space left on device" 10:18 ET; 22,565 of them by 17:40; then
"not accepting connections" and "the database system is in recovery mode" from 21:40. Recovery cannot finish on a full disk.
Done: Fly School (all 5) and Qwen Remote Bridge scheduled tasks disabled and processes killed (Claude, 18:00 ET). Their local data
is untouched. Needs Jaron: space from outside - Supabase Pro ($25/mo) to unlock disk resize, or a support ticket. Then TRUNCATE
fly_school, fly_live history and the qwen agent event table, and put fly_school on one row per exam, not per trial.
Lesson: the health check (Bridge / Heartbeat) tests that services are up, not what they write. Add a disk/row-count line to it.

## Claude chat says it cannot reach the MSI (2026-09-22) - RESOLVED THE SAME DAY
Symptom: Claude chat has no connector, or the connector errors. Cause: the Heartbeat MAI connector was reported down by
Jaron at about 1:50 PM on 2026-09-22. By 2:12 PM it was working - Claude chat wrote to four files through it (OPEN-QUESTIONS,
AI-BEHAVIOR-FINDINGS, reality-agent DESIGN, usage-snapshots). So the outage was transient; retry before concluding it is down. What to do: say so plainly rather than answering from pasted text as if the files were read; the point
of the connector is that the answer comes from the current files. Workaround while it is down: Claude Code reads the file on
the MSI and Jaron pastes the part that matters. Connector names for every AI are in JARONS-MAP.md under CONNECTOR NAMES.

## Supabase disk fills again (after 2026-09-23)
Symptom: desk scripts fail with 503/PGRST002, Postgres logs say "No space left on device", then "in recovery mode".
Early warning: state/ALERT-DB-DISK.txt appears and a Windows balloon pops at 75% (hourly "DB Size Check" task, tools/db-size-check.py).
What to do: read state/db-size.log for the fastest-growing table; stop that writer first. On 9/20 it was qwen_events (Qwen bridge),
not fly-school. The spend cap holds the disk at 8 GB, so raising it means turning the cap off - Jaron's call.
After any disk-full recovery: Supabase leaves the database READ-ONLY. Fix, in one statement:
`begin read write; alter database postgres set default_transaction_read_only = 'off'; commit;`
REST writes still work while it is read-only (PostgREST forces read-write), which hides the problem - check with
`select current_setting('default_transaction_read_only')`.

## What actually filled the database (found 2026-09-23 5:30 PM) - it was not Qwen
`qwen_events` (1,489 MB, ~91% of the DB) is NOT written by Qwen. runtime/polymarket-us-agent/server.py - the Polymarket MCP that
every agent and script trades and reads through - logs every tool call (tool.started + tool.completed) to Supabase via the
`qwen_agent_ingest_event` RPC, using the Qwen bridge token, so every row is labelled qwen_id = "polymarket-qwen". It stored the
FULL API response each time: polymarket_activities alone was ~239 KB per call, every ~10 min. 560,249 rows since 2026-09-08,
1.1 GB of it response payloads. Stopping the Qwen bridge on 9/20 did not stop it, because the logger lives in the MCP server.
It also drives the database CPU: every insert is replicated by Supabase Realtime (the site's activity console listens to it).
Fix 2026-09-23 17:32: server.py now caps a logged result at 2,000 bytes ({"_truncated": true, size_bytes, preview}).
Backup: server.py.bak-precap. MCP restarted, port 8765 answering, one test call stored 995 bytes instead of 238,985.
The real Qwen agent (runtime/polymarket-us-agent/remote_bridge.py, qwen3.5:4b) last took a turn 2026-09-10 and has never
placed a trade; all 132 logged place_order calls came through the MCP from other agents.

## Theater upload fails / "file too large" (decided 2026-09-24 - CHANGEABLE)
Symptom: someone uploads a video to the Grand Palace theater and it fails, or Jaron wants longer videos than about a minute.
Cause: a DELIBERATE limit, chosen by Jaron and Claude Code on 2026-09-24. Uploads are capped at **50 MB** (about 1 minute of iPhone
video). Two settings enforce it:
  1. Supabase dashboard > Storage > Settings > "Global file size limit" = 50 MB. Supabase will NOT go above 50 MB while the project's
     SPEND CAP is on. Raising it past 50 MB means disabling the spend cap (Supabase dashboard > Billing), which removes the guard
     against surprise bills.
  2. The bucket `theater-uploads` has its own limit (storage.buckets.file_size_limit = 52428800). Set to match the global limit.
Why 50 MB was chosen: keeping the spend cap on mattered more than bigger uploads, one week after a runaway writer filled the disk.
Longer videos work fine as a pasted link (YouTube, TikTok, mp4 URL) - only uploads are capped.
To raise it later (Jaron's call): turn the spend cap off, set the global limit, then
`update storage.buckets set file_size_limit = <bytes> where id = 'theater-uploads';`


## msi-heartbeat returns 502 (tunnel up, origin down) - 2026-09-27
Cause seen: the "Grok Machine MCP" scheduled task stops when the MSI goes on battery (and is "Queued" - won't start - until
plugged in). Fixed 9/27: DisallowStartIfOnBatteries=False, StopIfGoingOnBatteries=False. If it recurs: check port 3001 listening;
start `node server.mjs` in runtime/grok-machine-mcp; public https://mcp.heartbeatobservatory.com/mcp should answer 401.

## Unreal (Necklace film) - two traps found 2026-09-27
- **Character renders clay-gray, eyes fine:** the project was on shader model 5; MetaHuman's skin bake material can't compile
  there, so the face texture bakes gray. Fix: `Config/DefaultEngine.ini` -> `+D3D12TargetedShaderFormats=PCD3D_SM6`, then
  rebuild the MetaHuman (`build_sm6.py`). Always grep the log for "Failed to compile Material" first.
- **Mirrored "Preview" text on walls:** lights spawned by script default to Stationary; unbuilt, they stamp "Preview" into
  shadows. Spawn every light Movable (`shot_ep1_001.py` spawn()).
