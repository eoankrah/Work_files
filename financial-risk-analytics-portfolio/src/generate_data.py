"""Seeded synthetic datasets; no real people, institutions, or employer records."""
import csv, random
from pathlib import Path
from datetime import date, timedelta
ROOT=Path(__file__).resolve().parents[1]
AS_OF=date(2026,10,1)
def write(name,rows,folder='raw'):
    path=ROOT/'data'/folder/(name+'.csv');path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def generate():
    r=random.Random(20261003); claims=[]; alerts=[]; filings=[]
    for i in range(6000):
        opened=date(2026,4,1)+timedelta(days=r.randrange(183))
        kind=r.choice(['Auto','Property','Liability']); channel=r.choice(['Mobile','Web','Agent'])
        missing=int(r.random() < (.30 if channel=='Mobile' else .15))
        duration=max(1,round(r.gammavariate(2,4)+(8 if missing else 0)+(5 if kind=='Property' else 0)))
        closed=opened+timedelta(days=duration)
        is_closed=closed<=AS_OF and r.random()>.08
        age=(AS_OF-opened).days
        claims.append(dict(claim_id=f'C{i:06}',carrier=r.choice(['Carrier A','Carrier B','Carrier C']),claim_type=kind,channel=channel,opened_date=str(opened),cohort_month=opened.strftime('%Y-%m'),closed_date=str(closed) if is_closed else '',status='Closed' if is_closed else 'Open',missing_documents=missing,first_response_hours=round(r.uniform(1,18)+missing*10,2),cycle_days=duration if is_closed else '',age_days=age,paid_amount=round(r.lognormvariate(8.1,.8),2) if is_closed else 0,sla_days=20 if kind=='Property' else 14))
    for i in range(1800):
        c=r.choice(claims);score=round(r.random(),4); reviewed=int(r.random()<.82)
        # Synthetic investigation outcomes are probabilistic, not proof from the score.
        confirmed=int(r.random() < .08+.55*score) if reviewed else ''
        alerts.append(dict(alert_id=f'A{i:05}',claim_id=c['claim_id'],rule=r.choice(['Velocity','Amount outlier','Duplicate pattern']),risk_score=score,reviewed=reviewed,confirmed_issue=confirmed,review_hours=round(r.uniform(.5,3.5),2) if reviewed else '',days_in_queue=r.randrange(1,25) if not reviewed else 0))
    for i in range(8000):
        variant=r.choice(['Control','Guided']);channel=r.choice(['Mobile','Web']);complete=int(r.random() < (.67+(.07 if variant=='Guided' else 0)-(.04 if channel=='Mobile' else 0)))
        filings.append(dict(user_id=f'U{i:06}',assigned_date=str(date(2026,8,1)+timedelta(days=r.randrange(31))),variant=variant,channel=channel,completed_7d=complete,rework_7d=int(complete and r.random()<(.11 if variant=='Guided' else .12)),support_contact_7d=int(r.random()<.08)))
    write('claims',claims,'curated');write('alerts',alerts,'curated');write('filing_experiment',filings,'curated')
    dirty=[dict(c) for c in claims]+[dict(c) for c in claims[:12]]
    for c in dirty[30:38]:c['carrier']=''
    for c in dirty[70:75]:c['paid_amount']=-100
    write('claims_ingest',dirty)
    return claims,alerts,filings
if __name__=='__main__':generate()
