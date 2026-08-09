import D0.Topology.GenericTripartiteZeroHomologyRing
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-UNIVERSAL-HOMOLOGY-001

This module bundles the constructive coefficient-universal homology theorem
for the canonical complete-tripartite clique complex:

```
H₀(K(p+1,q+1,r+1);R) ≃ R,
H₁(K(p+1,q+1,r+1);R) = 0,
H₂(K(p+1,q+1,r+1);R) ≃ R^(Fin p × Fin q × Fin r)
```

for every commutative ring `R`.  In degree two the equivalence is the explicit
octahedral basis; in degree one it is backed by an explicit filling operator;
in degree zero it is backed by an explicit spanning-tree decomposition.

For `R=ℤ`, this gives the full integral homology and torsion-freeness.  The
source scene has `H₂ ≃ ℤ^960`.
-/

namespace D0.Topology.GenericTripartiteUniversalHomology

open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing
open D0.Topology.GenericTripartiteFirstHomologyRing
open D0.Topology.GenericTripartiteZeroHomologyRing

variable (R : Type) [CommRing R]
variable {p q r : ℕ}

/-- Constructive homology data in all nonzero chain degrees. -/
structure UniversalHomologyPassport where
  zeroEquiv :
    ZeroHomologyR R (p:=p) (q:=q) (r:=r) ≃ₗ[R] R
  firstIsZero :
    Subsingleton (FirstHomologyR R (p:=p) (q:=q) (r:=r))
  topEquiv :
    TopKernel R (p:=p) (q:=q) (r:=r) ≃ₗ[R]
      (TopCycleIndex p q r → R)

/-- **Coefficient-universal homology passport.** -/
noncomputable def universalHomologyPassport :
    UniversalHomologyPassport R (p:=p) (q:=q) (r:=r) where
  zeroEquiv := zeroHomologyEquivR R
  firstIsZero := firstHomologyR_subsingleton R
  topEquiv := topCoordinateEquivR R

/-- Every first-homology class is zero. -/
theorem firstHomologyR_eq_zero
    (x : FirstHomologyR R (p:=p) (q:=q) (r:=r)) :
    x = 0 :=
  (universalHomologyPassport R (p:=p) (q:=q) (r:=r)).firstIsZero.elim _ _

/-- Integral homology passport for the source scene `(9,11,13)`. -/
noncomputable def sceneIntegerHomologyPassport :
    UniversalHomologyPassport ℤ (p:=8) (q:=10) (r:=12) :=
  universalHomologyPassport ℤ

/-- The source scene has a free integral top homology module with 960 explicit
octahedral basis elements. -/
theorem sceneIntegerTopHomologyFree :
    Module.Free ℤ (TopKernel ℤ (p:=8) (q:=10) (r:=12)) :=
  integerTopHomologyFree

/-- The source-scene integral top-homology basis has exactly 960 elements. -/
theorem sceneIntegerTopBasisCardinality :
    Fintype.card (TopCycleIndex 8 10 12) = 960 :=
  sceneIntegerTopCycleIndex_card

end D0.Topology.GenericTripartiteUniversalHomology
