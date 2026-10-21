#!/usr/bin/env python3
"""Merge the named personal finance exports into projects/life/ledger-all.md.

Read-only on source files. Re-run with: python tools/ledger-merge.py
"""
from __future__ import annotations
import csv, json, re
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIFE = ROOT / 'projects' / 'life'
START, END = date(2026, 7, 1), date.today()

def dec(x):
    try: return Decimal(str(x))
    except (InvalidOperation, TypeError): return Decimal(0)

def money(x):
    return '' if x is None or x == 0 else f"${abs(x):,.2f}"

def parse_date(s):
    return date.fromisoformat(s[:10])

def read_bank():
    rows=[]
    for line in (LIFE/'bank-ledger.md').read_text(encoding='utf-8').splitlines():
        m=re.match(r'^\| (\d{4}-\d\d-\d\d) \| ([+-])\$([\d,]+\.\d\d) \| (.*?) \| (.*?) \|$', line)
        if not m: continue
        dt=parse_date(m[1]);
        if not START <= dt <= END: continue
        a,b=(x.strip() for x in m[4].split('→',1)) if '→' in m[4] else ('Unclear','Unclear')
        val=dec(m[3].replace(',','')) * (1 if m[2]=='+' else -1)
        desc=m[5]
        rows.append(dict(date=dt,account=b if val>0 else a,amount=val,from_=a,to=b,what=desc,
                         counter=a if val>0 else b,source='bank', transfer=('transfer' in desc.lower() or '→' in m[4] and a.startswith('Chime') and b.startswith('Chime'))))
    return rows

def read_uphold():
    rows=[]
    with (LIFE/'uphold-transactions.csv').open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            dt=datetime.strptime(r['Date'][:24], '%a %b %d %Y %H:%M:%S').date()
            if not START <= dt <= END or r.get('Status','').lower() not in ('completed','complete'): continue
            typ=r['Type'].lower(); dest,orig=r['Destination Currency'],r['Origin Currency']
            amount=dec(r['Destination Amount']) if dest=='USD' else dec(r['Origin Amount']) if orig=='USD' else Decimal(0)
            if typ=='out': signed=-amount
            elif typ=='in': signed=amount
            else: signed=Decimal(0)
            what=f"Uphold {typ}: {r['Origin Amount']} {orig} → {r['Destination Amount']} {dest}"
            if typ=='out': what += ' (card spend from crypto to USD)'
            if amount==0: what += ' (non-USD crypto transfer; USD value unavailable)'
            rows.append(dict(date=dt,account='Uphold',amount=signed,from_=r['Origin'],to=r['Destination'],counter='Unclear / external',what=what,source='uphold',transfer=typ=='transfer'))
    return rows

def read_pm():
    rows=[]; trades=[]
    data=json.loads((ROOT/'state'/'polymarket-activities-all.json').read_text(encoding='utf-8'))
    for a in data:
        typ=a.get('type',''); obj=a.get('accountBalanceChange',{})
        if typ.startswith('ACTIVITY_TYPE_ACCOUNT_') or typ=='ACTIVITY_TYPE_TRANSFER':
            t=obj.get('createTime') or obj.get('updateTime');
            if not t: continue
            dt=parse_date(t)
            if not START<=dt<=END or obj.get('status')!='ACCOUNT_BALANCE_CHANGE_STATUS_COMPLETED': continue
            amt=dec((obj.get('amount') or {}).get('value')); desc=obj.get('description') or typ.replace('ACTIVITY_TYPE_','').replace('_',' ').title()
            isout='WITHDRAWAL' in typ
            rows.append(dict(date=dt,account='Polymarket',amount=-amt if isout else amt,from_='Polymarket' if isout else 'Unclear',to='Unclear' if isout else 'Polymarket',counter='Unclear (payment method omitted)' if ('Apple Pay' in desc or isout) else 'Polymarket',what=desc,source='pm',transfer=True))
        elif typ=='ACTIVITY_TYPE_TRADE':
            t=a.get('trade',{}); ex=t.get('aggressorExecution',{}); order=ex.get('order',{})
            if order.get('manualOrderIndicator')=='MANUAL_ORDER_INDICATOR_AUTOMATIC': actor='bot/automatic'
            elif order.get('manualOrderIndicator')=='MANUAL_ORDER_INDICATOR_MANUAL': actor='Jaron/manual'
            else: actor='actor unclear'
            tm=order.get('lastTransactTime') or order.get('insertTime') or order.get('createTime')
            if not tm: continue
            dt=parse_date(tm)
            if not START<=dt<=END: continue
            q=dec(ex.get('quantity') or order.get('cumQuantity')); px=dec((ex.get('price') or order.get('price') or {}).get('value'))
            trades.append((dt,actor,order.get('action','unspecified'),q*px))
    return rows,trades

def merge_transfers(rows):
    # Match only same-day, same-amount opposite-sign bank entries whose labels
    # identify the same two internal accounts; preserve all unmatched records.
    keep=[True]*len(rows); links={}
    ix=defaultdict(list)
    for i,r in enumerate(rows):
        if r['source']=='bank' and r['transfer'] and r['amount']:
            ix[(r['date'],abs(r['amount']),r['from_'],r['to'])].append(i)
    for (dt,amt,a,b), ids in ix.items():
        neg=[i for i in ids if rows[i]['amount']<0]; pos=[i for i in ids if rows[i]['amount']>0]
        for i,j in zip(neg,pos):
            keep[j]=False; links[i]=f"{a} → {b} (paired bank entry)"
    # Polymarket withdrawal records omit payment method. Link to Qc Clearing
    # only when amount matches and dates are within three days; this is the
    # account pairing documented in the life README, not a fuzzy amount guess.
    extras=[]
    for pi,p in enumerate(rows):
        if p['source']!='pm' or p['amount']>=0 or 'Withdrawal' not in p['what']: continue
        candidates=[i for i,b in enumerate(rows) if keep[i] and b['source']=='bank' and b['amount']>0
                    and 'qc clearing' in b['what'].lower() and b['amount']==abs(p['amount'])
                    and abs((b['date']-p['date']).days)<=3]
        if len(candidates)==1:
            bi=candidates[0]; bank=rows[bi]
            # Replace the two account-side rows with one linked movement row.
            keep[bi]=False; keep[pi]=False
            extras.append(dict(date=max(bank['date'],p['date']),account='Polymarket → Chime',amount=p['amount'],
                from_='Polymarket',to='Chime Checking',counter='Qc Clearing LLC',
                what=f"Polymarket withdrawal received by Chime via Qc Clearing LLC ({money(abs(p['amount']))})",
                source='paired',transfer=True,linked='Polymarket withdrawal ↔ Chime/Qc Clearing credit'))
    rows.extend(extras); keep.extend([True]*len(extras))
    for i,r in enumerate(rows):
        if not keep[i]: continue
        if r.get('linked'): continue
        if i in links: r['linked']=links[i]
        elif r['source']=='pm' and ('Deposit' in r['what'] or 'Withdrawal' in r['what']):
            r['linked']='Unmatched to bank row (payment method/date/amount not confirmed)'
        elif r['transfer'] and r['source']!='bank': r['linked']='Other side not present or not matched'
        else: r['linked']='—'
    return [r for i,r in enumerate(rows) if keep[i]]

def main():
    bank=read_bank(); uphold=read_uphold(); pm,trades=read_pm()
    rows=merge_transfers(bank+uphold+pm)
    rows.sort(key=lambda r:(r['date'],r['source'],r['account'],r['what']))
    lines=['# Combined money ledger','',f'Coverage: {START.isoformat()} through {END.isoformat()}. Generated from `bank-ledger.md`, `uphold-transactions.csv`, and `state/polymarket-activities-all.json`.','',
      'Amounts are USD where the source provides a USD amount. Uphold non-USD transfers with no USD leg show blank in/out. Polymarket trades are summarized separately below because they exchange positions and are not deposits or withdrawals. “Unmatched” means records do not establish the other account leg.','',
      '| Date | Account | In | Out | Counterparty | What it was | Linked to |','|---|---|---:|---:|---|---|---|']
    for r in rows:
        lines.append(f"| {r['date']} | {r['account']} | {money(r['amount']) if r['amount']>0 else ''} | {money(r['amount']) if r['amount']<0 else ''} | {r['counter']} | {r['what'].replace('|','/')} | {r.get('linked','—')} |")
    # Monthly source income, counted from external/source inflows only; own-account transfers excluded.
    inc=defaultdict(Decimal); spend=defaultdict(Decimal); cat=defaultdict(Decimal)
    for r in rows:
        month=r['date'].strftime('%Y-%m'); what=r['what'].lower(); amt=r['amount']
        if r['source']=='paired':
            inc[(month,'Trading withdrawals')]+=abs(amt)
        if amt>0 and r['source']=='bank' and not r['transfer']:
            source='Subway payroll' if 'payroll' in what or 'cgh group' in what else 'Reflective Coatings roofing' if 'reflective coatings' in what else 'Chime MyPay advances' if 'mypay' in what else 'X Money' if 'x money' in what else 'Trading withdrawals' if 'qc clearing' in what else 'Other / unclear'
            inc[(month,source)]+=amt
        if amt<0 and r['source']=='bank' and not r['transfer']:
            category='Trading/crypto funding' if any(x in what for x in ['uphold','polymarket']) else 'Child support' if 'support' in what else 'Food / groceries' if any(x in what for x in ['grocery','food','subway','mcdonald','restaurant','pizza']) else 'Bills / subscriptions' if any(x in what for x in ['bill','subscription','google one','apple.com','netflix']) else 'Other spending'
            spend[(month,category)]+=abs(amt); cat[month]+=abs(amt)
    lines+=['','## Income by source per month','', '| Month | Source | In |','|---|---|---:|']
    for (m,s),v in sorted(inc.items()): lines.append(f'| {m} | {s} | {money(v)} |')
    lines+=['','## Spending by category per month','', '| Month | Category | Out |','|---|---|---:|']
    for (m,c),v in sorted(spend.items()): lines.append(f'| {m} | {c} | {money(v)} |')
    lines+=['','## Money into and out of trading / crypto','', '| Month | Flow | Amount |','|---|---|---:|']
    flows=defaultdict(Decimal)
    for r in rows:
        if r['account'] in ('Uphold','Polymarket') and r['amount']:
            flows[(r['date'].strftime('%Y-%m'),'In' if r['amount']>0 else 'Out')]+=abs(r['amount'])
    for (m,k),v in sorted(flows.items()): lines.append(f'| {m} | {k} | {money(v)} |')
    tflow=defaultdict(Decimal)
    for dt,actor,action,v in trades: tflow[(dt.strftime('%Y-%m'),actor,action)]+=v
    if tflow:
        lines+=['','Polymarket trade notional by order action (approximate quantity × price; actor shown only when source indicator is present):','', '| Month | Actor | Action | Approx. notional |','|---|---|---|---:|']
        for (m,a,k),v in sorted(tflow.items()): lines.append(f'| {m} | {a} | {k} | {money(v)} |')
    lines+=['','## What the records show','',
      'The bank export reports Subway payroll ended July 30, roofing payments from Reflective Coatings arrived in August and September, and the bank ledger includes MyPay advances and X Money receipts. These figures describe recorded cash movements, not tax income classifications. Uphold card “out” rows represent crypto converted to USD for card purchases; non-USD swaps/transfers are not valued here. Polymarket deposits and withdrawals are separate from trade activity; the export does not expose a reliable payment counterparty, so the other account leg is marked unmatched unless a bank-side row was identifiable. Transfers between Chime accounts are paired and shown once.','',
      'Limitations: the bank source ends October 2 despite its header saying October 4; the Polymarket export has 1,391 activities but only completed account balance changes are treated as cash flows; activity dates use creation time. Robinhood is reported as having no rows in the bank source. Spending categories are descriptive keyword groupings and “Other spending” includes uncategorized bank debits.','']
    (LIFE/'ledger-all.md').write_text('\n'.join(lines),encoding='utf-8')
    print(f'Wrote ledger-all.md: {len(rows)} ledger rows, {len(trades)} Polymarket trade activities.')

if __name__=='__main__': main()
