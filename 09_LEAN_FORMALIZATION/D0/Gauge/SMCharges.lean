import Mathlib.Data.Rat.Defs

namespace D0

structure WeylField where
  mult : ℚ
  hypercharge : ℚ

def QL : WeylField := ⟨6, 1 / 6⟩
def uRc : WeylField := ⟨3, -2 / 3⟩
def dRc : WeylField := ⟨3, 1 / 3⟩
def LL : WeylField := ⟨2, -1 / 2⟩
def eRc : WeylField := ⟨1, 1⟩
def nuRc : WeylField := ⟨1, 0⟩

def generation : List WeylField := [QL, uRc, dRc, LL, eRc, nuRc]

end D0
