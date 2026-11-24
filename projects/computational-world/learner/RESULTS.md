# Path B, piece 1: a fresh learner learns to read the room by looking

Made by `node learner/learn.mjs` on 2026-11-24T01:43 UTC. Never typed. Plan: `learner/PLAN.md`.

200 learners, each starting from nothing, each living through 30 random rooms of its own. No language model: one weighing of five counts and five scored guesses. Everyone plays the same rooms.

## The planned learner

As written in the plan before any run: it looks only while it is opening a door. The four numbered lines are what I expected, written before the run.

| rooms lived through | reading (rooms it never plays) | looks so far | flips to open the door: the learner | a careful watcher (cannot see marks) | fewest possible | flipping blind |
|---|---|---|---|---|---|---|
| 0 | 56.3% | 0 | 3.27 | 3.67 | 1.40 | 5.9 |
| 1 | 55.8% | 30 | 2.52 | 3.69 | 1.40 | 5.7 |
| 2 | 71.4% | 55 | 2.20 | 3.93 | 1.35 | 5.7 |
| 3 | 75.8% | 78 | 1.85 | 3.38 | 1.28 | 5.3 |
| 4 | 76.2% | 97 | 1.89 | 4.21 | 1.45 | 6.3 |
| 6 | 78.1% | 137 | 1.74 | 3.51 | 1.38 | 5.5 |
| 9 | 79.9% | 194 | 1.76 | 3.39 | 1.30 | 5.4 |
| 14 | 83.3% | 288 | 1.72 | 3.39 | 1.36 | 5.7 |
| 19 | 86.0% | 382 | 1.51 | 3.62 | 1.39 | 5.6 |
| 29 | 90.3% | 563 | 1.67 | 3.89 | 1.38 | 5.9 |

Each row is the room played AFTER that many rooms; its reading is tested just before it walks in.

Reading first reached 99% after 20.7 rooms on average, among the 42 of 200 learners that got there within 30 rooms (slowest of those: 29).
What the 200 learners ended up trusting about a filled circle: named 200 ("named" = it follows the thing whose sign is drawn under it, which is the truth).

Reading, split by kind of thing:

| rooms lived through | needs 1, no dark wire | needs 2 or more | has a dark wire |
|---|---|---|---|
| 0 | 45.0% | 75.0% | 75.0% |
| 4 | 86.1% | 59.6% | 60.0% |
| 9 | 89.4% | 65.7% | 63.5% |
| 19 | 93.6% | 77.9% | 72.0% |
| 29 | 95.1% | 87.2% | 81.0% |

The four hand-made rooms of the Reading Room, played by each learner after its 30 random rooms:

| room | fewest flips | learners that used exactly that | average | worst |
|---|---|---|---|---|
| 1 | 2 | 200 of 200 | 2.00 | 2 |
| 2 | 2 | 171 of 200 | 2.48 | 8 |
| 3 | 3 | 199 of 200 | 3.02 | 7 |
| 4 | 4 | 97 of 200 | 6.84 | 24 |

1. Reading reaches 99% within 10 rooms on average: **did not hold** (after 10 rooms: 81.2%).
2. From room 11 on, the learner's flips are within 10% of the fewest possible: **did not hold** (1.62 against 1.38).
3. The watcher does not improve with experience and stays well above the learner: **held** (rooms 1 to 10: 3.71; rooms 21 to 30: 3.64; the learner late: 1.62).
4. Every trained learner opens the four hand-made rooms in exactly the fewest flips: **did not hold**.

## After the plan: the learner that may play

The next way, written into the plan before this ran: once a door is open it stays for as many extra flips as the room has levers, just to look, led by its own doubt. Play flips are counted apart from door flips. The same four expectations, applied to it.

| rooms lived through | reading (rooms it never plays) | looks so far | play flips so far | flips to open the door: the learner | a careful watcher (cannot see marks) | fewest possible | flipping blind |
|---|---|---|---|---|---|---|---|
| 0 | 56.3% | 0 | 0 | 3.27 | 3.67 | 1.40 | 5.9 |
| 1 | 71.4% | 58 | 4 | 2.29 | 3.69 | 1.40 | 5.7 |
| 2 | 79.2% | 112 | 8 | 2.00 | 3.93 | 1.35 | 5.7 |
| 3 | 81.0% | 162 | 12 | 2.00 | 3.38 | 1.28 | 5.3 |
| 4 | 84.1% | 210 | 16 | 1.79 | 4.21 | 1.45 | 6.3 |
| 6 | 88.1% | 307 | 24 | 1.67 | 3.51 | 1.38 | 5.5 |
| 9 | 91.2% | 449 | 36 | 1.52 | 3.39 | 1.30 | 5.4 |
| 14 | 95.2% | 682 | 56 | 1.46 | 3.39 | 1.36 | 5.7 |
| 19 | 96.8% | 913 | 76 | 1.45 | 3.62 | 1.39 | 5.6 |
| 29 | 98.4% | 1368 | 116 | 1.39 | 3.89 | 1.38 | 5.9 |

Each row is the room played AFTER that many rooms; its reading is tested just before it walks in.

Reading first reached 99% after 15.1 rooms on average, among the 158 of 200 learners that got there within 30 rooms (slowest of those: 29).
What the 200 learners ended up trusting about a filled circle: named 200 ("named" = it follows the thing whose sign is drawn under it, which is the truth).

Reading, split by kind of thing:

| rooms lived through | needs 1, no dark wire | needs 2 or more | has a dark wire |
|---|---|---|---|
| 0 | 45.0% | 75.0% | 75.0% |
| 4 | 89.7% | 69.6% | 76.3% |
| 9 | 92.9% | 82.1% | 90.1% |
| 19 | 96.7% | 93.6% | 97.9% |
| 29 | 98.5% | 96.7% | 98.8% |

The four hand-made rooms of the Reading Room, played by each learner after its 30 random rooms:

| room | fewest flips | learners that used exactly that | average | worst |
|---|---|---|---|---|
| 1 | 2 | 200 of 200 | 2.00 | 2 |
| 2 | 2 | 195 of 200 | 2.07 | 6 |
| 3 | 3 | 194 of 200 | 3.07 | 7 |
| 4 | 4 | 185 of 200 | 4.40 | 14 |

1. Reading reaches 99% within 10 rooms on average: **did not hold** (after 10 rooms: 92.8%).
2. From room 11 on, the learner's flips are within 10% of the fewest possible: **held** (1.48 against 1.38).
3. The watcher does not improve with experience and stays well above the learner: **held** (rooms 1 to 10: 3.71; rooms 21 to 30: 3.64; the learner late: 1.48).
4. Every trained learner opens the four hand-made rooms in exactly the fewest flips: **did not hold**.

One of the random rooms, as its own code page (to show what kind of room these are):

```
1 switch
2 switch
3 switch
A lamp needs 1 wires +3
B lamp needs 1 wires +2
C lamp needs 1 wires +B
D door needs 1 wires +C
```
