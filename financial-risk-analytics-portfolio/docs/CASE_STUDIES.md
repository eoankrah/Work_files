# Portfolio case studies
Author: Evans O. Ankrah. These are new synthetic demonstrations, not employer projects or claims of past results.

## 1 Claims operations and measurement
**Question:** Where should operations investigate delay and incomplete documentation?
**Approach:** SQL metric layer, opening cohorts, type/channel/carrier segmentation, median and P90, separate open backlog, 30-day matured cohort query.
**Result:** 6,000 claims, 5,206 closed, 794 open; median closed cycle 10.0 days and P90 20.0 days.
**Decision:** Inspect mobile documentation patterns and compare within type and carrier before prioritizing a documentation intervention. The generator intentionally raises missing-document probability on mobile and adds duration for missing documents; this is a demonstration, not independent evidence about insurance users.
**Next step:** Evaluate a targeted intervention with pre-agreed metrics. Closed-cycle averages exclude open cases; use survival analysis for a more complete time-to-closure assessment.

## 2 Risk-review workload and control quality
**Question:** Which alert queues merit attention, and can reporting be trusted?
**Approach:** Separate alert and claim grains, reviewed-only confirmation denominator, pending queue aging, preaggregated joins, raw ingestion checks.
**Result:** 1,800 synthetic alerts; dashboard shows rule-level review yield and backlog. Raw feed detects 12 excess duplicates, 8 missing carrier records and 5 negative amounts.
**Decision:** Compare aged backlog with review capacity and confirmation yield. Do not infer prevented losses or fraud recall from this data. Reviewed alerts are not a random sample; compare selection mechanisms before changing thresholds.
**Next step:** Add trustworthy event history, reviewer capacity and consistent ground-truth sampling. Quarantine defective data with documented ownership; do not silently fill or deduplicate.

## 3 Guided claim-filing experiment
**Question:** Does guided filing increase seven-day completion?
**Design:** 8,000 independent synthetic users randomized 50/50 during August 2026. Complete follow-up by snapshot. One primary completion metric; support and rework are exploratory guardrails.
**Result:** Control 65.63%; Guided 70.27%; absolute lift 4.64 percentage points; normal-approximation 95% interval 2.60 to 6.68 points. Assignment balance p=0.639.
**Decision:** The simulated primary metric supports a positive effect. A real launch requires instrumentation validation, planned power, guardrail uncertainty and thresholds, and cost/operational assessment. The generator contains a deliberate positive treatment effect; this is a methods demonstration.
**Limits:** No repeated users, clustering, interference, sequential peeking or attrition modeled. CI is unpooled Wald difference; test uses pooled two-proportion z. Exploratory comparisons do not receive confirmatory claims.

## Interview talking points
Explain the business decision, grain, numerator/denominator, validation and caveat before naming tools. Say “I built a synthetic portfolio demonstration” when discussing these results. Use your actual Discover/Capital One work separately to establish employment experience.
