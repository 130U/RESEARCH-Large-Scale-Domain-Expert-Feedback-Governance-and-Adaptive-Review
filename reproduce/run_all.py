"""Recompute every figure in the article and compare it with the text.

    python reproduce/run_all.py            # full run
    python reproduce/run_all.py --quick    # fewer draws of the audit lottery, no envelope

Writes reproduce/results.md and exits with status 1 if any figure disagrees.
Standard library only (Python 3.12+, for random.binomialvariate).
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import audit_allocation  # noqa: E402
import profile_study  # noqa: E402
import remediation  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--seed", type=int, default=20231101)
    args = parser.parse_args()
    reps = 20_000 if args.quick else 200_000
    lottery_tol = 3.0 if args.quick else 1.0  # percent gap between replicated and exact variance

    audit = audit_allocation.run(reps, args.seed)
    rem = remediation.run()
    study = profile_study.run(with_envelope=not args.quick)
    pol = audit["policies"]
    head = study["headline"]
    e2e = study["end_to_end"]
    sections: list[tuple[str, list]] = []
    rows: list = []

    def section(title: str) -> None:
        nonlocal rows
        rows = []
        sections.append((title, rows))

    def check(label, value, article, tol, where, shown=None):
        rows.append((label, value, shown if shown is not None else article, where, abs(value - article) <= tol))

    def check_true(label, value, where, shown="holds"):
        rows.append((label, None, shown, where, bool(value)))

    # ------------------------------------------------------------------ Section 6, measurement
    section("Measurement at equal audit budget (Section 6)")
    check("Batch defect rate (%)", study["batch_rate_percent"], 7.10, 0.005, "§6")
    check("Audit budget as a share of a full audit (%)", 100 * profile_study.AUDIT_SHARE, 14.8, 0.05, "§6")
    article_pi = {
        "uniform": (14.81, 14.81, 14.81),
        "predicted_risk": (3.00, 11.56, 43.33),
        "residual_cost_ideal": (7.89, 19.37, 21.84),
    }
    article_sd = {"uniform": 0.568, "predicted_risk": 0.657, "residual_cost_ideal": 0.515}
    names = {"uniform": "Uniform", "predicted_risk": "Risk-first", "residual_cost_ideal": "Residual- and cost-aware"}
    for key, pis in article_pi.items():
        for h, (got, want) in enumerate(zip(pol[key]["pi_percent"], pis), start=1):
            check(f"{names[key]}: audit probability, stratum {h} (%)", got, want, 0.005, "§6 table")
        check(f"{names[key]}: expected audit cost", pol[key]["expected_cost"], 2000, 1e-6, "§6")
        check(f"{names[key]}: standard deviation of the estimate (pp)", pol[key]["sd_pp"], article_sd[key], 0.0005, "§6 table")
    check("Risk-first: variance relative to uniform (%)", pol["predicted_risk"]["variance_change_percent"], 33.8, 0.05, "§6 table")
    check("Residual- and cost-aware: variance relative to uniform (%)", pol["residual_cost_ideal"]["variance_change_percent"], -17.8, 0.05, "§6 table")
    check("Risk-first queue: uncorrected error rate (%)", pol["predicted_risk"]["uncorrected_rate_percent"], 19.60, 0.005, "§6")
    check("Queue overstatement (times the batch rate)", head["queue_overstatement"], 2.76, 0.005, "§6")
    check("Risk-first against the residual- and cost-aware rule: extra variance (%)", 100 * head["risk_first_over_residual_cost"], 62.7, 0.05, "§6")
    check("Same result from the two independent implementations (pp)", study["policies"]["residual_cost"]["sd_pp"], pol["residual_cost_ideal"]["sd_pp"], 1e-9, "§6", shown="equal")

    # ------------------------------------------------------------------ the estimator itself
    section("The estimator under repeated draws of the audit lottery (Sections 2 and 3)")
    for key in pol:
        label = names.get(key, key.replace("_", " ").capitalize())
        check(f"{label}: mean of the estimate over the draws (%)", pol[key]["lottery_mean_percent"], 7.10, 0.02, "§2")
        check(f"{label}: variance over the draws against the exact formula (%)", pol[key]["lottery_vs_exact_variance_percent"], 0.0, lottery_tol, "§3", shown="0")
        check(f"{label}: variance estimator against the exact variance (%)", pol[key]["variance_estimator_vs_exact_percent"], 0.0, lottery_tol, "D5", shown="0")
    check("Risk-first queue: uncorrected rate averaged over the draws (%)", pol["predicted_risk"]["lottery_queue_rate_percent"], 19.60, 0.05, "§6")

    # ------------------------------------------------------------------ Section 4
    section("What the allocation is worth (Sections 4 and 6)")
    check("Closed-form optimal variance equals the rule's variance (pp)", audit["closed_form_optimal_sd_pp"], pol["residual_cost_ideal"]["sd_pp"], 1e-9, "§4", shown="equal")
    check("Budget ratio κ", profile_study.kappa(profile_study.REFERENCE), 0.848, 0.0005, "§6")
    check("Audit budget saved at any precision target (%)", 100 * head["budget_saved_at_equal_precision"], 15.2, 0.05, "§6")
    price = {0.50: (2100, 2475), 0.40: (2974, 3506), 0.30: (4399, 5185), 0.25: (5419, 6387)}
    for sd, (rule_budget, uniform_budget) in price.items():
        got = study["precision_price"][sd]
        check(f"Audit budget for a standard deviation of {sd:.2f} pp, residual- and cost-aware", got[0], rule_budget, 0.5, "§6 table")
        check(f"Audit budget for a standard deviation of {sd:.2f} pp, uniform", got[1], uniform_budget, 0.5, "§6 table")
        check(f"Ratio of the two budgets at {sd:.2f} pp", got[0] / got[1], 0.848, 0.0005, "§4")
    tolerance = {"10%": (0.30, 0.30, 0.005), "20%": (1.23, 1.19, 0.005), "30%": (2.88, 2.68, 0.005), "50%": (9.2, 7.4, 0.05)}
    for size, (exact, law, tol) in tolerance.items():
        got = study["calibration_tolerance"][size]
        check(f"Relative error {size}: variance above the optimum (%)", 100 * got["exact"], exact, tol, "§6 table")
        check(f"Relative error {size}: quarter-variance law (%)", 100 * got["law"], law, tol, "§6 table")
    for h, want in enumerate((23.00, 11.77, 3.00), start=1):
        check(f"Reversed residual ordering: audit probability, stratum {h} (%)", pol["reversed_estimates"]["pi_percent"][h - 1], want, 0.005, "§6")
    check("Reversed residual ordering: variance above uniform (%)", pol["reversed_estimates"]["variance_change_percent"], 199.7, 0.05, "§6")
    check("Same estimates with weight 0.7 on the uniform design (%)", pol["reversed_estimates_mixture_70"]["variance_change_percent"], 17.1, 0.05, "§6")
    check("Guaranteed ceiling of the mixture for any estimates (%)", audit["mixture_variance_cap_percent"], 50.3, 0.05, "§4, §6")

    # ------------------------------------------------------------------ Section 5
    section("Repair by removable loss (Section 5)")
    check("Worked example: expected errors left, ranking by initial risk", rem["expected_errors_initial_risk"], 45, 1e-9, "§5")
    check("Worked example: expected errors left, ranking by removable loss", rem["expected_errors_marginal_gain"], 41, 1e-9, "§5")
    check("Worked example: reduction at the same review volume (%)", rem["reduction_percent"], 8.89, 0.005, "§5")
    check("Ranking by removable loss equals the exhaustive optimum", rem["brute_force_optimum"], 41, 1e-9, "§5")
    check_true("Exchange identity ΔF = Δᵢ − Δₖ on 10,000 random pairs", rem["exchange_identity"], "§5")
    check_true("Bound F(ẑ) ≤ F(z*) + 2Nδ on 300 instances solved exhaustively", rem["two_n_delta_bound"], "§5")

    # ------------------------------------------------------------------ Section 6, one budget
    section("One budget, two products (Section 6)")
    check("Defects shipped with no handling", e2e["no_handling"], 710, 0.5, "§6")
    check("Total budget as a share of a full audit (%)", 100 * profile_study.TOTAL_SHARE, 37, 0.5, "§6")
    plans = {
        "risk_first_both": ("Risk-first for audits and reviews", (3.00, 11.56, 43.33), (0, 67, 100), 0.657, 320.9),
        "measure_then_repair": ("Measurement rule, then reviews by removable loss", (7.89, 19.37, 21.84), (0, 100, 50), 0.515, 336.2),
        "joint_rule_matched_precision": ("Joint rule at the precision of risk-first routing", (3.31, 9.57, 100.0), (0, 61, 0), 0.657, 197.1),
        "joint_rule": ("Joint rule at the precision of uniform sampling", (4.20, 12.74, 100.0), (0, 52, 0), 0.568, 209.9),
        "joint_rule_no_ceiling": ("Joint rule with no precision ceiling", (3.00, 3.00, 100.0), (0, 75, 0), 1.035, 174.9),
    }
    for key, (label, pis, reviews, sd, shipped) in plans.items():
        row = e2e[key]
        for h in range(3):
            check(f"{label}: audit probability, stratum {h + 1} (%)", row["pi_percent"][h], pis[h], 0.005, "§6 table")
            check(f"{label}: share reviewed, stratum {h + 1} (%)", row["review_percent"][h], reviews[h], 0.5, "§6 table")
        check(f"{label}: standard deviation of the estimate (pp)", row["sd_pp"], sd, 0.0005, "§6 table")
        check(f"{label}: defects shipped", row["delivered"], shipped, 0.05, "§6 table")
        check_true(f"{label}: spends no more than the total budget", row["audit_cost"] <= 5000 + 1e-6, "§6", shown="≤ 5,000")
    base = e2e["risk_first_both"]["delivered"]
    check("Joint rule against risk-first at the same budget and precision (% fewer defects)", 100 * (1 - e2e["joint_rule_matched_precision"]["delivered"] / base), 38.6, 0.05, "§6")
    check("Joint rule held to the precision of uniform sampling (% fewer defects)", 100 * (1 - e2e["joint_rule"]["delivered"] / base), 34.6, 0.05, "§6")
    sequential = e2e["measure_then_repair"]["delivered"]
    check("Joint rule held to the sequential plan's precision, against that plan (% fewer defects)", 100 * (1 - e2e["joint_rule_sequential_precision"]["delivered"] / sequential), 34.7, 0.05, "§6")
    check("Risk per unit cost in the hardest stratum", 0.35 / 3, 0.117, 0.0005, "§6")
    for key in ("joint_rule_matched_precision", "joint_rule"):
        mult = e2e[key]["multipliers"]
        label = plans[key][0]
        check_true(f"{label}: budget price λ = {mult['lambda']:.4f} lies in 0.093 to 0.096", 0.0925 <= mult["lambda"] <= 0.0965, "§6", shown="0.093 to 0.096")
        nu = list(mult["nu_by_stratum"].values())
        check_true(f"{label}: ν from the routine and the intermediate stratum agree to six digits", abs(nu[0] / nu[1] - 1) < 5e-7, "§5, §6")
    check("Shipped defects paid for holding the estimate at 0.657 pp", e2e["joint_rule_matched_precision"]["delivered"] - e2e["joint_rule_no_ceiling"]["delivered"], 22, 0.5, "§6")
    check("Further defects paid for tightening it to 0.568 pp", e2e["joint_rule"]["delivered"] - e2e["joint_rule_matched_precision"]["delivered"], 13, 0.5, "§6")

    # ------------------------------------------------------------------ Section 7
    section("Operating the design (Section 7)")
    price7 = study["reliability_price"]
    check("Auditor misses 5% of defects: audit budget (%)", 100 * (price7["sens 0.95, spec 1.00"]["budget_factor"] - 1), 5.2, 0.05, "§7 table")
    check("Auditor flags 2% of clean items: audit budget (%)", 100 * (price7["sens 1.00, spec 0.98"]["budget_factor"] - 1), 43.8, 0.05, "§7 table")
    check("Both errors: audit budget (%)", 100 * (price7["sens 0.95, spec 0.98"]["budget_factor"] - 1), 52.8, 0.05, "§7 table")
    ratio = (price7["sens 1.00, spec 0.98"]["budget_factor"] - 1) / (price7["sens 0.95, spec 1.00"]["budget_factor"] - 1)
    check("Cost of false flags relative to misses (times)", ratio, 8, 0.5, "§7")
    ref = profile_study.REFERENCE
    flagged_rate = 0.02 + 0.98 * ref.q[0]
    check("Routine stratum: audit-label rate with 2% false flags (%)", 100 * flagged_rate, 2.98, 0.005, "D14")
    check("Routine stratum: residual second moment, error-free auditor", ref.m[0], 0.0100, 0.00005, "D14")
    check("Routine stratum: residual second moment with 2% false flags", flagged_rate * (1 - ref.f[0]) ** 2 + (1 - flagged_rate) * ref.f[0] ** 2, 0.0290, 0.00005, "D14")
    tail = study["contributor_tail"]
    check("Tail probability, 33 of 40 audited tasks correct", tail["A_40_audits_33_ok"], 0.47, 0.005, "§7")
    check("Tail probability, 6 of 8 correct", tail["B_8_audits_6_ok"], 0.41, 0.005, "§7")
    check("Tail probability, 57 of 60 correct", tail["C_60_audits_57_ok"], 0.005, 0.0005, "§7")

    # ------------------------------------------------------------------ the envelope
    if not args.quick:
        section("Ranges over the 20% envelope (Summary and Section 6)")
        env = study["envelope"]["ranges"]
        e2e_env = study["envelope"]["end_to_end"]

        def check_range(label, got, low, high, tol, where):
            check(f"{label}, low end", got[0], low, tol, where)
            check(f"{label}, high end", got[1], high, tol, where)

        check_range("Queue overstatement (times)", env["queue_overstatement"], 1.96, 4.14, 0.005, "§6")
        check_range("Risk-first: variance relative to uniform (%)", [100 * x for x in env["risk_first_variance_change"]], -16, 97, 0.5, "§6 table")
        check_range("Residual- and cost-aware: variance relative to uniform (%)", [100 * x for x in env["residual_cost_variance_change"]], -32, -9, 0.5, "§6 table")
        check_range("Risk-first against the rule: extra variance (%)", [100 * x for x in env["risk_first_over_residual_cost"]], 14, 137, 0.5, "§6")
        check_range("Audit budget saved at equal precision (%)", [100 * x for x in env["budget_saved_at_equal_precision"]], 7.5, 27.3, 0.05, "§6")
        fewer = sorted(-100 * x for x in e2e_env["matched_precision_defects_vs_risk_first"])
        check_range("Joint rule against risk-first at equal budget and precision (% fewer defects)", fewer, 19, 67, 0.5, "Summary, §6")
        fewer_than_sequential = sorted(-100 * x for x in e2e_env["sequential_precision_defects_vs_sequential"])
        check_range("Joint rule against the sequential plan at that plan's precision (% fewer defects)", fewer_than_sequential, 12.4, 69.3, 0.05, "§6")
        check_true("The rule measures better than uniform sampling everywhere in the envelope", env["residual_cost_variance_change"][1] < 0, "§6")
        check_true("Risk-first measures worse than the rule everywhere in the envelope", env["risk_first_over_residual_cost"][0] > 0, "§6")
        check_true("Risk-first against uniform sampling changes sign within the envelope", env["risk_first_variance_change"][0] < 0 < env["risk_first_variance_change"][1], "§6")

    total = sum(len(r) for _, r in sections)
    failed = sum(1 for _, r in sections for row in r if not row[4])

    def fmt(x):
        if x is None:
            return ""
        if isinstance(x, float):
            return f"{x:.4f}" if abs(x) < 1000 else f"{x:,.1f}"
        return str(x)

    def art(x):
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            return str(x)
        return format(x, ",.10g")

    lines = [
        "# Results",
        "",
        "Every figure in the article, recomputed from the reference batch of Section 6.",
        "",
        f"{total - failed} of {total} figures agree with the article · {reps:,} draws of the audit lottery per policy · seed {args.seed}"
        + (" · quick run, envelope skipped" if args.quick else ""),
    ]
    for title, section_rows in sections:
        lines += ["", f"## {title}", "", "| Quantity | Recomputed | Article | Where | Agrees |", "| --- | ---: | ---: | --- | :---: |"]
        for label, value, article, where, ok in section_rows:
            lines.append(f"| {label.replace(chr(124), chr(92) + chr(124))} | {fmt(value)} | {art(article)} | {where} | {'✓' if ok else '✗'} |")
    report = "\n".join(lines) + "\n"
    (HERE / "results.md").write_text(report, encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print(report)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
