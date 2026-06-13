import D0.Combinatorics.PhaseTowerRecursion

namespace D0

abbrev WindowTower := Nat -> Nat

def sampleWindowEvidence (T : WindowTower) : Prop :=
  T 0 = 44 ∧ T 1 = 710

def sampleTowerA : WindowTower
  | 0 => 44
  | 1 => 710
  | _ => 710

def sampleTowerB : WindowTower
  | 0 => 44
  | 1 => 710
  | _ => 4059

theorem sampleTowerA_evidence : sampleWindowEvidence sampleTowerA := by
  exact ⟨rfl, rfl⟩

theorem sampleTowerB_evidence : sampleWindowEvidence sampleTowerB := by
  exact ⟨rfl, rfl⟩

theorem sample_windows_do_not_determine_infinite_tower :
    ∃ A B : WindowTower,
      sampleWindowEvidence A ∧ sampleWindowEvidence B ∧ A 2 ≠ B 2 := by
  refine ⟨sampleTowerA, sampleTowerB, sampleTowerA_evidence, sampleTowerB_evidence, ?_⟩
  norm_num [sampleTowerA, sampleTowerB]

end D0
