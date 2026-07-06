# W2 — QUANTITY IDENTIFICATION for cluster J (T1 "Obstruction=Equation") — v2, post-skeptic (repairs applied)

**Status:** candidate, skeptic #1 pass complete — SURVIVES (WOUNDED-minor on R1, repaired; §7).
No registry row edited, no book touched. Nothing containing 053040 touched.
**Targets:** R1, R2, R3, R5, E1, E2 (per `UPLIFT_MAP.md` cluster J; A2 pilot handled elsewhere; R4/E3/E4 skipped as torsor/sweep-frontier).
**Pre-flight run:** `preflight.sh 718 "718/33" 15708 14990 REPRESENTATION-RECONSTRUCTION ARCHIVE-CONTRACTION SCENE-NATIVE-MULTISCALE-TOWER ALPHA-LOG-CESARO POSTCORE-REPRESENTATION-EXTENSION POSTCORE-HISTORY-REFINEMENT` — all six rows located (registry lines 460/461/462/464/468/469), plus cross-refs: REHEATING rows 381/383/384, vNext2 rows 437/439, H3 row 490, W1 Ihara–Bass cert.
**Danger ledgers read first:** `ALPHA_SEAM_NOGO_V2.md` (α-front CLOSED, eight-pass-hardened — R5 here retypes the limit constant ONLY, no seam claim), `TICK_COUPLING_SCHUR_MEMO.md` (R2/Feshbach scopes honest; L_archive ≠ QUQ respected throughout).
**Verification:** `_TASKS_CENTER_ATTACK/w2_quantity_ident_check.py` (v2, incl. the R1 multiplicativity bridge) — RESULT: PASS; 7/7 mutation tests fire (each targeted wrong input fails its check's CONCLUSION). Runtime ~15 s, stdlib only, exact int/Fraction decisions (floats only in the R5 convergence illustration).

---

## 0. Claim under test (DEF-0.2.2 form, per target)

Each cluster-J no-go COMPUTES a specific nonzero quantity. The T1 uplift claim is: *that quantity
IS an owned-typed object* — an identification with named type and structural provenance, not a
dimension/number coincidence (word-dressing gate applied per target below).

---

## 1. Owned pre-facts (verbatim, file:line)

**P1 — R1 row (registry line 460), `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:460`:**
> "Aut(K(9,11,13))=S9xS11x S13 perm rep on C^33: isotypes (mult 3,1,1,1; dims 1,8,10,12), carrier 33, commutant dim Sum m^2 = 3^2+1+1+1 = 12. The generation count 3 = trivial-isotype multiplicity is RANK-ONLY: commutant block 9>1 (GL(3) basis freedom) => Weyl-role assignment unforced"
(quoted with spacing normalized; original has "S9xS11xS13").

**P2 — generation ownership, same CSV, D0-MATTER-REP-001 (CORE-FORMALIZED):**
> "Matter generation multiplicity is exactly three."

**P3 — typed collapse, D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001 (NO-GO):**
> "(A) TYPED COLLAPSE - D_zone=diag(24,22,20) simple spectrum reduces the raw M3(C) on the three zone-lines (dim 9) to the abelian diagonal (dim 3), so three zones = GENERATIONS not colour"

**P4 — E1 type statement, `09_LEAN_FORMALIZATION/D0/Extensions/RepresentationReadoutExtension.lean:20-22`:**
> "/-- Neutral-current channel count for a grading signature `(p,q)` on the 3-dim generation block:
> `dim` of the grading-even commutant `= p² + q² + 3` (the `+3` = the three multiplicity-1 standard blocks). -/
> def ncCount (p q : ℕ) : ℕ := p * p + q * q + 3"
NOTE: the Lean *proves* only the arithmetic (`nc_signature_21 : ncCount 2 1 = 8` etc., lines 27–32); the
"dim of the grading-even commutant" reading lives in the docstring. The W2 script COMPUTES it (§3.E1).

**P5 — R2 Lean scope, `09_LEAN_FORMALIZATION/D0/Cosmology/ArchiveContractionCriterion.lean:14-18`:**
> "the only concretely-realized archive operator (`L_archive`, radius 24) cannot host it without an external rescale (by `2|E| = 718`, a count = forbidden). This does NOT prove `QUQ` itself is non-contractive"
And the cert control, `05_CERTS/vp_root_r2_archive_contraction.py:21`:
> "print('FAIL_EXTERNAL_RESCALE_REJECTED  rescaling the archive block by 2|E|=718 (a count) to force contraction is caught.')"

**P6 — R3 Lean scope, `09_LEAN_FORMALIZATION/D0/Spectral/SceneNativeMultiscaleTower.lean:8-10`:**
> "the all-ones Rayleigh quotient gives `ρ(A) ≥ 2|E|/N = 718/33 ≈ 21.76`, while `φ³ = 2φ + 1 < 5`"

**P7 — REHEATING owner (registry line 383, D0-INFLATIONLESS-THRESHOLD-ENERGY-OWNER-001, CERT-CLOSED):**
> "forced early limit spectralWeightSum/totalMultiplicity=718/33"
and its cert `05_CERTS/vp_inflationless_threshold_energy_owner.py:15`: `SPEC = {0: 1, 20: 12, 22: 10, 24: 8, 33: 2}` — this is the K(9,11,13) **Laplacian spectrum** (verified independently, §3.CAP).

**P8 — E2 row (registry line 469):**
> "all-walks 15708 != non-backtracking 14990 (diff 2|E|=718) => refinement functor not unique"
Counts owned by D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001 (line 439: "First disagreement: depth-2 carrier count (15708 vs 14990)") and H3 (line 490).

**P9 — the backtracking bijection ALREADY cert-verified, `_TASKS_CENTER_ATTACK/vp_scene_ihara_bass_nb.py:9` (docstring) and 168-178 (check [2]):**
> "[2] depth-2 identity: Σd²=15708, Σd(d−1)=14990, excess=718=2|E|, excess ↔ directed edges (bijection)."
> "`backtracks = sum(1 for (a, b) in dedges ... )` ... `PASS_DEPTH2_BACKTRACK_BIJECTION`"
**Provenance flag (RESOLVED 2026-07-06):** the file's own docstring says "NOT placed in 05_CERTS/ (must not enter the CI cert glob)" and `TASK_W1_REPORT.md:3-4` says the same. A byte-identical copy had leaked into `05_CERTS/vp_scene_ihara_bass_nb.py` (unreferenced by any registry row, grep clean), where `run_registered_certs.py --orphans` would have swept it into the CI glob against that stated design intent; the copy has been removed. The canonical cert lives at `_TASKS_CENTER_ATTACK/vp_scene_ihara_bass_nb.py`. W2 cites it as in-tree verification, not as a registered owner.

**P10 — R5 Lean, `09_LEAN_FORMALIZATION/D0/Spectral/AlphaLogCesaroMeasurability.lean:8-11`:**
> "At the critical rate `a = 3` the per-block mass is constant (`φ³·φ^{-3} = 1`, `rate_three_eq_one` of the alpha maximality no-go), so the ordinary log-Cesàro (Dixmier) limit of the singular values is `... = 1/(3·log φ)`."

**P11 — critical-rate ownership, D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001 (registry):**
> "rate(3)=1 exactly (critical 1/j line) <=> carrier Perron eigenvalue phi^3, which 5-fold symmetry + M1 forbid (single golden rate phi)"

**P12 — I_f ownership (both MECH-LIMIT-flavored, cited as such):**
D0-FIBONACCI-IF-FORCING-001 (CERT-CLOSED): "[Iter7 cross-bridge, self-calibrated MECH-LIMIT NOT forcing] I_f=log phi reached two independent ways";
D0-IF-KS-FORMULA-FIX-001 (CORE-FORMALIZED): "the toral automorphism spectral radius |lambda_max|=|-phi|=phi ... The KS-entropy identification h_KS=log|lambda_max| (Pesin/Margulis-Ruelle) and the log-phi~0.4812 numeric are the external/monotone wrapper."

---

## 2. The unified capacity clause (computed, then stated ONCE)

All quantities below were rebuilt in `w2_quantity_ident_check.py` from the zone sizes (9,11,13)
alone; no corpus constant enters its own construction (pins compare at the end).

**CAP (candidate clause, feeds P-CAPACITY).** On the frozen scene K(9,11,13) there is ONE
capacity quantity, the total edge capacity
**C := Σ_v deg(v) = 2|E| = Tr L_scene = #(directed edges) = 718**,
whose computed faces are exactly the cluster-J obstruction constants:

| face | exact identity (verified) | where it appears |
|---|---|---|
| handshake | Σ_v deg(v) = 718 = 2·359 | definition |
| spectral | Tr L = Σ_λ λ·mult(λ) over {0¹,20¹²,22¹⁰,24⁸,33²} = 718 | REHEATING's spectralWeightSum (P7) |
| carrier-dimension | #(directed edges) = 718 = dim of the non-backtracking (Hashimoto) edge space | W1 Ihara–Bass cert (P9) |
| combinatorial | #(backtracking depth-2 walks) = 718, in BIJECTION (a,b,a) ↔ (a,b) with directed edges | E2's family gap (P8, P9) |
| density | C/N = 718/33 = mean degree = mean Laplacian eigenvalue | R3 Perron floor (P6) = REHEATING threshold (P7) |
| normalization | deg_z/C = {12/359, 11/359, 10/359}, all < 1, Σ_v deg_v/C = 1 | R2's forbidden rescale (P5) |

R2, R3, E2 (and REHEATING, already sharing R3's number in the registry) are **corollary
instances of CAP**: the same count in its trace, dimension, walk, density and normalization
faces. The identities Tr L = Σdeg = 2|E| and gap = 2|E| are theorem-grade (handshake;
backtracking bijection — verified on the scene AND on 4 unrelated control graphs, so the
identity is structural while the VALUE 718 is scene-specific: mutation K(9,11,15) moves all
faces together).

**REQUIRED clause for any future P-CAPACITY mint (skeptic #1, carried verbatim):** *"the
identity is structural while the VALUE 718 is scene-specific"* — a P-CAPACITY roster entry may
claim only that the obstruction constant is a face of the scene's capacity count; it may NOT
claim that the identity gap=2|E| (or Tr L=Σdeg) is itself D0-specific content. The pilot face
belongs to the same roster: div G_A2 = 4·deg (G_A2_EINSTEIN_MEMO.md §3 — the per-vertex
capacity as Bianchi-failure), so the roster reads: R2 rescale (total-capacity normalization),
R3 ≡ REHEATING density 718/33, E2 gap (backtracking face), A2 pilot divergence (per-vertex
face).

---

## 3. Per-target identification (computed, exact)

### R1 — D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001 → **IDENTIFIED-OWNED**

**Identification.** The commutant (dim 12) is not merely "12 = 9+1+1+1": the script computes,
independently (pair-orbit BFS under generated S9×S11×S13, closure under multiplication,
structure map):
- commutant dim = #(orbits on ordered pairs) = 12; closed as an ALGEBRA (all 144 basis products
  orbit-constant);
- the structure map X ↦ (π_gen(X), c₉(X), c₁₁(X), c₁₃(X)) is an exact algebra isomorphism onto
  **M₃(ℚ-span) ⊕ ℂ ⊕ ℂ ⊕ ℂ** (rank 12 = 9+1+1+1, π_gen surjective onto M₃: rank 9);
- **multiplicativity bridge (skeptic #1 repair, applied):** the structure map is checked to be
  an ALGEBRA homomorphism directly — coords(BᵢBⱼ) = coords(Bᵢ)·coords(Bⱼ) on all 12² basis
  pairs (π_gen multiplicative as 3×3 matrices, std scalars multiplicative per zone). This holds
  automatically because the generation span and the std blocks are invariant subspaces
  (restriction to an invariant subspace is an algebra map), but it is now COMPUTED, so
  rank 12 + multiplicativity = algebra isomorphism, not merely a linear one;
- the M₃ factor acts on **span{1₉, 1₁₁, 1₁₃}** — the trivial-isotype multiplicity space, which is
  the OWNED generation space (P1: "generation count 3 = trivial-isotype multiplicity";
  P2: "Matter generation multiplicity is exactly three").

**Owned type:** the commutant IS **End(generation space) ⊕ (one scalar per within-zone standard
block)** — the *flavor-frame algebra* of the generation space; its unit group GL(3) is the frame
freedom the no-go names, and the S₃ Weyl-role freedom is its permutation part. (Deliberately NOT
"bundle": there is no base space; "frame algebra + frame torsor" is the honest wording.)

**Typed-collapse consistency (self-attack executed):** the degree operator D ∈ commutant and its
centralizer inside the commutant has dim 6 (= 3 diagonal on M₃ + 3 scalars) — exactly P3's typed
collapse dim 9 → dim 3 on the generation block. So the GL(3) frame freedom coexists with, and is
cut to the zone-diagonal by, the owned degree typing; no contradiction with the COLOUR no-go.

**Word-dressing gate:** passed by computation — the claim verified is the algebra structure AND
its action (which space the M₃ acts on), not the dimension sum. Mutation: on K(9,9,13) with the
extra swap automorphism the orbit count drops to 7 and M₃-fullness FAILS (rank < 9) — the
conclusion is carried by the distinct zone sizes, and the check can fail it.

### E1 — D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001 → **IDENTIFIED-OWNED** (form); T3 residue intact

**Identification.** nc(p,q) = p²+q²+3 IS the **dimension of the graded commutant**: the
centralizer, inside the R1 commutant, of a grading involution acting with signature (p,q) on the
generation space. Computed exactly for all four signatures: dims {12, 8, 8, 12} = p²+q²+3,
**axis-independent** (all placements of the −1 give the same dim — the S₃-symmetry the row
claims). Equivalently: nc = Σ mᵢ² over the Γ-refined isotypes — the SAME Σm² commutant-dimension
form as R1, refined by the grading (3² → p²+q²). This answers UPLIFT_MAP sweep-frontier item (c)4:
**owned quadratic-form invariant on the M₃ block (full T1), not a bare count** — the Lean
docstring (P4) already states this type; W2 upgrades it from docstring to computed fact.

**Controls:** a non-involution element (π_gen = diag(1,2,3)) has centralizer dim 6 ∉ {8,12} — the
formula is signature-specific, not generic; wrong formula p²+q²+2 rejected by the computed dim.
**T3 residue unchanged:** nothing here selects between (2,1) and (3,0) — the two-completion
freedom (and the E1 no-go itself) stands.

### R2 — D0-ARCHIVE-CONTRACTION-NOGO-001 → **IDENTIFIED-OWNED** (quantity typed; firewall intact)

**Identification.** The obstruction is a capacity-vs-threshold statement in CAP faces:
spec(L_archive) = spec(L|ker A) = zone degrees {24,22,20} (verified: all 30 spanning within-zone
differences are exact eigenvectors, dim ker A = 30) — the archive block carries **absolute
per-vertex capacity weights**, all > 1. The rescale the no-go names is division by C = 718: the
rescaled spectrum {12/359, 11/359, 10/359} is the **per-vertex capacity share deg/C** (which sums
to 1 over vertices — the normalization face of CAP). So "718" in R2 is not an ad-hoc number: it
is the total-capacity normalizer, the same owned count as E2's gap and R3's numerator.

**Honesty (two firewalls kept):** (i) the cert's own negative control REJECTS using the rescale
(P5) — the T1 uplift types the quantity, it does NOT legalize the move; the obstruction reading
becomes: *the frozen core owns the absolute-capacity operator but does not own the
capacity-share normalization; supplying it is an external import (P-M1-FIREWALL)*. (ii) The
operator-type firewall stands: L_archive ≠ QUQ ≠ S_DE (P5, and TICK_COUPLING_SCHUR_MEMO —
ρ(QUQ) scoping honest; nothing here touches the Feshbach residual or the S_DE/w-leg).
**Non-minimality named (self-attack):** any constant > 24 would rescale below 1; 718 is not the
minimal witness but the only CANONICAL count of capacity type in the frozen inventory — the
identification claim is about the TYPE of the named rescale, not about minimality.

### R3 — D0-SCENE-NATIVE-MULTISCALE-TOWER-NOGO-001 → **IDENTIFIED-OWNED** (corollary of CAP)

**Identification.** The Perron floor 718/33 IS the **capacity density C/N = mean degree = mean
Laplacian eigenvalue** — verified exactly: the all-ones Rayleigh quotient equals C/N; the
comparison to φ³ is done exactly in ℚ(√5): (C/N − 2)² = 425104/1089 > 5 ⟺ C/N > φ³ = 2φ+1
(no floats). The obstruction = **capacity density vs golden rate gap**: every inherited-adjacency
carrier inherits the scene's capacity density, which sits far above the golden-critical rate φ³.
**Unification with REHEATING (UPLIFT_MAP top-10 item 3) — CONFIRMED EXACT:** REHEATING's
"spectralWeightSum/totalMultiplicity = 718/33" (P7) is Tr L / N; R3's floor is Σdeg/N; these are
THE SAME quantity by the trace identity Tr L = Σdeg (computed both ways from the independently
rebuilt spectrum {0¹,20¹²,22¹⁰,24⁸,33²}). One quantity, two independent theorems (Rayleigh floor;
threshold energy) — corollary instances of CAP's density face. R3's SCOPE-REPAIR (inherited-
adjacency class only) is untouched.

### R5 — D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001 → **IDENTIFIED-OWNED** (retype), reading leg **CONDITIONAL(MECH-LIMIT)**

**α-seam discipline (read first, ALPHA_SEAM_NOGO_V2.md):** the α-realization front is CLOSED at
the eight-pass-hardened NO-GO v2.1. This uplift makes **no seam claim, no μ₂-realization claim,
touches no seam object**; it retypes the computed limit constant only. The script's "seam guard"
line is a decorative RESTATEMENT of the row-464 conclusion (limit ≠ μ₂), relabeled as such per
skeptic #1 — not presented as a new check. None of the four reopening hooks is invoked.

**Identification (two layers, honest split):**
1. **Unconditional/owned:** 1/(3 ln φ) = **1/ln(φ³)** — the reciprocal log of the *critical
   Perron rate φ³* that the owned maximality row itself names (P11: "rate(3)=1 exactly ...
   carrier Perron eigenvalue phi^3"). Reading: at the critical line the tower's singular values
   are equidistributed in log-scale with period ln(φ³); the ordinary log-Cesàro limit is the
   **log-scale spectral density 1/ln(φ³)** of the critical golden tower. Convergence verified
   numerically (illustration); the identification tracks ln(rate), not the number — a base-2
   mutant tower converges to 1/(3 ln 2), and the subcritical a=2 tower to 0 (both controls fire).
2. **Conditional reading:** with the owned I_f = ln φ (P12), the constant reads **1/(3·I_f)** —
   "one state per 3 bits-of-φ", the golden information rate reading. BOTH I_f owners are
   self-labeled MECH-LIMIT / external-wrapper rows, so this leg is
   IDENTIFIED-CONDITIONAL(reading: I_f identification is MECH-LIMIT, not forcing) — it may be
   cited as interpretation, not as core typing.

The no-go's inequality then retypes as: **log-density (transcendental, conditional on
ASSUMP-LINDEMANN-LNPHI as already registered) ≠ rational moment μ₂** — a P-TYPED transcendence-
fingerprint instance. The registered conditionality is unchanged.

### E2 — D0-POSTCORE-HISTORY-REFINEMENT-MAXIMALITY-NOGO-001 → **IDENTIFIED-OWNED** (strongest of the six)

**Identification + structural provenance (the load-bearing question: is 718 emergent or
routed?).** ROUTED, theorem-grade: the two carrier counts are the first two capacity moments —
all-walks depth-2 = Σ deg² = 15708 (verified by direct 33³ enumeration, not by the formula),
non-backtracking = Σ deg(deg−1) = 14990 — so the family gap is **Σ deg = C exactly**, and
combinatorially the excess walks are in **explicit bijection (a,b,a) ↦ (a,b) with the directed
edges** (enumerated and matched, not counted-and-compared). The gap IS the backtracking-capacity
term: the all-walks family differs from the non-backtracking family by exactly one returning walk
per edge-end. Not a coincidence: the identity gap = 2|E| holds for EVERY graph (verified on P5,
C6, K1,4, K4), while the value 718 is scene-specific (K(9,11,15) mutation moves it to 766 with
all CAP faces moving together). Wrong identification gap = |E| is rejected by a firing control.
**Cross-reference (§05.8.U):** the bijection is already in-tree in `vp_scene_ihara_bass_nb.py`
check [2] (P9) — W2 independently reproduces it by enumeration and CITES it; no duplication. The
Hashimoto/NB edge space of that same cert has dimension 718 = C: the E2 gap equals the dimension
of the very carrier that separates the two families — the dimension face of CAP.
**Scope kept:** the E2 no-go (refinement functor not unique) is untouched; the uplift types its
computed gap, it does not pick a family.

---

## 4. Verdict table

| # | claim_id | computed quantity | owned type (citation) | verdict |
|---|---|---|---|---|
| R1 | D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001 | commutant dim 12 | flavor-frame algebra End(generation space) ⊕ ℂ³; generation space = trivial-isotype span (P1, P2); typed collapse consistent (P3) | **IDENTIFIED-OWNED** |
| R2 | D0-ARCHIVE-CONTRACTION-NOGO-001 | rescale 718 | CAP normalization face: total capacity; rescaled spectrum = capacity shares deg/C (P5); use stays firewalled | **IDENTIFIED-OWNED** (corollary of CAP) |
| R3 | D0-SCENE-NATIVE-MULTISCALE-TOWER-NOGO-001 | Perron floor 718/33 | CAP density face: mean degree = mean Laplacian eigenvalue; = REHEATING threshold exactly (P6, P7) | **IDENTIFIED-OWNED** (corollary of CAP) |
| R5 | D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001 | limit 1/(3 ln φ) | = 1/ln(φ³), log-scale density at the owned critical Perron rate (P10, P11); I_f-reading conditional (P12) | **IDENTIFIED-OWNED** (retype); 1/(3·I_f) leg **IDENTIFIED-CONDITIONAL(MECH-LIMIT reading)** |
| E1 | D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001 | nc = p²+q²+3 ∈ {8,12} | graded-commutant dimension (Σm² form refined by signature) on the R1 commutant (P4); T3 two-completion residue intact | **IDENTIFIED-OWNED** (form) |
| E2 | D0-POSTCORE-HISTORY-REFINEMENT-MAXIMALITY-NOGO-001 | gap 15708−14990 = 718 | CAP combinatorial face: backtracking-capacity term, bijection with directed edges (P8, P9) | **IDENTIFIED-OWNED** |

**Unified clause:** CAP (§2) survives computation; R2 + R3 + E2 (+ REHEATING, already sharing
R3's number in the registry) are corollary instances → feeds **P-CAPACITY** with the six-face
table as its computed roster entry. R1 + E1 feed **P-R1-COMMUTANT** (E1 = the graded refinement
of the same Σm² form).

---

## 5. Named risks & PRE-REGISTERED attack surface (strongest self-attacks included)

- **A1 (word-dressing, strongest against CAP):** "Σdeg = Tr L = 2|E| is high-school graph theory;
  calling it 'THE capacity coupling' may be renaming, not physics." Pre-registered defense: the
  T1 rubric (UPLIFT_MAP) asks precisely for *what the computed quantity IS, owned-typed*; the
  pilot (div G_A2 = 4·deg) was validated on the same shape. The non-trivial content is the
  CROSS-THEOREM identity: three independently-derived obstruction constants (R2 rescale, R3/REH
  ratio, E2 gap) are faces of one count. Skeptic must decide: is "one quantity, six faces"
  physics or bookkeeping? LEAP-test both directions explicitly.
- **A2 (R2 non-minimality):** any c > 24 witnesses contraction; the no-go's "718" could be read
  as one choice among many, making "718 IS the coupling" over-typed. Defense: P5's Lean text
  itself names 2|E| (not "some constant") as THE rescale; the identification types the NAMED
  quantity. If the skeptic finds a second owned count of equal standing (e.g. 33, 359, 24) that
  the corpus names as the R2 rescale, the identification is wounded.
- **A3 (R5 seam-adjacency):** any reading of "golden information rate" that implies a route to α
  reopens the closed seam. Defense: two-layer split (§3.R5); the conditional leg is explicitly
  MECH-LIMIT-labeled; the script's row-464 restatement (decorative) + "what this does NOT
  show" below.
- **A4 (E1 docstring-vs-proof gap):** the Lean proves arithmetic only; the "graded commutant"
  reading was docstring-level. W2's computation closes exactly this gap — but if the skeptic
  finds a DIFFERENT owned derivation of nc (e.g. a gauge-boson count route) that does NOT factor
  through the centralizer, the "IS" claim splits into two readings.
- **A5 (R1 'bundle' language):** UPLIFT_MAP says "flavor-frame bundle"; there is no base space.
  This memo deliberately downgrades to "frame algebra + GL(3) frame freedom". If a referee wants
  the bundle picture, the honest object is the frame TORSOR of the generation space.
- **A6 (unregistered cert copy) — RESOLVED 2026-07-06:** P9's provenance flag — a byte-identical
  `vp_scene_ihara_bass_nb.py` copy sat in 05_CERTS against its own docstring, unregistered, where
  the `run_registered_certs.py --orphans` cert glob would pick it up; the copy has been removed
  (canonical cert remains in `_TASKS_CENTER_ATTACK/`). W2 depends on it only as cross-reference;
  the independent enumeration carries the load, so nothing load-bearing changes.

## 6. What this does NOT show

- Does NOT legalize the R2 rescale, select a refinement family (E2), select a grading signature
  (E1), select a Weyl-role assignment (R1), or open any route to φ³/μ₂/α (R3/R5): every no-go's
  own conclusion stands unchanged; the uplift types the computed constants.
- Does NOT touch the α-seam (CLOSED, v2.1) or the Feshbach/QUQ scoping.
- Does NOT mint P-CAPACITY or P-R1-COMMUTANT — it supplies their computed roster entries;
  minting goes through VERIFIED_CLOSURE_PROTOCOL.md separately.
- Does NOT edit any registry row or book.

## 7. Skeptic verdict — RECORDED (independent agent, §05.8.R kill-mandate)

**Overall: SURVIVES; WOUNDED-minor on R1 only; zero citation errors found** (all verbatim
quotes verified on disk by the skeptic; script re-run by the skeptic: PASS, all mutations fire).

Per-target: R1 WOUNDED-minor (linear-vs-algebra isomorphism gap in the structure-map argument —
required repair: the direct multiplicativity check); R2 SURVIVES; R3 SURVIVES; R5 SURVIVES
(with the seam-guard relabel); E1 SURVIVES; E2 SURVIVES; CAP clause SURVIVES with the REQUIRED
scene-specificity clause carried into any future mint (§2).

**Repairs applied in full (no defense):**
1. R1 multiplicativity bridge added to `w2_quantity_ident_check.py` (coords(BᵢBⱼ) =
   coords(Bᵢ)·coords(Bⱼ), all 12² pairs, exact) + invariant-subspace note in §3.R1 —
   re-run PASS. R1 verdict after repair: **IDENTIFIED-OWNED**.
2. Script seam-guard relabeled as restatement of the row-464 conclusion (decorative).
3. §2 wording: "already registry-unified" → "already sharing R3's number in the registry".
4. §2 REQUIRED clause for any future P-CAPACITY mint (scene-specificity concession verbatim)
   + the A2 pilot face added to the roster text.
5. P9/A6 hygiene flag (unregistered `05_CERTS/vp_scene_ihara_bass_nb.py` copy) RESOLVED 2026-07-06
   by removing the copy (canonical cert remains in `_TASKS_CENTER_ATTACK/`); W2 never depended on
   the copy for any load-bearing claim.

## 8. Proposed registry motions (PROPOSALS ONLY — no CSV edit performed here; source-of-truth
flow per D0-REGISTRY rules: edit CLAIM_TO_LEAN_MAP.csv + regenerate, never the generated files)

Notes-only cross-reference additions (no status changes, no new rows):
- R1 row 460: append "T1-UPLIFT (W2): commutant = flavor-frame algebra End(generation space) ⊕
  ℂ³; computed algebra iso + typed-collapse consistency in
  _TASKS_CENTER_ATTACK/w2_quantity_ident_check.py; feeds P-R1-COMMUTANT."
- E1 row 468: append "T1-UPLIFT (W2): nc = graded-commutant dimension (Σm² form refined by
  signature), computed for all 4 signatures; Lean docstring type now computed; T3 two-completion
  residue unchanged."
- R2 row 461 / R3 row 462 / E2 row 469: append "T1-UPLIFT (W2): obstruction constant = face of
  the capacity count C = 2|E| = Tr L = 718 (normalization / density / backtracking face resp.);
  corollary instance of proposed P-CAPACITY; REQUIRED clause: identity structural, value
  scene-specific; R3 face ≡ REHEATING threshold (rows 383/384) exactly."
- R5 row 464: append "T1-UPLIFT (W2): limit retyped 1/(3 ln φ) = 1/ln(φ³) (log-density at the
  owned critical Perron rate, cf. ALPHA-PRESENT-CORE); 1/(3·I_f) reading conditional
  (MECH-LIMIT I_f rows); no α-seam claim; conditionality unchanged."
- P-CAPACITY / P-R1-COMMUTANT minting: separate motions via VERIFIED_CLOSURE_PROTOCOL.md,
  outside W2's scope; this memo supplies the computed roster entries only.
