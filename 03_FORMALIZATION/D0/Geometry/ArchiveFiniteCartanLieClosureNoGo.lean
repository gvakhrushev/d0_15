import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Basis.Basic
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.LinearAlgebra.FreeModule.Finite.Matrix
import Mathlib.LinearAlgebra.LinearIndependent.Defs
import Mathlib.Tactic
import D0.Geometry.A4DSymRoleCentralDifference

/-!
# Finite scalar Cartan Lie closure

On a finite set `X`, the matrices `G_xy = E_xy - E_xx` kill constant functions.
Along any simple directed path their nested brackets propagate, and on a
strongly connected relation they span every linear map that kills constants.
The dimension is `n (n - 1)`.

Specializing `X` to the archive `(Z/LZ)^4` with positive role steps gives
dimension `L^4 (L^4 - 1)`. This is the scalar site algebra only.

The same calculation shows there is no lattice-size-independent radius that
contains every nearest-neighbour generator and is closed under the Lie bracket.
Ordinary Leibniz derivations of the pointwise algebra `K^X` are separately zero,
so this Lie closure is not a derivation algebra. The associative crossed product,
proved in `ArchivePathWordAlgebra`, has dimension `n^2` and is a different object.

Nothing here selects a physical Hodge kernel or a constitutive action.
-/

namespace D0.Geometry

open D0

variable {K X : Type*} [Field K] [Fintype X] [DecidableEq X]

/-- Matrix unit `(E_xy f) z = δ_{z x} f(y)`. -/
def matrixUnit (x y : X) : (X → K) →ₗ[K] (X → K) where
  toFun f z := if z = x then f y else 0
  map_add' f g := by
    ext z
    by_cases hz : z = x <;> simp [hz, Pi.add_apply]
  map_smul' c f := by
    ext z
    by_cases hz : z = x <;> simp [hz]

/-- Scalar Cartan generator `G_xy = E_xy - E_xx`. -/
def finiteCartanGenerator (x y : X) : (X → K) →ₗ[K] (X → K) :=
  matrixUnit x y - matrixUnit x x

def lieBracket (A B : (X → K) →ₗ[K] (X → K)) : (X → K) →ₗ[K] (X → K) :=
  A.comp B - B.comp A

theorem matrixUnit_apply (x y : X) (f : X → K) (z : X) :
    matrixUnit x y f z = if z = x then f y else 0 := rfl

theorem edgeGenerator_apply (x y : X) (f : X → K) (z : X) :
    finiteCartanGenerator x y f z =
      (if z = x then f y else 0) - (if z = x then f x else 0) := by
  simp [finiteCartanGenerator, matrixUnit_apply, sub_eq_add_neg]

theorem edgeGenerator_kills_constants (x y : X) :
    finiteCartanGenerator x y (fun _ => (1 : K)) = 0 := by
  ext z
  simp only [edgeGenerator_apply]
  split_ifs <;> simp

theorem matrixUnit_comp (a b c d : X) :
    LinearMap.comp (matrixUnit (K := K) a b) (matrixUnit (K := K) c d) =
      (if b = c then matrixUnit (K := K) a d else 0 : (X → K) →ₗ[K] (X → K)) := by
  refine LinearMap.ext fun g => ?_
  funext z
  simp only [LinearMap.comp_apply, matrixUnit_apply, Pi.zero_apply]
  by_cases hbc : b = c <;> by_cases hz : z = a <;> simp [hbc, hz, matrixUnit_apply]

theorem edgeGenerator_sq (x y : X) (hxy : x ≠ y) :
    LinearMap.comp (finiteCartanGenerator (K := K) x y) (finiteCartanGenerator (K := K) x y) =
      -finiteCartanGenerator (K := K) x y := by
  refine LinearMap.ext fun g => ?_
  funext z
  simp only [LinearMap.comp_apply, LinearMap.neg_apply, edgeGenerator_apply]
  by_cases hz : z = x
  · simp only [hz, Ne.symm hxy, edgeGenerator_apply, ite_true, ite_false,
      LinearMap.neg_apply, Pi.neg_apply]
    abel
  · simp [hz, edgeGenerator_apply]

theorem edgeGenerator_bracket_of_pairwise_ne (i j k : X)
    (hij : i ≠ j) (hjk : j ≠ k) (hik : i ≠ k) :
    lieBracket (finiteCartanGenerator (K := K) i j) (finiteCartanGenerator (K := K) j k) =
      finiteCartanGenerator (K := K) i k - finiteCartanGenerator (K := K) i j := by
  refine LinearMap.ext fun g => ?_
  funext z
  have hji : j ≠ i := Ne.symm hij
  have hki : k ≠ i := Ne.symm hik
  simp only [lieBracket, LinearMap.sub_apply, LinearMap.comp_apply, edgeGenerator_apply]
  by_cases hz : z = i
  · simp only [hz, Pi.sub_apply, edgeGenerator_apply, hij, hji, hki, hjk, ite_true, ite_false]
    abel
  · by_cases hzj : z = j
    · simp only [hz, hzj, Pi.sub_apply, edgeGenerator_apply, hij, hji, hki, hjk,
        ite_true, ite_false]
      abel
    · simp [hz, hzj, Pi.sub_apply, edgeGenerator_apply, hji, hki]

/-- One nested-bracket step: distinct support indices cancel the reverse composition. -/
theorem nested_difference_bracket (s prev curr nxt : X)
    (hsc : s ≠ curr) (hsn : s ≠ nxt) (hpc : prev ≠ curr) (hpn : prev ≠ nxt)
    (hcn : curr ≠ nxt) :
    lieBracket (matrixUnit (K := K) s curr - matrixUnit (K := K) s prev)
        (finiteCartanGenerator (K := K) curr nxt) =
      matrixUnit (K := K) s nxt - matrixUnit (K := K) s curr := by
  refine LinearMap.ext fun g => ?_
  funext z
  simp only [lieBracket, LinearMap.sub_apply, LinearMap.comp_apply]
  by_cases hz : z = s
  · simp only [hz, Pi.sub_apply, matrixUnit_apply, edgeGenerator_apply, hsc, hsn, hpc, hpn, hcn,
      Ne.symm hsc, Ne.symm hsn, Ne.symm hpc, Ne.symm hpn, Ne.symm hcn, ite_true, ite_false]
    abel
  · simp [hz, Ne.symm hsc, Ne.symm hsn, Ne.symm hpc, Ne.symm hpn, Ne.symm hcn,
      Pi.sub_apply, matrixUnit_apply, edgeGenerator_apply]

def nestedGo (c : (X → K) →ₗ[K] (X → K)) (curr : X) : List X → (X → K) →ₗ[K] (X → K)
  | [] => c
  | nxt :: rest => nestedGo (lieBracket c (finiteCartanGenerator curr nxt)) nxt rest

/-- Nested bracket along `x₀, x₁, …`. The empty and singleton lists contribute zero. -/
def nestedBracket : List X → (X → K) →ₗ[K] (X → K)
  | x :: y :: rest => nestedGo (finiteCartanGenerator x y) y rest
  | _ => 0

def listLast (curr : X) : List X → X
  | [] => curr
  | nxt :: rest => listLast nxt rest

def secondLast (prev curr : X) : List X → X
  | [] => prev
  | nxt :: rest => secondLast curr nxt rest

theorem nestedGo_eq (s prev curr : X) (rest : List X)
    (hout : prev ∉ curr :: rest) (hn : (s :: curr :: rest).Nodup) :
    nestedGo (matrixUnit (K := K) s curr - matrixUnit (K := K) s prev) curr rest =
      matrixUnit s (listLast curr rest) - matrixUnit s (secondLast prev curr rest) := by
  induction rest generalizing prev curr with
  | nil =>
      simp [nestedGo, listLast, secondLast]
  | cons nxt rest ih =>
      have hnotin : s ∉ curr :: nxt :: rest := (List.nodup_cons.mp hn).1
      have htail : (curr :: nxt :: rest).Nodup := (List.nodup_cons.mp hn).2
      have hsc : s ≠ curr := by
        intro h
        exact hnotin (List.mem_cons.mpr (Or.inl h))
      have hsn : s ≠ nxt := by
        intro h
        exact hnotin (List.mem_cons_of_mem curr (List.mem_cons.mpr (Or.inl h)))
      have hcn : curr ≠ nxt := by
        intro h
        exact (List.nodup_cons.mp htail).1 (List.mem_cons.mpr (Or.inl h))
      have hpc : prev ≠ curr := by
        intro h
        exact hout (List.mem_cons.mpr (Or.inl h))
      have hpn : prev ≠ nxt := by
        intro h
        exact hout (List.mem_cons_of_mem curr (List.mem_cons.mpr (Or.inl h)))
      have hstep :=
        nested_difference_bracket (K := K) s prev curr nxt hsc hsn hpc hpn hcn
      simp only [nestedGo, hstep]
      have hout' : curr ∉ nxt :: rest := (List.nodup_cons.mp htail).1
      have hn' : (s :: nxt :: rest).Nodup := by
        rw [List.nodup_cons]
        constructor
        · intro hz
          exact (List.nodup_cons.mp hn).1 (List.mem_cons_of_mem curr hz)
        · exact (List.nodup_cons.mp htail).2
      rw [ih curr nxt hout' hn']
      simp [listLast, secondLast]

/-- On a simple path `x₀,…,xₘ`, the nested bracket is `E_{x₀ xₘ} - E_{x₀ x_{m-1}}`. -/
theorem nestedBracket_simplePath {p : List X}
    (hn : p.Nodup) (hlen : 2 ≤ p.length) :
    nestedBracket p =
      matrixUnit (K := K) p[0] (listLast p[1] (p.drop 2)) -
        matrixUnit (K := K) p[0] (secondLast p[0] p[1] (p.drop 2)) := by
  match p with
  | [] => simp at hlen
  | [a] => simp at hlen
  | x :: y :: rest =>
      have hnodup : (x :: y :: rest).Nodup := hn
      have hout : x ∉ y :: rest := (List.nodup_cons.mp hnodup).1
      simpa [nestedBracket, finiteCartanGenerator, listLast, secondLast] using
        nestedGo_eq x x y rest hout hnodup

theorem edgeGenerator_ne_zero (x y : X) (hxy : x ≠ y) :
    finiteCartanGenerator (K := K) x y ≠ 0 := by
  intro h0
  have hcoe := congrArg (fun f : (X → K) →ₗ[K] (X → K) => f (Pi.single y (1 : K)) x) h0
  simp [edgeGenerator_apply, Pi.single_apply, hxy] at hcoe

/-! ## Lie membership -/

/-- The Lie span of a set of endomorphisms: zero, the generators, and the
linear and bracket operations. -/
inductive InLie (gen : ((X → K) →ₗ[K] (X → K)) → Prop) :
    ((X → K) →ₗ[K] (X → K)) → Prop
  | zero : InLie gen 0
  | gen {A} : gen A → InLie gen A
  | add {A B} : InLie gen A → InLie gen B → InLie gen (A + B)
  | smul {c : K} {A} : InLie gen A → InLie gen (c • A)
  | brak {A B} : InLie gen A → InLie gen B → InLie gen (lieBracket A B)

def edgeGen (E : X → X → Prop) (A : (X → K) →ₗ[K] (X → K)) : Prop :=
  ∃ x y, E x y ∧ A = finiteCartanGenerator x y

theorem inLie_kills_constants {gen : ((X → K) →ₗ[K] (X → K)) → Prop}
    (hgen : ∀ A, gen A → A (fun _ => (1 : K)) = 0)
    {A : (X → K) →ₗ[K] (X → K)} (hA : InLie gen A) :
    A (fun _ => (1 : K)) = 0 := by
  induction hA with
  | zero => simp
  | gen h => exact hgen _ h
  | add _ _ ihA ihB => simp [ihA, ihB]
  | smul _ ih => simp [ih]
  | brak _ _ ihA ihB => simp [lieBracket, LinearMap.comp_apply, ihA, ihB]

theorem inLie_sum {ι : Type*} {gen : ((X → K) →ₗ[K] (X → K)) → Prop}
    {s : Finset ι} {c : ι → K} {v : ι → (X → K) →ₗ[K] (X → K)}
    (hv : ∀ i ∈ s, InLie gen (v i)) :
    InLie gen (∑ i ∈ s, c i • v i) := by
  classical
  induction s using Finset.induction with
  | empty => simp [InLie.zero]
  | insert a s ha ih =>
      rw [Finset.sum_insert ha]
      exact InLie.add (InLie.smul (hv a (Finset.mem_insert_self _ _)))
        (ih fun i hi => hv i (Finset.mem_insert_of_mem hi))

theorem inLie_sum_univ {ι : Type*} [Fintype ι] {gen : ((X → K) →ₗ[K] (X → K)) → Prop}
    {c : ι → K} {v : ι → (X → K) →ₗ[K] (X → K)}
    (hv : ∀ i, InLie gen (v i)) :
    InLie gen (∑ i, c i • v i) :=
  inLie_sum (s := Finset.univ) fun i _ => hv i

theorem edgeGen_kills (E : X → X → Prop) (A : (X → K) →ₗ[K] (X → K))
    (hA : edgeGen E A) : A (fun _ => (1 : K)) = 0 := by
  rcases hA with ⟨x, y, _, rfl⟩
  exact edgeGenerator_kills_constants x y

/-- Generators of the successive edges, then brackets, stay in the Lie span. -/
theorem nestedGo_mem (E : X → X → Prop)
    {c curr : X} {rest : List X} {start : (X → K) →ₗ[K] (X → K)}
    (hstart : InLie (edgeGen E) start)
    (hchain : List.IsChain E (curr :: rest))
    (hfirst : E c curr) :
    InLie (edgeGen E) (nestedGo start curr rest) := by
  induction rest generalizing c curr start with
  | nil => simpa [nestedGo] using hstart
  | cons nxt rest ih =>
      have hcur : E curr nxt := List.IsChain.rel_head hchain
      have htail : List.IsChain E (nxt :: rest) := hchain.tail
      have hbrak : InLie (edgeGen E)
          (lieBracket start (finiteCartanGenerator curr nxt)) :=
        InLie.brak hstart (InLie.gen ⟨curr, nxt, hcur, rfl⟩)
      simpa [nestedGo] using ih (c := curr) (curr := nxt) hbrak htail hcur

theorem nestedBracket_mem (E : X → X → Prop) {p : List X}
    (hlen : 2 ≤ p.length) (hchain : p.IsChain E) :
    InLie (edgeGen E : ((X → K) →ₗ[K] (X → K)) → Prop) (nestedBracket p) := by
  match p with
  | [] => simp at hlen
  | [a] => simp at hlen
  | x :: y :: rest =>
      have hxy : E x y := List.IsChain.rel_head hchain
      have htail : List.IsChain E (y :: rest) := hchain.tail
      simpa [nestedBracket] using
        nestedGo_mem E (InLie.gen ⟨x, y, hxy, rfl⟩) htail hxy

theorem listLast_mem (curr : X) (rest : List X) :
    listLast curr rest ∈ curr :: rest := by
  induction rest generalizing curr with
  | nil => simp [listLast]
  | cons nxt rest ih =>
      exact List.mem_cons_of_mem curr (ih nxt)

theorem secondLast_mem (prev curr : X) (rest : List X) :
    secondLast prev curr rest ∈ prev :: curr :: rest := by
  induction rest generalizing prev curr with
  | nil => simp [secondLast]
  | cons nxt rest ih =>
      exact List.mem_cons_of_mem prev (ih curr nxt)

theorem getLast_eq_listLast (x y : X) (ys : List X) (hys : ys ≠ []) :
    (x :: y :: ys).getLast (by simp) = listLast y ys := by
  induction ys generalizing y with
  | nil => exact (hys rfl).elim
  | cons z zs ih =>
      cases zs with
      | nil => simp [listLast, List.getLast]
      | cons w ws =>
          simp [listLast, List.getLast]
          exact ih z (by simp)

theorem listLast_append_singleton (curr a : X) (ys : List X) :
    listLast curr (ys ++ [a]) = a := by
  induction ys generalizing curr with
  | nil => simp [listLast]
  | cons z zs ih =>
      simp [listLast]
      exact ih z

theorem edgeGenerator_mem_of_simple_path (E : X → X → Prop) {p : List X}
    (hn : p.Nodup) (hchain : p.IsChain E) (hlen : 2 ≤ p.length) :
    InLie (edgeGen E : ((X → K) →ₗ[K] (X → K)) → Prop)
      (finiteCartanGenerator (K := K) p[0] (listLast p[1] (p.drop 2))) := by
  match p with
  | [] => simp at hlen
  | [a] => simp at hlen
  | x :: y :: rest =>
      have hnodup : (x :: y :: rest).Nodup := hn
      have hchain' : List.IsChain E (x :: y :: rest) := hchain
      induction rest using List.reverseRecOn generalizing x y with
      | nil =>
          have hxy : E x y := List.IsChain.rel_head hchain'
          simpa [listLast] using
            (InLie.gen ⟨x, y, hxy, rfl⟩ :
              InLie (edgeGen E : ((X → K) →ₗ[K] (X → K)) → Prop)
                (finiteCartanGenerator (K := K) x y))
      | append_singleton ys a ih =>
          have happ : listLast y (ys ++ [a]) = a := listLast_append_singleton y a ys
          have hpref_chain : List.IsChain E (x :: y :: ys) := by
            have hsplit := List.isChain_append.mp
              (show List.IsChain E ((x :: y :: ys) ++ [a]) from by simpa using hchain')
            simpa using hsplit.1
          have hpref_nodup : (x :: y :: ys).Nodup := by
            have hsub : x :: y :: ys <+: x :: y :: (ys ++ [a]) := by
              simpa using (List.dropLast_prefix (x :: y :: (ys ++ [a])))
            exact hnodup.sublist hsub.sublist
          by_cases hys : ys = []
          · subst hys
            have hxy : E x y := List.IsChain.rel_head hchain'
            have hya : E y a := by
              have hsplit := List.isChain_append.mp
                (show List.IsChain E ((x :: [y]) ++ [a]) from hchain')
              exact hsplit.2.2 y (by simp) a (by simp)
            have hxy_ne : x ≠ y := by
              intro h
              exact (List.nodup_cons.mp hnodup).1 (List.mem_cons.mpr (Or.inl h))
            have hya_ne : y ≠ a := by
              intro h
              exact (List.nodup_cons.mp (List.nodup_cons.mp hnodup).2).1
                (List.mem_cons.mpr (Or.inl h))
            have hxa_ne : x ≠ a := by
              intro h
              exact (List.nodup_cons.mp hnodup).1
                (List.mem_cons_of_mem y (List.mem_cons.mpr (Or.inl h)))
            have hbr := edgeGenerator_bracket_of_pairwise_ne (K := K) x y a hxy_ne hya_ne hxa_ne
            have hGxy : InLie (edgeGen E : ((X → K) →ₗ[K] (X → K)) → Prop)
                (finiteCartanGenerator (K := K) x y) :=
              InLie.gen ⟨x, y, hxy, rfl⟩
            have hGya : InLie (edgeGen E : ((X → K) →ₗ[K] (X → K)) → Prop)
                (finiteCartanGenerator (K := K) y a) :=
              InLie.gen ⟨y, a, hya, rfl⟩
            have hsum : finiteCartanGenerator (K := K) x a =
                lieBracket (finiteCartanGenerator (K := K) x y) (finiteCartanGenerator (K := K) y a) +
                  finiteCartanGenerator (K := K) x y := by
              rw [hbr]
              abel
            simp [listLast, List.drop]
            rw [hsum]
            exact InLie.add (InLie.brak hGxy hGya) hGxy
          · have hlen_pref : 2 ≤ (x :: y :: ys).length := by
              cases ys with
              | nil => exact (hys rfl).elim
              | cons _ _ => simp
            have hIH : InLie (edgeGen E : ((X → K) →ₗ[K] (X → K)) → Prop)
                (finiteCartanGenerator (K := K) x (listLast y ys)) := by
              have hxy_ne : x ≠ y := by
                intro h
                exact (List.nodup_cons.mp hpref_nodup).1 (List.mem_cons.mpr (Or.inl h))
              have hx_ys : x ∉ ys := by
                intro h
                exact (List.nodup_cons.mp hpref_nodup).1 (List.mem_cons_of_mem y h)
              have hy_ys : y ∉ ys :=
                (List.nodup_cons.mp (List.nodup_cons.mp hpref_nodup).2).1
              have hys_nd : ys.Nodup :=
                (List.nodup_cons.mp (List.nodup_cons.mp hpref_nodup).2).2
              have hxyE : E x y := List.IsChain.rel_head hpref_chain
              have htailc : List.IsChain E (y :: ys) := hpref_chain.tail
              simpa [List.drop, listLast] using
                ih x y hpref_nodup hpref_chain hlen_pref hpref_nodup hpref_chain
            have hx_prev : x ≠ listLast y ys := by
              intro hEq
              have hmem := listLast_mem y ys
              rw [← hEq] at hmem
              exact (List.nodup_cons.mp hpref_nodup).1 hmem
            have hv : listLast y ys ≠ a := by
              intro hEq
              have hmem : a ∈ x :: y :: ys :=
                List.mem_cons_of_mem x (by
                  have h := listLast_mem y ys
                  rw [hEq] at h
                  exact h)
              have hnd : ((x :: y :: ys) ++ [a]).Nodup := hnodup
              have hrev : (List.reverse ((x :: y :: ys) ++ [a])).Nodup :=
                List.nodup_reverse.mpr hnd
              rw [List.reverse_append, List.reverse_singleton, List.singleton_append] at hrev
              exact (List.nodup_cons.mp hrev).1 (List.mem_reverse.mpr hmem)
            have hxa : x ≠ a := by
              intro hEq
              have hnd : (a :: y :: (ys ++ [a])).Nodup := by simpa [hEq] using hnodup
              exact (List.nodup_cons.mp hnd).1
                (List.mem_cons_of_mem y (List.mem_append_right ys (List.mem_singleton_self a)))
            have hprev_edge : E (listLast y ys) a := by
              have hsplit := List.isChain_append.mp
                (show List.IsChain E ((x :: y :: ys) ++ [a]) from by simpa using hchain')
              have hsome : (x :: y :: ys).getLast? = some (listLast y ys) := by
                rw [List.getLast?_eq_some_getLast (by simp), getLast_eq_listLast x y ys hys]
              exact hsplit.2.2 _ hsome a (by simp)
            have hbr := edgeGenerator_bracket_of_pairwise_ne (K := K) x (listLast y ys) a
              hx_prev hv hxa
            have hGedge : InLie (edgeGen E : ((X → K) →ₗ[K] (X → K)) → Prop)
                (finiteCartanGenerator (K := K) (listLast y ys) a) :=
              InLie.gen ⟨listLast y ys, a, hprev_edge, rfl⟩
            have hsum : finiteCartanGenerator (K := K) x a =
                lieBracket (finiteCartanGenerator (K := K) x (listLast y ys))
                    (finiteCartanGenerator (K := K) (listLast y ys) a) +
                  finiteCartanGenerator (K := K) x (listLast y ys) := by
              rw [hbr]
              abel
            simp [listLast, List.drop, happ]
            rw [hsum]
            exact InLie.add (InLie.brak hIH hGedge) hIH

theorem exists_duplicate_of_not_nodup {p : List X} (h : ¬ p.Nodup) :
    ∃ i j : Fin p.length, i < j ∧ p.get i = p.get j := by
  classical
  rw [List.Nodup, List.pairwise_iff_get] at h
  push_neg at h
  obtain ⟨i, j, hij, heq⟩ := h
  exact ⟨i, j, hij, by simpa using heq⟩

theorem listLast_eq_getLast_of_length {p : List X} (hlen : 2 ≤ p.length) :
    listLast p[1] (p.drop 2) = p.getLast (List.ne_nil_of_length_pos (by omega)) := by
  match p with
  | [] => simp at hlen
  | [a] => simp at hlen
  | x :: y :: rest =>
      cases rest with
      | nil => simp [listLast, List.getLast]
      | cons z zs =>
          simpa [listLast] using (getLast_eq_listLast x y (z :: zs) (by simp)).symm

theorem secondLast_ne_listLast_aux :
    ∀ (x y : X) (rest : List X), (x :: y :: rest).Nodup →
      secondLast x y rest ≠ listLast y rest := by
  intro x y rest
  induction rest generalizing x y with
  | nil =>
      intro hn h
      exact (List.nodup_cons.mp hn).1 (List.mem_cons.mpr (Or.inl h))
  | cons nxt rest ih =>
      intro hn
      have htail : (y :: nxt :: rest).Nodup := (List.nodup_cons.mp hn).2
      simpa [secondLast, listLast] using ih y nxt htail

theorem secondLast_ne_listLast {p : List X} (hn : p.Nodup) (hlen : 2 ≤ p.length) :
    secondLast p[0] p[1] (p.drop 2) ≠ listLast p[1] (p.drop 2) := by
  match p with
  | [] => simp at hlen
  | [a] => simp at hlen
  | x :: y :: rest =>
      simpa using secondLast_ne_listLast_aux x y rest hn

theorem shorter_walk_of_not_nodup {E : X → X → Prop} {p : List X}
    (hchain : p.IsChain E) (hnot : ¬ p.Nodup) :
    ∃ q : List X, q.length < p.length ∧ q ≠ [] ∧ q.head? = p.head? ∧
      q.getLast? = p.getLast? ∧ q.IsChain E := by
  classical
  obtain ⟨i, j, hij, heq⟩ := exists_duplicate_of_not_nodup hnot
  have hi : i.1 + 1 ≤ p.length := Nat.succ_le_of_lt i.2
  have hj : j.1 + 1 ≤ p.length := Nat.succ_le_of_lt j.2
  let q := p.take (i.1 + 1) ++ p.drop (j.1 + 1)
  have htake_ne : p.take (i.1 + 1) ≠ [] :=
    List.ne_nil_of_length_pos (by
      rw [List.length_take, min_eq_left hi]
      exact Nat.succ_pos i.1)
  refine ⟨q, ?_, ?_, ?_, ?_, ?_⟩
  · have hlen : q.length = i.1 + 1 + (p.length - (j.1 + 1)) := by
      simp only [q, List.length_append, List.length_take, List.length_drop, hi, hj, min_eq_left]
    have hlt : i.1 + 1 + (p.length - (j.1 + 1)) < p.length := by
      have hij' : i.1 + 1 ≤ j.1 := Nat.succ_le_of_lt hij
      have hsub : j.1 + (p.length - (j.1 + 1)) = p.length - 1 := by omega
      have hle : i.1 + 1 + (p.length - (j.1 + 1)) ≤
          j.1 + (p.length - (j.1 + 1)) := by omega
      omega
    simp [hlen, hlt]
  · intro hq
    exact htake_ne (List.append_eq_nil_iff.mp hq).1
  · have hpne : p ≠ [] :=
      List.ne_nil_of_length_pos (Nat.lt_of_le_of_lt (Nat.zero_le i.1) i.2)
    simp only [q, List.head?_append, List.head?_take]
    rw [if_neg (Nat.succ_ne_zero i.1), List.head?_eq_some_head hpne]
    simp
  · by_cases hdrop : p.drop (j.1 + 1) = []
    · have hjlast : j.1 + 1 = p.length := by
        have hjle : p.length ≤ j.1 + 1 := List.drop_eq_nil_iff.mp hdrop
        omega
      have htake_last : (p.take (i.1 + 1)).getLast? = some (p.get j) := by
        rw [List.getLast?_take, if_neg (Nat.succ_ne_zero i.1)]
        have hsub : (i.1 + 1) - 1 = i.1 := by omega
        have hpi : p[i.1]? = some (p.get j) := by
          rw [← List.getElem_eq_iff i.2]
          simpa [List.get_eq_getElem] using heq
        rw [hsub, hpi, Option.some_or]
      simp only [q, hdrop, List.getLast?_append, List.getLast?_nil, Option.none_or, htake_last]
      rw [List.getLast?_eq_getElem?]
      have hidx : p.length - 1 = j.1 := by omega
      rw [hidx, eq_comm, ← List.getElem_eq_iff j.2]
      simp [List.get_eq_getElem]
    · have hlastq : q.getLast? = (p.drop (j.1 + 1)).getLast? := by
        simp only [q, List.getLast?_append]
        rw [List.getLast?_eq_some_getLast hdrop]
        simp
      rw [hlastq, List.getLast?_drop, if_neg]
      exact mt List.drop_eq_nil_of_le hdrop
  · apply List.IsChain.append (hchain.take _) (hchain.drop _)
    intro a ha b hb
    have hdrop_ne : p.drop (j.1 + 1) ≠ [] := by
      intro hempty
      simp [List.head?_eq_none_iff, hempty] at hb
    have ha' : (p.take (i.1 + 1)).getLast htake_ne = a := by
      simpa [List.getLast?_eq_some_getLast htake_ne] using ha
    have hlt : j.1 + 1 < p.length := by
      have hpos : 0 < (p.drop (j.1 + 1)).length := List.length_pos_iff.mpr hdrop_ne
      rw [List.length_drop] at hpos
      omega
    have hb' : p[j.1 + 1] = b := by
      simpa [List.head?_eq_some_head hdrop_ne, List.head_drop] using hb
    have hgl : (p.take (i.1 + 1)).getLast htake_ne = p.get i := by
      rw [List.getLast_take]
      have hsub : (i.1 + 1) - 1 = i.1 := by omega
      have hsome : p[(i.1 + 1) - 1]? = some (p.get i) := by
        rw [hsub, ← List.getElem_eq_iff i.2]
        simp [List.get_eq_getElem]
      rw [hsome, Option.getD_some]
    rw [← ha', ← hb', hgl]
    have hrel := hchain.getElem j.1 hlt
    rw [← List.get_eq_getElem] at hrel
    rw [heq.symm] at hrel
    exact hrel

/-- A directed walk from `a` to `b`. The one-point list is a walk from a site to itself. -/
def Reachable (E : X → X → Prop) (a b : X) : Prop :=
  ∃ p : List X, p ≠ [] ∧ p.head? = some a ∧ p.getLast? = some b ∧ p.IsChain E

/-- A walk with no repeated vertex. Length at least 2 keeps the endpoints apart. -/
def IsSimplePath (E : X → X → Prop) (p : List X) (a b : X) : Prop :=
  2 ≤ p.length ∧ p ≠ [] ∧ p.head? = some a ∧ p.getLast? = some b ∧
    p.IsChain E ∧ p.Nodup

/-- Every ordered pair of sites, including a site with itself, is joined by a directed walk. -/
def StronglyConnected (E : X → X → Prop) : Prop :=
  ∀ x y : X, Reachable E x y

theorem reachable_exists_simple {E : X → X → Prop} {a b : X}
    (hreach : Reachable E a b) (hne : a ≠ b) :
    ∃ p : List X, IsSimplePath E p a b := by
  classical
  rcases hreach with ⟨p0, hp0_ne, hp0_head, hp0_last, hp0_chain⟩
  suffices ∀ n, ∀ p : List X, p.length ≤ n → p ≠ [] → p.head? = some a →
      p.getLast? = some b → p.IsChain E → ∃ q, IsSimplePath E q a b by
    exact this p0.length p0 le_rfl hp0_ne hp0_head hp0_last hp0_chain
  intro n
  induction n with
  | zero =>
      intro p hp hne' _ _ _
      exact absurd (List.length_eq_zero_iff.mp (Nat.le_zero.mp hp)) hne'
  | succ n ih =>
      intro p hp hne' hhead hlast hchain
      by_cases hnodup : p.Nodup
      · have hlen2 : 2 ≤ p.length := by
          cases p with
          | nil => exact absurd rfl hne'
          | cons _ t =>
              cases t with
              | nil =>
                  simp at hhead hlast
                  exact absurd (hhead.symm.trans hlast) hne
              | cons _ _ => simp
        exact ⟨p, hlen2, hne', hhead, hlast, hchain, hnodup⟩
      · obtain ⟨q, hqlen, hqne, hqhead, hqlast, hqchain⟩ :=
          shorter_walk_of_not_nodup hchain hnodup
        exact ih q (by omega) hqne (hqhead.trans hhead) (hqlast.trans hlast) hqchain

theorem edgeGenerator_mem_of_connected (E : X → X → Prop)
    (hE : StronglyConnected E) {x y : X} (hxy : x ≠ y) :
    InLie (edgeGen E : ((X → K) →ₗ[K] (X → K)) → Prop)
      (finiteCartanGenerator (K := K) x y) := by
  obtain ⟨p, hlen, hpne, hhead, hlast, hchain, hnodup⟩ :=
    reachable_exists_simple (hE x y) hxy
  have hG := edgeGenerator_mem_of_simple_path (K := K) E hnodup hchain hlen
  have hx : p[0] = x := by
    cases p with
    | nil => simp at hpne
    | cons _ _ =>
        simp at hhead
        exact hhead
  have hy : listLast p[1] (p.drop 2) = y := by
    have hget := listLast_eq_getLast_of_length (p := p) hlen
    have hylast : p.getLast hpne = y := by
      apply Option.some_injective
      simpa [List.getLast?_eq_some_getLast hpne] using hlast
    simpa [hget, hylast]
  simpa [hx, hy] using hG

/-! ## Basis of the constant annihilator -/

def evalConst : ((X → K) →ₗ[K] (X → K)) →ₗ[K] (X → K) where
  toFun A := A (fun _ => 1)
  map_add' A B := by ext; simp
  map_smul' c A := by ext; simp

abbrev OffDiag (X : Type*) [DecidableEq X] := {p : X × X // p.1 ≠ p.2}

def offDiagSigma : OffDiag X ≃ Σ i : X, {j : X // j ≠ i} where
  toFun p := ⟨p.1.1, ⟨p.1.2, Ne.symm p.2⟩⟩
  invFun s := ⟨(s.1, s.2.1), Ne.symm s.2.2⟩
  left_inv p := by
    cases p
    apply Subtype.ext
    rfl
  right_inv s := by
    cases s
    rfl

theorem sum_single_eq_one : (∑ j : X, Pi.single j (1 : K)) = fun _ => 1 := by
  ext z
  simp [Finset.sum_apply, Pi.single_apply, Finset.sum_ite_eq']

theorem row_sum_of_kills (A : (X → K) →ₗ[K] (X → K))
    (hA : A (fun _ => (1 : K)) = 0) (i : X) :
    ∑ j : X, A (Pi.single j (1 : K)) i = 0 := by
  have hlin : A (∑ j : X, Pi.single j (1 : K)) i = ∑ j : X, A (Pi.single j (1 : K)) i := by
    simp [map_sum, Finset.sum_apply]
  rw [sum_single_eq_one, hA] at hlin
  simpa using hlin.symm

theorem offDiagonal_combination_eq (c : OffDiag X → K) (k pnt : X) :
    (∑ p : OffDiag X, c p • finiteCartanGenerator p.1.1 p.1.2) (Pi.single k (1 : K)) pnt =
      ∑ p : OffDiag X, c p * finiteCartanGenerator p.1.1 p.1.2 (Pi.single k (1 : K)) pnt := by
  simp [LinearMap.sum_apply, LinearMap.smul_apply, Pi.smul_apply, smul_eq_mul]

theorem coeff_extract (c : OffDiag X → K) {a b : X} (hab : a ≠ b)
    (h : (∑ p : OffDiag X, c p • finiteCartanGenerator (K := K) p.1.1 p.1.2) = (0 : (X → K) →ₗ[K] (X → K))) :
    c ⟨(a, b), hab⟩ = (0 : K) := by
  classical
  let p₀ : OffDiag X := ⟨(a, b), hab⟩
  let f : OffDiag X → K := fun p =>
    c p * finiteCartanGenerator (K := K) p.1.1 p.1.2 (Pi.single b (1 : K)) a
  have hpoint : (∑ p : OffDiag X, c p • finiteCartanGenerator (K := K) p.1.1 p.1.2)
      (Pi.single b (1 : K)) a = 0 := by
    simpa using congrFun
      (congrArg (fun A : (X → K) →ₗ[K] (X → K) => A (Pi.single b (1 : K))) h) a
  rw [offDiagonal_combination_eq] at hpoint
  have hsum : (∑ p : OffDiag X, f p) = f p₀ := by
    refine Fintype.sum_eq_single p₀ ?_
    intro p hp
    by_cases hia : p.1.1 = a
    · by_cases hjb : p.1.2 = b
      · exact (hp (Subtype.ext (Prod.ext hia hjb))).elim
      · have hg : finiteCartanGenerator (K := K) p.1.1 p.1.2 (Pi.single b (1 : K)) a = 0 := by
          rw [edgeGenerator_apply, hia]
          simp [hjb, hab]
        simp [f, hg, mul_zero]
    · have hg : finiteCartanGenerator (K := K) p.1.1 p.1.2 (Pi.single b (1 : K)) a = 0 := by
        rw [edgeGenerator_apply]
        simp [Ne.symm hia]
      simp [f, hg, mul_zero]
  have hsum_eval : f p₀ = c p₀ := by
    simp [f, p₀, edgeGenerator_apply, hab, mul_one, sub_self]
  rw [hsum, hsum_eval] at hpoint
  exact hpoint

theorem linearIndependent_edgeGenerator :
    LinearIndependent K (fun p : OffDiag X => finiteCartanGenerator (K := K) p.1.1 p.1.2) := by
  rw [Fintype.linearIndependent_iff]
  intro c hsum p
  exact coeff_extract c p.2 hsum

theorem row_complement (A : (X → K) →ₗ[K] (X → K))
    (hA : A (fun _ => (1 : K)) = 0) (pnt : X) :
    ∑ j : {j : X // j ≠ pnt}, A (Pi.single j.1 (1 : K)) pnt =
      -A (Pi.single pnt (1 : K)) pnt := by
  have hsum := row_sum_of_kills A hA pnt
  let f : X → K := fun j => A (Pi.single j (1 : K)) pnt
  have hsplit := Fintype.sum_subtype_add_sum_subtype (fun j : X => j ≠ pnt) f
  have hsing : (∑ j : {j : X // ¬ j ≠ pnt}, f j) = f pnt := by
    have hp : ¬ pnt ≠ pnt := fun hne => hne rfl
    refine Fintype.sum_eq_single (⟨pnt, hp⟩ : {j : X // ¬ j ≠ pnt}) ?_
    intro j hj
    have hj' : j.1 = pnt := by simpa using j.2
    exact (hj (Subtype.ext hj')).elim
  have hzero : (∑ j : {j : X // j ≠ pnt}, f j) + f pnt = 0 := by
    simpa [f, hsum, hsing] using hsplit
  simpa [f] using eq_neg_of_add_eq_zero_left hzero

theorem diagonal_generator_at_row (A : (X → K) →ₗ[K] (X → K)) (pnt : X) :
    ∑ j : {j : X // j ≠ pnt}, (A (Pi.single j.1 (1 : K)) pnt) *
        finiteCartanGenerator pnt j.1 (Pi.single pnt (1 : K)) pnt =
      ∑ j : {j : X // j ≠ pnt}, -A (Pi.single j.1 (1 : K)) pnt := by
  refine Finset.sum_congr rfl ?_
  intro j _
  have hj : j.1 ≠ pnt := j.2
  simp only [edgeGenerator_apply, Pi.single_apply, ite_true, ite_false, hj, smul_eq_mul,
    mul_one, mul_neg, neg_mul]
  ring

theorem diagonal_generator_sum (A : (X → K) →ₗ[K] (X → K)) (pnt : X) :
    ∑ p : OffDiag X, (A (Pi.single p.1.2 (1 : K)) p.1.1) *
        finiteCartanGenerator p.1.1 p.1.2 (Pi.single pnt (1 : K)) pnt =
      ∑ j : {j : X // j ≠ pnt}, -A (Pi.single j.1 (1 : K)) pnt := by
  have hre : ∑ p : OffDiag X, (A (Pi.single p.1.2 (1 : K)) p.1.1) *
        finiteCartanGenerator p.1.1 p.1.2 (Pi.single pnt (1 : K)) pnt =
      ∑ s : Σ i : X, {j : X // j ≠ i},
        (A (Pi.single s.2.1 (1 : K)) s.1) *
          finiteCartanGenerator s.1 s.2.1 (Pi.single pnt (1 : K)) pnt := by
    simpa [offDiagSigma] using
      (Equiv.sum_comp (offDiagSigma (X := X)) fun s : Σ i : X, {j : X // j ≠ i} =>
        (A (Pi.single s.2.1 (1 : K)) s.1) *
          finiteCartanGenerator s.1 s.2.1 (Pi.single pnt (1 : K)) pnt)
  rw [hre, Fintype.sum_sigma]
  rw [Fintype.sum_eq_single pnt fun i hi =>
    Finset.sum_eq_zero fun j _ => by
      simp [edgeGenerator_apply, Pi.single_apply, Ne.symm hi]]
  exact diagonal_generator_at_row A pnt

/-- If `A` kills constants, its rows sum to zero, so `A` is the off-diagonal
combination of the generators `G_ij`. -/
theorem annihilator_eq_offDiagonal (A : (X → K) →ₗ[K] (X → K))
    (hA : A (fun _ => (1 : K)) = 0) :
    A = ∑ p : OffDiag X,
      (A (Pi.single p.1.2 (1 : K)) p.1.1) • finiteCartanGenerator p.1.1 p.1.2 := by
  apply (Pi.basisFun K X).ext
  intro k
  ext pnt
  simp only [Pi.basisFun_apply]
  rw [offDiagonal_combination_eq]
  by_cases hpk : pnt = k
  · subst hpk
    have hdiag := diagonal_generator_sum A pnt
    have hcomp := row_complement A hA pnt
    have hneg : ∑ j : {j : X // j ≠ pnt}, -A (Pi.single j.1 (1 : K)) pnt =
        A (Pi.single pnt (1 : K)) pnt := by
      rw [Finset.sum_neg_distrib, hcomp, neg_neg]
    exact (show
      ∑ p : OffDiag X, (A (Pi.single p.1.2 (1 : K)) p.1.1) *
          finiteCartanGenerator p.1.1 p.1.2 (Pi.single pnt (1 : K)) pnt =
        A (Pi.single pnt (1 : K)) pnt from hdiag.trans hneg).symm
  · let p₀ : OffDiag X := ⟨(pnt, k), hpk⟩
    let g : OffDiag X → K := fun p =>
      (A (Pi.single p.1.2 (1 : K)) p.1.1) *
        finiteCartanGenerator p.1.1 p.1.2 (Pi.single k (1 : K)) pnt
    have hsingle : (∑ p : OffDiag X, g p) = g p₀ :=
      Fintype.sum_eq_single p₀ (by
        intro p hp
        by_cases hrow : p.1.1 = pnt
        · by_cases hcol : p.1.2 = k
          · exact (hp (Subtype.ext (Prod.ext hrow hcol))).elim
          · simp only [g]
            rw [edgeGenerator_apply, hrow]
            simp [Pi.single_apply, hcol, hpk, mul_zero]
        · simp only [g]
          rw [edgeGenerator_apply]
          simp [Pi.single_apply, Ne.symm hrow, mul_zero])
    have hterm : g p₀ = A (Pi.single k (1 : K)) pnt := by
      simp only [g, p₀]
      rw [edgeGenerator_apply]
      have hcol : k ≠ pnt := Ne.symm hpk
      simp [Pi.single_apply, hpk, hcol, mul_one, sub_zero]
    exact (hsingle.trans hterm).symm

def offDiagonalVec (p : OffDiag X) : LinearMap.ker (evalConst (K := K) (X := X)) :=
  ⟨finiteCartanGenerator p.1.1 p.1.2, by
    simpa [evalConst] using edgeGenerator_kills_constants p.1.1 p.1.2⟩

theorem linearIndependent_offDiagonalVec :
    LinearIndependent K (offDiagonalVec (K := K) (X := X)) := by
  refine LinearIndependent.of_comp
    (LinearMap.ker (evalConst (K := K) (X := X))).subtype ?_
  have hfun : (LinearMap.ker (evalConst (K := K) (X := X))).subtype ∘
      offDiagonalVec (K := K) (X := X) =
      fun p : OffDiag X => finiteCartanGenerator p.1.1 p.1.2 := by
    funext p
    rfl
  simpa [hfun] using linearIndependent_edgeGenerator (K := K) (X := X)

theorem offDiagonalVec_spans :
    ⊤ ≤ Submodule.span K (Set.range (offDiagonalVec (K := K) (X := X))) := by
  rw [Submodule.top_le_span_range_iff_forall_exists_fun]
  intro A
  refine ⟨fun p => (A : (X → K) →ₗ[K] (X → K)) (Pi.single p.1.2 (1 : K)) p.1.1, ?_⟩
  apply Subtype.ext
  have hkill : (A : (X → K) →ₗ[K] (X → K)) (fun _ => (1 : K)) = 0 := by
    exact A.property
  simp only [Submodule.coe_sum, Submodule.coe_smul, offDiagonalVec]
  exact (annihilator_eq_offDiagonal (A : (X → K) →ₗ[K] (X → K)) hkill).symm

/-- The family `G_ij`, `i ≠ j`, is a basis of the constant annihilator. -/
noncomputable def offDiagonalBasis :
    Module.Basis (OffDiag X) K (LinearMap.ker (evalConst (K := K) (X := X))) :=
  Module.Basis.mk (linearIndependent_offDiagonalVec (K := K) (X := X))
    (offDiagonalVec_spans (K := K) (X := X))

theorem card_offDiag : Fintype.card (OffDiag X) =
    Fintype.card X * (Fintype.card X - 1) := by
  classical
  have hdiag : Fintype.card {p : X × X // p.1 = p.2} = Fintype.card X :=
    Fintype.card_congr {
      toFun := fun p => p.1.1
      invFun := fun i => ⟨(i, i), rfl⟩
      left_inv := by
        intro p
        rcases p with ⟨⟨a, b⟩, h⟩
        cases h
        rfl
      right_inv := fun _ => rfl
    }
  have hcompl := Fintype.card_subtype_compl (fun p : X × X => p.1 = p.2)
  have hprod : Fintype.card (X × X) = Fintype.card X * Fintype.card X := by
    simp
  have hsub : Fintype.card X * Fintype.card X - Fintype.card X =
      Fintype.card X * (Fintype.card X - 1) := by
    simpa [mul_one] using
      (Nat.mul_sub_left_distrib (Fintype.card X) (Fintype.card X) 1).symm
  simpa [OffDiag, hprod, hdiag, hsub] using hcompl

theorem finrank_annihilatesConstants :
    Module.finrank K (LinearMap.ker (evalConst (K := K) (X := X))) =
      Fintype.card X * (Fintype.card X - 1) := by
  rw [Module.finrank_eq_card_basis (offDiagonalBasis (K := K) (X := X)), card_offDiag]

theorem edgeLieClosure_eq_annihilatesConstants (E : X → X → Prop)
    (hE : StronglyConnected E) (A : (X → K) →ₗ[K] (X → K)) :
    InLie (edgeGen E : ((X → K) →ₗ[K] (X → K)) → Prop) A ↔
      A (fun _ => (1 : K)) = 0 := by
  constructor
  · intro hA
    exact inLie_kills_constants (fun B hB => edgeGen_kills E B hB) hA
  · intro hA
    rw [annihilator_eq_offDiagonal A hA]
    refine inLie_sum_univ ?_
    intro p
    exact edgeGenerator_mem_of_connected E hE p.2

/-! ## Archive specialization

Positive role steps on `(Z/LZ)^4` are strongly connected. The scalar site
closure therefore has dimension `L^4 (L^4 - 1)`. Fock multiplicity is not
included.
-/

def archivePositiveEdge (N : ℕ) (x y : ArchiveRolePhaseGroup N) : Prop :=
  ∃ r : Role, y = roleTranslatePlus N r x

def coordWalk (N : ℕ) (r : Role) : ℕ → ArchiveRolePhaseGroup N → List (ArchiveRolePhaseGroup N)
  | 0, x => [x]
  | k + 1, x => x :: coordWalk N r k (roleTranslatePlus N r x)

theorem coordWalk_length (N : ℕ) (r : Role) (k : ℕ) (x : ArchiveRolePhaseGroup N) :
    (coordWalk N r k x).length = k + 1 := by
  induction k generalizing x with
  | zero => simp [coordWalk]
  | succ k ih => simp [coordWalk, ih]

theorem coordWalk_ne_nil (N : ℕ) (r : Role) (k : ℕ) (x : ArchiveRolePhaseGroup N) :
    coordWalk N r k x ≠ [] := by
  cases k <;> simp [coordWalk]

theorem coordWalk_head (N : ℕ) (r : Role) (k : ℕ) (x : ArchiveRolePhaseGroup N) :
    (coordWalk N r k x).head? = some x := by
  cases k <;> simp [coordWalk]

theorem coordWalk_getLast (N : ℕ) (r : Role) (k : ℕ) (x : ArchiveRolePhaseGroup N) :
    (coordWalk N r k x).getLast (coordWalk_ne_nil N r k x) =
      x + (k : ZMod (archiveFibers N)) • roleStep N r := by
  induction k generalizing x with
  | zero => simp [coordWalk, zero_smul, add_zero]
  | succ k ih =>
      simp only [coordWalk]
      rw [List.getLast_cons (coordWalk_ne_nil N r k (roleTranslatePlus N r x))]
      rw [ih, roleTranslatePlus_apply]
      have hcast : ((k + 1 : ℕ) : ZMod (archiveFibers N)) = (k : ZMod (archiveFibers N)) + 1 := by
        simp [Nat.cast_succ]
      rw [hcast, add_smul, one_smul]
      abel_nf

theorem coordWalk_chain (N : ℕ) (r : Role) (k : ℕ) (x : ArchiveRolePhaseGroup N) :
    (coordWalk N r k x).IsChain (archivePositiveEdge N) := by
  induction k generalizing x with
  | zero =>
      simpa [coordWalk] using List.isChain_singleton x
  | succ k ih =>
      simp only [coordWalk]
      refine List.IsChain.cons (ih _) ?_
      intro y hy
      have hhead := coordWalk_head N r k (roleTranslatePlus N r x)
      simp [hhead] at hy
      subst hy
      exact ⟨r, rfl⟩

def roleEnum : List Role := [(0, 0), (0, 1), (1, 0), (1, 1)]

theorem roleEnum_complete (r : Role) : r ∈ roleEnum := by
  rcases r with ⟨a, b⟩
  fin_cases a <;> fin_cases b <;> simp [roleEnum]

def spliceWalk (N : ℕ) : List Role → ArchiveRolePhaseGroup N → ArchiveRolePhaseGroup N →
    List (ArchiveRolePhaseGroup N)
  | [], _, x => [x]
  | r :: rs, target, x =>
      (coordWalk N r (target r - x r).val x).dropLast ++
        spliceWalk N rs target
          (x + (((target r - x r).val : ℕ) : ZMod (archiveFibers N)) • roleStep N r)

theorem isChain_glue {E : X → X → Prop} {w q : List X}
    (hw : w.IsChain E) (hq : q.IsChain E) (hwne : w ≠ []) (hqne : q ≠ [])
    (hjoin : q.head? = some (w.getLast hwne)) :
    (w.dropLast ++ q).IsChain E := by
  have hrecon : w.dropLast ++ [w.getLast hwne] = w := List.dropLast_concat_getLast hwne
  have hqcons : w.getLast hwne :: q.tail = q := by
    conv_rhs => rw [← List.cons_head_tail hqne]
    congr 1
    simpa [List.head?_eq_some_head hqne] using hjoin.symm
  have h1 : List.IsChain E (w.dropLast ++ [w.getLast hwne]) := by
    rw [hrecon]
    exact hw
  have h2 : List.IsChain E ([w.getLast hwne] ++ q.tail) := by
    rw [List.singleton_append, hqcons]
    exact hq
  have hoverlap := List.IsChain.append_overlap h1 h2 (by simp)
  rw [List.append_assoc, List.singleton_append, hqcons] at hoverlap
  exact hoverlap

theorem spliceWalk_last_fun (N : ℕ) (r : Role) (rs : List Role)
    (target x y : ArchiveRolePhaseGroup N) (hy_r : y r = target r)
    (hy_ne : ∀ s, s ≠ r → y s = x s) :
    (fun s => if s ∈ rs then target s else y s) =
      fun s => if s ∈ r :: rs then target s else x s := by
  ext s
  by_cases hs : s = r
  · subst hs
    by_cases hmem : s ∈ rs <;> simp [hmem, hy_r]
  · by_cases hmem : s ∈ rs <;> simp [hs, hmem, hy_ne s hs]

theorem spliceWalk_spec (N : ℕ) (rs : List Role) (target x : ArchiveRolePhaseGroup N) :
    (spliceWalk N rs target x) ≠ [] ∧
      (spliceWalk N rs target x).head? = some x ∧
      (spliceWalk N rs target x).getLast? =
        some (fun s => if s ∈ rs then target s else x s) ∧
      (spliceWalk N rs target x).IsChain (archivePositiveEdge N) := by
  induction rs generalizing x with
  | nil =>
      refine ⟨by simp [spliceWalk], by simp [spliceWalk], ?_, List.isChain_singleton x⟩
      simp [spliceWalk]
  | cons r rs ih =>
      dsimp [spliceWalk]
      set k : ℕ := (target r - x r).val with hk
      set y := x + ((k : ℕ) : ZMod (archiveFibers N)) • roleStep N r with hy
      set w := coordWalk N r k x with hw
      obtain ⟨rest_ne, rest_head, rest_last, rest_chain⟩ := ih (x := y)
      have wne : w ≠ [] := coordWalk_ne_nil N r k x
      have whead : w.head? = some x := coordWalk_head N r k x
      have wchain : w.IsChain (archivePositiveEdge N) := coordWalk_chain N r k x
      have wlast : w.getLast wne = y := by
        simpa [hw, hy] using coordWalk_getLast N r k x
      have hy_r : y r = target r := by
        rw [hy]
        simp only [Pi.add_apply, roleStep, Pi.smul_apply, if_pos rfl, mul_one]
        rw [hk, ZMod.natCast_zmod_val]
        simp [smul_eq_mul, mul_one, sub_eq_add_neg, add_assoc, add_left_comm, add_comm]
      have hy_ne : ∀ s, s ≠ r → y s = x s := by
        intro s hs
        rw [hy]
        simp only [Pi.add_apply, roleStep, Pi.smul_apply, if_neg hs, smul_zero, add_zero]
      have hlast_fun := spliceWalk_last_fun N r rs target x y hy_r hy_ne
      refine ⟨?_, ?_, ?_, ?_⟩
      · intro hnil
        exact rest_ne (List.append_eq_nil_iff.mp hnil).2
      · by_cases hk0 : k = 0
        · have hw0 : w = [x] := by rw [hw, hk0]; rfl
          have hdrop : w.dropLast = [] := by simp [hw0]
          have hyx : y = x := by simp [hy, hk0, zero_smul, add_zero]
          rw [hdrop, List.nil_append, rest_head, hyx]
        · have hlen : 1 < w.length := by
            rw [hw, coordWalk_length]
            omega
          simp [List.head?_append, List.head?_dropLast, hlen, whead]
      · have hgl : (w.dropLast ++ spliceWalk N rs target y).getLast? =
            (spliceWalk N rs target y).getLast? := by
          rw [List.getLast?_append, List.getLast?_eq_some_getLast rest_ne]
          simp
        rw [hgl, rest_last, hlast_fun]
      · by_cases hk0 : k = 0
        · have hw0 : w = [x] := by rw [hw, hk0]; rfl
          simpa [hw0] using rest_chain
        · exact isChain_glue wchain rest_chain wne rest_ne
            (by rw [rest_head, wlast])

theorem archive_positiveEdge_stronglyConnected (N : ℕ) :
    StronglyConnected (X := ArchiveRolePhaseGroup N) (archivePositiveEdge N) := by
  intro x y
  obtain ⟨hne, hhead, hlast, hchain⟩ := spliceWalk_spec N roleEnum y x
  have htarget : (fun s => if s ∈ roleEnum then y s else x s) = y := by
    ext s
    simp [roleEnum_complete s]
  refine ⟨spliceWalk N roleEnum y x, hne, hhead, ?_, hchain⟩
  simpa [htarget] using hlast

theorem archive_card (N : ℕ) :
    Fintype.card (ArchiveRolePhaseGroup N) = archiveModes N := by
  exact card_archive_role_phase_group N

theorem archive_scalar_closure_finrank (N : ℕ) :
    Module.finrank K (LinearMap.ker
      (evalConst (K := K) (X := ArchiveRolePhaseGroup N))) =
      archiveModes N * (archiveModes N - 1) := by
  rw [finrank_annihilatesConstants, archive_card]

theorem archive_edgeLie_iff_kills (N : ℕ)
    (A : (ArchiveRolePhaseGroup N → K) →ₗ[K] (ArchiveRolePhaseGroup N → K)) :
    InLie (edgeGen (archivePositiveEdge N) :
        ((ArchiveRolePhaseGroup N → K) →ₗ[K] (ArchiveRolePhaseGroup N → K)) → Prop) A ↔
      A (fun _ => (1 : K)) = 0 :=
  edgeLieClosure_eq_annihilatesConstants (archivePositiveEdge N)
    (archive_positiveEdge_stronglyConnected N) A

/-! ## Bounded-radius no-go

For each fixed radius `R`, the directed cycle of length `2R + 3` has every
nearest-neighbour generator inside radius 1, but the Lie closure contains an
operator with a nonzero matrix entry at distance `R + 1`.

This is a no-go for a lattice-size-independent radius that contains all those
generators and is closed under the Lie bracket. It is not a no-go for an
arbitrary nonlinear theory.
-/

def cycleEdge {n : ℕ} [NeZero n] (x y : ZMod n) : Prop :=
  y = x + 1

def cycleDist {n : ℕ} [NeZero n] (x y : ZMod n) : ℕ :=
  min (y - x).val (x - y).val

open Classical in
noncomputable def supportRadius {n : ℕ} [NeZero n]
    (A : (ZMod n → K) →ₗ[K] (ZMod n → K)) : ℕ :=
  Finset.univ.sup fun p : ZMod n × ZMod n =>
    if A (Pi.single p.2 (1 : K)) p.1 ≠ 0 then cycleDist p.1 p.2 else 0

theorem supportRadius_ge {n : ℕ} [NeZero n]
    (A : (ZMod n → K) →ₗ[K] (ZMod n → K)) {x y : ZMod n}
    (h : A (Pi.single y (1 : K)) x ≠ 0) :
    cycleDist x y ≤ supportRadius A := by
  classical
  let f : ZMod n × ZMod n → ℕ := fun p =>
    if A (Pi.single p.2 (1 : K)) p.1 ≠ 0 then cycleDist p.1 p.2 else 0
  have hle : f (x, y) ≤ Finset.univ.sup f := Finset.le_sup (Finset.mem_univ (x, y))
  calc
    cycleDist x y = f (x, y) := by simp [f, h]
    _ ≤ Finset.univ.sup f := hle
    _ = supportRadius A := rfl

def natPrefix (m : ℕ) : ℕ → List (ZMod m)
  | 0 => []
  | n + 1 => natPrefix m n ++ [(n : ZMod m)]

theorem natPrefix_length (m n : ℕ) : (natPrefix m n).length = n := by
  induction n with
  | zero => simp [natPrefix]
  | succ n ih => simp [natPrefix, ih]

theorem natPrefix_ne_nil (m n : ℕ) (hn : 0 < n) : natPrefix m n ≠ [] := by
  intro h
  have := congrArg List.length h
  rw [natPrefix_length, List.length_nil] at this
  omega

theorem natPrefix_getLast (m n : ℕ) (hn : 0 < n) :
    (natPrefix m n).getLast (natPrefix_ne_nil m n hn) = (n - 1 : ℕ) := by
  induction n with
  | zero => omega
  | succ n ih =>
      simp only [natPrefix, List.getLast_append, List.getLast_singleton]
      cases n with
      | zero => rfl
      | succ n =>
          have := ih (by omega)
          simp

def cyclePrefix (R : ℕ) : List (ZMod (2 * R + 3)) :=
  natPrefix (2 * R + 3) (R + 2)

theorem cyclePrefix_length (R : ℕ) : (cyclePrefix R).length = R + 2 := by
  simp [cyclePrefix, natPrefix_length]

theorem natPrefix_mem {m n : ℕ} (hn : n ≤ m) (hm : 0 < m) {a : ZMod m} :
    a ∈ natPrefix m n ↔ ∃ i, i < n ∧ a = (i : ZMod m) := by
  induction n with
  | zero => simp [natPrefix]
  | succ n ih =>
      have ihn := ih (Nat.le_of_succ_le hn)
      simp only [natPrefix, List.mem_append, List.mem_singleton, ihn]
      constructor
      · intro h
        rcases h with ⟨i, hi, hi'⟩ | hi'
        · exact ⟨i, Nat.lt_succ_of_lt hi, hi'⟩
        · exact ⟨n, Nat.lt_succ_self n, hi'⟩
      · intro ⟨i, hi, hi'⟩
        rcases Nat.lt_succ_iff_lt_or_eq.mp hi with hlt | heq
        · exact Or.inl ⟨i, hlt, hi'⟩
        · subst heq
          exact Or.inr hi'

theorem natPrefix_nodup (m n : ℕ) (hn : n ≤ m) (hm : 0 < m) : (natPrefix m n).Nodup := by
  induction n with
  | zero => simp [natPrefix]
  | succ n ih =>
      have hn' : n ≤ m := Nat.le_of_succ_le hn
      have hdisj : List.Disjoint (natPrefix m n) [((n : ℕ) : ZMod m)] := by
        rw [List.disjoint_iff_ne]
        intro a ha b hb
        have hb' : b = ((n : ℕ) : ZMod m) := by simpa using hb
        obtain ⟨i, hi, hi'⟩ := (natPrefix_mem hn' hm).1 ha
        intro h
        have hval := congrArg ZMod.val h
        haveI : NeZero m := ⟨by omega⟩
        rw [hi', hb', ZMod.val_natCast, ZMod.val_natCast,
          Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hi hn'),
          Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le (Nat.lt_succ_self n) hn)] at hval
        omega
      rw [show natPrefix m (n + 1) = natPrefix m n ++ [((n : ℕ) : ZMod m)] by rfl]
      exact List.nodup_append'.2 ⟨ih hn', by simp, hdisj⟩

theorem cyclePrefix_nodup (R : ℕ) : (cyclePrefix R).Nodup := by
  simpa [cyclePrefix] using natPrefix_nodup (2 * R + 3) (R + 2) (by omega) (by omega)

theorem natPrefix_chain (m n : ℕ) :
    (natPrefix m n).IsChain (fun x y : ZMod m => y = x + 1) := by
  induction n with
  | zero => simp [natPrefix]
  | succ n ih =>
      cases n with
      | zero => simp [natPrefix]
      | succ n =>
          have hne : natPrefix m (n + 1) ≠ [] := natPrefix_ne_nil m (n + 1) (by omega)
          apply List.IsChain.append ih (by simp [natPrefix])
          intro a ha b hb
          have ha' : (natPrefix m (n + 1)).getLast hne = a := by
            simpa [List.getLast?_eq_some_getLast hne] using ha
          have hb' : (n + 1 : ℕ) = b := by
            simpa [natPrefix] using hb
          rw [← ha', ← hb', natPrefix_getLast m (n + 1) (by omega)]
          simp [Nat.cast_succ]

theorem cyclePrefix_chain (R : ℕ) :
    (cyclePrefix R).IsChain (cycleEdge (n := 2 * R + 3)) := by
  haveI : NeZero (2 * R + 3) := ⟨by omega⟩
  simpa [cyclePrefix, cycleEdge] using natPrefix_chain (2 * R + 3) (R + 2)

theorem natPrefix_head (m n : ℕ) (hn : 0 < n) :
    (natPrefix m n).head (natPrefix_ne_nil m n hn) = 0 := by
  have h? : (natPrefix m n).head? = some 0 := by
    induction n with
    | zero => omega
    | succ n ih =>
        cases n with
        | zero => simp [natPrefix]
        | succ n =>
            have hprev : natPrefix m (n + 1) ≠ [] := natPrefix_ne_nil m (n + 1) (by omega)
            have hrec : natPrefix m (n + 2) =
                natPrefix m (n + 1) ++ [((n + 1 : ℕ) : ZMod m)] := by
              simp [natPrefix]
            rw [hrec, List.head?_append_of_ne_nil (natPrefix m (n + 1)) hprev]
            exact ih (by omega)
  simpa [List.head?_eq_some_head (natPrefix_ne_nil m n hn)] using h?

theorem cyclePrefix_getLast (R : ℕ) :
    (cyclePrefix R).getLast (by
        simpa [cyclePrefix] using natPrefix_ne_nil (2 * R + 3) (R + 2) (by omega)) =
      ((R + 1 : ℕ) : ZMod (2 * R + 3)) := by
  simpa [cyclePrefix] using natPrefix_getLast (2 * R + 3) (R + 2) (by omega)

theorem cycle_nested_entry (R : ℕ) :
    nestedBracket (K := K) (cyclePrefix R)
        (Pi.single (((R + 1 : ℕ) : ZMod (2 * R + 3))) (1 : K)) 0 = 1 := by
  have hlen : 2 ≤ (cyclePrefix R).length := by
    rw [cyclePrefix_length]
    omega
  have hn := cyclePrefix_nodup R
  rw [nestedBracket_simplePath hn hlen]
  have hlast := listLast_eq_getLast_of_length (p := cyclePrefix R) hlen
  have hget := cyclePrefix_getLast R
  have h0 : (cyclePrefix R)[0] = (0 : ZMod (2 * R + 3)) := by
    have hhead := natPrefix_head (2 * R + 3) (R + 2) (by omega)
    simpa [cyclePrefix, List.head_eq_getElem] using hhead
  have hne := secondLast_ne_listLast hn hlen
  rw [hlast, hget, h0] at hne
  simp only [LinearMap.sub_apply, Pi.sub_apply, matrixUnit_apply, Pi.single_apply, hlast, hget, h0]
  simp only [if_true, if_neg hne, sub_zero]

theorem cycleDist_prefix (R : ℕ) :
    cycleDist (n := 2 * R + 3) (0 : ZMod (2 * R + 3))
        (((R + 1 : ℕ) : ZMod (2 * R + 3))) = R + 1 := by
  haveI : NeZero (2 * R + 3) := ⟨by omega⟩
  have hlt : R + 1 < 2 * R + 3 := by omega
  have hval : (((R + 1 : ℕ) : ZMod (2 * R + 3))).val = R + 1 := by
    rw [ZMod.val_natCast]
    norm_num [Nat.mod_eq_of_lt hlt]
  have hne : (((R + 1 : ℕ) : ZMod (2 * R + 3))) ≠ 0 := by
    intro h
    have := congrArg ZMod.val h
    rw [hval, ZMod.val_zero] at this
    omega
  have hback : (2 * R + 3) - (R + 1) = R + 2 := by omega
  change min (((R + 1 : ℕ) : ZMod (2 * R + 3)) - 0).val
      (0 - ((R + 1 : ℕ) : ZMod (2 * R + 3))).val = R + 1
  simp only [sub_zero, zero_sub, hval]
  have hneg : ( -((R + 1 : ℕ) : ZMod (2 * R + 3))).val = R + 2 := by
    haveI : NeZero (((R + 1 : ℕ) : ZMod (2 * R + 3))) := ⟨hne⟩
    have hcalc := ZMod.val_neg_of_ne_zero (a := ((R + 1 : ℕ) : ZMod (2 * R + 3)))
    rw [hval, hback] at hcalc
    exact hcalc
  rw [hneg]
  exact Nat.min_eq_left (by omega)

/-- No single radius contains every nearest-neighbour generator of every directed
cycle and stays closed under the Lie bracket. -/
theorem no_uniform_radius_lie_closed (R : ℕ) :
    let n := 2 * R + 3
    ∃ A : (ZMod n → K) →ₗ[K] (ZMod n → K),
      InLie (edgeGen (cycleEdge (n := n)) :
          ((ZMod n → K) →ₗ[K] (ZMod n → K)) → Prop) A ∧
        R < supportRadius (n := n) A := by
  intro n
  haveI : NeZero n := ⟨by dsimp [n]; omega⟩
  have hlen : 2 ≤ (cyclePrefix R).length := by
    rw [cyclePrefix_length]
    omega
  refine ⟨nestedBracket (K := K) (cyclePrefix R), ?_, ?_⟩
  · simpa using nestedBracket_mem (E := cycleEdge (n := n)) hlen (cyclePrefix_chain R)
  · have hentry := cycle_nested_entry (K := K) R
    have hnz : nestedBracket (K := K) (cyclePrefix R)
        (Pi.single (((R + 1 : ℕ) : ZMod n)) (1 : K)) 0 ≠ 0 := by
      rw [hentry]
      exact one_ne_zero
    have hle := supportRadius_ge (nestedBracket (K := K) (cyclePrefix R)) hnz
    have hdist := cycleDist_prefix R
    rw [hdist] at hle
    exact Nat.lt_of_lt_of_le (Nat.lt_succ_self R) hle

/-! ## Pointwise derivations vanish

On the finite product algebra `K^X`, every linear Leibniz derivation is zero.
The argument uses the primitive idempotents and does not restrict the
characteristic: the coefficient `1 - 2 δ(z)` is a unit at every site.
-/

def pointwiseMul (f g : X → K) : X → K :=
  fun z => f z * g z

structure PointwiseDerivation (D : (X → K) →ₗ[K] (X → K)) : Prop where
  leibniz : ∀ f g : X → K,
    D (pointwiseMul f g) = pointwiseMul f (D g) + pointwiseMul (D f) g

theorem single_idem (x : X) :
    pointwiseMul (Pi.single x (1 : K)) (Pi.single x 1) = Pi.single x 1 := by
  ext z
  by_cases hz : z = x <;> simp [pointwiseMul, Pi.single_apply, hz]

theorem finite_scalar_derivation_eq_zero (D : (X → K) →ₗ[K] (X → K))
    (hD : PointwiseDerivation D) : D = 0 := by
  classical
  have hdelta : ∀ x, D (Pi.single x (1 : K)) = 0 := by
    intro x
    have hle := hD.leibniz (Pi.single x 1) (Pi.single x 1)
    rw [single_idem x] at hle
    ext z
    have hz := congrFun hle z
    have hdeltaVal : (Pi.single x (1 : K) : X → K) z = if z = x then 1 else 0 := by
      simp [Pi.single_apply]
    change D (Pi.single x (1 : K)) z =
      (Pi.single x (1 : K) : X → K) z * D (Pi.single x (1 : K)) z +
        D (Pi.single x (1 : K)) z * (Pi.single x (1 : K) : X → K) z at hz
    rw [hdeltaVal] at hz
    by_cases hx : z = x
    · subst z
      simp only [if_pos rfl, pointwiseMul, Pi.single_apply] at hz
      have hs : D (Pi.single x (1 : K)) x + D (Pi.single x (1 : K)) x =
          D (Pi.single x (1 : K)) x := by simpa [one_mul, add_comm] using hz.symm
      have hs' : D (Pi.single x (1 : K)) x + D (Pi.single x (1 : K)) x =
          D (Pi.single x (1 : K)) x + 0 := by simpa [Pi.zero_apply] using hs
      have hs0 : (D (Pi.single x (1 : K))) x + (D (Pi.single x (1 : K))) x =
          (D (Pi.single x (1 : K))) x + 0 := by simpa using hs
      exact add_left_cancel hs0
    · simp only [if_neg hx, pointwiseMul, Pi.single_apply, hx] at hz
      simpa using hz
  refine LinearMap.ext fun g => ?_
  funext z
  have hf : g = ∑ x : X, g x • Pi.single x (1 : K) := by
    ext z
    simp [Finset.sum_apply, Pi.smul_apply, Pi.single_apply, smul_eq_mul]
  rw [hf, map_sum]
  simp [map_smul, hdelta]

theorem edgeGenerator_not_derivation (x y : X) (hxy : x ≠ y) :
    ¬ PointwiseDerivation (finiteCartanGenerator (K := K) x y) := by
  intro hD
  exact edgeGenerator_ne_zero x y hxy
    (finite_scalar_derivation_eq_zero (finiteCartanGenerator x y) hD)

/-- The scalar Lie closure of a strongly connected edge set contains a nonzero
operator, while every pointwise derivation is zero. -/
theorem lie_closure_not_pointwise_derivation (E : X → X → Prop)
    (hE : StronglyConnected E) (hcard : 1 < Fintype.card X) :
    ∃ A : (X → K) →ₗ[K] (X → K),
      InLie (edgeGen E : ((X → K) →ₗ[K] (X → K)) → Prop) A ∧
        ¬ PointwiseDerivation A := by
  obtain ⟨x, y, hxy⟩ := Fintype.exists_pair_of_one_lt_card hcard
  exact ⟨finiteCartanGenerator x y, edgeGenerator_mem_of_connected E hE hxy,
    edgeGenerator_not_derivation x y hxy⟩

/-! ## Invertible local gates

`Q_xy(t) = I + t G_xy` uses `G_xy^2 = -G_xy`, so its inverse is another
polynomial in the same generator. No matrix exponential is required.
-/

def localGate (x y : X) (t : K) : (X → K) →ₗ[K] (X → K) :=
  LinearMap.id + t • finiteCartanGenerator x y

theorem localGate_comp_scalar (x y : X) (s t : K) (hxy : x ≠ y) :
    (localGate x y s).comp (localGate x y t) =
      LinearMap.id + (s + t - s * t) • finiteCartanGenerator x y := by
  change (LinearMap.id + s • finiteCartanGenerator x y).comp
      (LinearMap.id + t • finiteCartanGenerator x y) =
    LinearMap.id + (s + t - s * t) • finiteCartanGenerator x y
  simp only [LinearMap.add_comp, LinearMap.comp_add, LinearMap.id_comp,
    LinearMap.comp_id, LinearMap.smul_comp, LinearMap.comp_smul, smul_smul,
    edgeGenerator_sq x y hxy]
  module

theorem localGate_inverse (x y : X) (t : K) (hxy : x ≠ y) (ht : t ≠ 1) :
    (localGate x y (-(t / (1 - t)))).comp (localGate x y t) = LinearMap.id ∧
      (localGate x y t).comp (localGate x y (-(t / (1 - t)))) = LinearMap.id := by
  have hden : 1 - t ≠ 0 := sub_ne_zero.mpr (Ne.symm ht)
  have hcoef : -(t / (1 - t)) + t - (-(t / (1 - t)) * t) = 0 := by
    field_simp [hden]
    ring
  constructor
  · rw [localGate_comp_scalar x y (-(t / (1 - t))) t hxy]
    rw [hcoef, zero_smul, add_zero]
  · rw [localGate_comp_scalar x y t (-(t / (1 - t))) hxy]
    have hcoef' : t + -(t / (1 - t)) - t * -(t / (1 - t)) = 0 := by
      calc
        _ = -(t / (1 - t)) + t - (-(t / (1 - t)) * t) := by ring
        _ = 0 := hcoef
    rw [hcoef', zero_smul, add_zero]

theorem localGate_fixes_constants (x y : X) (t : K) :
    localGate x y t (fun _ => (1 : K)) = fun _ => 1 := by
  simp [localGate, edgeGenerator_kills_constants]

end D0.Geometry
