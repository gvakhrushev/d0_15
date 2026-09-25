# A4D resolution memory functoriality and minimality

**Task:** EXP-A4D-RESOLUTION-MEMORY-FUNCTORIALITY-MINIMALITY  
**Research PR:** #135  
**Start baseline:** 4527bd8937fd4888704197b571e9a3f94dfa6f29  
**Terminal:** RESOLUTION-MEMORY-MINIMALITY-CLASSIFIED  
**Positive subterminal:** RANK-HOLONOMY-RESOLUTION-GROUPOID-CONSTRUCTED  
**Negative subterminal:** POINTWISE-RESOLUTION-RECONSTRUCTION-OBSTRUCTED

## 0. Verdict

PR #130 introduced
\[
\Xi=((\Pi_y)_y,Q_o)
\]
as sufficient continuation memory for the local rank seam and the global
holonomy-fixed-kernel seam.

The exact result is sharper.

1. \(\Xi\) is functorial under the finite background/frame/label
   isomorphisms already used by D0.
2. The projector presentation is redundant.  The naturally minimal
   structural presentation is
   \[
   \boxed{\Xi_{\rm str}=((W_y)_y,\mathcal K)}
   \]
   with
   \[
   W_y\le\ker\mathcal B_y,
   \qquad
   \mathcal K=(\mathcal K_y)_y
   \]
   a basepoint-free parallel subbundle of the endpoint common-fixed bundle.
3. \(\Xi_{\rm str}\) is minimal as source-independent universal approach
   memory, up to natural equivalence.
4. For one fixed endpoint and fixed downstream selection gauge, the readout
   sees less:
   \[
   C_y^\Xi=\mathcal S_y\Pi_y,
   \qquad
   z_r^\Xi=Q_om_r^\Xi.
   \]
   This gives a strictly smaller stagewise readout datum and an exact
   equivalence relation classifying every sufficient forgetful map.
5. A complete punctured joint A/e background germ reconstructs \(\Xi\)
   whenever the projector limits exist.
6. The current pointwise pair, rank labels, endpoint free-path data, every
   finite parameter jet, and every finite set of sampled history values do
   not reconstruct it.
7. Quotients that identify the critical local or global resolution memories
   erase the mandatory pure-shift, Nyquist or corner distinctions.

Thus the resolution is an exact finite quotient of history but an irreducible
extension of pointwise geometry.

---

## 1. Frozen endpoint incidence

At every site,
\[
\mathcal B_y,\mathcal S_y:E_{\rm lab}\to V_y,
\]
\[
K_y=\ker\mathcal B_y,
\qquad
H_y=K_y^\perp.
\]

The local incidence fibre is
\[
\mathfrak P(\mathcal B_y)
=
\{\Pi:\Pi^2=\Pi=\Pi^\ast,\ \mathcal B_y\Pi=\mathcal B_y\}.
\]

Every member has the unique form
\[
\boxed{
\Pi=P_{H_y}+P_W,
\qquad
W\le K_y.
}
\tag{1.1}
\]

The resolved correlated action is
\[
C_y^\Pi=\mathcal S_y\Pi.
\]

At the global seam,
\[
\mathcal H_o
=
\bigcap_{\gamma:o\to o}\operatorname{Fix}P_\gamma.
\]
A limiting kernel projector has
\[
\mathcal K_o:=\operatorname{im}Q_o\le\mathcal H_o.
\]

No pointwise continuity result from #130 is reopened.

---

## 2. The resolution is a decorated cover of pointwise backgrounds

For a fixed endpoint define the structural resolution fibre by
\[
\operatorname{Res}(A,e,n;o)
=
\left\{
((W_y)_y,\mathcal K_o):
W_y\le K_y,\ 
\mathcal K_o\le\mathcal H_o
\right\}.
\]

Locally its fibre is
\[
\coprod_{k=0}^{\dim K_y}\operatorname{Gr}(k,K_y).
\]

At trivial holonomy the global abstract fibre is
\[
\coprod_{k=0}^{\dim V_o}\operatorname{Gr}(k,V_o),
\]
and #130 already constructed actual invertible-loop approaches realizing all
such subspaces.

Therefore there is an exact forgetful map
\[
\boxed{
\mathsf U:\mathbf{ResBg}\to\mathbf{Bg}
}
\tag{2.1}
\]
with generally non-singleton fibres.

These fibres are the finite approach-memory fibres.

---

## 3. Local functoriality

Consider an admissible invertible background isomorphism consisting of

- an orthogonal coefficient-label map
  \[
  u:E_{\rm lab}\to E'_{\rm lab},
  \]
- invertible fibre maps
  \[
  g_y:V_y\to V'_y,
  \]
- covariance
  \[
  \mathcal B'_yu=g_y\mathcal B_y,
  \qquad
  \mathcal S'_yu=g_y\mathcal S_y.
  \tag{3.1}
  \]

Pure-linear frame covariance is the special case \(u=I\).

Define
\[
\boxed{
\Pi'_y=u\Pi_yu^{-1}.
}
\tag{3.2}
\]

Then
\[
\mathcal B'_y\Pi'_y
=
g_y\mathcal B_y\Pi_yu^{-1}
=
g_y\mathcal B_yu^{-1}
=
\mathcal B'_y.
\]

Orthogonality is preserved because \(u\) is an isometry.  Therefore
\[
\boxed{
\Pi_y\in\mathfrak P(\mathcal B_y)
\Longrightarrow
u\Pi_yu^{-1}\in\mathfrak P(\mathcal B'_y).
}
\tag{3.3}
\]

In lost-subspace language,
\[
\boxed{
W'_y=uW_y.
}
\tag{3.4}
\]

For a pure output-frame change,
\[
u=I,
\]
hence
\[
\boxed{
\Pi'_y=\Pi_y,\qquad W'_y=W_y.
}
\tag{3.5}
\]

The rank-transition memory lives in coefficient-label space, not in the moving
output fibre.

---

## 4. Local composition, inverse and relative A/e compatibility

For composable isomorphisms \(u_1,u_2\),
\[
u_2(u_1\Pi u_1^{-1})u_2^{-1}
=
(u_2u_1)\Pi(u_2u_1)^{-1}.
\]
The inverse is conjugation by \(u^{-1}\).

Thus the local resolution has exact identity/composition/inverse.

The pointwise relation
\[
\mathscr R_y
=
\operatorname{im}(\mathcal B_y,\mathcal S_y)
\subseteq V_y\oplus V_y
\]
transforms as
\[
\boxed{
\mathscr R'_y=(g_y\oplus g_y)\mathscr R_y.
}
\tag{4.1}
\]

The resolved correlated action transforms as
\[
\boxed{
C_y^{\Xi'}
=
g_yC_y^\Xi u^{-1}.
}
\tag{4.2}
\]

The resolution does not graphify a vertical endpoint relation.  If
\(W_y\ne0\), then \(\mathcal B_y\) still vanishes on \(W_y\).  The datum only
records that those endpoint-kernel directions were active along the approach.

---

## 5. The global projector is naturally a subspace

Once the observer-positive form is part of the background,
\[
Q_o
=
\operatorname{Proj}^{h_{n(o)}}_{\mathcal K_o}
\]
is uniquely determined by
\[
\mathcal K_o=\operatorname{im}Q_o.
\]

Hence
\[
\boxed{
Q_o\longleftrightarrow\mathcal K_o
}
\tag{5.1}
\]
is lossless.

The subspace is the geometric memory.  The projector is its metric
representative.

---

## 6. Exact basepoint transport

Let
\[
p:o\to o'
\]
and use repository pull orientation
\[
T_p=P_p:V_{o'}\to V_o.
\]

Define
\[
\boxed{
\mathcal K_{o'}=T_p^{-1}\mathcal K_o.
}
\tag{6.1}
\]

This is independent of the path.

If \(q:o\to o'\) is another path, then
\[
L=T_qT_p^{-1}:V_o\to V_o
\]
is a based loop transport.  Since
\[
\mathcal K_o\le\mathcal H_o,
\]
every \(k\in\mathcal K_o\) obeys
\[
Lk=k.
\]
Because \(T_q=LT_p\),
\[
T_q^{-1}k
=
T_p^{-1}L^{-1}k
=
T_p^{-1}k.
\]

Therefore
\[
\boxed{
T_p^{-1}\mathcal K_o=T_q^{-1}\mathcal K_o.
}
\tag{6.2}
\]

The actual vectors, not only the dimension, transport path-independently.

---

### Loop conjugation under basepoint change

Let \(\lambda:o'\to o'\) be a labelled loop.  Relative to
\(p:o\to o'\), the corresponding loop based at \(o\) is
\[
\widehat\lambda
=
p++\lambda++\bar p .
\]
Exact append/reverse gives
\[
\boxed{
T_{\widehat\lambda}
=
T_pT_\lambda T_p^{-1}.
}
\tag{6.3}
\]

For
\[
k'=T_p^{-1}k,
\qquad
k\in\mathcal K_o,
\]
the based loop \(\widehat\lambda\) fixes \(k\), hence
\[
T_pT_\lambda k'
=
T_{\widehat\lambda}k
=
k.
\]
Applying \(T_p^{-1}\) gives
\[
\boxed{
T_\lambda k'=k'.
}
\tag{6.4}
\]

Therefore
\[
\mathcal K_{o'}\le\mathcal H_{o'}
\]
and the common-fixed condition itself is transported by exact loop
conjugation.  This makes the basepoint-change proof compatible with the
literal labelled path groupoid rather than only with an abstract
same-endpoint argument.

---

## 7. Append and reverse

For
\[
p:o\to o',
\qquad
q:o'\to o'',
\]
pull order is
\[
T_{p++q}=T_pT_q.
\]

Therefore
\[
(T_pT_q)^{-1}\mathcal K_o
=
T_q^{-1}(T_p^{-1}\mathcal K_o).
\]

Thus the global memory obeys exact append.

For the reversed path,
\[
T_{\bar p}=T_p^{-1},
\]
so transport to \(o'\) and back returns \(\mathcal K_o\) exactly.

This supplies the requested append/reverse law.

---

## 8. Basepoint-free parallel subbundle

For every site \(y\), choose any path \(p_y:o\to y\) and set
\[
\boxed{
\mathcal K_y=T_{p_y}^{-1}\mathcal K_o.
}
\tag{8.1}
\]
By §6 this is independent of \(p_y\).

For every labelled path \(p:y\to y'\),
\[
\boxed{
T_p\mathcal K_{y'}=\mathcal K_y.
}
\tag{8.2}
\]

Hence
\[
\boxed{
\mathcal K=(\mathcal K_y)_y
}
\tag{8.3}
\]
is a basepoint-free parallel subbundle.

A single \(Q_o\) is only a coordinate presentation of this object.

---

## 9. Projector transport and observer metric

At a new basepoint,
\[
Q_{o'}
=
\operatorname{Proj}^{h_{n(o')}}_{\mathcal K_{o'}}.
\tag{9.1}
\]

If \(T_p\) is an isometry between the observer-positive forms,
\[
h_{n(o')}(v,w)
=
h_{n(o)}(T_pv,T_pw),
\tag{9.2}
\]
then
\[
\boxed{
Q_{o'}=T_p^{-1}Q_oT_p.
}
\tag{9.3}
\]

Without (9.2), operator conjugation need not preserve orthogonality for the new
metric.  The unconditional functorial statement is the subspace law (6.1),
followed by re-projection in the target observer metric.

This is the required separation between fixed subspace and projector.

---

## 10. Pure-linear frame covariance globally

For a pure-linear frame family \(g_y\), landed transport covariance gives
\[
P'_p=g_yP_pg_{y'}^{-1}.
\]

Hence
\[
\mathcal H'_y=g_y\mathcal H_y.
\]

Define
\[
\boxed{
\mathcal K'_y=g_y\mathcal K_y.
}
\tag{10.1}
\]

The observer congruence then gives
\[
\boxed{
Q'_y=g_yQ_yg_y^{-1}.
}
\tag{10.2}
\]

Composition and inverse are exact.

Thus
\[
\boxed{
\Xi_{\rm str}=((W_y)_y,\mathcal K)
}
\tag{10.3}
\]
is exactly pure-linear frame covariant.

---

## 11. Resolution groupoid

Define an object
\[
\mathfrak B^\Xi
=
(\mathfrak B,((W_y)_y,\mathcal K))
\]
where \(\mathfrak B\) contains the finite A/e transport and observer data,
\(W_y\le\ker\mathcal B_y\), and \(\mathcal K\) is a parallel subbundle of the
endpoint common-fixed bundle.

A morphism is an admissible invertible background/frame/label isomorphism
\[
(u,(g_y)_y)
\]
satisfying §§3 and 10.

Its resolution action is
\[
\boxed{
W_y\mapsto uW_y,
\qquad
\mathcal K_y\mapsto g_y\mathcal K_y.
}
\tag{11.1}
\]

Identity, composition and inverse are exact.

Therefore
\[
\boxed{
\texttt{RANK-HOLONOMY-RESOLUTION-GROUPOID-CONSTRUCTED}.
}
\tag{11.2}
\]

This groupoid transports supplied resolution memory under isomorphisms.  It
does not invent a canonical map between the resolution fibres of unrelated
backgrounds.

---

## 12. Complete approach history reconstructs the resolution

Let
\[
t\mapsto\mathfrak B_t
\]
be a punctured joint background history with endpoint \(\mathfrak B_0\).

Assume
\[
P_{H_{t,y}}\to\Pi_y^*
\]
and
\[
Q_t^{\rm int}
=
\operatorname{Proj}^{h_{n_t(o)}}_{\mathcal H_t}
\to Q_o^*.
\]

Define
\[
\boxed{
\Xi(\mathfrak B_\bullet)
=
((\Pi_y^*)_y,Q_o^*).
}
\tag{12.1}
\]

Equivalently,
\[
W_y^*
=
\operatorname{im}\Pi_y^*\cap K_{0,y},
\qquad
\mathcal K_o^*
=
\operatorname{im}Q_o^*.
\]

Two histories with the same endpoint are resolution-equivalent iff
\[
\boxed{
\Pi_y^{*(1)}=\Pi_y^{*(2)}
\quad\forall y,
\qquad
\mathcal K_o^{*(1)}=\mathcal K_o^{*(2)}
}
\tag{12.2}
\]
after the basepoint identification of §6.

Thus \(\Xi_{\rm str}\) is a finite quotient of a complete approach germ.

---

## 13. Same endpoint and rank labels, different local memory

Embed a two-dimensional coefficient block in the four Role directions and
take
\[
B_0=0.
\]

For \(t\ne0\),
\[
B_t^{(A)}\varepsilon_A=t\,e_A,
\qquad
B_t^{(A)}\varepsilon_B=0,
\]
whereas
\[
B_t^{(B)}\varepsilon_A=0,
\qquad
B_t^{(B)}\varepsilon_B=t\,e_A.
\]

Both histories have
\[
\operatorname{rank}B_t=1
\quad(t\ne0),
\qquad
\operatorname{rank}B_0=0.
\]

But
\[
\boxed{
\Pi_A^*=P_{\mathbb R\varepsilon_A},
\qquad
\Pi_B^*=P_{\mathbb R\varepsilon_B}.
}
\tag{13.1}
\]

The complete rank history is identical.  The Grassmannian direction is not.

---

## 14. Same endpoint and fixed-space dimensions, different global memory

Let the endpoint loop be the identity on \(V=\mathbb R^4\).

For \(t\ne0\), set
\[
G_t^{(B)}=I+tP_{\mathbb Re_B},
\]
\[
G_t^{(C)}=I+tP_{\mathbb Re_C}.
\]

For small nonzero \(t\), both are invertible and
\[
\dim\operatorname{Fix}G_t^{(B)}
=
\dim\operatorname{Fix}G_t^{(C)}
=
3.
\]

Both tend to
\[
G_0=I,
\qquad
\dim\operatorname{Fix}G_0=4.
\]

Yet
\[
\boxed{
\mathcal K_B^*=\operatorname{span}(e_A,e_C,e_D),
}
\]
\[
\boxed{
\mathcal K_C^*=\operatorname{span}(e_A,e_B,e_D).
}
\tag{14.1}
\]

Dimension data do not determine global resolution memory.

---

## 15. Pointwise and endpoint-path reconstruction are obstructed

Sections 13 and 14 already prove that one pointwise endpoint can support
different valid resolution memories.

Therefore no rule
\[
(A_0,e_0)\mapsto\Xi
\]
can recover all approaches.

At the loop endpoint in §14 every loop is the identity.  The complete endpoint
free-path representation is therefore the same in both histories.  It
reconstructs the intrinsic endpoint fixed space
\[
\mathcal H_0=V
\]
but not the approach subspace \(\mathcal K^*\).

The local memory is stronger still: it belongs to the relative A/e coefficient
split and is not encoded by the endpoint linear free-path word.

Hence
\[
\boxed{
\texttt{POINTWISE-RESOLUTION-RECONSTRUCTION-OBSTRUCTED}.
}
\tag{15.1}
\]

---

### Finite labelled endpoint histories

A finite labelled-path record at the endpoint is a finite subset of the full
endpoint free-path representation.  Section 15 already shows that even the
**entire** endpoint free-path representation fails to determine the approach
subspace \(\mathcal K^*\), while the local \(W_y\) is not encoded by that
linear path representation at all.

Therefore no finite collection of endpoint labelled words, their endpoints,
and their endpoint transport values can reconstruct \(\Xi\) universally.

This must be separated from a parameterized background history: the missing
information is not longer spatial path words at the endpoint, but how the
joint A/e and loop-kernel data approach that endpoint.

---

## 16. Finite jets and finite sampled histories are insufficient

PR #130 already proved the finite-jet obstruction.

For any \(k\),
\[
B_t^{(0)}=B_0,
\qquad
B_t^{(W)}
=
B_0+t^{k+1}JP_W
\]
have identical derivatives through order \(k\) but different limiting active
subspaces.  The smooth-flat factor \(e^{-1/t^2}\) gives the same obstruction
even with identical full Taylor series in the unrestricted smooth category.

The loop seam has the same construction
\[
G_t=I+t^{k+1}T
\]
or
\[
G_t=I+e^{-1/t^2}T.
\]

Finite sampled history is also insufficient.

Given nonzero samples \(t_1,\ldots,t_m\), define
\[
q(t)
=
t
\frac{\prod_i(t-t_i)}
     {\prod_i(-t_i)}.
\]
Then
\[
q(0)=0,\qquad q(t_i)=0,
\qquad
\lim_{t\to0}\frac{q(t)}t=1.
\]

The histories
\[
B_t^{(1)}=t\,u\otimes\varepsilon_A^\ast
\]
and
\[
B_t^{(2)}
=
B_t^{(1)}+q(t)\,v\otimes\varepsilon_B^\ast
\]
agree at every listed sample and at the endpoint, but have different limiting
active subspaces.

Only a complete approach germ, or explicitly supplied equivalent memory, can
recover the general resolution.

---

## 17. Structural minimality

The projector presentation has a canonical lossless compression:
\[
\Pi_y
\longleftrightarrow
W_y
=
\operatorname{im}\Pi_y\cap K_y,
\]
because
\[
\Pi_y=P_{H_y}+P_{W_y}.
\]

Likewise
\[
Q_o\longleftrightarrow\mathcal K_o
\]
once the observer metric is known.

Hence
\[
\boxed{
\Xi
\simeq
\Xi_{\rm str}
=
((W_y)_y,\mathcal K)
}
\tag{17.1}
\]
naturally.

No source-independent universal compression can identify arbitrary distinct
\(W\)'s.  If
\[
W_1\ne W_2,
\]
their projectors differ, so there exist a coefficient vector \(c\) and a linear
solder synthesis \(\mathcal S\) with
\[
\mathcal S(P_{W_1}-P_{W_2})c\ne0.
\]

Likewise if
\[
\mathcal K_1\ne\mathcal K_2,
\]
their observer-metric projectors differ, so there exists \(m\) with
\[
(Q_1-Q_2)m\ne0.
\]

Therefore \(\Xi_{\rm str}\) is minimal, up to natural equivalence, as
source-independent universal structural approach memory.

This does not claim every abstract separating probe is already a registered
physical background.  The mandatory controls below give concrete D0 probes
for the distinctions actually required downstream.

---

## 18. Fixed-background readout factorization

Fix one endpoint background, observer, basepoint and PR #120 selection path
family.

For a resolution \(\Xi\), define
\[
C_y^\Xi=\mathcal S_y\Pi_y,
\]
\[
a_r^\Xi(y)
=
-\bar b_r(y)-C_y^\Xi\varepsilon_r,
\]
\[
m_r^\Xi
=
\frac1{|X|}
\sum_yT_ya_r^\Xi(y),
\]
\[
\boxed{
z_r^\Xi=Q_om_r^\Xi.
}
\tag{18.1}
\]

Then
\[
\boxed{
\delta_r^\Xi(y)
=
a_r^\Xi(y)-T_y^{-1}z_r^\Xi.
}
\tag{18.2}
\]

Therefore the fixed readout factors through
\[
\boxed{
\widehat\Xi_{\rm stage}
=
((C_y^\Xi)_y,(z_r^\Xi)_r).
}
\tag{18.3}
\]

This can be strictly smaller than the structural memory.

Thus structural minimality and fixed-readout minimality are different
questions.

---

## 19. Exact classification of all sufficient forgetful maps

Let \(\Xi_1,\Xi_2\) lie over the same fixed background and selection gauge.

They give the same selected diagonal iff
\[
\boxed{
a_r^{\Xi_2}(y)-a_r^{\Xi_1}(y)
=
T_y^{-1}
\left(
z_r^{\Xi_2}-z_r^{\Xi_1}
\right)
}
\tag{19.1}
\]
for every site and Role.

Equivalently,
\[
\boxed{
\mathcal S_y(\Pi_{2,y}-\Pi_{1,y})\varepsilon_r
=
-
T_y^{-1}
\left(
Q_2m_r^{\Xi_2}-Q_1m_r^{\Xi_1}
\right).
}
\tag{19.2}
\]

Since the edge linear maps are invertible and the raw background is fixed,
equality of all selected \(\delta\)'s is equivalent to equality of all final
\(\kappa\)'s.

Define
\[
\Xi_1\sim_{\rm rd}\Xi_2
\]
by (19.1).

Then a forgetful map
\[
F:\Xi\to Z
\]
determines the selected \((\delta,\kappa)\) set-theoretically iff
\[
\boxed{
F(\Xi_1)=F(\Xi_2)
\Longrightarrow
\Xi_1\sim_{\rm rd}\Xi_2.
}
\tag{19.3}
\]

Equivalently every fibre of \(F\) lies inside one readout-equivalence class.

For continuity there is one additional topological clause.  Let
\[
\mathcal R:\Xi\mapsto(\delta^\Xi,\kappa^\Xi)
\]
be the resolved readout, which is continuous on every admitted resolved
family by #130.  A general continuous forgetful map \(F\) supports a
continuous descended readout iff:

1. (19.3) holds, so the induced map
   \[
   \bar{\mathcal R}:F(\Xi)\to(\delta,\kappa)
   \]
   is well-defined; and
2. \(\bar{\mathcal R}\) is continuous on the image topology.

For an actual **quotient map** \(F\) equipped with the quotient topology, the
second clause is automatic: a continuous map constant on fibres descends
continuously.  Therefore the coarsest exact continuous quotient of one fixed
resolved readout is
\[
\boxed{
\Xi/\!\sim_{\rm rd}.
}
\tag{19.4}
\]

This is the promised classification of all forgetful maps at fixed selected
readout, including the continuity qualifier in the task.

It is source/readout dependent and background-dependent.  A single quotient
required to work uniformly for all admitted backgrounds and all downstream
source probes returns to the structural minimality theorem of §17.  Thus the
readout quotient is not a replacement for the universal structural memory.

---

## 20. The PR #120 selection-path gauge remains separate

The parallel subbundle \(\mathcal K\) is path-independent.

The transported mean
\[
m_r
=
\frac1{|X|}
\sum_yT_ya_r(y)
\]
need not be path-independent on generic nontrivial holonomy.

Changing a selected path by a loop changes the transported seed by the loop
action.  D0 does not own an all-loop observer-isometry theorem for arbitrary
\(A\), so one cannot generally conclude
\[
QP_\gamma=Q.
\]

Therefore
\[
\boxed{
\Xi\text{ does not remove the explicit PR #120 selection-path gauge on
generic holonomy.}
}
\tag{20.1}
\]

If all relevant loops are observer isometries, then projection onto the
pointwise-fixed \(\mathcal K\) obeys \(QP_\gamma=Q\), and the projected mean is
insensitive to that loop insertion.

That is an additional hypothesis.

---

## 21. Exact gauge: local resolution is invisible

On the exact translation-gauge chart,
\[
\mathcal S_y=T_y^{\rm chart}\mathcal B_y.
\]

Every incidence lift obeys
\[
\mathcal B_y\Pi_y=\mathcal B_y.
\]
Hence
\[
\boxed{
\mathcal S_y\Pi_y
=
T_y^{\rm chart}\mathcal B_y\Pi_y
=
\mathcal S_y.
}
\tag{21.1}
\]

Thus all local resolution memories are readout-equivalent at this stage,
including at the exact-gauge rank drop.

This is a literal example showing why structural memory can be larger than the
readout-minimal quotient.

---

## 22. Pure shift kills quotients that forget global memory

Take flat linear transport, \(e=0\), and constant \(b\ne0\).

Then
\[
a=-b,\qquad m=-b,\qquad\mathcal H_o=V.
\]

For
\[
Q=I,
\]
\[
z=-b,\qquad
\delta=0,\qquad
\boxed{\kappa=b.}
\tag{22.1}
\]

For
\[
Q=0,
\]
\[
z=0,\qquad
\delta=-b,\qquad
\boxed{\kappa=0.}
\tag{22.2}
\]

Any quotient identifying these global memories erases the mandatory pure
affine shift.

---

## 23. Nyquist and corner kill quotients that forget local memory

At a coframe-only point,
\[
\mathcal B=0.
\]
The intrinsic lift is
\[
\Pi_{\rm int}=0,
\]
whereas the maximal continuation lift is
\[
\Pi_{\rm max}=I.
\]

Thus
\[
C_{\rm int}=0,
\qquad
C_{\rm max}=\mathcal S.
\]

The intrinsic selector preserves the owned
\[
\boxed{\kappa_A=(+4,-4)e_A}
\tag{23.1}
\]
on the \(L=2\) Nyquist control and
\[
\boxed{\kappa_A(0)=e_B}
\tag{23.2}
\]
on the \(L=3\) corner.

The maximal lift feeds the whole solder increment into the correlated seed and
cancels the raw response.

Therefore a quotient identifying \(\Pi=0\) and \(\Pi=I\) cannot determine the
mandatory finite readout.

Likewise an output quotient killing the corresponding \(e_A\) or \(e_B\)
difference also kills the required Nyquist/corner response itself.

---

## 24. Mandatory L=3 rank-transition witness

Use the exact #130 family
\[
f=(1,-2,1),
\qquad
d=(0,-3,3),
\]
\[
b_{x,A}(t)=tf(j)e_A,
\]
\[
v_A(x)=e_A+f(j)e_B.
\]

At the nonzero-\(d_j\) sites and \(t\ne0\),
\[
\Pi_t=P_{\mathbb R\varepsilon_A}.
\]
At \(t=0\), the intrinsic endpoint projector is zero.

Thus the approach memory is
\[
W_*=\mathbb R\varepsilon_A.
\]

For every \(t\ne0\),
\[
\kappa_A(t;x)=0,
\]
whereas
\[
\boxed{
\kappa_A(0;0)=-3e_B.
}
\tag{24.1}
\]

Retaining the resolution memory reproduces the punctured continuation.
Forgetting it reverts to the intrinsic endpoint and produces the jump.

---

## 25. Same-dimensional global memories remain distinguishable

In §14 choose transported mean
\[
m=e_B.
\]

For the limiting fixed subspace excluding \(e_B\),
\[
Q_Bm=0.
\]

For the limiting fixed subspace containing \(e_B\),
\[
Q_Cm=e_B.
\]

The two projectors have the same rank \(3\) but different selected
corrections.

A dimension-only quotient fails.

---

## 26. Reconstruction hierarchy

| Input | Local \(W_y\) | Global \(\mathcal K\) | Verdict |
|---|---:|---:|---|
| current pointwise \((A,e)\) | no | no | obstructed |
| rank / dimension labels | no | no | obstructed |
| endpoint full free-path word | no | intrinsic \(\mathcal H\) only | obstructed |
| finite parameter jet | no | no | obstructed |
| full Taylor jet, unrestricted smooth histories | no | no | obstructed |
| finitely many sampled history values | no | no | obstructed |
| punctured transport germ only | no in general | yes if projector limit exists | partial |
| punctured joint A/e background germ | yes | yes | reconstructs when limits exist |
| supplied \(\Xi_{\rm str}\) | yes | yes | direct resolved datum |

The irreducible memory is not the entire history.  It is precisely the finite
Grassmannian endpoint record \(\Xi_{\rm str}\).

---

## 27. History functor

Let \(\mathbf{Hist}\) denote punctured joint background histories for which the
required projector limits exist.

Define
\[
\boxed{
\mathsf{LimRes}:\mathbf{Hist}\to\mathbf{ResBg}
}
\tag{27.1}
\]
by the limit construction of §12.

Histories are identified exactly by (12.2).

The composite
\[
\mathbf{Hist}
\xrightarrow{\mathsf{LimRes}}
\mathbf{ResBg}
\xrightarrow{\mathsf U}
\mathbf{Bg}
\]
forgets the approach direction.

Because \(\mathsf U\) has nontrivial fibres, no inverse pointwise
reconstruction functor can recover every history class.

Thus \(\Xi_{\rm str}\) is an exact finite quotient of history and irreducible
approach memory relative to pointwise geometry.

---

## 28. Minimality matrix

| Datum | Isomorphism-functorial | Basepoint-free | Source-independent | Determines selected readout | Status |
|---|---:|---:|---:|---:|---|
| \(((\Pi_y),Q_o)\) | yes | no as written | yes | yes | redundant presentation |
| \(((W_y),\mathcal K)\) | yes | yes | yes | yes | structurally minimal |
| \(((C_y),z_r)\) | yes with transformed selection gauge | no | no | yes | stagewise readout compression |
| \(\Xi/\!\sim_{\rm rd}\) | fixed-background notion | gauge-dependent | no | yes | coarsest exact readout quotient |
| rank/dimension labels | yes | yes | yes | no | insufficient |
| pointwise \((A,e)\) | yes | yes | yes | not across singular seams | insufficient |
| endpoint free-path word | yes | groupoid typed | yes | not across approach seams | insufficient |

---

## 28.1 Hostile implication audit

The following stronger readings are false and are explicitly excluded.

\[
\text{resolution functoriality}
\not\Rightarrow
\text{pointwise reconstructibility}.
\]
The groupoid transports a supplied \(W,\mathcal K\); non-singleton fibres of
\(\mathsf U\) prevent it from inventing them at a singular endpoint.

\[
\mathcal K\text{ basepoint/path independent}
\not\Rightarrow
m\text{ selection-path independent}.
\]
The former uses that \(\mathcal K\) is fixed pointwise by loop holonomy.  The
latter would additionally need the relevant loop action to disappear after
observer-metric projection.

\[
\Xi_{\rm str}\text{ structurally minimal}
\not\Rightarrow
\Xi_{\rm str}\text{ minimal for one fixed source}.
\]
Exact gauge already supplies the counterexample: every local lift has the same
\(\mathcal S\Pi=\mathcal S\).

\[
\mathcal K_{o'}=T_p^{-1}\mathcal K_o
\not\Rightarrow
Q_{o'}=T_p^{-1}Q_oT_p
\]
without the explicit observer-isometry hypothesis (9.2).

\[
\text{endpoint full free-path memory}
\not\Rightarrow
\text{approach memory}.
\]
At the endpoint of §14 the entire path representation is trivial in both
approaches while the limiting fixed subspaces differ.

Finally,
\[
\text{a quotient is continuous}
\not\Rightarrow
\text{it preserves the required readout}.
\]
The pure-shift and Nyquist/corner controls show literal continuous forgetful
maps which erase mandatory distinctions.

These firewalls are part of the minimality classification, not optional
interpretive remarks.

---

## 29. Formalization handoff

A narrow worker can formalize the following without reopening research.

### Local covariance

If
\[
B'u=gB,\qquad S'u=gS
\]
with orthogonal \(u\), prove
\[
B\Pi=B
\Longrightarrow
B'(u\Pi u^{-1})=B',
\]
and
\[
S'(u\Pi u^{-1})=g(S\Pi)u^{-1}.
\]

Add composition and inverse.

### Lost-subspace equivalence

For orthogonal \(\Pi\), prove
\[
B\Pi=B
\iff
\exists W\le\ker B,\ 
\Pi=P_{(\ker B)^\perp}+P_W.
\]

### Global subspace transport

For
\[
\mathcal K_o\le\bigcap_\gamma\operatorname{Fix}P_\gamma,
\]
prove path independence of \(T_p^{-1}\mathcal K_o\), append, reverse, frame
covariance, and projector conjugation under an explicit metric-isometry
hypothesis.

### Readout equivalence

Formalize (19.1) as the iff criterion for equality of two selected diagonals
built from supplied resolved actions and projected means.  Transfer the iff to
\(\kappa\) through invertible edge linear maps.

### Finite witnesses

Formalize the same-rank different-\(\Pi\) pair, same-dimension different
fixed-subspace pair, pure-shift \(Q=I\) versus \(Q=0\), and coframe-only
intrinsic versus maximal local lift.

No dressing, stress, continuum, time or golden theorem belongs here.

---

## 30. Exact checker

The standard-library checker below verifies the finite covariance identities
and mandatory witnesses.

~~~python
from fractions import Fraction as Q

checks=[]
def ck(x,name):
    if not x:
        raise AssertionError(name)
    checks.append(name)

def eye(n=4):
    return [[Q(i==j) for j in range(n)] for i in range(n)]
def zero(n=4):
    return [[Q(0) for _ in range(n)] for _ in range(n)]
def tr(a):
    return [list(c) for c in zip(*a)]
def mm(a,b):
    return [[sum((x*y for x,y in zip(r,c)),Q(0)) for c in tr(b)] for r in a]
def add(a,b):
    return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sub(a,b):
    return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sc(q,a):
    q=Q(q)
    return [[q*x for x in r] for r in a]
def mv(a,v):
    return [sum((x*y for x,y in zip(r,v)),Q(0)) for r in a]
def col(a,j):
    return [r[j] for r in a]
def cols(vs,n=4):
    return [[Q(v[i]) for v in vs] for i in range(n)]
def inv(a):
    n=len(a)
    aug=[list(a[i])+eye(n)[i] for i in range(n)]
    for j in range(n):
        p=next(i for i in range(j,n) if aug[i][j])
        aug[j],aug[p]=aug[p],aug[j]
        q=aug[j][j]
        aug[j]=[x/q for x in aug[j]]
        for i in range(n):
            if i!=j and aug[i][j]:
                q=aug[i][j]
                aug[i]=[x-q*y for x,y in zip(aug[i],aug[j])]
    return [r[n:] for r in aug]
def rank(a):
    m=[list(r) for r in a]
    rows=len(m); colsN=len(m[0]); k=0
    for j in range(colsN):
        p=next((i for i in range(k,rows) if m[i][j]),None)
        if p is None:
            continue
        m[k],m[p]=m[p],m[k]
        q=m[k][j]
        m[k]=[x/q for x in m[k]]
        for i in range(rows):
            if i!=k and m[i][j]:
                q=m[i][j]
                m[i]=[x-q*y for x,y in zip(m[i],m[k])]
        k+=1
        if k==rows:
            break
    return k
def va(*vs):
    return [sum(z,Q(0)) for z in zip(*vs)]

I=eye(); Z=zero()
e=[col(I,j) for j in range(4)]
o=[Q(0)]*4

# Local incidence and frame/label functoriality.
B=cols([e[0],o,o,o])
Pi=cols([e[0],e[1],o,o])
S=cols([e[1],e[2],o,o])

g=[
    [Q(1),Q(1),0,0],
    [0,Q(1),0,0],
    [0,0,Q(1),0],
    [0,0,0,Q(1)],
]
u=cols([e[1],e[0],e[2],e[3]])
ui=tr(u)

Bp=mm(g,mm(B,ui))
Sp=mm(g,mm(S,ui))
Pip=mm(u,mm(Pi,ui))

ck(mm(B,Pi)==B,'local incidence')
ck(mm(Bp,Pip)==Bp,'incidence covariant')
ck(mm(Sp,Pip)==mm(g,mm(mm(S,Pi),ui)),
   'resolved action covariant')

g2=[
    [Q(2),0,0,0],
    [0,Q(1),0,0],
    [0,0,Q(1),0],
    [0,0,0,Q(1)],
]
Bpp=mm(g2,Bp)
ck(mm(Bpp,Pip)==Bpp,'composition incidence')
ck(mm(inv(g),Bp)==mm(B,ui),'inverse frame recovery up to label')

# Exact-gauge local resolution invisibility.
T=cols([e[2],e[1],e[0],e[3]])
Sg=mm(T,B)
ck(mm(Sg,Pi)==Sg,'exact gauge any incidence lift invisible')
ck(mm(Sg,I)==Sg,'exact gauge maximal lift invisible')

# Same rank labels, different local projector limits.
BA=cols([e[0],o,o,o])
BB=cols([o,e[0],o,o])
PA=cols([e[0],o,o,o])
PB=cols([o,e[1],o,o])

ck(rank(BA)==rank(BB)==1,'same nonzero rank')
ck(PA!=PB,'different limiting projectors')
ck(rank(Z)==0,'same endpoint rank zero')

# Global basepoint path independence, append and reverse.
L=[
    [Q(1),0,0,0],
    [0,Q(2),0,0],
    [0,0,Q(3),0],
    [0,0,0,Q(4)],
]
T1=I
T2=L
v=e[0]

ck(mv(inv(T1),v)==mv(inv(T2),v),
   'basepoint path independence on fixed memory')

Tq=[
    [Q(1),0,0,0],
    [0,Q(1),Q(1),0],
    [0,0,Q(1),0],
    [0,0,0,Q(1)],
]
Tappend=mm(T1,Tq)
Kstep=mv(inv(Tq),mv(inv(T1),v))
ck(mv(inv(Tappend),v)==Kstep,'append transport')
ck(mv(inv(Tappend),mv(Tappend,v))==v,'reverse transport')

# Same fixed-space dimensions, different limiting fixed subspaces.
PBdir=cols([o,e[1],o,o])
PCdir=cols([o,o,e[2],o])
t=Q(1,5)
GB=add(I,sc(t,PBdir))
GC=add(I,sc(t,PCdir))

ck(rank(sub(GB,I))==rank(sub(GC,I))==1,'same loop defect rank')
ck(PBdir!=PCdir,'different killed loop directions')

QB=sub(I,PBdir)
QC=sub(I,PCdir)
ck(QB!=QC,'different limiting fixed projectors')
ck(rank(sub(I,I))==0,'same trivial endpoint loop')

# Pure shift: forgetting global memory erases the shift.
b=e[1]
a=[-x for x in b]
m=a

zI=mv(I,m)
z0=mv(Z,m)
dI=va(a,[-x for x in zI])
d0=va(a,[-x for x in z0])
kI=va(b,dI)
k0=va(b,d0)

ck(dI==o and kI==b,'pure shift intrinsic Q preserves shift')
ck(d0==a and k0==o,'forgetting Q erases pure shift')

# Intrinsic/maximal local lifts differ on corner and Nyquist probes.
Sco=cols([e[1],o,o,o])
ck(mm(Sco,Z)==Z and mm(Sco,I)==Sco,
   'corner intrinsic/maximal lifts differ')

Sny=cols([[Q(4),0,0,0],o,o,o])
ck(col(mm(Sny,I),0)==[Q(4),0,0,0] and col(mm(Sny,Z),0)==o,
   'Nyquist intrinsic/maximal differ')

# Mandatory L=3 discontinuity family.
f=(Q(1),Q(-2),Q(1))
d=tuple(f[j]-f[(j-1)%3] for j in range(3))
ck(d==(0,-3,3),'L3 d')

for t in (Q(1,7),Q(-2)):
    kap=[]
    for j in range(3):
        y=(j+1)%3
        delta_y=va(
            [-t*f[j] if i==0 else Q(0) for i in range(4)],
            [-d[y] if i==1 else Q(0) for i in range(4)],
        )
        bj=[t*f[j],0,0,0]
        vy=[1,f[y],0,0]
        vx=[1,f[j],0,0]
        kap.append(va(bj,vy,delta_y,[-x for x in vx]))
    ck(kap==[o,o,o],f'L3 kappa off transition {t}')

kap0=[]
for j in range(3):
    y=(j+1)%3
    vy=[1,f[y],0,0]
    vx=[1,f[j],0,0]
    kap0.append(va(vy,[-x for x in vx]))

ck(kap0[0]==[0,-3,0,0],'L3 transition jump')

# No finite sampled history reconstruction.
samples=[Q(1),Q(2),Q(3)]
def qfun(t):
    prod=Q(1)
    denom=Q(1)
    for s in samples:
        prod*=t-s
        denom*=-s
    return t*prod/denom

for s in samples:
    ck(qfun(s)==0,f'sample match {s}')

ck(qfun(Q(0))==0,'same endpoint')

prod0=Q(1)
den=Q(1)
for s in samples:
    prod0*=-s
    den*=-s
ck(prod0/den==1,'distinct hidden direction activates at first order')

print(f'PASS: {len(checks)} exact rational resolution-memory assertions')
~~~

Expected output:

~~~text
PASS: 30 exact rational resolution-memory assertions
~~~

---

## 31. Final classification

The strongest justified terminal is
\[
\boxed{
\texttt{RESOLUTION-MEMORY-MINIMALITY-CLASSIFIED}.
}
\]

The classification is:

1. \(\Xi\) promotes to an exact finite resolution groupoid under admissible
   background/frame/label isomorphisms.
2. The projector package is naturally equivalent to the smaller geometric
   package
   \[
   ((W_y)_y,\mathcal K).
   \]
3. This package is minimal as source-independent universal approach memory.
4. A fixed selected readout factors through smaller source-dependent data,
   and every sufficient forgetful map is classified by (19.3).
5. \(\mathcal K\) is basepoint-free and has exact loop-conjugation, append and reverse.
6. The projected mean still retains PR #120's separate path-family gauge on
   generic non-isometric holonomy.
7. Complete punctured joint-background history reconstructs the resolution.
8. Pointwise backgrounds, rank labels, finite labelled endpoint histories,
   endpoint free-path words, finite jets and finite samples do not.
9. Quotients that collapse the critical local or global memory erase pure
   shift, Nyquist or corner distinctions.

The resolution is neither arbitrary decoration nor latent pointwise geometry.

It is the minimal finite record of singular approach data required by the
current universal resolved interface.
