import D0.Geometry.OriginalBookWalsh
import Mathlib.Tactic

/-!
# The original Golden 128 Kraus matrices

The original uniform source, blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed`,
lines 16 and 94–100, and the modular checker, blob
`d111c5bfeae3c384a4fe725f4a6d19277ea0005a`, lines 174–182, both at commit
eebcb5e467742df3e9cf7fa9702042d7294aa742, prescribe this ordered family.
It is built from the actual source Walsh rows. This definition does not assert
CPTP, completeness, span, physical admission, or nonzero remaining slots.
-/

open D0.Geometry.OriginalBookJuliaWords
open D0.Geometry.OriginalBookWalsh
open Matrix
open scoped BigOperators

namespace D0.Geometry.OriginalBookGoldenKraus

/-- The original inverse Golden ratio, not the Golden ratio itself. -/
noncomputable def goldenP : ℝ := (Real.sqrt 5 - 1) / 2

lemma goldenP_pos : 0 < goldenP := by
  have h := Real.sq_sqrt (show (0 : ℝ) ≤ 5 by norm_num)
  have hnonneg := Real.sqrt_nonneg 5
  unfold goldenP
  nlinarith

lemma goldenP_lt_one : goldenP < 1 := by
  have h := Real.sq_sqrt (show (0 : ℝ) ≤ 5 by norm_num)
  have hnonneg := Real.sqrt_nonneg 5
  unfold goldenP
  nlinarith

lemma goldenP_equation : goldenP ^ 2 + goldenP = 1 := by
  have h := Real.sq_sqrt (show (0 : ℝ) ≤ 5 by norm_num)
  unfold goldenP
  nlinarith

lemma goldenRoot_sq : (Real.sqrt goldenP) ^ 2 = goldenP :=
  Real.sq_sqrt (le_of_lt goldenP_pos)

/-- Source flattening `2*row + port` of 64 rows and two fine ports. -/
def krausIndex (row : Fin 64) (port : Fin 2) : Fin 128 :=
  ⟨2 * row.val + port.val, by omega⟩

def krausRow (slot : Fin 128) : Fin 64 := ⟨slot.val / 2, by omega⟩
def krausPort (slot : Fin 128) : Fin 2 := ⟨slot.val % 2, by omega⟩

lemma krausIndex_coordinates (row : Fin 64) (port : Fin 2) :
    krausRow (krausIndex row port) = row ∧ krausPort (krausIndex row port) = port := by
  constructor <;> apply Fin.ext <;> simp [krausRow, krausPort, krausIndex] <;> omega

lemma krausIndex_reconstruct (slot : Fin 128) :
    krausIndex (krausRow slot) (krausPort slot) = slot := by
  apply Fin.ext
  simp [krausIndex, krausRow, krausPort]
  omega

/-- The source anchor is the first flattened Walsh endpoint. -/
noncomputable def sourceAnchor : Operator := sourceWalshRow 0

/-- `v_j = n_j† a` with source order retained. -/
noncomputable def sourceV (row : Fin 64) : Operator := (sourceWalshRow row)ᴴ * sourceAnchor

/-- The original two ordered Golden branches for one Walsh row. -/
noncomputable def sourceGoldenPair (row : Fin 64) (port : Fin 2) : Operator :=
  if port = 0 then (if row = 0 then 1 else 0) - (2 * goldenP ^ 2) • sourceV row
  else -(2 * goldenP * Real.sqrt goldenP) • sourceV row

/-- The actual ordered family of 128 complex 16×16 matrices. -/
noncomputable def sourceKraus (slot : Fin 128) : Operator :=
  sourceGoldenPair (krausRow slot) (krausPort slot)

theorem sourceKraus_order (row : Fin 64) (port : Fin 2) :
    sourceKraus (krausIndex row port) = sourceGoldenPair row port := by
  unfold sourceKraus
  rw [(krausIndex_coordinates row port).1, (krausIndex_coordinates row port).2]

theorem golden_anchor_controls :
    sourceGoldenPair 0 0 = 1 - (2 * goldenP ^ 2) • sourceV 0 ∧
    sourceGoldenPair 0 1 = -(2 * goldenP * Real.sqrt goldenP) • sourceV 0 := by
  simp [sourceGoldenPair]

/-- Every odd Walsh label yields both zero fine ports at each endpoint. -/
theorem odd_label_kraus_zero (label : Fin 32) (h : label.val % 2 = 1)
    (endpoint port : Fin 2) : sourceKraus (krausIndex (rowIndex label endpoint) port) = 0 := by
  rw [sourceKraus_order]
  have hz := odd_label_flat_row_zero label h endpoint
  have hn : rowIndex label endpoint ≠ 0 := by
    intro he
    have hv := congrArg Fin.val he
    simp [rowIndex] at hv
    omega
  fin_cases port <;> simp [sourceGoldenPair, sourceV, hz, hn]

/-- The count predicate below is linked to actual zero source matrices. -/
theorem marked_slot_zero (slot : Fin 128) (h : (rowLabel (krausRow slot)).val % 2 = 1) :
    sourceKraus slot = 0 := by
  have hr := rowIndex_reconstruct (krausRow slot)
  have hk := krausIndex_reconstruct slot
  calc
    sourceKraus slot = sourceKraus
        (krausIndex (rowIndex (rowLabel (krausRow slot)) (rowEndpoint (krausRow slot)))
          (krausPort slot)) := by rw [hr, hk]
    _ = 0 := odd_label_kraus_zero _ h _ _

/-- There are 64 such concrete slots; other slots are not asserted nonzero. -/
theorem odd_label_slot_count :
    (Finset.univ.filter (fun slot : Fin 128 => (rowLabel (krausRow slot)).val % 2 = 1)).card = 64 := by
  decide

end D0.Geometry.OriginalBookGoldenKraus
