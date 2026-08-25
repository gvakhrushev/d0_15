import Mathlib.Tactic
import D0.Spectral.ZoneMatrixSpectrum
import D0.Cosmology.PhasonFlipEntropy
import D0.Synthesis.SDECubicSpectralDisjointness

/-!
# The S_DE transfer is the active normalized-scene transfer

The preceding spectral-disjointness result rules out an intertwiner between the
owned two-mode S_DE transfer and the **unnormalized** rank-3 zone-quotient
adjacency.  That no-go is load-bearing: it identifies the wrong operator.

Here the normalized scene transport gives a positive result.  Let `M` be the
owned row-stochastic `3 × 3` zone transport and `L = I - M` its normalized
Laplacian.  The stationary weight is

`π = (9·24, 11·22, 13·20) = (216,242,260)`.

An explicit full-rank rational matrix `X : ℚ² → ℚ³` identifies the S_DE
two-mode transfer with the restriction of `L` to the active hyperplane
`ker π`.  An explicit retraction `Y` verifies both sides of the split.

The active subspace and its spectral projector are basis-free.  The particular
coordinate intertwiner `X` is **not canonical**: postcomposition by an
invertible element of the S_DE centralizer gives another valid basis.  Thus the
proved content is existence of an exact linear conjugacy/similarity class, not
a unique coordinate identification.

Honest scope: this is rational finite operator algebra for the already-owned
normalized scene transport.  It does not identify the archive Laplacian, the
unnormalized rank-3 adjacency, a log-det pressure operator, an EOS, redshift, or
survey data with the S_DE transfer.
-/

namespace D0.Synthesis.PhasonActiveSceneConjugacy

open scoped BigOperators
local notation:70 A " *ᵥ " B => Matrix.mulVec A B

abbrev Mode2 := Fin 2
abbrev Zone3 := Fin 3

/-- The owned row-stochastic zone transport. -/
abbrev sceneTransport : Matrix Zone3 Zone3 ℚ :=
  D0.Spectral.zoneTransport

/-- The normalized scene Laplacian `I - M`. -/
def normalizedSceneLaplacian : Matrix Zone3 Zone3 ℚ :=
  1 - sceneTransport

/-- The owned two-mode S_DE transfer. -/
abbrev sdeTransfer : Matrix Mode2 Mode2 ℚ :=
  D0.Cosmology.phasonFlipTransferMatrix

/-- Explicit active-sector embedding `ℚ² → ℚ³`. -/
def activeEmbedding : Matrix Zone3 Mode2 ℚ :=
  !![-132,   55;
      -24, -120;
      132,   66]

/-- Stationary weight `π_i = n_i d_i` of the zone random walk. -/
def stationaryWeight : Matrix (Fin 1) Zone3 ℚ :=
  !![216, 242, 260]

/-- Uniform right stationary vector of the row-stochastic transport. -/
def stationaryColumn : Matrix Zone3 (Fin 1) ℚ :=
  !![1; 1; 1]

/-- Explicit inverse on the active hyperplane. -/
def activeRetraction : Matrix Mode2 Zone3 ℚ :=
  !![-31 / 7898,  1 / 4308, 175 / 47388;
       13 / 3949, -2 / 359,    9 / 3949]

/-- Basis-free projection along the stationary line onto `ker π`. -/
def activeProjector : Matrix Zone3 Zone3 ℚ :=
  1 - (1 / 718 : ℚ) • (stationaryColumn * stationaryWeight)

/-- The active projector in closed scene-count form. -/
theorem activeProjector_closed_form :
    activeProjector =
      !![251 / 359, -121 / 359, -130 / 359;
         -108 / 359, 238 / 359, -130 / 359;
         -108 / 359, -121 / 359, 229 / 359] := by
  native_decide

/-- The scene weight is stationary: `πM = π`. -/
theorem stationaryWeight_mul_sceneTransport :
    stationaryWeight * sceneTransport = stationaryWeight := by
  native_decide

/-- Total stationary degree mass is `718 = 2·359`. -/
theorem stationaryWeight_total :
    stationaryWeight * stationaryColumn = !![718] := by
  native_decide

/-- The explicit embedding lands in the active hyperplane: `πX = 0`. -/
theorem stationaryWeight_mul_activeEmbedding :
    stationaryWeight * activeEmbedding = 0 := by
  native_decide

/-- **Exact operator intertwining**: `(I-M)X = XT₂`. -/
theorem normalized_scene_sde_intertwining :
    normalizedSceneLaplacian * activeEmbedding =
      activeEmbedding * sdeTransfer := by
  native_decide

/-- The retraction is a left inverse, hence `X` has full column rank. -/
theorem activeRetraction_mul_activeEmbedding :
    activeRetraction * activeEmbedding = 1 := by
  native_decide

/-- The other composite is the basis-free active projector. -/
theorem activeEmbedding_mul_activeRetraction :
    activeEmbedding * activeRetraction = activeProjector := by
  native_decide

/-- Strong split factorization: transport to two modes, apply S_DE, and embed
back gives the full normalized Laplacian. -/
theorem normalizedSceneLaplacian_factorization :
    activeEmbedding * sdeTransfer * activeRetraction =
      normalizedSceneLaplacian := by
  native_decide

/-- The reverse split factorization recovers the S_DE operator exactly. -/
theorem sdeTransfer_factorization :
    activeRetraction * normalizedSceneLaplacian * activeEmbedding =
      sdeTransfer := by
  native_decide

/-- The normalized Laplacian is supported exactly on the active projector. -/
theorem normalizedSceneLaplacian_projector_support :
    normalizedSceneLaplacian * activeProjector = normalizedSceneLaplacian ∧
      activeProjector * normalizedSceneLaplacian = normalizedSceneLaplacian := by
  native_decide

/-- The active projector is also the polynomial spectral projector

`I - (160M² + 160M + 39I)/359`.

The complementary polynomial is the factor of the scene charpoly that is
nonzero at the stationary eigenvalue `1`; this makes the active sector
basis-free rather than a post-hoc choice of `X`.
-/
theorem activeProjector_polynomial :
    activeProjector =
      1 - (1 / 359 : ℚ) •
        (160 • (sceneTransport ^ 2) + 160 • sceneTransport + 39 • (1 : Matrix Zone3 Zone3 ℚ)) := by
  native_decide

/-- The projector kills the stationary line. -/
theorem activeProjector_kills_stationary :
    activeProjector * stationaryColumn = 0 := by
  native_decide

/-- The projector fixes the active embedding. -/
theorem activeProjector_fixes_embedding :
    activeProjector * activeEmbedding = activeEmbedding := by
  native_decide

/-- The active projector is idempotent. -/
theorem activeProjector_idempotent :
    activeProjector * activeProjector = activeProjector := by
  rw [← activeEmbedding_mul_activeRetraction]
  rw [Matrix.mul_assoc]
  rw [← Matrix.mul_assoc activeRetraction activeEmbedding activeRetraction]
  rw [activeRetraction_mul_activeEmbedding, Matrix.one_mul]

/-! ## Universal image characterization -/

/-- The active linear constraint on a zone vector. -/
def IsActive (w : Zone3 → ℚ) : Prop :=
  (stationaryWeight *ᵥ w) = 0

/-- Every embedded two-mode vector satisfies the active constraint. -/
theorem activeEmbedding_mulVec_isActive (v : Mode2 → ℚ) :
    IsActive (activeEmbedding *ᵥ v) := by
  unfold IsActive
  rw [Matrix.mulVec_mulVec, stationaryWeight_mul_activeEmbedding]
  simp

/-- The basis-free projector fixes every vector in `ker π`. -/
theorem activeProjector_mulVec_eq_of_isActive
    (w : Zone3 → ℚ) (hw : IsActive w) :
    (activeProjector *ᵥ w) = w := by
  have hw0 := congrFun hw 0
  funext i
  fin_cases i <;>
    simp [activeProjector, stationaryColumn, stationaryWeight,
      Matrix.mulVec, dotProduct, Matrix.one_apply, Fin.sum_univ_succ] at hw0 ⊢ <;>
    linarith

/-- The image of `X` is exactly the canonical active hyperplane `ker π`. -/
theorem mem_activeEmbedding_image_iff (w : Zone3 → ℚ) :
    (∃ v : Mode2 → ℚ, (activeEmbedding *ᵥ v) = w) ↔ IsActive w := by
  constructor
  · rintro ⟨v, rfl⟩
    exact activeEmbedding_mulVec_isActive v
  · intro hw
    refine ⟨activeRetraction *ᵥ w, ?_⟩
    rw [Matrix.mulVec_mulVec, activeEmbedding_mul_activeRetraction]
    exact activeProjector_mulVec_eq_of_isActive w hw

/-- `X` is injective, witnessed constructively by `Y X = I`. -/
theorem activeEmbedding_mulVec_injective :
    Function.Injective (fun v : Mode2 → ℚ => (activeEmbedding *ᵥ v)) := by
  intro v w hvw
  have h := congrArg (fun z => activeRetraction *ᵥ z) hvw
  simpa [Matrix.mulVec_mulVec, activeRetraction_mul_activeEmbedding] using h

/-! ## Linear conjugacy on the active subtype -/

/-- The stationary-weight functional whose kernel is the active carrier. -/
def activeFunctional : (Zone3 → ℚ) →ₗ[ℚ] (Fin 1 → ℚ) :=
  Matrix.mulVecLin stationaryWeight

/-- Canonical active normalized-scene submodule. -/
def activeSceneSubmodule : Submodule ℚ (Zone3 → ℚ) :=
  LinearMap.ker activeFunctional

/-- Canonical active normalized-scene carrier. -/
abbrev ActiveScene : Type :=
  activeSceneSubmodule

/-- The explicit embedding as a linear map into the active subtype. -/
def activeEmbeddingLinear : (Mode2 → ℚ) →ₗ[ℚ] ActiveScene where
  toFun v := ⟨activeEmbedding *ᵥ v, by
    change IsActive (activeEmbedding *ᵥ v)
    exact activeEmbedding_mulVec_isActive v⟩
  map_add' v w := by
    apply Subtype.ext
    simp [Matrix.mulVec_add]
  map_smul' c v := by
    apply Subtype.ext
    simp [Matrix.mulVec_smul]

/-- The explicit active retraction as a linear map. -/
def activeRetractionLinear : ActiveScene →ₗ[ℚ] (Mode2 → ℚ) where
  toFun w := activeRetraction *ᵥ w.1
  map_add' v w := by simp [Matrix.mulVec_add]
  map_smul' c v := by simp [Matrix.mulVec_smul]

/-- Explicit linear equivalence between the S_DE carrier and the active scene. -/
def activeSceneEquiv : (Mode2 → ℚ) ≃ₗ[ℚ] ActiveScene where
  toLinearMap := activeEmbeddingLinear
  invFun := activeRetractionLinear
  left_inv v := by
    change (activeRetraction *ᵥ (activeEmbedding *ᵥ v)) = v
    simp [Matrix.mulVec_mulVec, activeRetraction_mul_activeEmbedding]
  right_inv w := by
    apply Subtype.ext
    change (activeEmbedding *ᵥ (activeRetraction *ᵥ w.1)) = w.1
    rw [Matrix.mulVec_mulVec, activeEmbedding_mul_activeRetraction]
    exact activeProjector_mulVec_eq_of_isActive w.1 w.2

/-- The S_DE operator on its owned two-mode carrier. -/
def sdeOperator : Module.End ℚ (Mode2 → ℚ) :=
  Matrix.toLinAlgEquiv' sdeTransfer

/-- The normalized scene Laplacian restricted to the canonical active carrier. -/
def activeSceneOperator : Module.End ℚ ActiveScene where
  toFun w :=
    ⟨normalizedSceneLaplacian *ᵥ w.1, by
      change IsActive (normalizedSceneLaplacian *ᵥ w.1)
      unfold IsActive
      rw [Matrix.mulVec_mulVec]
      have hzero : stationaryWeight * normalizedSceneLaplacian = 0 := by
        native_decide
      rw [hzero]
      simp⟩
  map_add' v w := by
    apply Subtype.ext
    simp [Matrix.mulVec_add]
  map_smul' c v := by
    apply Subtype.ext
    simp [Matrix.mulVec_smul]

/-- **Positive capstone.** There exists an explicit linear conjugacy from the
owned S_DE transfer to the normalized scene Laplacian restricted to `ker π`. -/
theorem active_scene_sde_conjugacy :
    activeSceneEquiv.toLinearMap.comp sdeOperator =
      activeSceneOperator.comp activeSceneEquiv.toLinearMap := by
  ext v i
  change
    (activeEmbedding *ᵥ (sdeTransfer *ᵥ Pi.single v 1)) i =
      (normalizedSceneLaplacian *ᵥ (activeEmbedding *ᵥ Pi.single v 1)) i
  rw [Matrix.mulVec_mulVec, Matrix.mulVec_mulVec, normalized_scene_sde_intertwining]

/-! ## Negative controls and non-uniqueness -/

/-- Uniform zero-sum is the wrong active constraint: the degree-stationary
weight `π`, not the uniform row, is load-bearing. -/
def uniformWeight : Matrix (Fin 1) Zone3 ℚ :=
  !![1, 1, 1]

theorem uniformWeight_mul_activeEmbedding :
    uniformWeight * activeEmbedding = !![-24, 1] := by
  native_decide

theorem activeEmbedding_not_uniform_zero_sum :
    uniformWeight * activeEmbedding ≠ 0 := by
  rw [uniformWeight_mul_activeEmbedding]
  native_decide

/-- The chosen coordinates are not canonical: `X` and `2X` are distinct
full-rank intertwiners with the same active image. -/
theorem active_intertwiner_coordinate_nonunique :
    (2 : ℚ) • activeEmbedding ≠ activeEmbedding ∧
      normalizedSceneLaplacian * ((2 : ℚ) • activeEmbedding) =
        ((2 : ℚ) • activeEmbedding) * sdeTransfer ∧
      (∀ w : Zone3 → ℚ,
        (∃ v, (((2 : ℚ) • activeEmbedding) *ᵥ v) = w) ↔ IsActive w) := by
  refine ⟨?_, ?_, ?_⟩
  · intro h
    have h00 := congrArg (fun M : Matrix Zone3 Mode2 ℚ => M 0 0) h
    norm_num [activeEmbedding] at h00
  · rw [Matrix.mul_smul, normalized_scene_sde_intertwining, Matrix.smul_mul]
  · intro w
    rw [← mem_activeEmbedding_image_iff]
    constructor
    · rintro ⟨v, rfl⟩
      refine ⟨(2 : ℚ) • v, ?_⟩
      rw [Matrix.mulVec_smul, Matrix.smul_mulVec]
    · rintro ⟨v, hv⟩
      refine ⟨(1 / 2 : ℚ) • v, ?_⟩
      rw [← hv]
      rw [Matrix.smul_mulVec, Matrix.mulVec_smul, smul_smul]
      norm_num

/-- The earlier no-go remains exact for the **unnormalized cubic** quotient:
every rational intertwiner from this same S_DE transfer into that quotient is
zero.  Normalization and active-sector restriction are therefore load-bearing.
-/
theorem unnormalized_cubic_intertwiner_still_zero
    (F : (Fin 2 → ℚ) →ₗ[ℚ] (Fin 3 → ℚ))
    (hIntertwines :
      F.comp
          D0.Synthesis.SDECubicSpectralDisjointness.ownedSDETransferOperator =
        D0.Synthesis.SDECubicSpectralDisjointness.ownedSceneQuotientOperator.comp F) :
    F = 0 :=
  D0.Synthesis.SDECubicSpectralDisjointness.concrete_owned_intertwiner_is_zero
    F hIntertwines

end D0.Synthesis.PhasonActiveSceneConjugacy
