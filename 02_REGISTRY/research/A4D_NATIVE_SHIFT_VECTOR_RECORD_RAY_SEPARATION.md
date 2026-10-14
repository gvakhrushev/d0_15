# Owned shift vectors are not the positive record ray

**Status:** conditional candidate. The kill of the ray control and the wound
on its zero branch are accepted, and the repair passed. No registry row.
Not a physical admission and not GR.
Pre-flight searched `02_REGISTRY/claims.csv` in this worktree for
`diagonalSeed`, `shift_irrelevant`, `record ray`, and `same-edge` and found
no row. Certificates in this worktree live under
`02_REGISTRY/research/certificates/`. Broader `shift` rows in
that file are cyclic, phason, toral, and compensator carriers, not this
Cartan seed. The affine-CAR transport blindness and the equal-weight
contraction are already on this branch and are not re-proved here.

## Claim

Let the linear part of every edge be the identity, and let every edge carry
the same translation \(b\in\mathbb R^4\). For every linear comparison \(J\),
the owned diagonal seed is \(-b\). Whenever \(b\neq 0\), \(-b\) is not the
positive unit ray \(b/\sqrt{b\cdot b}\).

On the zero coframe of `solderLegVector_zero`, the soldered creator vector is
the basis vector \(e_r\). Predecessor torsion equals \(b\), so it equals that
creator only when \(b=e_r\). The creator definition does not read the
translation. None of the ten definitions in the shift-vector closure below
occur in a file that applies `archiveExteriorCreator`.

## Owned pre-facts

The comparison endomorphism of the seed is supplied
(`03_FORMALIZATION/D0/Geometry/A4DConditionalSourcedDiagonalTransport.lean:9-11`):

> Assumes a **supplied** comparison endomorphism `𝔍`; does not construct or select it.

The seed is defined from the pulled shift
(`A4DConditionalSourcedDiagonalTransport.lean:66-70`):

> /-- Finite diagonal seed `a_r = -\bar b_r - 𝔍_y Δ^b_r`. -/
> def diagonalSeed (A : AffineCartanConnection N ℝ RoleSpace)
>     (J : ComparisonEndomorphismField N)
>     (y : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
>   -barB A y r - J y (deltaB A y r)

Predecessor torsion reads the same translation
(`A4DSourcedMismatchFactorPassport.lean:93-99`):

> /-- Predecessor torsion at edge `(x,r)` with source `y = x + r`:
> `τ = b_{x,r} + L_{x,r} v_r(y) − v_r(x)`. -/
> def predecessorTorsion
>     (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
>     (x : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
>   let y := sourceSiteFromPredecessor N r x
>   (A x r).shift + (A x r).lin (solderLegVector N e y r) - solderLegVector N e x r

The soldered creator reads the solder leg
(`ArchiveAffineExteriorLink.lean:318-325`):

> /-- Moving creator `C†(v_r(x))` on the pulled forward difference. -/
> def archiveSolderedCreateDirection
>     (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
>     (r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
>   fun p =>
>     archiveExteriorCreator (solderLegVector N e p.1 r)

and the zero coframe makes that leg the basis vector
(`ArchiveAffineExteriorLink.lean:307-308`):

> theorem solderLegVector_zero (x : ArchiveRolePhaseGroup N) (r : Role) :
>     solderLegVector N (0 : LocalCoframeField N) x r = archiveRoleBasis r := by

The identity affine map has zero translation
(`ArchiveAffineCartanConnection.lean:73`):

> @[simp] theorem one_shift : (1 : AffineCartanMap K V).shift = 0 := rfl

and the flat connection is that identity on every edge
(`ArchiveAffineCartanConnection.lean:336-337`):

> noncomputable def flatAffineConnection (N : ℕ) : AffineCartanConnection N ℝ (Role → ℝ) :=
>   fun _ _ => 1

The existing Dirac transports are already known to ignore the translation
(`ArchiveAffineExteriorLink.lean:396-399`):

> The complete coframe-soldered CAR Dirac operator is likewise blind to
> affine translations at fixed linear links and fixed raw solder and observer.
> These two existing CAR transports therefore do not select a local record
> readout from the affine shift.

At the identity coframe the native coordinate \(b_e\) is the translation
(`A4D_NATIVE_JOINT_FIELD_QUOTIENT.md:56`):

> b_e = F_x a_e,

The constant linear ansatz that does put a multiple of \(b\) into a reference
leg is already a scoped no-go, not a selected ray
(`A4DReferenceLocalCandidateNoGo.lean:12-22`):

> the constant-coefficient source-typed ansatz
>
> \[
> q_{a,c,d}
> =
> a\,v_y + c\,L^{-1}v_x + d\,L^{-1}b
> \]
>
> cannot simultaneously satisfy flat normalization, exact pure-gauge cancellation
> on the explicit L=3 equal-neighbour witness, and nonzero pure affine-shift
> visibility.

The golden-channel reconstruction that sets \(b_r=e_r\) is marked as an
unselected candidate
(`a4d_native_golden_channel_endogenous_preparation_check.py:287-290`):

> # The existing affine-shift slots do carry four vectors per site.  If a
> # return reads the oriented ray of its own shift, positive-G normalization
> # is canonical and covariant; this is a kinematic candidate interface,
> # not a physical identification currently selected by the core.

The channel closure in that checker is built from
`returns = [chronology.record(I4, n)[0] for n in basis]` before that
assignment.

## The separation

`barB` pulls `(A x r).shift` by the inverse linear part. `deltaB` subtracts
that pull from the local shift. For one common translation \(b\) and identity
linear part, both shifts equal \(b\), so `deltaB = 0`. Every linear \(J\)
therefore contributes \(J(0)=0\), and

\[
\operatorname{diagonalSeed}=-b.
\]

The positive unit ray \(u=b/\sqrt{b\cdot b}\) is the unique vector of squared
length \(1\) that is parallel to \(b\) and has positive inner product with
\(b\). The certificate builds the seed by the `barB`/`deltaB` arithmetic and
asks that predicate about the computed seed, not about \(b\) alone. The
predicate accepts \(e_0\) as the ray of both \(e_0\) and \(2e_0\). It rejects
\(-e_0\) by the sign and rejects \(2e_0\) by the squared length. The same
sign test rejects \(e_0\) as a ray of the zero shift: that vector is parallel
to \(0\) and has squared length \(1\), while the inner product is \(0\).
There is no separate zero branch. On each constant-shift sample the computed seed
is \(-b\), and the predicate rejects that seed. The unit sample \(e_0\) is
what makes a sign error fail.

The same identity-linear, zero-coframe evaluation gives predecessor torsion
\(b\) and creator vector \(e_r\). They agree at \(b=e_r\) and disagree at
\(b=2e_r\). The creator's defining body contains `solderLegVector` and does
not contain `.shift`.

The definitions reachable from `barB`, `deltaB`, and `predecessorTorsion` are
exactly

`barB`, `deltaB`, `diagonalSeed`, `relativeDefect`, `pathSource`,
`parallelResidual`, `predecessorTorsion`, `IncrementsInActiveSpan`,
`seedAsSuppliedDiagonal`, `conditionalMismatchFromSeed`.

No file under `03_FORMALIZATION` both applies `archiveExteriorCreator` and
mentions one of those ten names.

If the predecessor shift is \(0\) and the local shift is \(e_0\), the same
swap \(J\) sends the seed to \(-e_1\), not to \(-e_0\). The supplied
comparison acts as soon as the increment is nonzero. The identity
\(\operatorname{diagonalSeed}=-b\) uses the constant-shift hypothesis.

## Verification

`02_REGISTRY/research/certificates/a4d_native_shift_vector_record_ray_separation_check.py`.

Negative controls, each able to change the conclusion:

- A non-constant shift lets the hostile swap \(J\) send the seed to \(-e_1\) rather than \(-e_0\).
- At \(b=e_r\) torsion equals the creator, so agreement at that one value is not the claim.
- The hostile swap \(J\) is not zero, and the constant-shift seed is still \(-b\).
- A file that both created with `archiveExteriorCreator` and named `diagonalSeed` would fail the closure separation.
- The ray predicate accepts \(e_0\) for the unit shift and for the double shift. The computed seed is rejected. Replacing that seed by \(e_0\) on the unit sample fails the separation.
- \(-e_0\) is parallel to \(e_0\) and has squared length \(1\). The sign test is what rejects it.
- \(2e_0\) is parallel to itself and acute. The unit-length test is what rejects it.
- \(e_0\) is parallel to the zero shift and has squared length \(1\). The inner product is \(0\). The sign test is what rejects it.

Reproduce with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_shift_vector_record_ray_separation_check.py
```

## Named risks and pre-registered attack surface

The strongest self-attack is to read \(-b\neq u\) as “no owned law reads the
affine shift.” The named second object is `diagonalSeed` itself: it reads the
shift, and on a constant field it equals \(-b\). The separation is only from
the positive ray and from the soldered creator.

Next attacks:

- Treating `ResponseDecomposition.shift` as this translation. That definition is a common additive gauge of two scalar functions in `LocalRaychaudhuriRepresentation.lean`, and the closure scan does not include it.
- Treating the agreement \(b=e_r\) as an identity of maps. The double shift \(2e_r\) keeps the creator at \(e_r\) and moves the torsion.
- Importing the already proved Dirac blindness, or the constant-linear reference no-go, as this vector identity. Those are cited and not re-proved.
- Promoting the result to a whole-core exhaustion. A law outside the ten-name closure, or a non-constant shift with a selected \(J\), is the reopening hook.
- Identifying \(F_x=I\) with every native coframe. The coordinate sentence \(b_e=F_x a_e\) is used only at the identity factor, where the translation is \(b_e\).
- Testing \(-b\neq u\) on the shift alone. That sentence does not read `diagonalSeed`. The receipt predicate has to accept the true ray and reject the seed this checker computes.

## Skeptic #5, accepted

The first pass killed the ray control. Errors of record:

- `not_positive_ray` did not read the computed seed. For squared length other than \(1\) it returned true at once. For squared length \(1\), \(-b\neq b\) cannot fail for a nonzero vector. The samples never reached the zero branch, and deleting that branch left the receipt green.
- The memo named a zero-vector control that was not a receipt check.
- The channel sentence wrote `record(I_4,e_r)` and dropped the live `[0]` index.
- The pre-flight pointed at a retired certificate path instead of the live
  `02_REGISTRY/research/certificates/` directory.

The repair replaces that predicate, receipt-locks the sign, length, and zero refusals, compares the computed seed, quotes the live return line, and retargets the pre-flight.

Skeptic #6 wounded the zero early return. Deleting `if dot(b, b) == 0: return False` left the old zero check green, because the inner product with \(0\) is already not positive. That return is deleted. The receipt witness is now \(e_0\) against the zero shift: parallel, squared length \(1\), inner product \(0\). Removing the sign clause accepts that witness. That repair passed. This
remains a conditional candidate.

## What this does not show

This does not select a record ray, admit the golden channel, or produce a
preparation whose input is \(b_e\). It does not compare the ten-slot covector
with \(\rho_0\). It does not cancel an archive remainder. It does not choose
\(J\). The live gate on `conditional_endogenous_preparation` stays:

> The direct route through ArchiveAffineExteriorLink, archiveAffineLinkedHodgeDirac and archiveSolderedDirac is ruled out: all are invariant under changes of affine shift at fixed linear links (see conditional_archive_shift_blindness). Do not infer b_e->n_e from these transports. The next arrow is a separate already-owned local record/preparation law that reads b_e, with its action, joint variation, full-support preparation and refinement; if none exists, prove completeness of the actual interface before claiming obstruction. Then combine all owned heat/action terms with the candidate ten-slot covector and compare the total source with rho0; keep parent terminals open.

The ten-name closure is not that completeness proof. The coframe–curvature
principle \(\mathfrak{V}\), the own action, Ward identity, refinement, curved
roots, soundness and recovery, G0, and the parent terminals remain open.
