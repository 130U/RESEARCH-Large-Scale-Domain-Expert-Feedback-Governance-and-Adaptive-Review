# Reproduce

```bash
python reproduce/run_all.py           # every figure in the article, a few minutes
python reproduce/run_all.py --quick   # fewer draws of the audit lottery, envelope skipped
```

Python 3.12 or later, standard library only. `run_all.py` recomputes every figure in the article from the
reference batch of Section 6, compares each with the text, writes [`results.md`](results.md) and exits with
status 1 if any figure disagrees. The same command runs on every push.

| Script | Article | What it computes |
| --- | --- | --- |
| [`audit_allocation.py`](audit_allocation.py) | §2 to §4, §6 | The audit policies at equal expected cost: probabilities, exact design variances, the uncorrected queue rate, the closed-form optimum, the variance estimator (D5) and the mixture bound (D10). It also draws the audit lottery 200,000 times per policy and checks the estimator's mean and variance against the formulas |
| [`remediation.py`](remediation.py) | §5 | The worked example (45 against 41 expected errors), an exhaustive optimality check, the exchange identity and the $`2N\delta`$ bound |
| [`profile_study.py`](profile_study.py) | §4 to §7 | The budget identity and the price of precision, the calibration tolerance table, the five plans under one budget with their implied prices, the joint rule at the sequential plan's precision, the price of an auditor's error, the tail probabilities, and the range of every headline result over the 20% envelope |

**The reference batch and the envelope.** `profile_study.py` holds the reference batch as one `Profile`: stratum
shares, defect rates, frozen predictions, audit costs and the effect of a review. The envelope moves each entry
independently by up to 20% of its value and reports the range of each result over every combination of
low, reference and high values.

**How the lottery is drawn quickly.** Within a stratum every item shares $`f_h`$ and $`\pi_h`$, and the estimator
depends on the sample only through two counts: audited items with $`Y = 1`$ and audited items with $`Y = 0`$. Under
independent Bernoulli sampling these are independent binomials, so drawing the two counts is equivalent in
distribution to drawing 10,000 indicators.

**How the joint plans are found.** For any audit plan the reviews are optimal in closed form, so the search runs
over the audit probabilities: along the precision ceiling when there is one, with a search over the whole box as a
cross-check. The prices $`\lambda`$ and $`\nu`$ are then read off the plan, and $`\nu`$ computed from two different
strata agrees to six digits, which checks the closed form of D13 against the numerical optimum.
