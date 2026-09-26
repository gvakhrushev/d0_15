# MEMO A4D — resolved curved stationary closure

**Task:** `EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE`  
**Execution:** PR #202  
**Status:** IN_PROGRESS / durable checkpoint  
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`

## 0A. RESUME CHECKPOINT

### EXACT/DERIVED — F4 reduces to the star physical critical set on generic quotient-complete strata

PR #201 has now certified two facts for the selected family

[
S_{\rm trial}(\Theta,b,L)
=
\alpha S_{\widehat\star}(\Theta-b^\flat,L)
+
\beta Q_L(b).
]

On every declared generic curved stratum where the landed joint-residual map is
quotient-complete,

[
\ker J_L=\operatorname{im}D_L.
]

At a full stationary point the \(\Theta\)-equation first imposes

[
E_{\widehat\Theta}S_\star=0.
]

The \(b\)-equation then reduces to \(E_bQ_L=0\), hence

[
b\in\ker J_L=\operatorname{im}D_L,
qquad
J_Lb=0.
]

Therefore the residual energy and its first \(L\)-variation vanish on shell.
Consequently the quotient-completion channel cannot be tuned to cancel a failed
star coframe equation on these strata.

The lower-wall search is therefore reduced to

[
\boxed{
C(L)\neq0,quad
\det\widehat\Theta_x\neq0\ \forall x,quad
E_{\widehat\Theta}S_\star=0,quad
E_LS_\star=0.
}
]

This is the actual F4 target.

### EXACT/CERTIFIED inherited hostile controls

The landed stationary-sector packet already supplies:

1. a one-boost curved control with nondegenerate all-site solder satisfying the
   star solder Euler equation alone, so solder stationarity does **not** force
   flatness or degeneracy;
2. an exact connection-Euler operator of rank 282 on free bivector data, showing
   that joint stationarity is the first real nonlinear compatibility gate;
3. the canonical flat checkerboard quotient-null directions are obstructed at
   cubic order:
   [
   T(z,z,w_0)=-\frac{32}{3}(a^2+b^2),
   ]
   so they do not seed a nearby curved stationary branch from canonical flat
   solder;
4. the historical sparse two-link curved witness has no nondegenerate solder
   stationary representative.

Thus neither “all curved sectors die” nor “a small flat-null branch survives” is
currently supported.

## 1. Search strategy now fixed

The next search must be richer than the killed sparse witnesses.  Use at least
a multi-link / multi-plaquette curved ansatz with:

- exact proper-Lorentz links;
- all-site nondegenerate solder;
- enough link freedom to satisfy both solder and connection Euler equations;
- explicit nonzero curvature certificate;
- quotient/gauge fixing only after the equations are assembled.

Numerical root-finding is allowed only as a scout.  Any survivor must be
rationally reconstructed or converted into an exact algebraic certificate.

## 2. Terminal alternatives

A. Construct one exact nondegenerate curved critical point:
[
\boxed{\texttt{RESOLVED-AFFINE-NONDEGENERATE-CURVED-STATIONARY-WITNESS}}
]

B. Prove an exact no-go for a precisely declared ansatz class.

C. If only numerical roots appear, record them as NUMERICAL/EXPLORATORY and
identify the smallest exact polynomial subsystem needed for certification.

No GR/Einstein conclusion is allowed from F5 alone; F4 remains independently
load-bearing.


## 3. NUMERICAL/EXPLORATORY — broad homogeneous four-link roots survive the exact word controls

The exact homogeneous control certificate in this PR kills five explicit
rational word backgrounds, including the two generic quotient-complete
backgrounds from the joint-holonomy packet. That is a useful negative control,
but it does not exhaust the homogeneous four-link sector.

A separate broad root search was therefore run on the full homogeneous
four-link star action.

### 3.1 Exponential-Lorentz / SL(4) solder scout

Variables:

- four independent proper-Lorentz links, six Lie-algebra parameters each;
- a full homogeneous invertible solder;
- determinant fixed to (-1) only to prevent the optimizer from collapsing
  the homogeneous degree-two action by the trivial scale limit;
- the missing scale Euler equation imposed independently as (S=0).

Across 20 deterministic random starts, many nonflat roots were found. After
reconstructing the raw solder matrix, each candidate was checked against the
**unconstrained 40-component Euler gradient**.

Representative candidate:

[
|mathrm{EL}_{m raw}|_2=8.22	imes10^{-14},
quad
|mathrm{EL}_Theta|_2=4.15	imes10^{-14},
quad
|mathrm{EL}_L|_2=7.10	imes10^{-14},
]
[
detTheta=-1,
quad
|C|_{m scout}=0.9732,
quad
sigma_{min}(Theta)=0.2423,
quad
kappa(Theta)=17.9.
]

Thus the earlier numerical collapse to degenerate solder is not stable under a
wider homogeneous ansatz once scale collapse is excluded.

### 3.2 Rational Cayley/LDU scout

To remove dependence on exponential coordinates, the search was repeated with
the rational charts

[
L(A)=(I+A/2)(I-A/2)^{-1},
qquad Ainmathfrak{so}(1,3),
]

and a determinant-one rational (LDU) solder chart multiplied by the Lorentz
signature matrix. The stationary equations are therefore rational functions of
39 chart variables.

Again many nonflat roots were found. Representative candidate:

[
|mathrm{EL}|_2=1.21	imes10^{-13},
qquad
detTheta=-1,
]
[
|C|_{m scout}=1.3900123322164437,
qquad
sigma_{min}(Theta)=0.3797133,
qquad
kappa(Theta)=6.33.
]

The fixed-determinant homogeneous Hessian at this candidate has numerical

[
operatorname{rank}H=20,
qquad
operatorname{nullity}H=19
]

at tolerance (10^{-8}). This is evidence for a positive-dimensional
stationary manifold, not an isolated optimizer accident, but it is not yet an
exact theorem.

The persisted candidate is:

`02_REGISTRY/research/certificates/a4d_curved_stationary_cayley_scout_candidate.json`.

### 3.3 Current interpretation

The exact negative word controls and the broad numerical positive scout are
compatible:

- several simple rational word backgrounds provably have no nondegenerate full
  stationary point;
- the unrestricted homogeneous four-link sector appears to contain
  nondegenerate curved critical points outside those word families.

Therefore the next exact problem is sharply defined: extract one exact
rational/algebraic point from the apparent 19-dimensional Cayley/LDU stationary
manifold.

### SINGLE NEXT BLOCKER

Use the observed rank-20 transverse system:

1. choose 19 chart coordinates as free parameters;
2. fix them to simple rationals near the numerical candidate;
3. solve the remaining transverse equations exactly or by high-precision
   algebraic reconstruction;
4. certify (C
eq0), (detTheta
eq0), (E_Theta=0), (E_L=0).

Do not promote the floating-point roots before this exactification.
