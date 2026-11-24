# 3D Reading Room report

All four rooms are playable as a first-person walk. The switches, lamps, live plates and floor wires come from the existing room lists. A solved door swings open and lets you walk through. The shelf’s three books teach the marks, replay your flips and rebuild the room’s machine from its code.

I put timber beams and pendant lights in the first frame and tipped the starting view slightly toward the room. I gave Room 2’s door card enough space for the full explanation, fixed which book each physical tap opens, and made reduced-motion flips update the door immediately. I removed the two unused `.part.js` files. The code book reads the generated SVG shapes. The wall plates use the same marks and layout on canvas.

## What passed locally

`node reading-room-3d/test-walk.mjs --shots=all` finished with **148 passed, 0 failed, and 44 screenshots**. Both browsers completed all four rooms through real browser input, including finger drags, lever and book taps, and walking through each opened door. The checks covered walls, the shut door, the travelling wire light, reduced motion, the marks and words, “Same room,” and the final results. Both runs had zero page errors and fit the phone width. In Room 2, turning every switch on left the door shut at a sum of 1, and its full explanation fit without scrolling.

| Room | Test flips | Fewest | Random flips on average |
| --- | ---: | ---: | ---: |
| 1 | 2 | 2 | 4.0 |
| 2 | 4 | 2 | 9.0 |
| 3 | 5 | 3 | 20.3 |
| 4 | 4 | 4 | 41.7 |

Room 2’s run includes trying every switch on. Room 3’s run includes flipping a switch on and back off to check E and Enter, and one request for the words.

| Browser | Viewport | First room ready | Most draw calls sampled | Most triangles sampled |
| --- | --- | ---: | ---: | ---: |
| iPhone-profile WebKit 26.6 | 375 × 812 | 590 ms | 106 | 8,116 |
| Edge 158.0.4370.33 | 390 × 844 | 2,574 ms | 123 | 9,712 |

I checked the room views, plates, doors and books in the screenshots. Lamp A’s wall marks were readable at about 2.2 m and still clear across the aisle at about 3.6–3.7 m, with the card hidden. All 44 PNGs passed a file check. The screenshots are in [screenshots/](screenshots/).

The browser tests used Three.js r182 from the local World 2 remake copy at `C:/Users/lilli/AI-Shared/scratch/world2-remake/phase3/three/build`. Physical iPhone performance, two-thumb comfort, the public page and CDN, and direct clipboard copying on HTTPS remain unverified.

**Next thing**

Check Room 1 on a real iPhone, starting by walking and looking with both thumbs at once.
