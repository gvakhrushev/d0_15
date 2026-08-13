#!/usr/bin/env python3
"""SIEVE scan — family 'qft-rg' (vectorized null control).
Deterministic seed 20260814."""
import math, numpy as np
from fractions import Fraction

PHI = (1 + math.sqrt(5)) / 2
TOL = 0.005
KRANGE = np.arange(-17, 18)

LUCAS = [1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571]
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]
SCENE = [9, 11, 13, 33, 359, 1287, 960, 2574, 359 / PHI**2]
SEAM = [12/5, PHI**5 - 11, PHI**-17, 359/160]
MISC = [20, 44, 206, 15, 8, 10, 12, 1/math.sqrt(20), abs(3/5 - PHI), PHI, PHI**-3/2]
GROUP = [6, 8, 24, 48]
PHIPOW = [PHI**k for k in range(-17, 18)]
DIRECT = np.array(sorted(set(LUCAS + FIB + SCENE + SEAM + MISC + GROUP + PHIPOW)))

RATGRID = sorted(set(float(Fraction(p, r)) for p in range(1, 61) for r in range(1, 61)))
INT_LF = sorted(set(list(range(1, 61)) + LUCAS + FIB))
TARGETS = np.array(sorted(set(RATGRID + [float(t) for t in INT_LF])))
# label targets: is each target expressible as int/Lucas/Fib (vs only rational)?
INT_SET = set(float(t) for t in INT_LF)

CPV = len(DIRECT) + len(KRANGE) * 2 * len(TARGETS)

def scan_value(v):
    """Return list of raw hits and comparison count for one positive value."""
    hits = []
    rd = np.abs(v - DIRECT) / DIRECT
    for i in np.where(rd < TOL)[0]:
        hits.append(("direct", float(DIRECT[i]), float(rd[i])))
    for k in KRANGE:
        for sgn in (1, -1):
            x = v * PHI ** (float(sgn * k))
            rdt = np.abs(x - TARGETS) / TARGETS
            for i in np.where(rdt < TOL)[0]:
                t = float(TARGETS[i])
                kind = "int/L/F" if t in INT_SET else "rat"
                hits.append(("q*phi^%d vs %s" % (sgn * k, kind), t, float(rdt[i])))
    return hits, CPV

def null_rate(v, n=10000, seed=20260814):
    """Mean number of raw construction-hits per comparison for random values
    log-uniform over one decade centered on v. Vectorized."""
    rng = np.random.default_rng(seed)
    rv = 10 ** rng.uniform(math.log10(v) - 0.5, math.log10(v) + 0.5, n)  # (n,)
    total_hits = 0
    # direct
    rd = np.abs(rv[:, None] - DIRECT[None, :]) / DIRECT[None, :]
    total_hits += int((rd < TOL).sum())
    # phi^k sweeps vs targets
    lt = np.log(TARGETS)
    for k in KRANGE:
        for sgn in (1, -1):
            x = rv * PHI ** (float(sgn * k))
            # |x-t|/t < tol  <=>  t in [x/(1+tol), x/(1-tol)]
            lo = np.searchsorted(TARGETS, x / (1 + TOL), side="left")
            hi = np.searchsorted(TARGETS, x / (1 - TOL), side="right")
            total_hits += int((hi - lo).sum())
    return total_hits / (n * CPV)

# ------------- quantities -------------
PHYSICAL_EXTERNAL = []  # none found in assigned files (all are unfilled templates)
DILIGENCE = [
    ("Lambda_act = 38 (units m_e c^2) [D0-side matching scale]", 38.0),
    ("kY = 5/3 [scheme convention]", 5.0 / 3.0),
    ("2/(3*pi) one-loop QED kernel coeff [theory formula]", 2.0 / (3.0 * math.pi)),
]

def main():
    print("comparisons_per_value =", CPV)
    print("n external physical quantities =", len(PHYSICAL_EXTERNAL))
    print("same-unit ratios within family = 0")
    n_trials = 0
    for name, v in PHYSICAL_EXTERNAL + DILIGENCE:
        h, nc = scan_value(v)
        n_trials += nc
        print("\n[%s] value=%.10g  raw_hits=%d" % (name, v, len(h)))
        for cons, t, rdv in sorted(h, key=lambda z: z[2])[:10]:
            print("   %-24s target=%.10g rel_dev=%.5f" % (cons, t, rdv))
    print("\nn_trials_total =", n_trials)
    print("\n=== NULL CONTROL (seed 20260814, 10000 samples/value) ===")
    for name, v in PHYSICAL_EXTERNAL + DILIGENCE:
        nr = null_rate(v)
        print("%s : null_rate_per_comparison=%.6g expected_false_hits_over_scan=%.3f"
              % (name, nr, n_trials * nr))

if __name__ == "__main__":
    main()
