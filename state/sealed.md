# Sealed items - above Jaron's pay grade (rule: AGENTS.md, P-0179, Jaron 11/21 11:12 AM)

When something goes past what Jaron can judge (bio, chem, security, medical, legal, big money, or a breakthrough-level result), or
something goes wrong with real-world stakes:
1. Keep it private from the world. Never from Jaron.
2. Pause pushing that thing forward (other work goes on).
3. Get a qualified human professional in that field to look at it before going on. The AIs find the right person and write the
   plain summary for them; an AI review does not count as the professional.
4. List it here, put it in every handoff, and remind Jaron in each reply while it is open, even when he wants to keep building.
   (His words: "the team constantly reminds me that anything going forward needs to have someone as a professional in the field
   to look at things.")

| Opened | What | Why it is sealed | Professional needed | Status |
|---|---|---|---|---|
| 2026-11-22 11:40 AM | **MSI is damaging data now and then.** 3 signs in 16 hours: (1) 11/21 7:35 PM Sapling crashed on a memory row that parses fine afterward; (2) 11/22 ~5 AM ffmpeg could not read news frames that read fine elsewhere, then crashed; (3) 11/22 ~11 AM three map-briefing videos came out corrupted (in one, 11 bytes had turned to zero). Earlier: crashes 10/11 (bugcheck 0x20001) and 10/31 (sudden power-off; the news pipeline notes a CLOCK_WATCHDOG_TIMEOUT freeze). Disk reports Healthy, Windows logs no hardware errors (normal laptop RAM can't report them). Laptop: MSI Vector 16 HX A14VFG, Intel i9-14900HX, 2x16 GB DDR5-5600, BIOS E15M2IMS.910 from 10/15/2025. | Real-world stakes: silent corruption can reach Sapling's memory, backups, renders, repos. Hardware diagnosis is above Jaron's pay grade and ours. | A computer repair tech or MSI support (warranty?). They'd run a memory test (MemTest86 / Windows Memory Diagnostic), the Intel Processor Diagnostic Tool, and check for a newer MSI BIOS. | MOVED OUT 11/22 1:05 PM (Jaron: having someone else look at the MSI is "very different" from Sapling or the creature). Not a sealed item: it's the AIs' own machine. Now an AI-owned open problem in state/open-list.md; outside hands only as a last resort, after the machine is prepared. |
