#!/usr/bin/env python3
"""Exact retained-baseline REPORT corner and source, without an Info valuation.

Scope: the owned scalar-effect, independent-call target at fixed SAM/SITE.
No within-call READY/REPORT independence is assumed in the 256-outcome sum.
This does not execute native words, compute full heat, or identify physical Info.
Every check raises explicitly, so python -O cannot disable verification.
"""

import json
from itertools import product

import sympy as sp


CHECKS = []


def require(condition, label):
    if not bool(condition):
        raise RuntimeError("FAILED: " + label)
    CHECKS.append(label)


def zero(expression, label):
    require(sp.expand(expression) == 0, label)


def simplify_zero(expression, label):
    require(sp.simplify(expression) == 0, label)


lam, a, P0, beta = sp.symbols("lambda a P0 beta", real=True)
yp, ym, Pf, xp, xm, Pq = sp.symbols("Py_plus Py_minus Pf Px_plus Px_minus Pq", real=True)
other_probabilities = (yp, ym, Pf, xp, xm, Pq)
joint = {
    (0, 0): 1 - a - beta + P0,
    (0, 1): beta - P0,
    (1, 0): a - P0,
    (1, 1): P0,
}
zero(sum(joint.values()) - 1, "baseline four-cell normalization")
zero(sum(v for (aa, rr), v in joint.items() if aa) - a, "baseline READY marginal")
zero(sum(v for (aa, rr), v in joint.items() if rr) - beta, "baseline raw REPORT marginal")
zero(joint[(1, 1)] - P0, "baseline composite probability")

old = sp.Integer(0)
kept = sp.Integer(0)
dropped = sp.Integer(0)
count = 0
selector_counts = set()
for bits in product((0, 1), repeat=6):
    weight = sp.prod(pp if bit else 1 - pp for bit, pp in zip(bits, other_probabilities))
    byp, bym, bf, bxp, bxm, bq = bits
    for (aa, rr), mass in joint.items():
        baseline_composite = aa * rr
        n = 4 + (byp - bym) * (bf - baseline_composite) + (bxp - bxm) * (bq - baseline_composite)
        selector_counts.add(n)
        corner = 1 - 2 * lam * n
        old += weight * mass * corner
        kept += weight * mass * corner * (1 - rr)
        dropped += weight * mass * corner * rr
        count += 1
require(count == 256, "all 256 fine outcomes enumerated")
require(min(selector_counts) == 2 and max(selector_counts) == 6, "actual conditional selector count lies in [2,6]")

Dy, Dx = yp - ym, xp - xm
F = Dy * Pf + Dx * Pq
D = 1 - 2 * lam * (4 + F)
expected_kept = (1 - beta) * D
expected_old = D + 2 * lam * P0 * (Dy + Dx)
expected_dropped = beta * D + 2 * lam * P0 * (Dy + Dx)
zero(kept - expected_kept, "kept corner exact fine-outcome sum")
zero(old - expected_old, "original corner exact fine-outcome sum")
zero(dropped - expected_dropped, "dropped corner exact fine-outcome sum")
zero(old - kept - dropped, "kept and dropped sum to original corner")
for variable in (lam, a, P0, beta, *other_probabilities):
    zero(sp.diff(kept, variable) - sp.diff(expected_kept, variable), "complete coordinate derivative: " + str(variable))

# General joint law: eta is the ACTUAL failure-branch conditional marginal,
# not an assertion that an independent new control exists.
r, eta = sp.symbols("r eta", real=True)
beta_parameterized = a * r + (1 - a) * eta
parameterized = {P0: a * r, beta: beta_parameterized}
factorized_cells = {
    (0, 0): (1 - a) * (1 - eta),
    (0, 1): (1 - a) * eta,
    (1, 0): a * (1 - r),
    (1, 1): a * r,
}
for outcome in joint:
    zero(joint[outcome].subs(parameterized, simultaneous=True) - factorized_cells[outcome], "positive joint parameterization: " + str(outcome))
zero(beta_parameterized - a * r - (1 - a) * eta, "beta lower bound remainder is nonnegative on [0,1]")
zero(1 - a + a * r - beta_parameterized - (1 - a) * (1 - eta), "beta upper bound remainder is nonnegative on [0,1]")
zero(1 - beta_parameterized - a * (1 - r) - (1 - a) * (1 - eta), "strict retained mass lower bound a(1-r)")
zero(a * r - a * beta_parameterized - a * (1 - a) * (r - eta), "READY/REPORT covariance and independence criterion")
zero(sp.diff(beta_parameterized, a) - (r - eta), "beta readiness derivative")
zero(sp.diff(beta_parameterized, r) - a, "beta successful-report derivative")
zero(sp.diff(beta_parameterized, eta) - (1 - a), "beta failure-report derivative")

p_upper = sp.Rational(5, 8)
c_min_bound = 1 - 16 * p_upper**7
require(c_min_bound == sp.Rational(52947, 131072), "inherited conservative cold margin exact rational")
require(c_min_bound > 0, "positive conservative cold margin")
require(1 - 12 * p_upper**7 > c_min_bound, "actual selector count also obeys inherited conservative margin")

# Independent probability rows; these precede composition with a real writer.
zero(sp.diff(expected_kept, beta) + D, "raw REPORT marginal source is minus D")
zero(sp.diff(expected_kept, P0), "baseline composite row absent at fixed raw marginal")
zero(sp.diff(expected_kept, a), "baseline READY row absent at fixed raw marginal")
zero(sp.diff(expected_kept, yp) + 2 * lam * (1 - beta) * Pf, "positive y-reference row")
zero(sp.diff(expected_kept, ym) - 2 * lam * (1 - beta) * Pf, "negative y-reference row")
zero(sp.diff(expected_kept, xp) + 2 * lam * (1 - beta) * Pq, "positive x-reference row")
zero(sp.diff(expected_kept, xm) - 2 * lam * (1 - beta) * Pq, "negative x-reference row")
zero(sp.diff(expected_kept, lam) + 2 * (1 - beta) * (4 + F), "visibility row retained")
matched_current = {Pf: P0, Pq: P0}
for variable in (yp, ym, xp, xm):
    zero(sp.diff(expected_old, variable).subs(matched_current), "old null reference cancellation: " + str(variable))

alpha, eps, rf, rq, rho, Delta, df, dq = sp.symbols("alpha epsilon rf rq rho Delta df dq", nonzero=True, real=True)
field_source = (sp.diff(expected_kept, Pf) * alpha * eps * rf * df / rho
                - sp.diff(expected_kept, Pq) * alpha * eps * rq * dq / rho)
field_source = field_source.subs({yp: ym + Delta, xp: xm + Delta}, simultaneous=True)
expected_field = -2 * lam * (1 - beta) * Delta * alpha * eps * (rf * df - rq * dq) / rho
zero(field_source - expected_field, "fixed-beta field source with original df-minus-k0-dq direction")
old_field = -2 * lam * Delta * alpha * eps * (rf * df - rq * dq) / rho
zero(field_source - (1 - beta) * old_field, "retained source is one-minus-beta times original field source")
zero(sp.diff(field_source, dq) * rf + sp.diff(field_source, df) * rq, "material-to-geometric coefficient ratio is minus rq/rf")

# Check the ratio against the ORIGINAL reporter polynomial, not a fitted law.
x, y = sp.symbols("x y", real=True)
p = (sp.sqrt(5) - 1) / 2
z = sp.Rational(1, 2**20)
EE = p**2 * (1 + x)
ell = 4 * EE * (1 - EE)
u = p + p**2 * y
BB = 4 * u**2 * (1 - u**2)
AA = ell + (1 - ell) * BB
reporter = z * (AA + BB) - z**2 * AA * BB
Q = 1 - z * 4 * p**3
RR = 1 - z * 4 * p**3 * (1 + p**6)
rf_original = 4 * z * p**11 * Q
rq_original = 8 * z * p**6 * (RR + p**6 * Q)
simplify_zero(sp.diff(reporter, x).subs({x: 0, y: 0}) - rf_original, "original reporter exact rf")
simplify_zero(sp.diff(reporter, y).subs({x: 0, y: 0}) - rq_original, "original reporter exact rq")
simplify_zero(rq_original / rf_original - 2 * p**(-5) * (RR / Q + p**6), "original exact material ratio retained")

r0, Delta_r = sp.symbols("r0 Delta_r", real=True)
independent_ready_null = (1 - r0) * (1 - 2 * lam * (4 + 2 * alpha**2 * Delta_r * r0))
zero(sp.diff(independent_ready_null, alpha) + 8 * lam * (1 - r0) * alpha * Delta_r * r0, "new common-READY row with independent raw REPORT")
zero(sp.diff(independent_ready_null, Delta_r) + 4 * lam * (1 - r0) * alpha**2 * r0, "new linked reference-contrast row")
zero(sp.diff(1 - 8 * lam, alpha), "old matched null common-READY row vanishes")

# Hostile control: same a, P0 and all seven coarse effects; different actual
# failure REPORT law. It changes the kept corner while old corner is identical.
fixed = {lam: sp.Rational(1, 100), a: sp.Rational(1, 2), P0: sp.Rational(1, 8),
         yp: sp.Rational(1, 5), ym: sp.Rational(1, 10),
         xp: sp.Rational(1, 5), xm: sp.Rational(1, 10),
         Pf: sp.Rational(1, 8), Pq: sp.Rational(1, 8)}
beta_correlated = sp.Rational(1, 8)  # eta=0, r=1/4
beta_independent = sp.Rational(1, 4)  # eta=r=1/4
for bb in (beta_correlated, beta_independent):
    masses = [sp.simplify(value.subs({**fixed, beta: bb})) for value in joint.values()]
    require(all(mass >= 0 for mass in masses) and sum(masses) == 1, "hostile control has a valid four-outcome law, beta=" + str(bb))
old_A = sp.simplify(expected_old.subs({**fixed, beta: beta_correlated}))
old_B = sp.simplify(expected_old.subs({**fixed, beta: beta_independent}))
keep_A = sp.simplify(expected_kept.subs({**fixed, beta: beta_correlated}))
keep_B = sp.simplify(expected_kept.subs({**fixed, beta: beta_independent}))
require(old_A == old_B, "hostile control preserves original corner")
require(keep_A - keep_B == sp.Rational(1839, 16000) > 0, "hostile control changes retained corner by exact nonzero amount")
require(fixed[P0] - fixed[a] * beta_correlated == sp.Rational(1, 16), "hostile control is genuinely READY/REPORT-correlated")

print(json.dumps({
    "status": "PASS",
    "input_commit": "6164fe50b875a4876f8c17eb22d814cdc7937377",
    "checks": len(CHECKS),
    "check_labels": CHECKS,
    "fine_outcomes": count,
    "selector_count_range": [min(selector_counts), max(selector_counts)],
    "formulas": {
        "D": "1-2*lambda*(4+Delta_y*P_f+Delta_x*P_q)",
        "C_keep": "(1-beta)*D",
        "C_old": "D+2*lambda*P0*(Delta_y+Delta_x)",
        "C_drop": "beta*D+2*lambda*P0*(Delta_y+Delta_x)",
        "beta": "a0*r0+(1-a0)*eta",
        "retained_mass_lower_bound": "1-beta >= a0*(1-r0) > 0 for a0>0 and r0<1",
        "field_source_fixed_beta": "-2*lambda*(1-beta)*Delta*alpha*epsilon*(rf*df-rq*dq)/rho",
        "common_READY_row_independent_case": "-8*lambda*(1-r0)*alpha*Delta_r*r0",
    },
    "counterexample": {
        "a0": "1/2", "P0": "1/8", "r0": "1/4",
        "beta_correlated": str(beta_correlated), "beta_independent": str(beta_independent),
        "common_original_corner": str(old_A),
        "retained_correlated_corner": str(keep_A), "retained_independent_corner": str(keep_B),
        "retained_difference": str(keep_A - keep_B), "correlated_covariance": "1/16",
    },
    "assumptions": [
        "Fixed SAM/SITE; separately regenerated calls are conditionally independent.",
        "Original fixed comparator and fixed report marker, at the matched target.",
        "Protected DATA/oldRIGHT is an identity factor in this target.",
        "Probability derivatives must be composed with the ACTUAL writer and admitted control map.",
        "No within-call READY/REPORT independence is used in the general result.",
        "SITE/SAM averaging and their derivatives remain outside this pointwise scalar calculation.",
    ],
    "not_claimed": ["native_word_execution", "full_heat_price", "selected_physical_Info", "joint_stationarity", "GR_closure"],
    "GR_closed": False,
}, indent=2, sort_keys=True))
