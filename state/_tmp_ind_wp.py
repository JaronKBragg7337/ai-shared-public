import urllib.request, re, json, ssl
ctx = ssl.create_default_context()
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json,text/plain,*/*",
}

def fetch(u):
    req = urllib.request.Request(u, headers=UA)
    return urllib.request.urlopen(req, timeout=20, context=ctx).read()

mid = "151554"
apis = [
    f"https://www.cricbuzz.com/api/cricket-match/minimal/{mid}",
    f"https://www.cricbuzz.com/api/mcenter/v1/{mid}/scard",
    f"https://www.cricbuzz.com/api/mcenter/v1/{mid}/hscard",
    f"https://www.cricbuzz.com/api/mcenter/v1/{mid}",
    f"https://www.cricbuzz.com/match-api/{mid}/commentary.json",
    f"https://www.cricbuzz.com/live-cricket-scores/{mid}/ind-vs-wi-3rd-odi-india-vs-west-indies",
]
for u in apis:
    try:
        raw = fetch(u)
        text = raw.decode("utf-8", "replace")
        is_html = text.lstrip().startswith("<!" )
        print("OK", u, "len", len(raw), "html" if is_html else "data")
        if not is_html:
            print(text[:2500])
            print("---")
        else:
            for key in ["winProbability", "status", "crr", "runs", "wickets", "overs", "target"]:
                if key in text:
                    idx = text.find(key)
                    print("near", key, re.sub(r"\s+", " ", text[max(0, idx-40):idx+120])[:160])
            # score lines
            for m in re.finditer(r"(\d{2,3}/\d)[^0-9]{0,5}\((\d{1,2}\.\d)", text):
                print("SCORELIKE", m.group(0)[:40])
    except Exception as ex:
        print("FAIL", u, ex)

# also HLTV / VLR quick
print("\n=== CS2 Astralis BIG ===")
for u in [
    "https://www.hltv.org/matches",
    "https://liquipedia.net/counterstrike/Astralis",
]:
    try:
        raw = fetch(u)
        text = raw.decode("utf-8", "replace")
        print("OK", u, len(raw))
        for m in re.finditer(r".{0,30}(Astralis|BIG).{0,50}", text):
            s = re.sub(r"\s+", " ", m.group(0))
            if "Astralis" in s and "BIG" in s:
                print("HIT", s[:120])
    except Exception as ex:
        print("FAIL", u, ex)

print("\n=== Valorant KC ===")
try:
    raw = fetch("https://www.vlr.gg/")
    text = raw.decode("utf-8", "replace")
    print("OK vlr", len(raw))
    for m in re.finditer(r".{0,20}(Karmine|Nongshim|RedForce).{0,60}", text, re.I):
        print("HIT", re.sub(r"\s+", " ", m.group(0))[:140])
except Exception as ex:
    print("FAIL vlr", ex)
