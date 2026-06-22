#!/usr/bin/env python3
"""Append the 11 D0-v15 registry rows to CLAIM_TO_LEAN_MAP.csv (idempotent)."""
import csv, os, sys
sys.stdout.reconfigure(encoding="utf-8")
REG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "09_LEAN_FORMALIZATION", "docs", "CLAIM_TO_LEAN_MAP.csv")
rows = list(csv.reader(open(REG, encoding="utf-8", newline="")))
H = rows[0]
existing = {r[0] for r in rows[1:] if r}
M = "D0.Integration.V15."
# claim_id, book, section, lean_module, lean_theorem, lean_status, uses_bridge, assumption_ids, cert, release, notes
NEW = [
 ["D0-ZONE-CURRENT-001","BOOK_04","v15 zone current",M+"RawZone","zone_current_spine","LEAN_PROVED","False","","vp_zone_current_spine.py","CORE-FORMALIZED",
  "v15 WP-A THE. J=i[D,A] G-Hermitian in canonical part-size inner product G=diag(9,11,13); comm^3=-2840*comm; spectrum {0,+-2sqrt710}. FIREWALL: not a physical current/neutrino/charge."],
 ["D0-ZONE-NEUTRAL-ACTIVE-SPLIT-001","BOOK_04","v15 zone split",M+"RawZone","zone_current_spine","LEAN_PROVED","False","","vp_zone_current_spine.py","CORE-FORMALIZED",
  "v15 WP-A THE. ran(A)=neutral(1)+active(2) via G-orthogonal projectors P0,Pact (tr 1/2). Corrected from oblique (CONDITIONAL) to G-orthogonal (THE)."],
 ["D0-FESHBACH-SCHUR-FACTORIZATION-V15","BOOK_02","v15 Feshbach",M+"Feshbach","feshbach_schur_factorization","LEAN_PROVED","False","","","CORE-FORMALIZED",
  "v15 WP-E1 THE (algebraic identity only). det[[A,B],[C,I]]=det(A-B*C); Mathlib det_fromBlocks_one22. NOT an energy-pressure tensor."],
 ["D0-BRANCH-CP-READOUT-NOGO-V15","BOOK_04","v15 branch coupling",M+"BranchAudit","branch_readout_not_unique","LEAN_PROVED","False","","","NO-GO",
  "v15 WP-B NO-GO. branch commutant>C*I (3 blocks); same marginals, different coherence. Missing PRIM-BRANCH-ISOTROPIC-READOUT."],
 ["D0-LEPTON-DECIMAL-MASS-RATIOS","BOOK_04","v15 lepton mass ratios",M+"BranchAudit","mass_ratio_underdetermined","LEAN_PROVED","False","","","NO-GO",
  "v15 WP-D NO-GO. Vandermonde {0,1/4,1/3} det=1/144!=0; any (r_mu,r_tau) realizable. Missing PRIM-EFT-IR-MATCHING-FUNCTIONAL."],
 ["D0-P1-PHYSICAL-EOS","BOOK_08","v15 equation of state",M+"Feshbach","eos_underdetermined","LEAN_PROVED","False","","","NO-GO",
  "v15 WP-E2 NO-GO. same total response, distinct w=p/rho. Missing PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT. No 1+z=phi^n, no rho=e^u-1."],
 ["D0-EDGE-COVER-FAMILY-001","BOOK_04","v15 physical edge cover",M+"EdgeAudit","edge_cover_is_family","LEAN_PROVED","False","","","PROOF-TARGET",
  "v15 WP-C CONDITIONAL-EXTENSION. edge dim 359; lambda-family (z^3 coeff=-lambda). Missing PRIM-EDGE-HOLONOMY-SELECTOR. Halmos existence != uniqueness."],
 ["D0-STURMIAN-REFINEMENT","BOOK_06","v15 Sturmian refinement",M+"Refinement","sturmian_golden_tower","LEAN_PROVED","False","","","PROOF-TARGET",
  "v15 WP-F2 CONDITIONAL-EXTENSION. golden incidence det=-1,trace=1 (phi). Missing PRIM-STURMIAN-REFINEMENT-OWNER. No CFT/Virasoro import."],
 ["D0-ARCHIVE-REGULAR-REFINEMENT-NOGO-001","BOOK_01","v15 archive refinement",M+"Refinement","archive_window_not_measure_preserving","LEAN_PROVED","False","","","NO-GO",
  "v15 WP-F1 NO-GO. archive window 359/160 != 1 (regular cover ratio); archive map is contracting, not a regular cover."],
 ["D0-PRESENT-CORE-LIMITS-REGRESSION-V15","BOOK_05","v15 no-go regression",M+"PhysicalBoundary","regression_owners_present","LEAN_PROVED","False","","","NO-GO",
  "v15 WP-G. present-core limits unchanged (6 owners); finite heat-trace no pole; c_D0=1 (not SI c)."],
 ["D0-AMS-HEAVY-NUCLEI-PASSPORT-001","BOOK_05","v15 AMS passport",M+"PhysicalBoundary","ams_is_passport","LEAN_PROVED","False","","","EMPIRICAL-PASSPORT",
  "v15 WP-H EXTERNAL-PASSPORT. external flux b~1/3 (P,S,Cl), ~1/2 (Ar,K,Ca); amsHasInternalOwner=false. Needs internal nuclear-flux transfer operator. Comparison only."],
]
added = 0
with open(REG, "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    for r in NEW:
        if r[0] in existing:
            print("  skip (exists):", r[0]); continue
        assert len(r) == len(H), f"col mismatch {len(r)} vs {len(H)} for {r[0]}"
        w.writerow(r); added += 1; print("  added:", r[0])
print(f"[OK] appended {added} rows ({len(H)} cols each)")
