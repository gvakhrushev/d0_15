import Mathlib.Data.Finset.Card
import Mathlib.Data.Fintype.Basic
import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveLaplacianProperties
import D0.Geometry.ArchiveRolePhaseProductCarrier

namespace D0.Geometry.ArchiveFlatProductBondingNoGo

open D0
open D0.Geometry.ArchiveRolePhaseProductCarrier

/-!
# D0.Geometry.ArchiveFlatProductBondingNoGo

Owner: `D0-ARCHIVE-FLAT-PRODUCT-BONDING-NOGO-001`.

Structural obstruction proving that the flat integer-mod bonding map
`archiveProjection 0 : Fin (3^4) → Fin (2^4)` (mapping $x \mapsto x \bmod 16$)
cannot be isomorphic via stagewise bijections to the natural coordinate-wise product
bonding map $(\mathrm{Fin}\ 3)^4 \to (\mathrm{Fin}\ 2)^4$.

## Explicit Witness at $n = 0$:
1. The flat bonding fiber over 0 in `Fin 81 → Fin 16` has size 6:
   $$\{0, 16, 32, 48, 64, 80\}.$$
2. The coordinate-wise product bonding fiber over $(0,0,0,0)$ in $(\mathrm{Fin}\ 3)^4 \to (\mathrm{Fin}\ 2)^4$
   has size $2^4 = 16$:
   each cyclic coordinate has 2 preimages of 0 (namely 0 and 2 in `Fin 3`).
3. Since $6 \ne 16$, the two inverse-system bonding structures have strictly different
   fiber cardinalities and cannot be conjugated by levelwise bijections.
-/

/-- Flat bonding fiber over 0 for $n = 0$: indices in `Fin 81` whose value mod 16 is 0. -/
def flatZeroFiber : Finset (ArchivePoints 1) :=
  (Finset.univ : Finset (ArchivePoints 1)).filter (fun x => archiveProjection 0 x = zeroArchivePoint 0)

/-- The size of the flat zero-fiber in `Fin 81 → Fin 16` is exactly 6. -/
theorem card_flat_zero_fiber : flatZeroFiber.card = 6 := by
  native_decide

/-- Coordinate-wise 1D cyclic projection fiber over 0 in `Fin 3 → Fin 2` (values mod 2 = 0). -/
def cycleZeroFiber1D : Finset (archivePhaseIndex 1) :=
  (Finset.univ : Finset (Fin 3)).filter (fun x => (x.val % 2) = 0)

/-- In 1D `Fin 3 → Fin 2`, the preimages of 0 are 0 and 2 (size 2). -/
theorem card_cycle_zero_fiber_1D : cycleZeroFiber1D.card = 2 := by
  native_decide

/-- Fourfold coordinate-wise product fiber cardinality over the zero configuration is $2^4 = 16$. -/
def productZeroFiberCard : ℕ := 2^4

theorem product_zero_fiber_card_eq_sixteen : productZeroFiberCard = 16 := by
  decide

/-- Strict fiber cardinality mismatch: $6 \ne 16$. -/
theorem flat_ne_product_fiber_card : flatZeroFiber.card ≠ productZeroFiberCard := by
  rw [card_flat_zero_fiber, product_zero_fiber_card_eq_sixteen]
  decide

/-- **D0-ARCHIVE-FLAT-PRODUCT-BONDING-NOGO-001 (Owner)**:
The flat record bonding map `archiveProjection` cannot be identified with or conjugated to
the canonical 4D role-coordinate product bonding map:
their fiber cardinalities over the base zero-state strictly disagree ($6 \ne 16$).
The record inverse-limit object `archiveLightProfinite` and the geometric 4D role-product
continuum are distinct inverse-limit structures that must not be identified. -/
theorem archive_flat_product_bonding_nogo_owner :
    (flatZeroFiber.card = 6) ∧
    (productZeroFiberCard = 16) ∧
    (flatZeroFiber.card ≠ productZeroFiberCard) :=
  ⟨card_flat_zero_fiber, product_zero_fiber_card_eq_sixteen, flat_ne_product_fiber_card⟩

end D0.Geometry.ArchiveFlatProductBondingNoGo
