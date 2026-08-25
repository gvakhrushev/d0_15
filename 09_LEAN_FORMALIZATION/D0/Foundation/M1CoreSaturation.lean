import D0.Spectral.AlphaPresentCoreMaximalityNoGo
import D0.Matter.HiggsCondensationPresentCoreMaximalityNoGo
import D0.Representation.FinitePathRepresentation

/-!
# P-M1-SATURATION — Lean lift of the four extremality instances (owner-gated lift, 2026-07-18)

Source: `_TASKS_CENTER_ATTACK/RAISE_M1CORE_SATURATION_MEMO.md` (skeptic NO-KILL on all four
headlines, 2026-07-06; Lean lift was HELD owner-gated) + `raise_m1core_check.py` (26/26,
mutation-tested). Registry rows: `D0-P-M1-SATURATION-001` (umbrella), `D0-P-SUBCRIT-001`,
`D0-P-ABELIAN-001`.

The parent principle (one theorem shape, four functionals): the M1 present-core sub-object is the
unique F-extremum of an owned order/valuation functional on its admissible class, the no-go is the
saturation of that extremum, and a witness lies JUST PAST the extremum but OUTSIDE the class — the
exact external import the no-go names.

Machine-checked here — the four INSTANCES (COLOUR/ALPHA: core attains the extremum + bound over
the formalized candidate class + external witness just past + uniqueness over the M1 zone family;
R1: the centralizer value + isotype arithmetic, maximality and witness narrated; HIGGS: the full
commutant characterization — core = Comm(T) — plus the external witness):

1. **COLOUR → RIGIDITY-EXTREMALITY.** Functionals on zone frames `d : Fin 3 → ℕ`: `commPairs`
   (`#{(i,j) | dᵢ = dⱼ}` — equals `Σ (class size)²`, the commutant dimension of
   `diag(d₀,d₁,d₂) ⊆ M₃`) and `swapOrder` (`#{σ ∈ S₃ | d∘σ = d}`, the Weyl/zone-swap order). The
   M1 `+2` frame `{24,22,20}` attains the JOINT minimum `(3,1)`; the bounds `commPairs ≥ 3`,
   `swapOrder ≥ 1` hold over ALL ℕ-frames (a fortiori over the M1 zone family); the equal frame
   (the colour witness) sits just past at `(9,6)`. RR (memo repair, preserved): this is extremal
   RIGIDITY — colour `⊗ℂ³` stays an EXTERNAL import, NOT derived (abelian `ℂ³` dim 3 < dim M₃ 9).
2. **ALPHA → SUBCRITICAL-EXTREMALITY** (`D0-P-SUBCRIT-001`). `rate a = φ^a·r = φ^{a-3}`:
   the full characterization `rate a < 1 ↔ a ≤ 2` (the ⟸ leg is the owned `rate_lt_one`; the ⟹
   leg — criticality of every `a ≥ 3` — is NEW here via `φ`-monotonicity), with `rate 3 = 1` the
   critical wall (`φ³` carrier = the external witness just past).
3. **R1 → MAXIMAL-COMMUTANT.** The reconstructed Aut-representation has
   `commutantDim = 12 = 3² + 1 + 1 + 1` — the full centralizer (NARRATED maximality; owned
   `commutant_dim_eq`; the decomposition arithmetic added). Witness past: the external
   `PRIM-FINITE-SPECTRAL-TRIPLE-REP` (narrated, per memo).
4. **HIGGS → MAXIMAL-ABELIAN** (`D0-P-ABELIAN-001`). Every present-core projector
   (`a•1 + b•T`) commutes with `T` (owned `tPoly_commutes`); the non-commuting witness `Qnc`
   exists but is NOT present-core (owned `Qnc_not_commute`). RR (memo repair, preserved): this
   raises W1 (the commutativity wall) ONLY — W2 (the SSB double-well sign) STAYS EXTERNAL;
   filling `Qnc` is necessary-but-not-sufficient; NOT "condensation derived".

NOT machine-checked (narrated, per the memo): the parent schema's universality over "owned
functionals on the admissible class 𝒞" as a single quantified second-order meta-theorem — Lean
owns the four instances; the umbrella `m1_core_saturation` is their conjunction. UNIQUENESS
grading (skeptic #16 repair): over ALL ℕ-frames the joint floor `(3,1)` is attained by every
all-distinct frame (e.g. `![0,1,2]`) — uniqueness is claimed and machine-checked ONLY over the
M1 zone family (`m1Frame_unique_joint_min`); the R1 instance carries no formalized candidate
class (value + arithmetic only, maximality narrated). The four no-go rows stay NO-GO (this is
their positive face, never a promotion past the boundary).
-/

namespace D0.Foundation.M1CoreSaturation

open D0.Spectral.AlphaProfiniteSpectralTower
open D0.Spectral.AlphaPresentCoreMaximalityNoGo
open D0.Matter.HiggsCondensationPresentCoreMaximalityNoGo
open D0.Representation.FinitePathRepresentation
open D0

/-! ## Instance 1 — COLOUR: rigidity extremality of the `+2` frame -/

/-- Commutant-dimension functional: `#{(i,j) | dᵢ = dⱼ} = Σ (class size)²` — the dimension of the
commutant of `diag(d₀,d₁,d₂)` in `M₃`. -/
def commPairs (d : Fin 3 → ℕ) : ℕ :=
  ((Finset.univ : Finset (Fin 3 × Fin 3)).filter fun p => d p.1 = d p.2).card

/-- Zone-swap-order functional: `#{σ ∈ S₃ | d ∘ σ = d}`. -/
def swapOrder (d : Fin 3 → ℕ) : ℕ :=
  ((Finset.univ : Finset (Equiv.Perm (Fin 3))).filter fun σ => ∀ i, d (σ i) = d i).card

/-- The M1-forced `+2` zone frame `{L₅+2, L₅, L₅−2} = {24, 22, 20}`. -/
def m1Frame : Fin 3 → ℕ := ![24, 22, 20]

/-- The equal frame — the colour witness JUST PAST the extremum (external: `⊗ℂ³`). -/
def equalFrame : Fin 3 → ℕ := ![22, 22, 22]

theorem m1Frame_commPairs : commPairs m1Frame = 3 := by decide
theorem m1Frame_swapOrder : swapOrder m1Frame = 1 := by decide
theorem equalFrame_commPairs : commPairs equalFrame = 9 := by decide
theorem equalFrame_swapOrder : swapOrder equalFrame = 6 := by decide

/-- The diagonal is always in the equal-pair set: `commPairs ≥ 3` for EVERY frame — so `(3,·)` is
the global floor and the M1 frame attains it. -/
theorem commPairs_ge_three (d : Fin 3 → ℕ) : 3 ≤ commPairs d := by
  classical
  have hsub : (Finset.univ.image fun i : Fin 3 => ((i, i) : Fin 3 × Fin 3)) ⊆
      ((Finset.univ : Finset (Fin 3 × Fin 3)).filter fun p => d p.1 = d p.2) := by
    intro p hp
    simp only [Finset.mem_image] at hp
    obtain ⟨i, -, rfl⟩ := hp
    simp
  have hcard : (Finset.univ.image fun i : Fin 3 => ((i, i) : Fin 3 × Fin 3)).card = 3 := by decide
  calc (3 : ℕ) = _ := hcard.symm
    _ ≤ _ := Finset.card_le_card hsub

/-- The identity always fixes the frame: `swapOrder ≥ 1` for EVERY frame. -/
theorem swapOrder_ge_one (d : Fin 3 → ℕ) : 1 ≤ swapOrder d := by
  classical
  have hmem : (1 : Equiv.Perm (Fin 3)) ∈
      ((Finset.univ : Finset (Equiv.Perm (Fin 3))).filter fun σ => ∀ i, d (σ i) = d i) := by
    simp
  exact Finset.card_pos.mpr ⟨_, hmem⟩

/-- **COLOUR rigidity-extremality (bundle).** The M1 `+2` frame attains the joint floor `(3, 1)`
of (commutant dimension, swap order) over all frames; the equal frame — the colour witness just
past the extremum — sits at `(9, 6)`. Colour `⊗ℂ³` is NOT derived by this. -/
theorem colour_rigidity_extremality :
    (commPairs m1Frame = 3 ∧ swapOrder m1Frame = 1) ∧
    (∀ d : Fin 3 → ℕ, 3 ≤ commPairs d ∧ 1 ≤ swapOrder d) ∧
    (commPairs equalFrame = 9 ∧ swapOrder equalFrame = 6) :=
  ⟨⟨m1Frame_commPairs, m1Frame_swapOrder⟩,
   fun d => ⟨commPairs_ge_three d, swapOrder_ge_one d⟩,
   ⟨equalFrame_commPairs, equalFrame_swapOrder⟩⟩

/-- The memo's admissible M1 zone family 𝒞 — the script's three NAMED frames
(`raise_m1core_check.py` equal/degen/forced; its two floor-probes are NOT members of 𝒞). -/
def m1ZoneFamily : List (Fin 3 → ℕ) := [![22, 22, 22], ![24, 24, 20], ![24, 22, 20]]

/-- **Uniqueness over the M1 zone family** (the memo's 𝒞): within `m1ZoneFamily`, the joint
floor `(3, 1)` is attained by the `+2` frame ALONE. (Over all ℕ-frames uniqueness FAILS — every
all-distinct frame attains the floor — which is why the claim is graded to 𝒞; skeptic #16.) -/
theorem m1Frame_unique_joint_min :
    ∀ d ∈ m1ZoneFamily, (commPairs d = 3 ∧ swapOrder d = 1) ↔ d = m1Frame := by
  decide

/-! ## Instance 2 — ALPHA: golden-subcritical extremality (`D0-P-SUBCRIT-001`) -/

/-- NEW leg (the memo's ⟹ direction): at and past the wall, the rate is critical or worse —
`3 ≤ a ⇒ 1 ≤ rate a`, by `φ`-monotonicity from the owned `rate 3 = 1`. -/
theorem rate_ge_one_of_three_le (a : ℕ) (ha : 3 ≤ a) : 1 ≤ rate a := by
  have hφ : (1 : ℝ) ≤ phi := le_of_lt one_lt_phi
  have hmono : phi ^ 3 ≤ phi ^ a := pow_le_pow_right₀ hφ ha
  have hr : (0 : ℝ) < r := tower_weight_ratio_pos
  have h : rate 3 ≤ rate a := by
    unfold rate
    exact mul_le_mul_of_nonneg_right hmono (le_of_lt hr)
  calc (1 : ℝ) = rate 3 := rate_three_eq_one.symm
    _ ≤ rate a := h

/-- **Golden-subcritical extremality: the FULL characterization** `rate a < 1 ↔ a ≤ 2`.
`a ≤ 2` is exactly the maximal SUBCRITICAL region (the trace-class reading lives in the owned
NoGo module); the present-core (`a ∈ {0,1}`) sits strictly inside it; `a = 3` (`φ³` carrier) is the critical external witness just past. -/
theorem subcritical_iff (a : ℕ) : rate a < 1 ↔ a ≤ 2 := by
  constructor
  · intro h
    by_contra hgt
    have := rate_ge_one_of_three_le a (by omega)
    linarith
  · exact rate_lt_one a

/-- **ALPHA subcritical-extremality (bundle).** -/
theorem alpha_subcritical_extremality :
    (∀ a : ℕ, rate a < 1 ↔ a ≤ 2) ∧ rate 3 = 1 :=
  ⟨subcritical_iff, rate_three_eq_one⟩

/-! ## Instance 3 — R1: maximal commutant of the reconstructed representation -/

/-- **R1 maximal-commutant (value + isotype arithmetic).** `commutantDim = 12` (owned
`commutant_dim_eq`) and `commutantDim = generationMult² + 1 + 1 + 1` — the decomposition
arithmetic now consumes the owned `generationMult`, tying 12 to the generation block (3²) plus
three abelian lines. The FULL-centralizer maximality ("no larger algebra commutes") and the
witness just past (`PRIM-FINITE-SPECTRAL-TRIPLE-REP`) stay narrated — no candidate class is
formalized for this instance. -/
theorem r1_maximal_commutant :
    commutantDim = 12 ∧ commutantDim = generationMult ^ 2 + 1 + 1 + 1 :=
  ⟨commutant_dim_eq, by decide⟩

/-! ## Instance 4 — HIGGS: present-core is maximal abelian (`D0-P-ABELIAN-001`) -/

/-- **The maximality leg (NEW; skeptic #16 repair R3; forward direction — the converse is `tPoly_commutes`).** EVERY matrix commuting with `T` is a
present-core polynomial `a•1 + b•T` — concretely `Q = Q₀₀•1 + Q₀₁•T`. Together with
`tPoly_commutes` this is the full characterization `Comm(T) = {a•1 + b•T}`: the present-core is
not merely commuting but MAXIMAL abelian. Exhaustive over all `44⁴` matrices (native_decide,
same grade as the owned `Qnc_not_commute`). -/
theorem commute_T_core_characterization :
    ∀ Q : Matrix (Fin 2) (Fin 2) (ZMod 44),
      Commute Matter.HiggsReturnQuotientAction.T Q →
      Q = (Q 0 0) • (1 : Matrix (Fin 2) (Fin 2) (ZMod 44)) +
          (Q 0 1) • Matter.HiggsReturnQuotientAction.T := by
  unfold Commute SemiconjBy
  native_decide

/-- **HIGGS maximal-abelian (bundle).** Every present-core projector commutes with `T`; the
non-commuting witness `Qnc` exists but is not present-core. Raises W1 only — W2 (SSB sign)
stays external. -/
theorem higgs_maximal_abelian :
    (∀ a b : ZMod 44, Commute Matter.HiggsReturnQuotientAction.T
      (a • (1 : Matrix (Fin 2) (Fin 2) (ZMod 44)) + b • Matter.HiggsReturnQuotientAction.T)) ∧
    (∀ Q : Matrix (Fin 2) (Fin 2) (ZMod 44),
      Commute Matter.HiggsReturnQuotientAction.T Q →
      ∃ a b : ZMod 44, Q = a • (1 : Matrix (Fin 2) (Fin 2) (ZMod 44)) +
        b • Matter.HiggsReturnQuotientAction.T) ∧
    ¬ Commute Matter.HiggsReturnQuotientAction.T Qnc :=
  ⟨tPoly_commutes, fun Q h => ⟨Q 0 0, Q 0 1, commute_T_core_characterization Q h⟩, Qnc_not_commute⟩

/-! ## The umbrella -/

/-- **P-M1-SATURATION (four instances, machine-checked).** The conjunction of the four
extremality instances — the parent schema INSTANTIATED (the schema's second-order universality
over functionals stays narrated; the four no-go rows stay NO-GO). -/
theorem m1_core_saturation :
    ((commPairs m1Frame = 3 ∧ swapOrder m1Frame = 1) ∧
      (∀ d : Fin 3 → ℕ, 3 ≤ commPairs d ∧ 1 ≤ swapOrder d) ∧
      (commPairs equalFrame = 9 ∧ swapOrder equalFrame = 6)) ∧
    (∀ d ∈ m1ZoneFamily, (commPairs d = 3 ∧ swapOrder d = 1) ↔ d = m1Frame) ∧
    ((∀ a : ℕ, rate a < 1 ↔ a ≤ 2) ∧ rate 3 = 1) ∧
    (commutantDim = 12 ∧ commutantDim = generationMult ^ 2 + 1 + 1 + 1) ∧
    ((∀ a b : ZMod 44, Commute Matter.HiggsReturnQuotientAction.T
        (a • (1 : Matrix (Fin 2) (Fin 2) (ZMod 44)) + b • Matter.HiggsReturnQuotientAction.T)) ∧
      (∀ Q : Matrix (Fin 2) (Fin 2) (ZMod 44),
        Commute Matter.HiggsReturnQuotientAction.T Q →
        ∃ a b : ZMod 44, Q = a • (1 : Matrix (Fin 2) (Fin 2) (ZMod 44)) +
          b • Matter.HiggsReturnQuotientAction.T) ∧
      ¬ Commute Matter.HiggsReturnQuotientAction.T Qnc) :=
  ⟨colour_rigidity_extremality, m1Frame_unique_joint_min, alpha_subcritical_extremality,
   r1_maximal_commutant, higgs_maximal_abelian⟩

end D0.Foundation.M1CoreSaturation
