import Mathlib.Tactic
import D0.Synthesis.SceneNormalizedQuotientDescent
import D0.Claims.InvariantGenerationBridge

/-!
# Intrinsic reconstruction of the scene quotient

`SceneNormalizedQuotientDescent` proves the correct full-scene descent using the
hand-displayed zone indicator `Cind31` and a restriction to three representative
vertices.  This module removes both choices from the construction.

Start only with the literal adjacency and its row-sum degree operator `Dfull`.  Since
the three degree values `24,22,20` are distinct, the three Lagrange polynomials in
`Dfull` recover its spectral blocks.  Taking the diagonal of each block gives its
canonical `0/1` membership vector.  The traces of the same projectors recover the
block masses `9,11,13`, so normalized transposition gives an averaging left inverse.

Consequently the quotient matrices are intrinsic compressions

`Rdeg · Adj31 · Cdeg`, `Rdeg · Pfull · Cdeg`, and
`Rdeg · (I-Pfull) · Cdeg`.

No representative vertex occurs in any definition.  The reconstructed lift is proved
to equal `Cind31` in the degree order `(24,22,20)`, but that equality is a comparison
certificate rather than an input.  Its image projector is also exactly the already
owned Reynolds/generation projector.

Two boundaries are explicit:

* changing the order of the three degree labels conjugates every quotient by a
  permutation matrix;
* rescaling the three indicator columns changes quotient coordinates by diagonal
  similarity, while leaving their image projector unchanged.

Thus the quotient subspace and its induced operators are canonical.  A displayed
`3 × 3` matrix still contains an ordering/normalization convention; a choice of one
representative vertex per cell is neither canonical nor necessary.
-/

namespace D0.Synthesis.IntrinsicQuotientReconstruction

open Matrix

abbrev Vertex33 := Fin 33
abbrev Fibre3 := Fin 3

open D0.Synthesis.SceneNormalizedQuotientDescent

/-! ## Spectral blocks of the literal degree operator -/

/-- Degree-24 spectral block, as a Lagrange polynomial in the literal row-sum
degree operator. -/
def fullFibre24 : Matrix Vertex33 Vertex33 ℚ :=
  (1 / 8 : ℚ) •
    ((fullDegree - (22 : ℚ) • 1) *
      (fullDegree - (20 : ℚ) • 1))

/-- Degree-22 spectral block. -/
def fullFibre22 : Matrix Vertex33 Vertex33 ℚ :=
  (-1 / 4 : ℚ) •
    ((fullDegree - (24 : ℚ) • 1) *
      (fullDegree - (20 : ℚ) • 1))

/-- Degree-20 spectral block. -/
def fullFibre20 : Matrix Vertex33 Vertex33 ℚ :=
  (1 / 8 : ℚ) •
    ((fullDegree - (24 : ℚ) • 1) *
      (fullDegree - (22 : ℚ) • 1))

/-- The three spectral projectors, indexed in the explicit degree order
`(24,22,20)`.  The family is intrinsic; this enumeration is a quotient-coordinate
choice. -/
def fullDegreeFibre : Fibre3 → Matrix Vertex33 Vertex33 ℚ
  | 0 => fullFibre24
  | 1 => fullFibre22
  | 2 => fullFibre20

/-- Entrywise block recovery: the Lagrange projector is exactly the diagonal
coordinate projector onto the vertices of the corresponding degree fibre. -/
theorem fullDegreeFibre_apply (z : Fibre3) (i j : Vertex33) :
    fullDegreeFibre z i j =
      if i = j ∧ D0.Claims.zone31 i = z then 1 else 0 := by
  native_decide +revert

/-- The literal spectral blocks are pairwise orthogonal, complete, and idempotent. -/
theorem full_degree_spectral_blocks :
    (∀ z, fullDegreeFibre z * fullDegreeFibre z = fullDegreeFibre z) ∧
    fullDegreeFibre 0 + fullDegreeFibre 1 + fullDegreeFibre 2 =
      (1 : Matrix Vertex33 Vertex33 ℚ) ∧
    fullDegreeFibre 0 * fullDegreeFibre 1 = 0 ∧
    fullDegreeFibre 0 * fullDegreeFibre 2 = 0 ∧
    fullDegreeFibre 1 * fullDegreeFibre 2 = 0 := by
  constructor
  · intro z
    ext i j
    simp only [Matrix.mul_apply]
    rw [Finset.sum_eq_single i]
    · simp only [fullDegreeFibre_apply]
      by_cases h : D0.Claims.zone31 i = z <;> simp [h]
    · intro k _ hki
      rw [fullDegreeFibre_apply]
      simp [Ne.symm hki]
    · intro hi
      exact absurd (Finset.mem_univ i) hi
  · native_decide

/-! ## The indicator and averaging restriction are recovered, not supplied -/

/-- Canonically normalized membership lift: take the diagonal of each literal
degree-spectral projector. -/
def intrinsicIndicator : Matrix Vertex33 Fibre3 ℚ :=
  fun i z => fullDegreeFibre z i i

/-- Trace/multiplicity of a recovered degree block. -/
def intrinsicFibreMass (z : Fibre3) : ℚ :=
  Matrix.trace (fullDegreeFibre z)

/-- The three cell sizes are recovered from the literal degree spectrum. -/
theorem intrinsicFibreMass_values :
    intrinsicFibreMass = ![(9 : ℚ), 11, 13] := by
  funext z
  fin_cases z <;> native_decide

/-- Averaging restriction, normalized by the recovered spectral multiplicities.
Unlike `representativeRestriction`, this chooses no vertex in any cell. -/
def intrinsicRestriction : Matrix Fibre3 Vertex33 ℚ :=
  fun z i => (intrinsicFibreMass z)⁻¹ * intrinsicIndicator i z

/-- The reconstructed indicator agrees with the old displayed indicator in the
chosen degree order.  `Cind31` is not used by the construction. -/
theorem intrinsicIndicator_eq_Cind31 :
    intrinsicIndicator = D0.Claims.Cind31 := by
  ext i z
  rw [intrinsicIndicator, fullDegreeFibre_apply]
  simp [D0.Claims.Cind31]

/-- Canonical averaging is a left inverse to the recovered lift. -/
theorem intrinsicRestriction_indicator :
    intrinsicRestriction * intrinsicIndicator =
      (1 : Matrix Fibre3 Fibre3 ℚ) := by
  native_decide

/-- The averaging inverse is genuinely different from choosing the fixed
representatives `0,9,20`. -/
theorem intrinsicRestriction_ne_representativeRestriction :
    intrinsicRestriction ≠ representativeRestriction := by
  native_decide

/-! ## The quotient image is the already-owned invariant/generation space -/

/-- The canonical projector onto vectors which are constant on each recovered
degree fibre. -/
def intrinsicQuotientProjector : Matrix Vertex33 Vertex33 ℚ :=
  intrinsicIndicator * intrinsicRestriction

/-- The spectral reconstruction and the independent zone-map construction give
the same three-dimensional averaging projector. -/
theorem intrinsicQuotientProjector_eq_zoneProjector :
    intrinsicQuotientProjector =
      D0.Claims.InvariantGenerationBridge.Q := by
  native_decide

/-- Stronger owner identification: the reconstructed quotient image is exactly the
Reynolds fixed space computed from the literal list of within-zone generators. -/
theorem intrinsicQuotientProjector_eq_reynolds :
    intrinsicQuotientProjector =
      D0.Claims.InvariantGenerationBridge.P := by
  rw [D0.Claims.InvariantGenerationBridge.bridge_projector_eq]
  exact intrinsicQuotientProjector_eq_zoneProjector

/-- The quotient image is a symmetric rank-three projector, inherited from the
independent invariant-generation owner. -/
theorem intrinsicQuotientProjector_certificate :
    intrinsicQuotientProjector * intrinsicQuotientProjector =
        intrinsicQuotientProjector ∧
      intrinsicQuotientProjectorᵀ = intrinsicQuotientProjector ∧
      Matrix.trace intrinsicQuotientProjector = 3 := by
  rw [intrinsicQuotientProjector_eq_zoneProjector]
  exact
    ⟨D0.Claims.InvariantGenerationBridge.q_idempotent,
      D0.Claims.InvariantGenerationBridge.q_symmetric,
      D0.Claims.InvariantGenerationBridge.q_trace_three⟩

/-! ## Representative-free induced operators -/

/-- Intrinsic compression of the literal adjacency. -/
def reconstructedAdjacency : Matrix Fibre3 Fibre3 ℚ :=
  intrinsicRestriction * D0.Claims.Adj31 * intrinsicIndicator

/-- Intrinsic compression of the literal degree operator. -/
def reconstructedDegree : Matrix Fibre3 Fibre3 ℚ :=
  intrinsicRestriction * fullDegree * intrinsicIndicator

/-- Intrinsic compression of the literal full random walk. -/
def reconstructedTransport : Matrix Fibre3 Fibre3 ℚ :=
  intrinsicRestriction * fullTransport * intrinsicIndicator

/-- Intrinsic compression of the literal normalized Laplacian. -/
def reconstructedNormalizedLaplacian : Matrix Fibre3 Fibre3 ℚ :=
  intrinsicRestriction * fullNormalizedLaplacian * intrinsicIndicator

/-- The representative-free compression recovers the owned unnormalized quotient
adjacency exactly. -/
theorem reconstructedAdjacency_eq_AWq :
    reconstructedAdjacency = AWq := by
  unfold reconstructedAdjacency
  rw [intrinsicIndicator_eq_Cind31]
  calc
    intrinsicRestriction * D0.Claims.Adj31 * D0.Claims.Cind31 =
        intrinsicRestriction *
          (D0.Claims.Adj31 * D0.Claims.Cind31) := by
      rw [Matrix.mul_assoc]
    _ = intrinsicRestriction * (D0.Claims.Cind31 * AWq) := by
      rw [adjacency_indicator_intertwining]
    _ = (intrinsicRestriction * D0.Claims.Cind31) * AWq := by
      rw [Matrix.mul_assoc]
    _ = AWq := by
      rw [← intrinsicIndicator_eq_Cind31, intrinsicRestriction_indicator,
        Matrix.one_mul]

/-- The same compression recovers the quotient degree operator. -/
theorem reconstructedDegree_eq_DWq :
    reconstructedDegree = DWq := by
  unfold reconstructedDegree
  rw [intrinsicIndicator_eq_Cind31]
  calc
    intrinsicRestriction * fullDegree * D0.Claims.Cind31 =
        intrinsicRestriction * (fullDegree * D0.Claims.Cind31) := by
      rw [Matrix.mul_assoc]
    _ = intrinsicRestriction * (D0.Claims.Cind31 * DWq) := by
      rw [fullDegree_indicator_intertwining]
    _ = (intrinsicRestriction * D0.Claims.Cind31) * DWq := by
      rw [Matrix.mul_assoc]
    _ = DWq := by
      rw [← intrinsicIndicator_eq_Cind31, intrinsicRestriction_indicator,
        Matrix.one_mul]

/-- The normalized scene transport is reconstructed directly from the literal
random walk, with no representative rows. -/
theorem reconstructedTransport_eq_zoneTransport :
    reconstructedTransport = D0.Spectral.zoneTransport := by
  unfold reconstructedTransport
  rw [intrinsicIndicator_eq_Cind31]
  calc
    intrinsicRestriction * fullTransport * D0.Claims.Cind31 =
        intrinsicRestriction * (fullTransport * D0.Claims.Cind31) := by
      rw [Matrix.mul_assoc]
    _ = intrinsicRestriction *
        (D0.Claims.Cind31 * D0.Spectral.zoneTransport) := by
      rw [fullTransport_indicator_intertwining]
    _ = (intrinsicRestriction * D0.Claims.Cind31) *
        D0.Spectral.zoneTransport := by
      rw [Matrix.mul_assoc]
    _ = D0.Spectral.zoneTransport := by
      rw [← intrinsicIndicator_eq_Cind31, intrinsicRestriction_indicator,
        Matrix.one_mul]

/-- The normalized quotient Laplacian is likewise an intrinsic compression. -/
theorem reconstructedNormalizedLaplacian_eq_quotient :
    reconstructedNormalizedLaplacian = quotientNormalizedLaplacian := by
  unfold reconstructedNormalizedLaplacian
  rw [intrinsicIndicator_eq_Cind31]
  calc
    intrinsicRestriction * fullNormalizedLaplacian * D0.Claims.Cind31 =
        intrinsicRestriction *
          (fullNormalizedLaplacian * D0.Claims.Cind31) := by
      rw [Matrix.mul_assoc]
    _ = intrinsicRestriction *
        (D0.Claims.Cind31 * quotientNormalizedLaplacian) := by
      rw [full_laplacian_indicator_intertwining]
    _ = (intrinsicRestriction * D0.Claims.Cind31) *
        quotientNormalizedLaplacian := by
      rw [Matrix.mul_assoc]
    _ = quotientNormalizedLaplacian := by
      rw [← intrinsicIndicator_eq_Cind31, intrinsicRestriction_indicator,
        Matrix.one_mul]

/-- The reconstructed adjacency is characterized without mentioning the old
indicator or any representative restriction. -/
theorem reconstructed_adjacency_unique
    (T : Matrix Fibre3 Fibre3 ℚ)
    (hT : D0.Claims.Adj31 * intrinsicIndicator =
      intrinsicIndicator * T) :
    T = reconstructedAdjacency := by
  calc
    T = 1 * T := by rw [Matrix.one_mul]
    _ = (intrinsicRestriction * intrinsicIndicator) * T := by
      rw [intrinsicRestriction_indicator]
    _ = intrinsicRestriction * (intrinsicIndicator * T) := by
      rw [Matrix.mul_assoc]
    _ = intrinsicRestriction * (D0.Claims.Adj31 * intrinsicIndicator) := by
      rw [← hT]
    _ = intrinsicRestriction * D0.Claims.Adj31 * intrinsicIndicator := by
      rw [Matrix.mul_assoc]
    _ = reconstructedAdjacency := rfl

/-- The reconstructed transport has the same intrinsic uniqueness property. -/
theorem reconstructed_transport_unique
    (T : Matrix Fibre3 Fibre3 ℚ)
    (hT : fullTransport * intrinsicIndicator = intrinsicIndicator * T) :
    T = reconstructedTransport := by
  calc
    T = 1 * T := by rw [Matrix.one_mul]
    _ = (intrinsicRestriction * intrinsicIndicator) * T := by
      rw [intrinsicRestriction_indicator]
    _ = intrinsicRestriction * (intrinsicIndicator * T) := by
      rw [Matrix.mul_assoc]
    _ = intrinsicRestriction * (fullTransport * intrinsicIndicator) := by
      rw [← hT]
    _ = intrinsicRestriction * fullTransport * intrinsicIndicator := by
      rw [Matrix.mul_assoc]
    _ = reconstructedTransport := rfl

/-! ## Exact full-operator factorization and the archive -/

/-- The canonical quotient projector acts identically on the reconstructed
indicator lift. -/
theorem intrinsicQuotientProjector_indicator :
    intrinsicQuotientProjector * intrinsicIndicator =
      intrinsicIndicator := by
  unfold intrinsicQuotientProjector
  rw [Matrix.mul_assoc, intrinsicRestriction_indicator, Matrix.mul_one]

/-- The literal adjacency is symmetric.  This small structural fact lets us obtain
right invariance of the quotient projector from its obvious left invariance, without
an entrywise `33 × 33` computation. -/
theorem Adj31_transpose :
    D0.Claims.Adj31ᵀ = D0.Claims.Adj31 := by
  ext i j
  simp only [Matrix.transpose_apply, D0.Claims.Adj31, Matrix.of_apply]
  by_cases h : D0.Claims.zone31 i = D0.Claims.zone31 j
  · rw [if_pos h.symm, if_pos h]
  · have h' : D0.Claims.zone31 j ≠ D0.Claims.zone31 i := by
      exact fun hji => h hji.symm
    rw [if_neg h', if_neg h]

/-- The quotient projector is a left identity on the literal adjacency.  This is
purely the old rank-three factorization `Adj31 = Cind31 · Bpat31` plus the newly
reconstructed left inverse; no full-matrix decision procedure is used. -/
theorem intrinsicQuotientProjector_mul_Adj31 :
    intrinsicQuotientProjector * D0.Claims.Adj31 =
      D0.Claims.Adj31 := by
  rw [D0.Claims.adj31_factor]
  calc
    intrinsicQuotientProjector *
        (D0.Claims.Cind31 * D0.Claims.Bpat31) =
      intrinsicQuotientProjector *
        (intrinsicIndicator * D0.Claims.Bpat31) := by
          rw [intrinsicIndicator_eq_Cind31]
    _ = (intrinsicQuotientProjector * intrinsicIndicator) *
        D0.Claims.Bpat31 := by rw [Matrix.mul_assoc]
    _ = intrinsicIndicator * D0.Claims.Bpat31 := by
      rw [intrinsicQuotientProjector_indicator]
    _ = D0.Claims.Cind31 * D0.Claims.Bpat31 := by
      rw [intrinsicIndicator_eq_Cind31]

/-- By symmetry of both factors, the quotient projector is also a right identity
on the literal adjacency. -/
theorem Adj31_mul_intrinsicQuotientProjector :
    D0.Claims.Adj31 * intrinsicQuotientProjector =
      D0.Claims.Adj31 := by
  have h :=
    congrArg Matrix.transpose intrinsicQuotientProjector_mul_Adj31
  simpa [Matrix.transpose_mul, Adj31_transpose,
    intrinsicQuotientProjector_certificate.2.1] using h

/-- The full random walk depends only on fibre averages. -/
theorem fullTransport_mul_intrinsicQuotientProjector :
    fullTransport * intrinsicQuotientProjector = fullTransport := by
  unfold fullTransport
  rw [Matrix.mul_assoc, Adj31_mul_intrinsicQuotientProjector]

/-- The reconstructed lift intertwines the full random walk with the reconstructed
transport, without referring to the old indicator in the theorem statement. -/
theorem fullTransport_intrinsic_intertwining :
    fullTransport * intrinsicIndicator =
      intrinsicIndicator * reconstructedTransport := by
  rw [reconstructedTransport_eq_zoneTransport, intrinsicIndicator_eq_Cind31]
  exact fullTransport_indicator_intertwining

/-- **Exact full factorization.**  The literal `33 × 33` random walk is lift,
reconstructed `3 × 3` transport, and canonical orbit averaging. -/
theorem fullTransport_intrinsic_factorization :
    fullTransport =
      intrinsicIndicator * reconstructedTransport * intrinsicRestriction := by
  calc
    fullTransport =
        fullTransport * intrinsicQuotientProjector :=
      fullTransport_mul_intrinsicQuotientProjector.symm
    _ = fullTransport * (intrinsicIndicator * intrinsicRestriction) := rfl
    _ = (fullTransport * intrinsicIndicator) * intrinsicRestriction := by
      rw [Matrix.mul_assoc]
    _ = (intrinsicIndicator * reconstructedTransport) *
        intrinsicRestriction := by
      rw [fullTransport_intrinsic_intertwining]

/-- Equivalent factorization in the previously-owned quotient coordinates. -/
theorem fullTransport_zoneTransport_factorization :
    fullTransport =
      intrinsicIndicator * D0.Spectral.zoneTransport * intrinsicRestriction := by
  rw [← reconstructedTransport_eq_zoneTransport]
  exact fullTransport_intrinsic_factorization

/-- The quotient projector is also a left identity on the full transport.  Unlike
right invariance above, this now follows abstractly from the exact factorization. -/
theorem intrinsicQuotientProjector_mul_fullTransport :
    intrinsicQuotientProjector * fullTransport = fullTransport := by
  rw [fullTransport_intrinsic_factorization]
  unfold intrinsicQuotientProjector
  simp only [Matrix.mul_assoc]
  rw [← Matrix.mul_assoc intrinsicRestriction intrinsicIndicator
      (reconstructedTransport * intrinsicRestriction),
    intrinsicRestriction_indicator, Matrix.one_mul]

/-- The compressed normalized Laplacian is exactly `I` minus the compressed
transport. -/
theorem reconstructedNormalizedLaplacian_eq_one_sub_transport :
    reconstructedNormalizedLaplacian =
      1 - reconstructedTransport := by
  rw [reconstructedNormalizedLaplacian_eq_quotient,
    reconstructedTransport_eq_zoneTransport]
  rfl

/-- Lifting the reconstructed normalized Laplacian gives precisely the quotient
projector minus the full transport. -/
theorem lifted_reconstructed_laplacian_eq_projector_sub_transport :
    intrinsicIndicator * reconstructedNormalizedLaplacian *
        intrinsicRestriction =
      intrinsicQuotientProjector - fullTransport := by
  rw [reconstructedNormalizedLaplacian_eq_one_sub_transport]
  calc
    intrinsicIndicator * (1 - reconstructedTransport) *
        intrinsicRestriction =
      (intrinsicIndicator -
        intrinsicIndicator * reconstructedTransport) *
          intrinsicRestriction := by
            rw [Matrix.mul_sub, Matrix.mul_one]
    _ = intrinsicIndicator * intrinsicRestriction -
        (intrinsicIndicator * reconstructedTransport) *
          intrinsicRestriction := by
            rw [Matrix.sub_mul]
    _ = intrinsicQuotientProjector - fullTransport := by
      rw [fullTransport_intrinsic_factorization]
      rfl

/-- **Exact archive-plus-quotient decomposition.**  The full normalized Laplacian
is identity on the complement of the intrinsic quotient image and is the lifted
reconstructed quotient Laplacian on that image. -/
theorem fullNormalizedLaplacian_intrinsic_decomposition :
    fullNormalizedLaplacian =
      (1 - intrinsicQuotientProjector) +
        intrinsicIndicator * reconstructedNormalizedLaplacian *
          intrinsicRestriction := by
  rw [lifted_reconstructed_laplacian_eq_projector_sub_transport]
  unfold fullNormalizedLaplacian
  abel

/-- The canonical 30-dimensional archive projector. -/
def intrinsicArchiveProjector : Matrix Vertex33 Vertex33 ℚ :=
  1 - intrinsicQuotientProjector

/-- The archive is a right eigenblock of the full normalized Laplacian with
eigenvalue one. -/
theorem intrinsicArchive_eigenvalue_one_right :
    fullNormalizedLaplacian * intrinsicArchiveProjector =
      intrinsicArchiveProjector := by
  unfold fullNormalizedLaplacian intrinsicArchiveProjector
  rw [Matrix.sub_mul, Matrix.one_mul, Matrix.mul_sub, Matrix.mul_one,
    fullTransport_mul_intrinsicQuotientProjector, sub_self, sub_zero]

/-- The same archive is a left eigenblock with eigenvalue one. -/
theorem intrinsicArchive_eigenvalue_one_left :
    intrinsicArchiveProjector * fullNormalizedLaplacian =
      intrinsicArchiveProjector := by
  unfold fullNormalizedLaplacian intrinsicArchiveProjector
  rw [Matrix.mul_sub, Matrix.mul_one, Matrix.sub_mul, Matrix.one_mul,
    intrinsicQuotientProjector_mul_fullTransport, sub_self, sub_zero]

/-- Two-sided eigenvalue-one archive certificate. -/
theorem intrinsicArchive_eigenvalue_one :
    fullNormalizedLaplacian * intrinsicArchiveProjector =
        intrinsicArchiveProjector ∧
      intrinsicArchiveProjector * fullNormalizedLaplacian =
        intrinsicArchiveProjector :=
  ⟨intrinsicArchive_eigenvalue_one_right,
    intrinsicArchive_eigenvalue_one_left⟩

/-! ## Coordinate controls: order and scale are not intrinsic -/

/-- Reverse the displayed degree order, exchanging the 24- and 20-fibres. -/
def orderSwap : Matrix Fibre3 Fibre3 ℚ :=
  !![0, 0, 1; 0, 1, 0; 1, 0, 0]

theorem orderSwap_square :
    orderSwap * orderSwap = (1 : Matrix Fibre3 Fibre3 ℚ) := by
  native_decide

/-- The same quotient lift in a reversed coordinate order. -/
def reorderedIndicator : Matrix Vertex33 Fibre3 ℚ :=
  intrinsicIndicator * orderSwap

/-- Corresponding inverse averaging map. -/
def reorderedRestriction : Matrix Fibre3 Vertex33 ℚ :=
  orderSwap * intrinsicRestriction

theorem reorderedRestriction_indicator :
    reorderedRestriction * reorderedIndicator =
      (1 : Matrix Fibre3 Fibre3 ℚ) := by
  simp only [reorderedRestriction, reorderedIndicator, Matrix.mul_assoc]
  rw [← Matrix.mul_assoc intrinsicRestriction intrinsicIndicator orderSwap,
    intrinsicRestriction_indicator, Matrix.one_mul, orderSwap_square]

/-- Reordering the recovered fibres changes only the displayed quotient matrix by
permutation similarity. -/
theorem reordered_adjacency_permutation_similar :
    reorderedRestriction * D0.Claims.Adj31 * reorderedIndicator =
      orderSwap * reconstructedAdjacency * orderSwap := by
  simp only [reorderedRestriction, reorderedIndicator, reconstructedAdjacency,
    Matrix.mul_assoc]

theorem reordered_transport_permutation_similar :
    reorderedRestriction * fullTransport * reorderedIndicator =
      orderSwap * reconstructedTransport * orderSwap := by
  simp only [reorderedRestriction, reorderedIndicator, reconstructedTransport,
    Matrix.mul_assoc]

/-- A noncanonical rescaling of the three recovered constant vectors. -/
def scaleChoice : Matrix Fibre3 Fibre3 ℚ :=
  !![2, 0, 0; 0, 3, 0; 0, 0, 5]

def scaleChoiceInv : Matrix Fibre3 Fibre3 ℚ :=
  !![1 / 2, 0, 0; 0, 1 / 3, 0; 0, 0, 1 / 5]

theorem scaleChoice_inverse :
    scaleChoiceInv * scaleChoice = (1 : Matrix Fibre3 Fibre3 ℚ) ∧
      scaleChoice * scaleChoiceInv = 1 := by
  constructor <;> native_decide

def scaledIndicator : Matrix Vertex33 Fibre3 ℚ :=
  intrinsicIndicator * scaleChoice

def scaledRestriction : Matrix Fibre3 Vertex33 ℚ :=
  scaleChoiceInv * intrinsicRestriction

/-- Rescaling changes the coordinate lift but not the canonical quotient image
projector. -/
theorem scaling_changes_coordinates_not_image :
    scaledIndicator ≠ intrinsicIndicator ∧
      scaledIndicator * scaledRestriction = intrinsicQuotientProjector := by
  constructor
  · native_decide
  · simp only [scaledIndicator, scaledRestriction, intrinsicQuotientProjector,
      Matrix.mul_assoc]
    rw [← Matrix.mul_assoc scaleChoice scaleChoiceInv intrinsicRestriction,
      scaleChoice_inverse.2, Matrix.one_mul]

/-- Under arbitrary column normalization, the displayed adjacency is diagonally
similar to the canonical `0/1` normalization. -/
theorem scaled_adjacency_diagonal_similar :
    scaledRestriction * D0.Claims.Adj31 * scaledIndicator =
      scaleChoiceInv * reconstructedAdjacency * scaleChoice := by
  simp only [scaledRestriction, scaledIndicator, reconstructedAdjacency,
    Matrix.mul_assoc]

/-! ## Capstone -/

/-- **Intrinsic quotient reconstruction.**  The literal degree operator reconstructs
the zone blocks, their masses, the canonical quotient image, and both the unnormalized
and normalized induced dynamics without selecting representatives.  Only matrix
coordinates retain order/scale conventions. -/
theorem intrinsic_quotient_reconstruction :
    intrinsicIndicator = D0.Claims.Cind31 ∧
      intrinsicFibreMass = ![(9 : ℚ), 11, 13] ∧
      intrinsicRestriction * intrinsicIndicator =
        (1 : Matrix Fibre3 Fibre3 ℚ) ∧
      intrinsicQuotientProjector =
        D0.Claims.InvariantGenerationBridge.P ∧
      reconstructedAdjacency = AWq ∧
      reconstructedDegree = DWq ∧
      reconstructedTransport = D0.Spectral.zoneTransport ∧
      reconstructedNormalizedLaplacian = quotientNormalizedLaplacian :=
  ⟨intrinsicIndicator_eq_Cind31, intrinsicFibreMass_values,
    intrinsicRestriction_indicator, intrinsicQuotientProjector_eq_reynolds,
    reconstructedAdjacency_eq_AWq, reconstructedDegree_eq_DWq,
    reconstructedTransport_eq_zoneTransport,
    reconstructedNormalizedLaplacian_eq_quotient⟩

end D0.Synthesis.IntrinsicQuotientReconstruction
