# MEMO A4D — joint Palatini local uniqueness

**Task:** `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`  
**Execution:** PR #232  
**Status:** IN_PROGRESS / joint tangent-cone and continuum-transfer architecture fixed  
**Baseline:** main at task start `966e280f81d5d3e27d8715dd5fdc98f3c3e9b35d`  
**Primary target:** `NAKED-STAR-JOINT-PALATINI-SMOOTH-EINSTEIN-BRANCH-CLOSED`

## 0. Scope

This task studies the joint Palatini system near the designated smooth LC-like branch,

[
E_K(Q,K)=0,
qquad
E_Q(Q,K)=kappa T.
]

It does **not** ask for a globally single-valued off-shell section (K_*(Q)), and it does not require all connection-stationary sheets to have the same metric response.

Merged #227 proves that the latter all-sheet statement is false: at the fixed flat metric there is an exact curved family with (E_K=0), but its metric partial is nonzero. The present task asks whether the **joint** metric equation removes precisely such source-visible sheets and leaves a locally controlled smooth Palatini branch.

No new action channel, Holst term, (arphi), boundary selector, spectral filter, or torsion constraint is introduced.

## 1. Mandatory input audit

The following owners were read before the present deductions.

- #201: the naked-star flat metric Hessian, after regular connection Schur elimination, has exact small-momentum coefficient
  [
  T_1^{[2]}=rac14E_eta,
  qquad c_{m sp}=0.
  ]
- #208: the metric is the genuine nonlinear quotient coordinate (Q=ThetaetaTheta^T); the polarized connection block is regular at zero phase and singular on UV characters. At the diagonal quarter wave its connection rank is (16) and the genuine metric source raises the augmented rank to (20).
- #216: for fixed smooth realizations the IR parametrix has an (O(h^infty)) connection residual, the normal-center nonlinear terms of total momentum degree (le2) vanish, and the normalized IR response is
  [
  -rac12G+O(h).
  ]
  The old missing theorem was uniform all-sheet normal rescue.
- #223: independently packages the normal-coordinate locality statement and the fixed-realization (O(h)) postquadratic remainder.
- #225: the diagonal frozen connection germ can split under a slow phase detuning; constant-character isolation is therefore not a substitute for a slowly varying coupled theorem.
- #226: raw metric response is uniformly Lipschitz in the dimensionless link logarithm with no negative power of (h); after the single physical (h^{-2}) normalization the polynomial loss is exactly (h^{-2}). Hence an (O(h^infty)) connection error remains (O(h^infty)) in normalized metric response.
- #227: an exact curved connection-stationary family exists on every (L=4m), but its metric partial is nonzero and differs at normalized order one from the identity sheet. This kills all-sheet branch independence, not the joint Palatini branch.
- current #202: the corrected full-transverse audit kills the historical homogeneous parabolic false root and is used only as a lower-wall hostile control.

The registered workers are dependencies, not computations to be duplicated here:

1. `WRK-A4D-JOINT-RESONANCE-LINEAR-KERNEL`;
2. `WRK-A4D-JOINT-DIAGONAL-INVISIBLE-GERM`;
3. `WRK-A4D-JOINT-ONE-D-RESIDUAL-GERMS`;
4. `WRK-A4D-227-TORSION-DIAGNOSTIC`.

## 2. Exact structural identity: the metric Euler equation contains a connection factor

Use local metric and connection coordinates

[
q=Q-eta,qquad a=log K.
]

For identity links, every plaquette curvature is zero for every solder/metric. Therefore

[
S_star(Q,I)=0
]

identically in (Q), and hence

[
oxed{E_Q(Q,I)=0}
]

through the whole near-flat metric chart.

Analyticity then gives

[
oxed{
E_Q(q,a)=H_{QA}a+O(qa,a^2).
}
	ag{2.1}
]

Every Taylor monomial in (E_Q) contains at least one connection amplitude.

The connection equation has the ordinary mixed expansion

[
E_K(q,a)
=
H_{AQ}q+H_{AA}a+O(q^2,qa,a^2).
	ag{2.2}
]

The full linearized joint Palatini operator is therefore the mixed saddle/KKT matrix

[
oxed{
mathcal H_J=
egin{pmatrix}
0&H_{QA}\
H_{AQ}&H_{AA}
end{pmatrix}.
}
	ag{2.3}
]

This full matrix, not merely (ker H_{AA}), is the correct tangent object for arbitrary joint germs.

## 3. Valuation lemma and the precise role of (N_0)

Let a real/complex analytic, subanalytic, or Puiseux joint germ be parametrized by (t), and write

[
a(t)=t^p a_p+cdots,qquad q(t)=t^r q_r+cdots,
]

with (a_p
e0).

From (2.1), if the matter/source term is of valuation strictly greater than (p),

[
oxed{H_{QA}a_p=0.}
	ag{3.1}
]

There are then three distinct cases.

### 3.1 Connection-dominant case (p<r)

Equation (2.2) first sees (H_{AA}a_p), hence

[
H_{AA}a_p=0.
]

Together with (3.1),

[
oxed{
a_pin
N_0:=ker H_{AA}capker H_{QA}.
}
	ag{3.2}
]

This is the load-bearing regime for a nonlinear UV rescue whose connection amplitude is a positive fractional power of a super-algebraically small smooth UV source.

### 3.2 Equal valuation (p=r)

The first coefficients obey

[
H_{QA}a_p=0,
qquad
H_{AQ}q_p+H_{AA}a_p=0.
]

Thus

[
oxed{(q_p,a_p)inkermathcal H_J.}
	ag{3.3}
]

It is not legitimate to replace the full mixed-saddle census by (N_0) in this case.

### 3.3 Metric-dominant case (r<p)

The first connection equation constrains (H_{AQ}q_r) before the first connection coefficient appears. Again, the full KKT tangent cone is required.

**Conclusion.** The worker-owned full mixed saddle census is logically necessary. The residual space (N_0) is exactly the only place where a connection-dominant UV/Puiseux rescue can hide after the metric equation has removed source-visible connection kernel directions.

This valuation split is the precise scoped reading of the registered tangent-cone strategy.

## 3A. Exact abstract decomposition of the mixed saddle kernel

The full J1 census has a useful basis-independent form that does not require
recomputing any orbit.

Write

[
A:=H_{AA}:V	o V,qquad
B:=H_{AQ}:M	o V,qquad
C:=H_{QA}:V	o M,
]

with (M) the metric tangent space and (V) the connection tangent space.
Let

[
N:=ker A,qquad
pi:V	ooperatorname{coker}A.
]

The joint linear equations are

[
Cv=0,qquad Bq+Av=0.
	ag{3A.1}
]

First, every

[
nin N_0:=Ncapker C
]

gives the pure connection joint-null vector ((0,n)).

For a mixed vector, the second equation first requires

[
oxed{pi Bq=0.}
	ag{3A.2}
]

Define

[
M_0:=ker(pi B).
]

For (qin M_0), choose any (v_R(q)) satisfying

[
Av_R(q)=-Bq.
]

Every other solution of the second equation is (v_R(q)+n) with (nin N).
The first equation is solvable precisely when

[
-Cv_R(q)in C(N).
]

Therefore the remaining mixed obstruction is the well-defined quotient map

[
oxed{
Sigma:M_0	o M/C(N),
qquad
Sigma(q)=[Cv_R(q)].
}
	ag{3A.3}
]

Changing (v_R(q)) by an element of (N) changes (Cv_R) by an element of
(C(N)), so the class is independent of the chosen range solve.

Hence

[
oxed{
kermathcal H_J
	ext{ is an extension of }
kerSigma
	ext{ by }N_0,
}
	ag{3A.4}
]

and in particular

[
oxed{
dimkermathcal H_J
=
dim N_0+dimkerSigma.
}
	ag{3A.5}
]

Under the polarized Hessian symmetry used by the worker,
(operatorname{rank}C|_N=operatorname{rank}pi B=d), the Fredholm
incompatibility dimension. Thus (dim N_0=(24-r_H)-d), but (3A.3) shows
exactly why this arithmetic does **not** classify the full saddle kernel:
(kerSigma) contains the genuine metric-only/mixed KKT directions that J1
must identify and quotient correctly.

This decomposition is the parent-level integration rule for the forthcoming
worker table.

## 3B. Radical form of the symmetric mixed saddle

For the polarized Hessian pairing the full joint block has the symmetric form

[
mathcal H_J=
egin{pmatrix}
0&C\
C^{mathsf T}&A
end{pmatrix},
qquad
A=A^{mathsf T},
	ag{3B.1}
]

over the relevant real or (mathbb Q(i)) bilinear carrier. Put

[
W:=ker Csubset V.
]

A joint null vector ((q,v)) satisfies

[
Cv=0,qquad C^{mathsf T}q+Av=0.
	ag{3B.2}
]

The first equation says (vin W). The second is solvable in (q) iff

[
Avinoperatorname{im}C^{mathsf T}=W^perp.
]

Equivalently,

[
w^{mathsf T}Av=0
qquad
	ext{for every }win W.
]

Define the radical of the restricted connection form

[
operatorname{Rad}(A|_W)
:=
{vin W:; w^{mathsf T}Av=0 orall win W}.
	ag{3B.3}
]

Projection ((q,v)mapsto v) therefore gives the exact sequence

[
oxed{
0longrightarrow
ker C^{mathsf T}
longrightarrow
kermathcal H_J
longrightarrow
operatorname{Rad}(A|_W)
longrightarrow0.
}
	ag{3B.4}
]

Hence

[
oxed{
dimkermathcal H_J
=
dimker C^{mathsf T}
+
dimoperatorname{Rad}(A|_W).
}
	ag{3B.5}
]

The pure source-invisible connection space satisfies

[
N_0=ker Acap W
subseteq
operatorname{Rad}(A|_W).
	ag{3B.6}
]

Thus the three pieces of the linear joint problem are intrinsic:

1. (ker C^{mathsf T}): metric-only null directions;
2. (N_0): pure connection source-invisible directions;
3. (operatorname{Rad}(A|_W)/N_0): genuinely mixed saddle directions.

This is equivalent to the quotient-Schur description in §3A but is more useful
for the worker census. The positive 4/1/1 strategy is complete only if every
element of item 3 is absent after quotient or is classified as an already-owned
physical IR/metric-gauge tangent. Any additional physical UV class in item 3
is a new nonlinear blocker.

## 4. #227 hostile control is source-visible and is cut by the joint metric equation

Merged #227 uses

[
B=K_1+K_2+K_3,
]

and the four-phase pattern

[
(U,I,U^{-1},I).
]

Its first connection tangent is therefore the real cosine representative of the diagonal quarter-wave Role-0 kernel vector

[
lambda_0=K_1+K_2+K_3
]

already used in the diagonal resonance analysis.

#227 computes the exact descended metric covector

[
E_Q(x)
=
sigma_{p(x)}c(t)
(0,0,0,0,-1,1,1,-1,1,-1),
]

with

[
c(t)=rac{4t}{4-3t^2}.
]

Since

[
c'(0)=1,
]

the first metric Euler coefficient along the #227 tangent is nonzero. Equivalently,

[
oxed{H_{QA}lambda_0
e0.}
	ag{4.1}
]

Thus the exact curved (E_K=0) family of #227 is **source-visible** and is rejected at first connection valuation by the vacuum joint metric equation. With smooth sourced data, it cannot appear at an amplitude parametrically larger than the corresponding smooth UV metric/matter source.

This is an exact joint-Palatini distinction from the old all-sheet no-go: #227 remains a counterexample to branch-independent (E_K)-elimination, but it is not a joint vacuum branch.

The linear-kernel worker will provide the repository-owned exact basis statement and the full mixed-saddle classification; (4.1) is already independently visible from the exact #227 metric response.

## 4A. Torsion diagnostic from worker PR #233

Worker PR #233 has reached REVIEW with terminal

[
	exttt{J2-227-CURVED-STATIONARY-FAMILY-TORSION-DIAGNOSTIC-CERTIFIED}.
]

At constant standard solder it uses the owned coframe-transport torsion

[
T_{rs}=(L_r-I)e_s-(L_s-I)e_r.
]

For the #227 family all spatial faces have zero torsion and curvature. On
faces ((0,s)), phases (1,3) are torsion-free for every (t) even though
curvature and the metric partial are nonzero, while phases (0,2) have

[
T_{0s}
=
pmleft(
c(t)e_0+rac{2t^2}{4-3t^2}(e_1+e_2+e_3)
ight).
]

Across all phases/faces, torsion vanishes iff (t=0) in the near-identity
chart. Its leading amplitude, curvature, and the metric partial all scale as
(c(t)sim t).

This supports the interpretation that the #227 sheet is not LC-like, but it is
**diagnostic only**. No torsion-free equation and no (T^2) action term are
introduced, and the joint rejection of #227 already follows from (4.1).

## 5. Residual nonlinear sectors

The owned L=4 rank inventory gives the provisional arithmetic

[
dim N_0
=
(24-r_H)-(r_{m aug}-r_H)
=
24-r_{m aug}.
]

Therefore the already-owned rank types suggest

[
(20,24,4)mapsto0,
qquad
(22,24,2)mapsto0,
]

and only

[
oxed{
(22,23,1)mapsto1,quad
(20,23,3)mapsto1,quad
(16,20,4)mapsto4
}
	ag{5.1}
]

retain source-invisible connection kernel dimensions.

Equation (5.1) is a roadmap until the worker constructs (H_{QA}|_{ker H_{AA}}) explicitly and checks the genuine quotient/gauge status. Rank arithmetic alone is not promoted as the J1 theorem.

No nonlinear work is required on the source-visible orbit types if J1 certifies (N_0=0) there.

## 5A. Visible/invisible splitting: only (N_0) is nonlinear

Once J1 supplies the exact restriction

[
C_N:=H_{QA}|_N:N	o M,
qquad N=ker H_{AA},
]

choose any fixed complement

[
N=N_0oplus N_{m vis},
qquad
N_0=ker C_N.
]

Then

[
C_N|_{N_{m vis}}
]

is injective. On one finite orbit representative its smallest nonzero singular
value is positive. On a compact parameter stratum, if the rank is constant,
continuity gives a positive lower bound

[
sigma_{m vis}>0
]

after shrinking to one rank chart. Hence there is a uniformly bounded left
inverse (L_{m vis}) on the source-visible image.

Write the resonant connection amplitude as

[
u=u_0+u_{m vis},
qquad
u_0in N_0,quad
u_{m vis}in N_{m vis}.
]

The reduced metric equation has the form

[
C_Nu_{m vis}
+s_Q
+O(|u|^2+|q||u|)
=0,
	ag{5A.1}
]

because (C_Nu_0=0). Therefore, in any sufficiently small joint tube,

[
|u_{m vis}|
le
Cleft(
|s_Q|+|u_0|^2+|q||u|
ight).
	ag{5A.2}
]

Consequences:

1. a source-visible kernel direction such as #227 is **not** a nonlinear
   Palatini obstruction;
2. for smooth UV forcing (s_Q=O(h^infty)), the visible amplitude is
   (O(h^infty)) once the invisible amplitude is (O(h^infty));
3. no degree/Puiseux analysis is needed on (N_{m vis});
4. all genuine nonlinear UV pressure is concentrated on (N_0), together
   with any additional physical mixed-saddle sector that J1 may expose via
   (kerSigma).

This is the exact reason the registered 4/1/1 workers are sufficient **if and
only if** J1 classifies every extra mixed saddle null as genuine metric
gauge/physical IR data.

At rank-change boundaries the complement must be changed chartwise. A global
uniform claim requires a finite compact stratification on which
(operatorname{rank}C_N) is constant; one cannot take a pseudoinverse through
a rank jump and silently assume its norm stays bounded.

## 6. Joint nonlinear normal theorem needed from the residual sectors

Let (u) denote coordinates on a physical source-invisible normal sector after:

- genuine gauge/flat tangent directions have been separated;
- regular connection variables have been range-eliminated;
- every remaining metric/tangent equation has either been solved or retained.

The correct reduced object is the **joint** map

[
mathcal F_{m red}(u;s)
=
egin{pmatrix}
E_K^{m red}(u;s)\
E_Q^{m red}(u;s)
end{pmatrix}.
	ag{6.1}
]

A connection-only reduced potential is insufficient.

A sufficient local certificate on each residual physical stratum is:

1. at zero source, (u=0) is isolated modulo genuine gauge/flat moduli;
2. there is no zero on one common normal boundary;
3. the normal domain and codomain have matching dimensions after all tangent equations are accounted for;
4. the local Brouwer degree is nonzero, or another exact existence mechanism is supplied;
5. the resulting graph is subanalytic/analytic so a Łojasiewicz/Hölder bound is available.

Then on a compact parameter stratum there are constants

[
C>0,qquadeta>0
]

such that every small root on the selected joint branch obeys

[
oxed{
|u|le C|s|^eta.
}
	ag{6.2}
]

The task does not require the numerical value of (eta). It requires a positive exponent uniform on the finite compact stratification relevant to the smooth branch.

The diagonal four-space and the two one-dimensional sectors are delegated exact gates.

## 7. Smooth UV forcing: why any finite positive exponent is enough

For one fixed (C^infty) realization, #216 owns the UV Fourier-tail estimate in the lattice sum norm:

[
|s_h^{m UV}|=O(h^M)
qquad	ext{for every }M.
	ag{7.1}
]

Allow a fixed polynomial loss (h^{-p}) in the normal estimate,

[
|u_h|
le
C h^{-p}|s_h^{m UV}|^eta,
qquad
eta>0.
	ag{7.2}
]

For a requested (K), choose (M>(K+p)/eta). Then

[
oxed{u_h=O(h^K)}
]

for arbitrary (K), hence

[
oxed{u_h=O(h^infty).}
	ag{7.3}
]

This is why the task needs a finite positive joint visibility/Hölder exponent, not a preferred cubic or quintic exponent.

## 7A. IR/UV source separation in the sourced joint problem

The smooth sourced continuation has two mathematically different residuals and
they must not be conflated.

Let ((Q_h^{m sm},K_h^{m sm})) denote the designated smooth approximate
Palatini sheet. #216 gives

[
E_K(Q_h^{m sm},K_h^{m sm})=O(h^infty)
]

in the smooth/Wiener norms, while #216/#223 give at a normal center

[
h^{-2}E_{star,Q}(Q_h^{m sm},K_h^{m sm})
=
-rac12G+O(h).
]

For a smooth matter realization, the Fourier tail of the metric/matter source
at fixed nonzero lattice phase is also (O(h^infty)). Therefore the
**projection of the joint residual onto the UV/resonant normal blocks** is

[
oxed{s_h^{m UV}=O(h^infty).}
	ag{7A.1}
]

This is the source entering the residual (N_0)/mixed-saddle normal forms.

By contrast, the low-frequency metric Euler residual is the ordinary physical
Einstein/matter truncation error. Its normalized size need only be (O(h));
raw it is correspondingly polynomial in (h). It is handled by the physical
IR metric branch, with metric gauge and propagating/constraint modes retained.
It must **not** be fed into the UV Hölder estimate.

Thus the positive joint theorem factorizes as

[
	ext{physical IR Palatini branch}
quadoplusquad
	ext{UV normal correction}.
]

The present uniqueness task controls the second factor and proves that it does
not change the continuum coefficient. It does not claim global uniqueness or
existence of the low-frequency metric solution for arbitrary matter data.

## 8. Transfer to the metric response

Merged #226 gives a mesh-independent raw Lipschitz bound in the declared finite-stencil chart,

[
|Delta E_Q|
le M(ho)|Delta A|,
	ag{8.1}
]

and the physical normalization adds only the fixed polynomial loss (h^{-2}).

Thus (7.3) implies

[
oxed{
h^{-2}Delta E_Q=O(h^infty).
}
	ag{8.2}
]

Finite connection multivaluedness inside the certified joint normal tube is therefore harmless to the normalized continuum response once the residual sectors have uniform finite Hölder control.

No uniqueness of all (E_K=0) sheets is used.

## 9. Continuum coefficient on the designated joint branch

Merged #216/#223 give, on the smooth approximate/IR branch at a normal-coordinate center,

[
h^{-2}E_{star,Q}
=
-rac12G[g]+O(h)
	ag{9.1}
]

for each fixed admissible smooth realization.

After the joint normal theorem, (8.2) upgrades this from the approximate sheet to the nearby exact **joint-critical** sheet.

In the sourced convention of this task, combining the gravitational response with the matter Euler source gives the target local residual

[
oxed{
E_{star,h}
longrightarrow
-rac12G+kappa T
}
	ag{9.2}
]

with the sign/source placement understood in the repository's declared Palatini convention.

The coefficient (-1/2) is not re-fit here. It is inherited from the exact #201 factor (1/4) and E-NJET (E_eta=-2G).

## 9A. Sufficient sourced joint-branch theorem

A sufficient positive theorem can now be stated without an off-shell
connection selector.

Fix a smooth continuum Palatini/Eintein branch and one admissible fixed smooth
finite realization. Assume:

1. the owned IR construction supplies the smooth approximate connection with
   (E_K=O(h^infty));
2. the physical low-frequency metric/matter variables remain in the declared
   smooth branch neighborhood;
3. J1 shows that every UV mixed-saddle null direction not belonging to genuine
   metric gauge/physical IR data is represented in the finite residual normal
   sectors handed to J2/J3;
4. on those sectors the full joint reduced map has a uniform positive
   Hölder/Łojasiewicz rescue for the UV source (7A.1), with at most a fixed
   polynomial loss in (h).

Then every exact joint-critical sheet inside the selected Palatini normal tube
has UV normal displacement

[
d_{m UV}=O(h^infty).
]

By #226 its normalized metric partial differs from the smooth approximate
sheet by (O(h^infty)). Consequently

[
h^{-2}E_{star,Q}
=
-rac12G+O(h)+O(h^infty)
]

on that exact joint-critical sheet.

For two fixed smooth realizations of the same local metric 2-jet, the same
argument applies separately; both limits equal the same geometric
(-rac12G(J)). Thus extension independence on the designated **joint**
branch is recovered without the false all-(E_K)-sheet statement killed by
#227.

The logical stop condition is J1 item 3: if the worker finds an additional
physical UV mixed-saddle null sector outside the delegated 4/1/1 normals, that
sector becomes an explicit blocker and the positive terminal cannot be
declared merely from the existing nonlinear workers.

## 10. What would close the positive terminal

The positive terminal

[
oxed{	exttt{NAKED-STAR-JOINT-PALATINI-SMOOTH-EINSTEIN-BRANCH-CLOSED}}
]

requires all of the following.

### J1

Worker-owned exact full mixed-saddle census, including:

- (ker H_{AA});
- (H_{QA}|_{ker H_{AA}});
- exact (N_0);
- full (kermathcal H_J);
- gauge/flat/physical/mixed classification;
- exact source-visible identification of the #227 tangent.

### J2/J3

For precisely the residual physical sectors with (N_0
e0):

- diagonal four-dimensional joint germ;
- both one-dimensional joint germs;
- exact local isolation or an exact joint-vacuum branch/no-go.

### J4

Torsion is diagnostic only. It may distinguish the designated LC-like branch from #227 but is not an added equation.

### J5/J6

A compact/uniform sourced continuation of the isolated residual germs, sufficient for (7.2), followed by the already-owned #226 response transfer and #216/#223 IR coefficient.

## 11. Exact negative terminal

Any certified non-gauge/non-flat germ

[
(Q(t),K(t))	o(eta,I),
qquad
E_K=0,
qquad
E_Q=0,
]

inside one of the source-invisible physical sectors is a terminal obstruction to the requested local joint uniqueness:

[
oxed{	exttt{NAKED-STAR-JOINT-PALATINI-LOCAL-UNIQUENESS-NOGO}.}
]

A connection-stationary branch with (E_Q
e0), such as #227, is not this no-go.

## 12. Current boundary

No worker result is silently assumed. At this checkpoint:

- the exact #227 all-sheet obstruction is cut by the joint metric equation at linear order;
- the parent theorem reduces nonlinear UV pressure to worker-certified source-invisible sectors, subject to the full mixed-saddle valuation cases above;
- if those sectors admit uniform finite Hölder continuation, smooth UV amplitudes are (O(h^infty));
- #226 then makes their normalized metric-response effect (O(h^infty));
- #216/#223 already supply the surviving (-rac12G) coefficient and (O(h)) IR remainder.

The smallest unresolved scientific input is the exact J1 mixed-saddle/source-invisible census, followed by the delegated nonlinear joint germs on its nonzero residual sectors.
