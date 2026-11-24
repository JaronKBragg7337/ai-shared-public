// Path B, piece 1: the learner's own mind, in one file. learner/learn.mjs measures it in Node; the 3D Reading Room
// (reading-room-3d/main.js) carries the very same functions as the lantern. Nothing here is told what a mark means.
//
// It takes the four engine pieces it needs as arguments, so the same file loads in Node, in the page, and in the flat
// published copy where every file sits in one folder:
//   const mind = makeMind({ rng, buildRoom, marksOf, openSettings });   // rng from world.js, the rest from rooms.js
export function makeMind({ rng, buildRoom, marksOf, openSettings }) {
  const ones = (m) => { let c = 0; while (m) { m &= m - 1; c++; } return c; };

  // ---------------------------------------------------------------- rooms drawn at random from the Reading Room's own parts
  function randomRoom(r) {
    for (;;) {
      const n = 3 + Math.floor(r() * 3), lamps = 1 + Math.floor(r() * 3), things = [];
      for (let i = 0; i < n; i++) things.push({ id: String(i + 1), kind: 'switch' });
      const draw = (pool, most) => {
        const bag = [...pool], wires = [], k = 1 + Math.floor(r() * Math.min(most, bag.length));
        for (let j = 0; j < k; j++) wires.push([bag.splice(Math.floor(r() * bag.length), 1)[0], r() < 0.3 ? -1 : 1]);
        if (!wires.some(([, w]) => w > 0)) wires[0][1] = 1;        // at least one bright wire, or it could never glow
        return wires;
      };
      const markFor = (wires) => 1 + Math.floor(r() * wires.filter(([, w]) => w > 0).length);
      for (let j = 0; j < lamps; j++) { const wires = draw(things.map((t) => t.id), 3); things.push({ id: 'ABC'[j], kind: 'lamp', mark: markFor(wires), wires }); }
      const lampIds = things.filter((t) => t.kind === 'lamp').map((t) => t.id), first = lampIds[Math.floor(r() * lampIds.length)];
      const more = r() < 0.75 ? draw(things.map((t) => t.id).filter((id) => id !== first), 2) : [];
      const wires = [[first, 1], ...more];
      things.push({ id: 'D', kind: 'door', mark: markFor(wires), wires });
      const open = openSettings(things);
      if (!open.length || open.includes(0)) continue;               // it must be openable, and shut at the start
      return { things, open, n };
    }
  }

  // ---------------------------------------------------------------- a look: only what is drawn and what is visible
  function see(t, room) {
    const lit = room.E.out[room.at[t.id]] === 1, m = marksOf(t, lit, (k) => room.E.out[room.at[t.wires[k][0]]] === 1);
    return { sign: m.sign, lever: m.kind === 'switch', glow: lit, squares: m.squares ? m.squares.length : 0,
      circles: (m.wires || []).map((w) => ({ dashed: w.dark, filled: w.live, label: w.from })) };
  }

  // ---------------------------------------------------------------- the learner: nothing but weights at zero and five unscored guesses
  const GUESSES = ['never', 'place', 'before', 'host', 'named'];    // on a tie the earlier one wins, so the true one (last) has to earn it
  // circles: how many circles it has looked at (each look at a circle scores every guess once). Only counted, never used to choose.
  const newLearner = () => ({ w: new Float64Array(6), score: Object.fromEntries(GUESSES.map((g) => [g, 0])), looks: 0, wrong: 0, circles: 0 });
  const trusted = (L) => GUESSES.reduce((best, g) => (L.score[g] > L.score[best] ? g : best), GUESSES[0]);
  const dot = (w, f) => w[0] * f[0] + w[1] * f[1] + w[2] * f[2] + w[3] * f[3] + w[4] * f[4] + w[5] * f[5];
  function fillGuess(g, scene, i, k, c, glowOf) {                   // "this circle is filled when ..."
    if (g === 'never') return false;
    if (g === 'host') return glowOf(i);                             // ... the thing wearing it glows
    if (g === 'before') return i > 0 && glowOf(i - 1);              // ... the thing standing just before glows
    if (g === 'place') return k < scene.length && glowOf(k);        // ... the thing in the same place along the wall glows
    const j = scene.findIndex((o) => o.sign === c.label);           // ... the thing whose sign is drawn under it glows (the truth)
    return j >= 0 && glowOf(j);
  }
  function counts(circles, filledOf) {
    let sf = 0, df = 0, se = 0, de = 0;
    circles.forEach((c, k) => { const filled = filledOf(c, k); if (c.dashed) { if (filled) df++; else de++; } else if (filled) sf++; else se++; });
    return [sf, df, se, de];
  }
  function learn(L, scene) {                                        // one walk along the wall, looking at each thing once
    scene.forEach((s, i) => {
      L.looks++;
      if (s.lever) return;
      const [sf, df, se, de] = counts(s.circles, (c) => c.filled), f = [s.squares, sf, df, se, de, 1];
      const guess = dot(L.w, f) > 0 ? 1 : 0, truth = s.glow ? 1 : 0;
      if (guess !== truth) { L.wrong++; for (let k = 0; k < 6; k++) L.w[k] += (truth - guess) * f[k]; }      // Rosenblatt's rule
      s.circles.forEach((c, k) => { L.circles++; for (const g of GUESSES) if (fillGuess(g, scene, i, k, c, (j) => scene[j].glow) === c.filled) L.score[g]++; });
    });
  }
  function think(L, scene, mask) {                                  // imagine the levers standing like this, by its own two rules only
    const g = trusted(L), glow = []; let lever = 0, doubt = Infinity;
    for (const s of scene) glow.push(s.lever ? ((mask >> lever++) & 1) === 1 : false);
    const weigh = (s, i) => { const [sf, df, se, de] = counts(s.circles, (c, k) => fillGuess(g, scene, i, k, c, (j) => glow[j])); return dot(L.w, [s.squares, sf, df, se, de, 1]); };
    for (let sweep = 0; sweep <= scene.length; sweep++) {
      let changed = false;
      scene.forEach((s, i) => { if (s.lever) return; const now = weigh(s, i) > 0; if (now !== glow[i]) { glow[i] = now; changed = true; } });
      if (!changed) break;
    }
    scene.forEach((s, i) => { if (!s.lever) doubt = Math.min(doubt, Math.abs(weigh(s, i))); });     // how undecided it is, somewhere in the room
    return { glow, doubt };
  }
  const imagine = (L, scene, mask) => think(L, scene, mask).glow;

  // ---------------------------------------------------------------- its two choices
  // Where to go next: imagine every setting not tried yet and go to the nearest one it expects to open the door.
  // Nothing expected to work (or no learner, or it cannot read yet): the nearest setting not tried yet, by chance among equals.
  function chooseGoal(L, scene, setting, tried, n, r) {
    let goal = -1, near = 99;
    if (L) for (let s = 0; s < (1 << n); s++) {
      const d = ones(s ^ setting); if (tried.has(s) || d >= near) continue;
      if (imagine(L, scene, s)[scene.length - 1]) { goal = s; near = d; }
    }
    if (goal < 0) {
      const pool = []; near = 99;
      for (let s = 0; s < (1 << n); s++) { if (tried.has(s)) continue; const d = ones(s ^ setting); if (d < near) { near = d; pool.length = 0; } if (d === near) pool.push(s); }
      if (!pool.length) return -1;                                  // every setting already seen (only if someone else flipped too)
      goal = pool[Math.floor(r() * pool.length)];
    }
    return goal;
  }
  // A play flip, once the door is open: of the settings one flip away, one not seen in this room comes first, and among
  // those the one where its own weighing is closest to undecided for some thing (ties by chance). Returns the lever.
  function choosePlay(L, scene, setting, tried, n, r) {
    let pool = [], least = Infinity, fresh = false;
    for (let b = 0; b < n; b++) {
      const next = setting ^ (1 << b), isFresh = !tried.has(next), doubt = think(L, scene, next).doubt;
      if (isFresh && !fresh) { fresh = true; pool = []; least = Infinity; }               // a setting not seen in this room comes first
      if (isFresh !== fresh) continue;
      if (doubt < least - 1e-9) { least = doubt; pool = [b]; } else if (Math.abs(doubt - least) <= 1e-9) pool.push(b);
    }
    return pool[Math.floor(r() * pool.length)];
  }

  // ---------------------------------------------------------------- living through a room, one act at a time
  // A generator over a running room (made by buildRoom from def.things). It yields what it wants to do next:
  //   { act: 'look' }            it is about to walk along the wall; when resumed it takes the look and learns from it
  //   { act: 'flip', b, play }   flip lever b (the caller flips it, then resumes)
  //   { act: 'opened' }          the door is open; the play flips (if any) come next
  // and returns { flips, playFlips }. It reads the levers back from the room before each choice, so in the 3D room a
  // person may flip levers too. Run headless (play() below) it is exactly the measured learner.
  // L given: the reader-learner (playful: it may stay and flip just to look). L absent: the careful watcher.
  function* life(def, room, r, L, playful = false) {
    const n = room.switches.length, door = room.at[room.door.id];
    const levers = () => { let s = 0; for (let b = 0; b < n; b++) if (room.E.out[room.at[room.switches[b].id]]) s |= 1 << b; return s; };
    let scene = null, setting = levers(), flips = 0, playFlips = 0; const tried = new Set([setting]);
    const flipTo = function* (b, play) { yield { act: 'flip', b, play }; setting = levers(); tried.add(setting); };
    const look = function* () { yield { act: 'look' }; scene = def.things.map((t) => see(t, room)); learn(L, scene); };
    if (L) yield* look();
    while (!room.E.out[door]) {
      setting = levers(); tried.add(setting);
      let goal = chooseGoal(L, scene, setting, tried, n, r);
      if (goal < 0) { tried.clear(); tried.add(setting); goal = chooseGoal(L, scene, setting, tried, n, r); }
      for (let b = 0; b < n && !room.E.out[door]; b++) if (((goal ^ setting) >> b) & 1) {     // go there one flip at a time, looking after each
        yield* flipTo(b, false); flips++;
        if (L) yield* look();
      }
    }
    yield { act: 'opened' };
    if (L && playful) for (let step = 0; step < n; step++) {        // the door is open; stay and play, led by its own doubt
      setting = levers(); tried.add(setting);
      yield* flipTo(choosePlay(L, scene, setting, tried, n, r), true); playFlips++;
      yield* look();
    }
    return { flips, playFlips };
  }
  // The same life, all at once, with nothing drawn.
  function play(def, r, L, playful = false) {
    const room = buildRoom(def.things), it = life(def, room, r, L, playful);
    for (let step = it.next(); ; step = it.next()) {
      if (step.done) return step.value;
      if (step.value.act === 'flip') { const part = room.at[room.switches[step.value.b].id]; room.E.set(part, room.E.out[part] ? 0 : 1); }
    }
  }

  // ---------------------------------------------------------------- the reading test: rooms it will never play
  const HELD = 10, SETTINGS = 4;
  const heldR = rng(424242), held = [];
  for (let i = 0; i < HELD; i++) { const def = randomRoom(heldR), masks = []; for (let j = 0; j < SETTINGS; j++) masks.push(Math.floor(heldR() * (1 << def.n))); held.push({ def, masks }); }
  const KINDS = ['plain', 'needs2', 'dark'];
  const kindOf = (t) => (t.wires.some(([, w]) => w < 0) ? 'dark' : t.mark >= 2 ? 'needs2' : 'plain');
  function reading(L) {
    const right = { all: 0, plain: 0, needs2: 0, dark: 0 }, total = { all: 0, plain: 0, needs2: 0, dark: 0 };
    for (const { def, masks } of held) {
      const rest = buildRoom(def.things), scene = def.things.map((t) => see(t, rest));          // the marks as they hang at rest
      for (const mask of masks) {
        const real = buildRoom(def.things); for (let b = 0; b < def.n; b++) if ((mask >> b) & 1) real.E.set(real.at[real.switches[b].id], 1);
        const said = imagine(L, scene, mask);
        def.things.forEach((t, i) => { if (t.kind === 'switch') return; const ok = said[i] === (real.E.out[real.at[t.id]] === 1), kind = kindOf(t);
          total.all++; total[kind]++; if (ok) { right.all++; right[kind]++; } });
      }
    }
    return Object.fromEntries(Object.keys(total).map((key) => [key, right[key] / total[key]]));
  }

  return { ones, randomRoom, see, GUESSES, newLearner, trusted, fillGuess, counts, learn, think, imagine,
    chooseGoal, choosePlay, life, play, HELD, SETTINGS, held, KINDS, kindOf, reading };
}
