import os, sys, urllib.request
t = [l.split("=",1)[1].strip() for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig") if l.startswith("NTFY_TOPIC=")][0]
urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + t, data=" ".join(sys.argv[2:]).encode(), headers={"Title": sys.argv[1]}), timeout=20)
