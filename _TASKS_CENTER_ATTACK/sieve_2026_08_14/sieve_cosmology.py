#!/usr/bin/env python3
"""D0 SIEVE scan — family: cosmology (DESI/DESI_BAO/PlanckCMB passports).
Deterministic. Seed 20260814 for null control.
"""
import math, random
from fractions import Fraction
import numpy as np

PHI = (1 + math.sqrt(5)) / 2
SEED = 20260814
TOL = 0.005  # relative deviation < 0.5%

# ---------------------------------------------------------------- quantities
# External/measured side only (see file provenance in comments).
# 08_PASSPORTS/DESI/desi_bao_sde_real_data_results.csv and
# 08_PASSPORTS/DESI/desi_bao_sde_failure_diagnostics.csv
BASE = {
    "dm_rd_obs[BGS,z=0.3]": 7.85,
    "dm_rd_obs[LRG,z=0.7]": 17.8,
    "dm_rd_obs[ELG,z=1.1]": 25.4,
    "z_eff[BGS]": 0.3,
    "z_eff[LRG]": 0.7,
    "z_eff[ELG]": 1.1,
}
# same-unit ratios within family
RATIOS = {
    "dm_rd[LRG]/dm_rd[BGS]": 17.8 / 7.85,
    "dm_rd[ELG]/dm_rd[BGS]": 25.4 / 7.85,
    "dm_rd[ELG]/dm_rd[LRG]": 25.4 / 17.8,
    "z_eff[LRG]/z_eff[BGS]": 0.7 / 0.3,
    "z_eff[ELG]/z_eff[BGS]": 1.1 / 0.3,
    "z_eff[ELG]/z_eff[LRG]": 1.1 / 0.7,
}

# ---------------------------------------------------------------- motif library
LUCAS = [1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571]
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]

motifs = {}  # name -> value
def addm(name, val):
    key = round(val, 12)
    # dedupe by value, keep first name
    for n, v in motifs.items():
        if abs(v - val) <= 1e-12 * max(1.0, abs(val)):
            return
    motifs[name] = val

for k in range(-17, 18):
    addm(f"phi^{k}", PHI ** k)
for i, L in enumerate(LUCAS):
    addm(f"L_{i+1}", float(L))
for i, F in enumerate(FIB):
    addm(f"F_{i+1}", float(F))
for v in [9, 11, 13, 33, 359, 1287, 960, 2574]:
    addm(f"scene_{v}", float(v))
addm("359/phi^2", 359 / PHI ** 2)
addm("12/5", 12 / 5)
addm("xi5=phi^-5", PHI ** -5)
addm("phi^-17", PHI ** -17)
addm("359/160", 359 / 160)
for v in [20, 44, 206, 15, 8, 10, 12, 6, 24, 48]:
    addm(f"int_{v}", float(v))
addm("1/sqrt20", 1 / math.sqrt(20))
addm("3/5-phi", 3 / 5 - PHI)               # negative
addm("delta0=phi^-3/2", PHI ** -3 / 2)     # POST-HOC family -> flag
# toral traces Tr T^n = (-1)^n L_n : odd n give -L_n (evens dupe Lucas)
for i, L in enumerate(LUCAS):
    n = i + 1
    if n % 2 == 1:
        addm(f"TrT^{n}=-L_{n}", -float(L))

MOTIF_NAMES = list(motifs.keys())
MOTIF_VALS = np.array([motifs[n] for n in MOTIF_NAMES])
C_A = len(MOTIF_NAMES)  # comparisons per value, construction A

# positive motifs sorted (for vectorised null; negative motifs never match
# positive samples, but they ARE counted in C_A)
pos_mask = MOTIF_VALS > 0
POS_MOTIFS_SORTED = np.sort(MOTIF_VALS[pos_mask])

# construction B target set: reduced rationals p/r, 1<=p,r<=60, union Lucas, Fib
ratset = set()
for p in range(1, 61):
    for r in range(1, 61):
        ratset.add(Fraction(p, r))
targets = {}
for fr in ratset:
    targets[float(fr)] = f"{fr.numerator}/{fr.denominator}"
for i, L in enumerate(LUCAS):
    if float(L) not in targets:
        targets[float(L)] = f"L_{i+1}"
for i, F in enumerate(FIB):
    if float(F) not in targets:
        targets[float(F)] = f"F_{i+1}"
TARGET_VALS = np.array(sorted(targets.keys()))
TARGET_NAMES = [targets[v] for v in TARGET_VALS]
KLIST = list(range(-17, 18))
C_B = len(KLIST) * len(TARGET_VALS)  # comparisons per value, construction B

# ---------------------------------------------------------------- raw scan
n_trials = 0
raw_hits = []  # (qname, qval, construction, expr, motif_name, motif_val, rel_dev)

def reldev(q, m):
    return abs(q - m) / abs(m)

# A: direct motif comparison, all 12 quantities
ALLQ = {**BASE, **RATIOS}
for qn, qv in ALLQ.items():
    for mn in MOTIF_NAMES:
        mv = motifs[mn]
        n_trials += 1
        d = reldev(qv, mv)
        if d < TOL:
            raw_hits.append((qn, qv, "A", f"{qn} vs {mn}", mn, mv, d))

# B: phi^k sweep vs rational/Lucas/Fib grid, base quantities only
for qn, qv in BASE.items():
    for k in KLIST:
        t = qv * PHI ** k
        lo = t / (1 + TOL)
        hi = t / (1 - TOL)
        i0 = np.searchsorted(TARGET_VALS, lo, side="left")
        i1 = np.searchsorted(TARGET_VALS, hi, side="right")
        n_trials += len(TARGET_VALS)
        for j in range(i0, i1):
            mv = TARGET_VALS[j]
            d = reldev(t, mv)
            if d < TOL:
                raw_hits.append((qn, qv, "B",
                                 f"{qn} * phi^{k} vs {TARGET_NAMES[j]}",
                                 TARGET_NAMES[j], mv, d))

print(f"n_quantities = {len(ALLQ)}")
print(f"C_A (motif set size) = {C_A}")
print(f"C_B (35 k x {len(TARGET_VALS)} targets) = {C_B}")
print(f"n_trials_total = {n_trials}")
print(f"raw hits: {len(raw_hits)}")

# ---------------------------------------------------------------- null control
rng = random.Random(SEED)
null_cache = {}

def null_rate(v, construction):
    """total null hits over 10000 log-uniform samples in one decade around v,
    divided by (10000 * comparisons-per-value) -> per-comparison null rate."""
    key = (round(v, 12), construction)
    if key in null_cache:
        return null_cache[key]
    lo, hi = math.log10(v) - 0.5, math.log10(v) + 0.5
    samples = np.array([10 ** rng.uniform(lo, hi) for _ in range(10000)])
    total = 0
    if construction == "A":
        L = np.searchsorted(POS_MOTIFS_SORTED, samples / (1 + TOL), side="left")
        R = np.searchsorted(POS_MOTIFS_SORTED, samples / (1 - TOL), side="right")
        total = int(np.sum(R - L))
        C = C_A
    else:  # B
        for k in KLIST:
            t = samples * PHI ** k
            L = np.searchsorted(TARGET_VALS, t / (1 + TOL), side="left")
            R = np.searchsorted(TARGET_VALS, t / (1 - TOL), side="right")
            total += int(np.sum(R - L))
        C = C_B
    rate = total / 10000.0 / C
    null_cache[key] = (rate, total)
    return null_cache[key]

print()
survivors = []
for (qn, qv, cons, expr, mn, mv, d) in sorted(raw_hits, key=lambda h: h[6]):
    rate, tot = null_rate(qv, cons)
    exp_false = n_trials * rate
    print(f"[{cons}] {expr:45s} motif={mv:.10g} rel_dev={d:.6f} "
          f"null_total={tot} per-comp-rate={rate:.3e} expected_false={exp_false:.2f}"
          f"{'  << SURVIVES' if exp_false < 0.5 else ''}")
    if exp_false < 0.5:
        survivors.append((qn, qv, cons, expr, mn, mv, d, exp_false))

print()
print(f"survivors (expected_false < 0.5): {len(survivors)}")
for s in survivors:
    print(s)
