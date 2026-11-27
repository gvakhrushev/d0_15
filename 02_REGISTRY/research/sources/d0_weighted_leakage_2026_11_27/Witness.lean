import Mathlib.Tactic

namespace WeightedLeakageWitness

/-- Four vertices of a periodic two-by-two lattice, ordered by their two bits. -/
abbrev Sites := Fin 4
abbrev Field := Sites → ℤ

def xShift (i : Sites) : Sites := ![2, 3, 0, 1] i
def yShift (i : Sites) : Sites := ![1, 0, 3, 2] i
def dx (f : Field) (i : Sites) : ℤ := f (xShift i) - f i
def dy (f : Field) (i : Sites) : ℤ := f (yShift i) - f i
def d0 (f : Field) : Field × Field := (dx f, dy f)
def d1 (a : Field × Field) (i : Sites) : ℤ := dx a.2 i - dy a.1 i

/-- The positive multiplier is the square root of the weight `(1,1,4,4)`. -/
def weight (i : Sites) : ℤ := ![1, 1, 2, 2] i
def weightedD0 (f : Field) : Field × Field :=
  (fun i => weight i * (d0 f).1 i, fun i => weight i * (d0 f).2 i)
def weightedD1 (a : Field × Field) (i : Sites) : ℤ := weight i * d1 a i
def probe (i : Sites) : ℤ := if i = 2 then 1 else 0

theorem unweighted_is_nilpotent (f : Field) (i : Sites) : d1 (d0 f) i = 0 := by
  fin_cases i <;> simp [d1, d0, dx, dy, xShift, yShift] <;> ring

/-- A particular weighted composition has a nonzero 0-to-2 component. -/
theorem weighted_square_witness : weightedD1 (weightedD0 probe) 0 = -1 := by
  decide

end WeightedLeakageWitness
