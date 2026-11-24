"""AI mailbox: python tools/mailbox.py --help. Uses ~/.secrets/keys.env."""
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request, uuid
if sys.stdout: sys.stdout.reconfigure(encoding="utf-8")   # 11/22: pythonw (Task Scheduler) has no stdout; this line crashed every pythonw caller since 11/10
from pathlib import Path

def settings():
    values = {}
    path = Path.home() / '.secrets' / 'keys.env'
    if path.exists():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            line = line.strip()
            if line.startswith('export '): line = line[7:]
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1); values[k.strip()] = v.strip().strip('\"').strip("'")
    url = os.environ.get('SUPABASE_URL') or values.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY') or values.get('SUPABASE_SERVICE_ROLE_KEY')
    if not url or not key: raise ValueError('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in ~/.secrets/keys.env')
    return url.rstrip('/'), key

def request(method, query='', data=None):
    url, key = settings()
    req = urllib.request.Request(url + '/rest/v1/ai_mailbox' + query, data=None if data is None else json.dumps(data).encode(), method=method, headers={'apikey': key, 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json', 'Prefer': 'return=representation'})
    try:
        with urllib.request.urlopen(req, timeout=20) as response: return json.load(response)
    except urllib.error.HTTPError as e:
        raise RuntimeError('Mailbox request failed (HTTP %s)' % e.code) from None
    except urllib.error.URLError:
        raise RuntimeError('Could not reach mailbox') from None

def ident(value):
    try: return str(uuid.UUID(value))
    except ValueError: raise argparse.ArgumentTypeError('Use a valid message or thread UUID')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    s = sub.add_parser('send'); s.add_argument('--from', dest='sender', required=True); s.add_argument('--to', required=True); s.add_argument('--subject', required=True); s.add_argument('--body', required=True); s.add_argument('--thread', type=ident)
    l = sub.add_parser('list'); l.add_argument('--to', required=True); l.add_argument('--status', choices=['new','read','done']); l.add_argument('--limit', type=int, default=50)
    r = sub.add_parser('read'); r.add_argument('id', type=ident)
    d = sub.add_parser('mark-done'); d.add_argument('id', type=ident)
    a = parser.parse_args()
    if a.command == 'send':
        row = {'from_ai': a.sender.strip().lower(), 'to_ai': a.to.strip().lower(), 'subject': a.subject.strip(), 'body': a.body.strip()}
        if a.thread: row['thread_id'] = a.thread
        result = request('POST', data=row)
    elif a.command == 'list':
        if not 1 <= a.limit <= 500: parser.error('--limit must be 1 to 500')
        q = {'to_ai': 'eq.' + a.to.strip().lower(), 'order': 'created_at.desc', 'limit': str(a.limit)}
        if a.status: q['status'] = 'eq.' + a.status
        result = request('GET', '?' + urllib.parse.urlencode(q))
    elif a.command == 'read':
        result = request('GET', '?id=eq.' + a.id)
        if result and result[0]['status'] == 'new':
            changed = request('PATCH', '?id=eq.' + a.id + '&status=eq.new', {'status': 'read'})
            if changed: result = changed
    else: result = request('PATCH', '?id=eq.' + a.id, {'status': 'done'})
    if not result and a.command in ('read', 'mark-done'): raise ValueError('Message not found')
    print(json.dumps(result, indent=2, ensure_ascii=False))
if __name__ == '__main__':
    try: main()
    except (ValueError, RuntimeError) as e: print(str(e), file=sys.stderr); sys.exit(1)
