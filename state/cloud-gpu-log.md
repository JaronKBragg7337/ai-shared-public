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

2026-10-28 10:44 PM | Kimi | START | ahn183thmmeu2w | H100 SXM (secure) | growth speed test 20261028-224312; watchdog 12 min; reaper task | $3.99/hr
2026-10-28 10:47 PM | Kimi | TERMINATE | ahn183thmmeu2w | H100 SXM | growth speed test 20261028-224312 | deleted=True, 2.6 min x $3.99/hr = $0.17; sapling pods left: none
2026-10-28 10:54 PM | Kimi | START | hsx8cmsd0pax0w | H100 SXM (secure) | growth compiled speed test 20261028-224312; watchdog 15 min; reaper task | $3.99/hr
2026-10-28 10:57 PM | Kimi | TERMINATE | hsx8cmsd0pax0w | H100 SXM | growth compiled speed test 20261028-224312 | deleted=True, 3.6 min x $3.99/hr = $0.24; sapling pods left: none
2026-10-28 11:02 PM | Kimi | FINISH | - | - | compiled growth run stopped on error | pods left: none
2026-10-28 11:03 PM | Kimi | START | fowy9l9ij5tsjb | H100 SXM (secure) | growth compiled speed test 20261028-224312; watchdog 15 min; reaper task | $3.99/hr
2026-10-28 11:06 PM | Kimi | TERMINATE | fowy9l9ij5tsjb | H100 SXM | growth compiled speed test 20261028-224312 | deleted=True, 3.6 min x $3.99/hr = $0.24; sapling pods left: none
2026-10-28 11:06 PM | Kimi | PLAN | - | H100 SXM | growth 20261028-224312 compiled measured 459,389.0 tok/s; target 1,971,686,400 tokens | growth $6.09 worst case, all pods $6.74; local-fold reserve 25 min
2026-10-28 11:06 PM | Kimi | START | 61mdv4olhnr8xk | H100 SXM (secure) | growth training 20261028-224312; target 1,971,686,400 tokens; watchdog 178.4 min; reaper task | $3.99/hr
2026-10-29 12:30 AM | Kimi | TERMINATE | 61mdv4olhnr8xk | H100 SXM | growth training 20261028-224312 | deleted=True, 84.2 min x $3.99/hr = $5.60; sapling pods left: none
2026-10-29 12:30 AM | Kimi | FINISH | - | - | growth 20261028-224312; core ready=True | all pods $6.25; pods left: none
2026-10-29 2:10 AM | Kimi | START | 8bokw0i5kgp100 | H100 SXM (secure) | v5 conversation 20261029-020836; training 25 min / 3000 steps; watchdog 45 min; Windows reaper | $3.99/hr
2026-10-29 2:17 AM | Kimi | TERMINATE | 8bokw0i5kgp100 | H100 SXM | v5 conversation 20261029-020836 | deleted=True, 6.3 min x $3.99/hr = $0.42; pods left: none
2026-10-29 2:27 AM | Kimi | START | 4fn1yecujc9523 | H100 SXM (secure) | v5 conversation 20261029-022510; training 25 min / 3000 steps; watchdog 45 min; Windows reaper | $3.99/hr
2026-10-29 2:30 AM | Kimi | TERMINATE | 4fn1yecujc9523 | H100 SXM | v5 conversation 20261029-022510 | deleted=True, 3.1 min x $3.99/hr = $0.21; pods left: none
2026-10-29 2:37 AM | Kimi | FINISH | - | - | v5 conversation lessons complete | two runs total $0.63 estimated; pods left: none
2026-11-01 10:49 AM | Kimi | REST v2 migration verified read-only: H100 price query and pod list OK; dry run blocked incomplete clean bundle before upload/create; pods running: 0
2026-11-02 12:36 AM | Kimi | START | aisdfkwi5x0f7x | H100 SXM (secure) | fresh 350M pilot 20261102-003254; target 800,000,000 tokens; training 105 min; watchdog 125 min; Windows reaper; staged only | $3.99/hr
2026-11-02 2:25 AM | Kimi | TERMINATE | aisdfkwi5x0f7x | H100 SXM | fresh 350M pilot 20261102-003254 | deleted=True, 109.1 min x $3.99/hr = $7.25; pods left: none
2026-11-02 2:25 AM | Kimi | FINISH | - | H100 SXM | fresh 350M pilot 20261102-003254 | total $7.25; pods left: none
2026-11-24 11:38 AM | Claude | CHECK (read-only) | - | - | balance $7.88, spend $0/hr, pods 0, network volumes 0 | pods left: none
