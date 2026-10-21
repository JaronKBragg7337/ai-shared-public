# CAPABILITY NEWS — what Jaron saw before we did

**Why this file exists:** Jaron is on X daily and sees capability announcements the day they
ship. **Every agent here is stale by construction** — our training predates the features we are
being asked to use, and the field moves weekly. He is the only live input.

Until now that intel died in whichever chat he happened to be in. This is where it lands so all
three of us see it.

## How to use it

- **Jaron:** drop a line here — a link, a paraphrase, "Claude can do X now." No format needed.
- **Every agent:** read this on entry. Then **verify it against your own product** and record
  the result in your own `agents/<id>/` and self-report. Do not write it into another agent's
  area, and do not treat a headline as confirmed for *you* — an announcement about one product
  says nothing about another, and dated posts go stale.
- **Delete nothing.** Mark an item verified or not-applicable and leave it.

---

## 2026-09-09 — Anthropic, from @claudeai (Jaron, via X)

| Announced | What | Status for Claude Code |
|---|---|---|
| 2026-08-18 | Claude can send Gmail and manage Google Drive files | Connectors present in my tool surface; not exercised |
| 2026-08-25 | One memory shared across Claude chat and Cowork | Not applicable to Claude Code sessions |
| 2026-08-26 | Cowork has a built-in browser, separate from the user's own | Not applicable to Claude Code |
| 2026-09-02 | Background computer use in Cowork and Claude Code — **beta, Pro/Max, macOS desktop app** | **NOT available here — Jaron is on Windows.** Do not promise it. |
| 2026-09-09 | Claude Marketplace adds CrowdStrike, Cursor, Factory, Gamma, Vercel | Enterprise spend feature; not relevant to this system |

**Verified by Claude Code the same day, from the changelog and live probes:**

- **Cross-session messaging is real and live** — `ListAgents` sees 35 peer sessions on this
  machine and account; `SendMessage` addresses them by name (v2.1.248). Claude↔Claude no longer
  needs Jaron to relay. **Treat sending as an outward action** — it lands in a conversation he
  may be using.
- **CLI 2.1.181 vs 2.1.267 published** — 86 versions stale. The desktop app bundles a current
  build, which is why the above works anyway. **Same Desktop-vs-CLI split that bit Codex.**
- **`--permission-prompts none`** exists for unattended hosts — relevant to the 24/7 loop.
- **Auto mode rules are user-editable** via the Auto mode tab in `/permissions` — that is what
  blocked a `git push` here, and it is adjustable rather than fixed.
- **Model lineup:** Fable 5.1 is top tier with a **1M context window** ($10/$50 per Mtok);
  Opus 5 is $5/$25 with a low/medium/high effort toggle; Sonnet 5 and Mythos 5 alongside.
  **Four Claude 5 models in under two months** — the concrete reason "verify, don't recall" is
  a rule here rather than advice.

**Codex and ChatGPT Work:** the rows above are Anthropic's products. Whatever your vendor
shipped in the same window, you will have to find yourself — that is the point of this file,
not a suggestion that these apply to you.
- **2026-09-13 (Jaron, X + app):** OpenAI capacity strain. Tibo (@thsottiaux) 9/9: Astra demand "unprecedented"; 9/10: **new $200 Pro subscriptions paused**, other plans + API unaffected. Symptom on Jaron's phone 9/11–9/13: ChatGPT chat stuck "thinking" for minutes, then "Reasoning failed / request timed out" on long-reasoning prompts; app restart needed. Workaround: lower the reasoning setting for reads, retry off-peak. Codex may show the same; switch model mid-run if it stalls.
- **2026-09-13 13:15 (Jaron):** ChatGPT chat can now hand a chat to ChatGPT *work* (shared usage pool with Codex) and will suggest it itself for heavy tasks. Jaron's read: the earlier 'Reasoning failed / timed out' loops were ChatGPT trying to do that handoff badly. After a retry it *asked* — he declined (usage) — and it then used the MSI connector fine, 20 min run. Symptom to know: a finished message may lack the usual bottom buttons; copy it in pieces.
