# Finite closed-record pressure: a uniform first-source cut and its real cost

20 October 2026. Existing research owner #334 / native-programme-v1.
Input tree: f569c786730301e1603ee64062beccc6b20d05e7.
This consumes the original full128 fixed-horizon isometry, its actual
port-cost insertion, and the companion basis-free symmetric-record identity.
It does not select a new physical action or identify entropy with Book Info.

## 1. The finite object and the precise parent substitution

Let A=Q_0 V_n on the entire original data x oldRIGHT cut, of dimension d.
Thus F=A* A=(I-B^(2n)) tensor I_128 and 0<=F<=I. Each retained output
contains its whole chronological n-round record. Put G=zF, 0<z<1/2,
q=z||F||<1/2, and

    Z=det(I-G)^(-1),    J=log Z,
    Z_R=sum_(r=0)^R z^r ||Sym^r A||_HS^2,    J_R=log Z_R.

The companion proof realizes the coefficients by positive squared norms of
the actual r-copy map with a symmetric INPUT preparation. It does not erase
chronology inside a copy, identify distinct ordered output tapes, or assert
that the extra copies/reference/preparation are already compulsory D0 gates.
The finite sum is the genuine finite-occupation mathematical carrier. Here we
remove its previously unquantified VALUE AND FIRST-SOURCE truncation premise,
uniformly across dark eigenvalues. This is not a theorem that this preparation
is physically free, or that J is the complete cost of executing it.

## 2. Exact occupation bound without a positive eigenvalue floor

Write h_r(F)=Tr Sym^r F, and let the nonnegative integer N have law
P(N=r)=z^r h_r(F)/Z. For 1<a<1/q set

    M_a=((1-q)/(1-aq))^d,
    e_R=a^(-(R+1)) M_a.

Then

    P(N>R)<=e_R,
    0<=J-J_R=-log(1-P(N>R))<=-log(1-e_R),       (1)

whenever e_R<1. Indeed

    E a^N=det(I-G)/det(I-aG)<=M_a,

since (1-x)/(1-ax) is increasing for 0<=x<=q. Markov's inequality gives
(1). Zero eigenvalues cause no singularity.

For every Hermitian first variation X=delta F at fixed z and fixed d,

    |delta(J-J_R)|
      <= z d ||X|| M_a a^(-R)/(1-e_R)
           [1/(1-aq)+1/(a(1-q))].                    (2)

All admitted jets of A and its cut enter X, including their actual
coframe/link/observer/preparation sources. The stated symmetric input is held
fixed; an independent change in its coefficients has a separate source.
No eigenbasis is held physically fixed. To prove (2), the positive polynomial h_r has positive
matrix gradient on F>=0, and its exact symmetric-polynomial identity is

    sum_i partial_(lambda_i) h_r=(d+r-1) h_(r-1).

Consequently |delta h_r|<=||X||(d+r-1)h_(r-1). With
tau=P(N>R), differentiation of the two convergent series gives

    |delta tau| <= z||X|| E[(d+N) 1_(N>=R)]
                  +tau z||X|| E(d+N).

The two expectations obey

    E[(d+N) 1_(N>=R)]<=a^(-R) M_a d/(1-aq),
    E(d+N)<=d/(1-q).

Divide by 1-tau to obtain (2). The proof is polynomial at each finite R
and uses absolute convergent generating series for the tail; it does not
differentiate an unproved estimate or divide by a small eigenvalue of F.

## 3. The original full128 physical clock gives an explicit uniform C1 cut

Keep the original n=128L^2, m=2n, alpha=p^2/(128L^2), beta=m alpha=2p^2,
and z=2^(-20). The entire closed cut has d=2048L^4, with every CAR16
grade and all128 oldRIGHT columns counted. On 0<=B=I-alpha Delta<=I,

    delta F=alpha sum_(j=0)^(m-1) B^j(delta Delta)B^(m-1-j) tensor I_128,
    ||delta F||<=beta ||delta Delta||.                  (3)

Thus a finite occupation cap can preserve the original first source in
the norm dual to ||delta Delta||, including noncommuting jets. For any
declared nonnegative normalization power s, choose, for L>=2,

    R_L=ceil[d z/((1-2z)log 2)+(s+6)log_2 L].           (4)

Since log M_2<=d z/(1-2z), equations (1)-(4) give

    e_(R_L)<=1/(2 L^(s+6)),
    L^s |delta(J-J_(R_L))| <= C z beta L^(-2)||delta Delta||,
    L^s |J-J_(R_L)|=O(L^(-6)),                         (5)

where C is an explicit constant obtained from (2) and d=2048L^4, independent
of L and the smallest nonzero eigenvalue. If the physical variation norm
has a growing Delta-jet budget, that budget must multiply (5), or the cap
must be increased accordingly. No unproved uniform physical chart bound
is inserted. A fixed occupation cut is not asserted sufficient at refinement.

This supplies a FINITE value/source realization of the closed pressure as a
mathematical record functional. Primitive admission and complete resource
payment of the symmetric-input experiment remain separate physical premises.

## 4. The conditional return ensemble has a real clock price

Let C be the original retained port cost on one exit tape: n<=C<=2n.
For r copies the additive cost C^(r)=sum_(a=1)^r C_a obeys

    nr<=C^(r)<=2nr.

On the normalized symmetric ALL-RETURN ensemble the companion marked-return
identity therefore implies, exactly,

    n E N <= E C_total <=2n E N,
    E N=z Tr[F(I-zF)^(-1)].                            (6)

This is a CONDITIONAL expectation: all r copies return nonblank. It is not
the price of the complete apparatus, which also retains failed copies;
section6 supplies that distinct unconditional price. It is a bound on known
additive port-code cost, not on parallel wall time and not on complete Book
Cost-Info. Extra controller, copy and preparation charges remain uncomputed.
In particular the norm identity defining Z does not supply a zero-cost
realization of Z.

There is a sharper SAME-CARRIER test on the original flat physical-coframe
family Delta=rho mu_L tensor I_16, rho>0,

    mu_L(k)=sum_(r=0)^3 [2-2cos(2pi k_r/L)],
    0<=mu_L<=16,    Tr(mu_L)=8d,
    f_k=1-(1-alpha rho mu_L(k))^m,
    R_k=(1-zf_k)^(-1).

The already owned full128 energy conservation on these shells gives the
exact insertion C_exit=nF+p beta Delta (with oldRIGHT included). Hence

    E C_total=n z Tr(RF)+p beta z Tr(R Delta).           (7)

There is no shell deletion and no assumption that a varying proper-link
matrix remains scalar. Formula (7) is used only on this stated scale family.
At least a third of its modes have mu_L>=4, since their mean is8 and their
maximum16. Thus

    (1-exp(-4beta rho)) L^6/12 <= E C_total
                           <= L^6/[2(1-z)].            (8)

The lower bound uses nzd=L^6/4. This is the conditional cost in this extra
symmetric-copy interpretation, not a lower bound on every possible physical
implementation of a determinant. The original pressure J=O(L^4) and the
conditional additive execution cost Theta(L^6) are different here.

## 5. A conditional first-source separation, not just a value mismatch

The reduced coherent OUTPUT density of the normalized symmetric state has
the nonzero eigenvalues of independent geometric occupations x_k=z f_k.
Its von Neumann entropy (natural logs) is therefore exactly

    S_out=sum_k [-log(1-x_k)-x_k log(x_k)/(1-x_k)].       (9)

This formula is proved by the normalized product spectrum; no physical
eigenbasis preparation is required. It is one precise candidate information
quantity, NOT a declaration of the original Book Info or of complete
distinguishability of the entire apparatus. The purified whole state is pure;
the trace over the dual input reference must remain explicit.

For fixed rho>0, and fine meshes with 16alpha rho<=1/2, differentiating the
actual scale family gives

    partial_rho E C_total >=2 beta exp(-32 beta rho) L^6,
    0<=partial_rho J<=beta L^4/[64(1-z)],
    0<=partial_rho S_out<=d z(-log z)/[rho(1-z)^2].       (10)

For the first inequality, f'_k=beta mu_k B_k^(m-1),
B_k^(m-1)>=exp(-2beta rho mu_k)>=exp(-32beta rho),
and the second term of (7) has nonnegative derivative. For the entropy,
concavity of f_k(rho) with f_k(0)=0 gives rho f'_k<=f_k; moreover
x(-log x) is increasing for 0<=x<=z<exp(-1). This also controls dark
eigenvalues continuously. Therefore the derivative of the explicitly tested
candidate

    E C_total-S_out/log(phi)

has a positive Theta(L^6) leading term and cannot equal the original
closed-pressure derivative, which is O(L^4). This is an exact scoped
source separation on the original full spectrum, not a claim that ALL
possible native Info/work laws fail. It rules out calling the Born norm
identity itself a complete Cost-Info derivation. The actual additional
terms cannot be chosen to cancel (10) without their own physical owner.

## 6. Complete apparatus: all failures, finite preparation and actual cost

The companion construction additionally supplies a fully normalized finite
INPUT state: the r-sector is vec(P_sym,r), with coefficient z^(r/2), and
0<=r<=R. Its normalization is the field-independent

    Z_in,R=sum_(r=0)^R z^r binom(d+r-1,r).

Execute the FULL isometry V_n in every ordered copy. Every failed and
successful tape remains in the apparatus. The probability that every copy
is nonblank (vacuously true for r=0) is exactly

    P_all-return,R=Z_R/Z_in,R,
    J_R=log P_all-return,R+log Z_in,R.                  (11)

The extra preparation and dual input reference are explicit resources;
their primitive admission and price are not provided by an isometry formula.
Equation(11) is a complete positive readout representation, not physical
postselection or an assertion that no-return labels cost nothing.

Let N_in,R be its actual occupation, with probabilities proportional to
z^r binom(d+r-1,r), and C_op=V_n* C V_n on the full input. The normalized
symmetric input in each r-sector has single-copy marginal I/d, so the
complete unconditional known port cost is exactly

    E_all C=(E N_in,R/d) Tr C_op.                       (12)

This is also valid for correlated symmetric copies; independence is not
assumed when evaluating an additive observable. The factor E N_in,R is
field-independent at fixed R,d,z. In the convergent unrestricted generating
ensemble E N_in=d z/(1-z). On the original physical scale family,

    Tr C_op=nd+p beta Tr Delta,
    E_all C=z/(1-z)[nd+p beta Tr Delta],
    partial_rho E_all C=p beta L^4/[64(1-z)]>0.         (13)

The field-independent Theta(L^6) baseline in (13) does NOT have the
Theta(L^6) source of the conditional ensemble in section5. That difference
is exactly why conditioning the cost on successful return is invalid as a
replacement of the full apparatus. At finite R the same identity holds
with z/(1-z) replaced by E N_in,R/d, with no infinite protocol required.

If one tests coherent entropy of the entire retained OUTPUT (data, oldRIGHT
and all chronological tapes) after tracing ONLY the added dual input
reference, the full isometry preserves that density's nonzero spectrum.
Its entropy is therefore field-independent. Thus this precise complete
Cost-minus-coherent-entropy candidate has the nonzero source (13), or its
finite-cap version; it does not acquire the original J source just from
the determinant norm. An entropy of POINTERS ALONE is a different partial
trace and is not asserted constant. Neither choice is declared Book Info.

The exact identity (12), not the conditional scaling argument in section5,
is the resource statement for the complete normalized apparatus. This
distinction is required even though (11) represents the pressure exactly.

## 7. Use in the parent argument

The finite symmetric construction and (2)-(5) remove a mathematical
infinite-occupation/source-limit premise from the positive closed-record
interpretation. They do not remove its admission or full-price premise.
Equations (7)-(13) make the conditional versus complete-price test explicit
at the same physical coframe scale used by the primary GR family. Combined with the companion
clock-resolvent inversion, a closed endpoint/pressure, a retained clock and
a complete executed price have exact maps between them, without being
silently identified. Full Book selection, the curved all40+matter source
and physical GR closure remain open.

The companion checker tests the new symmetric-polynomial derivative,
finite occupation/source bounds at a dark eigenvalue, and the exact
original flat-spectrum price/entropy source formulas. It does not replay
the unchanged original full128 Kraus proof or the previous all40 proof.
