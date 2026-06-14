import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-!
# D0-GENERATIVE-DYNAMICS-001 (A.2) — the seam anomaly `C_n ≠ 0` sources time (Lean anchor)

Python certificate: `05_CERTS/vp_gluing_anomaly_time.py`.

D0 refines the carrier through a prolongation `B`. The coarse Laplacian is the Galerkin
restriction `L_n = Bᵀ L_{n+1} B` (the RG / conservation relation): the Laplacian is preserved
under restriction. But the refinement does NOT intertwine the Laplacians — the seam commutator
`C_n = L_{n+1} B - B L_n` is nonzero. A vanishing `C_n` would require `B` aligned to the
eigenbasis of `L_{n+1}`, an external spectral catalogue forbidden by M1. So `C_n ≠ 0` is forced:
the seam cannot close, the state is re-written at each refinement, and that irreversible re-write
is time. This module checks both facts by `native_decide` on the concrete integer model.
-/

namespace D0.Claims

open Matrix

/-- Fine Laplacian: path graph `P₃`. -/
def L1 : Matrix (Fin 3) (Fin 3) ℤ :=
  !![ 1, -1,  0;
     -1,  2, -1;
      0, -1,  1]

/-- Prolongation `B` (3 fine × 2 coarse). -/
def Bpro : Matrix (Fin 3) (Fin 2) ℤ :=
  !![ 1, 0;
      1, 1;
      0, 1]

/-- The Galerkin coarse operator `L_n = Bᵀ L₁ B` (here it evaluates to the identity). -/
def Ln : Matrix (Fin 2) (Fin 2) ℤ :=
  !![ 1, 0;
      0, 1]

/-- **Galerkin / RG relation.** The Laplacian is preserved under restriction:
`Bᵀ L₁ B = L_n`. -/
theorem galerkin_restriction : Bproᵀ * L1 * Bpro = Ln := by native_decide

/-- **Seam anomaly.** The refinement does NOT intertwine the Laplacians: the `(0,0)` entry of
the seam commutator `C_n = L₁ B - B L_n` is `-1 ≠ 0`, so `C_n ≠ 0`. -/
theorem seam_anomaly_entry : (L1 * Bpro - Bpro * Ln) 0 0 = -1 := by native_decide

/-- The seam commutator is a nonzero matrix. -/
theorem seam_anomaly_nonzero : L1 * Bpro - Bpro * Ln ≠ 0 := by
  intro h
  have : (L1 * Bpro - Bpro * Ln) 0 0 = (0 : Matrix (Fin 3) (Fin 2) ℤ) 0 0 := by rw [h]
  rw [seam_anomaly_entry] at this
  simp at this

/-- **D0-GENERATIVE-DYNAMICS-001 (A.2 anchor).** The Laplacian is preserved under restriction
(`Bᵀ L₁ B = L_n`) yet the refinement does not intertwine it (`C_n ≠ 0`): the seam cannot close,
so the refinement re-writes the state — time. -/
theorem gluing_anomaly_time :
    Bproᵀ * L1 * Bpro = Ln ∧ L1 * Bpro - Bpro * Ln ≠ 0 :=
  ⟨galerkin_restriction, seam_anomaly_nonzero⟩

end D0.Claims
