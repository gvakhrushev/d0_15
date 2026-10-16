#!/usr/bin/env python3
"""Exact finite algebra for the native-prefix secant detector.

This checks a generic symbolic block, not a finite enumeration of A4D roots.
The analytic secant theorem and the effective algebraic quotient proof are
in A4D_NATIVE_FINITE_PROBE_COMPLETION.md. Default execution checks the pinned
ledger without changing it; --output explicitly creates a ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sympy as sp

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
parser.add_argument('--expect',type=Path)
args=parser.parse_args()

p, s, z, w, a, b = sp.symbols("p s z w a b", real=True)
relations = sp.groebner([s*s-p, p*p+p-1], s, p, order="lex")


def reduce_phi(expr):
    """Polynomial reduction, treating z,w,a,b as coefficient variables."""
    poly = sp.Poly(sp.expand(expr), z, w, a, b)
    result = 0
    for exponents, coeff in poly.terms():
        remainder = relations.reduce(coeff)[1]
        monomial = sp.prod(t**e for t, e in zip((z,w,a,b), exponents))
        result += remainder * monomial
    return sp.expand(result)


checks = []


def check_zero(name, expr):
    entries = list(expr) if isinstance(expr, sp.MatrixBase) else [expr]
    reduced = [reduce_phi(x) for x in entries]
    assert all(x == 0 for x in reduced), (name, reduced)
    checks.append({"name": name, "scalar_identities": len(entries), "passed": True})


u = sp.Matrix([s,p])
v = sp.Matrix([p,-s])
check_zero("golden unit-vector norm", (u.T*u)[0]-1)
check_zero("golden contrast norm", (v.T*v)[0]-1)
check_zero("golden mean/contrast orthogonality", (u.T*v)[0])
check_zero("golden mean/detail decomposition", u*u.T+v*v.T-sp.eye(2))

D = lambda q: sp.diag(1,q+1,q-1,0)
R = lambda q: D(q).T*D(q)
check_zero("scalar positive-response total", sp.trace(R(z))-(3+2*z*z))
check_zero("signed contrast recovers z", R(z)[1,1]-R(z)[2,2]-4*z*R(z)[0,0])

J = sp.kronecker_product(sp.eye(4),u)
V = sp.kronecker_product(sp.eye(4),v)
P = J.T
D_old = a*D(z)
E_new = b*D(w)
D_fine = J*D_old*J.T + V*E_new*V.T
R_old = D_old.T*D_old
R_fine = D_fine.T*D_fine
check_zero("prefix isometry", P*J-sp.eye(4))
check_zero("prefix kills detail", P*V)
check_zero("history-specific exact operator naturality", P*D_fine-D_old*P)
check_zero("orthogonal positive-response split",
           R_fine-J*R_old*J.T-V*(E_new.T*E_new)*V.T)
check_zero("retained positive response exactly preserved", P*R_fine*P.T-R_old)
check_zero("trace adds independent history blocks",
           sp.trace(R_fine)-a*a*(3+2*z*z)-b*b*(3+2*w*w))

projectors = []
for i in range(4):
    e = sp.zeros(4,1)
    e[i,0] = 1
    projectors.append(e*e.T)

old_raw = [sp.trace(J*e*J.T*R_fine) for e in projectors]
new_raw = [sp.trace(V*e*V.T*R_fine) for e in projectors]
check_zero("every historical event raw response retained",
           sp.Matrix([old_raw[i]-R_old[i,i] for i in range(4)]))
check_zero("new detail event raw response has selected gain",
           sp.Matrix([new_raw[i]-b*b*R(w)[i,i] for i in range(4)]))
check_zero("old contrast survives addition and both gains",
           old_raw[1]-old_raw[2]-4*z*old_raw[0])
check_zero("new contrast survives addition and both gains",
           new_raw[1]-new_raw[2]-4*w*new_raw[0])

# The same naturality without sqrt(p): native weighted value basis.
Jq = sp.kronecker_product(sp.eye(4),sp.Matrix([1,1]))
Pq = sp.kronecker_product(sp.eye(4),sp.Matrix([[p,p*p]]))
Wq = sp.kronecker_product(sp.eye(4),sp.Matrix([p,-1]))
Wdagq = sp.kronecker_product(sp.eye(4),sp.Matrix([[p*p,-p*p]]))
invp = 1+p
Dq = Jq*D_old*Pq+invp*Wq*E_new*Wdagq
Rq = Dq*Dq
G_old = sp.diag(p*p,p**3,p**3,p**4)
G_fine = sp.kronecker_product(G_old,sp.diag(p,p*p))
check_zero("Q(phi) prefix isometry", Pq*Jq-sp.eye(4))
check_zero("Q(phi) weighted contrast orthogonality", Pq*Wq)
check_zero("Q(phi) weighted contrast norm", Wdagq*Wq-p*sp.eye(4))
check_zero("Q(phi) exact mean/detail decomposition", Jq*Pq+invp*Wq*Wdagq-sp.eye(8))
check_zero("Q(phi) weighted self-adjointness", G_fine*Dq-Dq.T*G_fine)
check_zero("Q(phi) native prefix operator naturality", Pq*Dq-D_old*Pq)
check_zero("Q(phi) retained positive response", Pq*Rq*Jq-R_old)
check_zero("Q(phi) positive response trace", sp.trace(Rq)-a*a*(3+2*z*z)-b*b*(3+2*w*w))
rawq_old = [sp.trace(Jq*e*Pq*Rq) for e in projectors]
rawq_new = [sp.trace(invp*Wq*e*Wdagq*Rq) for e in projectors]
check_zero("Q(phi) old weighted-event contrast", rawq_old[1]-rawq_old[2]-4*z*rawq_old[0])
check_zero("Q(phi) new weighted-event contrast", rawq_new[1]-rawq_new[2]-4*w*rawq_new[0])

for q in [Fraction(-7,3),Fraction(-1),Fraction(0),Fraction(1),Fraction(11,7)]:
    resp = [Fraction(1),(q+1)**2,(q-1)**2,Fraction(0)]
    total = sum(resp)
    probs = [x/total for x in resp]
    assert total > 0
    assert sum(probs) == 1
    assert (probs[1]-probs[2])/(4*probs[0]) == q
checks.append({"name":"exact rational finite-effect instances", "instances":5,"passed":True})

# Any set of diameter <=d/2 fits in at most two d-bins, including negatives
# and exact boundaries. This is only a boundary replay of the elementary
# theorem proved in the report, not its proof by finite testing.
for denominator in [1,2,3,5,11]:
    d = Fraction(1,denominator)
    for numerator in range(-17,18):
        start = numerator*d/Fraction(7)
        values = [start, start+d/Fraction(8), start+d/Fraction(4), start+d/Fraction(2)]
        bins = {(x/d).__floor__() for x in values}
        assert len(bins) <= 2
checks.append({"name":"terminal-bin boundary controls", "instances":175,"passed":True})

# Exact geometric-series formulas used by the attenuation theorem.
for n in range(1,9):
    finite_sum = sum(p**(2*j) for j in range(1,n+1))
    check_zero(f"gain-square finite geometric identity N={n}",
               (1-p*p)*finite_sum-p*p*(1-p**(2*n)))
check_zero("golden total gain-square bound factor", p*p-p*(1-p*p))

repo=Path(__file__).resolve().parents[3]
inputs=('03_FORMALIZATION/D0/CondensedAnchor/DetectorSupportGoldenWeight.lean','03_FORMALIZATION/D0/Core/BornFiniteEffects.lean','03_FORMALIZATION/D0/Condensed/OperatorNaturality.lean')
out = {
    'proof':'A4D_NATIVE_FINITE_PROBE_COMPLETION.md',
    'input_sha256':{name:hashlib.sha256((repo/name).read_bytes()).hexdigest() for name in inputs},
    "verdict":"PASS",
    "checks":checks,
    "summary":{
        "check_groups":len(checks),
        "symbolic_scalar_identities":sum(c.get("scalar_identities",0) for c in checks),
        "finite_instance_controls":sum(c.get("instances",0) for c in checks),
        "scope":"Generic exact finite detector, prefix naturality, golden attenuation; no A4D stationary-locus enumeration or native Role map."
    }
}
if args.expect or not args.output:
    expected_path=args.expect or Path(__file__).with_name('a4d_finite_probe_golden_detector_results.json')
    assert out == json.loads(expected_path.read_text()), 'pinned ledger mismatch'
if args.output:
    args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out["summary"],indent=2))
print("PASS")
