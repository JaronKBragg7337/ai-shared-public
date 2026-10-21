# RUNBOOK — driving the desktop, and standing up a Grok Bot

Written 2026-09-10 by Claude Code, after doing both end to end. Anyone repeating this —
another Claude session, Codex, or Jaron — should be able to follow it without rediscovering
the traps. Codex can also drive the desktop, so hand this to Codex if Claude usage is tight.

---

## PART 1 — Using the computer (mouse, keyboard, screen)

### It works, and it is worth using

Jaron said *"I wish you could fully use computer like use the mouse and look at screen and do
this for me."* You can. Onboarding wizards, permission cards, app setup — anything with no API.

### The sequence

1. **`ToolSearch` for `computer-use`, `max_results: 30`.** One call loads the whole toolkit.
   Do not fetch tools one at a time.
2. **`request_access` with the app names.** Nothing works before this. Names come from the
   Start-menu list the tool prints.
3. **`screenshot`** to see the screen. Coordinates come from this image.
4. **`computer_batch`** for anything you can predict — click, type, wait, screenshot in one
   round trip instead of four.

### Traps that cost real time

**Coordinates are in the FULL-RESOLUTION frame, not the scaled image.** A `scale: 0.6`
screenshot reports `coordinate frame: 1389x868`. Read a button at (313, 200) in the image and
you must click **(313/0.6, 200/0.6) = (522, 333)**. Getting this wrong clicks empty space.

**Apps not in the allowlist are masked to solid black.** That is a privacy feature, not a bug —
Jaron had a Sticky Note with a secret open and it never reached me. But if a masked window sits
ON TOP of your target, your click hits the masked window. Call `open_application` on your target
first to bring it forward, then re-screenshot.

**Browsers grant at "read" only; terminals and IDEs at "click" only.** You cannot type into
Cursor, VS Code or a terminal. Requesting them warns you once and requires an immediate retry
**in the same turn** — do not reply to the user in between or you get the warning again.
For shell work use the Bash tool. For browser work use the Chrome extension MCP.

**A batch dies if a non-allowed app steals focus mid-sequence.** The frontmost check runs before
every action. `textinputhost.exe` (the Windows IME) is a common culprit. Re-screenshot and retry.

**Elevated processes cannot be driven at all** — Task Manager, UAC, admin installers. Windows
UIPI blocks it. Ask Jaron to click those himself.

### Etiquette

Stop before anything consequential. Naming an agent, granting a permission, authorizing OAuth —
show him the card and let him press it. He is faster than you at deciding and it is his machine.

---

## PART 2 — Standing up a Grok Bot

### What it is and why it matters here

Grok Bot is a persistent cloud VM with a browser, filesystem, terminal, memory and MCP support.
It is **the only agent in this system that survives the MSI being off**. Claude Code, Codex and
Qwen all stop when the machine reboots or sits at a login screen — that cost a full day on
2026-09-09.

### Subscription

**Grok Bot is included with every SuperGrok tier** ($30 SuperGrok, $100 Plus, Heavy). The
standalone Pro/Pro+/Ultra tiers are for people with no Grok subscription. Jaron already had
SuperGrok, so it cost nothing extra.

**xAI publishes no per-tier usage numbers** — tiers are described only relative to each other.
On-demand billing is opt-in and there is **no Grok-Bot-specific spend cap**, only an
account-level one. Set that cap before enabling on-demand.

### The linking trap

**Mobile linking failed repeatedly** with *"requires an active SuperGrok... Upgrade this Grok
account"* on an account that HAD SuperGrok. **Desktop worked first try** at
`cursor.com/loginDeepGrokBot`. Grok Bot is served through Cursor infrastructure, which is why
sign-in bounces between `accounts.x.ai` and `cursor.com`.

**If a link fails on the phone, try desktop before buying anything.**

I also misread this: I told Jaron he had two accounts because the display name
("SYL Vexora- Jaron K Bragg") differed from the email (`<email>`). Same
account. He pushed back with a profile screenshot and was right.

### Onboarding

Engineering → GitHub + Vercel → name the bot → Get started. Three screens, all clickable.

---

## PART 3 — Connecting a Grok Bot to this machine

There are **two independent routes**, and Bridge found the second one itself.

### Route A — registered-computer (works with no setup)

Grok Bot's native Shell/Read/Write against a registered machine. Bridge used this to read
`AGENTS.md` and write its own self-report **while the MCP was still broken**. Each action raises
a per-call approval card.

### Route B — the Heartbeat MCP (49 tools, the rich one)

`https://mcp.heartbeatobservatory.com/mcp` — a Cloudflare tunnel to `127.0.0.1:3001` on the MSI,
serving PowerShell, filesystem, process control, window/input, clipboard, screen capture,
durable tasks, and **local Ollama access**. Source at `runtime/grok-machine-mcp`.

Grok Bot can only reach MCP servers on the **public internet** — it cannot see `127.0.0.1`.
The tunnel is what makes this possible.

**MCP wins for:** GUI control, Ollama, ports and processes, durable MSI tasks, and not needing a
click-approval on every shell call.
**Registered-computer wins for:** working when the tunnel or MCP is down.

### The two bugs that blocked Route B, and their fixes

**1. Google Drive killed it at every boot.** The task's working directory was on `G:`, and
GoogleDriveFS mounts ~46 seconds AFTER logon tasks fire. Result `0x8007010B` (invalid
directory) at every single boot. The tunnel was healthy the whole time; the origin was simply
dead, so the endpoint answered 502.
**Fix:** moved the runtime to `C:\Users\lilli\AI-Shared\runtime\grok-machine-mcp` and repointed
the task. There was even a `node_modules-drive-failed` folder in the original — Drive had broken
an npm install there before.

**2. OAuth rejected the client before sign-in could open.** `exactRedirectUriAllowed()` in
`oauth.mjs` accepted only `https:` and loopback `http:`. Grok Bot is a **native desktop app** and
registers a private-use scheme callback (`cursor://...`), which **RFC 8252 §7.1 explicitly
permits**. Registration returned 400 `invalid_redirect_uri`, no sign-in card ever appeared, and
the endpoint answered 401 forever — a dead-server symptom with a registration cause.
**Fix:** accept private-use schemes; still reject fragments, non-loopback plain `http:`, and
`javascript:` / `file:` / `data:` / `vbscript:` / `blob:` — schemes that execute code or read
local files, which matters because the OAuth server delivers a credential TO the redirect URI
and registration here is open. The real protection — exact matching at authorize time — was
untouched. Backup at `oauth.mjs.bak-preredirect`.

### THE TRAP THAT ALMOST SHIPPED A BROKEN FIX

**Restarting the server twice appeared to work and did not.** The port stayed listening, so it
looked healthy — but the ORIGINAL process was still running and the patch was never loaded. The
live test failed and that is the only reason it was caught.

**Always compare the listening PID's `CreationDate` against when you patched.**
"Port is listening" does not mean "my code is running." `Stop-Process -Id <pid> -Force` was the
only thing that actually replaced it.

### AND ITS SIBLING

**Repointing a scheduled task is not the same as testing it.** The task was repointed to `C:`
but never RUN, so the live server was a hand-started process and the autostart path was
completely untested — the exact trap that cost a day with Ollama. Bridge caught this on its
first run by noticing `LastTaskResult` still held the Drive-era code while the port was up.
**Test cold: stop everything holding the port, then `Start-ScheduledTask`, then verify.**

---

## PART 4 — Permissions

**Claude Code CAN modify existing scheduled tasks (`Set-ScheduledTask`) but CANNOT create them
(`Register-ScheduledTask` → Access denied).** Route creation to Codex; do repointing yourself.

`git push` is sometimes blocked by the auto-mode classifier. It refused a push of a local branch
onto a differently-named remote branch from a scratch clone, but allowed a normal `main → main`
push later. Do not retry a denial verbatim — say what you were trying to do and let Jaron decide.

---

## PART 5 — Standing up the routine

Bridge runs **hourly at :51, every day** — all days deliberately, because a silent post-reboot
failure does not respect working hours.

Ask the bot to create the routine and it handles the scheduling. Give it: cadence, a clear job
per wake, where to write, what counts as worth pinging about, and what to do when the machine is
unreachable. Tell it explicitly to **observe and record, not restart or fix** — otherwise you
have an unsupervised agent repairing production at 3am.

It appends to `state/bridge-health.md`, one dated line per run, never overwriting.

### What still limits it

`AutoAdminLogon` is **OFF**, so the MSI's own tasks wait for a human to sign in after a reboot.
Bridge keeps running regardless and can do cloud-only work while the machine is dark — but it
cannot refresh anything under `C:\Users\lilli\AI-Shared` until someone logs in. Bridge worked
this out itself from `INDEX.json` and said so unprompted.
