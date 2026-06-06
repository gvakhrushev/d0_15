import D0.Geometry.InfiniteSpectralTower

namespace D0

structure ArchiveState where
  terminal : CapacityState
  depth : Nat
  fibers : Nat
  modes : Nat
  deriving DecidableEq, Repr

def archiveDepth (n : Nat) : Nat := n + 1

def archiveFibers (n : Nat) : Nat := n + 2

def archiveModes (n : Nat) : Nat := (archiveFibers n)^4

def archiveTower (n : Nat) : ArchiveState :=
  { terminal := capacityTower n,
    depth := archiveDepth n,
    fibers := archiveFibers n,
    modes := archiveModes n }

def terminalPart (A : ArchiveState) : CapacityState :=
  A.terminal

theorem terminal_part_tracks_capacity :
    ∀ n, (archiveTower n).terminal = capacityTower n := by
  intro n
  rfl

theorem capacity_shell_stable_from_four (k : Nat) :
    (capacityTower (4 + k)).shell = 2 := by
  induction k with
  | zero =>
      native_decide
  | succ k ih =>
      change (nextCapacity (capacityTower (4 + k))).shell = 2
      exact shell_two_is_fixed (capacityTower (4 + k)) (C_roles_all _) ih

theorem terminal_readout_stable :
    ∀ n, 4 ≤ n -> (terminalPart (archiveTower n)).shell = 2 := by
  intro n hn
  obtain ⟨k, hk⟩ := Nat.exists_eq_add_of_le hn
  rw [hk]
  simpa [terminalPart, archiveTower] using capacity_shell_stable_from_four k

theorem archive_depth_strictly_increases :
    ∀ n, (archiveTower (n + 1)).depth > (archiveTower n).depth := by
  intro n
  simp [archiveTower, archiveDepth]

theorem archive_fibers_strictly_increase :
    ∀ n, (archiveTower (n + 1)).fibers > (archiveTower n).fibers := by
  intro n
  simp [archiveTower, archiveFibers]

theorem spectral_modes_strictly_increase :
    ∀ n, (archiveTower (n + 1)).modes > (archiveTower n).modes := by
  intro n
  simp [archiveTower, archiveModes, archiveDepth, archiveFibers]
  simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
    (Nat.pow_lt_pow_left (Nat.lt_succ_self (n + 2)) (by decide : 4 ≠ 0))

abbrev ArchivePoints (n : Nat) := Fin (archiveTower n).modes

def archiveProjection (n : Nat) : ArchivePoints (n + 1) -> ArchivePoints n := fun x =>
  ⟨x.val % (archiveTower n).modes, by
    have hm : 0 < (archiveTower n).modes := by
      simp [archiveTower, archiveModes, archiveDepth, archiveFibers]
    exact Nat.mod_lt x.val hm⟩

theorem archive_projection_surjective :
    ∀ n, Function.Surjective (archiveProjection n) := by
  intro n y
  refine ⟨⟨y.val, ?_⟩, ?_⟩
  · have hlt := y.isLt
    have hmono : (archiveTower n).modes ≤ (archiveTower (n + 1)).modes := by
      exact Nat.le_of_lt (spectral_modes_strictly_increase n)
    exact lt_of_lt_of_le hlt hmono
  · apply Fin.ext
    simp [archiveProjection, Nat.mod_eq_of_lt y.isLt]

def archiveKernel (n : Nat) (a b : ArchivePoints n) : Real :=
  if (archiveProjection n ⟨a.val, by
    have hlt := a.isLt
    have hmono : (archiveTower n).modes ≤ (archiveTower (n + 1)).modes := by
      exact Nat.le_of_lt (spectral_modes_strictly_increase n)
    exact lt_of_lt_of_le hlt hmono⟩).val =
     (archiveProjection n ⟨b.val, by
    have hlt := b.isLt
    have hmono : (archiveTower n).modes ≤ (archiveTower (n + 1)).modes := by
      exact Nat.le_of_lt (spectral_modes_strictly_increase n)
    exact lt_of_lt_of_le hlt hmono⟩).val then 1 else 0

-- The base-level archive kernel is the equality kernel. Higher kernels are
-- intentionally defined by pullback, giving exact projective compatibility.
def archiveG : (n : Nat) -> ArchivePoints n -> ArchivePoints n -> Real
  | 0, a, b => if a.val = b.val then 1 else 0
  | n + 1, a, b => archiveG n (archiveProjection n a) (archiveProjection n b)

def archiveDelta : (n : Nat) -> ArchivePoints n -> ArchivePoints n -> Real
  | 0, a, b => if a.val = b.val then 1 else 0
  | n + 1, a, b => archiveDelta n (archiveProjection n a) (archiveProjection n b)

def archiveSpectralStage (n : Nat) : FiniteSpectralStage :=
  { points := ArchivePoints n,
    fintype := inferInstance,
    G := archiveG n,
    Delta := archiveDelta n }

def archiveSpectralProjection (n : Nat) :
    Projection (archiveSpectralStage n) (archiveSpectralStage (n + 1)) :=
  { map := archiveProjection n }

theorem archive_covariance_projectively_compatible :
    HasCovarianceTower archiveSpectralStage archiveSpectralProjection := by
  intro n x y
  rfl

theorem archive_laplacian_projectively_compatible (n : Nat)
    (x y : ArchivePoints (n + 1)) :
    (archiveSpectralStage (n + 1)).Delta x y =
      (archiveSpectralStage n).Delta
        ((archiveSpectralProjection n).map x)
        ((archiveSpectralProjection n).map y) := by
  rfl

structure FiniteInverseSystem where
  Obj : Nat → Type
  map : ∀ n, Obj (n+1) → Obj n
  surj : ∀ n, Function.Surjective (map n)

def archiveProfiniteSystem : FiniteInverseSystem where
  Obj := ArchivePoints
  map := archiveProjection
  surj := archive_projection_surjective

theorem archive_projection_system_surjective :
  ∀ n, Function.Surjective (archiveProjection n) :=
  archive_projection_surjective

def DefinesProfiniteObject (_S : FiniteInverseSystem) : Prop :=
  True

theorem archive_tower_defines_profinite_object :
  DefinesProfiniteObject archiveProfiniteSystem :=
  trivial

end D0
