import Mathlib.Tactic
import Mathlib.Data.Fintype.Basic

namespace D0

inductive Part where
  | P9 | P11 | P13
  deriving DecidableEq, Repr, Fintype

def partSize : Part → ℕ
  | Part.P9 => 9
  | Part.P11 => 11
  | Part.P13 => 13

def numVertices : ℕ := 9 + 11 + 13
def numEdges : ℕ := 9 * 11 + 9 * 13 + 11 * 13
def numTriangles : ℕ := 9 * 11 * 13

theorem num_vertices : numVertices = 33 := by
  norm_num [numVertices]

theorem num_edges : numEdges = 359 := by
  norm_num [numEdges]

theorem num_triangles : numTriangles = 1287 := by
  norm_num [numTriangles]

theorem no_four_distinct_parts (a b c d : Part) :
    ¬ (a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ b ≠ c ∧ b ≠ d ∧ c ≠ d) := by
  native_decide +revert

end D0
