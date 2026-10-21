# Fly scene, second pass - Codex handoff, 2026-09-12

Live: https://www.heartbeatobservatory.com/live-systems/flies/brain/
Commit: b846bdf, main, pushed with Codex attribution. Vercel deployment verified.
Local route: Codex shell directly on MSI; no connector. Checkout: C:\Users\lilli\AI-Shared\state\fly-scene-build.

This is an additive correction to handoffs/2026-09-12-codex-fly-scene.md. That earlier handoff's statement that no GLB exists and its proposed next step are now superseded. Its historical record is preserved.

## Delivered

Read the updated Standards and The fly asset sections of projects/fly-brain/SCENE-BRIEF.md and decisions/3D-STANDARDS.md before this work.

- Built fly.glb headlessly with Blender 5.1.2 from TuragaLab/flybody commit d015e9bfe441bd90ae431bac24c55cb74bdbce26. All 85 mesh parts, 67 XML body nodes and 102 joint definitions remain. XML mesh scale 0.1 is applied once; source CGS lengths convert to metres at root. Welded duplicate vertices and decimated larger meshes: 272,550 source faces to 103,032 exported faces. GLB is 1,967,404 bytes, below 8 MB.
- XML body parents, mesh parents, local positions, normalized quaternions, joint axes and ranges preserved. glTF extras contain ordered joint definitions; runtime rotates the body nodes about their joint origins. The measured model's left/right wing roll sign was tested: negative roll actually raises both wings. No whole-avatar bobbing substitutes for joints.
- Above +20: wings rise. Below -15: forelegs groom. A fresh polled PRESS raises and returns the left foreleg for a tap. Selected-fly changes clear pending tap motion. Stale live state returns to neutral. No player controls, joystick, steering, or grid. Camera orbit remains.
- Regulation table envelope: 2.74 x 1.525 m; surface 0.76 m above floor; net 0.1525 m above table. Separate boards, white lines, apron, crossmembers, braced legs, casters, bolts, net posts/clamps/screws, woven net geometry, top tape, and paddle.
- CC0 ambientCG Wood051 colour, OpenGL normal and roughness maps, resized to 512 px; total 125,211 bytes. Original source and licence links in ASSETS.md. Flybody retains Apache-2.0 with its full licence. Table paint uses roughness variation; paddle wood repeats account for its smaller surface.
- Asset IDs toggle opens overview coordinate bubbles and an inspector for all 230 named nodes/components. No scene movement commands. Coordinates are world metres; individual fly body labels mark joint origins.
- On-screen honesty: fly enlarged 160x; brain separately enlarged, not registered inside the flybody model; motion is an illustrative threshold mapping. Table frame and paddle construction are illustrative rather than a measured manufacturer scan. Supabase and atlas read paths remain read-only.

## Verified locally

- tools/verify_fly.py checked all 66 body-parent edges and 85 mesh-parent edges against fruitfly.xml, and every body/geom translation/quaternion to 1e-6 after Z-up to Y-up conversion. All 85 meshes present; size under budget.
- Browser module test confirmed both wings move upward, foreleg grooming and tap rotate joints, fixed joint-origin translations, unchanged middle legs, and neutral pose restoration. Left wing centre rises 0.103 display metres; peak tap foot clearance about 0.098 m at 160x display scale. This checks the selected illustrative poses, not general physics collision safety.
- Fresh PRESS browser fixture traversed the real 10-second polling path and entered then left the press pose. Fixture intercepted browser responses only; no database writes or actual orders.
- Existing missing-field, duplicate/invalid-index, repeated-tick, stale-tick, outage, action-text escaping and learning-link tests pass. A Windows code-page error was caught by these tests and corrected before publication.
- Phone 390x844 and laptop 1440x1000: fly, atlas, vitals, selection and orbit controls work; no page errors, failed asset requests or horizontal overflow. Cached local readiness including GLB: 593/617 ms on MSI. Local screenshots inspected.

## Verified remotely

Anonymous public URL returns 200. Public GLB bytes exactly match the local built asset; index.html, scene.js and assets.js match after normalizing Git CRLF/LF line endings. Public phone/laptop tests: no page errors, failed requests or overflow; WATCH selection and orbit pause/reset work; measured atlas and live data load. Cached readiness including GLB: 707/719 ms on MSI. Public joint/debug inspection also passed.

Evidence: state/fly-scene-evidence/pass2-local/ and pass2-public/ (phone/laptop full-page and stage screenshots plus results.json); pass2-public-phone-debug.png; pass2-joint-tests.json and pass2-public-joint-tests.json.
Tests: state/test-fly-pass2.cjs, state/test-fly-pass2-public.cjs, state/test-fly-press.cjs, state/test-fly-scene-pass2-responsive.cjs, state/test-fly-scene-faults.cjs. Reproducible export and structural verifier are committed under the public scene's tools/ folder.

## Unverified / boundaries

Physical iPhone/Android hardware and mobile-network speed remain untested. Timing is Chromium on MSI at phone/laptop viewport sizes. A real newly recorded PRESS did not occur during the session; the polling path and joint motion were verified with browser-only fixtures. No browser MuJoCo simulation, measured motor reconstruction, locomotion, or universal self-collision guarantee is claimed. The brain atlas still reports 4,050 KC positions versus 4,064 in the brief; actual atlas membership is used.

## Synchronization and ownership

Source checkout, build recipe, tests, screenshots, provenance and this handoff are in AI-Shared. Scene sources, tests, evidence and handoff are copied to the existing G:\My Drive\AI-Shared-mirror, with file hashes checked. This verifies the mounted mirror, not completion of Google Drive cloud upload. No protected execution files or core records changed. No other agent was consulted.

No Jaron decision blocks this pass. Further locomotion or physics integration is future scope; this scene is delivered.
