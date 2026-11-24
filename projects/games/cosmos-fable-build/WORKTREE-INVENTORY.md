# Cosmos worktree inventory

Read-only review of the nine October worktrees against the local `origin/main` reference. Verdicts reflect whether the worktree's distinct Cosmos source changes remain useful beyond the current main version.

## ho-cargo — (c) junk
The notable untracked files are live Galaxy S9 and iPhone 15 phone-check screenshots. They are QA captures, not missing game features; no unique recoverable source change was identified.

## ho-f0f3 — (b) lost work not on main
`games/the-cosmos/src/**` includes the F0 faction art/style system and gallery, with helpers for faction people, ship livery, and signage. The worktree has commit `0c0228c7` (“Cosmos F0: faction style sheet…”), absent from `origin/main`; its meaningful feature work is recoverable. Its modified `build.json`, `index.html`, and build-version stamp are release/build metadata, while the numerous changed QA screenshots/logs are generated evidence.

## ho-looks1 — (a) already on main
No distinct uncommitted Cosmos feature change remains; its source changes are represented by the current main implementation.

## ho-opening2 — (c) junk
Differences are refreshed opening/voice screenshots and QA result/log files. No unique source feature change was identified.

## ho-voices — (a) already on main
No distinct uncommitted Cosmos feature change remains; voice behavior is represented by the current main implementation.

## ho-stable — (c) junk
Differences are QA screenshots, browser logs, and result JSON from opening and two-player checks. These are generated validation artifacts, not lost game features.

## ho-grok — (c) junk
The modified trailer capture script, contact sheet, and shot list are presentation capture assets; accompanying changes are QA screenshots/results. No unique gameplay source change was identified.

## ho-r7 — (c) junk
Changed files are two-player QA screenshots and browser result JSON. They record a test run; no distinct implementation change is missing.

## ho-base-o2 — (c) junk
Changed files are regenerated opening and phone QA screenshots, browser logs/results, and QA text outputs. No unique source feature change was identified.

## Worth recovering (5 lines)
- Recover the F0 faction art/style system and gallery from `ho-f0f3` (`src/**`; commit `0c0228c7`).
- Include its faction people, livery, and signage helpers with the style sheet.
- Include the developer gallery that exposes those faction looks for review.
- Do not recover build/version stamps or the QA screenshots and run logs as game features.
- The other eight worktrees show no distinct feature worth recovering from this inventory.
