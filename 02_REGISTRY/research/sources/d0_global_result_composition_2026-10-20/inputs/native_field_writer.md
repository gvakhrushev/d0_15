# Native field writing: the primary profile and the preserved pairing

20 October 2026. Bounded application within the existing scientific #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`; original input `7aafe436`,
integrated with the disjoint published continuation through `20d97664`.

**Consumer.** Sections 2–4 of the existing
[prospective field-and-price bridge](../../../sources/d0_native_joint_field_minimum_2026-10-20/PROSPECTIVE_FIELD_REALIZATION_BRIDGE.md)
require actual fields generated from one complete initial state. This note
tests the already constructed endpoint-isometric record transition as a
candidate for that arrow, on the original primary Brinkmann profile. It
does not propose another action or another geometric solution family.

**Conclusion.** If every transition preserves the same coordinate positive
pairing, and the primary metric is read through the fixed dictionary below,
even the field coordinate of that bridge fails: a nonzero primary profile
perturbation has a positive distance from every reachable endpoint. The
bound survives ordinary hereditary copying and its specified weighted norm.
This is stronger than the previous instantaneous rank-three statement:
arbitrarily many transitions, arbitrary record capacity and closure of the
reachable set do not repair this particular application. Moving the solder
changes the coordinate pairing and is an explicit escape from the hypothesis;
it is not excluded. Its actual native transition and full price remain to be
constructed. No universal D0 obstruction or physical admission theorem is
claimed.

## 1. The existing transition and the correctly typed metric

The [matter/observer owner](../../../A4D_NATIVE_MATTER_OBSERVER_PAIRING.md)
§§1–2 defines the complete quotient coordinates

```text
q = F eta F^T,   m = exterior(F) psi,
Q = -q + 2vv^T/(v^T q^-1 v) > 0,   v = grade_one(m),   G = Q^-1.
```

Thus `q` is not the fixed internal Lorentz matrix `eta`. The
[coframe bridge](../../../A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md) §2
writes `F=e^-1` for its inverse-coframe differential. For the proposed
reuse we explicitly identify the chronology's solder with that inverse
coframe: `F_chron=e^-1`, hence `q=(e^T eta e)^-1`. This is a declared
candidate dictionary, not a physical identification inferred from the
shared letter `F`. The pairing `Q` also contains that solder. The full
sixteen-grade pairing is `W=omega exterior_Gram(G)`, `omega=sqrt(det Q)`.

This inverse-coframe dictionary is the one tested here. A direct covariant
dictionary can instead be built with `F=e^T eta`, giving `q=e^T eta e`;
it has a different solder/link/matter identification. The equality of
these two `q` coordinates is not asserted. Each needs its own actual
history map before a physical application. The abstract bound in §2
also applies to the direct dictionary's rank-one covariant profile change.

The [record chronology](../../../A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md)
§§1–3 takes the actual full CAR gate `U(q,m)`, which is `W`-orthogonal,
and additionally assumes whole-operator endpoint isometry

\[
 U^T W(q_+,m_+)U=W(q,m),\qquad m_+=Um.
\tag{1}
\]

This is a conditional physical transition premise, not a consequence of
one-state norm conservation. With `w=grade_one(m_+)!=0`, its solved result is

\[
 Q_+=Q,\qquad q_+=-Q+\frac{2ww^T}{w^TGw}.
\tag{2}
\]

Every regular step of a composition satisfying these hypotheses preserves
the same `Q`. We grant all nonzero `w` in (2), an enlargement of the actual
gate's reachable outputs. Proving a restriction for that enlargement does
not assume controllability of the gate. Singular outputs and new operators
that fail (1) are outside the proposed reuse.

## 2. A closed invariant, not only a tangent count

For a fixed positive four-by-four `Q`, let

\[
 \mathcal R_Q=\{-Q+2ww^T/(w^TQ^{-1}w):w\ne0\}.
\]

Direct contraction gives

\[
 \operatorname{Tr}(Q^{-1}q)=-2,\qquad qQ^{-1}q=Q
 \quad(q\in\mathcal R_Q).
\tag{3}
\]

Indeed, writing `w=Q^(1/2)n` reduces the normalized matrix to
`-I+2nn^T/(n^Tn)`. The image of the unit sphere is compact, so
`R_Q` is closed. In particular all finite regular histories and all their
convergent endpoint limits obey (3). Only the trace identity is needed below.

Use the full symmetric-matrix norm

\[
 \|A\|_Q=\|Q^{-1/2}AQ^{-1/2}\|_F,
\tag{4}
\]

including both off-diagonal entries. For a target `q_t`, every reachable
`r` therefore satisfies, by Frobenius Cauchy–Schwarz and `||I_4||_F=2`,

\[
 \|q_t-r\|_Q\ \ge\frac12
 \left|\operatorname{Tr}(Q^{-1}q_t)+2\right|.
\tag{5}
\]

For `q_0 in R_Q` and any nonzero real rank-one change `q_t=q_0+a kk^T`,
the right side is `|a| k^TQ^-1 k/2>0`. This is a finite separation
statement. It rules out approximation, not merely a differentiable path.
The invariant does allow other nontrivial metric changes; it is not a
claim that (2) is a constant metric map.

## 3. Substitute the original primary Brinkmann coframe

Use precisely the primary null ordering `(u,v,x,y)`, with internal matrix
`eta_null=[[0,1],[1,0]] direct_sum (-I_2)`. The actual primary
null-to-rest map is the rational, nonorthogonal `T` retained in §4.
The original coframe and its coordinate metric are

\[
 e_H=\begin{pmatrix}1&0&0&0\\H/2&1&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix},
 \qquad
 g_H=e_H^T\eta_{null}e_H
 =\begin{pmatrix}H&1&0&0\\1&0&0&0\\0&0&-1&0\\0&0&0&-1\end{pmatrix}.
\tag{6}
\]

This is the coframe in the
[original all40 theorem](../../../../gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md)
§1, not a replacement carrier. Fix one mesh and all calibration/density
factors under the profile variation. The existing
[strict primary-domain application](../../d0_primary_native_domain_source_2026-10-20/RESULT.md)
§§1–2 supplies `e_raw'=rho_x^-1/2 T e_H / sigma` and
`g_read=sigma^2 rho_x g_raw'`. Here `sigma>0` is its fixed native-domain
scale (called `s` in that owner), distinct from the profile perturbation
parameter below. Consequently set `kappa_x=sigma^2 rho_x>0`. The
conditional field readout to be tested is exactly

\[
 q_H=\kappa_x g_H^{-1}
 =\kappa_x\begin{pmatrix}0&1&0&0\\1&-H&0&0\\0&0&-1&0\\0&0&0&-1\end{pmatrix}.
\tag{7}
\]

No varying density is silently differentiated as a constant. If an actual
physical identification changes `kappa` or introduces a link-dependent
center, its derivatives and finite map must instead be supplied; the
following chosen-dictionary conclusion is then not automatically applicable.

Start from the primary exact nonvacuum profile `H_*`. Use the existing
fixed-collar perturbation `H_s=H_*+s chi` from the prospective bridge §5,
with its original Cartan lift and unchanged CAR scalar/top data. At any
site with `s chi(x)!=0`, (7) gives exactly

\[
 q_{H_s}-q_{H_*}=-\kappa_x s\chi(x) e_v e_v^T.
\tag{8}
\]

For the initial positive coordinate pairing `Q_x` of any timelike initial
observer, (5) becomes

\[
 \inf_{r\in\mathcal R_{Q_x}}\|q_{H_s}-r\|_{Q_x}
 \ \ge\frac{\kappa_x|s\chi(x)|}{2}(Q_x^{-1})_{vv}>0.
\tag{9}
\]

The same primary off-shell family therefore cannot be generated or
approximated by repetitions of (2) with this fixed coordinate pairing and
dictionary. We do not need to solve a new link equation: failure of this
necessary metric projection already prevents convergence of the whole
coframe/link/matter target in the declared field chart. This leaves all
original 16+24+2 Euler equations and their stationary solutions unchanged.

## 4. The moving-solder control: the excluded hypothesis is explicit

It would be incorrect to replace coordinate `Q` in this theorem by the
internal constant `Q_int=I` in the orthonormal rest basis. The primary
domain owner fixes

```text
T = [[1,1/2],[1,-1/2]] direct_sum I_2,
T^T eta_rest T = eta_null,   T^T T = diag(2,1/2,1,1).
```

Its actual clock first grade is along the rest `e_0`, hence along
`(1/2,1,0,0)` in the null basis. Its positive null Gram must not be
replaced by the identity. With `F_H=sqrt(kappa)e_H^-1 T^-1` and matter
transported by the actual exterior representation, the observer
construction gives the valid kinematic pair

\[
 q_H=F_H\eta_{rest}F_H^T=\kappa g_H^{-1},\qquad
 Q_H=F_HF_H^T
 =\kappa\left[
 \begin{pmatrix}1/2&-H/4\\-H/4&2+H^2/8\end{pmatrix}\oplus I_2\right].
\tag{10}
\]

`Q_H` is positive for every real `H`; its determinant is `kappa^4`.
The Lorentz metric changes even though internal `eta` and `Q_int` do not.
At fixed `kappa`, its necessary positive-pairing change is explicitly

\[
 Q_{H+s\chi}-Q_H=\kappa
 \left[\begin{pmatrix}
 0&-s\chi/4\\-s\chi/4&H s\chi/4+s^2\chi^2/8
 \end{pmatrix}\oplus0_2\right].
\tag{11}
\]

For this initial observer `(Q_H^-1)_{vv}=1/(2kappa)`, and the separation in
(9) is at least `|s chi|/4`. Each moving pair individually obeys (3),
but with its own `Q_H`; keeping the initial `Q_H` gives the nonzero
trace defect `-s chi/2`. This control rejects any unconditional reading of
the obstruction. The kinematic map `H -> F_H` is not an admitted action
from one complete initial state, and its source and price are not supplied
by writing (10).

## 5. What copying and condensed compatibility actually preserve

The [closed record engine](../../../A4D_NATIVE_CLOSED_RECORD_ENGINE.md) §4
uses the actual adjacent archive maps and ordinary inheritance
`(Jf)(y)=f(pi(y))`. If the field, `Q` and the target are inherited in
this way, (3) and (9) hold at each child. With the owner's conditional
weights `mu_child=mu_parent/d_parent`, the squared field norm is exactly

\[
 \sum_y\mu_y\|J A(y)\|_{JQ(y)}^2
 =\sum_x\mu_x\|A(x)\|_{Q(x)}^2.
\tag{12}
\]

Hence the inherited target obeys the same lower bound

\[
 \|q_{H_s}-r\|_{\mu,Q}
 \ge\frac12\left(\sum_x\mu_x
 [\kappa_xs\chi(x)(Q_x^{-1})_{vv}]^2\right)^{1/2}.
\tag{13}
\]

This is about the stated inherited comparison, not an identification of
the nonuniform archive tower with a physical spacetime mesh. Independent
child values, a different coframe readout, moving `Q`, or a new refinement
map change the hypotheses and require their own owner.

Likewise any continuous endpoint closure retains (3). Describing these
same sections on profinite probes does not change the pointwise equation:
local lifts on jointly surjective covers satisfy it at every lifted point,
and their descended values do too. A target violating it cannot acquire
a lift solely by such gluing. This is the concrete obstruction to applying
the proposed condensed descent interface with this particular history map;
it is not a general objection to condensed geometry.

## 6. Precise parent substitution and next decisive check

In the prospective bridge's notation, if `Y(w)` has metric projection (7)
and all its admitted transitions satisfy (1), then `Y(w)` and its closure
lie in the invariant set (3). The target (8) lies a positive distance away.
Consequently `(y_s,S(y_s)+c_0)` cannot belong to the closure of the paid
graph `Gamma`, for **any** proposed price: its field coordinate already
fails. This disposes of the suggested direct endpoint-engine/inheritance
substitution into §3. It does not discharge `native_sector`,
`gr_operational_realization` or a positive GR premise.

The concurrent [actual CAR actuator](NATIVE_CAR_ACTUATED_METRIC.md)
supplies a complementary positive result: a paid finite word changes the
matter high pair and its live query distinguishes different supplied `H`
profiles. Its §§1,8 explicitly hold geometry and links during that word
and retain the live material-code/query premise. This changes a material
field and improves the future distinguishability quotient; it does not
claim to write `H` or realize the full paid field graph. The fixed-`Q`
metric restriction here neither excludes nor repeats that result. A
query being sensitive to `H` is compatible with its operations preserving
the `H` coordinate.

The next construction must exhibit a genuinely admitted joint step that
changes the needed coordinate pairing/solder, or another proved field
readout, and maintains the link constraint `D_e q_y D_e^T=q_x`. On the
rest-observer primary section, (11) gives the exact change such a step
must realize. Its retained preparation, oldRIGHT, clock, work and complete
Cost−Info must then enter the same paid graph. Another neutral detector
completion or a larger inherited archive supplies none of these missing
maps. Alternatively the independently native stationary-law route remains
open; the present result concerns the proposed execution-realization route.

The companion `check_native_field_writer_bridge.py` checks exact finite
matrix identities and hostile controls and pins its consumed sources.
The universal closure and norm arguments are the analytical proofs above,
not extrapolations from those controls. No Lean theorem or complete native
physical closure is claimed.
