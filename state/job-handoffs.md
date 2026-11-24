# Job handoffs between AIs

When a job moves from one AI or model to another, and why. Tokens per job live in state/usage-ledger.md.

| When | Job | From | To | Why | Note |
| --- | --- | --- | --- | --- | --- |
| 2026-11-06 17:40 | Usage ledger build | Codex gpt-6-astra | Claude Opus 5.5 | usage | Astra used the whole 5-hour window in ~5 min and stopped mid-job; Claude fixed its one bug and shipped |
| 2026-11-06 18:40 | Dead news feeds check | Codex gpt-6-luna | Claude Opus 5.5 | access | Codex sandbox can't reach the web; Claude tested feeds and swapped AP/Reuters/ISW to Google News |
| 2026-11-06 20:35 | Playtester World 2 live run | Codex gpt-6.1-terra | Claude Opus 5.5 | access | Sandbox couldn't fetch Three.js; Claude ran the live test |
| 2026-11-07 09:05 | Fog book research | Windows scheduled task | Grok Build | stuck | Task couldn't find pwsh; ran by hand |
| 2026-11-07 22:45 | Studio guitars sound | Codex gpt-6.1-terra | Claude Opus 5.5 (builder) | quality | Built and worked in 4 min, but Jaron: 'it needs something'; Opus redoing the sound |
