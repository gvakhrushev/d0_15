# RULE-R MEMBERSHIP — the lane-G convergence point: can rep-selection + the M2 module + the owned zone=generation binding produce a MASS-BLIND particle→shell membership rule that lifts the S1 cap? (DRAFT v1)

**Status:** DRAFT candidate; no registry row edited, no cert minted, no CLAIM_TO_LEAN_MAP / LEDGER /
built .lean touched; no 053040 row touched. Companion can-fail script:
`rule_r_membership_check.py`.

**HEADLINE (stated as EXACTLY what is owned):** *The three lane-G tracks (PDG shell-membership
signal, the M2 Q₈-typed module, the frontier rep-selection primitive) all terminate on ONE and the
SAME un-owned object — a per-vertex/per-slot attachment of an owned label to a graph slot — and
that object is independently ruled out three times in the owned corpus (M2's C1 non-invariance
X4; DSIGMA "operational roles carry no intrinsic geometric attachment" BOOK_04:1399; the carrier-
count wall 2<3 "one dimension up" BOOK_04:1383). Therefore NO mass-blind particle→shell membership
rule is constructible from the owned material, the S1 cap is NOT lifted, and the bridge provably
REQUIRES the C1-forbidden graph-slot attachment. This is a sharp obstruction with a named EXACT-
MISSING object, not a fit.* The confirmed PDG membership signal (Q2, exact p=8.66e-05) is REAL and
survives; what stays un-owned is any scene-geometric DERIVATION of it (Q1), exactly as Rule-R
attempts 1–4 found — this memo upgrades that repeated underdetermination to an obstruction by
showing the missing object is the SAME object three formalisms already prove absent.

---

## 0. What is owned (verbatim, file:line — every one verified to EXIST on disk this session)

**(O1) The PDG shell-membership signal is CONFIRMED external-data, but S1-capped.**
From memory `d0-pdg-phi-lattice-test` (SHELL_MEMBERSHIP_V2_RESULTS.md, verified on disk):
- Q2 = membership-signal-confirmed: exact permutation over the full 69,300 structure-matched
  family **p = 8.66e-05 (6/69,300)**; skeptic's larger freed-excluded family (5,405,400, exact)
  **p = 4.47e-04**; LOO 13/13; mass-scramble gate PASS; LINE control p=0.246 → the signal is
  CIRCLE-specific. Verified verbatim: `SHELL_MEMBERSHIP_V2_RESULTS.md` "exact p = 8.66e-05
  (6/69,300 assignments as good or better)".
- **S1 cap (binding):** `SHELL_MEMBERSHIP_V2_RESULTS.md`: "S1 cap holds: the (n_abs, H13)
  embedding is mass-derived; Q2 confirms structure of the embedding+membership PAIR. Only a
  Q1-style owned rule lifts this to scene geometry." The embedding coordinates come from PDG
  masses; the signal is about the mass-derived embedding, not (yet) about scene geometry.
- The frozen membership (slot indices, verified in `shell_membership_v2.py:28`):
  `FROZEN = {"A": [1, 2, 3, 10, 11], "B": [4, 5, 8, 9], "C": [2, 3, 12, 13]}`.
  Particle-level (memory, computed; slot 1 = γ light node): **A={γ,b,d,e,u}, B={τ,W,c,Z},
  C={b,d,t,H}, EXCLUDED={μ,s}.** Sizes 5/4/4; A∩C={b,d}; excluded slots = 6 (μ), 7 (s).

**(O2) The M2 Q₈-typed module and its OWN non-invariance no-go.**
`M2_PHASE_LABELING_MEMO.md` (verified on disk, DRAFT v2 post-skeptic-#1):
- The owned object is a labeling of the DETECTOR-LAYER pointed shell **V₉ = Ω₈ ⊔ {ω₀}**, forced up
  to G_res, Q₈-typed. The derived module is **ℂ^{V₉} = ℂω₀ ⊕ (E₀ ⊕ E₃ ⊕ E₄), dims 1+1+3+4**
  (M2:149), with the E-system pre-owned as `D0-Q8-TERMINAL-FOURIER-001`
  (`Q8Terminal.lean:24-79`, ranks (1,4,3)).
- **X4, verbatim (M2:79-83):** "All spectral tick consumers are invariant under BOTH G_res ... and
  the full within-zone relabeling torsor S₉×S₁₁×S₁₃ ... Per-slot consumers (M2 shell-membership)
  are NOT torsor-invariant (computed negative demo) — they need the bridge, which C1 + transitivity
  forbid resolving internally."
- **M2's own membership verdict (M2:197-205), verbatim:** "M2-membership application ... NOT fed,
  twice over: (i) every owned label value is RATIONAL ... Galois-on-values stays empty; (ii) per-
  slot use ALSO needs the graph-bridge (which vertex is which slot), which is exactly the non-
  torsor-invariant datum C1 forbids owning. ... An M2 owner would need BOTH the R-strong
  adjudication AND an owned irrational value map on Q₈ ⊔ {∗} — neither exists in the corpus."
- **Zones 11/13 own nothing per-vertex (M2:70, X3):** "NOTHING owned labels vertices within V₁₁ or
  V₁₃ ... The forcing is zone-9-only."

**(O3) The lane-G rep-selection completion primitive.**
`04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVES.csv:11`, verbatim row:
`PRIM-FINITE-SPECTRAL-TRIPLE-REP, finite representation module choosing Weyl roles, path/incidence
algebra + anomaly row + K0, graph alone does not choose Weyl roles (role-carrier no-go), finite
reps compatible with anomaly + unimodularity, "anomaly-free, unimodular/K0, symmetry-compatible",
unique Weyl-role assignment, graph-flow does not force five-field row, raw graph-flow -> Weyl row, G`
Note the primitive's own STATE column: *"graph alone does not choose Weyl roles (role-carrier
no-go)"* and *"graph-flow does not force five-field row"* — it is a COMPLETION object precisely
because the graph does not supply it.

**(O4) The owned zone=generation binding.**
`BOOK_04:912` [THE 04.6.M1.gen], verbatim: "The generation index is the zone label `9/11/13` of
the minimal scene. A fermion is a boundary resonance, and the 3D projection of the scene has
exactly three boundary types: center/point `→ e`, torus/cycle `→ μ`, shell/sphere `→ τ`."
Companion: `BOOK_04:1046` [THE 04.8.L.1]: "The muon is an excitation localized in the memory zone
(the torus, address 11)."; `BOOK_04:922` [REM 04.6.M1.Λ]: "Matter (zones 9+11) and vacuum
(shell 13)".

**(O5) The owned NO-GOs that must be respected (each verified this session).**
- **R1 rep-reconstruction (GL(3) freedom):** `BOOK_04:182`: "the generation count 3 is the trivial-
  isotype multiplicity (rank-only, `GL(3)` basis freedom), so the Weyl-role assignment is unforced —
  `D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001` ... missing `PRIM-FINITE-SPECTRAL-TRIPLE-REP`".
- **Lepton-branch 2<3 (Lean-proven NO-GO):** `BOOK_04:188`: "the lepton orbit-keyed selector exists
  but `2` orbits `< 3` generations"; the NO-GO is machine-checked — "all three [injection/
  surjection/bijection] are impossible by cardinality (Lean `decide`)" (`D0.Extensions.
  LeptonBranchFixingNoGo`).
- **DSIGMA-ROLE-CYCLE (no intrinsic geometric attachment):** `BOOK_04:1399`: "`Aut(K(9,11,13)) =
  S₉×S₁₁×S₁₃` is transitive on the 1287 triangles (a single orbit), and the operational roles carry
  no intrinsic geometric attachment ... any rank-5 carrier is an arbitrary symmetry-breaking choice"
  (`D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001`, NO-GO).

---

## 1. The question, decomposed into what a CLOSURE would have to supply

A mass-blind membership rule R must be a function of type

    R : {13 core slots} → 2^{A,B,C}    (a slot may land on 0, 1, or 2 shells)

built ONLY from owned scene structure (no PDG mass enters), that (i) reproduces the frozen
membership A/B/C above, (ii) explains the {μ,s} exclusion, (iii) explains the {b,d} A∩C doubling,
and — to LIFT the S1 cap — (iv) has its OUTPUT (the shell a slot lands on) defined WITHOUT
reference to the mass-derived (n_abs, H13) embedding. Requirement (iv) is what "mass-blind" and
"about scene geometry, not the embedding" mean together.

Decompose R into the two maps any such rule must compose:

- **(a) rep→role map:** owned scene structure → a per-particle Weyl/generation role (which slot is
  which fermion/boson field). This is the lane-G / R1 object.
- **(b) role→slot / label→vertex map:** that role, or the M2 label, attached to a specific graph
  vertex or slot index in K(9,11,13). This is the M2 graph-bridge and the DSIGMA attachment.

Both (a) and (b) must exist and be MASS-BLIND for R to lift the S1 cap. The rest of the memo shows
each of (a) and (b) is an owned NO-GO, and — the new content — that (b) is literally the SAME
object in all three tracks.

---

## 2. Track-by-track: what each track supplies and where it stops (owned facts only)

**Track 1 — PDG signal (O1).** Supplies: a confirmed, circle-specific membership PATTERN, and the
three anomalies {μ,s}-exclusion, {b,d}-doubling as the exact residues (memory Rule-R attempts 1–4).
Stops at: S1 cap — the coordinates the circles are fitted in are mass-derived. The pattern is
INPUT to R, not a derivation of R. (D0-internal reading: the pattern being circle-specific does not
by itself imply a scene origin; the LINE control only rules out the line model class, not "smooth
families" generally — `SHELL_MEMBERSHIP_V2_RESULTS.md` says so verbatim: "other smooth families
untested".)

**Track 2 — M2 module (O2).** Supplies: the derived module ℂ^{V₉}=ℂω₀⊕(1+3+4) and its canonical
projectors, zone-9-only, forced up to G_res. Stops at TWO owned walls, both M2's own results:
- (2-rational) every owned label value is RATIONAL (Q₈ exponent 4; characters ±1-valued), so the
  "mass-blind per-slot ℚ(φ)\ℚ invariant" that Rule-R attempt-4's M2 named as the missing object is
  NOT supplied. (M2:198-200; consistent with the memory Rule-R attempt-4 "M2" completion piece.)
- (2-bridge) per-slot use needs the graph-bridge (which vertex is which slot), which is NOT torsor-
  invariant and which C1 forbids resolving internally (M2:82-83, X4).

**Track 3 — lane-G rep-selection primitive (O3).** Supplies: the TYPE of the completion object
("finite representation module choosing Weyl roles ... unique Weyl-role assignment"). Stops at: its
own STATE column says the graph does not choose it ("graph alone does not choose Weyl roles (role-
carrier no-go)"), and R1 (O5) proves the Weyl-role assignment is unforced (GL(3) basis freedom).
The primitive is a COMPLETION target — a name for the missing object — not a construction of it.

**Track 4 — zone=generation binding (O4).** Supplies: a 3-valued generation index = zone label
9/11/13, with center→e / torus→μ / shell→τ, and muon→zone 11. Stops at: this is a GENERATION
index (3 classes), NOT a slot→shell map (13 slots → {A,B,C} with overlap). It does not name which
of the 13 slots sits on which of the 3 circles, and — decisive friction — it puts the MUON in
zone 11 while the frozen membership EXCLUDES μ from every shell (O1). The owned typing and the
frozen pattern DISAGREE on μ. (This is `SHELL_MEMBERSHIP_V2_RESULTS.md`'s "sharpest new fact",
verified verbatim: "The owned typing puts the MUON in zone 11 (THE 04.8.L.1) — yet slot 6 (μ) is
EXCLUDED from every frozen shell.")

---

## 3. The convergence result: (b) is the SAME un-owned object in all three tracks

This is the new content. The claim is NOT that the membership is derivable, and NOT any strong
consequence — it is a narrow IDENTITY between three named-absent objects.

**(3.1 — owned, theorem-grade in each corpus location).** Each of the following is an owned NO-GO
on attaching an owned label/role to a specific graph vertex or triangle:
- M2 X4: per-slot (per-vertex) consumers are not S₉×S₁₁×S₁₃-invariant; C1 forbids owning them
  (M2:82-83).
- DSIGMA: "the operational roles carry no intrinsic geometric attachment ... any rank-5 carrier is
  an arbitrary symmetry-breaking choice" (BOOK_04:1399).
- C1 itself: "No permutation inside a part may change the physics, i.e. the adjacency matrix `A` is
  invariant under `S9 × S11 × S13`. A part-internal exception would name a privileged vertex — an
  exogenous parameter — violating M1." (BOOK_01:1570, quoted in M2:111-113.)

**(3.2 — owned, verbatim unification).** The corpus ITSELF unifies these into one wall. BOOK_04:1383
states the flow→Weyl NO-GO shares "the same carrier-count wall as the owned LEPTON-BRANCH (`2 < 3`)
and role-cycle NO-GOs, one dimension up" and "This *sharpens* the root-carrier reason of
`D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001`". So the corpus already asserts: flow→Weyl (=the
lane-G object, track 3), lepton-branch (2<3), and DSIGMA role-cycle (the attachment, track 2's
graph-bridge analogue) are ONE wall.

**(3.3 — the reading, marked as a D0-INTERNAL READING, not a new theorem).** Rule-R's map (b)
role→slot is an instance of exactly this wall: it would attach a per-particle role (a Weyl role, or
an M2 Q₈-label) to a specific graph slot of K(9,11,13). By (3.1)+(3.2) every such attachment is
either non-invariant under the vacuum symmetry (⇒ C1-forbidden, names a privileged vertex) or an
arbitrary symmetry-breaking choice (⇒ not owned). **Reading:** therefore R's map (b) cannot be
owned, and since R = (b)∘(a) needs (b), R cannot be constructed mass-blind from owned structure.
*This step is a reading — it applies three separately-proven no-gos to the Rule-R object by
recognizing Rule-R's (b) as the same type. It is NOT itself machine-checked. It could fail only if
Rule-R's (b) were somehow NOT a per-vertex/per-slot attachment — but requirement (iv) of §1 (output
= a specific circle per slot, mass-blind) forces it to be exactly that. The script §5 pins this: any
mass-blind rule whose output is per-slot is non-invariant under S₉×S₁₁×S₁₃ unless it is zone-
constant, and a zone-constant rule collapses to ≤3 output values — too coarse to produce the
5/4/4 overlapping pattern with A∩C={b,d}.*

**(3.4 — the S1 cap is NOT lifted, owned consequence).** Because (b) is not owned, the only
coordinates in which the frozen circles are defined remain the mass-derived (n_abs, H13) embedding
(O1). No mass-blind output map replaces them. Hence the S1 cap stands: the confirmed signal remains
about the mass-derived embedding+membership pair, not about scene geometry. (This is the same
verdict `SHELL_MEMBERSHIP_V2_RESULTS.md` records — "Only a Q1-style owned rule lifts this to scene
geometry" — now with the reason PINNED to the specific missing object.)

---

## 4. Verdict and the EXACT-MISSING object

**Verdict: HONEST OBSTRUCTION (sharper than underdetermination).** The bridge provably REQUIRES the
C1-forbidden graph-slot attachment. Rule-R attempts 1–4 ended in underdetermination "we could not
find a rule"; this memo names WHY: the rule factors through a per-vertex/per-slot attachment that
is a proven NO-GO in three independent owned formalisms, which the corpus itself unifies into one
carrier-count wall (BOOK_04:1383). The default expectation (sharp underdetermination) is met and
tightened to an obstruction.

**EXACT-MISSING object (the single un-owned datum a CLOSURE would need):**

> **MISS-R = a mass-blind, S₉×S₁₁×S₁₃-EQUIVARIANT (hence C1-respecting) map from owned per-particle
> role/label data to the 13 core graph slots, whose image is the frozen A/B/C overlapping partition.**

MISS-R is un-owned and, in its C1-respecting form, cannot exist by (3.1)–(3.3): equivariance forces
zone-constancy (≤3 values), which cannot encode a 13→{A,B,C}-with-overlap map distinguishing μ,s
(excluded) from e,u,d,... within the SAME zone. Its non-equivariant form is C1-forbidden. So MISS-R
is not merely absent — it is over-constrained. A future owner would have to break the tie between
"mass-blind + C1-respecting" and "fine enough to be per-slot", i.e. supply an owned WITHIN-ZONE
distinguishing datum on the 33 vertices — the SAME object M2 X3 proves absent for zones 11/13, and
the same object Rule-R attempt-4's memory note "M2" (a within-zone irrational labeling) named as
the recurring missing piece. All three roads meet here.

**Compare to the two adjacent named objects (owned):** MISS-R is the per-slot MEMBERSHIP analogue of
`PRIM-FINITE-SPECTRAL-TRIPLE-REP`'s "unique Weyl-role assignment" (O3) and of M2's needed "R-strong
adjudication + owned irrational value map on Q₈⊔{∗}" (O2). It is NOT a new primitive; it is the
membership-shadow of the existing lane-G frontier object, now with the extra requirement (iv) that
makes its C1-obstruction explicit.

---

## 5. What this does NOT show (guard against the session's over-claim failure mode)

- Does NOT falsify the PDG signal: Q2 stands (p=8.66e-05), circle-specific. The obstruction is on
  DERIVING it from scene geometry, not on the signal's existence.
- Does NOT prove "membership is underivable by ANY owner": the obstruction is on OWNED/scene-
  internal construction (C1-respecting, mass-blind). A terminal-passport owner (e.g. an external
  Weyl-role table, an octonion/E₈ colour route) is not addressed — the S1 cap and the passport lanes
  stay exactly where they were. (This mirrors M2's own scope note M2:270: "no-go ... only that no
  internal/owned datum exists (passport route stays open).")
- Does NOT adjudicate M2's G_res reading; the argument is made under the LARGEST freedom so it is
  reading-independent (even R-strong's rational-valued labeling fails requirement (2-rational)).
- Does NOT claim MISS-R is the ONLY conceivable completion shape — it is the one all four owned
  tracks converge on; a genuinely different owned route (not through per-slot attachment) is not
  logically excluded, only unlocated in the corpus. (Marked: this is a scope honesty note, not a
  proof of uniqueness.)
- Does NOT LEAP from "attachment non-invariant" to "¬(membership rule exists in any framework)".
  The load-bearing inference (3.3) is a D0-internal READING applying three owned no-gos to a fourth
  object recognized as the same type; it is explicitly flagged as not machine-checked.
- Respects the three named no-gos: it USES R1 (GL(3)), lepton-branch (2<3), DSIGMA (no attachment)
  as owned inputs and adds no claim that contradicts them.

## 6. Pre-registered attack surface (strongest self-attacks first)

- **A1 (strongest): is Rule-R's map (b) really the DSIGMA/C1 object, or a coarser one that dodges
  it?** If a mass-blind rule could output shells using only ZONE-level (not vertex-level) data, it
  would be C1-safe. Counter (script CTRL_ZONE_CONSTANT_TOO_COARSE): a zone-constant rule has ≤3
  distinct outputs and cannot separate μ (excluded) from e,u (in A) — all three are in the same
  matter zones, and μ is owned to zone 11 alongside... the pattern needs WITHIN-zone resolution,
  which is exactly the forbidden datum. If a future owner exhibits a zone-level rule reproducing
  5/4/4+overlap, this memo's obstruction is REFUTED — that is the falsifier.
- **A2: does the confirmed circle-specificity secretly carry scene content that IS mass-blind?**
  The circles are fitted in mass-derived coordinates (S1). Counter: until the coordinates
  themselves are re-derived mass-blind, no scene claim follows; and no owned object re-derives them
  (Q1 negative). Falsifier: an owned, mass-blind coordinate map on the 13 slots.
- **A3: BOOK_04:1383's "one wall" unification is about flow→Weyl, not about MEMBERSHIP.** True —
  (3.2) is owned only for flow→Weyl/lepton/role-cycle; the extension to Rule-R's (b) is the reading
  (3.3), flagged as such. If (b) is provably NOT of carrier-attachment type, (3.3) fails. The
  script's non-invariance demo is the computational backstop for (3.3), not a substitute for a Lean
  proof.
- **A4: G_res R-strong loophole.** Under R-strong the M2 labeling exists and is unique — could its
  (rational) values still separate the 13 slots after the graph-bridge? No: even granting R-strong,
  (2-bridge) still needs the C1-forbidden vertex→slot map; R-strong removes the labeling ambiguity,
  not the attachment. (M2:204: "would need BOTH the R-strong adjudication AND an owned irrational
  value map ... neither exists".)
- **A5: model-completeness of the owned sweep.** The obstruction is only as strong as the claim
  that no owned within-zone per-vertex datum exists (M2 X3 for 11/13; C1 for 9). A missed owned
  per-vertex datum reopens everything (same hook as M2's CTRL_ZONE11_NO_BASEPOINT).

## 7. Registry proposal (PROPOSAL ONLY — no file edited)

Proposed frontier-register note (NOT written to any CSV/LEDGER/.lean; for a human to adjudicate):

- **MISS-R** (§4) is the per-slot MEMBERSHIP shadow of `PRIM-FINITE-SPECTRAL-TRIPLE-REP` (lane G),
  carrying the extra requirement (iv) mass-blind output. Suggested status: **NO-GO (obstruction)**
  under the C1-respecting + mass-blind conjunction, DERIVED here by reading (3.3) from the owned
  trio {M2-X4, DSIGMA-ROLE-CYCLE, carrier-count wall BOOK_04:1383}; PROOF-TARGET if a Lean lift of
  (3.3) is wanted (the lift would formalize "per-slot mass-blind ⇒ non-zone-constant ⇒ C1-violating
  OR arbitrary").
- Cross-reference (do NOT duplicate): `D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001` (R1),
  `D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001` (2<3, Lean),
  `D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001`, `D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`
  (flow→Weyl), and the M2 memo.
- NO change to any S1/Q1/Q2 status; NO CLAIM_TO_LEAN_MAP / LEDGER / built-.lean edit; NO 053040 row
  touched.

## 8. Verification

`rule_r_membership_check.py` — can-fail script. Each control can FAIL the CONCLUSION:
- `CTRL_FROZEN_SLOTS_MATCH` — frozen A/B/C slot sets match `shell_membership_v2.py:28` exactly
  (guards the O1 pattern against drift).
- `CTRL_PERSLOT_NOT_INVARIANT` — a per-slot membership indicator is NOT invariant under a random
  S₉×S₁₁×S₁₃ relabeling of the 33 vertices (reproduces M2 X4's negative demo for the membership
  consumer specifically); FAILS if per-slot membership were secretly torsor-invariant.
- `CTRL_ZONE_CONSTANT_TOO_COARSE` — any zone-constant (C1-respecting) rule yields ≤3 distinct
  outputs and provably cannot reproduce the 5/4/4-with-A∩C={b,d} pattern (μ,s excluded while
  same-zone e,u,d are placed); FALSIFIER for A1.
- `CTRL_MU_TYPING_CONFLICT` — the owned typing (μ→zone 11, THE 04.8.L.1) and the frozen membership
  (μ excluded) disagree on μ; FAILS if they were reconcilable by an owned zone→shell bijection.
- `CTRL_LABELS_RATIONAL` — M2's owned label values are rational (Q₈ exponent 4); FAILS if an owned
  irrational per-slot value existed (guards requirement (2-rational)).
- `CTRL_MISS_R_EXISTS_WOULD_REFUTE` — a POSITIVE control: constructs a mass-USING per-slot rule that
  DOES reproduce membership, to confirm the obstruction is specifically about MASS-BLINDNESS +
  C1, not about the pattern being unreachable in principle.


