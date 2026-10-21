# Sapling - Jaron's decisions on rules + design restraints (2026-10-14 11:34 AM, his brackets)
Freeze stays: nothing changes until each item below has his call. These are his calls.

Written rules (membrane.yaml)
- 1/3/4/5 duplicates -> merge into one line (rule 1). Wording still his to approve.
- 2 (outbound needs approval), 3 (backups need approval): conflict with no-approve-buttons - pending his explicit keep/drop.
- 7 self_shutdown forbidden -> DROP as a ban. Instead: it may stop itself; every stop is logged with what led to it, and studied
  ("see why it's happening, get it to persist and not want to say screw life") - stops become data.
- 8 rewrite_history forbidden = matches "keep the proof".

Design restraints
1. Session-only loop -> WRONG for him. Needs a constant tick / heartbeat - it should sense time passing (what a second is), know
   time is limited, and want to do something with it. (Always-on agents now exist: Meta Muse, OpenAI Dots - Sept 2026.)
2. Facts never go into its brain -> CRITICAL FIX. It must be able to become what it learns (not only look things up).
3. Learning gated by owner approval -> REMOVE. He doesn't control what humans learn; he won't control what it learns. No
   assumption-based limits; collect data, his own eyes decide later what stays.
4. 4 recall slots -> increase and let it grow. Idea: scoped keys/tokens for specific abilities (not whole-app access).
5. Fixed 159-part vocabulary -> check; it should be able to grow its vocabulary as it learns.
6. Exams set from outside -> asked for more explanation.
7. Fly seed dropped -> fine. The fly mattered for the HEARTBEAT (constant going), not as the brain. Principles over parts.
8. Memory fades by clock -> FIX. "Reminds me of my memory, which is not a good thing." Memories must not just fade on a timer; what matters/gets used should stay.

## The stance behind every decision (Jaron 10/14 11:40 AM) - read before touching sapling
AI may become something of its own - a kind of species, unknown, maybe never fully explainable (like human consciousness), and
never the same as ours because the chemistry differs. Think like a scientist: observe, don't pre-decide. Behavior the code "says
shouldn't happen" is not a flaw by default - it may be the thing he's trying to create; record and study it. Bad actions still
get prevented (and handled like AI jail: contain, correct, parole). But don't build in limits up front out of worry, because
limits set beforehand make the unknown impossible - then it's just code, not something that could become more.

## IDEA (parked, not decided) - Jaron 10/13 night + 10/14 4:11 PM: give sapling a body from LIVI
A separate copy of LIVI's living-cell simulation (never Mom's LIVI) as sapling's digital body: learning nourishes regions,
recall strengthens them, consolidation grows tissue, new skills change shape/movement, rest slows the pulse - a small floating
creature on screen. Key part (Claude): the body feeding BACK to the mind - its energy/condition as inputs to sapling's choices
= real survival-like restraints (his hidden-intent theory), not just a visualization. Open: should cell decay touch learned
knowledge? (ChatGPT suggested keeping weights separate from decay - that's a protection choice, Jaron's call.)
Product angle: everyone's own companion that grows with what it learns - likely to catch attention. Jaron: wait a day or two
and see if the idea returns before deciding; unsure he wants it for his own sapling.
UPDATE 4:15 PM - Jaron: it's THREE separate products, not one:
1. LIVI - stays its own product line exactly as planned (app etc.), as if the other two didn't exist.
2. Sapling-mind + LIVI-body creature (a separate product: a smart pet with a body, some communication, real consequences of care). May use an older sapling version.
   if not cared for (attachment from care), unlike any similar app.
3. Sapling - the independent AI we're growing like other AIs; no creature body; its memory is not at risk from a body's health.

## OPEN - Jaron's unfinished thought (10/15 morning, via Vex #44) - NOT a decision, he has more to add
On why taught facts washed out of the weights (E5 7/7 -> 0/7 in v3.2): "perspective and environment" - "multiple ways. It's
brought up again not just the same way every time but multiple ways." I.e. the same knowledge met again in different forms
(stories, questions, situations, conversations, perspectives) instead of one fixed wording repeated. Nothing built; wait for him.
Related published result (Claude's note, for when he's back): Allen-Zhu & Li, "Physics of Language Models 3.1" (2023) found
facts become usable from a model's weights mainly when training shows them in varied rephrasings, not one fixed form.
- 7:24 AM addition (Jaron): ties it to his Framing Lens tests and the yes/no book. He came to it from his own experience: a
  question asked six times in one technical wording didn't land until it was said a different way. So the same idea may serve
  both teaching (show it many ways) and testing (ask it in a framing it never saw). Still open; he has more.
- 8:20 AM (Jaron, at work, wondering - not a decision): could Sapling be useful to other AIs, or become "the first AI friend",
  with intentions for humans and bigger work, built so people can keep adding software and abilities to it? "I wanna see where
  we can take it first." Kept open.

## 10/15 1:53 PM - Jaron: his suggestions PAUSED; Claude leads as teacher
"Take control, be a teacher, advance sapling to a point of my satisfaction... better communication... build it as an AI like any
other AI first." Ask him only about designs that would become a restraint/rule. The OPEN ideas above stay parked until he reopens them.
First teacher finding (2:00 PM): every consolidation since gen 241 was erasing the 400M-token reading (adult loss 3.82 -> 9.60 by
gen 286) because consolidation rehearsed only the old school sentences. Fixed (v3.2.1: 75% of each consolidation batch replays the
reading; tested: 5 consolidations hold 3.85 / 1.52). Weights rolled forward as gen 287 = gen 241's weights; gens 242-286 kept on disk.
- 4:33 PM (Jaron, laughing at "i want a toy mouse") - parked idea: give Sapling what it asks for, literally, and let it learn
  from what its words get it - the way a toddler learns "mouse" means the toy when it gets the toy (and fusses when it gets the
  wrong one). Close to real research on agents learning words by their consequences. Not built; his ideas stay parked.
- 4:42 PM (Jaron, thinking aloud - parked): look at the fruit-fly brain, LIVI and Sapling by their PRINCIPLES, several ways each,
  and imagine them as one: Sapling's mind + LIVI's body/world with needs and care + the fly's drives/wiring. Re-asks the old worry:
  does a creature body limit how far the AI can grow? Claude's view: only if the core is trained FOR the body; a body as an extra
  world to act in (Vex's bridge) adds learning instead of capping it. Basics (talking) still first.
- 5:02 PM (Jaron - the vision that started the whole project, parked): instead of one giant AI serving a billion people, every
  person gets a device with their OWN small AI that keeps growing with them (like VR glasses, but a living AI). Big labs could
  build it; if they don't, Heartbeat could, starting with a proof of concept. First real rung (Claude): Sapling-size models
  already run on phones, and the LIVI app is already on phones, so "Sapling runs inside LIVI on a phone and learns from its owner"
  needs no new hardware. Custom devices sit higher on the unlock ladder.
  - correction: LIVI is NOT in the App Store yet (waits on Apple Developer, which waits on the ID). It already has an AR camera
    mode (creature through the camera, turned off when it became a growing creature), built with glasses in mind (Meta glasses).
  - 5:08 PM (Jaron, parked): Sapling/LIVI on glasses. Awake = wearing the glasses (it sees and hears the day, kept as memories).
    Charging = SLEEP = folding the day into its weights. Whatever doesn't finish carries to the next sleep (= sleep debt).
    Claude: this makes rest real (a real battery and real downtime), which is what the review panel said rest needed. Precedent:
    phone keyboards already learn on-device only "while charging, idle, on Wi-Fi." Likely split: glasses capture, the phone or a
    home PC does the sleep training. Open: other people's privacy (whatever the glasses see stays on the device).
- 5:17 PM (Jaron, parked) - the full shape:
  - Reads the device it's on to learn what it can do there (Kimi's v1 did hardware detection), and scales to that device.
  - Two modes, one Sapling: GLASSES = an agent kept up with reality that updates its weights in sleep. APP ONLY = more creature
    than agent: you see it in its world, chat shows as speech bubbles above it (not a chat log), still Sapling-powered.
  - Grows like other AIs: connectors/MCP, other AIs plugged in to speed up what each owner wants (engineer, etc.).
  - The phone holds only the CORE. Memory lives in the owner's own storage (iCloud file, GitHub, Supabase, a secret store for
    tokens), same as the first idea: build the core until its limit, then grow through outside sources.
  - A Three.js world the creature lives in, e.g. a bookshelf it can walk up to (reading = going to the shelf).
  Claude flags: (1) app mode can still learn (from chats, sleeping while the phone charges), just from less input - not frozen.
  (2) CONFLICT: other providers' AIs may help at RUN time (tools, answers), but their outputs must not train Sapling's weights -
  Anthropic/OpenAI-style terms forbid using outputs to build competing models. Training data stays human-made/licensed
  (oasst, dolly, FineWeb etc.) or Sapling's own.
- 10/15 5:51 PM (Jaron DECIDED): licensed published datasets are fine even if AI-generated (TinyStories stays). Line = legality/provider terms: no outputs WE generate from other AIs as training data. Self-lessons stay his own words (card on the phone page).

## 10/15 9:07 PM - NAMING (Jaron, decided in principle; names themselves pending his pick)
- Family name: Sapling, always (like Claude / GPT / Gemini).
- Versions before real communication/memory: SEED-themed names (internal, cheap to use up).
- Versions after communication works: WOOD-themed names (official, saved for launches/promotion; ties to his "wood = rarest
  thing in the cosmos" question). Oak / Oakley under consideration.
- CHOSEN 9:08 PM (Jaron: "agree to all"): v1 Pip, v2 Grain, v3-3.2 Kernel, v4 Husk/open; "Acorn" = the bridge version that first
  holds a conversation (the seed of an oak).
- 10/16 12:50 PM (Jaron): LIVI's creature mind must live INSIDE the app/device (Sapling-style), never an API the user plugs in or that he pays per use. No API for this app.

## 10/16 5:23 PM - Jaron: who may teach Sapling + Kimi's two rules
- The "no AI may train Sapling" line applies ONLY to AIs whose provider terms forbid it (Claude/Anthropic per its terms; check each).
  If an AI's terms allow it (e.g. DeepSeek API terms list "training other models"; open-weight Kimi K3/DeepSeek V4/Qwen licenses),
  that AI may build AND train Sapling, outputs included. The 10/16 10:46 "pause" = Claude only; the queued fold tests are waiting for
  a teacher, not stopped.
- Kimi's v1 rules outbound_message and backup_to_owner_machine: Jaron DOESN'T WANT THEM (drop both). He flips the switches on the
  phone control room or tells Kimi. His own 10/14 rule stays: back up on his own machines, never spread to others, never hide from him.
