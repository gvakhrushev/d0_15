# D0 Lean formalization audit (Iter-18) — status & what needs formalizing

Method: a 12-agent read-only census of all **1212** theorems/lemmas across `09_LEAN_FORMALIZATION/D0`
(318 files, 30 subdirectories) + a pass over the 19-row assumption ledger, each theorem classified by
*goal substance × proof shape*, cross-referenced to its registered claim. Two authoritative
cross-checks were run against the agent buckets: a direct grep for real proof holes, and `d0_score`.

---

## 1. Headline

- **Proof holes (`sorry` / `admit` / `axiom`): 0.** The authoritative grep finds only the English word
  "admit" in two prose comments (`…would admit the S₃ zone-swap`), never the Lean tactic; `d0_score`
  proof-debt = 0. The census's "8 SORRY_ADMIT_AXIOM" are all false positives — structural
  `:= { … }` instance constructors and one real `norm_num` arithmetic proof, none are holes.
- **No claim is registered LEAN_PROVED on a `: True` stub** after the Iter-18 sweep (Higgs proved
  for real; 8 claims repointed; the `check_no_tautology_proofs` guard now fails on new vacuous-True
  stubs, ratchet = 12 accepted markers).

| bucket (census) | count | honest reading |
|---|---:|---|
| LOAD_BEARING | 855 | genuine proofs (ring/linarith/induction/calc + multi-step) |
| WEAK_DEFINITIONAL | 302 | **mixed** — see §2: most are finite-decidable certs (load-bearing); the rest are shallow wrappers |
| VACUOUS | 32 | `: True` / `Prop := True` / `noGo : True` markers — assert nothing |
| SORRY_ADMIT_AXIOM | 8 | **0 real** (mislabeled structural constructors / one `norm_num`) |

---

## 2. Classification caveat — `native_decide` on a concrete finite object IS load-bearing

The census agents put **many `native_decide` / `decide` / `norm_num` proofs of concrete finite facts**
into WEAK_DEFINITIONAL (e.g. `e8_gram_unimodular` = native_decide on the concrete 8×8 determinant;
`q8_center_pm1`; `window44_unit_count` on `ZMod 44`; `ckm_row_sums_one` on the concrete 3×3 matrix;
`pisot_discriminant_eq_five`; the `D0-SPIN2-001` / `D0-SIGNATURE-31-SPLIT-001` matrix theorems). This
is **too harsh**: a kernel-checked `native_decide` of a concrete finite arithmetic/group/matrix fact
is a real, unfudgeable proof of *that finite instance* — and finite-decidable certs are precisely the
D0 proof style. What it does **not** do is prove the *abstract* generalization; where the claim needs
the abstract step, that step is already an explicit external-owner edge (e.g. the specific E8 Gram is
even-unimodular by `native_decide` = CORE; "this lattice **is** E8" = `ASSUMP-MORDELL-E8`). So those
theorems are **load-bearing for the finite instance, conditional-on-owner for the abstract claim** —
honest, not a gap.

Re-reading the 157 "non-load-bearing backing a CORE/LEAN_PROVED claim" with this lens: **~100 are
finite-decidable certs** (load-bearing instance proofs) and only **~50 are genuinely shallow** (§4).

---

## 3. Three honest tiers

- **Tier 1 — genuine internal proofs + finite-decidable certs (the solid core).** ~855 load-bearing
  + ~100 native_decide/decide/norm_num concrete-fact certs. Machine-checked; cannot be fudged. This
  is the bulk of the corpus.
- **Tier 2 — finite instance proved internally, abstract step owned by an external theorem
  (honest BRIDGE).** The 13 legitimate `ASSUMP-*` edges (§5) + their finite D0-side certs. Disclosed,
  not gaps.
- **Tier 3 — genuinely shallow (the real cleanup/formalization list, §4).** ~32 vacuous markers +
  ~structural-definition/struct-projection/well-typed wrappers. Mostly NOT a claim's sole support
  (each CORE claim typically also carries real certs); they are shallow *helpers/summaries*, but a
  few are a claim's only Lean content and warrant a real theorem or an honest status note.

---

## 4. Genuinely-shallow set (Tier 3) — grouped

1. **Vacuous markers (32).** `: True` theorem stubs (12, guarded + grandfathered), plus
   `def P : Prop := True` / `noGo : True` structure fields and `DefinesProfiniteObject := True`:
   - `D0-ARCHIVE-PHASE-CURVATURE`: `NO_GO_PHASE_LAPLACIAN_PROJECTIVE_COMPATIBILITY`,
     `NO_GO_PHASE_CURVATURE_OBSTRUCTION` — NO-GO markers (structural assertion only).
   - `D0-ARCHIVE-TOWER-001`: `archive_tower_defines_profinite_object : True` — needs a real
     definition of "finite inverse system defines a profinite limit".
   - `D0-LEAN-CORE-001` `release_m1_claims_present`, `D0-TRACEABILITY-…` guardrail — infra reflexivity.
2. **Structural `:= { … }` instance constructors (~18).** `D0-GRAVITY-ENTROPIC-ARCHIVE-001` (9
   definitions: GraphLaplacian, HeatTraceObservable, ArchiveFlux, … + the closure package),
   `D0-GRAVITY-MACRO-EINSTEIN-INTERFACE-001` (5), `D0-CONDENSED-PHI-VACUUM-CUT-PROJECT-001` (4). These
   *build* the object; they do not *prove* a property of it. Either prove a property (e.g. the flux is
   conserved — `ConservedArchiveFlux` should be a theorem, not a def) or mark the module as structural.
3. **Struct-field projection / "package coherence" wrappers (12).** `D0-INTERPRETATION-SPINE-001` —
   all 12 theorems are field projections / definitional unfolds of the interpretation package
   ("keeps core dimensionless", "single SI readout", …). Real content would relate the package to the
   actual core invariants, not just project its fields.
4. **`*_well_typed` existence stubs + `rfl`-unfolds + pure-composition wrappers.** e.g. `D0-FOUND-001`
   `delta_half_gap` (def unfold, should derive δ₀ as a quadratic root); `D0-HULL-001` (5 property
   assertions — FLC / aperiodicity / long-range-order stated, not derived from the tiling rule);
   the `*_well_typed` `⟨f, rfl⟩` existence lemmas and `…_closure := composition` wrappers throughout.

---

## 5. Assumption ledger (19 `ASSUMP-*`)

**13 LEGITIMATE_EXTERNAL_OWNER** — real classical theorems genuinely absent from Mathlib / external,
honestly cited as bridges (leave as-is):
`HURWITZ-GOLDEN, JONES-INDEX, MORDELL-E8, CONNES-RECONSTRUCTION, TOMITA-TAKESAKI, COMPLEX-QM,
M1-INFO-RECONSTRUCTION, VERLINDE-ENTROPIC, FROBENIUS-1877, WILSON-LATTICE-1974, DIXMIER-TRACE,
RIEFFEL-GHP, ADLER-WEISS`.

**6 QUESTIONABLE_SHOULD_BE_INTERNAL** — re-examine whether genuinely external or a dischargeable
assumption:
| ASSUMP | issue | action |
|---|---|---|
| `ASSUMP-COMPACT-LIE-KILLING-NEGATIVE` | **[Iter-18 corrected]** Mathlib has the Killing form + non-degeneracy but **NOT** Cartan's compactness criterion (compact ⟺ Killing neg-semidef) — so it is a *legitimate external owner* (Cartan), not internally-dischargeable. D0's operative Yang-Mills positivity is already internal (`skew_square_trace_nonpositive`). | reclassified LEGITIMATE; ledger cites Cartan + the internal operative proof |
| `ASSUMP-HST-EXTERNAL` | the external theorem itself is **unclear** ("HST" — hyperbolic systems? Holley–Stroock–Tibrewala?) | **identify or rename** the owner precisely, else it is a hidden assumption, not an owner-edge |
| `ASSUMP-RG-SMOOTH-INTERP` | continuous-RG smooth interpolation | likely genuinely external (continuum limit) — keep, but state the residual sharply |
| `ASSUMP-LORENTZ-MACRO` | finite-Clifford → macro Lorentz integration | continuum/macro limit — keep as external, align with the Rieffel/GHP + Connes continuum owners |
| `ASSUMP-SMOOTH-COVARIANCE` | smooth metric covariance/nondegeneracy | continuum limit — keep external (companion to Connes reconstruction) |
| `ASSUMP-SMOOTH-HEATTRACE` | heat-trace convergence / Weyl asymptotics | continuum limit — keep external (spectral geometry) |

Net: 4 of the 6 are continuum/smooth-limit owners (genuinely external, same family as Connes/Rieffel —
keep, sharpen the residual wording); **2 are real flags** — `ASSUMP-COMPACT-LIE-KILLING-NEGATIVE`
(internally provable) and `ASSUMP-HST-EXTERNAL` (owner unidentified).

---

## 6. Formalization roadmap (ranked; feasible + valuable first)

**A. High value, finite/decidable, clearly feasible:**
1. `D0-ARCHIVE-TOWER-001` — replace `archive_tower_defines_profinite_object : True` with a real
   profinite-limit statement; prove `capacity_shell_stable_from_four` (induction, decidable base) and
   `spectral_modes_strictly_increase` ((n+2)⁴>(n+1)⁴ monotonicity) as real lemmas (currently weak).
2. `D0-PHASE-UNFOLD-002` / `D0-WINDOW44-GROUP-SPECTRUM-001` — promote the totient facts (φ(44)=20,
   φ(710)=280) from `native_decide`-on-instance to the stated arithmetic theorems (already decidable;
   make the abstract statement explicit so the claim is self-contained).
3. `D0-GEN-INDEX-001` — the defect-action order-3 / generation count: prove the cyclic action and the
   count from the structure (currently 9 weak/def-action lemmas), not just state them.
4. `D0-OMEGA8-CENTER-001` — extend the exhaustive `center_eq_pm1` to the full collapse (order +
   non-centrality) as one theorem.

**B. Structural packages — prove a property or mark structural (don't leave as `:= {…}`):**
5. `D0-GRAVITY-ENTROPIC-ARCHIVE-001` — make `ConservedArchiveFlux` an actual conservation *theorem*
   (the flux sums to zero), not a definition; same for the macro-Einstein interface witnesses.
6. `D0-CONDENSED-PHI-VACUUM-CUT-PROJECT-001` — the cut-and-project objects are built but no property
   is proved; prove the φ-vacuum support cardinality / non-periodicity, or mark structural.
7. `D0-INTERPRETATION-SPINE-001` — relate the package fields to the real core invariants, or
   re-register as a structural/contract module (not 12 CORE theorems).
8. `D0-HULL-001` — derive FLC / aperiodicity / long-range-order from the tiling rule (currently
   asserted as properties).

**C. Ledger:**
9. Formalize `ASSUMP-COMPACT-LIE-KILLING-NEGATIVE` internally (Mathlib Killing form).
10. Identify/rename `ASSUMP-HST-EXTERNAL`'s owner precisely (or convert to a named PROOF-TARGET).

**D. Already honest (no action — do NOT "upgrade" by overclaiming):** the 13 legitimate external
owners; the finite-decidable certs (E8 Gram, Q8/Dedekind, CKM, window-44, Pisot, signature-(3,1),
spin-2 TT, Jones, mixing-hierarchy) — these are the intended finite proofs, abstract step owned.

---

## 7. Bottom line

The D0 Lean layer is in **good honest shape**: **zero proof holes**, a large genuinely
machine-checked finite-decidable core, and abstract steps disclosed via 13 legitimate external-owner
edges. "Not fully proved" resolves into three honest categories, not a wall of gaps: (i) abstract
generalizations correctly owned by classical theorems (keep); (ii) ~32 vacuous markers + ~30
structural-definition / struct-projection wrappers that are shallow but mostly redundant helpers
(prove-a-property or mark-structural — §6.B); (iii) a short high-value list of finite theorems worth
promoting from instance-decide to stated-theorem (§6.A) and 2 ledger assumptions to fix (§6.C). No
claim currently overclaims a `: True` stub as CORE (Iter-18 sweep + guard). The single most useful
next formalization pass is §6.A (4 finite, feasible upgrades) + §6.C (the 2 real ledger flags).
