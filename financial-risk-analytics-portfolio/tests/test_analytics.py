import unittest,sqlite3,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AnalyticsTests(unittest.TestCase):
 def test_join_preserves_claim_grain_with_multiple_alerts(self):
  db=sqlite3.connect(':memory:')
  db.executescript("CREATE TABLE claims(claim_id TEXT); CREATE TABLE alerts(claim_id TEXT,risk_score REAL); INSERT INTO claims VALUES ('C1'),('C2'); INSERT INTO alerts VALUES ('C1',0.2),('C1',0.8);")
  sql=(ROOT/'sql/sqlite/metrics.sql').read_text();db.executescript(sql[sql.index('CREATE VIEW claim_alert_summary'):])
  self.assertEqual(db.execute('SELECT COUNT(*) FROM claim_risk_join').fetchone()[0],2)
  self.assertEqual(db.execute("SELECT alerts_per_claim FROM claim_risk_join WHERE claim_id='C1'").fetchone()[0],2)
  self.assertEqual(db.execute("SELECT alerts_per_claim FROM claim_risk_join WHERE claim_id='C2'").fetchone()[0],0)
 def test_unreviewed_alerts_excluded_from_confirmation_denominator(self):
  db=sqlite3.connect(':memory:');db.executescript("CREATE TABLE alerts(rule TEXT,reviewed INT,confirmed_issue INT,review_hours REAL,days_in_queue INT); INSERT INTO alerts VALUES ('R',1,1,1,0),('R',1,0,2,0),('R',0,NULL,NULL,10);")
  sql=(ROOT/'sql/sqlite/metrics.sql').read_text();db.executescript(sql[sql.index('CREATE VIEW risk_metrics'):sql.index('CREATE VIEW experiment_metrics')])
  self.assertEqual(db.execute('SELECT reviewed_confirmation_rate FROM risk_metrics').fetchone()[0],0.5)
 def test_empty_review_denominator_is_null(self):
  db=sqlite3.connect(':memory:');db.executescript("CREATE TABLE alerts(rule TEXT,reviewed INT,confirmed_issue INT,review_hours REAL,days_in_queue INT); INSERT INTO alerts VALUES ('R',0,NULL,NULL,3);")
  sql=(ROOT/'sql/sqlite/metrics.sql').read_text();db.executescript(sql[sql.index('CREATE VIEW risk_metrics'):sql.index('CREATE VIEW experiment_metrics')])
  self.assertIsNone(db.execute('SELECT reviewed_confirmation_rate FROM risk_metrics').fetchone()[0])
 def test_summary_reconciliation(self):
  s=json.loads((ROOT/'outputs/summary.json').read_text());self.assertEqual(s['claims'],s['closed']+s['backlog']);self.assertEqual(sum(v['n'] for v in s['experiment']['groups'].values()),8000)
if __name__=='__main__':unittest.main()
