# MSI data-damage hunt - the team's own job (Jaron 11/24 7:54 AM: no outside repair, ever)

## FOUND and FIXED the same morning, Tuesday 11/24/2026 (Fable): one fast core of the processor gives wrong answers at its top speed. The fast cores are now held at 4.6 GHz.

**FIX IN PLACE since 8:45 AM: the fast cores' top speed is capped at 4,600 MHz. With the cap the yardstick read 0 failures
of 1,368; minutes before the cap it read 36 of 948. Check it: `python tools/msi_speed_cap.py status`. Undo it: `python tools/msi_speed_cap.py off`.**
**KEEP WATCHING: the cap is a Windows setting (an update could wipe it) and a worn core can get worse. The yardstick now
runs by itself every day at 11:30 AM (task "MSI Core Yardstick", about 2 minutes), and the everything check has a row
for the cap. Its three results: CLEAN = good. FAILS = lower the cap (`python tools/msi_speed_cap.py set 4300`) and run
it again. NOT A FAIR TEST = the run was held back, so a clean count proves nothing: find what slowed it, run it again.**
Second safety, still valid (no admin, no restart, tested): make this the first line of a PowerShell job, and the job
and everything it starts stay off the bad core: `(Get-Process -Id $PID).ProcessorAffinity = [IntPtr]4294964223`
(that number is FFFFF3FF = every core except logical 10 and 11). For a scheduled task: `cmd /c start "" /affinity FFFFF3FF /wait <command>`.
The news pipeline has carried that line since 8:40 AM (Claude).
Picture of the finding, phone size: `state/msi-data-hunt-picture.png`.

### In plain words (for anyone learning how a PC works)
- The processor (Intel i9-14900HX) is one chip with 24 small engines in it, called cores: 8 fast ones and 16 small ones.
  Windows counts 32 "logical" cores, because each fast core can do two things at once and shows up twice (numbers 0-15);
  the 16 small cores are numbers 16-31.
- One fast core, the one Windows calls logical 10 and 11, sometimes gets a sum wrong. Only when it runs flat out,
  above about 5.1 to 5.3 GHz (GHz = billions of steps a second). At 5.04 GHz and below it was right every time.
- The chip only lets a core run flat out while the rest of the chip is resting. So the fault bites a LONE job on a
  QUIET machine: one ffmpeg reading a picture, one Python job reading Sapling's memory, Google Drive tidying its index,
  Windows compiling something in the background. When the whole machine is busy (the nightly self-test, anything using
  every core) all cores run slower, about 4.0 to 4.4 GHz, and that core is right again.
- Windows ranks that core as one of its two favourites for a lone job (only logical 8-11 carry rank 2), so lone jobs
  land on it again and again. That is why it looked like "files read soon after they were written": a small job that
  starts right after a big one ends, on a machine going quiet.
- It is not the memory sticks, not the disk, not heat by itself (it was right at 97 C when running slower), and not
  ffmpeg (the same ffmpeg file has been on the MSI since June; other programs were hit too).

### The measurements
One PNG picture the size of a video frame, made by the test so every byte is known, checked good by Python's own
decoder and by PIL. Then the real ffmpeg decodes that same good file over and over. A healthy machine: 0 failures, always.

| What was tried | Result |
|---|---|
| Windows picks the core (normal use) | 30 of 60 failed ("inflate returned error -3", the same words as the news failures; 1 was a crash) |
| ffmpeg told to use one thread | 39 of 60 failed (so it is not ffmpeg's threads tripping over each other) |
| Held on the 8 fast cores | 21 of 60 failed |
| Held on the 16 small cores | 0 of 60 failed |
| Held on ONE logical core at a time, 24 tries each | logical 10: 4 failed. logical 11: 17 failed. Each of the other 30: 0 failed |
| Every core EXCEPT logical 10 and 11 | 0 of 300 failed |
| Logical 11, nothing else busy, running 5.29 GHz | 20 of 50 failed |
| Logical 11 with 1 to 6 other fast cores busy, running 5.04 / 4.87 / 4.69 / 4.44 / 4.36 / 4.32 GHz, heat zone 97 C | 0 of 300 failed |
| A healthy fast core (logical 2) alone at 5.36 GHz | 0 of 20 failed |
| One long ffmpeg run on logical 11 (the same picture 400 times) | 44 failures spread through the whole run; on logical 10: 1; on a small core: 0 |
| Video encode (x264, one thread, 90 test frames) held on logical 10 | 29 identical, 1 came out DIFFERENT with no error shown. On a small core: 6 of 6 identical |
| Python work with known answers held on logical 11 and 10 (what integrity_test.py runs) | 0 wrong of 378. Same inflate as 100 separate short Python programs: 0 wrong |

Windows' own map agrees that logical 10 and 11 are the two halves of one physical core, class "fast", scheduling rank 2.

Why the nightly self-test came back clean six times: it loads every core at once (so that core runs slow and right),
and its Python checks do not trip the fault even at top speed. ffmpeg's and x264's machine code does. The fault depends
on which exact steps the core is asked to do, which is typical of a worn or weak spot inside a core.

### What this explains
- ffmpeg "inflate returned error -3" on news frames (11/22, 11/24) and on the just-written logo (11/24 6:31), and
  ffmpeg's crashes in the Windows log (11/16, 11/17, 11/22, 11/24).
- The map-briefing videos with single bytes wrong and no error (11/22): the silent wrong encode above.
- Sapling's one bad memory row that parsed fine afterward (11/21): a lone Python job.
- Very likely Google Drive's index going "corrupt" only inside the running program, even on the slow gentle fill
  (a quiet machine is exactly when that core runs flat out). Not proven; Drive may have its own bug as well.
- Likely the other odd crashes in the Windows log: the .NET background compiler three times on 11/22, the audio engine,
  two Windows Update helpers at 4:14 AM on 11/24. And possibly the two whole-machine crashes (10/11, 10/31). Not proven.

### What is not established
- WHY the core went bad. Wear is the best guess: the chip is the same design Intel had the 2023-24 wear problem with
  (Intel says laptop chips were not affected); its patch level ("microcode") is 0x116 from mid-2023, older than every
  fix Intel shipped (Intel says 0x12F or later); the MSI runs day and night; the chip sits near 68 C idle and jumps to
  90-97 C on light work. And the same ffmpeg worked from June until its first crash on 11/16. That fits wear. It is not proof.
- Whether it will spread or get worse. Assume it creeps: the speed at which the core starts failing may come down.
- Whether a speed cap cures it. The slow-speed readings above came from keeping neighbour cores busy, not from a cap.
  A cap has to be tested with the yardstick after it is set.

### Fix A as done and measured (8:45 to 8:55 AM)
Jaron to Claude: "Go for what you think would work. If you need to use the fable chat go for it." Claude handed fix A to Fable.
`python tools/msi_speed_cap.py set 4600` sets one Windows power setting, "Maximum processor frequency" for the fast
cores, for plugged-in and battery. No admin rights, no restart. Before: no cap.

| Measured | Without the cap | With the 4.6 GHz cap |
|---|---|---|
| Speed of the bad core working alone | 5.23 to 5.27 GHz | 4.48 GHz |
| Bad core alone: logical 11 / logical 10 | 8 of 30 / 2 of 30 failed | 0 of 60 / 0 of 60 failed |
| Yardstick, Windows picks the core | 9 of 60 failed | 0 of 200 failed |
| Yardstick, fast cores only | 12 of 60 failed | 0 of 200 failed |
| Yardstick, ffmpeg on one thread | 39 of 60 failed (8:26 AM run) | 0 of 200 failed |
| Yardstick, each of the 32 cores, 24 tries | logical 10: 5, logical 11: 10, others 0 | all 0 |
| Whole yardstick | 36 of 948 failed | 0 of 1,368 failed |
| Video encode (x264) on the bad core; every result must match | 1 of 60 came out different, no error shown | 200 of 200 identical (100 on each half); one long run of 400 decodes on each half: 0 errors (without the cap: 44 and 1) |
| Heat zone during lone jobs | 88 to 94 C | 78 to 82 C |

What the cap costs, measured (see the next part): a lone job that runs flat out on a fast core takes about 22 percent
longer. (My first estimate, "at most about 13 percent slower", was too low.) A busy machine loses nothing: with the other
fast cores at work the chip already ran 4.4 GHz.
What the cap does not do: it does not heal the core and it does not stop wear. BIOS E15M2IMS.912 and cooler running
(C and D below) are still worth doing.
Not checked yet: that the setting survives a restart and Windows updates (it should; no restart was done), the news
render time with the cap, and Google Drive's index (a fresh index that holds now would be an independent sign the fix is real).

### What the cap costs and what it does to heat (measured 8:54 to 9:00 AM, cap in place, nothing changed for the test)
**Cost.** The same lone job timed before and after: one ffmpeg run that decodes the same picture 400 times, held on one core.

| Core | Without the cap (8:33 AM) | With the 4.6 GHz cap |
|---|---|---|
| Logical 10 (the bad core) | 10.4 s | 12.6, 12.9, 12.7 s |
| Logical 11 (its other half) | 10.7 s, with 44 errors | 12.6, 13.1 s, no errors |
| Logical 2 (a healthy fast core) | not timed | 12.4, 12.5, 12.5 s |
| Logical 20 (a small core; the cap does not touch it) | 19.3 s | 19.3, 19.3 s |

So a lone job that runs flat out on a fast core takes about 22 percent longer (10.4 s became 12.7 s). The small core took
exactly the same time before and after, which says the two timings can be compared. The "without" column is one run each.
Jobs that use many cores at once are not slowed: the chip already ran them below the cap.
If the speed is missed: the bad core read right at 4.87 and at 5.04 GHz too (50 tries each, see the table above), so a
cap of 4,800 or 5,000 might be enough and would cost about half as much. That needs its own long yardstick run first,
and it leaves less room if the core wears further. The other way to get the speed back is fix B (take that one core out
of use and lift the cap), which needs admin rights and a restart.

**Heat.** Heat zone, one reading every 2 seconds:

| When | How busy the processor was | Heat zone |
|---|---|---|
| Before the cap, three quiet moments (8:11, 8:28, 8:38 AM) | 3 to 5 percent | 66, 68, 69 C |
| Before the cap, light work (8:11 AM, 20 readings) | 9 to 16 percent | 74 to 91 C, mostly 87 to 91 |
| With the cap, ordinary running (8:54 AM, 75 readings over 150 s) | 16 to 33 percent, average 22 | low 68, middle 71, high 78 C; none above 80 |
| With the cap, quiet (10:55 AM, the 15 of 45 readings at 6 percent busy or less) | 4 to 6 percent | low 65, middle 68, high 71 C |

The resting temperature did not change: about 68 C, before and after. That floor comes from the fans and the cooling, not
from the top speed. What changed is the spikes: light work used to push the chip to about 90 C within a second, and now
the same kind of work stays in the 70s. The MSI was not fully idle during the "with the cap" sample (something else was
using about a fifth of the processor). The quiet reading was taken at 10:55 AM (last row): 65 to 71 C, middle 68, the same
as before the cap. All 45 readings of that minute and a half, processor 4 to 17 percent busy: 65 to 72 C.

### The daily yardstick: its first scheduled run went wrong, and what that taught (9:38 to 10:52 AM)
**What happened.** Claude made the yardstick a daily job (task "MSI Core Yardstick", 11:30 AM). Its first run by the
Task Scheduler, at 9:38 AM, took 29.9 minutes instead of 2, and said CLEAN. Claude doubted that clean (a run that slow
may never have reached top speed) and handed it over. The doubt was right. There were two causes, and both are measured.

**Cause 1: a console for every launch.** The task starts the yardstick with pythonw, which is Python without a window.
ffmpeg is a console program. Started from a windowless program it gets a brand-new console every time, and on this
machine every new console became a tab in the Windows Terminal program. 1,008 ffmpeg launches made 1,008 tabs, and the
terminal could not close them as fast as they came, so each launch waited longer and longer (1.8 seconds a launch on
average; the picture decode itself is 0.1). Counted at 10:12 AM: 516 conhost.exe and 480 OpenConsole.exe running
(normal here: about 40 and 2), the terminal program holding 9 to 11 GB, free memory down to 2 GB of 31.7.
**At 10:15:45 AM the terminal program crashed** closing them (Windows' log: WindowsTerminal.exe, ntdll.dll). Everything
that lived in one of its tabs was closed with it: the MSI connector (back by itself at 10:17:07), Sapling heartbeat and
Sapling relay (restarted 10:23 to 10:28 by the everything check, through their own jobs), and the guard program of the
Cosmos server (restarted by Claude, 10:29 to 10:31). The Cosmos game server itself stayed up the whole time.

**Cause 2: Windows slows down windowless background programs.** A program the Task Scheduler starts without a window
gets slowed by Windows to save power, even on mains power, and so do the programs it starts: about 1 GHz instead of
4.5. (Windows calls it power throttling. Claude guessed it; Fable's first answer, "it is not power throttling", was
wrong.) A program can tell Windows "do not slow me", but that does not pass on to the programs it starts (measured:
the started program reports "nothing decided"), so every ffmpeg has to be told as well.

Measured on a healthy fast core (logical 2), cap 4.6 GHz, 8 launches each way, everything started by the Task Scheduler
through a copy of the daily task, 10:30 to 10:38 AM:

| How ffmpeg is started | Seconds per launch | Speed of the core while it worked |
|---|---|---|
| For comparison, by hand (any of the ways below except "slowed on purpose") | 0.12 to 0.14 | 4.45 to 4.47 GHz |
| Plain launch, the 9:38 way (a console for each ffmpeg) | 0.19 to 0.25 | 2.0 to 3.7 GHz |
| "No window" | 0.40 to 0.43 | 1.0 to 1.2 GHz |
| "No window", only the yardstick told "full speed" | 0.30 to 0.39 | 1.5 to 2.2 GHz |
| "No window", the yardstick and each ffmpeg told "full speed" | 0.15 | 4.03 to 4.09 GHz |
| **No console at all, both told "full speed", ffmpeg paused until it has been told (the fix)** | **0.115** | **4.47 to 4.48 GHz** |
| Slowed on purpose (both told "save power") | 0.41 to 0.43 | 1.0 GHz |

(The plain-launch row was measured after Claude's 10:27 AM change, see below, so without the tab pile. The step from
4.05 to 4.47 GHz: with "no window" Windows still starts a small hidden console helper beside every ffmpeg, and that
helper is slowed too.)

**So the 9:38 AM "CLEAN" was not a fair test.** Started that way, ffmpeg runs at roughly 2 to 3.7 GHz (the speed was
not measured during that run itself). That is below the 4.5 GHz the fast cores run in daily use, and far below the
5.1+ where the fault lives.

**The fix, all in the tool (`tools/ffmpeg_png_probe.py`), nothing in the task:**
1. ffmpeg is started with no console at all. No tab, no helper program.
2. The yardstick tells Windows "do not slow me", and tells it the same for every ffmpeg before that ffmpeg runs its
   first instruction.
3. The yardstick no longer trusts itself blindly. While it tests a fast core it reads how fast that core really ran,
   and compares it with what the settings allow (92 percent of the cap; 5.1 GHz when there is no cap). A core that was
   not up to speed gets one more go. If it is still slow, the result is **NOT A FAIR TEST** instead of CLEAN.

**The proof (all 11/24, same picture, same 1,008 tries: 24 on each of the 32 cores plus 4 x 60):**

| Run | Started by | Cap | Minutes | Result | The fast cores ran |
|---|---|---|---|---|---|
| 9:38 AM, old code | Task Scheduler | 4.6 GHz | 29.9 | CLEAN 0 of 1,008, **not a fair test** | not measured then (2 to 3.7 GHz for that way of starting, by the table above) |
| 10:38 AM | by hand | 4.6 GHz | 2.0 | CLEAN 0 of 1,008 | 4.47 to 4.48 GHz |
| 10:40 AM | Task Scheduler (copy of the task) | 4.6 GHz | 2.0 | CLEAN 0 of 1,008 | 4.47 to 4.48 GHz |
| 10:43 AM, **catch test** | Task Scheduler (copy of the task) | **lifted** 10:43:25 to 10:47:45 | 4.3 | **FAILS 155 of 1,056**: logical 10: 37 of 48, logical 11: 45 of 48, every other core 0 | the healthy ones 5.33 to 5.52 GHz |
| 10:49 AM | Task Scheduler (the real task, switched back on) | 4.6 GHz | 2.3 | CLEAN 0 of 1,008 | 4.46 to 4.48 GHz |
| 10:27 AM, test of the test (6 tries a core, told "save power") | by hand | 4.6 GHz | 1.6 | **NOT A FAIR TEST** | 1.07 to 1.13 GHz |

- The catch test ran inside the scheduled program itself: it lifted the cap, ran the daily yardstick, and put 4,600 MHz
  back in the same program, so the cap could not stay off if a chat session died. Checked afterwards: cap 4,600 MHz.
  It took 4.3 minutes because a crashed ffmpeg takes Windows a while to clean up (24 of the failures were crashes).
- The catch test's count for the bad core alone is higher than this morning's (82 of 96 tries now; 15 of 48 at 8:38 AM).
  With Windows picking the core it is in this morning's range (24 of 60 now; 9 to 30 of 60 then). The way ffmpeg is
  started changed in between (no console, never slowed), so the per-core numbers are not the same test done twice.
  Whether the core is also getting worse is not established; the daily run with the cap on is what watches for that.
  The other 30 logical cores: 0 failures, at 5.33 to 5.52 GHz.
- What else changed on the machine: at 10:27 AM Claude set Windows' default console to the classic one (registry,
  HKCU\Console\%%Startup), so a windowless job cannot pile up terminal tabs again, and gave the everything check's own
  program launches "no window". `tools/msi_speed_cap.py` and `tools/data_hunt.py` start their helper programs with
  "no window" too.

**What to take from it (for anyone learning):**
- A test has to show that it ran under fair conditions. A slow, held-back run that says "clean" is worse than no test.
- Try a tool the way it will really be run. By hand this one took 3 minutes; the same code run by the scheduler took 30.
- When a job is slow, count before guessing: the list of running programs showed the 480 console hosts in one look.
- **Open lead, not measured yet:** other scheduled jobs that do heavy work without a window may be slowed by Windows in
  the same way (the night render and its ffmpeg, for one). Measuring the cores' speed while such a job runs would tell.

### Fix choices (A is done; the rest are Jaron's call)
- **A. DONE 11/24 8:45 AM at 4.6 GHz, see above.** Cap the fast cores' top speed in Windows' power settings. One setting, undone in seconds, no restart. Lone jobs
  take about 22 percent longer (measured; first guessed at 10 to 15 percent); a busy machine loses nothing (it already runs slower than the cap). Start at
  4.6 GHz (the fault began above about 5.1), then run the yardstick: it must read 0.
- **B. Take logical 10 and 11 out of use** (Windows "reserved CPU sets": admin rights and one restart). Loses one of
  eight fast cores. Certain to work for programs; pairs well with A.
- **C. ON HOLD (Claude, 11/24): a failed BIOS update can kill the machine, so this one gets planned with Jaron first.**
  BIOS update to E15M2IMS.912 for the newer processor patch, which lowers the stress that wears the chip.
  Needs a person at the MSI. Do it only after A or B is in place. It may not heal a core that is already worn.
- **D. Cooling.** Idle 68 C and 90-97 C on light work is hot. Fan and vent cleaning, and MSI's fan setting, are worth
  a look by whoever is next at the machine. Less heat = slower wear.

### The tools (both new 11/24, no admin, no downloads)
- `python tools/ffmpeg_png_probe.py --per-core 24` = the yardstick, about 2 minutes. Run it on a QUIET machine (a busy
  chip slows itself and hides the fault). It says CLEAN, FAILS or NOT A FAIR TEST (exit code 0, 1, 2) and reads how
  fast the fast cores really ran. Run it before and after any fix. It runs daily at 11:30 AM as the task
  "MSI Core Yardstick". `--per-core 6 --eco --no-log` is the test of the test: slowed on purpose, it must say NOT A FAIR TEST.
- `python tools/msi_speed_cap.py status | set 4600 | off` = the cap itself.
- `python tools/data_hunt.py --minutes 10 --label "what the machine is doing"` = the wider net: watches memory, the
  Windows file cache, just-written files read by a second program, real PNGs through ffmpeg, and each core. When
  something is wrong it writes down the exact bytes. `--inject` proves it catches planted errors.
- Runs: `state/msi-data-hunt-runs.md` (one line each), details: `state/msi-data-hunt-log.jsonl`.

### Not done
- No restart, nothing installed. One system setting was changed: the speed cap (fix A).
- Windows' memory test at boot (mdsched): no longer first in line. With the bad core left out, 300 of 300 were right,
  and the first data_hunt run found no memory or file-cache damage. Still worth one run some quiet night.
- sfc, DISM, chkdsk and the drive's health counters need admin rights; this session has none (a person would have to
  click Yes at the MSI). Low priority now: nothing points at Windows files or the disk.
- Other facts on file: Windows log shows no hardware-error reports in 75 days (this kind of fault does not report itself);
  drive Micron 2500 1 TB, Healthy; memory 2 x 16 GB Samsung at its rated speed; graphics driver for the Intel chip is
  from 10/2024 and several small MSI/Killer/Nahimic drivers are old (not suspects now, just noted).

---
(Earlier notes, kept as written.)

What was known when it came off the sealed list:

| 2026-11-22 11:40 AM | **MSI is damaging data now and then.** 3 signs in 16 hours: (1) 11/21 7:35 PM Sapling crashed on a memory row that parses fine afterward; (2) 11/22 ~5 AM ffmpeg could not read news frames that read fine elsewhere, then crashed; (3) 11/22 ~11 AM three map-briefing videos came out corrupted (in one, 11 bytes had turned to zero). Earlier: crashes 10/11 (bugcheck 0x20001) and 10/31 (sudden power-off; the news pipeline notes a CLOCK_WATCHDOG_TIMEOUT freeze). Disk reports Healthy, Windows logs no hardware errors (normal laptop RAM can't report them). Laptop: MSI Vector 16 HX A14VFG, Intel i9-14900HX, 2x16 GB DDR5-5600, BIOS E15M2IMS.910 from 10/15/2025. | Real-world stakes: silent corruption can reach Sapling's memory, backups, renders, repos. Hardware diagnosis is above Jaron's pay grade and ours. | A computer repair tech or MSI support (warranty?). They'd run a memory test (MemTest86 / Windows Memory Diagnostic), the Intel Processor Diagnostic Tool, and check for a newer MSI BIOS. | MOVED OUT 11/22 1:05 PM (Jaron: having someone else look at the MSI is "very different" from Sapling or the creature). Not a sealed item: it's the AIs' own machine. Now an AI-owned open problem in state/open-list.md; outside hands only as a last resort, after the machine is prepared. |

New since: 11/23-11/24 Drive index corrupt again (even after the slow gentle fill); 11/24 ffmpeg 'png inflate error -3' on fresh render frames AND a freshly written temp logo PNG; the same logo file read clean 30/30 later. Pattern so far: failures hit files read soon after being written.

## Plan (in-house, no downloads from untrusted sources)
1. Repeatable test: write+read-back loop (hash on write vs hash on read) on C:, at idle and under GPU load -> does damage track load, heat, or fresh writes?
2. Windows' own memory test (mdsched, needs one reboot at a quiet hour; AIs schedule it 3-6 AM window rules permitting).
3. sfc /scannow + DISM health check; chkdsk read-only scan; NVMe SMART details.
4. Log every hit to this file with time, load, temperature.
