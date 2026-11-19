# Derivations

The article states each result with the step that makes it work. This file gives every proof in full, in the
article's notation, so that each result can be checked line by line. Section numbers (§) refer to the
[article](../manuscript/large-scale-domain-expert-feedback-governance-and-adaptive-review.md); every
figure quoted here is recomputed in [results](../reproduce/results.md).

**Notation.** A batch has $`N`$ submissions with features $`X_i`$, latent reference labels $`Y_i \in \{0,1\}`$,
a frozen prediction $`f_i \in [0,1]`$, an audit indicator $`S_i \sim \text{Bernoulli}(\pi_i)`$ drawn independently,
and an audit cost $`c_i > 0`$. $`q(x) = P(Y = 1 \mid X = x)`$, $`e_i = Y_i - f_i`$ and $`\mu = N^{-1}\sum_i Y_i`$.
Throughout, $`C = \sum_i c_i`$, $`M = \sum_i m_i`$ and $`S = \sum_i \sqrt{m_i c_i}`$.

| | Result | Section |
| --- | --- | --- |
| [D1](#d1-what-a-review-queue-estimates) | What a review queue estimates | §1 |
| [D2](#d2-accuracy-drifts-with-the-task-mix) | Accuracy drifts with the task mix | §1 |
| [D3](#d3-the-reliability-posterior) | The reliability posterior | §1 |
| [D4](#d4-the-estimator-is-unbiased-for-any-predictions) | The estimator is unbiased for any predictions | §2 |
| [D5](#d5-the-design-variance-and-an-unbiased-estimator-of-it) | The design variance and an unbiased estimator of it | §3 |
| [D6](#d6-what-an-audit-is-worth) | What an audit is worth | §3 |
| [D7](#d7-the-optimal-audit-allocation) | The optimal audit allocation | §3 |
| [D8](#d8-the-gain-over-uniform-sampling-and-the-budget-identity) | The gain over uniform sampling and the budget identity | §4 |
| [D9](#d9-the-quarter-variance-law) | The quarter-variance law | §4 |
| [D10](#d10-the-mixture-bounds-the-loss-for-any-estimates) | The mixture bounds the loss for any estimates | §4 |
| [D11](#d11-repair-follows-removable-loss) | Repair follows removable loss | §5 |
| [D12](#d12-allocation-under-estimated-action-risks) | Allocation under estimated action risks | §5 |
| [D13](#d13-the-joint-rule) | The joint rule | §5 |
| [D14](#d14-the-price-of-an-auditors-error) | The price of an auditor's error | §7 |
| [D15](#d15-selection-by-tail-probability) | Selection by tail probability | §7 |

---

## D1. What a review queue estimates

**Claim.** If selection is randomized given $`X`$ with probability $`\pi(X) > 0`$ and is independent of the
unobserved label given $`X`$, then

```math
E[Y \mid S = 1] = \frac{E[\pi(X)q(X)]}{E[\pi(X)]}, \qquad
E[Y \mid S = 1] - E[Y] = \frac{\mathrm{Cov}(\pi(X), q(X))}{E[\pi(X)]}. \qquad (D1.1)
```

**Proof.** $`P(S = 1) = E[P(S=1 \mid X)] = E[\pi(X)]`$. By conditional independence of $`S`$ and $`Y`$ given $`X`$,
$`P(Y = 1, S = 1) = E[P(Y=1 \mid X)\,P(S=1 \mid X)] = E[q(X)\pi(X)]`$. Dividing gives the first identity. For the
second, $`E[\pi q] = \mathrm{Cov}(\pi, q) + E[\pi]E[q]`$ and $`E[Y] = E[q]`$, so
$`E[\pi q]/E[\pi] - E[q] = \mathrm{Cov}(\pi, q)/E[\pi]`$. ∎

The bias is the covariance between who gets audited and who is likely wrong. Better targeting makes the covariance
larger, so the queue's overstatement grows as routing improves. On the reference batch the risk-first queue reads
19.60% against a batch rate of 7.10%.

**Finite batch.** In a realized batch the queue reports $`\sum_i S_i Y_i / \sum_i S_i`$, a ratio with a random
denominator. By the delta method its expectation is $`\sum_i \pi_i Y_i / \sum_i \pi_i + O(1/\sum_i \pi_i)`$. With
about 960 expected audits the two agree to the second decimal: 19.5972% for the ratio of expectations and 19.60%
for the average of the realized ratio over 200,000 draws of the audit lottery.

## D2. Accuracy drifts with the task mix

With $`A_{jt} = \sum_h p_{jht} a_{jh}`$, subtracting consecutive periods gives
$`A_{j,t+1} - A_{jt} = \sum_h (p_{jh,t+1} - p_{jht}) a_{jh}`$ when the stratum accuracies $`a_{jh}`$ are fixed. The
change is nonzero whenever the mix moves toward strata of different difficulty, even though ability is constant.
Fixing a target mix $`w_h`$ gives $`A^{\text{std}}_j = \sum_h w_h a_{jh}`$, which depends only on the $`a_{jh}`$. ∎

## D3. The reliability posterior

Let $`\theta = a_{jh}`$ have prior $`\text{Beta}(\alpha_0, \beta_0)`$, and let $`k`$ of $`n`$ independent audited tasks
be verified correct. The likelihood is $`\binom{n}{k}\theta^k(1-\theta)^{n-k}`$, so the posterior density is
proportional to $`\theta^{\alpha_0 + k - 1}(1-\theta)^{\beta_0 + n - k - 1}`$, that is
$`\text{Beta}(\alpha_0 + k, \beta_0 + n - k)`$. Its mean $`(\alpha_0 + k)/(\alpha_0 + \beta_0 + n)`$ is a weighted
average of the prior mean and the observed rate $`k/n`$, with weight $`n/(\alpha_0 + \beta_0 + n)`$ on the data.
Contributors with few audits are shrunk toward the stratum prior, which keeps unequal sample sizes from producing
spurious rankings. ∎

## D4. The estimator is unbiased for any predictions

$`\hat\mu = N^{-1}\sum_i [f_i + (S_i/\pi_i)(Y_i - f_i)]`$. Subtracting $`\mu = N^{-1}\sum_i Y_i`$,

```math
\hat\mu - \mu = \frac{1}{N}\sum_i \Big(\frac{S_i}{\pi_i} - 1\Big) e_i . \qquad (D4.1)
```

Conditional on the batch, the predictions and the probabilities, $`E[S_i] = \pi_i`$, so each term has mean zero.
The labels and $`f_i`$ are fixed under the design and the only randomness is $`S`$, so nothing is assumed about the
accuracy of $`f`$. ∎

The argument needs $`f_i`$ and $`\pi_i`$ to be fixed before the batch's labels are seen. If either were chosen
after looking at some $`Y_i`$, then $`E[S_i \mid \cdots] = \pi_i`$ would no longer hold for the information actually
used. This is the reason for freezing predictions and audited objects.

## D5. The design variance and an unbiased estimator of it

Independent $`S_i`$ give $`\mathrm{Var}(S_i/\pi_i) = (1-\pi_i)/\pi_i`$ and zero covariances, so

```math
\mathrm{Var}_S(\hat\mu) = \frac{1}{N^2}\sum_i \frac{1-\pi_i}{\pi_i} e_i^2 . \qquad (D5.1)
```

The residual $`e_i`$ is known only for audited items, but

```math
\hat V = \frac{1}{N^2}\sum_i S_i\,\frac{1-\pi_i}{\pi_i^2}\, e_i^2 \qquad (D5.2)
```

is unbiased for that variance, because $`E[S_i]\,(1-\pi_i)\pi_i^{-2} = (1-\pi_i)/\pi_i`$. ∎ The reported interval is
$`\hat\mu \pm z\sqrt{\hat V}`$. On the reference batch the mean of $`\hat V`$ over 200,000 draws of the audit
lottery is within 1% of the exact variance under every policy.

## D6. What an audit is worth

For one item with $`q_i = P(Y_i = 1 \mid X_i)`$,

```math
m_i = E[(Y_i - f_i)^2 \mid X_i] = q_i(1-f_i)^2 + (1-q_i) f_i^2 = q_i(1-q_i) + (q_i - f_i)^2 . \qquad (D6.1)
```

Expand both sides: the left is $`q_i - 2q_i f_i + f_i^2`$, and so is the right. ∎ An item that is almost surely
wrong and known to be ($`q_i \approx f_i \approx 1`$) has $`m_i \approx 0`$. Auditing it teaches nothing about the
batch, even though repairing it may be valuable.

## D7. The optimal audit allocation

**Problem.** Minimize $`\Phi(\pi) = \sum_i m_i/\pi_i`$ subject to $`\sum_i c_i \pi_i \le B`$ and
$`\pi_{\min} \le \pi_i \le 1`$. The constant $`-\sum_i m_i`$ in the variance numerator is dropped.

**Convexity and existence.** Each $`m_i/\pi_i`$ is strictly convex on $`\pi_i > 0`$ when $`m_i > 0`$, and the
feasible set is a nonempty compact convex set whenever $`B \ge \pi_{\min}\sum_i c_i`$. A minimizer exists and is
unique.

**Optimality conditions.** With multiplier $`\lambda \ge 0`$ for the budget and box multipliers, each coordinate
satisfies: $`\pi_i = \pi_{\min}`$ if $`\sqrt{m_i/(\lambda c_i)} \le \pi_{\min}`$, $`\pi_i = 1`$ if
$`\sqrt{m_i/(\lambda c_i)} \ge 1`$, and otherwise $`-m_i/\pi_i^2 + \lambda c_i = 0`$. Together:

```math
\pi_i^* = \mathrm{clip}_{[\pi_{\min},1]}\Big(\sqrt{m_i/(\lambda c_i)}\Big). \qquad (D7.1)
```

**Choosing λ.** $`g(\lambda) = \sum_i c_i \pi^*_i(\lambda)`$ is continuous and nonincreasing in $`\lambda`$. If
$`\sum_i c_i \le B`$ the full audit is feasible and optimal. Otherwise the budget binds, because $`\Phi`$ strictly
decreases in each $`\pi_i`$, and $`\lambda`$ solves $`g(\lambda) = B`$. When some coordinates sit at a bound, $`g`$
can be flat on an interval of $`\lambda`$, so the multiplier need not be unique, but $`\pi^*`$ is. The code finds
$`\lambda`$ by bisection (`budget_matched` in [`audit_allocation.py`](../reproduce/audit_allocation.py)). ∎

## D8. The gain over uniform sampling and the budget identity

Uniform sampling at budget $`B`$ uses $`p = B/C`$. Averaging $`e_i^2`$ over the label distribution replaces it by
$`m_i`$.

- Uniform: $`V_{\text{uniform}} = N^{-2}\sum_i (1/p - 1)m_i = N^{-2}[CM/B - M]`$.
- Optimal, unclipped: $`\pi_i = \sqrt{m_i/c_i}/\sqrt\lambda`$, and the budget gives $`\sqrt\lambda = S/B`$. Then
  $`\sum_i m_i/\pi_i = \sqrt\lambda\, S = S^2/B`$, so $`V_{\text{optimal}} = N^{-2}[S^2/B - M]`$.

Cauchy-Schwarz applied to the vectors $`(\sqrt{c_i})`$ and $`(\sqrt{m_i})`$ gives $`S^2 \le CM`$, with equality if
and only if $`m_i/c_i`$ is constant. ∎ If all items in a stratum share $`\pi`$, substituting the stratum's
finite-batch mean of $`e_i^2`$ for $`m_i`$ makes both formulas exact for the fixed batch: the closed form and the
direct design variance of the rule agree to $`10^{-9}`$ on the reference batch.

**Budget identity.** Set each variance equal to a target $`\tau^2`$ and solve for the budget:

```math
B_{\text{optimal}}(\tau^2) = \frac{S^2}{N^2\tau^2 + M}, \qquad
B_{\text{uniform}}(\tau^2) = \frac{CM}{N^2\tau^2 + M}, \qquad
\frac{B_{\text{optimal}}(\tau^2)}{B_{\text{uniform}}(\tau^2)} = \frac{S^2}{CM} =: \kappa . \qquad (D8.1)
```

The denominators are the same, so the target cancels. ∎ The saving $`1 - \kappa`$ is a property of the batch alone:
it is zero when $`m_i/c_i`$ is constant and grows with the dispersion of $`\sqrt{m_i/c_i}`$ across the batch. On
the reference batch $`\kappa = 0.848`$ at every row of the price table in §6.

## D9. The quarter-variance law

Allocate with estimates $`\hat m_i = m_i(1+\varepsilon_i)`$, unclipped, at the same budget:
$`\hat\pi_i = B\sqrt{\hat m_i/c_i}/\hat S`$ with $`\hat S = \sum_j\sqrt{\hat m_j c_j}`$. Then

```math
\sum_i \frac{m_i}{\hat\pi_i} = \frac{\hat S}{B}\sum_i \frac{\sqrt{m_i c_i}}{\sqrt{1+\varepsilon_i}} . \qquad (D9.1)
```

With the weights $`w_i = \sqrt{m_i c_i}/S`$, which sum to one, $`\hat S = S\sum_i w_i\sqrt{1+\varepsilon_i}`$ and
$`\sum_i \sqrt{m_i c_i}/\sqrt{1+\varepsilon_i} = S\sum_i w_i/\sqrt{1+\varepsilon_i}`$. Subtracting the optimum
$`S^2/B`$:

```math
V(\hat\pi) - V(\pi^*) = \frac{S^2}{N^2 B}\left[\Big(\sum_i w_i\sqrt{1+\varepsilon_i}\Big)\Big(\sum_i \frac{w_i}{\sqrt{1+\varepsilon_i}}\Big) - 1\right]. \qquad (D9.2)
```

**Nonnegativity.** By Cauchy-Schwarz on $`a_i = \sqrt{w_i}(1+\varepsilon_i)^{1/4}`$ and
$`b_i = \sqrt{w_i}(1+\varepsilon_i)^{-1/4}`$, the product of the two sums is at least $`(\sum_i w_i)^2 = 1`$.

**Expansion.** Write $`\mu_1 = \sum_i w_i\varepsilon_i`$ and $`\mu_2 = \sum_i w_i\varepsilon_i^2`$. Since
$`\sqrt{1+\varepsilon} = 1 + \varepsilon/2 - \varepsilon^2/8 + O(\varepsilon^3)`$ and
$`1/\sqrt{1+\varepsilon} = 1 - \varepsilon/2 + 3\varepsilon^2/8 + O(\varepsilon^3)`$,

```math
\Big(1 + \tfrac{\mu_1}{2} - \tfrac{\mu_2}{8}\Big)\Big(1 - \tfrac{\mu_1}{2} + \tfrac{3\mu_2}{8}\Big) - 1
= \tfrac{1}{4}\big(\mu_2 - \mu_1^2\big) + O(\|\varepsilon\|^3) = \tfrac14\mathrm{Var}_w(\varepsilon) + O(\|\varepsilon\|^3). \quad ∎ \qquad (D9.3)
```

The first-order terms cancel, which is why the rule tolerates its inputs. A common factor costs nothing exactly:
if every $`\varepsilon_i = \varepsilon`$, the two sums are $`\sqrt{1+\varepsilon}`$ and $`1/\sqrt{1+\varepsilon}`$
and their product is one. The exact expression also shows the one direction that hurts: $`1/\sqrt{1+\varepsilon_i}`$
is unbounded as $`\varepsilon_i \to -1`$, a residual estimated as near zero somewhere in the task space. D10 bounds
that case.

## D10. The mixture bounds the loss for any estimates

Mix the computed probabilities with the uniform design: $`\pi_i(\rho) = (1-\rho)\hat\pi_i + \rho p`$.

1. **Same budget.** Expected cost is linear in $`\pi`$, so $`\sum_i c_i\pi_i(\rho) = (1-\rho)B + \rho B = B`$.
2. **Bounded loss.** Every $`\pi_i(\rho) \ge \rho p`$, hence $`(1-\pi_i)/\pi_i \le (1-\rho p)/(\rho p)`$, while
   uniform sampling has $`(1-p)/p`$ on every item. Dividing,

```math
\frac{V(\pi(\rho))}{V_{\text{uniform}}} \le \frac{1-\rho p}{\rho(1-p)} . \quad ∎ \qquad (D10.1)
```

The bound holds however wrong $`\hat\pi`$ is and needs no knowledge of $`m_i`$. On the reference batch
($`p = 14.81\%`$, $`\rho = 0.7`$) it is +50.3%. A residual ordering reversed across the strata costs +199.7%
without the mixture and +17.1% with it.

## D11. Repair follows removable loss

With equal review costs, one slot per task and capacity $`K`$, the delivered loss is
$`\sum_i r_{i0} - \sum_{i \in R}\Delta_i`$ for a reviewed set $`R`$ with $`\left\vert R\right\vert \le K`$. Minimizing it means choosing
the $`K`$ largest positive $`\Delta_i`$. **Exchange argument:** if $`i \in R`$, $`k \notin R`$ and
$`\Delta_k > \Delta_i`$, swapping changes the loss by
$`(r_{i0} + r_{k1}) - (r_{i1} + r_{k0}) = \Delta_i - \Delta_k < 0`$. No optimal set leaves a larger gain
unreviewed. ∎ Initial risk $`r_{i0}`$ appears in neither the variable part of the objective nor the exchange, so it
is the right ranking key only by coincidence. With unequal costs the same argument ranks by $`\Delta_i`$ per unit
cost, and with several specialists the assignment program of §5 replaces the sort.

## D12. Allocation under estimated action risks

Suppose $`\left\vert\hat r_{ia} - r_{ia}\right\vert \le \delta`$ for all feasible actions and each task takes exactly one action. For
any feasible $`z`$, $`\left\vert F(z) - \hat F(z)\right\vert \le N\delta`$, since the cost terms are identical. With $`\hat z`$ optimal
for $`\hat F`$:

```math
F(\hat z) \le \hat F(\hat z) + N\delta \le \hat F(z^*) + N\delta \le F(z^*) + 2N\delta . \quad ∎ \qquad (D12.1)
```

The quantity whose error enters is the post-action risk $`r_{ia}`$, not the pre-review risk, and randomized pilot
trials across the permitted actions estimate it directly. The code checks the bound on 300 instances solved
exhaustively.

## D13. The joint rule

**Program.** Item $`i`$ takes one action $`a_i`$ with post-action loss $`r_{ia}`$, cost $`d_{ia}`$ and specialist
time $`t_{iaj}`$, and is audited with probability $`\pi_i`$. An audited defect ships corrected, so the item ships
with expected loss $`(1-\pi_i)\,r_{i a_i}`$. The batch program of §5 minimizes $`\sum_i (1-\pi_i)\,r_{i a_i}`$
subject to the total budget, the precision ceiling $`N^{-2}\sum_i (1-\pi_i)m_i/\pi_i \le \tau^2`$ and the specialist
capacities.

**Separation.** Attach $`\lambda \ge 0`$ to the budget, $`\nu \ge 0`$ to the precision ceiling in units of
$`N^2 V`$, and $`\gamma_j \ge 0`$ to each capacity. The Lagrangian is a sum over items of

```math
g_i(\pi_i, a) = (1-\pi_i)\,r_{ia} + \lambda c_i\pi_i + \nu m_i\Big(\frac{1}{\pi_i} - 1\Big) + \lambda d_{ia} + \sum_j \gamma_j t_{iaj}, \qquad (D13.1)
```

minus terms that do not depend on the decisions. At fixed prices the batch problem is therefore $`N`$ independent
problems.

**Audit probability.** For a fixed action write $`r = r_{ia}`$. Then
$`\partial g_i/\partial\pi_i = \lambda c_i - r - \nu m_i/\pi_i^2`$ and
$`\partial^2 g_i/\partial\pi_i^2 = 2\nu m_i/\pi_i^3 \ge 0`$. If $`\lambda c_i > r`$ the function is convex with its
stationary point at $`\sqrt{\nu m_i/(\lambda c_i - r)}`$, and the constrained minimizer is that point clipped to
$`[\pi_{\min}, 1]`$. If $`\lambda c_i \le r`$ the derivative is negative on the whole interval and the minimizer is
$`\pi_i = 1`$. Together:

```math
\pi_i^* = \mathrm{clip}_{[\pi_{\min},1]}\left(\sqrt{\frac{\nu\,m_i}{(\lambda c_i - r_{i a_i})_+}}\right), \qquad \pi_i^* = 1 \ \text{ when } \ r_{i a_i} \ge \lambda c_i . \qquad (D13.2)
```

**Action.** For a given $`\pi_i`$ the terms of $`g_i`$ that depend on the action are
$`(1-\pi_i)\,r_{ia} + \lambda d_{ia} + \sum_j \gamma_j t_{iaj}`$, and the action minimizes them. With finitely many
actions the item's problem is solved by computing $`\pi_i^*`$ for each action and keeping the best pair. ∎

**Three corners.**

1. *Risk is a rebate.* The risk $`r_{i a_i}`$ enters only through the effective price $`\lambda c_i - r_{i a_i}`$.
2. *Measurement alone.* If audits repaired nothing the term $`(1-\pi_i)r`$ would be $`r`$, the rebate would vanish,
   and $`\pi_i^* = \mathrm{clip}\,\sqrt{\nu m_i/(\lambda c_i)}`$: the allocation of D7, with $`\nu/\lambda`$ in the
   place of $`1/\lambda`$.
3. *Repair alone.* At $`\nu = 0`$ the function $`g_i`$ is linear in $`\pi_i`$ with slope $`\lambda c_i - r`$, so
   $`\pi_i^* = 1`$ when $`r/c_i \ge \lambda`$ and $`\pi_{\min}`$ otherwise: a threshold on risk per unit cost, which
   is risk-first routing.

**Solving and certifying a batch.** For any prices the minimized Lagrangian is a lower bound on the optimal value
of the program (weak duality), and the search is over $`\lambda`$, $`\nu`$ and the $`\gamma_j`$, with one pass over
the items per step. With $`\pi`$ fixed, relaxing $`z_{ia} \in \{0,1\}`$ to $`[0,1]`$ leaves a linear program with
$`N`$ assignment equalities and $`G`$ coupling inequalities, the budget and one capacity per specialist. A basic
optimal solution has at most $`N + G`$ positive variables, and every task has at least one, so at most $`G`$ tasks
are split between actions. Rounding moves at
most those tasks, and the gap between the priced bound and the rounded plan certifies the result.

**On the reference batch.** The hardest stratum has risk per unit cost $`0.35/3 = 0.117`$, above the budget price
$`\lambda`$ of 0.093 to 0.096, so the rule audits all of it. In the two easier strata the probabilities are
interior, and $`\nu = \pi_i^2(\lambda c_i - r_i)/m_i`$ computed from the routine stratum and from the intermediate
stratum agrees to six digits in both joint plans, which confirms the closed form against the numerical optimum.

## D14. The price of an auditor's error

Let the audit label $`\tilde Y`$ have sensitivity $`\text{sens} = P(\tilde Y = 1 \mid Y = 1)`$ and specificity
$`\text{spec} = P(\tilde Y = 0 \mid Y = 0)`$, estimated from blind re-audits, and let
$`J = \text{sens} + \text{spec} - 1`$. In any group with true rate $`q`$ the audit-label rate is

```math
\tilde q = \text{sens}\cdot q + (1-\text{spec})(1-q) = (1-\text{spec}) + Jq,
\qquad\text{so}\qquad \mu = \frac{\tilde\mu - (1-\text{spec})}{J} . \qquad (D14.1)
```

The estimator of D4 is unbiased for $`\tilde\mu`$, and the corrected estimate has $`1/J^2`$ times its variance. To
hold the true rate to a standard deviation $`\tau`$ the label rate must be held to $`J\tau`$. The label error also
changes the residual moments, because the labels being audited now have rate $`\tilde q_i`$:
$`\tilde m_i = \tilde q_i(1-f_i)^2 + (1-\tilde q_i)f_i^2`$, with $`\tilde M`$ and $`\tilde S`$ defined from them.
By the budget identity of D8,

```math
\frac{B_{\text{with error}}}{B_{\text{error-free}}} = \frac{\tilde S^2}{N^2J^2\tau^2 + \tilde M}\cdot\frac{N^2\tau^2 + M}{S^2} . \quad ∎ \qquad (D14.2)
```

On the reference batch at $`\tau = 0.568`$ points this is +5.2% for 5% of defects missed, +43.8% for 2% of clean
items flagged and +52.8% for both. False flags act on the clean majority: a 2% false-flag rate moves the routine
stratum's label rate from 1% to 2.98% and its residual second moment from 0.0100 to 0.0290.

## D15. Selection by tail probability

For contributor $`j`$ in stratum $`h`$ the posterior of D3 gives

```math
t_j = \Pr(a_{jh} < a_0 \mid \text{audits}) = I_{a_0}\big(\alpha_{0h} + k_j,\ \beta_{0h} + n_j - k_j\big), \qquad (D15.1)
```

the regularized incomplete beta function at the stratum standard $`a_0`$. For any list $`L`$ the posterior expected
share of contributors on it who meet the standard is $`\left\vert L\right\vert^{-1}\sum_{j\in L}(1 - t_j)`$. Among lists of a given size
the one with the largest $`t_j`$ minimizes that share, so entering contributors in decreasing order of $`t_j`$ until
the running average of $`1 - t_j`$ reaches the set false-selection rate gives the longest list that respects it. ∎

With prior $`\text{Beta}(18, 2)`$ and $`a_0 = 0.85`$: 33 of 40 correct gives $`\text{Beta}(51, 9)`$ and
$`t = 0.47`$; 6 of 8 gives $`\text{Beta}(24, 4)`$ and $`t = 0.41`$; 57 of 60 gives $`\text{Beta}(75, 5)`$ and
$`t = 0.005`$.
