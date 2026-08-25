import Mathlib.Tactic
import D0.Claims.Signature31Split
import D0.Integration.V15.RawZone
import D0.Spectral.ZoneMatrixSpectrum

/-!
# Full-scene provenance of the normalized zone quotient

The normalized zone transport used by `PhasonActiveSceneConjugacy` was previously
arithmetically owned, but its descent from the literal `33 × 33` scene adjacency was
not.  This module closes that map.

Let `C : ℚ³ → ℚ³³` be the literal zone-indicator matrix.  We prove

* `Adj31 · C = C · AWq`: the existing `A_W` is the unique adjacency induced on
  zone-constant vectors;
* `Dfull · C = C · DWq` and `Dfull⁻¹ · C = C · DWinv`, where `Dfull` is computed
  from the row sums of the literal adjacency;
* `zoneTransport = DWinv · AWq`;
* consequently `Pfull · C = C · zoneTransport` and
  `(I - Pfull) · C = C · (I - zoneTransport)`.

Thus `I - zoneTransport` is not an isolated matrix: it is the normalized Laplacian
induced by the full scene graph on the canonical degree-zone quotient.

The stationary quotient weight is also descended from the full degree measure:
`π = (9·24, 11·22, 13·20) = (216,242,260)`.  Detailed balance is proved exactly.

**Canonicality and scope.**  For this frozen scene, equality of adjacency row degrees
is equivalent to equality of zones, so the three quotient cells are intrinsically
recoverable from the full graph.  Their displayed order is still a coordinate choice;
the operator without that order is canonical up to permutation similarity.  Unequal
row degrees are load-bearing for the intrinsic coordinate labels, while nonzero row
degrees are what make normalization possible.

Normalization alone forgets common scale, and therefore cannot recover the absolute
orbit sizes or the homological passport without `AWq`, `DWq`, or the counting measure.
No physical identification of the normalized active sector is asserted here.
-/

namespace D0.Synthesis.SceneNormalizedQuotientDescent

open Matrix
open scoped BigOperators

abbrev Vertex33 := Fin 33
abbrev Zone3 := Fin 3

/-! ## The existing quotient matrices, now connected to the literal graph -/

/-- Rational cast of the already-owned unnormalized zone adjacency `A_W`. -/
def AWq : Matrix Zone3 Zone3 ℚ :=
  fun i j => (D0.Integration.V15.RawZone.AW i j : ℚ)

/-- Rational cast of the already-owned zone degree matrix `D_W`. -/
def DWq : Matrix Zone3 Zone3 ℚ :=
  fun i j => (D0.Integration.V15.RawZone.DW i j : ℚ)

/-- The explicit inverse of `D_W`. -/
def DWinv : Matrix Zone3 Zone3 ℚ :=
  !![1 / 24, 0, 0;
     0, 1 / 22, 0;
     0, 0, 1 / 20]

/-- The frozen quotient degree values in the `9,11,13` zone order. -/
def zoneDegree : Zone3 → ℚ := ![24, 22, 20]

/-- The actual degree of a vertex, computed as a row sum of the literal adjacency. -/
def fullDegreeValue (i : Vertex33) : ℚ :=
  ∑ j, D0.Claims.Adj31 i j

/-- Full diagonal degree matrix computed from `Adj31`, not postulated by zone. -/
def fullDegree : Matrix Vertex33 Vertex33 ℚ :=
  Matrix.diagonal fullDegreeValue

/-- Full inverse-degree matrix. -/
def fullDegreeInv : Matrix Vertex33 Vertex33 ℚ :=
  Matrix.diagonal fun i => (fullDegreeValue i)⁻¹

/-- Random-walk normalization of the literal full adjacency. -/
def fullTransport : Matrix Vertex33 Vertex33 ℚ :=
  fullDegreeInv * D0.Claims.Adj31

/-- Normalized Laplacian of the literal full scene graph. -/
def fullNormalizedLaplacian : Matrix Vertex33 Vertex33 ℚ :=
  1 - fullTransport

/-- Normalized Laplacian of the induced zone transport. -/
def quotientNormalizedLaplacian : Matrix Zone3 Zone3 ℚ :=
  1 - D0.Spectral.zoneTransport

/-- Row restriction to the three fixed representative vertices. -/
def representativeRestriction : Matrix Zone3 Vertex33 ℚ :=
  Matrix.of fun z i => if i = D0.Claims.rep31 z then 1 else 0

/-! ## Exact descent from the literal `33 × 33` graph -/

/-- The pattern-indicator product counts the vertices in each target zone and is
exactly the existing unnormalized quotient adjacency. -/
theorem pattern_indicator_eq_AWq :
    D0.Claims.Bpat31 * D0.Claims.Cind31 = AWq := by
  native_decide

/-- **Actual adjacency provenance.**  The full literal adjacency preserves the
zone-constant subspace and induces `AWq` there. -/
theorem adjacency_indicator_intertwining :
    D0.Claims.Adj31 * D0.Claims.Cind31 =
      D0.Claims.Cind31 * AWq := by
  rw [D0.Claims.adj31_factor, Matrix.mul_assoc, pattern_indicator_eq_AWq]

/-- Restriction to one vertex per zone is a left inverse to the zone lift. -/
theorem representativeRestriction_indicator :
    representativeRestriction * D0.Claims.Cind31 = 1 := by
  native_decide

/-- The induced adjacency is unique once the canonical zone-indicator lift is fixed. -/
theorem induced_adjacency_unique
    (T : Matrix Zone3 Zone3 ℚ)
    (hT : D0.Claims.Adj31 * D0.Claims.Cind31 =
      D0.Claims.Cind31 * T) :
    T = AWq := by
  calc
    T = 1 * T := by rw [Matrix.one_mul]
    _ = (representativeRestriction * D0.Claims.Cind31) * T := by
      rw [representativeRestriction_indicator]
    _ = representativeRestriction * (D0.Claims.Cind31 * T) := by
      rw [Matrix.mul_assoc]
    _ = representativeRestriction *
        (D0.Claims.Adj31 * D0.Claims.Cind31) := by rw [← hT]
    _ = representativeRestriction *
        (D0.Claims.Cind31 * AWq) := by
      rw [adjacency_indicator_intertwining]
    _ = (representativeRestriction * D0.Claims.Cind31) * AWq := by
      rw [Matrix.mul_assoc]
    _ = AWq := by rw [representativeRestriction_indicator, Matrix.one_mul]

/-- The literal adjacency row sum is exactly the corresponding quotient degree. -/
theorem fullDegreeValue_eq_zoneDegree :
    ∀ i, fullDegreeValue i = zoneDegree (D0.Claims.zone31 i) := by
  native_decide

/-- **Intrinsic cell recovery.**  Two vertices have equal graph degree exactly when
they lie in the same zone.  Pairwise unequal row degrees are load-bearing here. -/
theorem equal_fullDegree_iff_same_zone :
    ∀ i j, fullDegreeValue i = fullDegreeValue j ↔
      D0.Claims.zone31 i = D0.Claims.zone31 j := by
  native_decide

/-- The full degree operator descends to the owned quotient degree operator. -/
theorem fullDegree_indicator_intertwining :
    fullDegree * D0.Claims.Cind31 =
      D0.Claims.Cind31 * DWq := by
  native_decide

/-- `DWinv` is genuinely the two-sided inverse of the nonzero quotient degree matrix. -/
theorem DWinv_inverse :
    DWinv * DWq = 1 ∧ DWq * DWinv = 1 := by
  constructor <;> native_decide

/-- The full inverse-degree operator descends to `DWinv`. -/
theorem fullDegreeInv_indicator_intertwining :
    fullDegreeInv * D0.Claims.Cind31 =
      D0.Claims.Cind31 * DWinv := by
  native_decide

/-- **Normalization provenance.**  The previously-owned row-stochastic matrix is
exactly `D_W⁻¹ A_W`. -/
theorem zoneTransport_eq_DWinv_mul_AWq :
    D0.Spectral.zoneTransport = DWinv * AWq := by
  native_decide

/-- **Full normalized descent.**  The random walk of the literal `33 × 33` graph
induces the owned zone transport on zone-constant vectors. -/
theorem fullTransport_indicator_intertwining :
    fullTransport * D0.Claims.Cind31 =
      D0.Claims.Cind31 * D0.Spectral.zoneTransport := by
  unfold fullTransport
  calc
    (fullDegreeInv * D0.Claims.Adj31) * D0.Claims.Cind31 =
        fullDegreeInv *
          (D0.Claims.Adj31 * D0.Claims.Cind31) := by
      rw [Matrix.mul_assoc]
    _ = fullDegreeInv * (D0.Claims.Cind31 * AWq) := by
      rw [adjacency_indicator_intertwining]
    _ = (fullDegreeInv * D0.Claims.Cind31) * AWq := by
      rw [Matrix.mul_assoc]
    _ = (D0.Claims.Cind31 * DWinv) * AWq := by
      rw [fullDegreeInv_indicator_intertwining]
    _ = D0.Claims.Cind31 * (DWinv * AWq) := by
      rw [Matrix.mul_assoc]
    _ = D0.Claims.Cind31 * D0.Spectral.zoneTransport := by
      rw [zoneTransport_eq_DWinv_mul_AWq]

/-- The full normalized adjacency is itself row-stochastic. -/
theorem fullTransport_row_stochastic :
    ∀ i, ∑ j, fullTransport i j = 1 := by
  native_decide

/-- The induced normalized transport is unique on the canonical indicator image. -/
theorem induced_transport_unique
    (T : Matrix Zone3 Zone3 ℚ)
    (hT : fullTransport * D0.Claims.Cind31 =
      D0.Claims.Cind31 * T) :
    T = D0.Spectral.zoneTransport := by
  calc
    T = 1 * T := by rw [Matrix.one_mul]
    _ = (representativeRestriction * D0.Claims.Cind31) * T := by
      rw [representativeRestriction_indicator]
    _ = representativeRestriction * (D0.Claims.Cind31 * T) := by
      rw [Matrix.mul_assoc]
    _ = representativeRestriction *
        (fullTransport * D0.Claims.Cind31) := by rw [← hT]
    _ = representativeRestriction *
        (D0.Claims.Cind31 * D0.Spectral.zoneTransport) := by
      rw [fullTransport_indicator_intertwining]
    _ = (representativeRestriction * D0.Claims.Cind31) *
        D0.Spectral.zoneTransport := by rw [Matrix.mul_assoc]
    _ = D0.Spectral.zoneTransport := by
      rw [representativeRestriction_indicator, Matrix.one_mul]

/-- **Normalized Laplacian descent.**  `I-M` is the actual induced normalized
Laplacian of the full graph, not a separately chosen operator. -/
theorem full_laplacian_indicator_intertwining :
    fullNormalizedLaplacian * D0.Claims.Cind31 =
      D0.Claims.Cind31 * quotientNormalizedLaplacian := by
  unfold fullNormalizedLaplacian quotientNormalizedLaplacian
  calc
    (1 - fullTransport) * D0.Claims.Cind31 =
        D0.Claims.Cind31 -
          fullTransport * D0.Claims.Cind31 := by
      rw [Matrix.sub_mul, Matrix.one_mul]
    _ = D0.Claims.Cind31 -
        D0.Claims.Cind31 * D0.Spectral.zoneTransport := by
      rw [fullTransport_indicator_intertwining]
    _ = D0.Claims.Cind31 * (1 - D0.Spectral.zoneTransport) := by
      rw [Matrix.mul_sub, Matrix.mul_one]

/-! ## Stationarity and detailed balance, descended from the full graph -/

/-- The stationary quotient weight `π_i = |Z_i| d_i`. -/
def stationaryWeight : Matrix (Fin 1) Zone3 ℚ :=
  !![216, 242, 260]

/-- Diagonal form of the stationary weight. -/
def stationaryDiagonal : Matrix Zone3 Zone3 ℚ :=
  !![216, 0, 0;
     0, 242, 0;
     0, 0, 260]

/-- Full degree measure of the literal undirected graph. -/
def fullStationaryWeight : Matrix (Fin 1) Vertex33 ℚ :=
  Matrix.of fun _ i => fullDegreeValue i

/-- The quotient stationary measure is the pushforward of the full degree measure. -/
theorem fullStationaryWeight_indicator :
    fullStationaryWeight * D0.Claims.Cind31 = stationaryWeight := by
  native_decide

/-- The full degree measure is stationary for the full random walk. -/
theorem fullStationaryWeight_stationary :
    fullStationaryWeight * fullTransport = fullStationaryWeight := by
  native_decide

/-- The descended weight `π=(216,242,260)` is stationary for `zoneTransport`. -/
theorem stationaryWeight_stationary :
    stationaryWeight * D0.Spectral.zoneTransport = stationaryWeight := by
  native_decide

/-- Exact detailed balance: `diag(π) M` is symmetric. -/
theorem zoneTransport_detailed_balance :
    (stationaryDiagonal * D0.Spectral.zoneTransport)ᵀ =
      stationaryDiagonal * D0.Spectral.zoneTransport := by
  native_decide

/-! ## Destructive controls -/

/-- A tempting uniform row normalization by `24` is not the true transport. -/
def uniformNormalization : Matrix Zone3 Zone3 ℚ :=
  (1 / 24 : ℚ) • AWq

/-- Unequal row degrees are operational: uniform normalization changes the operator. -/
theorem uniformNormalization_ne_zoneTransport :
    uniformNormalization ≠ D0.Spectral.zoneTransport := by
  native_decide

/-- The unnormalized quotient adjacency is not row-stochastic. -/
theorem AWq_not_row_stochastic :
    ¬ (∀ i, ∑ j, AWq i j = 1) := by
  native_decide

/-- The uniformly normalized matrix is still not row-stochastic because the three
row degrees are `24,22,20`, not equal. -/
theorem uniformNormalization_not_row_stochastic :
    ¬ (∀ i, ∑ j, uniformNormalization i j = 1) := by
  native_decide

/-- Normalization forgets a common scale.  Hence `M` alone cannot reconstruct absolute
orbit sizes or the homological passport; one must retain `AWq`, `DWq`, or counting data. -/
theorem normalization_forgets_common_scale :
    ((1 / 2 : ℚ) • DWinv) * ((2 : ℚ) • AWq) =
        D0.Spectral.zoneTransport ∧
      (2 : ℚ) • AWq ≠ AWq := by
  constructor <;> native_decide

/-- Pairwise unequal quotient row degrees, the finite fact behind intrinsic zone labels
and the failure of uniform normalization. -/
theorem quotient_degrees_pairwise_distinct :
    (24 : ℚ) ≠ 22 ∧ (24 : ℚ) ≠ 20 ∧ (22 : ℚ) ≠ 20 := by
  norm_num

/-! ## Capstone -/

/-- **D0-SCENE-NORMALIZED-QUOTIENT-DESCENT.**  One theorem packages the actual
full-graph-to-normalized-quotient provenance used by the downstream active-sector
conjugacy. -/
theorem scene_normalized_quotient_descent :
    D0.Claims.Adj31 * D0.Claims.Cind31 =
        D0.Claims.Cind31 * AWq ∧
      fullDegree * D0.Claims.Cind31 =
        D0.Claims.Cind31 * DWq ∧
      D0.Spectral.zoneTransport = DWinv * AWq ∧
      fullTransport * D0.Claims.Cind31 =
        D0.Claims.Cind31 * D0.Spectral.zoneTransport ∧
      fullNormalizedLaplacian * D0.Claims.Cind31 =
        D0.Claims.Cind31 * quotientNormalizedLaplacian ∧
      stationaryWeight * D0.Spectral.zoneTransport = stationaryWeight ∧
      (stationaryDiagonal * D0.Spectral.zoneTransport)ᵀ =
        stationaryDiagonal * D0.Spectral.zoneTransport :=
  ⟨adjacency_indicator_intertwining, fullDegree_indicator_intertwining,
    zoneTransport_eq_DWinv_mul_AWq, fullTransport_indicator_intertwining,
    full_laplacian_indicator_intertwining, stationaryWeight_stationary,
    zoneTransport_detailed_balance⟩

end D0.Synthesis.SceneNormalizedQuotientDescent
