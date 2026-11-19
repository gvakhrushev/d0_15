# Literal identity Euler symbol: continuous physical resonance circles

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input head: `de71bf30e9cfd34614fc8178255d456c49ebb8b1`.
Status: exact frozen coefficient and rank certificate; full theory remains open.
The action, Gram quotient and independent-source convention are unchanged.

## Literal placement audit

In the canonical `a4d_designated_full_gap_check.flat_symbols` convention the
physical connection-to-joint symbol is

\[
\mathcal J(\lambda)=\binom{A(\lambda)^T}{C(\lambda)}.
\]

The new certificate independently differentiates the actual four link factors
of every face. Each connection output is assembled at its own link, retaining
the input-minus-output shift. Metric variations are assembled at the face
base. The two Laurent stencils have radius at most one in each coordinate.
Equality at all 81 tensor nodes `{1,-1,i}^4` therefore proves coefficientwise
equality with `(A^T;C)` by unisolvent Laurent interpolation. This is not a
finite rank scan or a sampled gap claim.

At `(a,a,i,i)`, `a=(3+4i)/5`, the literal physical rank is 23; the
wrong-placement stack `(A;C)` has rank 24. This hostile control detects an
error invisible at the diagonal quarter point. The former first-slow and
isolated-parabolic physical interpretations are withdrawn; their scripts are
retained solely as labelled wrong-placement algebra controls.

## Exact lines and ranks

Use generator order `(K1,K2,K3,J12,J13,J23)` and role-supported vectors

\[
T_2=(1,0,-1,0,1,0),\qquad T_3=(1,-1,0,1,0,0).
\]

For every nonzero complex `a`, an exact kernel at `lambda=(a,a,i,i)` is

\[
v(a)=T_2^{(2)}+T_3^{(3)}
-\frac{a-i}{1-i}\bigl(K_1^{(0)}+K_1^{(1)}\bigr).
\tag{1}
\]

The certificate checks every Laurent coefficient in `J(a)v(a)=0`, retaining
the constant nonzero coordinate `v_21=1`. Thus rank is at most 23 on the
entire complex line. Two exact 23-column minor charts give monic gcd

\[
a^{15}(a-i)^4.
\]

For `a !=0,i`, at least one chart is nonzero, so rank is exactly 23. At `a=i`
the full matrix has rank 20. Both determinants are computed by exact
Gaussian-integer polynomial Bareiss division, their gcd over `Q(i)`, and
held-out exact determinant checks. This is an all-parameter theorem on `C*`.

Spatial permutations give variable roles `(0,2)` and `(0,3)`, with all other
phases fixed to `i`. Their selected chart gcds are `a^15(a-i)^4` and
`a^13(a-i)^4`. Clearing powers of `a` are immaterial on `C*`. Real stencil
coefficients give three conjugate lines with fixed phase `-i`.
Restricting `|a|=1` proves six continuous physical resonance circles.

For `L in 4N`, just one circle and its conjugate supply at least `2L` real
kernel coordinates. In physical space (1) is a finite shift construction on
an arbitrary complex envelope on `n=x0+x1`, multiplied by `i^(x2+x3)` and its
conjugate. Removing only diagonal-quarter coordinates cannot remove this
kernel.

## First-slow consequences

An exact 20-column normal elimination at `(i,i,i,i)` gives the physical
`14x4` center derivative `Gamma(k)`. Each individual coordinate derivative
has rank four, consistent with the earlier one-coordinate owners. But

\[
\operatorname{rank}\Gamma(1,1,0,0)=3,\qquad
\Gamma(1,1,0,0)(0,0,1,1)^T=0.
\]

The wrong-placement control has rank four on the same direction. Full
first-slow injectivity over all nonzero real covectors is therefore false.

At `(1,1,i,i)`, the physical first derivative after a 23-column normal
elimination has real rank two, with kernel

\[
\operatorname{span}_{\mathbb R}\{(1,1,0,0),(0,0,1,-1)\}.
\]

The first direction is tangent to (1); the exact Schur residual along the
circle vanishes to every order. No higher-order transverse classification is
claimed. The former eight-point physical torus premise cannot supply an
inverse or a finite polynomial range-loss theorem.

## Exact failure of a quarter-only range inverse

For every `L in 4N`, set `g=eta`, `K_sm=I` and

\[
u_x=\operatorname{Re}\bigl[i^{x_2+x_3}v(1)\bigr].
\]

This nonzero real lattice field has only characters `(1,1,i,i)` and its
conjugate. Both its linear connection residual and its linear metric readout
vanish exactly. Its projection on the diagonal quarter pair is zero, since
those discrete Fourier characters are distinct. Thus a complement removing
only the diagonal quarter fibers still contains an exact kernel, even for
each fixed mesh. No inverse on that complement can have any finite `h^-p`
bound.

This is not a gauge direction. In face `(0,2)` its linear curvature is

\[
(1-i)u_0+(1-1)u_2=(i-1)K_1\ne0.
\]

An infinitesimal pure gauge at I has
`u_r=(lambda_r-1)theta` and zero linear plaquette curvature. The certificate
checks the nonzero curvature coefficient exactly.

This refutes the proposed universal quarter-only linear range-inverse lemma.
It does not refute the designated flat root, which exists exactly, and does
not construct a nonlinear Einstein-response counterexample. A full Target-D
proof must enlarge the transported resonant center or use a different exact
solvability argument. For a strictly curved fixed metric, lifting of these
centers and the remaining connection equations still require proof.

## Nonlinear meaning and scope

A frozen kernel is not an exact nonlinear joint branch. The separate
[nonlinear gates](A4D_IDENTITY_RESONANCE_CIRCLE_NONLINEAR_GATES.md) exclude
small exact phase-erased branches at three four-phase circle carriers.
Arbitrary longitudinal envelopes and their coupling on a fixed genuinely
four-dimensional curved metric still need control.

The one-coordinate `(mu,z,mu,mu)` control and designated rescue remain valid:
they used the physical transpose and a different invariant sector. The
finite-amplitude Y `136x96` symbol is also different; the identity `34x24`
circles neither prove nor disprove its H_TORUS.

The full-class estimate must include transported circle kernels, their
nonlinear metric constraints, and actual shared links. A designated range
solve must also satisfy the remaining center equations. No all-torus
classification, nonlinear source counterexample, full curved continuation or
response-universality terminal follows here.

```sh
python3 02_REGISTRY/research/certificates/a4d_identity_physical_resonance_circles_check.py --expect 02_REGISTRY/research/certificates/a4d_identity_physical_resonance_circles_results.json
```

The certificate uses exact `Q(i)` arithmetic and NumPy object indexing.
