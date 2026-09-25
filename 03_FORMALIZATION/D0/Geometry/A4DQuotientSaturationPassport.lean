import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.LinearAlgebra.Quotient.Basic

/-!
# Same-fibre quotient saturation passport

Finite linear algebra for memo §11 of
`MEMO_A4D_CLASSICAL_KINEMATIC_INTERFACE_PRESSURE`:

* `(11.1)` `im(q ∘ B, q ∘ S)` is a graph iff `S(B⁻¹ W) ⊆ W`;
* `(11.2)` invertible quotient transport exists both ways iff `P W' = W`,
  and the loop acts as the identity on the quotient iff `(P - I) V ⊆ W`;
* `(11.3)` / Theorem 4: the saturation recursion produces the least
  basepoint subspace with both properties;
* the zero quotient `W = ⊤` is always a fixed point.

The coinvariant `H` is the sum of the images `(Pγ - I) V`. It is not
PR #120's common fixed space.

Firewalls (this module does **not**):
* infer a physical observer, readout, or physical quotient;
* choose a constitutive star, `C_N`, nonlinear `Q(e)`, or `H(e)`;
* touch stress, Einstein, continuum, physical time, or golden refinement;
* modify located `J`.
-/

namespace D0.Geometry

open Module

noncomputable section

variable {K U V Q : Type*} [Field K]
  [AddCommGroup U] [Module K U]
  [AddCommGroup V] [Module K V]
  [AddCommGroup Q] [Module K Q]

/-! ## 1. Same-fibre graph criterion (11.1) -/

/-- `im(q ∘ B, q ∘ S)` is a graph: equal quotient inputs determine the quotient output. -/
def SameFibreQuotientGraph (q : V →ₗ[K] Q) (B S : U →ₗ[K] V) : Prop :=
  ∀ x y : U, q (B x) = q (B y) → q (S x) = q (S y)

/-- Forgetting only the solder output: `(B, q ∘ S)` is a graph. -/
def SolderOutputQuotientGraph (q : V →ₗ[K] Q) (B S : U →ₗ[K] V) : Prop :=
  ∀ x y : U, B x = B y → q (S x) = q (S y)

/-- Vertical defect `M = S(ker B)`. -/
def verticalDefect (B S : U →ₗ[K] V) : Submodule K V :=
  (LinearMap.ker B).map S

theorem sameFibreQuotientGraph_iff_comap (q : V →ₗ[K] Q) (B S : U →ₗ[K] V) :
    SameFibreQuotientGraph q B S ↔
      Submodule.comap B (LinearMap.ker q) ≤ Submodule.comap S (LinearMap.ker q) := by
  constructor
  · intro h u hu
    have hBu : q (B u) = 0 := by
      simpa [LinearMap.mem_ker] using hu
    have hxy : q (B u) = q (B 0) := by
      simpa using hBu
    have hSu : q (S u) = q (S 0) := h u 0 hxy
    simpa [LinearMap.mem_ker] using hSu
  · intro h x y hxy
    have hker : B (x - y) ∈ LinearMap.ker q := by
      simp [LinearMap.mem_ker, map_sub, hxy]
    have hmem : x - y ∈ Submodule.comap B (LinearMap.ker q) := by
      simpa [Submodule.mem_comap] using hker
    have hS : S (x - y) ∈ LinearMap.ker q := h hmem
    simp [LinearMap.mem_ker, map_sub, sub_eq_zero] at hS
    exact hS

/-- (11.1). The same-fibre quotient relation is a graph iff `S(B⁻¹ W) ⊆ W`. -/
theorem sameFibreQuotientGraph_mkQ_iff (W : Submodule K V) (B S : U →ₗ[K] V) :
    SameFibreQuotientGraph W.mkQ B S ↔
      (Submodule.comap B W).map S ≤ W := by
  rw [sameFibreQuotientGraph_iff_comap, Submodule.ker_mkQ]
  exact (Submodule.map_le_iff_le_comap).symm

/-- Forgetting only the output coordinate is the weaker test `M ⊆ ker q`. -/
theorem solderOutputQuotientGraph_iff_verticalDefect_le
    (q : V →ₗ[K] Q) (B S : U →ₗ[K] V) :
    SolderOutputQuotientGraph q B S ↔ verticalDefect B S ≤ LinearMap.ker q := by
  constructor
  · intro h v hv
    rcases hv with ⟨u, hu, rfl⟩
    have hu0 : B u = 0 := by
      simpa [LinearMap.mem_ker] using hu
    have hzero : q (S u) = q (S 0) := h u 0 (by simpa using hu0)
    simpa [LinearMap.mem_ker] using hzero
  · intro h x y hxy
    have hdiff : x - y ∈ LinearMap.ker B := by
      simp [LinearMap.mem_ker, map_sub, hxy]
    have hS : S (x - y) ∈ LinearMap.ker q := h ⟨x - y, hdiff, rfl⟩
    simp [LinearMap.mem_ker, map_sub, sub_eq_zero] at hS
    exact hS

theorem solderOutputQuotientGraph_mkQ_iff (W : Submodule K V) (B S : U →ₗ[K] V) :
    SolderOutputQuotientGraph W.mkQ B S ↔ verticalDefect B S ≤ W := by
  rw [solderOutputQuotientGraph_iff_verticalDefect_le, Submodule.ker_mkQ]

/-- Under an existing factorization `S = J ∘ B`, (11.1) is invariance of `range B ∩ W`. -/
theorem sameFibreQuotientGraph_of_factor (J : V →ₗ[K] V) (B : U →ₗ[K] V)
    (W : Submodule K V) :
    (Submodule.comap B W).map (J.comp B) ≤ W ↔
      (LinearMap.range B ⊓ W).map J ≤ W := by
  rw [Submodule.map_comp, Submodule.map_comap_eq]

/-! ## 2. Quotient transport (11.2) -/

/-- `P - I`, with the identity annotated so the subtraction elaborates. -/
def loopDeviation (P : V ≃ₗ[K] V) : V →ₗ[K] V :=
  P.toLinearMap - LinearMap.id (R := K) (M := V)

/-- Image of `(P - I)`. This is one loop's contribution to the coinvariant. -/
def coinvariantImage (P : V ≃ₗ[K] V) : Submodule K V :=
  LinearMap.range (loopDeviation P)

/-- Sum of loop coinvariants. Not a common fixed space. -/
def coinvariantSum {loopIdx : Type*} (loops : loopIdx → V ≃ₗ[K] V) : Submodule K V :=
  ⨆ j, coinvariantImage (loops j)

theorem loopDeviation_apply (P : V ≃ₗ[K] V) (v : V) :
    loopDeviation P v = P v - v := by
  simp [loopDeviation, LinearMap.sub_apply, LinearMap.id_apply]

theorem coinvariantImage_refl : coinvariantImage (LinearEquiv.refl K V) = ⊥ := by
  unfold coinvariantImage loopDeviation
  have : (LinearEquiv.refl K V).toLinearMap - LinearMap.id (R := K) (M := V) = 0 := by
    ext v
    simp
  rw [this, LinearMap.range_zero]

theorem coinvariantImage_symm (P : V ≃ₗ[K] V) :
    coinvariantImage P.symm = coinvariantImage P := by
  apply le_antisymm
  · intro x hx
    rcases hx with ⟨v, rfl⟩
    rw [loopDeviation_apply]
    have hcalc : P.symm v - v = -(P (P.symm v) - P.symm v) := by
      rw [LinearEquiv.apply_symm_apply]
      abel
    rw [hcalc]
    refine (coinvariantImage P).neg_mem ?_
    rw [← loopDeviation_apply]
    exact LinearMap.mem_range_self _ (P.symm v)
  · intro x hx
    rcases hx with ⟨v, rfl⟩
    rw [loopDeviation_apply]
    have hcalc : P v - v = -(P.symm (P v) - P v) := by
      rw [LinearEquiv.symm_apply_apply]
      abel
    rw [hcalc]
    refine (coinvariantImage P.symm).neg_mem ?_
    rw [← loopDeviation_apply]
    exact LinearMap.mem_range_self _ (P v)

/-- `(PQ - I) V` sits in the sum of the factor images. `Q.trans P` applies `Q` first. -/
theorem coinvariantImage_trans_le (P Q : V ≃ₗ[K] V) :
    coinvariantImage (Q.trans P) ≤ coinvariantImage P ⊔ coinvariantImage Q := by
  intro x hx
  rcases hx with ⟨v, rfl⟩
  rw [loopDeviation_apply, LinearEquiv.trans_apply]
  have hcalc : P (Q v) - v = (P (Q v) - Q v) + (Q v - v) := by
    abel
  rw [hcalc]
  refine Submodule.add_mem _ ?_ ?_
  · exact Submodule.mem_sup_left (by
      rw [← loopDeviation_apply]
      exact LinearMap.mem_range_self _ (Q v))
  · exact Submodule.mem_sup_right (by
      rw [← loopDeviation_apply]
      exact LinearMap.mem_range_self _ v)

theorem quotientTransport_exists_iff
    {V' : Type*} [AddCommGroup V'] [Module K V']
    (P : V' →ₗ[K] V) (W' : Submodule K V') (W : Submodule K V) :
    (∃ Pbar : (V' ⧸ W') →ₗ[K] (V ⧸ W), W.mkQ.comp P = Pbar.comp W'.mkQ) ↔
      W'.map P ≤ W := by
  constructor
  · rintro ⟨Pbar, hbar⟩
    intro x hx
    rcases hx with ⟨w', hw', rfl⟩
    have happ :
        W.mkQ (P w') = Pbar (W'.mkQ w') := by
      simpa [LinearMap.comp_apply] using LinearMap.congr_fun hbar w'
    have hzero : W'.mkQ w' = 0 := (Submodule.Quotient.mk_eq_zero _).2 hw'
    rw [hzero, map_zero] at happ
    exact (Submodule.Quotient.mk_eq_zero _).1 (by simpa [Submodule.mkQ_apply] using happ)
  · intro hle
    have hker : W' ≤ LinearMap.ker (W.mkQ.comp P) := by
      intro w' hw'
      rw [LinearMap.mem_ker, LinearMap.comp_apply, Submodule.mkQ_apply,
        Submodule.Quotient.mk_eq_zero]
      exact hle ⟨w', hw', rfl⟩
    refine ⟨W'.liftQ (W.mkQ.comp P) hker, ?_⟩
    simp [Submodule.liftQ_mkQ]

theorem map_eq_of_symm_maps_le
    {V' : Type*} [AddCommGroup V'] [Module K V']
    (P : V' ≃ₗ[K] V) (W' : Submodule K V') (W : Submodule K V)
    (hP : W'.map P.toLinearMap ≤ W) (hS : W.map P.symm.toLinearMap ≤ W') :
    W'.map P.toLinearMap = W := by
  apply le_antisymm hP
  intro w hw
  refine ⟨P.symm w, hS ⟨w, hw, rfl⟩, ?_⟩
  simp

/-- Both directions of quotient transport exist iff `P` identifies the kernels. -/
theorem quotientTransport_bi_iff
    {V' : Type*} [AddCommGroup V'] [Module K V']
    (P : V' ≃ₗ[K] V) (W' : Submodule K V') (W : Submodule K V) :
    W'.map P.toLinearMap = W ↔
      W'.map P.toLinearMap ≤ W ∧ W.map P.symm.toLinearMap ≤ W' := by
  constructor
  · intro h
    refine ⟨h.le, ?_⟩
    rw [← h]
    intro x hx
    rcases hx with ⟨w, hw, rfl⟩
    rcases hw with ⟨w', hw', rfl⟩
    simpa using hw'
  · rintro ⟨hP, hS⟩
    exact map_eq_of_symm_maps_le P W' W hP hS

/-- (11.2), loop form: `(P - I) V ⊆ W` iff `P` acts as the identity on `V ⧸ W`. -/
theorem coinvariant_le_iff_quotient_id (P : V ≃ₗ[K] V) (W : Submodule K V) :
    coinvariantImage P ≤ W ↔ ∀ v : V, W.mkQ (P v) = W.mkQ v := by
  constructor
  · intro h v
    rw [Submodule.mkQ_apply, Submodule.mkQ_apply, Submodule.Quotient.eq]
    exact h (LinearMap.mem_range_self _ v)
  · intro h x hx
    rcases hx with ⟨v, rfl⟩
    have hmk := h v
    rw [Submodule.mkQ_apply, Submodule.mkQ_apply, Submodule.Quotient.eq] at hmk
    simpa [loopDeviation_apply] using hmk

theorem map_eq_of_coinvariant_le (P : V ≃ₗ[K] V) {W : Submodule K V}
    (h : coinvariantImage P ≤ W) : W.map P.toLinearMap = W := by
  apply le_antisymm
  · intro x hx
    rcases hx with ⟨w, hw, rfl⟩
    have hdev : P w - w ∈ W := by
      have := h (LinearMap.mem_range_self (loopDeviation P) w)
      simpa [loopDeviation_apply] using this
    have hsum : (P w - w) + w ∈ W := W.add_mem hdev hw
    simpa [sub_add_cancel] using hsum
  · intro w hw
    refine ⟨P.symm w, ?_, by simp⟩
    have hdev : P.symm w - w ∈ W := by
      have hsym : coinvariantImage P.symm ≤ W := by
        simpa [coinvariantImage_symm P] using h
      have := hsym (LinearMap.mem_range_self (loopDeviation P.symm) w)
      simpa [loopDeviation_apply] using this
    have hsum : (P.symm w - w) + w ∈ W := W.add_mem hdev hw
    simpa [sub_add_cancel] using hsum

theorem comap_eq_of_coinvariant_le (P : V ≃ₗ[K] V) {W : Submodule K V}
    (h : coinvariantImage P ≤ W) : Submodule.comap P.toLinearMap W = W := by
  apply le_antisymm
  · intro v hv
    have hPv : P v ∈ W := by simpa [Submodule.mem_comap] using hv
    have hdev : P v - v ∈ W := by
      have := h (LinearMap.mem_range_self (loopDeviation P) v)
      simpa [loopDeviation_apply] using this
    have hsub : P v - (P v - v) ∈ W := W.sub_mem hPv hdev
    have hEq : P v - (P v - v) = v := by abel
    rwa [hEq] at hsub
  · intro v hv
    rw [Submodule.mem_comap]
    have hmap : W.map P.toLinearMap = W := map_eq_of_coinvariant_le P h
    rw [← hmap]
    exact ⟨v, hv, rfl⟩

/-- Replacing a pull `T` by `P ∘ T` does not change the preimage of a loop-invariant `W`. -/
theorem comap_trans_loop (P : V ≃ₗ[K] V) {V' : Type*} [AddCommGroup V'] [Module K V']
    (T : V' ≃ₗ[K] V) {W : Submodule K V} (h : coinvariantImage P ≤ W) :
    Submodule.comap (T.trans P).toLinearMap W = Submodule.comap T.toLinearMap W := by
  have hcomp : (T.trans P).toLinearMap = P.toLinearMap.comp T.toLinearMap := by
    ext v
    simp [LinearEquiv.trans_apply]
  rw [hcomp, Submodule.comap_comp, comap_eq_of_coinvariant_le P h]

/-! ## 3. Finite saturation (11.3) -/

variable {ι : Type*}

/-- One saturation step: `W + ∑_y S_y (B_y⁻¹ W)`. -/
def saturationSum (B S : ι → U →ₗ[K] V) (W : Submodule K V) : Submodule K V :=
  ⨆ i, (Submodule.comap (B i) W).map (S i)

def saturationStep (B S : ι → U →ₗ[K] V) (W : Submodule K V) : Submodule K V :=
  W ⊔ saturationSum B S W

def saturationIter (B S : ι → U →ₗ[K] V) : ℕ → Submodule K V → Submodule K V :=
  fun n W => Nat.rec W (fun _ prev => saturationStep B S prev) n

@[simp] theorem saturationIter_zero (B S : ι → U →ₗ[K] V) (W : Submodule K V) :
    saturationIter B S 0 W = W := rfl

@[simp] theorem saturationIter_succ (B S : ι → U →ₗ[K] V) (n : ℕ) (W : Submodule K V) :
    saturationIter B S (n + 1) W = saturationStep B S (saturationIter B S n W) := rfl

theorem saturationStep_self_le (B S : ι → U →ₗ[K] V) (W : Submodule K V) :
    W ≤ saturationStep B S W :=
  le_sup_left

theorem saturationStep_monotone (B S : ι → U →ₗ[K] V) :
    Monotone (saturationStep B S) := by
  intro W W' hW
  unfold saturationStep saturationSum
  refine sup_le_sup hW ?_
  refine iSup_le fun i => ?_
  refine le_trans ?_ (le_iSup (fun j => (Submodule.comap (B j) W').map (S j)) i)
  intro v hv
  rcases hv with ⟨u, hu, rfl⟩
  refine ⟨u, ?_, rfl⟩
  exact hW hu

theorem saturationIter_le_succ (B S : ι → U →ₗ[K] V) (n : ℕ) (W : Submodule K V) :
    saturationIter B S n W ≤ saturationIter B S (n + 1) W := by
  induction n with
  | zero =>
      simpa using saturationStep_self_le B S W
  | succ n ih =>
      simpa using saturationStep_monotone B S ih

theorem saturationIter_W0_le (B S : ι → U →ₗ[K] V) (n : ℕ) (W0 : Submodule K V) :
    W0 ≤ saturationIter B S n W0 := by
  induction n with
  | zero => simp
  | succ n ih =>
      exact le_trans ih (saturationIter_le_succ B S n W0)

theorem saturationStep_eq_self_iff (B S : ι → U →ₗ[K] V) (W : Submodule K V) :
    saturationStep B S W = W ↔ ∀ i, (Submodule.comap (B i) W).map (S i) ≤ W := by
  constructor
  · intro h i
    have hle : (Submodule.comap (B i) W).map (S i) ≤ saturationStep B S W :=
      le_trans (le_iSup (fun i => (Submodule.comap (B i) W).map (S i)) i) le_sup_right
    simpa [h] using hle
  · intro h
    exact le_antisymm (sup_le le_rfl (iSup_le h)) le_sup_left

/-- Equal finite dimension means the monotone step is already a fixed point. -/
theorem saturationStep_eq_of_finrank_eq [FiniteDimensional K V]
    (B S : ι → U →ₗ[K] V) (W : Submodule K V)
    (h : finrank K W = finrank K (saturationStep B S W)) :
    saturationStep B S W = W := by
  by_contra hne
  have hlt : W < saturationStep B S W :=
    lt_of_le_of_ne (saturationStep_self_le B S W) (Ne.symm hne)
  exact ne_of_lt (Submodule.finrank_strictMono hlt) h

theorem saturationIter_le_of_fixed (B S : ι → U →ₗ[K] V)
    {W0 W : Submodule K V} (h0 : W0 ≤ W) (hW : saturationStep B S W = W) :
    ∀ n, saturationIter B S n W0 ≤ W := by
  intro n
  induction n with
  | zero => simpa using h0
  | succ n ih =>
      rw [saturationIter_succ]
      exact (saturationStep_monotone B S ih).trans hW.le

theorem saturationIter_propagate (B S : ι → U →ₗ[K] V) (k : ℕ) (W0 : Submodule K V)
    (h : saturationIter B S (k + 1) W0 = saturationIter B S k W0) :
    ∀ m ≥ k, saturationIter B S m W0 = saturationIter B S k W0 := by
  have hfixed : saturationStep B S (saturationIter B S k W0) =
      saturationIter B S k W0 := by
    simpa [saturationIter_succ] using h
  intro m hm
  obtain ⟨t, rfl⟩ := Nat.exists_eq_add_of_le hm
  induction t with
  | zero => simp
  | succ t ih =>
      have hle : k ≤ k + t := Nat.le_add_right k t
      rw [Nat.add_succ, saturationIter_succ, ih hle]
      exact hfixed

private theorem nat_step_growth (d : ℕ → ℕ) (N : ℕ)
    (h : ∀ k ≤ N, d k + 1 ≤ d (k + 1)) :
    ∀ n ≤ N + 1, d 0 + n ≤ d n := by
  intro n hn
  induction n with
  | zero => simp
  | succ n ih =>
      have hnpred : n ≤ N + 1 := Nat.le_trans (Nat.le_succ n) hn
      have hnle : n ≤ N := Nat.succ_le_succ_iff.mp hn
      calc
        d 0 + (n + 1) = d 0 + n + 1 := (Nat.add_assoc (d 0) n 1).symm
        _ ≤ d n + 1 := Nat.add_le_add_right (ih hnpred) 1
        _ ≤ d (n + 1) := h n hnle

/-- The iteration stabilizes after at most `finrank K V` strict increases. -/
theorem exists_saturation_stabilizes [FiniteDimensional K V]
    (B S : ι → U →ₗ[K] V) (W0 : Submodule K V) :
    ∃ k ≤ finrank K V, saturationIter B S (k + 1) W0 = saturationIter B S k W0 := by
  let N := finrank K V
  by_contra h
  have hforall : ∀ k, k ≤ N → saturationIter B S (k + 1) W0 ≠ saturationIter B S k W0 := by
    intro k hk heq
    exact h ⟨k, hk, heq⟩
  have hstep : ∀ k ≤ N, finrank K (saturationIter B S k W0) + 1 ≤
      finrank K (saturationIter B S (k + 1) W0) := by
    intro k hk
    have hne : saturationIter B S (k + 1) W0 ≠ saturationIter B S k W0 := hforall k hk
    have hle : saturationIter B S k W0 ≤ saturationIter B S (k + 1) W0 :=
      saturationIter_le_succ B S k W0
    have hlt : saturationIter B S k W0 < saturationIter B S (k + 1) W0 :=
      lt_of_le_of_ne hle (Ne.symm hne)
    have hfin : finrank K (saturationIter B S k W0) <
        finrank K (saturationIter B S (k + 1) W0) :=
      Submodule.finrank_strictMono hlt
    exact Nat.succ_le_of_lt hfin
  have hgrow := nat_step_growth (fun n => finrank K (saturationIter B S n W0)) N hstep
  have htop : finrank K (saturationIter B S (N + 1) W0) ≤ N := by
    haveI : FiniteDimensional K V := inferInstance
    simpa [N] using
      (saturationIter B S (N + 1) W0).subtype.finrank_le_finrank_of_injective
        (Submodule.injective_subtype _)
  have hbig : N + 1 ≤ finrank K (saturationIter B S (N + 1) W0) := by
    have hsum := hgrow (N + 1) le_rfl
    exact le_trans (Nat.le_add_left (N + 1) (finrank K W0)) hsum
  exact Nat.not_succ_le_self N (hbig.trans htop)

/-- The iterate at `finrank` is a fixed point, and the least one above `W0`. -/
theorem saturationIter_finrank_fixed [FiniteDimensional K V]
    (B S : ι → U →ₗ[K] V) (W0 : Submodule K V) :
    saturationStep B S (saturationIter B S (finrank K V) W0) =
      saturationIter B S (finrank K V) W0 ∧
    ∀ W : Submodule K V, W0 ≤ W → saturationStep B S W = W →
      saturationIter B S (finrank K V) W0 ≤ W := by
  obtain ⟨k, hk, heq⟩ := exists_saturation_stabilizes B S W0
  have hprop := saturationIter_propagate B S k W0 heq (finrank K V) hk
  have hfixed : saturationStep B S (saturationIter B S (finrank K V) W0) =
      saturationIter B S (finrank K V) W0 := by
    rw [hprop]
    simpa [saturationIter_succ] using heq
  refine ⟨hfixed, ?_⟩
  intro W h0 hW
  exact saturationIter_le_of_fixed B S h0 hW (finrank K V)

theorem saturationStep_map_equiv (G : V ≃ₗ[K] V) (B S : ι → U →ₗ[K] V)
    (W : Submodule K V) :
    (saturationStep B S W).map G.toLinearMap =
      saturationStep (fun i => G.toLinearMap.comp (B i))
        (fun i => G.toLinearMap.comp (S i)) (W.map G.toLinearMap) := by
  unfold saturationStep saturationSum
  rw [Submodule.map_sup, Submodule.map_iSup]
  refine congrArg (fun M => (W.map G.toLinearMap) ⊔ M) ?_
  refine iSup_congr fun i => ?_
  have hpre :
      Submodule.comap (B i) W =
        Submodule.comap (G.toLinearMap.comp (B i)) (W.map G.toLinearMap) := by
    rw [Submodule.comap_comp]
    have hback : Submodule.comap G.toLinearMap (W.map G.toLinearMap) = W :=
      Submodule.comap_map_eq_of_injective G.injective W
    simp [hback]
  rw [← hpre, ← Submodule.map_comp]

theorem saturationIter_map_equiv (G : V ≃ₗ[K] V) (B S : ι → U →ₗ[K] V)
    (n : ℕ) (W : Submodule K V) :
    (saturationIter B S n W).map G.toLinearMap =
      saturationIter (fun i => G.toLinearMap.comp (B i))
        (fun i => G.toLinearMap.comp (S i)) n (W.map G.toLinearMap) := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [saturationIter_succ, saturationIter_succ, ← ih]
      exact saturationStep_map_equiv G B S _

theorem saturationStep_loop_invariant (P : V ≃ₗ[K] V) (B S : ι → U →ₗ[K] V)
    {W : Submodule K V} (hW : coinvariantImage P ≤ W) :
    saturationStep (fun i => P.toLinearMap.comp (B i))
      (fun i => P.toLinearMap.comp (S i)) W =
      saturationStep B S W := by
  have hcomap : ∀ i, Submodule.comap (P.toLinearMap.comp (B i)) W =
      Submodule.comap (B i) W := by
    intro i
    rw [Submodule.comap_comp, comap_eq_of_coinvariant_le P hW]
  have hdev : ∀ v : V, P v - v ∈ W := by
    intro v
    have := hW (LinearMap.mem_range_self (loopDeviation P) v)
    simpa [loopDeviation_apply] using this
  unfold saturationStep saturationSum
  apply le_antisymm
  · refine sup_le le_sup_left ?_
    refine iSup_le fun i => ?_
    rw [hcomap i]
    intro x hx
    rcases hx with ⟨u, hu, rfl⟩
    have hsplit : (P.toLinearMap.comp (S i)) u =
        S i u + (P (S i u) - S i u) := by
      simp [LinearMap.comp_apply, sub_eq_add_neg, add_comm]
    rw [hsplit]
    refine Submodule.add_mem _ ?_ ?_
    · exact (le_sup_right : saturationSum B S W ≤ W ⊔ saturationSum B S W)
        ((le_iSup (fun j => (Submodule.comap (B j) W).map (S j)) i) ⟨u, hu, rfl⟩)
    · exact (le_sup_left : W ≤ W ⊔ saturationSum B S W) (hdev (S i u))
  · refine sup_le le_sup_left ?_
    refine iSup_le fun i => ?_
    rw [← hcomap i]
    intro x hx
    rcases hx with ⟨u, hu, rfl⟩
    have hsplit : S i u =
        (P.toLinearMap.comp (S i)) u - (P (S i u) - S i u) := by
      simp [LinearMap.comp_apply, sub_eq_add_neg, add_comm]
    rw [hsplit]
    refine Submodule.sub_mem _ ?_ ?_
    · exact (le_sup_right :
          saturationSum (fun j => P.toLinearMap.comp (B j))
            (fun j => P.toLinearMap.comp (S j)) W ≤
          W ⊔ saturationSum (fun j => P.toLinearMap.comp (B j))
            (fun j => P.toLinearMap.comp (S j)) W)
        ((le_iSup (fun j =>
          (Submodule.comap (P.toLinearMap.comp (B j)) W).map
            (P.toLinearMap.comp (S j))) i) ⟨u, hu, rfl⟩)
    · exact (le_sup_left : W ≤ W ⊔ saturationSum (fun j => P.toLinearMap.comp (B j))
        (fun j => P.toLinearMap.comp (S j)) W) (hdev (S i u))

theorem saturationIter_loop_invariant (P : V ≃ₗ[K] V) (B S : ι → U →ₗ[K] V)
    (W0 : Submodule K V) (h0 : coinvariantImage P ≤ W0) :
    ∀ n, saturationIter (fun i => P.toLinearMap.comp (B i))
        (fun i => P.toLinearMap.comp (S i)) n W0 =
      saturationIter B S n W0 := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
      rw [saturationIter_succ, saturationIter_succ, ih]
      have hW : coinvariantImage P ≤ saturationIter B S n W0 := by
        exact le_trans h0 (by
          clear ih
          induction n with
          | zero => simp
          | succ n ih =>
              exact le_trans ih (saturationIter_le_succ B S n W0))
      exact saturationStep_loop_invariant P B S hW

/-- Theorem 4, in basepoint coordinates.

`W* = saturationIter (finrank) H` is a fixed point of (11.3). Every subspace
containing the coinvariant and closed under `S(B⁻¹ ·)` contains `W*`.
Loop preimages and a linear change of basepoint do not produce another
minimal family.
-/
theorem saturation_minimal_fixedPoint [FiniteDimensional K V]
    {loopIdx : Type*} (loops : loopIdx → V ≃ₗ[K] V) (B S : ι → U →ₗ[K] V) :
    let H := coinvariantSum loops
    let Wstar := saturationIter B S (finrank K V) H
    saturationStep B S Wstar = Wstar ∧
      (∀ i, (Submodule.comap (B i) Wstar).map (S i) ≤ Wstar) ∧
      (∀ j, coinvariantImage (loops j) ≤ Wstar) ∧
      ∀ W : Submodule K V, H ≤ W → (∀ i, (Submodule.comap (B i) W).map (S i) ≤ W) →
        Wstar ≤ W := by
  intro H Wstar
  obtain ⟨hfixed, hleast⟩ := saturationIter_finrank_fixed B S H
  have hHW : H ≤ Wstar := by
    simpa [H, Wstar] using saturationIter_W0_le B S (finrank K V) H
  refine ⟨hfixed, ?_, ?_, ?_⟩
  · intro i
    exact (saturationStep_eq_self_iff B S Wstar).1 hfixed i
  · intro j
    exact le_trans (le_iSup (fun j => coinvariantImage (loops j)) j) hHW
  · intro W hH hgraph
    have hstep : saturationStep B S W = W :=
      (saturationStep_eq_self_iff B S W).2 hgraph
    exact hleast W hH hstep

/-- `W = ⊤` is always a fixed point. A zero quotient therefore always exists.
This existence is not a classical-limit theorem. -/
theorem top_saturationStep (B S : ι → U →ₗ[K] V) :
    saturationStep B S ⊤ = ⊤ := by
  apply le_antisymm le_top
  exact le_sup_left

theorem top_contains_coinvariant (P : V ≃ₗ[K] V) : coinvariantImage P ≤ ⊤ := le_top

end

end D0.Geometry
