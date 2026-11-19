"""Section 5: review allocation by removable loss, and the worked example.

Two groups of 100 tasks. One review slot per task, equal costs, capacity 100 reviews.
Ranking by initial risk r_i0 and ranking by marginal gain Delta_i = r_i0 - r_i1 are
compared, and a brute-force search confirms that the marginal-gain order is optimal.
The script also checks the exchange identity Delta F = Delta_i - Delta_k and the
2 N delta performance bound for allocation under estimated risks.
"""

from __future__ import annotations

import itertools
import random

GROUPS = [
    # (count, initial risk r0, risk after review r1)
    (100, 0.40, 0.30),
    (100, 0.15, 0.01),
]
CAPACITY = 100


def expected_errors(reviewed_per_group) -> float:
    total = 0.0
    for (count, r0, r1), reviewed in zip(GROUPS, reviewed_per_group):
        total += reviewed * r1 + (count - reviewed) * r0
    return total


def allocate(key) -> list[int]:
    """Fill review capacity greedily in the order given by key(group)."""
    order = sorted(range(len(GROUPS)), key=lambda g: key(GROUPS[g]), reverse=True)
    left, reviewed = CAPACITY, [0] * len(GROUPS)
    for g in order:
        take = min(left, GROUPS[g][0])
        reviewed[g], left = take, left - take
    return reviewed


def brute_force_optimum() -> float:
    best = float("inf")
    for a in range(GROUPS[0][0] + 1):
        b = CAPACITY - a
        if 0 <= b <= GROUPS[1][0]:
            best = min(best, expected_errors([a, b]))
    return best


def exchange_identity_holds(trials: int = 10_000, seed: int = 5) -> bool:
    """Moving one slot from task i to task k changes loss by Delta_i - Delta_k."""
    rng = random.Random(seed)
    for _ in range(trials):
        ri0, rk0 = rng.random(), rng.random()
        ri1, rk1 = ri0 * rng.random(), rk0 * rng.random()
        before = ri1 + rk0            # i reviewed, k not
        after = ri0 + rk1             # k reviewed, i not
        if abs((after - before) - ((ri0 - ri1) - (rk0 - rk1))) > 1e-12:
            return False
    return True


def performance_bound_holds(trials: int = 300, n: int = 6, seed: int = 11) -> bool:
    """F(z_hat) <= F(z*) + 2 N delta when every action-risk estimate is within delta.

    Small random instances: n tasks, two actions (accept / review), capacity n // 2,
    unit review time. Exhaustive search gives both the true and the predicted optimum.
    """
    rng = random.Random(seed)
    for _ in range(trials):
        r0 = [rng.random() for _ in range(n)]
        r1 = [x * rng.random() for x in r0]
        delta = 0.1 * rng.random()
        h0 = [x + rng.uniform(-delta, delta) for x in r0]
        h1 = [x + rng.uniform(-delta, delta) for x in r1]

        def loss(sel, a, b):
            return sum(b[i] if i in sel else a[i] for i in range(n))

        feasible = [set(c) for k in range(n // 2 + 1) for c in itertools.combinations(range(n), k)]
        z_hat = min(feasible, key=lambda s: loss(s, h0, h1))
        z_star = min(feasible, key=lambda s: loss(s, r0, r1))
        if loss(z_hat, r0, r1) > loss(z_star, r0, r1) + 2 * n * delta + 1e-12:
            return False
    return True


def run() -> dict:
    by_risk = allocate(lambda g: g[1])
    by_gain = allocate(lambda g: g[1] - g[2])
    e_risk, e_gain = expected_errors(by_risk), expected_errors(by_gain)
    return {
        "reviews_by_initial_risk": by_risk,
        "reviews_by_marginal_gain": by_gain,
        "expected_errors_initial_risk": e_risk,
        "expected_errors_marginal_gain": e_gain,
        "reduction_percent": 100 * (1 - e_gain / e_risk),
        "brute_force_optimum": brute_force_optimum(),
        "exchange_identity": exchange_identity_holds(),
        "two_n_delta_bound": performance_bound_holds(),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2))
