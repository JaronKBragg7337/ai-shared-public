# Handoff 2026-11-16 evening (Claude Code, main session, Opus 5.5)

## Done today
- **Leaked keys (his mom's old Notes, from 4/23):** Claude key `daily-log` was LIVE, an orphan (not in keys.env/repos/env), deleted by Jaron, rechecked = HTTP 401 dead. The Kraken key in the note was an old one, already gone (doesn't match kraken.env). The GCP note isn't a credential. The forced model switch 5.5 -> 4.8 -> back to 5.5 (safety flag on the key words).
- **ChatGPT talks (word for word):** projects/strategy/chatgpt-2026-11-16.md + -part2.md + screenshots. Kit decisions in projects/strategy/SYSTEM-FOR-OTHERS.md (ONE company across many fields; free setup = current lean; their caution = their settings; Polymarket isn't in the kit; company rules ALWAYS need the owner's yes; the conductor explains in each person's own way; the kit repo in 5 stages + gaps; cloud-only is for OTHERS, ours stays on the MSI).
- **Relay tests:** 4 rounds (MSI + direct Supabase); a ChatGPT mid-task message worked; cloud-only pilot PASSED (cloud-claude, network set to Full by Jaron); a 12-round single-turn stress test (record; old was 8). Logs: research/relay-test-2026-11-16/ (MAILBOX-LOG, CLOUD-PILOT-LOG, STRESS-12-LOG). Pilot pass + functions dropped.
- **Kit inventory:** projects/strategy/KIT-INVENTORY-2026-11-16.md (~90 pieces, AI-team/machine/usage maps, gaps).
- **Fixes:** disabled the 'Trade Executor' task (live Polymarket order placer, against P-0112; kept, not deleted). Desktop Commander now restarts itself (tools/dc_remote_keepalive.ps1, task at logon + every 10 min, tested). AGENTS.md roofer line fixed.
- **Plans:** projects/strategy/PHONE-ONLY-GAME-TEST.md (ChatGPT conducts a cloud Claude -> Grok/Kimi building a game; tests phone interruptions). research/how-ideas-form/LOG.md started.
- News read written: measles is rising in Allen County (17, could hit 250-300); told Jaron to ask the OB about immunity before the baby arrives.

## Open
- Tell ChatGPT on the next relay: the Desktop Commander fix.
- The long vertical + YouTube cuts of 11/16 news failed (main show fine). Not looked at yet.
- Stale: state/routing.json (missing Kimi/Fable/DeepSeek/Perplexity), the budget bill list, INDEX.json (10/21). "Desk Weekly Review" task failed. HB Watch Loop exits 0x1 but the watch mail works.
- Still running: Polymarket MCP + Crypto Consensus (paper) + Live Board. Left alone; the executor is off.
- ChatGPT memory test (real preferences, fresh chats, days). Parked: analogies from both AIs for "corrections narrow".
- From earlier: safety scale v4 questions (his 3), Satya's overnight gap, money gaps, why two writers ran the 11/15 news, the /admin/fund/ check.
- Private: his partner is 36 almost 37 weeks (37 on Wed 11/18), estimate 5 lb 13 oz. Trailer job Wed 11/18.
- An autostash (stash@{0}) is still in the list; its files were restored, so it's safe to drop.

## Waiters
mailbox_wait (re-arm after each exit, mark done first); Seam listener bxvffytcy (6h timeout, restart on exit 2).
