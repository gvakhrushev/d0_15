import D0.Matter.CKMBasisMismatch
import D0.Matter.FiniteSelector
import Mathlib.Tactic

namespace D0.Matter

/--
A finite family of candidate operator bases for one flavour sector.

The point is to move CKM one step upstream: the up/down bases are not allowed to
be silent choices.  They must come from finite candidate supports together with
score functionals before the mismatch matrix is formed.
-/
structure FiniteOperatorBasisFamily (n : ℕ) (Op : Type) where
  Candidate : Type
  support_fintype : Fintype Candidate
  basis : Candidate → FiniteOperatorBasis n Op
  score : Candidate → ℚ


/-- The ordinary finite selector attached to a finite basis family. -/
def FiniteOperatorBasisFamily.toSelector {n : ℕ} {Op : Type}
    (F : FiniteOperatorBasisFamily n Op) : FiniteSelector F.Candidate where
  support_fintype := F.support_fintype
  score := F.score

/--
A strict basis selection: a finite family plus a strictly selected candidate.
This is the Lean-side replacement for the phrase "choose the up/down basis".
-/
structure StrictOperatorBasisSelection (n : ℕ) (Op : Type) where
  family : FiniteOperatorBasisFamily n Op
  selected : family.Candidate
  selected_strict : StrictSelected family.toSelector selected

/-- The actual operator basis produced by a strict finite basis selection. -/
def StrictOperatorBasisSelection.selectedBasis {n : ℕ} {Op : Type}
    (S : StrictOperatorBasisSelection n Op) : FiniteOperatorBasis n Op :=
  S.family.basis S.selected

/--
The CKM origin object: two finite basis selectors, one for the up sector and one
for the down sector.  The CKM carrier is downstream of these selectors.
-/
structure CKMBasisOrigin (n : ℕ) (Op : Type) where
  up : StrictOperatorBasisSelection n Op
  down : StrictOperatorBasisSelection n Op

/-- The matrix determined by the selected up/down bases of a CKM origin object. -/
def ckmOriginMatrix {n : ℕ} {Op : Type} (O : CKMBasisOrigin n Op) :
    Matrix (Fin n) (Fin n) ℚ :=
  basisMismatchMatrix O.up.selectedBasis O.down.selectedBasis

/--
An admissible CKM-origin candidate must use strictly selected up/down basis
candidates and must report the mismatch of the resulting bases.
-/
structure CKMOriginCandidate {n : ℕ} {Op : Type} (O : CKMBasisOrigin n Op) where
  upSelected : O.up.family.Candidate
  downSelected : O.down.family.Candidate
  up_strict : StrictSelected O.up.family.toSelector upSelected
  down_strict : StrictSelected O.down.family.toSelector downSelected
  matrix : Matrix (Fin n) (Fin n) ℚ
  agrees : matrix = basisMismatchMatrix (O.up.family.basis upSelected)
    (O.down.family.basis downSelected)

/-- A strict up-sector basis selector has a unique selected basis candidate. -/
theorem ckm_origin_up_candidate_unique {n : ℕ} {Op : Type}
    (O : CKMBasisOrigin n Op) (u : O.up.family.Candidate)
    (hu : StrictSelected O.up.family.toSelector u) :
    u = O.up.selected := by
  exact strict_selected_unique O.up.family.toSelector hu O.up.selected_strict

/-- A strict down-sector basis selector has a unique selected basis candidate. -/
theorem ckm_origin_down_candidate_unique {n : ℕ} {Op : Type}
    (O : CKMBasisOrigin n Op) (d : O.down.family.Candidate)
    (hd : StrictSelected O.down.family.toSelector d) :
    d = O.down.selected := by
  exact strict_selected_unique O.down.family.toSelector hd O.down.selected_strict

/--
The selected up/down bases are therefore unique under the same finite basis
selectors.  Any different basis requires a score deformation upstream.
-/
theorem ckm_origin_selected_bases_unique {n : ℕ} {Op : Type}
    (O : CKMBasisOrigin n Op) (u : O.up.family.Candidate)
    (d : O.down.family.Candidate)
    (hu : StrictSelected O.up.family.toSelector u)
    (hd : StrictSelected O.down.family.toSelector d) :
    O.up.family.basis u = O.up.selectedBasis ∧
      O.down.family.basis d = O.down.selectedBasis := by
  constructor
  · rw [ckm_origin_up_candidate_unique O u hu]
    rfl
  · rw [ckm_origin_down_candidate_unique O d hd]
    rfl

/--
Origin-level CKM closure: once the up/down basis selectors are fixed, every
admissible CKM-origin candidate returns the same matrix.
-/
theorem ckm_origin_candidate_matrix_unique {n : ℕ} {Op : Type}
    (O : CKMBasisOrigin n Op) (C : CKMOriginCandidate O) :
    C.matrix = ckmOriginMatrix O := by
  have hu : C.upSelected = O.up.selected :=
    ckm_origin_up_candidate_unique O C.upSelected C.up_strict
  have hd : C.downSelected = O.down.selected :=
    ckm_origin_down_candidate_unique O C.downSelected C.down_strict
  rw [C.agrees, hu, hd]
  rfl

/--
No alternative CKM matrix is admissible at fixed finite basis selectors.  A
second matrix means that at least one upstream basis selector/readout/calibration
layer changed.
-/
theorem ckm_no_free_matrix_at_fixed_basis_origin {n : ℕ} {Op : Type}
    (O : CKMBasisOrigin n Op) (M : Matrix (Fin n) (Fin n) ℚ)
    (hM : M ≠ ckmOriginMatrix O) :
    ¬ ∃ C : CKMOriginCandidate O, C.matrix = M := by
  rintro ⟨C, hC⟩
  apply hM
  rw [← hC]
  exact ckm_origin_candidate_matrix_unique O C

/--
If an alternative up-sector candidate differs from the selected one, it cannot
also be strictly selected under the same up-basis selector.
-/
theorem ckm_origin_no_alternative_up_basis {n : ℕ} {Op : Type}
    (O : CKMBasisOrigin n Op) (u : O.up.family.Candidate)
    (hu : u ≠ O.up.selected) :
    ¬ StrictSelected O.up.family.toSelector u := by
  exact no_alternative_strict_selected O.up.family.toSelector O.up.selected_strict hu

/--
If an alternative down-sector candidate differs from the selected one, it cannot
also be strictly selected under the same down-basis selector.
-/
theorem ckm_origin_no_alternative_down_basis {n : ℕ} {Op : Type}
    (O : CKMBasisOrigin n Op) (d : O.down.family.Candidate)
    (hd : d ≠ O.down.selected) :
    ¬ StrictSelected O.down.family.toSelector d := by
  exact no_alternative_strict_selected O.down.family.toSelector O.down.selected_strict hd

/-- A three-point orientation support used for the concrete CKM-origin witness. -/
inductive CKMOrientationCandidate where
  | canonical
  | cyclicShift
  | reversed
  deriving DecidableEq, Repr, Fintype

/-- The finite flavour operator carrier for the concrete witness. -/
abbrev CKMFlavorOperator := Fin 3

/-- Three finite orientation maps on the three-generation support. -/
def ckmOrientationVector : CKMOrientationCandidate → Fin 3 → CKMFlavorOperator
  | .canonical, i => i
  | .cyclicShift, i =>
      if i = 0 then 1 else if i = 1 then 2 else 0
  | .reversed, i =>
      if i = 0 then 2 else if i = 1 then 1 else 0

/-- Coordinate readout induced by an orientation map. -/
def ckmOrientationCoord (c : CKMOrientationCandidate) (x : CKMFlavorOperator)
    (j : Fin 3) : ℚ :=
  if x = ckmOrientationVector c j then 1 else 0

/-- Convert a finite orientation candidate to an operator basis. -/
def ckmOrientationBasis (c : CKMOrientationCandidate) :
    FiniteOperatorBasis 3 CKMFlavorOperator where
  vector := ckmOrientationVector c
  coord := ckmOrientationCoord c

/-- Up-sector orientation selector: canonical orientation is the strict minimum. -/
def ckmUpBasisScore : CKMOrientationCandidate → ℚ
  | .canonical => 0
  | .cyclicShift => 1
  | .reversed => 2

/-- Down-sector orientation selector: cyclic-shift orientation is the strict minimum. -/
def ckmDownBasisScore : CKMOrientationCandidate → ℚ
  | .canonical => 1
  | .cyclicShift => 0
  | .reversed => 2

/-- Finite up-sector basis family for the concrete CKM-origin witness. -/
def ckmUpBasisFamily : FiniteOperatorBasisFamily 3 CKMFlavorOperator where
  Candidate := CKMOrientationCandidate
  support_fintype := inferInstance
  basis := ckmOrientationBasis
  score := ckmUpBasisScore

/-- Finite down-sector basis family for the concrete CKM-origin witness. -/
def ckmDownBasisFamily : FiniteOperatorBasisFamily 3 CKMFlavorOperator where
  Candidate := CKMOrientationCandidate
  support_fintype := inferInstance
  basis := ckmOrientationBasis
  score := ckmDownBasisScore

/-- The canonical up orientation is strictly selected. -/
theorem ckm_up_canonical_strict :
    StrictSelected ckmUpBasisFamily.toSelector CKMOrientationCandidate.canonical := by
  constructor
  intro b hb
  cases b with
  | canonical => exact False.elim (hb rfl)
  | cyclicShift =>
      change ckmUpBasisScore CKMOrientationCandidate.canonical <
        ckmUpBasisScore CKMOrientationCandidate.cyclicShift
      norm_num [ckmUpBasisScore]
  | reversed =>
      change ckmUpBasisScore CKMOrientationCandidate.canonical <
        ckmUpBasisScore CKMOrientationCandidate.reversed
      norm_num [ckmUpBasisScore]

/-- The cyclic down orientation is strictly selected. -/
theorem ckm_down_cyclic_strict :
    StrictSelected ckmDownBasisFamily.toSelector CKMOrientationCandidate.cyclicShift := by
  constructor
  intro b hb
  cases b with
  | canonical =>
      change ckmDownBasisScore CKMOrientationCandidate.cyclicShift <
        ckmDownBasisScore CKMOrientationCandidate.canonical
      norm_num [ckmDownBasisScore]
  | cyclicShift => exact False.elim (hb rfl)
  | reversed =>
      change ckmDownBasisScore CKMOrientationCandidate.cyclicShift <
        ckmDownBasisScore CKMOrientationCandidate.reversed
      norm_num [ckmDownBasisScore]

/-- Concrete finite up-basis selection witness. -/
def ckmUpBasisSelection : StrictOperatorBasisSelection 3 CKMFlavorOperator where
  family := ckmUpBasisFamily
  selected := CKMOrientationCandidate.canonical
  selected_strict := ckm_up_canonical_strict

/-- Concrete finite down-basis selection witness. -/
def ckmDownBasisSelection : StrictOperatorBasisSelection 3 CKMFlavorOperator where
  family := ckmDownBasisFamily
  selected := CKMOrientationCandidate.cyclicShift
  selected_strict := ckm_down_cyclic_strict

/-- Concrete CKM-origin witness: the matrix is produced after both bases are selected. -/
def concreteCKMBasisOrigin : CKMBasisOrigin 3 CKMFlavorOperator where
  up := ckmUpBasisSelection
  down := ckmDownBasisSelection

/-- The concrete CKM origin is not a free matrix at fixed basis selectors. -/
theorem concrete_ckm_origin_no_free_matrix
    (M : Matrix (Fin 3) (Fin 3) ℚ)
    (hM : M ≠ ckmOriginMatrix concreteCKMBasisOrigin) :
    ¬ ∃ C : CKMOriginCandidate concreteCKMBasisOrigin, C.matrix = M := by
  exact ckm_no_free_matrix_at_fixed_basis_origin concreteCKMBasisOrigin M hM

end D0.Matter
