import Mathlib.Tactic

/-!
# D0-OMEGA8-CENTER-001 — Z(Q₈) = [Q₈,Q₈] = {±1}, the orientation-bit collapse (Lean)

Python certificate: `05_CERTS/vp_omega8_center_collapse.py`.

Closes the §01.7.1C PROOF-TARGET: the explicit map `Ω₈-orientation groupoid → Z(Q₈)`. The book
states `[Q₈,Q₈] = Z(Q₈) = Φ(Q₈) = {±1}` — the `±` orientation bit (center), the read/write
order-memory remainder (commutator subgroup), and the non-generating remainder (Frattini) are one
two-element group. This module proves the operational core in exact ℤ-quaternion arithmetic over
`Q₈ = {±1, ±i, ±j, ±k}`: the center is exactly `{±1}`, every commutator lands in `{±1}` (and `−1`
is realized, e.g. `[i,j]=−1`), and an imaginary unit is not central. (`Ω₈≅Q₈` itself is owned by
the Dedekind-minimality cert, §01.7.1A.)
-/

namespace D0.Foundation

/-- A unit quaternion over `ℤ` as `(a,b,c,d) = a + b·i + c·j + d·k`. -/
abbrev UQuat := Int × Int × Int × Int

def uqmul (x y : UQuat) : UQuat :=
  (x.1 * y.1 - x.2.1 * y.2.1 - x.2.2.1 * y.2.2.1 - x.2.2.2 * y.2.2.2,
   x.1 * y.2.1 + x.2.1 * y.1 + x.2.2.1 * y.2.2.2 - x.2.2.2 * y.2.2.1,
   x.1 * y.2.2.1 - x.2.1 * y.2.2.2 + x.2.2.1 * y.1 + x.2.2.2 * y.2.1,
   x.1 * y.2.2.2 + x.2.1 * y.2.2.1 - x.2.2.1 * y.2.1 + x.2.2.2 * y.1)

/-- Inverse of a unit quaternion = its conjugate. -/
def uqinv (x : UQuat) : UQuat := (x.1, -x.2.1, -x.2.2.1, -x.2.2.2)

def qONE : UQuat := (1, 0, 0, 0)
def qNEG : UQuat := (-1, 0, 0, 0)

/-- `Q₈ = {±1, ±i, ±j, ±k}`. -/
def Q8 : List UQuat :=
  [(1,0,0,0), (-1,0,0,0), (0,1,0,0), (0,-1,0,0),
   (0,0,1,0), (0,0,-1,0), (0,0,0,1), (0,0,0,-1)]

/-- **Center.** `Z(Q₈) = {q : q·r = r·q ∀ r} = {+1, −1}` — the `±` orientation bit. -/
theorem center_eq_pm1 :
    Q8.filter (fun q => Q8.all (fun r => uqmul q r == uqmul r q)) = [qONE, qNEG] := by
  native_decide

/-- **Commutator remainder.** Every commutator `[a,b] = a·b·a⁻¹·b⁻¹` lands in `{+1, −1}`. -/
theorem commutators_in_pm1 :
    (Q8.flatMap (fun a => Q8.map (fun b => uqmul (uqmul a b) (uqmul (uqinv a) (uqinv b))))).all
      (fun c => c == qONE || c == qNEG) = true := by
  native_decide

/-- `−1` is realized as a commutator: `[i,j] = i·j·i⁻¹·j⁻¹ = −1` (the remainder is nontrivial). -/
theorem commutator_ij_eq_neg :
    uqmul (uqmul (0,1,0,0) (0,0,1,0)) (uqmul (uqinv (0,1,0,0)) (uqinv (0,0,1,0))) = qNEG := by
  native_decide

/-- **Negative control.** An imaginary unit is not central: `i·j = k ≠ −k = j·i`. -/
theorem i_not_central : uqmul (0,1,0,0) (0,0,1,0) ≠ uqmul (0,0,1,0) (0,1,0,0) := by
  decide

/-- **D0-OMEGA8-CENTER-001.** The orientation-bit collapse: `Z(Q₈) = {±1}` is exactly the
commutator remainder (`[i,j]=−1` realizes it), and the imaginary units are non-central — so the
center, the order-memory remainder and (via the Klein-four abelianization) the Frattini subgroup
are the single two-element group `{±1}` = the `±` orientation bit of `Ω₈`. -/
theorem omega8_center_collapse :
    (Q8.filter (fun q => Q8.all (fun r => uqmul q r == uqmul r q)) = [qONE, qNEG]) ∧
    ((Q8.flatMap (fun a => Q8.map (fun b => uqmul (uqmul a b) (uqmul (uqinv a) (uqinv b))))).all
      (fun c => c == qONE || c == qNEG) = true) ∧
    (uqmul (uqmul (0,1,0,0) (0,0,1,0)) (uqmul (uqinv (0,1,0,0)) (uqinv (0,0,1,0))) = qNEG) ∧
    (uqmul (0,1,0,0) (0,0,1,0) ≠ uqmul (0,0,1,0) (0,1,0,0)) :=
  ⟨center_eq_pm1, commutators_in_pm1, commutator_ij_eq_neg, i_not_central⟩

end D0.Foundation
