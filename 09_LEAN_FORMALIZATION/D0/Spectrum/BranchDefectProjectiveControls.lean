import D0.Spectrum.BranchDefectProjectiveGeneration

namespace D0

structure BranchDefectProjectiveProof where
  exactlyThree : Fintype.card BranchRay = 3
  actionOrderThree : ∀ v : Vec2F2, defectAction (defectAction (defectAction v)) = v
  cardDefectGen : Fintype.card DefectGeneration = 3

theorem branch_defect_projective_proof_closed :
  Nonempty BranchDefectProjectiveProof :=
  ⟨{ exactlyThree := exactly_three_projective_branch_defect_generations
     actionOrderThree := defectAction_order_three
     cardDefectGen := defect_generation_card }⟩

end D0
