# Design notes

Why each piece of the design is the way it is, what it was chosen over, and what the pipeline has to supply for the
formulas to hold in production. Proofs are in [derivations](derivations.md); figures are recomputed in
[results](../reproduce/results.md).

## Choices and the alternatives they beat

| Choice | Alternative | Why | When I would switch |
| --- | --- | --- | --- |
| **Validity from the audit lottery** (known sampling probabilities) | Correct the targeted queue with a selection model | Unbiased whatever the quality of $`f`$ ([D4](derivations.md#d4-the-estimator-is-unbiased-for-any-predictions)); the model affects only the variance | Never for a governance metric. The measurement exists to check the model |
| **Prediction-assisted estimator** | Horvitz-Thompson on audited labels alone | Residuals $`Y - f`$ have a smaller second moment than $`Y`$ when $`f`$ is informative | In a stratum where $`E[(Y-f)^2] > E[Y^2]`$: put a weight below one on $`f`$ there, fitted on an earlier batch |
| **Independent Bernoulli audits** | A fixed number of audits per batch | Exact variance with no joint inclusion probabilities ([D5](derivations.md#d5-the-design-variance-and-an-unbiased-estimator-of-it)); the budget holds in expectation | A workflow that needs an exact audit count: a fixed-size design with the same first-order probabilities |
| **Square-root allocation in $`m_i/c_i`$** | Probability proportional to predicted risk | Minimizes variance at a fixed budget ([D7](derivations.md#d7-the-optimal-audit-allocation)); risk-first routing carries 62.7% more variance on the reference batch | No case: it is the optimum, and D9 shows it tolerates its inputs |
| **Floor $`\pi_{\min}`$ and a uniform mixture** | Trust the computed allocation | The loss is capped for any residual estimates ([D10](derivations.md#d10-the-mixture-bounds-the-loss-for-any-estimates)) | Lower the weight $`\rho`$ as residual estimates prove stable across batches |
| **Residuals by (task stratum × criteria version × cost stratum)** | Per-submission residuals from a learned model | Stable estimates; nothing is fitted to an individual submission | Strata that are too coarse to separate different residual levels |
| **Reliability by Beta-Binomial posterior within strata, read through the tail probability** | Raw accuracy per contributor | Comparable across unequal audit counts ([D3](derivations.md#d3-the-reliability-posterior), [D15](derivations.md#d15-selection-by-tail-probability)) | Strong dependence between one contributor's tasks, which the binomial ignores |
| **Repair ranked by removable loss per unit cost** | Ranked by initial risk | Exchange argument ([D11](derivations.md#d11-repair-follows-removable-loss)); 41 expected errors against 45 in the worked example | When $`\Delta_i`$ cannot be estimated better than $`r_{i0}`$: run randomized pilots across actions first |
| **One joint rule for audits and reviews** | Plan audits for measurement, then spend the rest on repair | An audited defect ships corrected, so the audit's repair belongs in its price ([D13](derivations.md#d13-the-joint-rule)); held to the sequential plan's own precision, the joint rule ships 34.7% fewer defects, 12.4% to 69.3% across the envelope | No case |
| **Measurement on frozen originals** | Measure on post-review deliverables | Repair cannot contaminate the estimate of production quality; $`\hat\mu_{\text{raw}}`$ and $`\hat\mu_{\text{final}}`$ are separate numbers | No case |

## How the three task quantities differ

| Task | Initial risk $`q_i`$ | Audit value $`m_i/c_i`$ | Removable loss $`\Delta_i`$ | What the joint rule does |
| --- | --- | --- | --- | --- |
| Certainly wrong, and predicted wrong | High | Near zero | Depends on the review | Audits it only for the repair: $`\pi_i = 1`$ when $`r_i \ge \lambda c_i`$ |
| Moderately risky, outcome open | Medium | High | Often high | Audits it for information, at $`\sqrt{\nu m_i/(\lambda c_i - r_i)}`$ |
| High risk, missing external evidence | High | Medium | Small | Does not spend a review on it; a reference solution is the only repair |
| Routine, well predicted | Low | Low | Low | Samples it at the floor, which keeps the whole task space covered |

On the reference batch the hardest stratum is the third row. A review removes 30% of its defects and a reference
audit removes all of them, so the joint rule sends every hard item to a reference solution and no reviews at all.
Risk-first routing sends that stratum both.

## Tiered review in the production workflow

A flagged submission went to three additional specialists, an initially accepted one went to one or two, and
adjudications updated reliability posteriors and review intensity. In the terms of this page the tier rule spends
repair capacity, and the random reference audits running beside it keep the measurement valid while escalation
concentrates on hard cases. Recurring disagreements were converted into explicit acceptance criteria, with missing
context separated from ambiguous instructions and from contributor error. That conversion is a third use of
review: it improves the criteria, and with them the meaning of $`Y`$.

## What the formulas need from the pipeline

1. **Freeze before reveal.** Predictions $`f_i`$ and probabilities $`\pi_i`$ are written to the batch record before
   any reference label of that batch exists. D4 holds for exactly the information fixed at that point.
2. **Honor the lottery.** A probability that is computed and not executed biases the estimate without any error
   being raised. The execution log records the realized $`S_i`$ beside the planned $`\pi_i`$, and the two are
   reconciled per stratum.
3. **Residuals from earlier batches.** $`\hat m`$ comes from independent audits of earlier batches or a pilot, never
   from the batch it allocates.
4. **Originals and revisions as separate records.** $`\hat\mu_{\text{raw}}`$ is computed on frozen originals and
   $`\hat\mu_{\text{final}}`$ on deliverables.
5. **One criteria version per estimate.** When the rubric changes, the anchor set is adjudicated under both
   versions and periods are compared under a common reference version.
6. **Blind reference audits.** The auditor does not see the automated verdict or the contributor's record.
   Sensitivity and specificity come from blind re-audits and enter the correction of D14.

## What to monitor

- **Residual drift.** A new task type or a rubric change is where $`\hat m`$ is underestimated. Realized squared
  residuals are tracked per stratum against $`\hat m`$ and refreshed from the latest independent audits; the mixture
  of D10 covers the batches in between.
- **Weight concentration.** The share of $`\hat V`$ contributed by the largest-weight audited items. At
  $`\pi_{\min} = 3\%`$ one weight can reach 33.
- **Realized audit hours.** The budget holds in expectation, so realized hours are tracked per batch against $`B`$.
- **Post-action risk.** If reviewer incentives reward measured loss reduction, estimates of $`r_{i1}`$ drift
  optimistic. Randomized pilots across the permitted actions keep them honest, which is the point of the
  $`2N\delta`$ bound ([D12](derivations.md#d12-allocation-under-estimated-action-risks)).
- **The exchange rate.** $`\nu/\lambda`$ is reported with each plan: the shipped defects the program pays for one
  unit of precision. On the reference batch, holding the estimate at 0.657 points costs 22 shipped defects and
  tightening it to 0.568 costs 13 more.

## Extensions

1. **Sequential audits within a batch.** Residual estimates sharpen as audits arrive. Updating $`\pi`$ during the
   batch while keeping the estimate valid calls for anytime-valid intervals in place of the normal interval of D5.
2. **Fixed-size designs.** For an exact audit count, conditional Poisson sampling with the same first-order
   probabilities is the natural design, and the allocation of D7 supplies those probabilities.
3. **Small strata.** With few audits in a rare stratum the normal interval undercovers. Strata are pooled for
   reporting and kept separate for allocation.
4. **Preference tasks.** The defect rate is defined for tasks with acceptance criteria. For preference comparisons
   the audited quantity becomes agreement with a calibrated panel, and the same design applies to it.
