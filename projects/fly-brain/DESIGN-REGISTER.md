# Fly brain — DESIGN REGISTER (what can change, what can't, who decided)
Written 2026-09-18 02:10 EDT by Claude Code at Jaron's request, while everything is still in one head. For the day he comes back and
says "it didn't go as intended — what in here can be changed, modified, extracted, and what has to stay or it isn't a system?"

Kinds: **LOAD-BEARING** = remove it and there is no system (not a rule, the physics of the build). **CHOSEN** = someone picked it;
changeable; who and why. **MEASURED** = the system told us; changes only by new measurement. **BORROWED** = someone else's, credited.
Decided-by: J = Jaron, C = Claude Code, G = Grok chat, O = ChatGPT chat, D = DeepSeek, L = lulzx/Mineplix, S = Shiu 2024 (field default).

## 1. The brain (runtime/flysim.py, versions/fly-v3/flysim_v3.py, gpu/flysim_gpu.py)
| item | kind | by | why / what breaks if changed |
|---|---|---|---|
| MaleCNS v1.0 graph: 165,122 neurons, signed synapse counts (graph.npz, CSR rows=POST cols=PRE) | LOAD-BEARING | J (the seed) | Everything is this wiring. Change the dataset = a different project. |
| Leaky integrate-and-fire cell: rest −52, reset −52, threshold −45 mV, tau 20 ms, dt 0.2 ms | CHOSEN (field default) | S | Could be conductance-based, adaptive, multi-compartment — nobody has per-cell parameters for 165k cells, so any change is invented numbers. Changing it re-opens Grade 0. |
| 0.275 mV per synapse contact, sign from transmitter prediction | CHOSEN (field default) | S | The one global unit. Global scaling was how ignition was fixed (v2/v3 ×0.35). |
| Refractory 3.8 ms (was 2.2) | BORROWED | L | Part of the anti-ignition recipe. |
| Sensory neurons receive no central input; edges under 6 synapses dropped (fly-v3) | BORROWED | L via C | Anti-ignition. O flagged it may delete real presynaptic inhibition onto ORNs — untested; changeable. |
| lLN1/lLN2 antennal-lobe local neurons flipped to inhibitory (fly-v9; v9b keeps lLN2T_a/b/c excitatory) | MEASURED + CHOSEN | C, O narrowed it | The table marks them ACh; biology says GABA. Without this one odour lights 160 glomeruli. v9 vs v9b is an open choice by evidence. |
| Per-type gains: PN ×2.96, APL ×1.44, KC ×2.01, KC threshold +6.7 mV, MBON ×2.87 (fly-v10 calib.json) | CHOSEN by search | C (search scored on the learned readout) | These are the "resistor values". Any of them can change; changing them un-freezes comm-loop-1. v7's KC→MBON ×24 is NOT in v10. |
| GPU kernel (torch sparse matmul, batched flies) | LOAD-BEARING for the two-fly work; CHOSEN implementation | C | Verified bit-identical to the CPU kernel; ~1 borderline spike flip per ~800 trials (chaotic cascade after). Any replacement must pass gpu/verify_gpu.py. |

## 2. Learning (runtime/mushroom.py, build/mb_sides.json)
| item | kind | by | why / what breaks |
|---|---|---|---|
| Plasticity only at KC→MBON synapses | CHOSEN (biology-first) | fruitflydev/flycoinrh, kept by C | The fly's real site. Could add other sites; that becomes "modified fly". |
| Dopamine-gated DEPRESSION only, no potentiation, no DAN feedback | CHOSEN (simplified biology) | flycoinrh, kept by C | Real fly also potentiates and has MBON→DAN loops. This is item 3 of Q-020 (expectation). Changeable; changes every learning number. |
| PAM side = reward, PPL1 side = punishment (mb_sides.json) | MEASURED vs Aso 2014 | C, checked by O | Aversive learning has existed from day one. Not yet run as the primary symbol. |
| lr 0.2 (frozen tests), 0.06 elsewhere; floor 0.25; trace ×0.55 | CHOSEN | C | lr 0.2 is what passed. The 0.06→0.2 transcription slip cost Gate 3 one declaration. |
| Dopamine is an injected scalar (`dopamine(+1)`) | CHOSEN (harness) | C | No internal reward computation. The first "restored" cell (state / prediction error) replaces this. |
| Eligibility: KC fired → trace 1 | CHOSEN (crude) | flycoinrh | O and G: should be a mask on strongly active KCs; changeable. |
| Forgetting: 6-hour half-life on the wall clock, on or off | CHOSEN | J (life-source rule) | Real short-term memory. NO consolidation step exists, so school pupils can never keep a lesson — contradicts intent (Q-020 item 4). Comm tests froze the clock. One number in SCHOOL settings. |

## 3. The tests and the discipline (Fly-Lab-2/comm_protocol.md, world/*_protocol.md)
| item | kind | by | why / what breaks |
|---|---|---|---|
| Predeclare every test; never redefine a failed one; new test = new seeds | LOAD-BEARING for credibility (not for code) | J | Remove it and nothing here is believable. Every pass and fail depends on it. |
| Freeze + fork with SHA-256 manifests (versions/) | LOAD-BEARING for reproducibility | J ("versions like model releases") | comm-loop-1 is the clean comparison for any modified brain. |
| Grade 0/0b organ check before and after (sugar→MN9, bitter veto, loom→DNp, JO-A→GF, no ignition) | CHOSEN gate | J ("eyes being eyes") + O's answer key | Known fails allowed: water, DM1 KC sparsity. |
| Symbols = odours (ORN_DA2 = A, ORN_DL3 = B, ORN_VM5d = C) at 40 Hz Poisson, 300 ms | CHOSEN | C | Morse was the first choice (J) and was MEASURED to be the wrong job for the MB (dot/dash 97% same KCs). Any odour works; C must not overlap A's KCs. |
| Answer channel = 5 PAM-side MBON types (09/01/05/03/06), fixed before the run | CHOSEN | C (from wiring); O insisted it be frozen | Test 8's top-K-by-wiring became test 9's fixed list. |
| Motor readout = DNa13 + DNa03 + MDN; decoded reply GO-TOWARD | CHOSEN | C | MDN alone drops ~30%. Direction is MEASURED. |
| Replay identical sensory realisations pre/post (paired) | CHOSEN (design) | O's review | Removing it buries the effect in noise. |
| 8 seeds; ≥6/8 or ≥7/8 lines; pooled z for small effects | CHOSEN | C | Per-fly z≥2 was under-powered twice; pooled + sign consistency is the fix for small consistent effects. |

## 4. The school (Fly-Lab-2/school/school.py, site /school)
| item | kind | by | why / what breaks |
|---|---|---|---|
| One brain per pupil, own memory file, persistent across restarts | LOAD-BEARING for "one fly, not a new fly each time" | J's diagnosis | The original fix. |
| Shifts (school-1..5 hours), meals, night sleep, morning exam before teaching | CHOSEN | J (the fly's life) | All schedule; all changeable. Meals are clock events until hunger exists (Q-019). |
| MSI = life source; off means off; lifeline to Supabase after every exam | CHOSEN | J | Pairs with forgetting above; revisit together. |
| Punish every miss in class | CHOSEN | C (school rule) | G: this is how 41k/44k synapses flattened. Changeable; likely should go. |
| Never script the classroom-with-doors | CHOSEN (principle) | J | Future; nothing built yet. |

## 5. The world (Fly-Lab-2/world/)
| item | kind | by | why / what breaks |
|---|---|---|---|
| Two brain objects / two processes; only the world file crosses; leak checks | LOAD-BEARING for "communication" claims | G's design, C built | Remove and it's one brain with an observer. |
| Channels: cVA (passive, on the cuticle) → ORN_DA1; wing air → JO-C/E/F; song pIP10 → wing MNs → JO-A | MEASURED which work | C pilots | Song: lesson does not reach it (measured). cVA→MDN saturates >4 Hz. Wing-air is graded both ends. |
| 1-D distance physics: d += K·(MDN_A+MDN_B)·bout; c = 1/(1+(d/D0)²); constants per protocol | CHOSEN (kinematic stand-in, like gait.py) | C | Every constant is a knob. Gate 4's gap may be world gain OR missing state — both stated. |
| MUTE / YOKED / SCRAMBLE controls | CHOSEN (design) | G, O | Without them nothing is unfakeable. |

## 6. Borrowed, credited
flycoinrh runtime (MIT); Shiu 2024 constants; lulzx/Mineplix anti-ignition recipe and gait.py (MIT); flybody + MuJoCo (Apache);
Aso 2014 sides; the answer keys and reviews from ChatGPT chat, Grok chat, DeepSeek (each named in FLY-BRAIN.md where they caught something).

## 7. What Jaron said he wants that the current design contradicts (open)
- Pupils should keep what they learn — the forgetting rule without consolidation prevents it (Q-020 #4).
- A fly that needs, loses, expects — the injected-dopamine, stateless board prevents it (Q-019, Q-020 #1–3).
- Back-and-forth communication — Gate 4 measured the reply arrives but cannot mean anything without state (same items).
- "Always on" — the school is scheduled trials, not a continuous life; needs a ticking world (not built).

## 8. What is NOT in this project's control
MaleCNS transmitter predictions (external; we patch known errors); per-cell physiology (unknown to science at this scale);
the GPU's floating-point order (documented, tolerated).
