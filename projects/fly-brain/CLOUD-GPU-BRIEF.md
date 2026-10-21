# Renting one cloud GPU for Sapling - brief for any AI helping Jaron set it up

> **WARNING - READ FIRST: A RENTED GPU BILLS EVERY HOUR IT EXISTS, EVEN WHEN IDLE.** Every run must end by TERMINATING the pod
> (stopping isn't enough if it keeps a paid disk). Before ending ANY session that touched RunPod - including a session about to
> compact or hand off - check that zero pods are running (RunPod console > Pods, or the runpod plugin's list tool), and log every
> pod start and stop in AI-Shared/state/cloud-gpu-log.md. If a pod is found running with no active job, terminate it and log it.

## Status (keep current)
- 10/15/2026 8:01 PM: RunPod plugin runpod@runpod v1.7.4 installed for Claude Code on the MSI (OAuth, no key stored).
- 10/15 10:43 PM: OAuth sign-in FAILED in the Claude desktop app ("redirect_uri is not allowed. It must be a registered client callback or a loopback address"). Plan B: RunPod API key (console > Settings > API Keys) saved on the MSI in ~/.secrets/keys.env as RUNPOD_API_KEY; Claude calls the REST API directly. Old plan: (2) one-time browser sign-in at
  the MSI ("/mcp" > runpod > Sign in with Runpod). Then Claude writes the run script and does one short test run.

Paste this whole file to the AI that's helping. Jaron does the account and payment steps; then he tells Claude Code (on the MSI)
it's ready, and Claude runs the training.

## What it's for
Sapling (github.com/JaronKBragg7337/sapling) is Jaron's own AI, trained from scratch on licensed text. A full night's training run
on his laptop RTX 4060 (about 1.2 billion tokens for a 60.5M-parameter model at ~35k tokens/s) would take about 30-60 minutes on
one rented H100. The goal is a pay-per-hour GPU, used now and then, about $2-3 per hour.

## What Jaron needs to end up with
1. An account at ONE of these GPU rental sites (pick by price and ease; all rent single GPUs by the hour):
   - RunPod (runpod.io) - "Pods", pay as you go, web terminal. Usually the easiest.
   - Lambda (lambda.ai) - on-demand instances, simple pricing.
   - Vast.ai - often cheapest, a marketplace of hosts.
2. A small prepaid balance, about $10-20, enough for a few runs. Pay on the web with his X Money card, never through Apple.
3. Sign-in: RunPod's official Claude Code plugin is installed on the MSI (10/15). Jaron signs in once in the browser (OAuth), no key to paste or store.
   (Only for unattended runs later: an API key saved on the MSI in C:\Users\lilli\.secrets\keys.env as RUNPOD_API_KEY, never pasted into a chat.)
4. If the site asks for an SSH public key: Claude Code makes one on the MSI and gives Jaron the PUBLIC part to paste.

## The GPU to pick
- One NVIDIA H100 (80 GB) or A100 (80 GB), on-demand (not "spot" or "interruptible" for the first try).
- A standard PyTorch template/image (PyTorch 2.x, CUDA 12).
- About 50 GB of disk. The training data is ~3 GB and checkpoints ~250 MB each.

## Safety and money rules
- Always STOP or terminate the GPU when a run finishes. Rented GPUs bill by the hour even when idle.
- Set a spending limit or keep only a small prepaid balance.
- No secrets in chats or screenshots. Key names are fine, values never.

## When done, Jaron tells Claude Code
"Cloud GPU is set up on <site>, key saved as <NAME>." Claude Code then writes the run script (upload data, train, download the
checkpoint, shut down), does one short test run, and reports the cost.
