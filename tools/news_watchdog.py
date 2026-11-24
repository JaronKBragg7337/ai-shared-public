"""Check that today's rendered Heartbeat News is available after 7 AM.

Run every 15 minutes from 7 AM through noon. --dry-run checks without sending
or recording an alert. State is recorded only after a notification succeeds.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
from datetime import datetime
from time import time

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "state" / "news-watchdog-alerts.json"
SECRETS = Path.home() / ".secrets" / "keys.env"
BASE = "https://ygjpnvrwhkrowkrskftk.supabase.co/storage/v1/object/public/news-video"


def check(date):
    """Return (status, reason); a failed network check never means missing."""
    try:
        with urllib.request.urlopen(f"{BASE}/index.json?t={int(time())}", timeout=20) as response:
            index = json.load(response)
        episodes = index["episodes"]
        if not isinstance(episodes, list) or any(not isinstance(e, dict) for e in episodes):
            raise ValueError("invalid episode list")
        episode = next((e for e in episodes if e.get("date") == date), None)
        if episode is None:
            return "missing", "today's show is absent from the public index"
        # The viewer uses this URL. Only check our own public storage location.
        video = f"{BASE}/{date}.mp4"
        if episode.get("video") != video:
            return "unreachable", "today's index entry has an unexpected video address"
        request = urllib.request.Request(video, method="HEAD")
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                if response.status != 200:
                    return "unreachable", "the video check returned an unexpected response"
                length = response.headers.get("Content-Length")
                if length is not None and int(length) <= 0:
                    return "missing", "today's video is empty"
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return "missing", "today's video is absent from storage"
            raise
        return "published", "today's index and video are accessible"
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return "unreachable", "the public news index or video could not be checked"


def send_alert(message):
    topic = None
    for line in SECRETS.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("NTFY_TOPIC="):
            topic = line.split("=", 1)[1].strip().strip('"\'')
            break
    if not topic:
        raise ValueError("NTFY_TOPIC missing")
    request = urllib.request.Request("https://ntfy.sh/" + topic, data=message.encode("utf-8"),
                                     headers={"Title": "Heartbeat News", "Priority": "high"})
    with urllib.request.urlopen(request, timeout=20) as response:
        if response.status not in (200, 201, 202):
            raise OSError("notification failed")


def run(date, dry_run=False, state_path=STATE):
    status, reason = check(date)
    print(f"{date}: {status}: {reason}")
    if status == "published" or dry_run:
        return 0 if status == "published" else 1
    try:
        sent = json.loads(state_path.read_text(encoding="utf-8"))
        if not isinstance(sent, dict):
            raise ValueError("invalid alert state")
    except FileNotFoundError:
        sent = {}
    except (OSError, ValueError):
        # A damaged state file must not silently suppress a real alert.
        sent = {}
    key = f"{date}:{status}"
    if key in sent:
        return 1
    message = (f"Heartbeat News: {reason}. Please check the news run." if status == "missing"
               else "Heartbeat News: cannot check whether today's show is live. Please check the news run.")
    try:
        send_alert(message)
    except Exception:
        # Do not print exceptions: URLs can contain the private ntfy topic.
        print("News alert could not be sent; the next scheduled check will retry.", file=sys.stderr)
        return 2
    sent[key] = datetime.now().isoformat(timespec="seconds")
    # Keep only today's records; write atomically so an interrupted write is safe.
    sent = {k: v for k, v in sent.items() if k.startswith(date + ":")}
    state_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = state_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(sent, indent=2), encoding="utf-8")
    os.replace(tmp, state_path)
    return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="check without sending or recording alerts")
    args = parser.parse_args()
    now = datetime.now()
    if not args.dry_run and not (7 <= now.hour < 12):
        print("Outside the 7 AM to noon watchdog window.")
        return 0
    return run(now.date().isoformat(), args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
