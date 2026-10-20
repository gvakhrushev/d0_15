#!/usr/bin/env python3
"""Read-only finite checks of the new complete-price composition.

All probabilities and paid-cost sums are rational. Entropies/KL use
ordinary floating logarithms with the declared fixed absolute tolerance.
These finite fixtures validate the exact finite-ledger algebra; they are
not substituted for the actual native Golden compiler's leaf law, its
Info choice, or physical admission. Running this script only prints JSON.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path


PHI = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI = math.log(PHI)
ATOL = 2.0e-11
ERRORS: list[float] = []

PREP = {
    "ready_a": F(1, 5),
    "ready_b": F(3, 5),
    "abort_a": F(1, 10),
    "abort_b": F(1, 10),
}
STAGE = {
    "ready_plus": F(3, 10),
    "ready_minus": F(3, 10),
    "abort_early": F(2, 15),
    "abort_late": F(4, 15),
}
PREP_COST = {"ready_a": 2, "ready_b": 5, "abort_a": 3, "abort_b": 4}
STAGE_COST = {
    "ready_plus": 11,
    "ready_minus": 13,
    "abort_early": 4,
    "abort_late": 8,
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def close(actual: float, expected: float, label: str) -> None:
    error = abs(actual - expected)
    ERRORS.append(error)
    require(math.isfinite(actual) and math.isfinite(expected), label + ": nonfinite")
    require(error <= ATOL, f"{label}: error {error!r} exceeds {ATOL!r}")


def log_phi(value: F | float) -> float:
    return math.log(float(value)) / LN_PHI


def entropy(law: dict) -> float:
    return math.fsum(-float(p) * log_phi(p) for p in law.values() if p)


def binary_entropy(p: F) -> float:
    return entropy({0: p, 1: 1 - p})


def ready(label: str) -> bool:
    return label.startswith("ready_")


ALPHA = sum((p for t, p in PREP.items() if ready(t)), F(0))
BETA = sum((p for t, p in STAGE.items() if ready(t)), F(0))
MU_PRE = sum((p * PREP_COST[t] for t, p in PREP.items()), F(0))
MU = sum((p * STAGE_COST[t] for t, p in STAGE.items()), F(0))
H_PRE = entropy(PREP)
H_T = entropy(STAGE)
ZETA_PRE = H_PRE - binary_entropy(ALPHA)
ZETA = H_T - binary_entropy(BETA)


def renewal(n: int, x: F) -> F:
    return sum((x**k for k in range(n)), F(0))


def fine_law(n: int, q: F) -> dict:
    """Each leaf retains bank, every attempted-stage transcript and report.

    Stage abort/no-click stops; click continues until the finite cap.
    Aborts and every retained failure are genuine leaves, not conditioned
    away. The cap is determined by the complete chronological leaf.
    """
    leaves: dict = defaultdict(F)

    def run(pre: str, steps: tuple, probability: F) -> None:
        for tag, weight in STAGE.items():
            if not ready(tag):
                leaves[(pre, steps + ((tag, "ABORT"),))] += probability * weight
                continue
            for report, report_probability in (("CLICK", q), ("NO_CLICK", 1 - q)):
                next_steps = steps + ((tag, report),)
                next_probability = probability * weight * report_probability
                if report == "CLICK" and len(next_steps) < n:
                    run(pre, next_steps, next_probability)
                else:
                    leaves[(pre, next_steps)] += next_probability

    for pre, probability in PREP.items():
        if ready(pre):
            run(pre, (), probability)
        else:
            leaves[(pre, ())] += probability
    return dict(leaves)


def coarse_key(leaf: tuple) -> tuple:
    pre, steps = leaf
    return (
        "READY" if ready(pre) else "ABORT",
        tuple(("READY" if ready(tag) else "ABORT", report) for tag, report in steps),
    )


def coarse_law(law: dict) -> dict:
    coarse: dict = defaultdict(F)
    for leaf, probability in law.items():
        coarse[coarse_key(leaf)] += probability
    return dict(coarse)


def mean_cost(law: dict) -> F:
    return sum(
        (
            probability * (PREP_COST[pre] + sum(STAGE_COST[tag] for tag, _ in steps))
            for (pre, steps), probability in law.items()
        ),
        F(0),
    )


def mean_stage_count(law: dict) -> F:
    return sum((p * len(leaf[1]) for leaf, p in law.items()), F(0))


def kl(p: dict, q: dict) -> float:
    require(p.keys() == q.keys(), "KL fixtures require identical positive support")
    return math.fsum(float(value) * log_phi(value / q[key]) for key, value in p.items())


def book_prices(law: dict, theta: F, anchor: F) -> dict:
    return {leaf: -float(theta) * log_phi(p) - float(anchor) for leaf, p in law.items()}


def expectation(law: dict, observable: dict) -> float:
    return math.fsum(float(p) * observable[leaf] for leaf, p in law.items())


def paired_path_mean(p: dict, q: dict, theta: F, jp: F, jq: F) -> float:
    sp, sq = book_prices(p, theta, jp), book_prices(q, theta, jq)
    return math.fsum(float(value) * (sp[key] - sq[key]) for key, value in p.items())


def main() -> None:
    require(sum(PREP.values(), F(0)) == 1, "bank law normalized exactly")
    require(sum(STAGE.values(), F(0)) == 1, "stage law normalized exactly")
    require(ZETA > float(BETA) * log_phi(2), "fixture retains a fair ready sign and abort refinement")
    caps, qs = (2, 3), (F(1, 5), F(3, 7), F(2, 3))
    laws = {(n, q): fine_law(n, q) for n in caps for q in qs}
    coarse = {key: coarse_law(law) for key, law in laws.items()}
    sizes = {}

    for (n, q), law in laws.items():
        require(sum(law.values(), F(0)) == 1, "all fine leaves normalized exactly")
        require(all(p > 0 for p in law.values()), "positive finite support")
        coarse_here = coarse[(n, q)]
        require(sum(coarse_here.values(), F(0)) == 1, "coarse law normalized exactly")
        e = renewal(n, BETA * q)
        expected_h = H_PRE + float(ALPHA * e) * (H_T + float(BETA) * binary_entropy(q))
        expected_coarse = binary_entropy(ALPHA) + float(ALPHA * e) * (
            binary_entropy(BETA) + float(BETA) * binary_entropy(q)
        )
        close(entropy(law), expected_h, "complete finite chronological entropy")
        close(entropy(coarse_here), expected_coarse, "coarse chronological entropy")
        close(entropy(law) - entropy(coarse_here), ZETA_PRE + float(ALPHA * e) * ZETA,
              "fine/coarse conditional entropy occupation")
        require(mean_stage_count(law) == ALPHA * e, "retained stage occupation exact")
        require(mean_cost(law) == MU_PRE + ALPHA * MU * e, "complete all-launch paid cost exact")
        sizes[str(n)] = {"fine_leaves": len(law), "coarse_leaves": len(coarse_here)}

    q_a, q_b, q_c = qs
    ja, jb, jc = F(2, 7), F(-1, 9), F(3, 11)
    kl_values, mean_path_gaps = {}, {}
    for n in caps:
        pa, pb, pc = (laws[(n, q)] for q in qs)
        ca, cb = coarse[(n, q_a)], coarse[(n, q_b)]
        require(mean_stage_count(pa) != mean_stage_count(pb), "variable stopping is actually exercised")
        for leaf in pa:
            c = coarse_key(leaf)
            require(pa[leaf] / ca[c] == pb[leaf] / cb[c], "shared refinement kernel exact")
        close(kl(pa, pb), kl(ca, cb), "conditional KL cancellation under variable stopping")
        kl_values[str(n)] = kl(pa, pb)
        for theta in (F(1, 2), F(1)):
            sa, sb, sc = (book_prices(p, theta, j) for p, j in ((pa, ja), (pb, jb), (pc, jc)))
            ma, mb, mc = (expectation(p, s) for p, s in ((pa, sa), (pb, sb), (pc, sc)))
            mean_difference = ma - mb
            path_difference = paired_path_mean(pa, pb, theta, ja, jb)
            close(mean_difference, float(theta) * (entropy(pa) - entropy(pb)) - float(ja - jb),
                  "difference of complete Book means")
            close(path_difference, -float(theta) * kl(pa, pb) - float(ja - jb),
                  "active-law mean of paired path prices")
            cross_term = math.fsum(float(pa[key] - pb[key]) * sb[key] for key in pa)
            close(mean_difference - path_difference, cross_term, "sampling-law term retained")
            require(abs(cross_term) > 1.0e-3, "mean difference is detectably not paired path mean")
            close((ma - mb) + (mb - mc), ma - mc, "scalar mean difference is a cocycle")
            forward_reverse = path_difference + paired_path_mean(pb, pa, theta, jb, ja)
            close(forward_reverse, -float(theta) * (kl(pa, pb) + kl(pb, pa)),
                  "paired expected log ratio is not an antisymmetric cocycle")
            require(forward_reverse < -1.0e-3, "KL negative control has nonzero defect")
            mean_path_gaps[f"N={n},theta={theta}"] = cross_term

    # Exact N=2 paid/source coefficients; this is not the native leaf law.
    pa, pb = laws[(2, q_a)], laws[(2, q_b)]
    ca, cb = coarse[(2, q_a)], coarse[(2, q_b)]
    refinement_pair = (entropy(pa) - entropy(ca)) - (entropy(pb) - entropy(cb))
    close(refinement_pair, float(ALPHA * BETA * (q_a - q_b)) * ZETA,
          "N=2 occupation-weighted refinement residual")
    require(abs(refinement_pair) > 1.0e-3, "matched reference does not cancel occupied compiler entropy")
    require(mean_cost(pa) - mean_cost(pb) == ALPHA * MU * BETA * (q_a - q_b),
            "N=2 paid compiler occupation residual exact")
    require(mean_cost(pa) != mean_cost(pb), "paid stage repetition is not a common constant")
    kappa = float(MU) - H_T
    internal_price_pair = float(ALPHA * BETA * (q_a - q_b)) * kappa
    require(abs(internal_price_pair) > 1.0e-3, "net internal compiler price survives pairing")

    # The absolute-anchor kernel is a mathematical negative control:
    # normalization alone cannot physically select or admit its shifts.
    fixed_law = laws[(3, q_a)]
    theta, slope = F(1, 2), F(7, 5)
    anchor_means = {}
    for z in (F(-1, 4), F(0), F(1, 4)):
        price = book_prices(fixed_law, theta, slope * z)
        raw = {key: PHI ** (-value / float(theta)) for key, value in price.items()}
        norm = math.fsum(raw.values())
        for key, probability in fixed_law.items():
            close(raw[key] / norm, float(probability), "common anchor shift invisible in normalized laws")
        anchor_means[z] = expectation(fixed_law, price)
    anchor_source = (anchor_means[F(1, 4)] - anchor_means[F(-1, 4)]) / 0.5
    close(anchor_source, -float(slope), "absolute anchor source survives normalization")
    require(abs(anchor_source) > 1.0, "dropping the normalizer fails the source test")

    # C2 source-neutral residual W=R*r^2/2 on the whole plateau r=0.
    # It cannot cure S0=a*s*r+b*r^2/2. All signs below are rational exact.
    a, b = F(2), F(3)
    neutral_cases = []
    for r_curvature in (F(0), F(1), F(1000000)):
        determinant = -(a * a)
        require(determinant < 0, "source-neutral normal curvature leaves indefinite mixed block")
        s = 1 / (4 * (b + r_curvature + 1))
        r = -(s * s)
        total_price = a * s * r + (b + r_curvature) * r * r / 2
        require(total_price < 0, "explicit same-root arbitrarily small descending direction")
        require(F(0) * (b + r_curvature) < a * a, "necessary PSD mixed inequality is violated")
        neutral_cases.append(str(r_curvature))
    p_curvature = F(2)
    require(p_curvature * b - a * a > 0, "root-only-neutral residual can satisfy PSD after altering plateau source")
    require(p_curvature * F(1, 10) != 0, "such a repair is not source-neutral on the whole plateau")

    result = {
        "status": "PASS",
        "scope": "Finite rational interface fixtures of analytic ledger identities; not a native-leaf replay or physical Info admission.",
        "read_only": True,
        "log_base": "phi",
        "fixed_absolute_tolerance": ATOL,
        "maximum_observed_log_identity_error": max(ERRORS),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "groups": [
            {
                "name": "complete_finite_renewal_and_entropy_chain",
                "status": "PASS",
                "caps": list(caps),
                "rational_click_probabilities": [str(q) for q in qs],
                "leaf_inventory": sizes,
                "includes": "bank aborts, stage aborts, no-click, every continued click and cap; exact all-launch cost and occupation",
            },
            {
                "name": "conditional_KL_and_two_paired_expectations",
                "status": "PASS",
                "variable_length_KL": kl_values,
                "mean_minus_path_expectation_gaps": mean_path_gaps,
                "shared_conditional_kernel": "verified exactly as fractions on every fine leaf",
            },
            {
                "name": "occupied_price_and_absolute_normalizer_negative_controls",
                "status": "PASS",
                "N2_paired_refinement_entropy": refinement_pair,
                "N2_paired_internal_net_price": internal_price_pair,
                "same_normalized_law_absolute_price_source": anchor_source,
                "interpretation": "computable residuals; no physical anchor or Info has been selected",
            },
            {
                "name": "source_neutral_full_minimum_negative_control",
                "status": "PASS",
                "normal_curvatures": neutral_cases,
                "mixed_determinant": str(-(a * a)),
                "interpretation": "whole-plateau-neutral C2 residuals cannot repair the mixed block; root-only neutrality is weaker",
            },
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
