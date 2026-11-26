"""prep_watch.py - Prep Watch: the team keeps watching government emergency-preparedness moves + unexplained
infrastructure failures all day (Jaron 11/17 1:52 AM: "pause during the news, then catch up from the news and keep
watching the rest of the day").

Run hourly by the "HB Prep Watch" scheduled task:  python tools/prep_watch.py tick
  - Paused from 2:30 AM until today's news is PUBLISHED (rendered-runs.log), or 8:30 AM at the latest.
  - The first round after the news = a catch-up round: read today's episode + what changed overnight.
  - Every other round = a "what's new since the last round" check. Seats take turns (Codex, Grok Build, Kimi),
    so each meter gets one run about every 3 hours.
  - Output: research/preparedness/rounds/DATE-HHMM-seat.md, a digest appended to research/preparedness/LIVE.md.
  - Lines starting "NOTABLE:" get mailed to claude + satya-twin (inputs only; Satya owns the safety level).
  - A seat that fails twice in a row mails claude so the conductor can push it again.
  python tools/prep_watch.py status   -> prints the state
"""
import datetime, json, os, re, subprocess, sys

ROOT = r"C:\Users\lilli\AI-Shared"
PREP = os.path.join(ROOT, "research", "preparedness")
TEAM = os.path.join(PREP, "team")
ROUNDS = os.path.join(PREP, "rounds")
LIVE = os.path.join(PREP, "LIVE.md")
STATE = os.path.join(ROOT, "state", "prep-watch.json")
LOG = os.path.join(ROOT, "state", "prep-watch.log")
NEWS_LOG = os.path.join(ROOT, "projects", "news-show", "rendered-runs.log")
NO_WINDOW = 0x08000000
SEATS = {
    "codex": [r"C:\Users\lilli\scoop\shims\codex.exe", "exec", "-s", "read-only", "--skip-git-repo-check", "-m", "gpt-6-luna",
              "-c", 'model_reasoning_effort="high"', "-C", ROOT],   # Luna = near free (agents/claude-code/TEAM-CALL.md)
    "grok": [os.path.expanduser(r"~\.grok\bin\grok.exe"), "--max-turns", "60", "-p"],
    "kimi": [os.path.expanduser(r"~\.kimi-code\bin\kimi.exe"), "-p"],
}
ORDER = ["codex", "grok", "kimi"]


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M} {msg}\n")


def load():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {"next": 0, "last_run": None, "catchup_done": None, "fails": {}}


def save(s):
    json.dump(s, open(STATE, "w", encoding="utf-8"), indent=1)


def news_published(today):
    try:
        with open(NEWS_LOG, encoding="utf-8", errors="replace") as f:
            return any(l.startswith(today) and f"{today} PUBLISHED" in l for l in f.readlines()[-80:])
    except Exception:
        return False


def mail(to, subject, body):
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mailbox.py"), "send", "--from", "prep-watch", "--to", to,
                    "--subject", subject, "--body", body], capture_output=True, timeout=60, creationflags=NO_WINDOW)


def prompt(seat, catchup, last_run, today):
    core = open(os.path.join(TEAM, "BRIEF-CORE.md"), encoding="utf-8").read()
    angle = open(os.path.join(TEAM, f"angle-{seat}.txt"), encoding="utf-8").read()
    live = open(LIVE, encoding="utf-8").read()[-2500:] if os.path.exists(LIVE) else "(first round)"
    if catchup:
        task = (f"THIS ROUND = CATCH-UP after the overnight pause. Read today's Heartbeat News episode "
                f"https://www.heartbeatobservatory.com/news/episodes/{today}.json and anything else since {last_run or 'yesterday'}. "
                "Report what changed overnight on your angle: new preparedness moves AND unexplained infrastructure failures.")
    else:
        task = (f"THIS ROUND = WATCH. Report ONLY what is NEW since {last_run or 'the last round'} on your angle "
                "(new preparedness moves; new unexplained infrastructure failures). If nothing new, reply with one line: "
                "'Nothing new since <time>.'")
    return (f"{core}\n\n{angle}\n\nThe team's latest notes (newest at the bottom):\n{live}\n\n{task}\n"
            "Start any line the safety lead MUST see right away with 'NOTABLE:' (rare; real, sourced, new). "
            "Keep it short (under ~400 words). Reply as markdown only. Do not edit, create or push any files.")


def tick():
    now = datetime.datetime.now()
    today = f"{now:%Y-%m-%d}"
    s = load()
    paused = (now.hour, now.minute) >= (2, 30) and not news_published(today) and (now.hour, now.minute) < (8, 30)
    if paused:
        log("paused for the news render"); return
    catchup = s.get("catchup_done") != today and (news_published(today) or now.hour >= 8) and now.hour < 14
    # a seat that ran out of its own usage sits out until its bench ends, so the round goes to the next seat (11/25)
    benched = s.setdefault("benched", {})
    seat = None
    for i in range(len(ORDER)):
        cand = ORDER[(s.get("next", 0) + i) % len(ORDER)]
        if benched.get(cand, "") <= f"{now:%Y-%m-%d %H:%M}":
            seat = cand
            s["next"] = s.get("next", 0) + i
            break
    if seat is None:
        log("every seat is benched for usage, skipping"); return
    # never run into the 2:30 AM news pause
    cutoff = now.replace(hour=2, minute=25, second=0)
    if now >= cutoff:
        cutoff += datetime.timedelta(days=1)
    budget = min(45 * 60, int((cutoff - now).total_seconds()))
    if budget < 300:
        log("too close to the news pause, skipping"); return
    os.makedirs(ROUNDS, exist_ok=True)
    out_path = os.path.join(ROUNDS, f"{now:%Y-%m-%d-%H%M}-{seat}.md")
    try:
        r = subprocess.run(SEATS[seat] + [prompt(seat, catchup, s.get("last_run"), today)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=budget, creationflags=NO_WINDOW, cwd=ROOT)
        text, ok = r.stdout.strip(), r.returncode == 0 and len(r.stdout.strip()) > 20
        err = r.stderr[-600:]
    except subprocess.TimeoutExpired:
        text, ok, err = "", False, f"timeout after {budget}s"
    except Exception as e:
        text, ok, err = "", False, repr(e)
    s["next"] = s.get("next", 0) + 1
    fails = s.setdefault("fails", {})
    if not ok:
        fails[seat] = fails.get(seat, 0) + 1
        if re.search(r"402|exhausted|usage limit|quota|rate limit|out of credits", err, re.I):
            until = now + datetime.timedelta(hours=12)
            benched[seat] = f"{until:%Y-%m-%d %H:%M}"
            log(f"{seat} out of usage, benched until {benched[seat]}")
            if fails[seat] == 2:
                mail("claude", f"Prep Watch: {seat} benched (usage)", f"{seat} is out of its own usage ({err.strip()[:200]}). "
                     f"It sits out until {benched[seat]} and the other seats take its rounds. Nothing to do.")
            save(s); return
        log(f"{seat} FAILED ({fails[seat]} in a row): {err.strip()[:200]}")
        if fails[seat] >= 2:
            mail("claude", f"Prep Watch: {seat} failing", f"{seat} failed {fails[seat]} rounds in a row. Last error: {err.strip()[:500]}")
        save(s); return
    fails[seat] = 0
    open(out_path, "w", encoding="utf-8").write(text)
    head = "\n".join(text.splitlines()[:25])
    with open(LIVE, "a", encoding="utf-8") as f:
        f.write(f"\n\n## {now:%Y-%m-%d %H:%M} {seat}{' (catch-up)' if catchup else ''}\n{head}\n")
    if catchup:
        s["catchup_done"] = today
    s["last_run"] = f"{now:%Y-%m-%d %H:%M}"
    save(s)
    notable = [l.strip() for l in text.splitlines() if l.strip().startswith("NOTABLE:")]
    log(f"{seat} ok{' catch-up' if catchup else ''}, {len(text)} chars, {len(notable)} notable")
    if notable:
        body = f"From {seat} ({now:%H:%M}):\n" + "\n".join(notable[:6]) + f"\nFull: {out_path}"
        for to in ("claude", "satya-twin"):
            mail(to, "Prep Watch: notable", body)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print(json.dumps(load(), indent=1))
    else:
        tick()
