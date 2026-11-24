"""watch_reply.py - Claude answers Jaron's "Tell Claude" messages on his phone/watch (2026-10-28).
His words arrive in ai_mailbox (from_ai jaron-watch) through the watch-inbox function; the reply goes back as an ntfy
buzz titled "Claude", which shows on his iPhone and mirrors to the Apple Watch (Siri can read it aloud).
  python tools/watch_reply.py "text of the reply"
"""
import os, sys, urllib.request


def keys():
    env = {}
    for line in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig"):
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env


def reply(text):
    req = urllib.request.Request("https://ntfy.sh/" + keys()["NTFY_TOPIC"], data=text.encode("utf-8"),
                                 headers={"Title": "Claude", "Tags": "speech_balloon"})
    return urllib.request.urlopen(req, timeout=20).status


if __name__ == "__main__":
    print(reply(" ".join(sys.argv[1:]) or "ok"))
