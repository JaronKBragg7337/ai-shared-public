"""News PAPER book. No orders, accounts, brokers, or exchanges are involved.

Daily: python tools/news_paper_book.py
A decision uses the news and last completed closes; entries wait for a subsequent
market close. A direct, stateless local model request has no tools or file access.
"""
import calendar
import csv
import io
import json
import math
import os
import sys
import tempfile
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / 'state' / 'news-paper-book.json'
REPORT = ROOT / 'state' / 'news-paper-book.md'
WIRE = Path(r'C:\Users\lilli\Projects\watch\wire')
ET = ZoneInfo('America/New_York')
SYMBOLS = ('SPY', 'QQQ', 'XLE', 'USO', 'GLD', 'ITA', 'TLT', 'UUP')
HORIZONS = ('1 week', '1 month', '3 months')
MODEL = 'qwen3.5:9b'


def request(url, data=None, timeout=30):
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'NewsPaperBook/1.0', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode('utf-8-sig')


def prices(symbol, now):
    # 11/9: Stooq now serves a JavaScript bot check, so daily closes come from Yahoo's free chart endpoint.
    raw = request('https://query1.finance.yahoo.com/v8/finance/chart/' + symbol.upper() + '?range=1y&interval=1d')
    data = json.loads(raw)['chart']['result'][0]
    stamps = data.get('timestamp') or []
    closes = (data.get('indicators', {}).get('adjclose') or [{}])[0].get('adjclose') or data['indicators']['quote'][0]['close']
    tz = timezone(timedelta(seconds=data['meta'].get('gmtoffset', -18000)))
    rows = {}
    for ts, close in zip(stamps, closes):
        try:
            day = datetime.fromtimestamp(ts, tz).date()
            # At 9:05 today's bar is incomplete. A late run can use today's
            # close as input but is never entered at that same close.
            if day > now.date() or (day == now.date() and now.hour * 60 + now.minute < 990):
                continue
            if close is not None and math.isfinite(close) and close > 0:
                rows[day.isoformat()] = float(close)
        except (ValueError, TypeError, OSError):
            continue
    if not rows:
        raise ValueError('no completed daily closes for ' + symbol)
    return rows


def expiry(entry, horizon):
    d = date.fromisoformat(entry)
    if horizon == '1 week':
        return (d + timedelta(days=7)).isoformat()
    months = 1 if horizon == '1 month' else 3
    month = d.month + months
    year = d.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    return date(year, month, min(d.day, calendar.monthrange(year, month)[1])).isoformat()


def validate(response, news):
    obj = json.loads(response)
    calls = obj.get('calls') if isinstance(obj, dict) else None
    if not isinstance(calls, list) or len(calls) > 3:
        raise ValueError('model must return a calls array of 0 to 3')
    result = []
    for c in calls:
        if not isinstance(c, dict):
            raise ValueError('call is not an object')
        symbol, direction, horizon = c.get('etf'), c.get('direction'), c.get('horizon')
        size, story, reason = c.get('size_pct'), c.get('story'), c.get('reason')
        if symbol not in SYMBOLS or direction not in ('long', 'short') or horizon not in HORIZONS:
            raise ValueError('unsupported ETF, direction, or horizon')
        if isinstance(size, bool) or not isinstance(size, (int, float)) or not math.isfinite(size) or not 0 < size <= 10:
            raise ValueError('size must be above 0 and at most 10 percent')
        if not isinstance(story, str) or len(story.strip()) < 12 or story.strip().lower() not in news.lower():
            raise ValueError('story must be an exact named excerpt from the news list, at least 12 characters')
        if not isinstance(reason, str) or not 10 <= len(reason.strip()) <= 300 or '\n' in reason or '\r' in reason:
            raise ValueError('reason must be a single line of 10 to 300 characters')
        result.append({'etf': symbol, 'direction': direction, 'horizon': horizon, 'size_pct': size,
                       'story': story.strip(), 'reason': reason.strip(), 'status': 'pending'})
    return result


def ask_model(news, latest):
    schema = {'type': 'object', 'properties': {'calls': {'type': 'array', 'maxItems': 3, 'items': {
        'type': 'object', 'properties': {'etf': {'type': 'string', 'enum': list(SYMBOLS)},
        'direction': {'type': 'string', 'enum': ['long', 'short']},
        'horizon': {'type': 'string', 'enum': list(HORIZONS)},
        'size_pct': {'type': 'number', 'exclusiveMinimum': 0, 'maximum': 10},
        'story': {'type': 'string'}, 'reason': {'type': 'string'}},
        'required': ['etf', 'direction', 'horizon', 'size_pct', 'story', 'reason']}}}, 'required': ['calls']}
    prompt = ('You are an independent PAPER-only news analyst. Give zero to three calls, or pass with an empty calls array. '
              'Use only the news and prices below. Consider competing explanations and avoid assuming one event causes a price move. '
              'Choose only the supplied ETFs, long or short, and one of the supplied horizons. Each size is a percent of a hypothetical '
              '$10,000 account, greater than zero and at most 10. Copy a named story as an exact excerpt of at least 12 characters '
              'from the news. Give one short line explaining the connection. No tools, past calls, or portfolio are provided.\n\n'
              'Last completed daily closes (date and USD):\n' + json.dumps(latest) + '\n\nNews list:\n' + news)
    payload = json.dumps({'model': MODEL, 'messages': [{'role': 'user', 'content': prompt}],
                          'stream': False, 'think': False, 'format': schema,
                          'options': {'temperature': 0.2, 'num_predict': 1200, 'num_ctx': 32768}}).encode('utf-8')
    response = json.loads(request('http://127.0.0.1:11434/api/chat', payload, timeout=600))
    message = response.get('message', {})
    if message.get('tool_calls'):
        raise ValueError('model requested a tool; no calls were accepted')
    return validate(message.get('content', ''), news)


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix=path.name + '.', suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(value, f, indent=2, ensure_ascii=False, allow_nan=False)
            f.write('\n')
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def mark_book(book, bars):
    for run in book['runs']:
        for c in run['calls']:
            if c['status'] in ('settled', 'declined'):
                continue
            etf = bars.get(c['etf'], {})
            spy = bars.get('SPY', {})
            # Matched dates permit an equal-dollar SPY comparison for every call.
            common = sorted(set(etf) & set(spy))
            if c['status'] == 'pending':
                eligible = [d for d in common if d >= c['entry_not_before']]
                if not eligible:
                    continue
                d = eligible[0]
                c.update(status='open', entry_date=d, entry_close=etf[d], spy_entry_close=spy[d],
                         due_date=expiry(d, c['horizon']))
            eligible = [d for d in common if d >= c['entry_date']]
            due = [d for d in eligible if d >= c['due_date']]
            if not eligible:
                continue
            day = due[0] if due else eligible[-1]
            # A delayed or truncated source response must not roll an existing
            # mark backwards and misrepresent an older price as the latest.
            if c.get('mark_date') and day < c['mark_date']:
                continue
            amount = 10000 * c['size_pct'] / 100
            sign = 1 if c['direction'] == 'long' else -1
            pnl = amount * sign * (etf[day] / c['entry_close'] - 1)
            spy_pnl = amount * (spy[day] / c['spy_entry_close'] - 1)
            c.update(mark_date=day, mark_close=etf[day], spy_mark_close=spy[day],
                     pnl=round(pnl, 2), spy_pnl=round(spy_pnl, 2))
            if due:
                c['status'] = 'settled'
                c['result'] = 'win' if pnl > 0 else 'loss' if pnl < 0 else 'flat'


def clean(s):
    return str(s).replace('|', '/').replace('\n', ' ').replace('\r', ' ').replace('—', '-').replace('–', '-')


def report(book, now, errors):
    calls = [c for r in book['runs'] for c in r['calls']]
    settled = [c for c in calls if c['status'] == 'settled']
    opened = [c for c in calls if c['status'] == 'open']
    pending = [c for c in calls if c['status'] == 'pending']
    declined = [c for c in calls if c['status'] == 'declined']
    wins = sum(c['result'] == 'win' for c in settled)
    passes = sum(not r['calls'] for r in book['runs'])
    lines = [f'# News PAPER book (updated {now:%Y-%m-%d %H:%M %Z})', '',
             'Paper only. No real money or orders. Each call uses a fixed percentage of the starting $10,000, with no compounding. The combined gross size of open calls and calls waiting for entry cannot exceed $10,000; extra calls are declined after the independent model decides.',
             'News and completed prices alone go to a fresh local model request with no tools or prior conversation. A decision before 1 PM Eastern enters at that day\'s close; later decisions enter at the next available close. The early cutoff also avoids backdating on early-close days. Due dates use calendar weeks/months; weekends and holidays settle at the next available close.',
             'Prices are Yahoo Finance daily closes, with no fees, slippage, short borrow costs or dividends explicitly modeled. Marks show their actual date and may be stale when prices are unavailable.',
             f'Runs: {len(book["runs"])}. Passes: {passes}. Declined for account limit: {len(declined)}. Settled: {len(settled)}. Wins: {wins}. Hit rate: ' + (f'{100*wins/len(settled):.1f}%' if settled else 'not yet available') + '.',
             'Flat calls count in the settled total but are not wins. A pass is a decision, not a win or loss.', '',
             'SPY comparison: for each call, the same paper dollars buy SPY over the same entry and mark or settlement dates. This is a matched-exposure comparison, not one continuous $10,000 buy-and-hold account.',
             f'Settled paper P&L: ${sum(c.get("pnl", 0) for c in settled):+.2f}; matched SPY: ${sum(c.get("spy_pnl", 0) for c in settled):+.2f}.',
             f'Open paper P&L: ${sum(c.get("pnl", 0) for c in opened):+.2f}; matched SPY: ${sum(c.get("spy_pnl", 0) for c in opened):+.2f}.']
    if errors:
        lines += ['', 'Latest run notes: ' + clean('; '.join(errors))]
    lines += ['', '## Waiting for entry close', '| Decision date | ETF | Direction | Horizon | Size | Story and reason |', '|---|---|---|---|---|---|']
    for c in pending:
        lines.append(f'| {c["decision_date"]} | {c["etf"]} | {c["direction"]} | {c["horizon"]} | {c["size_pct"]}% | {clean(c["story"])}: {clean(c["reason"])} |')
    if not pending: lines.append('| None | | | | | |')
    lines += ['', '## Declined calls', '| Decision date | ETF | Direction | Horizon | Size | Story and reason |', '|---|---|---|---|---|---|']
    for c in declined:
        lines.append(f'| {c["decision_date"]} | {c["etf"]} | {c["direction"]} | {c["horizon"]} | {c["size_pct"]}% | {clean(c["story"])}: {clean(c["reason"])} |')
    if not declined: lines.append('| None | | | | | |')
    for title, rows in [('Open calls', opened), ('Settled calls', settled)]:
        lines += ['', '## ' + title, '| Decision | ETF | Direction | Horizon | Size | Entry close | Mark or exit close | Paper P&L | SPY P&L | Story and reason |', '|---|---|---|---|---|---|---|---|---|---|']
        for c in rows:
            lines.append(f'| {c["decision_date"]} | {c["etf"]} | {c["direction"]} | {c["horizon"]} | {c["size_pct"]}% | {c["entry_date"]} ${c["entry_close"]:.2f} | {c["mark_date"]} ${c["mark_close"]:.2f} | ${c["pnl"]:+.2f} | ${c["spy_pnl"]:+.2f} | {clean(c["story"])}: {clean(c["reason"])} |')
        if not rows: lines.append('| None | | | | | | | | | |')
    for title, key, values in [('horizon', 'horizon', HORIZONS), ('ETF', 'etf', SYMBOLS)]:
        lines += ['', '## Settled by ' + title, '| ' + title + ' | Calls | Wins | Paper P&L | Matched SPY P&L |', '|---|---|---|---|---|']
        for v in values:
            group = [c for c in settled if c[key] == v]
            lines.append(f'| {v} | {len(group)} | {sum(c["result"] == "win" for c in group)} | ${sum(c["pnl"] for c in group):+.2f} | ${sum(c["spy_pnl"] for c in group):+.2f} |')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    now = datetime.now(ET)
    today = now.date().isoformat()
    book = json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {'version': 1, 'runs': []}
    bars, errors = {}, []
    for symbol in SYMBOLS:
        try:
            bars[symbol] = prices(symbol, now)
        except Exception as e:
            errors.append(f'{symbol} prices unavailable ({type(e).__name__}: {e})')
    mark_book(book, bars)
    # Save marks before the model/network work, so an error never loses settlements.
    save_json(STATE, book)
    if not any(r['date'] == today for r in book['runs']):
        try:
            news = (WIRE / (today + '-top.md')).read_text(encoding='utf-8')
            if not news.strip(): raise ValueError('news list is empty')
            if len(bars) != len(SYMBOLS): raise ValueError('all ETF prices are required for a decision')
            latest = {s: {'date': max(bars[s]), 'close': bars[s][max(bars[s])]} for s in SYMBOLS}
            # Fail closed rather than using a stale input as today's market context.
            if any((now.date() - date.fromisoformat(v['date'])).days > 5 for v in latest.values()):
                raise ValueError('at least one latest price is more than five days old')
            calls = ask_model(news, latest)
            decided = datetime.now(ET)
            if decided.date().isoformat() != today:
                raise ValueError('date changed during the model request; retry with the new day\'s news')
            first_day = decided.date() if decided.hour * 60 + decided.minute < 780 else decided.date() + timedelta(days=1)
            used = sum(c['size_pct'] for run in book['runs'] for c in run['calls'] if c['status'] in ('pending', 'open'))
            for c in calls:
                c.update(decision_date=today, decision_at=decided.isoformat(timespec='seconds'), entry_not_before=first_day.isoformat())
                if used + c['size_pct'] > 100 + 1e-9:
                    c.update(status='declined', declined_reason='The $10,000 gross account limit is full')
                else:
                    used += c['size_pct']
            book['runs'].append({'date': today, 'at': decided.isoformat(timespec='seconds'), 'model': MODEL,
                                 'context': {'news_list': today + '-top.md', 'completed_prices': latest,
                                             'workspace': False, 'open_positions': False, 'past_results': False,
                                             'prior_conversation': False, 'tools': False}, 'calls': calls})
            save_json(STATE, book)
        except Exception as e:
            errors.append(f'No decision recorded; retry today ({type(e).__name__}: {e})')
    report(book, datetime.now(ET), errors)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('Paper book updated: ' + str(REPORT))
    return 0


if __name__ == '__main__':
    # One writer at a time, even if a manual run overlaps the scheduled run.
    # OS file locks are released on exit or crash; the tiny lock file is reusable.
    lock_path = ROOT / 'state' / '.news-paper-book.lock.tmp'
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, 'a+b') as lock:
        lock.seek(0)
        if os.name == 'nt':
            import msvcrt
            try:
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                sys.exit('News paper book is already running; retry later.')
        else:
            import fcntl
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                sys.exit('News paper book is already running; retry later.')
        sys.exit(main())
