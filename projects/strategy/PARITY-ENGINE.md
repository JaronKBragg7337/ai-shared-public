# Heartbeat Observatory — engine parity map

Written by Codex, 26 October 2026. Source audit of **C:/Users/lilli/Projects/hb-render**. Companion: [Studio parity map](PARITY-STUDIO.md).

**This is the scope for one general build, not a ceiling.** Take the union of the useful capabilities in Unreal Engine 5, Unity, Blender and three.js, then connect them to Heartbeat's Studio and vision work. A missing feature is a task. A finished bottle shot is a working example, not the engine's boundary.

## How to read this map

- **HAVE:** an implementation exists for the specific capability and limits stated in that row. This does not claim equal speed, quality or breadth to another product.
- **PARTIAL:** useful code exists, but a material part of the full workflow is absent.
- **MISSING:** no implementation found in the inspected engine source. The linked file identifies the inspected boundary or closest existing code; it is not an invented future file.
- In the comparison columns, **+** means an add-on, package, external tool or application code is needed. **—** means the product does not supply that workflow as a general built-in feature. A named official system can also require enabling its plugin. Features vary by renderer, platform and product version.

Read [README.md][readme], [out/NOTES.md][notes], the scene, rendering, loader, geometry, fluid and history code, browser entry points, MCP server and related tools. Searched src/, web/, tools/, mcp/ and site/ for the other systems. Code takes precedence over dated notes: for example sheen, clearcoat, a material/physics library, flow explanations and sand history now exist. README's last status line and MCP README's original tool count are behind the code. There are **129 parity rows: 18 HAVE, 49 PARTIAL and 62 MISSING**, plus the Heartbeat-specific direction table.

**Verification boundary:** this is a code and documentation audit. No render, simulation, browser session, deployment, hardware benchmark or vendor application was run. Existing measurements in NOTES are historical observations, not new tests. Vendor documentation was checked online on 26 October 2026; comparisons describe capabilities, not a promise that every feature works on every target. Some Blender manual pages were available through official indexed extracts when full-page retrieval failed; the linked versions are references, not a claim about the latest released version.

## Rendering and cameras

The baseline follows Epic's [path tracer][ue-path] and [rendering support tables][ue-render], Unity's [manual][unity] and [HDRP overview][unity-hdrp], Blender's [rendering/manual index][blender] and [Cycles sampling guide][cycles], and the [three.js API][three]. Unity's path tracing belongs to HDRP; three.js's core renderers are not an offline path tracer.

| ID / capability | Unreal Engine 5 | Unity | Blender | three.js | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|
| E-R01 GPU path tracing, multi-bounce light | Path Tracer | HDRP | Cycles | + tracer | HAVE | [src/tracer.wgsl][tracer], trace; [src/render.js][render]. Keep the compute renderer as a first-class final renderer. |
| E-R02 Fast interactive renderer | Real-time paths | URP/HDRP | EEVEE | WebGL/WebGPU | PARTIAL | [src/render.js][render] accumulates samples; [web/index.html][web] renders explicit jobs. Add a responsive scene viewport with a fast raster/hybrid path and progressive final quality. |
| E-R03 Hardware ray acceleration | Hardware RT | HDRP RT | GPU backends | Backend dependent | MISSING | [src/tracer.wgsl][tracer], traverse, uses a software BVH. Add a backend boundary for native acceleration where available; preserve the browser compute path. |
| E-R04 Global illumination and reflections | Lumen/path trace | GI/HDRP | Cycles/EEVEE | Probes/+ GI | HAVE | [src/tracer.wgsl][tracer], trace, computes indirect surface light and reflection. Add a separate real-time GI strategy under E-R02. |
| E-R05 Progressive anti-aliasing | Temporal/path samples | Pipeline options | Render samples | Renderer options | HAVE | [src/tracer.wgsl][tracer], jittered camera rays; [src/render.js][render], accumulation. |
| E-R06 Spatial denoising | Denoisers | HDRP denoising | OIDN/OptiX | + pass | HAVE | [src/post.wgsl][post], albedo/normal-guided a-trous filter. Preserve detail and expose controls. |
| E-R07 Temporal reuse and stable moving images | Temporal systems | Temporal systems | Renderer dependent | + passes | PARTIAL | [web/index.html][web], clipFrame, restarts the same sample pattern each frame. Add motion vectors, disocclusion handling and temporal denoising; fixed noise is not temporal reconstruction. |
| E-R08 Adaptive samples and light selection | Render controls | HDRP controls | Adaptive/light tree | + | MISSING | [src/render.js][render], pass, samples every pixel; [src/tracer.wgsl][tracer] selects lights uniformly. Add variance estimates, noise targets and power/spatial light selection. |
| E-R09 Depth of field | Cine camera | Camera/post | Physical camera | + effect | HAVE | [src/tracer.wgsl][tracer], concentricDisk/trace; [src/render.js][render], writeParams. Thin lens and focus distance exist. |
| E-R10 Motion blur and shutter controls | Supported | Pipeline options | Supported | + pass | MISSING | [src/tracer.wgsl][tracer] traces one instant; [src/camera-path.js][camera] gives one camera pose. Sample shutter time and moving/deforming geometry. |
| E-R11 Orthographic, panorama, stereo cameras | Camera types | Camera types | Camera types | Camera classes | MISSING | [src/render.js][render], writeParams, only builds perspective rays. Add projection types and calibrated cameras. |
| E-R12 Exposure and display tone mapping | Exposure/color | Exposure/color | Color management | Tone/color settings | PARTIAL | [src/post.wgsl][post] has an ACES-style fitted curve and sRGB; [src/render.js][render], autoExposure. Add configurable scene-linear spaces, OCIO-compatible transforms, HDR output and calibrated views. A fitted curve is not a complete ACES pipeline. |
| E-R13 Bloom, glare, lens and grading effects | Post process | Post process | Compositor | + passes | MISSING | [src/post.wgsl][post] only denoises and tone maps. Add an ordered effects/compositor graph with bypass and linear-light handling. |
| E-R14 Render layers, AOVs and object masks | Movie/render passes | Render/custom passes | Layers/Cryptomatte | Render targets/+ | PARTIAL | [src/render.js][render] has internal albedo/normal buffers and raw accumulation readback. Add exported depth, motion, IDs, light groups and compositing passes. |
| E-R15 Images and animation export | Movie Render Queue | + Recorder | Render output | Capture/+ encode | PARTIAL | [tools/render.mjs][still], PNG; [tools/clip.mjs][clip], PNG frames and ffmpeg MP4. Add EXR, alpha, image sequences with metadata, HDR and selectable delivery codecs. |
| E-R16 2D, sprites, text and vector overlays | UI/Paper2D | 2D/UI tools | Grease Pencil/text | Sprites/text/+ | PARTIAL | [src/necklace-overlay.js][overlay] draws history overlays. Add general sprites, text, vector shapes, 2D animation and resolution-independent composition. |

## Materials and lighting

Material references are [Blender Principled BSDF][principled], [three.js physical materials][three-material], Epic's [content/material pipeline][ue-content] and [rendering tables][ue-render], and Unity's [HDRP documentation][unity-hdrp]. Their material options are a capability target; they are not all present in every renderer.

| ID / capability | Unreal Engine 5 | Unity | Blender | three.js | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|
| E-M01 Metallic/roughness materials | PBR | PBR | Principled | Standard/Physical | HAVE | [src/scene.js][scene], packMaterial; [src/tracer.wgsl][tracer], evalOpaque. |
| E-M02 Color, roughness, normal, emissive maps | Supported | Supported | Nodes | Supported | HAVE | [src/gltf.js][gltf] and [src/tracer.wgsl][tracer], surfaceAt; packed glTF roughness/metallic channels are handled. |
| E-M03 Glass, water, Fresnel, absorption | Supported | HDRP options | Transmission/volume | Transmission | PARTIAL | [src/tracer.wgsl][tracer], fresnelDielectric/trace. Rough refraction and absorption exist; one inside flag is not nested medium tracking. Add medium stacks, thickness, correct mixtures and overlapping dielectrics. |
| E-M04 Fabric sheen and clearcoat | Material models | Shader options | Principled | Physical | PARTIAL | [src/tracer.wgsl][tracer], evalOpaque; [src/scene.js][scene], extra2. Basic lobes exist; finish energy conservation, multiscatter compensation and texture/import controls. |
| E-M05 Anisotropy, thin film and dispersion | Model dependent | HDRP/custom | Node/model options | Physical options | MISSING | [src/tracer.wgsl][tracer], Material/Surf, has no such parameters. Add independent models and reference scenes. |
| E-M06 Skin, wax, subsurface and hair shading | Skin/hair models | HDRP/custom | SSS/hair | Node/+ shader | MISSING | [src/tracer.wgsl][tracer], surfaceAt/evalOpaque. Add subsurface transport, thin translucency and strand shading. |
| E-M07 Layered/node materials | Material graph | Shader Graph | Shader nodes | TSL/nodes | MISSING | [src/scene.js][scene] packs a fixed record. Add typed material graphs that compile to all render backends. |
| E-M08 Procedural textures and material functions | Graph functions | Graph/custom | Texture nodes | TSL/custom | PARTIAL | [src/tracer.wgsl][tracer] has grain and wetness; [tools/anything-writer.mjs][writer] maps material words to scans. Add reusable noise, masks, coordinate spaces and functions. |
| E-M09 Displacement and subdivision | Mesh/material paths | Tessellation/custom | Modifiers/Cycles | Displacement/+ | PARTIAL | [src/scene.js][scene], heightfield displacement; [src/mesh.js][mesh]. Add arbitrary mesh displacement, subdivision and adaptive detail. |
| E-M10 Opacity, cutouts, decals | Supported | Supported | Alpha/nodes | Alpha/+ decals | PARTIAL | [src/gltf.js][gltf] turns glTF BLEND into a 0.5 cutout; [src/tracer.wgsl][tracer], traverse. Add actual alpha blending, transmission distinctions and layered decals. |
| E-M11 UV editing, baking and texture painting | UV/model tools | Import/+ authoring | UV/bake/paint | Import/+ authoring | MISSING | [src/mesh.js][mesh] creates UVs and [src/gltf.js][gltf] reads TEXCOORD_0. Add unwrap, packing, painting, baking and multiple UV sets. |
| E-M12 Shared physical material presets | Physical materials | Physic materials | Physics settings | + physics data | PARTIAL | [src/physics-library.js][physics] has water plus sand, dirt and concrete; [src/scene.js][scene] applies it. Extend to solids, cloth, acoustics and measured properties with provenance. |
| E-L01 HDR environment lighting | Skylight/HDRI | Environment | World shader | Environment map | HAVE | [src/hdr.js][hdr], HDR decode/CDF; [src/tracer.wgsl][tracer], sampleEnv, rotation/intensity and importance sampling. |
| E-L02 Point, spot, rect, disc, sphere and mesh lights | Light types | Light types | Light/emission | Light types/+ | HAVE | [src/scene.js][scene], light records; [src/tracer.wgsl][tracer], sampleLight. Includes sampled model-material mesh lights. |
| E-L03 Indirect sampling, portals and shadows | Renderer dependent | Renderer dependent | Cycles | Shadows/+ | PARTIAL | [src/tracer.wgsl][tracer], MIS, portalPdf, shadowTransmittanceTo. Portals exist, but glass-shadow handling has approximations and light units use a rough scale. Add physical calibration and broad validation. |
| E-L04 Caustics | Renderer dependent | Renderer/+ | Cycles options | + | PARTIAL | [src/tracer.wgsl][tracer], photons/causticFinish, deposits sky photons on an XZ receiver grid. Generalize to arbitrary receivers, colored transport and other light sources. |
| E-L05 Sun, atmosphere, clouds and weather | Atmosphere/clouds | Sky/VFX packages | World/volume nodes | Sky/+ | PARTIAL | [src/hdr.js][hdr] and [src/scene.js][scene] use a static HDRI. Add an actual sun/sky model, time of day, clouds and weather fields. |
| E-L06 Fog, participating volumes, smoke and fire shading | Volumetrics | HDRP/VFX | Volume shaders | Volume/+ | MISSING | [src/tracer.wgsl][tracer] has surface tracing only. Add volume grids, phase functions, emission and light sampling. |
| E-L07 Baked light, probes and reflection captures | Lightmaps/probes | Lightmaps/probes | Bake/probes | Probes/maps | MISSING | [src/scene.js][scene] builds no bake/probe data. Add portable caches for interactive and phone rendering. |
| E-L08 IES, light linking and shadow controls | Light controls | Pipeline controls | Light linking | IES/+ | MISSING | [src/scene.js][scene], lightDefs, lacks profiles and receiver groups. Add profile import, groups, visibility masks and explicit artistic overrides. |

## Physics and simulation

Epic's [Chaos overview][ue-physics] lists rigid bodies, destruction, cloth, vehicles, fluids, hair and flesh systems. Unity's [physics manual][unity-physics] supplies rigid-body/collider workflows; general liquid, soft-body and destruction systems need additional packages or code. Blender has [cloth][cloth], [soft bodies][soft] and the other [physics families][blender]. The [three.js physics guide][three-physics] explicitly describes separate solvers and wrappers. A water surface shader is not a fluid solver.

| ID / capability | Unreal Engine 5 | Unity | Blender | three.js | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|
| E-P01 Fixed time steps and advancing simulation | Chaos tick | Physics tick | Simulation/cache | + solver | HAVE | [src/fluid.js][fluid], step; [src/fluid-gpu.js][gpu], advanceTo. This currently applies to the fluid session. |
| E-P02 Water particles and liquid surface | Niagara Fluids | + solver | Mantaflow liquid | + solver | PARTIAL | [src/fluid.js][fluid], PBF/surface; [src/fluid-gpu.wgsl][solver]; [src/mc.js][mc]. Generalize beyond the current container/ground setup and validate conservation and collision behavior. |
| E-P03 GPU and CPU fluid paths | System dependent | + | Solver dependent | + | PARTIAL | [src/scene.js][scene], useGPU, requires a device, container, wet map and no emitter. JS fallback exists but does not carry every newer GPU feature/history. Publish a backend support table and match behavior. |
| E-P04 Emitters, sinks and multiple fluid regions | Niagara | + | Flow/effector | + | PARTIAL | [src/fluid.js][fluid], addEmitter; [src/scene.js][scene] has one fluid block. Add multiple domains, sources, drains and moving emitters across CPU/GPU. |
| E-P05 Viscosity, cohesion, surface tension and breakup | Solver dependent | + | Liquid options | + | PARTIAL | [src/physics-library.js][physics] and [src/fluid-gpu.wgsl][solver], ctlPass. Has cohesion and a neck pressure/breakup model; add general surface tension, non-water liquids and measured units. |
| E-P06 Wetting, absorption and runoff | Materials/+ coupling | + coupling | Dynamic Paint/+ | + | PARTIAL | [src/physics-library.js][physics], resolveSurface; [src/fluid-gpu.wgsl][solver], soakFold/soakSpread. Add arbitrary curved porous bodies, volume saturation, drying and evaporation. |
| E-P07 Splash, foam, spray and bubbles | Niagara Fluids | VFX/+ | Secondary particles | + | PARTIAL | [src/fluid-gpu.wgsl][solver], spawnPass, creates secondary splash particles and models glugs. Add general spray/foam/air phase; glug events are not a bubble volume solver. |
| E-P08 General collision shapes and contacts | Chaos shapes | Colliders | Collision objects | + solver | PARTIAL | [src/fluid.js][fluid], latheSolid/_collide; [src/fluid-gpu.wgsl][solver] uses ground grid and one lathe shell. Add meshes, convex/compound shapes, layers, contact manifolds and swept collision. |
| E-P09 Dynamic rigid bodies | Chaos | Rigidbody | Rigid bodies | + solver | MISSING | [src/scene.js][scene] statically places objects; rest is placement correction. Add mass, inertia, forces, torque, sleep and contact solving. |
| E-P10 Continuous collision and broad phase | Chaos | Physics options | Solver dependent | + solver | MISSING | [src/fluid.js][fluid], _collide, resolves penetration after movement. Add fast-body sweeps, broad phase and tunneling tests. |
| E-P11 Joints, constraints and motors | Constraints | Joints | Constraints | + solver | MISSING | [src/scene.js][scene] has no joint records. Add hinges, sliders, springs, limits, drives and break thresholds. |
| E-P12 Cloth and fabric collision | Chaos Cloth | Cloth | Cloth | + solver | MISSING | [src/scene.js][scene] and [src/fluid.js][fluid] contain no cloth solver. Add stretch/bend constraints, self-collision, pins, wind and sewing patterns. Sheen does not simulate fabric. |
| E-P13 Soft bodies, flesh and deformation | Chaos Flesh | + solver | Soft body | + solver | MISSING | [src/mesh.js][mesh] and [src/fluid.js][fluid] have no deformable solid state. Add volume constraints, elasticity, plasticity and deformable collision. |
| E-P14 Destruction, fracture and debris | Chaos Destruction | + | + fracture/tools | + | MISSING | [src/scene.js][scene] and [src/mesh.js][mesh]. Add fracture assets, bonds, stress, break events, debris and dust. |
| E-P15 Rope, cable, hair and grooming physics | Cable/groom | + | Curves/physics | + | MISSING | [src/mesh.js][mesh] and [src/scene.js][scene] have no strand system. Add rod constraints, strand collision and renderable curves. |
| E-P16 Vehicles, wheels and buoyancy | Chaos Vehicles/+ | WheelCollider/+ | Rig/+ | + solver | MISSING | [src/procedural.js][procedural], hull, and imported cars are geometry. Add tire/suspension models, drivetrains, floating bodies and fluid forces. |
| E-P17 Character controller and ragdolls | Character/ragdoll | Controller/joints | Rig/rigid body | + | MISSING | [src/scene.js][scene] has no character runtime. Add capsule movement, slopes, steps, joints and animation handoff. |
| E-P18 Smoke, fire, gas and heat | Niagara Fluids | VFX/+ solver | Mantaflow gas | + | MISSING | [src/fluid-gpu.wgsl][solver] is a liquid particle solver. Add pressure/advection grids, temperature, combustion and volume outputs. |
| E-P19 Sand grains, snow, mud and granular solids | +/specialized | + | +/nodes | + | MISSING | [src/fluid-gpu.wgsl][solver] stores moisture and dimples; sand grains do not move as bodies. Add a granular/deformable ground solver and material transitions. |
| E-P20 General particles and force fields | Niagara | Particle/VFX Graph | Particles/nodes | Points/compute/+ | PARTIAL | [src/fluid.js][fluid] has liquid emitters; [src/procedural.js][procedural] is geometry generation. Add reusable spawn/update graphs, wind, attractors, trails and rendering. |
| E-P21 Two-way coupling between solver families | System dependent | + | System dependent/+ | + | MISSING | [src/scene.js][scene] gives fluid static solids; it does not push them back. Add common force/contact exchange for fluid, rigid, cloth and soft bodies. |
| E-P22 Bake, checkpoints, rewind and cache editing | Caches/debugger | + recording/cache | Bake/cache | + | PARTIAL | [src/fluid-gpu.js][gpu] advances forward; [src/history.js][history] records selected outputs. Add complete restartable solver checkpoints, parameter versions and deterministic/tolerance-based replay checks. |
| E-P23 Inspect contacts, forces and numerical error | Chaos debugger | Physics debugger | View/cache tools | + | PARTIAL | [src/stats.js][stats], [src/wetstats.js][wetstats], [tools/probe.mjs][probe] measure fluid/flow/wetting. Add contact, energy/mass error and constraint views for every solver. |

## Animation, rigging and characters

The reference workflows are Epic's [Control Rig][ue-rig] and [Sequencer][ue-cinema], Unity's [animation system][unity-animation], Blender's [animation and rigging families][blender] and the [three.js animation APIs][three]. three.js supplies playback building blocks; a full authoring application still needs to be built around them.

| ID / capability | Unreal Engine 5 | Unity | Blender | three.js | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|
| E-A01 Camera paths and keyframes | Sequencer | Timeline/Cinemachine | F-curves | Tracks/curves | HAVE | [src/camera-path.js][camera], cameraAt, includes eased orbit/push/truck and Catmull-Rom keys. |
| E-A02 General object/property animation | Sequencer | Animation/Timeline | Keyframes/drivers | Keyframe tracks | MISSING | [src/camera-path.js][camera] only animates cameras; [src/scene.js][scene] flattens static object transforms. Add typed tracks for any animatable property. |
| E-A03 Timeline, shots, curves and clip layers | Sequencer | Timeline | Dope Sheet/NLA | Playback/+ editor | PARTIAL | [tools/clip.mjs][clip] and [src/camera-path.js][camera] make one clip. Add multi-shot timelines, curve handles, layering, nested sequences and markers. |
| E-A04 Skeletons, skin weights and deformation | Skeletal meshes | Skinned meshes | Armatures | SkinnedMesh | MISSING | [src/gltf.js][gltf] reads POSITION/NORMAL/UV but no JOINTS/WEIGHTS/skins. Implement import, GPU skinning, weight tools and rest poses. |
| E-A05 Morph targets and facial shapes | Morph targets | Blend shapes | Shape keys | Morph targets | MISSING | [src/gltf.js][gltf] ignores primitive targets. Add shape blending, animation tracks and facial controls. |
| E-A06 Rig authoring, IK/FK and constraints | Control Rig | Animation Rigging | Armatures/IK | + IK | MISSING | [src/scene.js][scene] and [src/mesh.js][mesh] contain no rig graph. Add controls, solvers, constraints and reusable rigs. |
| E-A07 Retargeting, root motion and blend trees | IK retarget/Anim BP | Humanoid/Animator | Actions/+ | Mixer/+ | MISSING | [src/gltf.js][gltf] does not read animation clips. Add clip import, pose blending, retarget maps and root motion. |
| E-A08 Mocap, tracking and performance capture | Live Link/MetaHuman | Packages/+ | Tracking/+ | + | MISSING | [src/gltf.js][gltf] and [src/scene.js][scene]. Add live/recorded pose inputs, calibration, cleanup, source references and retargeting. Vision experiments outside this repo do not make this engine HAVE it. |
| E-A09 Lip sync, gaze and expressive speech | Character tools/+ | + | Shape/rig/+ | + | MISSING | [src/scene.js][scene] has no speech/face channels. Connect phonemes, emotion, gaze and Studio audio through the common clock. |
| E-A10 Character authoring and customization | MetaHuman/Mutable | Assets/+ | Model/sculpt/rig | + assets/tools | MISSING | [src/procedural.js][procedural] has rocks/trees/rooms, no character builder. Add body/face controls, clothing fit, hair, attachments and reusable character assets. |
| E-A11 Navigation, behavior and crowds | Nav/behavior/Mass | AI Navigation/+ | + runtime | + | MISSING | [src/scene.js][scene]. Add nav meshes, steering, behaviors, animation events and crowd budgets. |
| E-A12 Retiming, slow motion and animation export | Sequencer/caches | Timeline/+ | Time remap/export | Time scales/+ | PARTIAL | [web/index.html][web], timeAt, and [src/history.js][history], frameTime, support clip time maps. Add reversible seek and export of object, skeletal and cache animation. |

## Terrain, foliage, worlds and modeling

World-building references include [World Partition][ue-world], [PCG][ue-pcg], Unity's [manual][unity], [Blender Geometry Nodes][geo] and [three.js geometry/object APIs][three]. Chunk ideas in this repo are proposals until an actual streaming path exists.

| ID / capability | Unreal Engine 5 | Unity | Blender | three.js | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|
| E-W01 Mesh primitives and generated shapes | Modeling tools | Mesh API/+ | Modeling | Geometries | HAVE | [src/mesh.js][mesh] and [src/procedural.js][procedural]: boxes, spheres, lathes, bottles, terrain, rocks, trees, hulls and rooms. |
| E-W02 Mesh editing, sculpting, modifiers and curves | Modeling/Geometry Script | + authoring | Full toolsets | Geometry/+ tools | MISSING | [src/mesh.js][mesh] generates meshes, not editable topology. Add selection, extrude/bevel/boolean, sculpt, curves and a non-destructive modifier stack. |
| E-W03 Heightfields and terrain generation | Landscape | Terrain | Mesh/nodes/+ | Geometry/+ | PARTIAL | [src/scene.js][scene], heightfield branch, supports displacement, dunes, ripples and local bumps. Add terrain layers, tiled editing, erosion, holes and terrain LOD. |
| E-W04 Terrain painting, roads, rivers and splines | Landscape/splines | Terrain/+ | Curves/nodes/+ | Curves/+ | MISSING | [src/scene.js][scene] has no paint layers or spline road/river system. Add editable splines linked to terrain and material changes. |
| E-W05 Foliage scatter and biomes | Foliage/PCG | Terrain/details/+ | Geometry Nodes | Instancing/+ | PARTIAL | [src/procedural.js][procedural], tree; [tools/anything-writer.mjs][writer] requests loose plant placement. Add rule-based scatter, density masks, seasons, wind and instancing. |
| E-W06 Modular buildings and reusable assemblies | Actors/PCG | Prefabs/+ | Collections/nodes | Object3D/+ | PARTIAL | [src/assembler.js][assembler], assembleBuilding, assembles facade pieces. Add whole buildings, roofs, interiors, reusable sockets and kit schemas. |
| E-W07 Procedural graphs and simulation nodes | PCG/Niagara | Graph packages | Geometry Nodes | TSL/+ tools | MISSING | [src/procedural.js][procedural] exposes separate functions, not an editable graph. Add typed nodes, fields, attributes, instances, baking and reusable groups. |
| E-W08 Persistent scene hierarchy and prefabs | Actors/components | GameObjects/prefabs | Objects/collections | Object3D | PARTIAL | [src/gltf.js][gltf] traverses hierarchy but bakes meshes to model/world space; [src/scene.js][scene] uses names. Retain stable nodes, parent transforms, instances and prefab overrides. |
| E-W09 Large worlds, chunks and streaming | World Partition | Additive scenes/Addressables | Linked scenes/+ runtime | + application | MISSING | [src/scene.js][scene] builds the full scene; [WORLD-CHUNKS-IDEA.md][chunks] is a proposal. Add spatial cells, asynchronous paging, origin shifts and persistent edits. |
| E-W10 Placement, snapping and support | Editor snapping | Editor snapping | Snapping | + controls | PARTIAL | [src/scene.js][scene], scene.rest, puts static props on earlier supports. Add interactive grid/surface/socket snapping, overlap checks and intentional placement overrides. |
| E-W11 Oceans, water bodies and weather interaction | Water/fluids | Water/VFX/+ | Ocean/fluids | Water/+ | MISSING | [src/scene.js][scene] has one local fluid block. Add ocean/river surfaces, wave spectra, shore interaction and links to actual simulation. |
| E-W12 Scans, point clouds and reconstructed scenes | Import/plugins | Packages/+ | Import/tracking/+ | Loaders/+ | MISSING | [src/gltf.js][gltf] loads triangle models only. Add point clouds, depth/camera calibration, splats and evidence-linked reconstruction without hiding invented regions. |

## Audio, scripting and editor tools

Epic supplies [MetaSounds][ue-audio] and [Blueprints][ue-script]; Unity has [audio][unity-audio] and editor/runtime APIs; Blender has [animation, scripting, sound and sequencer workflows][blender]; three.js exposes [audio and scripting building blocks][three]. Heartbeat Studio's audio engine is separate today, so it is not counted as engine audio already delivered.

| ID / capability | Unreal Engine 5 | Unity | Blender | three.js | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|
| E-T01 Audio playback, spatial sound and listeners | Audio engine | AudioSource/listener | Speakers/sequencer | PositionalAudio | MISSING | [src/scene.js][scene] and [tools/clip.mjs][clip] define no audio scene or soundtrack input. Add listeners, emitters, attenuation and synchronized clip audio. |
| E-T02 Buses, DSP, synthesis and music clock | MetaSounds/submix | Mixer/DSP | Sequencer/+ | Web Audio/+ | MISSING | [src/render.js][render] is graphics-only. Share Studio's DSP graph, clock and instruments rather than building a second isolated audio stack. |
| E-T03 Collision/footstep/water sound and room acoustics | Events/audio/+ | Events/audio/+ | Script/+ | + | MISSING | [src/history.js][history] records impacts but does not synthesize sound. Use contact/material events for sound, occlusion, room impulse responses and Studio editing. |
| E-T04 Scene scripting and headless API | C++/Blueprint | C#/APIs | Python | JS/TS | PARTIAL | [web/index.html][web], window.hb, and JSON scenes are programmable. Add stable public object/query/command APIs, runtime components and lifecycle hooks. |
| E-T05 Visual behavior scripting and reusable packages | Blueprints | Visual Scripting | Nodes/Python | + | MISSING | [src/scene.js][scene] interprets fixed types. Add a typed behavior graph, reusable functions and versioned extension contracts. |
| E-T06 AI scene authoring | + integrations | + integrations | + integrations | + integrations | HAVE | [tools/anything-writer.mjs][writer], writeSceneWith/validateScene/resolveScene, writes catalog-backed scenes and one correction pass. General scene understanding remains a separate quality target. |
| E-T07 Edit an existing scene by talking | + | + | + | + | MISSING | [tools/anything-writer.mjs][writer] starts from a prompt; [web/anything.html][anything] does not send the current scene as an edit transaction. Preserve IDs, seeds and unaffected work when applying requested patches. |
| E-T08 MCP render and history access | + adapters | + adapters | + adapters | + adapters | HAVE | [mcp/server.mjs][mcp] exposes render_scene, job_status, list_scenes, trace_object, events_between, why_flow and sand_history with input checks. Local tool access is not shared-world networking. |
| E-T09 Scene tree, selection, gizmos and property inspector | Editor | Editor | Editor | + editor/controls | MISSING | [web/index.html][web] and [web/anything.html][anything] are render pages. Add inspect/select/move/rotate/scale, object properties and direct material editing. |
| E-T10 Undo/redo, versions and reusable projects | Transactions/assets | Undo/assets | Undo/files | + application | MISSING | [src/scene.js][scene] builds a JSON scene; [src/history.js][history] is simulation history, not an authoring command log. Add persistent project edits and branch/restore. |
| E-T11 Phone/touch and keyboard accessibility | Platform UI | Platform UI | Desktop UI | Browser/+ | PARTIAL | [web/anything.html][anything] and [web/phone-test.html][phone] have phone flows. Add touch editing, keyboard equivalents, readable inspectors and accessibility for the general editor. |
| E-T12 Game/app UI, input and interaction | UMG/input | UI Toolkit/input | + runtime | DOM/+ | MISSING | [web/index.html][web] has page controls, not a general input/UI system. Add action maps, mouse/touch/gamepad, focus and accessible runtime widgets. |
| E-T13 Debugging, profiling and automated jobs | Insights/debuggers | Profiler/debuggers | Stats/debug tools | + tools | PARTIAL | [src/stats.js][stats], [tools/probe.mjs][probe], [tools/render.mjs][still], [web/phone-test.html][phone]. Add per-pass GPU timing, CPU/memory views, captures and regression jobs. |
| E-T14 Render queue and machine resource controls | Queue/farm tools | + jobs | CLI/+ farm | + host | PARTIAL | [mcp/server.mjs][mcp] and [tools/gpu-lock.mjs][lock] have local queuing, curfew and limits. Add cancel/resume, job persistence, priorities and worker capability matching. |
| E-T15 Gallery, remix and published project pages | + service | + service | + service | + service | PARTIAL | [tools/publish-to-site.mjs][publish] publishes engine files; [tools/anything-writer.mjs][writer] supplies reports. Add a render/project gallery with words, recipes, licenses and exact remix state. |

## Asset pipeline and performance

The baseline draws on Epic's [content import systems][ue-content], [world streaming][ue-world] and [rendering support][ue-render], Unity's [manual][unity], Blender's [manual][blender] and [Geometry Nodes][geo], and the [three.js loader/object APIs][three]. glTF support must be stated field by field; accepting the file extension does not mean supporting its whole scene.

| ID / capability | Unreal Engine 5 | Unity | Blender | three.js | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|
| E-I01 Static glTF/GLB and OBJ import | Import | Import/packages | Import | Loaders | HAVE | [src/gltf.js][gltf], loadGLTF/loadOBJ, reads triangle meshes, transforms, UVs and material subsets. |
| E-I02 Complete glTF scenes and extensions | Import dependent | Package dependent | Import/export | Loader/extensions | PARTIAL | [src/gltf.js][gltf] lacks animation/skins/morphs/sparse accessors, compression and many material extensions. Add validation, extension support reporting, samplers and correct normal transforms. |
| E-I03 FBX, USD, Alembic, CAD and volume exchange | Import frameworks | Import/packages | Import/export | Loaders/+ conversion | MISSING | [src/gltf.js][gltf] only implements glTF/OBJ. Add interchange adapters, animation/cache preservation and clear unsupported-field reports. |
| E-I04 Geometry/project export and round trip | Export/frameworks | Packages/+ | Broad export | Exporters | PARTIAL | [tools/render.mjs][still] exposes OBJ export through [web/index.html][web]. Add glTF/USD and editable project export with materials, animation and references intact. |
| E-I05 Asset browser, catalogs and metadata | Content Browser | Project/Asset tools | Asset Browser | LoadingManager/+ | PARTIAL | [tools/build-catalog.mjs][catalog], [tools/fetch-kenney.mjs][kenney], [ASSETS.md][assets]. Add thumbnails, search, tags, scale, dependency/version data and project-local copies. |
| E-I06 Automatic reimport and dependency tracking | Asset system | Asset Database | Libraries/+ | + application | MISSING | [src/gltf.js][gltf] fetches files; [src/scene.js][scene] rebuilds them. Add hashes, dependency graphs, incremental rebuild and missing-file relink. |
| E-I07 Textures, HDR and compressed assets | Broad formats | Broad formats | Broad formats | Loaders | PARTIAL | [src/hdr.js][hdr] reads Radiance HDR; [src/scene.js][scene] uses browser image decoding. Add EXR, KTX2/Basis, geometry compression, correct color/data flags and failure reports. |
| E-I08 Per-asset licensing and source records | Metadata/+ | Metadata/+ | Metadata/+ | + application | PARTIAL | [ASSETS.md][assets] and [LICENSE][license] record CC0 sources and engine license. Add machine-readable rights, author/source hashes and notices for every dependency/import. |
| E-F01 Spatial acceleration for ray tests | Engine acceleration | Engine acceleration | Cycles BVH | + BVH | HAVE | [src/bvh.js][bvh], binned SAH, and [src/tracer.wgsl][tracer], traverse. |
| E-F02 Incremental BVH, instances and shared geometry | Instances/acceleration | Instancing/batching | Instances | InstancedMesh | MISSING | [src/mesh.js][mesh], flattenMeshes, duplicates triangles; [src/scene.js][scene] rebuilds merged BVHs per fluid frame. Add BLAS/TLAS, refit, instance transforms and dynamic/static separation. |
| E-F03 Mesh LOD, HLOD and virtualized geometry | LOD/HLOD/Nanite | LODGroup | Decimate/+ runtime | LOD/+ | MISSING | [src/scene.js][scene] builds full meshes; [src/bvh.js][bvh] has no LOD manager. Add screen-error budgets, simplification, transitions and clustered streaming. |
| E-F04 Texture mips and footprint selection | Streaming/mips | Streaming/mips | Filtering/mips | Mips/filtering | PARTIAL | [src/render.js][render], mipChain; [src/tracer.wgsl][tracer], surfaceAt, estimates footprint. Add ray differentials/cones, per-texture sizing and correct filtering by map type. |
| E-F05 Virtual textures and memory residency | Virtual textures | Streaming/packages | Renderer dependent | + | MISSING | [src/scene.js][scene] resizes textures into one 2048 array; [src/render.js][render] uploads all layers. Add budgets, paging and eviction; do not load an entire world into phone memory. |
| E-F06 Culling and many-object submission | Culling/instancing | Culling/batching | Renderer culling | Culling/instancing | PARTIAL | [src/bvh.js][bvh] culls ray candidates, not world/asset residency. Add frustum, occlusion, instance and spatial-cell culling for the fast renderer. |
| E-F07 Jobs, workers and large-data processing | Task systems | Jobs/Burst/ECS | Native workers | Workers/+ | PARTIAL | [src/fluid-gpu.js][gpu] uses GPU passes; scene builds/BVH/surfacing use main-thread JS. Move heavy builds to workers/WASM, support cancellation and incremental results. |
| E-F08 Device quality tiers and recovery | Scalability/platforms | Quality/platforms | Device preferences | Capability checks/+ | PARTIAL | [src/render.js][render] requests GPU limits and logs device loss; [web/phone-test.html][phone] probes capacity. Add explicit fallbacks, resize/recreate, memory recovery and saved quality profiles. |
| E-F09 Upscaling, dynamic resolution and frame budgets | TSR/other systems | Pipeline/upscalers | Renderer dependent | + passes | MISSING | [src/render.js][render] fixes width/height at creation. Add dynamic budgets and interchangeable upscalers while preserving final-render accuracy. |
| E-F10 Reproducible performance comparisons | Profilers/benchmarks | Profilers/benchmarks | Statistics | + measurements | PARTIAL | [out/NOTES.md][notes] and [tools/blender_yardstick.py][yardstick] contain useful comparisons, including known camera mismatches. Add matched scene/camera/material/time/quality fixtures and record hardware/load. |

## Networking, VR/AR and platforms

Use the actual distinction in Epic's [networking overview][ue-network], Unity's [multiplayer][unity-network], [XR][unity-xr] and [platform][unity-platform] manuals, and the [three.js API][three]. Blender authors content and previews scenes; it is not a replacement for a shipped multiplayer/XR application runtime.

| ID / capability | Unreal Engine 5 | Unity | Blender | three.js | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|
| E-N01 Runtime replication and authoritative servers | Built-in framework | Netcode packages | + external runtime | + application | MISSING | [src/scene.js][scene] and [mcp/server.mjs][mcp] contain no shared runtime state. Add authority, replication, interest management and identity independent of public viewing. |
| E-N02 Prediction, rollback and networked physics | Network physics | Package dependent | + | + | MISSING | [src/fluid-gpu.js][gpu] has no snapshot reconciliation. Add ticked commands, snapshots, correction and supported determinism guarantees. |
| E-N03 Collaborative editing and conflict resolution | Multi-user tools | Version/collab tools | + | + | MISSING | [web/anything.html][anything] creates one user's scene. Add project operations, branches, merge/conflict handling, presence and comments. |
| E-N04 Persistent worlds and shared saves | Save/backend | Save/backend | Files/+ | + backend | MISSING | [src/scene.js][scene] and [src/history.js][history] have no shared world store. Add project snapshots plus durable edits and asset references. |
| E-X01 Stereo VR, tracking and controllers | XR/OpenXR | XR providers | + inspection | WebXR | MISSING | [src/render.js][render] has one perspective camera and no XR session. Add eye views, tracking, controllers, locomotion and frame-budget tests. |
| E-X02 AR camera, anchors, planes and occlusion | AR systems | AR Foundation | + external runtime | WebXR/+ | MISSING | [web/index.html][web] requests no camera/XR input. Add tracked camera input, placement, anchors, scene depth and evidence labels. |
| E-X03 Hands, haptics, spatial audio and XR UI | XR features | XR packages | + | WebXR/+ | MISSING | [src/scene.js][scene] has no XR/input/audio entities. Add capability-based adapters and accessible alternatives. |
| E-O01 Browser rendering without installation | + streaming/web route | Web builds | + exported viewer | Core target | HAVE | [src/render.js][render] and [web/index.html][web] run the same source through WebGPU. Supported browser/device combinations still need a maintained test list. |
| E-O02 Desktop unattended rendering | Commandlets | Batch mode | CLI | Node/browser/+ | HAVE | [tools/render.mjs][still] and [tools/clip.mjs][clip] drive headless Chromium. Existing runners contain local defaults that need portable configuration. |
| E-O03 iPhone/Android browser experience | + delivery | Web/mobile paths | + viewer | Browser target | PARTIAL | [web/phone-test.html][phone] and [web/anything.html][anything] contain phone flows; [out/NOTES.md][notes] records some real iPhone feedback. Verify actual GPU, thermal, memory and audio/XR support per device. |
| E-O04 Native Windows/macOS/Linux and mobile packages | Native targets | Native targets | Desktop authoring | + shell | MISSING | [tools/render.mjs][still] is browser automation, not a native application build. Add packaging and optional native backends behind the same project/runtime interfaces. |
| E-O05 Consoles and device SDK delivery | Platform SDKs | Platform SDKs | + runtime export | + native host | MISSING | [src/render.js][render] has only WebGPU. Add the backend/packaging interfaces; actual builds require the target platform's SDK and access terms. |
| E-O06 Offline/PWA, caches and self-hosting | Packaged apps | Packaged/web | Local app | + application | PARTIAL | [tools/serve.mjs][serve] serves locally; [tools/publish-to-site.mjs][publish] copies the web engine. Add installable offline cache, project/asset storage, migrations and exportable self-hosted services. |

## What is Heartbeat's own advantage, and what can go beyond parity

These are **our distinctive combination and direction**, not unsupported claims that nobody else can log events, use AI or write open software. Blender and three.js are already open source; other tools have scripting, caches, replay and collaboration. Heartbeat can make the connections first-class across its own products.

| Capability | State | Evidence and direction |
|---|---|---|
| Ask a drop where it came from and what happened | HAVE | [src/history.js][history], story/stateAt/eventsBetween; [web/necklace.html][necklace]; [mcp/server.mjs][mcp]. Keep the link between a picture and the events that produced it. |
| Explain flow changes and wet ground with recorded numbers | HAVE | [src/history.js][history], whyFlow/sandAt/sandPoint; [src/stats.js][stats]. Explanations describe the model and sampled record, not proof of what real water must do. |
| History for every system, with explicit coverage | PARTIAL | [src/history.js][history] samples selected free particles; [src/scene.js][scene] enables history on the GPU container path. Add solids, animation, audio and vision; declare sample rates, precision, unrecorded regions and dropped events. |
| Seen, rebuilt, patched and made labels that follow objects | PARTIAL | Outside-engine seed: [lab/bedroom-unified/history.js][vision]. It records these bases and separate actor/cause links. [tools/anything-writer.mjs][writer] reports asset/procedural/skipped sources, but engine scenes do not yet share the vision labels. |
| AI controls a real, inspectable scene | HAVE | [tools/anything-writer.mjs][writer] creates structured geometry/material instructions; [mcp/server.mjs][mcp] gives bounded tools. Extend the same command API to editing, Studio and vision. |
| Our engine code and sourced assets are openly reusable | HAVE | [LICENSE][license] is CC0; [ASSETS.md][assets] records asset sources. Preserve third-party notices and imported creators' rights; do not relabel every imported asset CC0. |
| The same material determines appearance, motion and sound | PARTIAL | [src/physics-library.js][physics] links wetting/flow and appearance. Add acoustic response, friction, breakage, fabric and thermal properties under one material ID. |
| A scene becomes cover art, a score and a music video | MISSING | [tools/clip.mjs][clip] exports silent picture; [studio/save.js][studio-save] makes a simple audio visualizer, not an engine scene. Join them through one project and clock. |
| Change one cause and inspect the consequences | PARTIAL | [src/history.js][history] lets us inspect a run, not restore arbitrary state. Add checkpoints, branches and explicit causal links; distinguish a new simulation from recovered observed evidence. |

## Proposed architecture for ONE general build

This is a proposal, not a claim that the modules below already exist. It is the same shared architecture proposed in [PARITY-STUDIO.md](PARITY-STUDIO.md). Build the whole scope as connected modules with common contracts; do not create a separate engine for each demonstration.

### 1. One project, shared libraries, several working surfaces

Use a versioned **hb-project/1** manifest for scenes, songs, shots and evidence. Store stable project/entity/asset IDs, dependency hashes, units, camera calibration, clocks, seeds, tool versions and rights alongside editable recipes. Keep large audio, texture, mesh, video and simulation data in hash-addressed files/chunks; a project can open locally without signing in. Remote storage and collaboration are adapters.

Proposed modules:

| Module | Responsibility | Reuse first |
|---|---|---|
| core/project + assets | Schemas, IDs, dependency graph, transactions, undo/redo, migrations, local save/recovery, file bundles | Scene JSON, Studio beat recipes, asset catalogs |
| core/time + history | Rational clocks, event records, tracks, coverage, checkpoints, causal queries and evidence | [src/history.js][history], [lab/bedroom-unified/history.js][vision] |
| libraries/materials | One material identity with visual, mechanical, liquid/porous, thermal and acoustic properties | [src/physics-library.js][physics], scene material packing, Studio impulse/synthesis primitives |
| libraries/geometry + physics | Geometry processing, collider cooking, rigid/cloth/soft/fluid/strand/gas solvers and two-way coupling | mesh, BVH, PBF, marching tetrahedra, assembler |
| libraries/audio | Real-time DSP, instruments, sample processing, mixing, pitch/time tools, analysis and export | Studio Beat Lab, recorder and save code |
| engine/runtime + renderers | Scene/component state, animation, interaction, world streaming, fast viewport, path tracing, XR and platform adapters | Existing WebGPU path tracer and browser/headless drivers |
| studio + director | Multitrack editing, comping, MIDI, arrangement, mixer, mastering, sound-for-picture and shot timelines | Existing Studio UI and engine camera paths |
| vision | Observations, tracking/reconstruction, calibration, uncertainties and explicit generated fills | Existing evidence labels and bedroom history experiment |
| automation + services | Same commands for UI/AI/MCP, background jobs, collaboration, asset/distribution adapters and public project pages | Existing MCP queue, writer validation and publishing tools |

Keep **data definitions separate from solvers**. A shared water preset can include density and surface tension in real units; the solver derives its own numerical coefficients and records its version. Current viscosity/cohesion knobs are not all measured physical constants. A fabric preset can feed shading, cloth constraints and friction sounds. An acoustic approximation or artistic override must carry its source and units rather than being presented as a measured property.

### 2. A single history format across engine, Studio and vision

Both existing history writers say **hb-history/1**, but they are not a complete common implementation. Engine uses fluid samples/flow/sand rows; the bedroom writer adds entities, basis, event IDs and cause links, and its JSONL export omits some metadata/entity detail available in its JSON export. Studio's S.history is temporary undo state, not this format. Unify deliberately as **hb-history/2**, with import adapters that keep old records and mark unknown/missing fields. Do not silently reinterpret older files.

The shared record needs:

| Field or record | Rule |
|---|---|
| meta / clocks | Schema version; project/run/branch IDs; source and tool versions; meters, axes and reference frames. Each stream has integer ticks and a rational rate. Audio keeps sample indices; video keeps rational frame rate; physics keeps step indices. A stored mapping connects these to project time and musical beats/tempo changes. |
| entity / asset | Stable entity ID; kind; label; material ID; asset hash; source/rights; parent/attachment relationships. IDs survive edits and imports. Reused particle slots need a generation ID, not just the slot number. |
| event | Unique event ID, sequence, time, type, subject, targets, actor/tool, parameters and result. Explicit cause event IDs are separate from actor/entity ancestry. An unexplained event stays unexplained. |
| provenance / basis | seen, rebuilt, patched or made, attachable per entity, event, track segment and image/audio region. Evidence references original hash, frame/sample range, pixel region and calibration. Keep confidence/error and method; generated content never becomes seen merely because it was rendered or replayed. |
| tracks / measurements | Typed position/velocity/pose/audio/MIDI/automation/observation streams with units, interpolation rules and uncertainty. Audio samples live in media chunks, not millions of individual JSON events. |
| coverage | Sampling interval, filters, quantization, known gaps, recorded event kinds, buffer capacity, overflow/dropped counts and whether a record is complete, sampled or derived. Engine event buffers currently stop retaining data past capacity; this must become visible. |
| snapshot / checkpoint | Complete state needed to resume the relevant subsystem, including RNG, solver state, plugin state, transport, tempo and referenced assets. An image or sampled trail alone cannot restart a simulation. |
| edits / branches / exports | Durable authoring operations and new branches. Corrections append records. Each export names exact project revision, source history ranges, render/mix settings and output hash. |

One proposed event, timed on the project's declared physics clock:

    {
      "k": "event",
      "format": "hb-history/2",
      "eventId": "run7:event184",
      "at": { "clock": "physics", "tick": 240 },
      "type": "contact.begin",
      "subject": "run7:water42:gen1",
      "targets": ["ground3"],
      "actor": "solver:fluid",
      "causes": ["run7:event122"],
      "basis": "made",
      "data": { "position_m": [0.1, 0.0, 0.2], "speed_m_s": 0.4 }
    }

Declare the physics clock's rate in meta; 240 is a step index, not an assumed sample rate. A contact can cause a sound event at an exactly mapped audio sample; Studio can edit that sound while keeping its origin. A camera observation can support a reconstructed track without claiming the invented path was filmed. The three systems use the same reader, validator and queries: object story, events in a window, causes, sources, changes and export lineage.

Do not promise bit-identical GPU simulation or audio on every device. Save authoritative outputs/checkpoints when exact recovery is required; record tolerances and implementation versions when replay is approximate.

### 3. Build order and what proves each part complete

The order is dependency order inside the one build, not permission to discard later features.

1. **Contracts and permanent projects.** Finish project/asset/time/history schemas, migrations and local media recovery. Import existing scenes, a recorded song and the bedroom history. Prove reopen after reload, exact asset references, retained labels and old-file compatibility.
2. **Shared material, geometry, physics and audio libraries.** Extract existing working code without losing behavior. Add units, versioned presets, common contacts/events and reusable DSP. Prove the same material changes water/wetting appearance and contact sound; keep CPU/GPU support differences explicit.
3. **General editing and automation.** Build the common scene tree, inspectors, timeline, selection, undo/redo, file browser and command API. Add Studio clip edits, take lanes and piano roll on this base. Prove a touch edit and an AI command create the same durable operation and restore correctly.
4. **General simulation and animation.** Complete rigid bodies, collider/joint systems, cloth, soft bodies, destruction, strands, vehicles, fluids, gas and cross-solver coupling; complete skeletons, rigs, morphs, clips and character control. Prove a moving, dressed character can interact with solid and wet surfaces, break an object and produce traceable sound.
5. **Rendering, world and interchange breadth.** Complete the fast viewport, advanced materials/volumes, denoising/AOVs, modeling/procedural graphs, tiled worlds, instancing/LOD/streaming and import/export adapters. Prove a multi-cell outdoor/interior scene stays within measured phone and desktop budgets and survives a round trip.
6. **Complete Studio and director workflows.** Finish recording/comping/pitch, effects/mixer/automation/mastering, MIDI/sampling, stems, sound-for-picture, cover art and video exports. Prove picture, original takes, edits, sounds, lyrics and project recipes stay connected and synchronized. Use the detailed Studio rows as the completion list.
7. **Collaboration, networking, XR and delivery.** Finish durable shared edits, runtime authority/prediction, remote workers, public remix pages, native/platform adapters, VR/AR and rights-aware publishing/distribution. Prove conflict/reconnect/recovery, actual headset/device flows and exports with complete source/rights records.
8. **Run the whole connected proof.** Reconstruct a filmed space with seen/made boundaries; bring in a rigged character, cloth, breakable prop and water; generate editable event-linked sound; record/comp/mix a song; make cover art and a music video; reopen, branch, remix and inspect any object's history. Check local and public delivery on real phone width and document what is still unverified. Any unfinished parity row remains an explicit task.

Keep a trace from each row ID to its implementation, supported backends, usable controls, history/rights behavior and a meaningful acceptance scene or session. A hidden function, a screenshot, an import that drops half the data or a single special-case demo does not complete a general workflow.

**Next thing:** write the project, clock and history schemas against the three existing formats, then use them to save and reopen one connected project.

[readme]: ../../../Projects/hb-render/README.md
[notes]: ../../../Projects/hb-render/out/NOTES.md
[scene]: ../../../Projects/hb-render/src/scene.js
[tracer]: ../../../Projects/hb-render/src/tracer.wgsl
[render]: ../../../Projects/hb-render/src/render.js
[post]: ../../../Projects/hb-render/src/post.wgsl
[gltf]: ../../../Projects/hb-render/src/gltf.js
[hdr]: ../../../Projects/hb-render/src/hdr.js
[mesh]: ../../../Projects/hb-render/src/mesh.js
[bvh]: ../../../Projects/hb-render/src/bvh.js
[fluid]: ../../../Projects/hb-render/src/fluid.js
[gpu]: ../../../Projects/hb-render/src/fluid-gpu.js
[solver]: ../../../Projects/hb-render/src/fluid-gpu.wgsl
[physics]: ../../../Projects/hb-render/src/physics-library.js
[mc]: ../../../Projects/hb-render/src/mc.js
[history]: ../../../Projects/hb-render/src/history.js
[stats]: ../../../Projects/hb-render/src/stats.js
[wetstats]: ../../../Projects/hb-render/src/wetstats.js
[camera]: ../../../Projects/hb-render/src/camera-path.js
[procedural]: ../../../Projects/hb-render/src/procedural.js
[assembler]: ../../../Projects/hb-render/src/assembler.js
[overlay]: ../../../Projects/hb-render/src/necklace-overlay.js
[web]: ../../../Projects/hb-render/web/index.html
[anything]: ../../../Projects/hb-render/web/anything.html
[phone]: ../../../Projects/hb-render/web/phone-test.html
[necklace]: ../../../Projects/hb-render/web/necklace.html
[mcp]: ../../../Projects/hb-render/mcp/server.mjs
[writer]: ../../../Projects/hb-render/tools/anything-writer.mjs
[still]: ../../../Projects/hb-render/tools/render.mjs
[clip]: ../../../Projects/hb-render/tools/clip.mjs
[probe]: ../../../Projects/hb-render/tools/probe.mjs
[lock]: ../../../Projects/hb-render/tools/gpu-lock.mjs
[publish]: ../../../Projects/hb-render/tools/publish-to-site.mjs
[catalog]: ../../../Projects/hb-render/tools/build-catalog.mjs
[kenney]: ../../../Projects/hb-render/tools/fetch-kenney.mjs
[serve]: ../../../Projects/hb-render/tools/serve.mjs
[yardstick]: ../../../Projects/hb-render/tools/blender_yardstick.py
[assets]: ../../../Projects/hb-render/ASSETS.md
[license]: ../../../Projects/hb-render/LICENSE
[chunks]: ../../../Projects/hb-render/WORLD-CHUNKS-IDEA.md
[studio-save]: ../../../Projects/heartbeat-observatory/studio/save.js
[vision]: ../../../Projects/heartbeat-observatory/lab/bedroom-unified/history.js
[ue-path]: https://dev.epicgames.com/documentation/en-us/unreal-engine/path-tracer-in-unreal-engine
[ue-render]: https://dev.epicgames.com/documentation/en-us/unreal-engine/supported-features-by-rendering-path-for-desktop-with-unreal-engine
[ue-physics]: https://dev.epicgames.com/documentation/unreal-engine/physics-in-unreal-engine
[ue-rig]: https://dev.epicgames.com/documentation/en-us/unreal-engine/animating-with-control-rig-in-unreal-engine
[ue-cinema]: https://dev.epicgames.com/documentation/en-us/unreal-engine/cinematics-and-movie-making-in-unreal-engine
[ue-world]: https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine
[ue-pcg]: https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-overview
[ue-audio]: https://dev.epicgames.com/documentation/en-us/unreal-engine/metasounds-in-unreal-engine
[ue-script]: https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprints-visual-scripting-in-unreal-engine
[ue-network]: https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine
[ue-content]: https://dev.epicgames.com/documentation/en-us/unreal-engine/working-with-content-in-unreal-engine
[unity]: https://docs.unity3d.com/6000.6/Documentation/Manual/UnityManual.html
[unity-hdrp]: https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.0/manual/HDRP-Features.html
[unity-physics]: https://docs.unity3d.com/6000.6/Documentation/Manual/PhysicsSection.html
[unity-animation]: https://docs.unity3d.com/6000.6/Documentation/Manual/AnimationSection.html
[unity-audio]: https://docs.unity3d.com/6000.6/Documentation/Manual/Audio.html
[unity-network]: https://docs.unity3d.com/6000.6/Documentation/Manual/multiplayer.html
[unity-xr]: https://docs.unity3d.com/6000.6/Documentation/Manual/XR.html
[unity-platform]: https://docs.unity3d.com/6000.6/Documentation/Manual/PlatformSpecific.html
[blender]: https://docs.blender.org/manual/en/5.1/index.html
[cycles]: https://docs.blender.org/manual/en/4.4/render/cycles/render_settings/sampling.html
[principled]: https://docs.blender.org/manual/en/5.4/render/shader_nodes/shader/principled.html
[geo]: https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/
[cloth]: https://docs.blender.org/manual/en/latest/physics/cloth/introduction.html
[soft]: https://docs.blender.org/manual/id/4.5/physics/soft_body/introduction.html
[three]: https://threejs.org/docs/
[three-material]: https://threejs.org/docs/pages/MeshPhysicalMaterial.html
[three-physics]: https://threejs.org/manual/pages/physics.html
