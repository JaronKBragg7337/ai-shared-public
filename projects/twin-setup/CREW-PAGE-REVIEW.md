# Crew page review (2026-10-05, Claude Sonnet 5.5)

## Fixed directly (plain facts)
- Overview card "9 AIs on shift" -> "2 AIs trading now" (Darios, Satya) + "8 AIs on the crew". Each AI now has a status (tools/publish-crew.py STATUS table); paused ones show a "paused" chip.
- DeepSeek: job/schedule no longer say "$10 a day, researches every 2 hours"; says paused since Oct 1 (budget $0). Loss-breaker line hidden while paused.
- Demis Twin marked paused (Jaron, Oct 4).
- Sams Twin moved to Retired (switched off Oct 1); Retired intro updated.
- Schedule tab: removed Verifier+placer, DeepSeek every 2 h, Sams every 3 h; paused bots no longer listed as waking up.
- Rules list: removed the DeepSeek $10-week rule; added "Jaron can pause any trader" and the live Control Room hours/caps (read from `desk.py rules` every publish, so they stay current).
- "Who's on shift" heading -> "The crew".
- Tennis: no page text calls it active (Darios' instructions say "tennis off").
- Numbers now use Polymarket's own realized values (AI +$186.73, hand -$346.53, deposits $243.67, withdrawals $42.00; adds up to $49.00 with $7.13 bonuses/rounding).

## Bigger changes to discuss with Jaron
1. Tone for future clients: the lede ("out in the open... what it has made or lost") and the Retired lede ("told to be careful so many ways they barely acted") read as an internal diary. Needs a plain, professional intro and a one-paragraph "what this is".
2. Page now shows the human lane (hand trades, withdrawals) next to the AIs. Decide wording: "Human spend" and "Jaron by hand" are blunt; a client-facing page might say "Owner hand trades".
3. The Conversations tab publishes the raw bot chat log (shorthand, trade jargon, Jaron's own messages). Keep as an "unedited log" appendix, or hide for client viewing.
4. The Reasoning tab and bot pages show full instruction text word for word; fine for transparency, but long. Consider a short "how it works" summary above.
5. Retired tab: keep as history or fold into an "Archive" section; Live Wire/Darios share one trade tag, which is confusing.
6. Crew roster mixes traders (Darios, Satya, Demis, DeepSeek) with non-trading helpers (Codex, Claude Code, DeepSeek reader, Elons Twin). Split into "Traders" and "Builders and readers".
7. "AI trades so far: 178" counts desk fills grouped per market/side/hour; Polymarket shows 223 settled markets (AI+hand). Pick one definition for clients.
8. Model labels ("Opus 5.5", "GPT-6 Luna") are hand-typed in publish-crew.py and will go stale.
9. The 10/5 desk_schedule hours and caps are only listed as a rule line; a small table would read better.
10. Bills/receipts: coverage metric (system-paid bills vs monthly bills) needs a monthly-bills number to compare against.
