# Computational World, Prototype 0: results

Made by `report.mjs` from the saved runs. Machine: Intel(R) Core(TM) i9-14900HX, 32 threads, Node v24.16.0, 2026-11-23.
Every answer in every row was checked: **all correct** (141 rows). Facts mark `65e84cd1`.

## 1. The same job, eight ways

The job: one card joins or leaves the pile; say whether the pile now holds a set. Times are for one change. "Steps" is how many small pieces of work it took (pair checks, gate updates or messages).

**A big pile with no set in it (where a search lives)**

| way | 81 cards, pile ~17 | 243 cards, pile ~36 | 729 cards, pile ~70 | steps at 729 |
|---|---|---|---|---|
| Plain program (re-check) | 179 ns | 705 ns | 2.39 µs | 1,495 |
| Hand-written counters | 95 ns | 192 ns | 490 ns | 364 |
| Minecraft way (gates, every tick) | 257.74 µs | 2.70 ms | 26.48 ms | 5,119,582 |
| Gates, one sweep per answer | 14.72 µs | 127.82 µs | 1.07 ms | 265,355 |
| Gates, only what changed | 407 ns | 941 ns | 2.06 µs | 437 |
| Own parts, every tick | 24.29 µs | 207.66 µs | 1.78 ms | 265,359 |
| Own parts, one sweep per answer | 6.28 µs | 56.13 µs | 482.22 µs | 88,453 |
| World's own parts, only what changed | 155 ns | 330 ns | 842 ns | 368 |

**A small pile**

| way | 81 cards | 243 cards | 729 cards | steps at 729 |
|---|---|---|---|---|
| Plain program (re-check) | 47 ns | 81 ns | 135 ns | 75 |
| Hand-written counters | 87 ns | 188 ns | 493 ns | 364 |
| Minecraft way (gates, every tick) | 87.12 µs | 834.89 µs | 5.77 ms | 1,088,840 |
| Gates, one sweep per answer | 14.91 µs | 129.81 µs | 1.10 ms | 265,355 |
| Gates, only what changed | 234 ns | 465 ns | 1.11 µs | 373 |
| Own parts, every tick | 11.60 µs | 100.16 µs | 734.95 µs | 106,144 |
| Own parts, one sweep per answer | 7.06 µs | 60.65 µs | 495.05 µs | 88,453 |
| World's own parts, only what changed | 114 ns | 293 ns | 812 ns | 364 |

**What the table says**
- **When parts run matters most.** On the big pile at 729 cards the Minecraft way needs 26.48 ms per change and the same gates run only-what-changed need 2.06 µs: **12,838 times** apart, with identical parts. The gap grows with the world: 634 times at 81, 2,874 times at 243, 12,838 times at 729.
- **What the parts are matters much less.** Gates against the world's own parts, both run only-what-changed: 2.6 times at 81, 2.8 times at 243, 2.5 times at 729.
- **End to end**, Minecraft way against the world's own parts: 1,666 times at 81, 8,192 times at 243, 31,461 times at 729.
- **The world against the plain program.** On a big pile the world's own parts are 2.8 times faster than re-checking at 729 cards (2.1 at 243, 1.2 at 81). On a small pile the plain program wins: 6.0 times faster at 729 cards.
- **A step costs about the same everywhere.** At 729 cards on the big pile, one step takes 1.6 ns in the plain program (a pair check), 2.3 ns in the world's own parts (a message) and 5.2 ns the Minecraft way (a gate update). The ways differ in how many steps they take: 1,495, 368 and 5,119,582.
- **What the world itself costs.** The same idea written by hand, with no world around it, is 1.6 times faster at 81, 1.7 times faster at 243, 1.7 times faster at 729. That is the price of a general engine.

## 2. A fresh pile every time (nothing to reuse)

| way | 81 cards | 243 cards | 729 cards |
|---|---|---|---|
| Plain program (re-check) | 113 ns | 188 ns | 278 ns |
| Hand-written counters | 1.13 µs | 4.16 µs | 16.38 µs |
| Minecraft way (gates, every tick) | 238.26 µs | 2.43 ms | 25.14 ms |
| Gates, one sweep per answer | 14.76 µs | 124.22 µs | 1.06 ms |
| Gates, only what changed | 2.46 µs | 8.58 µs | 34.79 µs |
| Own parts, every tick | 19.36 µs | 161.83 µs | 1.45 ms |
| Own parts, one sweep per answer | 6.86 µs | 57.27 µs | 477.93 µs |
| World's own parts, only what changed | 1.63 µs | 6.14 µs | 26.35 µs |

Kept state does not pay here: the plain program is 95 times faster than the world's own parts at 729 cards, because each question starts from an empty table.

## 3. When many cards change at once

Only-what-changed against one full sweep, both on the world's own parts.

| share of the cards changing each step | 81: changed-only / sweep | 243: changed-only / sweep | 729: changed-only / sweep |
|---|---|---|---|
| 2% | 541 ns / 7.86 µs | 4.39 µs / 69.52 µs | 38.34 µs / 591.72 µs |
| 5% | 1.18 µs / 8.03 µs | 9.82 µs / 70.88 µs | 92.01 µs / 590.94 µs |
| 10% | 2.43 µs / 7.97 µs | 20.54 µs / 71.70 µs | 188.60 µs / 590.49 µs |
| 25% | 5.75 µs / 8.19 µs | 52.45 µs / 71.45 µs | 466.41 µs / 590.47 µs |
| 50% | 11.79 µs / 8.65 µs (sweep wins) | 103.62 µs / 72.37 µs (sweep wins) | 904.23 µs / 591.41 µs (sweep wins) |

Only-what-changed stops paying when about **36%, 35%, 32%** of the cards change in one step (81, 243, 729 cards; read off the 25% and 50% rows).

## 4. Search: building a pile with no set in it

| job | cards | plain program | hand-written counters | world's own parts | best pile found | best possible |
|---|---|---|---|---|---|---|
| take free cards in a random order | 81 | 12.37 µs | 12.87 µs | 23.20 µs | 20 (300 piles) | 20 |
| take free cards in a random order | 243 | 35.75 µs | 49.64 µs | 107.27 µs | 38 (60 piles) | 45 |
| take free cards in a random order | 729 | 105.12 µs | 178.77 µs | 696.81 µs | 74 (12 piles) | 112 |
| look ahead one card | 81 | 997.27 µs | 390.68 µs | 810.00 µs | 18 (12 piles) | 20 |
| look ahead one card | 243 | 24.47 ms | 4.18 ms | 12.02 ms | 38 (3 piles) | 45 |
| look ahead one card | 729 | 740.79 ms | 62.92 ms | 209.02 ms | 80 (1 pile) | 112 |

- Taking cards in a fixed order asks one small question per card, and the plain program is the cheapest way to answer it (6.6 times faster than the world at 729 cards).
- Looking ahead asks a whole-table question ("how many cards would still be free?") hundreds of times per card. There the kept state pays: the world is 3.5 times faster than the plain program at 729 cards, and hand-written counters are 12 times faster.
- All three ways built identical piles in every run (same cards, same order), and the Verifier found no set in any of them.

## 5. Memory

| cards | world's own parts | the same, every change written to the Chronicle | replay of one change | bytes per change |
|---|---|---|---|---|
| 81 | 114 ns | 84 ns | 94 ns | 8 |
| 243 | 293 ns | 294 ns | 296 ns | 8 |
| 729 | 812 ns | 768 ns | 811 ns | 8 |

Keeping every change costs almost nothing next to doing the work (differences this small are inside the run-to-run noise), and replaying the list on a fresh world lands on the same state every time (3 of 3 replays).

Room each way needs (its tables plus its running state):

| way | 81 cards | 243 cards | 729 cards |
|---|---|---|---|
| Plain program | 13 KB | 117 KB | 1.0 MB |
| Hand-written counters | 14 KB | 126 KB | 1.1 MB |
| Gate world | 144 KB | 1.3 MB | 11.4 MB |
| World's own parts | 71 KB | 628 KB | 5.5 MB |

World sizes: 81 cards, gates: 3320 parts, 6478 links, 13 deep; 81 cards, own parts: 1162 parts, 4320 links, 2 deep; 81 cards, own parts + search state: 4484 parts, 14202 links, 3 deep; 243 cards, gates: 29645 parts, 58804 links, 16 deep; 243 cards, own parts: 10045 parts, 39204 links, 2 deep; 243 cards, own parts + search state: 39692 parts, 127899 links, 3 deep; 729 cards, gates: 266084 parts, 530710 links, 19 deep; 729 cards, own parts: 89182 parts, 353808 links, 2 deep; 729 cards, own parts + search state: 355268 parts, 1151334 links, 3 deep.

## 6. Energy

Read from the processor's own power meter (Intel RAPL through Windows), small-pile stream, about 5 seconds per row. Idle was 5.3 W. This is the whole processor package, so a row's watts depend on which core Windows chose.

| cards | way | watts | microjoules per change | above idle |
|---|---|---|---|---|
| 81 | ordinary software (re-check) | 27.1 | 1.111 | 0.893 |
| 81 | hand-written counters | 24.4 | 1.749 | 1.368 |
| 81 | the world's own parts, only what changed | 26 | 2.594 | 2.064 |
| 81 | gates, only what changed | 32.3 | 6.403 | 5.349 |
| 81 | gates, every tick (the Minecraft way) | 25.1 | 1,791 | 1,412 |
| 729 | ordinary software (re-check) | 26 | 3.368 | 2.678 |
| 729 | hand-written counters | 25.5 | 11.49 | 9.097 |
| 729 | the world's own parts, only what changed | 29.1 | 22.522 | 18.413 |
| 729 | gates, only what changed | 34 | 37.21 | 31.386 |
| 729 | gates, every tick (the Minecraft way) | 24.6 | 134,424 | 105,376 |

Energy follows time: the Minecraft way used 691 times the energy of the world's own parts per change at 81 cards and 5,969 times at 729.

## 7. The same world on a phone and in a browser

The page (`index.html`) runs the identical `world.js`. Each row is the page's own "Run the measurement" button, except the last, which is the Node run from section 1 for comparison. 243 cards, big pile, time for one change.

| where | plain program | hand-written | Minecraft way | gates, changes only | world's own parts | Minecraft / own |
|---|---|---|---|---|---|---|
| **Jaron's iPhone (iOS 18.7, inside the Claude app), 11/23/2026 3:29 PM** | 467 ns | 207 ns | 2.13 ms | 1.25 µs | 417 ns | 5,116 times |
| MSI, iphone-webkit | 697 ns | 214 ns | 1.61 ms | 977 ns | 313 ns | 5,152 times |
| MSI, edge | 533 ns | 201 ns | 3.10 ms | 1.05 µs | 343 ns | 9,040 times |
| MSI, Node (section 1) | 705 ns | 192 ns | 2.70 ms | 941 ns | 330 ns | 8,192 times |

On the real phone every answer matched. Against the MSI's Node run, the phone took 0.7 times the MSI's time for the plain program, 0.8 for the Minecraft way and 1.3 for the world's own parts. A phone chip runs this world at about the speed of the laptop. The two are different JavaScript engines, so small differences mean little.

## 8. Bare against built (plan: `llm/PLAN.md`, committed before the first graded try)

### qwen3.5:4b: 120 tries per run, 5 complete runs per arm, 4800 tries in the chronicle

| arm | best grade, average of the runs | each run | first try | tries it could read | different recipes per run | best came at try | seconds | watt-hours |
|---|---|---|---|---|---|---|---|---|
| A: bare, one try | 3.211 | 4.01 4.01 4.01 4.01 0.00 | | | | | | |
| 0a: no model: random card orders | **4.476** | 4.46 4.48 4.46 4.48 4.50 | 4.34 | 100% |  | 23 84 59 106 110 |  |  |
| 0b: no model: random recipes | **4.846** | 4.65 5.16 5.00 4.69 4.72 | 4.01 | 100% | 120 | 110 59 57 93 28 |  |  |
| A+: bare, checker keeps the best | **4.362** | 4.47 4.37 4.12 4.36 4.48 | 3.21 | 89% | 49 | 16 24 73 95 38 | 147 | 2.62 |
| B: + its own last grade | **4.636** | 4.40 4.54 4.58 4.80 4.86 | 2.41 | 96% | 63 | 29 57 66 18 47 | 227 | 4.89 |
| C: + the 3 best from the record | **4.545** | 4.65 4.56 4.59 4.01 4.91 | 3.21 | 97% | 64 | 66 93 106 1 49 | 281 | 6.16 |
| D: + 3 picked by facing | **4.832** | 4.66 4.73 4.79 4.77 5.20 | 4.01 | 90% | 71 | 93 100 69 58 26 | 436 | 9.80 |
| E: AFTER THE PLAN: changes one thing in a good recipe; record starts with 0b's finds | **4.955** | 4.78 5.20 5.20 4.77 4.83 | 4.59 | 99% | 43 | 88 118 34 5 118 | 423 | 9.44 |
| R: AFTER THE PLAN (control): + 3 drawn at random from the record | **4.352** | 4.73 4.17 4.01 4.36 4.48 | 4.01 | 96% | 78 | 98 7 1 110 73 | 292 | 6.30 |

Seconds and watt-hours are rough: other jobs (the timing pass, page checks, the loops below) ran on the machine during some arms, which stretches them. Grades are not affected.

By the rule fixed in the plan (higher on average and in at least 4 of 5 paired runs):
- 1. The checker is worth something (A+ over A): **yes** (average +1.151, higher in 5 of 5 paired runs).
- 2. Feedback helps (B over A+): **yes** (average +0.275, higher in 4 of 5 paired runs).
- 3. Keeping what worked helps (C over B): **no clear difference** (average -0.092, higher in 4 of 5 paired runs).
- 4. Facing against the top list (D over C): **yes** (average +0.287, higher in 5 of 5 paired runs).
-    and the other way (C over D): **no clear difference** (average -0.287, higher in 0 of 5 paired runs).
- 6. Not decoration (A+ over random recipes 0b): **no clear difference** (average -0.484, higher in 0 of 5 paired runs).
- 6. Not decoration (B over random recipes 0b): **no clear difference** (average -0.210, higher in 2 of 5 paired runs).
- 6. Not decoration (C over random recipes 0b): **no clear difference** (average -0.301, higher in 1 of 5 paired runs).
- 6. Not decoration (D over random recipes 0b): **no clear difference** (average -0.014, higher in 3 of 5 paired runs).
-    A+ over random card orders 0a: **no clear difference** (average -0.114, higher in 1 of 5 paired runs).
-    B over random card orders 0a: **yes** (average +0.161, higher in 4 of 5 paired runs).
-    C over random card orders 0a: **yes** (average +0.069, higher in 4 of 5 paired runs).
-    D over random card orders 0a: **yes** (average +0.357, higher in 5 of 5 paired runs).

After the plan (exploratory, same rule applied):
- The model as a changer of good recipes (E) over the random recipes it started from (0b): **yes** (average +0.109, higher in 5 of 5 paired runs).
- E over the top-list arm (C): **yes** (average +0.410, higher in 4 of 5 paired runs).
- E over facing (D): **no clear difference** (average +0.123, higher in 3 of 5 paired runs).

The control for the facing result (arm R, asked for by ChatGPT; plan note written before its first try; same rule):
- Facing over a random draw (D over R): **yes** (average +0.480, higher in 4 of 5 paired runs).
-    and the other way (R over D): **no clear difference** (average -0.480, higher in 1 of 5 paired runs).
- The top list over a random draw (C over R): **no clear difference** (average +0.192, higher in 3 of 5 paired runs).
-    and the other way (R over C): **no clear difference** (average -0.192, higher in 2 of 5 paired runs).
- Three random earlier tries over the last grade alone (R over B): **no clear difference** (average -0.284, higher in 1 of 5 paired runs).

Best single try in each arm: 0a: `(a card order)` 4.499 (9, 18, 37, 75, 141, 261); 0b: `min(3, (t + (d(2) == d(1))))` 5.161 (8, 18, 40, 96, 192, 416); A+: `-z && -o && -t` 4.484 (8, 20, 38, 72, 138, 268); B: `-abs(z-o)` 4.861 (9, 20, 38, 80, 147, 348); C: `z*o/t + w/n` 4.911 (9, 20, 39, 79, 163, 332); D: `max(9 + (n==3 ? 1 : (n==4 ? 2 : (n==5 ? 4 : (n==6 ? 7 : (n==7 ? 10 : 18))))) * min(t+1, 3), n)` 5.199 (8, 20, 40, 96, 192, 384); E: `min(3, t + ((d(1) == d(2)) || (d(0) == d(2)) || (d(0) == d(1))))` 5.199 (8, 20, 40, 96, 192, 384); R: `-n + t*o*z` 4.733 (8, 20, 40, 79, 154, 306).

### qwen3.5:9b: 120 tries per run, 5 complete runs per arm, 4200 tries in the chronicle

| arm | best grade, average of the runs | each run | first try | tries it could read | different recipes per run | best came at try | seconds | watt-hours |
|---|---|---|---|---|---|---|---|---|
| A: bare, one try | 0.803 | 0.00 4.01 0.00 0.00 0.00 | | | | | | |
| 0a: no model: random card orders | **4.476** | 4.46 4.48 4.46 4.48 4.50 | 4.34 | 100% |  | 23 84 59 106 110 |  |  |
| 0b: no model: random recipes | **4.846** | 4.65 5.16 5.00 4.69 4.72 | 4.01 | 100% | 120 | 110 59 57 93 28 |  |  |
| A+: bare, checker keeps the best | **4.283** | 4.48 4.10 4.22 4.25 4.37 | 0.80 | 69% | 54 | 115 40 8 101 83 | 471 | 10.82 |
| B: + its own last grade | **4.512** | 4.73 4.32 4.44 4.46 4.61 | 3.21 | 58% | 48 | 59 46 58 14 81 | 919 | 21.78 |
| C: + the 3 best from the record | **4.121** | 4.01 4.01 4.01 4.55 4.01 | 2.41 | 81% | 49 | 1 1 1 108 2 | 687 | 15.98 |
| D: + 3 picked by facing | **4.522** | 4.82 4.22 4.80 4.64 4.13 | 2.41 | 88% | 63 | 120 83 50 111 30 | 1127 | 26.57 |
| E: AFTER THE PLAN: changes one thing in a good recipe; record starts with 0b's finds | **4.989** | 4.69 5.16 5.11 5.26 4.72 | 4.54 | 88% | 39 | 106 1 33 85 2 | 786 | 18.63 |

Seconds and watt-hours are rough: other jobs (the timing pass, page checks, the loops below) ran on the machine during some arms, which stretches them. Grades are not affected.

By the rule fixed in the plan (higher on average and in at least 4 of 5 paired runs):
- 1. The checker is worth something (A+ over A): **yes** (average +3.480, higher in 5 of 5 paired runs).
- 2. Feedback helps (B over A+): **yes** (average +0.229, higher in 5 of 5 paired runs).
- 3. Keeping what worked helps (C over B): **no clear difference** (average -0.391, higher in 1 of 5 paired runs).
- 4. Facing against the top list (D over C): **yes** (average +0.401, higher in 5 of 5 paired runs).
-    and the other way (C over D): **no clear difference** (average -0.401, higher in 0 of 5 paired runs).
- 6. Not decoration (A+ over random recipes 0b): **no clear difference** (average -0.563, higher in 0 of 5 paired runs).
- 6. Not decoration (B over random recipes 0b): **no clear difference** (average -0.334, higher in 1 of 5 paired runs).
- 6. Not decoration (C over random recipes 0b): **no clear difference** (average -0.726, higher in 0 of 5 paired runs).
- 6. Not decoration (D over random recipes 0b): **no clear difference** (average -0.324, higher in 1 of 5 paired runs).
-    A+ over random card orders 0a: **no clear difference** (average -0.193, higher in 1 of 5 paired runs).
-    B over random card orders 0a: **no clear difference** (average +0.037, higher in 2 of 5 paired runs).
-    C over random card orders 0a: **no clear difference** (average -0.355, higher in 1 of 5 paired runs).
-    D over random card orders 0a: **no clear difference** (average +0.046, higher in 3 of 5 paired runs).

After the plan (exploratory, same rule applied):
- The model as a changer of good recipes (E) over the random recipes it started from (0b): **no clear difference** (average +0.142, higher in 3 of 5 paired runs).
- E over the top-list arm (C): **yes** (average +0.868, higher in 5 of 5 paired runs).
- E over facing (D): **yes** (average +0.467, higher in 4 of 5 paired runs).

Best single try in each arm: 0a: `(a card order)` 4.499 (9, 18, 37, 75, 141, 261); 0b: `min(3, (t + (d(2) == d(1))))` 5.161 (8, 18, 40, 96, 192, 416); A+: `-mod(t+o+z*(t==0?1:0), n-2)*max(1, (n-3)*(n-2)/2 + (n-4)*(n-3)/2)` 4.482 (8, 16, 40, 79, 152, 284); B: `n*(n-1)*(n-2)/6 + z*o*t - (w==n) * 0 - (z==n) * (o==n) * (t==n) * 0` 4.733 (8, 20, 40, 79, 154, 306); C: `-(n<6)?(o==t&&o!=0?2:-1):min(o,t)*3+min(o,t)-1` 4.548 (8, 17, 33, 78, 167, 344); D: `-(z+o+t)/2 + max(0, z*o*t/4)*min(z+o+t, 4) - (n==8)*(z*o*t + z*o + o*t)*0.5` 4.819 (8, 20, 40, 79, 154, 350); E: `((min(d(1), d(1)) + last - 1) < t && (s > 3 || s < 5) || (last == 0 && n != 8) && last != 2) && last != 1` 5.255 (9, 20, 40, 88, 196, 384).

### Arm F: a frontier model alone (GPT-6.2 Sol through Codex), one try, no checker, told to run no code

- (frontier-kimi-1.out: not finished)
- (frontier-kimi-2.out: not finished)
- (frontier-kimi-3.out: not finished)
- 695 characters, 41,748 tokens, no commands run. By the grader as committed: unreadable (too long). With the grader's length cap lifted: **grade 5.912** (9, 20, 45, 112, 224, 493).
  `(n==3 ? mod(d(0)*d(0)+d(1)*d(1)+3-last,3)==0 : n==4 ? w>0 && mod(w+min(last,1),3)==0 : (n==7 ? last<2 : n==8 ? last==min(d(5),1)+min(d(6),1) || (d(6)==0 && d(5)<2 && last==d(5)+1) || (d(5)==0 && d(6)==1 && last==0) || (d(5)==1 && d(6)==2 && ...`
- 796 characters, 34,273 tokens, no commands run. By the grader as committed: unreadable (too long). With the grader's length cap lifted: **grade 5.916** (9, 20, 45, 112, 225, 493).
  `(n==3 ? d(2)==(d(0)!=0)+(d(1)!=0) : n==4 ? (w==3 && d(3)==0) || (w==2 && d(3)!=0) : (n==6 || n==7) ? (n==7 && last==2 ? w==1 : (w-(n==7 && last!=0)==6 && mod(t,2)==(n==7 ? last : 0)) || (w-(n==7 && last!=0)==3 && (((d(0)*d(1)!=0)+(d(1)*d(2) ...`
- 408 characters, 14,359 tokens, no commands run. By the grader as committed: unreadable (too long). With the grader's length cap lifted: **grade 5.635** (9, 20, 45, 112, 225, 349).
  `(n==3 ? mod(d(0)*d(0)+d(1)*d(1)+3-last,3)==0 : n==4 ? (last==0 ? w==3 : w==2) : n==7&&last==0 ? w==0 : n==8&&d(n-2)*last==0 ? w==1 : z==0&&(n!=5||mod(7-d(0)-d(1),3)!=0) ? mod(t+(n==5&&mod(7-d(0)-d(1),3)==2 ? 1 : 0),2)==0 : z+(n==5&&mod(7-d( ...`

Average of the 3 finished shots: **5.821** with the length cap lifted (0.000 by the grader as committed; the cap of 300 characters was in the grader and was never told to any model, see the note at the end of `llm/PLAN.md`).

### An open big model alone (Kimi K3.1 Pro), one try, no checker, told to run no code

- grade 4.014 (8, 16, 32, 64, 128, 256): `-abs(s-n)`
- grade 4.742 (9, 18, 36, 81, 162, 324): `(n==3 ? (d(2)==(d(0)*d(0)+d(1)*d(1))%3)*1000-t : n==4 ? ((d(2)==(d(0)*d(0)+d(1)*d(1))%3)&&d(3)<2)*1000-t : n== ...`
- grade 4.833 (8, 20, 40, 84, 168, 304): `-abs(2*t-n)`

Average of the 3 shots: **4.530**. This way did not get the open big model to the closed one's level (5.82). It has not yet been given the checker.

### After the plan: a cheap loop on top of the big model's answers (exploratory, not pre-registered)

No model runs here. Each recipe the frontier model wrote keeps picking its cards first; the loop tries 800 random tie-breakers for the order of everything else, then small changes to the numbers inside the recipe, and keeps a change only when the exact checker says the grade went up. 131 seconds of one processor core in all.

| the big model's recipe | its own grade | after the loop | piles after (3 to 8 features) |
|---|---|---|---|
| sol-1 | 5.912 (9, 20, 45, 112, 224, 493) | **5.912** | 9, 20, 45, 112, 224, 493 |
| sol-2 | 5.916 (9, 20, 45, 112, 225, 493) | **5.963** | 9, 20, 45, 112, 236, 493 |
| sol-3 | 5.635 (9, 20, 45, 112, 225, 349) | **5.883** | 9, 20, 45, 112, 236, 452 |

The loop raised 2 of 3 recipes. Best grade before the loop 5.916, after 5.963. Best piles known: 9, 20, 45, 112, 236, 512.

### After the plan: the deeper loop (exploratory)

The same idea for 8 minutes per recipe, with more kinds of small change (a number, a comparison, an and/or, a plus/minus, a name), one at a time at every spot and then in random pairs. Still no model.

| the big model's recipe | alone | after the first loop | after the deeper loop | piles after | changes tried | changes kept |
|---|---|---|---|---|---|---|
| sol-1 | 5.912 | 5.912 | **5.912** | 9, 20, 45, 112, 224, 493 | 22,013 | 0 |
| sol-2 | 5.916 | 5.963 | **5.963** | 9, 20, 45, 112, 236, 493 | 18,792 | 0 |
| sol-3 | 5.635 | 5.883 | **5.902** | 9, 20, 45, 112, 236, 462 | 22,309 | 1 |

63,114 changes tried, 1 kept. This way is nearly used up: small changes of these kinds find almost nothing more. The gap that is left is on the 6,561-card deck (best here 493, best known 512).

### After the plan: a second big model holding the checker (GPT-6.2 Astra, exploratory)

Astra was handed the best recipe so far (5.963) and the exact checker, with up to 40 graded tries. It returned a 733-character recipe after 1 graded try and 45,570 tokens: **grade 6.000 of 6** (9, 20, 45, 112, 236, 512), the best pile known on every deck. Re-graded here by the same checker. Astra says it translated the published FunSearch 512-card construction (Nature, 2023) into the recipe language, so this matches the best known and does not beat it.

The path on this puzzle today: the big model alone 5.82, plus a cheap no-model checker loop 5.96, plus a second big model holding the checker 6.00.
