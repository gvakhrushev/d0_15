# Native pairing and refinement: exact reaction source and the remaining Gram modulus

Research continuation, 2026-10-13. Input SOURCE
`2f3360c5d3bfcb40d4791b23ade8e82e03f887c8`. Existing #310 and CONTROL #322.
All original #310/#202/#317 and G0–G4 obligations remain open. No new action,
selector, physical postulate or replacement of a supported operator is installed.

The current preparation question is tested on the actual graded cochain lift,
its positive pairings and the whole retained complement. The outcome has three
parts. Positive local diagonal Hodge weights cannot turn the actual chain lift
into an adjoint intertwiner. The correct compressed square contains an exact
positive reaction term R^dagger R with its own derivative. General nonlocal
pairings can repair the intertwiner, but even a complete one-parameter repair
family preserving the same coarse Gram changes the full heat price strictly.
This is a price-relevance test for a stated mathematical modulus, not its
native admission or a no-go for the full core.

## 1. Actual lift and what it fixes

Use the real definitions and research proofs in
[A4D_NATIVE_COCHAIN_REFINEMENT](A4D_NATIVE_COCHAIN_REFINEMENT.md), with their
actual source-pinned owners. For L>=2, K=L+1, c=K/L, the one-dimensional maps are

    (B0 f)(i)=f(i) for i<L, (B0 f)(L)=f(0),
    (B1 a)(i)=a(i) for i<L, (B1 a)(L)=0,
    J_S=c^|S| tensor_r (B1 if r in S else B0).             (1)

The differential on the full sixteen exterior sectors is the actual
L-scaled cubical forward differential, including its CAR signs. It obeys

    d_f J=J d_c.                                        (2)

At counting fine Gram, its complete pullback is

    G_c,S(x)=c^(2|S|) product_(r notin S)m(x_r),
    m(0)=2, m(j)=1 otherwise.                           (3)

This is the metric-measure formula with mu=product m and directional
conductance c'_r=c^2 mu/m_r. The actual all-degree research proposition proves
that identity; the old supported metric-measure capstone only proves endpoint
formulas and cardinalities. Neither statement defines a physical map from
(q,mathsfD,b,m) to these weights or to the separate golden apparatus.

Even (3) at every adjacent level is not a compatible Gram tower. In degree zero
and one dimension, B0^T diag(2,1,...,1) B0=diag(3,1,...,1), rather than the
coarse diag(2,1,...,1). A true positive diagonal tower must instead satisfy

    G_L,S(x)=c^(2|S|) sum_(q(y)=x, y_r<L for r in S) G_K,S(y). (4)

Here q is the literal adjacent coordinate projection in (1), not the flat
archive long-arrow modulo or a physical resampling. The finite scalar/tensor
maps, the flat-index archive tower and the AF matrix tower remain distinct.

## 2. Complete local diagonal adjoint obstruction, all sixteen sectors

Allow arbitrary positive diagonal G_c,G_f on every site and exterior sector;
no metric-measure factorization or fixed values are assumed. Let dagger denote
the actual coarse/fine weighted adjoints. Pick a singleton sector r and put

    psi_r(x)=1_(x_r=0), all other components zero.

It is constant in the three spectator coordinates. At a fine site with y_r=L,
J psi has no r-component at y or at its predecessor y-r: the former is the new
collapsed edge and the latter copies old edge L-1, where psi vanishes. Only
role r can contract a singleton r. Therefore

    (d_f^dagger J psi)_empty(y)=0,
    (J d_c^dagger psi)_empty(y)
        =-L G_c,{r}(q(y))/G_c,empty(q(y)) != 0.           (5)

This proves that no positive diagonal pairings in this complete class yield
d_f^dagger J=J d_c^dagger. Fine weights are arbitrary and cannot alter the zero
support. All four roles and every other grade remain in the actual carrier;
the test does not discard them. The L=2 case also has L-1!=0 and obeys (5).

If a<=G_{c,0},G_{c,1},G_{f,0}<=b, using weighted site norms normalized by the
number of sites, the same input gives

    ||d_f^dagger J-Jd_c^dagger||
       >= L sqrt(L/(L+1)) (a/b)^(3/2).                 (6)

Indeed the new hyperplane is 1/(L+1) of fine sites, its coefficient is at least
La/b, and its scalar fine weight is at least a. The input norm squared is at
most b/L. No lattice-independent smoothness is assigned to this test input.

For the actual counting pullback (3) there is additionally a fixed smooth
probe alpha=dx_r. Both d_c alpha and d_c^dagger alpha vanish. But

    (d_f^dagger J-Jd_c^dagger)alpha
       =(K^2/L)(1_(y_r=L)-1_(y_r=0))                    (7)

in the scalar sector. Normalized component counting norms are exactly

    L1=2K/L, squared L2=2K^3/L^2, Linfty=K^2/L.

Thus the chain lift does not preserve the harmonic representative of this
constant one-form. Smooth weak testing of the two nearby hyperplanes may
still vanish. Equations (5)–(7) alone do not exclude an O(h) action contrast,
low-frequency limit or a different admitted observable.

## 3. Exact compression, positive reaction and its full derivative

For any positive fine pairing, define the coarse pairing and adjoint readback

    G_c=J* G_f J, C=G_c^-1 J* G_f, E=JC, Q=I-E.

Here J is injective, CJ=I, E=E^dagger and Q is the orthogonal complement.
Equation (2) implies the genuine compressed-adjoint equality

    C d_f^dagger J=d_c^dagger, C D_f J=D_c,
    D=d+d^dagger.                                      (8)

It does not imply intertwining. In image/complement coordinates the full
operators have the complete blocks

    d_f=[[d_c,B],[0,a]],
    D_f=[[D_c,B],[B^dagger,D_o]],
    R=Q D_f J=D_f J-J D_c.

Consequently

    C D_f^2 J=D_c^2+R^dagger R.                        (9)

The reaction is positive and vanishes precisely when R=0. Equivalently the
image reduces d_f, both d and its adjoint intertwine, and D intertwines.
Intertwining of D^2 is also equivalent: its compressed defect is the positive
R^dagger R. For beta>0, exact heat intertwining at that beta implies D^2
intertwining, since the finite positive spectral function exp(-beta lambda)
is injective and logarithmic functional calculus recovers D^2. This argument
is not an operator-convexity claim about the exponential.

For every admitted differentiable family preserving these constraints, set
K_c=G_c^-1 dot G_c and K_f=G_f^-1 dot G_f. The rectangular adjoint derivative is

    dot(R^dagger)=G_c^-1 dot R* G_f-K_c R^dagger+R^dagger K_f,
    dot(R^dagger R)=G_c^-1 dot R* G_f R+R^dagger dot R
                    -K_c R^dagger R+R^dagger K_f R.     (10)

Changes of J and C are included in dot R, not silently frozen. For the
compressed-square heat with A=D_c^2+R^dagger R and
rho_A=exp(-beta A)/Tr exp(-beta A), its exact derivative is

    dot H_A=-Tr[rho_A (dot(D_c^2)+dot(R^dagger R))].     (11)

The same rho_A appears in both terms. It cannot be replaced by the coarse
rho_(D_c^2) without a quantitative estimate. This is the forced reaction
contribution to the source of this readout; it is not a selected new action
or an identification of the compressed heat with the native physical action.
The uncompressed full heat retains the complement as well.

Under simultaneous fine/coarse basis changes T_f,T_c, the actual rectangular
map transforms as R'=T_f R T_c^-1. With the corresponding transformed Gram
matrices, its reaction transforms as (R')^dagger R'=T_c R^dagger R T_c^-1.
Thus A and its complete heat trace transform covariantly/invariantly. At first
order, dot A=[V_c,A] and its heat variation vanishes by cyclic trace. This
internal frame Ward identity includes the reaction and both Gram terms; it
does not supply a spacetime stress-divergence Ward equation.

## 4. Complete one-parameter nonlocal repair at the same coarse Gram

The local obstruction is not extended to every positive Gram. A constructive
escape preserves exactly the coarse Gram already given by (3). In one dimension
put

    M=diag(2,1,...,1), v=(e0+e_(L-1))/2,
    G_c,0=M, G_c,1=c^2 I_L,
    G_f,0=I_K, G_f,1=[[I_L,v],[v^T,gamma]], gamma>1/2.   (12)

The upper-left block of G_f,1 is forced by J*G_fJ=G_c. Its positive Schur
complement is gamma-v^Tv=gamma-1/2. The actual adjoint readback is

    C0=M^-1 B0^T,
    C1=c^-1 [I_L | v].                                 (13)

Direct row comparison gives C1 d_f=d_c C0, including ordinary rows and both
wrap rows. Conversely that comparison forces each entry of v: 1/2 at 0 and
L-1, zero elsewhere. Thus (12) is the full repair class with this coarse Gram,
G_f,0=I, grade-orthogonal pairing and the actual J. Gamma is its only remaining
real parameter. It is not a coordinate convention: its value changes the
complement spectrum below.

The complement has scalar vector e_L-e0 and edge vector (-v,1); these are
orthogonal to the inherited image in (12). The differential sends the former
to -2K times the latter. Their squared norms are 2 and gamma-1/2. Therefore

    D_o^2=lambda_gamma I_2,
    lambda_gamma=K^2(2gamma-1)>0.                      (14)

Tensoring the four one-dimensional constructions, with the actual CAR signs,
repairs the full sixteen-sector chain and adjoint maps. Coarse Gram is precisely
(3), all old and new directions stay present, and each directional gamma_r
supplies an independently changing retained complement spectrum.

The fine Gram in (12) couples different sites. It lies outside the positive
diagonal class of section 2. In the original point-multiplication representation,
a real point observable is selfadjoint precisely when it commutes with G.
The projector onto site 0 does not commute with the nonzero (0,L) entry of
G_f,1. Thus this explicit escape cannot keep the same point *-representation
unchanged. Conjugating the represented algebra together with G is possible,
but the physical point/readout identification then requires its own native
map. No nonlocal pairing or new observable algebra is installed here.

## 5. Full price detects the repair modulus

Let Z_c(beta)=Tr exp(-beta D_c^2) on the complete one-dimensional coarse
complex, including its two harmonic modes. Exact reducing refinement gives

    Z_f=Z_c+2 exp(-beta lambda_gamma),
    H_f-H_c=beta^-1 log(1+2 exp(-beta lambda_gamma)/Z_c)>0,
    partial_gamma H_f
       =-4K^2 exp(-beta lambda_gamma)/(Z_c+2 exp(-beta lambda_gamma))<0. (15)

For the four-fold tensor with directional gamma_r, heat traces multiply; each
partial_gamma_r H has the same negative expression for that factor. Setting
all gamma_r equal multiplies it by four. The full operator spectrum varies,
so this direction is not null response or a simultaneous basis change.

For any existing coarse unitary/cut tuple extended by identity unitary and
zero cut on this reducing complement, the feedback determinant is unchanged
along gamma. The extension is a stated mathematical test, not a physically
admitted new gate. Thus its complete bootstrap price strictly decreases along
the repair modulus. There is no stationary point if this direction is freely
admitted with all other contributions constant, and no attained minimum as
gamma grows without bound. A native restriction or changing coupling must
be derived; no compensator is fitted to (15).

Even R=0 and perfect heat intertwining of the inherited block do not give
full price equality. More generally for any reducing full heat/cut/unitary
preparation, Z_f=Z_c+Z_Q, and the heat source obeys

    dot H_f=theta dot H_c+(1-theta)dot H_Q,
    theta=Z_c/(Z_c+Z_Q).                              (16)

No dot-theta term is added: (16) is the derivative of log(Z_c+Z_Q). Both
partition functions and their full multiplicities remain. Feedback adds its
own retained complement source. This is an exact rule that a quantitative
native-to-physical source transfer must control.

## 6. Does the missing site density restore all metric probes?

The preceding Lorentz/observer stored-operator classification used counting
site weights. Now retain the same actual stored d and lower operator, but
supply G_x=mu_x Lambda(h_n(x)), with mu_x>0 shared across degrees. No arbitrary
grade weights or volume selection is inferred. F is invertible at every site,
so every role leg v_r is nonzero, as required by the degree-two classification.
In this same exterior basis,
a diagonal observer form h_n forces all spatial components of n to vanish
and hence h_n=I. The intersection with the diagonal metric-measure class is
therefore only c_r=mu for all roles. The frozen weights (3), whose one-form
ratios are c^2/m_r, generally lie outside this observer family. Arbitrary
positive h would be a larger class and is not classified by (17).

For an edge x->y put r=mu_x/mu_y,
T=h_y^-1 A^T h_x A, b=h_y v_y, c_vec=A^T h_x v_x. The complete exterior
adjoint equation becomes

    i_b=r Lambda(T)i_c_vec.

Degree one gives b=r c_vec; degree two then says T fixes ker b pointwise.
The observer forms have determinant one and A is Lorentz, so the remaining
positive rank-one eigenvalue is one. Exactly as in the previous full proof,
all sixteen degrees are equivalent to

    A^T h_x A=h_y, A v_y=(mu_x/mu_y)v_x.               (17)

The observer line still permits both signs; the plus sign uses a time-cone
component. Lorentz links and positive weights alone do not imply (17).

Set Ftilde=mu F. Equation (17) is exactly the old counting admissible class
for Ftilde, n and A. If the declared density is mu=abs(det F), then

    abs(det Ftilde)=mu^5,
    F=Ftilde/abs(det Ftilde)^(1/5).                    (18)

This is an exact smooth reparameterization near the flat invertible frame.
It preserves the previously nonempty curved sector after transforming its
metric, rather than claiming its old q is unchanged. For example a(t)=2+cos(2pi t)
and Ftilde=diag(1,-a,-1,-1) give
q=a^(-2/5)diag(1,-a^2,-1,-1), uniformly nondegenerate and curved. In the preceding
curvature sign convention, with the first index lowered,
R0101(0)=-(16pi^2/5)3^(3/5)!=0. This is kinematic.

Linearizing with w=dot(log mu), E_F=dot F and u=dot n gives

    B_r e0=kappa_r u,
    B_r e_r=kappa_r(eta E_F,row_r^T+w e_r).            (19)

For independent mu, every nonzero Fourier pattern gains one conformal metric
direction. Its image dimension is

    10-b-s-bs+1_(b+s>0).

For mu=abs(det F), w=tr(eta H)/2 and

    Htilde=H+tr(eta H)eta,
    H=Htilde-tr(eta Htilde)eta/5.                      (20)

Consequently the declared-volume metric-image ranks equal the previous
counting-class ranks 10-b-s-bs.
At a generic mode there are still only three spatial mixed components.
The independent-density image, compared with ordinary coordinate gauge, has
rank seven if every k_i^2=k_0^2, otherwise eight; at least two nongauge
metric directions remain missing. With the declared volume, three remain.
This coordinate-gauge comparison is not native diffeomorphism admission.

The rescaling is not an equality of heat operators. In the same original
coordinate representation Dtilde=M_mu D. Removing the scalar density by the
isometry from mu Lambda(h_n) to Lambda(h_n) gives

    Dbar=M_(mu^-1/2) Dtilde M_(mu^-1/2).                (21)

For general n this is still the observer exterior pairing. A counting
representative additionally conjugates (21) by Lambda(h_n)^(1/2); at the
rest observer that factor is I.
Thus similarity of admissible domains cannot erase density dependence in the
price. The full native field covector must retain both operator and Gram
terms from the preceding joint-adjoint proof.

## 7. Consequence for the critical path

There is now a concrete obstruction and a concrete extension modulus, rather
than a claim that any supplied positive weights solve the preparation problem.
The actual local cochain lift forces (9) and excludes exact adjoint intertwining
for every positive diagonal Hodge weight. A nonlocal full repair preserves the
same coarse Gram but changes the full price through a freely varying spectrum;
it also changes the compatibility of the original point observable algebra.
The complete density extension of the stored Lorentz operator does not restore
all local metric probes.

The next required native preparation must specify its physical represented
observable/readout, compatible full Gram transition and apparatus map. On a
compression route it must retain or quantitatively control the reaction (10)
and full complement source (16). On another existing operator/pairing route
its owner, domain and physical readout are required. These conditions concern
the actual derivative, not another role/word enumeration. Native stationarity,
source/Ward, quantitative contrast, joint curved roots, soundness/recovery and
positive GR remain open. The original fixed-source/raw-owner terminal is retained.

## 8. Evidence and proof boundary

Run the accompanying immutable checker
`python3 02_REGISTRY/research/certificates/a4d_native_pairing_refinement_source_check.py`.
The analytical classification, all-level tensor extension, positivity, thermal
variation and density rescaling have the hypotheses stated above. Exact matrix
controls and the narrow Lean capsule support the named kernels and expose the
actual owner propositions. They do not turn an independently supplied Gram,
unitary tuple or compatible projection into a native physical preparation.
General rational matrix source controls use a normalized positive commuting
resolvent weight solely for cyclic-trace algebra, explicitly distinct from a
Gibbs exponential. The scalar complement family (14)–(15) instead checks its
actual symbolic Gibbs heat and derivative, with the coarse partition retained.
No supported CORE/claim/book is changed and no D0.All or GR closure is asserted.
