"""
settings.py - the Control Room's numbers, for the scripts on the MSI (2026-09-26, Claude Code).

Jaron edits the knobs at heartbeatobservatory.com/admin/control/ (Supabase public.system_settings). Every trading script asks
here instead of keeping its own copy, so a change in the Control Room changes everywhere. If Supabase can't be reached, each
script's built-in default is used - a network blip never stops trading or changes a limit by accident.

    from settings import setting
    MAX_SPREAD = setting("desk_max_spread", 0.05)
"""
import json
import os
import time
import urllib.request

_cache = {"at": 0.0, "rows": None}
SECRETS = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")


def _env():
    out = {}
    try:
        for line in open(SECRETS, encoding="utf-8"):
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"')
    except OSError:
        pass
    return out


def _rows():
    if _cache["rows"] is not None and time.time() - _cache["at"] < 60:
        return _cache["rows"]
    env = _env()
    url, key = env.get("SUPABASE_URL"), env.get("SUPABASE_SERVICE_ROLE_KEY")
    rows = {}
    if url and key:
        try:
            req = urllib.request.Request(f"{url.rstrip('/')}/rest/v1/system_settings?select=key,value",
                                         headers={"apikey": key, "Authorization": f"Bearer {key}"})
            rows = {r["key"]: r["value"] for r in json.load(urllib.request.urlopen(req, timeout=10))}
        except Exception:
            rows = {}
    _cache.update(at=time.time(), rows=rows)
    return rows


def setting(key, default):
    """The Control Room value for key, as the same type as default; default if unreachable or unset."""
    v = _rows().get(key)
    if v is None:
        return default
    try:
        return type(default)(v) if isinstance(default, (int, float)) and not isinstance(default, bool) else v
    except (TypeError, ValueError):
        return default
