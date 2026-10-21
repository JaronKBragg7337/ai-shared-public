# Sapling v3 - school level 2 (real sentences) - 2026-10-14 evening (Claude Fable 5.1)

Jaron 7:02 PM: "school level 2: real sentences". Shipped: repo C:\Users\lilli\Projects\sapling (v3), phone page
heartbeatobservatory.com/admin/sapling/ (E6/E7 columns, core line, "What it wrote").

Where it stands
- Core v3: 11,919,744 params (d 384, 6 layers, 256 ctx), vocab 3,081+ (all 178 old parts kept + whole words).
- Same individual: memory.db + chain untouched (verified), gen keeps counting (151 -> 152), one ledger row
  `growth: core v2 -> v3`, v2 keepsake at results/checkpoints/core_v2_gen_0151.pt.
- Exams before -> after: E1-E5 held; E6 grammar 0 -> 14/48 (FAIL vs bar .60, kept); E7 reading 0 -> 27/40 PASS.
  E8 writing samples: results/writing_samples/.
- Heartbeat restarted on v3 (pid in results/heartbeat.pid). First consolidation (gen 153) drifted E7 27 -> 20;
  consolidation retuned (lr 1.5e-4, 2x level-2 rehearsal; DESIGN-CHOICES D14). Watch the next generations.
- Data: TinyStories GPT-4 validation split (CDLA-Sharing-1.0, checked live), data/tinystories/ (gitignored).
  None of Jaron's documents used (his step 2 - what it needs is in sapling/NEXT.md section 0).

Next thing: read E6/E7 per generation on the page for a day; if E7 keeps sliding, lower consolidate_steps
in membrane.yaml (owner's number) or raise rehearsal again.
