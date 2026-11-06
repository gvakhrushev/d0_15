import D0.Algebra.OriginalBookLocalStaticRoots
import D0.Geometry.OriginalBookMovedJuliaLeft
import D0.Geometry.OriginalBookMovedJuliaRight
import Mathlib.Tactic

/-!
# Local representatives of the actual moved D Julia roots

The fixed source modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a,
lines 97–104 and 137–143, at commit eebcb5e467742df3e9cf7fa9702042d7294aa742,
uses q=sqrt(12071/20000) and the boosted mode D. The already proved complex
root witnesses provide a diagonal left root and explicit 2×2-block right root.
This module constructs those values in the local ring, and shows their complex
and both explicit mod-1009 images. Equality of those explicit modular values
with the source's Lagrange-interpolation implementation is a separate check;
no effect span, rank, or physical admission follows.
-/
open D0
open Matrix
open D0.Algebra.OriginalBookRadicalLocal
open D0.Algebra.OriginalBookRadicalMod1009
open D0.Algebra.OriginalBookRadicalSourceConstants
open D0.Algebra.OriginalBookLocalCreators
open D0.Algebra.OriginalBookLocalStaticRoots
open D0.Geometry.OriginalBookMovedJuliaLeft
open D0.Geometry.OriginalBookMovedJuliaRight
open D0.Geometry.OrthogonalProjectionRoot
open D0.Geometry.OriginalBookJuliaWords

namespace D0.Algebra.OriginalBookLocalMovedRoots

/-- Since 1762 divides 8810, the right-root projector denominator is local. -/
noncomputable def localInv1762 : LocalSource := 5 * localInvD

lemma complexInv1762 : localSourceToComplex localInv1762 = (1 / 1762 : ℂ) := by
  simp [localInv1762, complexInvD, map_ofNat]
  norm_num

lemma localInvD_star : star localInvD = localInvD := by
  apply localSourceToComplex_injective
  rw [localSourceToComplex_star, complexInvD]
  simp

lemma modInv1762 : redPlus localInv1762 = (1 / 1762 : ZMod 1009) := by
  simp only [localInv1762, map_mul, map_ofNat, modInvD]
  decide

lemma modInv1762_minus : redMinus localInv1762 = (1 / 1762 : ZMod 1009) := by
  have hs : star localInv1762 = localInv1762 := by
    apply localSourceToComplex_injective
    rw [localSourceToComplex_star, complexInv1762]
    simp
  change redPlus (star localInv1762) = _
  rw [hs, modInv1762]

/-- The moved left-root diagonal uses the actual source index partition. -/
noncomputable def localMovedLeftValue (i : Fin 16) : LocalSource :=
  if mediumIndex i then 4 * localInv5 else if largeIndex i then localQ else 1

noncomputable def localMovedLeft : LocalOperator := Matrix.diagonal localMovedLeftValue

/-- The moved right-root's already verified regular and 2×2-block projectors. -/
def localRegular : LocalOperator := regularInt.map (Int.castRingHom LocalSource)
def localNumerator : LocalOperator := blockNumeratorInt.map (Int.castRingHom LocalSource)
noncomputable def localBoosted : LocalOperator := localInv1762 • localNumerator

noncomputable def localMovedRight : LocalOperator :=
  1 - localRegular - localBoosted + (4 * localInv5) • localRegular + localQ • localBoosted

/-- These are the actual positive roots previously verified for moved D. -/
theorem localMovedLeft_complex : localMovedLeft.map localSourceToComplex = liveLeft D := by
  ext bra ket
  by_cases h : bra = ket
  · subst ket
    simp only [localMovedLeft, Matrix.map_apply, Matrix.diagonal_apply_eq, liveLeft,
      candidateRoot, localMovedLeftValue]
    split_ifs <;> simp [rootValue, *, complexInv5, localSourceConstants_complex.2,
      D0.Geometry.OrthogonalProjectionRoot.coefficient, map_ofNat, div_eq_mul_inv]
  · simp [localMovedLeft, liveLeft, candidateRoot, h]

theorem localMovedRight_complex : localMovedRight.map localSourceToComplex = liveRight D := by
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localMovedRight, localBoosted, localRegular, localNumerator, liveRight,
      rootCandidate, D0.Geometry.OrthogonalProjectionRoot.residual, regularC, boostedC, numeratorC, complexInv1762,
      complexInv5, localSourceConstants_complex.2, h, map_ofNat] <;> ring_nf <;> simp

/-- The explicit modular left-root value for the pinned q image 278. -/
def modMovedLeftValue (i : Fin 16) : ZMod 1009 :=
  if mediumIndex i then 4 / 5 else if largeIndex i then 278 else 1

def modMovedLeft : Matrix (Fin 16) (Fin 16) (ZMod 1009) := Matrix.diagonal modMovedLeftValue

def modRegular : Matrix (Fin 16) (Fin 16) (ZMod 1009) := regularInt.map (Int.castRingHom (ZMod 1009))
def modNumerator : Matrix (Fin 16) (Fin 16) (ZMod 1009) := blockNumeratorInt.map (Int.castRingHom (ZMod 1009))
noncomputable def modBoosted : Matrix (Fin 16) (Fin 16) (ZMod 1009) := (1 / 1762 : ZMod 1009) • modNumerator
noncomputable def modMovedRight : Matrix (Fin 16) (Fin 16) (ZMod 1009) :=
  1 - modRegular - modBoosted + (4 / 5 : ZMod 1009) • modRegular + (278 : ZMod 1009) • modBoosted

lemma modQ : redPlus localQ = 278 := localSourceConstants_mod.2
lemma modQ_minus : redMinus localQ = 278 := by
  simpa [redPair] using congrArg Prod.snd localSourceConstants_redPair.2

theorem localMovedLeft_mod : localMovedLeft.map redPlus = modMovedLeft := by
  ext bra ket
  by_cases h : bra = ket
  · subst ket
    simp only [localMovedLeft, Matrix.map_apply, Matrix.diagonal_apply_eq, modMovedLeft,
      modMovedLeftValue, localMovedLeftValue]
    split_ifs <;> simp [modInv5, modQ, map_ofNat, div_eq_mul_inv]
  · simp [localMovedLeft, modMovedLeft, h]

theorem localMovedLeft_mod_minus : localMovedLeft.map redMinus = modMovedLeft := by
  ext bra ket
  by_cases h : bra = ket
  · subst ket
    simp only [localMovedLeft, Matrix.map_apply, Matrix.diagonal_apply_eq, modMovedLeft,
      modMovedLeftValue, localMovedLeftValue]
    split_ifs <;> simp [modInv5_minus, modQ_minus, map_ofNat, div_eq_mul_inv]
  · simp [localMovedLeft, modMovedLeft, h]

theorem localMovedRight_mod : localMovedRight.map redPlus = modMovedRight := by
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localMovedRight, localBoosted, localRegular, localNumerator, modMovedRight,
      modBoosted, modRegular, modNumerator, modInv1762, modInv5, modQ, h, map_ofNat] <;> ring_nf <;> simp

theorem localMovedRight_mod_minus : localMovedRight.map redMinus = modMovedRight := by
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localMovedRight, localBoosted, localRegular, localNumerator, modMovedRight,
      modBoosted, modRegular, modNumerator, modInv1762_minus, modInv5_minus, modQ_minus, h, map_ofNat] <;> ring_nf <;> simp

end D0.Algebra.OriginalBookLocalMovedRoots
