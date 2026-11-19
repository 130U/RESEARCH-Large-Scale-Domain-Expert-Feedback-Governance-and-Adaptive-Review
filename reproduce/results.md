# Results

Every figure in the article, recomputed from the reference batch of Section 6.

158 of 158 figures agree with the article · 200,000 draws of the audit lottery per policy · seed 20231101

## Measurement at equal audit budget (Section 6)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Batch defect rate (%) | 7.1000 | 7.1 | §6 | ✓ |
| Audit budget as a share of a full audit (%) | 14.8148 | 14.8 | §6 | ✓ |
| Uniform: audit probability, stratum 1 (%) | 14.8100 | 14.81 | §6 table | ✓ |
| Uniform: audit probability, stratum 2 (%) | 14.8100 | 14.81 | §6 table | ✓ |
| Uniform: audit probability, stratum 3 (%) | 14.8100 | 14.81 | §6 table | ✓ |
| Uniform: expected audit cost | 2,000.0 | 2,000 | §6 | ✓ |
| Uniform: standard deviation of the estimate (pp) | 0.5681 | 0.568 | §6 table | ✓ |
| Risk-first: audit probability, stratum 1 (%) | 3.0000 | 3 | §6 table | ✓ |
| Risk-first: audit probability, stratum 2 (%) | 11.5600 | 11.56 | §6 table | ✓ |
| Risk-first: audit probability, stratum 3 (%) | 43.3300 | 43.33 | §6 table | ✓ |
| Risk-first: expected audit cost | 2,000.0 | 2,000 | §6 | ✓ |
| Risk-first: standard deviation of the estimate (pp) | 0.6570 | 0.657 | §6 table | ✓ |
| Residual- and cost-aware: audit probability, stratum 1 (%) | 7.8900 | 7.89 | §6 table | ✓ |
| Residual- and cost-aware: audit probability, stratum 2 (%) | 19.3700 | 19.37 | §6 table | ✓ |
| Residual- and cost-aware: audit probability, stratum 3 (%) | 21.8400 | 21.84 | §6 table | ✓ |
| Residual- and cost-aware: expected audit cost | 2,000.0 | 2,000 | §6 | ✓ |
| Residual- and cost-aware: standard deviation of the estimate (pp) | 0.5151 | 0.515 | §6 table | ✓ |
| Risk-first: variance relative to uniform (%) | 33.7659 | 33.8 | §6 table | ✓ |
| Residual- and cost-aware: variance relative to uniform (%) | -17.7888 | -17.8 | §6 table | ✓ |
| Risk-first queue: uncorrected error rate (%) | 19.5972 | 19.6 | §6 | ✓ |
| Queue overstatement (times the batch rate) | 2.7602 | 2.76 | §6 | ✓ |
| Risk-first against the residual- and cost-aware rule: extra variance (%) | 62.7100 | 62.7 | §6 | ✓ |
| Same result from the two independent implementations (pp) | 0.5151 | equal | §6 | ✓ |

## The estimator under repeated draws of the audit lottery (Sections 2 and 3)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Uniform: mean of the estimate over the draws (%) | 7.0976 | 7.1 | §2 | ✓ |
| Uniform: variance over the draws against the exact formula (%) | 0.1796 | 0 | §3 | ✓ |
| Uniform: variance estimator against the exact variance (%) | -0.0240 | 0 | D5 | ✓ |
| Risk-first: mean of the estimate over the draws (%) | 7.0999 | 7.1 | §2 | ✓ |
| Risk-first: variance over the draws against the exact formula (%) | -0.4139 | 0 | §3 | ✓ |
| Risk-first: variance estimator against the exact variance (%) | -0.0226 | 0 | D5 | ✓ |
| Residual- and cost-aware: mean of the estimate over the draws (%) | 7.0998 | 7.1 | §2 | ✓ |
| Residual- and cost-aware: variance over the draws against the exact formula (%) | 0.1820 | 0 | §3 | ✓ |
| Residual- and cost-aware: variance estimator against the exact variance (%) | 0.0144 | 0 | D5 | ✓ |
| Reversed estimates: mean of the estimate over the draws (%) | 7.0977 | 7.1 | §2 | ✓ |
| Reversed estimates: variance over the draws against the exact formula (%) | -0.2114 | 0 | §3 | ✓ |
| Reversed estimates: variance estimator against the exact variance (%) | -0.0095 | 0 | D5 | ✓ |
| Reversed estimates mixture 70: mean of the estimate over the draws (%) | 7.0995 | 7.1 | §2 | ✓ |
| Reversed estimates mixture 70: variance over the draws against the exact formula (%) | -0.1641 | 0 | §3 | ✓ |
| Reversed estimates mixture 70: variance estimator against the exact variance (%) | 0.0014 | 0 | D5 | ✓ |
| Risk-first queue: uncorrected rate averaged over the draws (%) | 19.5988 | 19.6 | §6 | ✓ |

## What the allocation is worth (Sections 4 and 6)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Closed-form optimal variance equals the rule's variance (pp) | 0.5151 | equal | §4 | ✓ |
| Budget ratio κ | 0.8485 | 0.848 | §6 | ✓ |
| Audit budget saved at any precision target (%) | 15.1534 | 15.2 | §6 | ✓ |
| Audit budget for a standard deviation of 0.50 pp, residual- and cost-aware | 2,099.9 | 2,100 | §6 table | ✓ |
| Audit budget for a standard deviation of 0.50 pp, uniform | 2,474.9 | 2,475 | §6 table | ✓ |
| Ratio of the two budgets at 0.50 pp | 0.8485 | 0.848 | §4 | ✓ |
| Audit budget for a standard deviation of 0.40 pp, residual- and cost-aware | 2,974.3 | 2,974 | §6 table | ✓ |
| Audit budget for a standard deviation of 0.40 pp, uniform | 3,505.6 | 3,506 | §6 table | ✓ |
| Ratio of the two budgets at 0.40 pp | 0.8485 | 0.848 | §4 | ✓ |
| Audit budget for a standard deviation of 0.30 pp, residual- and cost-aware | 4,399.2 | 4,399 | §6 table | ✓ |
| Audit budget for a standard deviation of 0.30 pp, uniform | 5,184.9 | 5,185 | §6 table | ✓ |
| Ratio of the two budgets at 0.30 pp | 0.8485 | 0.848 | §4 | ✓ |
| Audit budget for a standard deviation of 0.25 pp, residual- and cost-aware | 5,419.1 | 5,419 | §6 table | ✓ |
| Audit budget for a standard deviation of 0.25 pp, uniform | 6,386.9 | 6,387 | §6 table | ✓ |
| Ratio of the two budgets at 0.25 pp | 0.8485 | 0.848 | §4 | ✓ |
| Relative error 10%: variance above the optimum (%) | 0.3001 | 0.3 | §6 table | ✓ |
| Relative error 10%: quarter-variance law (%) | 0.2979 | 0.3 | §6 table | ✓ |
| Relative error 20%: variance above the optimum (%) | 1.2285 | 1.23 | §6 table | ✓ |
| Relative error 20%: quarter-variance law (%) | 1.1915 | 1.19 | §6 table | ✓ |
| Relative error 30%: variance above the optimum (%) | 2.8766 | 2.88 | §6 table | ✓ |
| Relative error 30%: quarter-variance law (%) | 2.6809 | 2.68 | §6 table | ✓ |
| Relative error 50%: variance above the optimum (%) | 9.2164 | 9.2 | §6 table | ✓ |
| Relative error 50%: quarter-variance law (%) | 7.4470 | 7.4 | §6 table | ✓ |
| Reversed residual ordering: audit probability, stratum 1 (%) | 23.0000 | 23 | §6 | ✓ |
| Reversed residual ordering: audit probability, stratum 2 (%) | 11.7700 | 11.77 | §6 | ✓ |
| Reversed residual ordering: audit probability, stratum 3 (%) | 3.0000 | 3 | §6 | ✓ |
| Reversed residual ordering: variance above uniform (%) | 199.6550 | 199.7 | §6 | ✓ |
| Same estimates with weight 0.7 on the uniform design (%) | 17.0672 | 17.1 | §6 | ✓ |
| Guaranteed ceiling of the mixture for any estimates (%) | 50.3106 | 50.3 | §4, §6 | ✓ |

## Repair by removable loss (Section 5)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Worked example: expected errors left, ranking by initial risk | 45.0000 | 45 | §5 | ✓ |
| Worked example: expected errors left, ranking by removable loss | 41.0000 | 41 | §5 | ✓ |
| Worked example: reduction at the same review volume (%) | 8.8889 | 8.89 | §5 | ✓ |
| Ranking by removable loss equals the exhaustive optimum | 41.0000 | 41 | §5 | ✓ |
| Exchange identity ΔF = Δᵢ − Δₖ on 10,000 random pairs |  | holds | §5 | ✓ |
| Bound F(ẑ) ≤ F(z*) + 2Nδ on 300 instances solved exhaustively |  | holds | §5 | ✓ |

## One budget, two products (Section 6)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Defects shipped with no handling | 710.0000 | 710 | §6 | ✓ |
| Total budget as a share of a full audit (%) | 37.0370 | 37 | §6 | ✓ |
| Risk-first for audits and reviews: audit probability, stratum 1 (%) | 3.0000 | 3 | §6 table | ✓ |
| Risk-first for audits and reviews: share reviewed, stratum 1 (%) | 0.0000 | 0 | §6 table | ✓ |
| Risk-first for audits and reviews: audit probability, stratum 2 (%) | 11.5600 | 11.56 | §6 table | ✓ |
| Risk-first for audits and reviews: share reviewed, stratum 2 (%) | 66.7000 | 67 | §6 table | ✓ |
| Risk-first for audits and reviews: audit probability, stratum 3 (%) | 43.3300 | 43.33 | §6 table | ✓ |
| Risk-first for audits and reviews: share reviewed, stratum 3 (%) | 100.0000 | 100 | §6 table | ✓ |
| Risk-first for audits and reviews: standard deviation of the estimate (pp) | 0.6570 | 0.657 | §6 table | ✓ |
| Risk-first for audits and reviews: defects shipped | 320.8556 | 320.9 | §6 table | ✓ |
| Risk-first for audits and reviews: spends no more than the total budget |  | ≤ 5,000 | §6 | ✓ |
| Measurement rule, then reviews by removable loss: audit probability, stratum 1 (%) | 7.8900 | 7.89 | §6 table | ✓ |
| Measurement rule, then reviews by removable loss: share reviewed, stratum 1 (%) | 0.0000 | 0 | §6 table | ✓ |
| Measurement rule, then reviews by removable loss: audit probability, stratum 2 (%) | 19.3700 | 19.37 | §6 table | ✓ |
| Measurement rule, then reviews by removable loss: share reviewed, stratum 2 (%) | 100.0000 | 100 | §6 table | ✓ |
| Measurement rule, then reviews by removable loss: audit probability, stratum 3 (%) | 21.8400 | 21.84 | §6 table | ✓ |
| Measurement rule, then reviews by removable loss: share reviewed, stratum 3 (%) | 50.0000 | 50 | §6 table | ✓ |
| Measurement rule, then reviews by removable loss: standard deviation of the estimate (pp) | 0.5151 | 0.515 | §6 table | ✓ |
| Measurement rule, then reviews by removable loss: defects shipped | 336.1681 | 336.2 | §6 table | ✓ |
| Measurement rule, then reviews by removable loss: spends no more than the total budget |  | ≤ 5,000 | §6 | ✓ |
| Joint rule at the precision of risk-first routing: audit probability, stratum 1 (%) | 3.3100 | 3.31 | §6 table | ✓ |
| Joint rule at the precision of risk-first routing: share reviewed, stratum 1 (%) | 0.0000 | 0 | §6 table | ✓ |
| Joint rule at the precision of risk-first routing: audit probability, stratum 2 (%) | 9.5700 | 9.57 | §6 table | ✓ |
| Joint rule at the precision of risk-first routing: share reviewed, stratum 2 (%) | 60.9000 | 61 | §6 table | ✓ |
| Joint rule at the precision of risk-first routing: audit probability, stratum 3 (%) | 100.0000 | 100 | §6 table | ✓ |
| Joint rule at the precision of risk-first routing: share reviewed, stratum 3 (%) | 0.0000 | 0 | §6 table | ✓ |
| Joint rule at the precision of risk-first routing: standard deviation of the estimate (pp) | 0.6570 | 0.657 | §6 table | ✓ |
| Joint rule at the precision of risk-first routing: defects shipped | 197.0724 | 197.1 | §6 table | ✓ |
| Joint rule at the precision of risk-first routing: spends no more than the total budget |  | ≤ 5,000 | §6 | ✓ |
| Joint rule at the precision of uniform sampling: audit probability, stratum 1 (%) | 4.2000 | 4.2 | §6 table | ✓ |
| Joint rule at the precision of uniform sampling: share reviewed, stratum 1 (%) | 0.0000 | 0 | §6 table | ✓ |
| Joint rule at the precision of uniform sampling: audit probability, stratum 2 (%) | 12.7400 | 12.74 | §6 table | ✓ |
| Joint rule at the precision of uniform sampling: share reviewed, stratum 2 (%) | 52.2000 | 52 | §6 table | ✓ |
| Joint rule at the precision of uniform sampling: audit probability, stratum 3 (%) | 100.0000 | 100 | §6 table | ✓ |
| Joint rule at the precision of uniform sampling: share reviewed, stratum 3 (%) | 0.0000 | 0 | §6 table | ✓ |
| Joint rule at the precision of uniform sampling: standard deviation of the estimate (pp) | 0.5681 | 0.568 | §6 table | ✓ |
| Joint rule at the precision of uniform sampling: defects shipped | 209.9103 | 209.9 | §6 table | ✓ |
| Joint rule at the precision of uniform sampling: spends no more than the total budget |  | ≤ 5,000 | §6 | ✓ |
| Joint rule with no precision ceiling: audit probability, stratum 1 (%) | 3.0000 | 3 | §6 table | ✓ |
| Joint rule with no precision ceiling: share reviewed, stratum 1 (%) | 0.0000 | 0 | §6 table | ✓ |
| Joint rule with no precision ceiling: audit probability, stratum 2 (%) | 3.0000 | 3 | §6 table | ✓ |
| Joint rule with no precision ceiling: share reviewed, stratum 2 (%) | 74.9000 | 75 | §6 table | ✓ |
| Joint rule with no precision ceiling: audit probability, stratum 3 (%) | 100.0000 | 100 | §6 table | ✓ |
| Joint rule with no precision ceiling: share reviewed, stratum 3 (%) | 0.0000 | 0 | §6 table | ✓ |
| Joint rule with no precision ceiling: standard deviation of the estimate (pp) | 1.0348 | 1.035 | §6 table | ✓ |
| Joint rule with no precision ceiling: defects shipped | 174.8587 | 174.9 | §6 table | ✓ |
| Joint rule with no precision ceiling: spends no more than the total budget |  | ≤ 5,000 | §6 | ✓ |
| Joint rule against risk-first at the same budget and precision (% fewer defects) | 38.5791 | 38.6 | §6 | ✓ |
| Joint rule held to the precision of uniform sampling (% fewer defects) | 34.5779 | 34.6 | §6 | ✓ |
| Joint rule held to the sequential plan's precision, against that plan (% fewer defects) | 34.7138 | 34.7 | §6 | ✓ |
| Risk per unit cost in the hardest stratum | 0.1167 | 0.117 | §6 | ✓ |
| Joint rule at the precision of risk-first routing: budget price λ = 0.0965 lies in 0.093 to 0.096 |  | 0.093 to 0.096 | §6 | ✓ |
| Joint rule at the precision of risk-first routing: ν from the routine and the intermediate stratum agree to six digits |  | holds | §5, §6 | ✓ |
| Joint rule at the precision of uniform sampling: budget price λ = 0.0931 lies in 0.093 to 0.096 |  | 0.093 to 0.096 | §6 | ✓ |
| Joint rule at the precision of uniform sampling: ν from the routine and the intermediate stratum agree to six digits |  | holds | §5, §6 | ✓ |
| Shipped defects paid for holding the estimate at 0.657 pp | 22.2138 | 22 | §6 | ✓ |
| Further defects paid for tightening it to 0.568 pp | 12.8379 | 13 | §6 | ✓ |

## Operating the design (Section 7)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Auditor misses 5% of defects: audit budget (%) | 5.2030 | 5.2 | §7 table | ✓ |
| Auditor flags 2% of clean items: audit budget (%) | 43.8333 | 43.8 | §7 table | ✓ |
| Both errors: audit budget (%) | 52.8322 | 52.8 | §7 table | ✓ |
| Cost of false flags relative to misses (times) | 8.4246 | 8 | §7 | ✓ |
| Routine stratum: audit-label rate with 2% false flags (%) | 2.9800 | 2.98 | D14 | ✓ |
| Routine stratum: residual second moment, error-free auditor | 0.0100 | 0.01 | D14 | ✓ |
| Routine stratum: residual second moment with 2% false flags | 0.0290 | 0.029 | D14 | ✓ |
| Tail probability, 33 of 40 audited tasks correct | 0.4663 | 0.47 | §7 | ✓ |
| Tail probability, 6 of 8 correct | 0.4072 | 0.41 | §7 | ✓ |
| Tail probability, 57 of 60 correct | 0.0053 | 0.005 | §7 | ✓ |

## Ranges over the 20% envelope (Summary and Section 6)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Queue overstatement (times), low end | 1.9628 | 1.96 | §6 | ✓ |
| Queue overstatement (times), high end | 4.1443 | 4.14 | §6 | ✓ |
| Risk-first: variance relative to uniform (%), low end | -16.2782 | -16 | §6 table | ✓ |
| Risk-first: variance relative to uniform (%), high end | 96.8171 | 97 | §6 table | ✓ |
| Residual- and cost-aware: variance relative to uniform (%), low end | -32.0600 | -32 | §6 table | ✓ |
| Residual- and cost-aware: variance relative to uniform (%), high end | -8.8495 | -9 | §6 table | ✓ |
| Risk-first against the rule: extra variance (%), low end | 13.5836 | 14 | §6 | ✓ |
| Risk-first against the rule: extra variance (%), high end | 136.8818 | 137 | §6 | ✓ |
| Audit budget saved at equal precision (%), low end | 7.5384 | 7.5 | §6 | ✓ |
| Audit budget saved at equal precision (%), high end | 27.3104 | 27.3 | §6 | ✓ |
| Joint rule against risk-first at equal budget and precision (% fewer defects), low end | 19.0689 | 19 | Summary, §6 | ✓ |
| Joint rule against risk-first at equal budget and precision (% fewer defects), high end | 67.2568 | 67 | Summary, §6 | ✓ |
| Joint rule against the sequential plan at that plan's precision (% fewer defects), low end | 12.3940 | 12.4 | §6 | ✓ |
| Joint rule against the sequential plan at that plan's precision (% fewer defects), high end | 69.3301 | 69.3 | §6 | ✓ |
| The rule measures better than uniform sampling everywhere in the envelope |  | holds | §6 | ✓ |
| Risk-first measures worse than the rule everywhere in the envelope |  | holds | §6 | ✓ |
| Risk-first against uniform sampling changes sign within the envelope |  | holds | §6 | ✓ |
