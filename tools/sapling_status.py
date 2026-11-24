"""Build the twice-daily Sapling status from its timestamped ledger."""
import datetime as dt
import json
from pathlib import Path
import re
import sqlite3
import urllib.request
import subprocess

from settings import _env
from watch_reply import reply

ROOT = Path(__file__).resolve().parents[1]
SAP = Path('C:/Users/lilli/Projects/sapling')
OUT = ROOT / 'state/sapling-status.json'
NOTICE = ROOT / 'state/.sapling-status-notice.json'

def build():
    now = dt.datetime.now().astimezone()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    db = sqlite3.connect(f'file:{(SAP / "results/memory.db").as_posix()}?mode=ro', uri=True, timeout=10)
    def rows(kind, since=0, limit=100000):
        return [(ts, json.loads(p)) for ts, p in db.execute('select ts,payload from ledger where kind=? and ts>=? order by id desc limit ?', (kind, since, limit))]
    ticks = rows('tick', start)
    last = rows('tick', limit=1)
    folds = rows('consolidation', start)
    latest_folds = rows('consolidation', limit=2)
    practice = [p.get('result', {}) for _, p in ticks if p.get('action') == 'practice']
    last_chat = rows('chat', limit=1)
    consumed = rows('consumption', start)
    stops = rows('stop', start)
    said = [p.get('result', {}).get('said') for _, p in rows('tick', limit=3000) if p.get('result', {}).get('said')][:3]
    db.close()
    lastrow = last[0][1] if last else {}
    try:
        pid = int((SAP/'results/heartbeat.pid').read_text().strip())
        cmd = subprocess.run(['powershell', '-NoProfile', '-Command', f"(Get-CimInstance Win32_Process -Filter 'ProcessId={pid}').CommandLine"], capture_output=True, text=True, timeout=10, check=True).stdout
        awake = 'awake' if 'sapling.heartbeat run' in cmd else 'asleep'
    except FileNotFoundError:
        awake = 'asleep'
    except (ValueError, OSError, subprocess.SubprocessError):
        awake = 'unknown'
    card = json.loads((SAP/'results/report_card.json').read_text(encoding='utf-8'))
    exams = {}
    for c in sorted(card.get('history', []) + [card], key=lambda x: x.get('ts', '')):
        for e in c.get('exams', []):
            name = e.get('exam', '').split('_')[0]
            if name in ('E1', 'E2', 'E5', 'E6', 'E7', 'E7L') and e.get('score'):
                exams[name] = {'score': e['score'], 'date': c.get('ts'), 'generation': c.get('generation')}
    for f in sorted((SAP/'results/conversation').glob('*.json')):
        try:
            c = json.loads(f.read_text(encoding='utf-8'))
            if c.get('name_thread', {}).get('score'):
                exams['name-thread'] = {'score': c['name_thread']['score'], 'date': c.get('ts'), 'generation': c.get('generation'), 'label': c.get('label', '')}
        except (ValueError, OSError):
            pass
    today = now.strftime('%Y-%m-%d')
    day = [line for line in (ROOT/'state/cloud-gpu-log.md').read_text(encoding='utf-8').splitlines() if line.startswith(today+' ')]
    starts, intervals = {}, []
    for line in (ROOT/'state/cloud-gpu-log.md').read_text(encoding='utf-8').splitlines():
        parts = [x.strip() for x in line.split('|')]
        if len(parts) < 7 or parts[2] not in ('START', 'TERMINATE'):
            continue
        try:
            when = dt.datetime.strptime(parts[0], '%Y-%m-%d %I:%M %p').astimezone()
        except ValueError:
            continue
        if parts[2] == 'START':
            rate = re.search(r'\$(\d+(?:\.\d+)?)/hr', parts[-1])
            if rate:
                starts[parts[3]] = (when, float(rate.group(1)))
        elif parts[3] in starts:
            begin, rate = starts.pop(parts[3])
            intervals.append((begin, when, rate))
    intervals += [(begin, now, rate) for begin, rate in starts.values()]
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    cost = sum(max(0, (min(end, now)-max(begin, midnight)).total_seconds()) * rate / 3600 for begin, end, rate in intervals)
    loss = [{'generation': p.get('generation'), 'first': p.get('loss_first'), 'last': p['loss_last']} for _, p in reversed(latest_folds) if p.get('loss_last') is not None]
    return {'updated': now.isoformat(timespec='seconds'), 'state': awake, 'last_action': lastrow.get('action'),
            'generation': lastrow.get('state', {}).get('generation', card.get('generation')), 'ticks_today': len(ticks),
            'practice': {'ok': sum(p.get('ok', 0) for p in practice), 'total': sum(p.get('n', 0) for p in practice)},
            'folds_today': len(folds), 'new_facts_today': sum(p.get('facts_new', 0) for _, p in folds),
            'loss': loss, 'exams': exams, 'said': said, 'gpu_spend_estimate': round(cost, 2),
            'gpu_cost_note': 'estimate from logged start and stop times and hourly rates; rounded times and unpriced runs can change the bill',
            'last_learned': dt.datetime.fromtimestamp(latest_folds[0][0]).astimezone().isoformat(timespec='minutes') if latest_folds else None,
            'last_chat': dt.datetime.fromtimestamp(last_chat[0][0]).astimezone().isoformat(timespec='minutes') if last_chat else None,
            'taken_in_today': len(consumed),
            'stops_today': [{'at': dt.datetime.fromtimestamp(ts).strftime('%H:%M'), 'by': p.get('who'), 'why': p.get('reason')} for ts, p in stops],
            'training_day': any('| START |' in line for line in day)}

def publish(status):
    env = _env()
    key = env['SUPABASE_SERVICE_ROLE_KEY']
    url = env['SUPABASE_URL'].rstrip('/') + '/rest/v1/sapling_status'
    body = json.dumps({'id': 1, 'updated_at': status['updated'], 'state': status}).encode()
    req = urllib.request.Request(url, data=body, headers={'apikey': key, 'Authorization': 'Bearer '+key, 'Content-Type': 'application/json', 'Prefer': 'resolution=merge-duplicates,return=minimal'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status

def main():
    s = build()
    OUT.write_text(json.dumps(s, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    exams = '; '.join(f"{k}: {v['score']} ({v.get('date', '')}, {v.get('label', 'report')})" for k, v in s['exams'].items())
    loss = '; '.join(f"gen {x['generation']}: {x['first']} to {x['last']}" for x in s['loss']) or 'not recorded'
    text = f"# Sapling status\n\nUpdated {s['updated']}\n\n- {s['state']}; last action: {s['last_action']}. Generation {s['generation']}.\n- Today: {s['ticks_today']} ticks; practice {s['practice']['ok']}/{s['practice']['total']}; {s['folds_today']} folds, {s['new_facts_today']} new facts.\n- Loss (lower is better): {loss}.\n- Exams: {exams}.\n- GPU: ${s['gpu_spend_estimate']:.2f} estimated; {s['gpu_cost_note']}.\n- Last things said: " + (' | '.join(s['said']) or 'none recorded')+'\n'
    stops = ', '.join(f"{x['at']} ({x['by']}: {x['why']})" for x in s['stops_today']) or 'none'
    text += (f"- Last time it learned (new version made): {s['last_learned'] or 'not recorded'}.\n"
             f"- Last chat with a person: {s['last_chat'] or 'never'}.\n"
             f"- Turns it processed today (tiny inputs, not new lessons): {s['taken_in_today']}.\n"
             f"- Stops today: {stops}. (The 4 AM news render pauses it for the GPU; that is logged as an owner stop.)\n")
    (ROOT/'state/sapling-status.md').write_text(text, encoding='utf-8')
    publish(s)
    previous = json.loads(NOTICE.read_text(encoding='utf-8')) if NOTICE.exists() else {}
    today = s['updated'][:10]
    changed = bool(previous) and (s['generation'] != previous.get('generation') or s['exams'] != previous.get('exams'))
    if (s['training_day'] or changed) and previous.get('notified_day') != today:
        reply(f"Sapling: generation {s['generation']}, {s['folds_today']} folds and {s['new_facts_today']} new facts today; GPU estimate ${s['gpu_spend_estimate']:.2f}.")
        previous['notified_day'] = today
    previous.update(generation=s['generation'], exams=s['exams'])
    NOTICE.write_text(json.dumps(previous, indent=2)+'\n', encoding='utf-8')
    print('Sapling status updated and published')

if __name__ == '__main__':
    main()
