import Mathlib.GroupTheory.Perm.Sign
import Mathlib.Tactic
import D0.Geometry.A4DLocatedPrimalDualCell
import D0.Geometry.ArchiveDiagonalRoleTransport
import D0.Geometry.ArchiveHodgeCARDiracKernel

/-!
# Located topological primal/dual star

The signed maps move an archive cochain from a primal corner to the
complementary dual corner. On a homogeneous degree-`k` sector their square is
the scalar `(-1)^{k(4-k)}`, with no leftover translation.

`D_H` is parity-odd. In four roles the complement preserves Fock parity, so the
located star commutes with `parityCochain`.

The dual forward incidence is the positive-direction creation differential. It is
not defined by conjugating `dForward` through the star. On this shared carrier
that positive stencil is extensionally `dForward`, and its counting adjoint is
`hodgeCodifferential`. The placed coface corner still moves by `2 e_r`; the
intertwiner uses one role step because `∇⁺` samples `x` and `x+e_r`.
-/

namespace D0.Geometry

open D0
open RoleFockPermutation
open scoped BigOperators

def koszulDegreeSign (k : ℕ) : ℝ :=
  if (k * (4 - k)) % 2 = 0 then 1 else -1

def incidenceDegreeSign (k : ℕ) : ℝ :=
  if (k + 1) % 2 = 0 then 1 else -1

def degreeParitySign (k : ℕ) : ℝ :=
  if k % 2 = 0 then 1 else -1

/-- Chirality on one exterior degree, `(-1)^{ℓ(ℓ-1)/2}`. -/
def chiralitySign (ℓ : ℕ) : ℝ :=
  if (ℓ * (ℓ - 1) / 2) % 2 = 0 then 1 else -1

/-- `⋆_PD` on the existing site/Fock cochain carrier. -/
def locatedPrimalStar (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    complementOrientation (occupationComplement p.2) *
      ψ (p.1 + occupationIndicator N p.2, occupationComplement p.2)

/-- Reverse star `⋆_DP`, with the orientation sign of the input label. -/
def locatedDualStar (N : ℕ) (φ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    complementOrientation (occupationComplement p.2) *
      φ (p.1 - occupationIndicator N (occupationComplement p.2),
        occupationComplement p.2)

theorem locatedPrimalStar_add (N : ℕ) (ψ φ : ArchiveCochain N) :
    locatedPrimalStar N (ψ + φ) = locatedPrimalStar N ψ + locatedPrimalStar N φ := by
  funext p
  simp only [locatedPrimalStar, Pi.add_apply]
  ring

theorem locatedPrimalStar_smul (N : ℕ) (a : ℝ) (ψ : ArchiveCochain N) :
    locatedPrimalStar N (a • ψ) = a • locatedPrimalStar N ψ := by
  funext p
  simp only [locatedPrimalStar, Pi.smul_apply, smul_eq_mul]
  ring

theorem locatedPrimalStar_homogeneous (N k : ℕ) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N (4 - k) (locatedPrimalStar N ψ) := by
  intro x S hS
  have hpre : fockDegree (occupationComplement S) ≠ k := by
    intro hk
    have hcomp := degree_complement S
    have hle := fockDegree_le_four S
    have hdeg : fockDegree S = 4 - k := by
      rw [hk] at hcomp
      omega
    exact hS hdeg
  simp only [locatedPrimalStar]
  rw [hψ _ _ hpre]
  ring

theorem locatedStar_square_homogeneous (N k : ℕ) (_hk : k ≤ 4)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    locatedDualStar N (locatedPrimalStar N ψ) = koszulDegreeSign k • ψ := by
  funext p
  simp only [locatedDualStar, locatedPrimalStar, Pi.smul_apply, smul_eq_mul]
  have hsite : p.1 - occupationIndicator N (occupationComplement p.2) +
      occupationIndicator N (occupationComplement p.2) = p.1 := by
    simp only [sub_eq_add_neg]
    abel
  rw [hsite, occupationComplement_involutive]
  by_cases hdeg : fockDegree p.2 = k
  · rw [show complementOrientation (occupationComplement p.2) *
          (complementOrientation p.2 * ψ p) =
          (complementOrientation p.2 *
            complementOrientation (occupationComplement p.2)) * ψ p by ring,
        epsilon_complement_sign, hdeg]
    simp only [koszulDegreeSign]
  · rw [hψ p.1 p.2 hdeg]
    simp [koszulDegreeSign]

theorem locatedStar_square_l2 (k : ℕ) (hk : k ≤ 4) (ψ : ArchiveCochain 0)
    (hψ : HomogeneousCochain 0 k ψ) :
    locatedDualStar 0 (locatedPrimalStar 0 ψ) = koszulDegreeSign k • ψ :=
  locatedStar_square_homogeneous 0 k hk ψ hψ

theorem locatedStar_square_l3 (k : ℕ) (hk : k ≤ 4) (ψ : ArchiveCochain 1)
    (hψ : HomogeneousCochain 1 k ψ) :
    locatedDualStar 1 (locatedPrimalStar 1 ψ) = koszulDegreeSign k • ψ :=
  locatedStar_square_homogeneous 1 k hk ψ hψ

theorem locatedStar_square_l5 (k : ℕ) (hk : k ≤ 4) (ψ : ArchiveCochain 3)
    (hψ : HomogeneousCochain 3 k ψ) :
    locatedDualStar 3 (locatedPrimalStar 3 ψ) = koszulDegreeSign k • ψ :=
  locatedStar_square_homogeneous 3 k hk ψ hψ

/-- The complement does not flip Fock parity: `(-1)^{|Sᶜ|} = (-1)^{|S|}`. -/
theorem locatedStar_commutes_fockParity (N : ℕ) (ψ : ArchiveCochain N) :
    parityCochain N (locatedPrimalStar N ψ) =
      locatedPrimalStar N (parityCochain N ψ) := by
  funext p
  simp only [parityCochain, locatedPrimalStar]
  rw [fockParitySign_occupationComplement]
  ring

theorem homogeneousCochain_eq_zero_of_degree_gt
    (N k : ℕ) (hk : 4 < k) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) : ψ = 0 := by
  funext p
  have hdeg : fockDegree p.2 ≠ k := by
    intro h
    have hle := fockDegree_le_four p.2
    omega
  exact hψ p.1 p.2 hdeg

theorem dForward_degree_four (N : ℕ) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N 4 ψ) : dForward N ψ = 0 := by
  have hdeg := dForward_degree_raise N 4 ψ hψ
  exact homogeneousCochain_eq_zero_of_degree_gt N 5 (by omega) (dForward N ψ) hdeg

theorem hodgeCodifferential_degree_zero (N : ℕ) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N 0 ψ) : hodgeCodifferential N ψ = 0 := by
  classical
  funext p
  unfold hodgeCodifferential backwardAnnihilateDirection annihilateAction backwardSite
  simp only [Pi.zero_apply]
  apply Finset.sum_eq_zero
  intro r _
  rw [← Finset.sum_neg_distrib]
  apply Finset.sum_eq_zero
  intro ket _
  by_cases hc : carAnnihilate r p.2 ket = 0
  · rw [hc]
    simp [backwardDifference_apply]
  · have hdeg := carAnnihilate_degree_lower r p.2 ket hc
    have hket : fockDegree ket ≠ 0 := by omega
    have hzero : ψ (p.1, ket) = 0 := hψ p.1 ket hket
    have hminus : ψ (roleTranslateMinus N r p.1, ket) = 0 :=
      hψ (roleTranslateMinus N r p.1) ket hket
    simp [backwardDifference_apply, hzero, hminus]

theorem hodgeCodifferential_degree_lower (N k : ℕ) (hk : 1 ≤ k)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N (k - 1) (hodgeCodifferential N ψ) := by
  classical
  intro x bra hbra
  unfold hodgeCodifferential backwardAnnihilateDirection annihilateAction backwardSite
  apply Finset.sum_eq_zero
  intro r _
  rw [← Finset.sum_neg_distrib]
  apply Finset.sum_eq_zero
  intro ket _
  by_cases hc : carAnnihilate r bra ket = 0
  · rw [hc]
    simp [backwardDifference_apply]
  · have hdeg := carAnnihilate_degree_lower r bra ket hc
    have hket : fockDegree ket ≠ k := by
      intro hkdeg
      apply hbra
      omega
    have hx := hψ x ket hket
    have hxm := hψ (roleTranslateMinus N r x) ket hket
    simp [backwardDifference_apply, hx, hxm]

/-- Positive corner step of one role.
`∇⁺` intertwines through the located star with this one-step stencil. -/
def dualPositiveStep (N : ℕ) (r : Role) : ArchiveRolePhaseGroup N :=
  roleStep N r

/-- Displacement between the placed corners of `(x,S)` and `(x+e_r, S∪{r})`. -/
def dualCofaceDisplacement (N : ℕ) (r : Role) : ArchiveRolePhaseGroup N :=
  roleStep N r + roleStep N r

theorem located_coface_corner (N : ℕ) (x : ArchiveRolePhaseGroup N)
    (S : ArchiveFockState) (r : Role) (h : S r = false) :
    (locatedPrimalToDual (PrimalCell.mk (x + roleStep N r) (insertRole S r))).site =
      (locatedPrimalToDual (PrimalCell.mk x S)).site + dualCofaceDisplacement N r := by
  classical
  funext s
  simp only [locatedPrimalToDual, dualCofaceDisplacement, Pi.add_apply, Pi.sub_apply,
    Pi.neg_apply, sub_eq_add_neg, occupationIndicator_apply, occupationComplement_apply,
    insertRole, roleStep]
  by_cases hsr : s = r
  · subst hsr
    simp only [h, ite_true, ite_false, Bool.not_false, Bool.not_true]
    abel_nf
  · simp only [hsr, ite_false]
    abel

noncomputable section

/-- Independent dual forward incidence: creation along one positive role step.
This is not `J d J⁻¹`. -/
def dualPositiveIncidence (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ r : Role, ∑ ket : ArchiveFockState,
    carCreate r p.2 ket *
      (forwardDifferenceScale N *
        (ψ (p.1 + dualPositiveStep N r, ket) - ψ (p.1, ket)))

theorem dualPositiveIncidence_eq_dForward (N : ℕ) (ψ : ArchiveCochain N) :
    dualPositiveIncidence N ψ = dForward N ψ := by
  funext p
  unfold dualPositiveIncidence dForward forwardCreateDirection dualPositiveStep
  simp only [forwardDifference_apply, roleTranslatePlus_apply]

/-- Counting adjoint of the dual forward incidence. On this carrier it is `d†`. -/
def dualIncidenceAdjoint (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ r : Role, ∑ ket : ArchiveFockState,
    carAnnihilate r p.2 ket *
      (forwardDifferenceScale N *
        (ψ (p.1 - dualPositiveStep N r, ket) - ψ (p.1, ket)))

theorem dualIncidenceAdjoint_eq_hodgeCodifferential (N : ℕ) (ψ : ArchiveCochain N) :
    dualIncidenceAdjoint N ψ = hodgeCodifferential N ψ := by
  funext p
  unfold dualIncidenceAdjoint hodgeCodifferential backwardAnnihilateDirection
    annihilateAction backwardSite dualPositiveStep
  simp only [backwardDifference_apply, roleTranslateMinus_apply]
  apply Finset.sum_congr rfl
  intro r _
  rw [← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro ket _
  ring

theorem dualIncidenceAdjoint_pairing (N : ℕ) (ψ φ : ArchiveCochain N) :
    cochainPairing N (dualPositiveIncidence N ψ) φ =
      cochainPairing N ψ (dualIncidenceAdjoint N φ) := by
  rw [dualPositiveIncidence_eq_dForward, dualIncidenceAdjoint_eq_hodgeCodifferential]
  exact dForward_adjoint N ψ φ

theorem carCreate_ne_removeRole (r : Role) (bra ket : ArchiveFockState)
    (hket : ket ≠ removeRole bra r) : carCreate r bra ket = 0 := by
  classical
  by_cases hc : carCreate r bra ket = 0
  · exact hc
  · have hs := carCreate_support r bra ket hc
    apply False.elim
    apply hket
    funext s
    by_cases hsr : s = r
    · subst hsr
      simp [removeRole, hs.2.1]
    · simp [removeRole, hsr, hs.2.2 s hsr]

theorem carAnnihilate_ne_insertRole (r : Role) (bra ket : ArchiveFockState)
    (hket : ket ≠ insertRole bra r) : carAnnihilate r bra ket = 0 := by
  classical
  by_cases hc : carAnnihilate r bra ket = 0
  · exact hc
  · have hs := carAnnihilate_support r bra ket hc
    apply False.elim
    apply hket
    funext s
    by_cases hsr : s = r
    · subst hsr
      simp [insertRole, hs.1]
    · simp [insertRole, hsr, (hs.2.2 s hsr).symm]

/-- Orientation and CAR signs of one positive coface, for every unoccupied role. -/
theorem located_incidence_sign_int :
    ∀ (S : ArchiveFockState) (r : Role), S r = false →
      complementOrientationInt (insertRole S r) * carCreateInt r (insertRole S r) S =
        (if fockDegree S % 2 = 0 then (1 : ℤ) else -1) *
          complementOrientationInt S *
          carAnnihilateInt r (occupationComplement (insertRole S r))
            (occupationComplement S) := by
  native_decide

theorem located_incidence_sign (S : ArchiveFockState) (r : Role) (h : S r = false) :
    complementOrientation (insertRole S r) * carCreate r (insertRole S r) S =
      degreeParitySign (fockDegree S) * complementOrientation S *
        carAnnihilate r (occupationComplement (insertRole S r))
          (occupationComplement S) := by
  have hZ := congrArg (fun z : ℤ => (z : ℝ)) (located_incidence_sign_int S r h)
  simpa [complementOrientation, degreeParitySign, carCreate_eq_intCast,
    carAnnihilate_eq_intCast, Int.cast_mul, Int.cast_ite] using hZ

theorem incidenceDegreeSign_eq_neg_parity (k : ℕ) :
    incidenceDegreeSign k = -degreeParitySign k := by
  rcases Nat.mod_two_eq_zero_or_one k with hk | hk
  · have hk1 : (k + 1) % 2 = 1 := by omega
    simp [incidenceDegreeSign, degreeParitySign, hk, hk1]
  · have hk1 : (k + 1) % 2 = 0 := by omega
    simp [incidenceDegreeSign, degreeParitySign, hk, hk1]

theorem locatedStar_intertwines_forward (N k : ℕ) (_hk : k ≤ 4)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    locatedPrimalStar N (dForward N ψ) =
      incidenceDegreeSign k • hodgeCodifferential N (locatedPrimalStar N ψ) := by
  classical
  funext p
  set y : ArchiveRolePhaseGroup N := p.1
  set T : ArchiveFockState := p.2
  set U : ArchiveFockState := occupationComplement T
  simp only [Pi.smul_apply, smul_eq_mul, locatedPrimalStar]
  have hforward :
      dForward N ψ (y + occupationIndicator N T, U) =
        ∑ r : Role,
          carCreate r U (removeRole U r) * forwardDifferenceScale N *
            (ψ (y + occupationIndicator N T + roleStep N r, removeRole U r) -
              ψ (y + occupationIndicator N T, removeRole U r)) := by
    unfold dForward forwardCreateDirection
    simp only [forwardDifference_apply, roleTranslatePlus_apply]
    apply Finset.sum_congr rfl
    intro r _
    rw [Finset.sum_eq_single (removeRole U r)]
    · ring
    · intro ket _ hket
      rw [carCreate_ne_removeRole r U ket hket]
      ring
    · intro h
      exact (h (Finset.mem_univ _)).elim
  have hbackward :
      hodgeCodifferential N (locatedPrimalStar N ψ) (y, T) =
        ∑ r : Role,
          carAnnihilate r T (insertRole T r) * forwardDifferenceScale N *
            ((locatedPrimalStar N ψ) (y - roleStep N r, insertRole T r) -
              (locatedPrimalStar N ψ) (y, insertRole T r)) := by
    rw [← dualIncidenceAdjoint_eq_hodgeCodifferential]
    unfold dualIncidenceAdjoint dualPositiveStep
    apply Finset.sum_congr rfl
    intro r _
    rw [Finset.sum_eq_single (insertRole T r)]
    · ring
    · intro ket _ hket
      rw [carAnnihilate_ne_insertRole r T ket hket]
      ring
    · intro h
      exact (h (Finset.mem_univ _)).elim
  rw [hforward, hbackward]
  rw [Finset.mul_sum, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro r _
  by_cases hTr : T r = false
  · have hUr : U r = true := by
      simpa [U, occupationComplement] using hTr
    set S : ArchiveFockState := removeRole U r
    have hinsert : insertRole S r = U := insertRole_removeRole U r hUr
    have hK : occupationComplement S = insertRole T r := by
      simpa [S, U, occupationComplement_involutive] using
        (occupationComplement_removeRole U r)
    have hSlabel : S = occupationComplement (insertRole T r) := by
      rw [← hK, occupationComplement_involutive]
    have hstep : occupationIndicator N (insertRole T r) =
        occupationIndicator N T + roleStep N r :=
      occupationIndicator_insertRole N T r hTr
    have hsiteMinus : y - roleStep N r + occupationIndicator N (insertRole T r) =
        y + occupationIndicator N T := by
      rw [hstep, sub_eq_add_neg]
      abel
    have hsitePlus : y + occupationIndicator N (insertRole T r) =
        y + occupationIndicator N T + roleStep N r := by
      rw [hstep]
      abel
    rw [incidenceDegreeSign_eq_neg_parity]
    by_cases hdeg : fockDegree S = k
    · have hsign := located_incidence_sign S r (by simp [S, removeRole])
      rw [hinsert, hdeg] at hsign
      have hsign' : complementOrientation U * carCreate r U S =
          degreeParitySign k * complementOrientation S *
            carAnnihilate r T (insertRole T r) := by
        simpa [U, hK, occupationComplement_involutive] using hsign
      have hK' : occupationComplement (insertRole T r) = S := by
        rw [← hK, occupationComplement_involutive]
      have hstarMinus :
          locatedPrimalStar N ψ (y - roleStep N r, insertRole T r) =
            complementOrientation S * ψ (y + occupationIndicator N T, S) := by
        rw [locatedPrimalStar, hK', hsiteMinus]
      have hstarAt :
          locatedPrimalStar N ψ (y, insertRole T r) =
            complementOrientation S *
              ψ (y + occupationIndicator N T + roleStep N r, S) := by
        rw [locatedPrimalStar, hK', hsitePlus]
      rw [hstarMinus, hstarAt]
      rw [show occupationComplement p.2 = U from rfl]
      rw [← mul_assoc, ← mul_assoc, hsign']
      ring
    · have hzero₁ : ψ (y + occupationIndicator N T + roleStep N r, S) = 0 :=
        hψ _ S hdeg
      have hzero₂ : ψ (y + occupationIndicator N T, S) = 0 := hψ _ S hdeg
      have hK' : occupationComplement (insertRole T r) = S := by
        rw [← hK, occupationComplement_involutive]
      have hstarMinus :
          locatedPrimalStar N ψ (y - roleStep N r, insertRole T r) =
            complementOrientation S * ψ (y + occupationIndicator N T, S) := by
        rw [locatedPrimalStar, hK', hsiteMinus]
      have hstarAt :
          locatedPrimalStar N ψ (y, insertRole T r) =
            complementOrientation S *
              ψ (y + occupationIndicator N T + roleStep N r, S) := by
        rw [locatedPrimalStar, hK', hsitePlus]
      rw [hstarMinus, hstarAt, hzero₁, hzero₂]
      simp
  · have hUr : U r = false := by
      simpa [U, occupationComplement] using hTr
    have hcreate : carCreate r U (removeRole U r) = 0 := by
      by_cases hc : carCreate r U (removeRole U r) = 0
      · exact hc
      · have htrue := (carCreate_support r U (removeRole U r) hc).1
        rw [hUr] at htrue
        cases htrue
    have hann : carAnnihilate r T (insertRole T r) = 0 := by
      by_cases hc : carAnnihilate r T (insertRole T r) = 0
      · exact hc
      · have hfalse := (carAnnihilate_support r T (insertRole T r) hc).2.1
        exact (hTr hfalse).elim
    rw [incidenceDegreeSign_eq_neg_parity, hcreate, hann]
    simp [locatedPrimalStar]

end

theorem occupationIndicator_transport {N : ℕ} (σ : Equiv.Perm Role)
    (S : ArchiveFockState) :
    permuteRoleSite σ (occupationIndicator N S) =
      occupationIndicator N (transportState σ S) := by
  funext s
  simp [permuteRoleSite, occupationIndicator, transportState]

theorem transportState_occupationComplement (σ : Equiv.Perm Role) (S : ArchiveFockState) :
    transportState σ (occupationComplement S) =
      occupationComplement (transportState σ S) := by
  funext r
  simp [transportState, occupationComplement]

theorem diagonalRoleTransport_apply {N : ℕ} (σ : Equiv.Perm Role)
    (ψ : ArchiveCochain N) (p : ArchiveCochainBasis N) :
    diagonalRoleTransport σ ψ p =
      (fermionSign σ (transportState σ.symm p.2) : ℝ) *
        ψ (permuteRoleSite σ.symm p.1, transportState σ.symm p.2) := by
  classical
  unfold diagonalRoleTransport
  rw [Finset.sum_eq_single (transportState σ.symm p.2)]
  · have hmatch : p.2 = transportState σ (transportState σ.symm p.2) :=
      (transportState_leftInverse σ.symm p.2).symm
    rw [signedTransport, if_pos hmatch]
  · intro ket _ hket
    have hne : p.2 ≠ transportState σ ket := by
      intro h
      have hket' : transportState σ.symm p.2 = ket := by
        rw [h]
        exact transportState_leftInverse σ ket
      exact (hket hket'.symm).elim
    rw [signedTransport, if_neg hne]
    simp
  · intro hmem
    exact (hmem (Finset.mem_univ _)).elim

/-- Fixed-orientation sign: complement transport picks up `sgn(σ)`. -/
theorem complement_transport_fermion_sign :
    ∀ (σ : Equiv.Perm Role) (U : ArchiveFockState),
      complementOrientationInt (transportState σ (occupationComplement U)) *
          fermionSign σ (occupationComplement U) =
        (Equiv.Perm.sign σ : ℤ) * fermionSign σ U *
          complementOrientationInt (occupationComplement U) := by
  native_decide

theorem locatedStar_role_pseudoequivariant (N : ℕ) (σ : Equiv.Perm Role)
    (ψ : ArchiveCochain N) :
    locatedPrimalStar N (diagonalRoleTransport σ ψ) =
      ((Equiv.Perm.sign σ : ℤ) : ℝ) •
        diagonalRoleTransport σ (locatedPrimalStar N ψ) := by
  classical
  funext p
  simp only [locatedPrimalStar, Pi.smul_apply, smul_eq_mul]
  rw [diagonalRoleTransport_apply, diagonalRoleTransport_apply]
  set S : ArchiveFockState := p.2
  set U : ArchiveFockState := transportState σ.symm S
  have hcomp : transportState σ.symm (occupationComplement S) =
      occupationComplement U := by
    simpa [U] using transportState_occupationComplement σ.symm S
  have hback : transportState σ (occupationComplement U) = occupationComplement S := by
    rw [← hcomp]
    exact transportState_leftInverse σ.symm (occupationComplement S)
  have hsite : permuteRoleSite σ.symm (p.1 + occupationIndicator N S) =
      permuteRoleSite σ.symm p.1 + occupationIndicator N U := by
    rw [permuteRoleSite_add]
    simp [U, occupationIndicator_transport]
  have hsignZ := complement_transport_fermion_sign σ U
  have hsign : (complementOrientation (transportState σ (occupationComplement U)) : ℝ) *
        (fermionSign σ (occupationComplement U) : ℝ) =
      ((Equiv.Perm.sign σ : ℤ) : ℝ) * (fermionSign σ U : ℝ) *
        (complementOrientation (occupationComplement U) : ℝ) := by
    have hcast := congrArg (fun z : ℤ => (z : ℝ)) hsignZ
    simpa [complementOrientation, Int.cast_mul] using hcast
  rw [hback] at hsign
  rw [hsite, hcomp]
  simp only [locatedPrimalStar]
  rw [← mul_assoc]
  rw [hsign]
  ring

theorem locatedStar_swapAB (N : ℕ) (ψ : ArchiveCochain N) :
    locatedPrimalStar N (diagonalRoleTransport (Equiv.swap D0.A D0.B) ψ) =
      -diagonalRoleTransport (Equiv.swap D0.A D0.B) (locatedPrimalStar N ψ) := by
  rw [locatedStar_role_pseudoequivariant]
  have hsign : ((Equiv.Perm.sign (Equiv.swap D0.A D0.B) : ℤ) : ℝ) = -1 := by
    rw [Equiv.Perm.sign_swap (by decide : D0.A ≠ D0.B)]
    norm_num
  rw [hsign]
  simp

def evenRoleCycle : Equiv.Perm Role :=
  Equiv.swap D0.A D0.B * Equiv.swap D0.B D0.C

theorem locatedStar_even_cycle (N : ℕ) (ψ : ArchiveCochain N) :
    locatedPrimalStar N (diagonalRoleTransport evenRoleCycle ψ) =
      diagonalRoleTransport evenRoleCycle (locatedPrimalStar N ψ) := by
  rw [locatedStar_role_pseudoequivariant]
  have hsign : ((Equiv.Perm.sign evenRoleCycle : ℤ) : ℝ) = 1 := by
    rw [evenRoleCycle, map_mul, Equiv.Perm.sign_swap (by decide : D0.A ≠ D0.B),
      Equiv.Perm.sign_swap (by decide : D0.B ≠ D0.C)]
    norm_num
  rw [hsign]
  simp

theorem koszulDegreeSign_eq_parity (k : ℕ) (hk : k ≤ 4) :
    koszulDegreeSign k = degreeParitySign k := by
  interval_cases k <;> simp [koszulDegreeSign, degreeParitySign]

theorem degreeParitySign_sq (k : ℕ) : degreeParitySign k * degreeParitySign k = 1 := by
  unfold degreeParitySign
  split_ifs <;> norm_num

theorem degreeParitySign_complement (k : ℕ) (hk : k ≤ 4) :
    degreeParitySign (4 - k) = degreeParitySign k := by
  interval_cases k <;> simp [degreeParitySign]

theorem incidenceDegreeSign_complement (k : ℕ) (hk : k ≤ 4) :
    incidenceDegreeSign (4 - k) = -degreeParitySign k := by
  interval_cases k <;> simp [incidenceDegreeSign, degreeParitySign]

theorem koszul_five_sub (k : ℕ) (hk1 : 1 ≤ k) (hk : k ≤ 4) :
    koszulDegreeSign (5 - k) = incidenceDegreeSign k := by
  interval_cases k <;> simp [koszulDegreeSign, incidenceDegreeSign]

theorem chiralitySign_sq (ℓ : ℕ) : chiralitySign ℓ * chiralitySign ℓ = 1 := by
  unfold chiralitySign
  split_ifs <;> norm_num

theorem chiralitySign_succ (k : ℕ) (hk : k ≤ 4) :
    chiralitySign (k + 1) * chiralitySign k = degreeParitySign k := by
  interval_cases k <;> simp [chiralitySign, degreeParitySign]

theorem chiralitySign_pred (k : ℕ) (hk1 : 1 ≤ k) (hk : k ≤ 4) :
    chiralitySign (k - 1) * chiralitySign k = -degreeParitySign k := by
  interval_cases k <;> simp [chiralitySign, degreeParitySign]

def applyChirality (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => chiralitySign (fockDegree p.2) * ψ p

theorem applyChirality_smul (N : ℕ) (a : ℝ) (ψ : ArchiveCochain N) :
    applyChirality N (a • ψ) = a • applyChirality N ψ := by
  funext p
  simp [applyChirality, Pi.smul_apply, smul_eq_mul]
  ring

theorem applyChirality_homogeneous (N k : ℕ) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    applyChirality N ψ = chiralitySign k • ψ := by
  funext p
  simp only [applyChirality, Pi.smul_apply, smul_eq_mul]
  by_cases hdeg : fockDegree p.2 = k
  · simp [hdeg]
  · have h0 : ψ p = 0 := hψ p.1 p.2 hdeg
    rw [h0]
    ring

theorem locatedPrimalStar_neg (N : ℕ) (ψ : ArchiveCochain N) :
    locatedPrimalStar N (-ψ) = -locatedPrimalStar N ψ := by
  funext p
  simp [locatedPrimalStar, Pi.neg_apply]

theorem locatedPrimalStar_hodge (N : ℕ) (ψ : ArchiveCochain N) :
    locatedPrimalStar N (hodgeCarDirac N ψ) =
      locatedPrimalStar N (dForward N ψ) +
        locatedPrimalStar N (hodgeCodifferential N ψ) := by
  rw [hodgeCarDirac, locatedPrimalStar_add]

theorem dualDirac_eq_hodgeCarDirac (N : ℕ) (ψ : ArchiveCochain N) :
    dualPositiveIncidence N ψ + dualIncidenceAdjoint N ψ = hodgeCarDirac N ψ := by
  rw [dualPositiveIncidence_eq_dForward, dualIncidenceAdjoint_eq_hodgeCodifferential,
    hodgeCarDirac]

/-- The complementary half of the signed incidence relation. -/
theorem locatedStar_intertwines_codifferential (N k : ℕ) (hk : k ≤ 4)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    locatedPrimalStar N (hodgeCodifferential N ψ) =
      degreeParitySign k • dForward N (locatedPrimalStar N ψ) := by
  classical
  funext p
  let y : ArchiveRolePhaseGroup N := p.1
  let T : ArchiveFockState := p.2
  let S : ArchiveFockState := occupationComplement T
  let x : ArchiveRolePhaseGroup N := y + occupationIndicator N T
  simp only [Pi.smul_apply, smul_eq_mul, locatedPrimalStar]
  have hleft : hodgeCodifferential N ψ (x, S) =
      ∑ r : Role, carAnnihilate r S (insertRole S r) * forwardDifferenceScale N *
        (ψ (x, insertRole S r) - ψ (x - roleStep N r, insertRole S r)) := by
    unfold hodgeCodifferential backwardAnnihilateDirection annihilateAction backwardSite
    simp only [backwardDifference_apply, roleTranslateMinus_apply]
    apply Finset.sum_congr rfl
    intro r _
    rw [Finset.sum_eq_single (insertRole S r)]
    · ring
    · intro ket _ hket
      rw [carAnnihilate_ne_insertRole r S ket hket]
      ring
    · intro h
      exact (h (Finset.mem_univ _)).elim
  have hright : dForward N (locatedPrimalStar N ψ) (y, T) =
      ∑ r : Role, carCreate r T (removeRole T r) * forwardDifferenceScale N *
        (locatedPrimalStar N ψ (y + roleStep N r, removeRole T r) -
          locatedPrimalStar N ψ (y, removeRole T r)) := by
    unfold dForward forwardCreateDirection
    simp only [forwardDifference_apply, roleTranslatePlus_apply]
    apply Finset.sum_congr rfl
    intro r _
    rw [Finset.sum_eq_single (removeRole T r)]
    · ring
    · intro ket _ hket
      rw [carCreate_ne_removeRole r T ket hket]
      ring
    · intro h
      exact (h (Finset.mem_univ _)).elim
  rw [hleft, hright]
  rw [Finset.mul_sum, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro r _
  by_cases hTr : T r = true
  · have hSr : S r = false := by simpa [S, occupationComplement] using hTr
    let K : ArchiveFockState := removeRole T r
    have hinsert : insertRole K r = T := insertRole_removeRole T r hTr
    have hcompK : occupationComplement K = insertRole S r := by
      simpa [K, S, occupationComplement_involutive] using occupationComplement_removeRole T r
    have hstep : occupationIndicator N T =
        occupationIndicator N K + roleStep N r := by
      simpa [K] using occupationIndicator_insertRole N K r (by simp [K, removeRole])
    have hxminus : x - roleStep N r = y + occupationIndicator N K := by
      dsimp [x]
      rw [hstep, sub_eq_add_neg]
      abel
    have hxplus : y + roleStep N r + occupationIndicator N K = x := by
      dsimp [x]
      rw [← hstep]
      abel
    have hstarPlus : locatedPrimalStar N ψ (y + roleStep N r, K) =
        complementOrientation K * ψ (x, insertRole S r) := by
      rw [locatedPrimalStar, hcompK, hxplus]
    have hstarAt : locatedPrimalStar N ψ (y, K) =
        complementOrientation K * ψ (x - roleStep N r, insertRole S r) := by
      rw [locatedPrimalStar, hcompK, hxminus]
    have hsign := located_incidence_sign K r (by simp [K, removeRole])
    rw [hinsert] at hsign
    have hsign' : complementOrientation T * carCreate r T K =
        degreeParitySign (fockDegree K) * complementOrientation K *
          carAnnihilate r S (insertRole S r) := by
      simpa [S, hcompK, occupationComplement_involutive] using hsign
    by_cases hdeg : fockDegree K = 4 - k
    · have hparity : degreeParitySign (fockDegree K) = degreeParitySign k := by
        rw [hdeg, degreeParitySign_complement k hk]
      have hsign'' : complementOrientation T * carAnnihilate r S (insertRole S r) =
          degreeParitySign k * complementOrientation K * carCreate r T K := by
        rw [← hparity] at hsign'
        linear_combination degreeParitySign_sq (fockDegree K) *
          (carAnnihilate r S (insertRole S r) * complementOrientation T)
      rw [hstarPlus, hstarAt, hsign'']
      ring
    · have hdegK : fockDegree (insertRole S r) = 4 - fockDegree K := by
        rw [← hcompK, degree_complement]
      have hnot : fockDegree (insertRole S r) ≠ k := by
        rw [hdegK]
        omega
      have hzero₁ : ψ (x, insertRole S r) = 0 := hψ x _ hnot
      have hzero₂ : ψ (x - roleStep N r, insertRole S r) = 0 := hψ _ _ hnot
      rw [hstarPlus, hstarAt, hzero₁, hzero₂]
      simp
  · have hSr : S r = false := by
      simpa [S, occupationComplement] using hTr
    have hcreate : carCreate r T (removeRole T r) = 0 := by
      by_cases hc : carCreate r T (removeRole T r) = 0
      · exact hc
      · have hfalse := (carCreate_support r T (removeRole T r) hc).1
        rw [hTr] at hfalse
        cases hfalse
    have hann : carAnnihilate r S (insertRole S r) = 0 := by
      by_cases hc : carAnnihilate r S (insertRole S r) = 0
      · exact hc
      · have htrue := (carAnnihilate_support r S (insertRole S r) hc).2.1
        exact (hSr htrue).elim
    rw [hcreate, hann]
    simp


end D0.Geometry
