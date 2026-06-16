import D0.Geometry.ArchiveLightProfinite
import D0.Geometry.ArchiveRefinementTower

/-!
# D0-CONTINUUM-INVLIM-001 — §21.2: the continuum as a profinite inverse limit

DEF 21.2.1 instantiated. The D0 "continuum" is not a set of actual-infinity points but the inverse
limit of the finite archive refinement tower `(V_k, π_{k→k-1})` — realised as a genuine Mathlib
`LightProfinite` (compact Hausdorff, totally disconnected, second countable), the categorical
upgrade of the bespoke nonempty-inverse-limit witness.

**Register:** D0-reformulation of "the continuum" under the explicit modelling hypothesis that the
real line is the inverse limit of its finite coarse-grainings — NOT the ZFC/actual-infinity continuum
(which postulates a completed infinity, an unprovable input). Reuses the pin's Clausen–Scholze
condensed apparatus (`Profinite.AsLimit`, `LightProfinite ≌ LightDiagram`). Two passports: physics
(the archive tower) + math (DEF 21.2.1 point-free continuum). This is the foundational anchor that the
§24/§25/§27/§30 reformulations cite for "κ-stable inverse limit".
-/

namespace D0.Foundation

open D0

/-- **The D0 continuum** (DEF 21.2.1): the inverse limit of the finite archive tower, as a genuine
Mathlib `LightProfinite`. -/
noncomputable def D0Continuum : LightProfinite := archiveLightProfinite

/-- The continuum is a (nonempty) profinite inverse limit: coherent infinite threads exist, built
from the finite levels and their surjective coarse-grainings — no actual infinity required. -/
theorem continuum_is_nonempty_inverse_limit :
    DefinesProfiniteObject archiveProfiniteSystem :=
  archive_tower_defines_profinite_object

/-- Point-free existence: the inverse-limit thread space is inhabited (DEF 21.3.3 limit object). -/
theorem continuum_no_actual_infinity :
    Nonempty (InverseLimit archiveProfiniteSystem) :=
  inverseLimit_nonempty archiveProfiniteSystem archivePoints_nonempty

/-- The continuum object is the archive tower's `LightProfinite` (definitional anchor). -/
theorem d0Continuum_eq : D0Continuum = archiveLightProfinite := rfl

end D0.Foundation
