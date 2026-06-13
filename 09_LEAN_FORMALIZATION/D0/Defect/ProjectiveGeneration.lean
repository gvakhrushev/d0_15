import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import D0.Defect.Basic

namespace D0.Defect

theorem ePlus_nonzero :
  ePlus ≠ 0 := by
  intro h
  injection h with h1 _
  have h2 : (1 : F2) = 0 := h1
  norm_num at h2

theorem eMinus_nonzero :
  eMinus ≠ 0 := by
  intro h
  injection h with _ h2
  have h3 : (1 : F2) = 0 := h2
  norm_num at h3

theorem eGap_nonzero :
  eGap ≠ 0 := by
  intro h
  injection h with h1 _
  have h2 : (1 : F2) = 0 := h1
  norm_num at h2

theorem branchRay_card :
  Fintype.card BranchRay = 3 := by
  decide

theorem defectAction_ePlus :
  defectAction ePlus = eMinus := by
  rfl

theorem defectAction_eMinus :
  defectAction eMinus = eGap := by
  rfl

theorem defectAction_eGap :
  defectAction eGap = ePlus := by
  unfold defectAction eGap ePlus
  simp
  decide

theorem defectAction_order_three :
  ∀ v : BranchPlane, defectAction (defectAction (defectAction v)) = v := by
  decide

theorem defectAction_cycles_generation_rays :
  defectAction ePlus = eMinus ∧
  defectAction eMinus = eGap ∧
  defectAction eGap = ePlus :=
  ⟨defectAction_ePlus, defectAction_eMinus, defectAction_eGap⟩

end D0.Defect
