#!/usr/bin/env python3
"""SIEVE scan, family: internal-spectra. Deterministic. Seed 20260814.

Quantities:
  - d0_gap_labels.json: 25 lower_bound + 25 upper_bound (spectral band edges).
    (ids / trace_val plateaux are KNOWN-MATCH EXCLUDED: Z+Z/phi plateaux, N6/R1.)
  - VacuumFeedback/finite_feedback_equation_of_state_summary.json: pressure=0.1875
  - VacuumFeedback/feedback_partition_function_summary.json: logZ=0.18252898675132667

Constructions:
  A: q vs motif m directly (rel dev = |q-m|/|m| < 0.005)
  B: q*phi^k, k in [-17..17], vs rationals p/r (|p|,r<=60) and Lucas/Fib integers
  C: ratios q_i/q_j of same-unit pairs (the 50 band edges) vs motifs
     (C-hits on motif phi^k are EXCLUDED as module-generic gap-ladder, N6/R1)

Null: per quantity, 10000 log-uniform random values over one decade around |q|
(same sign), same construction scan (A+B). Per-comparison null rate =
null_hits/(10000*cpv). expected_false_hits = n_trials_total * rate.
For C hits: null on the ratio value vs motif scan (cpv = |motifs|).
"""
import json, math, random, bisect
from fractions import Fraction

PHI = (1 + 5**0.5) / 2
TOL = 0.005
SEED = 20260814
ROOT = "/Users/grigorijvahrusev/Downloads/d0_15/.claude/worktrees/theory-next-level-b57173"

# ---------------- motif library (construction A + C targets) ----------------
motifs = {}  # name -> value
def add(name, val):
    # dedupe by value; keep first name
    key = round(val, 12)
    for n, v in motifs.items():
        if abs(v - val) < 1e-11 * max(1.0, abs(val)):
            return
    motifs[name] = val

for k in range(-17, 18):
    add(f"phi^{k}", PHI**k)
LUCAS = [1,3,4,7,11,18,29,47,76,123,199,322,521,843,1364,2207,3571]
FIB   = [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597]
for L in LUCAS: add(f"L({L})", float(L))
for F in FIB:   add(f"F({F})", float(F))
for name, v in [("9",9),("11",11),("13",13),("33",33),("359",359),
                ("1287",1287),("960",960),("2574",2574),
                ("359/phi^2", 359/PHI**2)]:
    add(name, float(v))
add("12/5", 2.4); add("xi5=phi^-5", PHI**5-11); add("359/160", 359/160)
for name, v in [("20",20),("44",44),("206",206),("15",15),
                ("1/sqrt20", 1/math.sqrt(20)), ("3/5-phi", 0.6-PHI)]:
    add(name, float(v))
add("delta0=phi^-3/2", PHI**-3/2)   # POST-HOC family -> flag
for g in [6,8,24,48]: add(f"group|{g}|", float(g))
# toral traces Tr T^n = (-1)^n L_n: adds negative odd-index Lucas
for i, L in enumerate(LUCAS, start=1):
    if i % 2 == 1: add(f"TrT^{i}=-L({L})", -float(L))
add("set{8,10,12}:10", 10.0); add("set{8,10,12}:12", 12.0)

motif_items = sorted(motifs.items(), key=lambda kv: kv[1])
motif_vals  = [v for _, v in motif_items]
motif_names = [n for n, _ in motif_items]
M_A = len(motif_vals)

# ---------------- construction-B target grid ----------------
grid = {}
for r in range(1, 61):
    for p in range(-60, 61):
        if p == 0: continue
        f = Fraction(p, r)
        key = (f.numerator, f.denominator)
        if key not in grid:
            grid[key] = (float(f), f"{f.numerator}/{f.denominator}")
for L in LUCAS:
    if L > 60: grid[(L,1)] = (float(L), f"L({L})")
for F in FIB:
    if F > 60 and (F,1) not in grid: grid[(F,1)] = (float(F), f"F({F})")
btargets = sorted(grid.values())
bvals  = [v for v, _ in btargets]
bnames = [n for _, n in btargets]
N_B = len(bvals)
KS = list(range(-17, 18))

def scan_sorted(x, vals, tol=TOL):
    """indices of vals within relative tol of x (rel dev = |x-v|/|v|)."""
    out = []
    lo = bisect.bisect_left(vals, x / (1 + tol) if x >= 0 else x * (1 + tol))
    i = max(0, lo - 2)
    while i < len(vals):
        v = vals[i]
        if v != 0 and abs(x - v) / abs(v) < tol:
            out.append(i)
        if v > x * (1 + 2*tol) + 1e-9 and v > 0 and x > 0: break
        if x < 0 and v > 0: break
        i += 1
        if i - lo > 400: break
    return out

def scan_all(x):
    """full A+B scan of one value; returns list of hits (cls, kexp, idx, reldev)."""
    hits = []
    for i in scan_sorted(x, motif_vals):
        hits.append(("A", 0, i, abs(x - motif_vals[i]) / abs(motif_vals[i])))
    for k in KS:
        s = x * PHI**k
        for i in scan_sorted(s, bvals):
            hits.append(("B", k, i, abs(s - bvals[i]) / abs(bvals[i])))
    return hits

# ---------------- load quantities ----------------
quantities = []  # (file, name, value)
gl = json.load(open(f"{ROOT}/d0_gap_labels.json"))
for row in gl:
    quantities.append(("d0_gap_labels.json", f"gap{row['gap_idx']}_lower_bound", row["lower_bound"]))
    quantities.append(("d0_gap_labels.json", f"gap{row['gap_idx']}_upper_bound", row["upper_bound"]))
eos = json.load(open(f"{ROOT}/08_PASSPORTS/VacuumFeedback/finite_feedback_equation_of_state_summary.json"))
quantities.append(("08_PASSPORTS/VacuumFeedback/finite_feedback_equation_of_state_summary.json",
                   "pressure", eos["pressure"]))
pf = json.load(open(f"{ROOT}/08_PASSPORTS/VacuumFeedback/feedback_partition_function_summary.json"))
quantities.append(("08_PASSPORTS/VacuumFeedback/feedback_partition_function_summary.json",
                   "logZ", pf["logZ"]))
NQ = len(quantities)

# same-unit set for ratios: the 50 band edges
edge_idx = [i for i, (f, n, v) in enumerate(quantities) if "bound" in n]

# ---------------- real scan ----------------
cpv_AB = M_A + len(KS) * N_B
raw_hits = []
n_trials = 0
for qi, (fname, qname, qv) in enumerate(quantities):
    n_trials += cpv_AB
    for cls, k, i, rd in scan_all(qv):
        if cls == "A":
            raw_hits.append((fname, qname, qv, f"{motif_names[i]}", motif_vals[i], rd, "A", qi))
        else:
            expr = f"q*phi^{k} vs {bnames[i]}" if k != 0 else f"q vs {bnames[i]}"
            raw_hits.append((fname, qname, qv, expr, bvals[i], rd, "B", qi))

# construction C: ratios among band edges vs motifs
ratio_hits = []
n_ratio_pairs = 0
for a in edge_idx:
    for b in edge_idx:
        if a == b: continue
        n_ratio_pairs += 1
        n_trials += M_A
        r = quantities[a][2] / quantities[b][2]
        for i in scan_sorted(r, motif_vals):
            rd = abs(r - motif_vals[i]) / abs(motif_vals[i])
            ratio_hits.append((quantities[a][1], quantities[b][1], r,
                               motif_names[i], motif_vals[i], rd))

# ---------------- null control ----------------
rng = random.Random(SEED)
NNULL = 10000
null_rate_per_q = {}
for qi, (fname, qname, qv) in enumerate(quantities):
    lo, hi = abs(qv) / math.sqrt(10), abs(qv) * math.sqrt(10)
    sgn = 1.0 if qv >= 0 else -1.0
    tot = 0
    for _ in range(NNULL):
        x = sgn * math.exp(rng.uniform(math.log(lo), math.log(hi)))
        tot += len(scan_all(x))
    null_rate_per_q[qi] = tot / (NNULL * cpv_AB)

# null for ratio-hit values: motif-only scan
def null_rate_ratio(rv):
    lo, hi = abs(rv) / math.sqrt(10), abs(rv) * math.sqrt(10)
    sgn = 1.0 if rv >= 0 else -1.0
    tot = 0
    r2 = random.Random(SEED + 999)
    for _ in range(NNULL):
        x = sgn * math.exp(r2.uniform(math.log(lo), math.log(hi)))
        tot += len(scan_sorted(x, motif_vals))
    return tot / (NNULL * M_A)

# ---------------- report ----------------
print(f"N_quantities={NQ}  M_A={M_A}  N_B={N_B}  cpv_AB={cpv_AB}")
print(f"n_ratio_pairs={n_ratio_pairs}")
print(f"n_trials_total={n_trials}")
print(f"raw AB hits: {len(raw_hits)}   raw C hits: {len(ratio_hits)}")

# best hit per (quantity, class) for readability; survivors filter
print("\n--- A-class raw hits (direct motif) ---")
for h in raw_hits:
    if h[6] == "A":
        rate = null_rate_per_q[h[7]]
        efh = n_trials * rate
        print(f"{h[1]}={h[2]}  vs {h[3]}={h[4]:.6f}  reldev={h[5]:.5f}  "
              f"null_rate={rate:.3e}  expected_false_hits={efh:.1f}")

print("\n--- B-class raw hits: only reldev < 0.0005 shown (10x tighter than tol) ---")
tight = [h for h in raw_hits if h[6] == "B" and h[5] < 0.0005]
for h in sorted(tight, key=lambda h: h[5])[:40]:
    rate = null_rate_per_q[h[7]]
    efh = n_trials * rate
    print(f"{h[1]}={h[2]}  {h[3]}  target={h[4]:.6f}  reldev={h[5]:.2e}  "
          f"expected_false_hits={efh:.1f}")

print("\n--- C-class raw hits (ratios vs motifs), phi^k flagged as gap-ladder-excluded ---")
seen = set()
for h in sorted(ratio_hits, key=lambda h: h[5]):
    keyt = (h[3],)
    tag = "EXCLUDED(gap-ladder N6/R1)" if h[3].startswith("phi^") else "candidate"
    if h[5] < 0.001 or tag == "candidate":
        k2 = (h[0], h[1], h[3])
        if k2 in seen: continue
        seen.add(k2)
        print(f"{h[0]}/{h[1]}={h[2]:.6f} vs {h[3]}={h[4]:.6f} reldev={h[5]:.5f}  [{tag}]")

# survivors per protocol formula
print("\n--- protocol survivors (expected_false_hits < 0.5) ---")
surv = []
for h in raw_hits:
    rate = null_rate_per_q[h[7]]
    efh = n_trials * rate
    if efh < 0.5:
        surv.append((h, efh))
        print(h, efh)
cand_ratio = [h for h in ratio_hits if not h[3].startswith("phi^")]
for h in cand_ratio:
    rate = null_rate_ratio(h[2])
    efh = n_trials * rate
    if efh < 0.5:
        surv.append((h, efh))
        print("C:", h, efh)
if not surv:
    print("(none)")

# summary of average null rates
import statistics
print("\navg null rate per comparison:", statistics.mean(null_rate_per_q.values()))
print("min null-rate expected_false_hits over quantities:",
      min(null_rate_per_q.values()) * n_trials)
