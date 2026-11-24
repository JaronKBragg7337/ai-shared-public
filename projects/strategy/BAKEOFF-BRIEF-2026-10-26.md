# Engine bake-off brief (2026-10-26, 1 AM). Same brief for every AI: Fable 5.1, GPT-6.1 Sol, Kimi K3.1 Pro, Sonnet 5.5

You are one of four AIs given this exact brief. Each of you does the WHOLE job. Jaron (owner, Heartbeat Observatory) will open
all four results on his iPhone and compare them. Work on your own; don't ask questions. Sign anything you write as your model.

## What this is for (the core - read first)
Jaron's "fourth piece": a shared **event history** under everything. Every object gets an ID, a path, speed, what it hit
and what it caused, so **every object can tell its own history** (his book The Necklace: touch anything, see everything
it has seen). Two honesty rules:
- **Real footage** (a video someone uploads): what the camera saw is solid; what we rebuild from evidence is marked
  rebuilt; what was never seen **fades like a memory** (Assassin's Creed style). We never invent the gaps.
- **Constructed worlds** (made by our own tools or AI generators): the engines may BUILD the missing parts, but anything
  made is marked "made", never passed off as seen.
Products this serves: step inside a video as a 3D place (memories, honestly marked), AND games, movies, shows, music
videos. **Find more uses** - list every other use you can think of, and pick 2-3 to show as tiny demos.
It must be **AI-friendly**: any AI (Claude, Grok, ChatGPT, Kimi, later Jaron's own AI) can read a scene and its event
history through one plain doorway (a JSON endpoint/file + a short AI-README; MCP tools if you can).

## What exists (read these, reuse them)
- Live v1 (baseline, tag `bedroom-lab-v1`): C:\Users\lilli\Projects\heartbeat-observatory\lab\bedroom\ - three.js page:
  Grok-made bedroom (depth-filled meshes room.glb), Grok-made man (person.glb, Hunyuan3D-2mini, 17-joint rig), walk from
  video, three faded padlocked doors ("Locked - not seen yet"). Weak: torn right-side lamps/nightstand, jagged bed foot,
  approximate rig + door placement, and **the room is not closed: nobody ever saw the LEFT side looking from the bed**.
  Viewable only from the filmed side.
- hb-vision (C:\Users\lilli\Projects\hb-vision): run.py (skeleton tracking -> history.json event format), room.py (SfM),
  room_depth.py, room_mesh.py, room_doors.py, build_person.py, walk_cycle.py, detail.py (slow-mo/zoom, SEEN/MADE
  stamps). Rooms out/rooms/grok-bedroom/. Inputs C:\Users\lilli\media\video-drops\2026-10-25\grok-* (room videos,
  stills, man anchor/turntable/walk).
- hb-render (C:\Users\lilli\Projects\hb-render): WebGPU path tracer + fluid sim; event history (ids W-####/D-####,
  fields t/position/velocity/event/target/children); mcp/server.mjs (render_scene, trace_object, events_between).
- Necklace view (tap a drop, see its story): heartbeat-observatory\lab\necklace\.
- Studio (music): heartbeat-observatory\studio\ (beatlab.js, beats/, save.js) - sound on a timeline = events too.
- Strategy notes: C:\Users\lilli\AI-Shared\projects\strategy\FOURTH-PIECE.md (read it).

## Your job - all of it
1. **Bedroom v2** at `heartbeat-observatory\lab\bedroom-<you>\index.html` (you = fable / sol / kimi / sonnet):
   - A **closed room**: floor, ceiling and all four walls. The unseen left wall and gaps get CONSTRUCTED by our side
     (geometry/textures in keeping with the room), shown as **made** (a toggle "show seen / made" is ideal).
   - Fix what you can of v1's tears. The man walks around the room believably (feet on the floor).
   - The three doors stay faded/locked; give ONE door a working **unlock** mechanic (tap -> something happens
     honestly: e.g. it becomes a "made" room beyond, clearly labelled).
   - **Event history live in the page:** the man, his footsteps, door taps etc. get IDs and are recorded; tap an object
     or the man -> see its history (Necklace style). Expose it at `lab/bedroom-<you>/history.json` (or a live JSON view)
     + `lab/bedroom-<you>/AI-README.md` explaining how an AI reads it.
   - **Sound**: footsteps/room tone tied to the events (Studio-style timeline); keep it light, muted until a tap (iOS).
   - Label: "AI-generated person (not real)"; corner credit "Room + person made by Grok Imagine, rebuilt by Heartbeat
     Observatory tools." Keep `<meta name="robots" content="noindex">`, link it from nowhere.
2. **USES.md** in your folder: other uses (games, movies, shows, music videos, + yours), each one line on how this
   stack does it; build 2-3 tiny demos of them inside your page or as sub-pages in your folder.
3. **A 15-30 s vertical (1080x1920) screen recording** of your page in action, saved to
   `C:\Users\lilli\Projects\hb-vision\out\bakeoff\<you>.mp4` (+ a phone screenshot `<you>.png`). It may be used in a
   public post, so make it look good.
4. Any new scripts go in `C:\Users\lilli\Projects\hb-vision\bake\<you>\` (never edit others' or the shared scripts).

## Hard rules
- iPhone Safari is the real target: 375 px wide, no horizontal scroll, touch works, total page weight ideally < 15 MB.
  Pin library versions (cdnjs/jsdelivr). Check it in WebKit/Playwright at 375 px if you can.
- **Do NOT git commit, push, or deploy.** Claude reviews and ships all four. Touch only your own folders.
- GPU (RTX 4060 8 GB): optional. CPU-first. Only use it holding the lock file `C:\Users\lilli\Projects\hb-vision\gpu.lock`
  (create it, delete when done; if it exists, wait or skip). No GPU at all 2:45-7:30 AM (the daily news renders).
- No RunPod. Never print secret values. Never make a real person's likeness; the Grok man is synthetic.
- No military content. Honest labels everywhere (seen / rebuilt / made / not seen).
- Budget: aim to finish in ~2 hours. A working, honest, good-looking page beats a sprawling unfinished one.

## Report back (short)
What you built, what works (numbers), what's weak, the uses you found, time taken, file paths.
