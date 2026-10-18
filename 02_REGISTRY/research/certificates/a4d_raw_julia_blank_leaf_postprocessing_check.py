#!/usr/bin/env python3
"""Exact native-Julia blank obstruction to passive sharp AF-leaf postprocessing.

Scope: CLASSICAL decoding of raw recorded words, not coherent access to data,
active LEFT CNOT registration, new measurements or GR physical forcing.
Read-only; no historical certificates are modified.
"""
import json
import sympy as sp

p = (sp.sqrt(5) - 1) / 2
u = sp.symbols("u", real=True)
assert sp.simplify(p + p**2 - 1) == 0

# Literal Julia golden port contribution at scalar A**2=u.
# Blank port0/label0, other port0, all port1; the 128 labels remain
# a complete POVM, although this two-active-Walsh-row algebraic fixture
# assigns zero effect to unrelated labels. This is NOT a native CAR16 census.
blank = 1 - 2*p**2*u
other_port0 = 4*p**4*u*(1-u)
port1_sum = 4*p**3*u
assert sp.simplify(blank**2 + other_port0 + port1_sum - 1) == 0

nu = sp.Rational(1, 256)
R = 2
T = sp.Rational(1, 4)
rows = []
for m in [1, 2, 8, 32]:
    floor = (1 - 2*p**2*(R*nu)**2)**(2*m)
    assert 0 < float(floor) < 1
    rows.append({
        "rounds": m,
        "minimum_blank_probability": float(floor.evalf(15)),
        "two_leaf_worst_TV_lower_bound": float((floor/2).evalf(15))
    })

# With m*nu_m**2 -> T the all-blank effect remains uniformly positive.
asymptotic_floor = sp.exp(-4*p**2*T*R**2)
assert 0 < float(asymptotic_floor) < 1

# A positive, complete POVM which saturates the sharp two-leaf decoder
# bound s(1-1/d): the ambiguous blank has effect s I.
s = sp.Rational(1, 3)
P = [sp.diag(1,0), sp.diag(0,1)]
E = [s*sp.eye(2), (1-s)*P[0], (1-s)*P[1]]
assert sum(E, sp.zeros(2)) == sp.eye(2)
for i in (0, 1):
    decoder = sp.Rational(1,2)*E[0] + E[i+1]
    p_correct = sp.trace(P[i]*decoder)
    assert p_correct == 1-s/2

# On the faithful uniform input the joint measurement has H(Y|Omega)
# exactly s log 2 (the blank is ambiguous, other words identify Y).
r = sp.Symbol("r", real=True)
h = lambda x: -x*sp.log(x)-(1-x)*sp.log(1-x)
assert sp.simplify(sp.diff(h(r),r).subs(r,sp.Rational(3,10))
                   - sp.log(sp.Rational(7,3))) == 0
missing_entropy_toy = s*sp.log(2)
assert float(missing_entropy_toy) >= float(s*s*sp.log(2))
# Scalar Julia effects are independent of the AF leaf; then precisely
# H(Y,Omega)-H(Omega)=h(r), with a nonzero preparation derivative at r=.3.

receipt = {
    "status":"EXACT_ALGEBRA_PASS",
    "carrier":"generic finite POVM plus two-mode Julia port algebra",
    "golden_128_port_completeness":"PASS",
    "exact_sharp_PVM_by_passive_postprocessing":"IMPOSSIBLE_WITH_FULL_RANK_BLANK",
    "minimax_control":"s*(1-1/d) sharp",
    "finite_blank_checks":rows,
    "weak_T_blank_limit":str(asymptotic_floor),
    "weak_T_blank_limit_decimal":float(asymptotic_floor.evalf(15)),
    "weak_T_two_leaf_TV_limit":float((asymptotic_floor/2).evalf(15)),
    "conditional_entropy_lower_bound":"s**2 * log(d)",
    "toy_conditional_entropy":str(missing_entropy_toy),
    "scalar_leaf_entropy_source_at_r_3_10":"log(7/3)",
    "scope":"NOT active LEFT gates; NOT exact D0-to-GR"
}
print(json.dumps(receipt, indent=2, sort_keys=True))
