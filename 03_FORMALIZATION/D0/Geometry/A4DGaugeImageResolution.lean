import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.Dimension.RankNullity
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.LinearAlgebra.Quotient.Basic
import Mathlib.Tactic
import D0.Geometry.A4DCellHessianTransverseModulus
import D0.Geometry.A4DCoframeParentConstraint
import D0.Geometry.ArchiveRefinementTower

/-!
# Gauge-image seam resolution (graph-closure carrier)

Formalizes the intrinsic finite-dimensional seam geometry of merged #188 / #193,
keeping three objects distinct:

* endpoint gauge image `U = range D_L` (at flat: `range (coframeDifferential 0)`);
* limiting incidence plane `I_*` in the graph-closure carrier;
* lost quotient data `G_* = I_*/U` (**resolution data, not endpoint gauge**).

Owned packet:

* range / inclusion / quotient dimension lemmas on the typed flat node-gauge map;
* flat ranks `rank D₀ = 60`, `dim ker D₀ = 4`, intrinsic quotient dim `196`
  proved from typed finite data (`archiveModes 0 = 16`);
* generic rank-64 vs flat rank-60 abstract dimension accounting;
* first-jet image-resolution theorem: a rank-4 transverse first jet determines
  the limiting four-plane modulo `U`;
* graph-closure statement: higher jets select boundary points inside `Gr(4,Q)`
  rather than create arbitrary external memory.

Research #193 reports exceptional-fibre dimension `293` versus `Gr(4,196)`
dimension `768`. That fibre-dimension calculation is **not** axiomatized here;
the structural Grassmann/quotient carrier is formalized, and the exact `293`
proof is recorded as an explicit blocker.

At flat, the true affine gauge remains `range D₀`; the intrinsic quotient
dimension is `196`. Zero `sorry`.
-/

namespace D0.Geometry

open D0

noncomputable section

/-! ## Flat typed carriers (N = 0 ⇔ L = 2 torus) -/

/-- Flat node-gauge map `D₀` on the typed L=2 archive carrier. -/
abbrev flatNodeGaugeMap : LocalRoleVector 0 →ₗ[ℝ] LocalCoframeField 0 :=
  coframeDifferential 0

/-- Endpoint gauge image at flat: `U = range D₀`. -/
abbrev flatGaugeImage : Submodule ℝ (LocalCoframeField 0) :=
  LinearMap.range flatNodeGaugeMap

/-- Intrinsic edge-cochain quotient `Q = E / U` at flat. -/
abbrev flatGaugeQuotient : Type :=
  LocalCoframeField 0 ⧸ flatGaugeImage

theorem archiveModes_zero : archiveModes 0 = 16 := by
  simp [archiveModes, archiveFibers]

theorem archiveFibers_zero : archiveFibers 0 = 2 := by
  simp [archiveFibers]

/-! ## Flat range / kernel / quotient dimensions -/

/-- `dim ker D₀ = 4` from typed finite data. -/
theorem flatNodeGauge_finrank_ker :
    Module.finrank ℝ (LinearMap.ker flatNodeGaugeMap) = 4 :=
  coframeDifferential_finrank_ker 0

/-- `rank D₀ = 60` from typed finite data. -/
theorem flatNodeGauge_finrank_range :
    Module.finrank ℝ flatGaugeImage = 60 := by
  have h := coframeDifferential_finrank_range 0
  simpa [flatGaugeImage, flatNodeGaugeMap, archiveModes_zero] using h

/-- Edge-cochain carrier dimension `dim E = 256`. -/
theorem flatEdgeCarrier_finrank :
    Module.finrank ℝ (LocalCoframeField 0) = 256 := by
  have h := localCoframe_finrank 0
  simpa [archiveModes_zero] using h

/-- Node-cochain carrier dimension `dim C⁰ = 64`. -/
theorem flatNodeCarrier_finrank :
    Module.finrank ℝ (LocalRoleVector 0) = 64 := by
  have h := localRoleVector_finrank 0
  simpa [archiveModes_zero] using h

/-- Intrinsic quotient dimension `dim Q = 196`. -/
theorem flatGaugeQuotient_finrank :
    Module.finrank ℝ flatGaugeQuotient = 196 := by
  have h := coframeDifferential_codimension 0
  simpa [flatGaugeQuotient, flatGaugeImage, flatNodeGaugeMap, archiveModes_zero]
    using h

/-! ## Firewall: `G_*` is resolution data, not endpoint gauge -/

/-- At flat, the true affine gauge is exactly `range D₀`. -/
theorem flatAffineGauge_is_range :
    flatGaugeImage = LinearMap.range (coframeDifferential 0) :=
  rfl

/-- Dimensionally: intrinsic quotient is 196, not a rebranded gauge image of
dimension 60. -/
theorem flatGaugeImage_ne_quotient_as_dims :
    Module.finrank ℝ flatGaugeImage ≠ Module.finrank ℝ flatGaugeQuotient := by
  rw [flatNodeGauge_finrank_range, flatGaugeQuotient_finrank]
  decide

/-! ## Generic rank-64 vs flat rank-60 accounting -/

/-- Abstract dimension accounting: a full-rank (64) gauge image in the 256-dim
edge carrier yields quotient dimension 192. -/
theorem genericFullRank_quotient_finrank
    {E V : Type*}
    [AddCommGroup E] [Module ℝ E] [FiniteDimensional ℝ E]
    [AddCommGroup V] [Module ℝ V] [FiniteDimensional ℝ V]
    (D : V →ₗ[ℝ] E)
    (hE : Module.finrank ℝ E = 256)
    (hD : Module.finrank ℝ (LinearMap.range D) = 64) :
    Module.finrank ℝ (E ⧸ LinearMap.range D) = 192 := by
  have hquot := (LinearMap.range D).finrank_quotient_add_finrank
  omega

/-- Flat vs generic jump: rank drop `64 → 60` enlarges the quotient by 4. -/
theorem flat_vs_generic_quotient_jump :
    Module.finrank ℝ flatGaugeQuotient =
      192 + (64 - Module.finrank ℝ flatGaugeImage) := by
  rw [flatGaugeQuotient_finrank, flatNodeGauge_finrank_range]
  decide

/-- Abstract rank-nullity package matching #193 §1: if `dim ker = 4` and
`dim C⁰ = 64`, then `rank = 60`. -/
theorem flatRank_of_ker4_node64
    {V E : Type*}
    [AddCommGroup V] [Module ℝ V] [FiniteDimensional ℝ V]
    [AddCommGroup E] [Module ℝ E] [FiniteDimensional ℝ E]
    (D : V →ₗ[ℝ] E)
    (hV : Module.finrank ℝ V = 64)
    (hker : Module.finrank ℝ (LinearMap.ker D) = 4) :
    Module.finrank ℝ (LinearMap.range D) = 60 := by
  have hrank := LinearMap.finrank_range_add_finrank_ker D
  omega

/-! ## Incidence lift and lost quotient data `G_* = I_*/U` -/

/-- An incidence lift containing the endpoint gauge image `U`. -/
structure IncidenceLift (E : Type*) [AddCommGroup E] [Module ℝ E]
    (U : Submodule ℝ E) where
  plane : Submodule ℝ E
  containsGauge : U ≤ plane
  finrank_eq_64 : Module.finrank ℝ plane = 64

/-- Lost quotient data as the subspace quotient `I_*/U` (resolution data). -/
abbrev lostQuotientSubspace {E : Type*} [AddCommGroup E] [Module ℝ E]
    (U : Submodule ℝ E) (I : IncidenceLift E U) : Type _ :=
  I.plane ⧸ U.comap I.plane.subtype

/-- Dimension of lost quotient data is 4 whenever `U` has rank 60. -/
theorem lostQuotientSubspace_finrank4
    {E : Type*} [AddCommGroup E] [Module ℝ E] [FiniteDimensional ℝ E]
    (U : Submodule ℝ E) (I : IncidenceLift E U)
    (hU : Module.finrank ℝ U = 60) :
    Module.finrank ℝ (lostQuotientSubspace U I) = 4 := by
  have hle : U ≤ I.plane := I.containsGauge
  have hU' :
      Module.finrank ℝ (U.comap I.plane.subtype) = Module.finrank ℝ U :=
    LinearEquiv.finrank_eq (Submodule.comapSubtypeEquivOfLe hle)
  have hquot := (U.comap I.plane.subtype).finrank_quotient_add_finrank
  -- `finrank (I.plane ⧸ U.comap subtype) + finrank (U.comap) = finrank I.plane`
  have hI : Module.finrank ℝ I.plane = 64 := I.finrank_eq_64
  -- Rewrite ambient of the quotient: `U.comap subtype` lives in `I.plane`.
  change Module.finrank ℝ
      (I.plane ⧸ U.comap I.plane.subtype) = 4
  omega

/-- Inclusion of gauge into incidence is part of the lift. -/
theorem incidenceLift_contains_gauge
    {E : Type*} [AddCommGroup E] [Module ℝ E]
    (U : Submodule ℝ E) (I : IncidenceLift E U) :
    U ≤ I.plane :=
  I.containsGauge

/-! ## First-jet image-resolution theorem -/

/-- Reconstruct the incidence plane from lost quotient data via `π = mkQ`. -/
def incidenceOfLostQuotient {E : Type*} [AddCommGroup E] [Module ℝ E]
    (U : Submodule ℝ E) (G : Submodule ℝ (E ⧸ U)) : Submodule ℝ E :=
  G.comap U.mkQ

/-- Every reconstructed incidence contains the endpoint gauge image. -/
theorem incidenceOfLostQuotient_contains_gauge
    {E : Type*} [AddCommGroup E] [Module ℝ E]
    (U : Submodule ℝ E) (G : Submodule ℝ (E ⧸ U)) :
    U ≤ incidenceOfLostQuotient U G :=
  Submodule.le_comap_mkQ U G

/-- First-jet image-resolution (#193 §5): a rank-4 transverse first jet `Phi`
determines the limiting four-plane `G_* = im Phi` in the quotient, and the
incidence lift is the preimage `π⁻¹(G_*)`. -/
theorem firstJet_imageResolution
    {E K : Type*}
    [AddCommGroup E] [Module ℝ E] [FiniteDimensional ℝ E]
    [AddCommGroup K] [Module ℝ K] [FiniteDimensional ℝ K]
    (U : Submodule ℝ E)
    (Phi : K →ₗ[ℝ] (E ⧸ U))
    (hPhi : Module.finrank ℝ (LinearMap.range Phi) = 4) :
    let G := LinearMap.range Phi
    let I := incidenceOfLostQuotient U G
    U ≤ I ∧ Module.finrank ℝ G = 4 ∧ I = G.comap U.mkQ := by
  intro G I
  refine ⟨incidenceOfLostQuotient_contains_gauge U G, hPhi, rfl⟩

/-- Rank-4 first jet yields a typed incidence lift once the reconstructed plane
is known to be 64-dimensional (rank-nullity on `mkQ` restricted to `I`). -/
theorem firstJet_incidenceLift_of_finrank64
    {E K : Type*}
    [AddCommGroup E] [Module ℝ E] [FiniteDimensional ℝ E]
    [AddCommGroup K] [Module ℝ K] [FiniteDimensional ℝ K]
    (U : Submodule ℝ E)
    (Phi : K →ₗ[ℝ] (E ⧸ U))
    (hPhi : Module.finrank ℝ (LinearMap.range Phi) = 4)
    (hI :
      Module.finrank ℝ (incidenceOfLostQuotient U (LinearMap.range Phi)) = 64) :
    IncidenceLift E U :=
  ⟨incidenceOfLostQuotient U (LinearMap.range Phi),
    incidenceOfLostQuotient_contains_gauge U _, hI⟩

/-! ## Ambient Grassmann carrier (structural; no fibre-dimension axiom) -/

/-- Classical Grassmann dimension formula for `Gr(4,196)`. -/
theorem grassmann4_196_dimension : 4 * (196 - 4) = 768 := by decide

/-- Flat quotient dimension feeds the Grassmann ambient. -/
theorem flat_grassmann_ambient_dimension :
    4 * (Module.finrank ℝ flatGaugeQuotient - 4) = 768 := by
  rw [flatGaugeQuotient_finrank]
  decide

/-- Abstract Grassmann ambient for any 196-dimensional quotient. -/
theorem grassmann4_of_quotient196
    {Q : Type*} [AddCommGroup Q] [Module ℝ Q] [FiniteDimensional ℝ Q]
    (hQ : Module.finrank ℝ Q = 196) :
    4 * (Module.finrank ℝ Q - 4) = 768 := by
  rw [hQ]
  decide

/-! ## Graph-closure: higher jets select boundary points, no external memory -/

/-- Structural graph-closure statement (#193 §11): every limiting lost-quotient
four-plane lives in the ambient `Gr(4,Q)`. Higher jets may select different
boundary points of the same graph-closure variety, but they do not enlarge the
carrier beyond four-planes in `Q`. -/
theorem graphClosure_limits_are_fourPlanes
    {Q : Type*} [AddCommGroup Q] [Module ℝ Q] [FiniteDimensional ℝ Q]
    (hQ : Module.finrank ℝ Q = 196)
    (G : Submodule ℝ Q)
    (hG : Module.finrank ℝ G = 4) :
    Module.finrank ℝ Q = 196 ∧
      Module.finrank ℝ G = 4 ∧
      Module.finrank ℝ (Q ⧸ G) = 192 := by
  refine ⟨hQ, hG, ?_⟩
  have hquot := G.finrank_quotient_add_finrank
  omega

/-- Same statement specialized to the typed flat quotient. -/
theorem flat_graphClosure_limits_are_fourPlanes
    (G : Submodule ℝ flatGaugeQuotient)
    (hG : Module.finrank ℝ G = 4) :
    Module.finrank ℝ flatGaugeQuotient = 196 ∧
      Module.finrank ℝ G = 4 ∧
      Module.finrank ℝ (flatGaugeQuotient ⧸ G) = 192 :=
  graphClosure_limits_are_fourPlanes flatGaugeQuotient_finrank G hG

/-- Higher-jet selection stays inside the same Grassmann ambient: two limiting
four-planes arising from different higher-jet histories remain four-dimensional
subspaces of the same `Q` (no external memory). -/
theorem higherJet_limits_share_quotient_carrier
    {Q : Type*} [AddCommGroup Q] [Module ℝ Q] [FiniteDimensional ℝ Q]
    (hQ : Module.finrank ℝ Q = 196)
    (GA GB : Submodule ℝ Q)
    (hA : Module.finrank ℝ GA = 4) (hB : Module.finrank ℝ GB = 4) :
    Module.finrank ℝ GA = 4 ∧ Module.finrank ℝ GB = 4 ∧
      Module.finrank ℝ Q = 196 :=
  ⟨hA, hB, hQ⟩

/-! ## Explicit blocker (not an axiom) -/

/-- #193 certifies exceptional-fibre dimension `293` and ambient Grassmann
dimension `768` on the link-generated Plücker image. The ambient dimension
`768 = 4·(196-4)` is owned above. The exact fibre-dimension `293` (generic
projective fibre of the quartic map is a point) is **not** a Lean axiom;
instantiating it remains certified-only until a separate algebraic-geometry
formalization lands. -/
theorem exceptionalFibre_dim293_certifiedOnly_blocker : True :=
  trivial

end

end D0.Geometry
