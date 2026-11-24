# Heartbeat Observatory — Studio parity map

Written by Codex, 26 October 2026. Source audit of **C:/Users/lilli/Projects/heartbeat-observatory/studio/**. Companion: [Engine parity map](PARITY-ENGINE.md).

**This is the scope for one complete, general studio build, not a ceiling.** Take the useful union of Logic Pro, FL Studio, Ableton Live, Pro Tools and BandLab, then connect it to our engine, vision and event history. Keep the direct phone experience while adding the depth behind it. Gaps are work items.

## How to read this map

- **HAVE:** working implementation found for the stated capability and limits. This is a source finding, not a claim of equal quality or a fresh listening test.
- **PARTIAL:** some useful pieces exist, but the general workflow is incomplete.
- **MISSING:** no implementation found in the inspected Studio code. Its evidence link points to the inspected boundary or closest existing piece.
- **+** in a competitor column means a plugin, separate service, package or external workflow; **—** means that product does not supply that general workflow itself. Editions, operating systems, subscriptions and hardware change availability. Do not copy a limitation into our feature scope.

Read [studio/index.html][studio], [studio/beatlab.js][beatlab], [studio/save.js][save], [studio/lyrics/lyrics.js][lyrics], [studio/lyrics/index.html][lyrics-page] and [studio/learn/index.html][learn]; inspected the beat/vendor inventory and searched for recording, editing, MIDI, pitch, automation, persistence and collaboration paths. The minified MP3 codec is a dependency, not a new Heartbeat instrument or effect. There are **149 parity rows: 19 HAVE, 52 PARTIAL and 78 MISSING**, plus the Heartbeat-specific direction table.

**Current shape:** one backing audio buffer plus up to six voice layers; one mono microphone capture at a time; punch-in, take review and undo; a rule-based synthesized Beat Lab with six styles; local beat recipes; mixed audio, beat parts and visualizer-video exports. Voice recordings stay in memory and are lost when the page reloads. A saved beat recipe does not contain the voice session.

**Verification boundary:** code and official documentation were inspected; no microphone, listening test, browser recording, export, live service, deployment or vendor application was run. Existing text claiming approximate loudness or exact playback is not a fresh measurement. The map separates findings from proposed behavior. Vendor references were checked online on 26 October 2026.

## Recording and transport

Baselines: [Logic recording/production][logic], [FL audio tools and edition differences][fl-editions], [Live recording][live-record], [Pro Tools recording][pt-record] and [BandLab Studio][band-start]. BandLab's documented [track/duration limits][band-limits] and [input channel choices][band-input] are product limits, not limits for Heartbeat.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-R01 Record a microphone locally | Audio tracks | Playlist/Edison | Audio tracks | Audio tracks | Voice/audio | HAVE | [studio/index.html][studio], getMic/prepareCapture. Web Audio mono capture, AudioWorklet plus ScriptProcessor fallback; original takes are separate from playback effects. |
| S-R02 General multitrack recording | Multitrack | Multitrack | Multitrack | Multitrack | Layered tracks | PARTIAL | [studio/index.html][studio], S.layers/addLayer, caps voice layers at six plus one beat. Build general audio/instrument/bus tracks; use measured device budgets rather than a six-track product ceiling. |
| S-R03 Simultaneous multi-input recording | Interfaces | Mixer inputs | Multiple inputs | Multiple inputs | Input choices/limits | MISSING | [studio/index.html][studio], getMic, has one stream and explicit mono capture. Add input/channel selection, multiple armed tracks and synchronized recording. |
| S-R04 Stereo and multichannel capture | Supported | Supported | Supported | Supported | Up to stereo/track | MISSING | [studio/index.html][studio], StudioCapture, copies input[0] only. Preserve channels and channel maps instead of reducing every input to mono. |
| S-R05 Device, sample-rate and buffer settings | Audio settings | Audio settings | Audio settings | Playback engine | Device dependent | PARTIAL | [studio/index.html][studio], ensureCtx/getMic, accepts browser defaults. Add device selection and honest capability/latency readouts, plus native interface adapters where needed. |
| S-R06 Input gain, meters and clip warnings | Channel controls | Mixer meters | Track meters | Track meters | Track controls | MISSING | [studio/index.html][studio] has waveform playback and layer volume, no live input meter/clip counter. Add input trim, peak/RMS meters, headroom and overload display. |
| S-R07 Input monitoring, cue mixes and talkback | Routing | Routing | Monitoring/routing | Cue mixes | Monitoring | MISSING | [studio/index.html][studio] sends the capture path to a zero-gain sink. Add dry/wet monitor controls, cue sends and latency-safe monitoring choices. |
| S-R08 Record in an empty project | Supported | Supported | Supported | Supported | Supported | MISSING | [studio/index.html][studio], record/controls, requires hasAudio. Allow a blank session to arm and record, with optional click/count-in. |
| S-R09 Overdub and select target track | Supported | Supported | Supported | Supported | Supported | HAVE | [studio/index.html][studio], S.target/record/start; new audio records against the backing beat and other layers. |
| S-R10 Punch-in and punch-out ranges | Punch modes | Recording options | Punch controls | QuickPunch/ranges | Region workflows | PARTIAL | [studio/index.html][studio], rvKeep/outside, replaces the covered part of the chosen layer. Add stored punch boundaries, auto stop and non-destructive take lanes. |
| S-R11 Count-in and recording metronome | Supported | Supported | Supported | Supported | Supported | PARTIAL | [studio/index.html][studio] offers a two-second pre-roll; the headphone sync clicks are a separate calibration tool. Add musical count-in, meter, accent and recording click routing. |
| S-R12 Loop recording and multiple passes | Take folders | Loop takes | Take lanes | Playlists | Region/overdub | MISSING | [studio/index.html][studio] captures one pending take. Add cycle recording with automatic pass lanes and retained originals. |
| S-R13 Latency compensation and calibration | Driver/PDC | Driver/PDC | Driver/PDC | Driver/PDC | Device dependent | PARTIAL | [studio/index.html][studio], captureChunk/record/finishRecording, uses audio-clock timestamps, latency estimates and manual nudge. Add measured round-trip calibration and separate recording/effect delay compensation. |
| S-R14 Stop, seek, rewind and overview | Transport | Transport | Transport | Transport | Transport | HAVE | [studio/index.html][studio], start/stop/seek/draw; whole-song strip, 30-second detail view and 10/15-second rewind buttons. |
| S-R15 Loop selection, scrub and detailed zoom | Supported | Supported | Supported | Supported | Region/transport | PARTIAL | [studio/index.html][studio], view/posFromEvent, offers seeking but fixed close-up length. Add loop ranges, zoom, snap modes, scrub and precise numeric positions. |
| S-R16 Recovery from page/device interruption | Recovery | Recovery | Recovery | Recovery | Cloud revisions | PARTIAL | [studio/index.html][studio] stops on hidden page, mic end or suspended audio. Add chunked durable capture, crash recovery, device reconnect and missing-media handling. |
| S-R17 Retrospective recording and external sync | Capture/sync | Recording buffer/sync | Capture MIDI/Link | Sync workflows | + | MISSING | [studio/index.html][studio] only stores actively captured chunks. Add opt-in capture buffers, MIDI clock/MTC/Link adapters and reliable transport synchronization. |

## Vocal editing, comping, timing and pitch

References: Logic's [comping][logic-comp] and [Flex Time/Pitch][logic-flex], FL's [Newtone/Newtime/Edison availability][fl-editions], [Live comping][live-comp], [Pro Tools editing][pt-edit] and [BandLab AutoPitch][band-pitch]. Punching over a passage is useful, but it is not a take-lane comp editor. Noise filtering and compression do not correct pitch.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-V01 See waveforms on tracks | Supported | Supported | Supported | Supported | Supported | HAVE | [studio/index.html][studio], draw/peaks, draws backing, kept takes, pending takes and capture regions. |
| S-V02 Split, cut, copy, paste and move clips | Region tools | Playlist/Edison | Clip tools | Smart Tool | Region tools | MISSING | [studio/index.html][studio] timeline pointers seek; they do not select or move clips. Add sample-accurate clip edits, snapping and multi-selection. |
| S-V03 Trim either edge and slip source audio | Region tools | Clip tools | Clip tools | Trim/slip | Region tools | PARTIAL | [studio/index.html][studio], trim/slice, only keeps a percentage from the beginning of a pending take. Add reversible edges, source offsets and slip edits on kept clips. |
| S-V04 Fades and automatic crossfades | Supported | Supported | Supported | Supported | Fade tools | MISSING | [studio/index.html][studio], rvKeep/slice, joins buffer pieces without editable fades. Add equal-power/linear curves and click-free punch boundaries. |
| S-V05 Clip gain, envelopes and normalization | Region gain | Clip gain | Clip envelopes | Clip gain | Region controls | MISSING | [studio/index.html][studio] has layer gain only; wav has export peak reduction. Add per-clip gain/envelopes, analysis and reversible processing. |
| S-V06 Keep, audition, redo and discard a take | Take tools | Recording/edit tools | Take tools | Take tools | Recording/edit tools | HAVE | [studio/index.html][studio], finishRecording/rvListen/rvKeep/rvRedo/rvDelete. Pending-take review is implemented. |
| S-V07 Comp best phrases from multiple takes | Quick Swipe | Clip-based/+ | Take lanes | Playlists | Manual regions | MISSING | [studio/index.html][studio] keeps one replacement result and an undo snapshot. Add retained take lanes, swipe/range selection, alternate comps and crossfades. |
| S-V08 Global undo/redo and version branches | Supported | Supported | Supported | Supported | Revisions | PARTIAL | [studio/index.html][studio], S.history/undoBtn, restores clip arrays for selected edits only. Add redo, effects/mixer/arrangement history and durable branches. |
| S-V09 Pitch detection and note display | Flex Pitch | Newtone | + editor | + ARA/Melodyne | AutoPitch/+ | MISSING | [studio/index.html][studio], layerOut, has high-pass/compressor/pan only. Add pitch analysis with voiced/unvoiced confidence and editable notes. |
| S-V10 Real-time pitch correction and scale lock | Pitch tools | Pitcher/+ | Auto Shift | + plugin | AutoPitch | MISSING | [studio/index.html][studio] contains no pitch processor. Add key/scale, retune speed, blend and low-latency monitoring. |
| S-V11 Note, drift, vibrato and formant editing | Flex Pitch | Newtone | + editor | + ARA/editor | Effect controls/+ | MISSING | [studio/index.html][studio] and [studio/beatlab.js][beatlab] have no recorded-vocal pitch map. Add independent note/drift/vibrato/formant controls that preserve source audio. |
| S-V12 Time stretching, transient warp and quantize | Flex Time | Newtime/stretch | Warp | Elastic Audio | Stretch tools | MISSING | [studio/index.html][studio], loadBeat, explicitly warns tempo changes will not stretch takes. Add transient/warp markers, stretch algorithms and tempo maps. |
| S-V13 Align doubles, harmonies and dialogue | Flex/+ | + tools | Warp/+ | ARA/+ | + | MISSING | [studio/index.html][studio] offers recording nudge only. Add alignment between existing clips, phase-safe multitrack groups and editable anchors. |
| S-V14 Breath, de-ess, noise and spectral repair | Effects/+ | Edison/+ | Effects/+ | ARA/AudioSuite/+ | Voice Cleaner | MISSING | [studio/index.html][studio], cleanVoice, is an 80 Hz high-pass and compressor. Add dedicated noise, click, plosive, sibilance and spectral tools with before/after comparison. |
| S-V15 Harmonies, doubling and voice transformation | Instruments/effects | Effects/+ | Devices/+ | + plugins | AutoPitch/voice tools | MISSING | [studio/index.html][studio] can record real layers but cannot synthesize harmonies or transform a take. Add editable generated harmony/voice layers with clear made labels. |
| S-V16 Lyrics linked to words, notes and audio | Editors/+ | + | + | + | Lyrics/tools | PARTIAL | [studio/lyrics/lyrics.js][lyrics] saves text and estimates syllables; it has no song/clip timing link. Add word timestamps, pronunciation, syllable placement and lyric-to-performance navigation. |
| S-V17 Reverse, stretch, render and restore clip processing | Region tools | Edison | Clip/sample tools | AudioSuite | Region tools | MISSING | [studio/index.html][studio], slice/render, has no selected-clip process rack. Add reversible transforms and rendered variants with their source lineage. |

## Effects and sound design

The effect baseline comes from [Logic plugins][logic-plugins], [FL's mixer][fl-mixer] and [feature catalog][fl-features], [Live's devices/manual][live], [Pro Tools mixing][pt-mix] and [BandLab's effect/tool offerings][band-membership]. Separate an effect present inside our beat generator from an effect the user can insert on any recorded track.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-F01 Basic recorded-voice cleanup | Channel tools | Mixer effects | Track devices | Plugins | FX presets | HAVE | [studio/index.html][studio], layerOut/cleanVoice, applies an 80 Hz high-pass and 3:1 compressor on playback and offline mix. |
| S-F02 Per-track insert chains and effect presets | Channel strips | Mixer/Patcher | Device racks | Inserts/presets | FX chains | MISSING | [studio/index.html][studio] has one global cleanVoice toggle. Add arbitrary ordered track/clip/bus chains, presets, bypass and wet/dry. |
| S-F03 Parametric EQ, filters and spectrum view | EQ/plugins | EQ/plugins | EQ Eight/etc. | EQ/plugins | Visual EQ/FX | PARTIAL | [studio/index.html][studio] has fixed high-pass; [studio/beatlab.js][beatlab], graph, has fixed beat EQ. Add editable bands, curves and analyzer. |
| S-F04 Compressor, gate, expander and de-esser | Plugins | Plugins | Devices/+ | Plugins | FX | PARTIAL | [studio/index.html][studio] has one fixed compressor; [studio/beatlab.js][beatlab], master, has glue compression. Add the other processors and full controls. |
| S-F05 Algorithmic and convolution reverb | Plugins | Plugins | Devices | Plugins | FX | PARTIAL | [studio/beatlab.js][beatlab], graph, synthesizes a convolution impulse for beat buses. Expose reverb on vocals/any bus, with size, decay, predelay, filtering and imported impulses. |
| S-F06 Echo and tempo delay | Plugins | Plugins | Devices | Plugins | FX | PARTIAL | [studio/beatlab.js][beatlab], graph, has fixed dotted-eighth melody delay. Add selectable timing, feedback/filtering and per-track/send use. |
| S-F07 Saturation, distortion and amp/cabinet | Plugins | Plugins | Devices | Plugins | FX | PARTIAL | [studio/beatlab.js][beatlab], graph/master, has drum/bass waveshaping and soft saturation. Add general processors, models, oversampling and gain compensation. |
| S-F08 Chorus, flanger, phaser, tremolo and modulation | Plugins | Plugins | Devices | Plugins | FX | MISSING | [studio/index.html][studio], layerOut, and [studio/beatlab.js][beatlab], graph, have no general modulation rack. Add controllable modulation processors. |
| S-F09 Multiband, dynamic EQ and transient shaping | Plugins | Plugins | Devices/+ | Plugins/+ | Membership FX | MISSING | [studio/beatlab.js][beatlab], master, is broadband. Add band splits, dynamics, transient controls and crossover/phase handling. |
| S-F10 Sidechain, ducking, parallel and mid/side effects | Routing/plugins | Mixer/Patcher | Sidechains/racks | Routing/plugins | Tool dependent/+ | MISSING | [studio/index.html][studio] and [studio/beatlab.js][beatlab], graph, have no external detector or general routing graph. Add sidechain inputs, parallel chains and channel matrices. |
| S-F11 Granular, resonator, vocoder and creative spectral tools | Plugins | Plugins | Devices | + plugins | Effects/+ | MISSING | [studio/beatlab.js][beatlab], kitFor, synthesizes instruments but has no such audio processors. Add general creative sound transformations and modulation. |
| S-F12 Modulators, macros and audio/MIDI control mapping | Smart controls | Controllers/Patcher | Racks/Max | Automation/+ | Controls/+ | MISSING | [studio/beatlab.js][beatlab] has hand-coded envelopes only. Add LFO/envelope/follower nodes, macros and MIDI-learn. |
| S-F13 Third-party instrument/effect hosting | AU | VST/AU/CLAP | VST/AU | AAX/ARA | Curated built-ins | MISSING | [studio/index.html][studio] and [studio/beatlab.js][beatlab] create Web Audio nodes directly. Add a versioned web/WASM plugin interface and optional native plugin bridge; a normal tab does not load native AU/VST/AAX binaries directly. |
| S-F14 Plugin delay compensation and offline parity | Supported | Supported | Supported | Supported | Managed graph | PARTIAL | [studio/index.html][studio] reuses layerOut for live/offline voice effects, but has no latency-reporting graph. Match live/offline processors and compensate all paths. |
| S-F15 Effect tails, automation and freeze/commit | Supported | Supported | Supported | Supported | Freeze/FX | PARTIAL | [studio/beatlab.js][beatlab], render, overlaps fixed tails; recorder render adds 0.5 seconds. Add effect-reported tails, automation and freeze/commit with reversible source state. |

## Mixing and metering

Mix targets follow [FL mixer routing][fl-mixer], [Live routing][live-routing] and [mixing][live-mix], [Pro Tools mixing][pt-mix], [Logic workflows][logic] and [BandLab Studio][band-start]. Existing faders are a start, not a complete console.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-M01 Track level, pan and mute | Supported | Supported | Supported | Supported | Supported | HAVE | [studio/index.html][studio], drawLayers/updateMix/layerOut, implements all three for voice layers and level for the beat. |
| S-M02 Solo, polarity and gain staging | Console | Mixer | Mixer | Console | Track controls/+ | MISSING | [studio/index.html][studio], drawLayers, has mute/clear but no solo/polarity/input trim. Add them with clear pre/post gain points. |
| S-M03 Name, color, reorder and group tracks | Supported | Supported | Supported | Supported | Track organization | PARTIAL | [studio/index.html][studio] assigns fixed layer names; [studio/beatlab.js][beatlab] can rename saved beats. Add full track organization and folders. |
| S-M04 Buses, submixes, sends and returns | Aux/stack | Mixer routing | Groups/returns | Aux/buses | Tool dependent/+ | PARTIAL | [studio/beatlab.js][beatlab], graph, internally routes four beat buses to reverb/master. Expose a general graph across beats, voice, instruments and scene audio. |
| S-M05 Per-track peak, RMS and gain-reduction meters | Meters | Meters | Meters | Meters | Meters | MISSING | [studio/index.html][studio] draws waveforms, not mixer meters. Add pre/post meters, overload holds and compressor reduction. |
| S-M06 Spectrum, phase, correlation and mono check | Tools | Wave Candy/+ | Spectrum/Utility | Plugins/meters | Tool dependent/+ | MISSING | [studio/save.js][save] uses an analyzer only for video animation. Add mix analyzers, reference routing and mono/downmix checks. |
| S-M07 Volume, pan, effect and send automation | Automation | Automation clips | Automation | Automation modes | Automation | MISSING | [studio/index.html][studio], updateMix, changes current values only. Add stored curves, read/touch/latch/write, trim and editable breakpoints. |
| S-M08 Groups, linked edits and VCA-style control | Groups/VCAs | Groups/routing | Groups/macros | Groups/VCAs | + | MISSING | [studio/index.html][studio], S.layers, has independent faders only. Add linked controls and grouping without duplicating audio. |
| S-M09 Flexible channel layouts and surround | Surround/Atmos | Routing/+ | Routing/+ | Surround/Atmos | Stereo | MISSING | [studio/index.html][studio], render/wav, fixes stereo output. Add channel-layout-aware processing, buses, downmixes and optional immersive delivery. |
| S-M10 Reference tracks and loudness-matched A/B | Plugins/routing | Routing/+ | Routing/+ | Routing/+ | Mastering/reference | MISSING | [studio/index.html][studio] has no independent reference path. Add level-matched comparison that bypasses the master chain appropriately. |
| S-M11 Mixer snapshots and alternate mixes | Alternatives | Project versions | Sets/automation | Playlists/snapshots | Revisions | MISSING | [studio/index.html][studio], S.history, stores clip edits only. Add recalled mix scenes, alternate versions and revision comparisons. |
| S-M12 Hardware inserts and control surfaces | Supported | MIDI/routing | External effects | Hardware/EUCON | Device dependent/+ | MISSING | [studio/index.html][studio], ensureCtx, only connects the default destination. Add interface routing, external round-trip compensation and surface adapters. |
| S-M13 Freeze, bounce and CPU/memory budgeting | Freeze/bounce | Consolidate | Freeze/flatten | Freeze/commit | Freeze | PARTIAL | [studio/beatlab.js][beatlab] caches one rendered beat and renders short chunks. Add per-track freeze, disk-backed audio, scheduling budgets and safe recovery from resource pressure. |

## Mastering and final quality

Baselines include [Logic Mastering Assistant][logic-master], [FL Cloud mastering][fl-cloud], [Live's processing devices][live], [Pro Tools mixing/meters][pt-mix] and [BandLab mastering tools][band-membership]. A self-described approximate LUFS target is not a loudness meter.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-Q01 Master bus for every complete song | Master/output | Master | Main track | Master faders | Mix/master | PARTIAL | [studio/beatlab.js][beatlab], master, processes generated beats; [studio/index.html][studio], render, mixes vocals without that mastering chain. Add one editable final-song master graph. |
| S-Q02 Compression, saturation and peak limiting | Plugins | Plugins | Devices | Plugins | Mastering | PARTIAL | [studio/beatlab.js][beatlab], master, has all three, fixed for generated beats. Make them general, bypassable and parameterized. |
| S-Q03 Measured integrated/short-term loudness and LRA | Metering | + meter/service | + meter | Meter/plugin | Service analysis | MISSING | [studio/beatlab.js][beatlab] uses gated RMS without full BS.1770 weighting; no user meter exists. Add validated LUFS/LRA analysis and units. |
| S-Q04 True-peak measurement and codec checks | Metering/+ | + meter/service | Limiter/+ | Meter/plugin | Service | PARTIAL | [studio/beatlab.js][beatlab], master, estimates between-sample peaks; [studio/save.js][save], encodeMp3, adds peak headroom. Add oversampled true-peak analysis and checks on the encoded output. |
| S-Q05 Target loudness, ceiling and platform versions | Master tools | Plugins/Cloud | Chain/+ | Chain/+ | Mastering presets | MISSING | [studio/beatlab.js][beatlab], master, has fixed goals; [studio/save.js][save] has no target profile. Add selectable delivery goals without silently replacing an artist's mix. |
| S-Q06 Automated/reference mastering with editable result | Assistant | FL Cloud | + | + plugins | Mastering/reference | MISSING | [studio/beatlab.js][beatlab] is a fixed rules chain, not mix analysis that produces editable mastering decisions. Add analysis, explanations, level-matched bypass and revision history. |
| S-Q07 Dither, bit depth and sample-rate conversion | Bounce options | Export options | Export options | Bounce options | Download options | PARTIAL | [studio/index.html][studio], wav/render, writes 16-bit stereo at 44.1 kHz with no dither. Add high-quality resampling, selectable integer/float formats and dither only where appropriate. |
| S-Q08 Album/EP sequencing, gaps and consistency | + workflow | + workflow | Arrangement/+ | Album workflow/+ | + | MISSING | [studio/save.js][save] saves one buffer. Add track order, gaps, shared references, matched levels and album delivery packages. |
| S-Q09 Technical QC and delivery report | Tools/+ | Tools/+ | Tools/+ | Tools/+ | Service/+ | MISSING | [studio/save.js][save] has progress/error UI but no audio QC report. Add duration, silence, clipping, DC, phase, loudness, true peak, channel and metadata checks. |

## MIDI, instruments and composition

Baselines: [Logic instruments/plugins][logic-plugins], [FL Piano roll][fl-piano], [Live instruments/MIDI tools][live], [MPE][live-mpe] and [tuning systems][live-tuning], [Pro Tools comparison][pt-editions], and [BandLab audio/MIDI tracks][band-start]. Our internal MIDI note numbers are useful composition data, not a MIDI device or file implementation.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-I01 Synthesized drums, bass, keys, pads and leads | Instruments | Instruments | Instruments | Instruments/+ | Virtual instruments | HAVE | [studio/beatlab.js][beatlab], kitFor, synthesizes kicks/snares/claps/hats/perc, 808/round/log bass, FM keys/bells, pluck, pad and dark lead. |
| S-I02 Playable instruments and live note recording | MIDI instruments | Channels | MIDI tracks | Instrument tracks | Instrument tracks | MISSING | [studio/beatlab.js][beatlab] schedules generated notes offline. Add real-time note on/off, sustain, monitoring and recorded performances. |
| S-I03 Piano roll and arbitrary note editing | Piano Roll | Piano roll | MIDI editor | MIDI editor | MIDI editor | MISSING | [studio/beatlab.js][beatlab], drawParts, prints note names but exposes no note editor. Add move/resize/draw, audition, selection and numeric edits. |
| S-I04 MIDI device I/O and mapping | MIDI settings | MIDI settings | MIDI ports | MIDI setup | MIDI devices | MISSING | [studio/index.html][studio] and [studio/beatlab.js][beatlab] never request MIDI access. Add web/native device adapters, keyboard/touch playing and mapping. |
| S-I05 MIDI file import/export | Supported | Supported | Supported | Supported | Import/export options | MISSING | [studio/save.js][save] exports audio/video only. Add SMF import/export with tempo, meter, programs, controllers and note timing. |
| S-I06 Velocity, expression, sustain, CC and pitch bend | MIDI editors | Piano roll/events | Envelopes/MPE | MIDI editors | MIDI controls | MISSING | [studio/beatlab.js][beatlab], schedBar, sets velocity/glides by code. Add editable event lanes and expressive performance recording. |
| S-I07 MPE and alternate tuning | Instruments | Instrument dependent | MPE/tunings | Plugin dependent | Tool dependent/+ | MISSING | [studio/beatlab.js][beatlab], hz, assumes 12-tone equal temperament and no per-note expression. Add tuning tables and per-note controls. |
| S-I08 Step sequencer and drum editing | Step Sequencer | Channel Rack | Drum Rack/clips | MIDI tools/+ | Drum Machine | PARTIAL | [studio/beatlab.js][beatlab], drawParts, has three 16-step rows. Add multiple patterns, per-step velocity/probability, lengths, ratchets, microtiming and per-hit sounds. |
| S-I09 Scales, chords and progression generation | Chord/session tools | Chord tools | MIDI tools | MIDI/+ | SongStarter/+ | PARTIAL | [studio/beatlab.js][beatlab], compose, has major/minor scales, chord pools, inversions and motifs. Add arbitrary chords, modes, key changes, voicings and editable harmonic tracks. |
| S-I10 Rule-based variations and human feel | Session tools | Generators | MIDI generators | MIDI/+ | SongStarter/+ | HAVE | [studio/beatlab.js][beatlab], roll/compose/schedBar, uses seeded style rules, swing, velocity/timing variation and separate seeds. Keep the result inspectable and editable. |
| S-I11 Arpeggiators, MIDI effects and generative devices | MIDI FX | Plugins/scripts | MIDI effects/Max | + plugins | + | MISSING | [studio/beatlab.js][beatlab] has fixed composition routines, no reusable MIDI processor graph. Add chainable transforms and generators. |
| S-I12 General synth editing and modulation | Synths | Synths/Patcher | Synths/racks | Plugins | Presets/+ | PARTIAL | [studio/beatlab.js][beatlab], kitFor, defines oscillators, filters and envelopes in code. Expose patch editing, modulation, presets and reusable instrument definitions. |
| S-I13 Sample-based instruments and large libraries | Sampler/libraries | Samplers/FLEX | Sampler/Simpler | Plugins/libraries | Sampler/instruments | MISSING | [studio/beatlab.js][beatlab] makes sounds mathematically; no sample zones/layers are read. Add multisamples, velocity layers, articulations and streaming. |
| S-I14 Drum pads, keyboard and hardware performance | Controllers | Controllers | Push/controllers | Controllers | Touch/MIDI | MISSING | [studio/beatlab.js][beatlab] has sequence buttons, not playable performance pads. Add touch/keyboard pads, expressive controllers and recorded pad events. |
| S-I15 Notation, chord charts and lyric sheets | Score editor | + score tools | + export/tools | Score editor | + | PARTIAL | [studio/lyrics/lyrics.js][lyrics] exports plain lyrics; [studio/beatlab.js][beatlab] displays chord names/Roman numerals. Add lead sheets, notation and synchronized lyric/chord exports. |
| S-I16 Style libraries and reusable instrument presets | Libraries | Libraries | Packs/library | Presets/plugins | Sounds/presets | PARTIAL | [studio/beatlab.js][beatlab], STYLES, contains six styles; [studio/index.html][studio], BEATS, lists prebuilt beats. Add searchable, versioned patterns/presets and broader musical structures. |

## Sampling, audio library and one-shots

Reference points are [Logic Sampler][logic-sampler], [FL audio editing][fl-features], [Live's sample instruments][live] and [BandLab's Studio/sound library][band-start]. Loading a whole audio file for playback is not a full sampler.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-S01 Import beats and recorded audio | Supported | Supported | Supported | Supported | Supported | HAVE | [studio/index.html][studio], beatFile/voiceFile, uses browser decoding. Actual formats depend on the browser; selected file extensions are not proof every codec decodes. |
| S-S02 Place one-shots anywhere on the timeline | Regions/sampler | Clips/channels | Clips/Drum Rack | Clips/sampler | Regions/sampler | PARTIAL | [studio/index.html][studio], voiceFile, imports a file at the playhead into a voice layer. Add a sound browser, preview, drag/tap placement, repeat and proper sound tracks. |
| S-S03 Sample trim, loop points and envelopes | Sampler | Samplers | Sampler/Simpler | + sampler | Sampler | MISSING | [studio/index.html][studio], slice, is take trimming; [studio/beatlab.js][beatlab] has no user-sample instrument. Add sampler zones, loops and envelopes. |
| S-S04 Slice by transients, chop and map to pads | Quick Sampler | Slicex/Edison | Slice/Drum Rack | Edit/+ sampler | Sampler/tools | MISSING | [studio/index.html][studio] has no transient/slice map. Add manual/automatic chopping with source boundaries and pad/MIDI mapping. |
| S-S05 Detect tempo/key and match loops | Smart Tempo | Analysis/tools | Warp/tools | Elastic workflows/+ | Splitter/tools | MISSING | [studio/index.html][studio] sets uploaded beat BPM to null. Add analysis with confidence, manual correction and non-destructive tempo/key matching. |
| S-S06 Resample, bounce in place and reuse output | Bounce | Consolidate | Resampling | Commit/bounce | Merge/freeze | PARTIAL | [studio/index.html][studio], render, produces the full mix or combined vocals. Add selected clip/track/bus capture and immediate library reuse. |
| S-S07 Search, tag, preview and manage media | Browser | Browser/Cloud | Browser | Workspace | Sounds | PARTIAL | [studio/index.html][studio] lists fixed beats; [studio/beatlab.js][beatlab], My beats, lists recipes. Add a media browser with previews, metadata, hash deduplication and missing-file relink. |
| S-S08 Royalty/license/source records for samples | Metadata/+ | Library terms/+ | Pack terms/+ | Metadata/+ | Sound terms/+ | PARTIAL | [studio/learn/index.html][learn] explains clearance; no media-level rights record exists in [studio/index.html][studio]. Store exact source, license, owner and allowed-use fields per asset. |

## Arrangement and songwriting

The baseline includes [Logic production workflows][logic], [FL Playlist][fl-playlist], [Live's Session/Arrangement tools][live], [Pro Tools editing][pt-edit] and [BandLab projects][band-start]. Keep beat generation and recorded-song arrangement on the same editable timeline.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-A01 A complete generated song structure | Arrangement/session tools | Playlist/generators | Arrangement/tools | Timeline/+ | Timeline/SongStarter | PARTIAL | [studio/beatlab.js][beatlab], plan/SECTIONS, generates Intro/Verse/Hook/Verse/Hook/Outro. Add arbitrary section order, lengths and transitions. |
| S-A02 Mark verse/chorus and move/repeat sections | Arrangement markers | Playlist sections | Locators/arrangement | Markers/sections | Region workflows | MISSING | [studio/index.html][studio] has no sections; Beat Lab's fixed plan is not editable song arrangement. Add section operations across audio, MIDI, lyrics and automation. |
| S-A03 Copy, loop, duplicate and rearrange clips | Region tools | Playlist | Clips | Clip tools | Region tools | MISSING | [studio/index.html][studio] can import/punch takes, not repeat/move them. Add non-destructive instances and independent-copy choices. |
| S-A04 Tempo/meter/key maps and musical grid | Global tracks | Tempo/signature | Tempo/signature | Tempo/conductor | Tempo/key | PARTIAL | [studio/beatlab.js][beatlab] has one BPM/key, fixed four-beat bars and swing. Add map changes, odd meters and exact bar/beat/sample conversions. |
| S-A05 Session clips, scenes and live launching | Live Loops | Performance mode | Session View | + | + | MISSING | [studio/beatlab.js][beatlab] plays a rendered buffer. Add quantized clip launching, scene capture and follow actions. |
| S-A06 Markers, cue points and rehearsal loops | Supported | Supported | Locators | Memory locations | Loop/region tools | MISSING | [studio/index.html][studio] has numeric time and seeking only. Add named markers, cue lists and saved rehearsal ranges. |
| S-A07 Song alternatives and arrangement versions | Alternatives | Project versions | Sets/take lanes | Playlists/session versions | Revisions | PARTIAL | [studio/beatlab.js][beatlab] saves beat variants; [studio/index.html][studio] does not save song variants. Add branches covering all takes, tracks, mix and arrangement. |
| S-A08 Lyric writing, rhyme help and syllable map | + | + | + | + | Lyrics/+ | HAVE | [studio/lyrics/lyrics.js][lyrics] has local autosave, approximate English syllables, a small rhyme list and text export. Add languages/dictionaries without calling these estimates exact. |
| S-A09 Chord, melody, bass and drum editing together | Editors | Editors | Editors | Editors | Editors | PARTIAL | [studio/beatlab.js][beatlab] rerolls parts and directly edits drums, but not arbitrary notes or chord progression. Add linked harmonic and note editors. |
| S-A10 Video reference, timecode and sound-for-picture | Movie/sync | Video/+ | Video | Video/timecode | + video tools | MISSING | [studio/save.js][save] generates a visualizer; it does not load reference picture. Add video tracks, rational timecode, markers and edit/mix to picture. |
| S-A11 Project templates and portable session bundles | Templates/projects | Templates/projects | Templates/sets | Templates/sessions | Templates/revisions | PARTIAL | [studio/beatlab.js][beatlab] saves recipes only. Add whole-session templates, collected media and portable, versioned project files. |
| S-A12 Tempo-safe edits across recorded takes and beat | Flex/global edits | Playlist/stretch | Warp/global edits | Groups/Elastic | Stretch/regions | MISSING | [studio/index.html][studio], loadBeat, keeps old take positions when tempo changes. Apply section/tempo edits coherently to all linked media with explicit stretch choices. |

## Collaboration, saved projects and publishing

References include [Pro Tools cloud workflows][pt-cloud], [BandLab collaboration][band-collab], [revision/source protection][band-revisions] and [current access rules][band-access]. Shared editing is different from transmitting a low-latency musical performance; each needs its own timing design.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-C01 Save/reopen the whole song with original takes | Projects | Projects | Sets | Sessions/projects | Cloud projects | MISSING | [studio/index.html][studio], S, stores voice buffers in memory and warns leaving clears takes. Add durable local audio chunks, project snapshots and reopen/recovery before expanding recording depth. |
| S-C02 Save/reopen editable beat choices | Projects/presets | Projects/presets | Sets/presets | Sessions/presets | Projects | HAVE | [studio/beatlab.js][beatlab], recipe/saveNow/openRecipe, stores recent/kept recipes; [studio/save.js][save] embeds/reads them in WAV/MP3. |
| S-C03 Full version history and branches | Project alternatives | Versions | Set versions | Session/cloud workflows | Revision history | PARTIAL | [studio/beatlab.js][beatlab] updates the current recipe and keeps recent rolls; [studio/index.html][studio] has temporary undo. Add immutable edit history and recoverable branches. |
| S-C04 Invite collaborators and share an editable project | + sharing | + sharing | + sharing | Cloud projects | Shared projects | MISSING | [studio/save.js][save] shares output files, not a synchronized project. Add scoped editable links, asset transfer and explicit roles without requiring login just to listen. |
| S-C05 Concurrent editing, presence and conflicts | + | + | + | Shared-track workflow | Live/project tools | MISSING | [studio/index.html][studio] and [studio/beatlab.js][beatlab] have no sync protocol. Add ordered operations, presence, conflict/merge handling and offline reconnect. |
| S-C06 Time-linked comments and review versions | + | + | + | Project/review tools | Social/project tools | MISSING | [studio/index.html][studio] has no review record. Add comments on exact time ranges, mix versions, clip IDs and history events. |
| S-C07 Remote recording, talkback and jam sessions | + service | + service | Link/+ remote audio | + remote audio | Live sessions/+ | MISSING | [studio/index.html][studio], getMic/start, is local only. Add remote capture with clock alignment, talkback, delay-aware monitoring and separately designed live-jam paths. |
| S-C08 Public song pages, embeds and remix | + host | + host | + host | + host | Publishing/forking | MISSING | [studio/save.js][save] exports files but creates no song page. Add public listen pages, credits, tips, stems/recipe options and remix branches linked to the original. |
| S-C09 Requests to the crew | + external | + external | + external | + external | Social/tools | HAVE | [studio/index.html][studio], reqSend, sends text to beat_requests. This is a request inbox, not automatic composition or collaboration on audio. |
| S-C10 Cross-device backup and offline operation | Files/cloud sync | Files/cloud sync | Files/cloud sync | Files/cloud | Cloud/mobile | PARTIAL | [studio/beatlab.js][beatlab] and [studio/lyrics/lyrics.js][lyrics] use localStorage; [studio/index.html][studio] does not persist audio or cache the app. Add offline assets, portable backup, sync and migration. |

## Stems, AI assistance and work beyond a conventional DAW

Use current primary references: [Logic feature/hardware availability][logic-ai], [FL stem separation][fl-features], [Live updates][live-new], [BandLab Splitter][band-splitter] and [AutoMix][band-automix]. Existing rules-based generation deserves an honest label: our Beat Lab does not use a trained music model.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-B01 Export separate generated beat parts | Track bounce | Split mixer tracks | Track export | Stems/bounce | Track download | PARTIAL | [studio/beatlab.js][beatlab], getParts/render(only), makes drums/bass/keys/melody WAVs. Each part is mastered separately; they are not demonstrated to sum to the full mix. Add pre-master aligned stems and a shared mastering policy. |
| S-B02 Separate an uploaded recording into sources | Stem Splitter | Stem Separation | Suite Stem Separation | + plugin | Splitter | MISSING | [studio/beatlab.js][beatlab], getParts, only rerenders known synth parts; [studio/index.html][studio] has no source-separation model. Add stem separation with quality limits and retained original. |
| S-B03 Automatic mix balancing and cleanup | Assistant/plugins | Cloud/+ | + | + plugins | AutoMix/cleaner | MISSING | [studio/index.html][studio] has fixed cleanup and manual faders. Add analysis-driven, editable mix/cleanup operations with level-matched comparison. |
| S-B04 Text/voice commands that edit this project | + integrations | AI assistant | + integrations | SDK/+ | Assistant/tools | MISSING | [studio/index.html][studio], reqSend, only queues text. Add an AI command adapter to the same durable editing operations the user performs. |
| S-B05 Generate/continue music as editable notes | Session players | Chord/generator tools | MIDI generators | MIDI/+ | SongStarter/+ | PARTIAL | [studio/beatlab.js][beatlab], compose/roll, produces editable-in-code motifs and chords from rules. Add note-level editing, phrase continuation and optional model adapters with clear origins. |
| S-B06 Transcribe speech, lyrics, beats and melody | Tools/+ | Tools/+ | Audio-to-MIDI/+ | ARA/+ | Tools/MIDI options | MISSING | [studio/lyrics/lyrics.js][lyrics] expects typed lyrics; [studio/index.html][studio] has no transcription. Add word/phoneme, pitch, chord, onset and MIDI transcription with uncertainty. |
| S-B07 Engine cover art and scene-based music video | + | + | + | + | + | MISSING | [studio/save.js][save], recordVideo, draws a fixed 2D visualizer. Connect the actual engine scene/camera timeline and artwork renderer. |
| S-B08 Sound from material/physics/vision events | + custom systems | + custom systems | + custom systems | + custom systems | + | MISSING | [studio/index.html][studio] has no event-history reader. Import contacts, footsteps, wetting, motion and observation events as editable, source-linked audio. |
| S-B09 Explain every musical change and generated sound | + logs | + logs | + logs | + logs | Revisions/+ | PARTIAL | [studio/beatlab.js][beatlab] saves seeds/choices; [studio/index.html][studio], S.history, lacks durable causal records. Add common event IDs, source evidence, model/rule versions and readable explanations. |

## Export and interchange

Reference workflows are [Logic projects/output][logic], [FL export-capable editions][fl-editions], [Live manual][live], [Pro Tools formats/features][pt-editions] and [BandLab projects][band-start]. A renderable stereo mix, a stem package and an editable project are three separate deliverables.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-E01 Offline stereo song bounce | Bounce | Render | Export | Bounce | Mixdown | HAVE | [studio/index.html][studio], render/save, uses OfflineAudioContext and the voice mix graph. |
| S-E02 WAV and MP3 files | Supported | Supported | Supported | Supported | Downloads | HAVE | [studio/index.html][studio], wav, writes 16-bit WAV; [studio/save.js][save], encodeMp3, writes 192 kbps stereo MP3 through vendored lamejs. |
| S-E03 Vocal-only mix | Track/output bounce | Routing/export | Routing/export | Routing/bounce | Track/mix download | HAVE | [studio/index.html][studio], save(false), omits the beat and sums unmuted voice layers. This is one vocal mix, not every voice track separately. |
| S-E04 Individual tracks, dry/wet stems and batch ranges | Track export | Split tracks | Track export | Multi-source bounce | Track downloads | PARTIAL | [studio/beatlab.js][beatlab] exports beat parts; [studio/index.html][studio] cannot export each voice layer/take. Add aligned dry/wet track/bus/region batches with manifests. |
| S-E05 Stems recombine to the intended mix | Routing/settings | Routing/settings | Routing/settings | Routing/settings | Export dependent | MISSING | [studio/beatlab.js][beatlab], render, masters every part independently; [studio/index.html][studio], wav, peak-scales each file. Preserve common gain, starts/tails and dry stems; test a pre-master recombination separately from nonlinear master processing. |
| S-E06 Sample rate, depth, format and channel options | Bounce options | Export options | Export options | Bounce options | Download options | PARTIAL | [studio/index.html][studio], render/wav, fixes 44.1 kHz/16-bit/stereo; [studio/save.js][save] fixes MP3 bitrate by default. Add float/24-bit WAV, FLAC/other codecs, rates, layouts and codec settings. |
| S-E07 Trim range, loop, tail and realtime/offline choice | Bounce controls | Export controls | Export controls | Bounce controls | Mixdown options | PARTIAL | [studio/index.html][studio], render, bounces full duration plus 0.5 seconds. Add exact selections, tail policy, batch jobs and reliable progress/cancel/recovery. |
| S-E08 Share/download on a phone | OS sharing | File/share | File/share | File/share | Share/download | HAVE | [studio/save.js][save], openSave, offers file sharing, visible links and destination guidance. Actual OS share/video support needs device verification. |
| S-E09 Video for Photos/Gallery and social posting | Movie/+ | Video/+ | Video/+ | Video/+ | + tools | PARTIAL | [studio/save.js][save], recordVideo, makes a 540×960, 30 fps visualizer with realtime MediaRecorder. Add artwork, lyrics, engine shots, resolutions and reliable offline encoding. |
| S-E10 Editable recipe travels with audio | Project + metadata | Project + metadata | Set + metadata | Session + metadata | Cloud project | HAVE | [studio/save.js][save], embedRecipe/readRecipe, stores Beat Lab choices in WAV LIST/INFO or MP3 ID3 TXXX. It restores only the beat and is not tamper-proof or guaranteed to survive transcoding. |
| S-E11 Portable complete session and DAW interchange | Project/AAF | Project/stems/MIDI | Set/stems/MIDI | Session/AAF/OMF | Project/stems/MIDI | MISSING | [studio/save.js][save] has no complete-session packer. Add hb-project bundles, collected media, MIDI and interchange adapters with explicit loss reports. |
| S-E12 Credits, artwork, lyrics and broadcast metadata | Metadata/tools | Metadata/tools | Metadata/+ | BWF/metadata | Release metadata | PARTIAL | [studio/save.js][save] uses title/file names and recipe tags, not a release metadata editor. Add ID3/BWF/iXML/cues, contributors, artwork and timed lyrics. |

## Distribution, ownership and getting paid

Logic, Live and Pro Tools primarily create deliverables for external release workflows. FL adds [optional FL Cloud/DistroKid distribution][fl-cloud]; BandLab offers [distribution and membership tools][band-membership]. The target is to handle a complete release inside Heartbeat with adapters and clear records, not to claim every DAW is itself a distributor.

| ID / capability | Logic Pro | FL Studio | Ableton Live | Pro Tools | BandLab | Ours | Evidence and work for the general build |
|---|---|---|---|---|---|---|---|
| S-D01 Explain song/master ownership and release steps | + guidance | + guidance | + guidance | + guidance | Education/tools | HAVE | [studio/learn/index.html][learn] has a sourced U.S. guide covering song vs master, registration, splits, royalties, distribution and Content ID. It is education, not a filing service. |
| S-D02 Rights-aware asset and contribution ledger | + | + service | + | + | Collaboration/terms | MISSING | [studio/learn/index.html][learn] describes rights but [studio/index.html][studio] stores no asset/contributor ledger. Track composition/master ownership and permissions per source and contribution. |
| S-D03 Split sheets, credits and agreements | + | + distributor | + | + | Distribution/+ | PARTIAL | [studio/learn/index.html][learn] lists what a split sheet needs. Add actual records, separate song/master totals, versions and exportable agreements. |
| S-D04 Public release page with tips and licensing | + host | + host | + host | + host | Publishing/social | MISSING | [studio/save.js][save] only creates local files. Add Heartbeat song/release pages, credits, license choices, tips and stems/remix links. |
| S-D05 Store/streaming distribution and status tracking | + distributor | + FL Cloud | + distributor | + distributor | Distribution | MISSING | [studio/learn/index.html][learn] links to distributors; no submission/status code exists in [studio/index.html][studio]. Add provider adapters, validated release packages, delivery states and corrections/takedowns. |
| S-D06 ISRC/UPC, release metadata and artwork checks | + release tools | + distributor | + release tools | + release tools | Distribution | MISSING | [studio/save.js][save] has no release object. Add recording/release identifiers, metadata validation, explicit labels, dates and artwork specifications. |
| S-D07 Publishing/PRO/mechanical/neighbouring-right registrations | + external | + external | + external | + external | + external | PARTIAL | [studio/learn/index.html][learn] explains distinct collection lanes. Add exportable registration data and permitted integrations; a guide does not submit or collect royalties. |
| S-D08 Royalty reports, splits and payouts | + external | + distributor | + external | + external | Distribution | MISSING | [studio/learn/index.html][learn] is informational. Add statement import, auditable allocation, payment status and provider connections. |
| S-D09 Sample/cover/voice permissions and Content ID eligibility | + external | + external | + external | + external | Rules/distributor | PARTIAL | [studio/learn/index.html][learn] covers these boundaries; [studio/index.html][studio] stores no proof. Attach permissions/exclusivity evidence and eligibility reports to release records. |
| S-D10 Open/CC0 choices without erasing third-party rights | Owner's license | Owner's license | Owner's license | Owner's license | Creator terms | PARTIAL | [studio/index.html][studio] labels Heartbeat beats CC0; [studio/save.js][save] identifies its own code as CC0 and lamejs as LGPL. Add explicit source/dependency licenses; do not label imported music, a user's voice, or every library CC0. |
| S-D11 Release revisions, source receipts and audit trail | + project/service | + project/service | + project/service | + project/service | Revisions/distribution | MISSING | [studio/save.js][save] embeds beat choices but no signed/revisioned release manifest. Record exact source versions, mix/export hashes, metadata, rights and delivery receipts. |

## What is Heartbeat's own advantage, and what can go beyond parity

These are our own product connections and commitments, not a claim that no other tool has AI, revisions, privacy or open code. The distinction is making one inspectable system across sound, scenes and evidence.

| Capability | State | Evidence and direction |
|---|---|---|
| A phone studio that records locally and needs no studio account | HAVE | [studio/index.html][studio] captures/mixes on-device. Text beat requests are the explicit network write; audio is not uploaded by the recording/export paths. Keep this local route as the full project system grows. |
| Explainable, seeded beats instead of an opaque audio result | HAVE | [studio/beatlab.js][beatlab], compose/roll, preserves scales, chords, seeds and style choices. Expose every note and sound as editable data. Same recipe does not mean exclusive ownership or guaranteed bit-identical output on every device. |
| The editable beat recipe lives inside WAV/MP3 | HAVE | [studio/save.js][save], embedRecipe/readRecipe. Extend it with a portable project/asset manifest; retain a separate bundle because other apps may strip tags. |
| Every take, edit, note and sound has a readable history | PARTIAL | [studio/index.html][studio], S.history, and [studio/beatlab.js][beatlab], My beats, are separate limited records. Adopt engine/vision history with durable event IDs, exact clocks, source links and complete session recovery. |
| Honest heard/recorded, rebuilt, patched and made labels | MISSING | [studio/index.html][studio] and [studio/save.js][save] have no such schema. Use common seen/rebuilt/patched/made basis values; show seen audio as recorded/heard in the UI and distinguish AI/processed/derived segments. |
| Material physics becomes music and sound design | MISSING | Engine seed: [hb-render/src/physics-library.js][physics] and [hb-render/src/history.js][engine-history]. Import impacts, movement and fluids as editable sound events; send music/automation back to scene lights and motion. |
| AI operates the same tools the artist can inspect | MISSING | [studio/index.html][studio] only sends beat requests. Add UI/AI/MCP adapters over one command model with durable undo and explanations. |
| Open code, CC0 Heartbeat-created materials and public listening | PARTIAL | CC0 beats/code labels are in [studio/index.html][studio] and [studio/save.js][save]; a complete Studio license inventory/public project publisher is absent. Keep dependencies' licenses and creators' rights visible. |
| A song, filmed place, character and video are one project | MISSING | [studio/save.js][save] only draws a visualizer. Connect the engine/director/vision surfaces with exact timing and preserved evidence. |

## Proposed architecture for ONE general build

This is the same proposal as the engine map: **one project model, shared libraries and event history, several editing surfaces**. The modules below are proposed work, not folders claimed to exist today. The full parity list remains in scope.

### 1. One project and shared libraries

Use **hb-project/1** for the whole song/scene/shot/evidence project. Give tracks, clips, takes, notes, sounds, people, materials and source assets stable IDs. Store original audio/video in hash-addressed chunks; store edits, plugin settings, tempo maps and recipes as versioned data. Use durable browser storage such as OPFS/IndexedDB behind an adapter, with file bundles and optional remote sync. Keep original takes before processed derivatives. Opening a local project and listening to a public release should not require an account.

| Module | Responsibility | Reuse first |
|---|---|---|
| core/project + assets | Durable originals, manifests, versions, edit transactions, undo/redo, recovery, dependencies, rights and import/export | Studio recipes, lyric storage, engine scene JSON/catalogs |
| core/time + history | Exact sample/frame/physics clocks, tempo mapping, events, provenance, source/causal queries and checkpoints | [hb-render/src/history.js][engine-history] and [lab/bedroom-unified/history.js][vision] |
| libraries/materials | Shared visual/mechanical/liquid/porous/thermal/acoustic definitions | [hb-render/src/physics-library.js][physics] |
| libraries/geometry + physics | General geometry, colliders and rigid/cloth/soft/fluid/strand/gas systems emitting common events | Existing engine mesh/BVH/fluid/surfacing code |
| libraries/audio | Real-time/offline DSP graph, instruments, sampler, pitch/time analysis, metering, conversion and encoding | [studio/beatlab.js][beatlab], [studio/index.html][studio], [studio/save.js][save] |
| engine/runtime + renderers | Scene state, animation, world streaming, interactive/path-traced picture, input and XR | Existing hb-render |
| studio + director | Audio/MIDI/take/automation editors, arrangement, mixer, mastering, lyrics and multi-shot picture timelines | Existing phone recorder, Beat Lab and camera paths |
| vision | Source observations, reconstructed tracks, calibration, uncertainty and generated fills | Bedroom evidence/history experiment |
| automation + services | UI/AI/MCP commands, workers, collaboration, public pages, rights/release and distribution adapters | Engine writer/MCP queues and existing publishing pieces |

The **audio engine** needs one graph for live playback, recording monitoring, freeze and offline rendering. Every processor declares ports, channel layouts, latency, tail length, automatable parameters, state/version and real-time/offline behavior. Run real-time work in AudioWorklets/WASM as appropriate; keep file encoding and heavy analysis away from the audio deadline. Use a portable web plugin contract plus an optional native bridge for native formats. Do not put a separate hard-coded master chain inside each stem render.

Separate **mixing**, **mastering** and **delivery encoding**. Stems start at a shared origin, retain a common gain policy and either bypass the nonlinear master or declare how that master is delivered. Measure whether pre-master stems recombine correctly. Measure the decoded MP3/video output as well as the floating-point mix.

The **material library** joins sound to the world. A surface ID can define roughness/absorption for rendering, friction/elasticity for physics and resonance/absorption/contact response for sound. A footstep or water impact supplies time, position, force/speed and both materials; audio creates an editable sound entity linked to that event. Record whether a property was measured, estimated or chosen for art. Solver coefficients and audio approximations are not interchangeable physical constants.

### 2. One event-history format for engine, Studio and vision

Adopt **hb-history/2** with adapters from the existing hb-history/1 writers and Studio recipes/temporary undo. Both engine and bedroom files currently use the v1 name, but their entity/sample/provenance fields differ. The bedroom JSONL path omits some richer JSON metadata. Studio's S.history is not an implementation of hb-history/1. Preserve original records and mark missing/unknown information when converting.

The shared contract is:

| Field or record | Rule |
|---|---|
| meta / clocks | Version, project/run/branch IDs, tools/seeds, units and coordinate frames. Streams use integer ticks with rational rates: original audio samples, video frames and physics steps remain exact. Store mappings to project time and the beat/tempo/meter map. |
| entity / asset | Stable ID, kind, label, source hash, material, rights and attachment/parent relationships. A clip references original media plus source offsets; it does not overwrite samples whenever trimmed. |
| event | Unique event ID, sequence, time, type, subject, targets, actor/tool, parameters and result. Cause event IDs are separate from actors and entity ancestry. Types include record.start/stop, take.created, clip.split, note.on/off, parameter.changed, render.completed and contact.begin. |
| provenance / basis | Common seen/rebuilt/patched/made values at entity, event, track-segment and media-region level. For audio, seen means captured/recorded/heard evidence in plain UI wording. Keep source frame/sample ranges, method, uncertainty and permissions. Synthesized or generated content stays made. A processed recording retains its original capture plus a distinct transformation record. |
| tracks / measurements | Typed audio, MIDI, automation, pose, position and observation streams with units/interpolation/uncertainty. Keep sample arrays in media chunks, not one JSON row for every audio sample. |
| coverage | Sampling rate, filters, rounding, gaps, dropped counts and complete/sampled/derived status. Do not imply a compressed trail or selected measurements record every event. |
| snapshot / checkpoint | State needed to restore the subsystem: audio originals, edits, plugin states/versions, graph, automation, transport, RNG/solver and references. A final WAV or screenshot alone cannot restore an editable project. |
| edits / branches / exports | Durable operations and branches; corrections append records. Every export names project revision, source/history ranges, mix/master/codec settings, rights and output hash. |

Example connection: physics emits an impact at a tick on its clock; the time service maps it to an audio sample; the sound engine creates a made sound with the impact event as cause; Studio trims or replaces it and records that edit; the director uses the same clock for picture. Vision can supply a recorded footstep or a reconstructed motion track, with the evidence basis attached. A later AI answer can say which sound came from which contact and which parts were made.

Do not infer causation from close timestamps or an entity parent. Do not call a saved/generated waveform a recorded performance. Do not promise cross-device bit identity: save authoritative output where exact recovery matters, and document tolerances and versions for replay.

### 3. Build order and acceptance sessions

This is the dependency order within the one complete build. It is not a shortened feature list.

1. **Contracts and permanent projects.** Implement the common project, asset, clock and history formats with migrations. Persist a real microphone take as chunks, reload, recover an interrupted capture and reopen the complete song/scene/evidence project. This removes the current loss-of-takes gap first.
2. **Shared material, physics and audio libraries.** Extract the existing engine/Beat Lab/recorder code into reusable modules. Establish channel layouts, processor latency/tails, live/offline parity and measured metering. Prove a material-driven contact produces editable, correctly timed sound and traceable history.
3. **General editing and automation.** Build the common editor/command API, scene tree, timeline, undo/redo and asset browser. Complete clip split/move/trim/fades, take lanes/comping, section edits, piano roll and MIDI recording. Prove touch, keyboard and AI commands preserve the same IDs and replayable edits.
4. **General simulation and animation.** In the shared engine, complete colliders/joints, rigid/cloth/soft/fluid/destruction/gas/strand systems and character/rig animation. In Studio, consume those events as sound and automation; prove a character/environment interaction is inspectable in both picture and audio.
5. **Rendering, world and interchange breadth.** Complete interactive/final renderers, materials/volumes, procedural/modeling tools, world streaming/LOD and asset adapters. Complete the corresponding media/plugin/project interchange in Studio. Prove round trips report retained and unsupported data honestly.
6. **Complete Studio and director workflows.** Finish multitrack input, monitoring, pitch/time tools, sampler/instrument depth, effects/buses/automation, mastering/QC, aligned stems, lyrics, cover art and music-video export. Prove an empty-session recording can become a comped, arranged, mixed, mastered release; pre-master stems recombine and picture remains synchronized.
7. **Collaboration, networking, XR and delivery.** Complete concurrent projects/reconnect/conflicts, remote recording, public listen/remix pages, engine runtime networking/XR/native adapters and rights-aware distribution services. Prove separate-device edits, media transfer, credits/splits and release-status recovery. Keep provider-specific credentials/terms in adapters, not in the project format.
8. **Run one complete connected proof.** Use a filmed place with explicit seen/made regions, a rigged character and interacting materials; generate and edit source-linked sound; record/comp a vocal, arrange MIDI/samples, mix/master, create cover art/video, export a session and aligned stems, publish a listen/remix page, then reopen and branch it on another device. Document local checks, live checks and unverified behavior separately. Every unfinished row remains a task.

Each row ID should map to code, supported devices/backends, usable controls, persistent state, history/rights behavior and a meaningful test session. Keep phone controls simple while leaving the complete tools reachable. Do not call a feature complete because a parameter exists in code or one demonstration exported.

**Next thing:** write the shared project, clock and history schemas against the current engine, Studio and bedroom formats; make the first acceptance session save and reopen original voice takes without losing edits.

[studio]: ../../../Projects/heartbeat-observatory/studio/index.html
[beatlab]: ../../../Projects/heartbeat-observatory/studio/beatlab.js
[save]: ../../../Projects/heartbeat-observatory/studio/save.js
[lyrics]: ../../../Projects/heartbeat-observatory/studio/lyrics/lyrics.js
[lyrics-page]: ../../../Projects/heartbeat-observatory/studio/lyrics/index.html
[learn]: ../../../Projects/heartbeat-observatory/studio/learn/index.html
[physics]: ../../../Projects/hb-render/src/physics-library.js
[engine-history]: ../../../Projects/hb-render/src/history.js
[vision]: ../../../Projects/heartbeat-observatory/lab/bedroom-unified/history.js
[logic]: https://www.apple.com/uk/logic-pro/
[logic-comp]: https://support.apple.com/en-bw/guide/logicpro/lgcp317d758e/10.7/mac/11.0
[logic-flex]: https://support.apple.com/en-ae/guide/logicpro/lgcp15968647/12.3/mac/15.6
[logic-plugins]: https://support.apple.com/en-gb/guide/logicpro/lgcpbc218dde/10.7/mac/11.0
[logic-sampler]: https://support.apple.com/en-asia/guide/logicpro/lgsifc860d24/mac
[logic-master]: https://support.apple.com/en-bh/108294
[logic-ai]: https://support.apple.com/en-us/120406
[fl-features]: https://www.image-line.com/fl-studio/features
[fl-editions]: https://www.image-line.com/fl-studio/compare
[fl-mixer]: https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/mixer.htm
[fl-playlist]: https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/playlist.htm
[fl-piano]: https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/pianoroll.htm
[fl-cloud]: https://www.image-line.com/fl-cloud/whats-included
[live]: https://www.ableton.com/en/live-manual/12/
[live-record]: https://www.ableton.com/en/live-manual/12/recording-new-clips/
[live-comp]: https://www.ableton.com/en/live-manual/12/comping/
[live-routing]: https://www.ableton.com/en/live-manual/12/routing-and-i-o/
[live-mix]: https://www.ableton.com/en/live-manual/12/mixing/
[live-mpe]: https://help.ableton.com/hc/en-us/articles/360019144999-MPE-in-Live-FAQ
[live-tuning]: https://help.ableton.com/hc/en-us/articles/11535414344476-Tuning-Systems-FAQ
[live-new]: https://www.ableton.com/en/live/all-new-features
[pt-record]: https://www.avid.com/pro-tools/features/audio-recording
[pt-edit]: https://www.avid.com/pro-tools/features/audio-editing
[pt-mix]: https://www.avid.com/pro-tools/features/audio-mixing
[pt-editions]: https://www.avid.com/pro-tools/comparison
[pt-cloud]: https://kb.avid.com/pkb/articles/en_US/Knowledge/Pro-Tools-Cloud-Collaboration-FAQ
[band-start]: https://help.bandlab.com/hc/en-us/articles/115002945153-Getting-Started-with-the-BandLab-Studio
[band-limits]: https://help.bandlab.com/hc/en-us/articles/115002945433-Track-and-Project-Duration-Limits
[band-input]: https://help.bandlab.com/hc/en-us/articles/115002960114-Connecting-Instruments-and-Microphones
[band-membership]: https://help.bandlab.com/hc/en-us/articles/20758981227033-BandLab-Membership-FAQ
[band-pitch]: https://help.bandlab.com/hc/en-us/articles/29099155628953-AutoPitch-FAQ
[band-collab]: https://blog.bandlab.com/forking-and-collaboration-on-bandlab-explained/
[band-revisions]: https://help.bandlab.com/hc/en-us/articles/360018947313-Protecting-my-Content-on-BandLab
[band-access]: https://help.bandlab.com/hc/en-us/articles/63415042774553-Changes-to-BandLab-Studio-Access
[band-splitter]: https://blog.bandlab.com/splitter/
[band-automix]: https://blog.bandlab.com/how-to-use-automix-bandlab/
