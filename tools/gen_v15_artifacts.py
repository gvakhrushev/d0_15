#!/usr/bin/env python3
"""gen_v15_artifacts.py — emit the 6 D0-v15 machine-readable artifacts from one source of truth.

Deterministic: the node table below is the single source; the CSV/JSON/MD artifacts are generated.
Run:  python tools/gen_v15_artifacts.py
"""
import csv, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "artifacts")
os.makedirs(ART, exist_ok=True)

# claim_id, statement, source_owner, exact_formula_or_theorem, admissible_class, symmetry_group,
# gauge_relation, proof_module, negative_control, status_before, status_after, reason, book_patch
NODES = [
 ["D0-ZONE-CURRENT-001",
  "Zone commutator generator J=i[D_W,A_W] is G-Hermitian (canonical part-size inner product G=diag(9,11,13)) with spectrum {0,+-2sqrt710}",
  "D0-KERNEL-ZONE-SPLIT-001 (D0.Claims.KernelZoneSplit)",
  "comm^3=-2840*comm; (G*comm)^T=-(G*comm); spectrum {0,+-2sqrt710}",
  "i[D_W,W], W frozen zone-label weight on ran(A)",
  "Aut_raw acts trivially on the 3-dim quotient (part sizes distinct)",
  "global phase only; convention A_W vs A_W^T both symmetrize to n_i n_j (resolved by G)",
  "D0.Integration.V15.RawZone.zone_current_spine",
  "diagonal-only adjacency -> comm=0; naive Euclidean G=I not Hermitian",
  "CONDITIONAL (naive, oblique)", "THE",
  "Hermiticity gate met in the canonical frozen part-size inner product; projectors genuinely G-orthogonal",
  "Book04: zone-current theorem"],
 ["D0-ZONE-NEUTRAL-ACTIVE-SPLIT-001",
  "ran(A)=neutral(1)+active(2) via G-orthogonal spectral projectors P0,Pact of J",
  "D0-ZONE-CURRENT-001",
  "P0+Pact=I; (G*Pact)^T=G*Pact; tr Pact=2, tr P0=1; neutral vec (143,-234,99)",
  "spectral projectors of J (polynomials in J)",
  "trivial (canonical eigenspaces of a fixed frozen operator)",
  "unique orthogonal projectors of a G-Hermitian operator",
  "D0.Integration.V15.RawZone.zone_current_spine",
  "remove degree splitting -> ambiguity returns",
  "CONDITIONAL", "THE",
  "orthogonal (not oblique) once G is used; FIREWALL: not a physical neutral current/neutrino/charge",
  "Book04: neutral/active response theorem"],
 ["D0-FESHBACH-SCHUR-FACTORIZATION-V15",
  "Schur/Feshbach determinant factorization det[[A,B],[C,I]]=det(A-B*C)",
  "D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001",
  "det Mfull=4=det(A-B*C); Mathlib det_fromBlocks_one22; -d/dz logdet(I-zU)=R_Q+R_P",
  "block operators with invertible D-block",
  "n/a (algebraic identity)", "n/a",
  "D0.Integration.V15.Feshbach.feshbach_schur_factorization",
  "n/a (identity)",
  "(identity not previously isolated)", "THE (algebraic identity only)",
  "true block-determinant identity; NOT an energy-pressure tensor",
  "Book02: Feshbach two-source factorization"],
 ["D0-BRANCH-CP-READOUT-NOGO-V15",
  "Branch CP readout is not unique: commutant wider than C*I; same marginals, different coherence",
  "D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001",
  "commutantDim=3>1; rho1!=rho2 with equal diagonal",
  "Stinespring V:W->H_br(x)E with V*(E_j)V=Q_j",
  "branch group; 3 isotypic generation blocks",
  "branch-unitary + environment-unitary gauge",
  "D0.Integration.V15.BranchAudit.branch_readout_not_unique",
  "two admissible readouts share frozen marginals yet differ",
  "(open)", "NO-GO",
  "branch symmetry leaves a family; needs PRIM-BRANCH-ISOTROPIC-READOUT",
  "Book04: branch-coupling no-go"],
 ["D0-LEPTON-DECIMAL-MASS-RATIOS",
  "Lepton mass ratios underdetermined by branch exponents {0,1/4,1/3}",
  "D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001",
  "Vandermonde det at {0,1/4,1/3}=1/144!=0 -> any (r_mu,r_tau) realized by a smooth m(p)",
  "smooth positive matching functions on the 3 exponents",
  "n/a", "n/a",
  "D0.Integration.V15.BranchAudit.mass_ratio_underdetermined",
  "explicit quadratic interpolants for two distinct target pairs",
  "(open)", "NO-GO",
  "exponents impose no constraint on ratios; needs PRIM-EFT-IR-MATCHING-FUNCTIONAL",
  "Book04: lepton EFT/IR mass-ratio no-go"],
 ["D0-P1-PHYSICAL-EOS",
  "Physical equation of state w=p/rho not determined by two-source response",
  "D0-ARCHIVE-CONTRACTION-NOGO-001",
  "(rho,p)=(3,1) and (1,3): same total 4, distinct w (1/3 vs 3)",
  "(rho,p) assignments with identical response data",
  "n/a", "n/a",
  "D0.Integration.V15.Feshbach.eos_underdetermined",
  "two inequivalent (rho,p) with identical response, distinct w",
  "(open)", "NO-GO",
  "response fixes only the total; needs PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT; no rho=e^u-1,p=e^u/phi",
  "Book08: keep internal-scale vs physical w(z) separate"],
 ["D0-EDGE-COVER-FAMILY-001",
  "Physical edge cover is a 1-parameter holonomy family in lambda",
  "D0-EDGE-ALPHA-001 (D0.Spectral.ZetaResidueAlpha)",
  "edge dim 359; z^3 coeff of (1-lz^4)(1-lz^3) = -lambda; lambda not fixed by frozen data",
  "W_lambda edge-star modes, lambda free",
  "U(1) holonomy circle", "lambda-gauge until externally fixed",
  "D0.Integration.V15.EdgeAudit.edge_cover_is_family",
  "lambda=1 vs 2 give different cover observables; arbitrary unitary breaks source-derivation",
  "(open)", "CONDITIONAL-EXTENSION",
  "lambda unfixed; needs PRIM-EDGE-HOLONOMY-SELECTOR; Halmos existence != uniqueness",
  "Book04: physical edge status (conditional)"],
 ["D0-STURMIAN-REFINEMENT",
  "Golden substitution sigma(a)=ab,sigma(b)=a is a valid refinement tower (Perron phi)",
  "D0-PHI-STURMIAN-CYLINDER-CONJUGACY-001",
  "incidence [[1,1],[1,0]]: det=-1, trace=1, charpoly t^2-t-1, phi^2=phi+1",
  "substitution / Bratteli tower",
  "n/a", "n/a",
  "D0.Integration.V15.Refinement.sturmian_golden_tower",
  "Sturmian data removed -> downgrade to conditional",
  "(open)", "CONDITIONAL-EXTENSION",
  "valid extension; identifying with archive maps needs PRIM-STURMIAN-REFINEMENT-OWNER; no CFT import",
  "Book06: Sturmian theorem (conditional)"],
 ["D0-ARCHIVE-REGULAR-REFINEMENT-NOGO-001",
  "Archive bonding map is not a regular (measure-preserving) cover",
  "D0-ARCHIVE-CONTRACTION-NOGO-001",
  "regular cover ratio=1; archive window=359/160!=1",
  "regular mod-N covers C_2N->C_N",
  "rotation Z/2N->Z/N", "n/a",
  "D0.Integration.V15.Refinement.archive_window_not_measure_preserving",
  "actual archive map (window 359/160) vs constant-fibre regular cover",
  "(open)", "NO-GO",
  "archive map is contracting, not regular; do not substitute a regular cover",
  "Book01: refinement source data"],
 ["D0-PRESENT-CORE-LIMITS-REGRESSION-V15",
  "Present-core limits (heat-trace no pole, alpha blocked, c_D0!=c, internal flow != w(z), passports) unchanged",
  "D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001 + suite",
  "finiteHeatTracePoles=0; c_D0=1; 6 owners unchanged",
  "each named owner's full admissible class",
  "n/a", "n/a",
  "D0.Integration.V15.PhysicalBoundary.regression_owners_present",
  "per-owner negative controls (unchanged)",
  "NO-GO (each)", "NO-GO (regression holds)",
  "v15 work did not breach established limits",
  "Book05: ledger artifact-vs-claim split"],
 ["D0-AMS-HEAVY-NUCLEI-PASSPORT-001",
  "AMS heavy-nuclei flux is an external comparison passport (b~1/3 P,S,Cl; b~1/2 Ar,K,Ca)",
  "NONE (external; nearest internal D0-SRC-001)",
  "Phi_X=a_X Phi_Si + b_X Phi_F; amsHasInternalOwner=false",
  "external flux model", "n/a", "n/a",
  "D0.Integration.V15.PhysicalBoundary.ams_is_passport",
  "no internal nuclear carrier exists",
  "(none)", "EMPIRICAL-PASSPORT",
  "external target; needs internal nuclear-flux transfer operator before any prediction",
  "Book05: passport row (non-core)"],
]

REJECTED = [
 "D0_INTERFACE_DISPLACEMENT_RESULT","D0_DYADIC_REFINEMENT_AND_SEAM_GROUPOID_RESULT",
 "D0_UNIVERSAL_PHASE_BRANCH_AND_FESHBACH_RESULT","D0_X5_INTERFACE_BRANCH_ROUTE_FINAL_NO_GO",
 "D0_CANONICAL_ZONE_CURRENT_RESULT","D0_ZONE_STURMIAN_PHI_CLOSURE_RESULT",
 "D0_LEPTON_BRANCH_COUPLING_CLOSURE","D0_PHYSICAL_EDGE_COVER_AND_EFT_IR_BOUNDARY",
]

MISSING_PRIMITIVES = {
 "D0-BRANCH-CP-READOUT-NOGO-V15":"PRIM-BRANCH-ISOTROPIC-READOUT",
 "D0-LEPTON-DECIMAL-MASS-RATIOS":"PRIM-EFT-IR-MATCHING-FUNCTIONAL",
 "D0-P1-PHYSICAL-EOS":"PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT",
 "D0-EDGE-COVER-FAMILY-001":"PRIM-EDGE-HOLONOMY-SELECTOR",
 "D0-STURMIAN-REFINEMENT":"PRIM-STURMIAN-REFINEMENT-OWNER",
}

HEADER = ["claim_id","statement","source_owner","exact_formula_or_theorem","admissible_class",
 "symmetry_group","gauge_relation","proof_module","negative_control","status_before","status_after",
 "reason_for_status","book_patch"]

# 1. claim manifest CSV
with open(os.path.join(ART,"v15_claim_manifest.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(HEADER); w.writerows(NODES)

# 2. provenance matrix CSV (claim -> raw owner -> formula -> theorem)
with open(os.path.join(ART,"v15_provenance_matrix.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["claim_id","frozen_source_owner","formula","proof_theorem","status"])
    for n in NODES: w.writerow([n[0],n[2],n[3],n[7],n[10]])

# 3. dependency graph JSON
deps={
 "D0-ZONE-NEUTRAL-ACTIVE-SPLIT-001":["D0-ZONE-CURRENT-001"],
 "D0-ZONE-CURRENT-001":["D0-KERNEL-ZONE-SPLIT-001"],
 "D0-FESHBACH-SCHUR-FACTORIZATION-V15":["D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001"],
 "D0-BRANCH-CP-READOUT-NOGO-V15":["D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001"],
 "D0-P1-PHYSICAL-EOS":["D0-FESHBACH-SCHUR-FACTORIZATION-V15","D0-ARCHIVE-CONTRACTION-NOGO-001"],
 "D0-ARCHIVE-REGULAR-REFINEMENT-NOGO-001":["D0-ARCHIVE-CONTRACTION-NOGO-001"],
}
with open(os.path.join(ART,"v15_dependency_graph.json"),"w",encoding="utf-8") as f:
    json.dump({"nodes":[{"id":n[0],"status":n[10],"module":n[7]} for n in NODES],
               "edges":[{"from":k,"to":v} for k,vs in deps.items() for v in vs],
               "rejected_inputs":REJECTED}, f, indent=2)

# 4. negative controls JSON
negctrl={n[0]:n[8] for n in NODES}
with open(os.path.join(ART,"v15_negative_controls.json"),"w",encoding="utf-8") as f:
    json.dump({"negative_controls":negctrl,
               "cert":"05_CERTS/vp_zone_current_spine.py (4 reachable FAIL-controls incl. naive-Euclidean-not-Hermitian)"},
              f, indent=2)

# 5. status reconciliation MD
from collections import Counter
cnt=Counter(n[10] for n in NODES)
with open(os.path.join(ART,"v15_status_reconciliation.md"),"w",encoding="utf-8") as f:
    f.write("# D0-v15 status reconciliation\n\n")
    f.write("| claim | status_before | status_after | reason |\n|---|---|---|---|\n")
    for n in NODES: f.write(f"| {n[0]} | {n[9]} | {n[10]} | {n[11]} |\n")
    f.write("\n## Counts\n\n")
    for k,v in sorted(cnt.items()): f.write(f"- {k}: {v}\n")
    f.write(f"\n## Rejected inputs (non-existent *_RESULT.md): {len(REJECTED)}\n\n")
    for r in REJECTED: f.write(f"- {r}\n")
    f.write("\n**D0 is NOT declared complete.** Two genuine present-core THE (zone-current split, "
            "Feshbach algebraic identity); the rest are proved no-gos, named conditionals, or external passports.\n")

# 6. final open joints MD
with open(os.path.join(ART,"v15_final_open_joints.md"),"w",encoding="utf-8") as f:
    f.write("# D0-v15 final open joints (genuine unresolved theory, not construction artifacts)\n\n")
    f.write("Each open joint is a NAMED missing primitive that would be required to cross a physical bridge.\n\n")
    for cid,prim in MISSING_PRIMITIVES.items():
        f.write(f"- **{prim}** — required by `{cid}`.\n")
    f.write("\nPlus: an internal nuclear-flux transfer operator (for AMS, currently passport-only).\n")
    f.write("\nNo other joint is open: present-core finite structure is machine-checked; the 8 phantom "
            "RESULT files are rejected; no physical THE is claimed beyond the zone-current split and the "
            "Feshbach algebraic identity.\n")

print(f"[OK] wrote 6 artifacts to {ART}")
for fn in sorted(os.listdir(ART)):
    if fn.startswith("v15_"): print("   ",fn)
print(f"[STATUS COUNTS] {dict(cnt)}  REJECTED={len(REJECTED)}")
