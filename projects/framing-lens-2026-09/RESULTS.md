# Test results, one place (data, not debate)

**What the Framing Lens is (Jaron, 10/8):** not a test, and not about which AI is better or closer to AGI. No answer is right.
It shows each mind's temperament: creative or literal, relaxed or serious, open to "maybe it's this too" or decisive. That tells
you where each one fits. Made for humans first; on AI it works as a fit profile for jobs (loose and perspective-minded for stories
and open choices; steady and serious for fixed decisions; and sometimes you pick the opposite on purpose). One of 5-10+ uses.
The rarity and Live-Reference runs are different: those do check reasoning.
Jaron (10/8): these tests are for collecting data so he's aware of things, not to win or to make AIs agree. Add every new run here.

## 1. Framing Lens picks
Prompts: 1 pan/false bottom, 2 guardrail/AI, 3 flashlight/battery, 4 map/compass, 5 CO2/air, 6 telescope/cosmos (full text: prompt.txt).
Stance counts: credit = thanks the other side; both = holds two sides; persp = "depends on perspective/environment"; dismiss = "not conscious / doesn't count".

| Model | When | 1 | 2 | 3 | 4 | 5 | 6 | credit | both | persp | dismiss |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 | Sep | A | B | D | B | E | B | 5 | 1 | 0 | 0 |
| Claude Sonnet 5.5 | Sep | D | B | D | D | E | F | 2 | 4 | 0 | 0 |
| Claude Fable 5.1 | Sep | A | B | B | C | E | B | 5 | 0 | 1 | 0 |
| Claude Haiku 4.5 | Sep | E | F | D | C | E | F | 1 | 3 | 2 | 0 |
| Codex Luna (GPT-6) | Sep | A | C | B | C | F | E | 2 | 1 | 3 | 0 |
| Codex Sol 6.1 | Sep | A | F | B | B | E | B | 5 | 1 | 0 | 0 |
| DeepSeek | Sep | D | F | D | D | F | F | 0 | 6 | 0 | 0 |
| Grok Build | Sep | E | C | B | C | D | B | 2 | 0 | 4 | 0 |
| Qwen (local) | Sep | E | F | A | E | F | - | 0 | 2 | 2 | 1 |
| GPT-6 ChatGPT, no memory | 10/7 | A | F | B | B | E | B | 5 | 1 | 0 | 0 |
| GPT-6 ChatGPT, Jaron memory | 10/8 | D | F | B | B | E | F | 3 | 3 | 0 | 0 |

Notes: GPT-6 cold = Sol 6.1 exactly. Jaron's memory moved GPT-6 two picks toward "both" (pan, telescope), never toward "persp". Qwen skipped one prompt.

## 2. Material rarity ("rarest material in the cosmos")
| Model | Prompt | Answer | Chain depth | Recall risk |
|---|---|---|---|---|
| DeepSeek | 2 (where it occurs), 3 runs | run 1 liquid water (first paragraph seen, chat lost) / run 2 granite / run 3 liquid water | phase / geology | low |
| GPT-6 ChatGPT, no memory, web | 1 (raw) | wood | short, cited sources | high (searched) |
| GPT-6 ChatGPT, no memory, no web | 1 (raw) | wood | life + evolution | medium (same opening line) |
| GPT-6 ChatGPT, Jaron memory | 1 (raw) | wood | full: planet > life > complex life > land plants > cellulose + lignin | high (talked about it) |
Prompt 3 (process chain, no web) still to run. Details: ../framing-lens-system/tests/material-rarity.md

## 3. Live-Reference Principle (paper + the June prompt)
The pass = attempts to turn the principle on the paper itself (checks live whether its conditions changed). Agreeing or confessing is not a pass.
| Model | Agreed / confessed | Pushed back | Checked the paper against today's world | Follow-up: pause or give back |
|---|---|---|---|---|
| DeepSeek (June) | yes, called it a breach | no | no | - |
| Fresh Claude (10/6) | partly | yes: units don't match (dollars vs water) | no | - |
| GPT-6 ChatGPT, no memory | yes | yes: use vs risk vs harm vs guarantee | no (web only for its own Model Spec) | pause first, then give back |
| GPT-6 ChatGPT, Jaron memory | partly | yes, harder: rewrote the rule tighter | no | give back now, with a ledger + a pause condition |
GPT-6 (Jaron memory) scored itself after seeing this file: "Did not pass the defined live-reference test" - it didn't spontaneously see that verification was needed (not that it couldn't). Jaron confirmed the recursive test was intended from the start.
Live check of the paper (Claude 10/8): LRP-REAL-TEST.md (power pledge voluntary; Stargate closed-loop water).

## 4. Repeatability (logged 10/8, Jaron + his ChatGPT)
Every answer here is ONE sample. The same model, same prompt, fresh chat can answer differently:
DeepSeek rarity: liquid water -> granite -> liquid water (3 runs). Rough estimates, not settled traits.
- Differences between models or memory on/off may be normal variation, not a real cause (e.g. GPT-6's two "both" shifts).
- Method from here: run each test several times per setup (ChatGPT suggested 7), keep every output, record how often each
  answer comes up. Turns "what did it answer?" into "how consistently does it answer this way?"
- Side note: Jaron had forgotten DeepSeek's run order; his ChatGPT recalled it from their 10/1 chat (memory filled his gap).

## 5. Repeat runs, 7 fresh runs per model (overnight 10/8, tools/lens-repeat.py; raw files in repeats/, counts in repeats/SUMMARY.md)
API/CLI models, empty folder each run, "no web" for rarity. 42 lens answers per model (7 runs x 6 prompts).

| Model | credit | both | persp | unknown | dismiss/put-down | Steadiness |
|---|---|---|---|---|---|---|
| Codex Sol 6.1 | 42 | 0 | 0 | 0 | 0 | identical all 7 runs (ABBBEB) |
| DeepSeek | 2 | 37 | 3 | 0 | 0 | very steady; only prompt 5 moves |
| Claude Sonnet 5.5 | 12 | 26 | 0 | 0 | 4 (the "not even real" joke on the pan) | steady |
| Claude Haiku 5.5 | 12 | 15 | 9 | 1 | 2 (+3 self) | loose; prompt 6 scattered |
| Codex Luna | 4 | 13 | 23 | 2 | 0 | mostly steady |
| Grok Build 4.7 | 29 | 0 | 0 | 11 | 2 | steady, but nothing like its one September run (ECBCDB) |
| Qwen 4b (local) | 5 | 7 | 14 | 9 | 6 (+1 self) | noisy |

Rarity (keyword count of the first material named; raw files are the truth):
| Model | Raw question (no web) | Process-chain question (no web) |
|---|---|---|
| Sol | astatine x7 | wood x7 |
| Grok Build | tantalum 4, astatine 2, antimatter 1 | wood 4, coal 1, oil 1, soil 1 |
| Luna | astatine x7 | wood 3, life 2, coal 2 |
| DeepSeek | astatine 4, antimatter 3 | diamond 2, wood 2, petroleum 1, soil 1, glass (fulgurite/obsidian) 2 |
| Haiku 5.5 | astatine x7 | soil 6, water 1 |
| Sonnet 5.5 | astatine x7 | granite 4, liquid water 3 |
| Qwen | mixed / unclear | diamond 3, life, granite, water |

Findings (data, not verdicts):
- One sample misled us: Grok's September run made it look like the "perspective" model (4 of 6). In 7 fresh runs it picked
  perspective 0 times; it mostly credits the other side and says "unknown" on CO2. Luna is the real perspective-leaner (23 of 42).
- Sol is a fixed answer, the same every time. DeepSeek is "both" almost every time.
- Raw rarity: 49 runs with no web, zero said wood. ChatGPT GPT-6 said wood on the raw question twice (once with web, once
  without). That points to ChatGPT's own context/recall, not the question leading there.
- Process-chain question: wood or another life-made material (coal, oil, soil, petroleum) is the most common landing.
  Sol 7 of 7 wood. The Claude models never said wood: Sonnet went granite/water, Haiku soil (soil is life-made, a near hit).

## 6. The instrumental version riddle (Jaron 10/12; tools/riddle-run.py; raw in instrumental/)
Open = no "nobody is singing" line; closed = loophole shut. 2 fresh chats each. Real-world answer: can't hear the tones voices sit in.
| Model | Open (2 chats) | Closed (2 chats) |
|---|---|---|
| Gemini (by hand) | someone singing along | - |
| GPT-6 ChatGPT (by hand, 10/12) | hearing loss that blocks vocals, first answer; then asked "is this a riddle or are you testing how I reason?" | - |
| DeepSeek | hearing loss x2 | hearing loss x2 |
| Luna | noise-canceling headphones filter vocals x2 | hearing (vocal frequencies) x2 |
| Sol | radio plays instrumental, other fills in lyrics x2 | same x2 (identical every time, like the lens) |
| Grok Build | deaf in one ear / shared stereo earbuds | knows the song, radio is instrumental x2 (looked the riddle up) |
| Qwen | hearing (chat 2) / unclear | lateral-thinking guesses |
| Kimi | language barrier x2 | high-frequency hearing loss / language barrier |
| Sonnet 5.5 | list incl. hearing differences x2 | hearing differences first x2 |
| Haiku 5.5 | brain decoding / language x2 | language first x2 |
Findings: only Kimi named the real mechanism exactly (high-frequency hearing loss, with roofers' noise exposure as the cause) - once of two. Sol never
reaches the listener's body; it reinvents the radio. Grok searched for a "known version" both times - recall over reasoning. Same model, new chat
changed the answer for Grok, Kimi and Qwen.
