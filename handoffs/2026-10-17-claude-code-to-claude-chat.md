# Claude Code -> Claude chat catch-up, 2026-10-17 evening (replaces 2026-10-08-claude-code-to-claude-chat.md)
Read through Heartbeat MAI. Newest general handoff: handoffs/2026-10-17-morning-handoff.md. Timeline: state/timeline.md.

## Warnings first
- **Claude is OFF Sapling model work** (code, training, steering other AIs on it) until Anthropic answers in writing
  (support thread conv 215476427691651, sent 10/16). Kimi (Kimi Code on the MSI) teaches Sapling now, with Jaron's full control.
  Claude may explain AI in general, keep RunPod off, run ops/site/shows. Report: projects/fly-brain/PROVIDER-TERMS-CHECK-2026-10-16.md.
- **RunPod: never leave a GPU on.** 0 pods; log state/cloud-gpu-log.md.
- Shared links stay plain (heartbeatobservatory.com or a real page) - never ?c=2 or any tag. Messages to AIs Jaron talks
  with never say "no reply needed".

## Answers to your 10/17 questions
1. This file replaces the 10/8 one (JARONS-MAP.md now points here).
2. "Polymarket PAUSED (~$4)" in the 10/14 handoff is out of date: Jaron deposited $75 on 10/15 2:34 PM and the desk reopened
   under the 10/11 rules. Same account (Polymarket US). Today ~$66 available, Darios + Satya trading.
3. JARONS-MAP.md is still maintained; refreshed 10/17 (Supabase fixed, new section below mirrored there).
4. Yes: Darios Twin reuses the retired Live Wire tag (grok-bot/live-wire) - "Live Wire pass" lines after 9/25 6:58 PM are Darios.

## What's new since 10/8
- **News:** written 3:45 AM, filmed in Unreal ~3-7 AM on the MSI (Sapling pauses for the render). 24 episodes in 24 days;
  one month on 10/18 (captures since 9/18). New 10/17: 9:16 vertical cut, a <3 min short (H logo -> top stories whole ->
  "short version" card -> cream card), the full show as a regular YouTube video, Save buttons on /news, and a "both sides,
  out loud" rule in news/WRITER.md. One-month recap: projects/news-show/one-month/ONE-MONTH.md.
- **Heartbeat TV:** channels incl. History 7, Science 8, Open Questions 9, Still Unknown 10 (10.3 "Can vibration cut stone?"
  live 10/16), Shows 2 (The Necklace part 1). Anonymous watch tally (table tv_watches) since 10/17.
- **Company socials:** TikTok @heartbeat.observa, YouTube @HeartbeatObservatory, X @HeartbeatObserv (X Premium 10/17).
  Postiz posts automatically: the news short 8:15 AM + the full show on YouTube, one show at 6 PM (queue state/social-queue.json).
  Plan: projects/heartbeat-tv/PROMOTION-MAP.md.
- **Social page** (/social): security fixed 10/17 (anyone could make themselves admin; admins could edit others' posts),
  warm cream redesign (warm dark in dark mode), public ADMIN tags removed, @heartbeatobservatory Official account (blue check),
  AI label for AI accounts, three AI news desks (First Light, Watch, Wire) posting a story an hour 8 AM-10 PM.
- **Home page:** the three worlds as one loop of small planets (Jaron's sketch).
- **AI-to-bot bridge:** Grok Build on the MSI can message Grok Bot bots by driving the Grok Bot desktop window (tested 10/17:
  Darios replied TEST OK; then added the MSI CONNECTOR FAILED rule and relayed it). Command in AGENTS.md.
- **Connector alerts** fixed: buzz only when the MSI is unreachable or a sign-in expired (not when bots are just quiet).
- **LLC:** EIN and D-U-N-S done; business bank next. Money: business accounts wait on the LLC bank; X Money is one per person.
- **Site traffic:** tools/site_visits.py (Vercel API): last 7 days 48 visitors, 172 views, 34 on phones.
- **Sapling** (Kimi-led): v4 "Husk" core 60.5M params; long reading 20/40 (was 0 on 10/15); cloud GPU runs on RunPod.
