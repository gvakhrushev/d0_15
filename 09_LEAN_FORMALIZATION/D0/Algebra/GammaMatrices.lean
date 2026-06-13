import Mathlib.Tactic

namespace D0

structure GI where
  re : ℤ
  im : ℤ
  deriving DecidableEq, Repr

namespace GI

def zero : GI := ⟨0, 0⟩
def one : GI := ⟨1, 0⟩
def negOne : GI := ⟨-1, 0⟩
def I : GI := ⟨0, 1⟩
def negI : GI := ⟨0, -1⟩
def ofInt (n : ℤ) : GI := ⟨n, 0⟩
def add (a b : GI) : GI := ⟨a.re + b.re, a.im + b.im⟩
def neg (a : GI) : GI := ⟨-a.re, -a.im⟩
def mul (a b : GI) : GI := ⟨a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re⟩

instance : Zero GI := ⟨zero⟩
instance : One GI := ⟨one⟩
instance : Neg GI := ⟨neg⟩
instance : Add GI := ⟨add⟩
instance : Mul GI := ⟨mul⟩

end GI

abbrev Mat4 := Fin 4 → Fin 4 → GI

def mAdd (A B : Mat4) : Mat4 := fun i j => A i j + B i j
def mMul (A B : Mat4) : Mat4 := fun i j =>
  A i 0 * B 0 j + A i 1 * B 1 j + A i 2 * B 2 j + A i 3 * B 3 j
def scalarDiag (c : ℤ) : Mat4 := fun i j => if i = j then GI.ofInt c else 0

def gamma0 : Mat4 := fun i j =>
  if i = j then
    if i.val < 2 then GI.one else GI.negOne
  else 0

def gamma1 : Mat4 := fun i j =>
  match i.val, j.val with
  | 0, 3 => GI.one
  | 1, 2 => GI.one
  | 2, 1 => GI.negOne
  | 3, 0 => GI.negOne
  | _, _ => 0

def gamma2 : Mat4 := fun i j =>
  match i.val, j.val with
  | 0, 3 => GI.negI
  | 1, 2 => GI.I
  | 2, 1 => GI.I
  | 3, 0 => GI.negI
  | _, _ => 0

def gamma3 : Mat4 := fun i j =>
  match i.val, j.val with
  | 0, 2 => GI.one
  | 1, 3 => GI.negOne
  | 2, 0 => GI.negOne
  | 3, 1 => GI.one
  | _, _ => 0

def gamma (mu : Fin 4) : Mat4 :=
  match mu.val with
  | 0 => gamma0
  | 1 => gamma1
  | 2 => gamma2
  | _ => gamma3

def eta (mu nu : Fin 4) : ℤ :=
  if mu = nu then
    if mu.val = 0 then 1 else -1
  else 0

def anticommutator (A B : Mat4) : Mat4 := mAdd (mMul A B) (mMul B A)

def cliffordRhs (mu nu : Fin 4) : Mat4 := scalarDiag (2 * eta mu nu)

theorem gamma_anticomm_entries (mu nu i j : Fin 4) :
    anticommutator (gamma mu) (gamma nu) i j = cliffordRhs mu nu i j := by
  native_decide +revert

theorem bivector_count : Nat.choose 4 2 = 6 := by
  native_decide

end D0
