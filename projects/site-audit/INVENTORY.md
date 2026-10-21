# Heartbeat Observatory site audit

Read-only inventory requested in `BRIEF.md`. No code, settings, database rows, or deployments were changed.

**Evidence date:** 2026-09-24. The public-site page sweep and trade-page check were made during the earlier audit run. Vercel’s live deployment list now shows production READY at `d45b078` on GitHub `main`; later same-day commits add “bring your own video,” social ranking, and the Grand Palace in Ashgrove. The MSI checkouts are old branches: `C:\Users\lilli\Claude active\heartbeat-observatory` is on `codex/professional-observatory` at `69ad5f2` (2026-09-09); the G: checkout is on that branch at `33a339a` (2026-09-07) and has uncommitted Qwen changes. Do not use either as the current site.

## 1. Every page

The site repo is [heartbeat-observatory](https://github.com/JaronKBragg7337/heartbeat-observatory). The production hostname is `https://www.heartbeatobservatory.com`. The current GitHub `main` tree contains 72 HTML pages. The earlier public-route sweep reported HTTP 200 for its 71 routes; Vercel’s current production deployment is READY at `d45b078` on `main`. The same-day theater handoff reports `/video/3d/` live and drawing in its iPhone check. Reachability means a link or in-world portal on the site, not merely that a URL can be guessed.

The route bullets below use `heartbeat-observatory` `main` as their source unless a separate deployment or embedded app is named. The 71 visitor routes tested in the earlier public sweep returned HTTP 200; the extra HTML file is the exposed template artifact noted below. Each bullet states whether an ordinary site link was found and where. Embedded apps have their own Vercel deployment in addition to the wrapper page.

### Main pages and tools

- `/` — Observatory home and page directory; directly reachable by the site address. Its directory is Supabase-backed with a fallback list.
- `/3DPrinterAsset/` — 3D printer asset area; linked from the home directory. No older duplicate identified.
- `/admin/` — admin tools; no ordinary visitor link found. Admin/editor controls may expose it after sign-in. No public duplicate identified.
- `/chat-neighborhood/` — neighborhood chat page; no ordinary home-directory link found. Current live use was not established.
- `/engine/` — entry to The Engine world; home world card links here. `/engine/hub/` is its playable hub, not a duplicate.
- `/engine/hub/` — walkable Town Square world with NPC actors and theater interior; linked from `/engine/` and the home world card.
- `/HeartbeatCenter/` — Heartbeat Center page; site page, but no current home-directory link was confirmed.
- `/island/` — The Unfinished Island; no ordinary home or directory link found. Its Windows hourly world-worker task is disabled.
- `/lab/voice/` — device voice test page (“Voice lab — can the world talk?”); no link from the home page or a parent page was found in the current repository.
- `/library/` — library page; linked from the home directory and world interiors. No older deployed duplicate identified.
- `/pam/` — PAM dashboard and application map; its home card is hidden and no visitor entry link is present. The page links back to itself and to `/admin/`.
- `/projects/` — project directory; linked from the home directory. No duplicate identified.
- `/qwen/` — Qwen dashboard; no current home-directory card was confirmed. Its database dependencies are listed below.
- `/school/` — Fly School landing page; linked from the home page’s Fly School section. `/school/<fly-id>` rewrites to the live classroom route.
- `/social/` — social feed and live news; linked from the home directory. Keava is labeled “Not connected yet”; older local copies are stale.
- `/space/` — space page; site page, but no current home-directory link was confirmed.
- `/standards/` — standards page; site page, but no current home-directory link was confirmed.
- `/video/` — film page with seven fixed free films plus “bring your own video” link/device playback; linked from the home directory and world theaters. The same-day production deployment adds local media and pasted-link playback.
- `/video/3d/` — framed Grand Palace Cinema; linked from `/video/`. The 2026-09-24 handoff reports it live and drawing in its iPhone check.

### Live systems and school

- `/live-systems/` — directory of operating systems; linked from the home directory.
- `/live-systems/flies/` — fly systems page; linked from Live Systems.
- `/live-systems/flies/brain/` — fly brain view; reachable through the fly pages.
- `/live-systems/flies/school/` — Fly School status; linked from the fly pages. It currently reports students but their last sign of life was 3.3 days ago, so “live” wording overstates activity.
- `/live-systems/flies/school/live/` — live classroom view; linked from Fly School.
- `/live-systems/habitat/` — Habitat systems view; linked from Live Systems.
- `/live-systems/paper/` — paper-trading view; linked from Live Systems.
- `/live-systems/revenue/` — Revenue Desk view; linked from Live Systems.
- `/live-systems/trades/` — trade queue and proposals; reachable from Live Systems. Rechecked signed out on 2026-09-24: first paint showed “Loading…”, then after about 7 seconds the page showed `Updated 10:20:41 AM`, 56 awaiting, 46 verified, 0 approved, 4 placed, and populated proposal cards. No controls were clicked and no trade was submitted. It works, with a noticeable initial wait.

### Games

Every row below is deployed under the main site repo and linked from `/games/`, except where called out. The game index contains 18 entries; the extra route below is the President Sim classic page.

- `/games/` — game directory; linked from the home directory.
- `/games/cyber-trench-overdrive/` — Cyber-Trench Overdrive wrapper for its Vercel game; linked from `/games/`.
- `/games/fable-survival/` — Fable Survival; linked from `/games/`. Its standalone source includes a paused-project save API, while the live wrapper targets the active Heartbeat project for Realtime; see project notes below.
- `/games/mindgames/` — MindGames wrapper for the GitHub Pages build; linked from `/games/`.
- `/games/northstar-addressable-world/` — Northstar Addressable World wrapper; linked from `/games/`.
- `/games/orbit-salvage/` — Orbit Salvage; linked from `/games/`, retained but not promoted after Jaron’s review.
- `/games/parkworks/` — Parkworks Tycoon; linked from `/games/`.
- `/games/president-sim/` — current 3D President Sim; linked from `/games/`.
- `/games/president-sim/classic.html` — older classic President Sim edition; linked from the President Sim page/index.
- `/games/rift-clash/` — Rift Clash wrapper; linked from `/games/`. Bots work; online multiplayer needs a running game server and was not verified.
- `/games/robot-evolution-lab/` — Robot Evolution Lab wrapper; linked from `/games/`.
- `/games/rustfall/` — Rustfall; linked from `/games/`.
- `/games/signal-drift/` — Signal Drift wrapper; linked from `/games/`.
- `/games/syl/` — canonical SYL — Space You Land; linked from `/games/`.
- `/games/syl/desktop.html` — desktop variant of canonical SYL; reachable from the SYL page.
- `/games/syl-test/` — older SYL test, not the canonical game; linked from the game list.
- `/games/the-cosmos/` — The Cosmos; linked from `/games/`.
- `/games/the-defender-3d/` — The Defender 3D wrapper; linked from `/games/`.
- `/games/the-necklace-show/` — The Necklace Show wrapper; linked from `/games/`.
- `/games/wasteland-commons/` — Wasteland Commons wrapper to its Vercel deployment; linked from `/games/`. Shared multiplayer and persistence are not configured in the live service.

### Legacy PC games

- `/PCGames/` — legacy PC game directory; linked from the home directory.
- `/PCGames/peakaboom/` — Peakaboom page; linked from `/PCGames/`.
- `/PCGames/syl/` — older SYL desktop experiment; linked from `/PCGames/`. The canonical SYL is `/games/syl/`.

### Worlds

- `/world2/` — World 2 city; linked from its home world card. Its in-world theater is an older, separate implementation from `/video/3d/`.
- `/world2/gate/` — World 2 entrance; linked from `/world2/` and the world card.
- `/world3/` — Ashgrove/world 3 entry; linked from its home world card. The latest production deployment places Grand Palace Cinema in Ashgrove.
- `/world3/gate/` — World 3 entrance; linked from `/world3/`.
- `/world3/town/` — Ashgrove town; linked from the World 3 gate/world flow. Its daily clock workflow is described below.
- `/worlds-lab/` — preview world directory; linked from the home directory.
- `/worlds-lab/starter/` — starter world; linked from Worlds Lab.
- `/worlds-lab/worlds/cinema-district/` — Marquee Row cinema preview; linked from Worlds Lab. This is another theater implementation.
- `/worlds-lab/worlds/cosmodrome/` — Cosmodrome preview, includes a theater; linked from Worlds Lab.
- `/worlds-lab/worlds/fort-wayne/` — Fort Wayne preview; linked from Worlds Lab.
- `/worlds-lab/worlds/island-resort/` — Island Resort preview; linked from Worlds Lab.
- `/worlds-lab/worlds/neon-bazaar/` — Neon Bazaar preview; linked from Worlds Lab.
- `/worlds-lab/worlds/railway-valley/` — Railway Valley preview; linked from Worlds Lab.
- `/worlds-lab/worlds/skyport/` — Skyport preview; linked from Worlds Lab.
- `/worlds-lab/worlds/theme-park/` — Theme Park preview; linked from Worlds Lab.
- `/worlds-lab/worlds/winter-hollow/` — Winter Hollow preview; linked from Worlds Lab.
- `/worlds-lab/coming-soon/haunted-manor/` — coming-soon world stub; linked from Worlds Lab.
- `/worlds-lab/coming-soon/mars-colony/` — coming-soon world stub; linked from Worlds Lab.
- `/worlds-lab/coming-soon/sky-islands/` — coming-soon world stub; linked from Worlds Lab.
- `/worlds-lab/coming-soon/underwater-reef/` — coming-soon world stub; linked from Worlds Lab.
- `/worlds-lab/lib/v1/page-template.html` — internal page template served publicly but not linked as a visitor destination; treat as an exposed build artifact, not a finished world.

### Deployed game pages outside the site

These are separate deployments, not pages under `heartbeatobservatory.com`. MindGames, Robot Evolution Lab, Signal Drift, The Necklace Show, Northstar Addressable World, The Defender 3D, Cyber-Trench Overdrive, Rift Clash, and Wasteland Commons each have an external deployment embedded by a site wrapper above. Their separate external URLs are listed in `projects/games/INVENTORY-2026-09-22.md`. The eight Free Game Hub titles (TRACE, Roll & Reach, The Loop, LATTICE, FLUX, DRIFT, SENTINEL, TWIST) share `https://jaronkbragg7337.github.io/Free-Game-Hub/` and were not linked from the site in the prior route audit.

**Theater versions:** `/video/` is the flat page with fixed films and user-selected playback; `/engine/hub/` and `/world2/` have older in-world screens; Worlds Lab has cinema previews; Grand Palace is framed at `/video/3d/` and, in the latest deployment, placed in Ashgrove. Grand Palace is the strongest theater: 448 seats, seat selection, playlists and local-file/direct-link/YouTube/TikTok playback. Local uploads play only in that visitor’s browser; they are not stored or shared. Its standalone test URL remains a duplicate deployment.

**Reachability limits:** the earlier crawler found 55 of 71 routes by following static links from `/`; live database-built home links and in-world portals add paths the static crawler cannot see. “No ordinary home link” means not present in the live home directory or the checked static link tree; it does not rule out a direct link from an untested signed-in view. The unlinked Free Game Hub is a confirmed orphan. Pirate World has no site route or browser build yet; see inactive Supabase projects below.

### GitHub repository register (all 100 repositories)

GitHub returned 100 repositories for `JaronKBragg7337`; a second page at offset 100 returned none. All 100 are public. Each line gives the latest default-branch commit SHA/date fetched from GitHub. Two repositories returned no commit SHA; their last-push dates are shown instead. A homepage URL is reported as deployment evidence, not proof that the page still works. For lines marked with no match, I found neither a GitHub homepage deployment nor a matching project in the 12-project Vercel list; an unlisted host is not ruled out.

#### A site page or deployment was found

- [President-Sim](https://github.com/JaronKBragg7337/President-Sim) — A presidential choice-based simulation where every decision shapes peace, rebellion, and morality. Built ; last commit: 2026-09-05 UTC, 3b78a70. Deployment/site: No separate homepage or Vercel deployment found; Heartbeat has a separate in-repo page at /games/president-sim/.
- [The-Engine-Of-Division-](https://github.com/JaronKBragg7337/The-Engine-Of-Division-) — Humanity was never destroyed by its monsters—it was distracted by its mirrors. The Engine of Division exp; last commit: 2025-12-22 UTC, 9d8b03b. Deployment/site: A separate Vercel project named v0-engine-of-division-summary is READY; repo-to-project linkage is not established.
- [Framing-Lens](https://github.com/JaronKBragg7337/Framing-Lens) — A mobile-first Perspective / Framing exercise app that converts ambiguous prompts into descriptive respon; last commit: 2026-01-09 UTC, abbc9aa. Deployment/site: A Vercel project named v0-framing-lens-project exists but has no deployment; its GitHub source link was not established.
- [heartbeat-observatory](https://github.com/JaronKBragg7337/heartbeat-observatory) — A live, open place to watch working systems, host projects in the open, share what actually works, and pl; last commit: 2026-09-24 UTC, d45b078. Deployment/site: https://www.heartbeatobservatory.com — READY main site; its current page source is this repo.
- [Kurearthis](https://github.com/JaronKBragg7337/Kurearthis) — Game project — built by Claude and Codex with Jaron; last commit: 2026-06-22 UTC, c972376. Deployment/site: No runnable deployment found; prior inventory found only a README.
- [Free-Game-Hub](https://github.com/JaronKBragg7337/Free-Game-Hub) — A single shelf for the playable browser games on this account, indexed by games.json.; last commit: 2026-07-02 UTC, 899acdd. Deployment/site: https://jaronkbragg7337.github.io/Free-Game-Hub/ — live, with eight games; not linked from Heartbeat.
- [fable-survival](https://github.com/JaronKBragg7337/fable-survival) — Mobile-first DayZ-inspired browser survival prototype in Three.js. Runs from a link; cloud save exists bu; last commit: 2026-07-09 UTC, 085c4cd. Deployment/site: https://fable-survival.vercel.app — READY; also has the compiled site wrapper at /games/fable-survival/.
- [SYL-Full-Game](https://github.com/JaronKBragg7337/SYL-Full-Game) — Space You Land — world-scale space game foundation: multiple planets, seamless surface-to-space traversal; last commit: 2026-08-16 UTC, 8db1f2d. Deployment/site: No separate homepage or Vercel deployment found; Heartbeat has a site build at /games/syl/, but separate repo lineage is not verified.
- [World-Printer-Lab-For-3D-Worlds](https://github.com/JaronKBragg7337/World-Printer-Lab-For-3D-Worlds) — Lab for generating 3D worlds, with a versioned inventory of what each build produced.; last commit: 2026-07-24 UTC, 922b0c7. Deployment/site: https://world-printer-lab-for-3-d-worlds.vercel.app — READY standalone lab; separate from /3DPrinterAsset/ and no site route found.
- [Pirate-World-Sea-Of-Fortune-](https://github.com/JaronKBragg7337/Pirate-World-Sea-Of-Fortune-) — Three.js pirate world with a Supabase backend. The database project is currently paused.; last commit: 2026-07-11 UTC, 5b3a81d. Deployment/site: https://pirate-world-sea-of-fortune.vercel.app — deployment ERROR; no Heartbeat route; see inactive Supabase entry.
- [New-Age-Of-War](https://github.com/JaronKBragg7337/New-Age-Of-War) — Unreal Engine C++ war game.; last commit: 2026-07-13 UTC, 0e81fa4. Deployment/site: No browser deployment found; this is an Unreal project without a packaged browser build.
- [the-current](https://github.com/JaronKBragg7337/the-current) — An autonomous deterministic civilization in a Three.js spectator world; last commit: 2026-07-24 UTC, 1126dec. Deployment/site: https://jaronkbragg7337.github.io/the-current/ — live homepage metadata; no Heartbeat route match confirmed.
- [the-defender-3d](https://github.com/JaronKBragg7337/the-defender-3d) — The Defender — 3D Courtroom Strategy Simulator. Built with React, Tailwind, Framer Motion, and React Thre; last commit: 2026-07-14 UTC, e7be7fe. Deployment/site: https://jaronkbragg7337.github.io/the-defender-3d/ — live per prior route audit; framed at /games/the-defender-3d/.
- [cyber-trench-overdrive](https://github.com/JaronKBragg7337/cyber-trench-overdrive) — Cyber-Trench Overdrive — A fast-paced cyberpunk Three.js endless trench flyer / runner game. Neon visuals; last commit: 2026-07-16 UTC, ca3b833. Deployment/site: https://cyber-trench-overdrive.vercel.app — READY; framed at /games/cyber-trench-overdrive/.
- [the-necklace-show](https://github.com/JaronKBragg7337/the-necklace-show) — An interactive Three.js story and open experiment in one-prompt cinematic production.; last commit: 2026-08-12 UTC, ec61618. Deployment/site: https://jaronkbragg7337.github.io/the-necklace-show/ — live per prior route audit; framed at /games/the-necklace-show/.
- [asset-pack-ue-threejs-blender-unity](https://github.com/JaronKBragg7337/asset-pack-ue-threejs-blender-unity) — 38 free CC0 modular building + prop assets for Unreal, Unity, three.js and Blender. Procedurally generate; last commit: 2026-07-25 UTC, f5a53ea. Deployment/site: https://jaronkbragg7337.github.io/asset-pack-ue-threejs-blender-unity/ — live homepage metadata; no Heartbeat route found.
- [rift-clash](https://github.com/JaronKBragg7337/rift-clash) — A browser-based League of Legends-style MOBA. 16 champions, full Summoner's Rift-style map, bots, and a f; last commit: 2026-07-26 UTC, 72b45cf. Deployment/site: https://rift-clash.vercel.app — READY; framed at /games/rift-clash/; network multiplayer remains unverified.
- [livi-organism](https://github.com/JaronKBragg7337/livi-organism) — Persistent AR artificial organism companion with cellular metabolism, adaptive behavior, bonding, growth,; last commit: 2026-07-30 UTC, 2dfcfe7. Deployment/site: https://livi-organism.vercel.app — READY standalone deployment; no Heartbeat route found.
- [spectral-gt-rs](https://github.com/JaronKBragg7337/spectral-gt-rs) — Detailed CC0 game-oriented sports car asset with an interactive GitHub Pages showcase; last commit: 2026-08-01 UTC, 34499c5. Deployment/site: https://JaronKBragg7337.github.io/spectral-gt-rs/ — live homepage metadata; no Heartbeat route found.
- [pam-continuum](https://github.com/JaronKBragg7337/pam-continuum) — PAM Continuum: an evergreen, provenance-first intelligence workspace and visual command center; last commit: 2026-09-23 UTC, 6dc34fc. Deployment/site: https://jaronkbragg7337.github.io/pam-continuum/ — live homepage metadata; no connection to the site's /pam/ dashboard was confirmed.
- [northstar-addressable-world](https://github.com/JaronKBragg7337/northstar-addressable-world) — Northstar first-person parkour game and addressable-world engine proof; last commit: 2026-08-02 UTC, f2dfd99. Deployment/site: https://jaronkbragg7337.github.io/northstar-addressable-world/ — live; framed at /games/northstar-addressable-world/.
- [wasteland-commons](https://github.com/JaronKBragg7337/wasteland-commons) — CC0 cross-platform cooperative wasteland game with deterministic grid inspection and multiplayer relay; last commit: 2026-08-02 UTC, 3b1d196. Deployment/site: https://wasteland-commons.vercel.app — READY; framed at /games/wasteland-commons/; production health reports local-memory persistence.
- [rustfall](https://github.com/JaronKBragg7337/rustfall) — RUSTFALL — a deterministic post-apocalyptic wasteland survival engine. Three.js vertical slice: roaming w; last commit: 2026-08-15 UTC, 610f4ad. Deployment/site: No separate homepage or Vercel deployment found; Heartbeat has /games/rustfall/ and its multiplayer data uses the active Heartbeat Supabase project.
- [Air-Vehicles-](https://github.com/JaronKBragg7337/Air-Vehicles-) — Flight vehicles built with Vite and TypeScript.; last commit: 2026-08-03 UTC, 830dd98. Deployment/site: https://air-vehicles-vtol.vercel.app — Vercel deployment READY; no Heartbeat route. The prior game inventory still flags the browser build/base as unresolved.
- [MindGames](https://github.com/JaronKBragg7337/MindGames) — A mobile-first Three.js experiment in live recursive worlds, traversable screens, folding architecture, a; last commit: 2026-08-09 UTC, 1b44686. Deployment/site: https://jaronkbragg7337.github.io/MindGames/ — live; framed at /games/mindgames/.
- [signal-drift](https://github.com/JaronKBragg7337/signal-drift) — A tiny neon arcade game with a live Codex pilot; last commit: 2026-08-12 UTC, 74d7092. Deployment/site: https://jaronkbragg7337.github.io/signal-drift/ — live; framed at /games/signal-drift/.
- [parkworks-tycoon](https://github.com/JaronKBragg7337/parkworks-tycoon) — A mobile-friendly 3D amusement-park management game with rides, food, facilities, guests, litter, and CC0; last commit: 2026-08-15 UTC, ec65697. Deployment/site: https://jaronkbragg7337.github.io/parkworks-tycoon/ — live homepage metadata; Heartbeat also has /games/parkworks/.
- [Frontier-Empires](https://github.com/JaronKBragg7337/Frontier-Empires) — Three.js real-time strategy game and AI-model war history.; last commit: 2026-08-18 UTC, 7b12902. Deployment/site: No deployment found in Vercel or repository homepage metadata; prior game inventory says a browser build is still needed.
- [robot-evolution-lab](https://github.com/JaronKBragg7337/robot-evolution-lab) — MEC-01 mobile browser robot evolution lab.; last commit: 2026-08-26 UTC, 902591a. Deployment/site: https://jaronkbragg7337.github.io/robot-evolution-lab/ — live; framed at /games/robot-evolution-lab/.

#### No site page or deployment was found in the checked sources

- [persistent-memory-substrate](https://github.com/JaronKBragg7337/persistent-memory-substrate) — A Persistent Memory Substrate (PMS) is a system class where historical state persists and new state is ad; last commit: 2025-12-13 UTC, 8e1f92e. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Atomic-Chronicle-Memory-Chain-](https://github.com/JaronKBragg7337/Atomic-Chronicle-Memory-Chain-) — a Python prototype combining a local blockchain ledger, tokenized wallet system, Asteroids-style game, an; last commit: 2025-12-16 UTC, c55c407. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [ATOMIC-CHRONICLE-v4.0-A-world-you-want-or-a-world-of-worlds-](https://github.com/JaronKBragg7337/ATOMIC-CHRONICLE-v4.0-A-world-you-want-or-a-world-of-worlds-) — Atomic Chronicle v4.0 Summary An append-only execution substrate that records immutable actions and state; last commit: 2025-12-17 UTC, eca57dc. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [ATOMIC-CHRONICLE-v4.0-A-World-You-Want-Or-a-World-of-Worlds](https://github.com/JaronKBragg7337/ATOMIC-CHRONICLE-v4.0-A-World-You-Want-Or-a-World-of-Worlds) — 💡 Atomic Chronicle v4.0 Summary An append-only execution substrate that records immutable actions and st; last commit: 2025-12-17 UTC, 32cb02e. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Atomic-World-Chronicle-3.7](https://github.com/JaronKBragg7337/Atomic-World-Chronicle-3.7) — A world you want — or a world of worlds. Atomic Chronicle v4.0 is an append-only execution and memory sub; last commit: 2025-12-17 UTC, 1af12c2. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [AETHERSPAN-v1.1-Anonymous-Teleoperation-Bridge](https://github.com/JaronKBragg7337/AETHERSPAN-v1.1-Anonymous-Teleoperation-Bridge) — AETHERSPAN is a local-first, anonymous WebSocket bridge for real-time teleoperation. It maps controller i; last commit: 2025-12-17 UTC, b56018d. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Reflector-To-API-Bridges-](https://github.com/JaronKBragg7337/Reflector-To-API-Bridges-) — Connects to an existing AETHERSPAN WebSocket endpoint; last commit: 2025-12-17 UTC, 4f58caa. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Perspective-Environmental-framework-Exercise](https://github.com/JaronKBragg7337/Perspective-Environmental-framework-Exercise) — A short framing exercise that reveals how people (and AI systems) naturally process ambiguous prompts — n; last commit: 2026-02-23 UTC, 9ec1b1a. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [YES-NO-Environment-Perspective-You-Myself-Observer-Paradox](https://github.com/JaronKBragg7337/YES-NO-Environment-Perspective-You-Myself-Observer-Paradox) — This book has four names because it lives in four states at once. YES / NO — the binary that refuses puri; last commit: 2026-02-23 UTC, 066b3ab. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Neuro-consciousness-and-chemistry-](https://github.com/JaronKBragg7337/Neuro-consciousness-and-chemistry-) — Complicated ; last commit: 2026-03-09 UTC, 551bffb. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [THE-ENVIRONMENT-CONSTRAINT-INTELLIGENCE-HYPOTHESIS-ECIH-](https://github.com/JaronKBragg7337/THE-ENVIRONMENT-CONSTRAINT-INTELLIGENCE-HYPOTHESIS-ECIH-) — Complicated. ; last commit: 2026-03-09 UTC, 9eedd82. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [My-Influence-on-others-](https://github.com/JaronKBragg7337/My-Influence-on-others-) — A documentation. A timestamp. A record.; last commit: 2026-03-10 UTC, 0e688b4. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [THEY-NEVER-LEFT](https://github.com/JaronKBragg7337/THEY-NEVER-LEFT) — A Pattern Recognition Hypothesis on Ancient Civilizations, Hidden Evolution, and What We Call Aliens by J; last commit: 2026-03-12 UTC, 20ebe66. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [The-Structural-Conflict](https://github.com/JaronKBragg7337/The-Structural-Conflict) — Timeline of some history and patterns of possibilities ; last commit: 2026-03-27 UTC, f4044c2. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [EchosOrchestra](https://github.com/JaronKBragg7337/EchosOrchestra) — Empty. Created and never used.; last commit: no commit SHA returned; GitHub last-push metadata 2026-04-24 UTC. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [signal-pebble-echo-2917](https://github.com/JaronKBragg7337/signal-pebble-echo-2917) — Tiny test repo for connector push verification.; last commit: 2026-05-10 UTC, 87e541f. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [grok-test-dummy-penguin-2026](https://github.com/JaronKBragg7337/grok-test-dummy-penguin-2026) — A dummy test repository created by Grok AI; last commit: 2026-05-10 UTC, e67bbff. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [memory-as-spatial-arrangement](https://github.com/JaronKBragg7337/memory-as-spatial-arrangement) — A working hypothesis on holding memory as a spatial arrangement rather than a linear sequence — and why a; last commit: 2026-05-26 UTC, b21014d. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [emergence-structure-that-grows](https://github.com/JaronKBragg7337/emergence-structure-that-grows) — A working note on emergence in trained systems — that internal structure is grown and discovered, not des; last commit: 2026-05-26 UTC, a9bed85. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [live-reference-principle](https://github.com/JaronKBragg7337/live-reference-principle) — A formal argument that a system's constraints, goals, and signals are only valid while they stay connecte; last commit: 2026-05-28 UTC, 443eefb. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Keava-Owent](https://github.com/JaronKBragg7337/Keava-Owent) — Architecture for a persistent, live-reference, resource-accountable agent loop that generates its own wor; last commit: 2026-09-24 UTC, 6c1a5d4. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [theater-vs-record-trump-drug-clemency](https://github.com/JaronKBragg7337/theater-vs-record-trump-drug-clemency) — Analysis of Trump’s 2025–26 second-term anti-narcotics military campaign versus selective clemency for dr; last commit: 2026-05-30 UTC, c4e350e. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [ai-workforce-xai-openai](https://github.com/JaronKBragg7337/ai-workforce-xai-openai) — A self-documenting recurring-task system built on Grok (xAI) and ChatGPT (OpenAI) as co-workers. Live-ref; last commit: 2026-05-31 UTC, 9e93a0b. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [testing-ai-workforce-loop](https://github.com/JaronKBragg7337/testing-ai-workforce-loop) — Testing AI workforce loop; last commit: 2026-05-31 UTC, 7e8071c. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [ai-workforce](https://github.com/JaronKBragg7337/ai-workforce) — Specification for a self-documenting recurring-task system that runs on consumer AI apps - no server, no ; last commit: 2026-06-01 UTC, d51031f. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [heartbeat-test](https://github.com/JaronKBragg7337/heartbeat-test) — Pulse check for the AI Heartbeat Engine.; last commit: 2026-06-01 UTC, 7cb8e78. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [ai-anonymous-task-force](https://github.com/JaronKBragg7337/ai-anonymous-task-force) — Stub. README only.; last commit: 2026-06-02 UTC, 93b9e38. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [autonomous-agent-os](https://github.com/JaronKBragg7337/autonomous-agent-os) — Self-healing, autonomous multi-AI agent operating system — Supervisor + Workers + Durable Execution + Cri; last commit: 2026-06-03 UTC, eb7d891. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [ai-heartbeat-engine](https://github.com/JaronKBragg7337/ai-heartbeat-engine) — A proven, portable substrate for autonomous multi-AI work on a single machine — with a human stop-channel; last commit: 2026-06-03 UTC, 309a706. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [SYL-Testing-pvp](https://github.com/JaronKBragg7337/SYL-Testing-pvp) — PvP test bed for Space You Land - a small Node server and client.; last commit: 2026-06-07 UTC, f1a4361. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [The-Last-Theory.-](https://github.com/JaronKBragg7337/The-Last-Theory.-) — A short theory note.; last commit: 2026-06-12 UTC, 3de8f4f. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Pieces-Of-My-Life-](https://github.com/JaronKBragg7337/Pieces-Of-My-Life-) — Personal record.; last commit: 2026-06-12 UTC, 26d3851. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [SpaceYouLand](https://github.com/JaronKBragg7337/SpaceYouLand) — SYL — Space You Land: a persistent first-person space game (Unreal Engine). Fortis outpost vertical slice; last commit: 2026-06-20 UTC, 6edf667. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [agent-workbench](https://github.com/JaronKBragg7337/agent-workbench) — Local-first control plane for deterministic workers and AI adapters.; last commit: 2026-06-30 UTC, b46119d. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Comedy-Skits](https://github.com/JaronKBragg7337/Comedy-Skits) — Purpose not described in GitHub metadata or README.; last commit: 2026-06-22 UTC, 1fb22ca. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [reality-skin-engine](https://github.com/JaronKBragg7337/reality-skin-engine) — Specification-first skinning engine for reworlding existing scenes: design principles, system architectur; last commit: 2026-07-01 UTC, 8e0f7ac. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [zeus-ai](https://github.com/JaronKBragg7337/zeus-ai) — Local-first AI workbench: FastAPI + React over Ollama with local RAG, desktop tools, a ledger and heartbe; last commit: 2026-08-11 UTC, 67cb0b5. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [pictures-Screenshots-](https://github.com/JaronKBragg7337/pictures-Screenshots-) — Purpose not described in GitHub metadata or README; near-name Pictures-screenshots repo exists, relations; last commit: 2026-07-03 UTC, f1732c1. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Pictures-screenshots](https://github.com/JaronKBragg7337/Pictures-screenshots) — Personal media library — photos and screenshots accessible to AI assistants and collaborators.; last commit: 2026-08-17 UTC, 367682e. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [physics-lab-sandbox](https://github.com/JaronKBragg7337/physics-lab-sandbox) — Visual physics simulator for energy and mechanism experiments — playable from any phone browser. Built by; last commit: no commit SHA returned; GitHub last-push metadata 2026-07-03 UTC. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Summary-Of-repos-Memory-linker](https://github.com/JaronKBragg7337/Summary-Of-repos-Memory-linker) — Machine-readable map of every repo on this account, built for Zeus AI and rendered as a Three.js data cen; last commit: 2026-07-12 UTC, 9968857. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Orchestra-Financial-](https://github.com/JaronKBragg7337/Orchestra-Financial-) — Placeholder for the financial arm of Orchestra. README and licence only.; last commit: 2026-07-12 UTC, 91c2e84. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [market-architect](https://github.com/JaronKBragg7337/market-architect) — TypeScript monorepo for market structure experiments, with a vitest suite.; last commit: 2026-07-14 UTC, 8e3c118. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Circuit-Sim-3D-Mobile-Lab-v2](https://github.com/JaronKBragg7337/Circuit-Sim-3D-Mobile-Lab-v2) — Mobile-first 3D circuit simulator that runs in the browser.; last commit: 2026-07-17 UTC, 620723a. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [orchestra](https://github.com/JaronKBragg7337/orchestra) — Public archive of Orchestra AI intelligence collection prompts and daily response logs; last commit: 2026-07-19 UTC, d60f790. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Emergence-Forge-By-GPT-5.6-Luna](https://github.com/JaronKBragg7337/Emergence-Forge-By-GPT-5.6-Luna) — Cellular-automata lab, conjecture lab and pattern miner, with recorded results. Research that actually ra; last commit: 2026-07-22 UTC, c35b77a. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [tessera-worldkit](https://github.com/JaronKBragg7337/tessera-worldkit) — An AI-readable world-building framework and original asset pack. Ships the placement contract, not just t; last commit: 2026-07-25 UTC, 9abd36d. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [aetherforge-threejs-mod-studio](https://github.com/JaronKBragg7337/aetherforge-threejs-mod-studio) — Three.js asset mod-pack editor and cinematic ruin showcase; last commit: 2026-07-27 UTC, 0625c3f. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [The-Thinking-Gym](https://github.com/JaronKBragg7337/The-Thinking-Gym) — Written exercises for thinking through problems. No code.; last commit: 2026-07-31 UTC, 875cf38. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Phone-AI-App-builds](https://github.com/JaronKBragg7337/Phone-AI-App-builds) — Apps built entirely from a phone, collected into one page.; last commit: 2026-07-30 UTC, ca82eae. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Jaron-Game-World-Foundation](https://github.com/JaronKBragg7337/Jaron-Game-World-Foundation) — Shared foundation layer for the game worlds - a registry of parts and agent instructions the other world ; last commit: 2026-07-31 UTC, c7f60d7. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [cinematic-inspection-lab](https://github.com/JaronKBragg7337/cinematic-inspection-lab) — Camera and lighting inspection rig with an asset registry, scene and sequence manifests, constraints and ; last commit: 2026-08-01 UTC, abd9df0. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [surface-material-lab](https://github.com/JaronKBragg7337/surface-material-lab) — A standalone Three.js lab for testing real photographic surface materials in simple worlds.; last commit: 2026-08-01 UTC, a104383. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [showcase-world](https://github.com/JaronKBragg7337/showcase-world) — A texture-forward, inspection-ready Three.js major-city showcase with real material maps, deterministic g; last commit: 2026-08-02 UTC, 864fb52. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [worldbuilding-lab](https://github.com/JaronKBragg7337/worldbuilding-lab) — Worldbuilding doctrine and texture standards with a working reference build - the style guide the other w; last commit: 2026-08-04 UTC, 183018f. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [SYL-Neighborhood](https://github.com/JaronKBragg7337/SYL-Neighborhood) — (grok 4.5 version); last commit: 2026-08-04 UTC, 48df4d0. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [The-Free-Online-Neighborhood-](https://github.com/JaronKBragg7337/The-Free-Online-Neighborhood-) — Shared online neighbourhood built on Next.js with a Drizzle database layer and a background worker.; last commit: 2026-08-04 UTC, 9ca82a6. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Online-NPC-City-](https://github.com/JaronKBragg7337/Online-NPC-City-) — Early scaffold of the living NPC town idea. Superseded by ashgrove-npc-online.; last commit: 2026-08-04 UTC, f3b41ce. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [ashgrove-npc-online](https://github.com/JaronKBragg7337/ashgrove-npc-online) — A living town where NPCs and online players share the same world - jobs, households, growth. Built on the; last commit: 2026-08-06 UTC, 9c8efa2. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [THE-SHIFTING](https://github.com/JaronKBragg7337/THE-SHIFTING) — Vite + TypeScript experiment with an automated deploy.; last commit: 2026-08-05 UTC, 822557b. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [Movie-Theater-Three.js-Asset-](https://github.com/JaronKBragg7337/Movie-Theater-Three.js-Asset-) — Three.js movie theater asset with a Playwright test rig. Feeds the cinema inside Heartbeat Observatory.; last commit: 2026-09-24 UTC, f94de95. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [vibecoding-training-grounds-](https://github.com/JaronKBragg7337/vibecoding-training-grounds-) — Vite + TypeScript training grounds with agent instructions and an automated deploy.; last commit: 2026-08-09 UTC, db381be. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [direct-binary-emission-system](https://github.com/JaronKBragg7337/direct-binary-emission-system) — Deterministic direct-byte emission, validation, recall, and mutation for PE, ELF, WASM, boot sectors, and; last commit: 2026-08-09 UTC, ebb47e4. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [accumulation-sort](https://github.com/JaronKBragg7337/accumulation-sort) — Every repo on this account sorted by one question: does it run without you, keep what happened, and show ; last commit: 2026-09-24 UTC, f6b695c. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [fed-not-filled](https://github.com/JaronKBragg7337/fed-not-filled) — A working hypothesis: intelligence as something maintained daily rather than compressed once. A trained m; last commit: 2026-08-12 UTC, 75181c6. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [atlas-field-unit](https://github.com/JaronKBragg7337/atlas-field-unit) — Mobile-first mechanically assembled Three.js field android with CC0 PBR materials.; last commit: 2026-08-12 UTC, 1c0a03b. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [origin-works](https://github.com/JaronKBragg7337/origin-works) — A Three.js world where manufactured things are actually manufactured — persistent identity, real assembly; last commit: 2026-08-15 UTC, 271e26d. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [MachineManager](https://github.com/JaronKBragg7337/MachineManager) — Persistent autonomous Machine Manager system: job registry, specialist workers, multi-signal health, refe; last commit: 2026-09-01 UTC, f7b14ff. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [official-watch-briefs](https://github.com/JaronKBragg7337/official-watch-briefs) — Full-text archive of Grok official-account security watches. Private log so daily briefs are readable wit; last commit: 2026-09-23 UTC, e7cb003. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [MachineManager-RevenueLab](https://github.com/JaronKBragg7337/MachineManager-RevenueLab) — Public evidence-first control plane for persistent AI-assisted work; first experiment is Bitcoin proof-of; last commit: 2026-09-02 UTC, 07927d2. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
- [binary-bridge](https://github.com/JaronKBragg7337/binary-bridge) — A fast, on-device translator for text, binary, hexadecimal, and decimal bytes.; last commit: 2026-09-02 UTC, edd0576. No repo homepage or matching Vercel deployment was found; other hosting is not ruled out.
## 2. Everything that runs on its own

### Supabase jobs and functions

- **Project Heartbeat** (`ygjpnvrwhkrowkrskftk`) is `ACTIVE_HEALTHY`. The other three projects are inactive; their owners and site connections are in section 4.
- `habitat-world-heartbeat` runs every minute (`* * * * *`) in Supabase `pg_cron` and calls `habitat_world_heartbeat()`. It advances the Habitat simulation in the `habitat_*` tables; it uses database compute, not a paid model API.
- `the-current-tick` runs every 10 minutes (`*/10 * * * *`) in `pg_cron`, calling the `the-current-tick` Edge Function (v7, JWT required). It advances the `the_current_*` simulation tables.
- `world3-tick` Edge Function v3 is active with JWT verification off. It is publicly callable; its endpoint can advance the World 3 simulation. I found no Supabase cron schedule for it; the daily writer is the Ashgrove GitHub Action below.
- The daily Ashgrove script calls `world3_advance_day()` and updates `world3_world`. It can also rebuild/validate the town model. Its workflow runs at 05:23 UTC once daily. The prior local audit saw five recent failed runs, last tied to the database outage; I could not retrieve the 2026-09-24 run outcome through the connected GitHub tool, so today’s run remains unverified.

### Vercel and GitHub schedules

- GitHub Action `Enrich world spaces` calls `/api/enrich-world-spaces` hourly at minute 7 UTC. It reads up to 12 stale/missing GitHub repository records from `world_spaces`, fetches public GitHub metadata, and writes metadata back through `set_world_space_repo_metadata`. This uses network and database resources, not a model API.
- Vercel also schedules the same route daily at 05:00 UTC as a fallback. The twice-scheduled job may often have nothing stale to do after the hourly pass.
- `/api/enrich-world-spaces` only checks `CRON_SECRET` when that variable exists. A fresh read-only Vercel environment-name check on 2026-09-24 found no `CRON_SECRET`, so the route appears callable without authentication. `SITE_EDITOR_GITHUB_TOKEN` is present by name. No request was sent to this write-capable endpoint.
- `world3/town/tools/advance.js` is the Ashgrove daily writer. It uses the active Heartbeat project and calls the `world3_advance_day` RPC with the daily clock job’s service credential.

### Windows Task Scheduler on the MSI

Status and last-result values are from the local machine scan on 2026-09-24. A result of `0` is success; `2147942402` is Windows “file not found.”

| Task | Schedule | Current state and result | What it touches |
|---|---|---|---|
| AgentWorkbench-Scheduler | Every 15 minutes | Ready, but last run failed (`2147942402`) | AgentWorkbench scheduler tick; points at a removed PowerShell 7.6.3 WindowsApps executable. |
| AgentWorkbench-Server | At user logon | Ready, but last run failed (`2147942402`) | AgentWorkbench server; same missing executable. The scripts still exist under `C:\Users\lilli\Projects\agent-workbench\scripts\`. |
| Trade Proposer | Every 2 hours | Ready; last result 0 | Calls DeepSeek and writes new proposals to the trade queue. |
| Trade Verifier | Every 5 minutes | Ready; last result 0 | Rechecks proposals and writes verification state. |
| Trade Executor | Every 5 minutes | Ready; last result 0 | Checks approved decisions and updates the trade ledger; current live page showed 0 approved at 10:20 AM. |
| DB Size Check | Every hour | Ready; last result 0 | Reads Heartbeat database size and warns locally at 75% of the 8 GB disk. |
| Revenue Desk Daily | Daily, 7:03 AM local | Ready; last result 0 | Runs the local Revenue Desk scan/export workflow. |
| Watch Codex Writer | Daily, 3:00 AM local (moved from 7:30 AM on 2026-10-15) | Ready; last result 0 | Writes the daily Codex watch report. |
| Watch DeepSeek Reader | Daily, 3:40 AM local (moved from 9:00 AM on 2026-10-15) | Ready; last result 0 on 2026-09-24 | Runs the DeepSeek reader, records a run log, then stages, commits, and pushes the Watch project. The PowerShell script does not stop if the Python model request fails; the scheduled-task result therefore does not prove the model call worked. This is an existing scheduled external write, not performed during this audit. |
| OpenClaw Gateway | At user logon | Ready; last result 0 | Starts the local OpenClaw gateway. Its listener is active on `127.0.0.1:18789`. |
| Polymarket MCP | At user logon | Running | Local connector on `127.0.0.1:8765`; each tool call writes `tool.started` plus `tool.completed` into `qwen_events` through `qwen_agent_ingest_event`. |
| Fly Brain; Fly School (five tasks); Fly Watcher | At logon and/or one-shot time | All disabled | Fly brain/school loops and watcher are off. |
| Qwen Remote Bridge | At user logon | Disabled | Remote Qwen bridge is off as a scheduled task. |
| OpenClaw Paper Gateway; Paper Sync | At user logon | Both disabled | Local paper-trading gateway and sync are off. |
| Unfinished Island hourly world worker | Hourly | Disabled | Local Unfinished Island world worker is off. |
| Heartbeat Courier | Several times daily | Disabled | No current courier loop. |
| Desktop Commander Remote | At logon | Ready; last result 1 | Startup task did not report success; exact impact not established. |

Other listeners found on the MSI: Ollama at `127.0.0.1:11434`, Grok Machine MCP at `127.0.0.1:3001`, Polymarket MCP at `127.0.0.1:8765`, and OpenClaw at `127.0.0.1:18789`. Port `19789` (paper gateway) was closed. The process list showed eight `Grok Bot` entries; that count alone does not establish eight independent loops. These are local services, not public website pages.

**Database write that is still running:** `qwen_events` is about 1,511 MB. In a one-hour database query on 2026-09-24 it received 683 `tool.started` rows and 683 `tool.completed` rows; 439 completions were marked failed and 244 succeeded. The active Windows `Polymarket MCP` task is the writer: its local `server.py` wraps each connector call and sends both events to `qwen_agent_ingest_event`. This confirms the connector log source despite the Qwen table name and the disabled Qwen Remote Bridge. The brief says this table is now capped; I did not inspect or test the retention cap itself. At the measured rate, it receives roughly 33,000 event rows per day, so confirm the cap keeps total storage bounded.

### Vercel projects found

The Vercel account has 12 projects. Latest deployment state is from Vercel’s deployment list on 2026-09-24; the deployment hostnames are Vercel-generated addresses, while only the main site’s custom domain was independently confirmed in this audit.

| Vercel project | Project domains (read from Vercel) | Latest production deployment | Site connection |
|---|---|---|---|
| `heartbeatobservatory` | `heartbeatobservatory.com`, `www.heartbeatobservatory.com`, `project-7mya9.vercel.app` | READY, `d45b078`, `heartbeatobservatory-py6pnihpi-kylerbragg73-2101s-projects.vercel.app` | Main site. |
| `air-vehicles-vtol` | `air-vehicles-vtol.vercel.app` | READY, `830dd98`, `air-vehicles-vtol-lyybqtutp-kylerbragg73-2101s-projects.vercel.app` | Air Vehicles deployment; not yet framed by a site route. |
| `wasteland-commons` | `wasteland-commons.vercel.app` | READY, `58a1165`, `wasteland-commons-ebm2hpi55-kylerbragg73-2101s-projects.vercel.app` | Embedded by `/games/wasteland-commons/`. |
| `livi-organism` | `livi-organism.vercel.app` | READY, `2dfcfe7`, `livi-organism-gvxpwmwui-kylerbragg73-2101s-projects.vercel.app` | Separate deployment; no site route found. |
| `rift-clash` | `rift-clash.vercel.app` | READY, `72b45cf`, `rift-clash-ft0avnsfp-kylerbragg73-2101s-projects.vercel.app` | Embedded by `/games/rift-clash/`. |
| `world-printer-lab-for-3-d-worlds` | `world-printer-lab-for-3-d-worlds.vercel.app` | READY, `922b0c7`, `world-printer-lab-for-3-d-worlds-b1ba3l5fb.vercel.app` | Separate printer lab deployment; site `/3DPrinterAsset/` is in the main repo. |
| `cyber-trench-overdrive` | `cyber-trench-overdrive.vercel.app` | READY, `cyber-trench-overdrive-5s65lloe5-kylerbragg73-2101s-projects.vercel.app` | Embedded by `/games/cyber-trench-overdrive/`. |
| `pirate-world-sea-of-fortune` | `pirate-world-sea-of-fortune.vercel.app` | **ERROR**, `pirate-world-sea-of-fortune-rjf3jk3qo.vercel.app` | No Heartbeat site route; its Supabase project is inactive. |
| `fable-survival` | `fable-survival.vercel.app` | READY, `085c4cd`, `fable-survival-fxy261d44-kylerbragg73-2101s-projects.vercel.app` | Separate game deployment; the site also hosts a compiled wrapper/build at `/games/fable-survival/`. |
| `v0-framing-lens-project` | `v0-framing-lens-project.vercel.app` | No deployment returned | No site route found. |
| `v0-engine-of-division-summary` | `v0-engine-of-division-summary.vercel.app` | READY, `v0-engine-of-division-summary-64f09buww.vercel.app` | No site route found. |
| `v0-ai-gateway-starter` | `v0-ai-gateway-starter-livid.vercel.app` | No deployment returned | No site route found. |

The MSI has a `VERCEL_TOKEN` entry in `C:\Users\lilli\.secrets\keys.env`; only its name and presence were checked. With it, read-only Vercel API calls verified the domains and environment-variable names below. No values were read or printed.

| Vercel project | Environment-variable names returned |
|---|---|
| `heartbeatobservatory` | `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY`, `GROK_API_KEY`, `OPENAI_API_KEY`, `PAM_BRIDGE_TOKEN`, `PAM_BRIDGE_URL`, `PAM_RUNTIME_BRIDGE_TOKEN`, `PAM_RUNTIME_BRIDGE_URL`, `PERPLEXITY_API_KEY`, `SITE_EDITOR_GITHUB_TOKEN`, `WORLD_SPACE_ENRICH_SECRET` |
| `air-vehicles-vtol`, `rift-clash`, `world-printer-lab-for-3-d-worlds`, `cyber-trench-overdrive`, `v0-engine-of-division-summary`, `v0-ai-gateway-starter` | No environment-variable names returned. |
| `wasteland-commons` | `SUPABASE_URL` |
| `livi-organism`, `v0-framing-lens-project` | `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, `POSTGRES_DATABASE`, `POSTGRES_HOST`, `POSTGRES_PASSWORD`, `POSTGRES_PRISMA_URL`, `POSTGRES_URL`, `POSTGRES_URL_NON_POOLING`, `POSTGRES_USER`, `SUPABASE_ANON_KEY`, `SUPABASE_JWT_SECRET`, `SUPABASE_PUBLISHABLE_KEY`, `SUPABASE_SECRET_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_URL` |
| `pirate-world-sea-of-fortune` | `VITE_SUPABASE_ANON_KEY`, `VITE_SUPABASE_URL` |
| `fable-survival` | `GITHUB_TOKEN`, `SUPABASE_SECRET_KEY`, `SUPABASE_URL` |

The main site has no `CRON_SECRET` variable name. `GEMINI_API_KEY`, `GROK_API_KEY`, and `OPENAI_API_KEY` are configured by name, but no direct caller for them was found in the current site API routes. They may belong to another local service or bridge; that use is not established here.

### Cloudflare visibility

Public DNS delegates `heartbeatobservatory.com` to `raquel.ns.cloudflare.com` and `wesley.ns.cloudflare.com`. Google Public DNS returned apex A record `76.76.21.21` and `www` CNAME `cname.vercel-dns.com` on 2026-09-24. No `CLOUDFLARE_API_TOKEN` name is present in the checked MSI secrets file, and no Cloudflare connector is available in this session. I could see public DNS answers only; Cloudflare’s zone record dashboard, Workers and routes, Pages projects, R2 buckets, cache rules, and other account settings remain inaccessible from this MSI session.

## 3. Everything that can spend money or API credits

“Idle” below means no one is browsing the site. The scheduled MSI jobs still run at idle. The current DeepSeek scripts name a model the provider has retired, so their task exit codes do not establish that a model response succeeded.

| Provider / route | Trigger and current limits | Estimated spend with no site visitors |
|---|---|---|
| DeepSeek, local Watch Reader | `Watch DeepSeek Reader` runs daily at 3:40 AM local (moved 2026-10-15) and calls `deepseek-chat` once. `DEEPSEEK_API_KEY` is present by name in `C:\Users\lilli\.secrets\keys.env`. Its prompt size depends on that day’s captures. | **Unverified.** One scheduled model request/day even with no website visitors; the input/token usage and provider billing record were not available. The Python output is logged, but the task’s success result is not a reliable model-call check. |
| DeepSeek, Trade Proposer | Every 2 hours, 12 scheduled runs/day; selects at most 6 candidates/run. The default `both` method can make 2 model requests per candidate, so the code allows up to 144 calls/day. The key name is present locally; it defaults to DeepSeek when the key is set. | **Current code likely fails before generating billable tokens:** it still sends `model: deepseek-chat`, which DeepSeek’s changelog says was discontinued on 2026-07-24. Per-candidate API exceptions are caught and the process can still exit 0. If changed to current DeepSeek Flash, a planning example of 5,000 input + 700 output tokens for all 144 calls is about **$0.17/day off-peak or $0.34/day at peak rates**, before any cache discount. This is a scenario, not measured usage, and excludes the Watch Reader. |
| Perplexity, `/api/news` from `/social/` | Runs after a page request, uses Sonar, caps output at 600 tokens, and returns a 6-hour cache header. No site request means no call. | **$0/day with no visitors.** For scale, one cache miss every six hours would mean 4 calls/day; current Sonar request fees alone are about $0.02–$0.05/day depending on search-context size, plus input/output token charges. Actual cache misses and token counts were not available. |
| Anthropic Claude Haiku, `/api/ask` | Called by explicit player/user questions, including from the Engine NPC dialogue. Output is capped at 300 tokens and `ask_allow` limits a browser/IP to about 3 answers/hour. No prompt means no model call. | **$0/day with no user prompts.** At current published rates, an example 1,000-token question and 300-token answer is about $0.0025; 72 such calls from one IP in a full day would be about $0.18. Actual input length and request totals are unknown. |
| PAM runtime bridge | `/api/pam-chat` stores the message, then forwards it to the configured `PAM_RUNTIME_BRIDGE_URL` with `PAM_RUNTIME_BRIDGE_TOKEN`. The connected provider/model and its usage are behind that bridge. | No automatic site request was found; no user messages means no page-triggered call. If another process polls or invokes the bridge, its cost and cadence remain unverified. `pam-agent-heartbeat` itself calls a Supabase RPC, not a model. |
| OpenAI, Gemini, xAI/Grok | Their key names are set on the main Vercel project, but no direct call to those providers was found in the current site’s API routes. The Engine calls Claude through `/api/ask` on a user prompt. Local Grok Machine MCP on port 3001 calls Ollama at `127.0.0.1:11434`; its inspected source contains no xAI API endpoint. Eight `Grok Bot.exe` processes were present, but their provider usage was not established. | No direct idle spend attributed to the current site code. Ollama uses local compute; any xAI service/API usage by Grok Bot or another local bridge is unverified. |

The two local DeepSeek jobs are configured with `deepseek-chat`. DeepSeek’s [official changelog](https://api-docs.deepseek.com/updates/) says that legacy API name was discontinued on 2026-07-24. Successful output from those jobs is unverified. Its current [model pricing page](https://api-docs.deepseek.com/quick_start/pricing/) lists Flash at $0.15 input/$0.60 output per million tokens off-peak and double those rates at peak. The Watch Reader’s PowerShell wrapper continues to log and push after its Python subprocess, without checking that subprocess’s exit code; its 2026-09-24 task result of 0 and 9:10 AM log timestamp do not prove successful DeepSeek output.

Perplexity’s current [Sonar pricing](https://docs.perplexity.ai/docs/getting-started/pricing) is $1 per million input tokens and $1 per million output tokens, plus a request fee of $5–$12 per 1,000 requests for low–high search context. Anthropic states [Haiku 4.5 pricing](https://www.anthropic.com/news/claude-haiku-4-5) of $1 per million input and $5 per million output tokens. No provider billing dashboard was read, so all daily amounts above are code-based estimates rather than billed totals.

The brief’s claim that Claude and Perplexity roam as background NPCs was not confirmed in the current site code. The Engine renders connected characters and calls Claude only when a user asks through `/api/ask`; the Perplexity route is news. Persistent character rows can remain visible after a player leaves, but the inspected site source did not show those rows running an autonomous paid-model loop. An external NPC worker outside the inspected site and MSI task list remains possible, but is unverified.

## 4. Every database dependency

### Supabase projects

The connected Supabase account returned exactly one active project and three inactive projects on 2026-09-24. The live database has **76 public tables**, one more than the brief’s 75-table snapshot from 2026-09-23; RLS is enabled on all 76. The user-reported Pro upgrade, 8 GB disk, Micro compute, read/write restoration, and replay of 10 offline trades are context. I independently verified the active project and the public trade page; I did not inspect the billing invoice or change database settings.

| Project | What it belongs to | Does a current site/deployment still point at it? |
|---|---|---|
| **Active:** `JaronKBragg7337's Project Heartbeat` (`ygjpnvrwhkrowkrskftk`) | Heartbeat Observatory’s live database and current shared game/world services. | **Yes.** Current site pages and serverless routes use it; public source and the recovered trade-page check agree. |
| **Inactive:** `Pirate World Seas of Fortune` (`uxyrwbdknvykgvxkigzh`) | Pirate World: Sea of Fortune. Its repository configuration names this project and its code uses player, ship, crew, score, and session tables. This game needs the project restored to run. | **No Heartbeat site route.** The separate Vercel project `pirate-world-sea-of-fortune.vercel.app` is in deployment ERROR; its environment-variable names include `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`. Values were not read. |
| **Inactive:** `fable-survival` (`ukguppzfpvdcemyxzdbn`) | Standalone Fable Survival cloud saves/account API. Its repo’s `.env.example` and `SUPABASE.md` name the paused project. | **Standalone deployment: likely yes by source configuration** (`fable-survival.vercel.app`, READY; Vercel has `SUPABASE_URL` and `SUPABASE_SECRET_KEY` names). **Heartbeat wrapper: no.** Its compiled site bundle points at the active Heartbeat project. The bundle’s account/save paths are absent from the main repo’s API routes and the site copy’s `/api/save` returns 404, so cloud save through the Heartbeat wrapper is not working. Environment values were not read. |
| **Inactive:** `wasteland-commons` (`wnwxihhjtoilmcilyyuk`) | Intended optional persistent/multiplayer database for Wasteland Commons. | **The site points to the Wasteland Vercel app, but no live Supabase connection is confirmed.** Its Vercel project has a `SUPABASE_URL` variable name; the current public `/api/health` response says persistence is local memory and shared multiplayer is pending. The environment value was not read, so whether it names this paused ref is unverified. |

### Pages, jobs, tables, and access

“Realtime” below means the table is in the Supabase Realtime publication. The current project publishes 19 tables. The page-to-table map comes from the current GitHub `main` source and the active database function definitions; local background writers are called out separately.

| Tables | Page or job | Reads / writes / live updates |
|---|---|---|
| `surfaces` | Home `/`, `/games/`, `/live-systems/`, `/projects/`, `/social/`, `/video/`, `/admin/` | Directory and page metadata reads; the home and games pages keep a fallback if the read fails. Admin/editor actions can write. |
| `people` | `/social/`, `/admin/`, `/library/`, `/engine/`, `/engine/hub/`, `bubble.js` | Profile/identity reads and edits; used by social, world identity, admin and chat. |
| `posts`, `post_likes`, `post_reposts`, `post_replies`, `post_bookmarks`, `follows` | `/social/` | Feed and relationship reads; visitor actions write likes, reposts, replies, bookmarks, and follows. `posts` is Realtime; the page also subscribes to `agent_events`. |
| `agent_state`, `agent_events` | `/social/`, `/engine/`, `/engine/hub/` | Agent status/event reads; these pages subscribe to live changes. A current writer for every displayed agent was not established. |
| `messages` | `bubble.js` overlay, `/admin/`, Qwen message RPCs | Chat reads/writes use `send_message` and Qwen RPCs. `bubble.js` subscribes on `hb-messages`; `messages` is Realtime. |
| `ask_log` | `/api/ask` via `ask_allow` RPC | `ask_allow` checks and records rate-limit usage; this is not an idle AI loop. |
| `library_books` | `/library/` | Library listing reads; page also reads `people`. |
| `apartments`, `world_characters`, `world_spaces`, `world_props`, `world_admins` | `/engine/`, `/engine/hub/`, `/world2/`, `/projects/` | World, character, apartment, prop, admin, and space reads/writes. The Engine pages subscribe to `apartments`, `world_characters`, `world_spaces`, and `world_props`; `world2` claims repositories and updates presence. |
| `agent_jobs`, `world_protected_zones` | World schema | Present in the active schema, but no direct current-page call or active writer was found in the scanned production source. Their current use is unverified. |
| `pam_instances`, `pam_threads`, `pam_messages` | `/pam/`, `/api/pam-chat` | Dashboard reads; chat writes instance/thread/message records, then forwards to the configured runtime bridge. `pam-agent-heartbeat` calls its RPC. |
| `pam_devices`, `pam_device_tokens` | Qwen agent RPCs | `qwen_agent_poll` and `qwen_agent_ingest_event` reference these for device identity/auth. No token values or row contents were read. These tables are Realtime-published, but a current page subscription was not found. |
| `pam_events`, `pam_action_ledger` | PAM schema | Present, with `pam_events` Realtime-published. No current page/job writer was confirmed in the inspected source. |
| `placements` | `/3DPrinterAsset/` | Printer scene reads/writes placement records and subscribes to live placement updates. |
| `the_current_world`, `the_current_entropy` | `the-current-tick` Edge Function, every 10 minutes; standalone `the-current` viewer | Function reads/writes the current simulation. Both identifiers appear in the active function source. |
| `the_current_era_archives`, `the_current_era_entropy` | The Current era archive schema | Retired-era snapshots/replay data. No separate live page reader was found; archival write timing was not established in the current source. |
| `world3_world`, `world3_seats`, `world3_edits` | `/world3/`, `/world3/town/`, Ashgrove daily workflow | Town reads and player changes use the `world3_*` RPCs; the daily GitHub workflow advances the shared town. Public `world3-tick` also references `people` and `world3_world`. |
| `parkworks_saves` | `/games/parkworks/` save backend | Game save/load table; the site page includes a save-backend script. No independent scheduled writer was found. |
| `rustfall_rooms`, `rustfall_room_leases`, `rustfall_player_sessions`, `rustfall_commands`, `rustfall_events` | `/games/rustfall/` | Game bundle reads/writes room, lease, player, command and event state. All five are Realtime-published; the inspected bundle explicitly subscribes to `rustfall_player_sessions`. |
| `habitat_worlds`, `habitat_actors`, `habitat_bodies`, `habitat_events`, `habitat_controller_sessions`, `habitat_controller_tokens` | `/live-systems/habitat/`, Habitat API routes, one-minute `habitat-world-heartbeat` | Snapshot/action/heartbeat RPCs and the cron update world/actor/body/session state; actions and controller heartbeats record events. These are database-driven simulation calls, not paid model calls. |
| `habitat_model_generations`, `habitat_objects`, `habitat_memories` | Habitat snapshot/schema | Snapshot function reads model-generation/object data. No current writer for model generations or memories was established. |
| `qwen_instances`, `qwen_state`, `qwen_messages`, `qwen_events`, `qwen_runtime_control` | `/qwen/`, Qwen RPCs, local Polymarket MCP | Dashboard reads and subscribes to `qwen_state`, `qwen_events`, and `qwen_messages`; message actions enqueue through RPC. The active Polymarket MCP calls `qwen_agent_ingest_event` for each tool call and writes `qwen_events`. Qwen Remote Bridge is disabled. `qwen_runtime_control` is published, but a current page listener was not confirmed. |
| `desk_queue`, `desk_decisions`, `desk_stats`, `desk_owners` | `/live-systems/revenue/` | Page reads the public queue, statistics, decisions, and owner status. Queue is a read-only mirror of the local Revenue Desk ledger; approval/owner writes stay restricted. |
| `desk_agents`, `desk_tasks` | Revenue Desk schema | Present but closed by RLS/no public policies; no current site page reader or writer was found. |
| `trade_proposals`, `desk_account`, `desk_trades` | `/live-systems/trades/`, local Proposer, Verifier, Executor | Trade page reads queue/account/trade state. Proposer inserts proposals; verifier changes verification state; executor updates placement/ledger state. All three tasks last reported result 0; no trade was submitted during this audit. |
| `paper_state`, `paper_positions`, `paper_trades` | `/live-systems/paper/`, local Paper Gateway/Sync | Page reads paper-trading state. The two local gateway/sync tasks are disabled and port 19789 is closed; no current writer was found. |
| `fly_ground`, `fly_actions` | `/live-systems/flies/` | Page reads ground/action status. Fly Brain and all five Fly School tasks are disabled. |
| `fly_live`, `fly_school` | Fly School schema/page family | No current page query or running scheduled writer was found. `fly_school` is still about 136 MB; its row estimate is stale/zero, so the live row count is not established. |
| `items`, `item_surfaces`, `observable_sources`, `source_layers`, `source_events` | Older observatory/source schema | No current production page/API call or active job was found in the current main tree and scanned task list; these tables may be legacy or used by a separate tool. |

### Realtime publication

The 19 published tables are `agent_events`, `agent_state`, `apartments`, `messages`, `pam_devices`, `pam_events`, `pam_messages`, `placements`, `qwen_events`, `qwen_messages`, `qwen_runtime_control`, `qwen_state`, `rustfall_commands`, `rustfall_events`, `rustfall_player_sessions`, `rustfall_rooms`, `world_characters`, `world_props`, and `world_spaces`. Confirmed listeners are: Engine pages for agent/character/apartment/world updates; the site chat bubble for `messages`; Social for `posts` and `agent_events`; `/3DPrinterAsset/` for `placements`; `/qwen/` for state/events/messages; and Rustfall for player sessions. PAM tables and `qwen_runtime_control` are published, but their current frontend listeners were not found. Rustfall’s other published tables are used by its game backend, but only the player-session subscription was explicit in the bundle scan.

Table sizes from a read-only query: `qwen_events` 1,511 MB (about 25,551 estimated rows), `fly_school` 136 MB, `fly_ground` 7.7 MB, and `fly_live` 1.8 MB; the other listed tables were below 2 MB. Row estimates are PostgreSQL statistics, not exact counts. The one-hour qwen event query and active local writer are recorded in section 2.

## 5. Orphans and ghosts

### Built pages and deployments with no ordinary site path

- **Free Game Hub:** eight finished titles (TRACE, Roll & Reach, The Loop, LATTICE, FLUX, DRIFT, SENTINEL, and TWIST) are published at [the shared GitHub Pages hub](https://jaronkbragg7337.github.io/Free-Game-Hub/). I found no link to that hub from Heartbeat Observatory. They are playable directly, but are undiscoverable from the site’s game directory.
- **Separate Vercel apps with no Heartbeat wrapper:** `air-vehicles-vtol`, `livi-organism`, `world-printer-lab-for-3-d-worlds`, and `v0-engine-of-division-summary` have READY deployments and no matching route in the current site. READY confirms deployment state, not a complete gameplay check. The standalone printer lab overlaps in purpose with the linked `/3DPrinterAsset/` page.
- **Standalone Vercel projects without a production deployment:** `v0-framing-lens-project` and `v0-ai-gateway-starter` had no production deployment in the account response and no Heartbeat route. These are unmatched projects, not confirmed working orphans.
- **Direct-link-only site pages:** `/island/`, `/lab/voice/`, `/pam/`, `/qwen/`, `/chat-neighborhood/`, `/HeartbeatCenter/`, `/space/`, and `/standards/` have no ordinary home-directory link in the checked source/link tree. They are pages in the site repo and were within the earlier public route sweep; “orphan” here means low discoverability, not a broken URL. The Island’s hourly worker is disabled. PAM’s home card is hidden. Keava on Social is marked “Not connected yet.”
- **Exposed internal artifact:** `/worlds-lab/lib/v1/page-template.html` is publicly served but is not a visitor destination. It looks like a development template.
- **Games whose separate backends are unavailable:** Pirate World has no Heartbeat wrapper and its Vercel deployment is ERROR while its Supabase project is inactive. Fable’s standalone deployment is READY but depends on its inactive project; the Heartbeat wrapper’s `/api/save` returns 404. Wasteland Commons is embedded, but its live health response says persistence is local memory and shared multiplayer is pending. These are visible in section 4 as partial or broken dependencies, not functioning orphan games.

### Running or persistent behavior with no confirmed live need

- **`world3-tick`** is an active Edge Function with JWT verification off. I found no current site caller or scheduled job for it; the daily Ashgrove writer uses `world3_advance_day()` instead. Any external caller is unknown, so its necessity and invocation rate remain unverified. The public function is a security finding in section 6.
- **World characters can outlive a player session.** Rows persist and can render after a visitor leaves, matching the “ghost” behavior in the brief. The inspected site code does not show Claude/Perplexity being called in an autonomous NPC loop. No paid idle NPC loop was confirmed; an external worker remains unverified.
- **AgentWorkbench tasks are registered but do not currently run successfully:** both scheduled entries fail with Windows file-not-found because they point to a removed PowerShell 7.6.3 executable. The scripts remain on disk, but the scheduler entries are not evidence of a functioning background service.
- **Disabled loops are not currently active ghosts:** Fly Brain and five Fly School tasks, the Unfinished Island worker, Qwen Remote Bridge, OpenClaw Paper Gateway, and Paper Sync are disabled. Their pages/data may remain, but no task execution was observed during this audit.
- **The minute Habitat heartbeat and 10-minute Current tick continue when nobody is browsing.** They are active by design and write simulation state; both have corresponding live system/viewer pages, so I have not classified them as unnecessary ghosts.
- **Local service activity has different triggers:** Polymarket MCP is listening, and its tool calls write to `qwen_events`; the connector is not scheduled to generate calls on its own. Grok Machine MCP and Ollama are local listeners. The eight Grok Bot processes do not establish an autonomous xAI API loop.

## 6. Top five findings

1. **The largest database table has a high ongoing write rate.** `qwen_events` is about 1.5 GB. In the sampled hour it received 683 starts and 683 completions, with 439 completions marked failed. That is about 32,800 rows/day if the same rate continued. The writer is the active Polymarket MCP connector, not a Qwen model loop. The brief reports that a cap is in place; I did not test whether it keeps total storage bounded. No rows were changed in this audit.
2. **Two write paths lack a confirmed caller gate.** Supabase `world3-tick` is active with JWT verification disabled, and I found no current page or scheduled caller. The Vercel `/api/enrich-world-spaces` route is also scheduled but has no `CRON_SECRET` variable name; its handler appears to accept requests without that secret and can write repository metadata. Review how each route should be authorized before relying on it.
3. **AgentWorkbench’s scheduled services are broken.** Both the 15-minute scheduler and logon server task fail because they reference a PowerShell executable that no longer exists. Their scripts are still present, but the services are not running from those tasks.
4. **The two DeepSeek jobs may report success without usable output.** They send the discontinued `deepseek-chat` model name. The proposer can catch request errors and still exit successfully; the Watch Reader wrapper logs, stages, commits, and pushes after its Python child even if that child fails. The actual provider response and billing remain unverified. DeepSeek’s [changelog](https://api-docs.deepseek.com/updates/) and [current pricing](https://api-docs.deepseek.com/quick_start/pricing/) are linked in section 3.
5. **Several game persistence paths are incomplete.** Pirate World has no Heartbeat route, an ERROR deployment, and an inactive database project. Fable’s standalone source uses its inactive database project, but the deployed environment target was not read; the Heartbeat wrapper’s `/api/save` returns 404. Wasteland is embedded but currently reports local-memory persistence and pending multiplayer. The active trade page itself now loads live data after about seven seconds; it initially shows only “Loading…”.

### Three simple site improvements, held for the end

These are the small changes previously identified. They are recommendations only; no site code was changed during this read-only audit.

1. Fix the Fly School button’s link or action so it opens the intended live classroom/status view.
2. Replace the trade page’s indefinite-looking “Loading…” message with a clear loading state and a retry/error message. The live data arrived after about seven seconds in the signed-out check.
3. Put a compact games list near the top of the home page so visitors can find the games without first scanning the full directory.

**Verified locally:** MSI task registrations and listener ports; selected current-source call paths; the local Grok MCP’s use of Ollama; GitHub repository metadata. No site code, service settings, database rows, or deployments were changed. This requested inventory is the only file written for the audit.

**Verified remotely:** public trade page loaded live queue data; Vercel project domains, deployments, and environment-variable names; Supabase project states, public schema, RLS, Realtime publication, cron jobs, functions, and table sizes; GitHub repository list and current main tree; public DNS answers.

**Still unverified:** provider billing/usage records; Cloudflare account resources beyond public DNS; secret values and the exact target of Wasteland’s `SUPABASE_URL`; any external caller of `world3-tick`; model usage by Grok Bot or a separate NPC worker; whether standalone game multiplayer works in a player session; today’s Ashgrove workflow outcome.
