import Mathlib.Tactic
import D0.Core.DyadClosureForcing

/-!
# D0-TRIAD-COMPLEMENTARITY-001 — the trinary law the pairwise world cannot see

For N = 2 branches the whole complementarity house is the dyad bound `D² + V² ≤ 1`.  For
N = 3 there is NO consensus tight relation in the mainstream literature: naive pairwise
generalizations collapse (summing the three 2×2 principal-block bounds yields only the trivial
`tr ρ² ≤ 1`), and proposed trivariate inequalities conflict.  This module derives, from the
triad architecture alone, the genuinely trinary law.

**The triad record.**  Admissible = unit closure over three branches (`r11+r22+r33 = 1`) and
positive joint response — here the full 3×3 determinant condition

    det ≡ r11·r22·r33 + 2·r12·r23·r13 − r11·r23² − r22·r13² − r33·r12² ≥ 0,

which contains the cubic coupling `r12·r23·r13`: coherence of one pair multiplies coherence of
the other two.  Pairwise (2×2 principal) checks cannot see this term.

**Main theorem (magnitude form of the determinant constraint).**  Writing `t1 = |r23|`,
`t2 = |r13|`, `t3 = |r12|` (coherence of the pair OPPOSITE branch i) and `a=r11, b=r22, c=r33`:

    a·b·c + 2·t1·t2·t3  ≥  a·t1² + b·t2² + c·t3².

Proof: `det ≥ 0` gives `a·b·c + 2·r12·r23·r13 ≥ a·t1² + b·t2² + c·t3²` (squares equal absolute
squares); and `r12·r23·r13 ≥ −|r12·r23·r13| = −t1·t2·t3`; combine.  Pure real algebra — no
quantum postulates, same primitives as the whole dyad house.

**Tightness.**  The balanced coherent record `(all six entries = 1/3)` is admissible (`det = 0`,
rank-one/pure) and SATURATES the constraint exactly — the wave-mode extremum of the triad.

**Why this is the missing trinary law (honest scope).**  The constraint is a proved NECESSARY
condition cutting the joint region of the three pair-coherences `t1, t2, t3`; there exist
magnitude triples that pass EVERY pairwise 2×2 test while violating it (cert control C2), so its
content is irreducible to pairs.  Its operational identification — `t_ij` against the pairwise
fringe contrast of arms i,j in a triple-arm interferometer — inherits the apparatus bridge of
`D0-DYAD-FRINGE-BRIDGE-001`.  Whether the constraint is also SUFFICIENT (with phase choice) for
admissibility, and whether an experimentally tighter form exists, stay open targets; the
mainstream has neither agreed on a trivariate law nor closed this one out.
-/

namespace D0

/-- Admissible triad readout state: three branch weights with unit closure and positive joint
    response.  Positivity = Sylvester for the real symmetric 3×3: all THREE 2×2 principal
    minors plus the determinant (the cubic coupling lives here). -/
structure TriadState where
  r11 : ℝ
  r22 : ℝ
  r33 : ℝ
  r12 : ℝ
  r13 : ℝ
  r23 : ℝ
  htrace : r11 + r22 + r33 = 1
  hmin12 : 0 ≤ r11 * r22 - r12 ^ 2
  hmin13 : 0 ≤ r11 * r33 - r13 ^ 2
  hmin23 : 0 ≤ r22 * r33 - r23 ^ 2
  hdet : 0 ≤ r11 * r22 * r33 + 2 * r12 * r23 * r13
      - r11 * r23 ^ 2 - r22 * r13 ^ 2 - r33 * r12 ^ 2

/-- Coherence of the pair opposite branch 1 (arms 2–3). -/
def t1 (ρ : TriadState) : ℝ := |ρ.r23|

/-- Coherence of the pair opposite branch 2 (arms 1–3). -/
def t2 (ρ : TriadState) : ℝ := |ρ.r13|

/-- Coherence of the pair opposite branch 3 (arms 1–2). -/
def t3 (ρ : TriadState) : ℝ := |ρ.r12|

/-- **Trinary constraint (magnitude form).**  Every admissible triad record obeys
    `a·b·c + 2·t1·t2·t3 ≥ a·t1² + b·t2² + c·t3²`.  This is the determinant face of the
    admissible cone — the law invisible to pairwise checks. -/
theorem triad_constraint (ρ : TriadState) :
    ρ.r11 * ρ.r22 * ρ.r33 + 2 * t1 ρ * t2 ρ * t3 ρ
      ≥ ρ.r11 * t1 ρ ^ 2 + ρ.r22 * t2 ρ ^ 2 + ρ.r33 * t3 ρ ^ 2 := by
  unfold t1 t2 t3
  have hdet := ρ.hdet
  -- squares under absolutes are the raw squares
  have e1 : ρ.r11 * |ρ.r23| ^ 2 = ρ.r11 * ρ.r23 ^ 2 := by rw [sq_abs]
  have e2 : ρ.r22 * |ρ.r13| ^ 2 = ρ.r22 * ρ.r13 ^ 2 := by rw [sq_abs]
  have e3 : ρ.r33 * |ρ.r12| ^ 2 = ρ.r33 * ρ.r12 ^ 2 := by rw [sq_abs]
  -- the cubic term: product never exceeds its magnitude
  have hsign : 2 * ρ.r12 * ρ.r23 * ρ.r13
      ≤ 2 * |ρ.r23| * |ρ.r13| * |ρ.r12| := by
    have h0 := le_abs_self (ρ.r12 * ρ.r23 * ρ.r13)
    calc 2 * ρ.r12 * ρ.r23 * ρ.r13
        ≤ 2 * |ρ.r12 * ρ.r23 * ρ.r13| := by nlinarith
      _ = 2 * (|ρ.r12| * |ρ.r23| * |ρ.r13|) := by rw [abs_mul, abs_mul]
      _ = 2 * |ρ.r23| * |ρ.r13| * |ρ.r12| := by ring
  rw [e1, e2, e3]
  linarith

/-! ### Tightness: the balanced coherent record saturates the law -/

/-- Wave-mode extremum of the triad: the balanced coherent record (pure, rank one). -/
noncomputable def balancedTriad : TriadState :=
  ⟨1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num⟩

/-- The balanced coherent record sits exactly on the determinant face. -/
theorem balancedTriad_det_zero :
    balancedTriad.r11 * balancedTriad.r22 * balancedTriad.r33
      + 2 * balancedTriad.r12 * balancedTriad.r23 * balancedTriad.r13
      - balancedTriad.r11 * balancedTriad.r23 ^ 2
      - balancedTriad.r22 * balancedTriad.r13 ^ 2
      - balancedTriad.r33 * balancedTriad.r12 ^ 2 = 0 := by
  unfold balancedTriad
  norm_num

/-- **Saturation.**  The balanced coherent record attains equality in the trinary constraint —
    the constraint is tight, not slack. -/
theorem balancedTriad_saturates :
    balancedTriad.r11 * balancedTriad.r22 * balancedTriad.r33
      + 2 * t1 balancedTriad * t2 balancedTriad * t3 balancedTriad
      = balancedTriad.r11 * t1 balancedTriad ^ 2
        + balancedTriad.r22 * t2 balancedTriad ^ 2
        + balancedTriad.r33 * t3 balancedTriad ^ 2 := by
  unfold balancedTriad t1 t2 t3
  norm_num

end D0
