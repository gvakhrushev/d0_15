#!/usr/bin/env python3
"""SIEVE scan v2 (vectorized), family: internal-spectra. Deterministic seed 20260814.

Same semantics as v1:
  A: q vs motif directly, rel dev |q-m|/|m| < 0.005
  B: q*phi^k, k=-17..17, vs rationals p/r (|p|,r<=60) + Lucas/Fib > 60
  C: ratios of same-unit pairs (50 band edges) vs motifs
     (C-hits on phi^k are module-generic gap-ladder statements -> excluded, N6/R1)
Null: 10000 log-uniform values over one decade around |q|, same sign, same scan.
expected_false_hits = n_trials_total * (null_hits / 10000 / cpv).
"""
import json, math
import numpy as np
from fractions import Fraction

PHI = (1 + 5**0.5) / 2
TOL = 0.005
SEED = 20260814
ROOT = "/Users/grigorijvahrusev/Downloads/d0_15/.claude/worktrees/theory-next-level-b57173"

# ---------- motif library ----------
raw = []
for k in range(-17, 18): raw.append((f"phi^{k}", PHI**k))
LUCAS = [1,3,4,7,11,18,29,47,76,123,199,322,521,843,1364,2207,3571]
FIB   = [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597]
raw += [(f"L({L})", float(L)) for L in LUCAS]
raw += [(f"F({F})", float(F)) for F in set(FIB)]
raw += [("9",9.),("11",11.),("13",13.),("33",33.),("359",359.),("1287",1287.),
        ("960",960.),("2574",2574.),("359/phi^2",359/PHI**2),
        ("12/5",2.4),("xi5=phi^-5",PHI**5-11),("359/160",359/160),
        ("20",20.),("44",44.),("206",206.),("15",15.),
        ("1/sqrt20",1/math.sqrt(20)),("3/5-phi",0.6-PHI),
        ("delta0=phi^-3/2",PHI**-3/2),
        ("|S3|=6",6.),("|Q8|=8",8.),("24",24.),("48",48.),("10",10.),("12",12.)]
for i, L in enumerate(LUCAS, start=1):
    if i % 2 == 1: raw.append((f"TrT^{i}=-L({L})", -float(L)))
# dedupe by value
motifs = []
for n, v in raw:
    if not any(abs(v - v2) < 1e-11 * max(1, abs(v)) for _, v2 in motifs):
        motifs.append((n, v))
motifs.sort(key=lambda t: t[1])
mnames = [n for n, _ in motifs]
mvals = np.array([v for _, v in motifs])
M_A = len(mvals)

# ---------- B-grid ----------
grid = {}
for r in range(1, 61):
    for p in range(-60, 61):
        if p == 0: continue
        f = Fraction(p, r)
        grid.setdefault((f.numerator, f.denominator), f"{f.numerator}/{f.denominator}")
for L in LUCAS:
    if L > 60: grid.setdefault((L, 1), f"L({L})")
for F in FIB:
    if F > 60: grid.setdefault((F, 1), f"F({F})")
bitems = sorted(((num/den, nm) for (num, den), nm in grid.items()))
bvals = np.array([v for v, _ in bitems])
bnames = [nm for _, nm in bitems]
N_B = len(bvals)
KS = np.arange(-17, 18)
PHIK = PHI**KS.astype(float)
cpv_AB = M_A + len(KS) * N_B

def count_hits(xs, targets):
    """xs: array of scan values; targets: sorted array. Counts of targets t with
    |x-t|/|t| < TOL. Interval endpoints x/(1+TOL), x/(1-TOL) (order by sign)."""
    a = xs / (1 + TOL); b = xs / (1 - TOL)
    lo = np.minimum(a, b); hi = np.maximum(a, b)
    return np.searchsorted(targets, hi, side="left") - np.searchsorted(targets, lo, side="right")

def enum_hits(x, targets, names):
    a = x / (1 + TOL); b = x / (1 - TOL)
    lo, hi = min(a, b), max(a, b)
    i0 = np.searchsorted(targets, lo, side="right")
    i1 = np.searchsorted(targets, hi, side="left")
    return [(names[i], targets[i], abs(x - targets[i]) / abs(targets[i])) for i in range(i0, i1)]

# ---------- quantities ----------
quantities = []
gl = json.load(open(f"{ROOT}/d0_gap_labels.json"))
for row in gl:
    quantities.append(("d0_gap_labels.json", f"gap{row['gap_idx']}_lower_bound", row["lower_bound"]))
    quantities.append(("d0_gap_labels.json", f"gap{row['gap_idx']}_upper_bound", row["upper_bound"]))
eos = json.load(open(f"{ROOT}/08_PASSPORTS/VacuumFeedback/finite_feedback_equation_of_state_summary.json"))
quantities.append(("08_PASSPORTS/VacuumFeedback/finite_feedback_equation_of_state_summary.json", "pressure", eos["pressure"]))
pf = json.load(open(f"{ROOT}/08_PASSPORTS/VacuumFeedback/feedback_partition_function_summary.json"))
quantities.append(("08_PASSPORTS/VacuumFeedback/feedback_partition_function_summary.json", "logZ", pf["logZ"]))
NQ = len(quantities)
edge_idx = [i for i, (f, n, v) in enumerate(quantities) if "bound" in n]

# ---------- real scan ----------
n_trials = 0
ab_hits = []   # (file, qname, qval, expr, motifval, reldev, class, qi)
for qi, (fn, qn, qv) in enumerate(quantities):
    n_trials += cpv_AB
    for nm, tv, rd in enum_hits(qv, mvals, mnames):
        ab_hits.append((fn, qn, qv, f"q vs {nm}", tv, rd, "A", qi))
    for k in KS:
        s = qv * PHI**int(k)
        for nm, tv, rd in enum_hits(s, bvals, bnames):
            ab_hits.append((fn, qn, qv, f"q*phi^{int(k)} vs {nm}", tv, rd, "B", qi))

c_hits = []
n_pairs = 0
for a in edge_idx:
    for b in edge_idx:
        if a == b: continue
        n_pairs += 1
        n_trials += M_A
        rv = quantities[a][2] / quantities[b][2]
        for nm, tv, rd in enum_hits(rv, mvals, mnames):
            c_hits.append((quantities[a][1], quantities[b][1], rv, nm, tv, rd))

# ---------- null control ----------
rng = np.random.default_rng(SEED)
NN = 10000
null_rate = {}
for qi, (fn, qn, qv) in enumerate(quantities):
    lo, hi = math.log(abs(qv)) - math.log(10)/2, math.log(abs(qv)) + math.log(10)/2
    xs = np.exp(rng.uniform(lo, hi, NN)) * (1 if qv >= 0 else -1)
    tot = count_hits(xs, mvals).sum()
    S = np.outer(xs, PHIK)              # NN x 35
    tot += count_hits(S.ravel(), bvals).sum()
    null_rate[qi] = tot / (NN * cpv_AB)

# ratio null (motif-only scan, cpv = M_A) for each distinct C-hit ratio value
def ratio_null(rv):
    r2 = np.random.default_rng(SEED + 999)
    lo, hi = math.log(abs(rv)) - math.log(10)/2, math.log(abs(rv)) + math.log(10)/2
    xs = np.exp(r2.uniform(lo, hi, NN)) * (1 if rv >= 0 else -1)
    return count_hits(xs, mvals).sum() / (NN * M_A)

# ---------- report ----------
print(f"NQ={NQ} M_A={M_A} N_B={N_B} cpv_AB={cpv_AB} n_pairs={n_pairs}")
print(f"n_trials_total={n_trials}")
print(f"raw AB hits={len(ab_hits)}  raw C hits={len(c_hits)}")

print("\n=== A-class raw hits ===")
for h in ab_hits:
    if h[6] == "A":
        efh = n_trials * null_rate[h[7]]
        print(f"{h[1]}={h[2]} {h[3]}={h[4]:.6g} reldev={h[5]:.5f} EFH={efh:.1f}")

print("\n=== B-class tight hits (reldev<5e-4), sorted ===")
bt = sorted([h for h in ab_hits if h[6] == "B" and h[5] < 5e-4], key=lambda h: h[5])
for h in bt[:50]:
    efh = n_trials * null_rate[h[7]]
    print(f"{h[1]}={h[2]} {h[3]} target={h[4]:.6g} reldev={h[5]:.2e} EFH={efh:.1f}")

print("\n=== C-class non-phi^k hits (candidates) sorted by reldev, top 40 ===")
cc = sorted([h for h in c_hits if not h[3].startswith("phi^")], key=lambda h: h[5])
for h in cc[:40]:
    efh = n_trials * ratio_null(h[2])
    print(f"{h[0]}/{h[1]}={h[2]:.6f} vs {h[3]}={h[4]:.6g} reldev={h[5]:.5f} EFH={efh:.2f}")
n_phik = sum(1 for h in c_hits if h[3].startswith("phi^"))
print(f"(C-hits on phi^k, EXCLUDED as module-generic gap-ladder: {n_phik})")

print("\n=== protocol survivors (EFH < 0.5) ===")
nsurv = 0
for h in ab_hits:
    efh = n_trials * null_rate[h[7]]
    if efh < 0.5:
        nsurv += 1
        print("AB:", h, efh)
for h in cc:
    efh = n_trials * ratio_null(h[2])
    if efh < 0.5:
        nsurv += 1
        print("C:", h, efh)
if nsurv == 0: print("(none)")

rates = np.array(list(null_rate.values()))
print(f"\nnull rate per comparison: mean={rates.mean():.3e} min={rates.min():.3e} max={rates.max():.3e}")
print(f"min EFH over quantities = {rates.min()*n_trials:.1f}")

# refined diagnostics: deviation-based tail p for the tightest hits (informational)
print("\n=== informational: deviation-tail check on tightest B hits ===")
for h in bt[:8]:
    qi = h[7]; qv = h[2]; obs = h[5]
    r3 = np.random.default_rng(SEED + 7)
    lo, hi = math.log(abs(qv)) - math.log(10)/2, math.log(abs(qv)) + math.log(10)/2
    xs = np.exp(r3.uniform(lo, hi, NN)) * (1 if qv >= 0 else -1)
    S = np.outer(xs, PHIK).ravel()
    a = S/(1+obs); b = S/(1-obs)
    lo2 = np.minimum(a,b); hi2 = np.maximum(a,b)
    cnt = (np.searchsorted(bvals, hi2, "left") - np.searchsorted(bvals, lo2, "right")).sum()
    # also motif direct at obs
    a = xs/(1+obs); b = xs/(1-obs)
    cnt += (np.searchsorted(mvals, np.maximum(a,b), "left") - np.searchsorted(mvals, np.minimum(a,b), "right")).sum()
    per_value_p = cnt / NN     # expected hits at <=obs tightness per random value
    print(f"{h[1]} {h[3]} reldev={obs:.2e}: E[hits at this tightness per random value]={per_value_p:.4f}; x NQ={per_value_p*NQ:.2f}")
