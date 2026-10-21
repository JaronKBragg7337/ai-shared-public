# Job router

Claude Opus stays the entry point. For a job meant for another model, Claude can run:

```powershell
python tools/route.py "publish the current build"
```

The router guesses a role and prints the ordered pick, available usage readings, and exact launch command. Use `--kind looks|build|chore|research|judgment` to choose the role yourself, or `--dir <folder>` to set the working directory. `--run` starts a Codex or Grok job in the background and records its log in `state/route-runs/` and its selection in `state/route-log.md`. For Claude picks, the output tells Claude which Agent model to launch.

Edit `state/routing.json` to change each role's candidate order, keyword list, usage thresholds, or paused agent IDs. Unknown usage is shown as unknown and does not by itself block a candidate. Fable is blocked because it needs Jaron's prior approval. Judgment always stays with Opus. The router refuses jobs that mention trading, bets, wagers, or Polymarket.

Usage sources: Codex percentages come from the recent local rollout rate-limit snapshot produced by `tools/usage.py`; GPT-Reserve's separate meter is not exposed in the data found so far. Claude uses `state/usage-live.json`'s local token estimate (low-trust), overridden by the newest reading in `state/claude-usage.md`. Add readings there as `YYYY-MM-DD HH:MM ET | 5h: N% | week: N% | resets: ... | source: ...`. Grok's CLI help has no account meter, so its usage is unknown unless a current trustworthy source is added. DeepSeek reads `deepseek_daily_budget_usd` through `tools/settings.py`; zero marks it paused.
