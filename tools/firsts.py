"""firsts.py - the "huh, that's actually cool" log (Jaron 11/21 11:21 AM).

Small level, next to the big sealed level (P-0179, state/sealed.md): when Sapling or the creature does something nobody built in,
figures something out on its own, gets measurably smarter, or does something unique - catch it, write it down, show Jaron.
Nothing pauses. If a first keeps climbing toward real-world stakes, it moves up to state/sealed.md.

Jaron asked for BOTH ways for now (then see which is needed): each first as it happens (ntfy + mailbox to claude),
and a daily roundup (task "Firsts Roundup", 8:30 PM local).

  python tools/firsts.py add --project sapling|creature --what "..." --why "why it surprised us" --proof "numbers/clip/file" [--checked] [--by kimi]
  python tools/firsts.py roundup            # today's firsts, one phone line (sent even when there are none, while the habit is new)
  python tools/firsts.py list [--project X] [--days 7]

Every entry needs proof, and says checked / not checked yet, so nobody hypes small stuff.
Store: state/firsts/<project>.jsonl (+ readable state/firsts/FIRSTS.md). AI-Shared is a private repo; the creature's firsts stay
private from the world (never from Jaron). Sapling's may be shown on its control-room page.
"""
import argparse, json, os, subprocess, sys, urllib.request
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "state" / "firsts"
NAMES = {"sapling": "Sapling", "creature": "her (the creature)"}
# Jaron 11/21 6:20 PM: not every surprise is "cool". Three kinds, all worth noticing; none of them pauses anything.
KINDS = {"wow": "Wow", "hmm": "Hmm", "uh-oh": "Uh-oh"}  # wow = good surprise; hmm = strange, not sure if good or bad; uh-oh = going wrong but not dangerous (may need a fix)


def topic():
    for line in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig"):
        if line.startswith("NTFY_TOPIC="):
            return line.split("=", 1)[1].strip()


def push(msg, title):
    try:
        req = urllib.request.Request("https://ntfy.sh/" + topic(), data=msg.encode(), headers={"Title": title})
        urllib.request.urlopen(req, timeout=20)
        return True
    except Exception as e:
        print("ntfy failed:", e)
        return False


def mail(subject, body):
    try:
        subprocess.run([sys.executable, str(ROOT / "tools" / "mailbox.py"), "send", "--from", "firsts", "--to", "claude",
                        "--subject", subject, "--body", body], capture_output=True, timeout=60, stdin=subprocess.DEVNULL)
    except Exception as e:
        print("mailbox failed:", e)


def load(project=None):
    out = []
    for p in sorted(DIR.glob("*.jsonl")):
        if project and p.stem != project:
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return sorted(out, key=lambda e: e["at"])


def write_md():
    rows = load()
    lines = ["# Firsts - the surprises worth noticing: wow, hmm, uh-oh (newest last). Written by tools/firsts.py; don't hand-edit.", "",
             "Small level of Jaron's two-level rule (11/21). Big level (sealed, needs a professional): state/sealed.md.", ""]
    for proj in NAMES:
        mine = [e for e in rows if e["project"] == proj]
        lines += [f"## {NAMES[proj]}", ""] + ([f"- **{(e.get('when') or e['at'][:16].replace('T', ' '))}**{' (found ' + e['at'][:10] + ')' if e.get('when') else ''} [{KINDS.get(e.get('kind', 'wow'), 'Wow')}] {e['what']} - why it surprised us: {e['why']}. "
                                               f"Proof: {e['proof']}. {'Checked' if e['checked'] else 'Not checked yet'} (by {e['by']})."
                                               for e in mine] or ["- none yet"]) + [""]
    (DIR / "FIRSTS.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--project", required=True, choices=list(NAMES))
    a.add_argument("--what", required=True)
    a.add_argument("--why", required=True)
    a.add_argument("--proof", required=True)
    a.add_argument("--checked", action="store_true")
    a.add_argument("--by", default="unknown")
    a.add_argument("--when", default="", help="when it actually happened, if not just now (e.g. 2026-10-14)")
    a.add_argument("--kind", default="wow", choices=list(KINDS), help="wow = good surprise, hmm = strange/unsure, uh-oh = going wrong, not dangerous")
    r = sub.add_parser("roundup")
    r.add_argument("--dry", action="store_true")
    l = sub.add_parser("list")
    l.add_argument("--project", choices=list(NAMES))
    l.add_argument("--days", type=int, default=7)
    args = ap.parse_args()
    DIR.mkdir(parents=True, exist_ok=True)

    if args.cmd == "add":
        e = {"at": datetime.now().isoformat(timespec="seconds"), "project": args.project, "what": args.what.strip(),
             "why": args.why.strip(), "proof": args.proof.strip(), "checked": args.checked, "by": args.by, "when": args.when.strip() or None, "kind": args.kind}
        with open(DIR / f"{args.project}.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
        write_md()
        tag = "" if e["checked"] else " (not checked yet)"
        old = f" (happened {e['when']}, found now)" if e["when"] else ""
        push(f"{e['what']}{old}{tag}. Why it's cool: {e['why']}", f"{KINDS[e['kind']]}: {NAMES[args.project]}")
        mail(f"FIRST ({args.project}): {e['what'][:80]}", json.dumps(e, ensure_ascii=False))
        print("logged + sent:", e["what"])
    elif args.cmd == "roundup":
        today = datetime.now().date().isoformat()
        todays = [e for e in load() if e["at"].startswith(today)]
        if todays:
            parts = []
            for proj in NAMES:
                mine = [f"{KINDS.get(e.get('kind', 'wow'), 'Wow')}: {e['what']}" for e in todays if e["project"] == proj]
                if mine:
                    parts.append(f"{NAMES[proj]}: " + "; ".join(mine))
            msg = f"{len(todays)} today. " + " | ".join(parts)
        else:
            msg = "None today. Sapling and her are both being watched for them."
        print(msg)
        if not args.dry:
            push(msg, "Firsts today")
    else:
        since = (datetime.now() - timedelta(days=args.days)).isoformat()
        for e in load(args.project):
            if e["at"] >= since:
                print(f"{e['at'][:16]} [{e['project']}] [{e.get('kind', 'wow')}] {e['what']} | {e['why']} | proof: {e['proof']} | "
                      f"{'checked' if e['checked'] else 'not checked'} | by {e['by']}")


if __name__ == "__main__":
    main()
