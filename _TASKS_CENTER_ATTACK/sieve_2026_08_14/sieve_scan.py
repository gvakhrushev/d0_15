#!/usr/bin/env python3
"""D0 SIEVE scan - family: neutrino-nuclear.
Deterministic. Seed 20260814 for null control.
Dirs: 08_PASSPORTS/IceCube, 08_PASSPORTS/NuclearSRC, 08_PASSPORTS/BaryonAsymmetry
"""
import csv, json, math
import numpy as np
from math import gcd

ROOT = "/Users/grigorijvahrusev/Downloads/d0_15/.claude/worktrees/theory-next-level-b57173"
PHI = (1 + 5**0.5) / 2
TOL = 0.005
SEED = 20260814

# ---------------- motif library (direct comparisons) ----------------
motif_vals = []
motif_labels = []
_seen = {}
def add_motif(v, lab):
    key = round(float(v), 12)
    if key in _seen:
        return
    _seen[key] = lab
    motif_vals.append(float(v))
    motif_labels.append(lab)

for k in range(-17, 18):
    add_motif(PHI**k, f"phi^{k}")
LUCAS = [1,3,4,7,11,18,29,47,76,123,199,322,521,843,1364,2207,3571]
FIB   = [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597]
for i, L in enumerate(LUCAS, 1): add_motif(L, f"L_{i}={L}")
for i, F in enumerate(FIB, 1):   add_motif(F, f"F_{i}={F}")
for v, lab in [(9,"9"),(11,"11"),(13,"13"),(33,"33"),(359,"359=|E|"),
               (1287,"1287"),(960,"960"),(2574,"2574"),
               (359/PHI**2,"359/phi^2")]:
    add_motif(v, lab)
add_motif(12/5, "12/5")
add_motif(PHI**5 - 11, "xi5=phi^-5")
add_motif(359/160, "359/160")
for v, lab in [(20,"20"),(44,"44"),(206,"206"),(15,"15"),(8,"8"),(10,"10"),(12,"12")]:
    add_motif(v, lab)
add_motif(1/20**0.5, "1/sqrt(20)")
add_motif(3/5 - PHI, "w=3/5-phi")
add_motif(PHI**-3/2, "delta0=phi^-3/2")   # POST-HOC family -> flag
for v, lab in [(6,"6=|S3|"),(24,"24"),(48,"48")]:
    add_motif(v, lab)
for n in range(1, 18):  # toral traces (-1)^n L_n ; odd n adds negatives
    add_motif(((-1)**n) * LUCAS[n-1], f"TrT^{n}=(-1)^{n}L_{n}")
MV = np.array(motif_vals)
N_MOTIF = len(MV)

# ---------------- scaled-comparison target grid ----------------
# reduced fractions p/r, 1<=p,r<=60  (integers<=60 included via r=1)
grid_vals, grid_labels = [], []
for r in range(1, 61):
    for p in range(1, 61):
        if gcd(p, r) == 1:
            grid_vals.append(p / r)
            grid_labels.append(f"{p}/{r}" if r > 1 else f"{p}")
for L in LUCAS:
    if L > 60:
        grid_vals.append(float(L)); grid_labels.append(f"Lucas {L}")
for F in FIB:
    if F > 60:
        grid_vals.append(float(F)); grid_labels.append(f"Fib {F}")
GV = np.array(grid_vals)
N_GRID = len(GV)
KS = np.arange(-17, 18)
PHIK = PHI ** KS.astype(float)
N_K = len(KS)

# ---------------- quantities ----------------
# (file, name, value, class)  class: "full" = direct + phi^k sweeps ; "ratio" = direct motifs only
quantities = []
f_curve = "08_PASSPORTS/IceCube/icecube_phason_decoherence_curve.csv"
energies = []
with open(f"{ROOT}/{f_curve}") as fh:
    for row in csv.DictReader(fh):
        e = float(row["energy"]); ra = float(row["ra"]); dec = float(row["dec"])
        i = row["id"]
        energies.append((i, e))
        quantities.append((f_curve, f"energy[id={i}]", e, "full"))
        quantities.append((f_curve, f"ra[id={i}]", ra, "full"))
        quantities.append((f_curve, f"dec[id={i}]", dec, "full"))
        # gamma_d0, damping_d0 EXCLUDED: D0-predicted side

f_sum = "08_PASSPORTS/IceCube/icecube_hese_baseline_summary.json"
with open(f"{ROOT}/{f_sum}") as fh:
    S = json.load(fh)
quantities.append((f_sum, "mu_null_high", S["mu_null_high"], "full"))
quantities.append((f_sum, "poisson_loglik_null", S["poisson_loglik_null"], "full"))
quantities.append((f_sum, "chi2_null_high", S["chi2_null_high"], "full"))
quantities.append((f_sum, "topology_ratio_metric", S["topology_ratio_metric"], "full"))
# excluded: events_used, high_bin_obs (counts); bins edges (config, derived);
# mu_d0_high, avg_damping_high, *_d0, delta_* (D0 side)

# Nuclear SRC: A/Z/N are nucleon counts (excluded as counts); include standard
# physically-defined non-trivial ratios only. neutron-excess ratios excluded
# (integer-count artifact; 8/2=4 would fake an exact Lucas hit).
f_src = "08_PASSPORTS/NuclearSRC/nature2026_src_results.csv"
nuc = {}
with open(f"{ROOT}/{f_src}") as fh:
    for row in csv.DictReader(fh):
        nuc[row["label"]] = {k: float(row[k]) for k in ("A","Z","N","neutron_excess")}
nuclear_ratios = [
    ("N/Z(Ca-48)",  nuc["Ca-48"]["N"]/nuc["Ca-48"]["Z"]),
    ("N/Z(Fe-54)",  nuc["Fe-54"]["N"]/nuc["Fe-54"]["Z"]),
    ("A(Ca-48)/A(Ca-40)", nuc["Ca-48"]["A"]/nuc["Ca-40"]["A"]),
    ("A(Fe-54)/A(Ca-40)", nuc["Fe-54"]["A"]/nuc["Ca-40"]["A"]),
    ("A(Fe-54)/A(Ca-48)", nuc["Fe-54"]["A"]/nuc["Ca-48"]["A"]),
    ("Z(Fe-54)/Z(Ca-40)", nuc["Fe-54"]["Z"]/nuc["Ca-40"]["Z"]),
    ("N(Ca-48)/N(Ca-40)", nuc["Ca-48"]["N"]/nuc["Ca-40"]["N"]),
]
for name, v in nuclear_ratios:
    if abs(v - 1.0) > 1e-12:   # skip trivial identity ratios
        quantities.append((f_src, name, v, "ratio"))

# Energy pairwise ratios (same-unit, within family): larger/smaller
n_e = len(energies)
for a in range(n_e):
    for b in range(a+1, n_e):
        ia, ea = energies[a]; ib, eb = energies[b]
        if ea >= eb:
            quantities.append((f_curve, f"E[{ia}]/E[{ib}]", ea/eb, "ratio"))
        else:
            quantities.append((f_curve, f"E[{ib}]/E[{ia}]", eb/ea, "ratio"))

n_full  = sum(1 for q in quantities if q[3] == "full")
n_ratio = sum(1 for q in quantities if q[3] == "ratio")

# ---------------- scan ----------------
n_trials = 0
raw_hit_count = 0
candidates = []   # (file, name, value, construction, motif_expr, motif_val, dev)
CAND_TOL = 1e-6   # anything above cannot survive null (bound ~0.87*dev*n_trials)

for (fname, qname, qval, klass) in quantities:
    # direct vs motifs (signed)
    devs = np.abs(qval - MV) / np.abs(MV)
    n_trials += N_MOTIF
    nh = int((devs < TOL).sum())
    raw_hit_count += nh
    if nh:
        for idx in np.where(devs < CAND_TOL)[0]:
            candidates.append((fname, qname, qval, "direct", motif_labels[idx], MV[idx], float(devs[idx])))
    if klass == "full":
        x = abs(qval) * PHIK                     # 35 scaled values
        d2 = np.abs(x[:, None] - GV[None, :]) / GV[None, :]
        n_trials += N_K * N_GRID
        m = d2 < TOL
        raw_hit_count += int(m.sum())
        cand = np.argwhere(d2 < CAND_TOL)
        for (ki, gi) in cand:
            sign = "" if qval >= 0 else "-"
            expr = f"|q|*phi^{KS[ki]} = {sign and '(-q)' or 'q'}*phi^{KS[ki]} vs {grid_labels[gi]}"
            candidates.append((fname, qname, qval, f"scaled_k={KS[ki]}", f"phi^{-KS[ki]}*({grid_labels[gi]})", GV[gi] * PHI**(-float(KS[ki])), float(d2[ki, gi])))

print(f"n_quantities_full={n_full}  n_quantities_ratio={n_ratio}")
print(f"N_MOTIF={N_MOTIF}  N_GRID={N_GRID}  N_K={N_K}")
print(f"n_trials_total={n_trials}")
print(f"raw_hits_at_0.5pct={raw_hit_count}")
print(f"candidates dev<{CAND_TOL}: {len(candidates)}")
candidates.sort(key=lambda c: c[6])
for c in candidates[:40]:
    print("  CAND", c[0].split('/')[-1], c[1], f"val={c[2]:.10g}", c[3], c[4], f"target={c[5]:.10g}", f"dev={c[6]:.3e}")

# ---------------- null control for candidates ----------------
# For each candidate: 10000 log-uniform values over one decade around the
# quantity, seed 20260814, same construction scan, threshold = observed dev.
# expected_false_hits = n_trials_total * (null_hits / 10000 / comparisons_per_value)
survivors = []
NULLN = 10000
for (fname, qname, qval, constr, mexpr, mval, dev) in candidates:
    rng = np.random.default_rng(SEED)
    lo = math.log10(abs(qval)) - 0.5
    vals = 10 ** rng.uniform(lo, lo + 1.0, NULLN)
    if constr == "direct":
        comparisons_per_value = N_MOTIF
        nd = np.abs(vals[:, None] - np.abs(MV)[None, :]) / np.abs(MV)[None, :]
        null_hits = int((nd <= dev).sum())
    else:
        comparisons_per_value = N_K * N_GRID
        null_hits = 0
        for ki in range(N_K):
            xv = vals * PHIK[ki]
            nd = np.abs(xv[:, None] - GV[None, :]) / GV[None, :]
            null_hits += int((nd <= dev).sum())
    rate = null_hits / NULLN / comparisons_per_value
    efh = n_trials * rate
    print(f"NULL {qname} {constr} {mexpr} dev={dev:.3e} null_hits={null_hits} rate={rate:.3e} expected_false={efh:.3f}")
    if efh < 0.5:
        survivors.append(dict(file=fname, quantity=qname, value=qval,
                              motif_expr=mexpr, motif_value=float(mval),
                              rel_dev=dev, expected_false_hits=efh))

print("\nSURVIVORS:", json.dumps(survivors, indent=1))

# analytic sanity: survival bound dev < 0.5/(0.87*n_trials)
print(f"analytic survival bound dev < {0.5/(2/math.log(10)*n_trials):.3e}")

# sharpest overall (even non-surviving) for notes
print("sharpest 5 candidate devs:", [f"{c[6]:.2e}" for c in candidates[:5]])
