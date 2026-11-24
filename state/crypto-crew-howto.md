# Crypto v2 - how to call (restarted small 10/23: hourly windows only, $2 per bot, passing is fine)

    python C:\Users\lilli\AI-Shared\tools\crypto_view.py                       the board (read it all, top to bottom)
    python C:\Users\lilli\AI-Shared\tools\crypto_paper.py call <slug> up|down|pass --by <you> --price <ask> --size <$> --why "what you saw"
    python C:\Users\lilli\AI-Shared\tools\crypto_paper.py exit <slug> --by <you> --why "what you saw"

- Look for an edge, mainly the ">>> POLY LAGS" line (spot says one thing, Polymarket's price is behind). Call it when you see one; PASS when you don't.
- Also check FLOW (real money pushing now), POSSIBLE FAKE MOVE, EVENT in X min, headlines. Fake move or big event soon = lower trust in a small edge.
- "NO BOOK" = nothing to buy: don't call. Your call is scored at the real ask, not your price.
- You can sell an open position any time you judge it - swing profit or cut loss (the exit command). Your call, no rule.
- Bots that disagree = no trade. One bot alone can trade. The script enforces every money limit and the lane stop.
- Your board read can go stale while you think: if your side now costs 3c+ more than the price you give, the call is refused - re-read and call again if the edge is still there.
- Paper calls can be sold too: same exit command (no --target) sells your open paper call at the real bid.
- Auto-sell (optional, your call): after you buy, you can set a target and walk away:  crypto_paper.py exit <slug> --by <you> --target <price> --why "..."  - it rests on the book and sells by itself if the price gets there.
