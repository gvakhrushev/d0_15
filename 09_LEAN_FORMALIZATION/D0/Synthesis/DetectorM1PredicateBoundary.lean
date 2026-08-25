import D0.Foundation.M1Predicate
import D0.Synthesis.DetectorCatalogueFreedom

/-!
# Detector/M1 predicate boundary: catalogue-free is a class, not a unique forced answer

`DetectorCatalogueFreedom` proves the correct catalogue-independence mathematics:

* catalogue-free comparisons factor through current data;
* order/history is not catalogue-free.

But the canonical repository predicate `D0.Foundation.M1Forced Forced a` is not a general
"admissible class" predicate. It requires `a` to be the **unique** witness of `Forced`. The
catalogue-free detector class has many members (constant false, constant true, equality, etc.),
so it has no `M1Forced` witness.

This module proves the exact seam:

1. the canonical `RequiresExternalCatalogue` can restate
   `¬ CatalogueFree orderComparison`;
2. this restatement is NOT load-bearing under the current M1 contract because the
   `CatalogueFree` constraint has no unique forced answer;
3. therefore T46 is a catalogue-independence theorem, not yet an instance of
   `D0-M1-PREDICATE-001`;
4. the missing object is a **class-level M1 admissibility predicate** (or a canonical finite
   obligation on capability kinds) that excludes catalogue-dependent comparisons without
   requiring one unique comparison function.

This correction prevents a local no-catalogue property from being promoted to global M1 forcing
by definitional relabeling.
-/

namespace D0.Synthesis.DetectorM1PredicateBoundary

open D0.Foundation
open D0.Synthesis.DetectorCatalogueFreedom

/-- The candidate canonical constraint: a detector comparison is independent of the external
orientation catalogue. -/
def CatalogueFreeConstraint (cmp : CatalogueComparison Bool) : Prop :=
  CatalogueFree cmp

/-- A catalogue-free constant-false comparison. -/
def falseDetector : CatalogueComparison Bool :=
  liftCat (fun _ _ => false)

/-- A distinct catalogue-free constant-true comparison. -/
def trueDetector : CatalogueComparison Bool :=
  liftCat (fun _ _ => true)

theorem falseDetector_catalogueFree :
    CatalogueFreeConstraint falseDetector :=
  liftCat_catalogueFree _

theorem trueDetector_catalogueFree :
    CatalogueFreeConstraint trueDetector :=
  liftCat_catalogueFree _

theorem falseDetector_ne_trueDetector :
    falseDetector ≠ trueDetector := by
  intro h
  have hx := congrFun (congrFun (congrFun h (fun _ => false)) false) false
  simp [falseDetector, trueDetector, liftCat] at hx

/-- **No unique M1-forced detector comparison exists for the catalogue-free class.** There are
at least two distinct catalogue-free witnesses, contradicting the uniqueness field of
`M1Forced`. -/
theorem no_M1Forced_catalogueFree :
    ¬ ∃ cmp : CatalogueComparison Bool,
      M1Forced CatalogueFreeConstraint cmp := by
  rintro ⟨cmp, hcmp⟩
  have hf : falseDetector = cmp :=
    hcmp.unique falseDetector falseDetector_catalogueFree
  have ht : trueDetector = cmp :=
    hcmp.unique trueDetector trueDetector_catalogueFree
  exact falseDetector_ne_trueDetector (hf.trans ht.symm)

/-- The local order no-go can be written using the canonical repository
`RequiresExternalCatalogue`, relative to `CatalogueFreeConstraint`. -/
theorem order_requires_catalogue_relative_to_constraint :
    D0.Foundation.RequiresExternalCatalogue
      CatalogueFreeConstraint
      (orderComparison : CatalogueComparison Bool) :=
  order_not_catalogueFree

/-- However, the constraint has no `M1Forced` witness, so the canonical M1 reductio theorem
`m1_alternative_needs_catalogue` cannot be applied to this whole class. -/
theorem canonical_M1_reductio_unavailable :
    (¬ ∃ cmp : CatalogueComparison Bool,
      M1Forced CatalogueFreeConstraint cmp)
      ∧ D0.Foundation.RequiresExternalCatalogue
        CatalogueFreeConstraint
        (orderComparison : CatalogueComparison Bool) :=
  ⟨no_M1Forced_catalogueFree, order_requires_catalogue_relative_to_constraint⟩

/-- Capstone: catalogue-independence excludes order, but it is not represented by the current
unique-answer M1 predicate. A class-level admissibility bridge remains necessary. -/
theorem detector_M1_predicate_boundary :
    CatalogueFreeConstraint falseDetector
      ∧ CatalogueFreeConstraint trueDetector
      ∧ falseDetector ≠ trueDetector
      ∧ (¬ ∃ cmp : CatalogueComparison Bool,
          M1Forced CatalogueFreeConstraint cmp)
      ∧ D0.Foundation.RequiresExternalCatalogue
          CatalogueFreeConstraint
          (orderComparison : CatalogueComparison Bool) :=
  ⟨falseDetector_catalogueFree, trueDetector_catalogueFree,
    falseDetector_ne_trueDetector, no_M1Forced_catalogueFree,
    order_requires_catalogue_relative_to_constraint⟩

end D0.Synthesis.DetectorM1PredicateBoundary
