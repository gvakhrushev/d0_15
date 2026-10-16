# Lorentz reflection: the complete curvature and native matter source

2026-10-16. SOURCE #310. Exact differential-geometric continuation of the
[controlled AF price](A4D_NATIVE_JACOBIAN_CONTROLLED_RECORD_SOURCE.md).
The physical metric/record binding and parent terminals remain open.

The positive-record curvature price cannot be renamed a Lorentzian
Einstein-Hilbert price by pointwise signature reflection. The same
reflection produces an explicit observer-derivative term of the **same
order** as the Einstein term. Its full source is determined below. The
term is nonzero on an already owned sixteen-component CAR family, where
the Lorentz metric is flat. On that family it gives a genuine projected
matter Euler derivative, not just a change of the curvature's value.

Nothing is added to the action: this is an exact rewriting of the existing
positive curvature sector under the existing reflection. No future
orientation, foliation, twist-free condition or observer equation is imposed.

## 1. Covariant notation and the native owner

Use h for a positive **covariant** metric and g for a Lorentz covariant
metric of signature(+---). This avoids confusing h with the native
quotient's contravariant Gram slot `q_native=F eta F^T`.
For a smooth h-unit vector field u set omega=h(u,·) and

```text
g=2 omega tensor omega-h,
g^-1=2u tensor u-h^-1,
g(u,u)=h(u,u)=1,
det g=-det h,  dVol_|g|=dVol_h.                       (1)
```

In the [actual matter-observer owner](A4D_NATIVE_MATTER_OBSERVER_PAIRING.md),
g=q_native^-1, J=v, kappa=J^T g J>0, and

```text
u=J/sqrt(kappa),
h=-g+2(gJ)(gJ)^T/kappa.
```

This h is its positive inverse pairing G. Its contravariant Q is h^-1.
The native owner permits its fixed linear P1 readout in the stated class;
the [full CAR current owner](A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md)
has a different nonlinear readout and retains its reference frame/pairing.
Neither choice is silently promoted to the unique physical observer law.
The formulas here apply to either smooth nonzero timelike line when its
own hypotheses hold. Zero/null/spacelike failures retain their old domains.

Section8 supplies a smooth native kinematic lift of any prescribed positive
projector metric h_record. It does not prove that the same existing record
program, evaluated on those lifted fields, produces the prescribed metric
with its full price and history. The curvature/source identity below is the
required consumer of such a physical binding; notation does not supply it.

## 2. The connection difference is explicit

Let nabla=nabla^h and decompose

```text
B_ab=nabla_a u_b=omega_a a_b+K_ab+Omega_ab,
a_b=u^a nabla_a u_b,
K_ab=K_ba, Omega_ab=-Omega_ba,
theta=tr_h K=div_h u.
```

Both indices of K and Omega, and the covector a, are h-orthogonal to u.
Omega uses the usual one-half antisymmetrization. Throughout this memo
`Omega²=Omega_ab Omega^ab` sums both index orders: it is twice the
ordinary differential-two-form norm. All raised indices in Sections2–3
use h. In four dimensions K²=sigma²+theta²/3.

Direct differentiation of (1) in the Levi-Civita formula gives

```text
C^a_bc=Gamma(g)^a_bc-Gamma(h)^a_bc
      =2u^a K_bc-2a^a omega_b omega_c
                  +2omega_c Omega^a_b+2omega_b Omega^a_c.       (2)
```

No field derivative is frozen. In particular the connection is generally
different even when the pointwise reflection matrix is involutive.
Useful complete contractions are

```text
C^a_ab=0,
g^bc C^a_bc=-2(theta u^a+a^a),
(nabla_a g^bc) C^a_bc=8 Omega²,
g^bd C^a_be C^e_ad=-4 Omega².                         (3)
```

For example use an h-orthonormal frame adapted to u at one point. The only
nonzero types are C^0_ij=2K_ij, C^i_00=-2a_i and C^i_0j=2Omega_ij.
Tracing them proves (3) for arbitrary a,K,Omega, not a sampled family.
The first trace also follows from the equal volume densities in (1).

## 3. Exact scalar identity, including twist and boundary

Use the Ricci convention for which a round positive sphere has positive
scalar curvature. The difference formula and C^a_ab=0 imply

```text
Ric(g)_bd=Ric(h)_bd+nabla_a C^a_bd-C^a_be C^e_ad.
```

Contract using (3), differentiating g^-1 as well as C:

```text
R_g=-R_h+2Ric_h(u,u)-2div_h(theta u+a)-4Omega².         (4)
```

Commuting the two covariant derivatives in div a gives the independent
unit-vector identity

```text
Ric_h(u,u)=div_h a-u(theta)-K²+Omega².
```

Substitution, with div(theta u)=u(theta)+theta², yields

```text
R_g=-R_h+2(theta²-K²-Omega²)-4div_h(theta u),
R_h=-R_g+2(theta²-K²-Omega²)-4div_h(theta u).          (5)
```

The two displayed lines are the same rearranged identity. Acceleration
cancels after the Ricci substitution; there is no leftover a² term or
extra acceleration-flux in (5). Expansion, shear and twist remain.
All terms are invariant under u->-u, so no choice of future follows.

For a scalar coefficient c(x), equality of the volume forms gives

```text
integral c R_h dVol_h
 =-integral c R_g dVol_|g|
   +integral c[(4/3)theta²-2sigma²-2Omega²] dVol_|g|
   +4integral theta u(c) dVol_|g|
   -4integral_boundary c theta h(u,n_h) dSigma_h.       (6)
```

The boundary is stated with the h-unit normal, as a Stokes flux for the
common volume density. This is not a derivation of a GHY completion or a
claim of equivalence for unspecified Dirichlet boundary data.

Even a parallel observer gives R_h=-R_g, not +R_g. Geodesicity alone
does not remove K or Omega; a hypersurface-orthogonal observer removes
twist but leaves expansion/shear; a Killing observer can retain twist.
None of these is installed as an admission condition.

## 4. The preceding actual price has an observer term at leading order

For the preceding common controlled family, write

```text
A=B+c R_h+Rem,  c=alpha t²/2>0.
```

The concurrently published [golden matrix-return compiler](A4D_GOLDEN_DETERMINANT_COMPILER.md)
also composes its effect with that same complete AF-price family. For its
declared canonical W_E realization, replace c by
`gamma alpha t²/2`, with the fixed native selector factor `gamma=2p6>0`.
Every identity below is unchanged. Its effect-level composition does not
yet identify the auxiliary compiler's full instrument, archive and cost
with W_E, so that admission premise remains explicit.

If a common physical metric binding and geometric volume measure are
separately proved, its integrated curvature sector becomes exactly (6).
Thus the leading Lorentz form includes

```text
B-c R_g+2c(theta²-K²-Omega²)+4theta u(c)+Rem
```

and the boundary flux. The observer term has the same coefficient c as
the Einstein term. Small t alone does not demote it to the old O(t4)
remainder. Its derivatives, c's matter/scale jet and the full preparation
source must remain. The absolute volume B also remains because the two
volume densities agree.
For fixed B its covariant-g metric source is `(B/2)g^-1` and its current
source is zero. Moving B still has its own preparation/field derivative;
equal volume densities do not remove that derivative.

For reference, nabla^g_a u_b=omega_a a_b-K_ab+Omega_ab, with the same
covector omega=g(u,·)=h(u,·). The expansion and spatial double-contraction
norms agree between the two descriptions. This is a specified observer
derivative functional, not a new independently adjustable vector action.

## 5. An owned full-CAR witness with flat g and nonzero observer price

Consume the published #322 amplitude family, at commit
`c57e9d70a6340e5d70fdf22579cce309ab793645`. Its extension-checker source
blob is `f134307e5ecd73621387adada0d796d97fb63ad0`; the new consumer does
not import or run that checker. The current definition is the already
local `a4d_native_correlated_current_transition.py`.

At the retained reference frame F=I and g=eta, the complete sixteen-entry
matter vector is

```text
m(s)=-2ap e_mask0+(2p-1)e_mask1+s(e_mask13+e_mask14),
N=m^T m=1+2s²,
J=(1,-2s²/(1+2s²),0,0).
```

This is a field in the full carrier, not a deletion of other grades or
their possible variations. Its current is timelike for every finite s.
Assign s=1+y in a transverse coordinate. Write

```text
J/sqrt(g(J,J))=(cosh chi,sinh chi,0,0),
chi=atanh[-2s²/(1+2s²)],
chi_s=-4s/(1+4s²).
```

The reflected h has determinant1 for the whole varied family. At y=0,

```text
u=(3,-2,0,0)/sqrt(5),
partial_y u=(8,-12,0,0)/(5sqrt(5)),
h_01block=(1/5)[[13,12],[12,13]],  h_22=h_33=1,
theta=0, a=0, K²=Omega²=8/25,
R_h=-32/25, R_g=0,
omega wedge d omega=-(4/5) dt wedge dx1 wedge dy.
```

In the h-orthonormal frame (u,spatial rapidity partner,partial_y,partial_z),
the one nonzero derivative type is B_12=chi_y. Its symmetric and
antisymmetric contractions are each chi_y²/2. In fact along the whole
transverse family

```text
R_h=-2chi_y²,  theta=0, R_g=0.
```

So the observer contribution in (5) is required pointwise. It is not only
a disputed boundary convention. The native kinematic equations do not
imply a parallel or twist-free line. This spatial assignment is not a
claim that the engine's constrained update or a physical evolution admits
the chosen family; the reference input also remains retained.

The concurrently published [AF/CAR role-orbit consumer](A4D_NATIVE_AF_ROLE_ORBIT_CAR_GEOMETRY_2026-10-16.md)
uses this same active seed to obtain a nondegenerate four-current Gram,
while its actual canonical AF blank-started orbit has only the current e0
and a rank-one role frame. That scoped startup failure is retained. Neither
the present transverse extension nor the smooth chart below claims that
this blank operation prepares the needed moving observer or geometric metric.

There is a genuine matter-Euler consumer. Per unit constant curvature
coefficient and unit spectator volume, the curvature density is

```text
L(s,s_y)=-2 chi_s(s)² s_y²,
E_s=partial_s L-d_y(partial_(s_y)L)
   =4chi_s[chi_ss s_y²+chi_s s_yy].                    (7)
```

For s=1+y, E_s(0)=-192/125, or -192c/125 for coefficient c. The pointwise partial_s L at this same jet
is instead +192/125; it is not the Euler derivative. Compactly supported
delta s removes endpoints. Because det h=1 on the entire s-family,
there is no hidden varying volume in (7), and a fixed blank-volume term
has zero source along it. Replacing the curvature sector by only R_g=0
would delete this actual projected matter force. Additional native
preparation/direct-action terms can contribute and are not set to zero.

## 6. The full ten-metric and sixteen-matter source

The pointwise reflection's source can be transported without deriving a
separate observer equation by assumption. Treat the nonzero line J first
as a variable; normalization u=J/sqrt(kappa) then moves automatically.
For b=gJ, kappa=J^TgJ, write h=-g+2bb^T/kappa. Let E=E_h be a symmetric
metric Euler covector, with full Frobenius pairing, and set
z=Eb, s0=b^TEb. Direct differentiation gives

```text
M=-E+(2/kappa)(z J^T+J z^T)-(2s0/kappa²)JJ^T,
L_J=(4/kappa)[g z-(s0/kappa)b],
delta S=<M,delta g>+L_J^T delta J,  L_J^T J=0.        (8)
```

This accounts for all ten symmetric metric slots; off-diagonal entries
have their usual double weight in the full tensor pairing. If the actual
current is J(g,m,reference), the source is

```text
E_g,total=M+(D_g J)*L_J+E_g,direct,
E_m,total=(D_m J)*L_J+E_m,direct.                      (9)
```

All sixteen matter components enter D_m J; twelve or thirteen invisible
directions of a particular readout are not declared gauge or removed
from the remaining action. Reference/frame/pairing motion contributes
its own derivative. For the full CAR current

```text
r_i=<m,alpha_i m>_W/N,
delta r_i=2 Re<delta m,(alpha_i-r_i I)m>_W/N
```

holds at fixed frame/pairing. General variation also has delta W and
delta alpha_i, as well as delta N. On the actual family above, r_1'(1)
is -4/9; freezing N would give -4/3. The normalizer is a real source term.

For fixed nonzero J the reflection is an involution: hJ=gJ and
J^ThJ=J^TgJ imply reflection_J(h)=g. Its ten-slot differential is
invertible. This rank fact does not erase the second term of (9) when
J is a matter readout, nor identify the two Levi-Civita curvatures.
For the owner's contravariant metric slot the additional inversion is
`delta g=-g(delta q_native)g`; thus its tensor source is
`-g E_g,total g`, before any other explicit q_native dependence is added.

## 7. All three observer directions have a full-matter lift

In the actual fixed positive reference frame, the three self-adjoint
CAR alpha_i anticommute and square to I. Put v_i=(alpha_i-r_i I)m. Then

```text
Re<v_i,v_j>_W=N(delta_ij-r_i r_j).
```

On the timelike sector |r|<1 this Gram is positive. Every real observer
variation delta r has the explicit full-carrier lift

```text
delta m=(1/2)sum_i[(I-rr^T)^-1 delta r]_i v_i,
Re<m,delta m>_W=0,
D_m r[delta m]=delta r,
||delta m||_W²=(N/4)delta r^T(I-rr^T)^-1 delta r.      (10)
```

The bound degrades near the causal boundary; it is not a uniform
all-state admission theorem. At s=1 the normalized Gram is
diag(5/9,1,1). This is a constructive source consumer of the existing
full16 readout, not a new apparatus-axis law or a restriction of the
engine transition class.

The lift also compensates a metric-induced change of the current **line**.
If `b0=F^-1 delta J_metric` and `J=F(1,r)`, choose
`lambda=(b0)_0` and lift `delta r=lambda r-(b0)_spatial` by (10).
The total current jet is then `delta J=lambda J`, which the homogeneous
reflection does not see. A radial matter adjustment can separately
preserve the moving W-norm without changing r. The focused consumer checks
this for all ten metric/coframe slots, including W and normalizer motion.
Holding the line fixed does not require holding the current vector fixed.

For a price depending only on h(g,J), with compact variations or
consistently pulled-back boundary data, the independent-line stationary
system is equivalent to E_h=0, using the invertible ten-slot map. If
J is the full CAR readout and all lifted matter tests are admitted,
the matter equations first imply L_J=0, then the metric equations imply
E_h=0. Direct matter, link and preparation terms change this coupled
balance and must be retained. In neither case does this argument turn
E_h=0 into the Lorentz equation G_g=0: the observer term in (6) is part
of the same transformed action.

One analytic curvature-sector control makes this last distinction direct.
Take h=I and J=(1,kx,0,0). Its inverse reflection is
`g=-I+2JJ^T/(1+k²x²)`. The constant-coefficient h-curvature sector has
E_h=0, so its complete pulled-back metric/current Euler pair vanishes.
Near x=0, remove the dt dx cross term to write the two-dimensional block
as `A(x)dt'²-A(x)^-1 dx²`, where `A=(1-k²x²)/(1+k²x²)`.
Its scalar curvature is A'', hence `R_g(0)=-4k²` and G_g is nonzero
in four dimensions for k nonzero. The other two directions are flat
spectators. Thus the critical-point systems themselves differ, not merely
the off-shell action values. This is a geometric control, not an admitted
native preparation; the absolute B-volume sector would have a nonzero
metric source at this h and is not stationary by this argument.

## 8. A complete native kinematic lift of a prescribed positive metric

There is no algebraic obstruction to realizing the positive record metric
as an actual native observer pairing. Whitening/polar decomposition applied
to the full CAR owner's covariance gives the following explicit corollary:

```text
m0=rho(F)^-1 m,  j=(1,r(m0)),  J=Fj,
g=F^-T eta F^-1,
h_native=F^-T H(r)F^-1,
H(r)=-eta+2(eta j)(eta j)^T/(1-|r|²)>0.               (11)
```

Here rho is the full exterior representation; all16 amplitudes remain.
Take any smooth prescribed h>0, any nonzero rest matter m0 in the open
timelike-current domain, and any O in O(4). With the unique positive matrix
square roots set

```text
F=h^-1/2 O H(r(m0))^1/2,
m=rho(F)m0.                                         (12)
```

Then `F^T h F=H`, so the actual native pairing in (11) is exactly h.
Conversely, from any raw timelike pair (F,m), compute m0 and h by (11) and

```text
O=h^1/2 F H^-1/2.
```

Its orthogonality follows from `F^T h F=H`; substitution in (12) recovers
F and m. Positive matrix square roots are smooth without choosing an
eigenbasis, including at repeated eigenvalues. These formulas are therefore
a smooth full-dimensional reparametrization of the **raw** frame/matter
domain: 10 positive-metric coordinates, 16 nonzero rest-matter coordinates
and 6 orthogonal-frame coordinates, totaling32. The current normalizer
remains explicit. Imposing N=1 would instead remove one radial coordinate;
that restriction is not made here. O(4) is a coordinate factor, not a newly
declared Lorentz gauge quotient, and its six reference directions remain.

In fact H is a positive Lorentz matrix: `H eta H=eta`. Its positive root
B is the symmetric boost with gamma=(1-|r|²)^-1/2, blocks
`B00=gamma`, `B0i=-gamma r_i`,
`Bij=delta_ij+(gamma-1)r_i r_j/|r|²`, continuous at r=0.
It satisfies `B eta B=eta` and `Bj=sqrt(1-|r|²)e0`. Consequently

```text
g=h^1/2 O eta O^T h^1/2,
u=h^-1/2 Oe0,
J=sqrt(1-|r|²)u,
m^T W(F)m=m0^T m0.                                 (13)
```

Thus the metric and unit observer are independent of m0 **at fixed h,O**;
the full matter amplitudes still move F,m. This is a joint reparametrization,
not a claim that the current has zero matter derivative at fixed F. O(x)
remains free, so no fixed observer section is selected. The construction
also produces g; it does not realize arbitrary h while an independent g
is simultaneously held fixed.

The identity holds for smooth field germs, not merely metric values. Its
full jets are obtained by differentiating (12). For example, if X=h^1/2,
`X delta X+delta X X=delta h` determines its unique symmetric derivative;
the same Sylvester equation differentiates H^1/2. Both delta m0 and delta O
also move. Thus an independently prescribed positive h_record and all its
metric jets have an explicit native kinematic lift, while all other raw
variables remain available. This is stronger than identifying h_record
and h_native by a name, and it does not freeze matter to r=0 or a parallel
observer.

This is not yet a commuting physical record construction. If the actual
record metric itself depends on the lifted F,m, its equality to the
prescribed h must still be proved for that same program; otherwise (12)
would only prescribe an external target. Primitive admission, physical
preparation, complete controller/archive cost, volume law and action
selection are not consequences of a smooth coordinate chart. Nor is a
uniform refinement bound supplied near a vanishing metric eigenvalue or
the causal boundary. The full reflection and source identities in the
preceding sections hold on this lift, with every derivative retained.

## 9. Evidence scope and the next unproved arrow

The new focused entrypoint is
`certificates/a4d_native_lorentz_reflection_source_check.py`. It checks
generic adapted-frame connection contractions, exact curved metric/observer
jets, the actual current/normalizer and transverse witness, the full source
chain rule and observer matter lift. The general curvature theorem is
proved in Sections2–3 and the kinematic chart directly in Section8; finite
examples are controls, not extrapolations of either general theorem.
The combined consumer passes226 named exact conditions (158 native and68
geometry); normal and optimized Python outputs agree byte-for-byte. The
actual matter Euler value is also checked by the independent full Einstein
tensor contraction, beyond the reduced calculation in (7). Independent
mathematical reviews cover the source formulas and raw-carrier chart.
Unchanged old suites, Lean capsules and generated receipts are not replayed.

For the route to physical GR, the remaining common-family test must now
retain the derived observer sector, its full matter/source equations,
the absolute price/volume term and the same-program physical metric binding. An
existing term may cancel or balance it only by an independently derived
identity on that same admitted family. A signature convention, a selected
future or a fitted compensating action is not such an identity. The
primitive controller, native Info selection, joint curved solutions,
physical refinement and original fixed-source/raw-owner terminal remain open.
