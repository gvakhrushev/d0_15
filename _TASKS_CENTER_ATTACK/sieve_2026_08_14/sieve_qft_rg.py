#!/usr/bin/env python3
"""SIEVE scan — family 'qft-rg'.
Assigned dirs:
  08_PASSPORTS/QFT_RG_ALPHA_PASSPORT
  08_PASSPORTS/QFT_RG_SCHEME_PASSPORTS
  08_PASSPORTS/PDG_RG_SCHEME_TEMPLATES
Deterministic. Seed 20260814 for null control.
"""
import math, random, json
from fractions import Fraction

PHI = (1 + math.sqrt(5)) / 2

# ---------------------------------------------------------------
# Step 1: quantity extraction (done by inspection of the 4 files;
# every numeric token in the assigned files is listed here with its
# classification).
# ---------------------------------------------------------------
ALL_NUMERIC_TOKENS = [
    # (file, token, value, classification, reason)
    ("08_PASSPORTS/PDG_RG_SCHEME_TEMPLATES/PDG_RG_SCHEME_PASSPORT_TEMPLATES.csv",
     "matching_scale_Lambda_act = 38 m_e c^2", 38.0,
     "EXCLUDED-D0-SIDE",
     "Lambda_act is D0's own declared matching scale (model construction), not an external measured value"),
    ("08_PASSPORTS/QFT_RG_SCHEME_PASSPORTS/D0_V11_33_QFT_RG_PDG_SCHEME_PASSPORTS.md",
     "kY = 5/3", 5.0/3.0,
     "EXCLUDED-CONVENTION",
     "GUT hypercharge normalization constant: a scheme convention, not a measured quantity"),
    ("08_PASSPORTS/QFT_RG_ALPHA_PASSPORT/D0_V11_34_ALPHA_SCHEME_PASSPORT_EXECUTED.md",
     "one-loop QED kernel coefficient 2/(3*pi)", 2.0/(3.0*math.pi),
     "EXCLUDED-THEORY-FORMULA",
     "Standard one-loop QED beta coefficient, textbook constant, not measured data"),
    ("08_PASSPORTS/QFT_RG_ALPHA_PASSPORT/D0_V11_34_ALPHA_SCHEME_PASSPORT_EXECUTED.md",
     "version tokens v11.33/v11.34, guardrail item numbers 1-5", None,
     "EXCLUDED-METADATA", "versions / list indices"),
]

# External physical measured quantities found in the assigned files:
PHYSICAL_QUANTITIES = []  # none — all files are unfilled scheme/passport TEMPLATES

# Diligence set: excluded-by-protocol values that we nevertheless scan
# (results flagged, not reportable as external hits).
DILIGENCE = [(t[1], t[2]) for t in ALL_NUMERIC_TOKENS if t[2] is not None]

# ---------------------------------------------------------------
# Motif library
# ---------------------------------------------------------------
LUCAS = [1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571]
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]
SCENE = [9, 11, 13, 33, 359, 1287, 960, 2574, 359 / PHI**2]
SEAM = [12/5, PHI**5 - 11, PHI**-17, 359/160]
MISC = [20, 44, 206, 15, 8, 10, 12, 1/math.sqrt(20), 3/5 - PHI, PHI, PHI**-3/2]
GROUP = [6, 8, 24, 48]
PHIPOW = [PHI**k for k in range(-17, 18)]

DIRECT_MOTIFS = sorted(set(
    [abs(x) for x in (LUCAS + FIB + SCENE + SEAM + MISC + GROUP + PHIPOW)]))

# rational grid p/r, 1<=p<=60, 1<=r<=60 (positive; quantities here all positive)
RATGRID = sorted(set(float(Fraction(p, r)) for p in range(1, 61) for r in range(1, 61)))
INT_LF = sorted(set(list(range(1, 61)) + LUCAS + FIB))  # integers + Lucas + Fib targets

TOL = 0.005
KRANGE = list(range(-17, 18))

def scan_value(v):
    """Scan one positive value with all allowed constructions.
    Returns (hits, n_comparisons)."""
    hits = []
    ncmp = 0
    # (a) direct vs motif
    for m in DIRECT_MOTIFS:
        ncmp += 1
        if m != 0:
            rd = abs(v - m) / abs(m)
            if rd < TOL:
                hits.append(("direct", "m=%.10g" % m, m, rd))
    # (b) v*phi^k and v/phi^k vs rationals and vs integers/Lucas/Fib
    targets = sorted(set([("rat", t) for t in RATGRID] + [("int", float(t)) for t in INT_LF]))
    for k in KRANGE:
        for sgn in (1, -1):
            x = v * PHI**(sgn * k)
            for kind, t in targets:
                ncmp += 1
                rd = abs(x - t) / abs(t)
                if rd < TOL:
                    hits.append(("q*phi^%d vs %s" % (sgn * k, kind), "t=%.10g" % t, t, rd))
    return hits, ncmp

def comparisons_per_value():
    targets = sorted(set([("rat", t) for t in RATGRID] + [("int", float(t)) for t in INT_LF]))
    return len(DIRECT_MOTIFS) + len(KRANGE) * 2 * len(targets)

def null_rate(v, n=10000, seed=20260814):
    """Fraction of comparisons that raw-hit for random values log-uniform
    over one decade around v."""
    rng = random.Random(seed)
    lo, hi = math.log10(v) - 0.5, math.log10(v) + 0.5
    tot_hits = 0
    cpv = comparisons_per_value()
    for _ in range(n):
        rv = 10 ** rng.uniform(lo, hi)
        h, _ = scan_value(rv)
        tot_hits += len(h)
    return tot_hits / (n * cpv)

def main():
    cpv = comparisons_per_value()
    print("comparisons_per_value =", cpv)
    n_trials_total = 0
    results = []

    print("\n=== EXTERNAL PHYSICAL QUANTITIES ===")
    print("count =", len(PHYSICAL_QUANTITIES))
    for name, v in PHYSICAL_QUANTITIES:
        h, nc = scan_value(v)
        n_trials_total += nc
        results.append((name, v, h, "external"))

    # ratios within family: 0 external quantities -> 0 ratios
    print("same-unit ratio pairs within family: 0 (no external quantities)")

    print("\n=== DILIGENCE SCAN (protocol-EXCLUDED values, not reportable) ===")
    for name, v in DILIGENCE:
        h, nc = scan_value(v)
        n_trials_total += nc
        results.append((name, v, h, "excluded-diligence"))
        print("\n%s = %.10g : %d raw construction-hits out of %d comparisons"
              % (name, v, len(h), nc))
        # keep only best few by deviation for display
        for cons, tdesc, t, rd in sorted(h, key=lambda z: z[3])[:8]:
            print("   %-22s %-18s rel_dev=%.5f" % (cons, tdesc, rd))

    print("\nn_trials_total =", n_trials_total)

    print("\n=== NULL CONTROL (per diligence value) ===")
    for name, v in DILIGENCE:
        nr = null_rate(v)
        efh = n_trials_total * nr
        print("%s: null hit rate per comparison = %.6f ; expected_false_hits over whole scan = %.2f"
              % (name, nr, efh))

    print("\nSurviving reportable hits (external quantities, expected_false_hits<0.5): 0")

if __name__ == "__main__":
    main()
