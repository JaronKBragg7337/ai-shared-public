# Computational World - Prototype 0 (build brief, 11/23/2026)

**Jaron (2:18 PM, to ChatGPT, relayed):** "I think we might have Fable 5.2 work on a build today... there is even a time period I tried to have
AI reconstruct a GPU chip and even try to make a full data center inside a simulation. I think that might be too far and I think the
Minecraft one might be not enough, but if we just design our own way of something that doesn't exist, maybe a new game with certain
mechanics... could also do it on an application or does it necessarily need just the MSI... I think it starts from all of this connecting,
looking for principles, extracting things and finding what could work."
On CraftGPT: "it's slow because of how the system is made itself but the principle stands... if it's made a whole different way then what?"

**Dated history (ChatGPT's record, 11/23):** 9/28/2025 CraftGPT published (5.09M params on Minecraft redstone, ~2 h per reply at 40,000x tick);
9/30/2025 12:43 AM his first CraftGPT talk ("The principle alone of it being on a game should be huge?!"), same morning: could Stargate-scale
GPU infrastructure be done inside a coded game simulation; 11/24/2025 Fallout 4 settlement mechanics (terminals, switches, timers, lights) as
logic; 12/14-15/2025 simulated infrastructure (GPU, memory bandwidth, storage, network, power); 12/22/2025 many simulations together as an AI
chip; 8/9/2026 back to CraftGPT's principle with a different in-world mechanism.

**The question (ChatGPT's framing, Jaron's idea):** not "simulate a GPU" (simulation never makes computation free - the host still runs it),
but "what fundamental operations would a computational world need, and could a different arrangement do useful work with LESS work?"
e.g. only changed states trigger computation (good for sparse work, not dense matrix math).

**Prototype 0:** a small world whose mechanics ARE the computation. Primitives: State (values), Rules (transform values), Events (trigger
updates), Links (move information), Memory (history - Atomic Chronicle style, append-only), Verifier (checks outcomes). One world definition,
several engines: phone browser (CPU/WebGPU), MSI (CPU/GPU), cloud optional. A game in the sense you can place parts, connect them, and watch
information flow.

**The measurement:** the SAME checkable task three ways - (1) ordinary software, (2) hardware-style logic inside the world (the Minecraft way),
(3) original mechanics designed for the task (sparse/event-driven, reusable state, different memory relationships). Measure correctness, time,
memory, energy where possible. If (3) wins on a workload, find out why; if it loses, learn which assumption failed.

**Fits with:** Fable's "Bare against Built" SET-cards experiment (research/memory-lane/fable-read-2026-11-23.md) - the exact checker and the
append-only graded record are the same Verifier + Memory primitives; the SET puzzle can be one of Prototype 0's workloads.
Keep it SMALL: real measurements, not another blueprint. Public repo caution: creature stays out of research/.
