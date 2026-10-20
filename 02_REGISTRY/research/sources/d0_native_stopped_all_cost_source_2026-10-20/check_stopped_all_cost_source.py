#!/usr/bin/env python3
"""Bounded exact controls for the all-cost stopped Golden source theorem.

Standard library only. Every check remains active under python -O.
The theorem allows every fixed real T>=5 and rotation price ell>=1.
The unbounded-k, irrationality, and minimum-existence arguments are analytic
in STOPPED_ALL_COST_SOURCE.md; finite controls below do not replace them.
The finite-window part is independently replayed with rational bounds.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


CHECKS = 0


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


# Exact Q[p], p^2 + p - 1 = 0; coefficients are (constant, p).
ZERO, ONE, P = (Q(0), Q(0)), (Q(1), Q(0)), (Q(0), Q(1))


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def scale(a, r):
    return a[0] * r, a[1] * r


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    return a[0] * b[0] + a[1] * b[1], a[0] * b[1] + a[1] * b[0] - a[1] * b[1]


def power(a, k):
    out = ONE
    for _ in range(k):
        out = mul(out, a)
    return out


def conj(a):
    return a[0] - a[1], -a[1]


def norm(a):
    return a[0] ** 2 - a[0] * a[1] - a[1] ** 2


def divide(a, b):
    n = norm(b)
    require(n != 0, "Division by a nonzero Golden field element")
    return scale(mul(a, conj(b)), 1 / n)


def sign(a):
    # 2(a0+a1*p) = u+v*sqrt(5); compare rational squares exactly.
    u, v = 2 * a[0] - a[1], a[1]
    if v == 0:
        return (u > 0) - (u < 0)
    if u == 0 or u * v > 0:
        return (v > 0) - (v < 0)
    d = u * u - 5 * v * v
    require(d != 0, "sqrt(5) is irrational for nonzero rational u,v")
    return ((u > 0) - (u < 0)) if d > 0 else ((v > 0) - (v < 0))


# Rational interval operations, used only with proved positive divisors.
def iadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def imul(a, b):
    vals = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(vals), max(vals)


def idiv(a, b):
    require(b[0] > 0, "Positive interval divisor")
    return imul(a, (1 / b[1], 1 / b[0]))


def log_bounds(x, n):
    """ln(x), x>1: positive atanh series with rigorous rational tail."""
    require(x > 1 and n > 0, "Logarithm enclosure domain")
    z = (x - 1) / (x + 1)
    zpow, partial = z, Q(0)
    for j in range(n):
        partial += 2 * zpow / (2 * j + 1)
        zpow *= z * z
    tail = 2 * zpow / ((2 * n + 1) * (1 - z * z))
    return partial, partial + tail


PINNED = {
    "upstream_check_stopped_source_minimum.py": "e022977c672f9c64c9c3ee27d652b009508a2b584b46232ec88c270ff61bbe70",
    "corrected_check_stopped_source_minimum.py": "e6f20aa5c9850635165cdaff08f7c4799cdd441aced84be2d64739ac771f901f",
    "upstream_stopped_proof.md": "1e2815efc4daab717a7b84069607e287330360093d5a6eaedcfb55c080f9681a",
    "upstream_reviewed_stopped_proof.md": "ea2016810eb5b7bbc3e41941faf66900d7c0c0b4d97c064f098275102aafc34e",
    "UPSTREAM_TARGET_CORRECTION.patch": "c08c7806059a61e3cab0372d236882317c7ffe838d9eaf3eaaaf9f9b83257026",
}


def run():
    here = Path(__file__).resolve().parent
    for name, digest in PINNED.items():
        require(sha256((here / name).read_bytes()).hexdigest() == digest, "Frozen input: " + name)
    upstream = (here / "upstream_check_stopped_source_minimum.py").read_bytes()
    corrected = (here / "corrected_check_stopped_source_minimum.py").read_bytes()
    old = b'target=-D(2)/(pp**D("1.5"))'
    new = b'target=-D(1)/(pp**D("1.5"))'
    require(upstream.count(old) == 1, "Unique historical target defect")
    require(corrected == upstream.replace(old, new), "Only target factor corrected; no weakened check")
    reproduction = json.loads((here / "UPSTREAM_REPRODUCTION.json").read_text())
    for label, exit_code in (("upstream", 1), ("corrected", 0)):
        row = reproduction["runs"][label]
        require(row["exit_code"] == exit_code, "Historical normal-Python outcome: " + label)
        require(sha256((here / row["log_file"]).read_bytes()).hexdigest() == row["log_sha256"], "Reproduction log hash: " + label)

    phi = add(ONE, P)
    x = sub(scale(P, 2), ONE)
    require(add(power(P, 2), P) == ONE, "Golden equation")
    require(mul(P, phi) == ONE, "p = phi^(-1)")
    require(conj(x) == scale(power(phi, 3), -1), "Chebyshev conjugate x' = -phi^3")
    cosh5 = scale(add(power(phi, 5), power(P, 5)), Q(1, 2))
    eta_gap = sub(cosh5, power(phi, 3))
    require(eta_gap == (Q(-1, 2), Q(3)), "cosh(5 ln phi)-phi^3=(3 sqrt(5)-4)/2")
    require(sign(eta_gap) > 0, "eta < 5 ln phi, by strict monotonicity of cosh")

    # A_k = cos^2(k theta) belongs to Z[p] by this integral recurrence.
    # C_k = T_k(x) supplies an independent recurrence check of 2 A_k - 1.
    A, C = [ONE, P], [ONE, x]
    for k in range(1, 24):
        A.append(add(sub(mul(scale(x, 2), A[-1]), A[-2]), sub(ONE, x)))
        C.append(sub(mul(scale(x, 2), C[-1]), C[-2]))
    for k in range(1, 25):
        require(all(v.denominator == 1 for v in A[k]), "Integral A recurrence at k=" + str(k))
        require(sub(scale(A[k], 2), ONE) == C[k], "Chebyshev A identity at k=" + str(k))
        require(norm(A[k]).denominator == 1 and norm(A[k]) != 0, "Nonzero integer norm control at k=" + str(k))
        require(mul(A[k], conj(A[k])) == (norm(A[k]), Q(0)), "Norm product control at k=" + str(k))
        require(sign(A[k]) > 0 and sign(sub(ONE, A[k])) > 0, "Nondegenerate trigonometric control at k=" + str(k))
        require(sign(sub(A[k], power(P, 5 * k))) > 0, "Algebraic separation control at k=" + str(k))
    require(norm(A[1]) == -1 and sign(conj(A[1])) < 0, "Negative control: absolute norm is essential")

    q = [sub(ONE, a) for a in A]
    require(q[1] == power(P, 2), "q1=p^2")
    require(q[2] == scale(power(P, 3), 4), "q2=4p^3")
    require(A[2] == power(P, 6), "1-q2=p^6")
    require(sign(sub(P, (Q(8, 13), Q(0)))) > 0, "p>8/13")
    require(sign(sub(q[2], (Q(12, 13), Q(0)))) > 0, "q2>12/13")
    r1, r2 = divide(ONE, q[1]), divide(scale(ONE, 2), q[2])
    require(sub(r1, r2) == scale(ONE, Q(1, 2)), "R1-R2=1/2 for Rk=k/qk")
    require(sign(sub(scale(ONE, 3), r2)) > 0, "R2<3; every k>=3 has Rk>k>=3")

    # Independent ACTIVE replay of the entire finite-window proof.
    plo, phi_upper = Q("0.61803398874989"), Q("0.61803398874990")
    require((2 * plo + 1) ** 2 < 5 < (2 * phi_upper + 1) ** 2, "Certified Golden enclosure")

    def interval(a):
        vals = (a[0] + a[1] * plo, a[0] + a[1] * phi_upper)
        return min(vals), max(vals)

    lp = (log_bounds(1 / phi_upper, 35)[0], log_bounds(1 / plo, 35)[1])
    l4phi = idiv(log_bounds(Q(4), 75), lp)
    require(l4phi[0] > 1, "Positive log_phi(4)-1 in the D2 enclosure")
    r3, r6 = (plo ** 3, phi_upper ** 3), (plo ** 6, phi_upper ** 6)
    d2lo = 4 * r3[0] * (l4phi[0] - 1) - 5 * r6[1]
    d2hi = 4 * r3[1] * (l4phi[1] - 1) - 5 * r6[0]
    require(Q(1497, 1000) < d2lo < d2hi < Q(1498, 1000), "Certified 1.497<D2<1.498")
    q2lo = 4 * r3[0]
    require((7 + d2hi) / q2lo < 9, "S2(5)<9")
    require((52 + d2hi) / q2lo < 57, "S2(50)<57; excludes every k>=7 on [5,50]")
    for k in (1, 3, 4, 5, 6):
        qi = interval(q[k])
        require(0 < qi[0] <= qi[1] < q2lo, "Positive comparison slope at k=" + str(k))
        require((5 + k) / qi[1] > 9, "Strict T=5 competitor gap at k=" + str(k))

    # D(q)<=max(D(0),D(1))=2 by convexity, strictly inside (0,1).
    # For any ell>=1 minimizer, S_k(T,1)<=S_2(T,1) since Rk>=R2.
    # This is a sublevel conclusion, not minimization of the ell=1 score.
    # Thus k < S_2(T,1)-T < (T+4)/(12/13)-T = T/12+13/3.
    candidate_slope = Q(13, 12) - 1
    candidate_intercept = Q(13, 12) * 4
    require(candidate_slope == Q(1, 12) and candidate_intercept == Q(13, 3), "All-T finite candidate affine bound")
    source_slope = 1 - 4 * candidate_slope
    source_intercept = 1 - 4 * candidate_intercept
    require(source_slope == Q(2, 3) and source_intercept == Q(-49, 3), "Bk>(2T-49)/3 tail bound")
    require(source_slope > 0 and source_slope * 50 + source_intercept == 17, "T>=50 implies Bk>17")
    require(5 - 3 == 2, "T in [5,50], k2: B2=T-3>=2")

    # q D'(q)-D(q)=-log_phi((1-q)/p), checked as formal log coefficients.
    D_coeff = {"log_q": (0, 1), "log_1mq": (1, -1), "log_p": (-1, -1)}
    qDp_coeff = {"log_q": (0, 1), "log_1mq": (0, -1), "log_p": (0, -1)}
    difference = {key: tuple(qDp_coeff[key][j] - D_coeff[key][j] for j in (0, 1)) for key in D_coeff}
    require(difference == {"log_q": (0, 0), "log_1mq": (-1, 0), "log_p": (1, 0)}, "Exact stopped derivative log identity")
    # q2'=8 p^4 sqrt(p), so q2'/q2^2=1/(2p^(3/2)).
    qp2_sqrtp_coefficient = scale(power(P, 4), 8)
    require(mul(qp2_sqrtp_coefficient, scale(power(P, 2), 2)) == power(q[2], 2), "Exact q2'/q2^2 factor 1/(2p^(3/2))")
    normalized_source = mul(divide(scale(qp2_sqrtp_coefficient, -2), power(q[2], 2)), power(P, 2))
    require(normalized_source == scale(ONE, -1), "At T=5, source times p^(3/2) is exactly -1")
    require(normalized_source != scale(ONE, -2), "Historical factor-2 target is rejected")
    require(3 + 2 - 5 == 0, "Hostile control: T=3 cancels the k2 source")

    return {
        "schema": 1,
        "status": "PASS",
        "active_exact_checks": CHECKS,
        "arithmetic": "fractions.Fraction; exact Q[p]; certified rational logarithm bounds; no floating point",
        "input_commit": "f22c1864bd85e097166abd75dc048164d8d63c65",
        "reviewed_work_entropy_input_commit": "1cb164de3753f9dbaf214ea140eb9ea21a7b9d90",
        "input_sha256": PINNED,
        "finite_window": {"T_closed_interval": [5, 50], "rotation_price_domain": "every real ell>=1", "unique_minimizer": 2, "D2_strict_interval": ["1497/1000", "1498/1000"]},
        "all_cost_theorem": {"T_domain": "every real T>=5, fixed during field variation", "rotation_price_domain": "every real ell>=1, fixed during field variation", "rotation_price_comparison": "Rk=k/qk has unique minimum k=2; R1-R2=1/2 and Rk>3>R2 for k>=3", "selected_unit_price_sublevel": "S_k(T,1)<=S_2(T,1); k need not minimize the unit-price score", "minimizer_exists": True, "each_minimizer_candidate_bound": "k<T/12+13/3", "each_minimizer_B_lower_bound": "B_k(T,ell)>=2", "tail_T_ge_50_bound": "B_k(T,ell)>(2T-49)/3>=17", "branch_source_coefficient": "-B_k*q_k_prime/q_k^2 is nonzero", "true_local_minimum_necessary_condition": "DJ2=0 if fixed-k scores are admissible near the background across the full two-sided allowed field space and Dt=gamma_h DJ2, gamma_h>0"},
        "upstream_control": {"original_normal_run": "FAILED at factor-2 target", "corrected_normal_run": "PASS with target -1 only", "T5_source_times_p_to_3_over_2": "-1", "wrong_target_rejected": "-2", "T3_source_cancels": True},
        "analytic_proof_scope": "Unbounded-k algebraic norm/separation, irrationality/nondegeneracy, convex KL bound, existence of discrete minimum and local-minimum implication are proved analytically in STOPPED_ALL_COST_SOURCE.md. Finite k=1..24 controls do not stand in for these proofs.",
        "actual_score_scope": "S_actual=S_scalar_ports-E_k with E_k>=0, E_k=DE_k=0 on Sigma and E_k=O(t^4*abs(log(abs(t)))); the full-work bound is reused from the pinned reviewed upstream proof, not retested here. With oldRIGHT in Info, use the corresponding conditional classical-work entropy and fixed oldRIGHT baseline.",
        "remaining_assumptions": ["Declared actual first-port1 stopping task", "Whole-pointer Shannon Info with the original 0/10 code", "Fixed per-G price ell>=1 and fixed per-attempt T>=5", "All additional moving physical cost/Info sources retained separately", "Admissibility near y0 across all claimed field directions"],
        "not_claimed": ["D0 forces this task or this Info cut", "Differentiability of the optimized envelope at ties", "Every Clarke stationary point satisfies DJ2=0", "DJ2=0 is sufficient for a local minimum", "Existence of a physical local minimum"],
        "full_D0_price_selected": False,
        "GR_closed": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
