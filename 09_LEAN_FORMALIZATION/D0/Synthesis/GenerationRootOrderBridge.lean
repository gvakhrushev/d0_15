import D0.Geometry.TorusShellAttachment
import D0.Matter.PhasonStrainGenerations
import D0.Synthesis.TransportRootLabeling

/-!
# Generation-root order bridge: the structural orientation is internal

`GenerationPhasonMode` is definitionally `TorusShell`; `TorusShellAttachment` owns its radial
order `innerD9 < coreD11 < outerD13`; `TransportRootLabeling` owns the unique increasing order of
the three transport roots. Therefore there is a unique order-preserving bridge from structural
generation modes to transport roots. This closes the orientation bit of T35 on the *structural*
generation carrier. The sole external residue is now only the naming of those ordered modes as
physical `electron/muon/tau` and the empirical target spectrum — not any ordering choice.
-/

namespace D0.Synthesis.GenerationRootOrderBridge

open D0.Geometry
open D0.Matter
open D0.Synthesis.YukawaQualitativeSelectorNoGo
open D0.Synthesis.YukawaSpectralFiber
open D0.Synthesis.TransportRootLabeling

/-- The canonical order-preserving map from structural generation shells to transport roots. -/
def generationRootBridge (R : TransportRootFrame) : GenerationPhasonMode → ℝ :=
  fun s => R.root (torusShellEquivShell3 s)

@[simp] theorem generationRootBridge_inner (R : TransportRootFrame) :
    generationRootBridge R .innerD9 = R.root 0 := rfl

@[simp] theorem generationRootBridge_core (R : TransportRootFrame) :
    generationRootBridge R .coreD11 = R.root 1 := rfl

@[simp] theorem generationRootBridge_outer (R : TransportRootFrame) :
    generationRootBridge R .outerD13 = R.root 2 := rfl

/-- **Structural generation-root orientation is unique.** Any map from generation/phason modes
to the same root set that preserves the owned radial order equals the canonical bridge. -/
theorem generation_root_order_bridge_unique :
    ∃ R : TransportRootFrame,
      StrictMono R.root
        ∧ generationRootBridge R .innerD9 < generationRootBridge R .coreD11
        ∧ generationRootBridge R .coreD11 < generationRootBridge R .outerD13
        ∧ (∀ f : GenerationPhasonMode → ℝ,
            f .innerD9 < f .coreD11 → f .coreD11 < f .outerD13 →
            (∀ s, f s ∈ ({R.root 0, R.root 1, R.root 2} : Finset ℝ)) →
            f = generationRootBridge R)
        ∧ Function.Injective (orderedEig R) := by
  obtain ⟨R, hmono, huniq, hinj⟩ := transport_root_labeling_canonical
  refine ⟨R, hmono, hmono (by decide), hmono (by decide), ?_, hinj⟩
  intro f h01 h12 hmem
  let g : Fin 3 → ℝ := fun i => f (torusShellEquivShell3.symm i)
  have hg : StrictMono g := by
    intro i j hij
    fin_cases i <;> fin_cases j <;>
      simp_all [g, torusShellEquivShell3, TorusShell.ofShell3]
    exact lt_trans h01 h12
  have hgmem : ∀ i, g i ∈ ({R.root 0, R.root 1, R.root 2} : Finset ℝ) := by
    intro i
    exact hmem (torusShellEquivShell3.symm i)
  have hgeq : g = R.root := huniq g hg hgmem
  funext s
  have hs := congrFun hgeq (torusShellEquivShell3 s)
  simpa [g, generationRootBridge] using hs

end D0.Synthesis.GenerationRootOrderBridge
