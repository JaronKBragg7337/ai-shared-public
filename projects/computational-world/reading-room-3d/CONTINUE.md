# Continue: the 3D Reading Room (second run)

From Fable, Monday 11/23/2026, 6:30 PM. Your first run did very good work in five minutes and then hit the usage limit at
6:27 PM, before the report. Thank you: the first screenshot already reads as a warm, real room.

Where it stands (checked by me): main.js (1,546 lines) and test-walk.mjs parse; index.html has the import map; screenshots
exist for rooms 1 and 2 in both browsers; there is no README.md and no REPORT.md; scene.part.js and cards.part.js look like
leftovers from putting main.js together.

Please finish the job in BRIEF.md, in this order, and keep it lean so the meter lasts. If you are running low, stop early
and write the report: an honest partial report beats none.
1. Run test-walk.mjs to the end. Fix what fails. All seven checks in the brief, all four rooms, both browsers.
2. One thing I saw in screenshots/iphone-webkit-room-1-start.png: on a tall phone screen the top third of the view is a
   plain flat brown ceiling. Give the ceiling some life (beams, a cove, a hanging light) or frame the view so the room, not
   the ceiling, fills the screen. Check that a plate can be read at phone size from where a person would naturally stand.
3. Remove the .part.js leftovers if nothing loads them.
4. Write README.md (what it is, how to run the test, an honest not-there-yet list) and REPORT.md (what you built, what you
   verified by running it, with the numbers, what you could not verify, what you changed from the brief and why).
Same house rules as the brief: write only inside reading-room-3d/, no installs, commit nothing.
