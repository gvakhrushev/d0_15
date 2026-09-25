# MEMO A4D — Oriented spatial Role selector

**Task:** `EXP-A4D-ORIENTED-SPATIAL-ROLE-SELECTOR`  
**Execution:** PR #172  
**Status:** terminal research classification  
**Verdict:** `ORIENTED-SPATIAL-SELECTOR-STAR`

## 1. Question closed

Current main had already closed the typing and proper-Lorentz Hom-space calculation:
[
operatorname{End}_{SO^+(1,3)}(Lambda^2V)
=
mathbb R Ioplusmathbb Rstar .
]

It left exactly one downstream question: transform the **complete**
finite density under simultaneous odd spatial Role/site relabeling, including
the base complement-orientation sign and the internal star pseudo-sign.

That calculation is now closed exactly.

Let
[
G_A={sigmainoperatorname{Perm}(Role):sigma(A)=A}cong S_3
]
be the already-owned spatial Role stabilizer.  For an oriented two-face
(Ssubset{A,B,C,D}), let (S^c) be its ordered complement and write

[
epsilon(S)=operatorname{complementOrientation}(S).
]

Let (chi_S(sigma)in{pm1}) be the sign needed to sort the transported
oriented face blade, and similarly (chi_{S^c}(sigma)).

Direct enumeration of all
[
6 	ext{elements of }G_A
	imes
6 	ext{two-faces}
=
36
]
cases gives the exact finite identity

[
oxed{
epsilon(sigma S)
=
operatorname{sgn}(sigma),
epsilon(S),
chi_S(sigma),
chi_{S^c}(sigma).
}
	ag{1.1}
]

No continuum epsilon tensor is used; this is the literal Role-order/complement
sign convention.

## 2. Consequence for the two candidate densities

Use the already-typed proper-Lorentz candidates

[
mathcal L_I(S)
=
epsilon(S),
G_2(B_{S^c},C_S),
	ag{2.1}
]

[
mathcal L_star(S)
=
epsilon(S),
G_2(B_{S^c},star C_S).
	ag{2.2}
]

Under (sigmain G_A), the oriented face and complement blades contribute

[
chi_S(sigma)chi_{S^c}(sigma).
]

For the identity channel, the complete density ratio is therefore

[
rac{mathcal L_I(sigma S)}{mathcal L_I(S)}
=
epsilon(sigma S),
chi_S(sigma)chi_{S^c}(sigma),
epsilon(S)
=
operatorname{sgn}(sigma).
	ag{2.3}
]

Hence every odd spatial transposition flips (mathcal L_I).

For the star channel, the owned middle-degree pseudoequivariance supplies one
additional factor (operatorname{sgn}(sigma)):

[
star,ho_2(sigma)
=
operatorname{sgn}(sigma),
ho_2(sigma)star .
	ag{2.4}
]

Therefore

[
rac{mathcal L_star(sigma S)}{mathcal L_star(S)}
=
operatorname{sgn}(sigma)^2
=
1.
	ag{2.5}
]

Thus the complete simultaneous Role/site transformation theorem is

[
oxed{
mathcal L_Imapsto operatorname{sgn}(sigma)mathcal L_I,
qquad
mathcal L_starmapsto mathcal L_star .
}
	ag{2.6}
]

Since (G_A) contains odd spatial transpositions, scalar action-density
naturality leaves exactly

[
oxed{mathbb Rstar}.
	ag{2.7}
]

## 3. Why this does not contradict the fixed-base reflection calculation

The same permutation matrix (Bleftrightarrow C) can be used in two
different tests.

### Fixed-base internal improper Lorentz reflection

The base face is held fixed.  The condition is the ordinary commutant law

[
Kho_2(sigma)=ho_2(sigma)K.
]

This retains (I) and removes (star).

### Simultaneous spatial Role/site relabeling

The base face, complementary base directions, solder legs and internal fibre
all move together.  The complement/top-cell orientation contributes the extra
sign in (1.1).  The complete scalar-density condition is therefore the
sign-twisted law

[
Kho_2(sigma)
=
operatorname{sgn}(sigma)ho_2(sigma)K.
]

This retains (star) and removes (I).

These operations are not identified.  The second is exactly the downstream
calculation that the current main memo had left open.

## 4. Exact certificate

The checker

`02_REGISTRY/research/certificates/a4d_oriented_spatial_role_selector_check.py`

exhausts every spatial permutation fixing (A) and every two-face.

For each of the 36 cases it verifies:

[
epsilon(sigma S)
=
operatorname{sgn}(sigma)epsilon(S)
chi_S(sigma)chi_{S^c}(sigma),
]

[
mathcal L_I(sigma S)/mathcal L_I(S)
=
operatorname{sgn}(sigma),
]

[
mathcal L_star(sigma S)/mathcal L_star(S)
=
1.
]

Hostile controls explicitly require all three odd spatial permutations to reject
the identity channel and preserve the star channel.

The calculation uses exact integer signs only.

## 5. Theorem-ready statements

1. `SpatialRoleStabilizer` contains exactly the six permutations of
   (B,C,D) fixing (A).

2. For every (sigmain G_A) and every degree-two face (S),
   equation (1.1) holds.

3. The full identity-channel density is (G_A)-pseudoinvariant with character
   (operatorname{sgn}).

4. The full star-channel density is (G_A)-invariant.

5. Every odd spatial transposition excludes the identity channel from a scalar
   action density.

6. Even spatial permutations alone do not separate (I) from (star).

7. Proper Lorentz covariance plus complete spatial Role/site scalar-density
   naturality has one-dimensional insertion space (mathbb Rstar).

8. Fixed-base improper Lorentz covariance and simultaneous spatial Role/site
   covariance are inequivalent selector conditions and select different lines.

9. The result uses only owned complement orientation and star
   pseudoequivariance; no new orientation primitive is introduced.

10. Flat-curvature compatibility from the parent memo is unchanged, since the
    selector acts only on the already-classified insertion channel.

## 6. Disposition

The open selector named in current main,

`ACTION-LEVEL-DIAGONAL-ROLE-ORIENTATION-SELECTOR-UNPROVED`,

is closed by the complete finite transformation calculation above.

The proper-Lorentz two-dimensional classification remains a correct
intermediate statement, but after imposing the already-owned simultaneous
spatial Role/site scalar-density naturality the terminal insertion space is

[
oxed{mathbb Rstar}.
]

Hence the downstream verdict is

[
oxed{	exttt{ORIENTED-SPATIAL-SELECTOR-STAR}.}
]

Equivalently, combining this packet with the parent Role-bivector memo upgrades
the finite insertion to **unique up to overall scale**.

No claim is made here about that overall normalization, a continuum Einstein
equation, time, or any quadratic-curvature action.


## 7. Validation boundary

The exact certificate is finite and exhaustive for the selector question: it checks all
36 pairs of a spatial A-stabilizer permutation and a degree-two Role face. Repository
CI/guard status is a separate execution check and does not enter the mathematical
sign identity.
