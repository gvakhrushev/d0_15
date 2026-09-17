import D0.Synthesis.Edge359SceneSelectionBoundary

/-!
# Scene over-determination: no single count pins the scene, any two do

`D0-EDGE359-SCENE-SELECTION-NOGO-001` showed the edge count `359` alone does not select the
scene. This module places that fact in its exact context and turns the "is the scene
hand-picked?" objection into a theorem.

For the ordered tripartite invariants

`V = a+b+c`, `E = ab+ac+bc`, `T = abc`,

the source scene has `(V,E,T) = (33, 359, 1287)`. Complete enumeration shows:

* **no single invariant is selective** — `V=33` has 91 ordered solutions, `E=359` has 19,
  `T=1287` has 10; each is exhibited with an explicit second witness here;
* **every pair is selective** — `(V,E)`, `(V,T)` and `(E,T)` each force `(9,11,13)` uniquely.

So the scene is over-determined: it is the unique common solution of any two independent count
readings, and no reading is individually load-bearing. This is robustness against a single
cherry-picked invariant, not a coincidence of one number.
-/

namespace D0.Synthesis.SceneInvariantOverdetermination

open D0.Synthesis.TransportSpectrumBlindness
open D0.Synthesis.Edge359SceneSelectionBoundary

/-- The source scene invariants. -/
theorem source_invariants :
    V 9 11 13 = 33 ∧ E 9 11 13 = 359 ∧ T 9 11 13 = 1287 := by decide

/-- `V = 33` is not selective: a second ordered triple realizes it. -/
theorem vertex_not_selective :
    V 9 11 13 = 33 ∧ V 1 1 31 = 33 ∧ (1, 1, 31) ≠ (9, 11, 13) := by decide

/-- `E = 359` is not selective (the explicit `(7,10,17)` rival). -/
theorem edge_not_selective :
    E 9 11 13 = 359 ∧ E 7 10 17 = 359 ∧ (7, 10, 17) ≠ (9, 11, 13) := by decide

/-- `T = 1287` is not selective: a second ordered triple realizes it. -/
theorem triangle_not_selective :
    T 9 11 13 = 1287 ∧ T 1 1 1287 = 1287 ∧ (1, 1, 1287) ≠ (9, 11, 13) := by decide

/-- **Pair (V,E) is selective** (re-exported from the edge-selection boundary). -/
theorem vertex_edge_selective
    (a b c : ℕ) (hab : a ≤ b) (hbc : b ≤ c)
    (hV : V a b c = 33) (hE : E a b c = 359) :
    (a, b, c) = (9, 11, 13) :=
  scene_unique_from_vertex_and_edge a b c hab hbc hV hE

/-- **Pair (V,T) is selective.** Vertex count `33` and triangle count `1287` force the scene. -/
theorem vertex_triangle_selective
    (a b c : ℕ) (hab : a ≤ b) (hbc : b ≤ c)
    (hV : V a b c = 33) (hT : T a b c = 1287) :
    (a, b, c) = (9, 11, 13) := by
  simp only [V] at hV
  simp only [T] at hT
  have ha : a ≤ 33 := by omega
  have hb : b ≤ 33 := by omega
  have hcomp : a = 9 ∧ b = 11 ∧ c = 13 := by
    interval_cases a <;> interval_cases b <;> omega
  obtain ⟨rfl, rfl, rfl⟩ := hcomp
  rfl

/-- **Pair (E,T) is selective.** Edge count `359` and triangle count `1287` force the scene. -/
theorem edge_triangle_selective
    (a b c : ℕ) (ha1 : 1 ≤ a) (hab : a ≤ b) (hbc : b ≤ c)
    (hE : E a b c = 359) (hT : T a b c = 1287) :
    (a, b, c) = (9, 11, 13) := by
  simp only [E] at hE
  simp only [T] at hT
  have hb1 : 1 ≤ b := le_trans ha1 hab
  have hc1 : 1 ≤ c := le_trans hb1 hbc
  -- a³ ≤ abc = 1287 and b² ≤ bc ≤ abc = 1287 give finite ranges.
  have hac : a ≤ c := le_trans hab hbc
  have ha_cube : a * a * a ≤ 1287 := by
    calc a * a * a ≤ a * b * c := by
          have h1 : a * a ≤ a * b := Nat.mul_le_mul_left a hab
          have h2 : a * a * a ≤ a * b * a := Nat.mul_le_mul_right a h1
          calc a * a * a ≤ a * b * a := h2
            _ ≤ a * b * c := Nat.mul_le_mul_left (a * b) hac
      _ = 1287 := hT
  have hb_sq : b * b ≤ 1287 := by
    calc b * b ≤ b * c := Nat.mul_le_mul_left b hbc
      _ ≤ a * (b * c) := Nat.le_mul_of_pos_left (b * c) ha1
      _ = a * b * c := by ring
      _ = 1287 := hT
  have ha : a ≤ 10 := by nlinarith
  have hb : b ≤ 35 := by nlinarith
  have hcomp : a = 9 ∧ b = 11 ∧ c = 13 := by
    interval_cases a <;> interval_cases b <;> omega
  obtain ⟨rfl, rfl, rfl⟩ := hcomp
  rfl

/-- **Over-determination capstone.** No single count selects the scene, yet each of the three
pairs `(V,E)`, `(V,T)`, `(E,T)` selects `(9,11,13)` uniquely. -/
theorem scene_invariant_overdetermination :
    (V 9 11 13 = 33 ∧ V 1 1 31 = 33 ∧ (1, 1, 31) ≠ (9, 11, 13))
    ∧ (E 9 11 13 = 359 ∧ E 7 10 17 = 359 ∧ (7, 10, 17) ≠ (9, 11, 13))
    ∧ (T 9 11 13 = 1287 ∧ T 1 1 1287 = 1287 ∧ (1, 1, 1287) ≠ (9, 11, 13))
    ∧ (∀ a b c : ℕ, a ≤ b → b ≤ c → V a b c = 33 → E a b c = 359 → (a, b, c) = (9, 11, 13))
    ∧ (∀ a b c : ℕ, a ≤ b → b ≤ c → V a b c = 33 → T a b c = 1287 → (a, b, c) = (9, 11, 13))
    ∧ (∀ a b c : ℕ, 1 ≤ a → a ≤ b → b ≤ c → E a b c = 359 → T a b c = 1287 →
        (a, b, c) = (9, 11, 13)) :=
  ⟨vertex_not_selective, edge_not_selective, triangle_not_selective,
    vertex_edge_selective, vertex_triangle_selective, edge_triangle_selective⟩

end D0.Synthesis.SceneInvariantOverdetermination
