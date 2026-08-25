import Mathlib.Data.Finset.Sort
import D0.Synthesis.YukawaSpectralFiber

/-!
# The transport-root generation labeling is canonically fixed by the real order

`YukawaSpectralFiber` (T33) reduced the Yukawa coefficient ambiguity to the `S₃` relabeling of
the three transport roots and named the residual `PRIM-GENERATION-ROOT-LABELING`. This module
resolves the *mathematical* half of that primitive: the three real roots are linearly ordered,
so there is a **unique** strictly-increasing enumeration of them. Consequently the `S₃`
labeling freedom is not free — the reals canonically order the roots, and the only genuinely
external residue is the order-preserving identification of the ordered roots with the physical
generation labels `e < μ < τ` (a single monotone bridge, not an `S₃` choice).
-/

namespace D0.Synthesis.TransportRootLabeling

open D0.Synthesis.YukawaQualitativeSelectorNoGo
open D0.Synthesis.YukawaSpectralFiber
open D0.Synthesis.YukawaCommutantSpectrum

/-- **Canonical generation labeling.** There is a transport root frame whose roots are strictly
increasing, whose ordering is the *unique* strictly-monotone enumeration of the three roots, and
on which the labeled Yukawa coefficient map is injective. Hence the `T33` `S₃` residue collapses
to the identity once the intrinsic real order is used. -/
theorem transport_root_labeling_canonical :
    ∃ R : TransportRootFrame,
      StrictMono R.root
        ∧ (∀ g : Fin 3 → ℝ, StrictMono g →
            (∀ i, g i ∈ ({R.root 0, R.root 1, R.root 2} : Finset ℝ)) → g = R.root)
        ∧ Function.Injective (orderedEig R) := by
  classical
  obtain ⟨l0, l1, l2, h0, h1, h2, _, _, _, h01, h12⟩ := transport_three_real_roots
  set root : Fin 3 → ℝ := fun i => if i = 0 then l0 else if i = 1 then l1 else l2 with hroot
  have h02 : l0 < l2 := lt_trans h01 h12
  have hmono : StrictMono root := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp_all
  have hisRoot : ∀ i, (root i) ^ 3 - 359 * root i - 2574 = 0 := by
    intro i
    fin_cases i
    · simpa [hroot] using h0
    · simpa [hroot] using h1
    · simpa [hroot] using h2
  refine ⟨⟨root, hisRoot, hmono.injective⟩, hmono, ?_, orderedEig_injective _⟩
  intro g hg hgs
  show g = root
  replace hgs : ∀ i, g i ∈ ({root 0, root 1, root 2} : Finset ℝ) := hgs
  have hne01 : root 0 ≠ root 1 := ne_of_lt (hmono (by decide))
  have hne02 : root 0 ≠ root 2 := ne_of_lt (hmono (by decide))
  have hne12 : root 1 ≠ root 2 := ne_of_lt (hmono (by decide))
  have hcard : ({root 0, root 1, root 2} : Finset ℝ).card = 3 := by
    rw [Finset.card_eq_three]
    exact ⟨root 0, root 1, root 2, hne01, hne02, hne12, rfl⟩
  have hroots : ∀ i, root i ∈ ({root 0, root 1, root 2} : Finset ℝ) := by
    intro i
    fin_cases i
    · exact Finset.mem_insert_self _ _
    · exact Finset.mem_insert_of_mem (Finset.mem_insert_self _ _)
    · exact Finset.mem_insert_of_mem (Finset.mem_insert_of_mem (Finset.mem_singleton_self _))
  have hg_eq := Finset.orderEmbOfFin_unique hcard hgs hg
  have hroot_eq := Finset.orderEmbOfFin_unique hcard hroots hmono
  exact hg_eq.trans hroot_eq.symm

end D0.Synthesis.TransportRootLabeling
