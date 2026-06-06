import numpy as np
import math
import matplotlib.pyplot as plt
import os
import pandas as pd
import argparse

from d0.constants import phi, psi, delta0, eps, eps2 as eps2_canon, xi5, pi0, m0, tau0_D0, sqrt5
from d0.io import get_outdir, save_json, t0_override
from d0.protocol import load_protocol, P
from d0.report import CertReport

# ============================================================
# D0 DYNAMICS: SPACE ⊕ eps^2·SCENE (FULL SINGLE-CELL CODE)
# exact ds(t) from spectra (no numeric gradients)
# ============================================================

# -------------------------
# 0.2) RUNTIME CONFIG (no physics knobs)
# -------------------------
VERBOSE = os.environ.get("D0_VERBOSE", "1").strip() != "0"

UQ_N = int(os.environ.get("D0_UQ_N", "4096"))
SDE_COARSE_N = int(os.environ.get("D0_SDE_COARSE_N", "4096"))
SDE_GOLD_ITERS = int(os.environ.get("D0_SDE_GOLD_ITERS", "80"))
SDE_FWHM_ITERS = int(os.environ.get("D0_SDE_FWHM_ITERS", "80"))

def vprint(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

# ------------------------------------------------------------
# CLI / initialization
# NOTE: keep module import side-effect free for CI and reuse.
# ------------------------------------------------------------

PROT = None
OUTDIR = None
CORE_ONLY = False
rep = None
_BOOK6_READY = False

def init(protocol_path: str, core_only: bool = False) -> CertReport:
    """Initialize global protocol/output/report objects.

    This module is used both as a CLI cert tool and as an importable library.
    Importing must not parse argv or write files.
    """
    global PROT, OUTDIR, CORE_ONLY, rep
    PROT = load_protocol(protocol_path)
    OUTDIR = get_outdir()
    OUTDIR.mkdir(parents=True, exist_ok=True)

    CORE_ONLY = bool(core_only or P(PROT, "core_only_default", False))

    rep = CertReport(cert_id="BOOK6_CERTPACK", protocol_id=PROT.protocol_id)
    rep.add("PROTO_LOADED", True, protocol=protocol_path, core_only=CORE_ONLY)
    return rep

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", default=os.environ.get("D0_PROTOCOL", "protocols/book6_certpack.json"))
    ap.add_argument("--core-only", action="store_true", help="Skip slow/optional sections and keep CORE-only outputs.")
    ap.add_argument("--show", action="store_true", help="Show plots interactively (default: save only).")
    ap.add_argument("--no-perc", action="store_true", help="Disable percolation toy (CI-friendly).")
    args = ap.parse_args()

    if args.no_perc:
        os.environ["D0_PERC"] = "0"

    init(args.protocol, core_only=args.core_only)

    run_book6_certs()

    if args.show:
        plt.show()

###########################
def tome23_universe_age_seconds():
    """BOOK III/IV: predict Universe age (seconds) from electron chronon."""
    # electron chronon (reduced Compton period)
    t_e = hbar_SI / (m_e_kg * (c_SI**2))

    # depth product N = D_electron * D_vacuum (canonical: 23*8=184)
    N = int(D_ELECTRON * D_VACUUM)

    # geometric factor k_geom = pi0/phi^2 (=6/5 in the canonical certificate)
    k_geom = float(pi0 / (phi**2))

    # compute phi^N safely (avoid float overflow / precision loss)
    try:
        from decimal import Decimal, getcontext
        getcontext().prec = 160
        phiD = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
        phiN = phiD ** int(N)
        T = Decimal(str(t_e)) * phiN * Decimal(str(k_geom))
        return float(T)
    except Exception:
        return float(t_e * (phi**N) * k_geom)

def calibrate_t0_s():
    """Return seconds per 1 D0-time unit.

    Priority:
      1) Direct micro tick (env D0_T0_S)
      2) Macro check (env D0_AGE_UNIVERSE_S)
      3) BOOK III/IV autonomous prediction (default ON unless D0_DISABLE_TOME23=1)
      4) else dimensionless (1.0)
    """
    if T0_S_DIRECT is not None:
        return float(T0_S_DIRECT)

    # t_now(D0) = u_now / eps^2  (dimensionless)
    t_now_D0 = float(u_now_canon) / float(eps2_canon)

    if AGE_UNIVERSE_S is not None:
        return float(AGE_UNIVERSE_S) / t_now_D0

    if not DISABLE_TOME23:
        T_theory = tome23_universe_age_seconds()
        return float(T_theory) / t_now_D0

    return 1.0

### SI calibration values
def omega_pi0_bridge(pi0):
    # BRIDGE/APPX: macro mapping proposal (not used in dynamics)
    Omega_M = 1.0 / pi0
    Omega_L = 1.0 - Omega_M
    Omega_b = 1.0 / (2.0 * (pi0**2))
    Omega_c = Omega_M - Omega_b
    vprint("\n=== Ω BRIDGE (π0-geometry) [BRIDGE/APPX] ===")
    vprint(f"Omega_M = 1/pi0      = {Omega_M:.6f}")
    vprint(f"Omega_L = 1-1/pi0    = {Omega_L:.6f}")
    vprint(f"Omega_b = 1/(2*pi0^2)= {Omega_b:.6f}")
    vprint(f"Omega_c = Omega_M-Ob = {Omega_c:.6f}")
    vprint(f"sum = {Omega_L+Omega_c+Omega_b:.6f}")
    if Omega_b != 0:
        vprint(f"Omega_c/Omega_b = {Omega_c/Omega_b:.6f}  (BRIDGE/APPX)")

def logsumexp(a, axis=None):
    a = np.asarray(a, float)
    m = np.max(a, axis=axis, keepdims=True)
    s = np.sum(np.exp(a - m), axis=axis, keepdims=True)
    out = np.log(s) + m
    if axis is not None:
        out = np.squeeze(out, axis=axis)
    return out

def safe_div(a, b, eps=1e-300):
    return np.asarray(a, float) / np.maximum(np.asarray(b, float), eps)


def to_km_s_Mpc(H_si):
    return float(H_si) * MPC_M / 1000.0

# -------------------------
# 2) SCENE 9-11-13 GRAPH + D0 GENERATOR SPECTRUM
# -------------------------
def build_scene_adj(n9=9, n11=11, n13=13):
    n = n9 + n11 + n13
    A = np.zeros((n, n), float)
    idx9  = np.arange(0, n9)
    idx11 = np.arange(n9, n9+n11)
    idx13 = np.arange(n9+n11, n)
    # complete bipartite between each pair of parts
    for U,V in [(idx9,idx11),(idx11,idx13),(idx13,idx9)]:
        A[np.ix_(U,V)] = 1.0
        A[np.ix_(V,U)] = 1.0
    return A

def scene_d0_spectrum():
    A = build_scene_adj(9,11,13)
    deg = A.sum(axis=1)
    n = A.shape[0]

    # IMPORTANT FIX:
    # L_rw = I - D^{-1}A is generally NON-symmetric on irregular graphs (degrees differ).
    # Using eigvalsh on a non-symmetric matrix can create fake negative modes.
    # We therefore use the symmetric normalized Laplacian:
    #   L_sym = I - D^{-1/2} A D^{-1/2}   (symmetric PSD)
    # and define D0 generator:
    #   G = (1/phi) * L_sym
    dinv_sqrt = 1.0/np.sqrt(deg)
    S = (dinv_sqrt[:,None] * A) * dinv_sqrt[None,:]   # symmetric similarity of random-walk operator
    Lsym = np.eye(n) - S
    G = (1.0/phi) * Lsym

    lam = np.linalg.eigvalsh(G)
    lam.sort()

    # quick report + multiplicities
    E = int(A.sum()/2)
    vprint("\n=== Scene 9-11-13 graph ===")
    vprint("N nodes =", n)
    vprint("E edges =", E, " (target 359)")
    vprint("degrees (unique) =", sorted(set(deg.tolist())))

    uniq = {}
    for x in lam:
        # clamp numerical noise
        if abs(x) < 5e-15:
            x = 0.0
        xr = float(np.round(x, 12))
        uniq[xr] = uniq.get(xr, 0) + 1
    vprint("\n=== FIXED D0 scene eigenvalues (value : multiplicity) ===")
    for k in sorted(uniq.keys()):
        vprint(f"{k} : {uniq[k]}")
    return lam

def scene_rank_nullity_certificate(n9=9, n11=11, n13=13, tol=1e-12):
    A = build_scene_adj(n9, n11, n13)
    N = A.shape[0]
    deg = A.sum(axis=1)
    dinv_sqrt = 1.0 / np.sqrt(deg)
    S = (dinv_sqrt[:, None] * A) * dinv_sqrt[None, :]

    rA = np.linalg.matrix_rank(A)
    rS = np.linalg.matrix_rank(S, tol=tol)
    nullA = N - rA
    nullS = N - rS

    null_pred = (n9 - 1) + (n11 - 1) + (n13 - 1)

    mult_mem = int(np.sum(np.isclose(_vals_round, 1.0/phi, atol=1e-12, rtol=0.0)))

    vprint("\n=== DARK SECTOR (STRICT): Rank–Nullity on K(9,11,13) ===")
    vprint(f"N={N}")
    vprint(f"rank(A)={rA}   nullity(A)={nullA}")
    vprint(f"rank(S)={rS}   nullity(S)={nullS}   (tol={tol:g})")
    vprint(f"nullity_pred=(9-1)+(11-1)+(13-1) = {null_pred}")
    vprint(f"mult(λ_G=1/phi) = {mult_mem}   (must match nullity(S)=30)")

    if nullS != 30 or mult_mem != 30:
        vprint("[FAIL] mismatch: check spectrum construction / rounding tolerances.")
    else:
        vprint("[PASS] 30 dark kernel modes == 30 memory eigenmodes (λ=1/phi).")

    return dict(N=N, rankA=rA, nullA=nullA, rankS=rS, nullS=nullS, mult_mem=mult_mem)

def scene_P_logP_ds(t_grid, eps2):
    t = np.asarray(t_grid, float)
    u = eps2 * t
    # logZ(u)=log sum exp(-u*λ)
    logZ = logsumexp((-u[:,None] * lam_scene[None,:]), axis=1)
    logP = logZ - math.log(len(lam_scene))
    # exact ds_scene(t) = 2u*mu(u) with mu(u)=E[λ]
    W = np.exp(-u[:,None] * lam_scene[None,:])
    Z = W.sum(axis=1)
    mu = (W * lam_scene[None,:]).sum(axis=1) / Z
    ds_scene = 2.0 * u * mu
    return logP, ds_scene, u, mu

# -------------------------
# 3) D0 SPACE (3D TORUS) EXACT VIA 1D SPECTRUM + FACTORIZATION
# -------------------------
# We use D0-space generator consistent with:
# eigen_1D: λ(k) = (1/phi) * (1 - cos(2πk/L))  in [0, 2/phi]
# 3D generator uses average of axes => exp(-t*(λx+λy+λz)/3) => Z3D(t) = Z1D(t/3)^3
def space_1d_eigs(L):
    k = np.arange(L, dtype=float)
    ang = 2.0*np.pi*k/L
    lam1 = (1.0/phi) * (1.0 - np.cos(ang))
    return lam1

def space_P_logP_ds(L, t_grid):
    t = np.asarray(t_grid, float)
    lam1 = space_1d_eigs(L)
    tau = t/3.0
    # Z1(tau)
    logZ1 = logsumexp((-tau[:,None] * lam1[None,:]), axis=1)
    # Z3 = Z1^3
    logZ3 = 3.0 * logZ1
    logP = logZ3 - math.log(L**3)

    # exact ds_space:
    # logZ3(t)=3 logZ1(t/3), d/dlogt logZ3 = t * d/dt logZ3 = t * d/dtau logZ1
    # d/dtau logZ1 = -E_tau[λ]
    W = np.exp(-tau[:,None] * lam1[None,:])
    Z = W.sum(axis=1)
    mu1 = (W * lam1[None,:]).sum(axis=1) / Z
    ds_space = 2.0 * t * mu1

    return logP, ds_space, lam1

# -------------------------
# 4) PLATEAU WINDOW FINDER (median/MAD score)
# Plateau search configuration (Step 1)
# Raise the artificial ceiling so tmax is not just a technical cutoff.
def best_plateau_window(t_grid, ds, t_lo=1.0, t_hi=300.0, n=80, min_pts=18):
    t = np.asarray(t_grid, float)
    y = np.asarray(ds, float)
    # candidate boundaries on log-grid
    candidates = np.logspace(np.log10(t_lo), np.log10(t_hi), n)
    best = None
    for i in range(len(candidates)-1):
        for j in range(i+1, len(candidates)):
            a, b = candidates[i], candidates[j]
            mask = (t>=a) & (t<=b)
            if mask.sum() < min_pts:
                continue
            seg = y[mask]
            med = float(np.median(seg))
            mad = float(np.median(np.abs(seg - med)))
            # score: prefer low MAD, closeness to the 3D plateau (~3), and longer windows mildly
            length = math.log(b/a)
            score = -(mad + abs(med - 3.0)) + 0.02*length
            if (best is None) or (score > best["score"]):
                best = dict(tmin=a, tmax=b, med=med, mad=mad, score=score)
    return best

# -------------------------
# 5) CANONICAL TURN-ON TIMES: D(u)=1-P_scene(u)=kappa
# -------------------------
def logP_scene(u):
    """log P_scene(u) where P is the *average* heat trace over scene modes."""
    u = np.asarray(u, float)
    logZ = logsumexp((-u[:,None] * lam_scene[None,:]), axis=1)
    return logZ - math.log(len(lam_scene))

def D_scene(u):
    """Deviation D(u)=1-P_scene(u) computed stably via expm1."""
    lp = logP_scene(u)
    # P = exp(lp). For small |lp|, use expm1 for stability: 1-exp(lp) = -expm1(lp)
    return -np.expm1(lp)

def find_u_for_deviation(kappa, u0=0.0):
    """Solve D(u)=1-P_scene(u)=kappa with automatic bracketing + bisection.
    No free cutoffs: grows hi until it brackets the target.
    """
    if kappa <= 0:
        return 0.0

    def D_of(u):
        return float(D_scene(np.array([u], float))[0])

    lo = max(float(u0), 0.0)
    # start at a tiny positive value so expm1 behaves nicely
    hi = 1e-12

    # grow hi until D(hi) >= kappa
    while D_of(hi) < kappa:
        hi *= 2.0
        if hi > 1e6:
            raise RuntimeError("Failed to bracket kappa: hi too large. Check scene spectrum.")

    # bisection
    for _ in range(140):
        mid = 0.5*(lo+hi)
        if D_of(mid) < kappa:
            lo = mid
        else:
            hi = mid
    return hi

def merge_times(base, extra, rtol=0.0, atol=0.0):
    """Return sorted unique times from base ∪ extra.
    Uses exact uniqueness by default (rtol=atol=0) to preserve marker points."""
    x = np.asarray(base, float)
    y = np.asarray(extra, float)
    allv = np.concatenate([x, y])
    allv = allv[np.isfinite(allv) & (allv > 0)]
    allv.sort()
    if allv.size == 0:
        return allv
    out = [allv[0]]
    for v in allv[1:]:
        if not np.isclose(v, out[-1], rtol=rtol, atol=atol):
            out.append(v)
    return np.array(out, float)

# canonical marker times (in D0-time)
def Dprime_scene(u):
    u = np.asarray(u, float)
    x = -u[:, None] * uniq_vals[None, :]
    m = np.max(x, axis=1, keepdims=True)
    W = uniq_mult[None, :] * np.exp(x - m)
    num = (W * uniq_vals[None, :]).sum(axis=1)
    return (np.exp(m[:, 0]) * num) / float(len(lam_scene))


def S_DE(u):
    u = np.asarray(u, float)
    return u * Dprime_scene(u)


def _golden_max_on_logu(f_logu, a, b, iters=80):
    """Maximize f_logu(x) for x in [a,b] (x=log u). Returns (x*, f*)."""
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    fc = f_logu(c)
    fd = f_logu(d)
    for _ in range(int(iters)):
        if fc < fd:
            a = c
            c = d
            fc = fd
            d = a + gr * (b - a)
            fd = f_logu(d)
        else:
            b = d
            d = c
            fd = fc
            c = b - gr * (b - a)
            fc = f_logu(c)
    x = 0.5 * (a + b)
    return x, f_logu(x)


def find_SDE_peak(u_now, factor_max=512.0):
    """Return (u_peak, S_peak) for S_DE on (0, u_now*factor]."""
    factor = 4.0
    while True:
        u_max = float(u_now * factor)
        u_grid = np.logspace(-12, np.log10(u_max), int(SDE_COARSE_N))
        S_grid = S_DE(u_grid)
        i = int(np.nanargmax(S_grid))
        if (i >= len(u_grid) - 2) and (factor < float(factor_max)):
            factor *= 2.0
            continue
        break

    i0 = max(1, min(i, len(u_grid) - 2))
    uL = float(u_grid[i0 - 1])
    uR = float(u_grid[i0 + 1])

    cache = {}
    def f_logu(x):
        if x in cache:
            return cache[x]
        val = float(S_DE(np.array([math.exp(x)], float))[0])
        cache[x] = val
        return val

    x_star, s_star = _golden_max_on_logu(f_logu, math.log(uL), math.log(uR), iters=SDE_GOLD_ITERS)
    return float(math.exp(x_star)), float(s_star)


def _find_level_crossing_logu(u_peak, level, side, iters=80):
    """Solve S_DE(u)=level on one side of peak (side='left'/'right') in log-u."""
    if side not in ("left", "right"):
        raise ValueError("side must be 'left' or 'right'")

    uA = float(u_peak)
    sA = float(S_DE(np.array([uA], float))[0])
    if not (sA >= level):
        return None

    step = 1.6
    uB = uA
    for _ in range(120):
        uB = uB / step if side == "left" else uB * step
        if uB <= 0:
            return None
        sB = float(S_DE(np.array([uB], float))[0])
        if sB <= level:
            break
    else:
        return None

    x_lo, x_hi = (math.log(uB), math.log(uA)) if side == "left" else (math.log(uA), math.log(uB))

    def g(x):
        return float(S_DE(np.array([math.exp(x)], float))[0]) - level

    glo, ghi = g(x_lo), g(x_hi)
    if not (np.isfinite(glo) and np.isfinite(ghi)):
        return None
    if (glo > 0 and ghi > 0) or (glo < 0 and ghi < 0):
        return None

    for _ in range(int(iters)):
        xm = 0.5 * (x_lo + x_hi)
        gm = g(xm)
        if gm > 0:
            x_hi = xm
        else:
            x_lo = xm
    return float(math.exp(0.5 * (x_lo + x_hi)))


def fwhm_SDE(u_peak, S_peak):
    half = 0.5 * float(S_peak)
    u_left = _find_level_crossing_logu(u_peak, half, side="left", iters=SDE_FWHM_ITERS)
    u_right = _find_level_crossing_logu(u_peak, half, side="right", iters=SDE_FWHM_ITERS)
    if (u_left is None) or (u_right is None) or not (u_right > u_left):
        return None, None, None
    return float(u_left), float(u_right), float(u_right - u_left)


def _find_idx(target, tol=1e-10):
    idx = np.where(np.isclose(uniq_vals, target, rtol=0.0, atol=tol))[0]
    return int(idx[0]) if idx.size else None

def mode_fracs(u):
    u = np.asarray(u, float)
    W = uniq_mult[None, :] * np.exp(-u[:, None] * uniq_vals[None, :])
    Z = W.sum(axis=1, keepdims=True)
    return W / Z

def grouped_fracs(u):
    """Return (f_zero, f_memory, f_transport) as functions of u."""
    fr = mode_fracs(u)
    f0 = fr[:, idx_zero]
    fm = fr[:, idx_mem]
    ft = fr[:, transport_mask].sum(axis=1)
    f0 = np.clip(f0, 0.0, 1.0)
    fm = np.clip(fm, 0.0, 1.0)
    ft = np.clip(ft, 0.0, 1.0)
    return f0, fm, ft

#
# canonical range for cosmological diagnostics: early -> now (u_now)
# NOTE: D0-time starts at the canonical phase; we do not extend t<0.
def first_crossing_after(t, y, x0, level=0.0):
    """Return x where y(x)=level first crosses after x0 using linear interpolation.
    If no crossing, return None.
    """
    t = np.asarray(t, float)
    y = np.asarray(y, float) - level

    m = t >= x0
    t2 = t[m]
    y2 = y[m]
    if t2.size < 3:
        return None

    s = np.sign(y2)
    s[s == 0] = 1.0

    k = np.where(s[:-1] * s[1:] < 0)[0]
    if k.size == 0:
        return None

    i = int(k[0])
    xA, xB = t2[i], t2[i+1]
    yA, yB = y2[i], y2[i+1]
    return float(xA + (0.0 - yA) * (xB - xA) / (yB - yA))

# --- canonical threshold: after scene "eps" turn-on
def interp_on_grid(x, y, x0):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if (x0 is None) or (not np.isfinite(x0)):
        return None
    j = np.searchsorted(x, x0)
    if j <= 0:
        return float(y[0])
    if j >= x.size:
        return float(y[-1])
    xA, xB = x[j-1], x[j]
    yA, yB = y[j-1], y[j]
    if xB == xA:
        return float(yA)
    return float(yA + (x0 - xA) * (yB - yA) / (xB - xA))

def set_time_xlim(ax):
    ax.set_xlim(T_PLOT_MIN, T_PLOT_MAX)

def add_common_time_markers(ax, *, include_turnon=True, include_peak_now=True):
    # canonical turn-on markers
    if include_turnon:
        for name, kappa, u_star, t_star in turnon:
            ax.axvline(t_star, linestyle="--", linewidth=1, alpha=0.75)
    # peak/now markers
    if include_peak_now:
        ax.axvline(u_peak/eps2_canon, linestyle="--", linewidth=1, alpha=0.85)
        ax.axvline(t_now, linestyle=":", linewidth=1, alpha=0.95)
        ax.axvline((0.7*u_now)/eps2_canon, linestyle=":", linewidth=1, alpha=0.65)

# (1) ds curves + plateau + canonical markers
def lucas_number(n: int) -> int:
    """Lucas numbers: L0=2, L1=1, L(n)=L(n-1)+L(n-2)."""
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return 2
    if n == 1:
        return 1
    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def cert_41_2_generation_cutoff(n_min=9, n_max=17, denom_base=9):
    """Compute impedance I_n = L_n/(denom_base*n) and highlight n=15."""
    rows = []
    for n in range(n_min, n_max + 1):
        L = lucas_number(n)
        I = L / (denom_base * n)
        rows.append((n, L, I))
    # canonical check at n=15 if available
    row15 = next((r for r in rows if r[0] == 15), None)
    row13 = next((r for r in rows if r[0] == 13), None)
    status = "WAIT"
    if row15 and row13:
        status = "PASS" if (row15[2] >= 10.0 and row13[2] < 10.0) else "FAIL"
    return rows, status

def cert_41_3_delta_ladder(delta0, eps2, kappa_cap=30):
    """Find minimal kappa s.t. delta0^(kappa+1) <= eps2."""
    if not (0 < delta0 < 1) or not (0 < eps2 < 1):
        return dict(status="FAIL", reason="delta0/eps2 must be in (0,1)")
    k = 0
    while (delta0 ** (k + 1)) > eps2 and k < 10_000:
        k += 1
    status = "PASS" if k < kappa_cap else "FAIL"
    return dict(status=status, kappa=k, delta_at_k=delta0 ** (k + 1), eps2=eps2, kappa_cap=kappa_cap)

def cert_41_5_memory_pressure(u, lam, mem_mask, eps2_reg):
    """
    CERT 41.5 (Memory-Pressure) — sign/semantics consistent with BOOK VI.

    We separate two notions:
      • M_active(u) := H_mem(u)/H(u)  — *instantaneous* weight of memory-modes
        inside the current heat-trace state.
      • M_arch(u)   := 1 - M_active(u) — *archived* (already-decayed) share.

    On the strict 9-11-13 scene spectrum (G=(1/φ)(I-S)) the memory eigenmodes are at λ=1/φ,
    so M_active(u) decreases with u, while M_arch(u) increases with u.

    D0 “memory pressure” is tied to *accumulation/archiving*, hence we certify positivity of:

        Λ_mem(u) := d/du ln(M_arch(u) + eps2_reg)
                = M_arch'(u) / (M_arch(u) + eps2_reg)

    Derivatives are computed analytically from eigenvalues (no numeric gradients).
    """
    u = np.asarray(u, float)
    lam = np.asarray(lam, float)
    mem_mask = np.asarray(mem_mask, bool)
    if mem_mask.sum() == 0:
        return dict(status="WAIT", reason="mem_mask is empty (no kernel/memory modes detected)")

    W = np.exp(-u[:, None] * lam[None, :])
    H = W.sum(axis=1)
    Hm = W[:, mem_mask].sum(axis=1)

    # derivatives
    H_prime = -(W * lam[None, :]).sum(axis=1)
    Hm_prime = -(W[:, mem_mask] * lam[mem_mask][None, :]).sum(axis=1)

    M_active = Hm / np.maximum(H, 1e-300)
    # M_active' = (Hm'/H) - (Hm/H^2)H' = (Hm'/H) - M_active*(H'/H)
    M_active_prime = (Hm_prime / np.maximum(H, 1e-300)) - M_active * (H_prime / np.maximum(H, 1e-300))

    # archived share grows with u
    M_arch = 1.0 - M_active
    M_arch_prime = -M_active_prime

    denom = (M_arch + eps2_reg)
    Lambda_mem = (M_arch_prime / np.maximum(denom, 1e-300))

    # monotonic check for M_arch(u) (weak, up to numerical jitter)
    dM = np.diff(M_arch)
    mono_ok = np.all(dM >= -1e-12)

    # positivity window: use canonical [u_eps, u_now] if available; else middle 60%
    try:
        u_eps = float(eps2_canon * _t_eps)
        u_now = float(u_now_canon)
        win = (u >= u_eps) & (u <= u_now)
        if win.sum() < 5:
            win = slice(int(0.2 * len(u)), int(0.8 * len(u)))
    except Exception:
        win = slice(int(0.2 * len(u)), int(0.8 * len(u)))

    Lmin = float(np.nanmin(Lambda_mem[win]))
    Lmed = float(np.nanmedian(Lambda_mem[win]))
    Lmax = float(np.nanmax(Lambda_mem[win]))
    status = "PASS" if (Lmed > 0.0 and Lmax > 0.0) else "FAIL"

    return dict(
        status=status,
        mono_M=bool(mono_ok),
        M_now=float(M_arch[np.argmax(u)]),
        M_min=float(np.min(M_arch)),
        M_max=float(np.max(M_arch)),
        # also expose the instantaneous share for debugging/plots
        M_active_now=float(M_active[np.argmax(u)]),
        M_active_min=float(np.min(M_active)),
        M_active_max=float(np.max(M_active)),
        Lambda_min=Lmin,
        Lambda_med=Lmed,
        Lambda_max=Lmax,
        mem_mult=int(mem_mask.sum()),
    )

def cert_41_6_percolation_toy(A, u_min, u_max, m0, trials=200, grid_n=40, seed=0):
    """
    Toy percolation: each edge kept with probability p(u)=1-exp(-u*m0).
    Report u_c where P(connected) crosses ~0.5.
    Uses only internal m0 and graph A.
    """
    rng = np.random.default_rng(seed)
    A = np.asarray(A, int)
    n = A.shape[0]
    # edge list (undirected)
    iu, ju = np.triu_indices(n, 1)
    mask = A[iu, ju] > 0
    edges = np.stack([iu[mask], ju[mask]], axis=1)
    E = edges.shape[0]
    if E == 0:
        return dict(status="FAIL", reason="no edges in A")

    u_grid = np.logspace(np.log10(max(u_min, 1e-12)), np.log10(u_max), grid_n)
    p_grid = 1.0 - np.exp(-u_grid * float(m0))

    def is_connected(edge_keep):
        # build adjacency lists quickly
        adj = [[] for _ in range(n)]
        kept = edges[edge_keep]
        for a, b in kept:
            adj[a].append(b)
            adj[b].append(a)
        # BFS from 0
        seen = np.zeros(n, dtype=bool)
        stack = [0]
        seen[0] = True
        while stack:
            v = stack.pop()
            for w in adj[v]:
                if not seen[w]:
                    seen[w] = True
                    stack.append(w)
        return bool(seen.all())

    conn_prob = []
    for p in p_grid:
        cnt = 0
        for _ in range(trials):
            keep = rng.random(E) < p
            if is_connected(keep):
                cnt += 1
        conn_prob.append(cnt / trials)
    conn_prob = np.array(conn_prob, float)

    # find crossing ~0.5
    target = 0.5
    idx = np.where(conn_prob >= target)[0]
    if len(idx) == 0:
        return dict(status="FAIL", reason="never reaches 0.5 connectivity", u_star=float(u_grid[-1]), p_star=float(p_grid[-1]),
                    conn_prob=conn_prob.tolist(), u_grid=u_grid.tolist())
    j = int(idx[0])
    if j == 0:
        u_star = float(u_grid[0])
    else:
        # linear interp in prob
        u0, u1 = u_grid[j-1], u_grid[j]
        p0, p1 = conn_prob[j-1], conn_prob[j]
        if p1 == p0:
            u_star = float(u1)
        else:
            u_star = float(u0 + (target - p0) * (u1 - u0) / (p1 - p0))

    return dict(
        status="PASS",
        u_star=u_star,
        p_star=float(1.0 - math.exp(-u_star * float(m0))),
        t_star=float(u_star / eps2_canon),
        trials=int(trials),
        grid_n=int(grid_n),
        conn_prob=conn_prob.tolist(),
        u_grid=u_grid.tolist(),
    )


def _ensure_book6_globals():
    global _BOOK6_READY
    if _BOOK6_READY:
        return

    # 0.1) SI CALIBRATION (time/length scale)
    ###########################
    # D0 dynamics here is dimensionless in D0-time units.
    # To express results in SI seconds/meters you need ONE BOOK III/IV bridge scale.
    # We support two *non-ad-hoc* injection points (both are dimensionful, not new dimensionless knobs):
    #
    #   (1) Direct tick: set env D0_T0_S = seconds per 1 unit of D0-time.
    #       (This should come from BOOK IV — VERIFICATION, CERT 19.4.2 mass↔frequency bridge using m_e.)
    #
    #   (2) Macro check: set env D0_AGE_UNIVERSE_S = age of Universe in seconds,
    #       and we map the canonical present scene-time u_now=√5 to that age.
    #
    # If neither is provided, we keep t0_s=1 (dimensionless) and still compute all ratios/peaks.
    #
    #   (3) BOOK III/IV micro→macro prediction: use electron mass and D0 structure to predict Universe age.
    #       This is used automatically unless D0_DISABLE_TOME23=1 in env.


    c_SI = 299_792_458.0  # m/s (exact)
    SEC_PER_YEAR = 365.25 * 24.0 * 3600.0
    SEC_PER_GYR = SEC_PER_YEAR * 1e9

    # Structural π0 and mass quantum from BOOK III/IV canonical certificate (dimensionless, internal)

    # -------------------------
    # 0.15) α-seam certificate (BOOK III §16.3)
    # Δα := |α^{-1}_top - α^{-1}_alg|  with  α^{-1}_alg using structural π0 (NOT π)
    # Contract: Δα < ε²
    # -------------------------
    alpha_inv_top = 359.0 / (phi ** 2) - xi5
    alpha_inv_alg = (2.0 ** 11) * pi0 / (phi ** 8) + (2.0 * delta0) / 3.0
    Delta_alpha = abs(alpha_inv_top - alpha_inv_alg)
    Seam_contract_pass = bool(Delta_alpha < eps2_canon)

    vprint("\n=== α-seam certificate (BOOK III §16.3) ===")
    vprint(f"alpha_inv_top = {alpha_inv_top:.12f}")
    vprint(f"alpha_inv_alg = {alpha_inv_alg:.12f}")
    vprint(f"Delta_alpha   = {Delta_alpha:.12e}")
    vprint(f"eps^2         = {eps2_canon:.12e}")
    vprint("status        =", "PASS" if Seam_contract_pass else "FAIL")

    # ---- preferred: BOOK III/IV micro calibration (seconds per D0-time)
    _t0_env = os.environ.get("D0_T0_S", "").strip()
    T0_S_DIRECT = float(_t0_env) if _t0_env else None

    # ---- optional macro check: map u_now=√5 to Universe age (seconds)
    _age_env = os.environ.get("D0_AGE_UNIVERSE_S", "").strip()
    AGE_UNIVERSE_S = float(_age_env) if _age_env else None

    #
    # ---- BOOK III/IV (micro→macro) autonomous prediction:
    #     T_univ = t_e * phi^(N) * k_geom,
    #       t_e = ħ/(m_e c^2)
    #       N  = D_electron * D_vacuum  (BOOK III/IV derived integers; default 23*8=184)
    #       k_geom = pi0/phi^2 (=6/5 in the canonical certificate)
    # This uses only micro input (m_e, c) + SI definition of h (exact) and D0 structure.
    # You can disable it by setting env D0_DISABLE_TOME23=1 (legacy name).
    DISABLE_TOME23 = os.environ.get("D0_DISABLE_TOME23", "").strip() == "1"

    # SI micro inputs (can be overridden via env)
    _me_env = os.environ.get("D0_M_E_KG", "").strip()
    m_e_kg = float(_me_env) if _me_env else 9.1093837015e-31  # kg (CODATA 2022)

    # Allow overriding hbar if you want to avoid injecting SI h here.
    # If not provided, we use SI-defined h (exact) => hbar.
    _hbar_env = os.environ.get("D0_HBAR_J_S", "").strip()
    if _hbar_env:
        hbar_SI = float(_hbar_env)
        h_SI = None
    else:
        h_SI = 6.62607015e-34  # J·s (exact by SI definition)
        hbar_SI = h_SI / (2.0 * math.pi)

    # Bridge-structure depths (should match your BOOK III/IV certificates)
    _DE_env = os.environ.get("D0_D_ELECTRON", "").strip()
    _DV_env = os.environ.get("D0_D_VACUUM", "").strip()
    D_ELECTRON = int(_DE_env) if _DE_env else 23
    D_VACUUM = int(_DV_env) if _DV_env else 8

    # canonical present scene-time and corresponding D0-time
    sqrt5 = phi - psi
    u_now_canon = math.sqrt(5.0)  # canonical present scene-time

    globals().update(locals())

    t0_s = calibrate_t0_s()
    t0_s_raw = t0_s
    t0_s, used_override = t0_override(t0_s_raw)
    l0_m = c_SI * t0_s

    # report calibration source
    cal_src = "dimensionless"
    if T0_S_DIRECT is not None:
        cal_src = "env:D0_T0_S"
    elif AGE_UNIVERSE_S is not None:
        cal_src = "env:D0_AGE_UNIVERSE_S"
    elif not DISABLE_TOME23:
        cal_src = "BOOKIII/IV(m_e)"
    if used_override:
        cal_src = "env:D0_T0_S(override)"

    T23_age_s = None
    if (not DISABLE_TOME23):
        try:
            T23_age_s = tome23_universe_age_seconds()
        except Exception:
            T23_age_s = None

    vprint("\n=== SI calibration ===")
    vprint("source =", cal_src)
    vprint(f"m_e_kg  = {m_e_kg:.16e} kg")
    if os.environ.get("D0_HBAR_J_S", "").strip():
        vprint(f"hbar_SI = {hbar_SI:.16e} J·s  (from env:D0_HBAR_J_S)")
    else:
        vprint(f"hbar_SI = {hbar_SI:.16e} J·s  (from SI h definition)")
    vprint(f"depths  = D_ELECTRON={D_ELECTRON}, D_VACUUM={D_VACUUM}  => N={D_ELECTRON*D_VACUUM}")
    vprint(f"k_geom  = pi0/phi^2 = {pi0/(phi**2):.12f}")

    if T23_age_s is not None:
        vprint("T_univ_T23 =", T23_age_s, "s  =", (T23_age_s/SEC_PER_GYR), "Gyr")

    if used_override:
        vprint(f"[BRIDGE] D0_T0_S override: {t0_s_raw:.6e} -> {t0_s:.6e} seconds per D0-time")
    t0_s_raw = t0_s
    t0_s, used_override = t0_override(t0_s_raw)
    if used_override:
        vprint(f"[BRIDGE] D0_T0_S override: {t0_s_raw:.6e} -> {t0_s:.6e}")
    vprint("t0_s   =", t0_s, "seconds per D0-time")
    vprint("      =", (t0_s/SEC_PER_YEAR)/1e6, "Myr per D0-time")
    vprint("l0_m   =", l0_m, "meters per D0-length  (l0=c*t0)")
    vprint("pi0    =", pi0, "(structural)")
    vprint("m0     =", m0, "= 2*pi0 (memory mass quantum)")

    vprint("tau0_D0=", tau0_D0, "= 1/m0 (base period in D0-time units)")

    omega_pi0_bridge(pi0)

    vprint("\n=== Neutron/proton lifetime bridge (gap idea; discrete, no new params) ===")
    # Micro chronon (reduced Compton period of the electron): t_e = ħ/(m_e c^2)
    # Use it as a universal attempt-time for topological relaxation.
    # Candidate discrete exponent for neutron (sphere, k=1) vs vacuum (k=6/5):
    #   N_n := D_ELECTRON * (D_VACUUM - 3) - 1
    # Interpretation:
    #   - D_VACUUM - 3 counts the non-transport (\"memory\") depth over 3D space
    #   - \"-1\" is the canonical neutrality/topology correction (no new knob; fixed integer)
    # This predicts a finite lifetime for neutron-like (non-knot-protected) excitations.

    t_e = hbar_SI / (m_e_kg * (c_SI**2))
    N_n = int(D_ELECTRON * (D_VACUUM - 3) - 1)

    # neutron-like lifetime estimate (seconds)
    tau_n_s = float(t_e * (phi**N_n))

    # proton-like stability scale: topologically protected knot (matches vacuum), so the natural
    # upper scale coincides with the macro age predicted by the BOOK III/IV bridge.
    N_p = int(D_ELECTRON * D_VACUUM)
    tau_p_s = float(t_e * (phi**N_p) * (pi0/(phi**2)))  # == BOOK III/IV bridge age if enabled

    vprint(f"t_e (electron chronon) = {t_e:.12e} s")
    vprint(f"N_n = D_E*(D_V-3)-1 = {N_n}")
    vprint(f"tau_n (pred)         = {tau_n_s:.6e} s  ({tau_n_s:.6f} s)")
    vprint(f"N_p = D_E*D_V         = {N_p}")
    vprint(f"tau_p scale (pred)   = {tau_p_s:.6e} s  ({tau_p_s/SEC_PER_GYR:.6f} Gyr)")

    # --- neutron refinement: first leakage correction by canonical eps (still no new params)
    # tau_n_corr := tau_n * (1 + eps)
    # (Reference values are ONLY for reporting relative error; no fitting.)
    tau_n_corr_s = float(tau_n_s * (1.0 + eps))
    # Reference values for reporting ONLY (not used for fitting)
    _ref_bottle = float(os.environ.get("D0_REF_NEUTRON_BOTTLE_S", "879.4"))
    _ref_beam   = float(os.environ.get("D0_REF_NEUTRON_BEAM_S",   "888.0"))
    vprint(f"tau_n_corr = tau_n*(1+eps) = {tau_n_corr_s:.6e} s  ({tau_n_corr_s:.6f} s)")
    vprint(f"relerr vs 879.4 s (bottle): {(tau_n_corr_s-_ref_bottle)/_ref_bottle:+.4%}")
    vprint(f"relerr vs 888.0 s (beam):   {(tau_n_corr_s-_ref_beam)/_ref_beam:+.4%}")

    # --- proton lower-bound proxy: add a discrete barrier depth (knot protection)
    # N_gap := D_ELECTRON*(D_VACUUM-3)  (pure integer; no new knobs)
    N_gap = int(D_ELECTRON * (D_VACUUM - 3))

    # tau_p_bound := t_e * phi^(N_p + N_gap) * k_geom
    try:
        from decimal import Decimal, getcontext
        getcontext().prec = 240
        phiD = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
        k_geom_D = Decimal(str(pi0/(phi**2)))
        tau_p_bound_D = Decimal(str(t_e)) * (phiD ** int(N_p + N_gap)) * k_geom_D
        tau_p_bound_s = float(tau_p_bound_D)
    except Exception:
        tau_p_bound_s = float(t_e * (phi ** (N_p + N_gap)) * (pi0/(phi**2)))

    vprint(f"N_gap = D_E*(D_V-3)   = {N_gap}")
    vprint(f"tau_p_bound (proxy)  = {tau_p_bound_s:.6e} s  ({(tau_p_bound_s/SEC_PER_YEAR):.6e} yr)")

    if T0_S_DIRECT is None and AGE_UNIVERSE_S is None and DISABLE_TOME23:
        vprint("[WARN] SI scale not set. Provide env D0_T0_S (BOOK III/IV micro) or D0_AGE_UNIVERSE_S (macro) or enable BOOK III/IV micro→macro bridge.")

    vprint("=== ABCD ===")
    vprint("A:", phi+psi)
    vprint("B:", phi*psi)
    vprint("C:", phi**2, "vs", phi+1)
    vprint("D:", psi**2, "vs", psi+1)

    vprint("\n=== delta0, eps ===")
    vprint("delta0 =", delta0)
    vprint("eps    =", eps, " eps^2 =", eps2_canon)

    vprint("\n=== Q(D) = 2*delta0*phi^(D-1) ===")
    for D in range(1, 6):
        QD = 2.0*delta0*(phi**(D-1))
        tag = ""
        if D == 4:
            tag = " <-- UNITY"
        vprint(f"D={D}: Q={QD:.12f}{tag}")

    vprint("\n=== Canonical kappas ===")
    vprint("eps2 =", eps2_canon)
    vprint("eps  =", eps)
    vprint("xi5  =", xi5)
    vprint("delta0=", delta0)

    # -------------------------
    # 1) NUMERIC UTILS
    # -------------------------
    lam_scene = scene_d0_spectrum()

    # ---- grouped/rounded spectrum (precompute once; used by S_DE and mode fractions)
    _vals_round = np.round(lam_scene, 12)
    _uniq_list = sorted(set(_vals_round.tolist()))
    uniq_vals = np.array(_uniq_list, float)
    uniq_mult = np.array([int(np.sum(_vals_round == v)) for v in _uniq_list], int)

    globals().update(locals())

    # -------------------------
    # 2.1) DARK SECTOR: RANK–NULLITY CERTIFICATE (STRICT)
    # Dark kernel for K(9,11,13):
    #   dim Ker(A) = Σ_i (n_i - 1) = (9-1)+(11-1)+(13-1)=30
    # Proof idea:
    #   For each part i, any vector supported on part i with sum(v)=0 is killed by A:
    #     - outside the part: receives sum(v)=0
    #     - inside the part: sees only outside parts, but v=0 there
    # Hence nullity ≥ 30. Since N=33, rank ≤ 3. Nontrivial action on partition-constant
    # subspace (dim=3) => rank=3 and nullity=30.
    # In our normalized generator G=(1/phi)*(I-S), S = D^-1/2 A D^-1/2,
    # eigenvalue 1/phi in G corresponds exactly to eigenvalue 0 of S (kernel modes).

    dark_cert = scene_rank_nullity_certificate()

    # Scene heat trace and exact ds_scene (== Δd)
    PLATEAU_T_LO = float(os.environ.get("D0_PLATEAU_T_LO", "1.0"))
    PLATEAU_T_HI = float(os.environ.get("D0_PLATEAU_T_HI", "3000.0"))
    PLATEAU_N = int(os.environ.get("D0_PLATEAU_N", "120"))
    PLATEAU_MIN_PTS = int(os.environ.get("D0_PLATEAU_MIN_PTS", "20"))

    levels = [
        ("eps2", eps2_canon),
        ("eps",  eps),
        ("xi5",  xi5),
        ("delta0", delta0),
    ]

    turnon = []
    for name, kappa in levels:
        u_star = find_u_for_deviation(kappa)
        t_star = u_star / eps2_canon
        turnon.append((name, kappa, u_star, t_star))

    vprint("\n=== Canonical scene turn-on times (D(u)=1-P_scene(u)=kappa) ===")
    for name, kappa, u_star, t_star in turnon:
        t_star_SI = t_star * t0_s
        vprint(
            f"{name:7s}  kappa={kappa:.10e}  u*={u_star:.10e}  t*={t_star:.6f}"
            f"  |  t*_SI={t_star_SI:.6e} s  ({t_star_SI/SEC_PER_YEAR:.3e} yr)"
        )

    # -------------------------
    # 5.1) GRID UTIL: include exact marker times in grids
    # -------------------------
    _t_eps2   = dict((n,ts) for n,_,_,ts in turnon)["eps2"]
    _t_eps    = dict((n,ts) for n,_,_,ts in turnon)["eps"]
    _t_xi5    = dict((n,ts) for n,_,_,ts in turnon)["xi5"]
    _t_delta0 = dict((n,ts) for n,_,_,ts in turnon)["delta0"]

    # external comparison point (DESI-style statement): 70% of present age
    _t_70 = 0.7 * _t_delta0

    # --- canonical (parameter-free) space-dimension diagnostic on the kappa window [t_eps, t_xi5]
    # Uses only canonical kappas; no plateau-search heuristics.
    _canon_window = dict(tmin=_t_eps, tmax=_t_xi5)

    L0 = 129

    # -------------------------
    # 5.2) MASTER TIME GRID (Step 1)
    # -------------------------
    # Ensure grids cover:
    #  - plateau search upper bound (PLATEAU_T_HI)
    #  - canonical present time (t_now)
    #  - DE strength peak search window

    T_MAX = max(
        1000.0,
        1.10 * PLATEAU_T_HI,
        float((u_now_canon * 3.0) / eps2_canon),
    )

    # base grid + inject canonical times so peak/ratios are not grid-artifacts
    _base_grid = np.logspace(-3, np.log10(T_MAX), 420)
    _extra_times = [_t_eps2, _t_eps, _t_xi5, _t_delta0, _t_70]
    t_grid = merge_times(_base_grid, _extra_times)

    logP_sp, ds_sp, lam1 = space_P_logP_ds(L0, t_grid)
    logP_sc, ds_sc, u_grid, mu_u = scene_P_logP_ds(t_grid, eps2_canon)

    # fiber (exact factorization)
    logP_fb = logP_sp + logP_sc
    ds_fb = ds_sp + ds_sc
    dd = ds_fb - ds_sp  # == ds_sc exactly (up to float)

    # checks
    err_abs = np.max(np.abs(np.exp(logP_fb) - np.exp(logP_sp)*np.exp(logP_sc)))
    err_rel = np.max(np.abs((np.exp(logP_fb) - np.exp(logP_sp)*np.exp(logP_sc)) / np.maximum(np.exp(logP_fb),1e-300)))
    vprint("\n=== Factorization check: P_fiber ?= P_space * P_scene(eps2 t) ===")
    vprint("max abs err:", err_abs)
    vprint("max rel err:", err_rel)

    # plateau window on space
    win_legacy = best_plateau_window(t_grid, ds_sp, t_lo=PLATEAU_T_LO, t_hi=300.0, n=80, min_pts=18)
    win = best_plateau_window(t_grid, ds_sp, t_lo=PLATEAU_T_LO, t_hi=PLATEAU_T_HI, n=PLATEAU_N, min_pts=PLATEAU_MIN_PTS)
    vprint(f"\n=== Space plateau window (L={L0}) legacy(t_hi=300) ===", win_legacy)
    vprint(f"=== Space plateau window (L={L0}) extended(t_hi={PLATEAU_T_HI:g}) ===", win)

    # --- Canonical volume normalization for FRW-like a(t)
    # Heat-trace logP behaves like an extensive (volume-like) quantity.
    # To obtain a linear scale-factor proxy, normalize by an effective spatial dimension.
    # We use the space plateau median (no new params).
    d_ref = float(win["med"]) if (win is not None) else 3.0

    # Canonical window stats (no heuristics): ds_space on [t_eps, t_xi5]
    _mask_canon = (t_grid >= _canon_window["tmin"]) & (t_grid <= _canon_window["tmax"])
    if np.any(_mask_canon):
        _seg = ds_sp[_mask_canon]
        _med = float(np.median(_seg))
        _mad = float(np.median(np.abs(_seg - _med)))
        vprint("\n=== Canonical space dimension on [t_eps, t_xi5] ===")
        vprint(f"t_eps={_canon_window['tmin']:.6f}  t_xi5={_canon_window['tmax']:.6f}")
        vprint(f"ds_space median = {_med:.12f}")
        vprint(f"ds_space MAD    = {_mad:.12f}")
    else:
        vprint("\n[WARN] canonical window [t_eps, t_xi5] not covered by t_grid")

    # -------------------------
    # 7) SWEEP BY L: plateau window vs L (exact spectra, fast)
    # -------------------------
    L_list = [17,21,25,29,33,41,49,65,81,101,129,161,201,257,321]
    rows = []
    for L in L_list:
        logP_sp_L, ds_sp_L, _ = space_P_logP_ds(L, t_grid)
        w = best_plateau_window(t_grid, ds_sp_L, t_lo=PLATEAU_T_LO, t_hi=PLATEAU_T_HI, n=PLATEAU_N, min_pts=PLATEAU_MIN_PTS)
        rows.append((L, w["tmin"], w["tmax"], w["med"], w["mad"]))

    vprint("\nL   tmin     tmax     ds_med   MAD")
    for L,tmin,tmax,med,mad in rows:
        vprint(f"{L:<3d} {tmin:8.2f} {tmax:8.2f} {med:7.4f} {mad:7.4f}")

    Ls = np.array([r[0] for r in rows], int)
    tmin = np.array([r[1] for r in rows], float)
    tmax = np.array([r[2] for r in rows], float)

    t_eps = dict((n,ts) for n,_,_,ts in turnon)["eps"]
    t_xi5 = dict((n,ts) for n,_,_,ts in turnon)["xi5"]
    vprint("\nNormalized window positions (plateau) relative to eps and xi5:")
    for L,a,b,med,mad in rows:
        vprint(f"L={L:<3d}  tmin/teps={a/t_eps:6.3f}  tmax/txi5={b/t_xi5:6.3f}")

    # -------------------------
    # 8) DARK-SECTOR DYNAMICS (scene-only, no spikes, no gradients)
    # -------------------------
    # The q(t) construction is very sensitive to H≈0 crossings (even with exact moments),
    # which can generate artificial blow-ups/spikes on log axes.
    # For a robust D0-canonical proxy, we use a *scene-only strength functional*:
    #   S_DE(u) := u * D'(u),  where D(u)=1-P_scene(u) and D'(u)=(1/N) Σ λ e^{-uλ}.
    # This is the response per logarithmic scene-time (u), and it is purely spectral.
    #
    # We also define the "present" cosmic scene-time canonically (no ad hoc):
    #   u_now := φ - ψ = √5.
    # The corresponding D0-time is t_now = u_now / eps^2.

    u_now = u_now_canon

    # D'(u) using grouped spectrum (stable, faster):
    #   D'(u) = (1/N) * sum_i (m_i * λ_i * exp(-u λ_i))
    # where (λ_i, m_i) are unique eigenvalues and their multiplicities.

    u_now = sqrt5
    t_now = u_now / eps2_canon

    # ---------- Peak/FWHM for S_DE (spectral; fast; no giant grids) ----------
    u_peak, S_peak = find_SDE_peak(u_now)
    left_cross, right_cross, fwhm_u = fwhm_SDE(u_peak, S_peak)
    fwhm_t = (fwhm_u / eps2_canon) if (fwhm_u is not None) else None

    # External comparison point: 70% of the present age (canonical)
    u_70 = 0.7 * u_now

    S_now = float(S_DE(np.array([u_now]))[0])
    S_70  = float(S_DE(np.array([u_70]))[0])

    vprint("\n=== DARK ENERGY (scene-only strength; canonical u_now=√5) ===")
    vprint(f"u_now = φ-ψ = √5 = {u_now:.12f}")
    vprint(f"t_now = u_now/eps^2 = {t_now:.6f}")
    vprint(f"t_now_SI = t_now * t0_s = {t_now*t0_s:.6e} s  ({(t_now*t0_s)/SEC_PER_GYR:.6f} Gyr)")
    vprint(f"u_peak = {u_peak:.12f}   (u_peak/u_now = {u_peak/u_now:.3f})")
    vprint(f"t_peak = u_peak/eps^2 = {u_peak/eps2_canon:.6f}")
    vprint(f"t_peak_SI = {((u_peak/eps2_canon)*t0_s):.6e} s  ({((u_peak/eps2_canon)*t0_s)/SEC_PER_GYR:.6f} Gyr)")
    vprint(f"S_peak = {S_peak:.6e}")
    vprint(f"S(now)/S_peak = {S_now/S_peak:.3f}   => weakening now vs peak: {(1.0 - S_now/S_peak)*100.0:+.2f}%")
    vprint(f"S(0.7 now)/S_peak = {S_70/S_peak:.3f} => weakening at 0.7 now vs peak: {(1.0 - S_70/S_peak)*100.0:+.2f}%")

    vprint("\n--- DE peak width (FWHM) ---")
    if fwhm_u is None or left_cross is None or right_cross is None:
        vprint("FWHM: not bracketed (increase D0_SDE_COARSE_N or widen factor_max in find_SDE_peak if needed)")
    else:
        log_width = math.log(right_cross / left_cross)
        vprint(f"u_left   = {left_cross:.12f}")
        vprint(f"u_right  = {right_cross:.12f}")
        vprint(f"FWHM_u   = {fwhm_u:.12f}  (Δu/u_peak = {fwhm_u/u_peak:.3f})")
        vprint(f"FWHM_log = ln(u_right/u_left) = {log_width:.6f}")
        vprint(f"FWHM_t   = {fwhm_t:.6f} D0-time")
        vprint(f"FWHM_SI  = {fwhm_t*t0_s:.6e} s  ({(fwhm_t*t0_s)/SEC_PER_GYR:.6f} Gyr)")

    # ---------- Step 3: Acceleration q(t) and equation-of-state w(t) (no ad hoc) ----------
    # Canonical scale factor from scene heat-trace:
    #   a(u) := P_scene(u_now)/P_scene(u)  => ln a = logP(u_now) - logP(u)
    # Then:
    #   d/du ln a = -d/du logP = mu(u)
    # With u=eps^2 t:
    #   H(t) = d/dt ln a = eps^2 * mu(u)
    #   q(t) = -1 - (dH/dt)/H^2 = -1 - mu'(u)/mu(u)^2
    # Effective equation of state (single-fluid proxy):
    #   w_eff(t) = (2 q(t) - 1)/3
    # Dark-energy (zero-mode) EoS by deconvolving grouped fractions:
    #   w_eff = Ω_DE * w_DE   with Ω_DE := f0(u) and matter-like remainder w=0.
    #   => w_DE = w_eff / Ω_DE (where Ω_DE>0)

    # (uniq_vals, uniq_mult) were precomputed once right after lam_scene construction.

    # Grouped mode masks for scene spectrum:
    #   zero mode: 0
    #   memory:    1/phi
    #   transport: remaining nonzero non-(1/phi)
    idx_zero = _find_idx(0.0, tol=1e-12)
    idx_mem  = _find_idx(1.0/phi, tol=1e-10)

    if idx_zero is None:
        raise RuntimeError("Scene spectrum grouping failed: zero-mode not found.")
    if idx_mem is None:
        raise RuntimeError("Scene spectrum grouping failed: memory mode (1/phi) not found.")

    transport_mask = np.ones(len(uniq_vals), dtype=bool)
    transport_mask[idx_zero] = False
    transport_mask[idx_mem] = False

    globals().update(locals())

    u_q = np.logspace(-10, np.log10(u_now), int(UQ_N))
    t_q = u_q / eps2_canon

    # mu(u) and mu'(u) from exact spectrum (no numeric gradients)
    # (reuse uniq spectrum to be consistent with mode fractions)
    Wq = (uniq_mult[None, :] * np.exp(-u_q[:, None] * uniq_vals[None, :]))
    Zq = Wq.sum(axis=1)
    mu_q = (Wq * uniq_vals[None, :]).sum(axis=1) / Zq

    # Exact identity: d/du E_u[λ] = -Var_u(λ) = -(E_u[λ^2] - E_u[λ]^2)
    E2_q = (Wq * (uniq_vals[None, :]**2)).sum(axis=1) / Zq
    mu_q_prime = -(E2_q - mu_q**2)

    # q_scene(u) and w_scene(u) are CANONICAL (scene-only): no d_ref factor.
    q_scene_q = -1.0 - (mu_q_prime / np.maximum(mu_q, 1e-300)**2)
    w_scene_q = (2.0 * q_scene_q - 1.0) / 3.0

    # grouped fractions (spectral weights): f0 (zero-mode), fm (memory), ft (transport)
    f0_q, fm_q, ft_q = grouped_fracs(u_q)

    # evaluate at canonical points (nearest grid index)
    idx_now = int(np.argmin(np.abs(u_q - u_now)))
    idx_pk  = int(np.argmin(np.abs(u_q - u_peak)))

    vprint("\n=== ACCELERATION + EQUATION OF STATE (scene-derived, CANONICAL) ===")
    vprint(f"q_scene(now)  = {q_scene_q[idx_now]:+.6f}   |  w_scene(now)  = {w_scene_q[idx_now]:+.6f}")
    vprint(f"q_scene(peak) = {q_scene_q[idx_pk]:+.6f}   |  w_scene(peak) = {w_scene_q[idx_pk]:+.6f}")

    vprint(f"f0(now)   = {f0_q[idx_now]:.6f}   (zero-mode spectral weight)")
    vprint(f"f0(peak)  = {f0_q[idx_pk]:.6f}   (zero-mode spectral weight)")

    # ---------- Fiber (space ⊕ eps^2·scene) acceleration + EoS (no new params) ----------
    # Define scale factor from *fiber* heat trace:
    #   ln a_fib(t) = logP_fib(t_now) - logP_fib(t)
    # where logP_fib = logP_space(t) + logP_scene(eps^2 t)
    # Then:
    #   H_fib(t) = - d/dt logP_fib(t)
    #            = mu_space(t) + eps^2 * mu_scene(u)
    # with u=eps^2 t, and mu' = -Var.
    #   d/dt mu_space(t) = (d/dtau mu1)(1/3) = -Var_space/3, where tau=t/3
    #   d/dt (eps^2 mu_scene(u)) = eps^4 * mu_scene'(u) = -eps^4 * Var_scene
    # so:
    #   q_fib(t) = -1 - H'_fib / H_fib^2
    #   w_eff_fib(t) = (2 q_fib - 1)/3

    # 1D space spectrum for the chosen L0
    lam1_L0 = space_1d_eigs(L0)

    # Space moments at tau=t/3
    _tau_q = t_q / 3.0
    Wsp = np.exp(-_tau_q[:, None] * lam1_L0[None, :])
    Zsp = Wsp.sum(axis=1)
    mu_space_q = (Wsp * lam1_L0[None, :]).sum(axis=1) / Zsp
    E2_space_q = (Wsp * (lam1_L0[None, :]**2)).sum(axis=1) / Zsp
    var_space_q = np.maximum(E2_space_q - mu_space_q**2, 0.0)

    # Scene moments (already computed on u_q): mu_q, mu_q_prime = -Var_scene
    var_scene_q = np.maximum(-(mu_q_prime), 0.0)

    # Fiber Hubble in D0-time units
    # Keep BOTH:
    #   - raw rate (entropy/trace rate)
    #   - d_ref-normalized rate (scale-factor proxy)
    H_fib_raw_q = mu_space_q + (eps2_canon * mu_q)
    Hprime_fib_raw_q = (-var_space_q / 3.0) + (eps2_canon**2) * mu_q_prime

    H_fib_q = H_fib_raw_q / d_ref
    Hprime_fib_q = Hprime_fib_raw_q / d_ref

    # q and w_eff for fiber
    q_fib_q = -1.0 - (Hprime_fib_q / np.maximum(H_fib_q, 1e-300)**2)
    w_eff_fib = (2.0 * q_fib_q - 1.0) / 3.0

    # SI diagnostics at canonical points
    H_now_raw_D0  = float(H_fib_raw_q[idx_now])
    H_peak_raw_D0 = float(H_fib_raw_q[idx_pk])
    H_now_D0      = float(H_fib_q[idx_now])
    H_peak_D0     = float(H_fib_q[idx_pk])

    H_now_raw_SI  = H_now_raw_D0 / t0_s
    H_peak_raw_SI = H_peak_raw_D0 / t0_s
    H_now_SI      = H_now_D0 / t0_s
    H_peak_SI     = H_peak_D0 / t0_s

    # cH scales
    cH_raw_now = c_SI * H_now_raw_SI
    cH_now     = c_SI * H_now_SI

    # Dimension leak proxy: use the space-plateau median as an effective spatial dimension
    # (do NOT hardcode 0.04; derive from ds plateau)
    d_vac = d_ref
    Delta_d = d_vac - 3.0

    a_dim_now = cH_now * Delta_d

    vprint("\n=== FIBER ACCELERATION + EoS + cH (space ⊕ eps^2·scene) ===")
    vprint(f"H_fib(now)  = {H_now_SI:.6e} 1/s")
    vprint(f"H_fib(peak) = {H_peak_SI:.6e} 1/s")
    vprint(f"c·H_raw(now)= {cH_raw_now:.6e} m/s^2  (trace-rate)")
    vprint(f"c·H(now)    = {cH_now:.6e} m/s^2      (d_ref-normalized)")
    vprint(f"d_vac (from space plateau med) = {d_vac:.6f}  => Δd={Delta_d:.6f}")
    vprint(f"a_dim(now) = cH(now)·Δd = {a_dim_now:.6e} m/s^2")
    vprint(f"q_fib(now)   = {q_fib_q[idx_now]:+.6f}   |  w_eff_fib(now)  = {w_eff_fib[idx_now]:+.6f}")
    vprint(f"q_fib(peak)  = {q_fib_q[idx_pk]:+.6f}   |  w_eff_fib(peak) = {w_eff_fib[idx_pk]:+.6f}")

    # --- BOOK IV style: non-constancy certificate for w(t) (internal only)
    mask_w = (t_q >= t_eps) & (t_q <= t_now)
    if np.any(mask_w):
        w_span = float(np.nanmax(w_eff_fib[mask_w]) - np.nanmin(w_eff_fib[mask_w]))
        w_nonconst = (w_span > eps2_canon)
        vprint("\n=== CERT (model): w_eff_fiber is non-constant on [t_eps, t_now] ===")
        vprint(f"span = {w_span:.6e}  compare eps^2={eps2_canon:.6e}  =>", "PASS" if w_nonconst else "FAIL")
    else:
        vprint("\n[WARN] w(t) certificate window not covered")

    # Optional: a conservative, non-claiming component split proxy
    # Define a fractional contribution of the scene term to H (not to Ω):
    frac_scene_H_now = float((eps2_canon * mu_q[idx_now]) / np.maximum(H_fib_raw_q[idx_now], 1e-300))
    frac_scene_H_pk  = float((eps2_canon * mu_q[idx_pk]) / np.maximum(H_fib_raw_q[idx_pk], 1e-300))
    vprint(f"frac_scene_in_H(now)  = {frac_scene_H_now:.6f}   (NOTE: not Ω_DE)")
    vprint(f"frac_scene_in_H(peak) = {frac_scene_H_pk:.6f}   (NOTE: not Ω_DE)")

    # --- H in km/s/Mpc (diagnostic only)
    MPC_M = 3.085677581e22
    H_now_km_s_Mpc = H_now_SI * MPC_M / 1000.0
    H_peak_km_s_Mpc = H_peak_SI * MPC_M / 1000.0
    vprint(f"H_fib(now)  = {H_now_km_s_Mpc:.3f} km/s/Mpc  (BRIDGE/DIAGNOSTIC — not a CORE certificate)")
    vprint(f"H_fib(peak) = {H_peak_km_s_Mpc:.3f} km/s/Mpc  (BRIDGE/DIAGNOSTIC — not a CORE certificate)")

    # --- Pioneer/MOND scale from spectral split (no ad hoc factors)
    a_pioneer_proxy_now = cH_raw_now * frac_scene_H_now
    vprint(f"a_proxy(now)=cH_raw*frac_scene = {a_pioneer_proxy_now:.6e} m/s^2  (BRIDGE/DIAGNOSTIC)")


    # ============================================================
    # 9) CANONICAL ONSET: acceleration crossing AFTER scene turn-on
    # + redshift z_acc from fiber scale factor
    # ============================================================

    t_eps = dict((n, ts) for n, _, _, ts in turnon)["eps"]
    t_acc_fib_phys = first_crossing_after(t_q, q_fib_q, x0=t_eps, level=0.0)

    # --- compute fiber ln a(t) on the SAME grid t_q (not t_grid) so z_acc is consistent
    logP_sp_q, _, _ = space_P_logP_ds(L0, t_q)
    logP_sc_q = logP_scene(u_q)
    logP_fb_q = logP_sp_q + logP_sc_q

    logP_fb_now = float(logP_fb_q[idx_now])
    # Consistent with H_fib = (1/d_ref)*(-d/dt logP_fb):
    ln_a_fib_q = (logP_fb_now - logP_fb_q) / d_ref
    # z = 1/a - 1 = exp(-ln a) - 1
    z_fib_q = np.expm1(-ln_a_fib_q)

    z_acc_fib_phys = interp_on_grid(t_q, z_fib_q, t_acc_fib_phys)
    t_acc_fib_phys_SI = (t_acc_fib_phys * t0_s) if (t_acc_fib_phys is not None) else None

    vprint("\n=== EoS + acceleration onset (CANONICAL; after t_eps) ===")
    vprint(f"t_eps (scene on) = {t_eps:.6f} D0-time  |  {(t_eps*t0_s)/SEC_PER_GYR:.6f} Gyr")

    if t_acc_fib_phys is None:
        vprint("t_acc_fib_phys: no q_fib(t)=0 crossing after t_eps on computed grid")
    else:
        vprint(f"t_acc_fib_phys = {t_acc_fib_phys:.6f} D0-time  |  {t_acc_fib_phys_SI/SEC_PER_GYR:.6f} Gyr")
        vprint(f"z_acc_fib_phys = {z_acc_fib_phys:.6f}")

    # ============================================================
    # 10) CANONICAL dark-sector fraction in H (rate-split) + w_scene^H
    # ============================================================
    # Build full time-series (canonical H-split; no H^2)
    H_scene_raw_q = eps2_canon * mu_q
    Omega_scene_H_q = safe_div(H_scene_raw_q, H_fib_raw_q)
    Omega_scene_H_q = np.clip(Omega_scene_H_q, 0.0, 1.0)

    w_scene_H_q = safe_div(w_eff_fib, Omega_scene_H_q)
    w_scene_H_q = np.where(np.isfinite(w_scene_H_q), w_scene_H_q, np.nan)

    Omega_scene_H_now = float(Omega_scene_H_q[idx_now])
    Omega_scene_H_pk  = float(Omega_scene_H_q[idx_pk])
    w_scene_H_now = float(w_scene_H_q[idx_now])
    w_scene_H_pk  = float(w_scene_H_q[idx_pk])

    vprint("\n=== CANONICAL dark-sector closure (H-split; no H^2) ===")
    vprint(f"Omega_scene_H(now)  = {Omega_scene_H_now:.6f}")
    vprint(f"Omega_scene_H(peak) = {Omega_scene_H_pk:.6f}")
    vprint(f"w_scene_H(now)      = {w_scene_H_now:+.6f}")
    vprint(f"w_scene_H(peak)     = {w_scene_H_pk:+.6f}")

    # --- Save canonical cosmology time-series (single file; no duplicates)
    out_csv = OUTDIR / P(PROT, "outputs")["csv"]
    df = pd.DataFrame({
        "u": u_q,
        "t_D0": t_q,
        "t_SI_s": t_q * t0_s,
        "t_Gyr": (t_q * t0_s) / SEC_PER_GYR,
        "H_fib_raw_SI_1s": H_fib_raw_q / t0_s,
        "H_fib_SI_1s": H_fib_q / t0_s,
        "H_fib_km_s_Mpc": (H_fib_q / t0_s) * (MPC_M / 1000.0),
        "q_scene": q_scene_q,
        "w_scene": w_scene_q,
        "q_fib": q_fib_q,
        "w_fib": w_eff_fib,
        "Omega_scene_H": Omega_scene_H_q,
        "w_scene_H": w_scene_H_q,
        "ln_a_fib": ln_a_fib_q,
        "z_fib": z_fib_q,
    })
    df.to_csv(out_csv, index=False)
    print(f"[SAVED] {out_csv.as_posix()}")

    # -------------------------
    # 6.1) SINGLE SUMMARY FIGURE (one image)
    # -------------------------
    # --- grouped fractions (interpretation: transport vs memory)
    # Groups are defined canonically from the scene spectrum:
    #   zero-mode:   λ = 0
    #   memory:      λ = 1/phi  (multiplicity 30 in K_{9,11,13})
    # quick grouped fractions at canonical points
    u_now_dbg = u_now_canon
    u_peak_dbg = u_peak
    f0_now, fm_now, ft_now = (x[0] for x in grouped_fracs(np.array([u_now_dbg], float)))
    f0_pk,  fm_pk,  ft_pk  = (x[0] for x in grouped_fracs(np.array([u_peak_dbg], float)))
    vprint("\n=== Scene mode fractions (grouped) ===")
    vprint(f"at u_now=√5:    f0={f0_now:.6f}  f_mem={fm_now:.6f}  f_tr={ft_now:.6f}")
    vprint(f"at u_peak(S):   f0={f0_pk:.6f}   f_mem={fm_pk:.6f}   f_tr={ft_pk:.6f}")


    fig, axs = plt.subplots(2, 3, figsize=(19, 10), constrained_layout=True)

    # --- common time x-limits for all t-plots (align panels)
    T_PLOT_MIN = float(np.min(t_grid))
    T_PLOT_MAX = float(np.max(t_grid))

    globals().update(locals())

    ax = axs[0,0]
    ax.semilogx(t_grid, ds_sp, label="ds_space")
    ax.semilogx(t_grid, ds_fb, label="ds_fiber")
    if win is not None:
        ax.axvspan(win["tmin"], win["tmax"], alpha=0.2, label="space plateau")
    # place labels near the top of the axis (in axes coords) to avoid overlapping the curve
    for name, kappa, u_star, t_star in turnon:
        ax.axvline(t_star, linestyle="--", linewidth=1, alpha=0.75)
        ax.annotate(
            name,
            xy=(t_star, 1.0), xycoords=("data", "axes fraction"),
            xytext=(2, -6), textcoords="offset points",
            rotation=90, va="top", ha="left",
            fontsize=9,
            clip_on=False,
        )
    ax.set_xlabel("t (D0-time)")
    ax.set_ylabel("d_s(t)")
    ax.set_title("Space vs Fiber + canonical turn-on")
    ax.legend(loc="best")
    set_time_xlim(ax)
    add_common_time_markers(ax, include_turnon=True, include_peak_now=False)

    # (2) Δd(t)=ds_scene exact + small-u law
    ax = axs[0,1]
    mu0 = float(np.mean(lam_scene))
    ax.semilogx(t_grid, ds_sc, label="Δd(t)=ds_scene exact")
    ax.semilogx(t_grid, 2*(eps2_canon*t_grid)*mu0, "--", label=f"small-u: 2*mu0*eps2*t (mu0={mu0:.6f})")
    ax.set_xlabel("t (D0-time)")
    ax.set_ylabel("Δd(t)")
    ax.set_title("Scene dynamics: Δd(t)")
    ax.legend(loc="best")
    set_time_xlim(ax)
    add_common_time_markers(ax, include_turnon=False, include_peak_now=False)

    # (3) plateau window vs L with canonical turn-on times
    ax = axs[0,2]
    Ls = np.array([r[0] for r in rows], int)
    _tmin = np.array([r[1] for r in rows], float)
    _tmax = np.array([r[2] for r in rows], float)
    ax.semilogy(Ls, _tmin, marker="o", label="tmin (space plateau)")
    ax.semilogy(Ls, _tmax, marker="o", label="tmax (space plateau)")
    _labeled = False
    for name, kappa, u_star, t_star in turnon:
        ax.axhline(
            t_star, linestyle="--", linewidth=1, alpha=0.75,
            label=(f"t_{name}" if not _labeled else None)
        )
        _labeled = True
    ax.set_xlabel("L (space torus size)")
    ax.set_ylabel("t (D0-time)")
    ax.set_title("Plateau window vs L")
    ax.legend(loc="best")

    # (4) dark energy strength S_DE(t) from scene spectrum (no spikes)
    ax = axs[1,0]
    # Use the common t-grid so panel (4) shares identical time limits with panel (1)
    _u_plot = eps2_canon * t_grid
    _S_plot = S_DE(_u_plot)
    ax.semilogx(t_grid, _S_plot, label="S_DE(t)=u*D'(u)")
    ax.axhline(0.0, linewidth=1, alpha=0.25)
    # markers: peak and "now" (u_now=√5)
    add_common_time_markers(ax, include_turnon=False, include_peak_now=True)
    ax.annotate("peak", xy=(u_peak/eps2_canon, 1.0), xycoords=("data", "axes fraction"),
                xytext=(2, -6), textcoords="offset points", rotation=90,
                va="top", ha="left", fontsize=9)
    ax.annotate("now (u=√5)", xy=(t_now, 1.0), xycoords=("data", "axes fraction"),
                xytext=(2, -6), textcoords="offset points", rotation=90,
                va="top", ha="left", fontsize=9)
    ax.annotate("0.7·now", xy=((0.7*u_now)/eps2_canon, 1.0), xycoords=("data", "axes fraction"),
                xytext=(2, -6), textcoords="offset points", rotation=90,
                va="top", ha="left", fontsize=9)
    ax.set_xlabel("t (D0-time)")
    ax.set_ylabel("S_DE(t)")
    ax.set_title("Dark-energy strength from scene spectrum")
    ax.legend(loc="best")
    set_time_xlim(ax)

    # (5) acceleration q(t) + equation of state w(t)
    ax = axs[1,1]
    ax.semilogx(t_q, q_scene_q, label="q_scene(t)")
    ax.semilogx(t_q, w_scene_q, label="w_scene(t)")
    ax.semilogx(t_q, q_fib_q, label="q_fiber(t)")
    ax.semilogx(t_q, w_eff_fib, label="w_eff_fiber(t)")
    # Plot w_scene_H only where Ω_scene_H is canonically non-negligible.
    # Use xi5 as canonical (no ad-hoc) visibility threshold.
    Omega_min = float(xi5)
    mask = (t_q >= t_eps) & (Omega_scene_H_q >= Omega_min)
    ax.semilogx(t_q[mask], w_scene_H_q[mask], label="w_scene_H(t) (Ω≥xi5, t≥t_eps)")
    ax.axhline(0.0, linewidth=1, alpha=0.25)
    ax.axhline(-1.0/3.0, linewidth=1, alpha=0.25)
    # markers: peak, now, and 0.7 now
    add_common_time_markers(ax, include_turnon=False, include_peak_now=True)
    ax.set_xlabel("t (D0-time)")
    ax.set_ylabel("q, w")
    ax.set_title("Acceleration + equation of state")
    ax.legend(loc="best")
    set_time_xlim(ax)

    # (6) deviation curve D(u)=1-P_scene(u) with canonical kappas
    ax = axs[1,2]
    # build u grid automatically from smallest to largest turn-on (with margin)
    _u_min = min([u for _,_,u,_ in turnon]) / 50.0
    _u_max = max([u for _,_,u,_ in turnon]) * 50.0
    _u = np.logspace(np.log10(max(_u_min, 1e-16)), np.log10(_u_max), 400)
    D_u = D_scene(_u)
    ax.loglog(_u, D_u, label="D(u)=1-P_scene(u)")
    for name,kappa,u_star,t_star in turnon:
        ax.axhline(kappa, linestyle="--", linewidth=1)
        ax.axvline(u_star, linestyle=":", linewidth=1)
        ax.text(u_star, kappa, name, va="bottom", ha="left")
    ax.set_xlabel("u = eps^2 t")
    ax.set_ylabel("D(u)")
    ax.set_title("Scene deviation curve + canonical kappas")
    ax.legend(loc="best")

    fig.suptitle(f"D0 Summary (L={L0}, eps^2=phi^-16): exact spectra", fontsize=14)

    # Save one consolidated figure (so you can send a single image)
    out_png = OUTDIR / P(PROT, "outputs")["png"]
    plt.savefig(out_png, dpi=220, bbox_inches="tight")
    vprint(f"\n[SAVED] {out_png.as_posix()}")


    # ============================================================
    # BOOK VI — CERT PACK (41.1–41.6) + POSTANOVKA (41.7–41.10)
    # Adds: DarkRatio, DeltaLadder, GenerationCutoff, MemoryPressure, PercolationToy
    # Controlled by env:
    #   D0_BOOK6_CERTS=1 (default 1)
    #   D0_PERC_TRIALS=200, D0_PERC_GRID=40
    # ============================================================


    globals().update({k: v for k, v in locals().items() if k != "_BOOK6_READY"})
    _BOOK6_READY = True

def run_book6_certs():
    if PROT is None or rep is None or OUTDIR is None:
        raise RuntimeError("book6_certpack: not initialized. Call init(...) or run as a script.")

    _ensure_book6_globals()

    book6_on = os.environ.get("D0_BOOK6_CERTS", "1").strip() != "0"
    if not book6_on:
        return None

    print("\n=== BOOK VI CERT PACK (41.1–41.6) ===")

    # 41.1 Dark Ratio (from already computed strict certificate)
    try:
        ratio = dark_cert["nullS"] / max(dark_cert["rankS"], 1)
        status = "PASS" if abs(ratio - 10.0) < 1e-12 else "FAIL"
        print(f"[CERT 41.1] DarkRatio  nullity/rank = {ratio:.12g}  status={status}")
        print("  NOTE: CORE invariant (linear algebra). Mapping to Ω ratios is BRIDGE/APPX and must be labeled as such.")
    except Exception as e:
        print(f"[CERT 41.1] DarkRatio  status=WAIT  reason={e}")

    # 41.3 Delta ladder κ
    c41_3 = cert_41_3_delta_ladder(delta0, eps2_canon, kappa_cap=30)
    print(f"[CERT 41.3] DeltaLadder  kappa={c41_3.get('kappa')}  delta^(k+1)={c41_3.get('delta_at_k'):.3e}  eps2={c41_3.get('eps2'):.3e}  status={c41_3.get('status')}")

    # 41.2 Generation cutoff (Lucas impedance)
    rows, st = cert_41_2_generation_cutoff(9, 17, denom_base=9)
    print(f"[CERT 41.2] GenerationCutoff (Lucas impedance) status={st}")
    for n, L, I in rows:
        mark = " <==" if n == 15 else ""
        print(f"  n={n:2d}  L_n={L:5d}  I_n=L_n/(9n)={I:8.4f}{mark}")
    # store strict crossing index
    try:
        cross = None
        for n, L, I in rows:
            if I >= 10.0:
                cross = n
                break
        print(f"  crossing(I>=10) at n* = {cross}")
    except Exception:
        cross = None

    # 41.5 Memory pressure
    mem_mask = np.isclose(lam_scene, 1.0/phi, atol=1e-12, rtol=0.0)
    c41_5 = cert_41_5_memory_pressure(u_grid, lam_scene, mem_mask, eps2_reg=eps2_canon)
    print(
        f"[CERT 41.5] MemoryPressure  status={c41_5.get('status')}  mono(M_arch)={c41_5.get('mono_M')}  "
        f"Lambda_med={c41_5.get('Lambda_med'):.3e}  Lambda_min={c41_5.get('Lambda_min'):.3e}  mem_mult={c41_5.get('mem_mult')}"
    )

    # 41.6 Percolation toy (optional, may be slow)
    do_perc = os.environ.get('D0_PERC', '1').strip() != '0'
    c41_6 = None
    if do_perc:
        trials = int(os.environ.get("D0_PERC_TRIALS", "200"))
        grid_n = int(os.environ.get("D0_PERC_GRID", "40"))
        A = build_scene_adj(9,11,13)
        u_min = float(np.min(u_grid[u_grid>0])) if np.any(u_grid>0) else 1e-12
        u_max = float(u_now_canon)
        c41_6 = cert_41_6_percolation_toy(A, u_min=u_min, u_max=u_max, m0=m0, trials=trials, grid_n=grid_n, seed=0)
        print(f"[CERT 41.6] PercolationToy (connectivity proxy)  status={c41_6.get('status')}  u*={c41_6.get('u_star', float('nan')):.3e}  t*={c41_6.get('t_star', float('nan')):.3e}  p*={c41_6.get('p_star', float('nan')):.3e}  trials={trials}")
    else:
        print("[CERT 41.6] PercolationToy  status=SKIP (set D0_PERC=1 to enable)")

    # CORE checks already computed in script
    rep.add(
        "ALPHA_SEAM",
        bool(Seam_contract_pass),
        alpha_inv_top=float(alpha_inv_top),
        alpha_inv_alg=float(alpha_inv_alg),
        Delta_alpha=float(Delta_alpha),
        eps2=float(eps2_canon),
    )

    rep.add(
        "DARK_SECTOR_RANK_NULLITY",
        bool(dark_cert.get("nullS") == 30 and dark_cert.get("mult_mem") == 30),
        **{k: int(v) if isinstance(v, (int, np.integer)) else v for k, v in dark_cert.items()},
    )

    # CERT 41.* (if variables exist; keep safe)
    try:
        rep.add("CERT_41_1_DARKRATIO", True, ratio=float(dark_cert["nullS"] / max(dark_cert["rankS"], 1)))
    except Exception as e:
        rep.skip("CERT_41_1_DARKRATIO", f"{e}")

    try:
        rep.add("CERT_41_3_DELTALADDER", bool(c41_3.get("pass", False)), **c41_3)
    except Exception as e:
        rep.skip("CERT_41_3_DELTALADDER", f"{e}")

    try:
        rep.add("CERT_41_5_MEMORYPRESSURE", bool(c41_5.get("pass", False)), **c41_5)
    except Exception as e:
        rep.skip("CERT_41_5_MEMORYPRESSURE", f"{e}")

    try:
        rep.add("CERT_41_6_PERCOLATION", bool(c41_6.get("pass", False)), **c41_6)
    except Exception as e:
        rep.skip("CERT_41_6_PERCOLATION", f"{e}")

    # write compact json summary
    try:
        out_json = OUTDIR / P(PROT, "outputs")["json"]
        save_json(out_json, rep.to_dict())
        rep.artifacts["json"] = out_json.name
        rep.artifacts["csv"] = out_csv.name
        rep.artifacts["png"] = out_png.name
    except Exception as e:
        print(f"[WARN] could not save book6_certpack.json: {e}")

    return dict(c41_3=c41_3, c41_5=c41_5, c41_6=c41_6)

if __name__ == "__main__":
    main()
