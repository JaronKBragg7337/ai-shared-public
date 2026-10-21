# SPOILER - builders only. Jaron designed the opening's shape himself (10/3 10:46 AM) and that shape is public in BIBLE-v3.md
# section 10.1. What stays in here are the surprise details he has not played: what is in the wreck, who the driver is, what
# waits at the port, the per-season crash causes, and the money numbers. Keep all of that out of anything he reads.

## The shape (public, from the bible; repeated so this file stands alone)
1. Transport to Mars with huge ships beside you. Walkable passenger deck.
2. Normal landing at Marineris Port. Walk into the arrivals hall.
3. The board: every world and faction, pictures, plain lines, live numbers. Pick a world and a faction, or a world and no side.
   Staying on Mars with no side is allowed (walk out of the port; today's start).
4. Transport to the chosen world. It crashes on the way down. The cause changes each season.
5. Climb out a few km from the nearest port. Dig, carry, salvage. A rover comes. Ride to the port.
6. Build your way back to space: earn the first ship.

Jaron's older Mars-crash design (the freighter that comes down in the desert) is now simply the Mars version of beat 4 and 5, kept
for players who crash on Mars in a season where that is the cause. The Meridian-at-the-port start keeps working until the new
opening is built.

## The surprise details (not public)

### The wreck
- Tilted cabin, emergency lights, a dead crew member's locker you can open (a photo, a name, a note: the game's first small story).
- A supply crate buried under collapsed material: the first real dig. Inside: a hand tool, a day of air and water, a beacon.
- The transport's **lifeboat** is intact but drained. Fixing it is the first chain at the port (a part from each of the two
  factions: that is how the player meets both sides for a reason, and the lifeboat is the starter ship on every world).
- The wreck stays in the world as a landmark for that player (seeded per player per season), walkable, with salvage left in it.

### The driver
- One of the world's two factions, random per player, recorded on the player as the first nudge. Pitches their side on the ride.
  The other side's recruiter is waiting at the port and makes the counter-pitch before the player leaves the pad.
- On Mars (no side): a port worker. Mars players are recruited later by the station factions and by passing players.

### At the port
- The settlement from the transport line: the purse (below), a pad, the lifeboat towed in.
- On a far pad stands the ship to earn one day: whichever side the driver was NOT (Fortis gunship or Technos research vessel on the
  Moon; Ironclad rig or Greenhaven living-hull merchant on Ceres; Skyward lifter or a Homeguard armoured hauler on Earth; a Mystara
  research vessel or a prospector's rig on Callisto; the Meridian on Mars), so the player sees both sides in the first ten minutes.

### Per world
| Beat | Mars | The Moon | Ceres | Earth | Callisto |
|---|---|---|---|---|---|
| Nearest port | Marineris Port | Tranquility Civil Hub | Kerwan Landing | The launch site of the continent they chose | Valhalla camp |
| The crash site | Red desert, dust through the hull, butterscotch glow | Crater floor on the terminator: half in hard sun, half black; no dust, a slow spray of frozen coolant, a suit timer from the moment the hull opens | Grey-white salt and ice, 0.28 m/s2 so every step floats, frost haze from the vented water tank | Real ground from the data: a coast, a plain, a forest edge; rain; the first sky with weather | Ice and dark rock, Jupiter filling half the sky, radiation counter ticking slowly |
| What you dig | The crate out of collapsed dust | The crate out of low-g regolith; teaches the moon hop | The crate out of ice-rich regolith; the first lot is water, which is money here | The crate out of mud; teaches that Earth ground is heavy and wet | The crate out of ice; teaches the suit's heater |
| The driver | A port worker | Fortis trooper in red-trimmed armour, pressurised rover; or Technos technician in white, glass-cabbed rover | Ironclad shift boss in hi-vis, mine crawler; or Greenhaven medic in green, farm hauler | Homeguard ranger in a truck; or Skyward launch tech in a crew bus | Mystara researcher in a sealed crawler; or a prospector from the open-seat camp |
| Local money | marks | lunars | shares | dollars | credits (no local money yet) |

### Per-season crash causes (rotate; never the same two seasons running)
1. Solar storm: comms die, guidance fails, alarms (the first taste of COMMS FALL, never named). The season's storms follow.
2. Meteor: a strike on the hull, decompression, a hole you can look out of. That season has meteor falls on the home worlds.
3. Pirate hit: the Corsairs board the transport for its cargo; the player hides; the transport is shot down after. The season's
   pirates are bolder.
4. Failed part: a drive fault, a controlled crash, the crew's fault; the line pays more in settlement. A quiet season.
5. Bad landing in weather: dust storm on Mars, hurricane on Earth, ice fog on Ceres. The season's weather is heavier.
If several players start in the same window, they crash in the same event and can find that out later.

## Money at the start (Claude, 10/1 2:37 PM; still the numbers)
- The transport line's survivor settlement is the starting purse: **2,500 credits** in the local money (Mars marks: 1 credit =
  4 marks). Plus the lifeboat once fixed.
- Wages per Mars sol from the ship account: pilot 140, captain 180, navigator 110, gunner 90, comms 100 credits/sol. Signing fee =
  1 sol's wage. Unpaid crew leave at the next port. Replacing a crew member who died costs a fresh signing fee.
- Regolith sells at the depot for 3 credits/tonne (raw) and more once compacted into blocks; a full hopper (48 t) is a day's honest
  work, a bit more than one gunner's wage.

## Rules for whoever builds it
- One script, one set of beats and timings. One `dialogue.js` per world, same keys. The crash cause is a season setting the script reads.
- The driver's faction is random per player and recorded on the player: a nudge, never a lock.
- The big transports (SH15) must be walkable and must fly past real ships with real names on the way in.
- Nothing from the "surprise details" section goes into the bible or anything Jaron reads until he has played it.
