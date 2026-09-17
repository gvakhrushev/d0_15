import D0.Synthesis.TransportSpectrumBlindness

/-!
# Edge count 359 does not select the scene; `(V,E)=(33,359)` does

The D0 alpha-leading expression consumes the scene edge count `359`. This module tests the
stronger reading sometimes suggested by the prose: could `359` itself independently select the
scene `K(9,11,13)`?

No. The complete-tripartite scenes `(9,11,13)` and `(7,10,17)` both have exactly `359` edges,
while their vertex and triangle counts differ. Thus any selector factoring only through the edge
count — including an expression that merely reuses that count — is blind to the scene.

The sharp positive boundary is also proved. Among ordered natural triples, the pair

`V=a+b+c=33`, `E=ab+ac+bc=359`

has the unique solution `(9,11,13)`. Hence one independent scalar beyond `E` is sufficient:
vertex count repairs the ambiguity. The edge count is a valid cross-sector invariant *after* the
scene is selected, but it is not an independent scene-selection theorem.
-/

namespace D0.Synthesis.Edge359SceneSelectionBoundary

open D0.Synthesis.TransportSpectrumBlindness

/-- The source scene has edge count `359`, vertex count `33`, triangle count `1287`. -/
theorem source_scene_counts :
    E 9 11 13 = 359 ∧ V 9 11 13 = 33 ∧ T 9 11 13 = 1287 := by
  decide

/-- A concrete rival scene with the same edge count but different vertex and triangle counts. -/
theorem edge359_rival_counts :
    E 7 10 17 = 359 ∧ V 7 10 17 = 34 ∧ T 7 10 17 = 1190 := by
  decide

/-- The rival is genuinely distinct from the source scene. -/
theorem edge359_rival_ne_source :
    (7, 10, 17) ≠ (9, 11, 13) := by decide

/-- **Edge-only scene selection fails.** Two distinct ordered positive triples have the same
complete-tripartite edge count `359`. -/
theorem edge359_not_scene_injective :
    ∃ a b c a' b' c' : ℕ,
      1 ≤ a ∧ a ≤ b ∧ b ≤ c
      ∧ 1 ≤ a' ∧ a' ≤ b' ∧ b' ≤ c'
      ∧ E a b c = 359 ∧ E a' b' c' = 359
      ∧ (a, b, c) ≠ (a', b', c') :=
  ⟨9, 11, 13, 7, 10, 17, by decide, by decide, by decide,
    by decide, by decide, by decide, by decide, by decide, by decide⟩

/-- An edge-only predicate cannot distinguish the source scene from the explicit rival. -/
def FactorsThroughEdgeCount
    (select : ℕ × ℕ × ℕ → Prop) : Prop :=
  ∀ x y,
    E x.1 x.2.1 x.2.2 = E y.1 y.2.1 y.2.2 →
    (select x ↔ select y)

/-- Any edge-count-only selector that accepts the source must also accept the rival. -/
theorem edgeOnlySelector_accepts_rival
    (select : ℕ × ℕ × ℕ → Prop)
    (hfactor : FactorsThroughEdgeCount select)
    (hsource : select (9, 11, 13)) :
    select (7, 10, 17) := by
  apply (hfactor (9, 11, 13) (7, 10, 17) (by decide)).mp
  exact hsource

/-- **Positive repair.** Among ordered natural triples, vertex count `33` together with edge
count `359` uniquely determines `(9,11,13)`. -/
theorem scene_unique_from_vertex_and_edge
    (a b c : ℕ)
    (hab : a ≤ b) (hbc : b ≤ c)
    (hV : V a b c = 33)
    (hE : E a b c = 359) :
    (a, b, c) = (9, 11, 13) := by
  simp only [V] at hV
  simp only [E] at hE
  have ha : a ≤ 33 := by omega
  have hb : b ≤ 33 := by omega
  interval_cases a <;> interval_cases b <;>
    (try norm_num at hV hE ⊢) <;> omega

/-- The `(V,E)` repair is non-vacuous at the source scene. -/
theorem source_scene_realizes_vertex_and_edge :
    V 9 11 13 = 33 ∧ E 9 11 13 = 359 := by decide

/-- Capstone: `E=359` alone is blind, while the minimal two-coordinate reading `(V,E)` pins the
ordered tripartite scene. -/
theorem edge359_scene_selection_boundary :
    E 9 11 13 = E 7 10 17
      ∧ (9, 11, 13) ≠ (7, 10, 17)
      ∧ V 9 11 13 ≠ V 7 10 17
      ∧ T 9 11 13 ≠ T 7 10 17
      ∧ (∀ a b c : ℕ, a ≤ b → b ≤ c →
          V a b c = 33 → E a b c = 359 →
          (a, b, c) = (9, 11, 13)) :=
  ⟨by decide, by decide, by decide, by decide, scene_unique_from_vertex_and_edge⟩

end D0.Synthesis.Edge359SceneSelectionBoundary
