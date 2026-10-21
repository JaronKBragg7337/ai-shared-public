# OpenAI usage reference — Jaron's $20 ChatGPT Plus (checked by ChatGPT Chat against OpenAI docs, 2026-09-14)

Three separate meters inside one subscription. Watching one tells you nothing about the others.

## 1. CHAT battery (normal ChatGPT chat — e.g. Fly-Lab-2 sessions)
| Model | Plus? | How it's metered |
|---|---|---|
| GPT-5.6 Sol Instant | yes | effectively unlimited everyday text (abuse safeguards; uploads/images/voice have own limits) |
| Sol Medium / High | yes | one separate reasoning allowance; **no published Plus number**; on hitting it, ChatGPT shows the reset time and may fall back to another model |
| Sol Extra High, Sol Pro, GPT-6 Pro (= Astra in chat) | **no** | Pro tier only |
- Automatic reasoning triggered by Instant does NOT draw from the manual Medium/High allowance.
- **Chat usage never draws from Work/Codex.** That is why ChatGPT Chat kept running all week while Codex sat at 0%.

## 2. AGENT battery (Work + Codex — ONE shared pool; two constraints at once: 5-hour window AND weekly)
| Model | ~messages per Plus 5-hour window (OpenAI's own ranges, not caps) |
|---|---|
| GPT-5.6 **Luna** | 250–2,000 |
| GPT-5.6 Terra | 25–200 |
| GPT-5.6 Sol | 10–100 |
| GPT-6 **Astra** | 5–45 |
- Measured here: Luna L3 fix 3 pts, Luna axis job 4 pts; Astra slow-arm job 66 pts; Astra scene ~60. Matches the table.
- Weekly cap exists; no published Plus number — the Settings → Usage meter is the authority.
- **ChatGPT Work scheduled tasks (roofing scan) draw from this pool.** Codex jobs draw from this pool. They compete.
- Eligible Plus accounts can buy credits after included usage, or an immediate weekly reset.
- Astra in chat appears as "GPT-6 Pro" and needs Pro; Plus has Astra only inside Work/Codex.

## 3. API — separate pay-as-you-go billing. Not used here (DeepSeek is our only API spend).

## Tier notes (Sept 2026)
- Go $8 / Plus $20 / Pro $100 / Pro $200 (20×). As of 2026-09-10 new $200 upgrades are paused; Plus can upgrade only to Pro $100.
- Pro $100 chat: Sol Pro + GPT-6 Pro share ONE pool of 50 messages/week. Pro $200: 170 Sol Pro/day + 200 Astra/week, combined ≤200 Pro-model messages/day.

## Routing rules that fall out of this
1. Anything a *conversation* can do (design, read, reason, write briefs) → ChatGPT Chat. Free relative to the agent pool.
2. Anything that must *run on the MSI* (Codex) → Luna by default; Terra if Luna fails a check; Sol rarely; Astra only for from-scratch kernels.
3. The roofing scan and any Work schedule share the Codex pool — count them in `task-costs.jsonl` like any Codex job.
4. Long runs never inside an agent session; launch detached (Task Scheduler / Claude) — the agent pool pays per message, the CPU is free.

## Contrast with Anthropic (Jaron: "one counts up, the other counts down")
Claude shows % USED (up), weekly reset Wed 4 PM, 5-h session window; credits toggle on/off. OpenAI Work/Codex shows % REMAINING (down), weekly reset Sat 8:05 AM, 5-h window; chat is a separate unmetered-ish battery.
