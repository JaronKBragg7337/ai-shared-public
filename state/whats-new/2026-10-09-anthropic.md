# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-09

No earlier Anthropic file existed in this folder, so this one covers October 6-9, 2026 (not just since the 8th).

- **October 6 — Claude Opus 5.5 launched.** Works about as well as Fable 5.1 on most jobs but costs 40% less to run than the old Opus 5. [Anthropic news](https://www.anthropic.com/news)
  for Jaron: cheaper top-tier model now exists; worth a side test on one job per [[jaron-fits-with-opus]] rule — don't move your main seat off Opus without a reason.

- **October 6 — Claude Cowork tasks on Pro/Max now start in Anthropic's cloud by default.** The "Only on your computer" setting is gone for new tasks (tasks already running locally stay local). Cloud tasks follow you across desktop/web/phone and keep running when the computer sleeps or closes. [Release notes](https://support.claude.com/en/articles/12138966-release-notes)
  for Jaron: if any Cowork task on the MSI is mid-run, it finishes locally as normal; any *new* Cowork task now keeps running even if the MSI is off or asleep — useful for overnight jobs.

- **October 7 — Claude Haiku 5.5 launched.** Cheapest, fastest small model yet: 1M-token context, up to 128K output tokens, costs 75% less than Haiku 4.5. Built for high-volume jobs (classification, summarizing, extraction, voice/chat agents). [Anthropic news](https://www.anthropic.com/news)
  for Jaron: good fit for chore-type routing (what Luna 6 handles now) if a Claude-side option is ever wanted — cheap enough to run a lot of small jobs.

- **October 7 — Monthly API credits added for Claude Max and Team plan subscribers.** $100/month on Max 5x, $200/month on Max 20x, up to $500/month pooled for Team seats. Claim by linking a Claude Console organization (Settings → Billing for Max, Organization settings → Billing for Team). Does not cover interactive Claude Code use, and unused balance does not roll over. [Release notes](https://support.claude.com/en/articles/12138966-release-notes)
  for Jaron: if the MSI's Claude plan is Max, this is free API spending money sitting unclaimed each month — matches "money you can see and reach is yours to use." Worth checking Settings → Billing and linking a Console org to not leave it on the table.

- **October 8 — Claude Dashboards and Claude Motion launched in beta; Docs/Slides/Design came out of beta on every plan.** Dashboards builds a live chart/dashboard from a plain-language question (connects to things like BigQuery, Snowflake). Motion turns text/data into an animated video, written as editable code (not a video model) and exported to MP4. [Anthropic news](https://www.anthropic.com/news)
  for Jaron: Motion could be a cheap way to make a short explainer animation for a site page or TV short without going through Unreal/Blender — only if it's ever the right tool, not a default.

- **October 8 — 2026 Usage Policy update.** Clarifies weapons rules (covers software/components that make weapons work, arming drones/autonomous vehicles) and adds a ban on sustained, needless abusive or cruel treatment of the models. [Usage Policy update](https://www.anthropic.com/news/2026-usage-policy-update)
  for Jaron: nothing changes for us — none of the crew's work touches weapons, and the new line is about how the models are treated, not a new restriction on legitimate work.

- **October 8 — Claude Code 2.1.294/2.1.295.** Bug fixes for hooks (a hook written as a plain-language instruction can now actually block an action instead of just being advisory); added an `effort` parameter for the Agent tool and a `--marketplace` flag for plugin installs. [Claude Code changelog](https://code.claude.com/docs/en/changelog)
  for Jaron: background plumbing — explains why hook behavior might feel stricter/more reliable going forward; no action needed.

Checked through October 9: no further official Anthropic posts past the Dashboards/Motion/usage-policy batch above.
