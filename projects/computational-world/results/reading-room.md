# The Reading Room: what the checks say

Made by `node test-reading-room.mjs` on 2026-11-23T23:07 UTC. Never typed.

| room | switches | words shown | the one setting that opens it | fewest flips (a reader) | flipping blind, average (worked out) | the same, played out 40,000 times | trying every setting, worst case | does turning everything on open it |
|---|---|---|---|---|---|---|---|---|
| 1 | 2 | yes | 1, 2 on | 2 | 4 | 3.993 | 3 | yes |
| 2 | 3 | yes | 2, 3 on | 2 | 9 | 9.043 | 7 | no |
| 3 | 4 | no, marks only | 1, 2, 4 on | 3 | 20.333 | 20.307 | 15 | no |
| 4 | 5 | no, marks only | 1, 3, 4, 5 on | 4 | 41.667 | 41.5 | 31 | no |

Checks: 106 passed, 0 failed, in Node and in two phone-sized browsers (iphone-webkit, edge) with real taps and walking.

"Flipping blind" is someone who cannot read the things and flips one switch at random each time, starting with every switch off, until the door first opens.
