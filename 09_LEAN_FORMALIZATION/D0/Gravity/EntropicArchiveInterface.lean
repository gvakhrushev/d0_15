import Mathlib.Data.Rat.Lemmas
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Set.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

open scoped BigOperators

namespace D0.Gravity

/-- Finite archive graph carrying rational edge capacities. -/
structure FiniteArchiveGraph where
  V : Type
  instFintype : Fintype V
  instDecEq : DecidableEq V
  edgeWeight : V -> V -> Rat
  symmetric : forall i j, edgeWeight i j = edgeWeight j i
  nonnegative : forall i j, 0 <= edgeWeight i j

attribute [instance] FiniteArchiveGraph.instFintype
attribute [instance] FiniteArchiveGraph.instDecEq

/-- Directed cut weight from a finite region to its complement. -/
noncomputable def BoundaryCutWeight (G : FiniteArchiveGraph) (S : Set G.V) : Rat := by
  classical
  exact
    ∑ i, ∑ j,
      if i ∈ S ∧ j ∉ S then G.edgeWeight i j else 0

/-- Finite boundary-capacity rule: the cut-area response divided by four. -/
noncomputable def BoundaryCapacity (G : FiniteArchiveGraph) (S : Set G.V) : Rat :=
  BoundaryCutWeight G S / 4

theorem boundary_cut_weight_nonnegative
    (G : FiniteArchiveGraph) (S : Set G.V) :
    0 <= BoundaryCutWeight G S := by
  classical
  unfold BoundaryCutWeight
  exact Finset.sum_nonneg (fun i _ =>
    Finset.sum_nonneg (fun j _ => by
      by_cases h : i ∈ S ∧ j ∉ S
      · simp [h, G.nonnegative i j]
      · simp [h]))

theorem boundary_capacity_nonnegative
    (G : FiniteArchiveGraph) (S : Set G.V) :
    0 <= BoundaryCapacity G S := by
  unfold BoundaryCapacity
  exact div_nonneg (boundary_cut_weight_nonnegative G S) (by norm_num)

/-- Finite weighted degree. -/
def GraphDegree (G : FiniteArchiveGraph) (i : G.V) : Rat :=
  ∑ j, G.edgeWeight i j

/-- Combinatorial weighted graph Laplacian. -/
def GraphLaplacian (G : FiniteArchiveGraph) : Matrix G.V G.V Rat :=
  fun i j =>
    if i = j then GraphDegree G i
    else -G.edgeWeight i j

theorem graph_laplacian_symmetric
    (G : FiniteArchiveGraph) :
    (GraphLaplacian G).transpose = GraphLaplacian G := by
  ext i j
  by_cases h : i = j
  · subst j
    simp [GraphLaplacian]
  · have hji : j ≠ i := fun h' => h h'.symm
    simp [GraphLaplacian, h, hji, G.symmetric i j]

/-- Formal finite heat-trace observable; executable spectral checks live in certs. -/
structure HeatTraceObservable (G : FiniteArchiveGraph) where
  scale : Rat
  value : Rat
  nonnegative : 0 <= value

/-- Antisymmetric finite archive flux. -/
structure ArchiveFlux (G : FiniteArchiveGraph) where
  flux : G.V -> G.V -> Rat
  antisymm : forall i j, flux i j = -flux j i

/-- Net flux through one archive vertex. -/
def NetFluxAt (G : FiniteArchiveGraph) (F : ArchiveFlux G) (i : G.V) : Rat :=
  ∑ j, F.flux i j

/-- Local finite archive conservation. -/
def ConservedArchiveFlux (G : FiniteArchiveGraph) (F : ArchiveFlux G) : Prop :=
  forall i, NetFluxAt G F i = 0

theorem conserved_flux_no_creation
    (G : FiniteArchiveGraph) (F : ArchiveFlux G)
    (h : ConservedArchiveFlux G F) :
    ∑ i, NetFluxAt G F i = 0 := by
  calc
    ∑ i, NetFluxAt G F i = ∑ _i : G.V, 0 := by
      exact Finset.sum_congr rfl (fun i _ => h i)
    _ = 0 := by simp

/-- Finite entropic boundary tension on a cut region. -/
structure EntropicBoundaryTension (G : FiniteArchiveGraph) where
  region : Set G.V
  pressure : Rat
  pressure_nonnegative : 0 <= pressure

/-- The induced finite surface-tension response. -/
noncomputable def EntropicTensionEnergy
    (G : FiniteArchiveGraph)
    (T : EntropicBoundaryTension G) : Rat :=
  BoundaryCapacity G T.region * T.pressure

theorem entropic_tension_energy_nonnegative
    (G : FiniteArchiveGraph)
    (T : EntropicBoundaryTension G) :
    0 <= EntropicTensionEnergy G T := by
  unfold EntropicTensionEnergy
  exact
    mul_nonneg
      (boundary_capacity_nonnegative G T.region)
      T.pressure_nonnegative

/-- Finite core closure package for the archive entropy interface. -/
structure EntropicArchiveInterfaceClosure (G : FiniteArchiveGraph) where
  laplacian_symmetric :
    (GraphLaplacian G).transpose = GraphLaplacian G
  boundary_nonnegative :
    forall S : Set G.V, 0 <= BoundaryCapacity G S
  tension_nonnegative :
    forall T : EntropicBoundaryTension G, 0 <= EntropicTensionEnergy G T
  conserved_flux_has_no_creation :
    forall F : ArchiveFlux G,
      ConservedArchiveFlux G F -> ∑ i, NetFluxAt G F i = 0

def entropic_archive_interface_closure
    (G : FiniteArchiveGraph) :
    EntropicArchiveInterfaceClosure G where
  laplacian_symmetric := graph_laplacian_symmetric G
  boundary_nonnegative := boundary_capacity_nonnegative G
  tension_nonnegative := entropic_tension_energy_nonnegative G
  conserved_flux_has_no_creation := conserved_flux_no_creation G

end D0.Gravity
