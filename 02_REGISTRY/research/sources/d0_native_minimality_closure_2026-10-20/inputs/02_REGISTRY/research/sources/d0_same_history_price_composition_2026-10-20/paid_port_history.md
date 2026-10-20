# Actual all128 paid-port history partition and its complete source

Research derivation for existing native programme / PR #334.
The new object is the generating function of the actual original port code
cost, not a new dynamics, a new physical action or an identification of Info.
The real parameter t below is only an analysis variable. No new primitive
fugacity or price is selected by varying it.

## 1. Same actual instrument and complete retained history

Consume `A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md` §§1–3.
On the existing data Hilbert space, including every site and CAR16 grade,
write p=phi^-1, p+p²=1, a=sqrt(p), A=hD/16=A*, Delta=D²,
epsilon=p²h²/64. The actual 64 label/coefficient rows obey

    N_0=A,       sum_k N_k N_k*=I,
    T(X)=sum_k N_k* X N_k.

The complete original 128 Kraus operators, with k=0,...,63 and b=0,1, are

    K_(0,k)=delta_(k,0) I - 2p² N_k* A,
    K_(1,k)=                 - 2p sqrt(p) N_k* A.

All maps act as identity on the unchanged oldRIGHT/reference. Every fresh
label/coefficient/port is retained in the global record. Repeating n rounds
uses precisely the original fresh-round channel; it does not reset data or
erase old records. For omega=((b_1,k_1),...,(b_n,k_n)), put

    K_omega=K_(b_n,k_n)...K_(b_1,k_1),
    q_y(omega)=Tr K_omega rho_y K_omega*,
    C_port(omega)=sum_j(1+b_j)=n+N_port1(omega).

This is the original direct0/return10 code, of costs 1 and 2. It is ONLY the
known port part of the full physical cost. The actual label, controller,
archive, preparation and work prices are not set to zero. The same fixed n
and literal outcome labels are used throughout field differentiation.

The finite, positive, all-outcome cost transform is

    Z_n(t;y)=sum_omega q_y(omega) exp[-t C_port(omega)] > 0.

Equivalently it is the expectation of the diagonal function exp(-t C_port)
on the actual retained tape. With a purification psi_y on data x oldRIGHT,
it is the squared norm of the analytical, generally unnormalized vector

    sum_omega exp[-t C_port(omega)/2] |omega> (K_omega tensor I) psi_y.

The distinct history labels remain orthogonal; no interference classes,
failure histories or oldRIGHT columns have been removed. This vector is a
generating-vector representation, not an asserted free physical filter.

## 2. Exact new cost-tilted transfer on the actual full carrier

Set x=exp(-t)>0 and a_x=p²+px. Define the actual cost-weighted CP map

    Phi_t(X)=sum_(k,b) x^(1+b) K_(b,k) X K_(b,k)*.

Then the exact all-size operator identity is

    Phi_t(X)
      =x [X + epsilon (a_x T(D X D) - {Delta,X}/2)].       (1)

Proof directly from every original Kraus row: set M_k=N_k* A. Then
sum M_k X M_k*=T(A X A) and M_0=A². The b=0 sum is

    X - 2p² {A²,X} + 4p^4 T(A X A),

whereas the b=1 sum is 4p³ T(A X A). Multiply respectively by x and x²,
use A=hD/16 and epsilon=p²h²/64, and obtain (1). No commutation of X,D
or any row is used. Complete row unitarity makes T trace preserving, so

    Tr Phi_t(X)=x [Tr X + epsilon p(x-1) Tr(Delta X)].     (2)

At t=0, (1) is precisely the original trace-preserving Phi. For arbitrary
real t the weighted map is CP because its defining Kraus coefficients are
positive. It is not asserted trace preserving away from t=0.

The exact finite-horizon partition is therefore

    Z_n(t;y)=Tr Phi_t(y)^n(rho_y).                       (3)

Equation (3) follows by expanding the n-fold product into all 128^n
ordered complete outcomes. It is a contraction of their full weight sum,
not a deletion or quotient of physically retained histories.

This is different from the previous total-EXIT transform
`Bmap+exp(s)Jmap`: its mark is the actual original cost 1 or 2, including
every blank-label port and all nonblank labels. Its nontrivial coefficient
`a_x=p²+px` multiplies recycling; replacing it by a scalar clock factor
times the original channel gives a wrong partition and wrong source.

## 3. Complete field, preparation and clock source

Take any genuinely admitted smooth field/preparation direction V on the
same fixed Hilbert fiber, with fixed integer n and fixed Golden p. A moving
observer/pairing requires the owned isometric trivialization and its
derivative in D, N_k and rho. Do not omit them. Write r_0=rho and

    r_(j+1)=Phi_t(r_j),
    dr_0=drho,
    dr_(j+1)=Phi_t(dr_j)+(dPhi_t)(r_j).

Then dZ_n=Tr dr_n. Equivalently, with E_(j+1)=(Phi_t*)^(n-j-1)(I),

    dZ_n=Tr[(Phi_t*)^n(I) drho]
           +sum_(j=0)^(n-1) Tr[E_(j+1) (dPhi_t)(r_j)].   (4)

At fixed analysis variable t,

    dPhi_t(X)=x { d epsilon [a_x T(DXD)-{Delta,X}/2]
          + epsilon [a_x ((dT)(DXD)+T(dD X D+D X dD))
                     - {dDelta,X}/2] },                (5)
    dDelta=dD D+D dD,
    (dT)(Y)=sum_k[(dN_k)* Y N_k+N_k* Y dN_k].

All data/oldRIGHT preparation derivatives, native Julia-root derivatives,
adjoints, geometric/link/observer jets and any admitted clock epsilon jet
are explicit. If h moves, epsilon and N_0=hD/16 must move consistently;
the formula does not authorize choosing epsilon independently. Changing
integer n is a comparison of different programmes, not this smooth jet.
For normalized rho=Sigma/Tr Sigma use
drho=(dSigma-rho Tr dSigma)/Tr Sigma.

Since the unweighted full process is trace preserving, Z_n(0;y)=1 on the
whole admitted family, and dZ_n(0;y)=0. The first nontrivial joint source is
the cost response, not a missing field dependence hidden in log 1.

## 4. Exact actual finite-horizon cost and variance

Define marked maps on the same full128 instrument:

    M_1(X)=sum_(k,b) (1+b) K_(b,k) X K_(b,k)*,
    M_2(X)=sum_(k,b) (1+b)^2 K_(b,k) X K_(b,k)*.

Direct differentiation of (1), or summing the two actual ports, gives

    M_1(X)=Phi(X)+p epsilon T(D X D),
    M_2(X)=Phi(X)+3p epsilon T(D X D).                    (6)

Let rho_j=Phi^j(rho). Then exactly

    E C_port=n+p epsilon sum_(j=0)^(n-1) Tr(Delta rho_j), (7)
    -partial_t log Z_n|_(t=0)=E C_port,
    partial_t² log Z_n|_(t=0)=Var C_port.                (8)

For the full second moment without any independence assumption propagate

    u_0=v_0=0,
    rho_(j+1)=Phi(rho_j),
    u_(j+1)=Phi(u_j)+M_1(rho_j),
    v_(j+1)=Phi(v_j)+2M_1(u_j)+M_2(rho_j).

Then Tr u_n=E C_port and Tr v_n=E C_port². These are the exact derivatives
of the same all-outcome partition; the complete actual correlations are
kept in u_j and v_j. Mixed field/t derivatives commute in every finite smooth
chart. In particular

    -d_y partial_t log Z_n|_0
      =p (d epsilon) sum_j Tr(Delta rho_j)
       +p epsilon sum_j Tr[(dDelta)rho_j+Delta d rho_j],  (9)

with the actual unweighted sensitivity recursion for d rho_j. The n term
has zero field derivative only at this fixed integer clock. Its paid value
must remain when prospective minimality compares different programmes.

## 5. Exact full16 scalar-shell specialization

Use the ORIGINAL flat Fourier shell, preserved by every original Kraus
operator, on which Delta=lambda I16. No form grade or oldRIGHT/reference
component is removed. For any normalized system/reference preparation in
that shell, put r=p epsilon lambda. The actual port1 effect is r I, so at
every prefix its conditional port1 probability is r independently of the
conditioned data state. Therefore the port bits are IID Bernoulli(r), even
though the remaining labels and conditional matter states can be correlated.

Equation (2) yields, exactly at every finite n,

    Z_n(t)=exp(-nt)[1-epsilon p(1-exp(-t))lambda]^n,       (10)
    E C_port=n(1+r),
    Var C_port=n r(1-r).                                (11)

For an actually moving scalar-shell family, r'=p(epsilon' lambda+
epsilon lambda'),

    d log Z_n=n (x-1) r'/[1+(x-1)r],
    d E C_port=n r',
    d Var C_port=n(1-2r)r'.                             (12)

These shell derivatives apply only when that family stays in the stated
scalar, invariant shell. Arbitrary proper-link/observer/coframe directions
must use (4)–(5); being scalar at one base point alone is insufficient for
dropping the actual recycling/preparation derivatives.

## 6. Exact scope and consuming missing Book map

Equations (1)–(12) close the actual complete original PORT-COST history
normalizer and its complete first source, with all records and primitive
round counts retained. They supply a concrete cost-deformed transfer to the
clock/first-return Schur construction. Unlike a generic Gibbs identity,
the transfer here is derived from the literal original 128 Kraus operators.

No identification of Shannon entropy with Book Info is made. No maximum or
minimum principle on t or these tilted histories is asserted physical.
The known port price does not include the remaining labels, controller,
preparation or work. Book03's algebra-valued sum uses amplitude/memory
classes before quadratic readout; its complete Cost−Info weight still
requires its own same-process map to this (or another actually forced)
positive history normalizer. The result does not identify the cycle
determinant with this normalized tape, choose a resetting boundary, close
the remaining field equations or prove GR.

## 7. Targeted exact original-carrier check

`check_paid_port_cost.py --root REPOSITORY` constructs the original 32
Walsh-controlled Julia words, both coefficient rows and both Golden ports.
It checks every complete row and Kraus sum on all CAR16 grades, using exact
sparse Q(i) matrices and Q[p]/(p²+p−1) coefficients. The sqrt(p) port1
amplitude is retained in its exact quadratic CP weight, not rounded away.

The two actual source fixtures are the original h=1/4, nu=3/5 nonzero flat
Fourier shell and a compact proper J23 link with cos(theta)=3/5,
sin(theta)=4/5 on the same native row. All positive Julia roots and their
true link derivatives are checked. A normalized full-rank preparation and
a nonzero LEFT-unitary preparation jet preserve the same oldRIGHT Gram.
This finite Fourier fixture has a rank16 density and 16 active purification
columns; it is not a replay of the original full-site fixedRIGHT128 Riesz
preparation. The all-size theorem tensors the identity on arbitrary oldRIGHT
and therefore applies to rank128 preparation when the actual data carrier
has sufficient dimension, without changing any of the formulas above.
Both an incorrectly frozen preparation and an incorrectly frozen native
epsilon are rejected by nonzero exact sources. An omitted recycling tilt
and a substitution of total exits for port1 are separately rejected.

The whole two-round sum is evaluated by exact CP contraction of all128
Kraus operators, and therefore contains all16384 ordered histories. At the
original scalar shell lambda=288/25, epsilon=p²/1024, it gives

    r=-9/800+(9/400)p,
    E C_2=791/400+(9/200)p,
    Var C_2=-1521/64000+(1881/40000)p.

The all-n derivatives of (10) are checked independently and give exactly
(11). The script checks the two original source hashes before calculating,
writes no repository files and only prints its deterministic JSON result.
This exact finite checker supports the all-size derivation above; it does
not turn the missing full Book Info/price identification into a premise.
