import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.VNext2.SpectralEinsteinResponse

/-!
# D0.Gravity.FiniteGravityResponseSingleWitness

This module packages the finite response `E_L := 2L` as one stored witness.
Every predicate in `SingleWitnessProperties` refers to that same stored `W.E`;
none is assembled from an unrelated probe, flux, TT operator, or scalar
spectral witness as in the legacy macro-signature aggregator.

The result is a finite graph-Laplacian seed only.  It makes no claim about a
continuum tensor, Lorentz covariance, diffeomorphism naturality, differential
order two, Bianchi identity, TT gravitons, or an Einstein tensor.
-/

namespace D0.Gravity.FiniteGravityResponseSingleWitness

open BigOperators Matrix
open D0.VNext2.SpectralEinsteinResponse

/-! A stored finite Laplacian and its one stored response. -/

structure FiniteGravityResponseWitness
    (N : Type*) [Fintype N] [DecidableEq N] where
  L : Matrix N N ℝ
  hL : IsGraphLaplacian L
  E : Matrix N N ℝ
  response_eq : E = einsteinResponse L

/-- Store exactly the canonical response `E_L := 2L` for a graph Laplacian. -/
def ofGraphLaplacian
    {N : Type*} [Fintype N] [DecidableEq N]
    (L : Matrix N N ℝ) (hL : IsGraphLaplacian L) :
    FiniteGravityResponseWitness N :=
  { L := L
    hL := hL
    E := einsteinResponse L
    response_eq := rfl }

/-! Predicates below all mention the single stored response `W.E`. -/

structure SingleWitnessProperties
    {N : Type*} [Fintype N] [DecidableEq N]
    (W : FiniteGravityResponseWitness N) : Prop where
  response_identity : W.E = (2 : ℝ) • W.L
  symmetric : W.E.transpose = W.E
  archive_divergence_zero : archiveDivergence W.E = 0
  nontrivial : W.L ≠ 0 → W.E ≠ 0

theorem response_identity
    {N : Type*} [Fintype N] [DecidableEq N]
    (W : FiniteGravityResponseWitness N) :
    W.E = (2 : ℝ) • W.L := by
  calc
    W.E = einsteinResponse W.L := W.response_eq
    _ = (2 : ℝ) • W.L := rfl

theorem response_symmetric
    {N : Type*} [Fintype N] [DecidableEq N]
    (W : FiniteGravityResponseWitness N) :
    W.E.transpose = W.E := by
  rw [W.response_eq]
  exact einstein_response_symmetric W.L W.hL

theorem response_archive_divergence_zero
    {N : Type*} [Fintype N] [DecidableEq N]
    (W : FiniteGravityResponseWitness N) :
    archiveDivergence W.E = 0 := by
  rw [W.response_eq]
  exact einstein_response_divergence_free W.L W.hL

theorem response_nontrivial
    {N : Type*} [Fintype N] [DecidableEq N]
    (W : FiniteGravityResponseWitness N) :
    W.L ≠ 0 → W.E ≠ 0 := by
  intro hL hE
  apply hL
  have hscaled : (2 : ℝ) • W.L = 0 := by
    calc
      (2 : ℝ) • W.L = einsteinResponse W.L := rfl
      _ = W.E := W.response_eq.symm
      _ = 0 := hE
  ext i j
  have hij := congrArg (fun M : Matrix N N ℝ => M i j) hscaled
  have hentry : (2 : ℝ) * W.L i j = 0 := by
    simpa [Matrix.smul_apply, smul_eq_mul] using hij
  have hzero : W.L i j = 0 := by linarith
  simpa using hzero

/-- All four finite predicates are properties of one stored `W.E`. -/
theorem single_witness_properties
    {N : Type*} [Fintype N] [DecidableEq N]
    (W : FiniteGravityResponseWitness N) :
    SingleWitnessProperties W :=
  { response_identity := response_identity W
    symmetric := response_symmetric W
    archive_divergence_zero := response_archive_divergence_zero W
    nontrivial := response_nontrivial W }

/-- The canonical one-witness package obtained directly from `L`. -/
theorem canonical_single_witness_properties
    {N : Type*} [Fintype N] [DecidableEq N]
    (L : Matrix N N ℝ) (hL : IsGraphLaplacian L) :
    SingleWitnessProperties (ofGraphLaplacian L hL) :=
  single_witness_properties (ofGraphLaplacian L hL)

end D0.Gravity.FiniteGravityResponseSingleWitness
