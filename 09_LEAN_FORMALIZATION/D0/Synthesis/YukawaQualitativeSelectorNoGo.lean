import Mathlib.LinearAlgebra.Matrix.Notation
import D0.Synthesis.YukawaCommutantSpectrum

/-!
# Yukawa selector no-go: the owned qualitative profile cannot choose `(a,b,c)`

The equivariant Yukawa class is

`Y(a,b,c; λ) = a + bλ + cλ²`,  with `a,b,c ∈ ℚ`.

`YukawaCommutantSpectrum` proves two universal facts for every non-scalar member
`(b,c) ≠ (0,0)`:

1. its values at the three transport roots are pairwise distinct;
2. every value is irrational.

Those are strong rigidity statements, but they do not select coefficients. This module
proves the exact obstruction:

* all non-scalar coefficient triples have the same equality/rationality profile;
* an injective rational one-parameter family `(0,1,t)` lies entirely in that one profile;
* therefore any selector factoring only through the owned profile is constant on an
  infinite family and cannot have a unique non-scalar winner;
* conversely, every unique selector must distinguish two operators that the present
  profile declares equivalent — it needs a genuinely new quantitative functional.

This is the exact theorem-level boundary behind the former status phrase
"an owned `(a,b,c)` selector is missing".
-/

namespace D0.Synthesis.YukawaQualitativeSelectorNoGo

open D0.Synthesis.YukawaCommutantSpectrum

/-- Rational coefficients of an equivariant Yukawa polynomial. -/
structure YukawaCoeff where
  a : ℚ
  b : ℚ
  c : ℚ
  deriving DecidableEq, Repr

/-- The scalar line consists exactly of triples with `b=c=0`. -/
def NonScalar (k : YukawaCoeff) : Prop :=
  ¬ (k.b = 0 ∧ k.c = 0)

/-- Value of the polynomial member at a real transport eigenvalue. -/
def yukawaValue (k : YukawaCoeff) (x : ℝ) : ℝ :=
  (k.a : ℝ) + k.b * x + k.c * x ^ 2

/-- A typed enumeration of the three distinct real roots of the transport cubic. -/
structure TransportRootFrame where
  root : Fin 3 → ℝ
  isRoot : ∀ i, root i ^ 3 - 359 * root i - 2574 = 0
  injective : Function.Injective root

/-- The exact currently-owned qualitative profile: equality pattern of the three
generation values plus all rational-value tests. -/
def OwnedProfileEquivalent (R : TransportRootFrame) (k l : YukawaCoeff) : Prop :=
  (∀ i j,
      yukawaValue k (R.root i) = yukawaValue k (R.root j) ↔
      yukawaValue l (R.root i) = yukawaValue l (R.root j))
    ∧
  (∀ (i : Fin 3) (q : ℚ),
      yukawaValue k (R.root i) = (q : ℝ) ↔
      yukawaValue l (R.root i) = (q : ℝ))

/-- Every non-scalar member separates the three root directions. -/
theorem nonScalar_values_injective (R : TransportRootFrame) (k : YukawaCoeff)
    (hk : NonScalar k) :
    Function.Injective (fun i => yukawaValue k (R.root i)) := by
  intro i j hij
  by_contra hne
  exact qq_spectrum_splits k.a k.b k.c hk (R.root i) (R.root j)
    (R.isRoot i) (R.isRoot j) (R.injective.ne hne) hij

/-- Every non-scalar value at every transport root is irrational. -/
theorem nonScalar_values_irrational (R : TransportRootFrame) (k : YukawaCoeff)
    (hk : NonScalar k) :
    ∀ (i : Fin 3) (q : ℚ), yukawaValue k (R.root i) ≠ (q : ℝ) := by
  intro i q
  exact no_rational_value_at_root k.a k.b k.c q hk (R.root i) (R.isRoot i)

/-- **Profile collapse.** All non-scalar coefficient triples are indistinguishable by
the complete equality/rationality profile currently owned by the theory. -/
theorem all_nonScalar_profile_equivalent (R : TransportRootFrame)
    (k l : YukawaCoeff) (hk : NonScalar k) (hl : NonScalar l) :
    OwnedProfileEquivalent R k l := by
  have hik := nonScalar_values_injective R k hk
  have hil := nonScalar_values_injective R l hl
  have hqk := nonScalar_values_irrational R k hk
  have hql := nonScalar_values_irrational R l hl
  constructor
  · intro i j
    constructor
    · intro h
      exact congrArg (fun x => yukawaValue l (R.root x)) (hik h)
    · intro h
      exact congrArg (fun x => yukawaValue k (R.root x)) (hil h)
  · intro i q
    constructor
    · intro h
      exact (hqk i q h).elim
    · intro h
      exact (hql i q h).elim

/-- An explicit infinite rational line of non-scalar coefficient choices. -/
def affineFamily (t : ℚ) : YukawaCoeff :=
  ⟨0, 1, t⟩

theorem affineFamily_nonScalar (t : ℚ) : NonScalar (affineFamily t) := by
  simp [NonScalar, affineFamily]

theorem affineFamily_injective : Function.Injective affineFamily := by
  intro s t h
  exact congrArg YukawaCoeff.c h

/-- Every point of the injective rational line `(0,1,t)` has the same owned profile. -/
theorem affineFamily_profile_collapse (R : TransportRootFrame) (s t : ℚ) :
    OwnedProfileEquivalent R (affineFamily s) (affineFamily t) :=
  all_nonScalar_profile_equivalent R _ _
    (affineFamily_nonScalar s) (affineFamily_nonScalar t)

/-- A selector uses no information beyond the current theorem-level profile when it
is invariant under `OwnedProfileEquivalent`. -/
def FactorsThroughOwnedProfile (R : TransportRootFrame)
    (select : YukawaCoeff → Prop) : Prop :=
  ∀ k l, OwnedProfileEquivalent R k l → (select k ↔ select l)

/-- Every profile-based selector is constant on all non-scalar coefficients. -/
theorem profile_selector_constant_on_nonScalar (R : TransportRootFrame)
    (select : YukawaCoeff → Prop) (hselect : FactorsThroughOwnedProfile R select)
    (k l : YukawaCoeff) (hk : NonScalar k) (hl : NonScalar l) :
    select k ↔ select l :=
  hselect k l (all_nonScalar_profile_equivalent R k l hk hl)

/-- **Selector no-go.** No predicate factoring only through the owned qualitative
profile can select a unique non-scalar Yukawa coefficient triple. -/
theorem no_unique_nonScalar_profile_selector (R : TransportRootFrame)
    (select : YukawaCoeff → Prop) (hselect : FactorsThroughOwnedProfile R select) :
    ¬ ∃! k : YukawaCoeff, NonScalar k ∧ select k := by
  rintro ⟨k, hk, huniq⟩
  have h0 : NonScalar (affineFamily 0) := affineFamily_nonScalar 0
  have h1 : NonScalar (affineFamily 1) := affineFamily_nonScalar 1
  have hs0 : select (affineFamily 0) :=
    (profile_selector_constant_on_nonScalar R select hselect k (affineFamily 0) hk.1 h0).mp hk.2
  have hs1 : select (affineFamily 1) :=
    (profile_selector_constant_on_nonScalar R select hselect k (affineFamily 1) hk.1 h1).mp hk.2
  have heq0 := huniq (affineFamily 0) ⟨h0, hs0⟩
  have heq1 := huniq (affineFamily 1) ⟨h1, hs1⟩
  have : affineFamily (0 : ℚ) = affineFamily 1 := heq0.trans heq1.symm
  exact (by norm_num : (0 : ℚ) ≠ 1) (affineFamily_injective this)

/-- Equivalent positive boundary: any genuinely unique non-scalar selector must fail
profile invariance, i.e. distinguish operators with identical presently-owned outcomes. -/
theorem unique_selector_requires_new_information (R : TransportRootFrame)
    (select : YukawaCoeff → Prop)
    (huniq : ∃! k : YukawaCoeff, NonScalar k ∧ select k) :
    ¬ FactorsThroughOwnedProfile R select := by
  intro hfactor
  exact no_unique_nonScalar_profile_selector R select hfactor huniq

/-- The transport cubic supplies a concrete root frame. -/
theorem transportRootFrame_exists : Nonempty TransportRootFrame := by
  obtain ⟨l0, l1, l2, h0, h1, h2, hb0, hb1, hb2, h01, h12⟩ :=
    transport_three_real_roots
  let roots : Fin 3 → ℝ := ![l0, l1, l2]
  refine ⟨⟨roots, ?_, ?_⟩⟩
  · intro i
    fin_cases i <;> simp [roots, h0, h1, h2]
  · intro i j hij
    fin_cases i <;> fin_cases j <;>
      simp_all [roots] <;> linarith

/-- Capstone: on an actual three-root transport frame, the owned profile collapses an
injective rational one-parameter family and cannot support a unique Yukawa selector. -/
theorem transport_yukawa_selector_nogo :
    ∃ R : TransportRootFrame,
      Function.Injective affineFamily
        ∧ (∀ s t, OwnedProfileEquivalent R (affineFamily s) (affineFamily t))
        ∧ (∀ select : YukawaCoeff → Prop,
            FactorsThroughOwnedProfile R select →
            ¬ ∃! k : YukawaCoeff, NonScalar k ∧ select k) := by
  obtain ⟨R⟩ := transportRootFrame_exists
  exact ⟨R, affineFamily_injective, affineFamily_profile_collapse R,
    no_unique_nonScalar_profile_selector R⟩

end D0.Synthesis.YukawaQualitativeSelectorNoGo
