# Science 8.7 — Does AI Know Physics? One Pour, Three Answers

**Channel:** Science (CH 8)  
**Why next:** Science 8.6, “Phobos: the moon that’s falling,” shipped 2026-10-14; no later Science episode exists.  
**Target runtime:** 4:25  
**Format:** 16:9 master plus a full 9:16 cut; realistic macro photography and matched photoreal 3D, not an AI presenter or cartoon diagram.  
**One-line pitch:** A real measured pour of water onto sand tests the difference between an image model’s plausible pixels, a fluid solver’s calculated motion, and AI trained to simulate physics.

## Editorial and visual rules

- Use three clearly labeled panels: **REAL REFERENCE**, **TEXT-TO-IMAGE OUTPUT**, and **NUMERICAL MODEL**. Never call the simulation “ground truth.”
- Do not invent a failure or a winner. Edit the comparison around the actual recorded pour, actual model output, and actual baked simulation. The narration below deliberately makes no claim about which looks best.
- The real reference must be real footage: 250 mL of water measured in a graduated clear bottle, poured onto a level tray of dry sand. Lock the camera, bottle height, pour angle, lighting, and tray position; record the pour rate and model/settings used. Do not substitute stock footage or a Blender render for the reference.
- Look: sunlight from one direction, physically based glass and water materials, natural sand grain variation, soft contact shadows, restrained color, no glowing UI. Use a 70–100 mm macro look, shallow but readable depth of field, and slow lateral camera moves only between pours. Keep the stream and impact point inside the central square so the vertical cut preserves the experiment.
- Show the model name/version and full prompt for the image output. Show Blender version, liquid method, gravity, domain resolution, time steps, and whether infiltration is modeled for the simulation. Keep source lines on screen long enough to read.
- Sound: close, natural water sounds for the real pour; quiet room tone elsewhere; no dramatic “error” sting. Narration target approximately 145–150 words per minute with short pauses for inspection.

## Scene 1 — Three waters, one question (0:00–0:30; 30 s)

**Seen:** A fast three-shot opening: the real bottle begins to pour; cut to the actual AI-generated image; cut to the Blender render at the same camera angle. Freeze all three in a labeled triptych. The real pour stays the visual reference throughout the episode. Title: **DOES AI KNOW PHYSICS?** Subtitle: **One pour. Three kinds of evidence.**

**Said:**  
“This is water recorded by a camera. This is water imagined by a text-to-image model. And this is water calculated by a fluid solver. Same bottle, same sand, same intended pour. But three very different ways of making a picture. So instead of asking which one looks impressive, let’s ask a harder question: does AI know physics? The careful answer starts with a distinction—AI is not one method, and a realistic image is not the same thing as a physical measurement.”

**On-screen source:** “Image generation example: Saharia et al., 2022 · Fluid model: Blender Mantaflow manual”

## Scene 2 — A picture built to fit a prompt (0:30–1:05; 35 s)

**Seen:** Show the real generated image full-screen, with the exact prompt typed once beside it. Then use a restrained inspection overlay: a circle where the stream meets the bottle, another at the impact point, and a line along the bottle’s silhouette. Do not circle a supposed error unless it is actually present. Cut to a neutral schematic: **TEXT → IMAGE MODEL → PIXELS**, not a fake internal visualization.

**Said:**  
“A text-to-image model is built to produce plausible pixels from a prompt. Imagen, one published example, combines language understanding with diffusion-based image generation. Our prompt describes the glass bottle, the water, the dry sand, the camera, and the sunlight. It does not provide a measured trajectory for every drop. So judge this result as a picture. Does the stream connect naturally to the bottle? Does the splash begin where the water lands? Are the glass, shadow, and water surface consistent? Those are visible checks—not proof of what the model understands.”

**On-screen source:** “Saharia et al., ‘Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding,’ NeurIPS 2022”

## Scene 3 — The measured reference (1:05–1:40; 35 s)

**Seen:** Real footage only. Insert a close-up of the 250 mL mark before the pour and the bottle afterward. Return to the locked wide shot, then a real high-speed close-up of the stream striking the sand. Finish on the wet patch spreading; no time reversal or synthetic replacement frames.

**Said:**  
“Now the reference. Two hundred fifty millilitres of water, one bottle, one level tray of dry sand, and a fixed camera. The measurement matters more than the cinematic lighting. Gravity shapes the falling stream; the impact throws water outward; and the wet patch changes as water moves into the spaces between grains. That downward movement is infiltration. Some water can vanish from the surface without vanishing altogether. This is the behavior the other two versions have to match—and the real pour, not our preference for one picture, sets the test.”

**On-screen source:** “USGS Water Science School, ‘Infiltration and the Water Cycle’ · Experiment: Heartbeat Observatory recording”

## Scene 4 — A solver, not a paintbrush (1:40–2:25; 45 s)

**Seen:** Transition from the real bottle to its matched Blender wireframe. Reveal the liquid domain, a brief voxel grid, and liquid particles; then render the same shot with glass, water, sand, and sunlight. Display the actual bake settings in a compact panel. Label the whole sequence **NUMERICAL MODEL — APPROXIMATION**.

**Said:**  
“Blender’s Mantaflow system approaches the pour differently. Its liquid domain is divided into cells called voxels, while particles carry the liquid through the simulation. By default, the solver can use the scene’s gravity. Here we match the bottle, the measured initial water volume, the camera, and Earth gravity—nine point eight one metres per second squared. The FLIP method is designed for lively splashes; APIC is another available method with different behavior. This is calculated motion, not just pixels fitted to a caption. But it is still a model. Blender’s own manual notes that resolution and time-step choices affect accuracy. A solver does not become reality merely because its render looks convincing.”

**On-screen source:** “Blender Manual → Physics → Fluid → Domain → Settings · Simulation settings shown from the actual bake”

## Scene 5 — Sand is more than a texture (2:25–3:05; 40 s)

**Seen:** Split screen: real infiltration darkens the sand on the left; the actual simulation result plays on the right. Below them, a simple cross-section shows surface flow above and pore spaces below. If the bake has no infiltration model, place a plain label over it: **SURFACE LIQUID ONLY — INFILTRATION NOT MODELED**. Do not fade or delete water to imitate absorption.

**Said:**  
“Here is the trap: a sand texture is not sand physics. A liquid solver can collide with a solid surface without reproducing water moving through a porous bed. If infiltration was not modeled, we say so on screen. We must not quietly shrink or fade the water and call that absorption. To compare infiltration, we would need a model for porous material and its measured properties. For this basic liquid bake, the fair comparison is narrower: the falling stream, the splash, and the surface flow. Knowing what a model leaves out is part of knowing what its picture means.”

**On-screen source:** “Blender Manual: liquid domains, particles, obstacles · USGS: infiltration and subsurface pore spaces”

## Scene 6 — AI can be trained to simulate (3:05–3:50; 45 s)

**Seen:** Replace the text-to-image schematic with a particle graph. Each particle carries a small state marker; connected particles pass information, and the graph advances from time **t** to **t + 1**. Use a simple published-method schematic, not footage claimed to be our own learned simulator. Then return to the three-way pour comparison.

**Said:**  
“Does that mean AI cannot do physics? No. In twenty twenty, Sanchez-Gonzalez and colleagues published graph network-based simulators that learned dynamics involving fluids, rigid solids, and deformable materials. Their system represented a physical state as particles connected in a graph, then learned how that state changed over time. That is a very different task from answering a caption with a convincing image. So the divide is not simply AI versus physics. It is between different inputs, different training goals, and different outputs. A learned simulator still has to survive comparison with observations, just as a conventional solver does.”

**On-screen source:** “Sanchez-Gonzalez et al., ‘Learning to Simulate Complex Physics with Graph Networks,’ ICML 2020”

## Scene 7 — The test is measurement (3:50–4:25; 35 s)

**Seen:** Real-time triptych, then the real reference alone. End on the empty bottle beside the measured mark, followed by a clean source card with the four references below and a link to the episode’s full settings and prompt.

**Said:**  
“So, does AI know physics? A photorealistic image can look right without calculating why it is right. A numerical solver calculates, but only within the assumptions and resolution we give it. A learned simulator can predict changing physical states, but it also needs testing. The useful question is not ‘Which frame impresses you?’ It is ‘Which method survives measurement?’ One bottle. One measured pour. Three kinds of evidence. The sources, prompt, and simulation settings are on screen. Heartbeat Observatory.”

**On-screen source:** “Full sources + experiment record + prompt + bake settings: heartbeatobservatory.com/tv/?ch=8.7”

## Sources and the claims they support

1. **Saharia, Chitwan, et al. (2022). “Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding.” NeurIPS 2022.** Supports the description of Imagen as a text-to-image diffusion model using deep language understanding; it is an architectural example, not evidence about an unnamed model’s hidden reasoning.  
   https://arxiv.org/abs/2205.11487  
   DOI: https://doi.org/10.48550/arXiv.2205.11487

2. **Blender Manual, “Domain Settings.”** Supports liquid domains, voxel resolution, default scene gravity, FLIP/APIC particle methods, particle behavior, and the effect of resolution/time-step choices on simulation accuracy. Record the manual version matching the production Blender version before rendering.  
   https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/settings.html

3. **U.S. Geological Survey, Water Science School, “Infiltration and the Water Cycle.”** Supports water moving into subsurface material, vertical/horizontal movement in shallow soil, and the role of pore spaces and soil characteristics.  
   https://www.usgs.gov/water-science-school/science/infiltration-and-water-cycle

4. **Sanchez-Gonzalez, Alvaro, et al. (2020). “Learning to Simulate Complex Physics with Graph Networks.” Proceedings of the 37th International Conference on Machine Learning, PMLR 119:8459–8468.** Supports learned particle/graph representations and learned dynamics for fluids, rigid solids, and deformable materials.  
   https://proceedings.mlr.press/v119/sanchez-gonzalez20a.html

## Fact-check and production gates

- The four external sources above were opened and checked against the outline on 2026-10-28.
- Before render, a second AI must check the final narration and the actual comparison edit, especially any newly observed difference between outputs.
- The real experiment record is a required source but does not exist yet. Capture it before locking scenes 3, 5, and 7; never write observed results ahead of the recording.
- Do not say “AI cannot do physics,” “the image model ran a fluid simulation,” or “the Blender simulation proves what water does.”
- Final video still requires the normal `verify_voice.py` gate and watched picture-and-sound review before release.
