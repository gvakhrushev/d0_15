#!/usr/bin/env python3
"""SIEVE agent scan: family 'particles' (PDG mass_width_2025.mcd).

Deterministic. Seed 20260814 for null control.
Protocol: raw hit = rel dev < 0.5%; survivor = expected_false_hits < 0.5
with expected_false_hits = n_trials_total * (null_hits/10000/cpv).
"""
import math, json
import numpy as np
from fractions import Fraction

REPO = "/Users/grigorijvahrusev/Downloads/d0_15/.claude/worktrees/theory-next-level-b57173"
MCD = REPO + "/08_PASSPORTS/PDG/data/mass_width_2025.mcd"
PHI = (1 + math.sqrt(5)) / 2
TOL = 0.005
SEED = 20260814

# ---------------- parse mcd ----------------
masses = []   # (label, value)
widths = []
with open(MCD) as f:
    for line in f:
        if line.startswith('*'):
            continue
        line = line.rstrip('\n')
        mfield = line[33:51].strip()
        wfield = line[70:88].strip() if len(line) > 70 else ''
        name = line[107:128].strip() if len(line) > 107 else '?'
        name = ' '.join(name.split())
        try:
            m = float(mfield)
        except ValueError:
            m = None
        try:
            w = float(wfield) if wfield else None
        except ValueError:
            w = None
        if m is not None and m > 0:
            masses.append((f"m({name})", m))
        if w is not None and w > 0:
            widths.append((f"Gamma({name})", w))

quantities = masses + widths  # base physical quantities, GeV

# ---------------- motif library ----------------
LUCAS = [1,3,4,7,11,18,29,47,76,123,199,322,521,843,1364,2207,3571]
FIB   = [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597]

motif_raw = []
for k in range(-17, 18):
    motif_raw.append((PHI**k, f"phi^{k}", ""))
for L in LUCAS:
    motif_raw.append((float(L), f"L={L}", ""))
for F in set(FIB):
    motif_raw.append((float(F), f"F={F}", ""))
for s in [9,11,13,33,359,1287,960,2574]:
    motif_raw.append((float(s), f"scene:{s}", ""))
motif_raw.append((359/PHI**2, "359/phi^2", ""))
motif_raw.append((12/5, "12/5", ""))
motif_raw.append((PHI**5 - 11, "xi5=phi^-5", ""))          # dup of phi^-5
motif_raw.append((359/160, "359/160", ""))
for s in [20,44,206,15,8,10,12,6,24,48]:
    motif_raw.append((float(s), f"int:{s}", ""))
motif_raw.append((1/math.sqrt(20), "1/sqrt(20)", ""))
motif_raw.append((abs(3/5 - PHI), "|3/5-phi|=1.01803", ""))
motif_raw.append((PHI**-3/2, "delta0=phi^-3/2", "POST-HOC"))

# dedupe by value (rel 1e-9), keep first label, keep POST-HOC flag if any
motif_raw.sort(key=lambda t: t[0])
motifs = []
for v, lab, fl in motif_raw:
    if motifs and abs(v/motifs[-1][0] - 1) < 1e-9:
        if fl and not motifs[-1][2]:
            motifs[-1] = (motifs[-1][0], motifs[-1][1], fl)
        continue
    motifs.append((v, lab, fl))
motif_vals = np.array([m[0] for m in motifs])
motif_labs = [m[1] for m in motifs]
motif_flag = [m[2] for m in motifs]
N_MOTIF = len(motifs)

# ratio motifs: exclude value 1.0 (isospin-partner ratios ~1 are trivial QCD
# degeneracy, not a D0 motif statement)
ridx = [i for i in range(N_MOTIF) if abs(motif_vals[i] - 1.0) > 1e-9]
rmotif_vals = motif_vals[ridx]
rmotif_labs = [motif_labs[i] for i in ridx]
rmotif_flag = [motif_flag[i] for i in ridx]
N_RMOTIF = len(ridx)

# scaled-scan targets: reduced rationals p/r, 1<=p,r<=60, plus Lucas/Fib > 60
targ = set()
for p in range(1, 61):
    for r in range(1, 61):
        targ.add(Fraction(p, r))
targ_list = sorted(targ)
targ_labels = {float(fr): f"{fr.numerator}/{fr.denominator}" for fr in targ_list}
extra_ints = sorted(set([x for x in LUCAS + FIB if x > 60]))
for x in extra_ints:
    if Fraction(x, 1) not in targ:
        targ_labels[float(x)] = f"LF:{x}"
targ_vals = np.array(sorted(targ_labels.keys()))
targ_labs = [targ_labels[v] for v in targ_vals]
N_TARG = len(targ_vals)

KS = np.arange(-17, 18)
PHIK = PHI ** KS.astype(float)
N_K = len(KS)

# ---------------- trials accounting ----------------
N_Q = len(quantities)
trials_direct = N_Q * N_MOTIF
trials_scaled = N_Q * N_K * N_TARG

mass_vals = np.array([v for _, v in masses])
width_vals = np.array([v for _, v in widths])
n_mm = len(masses) * (len(masses) - 1)
n_ww = len(widths) * (len(widths) - 1)
# mass_i/width_i (and inverse) for particles that have both
mname = {lab[2:]: v for lab, v in masses}   # strip "m("
wname = {lab[6:]: v for lab, v in widths}   # strip "Gamma("
both = sorted(set(mname) & set(wname))
n_mw = 2 * len(both)
n_ratios = n_mm + n_ww + n_mw
trials_ratio = n_ratios * N_RMOTIF
n_trials_total = trials_direct + trials_scaled + trials_ratio

# ---------------- scan ----------------
raw_hits = []  # dict: construction, qlabel, qvalue, k, target_label, target_value, motif_label, dev, flag

def scan_direct(qlab, q, vals, labs, flags, cons):
    dev = np.abs(q / vals - 1)
    for i in np.nonzero(dev < TOL)[0]:
        raw_hits.append(dict(construction=cons, qlabel=qlab, qvalue=q,
                             expr=labs[i], mval=float(vals[i]),
                             dev=float(dev[i]), flag=flags[i]))

for qlab, q in quantities:
    scan_direct(qlab, q, motif_vals, motif_labs, motif_flag, "direct")

# scaled: q*phi^k vs rationals/ints
for qlab, q in quantities:
    scaled = q * PHIK
    lo = np.searchsorted(targ_vals, scaled / (1 + TOL), side='left')
    hi = np.searchsorted(targ_vals, scaled / (1 - TOL), side='right')
    for j in range(N_K):
        for i in range(lo[j], hi[j]):
            dev = abs(scaled[j] / targ_vals[i] - 1)
            if dev < TOL:
                raw_hits.append(dict(construction="scaled", qlabel=qlab, qvalue=q,
                                     k=int(KS[j]), expr=f"*phi^{KS[j]} vs {targ_labs[i]}",
                                     mval=float(targ_vals[i]), dev=float(dev), flag=""))

# ratios
def scan_ratio_block(labsA, valsA, labsB, valsB, same_list=False):
    # ordered pairs a/b, a from A, b from B, skip identical index when same_list
    for ia, (la, va) in enumerate(zip(labsA, valsA)):
        r = va / np.asarray(valsB)
        for ib in range(len(valsB)):
            if same_list and ia == ib:
                continue
            rv = r[ib]
            dev = np.abs(rv / rmotif_vals - 1)
            for i in np.nonzero(dev < TOL)[0]:
                raw_hits.append(dict(construction="ratio", qlabel=f"{la}/{labsB[ib]}",
                                     qvalue=float(rv), expr=rmotif_labs[i],
                                     mval=float(rmotif_vals[i]), dev=float(dev[i]),
                                     flag=rmotif_flag[i]))

m_labs = [lab for lab, _ in masses]
w_labs = [lab for lab, _ in widths]
scan_ratio_block(m_labs, mass_vals, m_labs, mass_vals, same_list=True)
scan_ratio_block(w_labs, width_vals, w_labs, width_vals, same_list=True)
for nm in both:
    for rv, lab in [(mname[nm]/wname[nm], f"m({nm}/Gamma({nm})"),
                    (wname[nm]/mname[nm], f"Gamma({nm})/m({nm})")]:
        dev = np.abs(rv / rmotif_vals - 1)
        for i in np.nonzero(dev < TOL)[0]:
            raw_hits.append(dict(construction="ratio", qlabel=lab, qvalue=float(rv),
                                 expr=rmotif_labs[i], mval=float(rmotif_vals[i]),
                                 dev=float(dev[i]), flag=rmotif_flag[i]))

# ---------------- null control ----------------
rng = np.random.default_rng(SEED)
sorted_motifs = np.sort(motif_vals)
sorted_rmotifs = np.sort(rmotif_vals)
null_cache = {}

def null_rate(cons, q):
    key = (cons, round(math.log10(q), 6))
    if key in null_cache:
        return null_cache[key]
    samples = q * 10 ** rng.uniform(-0.5, 0.5, 10000)
    if cons == "direct":
        tv, cpv = sorted_motifs, N_MOTIF
        vals = samples
    elif cons == "ratio":
        tv, cpv = sorted_rmotifs, N_RMOTIF
        vals = samples
    else:  # scaled
        tv, cpv = targ_vals, N_K * N_TARG
        vals = np.outer(samples, PHIK).ravel()
    lo = np.searchsorted(tv, vals / (1 + TOL), side='left')
    hi = np.searchsorted(tv, vals / (1 - TOL), side='right')
    nhits = int(np.sum(hi - lo))
    rate = nhits / 10000 / cpv
    null_cache[key] = rate
    return rate

for h in raw_hits:
    r = null_rate(h["construction"], h["qvalue"])
    h["null_rate"] = r
    h["expected_false_hits"] = n_trials_total * r

survivors = [h for h in raw_hits if h["expected_false_hits"] < 0.5]

# observed-deviation (analytic) accounting for tightest hits, for the notes:
# E_obs = n_trials * (targets_in_decade * 2*dev/ln10) / cpv
def e_obs(h):
    d = h["dev"]
    q = h["qvalue"]
    if h["construction"] == "direct":
        tv, cpv = sorted_motifs, N_MOTIF
        n_in = int(np.sum((tv >= q / math.sqrt(10)) & (tv <= q * math.sqrt(10))))
    elif h["construction"] == "ratio":
        tv, cpv = sorted_rmotifs, N_RMOTIF
        n_in = int(np.sum((tv >= q / math.sqrt(10)) & (tv <= q * math.sqrt(10))))
    else:
        cpv = N_K * N_TARG
        n_in = 0
        for pk in PHIK:
            v = q * pk
            n_in += int(np.sum((targ_vals >= v / math.sqrt(10)) & (targ_vals <= v * math.sqrt(10))))
        n_in = n_in / N_K  # per scaled value decade average -> times N_K below
        n_in = n_in * N_K
    if d <= 0:
        d = 1e-16
    return n_trials_total * (n_in * 2 * d / math.log(10)) / cpv

raw_sorted = sorted(raw_hits, key=lambda h: h["dev"])
tightest = []
for h in raw_sorted[:20]:
    tightest.append(dict(qlabel=h["qlabel"], expr=h["expr"], q=h["qvalue"],
                         mval=h["mval"], dev=h["dev"],
                         E_tol=round(h["expected_false_hits"], 1),
                         E_obs_dev=round(e_obs(h), 3), flag=h["flag"]))

# known-match probes
probes = {}
me = mname.get("e -"); mmu = mname.get("mu -")
md_ = mname.get("d -1/3"); ms_ = mname.get("s -1/3")
if me and mmu:
    probes["m_mu/m_e vs 206"] = abs(mmu/me/206 - 1)
if md_ and ms_:
    probes["m_s/m_d vs 20"] = abs(ms_/md_/20 - 1)

out = dict(
    n_masses=len(masses), n_widths=len(widths), n_quantities=N_Q,
    n_motifs_direct=N_MOTIF, n_ratio_motifs=N_RMOTIF, n_scaled_targets=N_TARG,
    n_ratios=n_ratios,
    trials_direct=trials_direct, trials_scaled=trials_scaled,
    trials_ratio=trials_ratio, n_trials_total=n_trials_total,
    n_raw_hits=len(raw_hits),
    raw_by_construction={c: sum(1 for h in raw_hits if h["construction"] == c)
                         for c in ("direct", "scaled", "ratio")},
    n_survivors=len(survivors),
    survivors=[{k: v for k, v in h.items()} for h in survivors[:50]],
    tightest=tightest,
    known_probes=probes,
    min_expected_false_hits=min((h["expected_false_hits"] for h in raw_hits), default=None),
)
print(json.dumps(out, indent=1))
