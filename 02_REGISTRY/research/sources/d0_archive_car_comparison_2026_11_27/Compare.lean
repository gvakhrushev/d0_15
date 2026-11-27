import D0.Geometry.ArchiveCARRelations

open D0 D0.Geometry

def roleAt (n : Nat) : Role :=
  if n = 0 then A else if n = 1 then B else if n = 2 then C else D

def stateAt (n : Nat) : ArchiveFockState :=
  fun role => Nat.testBit n (roleOrderIndex role)

def matrixRows : List (List (List Int)) :=
  (List.range 4).map fun r =>
    (List.range 16).map fun bra =>
      (List.range 16).map fun ket =>
        carAnnihilateInt (roleAt r) (stateAt bra) (stateAt ket)

#eval matrixRows
