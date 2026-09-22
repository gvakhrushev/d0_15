import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Geometry.A4DSymRoleCentralDifference

namespace D0.Gravity

open D0
open D0.Geometry

/-!
This module owns one explicit finite Euclidean response seed.  It is an algebraic
construction on the already-owned role-phase group and symmetric role-tensor carrier.
It is not a continuum tensor, an Einstein tensor, a Lovelock tensor, or a uniqueness
statement.
-/

instance : Zero SymRoleTensor where
  zero :=
    { toMatrix := 0
      symmetric := by simp }

instance : Add SymRoleTensor where
  add A B :=
    { toMatrix := A.toMatrix + B.toMatrix
      symmetric := by
        intro a b
        simp only [Matrix.add_apply]
        rw [A.symmetric a b, B.symmetric a b] }

instance : SMul ℝ SymRoleTensor where
  smul c A :=
    { toMatrix := c • A.toMatrix
      symmetric := by
        intro a b
        simp only [Matrix.smul_apply]
        rw [A.symmetric a b] }

def tensorEntry (N : ℕ) (h : LocalSymRoleField N) (a b : Role) :
    ArchiveRolePhaseGroup N → ℝ :=
  fun x => (h x).toMatrix a b

def roleTrace (N : ℕ) (h : LocalSymRoleField N) :
    ArchiveRolePhaseGroup N → ℝ :=
  fun x => ∑ c, tensorEntry N h c c x

noncomputable def roleDivergence (N : ℕ) (h : LocalSymRoleField N) (b : Role) :
    ArchiveRolePhaseGroup N → ℝ :=
  ∑ c, centeredDifference N c (tensorEntry N h c b)

noncomputable def roleDoubleDivergence (N : ℕ) (h : LocalSymRoleField N) :
    ArchiveRolePhaseGroup N → ℝ :=
  ∑ c, centeredDifference N c
    (∑ d, centeredDifference N d (tensorEntry N h c d))

noncomputable def roleLaplacian (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) :
    ArchiveRolePhaseGroup N → ℝ :=
  ∑ c, centeredDifference N c (centeredDifference N c f)

noncomputable def roleTensorLaplacian (N : ℕ) (h : LocalSymRoleField N) (a b : Role) :
    ArchiveRolePhaseGroup N → ℝ :=
  roleLaplacian N (tensorEntry N h a b)

def roleDelta (a b : Role) : ℝ := if a = b then 1 else 0

noncomputable def responseEntry (N : ℕ) (h : LocalSymRoleField N) (a b : Role) :
    ArchiveRolePhaseGroup N → ℝ :=
  roleTensorLaplacian N h a b
    - centeredDifference N a (roleDivergence N h b)
    - centeredDifference N b (roleDivergence N h a)
    + centeredDifference N a (centeredDifference N b (roleTrace N h))
    + roleDelta a b • roleDoubleDivergence N h
    - roleDelta a b • roleLaplacian N (roleTrace N h)

/-- One explicit finite Euclidean local metric-response seed. -/
noncomputable def finiteResponse (N : ℕ) (h : LocalSymRoleField N) :
    LocalSymRoleField N :=
  fun x =>
    { toMatrix := fun a b => responseEntry N h a b x
      symmetric := by
        intro a b
        unfold responseEntry
        have hab : tensorEntry N h a b = tensorEntry N h b a := by
          funext y
          exact (h y).symmetric a b
        have hlab : roleTensorLaplacian N h a b = roleTensorLaplacian N h b a := by
          unfold roleTensorLaplacian
          rw [hab]
        rw [hlab]
        have hcomm := centeredDifference_comm N a b (roleTrace N h)
        simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply]
        rw [congrArg (fun f => f x) hcomm]
        have hdelta : roleDelta a b = roleDelta b a := by
          unfold roleDelta
          by_cases hab' : a = b
          · subst b
            rfl
          · have hba' : b ≠ a := Ne.symm hab'
            simp [hab', hba']
        rw [hdelta]
        ring }

theorem finiteResponse_entry (N : ℕ) (h : LocalSymRoleField N)
    (x : ArchiveRolePhaseGroup N) (a b : Role) :
    (finiteResponse N h x).toMatrix a b = responseEntry N h a b x := rfl

theorem finiteResponse_sitewise_symmetric (N : ℕ) (h : LocalSymRoleField N)
    (x : ArchiveRolePhaseGroup N) (a b : Role) :
    (finiteResponse N h x).toMatrix a b =
      (finiteResponse N h x).toMatrix b a :=
  (finiteResponse N h x).symmetric a b

theorem roleLaplacian_apply (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ)
    (x : ArchiveRolePhaseGroup N) :
    roleLaplacian N f x =
      ∑ c, centeredDifference N c (centeredDifference N c f) x := by
  rfl

theorem roleTrace_apply (N : ℕ) (h : LocalSymRoleField N)
    (x : ArchiveRolePhaseGroup N) :
    roleTrace N h x = ∑ c, (h x).toMatrix c c := by
  rfl

theorem roleDivergence_apply (N : ℕ) (h : LocalSymRoleField N) (b : Role)
    (x : ArchiveRolePhaseGroup N) :
    roleDivergence N h b x =
      ∑ c, centeredDifference N c (tensorEntry N h c b) x := by
  rfl

theorem roleDoubleDivergence_apply (N : ℕ) (h : LocalSymRoleField N)
    (x : ArchiveRolePhaseGroup N) :
    roleDoubleDivergence N h x =
      ∑ c, ∑ d, centeredDifference N c
        (centeredDifference N d (tensorEntry N h c d)) x := by
  change (∑ c, centeredDifference N c
      (∑ d, centeredDifference N d (tensorEntry N h c d))) x = _
  rw [Finset.sum_apply]
  apply Finset.sum_congr rfl
  intro c hc
  exact congrFun (map_sum (centeredDifference N c)
    (fun d => centeredDifference N d (tensorEntry N h c d)) Finset.univ) x

theorem centeredDifference_sum (N : ℕ) (r : Role)
    (F : Role → ArchiveRolePhaseGroup N → ℝ) :
    centeredDifference N r (∑ c, F c) =
      ∑ c, centeredDifference N r (F c) := by
  exact map_sum (centeredDifference N r) F Finset.univ

theorem centeredDifference_sub (N : ℕ) (r : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    centeredDifference N r (f - g) =
      centeredDifference N r f - centeredDifference N r g :=
  (centeredDifference N r).map_sub f g

noncomputable def vectorDivergence (N : ℕ) (xi : LocalRoleVector N) :
    ArchiveRolePhaseGroup N → ℝ :=
  ∑ c, centeredDifference N c (fun x => xi x c)

theorem symmetricRoleGradient_tensorEntry (N : ℕ) (xi : LocalRoleVector N)
    (a b : Role) :
    tensorEntry N (symmetricRoleGradient N xi) a b =
      centeredDifference N a (fun x => xi x b) +
        centeredDifference N b (fun x => xi x a) := by
  funext x
  exact symmetricRoleGradient_entry N xi x a b

theorem roleDoubleDivergence_eq_divergence (N : ℕ) (h : LocalSymRoleField N) :
    roleDoubleDivergence N h =
      ∑ c, centeredDifference N c (roleDivergence N h c) := by
  unfold roleDoubleDivergence roleDivergence
  apply Finset.sum_congr rfl
  intro c hc
  rw [centeredDifference_sum, centeredDifference_sum]
  apply Finset.sum_congr rfl
  intro d hd
  have hentry : tensorEntry N h c d = tensorEntry N h d c := by
    funext x
    exact (h x).symmetric c d
  rw [hentry]

theorem centeredDifference_roleDelta_sum (N : ℕ) (b : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    (∑ a, centeredDifference N a (roleDelta a b • f)) =
      centeredDifference N b f := by
  classical
  rw [Finset.sum_eq_single b]
  · simp [roleDelta]
  · intro a ha hab
    simp [roleDelta, hab]
  · simp

theorem roleTrace_symmetricRoleGradient (N : ℕ) (xi : LocalRoleVector N) :
    roleTrace N (symmetricRoleGradient N xi) =
      (2 : ℝ) • vectorDivergence N xi := by
  funext x
  unfold roleTrace vectorDivergence tensorEntry
  simp only [Finset.sum_apply, symmetricRoleGradient_entry, Pi.smul_apply]
  rw [Finset.sum_add_distrib]
  ring_nf

theorem roleLaplacian_add (N : ℕ) (f g : ArchiveRolePhaseGroup N → ℝ) :
    roleLaplacian N (f + g) = roleLaplacian N f + roleLaplacian N g := by
  unfold roleLaplacian
  simp_rw [centeredDifference_add]
  rw [Finset.sum_add_distrib]

theorem roleLaplacian_smul (N : ℕ) (c : ℝ)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    roleLaplacian N (c • f) = c • roleLaplacian N f := by
  unfold roleLaplacian
  simp_rw [centeredDifference_smul]
  rw [← Finset.smul_sum]

theorem roleLaplacian_centeredDifference_comm (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    centeredDifference N r (roleLaplacian N f) =
      roleLaplacian N (centeredDifference N r f) := by
  unfold roleLaplacian
  rw [centeredDifference_sum]
  apply Finset.sum_congr rfl
  intro c hc
  calc
    centeredDifference N r (centeredDifference N c
        (centeredDifference N c f)) =
        centeredDifference N c (centeredDifference N r
          (centeredDifference N c f)) := centeredDifference_comm N r c _
    _ = centeredDifference N c (centeredDifference N c
          (centeredDifference N r f)) := by
      rw [centeredDifference_comm N r c f]

theorem roleLaplacian_sum (N : ℕ)
    (F : Role → ArchiveRolePhaseGroup N → ℝ) :
    roleLaplacian N (∑ c, F c) =
      ∑ c, roleLaplacian N (F c) := by
  unfold roleLaplacian
  simp_rw [centeredDifference_sum]
  rw [Finset.sum_comm]

theorem roleDivergence_symmetricRoleGradient (N : ℕ) (xi : LocalRoleVector N)
    (b : Role) :
    roleDivergence N (symmetricRoleGradient N xi) b =
      roleLaplacian N (fun x => xi x b) +
        centeredDifference N b (vectorDivergence N xi) := by
  unfold roleDivergence
  have hsplit :
      (∑ c, centeredDifference N c
          (tensorEntry N (symmetricRoleGradient N xi) c b)) =
        ∑ c, (centeredDifference N c (centeredDifference N c
            (fun x => xi x b)) +
          centeredDifference N c (centeredDifference N b
            (fun x => xi x c))) := by
    apply Finset.sum_congr rfl
    intro c hc
    rw [symmetricRoleGradient_tensorEntry, centeredDifference_add]
  rw [hsplit, Finset.sum_add_distrib]
  have hcomm :
      (∑ c, centeredDifference N c (centeredDifference N b
        (fun x => xi x c))) =
        ∑ c, centeredDifference N b (centeredDifference N c
          (fun x => xi x c)) := by
    apply Finset.sum_congr rfl
    intro c hc
    exact centeredDifference_comm N c b (fun x => xi x c)
  calc
    (∑ c, centeredDifference N c (centeredDifference N c
        (fun x => xi x b))) +
        ∑ c, centeredDifference N c (centeredDifference N b
          (fun x => xi x c)) =
      roleLaplacian N (fun x => xi x b) +
        ∑ c, centeredDifference N c (centeredDifference N b
          (fun x => xi x c)) := by rfl
    _ = roleLaplacian N (fun x => xi x b) +
        centeredDifference N b (vectorDivergence N xi) := by
      rw [hcomm, ← centeredDifference_sum]
      rfl

theorem roleTensorLaplacian_symmetricRoleGradient (N : ℕ)
    (xi : LocalRoleVector N) (a b : Role) :
    roleTensorLaplacian N (symmetricRoleGradient N xi) a b =
      centeredDifference N a (roleLaplacian N (fun x => xi x b)) +
        centeredDifference N b (roleLaplacian N (fun x => xi x a)) := by
  unfold roleTensorLaplacian
  rw [symmetricRoleGradient_tensorEntry, roleLaplacian_add,
    roleLaplacian_centeredDifference_comm,
    roleLaplacian_centeredDifference_comm]

theorem roleDoubleDivergence_symmetricRoleGradient (N : ℕ)
    (xi : LocalRoleVector N) :
    roleDoubleDivergence N (symmetricRoleGradient N xi) =
      (2 : ℝ) • roleLaplacian N (vectorDivergence N xi) := by
  rw [roleDoubleDivergence_eq_divergence]
  simp_rw [roleDivergence_symmetricRoleGradient, centeredDifference_add]
  rw [Finset.sum_add_distrib]
  have hfirst :
      (∑ c, centeredDifference N c
        (roleLaplacian N (fun x => xi x c))) =
        ∑ c, roleLaplacian N
          (centeredDifference N c (fun x => xi x c)) := by
    apply Finset.sum_congr rfl
    intro c hc
    exact roleLaplacian_centeredDifference_comm N c (fun x => xi x c)
  rw [hfirst, ← roleLaplacian_sum]
  change roleLaplacian N (vectorDivergence N xi) +
      roleLaplacian N (vectorDivergence N xi) = _
  funext x
  simp only [Pi.add_apply, Pi.smul_apply]
  ring

theorem finiteResponse_gauge_nullity (N : ℕ) (xi : LocalRoleVector N) :
    finiteResponse N (symmetricRoleGradient N xi) = 0 := by
  funext x
  apply SymRoleTensor.ext
  funext a b
  rw [finiteResponse_entry]
  change responseEntry N (symmetricRoleGradient N xi) a b x = 0
  unfold responseEntry
  have hL := roleTensorLaplacian_symmetricRoleGradient N xi a b
  have hDa := roleDivergence_symmetricRoleGradient N xi b
  have hDb := roleDivergence_symmetricRoleGradient N xi a
  have ht := roleTrace_symmetricRoleGradient N xi
  have hq := roleDoubleDivergence_symmetricRoleGradient N xi
  have hH :
      centeredDifference N a (centeredDifference N b
        ((2 : ℝ) • vectorDivergence N xi)) =
        (2 : ℝ) • centeredDifference N a (centeredDifference N b
          (vectorDivergence N xi)) := by
    calc
      centeredDifference N a (centeredDifference N b
          ((2 : ℝ) • vectorDivergence N xi)) =
          centeredDifference N a ((2 : ℝ) •
            centeredDifference N b (vectorDivergence N xi)) := by
              rw [centeredDifference_smul]
      _ = (2 : ℝ) • centeredDifference N a
          (centeredDifference N b (vectorDivergence N xi)) := by
            rw [centeredDifference_smul]
  have hLT :
      roleLaplacian N ((2 : ℝ) • vectorDivergence N xi) =
        (2 : ℝ) • roleLaplacian N (vectorDivergence N xi) :=
    roleLaplacian_smul N 2 (vectorDivergence N xi)
  have hDaAdd :
      centeredDifference N a
          (roleLaplacian N (fun x => xi x b) +
            centeredDifference N b (vectorDivergence N xi)) =
        centeredDifference N a (roleLaplacian N (fun x => xi x b)) +
          centeredDifference N a (centeredDifference N b
            (vectorDivergence N xi)) :=
    centeredDifference_add N a _ _
  have hDbAdd :
      centeredDifference N b
          (roleLaplacian N (fun x => xi x a) +
            centeredDifference N a (vectorDivergence N xi)) =
        centeredDifference N b (roleLaplacian N (fun x => xi x a)) +
          centeredDifference N b (centeredDifference N a
            (vectorDivergence N xi)) :=
    centeredDifference_add N b _ _
  rw [hL, hDa, hDb, ht, hq]
  simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply]
  rw [congrArg (fun f => f x) hH, congrArg (fun f => f x) hLT,
    congrArg (fun f => f x) hDaAdd, congrArg (fun f => f x) hDbAdd]
  simp only [Pi.add_apply, Pi.smul_apply]
  have hcomm := centeredDifference_comm N a b (vectorDivergence N xi)
  rw [congrArg (fun f => f x) hcomm]
  ring

theorem finiteResponse_divergence_free (N : ℕ) (h : LocalSymRoleField N)
    (b : Role) :
  roleDivergence N (finiteResponse N h) b = 0 := by
  unfold roleDivergence
  unfold tensorEntry
  simp_rw [finiteResponse_entry]
  have hA :
      (∑ a, centeredDifference N a
        (roleTensorLaplacian N h a b)) =
        roleLaplacian N (roleDivergence N h b) := by
    unfold roleTensorLaplacian
    calc
      (∑ a, centeredDifference N a
          (roleLaplacian N (tensorEntry N h a b))) =
          ∑ a, roleLaplacian N
            (centeredDifference N a (tensorEntry N h a b)) := by
        apply Finset.sum_congr rfl
        intro a ha
        exact roleLaplacian_centeredDifference_comm N a
          (tensorEntry N h a b)
      _ = roleLaplacian N (∑ a,
          centeredDifference N a (tensorEntry N h a b)) := by
        rw [roleLaplacian_sum]
      _ = roleLaplacian N (roleDivergence N h b) := by rfl
  have hB :
      (∑ a, centeredDifference N a
        (centeredDifference N a (roleDivergence N h b))) =
        roleLaplacian N (roleDivergence N h b) := by
    rfl
  have hC :
      (∑ a, centeredDifference N a
        (centeredDifference N b (roleDivergence N h a))) =
        centeredDifference N b (roleDoubleDivergence N h) := by
    calc
      (∑ a, centeredDifference N a
          (centeredDifference N b (roleDivergence N h a))) =
          ∑ a, centeredDifference N b
            (centeredDifference N a (roleDivergence N h a)) := by
        apply Finset.sum_congr rfl
        intro a ha
        exact centeredDifference_comm N a b (roleDivergence N h a)
      _ = centeredDifference N b
          (∑ a, centeredDifference N a (roleDivergence N h a)) := by
        rw [centeredDifference_sum]
      _ = centeredDifference N b (roleDoubleDivergence N h) := by
        rw [roleDoubleDivergence_eq_divergence]
  have hD :
      (∑ a, centeredDifference N a
        (centeredDifference N a (centeredDifference N b (roleTrace N h)))) =
        centeredDifference N b (roleLaplacian N (roleTrace N h)) := by
    calc
      (∑ a, centeredDifference N a
          (centeredDifference N a (centeredDifference N b (roleTrace N h)))) =
          roleLaplacian N (centeredDifference N b (roleTrace N h)) := by rfl
      _ = centeredDifference N b (roleLaplacian N (roleTrace N h)) := by
        exact (roleLaplacian_centeredDifference_comm N b
          (roleTrace N h)).symm
  have hexpand :
      (∑ a, centeredDifference N a (responseEntry N h a b)) =
        ∑ a, (centeredDifference N a
              (roleTensorLaplacian N h a b) -
            centeredDifference N a
              (centeredDifference N a (roleDivergence N h b)) -
            centeredDifference N a
              (centeredDifference N b (roleDivergence N h a)) +
            centeredDifference N a
              (centeredDifference N a
                (centeredDifference N b (roleTrace N h))) +
            centeredDifference N a (roleDelta a b •
              roleDoubleDivergence N h) -
            centeredDifference N a (roleDelta a b •
              roleLaplacian N (roleTrace N h))) := by
    apply Finset.sum_congr rfl
    intro a ha
    unfold responseEntry
    simp only [centeredDifference_sub, centeredDifference_add]
  rw [hexpand]
  simp only [Finset.sum_sub_distrib]
  simp only [Finset.sum_sub_distrib, Finset.sum_add_distrib]
  rw [hA, hB, hC, hD, centeredDifference_roleDelta_sum,
    centeredDifference_roleDelta_sum]
  ring

@[simp] theorem tensorEntry_zero (N : ℕ) (a b : Role)
    (x : ArchiveRolePhaseGroup N) :
    tensorEntry N (0 : LocalSymRoleField N) a b x = 0 := rfl

@[simp] theorem tensorEntry_add (N : ℕ) (h k : LocalSymRoleField N)
    (a b : Role) (x : ArchiveRolePhaseGroup N) :
    tensorEntry N (h + k) a b x =
      tensorEntry N h a b x + tensorEntry N k a b x := by
  rfl

@[simp] theorem tensorEntry_smul (N : ℕ) (c : ℝ) (h : LocalSymRoleField N)
    (a b : Role) (x : ArchiveRolePhaseGroup N) :
    tensorEntry N (c • h) a b x = c * tensorEntry N h a b x := by
  rfl

theorem roleTrace_add (N : ℕ) (h k : LocalSymRoleField N) :
    roleTrace N (h + k) = roleTrace N h + roleTrace N k := by
  funext x
  unfold roleTrace
  simp_rw [tensorEntry_add]
  simp only [Pi.add_apply]
  rw [Finset.sum_add_distrib]

theorem roleTrace_smul (N : ℕ) (c : ℝ) (h : LocalSymRoleField N) :
    roleTrace N (c • h) = c • roleTrace N h := by
  funext x
  unfold roleTrace
  simp_rw [tensorEntry_smul]
  change (∑ d, c * tensorEntry N h d d x) =
    c * ∑ d, tensorEntry N h d d x
  rw [Finset.mul_sum]

theorem roleDivergence_add (N : ℕ) (h k : LocalSymRoleField N) (b : Role) :
    roleDivergence N (h + k) b =
      roleDivergence N h b + roleDivergence N k b := by
  have hentry : ∀ c : Role, tensorEntry N (h + k) c b =
      tensorEntry N h c b + tensorEntry N k c b := by
    intro c
    funext x
    exact tensorEntry_add N h k c b x
  unfold roleDivergence
  simp_rw [hentry, centeredDifference_add]
  rw [Finset.sum_add_distrib]

theorem roleDivergence_smul (N : ℕ) (c : ℝ) (h : LocalSymRoleField N) (b : Role) :
    roleDivergence N (c • h) b = c • roleDivergence N h b := by
  have hentry : ∀ d : Role, tensorEntry N (c • h) d b =
      c • tensorEntry N h d b := by
    intro d
    funext x
    simpa only [Pi.smul_apply] using tensorEntry_smul N c h d b x
  unfold roleDivergence
  simp_rw [hentry, centeredDifference_smul]
  rw [Finset.smul_sum]

theorem roleDoubleDivergence_add (N : ℕ) (h k : LocalSymRoleField N) :
    roleDoubleDivergence N (h + k) =
      roleDoubleDivergence N h + roleDoubleDivergence N k := by
  have hentry : ∀ c d : Role, tensorEntry N (h + k) c d =
      tensorEntry N h c d + tensorEntry N k c d := by
    intro c d
    funext x
    exact tensorEntry_add N h k c d x
  unfold roleDoubleDivergence
  simp_rw [hentry, centeredDifference_add]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro c hc
  rw [Finset.sum_add_distrib, centeredDifference_add]

theorem roleDoubleDivergence_smul (N : ℕ) (c : ℝ) (h : LocalSymRoleField N) :
    roleDoubleDivergence N (c • h) = c • roleDoubleDivergence N h := by
  have hentry : ∀ a b : Role, tensorEntry N (c • h) a b =
      c • tensorEntry N h a b := by
    intro a b
    funext x
    simpa only [Pi.smul_apply] using tensorEntry_smul N c h a b x
  unfold roleDoubleDivergence
  simp_rw [hentry, centeredDifference_smul]
  rw [Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro d hd
  rw [← Finset.smul_sum, centeredDifference_smul]

theorem roleTensorLaplacian_add (N : ℕ) (h k : LocalSymRoleField N)
    (a b : Role) :
    roleTensorLaplacian N (h + k) a b =
      roleTensorLaplacian N h a b + roleTensorLaplacian N k a b := by
  have hentry : tensorEntry N (h + k) a b =
      tensorEntry N h a b + tensorEntry N k a b := by
    funext x
    exact tensorEntry_add N h k a b x
  unfold roleTensorLaplacian
  rw [hentry, roleLaplacian_add]

theorem roleTensorLaplacian_smul (N : ℕ) (c : ℝ) (h : LocalSymRoleField N)
    (a b : Role) :
    roleTensorLaplacian N (c • h) a b =
      c • roleTensorLaplacian N h a b := by
  have hentry : tensorEntry N (c • h) a b =
      c • tensorEntry N h a b := by
    funext x
    exact tensorEntry_smul N c h a b x
  unfold roleTensorLaplacian
  rw [hentry, roleLaplacian_smul]

theorem responseEntry_add (N : ℕ) (h k : LocalSymRoleField N)
    (a b : Role) :
    responseEntry N (h + k) a b =
      responseEntry N h a b + responseEntry N k a b := by
  funext x
  unfold responseEntry
  rw [roleTensorLaplacian_add, roleDivergence_add, roleDivergence_add,
    roleTrace_add, roleDoubleDivergence_add, roleLaplacian_add]
  simp_rw [centeredDifference_add]
  simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply]
  ring

theorem responseEntry_smul (N : ℕ) (c : ℝ) (h : LocalSymRoleField N)
    (a b : Role) :
    responseEntry N (c • h) a b =
      c • responseEntry N h a b := by
  funext x
  unfold responseEntry
  rw [roleTensorLaplacian_smul, roleDivergence_smul, roleDivergence_smul,
    roleTrace_smul, roleDoubleDivergence_smul, roleLaplacian_smul]
  simp_rw [centeredDifference_smul]
  simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply]
  ring

theorem finiteResponse_add (N : ℕ) (h k : LocalSymRoleField N) :
    finiteResponse N (h + k) =
      finiteResponse N h + finiteResponse N k := by
  funext x
  apply SymRoleTensor.ext
  funext a b
  rw [finiteResponse_entry]
  change responseEntry N (h + k) a b x =
    responseEntry N h a b x + responseEntry N k a b x
  exact congrFun (responseEntry_add N h k a b) x

theorem finiteResponse_smul (N : ℕ) (c : ℝ) (h : LocalSymRoleField N) :
    finiteResponse N (c • h) =
      c • finiteResponse N h := by
  funext x
  apply SymRoleTensor.ext
  funext a b
  rw [finiteResponse_entry]
  change responseEntry N (c • h) a b x =
    c * responseEntry N h a b x
  exact congrFun (responseEntry_smul N c h a b) x

def scalarInnerProduct (N : ℕ)
    (f g : ArchiveRolePhaseGroup N → ℝ) : ℝ :=
  ∑ x, f x * g x

def roleVectorInnerProduct (N : ℕ) (xi eta : LocalRoleVector N) : ℝ :=
  ∑ b, scalarInnerProduct N (fun x => xi x b) (fun x => eta x b)

noncomputable def divergenceVector (N : ℕ) (h : LocalSymRoleField N) : LocalRoleVector N :=
  fun x b => roleDivergence N h b x

def tensorInnerProduct (N : ℕ)
    (h k : LocalSymRoleField N) : ℝ :=
  ∑ a, ∑ b, scalarInnerProduct N
    (tensorEntry N h a b) (tensorEntry N k a b)

theorem scalarInnerProduct_symm (N : ℕ)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N f g = scalarInnerProduct N g f := by
  unfold scalarInnerProduct
  apply Finset.sum_congr rfl
  intro x hx
  ring

theorem roleVectorInnerProduct_symm (N : ℕ)
    (xi eta : LocalRoleVector N) :
    roleVectorInnerProduct N xi eta = roleVectorInnerProduct N eta xi := by
  unfold roleVectorInnerProduct
  apply Finset.sum_congr rfl
  intro b hb
  exact scalarInnerProduct_symm N _ _

theorem tensorInnerProduct_symm (N : ℕ)
    (h k : LocalSymRoleField N) :
    tensorInnerProduct N h k = tensorInnerProduct N k h := by
  unfold tensorInnerProduct
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  exact scalarInnerProduct_symm N _ _

theorem scalarInnerProduct_add_right (N : ℕ)
    (f g k : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N f (g + k) =
      scalarInnerProduct N f g + scalarInnerProduct N f k := by
  unfold scalarInnerProduct
  simp only [Pi.add_apply, mul_add]
  rw [Finset.sum_add_distrib]

theorem scalarInnerProduct_sub_right (N : ℕ)
    (f g k : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N f (g - k) =
      scalarInnerProduct N f g - scalarInnerProduct N f k := by
  unfold scalarInnerProduct
  simp only [Pi.sub_apply, mul_sub]
  rw [Finset.sum_sub_distrib]

theorem scalarInnerProduct_smul_right (N : ℕ) (c : ℝ)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N f (c • g) =
      c * scalarInnerProduct N f g := by
  unfold scalarInnerProduct
  simp only [Pi.smul_apply]
  calc
    (∑ x, f x * (c * g x)) =
        ∑ x, c * (f x * g x) := by
      apply Finset.sum_congr rfl
      intro x hx
      ring
    _ = c * ∑ x, f x * g x := by
      rw [Finset.mul_sum]

theorem scalarInnerProduct_add_left (N : ℕ)
    (f g k : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N (f + g) k =
      scalarInnerProduct N f k + scalarInnerProduct N g k := by
  calc
    scalarInnerProduct N (f + g) k =
        scalarInnerProduct N k (f + g) := scalarInnerProduct_symm N _ _
    _ = scalarInnerProduct N k f + scalarInnerProduct N k g :=
      scalarInnerProduct_add_right N k f g
    _ = scalarInnerProduct N f k + scalarInnerProduct N g k := by
      rw [scalarInnerProduct_symm N k f, scalarInnerProduct_symm N k g]

theorem scalarInnerProduct_sub_left (N : ℕ)
    (f g k : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N (f - g) k =
      scalarInnerProduct N f k - scalarInnerProduct N g k := by
  calc
    scalarInnerProduct N (f - g) k =
        scalarInnerProduct N k (f - g) := scalarInnerProduct_symm N _ _
    _ = scalarInnerProduct N k f - scalarInnerProduct N k g :=
      scalarInnerProduct_sub_right N k f g
    _ = scalarInnerProduct N f k - scalarInnerProduct N g k := by
      rw [scalarInnerProduct_symm N k f, scalarInnerProduct_symm N k g]

theorem scalarInnerProduct_smul_left (N : ℕ) (c : ℝ)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N (c • f) g =
      c * scalarInnerProduct N f g := by
  calc
    scalarInnerProduct N (c • f) g =
        scalarInnerProduct N g (c • f) := scalarInnerProduct_symm N _ _
    _ = c * scalarInnerProduct N g f :=
      scalarInnerProduct_smul_right N c g f
    _ = c * scalarInnerProduct N f g := by
      rw [scalarInnerProduct_symm N g f]

theorem scalarInnerProduct_sum_right (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ)
    (F : Role → ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N f (∑ c, F c) =
      ∑ c, scalarInnerProduct N f (F c) := by
  unfold scalarInnerProduct
  simp only [Finset.sum_apply]
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]

theorem scalarInnerProduct_sum_left (N : ℕ) (F : Role → ArchiveRolePhaseGroup N → ℝ)
    (g : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N (∑ c, F c) g =
      ∑ c, scalarInnerProduct N (F c) g := by
  rw [scalarInnerProduct_symm, scalarInnerProduct_sum_right]
  apply Finset.sum_congr rfl
  intro c hc
  exact scalarInnerProduct_symm N _ _

theorem scalarInnerProduct_centeredDifference (N : ℕ) (r : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N (centeredDifference N r f) g =
      -scalarInnerProduct N f (centeredDifference N r g) :=
  centeredDifference_skew_adjoint N r f g

theorem scalarInnerProduct_secondDifference (N : ℕ) (r s : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N (centeredDifference N r
      (centeredDifference N s f)) g =
      scalarInnerProduct N f (centeredDifference N s
        (centeredDifference N r g)) := by
  calc
    scalarInnerProduct N (centeredDifference N r
        (centeredDifference N s f)) g =
        -scalarInnerProduct N (centeredDifference N s f)
          (centeredDifference N r g) :=
      scalarInnerProduct_centeredDifference N r _ _
    _ = -(-scalarInnerProduct N f
        (centeredDifference N s (centeredDifference N r g))) := by
      rw [scalarInnerProduct_centeredDifference]
    _ = scalarInnerProduct N f
        (centeredDifference N s (centeredDifference N r g)) := by ring

theorem symmetricRoleGradient_adjoint (N : ℕ)
    (xi : LocalRoleVector N) (h : LocalSymRoleField N) :
    tensorInnerProduct N (symmetricRoleGradient N xi) h =
      -2 * roleVectorInnerProduct N xi (divergenceVector N h) := by
  have hexpand :
      tensorInnerProduct N (symmetricRoleGradient N xi) h =
        ∑ a, ∑ b,
          (-scalarInnerProduct N (fun x => xi x b)
              (centeredDifference N a (tensorEntry N h a b)) -
            scalarInnerProduct N (fun x => xi x a)
              (centeredDifference N b (tensorEntry N h a b))) := by
    unfold tensorInnerProduct
    apply Finset.sum_congr rfl
    intro a ha
    apply Finset.sum_congr rfl
    intro b hb
    rw [symmetricRoleGradient_tensorEntry,
      scalarInnerProduct_add_left,
      scalarInnerProduct_centeredDifference,
      scalarInnerProduct_centeredDifference]
    ring
  have hswap :
      (∑ a, ∑ b, scalarInnerProduct N (fun x => xi x b)
          (centeredDifference N a (tensorEntry N h a b))) =
        ∑ a, ∑ b, scalarInnerProduct N (fun x => xi x a)
          (centeredDifference N b (tensorEntry N h a b)) := by
    calc
      (∑ a, ∑ b, scalarInnerProduct N (fun x => xi x b)
          (centeredDifference N a (tensorEntry N h a b))) =
          ∑ a, ∑ b, scalarInnerProduct N (fun x => xi x b)
            (centeredDifference N a (tensorEntry N h b a)) := by
        apply Finset.sum_congr rfl
        intro a ha
        apply Finset.sum_congr rfl
        intro b hb
        have hsym : tensorEntry N h a b = tensorEntry N h b a := by
          funext x
          exact (h x).symmetric a b
        rw [hsym]
      _ = ∑ a, ∑ b, scalarInnerProduct N (fun x => xi x a)
          (centeredDifference N b (tensorEntry N h a b)) := by
        rw [Finset.sum_comm]
  rw [hexpand]
  simp_rw [Finset.sum_sub_distrib]
  have hcollapse :
      (∑ a, ∑ b, scalarInnerProduct N (fun x => xi x b)
          (centeredDifference N a (tensorEntry N h a b))) =
        roleVectorInnerProduct N xi (divergenceVector N h) := by
    unfold roleVectorInnerProduct divergenceVector
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro b hb
    rw [← scalarInnerProduct_sum_right]
    rfl
  have hcollapse2 :
      (∑ a, ∑ b, scalarInnerProduct N (fun x => xi x a)
          (centeredDifference N b (tensorEntry N h a b))) =
        roleVectorInnerProduct N xi (divergenceVector N h) := by
    rw [← hswap, hcollapse]
  have hneg1 :
      (∑ a, ∑ b, -scalarInnerProduct N (fun x => xi x b)
          (centeredDifference N a (tensorEntry N h a b))) =
        -roleVectorInnerProduct N xi (divergenceVector N h) := by
    calc
      (∑ a, ∑ b, -scalarInnerProduct N (fun x => xi x b)
          (centeredDifference N a (tensorEntry N h a b))) =
          ∑ a, -(∑ b, scalarInnerProduct N (fun x => xi x b)
            (centeredDifference N a (tensorEntry N h a b))) := by
        apply Finset.sum_congr rfl
        intro a ha
        rw [Finset.sum_neg_distrib]
      _ = -(∑ a, ∑ b, scalarInnerProduct N (fun x => xi x b)
          (centeredDifference N a (tensorEntry N h a b))) := by
        rw [Finset.sum_neg_distrib]
      _ = -roleVectorInnerProduct N xi (divergenceVector N h) := by
        rw [hcollapse]
  rw [hneg1, hcollapse2]
  ring

theorem scalarInnerProduct_laplacian_self (N : ℕ)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    scalarInnerProduct N f (roleLaplacian N g) =
      scalarInnerProduct N (roleLaplacian N f) g := by
  unfold roleLaplacian
  rw [scalarInnerProduct_sum_right]
  rw [scalarInnerProduct_sum_left]
  apply Finset.sum_congr rfl
  intro c hc
  exact (scalarInnerProduct_secondDifference N c c f g).symm

theorem tensorLaplacian_pairing_self (N : ℕ)
    (h k : LocalSymRoleField N) :
    (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
      (roleTensorLaplacian N k a b)) =
      ∑ a, ∑ b, scalarInnerProduct N
        (roleTensorLaplacian N h a b) (tensorEntry N k a b) := by
  unfold roleTensorLaplacian
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  exact scalarInnerProduct_laplacian_self N
    (tensorEntry N h a b) (tensorEntry N k a b)

theorem hessianTrace_pairing (N : ℕ)
    (h k : LocalSymRoleField N) :
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
      (centeredDifference N a (centeredDifference N b (roleTrace N k)))) =
      scalarInnerProduct N (roleDoubleDivergence N h) (roleTrace N k) := by
  change (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
      (centeredDifference N a (centeredDifference N b (roleTrace N k)))) =
      scalarInnerProduct N
        (∑ c, centeredDifference N c
          (∑ d, centeredDifference N d (tensorEntry N h c d)))
        (roleTrace N k)
  have hR :
      scalarInnerProduct N
          (∑ c, centeredDifference N c
            (∑ d, centeredDifference N d (tensorEntry N h c d)))
          (roleTrace N k) =
        ∑ c, ∑ d, scalarInnerProduct N
          (centeredDifference N c
            (centeredDifference N d (tensorEntry N h c d)))
          (roleTrace N k) := by
    rw [scalarInnerProduct_sum_left]
    apply Finset.sum_congr rfl
    intro c hc
    rw [centeredDifference_sum, scalarInnerProduct_sum_left]
  rw [hR]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  have hs := scalarInnerProduct_secondDifference N b a
    (tensorEntry N h a b) (roleTrace N k)
  have hc := centeredDifference_comm N b a (tensorEntry N h a b)
  rw [hc] at hs
  exact hs.symm
  
theorem delta_pairing (N : ℕ) (h : LocalSymRoleField N)
    (f : ArchiveRolePhaseGroup N → ℝ) :
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
      (roleDelta a b • f)) =
      scalarInnerProduct N (roleTrace N h) f := by
  change (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
      (roleDelta a b • f)) =
      scalarInnerProduct N (∑ c, tensorEntry N h c c) f
  rw [scalarInnerProduct_sum_left]
  simp_rw [scalarInnerProduct_smul_right]
  apply Finset.sum_congr rfl
  intro a ha
  simp [roleDelta]

theorem divergence_gradient_pairing_symm (N : ℕ)
    (h k : LocalSymRoleField N) :
    (∑ a, ∑ b, (scalarInnerProduct N (tensorEntry N h a b)
      (centeredDifference N a (roleDivergence N k b)) +
        scalarInnerProduct N (tensorEntry N h a b)
          (centeredDifference N b (roleDivergence N k a)))) =
      ∑ a, ∑ b, (scalarInnerProduct N (tensorEntry N k a b)
        (centeredDifference N a (roleDivergence N h b)) +
        scalarInnerProduct N (tensorEntry N k a b)
          (centeredDifference N b (roleDivergence N h a))) := by
  have hleft :
      (∑ a, ∑ b, (scalarInnerProduct N (tensorEntry N h a b)
        (centeredDifference N a (roleDivergence N k b)) +
          scalarInnerProduct N (tensorEntry N h a b)
            (centeredDifference N b (roleDivergence N k a)))) =
        tensorInnerProduct N h
          (symmetricRoleGradient N (divergenceVector N k)) := by
    unfold tensorInnerProduct
    apply Finset.sum_congr rfl
    intro a ha
    apply Finset.sum_congr rfl
    intro b hb
    rw [symmetricRoleGradient_tensorEntry,
      scalarInnerProduct_add_right]
    rfl
  have hright :
      (∑ a, ∑ b, (scalarInnerProduct N (tensorEntry N k a b)
        (centeredDifference N a (roleDivergence N h b)) +
          scalarInnerProduct N (tensorEntry N k a b)
            (centeredDifference N b (roleDivergence N h a)))) =
        tensorInnerProduct N k
          (symmetricRoleGradient N (divergenceVector N h)) := by
    unfold tensorInnerProduct
    apply Finset.sum_congr rfl
    intro a ha
    apply Finset.sum_congr rfl
    intro b hb
    rw [symmetricRoleGradient_tensorEntry,
      scalarInnerProduct_add_right]
    rfl
  calc
    (∑ a, ∑ b, (scalarInnerProduct N (tensorEntry N h a b)
        (centeredDifference N a (roleDivergence N k b)) +
          scalarInnerProduct N (tensorEntry N h a b)
            (centeredDifference N b (roleDivergence N k a)))) =
        tensorInnerProduct N h
          (symmetricRoleGradient N (divergenceVector N k)) := hleft
    _ = tensorInnerProduct N (symmetricRoleGradient N (divergenceVector N k)) h :=
      tensorInnerProduct_symm N _ _
    _ = -2 * roleVectorInnerProduct N (divergenceVector N k)
          (divergenceVector N h) := by
      exact symmetricRoleGradient_adjoint N (divergenceVector N k) h
    _ = -2 * roleVectorInnerProduct N (divergenceVector N h)
          (divergenceVector N k) := by
      rw [roleVectorInnerProduct_symm N]
    _ = tensorInnerProduct N (symmetricRoleGradient N (divergenceVector N h)) k := by
      symm
      exact symmetricRoleGradient_adjoint N (divergenceVector N h) k
    _ = tensorInnerProduct N k
          (symmetricRoleGradient N (divergenceVector N h)) := by
      exact tensorInnerProduct_symm N _ _
    _ = (∑ a, ∑ b, (scalarInnerProduct N (tensorEntry N k a b)
        (centeredDifference N a (roleDivergence N h b)) +
          scalarInnerProduct N (tensorEntry N k a b)
            (centeredDifference N b (roleDivergence N h a)))) := hright.symm

theorem hessian_delta_pairing_symm (N : ℕ)
    (h k : LocalSymRoleField N) :
    (∑ a, ∑ b, (scalarInnerProduct N (tensorEntry N h a b)
      (centeredDifference N a (centeredDifference N b (roleTrace N k))) +
        scalarInnerProduct N (tensorEntry N h a b)
          (roleDelta a b • roleDoubleDivergence N k))) =
      ∑ a, ∑ b, (scalarInnerProduct N (tensorEntry N k a b)
        (centeredDifference N a (centeredDifference N b (roleTrace N h))) +
        scalarInnerProduct N (tensorEntry N k a b)
          (roleDelta a b • roleDoubleDivergence N h)) := by
  rw [show (∑ a, ∑ b, (scalarInnerProduct N (tensorEntry N h a b)
      (centeredDifference N a (centeredDifference N b (roleTrace N k))) +
        scalarInnerProduct N (tensorEntry N h a b)
          (roleDelta a b • roleDoubleDivergence N k))) =
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
        (centeredDifference N a (centeredDifference N b (roleTrace N k)))) +
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
        (roleDelta a b • roleDoubleDivergence N k)) by
    simp only [Finset.sum_add_distrib]]
  rw [show (∑ a, ∑ b, (scalarInnerProduct N (tensorEntry N k a b)
      (centeredDifference N a (centeredDifference N b (roleTrace N h))) +
        scalarInnerProduct N (tensorEntry N k a b)
          (roleDelta a b • roleDoubleDivergence N h))) =
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N k a b)
        (centeredDifference N a (centeredDifference N b (roleTrace N h)))) +
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N k a b)
        (roleDelta a b • roleDoubleDivergence N h)) by
    simp only [Finset.sum_add_distrib]]
  rw [hessianTrace_pairing N h k,
    delta_pairing N h (roleDoubleDivergence N k),
    hessianTrace_pairing N k h,
    delta_pairing N k (roleDoubleDivergence N h)]
  rw [scalarInnerProduct_symm N (roleDoubleDivergence N h) (roleTrace N k),
    scalarInnerProduct_symm N (roleTrace N h) (roleDoubleDivergence N k)]
  ring

theorem delta_laplacian_pairing_symm (N : ℕ)
    (h k : LocalSymRoleField N) :
    (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
      (roleDelta a b • roleLaplacian N (roleTrace N k))) =
      ∑ a, ∑ b, scalarInnerProduct N (tensorEntry N k a b)
        (roleDelta a b • roleLaplacian N (roleTrace N h)) := by
  rw [delta_pairing N h (roleLaplacian N (roleTrace N k)),
    delta_pairing N k (roleLaplacian N (roleTrace N h))]
  rw [scalarInnerProduct_laplacian_self N (roleTrace N h) (roleTrace N k)]
  exact scalarInnerProduct_symm N _ _

theorem finiteResponse_pairing_expand (N : ℕ)
    (h k : LocalSymRoleField N) :
    tensorInnerProduct N h (finiteResponse N k) =
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
        (roleTensorLaplacian N k a b)) -
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
        (centeredDifference N a (roleDivergence N k b))) -
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
        (centeredDifference N b (roleDivergence N k a))) +
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
        (centeredDifference N a
          (centeredDifference N b (roleTrace N k)))) +
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
        (roleDelta a b • roleDoubleDivergence N k)) -
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
        (roleDelta a b • roleLaplacian N (roleTrace N k))) := by
  have hentry : ∀ a b : Role,
      tensorEntry N (finiteResponse N k) a b = responseEntry N k a b := by
    intro a b
    funext x
    exact finiteResponse_entry N k x a b
  unfold tensorInnerProduct
  simp_rw [hentry]
  unfold responseEntry
  simp only [scalarInnerProduct_sub_right, scalarInnerProduct_add_right]
  simp only [Finset.sum_sub_distrib, Finset.sum_add_distrib]

theorem finiteResponse_self_adjoint (N : ℕ)
    (h k : LocalSymRoleField N) :
    tensorInnerProduct N h (finiteResponse N k) =
      tensorInnerProduct N (finiteResponse N h) k := by
  rw [tensorInnerProduct_symm N (finiteResponse N h) k,
    finiteResponse_pairing_expand N h k,
    finiteResponse_pairing_expand N k h]
  have hlap := tensorLaplacian_pairing_self N h k
  have hgrad := divergence_gradient_pairing_symm N h k
  have hcross := hessian_delta_pairing_symm N h k
  have hdelta := delta_laplacian_pairing_symm N h k
  have hlap' :
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
        (roleTensorLaplacian N k a b)) =
      ∑ a, ∑ b, scalarInnerProduct N (tensorEntry N k a b)
        (roleTensorLaplacian N h a b) := by
    calc
      (∑ a, ∑ b, scalarInnerProduct N (tensorEntry N h a b)
          (roleTensorLaplacian N k a b)) =
          ∑ a, ∑ b, scalarInnerProduct N
            (roleTensorLaplacian N h a b) (tensorEntry N k a b) := hlap
      _ = ∑ a, ∑ b, scalarInnerProduct N (tensorEntry N k a b)
          (roleTensorLaplacian N h a b) := by
        apply Finset.sum_congr rfl
        intro a ha
        apply Finset.sum_congr rfl
        intro b hb
        exact scalarInnerProduct_symm N _ _
  simp only [Finset.sum_add_distrib] at hgrad hcross
  linear_combination hlap' - hgrad + hcross - hdelta

theorem tensorInnerProduct_add_right (N : ℕ)
    (h k l : LocalSymRoleField N) :
    tensorInnerProduct N h (k + l) =
      tensorInnerProduct N h k + tensorInnerProduct N h l := by
  have hentry : ∀ a b : Role,
      tensorEntry N (k + l) a b =
        tensorEntry N k a b + tensorEntry N l a b := by
    intro a b
    funext x
    exact tensorEntry_add N k l a b x
  unfold tensorInnerProduct
  simp_rw [hentry, scalarInnerProduct_add_right]
  simp only [Finset.sum_add_distrib]

theorem tensorInnerProduct_add_left (N : ℕ)
    (h k l : LocalSymRoleField N) :
    tensorInnerProduct N (h + k) l =
      tensorInnerProduct N h l + tensorInnerProduct N k l := by
  calc
    tensorInnerProduct N (h + k) l =
        tensorInnerProduct N l (h + k) := tensorInnerProduct_symm N _ _
    _ = tensorInnerProduct N l h + tensorInnerProduct N l k :=
      tensorInnerProduct_add_right N l h k
    _ = tensorInnerProduct N h l + tensorInnerProduct N k l := by
      rw [tensorInnerProduct_symm N l h, tensorInnerProduct_symm N l k]

theorem tensorInnerProduct_smul_right (N : ℕ) (c : ℝ)
    (h k : LocalSymRoleField N) :
    tensorInnerProduct N h (c • k) =
      c * tensorInnerProduct N h k := by
  have hentry : ∀ a b : Role,
      tensorEntry N (c • k) a b = c • tensorEntry N k a b := by
    intro a b
    funext x
    simpa only [Pi.smul_apply] using tensorEntry_smul N c k a b x
  unfold tensorInnerProduct
  simp_rw [hentry, scalarInnerProduct_smul_right]
  simp only [Finset.mul_sum]

theorem tensorInnerProduct_smul_left (N : ℕ) (c : ℝ)
    (h k : LocalSymRoleField N) :
    tensorInnerProduct N (c • h) k =
      c * tensorInnerProduct N h k := by
  calc
    tensorInnerProduct N (c • h) k =
        tensorInnerProduct N k (c • h) := tensorInnerProduct_symm N _ _
    _ = c * tensorInnerProduct N k h :=
      tensorInnerProduct_smul_right N c k h
    _ = c * tensorInnerProduct N h k := by
      rw [tensorInnerProduct_symm N k h]

theorem finiteResponse_pairing_cross (N : ℕ)
    (h k : LocalSymRoleField N) :
    tensorInnerProduct N h (finiteResponse N k) =
      tensorInnerProduct N k (finiteResponse N h) := by
  calc
    tensorInnerProduct N h (finiteResponse N k) =
        tensorInnerProduct N (finiteResponse N h) k :=
      finiteResponse_self_adjoint N h k
    _ = tensorInnerProduct N k (finiteResponse N h) :=
      tensorInnerProduct_symm N _ _

theorem tensorInnerProduct_zero_right (N : ℕ) (h : LocalSymRoleField N) :
    tensorInnerProduct N h 0 = 0 := by
  have hzero : ∀ a b : Role,
      tensorEntry N (0 : LocalSymRoleField N) a b = 0 := by
    intro a b
    funext x
    exact tensorEntry_zero N a b x
  unfold tensorInnerProduct
  simp_rw [hzero]
  unfold scalarInnerProduct
  simp

theorem tensorInnerProduct_zero_left (N : ℕ) (h : LocalSymRoleField N) :
    tensorInnerProduct N 0 h = 0 := by
  rw [tensorInnerProduct_symm, tensorInnerProduct_zero_right]

noncomputable def quadraticAction (N : ℕ) (h : LocalSymRoleField N) : ℝ :=
  (1 / 2 : ℝ) * tensorInnerProduct N h (finiteResponse N h)

theorem quadraticAction_first_variation (N : ℕ)
    (h k : LocalSymRoleField N) (ε : ℝ) :
    quadraticAction N (h + ε • k) =
      quadraticAction N h +
        ε * tensorInnerProduct N k (finiteResponse N h) +
        ε ^ 2 * quadraticAction N k := by
  have hresponse : finiteResponse N (h + ε • k) =
      finiteResponse N h + ε • finiteResponse N k := by
    rw [finiteResponse_add, finiteResponse_smul]
  unfold quadraticAction
  rw [hresponse, tensorInnerProduct_add_left]
  simp_rw [tensorInnerProduct_add_right, tensorInnerProduct_smul_left,
    tensorInnerProduct_smul_right]
  have hcross := finiteResponse_pairing_cross N h k
  rw [hcross]
  ring

theorem quadraticAction_gauge_invariant (N : ℕ)
    (h : LocalSymRoleField N) (xi : LocalRoleVector N) :
    quadraticAction N (h + symmetricRoleGradient N xi) =
      quadraticAction N h := by
  have hresponse : finiteResponse N (h + symmetricRoleGradient N xi) =
      finiteResponse N h + finiteResponse N (symmetricRoleGradient N xi) :=
    finiteResponse_add N h (symmetricRoleGradient N xi)
  unfold quadraticAction
  rw [hresponse, finiteResponse_gauge_nullity,
    tensorInnerProduct_add_right, tensorInnerProduct_zero_right,
    tensorInnerProduct_add_left]
  have hcross := finiteResponse_pairing_cross N
    (symmetricRoleGradient N xi) h
  rw [hcross, finiteResponse_gauge_nullity, tensorInnerProduct_zero_right]
  ring

noncomputable def radiusOneOffsets (N : ℕ) : Finset (ArchiveRolePhaseGroup N) :=
  {0} ∪ (Finset.univ.image (roleStep N)) ∪
    (Finset.univ.image (fun r => -roleStep N r))

theorem radiusOneOffsets_zero (N : ℕ) :
    (0 : ArchiveRolePhaseGroup N) ∈ radiusOneOffsets N := by
  simp [radiusOneOffsets]

theorem radiusOneOffsets_plus (N : ℕ) (r : Role) :
    roleStep N r ∈ radiusOneOffsets N := by
  simp [radiusOneOffsets]

theorem radiusOneOffsets_minus (N : ℕ) (r : Role) :
    -roleStep N r ∈ radiusOneOffsets N := by
  simp [radiusOneOffsets]

theorem centeredDifference_point_congr (N : ℕ) (r : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N)
    (hplus : f (x + roleStep N r) = g (x + roleStep N r))
    (hminus : f (x - roleStep N r) = g (x - roleStep N r)) :
    centeredDifference N r f x = centeredDifference N r g x := by
  simp only [centeredDifference_apply, roleTranslatePlus_apply,
    roleTranslateMinus_apply]
  rw [hplus, hminus]

theorem centeredDifference_second_radius_two_congr (N : ℕ)
    (r s : Role) (f g : ArchiveRolePhaseGroup N → ℝ)
    (x : ArchiveRolePhaseGroup N)
    (hagree : ∀ u ∈ radiusOneOffsets N, ∀ v ∈ radiusOneOffsets N,
      f (x + u + v) = g (x + u + v)) :
    centeredDifference N r (centeredDifference N s f) x =
      centeredDifference N r (centeredDifference N s g) x := by
  have hpp := hagree (roleStep N r) (radiusOneOffsets_plus N r)
    (roleStep N s) (radiusOneOffsets_plus N s)
  have hpm := hagree (roleStep N r) (radiusOneOffsets_plus N r)
    (-roleStep N s) (radiusOneOffsets_minus N s)
  have hmp := hagree (-roleStep N r) (radiusOneOffsets_minus N r)
    (roleStep N s) (radiusOneOffsets_plus N s)
  have hmm := hagree (-roleStep N r) (radiusOneOffsets_minus N r)
    (-roleStep N s) (radiusOneOffsets_minus N s)
  have hpm' : f (x + roleStep N r - roleStep N s) =
      g (x + roleStep N r - roleStep N s) := by
    simpa [sub_eq_add_neg] using hpm
  have hmp' : f (x - roleStep N r + roleStep N s) =
      g (x - roleStep N r + roleStep N s) := by
    simpa [sub_eq_add_neg] using hmp
  have hmm' : f (x - roleStep N r - roleStep N s) =
      g (x - roleStep N r - roleStep N s) := by
    simpa [sub_eq_add_neg] using hmm
  simp only [centeredDifference_apply, roleTranslatePlus_apply,
    roleTranslateMinus_apply]
  rw [hpp, hpm', hmp', hmm']

theorem roleTrace_radius_two_congr (N : ℕ)
    (h k : LocalSymRoleField N) (x : ArchiveRolePhaseGroup N)
    (hagree : ∀ u ∈ radiusOneOffsets N, ∀ v ∈ radiusOneOffsets N,
      ∀ a b, tensorEntry N h a b (x + u + v) =
        tensorEntry N k a b (x + u + v))
    (u : ArchiveRolePhaseGroup N) (hu : u ∈ radiusOneOffsets N)
    (v : ArchiveRolePhaseGroup N) (hv : v ∈ radiusOneOffsets N) :
    roleTrace N h (x + u + v) = roleTrace N k (x + u + v) := by
  unfold roleTrace
  apply Finset.sum_congr rfl
  intro a ha
  exact hagree u hu v hv a a

theorem roleDivergence_radius_one_congr (N : ℕ)
    (h k : LocalSymRoleField N) (b : Role) (x : ArchiveRolePhaseGroup N)
    (hagree : ∀ u ∈ radiusOneOffsets N, ∀ v ∈ radiusOneOffsets N,
      ∀ a b, tensorEntry N h a b (x + u + v) =
        tensorEntry N k a b (x + u + v))
    (u : ArchiveRolePhaseGroup N) (hu : u ∈ radiusOneOffsets N) :
    roleDivergence N h b (x + u) = roleDivergence N k b (x + u) := by
  unfold roleDivergence
  change (∑ a, centeredDifference N a (tensorEntry N h a b) (x + u)) =
    ∑ a, centeredDifference N a (tensorEntry N k a b) (x + u)
  apply Finset.sum_congr rfl
  intro a ha
  have hp := hagree u hu (roleStep N a) (radiusOneOffsets_plus N a) a b
  have hm := hagree u hu (-roleStep N a) (radiusOneOffsets_minus N a) a b
  have hm' : tensorEntry N h a b (x + u - roleStep N a) =
      tensorEntry N k a b (x + u - roleStep N a) := by
    simpa [sub_eq_add_neg, add_assoc] using hm
  simp only [centeredDifference_apply, roleTranslatePlus_apply,
    roleTranslateMinus_apply]
  rw [hp, hm']

theorem roleTensorLaplacian_radius_two_congr (N : ℕ)
    (h k : LocalSymRoleField N) (a b : Role) (x : ArchiveRolePhaseGroup N)
    (hagree : ∀ u ∈ radiusOneOffsets N, ∀ v ∈ radiusOneOffsets N,
      ∀ a b, tensorEntry N h a b (x + u + v) =
        tensorEntry N k a b (x + u + v)) :
    roleTensorLaplacian N h a b x = roleTensorLaplacian N k a b x := by
  unfold roleTensorLaplacian roleLaplacian
  simp only [Finset.sum_apply]
  apply Finset.sum_congr rfl
  intro c hc
  apply centeredDifference_second_radius_two_congr N c c
    (tensorEntry N h a b) (tensorEntry N k a b) x
  intro u hu v hv
  exact hagree u hu v hv a b

theorem roleLaplacian_trace_radius_two_congr (N : ℕ)
    (h k : LocalSymRoleField N) (x : ArchiveRolePhaseGroup N)
    (hagree : ∀ u ∈ radiusOneOffsets N, ∀ v ∈ radiusOneOffsets N,
      ∀ a b, tensorEntry N h a b (x + u + v) =
        tensorEntry N k a b (x + u + v)) :
    roleLaplacian N (roleTrace N h) x =
      roleLaplacian N (roleTrace N k) x := by
  unfold roleLaplacian
  simp only [Finset.sum_apply]
  apply Finset.sum_congr rfl
  intro c hc
  apply centeredDifference_second_radius_two_congr N c c
    (roleTrace N h) (roleTrace N k) x
  intro u hu v hv
  exact roleTrace_radius_two_congr N h k x hagree u hu v hv

theorem roleDivergence_difference_radius_two_congr (N : ℕ)
    (h k : LocalSymRoleField N) (a b : Role) (x : ArchiveRolePhaseGroup N)
    (hagree : ∀ u ∈ radiusOneOffsets N, ∀ v ∈ radiusOneOffsets N,
      ∀ c d, tensorEntry N h c d (x + u + v) =
        tensorEntry N k c d (x + u + v)) :
    centeredDifference N a (roleDivergence N h b) x =
      centeredDifference N a (roleDivergence N k b) x := by
  apply centeredDifference_point_congr N a
  · exact roleDivergence_radius_one_congr N h k b x hagree
      (roleStep N a) (radiusOneOffsets_plus N a)
  · have hm := roleDivergence_radius_one_congr N h k b x hagree
      (-roleStep N a) (radiusOneOffsets_minus N a)
    simpa [sub_eq_add_neg] using hm

theorem roleDoubleDivergence_radius_two_congr (N : ℕ)
    (h k : LocalSymRoleField N) (x : ArchiveRolePhaseGroup N)
    (hagree : ∀ u ∈ radiusOneOffsets N, ∀ v ∈ radiusOneOffsets N,
      ∀ a b, tensorEntry N h a b (x + u + v) =
        tensorEntry N k a b (x + u + v)) :
    roleDoubleDivergence N h x = roleDoubleDivergence N k x := by
  rw [roleDoubleDivergence_eq_divergence N h,
    roleDoubleDivergence_eq_divergence N k]
  simp only [Finset.sum_apply]
  apply Finset.sum_congr rfl
  intro a ha
  have hp := roleDivergence_radius_one_congr N h k a x hagree
    (roleStep N a) (radiusOneOffsets_plus N a)
  have hm := roleDivergence_radius_one_congr N h k a x hagree
    (-roleStep N a) (radiusOneOffsets_minus N a)
  have hm' : roleDivergence N h a (x - roleStep N a) =
      roleDivergence N k a (x - roleStep N a) := by
    simpa [sub_eq_add_neg] using hm
  simp only [centeredDifference_apply, roleTranslatePlus_apply,
    roleTranslateMinus_apply]
  rw [hp, hm']

theorem finiteResponse_radius_two (N : ℕ)
    (h k : LocalSymRoleField N) (x : ArchiveRolePhaseGroup N)
    (a b : Role)
    (hagree : ∀ u ∈ radiusOneOffsets N, ∀ v ∈ radiusOneOffsets N,
      ∀ c d, tensorEntry N h c d (x + u + v) =
        tensorEntry N k c d (x + u + v)) :
    responseEntry N h a b x = responseEntry N k a b x := by
  have hL := roleTensorLaplacian_radius_two_congr N h k a b x hagree
  have hDa := roleDivergence_difference_radius_two_congr N h k a b x hagree
  have hDb := roleDivergence_difference_radius_two_congr N h k b a x hagree
  have hH := centeredDifference_second_radius_two_congr N a b
    (roleTrace N h) (roleTrace N k) x (by
      intro u hu v hv
      exact roleTrace_radius_two_congr N h k x hagree u hu v hv)
  have hq := roleDoubleDivergence_radius_two_congr N h k x hagree
  have hlt := roleLaplacian_trace_radius_two_congr N h k x hagree
  unfold responseEntry
  simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply]
  rw [hL, hDa, hDb, hH, hq, hlt]

theorem finiteResponse_radius_two_stencil (N : ℕ)
    (h k : LocalSymRoleField N) (x : ArchiveRolePhaseGroup N) :
    (∀ u ∈ radiusOneOffsets N, ∀ v ∈ radiusOneOffsets N,
      ∀ a b, tensorEntry N h a b (x + u + v) =
        tensorEntry N k a b (x + u + v)) →
      ∀ a b, responseEntry N h a b x = responseEntry N k a b x := by
  intro hagree a b
  exact finiteResponse_radius_two N h k x a b hagree

theorem responseEntry_zero (h : LocalSymRoleField 0) (a b : Role) :
    responseEntry 0 h a b = 0 := by
  simp [responseEntry, roleTensorLaplacian, roleLaplacian,
    roleDivergence, roleDoubleDivergence, centeredDifference_zero]

theorem finiteResponse_zero (h : LocalSymRoleField 0) :
    finiteResponse 0 h = 0 := by
  funext x
  apply SymRoleTensor.ext
  funext a b
  rw [finiteResponse_entry, responseEntry_zero]
  rfl

end D0.Gravity
