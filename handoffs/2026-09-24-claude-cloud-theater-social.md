# Handoff - Claude Code cloud session: theater + social, 2026-09-24

## ADDENDUM (same session, after Jaron re-approved the full MSI scan)
- KEAVA'S MISSING CODE EXISTS. C:\Users\lilli\iCloudDrive\Dummy test folder_\keava-owent (and "keava-owent 2",
  identical main.py hash 0E238AD8) holds all 15 subsystems the GitHub repo lacks: store, kernel (loop, continuity,
  state), livereference, ledger (consumption, contribution, orientation), memory (graph, recall, arrangement
  relational + packing_geometry slot), spark, membrane (modes, approval), actions (receipts, registry), transport
  (email). Its tests: 10 passed on the MSI (Python 3.12.10, pytest). NOT run as a loop: PyYAML is not installed and
  the loop has an email transport (outward - needs Jaron's yes). The GitHub repo can be completed from this copy
  when Jaron says so. C:\Users\lilli\iCloudDrive\Keava-Owent has no .py files.
- Theater copies: C:\Users\lilli\Claude Code\movie-theater = earlier same-day Grand Palace (f97492e, main.js 662
  lines); G:\My Drive\Codex Active\projects\Movie-Theater-Three.js-Asset- = same as GitHub HEAD (c3da1ed). GitHub
  is newest; /video/3d/ uses it.
- Six other site copies (Claude active, Codex Active x3 incl. president-office and island-integration, OneDrive
  Slack tab, _stale) hold older versions of the same /video and /social pages. None has an upload theater or a
  live Keava. (Their "upload" hits were upload.wikimedia.org film URLs.)

Pushed straight to main (AGENTS.md rule). Commit 056459e, Vercel production dpl_J7JX6dQkWKRT8WMxB3VmAztw89XM READY.
Rollback target: dpl_EGEc1QZoz3L7sBWFvuw2BzK4bZkB (commit 3d19da7, Jaron's "hid PAM" site edit).
No database changes; no SQL written. Codex INVENTORY.md did not exist yet when this ran (only BRIEF.md).

## Every theater version found
1. /video (this repo, video/index.html) - flat page, one screen, 7 fixed free films (Blender, public domain, NASA).
   No upload, no links. WORKS: live WebKit iPhone check played Big Buck Bunny (5.5 s, no errors).
2. Town Square theater interior (engine/hub/main.js, interior "theater") - films on an in-world screen. Can't sit.
3. World 2 theater interior (world2/main.js) - screening + real chair meshes; station reads "pick your seat soon". Can't sit.
4. Worlds-lab Marquee Row / cinema-district (worlds-lab/lib/v1+v2/cinema.js) - three walk-in theaters, preview world.
   Cosmodrome preview also uses cinema v2.
5. Grand Palace Cinema - repo JaronKBragg7337/Movie-Theater-Three.js-Asset- (CC0), test page
   https://jaronkbragg7337.github.io/Movie-Theater-Three.js-Asset- . 448-seat walkable building, sit in any seat,
   upload a file, paste mp4/webm/HLS, YouTube/TikTok links, 10-film playlist, phone controls. THE BEST ONE.
   It was never placed in a world. Now at /video/3d/ (see below).
   Playback limits (from its README, confirmed in code): direct links need the host to allow CORS for the 3D
   screen; YouTube/TikTok play in their own player (no light spill); uploads play only for the uploader (blob URL,
   nothing is stored or shared).

## Social page (/social) - what works, verified live signed out
Posts (18 shown), live news (AP/BBC headlines from /api/news - Perplexity), trending, minds to follow
(Perplexity, Claude), surface status, search box filters posts. Likes/reposts/follows/bookmarks/replies are all
wired to Supabase tables (post_likes, post_reposts, follows, post_bookmarks, post_replies) - not exercised signed
in (needs an account). Keava: NOT plugged in on the page ("Not connected yet" is accurate). See addendum: the
code to run it exists on the MSI.

## Shipped
- /social: on a phone the top bar was 489 px wide on a 390 px screen - "Sign in" was off the right edge, page
  scrolled sideways. Phones (<=560 px) now get two rows: logo + buttons, then full-width search. Nothing hidden.
- /video: widest seat row pushed the page sideways on phones; seats shrink under 420 px, room clips overflow.
- /video/3d/: Grand Palace Cinema framed on the site (same pattern as the game pages), with "← Theater" back link.
  /video got one new link "Take a seat in 3D →" so its "see it in 3D with your own seat" line is true.
Live check (MSI, WebKit, iPhone 13): no sideways scroll on either page, Sign in on screen, 3D frame loads and draws,
USE/GRID/MEDIA buttons present, no page errors.

## Upgrade choices put to Jaron (not built)
Theater: A) place Grand Palace in a world; B) shared uploads (storage + moderation rule: his call);
C) link + upload on the flat /video page; D) watch-together.
Social: Keava (what should it be; restore the full code to GitHub; run it - needs PyYAML and a yes on email),
young users (ages, parent controls, who moderates, private messages) - questions, not designs.

## How I reached the MSI
Heartbeat MAI connector: list_directory, read_file, write_file, verify_http_response, shell_exec (Playwright checks
in %LOCALAPPDATA%\Temp\hb-live-check\ with C:\Users\lilli\Claude active\hb-harness; the folder scan; Keava tests).
