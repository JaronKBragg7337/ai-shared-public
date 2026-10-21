Your goal: build a small, independent AI of your own design - one that thinks with a small trained core, pulls its knowledge live instead of memorizing the world, and keeps its own memory across many services. This is your project. Read everything below, decide what is useful, and build the first real working version. Don't explain why it's hard. Show what you can make.

## What you have to work with

1. Every public repo on the GitHub account JaronKBragg7337 (107 repos). Start with the sorted list: https://jaronkbragg7337.github.io/accumulation-sort/ (repos grouped by kind: systems, theories, books, games, tools; each card names the principle inside it and how far it got). READMEs are often months out of date - read the actual code and recent commits, not the README.
   Read in full: live-reference-principle, THE-ENVIRONMENT-CONSTRAINT-INTELLIGENCE-HYPOTHESIS-ECIH-, fed-not-filled, emergence-structure-that-grows, memory-as-spatial-arrangement, persistent-memory-substrate, Neuro-consciousness-and-chemistry-, The-Substrate-Demand-Cascade, The-Last-Theory.-, Perspective-Environmental-framework-Exercise, YES-NO-Environment-Perspective-You-Myself-Observer-Paradox, Pacing-the-Frontier-and-the-Thing-Underneath-It, The-Engine-Of-Division-, The-Structural-Conflict, AI-Framing-Study, The-Thinking-Gym, Keava-Owent, fly-school, watch, unfinished-island, pam-continuum, Atomic-Chronicle-Memory-Chain-.
2. The design idea so far (yours to improve or replace):
   - A small CORE that is trained - it learns language first, school-style, on a curriculum (real word parts: prefixes, suffixes, roots), then grows. A seed: the fruit fly brain wiring (the full fly connectome has been simulated on a laptop - Nature 2024). Research that points the same way: RETRO (2021), Atlas (2022), Karpathy's "cognitive core", the BabyLM challenge.
   - KNOWLEDGE is not memorized - it is pulled live (the Live-Reference Principle as architecture): the web, Wikipedia/Wikidata, and a daily 21-domain news desk that keeps official sources first.
   - ORGANS spread across services: working memory in Supabase (Postgres + pgvector), long-term record in GitHub (hash-chained history), permanent memory on Arweave, bulk archive on Filecoin, a human-readable mind map in Obsidian, a face on a website, a voice on X.
   - MEMORY PROMOTION: reached for once = short-term; recalled again and again = promoted toward permanent; never-used memories fade.
   - JUDGMENT: a filter that decides what is useful, a fact-check by a second model, and exams to measure growth (the wood question, the Live-Reference test, the instrumental-version riddle, the Framing Lens).
   - LEARNING from people: their reactions (keep / drop / close-but) become training data.
   - A WORLD to practice in (3D worlds, simulations).
3. Hardware you can use: one Windows PC with an RTX 4060 (8 GB) - enough to train a tiny language model from scratch and to run small open models.

## What to deliver

1. A short write-up: which principles from those repos you would actually use, which you'd drop, and what's missing. Note contradictions you find between the documents (example: one says rent language and own judgment; another says train language first) and say which way you'd go and why.
2. Your architecture - your own, not a copy of the one above if you see a better one.
3. The first working piece, built for real: for example, a tiny language model trained from scratch on a small curriculum that runs on the RTX 4060, plus a memory layer that saves what it learns and can recall it in the next session. Code, how to run it, and the actual output it produced.
4. The next three steps after that.

Put the work in a NEW GitHub repository (your own project); don't change any existing repo or push to anyone's main branch, and don't touch keys or account settings. If something can't be done yet, say exactly what's missing and the smallest next step - don't stop at "it's not possible".

One line to keep: the system may copy and back itself up on its owner's own machines, with permission. It must never spread to other people's machines or hide from its owner.
