# MEMO A4D — curved stationary sector after affine completion

**Task:** `EXP-A4D-CURVED-STATIONARY-SECTOR-AFTER-AFFINE-COMPLETION`  
**Execution:** PR #187  
**Status:** IN_PROGRESS / interim exact classification  
**Baseline:** `297067714e7c1a246b06ed981578105c58d9f3db`


## 0A. RESUME CHECKPOINT — durable state

**Checkpoint status:** all items below are already persisted in this PR and are
the required restart point for any cold-start continuation.

### EXACT/CERTIFIED

- Local curvature-to-solder-Euler map:
  [
  operatorname{rank}mathcal E_v=16,qquad dimkermathcal E_v=20.
  ]
- In the declared pair-symmetric + first-Bianchi algebraic curvature subclass:
  [
  dimmathcal C_{m alg}=20,qquad
  operatorname{rank}mathcal E_v=10,qquad
  dimkermathcal E_v=10.
  ]
  Therefore (E_v=0) does not imply (C=0).
- Exact #178 two-link curved witness:
  [
  operatorname{rank}H_v=28,
  ]
  and every fixed-link solder-stationary representative is degenerate at the
  origin.
- Exact one-boost curved control:
  [
  operatorname{rank}H_v=16,qquad dimker H_v=240,
  ]
  with an explicit all-site nondegenerate (E_v=0) solder witness.
- Exact connection-Euler operator on free bivector data for the one-boost
  background:
  [
  operatorname{rank}mathcal E_L^{(B)}=282,qquad
  dimkermathcal E_L^{(B)}=294.
  ]
  Modular reproduction was performed over multiple primes.
- Eliminating all non-origin bivector variables leaves exactly four independent
  origin constraints; these are compatible with an invertible local solder.
- For all three accepted Lorentz-null checkerboard sectors, the two-dimensional
  physical quotient-null plane is obstructed at second order.  For an exact
  basis ((u,v)) and real (z_1=a,u+b,v),
  [
  T(z_1,z_1,w_0)
  =
  -rac{32}{3}(a^2+b^2),
  ]
  so no nonzero real physical null direction continues to a smooth stationary
  branch from the canonical flat solder.

Supporting certificates:

- `02_REGISTRY/research/certificates/a4d_curved_stationary_sector_check.py`
- `02_REGISTRY/research/certificates/a4d_checkerboard_nonlinear_obstruction_check.py`
- `02_REGISTRY/research/certificates/a4d_checkerboard_nonlinear_lift_obstruction_check.py`

### NUMERICAL/EXPLORATORY — NOT A THEOREM

A nonlinear solve inside the exact one-boost solder kernel can drive the
connection-Euler residual very small, but observed solutions collapse toward
degenerate solder.  This remains evidence only.

### CURRENT STRONGEST STABLE STATEMENT

[
oxed{
	exttt{SOLDER-EULER-DOES-NOT-FORCE-FLATNESS-CONNECTION-COMPATIBILITY-IS-FIRST-BLOCKER}
}
]

together with the stronger local-flat result

[
oxed{
	exttt{CANONICAL-FLAT-CHECKERBOARD-QUOTIENT-NULLS-NONLINEARLY-OBSTRUCTED}.
}
]

### SINGLE NEXT BLOCKER

Decide the **joint** nondegenerate curved system
[
E_v=0,qquad E_L=0
]
(and, after independent reproduction, the minimal affine-residual equation)
without relying on numerical collapse.  The next accepted advance must be one
of:

1. an exact nondegenerate curved joint Euler witness;
2. an exact periodic/global elimination obstruction;
3. a certified extension of the nonlinear obstruction to the independently
   reproduced minimal full-affine completed family.

Do not restart from gauge-law speculation; resume from this joint-Euler blocker.

---

## 0. Research question

The affine-gauge discussion is not finished by constructing a covariant carrier.
A completed action must also possess a nontrivial stationary sector.

The current exact question is therefore:

[
E_v=0,qquad E_L=0,
]

with nondegenerate solder at every site and with nonzero finite curvature.

This memo deliberately separates:

1. the solder Euler equation;
2. the Lorentz-link Euler equation;
3. affine translation/gauge completion;
4. later translation-curvature residual terms.

No Einstein, GR, diffeomorphism, wave, time or continuum interpretation is made.

---

## 1. Local solder Euler does not force flatness

At one canonical nondegenerate four-Role cell write the six based curvature
bivectors as a 36-dimensional exact rational variable

[
Cin Lambda^2_{m base}otimesLambda^2_{m int}.
]

Linearizing only the solder Euler equation at the canonical solder gives

[
mathcal E_v:Clongrightarrow mathbb Q^{16}.
]

Exact row reduction gives

[
oxed{operatorname{rank}mathcal E_v=16},
qquad
oxed{dimkermathcal E_v=20}.
]

Therefore the pointwise solder equation does not imply (C=0).

A stronger control imposes the usual algebraic pair symmetry on the
(6	imes6) curvature matrix and one first-Bianchi scalar relation.  The
declared algebraic-curvature subspace then has dimension 20.  On that subspace

[
oxed{operatorname{rank}mathcal E_v=10},
qquad
oxed{dimkermathcal E_v=10}.
]

This is only an algebraic finite-cell statement.  The ten-dimensional kernel
is not identified with continuum Weyl curvature here because the exact D0
finite-holonomy realization and conventions must be established separately.

**Immediate consequence:** any claim
[
E_v=0Rightarrow C=0
]
is already false at the local algebraic level.

---

## 2. The accepted two-link curved witness has no nondegenerate stationary solder

Take the exact period-two witness used in the full-affine boundary packet:

- one (A)-link carries the rational (A/B) boost;
- one (B)-link at the same origin carries the (B/C) quarter-turn.

For fixed links, the star action is quadratic in the 256 solder components.
Its exact solder Hessian has

[
operatorname{rank}H_v=28,
qquad
dimker H_v=228.
]

The large nullity is misleading.

Exact nullspace projection at the origin shows that every vector in
(ker H_v) has

[
(v_A)^D=(v_B)^D=(v_C)^D=(v_D)^D=0
]

there.  Hence the entire fourth internal row of the local solder matrix
vanishes and

[
oxed{detTheta_{m origin}=0}
]

for every solder-stationary representative on this fixed curved background.

Therefore:

[
oxed{
	exttt{TWO-LINK-178-WITNESS-HAS-NO-NONDEGENERATE-SOLDER-STATIONARY-REPRESENTATIVE}
}
]

with scope restricted to this exact fixed-link witness.

This does **not** prove that nonzero curvature is globally incompatible with a
nondegenerate stationary solder.

---

## 3. A one-boost curved background gives the opposite control

Now keep only one rational boost link nontrivial on the same periodic (L=2)
carrier.

There are six nonzero curved cells.  The exact solder Hessian has

[
oxed{operatorname{rank}H_v=16},
qquad
oxed{dimker H_v=240}.
]

A deterministic exact-rational search inside this kernel finds a vector whose
16 site solder determinants are all nonzero.

Therefore:

[
oxed{
C
eq0,quad E_v=0,quad detTheta_x
eq0 orall x
}
]

is realized exactly for this fixed-link curved background.

This kills a stronger possible no-go:

[
oxed{
	ext{the solder Euler equation alone does not force either flatness or
degeneracy on the finite }L=2	ext{ torus.}
}
]

The connection equation is the first remaining dynamical filter.

---

## 4. Exact connection-Euler operator on free bivector data

For fixed one-boost links, regard the 96 complementary solder bivectors as
independent data,

[
Binmathbb Q^{96	imes6}congmathbb Q^{576}.
]

The six Lorentz tangents on each of 64 links give 384 link-Euler components,

[
mathcal E_L^{(B)}:mathbb Q^{576}	omathbb Q^{384}.
]

The operator is sparse: every equation touches at most the incident
plaquettes.  Exact rational sparse elimination gives

[
oxed{operatorname{rank}mathcal E_L^{(B)}=282},
qquad
oxed{dimkermathcal E_L^{(B)}=294}.
]

The rank 282 is independently reproduced modulo three primes
(1000003,1000033,1000037).

Thus the connection equation also does not force all bivectors to vanish when
they are treated as free linear data.

The actual problem is the nonlinear intersection

[
B=vwedge v,
qquad
vinker H_v,
qquad
mathcal E_L^{(B)}B=0,
]

plus nondegeneracy at every site.

---

## 5. Eliminating all other sites leaves only four origin constraints

Eliminate every bivector variable except the 36 origin-cell components from the
one-boost connection-Euler system.

The full rank is 282.  Removing the 36 origin columns lowers the rank only to
278.  Therefore exactly four independent linear constraints survive on origin
bivector data.

They are

[
(B_{01})_{03}-(B_{02})_{03}+(B_{03})_{03}=0,
]
[
(B_{01})_{02}-(B_{02})_{02}+(B_{03})_{02}=0,
]
[
(B_{01})_{13}-(B_{02})_{13}+(B_{03})_{13}=0,
]
[
(B_{01})_{12}-(B_{02})_{12}+(B_{03})_{12}=0.
]

Because the complementary solder bivectors obey

[
B_{01}=v_2wedge v_3,qquad
B_{02}=v_1wedge v_3,qquad
B_{03}=v_1wedge v_2,
]

the combination is

[
B_{01}-B_{02}+B_{03}
=
(v_2-v_1)wedge(v_3-v_1).
]

Only its (02,03,12,13) components are killed.

These four constraints are compatible with an invertible local solder.  For
example one may choose three legs whose differences span an allowed simple
two-plane and a fourth leg outside their span.  Hence the connection equation
does not produce a pointwise nondegeneracy no-go at the origin.

If a no-go exists, it is therefore a **global periodic compatibility
obstruction**, not a pointwise Cartan-algebra obstruction.

---

## 6. Exploratory nonlinear solve — not a theorem

Parameterizing the full exact 240-dimensional one-boost solder kernel and
numerically minimizing all 384 connection-Euler equations finds residuals below
(10^{-12}).

However every tested solution approaches the degenerate boundary: typical
minimum site determinant falls below (10^{-40}), including runs in which one
linear solder component at every site is fixed to one.

This is evidence for a possible global compatibility obstruction, but it is
**not** promoted to a theorem.  A nonlinear optimizer may select a singular
component even when a nondegenerate component exists.

The next exact task is to replace this observation by one of:

1. an exact nondegenerate joint (E_v=E_L=0) witness;
2. an exact elimination/Pluecker obstruction on the periodic carrier;
3. a perturbative nonlinear obstruction/survival theorem around one of the
   accepted Lorentz-null checkerboard Hessian sectors.

---

## 7. Relation to the active affine-completion PRs

Active PRs #184, #185 and #186 are intentionally not treated as repository
truth in this branch.

Their current claimed direction is useful as a hypothesis:

- relative solder can restore affine covariance but may erase nongauge
  edge-diagonal data;
- two based affine holonomies may provide a polynomial translational residual
  capable of detecting some of that lost sector.

The correct later dynamical test is therefore not merely (S^{rel}).  After
independent reproduction of the required affine residual, test the smallest
completed family schematically

[
S_{m trial}=S_{m rel}+mu S_R
]

and ask whether the joint Euler equations:

- select (mu);
- leave a modulus;
- or admit no nondegenerate curved stationary point in the declared class.

This memo has **not** reached that gate yet.

---

## 8. Current strongest stable statement

The correct interim terminal is

[
oxed{
	exttt{SOLDER-EULER-DOES-NOT-FORCE-FLATNESS-CONNECTION-COMPATIBILITY-IS-FIRST-BLOCKER}
}
]

with two exact finite controls:

- the #178 two-link witness has no nondegenerate solder-stationary
  representative;
- a one-boost curved background does admit all-site nondegenerate
  solder-stationary representatives.

Therefore the curved-vacuum question is neither trivially positive nor
trivially negative.  It is a joint finite-holonomy / connection-compatibility
problem.

No claim/release/BOOK or Lean promotion follows.


---

## 9. Nonlinear fate of the three Lorentz-null checkerboard sectors

The accepted flat quadratic packet has exactly three nonzero characters with

[
kappa_eta^2=0:
qquad
(-1,-1,+1,+1),;
(-1,+1,-1,+1),;
(-1,+1,+1,-1).
]

At each one, after quotienting the ten flat gauge directions, the Hessian has a
two-dimensional extra physical null plane.

A Hessian-null direction is not yet a nonlinear branch.  Let

[
z(t)=t z_1+t^2z_2+cdots
]

be a hypothetical stationary branch from the canonical flat solder.

At second order the Euler equation requires the quadratic source generated by
(z_1) to lie in the image of the flat Hessian.  Since the Hessian is
symmetric, a necessary Lyapunov--Schmidt condition is

[
T(z_1,z_1,w)=0
]

for every (winker H_0), where (T) is the cubic action tensor and (H_0)
is the zero-momentum Hessian.

Choose the exact zero-momentum constant-solder kernel vector

[
w_0:qquad delta v_A^A=1,
]

with all other reduced amplitudes zero.

For each of the three Lorentz-null sectors, choose any exact basis
((u,v)) of the two-dimensional quotient-null complement obtained by extending
the ten gauge vectors inside the 12-dimensional Hessian kernel.

The full 16-site cubic coefficient, evaluated with exact exponential link jets,
gives in all three sectors

[
T(u,u,w_0)=-rac{32}{3},
]

[
T(v,v,w_0)=-rac{32}{3},
]

and

[
T(u,v,w_0)=0.
]

Hence for every physical first-order null combination

[
z_1=a,u+b,v
]

the obstruction form is

[
oxed{
T(z_1,z_1,w_0)
=
-rac{32}{3}(a^2+b^2).
}
]

Over the real field this vanishes iff

[
a=b=0.
]

Therefore:

[
oxed{
	exttt{CANONICAL-FLAT-CHECKERBOARD-QUOTIENT-NULLS-NONLINEARLY-OBSTRUCTED}
}
]

for all six extra quotient-null directions carried by the three period-two
Lorentz-null sectors.

Equivalently, none of those infinitesimal rank-drop directions can be the
tangent of a smooth stationary branch emanating from the canonical flat solder.

This sharpens the interpretation of the flat rank drop:

- the rank drop is exact and real;
- it is not merely gauge;
- but it is also not, by itself, evidence for a nonlinear curved vacuum branch.

A direct finite hostile control illustrates the distinction.  Following one
physical null direction by an exact rational Cayley link path at
(t=1/2) keeps the solder nondegenerate,

[
detTheta_x=rac{15}{16}
]

at every site and produces nonzero curvature on 64 cells.  Nevertheless the
transverse solder Euler vector has 64 nonzero components.  One representative
component begins as

[
(E_v)_0=-2t^2+O(t^4).
]

The action restricted to the one-dimensional path can vanish while the full
transverse Euler vector does not.  Therefore an action-value test alone is not
a stationarity test.

### Scope of this obstruction

The result is local in configuration space around the **canonical** flat
solder.  It does not exclude:

1. a curved stationary point disconnected from the flat branch;
2. a nonlinear branch emanating from a different constant nondegenerate flat
   solder representative;
3. a branch after adding independently justified full-affine completion terms;
4. larger-period or non-checkerboard finite sectors.

The next exact target is therefore the dependence of the obstruction form on
the constant-solder flat moduli and, after independent reproduction of the
translation-curvature carrier, the corresponding obstruction for

[
S_{m rel}+mu S_R.
]

Exact checker:

`02_REGISTRY/research/certificates/a4d_checkerboard_nonlinear_obstruction_check.py`.
