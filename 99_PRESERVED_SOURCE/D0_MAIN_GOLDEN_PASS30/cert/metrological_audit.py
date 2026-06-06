"""
D0 METROLOGICAL AUDIT SUITE (BOOK IV — §44)
Purpose:
  Audit experimental *claims* against D0 structural invariants (CORE→BRIDGE).
  This is NOT an engineering manual and does not prescribe device construction.

Contract:
  - No new constants: φ, δ0, ε², Δα are derived canonically (see BOOK I–III, VI).
  - Outputs are BRIDGE-criteria only: COMPATIBLE / INCOMPATIBLE / INCONCLUSIVE.

Usage (example):
  python cert/metrological_audit.py --claim "Device_X" \
      --geom R=119.821 r=100.0 \
      --spectrum f0=100 peaks=161.8,261.8,423.6 \
      --power out=9.0 in=100.0
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple, Dict, Any

from d0.constants import phi as PHI, psi as PSI, delta0 as DELTA0, xi5 as XI5, eps2 as EPS2, pi0 as PI0
from d0.protocol import load_protocol, P
from d0.io import get_outdir, save_json
from d0.report import CertReport

# -------------------------
# IMMUTABLE CANON (BOOK I–III)
# -------------------------

# Rank/Nullity for K(9,11,13) adjacency A (BOOK III, D0 §17.1)
RANK: int = 3
NULLITY: int = 30

# Δα (seam width) derived from canonical α certificates (BOOK III + code)
def alpha_inv_top() -> float:
    # α_top^{-1} = 359/φ^2 − ξ5  (from φ–PDG strict certificate block)
    return 359.0 / (PHI ** 2) - XI5

def alpha_inv_alg() -> float:
    # α_alg^{-1} = 2^11·π0/φ^8 + 2·δ0/3  (BOOK III §16.3)
    return (2.0 ** 11) * PI0 / (PHI ** 8) + (2.0 * DELTA0) / 3.0

DELTA_ALPHA: float = abs(alpha_inv_alg() - alpha_inv_top())
# Seam theorem (BOOK III §16.3): Δα < ε² must hold inside the corpus.
SEAM_CONTRACT_PASS: bool = (DELTA_ALPHA < EPS2)
if not SEAM_CONTRACT_PASS:
    import warnings
    warnings.warn(
        f"[D0 CANON WARNING] Seam theorem violated: Δα={DELTA_ALPHA:.12g} >= ε²={EPS2:.12g}. "
        "Check that α_alg uses structural π0, not π."
    )

# Torus shows up in corpus as (R+r)/(R-r) = φ^5  (BOOK VI §31.2 / BOOK I geometry refs)
# A meter-friendly form-factor: major/minor ratio R/r forced by φ^5
TORUS_R_OVER_r: float = (PHI ** 5 + 1.0) / (PHI ** 5 - 1.0)  # = R/r


# -------------------------
# Helpers
# -------------------------

def relerr(x: float, y: float) -> float:
    if y == 0:
        return float("inf")
    return abs(x - y) / abs(y)

def nearest_phi_power_ratio(r: float) -> Tuple[int, float]:
    """
    Return (k, r_hat) where r_hat = φ^k is nearest to r in log space.
    """
    if r <= 0:
        return (0, float("nan"))
    k = int(round(math.log(r, PHI)))
    return (k, PHI ** k)

def phi_scaled_peaks(peaks: List[float], f0: float, tol: float = EPS2) -> List[Tuple[float, int, float]]:
    """
    For each peak f, check if f/f0 ≈ φ^k within relative tolerance tol.
    Return list of (f, k, relerr).
    """
    out = []
    if f0 <= 0:
        return out
    for f in peaks:
        if f <= 0:
            continue
        k, r_hat = nearest_phi_power_ratio(f / f0)
        f_hat = f0 * r_hat
        e = relerr(f, f_hat)
        if e <= tol:
            out.append((f, k, e))
    return out


# -------------------------
# Audit result model
# -------------------------

@dataclass
class AuditItem:
    PASS: bool
    msg: str
    payload: Dict[str, Any]

@dataclass
class AuditReport:
    claim_id: str
    eps2: float
    results: Dict[str, AuditItem]

    def overall(self) -> str:
        if not self.results:
            return "INCONCLUSIVE"
        # HARD FAIL if any structural invariant fails
        if any(not r.PASS for r in self.results.values()):
            return "INCOMPATIBLE"
        return "COMPATIBLE"


# -------------------------
# Auditor
# -------------------------

class D0Auditor:
    """
    CORE→BRIDGE auditor for metrological claims.
    """

    def __init__(self, claim_id: str = "Unknown"):
        self.claim_id = claim_id
        self.results: Dict[str, AuditItem] = {}

    # AUDIT-1: geometry (torus form-factor)
    def audit_geometry_R_r(self, R: float, r: float, tol: float = EPS2) -> AuditItem:
        """
        Checks major/minor ratio R/r against D0 torus invariant.
        """
        if r <= 0 or R <= 0 or R <= r:
            item = AuditItem(False, "Invalid (R,r) geometry", {"R": R, "r": r})
            self.results["P-GEOM"] = item
            return item

        ratio = R / r
        e = relerr(ratio, TORUS_R_OVER_r)
        ok = e <= tol
        msg = f"P-GEOM: R/r={ratio:.12f}, D0={TORUS_R_OVER_r:.12f}, relerr={e:.3e}, tol=ε²={tol:.3e}"
        item = AuditItem(ok, msg, {"ratio": ratio, "target": TORUS_R_OVER_r, "relerr": e, "tol": tol})
        self.results["P-GEOM"] = item
        return item

    # AUDIT-2: spectrum (φ-scaling)
    def audit_spectrum_phi(self, peaks_hz: List[float], f0: float, min_hits: int = 2, tol: float = EPS2) -> AuditItem:
        """
        Checks for φ-lattice scaling in peaks relative to base f0.
        min_hits=2 is minimal distinguishability (needs ≥2 points).
        """
        hits = phi_scaled_peaks(peaks_hz, f0=f0, tol=tol)
        ok = len(hits) >= min_hits
        msg = f"P-SPECTRA: hits={len(hits)}/{len(peaks_hz)} (need ≥{min_hits}), tol=ε²={tol:.3e}"
        item = AuditItem(ok, msg, {"f0": f0, "peaks": peaks_hz, "hits": hits, "min_hits": min_hits, "tol": tol})
        self.results["P-SPECTRA"] = item
        return item

    # AUDIT-3: seam modulation (Δα beat)
    def audit_seam_modulation(self, f_carrier: float, f_observed_mod: Optional[float] = None, tol: float = EPS2) -> AuditItem:
        """
        Predicts structural modulation frequency f_mod = Δα * f_carrier (beat law).
        If observed modulation is provided, checks consistency.
        """
        if f_carrier <= 0:
            item = AuditItem(False, "Invalid carrier frequency", {"f_carrier": f_carrier})
            self.results["P-SEAM"] = item
            return item

        f_pred = DELTA_ALPHA * f_carrier
        payload = {"f_carrier": f_carrier, "delta_alpha": DELTA_ALPHA, "f_pred": f_pred, "tol": tol}

        if f_observed_mod is None:
            item = AuditItem(True, f"P-SEAM: predicted f_mod=Δα·f_c={f_pred:.12g} Hz (no observed value supplied)", payload)
            self.results["P-SEAM"] = item
            return item

        e = relerr(f_observed_mod, f_pred)
        ok = e <= tol
        msg = f"P-SEAM: f_obs={f_observed_mod:.12g} Hz, f_pred={f_pred:.12g} Hz, relerr={e:.3e}, tol=ε²={tol:.3e}"
        payload.update({"f_obs": f_observed_mod, "relerr": e})
        item = AuditItem(ok, msg, payload)
        self.results["P-SEAM"] = item
        return item

    # AUDIT-4: power balance (Rank/Nullity ceiling)
    def audit_power_ratio(self, measured_output: float, total_input: float, tol: float = EPS2) -> AuditItem:
        """
        Structural ceiling for *observable* efficiency when a claim asserts involvement of Nullity modes.
        Derived ceiling (no extra weights): η_obs ≤ rank/(rank+nullity) = 3/33 = 1/11.
        """
        if total_input <= 0:
            item = AuditItem(False, "Invalid total input", {"total_input": total_input})
            self.results["P-RATIO"] = item
            return item

        eta = measured_output / total_input
        eta_max = RANK / (RANK + NULLITY)
        ok = eta <= eta_max * (1.0 + tol)  # allow ε² slack
        msg = f"P-RATIO: η_obs={eta:.6f}, ceiling={eta_max:.6f} (=rank/(rank+nullity)), tol=ε²={tol:.3e}"
        item = AuditItem(ok, msg, {"eta_obs": eta, "ceiling": eta_max, "tol": tol, "rank": RANK, "nullity": NULLITY})
        self.results["P-RATIO"] = item
        return item

    def report(self) -> AuditReport:
        return AuditReport(claim_id=self.claim_id, eps2=EPS2, results=self.results)


# -------------------------
# CLI
# -------------------------

def _parse_keyvals(s: str) -> Dict[str, float]:
    """
    Parse "R=...,r=..." style tokens.
    """
    out = {}
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        k,v = part.split("=")
        out[k.strip()] = float(v)
    return out

def _parse_flist(s: str) -> List[float]:
    return [float(x.strip()) for x in s.split(",") if x.strip()]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", default=os.environ.get("D0_PROTOCOL", "protocols/metrological_audit.json"))
    ap.add_argument("--claim", default="Unknown")
    ap.add_argument("--selftest", action="store_true", help="Run built-in canonical example that should PASS all audits.")
    ap.add_argument("--geom", default=None, help="Geometry as 'R=...,r=...' (major/minor)")
    ap.add_argument("--spectrum", default=None, help="Spectrum as 'f0=... peaks=f1,f2,...'")
    ap.add_argument("--seam", default=None, help="Seam as 'fc=... [fmod=...]'")
    ap.add_argument("--power", default=None, help="Power as 'out=... in=...'")
    args = ap.parse_args()

    PROT = load_protocol(args.protocol)
    OUTDIR = get_outdir()
    rep = CertReport(cert_id="METRO_AUDIT", protocol_id=PROT.protocol_id)
    rep.add("PROTO_LOADED", True, protocol=args.protocol)

    claim_id = args.claim
    if args.selftest and (claim_id == "Unknown" or not claim_id.strip()):
        claim_id = "SELFTEST"
    A = D0Auditor(claim_id)

    if args.selftest:
        # Canonical reference dataset (no external catalog): should PASS by construction.
        r0 = 100.0
        A.audit_geometry_R_r(R=TORUS_R_OVER_r * r0, r=r0)

        f0 = 100.0
        peaks = [f0 * (PHI ** k) for k in (2, 3, 4)]
        A.audit_spectrum_phi(peaks_hz=peaks, f0=f0)

        fc = 1000.0
        A.audit_seam_modulation(f_carrier=fc, f_observed_mod=DELTA_ALPHA * fc)

        A.audit_power_ratio(measured_output=1.0, total_input=20.0)

    else:
        if args.geom:
            kv = _parse_keyvals(args.geom)
            A.audit_geometry_R_r(R=kv.get("R", 0.0), r=kv.get("r", 0.0))

        if args.spectrum:
            # format: "f0=100 peaks=161.8,261.8"
            parts = args.spectrum.split()
            kv = {}
            for p in parts:
                if "=" in p:
                    k, v = p.split("=", 1)
                    kv[k.strip()] = v.strip()
            f0 = float(kv.get("f0", "0"))
            peaks = _parse_flist(kv.get("peaks", ""))
            A.audit_spectrum_phi(peaks_hz=peaks, f0=f0)

        if args.seam:
            kv = _parse_keyvals(args.seam)
            fc = kv.get("fc", 0.0)
            fmod = kv.get("fmod", None)
            A.audit_seam_modulation(f_carrier=fc, f_observed_mod=fmod)

        if args.power:
            kv = _parse_keyvals(args.power)
            A.audit_power_ratio(measured_output=kv.get("out", 0.0), total_input=kv.get("in", 0.0))

    R = A.report()

    for k, item in R.results.items():
        rep.add(k, bool(item.PASS), msg=item.msg)
    if not R.results:
        rep.skip("NO_AUDITS", "no checks were run")

    print("\n=== D0 METROLOGICAL AUDIT REPORT ===")
    print(f"claim_id = {R.claim_id}")
    print(f"eps2     = {R.eps2:.12g}")
    print(f"phi      = {PHI:.15g}")
    print(f"delta0   = {DELTA0:.15g}")
    print(f"pi0      = {PI0:.15g}")
    print(f"deltaα   = {DELTA_ALPHA:.12g}  (Δα<ε²: {'PASS' if SEAM_CONTRACT_PASS else 'FAIL'})")
    print(f"R/r*     = {TORUS_R_OVER_r:.12g}")
    print(f"ceiling  = {RANK}/({RANK}+{NULLITY}) = {RANK/(RANK+NULLITY):.12g}")
    for k,item in R.results.items():
        status = "PASS" if item.PASS else "FAIL"
        print(f"[{k}] {status}  {item.msg}")
    if not R.results:
        print("\n[HINT] No audits were run. Provide at least one of: --geom, --spectrum, --seam, --power")
        print("       or run the built-in reference run: --selftest")

    out_json = OUTDIR / P(PROT, "outputs")["json"]
    save_json(out_json, rep.to_dict())

    overall = R.overall()
    print(f"\n>>> FINAL VERDICT: {overall}")

    return 0 if overall == "COMPATIBLE" else 2

if __name__ == "__main__":
    raise SystemExit(main())
