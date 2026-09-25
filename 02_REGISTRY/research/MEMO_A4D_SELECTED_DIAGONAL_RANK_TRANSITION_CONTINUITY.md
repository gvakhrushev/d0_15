# A4D selected diagonal rank-transition continuity

**Task:** `EXP-A4D-SELECTED-DIAGONAL-RANK-TRANSITION-CONTINUITY`  
**Research PR:** #130  
**Start baseline:** `31bdb4bac83e5222dc6fa480e5819ae6b3a81e0a`  
**Terminal:** `SELECTED-DIAGONAL-RANK-TRANSITION-CONTINUITY-CRITERION-CONSTRUCTED`  
**Strength:** theorem-ready finite-dimensional continuity classification; no Lean source, no continuum limit, no finite graded dressing.

## 0. Verdict

The pointwise relative A/e construction has an exact stability theory, but
stability is not one condition.

There are two independent finite-dimensional seams.

### Local rank seam

For
\[
C_t=\mathcal S_tP_{H_t},\qquad D_t=\mathcal S_t-C_t,
\]
a rank drop in \(\mathcal B_t\) exposes coefficient directions that were
horizontal before the limit and become kernel directions at the limit. Along
a convergent projector subsequence
\[
P_{H_{t_n}}\longrightarrow P_*,
\]
the exact lost space is
\[
W_*:=\operatorname{im}P_*\cap K_0,
\qquad
\operatorname{im}P_*=H_0\oplus W_*.
\]
Then
\[
\boxed{
C_{t_n}\longrightarrow C_0
\iff
\mathcal S_0(W_*)=0,
}
\]
and the same iff holds for \(D\).

For a specified admissible family, only the actually reachable lost spaces
matter. For arbitrary perturbations through the point, the condition becomes
exactly
\[
\boxed{
C,D\text{ are universally continuous at }(\mathcal B_0,\mathcal S_0)
\iff
M_0=\mathcal S_0(K_0)=0.
}
\]

Thus the sufficient statement anticipated in PR #128 is sharp: \(M_0=0\) is
also necessary for **universal** continuity, but it is not necessary for
continuity along a restricted family.

### Post-source selector seam

Even if \(C,D\), the seed and every path source are continuous, the PR #120
post-source selector can jump when the common holonomy-fixed kernel changes
dimension.

With a fixed basepoint/path family, write
\[
\mathcal H_t=\bigcap_\gamma\operatorname{Fix}P_{\gamma,t},
\qquad
Q_t=\operatorname{Proj}^{h_t}_{\mathcal H_t},
\]
\[
m_t=\frac1{|X|}\sum_yP_{y,t}a_t(y).
\]
The selected section is
\[
\boxed{
\delta_t(y)=a_t(y)-P_{y,t}^{-1}Q_tm_t.
}
\]
When the seed is continuous, a sequence with \(Q_{t_n}\to Q_*\) is selected-
continuous exactly when
\[
\boxed{
Q_*m_0=Q_0m_0.
}
\]
Constant \(\dim\mathcal H_t\) is a robust sufficient condition because it
makes \(Q_t\) continuous, but it is not necessary for the selected value:
a kernel dimension can jump harmlessly when the transported mean has zero
component in the newly gained fixed directions.

There is also a full joint-cluster criterion below which remains necessary
and sufficient even when the seed itself jumps.

### Mandatory obstruction survives all easy cures

The required \(L=3\) family has:

- continuous background data;
- determinant-one raw solder;
- a continuous, constant-dimensional relation at the nonzero-\(d_j\) sites;
- identity linear transport;
- trivial affine holonomy for every parameter;
- zero selected mismatch for every \(t\ne0\);

but
\[
\kappa_A(0;0)=-3e_B.
\]

The failure occurs before the post-source selector: a surviving lost
coefficient direction makes \(C,D\), then the seed and source, jump.

Endpoint descent, affine flatness, raw-solder invertibility and relation
continuity are therefore not stability criteria.

The exact repair options are correspondingly limited:

1. restrict backgrounds by the lost-direction and fixed-kernel criteria;
2. add a new datum which remembers the disappearing active direction;
3. quotient/forget the jump direction, explicitly losing any observable that
   uses it.

For the mandatory family, any linear quotient that kills its \(e_B\) jump
also kills the mandatory \(L=3\) corner response \(e_B\). Hence quotienting
does not preserve the current full readout.

---

## 1. Ownership boundary

This memo uses the landed repository state only.

The pointwise coefficient construction is owned by
`A4DRelativeAEComparisonSpan.lean`. In the notation used here,
\[
K=\ker\mathcal B,\qquad H=K^\perp,
\]
and its canonical counting representative gives
\[
C=\mathcal SP_H,\qquad
D=\mathcal SP_K=\mathcal S-C.
\]

The sourced chain is owned conditionally by
`A4DConditionalSourcedDiagonalTransport.lean`:
\[
a_r=-\bar b_r-C\varepsilon_r,
\]
\[
S_{p,r}=P_pa_r(y')-a_r(y),
\]
and the sourced equation is equivalent to
\[
\delta_r=a_r+h_r,
\]
with \(h_r\) parallel.

`A4DActiveSpanExtensionIndependence.lean` already removes arbitrary
full-fibre extension freedom: only the action on actual affine increments is
used downstream.

`A4DLabelledEndpointLocalityPassport.lean` keeps endpoint descent separate:
endpoint locality of a specified labelled transport is equivalent to trivial
labelled holonomy for that transport. This memo does not replace labelled
paths by endpoints.

The post-source selector itself is the research rule of PR #120:
\[
h_o^*=-\operatorname{Proj}^{h_{n(o)}}_{\mathcal H_o}\bar a_o.
\]
This rule is pressure-tested literally; it is not replaced by a new selector.

No statement below is called newly Lean-owned.

---

## 2. Finite topology and continuity contract

Everything is finite-dimensional and at fixed archive size.

Use the counting inner product on
\[
E_{\rm lab}=\mathbb R^{\mathrm{Role}}.
\]
Choose any fixed positive coordinate norm on each finite output fibre for
continuity statements. Different such norms give the same finite-dimensional
topology. The observer form \(h_n\) is used only where the existing selector
requires it.

For a continuous parameter family, assume
\[
\mathcal B_t\to\mathcal B_0,\qquad
\mathcal S_t\to\mathcal S_0
\]
in operator norm. For archive backgrounds this follows sitewise from
continuous link shifts/linear maps and continuous coframe data.

For a subspace \(W_t\) of a fixed finite-dimensional space, “subspace
continuity” means continuity of its orthogonal projector, equivalently the
usual gap/Grassmannian topology on a fixed-rank stratum.

This distinction matters. Continuous generators do not imply continuous image
subspaces across a rank jump.

---

## 3. Lost-direction theorem

Let
\[
P_t:=P_{H_t},\qquad H_t=(\ker\mathcal B_t)^\perp.
\]

### Theorem 1 — cluster projector decomposition

Take any sequence \(t_n\to0\). Projectors are bounded, so after passing to a
subsequence,
\[
P_{t_n}\to P_*.
\]
Since each \(P_{t_n}\) is an orthogonal projector, so is \(P_*\).

The identity
\[
\mathcal B_tP_t=\mathcal B_t
\]
passes to the limit:
\[
\mathcal B_0P_*=\mathcal B_0.
\]
Hence
\[
\operatorname{im}(I-P_*)\subseteq K_0.
\]
Because \(P_*\) is orthogonal,
\[
H_0=K_0^\perp\subseteq\operatorname{im}P_*.
\]

Define
\[
\boxed{
W_*:=\operatorname{im}P_*\cap K_0.
}
\]
Then orthogonality gives the exact decomposition
\[
\boxed{
\operatorname{im}P_*=H_0\oplus W_*,
}
\]
and therefore
\[
\boxed{
P_*=P_{H_0}+P_{W_*}.
}
\]

This is the precise lost coefficient space for that approach.

### Theorem 2 — lost-direction jump formula

Since
\[
C_t=\mathcal S_tP_t,
\]
along the same subsequence
\[
C_{t_n}\to\mathcal S_0P_*.
\]
Therefore
\[
\boxed{
\lim_{n\to\infty}C_{t_n}-C_0
=
\mathcal S_0P_{W_*}.
}
\tag{3.1}
\]

Because
\[
D_t=\mathcal S_t-C_t
\]
and \(\mathcal S_t\to\mathcal S_0\),
\[
\boxed{
D_{t_n}\to D_0
\iff
C_{t_n}\to C_0.
}
\tag{3.2}
\]

Consequently
\[
\boxed{
C_{t_n}\to C_0
\iff
D_{t_n}\to D_0
\iff
\mathcal S_0(W_*)=0.
}
\tag{3.3}
\]

This proves the formula requested by PR #128 without assuming an analytic
one-parameter curve. It is sequential and applies to arbitrary approaches.

---

## 4. Exact all-sequence criterion

For a specified admissible family \(\mathfrak F\) through the background,
let
\[
\mathscr P_0(\mathfrak F)
\]
be the set of all cluster projectors \(P_*\) obtained from all sequences in
\(\mathfrak F\) converging to the point. Define
\[
W(P_*):=\operatorname{im}P_*\cap K_0
\]
and the total reachable lost space
\[
\boxed{
L_0(\mathfrak F)
:=
\operatorname{span}\{W(P_*):P_*\in\mathscr P_0(\mathfrak F)\}.
}
\tag{4.1}
\]

### Theorem 3 — familywise continuity

\[
\boxed{
C,D\text{ are continuous at }0\text{ along }\mathfrak F
\iff
\mathcal S_0(L_0(\mathfrak F))=0.
}
\tag{4.2}
\]

**Proof.** Necessity is (3.3) for every cluster projector. For sufficiency,
every sequence has a projector-convergent subsequence, every such cluster has
the unique action limit \(C_0\), and finite-dimensional compactness then
forces the whole sequence to converge to \(C_0\). Equation (3.2) gives \(D\).

This is strictly weaker than \(M_0=0\) when the admissible family cannot expose
all kernel directions.

---

## 5. Universal continuity iff \(M_0=0\)

PR #128 recorded \(M_0=0\) as a sufficient condition. It is exactly sharp
when “continuity” quantifies over arbitrary nearby synthesis pairs.

### Theorem 4 — universal local criterion

At a fixed point \((\mathcal B_0,\mathcal S_0)\),
\[
\boxed{
\forall(\mathcal B_n,\mathcal S_n)\to(\mathcal B_0,\mathcal S_0),\
C_n\to C_0
\iff
M_0=\mathcal S_0(K_0)=0.
}
\tag{5.1}
\]
The same equivalence holds with \(D\) in place of \(C\).

**Sufficiency.** Every possible lost space lies in \(K_0\), so \(M_0=0\)
kills every term \(\mathcal S_0P_{W_*}\) in (3.1).

**Necessity.** Suppose \(M_0\ne0\). Choose
\[
0\ne w\in K_0,\qquad \mathcal S_0w\ne0,
\]
and normalize \(w\). Because \(w\in\ker\mathcal B_0\), \(\mathcal B_0\) is
not full rank, so choose
\[
u\notin\operatorname{im}\mathcal B_0.
\]
Let \(\lambda(c)=\langle w,c\rangle\) on the coefficient space and define
\[
\mathcal B_\epsilon
=
\mathcal B_0+\epsilon\,u\otimes\lambda,
\qquad
\mathcal S_\epsilon=\mathcal S_0.
\]
For every \(\epsilon\ne0\),
\[
\ker\mathcal B_\epsilon
=
K_0\cap w^\perp,
\]
hence
\[
H_\epsilon=H_0\oplus\mathbb Rw.
\]
Therefore
\[
C_\epsilon
=
C_0+\mathcal S_0P_{\mathbb Rw}
\]
for every nonzero \(\epsilon\), which cannot converge to \(C_0\).

Thus \(M_0=0\) is not merely a convenient graph hypothesis. It is the exact
criterion for robustness against **all** infinitesimal ways of activating
previous kernel directions.

### Restricted-family negative

\(M_0=0\) is not necessary along a specified family. Take
\[
\mathcal B_t\equiv0,\qquad
\mathcal S_t\equiv\mathcal S_0\ne0.
\]
Then
\[
C_t\equiv0,\qquad D_t\equiv\mathcal S_0
\]
are continuous while
\[
M_0=\operatorname{im}\mathcal S_0\ne0.
\]

This distinction between universal and familywise continuity is mandatory.

---

## 6. Eleven properties are genuinely different

The requested continuity notions separate as follows.

### 6.1 Relation \(\mathscr R_t\)

Let
\[
T_t=(\mathcal B_t,\mathcal S_t):
E_{\rm lab}\to V\oplus V,
\qquad
\mathscr R_t=\operatorname{im}T_t.
\]
For continuous \(T_t\),
\[
\boxed{
\mathscr R_t\text{ is gap-continuous at }0
\iff
\operatorname{rank}T_t
\text{ is locally constant at }0.
}
\tag{6.1}
\]

Constant rank gives continuity of the range projector. Conversely projectors
of different rank cannot converge in operator norm.

### 6.2 Active output subspace \(U_t\)

\[
U_t=\operatorname{im}\mathcal B_t
\]
is gap-continuous iff \(\operatorname{rank}\mathcal B_t\) is locally constant.

### 6.3 Coefficient projector \(P_{H_t}\)

The same exact condition holds:
\[
\boxed{
P_{H_t}\text{ continuous}
\iff
\operatorname{rank}\mathcal B_t\text{ locally constant}.
}
\tag{6.2}
\]

Thus every genuine rank drop makes the active-space/projector stage
discontinuous. That does **not** imply downstream \(C,D\) are discontinuous.

### 6.4 Correlated action \(C_t\)

This is controlled by the lost-direction criterion (4.2), not by rank alone.

### 6.5 Residual \(D_t\)

Because \(D_t=\mathcal S_t-C_t\), it has exactly the same continuity criterion
as \(C_t\).

### 6.6 Normalized graph operator \(J_t\)

On \(U_t\),
\[
J_t(\mathcal B_tc)=\mathcal S_tc,\qquad c\in H_t.
\]
Its operator norm is
\[
\boxed{
\|J_t\|
=
\sup_{0\ne c\in H_t}
\frac{\|\mathcal S_tc\|}{\|\mathcal B_tc\|}.
}
\tag{6.3}
\]

Local boundedness is therefore equivalent to a uniform inequality
\[
\|\mathcal S_tc\|\le K\|\mathcal B_tc\|
\quad(c\in H_t).
\]
A uniform lower singular-value bound for
\(\mathcal B_t|_{H_t}\), together with bounded \(\mathcal S_t\), is sufficient
but not necessary.

The exact control
\[
\mathcal B_t\varepsilon_A=t^2e_A,\qquad
\mathcal S_t\varepsilon_A=te_B
\]
has
\[
J_t(e_A)=t^{-1}e_B
\]
for \(t\ne0\), but
\[
C_t\varepsilon_A=te_B\to0=C_0\varepsilon_A.
\]
Thus bounded \(J\) is not necessary for downstream continuity.

On a neighborhood of genuinely constant \(\operatorname{rank}\mathcal B_t\),
the smallest nonzero singular value stays bounded away from zero, so \(J_t\)
is locally bounded for continuous \(\mathcal S_t\).

### 6.7 Seed \(a_t\)

For a continuous archive background, \(L^{-1}\) and \(\bar b\) are continuous.
Hence
\[
a_{t,r}(y)
=
-\bar b_{t,r}(y)-C_t(y)\varepsilon_r.
\]
Therefore operator continuity of \(C_t(y)\) at every site implies continuity
of every seed component.

For one selected Role only the corresponding column of \(C_t\) is needed.

The converse at operator level is not claimed from one Role.

### 6.8 Path source

For every fixed finite labelled path,
\[
S_{t,p,r}
=
P_{t,p}a_{t,r}(y')-a_{t,r}(y).
\]
If \(A_t\) and \(a_t\) are continuous, then \(S_{t,p,r}\) is continuous.

The converse fails: a discontinuous seed component which changes by a
parallel section can cancel from every sourced difference.

### 6.9 Affine solution space

Fix a basepoint and finite fundamental loop generators. Let
\[
F_t:V_o\to V_o^{\,m},
\qquad
F_t h=((P_{\gamma_i,t}-I)h)_i.
\]
Then
\[
\mathcal H_t=\ker F_t
\]
is the basepoint space of parallel residuals.

The global sourced solution set is an affine space
\[
\mathcal A_t=a_t+\operatorname{Par}_t.
\]
In the affine-Grassmannian sense, its direction subspace is continuous exactly
when
\[
\dim\mathcal H_t
\]
is locally constant. With that condition, affine-space continuity additionally
requires continuity of the translation class of \(a_t\) modulo
\(\operatorname{Par}_t\).

A kernel-dimension jump makes the full affine solution space discontinuous
even if one chosen solution stays continuous.

### 6.10 Selected \(\delta_t\)

This requires both the seed behavior and the actual PR #120 kernel projection.
The exact criterion is derived in §§8–9.

### 6.11 Final \(\kappa_t\)

For a continuous background,
\[
\kappa_t(x,r)
=
\tau_t(x,r)+L_{t,x,r}\delta_{t,r}(x+r),
\]
where \(\tau_t\) and \(L_t\) are continuous and \(L_t\) is invertible.

Hence
\[
\boxed{
\delta_t\text{ continuous}
\iff
\kappa_t\text{ continuous}.
}
\tag{6.4}
\]
The reverse implication uses
\[
\delta_{t,r}(x+r)
=
L_{t,x,r}^{-1}\bigl(\kappa_t(x,r)-\tau_t(x,r)\bigr).
\]

Therefore the requested case “continuous \(\delta\), discontinuous
\(\kappa\)” does not exist under the task's continuous-background
hypothesis.

---

## 7. Source-continuity propagation theorem

### Theorem 5

Assume on the finite archive:

1. every link \(A_t(x,r)\) and raw coframe \(e_t\) varies continuously;
2. at every site the lost-direction condition (4.2) holds for the admitted
   approaches.

Then:

- \(C_t,D_t\) are continuous;
- every \(\bar b_{t,r}\) and seed \(a_{t,r}\) is continuous;
- for every fixed labelled path, \(P_{t,p}\) and \(S_{t,p,r}\) are continuous.

No boundedness of \(J_t\) is required.

This is the exact propagation from the local coefficient split to the sourced
equations. It stops before the parallel-kernel selector because that kernel
can change independently through holonomy.

---

## 8. Literal PR #120 selector and its exact formula

Fix one Role \(r\) and suppress that index in this section. Apply the same formula Role-by-Role. Fix once and for all the selection data used by PR #120:

- basepoint \(o\);
- one labelled path \(p_y:o\to y\) for each site;
- observer field \(n_t\), hence positive form \(h_t=h_{n_t(o)}\).

Write
\[
P_{y,t}:V_y\to V_o
\]
for transport along \(p_y\). Define
\[
m_t
=
\frac1{|X|}
\sum_yP_{y,t}a_t(y).
\]
Let
\[
\mathcal H_t
=
\bigcap_{\gamma:o\to o}\operatorname{Fix}P_{\gamma,t}
=
\ker F_t
\]
and let
\[
Q_t=\operatorname{Proj}^{h_t}_{\mathcal H_t}.
\]

The PR #120 minimizer is
\[
h^*_{o,t}=-Q_tm_t.
\]
Parallel extension along the chosen paths gives
\[
h_t^*(y)=P_{y,t}^{-1}h^*_{o,t}.
\]
Hence the selected diagonal is exactly
\[
\boxed{
\delta_t(y)
=
a_t(y)-P_{y,t}^{-1}Q_tm_t.
}
\tag{8.1}
\]

This identity is the stability interface. No new selector has been inserted.

---

## 9. Kernel-projector continuity and the full selected criterion

### 9.1 Fixed-space projector

Because the finite generator matrix \(F_t\) is continuous,
\[
\boxed{
Q_t\text{ is continuous at }0
\iff
\dim\mathcal H_t\text{ is locally constant at }0.
}
\tag{9.1}
\]
Here \(Q_t\) is the orthogonal projection for a continuously varying positive
metric \(h_t\).

Equivalently, for a fixed coordinate inner product, the zero eigenspace of
\[
F_t^\dagger F_t
\]
has locally constant multiplicity. On a constant-rank neighborhood this is
equivalent to a local positive gap separating zero from the nonzero singular
spectrum.

A “spectral gap at the single point \(t=0\)” is not enough: a positive
singular value may tend to zero and become a new kernel direction at the
limit.

### 9.2 Cluster geometry at a kernel gain

For any sequence, pass to a subsequence with
\[
Q_{t_n}\to Q_*.
\]
Then \(Q_*\) is the \(h_0\)-orthogonal projector onto a limit fixed space
\[
\mathcal H_*\subseteq\mathcal H_0.
\]
The inclusion is forced by \(F_{t_n}Q_{t_n}=0\to F_0Q_*=0\).

Thus kernel dimension can only **gain** at the limiting background relative
to a fixed-rank approach. Write
\[
\mathcal H_0
=
\mathcal H_*\oplus_{h_0}W_{\rm gain}.
\]

### 9.3 Source-stable selector criterion

If \(a_t\to a_0\), then \(m_t\to m_0\), and (8.1) gives
\[
\boxed{
\delta_{t_n}\to\delta_0
\iff
Q_*m_0=Q_0m_0.
}
\tag{9.2}
\]
Equivalently,
\[
\boxed{
\operatorname{Proj}^{h_0}_{W_{\rm gain}}m_0=0.
}
\tag{9.3}
\]

Thus constant fixed-kernel dimension is sufficient but not necessary for the
selected value.

### 9.4 Full joint-cluster criterion

The preceding statement assumed a continuous seed. The exact selected-output
criterion does not need that assumption.

The seed remains bounded because \(C_t=\mathcal S_tP_{H_t}\) is bounded.
For any approaching sequence, take a joint convergent subsequence
\[
a_{t_n}\to a_*,
\qquad
Q_{t_n}\to Q_*.
\]
Since \(P_{y,t}\to P_{y,0}\),
\[
m_{t_n}\to
m_*:=
\frac1{|X|}
\sum_yP_{y,0}a_*(y).
\]
Equation (8.1) gives the cluster selected field
\[
\delta_*(y)
=
a_*(y)-P_{y,0}^{-1}Q_*m_*.
\]

Therefore:

### Theorem 6 — exact selected readout criterion

The selected diagonal is continuous at the background iff for **every**
joint cluster \((a_*,Q_*)\) induced by every approaching sequence,
\[
\boxed{
a_*(y)-a_0(y)
=
P_{y,0}^{-1}
\bigl(Q_*m_*-Q_0m_0\bigr)
\quad
\text{for every site and Role}.
}
\tag{9.4}
\]

Under continuous \(A,e\), the same condition is necessary and sufficient for
the pair
\[
(\delta,\kappa)
\]
by (6.4).

Equation (9.4) exposes the only possible cancellation: a seed jump can be
hidden by the existing selector only when the entire jump is exactly a
parallel correction produced by the limiting kernel projection. Generic
lost-direction jumps are not of this form.

This is the promised necessary-and-sufficient criterion for the current
selected finite readout.

---

## 10. Observer metric and frame covariance

The fixed-space \(\mathcal H_t\) is determined by transport alone and is
observer-independent.

If \(\dim\mathcal H_t\) is locally constant, any continuously varying positive
observer metric produces a continuous \(Q_t\). Thus the robust constant-rank
selector criterion does not depend on the observer.

At a dimension jump, the exceptional cancellation
\[
Q_*m_0=Q_0m_0
\]
can depend on the observer metric because orthogonal projection onto a proper
subspace depends on that metric. When \(Q_0=I\), the condition reduces to
\(m_0\in\mathcal H_*\), which is metric-independent.

PR #120's frame covariance survives the continuity analysis. Under a
continuous pure-linear frame \(g_t\),
\[
m'_t=g_{o,t}m_t,\qquad
\mathcal H'_t=g_{o,t}\mathcal H_t,
\]
and observer congruence gives
\[
Q'_t=g_{o,t}Q_tg_{o,t}^{-1}.
\]
Thus (8.1), (9.2) and (9.4) conjugate covariantly. Stability is not obtained
by fixing a preferred frame.

---

## 11. Mandatory \(L=3\) killing witness

Let \(j=x_A\),
\[
f=(1,-2,1),
\qquad
L_{x,r}=I,
\]
\[
b_{x,A}(t)=t f(j)e_A,
\qquad b_{x,s}=0\quad(s\ne A),
\]
\[
v_A(x)=e_A+f(j)e_B,
\qquad v_s(x)=e_s\quad(s\ne A).
\]

The raw coframe matrix has columns
\[
(e_A+f(j)e_B,e_B,e_C,e_D),
\]
so it is a shear with determinant one.

The shift cycle is the forward gradient of
\[
(0,t,-t)e_A,
\]
hence its affine period is zero. Linear transport is identity, so the full
affine holonomy is trivial.

With
\[
d_j=f(j)-f(j-1)=(0,-3,3),
\]
\[
\Delta b_A=t\,d_je_A,
\qquad
\Delta v_A=d_je_B.
\]

At the two sites with \(d_j\ne0\), for every \(t\ne0\),
\[
H_t=\mathbb R\varepsilon_A,
\qquad
C_t\varepsilon_A=d_je_B,
\qquad
D_t=0.
\]
At \(t=0\),
\[
H_0=0,\qquad C_0=0,\qquad
D_0\varepsilon_A=d_je_B.
\]

Thus
\[
W_*=\mathbb R\varepsilon_A
\]
and
\[
\mathcal S_0(W_*)=\mathbb R e_B\ne0.
\]
This is exactly the failure predicted by (3.3).

### Relation stays continuous

At a nonzero-\(d_j\) site the pair relation is the line
\[
\operatorname{span}\{(t e_A,e_B)\}
\subset V\oplus V.
\]
Its dimension is one for all \(t\), and it converges to
\[
\operatorname{span}\{(0,e_B)\}.
\]
So the relation is continuous even though \(U_t\), \(P_{H_t}\), \(C_t\) and
\(D_t\) are not.

This is the requested separation between relation continuity and selected
action continuity.

### Seed and source

For \(t\ne0\),
\[
a_A(j)
=
-t f(j-1)e_A-d_je_B.
\]
At \(t=0\),
\[
a_A(j)=0.
\]
The \(e_B\) pattern
\[
-d_j=(0,3,-3)
\]
is nonparallel. Hence a basic A-path source also jumps. The failure is already
present at the correlated-action/seed/source stage; it is not created by the
post-source kernel selector.

The transported mean is zero for every \(t\). Since transport is trivial,
\[
Q_t=I
\]
for every \(t\), so the selector contributes no compensating jump.

Therefore
\[
\delta_A(t)=a_A(t)\quad(t\ne0),
\qquad
\delta_A(0)=0.
\]

Finally,
\[
\kappa_A(t;x)=0\qquad(t\ne0),
\]
whereas
\[
\kappa_A(0;x)
=
(f(j+1)-f(j))e_B
=
(-3,3,0)e_B.
\]
In particular,
\[
\boxed{
\kappa_A(0;0)=-3e_B,
\qquad
\kappa_A(t;0)=0\quad(t\ne0).
}
\tag{11.1}
\]

No theorem requiring only relation continuity, raw-solder nondegeneracy,
trivial affine holonomy, endpoint descent, or smooth generators can exclude
this witness.

---

## 12. Benign rank drops and unbounded \(J\)

A rank drop is not itself a physical obstruction.

### 12.1 \(M_0=0\) rank drop

If
\[
\mathcal S_t=T\mathcal B_t
\]
for a continuous fixed \(T\), then
\[
M_t=0,\qquad C_t=\mathcal S_t,\qquad D_t=0
\]
on every rank stratum, including where rank drops.

This is the abstract reason the exact translation-gauge rank drop is benign:
the solder synthesis kills every coefficient relation of the affine synthesis.

### 12.2 Unbounded normalized graph

The control
\[
\mathcal B_t\varepsilon_A=t^2e_A,
\qquad
\mathcal S_t\varepsilon_A=te_B
\]
has
\[
M_t=0
\]
for every \(t\), and
\[
C_t\varepsilon_A=te_B\to0.
\]
But for \(t\ne0\),
\[
J_t(e_A)=t^{-1}e_B.
\]

Thus:

- the relation image itself loses dimension at \(0\);
- \(P_{H_t}\) jumps;
- \(J_t\) is unbounded;
- \(C,D\) and the sourced action can nevertheless remain continuous.

No stability criterion may require bounded \(J\).

---

## 13. Continuous source, discontinuous selector: independent witness

The second seam can fail on a literal finite archive with no source-rank
problem.

Use \(L=3\). Choose a spanning tree based at \(o\) which omits one positive
A-labelled closing edge. Put identity linear transport on every tree edge and
on every other edge, and put on the omitted closing edge
\[
G_t=
\operatorname{diag}(1,1+t,1,1),
\]
which is invertible for \(t\) near zero. The fundamental A-loop then has
holonomy \(G_t\).

For the selected Role \(C\), set every C-labelled affine shift to
\[
b_{x,C}=-e_B,
\]
with identity C-linear transport, and set the other affine shifts to zero.
Take the raw coframe \(e=0\).

Then every affine-shift increment is zero:
\[
\mathcal B_t=0.
\]
Hence
\[
C_t=0
\]
for every \(t\), irrespective of the solder residual map. For Role \(C\),
\[
\bar b_C=-e_B,\qquad
a_C=e_B
\]
at every site. The seed is therefore constant and continuous.

Choose the tree paths used by the PR #120 mean. They avoid the single closing
edge, so every tree transport on \(e_B\) is identity and
\[
m_t=e_B.
\]

Every tree-edge source is zero. The only new fundamental-loop source is
\[
(G_t-I)e_B=te_B,
\]
which is continuous and vanishes at the limit.

For \(t\ne0\),
\[
\mathcal H_t
=
\operatorname{span}(e_A,e_C,e_D),
\]
while
\[
\mathcal H_0=V.
\]
With the identity observer metric,
\[
Q_te_B=0\quad(t\ne0),
\qquad
Q_0e_B=e_B.
\]

Hence
\[
h_t^*=0\quad(t\ne0),
\qquad
h_0^*=-e_B,
\]
and
\[
\delta_{C,t}=e_B\quad(t\ne0),
\qquad
\delta_{C,0}=0.
\]

The earliest discontinuity is exactly the fixed-kernel projector /
post-source selector. The seed and all generating path sources are continuous.

This proves that source continuity does not imply selected-readout continuity.

The converse overstatement also fails: if the transported seed mean is zero,
the same kernel-dimension jump can leave the selected \(\delta\) continuous.
Constant kernel dimension is therefore sufficient for robust selector
continuity, not necessary for one particular mean.

## 14. Spectral formulation of the selector seam

Choose finitely many fundamental labelled loop generators and stack
\[
F_t=
\begin{bmatrix}
P_{\gamma_1,t}-I\\
\vdots\\
P_{\gamma_m,t}-I
\end{bmatrix}.
\]
Then
\[
\mathcal H_t=\ker F_t.
\]

For a fixed coordinate metric,
\[
K_t=F_t^\dagger F_t\ge0.
\]
The kernel selector is the zero-spectral projector of \(K_t\), modified by the
continuously varying observer metric for the actual PR #120 minimization.

The exact robust condition is
\[
\operatorname{rank}F_t
\text{ locally constant}.
\]
A convenient quantitative sufficient formulation is a neighborhood with:

- fixed multiplicity of the zero eigenvalue;
- a uniform \(c>0\) such that every nonzero eigenvalue of \(K_t\) is at least
  \(c\).

In finite dimension these follow locally from constant rank and continuity.
They are not necessary for a particular selected value because (9.2) can hold
even when \(Q_t\) jumps.

---

## 15. Remediation audit A — restrict admissible backgrounds

The restrictions have different jobs.

| Hypothesis | What it guarantees | Is it minimal? |
|---|---|---|
| constant \(\operatorname{rank}\mathcal B_t\) | \(U_t,P_{H_t},C_t,D_t\) continuous; local boundedness of \(J_t\) | sufficient but stronger than needed for \(C,D\) |
| lost-direction annihilation \(\mathcal S_0(L_0(\mathfrak F))=0\) | exact continuity of \(C,D\) for the specified family | necessary and sufficient |
| \(M_0=0\) | \(C,D\) continuous under every nearby perturbation | necessary and sufficient for universal robustness |
| constant pair rank \(\operatorname{rank}(\mathcal B_t,\mathcal S_t)\) | relation subspace continuity | neither sufficient nor necessary for \(C,D\) continuity |
| constant \(\dim\mathcal H_t\) | continuity of the kernel projector \(Q_t\) | exact for projector continuity, stronger than needed for one selected value |
| selector cluster condition (9.2) | continuity of selected value once source is stable | necessary and sufficient |
| full joint-cluster condition (9.4) | continuity of the full selected \((\delta,\kappa)\) | necessary and sufficient |

The mandatory witness has constant pair rank but violates lost-direction
annihilation. The \(t^2/t\) witness has continuous \(C\) while pair rank
drops. Thus pair-rank and action continuity cannot replace one another.

A clean robust admissible class is:

1. lost-direction annihilation at every site;
2. locally constant parallel-kernel dimension;
3. continuous observer field and fixed selection paths.

This is sufficient for a continuous selected readout and does not require
full rank or bounded \(J\).

---

## 16. Remediation audit B — change canonical representative

There is a no-go inside the current active-span architecture.

Let a proposed correlated action
\[
\widehat C(\mathcal B,\mathcal S):
E_{\rm lab}\to V
\]
satisfy both:

1. **active-factor condition:** it factors through actual affine increments,
   equivalently
   \[
   \ker\mathcal B\subseteq\ker\widehat C;
   \]
   in particular \(\widehat C=0\) when \(\mathcal B=0\);
2. **strict graph calibration:** whenever
   \[
   \ker\mathcal B\subseteq\ker\mathcal S,
   \]
   it reproduces the strict correlated action
   \[
   \widehat C=\mathcal S.
   \]

These are weaker than the full requested package of exact gauge calibration,
frame covariance, label symmetry, pure-shift/Nyquist/corner controls and
active-span extension independence.

Apply them to the mandatory family at a site with \(d_j\ne0\).

For every \(t\ne0\) the pair is a graph, so
\[
\widehat C_t\varepsilon_A=d_je_B.
\]
At \(t=0\), \(\mathcal B_0=0\), so active factorization forces
\[
\widehat C_0=0.
\]

Therefore:

\[
\boxed{
\text{No correlated representative satisfying active factorization and exact
graph calibration can be universally continuous across a surviving lost
direction.}
}
\tag{16.1}
\]

A continuous replacement must do at least one of:

- restrict the allowed family;
- stop calibrating the graph pointwise;
- stop factoring only through current active increments;
- carry additional history/stratum data.

The last option is genuinely a new datum. It cannot be described as a harmless
change of representative.

---

## 17. Remediation audit C — quotient

For a same-fibre quotient \(q_y:V_y\to\bar V_y\) with kernel \(W_y\), the
landed pressure memo already gives the exact relation condition
\[
\boxed{
\mathcal S_y(\mathcal B_y^{-1}W_y)\subseteq W_y.
}
\tag{17.1}
\]
Transport additionally requires a parallel family \(W_y\), and endpoint
descent requires loop coinvariants to lie in it. Finite saturation \(W^*\)
constructs the smallest simultaneous algebraic quotient.

Continuity adds another requirement. If a linear quotient is to remove a
selected-readout jump, its kernel must contain every jump direction.

For a family, define the readout jump span
\[
J_0
=
\operatorname{span}\{
(\delta_*,\kappa_*)-(\delta_0,\kappa_0)
:\text{all cluster readouts}
\}.
\]
A fixed linear quotient makes the readout continuous iff it kills \(J_0\).

### Mandatory conflict

For (11.1), the mismatch jump contains \(e_B\). Therefore every linear
quotient curing that witness must satisfy
\[
q(e_B)=0.
\]

But the mandatory \(L=3\) corner control has raw mismatch exactly
\[
\kappa_{\rm corner}=e_B.
\]
The same quotient sends this required response to zero.

Hence
\[
\boxed{
\text{No fixed linear quotient can cure the mandatory rank-transition jump
while preserving the mandatory L=3 corner distinction.}
}
\tag{17.2}
\]

This is stronger than observing that the zero quotient is useless.

A background-dependent quotient would itself require a continuously selected
kernel subbundle plus the relation/transport conditions above. That is extra
structure, not a cure supplied by the present theory.

---

## 18. Remediation audit D — weaken the output

A coarse linear readout
\[
q:(\delta,\kappa)\mapsto\bar O
\]
can be continuous even when the full readout is not.

The exact minimal condition is
\[
\boxed{
J_0\subseteq\ker q.
}
\tag{18.1}
\]
Thus coarse continuity is always a statement about which cluster differences
are forgotten.

For the mandatory witness,
\[
\mathbb Re_B\subseteq\ker q
\]
is necessary. Such a readout forgets the \(e_B\) corner distinction and cannot
be called the full classical finite interface.

The relation \(\mathscr R\) itself is a coarser continuous object in the
mandatory witness, but it does not retain the selected diagonal/mismatch
observables. This is precisely why relation continuity and readout continuity
must remain separate rows.

---

## 19. Mandatory control audit

### Flat

\[
\mathcal B=\mathcal S=0,\qquad
C=D=0,\qquad
a=\delta=\kappa=0.
\]
Rank zero is stable for the constant flat family.

### Constant pure affine shift

\[
\mathcal B=\mathcal S=0,\qquad
a=-b.
\]
The seed is parallel; the PR #120 kernel selector chooses \(h=b\), giving
\[
\delta=0,\qquad\kappa=b.
\]
Full rank is unnecessary.

### Exact translation gauge

On the exact chart,
\[
\mathcal S=T\mathcal B
\]
with the prescribed chart comparison. Hence \(M=0\), \(C=\mathcal S\),
\(D=0\), including rank-degenerate sites.

### \(L=3\) exact-gauge rank drop

Use the landed cycle
\[
b_A=(3,3,-6)e_B,\qquad
v_A=e_A-(3,3,-6)e_B.
\]
Then
\[
\Delta b_A=(9,0,-9)e_B,
\qquad
\Delta v_A=(-9,0,9)e_B=\eta\,\Delta b_A.
\]
The middle site has rank zero, but
\[
M=0,\qquad C=\mathcal S,\qquad D=0
\]
at all three sites. The selected diagonal is
\[
(15,-3,-12)e_B,
\]
and the exact mismatch is
\[
\kappa=0
\]
edge by edge. This is the nearest positive control to the mandatory bad rank
transition: rank loss is harmless when the limiting solder synthesis kills the
lost directions.

### Mandatory discontinuity family

Fully reproduced in §11. It has trivial affine holonomy and invertible raw
solder but violates lost-direction annihilation.

### \(L=2\) Nyquist

The flat-linear source has \(a=\delta=0\), so the raw response
\[
(+4,-4)e_A
\]
is retained. A quotient killing \(e_A\) would erase it.

### \(L=3\) corner/curl

The raw corner response
\[
e_B
\]
is retained. This supplies the direct contradiction to quotienting away the
mandatory \(e_B\) jump.

### Constant harmonic coframe

The source is zero and the raw harmonic geometry remains in the coframe.
The post-source selector chooses zero added parallel diagonal. This is a
kernel-selection control, not a rank-transition control.

### Duplicate increments

For
\[
\mathcal B=(e_A,e_A,0,0),
\qquad
\mathcal S=(e_B,-e_B,0,0),
\]
the endpoint is non-graph:
\[
M\ne0.
\]
As a constant family it nevertheless has continuous \(C,D\). This is another
literal witness that \(M_0=0\) is not necessary for restricted-family
continuity.

### Nontrivial linear holonomy

Nontrivial holonomy does not itself destroy continuity. If its common fixed
space keeps constant dimension, \(Q_t\) is continuous. A dimension change of
that fixed space is the relevant selector seam.

### Trivial affine holonomy

The mandatory witness already has it. It is not a cure for the local rank
seam.

### Rank-zero and rank-one active spans

Both are admissible pointwise. Stability depends on how their coefficient
subspaces are approached and on the lost solder images, not on an absolute
rank threshold.

---

## 20. Classification matrix

| Stratum / family | Relation | \(U,P_H\) | \(C,D\) | \(J\) | source | selector | selected \((\delta,\kappa)\) | earliest failure |
|---|---|---|---|---|---|---|---|---|
| constant-rank graph family | continuous if pair rank constant (automatic here when graph rank data stay constant) | continuous | continuous, \(C=S,D=0\) | locally bounded | continuous | continuous if fixed-kernel criterion passes | continuous under same selector condition | none before selector |
| rank drop, \(M_0=0\) | may fail if pair rank drops | discontinuous | continuous for every approach | may diverge | continuous | independent holonomy criterion | continuous if selector criterion passes | active subspace only |
| rank drop, \(M_0\ne0\), actual lost directions killed | may fail | discontinuous | continuous along that family | no general bound | continuous | independent holonomy criterion | continuous if selector criterion passes | active subspace only |
| rank drop, surviving lost direction | can remain continuous | discontinuous | discontinuous | irrelevant to diagnosis | generally discontinuous | may be perfectly continuous | generally discontinuous; exact cluster test (9.4) decides cancellation | correlated action \(C,D\) |
| \(B=t^2,\ S=t\) | discontinuous (pair rank 1→0) | discontinuous | continuous | unbounded \(1/t\) | continuous | can be fixed | continuous if fixed | normalized \(J\) only, not readout |
| continuous source, holonomy fixed-space jump | continuous local source data | can be constant | continuous | can be bounded | continuous | discontinuous | discontinuous for nonzero gained mean component | post-source selector |
| kernel jump with zero transported mean | continuous | independent | continuous | independent | continuous | projector discontinuous | selected value can remain continuous | affine solution space / projector, not selected value |
| continuous \(\delta\), discontinuous \(\kappa\) | — | — | — | — | — | — | impossible for continuous \(A,e\) by invertible edge formula | no such stratum |
| trivial holonomy | no implication for rank seam | no implication | no implication | no implication | no implication | \(Q=I\) while triviality persists | rank seam can still break it | mandatory witness |
| nontrivial holonomy with constant fixed-kernel dimension | no implication for rank seam | no implication | no implication | no implication | continuous if seed is | continuous | can be continuous | none forced by holonomy |

No row identifies relation continuity, graphification, endpoint descent,
bounded \(J\), or selected stability.

---

## 21. Hostile implication audit

The following tempting implications are false.

\[
\mathscr R_t\text{ continuous}
\;\not\Rightarrow\;
C_t\text{ continuous}
\]
by the mandatory witness.

\[
C_t\text{ continuous}
\;\not\Rightarrow\;
\mathscr R_t\text{ continuous}
\]
by the \(t^2/t\) witness.

\[
P_{H_t}\text{ discontinuous}
\;\not\Rightarrow\;
C_t\text{ discontinuous}
\]
by every killed-lost-direction example.

\[
J_t\text{ unbounded}
\;\not\Rightarrow\;
C_t\text{ discontinuous}
\]
again by \(t^2/t\).

\[
M_0\ne0
\;\not\Rightarrow\;
\text{familywise discontinuity}
\]
by the constant vertical family and duplicate-generator family.

\[
\text{source continuous}
\;\not\Rightarrow\;
\text{selected }\delta\text{ continuous}
\]
by §13.

\[
\dim\mathcal H_t\text{ jumps}
\;\not\Rightarrow\;
\text{selected }\delta\text{ jumps}
\]
when the transported mean has no gained-kernel component.

\[
\text{trivial affine holonomy}
\;\not\Rightarrow\;
\text{selected stability}
\]
by §11.

\[
\text{constant pair rank}
\;\not\Rightarrow\;
C,D\text{ continuity}
\]
again by §11.

These controls are why the final criterion must have both the local
lost-direction clause and the downstream fixed-kernel/cluster clause.

---

## 22. Minimal stable-interface passport

For a specified family of continuous finite backgrounds and the already-fixed
PR #120 basepoint/path/observer selection data, a robust easy-to-check
sufficient passport is:

\[
\boxed{
\begin{array}{l}
\text{(L) }\mathcal S_0(L_0(\mathfrak F))=0
\quad\text{at every site},\\[2mm]
\text{(K) }\dim\mathcal H_t
\quad\text{is locally constant}.
\end{array}}
\tag{22.1}
\]

(L) makes the correlated action, residual, seed and path source continuous.
(K) makes the post-source projection continuous. Then selected
\[
(\delta,\kappa)
\]
is continuous.

This passport does **not** require:

- rank four;
- invertible full \(J\);
- bounded \(J\) on a rank-changing family;
- trivial labelled holonomy;
- endpoint compression.

For an exact necessary-and-sufficient statement, replace (L)+(K) by the joint
cluster criterion (9.4). In the source-stable subclass, replace (K) by the
weaker exact applied-projector condition (9.2).

For universal robustness against arbitrary local synthesis perturbations,
(L) becomes exactly
\[
M_0=0.
\]

This is the completed hierarchy of stability assumptions.

---

## 23. What the terminal does and does not say

The terminal is

\[
\boxed{
\texttt{SELECTED-DIAGONAL-RANK-TRANSITION-CONTINUITY-CRITERION-CONSTRUCTED}.
}
\]

It is justified because:

1. (4.2) is necessary and sufficient for \(C,D\) on a specified family;
2. (5.1) is necessary and sufficient for universal local \(C,D\) robustness;
3. (9.4) is necessary and sufficient for the actual selected diagonal;
4. (6.4) transfers the same iff to the final mismatch;
5. the mandatory killing witness is explained exactly;
6. the independent selector-kernel failure is exhibited exactly;
7. the remediation options are classified, including a representative no-go
   and a quotient conflict with the corner control.

This does not prove a continuum classical limit, GR, QFT, stress dynamics or
finite graded dressing. It classifies stability of the already-constructed
finite selected interface.

---

## 24. Theorem-ready formalization handoff

A narrow WORKER can formalize the following package without reopening the
research.

### A. Lost-direction cluster theorem

For finite-dimensional real inner-product coefficient space:
if
\[
B_n\to B_0,\quad S_n\to S_0,\quad
P_{(\ker B_n)^\perp}\to P_*,
\]
prove:

1. \(P_*\) is an orthogonal projector;
2. \((\ker B_0)^\perp\le\operatorname{range}P_*\);
3. with
   \[
   W_*=\operatorname{range}P_*\cap\ker B_0,
   \]
   \[
   P_*=P_{H_0}+P_{W_*};
   \]
4.
   \[
   S_nP_{H_n}\to S_0P_*
   \]
   and the jump is \(S_0P_{W_*}\).

### B. All-sequence criterion

Package cluster projectors for an admitted sequence/family and prove:
\[
C_n\to C_0
\iff
\forall P_*,\ S_0(\operatorname{range}P_*\cap K_0)=0.
\]

### C. Universal theorem

Prove
\[
M_0=0
\iff
\text{continuity of }(B,S)\mapsto SP_{(\ker B)^\perp}
\text{ at }(B_0,S_0).
\]
For the reverse direction use the rank-one perturbation
\[
B_\epsilon=B_0+\epsilon u\otimes w^*.
\]

### D. Source propagation

Using the landed conditional sourced module, prove continuity algebraically
from \(C\) to:

- diagonal seed;
- fixed finite path source.

No full extension \(J:V\to V\) should be introduced.

### E. Fixed-kernel projector criterion

For a finite stacked loop-defect map \(F_t\), formalize:
\[
\ker F_t\text{ projector-continuous}
\iff
\operatorname{rank}F_t\text{ locally constant},
\]
plus the applied-projector cluster criterion
\[
Q_*m_0=Q_0m_0.
\]

### F. Exact periodic discontinuity witness

Formalize the \(L=3\) family of §11 and the exact values
\[
d=(0,-3,3),
\]
\[
\kappa_A(t;0)=0\quad(t\ne0),
\qquad
\kappa_A(0;0)=-3e_B.
\]

Keep the raw determinant-one solder and trivial affine period explicit.

This handoff is intentionally small. No Lean code is added by this research
task.

---

## 25. Reproducible exact checker

The standard-library checker below uses exact rational arithmetic. It
reproduces the mandatory \(L=3\) family, the universal-\(M_0\) necessity
perturbation, a non-graph stable restricted family, the unbounded-\(J\) control,
a killed-lost-direction control with \(M_0\ne0\), a benign exact graph rank
drop, the independent post-source selector jump, and the quotient/corner
conflict.

Run from repository root:

```bash
python - <<'CHECK'
from pathlib import Path
p = Path('02_REGISTRY/research/MEMO_A4D_SELECTED_DIAGONAL_RANK_TRANSITION_CONTINUITY.md')
s = p.read_text().split('\n<!-- EXACT_CHECKER_BEGIN -->\n', 1)[1]
code = s.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, str(p) + ':exact-checker', 'exec'))
CHECK
```

<!-- EXACT_CHECKER_BEGIN -->

```python
from fractions import Fraction as Q

checks = 0
def ck(x, name):
    global checks
    checks += 1
    if not x:
        raise AssertionError(name)

def eye(n=4):
    return [[Q(i == j) for j in range(n)] for i in range(n)]
def z(n=4):
    return [[Q(0) for _ in range(n)] for _ in range(n)]
def tr(a):
    return [list(c) for c in zip(*a)]
def add(a,b):
    return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sub(a,b):
    return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sc(t,a):
    t=Q(t); return [[t*x for x in r] for r in a]
def mul(a,b):
    return [[sum((x*y for x,y in zip(r,c)),Q(0)) for c in tr(b)] for r in a]
def mv(a,v):
    return [sum((x*y for x,y in zip(r,v)),Q(0)) for r in a]
def col(a,j):
    return [r[j] for r in a]
def cols(vs,n=4):
    return [[Q(v[i]) for v in vs] for i in range(n)]
def va(*vs):
    return [sum(q,Q(0)) for q in zip(*vs)]
def vs(t,v):
    return [Q(t)*x for x in v]
def rr(a):
    a=[[Q(x) for x in row] for row in a]
    piv=[]; k=0
    for j in range(len(a[0])):
        p=next((i for i in range(k,len(a)) if a[i][j]),None)
        if p is None:
            continue
        a[k],a[p]=a[p],a[k]
        q=a[k][j]; a[k]=[x/q for x in a[k]]
        for i in range(len(a)):
            if i != k and a[i][j]:
                q=a[i][j]
                a[i]=[x-q*y for x,y in zip(a[i],a[k])]
        piv.append(j); k+=1
        if k == len(a): break
    return a,piv
def rank(a):
    return len(rr(a)[1])
def ker(a):
    r,piv=rr(a); n=len(a[0]); ans=[]
    for j in range(n):
        if j in piv: continue
        v=[Q(i==j) for i in range(n)]
        for i,p in enumerate(piv): v[p]=-r[i][j]
        ans.append(v)
    return ans
def inv(a):
    n=len(a)
    aug=[a[i]+eye(n)[i] for i in range(n)]
    r,piv=rr(aug)
    if piv[:n] != list(range(n)): raise ValueError("singular")
    return [row[n:] for row in r]
def projector(basis,n=4):
    if not basis: return z(n)
    c=cols(basis,n)
    return mul(mul(c,inv(mul(tr(c),c))),tr(c))
def pack(B,S):
    PK=projector(ker(B))
    PH=sub(eye(),PK)
    return PH,mul(S,PH),mul(S,PK)

I=eye()
Z=z()
e=[col(I,j) for j in range(4)]
o=[Q(0)]*4

# 1. Universal necessity at a non-graph endpoint.
B0=cols([e[0],o,o,o])
S0=cols([o,e[2],o,o])
PH0,C0,D0=pack(B0,S0)
ck(mv(S0,e[1])==e[2], "M0 nonzero direction")
for t in (Q(1),Q(1,7),Q(-1,9)):
    Bt=cols([e[0],vs(t,e[1]),o,o])
    _,Ct,Dt=pack(Bt,S0)
    ck(col(Ct,1)==e[2] and col(C0,1)==o, "universal perturbation forces C jump")
    ck(add(Ct,Dt)==S0, "C+D=S")

# Restricted non-graph family can still be continuous.
for t in (Q(0),Q(1,3),Q(-2)):
    _,Ct,Dt=pack(Z,S0)
    ck(Ct==Z and Dt==S0, "non-graph restricted family stable")

# 2. Continuous C with unbounded normalized J.
for t in (Q(1),Q(1,2),Q(1,11)):
    Bt=cols([vs(t*t,e[0]),o,o,o])
    St=cols([vs(t,e[1]),o,o,o])
    _,Ct,_=pack(Bt,St)
    ck(col(Ct,0)==vs(t,e[1]), "C=t eB")
    ck(vs(1/(t*t),col(Ct,0))==vs(1/t,e[1]), "J gain = 1/t")
_,Cz,_=pack(Z,Z)
ck(Cz==Z, "C0=0")

# 3. Killed lost direction with M0 != 0.
Skeep=cols([o,e[2],o,o])
for t in (Q(1),Q(1,5),Q(0)):
    Bt=cols([vs(t,e[0]),o,o,o]) if t else Z
    _,Ct,Dt=pack(Bt,Skeep)
    ck(Ct==Z and Dt==Skeep, "lost eA killed although M0 nonzero")

# 4. Mandatory L=3 periodic family.
f=(Q(1),Q(-2),Q(1))
d=tuple(f[j]-f[(j-1)%3] for j in range(3))
ck(d==(Q(0),Q(-3),Q(3)), "mandatory d")

# Potential (0,t,-t) has forward gradient t*f.
for t in (Q(0),Q(1,7),Q(-2)):
    phi=(Q(0),t,-t)
    grad=tuple(phi[(j+1)%3]-phi[j] for j in range(3))
    ck(grad==tuple(t*x for x in f), "exact periodic affine gradient")
    ck(sum(grad,Q(0))==0, "trivial affine period")
    delta=[]
    for j in range(3):
        B=cols([vs(t*d[j],e[0]),o,o,o])
        S=cols([vs(d[j],e[1]),o,o,o])
        _,C,D=pack(B,S)
        a=va(vs(-t*f[(j-1)%3],e[0]),vs(-1,col(C,0)))
        delta.append(a)
        if t:
            ck(D==Z, "mandatory graph off zero")
            ck(col(C,0)==vs(d[j],e[1]), "mandatory correlated action off zero")
        else:
            ck(C==Z, "mandatory C zero at rank-zero endpoint")
    mean=[sum((delta[j][k] for j in range(3)),Q(0))/3 for k in range(4)]
    ck(mean==o, "mandatory transported mean zero")
    kap=[]
    for j in range(3):
        y=(j+1)%3
        b=vs(t*f[j],e[0])
        vx=va(e[0],vs(f[j],e[1]))
        vy=va(e[0],vs(f[y],e[1]))
        kap.append(va(b,vy,delta[y],vs(-1,vx)))
    if t:
        ck(kap==[o,o,o], "mandatory kappa zero off transition")
    else:
        ck(kap==[vs(-3,e[1]),vs(3,e[1]),o], "mandatory kappa jump at zero")
        ck(kap[0]==vs(-3,e[1]), "mandatory origin -3eB")

# Raw coframe shear is invertible.
for j in range(3):
    V=cols([va(e[0],vs(f[j],e[1])),e[1],e[2],e[3]])
    ck(rank(V)==4, "raw solder invertible")

# 5. Exact graph calibration rank drop is benign when S=T B.
T=cols([e[1],o,o,o]) # T eA=eB
for t in (Q(0),Q(1,9),Q(-3)):
    B=cols([vs(t,e[0]),o,o,o])
    S=mul(T,B)
    _,C,D=pack(B,S)
    ck(C==S and D==Z, "exact graph calibration survives rank drop")

# 5b. Literal L=3 exact translation-gauge rank drop from the landed control.
eta=cols([e[0],vs(-1,e[1]),vs(-1,e[2]),vs(-1,e[3])])
fg=(Q(3),Q(3),Q(-6))
dg=tuple(fg[j]-fg[(j-1)%3] for j in range(3))
ck(dg==(Q(9),Q(0),Q(-9)), "exact gauge increment pattern")
diag=[]
for j in range(3):
    B=cols([vs(dg[j],e[1]),o,o,o])
    S=mul(eta,B)
    _,C,D=pack(B,S)
    a=va(vs(-fg[(j-1)%3],e[1]),vs(-1,col(C,0)))
    diag.append(a)
    ck(C==S and D==Z, "L3 exact gauge C=S D=0")
ck(diag==[vs(15,e[1]),vs(-3,e[1]),vs(-12,e[1])], "L3 exact gauge selected diagonal")
for j in range(3):
    y=(j+1)%3
    b=vs(fg[j],e[1])
    vx=va(e[0],vs(-fg[j],e[1]))
    vy=va(e[0],vs(-fg[y],e[1]))
    kap=va(b,vy,diag[y],vs(-1,vx))
    ck(kap==o, "L3 exact gauge kappa zero")

# 5c. Nyquist, corner, harmonic, duplicate controls.
vn=(vs(-1,e[0]),vs(3,e[0]))
ck(va(vn[1],vs(-1,vn[0]))==vs(4,e[0]), "L2 Nyquist +4")
ck(va(vn[0],vs(-1,vn[1]))==vs(-4,e[0]), "L2 Nyquist -4")
corner_v0=va(e[0],vs(-1,e[1]))
corner_v1=e[0]
ck(va(corner_v1,vs(-1,corner_v0))==e[1], "L3 corner eB")
harm=va(e[0],vs(-1,e[1]))
ck(va(harm,vs(-1,harm))==o, "constant harmonic local mismatch zero")
Bdup=cols([e[0],e[0],o,o])
Sdup=cols([e[1],vs(-1,e[1]),o,o])
_,Cdup,Ddup=pack(Bdup,Sdup)
ck(Ddup!=Z and rank(Bdup)==1, "duplicate increments retain vertical defect")

# 6. Post-source selector jump with continuous source.
m=e[1]
Qoff=cols([e[0],o,e[2],e[3]]) # projection onto span(A,C,D)
Qzero=I
ck(mv(Qoff,m)==o and mv(Qzero,m)==e[1], "fixed-space projector jump")
h_off=vs(-1,mv(Qoff,m))
h_zero=vs(-1,mv(Qzero,m))
delta_off=va(m,h_off)
delta_zero=va(m,h_zero)
ck(delta_off==e[1] and delta_zero==o, "continuous seed, discontinuous selector")
for t in (Q(1),Q(1,7),Q(0)):
    src=vs(t,e[1]) # (G_t-I)eB
    ck(src==vs(t,e[1]), "continuous loop source")

# 7. Edge mismatch tracks selected delta continuously.
tau=e[2]
for q in (Q(0),Q(1,10),Q(-1,20)):
    delt=va(e[0],vs(q,e[1]))
    kap=va(tau,delt)
    ck(va(kap,vs(-1,tau))==delt, "kappa tracks delta")

# 8. Quotient cure conflicts with the L3 corner.
qkill=cols([e[0],o,e[2],e[3]])
ck(mv(qkill,e[1])==o, "quotient kills mandatory jump")
corner=e[1]
ck(mv(qkill,corner)==o, "same quotient erases mandatory corner response")

print(f"PASS: {checks} exact rational assertions; no floating tolerances")
```

Expected output:

```text
PASS: 78 exact rational assertions; no floating tolerances
```

The checker is evidence for the named finite witnesses only. The general
quantifiers are the linear-algebra proofs in the preceding sections.

---

## 26. Research closeout

The conceptual result is complete when this memo is in the PR:

- local lost-direction stability is classified exactly;
- \(M_0=0\) is upgraded from sufficient to exact universal criterion;
- relation/subspace/action/\(J\)/source/solution-space/selector/readout
  continuity are separated;
- the literal PR #120 selector is pressure-tested;
- a second independent selector-kernel discontinuity is exhibited;
- the mandatory \(L=3\) witness is reproduced exactly;
- all four remediation routes are classified;
- the theorem-ready worker handoff is bounded.

Ready audit: the exact checker passes 78 rational assertions; `main` remains at the audited baseline; the task has self-retired; the task brief and manifest row are absent; and the PR diff contains only this durable memo. The PR is `Lifecycle: REVIEW` and is not self-merged.

The first guard run on the retired head was spawned while GitHub still marked the PR as Draft, so the PR-contract guard correctly expected the active task row and failed. This lifecycle-audit commit is made after Ready specifically to trigger the contract against the final Ready state; it changes no research result.


---

## 27. Further synthesis: the exact projector-incidence resolution

The continuity criterion above identifies when the pointwise canonical rule
happens to descend continuously. There is a stronger structural statement:
the entire discontinuity can be resolved by remembering one finite
coefficient-space projector.

Let
\[
E=E_{\rm lab},\qquad
H_B=(\ker B)^\perp,\qquad
P_B=P_{H_B}.
\]

Define the projector-incidence fibre
\[
\boxed{
\mathfrak P(B)
=
\{\Pi\in\operatorname{End}(E):
\Pi^2=\Pi=\Pi^\ast,\quad B\Pi=B\}.
}
\tag{27.1}
\]

For an orthogonal projector, \(B\Pi=B\) is equivalent to
\[
H_B\subseteq\operatorname{im}\Pi.
\]
Writing \(K_B=\ker B\), every such range splits orthogonally as
\[
\operatorname{im}\Pi
=
H_B\oplus W,
\qquad
W\le K_B.
\]
Therefore
\[
\boxed{
\mathfrak P(B)
=
\{P_B+P_W:W\le K_B\}.
}
\tag{27.2}
\]

The intrinsic pointwise canonical choice is the **minimal** member
\[
\Pi_{\rm int}=P_B
\]
and the maximal member is
\[
\Pi_{\rm max}=I
\]
whenever the source and target dimensions are both four.

### Theorem 7 — exact closure of the active-projector graph

For the present \(4\to4\) synthesis maps, the closure of
\[
B\longmapsto P_{(\ker B)^\perp}
\]
inside
\[
\operatorname{Hom}(E,V)\times\operatorname{End}(E)
\]
is exactly the incidence set
\[
\boxed{
\mathfrak I_B
=
\{(B,\Pi):\Pi\in\mathfrak P(B)\}.
}
\tag{27.3}
\]

The cluster-projector theorem of §3 proves one inclusion. For the reverse,
take
\[
\Pi=P_B+P_W,
\qquad W\le K_B.
\]
Choose a complement
\[
V=\operatorname{im}B\oplus R
\]
and an injection
\[
J:W\hookrightarrow R.
\]
Extend \(J\) by zero on \(W^\perp\), and put
\[
B_\varepsilon
=
B+\varepsilon J P_W.
\]
If
\[
c=h+w+k,
\quad
h\in H_B,\quad
w\in W,\quad
k\in K_B\cap W^\perp,
\]
then
\[
B_\varepsilon c
=
Bh+\varepsilon Jw
\]
is a sum of vectors in the direct-sum factors
\(\operatorname{im}B\) and \(R\). Hence
\[
\ker B_\varepsilon
=
K_B\cap W^\perp
\]
for every nonzero \(\varepsilon\), so
\[
P_{(\ker B_\varepsilon)^\perp}
=
P_B+P_W
=
\Pi.
\]
Finally \(B_\varepsilon\to B\).

Thus every allowed \(W\) is an actual rank-transition approach direction, not
an abstract completion point.

Over a rank-\(r\) endpoint, the resolution fibre is the finite union
\[
\coprod_{k=0}^{4-r}\operatorname{Gr}(k,K_B).
\]
This Grassmannian language is a classification of finite matrix approach
data, not a claim that a physical continuum manifold has been derived.

---

## 28. Vertical defect = exact universal instability radius

On the incidence resolution define
\[
\boxed{
\widetilde C(B,S,\Pi)=S\Pi.
}
\tag{28.1}
\]
This is polynomial, hence continuous, in the resolved data. On the intrinsic
section \(\Pi=P_B\),
\[
\widetilde C=C.
\]

Using (27.2),
\[
\widetilde C-C
=
SP_W
=
(SP_{K_B})P_W
=
DP_W.
\tag{28.2}
\]

Therefore the complete cluster set of the correlated action is
\[
\boxed{
\operatorname{Clust}_B(C)
=
\{C+SP_W:W\le K_B\}.
}
\tag{28.3}
\]

This gives three exact new interpretations of the landed vertical data.

### 28.1 \(D\) is the maximal full-rank jump operator

Choosing \(W=K_B\) gives \(\Pi=I\), realizable by a full-rank perturbation.
Hence
\[
\boxed{
C_{\rm full\;rank\;cluster}-C=D.
}
\tag{28.4}
\]
Equivalently, the maximal lift has
\[
\widetilde C=S.
\]

For every Role basis vector,
\[
\boxed{
a^{\rm full}_r-a^{\rm int}_r=-D\varepsilon_r=-R_r.
}
\tag{28.5}
\]
Thus each canonical Role residual is literally a realizable full-rank
rank-transition seed jump.

### 28.2 \(M\) is the total possible jump-output space

Because the maximal jump is \(D\),
\[
\boxed{
\operatorname{span}\{\operatorname{im}(C_*-C):
C_*\in\operatorname{Clust}_B(C)\}
=
\operatorname{im}D
=
M.
}
\tag{28.6}
\]

So the vertical defect is not only the pointwise multivalued part of the
relation. It is exactly the output space in which arbitrary rank-transition
jumps can occur.

### 28.3 Exact quantitative radius

For any operator norm induced by the fixed finite-dimensional Hilbert norms,
\[
\|DP_W\|\le\|D\|.
\]
The choice \(W=K_B\) saturates the bound. Hence
\[
\boxed{
\sup_{C_*\in\operatorname{Clust}_B(C)}
\|C_*-C\|
=
\|D\|.
}
\tag{28.7}
\]

This gives \(D\) a quantitative stability meaning without introducing a new
physical norm into the definition of the source.

### Corollary — graphification is exact descent from the resolution

The continuous resolved action \(\widetilde C\) is constant on the entire
incidence fibre over \((B,S)\) iff
\[
D=0
\iff
M=0.
\]
Thus
\[
\boxed{
M=0
\iff
\text{the projector-resolved correlated action descends uniquely to the
unresolved pointwise background}.
}
\tag{28.8}
\]

This is a stronger structural reading of the universal-continuity theorem:
graphification is exactly the condition under which approach memory becomes
unobservable in the correlated action.

---

## 29. Rank labels and finite background jets do not determine the missing datum

The missing datum is not an integer rank.

At the same endpoint \(B_0=0\), take
\[
B_t^{(A)}=t\,e_A\otimes\varepsilon_A^\ast,
\qquad
B_t^{(B)}=t\,e_A\otimes\varepsilon_B^\ast.
\]
Both approaches have rank one for every \(t\ne0\), but
\[
P_{H_t^{(A)}}=P_{\mathbb R\varepsilon_A},
\qquad
P_{H_t^{(B)}}=P_{\mathbb R\varepsilon_B}.
\]
For an \(S_0\) which distinguishes those coefficient directions, the two
correlated-action limits differ.

Hence
\[
\boxed{
\text{rank stratum alone is insufficient; the Grassmannian direction is
essential.}
}
\tag{29.1}
\]

Nor can a universal finite-order parameter jet recover it.

For every integer \(k\ge0\), compare
\[
B_t^{(0)}=B_0
\]
with
\[
B_t^{(W)}
=
B_0+t^{k+1}JP_W.
\]
Their derivatives through order \(k\) at \(t=0\) agree, while for every
\(t\ne0\) the second family carries the nonzero lost space \(W\).

Therefore:
\[
\boxed{
\text{no fixed finite-order parameter jet determines the rank-resolution
projector on arbitrary smooth families.}
}
\tag{29.2}
\]

The obstruction is stronger in the \(C^\infty\) category. Replace
\(t^{k+1}\) by
\[
\chi(t)=
\begin{cases}
e^{-1/t^2},&t\ne0,\\
0,&t=0.
\end{cases}
\]
Then all derivatives at zero agree with the constant family, but the
nonzero-\(t\) active subspace is still \(H_B\oplus W\).

So even the full Taylor jet at the singular point does not recover the
approach projector for unrestricted smooth families.

Analytic/algebraic families are different: a full germ can encode the first
nonzero activation order. But no **uniform finite jet order** can do so,
because the order \(k+1\) above is arbitrary.

This matters downstream: neither the first derivative \(H(e)\) nor a finite
second-jet package can, by itself, repair arbitrary rank-transition memory.

---

## 30. Dual incidence resolution of the holonomy-fixed selector

The post-source seam has an exact dual form.

Fix a basepoint and finitely many fundamental loop generators, and stack
their defects:
\[
F:V_o\to Y,
\qquad
Fh=((P_{\gamma_i}-I)h)_i.
\]
Then
\[
\mathcal H=\ker F.
\]

Fix the positive observer inner product \(h_o\). Define
\[
\boxed{
\mathfrak Q(F)
=
\{Q:Q^2=Q=Q^{\dagger_{h_o}},\quad FQ=0\}.
}
\tag{30.1}
\]
These are exactly the \(h_o\)-orthogonal projectors onto subspaces
\[
H_*\le\mathcal H.
\]

The intrinsic PR #120 choice is the **maximal** member
\[
Q_{\rm int}=P^{h_o}_{\mathcal H}.
\]
The zero projector is the minimal member.

For arbitrary finite stacked defect maps with
\(\dim Y\ge\dim V_o\), the closure of
\[
F\longmapsto P^{h_o}_{\ker F}
\]
is exactly (30.1). The proof is the kernel-dual of §27: if
\[
\mathcal H=H_*\oplus W,
\]
perturb \(F\) by a small injection of \(W\) into a complement of
\(\operatorname{im}F\). The perturbed kernel is exactly \(H_*\).

At a trivial-holonomy transport background this whole fibre is also realized
inside actual invertible loop transports. Given any
\[
H_*\le V_o,
\]
choose \(T\) with \(\ker T=H_*\) and use one fundamental loop
\[
G_\varepsilon=I+\varepsilon T.
\]
For sufficiently small nonzero \(\varepsilon\), \(G_\varepsilon\) is
invertible and
\[
\operatorname{Fix}G_\varepsilon=H_*.
\]

Thus the selector seam is not merely an artifact of stacking loop equations.

### Resolved selector

For a transported seed mean \(m\), define
\[
\widetilde h_o(F,Q,m)=-Qm.
\tag{30.2}
\]
This is continuous on the resolved incidence space.

Let
\[
Q_0=P^{h_o}_{\mathcal H}.
\]
For \(Q=P^{h_o}_{H_*}\), write
\[
\mathcal H=H_*\oplus_{h_o}W_{\rm gain}.
\]
Then
\[
Q_0-Q=P^{h_o}_{W_{\rm gain}},
\]
and the selected correction jump is
\[
\boxed{
\widetilde h_o(Q)-h_o^*
=
P^{h_o}_{W_{\rm gain}}m.
}
\tag{30.3}
\]

Exactly as locally,
\[
\boxed{
\sup_{Q\in\mathfrak Q(F)}
\|\widetilde h_o(Q)-h_o^*\|_{h_o}
=
\|Q_0m\|_{h_o}
=
\|h_o^*\|_{h_o}.
}
\tag{30.4}
\]

Hence the already-selected parallel correction is itself the exact
worst-case selector-instability amplitude for arbitrary defect-map
perturbations.

The selector is constant on the entire incidence fibre iff
\[
\boxed{
Q_0m=0.
}
\tag{30.5}
\]

At trivial holonomy this is also the exact criterion for stability under
arbitrary small actual loop-holonomy perturbations.

The local and global seams are therefore genuinely dual:

| local relative A/e seam | post-source holonomy seam |
|---|---|
| endpoint kernel \(K=\ker B\) | endpoint kernel \(\mathcal H=\ker F\) |
| approach projector is **larger** than intrinsic \(P_H\) | approach projector is **smaller** than intrinsic \(Q_0\) |
| missing subspace \(W_{\rm lost}\le K\) | missing fixed subspace \(W_{\rm gain}\le\mathcal H\) |
| jump \(SP_{W_{\rm lost}}\) | jump \(P_{W_{\rm gain}}m\) |
| universal radius \(\|D\|\) | universal radius \(\|h_o^*\|\) |
| fibre collapses iff \(D=0\) | fibre collapses iff \(h_o^*=0\) |

This identifies the two exact instability carriers already present in the
landed construction:
\[
\boxed{
D
\quad\text{and}\quad
h_o^*.
}
\tag{30.6}
\]

---

## 31. The double-projector resolved selected interface

The two incidence resolutions combine without introducing a full extension
of \(J\).

At every site choose
\[
\Pi_y\in\mathfrak P(\mathcal B_y),
\]
and at the basepoint choose
\[
Q_o\in\mathfrak Q(F).
\]
Call
\[
\Xi=((\Pi_y)_y,Q_o)
\]
the **rank/holonomy resolution datum**.

With the PR #120 paths fixed, write \(T_y:V_y\to V_o\) for their linear
transport. Define
\[
\widetilde C_y
=
\mathcal S_y\Pi_y,
\]
\[
\widetilde a_r(y)
=
-\bar b_r(y)-\widetilde C_y\varepsilon_r,
\]
\[
\widetilde m_r
=
\frac1{|X|}
\sum_yT_y\widetilde a_r(y),
\]
\[
\boxed{
\widetilde\delta_r(y)
=
\widetilde a_r(y)-T_y^{-1}Q_o\widetilde m_r,
}
\tag{31.1}
\]
and finally
\[
\boxed{
\widetilde\kappa(x,r)
=
\tau(x,r)+L_{x,r}\widetilde\delta_r(x+r).
}
\tag{31.2}
\]

### Theorem 8 — resolved continuity

On the finite background domain where every affine link remains invertible,
the map
\[
(A,e,\Xi)\longmapsto
(\widetilde C,\widetilde a,\widetilde S,
\widetilde\delta,\widetilde\kappa)
\]
is continuous in all resolved variables.

No Moore–Penrose inverse and no normalized full graph operator is used.

### Theorem 9 — cluster completeness

Take any convergent background sequence for which the canonical coefficient
projectors and fixed-kernel projectors have a joint cluster
\[
P_{H_{n,y}}\to\Pi_{*,y},
\qquad
Q_n\to Q_*.
\]
Then the canonical selected outputs converge to the resolved formula
\[
(\widetilde\delta,\widetilde\kappa)
\]
evaluated at
\[
\Xi_*=((\Pi_{*,y})_y,Q_*).
\]

Thus the double-projector package does not invent a smoothing rule. It records
exactly the data needed to represent every existing cluster value.

Conversely, §27 realizes every local \(\Pi_y\) by synthesis perturbations, and
§30 realizes every \(Q_o\) at trivial holonomy by actual invertible loop
perturbations.

### Minimality

For a fixed \((B,S)\), two local projectors are observationally equivalent for
the sourced chain precisely when
\[
S\Pi_1=S\Pi_2.
\]
For a fixed transported mean, two selector projectors are equivalent precisely
when
\[
Q_1m=Q_2m.
\]

Those are the smallest **readout-dependent** quotients.

But they are not structural data: they depend on \(S\) and on the selected
mean. If the interface must work uniformly for arbitrary solder synthesis and
arbitrary source mean, the projectors themselves cannot be quotiented further.
Indeed, if
\[
\Pi_1\ne\Pi_2,
\]
one can choose an \(S\) separating them; and if
\[
Q_1\ne Q_2,
\]
one can choose an \(m\) separating them.

Therefore the minimal non-tautological universal memory is exactly:

- a lost-direction subspace \(W_y\le K_y\) at each local rank seam;
- an approach fixed subspace \(H_*\le\mathcal H_o\) at the selector seam.

No full-fibre comparison \(J:V\to V\) is required.

---

## 32. Exact covariance and control behavior of the resolved package

The local projector \(\Pi\) lives in the labelled coefficient space. Under an
invertible output-frame transformation
\[
B\mapsto gB,\qquad S\mapsto gS,
\]
the coefficient kernel is unchanged, so the same \(\Pi\) is admissible and
\[
\widetilde C\mapsto g\widetilde C.
\]

At the selector seam,
\[
Q_o\mapsto g_oQ_og_o^{-1}
\]
under the observer-congruent frame law. Hence (31.1)–(31.2) transform
covariantly. The resolution does not introduce a preferred output frame.

### Exact gauge is resolution-independent

On the exact translation-gauge chart,
\[
S=TB
\]
for the frozen chart comparison \(T\). Every admissible \(\Pi\) satisfies
\(B\Pi=B\), so
\[
\boxed{
S\Pi
=
TB\Pi
=
TB
=
S.
}
\tag{32.1}
\]
Thus the local rank-resolution datum is invisible on exact gauge, including
rank drops.

### Flat and pure shift

For the flat and constant pure-shift local synthesis,
\[
S=0.
\]
Hence
\[
S\Pi=0
\]
for every local resolution lift. The local projector cannot spoil these
controls.

### Coframe-only Nyquist/corner backgrounds expose the unavoidable tradeoff

For a coframe-only point,
\[
B=0,\qquad S\ne0.
\]
Then
\[
\mathfrak P(B)
\]
contains **every** orthogonal projector on \(E\).

The intrinsic lift
\[
\Pi_{\rm int}=0
\]
gives
\[
\widetilde C=0
\]
and therefore preserves the raw Nyquist/corner response exactly, as required
by PR #120.

But the maximal full-rank approach lift
\[
\Pi=I
\]
gives
\[
\widetilde C=S.
\]

Therefore:
\[
\boxed{
\text{a nonzero coframe-only raw response and invariance under every nearby
affine activation cannot both hold.}
}
\tag{32.2}
\]

This is not a defect of the resolution. It is the explicit content of
\(M=S(E)\ne0\) at the coframe-only point.

The raw controls therefore force one of two interpretations:

1. the admissible physical background family near such a point is restricted;
2. the approach/resolution datum is retained.

A pointwise rule cannot have both the intrinsic raw value and every
rank-changing limit.

### Global flat control

At the flat selector,
\[
m=0.
\]
Therefore every \(Q\) gives the same selected correction. The maximal
holonomy-resolution fibre is invisible.

By contrast, a nonzero transported mean can make a trivial-holonomy endpoint
selector-sensitive, exactly as the archive witness in §13 demonstrates.

---

## 33. No finite-jet dressing can manufacture the missing rank memory

The planned finite graded coframe dressing is constrained at first order by
the already-owned \(H(e)\), and any future second derivative would supply a
finite higher jet.

Section 29 gives a direct firewall:

\[
\boxed{
\text{no finite parameter-jet order can universally reconstruct }
\Pi_*.
}
\tag{33.1}
\]

The selector seam has the same obstruction. For any finite \(k\), take a loop
family
\[
G_t
=
I+t^{k+1}T.
\]
It has the same \(k\)-jet at zero as the identity loop, while for every
nonzero \(t\)
\[
\operatorname{Fix}G_t=\ker T.
\]
Using the flat \(C^\infty\) function \(e^{-1/t^2}\) makes even the full Taylor
jet at zero equal to the identity family while keeping the nonzero-\(t\)
fixed space \(\ker T\).

Hence neither local projector memory nor global fixed-space memory is selected
by a universal finite background jet.

This separates two tasks that could otherwise be conflated:

- constructing a finite dressing with the correct first derivative;
- selecting a global rank-transition continuation across singular strata.

Success at the first does not solve the second.

---

## 34. The nilpotent matter letter inherits every surviving \(\kappa\) jump

The repository already Lean-owns
\[
T_b
=
I+C^\dagger(b)P_0
\]
and
\[
T_bT_c=T_{b+c}.
\]
It also owns
\[
b\ne0\Longrightarrow T_b\ne I.
\]

These imply injectivity:
\[
\boxed{
T_b=T_c\iff b=c.
}
\tag{34.1}
\]
Indeed equality gives
\[
T_{b-c}=T_bT_{-c}=I,
\]
hence \(b-c=0\).

Therefore two distinct cluster mismatches
\[
\kappa_*\ne\kappa_0
\]
produce two distinct conditional matter letters
\[
\boxed{
T_{\kappa_*}\ne T_{\kappa_0}.
}
\tag{34.2}
\]

The existing conjugation no-go strengthens this. For any invertible Fock-space
linear equivalence \(\mathcal F\),
\[
\mathcal F T_b\mathcal F^{-1}=I
\]
is impossible when \(b\ne0\).

Consequently, if one unresolved background has two selected cluster values
whose difference is nonzero, applying the **same** finite dressing cannot
identify the two nilpotent responses:
\[
\boxed{
\mathcal F T_{\kappa_*}\mathcal F^{-1}
=
\mathcal F T_{\kappa_0}\mathcal F^{-1}
\Longrightarrow
\kappa_*=\kappa_0.
}
\tag{34.3}
\]

A branch-dependent dressing could compensate only by carrying the same
resolution/approach memory itself.

This is the first direct propagation of the rank-transition stability problem
into the already-owned affine-sensitive matter channel.

---

## 35. Consequence for the finite graded coframe-dressing gate

The planned
`EXP-A4D-FINITE-GRADED-COFRAME-DRESSING`
task remains mathematically open, but its typing can now be sharpened.

The dressing may still be constructed on arbitrary pointwise coframes.
Nothing here obstructs a finite \(\mathcal F_e\) with
\[
DW_0=H.
\]

What is ruled out is a stronger silent assumption:

> a single-valued unresolved dressing can consume the current selected
> \(\kappa(A,e)\) continuously across every rank/holonomy transition merely
> because its flat first derivative is correct.

The exact alternatives are now:

### Stable-domain route

Restrict the mixed A/e input family so that the local lost-direction criterion
and the applied fixed-kernel criterion hold. Then the existing selected
\(\kappa\) is continuous and may be passed to \(T_\kappa\).

### Resolved-background route

Type the mixed coupling on
\[
(A,e,\Xi),
\qquad
\Xi=((\Pi_y)_y,Q_o),
\]
and use
\[
\widetilde\kappa(A,e,\Xi).
\]
Then the selected mismatch and \(T_{\widetilde\kappa}\) are continuous in the
resolved data.

### Forgetful route

Make the dressing insensitive to every \(\kappa\)-jump direction. The
quotient/corner result of §17 already shows that this cannot preserve all
mandatory raw distinctions in the current interface.

Because \(T_\kappa\) is injective, replacing \(\kappa\) by the nilpotent
matter letter does not create a fourth route.

Thus the stability research does not block the graded-dressing task, but it
removes an ambiguity in its future statement of domain:

\[
\boxed{
\text{unresolved arbitrary background}
\quad\text{vs}\quad
\text{stable admissible family}
\quad\text{vs}\quad
\text{rank/holonomy-resolved background}.
}
\tag{35.1}
\]

Those are now mathematically different objects and must not be conflated.

---

## 36. External mathematical cross-check

The local projector can be written in standard finite-dimensional notation as
\[
P_{H_B}=B^\dagger B,
\]
where \(B^\dagger\) is the Moore–Penrose inverse.

Classical matrix-analysis literature records the familiar fact that
Moore–Penrose inversion is continuous on constant-rank strata and generally
fails at rank changes. A useful published pointer is the discussion in:

- *A note on the convexity of the Moore–Penrose inverse*,
  Linear Algebra and its Applications (2018), which explicitly recalls that
  continuity is essentially equivalent to constant rank and cites the
  standard Campbell–Meyer treatment.

The D0 result is deliberately sharper for the present composed observable:
even when \(B^\dagger\) and \(B^\dagger B\) are discontinuous,
\[
SB^\dagger B
\]
can remain continuous. The exact weakening is not “approximately constant
rank” but the lost-direction annihilation condition
\[
S_0(W_{\rm lost})=0.
\]

So the repository result is consistent with the standard pseudoinverse
boundary while identifying the strictly weaker continuity condition relevant
to the sourced diagonal chain.

---

## 37. Strengthened synthesis after continuation

The official task terminal remains

\[
\texttt{SELECTED-DIAGONAL-RANK-TRANSITION-CONTINUITY-CRITERION-CONSTRUCTED}.
\]

The continuation sharpens its meaning:

1. the singularity admits an exact finite projector-incidence resolution;
2. the vertical residual map \(D\) is the exact local universal instability
   radius/operator;
3. the selected parallel correction \(h_o^*\) is the exact dual selector
   instability radius;
4. rank integers and finite jets do not determine either resolution datum;
5. the double projector datum \(\Xi\) is sufficient to make the full selected
   finite interface continuous;
6. exact gauge is independent of the local resolution lift;
7. raw coframe-only Nyquist/corner data force genuine approach sensitivity
   unless the admissible family is restricted;
8. the injective nilpotent matter letter \(T_\kappa\) faithfully propagates
   every surviving mismatch jump;
9. a future finite graded dressing must therefore declare whether it lives on
   a stable unresolved domain or on the resolved background space.

This is the strongest research conclusion available from the current landed
objects without actually starting the separate finite graded dressing task.


---

## 38. Exact resolution checker

The following independent standard-library checker verifies the finite matrix
claims used in §§27–32 and §40: incidence \(B\Pi=B\), the exact jump
\(DP_W\), maximal lift \(D\), rank-label insufficiency, exact-gauge
resolution independence, coframe-only lift dependence, and the dual
fixed-space selector jump.

```python
from fractions import Fraction as Q

checks = 0
def ck(x, label):
    global checks
    checks += 1
    if not x:
        raise AssertionError(label)

def eye(n=4):
    return [[Q(i == j) for j in range(n)] for i in range(n)]
def zero(n=4):
    return [[Q(0) for _ in range(n)] for _ in range(n)]
def tr(a):
    return [list(c) for c in zip(*a)]
def mul(a,b):
    return [[sum((x*y for x,y in zip(r,c)),Q(0)) for c in tr(b)] for r in a]
def add(a,b):
    return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sub(a,b):
    return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def col(a,j):
    return [r[j] for r in a]
def cols(vs,n=4):
    return [[Q(v[i]) for v in vs] for i in range(n)]
def mv(a,v):
    return [sum((x*y for x,y in zip(r,v)),Q(0)) for r in a]
def sc(q,a):
    return [[Q(q)*x for x in r] for r in a]
def rr(a):
    a=[[Q(x) for x in row] for row in a]
    piv=[]; k=0
    for j in range(len(a[0])):
        p=next((i for i in range(k,len(a)) if a[i][j]),None)
        if p is None:
            continue
        a[k],a[p]=a[p],a[k]
        q=a[k][j]
        a[k]=[x/q for x in a[k]]
        for i in range(len(a)):
            if i != k and a[i][j]:
                q=a[i][j]
                a[i]=[x-q*y for x,y in zip(a[i],a[k])]
        piv.append(j); k+=1
        if k == len(a):
            break
    return a,piv
def rank(a):
    return len(rr(a)[1])

I=eye(); Z=zero()
e=[col(I,j) for j in range(4)]
o=[Q(0)]*4

PH=cols([e[0],o,o,o])
PW=cols([o,e[1],o,o])
PK=sub(I,PH)
Pi=add(PH,PW)

B=cols([e[0],o,o,o])
S=cols([o,e[2],o,o])
D=mul(S,PK)
C=mul(S,PH)
Cstar=mul(S,Pi)

ck(mul(B,Pi)==B, 'incidence BPi=B')
ck(sub(Cstar,C)==mul(D,PW), 'resolved jump = D P_W')
ck(sub(mul(S,I),C)==D, 'maximal full-rank jump = D')
ck(rank(Pi)==2 and rank(PH)==1, 'rank lift')
ck(mul(S,I)==S, 'maximal lift gives S')

PA=PH
PB=PW
ck(rank(PA)==rank(PB)==1, 'same rank, different Grassmannian directions')
ck(mul(I,PA)!=mul(I,PB), 'rank label alone insufficient')

T=cols([e[1],o,o,o])
Sg=mul(T,B)
ck(mul(Sg,PH)==Sg, 'exact gauge intrinsic lift')
ck(mul(Sg,I)==Sg, 'exact gauge maximal lift')

Scof=cols([e[1],o,o,o])
ck(mul(Scof,Z)==Z, 'coframe-only intrinsic lift')
ck(mul(Scof,I)==Scof and Scof!=Z, 'coframe-only maximal lift differs')

Q0=I
Qsub=cols([e[0],o,e[2],e[3]])
m=e[1]
ck(mv(Q0,m)==e[1], 'intrinsic selector projection')
ck(mv(Qsub,m)==o, 'reduced fixed-space projection')
ck(mv(sub(Q0,Qsub),m)==e[1], 'selector jump')

Tloop=cols([o,e[1],o,o])
for t in (Q(1),Q(1,7),Q(-2)):
    G=add(I,sc(t,Tloop))
    ck(rank(sub(G,I))==1, 'loop defect rank one')
    ck(mv(G,e[0])==e[0] and mv(G,e[2])==e[2] and mv(G,e[3])==e[3],
       'fixed subspace retained')
    ck(mv(G,e[1])!=e[1], 'one fixed direction lost')


# Unique continuous unresolved completion = predecessor selector.
b=e[1]
delta_pure=[-x for x in b]
kappa_pure=[b[i]+delta_pure[i] for i in range(4)]
ck(delta_pure!=o, 'continuous completion changes pure-shift diagonal')
ck(kappa_pure==o, 'continuous completion erases pure shift')

dv=e[1]
delta_cof=[-x for x in dv]
kappa_cof=[dv[i]+delta_cof[i] for i in range(4)]
ck(dv!=o, 'raw coframe response is nonzero')
ck(kappa_cof==o, 'continuous completion erases raw coframe response')

print(f'PASS: {checks} exact rational resolution assertions')
```

Expected output:

```text
PASS: 27 exact rational resolution assertions
```

Together with the earlier 78-assertion finite suite, the memo now contains
two independent exact checkers: one for the original continuity/hostile
controls and one for the projector-resolution synthesis.


---

## 39. Unique continuous sections of the two incidence resolutions

The incidence construction admits continuous resolved dynamics, but one might
still hope to choose the resolution projector canonically and continuously
from the unresolved background.

On the unrestricted finite matrix spaces, that hope is completely rigid.

### Theorem 10 — unique continuous local section

Consider the projection
\[
(B,\Pi)\longmapsto B
\]
from the incidence set of §27.

When \(B:E\to V\) is invertible,
\[
K_B=0,
\qquad
\mathfrak P(B)=\{I\}.
\]
Invertible \(4\times4\) maps are dense in the full matrix space.

Therefore any continuous section
\[
s:B\longmapsto\Pi(B)\in\mathfrak P(B)
\]
must satisfy
\[
\Pi(B)=I
\]
on a dense set, hence everywhere.

Thus
\[
\boxed{
\Pi_{\rm cont}(B)\equiv I
}
\tag{39.1}
\]
is the **unique** globally continuous section of the local incidence
resolution.

It exists because \(BI=B\) for every \(B\).

The intrinsic canonical section
\[
B\longmapsto P_{(\ker B)^\perp}
\]
is therefore not one among many possible continuous choices. It is necessarily
discontinuous at every rank transition where it differs from \(I\).

### Theorem 11 — unique continuous abstract kernel section

For the stacked loop-defect map
\[
F:V_o\to Y
\]
with
\[
\dim Y\ge\dim V_o,
\]
injective maps are dense. For injective \(F\),
\[
\ker F=0,
\qquad
\mathfrak Q(F)=\{0\}.
\]

Therefore any continuous section
\[
q:F\longmapsto Q(F)\in\mathfrak Q(F)
\]
on the unrestricted linear-map space is forced to be
\[
\boxed{
Q_{\rm cont}(F)\equiv0.
}
\tag{39.2}
\]

This theorem is stated for the abstract finite stacked defect space. The actual
labelled-transport parameter space is a constrained subset, so no density claim
about all physical holonomy families is inferred. At trivial holonomy,
however, §30 realizes every subspace by actual invertible loop perturbations,
so the same local obstruction is already physically present there.

The two unique continuous sections are opposite extremals:
\[
\boxed{
\Pi_{\rm cont}=I,
\qquad
Q_{\rm cont}=0.
}
\tag{39.3}
\]

By contrast, the current pointwise construction uses the opposite extremals
at singular points:
\[
\Pi_{\rm int}=P_H
\quad\text{(minimal local range)},
\]
\[
Q_{\rm int}=P_{\mathcal H}
\quad\text{(maximal fixed-kernel range)}.
\]

This extremal reversal is the structural origin of the two discontinuities.

---

## 40. The unique globally continuous unresolved completion is exactly the rejected predecessor selector

Insert the unique continuous local section
\[
\Pi=I
\]
into the resolved correlated action:
\[
\widetilde C=S.
\]
Hence the residual vanishes identically:
\[
\widetilde D=S-\widetilde C=0.
\]

The seed becomes
\[
\widetilde a_r
=
-\bar b_r-S\varepsilon_r
=
-\bar b_r-\Delta v_r.
\]
Since
\[
\Delta v_r=v_r(y)-\bar v_r(y),
\]
\[
\widetilde a_r
=
\bar v_r-\bar b_r-v_r(y).
\]
But this is exactly the landed predecessor defect:
\[
\boxed{
\widetilde a_r=\rho_r.
}
\tag{40.1}
\]

Now insert the unique continuous abstract kernel section
\[
Q=0.
\]
Then
\[
\widetilde h=0,
\qquad
\boxed{
\widetilde\delta_r=\widetilde a_r=\rho_r.
}
\tag{40.2}
\]

Thus the unique globally continuous unresolved completion of **both** projector
incidence problems is not a new construction. It is precisely the predecessor
selector rejected in PR #120.

The old hostile controls now acquire a structural interpretation.

### Pure affine shift

For
\[
e=0,\qquad L=I,\qquad b\ne0,
\]
\[
\rho=-b.
\]
The continuous completion gives
\[
\delta=-b,
\]
hence
\[
\boxed{
\kappa=0,
}
\tag{40.3}
\]
erasing the required pure affine shift.

### Coframe-only Nyquist/corner

For
\[
b=0,
\]
\[
\rho=-\Delta v
\]
at flat linear transport. The continuous completion therefore chooses
\[
\delta=-\Delta v
\]
and cancels the raw solder mismatch:
\[
\boxed{
\kappa=0
}
\tag{40.4}
\]
on exactly the responses which the current selector was built to preserve.

Therefore continuity does not fail because the repository chose a poor
pseudoinverse convention. The globally continuous unresolved choice is known
explicitly, and it fails the mandatory physics-facing finite controls.

---

## 41. Strong no-go: unrestricted continuity, current controls, and pointwise canonicity cannot coexist

Combine §§27–40.

Assume an unresolved selector is required to satisfy all of:

1. it is single-valued on every finite pointwise background;
2. it depends continuously on arbitrary local synthesis matrices and arbitrary
   stacked loop-defect matrices;
3. it respects the incidence constraints
   \[
   B\Pi=B,\qquad FQ=0;
   \]
4. it agrees with the forced regular values on invertible \(B\) and injective
   \(F\);
5. it preserves the repository's pure-shift and raw Nyquist/corner controls.

Then 1–4 force
\[
\Pi=I,\qquad Q=0
\]
by Theorems 10–11. Section 40 then forces
\[
\delta=\rho,
\]
which violates condition 5.

Hence:
\[
\boxed{
\texttt{UNRESOLVED-GLOBAL-CONTINUOUS-SELECTION-PRESERVING-CONTROLS-NOGO}.
}
\tag{41.1}
\]

This no-go is scoped exactly:

- finite-dimensional;
- fixed archive level;
- unrestricted local synthesis / abstract stacked-defect perturbations;
- current active-factor and post-source incidence architecture;
- current pure-shift and Nyquist/corner controls.

It does **not** exclude:

- continuity on a restricted admissible family;
- the resolved background \((A,e,\Xi)\);
- a new physical principle which constrains allowed rank/holonomy transitions;
- a different theory which intentionally abandons the current raw controls.

But it closes one tempting route completely:

> there is no hidden globally continuous pointwise canonical selector waiting
> to be found inside the existing incidence data while retaining the controls
> that motivated PR #120.

The choices are now mathematically exhaustive at this seam:

\[
\boxed{
\text{restrict the domain}
\quad\lor\quad
\text{retain resolution memory}
\quad\lor\quad
\text{forget a mandatory distinction}.
}
\tag{41.2}
\]

---

## 42. Implication for the next constitutive research

This strengthens §35.

The finite graded coframe-dressing task may still solve its own all-order
problem. But if it is asked to couple to the already-owned affine-sensitive
letter
\[
T_\kappa,
\]
then the no-go (41.1) prevents an unresolved globally continuous selector from
being silently supplied underneath it.

Moreover the unique continuous unresolved completion would feed
\[
\delta=\rho
\]
to the matter channel, exactly the choice already rejected for erasing pure
shift and raw coframe responses.

Therefore the next constitutive research should treat one of the following as
part of its **typing**, not as a later regularity detail:

\[
\boxed{
\begin{array}{ll}
\textbf{stable-stratum input:} &
(A,e)\in\mathfrak A_{\rm stable},
\\[1mm]
\textbf{resolved input:} &
(A,e,\Xi),
\end{array}}
\tag{42.1}
\]
where \(\mathfrak A_{\rm stable}\) satisfies the exact lost-direction and
selector-cluster criteria already derived.

A future construction that writes only “arbitrary background” without saying
which of these two meanings is intended will be under-typed at rank-transition
points.

This is a stability gate on the *mixed coupling*. It is not a claim that the
coframe-only dressing \(\mathcal F_e\) itself cannot exist on arbitrary raw
coframes.


---

## 43. One step into finite graded dressing: the pure-gauge dressing is a torsor, not a coframe function

The next heavy task asks for an arbitrary-background finite graded dressing
whose exact-coframe restriction is the owned \(F_\phi\). Before constructing
such an object, the phrase “restriction is \(F_\phi\)” needs one typing
correction.

The landed pure-gauge chart obeys
\[
d_f(\phi+c)=d_f\phi
\]
for a constant RoleSpace vector \(c\), while
\[
\boxed{
F_{\phi+c}
=
F_\phi R_c,
\qquad
R_c
=
\exp\!\left(\sum_a c^aD_a\right).
}
\tag{43.1}
\]

For \(L\ge3\), the centered differences
\[
D_a=\frac L2(U_a-U_a^{-1})
\]
are nonzero. Hence \(R_c\) is not identically the identity as \(c\) varies.
Therefore:

\[
\boxed{
\text{there is no single-valued map }e\mapsto F_e
\text{ which equals every }F_\phi
\text{ whenever }e=d_f\phi.
}
\tag{43.2}
\]

The exception \(L=2\), where \(U_a=U_a^{-1}\) and hence \(D_a=0\), does not
remove the general typing issue.

This is not an obstruction to the descended objects already used by D0.

Because
\[
U_a^T=U_a^{-1},
\]
one has
\[
D_a^T=-D_a.
\]
The \(D_a\) commute, so \(R_c\) is orthogonal:
\[
R_c^TR_c=I.
\]
It also commutes with every archive translation \(U_r\).

Consequently
\[
F_{\phi+c}U_rF_{\phi+c}^{-1}
=
F_\phi U_rF_\phi^{-1},
\tag{43.3}
\]
and
\[
F_{\phi+c}^{-T}F_{\phi+c}^{-1}
=
F_\phi^{-T}F_\phi^{-1}.
\tag{43.4}
\]

Thus both owned pure-gauge outputs

\[
\ell_{d_f\phi,r}
=
F_\phi U_rF_\phi^{-1}
\]
and
\[
W^{\rm gr}_{d_f\phi}
=
F_\phi^{-T}F_\phi^{-1}
\]
depend only on the exact coframe \(h=d_f\phi\), while \(F_\phi\) itself is a
right torsor under the constant orthogonal translation group generated by the
\(D_a\).

The correct arbitrary-background target must therefore be one of:

1. a gauge-fixed representative \(F_e\);
2. the right-orthogonal torsor class \([F_e]\);
3. a background-groupoid trivialization carrying the constant isotropy
   explicitly.

Literal equality to all representatives \(F_\phi\) is over-typed.

---

## 44. Bare finite extension theorem

Once the preceding torsor issue is respected, finite existence itself is easy.

Let
\[
\mathcal E
\]
be the finite raw-coframe vector space and
\[
\mathcal G=\operatorname{im}d_f\subset\mathcal E
\]
the exact-coframe subspace.

Choose:

- a linear retraction
  \[
  P:\mathcal E\to\mathcal G,
  \qquad P|_{\mathcal G}=I;
  \]
- a linear potential section
  \[
  \sigma:\mathcal G\to\Phi_0
  \]
  into a chosen complement \(\Phi_0\) of the constant potentials, with
  \[
  d_f\sigma(h)=h.
  \]

Such choices always exist in finite dimension. They are not claimed canonical
or frame-equivariant.

For
\[
e\in\mathcal E,
\]
write
\[
h=Pe,
\qquad
t=(I-P)e.
\]
The owned first jet is linear, so
\[
H(e)=H(h)+H(t).
\]

On the open domain where \(\sigma(h)\) lies in the owned pure-gauge chart,
define
\[
F_h^{0}:=F_{\sigma(h)},
\qquad
W_h^{\rm gr}:=(F_h^0)^{-T}(F_h^0)^{-1}.
\]

Now define the symmetric transverse factor
\[
\boxed{
E_t:=I+\frac12H(t).
}
\tag{44.1}
\]
Restrict to the open finite domain where \(E_t\) is invertible, and set
\[
\boxed{
F^{P,\sigma}_e
:=
E_t^{-1}F_h^0.
}
\tag{44.2}
\]

This is an explicit finite arbitrary-coframe dressing representative.

### Exact specialization

If \(e=h\in\mathcal G\), then \(t=0\) and
\[
E_t=I.
\]
Therefore
\[
\boxed{
F^{P,\sigma}_h=F_{\sigma(h)}.
}
\tag{44.3}
\]

This is an exact gauge-fixed representative of the owned pure-gauge torsor.
By (43.3)–(43.4), it reproduces the owned pure-gauge horizontal letters and
constitutive form for **every** potential representative of \(h\).

### Induced constitutive form

Define
\[
W^{P,\sigma}_e
=
(F^{P,\sigma}_e)^{-T}(F^{P,\sigma}_e)^{-1}.
\]
A direct inverse-transpose calculation gives
\[
\boxed{
W^{P,\sigma}_e
=
E_t^T\,W_h^{\rm gr}\,E_t.
}
\tag{44.4}
\]
Since \(H(t)\) is self-adjoint, \(E_t^T=E_t\).

Whenever \(W_h^{\rm gr}\) is positive definite, (44.4) stays positive definite
on the invertible \(E_t\) domain.

### Full owned first derivative

At flat,
\[
F_0^0=I,
\qquad
W_0^{\rm gr}=I.
\]
On exact directions the owned chart gives
\[
D W_0^{\rm gr}[h]=H(h).
\]
The transverse congruence contributes
\[
\frac12H(t)+\frac12H(t)=H(t).
\]
Hence
\[
\boxed{
D W^{P,\sigma}_0[e]
=
H(h)+H(t)
=
H(e).
}
\tag{44.5}
\]

Thus a finite dressing with exact pure-gauge specialization and the complete
owned \(H(e)\) first derivative **exists noncanonically** on an explicit open
arbitrary-coframe domain.

This construction uses neither the centered metric readout nor an inverse
solder. Therefore the raw \(L=2\) Nyquist and \(L=3\) corner directions remain
present in the first derivative exactly through the already-owned \(H(e)\).

No claim of bounded-stencil locality is made: inversion of \(E_t\) and the
pure-gauge \(F_\phi\) are finite global operators.

---

## 45. Exact path and background-groupoid composition do not select the extension

For any invertible dressing \(F_e\), define the horizontal letter
\[
\boxed{
\ell_{e,r}=F_eU_rF_e^{-1}.
}
\tag{45.1}
\]
Then every labelled path word is a product of actual invertible letters.
Append and reverse are therefore exact by associativity and inversion.

Likewise define the background comparison
\[
\boxed{
R(e_2,e_1)
=
F_{e_2}F_{e_1}^{-1}.
}
\tag{45.2}
\]
Then
\[
R(e_3,e_2)R(e_2,e_1)=R(e_3,e_1),
\qquad
R(e_2,e_1)^{-1}=R(e_1,e_2).
\tag{45.3}
\]

Hence exact labelled-path composition and exact pair-groupoid background
composition are automatic once a finite invertible \(F_e\) is chosen.

They do not by themselves select \(F_e\).

This is important because composition was one of the candidate constraints
which might have been expected to remove the transverse ambiguity. It does
not.

---

## 46. The complete first-order skew freedom survives exact finite composition

Let
\[
A:\ker P\to\operatorname{End}(\mathcal M)
\]
be any linear skew-adjoint map on the matter carrier:
\[
A(t)^T=-A(t).
\]

On the open domain where
\[
I-\frac12A(t)
\]
is invertible, form the Cayley orthogonal factor
\[
\boxed{
O_A(t)
=
\left(I-\frac12A(t)\right)^{-1}
\left(I+\frac12A(t)\right).
}
\tag{46.1}
\]
Then
\[
O_A(t)^TO_A(t)=I,
\qquad
O_A(0)=I,
\qquad
D O_A(0)[t]=A(t).
\]

Define the family
\[
\boxed{
F^{P,\sigma,A}_e
=
E_t^{-1}O_A(t)F_h^0.
}
\tag{46.2}
\]

Every member has:

- exact flat identity;
- exact gauge-fixed pure-gauge specialization;
- exact labelled-path append/reverse;
- exact background pair-groupoid composition.

Its flat tangent generator is
\[
G(e)
=
G_{\sigma(h)}
-\frac12H(t)
+A(t).
\tag{46.3}
\]
Therefore
\[
G(e)+G(e)^T
=
-H(h)-H(t)
=
-H(e),
\]
so
\[
\boxed{
D W_0[e]=H(e)
}
\tag{46.4}
\]
for **every** skew choice \(A\).

Thus the entire transverse skew-generator freedom anticipated by the finite
graded dressing brief survives exact finite composition.

Choosing
\[
A_\lambda=\lambda A_0
\]
for any nonzero transverse skew map \(A_0\) gives a continuous one-parameter
family of distinct finite dressings with the same exact pure-gauge
specialization and the same owned constitutive first derivative.

Consequently:
\[
\boxed{
\text{pure-gauge exactness}
+
DW_0=H
+
\text{exact path/background composition}
\quad\not\Rightarrow\quad
\text{unique finite dressing}.
}
\tag{46.5}
\]

The nonselection is not merely second-order freedom. It is already a literal
first-order skew modulus on transverse raw-coframe directions.

---

## 47. What remains after the bare construction

The construction above does **not** complete
\`EXP-A4D-FINITE-GRADED-COFRAME-DRESSING\`.

It identifies the surviving primitive more narrowly.

The arbitrary choices are now explicit:

1. the retraction
   \[
   P:\mathcal E\to\operatorname{im}d_f;
   \]
2. the potential gauge section \(\sigma\);
3. the transverse skew/orthogonal factor \(A\);
4. unrestricted higher-order transverse modifications which vanish to first
   order.

The exact path and background composition laws remove none of these.

The task's remaining nontrivial requirements therefore concentrate in:

- frame/observer covariance of the splitting and skew law;
- compatibility with the fixed located \(J\) / dual channel;
- compatibility with the already-selected solder–Cartan mismatch and
  \(T_\kappa\);
- any additional locality/support requirement one decides to impose.

In particular, a frame-covariant construction requires either an equivariant
retraction/section or a genuinely groupoid-valued replacement. The current
repository does not own such an equivariant retraction of arbitrary raw
coframes onto the exact-coframe orbit.

So the next primitive is no longer “some finite \(F_e\) exists.” It is:

\[
\boxed{
\text{an equivariant exact-orbit retraction / transverse orthogonal law}.
}
\tag{47.1}
\]

Whether the existing frame/observer structure selects it, or terminally fails
to do so, is the next hard classification.

---

## 48. Interaction with the rank/holonomy resolution

The bare coframe dressing (44.2) is a function of \(e\) and does not by itself
repair or worsen the A/e rank-transition seam.

The mixed matter coupling is different.

If the elementary affine-sensitive factor uses the selected mismatch
\[
T_{\kappa(A,e)},
\]
then §§34–42 still apply:

- on a stable unresolved family, \(\kappa\) is continuous and can be inserted;
- on a rank/holonomy-resolved background, use
  \[
  T_{\widetilde\kappa(A,e,\Xi)};
  \]
- on an unrestricted unresolved background, the no-go of §41 remains.

No choice of the transverse skew factor \(A(t)\) changes this conclusion,
because \(T_\kappa\) is injective in \(\kappa\), and conjugation by the same
invertible dressing cannot identify two distinct mismatch values.

Therefore the finite graded dressing and the stability resolution are
orthogonal pieces of the eventual mixed package:

\[
\boxed{
\text{coframe dressing datum}
\quad+\quad
\text{stable/resolved mismatch datum}.
}
\tag{48.1}
\]

Neither replaces the other.

---

## 49. Subterminal of this forward iteration

The one-step-forward research result is:

\[
\boxed{
\texttt{FINITE-GRADED-DRESSING-BARE-EXTENSIONS-CONSTRUCTED-
EQUIVARIANT-SELECTION-OPEN}.
}
\tag{49.1}
\]

This is a subterminal inside the current stability memo, not a claim that the
separate dressing task has been executed.

What is now established is stronger than the previous frontier statement:

- literal \(e\mapsto F_e=F_\phi\) is over-typed because \(F_\phi\) carries a
  constant-potential orthogonal torsor;
- the descended pure-gauge \(W\) and horizontal letters are coframe-defined;
- after any finite-dimensional exact-orbit retraction and gauge section, an
  explicit finite arbitrary-coframe dressing exists;
- its induced constitutive form has the complete owned first derivative
  \(H(e)\);
- exact labelled-path and background composition are automatic;
- the transverse skew generator remains completely unselected by those laws;
- the hard next question is covariance/duality/mismatch compatibility, not
  bare finite existence.

This is the correct starting point for the actual finite graded dressing task.


---

## 50. Exact bare-dressing checker

This independent rational checker verifies the finite algebra used in
§§43–46: torsor descent under an orthogonal commuting right factor, the
explicit transverse congruence extension, the full first derivative,
Cayley skew freedom, path-period composition, and background pair-groupoid
composition.

\`\`\`python
from fractions import Fraction as Q

checks = 0
def ck(x, label):
    global checks
    checks += 1
    if not x:
        raise AssertionError(label)

def eye(n=2):
    return [[Q(i == j) for j in range(n)] for i in range(n)]
def tr(a):
    return [list(c) for c in zip(*a)]
def add(a,b):
    return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sub(a,b):
    return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sc(q,a):
    return [[Q(q)*x for x in r] for r in a]
def mul(a,b):
    return [[sum((x*y for x,y in zip(r,c)), Q(0))
             for c in tr(b)] for r in a]
def inv(a):
    n=len(a)
    aug=[a[i]+eye(n)[i] for i in range(n)]
    for j in range(n):
        p=next(i for i in range(j,n) if aug[i][j])
        aug[j],aug[p]=aug[p],aug[j]
        q=aug[j][j]
        aug[j]=[x/q for x in aug[j]]
        for i in range(n):
            if i != j and aug[i][j]:
                q=aug[i][j]
                aug[i]=[x-q*y for x,y in zip(aug[i],aug[j])]
    return [r[n:] for r in aug]

I=eye()
G=[[Q(0),Q(1)],[Q(0),Q(0)]]
Hh=sc(-1,add(G,tr(G)))
Ht=[[Q(2),Q(0)],[Q(0),Q(-2)]]

h=Q(1,5)
t=Q(1,7)

Fg=add(I,sc(h,G))
E=add(I,sc(t/2,Ht))
F=mul(inv(E),Fg)

Finv=inv(F)
W=mul(tr(Finv),Finv)

Fginv=inv(Fg)
Wg=mul(tr(Fginv),Fginv)

ck(W==mul(tr(E),mul(Wg,E)),
   'finite transverse congruence')
ck(Fg==add(I,sc(h,G)),
   'exact pure representative')
ck(mul(F,inv(F))==I,
   'finite dressing invertible')

# Direction alpha*h + beta*t at flat.
alpha=Q(2)
beta=Q(3)
Fdot=add(sc(alpha,G),sc(-beta/2,Ht))
Wdot=sc(-1,add(tr(Fdot),Fdot))
ck(Wdot==add(sc(alpha,Hh),sc(beta,Ht)),
   'full first derivative H')

K=[[Q(0),Q(-1)],[Q(1),Q(0)]]
A=sc(t,K)
O=mul(inv(sub(I,sc(Q(1,2),A))),
      add(I,sc(Q(1,2),A)))

ck(mul(tr(O),O)==I,
   'Cayley skew factor orthogonal')

FA=mul(inv(E),mul(O,Fg))
ck(FA!=F,
   'transverse skew family distinct')

# Over zero exact component the orthogonal skew factor is invisible to W
# even at finite amplitude.
F0=inv(E)
FA0=mul(inv(E),O)
W0=mul(tr(inv(F0)),inv(F0))
WA0=mul(tr(inv(FA0)),inv(FA0))
ck(W0==WA0,
   'finite skew invisibility over flat exact component')

U=[[Q(0),Q(1)],[Q(1),Q(0)]]
ell=mul(F,mul(U,inv(F)))
ck(mul(ell,ell)==I,
   'conjugated path period exact')

h2=Q(2,5)
Fg2=add(I,sc(h2,G))
F2=mul(inv(E),Fg2)
R21=mul(F2,inv(F))
R12=mul(F,inv(F2))
ck(mul(R12,R21)==I,
   'background pair-groupoid inverse/composition')

# Abstract constant-potential torsor algebra: R is orthogonal and commutes
# with the horizontal translation Uc.
R=[[Q(-1),Q(0)],[Q(0),Q(1)]]
Uc=[[Q(1),Q(0)],[Q(0),Q(-1)]]

ck(mul(tr(R),R)==I,
   'right torsor factor orthogonal')
ck(mul(R,Uc)==mul(Uc,R),
   'right torsor factor commutes with horizontal translation')

Fp=mul(Fg,R)
Wp=mul(tr(inv(Fp)),inv(Fp))
ellp=mul(Fp,mul(Uc,inv(Fp)))
ellg=mul(Fg,mul(Uc,inv(Fg)))

ck(Wp==Wg,
   'constitutive form descends through torsor')
ck(ellp==ellg,
   'horizontal letter descends through torsor')

print(f'PASS: {checks} exact rational bare-dressing assertions')
\`\`\`

Expected output:

\`\`\`text
PASS: 13 exact rational bare-dressing assertions
\`\`\`

The three embedded exact suites now test complementary layers:

- 78 assertions: original continuity and hostile finite controls;
- 27 assertions: projector-resolution and continuous-selector no-go;
- 13 assertions: bare finite dressing extension and surviving skew modulus.


---

## 51. Full raw-solder frame covariance destroys the exact-coframe subspace

The bare construction of §44 used an arbitrary retraction onto
\[
\mathcal G=\operatorname{im}d_f.
\]
The remaining question was whether the owned frame structure might select such
a retraction equivariantly.

The landed raw-solder frame owner answers this negatively for a coframe-only
retraction.

The exact full-solder action is
\[
\boxed{
T_\Lambda(e)
=
(\eta+e)\Lambda-\eta
}
\tag{51.1}
\]
sitewise, with \(\Lambda_x\) acting on the right.

Even for a constant Lorentz frame \(\Lambda\), the flat perturbation transforms
as
\[
\boxed{
T_\Lambda(0)=\eta\Lambda-\eta.
}
\tag{51.2}
\]

Choose the exact rational A/B boost
\[
\Lambda=
\begin{pmatrix}
5/3&4/3&0&0\\
4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix},
\qquad
\eta=\operatorname{diag}(1,-1,-1,-1).
\]
It satisfies
\[
\Lambda^T\eta\Lambda=\eta.
\]
But
\[
\eta\Lambda-\eta
=
\begin{pmatrix}
2/3&4/3&0&0\\
-4/3&-2/3&0&0\\
0&0&0&0\\
0&0&0&0
\end{pmatrix}
\ne0.
\tag{51.3}
\]

This is a spatially constant raw coframe perturbation.

Every periodic exact coframe
\[
h=d_f\phi
\]
has zero period in each Role direction:
\[
\sum_{j=0}^{L-1}h_r(x+jr)=0.
\tag{51.4}
\]
A nonzero constant component has period \(Lh_r\ne0\). Therefore the field
(51.3) is not in \(\operatorname{im}d_f\).

Hence
\[
\boxed{
T_\Lambda(\operatorname{im}d_f)
\not\subseteq
\operatorname{im}d_f.
}
\tag{51.5}
\]

The exact pure-gauge coframe orbit is not invariant under the full raw-solder
frame action.

This is consistent with the repository's existing separation: a raw solder
frame change and an affine/background gauge move are different operations
until a joint typed bridge is supplied.

---

## 52. No full-frame-equivariant coframe-only exact-orbit retraction

Suppose one tried to strengthen the bare dressing construction with a
retraction
\[
P:\mathcal E\to\mathcal G
\]
which is equivariant under the full raw-solder frame action and fixes every
exact coframe.

Any meaningful equivariance of such a retraction would require
\[
P(T_\Lambda h)=T_\Lambda P(h)=T_\Lambda h
\tag{52.1}
\]
for
\[
h\in\mathcal G.
\]
The left side lies in \(\mathcal G\) by definition of \(P\), so (52.1)
forces
\[
T_\Lambda h\in\mathcal G.
\]

Taking
\[
h=0
\]
and the rational boost of §51 gives a contradiction to (51.5).

Therefore:
\[
\boxed{
\text{there is no coframe-only retraction onto }\operatorname{im}d_f
\text{ which is equivariant under the full raw-solder frame action}.
}
\tag{52.2}
\]

This is stronger than saying the particular orthogonal projection is not
covariant. **No** retraction with that source and target can satisfy the full
frame law, because the target subspace itself is not invariant.

Consequently the arbitrary choice \(P\) in §44 cannot be repaired by searching
for a more clever coframe-only canonical projector.

---

## 53. The next dressing object is necessarily joint-background / groupoid typed

The failure of §52 identifies why the dressing brief explicitly allowed a
“correctly typed background-groupoid equivalent.”

The repository already contains the relevant covariance pattern on the solder
side. A transported solder center becomes frame-covariant only after supplying
a row pull
\[
R_{x-r\to x}
\]
which transforms as
\[
\boxed{
R'_{x-r\to x}
=
\Lambda_{x-r}^{-1}
R_{x-r\to x}
\Lambda_x.
}
\tag{53.1}
\]
With that connection-like datum, the transported center transforms at the
target by the same right frame as the raw solder.

Thus the natural next source object is not
\[
e
\]
alone. It is at least a joint background carrying the transport needed to
compare frames between sites — in current repository language, naturally a
package built from
\[
(A,e)
\]
and, for the mixed selected channel, the stability datum
\[
\Xi.
\]

The correct forward target is therefore schematically
\[
\boxed{
\mathcal F_{A,e,\Xi,n}
}
\tag{53.2}
\]
or a background-groupoid torsor/cocycle equivalent, with the dependence
reduced when the extra arguments are irrelevant.

This does **not** assert that all four displayed arguments must enter every
factor. It records the minimal typing lesson:

- raw frame covariance cannot be solved by an \(e\)-only retraction to the
  exact orbit;
- the already-owned mismatch is intrinsically joint A/e data;
- the selected mismatch is stable only on the stable domain or after adding
  \(\Xi\);
- observer covariance belongs to the matter pairing/lift, not to the
  coefficient projector.

Any final construction may factor these pieces, but it cannot identify them
silently.

---

## 54. Revised frontier after one full forward iteration

The combined results §§43–53 replace the vague question

> “does an arbitrary-background finite graded dressing exist?”

by a much narrower sequence.

### Closed at research level

A bare finite invertible extension exists after arbitrary finite-dimensional
splitting choices. It can be made to satisfy:

- flat identity;
- exact gauge-fixed pure-gauge specialization;
- the owned descended pure-gauge horizontal letters and constitutive form;
- complete \(DW_0=H(e)\);
- raw Nyquist/corner first-jet retention;
- exact labelled-path append/reverse;
- exact background pair-groupoid composition.

The full transverse skew modulus is explicit.

### Terminal negative

A coframe-only retraction onto the exact orbit cannot be equivariant under the
owned full raw-solder frame action:
\[
\boxed{
\texttt{COFRAME-ONLY-FRAME-EQUIVARIANT-EXACT-ORBIT-RETRACTION-NOGO}.
}
\tag{54.1}
\]

### Exact next primitive

What remains is to construct or obstruct a **joint-background equivariant
trivialization/cocycle** which:

1. reduces to the pure-gauge torsor \(F_\phi\);
2. has constitutive first derivative \(H(e)\);
3. uses the transformed connection/row-pull data required by frame covariance;
4. keeps the transverse skew modulus explicit until covariance/duality selects
   it;
5. couples to \(T_\kappa\) only on the stable or resolved mismatch domain;
6. remains compatible with the fixed located \(J\).

This is a sharper starting brief than “construct \(F_e\).”

The mathematical pressure has therefore advanced one complete layer:

\[
\boxed{
\begin{array}{c}
\text{pointwise relative A/e relation}\\
\downarrow\\
\text{stability / rank-holonomy resolution}\\
\downarrow\\
\text{bare finite dressing exists noncanonically}\\
\downarrow\\
\textbf{joint-background equivariant dressing/groupoid law is now the first
unresolved constitutive seam}.
\end{array}}
\tag{54.2}
\]
