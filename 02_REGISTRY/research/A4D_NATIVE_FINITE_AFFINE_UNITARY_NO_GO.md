# Finite fixed-pairing unitary carriers erase affine translations

**Scoped theorem, 15 October 2026.** The shift-refinement obstruction for the
positive-ray readout extends to every finite-dimensional, differentiable
representation of the affine Lorentz action whose pure translations are
unitary on one fixed positive carrier. If Lorentz links act by invertible
covariant conjugation and affine paths act by operator composition, every
translation acts as the identity. The result applies at a fixed positive CAR
pairing; it does not exclude a level-changing or infinite-dimensional memory
process.

## Native inputs and the exact scope

The owned affine link law is

```text
(D1,b1) (D2,b2) = (D1 D2, b1 + D1 b2).
```

This is the `AffineCartanMap.mul` law in
`D0.Geometry.ArchiveAffineCartanConnection`. The fixed role metric has signs
`(+1,-1,-1,-1)` in `A4DSolderMetricCompletion`; its linear stabilizer contains
the standard proper Lorentz group on the four-dimensional shift space. The
current exterior CAR link explicitly
uses only the linear part and is invariant under changing the affine shift;
`archiveAffineExteriorLink_shift_irrelevant` proves that fact.

Test the strongest fixed-carrier completion of that missing shift action:

1. a finite-dimensional complex carrier has a fixed positive inner product;
2. pure translations are represented by a differentiable unitary
   homomorphism `T(b)` of the additive shift space;
3. Lorentz links are invertible on that carrier and satisfy the affine
   covariance law `S(D) T(b) S(D)⁻¹ = T(Db)`;
4. path concatenation acts by operator multiplication, as required of a
   representation of the owned affine composition law.

No assumption that the Lorentz implementers `S(D)` are unitary is needed.
The theorem is local to the fixed positive pairing and finite carrier. A
field-dependent pairing, nonunitary channel, path-dependent non-homomorphic
instrument, or refinement that changes the carrier lies outside it.

## Proof

Differentiate the translation homomorphism at zero. After multiplying its
skew-Hermitian generators by `-i`, obtain a real-linear map

```text
P : R^(3,1) → Herm(N),
```

with `S(D) P(v) S(D)⁻¹ = P(Dv)`. Define

```text
Q(v) = Tr(P(v)^2).
```

Hermiticity gives `Q(v) = sum_ij |P(v)_ij|² ≥ 0`. Similarity invariance of
trace gives `Q(Dv)=Q(v)`. Since `P` is linear, `Q` is a real quadratic form.

The Lean capsule proves the decisive finite-dimensional algebraic lemma. It
uses exact half-turns, quarter-turns in the spatial planes, and the exact
Lorentz boost with `(gamma, gamma beta)=(5/3,4/3)`. The rotations remove the
six mixed coefficients and make the three spatial coefficients equal. Boost
invariance forces the remaining form to be

```text
Q(t,x,y,z) = c (t² - x² - y² - z²).
```

The boost is also the already-owned `rationalABBoost_lorentz` in
`A4DObserverPositiveExterior.lean`. A separate Lean theorem proves that its
action in the declared `(t,x,y,z)=(A,B,C,D)` coordinates is exactly the
coordinate boost used in the coefficient theorem; its source is pinned by
the exact certificate. Nonnegativity on the time basis vector gives `c ≥ 0`;
nonnegativity on a spatial basis vector gives `-c ≥ 0`. Hence `c=0` and
`Q=0`. The sum-of-squares
identity then gives `P(v)=0` for every `v`. Exponentiation of the translation
generators yields `T(b)=I` for every shift. The D0 real orthogonal CAR carrier
is included by complexification. Thus exact subdivision, fixed
finite positive-pairing unitarity, and Lorentz covariance cannot all carry a
nontrivial affine-origin response.

## What the theorem says about memory and gravity

This is a stronger obstruction than the positive-ray result: retaining the
magnitude of `b` on the same finite CAR space does not repair the problem if
the full Lorentz covariance and exact path law are retained. A nontrivial
affine-origin response must use a larger mathematical class. Possibilities
that remain open in D0 include a refinement tower whose carrier changes with
level, an infinite-dimensional limit, or a nonunitary/stateful channel with
its own composition and readout laws. The theorem does not select any of
these, and it does not prove that D0 supplies one.

The connection to gravity is deliberately limited. The obstruction shows why
the existing finite CAR exterior lift cannot itself be the complete
translation-sensitive field mechanism. It does not derive a metric source,
Ward identity, Einstein equation, curved solution, soundness, or recovery.
G0 and positive ОТО remain open. It is not a no-go for the full D0 core and
does not alter #310, #202, or #317 terminal contracts.

## Sharpness: an infinite-dimensional affine memory representation exists

The finite obstruction is sharp as a representation statement. On
\(\mathcal H=L^2(V^*,d^4k)\), where \(V\) is the already present real shift
space, define

```text
(T(b)ψ)(k) = exp(i k(b)) ψ(k),
(R(D)ψ)(k) = ψ(Dᵀ k),
U(D,b)     = T(b) R(D).
```

For Lorentz `D`, `|det D|=1`, so `R(D)` preserves the Lebesgue `L²` norm;
`T(b)` is unitary by pointwise multiplication. Direct substitution gives
`R(D)T(b)R(D)⁻¹=T(Db)` and therefore

```text
U(D1,b1) U(D2,b2) = U(D1 D2, b1 + D1 b2).
```

For every nonzero `b`, the multiplier `exp(i k(b))` is nonconstant on a set
of positive measure, so `T(b)≠I`. Thus an infinite-dimensional memory can
retain a nontrivial translation while respecting exact affine subdivision.
This is an existence control on the affine group, not an admitted D0
construction: it does not identify the CAR/AF refinement with this `L²`
carrier, does not preserve distinct scene loops having the same affine
endpoint, and supplies no physical source or metric dynamics. The remaining
G0 question is whether the existing native history tower induces a larger
carrier and action of this kind from its own owners.

## Verification

The analytic implication from a smooth unitary affine representation to its
Hermitian generators is the ordinary finite-dimensional matrix Lie-group
calculation. The coefficient theorem is checked in Lean without user axioms;
the exact checker separately verifies all listed rational Lorentz matrices
and hostile controls. It also verifies properness and time orientation, checks
the exact owned-role boost coordinate bridge, and replays the hash-pinned Lean
transcript portably. The standalone compiler replay is available separately.

```sh
python3 02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic_check.py
```

To compile the capsule again with the local Lean toolchain and compare the
compiler transcript byte-for-byte, run:

```sh
python3 02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic_check.py --runtime-check
```

The Lean capsule, compiler transcript, exact-control output, and pinned source
hashes are adjacent to this note. No supported owner, action, selector,
physical postulate, or registry status is changed.
