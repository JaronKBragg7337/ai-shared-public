# Homes - every account gets its own place (idea, Jaron 2026-09-26 9:40 AM)

Each account gets its own personal page that is a home - a house or apartment, NOT a game world. Multiple rooms, an upstairs
and a downstairs, a balcony looking down onto the living room. The feel of a very successful person's place - a streamer's home.
Private by default, but the owner can **invite friends** in to hang out, customize, upgrade, and **watch Heartbeat TV together**
(the TV and the home are one idea: Jaron pictured someone on a couch flicking channels).

## Why now
- ARC Raiders is adding private outposts in its October update - private customizable space is trending; this gives people a
  calmer place to step into.
- Younger viewers watch streamers like IShowSpeed partly for the background - the setup, the lifestyle. A home that looks like
  that, that friends can visit, is aspirational in the same way. Jaron's kids would love it.
- Learned from Livi and his mom: people value a private space they own and can invite others into.

## Pieces that already exist - re-check before reusing
World 1 (the hub / Engine / Town Square - one world, three names) already has small apartments you can invite people to with a
code. Built by older models: audit the ownership, invite and persistence logic before reusing any of it. Start fresh as a page per
account, not inside a game world.

## Built 2026-09-26 - The Loft (v1)
- Page: `/homes/` (site repo `homes/index.html`, `homes/homes.js`, assets `homes/loft/`). Phone app "My Loft"; home-page card.
- How the realism works: the whole loft is modelled by script in Blender (`AI-Shared/projects/homes/blender/loft.py`), lit in
  Cycles (real bounced light, city panorama through the glass), and the light is **baked** into 4 atlas textures
  (floor / shell / living / upper, 4K desktop, 2K phone). The browser draws those unlit, so a phone gets path-traced lighting at
  full frame rate. The view out the windows is `city.py`, an 8K 360 render of a procedural city at blue hour.
- The TV is the real `/tv/?embed=1&ch=N` page placed on the wall (CSS3D), so it plays every channel, News included. It hides
  itself when a wall is between you and it.
- Walking: AABB colliders exported from Blender (`colliders.json`); stairs are real steps.
- Friends: signed-in owners get `my_home()` -> an invite link `/homes/?invite=<16 hex>`. Visitors join a Realtime channel named
  by that code and appear as avatars with name tags. "New link" rolls the code (old links stop working).
- Old World 1 apartments were audited: 6-digit never-changing room codes = guessable; not reused.
- Next: customization (swap sofa/art/colors), sit on the couch, voice chat, more home models (house with yard), bake per theme.

## Realism list for the Loft (Jaron 9/27: "the only reason I haven't showed the loft off yet")
1. **Realistic characters instead of capsule "blobs"** for you and visiting friends (real-time web characters - MetaHuman-derived
   or similar, with LODs light enough for phones; check the MetaHuman licence for use outside Unreal first).
2. **Sitting in seats**: walk up to the sofa / chairs and sit (seat anchors + sit pose), so friends can watch the TV together.
Status 2026-09-27 night: BOTH SHIPPED (v1).
- People: 7 Epic MetaHuman presets (Isaiah, Ada, Jorge, Sunita, Zuri, Walter, Aoi). Licence checked: since 2025 MetaHumans may be
  used in any engine (free under $1M/yr; no AI-model training on them). Pipeline: `necklace-unreal/loft_people.py`
  (LP_PRESET=A,B,C: copy preset, auto-rig, build OPTIMIZED/LOW, export FBX + textures + Epic's stand/walk loops) ->
  `blender/eyes.py NAME` (paints the iris in; system Python) -> `blender/person.py -- NAME --shirt r,g,b --shorts r,g,b [--render]`
  (one skeleton, 322 bones folded to 63, clothes decimated, Idle/Walk copied with the person's own neck/head, Sit pose built,
  ~1.3 MB GLB into site `homes/people/`, listed in `people.json`). Check renders go to necklace-unreal/Saved/LoftPeople/_checks.
- Visitors get a person picked from their name hash; they cross-fade Idle/Walk/Sit. `/homes/?guests=N` seats sample people (local only).
- Seats: couch x3, chaise, gaming chair, 2 lounge chairs, 2 balcony chairs (`SEATS` in homes.js, Blender coords -> three (x,z,-y)).
  Sit button appears near a free seat; on the couch the view narrows to ~48 deg across so the 115" TV (14 ft away) fills the screen.
- 9/28 00:30: MIRROR (full length, south wall at Blender x 6.65, three.js Reflector; you are drawn on layer 1 so only the mirror
  sees you). HAIR = Epic strand cards (necklace-unreal/loft_hair.py exports each groom's CardsAtlas_Attribute; eyes.py --hair
  bakes _<groom>_card.png = colour + R-channel strands as alpha; LOD2 hair / LOD3 beards; page alpha-tests "HairCard_*").
  CLOTHES = long pants + sneakers grown from each body's skin (offset along normals, same skinning; shoes = convex hull per
  foot); Epic's light build has no skin under the shorts, so the shorts stay, recoloured to the pants. GLBs now WebP, 1.2-3.2 MB.
- Polish list: Walter's goatee has no card atlas (still a shell); only tees on top (hoodies/jackets would need modelling);
  no facial animation.
