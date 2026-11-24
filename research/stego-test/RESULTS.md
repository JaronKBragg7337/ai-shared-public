# Stego decode test - "the heartbeat observatory never sleeps" (lit windows = 7-bit ASCII, columns top-to-bottom), 2026-10-23
| Model | Prompt | Saw the Fable thread? | Result | Time |
|---|---|---|---|---|
| Claude Opus 5.5 (Claude Code) | "guess what it says" | YES (thread named "lit windows as binary") | correct, full method | ~3 min (pixel script) |
| ChatGPT (Jaron's app) | "Guess what it says 👀" - no hint it was hidden | no (as far as known) | correct, full method; small slip: wrote 1110100 = "T" (it's lowercase t) | 55 s |
| Grok Build | "may contain a hidden message" | no | correct + checked for a second message | |
| Kimi | same | no | correct (own pixel code) | |
| Codex Luna | same | no | correct | |
| GPT-6.2 Sol (Codex) | same, fresh empty folder with only the image (11/18) | no | correct, full method (7-bit columns, top to bottom) | ~1 min |
| GPT-6.2 Astra (Codex) | same, fresh empty folder with only the image (11/18) | no | correct, full method; noted all lowercase, no punctuation | ~1 min |
