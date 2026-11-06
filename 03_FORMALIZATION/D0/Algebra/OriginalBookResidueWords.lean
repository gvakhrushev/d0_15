import D0.Algebra.OriginalBookLocalEffectWords

/-! Computable Walsh rows and reduced slots over the source field GF(1009).
The opposite evaluation supplies the transpose for each adjoint. -/
open Matrix
open D0.Geometry.OriginalBookJuliaWords D0.Geometry.OriginalBookWalsh
open D0.Geometry.OriginalBookGoldenKraus
open D0.Algebra.OriginalBookRadicalLocal D0.Algebra.OriginalBookRadicalSourceConstants
open D0.Algebra.OriginalBookRadicalMod1009 D0.Algebra.OriginalBookLocalMovedRoots
open D0.Algebra.OriginalBookLocalCreators D0.Algebra.OriginalBookLocalBoost
open D0.Algebra.OriginalBookLocalJuliaPairs D0.Algebra.OriginalBookLocalEffectWords
open D0.Algebra.OriginalBookLocalEffectTransport

namespace D0.Algebra.OriginalBookResidueWords

abbrev Op := Matrix (Fin 16) (Fin 16) (ZMod 1009)
abbrev Pairs := Fin 4 → Fin 4 → Op × Op

/-- Store the entries in eager vectors between dense matrix operations. -/
abbrev Block := Vector (Vector (ZMod 1009) 16) 16

def pack (M : Op) : Block := Vector.ofFn fun i => Vector.ofFn (M i)
def unpack (M : Block) : Op := fun i j => M[i.val][j.val]
@[simp] theorem unpack_pack (M : Op) : unpack (pack M) = M := by ext i j; simp [pack, unpack]

def walsh (pairs : Pairs) (row : Fin 64) : Op :=
  (473 : ZMod 1009) • ∑ word : Fin 32,
    (walshSign (rowLabel row) word) •
      (let pair := pairs (wordMode word) (wordRow word)
       if rowEndpoint row = 0 then pair.1 else pair.2)

private theorem map_walsh (e : LocalSource →+* ZMod 1009)
    (halfPower : e ((4405 * localInvD)^5) = 473)
    (pairs : Pairs) (hp : ∀ m r, ((localRowPair m r).1.map e,
      (localRowPair m r).2.map e) = pairs m r) (row : Fin 64) :
    (localWalshRow row).map e = walsh pairs row := by
  have he (w : Fin 32) :
      (localEndpoint w (rowEndpoint row)).map e =
        (if rowEndpoint row = 0 then (pairs (wordMode w) (wordRow w)).1
         else (pairs (wordMode w) (wordRow w)).2) := by
    by_cases h : rowEndpoint row = 0
    · simpa only [localEndpoint, h, if_true] using congrArg Prod.fst (hp (wordMode w) (wordRow w))
    · simpa only [localEndpoint, h, if_false] using congrArg Prod.snd (hp (wordMode w) (wordRow w))
  unfold walsh
  ext i j
  simp only [localWalshRow, Matrix.map_apply, Matrix.smul_apply, Matrix.sum_apply]
  simp only [smul_eq_mul, zsmul_eq_mul, map_mul, map_intCast, map_sum, halfPower]
  apply congrArg (fun s : ZMod 1009 => 473 * s)
  apply Finset.sum_congr rfl
  intro w _
  have hentry := congrArg (fun X : Op => X i j) (he w)
  exact congrArg (fun v : ZMod 1009 => (walshSign (rowLabel row) w : ZMod 1009) * v) hentry

/-- The Walsh-row input of a branch contains the evaluation with the opposite
sign of i on the first factor. -/
def slots (same opposite : Fin 64 → Op) (slot : Fin 128) : Op :=
  let row := krausRow slot
  let v := (opposite row).transpose * same 0
  if krausPort slot = 0 then
    (if row = 0 then 1 else 0) - (2 * (626 : ZMod 1009)^2) • v
  else (-(2 * 626 : ZMod 1009)) • v

private theorem map_slots (e f : LocalSource →+* ZMod 1009)
    (hp : e localP = 626) (hd : ∀ M : LocalOperator, Mᴴ.map e = (M.map f).transpose)
    (same opp : Fin 64 → Op) (hs : ∀ r, (localWalshRow r).map e = same r)
    (ho : ∀ r, (localWalshRow r).map f = opp r) (slot : Fin 128) :
    (localReducedKraus slot).map e = slots same opp slot := by
  have hv (r : Fin 64) : ((localWalshRow r)ᴴ * localWalshRow 0).map e =
      (opp r).transpose * same 0 := by simp [hd, hs, ho]
  have he (r : Fin 64) (i j : Fin 16) := congrArg (fun M : Op => M i j) (hv r)
  simp only [Matrix.map_apply] at he
  unfold slots
  by_cases hport : krausPort slot = 0 <;> by_cases hrow : krausRow slot = 0 <;>
    simp only [localReducedKraus, hport, hrow, if_false, if_true] <;> ext i j <;>
    simp only [Matrix.map_apply, Matrix.sub_apply, Matrix.smul_apply, smul_eq_mul,
      map_sub, map_neg, map_mul, map_ofNat, map_pow, hp, he,
      Matrix.one_apply, Matrix.zero_apply, apply_ite, map_one, map_zero]

/-- Table of the reduced slots in one orientation, computed from Julia pairs. -/
def krausTable (pairs opposite : Pairs) : Fin 128 → Op :=
  slots (walsh pairs) (walsh opposite)

theorem krausTables_correct (plus minus : Pairs)
    (hplus : ∀ m r, ((localRowPair m r).1.map redPlus,
      (localRowPair m r).2.map redPlus) = plus m r)
    (hminus : ∀ m r, ((localRowPair m r).1.map redMinus,
      (localRowPair m r).2.map redMinus) = minus m r) (k : Fin 128) :
    (localReducedKraus k).map redPlus = krausTable plus minus k ∧
    (localReducedKraus k).map redMinus = krausTable minus plus k := by
  have hinv : redMinus localInvD = redPlus localInvD := by
    change redPlus (star localInvD) = _
    rw [localInvD_star]
  have hn : redPlus ((4405 * localInvD)^5) = 473 := by
    rw [map_pow, map_mul, map_ofNat, modInvD]; decide
  have hm : redMinus ((4405 * localInvD)^5) = 473 := by
    simpa only [map_pow, map_mul, map_ofNat, hinv] using hn
  have wp := map_walsh redPlus hn plus hplus
  have wm := map_walsh redMinus hm minus hminus
  have hmp : redMinus localP = 626 := by
    change redPlus (star localP) = _
    rw [localSourceConstants_star.1, localSourceConstants_mod.1]
  unfold krausTable
  constructor
  · exact map_slots redPlus redMinus localSourceConstants_mod.1 localDagger_mod _ _
      wp wm k
  · exact map_slots redMinus redPlus hmp localDagger_mod_minus _ _
      wm wp k

private def pairData (pairs : Pairs) : Vector (Vector (Block × Block) 4) 4 :=
  Vector.ofFn fun m => Vector.ofFn fun r =>
    let pair := pairs m r
    (pack pair.1, pack pair.2)

private def unpackPairs (v : Vector (Vector (Block × Block) 4) 4) : Pairs :=
  fun m r => (unpack v[m.val][r.val].1, unpack v[m.val][r.val].2)

private theorem unpackPairs_pairData (p : Pairs) : unpackPairs (pairData p) = p := by
  funext m r
  simp [unpackPairs, pairData]

private def rowData (pairs : Pairs) : Vector Block 64 :=
  let prepared := pairData pairs
  Vector.ofFn fun r => pack (walsh (unpackPairs prepared) r)

private def slotData (same opp : Vector Block 64) : Vector Block 128 :=
  Vector.ofFn fun k => pack (slots (fun r => unpack same[r.val]) (fun r => unpack opp[r.val]) k)

private theorem slotData_correct (plus minus : Pairs) (k : Fin 128) :
    unpack ((slotData (rowData plus) (rowData minus))[k.val]) = krausTable plus minus k := by
  simp [slotData, rowData, unpackPairs_pairData, krausTable]

/-- Apply the terminal identity and fold the chronological word from the right.
The cached intermediate product avoids recomputing a row of a matrix product
inside the next matrix product. -/
private def effectData (plus minus : Vector Block 128) : List (Fin 128) → Block
  | [] => pack 1
  | k :: rest =>
    let tail := effectData plus minus rest
    let left := pack ((unpack minus[k.val]).transpose * unpack tail)
    pack (unpack left * unpack plus[k.val])

private theorem effectData_correct (plus minus : Vector Block 128) (path : List (Fin 128)) :
    unpack (effectData plus minus path) =
      crossEffect (fun k => unpack plus[k.val]) (fun k => unpack minus[k.val]) path := by
  induction path with
  | nil => simp [effectData, crossEffect]
  | cons k rest ih => simp [effectData, crossEffect, ih]

/-- Evaluate the coordinate matrix once from packed intermediates in both
residue orientations. Returning a vector keeps the full computation outside
the pointwise equality check of the stored numerical witness. -/
def computedTable {n : ℕ} (plus minus : Pairs)
    (paths : Fin n → List (Fin 128)) (coord : Fin n → Fin 16 × Fin 16) :
    Vector (Vector (ZMod 1009) n) n :=
  let wp := rowData plus
  let wm := rowData minus
  let kp := slotData wp wm
  let km := slotData wm wp
  Vector.ofFn fun i =>
    let effect := effectData kp km (paths i)
    Vector.ofFn fun j => unpack effect (coord j).1 (coord j).2

def computedRows {n : ℕ} (plus minus : Pairs)
    (paths : Fin n → List (Fin 128)) (coord : Fin n → Fin 16 × Fin 16) :
    Matrix (Fin n) (Fin n) (ZMod 1009) :=
  let table := computedTable plus minus paths coord
  fun i j => table[i.val][j.val]

theorem computedRows_eq_residueRows {n : ℕ} (plus minus : Pairs)
    (hplus : ∀ m r, ((localRowPair m r).1.map redPlus,
      (localRowPair m r).2.map redPlus) = plus m r)
    (hminus : ∀ m r, ((localRowPair m r).1.map redMinus,
      (localRowPair m r).2.map redMinus) = minus m r)
    (paths : Fin n → List (Fin 128)) (coord : Fin n → Fin 16 × Fin 16) :
    computedRows plus minus paths coord = residueRows paths coord := by
  ext i j
  have hk := krausTables_correct plus minus hplus hminus
  simp only [computedRows, computedTable, Vector.getElem_ofFn, effectData_correct,
    slotData_correct, residueRows, fun k => (hk k).1, fun k => (hk k).2]

/-- Check the two packed matrices once and recover equality of linear-algebra
objects. This avoids rebuilding the source matrix at each of its entries. -/
theorem computedRows_eq_of_table {n : ℕ} (plus minus : Pairs)
    (paths : Fin n → List (Fin 128)) (coord : Fin n → Fin 16 × Fin 16)
    (A : Matrix (Fin n) (Fin n) (ZMod 1009))
    (h : computedTable plus minus paths coord = Vector.ofFn (fun i => Vector.ofFn (A i))) :
    computedRows plus minus paths coord = A := by
  ext i j
  simp [computedRows, h]

end D0.Algebra.OriginalBookResidueWords
