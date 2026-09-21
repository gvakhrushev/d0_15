# A-NORM — Finite Gravity Relative Normalization

CONTROL disposition: **ACCEPT AS RESEARCH**  
Primary verdict: **TWO-FINITE-MODULI-LEFT**  
Secondary boundary: **RELATIVE-NORMALIZATION-NOGO-TERMINAL**  
Audited baseline: `8a822febd4ceb15225b8ef390e349bc448794952`

This packet is a durable research summary, not a Lean proof owner. Source memo:
`MEMO_15_ANORM_FINITE_GRAVITY_NORMALIZATION.md`.

## Frozen lane

The audited finite gravity lane combines:

- the accepted Hodge kinetic candidate `Q_H`;
- the unit-weight A1 reduced Hessian (4I);
- the finite two-tick symplectic skeleton;
- an unfixed spatial/two-tick coupling (alpha).

No matter-source selector question is reopened here. A-STRESS remains
`SOURCE-CARRIER-MISSING`; A-SOURCE remains `SELECTOR-NOGO-TERMINAL`.

## Fully parameterised quadratic operator

Write the quadratic action, before quotienting conventions, as

[
S_{m quad}[h]
=
kappa_0left[
rac{kappa_H}{2}langle h,Q_Hhangle
+
2kappa_Alangle h,hangle
ight].
]

The spatial Hessian is therefore

[
Q=kappa_HQ_H+4kappa_AI.
]

The literal A1 number (4) is owned only inside the A1 action normalization. It does not by itself identify the coefficient of the independent Hodge term.

## Genuine redundancy quotient

The finite transfer dynamics depends on the product (alpha Q). The exact reciprocal rescaling

[
Qmapsto sQ,qquad
alphamapsto alpha/s
]

leaves every transfer matrix unchanged.

Overall multiplication of the action and canonical field-coordinate rescalings remove no relative Hodge/contact ratio.

After quotienting:

- overall action scale;
- field/canonical coordinate changes;
- the exact (Q/alpha) reciprocal scaling;
- symplectic conjugacy;
- basis changes inside irreducible sectors;
- branch/sign/time-orientation equivalences;

the minimal continuous invariants are

[
oxed{m^2=rac{4kappa_A}{kappa_H}},
qquad
oxed{gamma=alphakappa_H}.
]

Different pairs are observable from the finite sector trace tuple, so this is an observable two-modulus count, not only parameter bookkeeping.

## Exact shifted Hodge spectrum

On the accepted six-sector common carrier,

[
operatorname{spec}_6(Q)
=
kappa_H
(13+m^2,,
11+m^2,,
9+m^2,,
24+m^2,,
22+m^2,,
20+m^2).
]

If the signed (omega) complement is retained, the additional eigenvalue is

[
kappa_H(33+m^2).
]

## Two-tick stability

For the oriented drift representative, the sector transfer trace is

[
	au_s
=
3-gamma(lambda_s+m^2).
]

Strict ellipticity requires

[
1<gamma(lambda_s+m^2)<5.
]

For the six-sector carrier this is exactly

[
oxed{
m^2>-rac{21}{4},
qquad
rac1{9+m^2}
<
gamma
<
rac5{24+m^2}
}.
]

If the (omega) line is retained, the upper controller becomes (33):

[
oxed{
m^2>-3,
qquad
rac1{9+m^2}
<
gamma
<
rac5{33+m^2}
}.
]

The positive conserved quadratic-energy condition is equivalent to the same strict ellipticity interval; it does not lower the dimension.

Thus stability leaves an open **two-dimensional** region, not a selected point or curve.

## Why the A1 coefficient 4 does not fix (m^2=4)

Current D0 does not own one parent action whose Hessian is literally

[
Q_H+4I
]

with a fixed relative coefficient.

The Hodge owner fixes incidence/adjointness/operator structure. The A1 owner fixes its own compensator Hessian normalization. The C1 isometry transports a chosen Euclidean normalization but cannot select a scalar coefficient:

[
U^*(cQ_H)U=c,U^*Q_HU.
]

Therefore

[
oxed{Q=Q_H+4I}
]

is a conditional modelling specialization, not an owned consequence.

## SceneSpectralAction, (S_{min}), and physical (hbar)

None of the following fixes (m^2) or (gamma):

- `SceneSpectralAction.rho1 = 1`;
- the scene spectral trace/EH-proxy identities;
- `EndogenousActionQuantum.S_min = 1`;
- relative action-scale invariance under an external (hbar) calibration;
- the finite symplectic-capacity mechanism.

The spectral action normalizes a background graph object, not the coefficient of an independent Hodge/A1 field action.

(S_{min}=1) is a lower-bound/global action-unit result and is not a typed decomposition theorem fixing relative coefficients.

Physical (hbar) normalization is explicitly a mechanism-limit/bridge and cannot be imported as a CORE selector.

## Tick/time normalization

The discrete two-tick transfer matrix is itself a dimensionless finite observable.

Changing seconds-per-tick does not change

[
	au_s=3-gamma(lambda_s+m^2).
]

Hence (gamma) is not removable by SI time or global tick-unit relabelling.

Likewise a real Hamiltonian logarithm maps each already-selected transfer matrix to a generator; it does not select one ((m^2,gamma)) from the family.

## C1 and reciprocity do not reduce the moduli

The C1 isometry preserves whatever coefficients are already chosen; it does not fix them.

For any admissible self-adjoint shifted Hodge operator, source-response reciprocity remains symmetric. Therefore reciprocity imposes no extra equation on (m^2) or (gamma).

## Strong negative controls

Two explicit strictly stable models preserve the same literal A1 factor (4) while differing in the observable finite trace tuple.

Model A:

[
kappa_A=1,qquad
kappa_H=1,qquad
alpha=1/10,
]

so

[
(m^2,gamma)=(4,1/10).
]

Model B:

[
kappa_A=1,qquad
kappa_H=1/2,qquad
alpha=1/5,
]

so

[
(m^2,gamma)=(8,1/10).
]

Both satisfy the same audited structural identities and strict elliptic/positive-energy conditions, yet their sector trace tuples differ.

At fixed (m^2=4), varying (gamma) inside the open stability interval gives an independent second witness.

## Terminal boundary

After all genuine finite redundancies and all audited owned constraints:

[
oxed{	ext{two continuous finite normalization moduli remain}.}
]

They are:

[
oxed{m^2}
quad	ext{and}quad
oxed{gamma}.
]

A theorem fixing only the common Hodge/A1 parent action would remove (m^2) but leave (gamma).

A theorem deriving only the discrete shear/generating coefficient would remove (gamma) but leave (m^2).

The smallest internal positive closure would be one typed common finite generating action that, up to one overall action factor, simultaneously derives:

[
operatorname{Hess}_{spatial}=Q_H+4I
]

and the two-tick coupling coefficient with no free (alpha).

Absent that, later continuum/SI/empirical matching is calibration/passport input rather than a retroactive CORE derivation.

## Scope firewall

This result does not:

- upgrade `D0-HODGE-LINKS-001` to CORE;
- fix a TT readout;
- close the matter→scene source carrier;
- derive Einstein dynamics;
- identify physical (hbar);
- make (m^2=4) or a numerical (alpha) owned.
