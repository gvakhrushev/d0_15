# Stopped terminal readout: full classical and coherent first sources

Owner: existing Draft #334, `constitutive` / `native_sector`.
Phase: native realization, conditional component estimate.
Input: `6e86ccbe2d0df83b920bc9307b5f82cb686b5010`, specifically
`sources/d0_native_flag_source_minimum_2026-10-20/flag_source.md` and
`sources/d0_relational_coherent_synthesis_2026-10-20/fixed_readout.md`.
No new execution, physical price, Info algebra or admission law is selected.

## 1. Same carrier, process, variations and consumer

Use the owned compact CAR16 Julia letters, full oldRIGHT purification,
chronological stopped flag tree, fixed success target m and attempt cap N.
Every leaf s has actual weight w_s=p^(T_s+K_s), including unfinished leaves;
sum w_s=1. Completed leaves share psi_m=(U_m tensor I)psi; failed leaves
have their actual psi_k. Let epsilon=sum_failed w_s. Hold m,N and w fixed
under the field derivative. All vectors are normalized in one specified
isometrically trivialized Hilbert fiber. Assume ||D_V psi_k||<=B||V||
for EVERY k, including supplied preparation/reference/observer jets.
The phase used to establish this bound is part of the supplied chart.

For the coherent statement supply a fixed finite instrument M_r with
sum M_r* M_r=I, and its actual isometry W=sum_r |r> M_r. The residual output
Hilbert space Q has dimension d, independent of the number of flag words.
For the specified full CAR16 Choi square-root instrument d=256 and R=17.
Its right Gram is I16/16 BEFORE this final readout; measurement on the joint
Choi carrier need not preserve that Gram afterwards. This is not an
identification with full128/reference128. The effects alone do not identify
the instrument of another historical implementation.

The parent source is the derivative of the declared reduced-record entropy
or fixed-code component in the actual field norm; its dual norm is used
below. The estimate removes rare unfinished-prefix contributions to this
terminal source. The ideal successful terminal source is retained, as are
all implementation, preparation/controller/work/clock prices and the
physical choice of Info. An exponentially accurate completion protocol
does not make its successful terminal source small.

## 2. Complete classical joint law: no outcome floor

Put q_kr=||M_r psi_k||^2. Measuring all retained flags and terminal outcomes
gives EXACTLY Q_sr=w_s q_(K_s,r), hence, with natural-log entropy,

    H(Q)=H(w)+(1-epsilon)H(q_m)+sum_failed w_s H(q_Ks).

This is a readout of a specified diagonal observable algebra, not physical
deletion of the coherent flags. In particular

    |H(Q)-H(w)-H(q_m)| <= epsilon log R.                 (1)

The function -||a||^2 log||a||^2 is C1 at a=0. Applying its derivative to
the blocks a_r=M_r psi_k, using sum ||D a_r||^2<=B^2 and
max_(0<=x<=1) x log^2 x=4/e^2, proves

    ||D H(q_k)||_* <= 4 B sqrt(R)/e,
    ||D H(Q)-D H(q_m)||_* <= 8 epsilon B sqrt(R)/e.       (2)

Normalization removes the '+1' term of the entropy derivative. Outcomes
of probability zero contribute their continuous zero derivative; no
division by a nonzero probability, or uniform floor, is required.

For a fixed positive normalized code reference mu_r, let
L_r=-log_phi mu_r and Lmax=max L_r, ell=log phi. The actual joint reference
is w_s mu_r, so the exact relative-code chain rule is

    D_phi(Q || w tensor mu)
      =(1-epsilon)D_phi(q_m||mu)+sum_failed w_s D_phi(q_Ks||mu).

Its first-source error from D_phi(q_m||mu) is bounded by

    epsilon B [4 Lmax+8 sqrt(R)/(e ell)].                (3)

The raw Golden flag code E L_s=H_phi(w) still has its full nonzero value.
It cancels in this specified relative-code component only because the
reference contains the SAME w. A different compulsory Book code needs
its own calculation. Self-information is not inserted as a physical cost.

## 3. Coherent flags plus final pointer: complementary spectrum

Keep the actual pure state, including all records,

    |Xi>=sum_s sqrt(w_s)|s>_F sum_r |r>_R M_r|psi_Ks>_Q.

No flag or pointer is dephased for this statement. The reduced archive
rho_FR has the SAME nonzero spectrum as

    rho = (1-epsilon) C(tau_m)+sum_failed w_s C(tau_Ks),
    C(X)=sum_r M_r X M_r*,   tau_k=|psi_k><psi_k|.

Thus S(rho_FR)=S(rho). The ideal successful archive has entropy
S(rho0), rho0=C(tau_m). Its pointer generally has OFF-DIAGONAL coherences;
this entropy is NOT H(q_m). Fixed-channel trace-norm contraction gives

    ||rho-rho0||_1 <= 2 epsilon,
    ||D rho-D rho0||_1 <= 4 epsilon B,
    ||D rho0||_1 <= 2 B.                                (4)

The complementary amplitude matrices have columns sqrt(w_s) M_r psi_Ks
and M_r psi_m respectively. Both have Hilbert--Schmidt derivative at most
B, regardless of the number of histories.

For 0<eta<=1 use S_eta(rho)=Tr[-(rho+eta I)log(rho+eta I)+eta log eta I].
The existing amplitude regularization proof gives, for either amplitude,

    |D S-D S_eta| <= 2 B sqrt(d eta).                    (5)

Indeed each singular gradient error is
2 sqrt(lambda) log(1+eta/lambda)<=2 sqrt(eta), continuously zero on an
exact zero singular value. This is a FULL matrix derivative statement.
Also the resolvent integral for log gives

    ||log(rho+eta I)-log(rho0+eta I)|| <= 2 epsilon/eta.

Using (4), trace derivative zero and
||log(rho+eta I)||<=log(1/eta)+log 2, yields

    ||D S(rho_FR)-D S(rho0)||_*
      <= 4 B sqrt(d eta)
         +4 epsilon B [log(1/eta)+log 2+1/eta].           (6)

This proof allows rank births in both actual and ideal outputs. With
eta=epsilon^(2/3), it gives the explicit no-floor bound

    4 B [(sqrt(d)+1)epsilon^(1/3)
          +epsilon((2/3)log(1/epsilon)+log 2)].           (7)

At epsilon=0 the spectra and ALL first derivatives agree exactly.
This deliberately conservative estimate is sufficient for the owned
exponential cap. It does not assert optimal continuity exponents or C2.
There is no requirement that the original readout commute with rho or
that its effects be rank one. The fixed-instrument assumption supplies
the channel derivative in (4); the extension below accounts for it when
the actual observer/instrument moves.

### Moving observer/instrument extension on the supplied fiber chart

Allow a differentiable actual isometry W_y with the SAME finite input,
pointer and residual output types in the stated trivialization. Suppose
||D_V W_y||<=A||V|| and ||D_V psi_k||<=P||V||, and set B=P+A.
The branch amplitudes W_y psi_k have first jet at most B. For Hermitian X,
the actual channel C_y(X)=Tr_R W_y X W_y* satisfies

    ||(D_V C_y)(X)||_1 <= 2 A ||X||_1 ||V||.

This follows from the two differentiated Stinespring factors, followed
by trace-norm contraction on their Hermitian sum. Consequently

    D(rho-rho0)=C_y(D Delta tau)+(D C_y)(Delta tau),
    ||Delta tau||_1<=2 epsilon,
    ||D Delta tau||_1<=4 epsilon P,
    ||D(rho-rho0)||_1<=4 epsilon(P+A)=4 epsilon B.

The ideal derivative is at most 2B. Thus (1)-(7) hold unchanged with
this actual B, including the channel/observer first source. This extension
requires fixed cap weights and the actual isometry and its jet bounds;
probabilities/effects alone do not supply them. A parameter-dependent
square root need not have a bounded jet at an effect rank birth, so such
a bound must be proved or supplied rather than inferred from smooth effects.

### Coherent relative-code component on the complete archive

For the SAME fixed positive reference mu, the complete archive reference is
Gamma=diag(w_s mu_r). Its actual diagonal is w_s q_(K_s,r), hence exactly

    D_phi(rho_FR||Gamma)
      =H_phi(w)+sum_s w_s sum_r q_(K_s,r) L_r-S(rho)/ell.

This calculation retains OFF-DIAGONAL archive coherences through S(rho).
The ideal successful terminal component is

    C_m=sum_r q_mr L_r-S(rho0)/ell.

Its first-source difference from the complete relative-code price is bounded
by 4 epsilon B Lmax plus (6), or (7), divided by ell. H_phi(w) retains its
full value and has zero derivative only under the fixed-tree variation.
The auxiliary all-branches-completed comparison state is the product of
sum_s sqrt(w_s)|s> with W psi_m. It is a mathematical comparison, not an
admitted cheaper execution or erasure of real failed attempts and clocks.
It has the same flag diagonal w, so the reference and source comparison
are on one specified record algebra. This does not set native Info equal
to a chosen reduced entropy or remove the cost of coherent access.

The complete dephasing/coherence split is also exact on this carrier:

    D_phi(rho_FR||Gamma)
      =D_phi(Q||w tensor mu)+[H(Q)-S(rho)]/ell.

Thus the retained terminal coherence-source contribution approaches
[D H(q_m)-D S(rho0)]/ell, rather than zero by definition. Its source
error is bounded by (2) plus (7), divided by ell. The large H_phi(w)
value remains in the coherence term. Neither dephasing all records nor
equating classical and coherent Info follows from the cap estimate.

## 4. Application to the owned refinement and scope of substitution

For m_h=floor(tau/h^2), N_h=ceil(2m_h/g), the owned theorem supplies
epsilon_h<=exp(-m_h/4). Therefore (2), (3) and (7) vanish after ANY fixed
polynomial source normalization, provided B_h, d_h, R_h and Lmax_h grow
at most polynomially. For the coherent estimate the dominant exponential
is exp(-m_h/12). For a sum of local source terms, sum the actual B_(x,h)
bounds (with their d,R,code factors) BEFORE applying the normalization.
Polynomial site count and bounded-overlap maps suffice; an unproved local
to global identification is not being made. The derivative fixes the
integers m_h,N_h at each h, rather than differentiating a floor function.

This substitutes a quantitative terminal rare-failure estimate into the
compact component calculation that previously stopped BEFORE final readout.
It leaves an explicit ideal-source computation on the SAME instrument:

    D H(q_m), D S(C(tau_m)), D D_phi(q_m||mu), or D C_m,

depending on the actually selected observable/price algebra. These are
different quantities. They are not automatically zero, equal to the flag
source, or the source of the full Book action. The square-root instrument
is a declared extension of the owned POVM; transferring this result to a
different actual instrument requires its instrument map.

Moving instruments are not silently frozen: the extension above carries
their supplied isometry jets and channel derivative. The fixed-instrument
case suffices for the existing fixed Golden17 chart. Neither case supplies native
observer/actuator admission, no full128 or noncompact theorem, no minimum
selection, no physical Einstein source and no uniform nonlinear recovery.
`GR_closed=false`; raw216 and the original task terminal remain open.

## 5. Decisive checks

`check_terminal_readout.py` independently builds the fixed full-CAR16
Golden17 square-root instrument and all exterior grades. It checks the full
stopped word tree, exact Golden weights, classical joint-chain/source
identities, actual coherent-complement sources, the estimates and a dark
marked outcome with continuous entropy derivative. A fixed-code hostile
control keeps a nonzero ideal successful source when cap error shrinks.
The calculation validates this application; the universal inequalities are
proved above rather than inferred from sampled caps.
