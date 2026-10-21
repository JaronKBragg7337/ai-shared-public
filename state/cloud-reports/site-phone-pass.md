# Site phone pass — report (2026-10-03)

Scope: home, games, live-systems (index, crew, trades, schedule, chat, reasoning), news, tv, worlds-lab. `games/the-cosmos/` untouched.
Method: Chromium at 390x844 (touch, 2x) against a local server; checked horizontal overflow, tap targets, text size, lazy loading, console errors, internal links.

## Shipped (branch `claude/heartbeat-phone-polish-lwfwo6`, draft PR https://github.com/JaronKBragg7337/heartbeat-observatory/pull/27 — NOT merged)
1. section.css — 44px taps, tighter padding (games, live-systems, crew pages)
2. observatory.css — home nav fits at 390px (two rows), 44px taps, 12px+ text
3. news.css — 44px control buttons/links
4. tv/ — 44px taps, 12px+ text, title "Heartbeat TV — tuning in…" instead of "…"
5. worlds-lab — tap targets, chip text
6. live-systems — fixed missing trades.css path (crew/reasoning + flies pages were unstyled)

## Results at 390px
- No sideways scroll on any page (before or after).
- Tap targets: all links/buttons in scope now >=44px (flies pages not in scope; still ~22px).
- No images/iframes below the fold lacked lazy loading (none found).
- Home first screen already states what the site is (eyebrow + dek); kept your words.

## Not done / caveats
- LIVE CHECK NOT DONE: sandbox network policy blocks heartbeatobservatory.com (403). I did not push straight to main because I couldn't verify after deploy; merge the PR, then check live.
- Console errors seen locally were blocked CDNs (supabase/esm.sh/jsdelivr/fonts) and /_vercel/insights 404 on the local server — environment artifacts, not confirmed on live.
- News page loads Three.js studio up front; it is the first-screen content, so I did not defer it.
- Floating phone button (bubble.js) overlaps text at screen bottom right; not changed.
