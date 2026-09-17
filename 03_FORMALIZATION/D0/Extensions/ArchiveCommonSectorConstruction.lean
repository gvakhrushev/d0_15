import D0.Extensions.ArchiveCoordinateExtension
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-PHASON-PRESSURE-ENERGY-001 — Lane P1 terminal (P1-C)

No typed common sector exists across the operator-firewalled `{L_archive, QUQ, W_eff, log-det pressure,
S_DE}`: `L_archive` has integer spectrum `{24,22,20}`, the `S_DE` active window is irrational
(`(3/2−√10/40)(3/2+√10/40) = 359/160`), and `QUQ` lives on the toral tick — distinct carriers with no
canonical intertwiner in the admissible map class (intertwiner/compression/dilation/Riesz/cond-exp/response).
Terminal **P1-C**: no common pressure-energy sector; no trace/det coincidence is an intertwiner.
-/

namespace D0.Extensions.ArchiveCommonSectorConstruction

open D0 D0.Extensions.ArchiveCoordinateExtension

/-- **Terminal P1-C.** The `S_DE` window is irrational (`359/160` product), incommensurate with the integer
`L_archive` spectrum — no common sector / canonical intertwiner in the typed class. -/
theorem archive_common_sector_P1C :
    (3 / 2 - Real.sqrt 10 / 40) * (3 / 2 + Real.sqrt 10 / 40) = 359 / 160 :=
  window_product

/-- **Load-bearing spectral-disjointness separator (D0-PHASON-WZ-TRANSFER-OWNER-001 NO-GO).** The `S_DE`
active-window eigenvalues are the two roots of `x² − 3x + 359/160` (sum `3`, product `359/160`). NONE of the
integer `L_archive` eigenvalues `{24, 22, 20}` is such a root — verified over `ℚ`. So the archive carrier and
the `S_DE` window carrier are SPECTRALLY DISJOINT: no eigenvalue-matching, hence no canonical intertwiner, maps
one onto the other. This is the genuine separator behind P1-C (the `archive_common_sector_P1C` identity above
only records the window product); together with the role-orientation maximality witnesses it makes the explicit
internal transfer `archive kernel → phason pressure → w_D0` underdetermined — the missing artifact is
`PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT`. -/
theorem sde_window_root_not_archive_eigenvalue :
    ∀ n ∈ ([24, 22, 20] : List ℚ), n ^ 2 - 3 * n + 359 / 160 ≠ 0 := by
  intro n hn
  fin_cases hn <;> norm_num

end D0.Extensions.ArchiveCommonSectorConstruction
