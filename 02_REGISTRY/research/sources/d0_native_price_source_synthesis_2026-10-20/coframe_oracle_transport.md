# From the actual inverse-coframe Julia calls to a relational reference

Proof for the existing #334 consumer. No new physical price is selected here. The new result is an explicit rational CAR formula and a fixed-query compilation of the required coframe reference, conditional on the already stated coherent Julia interface and its actual scalar work cut.

## 1. Inputs already owned, and the exact output

The original coframe owner `A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md`, §1, uses `F=e^{-1}`, `v_r=eta F_r^T`. The full-source owner `A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`, §8.5, (30a), transports these to the principal observer frame:

    V=[u_0 ... u_3]=eta e_bar^{-T},   e_bar=L e.

It explicitly retains the inverse-coframe and observer derivatives. Work below uses this actual `e_bar`, renamed `e`. If the face convention samples legs `h_r e_r`, its known factors `h_u h_v` multiply the formulas below; they must not be lost or confused with a new field normalization.

Assume a fixed oriented compact chart on which the actual coherent calls `J(C(u_r))` are supplied, `||C(u_r)||<=kappa<1`, `|det V|>=delta>0`, and the required field jets are bounded. These are the supplied moving Julia calls, not finite words manufactured from constant gates alone. The exact inverse and controlled-call constructions already belong to §§6.25 and 8.6 of that owner:

* `J(X)^T=Y J(X)Y` with a fixed scalar quarter-turn `Y` at the algebraic level; fixed controls can be approximated by Golden/CNOT words.
* §6.25, (13bq2), constructs controlled calls by the scalar echo, a uniform half-log branch and a finite product formula. It needs no additional moving controlled-query oracle or CAR parking input.
* The conclusion is convergence on the declared clean scalar-work input cut, on **all** query columns; all output leakage remains. In the forward-only variant its actual cut includes the retained `c=1` resource. It is not an identity on every unprepared work sector.

For each chart precision and each fixed mesh `h`, the construction below produces one finite program, with field-independent query/gate counts, whose clean-work action approximates the relational reference in `C^1`. It does not assert an exact finite Golden word for an arbitrary moving matrix. It does not supply the direct-face operation `J(p Lambda(P))` from sequential edge Julias; that separate interface remains explicit.

## 2. The cofactor identity removes the wrong quadratic-in-native-legs shortcut

Set `eta=diag(1,-1,-1,-1)`, `d=det V`, and `a wedge b=ab^T-ba^T`. Use the original oriented coframe face

    B_rs = epsilon(r,s,u,v) * (e_u wedge e_v) eta,

where `*` is the Lorentz Hodge star and `(u,v)` is the ordered complementary pair. Then exactly

    B_rs = (u_r u_s^T-u_s u_r^T) eta / d.                 (1)

This is the complementary-minor identity for `V=eta e^{-T}`. In particular, `det eta=-1` and `1/d=-det e`; the sign and inverse determinant in (1) are essential. Under `V -> cV`, (1) scales as `c^{-2}`, as a coframe area must. It is not quadratic in the native inverse legs.

Every variation is retained:

    delta B_rs = ((delta u_r wedge u_s)+(u_r wedge delta u_s)) eta/d
                 - B_rs Tr(V^{-1} delta V).              (2)

Consequently all sixteen coframe directions and all observer dependence transmitted through `u_r` survive. On a common compact nondegenerate chart this is a smooth identity, rather than a fit along one family.

Let `c_j` be the four CAR creation matrices on the full 16-dimensional exterior carrier, `C_r=C(u_r)`, and `H_eta=Lambda(eta)`. Since `H_eta C(u)^T H_eta=C(eta u)^T`, the exact full-CAR lift is

    D_rs=dLambda(B_rs)
        =[C_r H_eta C_s^T H_eta-C_s H_eta C_r^T H_eta]/d. (3)

Thus the numerator needs only two actual creation blocks per term, their adjoints and one fixed metric involution. There is no added coframe, Hodge or pointwise matrix-inverse oracle.

## 3. A finite polynomial reciprocal with actual query access

The determinant itself is an actual coherent amplitude:

    C_0 C_1 C_2 C_3 = d T,  T=|top><vac|=c_0 c_1 c_2 c_3. (4)

Multiplication on the left by the **fixed** `T^T` gives `d P_vac`. With `M_A` the ordered product of fixed Majoranas `c_j+c_j^T` over a subset `A`,

    sum_A M_A T^T(C_0 C_1 C_2 C_3) M_A^T = d I_16.       (5)

The sixteen conjugated vacuum projectors partition the occupation basis. The left conversion in (5) is necessary: conjugation alone could not turn the trace-zero `dT` into `dI`.

All fixed creation/annihilation matrices used in this algebra are finite linear combinations of fixed orthogonal CAR matrices. Equation (5) is a finite operator polynomial, not a measurement or a free scalar oracle. For an exact finite gauge Ward identity one can instead consume the invariant moving-matrix-unit centralization (13bq1) in §6.25. A fixed CAR-basis decomposition by itself only proves the approximation below, not exact covariance of every finite approximant.

On the chosen orientation component let `s=sign d`. Hadamard gives `|d|<=kappa^4<1`. The polynomial with fixed integer coefficients

    r_N(d)=s sum_(k=0)^N (1-sd)^k

satisfies

    1/d-r_N(d)=(1-sd)^(N+1)/d,
    ||1/d-r_N(d)||_(C^1) <= C(N+1)(1-delta)^N.           (6)

Here `C` includes the bounded field derivative of `d`; it does not hide a variation of the fixed integer `N`. Replacing `1/d` in (3) by `r_N` gives `D_rs,N` with the same bound, and maximum moving-query degree `4N+2`. The number of terms is finite and fixed over the field chart. This is not a query-efficiency claim: a naive expansion can have a large coefficient norm.

For completeness, extraction of a creation block does not assume that its nonunitary matrix is a new gate. In a scalar Julia flag, `Pi_0 J(C_r) Pi_0=Pi_0 tensor C_r`. Products insert the same flag projector; replace `Pi_0` by `(I+Z)/2` to obtain a finite Laurent sum of actual unitary query words and fixed controls. Scalar flag matrix units can restore a common work-blank sector. Apply the same procedure to (5), (6), transposes and the skew parts below. This is precisely the product/Laurent construction of §§6.25 and 8.6. No postselection or one-step oblivious-amplification assumption is used.

## 4. A root-free quarter-turn gives the required reference accuracy

For the feedback consumer define `p=phi^{-1}`, `a=sqrt(p)`, and for one face

    D_A=(D-D^T)/2,  D_S=(D+D^T)/2,
    S0=(1/2)[[D_A, ap D_S],[-ap D_S,-D_A]],  S=sigma S0. (7)

This is the same full-CAR coframe reference used in `paired_feedback.md`; `S0` is real skew on dimension 32. Use the polynomial `D_N` in (7) for `S_N`, preserving skewness exactly. The canonical reference is

    R_S=[[S,sqrt(I+S^2)],[-sqrt(I+S^2),-S]].             (8)

It need not be supplied as a moving matrix-root oracle. Put

    R0=[[0,I],[-I,0]],  K_S=[[0,S],[S,0]],
    T_S=exp(-K_S/2).

Since `K_S` is skew and anticommutes with `R0`, direct multiplication gives

    Rcheap(S)=T_S R0 T_S^T
            =[[sinh S,cosh S],[-cosh S,-sinh S]].        (9)

This is an exact orthogonal complex structure: `Rcheap^T=-Rcheap`, `Rcheap^2=-I`. On `||S||<1` it differs from (8) by `O_(C^1)(sigma^3)` when `S0` and its first jets are bounded; the diagonal difference starts at `S^3/6`, the offdiagonal at order `S^4`.

The existing skew-polynomial execution lemma compiles `T_(S_N)` by finite product formulas. One direct mechanism is the owned `K(W)-K(W^T)=-X_f tensor(W-W^T)` followed by a fixed scalar basis rotation, giving the appropriate skew exponential on its clean scalar work sector. Controlled calls are obtained by the owned echo/half-log construction, not assumed separately. Reversing the **actual completed** word produces its actual adjoint on the declared retained sector; one must not replace this by an independently fitted inverse. Fixed `R0` and scalar basis rotations may themselves be approximated to the same budget if the selected primitive interface does not provide them exactly.

For each `h`, choose all these precision integers before field variation. Their combined whole-output `C^1` error on the specified clean-work cut can be any prescribed `epsilon_h>0`. The same applies when reference calls are embedded in the paired coherent word. Work outputs remain in the complement of the actual return projector. The construction therefore yields an approximate executed reference on the declared cut, **not** an all-work-sector exact realization of (8).

## 5. Source accuracy in the paired word

Let the actual ideal paired operation use `Vhat=diag(V,V^T)`, where `V=I+O_(C^1)(h^2)`, with all moving fields included. For either exact quarter-turn reference (8) or (9),

    F_R=p^3(2I-R^T Vhat-Vhat^T R),
    F_R at Vhat=I = 2p^3 I.                            (10)

Their flat baseline is identical for **every** coframe. Consequently the exact reference replacement error has the stronger bound

    ||F_Rcheap-F_RS||_(C^1)=O(sigma^3 h^2),
    ||S_Rcheap-S_RS||_(C^1)=O(sigma^3 h^2),             (11)

for `S_R=-logdet(I-zF_R)` on a fixed positive-pencil gap and fixed trace carrier. To see this, use `Delta R^T=-Delta R` in the difference of (10), so each term contains `Vhat-I`; then differentiate without freezing either factor. The logdet estimate follows by the resolvent chain rule. Relative to the paired Palatini coefficient, proportional to `sigma h^2`, (11) is `O(sigma^2)`.

Likewise, replacing `D` by `D_N` changes the exact quarter-turn price source by

    O(sigma h^2 (N+1)(1-delta)^N).                      (12)

Finite compilation error does not automatically preserve the quarter-turn identity or the exact baseline. It is therefore charged separately using the full-cut `C^1` perturbation estimate, including actual return rank, spectator multiplicity, pencil gap and `z` jets. Choose the operator approximation precision so that this **actual source error** is `o(sigma h^2)`. The ideal pairing must use the actual compiled inverse of the actual forward word, not a second independently approximated operation.

For example, on `h=p^k`, take the already proposed native `sigma=p^(3k)=h^3`, a fixed-for-that-mesh `N_h` with `(N_h+1)(1-delta)^N_h=O(h^3)`, and tighten the finite-word precision until its full-cut source error is `O(h^6)`. Then (11), (12) and compilation all vanish relative to `sigma h^2=h^5`. If the trace/work carrier grows with precision, its actual rank factors are included when choosing that precision; no rank-free rate is claimed. Exact-exponential (11) actually only needs `sigma->0`, since its baseline is identical.

The same reasoning works facewise for all six original Hodge faces, with their original orientation signs and sampling factors. Derivatives include the inverse determinant, observer whitening and link dependence of `V`; there is no frozen reference during variation.

## 6. Exact admission and payment boundary

The previously missing **coframe-reference matrix map** has been reduced to actual onsite creation Julia calls, fixed controls, polynomial arithmetic and the already owned skew-exponential compiler. A separate coframe-controlled matrix input, Hodge oracle, fitted continuous rotation or pointwise-density argument is unnecessary inside that interface.

What this theorem does not remove:

1. Actual coherent onsite Julia actuation and the declared scalar work preparation/cut must be admitted. If only the old measured instrument is available, coherent query access is still the missing operation. Countable fixed Golden words alone cannot supply a continuum of moving creation matrices.
2. The edge/direct-face map is separate. A product of original edge Julias is not automatically `J(p Lambda(P))`; this proof does not identify them.
3. The price of the complete executed word, work resources, copies, inverse execution and off-cut histories remains actual. Fixed query counts imply constant count-clock derivatives only under the original fixed-count rule; label costs and information need not be constant. No whole-HJR source or fundamental selection claim follows.

Verification: `check_coframe_oracle_transport.py` performs exact rational checks of all six original Hodge identities, all 96 coframe first jets, the full CAR16 lift, determinant word and scalarization, signed reciprocal remainder, and the root-free quarter-turn jet. It is a bounded algebraic certificate, not a gate-level execution or payment simulation.
