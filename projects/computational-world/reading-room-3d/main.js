import * as THREE from 'three';
import { createThumbstick } from 'hb-thumbstick';
import 'hb-device-tier';
import {
  ROOMS, buildRoom, marksOf, thingFromMarks, wordsOf, openSettings,
  fewestFlips, blindAverage, nameOf, count, codeText,
} from 'rr-rooms';
import { Chronicle, stateMark, rng } from 'rr-world';
import { makeMind } from 'rr-mind';
import { makeRoomPaint, readRoomPaint, parseSkin } from './room-skins.js';
import { buildScene } from './room-scene.js';

// The lantern is the Path B learner itself (learner/mind.js, the file learner/learn.mjs measures), not a look-alike.
const mind = makeMind({ rng, buildRoom, marksOf, openSettings });

const EYE = 1.6;
const RADIUS = 0.23;
const WAVE = 330;
const START_PITCH = -0.08;
const MOVEMENT = new Set(['KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ShiftLeft', 'ShiftRight']);
const WIRE_SAMPLES = 512;
const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
const angle = (radians) => Math.atan2(Math.sin(radians), Math.cos(radians));

function wireRoute(link, world) {
  const source = world.objects.get(link.source);
  const target = world.objects.get(link.target.id);
  const spread = (link.input - (link.target.wires.length - 1) / 2) * 0.071;
  const socket = target.inlet.clone();
  if (link.target.kind === 'door') socket.x += spread;
  else socket.z += spread;
  socket.y += link.input * 0.05;
  const from = source.output.clone();
  from.z += (link.branch - (link.branches - 1) / 2) * 0.065;
  const side = Math.sign(source.x);
  const inset = 3.59 - link.row * 0.101;
  const floor = 0.022;
  const at = (x, z) => new THREE.Vector3(x, floor, z);
  const points = [from, at(from.x, from.z), at(side * inset, from.z)];

  if (link.target.kind === 'door') {
    const farLane = world.doorway.z + 0.66 + link.input * 0.12;
    points.push(at(side * inset, farLane), at(socket.x, farLane));
  } else if (Math.sign(target.x) !== side) {
    const crossLane = -2.05 - link.row * (world.depth - 3.7) / Math.max(1, link.total - 1);
    points.push(at(side * inset, crossLane), at(-side * inset, crossLane), at(-side * inset, socket.z));
  } else {
    points.push(at(side * inset, socket.z));
  }
  points.push(at(socket.x, socket.z), socket);
  return points;
}

// Each wire is one measured path through right-angle segments. All wires share one draw call.
function makeWires(links, world, scene) {
  const positions = [], ranges = [], shading = [], indices = [];
  const rows = Math.max(1, links.length);
  const pixels = new Uint8Array(WIRE_SAMPLES * rows);
  const signal = new THREE.DataTexture(pixels, WIRE_SAMPLES, rows, THREE.RedFormat);
  signal.needsUpdate = true;

  links.forEach((link) => {
    const path = wireRoute(link, world);
    const segments = path.slice(1).map((end, i) => end.distanceTo(path[i]));
    const total = segments.reduce((sum, length) => sum + length, 0);
    let along = 0;
    const unit = new THREE.Vector3(), cross = new THREE.Vector3(), up = new THREE.Vector3();
    const yAxis = new THREE.Vector3(0, 1, 0), zAxis = new THREE.Vector3(0, 0, 1);
    const point = new THREE.Vector3();
    segments.forEach((length, i) => {
      if (length < 0.0001) return;
      const start = path[i], end = path[i + 1];
      unit.subVectors(end, start).normalize();
      // On the floor a wire is a wide flat inlay you can follow with your eyes; on a wall it stays slim where it climbs to the thing.
      const rising = Math.abs(unit.y) > 0.9;
      cross.crossVectors(unit, rising ? zAxis : yAxis).normalize().multiplyScalar(rising ? 0.014 : 0.022);
      up.crossVectors(cross, unit).normalize().multiplyScalar(rising ? 0.011 : 0.008);
      const first = positions.length / 3;
      const profile = [[1, 0], [0, 1], [-1, 0], [0, -1]];
      for (const [center, measure] of [[start, along], [end, along + length]]) {
        for (const [a, b] of profile) {
          point.copy(center).addScaledVector(cross, a).addScaledVector(up, b);
          positions.push(point.x, point.y, point.z);
          ranges.push(measure / total, (link.row + 0.5) / links.length, measure, link.weight < 0 ? 1 : 0);
          shading.push(b === 1 ? 1 : b === -1 ? 0.52 : 0.78);
        }
      }
      for (let corner = 0; corner < 4; corner++) {
        const next = (corner + 1) % 4;
        indices.push(first + corner, first + next, first + 4 + corner, first + next, first + 4 + next, first + 4 + corner);
      }
      along += length;
    });
  });

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geometry.setAttribute('range', new THREE.Float32BufferAttribute(ranges, 4));
  geometry.setAttribute('metalShade', new THREE.Float32BufferAttribute(shading, 1));
  geometry.setIndex(indices);
  const material = new THREE.ShaderMaterial({
    side: THREE.DoubleSide,
    toneMapped: false,
    uniforms: {
      signal: { value: signal },
      brass: { value: new THREE.Color('#705836') },
      amber: { value: new THREE.Color('#ffd46e') },
      purple: { value: new THREE.Color('#795996') },
      violet: { value: new THREE.Color('#d6a2ff') },
    },
    vertexShader: `
      attribute vec4 range;
      attribute float metalShade;
      varying vec4 path;
      varying float shade;
      void main() {
        path = range;
        shade = metalShade;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }`,
    fragmentShader: `
      uniform sampler2D signal;
      uniform vec3 brass, amber, purple, violet;
      varying vec4 path;
      varying float shade;
      void main() {
        if (path.w > 0.5 && mod(path.z, 0.24) > 0.151) discard;
        float power = texture2D(signal, path.xy).r;
        vec3 rest = mix(brass * shade, purple * shade, path.w);
        vec3 glow = mix(amber, violet, path.w) * (0.86 + 0.14 * shade);
        gl_FragColor = vec4(mix(rest, glow, power), 1.0);
        #include <colorspace_fragment>
      }`,
  });
  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);
  let animated = false;
  return {
    refresh(now) {
      let moving = false;
      let changed = false;
      for (const link of links) {
        const offset = link.row * WIRE_SAMPLES;
        const active = link.signals.length && link.signals[0].start <= now;
        if (!active && !link.repaint) continue;
        pixels.fill(link.live ? 255 : 0, offset, offset + WIRE_SAMPLES);
        changed = true;
        link.repaint = active;
        for (const pulse of link.signals) {
          if (pulse.start > now) break;
          moving = true;
          const edge = clamp((now - pulse.start) / (pulse.arrive - pulse.start), 0, 1);
          pixels.fill(pulse.to ? 255 : 0, offset, offset + Math.ceil(edge * WIRE_SAMPLES));
        }
      }
      if (changed) signal.needsUpdate = true;
      const wasAnimated = animated;
      animated = moving;
      return moving || wasAnimated || changed;
    },
    dispose() {
      scene.remove(mesh);
      geometry.dispose();
      material.dispose();
      signal.dispose();
    },
  };
}

function beginReadingRoom() {
  const canvas = document.getElementById('view');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  // This room is small (under 2,000 triangles and about 50 MB of painted surfaces at full size), so a phone with
  // WebGL 2 gets the full look and the full-size paint even where the house tier file plays safe for the big worlds
  // (an iPhone reports 4 cores and lands in its lite tier). Only a phone that reports little memory gets the small
  // paint. The frame clock in frame() lowers the sharpness if a phone turns out to struggle.
  const house = window.HBDevice.tier, caps = window.HBDevice.caps;
  const tier = house === 'mobile-lite' && caps.gl.version === 'webgl2' && (caps.memory ?? 4) >= 3 ? 'mobile-high' : house;
  let sharp = Math.min(caps.dpr, tier === 'mobile-lite' ? 1.15 : 2), slow = 0;
  const keys = new Set();
  const player = { x: 0, z: 0, yaw: 0, pitch: START_PITCH, vx: 0, vz: 0, stride: 0, bob: 0, sway: 0 };
  const hintsBar = document.getElementById('controls');
  const tried = { walk: false, look: false };
  function triedIt(what) {                 // once a person has walked and looked, the two hints get out of the way
    if (tried[what]) return;
    tried[what] = true;
    if (tried.walk && tried.look) hintsBar?.classList.add('gone');
  }
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x070818);
  scene.fog = new THREE.Fog(0x070818, 8, 25);
  const camera = new THREE.PerspectiveCamera(78, 1, 0.045, 38);
  camera.rotation.order = 'YXZ';
  const ray = new THREE.Raycaster();
  ray.far = 3.5;
  const forward = new THREE.Vector3(), to = new THREE.Vector3();
  let renderer, stick, room, faced = null, dirty = true, last = performance.now();
  let frameStats = { calls: 0, triangles: 0 };
  let done = ROOMS.map(() => null);
  // After the four hand-made rooms come rooms drawn by the mind file's own room maker, without end.
  const drawn = new Map();
  function roomDefinition(index) {
    if (index < ROOMS.length) return ROOMS[index];
    if (!drawn.has(index)) drawn.set(index, { words: false, things: mind.randomRoom(lantern.roomChance).things });
    return drawn.get(index);
  }
  // The lantern: one learner for the whole visit. Its own chance (the same seed as the first playing learner in
  // learn.mjs) and the stream its random rooms come from. Its flips are counted apart from the person's.
  const lantern = {
    awake: false, L: mind.newLearner(), chance: rng(7000), roomChance: rng(1000),
    rooms: 0, doorFlips: 0, playFlips: 0, phase: 'asleep', seeing: null, it: null, queue: [],
    pos: new THREE.Vector3(), tried: [], lastOpen: null, looksHere: 0,
    readingAt: -1, reading: null, woke: 0, view: null,
  };
  const ui = makeReadingUI({
    use: (id) => useSwitch(id),
    wake: wakeLantern,
    requestWords(id) {
      if (room.asked.has(id)) return;
      room.asked.add(id);
      room.asks++;
    },
    next: () => enter(room.index + 1),
    restart() {
      done = ROOMS.map(() => null);
      enter(0);
    },
    pauseInput,
  });

  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: tier !== 'mobile-lite', powerPreference: 'high-performance' });
    renderer.setPixelRatio(sharp);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
  } catch {
    ui.fail('The 3D room needs WebGL 2. Try opening this page in a newer browser.');
    return;
  }
  const beliefs = makeBeliefCard({ wake: wakeLantern, live: liveMore, learner: () => lantern.L });

  function enter(index) {
    pauseInput();
    ui.closeBook();
    if (room) {
      room.wires.dispose();
      room.world.dispose();
      // A phone holds on to a painted canvas's memory until the canvas is emptied. The room being left is never
      // read or drawn again, so its paint is handed back before the next room is painted.
      for (const surface of room.surfaces) surface.width = surface.height = 0;
    }
    const began = performance.now();
    const { things: plan, words } = roomDefinition(index);
    const made = makeRoomPaint(plan, tier === 'mobile-lite');
    const read = readRoomPaint(made.surfaces);
    const rules = read.things.filter((thing) => thing.rule);
    const definition = { words, things: rules.map((thing) => thing.rule) };
    const machine = buildRoom(definition.things);
    const world = buildScene({ things: read.things, scene, tier });
    const madeMs = Math.round(performance.now() - began);            // paint it, read it back, build what was read
    const skinById = new Map(read.things.filter((thing) => thing.id).map((thing) => [thing.id, thing]));
    const links = [], incoming = new Map(), branches = new Map();
    const stand = [...definition.things, skinById.get('shelf')];
    for (const thing of definition.things) {
      const inputs = (thing.wires ?? []).map(([source, weight], input) => {
        const branch = branches.get(source) ?? 0;
        branches.set(source, branch + 1);
        const link = {
          source, target: thing, weight, input, branch, row: links.length,
          sp: machine.at[source], dp: machine.at[thing.id],
          live: machine.E.out[machine.at[source]], signals: [], repaint: true,
        };
        links.push(link);
        return link;
      });
      incoming.set(thing.id, inputs);
    }
    for (const link of links) {
      link.branches = branches.get(link.source);
      link.total = links.length;
    }
    scene.updateMatrixWorld(true);
    const wires = makeWires(links, world, scene);
    const open = openSettings(definition.things);
    const hitObjects = [], hitThings = new Map();
    for (const thing of stand) {
      for (const target of world.objects.get(thing.id).hit) {
        hitObjects.push(target);
        hitThings.set(target, thing);
      }
    }
    for (const target of world.lanternView.hits) {                 // a tap on the sleeping lantern or its stand wakes it
      hitObjects.push(target);
      hitThings.set(target, world.lanternView.thing);
    }
    room = {
      index, definition, machine, world, stand, links, incoming, wires, open, hitObjects, hitThings, skinById,
      skins: read.skins, skinTexts: read.things.map((thing) => thing.text), surfaces: made.surfaces, madeMs,
      chron: new Chronicle(), shown: machine.E.out.slice(), waves: [], asked: new Set(),
      best: fewestFlips(open), blind: blindAverage(open, machine.switches.length),
      flips: 0, asks: 0, through: false, started: performance.now(),
      doorMove: { from: 0, to: 0, at: 0 }, doorProgress: 0, visual: '',
      lanternHere: lantern.awake,
    };
    room.facesOk = codeText(readFaces(definition.things, marksFor)) === codeText(plan) &&
      made.written.every((text, i) => room.skinTexts[i] === text);
    Object.assign(player, world.start, { yaw: 0, pitch: START_PITCH, vx: 0, vz: 0, stride: 0, bob: 0, sway: 0 });
    faced = null;
    dirty = true;
    paint(performance.now());
    if (lantern.awake) {                                // it came through the door with you, and carries on here
      lantern.pos.set(world.start.x + 0.5, 1.75, world.start.z - 0.3);
      world.lanternView.wake(lantern.woke);
      beginLanternRoom([{ phase: 'arrive', wait: 900 }]);
    } else {
      const { x, y, z } = world.perch;
      lantern.pos.set(x, y + 0.095, z);
    }
  }

  // ---------------------------------------------------------------- the lantern at work
  // The mind file decides every look and every flip (mind.life). This part only carries them out where a person can
  // see them: it glides to a thing and pauses before its skin, goes to a lever and flips it, at a pace you can follow.
  const V = (x, y, z) => new THREE.Vector3(x, y, z);
  function setLevers() {
    let setting = 0;
    room.machine.switches.forEach((thing, b) => { if (room.machine.E.out[room.machine.at[thing.id]]) setting |= 1 << b; });
    return setting;
  }
  function beginLanternRoom(first = []) {
    lantern.queue = [...first];
    lantern.it = mind.life(room.definition, room.machine, lantern.chance, lantern.L, true);
    lantern.tried = [setLevers()];
    lantern.lastOpen = litNow(room.machine.door) ? setLevers() : null;
    lantern.looksHere = 0;
    lantern.seeing = null;
    room.lanternHere = true;
  }
  function wakeLantern() {
    if (lantern.awake || !room || room.through || ui.blocking()) return;
    lantern.awake = true;
    lantern.woke = performance.now();
    const { x, y, z } = room.world.perch;
    lantern.pos.set(x, y + 0.095, z);
    beginLanternRoom([{ phase: 'waking', move: V(x, y + 0.6, z), speed: 0.6 }, { wait: 350 }]);
    room.world.lanternView.wake(lantern.woke);
    faced = null;
    dirty = true;
  }
  function skinSpot(thing) {                            // where it hovers to look at a thing's skin
    const entry = room.world.objects.get(thing.id);
    // A little to one side and a little low, so the skin it reads stays in view for the person watching.
    if (thing.kind === 'door') return V(entry.x + 0.91, 1.32, entry.z + 0.95);
    const side = Math.sign(entry.x);
    return V(entry.x - side * (thing.kind === 'lamp' ? 0.95 : 0.8), 1.3, entry.z + 0.62);
  }
  function leverSpot(thing) {
    const entry = room.world.objects.get(thing.id);
    return V(entry.x + 0.52, 1.08, entry.z + 0.2);
  }
  function queueLook() {
    const things = room.definition.things, levers = things.filter((t) => t.kind === 'switch');
    const lamps = things.filter((t) => t.kind === 'lamp').reverse(), door = things.at(-1);
    const order = [...levers, door, ...lamps];          // down the switch wall, the door, back up the lamp wall
    if (lantern.looksHere === 0) {                      // the first look in a room: it goes to each thing in turn
      for (const thing of order) {
        lantern.queue.push({ phase: 'look', move: skinSpot(thing), seeing: null });
        lantern.queue.push({ phase: 'look', wait: thing.kind === 'switch' ? 380 : 700, seeing: thing.id });
      }
    } else {                                            // after a flip: it rises and looks along both walls again
      const z = clamp(lantern.pos.z, -room.world.depth + 2.4, -2.2);
      lantern.queue.push({ phase: 'look', move: V(0, 1.95, z), seeing: null });
      for (const thing of order) lantern.queue.push({ phase: 'look', wait: 300, seeing: thing.id });
    }
    lantern.queue.push({ seeing: null, call: () => { lantern.looksHere++; } });
  }
  function queueFlip(b, play) {
    const thing = room.machine.switches[b];
    lantern.queue.push({ phase: play ? 'play' : 'go', move: leverSpot(thing), seeing: null, target: thing.id });
    lantern.queue.push({ phase: play ? 'play' : 'flip', wait: 260, target: thing.id });
    lantern.queue.push({ call: () => useSwitch(thing.id, play ? 'play' : 'door') });
    lantern.queue.push({ until: () => room.waves.length === 0, wait: 200 });
  }
  function queueLeave() {
    const door = room.machine.door, open = lantern.lastOpen;
    if (!litNow(door) && open !== null) {               // its play may have shut the door: it sets the levers back, without looking
      room.machine.switches.forEach((thing, b) => {
        lantern.queue.push({ call: () => {
          if (((setLevers() ^ open) >> b) & 1) {
            lantern.queue.unshift({ phase: 'back', move: leverSpot(thing), target: thing.id }, { phase: 'back', wait: 220, target: thing.id },
              { call: () => useSwitch(thing.id, 'back') }, { until: () => room.waves.length === 0, wait: 150 });
          }
        } });
      });
    }
    const { doorway } = room.world;
    lantern.queue.push({ phase: 'leave', move: V(doorway.x, 1.5, doorway.z + 1.3) });
    lantern.queue.push({ phase: 'leave', until: () => room.doorProgress >= 0.93 && litNow(door) });
    lantern.queue.push({ phase: 'leave', move: V(doorway.x, 1.5, doorway.z - 1.35) });
    lantern.queue.push({ phase: 'wait', call: () => {} });
  }
  function lanternPlan() {
    if (!lantern.it) return;
    const step = lantern.it.next();
    if (step.done) { lantern.it = null; queueLeave(); return; }
    const act = step.value;
    if (act.act === 'look') queueLook();
    else if (act.act === 'flip') queueFlip(act.b, act.play);
    else if (act.act === 'opened') { lantern.rooms++; lantern.queue.push({ phase: 'opened', wait: 700 }); }
  }
  function lanternStep(dt, now) {
    if (!lantern.awake || !room || ui.blocking()) return;
    for (let guard = 0; guard < 200; guard++) {
      const task = lantern.queue[0];
      if (!task) {
        if (!lantern.it) break;
        lanternPlan();
        continue;
      }
      if (task.phase) lantern.phase = task.phase;
      if ('seeing' in task) lantern.seeing = task.seeing;
      if ('target' in task) lantern.target = task.target;
      if (task.move) {
        const gap = lantern.pos.distanceTo(task.move);
        const speed = (task.speed ?? 1.9) * Math.min(1, 0.25 + gap / 0.6);
        if (motion.matches || gap <= speed * dt) { lantern.pos.copy(task.move); lantern.queue.shift(); continue; }
        lantern.pos.lerp(task.move, speed * dt / gap);
        break;
      }
      if (task.until && !task.until()) break;
      if (task.wait) {
        task.ends ??= now + task.wait;
        if (now < task.ends) break;
      }
      lantern.queue.shift();
      task.call?.();
    }
    lantern.view = null;
  }
  // The hidden life: the same learner through rooms drawn at random, all at once, with nothing drawn.
  function liveMore(count = 10) {
    if (!lantern.awake) return;
    for (let k = 0; k < count; k++) {
      const went = mind.play(mind.randomRoom(lantern.roomChance), lantern.chance, lantern.L, true);
      lantern.rooms++;
      lantern.doorFlips += went.flips;
      lantern.playFlips += went.playFlips;
    }
    dirty = true;
  }
  function lanternReading() {
    const key = lantern.L.looks;
    if (lantern.readingAt !== key) { lantern.readingAt = key; lantern.reading = mind.reading(lantern.L).all; }
    return lantern.reading;
  }
  function lanternView() {
    return {
      awake: lantern.awake, rooms: lantern.rooms, looks: lantern.L.looks, doorFlips: lantern.doorFlips, playFlips: lantern.playFlips,
      reading: lanternReading(), trusts: mind.trusted(lantern.L), phase: lantern.phase, seeing: lantern.seeing,
      target: lantern.target ?? null, tried: lantern.tried.slice(),
    };
  }

  function litNow(thing) {
    return room.shown[room.machine.at[thing.id]] === 1;
  }

  function marksFor(thing) {
    return marksOf(thing, litNow(thing), (index) => room.incoming.get(thing.id)[index].live);
  }

  function wordsFor(thing) {
    const sum = room.incoming.get(thing.id).reduce((total, link) => total + link.weight * link.live, 0);
    return wordsOf(thing, room.definition.things, litNow(thing), sum);
  }

  // by: 'person', or the lantern ('door' while it opens the door, 'play' after, 'back' when it sets the levers back
  // so the door stands open again). Only the person's flips count as the person's.
  function useSwitch(id, by = 'person') {
    if (room.through || ui.blocking()) return;
    const { machine } = room;
    const part = machine.at[id];
    if (!machine.W.isInput[part]) return;
    const before = machine.E.out.slice();
    const value = before[part] ? 0 : 1;
    const start = performance.now();
    const pace = motion.matches ? 0 : WAVE;
    machine.E.set(part, value);
    room.chron.add(part, value);
    if (by === 'person') room.flips++;
    else if (by === 'door') { lantern.doorFlips++; lantern.tried.push(setLevers()); }
    else if (by === 'play') lantern.playFlips++;
    if (machine.E.out[machine.at[machine.door.id]]) lantern.lastOpen = setLevers();
    for (let q = 0; q < before.length; q++) {
      if (before[q] === machine.E.out[q]) continue;
      const at = start + machine.W.level[q] * pace;
      room.waves.push({ q, value: machine.E.out[q], at });
      for (const link of room.links) {
        if (link.sp === q) link.signals.push({ start: at, arrive: start + machine.W.level[link.dp] * pace, to: machine.E.out[q] });
      }
    }
    room.waves.sort((a, b) => a.at - b.at);
    runWaves(start);
    if (motion.matches) paint(start);
  }

  function runWaves(now) {
    while (room.waves.length && (motion.matches || room.waves[0].at <= now)) {
      const { q, value, at } = room.waves.shift();
      room.shown[q] = value;
      if (q === room.machine.at[room.machine.door.id]) room.doorMove = { from: room.doorProgress, to: value, at };
    }
    for (const link of room.links) {
      while (link.signals.length && (motion.matches || link.signals[0].arrive <= now)) {
        link.live = link.signals.shift().to;
        link.repaint = true;
      }
    }
  }

  function paint(now) {
    const visual = room.shown.join('');
    if (visual !== room.visual) {
      room.visual = visual;
      for (const thing of room.definition.things) {
        room.world.updateThing(thing, litNow(thing));
      }
      dirty = true;
    }
    const { from, to: destination, at } = room.doorMove;
    const completion = motion.matches ? 1 : clamp((now - at) / 450, 0, 1);
    const eased = completion * completion * (3 - 2 * completion);
    const progress = from + (destination - from) * eased;
    if (progress !== room.doorProgress) {
      room.doorProgress = progress;
      room.world.updateDoor(progress);
      dirty = true;
    }
    if (room.wires.refresh(now)) dirty = true;
  }

  function pauseInput() {
    keys.clear();
    stick?.reset();
  }

  function useFacing() {
    if (faced?.kind === 'switch') useSwitch(faced.id);
    if (faced?.kind === 'shelf') ui.openBook(1);
    if (faced?.kind === 'lantern') wakeLantern();
  }

  function useAt(x, y) {
    if (!room || ui.blocking() || room.through) return;
    const bounds = canvas.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2(2 * (x - bounds.left) / bounds.width - 1, 1 - 2 * (y - bounds.top) / bounds.height), camera);
    let thing, book;
    for (const hit of ray.intersectObjects(room.hitObjects, true)) {
      let object = hit.object;
      thing = undefined;
      book = undefined;
      while (object && !thing) {
        book ??= object.userData.book;
        thing = room.hitThings.get(object);
        object = object.parent;
      }
      if (thing?.kind === 'lantern' && lantern.awake) continue;   // awake, it is a light passing by: a tap goes to what is behind it
      break;
    }
    if (thing?.kind === 'switch') useSwitch(thing.id);
    if (thing?.kind === 'shelf' && Number.isInteger(book)) ui.openBook(book + 1);
    if (thing?.kind === 'lantern') wakeLantern();
  }

  function resize() {
    const { clientWidth: width, clientHeight: height } = canvas;
    camera.aspect = width / Math.max(1, height);
    camera.fov = camera.aspect < 0.68 ? 84 : 68;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height, false);
    dirty = true;
  }

  function fits(x, z) {
    const { bounds, doorway, obstacles } = room.world;
    if (x < bounds.left + RADIUS || x > bounds.right - RADIUS || z > bounds.near - RADIUS) return false;
    if (z < doorway.z + RADIUS) {
      const inOpening = Math.abs(x - doorway.x) <= doorway.width / 2 - RADIUS;
      const passable = room.doorProgress >= 0.93 && litNow(room.machine.door);
      if (!inOpening || (!passable && player.z >= doorway.z + RADIUS) || z < doorway.z - 1.9) return false;
    }
    return !obstacles.some((box) => {
      const dx = x - clamp(x, box.minX, box.maxX);
      const dz = z - clamp(z, box.minZ, box.maxZ);
      return dx * dx + dz * dz < RADIUS * RADIUS;
    });
  }

  function finishRoom(now) {
    room.through = true;
    if (room.lanternHere) {                             // the lantern worked this room, so it is not the person's result
      pauseInput();
      enter(room.index + 1);
      return;
    }
    done[room.index] = {
      flips: room.flips, best: room.best, blind: room.blind, asks: room.asks,
      words: room.definition.words, secs: Math.round((now - room.started) / 1000),
    };
    pauseInput();
  }

  function walk(dt, now) {
    if (ui.blocking() || room.through) { player.vx = player.vz = 0; return; }
    const turning = Number(keys.has('ArrowRight')) - Number(keys.has('ArrowLeft'));
    if (turning) {
      player.yaw = angle(player.yaw + turning * 1.85 * dt);
      dirty = true;
      triedIt('look');
    }
    const lateral = Number(keys.has('KeyD')) - Number(keys.has('KeyA')) + stick.x;
    const advance = Number(keys.has('KeyW') || keys.has('ArrowUp')) - Number(keys.has('KeyS') || keys.has('ArrowDown')) + stick.y;
    const speed = stick.running || keys.has('ShiftLeft') || keys.has('ShiftRight') ? 3.8 : 2.75;
    const push = Math.max(1, Math.hypot(lateral, advance));
    const sin = Math.sin(player.yaw), cos = Math.cos(player.yaw);
    const wantX = (advance * sin + lateral * cos) * speed / push;
    const wantZ = (-advance * cos + lateral * sin) * speed / push;
    // A body has weight: it takes a moment to get going. Letting go stops you at once, so you can line up with a thing.
    // With reduced motion it simply follows the thumb.
    if (!lateral && !advance) player.vx = player.vz = 0;
    else {
      const ease = motion.matches ? 1 : 1 - Math.exp(-dt / 0.055);
      player.vx += (wantX - player.vx) * ease;
      player.vz += (wantZ - player.vz) * ease;
    }
    const dx = player.vx * dt, dz = player.vz * dt;
    if (dx || dz) {
      const fromX = player.x, fromZ = player.z;
      const steps = Math.max(1, Math.ceil(Math.hypot(dx, dz) / 0.07));
      for (let i = 0; i < steps; i++) {
        const x = player.x + dx / steps, z = player.z + dz / steps;
        if (fits(x, player.z)) player.x = x; else player.vx = 0;
        if (fits(player.x, z)) player.z = z; else player.vz = 0;
      }
      const went = Math.hypot(player.x - fromX, player.z - fromZ);
      if (went > 0) { player.stride += went; dirty = true; triedIt('walk'); }
    }
    // A small rise and fall with each step. It settles gently when you stop, so the view never jumps.
    const pace = Math.min(1, Math.hypot(player.vx, player.vz) / 2.75);
    player.sway += (pace - player.sway) * (1 - Math.exp(-dt / 0.11));
    if (player.sway < 0.004) player.sway = 0;
    const bob = motion.matches ? 0 : Math.sin(player.stride * Math.PI * 2 / 1.45) * 0.016 * player.sway;
    if (bob !== player.bob) { player.bob = bob; dirty = true; }
    if (player.z < room.world.doorway.z - 0.56) finishRoom(now);
  }

  function lookForThing() {
    if (room.through || ui.blocking()) return;
    camera.getWorldDirection(forward);
    let best = null, score = 0.906;
    const lanternView = room.world.lanternView;
    for (const thing of lantern.awake ? room.stand : [...room.stand, lanternView.thing]) {
      const entry = thing.kind === 'lantern' ? lanternView : room.world.objects.get(thing.id);
      const sights = entry.aims ?? [entry.aim];
      for (const sight of sights) {
        to.subVectors(sight, camera.position);
        const distance = to.length();
        if (distance > 3.5 || distance === 0) continue;
        const alignment = to.dot(forward) / distance - distance * 0.002;
        if (alignment > score) {
          score = alignment;
          best = thing;
        }
      }
    }
    faced = best;
  }

  function frame(now) {
    const dt = clamp((now - last) / 1000, 0, 0.1);
    last = now;
    runWaves(now);
    walk(dt, now);
    lanternStep(dt, now);
    paint(now);
    if (room.world.lanternView.update(now, lantern, motion.matches)) dirty = true;     // a lantern in motion counts as something changing
    beliefs.update(lanternView, room, motion.matches);
    camera.position.set(player.x, EYE + player.bob, player.z);
    camera.rotation.set(player.pitch, -player.yaw, 0);
    camera.updateMatrixWorld();
    lookForThing();
    ui.update({
      index: room.index, things: room.definition.things, faced, words: room.definition.words,
      asked: room.asked, flips: room.flips, through: room.through, done, marksFor, wordsFor,
      chron: room.chron, engine: room.machine.E, skinTexts: room.skinTexts, skinById: room.skinById,
      doorOpen: room.doorProgress >= 0.93 && litNow(room.machine.door),
    });
    if (dirty) {
      renderer.render(scene, camera);
      frameStats = { calls: renderer.info.render.calls, triangles: renderer.info.render.triangles };
      dirty = false;
      // Slow frames for a while: trade a little sharpness for smoothness. It only ever steps down.
      slow = dt > 0.03 ? slow + 1 : Math.max(0, slow - 2);
      if (slow > 45 && sharp > 1.15) { sharp = Math.max(1.15, sharp - 0.35); renderer.setPixelRatio(sharp); slow = 0; resize(); }
    }
    requestAnimationFrame(frame);
  }

  stick = createThumbstick(canvas, {
    enabled: () => room && !room.through && !ui.blocking(),
    onLook(dx, dy, kind) {
      const sensitivity = kind === 'mouse' ? 0.0045 : 0.006;
      player.yaw = angle(player.yaw + dx * sensitivity);
      player.pitch = clamp(player.pitch - dy * sensitivity, -1.23, 1.23);
      dirty = true;
      triedIt('look');
    },
    onTap: useAt,
  });
  addEventListener('keydown', (event) => {
    if (!room || room.through || ui.blocking() || event.ctrlKey || event.metaKey || event.altKey) return;
    if (MOVEMENT.has(event.code)) {
      keys.add(event.code);
      event.preventDefault();
    } else if (!event.repeat && (event.code === 'KeyE' || (event.code === 'Enter' && !event.target.closest?.('button, a, input, textarea, select')))) {
      useFacing();
      event.preventDefault();
    }
  });
  addEventListener('keyup', (event) => keys.delete(event.code));
  addEventListener('blur', pauseInput);
  document.addEventListener('visibilitychange', () => { if (document.hidden) pauseInput(); });
  addEventListener('resize', resize);
  canvas.addEventListener('webglcontextlost', (event) => {
    event.preventDefault();
    ui.fail('The 3D view paused. Reload the page to walk again.');
    pauseInput();
  });

  enter(0);
  resize();
  frame(performance.now());
  ui.ready();
  const vector = (p) => ({ x: p.x, y: p.y, z: p.z });
  const values = (data) => Object.fromEntries(room.definition.things.map((thing) => [thing.id, data[room.machine.at[thing.id]]]));
  window.rr = Object.freeze({
    state: () => ({
      room: room.index + 1, x: player.x, z: player.z, yaw: player.yaw, pitch: player.pitch,
      facing: faced?.id ?? null, through: room.through,
      settled: room.waves.length === 0 && room.links.every((link) => !link.signals.length),
      on: values(room.machine.E.out), shown: values(room.shown),
      open: room.open.slice(), best: room.best, blind: room.blind, flips: room.flips, asks: room.asks,
      history: room.chron.n, facesOk: room.facesOk, skins: { ...room.skins }, words: room.definition.words,
      done: done.map((result) => result && { ...result }),
      wireMotion: room.links.filter((link) => link.signals.some((pulse) => pulse.start <= performance.now())).length,
      doorProgress: room.doorProgress,
      render: { ...frameStats, tier, paint: tier === 'mobile-lite' ? 'small' : 'full', madeMs: room.madeMs,
        pixelRatio: renderer.getPixelRatio(), decorated: room.world.decorated },
      lantern: { ...lanternView(), x: lantern.pos.x, y: lantern.pos.y, z: lantern.pos.z },
    }),
    pos: () => ({
      ...Object.fromEntries([...room.world.objects].map(([id, entry]) => [id, {
        x: entry.x, z: entry.z, aimY: entry.aim.y,
        ...(entry.leverKnob ? { lever: vector(entry.leverKnob.getWorldPosition(new THREE.Vector3())) } : {}),
        ...(id === 'shelf' ? { books: entry.hit.map((volume) => vector(volume.getWorldPosition(new THREE.Vector3()))) } : {}),
      }])),
      doorway: { ...room.world.doorway },
      start: { ...room.world.start },
      lantern: { x: room.world.perch.x, z: room.world.perch.z, aimY: room.world.lanternView.aim.y },
    }),
  });
}

// The chip under the top bar and the card it opens: what the lantern believes, worked out from its real numbers.
// Every sentence is a template; the numbers and choices in it come from the learner's own weights and scores.
const MARKS = [
  ['square', 'Each square'], ['solid-filled', 'A filled solid circle'], ['dashed-filled', 'A filled dashed circle'],
  ['solid-empty', 'An empty solid circle'], ['dashed-empty', 'An empty dashed circle'],
];
const FILLS = {
  named: 'the thing whose sign is under it', host: 'the thing wearing it', before: 'the thing standing just before it',
  place: 'the thing standing in the same place along the wall', never: 'nothing: circles are never filled',
};
const PHASES = {
  asleep: () => 'Asleep on its stand.', waking: () => 'Waking up.', arrive: () => 'Coming into this room with you.',
  look: (v, name) => (v.seeing ? `Looking at ${name(v.seeing)}.` : 'Going to look.'),
  go: (v, name) => `Going to ${name(v.target)}.`, flip: (v, name) => `Flipping ${name(v.target)}.`,
  play: (v, name) => `The door is open. Flipping ${name(v.target)}, just to see what happens.`,
  opened: () => 'The door is open. Now it stays and plays a little, to learn more.',
  back: (v, name) => `Setting ${name(v.target)} back, so the door stands open.`,
  leave: () => 'Going through the door.', wait: () => 'Waiting for you beyond the door. Walk through and it comes too.',
};
function markIcon(kind) {
  if (kind === 'square') return '<svg class="mark" viewBox="0 0 20 20" aria-hidden="true"><rect x="3" y="3" width="14" height="14" rx="2" fill="#624421" stroke="#624421" stroke-width="2"/></svg>';
  const dashed = kind.startsWith('dashed'), filled = kind.endsWith('filled');
  return `<svg class="mark" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7" fill="${filled ? (dashed ? '#8a5cac' : '#d99232') : 'none'}" ` +
    `stroke="${dashed ? '#653e82' : '#8a4c16'}" stroke-width="2.4"${dashed ? ' stroke-dasharray="3.6 2.6"' : ''}/></svg>`;
}
function makeBeliefCard({ wake, live, learner }) {
  const chip = document.getElementById('mind-chip'), card = document.getElementById('mind');
  let open = false, key = '', view = null;
  card.innerHTML = '<div class="mind-head"><h2 id="mind-title">The lantern</h2><button type="button" class="quiet close" id="mind-close">Close</button></div>' +
    '<p class="now" id="mind-now"></p><div id="mind-top"></div>' +
    '<div class="buttons"><button type="button" id="mind-wake">Wake it</button><button type="button" id="mind-live">Let it live 10 more rooms</button></div>' +
    '<div id="mind-more"></div>' +
    '<p class="note eyes">Its eyes are simple. It gets the rule as marks. It can see how many squares there are and which circles are filled. It is never told what they mean.</p>';
  const byId = (id) => document.getElementById(id);
  function toggle(to = !open) {
    open = to;
    card.hidden = !open;
    chip.setAttribute('aria-expanded', String(open));
    key = '';
  }
  chip.addEventListener('click', () => toggle());
  byId('mind-close').addEventListener('click', () => toggle(false));
  byId('mind-wake').addEventListener('click', wake);
  byId('mind-live').addEventListener('click', () => { live(10); key = ''; });
  return {
    update(read, room) {
      view = read();
      const pct = Math.round(100 * view.reading);
      const chipText = view.awake ? `Lantern · reads ${pct}%` : 'Lantern · asleep';
      if (chip.dataset.text !== chipText) { chip.dataset.text = chipText; chip.querySelector('span').textContent = chipText; }
      chip.classList.toggle('awake', view.awake);
      if (!open) return;
      const name = (id) => nameOf(room.definition.things.find((thing) => thing.id === id) ?? { kind: 'lantern' });
      const next = `${view.awake}|${view.rooms}|${view.looks}|${view.doorFlips}|${view.playFlips}|${view.phase}|${view.seeing}|${view.target}`;
      if (next === key) return;
      key = next;
      byId('mind-now').textContent = `Now: ${(PHASES[view.phase] ?? PHASES.asleep)(view, name)}`;
      byId('mind-wake').hidden = view.awake;
      byId('mind-live').hidden = !view.awake;
      const [top, more] = beliefHtml(view);
      byId('mind-top').innerHTML = top;
      byId('mind-more').innerHTML = more;
    },
    get open() { return open; },
  };
  function beliefHtml(v) {
    const L = learner();
    const intro = v.awake ? '' : '<p>A new mind. It knows nothing about the marks yet. Wake it and watch it look, flip and learn, room after room.</p>';
    const plural = (n, one, many) => `<b>${n}</b> ${n === 1 ? one : many}`;
    const facts = `<p class="facts">${plural(v.rooms, 'room', 'rooms')} lived through · ${plural(v.looks, 'look', 'looks')} · ` +
      `${plural(v.doorFlips, 'door flip', 'door flips')} · ${plural(v.playFlips, 'play flip', 'play flips')}</p>`;
    const reading = `<p class="reading">It reads rooms it has never seen <b>${Math.round(100 * v.reading)}%</b> right.</p>` +
      '<p class="note">The test: 10 rooms it never plays, 4 ways the levers can stand in each. From the marks alone, it says which things glow.</p>';
    if (!L.looks) return [intro + facts + reading, '<p class="note">It has not looked at anything yet, so it has no beliefs about the marks.</p>'];
    const strength = (w) => (Math.abs(w) % 1 ? Math.abs(w).toFixed(1) : String(Math.abs(w)));
    const marks = MARKS.map(([kind, label], i) => {
      const w = L.w[i];
      const means = w > 0 ? `counts for glowing (${strength(w)})` : w < 0 ? `counts against (${strength(w)})` : 'it gives these no weight';
      return `<li>${markIcon(kind)}<span>${label}: ${means}.</span></li>`;
    }).join('');
    const lean = L.w[5] > 0 ? `glowing (${strength(L.w[5])})` : L.w[5] < 0 ? `dark (${strength(L.w[5])})` : 'neither way';
    const ranked = mind.GUESSES.slice().reverse().sort((a, b) => L.score[b] - L.score[a]);
    const best = mind.trusted(L), second = ranked.find((g) => g !== best);
    const fills = L.circles
      ? `<p>It thinks a circle is filled by <b>${FILLS[best]}</b>: right ${L.score[best]} of ${L.circles} times.</p>` +
        `<p class="note">Next best: ${FILLS[second]} (right ${L.score[second]} of ${L.circles}).</p>`
      : '<p>It has not looked at a circle yet.</p>';
    return [intro + facts + reading, `<h3>What each mark means to it</h3><ul class="marks">${marks}</ul>` +
      `<p class="note">Before it counts any marks, it leans ${lean}. The numbers are how strongly.</p><h3>What fills a circle</h3>${fills}`];
  }
}

// The card translates the rule into marks; the room itself wears the window code.
function faceLayout(m) {
  const toggle = m.kind === 'switch';
  return {
    width: toggle ? 96 : 40 + Math.max(m.squares.length * 20, m.wires.length * 28),
    height: toggle ? 44 : 68,
    wireX: (k) => 48 + k * 28,
    wireY: 38,
  };
}

function rrEscape(value) {
  return String(value).replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch]);
}

function faceSvg(m, label = '') {
  const aria = label ? ` role="img" aria-label="${rrEscape(label)}"` : ' aria-hidden="true"';
  const { width, height, wireX, wireY } = faceLayout(m);
  const sign = rrEscape(m.sign);
  if (m.kind === 'switch') {
    return `<svg class="face toggle" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"${aria}><text class="sign" x="2" y="30">${sign}</text>` +
      `<line class="track${m.lit ? ' on' : ''}" x1="48" y1="22" x2="74" y2="22" stroke="currentColor" stroke-width="22" stroke-linecap="round"/><ellipse class="knob" cx="${m.lit ? 74 : 48}" cy="22" rx="8" ry="8"/></svg>`;
  }
  let svg = `<svg class="face" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"${aria}><text class="sign" x="${m.kind === 'door' ? 7 : 2}" y="33">${sign}</text>`;
  if (m.kind === 'door') svg += '<path class="arch" d="M3 42 V16 a12 12 0 0 1 24 0 V42" fill="none" stroke="currentColor" stroke-width="2"/>';
  m.squares.forEach((on, i) => {
    svg += `<rect class="sq" x="${39 + i * 20}" y="4" width="15" height="15" rx="2" fill="${on ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2"/>`;
  });
  m.wires.forEach((wire, i) => {
    const x = wireX(i);
    svg += `<circle class="wire${wire.dark ? ' dark' : ''}" cx="${x}" cy="${wireY}" r="9.5" fill="${wire.live ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2.5"${wire.dark ? ' stroke-dasharray="4 3"' : ''}/>` +
      `<text class="from" x="${x}" y="64" text-anchor="middle">${rrEscape(wire.from)}</text>`;
  });
  return svg + '</svg>';
}

function readFace(svg) {
  const signs = [...svg.querySelectorAll('text')].map((node) => node.textContent);
  const knob = svg.querySelector('ellipse');
  if (knob) return { sign: signs[0], kind: 'switch', lit: Number(knob.getAttribute('cx')) > 60 };
  return {
    sign: signs[0],
    kind: svg.querySelector('path') ? 'door' : 'lamp',
    squares: [...svg.querySelectorAll('rect')].map((node) => node.getAttribute('fill') !== 'none'),
    wires: [...svg.querySelectorAll('circle')].map((node, i) => ({
      from: signs[i + 1],
      dark: node.hasAttribute('stroke-dasharray'),
      live: node.getAttribute('fill') !== 'none',
    })),
  };
}

function readFaces(things, marksFor) {
  const drawn = document.createElement('template');
  return things.map((thing) => {
    drawn.innerHTML = faceSvg(marksFor(thing));
    return thingFromMarks(readFace(drawn.content.firstElementChild));
  });
}

function rrGlyphLabel(marks) {
  if (marks.kind === 'switch') return `${marks.sign}, toggle ${marks.lit ? 'on' : 'off'}`;
  const rings = marks.wires.map((wire) => `${wire.from}, ${wire.live ? 'filled' : 'empty'} ${wire.dark ? 'dashed' : 'solid'} ring`);
  return [marks.sign, count(marks.squares.length, 'square'), ...rings].join(', ');
}

const RR_BOOK_NAMES = ['How to read the marks', "This room's history", 'What the world read off its things'];

function makeReadingUI({ use, wake, requestWords, next, restart, pauseInput }) {
  const byId = (id) => document.getElementById(id);
  const where = byId('where');
  const flips = byId('flips');
  const roomCard = byId('card');
  const bookPanel = byId('book');
  const results = byId('results');
  const status = byId('status');
  const reticle = document.querySelector('.reticle');
  let view;
  let book;
  let cardKey;
  let marksKey;
  let resultIndex = -1;

  function ready() {
    status.hidden = true;
  }

  function fail(message) {
    status.textContent = message;
    status.hidden = false;
    reticle.hidden = true;
  }

  function showCard(faced, showWords) {
    roomCard.toggleAttribute('data-visible', Boolean(faced));
    roomCard.inert = !faced;
    roomCard.setAttribute('aria-hidden', String(!faced));
    reticle.classList.toggle('on', Boolean(faced));
    if (!faced) return;
    const quote = `<p class="skin-quote"><q id="skin-text">${rrEscape(view.skinById.get(faced.id).text)}</q></p>`;
    if (faced.kind === 'shelf') {
      const books = RR_BOOK_NAMES.map((name, i) => `<button type="button" class="quiet" id="b${i + 1}"><span class="roman" aria-hidden="true">${['I', 'II', 'III'][i]}</span>${name}</button>`).join('');
      roomCard.innerHTML = `<div class="card-content">${quote}<h2>The bookshelf</h2><div class="buttons book-list">${books}</div></div>`;
      RR_BOOK_NAMES.forEach((_, i) => byId(`b${i + 1}`).addEventListener('click', () => openBook(i + 1)));
      return;
    }
    if (faced.kind === 'lantern') {
      roomCard.innerHTML = `<div class="card-content">${quote}<h2>A lantern</h2><p>A new mind. It knows nothing about the marks yet. ` +
        'Wake it and it will look, flip and learn, room after room.</p><div class="buttons"><button type="button" id="wake">Wake it</button></div></div>';
      byId('wake').addEventListener('click', wake);
      return;
    }
    roomCard.innerHTML = `<div class="card-content">${quote}<div class="card-head"><h2>${rrEscape(nameOf(faced))}</h2><div id="face"></div></div>` +
      `<p id="words"${showWords ? '' : ' hidden'}></p><p id="hint" class="good" hidden>The door is open. Walk through it.</p>` +
      `<div class="buttons">${faced.kind === 'switch' ? '<button type="button" id="use">Flip it</button>' : ''}` +
      `${showWords ? '' : '<button type="button" class="quiet" id="ask">Read it to me</button>'}</div></div>`;
    byId('use')?.addEventListener('click', () => use(faced.id));
    byId('ask')?.addEventListener('click', () => requestWords(faced.id));
  }

  function update(nextView) {
    const previous = view;
    view = nextView;
    if (previous?.index !== view.index) {
      where.textContent = view.index < ROOMS.length ? `Room ${view.index + 1} of ${ROOMS.length}` : `Room ${view.index + 1}`;
      closeBook();
      results.close();
      resultIndex = -1;
    }
    if (previous?.flips !== view.flips) flips.textContent = count(view.flips, 'flip');
    const faced = view.through ? null : view.faced;
    const showWords = view.words || view.asked.has(faced?.id);
    const key = `${view.index}|${faced?.id}|${showWords}`;
    if (cardKey !== key) {
      cardKey = key;
      marksKey = '';
      showCard(faced, showWords);
    }
    if (faced && faced.kind !== 'shelf' && faced.kind !== 'lantern') {
      const marks = view.marksFor(faced);
      const signature = `${marks.lit}|${marks.wires?.map((wire) => wire.live ? 1 : 0).join('')}`;
      if (marksKey !== signature) {
        marksKey = signature;
        byId('face').innerHTML = faceSvg(marks, rrGlyphLabel(marks));
        if (showWords) byId('words').textContent = view.wordsFor(faced);
      }
      byId('hint').hidden = !(faced.kind === 'door' && view.doorOpen);
    }
    if (view.through && resultIndex !== view.index && view.done[view.index]) showResults();
  }

  function openBook(number) {
    if (!view || blocking() || !RR_BOOK_NAMES[number - 1]) return;
    book = { number, page: 0 };
    renderBook();
    pauseInput();
    bookPanel.showModal();
  }

  function closeBook() {
    book = null;
    if (bookPanel.open) bookPanel.close();
  }

  bookPanel.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeBook();
  });

  function bookPages() {
    const { things, marksFor, wordsFor, chron } = view;
    const door = things.at(-1);
    const lamp = things.find((thing) => thing.kind === 'lamp');
    if (book.number === 1) {
      const darkOne = things.find((thing) => thing.wires?.some(([, weight]) => weight < 0));
      return [
        `<p>Each thing wears its code in windows. Its card shows the same rule as marks.</p>${faceSvg(marksFor(lamp))}<p>The squares on top say how much a thing needs. Count them. ${rrEscape(nameOf(lamp))} needs ${lamp.mark}.</p>`,
        `<p>Each circle is one wire coming in. The mark under it says where the wire comes from: a number is a switch, a letter is a lamp.</p>${faceSvg(marksFor(darkOne || door))}<p>A solid ring is a bright wire. It adds one while it carries light. A dashed ring is a dark wire. It takes one away while it carries light.${darkOne ? '' : ' This room has no dark wires yet.'}</p>`,
        `<p>A filled circle is carrying light right now. Add up the filled bright circles and take away the filled dark ones. When that reaches the number of squares, the thing lights. A door opens.</p>${faceSvg(marksFor(door))}<p class="note">${rrEscape(wordsFor(door))}</p><p>The wires on the floor are the same wires. Follow one to see where a switch sends its light.</p>`,
      ];
    }
    if (book.number === 2) {
      const again = buildRoom(things);
      const lines = [];
      chron.replay((part, value) => {
        again.E.set(part, value);
        const id = again.ids[part];
        const changed = things.find((thing) => thing.id === id);
        const states = things.filter((thing) => thing.wires).map((thing) => {
          const on = again.E.out[again.at[thing.id]];
          if (thing.kind === 'door') return `the door ${on ? 'open' : 'shut'}`;
          return `${nameOf(thing)} ${on ? 'lit' : 'dark'}`;
        });
        lines.push(`${lines.length + 1}. ${nameOf(changed)} turned ${value ? 'on' : 'off'}. Then: ${states.join(', ')}.`);
      });
      const pages = [];
      for (let i = 0; i < lines.length; i += 6) pages.push(`<pre>${rrEscape(lines.slice(i, i + 6).join('\n'))}</pre>`);
      if (!pages.length) pages.push('<p class="note">Nothing has happened yet. Flip a switch, then open this book again.</p>');
      pages[0] = '<p>It writes itself as you play. Nothing in it is ever rubbed out.</p>' + pages[0];
      const check = (chron.chain >>> 0).toString(16).padStart(8, '0');
      pages.push(`<p>Check number: ${check}. Change anything in the past and this number changes.</p>`);
      return pages;
    }
    return [
      `<p>Each line came from the windows on a thing in this room.</p><pre id="code">${rrEscape(view.skinTexts.join('\n'))}</pre><div class="buttons"><button type="button" id="rebuild">Build the room again from this page</button></div><p id="same" aria-live="polite"></p>`,
      `<p>The numbers after “at” say where each thing stands. “Needs” is the number of squares. + is a bright wire and − is a dark wire.</p>${faceSvg(marksFor(lamp))}`,
    ];
  }

  function checkRebuild() {
    const message = byId('same');
    try {
      const lines = byId('code').textContent.split('\n');
      const read = lines.map(parseSkin);
      if (read.some((thing) => !thing)) throw new Error('A line could not be read.');
      const again = buildRoom(read.filter((thing) => thing.rule).map((thing) => thing.rule));
      view.chron.replay((part, value) => again.E.set(part, value));
      const out = view.engine.out;
      const same = lines.length === view.skinTexts.length && lines.every((line, i) => line === view.skinTexts[i]) &&
        again.E.out.length === out.length && again.E.out.every((value, i) => value === out[i]) && stateMark(again.E.out) === stateMark(out);
      if (same) {
        message.innerHTML = `<span class="good">Same room.</span> Built again from this page and ${count(view.chron.n, 'change')} of history. Every part matches.`;
        return;
      }
      message.textContent = 'It came out different. That is a bug.';
    } catch (error) {
      message.textContent = `It came out different. That is a bug. ${error.message}`;
    }
  }

  function renderBook() {
    const pages = bookPages();
    const binding = view.skinById.get(`book-${book.number}`);
    bookPanel.innerHTML = `<h2 id="book-title">${RR_BOOK_NAMES[book.number - 1]}</h2><p class="skin-quote"><q>${rrEscape(binding.text)}</q></p>${pages[book.page]}` +
      `<div class="buttons"><button type="button" class="quiet" id="prev"${book.page ? '' : ' disabled'}>Back a page</button>` +
      `<button type="button" class="quiet" id="nextp"${book.page < pages.length - 1 ? '' : ' disabled'}>Next page</button>` +
      `<button type="button" class="quiet" id="shut">Close the book</button></div><p class="note page-number" id="pageno">Page ${book.page + 1} of ${pages.length}</p>`;
    bookPanel.scrollTop = 0;
    const turn = (by, button) => {
      book.page += by;
      renderBook();
      const target = byId(button);
      (target.disabled ? byId(by < 0 ? 'nextp' : 'prev') : target).focus({ preventScroll: true });
    };
    byId('prev').addEventListener('click', () => turn(-1, 'prev'));
    byId('nextp').addEventListener('click', () => turn(1, 'nextp'));
    byId('shut').addEventListener('click', closeBook);
    byId('rebuild')?.addEventListener('click', checkRebuild);
  }

  function showResults() {
    closeBook();
    const { index, done } = view;
    resultIndex = index;
    const row = done[index];
    const last = index === ROOMS.length - 1;
    const asks = row.words ? '' : ` You asked for the words ${count(row.asks, 'time')}.`;
    results.innerHTML = `<h2 id="results-title">You are through the ${last ? 'last ' : ''}door</h2><p class="good">You opened Room ${index + 1} in ${count(row.flips, 'flip')}.</p>` +
      `<p class="note">The fewest possible is ${row.best}. Flipping switches without reading takes about ${Math.round(row.blind)} on average.${asks}</p>` +
      (last ? '<p>That was the last room. Your reading is written out below.</p><section id="log"></section><div class="buttons"><button type="button" class="quiet" id="again">Start again</button></div>' :
        `<div class="buttons"><button type="button" id="next">Go on to Room ${index + 2}</button></div>`);
    if (last) {
      showLog(done);
      byId('again').addEventListener('click', () => {
        results.close();
        restart();
      });
    } else {
      byId('next').addEventListener('click', () => {
        results.close();
        next();
      });
    }
    pauseInput();
    results.showModal();
  }

  function showLog(done) {
    const rows = done.map((row, i) => row ? `<tr><td>${i + 1}</td><td>${row.flips}</td><td>${row.best}</td><td>${Math.round(row.blind)}</td><td>${row.words ? 'shown' : row.asks}</td></tr>` : '').join('');
    byId('log').innerHTML = '<h2>Your reading so far</h2><table><thead><tr><th>Room</th><th>Your flips</th><th>Fewest</th><th>Flipping blind</th><th>Words</th></tr></thead>' +
      `<tbody id="logbody">${rows}</tbody></table><p class="note">“Flipping blind” is the average for someone who cannot read the things and flips a switch at random each time. “Words” is how many times you asked a thing to read itself out.</p>` +
      '<div class="buttons"><button type="button" id="copy">Copy my results</button></div><pre id="raw"></pre><p class="note" id="copied" aria-live="polite"></p>';
    const record = done.map((row, i) => row ? `r${i + 1} flips=${row.flips} best=${row.best} blind=${row.blind.toFixed(1)} asked=${row.words ? '-' : row.asks} secs=${row.secs}` : '').filter(Boolean);
    const raw = byId('raw');
    raw.textContent = [`RR ${new Date().toISOString().slice(0, 16)}`, ...record, navigator.userAgent].join(' | ');
    byId('copy').addEventListener('click', async () => {
      const copied = byId('copied');
      try {
        await navigator.clipboard.writeText(raw.textContent);
        copied.textContent = 'Copied.';
      } catch {
        copied.textContent = 'Press and hold the line above to copy it.';
      }
    });
  }

  results.addEventListener('cancel', (event) => event.preventDefault());
  function blocking() { return bookPanel.open || results.open; }
  return { ready, fail, update, openBook, closeBook, blocking };
}

beginReadingRoom();
