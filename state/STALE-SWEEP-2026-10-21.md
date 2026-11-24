# Stale-notes sweep - 2026-10-21 (Claude Code, Sonnet 5.5)

Why: on 10/21 a new bot reported "Postiz bill missing" and "Anthropic key broken" from stale lines (both already fixed).
Method: read state/timeline.md (lines ~524-823, 10/9 to 10/21), then checked each file below against it and against live state
(Windows scheduled tasks, state/logins.md, state/MSI-STATUS.md, state/subscriptions.json). Present-tense claims were corrected in
place; history sections were kept. Nothing was answered for Jaron. Repeat weekly: `tools/stale_sweep.py` -> `state/STALE-CANDIDATES.md`
(task "Stale Sweep", Sunday 5 AM).

Timeline lines are cited by their date/time stamp.

## Changes (file: old -> new | proof)

### AGENTS.md (still one page, 84 lines)
1. Current focus: "Finish a few more TV shows (Keeper's Light ep 2-3, Necklace film ep 1)" -> "TV channels + shows out (Jaron 10/17); Keeper's Light and Necklace ep 1 done; games paused ~1 week from 10/17". Proof: 9/29 05:55 (Keeper's Light ep.3 live), 10/12 04:30 (Necklace Ep.1 Part 1 live), 10/17 20:55 (no Cosmos work now; focus = all TV channels).
2. Grok Bot bot list "Darios, Satya, Demis..." -> "Darios, Satya; Demis is off; Jarons Twin new 10/21". Proof: 10/21 09:50 (Demis off), 10/21 09:25 (Jarons Twin).
3. Added "Heavy scheduled work runs 3-6 AM only" to the news-deadline bullet. Proof: 10/15 1:05 PM.

### state/open-list.md
4. #2 "Twins on at 5 PM ... flip Darios + Satya ON" -> DONE 10/15; traders every day noon-1 AM since 10/21. Proof: 10/15 5:44 PM, 10/21 09:50.
5. #7 "New bot routines (optional)" -> DONE (Darios :22 / Satya :52 routines). Proof: 10/15 3:01 PM, 10/15 5:44 PM.
6. #13 TV channels "CH9 + CH10 go on the guide when first episodes done" -> channel list live by 10/21 (7, 8, 9, 10, 11, 13, 17, 19, 22). Proof: 10/12 00:15, 10/17 21:41/21:50/22:00, 10/20 07:55, 10/18 15:25.
7. #16 socials tail "then Postiz so AI posts ... Claude walks each" -> Postiz done; trial ends 10/24 then $29/mo, Jaron knows. Proof: 10/17 09:46, 10/20 07:40 (runbook), runbook "Jaron knew (10/20)".
8. #17 "His own AI (parked) ... First step: train a tiny language model" -> Sapling exists since 10/14 (now v4 Husk), Claude paused on it pending Anthropic's answer. Proof: 10/14 05:35, 10/16 12:33 AM, 10/16 10:46 AM, 10/17 8:50 AM.
9. #18 "Sapling control room + phone chat (after 4 PM reset 10/14)" -> DONE 10/14. Proof: 10/14 15:20.
10. #19 "Phobos post (Oct 19-20)" -> date PASSED; Codex Phobos job stopped 10/17 when Cosmos work paused; asks Jaron if he still wants it. Proof: 10/17 20:55.
11. "Cloud GPU brief ready" -> DONE 10/16 (RunPod via API key, first cloud lesson). Proof: 10/16 12:02 AM, 10/16 2:35 AM.
12. "Sapling budget accounting fix (after the v4 build finishes)" -> noted v4 finished 10/16; fix not logged as done (left open). Proof: 10/16 12:33 AM.

### RECONNECT.md
13. Section 5 "A new key": desktop-icon/clipboard flow -> Key Drop on the phone (heartbeatobservatory.com/admin/keys/) first, old way kept. Proof: 10/19 18:40, 10/19 19:20.
14. Section 10 Postiz: "first setup" -> marked DONE 10/17, trial ends 10/24 then $29/mo. Proof: 10/17 09:46.
15. "How you find out" table: added Polymarket/Kraken keys and Postiz channels rows. Proof: 10/19 19:11, 10/17 09:46.

### WHEN-IT-BREAKS.md
16. Trading entries about the Decide tab / "executor has no exit rule yet": marked history, retired queue (traders close with desk-trade.py --exit). Proof: OPEN-QUESTIONS Q-023 (9/24); Trade Executor task still Ready (exits only).
17. FLIES header: added that Fly School (all 5), Fly Brain, Fly Watcher and Qwen Remote Bridge tasks are DISABLED on purpose. Proof: live task list 10/21 (all Disabled); Q-021 / 9/20 entry.
18. 9/20 Supabase disk-full entry: "Needs Jaron: Supabase Pro" -> RESOLVED 9/23 (Pro, disk 8 GB). Proof: OPEN-QUESTIONS Q-021 resulting action.
19. New sections: "connector says sign-in expired (fixed 10/21)" and "News not live by 8 AM / daily post missing". Proof: 10/21 08:10, 10/21 09:20, 10/18 11:40, 10/18 11:50, 10/20 08:50, 10/21 06:05.

### projects/runs-without-jaron/RUNBOOK.md and README.md
20. RUNBOOK Grok row "PREPAID ~3 months" -> PAID 10/20 (Apple order $43.87 charged to X Money card; safe to Jan 10). Proof: 10/20 09:00.
21. RUNBOOK "WARNING 10/20 8:38 ... FAILED ... Grok at risk" -> RESOLVED 10/20 09:00; "UPDATE 8:44 pays from paycheck" -> what really happened (10/20 08:47 $35 Polymarket -> X card, 09:00 Apple charged to X card). Proof: 10/20 08:46, 08:47, 09:00.
22. RUNBOOK Kimi row "X Money card" -> APPLE (renews 11/2), to move to web. Proof: RUNBOOK's own 10/20 8:33 Apple screen line; 10/9 18:49.
23. RUNBOOK watch list: added MSI Status task; "Check: personal X Premium still active?" -> confirmed renews 2026-11-10 (same page). Proof: 10/21 15:20.
24. README "To build (next session)" 1-5 -> built (RUNBOOK 10/20; his partner-GUIDE.md exists); "check what Polymarket API allows" -> answered: retail keys cannot withdraw. Proof: 10/20 07:40, 10/19 18:45, 18:50.

### state/models.md
25. Fable "ASK JARON FIRST" -> "own Max limit; Claude picks any available AI without asking (10/2)". Proof: memory note "Fable + orchestrator calls" (Jaron 10/2); not a timeline line.
26. Kimi "No CLI found on the MSI yet" -> Kimi Code CLI installed 10/9, runs First Light and teaches Sapling. Proof: 10/9 19:56, 10/9 23:40.
27. "Grok Bot bots (Darios Twin = primary, Elons Twin; Sams Twin inactive)" -> current roster/schedule. Proof: 10/15 3:01 PM, 10/21 09:50, 10/18 21:45, 10/15 9:54 PM, 10/21 09:25.
28. DeepSeek "Trading through DeepSeek is paused" -> "paused 10/1, not re-checked" plus news reader role. Proof: 10/15 timeline (DeepSeek reader 3:40).

### OPERATING-MAP.md
29. Added a dated STATUS NOTE above the TOS matrix: any AI may trade if its own provider allows (Claude/Codex long/medium with approval, 10/7), approve queue retired 9/24, Qwen dropped 9/30, itch/Gumroad dropped 10/11, bounty scanner disabled, funding lane. Proof: AGENTS.md, Q-018, Q-023, 10/11 13:11, live task list. The Sept matrix and "Hard rule" text were left as history.
30. "PayPal / Stripe: not set up yet" -> added 10/11 reason (waiting for replacement ID; tips via X Money + wallets). Proof: 10/11 23:35.

### JARONS-MAP.md
31. "AI-SHARED ... local workspace, not a public repo" -> private GitHub repo + cleaned public copy. Proof: 10/21 12:10, 15:12.
32. "Bills ($95/mo, Supabase Pro bought 9/23)" -> ~$258/mo with the list. Proof: 10/19 07:12, 10/20 07:40 (runbook).
33. GROK BOT line, GROK BUILD line ("out of allowance 9/22") and KIMI line ("Fourth writer candidate, not wired") -> current. Proof: 10/21 09:50, 10/17 (Grok Build used), 10/9 23:40 (First Light live), 10/18 12:30.
34. THE DAY: added a 10/21 schedule block (3-6 AM pipeline); "Claude writer paused as of 9/22" -> running (all 5 captures 10/16). Proof: 10/15 1:05 PM, 10/16 7:12 AM, 10/18 12:30.
35. "My ID - lost" -> court mail arrived 10/13, replacement not yet logged. Proof: 10/13 22:41.
36. WAITING ON ME: Q-004 -> DONE 10/21; Q-021 -> DONE 9/23. Proof: 10/21 12:10; OPEN-QUESTIONS Q-021.
37. "LLC: EIN + D-U-N-S done" -> EIN 10/14; D-U-N-S requested 10/14, arrival not logged. Proof: 10/14 10:38, 16:27.

### working-with-jaron.md
38. "Nothing outward - send, post, spend, submit, accept terms, trade - fires without Jaron's explicit yes" -> marked SUPERSEDED, points to AGENTS.md "Act on your own" (9/23, 9/26, 10/8). Proof: AGENTS.md hard rules; memory notes.
39. Credits "13.6 credits sit behind it" -> "sat on 9/13, amount not re-checked".
40. Fly section: added status note (tasks disabled since 9/20-9/21; Sapling is the own-AI work now).

### INDEX.json (still valid JSON)
41. Header updated date/by. 42. hard_rules "Nothing outward ... without explicit yes" -> SUPERSEDED with current rule. 43. hard_rules trading line: added 10/21 update (Claude/Codex long/medium with approval, any AI per own provider). 44. ai-shared-not-a-repo: DEFERRED -> DONE 10/21 (private + public copy). 45. heartbeat-tv status: "Permanent uploads wait for Jaron's review" -> only OTHER users' uploads wait; AI-made go live; channel list. 46. necklace-film status "IN PROGRESS ... Ep1 shot 001" -> Ep1 Part 1 live 10/12. 47. qwen status "ACTIVE participant" -> dropped from active use 9/30, bridge task disabled. 48. vercel THE_LANDMINE "DO NOT PUSH TO MAIN" -> RESOLVED 9/10. 49. unattended_caveat "AutoAdminLogon OFF" -> superseded (ON since 9/11). 50. payment-rail-undecided: added 10/11 note. 51. FIRST_REAL_TRADE "executor was run by hand" -> fixed later. 52. FLY_BRAIN_1 task -> disabled since pause.
   Proof: timeline 10/21 12:10/15:12, 10/12 04:30, 9/29 05:55, 10/11 23:35; AGENTS.md; live task list; models.md; REBOOT_SURVIVAL entry in the same file.

### decisions/OPEN-QUESTIONS.md
53. Q-004: added Status "DONE 2026-10-21" quoting timeline 10/21 12:10 and 15:12 (marked by action; Jaron's exact words are not in the timeline; the old DEFERRED answer is kept).
54. Q-006: added the 10/11 and 10/13 timeline lines; stays OPEN (no rail chosen).
55. Q-012: leftover "Answer: -" fixed to quote his answer (status already said ANSWERED); Q-021: added "Status: DONE 2026-09-23" (it sat under OPEN with the action already recorded); first Q-024 "OPEN" -> SUPERSEDED by the answered second Q-024.
56. Q-018: added the AGENTS.md 10/7 line (Claude and Codex long/medium trading with approval) under the 9/12 "never trade" text.

Total: 56 numbered changes across 12 files (about 45 distinct lines/blocks), plus the new tool and task.

## Left unchanged - unsure, needs a look
- **open-list #1 D-U-N-S**: requested 10/14, "~5 business days" has passed; no timeline line says it arrived or didn't.
- **JARONS-MAP "USAGE RESETS"**: [checked 10/21: Codex Oct 22 one used 10/1; Codex has Oct 29 + Nov 6] says Claude and Codex banked resets "expire Oct 22" (tomorrow). Not known if used. Also "Claude emergency credits OFF"; WHEN-IT-BREAKS says "2.53 left", working-with-jaron said 13.6 on 9/13 - the real number is in the app.
- **JARONS-MAP "MONEY OUT THE DOOR"** (GOAT submitted 9/21 "waiting", Autonomys, 0G): no outcome in the timeline range I read; check watch/offers/agent-funding/PROSPECTS.md.
- **JARONS-MAP "Organizer - no brief newer than 9/18"** and "Grok 08:00 writer": not rechecked since 10/17.
- **Trade Proposer** task is Disabled in Windows but OPEN-QUESTIONS Q-023 says "Proposer and verifier back on" (9/24 3:10 PM). Trade Verifier and Executor are Ready. I did not change either text; someone who knows should say which is true now.
- **Theater upload limit 50 MB** (JARONS-MAP, WHEN-IT-BREAKS): Supabase is Pro now; open-list still says "raise Storage limit to 1 GB (dashboard only)". Likely still 50 MB; unchanged.
- **Q-014 (Qwen's role)**: models.md/memory say Jaron dropped Qwen from active use 9/30, but no timeline line shows him answering; left OPEN. (I used "dropped 9/30" in OPERATING-MAP and INDEX status text on the strength of models.md.)
- **Sapling "paused"**: timeline 10/16-10/17 says Claude paused pending Anthropic's answer, 10/20 says paused until RunPod balance $8-15, but state/MSI-STATUS shows Sapling running now. Wording kept loose in open-list #17.
- **Q-005, Q-009, Q-019, Q-020, Q-013 (fly)**: unanswered, left alone as the rules say.
- **Kimi 11/2 renewal** is still via Apple (decision due 10/30); a reminder task exists.
- **INDEX.json** is mostly dated Sept history; I corrected the present-tense claims I could prove, not the full file. The weekly candidate list will keep surfacing the rest.
- Older heartbeat-observatory / revenue-desk entries in INDEX.json (G: paths, Codex's three projects) were not verified against disk.

## Tool
- tools/stale_sweep.py -> state/STALE-CANDIDATES.md (38 candidates on first run, mostly dead relative paths and "waiting" words in old READMEs / INDEX.json).
- Windows task "Stale Sweep": weekly Sunday 5 AM, pythonw.exe, first manual run exit code 0, next run Sun 10/25 05:00.
