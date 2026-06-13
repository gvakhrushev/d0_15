import Mathlib.Tactic
import D0.Physics.PhasonFlipInertia

namespace D0.Cosmology

/-!
QUASI-008: finite phason-flip entropy / S_DE archive pressure.

This is the internal finite algebra owner.  Empirical survey comparison remains
an external passport and is not used here.
-/

/-- Entropy proxy: finite phason flip count as a nonnegative rational. -/
def PhasonFlipEntropy (flips : Nat) : Rat :=
  flips

/-- Archive pressure is the entropy/osmotic pressure of phason flips. -/
def ArchivePressureFromPhasonFlips (flips : Nat) : Rat :=
  PhasonFlipEntropy flips

/-- Finite 2x2 phason-flip transfer matrix for the S_DE algebra layer. -/
def phasonFlipTransferMatrix : Matrix (Fin 2) (Fin 2) Rat :=
  fun i j =>
    if i = 0 /\ j = 0 then (3 : Rat) / 2
    else if i = 0 /\ j = 1 then (1 : Rat) / 16
    else if i = 1 /\ j = 0 then (1 : Rat) / 10
    else if i = 1 /\ j = 1 then (3 : Rat) / 2
    else 0

/-- Characteristic polynomial `det(lambda I - T)` for the 2x2 transfer. -/
def phasonFlipTransferCharacteristic (lambda : Rat) : Rat :=
  (lambda - phasonFlipTransferMatrix 0 0) *
      (lambda - phasonFlipTransferMatrix 1 1) -
    phasonFlipTransferMatrix 0 1 * phasonFlipTransferMatrix 1 0

/-- The normalized S_DE polynomial. -/
def SDEPolynomial (lambda : Rat) : Rat :=
  160 * lambda ^ 2 - 480 * lambda + 359

/-- Relaxation mode predicate for the finite phason-flip transfer. -/
def PhasonFlipRelaxationMode (lambda : Rat) : Prop :=
  phasonFlipTransferCharacteristic lambda = 0

/-- Finite phason-flip entropy is nonnegative. -/
theorem phason_flip_entropy_nonnegative
    (flips : Nat) :
    0 <= PhasonFlipEntropy flips := by
  unfold PhasonFlipEntropy
  exact_mod_cast Nat.zero_le flips

/-- Archive pressure is phason-flip entropy osmosis by definition of the finite proxy. -/
theorem archive_pressure_is_phason_flip_entropy_osmosis
    (flips : Nat) :
    ArchivePressureFromPhasonFlips flips = PhasonFlipEntropy flips := by
  rfl

/-- The finite transfer characteristic is exactly the normalized S_DE polynomial. -/
theorem phason_flip_transfer_matrix_has_sde_polynomial
    (lambda : Rat) :
    160 * phasonFlipTransferCharacteristic lambda = SDEPolynomial lambda := by
  norm_num [phasonFlipTransferCharacteristic, phasonFlipTransferMatrix,
    SDEPolynomial]
  ring

/-- Roots of the S_DE polynomial are precisely phason-flip relaxation modes. -/
theorem sde_roots_are_phason_flip_relaxation_modes
    (lambda : Rat)
    (hroot : SDEPolynomial lambda = 0) :
    PhasonFlipRelaxationMode lambda := by
  have hchar : 160 * phasonFlipTransferCharacteristic lambda = 0 := by
    rw [phason_flip_transfer_matrix_has_sde_polynomial lambda, hroot]
  have hnonzero : (160 : Rat) ≠ 0 := by norm_num
  exact mul_eq_zero.mp hchar |>.resolve_left hnonzero

/-- Closure package for the internal finite phason-flip entropy layer. -/
structure PhasonFlipEntropySDEClosure where
  entropy_nonnegative :
    forall flips : Nat, 0 <= PhasonFlipEntropy flips
  pressure_eq_entropy :
    forall flips : Nat,
      ArchivePressureFromPhasonFlips flips = PhasonFlipEntropy flips
  characteristic_eq_sde :
    forall lambda : Rat,
      160 * phasonFlipTransferCharacteristic lambda = SDEPolynomial lambda
  roots_are_modes :
    forall lambda : Rat,
      SDEPolynomial lambda = 0 -> PhasonFlipRelaxationMode lambda

/-- Concrete finite QUASI-008 closure. -/
def phasonFlipEntropySDEClosure :
    PhasonFlipEntropySDEClosure where
  entropy_nonnegative := phason_flip_entropy_nonnegative
  pressure_eq_entropy := archive_pressure_is_phason_flip_entropy_osmosis
  characteristic_eq_sde := phason_flip_transfer_matrix_has_sde_polynomial
  roots_are_modes := sde_roots_are_phason_flip_relaxation_modes


end D0.Cosmology
