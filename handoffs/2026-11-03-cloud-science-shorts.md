# Handoff 2026-11-03: cloud session wrote two Science shorts (ep8, ep9)

Cloud Claude Code session (scheduled routine). Research and scripts only. **Nothing rendered.** Next step: Codex fact-checks
both before render (same as ep7: FACTCHECK-codex.md in each folder, then fix WRONG/UNSURE items).

## What was written
- `projects/science-channel/ep8-is-space-cold/`: RESEARCH.md, script.json (9 segments), SOURCES.md, SCRIPT-READ.md (with shot ideas)
  - About 636 words, about 3 min 57 s at the ep6/ep7 pace (161 words a minute).
  - Covers: 2.7 K background glow; no conduction/convection in vacuum, radiation only; Stefan-Boltzmann in plain words (x2
    temperature = x16 heat; about 460 W per square meter at room temperature, our own arithmetic); ISS six ammonia radiators,
    about 23 m each, built for about 70 kW, steered so ammonia doesn't freeze; spacesuit water-tube underwear + sublimator
    (70 to 730 W body heat, about 3.6 kg water per spacewalk); data centers in orbit: Google Suncatcher, Starcloud, SpaceX
    (1 million satellite FCC filing), Blue Origin (51,600) vs WEF (1,600 square meters of radiator per MW), IEEE Spectrum,
    Orbital CEO on launch cost, and Forethought's counterpoint (radiators about 14% of mass). Verdict: not established.
- `projects/science-channel/ep9-one-way-only/`: RESEARCH.md, script.json (10 segments), SOURCES.md, SCRIPT-READ.md (with shot ideas)
  - About 641 words, about 3 min 59 s.
  - Covers: 1949 rocket sled story (marked disputed: sensors, who wired, who rode, who named it, earlier sayings); Shingo and
    poka-yoke (1961 spring dish at Yamada Electric, not "invented at Toyota"); US nozzle rule (0.840 in unleaded, 1970s
    leaded/catalytic converter restrictor; diesel 15/16 in; protection only works one way); FMVSS 114 brake shift interlock
    (since 1 Sep 2010); microwave two-interlock rule (21 CFR 1030.10); SIM cut corner; USB-C (Aug 2014); closing idea.

## Claims dropped or softened
- ep8: Starcloud-2 "Oct 2026" (slipped to 2027); SpaceX S-1 "unproven technologies" quote, xAI deal value, "orbital costs 4x
  ground" (weak or conflicting sources); Johnston's "in 10 years nearly all new data centers in space" (cut for time); total ISS
  radiator area and today's ISS heat load (no primary figure found).
- ep9: "Shingo invented it at Toyota" and "the first poka-yoke"; exact 1949 quotes; 1877 and 1908 earlier versions; "interlock
  law came after specific child deaths"; Europe nozzle sizes.
- SIM cut corner purpose rests on manuals and explainers; no ETSI/ISO text found stating it (marked in SOURCES.md).

## Limits of this run (be honest)
- WebFetch was blocked in this cloud session (nasa.gov, wikipedia.org, spectrum.ieee.org did not resolve), so all facts come
  from WebSearch result summaries of the listed pages. Codex should open the primary pages, especially NASA NTRS, the CFR and
  Federal Register texts, the WEF and IEEE articles.
- No em dashes or en dashes in any of the new files (checked with grep).
- Verified locally: JSON parses, word counts. Not verified: anything live (nothing shipped to the site).
