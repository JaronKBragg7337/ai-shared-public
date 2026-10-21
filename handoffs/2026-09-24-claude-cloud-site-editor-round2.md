# Handoff - Claude Code cloud session, site editor round 2, 2026-09-24

Pushed straight to main under the new AGENTS.md rule (no PR). Commit 976c9d0, Vercel production deployment
dpl_AfKVfYdpcYzDtmB9A1Mg8XL3XWCL is READY. Rollback target if needed: dpl_3S5JRTAeHttiamRJLQ5LnG7w61jX (commit d644e6b,
Jaron's own first site edit).

## What changed
1. Editing panel scrolls by itself on iPhone. Cause: the editor's layer covered the page with pointer-events:none;
   iPhone Safari then sent swipes on the panel to the page. The layer is now zero-size, the panel keeps its own swipes
   (overscroll-behavior: contain + a touch guard at its top/bottom edge).
2. Hide this card. Tap any card -> "Hide this card". The list lives in index.html as
   <script type="application/json" id="hb-hidden-cards">. The directory filters it whether the list came from
   Supabase or FALLBACK. Page -> Hidden cards -> Show again. Undo in Changes, History restores.
   "The World" (engine) is hidden now, as Jaron asked. Qwen and Revenue Desk moved into the same list (were a Set in code).
3. Layout mode (bar -> Layout). Home page cards on a board of square cells; shapes Small/Wide/Tall/Big/Round
   (Round = picture circle with a name label, like the preview image). Drag by the ✥ handle, not the card.
   Phone and Computer layouts saved separately in <script id="hb-layout">; each null = normal page (phone = the
   clean single column it already was). Computer board can be arranged from the phone (shown shrunk).
   Long-press link preview (-webkit-touch-callout) is off while editing. Runtime: /hb-board.js.
4. The directory request now gives up after 6 s and uses FALLBACK (no more endless "Loading").
No words changed: visible text of the home page compared line by line before/after; only The World card differs.

## Cards on the board
world-town, world-2, world-ashgrove, studio-school, studio-worlds-lab, studio-pc-games, plus every directory key
(social, video, host, showcase, games, library, printer, pam). Trade Desk, AI Workers, AI Funding (in the preview
image) are NOT cards on the home page today, so they can't be placed yet. Adding them means new cards with new words -
Jaron's call.

## Migration for the local Claude
None.

## Verified
- tests/editor-browser.mjs 30/30 at 390x844 (real api/site-edit.js, fake GitHub/Supabase): panel swipe scrolls the
  panel and not the page; hide card; board start, shape change, touch-drag moves a card with no overlaps; computer
  board shrunk on phone; publish writes only the two JSON lines; visitor sees phone board then computer board on a
  wide screen; History restores the earlier file. node --test tests/editor-source.test.mjs 13/13.
- Live: https://www.heartbeatobservatory.com/ loaded from the MSI in WebKit and Chromium at iPhone 13 size, signed out:
  status 200, no page errors, no sideways scroll, The World not shown, no board (none arranged yet), editor not loaded.
  Supabase answered ("Current directory") at check time.

## Not verified
The panel scroll on a real iPhone (iOS scrolling can't be emulated here; WebKit desktop is the closest). The editor
itself on the live site (needs Jaron's sign-in).

## World pictures - finding and proposal (not built)
Finding: the live world cards never showed screenshots. They are CSS gradients (observatory.css .orb-town/.orb-city/
.orb-grove). The screenshots Jaron sees are baked into og-revised.jpg, a flat link-preview image made once by hand.
Nothing refreshes it. Why other AIs failed to show the real worlds:
- The worlds are WebGL. A plain headless screenshot (no GPU) gives a black or blank canvas.
- The hub has a 300 s day/night cycle and an orbiting camera, so a capture at a random moment is random.
- Only engine/hub has pin flags (?preview=1&dev=1&tod=&cam=). world2 has ?preview only; world3/Ashgrove has none.
- Serverless (Vercel) can't run a WebGL browser cheaply; nobody had a scheduled runner.
Proposal: a GitHub Actions workflow (the repo already runs two), nightly and on demand:
Playwright + SwiftShader (tools/harness/shoot.js already does this and checks real pixels) opens each world with a
pinned time and camera, refuses a blank frame, saves images/worlds/<key>.webp (~600 px), commits only if it changed
visibly. Cards read it as background-image with today's gradient as fallback; og-revised.jpg can be rebuilt the same
way. Needs: tod/cam flags added to world2 and Ashgrove (small), one workflow file. Free on a public repo; one commit
and redeploy per night at most.

## How I reached the MSI
Heartbeat MAI connector: read_file, write_file, shell_exec (ran the live check with the Playwright in
C:\Users\lilli\Claude active\hb-harness; script and screenshots in %LOCALAPPDATA%\Temp\hb-live-check\).
This container's own network can't reach heartbeatobservatory.com (proxy 403), so live checks go through the MSI.
