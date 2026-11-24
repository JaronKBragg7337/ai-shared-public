import * as THREE from 'three';
import { WINDOW_COLOR } from './room-skins.js';

const V = (x, y, z) => new THREE.Vector3(x, y, z);
const clamp = (value, low, high) => Math.max(low, Math.min(high, value));

// All positions and outside dimensions come from the objects the reader decoded.
export function buildScene({ things, scene, tier }) {
  const objects = new Map(), lamps = new Map(), obstacles = [];
  const root = new THREE.Group();
  const textures = new Set(), materials = new Set(), geometries = new Set();
  const geometry = (shape) => { geometries.add(shape); return shape; };
  const basic = (color, extras = {}) => {
    const material = new THREE.MeshBasicMaterial({ color, toneMapped: false, ...extras });
    materials.add(material);
    return material;
  };
  const spriteMaterial = new THREE.SpriteMaterial({ color: 0xffbd70, transparent: true, depthWrite: false,
    blending: THREE.AdditiveBlending, toneMapped: false, opacity: 0.16 });
  materials.add(spriteMaterial);
  const texture = (canvas) => {
    const map = new THREE.CanvasTexture(canvas);
    map.colorSpace = THREE.SRGBColorSpace;
    map.anisotropy = tier === 'mobile-lite' ? 2 : 4;
    textures.add(map);
    return map;
  };
  const unit = geometry(new THREE.BoxGeometry());
  const quad = geometry(new THREE.PlaneGeometry());
  const segments = tier === 'mobile-lite' ? 10 : 16;
  const ball = geometry(new THREE.SphereGeometry(1, segments, 8));
  const cylinder = geometry(new THREE.CylinderGeometry(1, 1, 1, segments));
  const frame = basic(0x222746), brass = basic(0x8c6639), pale = basic(0xc19c61), dark = basic(0x141831);
  function mesh(parent, shape, material, x, y, z, w = 1, h = 1, d = 1) {
    const part = new THREE.Mesh(shape, material);
    part.position.set(x, y, z);
    part.scale.set(w, h, d);
    parent.add(part);
    return part;
  }
  const box = (parent, material, x, y, z, w, h, d) => mesh(parent, unit, material, x, y, z, w, h, d);
  function group(parent, x, y, z, turn = 0) {
    const part = new THREE.Group();
    part.position.set(x, y, z);
    part.rotation.y = turn;
    parent.add(part);
    return part;
  }
  function block(x, z, w, d) {
    obstacles.push({ minX: x - w / 2, maxX: x + w / 2, minZ: z - d / 2, maxZ: z + d / 2 });
  }
  // One skin wraps a whole piece of furniture. Each board shows the part of the canvas that falls on it, at the
  // canvas's own scale, so the windows keep their shape instead of being squeezed into stripes. Two small moves keep
  // every board in windows: a narrow board is slid sideways onto the towers (the canvas has an empty margin either
  // side of them), and an edge thinner than a window and a half shows the one whole row its middle falls on.
  // The window size and where the towers stand come from the reader, which measured them off the ruler.
  // x, y, z are the board's centre measured from the thing's own origin (the middle of its foot).
  function wrapped(parent, material, thing, x, y, z, w, h, d) {
    const [fullW, fullH] = thing.size, { width, height } = thing.canvas;
    const cell = thing.cell, [first, last] = thing.span, rows = Math.floor((height - cell) / cell);
    const across = (from, size) => {
      const length = Math.min(width, size * width);
      let start = clamp(from * width, 0, width - length);
      if (length < last - first) start = clamp(start, first, last - length);
      return [start / width, (start + length) / width];
    };
    const up = (from, size) => {
      const length = Math.min(1, size), start = clamp(from, 0, 1 - length);
      if (length * height >= 1.6 * cell) return [start, start + length];
      const row = clamp(Math.floor((height - (start + length / 2) * height - cell) / cell), 0, rows - 1);
      return [1 - (row + 2) * cell / height, 1 - (row + 1) * cell / height];
    };
    const left = (x - w / 2) / fullW + 0.5, low = (y - h / 2) / fullH;
    const side = [across(left, d / fullW), up(low, h / fullH)];
    const top = [across(left, w / fullW), up(low, d / fullH)];
    const front = [across(left, w / fullW), up(low, h / fullH)];
    const shape = geometry(new THREE.BoxGeometry(w, h, d)), uv = shape.attributes.uv;
    [side, side, top, top, front, front].forEach(([[u0, u1], [v0, v1]], face) => {     // the order a box is built in
      for (let i = face * 4; i < face * 4 + 4; i++) {
        uv.setXY(i, u0 + (u1 - u0) * uv.getX(i), v0 + (v1 - v0) * uv.getY(i));
      }
    });
    return mesh(parent, shape, material, x, y, z);
  }

  // State lives in a uniform. The texture and its readable window pattern stay untouched.
  const bright = new THREE.Color(WINDOW_COLOR.glow), resting = new THREE.Color(WINDOW_COLOR.rest);
  const gain = new THREE.Vector3(bright.r / resting.r - 1, bright.g / resting.g - 1, bright.b / resting.b - 1);
  function skin(thing, canGlow = false) {
    const material = basic(0xffffff, { map: texture(thing.canvas) });
    const power = { value: 0 };
    if (canGlow) {
      material.onBeforeCompile = (shader) => {
        shader.uniforms.skinPower = power;
        shader.uniforms.skinGain = { value: gain };
        shader.fragmentShader = `uniform float skinPower; uniform vec3 skinGain;\n${shader.fragmentShader}`
          .replace('#include <map_fragment>', `#include <map_fragment>
            float window = smoothstep(0.045, 0.20, diffuseColor.r);
            diffuseColor.rgb *= vec3(1.0) + window * skinPower * skinGain;`);
      };
    }
    return { material, power };
  }

  const glareCanvas = document.createElement('canvas');
  glareCanvas.width = glareCanvas.height = 96;
  const ink = glareCanvas.getContext('2d');
  const fade = ink.createRadialGradient(48, 48, 0, 48, 48, 48);
  for (const [stop, color] of [[0, '#fff'], [0.3, '#aaa'], [0.66, '#393939'], [1, '#000']]) fade.addColorStop(stop, color);
  ink.fillStyle = fade;
  ink.fillRect(0, 0, 96, 96);
  const glowMap = texture(glareCanvas);
  spriteMaterial.map = glowMap;
  const additive = (color, map = glowMap) => basic(color, {
    map, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending,
  });
  function glow(x, y, z, w, h, tilt, turn, color) {
    const material = additive(color);
    mesh(root, quad, material, x, y, z, w, h).rotation.set(tilt, turn, 0);
    return material;
  }

  const doorThing = things.find((t) => t.kind === 'door');
  const shelfThing = things.find((t) => t.kind === 'shelf');
  const standThing = things.find((t) => t.kind === 'stand');
  const lanternThing = things.find((t) => t.kind === 'lantern');
  const grounds = things.filter((t) => t.kind === 'floor');
  const [roomFloor, hallFloor] = grounds;
  const [floorX, , floorZ] = roomFloor.at;
  const [floorW, , depth] = roomFloor.size;
  const bounds = { left: floorX - floorW / 2, right: floorX + floorW / 2, near: floorZ + depth / 2 };
  const [doorX, doorY, doorZ] = doorThing.at;
  const [doorW, doorH, doorD] = doorThing.size;
  const doorway = { x: doorX, z: doorZ - 0.018, width: doorW };
  const start = { x: floorX, z: bounds.near - 1.25 };

  for (const thing of things) {
    const { at: [x, y, z], size: [w, h, d], kind } = thing;
    if (kind === 'wall') {
      const { material } = skin(thing);
      const faces = d < w ? [dark, dark, dark, dark, material, material] : [material, material, dark, dark, dark, dark];
      box(root, faces, x, y, z, w, h, d);
    }
    if (kind === 'floor' || kind === 'ceiling') {
      const { material } = skin(thing);
      const faces = [dark, dark, material, material, dark, dark];
      box(root, faces, x, y, z, w, h, d);
    }
  }

  // The paired leaves share the door's skin and swing into the passage, clear of the player's path.
  const doorSkin = skin(doorThing, true);
  const doorHit = group(root, doorX, doorY, doorZ);
  const hinges = [-1, 1].map((side) => {
    const hinge = group(doorHit, side * (doorW / 2 - 0.018), 0, 0);
    const center = -side * (doorW / 4 - 0.01);
    box(hinge, doorSkin.material, center, 0, 0, doorW / 2 - 0.028, doorH - 0.026, doorD);
    for (const y of [-doorH / 2 + 0.06, doorH / 2 - 0.06]) {
      box(hinge, brass, center, y, 0, doorW / 2 - 0.006, 0.044, doorD + 0.035);
    }
    return hinge;
  });
  for (const side of [-1, 1]) box(root, frame, doorX + side * (doorW / 2 + 0.047), doorY, doorZ + 0.044, 0.094, doorH + 0.1, 0.25);
  box(root, frame, doorX, doorY + doorH / 2 + 0.055, doorZ + 0.045, doorW + 0.188, 0.1, 0.25);
  box(root, brass, doorX, 0.013, doorZ, doorW, 0.026, 0.31);
  const [hallX, , hallZ] = hallFloor.at;
  const [hallW, , hallD] = hallFloor.size;
  const passageEnd = hallZ - hallD / 2;
  const passage = document.createElement('canvas');
  passage.width = 128;
  passage.height = 192;
  const portal = passage.getContext('2d');
  portal.fillStyle = '#13162c';
  portal.fillRect(0, 0, 128, 192);
  const daylight = portal.createRadialGradient(65, 116, 14, 65, 116, 88);
  daylight.addColorStop(0, '#fff2cb');
  daylight.addColorStop(0.57, '#ffe3aa');
  daylight.addColorStop(1, '#f0ad60');
  portal.beginPath();
  portal.moveTo(9, 192);
  portal.lineTo(9, 62);
  portal.arc(64, 62, 55, Math.PI, 0);
  portal.lineTo(119, 192);
  portal.closePath();
  portal.fillStyle = daylight;
  portal.fill();
  const portalView = mesh(root, quad, basic(0xffffff, { map: texture(passage) }), hallX, 1.3, passageEnd, hallW - 0.12, 2.6);
  portalView.visible = false;
  const spill = glow(doorX, 0.006, doorway.z + 0.75, doorW * 2.6, 4.8, -Math.PI / 2, 0, 0xffbe73);
  const doorGlow = glow(doorX, doorY, doorZ + 0.084, doorW * 2.45, doorH * 1.35, 0, 0, 0xffc583);
  const doorReadAt = group(hinges[1], -doorW / 4 + 0.01, 0.22, doorD / 2 + 0.012);
  const doorAim = V(doorX, doorY + 0.3, doorway.z + 0.19);
  objects.set(doorThing.id, { x: doorAim.x, z: doorAim.z, aim: doorAim,
    aims: [doorAim, ...[-1, 1].map((side) => V(doorX + side * doorW * 0.29, doorAim.y, doorAim.z))],
    hit: [doorHit], readAt: doorReadAt,
    power: doorSkin.power, inlet: V(doorX + doorW / 2 + 0.085, 0.93, doorZ + 0.205) });

  for (const thing of things.filter((t) => t.kind === 'switch' || t.kind === 'lamp')) {
    const { id, kind, at: [x, y, z], size: [w, h, d] } = thing;
    const side = Math.sign(x - floorX);
    const body = group(root, x, y, z, -side * Math.PI / 2);
    const { material, power } = skin(thing, true);
    box(body, material, 0, 0, 0, w, h, d);
    for (const end of [-1, 1]) box(body, brass, 0, end * (h / 2 + 0.018), 0, w + 0.045, 0.035, d + 0.045);
    const data = { x, z, aim: V(x, y, z), hit: [body], power,
      readAt: group(body, 0, 0, d / 2 + 0.01),
      output: V(x - side * d * 0.35, y - h / 2 - 0.046, z),
      inlet: V(x - side * d * 0.32, y - h / 2 - 0.009, z) };
    objects.set(id, data);
    if (kind === 'switch') {
      const handle = group(body, 0, -h / 2 - 0.08, d * 0.49);
      const pin = mesh(body, cylinder, frame, 0, handle.position.y, handle.position.z, 0.053, 0.096, 0.053);
      pin.rotation.z = Math.PI / 2;
      mesh(handle, cylinder, brass, 0, 0.084, 0, 0.021, 0.168, 0.021);
      data.leverKnob = mesh(handle, ball, pale, 0, 0.181, 0, 0.048, 0.052, 0.048);
      data.lever = handle;
      block(x - 0.05, z, 0.35, 0.38);
    } else {
      box(body, frame, 0, h * 0.36, -d / 2 - 0.07, 0.095, 0.09, 0.14);
      const wallX = side > 0 ? bounds.right - 0.008 : bounds.left + 0.008;
      const wall = glow(wallX, y, z, 3.4, 3.25, 0, body.rotation.y, 0xffb765);
      const floor = glow(x - side * 1.28, 0.005, z, 3.65, 4, -Math.PI / 2, 0, 0xffb765);
      lamps.set(id, { wall, floor });
      block(x - side * 0.06, z, 0.56, 0.5);
    }
  }

  const shelf = group(root, ...shelfThing.at);
  const [shelfW, shelfH, shelfD] = shelfThing.size;
  const cabinet = skin(shelfThing).material;
  const board = (...place) => wrapped(shelf, cabinet, shelfThing, ...place);
  board(0, shelfH / 2, -shelfD * 0.38, shelfW, shelfH, 0.093);
  for (const side of [-1, 1]) board(side * (shelfW / 2 - 0.075), shelfH / 2, 0, 0.15, shelfH, shelfD);
  for (const y of [0.08, 0.55, 1.136, 1.78, shelfH - 0.038]) {
    board(0, y, 0, shelfW, 0.074, shelfD);
    box(shelf, brass, 0, y - 0.02, shelfD / 2 + 0.005, shelfW - 0.16, 0.016, 0.016);
  }
  const [shelfX, shelfY, shelfZ] = shelfThing.at;
  const shelfAim = V(shelfX, shelfY + 1.44, shelfZ + 0.23);
  const volumes = things.filter((t) => t.kind === 'book').sort((a, b) => a.index - b.index).map((book) => {
    const volume = group(root, ...book.at);
    const [w, h, d] = book.size;
    volume.rotation.set(0, [0.16, -0.13, 0.12][book.index], [-0.096, 0.04, -0.052][book.index]);
    volume.userData.book = book.index;
    const cover = skin(book).material;
    box(volume, cover, 0, 0, 0, w, h, d);
    box(volume, pale, w * 0.48, 0, 0, 0.016, h - 0.045, d - 0.036);
    return volume;
  });
  objects.set(shelfThing.id, { x: shelfAim.x, z: shelfAim.z, aim: shelfAim, hit: volumes });
  block(shelfX, shelfZ, shelfW, shelfD);

  const bench = things.find((t) => t.kind === 'bench');
  if (bench) {
    const [x, y, z] = bench.at, [w, h, d] = bench.size;
    const material = skin(bench).material;
    const seat = group(root, x, y, z);
    wrapped(seat, material, bench, 0, h - 0.052, 0, w, 0.104, d);
    for (const side of [-1, 1]) wrapped(seat, material, bench, side * w * 0.39, h * 0.43, 0, 0.12, h * 0.86, d * 0.84);
    block(x, z, w, d);
  }

  const [perchX, perchY, perchZ] = lanternThing.at;
  const perch = { x: perchX, y: perchY, z: perchZ };
  const [standX, standY, standZ] = standThing.at;
  const [footW, standH, footD] = standThing.size;
  const stand = group(root, standX, standY, standZ);
  const column = skin(standThing).material;
  wrapped(stand, column, standThing, 0, 0.039, 0, footW, 0.078, footD);
  wrapped(stand, column, standThing, 0, standH / 2, 0, footW * 0.45, standH, footD * 0.45);
  box(stand, frame, 0, standH - 0.02, 0, footW * 0.83, 0.045, footD * 0.83);
  block(standX, standZ, footW, footD);

  const body = group(root, ...lanternThing.at);
  const [w, h, d] = lanternThing.size;
  const lanternSkin = skin(lanternThing, true);
  box(body, lanternSkin.material, 0, h * 0.38, 0, w, h * 0.73, d);
  for (const y of [0.014, h * 0.76]) box(body, brass, 0, y, 0, w + 0.028, 0.024, d + 0.028);
  const handle = geometry(new THREE.TorusGeometry(0.029, 0.0045, 6, segments));
  mesh(body, handle, pale, 0, h * 0.89, 0);
  const sprite = new THREE.Sprite(spriteMaterial);
  sprite.scale.setScalar(0.22);
  sprite.position.y = 0.095;
  body.add(sprite);
  const pool = mesh(root, quad, additive(0xffb466), perchX, 0.007, perchZ, 0.7, 0.7);
  pool.rotation.x = -Math.PI / 2;
  const thread = mesh(root, cylinder, additive(0xffd08c, null), 0, 0, 0);
  thread.material.opacity = 0.48;
  const seenGlow = mesh(root, quad, additive(0xffc278), 0, 0, 0, 0.68, 0.82);
  thread.visible = seenGlow.visible = false;
  const up = V(0, 1, 0), along = V(0, 0, 0), targetAt = V(0, 0, 0), from = V(0, 0, 0);
  let wokeAt = 0, lastKey = '';
  const lanternView = {
    thing: lanternThing,
    aim: V(perchX, perchY + 0.12, perchZ),
    hits: [body, stand],
    wake(now) { wokeAt = now; },
    update(now, lantern, still) {
      if (!lantern.awake) return false;
      const t = still ? 1 : clamp((now - wokeAt) / 900, 0, 1);
      const ease = t * t * (3 - 2 * t);
      const bob = still ? 0 : Math.sin(now / 640) * 0.022 + Math.sin(now / 1730) * 0.008;
      body.position.set(lantern.pos.x, lantern.pos.y - 0.095 + bob * ease, lantern.pos.z);
      if (!still) body.rotation.y = Math.sin(now / 2400) * 0.35;
      lanternSkin.power.value = ease;
      sprite.scale.setScalar(0.22 + 0.65 * ease);
      spriteMaterial.opacity = 0.16 + 0.48 * ease;
      const height = Math.max(0.4, body.position.y);
      pool.position.set(body.position.x, 0.007, body.position.z);
      pool.scale.setScalar(0.9 + height * 0.45);
      pool.material.opacity = (0.05 + 0.22 * ease) * clamp(1.9 / height, 0.55, 1.25);
      const target = objects.get(lantern.seeing)?.readAt;
      seenGlow.visible = thread.visible = Boolean(target);
      if (target) {
        target.getWorldPosition(targetAt);
        target.getWorldQuaternion(seenGlow.quaternion);
        seenGlow.position.copy(targetAt);
        seenGlow.material.opacity = 0.33;
        from.copy(body.position).addScaledVector(up, 0.095);
        along.subVectors(targetAt, from);
        const length = along.length();
        thread.position.copy(from).addScaledVector(along, 0.5);
        thread.quaternion.setFromUnitVectors(up, along.normalize());
        thread.scale.set(0.004, Math.max(0.01, length - 0.1), 0.004);
      }
      const key = still ? `${lantern.pos.x},${lantern.pos.y},${lantern.pos.z},${lantern.seeing},${t}` : '';
      const changed = !still || key !== lastKey;
      lastKey = key;
      return changed;
    },
  };

  scene.add(root);
  return {
    depth, bounds, objects, obstacles, doorway, start, perch, lanternView, decorated: true,
    updateDoor(progress) {
      hinges[0].rotation.y = progress * 1.52;
      hinges[1].rotation.y = -progress * 1.52;
      portalView.visible = progress > 0;
      spill.opacity = progress * 0.51;
      doorGlow.opacity = progress * 0.2;
    },
    updateThing(thing, on) {
      const entry = objects.get(thing.id);
      entry.power.value = Number(on);
      if (entry.lever) entry.lever.rotation.x = on ? 0.62 : 2.54;
      const lamp = lamps.get(thing.id);
      if (lamp) {
        lamp.wall.opacity = on ? 0.62 : 0;
        lamp.floor.opacity = on ? 0.37 : 0;
      }
    },
    dispose() {
      root.removeFromParent();
      for (const map of textures) map.dispose();
      for (const material of materials) material.dispose();
      for (const shape of geometries) shape.dispose();
    },
  };
}
