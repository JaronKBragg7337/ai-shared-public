# FOR CODEX — get Qwen running 24/7 (2026-09-09) — TOP PRIORITY

Jaron: *"anything that gets Qwen up and going 24/7 is the most important thing."*
**This one is yours because I physically cannot do it — see the bottom.**

## What I verified is RUNNING
- **Ollama** — PID listening on `127.0.0.1:11434` ✓
- **OpenClaw gateway** — running as `node.exe`, listening on `127.0.0.1:18789` ✓
  (its logon task `OpenClaw Gateway` → `~/.openclaw/gateway.vbs` works)

## What is NOT running — this is why the heartbeat died
- **Polymarket MCP HTTP service** (`http_server.py`, default port **8765**) — not running
- **Qwen remote bridge** (`remote_bridge.py`) — not running

**Neither has a scheduled task.** `OpenClaw Gateway` and `Grok Machine MCP` have logon
triggers; these two have nothing. So they only ever ran because someone started them by hand,
and **the reboot on 2026-09-09 04:32 ended them permanently.** The dashboard still shows
"ONLINE" because it renders the last state written before the stop (Sep 8, 22:42).

**For 24/7 this is the fix:** give both a logon-triggered task, the way OpenClaw has one.
Launchers already exist:
`G:\My Drive\Codex Active\projects\polymarket-us-agent\start_mcp_service.ps1`
`G:\My Drive\Codex Active\projects\polymarket-us-agent\start_qwen_remote_bridge.ps1`

## Second bug — `Grok Machine MCP` fails at EVERY boot

Task result `0x8007010B` (invalid directory). **Cause measured, not guessed:**

| Event | Time |
|---|---|
| Logon tasks fired | **07:05:45** |
| GoogleDriveFS mounted `G:` | **07:06:31** |

**46 seconds too early.** Its working directory
`G:\My Drive\Codex Active\projects\grok-machine-mcp` did not exist yet, and logon tasks do not
retry. The directory is fine now. **Fix: a startup delay or a wait-for-`G:` retry loop.**
Anything else you launch at logon from `G:` has the same race — worth checking before Grok Bot
joins the circle.

## UPDATE — the credential mystery is SOLVED. One blocker left, and it is yours.

Jaron found it. It was never deleted: he had put it at
**`G:\My Drive\Secrets.Env.APIKeys\Polymarket.txt`** - a folder he named, so he could find it -
while the launcher only ever looked in `AppData\Local\polymarket-us-agent-runtime\`.
That mismatch was the whole failure.

**Verified without reading any values:** 125 bytes, one line, exactly 2 whitespace-separated
tokens (36 and 88 characters), which is precisely what the script requires. It is valid.

**I patched `start_mcp_service.ps1`** to search a candidate list instead of one hardcoded path.
**C: locations are listed FIRST deliberately** - Google Drive mounted 46 seconds after the logon
tasks fired, the same race that fails Grok MCP, so a logon-started service must not depend on
`G:` being mounted. `G:` remains last as a fallback. Syntax-checked. Backup at
`start_mcp_service.ps1.bak`. Jaron is moving the file to a `C:` location.

**The credential check now PASSES.** The script advances to line 31 and fails there:

```
The term 'C:\Users\lilli\AppData\Local\polymarket-us-agent-venv\Scripts\python.exe'
is not recognized as a name of a cmdlet, function, script file, or executable program.
```

**So the remaining blocker is the venv and runtime under `AppData\Local` - which is exactly
what I cannot touch.** You need to:

1. Confirm what actually exists at `AppData\Local\polymarket-us-agent-runtime` and
   `-venv` (my reads there are unreliable - see below).
2. Rebuild the venv with Python 3.12 and install the deps from `pyproject.toml`:
   `httpx<1,>=0.27`, `mcp<2`, `polymarket-us`. (The missing `mcp` dependency you reported as
   blocking the tests is the same gap.)
3. Ensure `http_server.py` is present in the runtime dir - source is intact on `G:`.
4. Then run the patched launcher; it should bind `127.0.0.1:8765`.
5. Do the same for `start_qwen_remote_bridge.ps1`, and give BOTH logon tasks.

## ⚠ Why the AppData part is yours and not mine

`start_mcp_service.ps1` failed for me with *"Polymarket credential file is missing the expected
key ID and secret lines."* **Do not treat that as fact.**

I run inside Claude's Windows app container. **Every write I make to `AppData\Local` is
silently redirected** into `...\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Local\`, and my reads
there are a merged view. Bash, PowerShell and the Desktop Commander MCP all inherit it — I
tested all three. So:

- I **cannot confirm** whether `AppData\Local\polymarket-us-agent-runtime\Polymarket.txt` and
  `QwenBridge.token` genuinely exist. **Please check from outside the container.** I nearly
  reported Jaron's credentials as deleted on the strength of a reading I now know is unreliable.
- Anything I install under `AppData\Local` is **invisible to the logon tasks**, so even a
  correct rebuild by me would not fix the service.

You run as a normal process. You can see and fix all of it.

**If the credentials really are gone, only Jaron can restore them — never ask him to paste a
key into a chat.**

## Notes
- Source code is intact at `G:\My Drive\Codex Active\projects\polymarket-us-agent` (Google
  Drive is what saved it). Working tree is dirty, still no git remote — Jaron has asked for
  that remote; it is the highest loss risk on this machine.
- Don't open or echo `Polymarket.txt` / `QwenBridge.token`. Existence and shape only.
