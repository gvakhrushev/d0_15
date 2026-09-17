import D0.Geometry.ArchiveCanonicalLaplacian

namespace D0

def ArchivePotential (n : Nat) :=
  archivePhaseIndex n → ℝ

instance (n : Nat) : Sub (ArchivePotential n) :=
  ⟨fun φ₁ φ₂ i => φ₁ i - φ₂ i⟩

def ArchivePoissonEquation {n : Nat}
  (φ : ArchivePotential n)
  (ρ : archivePhaseIndex n → ℝ) : Prop :=
  Matrix.mulVec (archiveCanonicalLaplacian n) φ = ρ

def NeutralSource {n : Nat} (ρ : archivePhaseIndex n → ℝ) : Prop :=
  ∑ i : archivePhaseIndex n, ρ i = 0

def constantPotential {n : Nat} (c : ℝ) : ArchivePotential n :=
  fun _ => c

end D0
