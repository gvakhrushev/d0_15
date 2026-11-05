import D0.Geometry.OriginalBookWalsh
import Mathlib.Tactic
/-!
# Exact orthogonality of the original 32 Walsh signs

The OriginalBookWalsh.walshSign definition is the actual five-bit source
character for pinned uniform blob ee8de4635d24c668949ac9a0186616ab7d59f2ed,
lines 88-92, and modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a,
lines 160-174. Finite case proofs use kernel decide and no assumed
orthogonality. Operator Parseval and Kraus completeness are separate steps.
-/
open scoped BigOperators
open D0.Geometry.OriginalBookWalsh
namespace D0.Geometry.OriginalBookWalshOrthogonality

private theorem ortho0 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 0 * walshSign label k) = if (0 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho1 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 1 * walshSign label k) = if (1 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho2 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 2 * walshSign label k) = if (2 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho3 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 3 * walshSign label k) = if (3 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho4 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 4 * walshSign label k) = if (4 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho5 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 5 * walshSign label k) = if (5 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho6 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 6 * walshSign label k) = if (6 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho7 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 7 * walshSign label k) = if (7 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho8 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 8 * walshSign label k) = if (8 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho9 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 9 * walshSign label k) = if (9 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho10 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 10 * walshSign label k) = if (10 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho11 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 11 * walshSign label k) = if (11 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho12 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 12 * walshSign label k) = if (12 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho13 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 13 * walshSign label k) = if (13 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho14 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 14 * walshSign label k) = if (14 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho15 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 15 * walshSign label k) = if (15 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho16 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 16 * walshSign label k) = if (16 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho17 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 17 * walshSign label k) = if (17 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho18 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 18 * walshSign label k) = if (18 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho19 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 19 * walshSign label k) = if (19 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho20 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 20 * walshSign label k) = if (20 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho21 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 21 * walshSign label k) = if (21 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho22 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 22 * walshSign label k) = if (22 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho23 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 23 * walshSign label k) = if (23 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho24 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 24 * walshSign label k) = if (24 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho25 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 25 * walshSign label k) = if (25 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho26 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 26 * walshSign label k) = if (26 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho27 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 27 * walshSign label k) = if (27 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho28 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 28 * walshSign label k) = if (28 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho29 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 29 * walshSign label k) = if (29 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho30 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 30 * walshSign label k) = if (30 : Fin 32) = k then 32 else 0 := by
  decide

private theorem ortho31 : ∀ k : Fin 32, (∑ label : Fin 32, walshSign label 31 * walshSign label k) = if (31 : Fin 32) = k then 32 else 0 := by
  decide

theorem walsh_orthogonal (j k : Fin 32) :
    (∑ label : Fin 32, walshSign label j * walshSign label k) = if j = k then 32 else 0 := by
  fin_cases j
  · exact ortho0 k
  · exact ortho1 k
  · exact ortho2 k
  · exact ortho3 k
  · exact ortho4 k
  · exact ortho5 k
  · exact ortho6 k
  · exact ortho7 k
  · exact ortho8 k
  · exact ortho9 k
  · exact ortho10 k
  · exact ortho11 k
  · exact ortho12 k
  · exact ortho13 k
  · exact ortho14 k
  · exact ortho15 k
  · exact ortho16 k
  · exact ortho17 k
  · exact ortho18 k
  · exact ortho19 k
  · exact ortho20 k
  · exact ortho21 k
  · exact ortho22 k
  · exact ortho23 k
  · exact ortho24 k
  · exact ortho25 k
  · exact ortho26 k
  · exact ortho27 k
  · exact ortho28 k
  · exact ortho29 k
  · exact ortho30 k
  · exact ortho31 k


end D0.Geometry.OriginalBookWalshOrthogonality

