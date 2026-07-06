#!/usr/bin/env python3
"""pdg_phi_lattice_3arm - executes PDG_PHI_LATTICE_PREREG.md EXACTLY (DRAFT companion, not a cert).

Order enforced by the prereg: NULL GATE first (200 synthetic draws), then TRAIN, then HOLDOUT once.
Metric M = median |log10(m_MeV) - nearest lattice point| (log10-MeV space, points absolute).
Deterministic; masses in MeV; sha256 of the dataset verified against the pinned manifest.

Implementation choices documented for the skeptic (not in prereg, frozen here before any run):
  - "distinct in-window points" resolution eps = 1e-9 in log10 units;
  - Arm-2/3 budget equalization: n in [-16,16] fixed, k-bound K searched in [1..400] so the
    distinct in-window count is closest to B (ties -> smaller K);
  - sensitivity variant (prereg S1): complexity-ordered first-B points, c = |n|+|k|+rank;
  - shell control (c): prereg's parenthetical "zone sizes 8/12/13" does not map onto the 13-slot
    shell machinery; implemented as the literal "scrambled shell_defs" = 200 random same-size
    reassignments of the 13 core slots, compared to the frozen A/B/C on mean circle-fit RMS.
"""
import hashlib
import json
import math
import sys
from bisect import bisect_left
from pathlib import Path

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
PDG = ROOT / "08_PASSPORTS" / "PDG"
PHI = (1 + 5 ** 0.5) / 2
DELTA0 = PHI - 1.5
LOG10_ME = math.log10(0.51099895)  # MeV
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]          # F1..F12 (repo BASIS layer)
LUC = [1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322]      # L1..L12 (control b)
ARI = list(range(1, 13))                                    # arithmetic (control a)
EPS = 1e-9
SEED, FRACTION = 20250101, 0.2                              # pdg_strict_protocol.json (frozen)
BETAS = [round(1.05 + 0.005 * i, 3) for i in range(int((2.20 - 1.05) / 0.005) + 1)]


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_masses():
    man = json.loads((PDG / "pdg_dataset_manifest.json").read_text())
    f = PDG / "data" / "mass_width_2025.mcd"
    want = None
    for v in (man.get("files") or man.get("datasets") or [man]):
        if isinstance(v, dict) and "sha256" in v and "mcd" in json.dumps(v):
            want = v["sha256"]
    got = sha256(f)
    if want:
        assert got == want, f"dataset hash mismatch: {got} != {want}"
    masses = {}
    for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("*"):
            continue
        toks = line.split()
        ids, mass = [], None
        for t in toks:
            if mass is None:
                try:
                    ids.append(abs(int(t)))
                    continue
                except ValueError:
                    pass
                try:
                    mass = float(t)
                except ValueError:
                    break
        if mass and mass > 0:
            for pid in ids:
                masses.setdefault(pid, mass * 1000.0)  # GeV -> MeV
    return masses, got


def is_holdout(pid):
    h = hashlib.sha256(f"{SEED}:{abs(int(pid))}".encode()).hexdigest()
    return int(h[:12], 16) / float(16 ** 12) < FRACTION


def lattice_points(base, kap, kmax, lo, hi, nmax=16, order_by_complexity=False, budget=None):
    """Vectorized. Semantics identical to prereg: distinct (eps=1e-9) in-window values."""
    lb, l2 = math.log10(base), math.log10(2.0)
    ns = np.arange(-nmax, nmax + 1) * l2
    ks = np.arange(-kmax, kmax + 1) * lb
    kaps = np.log10(np.array(kap, dtype=float))
    V = (ns[:, None, None] + ks[None, :, None] + kaps[None, None, :]).ravel()
    if order_by_complexity and budget:
        C = (np.abs(np.arange(-nmax, nmax + 1))[:, None, None]
             + np.abs(np.arange(-kmax, kmax + 1))[None, :, None]
             + np.arange(1, len(kap) + 1)[None, None, :]).ravel()
        m = (V >= lo - 0.5) & (V <= hi + 0.5)
        V, C = V[m], C[m]
        order = np.lexsort((V, C))
        out, seen = [], []
        for idx in order:
            v = float(V[idx])
            j = bisect_left(seen, v - EPS)
            if j < len(seen) and abs(seen[j] - v) < EPS:
                continue
            seen.insert(bisect_left(seen, v), v)
            out.append(v)
            if len(out) >= budget:
                break
        return sorted(out)
    V = np.sort(V[(V >= lo - 0.5) & (V <= hi + 0.5)])
    if V.size == 0:
        return []
    keep = np.concatenate(([True], np.diff(V) > EPS))
    return V[keep].tolist()


def median_err(xs, pts):
    a = np.asarray(pts)
    x = np.asarray(xs)
    i = np.clip(np.searchsorted(a, x), 1, len(a) - 1)
    best = np.minimum(np.abs(x - a[i - 1]), np.abs(x - a[i]))
    return float(np.median(best))


def equalize_kmax(base, kap, B, lo, hi):
    """Binary search on monotone distinct-count; ties -> smaller K (same rule as prereg scan)."""
    def cnt(K):
        return len(lattice_points(base, kap, K, lo, hi))
    if cnt(400) <= B:
        return 400
    lo_k, hi_k = 1, 400
    while lo_k < hi_k:
        mid = (lo_k + hi_k) // 2
        if cnt(mid) < B:
            lo_k = mid + 1
        else:
            hi_k = mid
    best, bestK = 10 ** 9, lo_k
    for K in (lo_k - 1, lo_k):
        if K >= 1:
            d = abs(cnt(K) - B)
            if d < best:
                best, bestK = d, K
    return bestK


def main() -> int:
    print("=== pdg_phi_lattice_3arm — executing PDG_PHI_LATTICE_PREREG.md ===")
    masses, h = load_masses()
    print(f"[data] {len(masses)} unique ids, sha256={h[:16]}..., split seed={SEED} frac={FRACTION}")
    ids = sorted(masses)
    X = {p: math.log10(masses[p]) for p in ids}
    lo, hi = min(X.values()), max(X.values())
    train = [p for p in ids if not is_holdout(p)]
    hold = [p for p in ids if is_holdout(p)]
    print(f"[split] train={len(train)} holdout={len(hold)} window=[{lo:.3f},{hi:.3f}] log10-MeV")

    # Arm 1: scene-pinned phi lattice, repo bounds -> budget B
    arm1 = lattice_points(PHI, FIB, 16, lo, hi)
    B = len(arm1)
    print(f"[arm1] scene-pinned phi+Fib: {B} distinct in-window points (BUDGET)")

    # Arm 2 grid equalization (mass-independent: window+budget only)
    kmaxes = {b: equalize_kmax(b, FIB, B, lo, hi) for b in BETAS}
    grids = {b: lattice_points(b, FIB, kmaxes[b], lo, hi) for b in BETAS}
    counts = [len(g) for g in grids.values()]
    print(f"[arm2] {len(BETAS)} betas equalized: point-count range [{min(counts)},{max(counts)}] vs B={B}")

    # Arm 3 lattice controls at phi, equalized
    ctrlA = lattice_points(PHI, ARI, equalize_kmax(PHI, ARI, B, lo, hi), lo, hi)
    ctrlB = lattice_points(PHI, LUC, equalize_kmax(PHI, LUC, B, lo, hi), lo, hi)
    print(f"[arm3] kappa-controls: arithmetic {len(ctrlA)} pts, Lucas {len(ctrlB)} pts")

    def rank_of_phi(xs):
        m_phi = median_err(xs, arm1)
        worse = sum(1 for b in BETAS if median_err(xs, grids[b]) < m_phi)
        return worse, m_phi

    def a2_margins(xs):
        m1 = median_err(xs, arm1)
        return median_err(xs, ctrlA) - m1, median_err(xs, ctrlB) - m1

    # ---- NULL GATE FIRST (prereg) ----
    rng = np.random.default_rng(20260704)
    n_draws = 200
    a1_pass_null = a2_pass_null = 0
    null_margins = []
    for _ in range(n_draws):
        xs = list(rng.uniform(lo, hi, len(ids)))
        r, _ = rank_of_phi(xs)
        if r <= 0.05 * len(BETAS):
            a1_pass_null += 1
        gA, gB = a2_margins(xs)
        null_margins.append(min(gA, gB))
        if gA > 0 and gB > 0:
            a2_pass_null += 1
    thresh95 = float(np.percentile(null_margins, 95))
    print(f"[null] A1 fired on {a1_pass_null}/{n_draws} synthetic draws (must be <=5%: {'PASS' if a1_pass_null <= 10 else 'FAIL'})")
    print(f"[null] A2 fired on {a2_pass_null}/{n_draws} synthetic draws (must be <=5%: {'PASS' if a2_pass_null <= 10 else 'FAIL'})")
    print(f"[null] 95th pct of min A2-margin on noise = {thresh95:.6f} (frozen A2 threshold)")
    null_ok = a1_pass_null <= 10 and a2_pass_null <= 10

    # ---- TRAIN ----
    xs_tr = [X[p] for p in train]
    r_tr, m_tr = rank_of_phi(xs_tr)
    gA_tr, gB_tr = a2_margins(xs_tr)
    print(f"[train] phi M={m_tr:.5f}, rank {r_tr}/{len(BETAS)} betas beat phi; A2 margins arith={gA_tr:+.5f} lucas={gB_tr:+.5f}")

    # ---- HOLDOUT (read once) ----
    xs_ho = [X[p] for p in hold]
    r_ho, m_ho = rank_of_phi(xs_ho)
    gA_ho, gB_ho = a2_margins(xs_ho)
    frac = r_ho / len(BETAS)
    a1 = "discriminating" if frac <= 0.05 else ("non-discriminating" if frac >= 0.50 else "ambiguous")
    a2_floor = max(0.0, thresh95)  # controls must not tie/beat Arm 1 (prereg conjunct; skeptic R-3)
    a2 = "load-bearing" if (gA_ho > a2_floor and gB_ho > a2_floor) else "not-shown"
    print(f"[HOLDOUT] phi M={m_ho:.5f}, rank {r_ho}/{len(BETAS)} (frac {frac:.2f}) -> A1: {a1}")
    print(f"[HOLDOUT] A2 margins arith={gA_ho:+.5f} lucas={gB_ho:+.5f} vs null95={thresh95:.5f} -> A2: {a2}")

    # ---- sensitivity variant (S1): complexity-ordered first-B points ----
    arm1c = lattice_points(PHI, FIB, 60, lo, hi, order_by_complexity=True, budget=B)
    r_c = sum(1 for b in BETAS
              if median_err(xs_ho, lattice_points(b, FIB, 60, lo, hi, order_by_complexity=True, budget=B)) < median_err(xs_ho, arm1c))
    print(f"[S1-sensitivity] complexity-ordered budget: phi holdout rank {r_c}/{len(BETAS)}")

    # ---- shell control (c): scrambled shell_defs vs frozen, via the passport machinery ----
    sys.path.insert(0, str(ROOT / "05_CERTS"))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("c13", ROOT / "05_CERTS" / "vp_core13_shell_geometry_passport.py")
        c13 = importlib.util.module_from_spec(spec)
        sys.modules["c13"] = c13  # py3.9: dataclasses/__future__ need registration (skeptic R-1)
        spec.loader.exec_module(c13)
        proto = json.loads((PDG / "core13_geometry_protocol.json").read_text())
        K_E = 2 ** 23 * (2 * math.pi) ** 3 * PHI ** (233 / 4.0)
        H_E = math.log10(K_E) / DELTA0
        nodes = [dict(id=1, n_abs=0.0, H13=0.0)]
        for idx, pid in enumerate(proto["legacy_core_pdgids"], start=1):
            if pid not in masses:
                continue
            l10 = math.log10(masses[pid])
            fit = c13.fit_lattice_log10(l10)
            Hp = H_E + (l10 - LOG10_ME) / DELTA0
            nodes.append(dict(id=idx, n_abs=abs(float(fit.n)), H13=Hp % 13.0))
        byid = {}
        for nd in nodes:
            byid.setdefault(int(nd["id"]), nd)
        nodes = [byid[k] for k in sorted(byid)]
        ref_y = float(next(n for n in nodes if n["id"] == 7)["H13"])
        for nd in nodes:
            nd["H13_u"] = c13.unwrap13(float(nd["H13"]), ref_y)

        def shells_rms(defs):
            tot = []
            for label, sids in defs.items():
                sub = [n for n in nodes if int(n["id"]) in sids]
                if len(sub) < 3:
                    return float("inf")
                x = np.array([float(n["n_abs"]) for n in sub])
                y = np.array([float(n["H13_u"]) for n in sub])
                cx, cy, r = c13.fit_circle_ls(x, y)
                rms, _ = c13.circle_residuals(x, y, cx, cy, r)
                tot.append(rms)
            return float(np.mean(tot))

        true_defs = proto["shell_defs"]
        rms_true = shells_rms(true_defs)
        sizes = [len(v) for v in true_defs.values()]
        beats = 0
        for _ in range(200):
            pool = list(range(1, 14))
            rng.shuffle(pool)
            fake, i0 = {}, 0
            for lab, s in zip(true_defs, sizes):
                fake[lab] = pool[i0:i0 + s]
                i0 += s
            if shells_rms(fake) <= rms_true:
                beats += 1
        print(f"[shell-c] frozen A/B/C mean-RMS={rms_true:.5f}; {beats}/200 random same-size scrambles do as well (p~{beats/200:.3f})")
    except Exception as e:
        print(f"[shell-c] DEFERRED (import/port failure: {e}) — recorded, not hidden")

    verdict = {"null_ok": null_ok, "A1": a1, "A2": a2, "phi_rank_holdout": r_ho,
               "betas": len(BETAS), "budget": B, "train_rank": r_tr,
               "margins_holdout": [gA_ho, gB_ho], "null95": thresh95}
    (ROOT / "_TASKS_CENTER_ATTACK" / "pdg_phi_lattice_3arm.results.json").write_text(json.dumps(verdict, indent=1))
    print("verdict:", json.dumps(verdict))
    if not null_ok:
        print("NULL GATE FAILED — per prereg, NO positive conclusion may be drawn from A1/A2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
