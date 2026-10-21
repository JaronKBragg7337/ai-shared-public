# Jaron's opening playtest, first pass (10/4 1:26 PM, iPhone Safari) - fix list, build PAUSED
Screens beside this file (6). His full written notes come later from a second walkthrough.

## From Jaron
1. Skiff/lifeboat: the engine nozzle sits in the hatch where the ramp drops - ramp down = nozzle floating in the doorway (1191d511).
2. Port walls: wall pipes/columns, rails and boards cover doors (4c8676a4 pipe through Medbay door; 42655e55 board in front of a door; 5659ccdf glass partition cuts across a door frame).
3. Every door is labelled MEDBAY except two; there is one medbay. Each door needs its real name.
4. Digging the crate at the crash site on the new world: the first dig showed Mars soil, not that world's soil.
5. Players need hints (onboarding) - from earlier.

## Seen in the same screens (Claude)
6. Skiff flight deck (1c4db886): blob seats with pink sticks, faceless grey mannequins, a floating blank white panel - far below the Meridian bar.
7. Arrivals/departure boards show bars, not text (42655e55) - placeholder.
8. Boarding hall seats (5659ccdf) are blocky boxes.
9. Skiff at night (1191d511): no ground visible around the pad, ship reads as floating in black.
10. Hellas Dawn hull: pale-blue blank panel + flat cream windows (from earlier screens).
11. Older polish: dark Kestrel ceiling, Ceres too tan, terrain tear, blue streak in the sky.

## For the fix round
One screen-by-screen phone pass (eyes, not just taps) for anything covering a door, path or button.

## Jaron 1:32 PM - more
12. Getting off the Hellas Dawn: the side door was hard to find (all doors say MEDBAY). The side gangway ramp is invisible -
    you float down. First arrival on Mars should be a real ramp you walk down.
13. The cargo bay at the back opens too: invisible ramp, and looking back the ship is see-through/empty from outside
    (59b59453: shelves and doors hanging in the air, no hull). You can't walk off that way - so that door shouldn't open,
    or the hull must be solid.
14. No hint where the arrivals hall is. He explored first (as a new player would), didn't know the trade hall was the place,
    found it on the second play right in front of the ship. Wants guidance; NOT more floating stuff on screen. Idea: a
    pointer to the current goal, on the planet only. (Options to offer: lit path + big sign over the hall door + a crew
    voice line; a small edge arrow only after wandering ~1 min.)
15. Rover ride: one stretch dipped under a layer of the ground. The planet should be one solid surface.
16. After arrival (game start): far too dark - no idea where to go. The landing pad is a distance from the buildings.
    Night is fine, but a settlement needs lights: lit buildings, pad lights, path lights, so it reads as a place at night.

## After Grok looks r1 went live (Jaron 4:39 PM)
17. The new departure board on the Ares promenade stands in front of a door (sent to Sol's resume).
18. Skiff cockpit: from the front window looking back, a big tan slab covers everything - can't see the cabin or the door (sent to Sol). Seats still blocky - looks round 2.
19. Control tower elevator doesn't work during the opening (he went to find the old tower quest). And: what does a player
    who chooses "stay on Mars" (peacekeeper) do next - is there a first mission? (sent to Luna's stale audit)

## Jaron 10:31 PM, live after fix rounds 1-2 (got through the opening to Ceres with no issues he remembers)
20. COURSE freezes the game.
21. Red "CANN(OT...)" in the flight bar is cut off behind Ramp/Course.
22. Can't lift off and doesn't know why (drained lifeboat needs 2 parts - the game doesn't say so).
23. Doesn't know when/where to hire crew.
24. Skiff cockpit: something still through the seats.
25. On the new planet: no idea what to do or where a mission is.
(20-25 sent to Sonnet fix round 3)

## Fix round 3 LIVE (cf5fc5d, 11:40 PM): settings layout, empty boot button, opening dig ring + aim, COURSE freeze (Ceres course list crash), readable can't-lift reason + NEXT line, Skiff seat post.
Design gaps found (for when the build resumes): Ceres has no job board; crew hiring exists only on Mars; peacekeeper ("stay on Mars") first mission unknown - see Luna's stale audit.

## Stale cleanup LIVE (10/5 ~1:55 AM): Ore Lane / lane fees / jump-drive text + voices removed; Ceres Lane Office -> Flight office; solo board honest (solo starts at Mars); "stay on Mars" next step -> tower lift + watch supervisor's paid job.
Still to check: Jaron couldn't use the tower lift during the opening, but code shows nothing disabling it - needs his eyes or a repro. Bot still logged one opening dig tap with no cut (real taps cut in round 3). One Deimos trip-timing test failing (not touched by this change). Playtest: 0 blockers, 2 serious (bot walking), 12 total.

## Jaron 10/5 7:33 PM (stayed on Mars, fresh private-browser character) - screens ff2cc24d, ccbeae39, c08ac408
26. BLOCKER: NEXT says buy a power cell from the Salvage trader and a fuel coupler from the Field kit trader - neither shop
    stocks them (Salvage: spare parts kit, ammo box; Field kit: O2 cylinder, spare parts kit). Can't fix the lifeboat.
27. Hiring only exists if you stay on Mars; hire candidates are nowhere to be found during the intro. World feels empty.
28. Skiff flight deck: the big tan slab still cuts across the console/seats (ff2cc24d) - round 3 did NOT fix it.
29. People walk backwards toward the ship - they never turn to face where they walk (only correct when seated).
30. Crew-flown ship: flies very low, weird, and BACKWARDS.

## Fix round 4 LIVE (9e912f9, 10/5 ~8:25 PM): parts buyable at Salvage/Field kit (+ Ceres), Skiff roof hidden aboard (slab gone, checked in real GL), NPCs face their walk, crew pilot climbs to 260 m + no tail-first, arrow to Crew Hall after the lifeboat is fitted.
Needs Jaron's eyes: Buy buttons on phone, NPC walking, crew-flown ship direction ("backwards" not reproduced headless).
