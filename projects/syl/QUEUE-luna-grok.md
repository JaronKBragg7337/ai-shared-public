# Next Cosmos jobs for Luna 6 and Grok Build (Jaron 10/2 12:41 AM: "let's see how much can we do with Luna and grok build")
Start after Sol's two-player fix is published. One job at a time per worktree; each publishes itself (validate, rebase, push,
restart the 8390 server if server code changed) and appends a timeline line. Claude only writes briefs and reads reports.

## Luna 6 (chores, near free)
1. Server watchdog: restart the 8390 authority if it dies or /health fails (no admin needed; e.g. a hidden PowerShell loop
   started from the HKCU Run entry), log restarts.
2. Client-error log reader: summarize server/.data/client-errors.log for Claude (after one of his kids's next try).
3. Raider crews: vary faces/clothes from the 7 Loft people (tints, hair, outfits) so raiders don't share hire-pool faces.
4. NPC pilot orders held by the server (Sol's list: still local-only).
5. Separate landing pads on Phobos/Deimos per player.

## Grok Build (looks + builds - also the test of how far it goes alone)
6. Real models for the plain props: the salvage cargo module and the survey sample beacons (Meridian-level detail).
7. Phobos ground near the pad: boulders, crater-on-crater shadows, real regolith look at eye level.
8. The Shrike's own look: a meaner palette and silhouette, not the Meridian's.
9. Fly a captured ship home yourself (today a prize crew delivers it).
10. Player-to-player and player-to-ship collision on the server (Sol's list).

Measure: each job's time, whether it finished alone, and what Claude had to fix. That decides how much Claude/Sonnet/Sol
work moves to Luna and Grok for good.

## Money (Luna, first thing after 5:38 AM Codex reset)
11. desk_trades fills don't record buy vs sell (side = yes/no only), so round-trip profit (buy then sell before the game
    ends, e.g. Jaron's +$29 Tulsa trade 10/2) is invisible; only settlement P&L counts. Add an `action` column (buy/sell)
    from the activity's ORDER_ACTION, backfill from the Polymarket activities feed as far back as it pages, and make
    tools/my-trades.py and tools/grok-money.py compute realized profit from fills + settlements. Bots and Jaron stay separate
    (actor). Verify against his Tulsa trade (+~$29.38) and tonight's BTC windows.

## Jaron 10/2 6:54 PM - after playing the opening (queued, not started)
12. Voices: every NPC speaks its lines (TTS or recorded), and proximity voice chat between nearby players without a phone call (WebRTC through the authority for signalling).
13. A bigger cargo ship with a vehicle ramp to carry rovers between worlds.
14. Player shops: buy goods, then sell them at your own shop/stall.
