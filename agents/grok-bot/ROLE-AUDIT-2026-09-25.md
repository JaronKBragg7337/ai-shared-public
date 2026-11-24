# Grok Bot role audit - 2026-09-25 (Claude Code, from Jaron's notes)

Jaron: "We use Grok Bot for so much it consumes more usage than the usage that gets used to actually make money. If it's not
touching money or giving info other AIs can't give (TOS), it needs swapped. Telling an AI to change something and things actually
being changed where the settings are is a completely different thing. Some bots may need to be completely remade - no issue."

## What the numbers say
- $15 of Grok on-demand credit (bought 9/23 ~5:20 PM) was gone by 9/24 9:32 AM - about 16 hours. In that window Live Wire
  placed 2 orders of $5 (state/usage-snapshots.md, state/desk-trade.md).
- Live Wire woke ~18 times on 9/24 and wrote 169 log lines; it placed 1 order that day and 1 on 9/25 by 3 PM.
- Most of each wake is not deciding - it is FETCHING: ESPN/Flashscore/Robinhood scoreboards, Polymarket books, positions, the
  last 20 log lines. Fetching needs no judgement and no Grok.

## Each Grok Bot job, and where it should live
| Job | Money or Grok-only info? | Move to |
|---|---|---|
| Live Wire: decide + place live trades | YES (money; Sept belief that Claude/Codex can't trade, superseded 10/7: each provider's terms decide) | **Stays Grok** - but only the decision |
| Live Wire: fetch scores, books, positions every wake | no | **Free script on the MSI** (`tools/live-board.py`, Windows task every 5 min) writes `state/live-board.md`; Live Wire reads that one file instead of browsing |
| Bridge: hourly MSI stack health | no | Free PowerShell Windows task (bridge-health.md shows no runs on 9/24 - it may already be off) |
| 9 PM capture of Jaron's X posts (watch/jaron-x) | Grok-only (X search) | Stays Grok, once a day |
| Sentiment for Bridge (state/sentiment, X mood on markets) | Grok-only (X) | Stays Grok, only for markets actually being traded |
| Scout estimates | no longer needed - DeepSeek is the researcher (proposer.py) | Retire |

## The "remake" (Sept 25 belief that only Jaron could do it; platform fact: the text lives inside the Grok Bot app. Since 10/17 Grok Build can drive that window and bots can edit their own Instructions when told in chat)
Grok Bot's instructions and routine live inside the Grok Bot product, not on the MSI - nothing here can edit them. Once the free
board exists, Live Wire gets new, much shorter Instructions + Routine (to paste once, written in LIVE-WIRE-v2.md): each wake, read
`state/live-board.md`; if nothing is flagged, write one line and sleep; if a game is flagged, check that one game and decide.
