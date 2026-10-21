# HANDOFF — News Archive: live

- **Date/time:** 2026-09-25 (early morning ET)
- **From:** Claude (Claude Code cloud session; AGENTS.md and the MSI live checks through the Heartbeat MAI connector)
- **Project:** projects/news-show  |  **Repo/branch:** JaronKBragg7337/heartbeat-observatory @ main (90bb896)  |  **Live URL:** https://www.heartbeatobservatory.com/news/archive/

## What I did
- **/news/archive/**: every day's captures from every AI, read straight from the public watch repo on GitHub. No database, no
  copies in the site repo: new captures show up as soon as they're pushed to watch.
  - File list: GitHub tree API (one call, cached 10 min per browser). If GitHub rate-limits (60 calls/hour per address), it falls
    back to the jsDelivr mirror plus a direct check for today's and yesterday's files. Files: raw.githubusercontent.com (jsDelivr
    fallback). The page re-lists every 10 minutes, so captures landing during the day appear without a reload.
  - Reads: `<writer>/YYYY-MM-DD.md` (and hourly `-HH.md`) for every writer folder, `brief/`, `market-feed/*.jsonl`. Skips
    jaron-x (Jaron's own X posts, not news), offers, agents, collectors. grok/, qwen/, kimi/, perplexity/ appear automatically
    once they file.
- **By day** (default: today, or the latest captures with "today's haven't landed yet"): each AI's card (filed time, status, item
  count, link to the file), the day's brief, a jump bar of the 21 domains with counts, every domain with each AI's items (label
  observed/claim/theory, source class, time, source links, market tag), the market feed, and the AIs' own notes (persistence,
  silences, could not see, convergence/divergence) folded away. Date picker, back/forward, a strip of every day back to Sept 18.
- **By topic**: one domain from every AI across every day. **By AI**: everything one AI filed, day by day, domain by domain.
- **Search**: across all days (every word must match), with the label filter and highlighted matches.
- Domain names come from each day's own files, so Sept 18-24 show 11 as "Indiana / Midwest ground truth" and later days show
  "major US cities and regions" (d2b4702 in watch). Links are shareable: #/day/2026-09-24, #/topic/03, #/ai/codex, #/search/diesel.
- **Links in**: /news/ has "Every story, every source →" under the TV and in "How this show is made", and each show's date links
  to that day in the archive. Home page: a "News Archive" row right under Heartbeat News in the directory (added by the page
  even without a surfaces row).
- Main had moved during the work (2380977, Jaron's WRITER.md change); I rebased onto it, nothing of his touched.

## Verified vs assumed
- Verified live (MSI, real site, real GitHub; iPhone 13 WebKit, Pixel 7 Chromium, desktop Chromium): Sept 24 = 3 AIs, 77 items
  across 20 of 21 domains, 94 source links; Sept 18 = 2 AIs, 48 items; topic 01 = 19 items on 5 days; By AI Claude = 73 items in 5
  captures; search "diesel" = 10 matches; 6 days in the strip; list via GitHub; no sideways scroll; inputs 16px (no iPhone zoom);
  no page errors on the archive; links from /news/ and the home page present on all three.
- Verified locally: parser on all 15 captures (338 items; labels read, including the first captures' "[09-18]"/"[this week]"
  time markers).
- NOT verified: the jsDelivr fallback path live (GitHub answered every time); a real phone (test browsers only); how it feels at
  60+ days of captures (search reads every capture file, 6 at a time: fine now at ~15 files, worth an index file if it slows).

## Exact next step for the next AI
- Nothing blocking. If the archive gets slow as captures pile up, add a daily index.json to the watch repo (the writers already
  commit there) and have the page read that first.
