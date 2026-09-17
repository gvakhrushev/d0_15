import Mathlib.Data.ZMod.Basic

namespace D0.Defect

abbrev F2 := ZMod 2
abbrev BranchPlane := F2 × F2

def ePlus : BranchPlane := (1, 0)
def eMinus : BranchPlane := (0, 1)
def eGap : BranchPlane := (1, 1)

def NonzeroVec (v : BranchPlane) : Prop := v ≠ 0

instance decidableNonzero (v : BranchPlane) : Decidable (v ≠ 0) :=
  instDecidableNot

abbrev BranchRay := { v : BranchPlane // v ≠ 0 }

instance : Fintype BranchRay :=
  Subtype.fintype (fun v : BranchPlane => v ≠ 0)

def defectAction (v : BranchPlane) : BranchPlane :=
  (v.2, v.1 + v.2)

end D0.Defect
