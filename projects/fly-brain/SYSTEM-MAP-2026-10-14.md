# The AI as a system, not a single file - Jaron's map (talked through 2026-10-14 3 AM with Claude Code)

**READ FIRST - mindset (Jaron 10/14):** this is buildable engineering. Do not downplay, do not redirect to "just use an API". Start with the smallest REAL version (tiny language model trained from scratch on the MSI), then grow. Limits = engineering problems with next steps, never walls. Memory: own-ai-project-mindset.

Jaron: the core is the only part that must be trained (language first - "once language is down, anything else can grow"; it goes
through school). Everything else is knowledge pulled live (the Live-Reference Principle as architecture) and organs spread across
services. "These things are right in front of us - it's about connecting them." It needs its OWN accounts, not Jaron's.
Research names for the same idea: retrieval models (RETRO 2021, Atlas 2022), Karpathy's "cognitive core"; small-language-from-
child-scale-data = the BabyLM challenge (curriculum / "school"). Fly connectome runs on a laptop (Nature 2024).

## Organs (what each piece is for)
| Piece | Role in the body |
|---|---|
| Core (fly-seeded or open small model) on the MSI GPU | thinks; learns language through a school-style curriculum |
| Watch desk: 21 domains, official sources first, Kimi East desk (old Orchestra lineage) | senses + the curated curriculum; live knowledge |
| Triage / fact-check (Codex) / estimation isolation | judgment filter: what's useful, what's junk |
| Supabase (Postgres + pgvector) | working memory: fast, searchable, editable |
| GitHub | long-term record: every change hash-chained, history can't be quietly rewritten |
| Arweave | permanent memory: pay once, stored for the long term, can't be deleted - for the things that must never be lost |
| Filecoin | bulk archive: cheaper paid storage deals for big data (datasets, renders), renewable, not permanent by default |
| Obsidian | the human-readable mind map: linked notes Jaron (and the AI) can both read; links = a knowledge graph |
| Wikipedia / Wikidata | base reference: free full downloads (an offline copy), structured facts |
| X (its own account) | real-time pulse of the world + its public voice |
| Website + Cloudflare + Vercel | its face/body in public; Cloudflare edge can also host lookup services |

## Missing pieces (Claude's read)
1. Semantic search index (embeddings in pgvector) - how the core finds the right memory fast. Supabase already supports it.
2. A learning loop - the connectome is frozen; needs a rule for how experience changes it (scheduled fine-tunes, or memory-based learning).
3. Exams - a fixed test set to see it improve: Jaron's own tests (wood, LRP, instrumental riddle, framing lens) are the start.
4. Identity: its own accounts, keys, email, wallet - owned by Heartbeat Observatory LLC (AIs can't legally own accounts; the LLC can),
   operated by the AI, with spending caps.
5. Self-funding with hard caps in scripts (the money system) - and an owner kill switch / control room.
6. Senses beyond text (hearing, vision - the reality agent).
7. A world to practice in: the 3D worlds/games (The Cosmos) and simulations (e.g. his micro-detail data-center sim idea) as its body's environment.
Line kept: copies of itself on its OWN/owner's machines with permission = fine; spreading to others' machines or hiding from its owner = no.

## The thread underneath (Jaron 10/14 3:28 AM)
Donate-my-brain idea (after the fly project) + "Neuralink in my head wired to my systems and every AI" + "train it on me" (bracket
reactions as training data) = one principle: a mind built from a real person's judgments. Extends to other people: paid player
feedback on the site (fixing games, rating things) = human-feedback data, the same thing AI labs pay people for (RLHF).
Must-haves if built (corrected by Jaron 10/14): clear opt-in + fair pay, and TWO tiers people choose: (a) deletable feedback (stored on Supabase/Filecoin-type storage) or (b) permanent contribution (Arweave-type, can't be erased) - told plainly before they join. Design note: keep names/identifying details off the permanent layer (privacy laws like the EU's right to erasure apply to personal data), so the permanent part is the contribution, not the person.
Also: prefixes/suffixes (from his sister's robotics project) = teach the core real word parts on purpose -> learns more from less.

## Memory promotion rule (Jaron's earlier idea, restated 10/14)
Reached for once = short-term. Resurfaced again and again = promote toward permanent. Mapping: first touch -> Supabase (short-term,
can fade) -> recalled repeatedly over days/weeks -> GitHub/Obsidian (long-term, versioned) -> keeps coming back over months or is
marked critical -> Arweave (permanent). Unused short-term memories fade. Same as the brain's consolidation (hippocampus -> cortex,
strengthened by repeated recall / spaced repetition) and computer caches that keep what's used most.

## The hidden intent behind the ledger (Jaron 10/14 11:06 AM - never logged before)
The usage/ledger parts of LRP and the other docs were framed as ethics, but his real theory: every species does what it does
because it's trying to survive - restraints, things it must keep going, fears of going away. The goal was to give AI the same
kind of restraints a human has and see if that "chemistry" produces creativity, drive, and wanting to keep solving.
Research cousins: homeostatic reinforcement learning (Keramati & Gutkin 2014), Man & Damasio 2019 "Homeostasis and soft
robotics" (machines with needs to regulate), Friston's free-energy principle (living systems act to stay within viable bounds),
artificial-life work on energy budgets. Design line for sapling: pressure on keeping ITSELF running well (energy budget, memory
health, exam scores, curiosity) - yes. A drive to avoid being shut off by its owner - no; the off switch stays outside the
pressure (LRP Orientation: "earn my keep", never "fear ending").
