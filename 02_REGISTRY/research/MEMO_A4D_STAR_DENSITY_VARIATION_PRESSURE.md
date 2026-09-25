# MEMO A4D — star-density variation pressure

**Task:** `CTRL-A4D-STAR-DENSITY-VARIATION-PRESSURE`  
**Execution:** PR #175  
**Status:** terminal CONTROL research classification  
**Starting point:** accepted canonical spatial-Role-natural insertion with \(d_A=1\)

## 0. Verdict

The selected canonical \(\star\)-density survives the first variational
pressure.  It does **not** collapse to a boundary/topological zero, and it does
not disappear under the owned flat linearized gauge quotient.

The exact status is

\[
\boxed{d_A=1},
\qquad
\boxed{d_E=1},
\qquad
\boxed{d_{P,\mathrm{flat},L=2}=1}.
\]

The last statement is deliberately scoped: it is the physical-operator family
after exact quadratic connection elimination and the owned **flat linearized**
local-frame / forward-coframe quotient on the period-two four-Role torus.

The full nonlinear finite \(d_P\) is **not yet owned**, for one prior typed
reason:

\[
\boxed{
\texttt{FULL-AFFINE-SOLDER-GAUGE-QUOTIENT-MISSING}.
}
\]

The repository already proves that `rawFullSolderFrameAction` supplies only
the linear right-frame action and misses the additive node-translation term
required for a full affine solder-point law
(`A4DAffineOriginSolderBoundary.rawFullSolderFrameAction_misses_affine_translation_term`).
Therefore the exact flat forward-coframe null directions found below cannot yet
be promoted to a global nonlinear physical quotient without adding a new
affine solder/gauge owner.

A second important pressure result is negative but not an additional missing
principle:

> the actual finite connection Euler equation of the selected density is **not
> identically the naive forward torsion equation** at finite \(L=2\).

Thus this task does not write
\(D(e\wedge e)=0\Rightarrow T=0\), does not call the eliminated connection
Levi-Civita, and does not call the coframe equation Einstein.

The exact certificate is

`02_REGISTRY/research/certificates/a4d_star_density_variation_pressure_check.py`.

---

## 1. The action under pressure

Use the accepted cell density

\[
\mathcal L_\star(S,x)
=
c\,\epsilon_S\,
G_2\!\left(
B_{S^c}(e,x),
\star\,\mathfrak b\!\left(\mathcal R(P_S(A,x))\right)
\right),
\tag{1.1}
\]

where

\[
\mathcal R(P)=\frac12(P-P^{-1}),
\tag{1.2}
\]

\(P_S\) is the based linear plaquette holonomy,
\(B_{S^c}=v_u\wedge v_v\), and \(G_2\) is the Lorentz degree-two pairing.

The finite action used in this research pressure test is the literal counting
sum

\[
S_\star[e,A]
=
\sum_x\sum_{S\in\binom{Role}{2}}
\mathcal L_\star(S,x).
\tag{1.3}
\]

No curvature-square, volume potential, torsion-square, fitted coefficient or
additional parity field is added.

The overall coefficient \(c\) is irrelevant for every rank/nullity statement
below as long as \(c\ne0\).

---

## 2. Exact differential of the finite curvature extraction

For any invertible matrix path \(P(t)\),

\[
D(P^{-1})_P[\dot P]
=
-P^{-1}\dot P P^{-1}.
\]

Hence

\[
\boxed{
D\mathcal R_P[\dot P]
=
\frac12
\left(
\dot P+P^{-1}\dot P P^{-1}
\right).
}
\tag{2.1}
\]

At the identity,

\[
\boxed{
D\mathcal R_I[\dot P]=\dot P.
}
\tag{2.2}
\]

For the based square
\(P=A_\square B_\square^{-1}\),

\[
\dot P
=
\dot A_\square B_\square^{-1}
-
A_\square B_\square^{-1}\dot B_\square B_\square^{-1},
\tag{2.3}
\]

with \(\dot A_\square,\dot B_\square\) themselves the ordered link
insertions in the two two-edge paths.

Thus the exact connection Euler equation is a finite
**Jacobian-adjoint equation**.  It is not licensed to be renamed a continuum
covariant derivative before an exact identification theorem is proved.

The coframe derivative is simpler because the solder legs are affine-linear in
the raw coframe:

\[
D B_{S^c}[h]
=
\delta v_u[h]\wedge v_v
+
v_u\wedge\delta v_v[h].
\tag{2.4}
\]

Therefore

\[
\begin{aligned}
D S_\star[e,A][h,\dot A]
=
c\sum_{x,S}\epsilon_S\bigl[
&
G_2\left(D B_{S^c}[h],\star C_S\right)
\\
&+
G_2\left(
B_{S^c},
\star\,\mathfrak b
\left(D\mathcal R_{P_S}[D P_S[\dot A]]\right)
\right)
\bigr].
\end{aligned}
\tag{2.5}
\]

Equation (2.5) is the exact finite first-variation formula used conceptually in
the rest of the memo.

---

## 3. Flat background is stationary

At

\[
e=0,
\qquad
P_S=I,
\]

the accepted solder legs are the Role basis vectors and

\[
C_S=0.
\]

Hence the coframe part of (2.5) vanishes.

The connection part uses (2.2).  Its first plaquette jet is the oriented
forward curl of the link tangent.  Since the flat complementary bivectors are
constant and the archive is periodic, the counting sum telescopes.

Therefore

\[
D S_\star[0,I]=0.
\tag{3.1}
\]

This is important for the quadratic pressure test: the Hessian at the flat
background is coordinate-independent under any smooth reparameterization of
the Lorentz links with the same first tangent.  The certificate uses
exponential link two-jets only as a convenient exact chart.

---

## 4. Exact quadratic form on the \(L=2\) four-Role torus

For \(N=0\),

\[
archiveFibers(0)=2.
\]

Every translation character is therefore

\[
\chi=(\chi_A,\chi_B,\chi_C,\chi_D),
\qquad
\chi_r\in\{+1,-1\}.
\]

At one momentum sector write the solder-leg perturbations as

\[
v_r=e_r+t h_r
\]

with 16 real amplitudes, and the Lorentz link tangents as

\[
L_r(x,t)
=
\exp\left(t\,\chi(x)a_r\right),
\qquad
a_r\in\mathfrak{so}(1,3),
\]

with \(4\times6=24\) amplitudes.

For a face \(r<s\),

\[
P_{rs}
=
L_r(x)L_s(x+r)L_r(x+s)^{-1}L_s(x)^{-1}.
\tag{4.1}
\]

Write

\[
P_{rs}=I+tP_1+t^2P_2+O(t^3).
\]

Then exactly

\[
\mathcal R(P_{rs})
=
tP_1+t^2\left(P_2-\frac12P_1^2\right)+O(t^3).
\tag{4.2}
\]

The first curvature jet is

\[
P_1
=
(\chi_r-1)a_s-(\chi_s-1)a_r.
\tag{4.3}
\]

The quadratic action has the block form

\[
S_\star^{(2)}
=
\frac12
\begin{pmatrix}h&a\end{pmatrix}
\begin{pmatrix}
0&H_{ha}\\
H_{ah}&H_{aa}
\end{pmatrix}
\begin{pmatrix}h\\a\end{pmatrix}.
\tag{4.4}
\]

The zero \(hh\) block is structural: curvature vanishes at the background,
so two coframe variations without a connection variation do not contribute at
quadratic order.

All matrices in this section are computed exactly over \(\mathbb Q\).

---

## 5. Connection elimination survives

For **all 16** \(L=2\) momentum characters,

\[
\boxed{
\operatorname{rank}H_{aa}=24.
}
\tag{5.1}
\]

Thus, in this flat quadratic specialization, the Lorentz connection variables
are auxiliary and algebraically eliminable without a pseudoinverse:

\[
a_*(h)
=
-H_{aa}^{-1}H_{ah}h.
\tag{5.2}
\]

The exact Schur operator is

\[
K_{\rm eff}
=
-H_{ha}H_{aa}^{-1}H_{ah}.
\tag{5.3}
\]

This already kills two possible failure modes:

1. the selected density is not variationally empty;
2. the quadratic connection equation is not underdetermined by an extra
   connection kernel on \(L=2\).

No statement is made that (5.2) is the globally selected nonlinear connection.

---

## 6. \(d_E=1\)

The accepted insertion/action family is one-dimensional:

\[
S_c=cS_\star.
\]

Euler differentiation is linear in the action:

\[
\operatorname{EL}(S_c)
=
c\,\operatorname{EL}(S_\star).
\]

Therefore

\[
d_E\le1.
\]

The exact certificate finds nonzero Hessian rank (indeed rank 24 already at
zero momentum and rank 28 or 30 at every nonzero sector).  Hence
\(S_\star\) is not a constant functional / total variational zero:

\[
\operatorname{EL}(S_\star)\ne0.
\]

Consequently

\[
\boxed{d_E=1.}
\tag{6.1}
\]

This conclusion is about the Euler family generated by the selected finite
action.  It is not an identification of those equations with a continuum field
equation.

---

## 7. Exact flat gauge kernel

At a nonzero \(L=2\) momentum the certificate constructs ten independent
Hessian-null directions.

### 7.1 Six local Lorentz directions

For \(\lambda\in\mathfrak{so}(1,3)\),

\[
\delta h_r=\lambda e_r,
\qquad
\delta a_r=(1-\chi_r)\lambda.
\tag{7.1}
\]

These are precisely the flat tangent form of a local frame transformation in
the link/solder conventions used by the repository.

### 7.2 Four forward-coframe directions

For \(\xi\in V\),

\[
\delta h_r=(\chi_r-1)\xi,
\qquad
\delta a_r=0.
\tag{7.2}
\]

Up to the invertible Lorentz musical map between the raw coframe row and the
solder vector, these are the momentum components of the owned
`forwardGaugeCoframe`.

For every nonzero character,

\[
\operatorname{rank}G_{\rm gauge}=10,
\qquad
H\,G_{\rm gauge}=0.
\tag{7.3}
\]

Thus the quadratic action has at least the exact expected flat null directions
from local frame plus forward-coframe gauge tangents.

---

## 8. Generic quotient and the exact Lorentz-null rank drop

Define the discrete checkerboard derivative vector

\[
\kappa_r:=1-\chi_r\in\{0,2\},
\]

and its Role-Lorentz norm

\[
\kappa_\eta^2
=
\kappa_A^2
-
\kappa_B^2
-
\kappa_C^2
-
\kappa_D^2.
\tag{8.1}
\]

### 8.1 Generic nonzero sectors

For every nonzero sector with

\[
\kappa_\eta^2\ne0,
\]

the full 40-variable Hessian has

\[
\operatorname{rank}H=30,
\qquad
\dim\ker H=10.
\tag{8.2}
\]

Because the ten gauge vectors in (7.3) are independent, they exhaust the
kernel.

Equivalently, after exact connection elimination,

\[
\boxed{
\operatorname{rank}K_{\rm eff}=6,
}
\tag{8.3}
\]

on the six-dimensional coframe quotient left after removing the ten
coframe/frame gauge directions from the 16 coframe amplitudes.

Thus the quotient operator is nonzero and generically nonsingular.

### 8.2 Lorentz-null sectors

There are exactly three nonzero period-two sectors with

\[
\kappa_\eta^2=0:
\]

\[
(-1,-1,+1,+1),
\quad
(-1,+1,-1,+1),
\quad
(-1,+1,+1,-1).
\tag{8.4}
\]

They are characterized algebraically by a nonzero A component together with
exactly one nonzero spacelike Role component.  No physical time interpretation
of Role A is used here.

At each of these three sectors,

\[
\operatorname{rank}H=28,
\qquad
\dim\ker H=12,
\tag{8.5}
\]

and

\[
\boxed{
\operatorname{rank}K_{\rm eff}=4.
}
\tag{8.6}
\]

After quotienting the ten gauge directions, exactly two additional null
directions remain:

\[
\boxed{
\dim\left(\ker H/G_{\rm gauge}\right)=2.
}
\tag{8.7}
\]

This is an exact finite algebraic rank drop.  It is not called a wave,
propagating graviton, frequency shell or physical time mode in this memo.

---

## 9. Flat physical-family survival

The map

\[
\operatorname{EL}\longrightarrow
\operatorname{EL}/(\text{flat gauge})
\]

can only send the one-dimensional Euler family either to zero or to a
one-dimensional family.

Sections 7–8 show that the quotient operator is nonzero: it has rank six on
generic nonzero sectors.

Therefore the selected action survives the **owned flat linearized quotient**:

\[
\boxed{
d_{P,\mathrm{flat},L=2}=1.
}
\tag{9.1}
\]

This is the strongest physical-operator statement licensed by the current
owners.

---

## 10. Hostile torsion test: the naive identity fails

The most important negative control is the finite torsion identification.

At flat solder define the obvious vector-valued forward torsion candidate

\[
T_{rs}
=
(\chi_r-1)h_s
-
(\chi_s-1)h_r
+
a_r e_s
-
a_s e_r.
\tag{10.1}
\]

It is exactly invariant under the gauge tangents (7.1)–(7.2), and its
connection part

\[
T=T_a a+T_h h
\]

has

\[
\boxed{
\operatorname{rank}T_a=24.
}
\tag{10.2}
\]

Therefore \(T=0\) would uniquely determine a connection for every coframe
perturbation.

The actual connection Euler equation is

\[
H_{aa}a+H_{ah}h=0.
\tag{10.3}
\]

If (10.3) were merely an invertible recombination of \(T=0\), then necessarily

\[
H_{ah}
=
H_{aa}T_a^{-1}T_h.
\tag{10.4}
\]

The exact certificate disproves (10.4).

For example, in the single-direction checkerboard sector

\[
\chi=(+1,+1,+1,-1),
\]

the mismatch matrix

\[
H_{ah}-H_{aa}T_a^{-1}T_h
\]

has exact rank

\[
\boxed{6}.
\tag{10.5}
\]

Hence

\[
\boxed{
\text{finite connection EL}
\not\equiv
\text{naive forward }T=0
}
\]

for the accepted same-site complementary-solder / based-plaquette placement.

This kills the shortcut

\[
D(e\wedge e)=0
\Rightarrow
T=0
\]

as an **exact finite theorem for the current placement**.

It does not prove that no better transported/common-center torsion identity can
be built.  Such a repair would be new geometry and must be derived rather than
inserted.

---

## 11. Why the full nonlinear \(d_P\) stops here

The flat quadratic calculation itself has a clean quotient.  The full finite
theory does not yet have the required global gauge action on the solder.

The existing Lean boundary is explicit:

- an affine node gauge acts on a genuine affine point by
  \(v\mapsto h_x(v)=g_xv+c_x\);
- the owned raw solder frame action supplies only the linear part
  \(v\mapsto g_xv\);
- under a pure node translation, the missing additive term leaves an exact
  residual \(c_x\).

This is
`A4DAffineOriginSolderBoundary.rawFullSolderFrameAction_misses_affine_translation_term`.

Therefore the flat direction

\[
h=d_f\xi
\]

is an owned **tangent / exact-coframe** direction, and the Hessian correctly
kills it, but D0 does not yet own one nonlinear finite action of arbitrary
affine node gauges on the raw solder data used by (1.1).

Without that owner, a global quotient

\[
\{	ext{finite EL configurations}\}/
\{	ext{full affine solder gauge}\}
\]

is not a defined repository object.

Thus the first exact global blocker is

\[
\boxed{
\texttt{FULL-AFFINE-SOLDER-GAUGE-QUOTIENT-MISSING}.
}
\tag{11.1}
\]

The older solder-reference work further shows that merely declaring a full
affine point law would not by itself select all source-reference/path data.
This task does not reopen that lane; it only records that the missing affine
solder action prevents promotion of (9.1) to an all-background \(d_P=1\)
theorem.

---

## 12. What survived and what did not

| Gate | Result |
|---|---|
| selected action family | \(d_A=1\) accepted upstream |
| exact first variation | well typed as finite Jacobian-adjoint formula |
| variational nontriviality | survives; Hessian nonzero |
| Euler-family dimension | \(d_E=1\) |
| flat connection elimination | survives; \(H_{aa}\) rank 24 everywhere on \(L=2\) |
| flat local Lorentz gauge | exact Hessian null |
| flat forward-coframe gauge | exact Hessian null |
| generic flat quotient | nonzero, effective rank 6 |
| Lorentz-null checkerboard | rank 4 after connection elimination; two extra quotient nulls |
| naive exact finite torsion-free identity | **fails** |
| full nonlinear affine quotient | **not owned** |
| global finite \(d_P\) | blocked by (11.1) |
| continuum / Einstein / time interpretation | not attempted |

So the density does not die.  It reaches the full-affine quotient boundary with
a nontrivial, highly structured flat operator already visible.

---

## 13. Theorem-ready statements

1. **Finite curvature differential.**  
   \[
   D\mathcal R_P[\dot P]
   =
   \tfrac12(\dot P+P^{-1}\dot P P^{-1}).
   \]

2. **Identity derivative.**  
   \[
   D\mathcal R_I=\operatorname{id}.
   \]

3. **Flat stationarity.**  
   The periodic flat background \((e=0,P=I)\) is stationary for
   \(S_\star\).

4. **Quadratic no-\(hh\) block.**  
   At flat curvature the pure coframe Hessian block vanishes before connection
   elimination.

5. **Period-two connection invertibility.**  
   For every \(L=2\) Role momentum,
   \[
   \operatorname{rank}H_{aa}=24.
   \]

6. **Nontrivial Euler family.**  
   The Hessian is nonzero, hence the selected one-dimensional action family has
   \(d_E=1\).

7. **Ten flat gauge tangents.**  
   At every nonzero \(L=2\) momentum the six local-Lorentz and four
   forward-coframe tangents are independent and Hessian-null.

8. **Generic kernel is exactly gauge.**  
   For every nonzero \(\kappa_\eta^2\ne0\) sector,
   \[
   \operatorname{rank}H=30,
   \quad
   \ker H=G_{\rm gauge}.
   \]

9. **Generic effective coframe rank.**  
   \[
   \operatorname{rank}K_{\rm eff}=6.
   \]

10. **Exact null-shell classification at \(L=2\).**  
    Exactly three nonzero characters satisfy \(\kappa_\eta^2=0\).

11. **Null-shell rank drop.**  
    On those sectors,
    \[
    \operatorname{rank}H=28,
    \quad
    \operatorname{rank}K_{\rm eff}=4.
    \]

12. **Two nongauge null directions.**  
    \[
    \dim(\ker H/G_{\rm gauge})=2
    \]
    on every nonzero Lorentz-null checkerboard sector.

13. **Flat physical-family survival.**  
    The quotient operator is not zero, so
    \[
    d_{P,\mathrm{flat},L=2}=1.
    \]

14. **Naive torsion map is connection-injective.**  
    The flat forward torsion map has connection block rank 24.

15. **Connection EL is not naive torsion.**  
    In sector \((+,+,+,-)\),
    \[
    \operatorname{rank}
    (H_{ah}-H_{aa}T_a^{-1}T_h)=6.
    \]

16. **No exact finite torsion-free promotion.**  
    The current density/placement does not justify identifying the connection
    Euler equation with \(T=0\).

17. **Full affine quotient owner is missing.**  
    The existing raw solder action lacks the node-translation term required for
    a global affine solder gauge law.

18. **Global \(d_P\) remains unclassified.**  
    Promotion from (9.1) to all finite backgrounds requires the missing owner
    in Proposition 17.

---

## 14. Mandatory negative controls

- **Total-divergence collapse:** rejected by the exact nonzero Hessian.
- **Connection underdetermination:** rejected on \(L=2\); \(H_{aa}\) is
  full rank 24.
- **Fake torsion-free shortcut:** rejected by the rank-6 mismatch witness.
- **Gauge directions counted as physical:** rejected; all ten explicit gauge
  tangents lie in the Hessian kernel.
- **Null-shell directions counted before quotient:** rejected; the two residual
  directions are counted only after removing the ten gauge directions.
- **Role A called physical time:** rejected; only the owned Lorentz signature is
  used in \(\kappa_\eta^2\).
- **Rank drop called a wave equation:** rejected.
- **Continuum Einstein identification:** rejected.
- **Full \(d_P=1\) from a flat Hessian:** rejected; only
  \(d_{P,\mathrm{flat},L=2}=1\) is claimed.
- **Full affine solder covariance assumed:** rejected by the existing Lean
  boundary theorem.

---

## 15. Terminal disposition

The pressure test does **not** kill the canonical \(\star\)-density.

It establishes the chain

\[
\boxed{
d_A=1
\longrightarrow
d_E=1
\longrightarrow
d_{P,\mathrm{flat},L=2}=1
}
\]

with exact finite rank/nullity witnesses.

The full nonlinear path stops at one already-visible typed boundary:

\[
\boxed{
\texttt{FULL-AFFINE-SOLDER-GAUGE-QUOTIENT-MISSING}.
}
\]

The next legitimate calculation is therefore **not** another action selector.
It is a full affine solder/gauge action or equivalent finite quotient owner
that:

1. extends the current pure-linear solder action by the required translation
   term without erasing the independently owned affine-shift information;
2. reduces to `forwardGaugeCoframe` on the flat translation chart;
3. makes the complete finite \(S_\star\) transformation law explicit;
4. permits the nonlinear EL quotient to be defined;
5. is then pressure-tested against the exact \(L=2\) flat result above.

Until that object exists, the exact flat rank structure is evidence of survival,
not a license for a continuum gravity claim.


---

## Ready-state CONTROL audit

PR #175 is `Lifecycle: REVIEW`; the CONTROL task row remains present in the
branch manifest with state `REVIEW`, and the executable brief remains present,
as required for a Ready CONTROL PR. This audit-only commit changes no
mathematical result; it exists to run repository guards against the final
Ready-state contract.
