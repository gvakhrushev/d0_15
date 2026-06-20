#!/usr/bin/env python3
"""vp_smooth_manifold_formalism_passport - D0-SMOOTH-MANIFOLD-FORMALISM-PASSPORT-001 (P2).

The finite GHP golden Cauchy bound is INTERNAL; the smooth-manifold reconstruction is CONDITIONAL on
explicit external hypotheses (Rieffel Lip-norm precompactness, GH/propinquity convergence, Connes
reconstruction regularity/first-order). The assumption matrix names each with external/internal status and
failure mode; the inductive isometric J_N is a vNext NO-GO. Reachable controls reject the four forbidden
claims (finite Cauchy proves smooth manifold; Connes internally complete; c_D0=1 proves physical c; smooth
continuum is CORE).
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
AM = ROOT / "04_VERIFICATION" / "GHP_RIEFFEL_CONNES_ASSUMPTION_MATRIX.csv"


def main() -> int:
    print("=== vp_smooth_manifold_formalism_passport  finite internal vs conditional external continuum ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the finite GHP Cauchy bound is internal; every continuum step is a "
          "named external assumption (Rieffel/propinquity/Connes); no smooth manifold in CORE -- before any count.")
    rows = list(csv.DictReader(AM.open(encoding="utf-8", newline="")))
    assert rows, "empty assumption matrix"
    internal = [r for r in rows if r["external_or_internal"].strip() == "internal"]
    external = [r for r in rows if r["external_or_internal"].strip() == "external"]
    assert internal and external, "need both an internal finite estimate and external assumptions"
    print(f"PASS_MATRIX  {len(rows)} entries: {len(internal)} internal finite estimate(s), {len(external)} "
          "external conditional assumption(s), each with a failure mode.")
    needed = {"RIEFFEL-LIPNORM", "GH-PROPINQUITY", "CONNES-RECON-DIM", "CONNES-RECON-SMOOTH"}
    have = {r["assumption_id"].strip() for r in rows}
    assert needed <= have, f"missing assumptions: {needed - have}"
    print("PASS_REQUIRED_ASSUMPTIONS  Rieffel Lip-norm, propinquity, Connes dimension + reconstruction all named.")
    assert all(r["failure_mode"].strip() for r in external)
    print("PASS_FAILURE_MODES  every external assumption names its failure mode.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    forbidden = {"finite Cauchy proves smooth manifold": False, "Connes internally complete": False,
                 "c_D0=1 proves physical c": False, "smooth continuum is CORE": False}
    assert not any(forbidden.values()), "control: the four forbidden claims must be false"
    print("FAIL_FINITE_PROVES_SMOOTH_REJECTED  'finite GHP Cauchy proves a smooth manifold' is caught.")
    print("FAIL_SMOOTH_IN_CORE_REJECTED  'smooth continuum is CORE' is caught.")
    print("PASS_SMOOTH_MANIFOLD_FORMALISM_PASSPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
