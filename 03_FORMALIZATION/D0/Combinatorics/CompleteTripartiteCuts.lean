import Mathlib.Tactic

/-!
# CompleteTripartiteCuts

data fixture for future cut-pairing lemma
-/

namespace D0

/-- Number of vertices of `K(p,q,r)`. -/
def V (p q r : ℕ) := p + q + r

/-- Number of edges of `K(p,q,r)`. -/
def E (p q r : ℕ) := p * q + p * r + q * r

/-- Number of triangles of `K(p,q,r)`. -/
def T (p q r : ℕ) := p * q * r

/-- Cut size opposite the first part (not incident to it). -/
def oppositeCutP (p q r : ℕ) := q * r

/-- Cut size opposite the second part. -/
def oppositeCutQ (p q r : ℕ) := p * r

/-- Cut size opposite the third part. -/
def oppositeCutR (p q r : ℕ) := p * q

/-- Dimension of the balanced (zero-sum) space on a part of size `n`. -/
def balancedDim (n : ℕ) := n - 1

/-- Scene checks for `(p,q,r) = (9,11,13)`. -/
lemma checks_9_11_13 :
    V 9 11 13 = 33 ∧
    E 9 11 13 = 359 ∧
    T 9 11 13 = 1287 ∧
    oppositeCutP 9 11 13 = 143 ∧
    oppositeCutQ 9 11 13 = 117 ∧
    oppositeCutR 9 11 13 = 99 ∧
    balancedDim 9 = 8 ∧
    balancedDim 11 = 10 ∧
    balancedDim 13 = 12 := by
  native_decide

/-- Twin triples from the TopHodge docstring, as data only. -/
def twinList : List (ℕ × ℕ × ℕ) :=
  [(2, 6, 6), (3, 3, 8), (2, 15, 15), (3, 3, 50), (3, 17, 22), (4, 8, 33)]

/-- Formula control on one twin: `K(2,6,6)` opposite cuts. -/
lemma oppositeCuts_2_6_6 :
    oppositeCutP 2 6 6 = 36 ∧
    oppositeCutQ 2 6 6 = 12 ∧
    oppositeCutR 2 6 6 = 12 := by
  native_decide

end D0
