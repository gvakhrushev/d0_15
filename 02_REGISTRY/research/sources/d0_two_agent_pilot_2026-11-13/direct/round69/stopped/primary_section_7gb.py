#!/usr/bin/env python3
"""Exact one-jet proof on the original full128 Fourier/CAR fixture.

No numerical spectra: the original N_j N_j^dagger are checked diagonal.
This concerns the specified fine conditional-CQ observable, not selection
of physical Book Info or a complete D0/GR price.
"""
from collections import defaultdict
import json
import sympy as s

I, O = s.eye(16), s.zeros(16)
nu, kappa = s.Rational(3, 5), s.Rational(9, 640)
order = (0, 2, 3, 1)
cs = []
for r in range(4):
    c = O.copy()
    before = order[:order.index(r)]
    for bits in range(16):
        if not ((bits >> r) & 1):
            c[bits | (1 << r), bits] = (-1) ** sum((bits >> j) & 1 for j in before)
    cs.append(c)

phases = (s.I, s.I, -1, -s.I)
words, jets = [], []
def need(condition, label):
    if not condition:
        raise ArithmeticError(label)

def same(left, right):
    return (left - right).applyfunc(s.expand) == s.zeros(*left.shape)

def rootjet(root, rhs):
    result = s.Matrix(16, 16, lambda i, j: rhs[i, j] / (root[i, i] + root[j, j]))
    need(same(root * result + result * root, rhs), "true Sylvester derivative")
    return result

for r, c in enumerate(cs):
    base = nu * c
    dbase = cs[0] - cs[1] if r == 0 else O
    x, dx = phases[r] * base, phases[r] * dbase
    left, right = I - (c * c.H) / 5, 4 * I / 5 + (c * c.H) / 5
    dleft = rootjet(left, -dx * x.H - x * dx.H)
    dright = rootjet(right, -dx.H * x - x.H * dx)
    dleft0 = rootjet(left, -dbase * base.H - base * dbase.H)
    dright0 = rootjet(right, -dbase.H * base - base.H * dbase)
    for word, jet in zip(
        ((x, left), (x.H, right), (-base, -left), (-base.H, -right)),
        ((dx, dleft), (dx.H, dright), (-dbase, -dleft0), (-dbase.H, -dright0)),
    ):
        words.extend((word, word))
        jets.extend((jet, jet))

ns, dns = [], []
for lab in range(32):
    signs = [(-1) ** (bin(lab & j).count("1") & 1) for j in range(32)]
    for bit in (0, 1):
        ns.append(sum((signs[j] * words[j][bit] for j in range(32)), O.copy()) / 32)
        dns.append(sum((signs[j] * jets[j][bit] for j in range(32)), O.copy()) / 32)

a, da = ns[0], dns[0]
pi = s.diag(*[(-1) ** bin(bits).count("1") for bits in range(16)])
need(same(a.H, a) and same(da.H, da), "actual self-adjoint row and its jet")
need(same(a * a, kappa * I), "original scalar Lambda")
need(same(pi * a + a * pi, O), "original odd Dirac row")
need(same(a * da + da * a, O), "D Lambda is the zero MATRIX")
need(same(sum((n.H * n for n in ns), O.copy()), I), "all64 original Walsh rows retained")
need(same(sum((n * n.H for n in ns), O.copy()), I), "original coisometric row identity")

coeff = defaultdict(lambda: s.S.Zero)
trace_jet = s.S.Zero
dark_diagonal_jet = s.S.Zero
active_rows = 0
for j, (n, dn) in enumerate(zip(ns, dns)):
    m = (n * n.H).applyfunc(s.expand)
    dm = (dn * n.H + n * dn.H).applyfunc(s.expand)
    need(m == s.diag(*m.diagonal()), "exact diagonal baseline M_j")
    projectors = []
    for eig in set(m.diagonal()):
        need(eig.is_Rational and eig >= 0, "exact nonnegative rational spectrum")
        proj = s.diag(*[int(value == eig) for value in m.diagonal()])
        need(proj * proj == proj and m * proj == eig * proj,
             "exact rational spectral projector")
        if eig == 0:
            need(proj * dm * proj == O, "zero-support first spectral jet vanishes")
        projectors.append(proj)
    need(sum(projectors, O.copy()) == I, "complete spectral resolution, including zero")
    trace_jet += s.trace(dm)
    if j == 0:
        need(dm == O, "special quiet row has no jet")
        continue
    if dm != O:
        active_rows += 1
    for eig, derivative in zip(m.diagonal(), dm.diagonal()):
        if eig == 0:
            need(derivative == 0, "zero eigenvalue has zero first eigenvalue derivative")
            dark_diagonal_jet += derivative
        elif derivative != 0:
            coeff[eig] += derivative
need(trace_jet == 0, "all-channel trace normalizer differentiated")
coeff = {e: s.factor(w) for e, w in coeff.items() if w != 0}
expected = {
    s.Rational(81, 100): -s.Rational(27, 10),
    s.Rational(1, 400): s.Rational(3, 20),
    s.Rational(1, 100): s.Rational(3, 20),
    s.Rational(9, 640): s.Rational(6, 5),
    s.Rational(27, 3200): s.Rational(6, 5),
}
need(coeff == expected, "exact full-palette logarithmic derivative coefficients")
need(sum(coeff.values()) == 0, "all scalar log factors cancel")

# Factor rational eigenvalues into primes; no approximate logarithm is used.
prime_coeff = defaultdict(lambda: s.S.Zero)
for eig, weight in coeff.items():
    numerator, denominator = s.fraction(eig)
    for prime, power in s.factorint(numerator).items():
        prime_coeff[int(prime)] += weight * power
    for prime, power in s.factorint(denominator).items():
        prime_coeff[int(prime)] -= weight * power
need(dict(prime_coeff) == {2: -s.Rational(123, 10), 3: -s.Rational(24, 5), 5: s.Rational(6, 5)},
     "exact reduction to log2 log3 log5")
need(2**41 * 3**16 > 5**4, "strict sign by integer comparison")
p = (s.sqrt(5) - 1) / 2
answer = 27 * p**2 / 25600 * (41*s.log(2) + 16*s.log(3) - 4*s.log(5))
result = {
    "status": "PASS_EXACT_FULL128_CQ_COFRAME_RESIDUAL",
    "actual_tangent": "dC_0=c_0-c_1; dx_0=i*dC_0; all other legs fixed",
    "D_Lambda_zero_as_matrix": True,
    "generated_inverse_Lambda_preparation_jet_zero": True,
    "all_baseline_M_j_exactly_diagonal": True,
    "all_rational_spectral_projectors_exactly_verified": True,
    "active_M_j_derivative_rows": active_rows,
    "sum_Tr_DM_logM_coefficients": {str(e): str(w) for e,w in coeff.items()},
    "zero_support_first_eigenvalue_derivatives": str(dark_diagonal_jet),
    "CQ_direct_derivative_exact": "27*p^2/25600 * (41*log(2)+16*log(3)-4*log(5))",
    "CQ_direct_derivative_decimal_diagnostic": str(s.N(answer, 50)),
    "strictly_positive_by_integer_comparison": True,
    "scope": "Specified complete one-round fine conditional-CQ operand only. No physical Info selection, stopped-history theorem, complete Cost-Info binding, or GR closure.",
}
print(json.dumps(result, sort_keys=True, indent=2))
