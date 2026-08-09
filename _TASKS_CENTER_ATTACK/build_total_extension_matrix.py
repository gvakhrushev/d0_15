#!/usr/bin/env python3
"""build_total_extension_matrix - deterministic generator for the N-parametric
total-extension-primitive independence adjudication (2026-08-09 campaign).

Reads:  04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVES.csv  (catalog; row order = matrix order)
Writes: 04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_INDEPENDENCE_MATRIX.csv   (NxN typed cells)
        04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_DERIVE_EDGES.csv          (registered derive-relation)
        04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_PAIR_JUSTIFICATIONS.csv   (all C(N,2) pairs, one verdict + justification each)

The derive-relation and the per-pair justifications are DATA here (single source
of truth); the cert 05_CERTS/vp_total_extension_primitive_minimality.py re-verifies
the emitted files independently and does NOT trust this generator.
"""
import csv, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CAT = ROOT / "04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVES.csv"

# short handles
SH  = "PRIM-SCENE-HISTORY-REFINEMENT-RULE"
XI  = "PRIM-COMPARISON-MAP-XI-N"
DS  = "PRIM-DIRAC-SCALE-SELECTION"
MAG = "PRIM-PHYSICAL-MAGNITUDE-MAP"
RED = "PRIM-PHYSICAL-REDSHIFT-OBSERVABLE"
SMW = "PRIM-FORCED-SMOOTHING-WINDOW"
LEP = "PRIM-LEPTON-BRANCH-FIXING-OPERATOR"
PER = "PRIM-PERRON-PHI3-CARRIER"
NCT = "PRIM-NONCOMMUTING-TRIPLE"
FST = "PRIM-FINITE-SPECTRAL-TRIPLE-REP"
BAR = "PRIM-BARYON-PHYSICAL-LABEL-TRANSFER"
BIR = "PRIM-BRANCH-ISOTROPIC-READOUT"
CSF = "PRIM-CANONICAL-SELF-READING-FUNCTOR"
EHS = "PRIM-EDGE-HOLONOMY-SELECTOR"
EFT = "PRIM-EFT-IR-MATCHING-FUNCTIONAL"
GNC = "PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR"
IDJ = "PRIM-ISOMETRIC-DIRAC-J"
PCF = "PRIM-PHASON-COORDINATE-FUNCTOR"
PPE = "PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT"
SCT = "PRIM-SEAM-CROSSING-TICK-IDENTIFICATION"

# carrier / moduli typing used to justify default 'independent' verdicts.
CARRIER = {
    SH:  ("K(9,11,13) history tower (E2 frontier)", "admissible refinement functors (all-walks vs non-backtracking)"),
    XI:  ("vNext refinement-tower endpoints", "tripartite-preserving conditional expectations C_n"),
    DS:  ("vNext intrinsic scale cocycles", "covariance-compatible scale cocycles (phi-scale vs 2-scale)"),
    MAG: ("external w_DE magnitude passport (lane B)", "Galois-sign/positivity-preserving magnitude maps"),
    RED: ("external redshift passport: internal s -> physical z (P2-E)", "frozen monotone redshift observables"),
    SMW: ("scene Laplacian heat data on spectrum {20,22,24,33}", "(k,u) smoothing/evaluation functionals"),
    LEP: ("C4xR3 resolvent Puiseux branches on the 7-pt shell torus (E4 frontier)", "mass-independent coefficient sections"),
    PER: ("profinite Dixmier/Wodzicki carrier for alpha mu_2 (lane E)", "phi^3 Perron carriers"),
    NCT: ("Higgs isolated spectral cluster + Riesz projector (period-44 flow)", "frozen noncommuting triples (U,Q0,Pi_H)"),
    FST: ("33-scene path/incidence-algebra representation, full (rho,Gamma,J,Q_role) interface (E1 frontier)", "anomaly/K0-compatible finite reps"),
    BAR: ("40/56 baryon carriers + compressed poles", "physical label transfers"),
    BIR: ("v15 WP-B 3-block branch-coupling commutant", "marginal-preserving coherence assignments"),
    CSF: ("BUNDLE: S0 (owned) + the 4 self-reading frontiers E1-E4", "would-be single subsuming functor"),
    EHS: ("unified-edge-spine return edge, U(1) lambda-family", "holonomy PHASE selectors on |lambda|=1"),
    EFT: ("lepton exponent lattice, Vandermonde {0,1/4,1/3}", "(r_mu,r_tau) IR-matching functionals"),
    GNC: ("derived M3 generation block of the R1 commutant (Wedderburn)", "Z2-grading operators of signature (p,q)"),
    IDJ: ("BUNDLE: vNext Perron-GNS isometric tower Dirac completion", "finite Dirac J with real structure"),
    PCF: ("phason archive internal coordinate cocycle z(s) (X5 contract scope)", "tick cocycles (phi-tick vs integer-tick)"),
    PPE: ("L_archive spectrum {24,22,20} vs S_DE window (P1-C)", "pressure/energy role sections"),
    SCT: ("door-2 seam carrier V11 u {*} + toral tick (02.13.h depth axis)", "crossing<->tick identifications (alpha,beta,gamma)"),
}

# Registered derive-relation (the ONLY non-independent off-diagonal content).
# Every edge is owned by an already-registered claim; nothing minted here.
EDGES = [
    (CSF, FST, "D0-SELF-READING-PRIMITIVE-MINIMALITY-001",
     "conjunction leg E1: the would-be single functor forces the finite spectral-triple rep (registry note: 'it is S0 (owned) + 4 semantically-independent primitives')"),
    (CSF, SH,  "D0-SELF-READING-PRIMITIVE-MINIMALITY-001",
     "conjunction leg E2: forces the scene-history refinement rule"),
    (CSF, PPE, "D0-SELF-READING-PRIMITIVE-MINIMALITY-001",
     "conjunction leg E3 (role factor): forces the phason pressure/energy role assignment"),
    (CSF, PCF, "D0-SELF-READING-PRIMITIVE-MINIMALITY-001",
     "conjunction leg E3 (cocycle factor): forces the phason coordinate functor"),
    (CSF, LEP, "D0-SELF-READING-PRIMITIVE-MINIMALITY-001",
     "conjunction leg E4: forces the lepton branch-fixing operator"),
    (CSF, GNC, "D0-SELF-READING-PRIMITIVE-MINIMALITY-001 + D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001",
     "transitive: E1 leg supplies the full (rho,Gamma,J,Q_role) interface, whose Gamma restricts to the M3 grading operator"),
    (IDJ, DS,  "D0-VNEXT-ISOMETRIC-DIRAC-TOWER-NOGO-001",
     "vNext split: 'a Dirac-compatible tower requires ... a forced scale law (Outcome C)'; a Dirac completion carries its scale"),
    (IDJ, XI,  "D0-VNEXT-ISOMETRIC-DIRAC-TOWER-NOGO-001",
     "vNext split: 'requires ... a canonical comparison map Xi_N (Outcome D)'; the NOGO says the single primitive splits into +2"),
    (FST, GNC, "D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001 + D0-GRADING-NEUTRAL-CURRENT-MAXIMALITY-NOGO-001",
     "GRADAXIS component: the E1 completion interface (rho,Gamma,J,Q_role) contains the grading operator whose M3 restriction is exactly this PRIM's datum; converse fails (a grading does not give the rep)"),
]

# Rows excluded from the pairwise-independent core, with reasons.
CORE_EXCLUDED = {
    CSF: "proven conjunction-of-independent (bundle), D0-SELF-READING-PRIMITIVE-MINIMALITY-001 (LEAN_PROVED)",
    IDJ: "NOGO-split bundle, D0-VNEXT-ISOMETRIC-DIRAC-TOWER-NOGO-001 ('splits into +2 independent primitives')",
    GNC: "subsumed component of the E1 interface (D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001 + D0-GRADING-NEUTRAL-CURRENT-MAXIMALITY-NOGO-001 GRADAXIS split keeps the row as the sharper G2-typed object)",
}

# Hand-written justifications for the trap-sensitive independent pairs
# (shared word / shared number / same lane / construction edges).
OVERRIDES = {
    frozenset({SH, XI}): "construction dependence only (Xi is built on a refinement tower) - not a derive-edge: two refinement rules give two Xi (witness), and Xi supplies no refinement rule; original 11x11 adjudication upheld",
    frozenset({XI, DS}): "the vNext NOGO itself registers these as the two INDEPENDENT split pieces ('+2 independent primitives'); scale cocycle supplies no comparison map and conversely",
    frozenset({PPE, PCF}): "Lean-owned construction edge P1->P2 (D0.Extensions.FivePrimitiveSemanticDependence: the coordinate functor's construction requires a pressure-energy sector) - explicitly 'no merge, asymmetric dependence, not equivalence'; neither DERIVES the other, both must be independently supplied",
    frozenset({RED, PCF}): "internal-vs-external firewall: PCF is the internal tick cocycle (X5 contract: z(s)=phi^s-1, deletion-minimality phi-tick vs integer-tick); RED is the external passport datum (P2-E: 'no internal coordinate = observed redshift', EXACT-MISSING = external redshift observable). An internal cocycle does not identify itself with observed redshift; a passport does not select the internal normalization freedom (the X5 freedom is registered ON TOP of the passport layer)",
    frozenset({RED, PPE}): "role section vs external redshift passport: disjoint moduli (pressure/energy split vs observable identification); P1-C and P2-E are separate registered no-gos",
    frozenset({MAG, PPE}): "shared constraint words (Galois sign + positivity) but distinct data: |w_DE| magnitude map vs pressure/energy role section; magnitude no-go and P1-C are separate no-gos; a magnitude assigns no roles, a role fixes no magnitude",
    frozenset({MAG, PCF}): "magnitude vs coordinate: |w_DE| map vs tick cocycle; the phason no-go keeps 'physical map = external passport' separate from the internal 4-torsor moduli",
    frozenset({MAG, RED}): "original 11x11 adjudication: magnitude passport vs redshift passport, distinct external data",
    frozenset({SMW, PPE}): "shared NUMBERS {20,22,24} (scene Laplacian spectrum vs L_archive) - carrier-mismatch-by-shared-number checked: smoothing lives on scene heat data incl. 33, the role section on L_archive-vs-S_DE incommensurability (359/160); P1-C says there is no common sector, so neither datum transfers",
    frozenset({SMW, PCF}): "shared number family {20,22,24} checked: (k,u) smoothing functional vs tick cocycle; five-primitive witness 'a refinement carrier supplies no archive coordinate' pattern - no common sector, no derivation",
    frozenset({LEP, BIR}): "shared word 'branch' checked: Puiseux branches of the C4xR3 lepton resolvent (7-pt shell torus) vs the v15 WP-B 3-block branch-coupling commutant - disjoint carriers (five-primitive witness pattern 'disjoint carriers; fixing a grading leaves the branch row free' analog); coherence assignment fixes no coefficient section and conversely",
    frozenset({LEP, EFT}): "both lane D lepton: separator = LEP's registered 'mass-independent' necessary condition vs EFT's mass-ratio selection; the Vandermonde det=1/144!=0 keeps (r_mu,r_tau) free after any coefficient section, and a ratio pair selects no section",
    frozenset({PER, SCT}): "both alpha-line lane E: Dixmier mu_2 carrier realization vs door-2 crossing/tick identification - distinct moduli (a carrier with phi^3 Perron eigenvalue vs the (alpha)(beta)(gamma) conjunction); the identification uses no Dixmier structure, the carrier fixes no tick reading",
    frozenset({EHS, SCT}): "shared words edge/seam/alpha checked: U(1) holonomy PHASE on the return edge (injective separator z^3-coeff=-lambda) vs crossing<->tick identification on V11 u {*} - moduli U(1) vs a finite conjunction; a phase choice identifies no crossing with a tick, the identification selects no lambda",
    frozenset({EHS, PER}): "alpha-line adjacency checked: edge-cover phase vs Dixmier carrier - disjoint moduli and owners (D0-EDGE-COVER-FAMILY-001 vs alpha maximality no-go)",
    frozenset({FST, NCT}): "shared word 'triple' checked (original 11x11 pair): finite rep module on the 33-scene vs frozen Higgs (U,Q0,Pi_H) on the isolated cluster - original adjudication upheld",
    frozenset({BIR, GNC}): "block-structure words checked: WP-B 3-block branch-coupling commutant vs R1 Wedderburn M3 block - different commutants; coherence moduli vs grading involutions",
    frozenset({BIR, BAR}): "readout coherence vs physical labels: distinct moduli on distinct carriers (branch commutant vs 40/56 carriers)",
    frozenset({FST, IDJ}): "shared symbol 'J' checked: the finite rep's real structure lives on the 33-scene E1 interface; IDJ's J on the vNext profinite GNS tower; bundle row IDJ has NO registered edge to FST (the vNext split lands on XI/DS, not on E1)",
    frozenset({SMW, SH}): "original 11x11 adjudication; refinement covariance is a CONSTRAINT on smoothing, not a derivation (H-does-not-force pattern)",
    frozenset({PCF, SCT}): "shared word 'tick' AND shared golden value checked (X5 tick z(1)=phi-1 vs per-crossing ratio phi^-1): X5 internal ARCHIVE cocycle tick vs door-2 SEAM crossing/toral tick - different carriers (phason archive vs 02.13.h seam depth axis); the value coincidence is guarded by D0-SEAM-CROSSING-WEIGHT-001's own clause (forced_value_is_toral_stable_root is a coincidence-of-values record, not an explanation claim); a tick normalization identifies no crossing, an identification fixes no archive cocycle",
    frozenset({DS, PCF}): "shared word 'cocycle' + phi-vs-rival-normalization shape checked: vNext intrinsic SCALE cocycle on the refinement tower vs phason archive TICK cocycle - different carriers and owners (vNext joint no-go vs phason_extension_nogo/X5); neither cocycle choice determines the other",
}

BUNDLE_NOTE = {
    CSF: "bundle row (conjunction-of-independent); partner is NOT among its registered constituents {E1,E2,E3-role,E3-cocycle,E4,+transitive GNC}: constituent carriers are disjoint from the partner's carrier, and the partner's datum forces no conjunction leg",
    IDJ: "bundle row (vNext NOGO split); partner is NOT among its registered split pieces {XI,DS}: the tower Dirac completion neither supplies nor needs the partner's datum",
}


def main() -> int:
    P = list(csv.DictReader(CAT.open(encoding="utf-8", newline="")))
    ids = [p["primitive_id"] for p in P]
    N = len(ids)
    assert set(CARRIER) == set(ids), f"carrier typing out of sync: {set(CARRIER) ^ set(ids)}"
    edge_set = {(a, b) for a, b, *_ in EDGES}
    # transitive closure must already be registered
    for a, b in list(edge_set):
        for c, d in list(edge_set):
            if b == c:
                assert (a, d) in edge_set, f"missing transitive edge {a}->{d}"
    # matrix
    idx = {p: i for i, p in enumerate(ids)}
    cells = [["independent"] * N for _ in range(N)]
    for i in range(N):
        cells[i][i] = "self"
    for a, b, *_ in EDGES:
        cells[idx[a]][idx[b]] = "subsumes"
        cells[idx[b]][idx[a]] = "component-of"
    with (ROOT / "04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_INDEPENDENCE_MATRIX.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["primitive"] + ids)
        for i, p in enumerate(ids):
            w.writerow([p] + cells[i])
    # derive-edge ledger
    with (ROOT / "04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_DERIVE_EDGES.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["src", "dst", "relation", "owner_claims", "justification"])
        for a, b, own, j in EDGES:
            w.writerow([a, b, "subsumes", own, j])
        w.writerow([])
        w.writerow(["# core_excluded", "reason", "", "", ""])
        for p, r in CORE_EXCLUDED.items():
            w.writerow([p, r, "", "", ""])
    # pair justifications (all C(N,2))
    with (ROOT / "04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_PAIR_JUSTIFICATIONS.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["a", "b", "verdict", "justification"])
        orig11 = set(ids[:11])
        for i in range(N):
            for j in range(i + 1, N):
                a, b = ids[i], ids[j]
                key = frozenset({a, b})
                if (a, b) in edge_set or (b, a) in edge_set:
                    s, d = (a, b) if (a, b) in edge_set else (b, a)
                    own, jtext = next((o, t) for x, y, o, t in EDGES if (x, y) == (s, d))
                    w.writerow([a, b, f"derive-edge {s}->{d}", f"[{own}] {jtext}"])
                    continue
                if key in OVERRIDES:
                    w.writerow([a, b, "independent", OVERRIDES[key]])
                    continue
                if a in BUNDLE_NOTE or b in BUNDLE_NOTE:
                    bn = a if a in BUNDLE_NOTE else b
                    w.writerow([a, b, "independent", BUNDLE_NOTE[bn]])
                    continue
                if a in orig11 and b in orig11:
                    w.writerow([a, b, "independent",
                                "original 11x11 adjudication (Lean total_extension_primitive_independence; distinct signatures, empty derive-relation)"])
                    continue
                ca, ma = CARRIER[a]
                cb, mb = CARRIER[b]
                if SCT in (a, b):
                    other = b if a == SCT else a
                    w.writerow([a, b, "independent",
                                f"distinct carriers ({ca} vs {cb}) and distinct moduli ({ma} vs {mb}); {other} is the registered completion gap of its own owner, while SEAM-CROSSING-TICK is the registered RESIDUAL of a core obligation (D0-TRANSPORT-FORK-ENDGAME-001 / D0-SEAM-CROSSING-WEIGHT-001), door-2-conditional - refutation reopens the depth axis, no no-go; neither completion datum determines the other"])
                    continue
                w.writerow([a, b, "independent",
                            f"distinct carriers ({ca} vs {cb}) and distinct moduli ({ma} vs {mb}); each is the registered completion gap of a different owner (no-go or obligation row); neither completion datum determines the other"])
    core = [p for p in ids if p not in CORE_EXCLUDED]
    for a, b, *_ in EDGES:
        assert not (a in core and b in core), f"edge inside core: {a}->{b}"
    print(f"N={N} edges={len(EDGES)} core={len(core)} pairs={N*(N-1)//2}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
