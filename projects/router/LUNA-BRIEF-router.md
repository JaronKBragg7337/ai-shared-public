# Brief for Luna 6 - the job router (non-visual tooling; plain, sturdy, honest)

Jaron (10/1 6:45 PM): "What we need is something that when I message you [Claude] and it's a job for another it routes it to
any other AI based on usage and the role it's gonna have what's available."

Claude Opus stays the entry point (Jaron talks to Claude). You build the tool Claude calls to pick WHO does a job and HOW to
start it. Work in C:/Users/lilli/AI-Shared (tools/ and state/). Read state/models.md first (every callable model, with roles).

## Build
1. `state/routing.json` - the roles table, editable by hand: job kinds -> ordered candidates. Starting rules (Jaron's):
   - looks (assets, characters, sets, game visuals, ships): Claude Sonnet 5.5 -> GPT-6.1 Sol -> Grok 4.7 (Grok Build)
   - major build (systems, multiplayer, economy): GPT-6.1 Sol -> Claude Sonnet 5.5 -> Grok 4.7
   - chore (publish, checks, docs, plumbing, small fixes, data): GPT-6 Luna -> Grok 4.7 build-fast -> GPT-Reserve
   - research / review / second opinion: Grok 4.7 -> GPT-6 Luna -> Claude Haiku
   - judgment / orchestration: Claude Opus (never routed away)
   - never: Fable (asks Jaron first), anything trading (Claude and Codex never trade).
   GPT-Reserve (Codex "Luna Reserve") is a separate weekly pool for after the normal Codex allowance runs out - use it as
   Codex overflow.
2. Usage readers, one per meter, each returning {used_pct_5h, used_pct_week, resets, source, as_of} or "unknown":
   - Codex: find where the CLI records rate limits (e.g. token_count / rate_limits events in ~/.codex/sessions/**/*.jsonl or
     ~/.codex/logs_2.sqlite) and read the latest primary (5-hour) and secondary (weekly) percentages, plus the gpt-reserve
     limit if present. Verify against a real recent run; say how you verified.
   - Claude: state/usage-live.json (tools/usage.py) plus any manual reading Jaron sent (add state/claude-usage.md readings,
     same format as state/grok-usage.md). Mark Claude estimates as low-trust.
   - Grok: state/grok-usage.md (Jaron's readings) and whatever the new Grok CLI exposes (check `grok --help` for a
     usage/status command; don't spend usage finding out).
   - DeepSeek: Control Room row deepseek_daily_budget_usd via tools/settings.py (0 = off).
3. `tools/route.py "<job>" [--kind looks|build|chore|research|judgment] [--dir <workdir>] [--run]`:
   - guesses the kind from the words if not given (simple keyword rules in routing.json; print the guess);
   - skips a candidate whose meter is over a threshold (routing.json: e.g. 5-hour > 85% or week > 90%) or "paused";
   - prints the pick, why, the meters, and the exact command (codex exec -m ..., grok -p / grok with --cwd and
     --always-approve for builds, or "Claude Agent tool, model sonnet" for Claude models, which Claude launches itself);
   - with --run (Codex/Grok only): starts it in the background, output to state/route-runs/<time>-<agent>.log, and appends a
     line to state/route-log.md (time, job, kind, pick, why).
4. Tests: a small `tools/test_route.py` with fake meters (each kind, a full meter skipping to the next, unknown meters).
5. A short `projects/router/README.md` in plain words: how Claude uses it, how to change the roles table.

Rules: never print or store secret values. Don't edit ~/.codex/config.toml or ~/.grok/config.toml. Don't actually route any
real job while building (only dry runs, and at most one tiny real test per meter reader if you need it). Report honestly what
each meter reader really reads and what is still "unknown".
