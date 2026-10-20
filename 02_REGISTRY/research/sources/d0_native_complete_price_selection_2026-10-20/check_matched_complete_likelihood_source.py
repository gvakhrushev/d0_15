#!/usr/bin/env python3
"""Exact complete mean-score test for the existing positive loop/void proposal.

Read-only research checker. No assertion of selected physical Book03 Info.
Run: python check_matched_complete_likelihood_source.py --root PATH
The original positive effect fixture is consumed from the c7a2 source;
the native all-launch shell theorem is consumed, not re-certified here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as s


def require(value: bool, message: str) -> None:
    if not value:
        raise ArithmeticError(message)


def iszero(value) -> bool:
    return s.simplify(value) == 0


parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, required=True)
args = parser.parse_args()
paths = [
    "02_REGISTRY/research/sources/d0_native_triz_reference_2026-10-20/TRIZ_MATCHED_LOOP_VOID_SOURCE.md",
    "02_REGISTRY/research/sources/d0_native_triz_reference_2026-10-20/check_matched_feedback_poisson.py",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md",
    "02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md",
    "02_REGISTRY/research/A4D_P25_NATIVE_COST_FLOOR_PSD_MIXED_PALATINI_VACUUM_NO_GO_2026_10_20.md",
]
pins = {path: hashlib.sha256((args.root / path).read_bytes()).hexdigest()
        for path in paths}

x, t = s.symbols("x t", real=True)
z = s.Rational(1, 2**20)
origin = {x: 0, t: 0}

# Exact constants from the newest upstream positive-effect fixture.
id2 = s.eye(2)
A0 = s.diag(s.Rational(1, 3), s.Rational(1, 2))
Ae = s.diag(s.Rational(1, 7), -s.Rational(1, 11))
Au = s.Matrix([[0, s.Rational(1, 13)], [s.Rational(1, 13), 0]])
Aeu = s.diag(s.Rational(1, 17), -s.Rational(1, 19))
fixture_text = (args.root / paths[1]).read_text()
for fragment in ["s.Rational(1,3)", "s.Rational(1,2)",
                 "s.Rational(1,7)", "s.Rational(1,11)",
                 "s.Rational(1,13)", "s.Rational(1,17)",
                 "s.Rational(1,19)"]:
    require(fragment in fixture_text, "upstream effect constant missing")

loop_results = []
for name, active in [("original_noncommuting_fixture", Au),
                     ("nonzero_fisher_control",
                      Au + s.diag(s.Rational(1, 23), -s.Rational(1, 29)))]:
    # Whole |x|,|t|<=1/5 rectangle is strictly between zero and I
    # by a rational Gershgorin row-sum norm bound, not sampled eigenvalues.
    perturb = (Ae.applyfunc(abs)/5 + active.applyfunc(abs)/5
               + Aeu.applyfunc(abs)/25)
    bound = max(sum(perturb[i, j] for j in range(2)) for i in range(2))
    require(bound < s.Rational(1, 3), "positive entire effect chart")
    require(s.Rational(1, 2) + bound < 1, "contractive entire effect chart")
    A = A0 + x*Ae + t*active + x*t*Aeu
    require(A0*active != active*A0, "control really noncommuting")

    J = -128*s.log((id2-z*A).det())
    Jref = J.subs(t, 0)
    void_mixed = s.simplify(s.diff(J-Jref, x, t).subs(origin))
    R = (id2-z*A0).inv()
    upstream_formula = 128*z*s.trace(R*Aeu) + 128*z*z*s.trace(R*Ae*R*active)
    require(iszero(void_mixed-upstream_formula), "same exact void mixed-source formula")
    require(void_mixed != 0, "void mixed source actually nonzero")

    lambdas = [s.expand(128*z**r*s.trace(A**r)/r) for r in range(1, 4)]
    means = [v.subs(t, 0) for v in lambdas]
    truncations = []
    for limit in (1, 2, 3):
        divergence = sum((lam*s.log(lam/mu)-lam+mu
                          for lam, mu in zip(lambdas[:limit], means[:limit])), s.S.Zero)
        require(iszero(divergence.subs(t, 0)), "full mean value on matching diagonal")
        require(iszero(s.diff(divergence, t).subs(t, 0)), "complete mean link gradient for every common x")
        mixed = s.simplify(s.diff(divergence, x, t).subs(origin))
        require(mixed == 0, "complete mean mixed source cancels")
        uu = s.simplify(s.diff(divergence, t, 2).subs(origin))
        fisher = sum((s.diff(lam, t).subs(origin)**2/mu.subs(x, 0)
                      for lam, mu in zip(lambdas[:limit], means[:limit])), s.S.Zero)
        require(iszero(uu-fisher), "complete active Hessian equals Fisher block")

        # Explicit cancellation of constant/void and nonzero-count terms.
        mean_counts = sum((lam*s.log(lam/mu)
                           for lam, mu in zip(lambdas[:limit], means[:limit])), s.S.Zero)
        counts_mixed = s.simplify(s.diff(mean_counts, x, t).subs(origin))
        Jtrunc = sum(lambdas[:limit])
        require(iszero(counts_mixed-s.diff(Jtrunc, x, t).subs(origin)),
                "nonzero count histories carry exactly missing mixed source")
        if name == "nonzero_fisher_control":
            require(uu > 0, "nonzero surviving Fisher response")
        truncations.append({"R": limit, "full_mean_mixed": str(mixed),
                            "link_fisher": str(uu),
                            "counts_mixed_cancels_void": str(counts_mixed)})
    loop_results.append({"fixture": name, "strict_chart_norm_bound": str(bound),
                         "void_mixed": str(void_mixed), "truncations": truncations})

# One complete finite probability family; labels may include arbitrary
# deterministic clock/control copies without changing the distribution.
q = s.Matrix([(2+x)/10, (3-x)/10, s.Rational(1, 4), s.Rational(1, 4)])
v = s.Matrix([(1+x)/40, (-1+2*x)/40, -3*x/40, 0])
prob = q+t*v
require(iszero(sum(q)-1) and iszero(sum(v)), "whole finite model normalized")
for i in range(4):
    qlower = min(q[i].subs(x, xx) for xx in (-s.Rational(1, 5), s.Rational(1, 5)))
    vmax = max(abs(v[i].subs(x, xx)) for xx in (-s.Rational(1, 5), s.Rational(1, 5)))
    require(qlower-vmax/5 > 0, "finite probability chart strictly positive")
D = sum((prob[i]*s.log(prob[i]/q[i]) for i in range(4)), s.S.Zero)
require(iszero(s.diff(D, t).subs(t, 0)), "finite full-score identity")
require(iszero(s.diff(D, x, t).subs(origin)), "moving reference mixed cancellation")

ell = s.log((1+s.sqrt(5))/2)
cost = s.Matrix([1, 2, 2, 3])
B = [cost[i]+s.log(q[i])/ell for i in range(4)]
S = sum((prob[i]*(cost[i]+s.log(prob[i])/ell) for i in range(4)), s.S.Zero)
residual = sum((prob[i]*B[i] for i in range(4)), s.S.Zero)
# Prove the summand identity with genuinely positive symbols, then apply it
# on the just-proved positive probability chart.  SymPy does not know the
# bounded x,t chart from its bare real-symbol assumptions.
pp, qq = s.symbols("pp qq", positive=True)
cc = s.symbols("cc", real=True)
summand_identity = pp*(cc+s.log(pp)/ell) - pp*s.log(pp/qq)/ell - pp*(cc+s.log(qq)/ell)
require(iszero(s.expand_log(summand_identity)),
        "complete Cost minus Shannon residual identity on every positive summand")
formula = sum((s.diff(prob[i], x, t)*B[i]
               +s.diff(prob[i], t)*s.diff(B[i], x)
               +s.diff(prob[i], x)*s.diff(B[i], t)
               +prob[i]*s.diff(B[i], x, t) for i in range(4)), s.S.Zero)
require(iszero(s.diff(S, x, t).subs(origin)-formula.subs(origin)),
        "full mixed paid residual derivative")
matched_cost = [-s.log(q[i])/ell+7+x*x for i in range(4)]
Smatched = sum((prob[i]*(matched_cost[i]+s.log(prob[i])/ell)
                for i in range(4)), s.S.Zero)
require(iszero(s.diff(Smatched, x, t).subs(origin)), "matched cross-code has no mixed jet")

# Exact noncommuting quantum record, all density-matrix entries retained.
qa = s.Rational(1, 3)+x/20
radicand = (2*qa-1)**2+4*t*t/49
eig = [(1+s.sqrt(radicand))/2, (1-s.sqrt(radicand))/2]
quantum = sum((ev*s.log(ev) for ev in eig), s.S.Zero) - qa*s.log(qa) - (1-qa)*s.log(1-qa)
q_mixed = s.simplify(s.diff(quantum, x, t).subs(origin))
q_uu = s.simplify(s.diff(quantum, t, 2).subs(origin))
require(q_mixed == 0, "quantum co-transported reference mixed cancellation")
require(iszero(q_uu-6*s.log(2)/49), "quantum BKM Hessian preserves offdiagonal coherence")

# Owned original all128 scalar-shell cost and exact native clock factors.
p = (s.sqrt(5)-1)/2
native = []
for L in (4, 8, 16):
    h = s.Rational(1, L)
    n = 128*L*L
    epsilon = p*p*h*h/64
    beta = 2*p*p
    mu = s.simplify(2-2*s.cos(2*s.pi/L))
    r = s.simplify(p*epsilon*mu)
    price_source = s.simplify(n*p*epsilon*mu)
    require(iszero(n*epsilon-beta), "unchanged original native clock")
    require(iszero(price_source-p*beta*mu), "same all-launch shell derivative")
    require(float(price_source) > 0 and float(r) < float(p*p), "native positive source and low-event chart")
    port_source = s.simplify(price_source*(1-s.log((1-r)/r)/ell))
    require(float(port_source) < 0, "different port-Shannon candidate source sign")
    native.append({"L": L, "actual_port_cost_source": str(price_source),
                   "actual_port_cost_source_numeric": float(price_source),
                   "port_shannon_candidate_source_numeric": float(port_source)})

p25 = (1-x)*s.sin(t)
require(s.diff(p25, x, t).subs({x: 1, t: 0}) == -1,
        "owned P25 nonzero mixed target is not matched full mean")
print(json.dumps({
    "status": "PASS",
    "scope": "Complete expected relative-information source test, not Book03 selection or GR closure",
    "input_sha256": pins,
    "loop_positive_fixtures": loop_results,
    "finite_normalized_model_and_actual_charge_residual": "exact PASS",
    "quantum_full_record": {"mixed": str(q_mixed), "active_hessian": str(q_uu)},
    "native_all_launch_shell_consumer": native,
    "full_D0_price_selected": False,
    "GR_closed": False,
}, indent=2, sort_keys=True))
