import D0.Integration.V15.Truth
import D0.Integration.V15.RawZone
import D0.Integration.V15.BranchAudit
import D0.Integration.V15.EdgeAudit
import D0.Integration.V15.Feshbach
import D0.Integration.V15.Refinement
import D0.Integration.V15.PhysicalBoundary
import D0.Integration.V15.Reconciliation

/-!
# D0-V15 integration aggregate

The canonical integration release. Source-to-theorem audit of `K(9,11,13)`:

* `Truth` — decidable §1.2 derivability discipline (five statuses).
* `RawZone` — **THE**: zone-current `G`-Hermitian spectral split (canonical part-size inner product).
* `Feshbach` — **THE** (algebraic identity): Schur/Feshbach determinant factorization; **NO-GO**: physical EOS.
* `BranchAudit` — **NO-GO**: branch CP readout non-unique; lepton mass ratios underdetermined.
* `EdgeAudit` — **CONDITIONAL**: physical edge cover is a λ-family.
* `Refinement` — **NO-GO**: archive ≠ regular cover; **CONDITIONAL**: Sturmian tower.
* `PhysicalBoundary` — regression of present-core limits; AMS **EXTERNAL-PASSPORT**.
* `Reconciliation` — the machine-checked truth manifest.

D0 is NOT declared complete: every physical bridge remains gated by a named missing primitive.
-/
