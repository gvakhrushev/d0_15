import D0.Matter.Book04ConcreteSelectors
import Mathlib.Tactic

namespace D0.Matter

/--
Finite candidates for the charged-lepton coefficient row.  The selected row is
not a free Yukawa table: it is the finite operator-origin row used by the
Book 04 generation action.
-/
inductive ChargedLeptonCoefficientRow where
  | operatorOrigin
  | pureDepthOnly
  | freeYukawaFit
  deriving DecidableEq, Repr, Fintype

/--
The coefficient-row selector ranks admissible finite origins.  The operator
origin row is the unique zero-residual candidate; depth-only and fitted-Yukawa
rows are rejected at the same frozen origin.
-/
def chargedLeptonCoefficientRowScore : ChargedLeptonCoefficientRow → ℚ
  | .operatorOrigin => 0
  | .pureDepthOnly => 1
  | .freeYukawaFit => 2

/-- Finite selector for the charged-lepton coefficient row. -/
def chargedLeptonCoefficientRowSelector : FiniteSelector ChargedLeptonCoefficientRow where
  support_fintype := inferInstance
  score := chargedLeptonCoefficientRowScore

/-- The operator-origin coefficient row is strictly selected. -/
theorem charged_lepton_operator_origin_row_strict :
    StrictSelected chargedLeptonCoefficientRowSelector
      ChargedLeptonCoefficientRow.operatorOrigin := by
  constructor
  intro b hb
  cases b with
  | operatorOrigin => exact False.elim (hb rfl)
  | pureDepthOnly => norm_num [chargedLeptonCoefficientRowSelector, chargedLeptonCoefficientRowScore]
  | freeYukawaFit => norm_num [chargedLeptonCoefficientRowSelector, chargedLeptonCoefficientRowScore]

/-- Certificate for the charged-lepton finite coefficient-origin row. -/
def chargedLeptonCoefficientRowCertificate :
    StrictSelectorCertificate ChargedLeptonCoefficientRow where
  selector := chargedLeptonCoefficientRowSelector
  selected := ChargedLeptonCoefficientRow.operatorOrigin
  selected_strict := charged_lepton_operator_origin_row_strict

/--
Dimensionless ratio coefficients attached to a coefficient-row candidate.  The
operator row records the active Book 04 coefficient line; the alternatives are
control rows used only to state no-free-retuning theorems.
-/
def chargedLeptonRatioCoefficient :
    ChargedLeptonCoefficientRow → ChargedLeptonBranch → ℚ
  | .operatorOrigin, .electron => 1
  | .operatorOrigin, .muon => 38814328681047283 / 10000000000000000
  | .operatorOrigin, .tau => 103183483253993735 / 10000000000000000
  | .pureDepthOnly, _ => 1
  | .freeYukawaFit, .electron => 1
  | .freeYukawaFit, .muon => 2
  | .freeYukawaFit, .tau => 3

/-- Electroweak-depth exponents attached to a coefficient-row candidate. -/
def chargedLeptonDepthExponent :
    ChargedLeptonCoefficientRow → ChargedLeptonBranch → ℚ
  | .operatorOrigin, .electron => 0
  | .operatorOrigin, .muon => 1 / 4
  | .operatorOrigin, .tau => 1 / 3
  | .pureDepthOnly, .electron => 0
  | .pureDepthOnly, .muon => 1 / 4
  | .pureDepthOnly, .tau => 1 / 3
  | .freeYukawaFit, _ => 0

/-- Residual bridge factors attached to a coefficient-row candidate. -/
def chargedLeptonBridgeFactor :
    ChargedLeptonCoefficientRow → ChargedLeptonBranch → ℚ
  | .operatorOrigin, _ => 1
  | .pureDepthOnly, _ => 1
  | .freeYukawaFit, .electron => 1
  | .freeYukawaFit, .muon => 2
  | .freeYukawaFit, .tau => 3

/--
A charged-lepton coefficient origin is a selected finite row plus the three
coefficient functions used by the generation action.  The functions must be
read from the selected row; they are not independent fit knobs.
-/
structure ChargedLeptonCoefficientOrigin where
  row : ChargedLeptonCoefficientRow
  row_strict : StrictSelected chargedLeptonCoefficientRowSelector row
  ratio : ChargedLeptonBranch → ℚ
  exponent : ChargedLeptonBranch → ℚ
  bridge : ChargedLeptonBranch → ℚ
  ratio_eq : ratio = chargedLeptonRatioCoefficient row
  exponent_eq : exponent = chargedLeptonDepthExponent row
  bridge_eq : bridge = chargedLeptonBridgeFactor row

/-- Concrete Book 04 charged-lepton coefficient origin. -/
def concreteChargedLeptonCoefficientOrigin : ChargedLeptonCoefficientOrigin where
  row := ChargedLeptonCoefficientRow.operatorOrigin
  row_strict := charged_lepton_operator_origin_row_strict
  ratio := chargedLeptonRatioCoefficient ChargedLeptonCoefficientRow.operatorOrigin
  exponent := chargedLeptonDepthExponent ChargedLeptonCoefficientRow.operatorOrigin
  bridge := chargedLeptonBridgeFactor ChargedLeptonCoefficientRow.operatorOrigin
  ratio_eq := rfl
  exponent_eq := rfl
  bridge_eq := rfl

/-- Any charged-lepton coefficient origin has the same selected row. -/
theorem charged_lepton_coefficient_origin_row_unique
    (O : ChargedLeptonCoefficientOrigin) :
    O.row = ChargedLeptonCoefficientRow.operatorOrigin := by
  exact strict_selected_unique chargedLeptonCoefficientRowSelector O.row_strict
    charged_lepton_operator_origin_row_strict

/--
At the fixed finite coefficient origin, the ratio/exponent/bridge coefficient
functions are forced.  This is the theorem-level replacement for treating
`r_g`, `p_g`, and `B_g` as free charged-lepton knobs.
-/
theorem charged_lepton_coefficient_table_forced
    (O : ChargedLeptonCoefficientOrigin) :
    O.ratio = chargedLeptonRatioCoefficient ChargedLeptonCoefficientRow.operatorOrigin ∧
      O.exponent = chargedLeptonDepthExponent ChargedLeptonCoefficientRow.operatorOrigin ∧
        O.bridge = chargedLeptonBridgeFactor ChargedLeptonCoefficientRow.operatorOrigin := by
  have hrow := charged_lepton_coefficient_origin_row_unique O
  constructor
  · simpa [hrow] using O.ratio_eq
  constructor
  · simpa [hrow] using O.exponent_eq
  · simpa [hrow] using O.bridge_eq

/-- No alternative coefficient row is selectable at the same finite origin. -/
theorem charged_lepton_coefficient_no_free_row_alternative
    (row : ChargedLeptonCoefficientRow)
    (hrow : row ≠ ChargedLeptonCoefficientRow.operatorOrigin) :
    ¬ StrictSelected chargedLeptonCoefficientRowSelector row := by
  exact physical_selector_no_free_alternative chargedLeptonCoefficientRowCertificate row hrow

/--
Changing any one of the three charged-lepton coefficient functions is a real
origin deformation, not a notation change.
-/
theorem charged_lepton_coefficients_no_free_retuning
    (O : ChargedLeptonCoefficientOrigin) :
    ¬ (O.ratio ≠ chargedLeptonRatioCoefficient ChargedLeptonCoefficientRow.operatorOrigin ∨
      O.exponent ≠ chargedLeptonDepthExponent ChargedLeptonCoefficientRow.operatorOrigin ∨
        O.bridge ≠ chargedLeptonBridgeFactor ChargedLeptonCoefficientRow.operatorOrigin) := by
  intro h
  rcases charged_lepton_coefficient_table_forced O with ⟨hr, hp, hb⟩
  rcases h with hratio | hexp | hbridge
  · exact hratio hr
  · exact hexp hp
  · exact hbridge hb

end D0.Matter
