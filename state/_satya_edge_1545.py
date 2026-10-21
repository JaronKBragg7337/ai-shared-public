import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=25).read())

def wp(eid):
    s = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={eid}")
    wpl = s.get("winprobability") or []
    header = s.get("header") or {}
    comps = ((header.get("competitions") or [{}])[0].get("competitors") or [])
    status = ((header.get("competitions") or [{}])[0].get("status") or {}).get("type", {}).get("detail")
    home = next(c for c in comps if c.get("homeAway")=="home")
    away = next(c for c in comps if c.get("homeAway")=="away")
    hwp = wpl[-1]["homeWinPercentage"] if wpl else None
    return {
        "status": status,
        "away": away["team"]["abbreviation"], "away_score": away.get("score"),
        "home": home["team"]["abbreviation"], "home_score": home.get("score"),
        "home_wp": hwp,
        "away_wp": (None if hwp is None else 1-hwp),
    }

games = {
  "UVA-FSU": "401858253",
  "OHIO-KENT": "401866434",
  "EMU-MASS": "401866433",
  "ODU-GAST": "401869956",
  "LOU-NCSU": "401858248",
  "TOL-BALL": "401866431",
  "WMU-BUF": "401866432",
  "SYR-CONN": "401858252",
  "OSU-IOWA": "401858473",
  "AUB-TENN": "401856710",
  "CAL-UNLV": "401858247",
  "AKR-CMU": "401866430",
  "BGSU-MOH": "401866477",
}
for k,eid in games.items():
    try:
        r = wp(eid)
        print(k, json.dumps(r))
    except Exception as e:
        print(k, "ERR", e)

# polymarket gamma for a few slugs
slugs = [
  "aec-cfb-toledo-ballst-2026-10-03",
  "aec-cfb-lou-ncst-2026-10-03",
  "aec-cfb-vir-flst-2026-10-03",
  "aec-cfb-ohio-kentst-2026-10-03",
  "aec-cfb-old-gast-2026-10-03",
  "aec-cfb-syra-uconn-2026-10-03",
  "aec-cfb-wmich-buf-2026-10-03",
  "aec-cfb-ohiost-iowa-2026-10-03",
  "aec-cfb-aubrn-tenn-2026-10-03",
  "aec-cfb-cah-unlv-2026-10-03",
  "aec-cfb-elon-nhamp-2026-10-03",
  "atc-unl-mkd-sco-2026-10-03-sco",
  "atc-unl-sui-slo-2026-10-03-sui",
]
print("=== BOOKS ===")
for slug in slugs:
    try:
        # US gamma often via gamma-api.polymarket.com or clob
        url = f"https://gamma-api.polymarket.com/markets?slug={slug}"
        data = get(url)
        if isinstance(data, list) and data:
            m = data[0]
            print(slug, "bestBid", m.get("bestBid"), "bestAsk", m.get("bestAsk"), "outcomePrices", m.get("outcomePrices"), "question", (m.get("question") or "")[:80])
        else:
            # try events
            url2 = f"https://gamma-api.polymarket.com/events?slug={slug}"
            d2 = get(url2)
            print(slug, "event", type(d2).__name__, str(d2)[:200])
    except Exception as e:
        print(slug, "ERR", e)
