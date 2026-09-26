import Mathlib.Tactic
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Order.Ring.Abs

/-!
# Checkerboard nonlinear obstruction (finite L=2 Lorentz-null sectors)

Owns the real-quadratic core of the exact second-order Lyapunov–Schmidt
obstruction for the three nonzero Lorentz-null period-two checkerboard
sectors of the accepted flat A4D star Hessian (merged #199/#200 packet;
certificate
`02_REGISTRY/research/certificates/a4d_checkerboard_nonlinear_obstruction_check.py`).

## Owned packet

After quotienting the ten accepted flat gauge directions, each of the three
characters

* `(-1,-1,+1,+1)`,
* `(-1,+1,-1,+1)`,
* `(-1,+1,+1,-1)`

carries a two-dimensional physical null plane.  On any exact basis `(u,v)` of
that plane, and for the fixed zero-momentum constant-solder kernel direction
`w0` (`δ v_A^A = 1`), the cubic action tensor of the finite star density
evaluates to the diagonal obstruction form

```
T(u,u,w0) = -32/3,   T(v,v,w0) = -32/3,   T(u,v,w0) = 0.
```

Consequently every physical first-order combination `z₁ = a u + b v` has

```
T(z₁, z₁, w0) = -(32/3) (a² + b²),
```

which vanishes over `ℝ` if and only if `a = b = 0`.

## Witness / basis path (not the 40-variable cubic)

Reconstructing the full 40-component cubic coefficient of the 16-site action
inside Lean is deliberately out of scope.  Instead this module:

1. packages the three sector characters as an explicit finite enumeration;
2. packages the certified diagonal coefficients as a typed witness structure
   (no `axiom`);
3. Lean-owns the finite real algebra from those coefficients to the vanishing
   criterion.

The numerical identity of the witness coefficients with the cubic `T` of the
accepted star action is the **explicit** finite SymPy enumeration in the
certificate above (PASS checks `CUBIC_OBSTRUCTION_Q11_*`,
`CUBIC_OBSTRUCTION_Q22_*`, `CUBIC_OBSTRUCTION_Q12_ZERO_*` on each sector).
That enumeration is not re-imported as a Lean axiom and is not claimed as a
Lean theorem here.

## Scope

Local near the canonical flat solder; finite `L=2` only.  Does **not**
exclude disconnected curved stationary points (EXP #202 searches that sector).
Does **not** call these modes waves or physical time.  Does **not** claim a
no-go for every curved stationary solution, every constant-solder background,
or every later affine-completed action.

Zero `sorry`.
-/

namespace D0.Geometry

set_option linter.unusedSimpArgs false

/-! ## Sector characters (explicit finite enumeration) -/

/-- Sign pattern of one period-two Lorentz-null checkerboard sector.
Values are required to be `±1` on each of the four roles. -/
structure CheckerboardNullCharacter where
  /-- Role-wise sign (`±1`). -/
  sign : Fin 4 → ℤ
  /-- Each coordinate is exactly `±1`. -/
  is_unit_sign : ∀ i, sign i = 1 ∨ sign i = -1

namespace CheckerboardNullCharacter

/-- First Lorentz-null L=2 character `(-1,-1,+1,+1)`. -/
def sectorMMPP : CheckerboardNullCharacter where
  sign
    | 0 => -1
    | 1 => -1
    | 2 => 1
    | 3 => 1
  is_unit_sign i := by
    fin_cases i <;> simp

/-- Second Lorentz-null L=2 character `(-1,+1,-1,+1)`. -/
def sectorMPMP : CheckerboardNullCharacter where
  sign
    | 0 => -1
    | 1 => 1
    | 2 => -1
    | 3 => 1
  is_unit_sign i := by
    fin_cases i <;> simp

/-- Third Lorentz-null L=2 character `(-1,+1,+1,-1)`. -/
def sectorMPPM : CheckerboardNullCharacter where
  sign
    | 0 => -1
    | 1 => 1
    | 2 => 1
    | 3 => -1
  is_unit_sign i := by
    fin_cases i <;> simp

/-- The three nonzero Lorentz-null L=2 checkerboard sectors, enumerated
explicitly. -/
def allNullSectors : List CheckerboardNullCharacter :=
  [sectorMMPP, sectorMPMP, sectorMPPM]

theorem allNullSectors_length : allNullSectors.length = 3 := rfl

theorem allNullSectors_nodup_signs :
    (allNullSectors.map (fun s => (s.sign 0, s.sign 1, s.sign 2, s.sign 3))).Nodup := by
  native_decide

end CheckerboardNullCharacter

/-! ## Typed obstruction witness (certificate coefficients, not axioms) -/

/-- Certified cubic obstruction coefficients on one physical null-plane basis
`(u,v)` relative to the fixed zero-momentum solder kernel direction `w0`.

The fields `q11`, `q22`, `q12` are ordinary definitions equal to the certificate
values `-32/3`, `-32/3`, `0`.  They are **not** Lean axioms: the claim that
these numbers equal the cubic `T` of the accepted star action on that sector
is the explicit finite enumeration outside this module. -/
structure CheckerboardObstructionWitness where
  /-- Sector character carrying the physical null plane. -/
  sector : CheckerboardNullCharacter
  /-- `T(u,u,w0)`. -/
  q11 : ℚ := -32 / 3
  /-- `T(v,v,w0)`. -/
  q22 : ℚ := -32 / 3
  /-- `T(u,v,w0)`. -/
  q12 : ℚ := 0

namespace CheckerboardObstructionWitness

/-- Canonical witness for one sector: the certificate diagonal form. -/
def canonical (sector : CheckerboardNullCharacter) : CheckerboardObstructionWitness where
  sector := sector
  q11 := -32 / 3
  q22 := -32 / 3
  q12 := 0

theorem canonical_q11 (s : CheckerboardNullCharacter) :
    (canonical s).q11 = -32 / 3 := rfl

theorem canonical_q22 (s : CheckerboardNullCharacter) :
    (canonical s).q22 = -32 / 3 := rfl

theorem canonical_q12 (s : CheckerboardNullCharacter) :
    (canonical s).q12 = 0 := rfl

/-- Explicit finite list of the three canonical sector witnesses. -/
def allCanonical : List CheckerboardObstructionWitness :=
  CheckerboardNullCharacter.allNullSectors.map canonical

theorem allCanonical_length : allCanonical.length = 3 := rfl

theorem allCanonical_q11 (W : CheckerboardObstructionWitness) (h : W ∈ allCanonical) :
    W.q11 = -32 / 3 := by
  simp [allCanonical, CheckerboardNullCharacter.allNullSectors, canonical] at h
  rcases h with h | h | h <;> subst h <;> rfl

theorem allCanonical_q22 (W : CheckerboardObstructionWitness) (h : W ∈ allCanonical) :
    W.q22 = -32 / 3 := by
  simp [allCanonical, CheckerboardNullCharacter.allNullSectors, canonical] at h
  rcases h with h | h | h <;> subst h <;> rfl

theorem allCanonical_q12 (W : CheckerboardObstructionWitness) (h : W ∈ allCanonical) :
    W.q12 = 0 := by
  simp [allCanonical, CheckerboardNullCharacter.allNullSectors, canonical] at h
  rcases h with h | h | h <;> subst h <;> rfl

end CheckerboardObstructionWitness

/-! ## Real quadratic obstruction form -/

/-- Polarized quadratic obstruction on amplitudes `(a,b)` of `z₁ = a u + b v`:

`Q(a,b) = q11 a² + 2 q12 a b + q22 b²`. -/
def checkerboardObstructionQuadratic (W : CheckerboardObstructionWitness) (a b : ℝ) : ℝ :=
  (W.q11 : ℝ) * a ^ 2 + 2 * (W.q12 : ℝ) * a * b + (W.q22 : ℝ) * b ^ 2

/-- On every canonical witness the obstruction collapses to `-(32/3)(a²+b²)`. -/
theorem checkerboardObstructionQuadratic_canonical
    (s : CheckerboardNullCharacter) (a b : ℝ) :
    checkerboardObstructionQuadratic (CheckerboardObstructionWitness.canonical s) a b =
      -(32 / 3 : ℝ) * (a ^ 2 + b ^ 2) := by
  simp [checkerboardObstructionQuadratic, CheckerboardObstructionWitness.canonical]
  ring

/-- Same identity for every witness in the explicit three-sector list. -/
theorem checkerboardObstructionQuadratic_allCanonical
    (W : CheckerboardObstructionWitness) (h : W ∈ CheckerboardObstructionWitness.allCanonical)
    (a b : ℝ) :
    checkerboardObstructionQuadratic W a b = -(32 / 3 : ℝ) * (a ^ 2 + b ^ 2) := by
  simp [CheckerboardObstructionWitness.allCanonical,
    CheckerboardNullCharacter.allNullSectors] at h
  rcases h with h | h | h
  · subst h; exact checkerboardObstructionQuadratic_canonical _ a b
  · subst h; exact checkerboardObstructionQuadratic_canonical _ a b
  · subst h; exact checkerboardObstructionQuadratic_canonical _ a b

/-! ## Vanishing over the reals iff `a = b = 0` -/

/-- Core finite algebra: `-(32/3)(a²+b²) = 0` over `ℝ` iff `a = b = 0`. -/
theorem checkerboard_obstruction_core_vanishes_iff (a b : ℝ) :
    -(32 / 3 : ℝ) * (a ^ 2 + b ^ 2) = 0 ↔ a = 0 ∧ b = 0 := by
  constructor
  · intro h
    have hcoeff : (32 / 3 : ℝ) ≠ 0 := by norm_num
    have hsum : a ^ 2 + b ^ 2 = 0 := by
      have := mul_eq_zero.mp h
      cases this with
      | inl hneg =>
          exact absurd hneg (neg_ne_zero.mpr hcoeff)
      | inr hsq =>
          exact hsq
    have ha : a = 0 := by
      have : a ^ 2 = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, hsum]
      exact (sq_eq_zero_iff.mp this)
    have hb : b = 0 := by
      have : b ^ 2 = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, hsum]
      exact (sq_eq_zero_iff.mp this)
    exact ⟨ha, hb⟩
  · rintro ⟨rfl, rfl⟩
    simp

/-- On a canonical sector witness, the obstruction vanishes iff the physical
amplitudes vanish. -/
theorem checkerboardObstructionQuadratic_canonical_eq_zero_iff
    (s : CheckerboardNullCharacter) (a b : ℝ) :
    checkerboardObstructionQuadratic (CheckerboardObstructionWitness.canonical s) a b = 0 ↔
      a = 0 ∧ b = 0 := by
  rw [checkerboardObstructionQuadratic_canonical, checkerboard_obstruction_core_vanishes_iff]

/-- Same vanishing criterion on every witness of the explicit three-sector list. -/
theorem checkerboardObstructionQuadratic_allCanonical_eq_zero_iff
    (W : CheckerboardObstructionWitness) (h : W ∈ CheckerboardObstructionWitness.allCanonical)
    (a b : ℝ) :
    checkerboardObstructionQuadratic W a b = 0 ↔ a = 0 ∧ b = 0 := by
  rw [checkerboardObstructionQuadratic_allCanonical W h a b,
    checkerboard_obstruction_core_vanishes_iff]

/-- Packaged theorem: every nonzero real combination in each of the three
canonical L=2 Lorentz-null physical null planes is obstructed. -/
theorem checkerboard_physical_null_plane_obstructed
    (W : CheckerboardObstructionWitness) (h : W ∈ CheckerboardObstructionWitness.allCanonical)
    (a b : ℝ) (hne : ¬ (a = 0 ∧ b = 0)) :
    checkerboardObstructionQuadratic W a b ≠ 0 := by
  intro hz
  exact hne ((checkerboardObstructionQuadratic_allCanonical_eq_zero_iff W h a b).mp hz)

/-- Convenience: the three sector witnesses share the same diagonal obstruction
constant `-32/3`. -/
theorem checkerboard_obstruction_constant :
    ∀ W ∈ CheckerboardObstructionWitness.allCanonical,
      W.q11 = -32 / 3 ∧ W.q22 = -32 / 3 ∧ W.q12 = 0 := by
  intro W h
  exact ⟨CheckerboardObstructionWitness.allCanonical_q11 W h,
    CheckerboardObstructionWitness.allCanonical_q22 W h,
    CheckerboardObstructionWitness.allCanonical_q12 W h⟩

end D0.Geometry
