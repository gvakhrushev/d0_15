import Mathlib.Tactic
import D0.Representation.OrientationNontrivialGrading
import D0.Extensions.RepresentationReadoutExtension
import D0.Matter.CanonicalZoneCirculation
import D0.Foundation.ObservableCompletionCanonicity

/-!
# D0.Synthesis.RepresentationAndCirculationCanonicity

Theoretical owner: `D0-REPRESENTATION-AND-CIRCULATION-CANONICITY-001`.

Foundational synthesis linking the new representation / grading and matter circulation
results to the canonical `ObservableCompletionCanonicity` framework:

1. **Orientation Nontrivial Grading Canonicity**:
   - Any 3-dimensional generation grading satisfying `BothSignsPresent` has signatures
     in `{(2,1), (1,2)}`.
   - The observable `readout := fun (p, q) => ncCount p q` evaluates to `8` on ALL
     such completions.
   - By `constant_readout_m1_forced`, the neutral-current count `8` is `M1Forced`
     WITHOUT variational MDL / commutant-minimization.

2. **Cross-carrier transport-choice invariance**:
   - The three owned terminal sectors `(E₀,E₄,E₃)` carry the sign multiset `(+,-,+)`.
   - The intrinsic generation frame has exactly three lines.
   - Any bijective relabelling of terminal sectors onto generation lines preserves the
     sign multiplicities `(2,1)`; therefore every such transport completion has
     neutral-current readout `8`.
   - Hence the *choice of bijection itself* is gauge for this observable: no canonical
     sector-to-generation numbering is required to force `nc=8`.

   Honest boundary: this removes the need to choose a privileged bijection.  It does
   not prove the stronger semantic statement that the terminal sector sign is the
   physical grading acting on the generation block; that representation-level bridge
   remains distinct.

3. **Canonical Zone Circulation Direction Canonicity**:
   - For any nonzero divergence-free zone-homogeneous flow $J$ on $K(9,11,13)$,
     all three components are nonzero and proportional to $(13, 9, 11)$.
   - The normalized orientation ray / projectivized circulation line is uniquely forced.
-/

namespace D0.Synthesis.RepresentationAndCirculationCanonicity

open D0.Representation.OrientationNontrivialGrading
open D0.Extensions.RepresentationReadoutExtension
open D0.Matter.CanonicalZoneCirculation
open D0.Foundation.ObservableCompletionCanonicity
open D0.Foundation

/-- Admissible 3-generation grading completion: non-negative integer pair `(p, q)`
summing to 3 with both signs present. -/
def AdmissibleGradingSignature (sig : ℕ × ℕ) : Prop :=
  sig.1 + sig.2 = 3 ∧ BothSignsPresent sig.1 sig.2

/-- Observable readout map: neutral-current channel count. -/
def ncReadout (sig : ℕ × ℕ) : ℕ :=
  ncCount sig.1 sig.2

/-- Concrete witness: `(2, 1)` is admissible. -/
theorem admissible_grading_21 : AdmissibleGradingSignature (2, 1) := by
  refine ⟨rfl, ⟨by norm_num, by norm_num⟩⟩

/-- All admissible grading completions produce identical readout `8`. -/
theorem all_admissible_gradings_give_eight (sig : ℕ × ℕ) (hs : AdmissibleGradingSignature sig) :
    ncReadout sig = 8 := by
  rcases hs with ⟨hsum, hboth⟩
  unfold ncReadout
  exact nontrivial_signature_nc sig.1 sig.2 hsum hboth

/-- **Theorem: Neutral-current count 8 is M1-forced by orientation nontriviality.**
This upgrades the previous commutant-minimization selection to exact proof-theoretic
canonicity under `ObservableCompletionCanonicity`. -/
theorem nc_count_eight_m1_forced :
    M1Forced
      (CompletionForcesReadout AdmissibleGradingSignature ncReadout)
      8 := by
  have h_const : ∀ sig, AdmissibleGradingSignature sig → ncReadout sig = ncReadout (2, 1) := by
    intro sig hsig
    rw [all_admissible_gradings_give_eight sig hsig]
    rw [all_admissible_gradings_give_eight (2, 1) admissible_grading_21]
  have h_forced := constant_readout_m1_forced
    AdmissibleGradingSignature ncReadout (2, 1) admissible_grading_21 h_const
  have h_val : ncReadout (2, 1) = 8 := all_admissible_gradings_give_eight (2, 1) admissible_grading_21
  rw [h_val] at h_forced
  exact h_forced

/-! ## Transport-choice invariance

The cross-carrier issue has two logically separate parts:

* a semantic bridge saying that terminal orientation signs grade the generation lines;
* a choice of which of the three terminal sectors is identified with which generation line.

Only the first can matter for the neutral-current observable.  Once the semantic bridge
is admitted, the second is a pure permutation choice, and the theorem below proves that
all six choices have the same readout.
-/

/-- Three terminal orientation sectors in the owned order `(E₀,E₄,E₃)`.
`true` denotes the `+1` orientation sign and `false` the `-1` sign.  This is
exactly the sign pattern proved by `terminalOrientationSign_on_E0/E4/E3`. -/
def terminalSectorPositive : Fin 3 → Bool
  | 0 => true
  | 1 => false
  | 2 => true

/-- A transport completion is any bijective relabelling of the three terminal sectors
onto the three intrinsic generation lines. -/
abbrev OrientationTransport := Equiv.Perm (Fin 3)

/-- Pull the terminal sign pattern through a transport. -/
def transportedSectorPositive (σ : OrientationTransport) (g : Fin 3) : Bool :=
  terminalSectorPositive (σ.symm g)

/-- Number of positive generation lines after transport. -/
def transportedPositiveCount (σ : OrientationTransport) : ℕ :=
  ((Finset.univ : Finset (Fin 3)).filter
    (fun g => transportedSectorPositive σ g = true)).card

/-- Number of negative generation lines after transport. -/
def transportedNegativeCount (σ : OrientationTransport) : ℕ :=
  ((Finset.univ : Finset (Fin 3)).filter
    (fun g => transportedSectorPositive σ g = false)).card

/-- The transported grading signature. -/
def transportedSignature (σ : OrientationTransport) : ℕ × ℕ :=
  (transportedPositiveCount σ, transportedNegativeCount σ)

/-- Permuting the three sectors cannot change the sign multiplicities: every transport
has signature exactly `(2,1)`.  The proposition is finite (six permutations), so this
is discharged by exact kernel computation rather than by a chosen transport. -/
theorem transported_signature_invariant :
    ∀ σ : OrientationTransport, transportedSignature σ = (2, 1) := by
  native_decide

/-- Every bijective transport therefore lands inside the already-owned admissible
nontrivial grading class. -/
theorem transported_signature_admissible (σ : OrientationTransport) :
    AdmissibleGradingSignature (transportedSignature σ) := by
  rw [transported_signature_invariant σ]
  exact admissible_grading_21

/-- Neutral-current readout of a transport completion. -/
def transportNcReadout (σ : OrientationTransport) : ℕ :=
  ncReadout (transportedSignature σ)

/-- **Cross-carrier choice elimination for the observable.**
Every one of the six terminal-sector ↔ generation-line bijections gives `nc=8`. -/
theorem all_orientation_transports_give_eight (σ : OrientationTransport) :
    transportNcReadout σ = 8 := by
  unfold transportNcReadout
  exact all_admissible_gradings_give_eight
    (transportedSignature σ) (transported_signature_admissible σ)

/-- All bijective sector-to-line transports are admissible as *labelling completions*.
This intentionally does not assert the stronger physical representation bridge. -/
def AdmissibleOrientationTransport (_σ : OrientationTransport) : Prop := True

/-- **M1 canonicity modulo transport choice.**
The neutral-current observable is forced even though the transport object is not unique:
all admissible transport completions have the same readout. -/
theorem nc_transport_choice_m1_forced :
    M1Forced
      (CompletionForcesReadout AdmissibleOrientationTransport transportNcReadout)
      8 := by
  let σ₀ : OrientationTransport := Equiv.refl (Fin 3)
  have hσ₀ : AdmissibleOrientationTransport σ₀ := trivial
  have h_const :
      ∀ σ, AdmissibleOrientationTransport σ →
        transportNcReadout σ = transportNcReadout σ₀ := by
    intro σ _
    rw [all_orientation_transports_give_eight σ]
    rw [all_orientation_transports_give_eight σ₀]
  have h_forced := constant_readout_m1_forced
    AdmissibleOrientationTransport transportNcReadout σ₀ hσ₀ h_const
  have h_val : transportNcReadout σ₀ = 8 :=
    all_orientation_transports_give_eight σ₀
  rw [h_val] at h_forced
  exact h_forced

/-- Admissible circulation ray: ratio of $x$ to $y$ component for any nonzero divergence-free current. -/
def circulationRatio (J : ZoneFlow) : ℚ :=
  J.x / J.y

/-- For every nonzero divergence-free zone-homogeneous current, the circulation ratio
$J_x / J_y$ is invariant and identically equals $13 / 9$. -/
theorem circulation_ratio_invariant
    (J : ZoneFlow) (hJ : DivergenceFree J) (hnz : J.x ≠ 0 ∨ J.y ≠ 0 ∨ J.z ≠ 0) :
    circulationRatio J = 13 / 9 := by
  obtain ⟨t, hx, hy, hz⟩ := divergenceFree_classification J hJ
  have ht_nonzero : t ≠ 0 := by
    intro ht0
    subst t
    simp at hx hy hz
    rcases hnz with h | h | h
    · exact h hx
    · exact h hy
    · exact h hz
  unfold circulationRatio
  rw [hx, hy]
  have h9t : (9 : ℚ) * t ≠ 0 := mul_ne_zero (by norm_num) ht_nonzero
  calc (13 * t) / (9 * t) = (13 / 9 : ℚ) * (t / t) := by ring
  _ = (13 / 9 : ℚ) * 1 := by rw [div_self ht_nonzero]
  _ = 13 / 9 := mul_one _

/-- Summary owner connecting representation and matter circulation to the canonicity framework.
It now records both grading-signature canonicity and invariance under all cross-carrier
sector relabellings, while leaving the stronger semantic representation bridge explicit. -/
theorem representation_circulation_canonicity_owner :
    M1Forced (CompletionForcesReadout AdmissibleGradingSignature ncReadout) 8 ∧
    M1Forced (CompletionForcesReadout AdmissibleOrientationTransport transportNcReadout) 8 ∧
    (∀ J : ZoneFlow, DivergenceFree J → (J.x ≠ 0 ∨ J.y ≠ 0 ∨ J.z ≠ 0) →
      circulationRatio J = 13 / 9) :=
  ⟨nc_count_eight_m1_forced, nc_transport_choice_m1_forced, circulation_ratio_invariant⟩

end D0.Synthesis.RepresentationAndCirculationCanonicity
