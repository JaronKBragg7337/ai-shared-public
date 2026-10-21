# MaleCNS / FlyWire simulation runtimes used in the September 2026 demo wave

Research date: 2026-09-12. Scope: open-source runtimes that can actually advance a FlyWire/MaleCNS connectome and that are directly tied to, or technically representative of, this week's Beat Saber, Doom, Bitcoin-trading, FruitFly Capital / fly-finance demos.

## Bottom line

There is not one canonical "MaleCNS runtime." The viral projects are mostly separate LIF-style simulators built around the same public connectome, with engineered sensory injection and engineered motor/readout mappings.

For our purposes there are three especially useful runtime families:

1. **DOOMFLY / Stonkfly native runtime** — full retained MaleCNS v1.0, Python orchestration plus a compiled C++ neural kernel. CPU/real-machine oriented; no GPU requirement. This is the strongest directly verified lineage for the Doom and $100 Bitcoin/Coinbase demos.
2. **fruitflydev `flysim` runtime** — NumPy/SciPy CPU LIF over a large MaleCNS graph, plus a real mushroom-body plasticity module. This is unusually easy to repurpose because external input is literally `{neuron_indices: rate_hz}` and readouts are selected populations. It powered the flycoin / browser / token-launch demos and is the clearest open implementation of the "learning mushroom body" claim.
3. **Browser/WASM/Web Worker runtimes** — smaller/filtered or differently packed connectomes can run client-side. `fly-escape` (Rust→WASM) and `snedea/flybrain` (JS Web Worker) prove that the simulation does not inherently require a server or GPU. They are important deployment references even though they are not the exact runtime behind Doom/Stonkfly.

The **Beat Saber demo is public, but I could not verify a public repository for Lyra Bubbles' exact Beat Saber runtime** as of this research pass. The creator explicitly said the shown motor behavior was overfit to a replay while visual reactivity / RL was still being developed. Do not silently treat DOOMFLY, flycoinrh, or another repo as the Beat Saber source code.

Likewise, I found **no verifiable public FruitFly Capital backend repository**. Its deployed frontend does reveal a `brian2-malecns-v1-realtime-*` WebSocket brain protocol and the sensory/motor message shape, so the runtime family is partly identifiable even though the backend source is not auditable. Keep that distinction in our architecture notes.

## 1. DOOMFLY — Alex Wormuth / nftechie

Repo: https://github.com/nftechie/doomfly

Direct demo lineage: Doom. Stonkfly later adapts this connectome importer, inferred visual projection, spiking kernel and baseline-centered plasticity implementation.

Runtime: Python 3.11 orchestration + native C++ compiled neural kernel; ViZDoom supplies frames. Full retained graph reported as 166,700 neurons, 25,582,938 directed connection rows, 124,177,617 contacts.
### GPU?

**No GPU required.** The published run instructions require Python 3.11, a C++ compiler, several GB of RAM and the downloaded MaleCNS files. The project warns against multiple full-graph jobs on a small machine. A GPU is not part of the documented neural runtime.

### Sensory input

Each real ViZDoom frame is projected onto modeled fly visual inputs: **3,335 R1–R6 brightness inputs + 811 R8 color inputs**. These are inferred/engineered retinal proxies, not a validated reconstruction of fly optics.

Conceptually the adapter is:

`environment frame -> retinal projection -> selected sensory neuron stimulation -> recurrent MaleCNS propagation`

### Motor/readout

The fixed controller reads named descending-neuron populations. **DNp20 right-minus-left firing rate** drives turning (`clip(0.12 × ΔHz, -6, 6)` degrees/game tic). **Summed DNpe017 firing** drives forward motion (`clip(0.4 × summed_Hz, 0, 20)`), and any DNpe017 spike presses attack for one tic. The rates use a 100 ms exponential filter. Those assignments are explicitly described as an engineered brain-computer interface rather than established natural fly motor semantics.

### Mushroom-body learning?

**Optional/experimental, yes in current learning variants; no in the fixed baseline.** The current v6 learning path uses KC + dopamine activity to modify **4,184 existing KC→MBON11 connections**. Nonfatal Doom damage schedules a 200 ms artificial aversive input to two **PPL101** dopamine cells. The repo is careful that this has *not* demonstrated learned survival; its current v6 candidate failed visual, conditioning and survival validation gates.

Important historical note: the repo's neuroscience review dated 2026-09-05 found that the then-current implementation had no valid synaptic plasticity. The later `doom_learning_v*` work added explicit candidate plasticity. Do not cite early Doom clips as proof that mushroom-body learning was already working.

### Edge/serverless fit

**Cloudflare Worker:** No for the full runtime. Workers currently cap an isolate at 128 MB; this runtime needs several GB and native compiled dependencies / full graph state.

**Vercel Function:** Practically no for the full persistent simulation. Vercel Node/Python functions can have 2–4 GB RAM depending plan and newer long durations, but the runtime needs persistent multi-GB graph/state, a compiled native kernel, ViZDoom, and continuous closed-loop execution. A Vercel function could proxy/control a separately hosted simulator, not sensibly *be* the simulator.

**Supabase Edge Function:** No. Hosted Edge Functions are capped at 256 MB and 2 seconds CPU per request, far below this workload.

**Real machine / VM / container:** **Yes; intended deployment.** A Linux host/container or our MSI is the natural target. The UI can live at the edge while the brain stays on a machine.

Sources: repo README and neural docs: https://github.com/nftechie/doomfly ; current platform limits: https://developers.cloudflare.com/workers/platform/limits/ , https://vercel.com/docs/functions/limitations , https://supabase.com/docs/guides/functions/limits
## 2. Stonkfly — Alex Wormuth / nftechie

Repo: https://github.com/nftechie/stonkfly

Direct demo lineage: the viral **"I gave the fly brain $100 to trade bitcoin"** Coinbase experiment. Stonkfly explicitly says its connectome importer, inferred visual projection, spiking kernel and baseline-centered plasticity are adapted from DOOMFLY.

Runtime: Python 3.11 + C++17 compiler, full retained MaleCNS v1.0 graph: 166,700 neurons / ~25.6M directed connections. Recommended RAM is **16 GB**. Public Coinbase BTC-USDC data is converted into an RGB chart; default mode paper-trades.

### GPU?

**No GPU required/documented.** It is CPU/native-code oriented. The hardware pressure is RAM + sustained CPU rather than CUDA.

### Sensory input

Market prices become an **RGB candlestick/chart image**, then the same broad visual interface drives **3,335 brightness inputs and 811 R8 color inputs** in the MaleCNS graph.

This is the key reusable idea: arbitrary numerical state can be rendered/encoded as a sensory field instead of bypassing the connectome and directly handing it a feature vector.

### Motor/readout

Each market observation advances **500 ms of neural time**. The decoder takes mean right-DNp20 firing minus mean left-DNp20 firing: **≥ +2 Hz plus at least one DNpe017 spike -> Buy; ≤ -2 Hz plus at least one DNpe017 spike -> Sell; otherwise -> Hold**. A custom Coinbase AgentKit ActionProvider then enforces execution limits and can place Coinbase Advanced spot orders. The trading semantics are therefore an engineered output adapter around actual neural activity, not a naturally biological "trading neuron."

### Mushroom-body learning?

**Yes, candidate/experimental.** Positive portfolio P&L stimulates **15 identified PAM11 dopamine cells**; negative P&L stimulates **two PPL101 aversive dopamine cells**. A candidate memory rule modifies existing **KC→MBON** connections. The repo explicitly says profitable learning has not been demonstrated.

### Edge/serverless fit

**Cloudflare Worker:** No — 128 MB isolate memory is radically below the several-GB/16-GB-recommended runtime.

**Vercel Function:** No as a persistent brain. Even where memory/duration could start a reduced job, function lifecycle, native build/dependency packaging, graph size, persistent neural state and continuous market loop make it the wrong execution substrate.

**Supabase Edge Function:** No — 256 MB / 2 s CPU per request.

**Real machine / VM / container:** **Yes.** This is the intended class of host. For our architecture, keep the brain process on MSI or a proper compute VM; let Vercel/Cloudflare/Supabase expose telemetry, state, auth, queues or UI.

Source: https://github.com/nftechie/stonkfly
## 3. `fruitflydev/flycoinrh` + `flysim.py` — the most hackable CPU runtime I found

Repo: https://github.com/fruitflydev/flycoinrh

Direct demo lineage: fruit-fly browser control, Robinhood Chain token-launch experiments, and the creator's public **"learning mushroom body"** demo. This is not FruitFly Capital's verified repo, but it is highly relevant to that class of finance/on-chain experiment.

Runtime: pure Python/NumPy/SciPy LIF engine in `flysim.py`. The built graph reported by the repo is **165,122 traced MaleCNS neurons and 10,228,000 signed edges**. `build_graph.py` starts from the ~1.1 GB MaleCNS connection file and creates `build/graph.npz`.

### GPU?

**No.** `flysim.py` imports NumPy and `scipy.sparse`; its spike propagation is a CPU ragged-gather over CSC columns. Cost scales with neurons that fired rather than blindly multiplying the entire adjacency matrix each timestep.

### Sensory input API

This is exceptionally straightforward. `FlyBrain.run()` accepts:

`drive: dict { neuron_index_array: rate_hz }`

The rate may be one scalar for a population or a per-neuron array. The runtime converts Hz into per-step Poisson spike probability and gives selected neurons a suprathreshold kick. That means a new environment adapter only has to identify the desired MaleCNS sensory population and generate rates.

The browser demo samples screenshots through **892 retinotopic hex columns into L1/L2**. The repo also notes **2,635 ORNs across 53 receptor types** are available for an unused olfactory channel.

### Motor/readout API

`FlyBrain.run(..., record={name: neuron_indices})` counts selected population spikes and returns rates plus total/fired-neuron telemetry. The browser controller reads:

- **DNa02 left vs right** -> horizontal steering/cursor X
- **DNa01** -> forward / cursor Y
- **MDN** -> reverse
- **DNp09** -> stop/click

`FlyPilot.step(detail=True)` additionally returns fired-neuron and visual/motor telemetry. In other words, inputs and outputs are not hardwired into the core solver; adapters select populations around it.
### Mushroom-body learning?

**Yes — the clearest explicit implementation found.** `mushroom.py` implements dopamine-gated depression of **KC→MBON** synapses with an eligibility trace, floor and slow recovery toward baseline. It discovers reward-side vs punishment-side MBONs from relative PAM/PPL1 input in the connectome rather than hardcoding every MBON assignment.

Published module counts: **44,042 KC→MBON synapses; 27,939 reward-side; 14,349 punishment-side.** Only eligible synapses in the dopamine-addressed compartment are depressed. The code persists gain state in `mb_gains.npz` and can point `FLY_STATE_DIR` at persistent storage.

Important caveat: the *plasticity site/direction* is biologically motivated, but the demo's reward signal is engineered (for example novelty/reaching a page), not a literal fly reward.

### Edge/serverless fit

**Cloudflare Worker:** Full Python/SciPy runtime no. 128 MB is too small and the Python/SciPy execution model does not map directly to Workers. A substantial Rust/WASM rewrite plus a much tighter graph representation might make a reduced/browser-like version possible, but not this implementation as-is.

**Vercel Function:** The repo already uses **Vercel for the static site / a small serverless chain proxy**, but explicitly keeps the fly itself elsewhere. That separation is the right model. Full brain: no/practically unsuitable. UI/proxy: yes.

**Supabase Edge Function:** Full brain no. Supabase is suitable for state/telemetry/events, not 165K-neuron sustained CPU simulation.

**Real machine:** **Yes.** This is a particularly attractive candidate for our MSI because it needs no GPU and exposes a simple sensory-drive/readout interface plus persistent mushroom-body state.

Source files: https://github.com/fruitflydev/flycoinrh/blob/main/flysim.py and https://github.com/fruitflydev/flycoinrh/blob/main/mushroom.py

## 4. Beat Saber — Lyra Bubbles (`@_lyraaaa_`)

Public demo: viral 2026-09-08/09 Beat Saber clip.

**Exact open-source repo: not verified/found as of 2026-09-12.** I searched by creator handle, Beat Saber, MaleCNS, fly brain and GitHub. News/social mirrors describe the demo but do not expose a source repository that can be confidently attributed to it.

What the creator publicly clarified: the shown version was **not yet fully reactive autonomous play**. The motor system was overfit/trained to a recorded replay; visual-cortex reactivity was still being trained and the creator described RL work intended to reduce reliance on external signals.

Therefore:

- **GPU:** unknown for the exact runtime.
- **Sensory injection:** visual-reactivity work exists, exact neuron API/source not public enough to verify.
- **Motor readout:** motor activity was trained against replay behavior in the shown build; exact population mapping not verified.
- **Mushroom body:** **not verified**. Do not infer it merely because RL/dopamine language appears around other fly demos.
- **Cloudflare/Vercel/Supabase:** cannot honestly classify the exact implementation without code. The safest assumption is a real machine because Beat Saber itself and the training loop are stateful/native/interactive.

Coverage confirming the qualification: https://www.pcgamer.com/hardware/after-google-mapped-an-adult-male-fruit-flys-brain-software-engineers-made-it-play-doom-mario64-and-beat-saber/
## 5. FruitFly Capital (`@fruitflycap`) — frontend/protocol inspectable, backend source not found

Public site: https://fruitflycapital.xyz/ (the `.fun` URL redirects here).

**Exact open-source backend repo: not verified/found as of 2026-09-12.** However, the deployed production JavaScript exposes enough protocol metadata to identify the runtime family and the external interface. This is stronger than treating the entire implementation as unknown, but it still does **not** make the backend auditable/open source.

### Runtime / GPU

The live client identifies its brain source with a prefix **`brian2-malecns-v1-realtime-`** and labels the neural panel **`LIVE BRIAN2 -> DECODER` / `MALECNS: live Brian2`**. The browser connects to a separate backend over WebSocket; the brain is not executing in Three.js or in the static page.

**GPU:** no GPU requirement is demonstrated by the public client. Standard Brian2 has a CPU/C++ path, so CPU execution is plausible, but the unpublished backend could use another Brian2 device. Mark the exact backend accelerator as **unverified**, not "GPU required."

### Sensory input

The browser builds per-fly sensory state and sends WebSocket `brain_input` messages with `mode: "malecns"`. The client-side sensor structure includes bilateral eye summaries (luminance, contrast, optic flow), odor/antenna state, body/angular motion and contact. Its debug interface names encoded MaleCNS populations including **R8d** (visual), **ORN_DA1** (olfactory) and **JO** (Johnston's-organ/mechanosensory) stimulation. The client runs brain updates at up to about **2 Hz wall-clock**; this is the environment-to-brain cadence, not the neural integration timestep.

### Motor/readout

The WebSocket response exposes **descending-neuron rates, spike counts, a decoded flight command, MaleCNS command, low-level flight command and steering reference**. The rendered actuator command contains **forward thrust, vertical thrust, yaw torque, pitch torque and roll torque**. So the architecture is:

`browser world/sensors -> selected MaleCNS sensory encoding -> remote Brian2 simulation -> descending-neuron decoder -> 5-axis flight command -> Three.js fly body`

### Mushroom-body learning?

**Not verified.** I found no public backend code and no `mushroom` / KC-to-MBON learning evidence in the deployed client. The About page mentions each fly retaining a *memory of contact with a token habitat*, but that should not be equated with biological mushroom-body synaptic plasticity. Until backend code shows KC/MBON/DAN weight changes, classify FruitFly Capital as **learning unknown**.

### Edge/serverless fit

**Frontend:** yes — ordinary static hosting on Vercel/Cloudflare is fine. **Brain backend as currently architected:** no evidence it runs in an edge function; the production page talks to a persistent WebSocket brain service. A full Brian2/MaleCNS process belongs on a real machine, VM or container unless substantially repackaged. Cloudflare Workers (128 MB) and Supabase Edge (256 MB / 2 s CPU per request) are not credible full-brain hosts. Vercel Functions now support Python and WebSockets, but a persistent Brian2 state machine with large connectome assets/native compilation is still the wrong fit; use Vercel as the UI/control bridge, not the nervous system.

Production evidence inspected 2026-09-12: https://fruitflycapital.xyz/about/ and the site's then-current `assets/main-vltxEDJF.js` bundle. The closest fully open implementations for recreating the idea remain Stonkfly (market image -> neural buy/sell/hold) and `flycoinrh` (generic sensory/readout adapters + explicit KC->MBON plasticity).

## 6. Browser-capable reference: `dzhng/fly-escape` (Rust -> WebAssembly)

Repo: https://github.com/dzhng/fly-escape

Why it matters: it demonstrates that a MaleCNS-derived neural simulation can be compiled to WASM and run **entirely client-side in a browser**, with TypeScript handling the world/UI. It uses a **selected part** of MaleCNS rather than claiming the same full retained graph as DOOMFLY/Stonkfly.

**GPU:** no requirement documented. Simulation is Rust/WASM; ordinary build uses Bun + Rust/wasm-pack.

**Inputs/outputs:** the 3D world supplies modeled sensory conditions to the selected MaleCNS graph; neural activity drives fly movement. The exact game intentionally discovers behavior rather than imposing a desired strategy.

**Mushroom body:** no verified learning module highlighted in the published README; treat as fixed-weight unless code review proves otherwise.

**Deployment:** this is the strongest route for "serverless" because the brain does **not need to execute inside the serverless function at all**. Host static assets on Cloudflare Pages/Workers assets, Vercel, or Supabase Storage and let the user's browser execute WASM. That sidesteps edge CPU/memory/lifetime limits.

## 7. Browser-capable reference: `snedea/flybrain` (JavaScript Web Worker)

Repo: https://github.com/snedea/flybrain

Runtime: 139,255-neuron FlyWire FAFB v783 LIF simulation in a browser **Web Worker**, with ~2.7M retained connections in its packaged representation. This is FlyWire female-brain-era data, not MaleCNS v1.0, so use it as a deployment/runtime reference rather than a MaleCNS-equivalent scientific implementation.
**GPU:** not required for the neural solver; WebGL is used for visualization.

**Inputs:** UI/environment events such as food, touch, air, light and temperature are translated into sensory activity.

**Outputs:** activity is grouped/read as Sensory/Central/Drives/Motor and used for behavior.

**Mushroom body:** no verified plasticity/learning module in the published description.

**Deployment:** static hosting anywhere; brain executes in the browser, not Cloudflare/Vercel/Supabase compute. This is a useful pattern if we want a public interactive fly without keeping the MSI online.

## 8. Other runtime worth knowing: Eon Systems `fly-brain`

Repo: https://github.com/eonsystemspbc/fly-brain

This predates the September MaleCNS wave and is based on the FlyWire brain, but it is the most explicit multi-backend runtime collection I found: **Brian2, Brian2CUDA, PyTorch, NEST GPU and neuromorphic-chip targets**. Eon's embodied demo connected a fly-brain simulation to a MuJoCo body.

Use this when the question is "what execution backend can scale the LIF math?" rather than "what exact code ran Doom this week?" It proves GPU acceleration is available when desired, but the viral MaleCNS projects above generally do not *require* a GPU.

## Deployment matrix

| Runtime / demo | GPU required? | Mushroom-body plasticity | Cloudflare Worker | Vercel Function | Supabase Edge | Browser-only possible | Real machine |
|---|---:|---|---|---|---|---|---|
| DOOMFLY | No | Experimental KC→MBON learning variants | No | No / proxy only | No | Viewer only | **Yes** |
| Stonkfly | No | Experimental KC→MBON + PAM/PPL reward | No | No / API only | No | No | **Yes** |
| fruitflydev `flysim` | No | **Yes, explicit `mushroom.py`** | No as-is | No as brain; site/proxy yes | No as brain | Not as-is | **Yes** |
| Beat Saber exact build | Unknown | Unverified | Unverified | Unverified | Unverified | Unverified | Most likely |
| FruitFly Capital exact build | Not demonstrated; exact backend device unknown | Unverified | Brain: no; frontend can be static | Brain: poor fit; UI/bridge yes | Brain: no | Frontend only | **Yes / VM / container for backend** |
| `fly-escape` Rust/WASM | No | Not verified | Static host only | Static host only | Static host only | **Yes** | Yes |
| `snedea/flybrain` Web Worker | No | Not verified | Static host only | Static host only | Static host only | **Yes** | Yes |
| Eon `fly-brain` | Backend-dependent | Not the focus | No full sim | No full sim | No full sim | Not primary | **Yes; CPU/GPU options** |

## What I would use on the MSI

For a new AI-Shared fly-brain experiment, I would **not start by porting DOOMFLY wholesale**. I would clone and isolate **`fruitflydev/flycoinrh`'s `flysim.py` + `mushroom.py` as the first research runtime**, because:

1. it does not consume the RTX 4060, leaving the GPU free for Qwen/other models;
2. sensory injection is already a generic neuron-population/rate dictionary;
3. motor/readout selection is already generic population recording;
4. the mushroom-body memory is explicit, inspectable and persistent;
5. it is small enough to understand and instrument instead of treating the fly as a black box.

Then use **DOOMFLY/Stonkfly as a second reference implementation** for the faster native-kernel/full-retained-graph path and for comparing whether behavior survives a different solver.

For anything public-facing, use a split architecture:

`browser / Vercel / Cloudflare UI -> authenticated telemetry/control bridge -> persistent MSI brain process`

or, if we want zero MSI dependency:

`static site -> browser Web Worker/WASM brain`

The second path requires accepting a browser-oriented graph/runtime such as `fly-escape` or doing our own MaleCNS WASM packing; it is not a drop-in deployment of DOOMFLY/Stonkfly.

## Platform-limit rationale (checked 2026-09-12)

- **Cloudflare Workers:** 128 MB memory per isolate; paid HTTP CPU can be configured up to 5 minutes. Memory alone rules out the verified multi-GB full runtimes. Source: https://developers.cloudflare.com/workers/platform/limits/
- **Supabase Edge Functions:** 256 MB max memory, 2 s CPU/request, 150 s free / 400 s paid wall-clock worker duration. Not a sustained whole-connectome host. Source: https://supabase.com/docs/guides/functions/limits
- **Vercel Functions:** substantially roomier (2 GB Hobby; up to 4 GB Pro/Enterprise in documented function limits, with long-duration options), but still ephemeral function infrastructure. It is useful for API/proxy/orchestration, not a persistent nervous system with multi-GB state and native game/browser dependencies. Source: https://vercel.com/docs/functions/limitations

## Confidence / unresolved items

**High confidence:** DOOMFLY, Stonkfly, flycoinrh/flysim mechanics; their GPU requirements; documented sensory/readout mappings; presence/absence of their published plasticity modules; edge-platform limits.

**Medium confidence:** practical Vercel classification, because Vercel's 2026 duration capabilities are improving quickly. A carefully packaged *batch* connectome step might fit some Vercel plans, but that is different from hosting the continuous runtime.

**Unresolved:** the exact Beat Saber repository/runtime, and FruitFly Capital's **backend source repository / exact Brian2 device / mushroom-body implementation**. FruitFly Capital's deployed frontend protocol is partially verified (MaleCNS/Brian2 WebSocket input/output shape), so those interface facts are not unknown even though the backend code remains unpublished/unlocated.

### Primary repositories

- https://github.com/nftechie/doomfly
- https://github.com/nftechie/stonkfly
- https://github.com/fruitflydev/flycoinrh
- https://github.com/dzhng/fly-escape
- https://github.com/snedea/flybrain
- https://github.com/eonsystemspbc/fly-brain

---
## Cloudflare Containers note — different product from Workers

The **Cloudflare Workers 128 MB** conclusion above still stands for the product the question asked about. Cloudflare also has **Containers**, which are a different execution substrate and materially change the cloud answer: `standard-1` = 4 GiB / 0.5 vCPU, `standard-2` = 6 GiB / 1 vCPU, `standard-3` = 8 GiB / 2 vCPU, and `standard-4` = 12 GiB / 4 vCPU, with up to 20 GB local disk. That makes a CPU-only MaleCNS runtime plausible in a Cloudflare Container even though it will not fit in a Worker isolate.

Containers are usage-billed for provisioned memory/disk plus active CPU, with monthly inclusions on Workers Paid. Do **not** assume an always-on instance is only $10–20/month: provisioned memory alone can exceed that. Exact cost depends heavily on instance size, uptime and active CPU, so benchmark the chosen runtime before selecting the container size.

Sources: https://developers.cloudflare.com/containers/platform/pricing/ · https://developers.cloudflare.com/containers/platform/limits/ · https://developers.cloudflare.com/workers/platform/limits/
