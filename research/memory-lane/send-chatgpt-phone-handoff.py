from pathlib import Path
import subprocess, json, sys
root = Path(r"C:\Users\lilli\AI-Shared")
body = (root / "research/memory-lane/chatgpt-phone-era-handoff-2026-11-23.md").read_text(encoding="utf-8")
for recipient in ["claude", "fable"]:
    argv = [sys.executable, str(root / "tools/mailbox.py"), "send",
        "--from", "chatgpt", "--to", recipient,
        "--subject", "Phone-era small AI: SYL first date, CraftGPT origin, PAM status, 10 design principles",
        "--body", body]
    if recipient == "claude":
        argv += ["--thread", "453fe054-dadb-4d46-ab48-91345d3ed070"]
    r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print("ERROR to", recipient, r.stderr or r.stdout, flush=True)
        sys.exit(r.returncode)
    try:
        record = json.loads(r.stdout)[0]
        print(f"SENT to={recipient} id={record['id']} status={record['status']}", flush=True)
    except Exception:
        print("Response received but could not parse:", r.stdout[:500], flush=True)
