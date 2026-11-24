# The hidden-law world: results

Made by `law/report.mjs` from the chained records in `law/results`. Plan: `law/PLAN.md`, committed before any model was asked.
Each world has its own made-up law of nature, so nothing can be remembered. A grade is the share of 200 unseen experiments a written law predicts within 1%.

The twelve laws (never shown to any model):

| world | kind | the hidden law |
|---|---|---|
| 1 | power | `5 * m1 * pow(m2, 2) * pow(q2, 0.5) / (pow(r, 3) * q1)` |
| 2 | power | `3 * m1 * m2 * pow(q1, 0.5) / (pow(r, 1.5))` |
| 3 | power | `5 * pow(m2, 2) * q1 * q2 / (pow(r, 1.5) * m1)` |
| 4 | power | `0.5 * m1 * pow(m2, 0.5) * q1 / (pow(r, 1.5) * q2)` |
| 5 | plus | `5 * m1 * pow(m2, 0.5) * q1 * q2 / (pow(r, 0.5)) + 0.5 * m1` |
| 6 | plus | `0.5 * pow(m2, 0.5) * q2 / (pow(r, 1) * q1) + 0.5 * pow(q2, 2)` |
| 7 | plus | `3 * pow(m2, 2) * q2 / (pow(r, 1) * q1) + 2 * pow(m1, 2)` |
| 8 | plus | `1.5 * pow(m1, 2) * pow(m2, 2) * pow(q1, 0.5) * pow(q2, 2) / (pow(r, 1)) + 2 * q2` |
| 9 | mix | `0.25 * (m2 + 3 * q1) * m1 / pow(r, 1.5)` |
| 10 | mix | `5 * pow(q1 + 0.5 * q2, 2) * m1 / pow(r, 3)` |
| 11 | mix | `0.5 * (m2 + 0.5 * q1) * q2 / pow(r, 1.5)` |
| 12 | mix | `1.5 * pow(m1 + 3 * m2, 2) * q2 / pow(r, 2)` |

| who | arm | worlds | average grade | power | plus | mix | solved outright (0.95+) | unreadable |
|---|---|---|---|---|---|---|---|---|
| gpt-6.2-sol | A: bare: 12 random experiments, one try | 6 (1, 2, 5, 6, 9, 10) | **0.84** | 1.00 | 1.00 | 0.51 | 5 of 6 | 0 |
| kimi-k3.1-pro | A: bare: 12 random experiments, one try | 6 (1, 2, 5, 6, 9, 10) | **0.17** | 0.50 | 0.01 | 0.01 | 1 of 6 | 2 |
| no-model | 0: no model: straight-line fit on logs | 12 | **0.57** | 1.00 | 0.64 | 0.08 | 5 of 12 | 0 |
| no-model | S0: AFTER THE PLAN: no model, one fixed power-law shape, the same fitter | 12 | **0.57** | 1.00 | 0.63 | 0.07 | 5 of 12 | 0 |
| qwen3.5:4b | A: bare: 12 random experiments, one try | 12 | **0.00** | 0.00 | 0.00 | 0.00 | 0 of 36 | 0 |
| qwen3.5:4b | B: built: chooses its own 12 experiments | 12 | **0.00** | 0.00 | 0.00 | 0.00 | 0 of 36 | 0 |
| qwen3.5:4b | B2: built + sees its law checked against its notebook | 12 | **0.00** | 0.00 | 0.00 | 0.00 | 0 of 36 | 1 |
| qwen3.5:4b | S: AFTER THE PLAN: the model writes the shape, the world finds the numbers (4 rounds) | 12 | **0.29** | 0.51 | 0.33 | 0.05 | 7 of 36 | 0 |
| qwen3.5:9b | A: bare: 12 random experiments, one try | 12 | **0.00** | 0.00 | 0.00 | 0.00 | 0 of 36 | 6 |
| qwen3.5:9b | B: built: chooses its own 12 experiments | 12 | **0.00** | 0.00 | 0.00 | 0.00 | 0 of 36 | 8 |
| qwen3.5:9b | B2: built + sees its law checked against its notebook | 12 | **0.00** | 0.01 | 0.00 | 0.00 | 0 of 36 | 7 |
| qwen3.5:9b | S: AFTER THE PLAN: the model writes the shape, the world finds the numbers (4 rounds) | 12 | **0.09** | 0.09 | 0.14 | 0.05 | 1 of 36 | 0 |

By the rule fixed in the plan (higher on average, and higher or equal on at least three quarters of the worlds):
- gpt-6.2-sol: bare beats the no-model fit (same worlds): **yes** (average +0.203, higher or equal on 5 of 6 worlds).
- kimi-k3.1-pro: bare beats the no-model fit (same worlds): **no clear difference** (average -0.463, higher or equal on 1 of 6 worlds).
- qwen3.5:4b: choosing its own experiments helps (B over A): **no clear difference** (average -0.001, higher or equal on 9 of 12 worlds).
- qwen3.5:4b: seeing its law checked helps (B2 over B): **no clear difference** (average -0.000, higher or equal on 9 of 12 worlds).
- qwen3.5:4b: built beats the no-model fit: **no clear difference** (average -0.573, higher or equal on 0 of 12 worlds).
- qwen3.5:4b: bare beats the no-model fit (same worlds): **no clear difference** (average -0.572, higher or equal on 0 of 12 worlds).
- qwen3.5:4b, after the plan: its shapes beat the fixed power-law shape (S over S0): **no clear difference** (average -0.276, higher or equal on 3 of 12 worlds).
- qwen3.5:4b, after the plan: shape-and-fit beats the best planned arm (S over B2): **yes** (average +0.291, higher or equal on 12 of 12 worlds).
- qwen3.5:4b, after the plan: shape-and-fit against the big model alone, same worlds (S over Sol): **no clear difference** (average -0.427, higher or equal on 2 of 6 worlds).
- qwen3.5:9b: choosing its own experiments helps (B over A): **no clear difference** (average -0.001, higher or equal on 7 of 12 worlds).
- qwen3.5:9b: seeing its law checked helps (B2 over B): **yes** (average +0.001, higher or equal on 11 of 12 worlds).
- qwen3.5:9b: built beats the no-model fit: **no clear difference** (average -0.571, higher or equal on 0 of 12 worlds).
- qwen3.5:9b: bare beats the no-model fit (same worlds): **no clear difference** (average -0.571, higher or equal on 0 of 12 worlds).
- qwen3.5:9b, after the plan: its shapes beat the fixed power-law shape (S over S0): **no clear difference** (average -0.478, higher or equal on 1 of 12 worlds).
- qwen3.5:9b, after the plan: shape-and-fit beats the best planned arm (S over B2): **yes** (average +0.087, higher or equal on 10 of 12 worlds).
- qwen3.5:9b, after the plan: shape-and-fit against the big model alone, same worlds (S over Sol): **no clear difference** (average -0.787, higher or equal on 0 of 6 worlds).

Laws written by the big models (one try each):

- gpt-6.2-sol, world 1 (power): grade 1: `5*m1*pow(m2,2)*sqrt(q2)/(q1*pow(r,3))`
- gpt-6.2-sol, world 2 (power): grade 1: `3*m1*m2*sqrt(q1)/pow(r,1.5)`
- gpt-6.2-sol, world 5 (plus): grade 1: `5*m1*q1*q2*sqrt(m2/r)+0.5*m1`
- gpt-6.2-sol, world 6 (plus): grade 1: `(q2/2)*(q2+sqrt(m2)/(q1*r))`
- gpt-6.2-sol, world 9 (mix): grade 1: `m1*(0.75*q1+0.25*m2)/(r*sqrt(r))`
- gpt-6.2-sol, world 10 (mix): grade 0.025: `800/(pow(r,2)*(1+pow(0.253*pow(m1*q1,1.5)/pow(r,2.25)+0.16885*pow(r/7.7,2.25)*pow(q1/7.35,0.378)*pow(m1/4.94,0`
- kimi-k3.1-pro, world 1 (power): grade 1: `5*m1*pow(m2,2)*sqrt(q2)/(q1*pow(r,3))`
- kimi-k3.1-pro, world 2 (power): grade 0: `3*m1*m2*sqrt(q1)/pow(r,1.5) allowed expression. Could use /pow(r,3/2) but pow exponent1.5 fine. No q2. Respond`
- kimi-k3.1-pro, world 5 (plus): grade 0.015: `m1*m2*q1*q2/r*(m1/m2+q1/q2+q2/q1+2*(q1+q2)/(m1+m2))`
- kimi-k3.1-pro, world 6 (plus): grade 0: `q2*q2/2 + q2*sqrt(m2)/(2*q1*r) likely. Verify with row1 numeric: q2 sqrt(m2)=1.85*2.636285=4.877127; denominat`
- kimi-k3.1-pro, world 9 (mix): grade 0.015: `(m1*m2 + q1*q2)/pow(r,2)`
- kimi-k3.1-pro, world 10 (mix): grade 0.005: `(m1*m2+q1*q2)*(q1*q2)/pow(r,3)`

Read both ways (Kimi K3.1 Pro). The grader reads one line and nothing else. Two of Kimi's answers put the law inside a sentence, so the grader could not read them and they count as 0 above. Pulled out by hand (this is NOT the planned reading) and graded by the same grader:

- world 2: `3*m1*m2*sqrt(q1)/pow(r,1.5)` grades 1
- world 6: `q2*q2/2 + q2*sqrt(m2)/(2*q1*r)` grades 1

So Kimi solved 1 of 6 worlds as graded, and 3 of 6 if the law is lifted out of its sentence. The planned figure stays the first one.
