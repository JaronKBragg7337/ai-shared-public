"""
live-readings.py - balances the MSI can read, written to Supabase public.live_readings for the Control Room's
Balances tab (2026-10-25, Claude Code; Jaron: "no way of seeing DeepSeek's API credits").

Runs hourly as the Windows task "HB Live Readings". Each reading is one row; add a reader below for a new balance.
Prints names and amounts only, never key values.
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, __import__("os").path.dirname(__file__))
from settings import _env  # noqa: E402


def deepseek(env):
    req = urllib.request.Request("https://api.deepseek.com/user/balance",
                                 headers={"Authorization": f"Bearer {env['DEEPSEEK_API_KEY']}"})
    d = json.load(urllib.request.urlopen(req, timeout=30))
    infos = d.get("balance_infos", [])
    total = sum(float(b.get("total_balance", 0)) for b in infos)
    granted = sum(float(b.get("granted_balance", 0)) for b in infos)
    cur = infos[0].get("currency", "USD") if infos else "USD"
    value = f"${total:.2f}" if cur == "USD" else f"{total:.2f} {cur}"
    note = f"{value} left" + (f" (incl. ${granted:.2f} free credit)" if granted else "")
    return {"key": "deepseek_balance", "label": "DeepSeek API credit", "value": value, "sort": 10,
            "source": "api.deepseek.com/user/balance, hourly",
            "meaning": note + ". Pay-as-you-go: every DeepSeek call spends from this. "
                       + ("Usable." if d.get("is_available") else "NOT usable - top up at platform.deepseek.com.")}


READERS = [deepseek]


def main():
    env = _env()
    url, key = env.get("SUPABASE_URL"), env.get("SUPABASE_SERVICE_ROLE_KEY")
    rows = []
    for fn in READERS:
        try:
            r = fn(env)
            r["updated_at"] = datetime.now(timezone.utc).isoformat()
            rows.append(r)
            print(f"{r['label']}: {r['value']}")
        except Exception as e:
            print(f"{fn.__name__}: failed ({str(e)[:80]})")
    if rows and url and key:
        req = urllib.request.Request(f"{url.rstrip('/')}/rest/v1/live_readings?on_conflict=key", method="POST",
                                     data=json.dumps(rows).encode(),
                                     headers={"apikey": key, "Authorization": f"Bearer {key}",
                                              "Content-Type": "application/json",
                                              "Prefer": "resolution=merge-duplicates,return=minimal"})
        urllib.request.urlopen(req, timeout=15)


if __name__ == "__main__":
    main()
