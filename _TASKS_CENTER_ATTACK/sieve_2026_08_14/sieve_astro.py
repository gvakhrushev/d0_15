#!/usr/bin/env python3
"""D0 SIEVE agent - family 'astro'. Deterministic motif scan.

Quantities: physical/measured/fitted values only, from
08_PASSPORTS/{SPARC,GWOSC_LIGO,GWOSC,BlackHoleCapacity,CriticalCollapseDSS}.
Excluded: counts, indices, hashes, timestamps, tolerances/config, D0-side
predicted/model columns (loss_frac_d0, loss_frac_spin_only, residual,
d0_shape_response, target_archive_accel, the model-generated q=phi^alpha
column in the MERS sweep, all RMSE/correlation/score fit-statistics).

Constructions (per protocol):
  A) q vs motif m directly (motif library below)
  B) q*phi^k, k in [-17..17] (q/phi^k is the same set) vs
     reduced rationals p/r with 1<=p,r<=60, and vs Lucas/Fibonacci members
     and owned integer invariants {206,359,960,1287,2574} beyond 60.
  C) same-unit within-record physical ratios (mass ratio, Mf/Mtot,
     velocity-component ratios, radius_max/radius_min) treated as
     quantities and scanned with A+B.
Tolerance: rel dev < 0.5%.
Null control: per (construction class, decade bucket), 10000 log-uniform
samples over one decade around the quantity, seed derived from 20260814.
expected_false_hits = n_trials_total * (null_hits / 10000 / comparisons_per_value).
Survivor threshold: expected_false_hits < 0.5.
"""
import csv, json, math, os
import numpy as np

ROOT = "/Users/grigorijvahrusev/Downloads/d0_15/.claude/worktrees/theory-next-level-b57173"
PHI = (1.0 + math.sqrt(5.0)) / 2.0
TOL = 0.005
SEED = 20260814

# ---------------- motif library ----------------
LUCAS = [1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571]
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]

direct = {}  # value -> label (dedup by value, first label wins)
def add(v, lab):
    key = round(v, 12)
    if key not in direct and v > 0:
        direct[key] = (v, lab)

for k in range(-17, 18):
    add(PHI**k, f"phi^{k}")
for n, L in enumerate(LUCAS):
    add(float(L), f"L_{n+1}={L}")
for F in sorted(set(FIB)):
    add(float(F), f"F={F}")
for v, lab in [(9, "9"), (11, "11"), (13, "13"), (33, "33"), (359, "359=|E|"),
               (1287, "1287=9*11*13"), (960, "960"), (2574, "2574"),
               (359 / PHI**2, "359/phi^2"), (12/5, "12/5"),
               (359/160, "359/160"), (20, "20"), (44, "44"), (206, "206"),
               (15, "15"), (8, "8"), (10, "10"), (12, "12"),
               (1/math.sqrt(20), "1/sqrt(20)"), (PHI**-3/2, "delta0=phi^-3/2 [POST-HOC family-suspect]"),
               (6, "6=|S3|"), (24, "24"), (48, "48")]:
    add(float(v), lab)

_dpairs = sorted(direct.values(), key=lambda t: t[0])
direct_vals = np.array([v for v, _ in _dpairs])
direct_labs = [lab for _, lab in _dpairs]
N_DIRECT = len(direct_vals)

# sweep candidate set: reduced p/r (1..60 x 1..60) + Lucas/Fib>60 + owned big integers
sweep = {}
for p in range(1, 61):
    for r in range(1, 61):
        if math.gcd(p, r) == 1:
            v = p / r
            key = round(v, 12)
            if key not in sweep:
                sweep[key] = (v, f"{p}/{r}")
for L in LUCAS:
    key = round(float(L), 12)
    if key not in sweep:
        sweep[key] = (float(L), f"Lucas {L}")
for F in set(FIB):
    key = round(float(F), 12)
    if key not in sweep:
        sweep[key] = (float(F), f"Fib {F}")
for I in [206, 359, 960, 1287, 2574]:
    key = round(float(I), 12)
    if key not in sweep:
        sweep[key] = (float(I), f"int {I}")
_spairs = sorted(sweep.values(), key=lambda t: t[0])
sweep_vals = np.array([v for v, _ in _spairs])
sweep_labs = [lab for _, lab in _spairs]
N_SWEEP = len(sweep_vals)
KS = list(range(-17, 18))
PHIK = np.array([PHI**k for k in KS])

C_DIRECT = N_DIRECT
C_SWEEP = len(KS) * N_SWEEP
C_PER_Q = C_DIRECT + C_SWEEP

# ---------------- quantity extraction ----------------
Q = []  # dicts: file, name, value, negflag

def addq(f, name, v, neg=False):
    if v is None:
        return
    try:
        v = float(v)
    except (TypeError, ValueError):
        return
    if not math.isfinite(v) or v == 0.0:
        return
    if v < 0:
        Q.append(dict(file=f, name=name, value=-v, neg=True))
    else:
        Q.append(dict(file=f, name=name, value=v, neg=neg))

# --- GWOSC mass defect (clean + anomalies): measured side only
for rel in ["08_PASSPORTS/GWOSC/ligo_current_mass_defect_results.csv",
            "08_PASSPORTS/GWOSC/ligo_current_mass_defect_anomalies.csv"]:
    with open(os.path.join(ROOT, rel)) as fh:
        for row in csv.DictReader(fh):
            ev = row["event_name"]
            m1 = float(row["m1_source"]); m2 = float(row["m2_source"])
            mf = float(row["final_mass_source"])
            addq(rel, f"{ev}.m1_source", m1)
            addq(rel, f"{ev}.m2_source", m2)
            addq(rel, f"{ev}.final_mass_source", mf)
            addq(rel, f"{ev}.chi_eff", row["chi_eff"])
            addq(rel, f"{ev}.eta", row["eta"])
            addq(rel, f"{ev}.loss_frac_obs", row["loss_frac_obs"])
            if m2 > 0:
                addq(rel, f"{ev}.mass_ratio_m1_over_m2", m1 / m2)
            if m1 + m2 > 0 and mf > 0:
                addq(rel, f"{ev}.Mf_over_Mtot", mf / (m1 + m2))

# --- MERS_V10 fitted population alpha (grid-fitted parameter)
addq("08_PASSPORTS/GWOSC_LIGO/MERS_V10/mers_v10_report.json", "best_alpha", 0.605)

# --- SPARC phason halo rotation-curve table
seen_dist = set()
rel = "08_PASSPORTS/SPARC/sparc_phason_halo_results.csv"
with open(os.path.join(ROOT, rel)) as fh:
    for i, row in enumerate(csv.DictReader(fh)):
        g = row["galaxy_id"]
        if g not in seen_dist:
            seen_dist.add(g)
            addq(rel, f"{g}.distance_mpc", row["distance_mpc"])
        r_ = float(row["radius_kpc"]); vo = float(row["v_obs"])
        vg = float(row["v_gas"]); vd = float(row["v_disk"])
        vb = float(row["v_bulge"]); vbar = float(row["v_baryon_ml1"])
        tag = f"{g}.r{i}"
        addq(rel, f"{tag}.radius_kpc", r_)
        addq(rel, f"{tag}.v_obs", vo)
        addq(rel, f"{tag}.v_gas", vg)
        addq(rel, f"{tag}.v_disk", vd)
        addq(rel, f"{tag}.v_bulge", vb)
        addq(rel, f"{tag}.v_baryon_ml1", vbar)
        if vo > 0:
            if vg != 0: addq(rel, f"{tag}.vgas_over_vobs", abs(vg) / vo)
            if vd != 0: addq(rel, f"{tag}.vdisk_over_vobs", abs(vd) / vo)
            if vb > 0: addq(rel, f"{tag}.vbulge_over_vobs", vb / vo)
            if vbar > 0: addq(rel, f"{tag}.vbaryon_over_vobs", vbar / vo)
        if vd > 0 and vg > 0:
            addq(rel, f"{tag}.vgas_over_vdisk", vg / vd)

# --- SPARC failure diagnostics (per-galaxy physical / physically defined)
rel = "08_PASSPORTS/SPARC/sparc_failure_diagnostics.csv"
with open(os.path.join(ROOT, rel)) as fh:
    for row in csv.DictReader(fh):
        g = row["galaxy"]
        rmin = float(row["radius_min"]); rmax = float(row["radius_max"])
        addq(rel, f"{g}.radius_min", rmin)
        addq(rel, f"{g}.radius_max", rmax)
        addq(rel, f"{g}.gas_fraction_proxy", row["gas_fraction_proxy"])
        addq(rel, f"{g}.disk_fraction_proxy", row["disk_fraction_proxy"])
        addq(rel, f"{g}.surface_brightness_proxy", row["surface_brightness_proxy"])
        if rmin > 0:
            addq(rel, f"{g}.rmax_over_rmin", rmax / rmin)

# --- SPARC phason halo summary: fitted global gamma
addq("08_PASSPORTS/SPARC/sparc_phason_halo_summary.json", "global_gamma", 0.01250849213199194)

NQ = len(Q)
vals = np.array([q["value"] for q in Q])
n_trials_total = NQ * C_PER_Q

# ---------------- scan ----------------
def match_sorted(xs, grid):
    """return (idx_of_matching_grid_entry or -1, reldev) for each x, nearest grid entry"""
    j = np.searchsorted(grid, xs)
    j0 = np.clip(j - 1, 0, len(grid) - 1)
    j1 = np.clip(j, 0, len(grid) - 1)
    d0 = np.abs(xs / grid[j0] - 1.0)
    d1 = np.abs(xs / grid[j1] - 1.0)
    take1 = d1 < d0
    jj = np.where(take1, j1, j0)
    dd = np.where(take1, d1, d0)
    return jj, dd

raw_hits = []  # (qi, class, k or None, cand_idx, reldev)
# class A: direct
jj, dd = match_sorted(vals, direct_vals)
for qi in np.nonzero(dd < TOL)[0]:
    raw_hits.append((int(qi), "direct", None, int(jj[qi]), float(dd[qi])))
# class B: phi^k sweep vs sweep set
for ki, pk in enumerate(PHIK):
    xs = vals * pk
    jj, dd = match_sorted(xs, sweep_vals)
    for qi in np.nonzero(dd < TOL)[0]:
        raw_hits.append((int(qi), "sweep", KS[ki], int(jj[qi]), float(dd[qi])))

# ---------------- null control ----------------
def count_hits_multi(xs, grid):
    """total number of grid entries within TOL of each x, summed"""
    lo = np.searchsorted(grid, xs / (1 + TOL), side="left")
    hi = np.searchsorted(grid, xs / (1 - TOL), side="right")
    return int(np.sum(hi - lo))

null_cache = {}
def null_rate(cls, value):
    kb = int(round(math.log10(value) * 10))  # 0.1-decade bucket
    key = (cls, kb)
    if key in null_cache:
        return null_cache[key]
    seed = SEED * 1000 + (kb + 500) * 7 + (1 if cls == "sweep" else 0)
    rng = np.random.default_rng(seed)
    center = kb / 10.0
    xs = 10.0 ** rng.uniform(center - 0.5, center + 0.5, 10000)
    if cls == "direct":
        nh = count_hits_multi(xs, direct_vals)
        C = C_DIRECT
    else:
        nh = 0
        for pk in PHIK:
            nh += count_hits_multi(xs * pk, sweep_vals)
        C = C_SWEEP
    p_single = nh / 10000.0 / C
    null_cache[key] = (p_single, nh)
    return null_cache[key]

# evaluate every raw hit
survivors = []
best_by_class = {}
for (qi, cls, k, ci, dev) in raw_hits:
    q = Q[qi]
    p_single, nh = null_rate(cls, q["value"])
    ef = n_trials_total * p_single
    rec = (ef, dev, qi, cls, k, ci, nh)
    if ef < 0.5:
        survivors.append(rec)
    key = cls
    if key not in best_by_class or ef < best_by_class[key][0]:
        best_by_class[key] = rec
# also track globally minimal expected_false and tightest raw deviations
raw_sorted_by_dev = sorted(raw_hits, key=lambda t: t[4])[:10]

def hit_dict(rec):
    ef, dev, qi, cls, k, ci, nh = rec
    q = Q[qi]
    if cls == "direct":
        expr = f"q vs {direct_labs[ci]}"
        mval = float(direct_vals[ci])
    else:
        expr = f"q*phi^{k} vs {sweep_labs[ci]}"
        mval = float(sweep_vals[ci])
    return dict(file=q["file"], quantity=q["name"] + (" (abs of negative)" if q["neg"] else ""),
                value=q["value"], motif_expr=expr, motif_value=mval,
                rel_dev=dev, expected_false_hits=ef)

out = dict(
    n_quantities=NQ,
    n_trials_total=n_trials_total,
    n_direct_candidates=N_DIRECT,
    n_sweep_candidates=N_SWEEP,
    comparisons_per_quantity=C_PER_Q,
    n_raw_hits=len(raw_hits),
    n_raw_hits_direct=sum(1 for h in raw_hits if h[1] == "direct"),
    n_raw_hits_sweep=sum(1 for h in raw_hits if h[1] == "sweep"),
    n_survivors=len(survivors),
    survivors=[hit_dict(r) for r in sorted(survivors)[:32]],
    best_per_class={cls: hit_dict(rec) for cls, rec in best_by_class.items()},
    tightest_raw=[
        dict(hit_dict((0.0, dev, qi, cls, k, ci, 0)), expected_false_hits=None)
        for (qi, cls, k, ci, dev) in raw_sorted_by_dev
    ],
    min_expected_false=min((r[0] for r in
                            [(n_trials_total * null_rate(cls, Q[qi]["value"])[0], dev, qi, cls, k, ci, 0)
                             for (qi, cls, k, ci, dev) in raw_hits]), default=None),
)
print(json.dumps(out, indent=1))
