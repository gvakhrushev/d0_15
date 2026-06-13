#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ–PDG strict (compact)
- PDG load (particle lib + PDG mass/width mc table)
- φ-lattice best-fit in log10(m)
- electron anchor M0
- residuals: δ8 comb, helix Hφ
- audits (charge/spin) in compact form
- Core-13 geometry (3 shells + key line/parabola checks)
- CERT 19.4.2 Variant B++ (μ/p only) with M1+ ordering (BOOK IV — VERIFICATION)
- Minimal plots

Console output is controlled by VERBOSE and flags.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import os
import sys
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import requests
from matplotlib import pyplot as plt

from d0.constants import phi as PHI, psi as PSI, delta0 as DELTA_0, eps2 as EPS2, xi5 as XI5, pi0 as PI0
from d0.protocol import load_protocol, P
from d0.io import get_outdir, save_json
from d0.report import CertReport

# =============================================================================
# 0) CONFIG (compact, canonical-first)
# =============================================================================

def relpath_for_report(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()
# 0 = silent, 1 = normal summary, 2 = extra details
VERBOSE = 1

STRICT = True
USE_QUARK_OVERRIDES = False

# What to run

RUN_CERT_19_4_2 = False  # keep off by default to avoid repeating the already-canonized CERT 19.4.2 block
RUN_PLOTS = True
RUN_BASELINES = True
RUN_CORE_GEOMETRY = True

# Audits are heavy and not needed for the current narrowing experiments
RUN_AUDITS = False
PRINT_DELTA8_BY_CHARGE_SPIN = False


# δ8(mod1) offset narrowing experiments
PRINT_DELTA8_HYPOTHESES = False  # suppress hypotheses/baselines/decision block by default

# δ8 structure sanity / narrowing (no new hypotheses; only stricter tests)
DEDUP_ABS_PDGID_NON_NUC = True   # remove particle/antiparticle duplicates for non-nuclei pools
DEDUP_ABS_PDGID_NUC = False      # optional: dedup nuclei by abs(pdgid)
PRINT_DELTA8_PEAKS = True        # print refined peak locations for δ8 and δ8(mod1)
PRINT_DELTA8_POOL_RANKING = True # rank the 5 hypotheses across fixed pools (ALL/NO_NUC/HAD/NUC/FUND)
RUN_SEAM_BOOTSTRAP = False       # optional stability check (derived sample count; off by default)
RUN_DELTA8_SENSITIVITY = False   # rerun δ8 structure under stricter dedup variants and compare winners
RUN_DELTA8_LOO = False           # leave-one-pool-out stability: re-rank hypotheses while omitting each stable pool

# Output controls
PRINT_TOP_OUTLIERS = 0
SHOW_TYPE_BREAKDOWN = True   # compact per-type medians (no huge tables)

BASE_OUTDIR = get_outdir() / "cert_phi_pdg_strict"
DATA_DIR = Path(os.environ.get("D0_DATA_DIR", "data")).resolve()
PLOT_DIR = BASE_OUTDIR / "plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.size"] = 10


def log(msg: str = "", level: int = 1) -> None:
    if VERBOSE >= level:
        print(msg)


def section(title: str, level: int = 1) -> None:
    if VERBOSE >= level:
        print("\n" + str(title))


# =============================================================================
# 1) φ constants + strict invariants
# =============================================================================
LN_PHI = math.log(PHI)
LN2 = math.log(2.0)

# SI bridge
C_SI = 299_792_458
E_CHARGE = 1.602176634e-19
EV_TO_J = E_CHARGE
MEV_TO_J = 1e6 * EV_TO_J

# BOOK III electron anchor (explicit; BRIDGE)
M_E_MEV = 0.51099895
LOG10_ME = math.log10(M_E_MEV)

#
# π0 is CORE (structural circle holonomy); π is BRIDGE (numeral)
# From your canon: m0 = 2π0 = (12/5)·φ^2  ⇒  π0 = (6/5)·φ^2
PI = math.pi

# δ* as 2π/9: keep both CORE(π0) and BRIDGE(π)
DELTA_STAR0 = 2.0 * PI0 / 9.0   # CORE
DELTA_STAR = 2.0 * PI / 9.0     # BRIDGE

# Proposed seam candidates for the empirical δ8(mod1) offset a (NOT assumed canonical).
# We treat these as *testable hypotheses* only.
def p0_seam(k: int) -> float:
    """Candidate seam offset built only from CORE primitives (φ, δ0).

    p0_seam(k) := φ^-2 + δ0^2 - φ^-k
    """
    return (PHI ** (-2)) + (DELTA_0 ** 2) - (PHI ** (-int(k)))


# Current narrowing pack (5 hypotheses) focuses around k=15 because φ^-15 = φ·ε² links to ε² (BOOK III/IV).
P0_SEAM_13 = p0_seam(13)
P0_SEAM_14 = p0_seam(14)
P0_SEAM_15 = p0_seam(15)
P0_SEAM_16 = p0_seam(16)
P0_SEAM_17 = p0_seam(17)


def phi_pow(k: int) -> float:
    """Return φ^(-k) (your `phi^-k`)."""
    return PHI ** (-int(k))


def assert_close(a: float, b: float, tol: float, msg: str) -> None:
    if abs(a - b) > tol:
        raise AssertionError(f"{msg}: |Δ|={abs(a-b):.3e} > {tol}")


def assert_invariants() -> None:
    assert_close(PHI + PSI, 1.0, 1e-12, "A: φ+ψ=1")
    assert_close(PHI * PSI, -1.0, 1e-12, "B: φψ=-1")
    assert_close(PHI ** 2, PHI + 1.0, 1e-12, "C: φ²=φ+1")
    assert_close(PSI ** 2, PSI + 1.0, 1e-12, "D: ψ²=ψ+1")
    assert_close(PHI - DELTA_0, 1.5, 1e-12, "φ-δ₀=3/2")
    # π0/δ0 canonical relation from your CORE doc: δ0 = 3/(5π0φ)
    assert_close(PI0, (6.0 / 5.0) * (PHI ** 2), 1e-12, "π0=(6/5)φ²")
    assert_close(DELTA_0, 3.0 / (5.0 * PI0 * PHI), 5e-12, "δ0=3/(5π0φ)")


if STRICT:
    assert_invariants()

# CERT 19.4.2 invariants (no fitted params)
A0 = phi_pow(1)     # φ^-1
B0 = phi_pow(2)     # φ^-2


def report_seam_alpha() -> Dict[str, float]:
    """CORE seam check for α^{-1} (Seam Theorem) with ε² tolerance.

    Uses BOOK III formulas:
      α^{-1}_top = 359/φ^2 - ξ5,  where ξ5 = φ^-5
      α^{-1}_alg = 2^11·π0/φ^8 + 2·δ0/3
    PASS iff |Δα| < ε², where ε² = φ^-16.
    """
    alpha_inv_top = (359.0 / (PHI ** 2)) - XI5
    alpha_inv_alg = ((2.0 ** 11) * PI0 / (PHI ** 8)) + (2.0 * DELTA_0) / 3.0
    delta_alpha = abs(alpha_inv_top - alpha_inv_alg)
    pass_alpha = delta_alpha < EPS2

    section("=== SEAM α certificate (CORE) ===", 1)
    log(f"eps²=φ^-16={EPS2:.10g}  criterion: |Δα|<eps²", 1)
    log(f"alpha_inv_top = 359/φ^2 - ξ5 = {alpha_inv_top:.12f}", 1)
    log(f"alpha_inv_alg = 2^11·π0/φ^8 + 2·δ0/3 = {alpha_inv_alg:.12f}", 1)
    log(f"[ALPHA] Δα={delta_alpha:.6e}  PASS={pass_alpha}", 1)

    # also print α for convenience (BRIDGE display only)
    if alpha_inv_top > 0:
        log(f"α(top)=1/alpha_inv_top={1.0/alpha_inv_top:.12g}", 2)
    if alpha_inv_alg > 0:
        log(f"α(alg)=1/alpha_inv_alg={1.0/alpha_inv_alg:.12g}", 2)

    return {
        "alpha_inv_top": float(alpha_inv_top),
        "alpha_inv_alg": float(alpha_inv_alg),
        "delta_alpha": float(delta_alpha),
        "alpha_pass": float(1.0 if pass_alpha else 0.0),
    }


# =============================================================================
# 2) small math helpers
# =============================================================================
def mev_to_joule(mev: float) -> float:
    return float(mev) * MEV_TO_J


def mev_to_kg(mev: float) -> float:
    return mev_to_joule(mev) / (C_SI ** 2)


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def lucas(n: int) -> int:
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def relerr(pred: float, exp: float) -> float:
    exp = float(exp)
    return float(abs(float(pred) - exp) / exp)


def dist_to_integer(x: np.ndarray) -> np.ndarray:
    return np.abs(x - np.round(x))


# --- helpers for δ8 structure narrowing ---
def dedup_by_abs_pdgid(df: pd.DataFrame) -> pd.DataFrame:
    """Deterministic deduplication by |pdgid|.

    Intended to prevent double-counting particle/antiparticle copies in structure tests.
    Keeps the first row after sorting by (|pdgid|, prefer positive pdgid).
    """
    if df.empty or "pdgid" not in df.columns:
        return df
    out = df.copy()
    out["abs_pdgid"] = out["pdgid"].astype(int).abs()
    out["neg_flag"] = (out["pdgid"].astype(int) < 0).astype(int)
    out = out.sort_values(["abs_pdgid", "neg_flag"]).drop_duplicates("abs_pdgid", keep="first")
    return out.drop(columns=["abs_pdgid", "neg_flag"])


def obj_mean_median(arr: np.ndarray, a: float) -> Tuple[float, float]:
    """Return (mean, median) of dist-to-integer for (arr - a)."""
    if arr.size == 0:
        return (math.nan, math.nan)
    d = dist_to_integer(arr - float(a))
    return (float(np.mean(d)), float(np.median(d)))


def top_hist_peaks(values: np.ndarray, lo: float, hi: float, bins: int, topk: int = 5) -> List[Tuple[float, int]]:
    """Return [(center, count), ...] of the top-k histogram bins."""
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return []
    hist, edges = np.histogram(v, bins=int(bins), range=(float(lo), float(hi)))
    if hist.size == 0:
        return []
    idx = np.argsort(hist)[::-1][: int(topk)]
    peaks: List[Tuple[float, int]] = []
    for i in idx:
        center = 0.5 * (edges[int(i)] + edges[int(i) + 1])
        peaks.append((float(center), int(hist[int(i)])))
    return peaks


def best_offset_mod1(values: np.ndarray, grid: int = 4000) -> Tuple[float, float]:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return (math.nan, math.nan)
    v = np.mod(v, 1.0)
    a_grid = np.linspace(0.0, 1.0, grid, endpoint=False)
    best_a, best_score = 0.0, float("inf")
    for a in a_grid:
        score = float(np.mean(dist_to_integer(v - a)))
        if score < best_score:
            best_a, best_score = float(a), score
    return best_a, best_score


def best_offset_mod1_refined(values: np.ndarray, coarse: int = 4000, fine: int = 8000, span_steps: int = 6) -> Tuple[float, float]:
    """Two-stage best offset search on [0,1):

    1) coarse grid search (default 1/4000 step)
    2) local refinement around the coarse best within ±span_steps*coarse_step using a fine grid.

    Returns (best_a, best_score) where score = mean(|(v-a)-round(v-a)|).
    """
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return (math.nan, math.nan)
    v = np.mod(v, 1.0)

    coarse_a, coarse_score = best_offset_mod1(v, grid=int(coarse))
    step = 1.0 / float(coarse)
    left = coarse_a - span_steps * step
    right = coarse_a + span_steps * step

    # Build refinement grid and wrap into [0,1)
    a_grid = np.linspace(left, right, int(fine), endpoint=True)
    a_grid = np.mod(a_grid, 1.0)

    best_a, best_score = coarse_a, coarse_score
    for a in a_grid:
        score = float(np.mean(dist_to_integer(v - float(a))))
        if score < best_score:
            best_a, best_score = float(a), score

    return best_a, best_score


# =============================================================================
# 3) PDG loading
# =============================================================================
# -------------------------
# PDG source pinning (reproducible)
# -------------------------
PDG_YEAR = int(os.environ.get("D0_PDG_YEAR", "2025"))
MW_URL = f"https://pdg.lbl.gov/{PDG_YEAR}/mcdata/mass_width_{PDG_YEAR}.mcd"
MW_FILE = DATA_DIR / f"mass_width_{PDG_YEAR}.mcd"

OFFLINE = os.environ.get("D0_PDG_OFFLINE", "0").strip() == "1"
HTTP_TIMEOUT = float(os.environ.get("D0_PDG_TIMEOUT_S", "30"))
PDG_SHA256: Optional[str] = None


class DownloadError(RuntimeError):
    pass


def download_text(url: str, target: Path) -> None:
    try:
        resp = requests.get(url, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
    except requests.exceptions.SSLError as exc:
        raise DownloadError(
            f"SSL error while downloading PDG data. Download manually to {target}"
        ) from exc
    target.write_text(resp.text, encoding="utf-8")

def ensure_pdg_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if MW_FILE.exists():
        return
    if OFFLINE:
        raise RuntimeError(
            f"[OFFLINE] PDG file missing: {MW_FILE}. "
            "Download it once (offline=0) or place the file manually."
        )
    log(f"Downloading {MW_URL}", 1)
    download_text(MW_URL, MW_FILE)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_mass_width() -> pd.DataFrame:
    ensure_pdg_file()
    log(f"Using cache {MW_FILE}", 2)
    pdg_sha256 = sha256_file(MW_FILE)
    global PDG_SHA256
    PDG_SHA256 = pdg_sha256
    print(f"[PDG] year={PDG_YEAR} file={MW_FILE.name} sha256={pdg_sha256} path={relpath_for_report(MW_FILE)}")

    rows: List[Dict[str, object]] = []
    with MW_FILE.open("r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip() or line.lstrip().startswith("*"):
                continue
            line = line.rstrip("\n").ljust(128)
            mcids = [line[0:8], line[8:16], line[16:24], line[24:32]]
            ids = [f.strip() for f in mcids if f.strip()]
            if not ids:
                continue
            mass_str = line[33:51].strip()
            width_str = line[70:88].strip()
            name = line[107:128].strip()
            mass = float(mass_str) if mass_str else math.nan
            width = float(width_str) if width_str else math.nan
            for mid in ids:
                if mid.lstrip("-").isdigit():
                    rows.append(
                        dict(
                            mcid=int(mid),
                            mass_GeV_mc=mass,
                            width_GeV_mc=width,
                            name_mc=name,
                        )
                    )
    df = pd.DataFrame(rows).drop_duplicates("mcid")
    log(f"MC-ID records: {len(df)}", 2)
    return df


def load_particle_library() -> pd.DataFrame:
    try:
        from particle import Particle, pdgid as pidmod
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "particle"])
        from particle import Particle, pdgid as pidmod

    def classify(pid: Optional[int]) -> str:
        if pid is None:
            return "other"
        apid = abs(int(pid))
        if apid > 1_000_000_000:
            return "nucleus"
        if pidmod.is_quark(pid):
            return "quark"
        if pidmod.is_lepton(pid):
            return "lepton"
        if pidmod.is_sm_gauge_boson_or_higgs(pid):
            return "gauge"
        if pidmod.is_baryon(pid):
            return "baryon"
        if pidmod.is_meson(pid):
            return "meson"
        return "other"

    rows: List[Dict[str, object]] = []
    for part in Particle.findall():
        pid = getattr(part, "pdgid", None)
        if pid is None:
            continue
        mass = getattr(part, "mass", None)
        width = getattr(part, "width", None)
        rows.append(
            dict(
                pdgid=int(pid),
                mcid=int(pid),
                name_pdg=getattr(part, "name", None),
                mass_GeV_pdg=(mass / 1000.0) if mass else math.nan,
                width_GeV_pdg=(width / 1000.0) if width else math.nan,
                charge_e_pdg=getattr(part, "charge", None),
                J_pdg=getattr(part, "J", None),
            )
        )
    df = pd.DataFrame(rows)
    df["type"] = df["pdgid"].apply(classify)
    log(f"Particle library: {len(df)} records", 2)
    return df


QUARK_OVERRIDES_MEV = {1: 4.8, 2: 2.3, 3: 95.0, 4: 1270.0, 5: 4180.0, 6: 172760.0}


def build_master() -> pd.DataFrame:
    df_mc = load_mass_width()
    df_particle = load_particle_library()

    master = df_particle.merge(df_mc, on="mcid", how="left", suffixes=("_pdg", "_mc"))
    master["mass_GeV"] = master["mass_GeV_pdg"].fillna(master["mass_GeV_mc"])
    master["width_GeV"] = master["width_GeV_pdg"].fillna(master["width_GeV_mc"])
    master["mass_MeV"] = master["mass_GeV"] * 1000.0
    master["width_MeV"] = master["width_GeV"] * 1000.0

    if USE_QUARK_OVERRIDES:
        for pid, mass in QUARK_OVERRIDES_MEV.items():
            mask = (master["pdgid"] == pid) & (master["mass_MeV"].isna())
            master.loc[mask, "mass_MeV"] = float(mass)

    master["log10_m"] = np.nan
    msk = master["mass_MeV"].notna() & (master["mass_MeV"] > 0)
    master.loc[msk, "log10_m"] = np.log10(master.loc[msk, "mass_MeV"].astype(float))
    return master


# =============================================================================
# 4) CERT 19.4.2 Variant B++ certificate (μ/p only)
# =============================================================================
def tom16_variant_bpp_report(master: pd.DataFrame) -> Dict[str, float]:
    if VERBOSE <= 0:
        return {}

    def mass_mev(pdgid: int) -> float:
        row = master.loc[(master["pdgid"] == pdgid) & master["mass_MeV"].notna()]
        if row.empty:
            raise RuntimeError(f"PDGID {pdgid} not found with mass in MASTER")
        return float(row.iloc[0]["mass_MeV"])

    me = mass_mev(11)
    mmu = mass_mev(13)
    mp = mass_mev(2212)

    mu_exp = mmu / me
    p_exp = mp / me

    # Proton check (APPX7.9.3)
    sqrt5 = math.sqrt(5.0)
    L4 = lucas(4)
    p_pred = (PHI ** ((29.0 + sqrt5) / 2.0)) - (L4 * DELTA_0 / 3.0)
    p_rel = relerr(p_pred, p_exp)
    p_pass = p_rel <= EPS2

    section("=== CERT 19.4.2 (μ/p) canonical certificate ===", 1)
    log(f"phi={PHI:.15f}  eps^2=phi^-16={EPS2:.10g}", 1)
    log(f"mu_exp={mu_exp:.9f}  p_exp={p_exp:.11f}", 1)
    log(f"[PROTON] p_pred={p_pred:.15f}  relerr={p_rel:.6e}  PASS={p_pass}", 1)

    # μ hypotheses
    L11 = lucas(11)
    mu0 = float(L11 + L4)  # 206

    terms: Dict[str, Tuple[float, int]] = {
        "a0": (A0, 7),
        "b0": (B0, 6),
        "phi^-2": (phi_pow(2), 6),
        "phi^-3": (phi_pow(3), 7),
        "phi^-4": (phi_pow(4), 8),
        "xi5": (XI5, 9),
        "d0": (DELTA_0, 9),
        "2d0/3": ((2.0 * DELTA_0) / 3.0, 9),
        "d0^2": (DELTA_0 ** 2, 11),
        "eps2": (EPS2, 11),
    }

    def mu_from(tl: List[str]) -> float:
        return float(mu0 + sum(terms[t][0] for t in tl))

    def depth_of(tl: List[str]) -> int:
        return 1 if not tl else 1 + int(max(terms[t][1] for t in tl))

    # Certificate search (μ only): atoms<=2, depth<=7, canonical by (atoms, depth, terms)
    allowed = ["a0", "b0", "phi^-2", "phi^-3", "phi^-4", "d0", "2d0/3", "xi5", "d0^2", "eps2"]
    all_cands: List[Tuple[int, int, List[str], float, float]] = []
    for r in range(0, 3):
        for combo in combinations(allowed, r):
            tl = sorted(list(combo))
            depth = depth_of(tl)
            if depth > 7:
                continue
            mu_pred = mu_from(tl)
            rr = relerr(mu_pred, mu_exp)
            all_cands.append((r, depth, tl, mu_pred, rr))

    pass_cands = [c for c in all_cands if c[4] <= EPS2]
    pass_sorted = sorted(pass_cands, key=lambda c: (c[0], c[1], c[2]))
    winner = pass_sorted[0] if pass_sorted else None

    section("=== μ certificate (M1+) ===", 1)
    log(f"eps²=φ^-16={EPS2:.10g}  criterion: relerr≤eps²", 1)
    log(f"Search: atoms≤2 depth≤7  enumerated={len(all_cands)}  PASS={len(pass_cands)}", 1)
    if winner is None:
        log("No PASS candidate in this bucket.", 1)
        log("[MUON] mu_pred=nan  relerr=nan  PASS=False", 1)
        return

    atoms, depth, tl, mu_pred, rr = winner
    theta11 = 1.0 / mu_pred
    log(f"WINNER: μ={mu_pred:.15f}  relerr={rr:.6e}  terms={tl}  atoms={atoms} depth={depth}", 1)
    log(f"[MUON] mu_pred={mu_pred:.15f}  relerr={rr:.6e}  PASS={rr <= EPS2}", 1)
    log(f"Θ11 = 1/μ = {theta11:.18f}", 1)

    # Invariant equivalence note (printed even in VERBOSE=1 because it closes ambiguity)
    mu_canon = mu0 + B0 + phi_pow(2)
    mu_alt = mu0 + A0 + phi_pow(4)
    log(f"Equivalence: 206+b0+φ^-2 = 206+a0+φ^-4  (|diff|={abs(mu_canon-mu_alt):.3e})", 1)

    # Return a compact machine-readable summary for kill-switch panels
    return {
        'mu_exp': float(mu_exp), 'p_exp': float(p_exp),
        'mu_pred': float(mu_pred), 'mu_rel': float(rr), 'mu_pass': float(1.0 if rr <= EPS2 else 0.0),
        'p_pred': float(p_pred), 'p_rel': float(p_rel), 'p_pass': float(1.0 if p_pass else 0.0),
    }


# =============================================================================
# 5) φ-lattice (log10 basis)
# =============================================================================
@dataclass
class LatticeFit:
    n: float
    k: float
    kappa: float
    log10_pred: float
    delta_log10: float
    err_quanta: float
    complexity: float


def build_lattice_basis() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    # κ candidates: Fibonacci-ish set (as in your code)
    fib_c = sorted({int(round((PHI ** n - PSI ** n) / math.sqrt(5.0))) for n in range(1, 13)})
    n_vals = np.arange(-16, 17)
    k_vals = np.arange(-16, 17)

    # rank for κ complexity
    kappa_rank = {kappa: i + 1 for i, kappa in enumerate(fib_c)}

    _log2 = math.log10(2.0)
    _logphi = math.log10(PHI)

    Bn, Bk, Bkap, Blog, Bc = [], [], [], [], []
    for n in n_vals:
        for k in k_vals:
            for kappa in fib_c:
                logpred = n * _log2 + k * _logphi + math.log10(kappa)
                cplx = abs(int(n)) + abs(int(k)) + kappa_rank[int(kappa)]
                Bn.append(int(n))
                Bk.append(int(k))
                Bkap.append(int(kappa))
                Blog.append(float(logpred))
                Bc.append(int(cplx))
    return (
        np.asarray(Bn, dtype=int),
        np.asarray(Bk, dtype=int),
        np.asarray(Bkap, dtype=int),
        np.asarray(Blog, dtype=float),
        np.asarray(Bc, dtype=int),
    )


B_N, B_K, B_KAPPA, B_LOG, B_CPLX = build_lattice_basis()
CPLX_EPS = 1e-12


def fit_lattice_log10(log10m: float) -> LatticeFit:
    if not np.isfinite(log10m):
        return LatticeFit(np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)
    delta = np.abs(B_LOG - float(log10m))
    dmin = float(np.min(delta))

    # Canonical tie-breaking (M1+):
    # 1) minimize |Δlog10|
    # 2) minimize complexity C
    # 3) minimize (|n|, |k|, κ, n, k) for determinism
    tol = 1e-12
    cand = np.where(delta <= dmin + tol)[0]
    if cand.size == 1:
        idx = int(cand[0])
    else:
        C = B_CPLX[cand]
        Cmin = int(np.min(C))
        cand2 = cand[np.where(C == Cmin)[0]]
        if cand2.size == 1:
            idx = int(cand2[0])
        else:
            n = B_N[cand2]
            k = B_K[cand2]
            kap = B_KAPPA[cand2]
            key = np.lexsort((k, n, kap, np.abs(k), np.abs(n)))
            idx = int(cand2[key[0]])

    dlog = float(log10m) - float(B_LOG[idx])
    return LatticeFit(
        float(B_N[idx]),
        float(B_K[idx]),
        float(B_KAPPA[idx]),
        float(B_LOG[idx]),
        float(dlog),
        float(dlog / DELTA_0),
        float(B_CPLX[idx]),
    )


# =============================================================================
# 6) δ8 residual extraction (strict)
# =============================================================================
def compute_delta8(master: pd.DataFrame) -> None:
    master["phi_exp"] = np.nan
    master["g8"] = np.nan
    master["delta8"] = np.nan

    mask = master["mass_MeV"].notna() & (master["mass_MeV"] > 0) & master["n"].notna() & master["kappa"].notna()
    if not mask.any():
        return

    m = master.loc[mask, "mass_MeV"].astype(float)
    n = master.loc[mask, "n"].astype(float)
    kap = master.loc[mask, "kappa"].astype(float)

    # φ-exponent relative to electron after removing 2^n and κ
    phi_exp = np.log(m / M_E_MEV) / LN_PHI - n * (LN2 / LN_PHI) - np.log(kap) / LN_PHI
    g8 = np.floor(phi_exp / 8.0)
    delta8 = phi_exp - 8.0 * g8
    delta8 = np.where(delta8 < 0, delta8 + 8.0, delta8)

    master.loc[mask, "phi_exp"] = phi_exp
    master.loc[mask, "g8"] = g8
    master.loc[mask, "delta8"] = delta8


def report_delta8(master: pd.DataFrame) -> None:
    sub = master.dropna(subset=["delta8"]).copy()
    if sub.empty:
        return

    section(f"δ8 quick: δ* CORE(2π0/9)={DELTA_STAR0:.6f}  BRIDGE(2π/9)={DELTA_STAR:.6f}", 1)
    hist, edges = np.histogram(sub["delta8"].to_numpy(float), bins=160, range=(0.0, 8.0))
    imax = int(np.argmax(hist))
    mode = 0.5 * (edges[imax] + edges[imax + 1])

    log(f"N={len(sub)}  median={sub['delta8'].median():.4f}  mode≈{mode:.4f}", 1)


def report_delta8_structure(
    master: pd.DataFrame,
    *,
    label: str = "",
    dedup_abs_pdgid_non_nuc: Optional[bool] = None,
    dedup_abs_pdgid_nuc: Optional[bool] = None,
    run_seam_bootstrap: Optional[bool] = None,
) -> Dict[str, object]:
    ddf = master.dropna(subset=["delta8"]).copy()
    if ddf.empty:
        return {}

    # Resolve effective flags (allow sensitivity runs without mutating globals)
    _dedup_non_nuc = DEDUP_ABS_PDGID_NON_NUC if dedup_abs_pdgid_non_nuc is None else bool(dedup_abs_pdgid_non_nuc)
    _dedup_nuc = DEDUP_ABS_PDGID_NUC if dedup_abs_pdgid_nuc is None else bool(dedup_abs_pdgid_nuc)
    _run_boot = RUN_SEAM_BOOTSTRAP if run_seam_bootstrap is None else bool(run_seam_bootstrap)
    _lab = (label.strip() + ": ") if label.strip() else ""

    # Optional dedup to avoid double counting ±pdgid copies
    if _dedup_nuc:
        ddf = dedup_by_abs_pdgid(ddf)
    else:
        if _dedup_non_nuc:
            non_nuc = ddf[ddf["type"] != "nucleus"]
            nuc = ddf[ddf["type"] == "nucleus"]
            non_nuc = dedup_by_abs_pdgid(non_nuc)
            ddf = pd.concat([non_nuc, nuc], ignore_index=True)

    # Fixed evaluation pools (no new free parameters)
    pools: Dict[str, pd.DataFrame] = {
        "ALL": ddf,
        "NO_NUC": ddf[ddf["type"] != "nucleus"],
        "HAD": ddf[ddf["type"].isin(["baryon", "meson"])],
        "NUC": ddf[ddf["type"] == "nucleus"],
        "FUND": ddf[ddf["type"].isin(["lepton", "gauge", "quark"])],
    }

    # Derived minimum sample size for “stable pool” reporting (no ad hoc constant):
    # N_min := ceil(1/δ0^2)
    N_MIN_STABLE = int(math.ceil(1.0 / (DELTA_0 ** 2)))
    MIN_POOL_N = int(os.environ.get("D0_MIN_POOL_N", "72"))
    summary: Dict[str, object] = {
        "label": label,
        "N_MIN_STABLE": int(N_MIN_STABLE),
        "pool_best": {},
        "pool_winner": {},
        "rank_winner": None,
        "rank_sum": {},
        "minimax_winner": None,
        "minimax_items": [],
        "loo_winners": {},
        "loo_counts": {},
        "loo_consensus": None,
    }

    # --- EXACTLY 5 testable hypotheses for δ8(mod1) offset a ---
    def frac(x: float) -> float:
        return float(np.mod(float(x), 1.0))

    H = [
        ("H1 a=frac(p0_seam15)", frac(P0_SEAM_15)),
        ("H2 a=frac(p0_seam14)", frac(P0_SEAM_14)),
        ("H3 a=frac(p0_seam16)", frac(P0_SEAM_16)),
        ("H4 a=frac(p0_seam13)", frac(P0_SEAM_13)),
        ("H5 a=frac(p0_seam17)", frac(P0_SEAM_17)),
    ]

    baselines = [
        ("BASE 0", 0.0),
        ("BASE 3/8", 3.0 / 8.0),
        ("BASE 1/φ", 1.0 / PHI),
        ("BASE δ0", frac(DELTA_0)),
    ]

    # Compute empirical best a per pool
    pool_best: Dict[str, Tuple[float, float, int]] = {}
    pool_mod1: Dict[str, np.ndarray] = {}
    for pname, pdf in pools.items():
        arr = np.mod(pdf["delta8"].astype(float).to_numpy(), 1.0)
        arr = arr[np.isfinite(arr)]
        pool_mod1[pname] = arr
        if arr.size == 0:
            pool_best[pname] = (math.nan, math.nan, 0)
            continue
        a_best, sc_best = best_offset_mod1_refined(arr, coarse=4000, fine=8000, span_steps=6)
        pool_best[pname] = (float(a_best), float(sc_best), int(arr.size))

    # Compact headline
    summary["pool_best"] = {k: (float(v[0]), float(v[1]), int(v[2])) for k, v in pool_best.items()}
    section(f"=== {_lab}δ8 comb / offset test (mod 1): pool stability ===", 1)
    for pname in ["ALL", "NO_NUC", "HAD", "NUC", "FUND"]:
        a_best, sc_best, n = pool_best[pname]
        if n == 0:
            log(f"{pname:6s}: N=0", 1)
        else:
            flag = "OK" if n >= N_MIN_STABLE else f"LOW_N(<{N_MIN_STABLE})"
            log(f"{pname:6s}: N={n:5d}  best a≈{a_best:.6f}  mean-dist={sc_best:.6e}  [{flag}]", 1)

    # Hypotheses table (exactly 5) + optional ranking across pools
    if PRINT_DELTA8_HYPOTHESES:
        log("Hypotheses (exactly 5):", 1)
        for name, a in H:
            parts = []
            for pname in ["ALL", "NO_NUC", "HAD", "NUC", "FUND"]:
                arr = pool_mod1[pname]
                if arr.size == 0:
                    parts.append(f"{pname}:N0")
                    continue
                a_best, sc_best, _ = pool_best[pname]
                m_mean, m_med = obj_mean_median(arr, a)
                gap = m_mean - sc_best
                parts.append(f"{pname}:Δa={abs(a-a_best):.2e},ΔF={gap:.2e}")
            log(f"  {name:20s}  a={a:.6f}  " + "  ".join(parts), 1)

        log("Baselines:", 1)
        for name, a in baselines:
            parts = []
            for pname in ["ALL", "NO_NUC", "HAD", "NUC", "FUND"]:
                arr = pool_mod1[pname]
                if arr.size == 0:
                    parts.append(f"{pname}:N0")
                    continue
                a_best, sc_best, _ = pool_best[pname]
                m_mean, _ = obj_mean_median(arr, a)
                gap = m_mean - sc_best
                parts.append(f"{pname}:Δa={abs(a-a_best):.2e},ΔF={gap:.2e}")
            log(f"  {name:20s}  a={a:.6f}  " + "  ".join(parts), 1)

        # Strict per-pool decision summary: among H1..H5 only
        section("=== δ8 decision: best hypothesis per pool (H1..H5) ===", 1)
        for pname in ["ALL", "NO_NUC", "HAD", "NUC", "FUND"]:
            arr = pool_mod1[pname]
            if arr.size == 0:
                log(f"{pname:6s}: N=0", 1)
                continue
            a_best, sc_best, n = pool_best[pname]
            # compute mean-dist gaps for each hypothesis relative to empirical best
            items = []
            for hname, a in H:
                m_mean, m_med = obj_mean_median(arr, a)
                items.append((hname, a, float(m_mean - sc_best), float(abs(a - a_best))))
            items_sorted = sorted(items, key=lambda t: (t[2], t[3], t[0]))
            win = items_sorted[0]
            runner = items_sorted[1] if len(items_sorted) > 1 else None
            summary["pool_winner"][pname] = {"win": win[0], "gap": float(win[2]), "delta_a": float(win[3])}

            stability = "OK" if n >= N_MIN_STABLE else f"LOW_N(<{N_MIN_STABLE})"
            # math is already imported at top-level, so do not import here
            if runner is None:
                rho_w = float(win[2] / sc_best) if sc_best > 0 else math.nan
                log(f"{pname:6s}: N={n:5d}  WIN={win[0]}  ΔF={win[2]:.2e}  ρ={rho_w:.2e}  Δa={win[3]:.2e}  [{stability}]", 1)
            else:
                margin = float(runner[2] - win[2])
                rho_w = float(win[2] / sc_best) if sc_best > 0 else math.nan
                rho_r = float(runner[2] / sc_best) if sc_best > 0 else math.nan
                log(
                    f"{pname:6s}: N={n:5d}  WIN={win[0]}  ΔF={win[2]:.2e}  ρ={rho_w:.2e}  Δa={win[3]:.2e}  "
                    f"RUNNER={runner[0]}  ΔF={runner[2]:.2e}  ρ={rho_r:.2e}  margin(ΔF)={margin:.2e}  [{stability}]",
                    1,
                )

    if PRINT_DELTA8_POOL_RANKING:
        # Rank the 5 hypotheses by (sum of pool ranks) using gap to empirical best in each pool.
        # Deterministic: lower is better.
        pool_list = [p for p in ["ALL", "NO_NUC", "HAD", "NUC", "FUND"] if pool_best[p][2] >= MIN_POOL_N]
        scores: Dict[str, float] = {name: 0.0 for name, _ in H}
        for pname in pool_list:
            arr = pool_mod1[pname]
            if arr.size == 0:
                continue
            a_best, sc_best, _ = pool_best[pname]
            gaps = []
            for name, a in H:
                m_mean, _ = obj_mean_median(arr, a)
                gaps.append((name, m_mean - sc_best, abs(a - a_best)))
            # primary: gap; secondary: |Δa|
            gaps_sorted = sorted(gaps, key=lambda t: (t[1], t[2], t[0]))
            for rank, (name, _, _) in enumerate(gaps_sorted, start=1):
                scores[name] += float(rank)

        winner = sorted(scores.items(), key=lambda kv: (kv[1], kv[0]))[0]
        summary["rank_winner"] = winner[0]
        summary["rank_sum"] = {k: float(v) for k, v in scores.items()}
        section("=== δ8 hypothesis ranking (lower is better) ===", 1)
        log(f"Pools used for ranking (N≥{MIN_POOL_N}): {pool_list}", 1)
        for name, sc in sorted(scores.items(), key=lambda kv: (kv[1], kv[0])):
            log(f"  {name:20s}  rank_sum={sc:.1f}", 1)
        log(f"WINNER (by rank_sum): {winner[0]}", 1)

        # Minimax check (strict, stable pools only): choose the hypothesis with the smallest worst-case ΔF
        # and also report worst-case relative penalty ρ := ΔF/sc_best.
        section("=== δ8 universal candidate (minimax over stable pools) ===", 1)
        worst_abs: Dict[str, float] = {name: 0.0 for name, _ in H}
        worst_rho: Dict[str, float] = {name: 0.0 for name, _ in H}

        for pname in pool_list:
            a_best, sc_best, _n = pool_best[pname]
            for hname, a in H:
                m_mean, _ = obj_mean_median(pool_mod1[pname], a)
                gap = float(m_mean - sc_best)
                worst_abs[hname] = max(worst_abs[hname], gap)
                rho = float(gap / sc_best) if sc_best > 0 else math.nan
                if math.isfinite(rho):
                    worst_rho[hname] = max(worst_rho[hname], rho)

        # deterministic reporting: sort by worst_abs then worst_rho then name
        items = sorted([(h, worst_abs[h], worst_rho[h]) for h, _ in H], key=lambda t: (t[1], t[2], t[0]))
        summary["minimax_items"] = [(h, float(wabs), float(wrho)) for h, wabs, wrho in items]
        summary["minimax_winner"] = items[0][0]
        for h, wabs, wrho in items:
            log(f"  {h:20s}  worst ΔF={wabs:.2e}  worst ρ={wrho:.2e}", 1)
        log(f"MINIMAX winner: {items[0][0]}", 1)

        # Leave-one-pool-out stability: repeat rank-sum winner while omitting each stable pool once.
        if RUN_DELTA8_LOO and len(pool_list) >= 2:
            section("=== δ8 leave-one-pool-out (LOO) ranking ===", 1)
            loo_winners: Dict[str, str] = {}
            loo_counts: Dict[str, int] = {name: 0 for name, _ in H}

            for leave in pool_list:
                pools2 = [p for p in pool_list if p != leave]
                scores2: Dict[str, float] = {name: 0.0 for name, _ in H}

                for pname in pools2:
                    arr = pool_mod1[pname]
                    if arr.size == 0:
                        continue
                    a_best, sc_best, _ = pool_best[pname]
                    gaps = []
                    for name, a in H:
                        m_mean, _ = obj_mean_median(arr, a)
                        gaps.append((name, float(m_mean - sc_best), float(abs(a - a_best))))
                    gaps_sorted = sorted(gaps, key=lambda t: (t[1], t[2], t[0]))
                    for rank, (name, _gap, _da) in enumerate(gaps_sorted, start=1):
                        scores2[name] += float(rank)

                win2 = sorted(scores2.items(), key=lambda kv: (kv[1], kv[0]))[0][0]
                loo_winners[str(leave)] = str(win2)
                loo_counts[str(win2)] += 1
                log(f"leave {leave:6s}: pools={pools2}  winner={win2}", 1)

            # consensus diagnostic
            uniq = sorted(set(loo_winners.values()))
            consensus = (len(uniq) == 1)
            if consensus:
                log(f"LOO consensus: YES  winner={uniq[0]}", 1)
            else:
                log(f"LOO consensus: NO   winners={', '.join(uniq)}", 1)
                for k in sorted(loo_winners.keys()):
                    log(f"  omit {k:6s} -> {loo_winners[k]}", 1)

            # store in summary
            summary["loo_winners"] = loo_winners
            summary["loo_counts"] = loo_counts
            summary["loo_consensus"] = consensus

    if PRINT_DELTA8_PEAKS:
        # Refine the visible peak locations (avoid binning artifacts)
        # bins are derived from δ0^2 to avoid arbitrary choices.
        bins_delta8 = max(200, int(round(8.0 / (DELTA_0 ** 2))))
        bins_mod1 = max(200, int(round(1.0 / (DELTA_0 ** 2))))

        section("=== δ8 peaks (refined histogram) ===", 1)
        peaks8 = top_hist_peaks(ddf["delta8"].to_numpy(float), 0.0, 8.0, bins=bins_delta8, topk=5)
        for c, cnt in peaks8:
            log(f"  peak@{c:.4f}  count={cnt}", 1)

        section("=== δ8(mod1) peaks (refined histogram) ===", 1)
        mod1_all = pool_mod1["ALL"]
        peaks1 = top_hist_peaks(mod1_all, 0.0, 1.0, bins=bins_mod1, topk=5)
        for c, cnt in peaks1:
            log(f"  peak@{c:.4f}  count={cnt}", 1)

        section("=== δ8(mod1) peaks by pool ===", 1)
        for pname in ["ALL", "NO_NUC", "HAD", "NUC"]:
            arr = pool_mod1[pname]
            if arr.size == 0:
                continue
            pk = top_hist_peaks(arr, 0.0, 1.0, bins=bins_mod1, topk=3)
            s = ", ".join([f"{c:.4f}({cnt})" for c, cnt in pk])
            log(f"  {pname:6s}: {s}", 1)

    if _run_boot:
        # Non-parametric stability check across stable pools (no new hypotheses).
        # Reps are derived: reps := ceil(1/δ0^2) = N_MIN_STABLE.
        reps = int(N_MIN_STABLE)
        rng = np.random.default_rng(12345)

        # Use the same stable pool_list as ranking if available; otherwise derive it.
        try:
            pool_list_boot = [p for p in ["ALL", "NO_NUC", "HAD", "NUC", "FUND"] if pool_best[p][2] >= MIN_POOL_N]
        except Exception:
            pool_list_boot = ["ALL", "NO_NUC", "HAD", "NUC"]

        section("=== seam bootstrap (stable pools, H1..H5) ===", 1)
        log(f"reps={reps}  pools={pool_list_boot}", 1)

        for pname in pool_list_boot:
            arr = pool_mod1.get(pname, np.asarray([], dtype=float))
            if arr.size < 50:
                log(f"{pname:6s}: skipped (N={arr.size} < 50)", 1)
                continue

            # Count which hypothesis is best (min mean-dist) on each bootstrap replicate.
            counts: Dict[str, int] = {hname: 0 for hname, _ in H}
            # Track |a_best - a_h| for each hypothesis as a stability diagnostic.
            dA: Dict[str, List[float]] = {hname: [] for hname, _ in H}

            for _ in range(reps):
                sample = rng.choice(arr, size=arr.size, replace=True)
                a_b, sc_b = best_offset_mod1_refined(sample, coarse=4000, fine=4000, span_steps=4)

                # Evaluate all 5 hypotheses on this replicate
                best_h = None
                best_gap = float("inf")
                best_da = float("inf")
                for hname, a in H:
                    m_mean, _ = obj_mean_median(sample, a)
                    gap = float(m_mean - sc_b)
                    da = float(abs(a - a_b))
                    dA[hname].append(da)
                    if (gap < best_gap) or (abs(gap - best_gap) <= 1e-15 and da < best_da) or (abs(gap - best_gap) <= 1e-15 and abs(da - best_da) <= 1e-15 and (best_h is None or hname < best_h)):
                        best_gap = gap
                        best_da = da
                        best_h = hname

                if best_h is not None:
                    counts[best_h] += 1

            # Print winner rates + median |Δa| to the bootstrap best a
            items = sorted([(h, counts[h]) for h, _ in H], key=lambda t: (-t[1], t[0]))
            top = items[0][0]
            log(f"{pname:6s}: N={arr.size:5d}  top={top}  hit_rate={counts[top]/reps:.3f}", 1)
            for hname, _a in H:
                med_da = float(np.median(np.asarray(dA[hname], dtype=float))) if len(dA[hname]) else math.nan
                log(f"  {hname:20s}  hits={counts[hname]:3d}/{reps}  rate={counts[hname]/reps:.3f}  med|Δa|={med_da:.3e}", 1)

    return summary


# =============================================================================
# 7) Anchor + errors
# =============================================================================
def apply_anchor_and_errors(master: pd.DataFrame) -> float:
    e_row = master.loc[(master["pdgid"] == 11) & master["mass_MeV"].notna()].iloc[0]
    anchor_log10_M0 = float(math.log10(float(e_row["mass_MeV"])) - float(e_row["log10_pred"]))
    master["m_pred"] = np.power(10.0, anchor_log10_M0 + master["log10_pred"])
    master["rel_err"] = (master["m_pred"] - master["mass_MeV"]) / master["mass_MeV"]

    section(f"M0 (anchor) = {10 ** anchor_log10_M0:.6e} MeV", 1)
    log(f"median |rel_err| (all) = {master['rel_err'].abs().median():.4e}", 1)
    log(f"electron lattice: n={e_row['n']:.0f} k={e_row['k']:.0f} κ={e_row['kappa']:.0f}  Δlog10={e_row['delta_log10']:.3e}  err_quanta={e_row['err_quanta']:.3e}  C={e_row['complexity']:.0f}", 2)
    return anchor_log10_M0


def report_errors_by_type(master: pd.DataFrame, title: str, mask: Optional[pd.Series] = None) -> None:
    df = master if mask is None else master.loc[mask]
    sub = df.dropna(subset=["rel_err"]).copy()
    if sub.empty:
        return
    section(title, 1)
    log(f"N={len(sub)}  median|rel|={sub['rel_err'].abs().median():.4e}", 1)

    if not SHOW_TYPE_BREAKDOWN:
        return

    # Compact per-type medians (no q90/q99 spam)
    for t in ["lepton", "gauge", "quark", "baryon", "meson", "other", "nucleus"]:
        g = sub[sub["type"] == t]
        if g.empty:
            continue
        log(f"  {t:8s} N={len(g):5d}  median|rel|={g['rel_err'].abs().median():.4e}", 1)


# =============================================================================
# 8) Audits (compact)
# =============================================================================
def run_audits(master: pd.DataFrame) -> None:
    if not RUN_AUDITS:
        return
    audit = master.copy()

    # Charge quantization (3Q integer)
    qmask = audit["charge_e_pdg"].notna()
    if qmask.any():
        audit.loc[qmask, "Q3"] = np.round(3.0 * audit.loc[qmask, "charge_e_pdg"].astype(float))
        audit.loc[qmask, "Q3_err"] = (3.0 * audit.loc[qmask, "charge_e_pdg"].astype(float) - audit.loc[qmask, "Q3"]).abs()

        section("=== Charge audit ===", 1)
        log(f"charge known: {int(qmask.sum())}/{len(audit)}  median|3Q-round|={audit.loc[qmask,'Q3_err'].median():.3e}", 1)
        for t, g in audit.loc[qmask].groupby("type"):
            log(f"  {t:8s} N={len(g):5d}  unique Q3 count={g['Q3'].nunique()}", 2)

    # Spin quantization (2J integer)
    smask = audit["J_pdg"].notna()
    if smask.any():
        audit.loc[smask, "J2"] = np.round(2.0 * audit.loc[smask, "J_pdg"].astype(float))
        audit.loc[smask, "J2_err"] = (2.0 * audit.loc[smask, "J_pdg"].astype(float) - audit.loc[smask, "J2"]).abs()

        section("=== Spin audit ===", 1)
        log(f"spin known: {int(smask.sum())}/{len(audit)}  median|2J-round|={audit.loc[smask,'J2_err'].median():.3e}", 1)
        for t, g in audit.loc[smask].groupby("type"):
            log(f"  {t:8s} N={len(g):5d}  unique 2J count={g['J2'].nunique()}", 2)

    # Helix residual |Hφ-round(Hφ)|
    if "H_phi" in audit.columns:
        hmask = audit["H_phi"].notna()
        if hmask.any():
            dist = np.abs(audit.loc[hmask, "H_phi"].astype(float) - np.round(audit.loc[hmask, "H_phi"].astype(float)))
            section("=== Helix quantization (Hφ → ℤ) ===", 1)
            log(f"N={int(hmask.sum())}  median={float(np.median(dist)):.4e}  q90={float(np.quantile(dist,0.9)):.4e}", 1)

    # δ8 by charge/spin (optional heavy)
    if ("delta8" in audit.columns) and audit["delta8"].notna().any():
        dmask = audit["delta8"].notna()
        audit.loc[dmask, "delta8_mod1"] = np.mod(audit.loc[dmask, "delta8"].astype(float), 1.0)

        if PRINT_DELTA8_BY_CHARGE_SPIN:
            section("=== δ8(mod1) by charge Q3 ===", 1)
            if qmask.any():
                for q3, g in audit.loc[dmask & qmask].groupby("Q3"):
                    if len(g) < 20:
                        continue
                    a_q, sc_q = best_offset_mod1(g["delta8_mod1"].to_numpy(float), grid=1500)
                    log(f"  Q3={int(q3):>4d} N={len(g):5d}  med={g['delta8_mod1'].median():.4f}  best a≈{a_q:.4f}  score={sc_q:.2e}", 1)

            section("=== δ8(mod1) by spin 2J ===", 1)
            if smask.any():
                for j2, g in audit.loc[dmask & smask].groupby("J2"):
                    if len(g) < 20:
                        continue
                    a_j, sc_j = best_offset_mod1(g["delta8_mod1"].to_numpy(float), grid=1500)
                    log(f"  2J={int(j2):>2d} N={len(g):5d}  med={g['delta8_mod1'].median():.4f}  best a≈{a_j:.4f}  score={sc_j:.2e}", 1)

        # always print compact summary
        n_q3 = int(audit.loc[dmask & qmask, "Q3"].nunique()) if qmask.any() else 0
        n_j2 = int(audit.loc[dmask & smask, "J2"].nunique()) if smask.any() else 0
        log(f"δ8(mod1) groups: Q3={n_q3}  2J={n_j2}  (details={'ON' if PRINT_DELTA8_BY_CHARGE_SPIN else 'OFF'})", 1)


# =============================================================================
# 9) Core-13 geometry (kept, but no debug spam)
# =============================================================================
def line_ABC(p: Tuple[float, float], q: Tuple[float, float]) -> Tuple[float, float, float]:
    (x1, y1), (x2, y2) = p, q
    A = (y2 - y1)
    B = (x1 - x2)
    C = A * x1 + B * y1
    return float(A), float(B), float(C)


def intersect_lines(L1, L2) -> Optional[Tuple[float, float]]:
    A1, B1, C1 = L1
    A2, B2, C2 = L2
    det = A1 * B2 - A2 * B1
    if abs(det) < 1e-12:
        return None
    x = (C1 * B2 - C2 * B1) / det
    y = (A1 * C2 - A2 * C1) / det
    return float(x), float(y)


def point_line_distance(point: Tuple[float, float], L) -> float:
    x, y = point
    A, B, C = L
    return abs(A * x + B * y - C) / math.sqrt(A * A + B * B)


def fit_circle_ls(x: np.ndarray, y: np.ndarray) -> Tuple[float, float, float]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if len(x) < 3:
        return (math.nan, math.nan, math.nan)
    A = np.column_stack([2 * x, 2 * y, np.ones_like(x)])
    b = x * x + y * y
    cx, cy, c = np.linalg.lstsq(A, b, rcond=None)[0]
    r = math.sqrt(max(0.0, cx * cx + cy * cy + c))
    return float(cx), float(cy), float(r)


def circle_residuals(x: np.ndarray, y: np.ndarray, cx: float, cy: float, r: float) -> Tuple[float, float]:
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    res = d - r
    rms = float(np.sqrt(np.mean(res ** 2)))
    mx = float(np.max(np.abs(res)))
    return rms, mx


def wrap13(delta: float) -> float:
    return ((delta + 6.5) % 13.0) - 6.5


def unwrap_H13(value: float, ref: float) -> float:
    return ref + wrap13(value - ref)


def run_core_geometry(master: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Tuple[float, float, float, float, float]]]:
    if not RUN_CORE_GEOMETRY:
        return pd.DataFrame(), {}

    CORE_PDGIDS = [12, 5, 1, 15, 24, 13, 3, 4, 23, 11, 2, 6, 25]
    core = master[master["pdgid"].isin(CORE_PDGIDS)].copy()
    core["id"] = core["pdgid"].map({pid: i + 1 for i, pid in enumerate(CORE_PDGIDS)})
    core = core.sort_values("id").reset_index(drop=True)
    core = core[core["H_phi"].notna()].copy()
    core["n_abs"] = np.abs(core["n"])

    node_light = pd.DataFrame([dict(pdgid=0, id=1, type="light", n_abs=0.0, H13=0.0, H_phi=0.0, name_pdg="γ")])
    core_nodes = pd.concat([node_light, core], ignore_index=True)
    core_nodes = core_nodes.drop_duplicates("id", keep="first")

    core7 = core_nodes.loc[core_nodes["pdgid"] == 3].iloc[0]  # s-quark as reference
    CORE_X, CORE_Y = float(core7["n_abs"]), float(core7["H13"])

    core_nodes["H13_u"] = core_nodes["H13"].apply(lambda v: unwrap_H13(float(v), CORE_Y))
    core_nodes["dH_u"] = core_nodes["H13_u"] - CORE_Y
    core_nodes["r_from_7"] = np.sqrt((core_nodes["n_abs"] - CORE_X) ** 2 + core_nodes["dH_u"] ** 2)
    core_nodes["theta"] = np.arctan2(core_nodes["dH_u"], core_nodes["n_abs"] - CORE_X)

    shell_defs = {"A": [1, 2, 3, 10, 11], "B": [4, 5, 8, 9], "C": [2, 3, 12, 13]}
    shell_params: Dict[str, Tuple[float, float, float, float, float]] = {}

    section("=== Core-13 shells ===", 1)
    for lbl, ids in shell_defs.items():
        sub = core_nodes[core_nodes["id"].isin(ids)]
        x = sub["n_abs"].to_numpy(float)
        y = sub["H13_u"].to_numpy(float)
        cx, cy, r = fit_circle_ls(x, y)
        if not np.isfinite(r):
            log(f"shell {lbl}: insufficient points", 1)
            shell_params[lbl] = (math.nan, math.nan, math.nan, math.nan, math.nan)
            continue
        rms, mx = circle_residuals(x, y, cx, cy, r)
        log(f"shell {lbl}: r={r:.3f}  rms={rms:.4f} ({rms/DELTA_0:.3f}·δ0)  max={mx:.4f} ({mx/DELTA_0:.3f}·δ0)", 1)
        shell_params[lbl] = (cx, cy, r, rms, mx)

    rA, rB, rC = shell_params["A"][2], shell_params["B"][2], shell_params["C"][2]
    if np.isfinite(rA) and np.isfinite(rB) and np.isfinite(rC):
        r0 = rB / (PHI ** 2)
        log(f"φ-hierarchy: rA/(φ^4 r0)={rA/(PHI**4*r0):.3f}  rC/(φ^6 r0)={rC/(PHI**6*r0):.3f}", 1)

    # line checks
    pts = {
        pid: (
            float(core_nodes.loc[core_nodes["id"] == pid, "n_abs"].iloc[0]),
            float(core_nodes.loc[core_nodes["id"] == pid, "H13_u"].iloc[0]),
        )
        for pid in [2, 4, 5, 8, 10, 6, 11, 9, 7, 3, 12, 13]
        if not core_nodes.loc[core_nodes["id"] == pid].empty
    }
    if 2 in pts and 8 in pts and 5 in pts and 4 in pts:
        L28 = line_ABC(pts[2], pts[8])
        L54 = line_ABC(pts[5], pts[4])
        inter = intersect_lines(L28, L54)
        if inter:
            vec = (pts[4][0] - pts[5][0], pts[4][1] - pts[5][1])
            denom = vec[0] ** 2 + vec[1] ** 2
            t = float(((inter[0] - pts[5][0]) * vec[0] + (inter[1] - pts[5][1]) * vec[1]) / denom) if denom > 1e-12 else math.nan
            log(f"intersection (2-8)×(5-4) = {inter},  fraction along 5→4 = {t:.3f}", 1)

        if 10 in pts:
            dist_e = point_line_distance(pts[10], L28)
            log(f"e deviation from line(2-8): {dist_e:.6f} ({dist_e/DELTA_0:.3f}·δ0)", 1)

    # parabola intersection (kept, no debug spam)
    ids_H6 = [11, 9, 6, 7, 3]
    ids_H7 = [6, 12, 13]
    s6 = core_nodes[core_nodes["id"].isin(ids_H6)]
    s7 = core_nodes[core_nodes["id"].isin(ids_H7)]
    if len(s6) >= 3 and len(s7) >= 3:
        x6, y6 = s6["n_abs"].to_numpy(float), s6["H13_u"].to_numpy(float)
        x7, y7 = s7["n_abs"].to_numpy(float), s7["H13_u"].to_numpy(float)
        if np.isfinite(x6).all() and np.isfinite(y6).all() and np.isfinite(x7).all() and np.isfinite(y7).all():
            c6 = np.polyfit(x6, y6, 2)
            c7 = np.polyfit(x7, y7, 2)
            A_q, B_q, C_q = (c6[0] - c7[0]), (c6[1] - c7[1]), (c6[2] - c7[2])
            disc = B_q ** 2 - 4 * A_q * C_q
            if disc >= 0 and abs(A_q) > 1e-12:
                roots = [(-B_q + math.sqrt(disc)) / (2 * A_q), (-B_q - math.sqrt(disc)) / (2 * A_q)]
                p6 = pts.get(6)
                if p6:
                    X = min(roots, key=lambda v: abs(v - p6[0]))
                    Y = float(np.polyval(c6, X))
                    dist_mu = float(math.hypot(X - p6[0], Y - p6[1]))
                    log(f"parabola intersection ≈ ({X:.3f},{Y:.3f}), dist(μ)={dist_mu:.3f} ({dist_mu/DELTA_0:.3f}·δ0)", 1)

    return core_nodes, shell_params


# =============================================================================
# 10) Baselines + outliers
# =============================================================================
def report_outliers_and_baselines(master: pd.DataFrame, anchor_log10_M0: float) -> None:
    if not RUN_BASELINES:
        return

    # outliers
    out = master.dropna(subset=["rel_err"]).copy()
    out["abs_rel"] = out["rel_err"].abs()
    worst = out.nlargest(int(PRINT_TOP_OUTLIERS), "abs_rel")

    if PRINT_TOP_OUTLIERS > 0:
        section("Top worst (|rel_err|)", 1)
        for _, r in worst.iterrows():
            name = str(r.get("name_pdg") if pd.notna(r.get("name_pdg")) else (r.get("name_mc") if pd.notna(r.get("name_mc")) else "?"))
            log(f"pdgid={int(r['pdgid']):>12d}  {name:>10s}  type={str(r['type']):<8s}  mass={float(r['mass_MeV']):.3e}  |err|={float(r['abs_rel']):.3e}  (n={r['n']:.0f} k={r['k']:.0f} κ={r['kappa']:.0f} C={r['complexity']:.0f})", 1)

    # baseline 1: permute log10_pred
    base = master[["mass_MeV", "log10_pred"]].dropna().copy().reset_index(drop=True)
    if len(base) > 10:
        perm = base["log10_pred"].sample(frac=1.0, random_state=42).to_numpy(float)
        mass_arr = base["mass_MeV"].to_numpy(float)
        pred_perm = np.power(10.0, anchor_log10_M0 + perm)
        rel_perm = (pred_perm - mass_arr) / mass_arr
        log(f"Baseline permute(log10_pred): median|rel|={float(np.median(np.abs(rel_perm))):.3e}", 1)

        rng = np.random.default_rng(123)
        idx = rng.integers(0, len(B_LOG), size=len(mass_arr))
        pred_rand = np.power(10.0, anchor_log10_M0 + B_LOG[idx])
        rel_rand = (pred_rand - mass_arr) / mass_arr
        log(f"Baseline random lattice:       median|rel|={float(np.median(np.abs(rel_rand))):.3e}", 1)


# =============================================================================
# 11) Plots (minimal)
# =============================================================================
def _savefig(fig: plt.Figure, name: str) -> None:
    fig.savefig(PLOT_DIR / name, dpi=150)
    plt.close(fig)


def _type_colors() -> Dict[str, str]:
    return {
        "quark": "green",
        "lepton": "orange",
        "gauge": "royalblue",
        "meson": "purple",
        "baryon": "red",
        "nucleus": "gray",
        "other": "black",
        "light": "yellow",
    }


def plot_basic(master: pd.DataFrame, core_nodes: pd.DataFrame, shell_params: Dict[str, Tuple[float, float, float, float, float]]) -> None:
    if not RUN_PLOTS:
        return

    colors = _type_colors()

    # scatter |n| vs H13
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    for t, g in master.groupby("type"):
        g = g.dropna(subset=["n", "H13"])
        if g.empty:
            continue
        ax.scatter(np.abs(g["n"]), g["H13"], s=4, alpha=0.25, c=colors.get(t, "black"), label=t)
    if not core_nodes.empty:
        cc = core_nodes.dropna(subset=["n_abs", "H13"])
        ax.scatter(cc["n_abs"], cc["H13"], s=70, facecolors="none", edgecolor="k", lw=1.2)
    ax.set_xlabel("|n|"); ax.set_ylabel("H13"); ax.set_title("PDG scatter: |n| vs H13")
    ax.grid(alpha=0.3); ax.legend(fontsize=8, ncols=2)
    plt.tight_layout(); _savefig(fig, "phi_pdg_scatter.png")

    # rel_err hist
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.hist(master["rel_err"].abs().dropna(), bins=60, log=True)
    ax.set_xlabel("|rel_err|"); ax.set_ylabel("count (log)"); ax.set_title("|rel_err| distribution")
    ax.grid(alpha=0.3)
    plt.tight_layout(); _savefig(fig, "phi_pdg_relerr_hist.png")

    # δ8 hist + mod1
    ddf = master.dropna(subset=["delta8"]).copy()
    if not ddf.empty:
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.hist(ddf["delta8"].astype(float), bins=160, range=(0, 8), alpha=0.7)
        ax.axvline(DELTA_STAR, linestyle="--", linewidth=2.0, color="k", label="δ*=2π/9")
        ax.set_xlabel("δ8 (mod 8)"); ax.set_ylabel("count"); ax.set_title("δ8 distribution")
        ax.grid(alpha=0.3); ax.legend(fontsize=9)
        plt.tight_layout(); _savefig(fig, "phi_delta8_hist.png")

        mod1 = np.mod(ddf["delta8"].astype(float).to_numpy(), 1.0)
        a_best, _ = best_offset_mod1(mod1, grid=4000)
        fig, ax = plt.subplots(1, 1, figsize=(10, 4))
        ax.hist(mod1, bins=200, range=(0, 1), alpha=0.75)
        ax.axvline(a_best, linestyle="--", linewidth=2.0, color="k", label=f"best a≈{a_best:.4f}")
        ax.axvline(3.0 / 8.0, linestyle=":", linewidth=2.0, color="k", label="3/8")
        ax.axvline(float(np.mod(DELTA_STAR, 1.0)), linestyle="-.", linewidth=2.0, color="k", label="(2π/9) mod1")
        ax.set_xlabel("δ8 mod 1"); ax.set_ylabel("count"); ax.set_title("δ8 comb (mod 1)")
        ax.grid(alpha=0.3); ax.legend(fontsize=9)
        plt.tight_layout(); _savefig(fig, "phi_delta8_mod1.png")

    # core shells plot
    if not core_nodes.empty and shell_params:
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        for _, row in core_nodes.iterrows():
            if not np.isfinite(row.get("n_abs", np.nan)) or not np.isfinite(row.get("H13_u", np.nan)):
                continue
            ax.scatter(float(row["n_abs"]), float(row["H13_u"]), s=70, c=colors.get(str(row.get("type", "other")), "black"), edgecolor="k")
            ax.text(float(row["n_abs"]) + 0.1, float(row["H13_u"]) + 0.1, str(int(row["id"])), fontsize=8)
        theta = np.linspace(0, 2 * np.pi, 400)
        for lbl, (cx, cy, r, _, _) in shell_params.items():
            if not np.isfinite(r):
                continue
            ax.plot(cx + r * np.cos(theta), cy + r * np.sin(theta), lw=2.0, label=f"shell {lbl}")
        ax.set_xlabel("|n|"); ax.set_ylabel("H13 (unwrapped)"); ax.set_title("Core-13 shells")
        ax.grid(alpha=0.3); ax.legend(fontsize=9)
        plt.tight_layout(); _savefig(fig, "phi_core_shells.png")


# =============================================================================
# 12) MAIN
# =============================================================================
def main() -> int:
    section("=== Φ–PDG strict (canonical) ===", 1)
    log(f"φ={PHI:.15f}, ψ={PSI:.15f}, δ₀={DELTA_0:.15f}", 1)
    if VERBOSE >= 2:
        F13 = fibonacci(13); L13 = lucas(13)
        K_E = 2 ** 23 * (2 * math.pi) ** 3 * PHI ** (F13 / 4)
        H_E = math.log10(K_E) / DELTA_0
        log(f"F(13)={F13}, L(13)={L13}, H_e={H_E:.2f}", 2)
        log(f"π0(CORE)={PI0:.10f}  π(BRIDGE)={PI:.10f}  Δ={PI0-PI:+.3e}", 2)
        log(f"c_SI={C_SI}, 1 MeV={MEV_TO_J:.6e} J, m_e={M_E_MEV:.9f} MeV => {mev_to_kg(M_E_MEV):.6e} kg", 2)

    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", default=os.environ.get("D0_PROTOCOL", "protocols/phi_pdg_strict.json"))
    args = ap.parse_args()

    PROT = load_protocol(args.protocol)
    OUTDIR = get_outdir() / "cert_phi_pdg_strict"
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rep = CertReport(cert_id="PHI_PDG_STRICT", protocol_id=PROT.protocol_id)

    master = build_master()
    rep.add(
        "PDG_DATASET",
        True,
        year=PDG_YEAR,
        file=MW_FILE.name,
        sha256=PDG_SHA256,
        path=relpath_for_report(MW_FILE),
    )
    log(f"MASTER particles: {len(master)}", 1)
    log(f"types: {master['type'].value_counts().to_dict()}", 2)

    hold = P(PROT, "holdout", {"enabled": True, "seed": 20250101, "fraction": 0.2})
    hold_enabled = bool(hold.get("enabled", True))
    hold_seed = int(hold.get("seed", 20250101))
    hold_frac = float(hold.get("fraction", 0.2))

    def _is_holdout(pdgid: int) -> bool:
        msg = f"{hold_seed}:{pdgid}".encode("utf-8")
        h = hashlib.sha256(msg).digest()
        x = int.from_bytes(h[:8], "big") / 2**64
        return x < hold_frac

    m_train = None
    m_hold = None


    section("=== CORE CERTIFICATES (parameter-free) ===", 1)

    # -------------------------------------------------------------------------
    # CORE kill-switch certificates (make them explicit in the log)
    # -------------------------------------------------------------------------
    alpha_summary = report_seam_alpha()
    mup_summary = tom16_variant_bpp_report(master)

    section("=== KILL-SWITCH panel (CORE) ===", 1)
    if alpha_summary:
        log(f"F-α (Seam): PASS={bool(alpha_summary.get('alpha_pass', 0.0))}  Δα={alpha_summary.get('delta_alpha', float('nan')):.6e}  eps²={EPS2:.6e}", 1)
    if mup_summary:
        log(f"F-μ: PASS={bool(mup_summary.get('mu_pass', 0.0))}  relerr={mup_summary.get('mu_rel', float('nan')):.6e}  eps²={EPS2:.6e}", 1)
        log(f"F-p: PASS={bool(mup_summary.get('p_pass', 0.0))}  relerr={mup_summary.get('p_rel', float('nan')):.6e}  eps²={EPS2:.6e}", 1)


    # lattice fit
    fits = master["log10_m"].apply(fit_lattice_log10)
    master = master.join(pd.DataFrame([f.__dict__ for f in fits]))

    if hold_enabled:
        m_train = master[~master["pdgid"].astype(int).apply(_is_holdout)].copy()
        m_hold = master[ master["pdgid"].astype(int).apply(_is_holdout)].copy()
    else:
        m_train, m_hold = master.copy(), master.iloc[0:0].copy()

    log(f"HOLDOUT enabled={hold_enabled} train={len(m_train)} holdout={len(m_hold)}", 1)
    rep.add(
        "PROTO_HOLDOUT",
        True,
        enabled=hold_enabled,
        seed=hold_seed,
        fraction=hold_frac,
        train_N=int(len(m_train)),
        holdout_N=int(len(m_hold)),
    )

    # heights with electron anchor (BOOK III)
    F13 = fibonacci(13)
    K_E = 2 ** 23 * (2 * math.pi) ** 3 * PHI ** (F13 / 4)
    H_E = math.log10(K_E) / DELTA_0
    master["H_phi"] = np.where(
        master["log10_m"].notna(),
        H_E + (master["log10_m"] - LOG10_ME) / DELTA_0,
        np.nan,
    )
    master["H13"] = np.mod(master["H_phi"], 13.0)

    section("=== VERIFICATION / STAT BLOCK (BRIDGE) ===", 1)
    log("NOTE: The following δ8/offset/peaks analyses are statistical diagnostics, not CORE certificates.", 1)

    compute_delta8(master)
    compute_delta8(m_train)
    if len(m_hold) > 0:
        compute_delta8(m_hold)

    report_delta8(m_train)
    _delta8_train = report_delta8_structure(m_train, label="TRAIN")
    if len(m_hold) > 0:
        _delta8_hold = report_delta8_structure(m_hold, label="HOLDOUT")
    else:
        _delta8_hold = None
    if RUN_DELTA8_SENSITIVITY:
        _base = report_delta8_structure(
            m_train,
            label="BASE",
            dedup_abs_pdgid_non_nuc=True,
            dedup_abs_pdgid_nuc=False,
            run_seam_bootstrap=False,
        )
        _dedn = report_delta8_structure(
            m_train,
            label="DEDUP_NUC",
            dedup_abs_pdgid_non_nuc=True,
            dedup_abs_pdgid_nuc=True,
            run_seam_bootstrap=False,
        )

        section("=== δ8 sensitivity summary (BASE vs DEDUP_NUC) ===", 1)
        for pool in ["ALL", "NO_NUC", "HAD", "NUC"]:
            b = (_base.get("pool_winner", {}) or {}).get(pool, {})
            d = (_dedn.get("pool_winner", {}) or {}).get(pool, {})
            if not b or not d:
                continue
            log(
                f"{pool:6s}: BASE win={b.get('win')} | DEDUP_NUC win={d.get('win')}",
                1,
            )
        log(f"rank_winner: BASE={_base.get('rank_winner')}  DEDUP_NUC={_dedn.get('rank_winner')}", 1)
        log(f"minimax_winner: BASE={_base.get('minimax_winner')}  DEDUP_NUC={_dedn.get('minimax_winner')}", 1)

    mt = P(PROT, "multiple_testing", {"method": "bonferroni", "families": ["delta8_hypotheses"]})
    rep.add("PROTO_MULTIPLE_TESTING", True, **mt)

    anchor_log10_M0 = apply_anchor_and_errors(master)
    report_errors_by_type(master, "Errors (summary)")

    # run_audits(master)   # audits block removed per instructions

    core_nodes, shell_params = run_core_geometry(master)

    report_outliers_and_baselines(master, anchor_log10_M0)

    plot_basic(master, core_nodes, shell_params)

    try:
        passed = bool(alpha_summary.get("PASS", alpha_summary.get("alpha_pass", True)))
        rep.add("ALPHA_SEAM", passed, **alpha_summary)
    except Exception:
        rep.skip("ALPHA_SEAM", "alpha_summary not available")

    out_json = OUTDIR / P(PROT, "outputs")["json"]
    save_json(out_json, rep.to_dict())

    log(f"\nDone. Outputs saved to {BASE_OUTDIR.as_posix()}/", 1)

    overall_pass = True
    if alpha_summary:
        overall_pass = overall_pass and bool(alpha_summary.get("alpha_pass", alpha_summary.get("PASS", 1)))
    if mup_summary:
        overall_pass = overall_pass and bool(mup_summary.get("mu_pass", 1.0)) and bool(mup_summary.get("p_pass", 1.0))

    return 0 if overall_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
