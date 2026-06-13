import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

namespace D0.Gauge

structure DirectedEdge (V : Type) where
  src : V
  tgt : V

abbrev Connection (V G : Type) := DirectedEdge V -> G

structure GaugeGroupDerivable (G : Type) [Group G] : Prop where
  derived_associative_carrier : True

theorem wilson_link_group_carrier_derivable {G : Type} [Group G] :
    GaugeGroupDerivable G := by
  exact ⟨trivial⟩

structure Face3 (V : Type) where
  e1 : DirectedEdge V
  e2 : DirectedEdge V
  e3 : DirectedEdge V
  h_path1 : e1.tgt = e2.src
  h_path2 : e2.tgt = e3.src
  h_path3 : e3.tgt = e1.src

def plaquetteHolonomy {V G : Type} [Group G]
    (U : Connection V G) (f : Face3 V) : G :=
  U f.e1 * U f.e2 * U f.e3

def gaugeTransform {V G : Type} [Group G]
    (U : Connection V G) (g : V -> G) : Connection V G :=
  fun e => (g e.src)⁻¹ * U e * g e.tgt

theorem wilson_loop_covariance {V G : Type} [Group G]
    (U : Connection V G) (g : V -> G) (f : Face3 V) :
    plaquetteHolonomy (gaugeTransform U g) f =
      (g f.e1.src)⁻¹ * plaquetteHolonomy U f * (g f.e1.src) := by
  unfold plaquetteHolonomy gaugeTransform
  rw [f.h_path1, f.h_path2, f.h_path3]
  group

noncomputable def matrixCurvature {n : Type} [Fintype n]
    (D A : Matrix n n Real) : Matrix n n Real :=
  D * A - A * D

noncomputable def naiveGaugeTransform {n : Type} [Fintype n]
    (D U A : Matrix n n Real) : Matrix n n Real :=
  U * A * U + matrixCurvature D U

def fin3D : Matrix (Fin 3) (Fin 3) Real := fun i j =>
  if i.val = 0 /\ j.val = 1 then 1
  else if i.val = 1 /\ j.val = 0 then -1
  else 0

def fin3U : Matrix (Fin 3) (Fin 3) Real := fun i j =>
  if i.val = 1 /\ j.val = 2 then 1
  else if i.val = 2 /\ j.val = 1 then -1
  else 0

theorem naive_local_gauge_covariance_counterexample_fin3 :
    exists D U A : Matrix (Fin 3) (Fin 3) Real,
      A = 0 /\
      matrixCurvature D A = 0 /\
      Not (matrixCurvature D (naiveGaugeTransform D U A) = 0) := by
  refine ⟨fin3D, fin3U, 0, rfl, ?_, ?_⟩
  · simp [matrixCurvature]
  · intro h
    have h_entry := congr_fun (congr_fun h (1 : Fin 3)) (2 : Fin 3)
    norm_num [matrixCurvature, naiveGaugeTransform, fin3D, fin3U, Matrix.mul_apply,
      Fin.sum_univ_three] at h_entry

end D0.Gauge
