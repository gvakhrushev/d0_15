# Constant translation: path sum versus open torsion

**Status:** conditional candidate. The ray comparison passed review. No new
registry row. Not a physical admission and not GR.
`02_REGISTRY/claims.csv` already owns `D0-AFFINE-CARTAN-PATH-CLOSURE-001`.
That row owns the path algebra, including `affinePath_shift_eq_covariant_sum`
and `affineOpenTorsion_gauge`, and it selects no constitutive action. This
note does not re-prove it. The search for `covariantShift` and `positive
unit ray` in that file returned no row. The constant identity-linear
evaluation below is the new comparison.

## Claim

Let every edge carry the affine map \((I,b)\). The owned covariant sum of
one forward step is \(b\). One backward step is \(-b\). Two forward steps
sum to \(2b\). Open torsion of every face is \(0\).

The forward value equals the positive unit ray of \(b\) precisely when \(b\)
itself is that ray. Both \(e_0\) and \(-e_0\) are such rays of themselves.
The forward value at \(b=2e_0\) is not. Open torsion remains \(0\) at
\(b=e_0\), where the forward step meets the ray. Based torsion agrees with
open torsion on this identity family and differs from it when a swap link
moves the square translation.
That difference is the already owned holonomy clause, evaluated on one
witness.

## Owned pre-facts

Composition and inversion are
(`ArchiveAffineCartanConnection.lean:68-69`, `:77-78`):

> @[simp] theorem mul_shift (φ ψ : AffineCartanMap K V) :
>     (φ * ψ).shift = φ.shift + φ.lin ψ.shift := rfl

> @[simp] theorem inv_shift (φ : AffineCartanMap K V) :
>     (φ⁻¹).shift = -φ.lin.symm φ.shift := rfl

A backward step is the inverse of the stored forward link
(`ArchiveAffineCartanConnection.lean:174-178`):

> /-- Affine pull of one oriented step. Backward is the inverse of the stored forward link. -/
> def affineStepMap (A : AffineCartanConnection N K V) :
>     ChainStep → ArchiveRolePhaseGroup N → AffineCartanMap K V
>   | .fwd r, x => A x r
>   | .bwd r, x => (A (roleTranslateMinus N r x) r)⁻¹

The covariant sum is the head translation plus its linear action on the rest
(`ArchiveAffineCartanConnection.lean:186-192`):

> /-- Covariant translation sum `θ₁ + U₁ θ₂ + U₁ U₂ θ₃ + ⋯`. -/
> def covariantShift (A : AffineCartanConnection N K V) :
>     List ChainStep → ArchiveRolePhaseGroup N → V
>   | [], _ => 0
>   | s :: rest, x =>
>       (affineStepMap A s x).shift +
>         (affineStepMap A s x).lin (covariantShift A rest (stepTarget N s x))

Open torsion expands by the same product rule
(`ArchiveAffineCartanConnection.lean:409-419`):

> /-- Translation defect `T = a - b`. -/
> def affineOpenTorsion (A : AffineCartanConnection N K V) (r s : Role)
>     (x : ArchiveRolePhaseGroup N) : V :=
>   (affineSquareA A r s x).shift - (affineSquareB A r s x).shift

> theorem affineOpenTorsion_expand (A : AffineCartanConnection N K V) (r s : Role)
>     (x : ArchiveRolePhaseGroup N) :
>     affineOpenTorsion A r s x =
>       (A x r).shift + (A x r).lin (A (roleTranslatePlus N r x) s).shift -
>         ((A x s).shift + (A x s).lin (A (roleTranslatePlus N s x) r).shift) := by

Based holonomy is the square product, and the header keeps it distinct from
open torsion (`ArchiveAffineCartanConnection.lean:19-21`, `:574-576`):

> Open torsion gauges by `T' = g_x T - F' b_y`. The translation term is absent
> only when `F'` kills `b_y`. Based torsion is `t = T + (I - P) b`, so it agrees
> with open torsion only when `P` fixes `b`.

> def affineBasedHolonomy (A : AffineCartanConnection N K V) (r s : Role)
>     (x : ArchiveRolePhaseGroup N) : AffineCartanMap K V :=
>   affineSquareA A r s x * (affineSquareB A r s x)⁻¹

The registry sentence for that distinction is
(`02_REGISTRY/claims.csv:877`):

> Based holonomy differs from that open pair when the linear holonomy is not the identity.

The same row says the path theorem is already owned and that no action is
selected:

> Path transport multiplies linear parts and sums the covariant shift, and a node gauge leaves only the endpoint factors.

> No physical Hodge kernel or constitutive action is selected.

The #227 solder schematic is a different tensor. Its translation slot is
absent (`A4D_227_TORSION_DIAGNOSTIC.md:35`):

> The schematic is therefore correct for this convention. It is not the affine open torsion of `affineOpenTorsion`, which is a difference of translation shifts. The #227 links are pure Lorentz matrices, so that translation defect is the zero vector on every phase and face, for every \(t\).

The ten-name shift closure of the previous candidate does not contain
`covariantShift` or `affineOpenTorsion`.

## The evaluation

The arithmetic uses the quoted product, inverse, and head-plus-remainder
rules. It does not assign the constant-shift values in advance.

For \((I,b)\) the inverse translation is \(-b\). One forward step therefore
returns \(b\), and one backward step returns \(-b\). Two forward steps
return \(b+Ib=2b\). Both square paths are \((I,2b)\), so their translation
difference is \(0\). The expansion in the four edge translations gives the
same \(0\). Based holonomy is \((I,2b)(I,-2b)=(I,0)\), so it agrees here.

The positive unit ray is the rational predicate already used for the
diagonal seed: squared length \(1\), parallel to \(b\), and positive inner
product with \(b\). No square root is formed. At \(b=e_0\) and at
\(b=-e_0\) the forward step equals \(b\), and the predicate accepts that
value as the ray of that same \(b\). The value \(-e_0\) is not the ray of
\(e_0\): the sign rejects it. At \(b=2e_0\) the forward step is \(2e_0\); the
predicate accepts \(e_0\) and rejects \(2e_0\). The backward step of \(e_0\)
is \(-e_0\), which is not the ray of \(e_0\). Open torsion at \(b=e_0\) is
the zero vector, which is not that ray.

If the predecessor edge in direction \(r\) carries \(e_0\), the far \(s\)
edge carries \(e_1\), the local \(s\) edge carries \(0\), and the far \(r\)
edge carries \(e_0\), with every linear part the identity, the expansion
returns \(e_1\). The constant-shift cancellation uses the common
translation.

If the first step is the coordinate swap and both translations are \(e_0\),
the two-step sum is \(e_0+e_1\), not \(2e_0\).

On that same swap at the \(r\) edge and identity elsewhere, open torsion is
\(e_1-e_0\) and based torsion is \(e_0-e_1\). They differ. Their difference
is \((I-P)\) on the square-\(B\) translation, which is the owned relation
`open_based_torsion_relation`. The zero statement does not extend to based
torsion off the identity family.

## Verification

`02_REGISTRY/research/certificates/a4d_native_covariant_shift_open_torsion_ray_check.py`.

Negative controls, each able to change the conclusion:

- The forward step at \(b=e_0\) is the positive ray of \(e_0\). A statement that the path sum never meets the ray fails on this sample.
- The forward step at \(b=-e_0\) is the positive ray of \(-e_0\) and is not the positive ray of \(e_0\).
- The forward step at \(b=2e_0\) is not the positive ray. The predicate still accepts \(e_0\).
- The backward step at \(b=e_0\) is \(-e_0\). Using the forward formula there fails the check.
- A site-dependent translation makes open torsion \(e_1\), not \(0\).
- A swap on the first step makes the two-step sum \(e_0+e_1\), not \(2e_0\).
- The swap witness makes based torsion differ from open torsion. Equating them on every connection fails that witness.
- \(-e_0\) is rejected by the sign, \(2e_0\) by the length, and \(e_0\) against the zero shift by the sign. There is no separate zero branch.

Reproduce with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_covariant_shift_open_torsion_ray_check.py
```

## Named risks and pre-registered attack surface

The strongest self-attack is to read the coincidence at \(b=e_0\) as “the
covariant sum is the record ray.” The named second object is \(b=2e_0\): the
sum is \(2e_0\), while the positive unit ray is \(e_0\). The map returns the
translation, not \(b/\sqrt{b\cdot b}\).

Next attacks:

- Calling the zero open torsion a vanishing of every torsion. Based torsion on the swap witness is the second object, and the claims row already states that difference.
- Treating the #227 zero as this result. Those links have no translation slot.
- Re-proving `affinePath_shift_eq_covariant_sum` or `affineOpenTorsion_gauge`. They are cited.
- Promoting the two definitions to a complete interface. `nilpotentAffineGenerator` still takes a free `RoleSpace`, and the preparation checker still contains the unselected normalization. `ResponseDecomposition.shift` remains a scalar gauge, not this translation.
- Dropping the constant-shift or identity-linear hypothesis. The site-dependent face and the swap step are the reopening hooks.

## What this does not show

This does not select \(n_e\) from \(b_e\). It does not compare the ten-slot
covector with \(\rho_0\). It does not cancel an archive remainder. The live
gate on `conditional_endogenous_preparation` stays:

> The direct route through ArchiveAffineExteriorLink, archiveAffineLinkedHodgeDirac and archiveSolderedDirac is ruled out: all are invariant under changes of affine shift at fixed linear links (see conditional_archive_shift_blindness). Do not infer b_e->n_e from these transports. The next arrow is a separate already-owned local record/preparation law that reads b_e, with its action, joint variation, full-support preparation and refinement; if none exists, prove completeness of the actual interface before claiming obstruction. Then combine all owned heat/action terms with the candidate ten-slot covector and compare the total source with rho0; keep parent terminals open.

The coframe–curvature principle \(\mathfrak{V}\), the own action, Ward
identity, refinement, curved roots, soundness and recovery, G0, and the
parent terminals remain open.
