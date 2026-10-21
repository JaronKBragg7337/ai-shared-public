# qwen-local - Q-A
Time: 2026-10-15 07:52 | 41s

Based on the logs you provided, here is a summary of the current state of your **Pipeline Architecture (v2)** as of 2026-09-10:

### 1. The Core Failure Mode Identified
The previous attempt failed because the "Scout" bot performed research on a market with an **8c spread**, generating a solid 6.5c edge, yet the trade was killed by the liquidity gap.
*   **Lesson:** Researching a deep-water market (high spread) is often futile; it generates noise and costs resources without creating actionable edges once spread is factored in.
*   **Design Principle:** **Edge must exceed Spread.** If `(Scout Prob - Ask) <= (Ask - Bid)`, abort immediately regardless of thesis quality.

### 2. The New Pipeline (v2) Protocol
The workflow has been refined to ensure no bot contaminates another with price data, and every step is gated by liquidity logic.

1.  **Bridge (Screening Agent):**
    *   Reads the live order book via the Polymarket MCP.
    *   **Action:** Discards markets where `Spread > 2c`. Only sends questions to Scout if the spread is tight enough to be meaningful ($10 book, <2c spread).
    *   *Crucial:* It does **not** tell Scout which side is cheaper or what the absolute probability looks like.

2.  **Scout (Research Bot):**
    *   Receives a QUESTION only (e.g., "What happens in Falcons vs Packers on Sep 24?").
    *   **Constraints:** Never sees prices, spreads, positions, or AI-Shared.
    *   **Output:** Independent probability, evidence with dates/sources, confidence interval, and "what would change this."
    *   **Calibration:** Required to vary confidence based on evidence quality (avoiding PolyBench's "uniform overconfidence" failure).

3.  **Edge Calculation (Bridge):**
    *   Formula: `Net Edge = Scout Prob - Market Ask`.
    *   Check: Is `Net Edge > Market Spread`?
    *   If No $\rightarrow$ **Stop.** (Trade is too wide for the edge).
    *   If Yes $\rightarrow$ Size bet ($1–2 on a $10 book), request Jaron approval.

4.  **Claude Code (Cross-Check):**
    *   Independently verifies the market numbers and facts via its own route.
    *   **Gatekeeper:** A disagreement here stops the trade entirely. If Claude cannot confirm Bridge's numbers, no order is placed.

5.  **Jaron (Final Gate):**
    *   Reviews the thesis, the independent confirmation, and approves/refuses execution.

### 3. Current Status & Next Task
*   **Scout:** Created and briefed as of today.
*   **First Live Task:** Falcons vs. Packers (2026-09-24).
    *   Source: Underlying facts only.
    *   Goal: Identify if a researched discrepancy exists that remains profitable after the spread is removed.

### 4. Architectural Guarantees
*   **Isolation:** Each bot has its own cloud VM and isolated memory. Copying a bot wipes history but keeps skills, enabling clean-room resets (solving the Analyst Capture issue).
*   **Anti-Contamination:** The design ensures no agent ever sees another agent's estimates or market data before it makes its own independent judgment.

The system is now designed so that **bad research on bad markets** gets caught early by Bridge, **conflicting evidence** gets caught by Claude, and **insufficient edges** are never exposed to Jaron for approval.
