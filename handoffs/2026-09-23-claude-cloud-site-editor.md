# Handoff - Claude Code cloud session, site editor, 2026-09-23

## UPDATE 2026-09-23 23:37 UTC (7:37 PM ET): Jaron merged PR #26
It is on main, so Vercel deploys it. The Edit button will show for the admin. Publish will still say "not switched on
yet" until SITE_EDITOR_GITHUB_TOKEN is added in Vercel (see below). The first real save is still untested.

## What was built
An admin-only edit mode for heartbeatobservatory.com. PR (merged by Jaron):
https://github.com/JaronKBragg7337/heartbeat-observatory/pull/26
Branch: claude/heartbeat-admin-editor-0300ba

Signed in as admin (is_admin() true), an Edit button shows bottom-left on every page. Tap words to change them; tap a
block to change background, text color, size, bold, alignment, rounded corners, inner spacing, link address, or take it
off the page. "Page" edits the tab name and the page's color settings, and has History to put back any earlier version.
Publish writes the change into the real page file (or shared CSS) as one commit on main; Vercel redeploys in ~1 minute.

No page copy was changed. Every HTML file got exactly one added line (the loader script). Nothing else.

## Migration for the local Claude
None. The editor stores nothing in Supabase. It only calls the existing is_admin() RPC to check the admin.

## What is needed before it works (Jaron's yes)
Vercel env var SITE_EDITOR_GITHUB_TOKEN: a fine-grained GitHub token for heartbeat-observatory only, Contents: Read and
write. Separate from the existing GITHUB_TOKEN (that one is the Fable Survival feedback inbox). Without it, Publish says
"not switched on yet" and saves nothing. After adding it, Vercel needs one redeploy for the function to see it.

## Verified
- node --test tests/editor-source.test.mjs: 13/13.
- tests/editor-browser.mjs: 13/13. Chromium at 390x844, real api/site-edit.js against a fake GitHub and a fake Supabase.
  Edited a heading, a section background, a script-built home line, and a shared color. The saved files changed in
  exactly those spots. Signed-out visitors never load the editor.
- The source reader matches Chrome's parser on all 71 pages.
- Reachable text on main pages: 81-100% of visible words. The rest is database text or the chat bubble script, and the
  editor says so when tapped.
- Vercel preview build of the PR: Ready.

## Not verified
A real iPhone, the live is_admin() call (Supabase health still in question), and a real GitHub commit. All need the
token. On full-screen game pages the Edit button may sit over game controls (admin only).

## Note for every AI that edits this repo
Jaron's saves arrive as commits titled "Site edit: <file> - ...". Pull before editing a page, and never overwrite his words.

## Collisions avoided
Did not touch the Codex site audit. projects\site-audit\ had only BRIEF.md when read; no INVENTORY.md yet.

## How I reached the MSI
Heartbeat MAI connector from a claude.ai cloud session. read_file, list_directory and write_file all worked.
