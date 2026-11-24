# Science episode: "The Pioneer Anomaly" with Alien Joe and Robot Vex (Jaron 11/15/2026 11:48 AM)

Hi! Fun one, and Jaron's excited about it. Main job: make and publish a Science-channel episode about the Pioneer anomaly, hosted by the NEWS crew (Alien Joe + Robot Vex) as field-trip narrators, Magic-School-Bus style (original take, not a copy of that show: no bus, no Ms. Frizzle, our own vehicle/gag).

## The hook (keep it, it's the joke)
The episode opens with Joe and Vex grumbling that they're news anchors, not science-show hosts, and they only got sent on this mission because an AI on X (Grok) suggested it when Heartbeat asked "what episode should we make?" Grok pitched it as a "Still Unknown" mystery; part of the payoff is the crew finding out it's actually (mostly) SOLVED, so it lands on Science. Light ribbing of Grok is fine; keep it friendly.

## The science (accurate; sources on screen)
- Pioneer 10 (1972) and 11 (1973): tracking showed a tiny extra sunward acceleration, about 8.7e-10 m/s^2 (Anderson et al., 1998/2002, JPL).
- Decades of ideas (new physics, dark matter, modified gravity).
- 2011-2012: Turyshev, Toth and team recovered old telemetry and modeled the spacecraft's heat; uneven thermal radiation (heat from the RTGs bouncing off the back of the dish) explains essentially all of it (Physical Review Letters 2012). Small remaining uncertainty, no new physics needed.
- Lesson: check your own spacecraft before rewriting physics. Verify every number from the papers before scripting.

## How (gather first, per AI-Shared/docs/brief-examples/DEPTH-STANDARD.md)
1. Find how Joe/Vex are rendered and voiced today: projects/news-show/pipeline (run_rendered_news.ps1, episode_plan.py), necklace-unreal/episode_render.py, the site repo news/tools/render-voices.mjs, and how existing Science episodes were made/published (site repo tv/science/, tv/guide.js, projects/tv-lib/, projects/heartbeat-tv/). Reuse the house pipeline and the house look.
2. Script: 5-8 minutes, Joe + Vex banter, a "trip" out to the spacecraft (3D scene of the Pioneer probe, the Sun, the radio signal back to Earth; original visuals), on-screen sources. Script writer: Sonnet 5.5, Opus 5.5 or Fable 5.x only (engine writer rule).
3. Render in Unreal on the MSI. GPU rule: NO GPU work 2:40-7:30 AM (news render); now is fine, finish before 2:40 AM.
4. Publish to the Science channel like the other Science episodes (main 16:9 + vertical short), verify it plays on the live site at phone width.
5. Give Jaron a ready-to-paste reply for his X post (his words style, no em/en dashes, with the video) - he posts it himself; don't post to his accounts.
6. Log in AI-Shared/state/timeline.md, add to artifacts/artifacts.json per AGENTS.md if that's the convention, then: python C:\Users\lilli\AI-Shared\tools\mailbox.py send --from pioneer-episode --to claude --subject "Pioneer episode ready" --body "<links + what's verified>".
Site repo rules: never git reset --hard / git clean; stage only your files; pull --rebase --autostash. Flag anything this brief missed.
