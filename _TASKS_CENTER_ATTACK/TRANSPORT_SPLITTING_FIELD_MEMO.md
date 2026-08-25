# TRANSPORT-SPLITTING-FIELD — no golden content in the FULL transport spectral closure (POST-SKEPTIC v2)

**Status:** POST-SKEPTIC v2 (2026-08-09). Skeptic #1: WOUNDED-FIXABLE, no kill; R1-R3 applied.
Pre-flight, CORRECTED per R2 (three draft grep claims were FALSE, errors of record): the disc
value 6185264 is owned at D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001 (discriminant_positive), cited
at D0-RANK3-CAUSAL-CONE-FORCING-001 AND carried at D0-TRIPARTITE-SIGNATURE-GENERAL-001 (third
owner) + 5 Lean modules (Rank3MetricSignature.lean:63-65 proves the identical integer identity;
MixingHierarchyInversion.lean:91); PRIOR IN-TREE S3 COMPUTATION EXISTS: BOOK_04:1399 asserts
'the active cubic lambda^3-359lambda-2574 has non-square discriminant 6185264, so its Galois
group is S3' and vp_hypercharge_flow_weyl_nogo.py:104-111 prints PASS_GALOIS_S3_REJECTED --
the same S3-from-nonsquare-disc inference for the same cubic (there as rejected Weyl
numerology; SUPPORTING prior, no field-membership claim anywhere); 'Galois' also appears in
Synthesis/ in Q(sqrt5)-Galois contexts (different object). The genuinely unowned content:
sqrt5/phi OUTSIDE the splitting field, the unique-quadratic-subfield step, the 5*disc
criterion, the kernel control. `splitting field` itself appears only as TransportFieldNoGolden's
own named-but-unclaimed next step (`:34`). Target: discharge that named step at owner-edge
grade.

## Claim X (DEF-0.2.2 form)

X: Let `K = ℚ(λ₁,λ₂,λ₃)` be the splitting field of the transport cubic
`x³ − 359x − 2574`. Then `√5 ∉ K`, hence `φ ∉ K` and no element of `ℚ(√5)∖ℚ` lies in `K`:
**no rational function with rational coefficients of ALL THREE transport eigenvalues jointly
produces any golden quantity.** The quantified class — rational-coefficient functions of the
transport eigenvalues — is exhausted BY CONSTRUCTION (every member lies in `K`).

Structure of the proof (owner-edge split, each leg's owner named):
1. irreducible over ℚ — **Lean-owned** (`TransportFieldNoGolden.Pcubic_irreducible`);
2. `Δ = −4(−359)³ − 27(−2574)² = 6185264 = 2⁴·193·2003`, NOT a square (mod-9 certificate:
   `Δ ≡ 5`, squares mod 9 = {0,1,4,7}) — **Lean-owned**
   (`D0.Synthesis.TransportSplittingFieldObstruction`, clean axioms, D0.All 4471 GREEN);
3. irreducible + nonsquare Δ ⇒ `Gal(K/ℚ) = S₃` ⇒ `[K:ℚ] = 6` and `K` has EXACTLY ONE
   quadratic subfield, `ℚ(√Δ)` — **external owner edge**, standard Galois theory of cubics
   (Dummit–Foote, Abstract Algebra 3e §14.6–14.7; Cox, Galois Theory ch. 7); NOT re-proved
   in Lean; the row is an owner-edge/no-go row on the D0-GAP-LABELING-OWNER-EDGE-001
   convention (external theorems cited with named sources, internal hypotheses proved);
4. `ℚ(√Δ) = ℚ(√5)` iff `5Δ` is a rational square; `5Δ` is NOT a square (mod-7 certificate:
   `5Δ ≡ 5`, squares mod 7 = {0,1,2,4}) — **Lean-owned**. Hence `√5 ∉ K`.

## Owned pre-facts (verbatim, file:line)

- `TransportFieldNoGolden.lean:32-36`: "one eigenvalue at a time (`ℚ⟮λ⟯`, not the splitting
  field with several roots — symmetric functions of SEVERAL roots are rational and out of
  scope; the splitting-field statement is a possible further step, not claimed)" — the named
  open step this campaign discharges.
- `TransportFieldNoGolden.lean:91-93`: `Pcubic_irreducible` via
  `Polynomial.irreducible_of_degree_le_three_of_not_isRoot` — irreducibility Lean-owned.
- `D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001` note: "discriminant_positive: disc = 6185264 > 0
  so three distinct real eigenvalues" — the value re-derived here from coefficients
  (`disc_from_coefficients`).
- `D0-TRANSPORT-NOT-GOLDEN-001` / `D0-TRANSPORT-FIELD-NO-GOLDEN-001` — the two prior rungs
  (bracket table; single-eigenvalue fields); this is rung three, joint closure.
- `D0-TORAL-COMPOSITION-SEVENTEEN-001` (this session): the transport factor's owned TORAL
  origin — the counterpart positive fact for the synthesis reading.
- Owner-edge convention precedent: `D0-GAP-LABELING-OWNER-EDGE-001` ("External owners (cited,
  arXiv-verified)…" — CERT-CLOSED with named external theorems + internal certificates).

## The forcing / construction (every constant computed, exact)

`05_CERTS/vp_transport_splitting_field.py` (all exact integer arithmetic): disc value from
coefficients; full-divisor irreducibility sweep; factorization 2⁴·193·2003 with primality
checks; both modular non-squareness certificates; kernel positive control
`Δ·386579 = 1546316²` (the same machinery CONFIRMS `√386579 ∈ K` — as `√Δ` always is — while
refusing `√5`); negative controls that can fail the CONCLUSION: (a) `x³−3x−1`, disc 81 = 9²
square → A₃ branch, the S₃ classification does not apply; (b) SEARCH-FOUND golden-subfield
control `x³−48x−32`: disc 414720 with squarefree kernel EXACTLY 5, `5Δ` a square — an
irreducible cubic whose splitting field genuinely CONTAINS `ℚ(√5)`; the distinction test
provably can fail, and the transport cubic sits on the other side. Mutants killed: cubic
coefficient, disc value, kernel value, mod-target. Lean: module builds standalone (2958 jobs)
and in `D0.All` (4471 GREEN); axioms propext/Classical.choice/Quot.sound on the assembly.

## Named risks & PRE-REGISTERED attack surface (strongest first)

- **ATT-A (strongest: the owner-edge grade).** The S₃/unique-subfield steps are NOT Lean.
  A skeptic can demand the row not read as a Lean closure. Defense: the row is typed
  owner-edge/no-go with the external theorem NAMED and its hypotheses (irreducibility,
  nonsquare disc) Lean-proved — exactly the D0-GAP-LABELING-OWNER-EDGE-001 convention; the
  closure contract forbids "external theorem applies" WITHOUT proving hypotheses — here both
  hypotheses are machine-checked. The row text must carry the split verbatim.
- **ATT-B (universal scope).** "No rational function of the eigenvalues" — the class is
  exhausted by construction ONLY for rational coefficients and the three cubic eigenvalues;
  ℚ(√5)-coefficient readings, other operators, and non-field constructions are untouched and
  the row must say so (same scoping that TransportFieldNoGolden survived with).
- **ATT-C (consequence inflation).** Jointly with the toral law: "on every route the φ-power
  mechanism must be toral/counting, not transport-spectral" — the universal quantifies over
  MECHANISM READINGS; scope it to: transport-spectral origins in the exhausted class are
  closed; door adjudication unchanged; (γ) not owned; the seam untouched.
- **ATT-D (arithmetic error).** All five constants independently recomputed (sympy factorint
  + hand mod checks + Lean norm_num); the mod-9/mod-7 certificates are two independent
  routes to non-squareness alongside isqrt.
- **ATT-E (duplication).** Rung 1 (bracket sign table) and rung 2 (single-eigenvalue fields)
  are cited, not absorbed; neither contains a joint-field membership statement. [CORRECTED per
  R2 — the draft's grep parenthetical here was false: 6185264 has a third registry owner
  (D0-TRIPARTITE-SIGNATURE-GENERAL-001) and 5 Lean carriers; the S3 inference itself exists in
  BOOK_04:1399 + vp_hypercharge_flow_weyl_nogo.py (supporting prior). The unowned content is
  exactly: field membership (sqrt5/phi outside K), unique-quadratic-subfield step, 5*disc
  criterion, kernel control.]

## What this does NOT show

Nothing about non-rational-coefficient readings, other operator families, or the seam; no
door adjudicated; (γ) not owned. What it closes, permanently and at maximal scope for its
class: the transport SPECTRUM — one eigenvalue or all three jointly — cannot supply the
golden content of the registered total. Combined with
`D0-TORAL-COMPOSITION-SEVENTEEN-001` (owned toral origin of both factors), the toral return
system is the only OWNED positive origin to date for the φ-power structure of obligation (i)
(negative form actually proved: no transport-spectral origin in the exhausted
rational-coefficient class; doors unadjudicated, non-rational-coefficient readings untouched).

## Repairs (errors of record, accepted in full)

- R1: the consequence sentence in the module docstring was a universal over an unexhausted
  mechanism class, contradicting its own scope limiter (kill-shape 1 in the minted artifact).
  Repaired to the negative form + door-1 rival named.
- R2: three pre-flight grep claims were false (no-Galois-anywhere; 6185264-only-two-rows;
  no-Galois-in-Synthesis). Corrected above with the named priors; the BOOK_04:1399 +
  vp_hypercharge_flow_weyl_nogo.py prior is cited as the supporting in-tree S3 computation.
- R3: row note carries the split verbatim, assembly = arithmetic legs only, the
  eigenvalue<->root docstring-grade convention pointer, and the Z->Q nonsquare bridge sentence
  (an integer that is a rational square is an integer square). Advisory adopted:
  five_not_square added (sqrt5 irrationality internally owned); 'the only owned positive
  origin to date' wording.
