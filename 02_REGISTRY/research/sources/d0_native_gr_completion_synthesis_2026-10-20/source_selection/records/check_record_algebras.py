"""Exact finite block-algebra classification for the existing scalar reporter.

No action, field coefficient, or compensation term is selected by this checker.
The supplied source compression t is an independent scalar coordinate.
"""
import json
import argparse
import math
import time
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
started_at = time.perf_counter()
p = (sp.sqrt(5) - 1) / 2
pn = float(p)
ell = math.log(1 / pn)
t = sp.symbols("t", real=True)
names = ("A", "B", "C", "D")
active = (0, 1, 4, 5)
weights = (p**4, p**2, p**3, p**3)
derivs = (2*p**3, sp.S.Zero, -2*p**3, sp.S.Zero)
d = 2*p**3


def simp(x):
    return sp.simplify(sp.expand(x))


def partitions(n):
    if n == 0:
        yield ()
        return
    for old in partitions(n - 1):
        for j in range(len(old)):
            yield old[:j] + (old[j] + (n - 1,),) + old[j+1:]
        yield old + ((n - 1,),)


def code_probs_symbolic(cap):
    q, lengths = [], []
    aa = (p**2 + p*t, p*sp.sqrt(p)*(1-t))
    bb = (p, -p*sp.sqrt(p))
    for b in range(2):
        q.append(aa[b]**2)
        lengths.append(2+b)
        for k in range(1, cap+1):
            q.append(bb[b]**2*(1-t*t)**2*t**(2*k-2))
            lengths.append(2+b+2*k)
        q.append(bb[b]**2*(1-t*t)*t**(2*cap))
        lengths.append(3+b+2*cap)
    return q, lengths


def tape_rho(x, cap=2):
    # Resolved and unresolved flag vectors have disjoint support. The data/work
    # isometries multiplying them are orthogonal, hence this exact Gram matrix.
    dim = 2*(cap+2)
    rr, uu = np.zeros(dim), np.zeros(dim)
    for b, (aa, bb) in enumerate(((pn**2+pn*x, pn),
                                  (pn*math.sqrt(pn)*(1-x), -pn*math.sqrt(pn)))):
        base = b*(cap+2)
        rr[base] = aa
        for k in range(1, cap+1):
            rr[base+k] = bb*(1-x*x)*(-x)**(k-1)
        uu[base+cap+1] = bb*math.sqrt(1-x*x)*(-x)**cap
    return np.outer(rr, rr)+np.outer(uu, uu)


def entropy(matrix):
    vals = np.linalg.eigvalsh(matrix)
    assert vals.min() > -2e-14
    vals = vals[vals > 1e-15]  # Only numerical diagnostic; proof uses exact rank.
    return float(-np.dot(vals, np.log(vals))/ell)


def pinched(rho, blocks):
    out = np.zeros_like(rho)
    for block in blocks:
        out[np.ix_(block, block)] = rho[np.ix_(block, block)]
    return out


def ent_partition(x, partition):
    blocks = [tuple(active[i] for i in b) for b in partition]
    blocks.extend((i,) for i in range(8) if i not in active)
    return entropy(pinched(tape_rho(x), blocks))


def cc(x):
    return 2+2*pn+2*pn**3*(1-x)-pn*(1+x*x)*x**4


rows = []
for part in partitions(4):
    ma = next(simp(sum(weights[i] for i in b)) for b in part if 0 in b)
    mc = next(simp(sum(weights[i] for i in b)) for b in part if 2 in b)
    same = any(0 in b and 2 in b for b in part)
    ratio = sp.S.One if same else simp(ma/mc)
    factor = math.log(float(ratio))/ell-1
    if abs(factor) < 2e-13:
        factor = 0.0
    coeff = float(d)*factor
    label = "|".join("".join(names[i] for i in b) for b in part)
    baseline_h = -sum(
        float(sum(weights[i] for i in b))*math.log(float(sum(weights[i] for i in b)))/ell
        for b in part
    )
    # Central differentiation avoids cancellation from the even rank-birth term.
    eps = 1e-5
    numeric = ((cc(eps)-ent_partition(eps, part)) -
               (cc(-eps)-ent_partition(-eps, part)))/(2*eps)
    assert abs(numeric-coeff) < 4e-8, (label, numeric, coeff)
    rho = tape_rho(.023)
    blocks = [tuple(active[i] for i in b) for b in part]
    blocks.extend((i,) for i in range(8) if i not in active)
    assert np.allclose(np.diag(pinched(rho, blocks)), np.diag(rho), atol=1e-15)
    rows.append(dict(partition=label, ratio=str(ratio),
                     coefficient_over_2p3=factor, coefficient=coeff,
                     entropy_at_zero=baseline_h,
                     price_at_zero=6*pn-baseline_h,
                     numerical_derivative=numeric))

assert len(rows) == 15
assert sum(abs(r["coefficient"]) < 1e-14 for r in rows) == 1
assert sum(r["coefficient"] > 1e-14 for r in rows) == 2
assert sum(r["coefficient"] < -1e-14 for r in rows) == 12

# All cap-two algebras, not only representative active partitions: every
# partition of eight pointer atoms induces exactly one active four-partition.
full_counts = dict(zero=0, positive=0, negative=0)
weight_numbers = tuple(float(q) for q in weights)
for fullpart in partitions(8):
    induced = tuple(tuple(active.index(i) for i in b if i in active)
                    for b in fullpart if any(i in active for i in b))
    ma = next(sum(weight_numbers[i] for i in b) for b in induced if 0 in b)
    mc = next(sum(weight_numbers[i] for i in b) for b in induced if 2 in b)
    same = any(0 in b and 2 in b for b in induced)
    coeff = -float(d) if same else float(d)*(math.log(float(ma/mc))/ell-1)
    key = "zero" if abs(coeff) < 1e-13 else "positive" if coeff > 0 else "negative"
    full_counts[key] += 1
assert full_counts == dict(zero=372, positive=523, negative=3245), full_counts

# Exact zero-source identity, preserving every pointer projection.
assert simp(p**4+p**3-p**2) == 0
assert simp((p**4+p**3)/p**3-1/p) == 0
assert simp(6*p-(4*p**2+3*p**3)-(4*p-1)) == 0
# Exact positive-source identity.
assert simp(p**4+p**2+p**3-2*p**2) == 0

# An exact zero-source algebra with no quadratic entropy rank birth:
# block {A,D,E,F,U0,U1}, and singleton blocks {B}, {C}.
# The unresolved vector is orthogonal to the resolved vector in this block,
# so the exact spectrum is (R,qB,qC,delta), padded with zeros.
q2, _ = code_probs_symbolic(2)
null_eigs = (q2[0]+q2[5]+q2[2]+q2[6], q2[1], q2[4], q2[3]+q2[7])
assert simp(sum(null_eigs)-1) == 0
null_hessian = 4*float(p**2)/ell-2*float(p**3)
assert null_hessian > 0
positive = null_eigs[:3]
log_coeff = (2, 2, 3)  # log(m(0)) = -log_coeff * ln(phi)
null_hessian_symbolic = -sum(
    sp.diff(m,t,2).subs(t,0)*k for m,k in zip(positive,log_coeff)
) + sum(sp.diff(m,t).subs(t,0)**2/m.subs(t,0) for m in positive)/sp.Symbol("ell", positive=True)
assert simp(null_hessian_symbolic-(4*p**2/sp.Symbol("ell", positive=True)-2*p**3)) == 0

def null_price(x):
    eigs = [float(m.subs(t,x)) for m in null_eigs]
    h = -sum(v*math.log(v)/ell for v in eigs if v > 0)
    return cc(x)-h

eps = 1e-4
null_hessian_numeric = (null_price(eps)+null_price(-eps)-2*null_price(0))/eps**2
assert abs(null_hessian_numeric-null_hessian) < 2e-5
assert null_price(eps) > null_price(0)
assert null_price(-eps) > null_price(0)

# Hostile control: two independent pointer reporters have opposite first
# sources, hence exact pair stationarity, but a strict two-sided descent.
def pointer_price(x):
    eigs = [float(q.subs(t,x)) for q in q2]
    h = -sum(v*math.log(v)/ell for v in eigs if v > 0)
    return cc(x)-h

pointer_pair_control = []
for eps in (1e-2, 1e-3, 1e-4):
    change = pointer_price(eps)+pointer_price(-eps)-2*pointer_price(0)
    assert change < 0
    pointer_pair_control.append(dict(
        epsilon=eps, price_change=change,
        normalized_by_epsilon2_logepsilon2=change/(eps**2*math.log(eps**2)),
        limiting_coefficient=2*pn/ell,
    ))

exact = []
for cap in (1, 2, 3, 5):
    qs, ls = code_probs_symbolic(cap)
    code = sum(q*L for q, L in zip(qs, ls))
    assert simp(sum(qs)-1) == 0
    assert simp(sum(p**L for L in ls)-1) == 0
    assert simp(code-(2+2*p+2*p**3*(1-t)-p*(1+t*t)*t**(2*cap))) == 0
    # Total probability of newly born pointer leaves has universal leading p t².
    new = sum(qs[j] for j in range(len(qs)) if simp(qs[j].subs(t, 0)) == 0)
    assert simp(sp.diff(new,t,2).subs(t,0)/2-p) == 0
    exact.append(dict(cap=cap, normalization=True, kraft=True, code=True,
                      born_pointer_quadratic_coefficient=str(p)))

spectral_max_error = 0.
for cap in (1, 2, 3, 5):
    for x in (-.73, -.19, 0., .023, .32, .81):
        rho = tape_rho(x, cap)
        delta = pn*(1-x*x)*x**(2*cap)
        expected = np.zeros(len(rho))
        expected[-2:] = sorted((delta, 1-delta))
        err = float(np.max(abs(np.linalg.eigvalsh(rho)-expected)))
        spectral_max_error = max(spectral_max_error, err)
        assert err < 2e-14

result = dict(
    source_revision="41582f57",
    full_pinned_source_revision="41582f57 (parent supplied published pin)",
    cap_two_leaf_order="A,B,E,unresolved0,C,D,F,unresolved1",
    classification=rows,
    counts=dict(partitions=15, zero=1, positive=2, negative=12),
    full_eight_leaf_partition_counts=full_counts,
    source_coefficient_classes=9,
    stationary_pointer_pair_descent_control=pointer_pair_control,
    smooth_zero_source_algebra=dict(
        blocks=[[0,5,2,6,3,7],[1],[4]],
        hessian=null_hessian,
        hessian_finite_difference=null_hessian_numeric,
        exact_formula="4*p**2/log(phi)-2*p**3",
        price_at_zero="4*p-1",
    ),
    exact_algebra_checks=exact,
    max_coherent_tape_spectrum_error=spectral_max_error,
    scope="Fixed unital *-subalgebras containing all rank-one pointer projections; "
          "canonical ambient trace entropy. No physical algebra selection asserted.",
    checker_runtime_seconds=time.perf_counter()-started_at,
)
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, help="Optional new receipt; default replay is read-only")
args = parser.parse_args()
if args.output:
    if args.output.resolve() == (HERE/"results.json").resolve():
        raise SystemExit("Refusing to overwrite the saved research receipt")
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
for row in rows:
    print(f"{row['partition']:11s} ratio={row['ratio']:22s} "
          f"kappa={row['coefficient']:+.12f} S0={row['entropy_at_zero']:.9f}")
print(json.dumps({k: result[k] for k in ("counts","full_eight_leaf_partition_counts",
      "smooth_zero_source_algebra","max_coherent_tape_spectrum_error")}))
