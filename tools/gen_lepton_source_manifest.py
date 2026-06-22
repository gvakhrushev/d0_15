#!/usr/bin/env python3
"""gen_lepton_source_manifest.py - emit D0_LEPTON_SOURCE_MANIFEST.json (§1): literal repo paths + sha256
for every source object in the v16 lepton chain, with status + source-native/§0 flags from the audit."""
import json, os, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = "09_LEAN_FORMALIZATION/D0"

# module -> (claim_id, status, role, source_native, note)
OWNERS = {
 f"{LEAN}/Core/DyadABCD.lean": ("D0-ABCD-001","CORE-FORMALIZED","carrier: Role=4, Omega8=8 (source-native type defs)", True, "foundational labelling; supplies the 8-point Omega8 carrier"),
 f"{LEAN}/Claims/VietaGaloisAbcd.lean": ("D0-VIETA-GALOIS-ABCD-001","CORE-FORMALIZED","ABCD = Vieta/Galois data of x^2-x-1", True, "Galois-conjugation swap template (branch pairing)"),
 f"{LEAN}/Claims/Q8DedekindMinimality.lean": ("D0-Q8-DEDEKIND-MINIMALITY-001","CERT-CLOSED","Q8 forced as the role group (Hamiltonian, triple Z2 identity)", False, "S0 CAVEAT: carrier is hand-built FinGrp tables; cite as finite-catalog cert, not source-extracted"),
 f"{LEAN}/Matter/LeptonFiniteGreenResolventOwner.lean": ("D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001","CERT-CLOSED","finite Green resolvent (Ueff^12=1, G(0)=I)", False, "S0 CAVEAT: Ueff is a hand-typed 7x7 literal proved at z=0; det=(1-z^4)(1-z^3) is prose. Positive resolvent half only."),
 f"{LEAN}/Matter/LeptonGreenPuiseuxOwner.lean": ("D0-LEPTON-GREEN-PUISEUX-OPERATOR-001","CERT-CLOSED","(0,1/4,1/3) exponent-row operator scaffold", False, "exponent-row scaffold; cite"),
 f"{LEAN}/Matter/LeptonPuiseuxUniquenessObstruction.lean": ("D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001","NO-GO","many-to-one index->operator obstruction", False, "branch index many-to-one; cite"),
 f"{LEAN}/Matter/LeptonRiemannHurwitzBranchIndex.lean": ("D0-LEPTON-RIEMANN-HURWITZ-BRANCH-INDEX-001","CERT-CLOSED","ramification/genus-0 + non-uniqueness", False, "Puiseux ramification; cite"),
 f"{LEAN}/Matter/LeptonBranchAssignmentNoGo.lean": ("D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001","NO-GO","two-completion no-go: sigmaA/sigmaB order 12, distinct", False, "THE necessity witness; load-bearing negative theorem; cite, do NOT re-mint"),
 f"{LEAN}/Extensions/LeptonSelectorExtension.lean": ("D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001","NO-GO","terminal L4: 2 orbits < 3 generations", False, "cite"),
 f"{LEAN}/Extensions/LeptonBranchSelectorConstruction.lean": ("D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001","PROOF-TARGET","orbit-keyed selector 1/4!=1/3 (intrinsic)", False, "names PRIM-LEPTON-BRANCH-FIXING-OPERATOR; cite"),
 f"{LEAN}/Evolution/FeshbachSchurTimeDelayOwner.lean": ("D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001","CERT-CLOSED","tick / Feshbach-Schur time delay", False, "tick step; cite"),
 f"{LEAN}/LeptonClosure/BranchRowMinimalExtension.lean": ("D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001","NEW","v16 increment: B_row necessity+sufficiency+minimality", True, "source-native permutation combinatorics; NO hand-built matrices"),
}

def sha(path):
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full): return None
    return hashlib.sha256(open(full,"rb").read()).hexdigest()[:16]

manifest = {
 "task": "D0-v16 source-native lepton Green closure",
 "decision": "OUTCOME-B: source proves exact two-completion no-go + names one minimal operator (PRIM-LEPTON-BRANCH-FIXING-OPERATOR = B_row); no source-native unique Green+row map (Outcome A excluded).",
 "carrier_distinction": "Omega8 (8 role points) != C^{V9} (vertices) != C^{E(K)} (359 edges) != H_N (shell stages) != 7-point shell-torus monodromy carrier. No morphism assumed without an explicit code-level map.",
 "objects": [],
 "s0_caveats": [],
}
for path,(cid,status,role,native,note) in OWNERS.items():
    h = sha(path)
    rec = {"path": path, "exists": h is not None, "sha256_16": h, "claim_id": cid,
           "status": status, "role": role, "source_native": native, "note": note}
    manifest["objects"].append(rec)
    if not native and "CAVEAT" in note:
        manifest["s0_caveats"].append({"path": path, "caveat": note})

out = os.path.join(ROOT, "D0_LEPTON_SOURCE_MANIFEST.json")
json.dump(manifest, open(out,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"[OK] wrote {out}")
print(f"  objects: {len(manifest['objects'])}, missing: {sum(1 for o in manifest['objects'] if not o['exists'])}, S0 caveats: {len(manifest['s0_caveats'])}")
