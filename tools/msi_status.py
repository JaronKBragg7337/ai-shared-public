"""MSI health + system snapshot (Jaron 10/21: "keep an eye on if the MSI is overheating, charging, memory space ... with me not
being there to see most times"). Every 30 min (task "MSI Status"): writes state/MSI-STATUS.md (latest) and appends one line to
state/msi-status.log (history). Buzzes Jaron's phone only for real trouble, at most once per problem per 6 h.
Shows: GPU temp/load/memory, battery + charging, RAM, disk, uptime, what heavy work is running (news render, engine, Sapling,
builders), connectors (from login-watch), and the scheduled tasks that failed last run."""
import os, subprocess, json, time, datetime, shutil, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
NOWIN = 0x08000000
LIMITS = {"gpu_temp_c": 87, "disk_free_gb": 80, "ram_free_gb": 1.5, "battery_low_pct": 30}


def sh(cmd, ps=False, timeout=60):
    try:
        args = ["powershell", "-NoProfile", "-Command", cmd] if ps else cmd
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout, creationflags=NOWIN).stdout.strip()
    except Exception as e:
        return ""


def ntfy(msg, key):
    flag = os.path.join(ROOT, "state", f".msi-alert-{key}")
    if os.path.exists(flag) and time.time() - os.path.getmtime(flag) < 6 * 3600: return
    topic = ""
    for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8"):
        if l.startswith("NTFY_TOPIC="): topic = l.split("=", 1)[1].strip()
    if topic:
        try: urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + topic, msg.encode(), {"Title": "MSI health"}), timeout=15)
        except Exception: pass
    open(flag, "w").write(msg)


def main():
    now = datetime.datetime.now()
    g = sh(["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw", "--format=csv,noheader,nounits"]).split(",")
    gpu = {"temp": int(g[0]), "load": int(g[1]), "mem": f"{int(g[2])/1024:.1f}/{int(g[3])/1024:.0f} GB", "watts": float(g[4])} if len(g) >= 5 else {}
    # 10/27: Win32_Battery froze at 94% "AC" for days while the MSI was unplugged; PowerStatus is live.
    bat = sh("Add-Type -AssemblyName System.Windows.Forms; $p=[System.Windows.Forms.SystemInformation]::PowerStatus; '{0} {1}' -f [int]($p.BatteryLifePercent*100), $p.PowerLineStatus", ps=True).split()
    pct = int(bat[0]) if bat and bat[0].isdigit() else None
    charging = (bat[1] == "Online") if len(bat) > 1 and bat[1] in ("Online", "Offline") else None
    mem = sh("$o=Get-CimInstance Win32_OperatingSystem; \"$($o.FreePhysicalMemory) $($o.TotalVisibleMemorySize) $($o.LastBootUpTime.ToString('s'))\"", ps=True).split()
    ram_free = int(mem[0]) / 1048576 if mem else None
    ram_tot = int(mem[1]) / 1048576 if len(mem) > 1 else None
    boot = mem[2] if len(mem) > 2 else "?"
    disk = shutil.disk_usage("C:\\").free / 1e9
    procs = sh("Get-CimInstance Win32_Process | % { $_.Name + ' ' + $_.CommandLine }", ps=True).lower()
    heavy = [name for name, needle in (("news render (Unreal)", "unrealeditor"), ("engine render", "render.mjs"), ("Sapling", "sapling"),
                                       ("Blender", "blender.exe"), ("a builder AI (claude/codex/grok)", "claude.exe -p"), ("ffmpeg", "ffmpeg"))
             if needle in procs]
    failed = sh("Get-ScheduledTask | ? { $_.State -notin 'Disabled','Running' -and $_.TaskPath -eq '\\' } | % { $i = $_ | Get-ScheduledTaskInfo; "
                "if ($i.LastTaskResult -notin 0,267009,267011,267014 -and $i.LastRunTime -gt (Get-Date).AddDays(-2)) { $_.TaskName + ' (' + $i.LastTaskResult + ')' } }",
                ps=True, timeout=120).splitlines()
    failed = [f for f in failed if not f.lower().startswith(("nv", "onedc", "nahimic", "npcap", "microsoft", "google", "opera", "ccleaner", "adobe", "onedrive"))]
    logins = ""
    try: logins = "\n".join(l for l in sh(["python", os.path.join(ROOT, "tools", "login-watch.py")], timeout=240).splitlines() if l.startswith("| NEEDS"))
    except Exception: pass

    problems = []
    if gpu and gpu["temp"] >= LIMITS["gpu_temp_c"]: problems.append(("gpu-hot", f"GPU is {gpu['temp']}C (limit {LIMITS['gpu_temp_c']}C) - check the MSI's vents/fans"))
    if disk < LIMITS["disk_free_gb"]: problems.append(("disk", f"only {disk:.0f} GB free - the news render needs ~70 GB"))
    if ram_free is not None and ram_free < LIMITS["ram_free_gb"]: problems.append(("ram", f"only {ram_free:.1f} GB of RAM free"))
    if pct is not None and charging is False: problems.append(("unplugged", f"the MSI is on battery ({pct}%) - is it unplugged?"))
    for key, msg in problems: ntfy("MSI: " + msg, key)

    lines = [f"# MSI status - {now:%a %b %d %I:%M %p} (updates every 30 min; tools/msi_status.py)", "",
             f"- **Health:** {'OK' if not problems else 'PROBLEM: ' + '; '.join(m for _, m in problems)}",
             f"- **GPU:** {gpu.get('temp', '?')}C, {gpu.get('load', '?')}% busy, memory {gpu.get('mem', '?')}, {gpu.get('watts', '?')} W",
             f"- **Power:** battery {pct}% , {'plugged in' if charging else 'ON BATTERY' if charging is False else '?'}",
             f"- **RAM:** {ram_free:.1f} GB free of {ram_tot:.0f} GB" if ram_free else "- **RAM:** ?",
             f"- **Disk C:** {disk:.0f} GB free",
             f"- **Up since:** {boot}",
             f"- **Heavy work running now:** {', '.join(heavy) or 'none'}",
             f"- **Scheduled tasks that failed in the last 2 days:** {', '.join(failed) or 'none'}",
             f"- **Logins that need Jaron:** " + ("\n" + logins if logins else "none")]
    open(os.path.join(ROOT, "state", "MSI-STATUS.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    # 10/21 (Jaron: "can it be another thing added to control room?") - the same readings on the Control Room's MSI tab
    try:
        e = {}
        for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8"):
            if "=" in l and not l.startswith("#"): k, v = l.strip().split("=", 1); e[k] = v.strip()
        vals = {"msi_health": "OK" if not problems else "PROBLEM: " + "; ".join(m for _, m in problems),
                "msi_gpu": f"{gpu.get('temp', '?')}C, {gpu.get('load', '?')}% busy, memory {gpu.get('mem', '?')}",
                "msi_power": f"battery {pct}%, {'plugged in' if charging else 'ON BATTERY' if charging is False else '?'}",
                "msi_space": f"RAM {ram_free:.1f} GB free of {ram_tot:.0f} GB; disk {disk:.0f} GB free",
                "msi_running": ", ".join(heavy) or "nothing heavy", "msi_failed": ", ".join(failed) or "none",
                "msi_logins": logins.replace("|", " ").strip() or "none needed", "msi_updated": now.strftime("%a %b %d, %I:%M %p")}
        H = {"apikey": e["SUPABASE_SERVICE_ROLE_KEY"], "Authorization": "Bearer " + e["SUPABASE_SERVICE_ROLE_KEY"], "Content-Type": "application/json"}
        base = e["SUPABASE_URL"].rstrip("/") + "/rest/v1/system_settings?key=eq."
        for k, v in vals.items():
            urllib.request.urlopen(urllib.request.Request(base + k, json.dumps({"value": v, "updated_by": "msi"}).encode(), H, method="PATCH"), timeout=20)
    except Exception as ex:
        print("control room update failed:", type(ex).__name__)
    open(os.path.join(ROOT, "state", "msi-status.log"), "a", encoding="utf-8").write(
        f"{now:%Y-%m-%d %H:%M} | gpu {gpu.get('temp', '?')}C {gpu.get('load', '?')}% | bat {pct}% {'AC' if charging else 'BAT'} | ram {ram_free:.1f}GB | disk {disk:.0f}GB | {', '.join(heavy) or '-'} | {len(problems)} problems\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
