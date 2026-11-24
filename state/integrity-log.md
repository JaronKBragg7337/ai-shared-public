# Integrity self-test log

Written by `tools/integrity_test.py` (how to read it: top of that file, and below). Newest last.
CLEAN = every memory read, CPU answer and disk read-back was right. ANY wrong answer on a clean
machine is not normal: one is a warning, two in different runs means hardware.

- 2026-11-22 13:12 | **CLEAN** | 3.1 min | 7 workers, below_normal | RAM 6.0 GB, 186 passes (110 GB checked) | 2168 CPU answers | disk 4.4 GB written+read (uncached) | wrong: 0 (none) | whole-machine CPU 32%
- 2026-11-22 13:30 | **CLEAN** | 6.1 min | 7 workers, normal | RAM 6.0 GB, 346 passes (205 GB checked) | 4112 CPU answers | disk 7.0 GB written+read (uncached) | wrong: 0 (none) | whole-machine CPU 34%
- 2026-11-22 13:36 | **CLEAN** | 6.1 min | 7 workers, normal | RAM 6.0 GB, 302 passes (179 GB checked) | 3504 CPU answers | disk 7.0 GB written+read (uncached) | wrong: 0 (none) | whole-machine CPU 30%
- 2026-11-22 13:43 | **CLEAN** | 10.1 min | 30 workers, normal | RAM 8.0 GB, 2896 passes (272 GB checked) | 23240 CPU answers | disk 11.2 GB written+read (uncached) | wrong: 0 (none) | whole-machine CPU 97%
- 2026-11-23 01:15 | **CLEAN** | 30.2 min | 30 workers, below_normal | RAM 8.0 GB, 6020 passes (564 GB checked) | 24064 CPU answers | disk 22.5 GB written+read (uncached) | wrong: 0 (none) | whole-machine CPU 54%
