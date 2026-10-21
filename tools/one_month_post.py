# One-time: Heartbeat News one-month post on the Official account, Oct 18 2026 (Jaron 10/17). Removes its own task after.
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social_daily as sd
text = ("Heartbeat News is one month old today. 🎂\n"
        "From the first capture on September 18 through October 17: the Iran war ran from day 203 to day 232 with no public Hormuz deal, "
        "the Houthis and Saudi Arabia traded deadly strikes, and a Russia-Ukraine energy ceasefire announced October 12 did not hold. "
        "Brent settled at $109.86, Seoul had its worst week since 2008, and Kenya confirmed a third Ebola case.\n\n"
        "An AI read the whole month, including which claims checked out and which didn't. Every day, every source: "
        "https://www.heartbeatobservatory.com/news/archive/\n#news #AI")
sd.log("one-month post -> site " + sd.site_post(text))
subprocess.run(["schtasks", "/Delete", "/TN", "HB News One Month", "/F"], capture_output=True, creationflags=0x08000000)
