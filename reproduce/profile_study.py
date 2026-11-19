"""Sections 4 to 7: the reference batch, the envelope around it, and every figure reported on them.

The reference batch gives stratum shares, defect rates, frozen risk predictions, audit
costs and the effect of one additional review. Every result is evaluated twice: at the
reference batch, and as a range over an envelope in which each entry moves independently
by up to ENVELOPE (relative), on a grid of 3 levels per entry.

All quantities are closed-form or come from a deterministic search; nothing is drawn at
random.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, replace

N = 10_000
ENVELOPE = 0.20                 # each entry moves by up to 20% of its reference value
PI_MIN = 0.03                   # sampling floor
AUDIT_SHARE = 2_000 / 13_500    # audit budget as a share of the cost of auditing everything
TOTAL_SHARE = 5_000 / 13_500    # audit plus review budget, same unit


@dataclass(frozen=True)
class Profile:
    share: tuple[float, float, float] = (0.60, 0.30, 0.10)   # routine, intermediate, hardest
    q: tuple[float, float, float] = (0.01, 0.10, 0.35)       # defect rate of original submissions
    f: tuple[float, float, float] = (0.02, 0.08, 0.30)       # frozen risk prediction
    c: tuple[float, float, float] = (1.0, 1.5, 3.0)          # cost of an independent reference audit
    review_cost_ratio: float = 0.5                           # one review costs this share of an audit
    fix: tuple[float, float, float] = (0.80, 0.80, 0.30)     # share of defects one review removes

    @property
    def n(self):
        return tuple(N * s for s in self.share)

    @property
    def m(self):
        """Mean squared residual per stratum: q(1-q) + (q-f)^2."""
        return tuple(q * (1 - f) ** 2 + (1 - q) * f**2 for q, f in zip(self.q, self.f))

    @property
    def full_audit_cost(self):
        return sum(n * c for n, c in zip(self.n, self.c))

    @property
    def d(self):
        return tuple(self.review_cost_ratio * c for c in self.c)


REFERENCE = Profile()


# ---------------------------------------------------------------------- audit allocation
def audit_cost(p: Profile, pis) -> float:
    return sum(n * c * x for n, c, x in zip(p.n, p.c, pis))


def budget_matched(p: Profile, scores, budget: float):
    """pi_h = clip(k * score_h, PI_MIN, 1), with k set so the expected audit cost is `budget`."""
    def cost(k):
        return audit_cost(p, [min(1.0, max(PI_MIN, k * s)) for s in scores])
    lo, hi = 0.0, 1.0
    while cost(hi) < budget and hi < 1e9:
        hi *= 2.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if cost(mid) < budget else (lo, mid)
    return tuple(min(1.0, max(PI_MIN, hi * s)) for s in scores)


def variance(p: Profile, pis) -> float:
    """Design variance of the corrected estimate: N^-2 sum_h n_h m_h (1 - pi_h) / pi_h."""
    return sum(n * m * (1 - x) / x for n, m, x in zip(p.n, p.m, pis)) / N**2


def queue_rate(p: Profile, pis) -> float:
    """Defect rate read off the audited queue with no correction."""
    return sum(x * n * q for x, n, q in zip(pis, p.n, p.q)) / sum(x * n for x, n in zip(pis, p.n))


def batch_rate(p: Profile) -> float:
    return sum(n * q for n, q in zip(p.n, p.q)) / N


def audit_policies(p: Profile, budget: float | None = None) -> dict:
    budget = AUDIT_SHARE * p.full_audit_cost if budget is None else budget
    return {
        "uniform": (budget / p.full_audit_cost,) * 3,
        "risk_first": budget_matched(p, p.f, budget),
        "residual_cost": budget_matched(p, [math.sqrt(m / c) for m, c in zip(p.m, p.c)], budget),
    }


def kappa(p: Profile) -> float:
    """Audit budget of the residual-cost rule as a share of the uniform budget at equal precision."""
    s = sum(n * math.sqrt(m * c) for n, m, c in zip(p.n, p.m, p.c))
    big_m = sum(n * m for n, m in zip(p.n, p.m))
    return s * s / (p.full_audit_cost * big_m)


def budget_for_precision(p: Profile, sd_pp: float, rule: str = "residual_cost") -> float:
    """Expected audit budget that reaches a standard deviation of `sd_pp` percentage points."""
    big_m = sum(n * m for n, m in zip(p.n, p.m))
    tau2 = (sd_pp / 100) ** 2
    if rule == "uniform":
        return p.full_audit_cost * big_m / (N**2 * tau2 + big_m)
    s = sum(n * math.sqrt(m * c) for n, m, c in zip(p.n, p.m, p.c))
    return s * s / (N**2 * tau2 + big_m)


# ------------------------------------------------------------------ calibration tolerance
def excess_variance_ratio(p: Profile, rel_errors) -> tuple[float, float]:
    """Excess design variance from allocating with m_hat = m (1 + eps), in units of S^2/(N^2 B).

    Returns the exact value and the second-order law Var_w(eps) / 4.
    """
    s_h = [n * math.sqrt(m * c) for n, m, c in zip(p.n, p.m, p.c)]
    s = sum(s_h)
    w = [x / s for x in s_h]
    a = sum(wi * math.sqrt(1 + e) for wi, e in zip(w, rel_errors))
    b = sum(wi / math.sqrt(1 + e) for wi, e in zip(w, rel_errors))
    mean = sum(wi * e for wi, e in zip(w, rel_errors))
    var = sum(wi * (e - mean) ** 2 for wi, e in zip(w, rel_errors))
    return a * b - 1, var / 4


def tolerance_table(p: Profile) -> dict:
    """Extra variance over the optimum, as a share of the optimal variance, for alternating
    relative errors of size e in the residual estimates, beside the second-order law."""
    s = sum(n * math.sqrt(m * c) for n, m, c in zip(p.n, p.m, p.c))
    big_m = sum(n * m for n, m in zip(p.n, p.m))
    budget = AUDIT_SHARE * p.full_audit_cost
    unit = (s * s / budget) / (s * s / budget - big_m)
    out = {}
    for e in (0.10, 0.20, 0.30, 0.50):
        exact, law = excess_variance_ratio(p, (e, -e, e))
        out[f"{int(100 * e)}%"] = {"exact": unit * exact, "law": unit * law}
    return out


# ------------------------------------------------------------------- one budget, two jobs
def delivered(p: Profile, pis, zs) -> float:
    """Expected defects shipped: an audited defect is corrected, a review removes `fix` of the rest."""
    return sum(n * (1 - x) * q * (1 - z * r) for n, x, q, z, r in zip(p.n, pis, p.q, zs, p.fix))


def reviews_by_order(p: Profile, order, budget: float):
    """Spend `budget` on reviews, stratum by stratum in the given order."""
    zs = [0.0, 0.0, 0.0]
    for h in order:
        full = p.n[h] * p.d[h]
        zs[h] = min(1.0, budget / full) if budget > 0 else 0.0
        budget -= zs[h] * full
    return tuple(zs)


def reviews_by_gain(p: Profile, pis, budget: float):
    """Reviews ranked by removable loss per unit cost, (1 - pi) q fix / d."""
    density = [(1 - x) * q * r / d for x, q, r, d in zip(pis, p.q, p.fix, p.d)]
    order = sorted(range(3), key=lambda h: -density[h])
    return reviews_by_order(p, order, budget)


def _grid(lo: float, hi: float, steps: int):
    return [lo + (hi - lo) * i / steps for i in range(steps + 1)]


def _box_search(p: Profile, total_budget: float, cap: float, rounds: int, steps: int):
    """Search the three audit probabilities on a grid, refining around the incumbent."""
    best = (math.inf, None, None)
    lo, hi = [PI_MIN] * 3, [1.0] * 3
    for _ in range(rounds):
        for pis in itertools.product(*[_grid(lo[h], hi[h], steps) for h in range(3)]):
            cost = audit_cost(p, pis)
            if cost > total_budget or variance(p, pis) > cap:
                continue
            zs = reviews_by_gain(p, pis, total_budget - cost)
            value = delivered(p, pis, zs)
            if value < best[0]:
                best = (value, pis, zs)
        if best[1] is None:
            break
        width = [(hi[h] - lo[h]) / steps for h in range(3)]
        lo = [max(PI_MIN, best[1][h] - width[h]) for h in range(3)]
        hi = [min(1.0, best[1][h] + width[h]) for h in range(3)]
    return best


def _ceiling_search(p: Profile, total_budget: float, cap: float):
    """Search along the precision ceiling: two audit probabilities are free and the third
    is the smallest value that keeps the variance at or below the ceiling."""
    n, m = p.n, p.m
    budget_k = cap * N**2
    best = (math.inf, None, None)
    for k in range(3):
        a, b = [h for h in range(3) if h != k]
        lo, hi = [PI_MIN, PI_MIN], [1.0, 1.0]
        incumbent = None
        for steps in (60, 20, 20, 20, 20, 20):
            for xa in _grid(lo[0], hi[0], steps):
                for xb in _grid(lo[1], hi[1], steps):
                    rest = budget_k - n[a] * m[a] * (1 / xa - 1) - n[b] * m[b] * (1 / xb - 1)
                    if rest < 0:
                        continue
                    xk = max(PI_MIN, 1 / (1 + rest / (n[k] * m[k])))
                    pis = [0.0, 0.0, 0.0]
                    pis[a], pis[b], pis[k] = xa, xb, xk
                    cost = audit_cost(p, pis)
                    if cost > total_budget:
                        continue
                    zs = reviews_by_gain(p, pis, total_budget - cost)
                    value = delivered(p, pis, zs)
                    if incumbent is None or value < incumbent[0]:
                        incumbent = (value, tuple(pis), zs, xa, xb)
            if incumbent is None:
                break
            wa, wb = (hi[0] - lo[0]) / steps, (hi[1] - lo[1]) / steps
            lo = [max(PI_MIN, incumbent[3] - wa), max(PI_MIN, incumbent[4] - wb)]
            hi = [min(1.0, incumbent[3] + wa), min(1.0, incumbent[4] + wb)]
        if incumbent is not None and incumbent[0] < best[0]:
            best = incumbent[:3]
    return best


def joint_rule(p: Profile, total_budget: float, sd_cap: float | None):
    """Minimize delivered defects over audit probabilities and reviews at a total budget,
    with the corrected estimate held at or below `sd_cap` (None drops the precision ceiling).

    Reviews are optimal in closed form for any audit plan, so the search runs over the audit
    probabilities: over the whole box when there is no ceiling, and along the ceiling when
    there is one, with a box search as a cross-check for plans that leave the ceiling slack.
    """
    if sd_cap is None:
        return _box_search(p, total_budget, math.inf, rounds=9, steps=16)
    cap = sd_cap**2 * (1 + 1e-12)
    on_ceiling = _ceiling_search(p, total_budget, cap)
    in_box = _box_search(p, total_budget, cap, rounds=1, steps=16)
    return on_ceiling if on_ceiling[0] <= in_box[0] else in_box


def rule_multipliers(p: Profile, pis, zs) -> dict:
    """Prices implied by a joint plan: lambda from the stratum whose reviews are partly
    funded, nu from each stratum whose audit probability is interior. Equal nu values
    confirm the closed-form audit rule pi^2 = nu m / (lambda c - r)."""
    lam = None
    for h in range(3):
        if 1e-6 < zs[h] < 1 - 1e-6:
            lam = (1 - pis[h]) * p.q[h] * p.fix[h] / p.d[h]
    nus = {}
    if lam is not None:
        for h in range(3):
            if PI_MIN + 1e-6 < pis[h] < 1 - 1e-6:
                r = p.q[h] * (1 - p.fix[h] * zs[h])
                nus[h] = pis[h] ** 2 * (lam * p.c[h] - r) / p.m[h]
    return {"lambda": lam, "nu_by_stratum": nus}


def end_to_end(p: Profile, with_corner: bool = True) -> dict:
    audit_budget = AUDIT_SHARE * p.full_audit_cost
    total = TOTAL_SHARE * p.full_audit_cost
    pol = audit_policies(p, audit_budget)
    sd_uniform = math.sqrt(variance(p, pol["uniform"]))
    rows = {}
    by_risk = sorted(range(3), key=lambda h: -p.f[h])
    rows["risk_first_both"] = (pol["risk_first"], reviews_by_order(p, by_risk, total - audit_budget))
    rows["measure_then_repair"] = (
        pol["residual_cost"],
        reviews_by_gain(p, pol["residual_cost"], total - audit_budget),
    )
    joint = joint_rule(p, total, sd_uniform)
    rows["joint_rule"] = (joint[1], joint[2])
    sd_risk_first = math.sqrt(variance(p, pol["risk_first"]))
    matched = joint_rule(p, total, sd_risk_first)
    rows["joint_rule_matched_precision"] = (matched[1], matched[2])
    sd_sequential = math.sqrt(variance(p, pol["residual_cost"]))
    sequential = joint_rule(p, total, sd_sequential)
    rows["joint_rule_sequential_precision"] = (sequential[1], sequential[2])
    if with_corner:
        corner = joint_rule(p, total, None)
        rows["joint_rule_no_ceiling"] = (corner[1], corner[2])
    out = {"no_handling": N * batch_rate(p), "sd_uniform_pp": 100 * sd_uniform}
    for name, (pis, zs) in rows.items():
        out[name] = {
            "pi_percent": [round(100 * x, 2) for x in pis],
            "review_percent": [round(100 * x, 1) for x in zs],
            "audit_cost": audit_cost(p, pis),
            "sd_pp": 100 * math.sqrt(variance(p, pis)),
            "delivered": delivered(p, pis, zs),
        }
    out["joint_rule"]["multipliers"] = rule_multipliers(p, joint[1], joint[2])
    out["joint_rule_matched_precision"]["multipliers"] = rule_multipliers(p, matched[1], matched[2])
    return out


# --------------------------------------------------------------- audit-label reliability
def reliability_price(p: Profile, sens: float, spec: float, sd_pp: float) -> dict:
    """Audit budget needed for the same precision on the true rate when audit labels err."""
    j = sens + spec - 1
    noisy = replace(p, q=tuple((1 - spec) + j * q for q in p.q))
    exact = budget_for_precision(noisy, j * sd_pp) / budget_for_precision(p, sd_pp)
    return {"youden": j, "variance_factor": 1 / j**2, "budget_factor": exact}


# ------------------------------------------------------------------- contributor records
def beta_tail(a: float, b: float, x: float, steps: int = 20_000) -> float:
    """P(theta < x) for theta ~ Beta(a, b), by Simpson's rule on the log-density."""
    log_norm = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)

    def pdf(t):
        if t <= 0.0 or t >= 1.0:
            return 0.0
        return math.exp(log_norm + (a - 1) * math.log(t) + (b - 1) * math.log(1 - t))

    h = x / steps
    total = pdf(0.0) + pdf(x)
    for i in range(1, steps):
        total += (4 if i % 2 else 2) * pdf(i * h)
    return total * h / 3


# ---------------------------------------------------------------------------- envelope
def envelope_profiles(width: float = ENVELOPE):
    """Every batch with each entry at -width, 0 or +width of its reference value.

    Varied: the three defect rates, the three predictions, the two cost ratios, and the
    intermediate and hardest shares (the routine share takes the remainder).
    """
    base = REFERENCE
    levels = (1 - width, 1.0, 1 + width)
    for k in itertools.product(levels, repeat=10):
        s2, s3 = base.share[1] * k[8], base.share[2] * k[9]
        yield replace(
            base,
            share=(1 - s2 - s3, s2, s3),
            q=tuple(v * x for v, x in zip(base.q, k[0:3])),
            f=tuple(v * x for v, x in zip(base.f, k[3:6])),
            c=(1.0, base.c[1] * k[6], base.c[2] * k[7]),
        )


def headline(p: Profile) -> dict:
    pol = audit_policies(p)
    v = {k: variance(p, x) for k, x in pol.items()}
    return {
        "queue_overstatement": queue_rate(p, pol["risk_first"]) / batch_rate(p),
        "risk_first_variance_change": v["risk_first"] / v["uniform"] - 1,
        "residual_cost_variance_change": v["residual_cost"] / v["uniform"] - 1,
        "risk_first_over_residual_cost": v["risk_first"] / v["residual_cost"] - 1,
        "budget_saved_at_equal_precision": 1 - kappa(p),
    }


def envelope_ranges(width: float = ENVELOPE) -> dict:
    lo, hi = {}, {}
    for p in envelope_profiles(width):
        for key, value in headline(p).items():
            lo[key] = min(lo.get(key, value), value)
            hi[key] = max(hi.get(key, value), value)
    return {key: (lo[key], hi[key]) for key in lo}


def end_to_end_envelope(width: float = ENVELOPE) -> dict:
    """Range of the end-to-end comparison over the corners of the envelope in the eight entries
    that enter it: the hardest stratum's share, prediction and audit cost, the defect rates
    and review effects of the two harder strata, and the review cost ratio."""
    keys = ("matched_precision_defects_vs_risk_first", "sequential_precision_defects_vs_sequential")
    lo, hi = {}, {}
    base = REFERENCE
    for k in itertools.product((1 - width, 1 + width), repeat=8):
        s3 = base.share[2] * k[0]
        p = replace(
            base,
            share=(1 - base.share[1] - s3, base.share[1], s3),
            f=(base.f[0], base.f[1], base.f[2] * k[1]),
            c=(1.0, base.c[1], base.c[2] * k[2]),
            q=(base.q[0], base.q[1] * k[3], base.q[2] * k[4]),
            fix=(base.fix[0], min(1.0, base.fix[1] * k[5]), min(1.0, base.fix[2] * k[6])),
            review_cost_ratio=base.review_cost_ratio * k[7],
        )
        r = end_to_end(p, with_corner=False)
        base_row = r["risk_first_both"]
        vals = {
            keys[0]: r["joint_rule_matched_precision"]["delivered"] / base_row["delivered"] - 1,
            keys[1]: r["joint_rule_sequential_precision"]["delivered"] / r["measure_then_repair"]["delivered"] - 1,
        }
        for key, value in vals.items():
            lo[key] = min(lo.get(key, value), value)
            hi[key] = max(hi.get(key, value), value)
    return {key: (lo[key], hi[key]) for key in keys}


def run(with_envelope: bool = True) -> dict:
    p = REFERENCE
    pol = audit_policies(p)
    v_uniform = variance(p, pol["uniform"])
    out = {
        "batch_rate_percent": 100 * batch_rate(p),
        "policies": {
            name: {
                "pi_percent": [round(100 * x, 2) for x in pis],
                "sd_pp": 100 * math.sqrt(variance(p, pis)),
                "variance_change_percent": 100 * (variance(p, pis) / v_uniform - 1),
                "queue_rate_percent": 100 * queue_rate(p, pis),
            }
            for name, pis in pol.items()
        },
        "headline": headline(p),
        "precision_price": {
            sd: (budget_for_precision(p, sd), budget_for_precision(p, sd, "uniform"))
            for sd in (0.50, 0.40, 0.30, 0.25)
        },
        "calibration_tolerance": tolerance_table(p),
        "end_to_end": end_to_end(p),
        "reliability_price": {
            f"sens {sens:.2f}, spec {spec:.2f}": reliability_price(p, sens, spec, 100 * math.sqrt(v_uniform))
            for sens, spec in ((0.95, 1.00), (1.00, 0.98), (0.95, 0.98))
        },
        "contributor_tail": {
            "A_40_audits_33_ok": beta_tail(18 + 33, 2 + 7, 0.85),
            "B_8_audits_6_ok": beta_tail(18 + 6, 2 + 2, 0.85),
            "C_60_audits_57_ok": beta_tail(18 + 57, 2 + 3, 0.85),
        },
    }
    if with_envelope:
        out["envelope"] = {"width": ENVELOPE, "ranges": envelope_ranges(), "end_to_end": end_to_end_envelope()}
    return out


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2))
