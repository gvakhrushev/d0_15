import Mathlib.Tactic
import Mathlib.Data.ZMod.Basic
import D0.Synthesis.TransportFieldNoGolden

/-!
# The transport splitting field: discriminant obstruction to any golden content

**Target.** `D0-TRANSPORT-FIELD-NO-GOLDEN-001` proved that no quadratic-degree element (in
particular `φ`, `φ⁻¹`) lies in a SINGLE-eigenvalue field `ℚ⟮λ⟯` of the transport cubic
`λ³ − 359λ − 2574`, and named its own next step verbatim: "the splitting-field statement is a
possible further step, not claimed" — degree 6 admits a quadratic subfield, so the joint-field
question was genuinely open. This module discharges the ARITHMETIC content of that step, with
clean axioms (no `native_decide`):

* `disc_from_coefficients` — the cubic's discriminant is `Δ = −4p³ − 27q² = 6185264`
  (the same value owned as `discriminant_positive` at `D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001`);
* `disc_factorization` + `prime_193`/`prime_2003` — `Δ = 2⁴ · 193 · 2003`, squarefree kernel
  `386579 = 193 · 2003`;
* `disc_not_square` — `Δ` is not a square in `ℤ` (mod-9 certificate: `Δ ≡ 5`, squares mod 9
  are `{0,1,4,7}`);
* `five_disc_not_square` — `5Δ` is not a square in `ℤ` (mod-7 certificate: `5Δ ≡ 5`, squares
  mod 7 are `{0,1,2,4}`) — this is the exact criterion for `ℚ(√Δ) ≠ ℚ(√5)`;
* `kernel_certificate` — `Δ · 386579 = 1546316²` IS a square: the positive control — the same
  machinery CONFIRMS the discriminant's own kernel (√386579 does lie in the splitting field,
  as `√Δ` always does), while refusing `√5`.

**The owner-edge reading (external theorem, hypotheses proved here).** For an irreducible
cubic over ℚ (irreducibility OWNED in Lean: `TransportFieldNoGolden.Pcubic_irreducible`), the
Galois group of the splitting field `K` is `S₃` iff `Δ` is not a rational square (else `A₃`);
with `Gal = S₃`, `[K:ℚ] = 6` and `K` contains EXACTLY ONE quadratic subfield, `ℚ(√Δ)`
(standard Galois theory of cubics — external owner edge, cited in the registry row; not
re-proved in Lean). Given `disc_not_square` (so `S₃`) and `five_disc_not_square` (so
`ℚ(√Δ) ≠ ℚ(√5)`), it follows that `√5 ∉ K` and hence `φ = (1+√5)/2 ∉ K`: **no rational
function with rational coefficients of ALL THREE transport eigenvalues jointly — the full
splitting-field closure — contains any golden quantity.** The class "rational-coefficient
functions of transport eigenvalues" is exhausted BY CONSTRUCTION (every such function lies in
`K`), so this is the maximal-scope form of the twice-killed universal, and it upgrades
`TransportFieldNoGolden` from single-eigenvalue fields to the joint closure.

**Honest scope.** The `S₃`-classification and unique-quadratic-subfield steps are the named
EXTERNAL owner edge (the row is an owner-edge/no-go row, not a full Lean closure); everything
arithmetic — discriminant value, factorization, both non-squareness certificates, the kernel
certificate — is Lean-clean, and the assembly theorem below is the ARITHMETIC CONJUNCTION
ONLY. Prior in-tree computation of the same `S₃` leg: BOOK_04:1399 and
`vp_hypercharge_flow_weyl_nogo.py` already record "nonsquare 6185264 ⇒ Gal = S₃" for this
cubic (there as rejected Weyl numerology; supporting, no field-membership claim).
Consequence for obligation (i) of `D0-ALPHA-SEAM-FORM-FORCED-001`, jointly with
`D0-TORAL-COMPOSITION-SEVENTEEN-001`, stated in the negative form actually proved: NO
transport-spectral origin for the `φ`-power content exists in the exhausted
rational-coefficient class; the toral return system is the only OWNED positive origin to
date. Other operator families and non-rational-coefficient readings are untouched; no door
is adjudicated (door 1 `dim g_light` live rival); the seam is untouched; (γ) is not owned.
-/

namespace D0.Synthesis.TransportSplittingFieldObstruction

open D0.Synthesis.TransportFieldNoGolden

/-- The transport cubic's discriminant from its own coefficients:
`Δ = −4·(−359)³ − 27·(−2574)² = 6185264` (value owned at
`D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001` as `discriminant_positive`). -/
theorem disc_from_coefficients : -4 * (-359 : ℤ) ^ 3 - 27 * (-2574 : ℤ) ^ 2 = 6185264 := by
  norm_num

/-- `Δ = 2⁴ · 193 · 2003`; the squarefree kernel is `386579 = 193 · 2003`. -/
theorem disc_factorization :
    (6185264 : ℤ) = 2 ^ 4 * 193 * 2003 ∧ (386579 : ℤ) = 193 * 2003 := by
  norm_num

theorem prime_193 : Nat.Prime 193 := by norm_num

theorem prime_2003 : Nat.Prime 2003 := by norm_num

/-- Mod-9 certificate: squares in `ZMod 9` are `{0,1,4,7}` and `Δ ≡ 5`. -/
theorem disc_not_square : ¬ IsSquare (6185264 : ℤ) := by
  intro h
  have h9 : IsSquare ((6185264 : ℤ) : ZMod 9) := h.map (Int.castRingHom (ZMod 9))
  have : ((6185264 : ℤ) : ZMod 9) = 5 := by decide
  rw [this] at h9
  obtain ⟨r, hr⟩ := h9
  revert hr
  revert r
  decide

/-- Mod-7 certificate for the FIELD-DISTINCTION step: `5Δ` is not a square, hence
`ℚ(√Δ) ≠ ℚ(√5)` (two quadratic fields coincide iff the product of their radicands is a
rational square). -/
theorem five_disc_not_square : ¬ IsSquare (5 * 6185264 : ℤ) := by
  intro h
  have h7 : IsSquare ((5 * 6185264 : ℤ) : ZMod 7) := h.map (Int.castRingHom (ZMod 7))
  have : ((5 * 6185264 : ℤ) : ZMod 7) = 5 := by decide
  rw [this] at h7
  obtain ⟨r, hr⟩ := h7
  revert hr
  revert r
  decide

/-- `5` itself is not a square in `ℤ` (mod-3 certificate: `5 ≡ 2`, squares mod 3 are `{0,1}`)
— makes the irrationality of `√5` internally owned rather than absorbed in the owner edge. -/
theorem five_not_square : ¬ IsSquare (5 : ℤ) := by
  intro h
  have h3 : IsSquare ((5 : ℤ) : ZMod 3) := h.map (Int.castRingHom (ZMod 3))
  have : ((5 : ℤ) : ZMod 3) = 2 := by decide
  rw [this] at h3
  obtain ⟨r, hr⟩ := h3
  revert hr
  revert r
  decide

/-- Positive control (the machinery can CONFIRM membership): the discriminant's own kernel
passes — `Δ · 386579 = 1546316²` is a square, matching the standard fact `√Δ ∈ K`. The same
test refuses `5` (`five_disc_not_square`): the criterion distinguishes, it does not
blanket-reject. -/
theorem kernel_certificate : (6185264 : ℤ) * 386579 = 1546316 ^ 2 := by
  norm_num

/-- Assembly: the arithmetic legs of the splitting-field obstruction. Irreducibility of the
cubic is owned at `TransportFieldNoGolden.Pcubic_irreducible` (imported); the
`S₃`/unique-quadratic-subfield classification is the named external owner edge (row text). -/
theorem transport_splitting_field_obstruction :
    (-4 * (-359 : ℤ) ^ 3 - 27 * (-2574 : ℤ) ^ 2 = 6185264)
      ∧ ¬ IsSquare (6185264 : ℤ)
      ∧ ¬ IsSquare (5 * 6185264 : ℤ)
      ∧ (6185264 : ℤ) * 386579 = 1546316 ^ 2 :=
  ⟨disc_from_coefficients, disc_not_square, five_disc_not_square, kernel_certificate⟩

end D0.Synthesis.TransportSplittingFieldObstruction
