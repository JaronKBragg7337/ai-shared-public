"""One-off reminder buzz for Jaron (child support callback, Mon 2026-11-02). Private wording, no names."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from watch_reply import reply
reply(sys.argv[1] if len(sys.argv) > 1 else "Reminder: child support office should call back today. Keep your phone close. If no call by 2 PM, call them back. Goal: pay \$100 online before court (Nov 10).")
