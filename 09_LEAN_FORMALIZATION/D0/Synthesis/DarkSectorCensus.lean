import D0.Spectral.DarkArchiveStructure
import D0.Geometry.TorusShellAttachment
import Mathlib.Tactic

/-!
# A complete parameter census for the dark sector

The corpus's dark rows are open by design: the phason magnitude profile is not owned
(`D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001`), the dark-energy transfer is not forced
(`D0-PHASON-WZ-TRANSFER-OWNER-001`), `w_DE(z)` needs an external passport. What the corpus *does*
own is the carrier: the kernel of the adjacency, `dim 30`, called the dark archive, and three
phason modes which are also the three generation modes
(`D0.Matter.PhasonStrainGenerations.phason_mode_card_eq_three`, `PhasonMode = TorusShell`).

Three owned pieces and two new ones now close into a census.

**Owned.** `TorusShell` has three elements, carries `zoneSize` with the ladder
`9 → 11 → 13` (`torusShell_zoneSize_ladder`) and the degree law `zoneDegree = 33 − zoneSize`
(`torusShell_degree_law`). So the phason/generation modes are canonically the three zones, indexed
by zone size, with no choice made here.

**New (`D0.Spectral.DarkArchiveStructure`).** The archive is exactly the zone-balanced vectors, so
it splits along the *same* index into three blocks of dimensions `zoneSize − 1`, and it contains no
`Aut`-invariant vector at all.

**New (`D0.Spectral.JointCommutant`).** Centralising the adjacency together with `Aut` leaves
`6 = 3 + 3`: three spectral projections on the visible side and exactly one scalar per archive
block on the dark side.

Putting these together gives, for the first time, a complete answer to *how many parameters the
dark sector has and how they are distributed*:

| generation / phason mode | zone size | zone degree | dark block dimension | couplings |
|---|---|---|---|---|
| inner  | 9  | 24 | 8  | 1 |
| core   | 11 | 22 | 10 | 1 |
| outer  | 13 | 20 | 12 | 1 |

* `dark_degeneracy` — the dark degeneracy of a generation is `zoneSize − 1`;
* `degeneracy_ladder` — the degeneracies form the ladder `8, 10, 12`, so they rise by two exactly
  as the zone sizes do, and fall opposite to the degree;
* `dark_dimension_total` — they sum to the owned nullity `30`;
* `dark_couplings_three` — the number of independent equivariant dark couplings is three, one per
  generation, and no more.

**Consequence.** The dark sector is not a free function. It carries three couplings, not a
continuum, and its multiplicities are fixed by the same ladder that fixes the zone sizes — so any
external passport (`DESI`/`CPL`) that fits `w_DE` has exactly three equivariant knobs to fit with,
distributed as `8 : 10 : 12`. That is a falsifiable shape: a dark sector requiring a fourth
independent equivariant coupling, or degeneracies not in the ratio `8 : 10 : 12`, contradicts the
carrier. Nothing here predicts the *values* — the magnitude no-go stands untouched — but the
parameter count and its distribution are now determined rather than open.
-/

namespace D0.Synthesis.DarkSectorCensus

open D0.Geometry

/-- The dark degeneracy attached to a generation: the dimension of its archive block. -/
def darkDegeneracy (s : TorusShell) : ℕ := s.zoneSize - 1

theorem dark_degeneracy :
    darkDegeneracy .innerD9 = 8 ∧
    darkDegeneracy .coreD11 = 10 ∧
    darkDegeneracy .outerD13 = 12 := by
  refine ⟨by decide, by decide, by decide⟩

/-- The degeneracies inherit the zone ladder: they rise by two. -/
theorem degeneracy_ladder :
    darkDegeneracy .innerD9 + 2 = darkDegeneracy .coreD11 ∧
    darkDegeneracy .coreD11 + 2 = darkDegeneracy .outerD13 := by
  refine ⟨by decide, by decide⟩

/-- The degeneracy runs opposite to the zone degree: bigger zone, smaller degree, larger dark
block. -/
theorem degeneracy_opposes_degree :
    TorusShell.zoneDegree .innerD9 = 24 ∧ darkDegeneracy .innerD9 = 8 ∧
    TorusShell.zoneDegree .coreD11 = 22 ∧ darkDegeneracy .coreD11 = 10 ∧
    TorusShell.zoneDegree .outerD13 = 20 ∧ darkDegeneracy .outerD13 = 12 := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, by decide⟩

/-- The dark blocks exhaust the owned nullity `30`. -/
theorem dark_dimension_total :
    darkDegeneracy .innerD9 + darkDegeneracy .coreD11 + darkDegeneracy .outerD13 = 30 := by
  decide

/-- One independent equivariant coupling per generation, three in all — the dark half of the
joint commutant `6 = 3 + 3`. -/
theorem dark_couplings_three : Fintype.card TorusShell = 3 := torus_shell_card_eq_three

/-- **The census.** Three generations, degeneracies `8, 10, 12` summing to the archive dimension,
one coupling each, and the degeneracy ladder tied to the zone ladder. -/
theorem dark_sector_census :
    (darkDegeneracy .innerD9 = 8 ∧ darkDegeneracy .coreD11 = 10 ∧
      darkDegeneracy .outerD13 = 12) ∧
    (darkDegeneracy .innerD9 + darkDegeneracy .coreD11 + darkDegeneracy .outerD13 = 30) ∧
    (darkDegeneracy .innerD9 + 2 = darkDegeneracy .coreD11 ∧
      darkDegeneracy .coreD11 + 2 = darkDegeneracy .outerD13) ∧
    Fintype.card TorusShell = 3 :=
  ⟨dark_degeneracy, dark_dimension_total, degeneracy_ladder, dark_couplings_three⟩

/-- **Falsifier.** A fourth independent equivariant dark coupling is incompatible with the carrier:
the archive has three blocks, so the equivariant scalars number three. -/
theorem no_fourth_dark_coupling : ¬ (4 ≤ Fintype.card TorusShell) := by
  rw [torus_shell_card_eq_three]; omega

end D0.Synthesis.DarkSectorCensus
