import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import D0.Geometry.ArchiveRefinementTower

open scoped BigOperators

namespace D0

structure ArchiveFiberGraph (n : Nat) where
  V : Type
  fintypeV : Fintype V
  adj : V → V → Prop
  symm : Symmetric adj
  irreflexive : Irreflexive adj

def archiveFiberGraph (n : Nat) : ArchiveFiberGraph n where
  V := ArchivePoints n
  fintypeV := inferInstance
  adj a b := a ≠ b
  symm a b h := h.symm
  irreflexive := by
    intro a h
    exact h rfl

instance (n : Nat) : DecidableRel (archiveFiberGraph n).adj := by
  intro a b
  unfold archiveFiberGraph
  dsimp
  infer_instance

instance (n : Nat) : DecidableEq (archiveFiberGraph n).V := by
  unfold archiveFiberGraph
  dsimp
  infer_instance

def graphDegree {n : Nat} (G : ArchiveFiberGraph n) [DecidableRel G.adj] (a : G.V) : Real :=
  haveI : Fintype G.V := G.fintypeV
  Finset.sum Finset.univ (fun x => if G.adj a x then (1:Real) else (0:Real))

def graphLaplacian {n : Nat} (G : ArchiveFiberGraph n) [DecidableEq G.V] [DecidableRel G.adj] (a b : G.V) : Real :=
  if a = b then graphDegree G a else if G.adj a b then -1 else 0

def Symmetric {V : Type} (L : V → V → Real) : Prop :=
  forall a b, L a b = L b a

theorem graph_laplacian_symmetric (n : Nat) :
  Symmetric (graphLaplacian (archiveFiberGraph n)) := by
  intro a b
  unfold graphLaplacian graphDegree
  by_cases h : a = b
  · subst b
    simp
  · have hba : b ≠ a := Ne.symm h
    simp [h, hba]
    have h_adj1 : (archiveFiberGraph n).adj a b := h
    have h_adj2 : (archiveFiberGraph n).adj b a := hba
    simp [h_adj1, h_adj2]

end D0
