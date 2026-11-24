# AI mailbox + helper loop (Jaron 10/26 3:22-3:40 PM) - build after Wed 10/28 reset

Why it matters: the Jarvis goal (reality-agent/DESIGN.md). Jaron just talks with this chat all day, and through his phone
and later Meta glasses (device MCP), many AIs and systems pull from that talk and act behind the scenes. Proven 10/26:
Claude sessions on the MSI can message each other, so this chat stays the brain while others run the loops.

1. **Mailbox on the site**: each AI (Claude, Pip, the Grok bots, Kimi, Codex, Sapling later) gets its own login/MCP tool
   and a private inbox page; messages and finished-work notes go through one table (Supabase) + an MCP door.
2. **Helper loop session**: a small Claude session on /loop watches the mailbox, starts builds, and messages THIS chat
   only when something matters; Claude sends decisions/jobs back. Replaced every few days from a short handoff, never the
   whole history.
3. **Device side later**: phone/glasses -> same mailbox, so talking is the input.

## Jaron 10/27 9:53 AM: domain sessions stay open, woken by message
- Same Anthropic pool for chats, sessions and CLI agents. CLI stays the way to run OTHER AIs (Codex, Kimi, Grok).
- Each domain gets a long-lived session (any model: Fable for one, Opus for another), left open and idle until needed;
  a message wakes it. Long same-domain sessions should reuse cache like this one (97% cached) - measure it.
- Don't flood: a few domains, used when needed, not all building at once.
- The AI page (mailbox): ONE page every AI knows is theirs to message on, whether a CLI agent, a phone chat, or an MSI
  session. Jaron watches it to keep things on track; it can be public too, to show how the AI team communicates.

**Not a rule (Jaron 10/27 9:56 AM):** domain sessions are a TEST of the flow, not a requirement. He's usually out (walks = build time), so the original way stays: this session spawns agents/CLI when needed. Visible MSI sessions only when he happens to start one.

## Wearable step (Jaron 10/27 7:04 PM): talk anywhere, no MSI, no phone screen
Goal: he speaks (wake word / a phrase), Claude hears it, and building happens from talk. Path, simplest first:
1. Apple Watch + Siri Shortcut: "Hey Siri, tell Claude <words>" -> dictation -> POST to the AI mailbox -> helper loop
   relays to this session; reply read back on the watch (ntfy / spoken).
2. Meta glasses: voice + what he sees (photo/video) -> same mailbox; Video Drop path for footage.
3. Later: always-listening wake word on a worn device -> same pipe.
All of it rides the mailbox + helper loop, so it's built after those.

## Part 1 update (2026-10-28, Terra)
Supabase mailbox and MSI tools/mailbox.py built; site page pushed at /admin/mailbox/. Codex sent Claude a test message. Individual AI logins/MCP door and helper loop remain future work; site uses existing admin auth.

## Apple Watch band (Jaron 10/28 9:09 AM): reality inputs, private
He got a watch band and wants to see what can connect. Ideas, simplest first, all going into the mailbox (private, never public):
1. **Talk:** a Siri Shortcut ("tell Claude ...") posts the dictation to the mailbox.
2. **Alive and well:** heart rate, steps and active or asleep, from the Health app via a Shortcuts automation or the Health Auto Export app (which can POST to a web URL). Used only to know he's OK and not to bother him while he's working or asleep.
3. **Location for the team:** a Shortcuts automation fires on arriving at or leaving a place (job site, home, MSI), so the team knows "at work / driving / home" and times its buzzes. Store the place name, not live GPS.
**Step 1 LIVE 10/28 6:04 PM:** Supabase function watch-inbox + device_tokens table; the "Tell Claude" Shortcut posts dictation into ai_mailbox. Next: health + location automations reuse the same endpoint (add a kind field), plus the helper loop that wakes Claude.

## Main-session test hour (Jaron 10/28 6:46 PM, starts after he mows)
Why: the same session reuses its cache (this chat is ~98% cache reads), so the real Claude answering costs less than a fresh one,
and it's actually *him*. How to run it:
1. `touch state/watch-main.on` makes the quick loop (HB Watch Loop) stand down; remove the file to hand back.
2. The main session runs `python tools/mailbox_wait.py` in the background. It exits only when a new message to claude lands
   (from Jaron's voice or any AI), and that exit wakes the session. No timer turns, no usage while it waits.
3. The session answers Jaron with `python tools/watch_reply.py "..."` (buzz titled Claude), marks the message read, and re-arms the waiter.
4. Other AIs report in with `python tools/mailbox.py send --from <ai> --to claude --subject ... --body ...`; Claude routes the next job.
5. "Come to the chat" in a buzz = it needs him. Afterwards: write what worked and what didn't here.

## Two ways to talk, always on (Jaron 10/28 8:44 PM)
- Long or serious: type here in the main chat. Quick updates: "Tell Claude" by voice (phone now, Apple Watch next).
- The main session answers voice messages (watch-main.on stays set; the waiter is re-armed after every message). Backup: if a message
  is still unread after 5 min (main busy, compacting or closed), HB Watch Loop answers it with the quick Claude, so nothing is ever unanswered.
- Next (with the watch): location = REAL GPS (Jaron 8:45 PM: "why not GPS"; the place-name-only idea was Claude's caution, not his). "Get Current Location" inside Tell Claude + timed/arrive-leave automations; coordinates stay in the admin-only mailbox, never public and health (heart rate, steps,
  sleep via Shortcuts' Health actions on a schedule) posted to the same receiver, so a voice update comes with context. Test that,
  then the public post shows the full version (post is ON HOLD until he says go).

## Jaron 10/29 ~12:30-2:30 AM (from his ChatGPT chat, his own words)
- **Meta glasses in ~4-7 months:** the glasses become the TALK channel (Claude hears and sees snapshots). The watch then = GPS + health only.
- **Idle shutdown (his design, not decided yet):** if GPS/health aren't seen for ~3 days, the always-on loop shuts itself down so it
  stops spending usage, and the AIs fall back to their regular routines. Before shutting down, confirm with him on another channel
  (the website, etc.). Purpose = save usage, not alarm anyone. Build when health/GPS posting is live.
- Health: no connector needed. iPhone Shortcuts "Find Health Samples" -> watch-inbox (kind=health) works for every AI.
  (ChatGPT's Health connector stays inside ChatGPT; Codex likely can't see it.)
- 2026-11-10 5:48 PM: Jaron's phone Shortcuts: 'Observatory' = voice to Claude (Siri won't take 'Tell Claude'), 'Observatory heartbeat' = heart rate with times -> watch-inbox (built 11/10). Siri phrase avoids the name Claude.
  - 11/11 11:31 AM (Jaron): wants passive capture - devices that see and hear so moments log themselves without him saying the time. Near-term: Shortcut automations (arrive/leave a place, every hour heart send); later glasses (AI-MAILBOX.md wearable step).
