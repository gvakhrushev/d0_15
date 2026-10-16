# The owned record reads the supplied observer scale

**Status:** conditional candidate. The scale comparison passed review.
No registry row. Not a physical admission and not GR.
Pre-flight searched
`02_REGISTRY/claims.csv` in this worktree for `nilpotentAffineGenerator`,
`positive unit ray`, and `record(I` and found no row. The chronology record,
the preparation channel, the quotient coordinate `b_e`, and the soldered
creator are already owned and are not re-proved here.

## Claim

At the identity Gram \(G=I_4\), the owned chronology record returns a
different operator at the supplied observer \(n=2e_0\) from the operator at
\(n=e_0\). The \((0,1)\) entry of that difference is \(-p\), and the
\((1,0)\) entry is \(-103p\), where \(a^2=p\), \(p+p^2=1\), and \(p\neq 0\).
The positive unit ray of \(2e_0\) is \(e_0\). The record at \(2e_0\) is
therefore not the record at its positive unit ray.

The same record's price cut is even in the observer when \(G=I_4\): the
creator is linear, and \(N=C(n)\,S^{-1}C(n)^T S\) does not change when \(n\)
is replaced by \(-n\). On the sample \(n=e_0\), the returned price cut agrees
at \(-e_0\) while the operator does not. The \((0,1)\) entry of that operator
difference is \(2p\).

The preparation channel is built from `record(I_4,e_r)` before the later
binding \(b_r=e_r\). That binding is the coordinate basis, not a value read
from a Cartan shift. The nilpotent generator applies the exterior creator to
a free `RoleSpace`, and its file does not mention a Cartan shift.

## Owned pre-facts

The record takes a Gram and an observer
(`a4d_native_record_metric_chronology_check.py:123-136`):

> def record(G, n, dG=None, dn=None):
>     """The orientation-independent full CAR formula and its genuine jet."""
>     S = ext(G)
>     Si = ext(G.inv())
>     cr = creator(n)
>     an = Si * cr.T * S
>     N = cr * an
>     X = DEG - N
>     H = (-2 * X**3 + 9 * X**2 - 7 * X) / 6
>     U = a * ((I - H) + H * (I - 2 * N)) + p * (
>         (I - H) * (cr - an) - H * (cr + an))
>     P = I - N
>     if dG is None:
>         return mat(U), mat(P)

The same definition continues to the jet and returns `mat(U), mat(P), mat(dU), mat(-dN)`
(`a4d_native_record_metric_chronology_check.py:148`). The calls below omit
`dG`, so they use the branch quoted above.

The creator is linear in the observer
(`a4d_native_fock_record_binding_check.py:83-87`):

> def creator(v):
>  C=s.zeros(16)
>  for r in range(4):
>   for mask,S in enumerate(SUBS):
>    if r not in S:C[mask|(1<<r),mask]+=v[r]*(-1)**sum(i<r for i in S)
>  return C

The preparation channel is assembled from the four basis records, and the
later normalization is marked unselected
(`a4d_native_golden_channel_endogenous_preparation_check.py:231` and `:287-293`):

>     returns = [chronology.record(I4, n)[0] for n in basis]

>     # The existing affine-shift slots do carry four vectors per site.  If a
>     # return reads the oriented ray of its own shift, positive-G normalization
>     # is canonical and covariant; this is a kinematic candidate interface,
>     # not a physical identification currently selected by the core.
>     q = eta
>     D = I4
>     b = [I4[:, r] for r in range(4)]

The native coordinate \(b_e\) is not that binding
(`A4D_NATIVE_JOINT_FIELD_QUOTIENT.md:56` and `:96-98`):

> b_e = F_x a_e,

> These
> formulas reconstruct an actual state and show that there are no further
> constraints on b or m.

The nilpotent generator takes a free vector
(`A4DNilpotentAffineMatterLift.lean:136-138`):

> def nilpotentAffineGenerator (b : RoleSpace) :
>     (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
>   (archiveExteriorCreatorLM b).comp vacuumProjector

The one definition whose body both names an affine connection and applies
`archiveExteriorCreator` is the soldered direction, and the creator argument
is the solder leg (`ArchiveAffineExteriorLink.lean:319-323`):

> def archiveSolderedCreateDirection
>     (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
>     (r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
>   fun p =>
>     archiveExteriorCreator (solderLegVector N e p.1 r)

The scalar common shift is a different carrier
(`LocalRaychaudhuriRepresentation.lean:191-195`):

> /-- Common-shift gauge of the two unobserved components. -/
> def ResponseDecomposition.shift {X : Type}
>     (D : ResponseDecomposition X) (g : X → ℝ) : ResponseDecomposition X where
>   darkDrive := fun x => D.darkDrive x + g x
>   focusingLoad := fun x => D.focusingLoad x + g x

The next declaration says what that gauge does
(`LocalRaychaudhuriRepresentation.lean:197-200`):

> /-- Every common local shift is invisible to the net readout. -/
> theorem common_shift_preserves_net
>     {X : Type} (D : ResponseDecomposition X) (g : X → ℝ) :
>     (D.shift g).net = D.net := by

## The separation

The positive unit ray is the vector of squared length \(1\) that is parallel
to the supplied observer and has positive inner product with it. There is no
separate zero branch. It accepts \(e_0\) as the ray of \(e_0\) and of
\(2e_0\). It rejects \(2e_0\) by the squared length, rejects \(-e_0\) as a
ray of \(e_0\) by the sign, and rejects \(e_0\) as a ray of the zero observer
by the sign.

Call the owned record at \(G=I_4\). The operator at \(2e_0\) differs from the
operator at \(e_0\). The ray of \(2e_0\) is \(e_0\), so this is a difference
between the record at a vector and the record at that vector's ray. The
price cut at \(2e_0\) also differs from the price cut at \(e_0\). Scaling is
visible to both returned matrices on this sample.

At \(-e_0\) the operator differs and the price cut does not. The same split
holds on the second axis. The evenness of the price cut at \(G=I_4\) is the
identity \(N(-n)=N(n)\) coming from the linear creator and the formula
\(N=C(n)\,S^{-1}C(n)^T S\). It is not inferred from the two axis samples.
Those samples are what show that the returned operator is not even.

For the raw observer \((3,4,0,0)\), the ray is \((3/5,4/5,0,0)\). The record
at the raw observer differs from the record at that ray. Two entries of the
difference are \(-12p/5\) and \(-16p/5\).

The zero observer is a legal input of `record`. Its operator differs from
the operator at \(e_0\). The ray predicate still rejects \(e_0\) against the
zero observer. Normalization by \(\sqrt{n\cdot n}\) is not applied to zero
in this note.

Replacing \(G=I_4\) by \(\operatorname{diag}(2,1,1,1)\) at the same observer
\(e_0\) also changes the operator. The \((0,1)\) entry of that difference is
again \(-p\), but the \((1,0)\) entry is \(-6p\), not \(-103p\). The two
differences are different matrices. The diagonal probe is not a native
admitted metric. It only shows that the first argument is read.

The preparation file contains the English words for an affine-shift slot and
does not contain the tokens `.shift` or `AffineCartan`. The channel slice
that runs from the basis-return line to `def channel` contains neither the
binding `b = [` nor a `record(G` call. The binding that follows is
\(b_r=e_r\). The chronology file likewise has neither token. Its signature
is `record(G, n, dG=None, dn=None)`.

Every `def` or `abbrev` under `03_FORMALIZATION/D0` whose uncommented body
contains the token `.shift` is exactly

`ResponseDecomposition.shift`, `barB`, `deltaB`, `predecessorTorsion`,
`apply`, `mul`, `inv`, `covariantShift`, `affineOpenTorsion`.

None of those nine applies `archiveExteriorCreator`. This list is a token
scan. It is not the ten-name call closure of `barB`, `deltaB`, and
`predecessorTorsion`, and it is not a closure upward from `apply`, `mul`,
or `inv`. The unique definition that both applies `archiveExteriorCreator`
and mentions `AffineCartan` or `.shift` is `archiveSolderedCreateDirection`,
whose creator argument is `solderLegVector` and whose body has no `.shift`.

`nilpotentAffineGenerator` is outside that scan. Its parameter is a
`RoleSpace`, its body applies `archiveExteriorCreatorLM` to that parameter,
and the file contains neither `.shift` nor `AffineCartan`.

## Verification

`02_REGISTRY/research/certificates/a4d_native_record_scale_not_cartan_shift_check.py`,
30/30 PASS.

Negative controls, each able to change the conclusion:

- At \(n=e_0\) the record meets the record at its own ray. A statement that the record never meets the ray fails on this sample.
- At \(n=2e_0\) the operator difference has \((1,0)\) entry \(-103p\). Replacing that witness by the gram probe, whose \((1,0)\) entry is \(-6p\), fails the double-shift check.
- The price cut at \(-e_0\) equals the price cut at \(e_0\). Saying that every returned matrix flips fails that cut.
- The raw observer \((3,4,0,0)\) is not a unit vector. Its record differs from the record at \((3/5,4/5,0,0)\).
- \(e_0\) is parallel to the zero observer and has squared length \(1\). The sign test is what rejects it. The record call on zero still returns a matrix.
- A new definition whose body contains `.shift`, or a preparation file that gains `AffineCartan`, fails the scan.
- The soldered creator reads the leg. Treating it as a shift reader fails the absent `.shift` token in its body.

Reproduce with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_record_scale_not_cartan_shift_check.py
```

## Named risks and pre-registered attack surface

The strongest self-attack is to read the agreement at \(n=e_0\) as “the
record is the positive unit ray.” The named second object is \(n=2e_0\).
Its ray is \(e_0\), and the owned record returns different operators there.
The \((0,1)\) entry of the difference is \(-p\neq 0\).

Next attacks:

- Reading the shared \(-p\) at cell \((0,1)\) as one phenomenon. The gram probe and the double observer produce different matrices; cell \((1,0)\) separates them.
- Promoting the even price cut to a sign-blind record. The operator at \(-e_0\) is the second object, and its \((0,1)\) entry differs by \(2p\).
- Treating \(\operatorname{diag}(2,1,1,1)\) as an admitted native metric. It is an algebraic probe of the first argument.
- Treating the preparation comment as a selected law. The binding is the coordinate basis, it stands after `def channel`, and the file has no Cartan shift token.
- Identifying `nilpotentAffineGenerator` with this record or with \(b_e\). The parameter is a free `RoleSpace`, and the file has no `.shift`.
- Promoting the nine-name token scan to a whole-core exhaustion. A reader that does not use the token `.shift` is the reopening hook. The nilpotent generator is already that kind of object, and it still does not name a Cartan connection.
- Calling the channel-before-binding order a new theorem. The seed certificate already checks it. It is re-read here so this note does not depend on a paraphrase.

## What this does not show

This does not select \(n_e\) from the Cartan coordinate \(b_e\). It does not
compare the ten-slot covector with \(\rho_0\). It does not cancel an archive
remainder. The live gate on `conditional_endogenous_preparation` stays:

> The direct route through ArchiveAffineExteriorLink, archiveAffineLinkedHodgeDirac and archiveSolderedDirac is ruled out: all are invariant under changes of affine shift at fixed linear links (see conditional_archive_shift_blindness). Do not infer b_e->n_e from these transports. The next arrow is a separate already-owned local record/preparation law that reads b_e, with its action, joint variation, full-support preparation and refinement; if none exists, prove completeness of the actual interface before claiming obstruction. Then combine all owned heat/action terms with the candidate ten-slot covector and compare the total source with rho0; keep parent terminals open.

The token scan is not that completeness proof. The coframe–curvature
principle \(\mathfrak{V}\), the own action, Ward identity, refinement, curved
roots, soundness and recovery, G0, and the parent terminals remain open.
