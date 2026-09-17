import D0.Synthesis.TransportRootLabeling

/-!
# Mass-sector selection: the entire residual is one orientation bit

Chain so far: qualitative profile ⇒ infinite fiber (T32); unordered spectrum ⇒ ≤6 (T33);
the real order pins a unique strictly-increasing labeling (T34). What is left? Exactly the
choice between the increasing and the decreasing enumeration — a single `ℤ/2` orientation bit.

This module proves that both the strictly-monotone and the strictly-antitone enumerations of the
transport root set are unique (the antitone one is `R.root ∘ Fin.rev`), and that they differ.
So after all present-core data the generation identification retains exactly two candidates; the
sole external inputs are this orientation bit (the empirical mass order `e<μ<τ`) and the
empirical target spectrum. Nothing combinatorial remains.
-/

namespace D0.Synthesis.MassSectorSelection

open D0.Synthesis.YukawaQualitativeSelectorNoGo
open D0.Synthesis.YukawaSpectralFiber
open D0.Synthesis.TransportRootLabeling

/-- **The residual is a single orientation bit.** On the transport root frame the increasing
enumeration is the unique strictly-monotone one, the decreasing enumeration is the unique
strictly-antitone one (`R.root ∘ Fin.rev`), and the two differ. -/
theorem mass_sector_orientation_bit :
    ∃ R : TransportRootFrame,
      StrictMono R.root
        ∧ (∀ g : Fin 3 → ℝ, StrictMono g →
            (∀ i, g i ∈ ({R.root 0, R.root 1, R.root 2} : Finset ℝ)) → g = R.root)
        ∧ (∀ g : Fin 3 → ℝ, StrictAnti g →
            (∀ i, g i ∈ ({R.root 0, R.root 1, R.root 2} : Finset ℝ)) → g = R.root ∘ Fin.rev)
        ∧ R.root ≠ R.root ∘ Fin.rev
        ∧ Function.Injective (orderedEig R) := by
  obtain ⟨R, hmono, huniq, hinj⟩ := transport_root_labeling_canonical
  refine ⟨R, hmono, huniq, ?_, ?_, hinj⟩
  · -- antitone uniqueness via the monotone one
    intro g hg hgs
    have hmg : StrictMono (g ∘ Fin.rev) := by
      intro i j hij
      exact hg (Fin.rev_lt_rev.mpr hij)
    have hgs' : ∀ i, (g ∘ Fin.rev) i ∈ ({R.root 0, R.root 1, R.root 2} : Finset ℝ) :=
      fun i => hgs (Fin.rev i)
    have hcomp := huniq (g ∘ Fin.rev) hmg hgs'
    funext i
    have := congrFun hcomp (Fin.rev i)
    simpa [Function.comp, Fin.rev_rev] using this
  · -- the two orientations differ
    intro hcontra
    have h02 : R.root 0 = R.root 2 := by
      have := congrFun hcontra 0
      simpa [Function.comp, show Fin.rev (0 : Fin 3) = 2 from by decide] using this
    exact absurd h02 (ne_of_lt (hmono (by decide)))

end D0.Synthesis.MassSectorSelection
