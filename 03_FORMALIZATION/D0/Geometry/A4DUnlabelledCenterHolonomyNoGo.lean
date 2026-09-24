import Mathlib.Tactic
import D0.Geometry.ArchivePathWordAlgebra

/-!
# Unlabelled single-center factorization holonomy no-go

Typed abstract class from `MEMO_A4D_ENDPOINT_COMPARISON_JET_OVERLAP_LAW` §2.

Uses plain `Equiv` so center cancellation is definitional/`simp`-friendly.
Endpoint transport (2.1): `T_{u←v} = C_u.symm ∘ C_v` coded as `(C v).trans (C u).symm`.
Chain products use matrix left-to-right order (later list edges act first).

Scoped no-go only: not a universal local-matter no-go.
-/

namespace D0.Geometry
namespace UnlabelledCenter

set_option linter.unusedSimpArgs false

/-- Unlabelled single-center factorization: invertible corner-to-center maps. -/
structure Factorization (corners Fiber Center : Type*) where
  toCenter : corners → (Fiber ≃ Center)

namespace Factorization
variable {corners Fiber Center : Type*}

/-- Endpoint transport (2.1). -/
def endpointTransport (C : Factorization corners Fiber Center) (u v : corners) :
    Fiber ≃ Fiber :=
  (C.toCenter v).trans (C.toCenter u).symm

/-- Reversal is automatic (2.2). -/
theorem endpointTransport_symm (C : Factorization corners Fiber Center) (u v : corners) :
    (C.endpointTransport u v).symm = C.endpointTransport v u := by
  ext x
  simp [endpointTransport]

/-- Center-gauge left action (2.5). -/
def centerGauge (C : Factorization corners Fiber Center) (Q : Center ≃ Center) :
    Factorization corners Fiber Center where
  toCenter := fun v => (C.toCenter v).trans Q

/-- Center-gauge leaves every endpoint transport unchanged (2.5). -/
theorem centerGauge_preserves_endpoint (C : Factorization corners Fiber Center)
    (Q : Center ≃ Center) (u v : corners) :
    (C.centerGauge Q).endpointTransport u v = C.endpointTransport u v := by
  ext x
  simp [endpointTransport, centerGauge]

/-- Induced center overlap (2.3). -/
def overlap (C D : Factorization corners Fiber Center) (v : corners) : Center ≃ Center :=
  (C.toCenter v).symm.trans (D.toCenter v)

/-- Overlap independence on shared endpoints (2.4). -/
theorem overlap_independent_of_endpoint (C D : Factorization corners Fiber Center)
    (v w : corners) (hT : C.endpointTransport v w = D.endpointTransport v w) :
    C.overlap D v = C.overlap D w := by
  have hT' :
      (C.toCenter w).trans (C.toCenter v).symm =
        (D.toCenter w).trans (D.toCenter v).symm := hT
  have h1 := congrArg (fun e => (C.toCenter w).symm.trans e) hT'
  -- Cancel leading `C_w.symm ∘ C_w` on the left-hand side.
  have h1' :
      (C.toCenter v).symm =
        (C.toCenter w).symm.trans ((D.toCenter w).trans (D.toCenter v).symm) := by
    simpa [← Equiv.trans_assoc, Equiv.symm_trans_self, Equiv.refl_trans] using h1
  have h2 := congrArg (fun e => e.trans (D.toCenter v)) h1'
  simpa [overlap, Equiv.trans_assoc, Equiv.symm_trans_self, Equiv.trans_refl,
    Equiv.refl_trans] using h2

/-- Fold endpoint transports in matrix left-to-right order. -/
def chainTransport (C : Factorization corners Fiber Center) : List corners → (Fiber ≃ Fiber)
  | [] => Equiv.refl Fiber
  | [_] => Equiv.refl Fiber
  | u :: v :: rest =>
      (chainTransport C (v :: rest)).trans (C.endpointTransport u v)

/-- Open-chain telescoping. -/
theorem chainTransport_telescopes (C : Factorization corners Fiber Center) (u : corners) :
    ∀ rest : List corners,
      C.chainTransport (u :: rest) =
        (C.toCenter (rest.getLastD u)).trans (C.toCenter u).symm
  | [] => by
      simp [chainTransport, List.getLastD, Equiv.symm_trans_self]
  | v :: rest => by
      have ih := chainTransport_telescopes C v rest
      simp only [chainTransport, ih, endpointTransport, List.getLastD_cons]
      have hcancel :
          (C.toCenter v).symm.trans ((C.toCenter v).trans (C.toCenter u).symm) =
            (C.toCenter u).symm := by
        rw [← Equiv.trans_assoc, Equiv.symm_trans_self, Equiv.refl_trans]
      rw [Equiv.trans_assoc, hcancel]

/-- Cyclic loop telescoping to the identity (2.7). -/
theorem loop_telescopes (C : Factorization corners Fiber Center)
    (v0 : corners) (mid : List corners) :
    C.chainTransport (v0 :: (mid ++ [v0])) = Equiv.refl Fiber := by
  rw [chainTransport_telescopes]
  cases mid with
  | nil => simp [List.getLastD, Equiv.symm_trans_self]
  | cons _ _ => simp [List.getLastD_cons, List.getLastD, Equiv.symm_trans_self]

/-- Reproduces a prescribed edge family. -/
def Reproduces (C : Factorization corners Fiber Center)
    (T : corners → corners → (Fiber ≃ Fiber)) : Prop :=
  ∀ u v, C.endpointTransport u v = T u v

/-- Prescribed-family chain fold. -/
def chainTransportT (T : corners → corners → (Fiber ≃ Fiber)) : List corners → (Fiber ≃ Fiber)
  | [] => Equiv.refl Fiber
  | [_] => Equiv.refl Fiber
  | u :: v :: rest =>
      (chainTransportT T (v :: rest)).trans (T u v)

theorem chainTransport_eq_T (C : Factorization corners Fiber Center)
    (T : corners → corners → (Fiber ≃ Fiber)) (hRep : C.Reproduces T) :
    ∀ vs, C.chainTransport vs = chainTransportT T vs
  | [] => rfl
  | [_] => rfl
  | u :: v :: rest => by
      simp [chainTransport, chainTransportT, hRep u v,
        chainTransport_eq_T C T hRep (v :: rest)]

theorem reproduces_implies_trivial_loop (C : Factorization corners Fiber Center)
    (T : corners → corners → (Fiber ≃ Fiber)) (hRep : C.Reproduces T)
    (v0 : corners) (mid : List corners) :
    chainTransportT T (v0 :: (mid ++ [v0])) = Equiv.refl Fiber := by
  rw [← chainTransport_eq_T C T hRep]
  exact C.loop_telescopes v0 mid

/-- Scoped no-go: nontrivial loop holonomy blocks unlabelled single-center factorization. -/
theorem unlabelledCenter_noGo_of_nontrivial_loop
    (T : corners → corners → (Fiber ≃ Fiber)) (v0 : corners) (mid : List corners)
    (hnontriv : chainTransportT T (v0 :: (mid ++ [v0])) ≠ Equiv.refl Fiber) :
    ¬ ∃ C : Factorization corners Fiber Center, C.Reproduces T := by
  rintro ⟨C, hRep⟩
  exact hnontriv (reproduces_implies_trivial_loop C T hRep v0 mid)

/-- Open transports between fixed endpoints always agree under a factorization. -/
theorem paths_agree (C : Factorization corners Fiber Center) (x y : corners)
    (p q : List corners) :
    C.chainTransport (x :: (p ++ [y])) = C.chainTransport (x :: (q ++ [y])) := by
  rw [chainTransport_telescopes, chainTransport_telescopes]
  cases p <;> cases q <;> simp [List.getLastD_cons, List.getLastD]

end Factorization

end UnlabelledCenter
end D0.Geometry
