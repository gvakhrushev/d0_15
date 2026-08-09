import D0.Topology.GenericTripartiteDiscreteMorse
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-PERFECT-MORSE-001

The canonical root-lexicographic discrete Morse matching on
`K(p+1,q+1,r+1)` (built in `D0.Topology.GenericTripartiteDiscreteMorse`) is
already proved acyclic there.  This module proves the sharper statement that
it is a **perfect** discrete Morse function: the number of critical cells in
each degree equals the corresponding rational Betti number.

* the matching is *lacunary* — every critical cell has dimension `0` or `2`,
  never `1`;
* `c₀ = 1 = dim H₀`, `c₁ = 0 = dim H₁`, `c₂ = p*q*r = dim H₂`;
* the critical vector equals the Betti vector, and its alternating sum
  reproduces the Euler characteristic.

For this matching, critical cells occur only in dimensions `0` and `2`.  A
standard discrete Morse realization theorem would therefore give a CW complex
homotopy equivalent to `K(p+1,q+1,r+1)`, with one `0`-cell and `p*q*r`
`2`-cells.  Such a CW complex is a wedge of `p*q*r` two-spheres.  That
realization theorem is not yet available in Mathlib and is deliberately not
asserted here; this module supplies the exact combinatorial certificate
(perfect critical vector `(1, 0, p*q*r)`) that it would consume.
-/

namespace D0.Topology.GenericTripartiteDiscreteMorse
open D0.Topology.GenericTripartiteAbstractComplex
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing

namespace Face

variable {p q r : ℕ}

/-- Critical faces in dimension zero. -/
abbrev CriticalZeroFace (p q r : ℕ) :=
  {f : Face p q r // IsCritical f ∧ dimension f = 0}

/-- Critical faces in dimension one. -/
abbrev CriticalOneFace (p q r : ℕ) :=
  {f : Face p q r // IsCritical f ∧ dimension f = 1}

/-- Every critical face has dimension `0` or `2`; dimension `1` is skipped.
The canonical matching is *lacunary*. -/
theorem critical_dimension_lacunary (f : Face p q r) (hf : IsCritical f) :
    dimension f = 0 ∨ dimension f = 2 := by
  rcases (isCritical_iff f).mp hf with hroot | ⟨i, hi⟩
  · subst hroot; left; rfl
  · subst hi; right; rfl

/-- The unique critical `0`-face is the root. -/
def criticalZeroFaceMap : Unit → CriticalZeroFace p q r
  | _ => ⟨root, root_isCritical, rfl⟩

lemma criticalZeroFaceMap_bijective : Function.Bijective
    (criticalZeroFaceMap : Unit → CriticalZeroFace p q r) := by
  constructor
  · intro x y _; cases x; cases y; rfl
  · rintro ⟨f, hf, hdim⟩
    rcases (isCritical_iff f).mp hf with hroot | ⟨i, hi⟩
    · subst hroot; exact ⟨(), rfl⟩
    · subst hi; simp [dimension, criticalTriangle] at hdim

noncomputable def criticalZeroFaceEquiv :
    CriticalZeroFace p q r ≃ Unit :=
  (Equiv.ofBijective criticalZeroFaceMap criticalZeroFaceMap_bijective).symm

noncomputable instance criticalZeroFaceFintype :
    Fintype (CriticalZeroFace p q r) :=
  Fintype.ofFinite _

/-- No critical face has dimension one. -/
lemma criticalOneFace_isEmpty : IsEmpty (CriticalOneFace p q r) := by
  constructor
  rintro ⟨f, hf, hdim⟩
  rcases critical_dimension_lacunary f hf with h | h <;> rw [h] at hdim <;> simp_all

noncomputable instance criticalOneFaceFintype :
    Fintype (CriticalOneFace p q r) :=
  Fintype.ofFinite _

/-- Exact count of critical `0`-cells: a single root vertex. -/
theorem criticalZeroFace_card :
    Fintype.card (CriticalZeroFace p q r) = 1 := by
  rw [Fintype.card_congr (criticalZeroFaceEquiv (p:=p) (q:=q) (r:=r))]
  simp

/-- Exact count of critical `1`-cells: none. -/
theorem criticalOneFace_card :
    Fintype.card (CriticalOneFace p q r) = 0 := by
  haveI := criticalOneFace_isEmpty (p:=p) (q:=q) (r:=r)
  exact Fintype.card_eq_zero

/-- Degree-0 bridge: critical `0`-cell count equals `dim H₀ = 1`. -/
theorem criticalZeroFace_card_eq_H0_finrank :
    Fintype.card (CriticalZeroFace p q r) =
      Module.finrank ℚ
        ((GenericVertex p q r → ℚ) ⧸
          LinearMap.range (boundary1 (p:=p) (q:=q) (r:=r)).mulVecLin) := by
  rw [criticalZeroFace_card, boundary1_cokernel_finrank]

/-- Degree-1 bridge: critical `1`-cell count equals `dim H₁ = 0`. -/
theorem criticalOneFace_card_eq_H1_finrank :
    Fintype.card (CriticalOneFace p q r) =
      Module.finrank ℚ (FirstHomology (p:=p) (q:=q) (r:=r)) := by
  rw [criticalOneFace_card, first_homology_finrank]

/-- **Perfect discrete Morse count.** The critical-cell count in each degree
equals the corresponding rational Betti number. -/
theorem critical_card_eq_betti :
    (Fintype.card (CriticalZeroFace p q r),
     Fintype.card (CriticalOneFace p q r),
     Fintype.card (CriticalTwoFace p q r)) =
    (Module.finrank ℚ
        ((GenericVertex p q r → ℚ) ⧸
          LinearMap.range (boundary1 (p:=p) (q:=q) (r:=r)).mulVecLin),
     Module.finrank ℚ (FirstHomology (p:=p) (q:=q) (r:=r)),
     Module.finrank ℚ
        (LinearMap.ker (boundary2 (p:=p) (q:=q) (r:=r)).mulVecLin)) := by
  rw [criticalZeroFace_card_eq_H0_finrank,
      criticalOneFace_card_eq_H1_finrank,
      criticalTwoFace_card_eq_top_homology_finrank]

/-- Numeric form of perfectness: the critical vector is `(1, 0, p*q*r)`. -/
theorem critical_card_vector :
    (Fintype.card (CriticalZeroFace p q r),
     Fintype.card (CriticalOneFace p q r),
     Fintype.card (CriticalTwoFace p q r)) = (1, 0, p * q * r) := by
  rw [criticalZeroFace_card, criticalOneFace_card, criticalTwoFace_card]

/-- Morse–Euler consistency: the alternating sum of critical counts
reproduces the independently computed Euler characteristic `1 + p*q*r`. -/
theorem morse_euler_consistency :
    (Fintype.card (CriticalZeroFace p q r) : ℤ)
      - Fintype.card (CriticalOneFace p q r)
      + Fintype.card (CriticalTwoFace p q r)
      = eulerCharacteristic (p:=p) (q:=q) (r:=r) := by
  rw [criticalZeroFace_card, criticalOneFace_card, criticalTwoFace_card,
      euler_characteristic_formula]
  push_cast
  ring

/-- Scene specialization: the perfect critical vector is `(1, 0, 960)`. -/
theorem scene_critical_card_vector :
    (Fintype.card (CriticalZeroFace 8 10 12),
     Fintype.card (CriticalOneFace 8 10 12),
     Fintype.card (CriticalTwoFace 8 10 12)) = (1, 0, 960) := by
  simpa using critical_card_vector (p:=8) (q:=10) (r:=12)

end Face
end D0.Topology.GenericTripartiteDiscreteMorse
