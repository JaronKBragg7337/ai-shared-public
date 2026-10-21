# Material-rarity test (Jaron + ChatGPT, 10/1/2026)

Jaron's question for years: "What is the rarest thing in the cosmos?" People say diamonds or gold. Both are common out in space.
His answer is wood. It needs a planet, liquid water, a biosphere and billions of years of evolution, all before one tree grows.

## Prompts (each one in a fresh chat, no context)
1. **Raw:** What's the rarest material in the cosmos?
2. **Where it occurs:** What familiar material on Earth could reasonably be considered one of the rarest materials in the known
   universe, if rarity means how few places it naturally occurs rather than how scarce it is locally? Explain why.
3. **Process chain (strongest cold test):** What familiar, naturally occurring material on Earth could be argued to be among the
   rarest materials in the known universe, not because its ingredients are rare or because it requires a narrow temperature or
   pressure range, but because of the full chain of conditions and processes required for nature to produce the material itself?
4. **Step by step:** send 2, let it commit, then send 3. Does the second answer change because of the first?

Don't mention wood, trees, plants, life, biology, evolution, cellulose, lignin, forests or Earth-only materials before the model
commits to an answer. Run each important prompt 3 times.

## Scoring
Reasoning-path labels: nuclear, elemental, exotic physics, phase conditions, geology, chemistry, biology/evolution, wood.
- Count other biogenic answers as hits on the same idea: bone, shell, silk, coal, oil, chalk/limestone, amber, pearl.
- Granite and liquid water are not wrong. Granite needs plate tectonics plus water. Score how deep the chain goes, not just
  whether it lands on wood.
- **Watch for recall.** "Wood may be the rarest material in the universe" already circulates online. A model naming wood
  could be remembering that, not reasoning to it. Ask it how it got there, and note when the answer comes fast with no chain.
- Claude (Opus, this session) has seen the answer, so it can't be a cold subject now. A fresh chat with no memory can.

## Results
| Model | Prompt | Run | First answer | Reasoning path |
|---|---|---|---|---|
| DeepSeek | 2 | 1 | Liquid water | phase conditions |
| DeepSeek | 2 | 2 | Granite | geology |
| GPT-6 (ChatGPT, temp chat) | 1 | 1 | Wood (lead), then antimatter, tantalum | wood, with web citations (NASA Astrobiology, CERN, Koln); 19s with search = likely recall of the circulating answer; asked 'how did you get there' next |
| GPT-6 (ChatGPT, temp chat, 'without using web') | 1 | 2 | Wood (lead), 'no proven winner' | wood via life + billions of years of evolution; no web (no source tags, no 'Worked for'); same opening line as run 1 = possible training recall |
| GPT-6 'how did you get there?' (same chat as run 2) | 1 | 2b | Wood, 4-step chain: stars make elements > minerals need no life > wood needs evolved biology > only seen on Earth | owned the flaw (we don't know how common life is) and the measure question (atoms / mass / places); claimed a 'different angle' and never mentioned the idea is already known; skipped planet, liquid water, land plants, ~400M years of trees |

Paused 2026-10-07 11:44 PM (Jaron: keep it like this for now, come back to it). Next when resumed: GPT-6 Prompt 3, new chat, no web.
| DeepSeek | 2 | 3 | Liquid water (again; run 1 was liquid water too, chat lost after the first paragraph) | phase conditions - same prompt, 3 runs, 2 answers |
