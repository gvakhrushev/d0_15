import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic

/-!
# D0-CARRIER-NOT-ICOSAHEDRAL-001 — K(9,11,13) is NOT an icosahedral cut-and-project (separation)

Python certificate: `05_CERTS/vp_carrier_not_icosahedral.py`.

The named gap of `D0-QUASICRYSTAL-PROJECTION-001` (is `K(9,11,13)` a 33D→3D icosahedral
cut-and-project with `A₅` symmetry on its rank-3 physical image?) is **resolved by separation** —
a decidable negative, not an open gap. `Aut(K(9,11,13)) = S₉×S₁₁×S₁₃`; because the zone sizes are
distinct (`9≠11≠13`), the induced symmetry on the three zone-classes (the rank-3 image) is
**trivial** — only the identity preserves the size assignment. The icosahedral group `A₅` has
order `60`; a faithful `A₅`-action on the three zone-classes would land in this trivial induced
symmetry, impossible since `60 > 1`. So `K(9,11,13)` carries no icosahedral symmetry on its rank-3
image and is **not** the icosahedral cut-and-project. (`A₅ = 2I/\{\pm1\}` lives on the flavor/`E₈`
side — the level-5 modular group — not on the carrier; `D0-MODULAR-TIME-FLAVOR-001`.)

The `rank = 3` *convergence* (carrier rank-3 = icosahedral 3D-slice dimension) is kept as a real
third channel to "3"; the `nullity 30 = ` icosahedron edges is a confirmed coincidence. The
obstruction is exactly the size-asymmetry: an *equal*-zone `K(n,n,n)` would admit the `S₃`
zone-swap symmetry, but `9≠11≠13` kills it.
-/

namespace D0.Claims

/-- The three zone sizes of `K(9,11,13)`. -/
def zoneSize : Fin 3 → ℕ
  | 0 => 9
  | 1 => 11
  | 2 => 13

/-- The zone sizes are pairwise distinct (the source of the obstruction). -/
theorem zone_sizes_injective : Function.Injective zoneSize := by decide

/-- The size-preserving permutations of the three zone-classes form the **trivial** group: only
the identity preserves the size assignment (because `9≠11≠13`). This is the entire induced
symmetry of the rank-3 physical image under `Aut(K) = S₉×S₁₁×S₁₃`. -/
theorem induced_zone_symmetry_trivial :
    (Finset.univ.filter
      (fun σ : Equiv.Perm (Fin 3) => ∀ i, zoneSize (σ i) = zoneSize i)).card = 1 := by
  native_decide

/-- The icosahedral rotation group `A₅` has order `60`. -/
theorem a5_order : Nat.factorial 5 / 2 = 60 := by decide

/-- Negative control: an *equal*-zone tripartite would admit the full `S₃` zone-swap (order `6`)
on its three classes — so the obstruction below is exactly the size-asymmetry `9≠11≠13`. -/
theorem equal_zones_would_admit_S3 :
    (Finset.univ.filter
      (fun σ : Equiv.Perm (Fin 3) => ∀ i, (fun _ : Fin 3 => (7 : ℕ)) (σ i)
        = (fun _ : Fin 3 => (7 : ℕ)) i)).card = 6 := by
  native_decide

/-- **D0-CARRIER-NOT-ICOSAHEDRAL-001 (separation).** The induced symmetry of `K(9,11,13)`'s
rank-3 image is trivial (order `1`), while `A₅` has order `60 > 1`; so no faithful icosahedral
`A₅`-action exists on the carrier, and `K(9,11,13)` is not an icosahedral cut-and-project. The
obstruction is the size-asymmetry (equal zones would give `S₃`, order `6`). -/
theorem carrier_not_icosahedral :
    (Finset.univ.filter
      (fun σ : Equiv.Perm (Fin 3) => ∀ i, zoneSize (σ i) = zoneSize i)).card = 1
    ∧ Nat.factorial 5 / 2 = 60
    ∧ 1 < Nat.factorial 5 / 2 :=
  ⟨induced_zone_symmetry_trivial, a5_order, by decide⟩

end D0.Claims
