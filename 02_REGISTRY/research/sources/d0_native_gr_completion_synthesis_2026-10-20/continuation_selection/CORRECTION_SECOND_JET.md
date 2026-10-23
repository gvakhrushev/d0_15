# A source-preserving remainder cannot stabilize the stopped field saddle

20 October 2026. Short continuation of [STOPPED_FIELD_SADDLE.md](STOPPED_FIELD_SADDLE.md).
No changes to the already reviewed theorem or checker. This note concerns the
same original finite coframe/shared-link slice and complete whole-J2 pointer
price, not an unspecified total compulsory action.

## 1. Normalization and hypotheses

Write x=a-1 and u for the original shared-link angle. The exact owned signal
satisfies, throughout the common-null curve u=0,

    t(a,0)=0,          t_a(a,0)=0,
    t_u(a,0)=g(1-a)=-g x,                  g>0,
    Dt=gamma_h DJ2,                        gamma_h>0 fixed.

At the flat point its exact second form is

    H_t=[[0,-g],[-g,-2gD]],                D>0.

Here the original normalizations are g=gamma_h a_J,h/h² and
D=chi²(p h²)^-1(rho_0^-1+rho_d^-1). The same true positive density ratios,
original full trace multiplicities, fixed F*, C and full retained records
are used. Let kappa=R'_k(0) be a fixed branch's stopped scalar multiplier,
which is nonzero on every active branch for T>=5,ell>=1.

Distinguish two ways to write a total first-source hypothesis on the curve:

    DS=eta(y) Dt       gives       eta(1,0)=eta_0,
    DS=mu(y) DJ2      gives       eta_0=mu(1,0)/gamma_h.

The multiplier must be continuous at the flat point with nonzero limiting
value. Its assigned value at a stationary point alone is insufficient: when
DJ2=0, an isolated arbitrary multiplier value carries no information about
the neighboring source. The unchanged stopped branch has eta=kappa and
mu=kappa gamma_h.

## 2. Stronger ridge theorem: no second derivatives are needed

Suppose S is defined on an open two-dimensional neighborhood of (1,0), its
restriction a -> S(a,0) is differentiable on an interval about 1, and at every
point of that interval the two-sided partial derivative in u exists. Assume

    d/da S(a,0)=0,
    partial_u S(a,0)=eta(a)g(1-a),
    eta(a) -> eta_0!=0 as a -> 1.

Then S has neither a local minimum nor a local maximum at (1,0).

Proof. The ordinary mean-value theorem makes S(a,0)=S(1,0) throughout a
smaller interval. In every neighborhood of (1,0), choose a distinct nearby a
with eta(a)!=0. Its u derivative is nonzero. For sufficiently small positive
and negative u, the directional first-order expansion at that fixed a gives
one value below and one above S(a,0)=S(1,0), both inside the prescribed
neighborhood. This proves the claim. No off-curve C1 regularity, uniform
Taylor remainder, Hessian or entropy differentiability away from the curve
is needed.

The hypothesis DS=eta Dt on all admitted field directions along this curve
implies the two displayed directional identities. The owned actual pointer
branch has exactly this source on every point of the curve and constant
value there. Its retained-work bound gives its directional derivative at
each such point. Thus the ridge theorem applies directly even without
promoting its second-order Peano expansion to a C2 theorem.

The full-field statement follows because this is an admissible original
two-dimensional slice. It introduces no restriction on the other independent
coframe, link or matter variables.

## 3. Convenient C2 version and the unavoidable mixed second source

If S is C2 on an open neighborhood and DS=eta(y)Dt along the whole curve,
with eta continuous at the flat point and eta_0!=0, then

    S(a,0)=constant,       H_aa=0,
    H_au=lim_(a->1) partial_u S(a,0)/(a-1)=-eta_0 g.

The central u derivative is zero. Differentiability of eta is unnecessary;
its continuity suffices for this difference quotient. For some real c,

    H_S|slice=[[0,-eta_0 g],[-eta_0 g,c]],
    det(H_S|slice)=-(eta_0 g)²<0.

In the convention DS=mu DJ2, the mixed entry is instead written
H_au=-mu(1,0)g/gamma_h=-mu(1,0)a_J,h/h².
There is no additional gamma_h factor to insert.

In particular, if an additional complete residual E_corr has DE_corr=0 in
all field directions at EVERY point of this curve, it cannot stabilize the
branch. The ridge theorem already proves this with directional derivatives.
If E_corr is C2, its second form has K_aa=K_au=0, so it can change only the
u-u entry on the slice; the negative determinant survives unchanged.

## 4. What an actual correction must supply at one root

The known actual branch has the second-order value expansion with quadratic
form kappa H_t. Suppose an actual additional scalar price E_corr has zero
first derivative at the flat root and a second-order Peano expansion with
symmetric form K there. A genuine local minimum of the total price requires
the following 2x2 form to be positive semidefinite:

    H_total=[[K_aa, K_au-kappa g],
             [K_au-kappa g, K_uu-2kappa gD]].

Equivalently, its necessary slice conditions are

    K_aa >= 0,
    K_uu-2kappa gD >= 0,
    K_aa(K_uu-2kappa gD) >= (K_au-kappa g)².             (P)

These are also sufficient for positive semidefiniteness of this slice form,
not for a local minimum of the full price or control of higher orders.
A second-order Peano expansion suffices for the necessary condition (P);
it does not by itself justify differentiating gradients along the curve.

If K_aa=0, (P) forces K_au=kappa g. For a C2 correction whose a-direction
first derivative is zero on the curve, this means

    partial_u E_corr(a,0)=kappa g(a-1)+o(|a-1|).

It cancels the branch's neighboring transverse geometric source to leading
order. Such a correction cannot simultaneously have zero first source on
the whole curve. If K_aa>0 is used instead, it changes the coframe first
source along the neighboring curve: partial_a E_corr(a,0)=K_aa(a-1)+o(|a-1|).
Thus stabilization at the root can retain its stationarity but cannot retain
the nonzero proportional full source throughout this curve.

Define E_corr=S_full-F_k only when the actual complete S_full has been
specified. E_corr is not identified with Tr(rho R)+W alone. For example,
under a complete normalized-state decomposition

    S_full=s_c+delta_s q_mark+Tr(rho R)+W,

the full first source is

    DS_full=Ds_c+q_mark Ddelta_s+delta_s Dq_mark
            +Tr((D rho)R)+Tr(rho DR)+DW,
    DE_corr=DS_full-DF_k.

This subtraction avoids double-counting terms already present in F_k.
Since DF_k vanishes at the root, DE_corr=0 there is necessary for full
stationarity. Its second form K must include every scalar, moving mark,
state, residual and work derivative, and any genuine internally reduced
response. Testing only DR or an unweighted residual table does not test (P).

## 5. Exact algebraic controls and remaining routes

At quadratic order write the verified branch slice as

    S0(x,u)=-kappa g x u-kappa gD u².

Any correction beta u² has zero full first derivative on the entire x-axis,
but the corrected Hessian determinant remains -(kappa g)². This directly
checks why purely transverse padding cannot remove the obstruction.

As a contrastive algebraic control ONLY, the correction

    E_test=kappa g x u+(kappa gD+lambda)u²,  lambda>0,

gives S0+E_test=lambda u². It removes the saddle precisely by supplying
partial_u E_test(x,0)=kappa g x, the neighboring source forbidden by the
source-preserving hypothesis. This is not a proposed or admitted D0 action.

The available logical alternatives must be derived from actual D0 data:

* The complete residual genuinely changes the neighboring first source and
  satisfies the necessary second-form conditions after all its paid terms.
  Its physical equations must then be checked anew; first-source preservation
  of the present whole-J2 reporter cannot simply be reused.
* The actual physical rule is stationary or constrained causal selection,
  with its allowed variations and full original Euler consumer proved from
  that rule. Removing this slice by declaration is not such a derivation.
* A different actually admitted sector or complete programme is selected;
  this theorem does not identify the present stopped component with every
  possible compulsory H+J+R price.

Terms having zero first field source on the entire curve, even when they
carry nontrivial higher orders away from it, do not offer a further escape:
the ridge proof already excludes a minimum. No new field, correction law or
physical postulate is introduced by this conclusion.
