# MEMO A4D — affine relative-solder star action completion

**Task:** \`EXP-A4D-AFFINE-RELATIVE-SOLDER-ACTION-COMPLETION\`  
**Execution:** PR #184  
**Status:** terminal EXPENSIVE research classification  
**Baseline:** main after the first Cartan-Hodge on-shell translation no-go

## 0. Verdict

There is a mathematically clean one-parameter way to make the canonical star
density exactly invariant under the already-constructed observer-completed
full affine node gauge:

\[
\widehat\Theta^{(\lambda)}_{x,r}
=
\Theta_{x,r}
-
\lambda\, b_{x,r}^{T}h_{n_x}.
\]

Full affine covariance uniquely forces

\[
\boxed{\lambda=1.}
\]

For

\[
\boxed{
\widehat\Theta_{x,r}
=
\Theta_{x,r}
-
b_{x,r}^{T}h_{n_x},
}
\tag{0.1}
\]

the relative row transforms with no translational inhomogeneity,

\[
\boxed{
\widehat\Theta'_{x,r}
=
\widehat\Theta_{x,r}g_x^{-1}.
}
\tag{0.2}
\]

Consequently the canonical star density built from
\(\widehat\Theta\) is exactly invariant under arbitrary finite
site-dependent Lorentz **and** node-translation gauges.  The exact certificate
checks all \(16\times6=96\) cell densities separately on a mixed curved
\(L=2\) background.

This is a genuine constructive result.

However the same construction fails the next KILL-FIRST gate.

The action factors only through the relative combination
\(\widehat\Theta\).  Hence it is invariant under every matched edgewise shift

\[
\Theta_{x,r}
\mapsto
\Theta_{x,r}+u_{x,r}^{T}h_{n_x},
\qquad
b_{x,r}\mapsto b_{x,r}+u_{x,r},
\tag{0.3}
\]

for an **arbitrary edge field** \(u\), not only for node-generated affine gauge
shifts

\[
u=D_Lc.
\]

On the exact curved \(L=2\) witness,

\[
\dim C^0(X,V)=64,
\qquad
\dim C^1_+(X,V)=256,
\]

and the covariant node-difference

\[
D_L:c\mapsto
\bigl(c_x-L_{x,r}c_{x+r}\bigr)_{x,r}
\]

has exact rank \(64\).  Thus it is injective, and the intended translation
gauge occupies only a 64-dimensional subspace of the 256-dimensional matched
edge-diagonal symmetry.

The completed action is blind to all 256 directions.

Therefore after removing the actual node gauge it still has

\[
\boxed{256-64=192}
\]

nongauge accidental edge-diagonal null directions.

An explicit one-edge vector \(u\) satisfies

\[
\operatorname{rank}D_L=64,
\qquad
\operatorname{rank}[D_L\mid u]=65,
\]

so it is not node gauge, while (0.3) leaves both
\(\widehat\Theta\) and the action exactly unchanged.

The terminal is therefore

\[
\boxed{
\texttt{AFFINE-RELATIVE-SOLDER-COMPLETION-OVERQUOTIENTS-EDGE-DIAGONAL}.
}
\]

The result has two parts that must not be conflated:

1. **positive:** \(\lambda=1\) is the unique fully affine-covariant member of
   this minimal relative-solder family;
2. **negative:** an action depending only on that relative solder erases the
   entire common edge-diagonal sector, much larger than the actual node gauge.

So this PR does **not** establish the final translation-invariant physical
action.

It proves what the next completion must do:

> retain the uniquely selected relative-solder star term, but add an
> independently justified affine/torsion/overlap invariant that vanishes on
> \(u=D_Lc\) while remaining sensitive to the nongauge
> \(\operatorname{coker}D_L\) edge sector.

The exact certificate is

\`02_REGISTRY/research/certificates/a4d_affine_relative_solder_action_completion_check.py\`.

---

## 1. Inputs already owned before this task

Fix one positive Role edge

\[
y=x+r.
\]

The affine link is

\[
A_{x,r}(z)
=
L_{x,r}z+b_{x,r},
\]

with

\[
L_{x,r}:V_y\to V_x,
\qquad
b_{x,r}\in V_x.
\]

The raw solder row is

\[
\Theta_{x,r}
=
\eta_r+e_{x,r}.
\]

The observer is a future unit vector

\[
n_x\in V_x,
\]

and the owned positive observer form is

\[
h_n
=
-\eta+2n^\flat\otimes n^\flat.
\tag{1.1}
\]

At the rest observer,

\[
h_{n_0}=I.
\tag{1.2}
\]

The affine node gauge is

\[
h_x(z)=g_xz+c_x.
\]

Its exact link law is

\[
L'_{x,r}
=
g_xL_{x,r}g_y^{-1},
\tag{1.3}
\]

\[
b'_{x,r}
=
g_xb_{x,r}
+
c_x
-
L'_{x,r}c_y.
\tag{1.4}
\]

Write

\[
\tau_{x,r}
=
c_x-L'_{x,r}c_y.
\tag{1.5}
\]

The observer-completed solder law constructed in the preceding affine-solder
packet is

\[
n'_x=g_xn_x,
\tag{1.6}
\]

\[
\Theta'_{x,r}
=
\Theta_{x,r}g_x^{-1}
+
\tau_{x,r}^{T}h_{n'_x}.
\tag{1.7}
\]

This law is an exact affine group action and reproduces the owned flat
\`forwardGaugeCoframe\` chart.

It was not a symmetry of the original star density because that density
contained \(\Theta\) but not \(b\).

The present task asks whether the smallest action enlargement that also uses
the already-owned independent \(b\) closes the symmetry.

---

## 2. Observer flattening of the affine shift

For a vector \(v\in V_x\), define its observer row

\[
v^{\flat_n}
:=
v^Th_n.
\tag{2.1}
\]

The observer congruence is

\[
h_{gn}
=
g^{-T}h_ng^{-1}.
\tag{2.2}
\]

Therefore

\[
(gv)^{\flat_{gn}}
=
v^{\flat_n}g^{-1}.
\tag{2.3}
\]

Using

\[
b'=gb+\tau,
\]

one gets

\[
\boxed{
(b')^{\flat_{n'}}
=
b^{\flat_n}g^{-1}
+
\tau^{\flat_{n'}}.
}
\tag{2.4}
\]

This is exactly the same inhomogeneous row term that appears in the solder law
(1.7).

That coincidence is not imposed by identifying \(b\) with the solder.

It follows from the independent affine connection transformation and the
already-owned observer pairing.

---

## 3. The one-parameter relative-solder family

Consider

\[
\boxed{
\widehat\Theta^{(\lambda)}
=
\Theta
-
\lambda\,b^{\flat_n}.
}
\tag{3.1}
\]

Combining (1.7) and (2.4),

\[
\begin{aligned}
\widehat\Theta'^{(\lambda)}
&=
\Theta g^{-1}
+
\tau^{\flat_{n'}}
-
\lambda
\left(
b^{\flat_n}g^{-1}
+
\tau^{\flat_{n'}}
\right)
\\
&=
\left(
\Theta-\lambda b^{\flat_n}
\right)g^{-1}
+
(1-\lambda)\tau^{\flat_{n'}}.
\end{aligned}
\]

Thus

\[
\boxed{
\widehat\Theta'^{(\lambda)}
=
\widehat\Theta^{(\lambda)}g^{-1}
+
(1-\lambda)\tau^{\flat_{n'}}.
}
\tag{3.2}
\]

The inhomogeneous term vanishes for every affine gauge if and only if

\[
\boxed{\lambda=1.}
\tag{3.3}
\]

So inside this minimal affine-linear family, translation covariance is not a
free coefficient choice.

It selects one relative solder.

---

## 4. Relative solder vector and bivector

For the selected row

\[
\widehat\Theta_{x,r}
=
\Theta_{x,r}
-
b_{x,r}^{\flat_{n_x}},
\]

define the relative solder vector with the same owned row/vector convention as
before:

\[
\boxed{
\widehat v_r(x)
=
\eta\,\widehat\Theta_{x,r}^{T}.
}
\tag{4.1}
\]

Because \(g\) is Lorentz and

\[
\widehat\Theta'
=
\widehat\Theta g^{-1},
\]

one has

\[
\boxed{
\widehat v'_r
=
g_x\widehat v_r.
}
\tag{4.2}
\]

For a complementary Role pair \(S^c=\{u,v\}\), set

\[
\widehat B_{S^c}
=
\widehat v_u\wedge\widehat v_v.
\tag{4.3}
\]

Then

\[
\boxed{
\widehat B'_{S^c}
=
\rho_2(g_x)\widehat B_{S^c}.
}
\tag{4.4}
\]

Thus the relative solder has exactly the same Lorentz exterior type as the
original solder.

No new Role orientation or parity datum is introduced.

---

## 5. Completed canonical star density

Keep the accepted based linear plaquette

\[
P_S(x)
\]

and exact odd extraction

\[
\mathcal R(P)
=
\frac12(P-P^{-1}).
\]

Let

\[
C_S
=
\mathfrak b(\mathcal R(P_S))
\]

be the accepted curvature bivector.

Define

\[
\boxed{
\widehat{\mathcal L}_\star(S,x)
=
c\,\epsilon_S\,
G_2\left(
\widehat B_{S^c},
\star C_S
\right).
}
\tag{5.1}
\]

The affine translations do not alter the linear link \(L\), hence they do not
alter \(P_S\) or \(C_S\).

Under the full affine gauge, the linear part still obeys

\[
P'_S
=
g_xP_Sg_x^{-1},
\]

so

\[
C'_S
=
\rho_2(g_x)C_S.
\tag{5.2}
\]

For proper Lorentz \(g_x\),

\[
\rho_2(g_x)^TG_2\rho_2(g_x)=G_2,
\]

\[
\star\rho_2(g_x)
=
\rho_2(g_x)\star.
\]

Together with (4.4),

\[
\boxed{
\widehat{\mathcal L}'_\star(S,x)
=
\widehat{\mathcal L}_\star(S,x)
}
\tag{5.3}
\]

cell by cell.

Therefore

\[
\boxed{
\widehat S_\star
=
\sum_{x,S}\widehat{\mathcal L}_\star(S,x)
}
\tag{5.4}
\]

is an exact finite full-affine invariant of the observer-completed gauge
package.

---

## 6. Exact mixed-gauge finite control

The certificate uses the full period-two Role torus and a curved affine
background with:

- a rational \(A/B\) boost link;
- a \(B/C\) quarter-turn link;
- a \(C/D\) quarter-turn link;
- two independent rational affine shifts;
- nontrivial raw solder perturbations;
- rest observers initially;
- a site-dependent proper-Lorentz field taking many distinct values;
- a nonconstant rational node-translation field.

It transforms simultaneously

\[
(L,b,\Theta,n)
\]

by the full affine laws.

For every one of the 64 positive links it verifies

\[
\widehat\Theta'_{x,r}
=
\widehat\Theta_{x,r}g_x^{-1}.
\]

It then evaluates all 96 site/face density terms exactly over \(\mathbb Q\).

The result is

\[
\boxed{
\widehat{\mathcal L}'_\star(S,x)
=
\widehat{\mathcal L}_\star(S,x)
\quad
\text{for all 96 cells}.
}
\tag{6.1}
\]

So the positive covariance result is not a global-sum cancellation.

---

## 7. Exact \(\lambda\) selector witness

Take the curved linear-link background used in the earlier translation
pressure:

\[
S_{\rm before}
=
-\frac23,
\]

with

\[
b=0,
\qquad
\Theta=\eta,
\qquad
n=n_0.
\]

Apply a pure node translation at one site.

For the family (3.1), the exact transformed action is

\[
S_{\rm after}(\lambda)
=
\frac23(\lambda-2).
\tag{7.1}
\]

Hence

\[
\boxed{
S_{\rm after}(\lambda)
-
S_{\rm before}
=
\frac23(\lambda-1).
}
\tag{7.2}
\]

Therefore

\[
\boxed{
S_{\rm after}=S_{\rm before}
\iff
\lambda=1.
}
\tag{7.3}
\]

At

\[
\lambda=0,
\]

one recovers exactly the old failure

\[
-\frac23
\longrightarrow
-\frac43.
\]

Thus the new selector is directly tied to cancellation of the known
translation defect.

---

## 8. Flat and old-action limits

### 8.1 \(b=0\)

If

\[
b=0,
\]

then

\[
\widehat\Theta=\Theta
\]

and

\[
\boxed{
\widehat S_\star
=
S_\star.
}
\tag{8.1}
\]

Thus the completed action contains the accepted canonical star action as a
literal slice.

It does not replace the previously selected insertion.

### 8.2 Exact flat translation gauge

At

\[
L=I,
\qquad
n=n_0,
\]

the owned translation gauge gives the same edge vector \(\tau\) in the affine
shift and raw solder row:

\[
b'=\tau,
\qquad
\Theta'=\eta+\tau^T.
\]

Therefore

\[
\boxed{
\widehat\Theta'
=
\eta.
}
\tag{8.2}
\]

The translation-gauge diagonal is removed exactly, as desired.

---

## 9. Independent affine shift remains visible

The relative action does not simply discard \(b\).

Hold the raw solder fixed and turn on one independent affine edge shift.

On the exact curved control,

\[
S_\star(b=0)
=
-\frac23,
\]

whereas one pure affine shift gives

\[
\boxed{
\widehat S_\star
=
-\frac53.
}
\tag{9.1}
\]

Thus

\[
\boxed{
\text{pure independent }b
\text{ changes the completed action.}
}
\]

So the action does not identify \(b\) with \(e\), and it does not erase a shift
merely because it exists.

The fatal problem below is subtler: it erases arbitrary **matched** edge
changes, whether or not they are genuine node gauge.

---

## 10. The hidden extra symmetry

Because the action depends on \((\Theta,b)\) only through

\[
\widehat\Theta
=
\Theta-b^{\flat_n},
\]

for any target-fibre edge vector field

\[
u_{x,r}\in V_x
\]

one has the exact transformation

\[
b_{x,r}
\mapsto
b_{x,r}+u_{x,r},
\tag{10.1}
\]

\[
\Theta_{x,r}
\mapsto
\Theta_{x,r}+u_{x,r}^{\flat_n},
\tag{10.2}
\]

with

\[
L,n
\]

fixed.

Then

\[
\boxed{
\widehat\Theta
\mapsto
\widehat\Theta.
}
\tag{10.3}
\]

Therefore

\[
\boxed{
\widehat S_\star
\mapsto
\widehat S_\star
}
\tag{10.4}
\]

for every edge field \(u\).

This symmetry is much larger than the intended affine node-translation gauge.

---

## 11. Intended node gauge versus arbitrary edge diagonal

For a pure node translation with fixed \(L\), the allowed matched edge field is

\[
\boxed{
u_{x,r}
=
(D_Lc)_{x,r}
=
c_x-L_{x,r}c_{x+r}.
}
\tag{11.1}
\]

So the intended translation gauge occupies

\[
\operatorname{im}D_L
\subset
C^1_+(X,V).
\]

On the exact curved \(L=2\) witness,

\[
\dim C^0(X,V)
=
16\cdot4
=
64,
\]

\[
\dim C^1_+(X,V)
=
16\cdot4\cdot4
=
256.
\]

The exact covariant node-difference matrix has

\[
\boxed{
\operatorname{rank}D_L=64.
}
\tag{11.2}
\]

Hence this witness has no nonzero covariantly constant translation parameter:

\[
\ker D_L=0.
\]

The gauge image is exactly 64-dimensional.

But the action is invariant under the entire 256-dimensional edge-diagonal
space (10.1)-(10.2).

Thus the excess accidental degeneracy has dimension

\[
\boxed{
256-64=192.
}
\tag{11.3}
\]

This is precisely the size of the finite edge sector not generated by node
translations on this witness.

---

## 12. Exact nongauge one-edge witness

Let \(u\) be supported on one edge/component only.

The exact matrix ranks are

\[
\boxed{
\operatorname{rank}D_L=64,
}
\]

\[
\boxed{
\operatorname{rank}[D_L\mid u]=65.
}
\tag{12.1}
\]

Therefore

\[
u\notin\operatorname{im}D_L.
\]

It is not a pure affine node gauge.

Now apply the matched edge shift

\[
(\Theta,b)
\mapsto
(\Theta+u^{\flat_n},b+u).
\]

The certificate verifies

\[
\boxed{
\widehat\Theta_{\rm after}
=
\widehat\Theta_{\rm before}
}
\]

on every edge and

\[
\boxed{
\widehat S_{\star,\rm after}
=
\widehat S_{\star,\rm before}
=
-\frac23.
}
\tag{12.2}
\]

Because the relative solder is nondegenerate, any full affine gauge preserving
the same \(\widehat\Theta\) must have

\[
g_x=I.
\]

Then a full affine gauge relation would reduce to

\[
D_Lc=u,
\]

which (12.1) excludes.

Thus the two configurations are on distinct intended affine-gauge orbits but
the completed action cannot distinguish them.

---

## 13. Why this is a real KILL-FIRST failure

One could simply declare the whole edge-diagonal transformation (10.1)-(10.2)
to be a new gauge symmetry.

Current D0 does not own that symmetry.

Doing so would quotient:

- curl-type common edge data;
- harmonic/cycle common edge data;
- every other component of
  \(\operatorname{coker}D_L\).

That is exactly the kind of silent information erasure earlier A/e and
reference-leg pressure tests were designed to prevent.

The intended affine gauge has **node** parameters.

The new accidental invariance has independent **edge** parameters.

They are not the same object.

Therefore the simple relative-solder action is too compressed to be accepted
as the final physical completion without a new principle declaring those extra
192 directions redundant.

No such principle is owned.

---

## 14. Role naturality

The selected relative solder introduces no new Role tensor.

For each Role edge it subtracts from the raw row another row in the same target
fibre.

Under the accepted simultaneous A-stabilizer Role/site relabeling:

- the edge Role label is relabeled in both \(\Theta_r\) and \(b_r\);
- the internal vector/row transformation is the same owned Role action;
- the observer pairing is natural under the corresponding metric-preserving
  frame action.

Hence

\[
\widehat\Theta_r
\]

has the same Role/exterior typing as the original solder.

The prior oriented-density selector therefore applies unchanged.

No new \(I/\star\) insertion modulus is introduced by the subtraction.

---

## 15. Dimension bookkeeping

### 15.1 Action family

Inside the family

\[
\Theta-\lambda b^{\flat_n},
\]

full affine covariance uniquely fixes

\[
\lambda=1.
\]

Only the old overall action scale remains.

Therefore, inside this completion class,

\[
\boxed{
d_A^{\rm rel}=1.
}
\tag{15.1}
\]

### 15.2 Euler family

The \(b=0\) slice is exactly the accepted star action, whose Euler family is
nonzero.

Therefore the completed one-dimensional action family is not variationally
trivial:

\[
\boxed{
d_E^{\rm rel}=1.
}
\tag{15.2}
\]

### 15.3 Physical quotient

The completed action is an exact invariant of the intended full affine gauge,
so it does descend through that gauge relation.

It is also nonconstant: already the \(b=0\) curved slice has the accepted
nonzero star response.

Thus the one-dimensional operator family does not disappear merely by taking
the intended affine quotient.

However the action has a further 192-dimensional nongauge null space on the
explicit \(L=2\) witness.

Accordingly this packet does **not** promote a final physical
\(d_P\) claim.

The blocker is not that the family vanishes.

The blocker is that its kernel is larger than the owned gauge distribution.

A faithful physical completion must first separate those nongauge directions.

---

## 16. Theorem-ready statements

1. **Observer-flattened shift law.**
   \[
   (gb+\tau)^{\flat_{gn}}
   =
   b^{\flat_n}g^{-1}
   +
   \tau^{\flat_{gn}}.
   \]

2. **Relative-family transformation.**
   \[
   \widehat\Theta'^{(\lambda)}
   =
   \widehat\Theta^{(\lambda)}g^{-1}
   +(1-\lambda)\tau^{\flat_{n'}}.
   \]

3. **Unique covariance coefficient.**
   Full affine row covariance in the \(\lambda\)-family holds iff
   \[
   \lambda=1.
   \]

4. **Relative solder covariance.**
   \[
   \widehat\Theta'=\widehat\Theta g^{-1},
   \qquad
   \widehat v'=g\widehat v.
   \]

5. **Relative bivector covariance.**
   \[
   \widehat B'=\rho_2(g)\widehat B.
   \]

6. **Cellwise full-affine invariance.**
   \[
   \widehat{\mathcal L}'_\star(S,x)
   =
   \widehat{\mathcal L}_\star(S,x).
   \]

7. **Finite \(\lambda\) selector.**
   On the curved translation witness,
   \[
   S_{\rm after}-S_{\rm before}
   =
   \frac23(\lambda-1).
   \]

8. **Old action slice.**
   \[
   b=0
   \Rightarrow
   \widehat S_\star=S_\star.
   \]

9. **Flat translation diagonal.**
   \[
   L=I,\quad
   \Theta=\eta+\tau^\flat,\quad
   b=\tau
   \Rightarrow
   \widehat\Theta=\eta.
   \]

10. **Independent shift visibility.**
    A pure \(b\)-shift changes the curved completed action.

11. **Arbitrary matched edge invariance.**
    \[
    (\Theta,b)\mapsto
    (\Theta+u^\flat,b+u)
    \Rightarrow
    \widehat\Theta,\widehat S_\star
    \text{ unchanged}.
    \]

12. **Curved node-difference injectivity.**
    On the exact \(L=2\) witness,
    \[
    \operatorname{rank}D_L=64.
    \]

13. **Nongauge one-edge control.**
    \[
    \operatorname{rank}[D_L\mid u]=65.
    \]

14. **Accidental quotient dimension.**
    The relative action has
    \[
    256-64=192
    \]
    matched edge-diagonal directions beyond node gauge on that witness.

15. **Action-family dimension in class.**
    \[
    d_A^{\rm rel}=1.
    \]

16. **Euler-family nontriviality.**
    \[
    d_E^{\rm rel}=1.
    \]

17. **No final physical promotion.**
    The intended affine quotient exists for the action, but the action kernel
    strictly exceeds the owned gauge distribution.

---

## 17. Hostile controls

| Control | Result |
|---|---|
| \(\lambda=0\) | reproduces prior curved translation failure |
| symbolic \(\lambda\) | exact selector \(\lambda=1\) only |
| mixed site-dependent Lorentz + translation | passes |
| 64 relative solder rows | transform homogeneously |
| 96 finite cell densities | invariant individually |
| \(b=0\) | exact accepted star action |
| flat translation gauge | relative solder exactly unchanged |
| pure independent \(b\) | visible |
| nonzero curved translation stabilizer | absent on witness; \(D_L\) injective |
| one-edge matched shift | not node gauge |
| matched one-edge action response | exactly zero |
| accidental nongauge dimension | 192 |
| supplied reference section \(q\) | not used |
| Euler/Hessian repair | not used |
| Einstein/diffeomorphism/time/wave | not used |

---

## 18. Terminal disposition

The simple action-completion route has now been pressure-tested far enough to
separate covariance from physical adequacy.

The positive exact result is

\[
\boxed{
\widehat\Theta
=
\Theta-b^{\flat_n}
}
\]

as the unique fully affine-covariant member of the minimal
\(\lambda\)-family.

The negative exact result is that an action built only from that relative
solder has an unowned edgewise diagonal symmetry much larger than the affine
node gauge.

Therefore the terminal is

\[
\boxed{
\texttt{AFFINE-RELATIVE-SOLDER-COMPLETION-OVERQUOTIENTS-EDGE-DIAGONAL}.
}
\]

This means the next action term is now constrained very sharply.

It must:

1. remain full-affine gauge invariant;
2. vanish or be redundant on
   \(u=D_Lc\);
3. distinguish at least part of
   \(\operatorname{coker}D_L\);
4. preserve the accepted \(\widehat\Theta\)-star term;
5. not reintroduce a supplied reference section.

The obvious owned source of such information is the affine translation
curvature / open-torsion sector, because it is gauge covariant and is sensitive
to non-exact edge shift data.

That is the next legitimate research gate.

A generic \(T^2\) term is **not** selected by this memo; its representation,
parity, coefficient space, flat limit and variation must be classified before
it is admitted.


---

## Ready-state EXPENSIVE audit

PR #184 is \`Lifecycle: REVIEW\`. The EXPENSIVE task self-retired before Ready:
its manifest/status entry and executable task brief are absent from the branch,
while the durable memo, exact certificate, and research-ledger verdict remain.
This audit-only commit changes no mathematical result; it exists so repository
guards evaluate the final Ready-state contract rather than the preceding Draft
event.
