import D0.Topology.GenericTripartiteSimplicialSet
import Mathlib.AlgebraicTopology.SimplicialSet.AnodyneExtensions.IsUniquelyCodimOneFace
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-SIMPLICIAL-MORSE-001

Transport the canonical perfect matching from typed faces to the actual
nondegenerate simplices of the Mathlib simplicial-set realization.
-/

namespace D0.Topology.GenericTripartiteSimplicialMorse

open D0.Topology.GenericTripartiteAbstractComplex
open D0.Topology.GenericTripartiteDiscreteMorse
open D0.Topology.GenericTripartiteSimplicialSet
open D0.Topology.GenericTripartiteTopHomologyRing

variable {p q r : ℕ}

noncomputable abbrev TripartiteSSet (p q r : ℕ) : SSet :=
  (simplicialSet (p:=p) (q:=q) (r:=r) : SSet)

abbrev NondegenerateFace (p q r : ℕ) := (TripartiteSSet p q r).N

@[simp] theorem nondegenerateFaceEquiv_dimension
    (x : NondegenerateFace p q r) :
    Face.dimension (nondegenerateFaceEquiv x) = x.dim := by
  calc
    Face.dimension (nondegenerateFaceEquiv x) =
        (faceToNondegenerate (nondegenerateFaceEquiv x)).dim :=
      (faceToNondegenerate_dim _).symm
    _ = (faceNondegenerateEquiv (nondegenerateFaceEquiv x)).dim := by
      rw [faceNondegenerateEquiv_apply]
    _ = x.dim := congrArg (fun y : NondegenerateFace p q r => y.dim)
      ((nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).symm_apply_apply x)


/-- Upper matching transported to actual nondegenerate simplices. -/
noncomputable def pairUpper (x : NondegenerateFace p q r) :
    Option (NondegenerateFace p q r) :=
  (Face.pairUpper (nondegenerateFaceEquiv x)).map faceNondegenerateEquiv

/-- Lower matching transported to actual nondegenerate simplices. -/
noncomputable def pairLower (x : NondegenerateFace p q r) :
    Option (NondegenerateFace p q r) :=
  (Face.pairLower (nondegenerateFaceEquiv x)).map faceNondegenerateEquiv

@[simp] theorem pairUpper_face (f : Face p q r) :
    pairUpper (faceNondegenerateEquiv f) =
      (Face.pairUpper f).map faceNondegenerateEquiv := by
  simp [pairUpper]

@[simp] theorem pairLower_face (f : Face p q r) :
    pairLower (faceNondegenerateEquiv f) =
      (Face.pairLower f).map faceNondegenerateEquiv := by
  simp [pairLower]

@[simp] theorem pairUpper_isSome_iff (x : NondegenerateFace p q r) :
    (pairUpper x).isSome ↔
      (Face.pairUpper (nondegenerateFaceEquiv x)).isSome := by
  simp [pairUpper]

@[simp] theorem pairLower_isSome_iff (x : NondegenerateFace p q r) :
    (pairLower x).isSome ↔
      (Face.pairLower (nondegenerateFaceEquiv x)).isSome := by
  simp [pairLower]

lemma pairUpper_eq_some_iff {lower upper : NondegenerateFace p q r} :
    pairUpper lower = some upper ↔
      Face.pairUpper (nondegenerateFaceEquiv lower) =
        some (nondegenerateFaceEquiv upper) := by
  constructor
  · intro h
    simp only [pairUpper, Option.map_eq_some_iff] at h
    obtain ⟨f, hf, hfu⟩ := h
    have hfeq : f = nondegenerateFaceEquiv upper := by
      calc
        f = nondegenerateFaceEquiv (faceNondegenerateEquiv f) :=
          ((nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).apply_symm_apply f).symm
        _ = nondegenerateFaceEquiv upper := congrArg nondegenerateFaceEquiv hfu
    simpa [hfeq] using hf
  · intro h
    simp only [pairUpper, Option.map_eq_some_iff]
    exact ⟨nondegenerateFaceEquiv upper, h,
      (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).symm_apply_apply upper⟩

lemma pairLower_eq_some_iff {upper lower : NondegenerateFace p q r} :
    pairLower upper = some lower ↔
      Face.pairLower (nondegenerateFaceEquiv upper) =
        some (nondegenerateFaceEquiv lower) := by
  constructor
  · intro h
    simp only [pairLower, Option.map_eq_some_iff] at h
    obtain ⟨f, hf, hfl⟩ := h
    have hfeq : f = nondegenerateFaceEquiv lower := by
      calc
        f = nondegenerateFaceEquiv (faceNondegenerateEquiv f) :=
          ((nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).apply_symm_apply f).symm
        _ = nondegenerateFaceEquiv lower := congrArg nondegenerateFaceEquiv hfl
    simpa [hfeq] using hf
  · intro h
    simp only [pairLower, Option.map_eq_some_iff]
    exact ⟨nondegenerateFaceEquiv lower, h,
      (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).symm_apply_apply lower⟩


/-- Every transported upper pair is a codimension-one typed face pair and
therefore differs in simplicial dimension by one. -/
private lemma codimOne_dimension {lower upper : Face p q r}
    (h : Face.CodimOne lower upper) :
    Face.dimension upper = Face.dimension lower + 1 := by
  rcases lower with v | e | t <;> rcases upper with v' | e' | t' <;>
    simp_all [Face.CodimOne, Face.dimension]

/-- On typed tripartite faces, an inclusion of vertex supports with a
dimension jump of one is exactly a codimension-one face relation. -/
lemma codimOne_of_vertices_subset_of_dimension
    {lower upper : Face p q r}
    (hsub : Face.vertices lower ⊆ Face.vertices upper)
    (hdim : Face.dimension upper = Face.dimension lower + 1) :
    Face.CodimOne lower upper := by
  rcases lower with v | e | t
  · rcases upper with v' | e' | t'
    · simp [Face.dimension] at hdim
    · rcases v with a | bc
      · rcases e' with ab | rest
        · rcases ab with ⟨a',b⟩
          simp [Face.vertices, Face.toCoordinates,
            FaceCoordinates.vertices, Face.CodimOne] at hsub ⊢
          exact hsub
        · rcases rest with ac | bc'
          · rcases ac with ⟨a',c⟩
            simp [Face.vertices, Face.toCoordinates,
              FaceCoordinates.vertices, Face.CodimOne] at hsub ⊢
            exact hsub
          · rcases bc' with ⟨b,c⟩
            simp [Face.vertices, Face.toCoordinates,
              FaceCoordinates.vertices] at hsub
      · rcases bc with b | c
        · rcases e' with ab | rest
          · rcases ab with ⟨a,b'⟩
            simp [Face.vertices, Face.toCoordinates,
              FaceCoordinates.vertices, Face.CodimOne] at hsub ⊢
            exact hsub
          · rcases rest with ac | bc'
            · rcases ac with ⟨a,c⟩
              simp [Face.vertices, Face.toCoordinates,
                FaceCoordinates.vertices] at hsub
            · rcases bc' with ⟨b',c⟩
              simp [Face.vertices, Face.toCoordinates,
                FaceCoordinates.vertices, Face.CodimOne] at hsub ⊢
              exact hsub
        · rcases e' with ab | rest
          · rcases ab with ⟨a,b⟩
            simp [Face.vertices, Face.toCoordinates,
              FaceCoordinates.vertices] at hsub
          · rcases rest with ac | bc'
            · rcases ac with ⟨a,c'⟩
              simp [Face.vertices, Face.toCoordinates,
                FaceCoordinates.vertices, Face.CodimOne] at hsub ⊢
              exact hsub
            · rcases bc' with ⟨b,c'⟩
              simp [Face.vertices, Face.toCoordinates,
                FaceCoordinates.vertices, Face.CodimOne] at hsub ⊢
              exact hsub
    · simp [Face.dimension] at hdim
  · rcases upper with v' | e' | t'
    · simp [Face.dimension] at hdim
    · simp [Face.dimension] at hdim
    · rcases e with ab | rest
      · rcases ab with ⟨a,b⟩
        rcases t' with ⟨a',b',c⟩
        constructor
        · have ha := hsub (show
              (Sum.inl a :
                D0.Topology.GenericTripartiteHomology.GenericVertex p q r) ∈
                Face.vertices (.edge (Sum.inl (a,b)) : Face p q r) by
              simp [Face.vertices, Face.toCoordinates,
                FaceCoordinates.vertices])
          simpa [Face.vertices, Face.toCoordinates,
            FaceCoordinates.vertices] using ha
        · have hb := hsub (show
              (Sum.inr (Sum.inl b) :
                D0.Topology.GenericTripartiteHomology.GenericVertex p q r) ∈
                Face.vertices (.edge (Sum.inl (a,b)) : Face p q r) by
              simp [Face.vertices, Face.toCoordinates,
                FaceCoordinates.vertices])
          simpa [Face.vertices, Face.toCoordinates,
            FaceCoordinates.vertices] using hb
      · rcases rest with ac | bc
        · rcases ac with ⟨a,c⟩
          rcases t' with ⟨a',b,c'⟩
          constructor
          · have ha := hsub (show
                (Sum.inl a :
                  D0.Topology.GenericTripartiteHomology.GenericVertex p q r) ∈
                  Face.vertices
                    (.edge (Sum.inr (Sum.inl (a,c))) : Face p q r) by
                simp [Face.vertices, Face.toCoordinates,
                  FaceCoordinates.vertices])
            simpa [Face.vertices, Face.toCoordinates,
              FaceCoordinates.vertices] using ha
          · have hc := hsub (show
                (Sum.inr (Sum.inr c) :
                  D0.Topology.GenericTripartiteHomology.GenericVertex p q r) ∈
                  Face.vertices
                    (.edge (Sum.inr (Sum.inl (a,c))) : Face p q r) by
                simp [Face.vertices, Face.toCoordinates,
                  FaceCoordinates.vertices])
            simpa [Face.vertices, Face.toCoordinates,
              FaceCoordinates.vertices] using hc
        · rcases bc with ⟨b,c⟩
          rcases t' with ⟨a,b',c'⟩
          constructor
          · have hb := hsub (show
                (Sum.inr (Sum.inl b) :
                  D0.Topology.GenericTripartiteHomology.GenericVertex p q r) ∈
                  Face.vertices
                    (.edge (Sum.inr (Sum.inr (b,c))) : Face p q r) by
                simp [Face.vertices, Face.toCoordinates,
                  FaceCoordinates.vertices])
            simpa [Face.vertices, Face.toCoordinates,
              FaceCoordinates.vertices] using hb
          · have hc := hsub (show
                (Sum.inr (Sum.inr c) :
                  D0.Topology.GenericTripartiteHomology.GenericVertex p q r) ∈
                  Face.vertices
                    (.edge (Sum.inr (Sum.inr (b,c))) : Face p q r) by
                simp [Face.vertices, Face.toCoordinates,
                  FaceCoordinates.vertices])
            simpa [Face.vertices, Face.toCoordinates,
              FaceCoordinates.vertices] using hc
  · rcases upper with v' | e' | t' <;>
      simp [Face.dimension] at hdim

/-- The order on nondegenerate simplices implies inclusion of their actual
vertex supports. -/
lemma simplexVertexFinset_mono {lower upper : NondegenerateFace p q r}
    (hle : lower ≤ upper) :
    simplexVertexFinset lower.simplex.val ⊆
      simplexVertexFinset upper.simplex.val := by
  rw [SSet.N.le_iff_exists_mono] at hle
  obtain ⟨f, _, hf⟩ := hle
  intro v hv
  unfold simplexVertexFinset at hv ⊢
  simp only [Finset.mem_image, Finset.mem_univ, true_and] at hv ⊢
  obtain ⟨i, rfl⟩ := hv
  refine ⟨f i, ?_⟩
  have hobj := congrArg (fun z => z.val.obj i) hf
  change upper.simplex.val.obj (f i) =
    lower.simplex.val.obj i at hobj
  exact congrArg (vertexOrderEquiv p q r).symm hobj

/-- An ordered inclusion of nondegenerate simplices with a dimension jump of
one is the typed codimension-one relation. -/
lemma codimOne_of_le_of_dimension
    {lower upper : NondegenerateFace p q r}
    (hle : lower ≤ upper) (hdim : upper.dim = lower.dim + 1) :
    Face.CodimOne (nondegenerateFaceEquiv lower)
      (nondegenerateFaceEquiv upper) := by
  apply codimOne_of_vertices_subset_of_dimension
  · change Face.vertices (nondegenerateToFace lower) ⊆
      Face.vertices (nondegenerateToFace upper)
    rw [nondegenerateToFace_vertices lower,
        nondegenerateToFace_vertices upper]
    exact simplexVertexFinset_mono hle
  · rw [nondegenerateFaceEquiv_dimension,
        nondegenerateFaceEquiv_dimension]
    exact hdim

/-- Every transported upper pair differs in simplicial dimension by one. -/
theorem pairUpper_dimension {lower upper : NondegenerateFace p q r}
    (h : pairUpper lower = some upper) :
    upper.dim = lower.dim + 1 := by
  rw [pairUpper_eq_some_iff] at h
  have hcodim := Face.pairUpper_codimOne h
  calc
    upper.dim = Face.dimension (nondegenerateFaceEquiv upper) :=
      (nondegenerateFaceEquiv_dimension upper).symm
    _ = Face.dimension (nondegenerateFaceEquiv lower) + 1 :=
      codimOne_dimension hcodim
    _ = lower.dim + 1 := by rw [nondegenerateFaceEquiv_dimension]

/-- Every transported matched pair is an actual codimension-one inclusion of
vertex supports in the simplicial-set carrier. -/
theorem pairUpper_actual_codimOne {lower upper : NondegenerateFace p q r}
    (h : pairUpper lower = some upper) :
    simplexVertexFinset lower.simplex.val ⊆
        simplexVertexFinset upper.simplex.val ∧
      (simplexVertexFinset upper.simplex.val).card =
        (simplexVertexFinset lower.simplex.val).card + 1 := by
  rw [pairUpper_eq_some_iff] at h
  have hactual := Face.pairUpper_actual_codimOne h
  simpa [← nondegenerateToFace_vertices] using hactual


/-- A dimension-one support inclusion between nondegenerate simplices is a
uniquely occurring codimension-one face in Mathlib's simplicial-set API. -/
theorem isUniquelyCodimOneFace_of_support
    {lower upper : NondegenerateFace p q r}
    (hdim : upper.dim = lower.dim + 1)
    (hsupp : simplexVertexFinset lower.simplex.val ⊆
      simplexVertexFinset upper.simplex.val) :
    lower.toS.IsUniquelyCodimOneFace upper.toS := by
  unfold SSet.S.IsUniquelyCodimOneFace
  refine ⟨hdim, ?_⟩
  let sUpper := Finset.image upper.simplex.val.obj Finset.univ
  have hcardUpper : sUpper.card = upper.dim + 1 := by
    unfold sUpper
    rw [Finset.card_image_of_injective _
      (nondegenerate_strictMono upper).injective]
    simp
  have hmemUpper (i : Fin (lower.dim + 1)) :
      lower.simplex.val.obj i ∈ sUpper := by
    have hlow : (vertexOrderEquiv p q r).symm
          (lower.simplex.val.obj i) ∈
        simplexVertexFinset lower.simplex.val := by
      unfold simplexVertexFinset
      simp
    have hup := hsupp hlow
    unfold sUpper
    rw [← orderedSimplexVertexFinset_eq_image upper]
    simpa using Finset.mem_image_of_mem (vertexOrderEquiv p q r) hup
  let upperIso : Fin (upper.dim + 1) ≃o sUpper :=
    Finset.orderIsoOfFin sUpper hcardUpper
  let fFun : Fin (lower.dim + 1) → Fin (upper.dim + 1) :=
    fun i => upperIso.symm ⟨lower.simplex.val.obj i, hmemUpper i⟩
  have hfStrict : StrictMono fFun := by
    intro i j hij
    apply upperIso.symm.strictMono
    exact nondegenerate_strictMono lower hij
  let f := SimplexCategory.mkHom
    ({ toFun := fFun
       monotone' := hfStrict.monotone } :
      Fin (lower.dim + 1) →o Fin (upper.dim + 1))
  have hupperUnique : upper.simplex.val.obj =
      sUpper.orderEmbOfFin hcardUpper := by
    apply Finset.orderEmbOfFin_unique hcardUpper
    · intro i
      unfold sUpper
      exact Finset.mem_image_of_mem _ (Finset.mem_univ i)
    · exact nondegenerate_strictMono upper
  have hfmap :
      (TripartiteSSet p q r).map f.op upper.simplex = lower.simplex := by
    apply Subtype.ext
    apply CategoryTheory.nerve.ext_of_isThin
    funext i
    change upper.simplex.val.obj (fFun i) = lower.simplex.val.obj i
    rw [hupperUnique]
    exact congrArg Subtype.val
      (upperIso.apply_symm_apply
        ⟨lower.simplex.val.obj i, hmemUpper i⟩)
  haveI : CategoryTheory.Mono f := SimplexCategory.mono_iff_injective.2 (by
    change Function.Injective fFun
    exact hfStrict.injective)
  refine ⟨f, ⟨inferInstance, hfmap⟩, ?_⟩
  intro g hg
  apply SimplexCategory.Hom.ext
  apply OrderHom.ext
  funext i
  apply (nondegenerate_strictMono upper).injective
  have hg_i : upper.simplex.val.obj (g i) =
      lower.simplex.val.obj i := by
    have := congrArg (fun z => z.val.obj i) hg.2
    exact this
  have hf_i : upper.simplex.val.obj (f i) =
      lower.simplex.val.obj i := by
    have := congrArg (fun z => z.val.obj i) hfmap
    exact this
  exact hg_i.trans hf_i.symm


/-- Every transported matched pair is a genuine uniquely occurring
codimension-one face in Mathlib's simplicial-set API. -/
theorem pairUpper_isUniquelyCodimOneFace
    {lower upper : NondegenerateFace p q r}
    (h : pairUpper lower = some upper) :
    lower.toS.IsUniquelyCodimOneFace upper.toS :=
  isUniquelyCodimOneFace_of_support
    (pairUpper_dimension h) (pairUpper_actual_codimOne h).1

/-- Upper and lower maps remain inverse after transport. -/
theorem pairUpper_pairLower {lower upper : NondegenerateFace p q r}
    (h : pairUpper lower = some upper) : pairLower upper = some lower := by
  rw [pairUpper_eq_some_iff] at h
  rw [pairLower_eq_some_iff]
  exact Face.pairUpper_pairLower h

/-- Lower and upper maps remain inverse after transport. -/
theorem pairLower_pairUpper {upper lower : NondegenerateFace p q r}
    (h : pairLower upper = some lower) : pairUpper lower = some upper := by
  rw [pairLower_eq_some_iff] at h
  rw [pairUpper_eq_some_iff]
  exact Face.pairLower_pairUpper h

/-- A transported lower pair differs in simplicial dimension by one. -/
theorem pairLower_dimension {upper lower : NondegenerateFace p q r}
    (h : pairLower upper = some lower) :
    upper.dim = lower.dim + 1 :=
  pairUpper_dimension (pairLower_pairUpper h)

/-- Every transported lower pair is the same actual codimension-one support
inclusion as its inverse upper pair. -/
theorem pairLower_actual_codimOne
    {upper lower : NondegenerateFace p q r}
    (h : pairLower upper = some lower) :
    simplexVertexFinset lower.simplex.val ⊆
        simplexVertexFinset upper.simplex.val ∧
      (simplexVertexFinset upper.simplex.val).card =
        (simplexVertexFinset lower.simplex.val).card + 1 :=
  pairUpper_actual_codimOne (pairLower_pairUpper h)

/-- Every transported lower pair is a genuine uniquely occurring
codimension-one face in Mathlib's simplicial-set API. -/
theorem pairLower_isUniquelyCodimOneFace
    {upper lower : NondegenerateFace p q r}
    (h : pairLower upper = some lower) :
    lower.toS.IsUniquelyCodimOneFace upper.toS :=
  pairUpper_isUniquelyCodimOneFace (pairLower_pairUpper h)

/-- No nondegenerate simplex has both matching roles. -/
theorem pair_roles_disjoint (x : NondegenerateFace p q r) :
    ¬ ((pairUpper x).isSome ∧ (pairLower x).isSome) := by
  simpa using Face.pair_roles_disjoint (nondegenerateFaceEquiv x)

/-- Criticality on the actual simplicial-set carrier. -/
def IsCritical (x : NondegenerateFace p q r) : Prop :=
  pairUpper x = none ∧ pairLower x = none

/-- Every actual nondegenerate simplex is critical, a lower matched simplex,
or an upper matched simplex. -/
theorem critical_or_matched (x : NondegenerateFace p q r) :
    IsCritical x ∨ (pairUpper x).isSome ∨ (pairLower x).isSome := by
  cases hu : pairUpper x with
  | none =>
      cases hl : pairLower x with
      | none => exact Or.inl ⟨hu, hl⟩
      | some lower => exact Or.inr (Or.inr (by simp))
  | some upper => exact Or.inr (Or.inl (by simp))

@[simp] theorem isCritical_iff_face (x : NondegenerateFace p q r) :
    IsCritical x ↔ Face.IsCritical (nondegenerateFaceEquiv x) := by
  simp [IsCritical, Face.IsCritical, pairUpper, pairLower]

/-- Critical actual nondegenerate simplices are lacunary: dimensions zero and
two only. -/
theorem critical_dimension_lacunary
    (x : NondegenerateFace p q r) (hx : IsCritical x) :
    x.dim = 0 ∨ x.dim = 2 := by
  have h := Face.critical_dimension_lacunary
    (nondegenerateFaceEquiv x) ((isCritical_iff_face x).1 hx)
  have hdim := nondegenerateFaceEquiv_dimension x
  rcases h with hzero | htwo
  · exact Or.inl (hdim.symm.trans hzero)
  · exact Or.inr (hdim.symm.trans htwo)

/-- Critical nondegenerate simplices in dimension zero. -/
abbrev CriticalZeroSimplex (p q r : ℕ) :=
  {x : NondegenerateFace p q r // IsCritical x ∧ x.dim = 0}

/-- Critical nondegenerate simplices in dimension one. -/
abbrev CriticalOneSimplex (p q r : ℕ) :=
  {x : NondegenerateFace p q r // IsCritical x ∧ x.dim = 1}

/-- Critical nondegenerate simplices in dimension two. -/
abbrev CriticalTwoSimplex (p q r : ℕ) :=
  {x : NondegenerateFace p q r // IsCritical x ∧ x.dim = 2}

private lemma criticalAtDimension_iff_face
    (x : NondegenerateFace p q r) (n : ℕ) :
    (IsCritical x ∧ x.dim = n) ↔
      (Face.IsCritical (nondegenerateFaceEquiv x) ∧
        Face.dimension (nondegenerateFaceEquiv x) = n) := by
  rw [isCritical_iff_face, nondegenerateFaceEquiv_dimension]

/-- Degree-zero critical simplices in the actual `SSet` are exactly the
critical zero-faces of the typed Morse model. -/
noncomputable def criticalZeroSimplexEquiv :
    CriticalZeroSimplex p q r ≃ Face.CriticalZeroFace p q r :=
  Equiv.subtypeEquiv (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r))
    (fun x => criticalAtDimension_iff_face x 0)

/-- Degree-one critical simplices in the actual `SSet` are exactly the empty
critical one-face carrier of the typed Morse model. -/
noncomputable def criticalOneSimplexEquiv :
    CriticalOneSimplex p q r ≃ Face.CriticalOneFace p q r :=
  Equiv.subtypeEquiv (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r))
    (fun x => criticalAtDimension_iff_face x 1)

/-- Degree-two critical simplices in the actual `SSet` are exactly the
critical two-faces of the typed Morse model. -/
noncomputable def criticalTwoSimplexEquiv :
    CriticalTwoSimplex p q r ≃ Face.CriticalTwoFace p q r :=
  Equiv.subtypeEquiv (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r))
    (fun x => criticalAtDimension_iff_face x 2)

lemma criticalOneSimplex_isEmpty :
    IsEmpty (CriticalOneSimplex p q r) := by
  letI : IsEmpty (Face.CriticalOneFace p q r) :=
    Face.criticalOneFace_isEmpty
  exact ⟨fun x => isEmptyElim
    (criticalOneSimplexEquiv (p:=p) (q:=q) (r:=r) x)⟩

noncomputable instance criticalZeroSimplexFintype :
    Fintype (CriticalZeroSimplex p q r) :=
  Fintype.ofEquiv (Face.CriticalZeroFace p q r)
    (criticalZeroSimplexEquiv (p:=p) (q:=q) (r:=r)).symm

noncomputable instance criticalOneSimplexFintype :
    Fintype (CriticalOneSimplex p q r) :=
  Fintype.ofEquiv (Face.CriticalOneFace p q r)
    (criticalOneSimplexEquiv (p:=p) (q:=q) (r:=r)).symm

noncomputable instance criticalTwoSimplexFintype :
    Fintype (CriticalTwoSimplex p q r) :=
  Fintype.ofEquiv (Face.CriticalTwoFace p q r)
    (criticalTwoSimplexEquiv (p:=p) (q:=q) (r:=r)).symm

@[simp] theorem criticalZeroSimplex_card :
    Fintype.card (CriticalZeroSimplex p q r) = 1 := by
  rw [Fintype.card_congr
    (criticalZeroSimplexEquiv (p:=p) (q:=q) (r:=r))]
  exact Face.criticalZeroFace_card

@[simp] theorem criticalOneSimplex_card :
    Fintype.card (CriticalOneSimplex p q r) = 0 := by
  rw [Fintype.card_congr
    (criticalOneSimplexEquiv (p:=p) (q:=q) (r:=r))]
  exact Face.criticalOneFace_card

@[simp] theorem criticalTwoSimplex_card :
    Fintype.card (CriticalTwoSimplex p q r) = p * q * r := by
  rw [Fintype.card_congr
    (criticalTwoSimplexEquiv (p:=p) (q:=q) (r:=r))]
  exact Face.criticalTwoFace_card

/-- The perfect critical vector now holds degreewise on the actual
nondegenerate simplices of the Mathlib realization. -/
@[simp] theorem critical_simplex_card_vector :
    (Fintype.card (CriticalZeroSimplex p q r),
     Fintype.card (CriticalOneSimplex p q r),
     Fintype.card (CriticalTwoSimplex p q r)) =
      (1, 0, p * q * r) := by
  rw [criticalZeroSimplex_card, criticalOneSimplex_card,
      criticalTwoSimplex_card]

/-- The root critical vertex as an actual nondegenerate simplex. -/
noncomputable def rootSimplex : NondegenerateFace p q r :=
  faceNondegenerateEquiv Face.root

@[simp] theorem nondegenerateFaceEquiv_rootSimplex :
    nondegenerateFaceEquiv (rootSimplex (p:=p) (q:=q) (r:=r)) =
      Face.root := by
  exact (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).apply_symm_apply
    Face.root

@[simp] theorem rootSimplex_dim :
    (rootSimplex (p:=p) (q:=q) (r:=r)).dim = 0 := by
  rw [← nondegenerateFaceEquiv_dimension,
      nondegenerateFaceEquiv_rootSimplex]
  rfl

/-- The point subcomplex generated by the root critical simplex. -/
noncomputable def rootSubcomplex : (TripartiteSSet p q r).Subcomplex :=
  (rootSimplex (p:=p) (q:=q) (r:=r)).subcomplex

@[simp] theorem mem_rootSubcomplex_iff (x : NondegenerateFace p q r) :
    x.simplex ∈ (rootSubcomplex (p:=p) (q:=q) (r:=r)).obj _ ↔
      x = rootSimplex := by
  constructor
  · intro hx
    have hleSub : x.subcomplex ≤
        (rootSimplex (p:=p) (q:=q) (r:=r)).subcomplex := by
      rw [SSet.Subcomplex.ofSimplex_le_iff]
      exact hx
    have hle : x ≤ rootSimplex := hleSub
    rcases lt_or_eq_of_le hle with hlt | heq
    · have hdim := SSet.N.dim_lt_of_lt hlt
      rw [rootSimplex_dim] at hdim
      omega
    · exact heq
  · rintro rfl
    exact SSet.Subcomplex.mem_ofSimplex_obj _

lemma topCycleIndex_isEmpty_of_zero
    (hzero : p = 0 ∨ q = 0 ∨ r = 0) :
    IsEmpty (TopCycleIndex p q r) := by
  rcases hzero with rfl | rfl | rfl <;> infer_instance

/-- If one zone has no nonroot vertex, the root is the only critical
nondegenerate simplex. -/
theorem isCritical_iff_eq_root_of_zero
    (hzero : p = 0 ∨ q = 0 ∨ r = 0)
    (x : NondegenerateFace p q r) :
    IsCritical x ↔ x = rootSimplex := by
  letI : IsEmpty (TopCycleIndex p q r) :=
    topCycleIndex_isEmpty_of_zero hzero
  rw [isCritical_iff_face, Face.isCritical_iff]
  constructor
  · rintro (hroot | ⟨i, _⟩)
    · apply (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).injective
      calc
        nondegenerateFaceEquiv x = Face.root := hroot
        _ = nondegenerateFaceEquiv rootSimplex :=
          nondegenerateFaceEquiv_rootSimplex.symm
    · exact isEmptyElim i
  · rintro rfl
    left
    exact nondegenerateFaceEquiv_rootSimplex

/-- In the zero-top-cell cases, the critical carrier is exactly the root
point subcomplex. -/
theorem rootSubcomplex_exactly_critical_of_zero
    (hzero : p = 0 ∨ q = 0 ∨ r = 0)
    (x : NondegenerateFace p q r) :
    x.simplex ∈ (rootSubcomplex (p:=p) (q:=q) (r:=r)).obj _ ↔
      IsCritical x := by
  rw [mem_rootSubcomplex_iff, isCritical_iff_eq_root_of_zero hzero]


/-- For positive offsets, the critical nondegenerate simplices do not form
a simplicial subcomplex. A critical triangle forces its noncritical boundary
edges into any subcomplex containing it. Hence the remaining realization step
cannot be a direct collapse onto a "critical subcomplex"; it requires a genuine
Morse cancellation or CW construction. -/
theorem no_subcomplex_exactly_critical
    (hp : 0 < p) (hq : 0 < q) (hr : 0 < r)
    (A : (TripartiteSSet p q r).Subcomplex)
    (hA : ∀ x : NondegenerateFace p q r,
      x.simplex ∈ A.obj _ ↔ IsCritical x) : False := by
  let i : Fin p := ⟨0, hp⟩
  let j : Fin q := ⟨0, hq⟩
  let k : Fin r := ⟨0, hr⟩
  let criticalFace : Face p q r := Face.criticalTriangle (i, j, k)
  let boundaryEdge : Face p q r := .edge (Sum.inl (i.succ, j.succ))
  let criticalSimplex : NondegenerateFace p q r :=
    faceNondegenerateEquiv criticalFace
  let edgeSimplex : NondegenerateFace p q r :=
    faceNondegenerateEquiv boundaryEdge
  have hcritical : IsCritical criticalSimplex := by
    rw [isCritical_iff_face]
    simpa [criticalSimplex, criticalFace] using
      Face.criticalTriangle_isCritical (i, j, k)
  have hcriticalA : criticalSimplex.simplex ∈ A.obj _ :=
    (hA criticalSimplex).2 hcritical
  have hedgeDim : criticalSimplex.dim = edgeSimplex.dim + 1 := by
    simp [criticalSimplex, edgeSimplex, criticalFace, boundaryEdge,
      Face.criticalTriangle, Face.dimension]
  have hedgeSupp :
      simplexVertexFinset edgeSimplex.simplex.val ⊆
        simplexVertexFinset criticalSimplex.simplex.val := by
    rw [← nondegenerateToFace_vertices edgeSimplex,
        ← nondegenerateToFace_vertices criticalSimplex]
    have hedgeEq : nondegenerateFaceEquiv edgeSimplex = boundaryEdge := by
      exact (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).apply_symm_apply boundaryEdge
    have hcriticalEq : nondegenerateFaceEquiv criticalSimplex = criticalFace := by
      exact (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).apply_symm_apply criticalFace
    have hedgeEq' : nondegenerateToFace edgeSimplex = boundaryEdge := by
      simpa using hedgeEq
    have hcriticalEq' : nondegenerateToFace criticalSimplex = criticalFace := by
      simpa using hcriticalEq
    rw [hedgeEq', hcriticalEq']
    simpa [boundaryEdge, criticalFace, Face.criticalTriangle,
      Face.vertices, Face.toCoordinates, FaceCoordinates.vertices]
  have hedgeFace : edgeSimplex.toS.IsUniquelyCodimOneFace
      criticalSimplex.toS :=
    isUniquelyCodimOneFace_of_support hedgeDim hedgeSupp
  have hcriticalGenerated : criticalSimplex.subcomplex ≤ A := by
    rw [SSet.Subcomplex.ofSimplex_le_iff]
    exact hcriticalA
  have hedgeSubcomplex : edgeSimplex.subcomplex ≤ criticalSimplex.subcomplex := by
    exact hedgeFace.le
  have hedgeGenerated : edgeSimplex.subcomplex ≤ A :=
    hedgeSubcomplex.trans hcriticalGenerated
  have hedgeA : edgeSimplex.simplex ∈ A.obj _ := by
    rw [← SSet.Subcomplex.ofSimplex_le_iff]
    exact hedgeGenerated
  have hedgeCritical : IsCritical edgeSimplex := (hA edgeSimplex).1 hedgeA
  have hedgeTypedCritical : Face.IsCritical boundaryEdge := by
    have h := (isCritical_iff_face edgeSimplex).1 hedgeCritical
    simpa [edgeSimplex] using h
  exact Face.edge_not_isCritical (Sum.inl (i.succ, j.succ)) hedgeTypedCritical

/-- Exact boundary: the critical nondegenerate simplices form a subcomplex if
and only if at least one nonroot-zone size vanishes. -/
theorem exists_subcomplex_exactly_critical_iff :
    (∃ A : (TripartiteSSet p q r).Subcomplex,
      ∀ x : NondegenerateFace p q r,
        x.simplex ∈ A.obj _ ↔ IsCritical x) ↔
      p = 0 ∨ q = 0 ∨ r = 0 := by
  constructor
  · rintro ⟨A, hA⟩
    by_contra hzero
    simp only [not_or] at hzero
    exact no_subcomplex_exactly_critical
      (Nat.pos_of_ne_zero hzero.1)
      (Nat.pos_of_ne_zero hzero.2.1)
      (Nat.pos_of_ne_zero hzero.2.2) A hA
  · intro hzero
    exact ⟨rootSubcomplex,
      rootSubcomplex_exactly_critical_of_zero hzero⟩

/-- Equivalent numeric form: an exact critical subcomplex exists precisely
when the number `p*q*r` of critical top cells vanishes. -/
theorem exists_subcomplex_exactly_critical_iff_topCount_zero :
    (∃ A : (TripartiteSSet p q r).Subcomplex,
      ∀ x : NondegenerateFace p q r,
        x.simplex ∈ A.obj _ ↔ IsCritical x) ↔
      p * q * r = 0 := by
  rw [exists_subcomplex_exactly_critical_iff]
  simp [or_assoc]

/-- Exact classification of critical nondegenerate simplices. -/
theorem isCritical_iff (x : NondegenerateFace p q r) :
    IsCritical x ↔
      nondegenerateFaceEquiv x = Face.root ∨
        ∃ i, nondegenerateFaceEquiv x = Face.criticalTriangle i := by
  rw [isCritical_iff_face, Face.isCritical_iff]

/-- The transported matching has one critical 0-simplex, no critical
1-simplex, and all-nonroot critical 2-simplices. -/
noncomputable def criticalEquiv :
    {x : NondegenerateFace p q r // IsCritical x} ≃
      {f : Face p q r // Face.IsCritical f} :=
  Equiv.subtypeEquiv (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r))
    isCritical_iff_face

noncomputable instance criticalFintype :
    Fintype {x : NondegenerateFace p q r // IsCritical x} :=
  Fintype.ofEquiv {f : Face p q r // Face.IsCritical f}
    (criticalEquiv (p:=p) (q:=q) (r:=r)).symm


@[simp] theorem critical_card :
    Fintype.card {x : NondegenerateFace p q r // IsCritical x} =
      1 + p * q * r := by
  rw [Fintype.card_congr (criticalEquiv (p:=p) (q:=q) (r:=r))]
  exact Face.criticalFace_card

/-- Forman gradient step transported to the actual nondegenerate simplices. -/
noncomputable def GradientStep (lower next : NondegenerateFace p q r) : Prop :=
  Face.GradientStep (nondegenerateFaceEquiv lower)
    (nondegenerateFaceEquiv next)

/-- The inherited finite rank strictly decreases on every transported
`V`-path step. -/
noncomputable def gradientRank (x : NondegenerateFace p q r) : ℕ :=
  Face.gradientRank (nondegenerateFaceEquiv x)

lemma gradientStep_rank_lt {lower next : NondegenerateFace p q r}
    (h : GradientStep lower next) :
    gradientRank next < gradientRank lower :=
  Face.gradientStep_rank_lt h

lemma gradientPath_rank_lt {lower next : NondegenerateFace p q r}
    (h : Relation.TransGen GradientStep lower next) :
    gradientRank next < gradientRank lower := by
  induction h with
  | single h => exact gradientStep_rank_lt h
  | tail _ hstep ih => exact lt_trans (gradientStep_rank_lt hstep) ih

/-- The matching is acyclic on the actual Mathlib simplicial-set carrier. -/
theorem gradient_acyclic (x : NondegenerateFace p q r) :
    ¬ Relation.TransGen GradientStep x x := by
  intro h
  exact (lt_irrefl _ (gradientPath_rank_lt h))

/-- Scene specialization on the actual simplicial-set carrier. -/
theorem scene_critical_card :
    Fintype.card {x : NondegenerateFace 8 10 12 // IsCritical x} = 961 := by
  simpa using critical_card (p:=8) (q:=10) (r:=12)

/-- Scene specialization of the degreewise perfect vector on the actual
simplicial-set carrier. -/
theorem scene_critical_simplex_card_vector :
    (Fintype.card (CriticalZeroSimplex 8 10 12),
     Fintype.card (CriticalOneSimplex 8 10 12),
     Fintype.card (CriticalTwoSimplex 8 10 12)) = (1, 0, 960) := by
  simpa using critical_simplex_card_vector (p:=8) (q:=10) (r:=12)

end D0.Topology.GenericTripartiteSimplicialMorse
