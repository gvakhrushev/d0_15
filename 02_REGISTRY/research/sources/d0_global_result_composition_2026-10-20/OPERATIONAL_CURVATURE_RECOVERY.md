# Native future probabilities recover the primary metric and its curvature

20 October 2026. Composition within existing research PR #334. This proof
consumes the original finite CAR actuation, the primary polynomial
Brinkmann family, the future-profile kernel, and the midpoint recovery.
It does not introduce an actuator, a scalar curvature oracle or a new
physical price. The exact input versions are in SOURCE_INPUTS.json.

## 1. Common carrier and the scope of the reconstruction

Use the primary operational metric

\[
 \widehat g'=s^{-2}g_H,\qquad
 g_H=2\,du\,dv+H(u,x,y)\,du^2-dx^2-dy^2.
\]

The same fixed calibration \(s>0\), positive original inverse-PF density
\(\rho_z\), matter preparation, native scene parameter \(\eta'>0\), and
live material-code/query binding are retained. The supplied original CAR
word acts at \(w=z+h\widehat v\); it changes the top amplitude by a known
nonzero \(\delta_z\), while keeping the metric and proper links fixed.
The word is chosen from the common bounded chart, independently of the
unknown \(H\). Actual address, preparation, execution and query costs
are not eliminated.

For this future experiment, the owned local query and port law are

\[
 q_z(H)=\rho_z^{-1}s^2
       \left(2v_{4,z}\frac{\delta_z}{h}
                    -H_z\frac{\delta_z^2}{h^2}\right),\quad
 t_z=p+\sigma p^2\eta'^2q_z,\quad
 B(t)=4t^2(1-t^2),\quad p=\varphi^{-1},\quad |\sigma|=1.
 \tag{1}
\]

All affected stencil sites, not just \(z\), lie in the admitted query
chart. In particular \(1/2<t_z<2/3\). With a field-independent actual
readiness \(r_z>0\), the complete coarse experiment has probabilities

\[
 (r_zB(t_z),\ r_z(1-B(t_z)),\ 1-r_z).
 \tag{2}
\]

The last outcome is the retained abort. The fine work/clock/reference
record is still present. Formula (2) is its declared marginal.
These are probability profiles of admitted future experiments, not exact
probabilities inferred from one finite observed sample. The live query
is a hypothesis of the original construction, not a free oracle made
from an unknown quantum input.

## 2. A quantitative inverse on the actual complete probability law

On the whole interval \([1/2,2/3]\),

\[
 B'(t)=8t(1-2t^2),\qquad
 \frac{16}{27}\le B'(t)\le2,
 \tag{3}
\]

because \(B''(t)=8-48t^2<0\) there. Define the actual sensitivity

\[
 L_{h,z}=\frac{r_z p^2\eta'^2s^2\delta_z^2}{\rho_z h^2}>0.
 \tag{4}
\]

For two profiles with the same stated preparation and calibration,
the mean-value theorem and (1) give the exact bounds

\[
 \boxed{\frac{16}{27}L_{h,z}|H_z-\widetilde H_z|
 \ \le\ {\rm TV}(P_z(H),P_z(\widetilde H))
 \ \le\ 2L_{h,z}|H_z-\widetilde H_z|.}
 \tag{5}
\]

Here the total variation is of the three-outcome law (2), so it equals
\(r_z|B(t_z)-B(\widetilde t_z)|\). The full tape has total variation
at least this large by marginalization; its distance is not assigned
the upper bound in (5).

The monotone branch has the explicit inverse

\[
 q_z=\frac{\sqrt{(1-\sqrt{1-B_z})/2}-p}
                  {\sigma p^2\eta'^2},\qquad
 H_z=\frac{2h\,v_{4,z}}{\delta_z}
                 -\frac{\rho_z h^2}{s^2\delta_z^2}q_z .
 \tag{6}
\]

If the known preparation fixes \(v_{4,z}\), an error at most
\(\epsilon_z\) in the unconditional first probability in (2), with
the estimated probability kept in the common branch, gives

\[
 |\widehat H_z-H_z|\le
                  \frac{27}{16}\frac{\epsilon_z}{L_{h,z}}.
 \tag{7}
\]

This inverse is an actual source of the norm used in reconstruction;
it is not an arbitrary renormalization of a physical action.

### Two probes eliminate an unknown common matter derivative

The original positive and negative rotations have known increments

\[
 \delta_\pm=\pm d_w\sin\alpha+b_w(\cos\alpha-1).
\]

Under the owned small-angle/slack bounds they are nonzero with opposite
signs. The second word has its actual two additional controller letters;
an inverse gate is not priced as free. The original inverse is

\[
 H_z=-\frac{\rho_z h^2}{s^2}
       \frac{q_{z,+}/\delta_+-q_{z,-}/\delta_-}
                  {\delta_+-\delta_-}.
 \tag{8}
\]

Thus the same unknown \(v_{4,z}\) cancels. With equal readiness and
errors at most \(\epsilon_z\) in each unconditional success probability,
replace (4) in (7) by

\[
 L^{\rm pair}_{h,z}
   =\frac{r_z p^2\eta'^2s^2|\delta_+\delta_-|}{\rho_z h^2}.
 \tag{9}
\]

Indeed,
\((1/|\delta_+|+1/|\delta_-|)/|\delta_+-\delta_-|
 =1/|\delta_+\delta_-|\).
For unequal ready probabilities replace \(\epsilon_z/r_z\) in the
derivation by \(\max(\epsilon_{z,+}/r_{z,+},
\epsilon_{z,-}/r_{z,-})\).
The prepared amplitudes/code and calibration are still supplied data;
this does not clone an unknown state or identify its amplitudes for free.

## 3. Five spatial points recover the entire owned polynomial wave

Now USE the previously proved polynomial primary family, instead of
differentiating a noisy full-grid reconstruction. At each physical
midpoint time write

\[
 H(x,y)=c_0(x^2+y^2)+c_2(x^2-y^2)+2d_2xy
       +c_3(x^3-3xy^2)+d_3(3x^2y-y^3).
 \tag{10}
\]

All five coefficients can be arbitrary functions of that time.
Write \(\Psi_{\rm read}=s^2\Psi_{\rm prepared}\) to distinguish the
original continuum/readout waveform from the calibrated prepared
amplitudes. The sourced primary member has
\(c_0(\tau)=-\lambda_-\|\partial_u\Psi_{\rm read}(\tau)\|^2\).
At coframe site \(j\), whose readout is \(\tau_j=u_j-h/2\), the exact
finite source is
\[
 c_{0,j}=-\lambda_-
   \left\|\frac{\Psi_{{\rm read},j}
                    -\Psi_{{\rm read},j-1}}h\right\|^2
 =-\lambda_-s^4
   \left\|\frac{\Psi_{{\rm prepared},j}
                    -\Psi_{{\rm prepared},j-1}}h\right\|^2.
\]
This is the previous interval \(j-1\); the diagnostic actuator in
(1) uses the actual forward derivative at its own site. They are
not identified by dropping the midpoint shift. The reconstruction
does not impose either source relation. It therefore reads
both that source coefficient and the four independent harmonic wave
coefficients. The Einstein relation is an independently testable
conclusion of the owned geometric action, not a decoder assumption.

Choose five accessible spatial points
\((a,0),(-a,0),(0,a),(0,-a),(a,a)\), with \(a>0\).
Their actuator sites and stencils must lie in the same admitted chart.
Denote the decoded values by \(X_+,X_-,Y_+,Y_-,Z\).
Then the exact inverse is

\[
\begin{aligned}
 c_0&=\frac{X_++X_-+Y_++Y_-}{4a^2},&
 c_2&=\frac{X_++X_--Y_+-Y_-}{4a^2},\\
 c_3&=\frac{X_+-X_-}{2a^3},&
 d_3&=\frac{Y_--Y_+}{2a^3},\\
 d_2&=\frac{Z-2a^2c_0+2a^3c_3-2a^3d_3}{2a^2}.
\end{aligned}
 \tag{11}
\]

This is an invertible five-by-five evaluation map. It uses five
probability profiles when the common matter derivative is known, or
two profiles at each of the five sites when it is eliminated by (8).
Five exact experimental outcomes do not determine these probabilities.

Suppose every decoded sample has error at most \(E_H\). Directly
substituting (11) gives

\[
 |\Delta c_0|,|\Delta c_2|\le E_H/a^2,\quad
 |\Delta c_3|,|\Delta d_3|\le E_H/a^3,\quad
 |\Delta d_2|\le 5E_H/(2a^2).
 \tag{12}
\]

For the last bound the five coefficients of \(d_2\) are
\((1/2,-3/2,1/2,-3/2,1)/(2a^2)\); their absolute sum
is \(5/(2a^2)\).
The spatial Hessian is recovered exactly:

\[
\begin{aligned}
 H_{xx}&=2(c_0+c_2)+6c_3x+6d_3y,\\
 H_{yy}&=2(c_0-c_2)-6c_3x-6d_3y,\\
 H_{xy}&=2d_2-6c_3y+6d_3x .
\end{aligned}
 \tag{13}
\]

Consequently, on \(|x|,|y|\le R\),

\[
 \boxed{\|\Delta D^2_\perp H\|_{\max}
       \le(5/a^2+12R/a^3)E_H.}
 \tag{14}
\]

The independent lower-index curvature components of \(g_H\) are, up to
the already fixed sign convention, one half of these three Hessian
entries. For the actual \(\widehat g'=s^{-2}g_H\), its lower-index
coordinate curvature has the additional fixed factor \(s^{-2}\);
the connection and curvature with one raised index are unchanged.
Its Ricci and Weyl components are therefore recovered as
well. The metric and actual proper Cartan links follow from their
original algebraic and shifted-difference formulas, without solving
the geometric equations again.

In particular this native readout distinguishes the nonflat VSI waves
whose polynomial scalar curvature invariants all vanish. The full
future profile is richer than the original unactuated \(f_i=q_i=0\)
detector statistic.

### The already-owned larger exact harmonic class takes nine points

There is a sharp boundary to the five-point statement. The already-owned
common continuous/discrete harmonic polynomial
\(Q=xy(x^2-y^2)\) vanishes at all five points, although
\(Q_{xx}=6xy\) and \(Q_{xy}=3(x^2-y^2)\) do not vanish identically.
It is therefore neither erased nor declared unphysical.

Use the full maximal polynomial common-harmonic class in the midpoint
owner, section 8, together with its independent sourced coefficient:

\[
 \mathcal V=\operatorname{span}
  \{1,x,y,x^2+y^2,x^2-y^2,2xy,
         x^3-3xy^2,3x^2y-y^3,xy(x^2-y^2)\}.
 \tag{15}
\]

At the nine points

\[
 a(0,0),\ a(1,0),\ a(-1,0),\ a(0,1),\ a(0,-1),\
 a(2,0),\ a(0,2),\ a(1,1),\ a(1,2)
 \tag{16}
\]

the evaluation determinant, in the displayed orders, is
\(3456a^{18}\ne0\).
Let \(M_1\) be that fixed evaluation matrix at \(a=1\).
If \(d=(0,1,1,2,2,2,3,3,4)\), the exact reconstruction is

\[
 c_i=a^{-d_i}(M_1^{-1}H_{\rm samples})_i .
 \tag{17}
\]

The row absolute sums of \(M_1^{-1}\), checked by exact rational
elimination, are
\((1,2,2,2,1,6,4/3,4/3,2)\).
Consequently the whole class, including its quartic curvature, obeys
the uniform transverse Hessian error bound

\[
 \boxed{\|\Delta D^2_\perp H\|_{\max}
   \le (12/a^2+16R/a^3+12R^2/a^4)E_H.}
 \tag{18}
\]

The coefficient of \(x^2+y^2\) is again read independently; its
Einstein–matter relation is not inserted into the inverse. The nine
points use nine single-probe profiles, or eighteen opposite-probe
profiles when the unknown matter derivative is eliminated. They must
all be accessible in the original common chart. This consumes the
larger already-proved exact polynomial space instead of mistaking
the five-point subfamily for the whole operational geometry.

## 4. Controlled refinement: which topology actually survives

On a refining lattice use \(a_h=h\lfloor a/h\rfloor\), whenever the five
points and their stencils remain in the common chart. For \(h\le a/2\),
\(a_h\ge a/2\), so (14) has a constant independent of \(h\).
Let \(L_{\min,h}\) be the minimum of the five actual sensitivities (4),
or (9), and let the unconditional probability error be bounded by
\(\epsilon_h\). Equations (7),(14) give

\[
 \|\Delta D^2_\perp H_h\|_{\max}
 \le \frac{27}{16}
   (5/a_h^2+12R/a_h^3)\frac{\epsilon_h}{L_{\min,h}}.
 \tag{19}
\]

For the OWNED polynomial primary family, \(\epsilon_h=o(L_{\min,h})\)
is sufficient for curvature recovery. To retain the owned \(O(h^2)\)
recovery rate it suffices to have
\(\epsilon_h=O(h^2L_{\min,h})\), in addition to that owner's field and
midpoint hypotheses. There is no extra \(h^{-2}\) loss from taking
second differences of noisy neighboring samples.

With exact probability profiles and the original midpoint right inverse,
the reconstructed common polynomial metric and its curvature agree
exactly with the fixed smooth metric at every supplied physical
midpoint slice, on every mesh. The original matter record still has
its independently proved \(O(h^2)\) recovery. Interpolation between
time slices retains the hypotheses of that owner.

For an arbitrary unrestricted grid profile, second-difference
curvature instead has error bounded by
\(C h^{-2}\epsilon_h/L_{\min,h}\); the stronger condition
\(\epsilon_h=o(h^2L_{\min,h})\) is then sufficient.
One must not use the polynomial bound for the whole analytic Fourier
family or every smooth metric.

The original small-word construction supplies \(\delta=O(h^2)\)
under its uniform hypotheses, but supplies NO uniform lower bound
on \(|\delta|\). Therefore \(L_{\min,h}\) must remain in (19);
replacing it by a claimed \(\Theta(h^2)\) is not justified. Finite
injectivity at each mesh does not by itself give a stable continuum
probability norm. The explicit inverse identifies the missing
precision requirement.

The nine-point reconstruction has the same conclusion after replacing
the constant in (19) by the one in (18) and taking the minimum over
its nine actual sensitivities. Its spatial domain must contain the
scaled points (16) and their full actuator stencils.

These estimates are pointwise, or uniform when the same bounds hold,
in the physical midpoint time. A noise-robust \(C^2\) estimate in the
time coordinate requires a separate temporal regularity bound.
No such estimate is inferred from pointwise noisy samples.

## 5. Observable separation from the fixed-pairing writer image

This section consumes the separate native field-writer theorem at the
pinned `inputs/native_field_writer.md`. Its hypotheses are substantive:
\(q=\kappa g_H^{-1}\), \(\kappa>0\), the specified exterior coordinate
pairing, an actual gate orthogonal for that pairing, and whole-operator
endpoint isometry. A one-state norm identity alone does not supply them.
The material diagnostic above is not silently declared to be a writer
obeying these additional hypotheses.

For that candidate writer the coordinate positive pairing \(Q\) is
invariant. All finite words and their limits lie in the compact set
\[
 \mathcal R_Q=\{-Q+2ww^T/(w^TQ^{-1}w):w\ne0\},
 \qquad \operatorname{Tr}(Q^{-1}q)=-2.
 \tag{20}
\]
Write \(\|A\|_Q=\|Q^{-1/2}AQ^{-1/2}\|_F\). Since the Frobenius
norm of the four-dimensional identity is 2, trace Cauchy–Schwarz gives
\[
 \operatorname{dist}_Q(q,\mathcal R_Q)
 \ge\tfrac12|\operatorname{Tr}(Q^{-1}q)+2|.
 \tag{21}
\]
In the owned null coordinates, with the actual rest-observer conversion,
\[
 q_H=\kappa\begin{pmatrix}0&1\\1&-H\end{pmatrix}
              \oplus(-\kappa I_2),\qquad
 Q_H=\kappa\begin{pmatrix}1/2&-H/4\\-H/4&2+H^2/8\end{pmatrix}
              \oplus\kappa I_2.
\]
Thus \((Q_{H_0}^{-1})_{vv}=1/(2\kappa)\) and
\(\operatorname{Tr}(Q_{H_0}^{-1}q_H)=-2-(H-H_0)/2\).
Combining (21) with the UPPER estimate in (5), using the same probe,
calibration and prepared derivative at both field values, yields
\[
 \boxed{\operatorname{dist}_{Q_{H_0}}(q_H,\mathcal R_{Q_{H_0}})
 \ge\frac{|H-H_0|}{4}
 \ge\frac{\operatorname{TV}(P_z(H),P_z(H_0))}{8L_{h,z}}.}
 \tag{22}
\]
An estimated value \(\widehat H\) with a justified error \(E_H\)
gives the robust bound
\(\tfrac14(|\widehat H-H_0|-E_H)_+\). The nine-point inverse makes
the entire stated polynomial class available for this diagnostic;
an unrestricted localized profile requires a probe in its support.

Even allowing a positive scalar factor \(\kappa\) alone does not remove
this obstruction. For (20), \(\det q=-\det Q\); on the primary
sheet, \(\det q_H=-\kappa^4\), while initially
\(\det Q_{H_0}=\kappa_0^4\). Hence a primary endpoint must have
\(\kappa=\kappa_0\), after which the trace fixes \(H=H_0\).
The same fixed-Q conclusion survives the owner's specified hereditary
copy and its closure. No choice of price makes the excluded endpoint
reachable in this class.

The explicit escape is to admit a genuine joint step that moves the
coordinate pairing. The change needed along the same geometric chart is
\[
 Q_{H+\Delta H}-Q_H
 =\kappa\begin{pmatrix}
 0&-\Delta H/4\\
 -\Delta H/4&H\Delta H/4+(\Delta H)^2/8
 \end{pmatrix}\oplus0_2.
 \tag{23}
\]
An internal pairing may remain the identity while this coordinate
pairing moves. A kinematic coframe formula is not yet the admitted
joint writer: its actual gate, solder/link constraints, work record and
full price must be given. Equations (22)–(23) are a conditional
composition for this specified writer, not a universal obstruction
to every D0 field readout or every stationary-law construction.

## 6. Actual use in the complete argument

The native future-profile kernel cannot identify two members of this
primary chart that differ at an accessible point. A verified
representation preserving these admitted contexts must therefore
retain their metric distinction. Equations (6),(11) give a concrete
readout map and (19) supplies its actual error norm for the existing
geometric recovery theorem.

This supplies a conditional operational interpretation of the primary
metric and curvature. It does not supply all-native context coverage,
a field-writing programme from one complete initial state, or the
complete Price-versus-field graph of ProspectiveExecution. The
actuator changes matter while holding the candidate metric fixed.
Nor does it choose the Book Info, task, clock or stationary law.
These are the exact physical interfaces still needed by the parent;
they are not defects repaired by more geometric root searches.
