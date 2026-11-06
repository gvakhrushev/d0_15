import D0.Geometry.OriginalBookCreatorBridge

namespace D0.Geometry.OriginalBookBoost

open D0
open OriginalBookCreatorBridge

/-!
Exact first boost stage of the original full128 checker, source blob
`d111c5bfeae3c384a4fe725f4a6d19277ea0005a`, lines 94–100, and its
original `native` construction, source blob
`ee8de4635d24c668949ac9a0186616ab7d59f2ed`, lines 70–80.

The checker specializes the half-angle parameter r=tanh(theta/2)=1/9:
theta=2atanh(1/9)=log(5/4), so sinh(theta)=9/40 and
cosh(theta)=41/40. This file constructs the algebraic rational polynomial;
the identity with the analytic matrix exponential is not claimed here.
The source uniform fixture elsewhere uses theta=0.08, not this specialization.
The original 128 Kraus operators, span and physical admission remain open.
-/

abbrev SourceMatrix := Matrix (Fin 16) (Fin 16) ℤ

/-- One of the four original creators, indexed through the typed D0 role. -/
def sourceCreatorMatrix (role : Role) : SourceMatrix :=
  fun bra ket => sourceCreator (sourceBit role) bra ket

/-- No assumed link: each entry is the previously proved typed CAR creator. -/
theorem sourceCreatorMatrix_eq_car (role : Role) (bra ket : Fin 16) :
    (sourceCreatorMatrix role bra ket : ℝ) =
      carCreate role (sourceState bra) (sourceState ket) :=
  source_creator_eq_real_car role bra ket

/-- Actual original G=c₀ c₁† + c₁ c₀†: mode 0 is A and mode 1 is D. -/
def sourceBoostGenerator : SourceMatrix :=
  sourceCreatorMatrix A * (sourceCreatorMatrix D).transpose +
    sourceCreatorMatrix D * (sourceCreatorMatrix A).transpose

/-- Explicit sparse form of G in the source bit basis. -/
def sparseBoostGenerator : SourceMatrix := fun bra ket =>
  if (bra = 1 ∧ ket = 2) ∨ (bra = 2 ∧ ket = 1) ∨
     (bra = 13 ∧ ket = 14) ∨ (bra = 14 ∧ ket = 13) then 1
  else if (bra = 5 ∧ ket = 6) ∨ (bra = 6 ∧ ket = 5) ∨
          (bra = 9 ∧ ket = 10) ∨ (bra = 10 ∧ ket = 9) then -1
  else 0

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_0 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (0 : Fin 16) =
      sparseBoostGenerator bra (0 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_1 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (1 : Fin 16) =
      sparseBoostGenerator bra (1 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_2 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (2 : Fin 16) =
      sparseBoostGenerator bra (2 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_3 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (3 : Fin 16) =
      sparseBoostGenerator bra (3 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_4 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (4 : Fin 16) =
      sparseBoostGenerator bra (4 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_5 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (5 : Fin 16) =
      sparseBoostGenerator bra (5 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_6 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (6 : Fin 16) =
      sparseBoostGenerator bra (6 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_7 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (7 : Fin 16) =
      sparseBoostGenerator bra (7 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_8 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (8 : Fin 16) =
      sparseBoostGenerator bra (8 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_9 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (9 : Fin 16) =
      sparseBoostGenerator bra (9 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_10 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (10 : Fin 16) =
      sparseBoostGenerator bra (10 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_11 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (11 : Fin 16) =
      sparseBoostGenerator bra (11 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_12 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (12 : Fin 16) =
      sparseBoostGenerator bra (12 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_13 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (13 : Fin 16) =
      sparseBoostGenerator bra (13 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_14 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (14 : Fin 16) =
      sparseBoostGenerator bra (14 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_entry_ket_15 : ∀ bra : Fin 16,
    sourceBoostGenerator bra (15 : Fin 16) =
      sparseBoostGenerator bra (15 : Fin 16) := by
  decide

theorem sourceBoostGenerator_eq_sparse : sourceBoostGenerator = sparseBoostGenerator := by
  ext bra ket
  fin_cases ket
  · exact boost_entry_ket_0 bra
  · exact boost_entry_ket_1 bra
  · exact boost_entry_ket_2 bra
  · exact boost_entry_ket_3 bra
  · exact boost_entry_ket_4 bra
  · exact boost_entry_ket_5 bra
  · exact boost_entry_ket_6 bra
  · exact boost_entry_ket_7 bra
  · exact boost_entry_ket_8 bra
  · exact boost_entry_ket_9 bra
  · exact boost_entry_ket_10 bra
  · exact boost_entry_ket_11 bra
  · exact boost_entry_ket_12 bra
  · exact boost_entry_ket_13 bra
  · exact boost_entry_ket_14 bra
  · exact boost_entry_ket_15 bra

/-- The squared generator projects onto the eight mixed-occupation states. -/
def sparseBoostSquare : SourceMatrix := fun bra ket =>
  if bra = ket ∧ (ket = 1 ∨ ket = 2 ∨ ket = 5 ∨ ket = 6 ∨
      ket = 9 ∨ ket = 10 ∨ ket = 13 ∨ ket = 14) then 1 else 0

set_option maxRecDepth 100000 in
private theorem boost_square_ket_0 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (0 : Fin 16) =
      sparseBoostSquare bra (0 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (0 : Fin 16) =
      sparseBoostGenerator bra (0 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_1 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (1 : Fin 16) =
      sparseBoostSquare bra (1 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (1 : Fin 16) =
      sparseBoostGenerator bra (1 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_2 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (2 : Fin 16) =
      sparseBoostSquare bra (2 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (2 : Fin 16) =
      sparseBoostGenerator bra (2 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_3 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (3 : Fin 16) =
      sparseBoostSquare bra (3 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (3 : Fin 16) =
      sparseBoostGenerator bra (3 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_4 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (4 : Fin 16) =
      sparseBoostSquare bra (4 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (4 : Fin 16) =
      sparseBoostGenerator bra (4 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_5 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (5 : Fin 16) =
      sparseBoostSquare bra (5 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (5 : Fin 16) =
      sparseBoostGenerator bra (5 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_6 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (6 : Fin 16) =
      sparseBoostSquare bra (6 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (6 : Fin 16) =
      sparseBoostGenerator bra (6 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_7 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (7 : Fin 16) =
      sparseBoostSquare bra (7 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (7 : Fin 16) =
      sparseBoostGenerator bra (7 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_8 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (8 : Fin 16) =
      sparseBoostSquare bra (8 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (8 : Fin 16) =
      sparseBoostGenerator bra (8 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_9 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (9 : Fin 16) =
      sparseBoostSquare bra (9 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (9 : Fin 16) =
      sparseBoostGenerator bra (9 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_10 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (10 : Fin 16) =
      sparseBoostSquare bra (10 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (10 : Fin 16) =
      sparseBoostGenerator bra (10 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_11 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (11 : Fin 16) =
      sparseBoostSquare bra (11 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (11 : Fin 16) =
      sparseBoostGenerator bra (11 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_12 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (12 : Fin 16) =
      sparseBoostSquare bra (12 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (12 : Fin 16) =
      sparseBoostGenerator bra (12 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_13 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (13 : Fin 16) =
      sparseBoostSquare bra (13 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (13 : Fin 16) =
      sparseBoostGenerator bra (13 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_14 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (14 : Fin 16) =
      sparseBoostSquare bra (14 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (14 : Fin 16) =
      sparseBoostGenerator bra (14 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem boost_square_ket_15 : ∀ bra : Fin 16,
    (sparseBoostGenerator * sparseBoostGenerator) bra (15 : Fin 16) =
      sparseBoostSquare bra (15 : Fin 16) ∧
    (sparseBoostSquare * sparseBoostGenerator) bra (15 : Fin 16) =
      sparseBoostGenerator bra (15 : Fin 16) := by
  decide

theorem sparseBoost_square_and_cube :
    sparseBoostGenerator * sparseBoostGenerator = sparseBoostSquare ∧
    sparseBoostSquare * sparseBoostGenerator = sparseBoostGenerator := by
  constructor
  · ext bra ket
    fin_cases ket
    · exact (boost_square_ket_0 bra).1
    · exact (boost_square_ket_1 bra).1
    · exact (boost_square_ket_2 bra).1
    · exact (boost_square_ket_3 bra).1
    · exact (boost_square_ket_4 bra).1
    · exact (boost_square_ket_5 bra).1
    · exact (boost_square_ket_6 bra).1
    · exact (boost_square_ket_7 bra).1
    · exact (boost_square_ket_8 bra).1
    · exact (boost_square_ket_9 bra).1
    · exact (boost_square_ket_10 bra).1
    · exact (boost_square_ket_11 bra).1
    · exact (boost_square_ket_12 bra).1
    · exact (boost_square_ket_13 bra).1
    · exact (boost_square_ket_14 bra).1
    · exact (boost_square_ket_15 bra).1
  · ext bra ket
    fin_cases ket
    · exact (boost_square_ket_0 bra).2
    · exact (boost_square_ket_1 bra).2
    · exact (boost_square_ket_2 bra).2
    · exact (boost_square_ket_3 bra).2
    · exact (boost_square_ket_4 bra).2
    · exact (boost_square_ket_5 bra).2
    · exact (boost_square_ket_6 bra).2
    · exact (boost_square_ket_7 bra).2
    · exact (boost_square_ket_8 bra).2
    · exact (boost_square_ket_9 bra).2
    · exact (boost_square_ket_10 bra).2
    · exact (boost_square_ket_11 bra).2
    · exact (boost_square_ket_12 bra).2
    · exact (boost_square_ket_13 bra).2
    · exact (boost_square_ket_14 bra).2
    · exact (boost_square_ket_15 bra).2

theorem sourceBoostGenerator_cube :
    sourceBoostGenerator * sourceBoostGenerator * sourceBoostGenerator =
      sourceBoostGenerator := by
  rw [sourceBoostGenerator_eq_sparse, sparseBoost_square_and_cube.1,
    sparseBoost_square_and_cube.2]

/-- The same integer generator, now in the characteristic-zero rational field. -/
def sourceBoostGeneratorRat : Matrix (Fin 16) (Fin 16) ℚ :=
  sourceBoostGenerator.map (Int.castRingHom ℚ)

theorem sourceBoostGeneratorRat_cube :
    sourceBoostGeneratorRat * sourceBoostGeneratorRat * sourceBoostGeneratorRat =
      sourceBoostGeneratorRat := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom ℚ))
    sourceBoostGenerator_cube
  change ((sourceBoostGenerator * sourceBoostGenerator * sourceBoostGenerator).map
    (Int.castRingHom ℚ)) = sourceBoostGenerator.map (Int.castRingHom ℚ) at h
  rw [Matrix.map_mul, Matrix.map_mul] at h
  exact h

/-- The checker's exact polynomial boost at its fixed half-angle parameter. -/
def sourceRationalBoost : Matrix (Fin 16) (Fin 16) ℚ :=
  1 + (1 / 40 : ℚ) • (sourceBoostGeneratorRat * sourceBoostGeneratorRat) +
      (9 / 40 : ℚ) • sourceBoostGeneratorRat

/-- Rational coefficients obey the Lorentz identity and the half-angle ratio.
The separate analytic identification with tanh and matrix exp is not asserted. -/
theorem sourceBoost_coefficients :
    (41 / 40 : ℚ) ^ 2 - (9 / 40 : ℚ) ^ 2 = 1 ∧
    (9 / 40 : ℚ) / (1 + 41 / 40) = 1 / 9 ∧
    (41 / 40 : ℚ) - 1 = 1 / 40 := by
  norm_num

/-- Exact original complex phase for each role under A,B,C,D → 0,2,3,1. -/
def sourceRolePhase (role : Role) : ℂ :=
  if role = A ∨ role = D then Complex.I else if role = B then -1 else -Complex.I

theorem sourceRolePhase_values :
    sourceRolePhase A = Complex.I ∧ sourceRolePhase D = Complex.I ∧
      sourceRolePhase B = -1 ∧ sourceRolePhase C = -Complex.I := by
  simp [sourceRolePhase, D0.A, D0.B, D0.C, D0.D]

def sourceCreatorComplex (role : Role) : Matrix (Fin 16) (Fin 16) ℂ :=
  (sourceCreatorMatrix role).map (Int.castRingHom ℂ)

/-- All four polynomial-fixture operands, with the actual Julia input order:
the boost is on the right of mode 1 and all four phases are retained. -/
noncomputable def sourcePolynomialOperand (role : Role) : Matrix (Fin 16) (Fin 16) ℂ :=
  sourceRolePhase role •
    (((3 / 5 : ℂ) • sourceCreatorComplex role) *
      (if role = D then sourceRationalBoost.map (Rat.castHom ℂ) else 1))

end D0.Geometry.OriginalBookBoost
