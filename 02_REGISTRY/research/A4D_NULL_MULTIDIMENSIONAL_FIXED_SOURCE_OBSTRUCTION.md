# Multidimensional commuting-null subgroup: exact local inverse and all-period obstruction

Input: D0 PR #310, f4f88161325574e4c5750e0af4a8cc14a2f4b48e.
Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.
This extends the [one-coordinate audit](A4D_NULL_SHEAR_FIXED_SOURCE_EXISTENCE_AUDIT.md)
to coefficient fields with arbitrary dependence on all four lattice
coordinates. It does not close the parent rooted NO-GO.

The exact finite-stencil inverse gives, in the explicit coefficient chart,
\[
 \|V_h\|_\infty\le3hC_1,\qquad
 C_1\le h(2C_2+5184C_1^2).
\]
Thus one fixed nonconstant pp profile cannot have a refining stationary
sequence anywhere in this null subgroup, including arbitrary UV fields.
The $O(h)$ conclusion is derived from full equations, rather than assumed.

## Precise scope

On the periodic four-torus of side L, let h=1/L and

    eta=diag(1,-1,-1,-1), k=(1,1,0,0)^T, k_flat=(1,-1,0,0),
    E(x)=I+(H(h*x2,h*x3)/2) k k_flat,
    Q(x)=eta+H(h*x2,h*x3) k_flat^T k_flat.

H is one fixed real C2 periodic function, prescribed before links.
The metric is nondegenerate for every H: det E=1 and det Q=-1.
Use the fixed Gram section E above. Let N2,N3 be the two Lorentz generators

    N_i=k e_i^T eta-e_i k_flat, i=2,3.

They commute and (a N2+b N3)^3=0. Allow every Role link

    U_r(x)=exp(V_r(x)), V_r(x)=a_r(x) N2+b_r(x) N3,

with arbitrary real coefficient fields a_r,b_r on all coordinates.
No translation invariance, derivative bound, expansion, or initial O(h)
assumption is imposed. Set

    delta=max_(x,r)(|a_r(x)|,|b_r(x)|).

The theorem below applies to the explicit fixed chart delta<=1/288.
For the usual entry sup norm, operator norm or Frobenius norm, a logarithm
chart radius rho<=1/288 suffices because a,b occur as individual matrix
entries. This is an explicit sufficient subchart. It is not automatically
a theorem for an earlier chart whose unspecified radius might be larger.

## Full literal Euler and Gram response

For a face (r,s), write its four factors in their literal order as

    U_r(x), U_s(x+r), U_r(x+s)^-1, U_s(x)^-1.

Define v_r=(a_r,b_r), N(v)=v_1 N2+v_2 N3. All factors commute within this
subgroup, so

    P_rs=U(c_rs), c_rs=D_r^+ v_s-D_s^+ v_r,
    C(P_rs)=(P_rs-P_rs^-1)/2=N(c_rs) exactly.

The ten raw Gram slots, in order 00,01,02,03,11,12,13,22,23,33, are

    Xi00=-(c12^a+c13^b)/2,
    Xi01=(c02^a+c03^b-c12^a-c13^b)/2,
    Xi02=-(c01^a+c23^b)/2,
    Xi03=(-c01^b+c23^a)/2,
    Xi11=(c02^a+c03^b)/2,
    Xi12=Xi02, Xi13=Xi03,
    Xi22=(c03^b+c13^b)/2,
    Xi23=-(c02^b+c12^b+c03^a+c13^a)/2,
    Xi33=(c02^a+c12^a)/2.

In particular every slot is linear in the null logs and independent of H.
The restricted global action telescopes to zero for arbitrary fields.
This does not imply full stationarity.

All full Lorentz-generator variations are reconstructed from the face kernel

    K_(rs),g(pre,post,H)
      =trace(U(post) W_(rs)(H)^T U(pre) G_g).

The exact six-generator kernels for all six faces are pinned in the JSON.
Their degrees in pre/post are at most two. The H-dependent term is only a
constant in these variables. The J01 and J23 kernels are linear. All full
shared-link equations therefore have the exact form

    F_H + S V + N(V,V)=0,

not just a Taylor expansion. The eight null-pairing equations vanish; eight
J01/J23 equations are homogeneous linear; the eight complementary equations
are the remaining linear-plus-quadratic equations with H forcing. This is a
reconstruction of all 24 rows, not variation of the restricted action.

The pairing with P is identical to the pairing with C(P) on the full Lorentz
group: every W and every Gram derivative weight obeys eta W^T eta=-W.
Thus <W,P^-1>=-<W,P>. Differentiation along any full Lorentz-generator tangent
preserves <W,C(P)>=<W,P>. This justifies the face-kernel derivative on the
full tangent space, including directions outside the null subgroup.

## The complementary eight-row operator has an exact finite inverse

Select J02 and J03 in each Role, with owner indices

    (1,2,7,8,13,14,19,20).

Let T_j f(x)=f(x+e_j), D_j^-=I-T_j^-1, and

    C_j=(T_j-T_j^-1)/2,
    B_rs=(T_r T_s+T_r-T_s+I)/(2 T_s),
    G_rs=-(T_r T_s-T_r+T_s+I)/(2 T_r),
    J_rs=[[-C_s, B_rs],[G_rs,C_r]].

All shifts commute. Direct Laurent-polynomial calculation gives

    det J_rs=1,
    J_rs^-1=[[C_r,-B_rs],[-G_rs,-C_s]].

The selected linear operator M acts as J01 on (a0,a1) and (b0,b1).
On the transverse variables its J02 rows act as -J23 on (b2,b3), while its
J03 rows act as J23 on (a2,a3). Hence M is exactly invertible on every finite
periodic torus, independently of L and every UV character. Its inverse is
an explicit finite Laurent stencil, not a spectral inverse with small
frequency denominators. The exact inverse matrix is pinned in the JSON.
Every inverse row has coefficient absolute sum at most 3, so

    ||M^-1||_(sup->sup)<=3.

## Quadratic and forcing bounds, with constants

Each individual face occurrence in one selected full Euler row has a
quadratic coefficient absolute sum at most 8, after substituting its actual
one/three or two/two prefix/suffix sums. This coefficient bound is checked
exactly. A shared row has at most six face occurrences. Consequently the
conservative mesh-independent bound is

    ||N(V,V)||sup<=48 ||V||sup^2.

Here ||V||sup means the coefficient norm delta. No derivatives enter.
For H=H(x2,x3), the exact selected forcing is

    F_H=(-D2^-H/2,-D3^-H/2,-D2^-H/2,-D3^-H/2,0,0,0,0).

Define C1=max(||partial2 H||sup,||partial3 H||sup) and
C2=max_(i,j in {2,3}) ||partial_i partial_j H||sup. Sampling H gives

    ||F_H||sup<=h C1/2.

Every full stationary field satisfies the selected equations, therefore

    ||V||sup<=3h C1/2+144 delta ||V||sup.

For delta<=1/288, absorption gives the automatic estimate

    ||V||sup<=3h C1.

Thus O(h) has been deduced from the original type of fixed small chart,
including arbitrary UV patterns. It has not been added as an admission rule.

The exact leading particular solution of M V_lin=-F_H is

    a0=-D2^-H/2, b0=-D3^-H/2,
    a1=+D2^-H/2, b1=+D3^-H/2,
    a2=b2=a3=b3=0.

This shift/sign convention is independently checked against the complete
Laurent symbol. The finite inverse and quadratic estimate imply

    ||V-V_lin||sup<=3*48*(3h C1)^2=1296 h^2 C1^2.

## Exact centered CR rows and their real energy identity

Average over x0,x1 with normalized counting measure; denote this contraction
by P_long and write A_r=P_long a_r, B_r=P_long b_r. This operation has sup
operator norm one and commutes with transverse shifts. The full J01/J23
rows are exactly homogeneous linear, so they survive this averaging without
an unknown quadratic remainder.

Four transverse Role rows imply

    A1=-A0, B1=-B0.

The differences of the longitudinal Role0 and Role1 J01/J23 equations give

    (T2-T2^-1) A0+(T3-T3^-1) B0=0,
    -(T3-T3^-1) A0+(T2-T2^-1) B0=0.

Write L_j=T_j-T_j^-1. On the finite periodic counting inner product,
L_j is skew-adjoint and L2,L3 commute. Hence the exact real energy identity
is

    ||L2 A0+L3 B0||2^2+||-L3 A0+L2 B0||2^2
      =||L2 A0||2^2+||L3 A0||2^2
       +||L2 B0||2^2+||L3 B0||2^2.

The cross terms cancel because <L2 A0,L3 B0>=<L3 A0,L2 B0>.
Thus every term on the right is zero. Both A0 and B0 satisfy

    T2^2 A0=A0, T3^2 A0=A0,
    T2^2 B0=B0, T3^2 B0=B0.

For even L these are precisely the four transverse checkerboard characters.
For odd L, translation by two generates the whole circle, leaving only the
constant character. No L multiple-four assumption is required. The complex
form is (L2-iL3)(A0+iB0)=0; the real energy argument prevents an erroneous
complex characteristic cancellation. The checker verifies the associated
Hermitian square and all designated full rows exactly.

## Projection of a smooth sampled difference

Let P_chi be the normalized average over the subgroup of transverse
translations generated by T2^2,T3^2. It is a conditional average, so
||P_chi||_(sup->sup)<=1, including unweighted field sup norm. Its range is
exactly the preceding checkerboard space, for both even and odd L.
It commutes with shifts and P_chi T_j=P_chi T_j^-1. Therefore

    P_chi D_j^-H=-(1/2) P_chi (T_j-2I+T_j^-1)H.

The central second difference of a fixed C2 profile is bounded by h^2 C2.
Consequently

    ||P_chi D_j^-H||sup<=h^2 C2/2.

For odd L the left side is actually zero. This is a uniform sup estimate
using normalized averages; it does not replace the original raw owner norm
with a volume norm in the parent theorem.

## All-period conclusion

Because A0 and B0 lie in the checkerboard space, apply P_chi to the preceding
leading-log estimate and to P_long, both norm-one contractions. It yields

    ||A0||sup,||B0||sup <=h^2 C2/4+1296h^2 C1^2.

Comparison with their prescribed leading particular values then gives

    ||D_j^-H||sup <=h^2 C2/2+5184h^2 C1^2, j=2,3.

The backward finite difference divided by h approximates partial_j H with
error at most h C2/2 at each sample. Thus the gradient at every mesh sample
has bound h(C2+5184 C1^2). Every continuum point is within h/2 in each of
the two transverse coordinates of a sample. The C2 bound adds at most h C2.
It follows that any claimed full stationary field in the coefficient chart
forces the fixed-profile inequality

    C1<=h(2 C2+5184 C1^2).

For an unbounded refinement sequence h->0, C1 and C2 belong to the one fixed
profile. Therefore C1=0 and H is constant. A fixed nonconstant H cannot have
such exact full stationary null-subgroup roots on all sufficiently fine
meshes, regardless of the prescribed source. In particular a fixed curved
pp-profile cannot supply the missing exact fixed-source sequence by this
expanded null-subgroup route.

This statement uses no smoothness of the unknown links, no C7 hypothesis,
no UV census, and no choice of source from a constructed connection. It is
still an obstruction for a special Lorentz subgroup and the explicit small
chart delta<=1/288. General Lorentz connections and a larger unspecified
chart are not covered. It is not the parent rooted NO-GO terminal.

## Reproduction

    python3 02_REGISTRY/research/certificates/a4d_null_multidimensional_full_euler_check.py --repo /path/to/d0_15

The default mode compares with the adjacent pinned JSON. --output chooses
another JSON; --write explicitly regenerates. The two imported finite-action
owners have pinned SHA256. No embedded scratch paths occur in the certificate.
