import Mathlib.Tactic
import Mathlib.Algebra.BigOperators.Fin
import D0.Geometry.ArchiveRefinementTower

open scoped BigOperators

namespace D0

abbrev ArchiveVector := Fin 4 -> Rat

structure FiniteArchiveMeasure where
  atomCount : Nat
  point : Fin atomCount -> ArchiveVector
  weight : Fin atomCount -> Rat
  nonneg : forall i, 0 <= weight i
  total_one : (Finset.univ.sum weight) = 1

def ArchiveFiniteSupport (mu : FiniteArchiveMeasure) : Prop :=
  0 < mu.atomCount

def archiveCrossWeight (_i : Fin 8) : Rat :=
  (1 : Rat) / 8

def archiveCrossVector (i : Fin 8) : ArchiveVector := fun k =>
  match i.val, k.val with
  | 0, 0 => (1 : Rat) / 5
  | 1, 0 => -(1 : Rat) / 5
  | 2, 1 => (1 : Rat) / 5
  | 3, 1 => -(1 : Rat) / 5
  | 4, 2 => (1 : Rat) / 5
  | 5, 2 => -(1 : Rat) / 5
  | 6, 3 => (1 : Rat) / 5
  | 7, 3 => -(1 : Rat) / 5
  | _, _ => 0

theorem archive_cross_weight_nonneg (i : Fin 8) :
    0 <= archiveCrossWeight i := by
  norm_num [archiveCrossWeight]

theorem archive_cross_weight_total_one :
    (Finset.univ.sum archiveCrossWeight) = 1 := by
  norm_num [archiveCrossWeight]

def d0ArchiveMeasure : FiniteArchiveMeasure :=
  { atomCount := 8
    point := archiveCrossVector
    weight := archiveCrossWeight
    nonneg := archive_cross_weight_nonneg
    total_one := archive_cross_weight_total_one }

def archiveStageMeasure (_n : Nat) : FiniteArchiveMeasure :=
  d0ArchiveMeasure

theorem d0ArchiveMeasure_atom_count :
    d0ArchiveMeasure.atomCount = 8 := by
  rfl

theorem d0ArchiveMeasure_total_one :
    (Finset.univ.sum d0ArchiveMeasure.weight) = 1 := by
  exact d0ArchiveMeasure.total_one

theorem d0ArchiveMeasure_finite_support :
    ArchiveFiniteSupport d0ArchiveMeasure := by
  norm_num [ArchiveFiniteSupport, d0ArchiveMeasure]

theorem archiveStageMeasure_finite_support (n : Nat) :
    ArchiveFiniteSupport (archiveStageMeasure n) := by
  exact d0ArchiveMeasure_finite_support

def supportCard (mu : FiniteArchiveMeasure) : Nat :=
  mu.atomCount

end D0
