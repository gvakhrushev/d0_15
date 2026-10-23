# Native CAR clocks: a concrete deformation-bracket test

21 October 2026. Bounded continuation of d0_15 PR #334 at scientific input
`441bdef5a02bef09a74ebe48dcf4d5527ba18988`. This is a **kinematic operator
identity and a new test of a possible constraint route**, not physical normal
clock admission, a canonical gravity constraint algebra, or GR closure.

## 1. Why this is the relevant alternative

The paid moment writer and the previous saddle theorem now allow lower-price
nearby field programmes on the declared counted-CQ action-word interface.
More positive-price minimization on that interface cannot establish this
particular saddle as a minimum of that same price. An alternative native
stationarity principle therefore needs a concrete mechanism.

One possible mechanism is consistency of local time changes: changing two
local normal displacements in opposite order should differ by the appropriate
spatial relabelling and internal-frame transport. This is the idea behind
Teitelboim's hypersurface-deformation equations and the Hojman--Kuchar--
Teitelboim reconstruction, under their substantial canonical and geometric
assumptions. D0 does not already satisfy those assumptions merely by possessing
noncommuting internal Lorentz links.

The useful new calculation is that the **existing CAR Dirac symbol**, with
its true adjoint and no fitted price, supplies exactly the required type of
metric-dependent spatial principal coefficient. It also supplies a spin term
which must not be dropped. The original finite stencil has a controlled
smooth-sector defect. This makes a precise next native-clock test available.

## 2. The owned operator and its continuum scaling

Use all16 grades of the original four-mode CAR, with creator order (0,2,3,1),
as in `sources/d0_native_preparation_closure_2026-10-21/inputs/native_input.py`.
Write c_i for creation and a_i=c_i^* for annihilation. In a declared spatial
slice use three of the four directions, leaving the full CAR16 space intact.
On the flat identity-link/constant-coframe chart, the original blank operator
has the spatial part

    A_h = (nu/16) sum_i [c_i(T_i-I)+a_i(T_i^{-1}-I)].

The corresponding normalized readout, not an extra physical gate, is

    D_h = 16 A_h/(nu h).

Its smooth limit is

    D = sum_i(c_i-a_i) partial_i = -i alpha^i partial_i,
    alpha^i=i(c_i-a_i),  {alpha^i,alpha^j}=2 delta^{ij} I.

For a constant nonsingular real spatial frame E, set
alpha^i=sum_a E_a^i alpha^a. The same CAR identity gives
{alpha^i,alpha^j}=2 q^{ij}I, with q^{ij}=sum_a E_a^i E_a^j.
This q is the induced positive spatial symbol, not a derivation of a Lorentzian
time signature or an identification of the physical D0 clock.

## 3. The true adjoint fixes the ordering

For a real scalar profile N and a formally self-adjoint D, consider

    H_N(a)=N D+a[D,N],  a real.

Its formal adjoint is N D+(1-a)[D,N]. Unless N is constant,
self-adjointness on a common compact-support domain forces a=1/2. Thus

    H_N = {N,D}/2
        = -i (N alpha^i partial_i + (1/2)alpha^i partial_i N).

This coefficient is fixed by the existing adjoint convention, not chosen to
fit a gravitational constant. On every finite periodic lattice the same
statement is an exact matrix identity for H_{N,h}={N,D_h}/2.

## 4. Exact constant-frame commutator

Let

    V^j = q^{ij}(N partial_i M-M partial_i N),
    Omega(N,M)=(1/4) sum_ij [alpha^i,alpha^j]
                                      (partial_i N)(partial_j M).

Then on smooth compactly supported full16 spinors,

    [H_N,H_M]
      = -[V^j partial_j + (1/2)partial_j V^j + Omega(N,M)].       (1)

Proof. Write H_N=-i A_N. The second-order derivatives in [A_N,A_M]
cancel. The first-order coefficient is

    sum_i {alpha^i alpha^j-(1/2)[alpha^i,alpha^j]}
             (N partial_i M-M partial_i N)
      = V^j I.

Symmetry of the Hessians of N,M reduces the remaining second-derivative
multiplication terms to (1/2)(N q^{ij}M_ij-M q^{ij}N_ij)
=(1/2)div V. The product of their first-gradient multiplication terms is
Omega. Finally (-i)^2=-1 gives (1).

For the unsymmetrized ordering a, a residual first-order Clifford bivector
has coefficient (1/2-a)[alpha^i,alpha^j](N M_i-M N_i). Hence both the
true-adjoint half ordering and the Clifford anticommutator are essential.

Omega is anti-Hermitian and is nonzero for generic independent gradients.
It is a concrete internal rotation of the spinor frame. It must be transported
by an actual admitted frame operation before the result could be identified
with a pure spatial deformation of a gravity state. Equation (1) alone does
not establish a full representation of all hypersurface-deformation brackets.
In particular, a frozen external Dirac background satisfies it without having
any dynamical metric, conjugate metric momentum, or Einstein equation.

## 5. Finite native stencil: a bound, not an exact lattice symmetry

Taylor expansion of the **actual one-sided creation/annihilation stencil** is

    D_h=D+(h/2) sum_i(c_i+a_i) partial_i^2+O(h^2).

On a compact interior with a slightly larger common collar, and C^4 bounds
on N,M and the test spinor f, expanding the two composed finite differences
gives

    ||[H_{N,h},H_{M,h}]f
        +V^j partial_j f+(1/2)div(V)f+Omega f||_infty
      <= C h ||f||_{C^4}.                                  (2)

C depends on the compact frame and profile derivative bounds, not on h.
This follows either from Taylor's formula at the finitely many double-shift
points or from the C^1 consistency of D_h-D on these smooth data. No
operator-norm convergence on arbitrary grid modes is asserted. The original
stencil has a nonzero O(h) term; replacing it by a centered derivative and
claiming O(h^2) would change the operator.

For one-dimensional grid momentum pi/h, its native symbol is
-2(c+a)/h, whereas the continuum symbol is pi alpha/h. Thus high-frequency
uniform operator convergence is false. This is precisely why a physical
smooth sector and its source norm are still required.

If one already has a passive weighted representation D_h^rho=U_rho^{-1}
D_h U_rho with U_rho multiplication by sqrt(rho)>0, lapse multiplication
commutes with U_rho. The full bracket is then conjugated exactly. This is
only a change of representation with its transported norm and states; it
does not make a physical variation of PF density, its preparation price or
its true open-edge source disappear.

## 6. A decisive wrong-clock control: heat is not a normal Dirac generator

The spectral heat operator is built from D^2. Replacing the candidate normal
generator by L_N={N,D^2}/2 does not obey (1). Already in flat coordinates,
its commutator has a nonzero third-order principal term. Since the scalar
principal symbol of L_N is N q^{ij}xi_i xi_j, the symbol of its commutator
contains

    2 (q^{ij}xi_i xi_j) q^{kl}xi_l
                             (N partial_k M-M partial_k N),      (3)

up to the conventional i/sign of the differential symbol. It has degree
three, while a spatial deformation has degree one. In one dimension,
L_N=-(N partial_x^2+N' partial_x+N''/2), so the coefficient of
partial_x^3 in [L_N,L_M] is exactly 2(N M'-M N').

Thus identifying local heat-time variation with normal spacetime evolution
does not pass this test. This is scoped to the symmetrized heat-generator
candidate; it is not a no-go for the entire Book heat/source programme.

## 7. Exact physical application still required

The next comparison is between **two forward orders** of actually admitted
local clock operations, with the same complete initial state and all outcomes,
not an unadmitted inverse-time loop. Its second difference must transport to
(1), with the actual spatial and internal-frame compensators, uniformly in
the intended smooth sector. The whole apparatus/clock/archive and the moving
coframe dependence of the generators must participate.

To turn this into gravity one must additionally construct the phase space or
presymplectic structure, show that these transformations are generated by
constraints of the same full selected process, establish the remaining
normal/tangential brackets and their Ward identities, and verify the relevant
canonical reconstruction hypotheses. Source and price admission have not
been bypassed; they have a different exact test. A clock commutator on
external spinors is not a canonical Poisson bracket on dynamical geometry.

There is an explicit check of the remaining frame issue. On fixed flat
matrices alpha, let K_X=X^i partial_i+(div X)/2+
(1/8)[alpha^i,alpha^j]partial_i X_j. The principal part of

    [K_X,H_N]-H_{X^i partial_i N}

is i N alpha^i partial_(i X_j) partial_j. For X=x partial_x and
N=1 it equals i alpha^x partial_x, which is nonzero. Thus even the
shift--normal bracket is not the desired covariant relation when the
frame is frozen. The missing dynamical coframe transport is a computable
term, not an implicit assumption that the whole algebra already closes.

This new test may be a productive alternative to another positive scalar
minimum calculation. It supplies no permission to insert Einstein's
Hamiltonian, a new lapse primitive, a discarded spin term, or a fitted action.

## Sources and validation

Native source: the original full128 Fourier input above and the counting /
weighted true-adjoint construction in
`A4D_DENSITY_DRESSED_CAR_EINSTEIN_METRIC_2026_10_18.md`.

Primary external references (background, not proofs of a D0 application):

* C. Teitelboim, *How commutators of constraints reflect the spacetime
  structure*, Annals of Physics 79 (1973), 542--557,
  https://doi.org/10.1016/0003-4916(73)90096-1 .
* S. A. Hojman, K. Kuchar, C. Teitelboim, *Geometrodynamics regained*,
  Annals of Physics 96 (1976), 88--135,
  https://doi.org/10.1016/0003-4916(76)90112-3 .
* V. Bonzom, B. Dittrich, *Dirac's discrete hypersurface deformation
  algebras*, https://arxiv.org/abs/1304.5983 . Their proved discrete
  sectors have explicit restrictions; they do not establish general
  finite-lattice covariance for D0.

The exact symbolic checker uses original CAR16 signs, a full16 polynomial
test, the unmodified one-sided stencil, and hostile controls for omitting
Omega, using ND instead of its true-adjoint half ordering, and identifying
the finite stencil with a uniform continuum operator. It complements the
analytical proof; a polynomial fixture alone is not the general theorem.

`GR_closed=false`.
