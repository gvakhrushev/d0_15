# A4D J² — exact obstruction to uniform coupled normal rescue

**Task:** `EXP-A4D-J2-UNIFORM-COUPLED-NORMAL-RESCUE`
**Execution:** PR #227
**Baseline:** `5523d8f679c1ea02f9b73d757c81649740010d0a` (merged #216)
**Review refresh:** `8639bcde495966629990772867b0d0e9e7de4635` (merged #225)
**Status:** exact research terminal B; no release/Lean claim
**Certificate:** [a4d_j2_uniform_coupled_normal_rescue_check.py](certificates/a4d_j2_uniform_coupled_normal_rescue_check.py)

## 0. Terminal

\[
\boxed{\texttt{NAKED-STAR-J2-COUPLED-NORMAL-RESCUE-NOGO}}
\]

The declared estimate fails already for the fixed smooth flat metric. There is
an analytic, genuinely curved family of **full connection-stationary** links
through identity on every four-dimensional torus of side length \(L=4m\).
All independent edge equations vanish; the metric partial does not vanish.

For the designated smooth sheet \(K_h^{\rm sm}=I\),

\[
r_h=E_K(\eta,I)=0,
\qquad
E_K(\eta,K(t))=0,
\qquad
d_\perp(K(t),\mathcal Z_h^{\rm sm})\asymp |t|>0
\quad(t\ne0).
\tag{0.1}
\]

Consequently no \(C,p,\beta>0\) can give the proposed estimate for **every**
stationary sheet in an actual neighborhood of the smooth/flat fiber. This
failure is exact at each such refinement; it is stronger than deterioration
of a Hölder exponent with mode count.

There is also a local response obstruction. With \(h=1/L\), \(t=h^2\), and
center \(x=0\), the genuine metric direction \(q_{11}\) has

\[
\boxed{
 h^{-2}E_Q(\eta,K(h^2))(0)[q_{11}]
 =-\frac{4}{4-3h^4}\longrightarrow-1,
 \qquad h^{-2}E_Q(\eta,I)(0)[q_{11}]=0.
}
\tag{0.2}
\]

The density has the unit coefficient used in the #201/#208 certificates. Any
fixed nonzero overall action coefficient multiplies both sides of the response
calculation and leaves the obstruction intact. Since \(G[\eta]=0\), (0.2)
contradicts the advertised local Einstein response on **all** flat-approaching
connection-stationary sheets in a link neighborhood.

This does not invalidate the already-owned infrared Einstein seed, the smooth
approximate sheet, or a response theorem for an additionally specified branch.
It does not assert a joint \(E_Q=E_K=0\) curved vacuum: the nonzero \(E_Q\) is
part of the obstruction here.

## 1. Inputs and scope

The calculation retains the naked star action, the #201 genuine Gram metric
lift, the #208/#216 polarized connection conventions, and the full nonlinear
Lorentz quotient. Mandatory inputs are:

- [#216 fixed-realization/IR memo](MEMO_A4D_J2_SMOOTH_RESONANCE_CLOSURE.md)
  and [its exact IR certificate](certificates/a4d_j2_fixed_realization_ir_check.py);
- [#201 physical quotient/seed](MEMO_A4D_RESOLVED_AFFINE_PHYSICAL_QUOTIENT.md);
- [E-NJET](ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md) and
  [typed reconstruction](ATORUS_TYPED_RESPONSE_RECONSTRUCTION.md);
- [#223 normal-coordinate locality](A4D_J2_NORMAL_COORDINATE_LOCALITY.md)
  and its certificate;
- [#208 corrected polarized owner](MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md)
  and the corrected #216 resonance certificate;
- #202 full-transverse E2 certificate at checkpoint
  `cd91d8cafb51b0b6d0fc96030bac06e1f43054ad`: its equations force
  \(j=\gamma=\delta=0\), rather than admitting the old claimed flat
  \(j\)-modulus. It is a hostile variation control, not an input theorem.

The result below does not alter #202, redo #223, solve the sourced diagonal
reduction, or compute the first slow-background correction owned by #225.
It proves a zero-source identity in the original action, with independent
variations of every edge. The response-sensitivity worker #226 is separate;
its then-Ready, unmerged checkpoint `fb0fa2bf5e736cf69a979d4e75fb8eb3f98c57a7`
is discussed only in §7. No unmerged theorem is needed for this terminal.

### 1.1 Fixed realization

Take the smooth metric \(g=\eta=\operatorname{diag}(1,-1,-1,-1)\), sampled
without any \(h\)-dependent modification. In the raw solder convention,
\(\Theta=\eta\) and the four internal legs are \(v_r=e_r\). Thus

\[
Q=\Theta\eta\Theta^T=\eta,
\qquad K_{x,r}=\eta L_{x,r}\eta.
\tag{1.1}
\]

The standard smooth sheet is the exact flat connection. It is an admissible
special case of the #216 approximate construction, with residual identically
zero. Use \(L=4m\), \(m\ge2\), to keep the radius-two reconstruction no-alias
guard while taking \(h=1/L\to0\).

### 1.2 Actual action

For \(r<s\),

\[
P_{rs}(x)=L_r(x)L_s(x+r)L_r(x+s)^{-1}L_s(x)^{-1},
\qquad \mathcal C(P)=\tfrac12(P-P^{-1}),
\tag{1.2}
\]

\[
S_\star=\sum_{x,r<s}\epsilon_{rsuv}
 (v_u\wedge v_v)^T G_2\star\mathfrak b(\mathcal C(P_{rs}(x))).
\tag{1.3}
\]

Here \(\mathfrak b(C)_{ab}=(C\eta)_{ab}\), \(u<v\) complement \(r,s\),
and the Lorentz generators and star signs are exactly those of the owners.
The smooth differential is

\[
D\mathcal C_P[\dot P]=\tfrac12(\dot P+P^{-1}\dot P P^{-1}).
\tag{1.4}
\]

## 2. A single analytic family, with a refinement-independent definition

Write \(B_s=K_s\) for the standard internal boost in plane \((0,s)\), and

\[
B=B_1+B_2+B_3,
\qquad B^3=3B.
\]

For real \(|t|<2/\sqrt3\), define the Cayley boost

\[
U(t)=(I-tB/2)^{-1}(I+tB/2)
 =I+\frac{4t}{4-3t^2}B+\frac{2t^2}{4-3t^2}B^2.
\tag{2.1}
\]

It is proper Lorentz, belongs to the identity component near zero, and
\(U(-t)=U(t)^{-1}\). On the torus let

\[
p(x)=x_0+x_1+x_2+x_3\pmod4,
\quad
(W_0,W_1,W_2,W_3)=(U,I,U^{-1},I),
\]

\[
\boxed{L_0(x)=W_{p(x)},\qquad L_s(x)=I\quad(s=1,2,3).}
\tag{2.2}
\]

For every \(L=4m\), **all** Role shifts increment \(p\) by one, including
periodic wraps. This proves that the same local formula defines a field on
every refinement in this subsequence, rather than only on one \(L=4\) orbit.
There is no new channel, invariant, filter, or action parameter.

The plaquettes are

\[
P_{0s}(x)=W_pW_{p+1}^{-1}=:
P_p=(U,U,U^{-1},U^{-1})_p,
\qquad P_{rs}(x)=I\quad(1\le r<s).
\tag{2.3}
\]

## 3. Full connection stationarity: an independent-edge proof

At standard solder the density of face \((0,s)\), applied to any Lorentz
Lie-algebra curvature \(C\), is

\[
\ell_{0s}(C)=\tfrac12\operatorname{tr}(B_s C).
\tag{3.1}
\]

This sign and coefficient are independently checked against the wedge/star
formula in the certificate. Vary exactly one edge by
\(L_r(x)\mapsto L_r(x)\exp(\varepsilon X)\), where \(X\) is **any** of the
six Lorentz generators. Nothing else in (2.2) is varied with that edge.

### 3.1 Roles \(s=1,2,3\)

The edge enters face \((0,s)\) at base \(x-0\) in its positive second corner,
and at base \(x\) in its negative fourth corner. Applying (1.4) gives one
quarter of the trace pairing with

\[
\mathcal G_s(p)=
 W_p^{-1}B_sW_{p-1}+W_{p-1}^{-1}B_sW_p
 -B_sP_p-P_p^{-1}B_s.
\tag{3.2}
\]

For the four values of \(p\), direct substitution gives the **zero matrix**.
For example, at \(p=1\), both positive and negative terms are
\(B_sU+U^{-1}B_s\). At \(p=0\), both are
\(U^{-1}B_s+B_sU\). The other two phases replace \(U\) by \(U^{-1}\).

The two spatial faces involving Role \(s\) have identity links throughout;
their independent positive/negative edge derivatives cancel at constant
solder. Hence every one of their transverse variations also vanishes.

### 3.2 Role \(0\)

For each face \((0,s)\), the varied edge occurs positively at base \(x\) and
inversely at base \(x-s\). Sum these three incident face pairs. The derivative
is one quarter of the trace pairing with

\[
\mathcal G_0(p)=
 W_{p+1}^{-1}BW_p+W_p^{-1}BW_{p+1}
 -W_p^{-1}BW_{p-1}-W_{p-1}^{-1}BW_p.
\tag{3.3}
\]

At \(p=0,2\) this is zero by equality of the preceding/following identity
links. At \(p=1,3\) it is respectively

\[
[U-U^{-1},B],\qquad-[U-U^{-1},B],
\]

which vanish since \(U\) is a rational function of \(B\).

Thus all six Lorentz variations vanish on all four Roles, independently at
**every single edge**, on **every** \(L=4m\) torus:

\[
\boxed{E_L(\eta,L(t))=0\quad\text{exactly}.}
\tag{3.4}
\]

The full lattice differential is the sum of these independent-edge
coefficients. Therefore (3.4) includes arbitrary coupled Fourier variations,
all tangent/normal equations, and all harmonics generated by the nonlinear
links. The finite four-phase computation evaluates coefficients of this full
differential; it is not the gradient of an ansatz restriction.

The certificate differentiates all six incident plaquettes for a single edge,
for each of the \(4\cdot4\cdot6=96\) phase/Role/generator choices. It also
checks (3.2)–(3.3) as matrix identities. The analytic local proof, rather than
an orbit inventory or finite spectrum scan, supplies the all-refinement claim.

A constant background is a valid subcase of the required universal theorem.
A positive theorem would need arbitrary slow backgrounds; an exact
counterexample on one admissible background with unbounded refinement already
falsifies that theorem. No inference from frozen isolation is used.

## 4. Curvature and the genuine quotient

Put \(c(t)=4t/(4-3t^2)\) and \(\sigma_p=(1,1,-1,-1)_p\). Then

\[
\mathcal C(P_p)=\sigma_p c(t)B,
\quad
\|\mathcal C(P_p)\|_F=\sqrt6|c(t)|,
\quad
\operatorname{tr}P_p-4=\frac{12t^2}{4-3t^2}.
\tag{4.1}
\]

For \(0<|t|<1/4\), these plaquettes are not identity. Their nonzero trace
defect is invariant under local Lorentz conjugation. The family is genuinely
curved; an action value or a restricted gradient cannot turn it into a flat
modulus.

Moreover the nondegenerate solder quotient has coordinates \((Q,K)\) from
(1.1). They are invariant under the original local Lorentz gauge, and the
pointwise solder stabilizer is trivial. This family therefore survives the
actual quotient. Gauge directions or genuine physical **flat** moduli cannot
remove (4.1). Even its first tangent has nonzero linearized curvature.

### 4.1 Uniform normal-distance bounds

Use the dimensionless logarithm chart, Frobenius fibre norm, and
\(d_\infty=\sup_{x,r}\|A_{x,r}-A'_{x,r}\|_F\). Let the local chart satisfy
\(\sup\|A\|_F\le\rho\), for the witness and for the candidate flat moduli.
The logarithm of \(U\) is

\[
\log U(t)=a(t)B,
\qquad a(t)=\frac2{\sqrt3}\operatorname{artanh}(\sqrt3t/2).
\]

On \(|t|\le1/4\), \(|t|\le|a(t)|\le(64/61)|t|\).
The exponential and four-factor product estimates give, independently of
lattice cardinality,

\[
\|\mathcal C(P(A))-\mathcal C(P(A'))\|_F
\le4e^{4\rho}d_\infty(A,A').
\tag{4.2}
\]

Indeed each exponential or inverse exponential has derivative norm at most
\(e^\rho\); telescope four products for \(P\) and for \(P^{-1}\), then use
the factor \(1/2\) in \(\mathcal C\). For **any** flat comparison field,
\(\mathcal C(P(A'))=0\). Taking an infimum over the genuine flat fiber gives

\[
\boxed{
\frac{\sqrt6}{4e^{4\rho}}|t|
\le d_\perp(K(t),\mathcal Z_h^{\rm sm})
\le\frac{64\sqrt6}{61}|t|.
}
\tag{4.3}
\]

The upper bound uses the identity sheet; the lower bound even allows all flat
connections in the local chart, a larger set than the permitted smooth/flat
moduli. Dressed conjugation by \(\eta\) preserves these norms. A physical
connection norm \(A/h\) merely adds the known factor \(h^{-1}\).
The same obstruction holds in the Wiener norm: \(A(t)\) has two character
coefficients, and \(\|A(t)\|_{W^0}=\sqrt6|a(t)|\), uniformly in \(L\).

With \(r_h=0\), any positive \(\beta\) makes the proposed rescue right side
zero. Every genuine open tube contains a nonzero sufficiently small \(t\)
from this family, even if its radius shrinks with \(h\). Thus G3 fails without
any limiting argument or small-denominator estimate.

If the tube has finitely many polynomially weighted derivative bounds, take
\(t_h=h^M\) with \(M\) large enough. If superalgebraic smallness of all
weighted seminorms is imposed, take \(t_h=\exp(-1/h^2)\): G3 still fails exactly
since its right side is zero. Such a choice alone does not obstruct G7; the
strong local-response witness in §5 uses the ordinary dimensionless/physical
link neighborhood and \(t_h=h^2\).

## 5. The metric response is a genuine Gram derivative

At \(\Theta=\eta\), the owner lift of a symmetric metric perturbation is

\[
H(q)=\tfrac12q\eta,
\qquad \delta v_r=H(q)_{r,:}^T,
\qquad DQ[H]=H\eta+\eta H^T=q.
\tag{5.1}
\]

Differentiate the wedge in (1.3) at a single site, with the plaquette held
fixed. List the ten directions in order
\((00,01,02,03,11,12,13,22,23,33)\). The exact covector is

\[
\boxed{
E_Q(x)=\sigma_{p(x)}c(t)
 (0,0,0,0,-1,1,1,-1,1,-1).
}
\tag{5.2}
\]

For off-diagonal directions, the listed coefficient contracts with a symmetric
basis having both entries equal to one. This convention matches #201.
In particular \(E_Q(x)[q_{11}]=-\sigma_{p(x)}c(t)\).

There is no change-of-section error in this calculation. Changing a metric
lift while holding another connection chart coordinate fixed adds a
connection variation and possibly a vertical Lorentz variation. The former
contracts with the **full** \(E_L=0\) of (3.4); the latter vanishes by exact
Lorentz covariance. Therefore (5.2) is the descended metric partial on this
stationary correspondence, not a fake solder response.

At \(x=0\), \(p=0\) for every refinement. With \(t=h^2\), equations (0.2)
follow exactly. Dimensionless links satisfy \(\|\log L\|=O(h^2)\), and the
physical connection satisfies \(\|\log L/h\|=O(h)\). Both approach the same
flat connection. Nevertheless their normalized local metric responses differ
by a nonzero limit. This violates G7 and the all-sheet local J² target on the
fixed flat realization.

The phase average of (5.2) is zero. A weak/averaged limit is consequently a
different question; the required local response at the center is pointwise.
A hypothesis selecting only the designated smooth sheet could exclude the
witness, but that would replace the current all-sheet rescue obligation.

## 6. Hostile controls and proof boundaries

The checker rejects two nearby mistakes:

1. replacing \((U,I,U^{-1},I)\) by \((U,I,U,I)\) produces nonzero full
   side-Role Euler components;
2. retaining the correct wave but replacing \(B_1+B_2+B_3\) by \(B_1\)
   produces nonzero Role-0 rotation Euler components.

These controls catch an action-flat or boost-only restricted-gradient proof.
All equations of the successful family were checked over rational functions
of \(t\), with no numerical root tolerance.

The required scalar \(u^3-hu\) regression is retained explicitly, by writing
\(h=a^2\) and checking the three roots \(0,\pm a\). It is not used as an
actual-star counterexample. Equations (2.2)–(3.4) supply that counterexample.
In fact the actual flat star germ here has an entire analytic zero-source
curve already at constant background. A frozen sourced root or odd-degree
argument elsewhere cannot exclude it. This is consistent with, and does not
recompute, the sourced diagonal quartic analysis in #216.

The counterexample does not establish a lack of exact sheets for arbitrary
slow metrics. G2 holds for this flat example because the identity is exact.
What it disproves is the joint G1–G7 rescue/branch-independence contract.
A theorem with a narrower specified connection-selection rule remains a
separate problem; no such rule is inserted into this action in this PR.

## 7. Quantitative inventory and handoff

| Gate | Result in this terminal |
|---|---|
| G1 full variables | The witness solves the actual full lattice differential: all independent link directions, every site, every \(L=4m\); no claim of a positive theorem for all slow metrics. |
| G2 exact existence | Identity and the analytic family are exact for the fixed flat metric. Existence for arbitrary smooth backgrounds is not proved or needed for the obstruction. |
| G3 uniform normal rescue | **False:** (4.3) has positive normal distance while the designated residual is exactly zero. No exponent or polynomial loss repairs it. |
| G4 gauge/flat moduli | Dressed coordinates and nonzero invariant plaquette trace certify a physical curved direction; it is excluded from genuine flat moduli. |
| G5 response sensitivity | The family has exact raw response (5.2), linear in \(t\) to leading order; normalization has loss \(h^{-2}\). #226 separately supplies a general finite-stencil estimate, at the unmerged checkpoint identified above. |
| G6 hostile control | Scalar regression passes; actual zero-source full-star curve is stronger evidence than the scalar analogy. No frozen-isolation promotion. |
| G7 branch independence | **False** in a link neighborhood: \(t=h^2\) gives (0.2) at the same fixed flat metric/center. |

The strongest estimates obtained here are the two-sided, refinement-independent
normal-distance bound (4.3) and the **exact** response identity (5.2). Along
this family \(\|E_Q\|_\infty=|c(t)|\asymp |t|\) in the ten coefficient norm,
so raw exponent zero and normalized loss \(h^{-2}\) are sharp. This uses no
unproved result from the sensitivity worker.

**Smallest obstruction:** the explicit analytic curved zero-source family
(2.2), not an unproved quantitative inverse estimate. G3 and G7 therefore
cannot be completed under the present all-sheet contract. Terminal B is
reached; there is no remaining calculation required to establish this no-go.
The original Einstein seed and selected approximate IR theorem retain their
previous scoped status. No CORE/public/Lean claim is promoted.

### Reproduction

```text
python3 02_REGISTRY/research/certificates/a4d_j2_uniform_coupled_normal_rescue_check.py
```

The checker passes 52 exact checks and prints the terminal. Process/generated-view,
claim-strength, syntax, and diff gates are recorded in the PR handoff. This
research result does not modify Lean owners and does not require a Lean build.
