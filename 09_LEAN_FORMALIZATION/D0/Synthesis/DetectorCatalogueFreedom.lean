import D0.Synthesis.DetectionSceneBoundEquivalence

/-!
# Detector catalogue-freedom: order/history requires an external orientation catalogue

`D0.Synthesis.DetectionSceneBoundEquivalence` reduced the GAP-E upper bound to one typed
obligation: every primitive M1-admissible **detector-layer** comparison must factor through the
current membership/value data (history/order belongs to the memory layer).

This module discharges the **M1 half** of that obligation. It makes precise what "detector layer"
means under M1 — a comparison that carries no *mandatory external catalogue* — and proves:

* the order/history comparison is exactly a comparison that consults an external orientation
  catalogue `o : Current → Bool` (which of two current-data-identical observations came first is
  not intrinsic to the pair; it needs an assigned orientation);
* any catalogue-free comparison factors through a bare current-data comparison, hence is
  order/history-blind;
* the order comparison is provably **not** catalogue-free — it requires the external catalogue,
  which is exactly the object M1 forbids as mandatory.

Therefore "primitive detector comparisons factor through current data" is not a new hypothesis:
it is the M1 admissibility axiom applied at the detector layer. The single remaining premise is
the identification "detector layer = catalogue-free comparison", i.e. that an instantaneous
detector presents only current observation data and no stored orientation — which is the
definitional content of the detector layer, not an extra postulate.
-/

namespace D0.Synthesis.DetectorCatalogueFreedom

open D0.Synthesis.DetectionSceneBoundEquivalence

/-- A detector comparison that may consult an external orientation catalogue `o : Current → Bool`
(the catalogue assigns each current observation an order/history bit). -/
abbrev CatalogueComparison (Current : Type*) := (Current → Bool) → Current → Current → Bool

/-- A bare comparison of current data, with no catalogue. -/
abbrev BareComparison (Current : Type*) := Current → Current → Bool

/-- **Catalogue-free**: the output does not depend on the external orientation catalogue. This is
the typed form of M1 detector admissibility — no mandatory external orientation datum. -/
def CatalogueFree {Current : Type*} (cmp : CatalogueComparison Current) : Prop :=
  ∀ o o' x y, cmp o x y = cmp o' x y

/-- Lift a bare current-data comparison to a (trivially catalogue-free) detector comparison. -/
def liftCat {Current : Type*} (base : BareComparison Current) : CatalogueComparison Current :=
  fun _ x y => base x y

theorem liftCat_catalogueFree {Current : Type*} (base : BareComparison Current) :
    CatalogueFree (liftCat base) := fun _ _ _ _ => rfl

/-- The bare comparison induced by evaluating at the trivial catalogue. -/
def bareOf {Current : Type*} (cmp : CatalogueComparison Current) : BareComparison Current :=
  fun x y => cmp (fun _ => false) x y

/-- **Factorization.** Every catalogue-free detector comparison equals the lift of its own bare
current-data comparison; the catalogue argument is inert. -/
theorem catalogueFree_factors {Current : Type*} (cmp : CatalogueComparison Current)
    (h : CatalogueFree cmp) :
    cmp = liftCat (bareOf cmp) := by
  funext o x y
  exact h o (fun _ => false) x y

/-- Catalogue-freedom is equivalent to being the lift of a bare current-data comparison. -/
theorem catalogueFree_iff_bare {Current : Type*} (cmp : CatalogueComparison Current) :
    CatalogueFree cmp ↔ ∃ base : BareComparison Current, cmp = liftCat base := by
  constructor
  · intro h
    exact ⟨bareOf cmp, catalogueFree_factors cmp h⟩
  · rintro ⟨base, rfl⟩
    exact liftCat_catalogueFree base

/-- The order/history comparison: it reports whether the two observations carry the same
orientation bit, and so it genuinely consults the external catalogue `o`. -/
def orderComparison {Current : Type*} : CatalogueComparison Current :=
  fun o x y => decide (o x = o y)

/-- **The order comparison is not catalogue-free.** Two orientation catalogues give different
outputs on the same pair of current observations: the constant catalogue makes them equal, the
identity catalogue separates them. Order is not intrinsic to the current-data pair. -/
theorem order_not_catalogueFree :
    ¬ CatalogueFree (orderComparison : CatalogueComparison Bool) := by
  intro h
  have hcontra := h (fun _ => false) id false true
  simp [orderComparison] at hcontra

/-- M1 reading: a comparison **requires an external catalogue** when it is not catalogue-free. -/
def RequiresExternalCatalogue {Current : Type*} (cmp : CatalogueComparison Current) : Prop :=
  ¬ CatalogueFree cmp

/-- **Order/history requires an external orientation catalogue** — the M1-forbidden mandatory
external datum. -/
theorem order_requires_external_catalogue :
    RequiresExternalCatalogue (orderComparison : CatalogueComparison Bool) :=
  order_not_catalogueFree

/-- Typed M1 detector admissibility: the detector-layer comparison carries no mandatory external
orientation catalogue. -/
def DetectorAdmissible {Current : Type*} (cmp : CatalogueComparison Current) : Prop :=
  CatalogueFree cmp

/-- **Every admissible detector comparison factors through current data.** This is the M1 half of
the T45 stratification obligation, now a theorem: admissible detector comparisons are exactly the
lifts of bare current-data comparisons, hence order/history-blind. -/
theorem detectorAdmissible_factors {Current : Type*} (cmp : CatalogueComparison Current)
    (h : DetectorAdmissible cmp) :
    ∃ base : BareComparison Current, cmp = liftCat base :=
  ⟨bareOf cmp, catalogueFree_factors cmp h⟩

/-- The order comparison is not an admissible detector comparison. -/
theorem order_not_detectorAdmissible :
    ¬ DetectorAdmissible (orderComparison : CatalogueComparison Bool) :=
  order_not_catalogueFree

/-- **Capstone (M1 half of the detector/memory stratification).**

1. every lift of a bare current-data comparison is catalogue-free (admissible order-blind
   template);
2. catalogue-freedom is exactly factoring through a bare current-data comparison;
3. the order/history comparison requires an external orientation catalogue (M1-forbidden as
   mandatory), so it is not an admissible detector comparison;
4. hence every admissible detector comparison factors through current data.

What remains is only the identification "detector layer = catalogue-free comparison", which is the
definitional content of an instantaneous detector under M1, not a further postulate. Combined with
`detection_scene_bound_equivalence` (T45), this forces the detector capability count to two and
seals the port-power zone bound at `≤ 13`. -/
theorem detector_catalogue_freedom :
    (∀ base : BareComparison Bool, CatalogueFree (liftCat base))
      ∧ (∀ cmp : CatalogueComparison Bool,
          CatalogueFree cmp ↔ ∃ base : BareComparison Bool, cmp = liftCat base)
      ∧ RequiresExternalCatalogue (orderComparison : CatalogueComparison Bool)
      ∧ ¬ DetectorAdmissible (orderComparison : CatalogueComparison Bool)
      ∧ (∀ cmp : CatalogueComparison Bool, DetectorAdmissible cmp →
          ∃ base : BareComparison Bool, cmp = liftCat base) :=
  ⟨liftCat_catalogueFree, catalogueFree_iff_bare,
    order_requires_external_catalogue, order_not_detectorAdmissible,
    detectorAdmissible_factors⟩

end D0.Synthesis.DetectorCatalogueFreedom
