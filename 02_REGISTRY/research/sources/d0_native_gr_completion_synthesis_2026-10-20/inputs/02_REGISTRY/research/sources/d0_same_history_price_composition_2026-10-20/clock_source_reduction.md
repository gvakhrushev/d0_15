# Exact paid-history clock reduction and its retained source

Research derivation for the existing native programme / PR #334.
This is a finite algebraic derivation from the original all128 process, not
a new physical price, a choice of Info, or a new operation admission.

## 1. The actual source-bearing history sum

Consume the literal all128 Kraus derivation in
[`paid_port_history.md`](paid_port_history.md), itself derived from
`A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md` §§1–3.
Let p+p²=1, Delta=D², epsilon=p²h²/64. On the full data/CAR16 carrier with arbitrary untouched oldRIGHT/reference,
and the ORIGINAL specified blank fresh-controller input, the actual
port-cost marked map is

    Phi_t(X)=x [X+epsilon(a(x) T(D X D)-{Delta,X}/2)],
    x=exp(-t),                    a(x)=p²+px=1+p(x-1).        (1)

T is the ACTUAL complete Julia recycling channel. This identity sums all
128 original outcomes with their original costs c_(b,k)=1+b. It is not a
replacement by a postselected return, a new Lindblad map, or a scalar clock
weight. OldRIGHT/reference is carried by tensoring every map with its
identity. A normalized data/reference preparation rho may be arbitrary and
correlated with oldRIGHT. This statement does not enlarge the fresh
controller preparation to arbitrary active work-input columns. All label/coefficient/port histories remain in the actual
global tape; partial tracing is used only to evaluate a diagonal tape
observable, not asserted as a physical erasure.

For fixed integer n and all complete ordered histories omega,

    Z_n(t)=sum_omega Pr_rho(omega) exp[-t C_port(omega)]
          =Tr Phi_t^n(rho),
    C_port(omega)=n+sum_j b_j.                                (2)

The auxiliary analysis variable t changes no actual dynamics. In
particular evaluating this generating function at t=log(phi) does not
identify it with Book03's algebra-valued amplitude sum or complete
Cost-Info weight.

## 2. One joint open-history / closed-loop generating object

The following finite identity holds over any finite complex or real vector
space, in any open domain where I-T is invertible. Let r be an initial
column, ell an endpoint row and u an auxiliary scalar:

    D(T,r,ell;u)=det(I-T-u r ell)
      =det(I-T) [1-u Z],       Z=ell (I-T)^(-1) r.             (3)

This is the matrix determinant lemma. It simultaneously retains the closed
loop determinant det(I-T) and the open-boundary observable Z. On a branch
where logarithms are defined,

    -log D=-log det(I-T)-log(1-u Z).                          (4)

No new physical feedback/reset is claimed by the rank-one boundary r ell.
It is a contraction specifying a generating function. Implementing a
trace-and-reprepare boundary as an actual operation would need its own
admission, preparation, clocks and prices.

For the ACTUAL n-round process use the clock space

    V = direct_sum_(j=0)^n L(H_data tensor H_oldRIGHT),
    (A_t)_(j+1,j)=Phi_t tensor Id_(L(H_oldRIGHT)),

with all other blocks zero. Inject rho at clock 0 with r, and trace only
clock n with ell. Then A_t^(n+1)=0, so exactly

    det(I-A_t)=1,
    Z_n(t)=ell (I-A_t)^(-1)r,
    D_n(t,u)=det(I-A_t-u r ell)=1-u Z_n(t).                  (5)

The coefficient in the finite resolvent that reaches clock n is precisely
the product of n actual weighted maps, including every ordered outcome.
The original prepared controller cut is unchanged; all output labels are
summed with their actual weights. No equivalence relation on tapes or new
admission of active work inputs is asserted. This is an exact compressed
computation of the complete weighted sum on the stated original input.
Inhomogeneous actual rounds use blocks Phi_(j,t) with the same identity.

## 3. Exact Schur reduction, including the open source

Let the space split into retained interfaces R and eliminated intermediate
clock states E. Write T in these two blocks and assume N=T_EE is nilpotent.
Set

    G=(I-N)^(-1),
    F=T_RR+T_RE G T_ER,
    r_eff=r_R+T_RE G r_E,
    ell_eff=ell_R+ell_E G T_ER,
    Z_ac=ell_E G r_E.

Then exact block elimination gives BOTH identities

    det(I-T)=det(I-F),
    Z=Z_ac+ell_eff (I-F)^(-1) r_eff.                         (6)

Although det(I-N)=1, its open resolvent G is generally variable. Its
source is dG=G(dN)G. In particular

    dF=dT_RR+(dT_RE)G T_ER+T_RE G(dN)G T_ER+T_RE G(dT_ER).

With R_F=(I-F)^(-1),

    dZ=dZ_ac+(dell_eff)R_F r_eff
            +ell_eff R_F (dr_eff)
            +ell_eff R_F(dF)R_F r_eff.                      (7)

All four terms belong to the same reduced process. Thus acyclic Schur
elimination preserves the original determinant source when its FULL F is
retained; it preserves the actual open-history source only when Z_ac and
both transformed boundaries, including their variations, are retained too.
Determinant one does not imply zero execution cost, zero open source, or
permission to discard the eliminated stages. The exact sufficient and
necessary accounting check is equality of (6) and its variation, rather
than source-free status inferred from det(I-N)=1.

## 4. Native costs survive as marked resolvent insertions

For R_t=(I-A_t)^(-1), arbitrary admitted variations give

    dZ=(dell)R_t r+ell R_t(dr)+ell R_t(dA_t)R_t r.          (8)

For a fixed endpoint trace and fixed analysis mark, dell=0; dr includes the
actual preparation/oldRIGHT/observer variation. All field and clock-scale
derivatives of the actual Julia maps are included in dA_t. Integer n stays
fixed when differentiating one programme.

For t-independent preparation and boundary,

    partial_t Z=ell R_t(partial_t A_t)R_t r,

and the full field derivative of this expression contains the two
resolvent variations, the mixed insertion d partial_t A_t, and dr. No
term vanishes merely because A_t is nilpotent.

At t=0, Phi is trace preserving on the complete process, hence Z_n(0)=1
and d_y Z_n(0)=0 throughout every normalized admitted smooth family. Yet

    C_n=-partial_t log Z_n|_0
       =n+p epsilon sum_(j=0)^(n-1)Tr[Delta Phi^j(rho)].    (9)

Therefore for K_n=-log D_n and fixed u with 0<=u<1,

    d_y K_n(0,u)=0,
    partial_t K_n(0,u)= -u C_n/(1-u),
    d_y partial_t K_n(0,u)= -u d_y C_n/(1-u).              (10)

If u itself varies, the last expression additionally contains
-C_n du/(1-u)^2. A zero unmarked source is fully compatible with a nonzero
mixed price source. This is the exact retained payment, not a fitted
counterterm or an omitted action.

For a finite computation without enumerating 128^n histories, define

    M_1(X)=-partial_t Phi_t(X)|_0
          =Phi(X)+p epsilon T(D X D),
    rho_(j+1)=Phi(rho_j),              rho_0=rho,
    v_(j+1)=Phi(v_j)+M_1(rho_j),       v_0=0.

Then Tr v_n=C_n. Every field/preparation source is propagated by

    eta_(j+1)=Phi(eta_j)+(dPhi)(rho_j),       eta_0=drho,
    dv_(j+1)=Phi(dv_j)+(dPhi)(v_j)
                  +M_1(eta_j)+(dM_1)(rho_j), dv_0=0.      (11)

The derivative of epsilon, D, T and any isometric trivialization remains
in dPhi and dM_1. Moving h changes epsilon and all native rows consistently;
it is not an independent free fugacity. The fixed paid n has zero field
jet at fixed n but must remain in comparisons of different future clocks.

## 5. Explicit non-scalar actual n=1 and n=2 sources

These formulas hold on the full original carrier, with arbitrary rho;
no scalar shell or commutation assumption is needed. Put

    R=Tr(Delta rho),
    G_2=Tr[Delta T(D rho D)],
    H_2=Tr(Delta^2 rho),       Gamma=G_2-H_2.

Trace preservation of T and cyclicity give exactly

    Z_1=x[1+p epsilon (x-1)R],
    Z_2=x^2[1+2p epsilon(x-1)R
              +p epsilon^2(x-1)(a(x)G_2-H_2)],             (12)
    C_1=1+p epsilon R,
    C_2=2+2p epsilon R+p epsilon^2 Gamma.                   (13)

The last term is precisely the native two-round clock feedback coefficient
in the existing paid-source owner, not a new force. Its full variation is

    dC_2=2p[(d epsilon)R+epsilon dR]
                  +p[2epsilon(d epsilon)Gamma+epsilon^2 dGamma].

Here dG_2 includes dDelta, the actual dT, both dD factors and drho; dH_2
includes both dDelta factors and drho. Thus this compression retains the
curved paid source already known to survive independent-link elimination.
For n=2, replacing Phi_t by x Phi would yield Z_2=x^2 and erase every term
in (13) beyond the two mandatory ticks: that replacement is false.

On an invariant original scalar shell Delta=lambda I, all input CAR16
and oldRIGHT columns remain allowed, and (12) specializes to

    Z_n=x^n[1+p epsilon lambda(x-1)]^n.

Only in this restricted scalar-effect situation can the cost transform's
trace be reduced to one scalar per round. An arbitrary direction away
from that shell must still use (8)–(11).

## 6. Weighted cyclic first return and the actual fugacity

Let finitely many complete linear transition blocks K_j map successive
clock stages cyclically back to stage 0. The stages may have different
finite dimensions. Eliminating all stages except 0 gives exactly

    det(I-T_cycle)=det(I-K_(L-1)...K_0).                    (14)

If each actual weight is a scalar a_j and the unweighted monodromy is
F=P W* Q W P, then

    det(I-T_cycle)=det(I-z_eff F),
    z_eff=z_0 product_j a_j,
    d[-log det(I-z_eff F)]
      =Tr[(I-z_eff F)^(-1)(z_eff dF+F dz_eff)],             (15)
    d log z_eff=d log z_0+sum_j d log a_j.

This is an exact same-partition subdivision identity. It does not assert
that the actual all-record transfer equals an amplitude feedback kernel,
that a scalar weight has been forced by Info, or that a matrix adjoint
must be executed as an additional physical inverse. Actual inverses already
specified inside the paired word remain paid; a formal Gram adjoint is
not double charged by this algebraic representation.

For the existing inverse-paired Golden feedback, a scalar-weight reduction
IF admitted replaces its coefficient by

    c_pair(z_eff)=-32 sigma z_eff p^5/(1-2z_eff p^3).       (16)

When each uncompensated net stage weight is <=p, this coefficient is
suppressed by at least p^L (away from a denominator singularity). That is
a conditional estimate, not a conclusion about complete Cost-Info: actual
Info may change net weights, and (1) shows even known original port costs
are normally NOT scalar. Nor does a closed-loop factor p^L multiply the
already paid open-history term in (9). The latter keeps its own source.

## 7. Full work versus prepared compression: exact spectral boundary

Let W(y) be a unitary on the FULL retained work/history input space, E a
fixed cost/event marker effect there, and rho a specified preparation. A
fixed marker applied after W has the full-input effect

    F_full(y)=W(y)* E W(y).

For any z in the determinant domain,

    det(I-z F_full)=det(I-z E),                            (17)
    dF_full=[F_full,K],           K=W* dW,
    d[-log det(I-z F_full)]=0     (fixed z).

Nevertheless d Tr(rho F_full)=Tr[(drho)F_full+rho[F_full,K]]
can be nonzero. Selecting an actual blank work input compresses F_full to
that input sector; its spectrum and its prepared expectation may vary.
Using this compression is legitimate only with its actual preparation and
cut, which are different from a determinant over every work input. An
output uncomputation acting identically on the marker's flag sectors does
not change the spectrum. This lemma applies to a fixed output marker;
it does not apply to the paired Golden circuit's field-dependent relative
operators inside interfering arms.

Thus the rank-one boundary in (3) is not smuggled in as a native way to turn
the prepared transform (2) into a responsive determinant on all work
inputs. Equations (3)–(15) are exact partition/source accounting identities,
while (17) blocks that particular physical admission shortcut.

## 8. What this closes and the exact remaining parent

The actual native port-price history normalizer now has a finite all-output
clock representation, exact Schur reduction, complete source and marked
source insertions. Acyclic compiler stages cannot be declared free from a
unit determinant; their open weights/boundaries are explicit. A scalar
first-return price must carry z_eff and its source, and the known native
128-outcome costs generally require the non-scalar map (1) instead.

The remaining parent is the physical SAME-PROCESS binding of the complete
Book Cost-Info (including labels, controllers, preparation, work, oldRIGHT
and executed clocks) to the admitted closed-memory/field action. A supplied
additive history price can be marked on an enlarged actual tape and reduced
by the same finite identities, but this does not supply its value or turn
coherent Info into pointer Shannon entropy. No cancellation, new primitive
price, resetting boundary, freely available coherent oracle or full-work
responsive determinant has been assumed. The derived source is suitable
for the existing full variational consumer; it is not yet a proof of GR.
