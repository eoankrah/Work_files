"""Runs SQL, exports Tableau sources, evaluates synthetic experiment, creates offline dashboard."""
import csv,json,sqlite3,math,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    with (ROOT/'data/curated'/f'{name}.csv').open() as f:return list(csv.DictReader(f))
def number(v):
    if v=='':return None
    try:return float(v) if '.' in v else int(v)
    except ValueError:return v
def export(name,rows):
    if not rows:return
    with (ROOT/'outputs'/f'{name}.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def run():
    db=sqlite3.connect(':memory:'); db.row_factory=sqlite3.Row
    types={'claims':{'cycle_days','age_days','missing_documents','first_response_hours','paid_amount','sla_days'},'alerts':{'reviewed','confirmed_issue','risk_score','review_hours','days_in_queue'},'filing_experiment':{'completed_7d','rework_7d','support_contact_7d'}}
    data={}
    for name,numeric in types.items():
        rows=load(name);cols=list(rows[0]);data[name]=[{k:number(v) if k in numeric else v for k,v in row.items()} for row in rows]
        db.execute('CREATE TABLE '+name+' ('+','.join(k+(' REAL' if k in numeric else ' TEXT') for k in cols)+')')
        db.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for _ in cols)+')',[[row[k] for k in cols] for row in data[name]])
    db.executescript((ROOT/'sql/sqlite/metrics.sql').read_text())
    for view in ['claims_metrics','risk_metrics','experiment_metrics','claim_risk_join']:
        export(view,[dict(x) for x in db.execute('SELECT * FROM '+view)])
    cohort_sql='\n'.join(line for line in (ROOT/'sql/sqlite/cohorts.sql').read_text().splitlines() if not line.lstrip().startswith('--'))
    for i, statement in enumerate(cohort_sql.split(';')):
        if statement.strip() and 'SELECT' in statement:
            export('cohort_analysis_'+str(i+1),[dict(x) for x in db.execute(statement)])
    raw_rows=list(csv.DictReader((ROOT/'data/raw/claims_ingest.csv').open()))
    db.execute('CREATE TABLE claims_ingest AS SELECT * FROM claims WHERE 1=0')
    keys=list(raw_rows[0])
    db.executemany('INSERT INTO claims_ingest VALUES ('+','.join('?' for _ in keys)+')',[[number(row[k]) if k in types['claims'] else row[k] for k in keys] for row in raw_rows])
    for i, statement in enumerate('\n'.join(line for line in (ROOT/'sql/sqlite/data_quality.sql').read_text().splitlines() if not line.lstrip().startswith('--')).split(';')):
        if statement.strip() and 'SELECT' in statement:
            export('data_quality_check_'+str(i+1),[dict(x) for x in db.execute(statement)])
    f=data['filing_experiment'];groups={v:[x for x in f if x['variant']==v] for v in ['Control','Guided']}
    stats={v:dict(n=len(x),success=sum(z['completed_7d'] for z in x),rate=statistics.mean(z['completed_7d'] for z in x)) for v,x in groups.items()}
    a,b=stats['Control'],stats['Guided'];diff=b['rate']-a['rate'];se=math.sqrt(a['rate']*(1-a['rate'])/a['n']+b['rate']*(1-b['rate'])/b['n'])
    pooled=(a['success']+b['success'])/(a['n']+b['n']);z=diff/math.sqrt(pooled*(1-pooled)*(1/a['n']+1/b['n']))
    # Sample ratio mismatch: planned 50/50, chi-square with one df.
    srm_chi=(a['n']-len(f)/2)**2/(len(f)/2)+(b['n']-len(f)/2)**2/(len(f)/2)
    experiment=dict(groups=stats,absolute_lift_pp=100*diff,relative_lift=diff/a['rate'],ci95_pp=[100*(diff-1.96*se),100*(diff+1.96*se)],two_sided_p=math.erfc(abs(z)/math.sqrt(2)),srm_p=math.erfc(math.sqrt(srm_chi/2)),method='Independent user randomization; 7-day intention-to-treat; normal approximation; unadjusted two-sided primary test')
    raw=list(csv.DictReader((ROOT/'data/raw/claims_ingest.csv').open()))
    quality=dict(raw_rows=len(raw),duplicate_excess=len(raw)-len({x['claim_id'] for x in raw}),missing_carrier_rows=sum(not x['carrier'] for x in raw),negative_paid_rows=sum(float(x['paid_amount'])<0 for x in raw))
    claims=data['claims'];closed=[x for x in claims if x['status']=='Closed'];cycles=sorted(x['cycle_days'] for x in closed)
    def quantile(x,p):
        pos=(len(x)-1)*p;lo=math.floor(pos);hi=math.ceil(pos);return x[lo]+(x[hi]-x[lo])*(pos-lo)
    summary=dict(as_of='2026-10-01',claims=len(claims),closed=len(closed),backlog=len(claims)-len(closed),median_closed_days=statistics.median(cycles),p90_closed_days=quantile(cycles,.9),experiment=experiment,data_quality=quality)
    (ROOT/'outputs/summary.json').write_text(json.dumps(summary,indent=2))
    payload=json.dumps(dict(claims=claims,alerts=data['alerts'],filings=f,summary=summary))
    template=(ROOT/'dashboard/template.html').read_text()
    (ROOT/'dashboard/index.html').write_text(template.replace('__DATA__',payload))
    # Baseline fixtures and analytical invariants, not just code mirroring.
    assert db.execute('SELECT COUNT(*) FROM claim_risk_join').fetchone()[0]==6000
    assert db.execute('SELECT SUM(claim_count) FROM claims_metrics').fetchone()[0]==6000
    assert quality==dict(raw_rows=6012,duplicate_excess=12,missing_carrier_rows=8,negative_paid_rows=5)
    assert len({x['user_id'] for x in f})==8000
    assert all(x['cycle_days'] is None or x['cycle_days']<=x['age_days'] for x in claims)
    assert all(x['closed_date']<=summary['as_of'] for x in closed)
    assert all(x['confirmed_issue'] is None for x in data['alerts'] if not x['reviewed'])
    assert a['n']+b['n']==8000 and 0<a['rate']<1 and 0<b['rate']<1
    assert experiment['ci95_pp'][0] < 100*diff < experiment['ci95_pp'][1]
    print(json.dumps(summary,indent=2)); print('PASS: grain, reconciliation, seeded quality issues, assignment, censoring, review denominators, confidence interval')
    db.close()
if __name__=='__main__':run()
