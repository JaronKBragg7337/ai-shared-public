// Path B, piece 1. A fresh learner with no language model learns what the Reading Room's marks mean by looking,
// then reads rooms it has never seen. Plan: learner/PLAN.md (committed before the first run; the playing learner
// was added after the first run, by a dated note written before it ran).
//   node learner/learn.mjs            writes learner/results.json and learner/RESULTS.md
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { rng } from '../world.js';
import { ROOMS, buildRoom, marksOf, openSettings, fewestFlips, blindAverage, codeText } from '../rooms.js';
import { makeMind } from './mind.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const LEARNERS = 200, LIFE = 30;
const mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;

// The learner itself lives in mind.js, the very file the 3D Reading Room carries as its lantern.
const { randomRoom, newLearner, trusted, play, KINDS, reading } = makeMind({ rng, buildRoom, marksOf, openSettings });

// ---------------------------------------------------------------- the run: the same rooms for everyone
const lives = [];
for (let s = 0; s < LEARNERS; s++) { const r = rng(1000 + s), rooms = []; for (let k = 0; k < LIFE; k++) rooms.push(randomRoom(r)); lives.push(rooms); }
const handDefs = ROOMS.map((def) => { const open = openSettings(def.things); return { things: def.things, open, n: def.things.filter((t) => t.kind === 'switch').length }; });
const base = Array.from({ length: LIFE }, (_, k) => ({ watcher: [], fewest: lives.map((rooms) => fewestFlips(rooms[k].open)), blind: lives.map((rooms) => blindAverage(rooms[k].open, rooms[k].n)) }));
lives.forEach((rooms, s) => { const theirs = rng(9000 + s); rooms.forEach((def, k) => base[k].watcher.push(play(def, theirs, null).flips)); });

function live(playful, seedBase) {
  const rows = Array.from({ length: LIFE }, () => ({ reader: [], reading: [], looks: [], played: [], plain: [], needs2: [], dark: [] }));
  const hand = ROOMS.map(() => []), trust = {}, readAt = [];
  lives.forEach((rooms, s) => {
    const L = newLearner(), mine = rng(seedBase + s); let first = null, played = 0;
    rooms.forEach((def, k) => {
      const share = reading(L), row = rows[k]; if (first === null && share.all >= 0.99) first = k;
      row.reading.push(share.all); for (const kind of KINDS) row[kind].push(share[kind]); row.looks.push(L.looks); row.played.push(played);
      const went = play(def, mine, L, playful); row.reader.push(went.flips); played += went.playFlips;
    });
    handDefs.forEach((def, i) => hand[i].push(play(def, mine, L, playful).flips));
    const t = trusted(L); trust[t] = (trust[t] || 0) + 1; readAt.push(first);
  });
  const span = (key, from, to) => mean(rows.slice(from, to).map((row) => mean(row[key])));
  const table = rows.map((row, k) => ({ room: k + 1, reading: mean(row.reading), plain: mean(row.plain), needs2: mean(row.needs2), dark: mean(row.dark), looks: mean(row.looks), played: mean(row.played),
    reader: mean(row.reader), watcher: mean(base[k].watcher), fewest: mean(base[k].fewest), blind: mean(base[k].blind) }));
  const late = span('reader', 10, LIFE), lateFewest = mean(base.slice(10).map((b) => mean(b.fewest))), wEarly = mean(base.slice(0, 10).map((b) => mean(b.watcher))), wLate = mean(base.slice(20).map((b) => mean(b.watcher)));
  const got = readAt.filter((v) => v !== null);
  return { table, trust, late, lateFewest, wEarly, wLate,
    hand: hand.map((flips, i) => ({ room: i + 1, fewest: fewestFlips(handDefs[i].open), exact: flips.filter((f) => f === fewestFlips(handDefs[i].open)).length, mean: mean(flips), worst: Math.max(...flips) })),
    readAt: { never: readAt.length - got.length, mean: got.length ? mean(got) : null, worst: got.length ? Math.max(...got) : null },
    predictions: { p1: mean(rows[10].reading) >= 0.99, p2: late <= lateFewest * 1.1, p3: Math.abs(wLate - wEarly) / wEarly <= 0.1 && wLate > late * 1.5, p4: hand.every((flips, i) => flips.every((f) => f === fewestFlips(handDefs[i].open))) } };
}
const planned = live(false, 5000), playing = live(true, 7000);
const out = { made: new Date().toISOString(), learners: LEARNERS, roomsEach: LIFE, planned, playing, exampleRoom: codeText(randomRoom(rng(7)).things) };
fs.writeFileSync(path.join(here, 'results.json'), JSON.stringify(out, null, 1));

// ---------------------------------------------------------------- the report
const P = [], f1 = (v) => v.toFixed(1), f2 = (v) => v.toFixed(2), pct = (v) => (100 * v).toFixed(1) + '%', say = (ok) => (ok ? '**held**' : '**did not hold**');
const PICK = [0, 1, 2, 3, 4, 6, 9, 14, 19, 29];
function section(title, intro, R, playful) {
  P.push(`## ${title}`, '', intro, '',
    `| rooms lived through | reading (rooms it never plays) | looks so far |${playful ? ' play flips so far |' : ''} flips to open the door: the learner | a careful watcher (cannot see marks) | fewest possible | flipping blind |`, `|---|---|---|${playful ? '---|' : ''}---|---|---|---|`);
  for (const k of PICK) { const t = R.table[k]; P.push(`| ${k} | ${pct(t.reading)} | ${Math.round(t.looks)} |${playful ? ` ${Math.round(t.played)} |` : ''} ${f2(t.reader)} | ${f2(t.watcher)} | ${f2(t.fewest)} | ${f1(t.blind)} |`); }
  P.push('', 'Each row is the room played AFTER that many rooms; its reading is tested just before it walks in.', '',
    `Reading first reached 99% after ${R.readAt.mean === null ? 'no' : f1(R.readAt.mean)} rooms on average, among the ${LEARNERS - R.readAt.never} of ${LEARNERS} learners that got there within ${LIFE} rooms (slowest of those: ${R.readAt.worst}).`,
    `What the ${LEARNERS} learners ended up trusting about a filled circle: ${Object.entries(R.trust).map(([g, c]) => `${g} ${c}`).join(', ')} ("named" = it follows the thing whose sign is drawn under it, which is the truth).`, '',
    'Reading, split by kind of thing:', '', '| rooms lived through | needs 1, no dark wire | needs 2 or more | has a dark wire |', '|---|---|---|---|',
    ...[0, 4, 9, 19, 29].map((k) => `| ${k} | ${pct(R.table[k].plain)} | ${pct(R.table[k].needs2)} | ${pct(R.table[k].dark)} |`), '',
    'The four hand-made rooms of the Reading Room, played by each learner after its 30 random rooms:', '', '| room | fewest flips | learners that used exactly that | average | worst |', '|---|---|---|---|---|',
    ...R.hand.map((h) => `| ${h.room} | ${h.fewest} | ${h.exact} of ${LEARNERS} | ${f2(h.mean)} | ${h.worst} |`), '',
    `1. Reading reaches 99% within 10 rooms on average: ${say(R.predictions.p1)} (after 10 rooms: ${pct(R.table[10].reading)}).`,
    `2. From room 11 on, the learner's flips are within 10% of the fewest possible: ${say(R.predictions.p2)} (${f2(R.late)} against ${f2(R.lateFewest)}).`,
    `3. The watcher does not improve with experience and stays well above the learner: ${say(R.predictions.p3)} (rooms 1 to 10: ${f2(R.wEarly)}; rooms 21 to 30: ${f2(R.wLate)}; the learner late: ${f2(R.late)}).`,
    `4. Every trained learner opens the four hand-made rooms in exactly the fewest flips: ${say(R.predictions.p4)}.`, '');
}
P.push('# Path B, piece 1: a fresh learner learns to read the room by looking', '',
  `Made by \`node learner/learn.mjs\` on ${out.made.slice(0, 16)} UTC. Never typed. Plan: \`learner/PLAN.md\`.`, '',
  `${LEARNERS} learners, each starting from nothing, each living through ${LIFE} random rooms of its own. No language model: one weighing of five counts and five scored guesses. Everyone plays the same rooms.`, '');
section('The planned learner', 'As written in the plan before any run: it looks only while it is opening a door. The four numbered lines are what I expected, written before the run.', planned, false);
section('After the plan: the learner that may play', 'The next way, written into the plan before this ran: once a door is open it stays for as many extra flips as the room has levers, just to look, led by its own doubt. Play flips are counted apart from door flips. The same four expectations, applied to it.', playing, true);
P.push('One of the random rooms, as its own code page (to show what kind of room these are):', '', '```', out.exampleRoom, '```', '');
fs.writeFileSync(path.join(here, 'RESULTS.md'), P.join('\n'));
console.log(P.join('\n'));
