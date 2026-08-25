import D0.Matter.Book04ConcreteSelectors
import D0.Matter.LeptonGreenPuiseuxOwner
import D0.Synthesis.GenerationRootOrderBridge

/-!
# Charged-lepton naming bridge: electron/muon/tau → inner/core/outer is order-unique

The charged-lepton branch already carries two owned structures:

* `electron` is the unique terminal calibration register;
* the exact Puiseux row is `p_e=0 < p_μ=1/4 < p_τ=1/3`.

The structural generation carrier is `GenerationPhasonMode = TorusShell` with strict radial
order `innerD9 < coreD11 < outerD13`. Therefore the order-preserving typed bridge is uniquely
forced:

`electron ↦ innerD9`, `muon ↦ coreD11`, `tau ↦ outerD13`.

This is independent of PDG masses and winding gap sizes. It closes the *naming/order* part of
the mass-sector bridge. Numerical masses and the EFT/IR matching functional remain external.
-/

namespace D0.Synthesis.ChargedLeptonShellBridge

open D0.Geometry
open D0.Matter

/-- Exact Puiseux exponent attached to each charged-lepton branch. -/
def chargedLeptonExponent : ChargedLeptonBranch → ℚ
  | .electron => p_e
  | .muon => p_mu
  | .tau => p_tau

/-- The charged-lepton exponent order is strict and data-free. -/
theorem chargedLeptonExponent_strict :
    chargedLeptonExponent .electron < chargedLeptonExponent .muon ∧
    chargedLeptonExponent .muon < chargedLeptonExponent .tau := by
  norm_num [chargedLeptonExponent, p_e, p_mu, p_tau]

/-- The unique order-preserving identification of physical branch names with structural shells. -/
def chargedLeptonShellBridge : ChargedLeptonBranch → GenerationPhasonMode
  | .electron => .innerD9
  | .muon => .coreD11
  | .tau => .outerD13

@[simp] theorem bridge_electron : chargedLeptonShellBridge .electron = .innerD9 := rfl
@[simp] theorem bridge_muon : chargedLeptonShellBridge .muon = .coreD11 := rfl
@[simp] theorem bridge_tau : chargedLeptonShellBridge .tau = .outerD13 := rfl

/-- The bridge preserves the shell radial order for every admissible torus parameter. -/
theorem chargedLeptonShellBridge_strict (T : TorusParameter) :
    TorusShell.radius T (chargedLeptonShellBridge .electron) <
      TorusShell.radius T (chargedLeptonShellBridge .muon) ∧
    TorusShell.radius T (chargedLeptonShellBridge .muon) <
      TorusShell.radius T (chargedLeptonShellBridge .tau) :=
  torusShell_radius_strictMono T

/-- **Typed naming uniqueness.** Any branch→generation-shell map whose radii increase in the
owned charged-lepton order is exactly the canonical bridge. No bijectivity hypothesis is needed:
strict increase already forces three distinct values on the three-element shell carrier. -/
theorem chargedLeptonShellBridge_unique (T : TorusParameter)
    (f : ChargedLeptonBranch → GenerationPhasonMode)
    (h01 : TorusShell.radius T (f .electron) < TorusShell.radius T (f .muon))
    (h12 : TorusShell.radius T (f .muon) < TorusShell.radius T (f .tau)) :
    f = chargedLeptonShellBridge := by
  funext b
  generalize he : f .electron = e
  generalize hm : f .muon = m
  generalize ht : f .tau = t
  cases e <;> cases m <;> cases t <;> cases b <;>
    simp_all [chargedLeptonShellBridge, TorusShell.radius, TorusShell.toShell3,
      TorusParameter.shellRadius, TorusParameter.inner, TorusParameter.core,
      TorusParameter.outer] <;> linarith [T.h_gt_one]

/-- Capstone: terminal electron + strict exponent order + unique radial bridge. The physical
charged-lepton names are now attached to the structural generation shells without mass data. -/
theorem charged_lepton_structural_naming_closed :
    StrictSelected chargedLeptonTerminalSelector ChargedLeptonBranch.electron
      ∧ chargedLeptonExponent .electron < chargedLeptonExponent .muon
      ∧ chargedLeptonExponent .muon < chargedLeptonExponent .tau
      ∧ (∀ T : TorusParameter,
          TorusShell.radius T (chargedLeptonShellBridge .electron) <
            TorusShell.radius T (chargedLeptonShellBridge .muon)
          ∧ TorusShell.radius T (chargedLeptonShellBridge .muon) <
            TorusShell.radius T (chargedLeptonShellBridge .tau))
      ∧ (∀ (T : TorusParameter) (f : ChargedLeptonBranch → GenerationPhasonMode),
          TorusShell.radius T (f .electron) < TorusShell.radius T (f .muon) →
          TorusShell.radius T (f .muon) < TorusShell.radius T (f .tau) →
          f = chargedLeptonShellBridge) :=
  ⟨charged_lepton_electron_terminal_strict, chargedLeptonExponent_strict.1,
    chargedLeptonExponent_strict.2, chargedLeptonShellBridge_strict,
    chargedLeptonShellBridge_unique⟩

end D0.Synthesis.ChargedLeptonShellBridge
