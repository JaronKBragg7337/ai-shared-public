# Cloud GPU log (RunPod) - every pod start and stop, one line each
# A rented GPU bills every hour it exists. Before ending any session that touched RunPod: zero pods running, or log why.
# Format: <local time> | <who> | START/TERMINATE | pod id | GPU | why | cost so far

2026-10-15 8:45 PM | Jaron | FUNDED | - | - | $15.00 credits loaded (X Money card, web). No pods. Spend rate $0.000/hr. Spend-rate limit shows $80/hr (RunPod default) | $0
2026-10-15 11:57 PM | Claude | START | cvnd3rc2lle3cs | H100 SXM | speed test (bench_speed.py micro 16 + 32), auto-terminate after | $3.99/hr
2026-10-16 12:02 AM | Claude | TERMINATE | cvnd3rc2lle3cs | H100 SXM | speed test done | balance now $15, pods now [], spend $0/hr
2026-10-16 1:23 AM | Claude | START | ycfqezzatkat9o | H100 SXM (secure) | long-reading lesson 20261016-0122 (tools/runpod_run.py; watchdog 95 min; reaper task) | $3.99/hr
2026-10-16 2:28 AM | Claude | TERMINATE | ycfqezzatkat9o | H100 SXM | long-reading lesson 20261016-0122 | deleted=True, 65 min x $3.99/hr = $4.34; sapling pods left: none
2026-10-16 11:18 PM | Kimi | START | tmqsavrbevrw9y | H100 SXM (secure) | long-reading lesson 20261016-2314 (tools/runpod_run.py; watchdog 95 min; reaper task) | $3.99/hr
2026-10-17 12:10 AM | Kimi | TERMINATE | tmqsavrbevrw9y | H100 SXM | long-reading lesson 20261016-2314 | deleted=True, 51 min x $3.99/hr = $3.42; sapling pods left: none

