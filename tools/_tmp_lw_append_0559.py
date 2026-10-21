from datetime import datetime, timezone
path = r"C:\Users\lilli\AI-Shared\state\live-wire.md"
ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
line = (
    f"{ts} | SESSION | board 11 live / 0 flagged (05:57Z) | before: YES Lazaro 14.49sh cost USD10.22 mark USD12.75 (+USD2.53) | "
    f"confirmed ESPN Lazaro 6-1 Fruhvirtova S1 3-3 S2 vs YES 0.78/0.80; ESPN Kalieva 7-6 Shi S1 vs YES 0.72/0.73; "
    f"ESPN Bassols 6-4 2-1 Xiaodi S2 vs 0.85/0.87; ESPN Sasnovich 4-3 Lepchenko S1 vs 0.84/0.85 | "
    f"HOLD YES Lazaro 14.49 (kill not hit; Fruhvirtova never led S2 3-0, Lazaro broke back to 3-3) | no new trade | "
    f"closest skip: YES Kalieva @0.72 (won S1 7-6 ranking fav; TB-tight ~fair not hard lag) | "
    f"skipped: Bassols set+break chalk @0.86; Sasnovich early break chalk @0.84; ITF unconfirmed; crypto never | "
    f"quiet (no loss over USD5) | Open Live Wire: 1 (YES Lazaro 14.49sh @0.705)\n"
)
with open(path, "a", encoding="utf-8") as f:
    f.write(line)
print("appended", ts)
print(line)
