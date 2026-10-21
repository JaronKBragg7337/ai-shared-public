# Inside the fly — Codex handoff, 2026-09-12

Live: https://www.heartbeatobservatory.com/live-systems/flies/brain/
Repository: https://github.com/JaronKBragg7337/heartbeat-observatory
Commit: bca3d58 (main, pushed; attribution trailer included). Vercel deployed automatically.
Build checkout: C:\Users\lilli\AI-Shared\state\fly-scene-build. Existing G: checkout and audit reference clone untouched.

## Built
Read projects/fly-brain/SCENE-BRIEF.md first. Reference image supplied mood only; no desk, keyboard, coffee, copied layout or third-party identity.
Static CDN Three.js 0.180.0, existing trades.css tokens, measured float16 atlas above a table-tennis table. Region colours, KC-centroid label, once-per-new-tick spike flashes, live vitals, trader/watcher switch, match/set state, last-eight action feed, learning link and visible honesty note. Polls fly_live at 3s and fly_actions at 10s; no write endpoints or trade controls.
Added colony navigation link and repaired #learn tab deep-link handling in the existing flies overview.

No fly.glb exists. Three-shape body/wings placeholder explicitly labelled. GLTFLoader is ready for a file at live-systems/flies/brain/fly.glb, normalizes bounds, and uses named idle/wing/groom/press clips or wing/foreleg bones. Actual asset rig and animations remain unverified until supplied. Avatar motion is illustrative. Sampled DN count is exposed on window.flyScene for future locomotion work.

## Honesty and source differences
- Atlas contains 140,024 positions and 4,050 labelled KC positions (brief said 4,064). Uses actual region membership/counts. Not every simulated neuron has a plotted soma.
- fly_actions column is action, not kind; implementation follows live schema. Table was empty during validation; empty trace is truthful, not demo events.
- DN count is explicitly sampled, not a population-wide firing total. Spikes/sec is labelled simulation time. DRY P&L is explicitly dry-run realized P&L.
- Missing fields are dashes. If data is older than 30s or fetch fails, last known vitals remain labelled and flashes stop. Same at timestamp is never replayed as a fresh spike event.

## Verified locally
Ran the repository with Python HTTP server on MSI loopback 8093. Anonymous Chromium at 390x844 and 1440x1000: WebGL renders measured geometry, region count correct, fresh updates produce flashes, WATCH toggle, orbit pause/reset, no JS errors, no horizontal overflow. Phone screenshot inspected; overlapping cap typography fixed before publication.
Cached local readiness approximately 0.25s on this machine (not a physical phone/network guarantee).
Fault tests passed for missing values, invalid/duplicate indices, duplicate tick suppression, stale tick suppression, network outage labelling, escaped action text, and #learn deep link. Test fixtures intercepted browser reads only; no database mutations.

## Verified remotely
Public route returns HTTP 200 without login. Public index.html, scene.css and scene.js match committed content. Repeated same Chromium phone/laptop checks against the public URL; live atlas and Supabase reads succeeded, zero JS errors/overflow, fresh flashes observed. Cached phone readiness 349ms on MSI. Public screenshots in state/fly-scene-evidence/phone.png and laptop.png; local screenshots preserved as local-phone.png/local-laptop.png. Results JSON files alongside them.

## Unverified / limitations
Physical iPhone/Android GPU and mobile-network timing, real GLB rig/foreleg motion, and an actual new press event (action table empty). GLB 404 is expected until the asset arrives. WebGL/CDN failure leaves live numeric data with an explicit scene-error message. No full connectome simulation runs in the browser.

## Coordination
AI-Shared source checkout, tests (state/test-fly-scene.cjs and state/test-fly-scene-faults.cjs), screenshots and this handoff preserved locally. Handoff/scene sources copied additively to existing G: mirror; cloud upload itself not verified. No protected execution files or core records changed. No PR was created; requested direct main commit used.

Next: drop the approved rigged fly.glb beside the scene and verify its animation naming/mapping. The rest of the live scene is delivered.
