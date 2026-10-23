# Curved Y symbol: local analytic division and the owner sum norm

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input head: `d76b27cd69d2842a14721144367b34f9dc4d71fd`.
Status: unconditional local analytic theorem, with conditional global and
flat nonlinear consequences. The physical compact-complement rank premise
is **not proved**. The curved response task stays Draft / `IN_PROGRESS`.

The correct target is the transverse field and center gradient. A constant
Y amplitude is an exact physical modulus and must remain free. The task
uses an unweighted sum over physical sites; a useful inverse must act in
that norm with a constant independent of the period.

## 1. Physical coordinates and a finite target

Let Q be the literal `136 x 96` rational joint Bloch stencil at the
constant z=1 Y vacuum. Here Q denotes the symbol, not the background metric.
Its inputs are `(phase,role,generator)`; outputs are 96 connection rows
and 40 Gram metric rows.

The owned injection B removes the Y direction independently from the
phase-0 and phase-2 temporal rotation slots. It retains 90 standard
coordinates and the two plane vectors `(1,1,0)` and `(0,1,1)` in each
exceptional slot. Its coordinate projection P uses the exact dual rows

\[
(2,1,-1)/3,\qquad(-1,1,2)/3.
\]

C has two columns, `(4/7)Y` in the phase-0 temporal slot and `-(4/7)Y`
in the phase-2 slot. They are the literal right-trivialized Cayley
amplitude derivatives at one. The amplitude projection A has rows
`(7/12)(1,-1,1)` and `-(7/12)(1,-1,1)` in those slots. Exactly,

\[
PB=I_{94},\quad AC=I_2,\quad PC=0,\quad AB=0,\quad BP+CA=I_{96}.
\]

Thus u=Bw+Cc with no discarded coordinate. On the physical carrier c is
one scalar field on the even-sum sites, recorded on its two phases.
For p=0,2 and s=1,2,3 its graph moves give

\[
(D_s^-c)_p=(\lambda_s/\lambda_0-1)c_p,\qquad
(D_s^+c)_p=\lambda_s\lambda_0c_{p+2}-c_p.
\]

The phase is reduced modulo four. The second expression includes the
actual phase interchange; erasing it changes the kernel at i. Define

\[
T(\lambda)u=(Pu,D_{\mathcal G}Au),\qquad
\mathcal G=\{e_s-e_0,e_s+e_0:s=1,2,3\}.
\]

T has 106 rows: 94 complement coordinates and 12 phase-resolved graph
rows. If any ratio `lambda_s/lambda_0` differs from one, its minus rows
force both center amplitudes to zero. If all ratios are one, write
`lambda_j=mu`. Its plus block is three copies of

\[
\begin{pmatrix}-1&\mu^2\\ \mu^2&-1\end{pmatrix},
\qquad\det=1-\mu^4.
\]

Hence T has complex rank 96 except at the four diagonal fourth roots,
where its rank is 95 and its kernel is exactly the physical Y kernel of Q.
This classifies T, not Q.

## 2. Unconditional folded local module

Near each folded character q, the full joint symbol is analytically
equivalent to 95 invertible coordinates and the four-component ideal

\[
\boxed{(\lambda_0/q-1,\lambda_1/q-1,\lambda_2/q-1,\lambda_3/q-1).}
\]

In particular, a holomorphic matrix M_q exists locally with

\[
\boxed{T(\lambda)=M_q(\lambda)Q(\lambda).}
\]

This is an all-order local identity, not a first-slow truncation.

At q=1 take the owned 95-row graph chart, delete the phase-0 temporal
J12 coordinate, and retain the four residual rows. Write the selected
99 equations as

\[
\begin{pmatrix}S&q_0\\ B_0&b_0\end{pmatrix},
\quad S\in\mathbb C^{95\times95},\quad B_0\in\mathbb C^{4\times95}.
\]

All blocks are functions of the characters. S is invertible near one.
Set x=-S^{-1}q_0 and F=B_0x+b_0. For u=(v,a) and e=v-xa the selected
equations are Se and B_0e+Fa. The owned holomorphic derivative J of F has

\[
\det J=-\frac{62976744635716940958283670688}
                {206230323499945683191645561081}\ne0.
\]

This is the character derivative at one. The angular derivative inserts
i in every column and also has nonzero determinant.

Put t=(lambda_j-1)_j. Hadamard's exact holomorphic identity is

\[
f(t)=H_f(t)t,\qquad H_f(t)=\int_0^1Df(st)\,ds
\]

for f(0)=0, on a sufficiently small neighborhood. Thus F=H_Ft, with
H_F(0)=J invertible. The selected equations recover ta analytically.
The other 37 reduced rows vanish at zero and are analytic combinations
of t. Row subtraction eliminates them, proving the stated module.

The target G=T(x,1) also vanishes at zero because T kills the Y kernel.
Write G=H_Gt. If y and z are the selected 95 and four output rows,

\[
Tu=T_{\rm cols}S^{-1}y+
H_GH_F^{-1}(z-B_0S^{-1}y).
\]

This constructs M_1 without division by |t|. Exact fourth-root covariance
of Q and T transports the identity to all four copies.

The certificate reconstructs the chart from the inexpensive literal
stencil. It checks the physical split, graph placements and covariance,
folded kernels, J, and the constant and kernel-first-jet terms of this
division. The all-order conclusion follows from the analytic identities;
the certificate does not enumerate an infinite Taylor series.

## 3. Conditional theorem in the actual owner sum norm

The **open premise H_TORUS** is

\[
\operatorname{rank}Q(\lambda)=96
\quad\text{on }\mathbb T^4\text{ outside the four folded characters.}
\]

Under this premise a smooth periodic matrix M exists on the entire torus
with MQ=T. Near folded points use the analytic matrices above. On the
compact complement full column rank gives `T(Q^*Q)^{-1}Q^*`. A finite
smooth partition of unity glues the identities. This is a proof device;
the lattice action and Euler equations are unchanged.

The Fourier coefficients M_n are absolutely summable. The kernel on an
L-periodic lattice is their periodization, and

\[
\sum_{r\in V_L}\left\|\sum_{k\in\mathbb Z^4}M_{r+Lk}\right\|
\le\sum_{n\in\mathbb Z^4}\|M_n\|=:C_M<\infty.
\]

Young's inequality gives, for every `1<=p<=infinity`,

\[
\boxed{\|w\|_{p,\mathrm{comp}}+\|D_{\mathcal G}c\|_p
\le C\|Q_{\mathrm{shift}}[Bw+Cc]\|_{p,\mathrm{comp}},}
\]

where C is independent of L and `Q_shift` is the owned finite shift
operator. The graph norm is the maximum of the six physical move norms.
Component-sum and owner Frobenius norms differ only by fixed fibre
constants. In particular p=1 is the unweighted owner sum norm.

One may work first with unrestricted phase-vector fields and then
restrict to the physical subspace, where phase p is supported at sites
whose coordinate sum is p. Coefficient covariance preserves this subspace.
No factor of L or lattice cardinality enters. A constant site weight can
be inserted on both sides.

This proves the norm-level consequence of H_TORUS, not H_TORUS itself.
T has rank 96 away from the folded points, so an additional physical
joint zero would also obstruct a global identity T=MQ.

## 4. Conditional flat nonlinear rigidity under refinement

At the flat standard solder use the actual chart

\[
K=K_Y(1+c)\exp(Bw).
\]

Its full joint derivative at zero is `Q_shift[Bw+Cc]`. The owned
[derivative remainder](A4D_Y_PURE_CENTER_QUANTITATIVE_TRANSPORT.md)
and finite-stencil analyticity give

\[
\|R(c,w)\|_{p,\mathrm{comp}}
\le1152\|c\|_\infty\|D_{\mathcal G}c\|_p+
C_r(\|c\|_\infty+\|w\|_\infty)\|w\|_{p,\mathrm{comp}}.
\]

C_r is finite on a fixed compact chart and independent of L. It is not
a numerically certified constant. Under H_TORUS choose a fixed chart
radius rho<=1/2 with `C(1152+C_r)rho<1`. If all flat joint Euler rows
vanish and `||c||_infinity+||w||_infinity<=rho`, the linear estimate and
remainder imply

\[
\|w\|+\|D_{\mathcal G}c\|
\le C(1152+C_r)\rho(\|w\|+\|D_{\mathcal G}c\|).
\]

Hence w=0 and the graph gradient is zero. The six moves generate the
connected even-sum carrier on every `L in 4N` lattice, so c is constant.
The field is an exact Y vacuum with zero metric response. This proves
flat local joint rigidity modulo the physical constant Y modulus,
**conditionally** on H_TORUS, in a chart independent of refinement.
It does not call Y gauge or establish connection uniqueness.

For a residual f the same absorption gives the conditional stable bound
`(||w||+||D_G c||) <= C/(1-C(1152+C_r)rho) ||f||` in the same norm.
A pointwise residual cannot replace the sum norm.

A nonconstant sampled metric requires separate control of the frozen
family, smooth comparison connection, mixed derivatives, and retained
curved compatibility equations. No normalized response limit follows
by inserting pointwise powers into an unweighted site sum.

## 5. Four short inverse templates are excluded over characteristic zero

A polynomial left inverse of QB would be a stronger route. The exact
calculations exclude these supports for each row of L:

| support | monomials | checked convolution matrix | rank | augmented rank |
|---|---:|---:|---:|---:|
| `0,+/-e_j` | 9 | `8366 x 1224` | 1224 | 1318 |
| literal stencil | 21 | `12314 x 2856` | 2856 | 2950 |
| `sum abs(alpha_j) <= 2` | 41 | `23594 x 5576` | 5576 | 5670 |
| `sum abs(alpha_j) <= 3`, phase-0 sector | 129 | `13431 x 4386` | 4386 | 4409 |

After clearing denominators by 14, ranks are computed exactly modulo
1000000007. Each checked matrix has full column rank, fixing its rational
rank to the column count. The augmented modular rank is already maximal
and larger by every checked target column. Therefore those rational
constant targets cannot lie in the image.

Exact phase covariance splits each convolution system into four blocks.
The first three rows of the table sum all four block ranks. The last
checks only the sector required for a phase-0 constant target: all 23
such targets are independent modulo its image. A full left inverse needs
them, so that sector suffices. The other three degree-three sectors and
their aggregate ranks are not asserted.

None of these templates can satisfy `L(QB)=I_94` over characteristic zero.
This does not rule out a longer template, rational or analytic inverse,
or H_TORUS. It is a scoped exclusion, not a spectral no-go.

## 6. Replay and remaining gate

```bash
python 02_REGISTRY/research/certificates/a4d_y_curved_joint_center_gradient_module_check.py
```

The local module, actual target and four short-template exclusions passed
exact local checks before the execution environment disconnected during
publication. The source and compact result ledger saved here were
reconstructed from those checks; GitHub CI must independently replay this
published reconstruction.

First missing global linear premise: H_TORUS on the physical compact
complement. Its proof would give the owner sum-norm estimate and flat
nonlinear rigidity above without a separate amplitude-smoothness hypothesis.
Curved reduced compatibility and the normalized comparison response remain
the subsequent task-level obligation. Neither physical terminal is asserted.
