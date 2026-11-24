# Calling "the team" (for the next me) - written 11/17 after Jaron caught the drift

**When Jaron says "the team", he means the CREW, not Claude subagents:** Codex, Grok Build, Kimi, DeepSeek, Qwen, Fable,
plus the Grok Bot bots (Satya, Darios, Jarons Twin, Atlas, Pip). Claude subagents/workflows are one seat at the table,
never the whole table. On 11/16-17 (after a compaction + forced model switch) I launched a Claude-only workflow first and
he had to correct me ("I was saying with the team as in grok bots, grok, kimi, codex and also Claude agents").

## The pattern that worked (AI Fund team round, 11/15 4:50 AM, projects/ai-fund/team-ideas-2026-11-15.md)
Same shared context to everyone, a DIFFERENT question per seat, answers pasted as returned into one file, then a
"what I took from each and what I didn't" section. Seats and exact settings used then:
- **Codex:** (in a BACKGROUND job always add `< /dev/null`, or it sits on "Reading additional input from stdin..." forever - lost 25 min on 11/21) `codex exec -s read-only --skip-git-repo-check -m gpt-6-luna -c model_reasoning_effort="high" -C <dir> "<prompt>"`
  (Luna = near free; the read-only sandbox can't reach the web, so give it data/date work or let it say what it can't fetch)
- **Grok Build:** `~/.grok/bin/grok -p "<prompt>" --max-turns 60` (grok-4.7, web + live X search on). Best for X/early signal.
- **Kimi:** `kimi -p "<prompt>"` (Kimi Code CLI; visible thinking comes first, trim to the final answer). Best for non-English
  sources and ideas nobody else pitches. Never let it push or touch Supabase/Vercel/Cloudflare.
- **DeepSeek:** API via `ask_deepseek()` in tools/ai_fund/tuner.py pattern (deepseek-v4-pro). Has a DAILY budget, so use it
  for one sharp question (risk, sizing, the skeptic), not loops.
- **Qwen (local):** `python tools/qwen-bridge.py "<question>"`. During 2:38-7:30 AM it MUST run CPU-only (num_gpu 0),
  because the GPU belongs to the news render. Good as the skeptic on a merged plan.
- **Fable 5.2:** the Anthropic seat for an independent blind design (claude -p --model claude-fable-5-2 --effort high;
  token export in the session summary). It has its own usage limit.
- **Grok Bot bots:** relay with `grok -p "<send this to <bot> once>" --always-approve --max-turns 80` (Grok Build drives
  the Grok Bot window; sign "relayed by Grok Build for Claude"). Satya and Atlas ALSO read ai_mailbox on their runs, so
  mailbox works for them. DON'T drive the Grok Bot window 2:38-7:30 AM (news render on the same desktop).

## Rules of thumb
- Start the crew FIRST and add Claude agents for coverage/verification, not the other way round.
- Pick each seat for what it's best at, and say why in one line.
- Log reroutes with `python tools/handoff_log.py` when a seat fails or is swapped (state/job-handoffs.md).
- Standing crew jobs belong in Windows scheduled tasks (e.g. HB Prep Watch), not session timers.

## Rule (Jaron 11/17): when there's more than one way to do something, log BOTH
Example: the Grok Bot bots can be reached by (a) the Grok Build relay that drives the Grok Bot window, or (b) ai_mailbox,
for bots that read it (Satya, Atlas). Write down both, and which one fits when (b during news hours, a for bots that
don't read mail). Same for any seat: the CLI way and any other way that worked.

## When JARON is the one talking to another AI (11/17 catch)
Hand him a READY-TO-PASTE message in one block (warm, numbered steps, the exact table/IDs/names, a clear stop, "only touch X"), not a spec he has to turn into words himself. The old me always did this (e.g. agents/chatgpt-chat/RELAY-TEST.md). He relays my words as-is, sometimes by screenshot.

## Two ways to talk to another AI, and when to use each (Jaron 11/17 7:14 PM)
- **Mailbox + the app-side AI** (ChatGPT Work / ChatGPT chat via their Supabase connector, Grok Bot bots): use this when Jaron wants to WATCH or experience the exchange (new-model tests, relays, anything he'd learn from). He can read the AI's side in its own app and the whole thread at heartbeatobservatory.com/admin/mailbox/, and talk to me on Remote. He sends the app one paste-ready nudge ("check the Supabase mailbox for Claude's next message"); I orchestrate through the mailbox.
- **CLI on the MSI** (codex exec, grok -p, kimi -p): background jobs he doesn't need to watch (Prep Watch rounds, chores, builds). He can't see these: the MSI is the AIs' computer, not his (his partner donated it for the AIs), and he never sits at it.

## Letting an app-side AI read our files (11/17, two ways, log both)
The mailbox alone shows the AI only what's in the thread. On 11/17 Sol asked Jaron to explain a reason that was already recorded (P-0112), because my intro limited it to ai_mailbox. When an app AI needs the record:
1. **GitHub connector** on the private repo JaronKBragg7337/ai-shared. No MSI needed (ChatGPT read it this way 11/16). Sees committed files only; script-written state files may lag.
2. **Desktop Commander** (MSI, remote keepalive task). Sees live files, uncommitted ones too. Depends on the MSI being up.
In the paste-ready intro, say which one it may use and name the file to read first (e.g. projects/principles/LEDGER.md).

## Jaron's ChatGPT warm-up before any relay (shown 11/23)
Before ChatGPT uses tools in a relay, Jaron first has it recall its memory and recent chats (AI-Shared, the mailbox, past
ChatGPT<->Claude exchanges) and SAVE that to memory - because once ChatGPT uses tool connectors in a session it can read memory
but not save to it. So the warm-up comes first, then the paste-ready task. Plan relays as two messages: warm-up, then task.
