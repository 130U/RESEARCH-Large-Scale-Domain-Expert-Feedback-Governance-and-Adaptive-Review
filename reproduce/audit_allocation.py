"""Sections 2 to 4 and 6: audit allocation at equal expected cost on the reference batch.

The reference batch has N = 10,000 submissions in three strata. Every policy spends the same
expected audit budget B = 2,000 cost units with a sampling floor of 3%, and every policy
uses the same prediction-assisted IPW estimator

    mu_hat = (1/N) * sum_i [ f_i + S_i / pi_i * (Y_i - f_i) ].

The script computes the exact design variance of each policy and checks it against
repeated draws of the audit lottery, the independent Bernoulli design the program runs. Within a stratum all items
share f_h and pi_h, so the number of audited error items and audited clean items are
independent binomials; drawing those two counts is exactly equivalent in distribution
to drawing 10,000 Bernoulli indicators, and much faster.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

# ------------------------------------------------------------------ the reference batch
SIZES = (6_000, 3_000, 1_000)        # n_h
ERRORS = (60, 300, 350)              # k_h, so the true batch defect rate is 7.10%
COSTS = (1.0, 1.5, 3.0)              # c_h, unit cost of an independent reference audit
PREDICTIONS = (0.02, 0.08, 0.30)     # f_h, frozen before the batch's labels are revealed
BUDGET = 2_000.0                     # B, expected audit cost per batch
PI_MIN = 0.03                        # sampling floor
SHRINK_RHO = 0.70                    # weight on uniform sampling in the defensive mixture

N = sum(SIZES)
TRUE_RATE = sum(ERRORS) / N


def mean_squared_residual(h: int) -> float:
    """Finite-batch mean of (Y_i - f_i)^2 within stratum h.

    Equals q(1-q) + (q-f)^2 with q = k_h / n_h: Bernoulli variance plus squared
    calibration error (manuscript Section 3).
    """
    n, k, f = SIZES[h], ERRORS[h], PREDICTIONS[h]
    return (k * (1 - f) ** 2 + (n - k) * f**2) / n


M_TRUE = tuple(mean_squared_residual(h) for h in range(3))


def expected_cost(pis) -> float:
    return sum(n * c * p for n, c, p in zip(SIZES, COSTS, pis))


def budget_matched(scores) -> tuple[float, ...]:
    """pi_h = clip(kappa * score_h, PI_MIN, 1) with kappa chosen so expected cost = BUDGET.

    Expected cost is continuous and nondecreasing in kappa, so bisection finds kappa.
    """
    lo, hi = 0.0, 1.0
    while expected_cost([min(1.0, max(PI_MIN, hi * s)) for s in scores]) < BUDGET:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if expected_cost([min(1.0, max(PI_MIN, mid * s)) for s in scores]) < BUDGET:
            lo = mid
        else:
            hi = mid
    return tuple(min(1.0, max(PI_MIN, hi * s)) for s in scores)


def policies() -> dict[str, tuple[float, ...]]:
    total_cost = sum(n * c for n, c in zip(SIZES, COSTS))
    uniform = (BUDGET / total_cost,) * 3
    by_risk = budget_matched(PREDICTIONS)
    ideal = budget_matched([math.sqrt(m / c) for m, c in zip(M_TRUE, COSTS)])
    reversed_m = M_TRUE[::-1]  # stress case: residual ordering reversed across strata
    from_reversed = budget_matched([math.sqrt(m / c) for m, c in zip(reversed_m, COSTS)])
    mixture = tuple((1 - SHRINK_RHO) * a + SHRINK_RHO * u for a, u in zip(from_reversed, uniform))
    return {
        "uniform": uniform,
        "predicted_risk": by_risk,
        "residual_cost_ideal": ideal,
        "reversed_estimates": from_reversed,
        "reversed_estimates_mixture_70": mixture,
    }


def design_variance(pis) -> float:
    """Exact Var_S(mu_hat) = N^-2 * sum_i (1 - pi_i)/pi_i * e_i^2 for the fixed batch."""
    return sum((1 - p) / p * n * m for n, m, p in zip(SIZES, M_TRUE, pis)) / N**2


def optimal_variance_unclipped() -> float:
    """Closed form V_optimal = N^-2 [ (sum_i sqrt(m_i c_i))^2 / B - sum_i m_i ]."""
    root = sum(n * math.sqrt(m * c) for n, m, c in zip(SIZES, M_TRUE, COSTS))
    return (root**2 / BUDGET - sum(n * m for n, m in zip(SIZES, M_TRUE))) / N**2


def uncorrected_rate(pis) -> float:
    """E[Y | S = 1]: the error rate an uncorrected dashboard reads in the audited queue."""
    return sum(p * k for p, k in zip(pis, ERRORS)) / sum(p * n for p, n in zip(pis, SIZES))


def mixture_variance_cap(rho: float) -> float:
    """Worst-case guarantee of the mixture (docs/derivations.md, D10): for ANY allocation pi_hat,
    pi(rho) = (1 - rho) pi_hat + rho p satisfies pi_i >= rho p, hence

        V(pi(rho)) / V_uniform <= (1 - rho p) / (rho (1 - p)).
    """
    total_cost = sum(n * c for n, c in zip(SIZES, COSTS))
    p = BUDGET / total_cost
    return (1 - rho * p) / (rho * (1 - p))


@dataclass
class Replication:
    mean: float
    variance: float
    raw_rate_mean: float
    variance_estimator_mean: float


def replicate(pis, reps: int, rng: random.Random) -> Replication:
    """Draw the audit lottery `reps` times and summarize the estimator over the draws."""
    base = sum(n * f for n, f in zip(SIZES, PREDICTIONS))
    total = total_sq = raw_total = vhat_total = 0.0
    for _ in range(reps):
        correction = vhat = 0.0
        audited = audited_errors = 0
        for n, k, f, p in zip(SIZES, ERRORS, PREDICTIONS, pis):
            s1 = rng.binomialvariate(k, p)        # audited items with Y = 1
            s0 = rng.binomialvariate(n - k, p)    # audited items with Y = 0
            correction += (s1 * (1 - f) - s0 * f) / p
            # unbiased design-variance estimator, D5 in docs/derivations.md
            vhat += (1 - p) / p**2 * (s1 * (1 - f) ** 2 + s0 * f**2)
            audited += s1 + s0
            audited_errors += s1
        est = (base + correction) / N
        total += est
        total_sq += est * est
        raw_total += audited_errors / audited
        vhat_total += vhat / N**2
    mean = total / reps
    var = (total_sq - reps * mean * mean) / (reps - 1)
    return Replication(mean, var, raw_total / reps, vhat_total / reps)


def run(reps: int = 200_000, seed: int = 20231101) -> dict:
    rng = random.Random(seed)
    pols = policies()
    v_uniform = design_variance(pols["uniform"])
    rows = {}
    for name, pis in pols.items():
        v = design_variance(pis)
        rep = replicate(pis, reps, rng) if reps else None
        rows[name] = {
            "pi_percent": [round(100 * p, 2) for p in pis],
            "expected_cost": expected_cost(pis),
            "sd_pp": 100 * math.sqrt(v),
            "variance_change_percent": 100 * (v / v_uniform - 1),
            "uncorrected_rate_percent": 100 * uncorrected_rate(pis),
            "lottery_mean_percent": None if rep is None else 100 * rep.mean,
            "lottery_queue_rate_percent": None if rep is None else 100 * rep.raw_rate_mean,
            "lottery_vs_exact_variance_percent": None if rep is None else 100 * (rep.variance / v - 1),
            "variance_estimator_vs_exact_percent": None if rep is None else 100 * (rep.variance_estimator_mean / v - 1),
        }
    return {
        "mixture_variance_cap_percent": 100 * (mixture_variance_cap(SHRINK_RHO) - 1),
        "true_rate_percent": 100 * TRUE_RATE,
        "mean_squared_residuals": M_TRUE,
        "closed_form_optimal_sd_pp": 100 * math.sqrt(optimal_variance_unclipped()),
        "reps": reps,
        "seed": seed,
        "policies": rows,
    }


if __name__ == "__main__":
    import json
    import sys

    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    print(json.dumps(run(reps), indent=2))
