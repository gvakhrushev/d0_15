# Coframe-coupled Hodge weights: exact fibers and the missing scale response

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Input: `2d3f5fff0273ae5c028c07343a72b27b54374602`.
Status: constructive exact special metric/link readout, and a complete
contrast obstruction for the explicitly stated additive class below.
**Native nonlinear GR and global closure remain OPEN.**

The [connection-only obstruction](A4D_NATIVE_CONNECTION_ACTION_BOUNDARY.md)
does not cover coframe-dependent weights. This follow-up tests that real
exception. It uses existing supplied-argument scalar owners; it does not
select a new action, matter law, coefficient, constraint or native gate.
The exact special fibers do not imply general finite surjectivity or
compatibility with a native interlevel transition.

## 1. Actual owners and tested bindings

`Geometry.ArchiveMetricMeasureHodgeLift.hodgeMetricMeasureWeight` is

\[
 W_k(\mu,p)=\mu^{1-k}p.                                      \tag{1}
\]

Its owner theorem proves the degree-zero and degree-one identities and
the cardinalities 16 and 4. Its actual proposition does **not** quantify
over competing Hodge laws and prove uniqueness. The function definition
admits real arguments; the positive density/conductance interpretation
in the comments is not a Lorentz positivity theorem. These actual types
are printed in the research capsule.

Under the explicit geometric diagonal binding

\[
 \mu=\sqrt{|\det Q|},\qquad c_r=\mu (Q^{-1})^{rr},\qquad
 W_S=\mu^{1-|S|}\prod_{r\in S}c_r,                          \tag{2}
\]

the spatial conductances can be negative. This is an algebraic instance
of (1), not an asserted construction of a selected native Lorentz Hodge.
If `Q -> s Q`, `s>0`, then `mu -> s^2 mu`, `c_r -> s c_r` and

\[
 W_S\longmapsto s^{2-|S|}W_S.                              \tag{3}
\]

All 16 slots are retained. In particular every degree-two weight is
unchanged. For a general nondiagonal metric the explicitly tested
exterior pairing is the full second compound

\[
 H_{ab,cd}(Q)=\mu\{(Q^{-1})^{ac}(Q^{-1})^{bd}
                         -(Q^{-1})^{ad}(Q^{-1})^{bc}\}.
                                                                    \tag{4}
\]

The inverse contributes `s^-2` and the density `s^2`, so (4) is exactly
scale invariant as well. This extends (2) algebraically; the flat-star
owner supplies its signs/minor conventions, not a selected curved law.

The old `Gauge.discreteYangMillsAction` permits arbitrary supplied
`Killing` and `K`. Take its index types to be singletons, its argument
type to be six matrix curvatures, and its pairing to be
`sum H_ab Tr(X_a Y_b)`. Its literal value is

\[
 -\sum_{a,b}H_{ab}(Q)\operatorname{Tr}(C_aC_b).             \tag{5}
\]

That equality is compiled. Testing this binding does not assert that
the core has already selected it or its odd-plaquette curvature map.
The supplied nonpositive-pairing hypothesis in the old positivity
theorem is not assumed. In Lorentz signature the two-form metric and
the internal trace pairing each have three signs of each kind.

This class really does depend on shape: with one nonzero `02` curvature,
changing from `diag(1,-1,-1,-1)` to `diag(4,-1/4,-1,-1)` changes (5),
although both volume densities are one. It is therefore outside
the previous coframe-blind class. Arbitrary nonlinear/nonlocal functions
of the scale-invariant data remain scale invariant.

There is a second actual owner of such data:
`a4dDressedLink(F_x,R,F_y)=F_x R F_y^-1`. Its value is unchanged when
both raw solders are multiplied by the same nonzero scalar. This exact
statement is compiled with the required invertibility hypothesis. A
functional of these dressed links is allowed below, including nonlocal
dependence. No full affine translation quotient is inferred.
The actual sitewise Lorentz transformation preserves the transported
Gram matrix and conjugates every based curvature at its owner site.
The trace pairings in (5) are invariant under that conjugation. The
checker verifies this covariance, rather than importing the earlier
Lorentz-descent failure of the different literal flux action.

## 2. The complete class tested here

Use the actual raw solder `F`, pull links `R`, and retained variables `z`.
The center and Gram map remain

\[
 T_R(F)_r(x)=\tfrac12\{F_r(x)+F_r(x-r)R_{x-r,r}\},\qquad
 Q=T_R(F)\eta T_R(F)^T,\quad \mu_x=|\det T_R(F)(x)|.       \tag{6}
\]

Consider all scalar bindings

\[
 I_h^N(F,R,z)=A_h(F,R,z)+B_h((\mu_x)_x,z),\qquad
 A_h(cF,R,z)=A_h(F,R,z)\quad(c>0).                        \tag{7}
\]

`A_h` can have arbitrary coframe/connection/shape dependence consistent
with the displayed global scale identity. `B_h` can be any function of
the **entire** volume-density vector, with arbitrary mesh dependence,
nonlinearity, nonlocality and sensitivity. There is no polynomial-degree,
convexity, positivity, bounded-coefficient or uniqueness hypothesis.
The metric Hodge binding (5), its nonlinear functions, and scalar
functions of the actual dressed links give tested instances of `A_h`.
The class also includes an arbitrary separate volume-only action.

The admitted native probes must include the two explicit families in
Section 3 and their uniform positive raw scalings, at fixed links and
the same independently retained `z`. An additional native constraint
that forbids those probes is outside this theorem and needs its own
owner and metric-variation/recovery analysis. Native on-shell or
interlevel admission is not built into this definition.

This is an additive separation requirement. A term with genuine mixed
scale/shape response, including the existing curvature-linear star
insertion, is outside (7). A volume-dependent coefficient multiplying
a shape-dependent term need not satisfy (7). The theorem does not
exclude those mechanisms or prove this class exhausts the core.

There is a variational completeness statement **within this specified
response class**. Suppose the admissible domain is a positive scaling
cone, S is C1 along its scaling rays, and its full raw radial derivative
`d S(exp(u)F,R,z)/du at u=0` equals a continuous function `G(mu,z)` of
volume data only. Put `V=sum mu>0`, `p=mu/V` and

\[
 B(\mu,z)=\frac14\int_1^V G(tp,z)\,\frac{dt}{t}.
\]

The fundamental theorem of calculus and `mu(cF)=c^4 mu(F)` imply that
S-B has zero derivative on every scaling ray, hence is scale invariant.
Thus every such S has representation (7). Conversely a differentiable
representation (7) has a volume-only radial response. The integral is a
proof of decomposition, not a selected native term or state selector.
Its completeness concerns volume-only radial response, not every D0
functional. The obstruction below itself does not require differentiability
of A or B, because it compares actual finite endpoint values.

## 3. Two exact native readout fibers at every allowed level

Set `L in 4N`, `h=1/L`, `N=L-2` in the actual native Role carrier,
`f(y)=1+cos(2 pi y)/10` and choose `c=1` or `c=2`.
Write

\[
 b=(c,c^{-1},1,1),\quad
 \Theta_c(y)=\operatorname{diag}(cf,-f/c,-f,-f),\quad
 E_c=\eta\Theta_c^T=\operatorname{diag}(cf,f/c,f,f).
\]

Their metrics and volume densities are

\[
 g_c=f^2\operatorname{diag}(c^2,-c^{-2},-1,-1),\qquad
 \sqrt{|\det g_c|}=f^4.                                  \tag{8}
\]

These are smooth, nondegenerate, periodic metrics with the same density
pointwise. The determinant identity is compiled; no equality of merely
approximate volumes is being used.

Let `B_0i` have ones in entries `(0,i)` and `(i,0)`. The torsion-free spin
connection in the existing pull convention is

\[
 \omega_0=0,\qquad
 \omega_i=(b_i/b_0)(f'/f)B_{0i},\qquad
 R_{h,r}(x)=C(h\omega_r(hx)),\quad
 C(Z)=(I-Z/2)^{-1}(I+Z/2).                               \tag{9}
\]

Indeed `de^i=b_i f' dy_0 wedge dy_i` cancels
`omega^i_0 wedge e^0`; all other torsion slots vanish. The checker
retains all 24 torsion slots and independently derives all 24 leading
physical connection Euler rows from all four face-factor positions.
Every one is zero. It also retains a sign-reversed-connection control,
which fails the leading equations.

Here there is an **exact**, not only approximate, inverse of the actual
transported center. Put `y=hx`, `delta=pi h` and define raw rows

\[
 F_{h,0}(x)=b_0\left[1+\frac{\cos(2\pi y_0+\delta)}
                                     {10\cos\delta}\right]e_0^T,
\qquad
 F_{h,i}(x)=\Theta_{c,i}(y)(I-h\omega_i(y)/2),\quad i>0.    \tag{10}
\]

For row zero, `R_0=I` and the sum of cosines at arguments
`2 pi y_0 +/- delta` is `2 cos(2 pi y_0) cos(delta)`.
For a spatial row, both `F_i` and `R_i` are constant along its own
direction, and

\[
 (I-h\omega_i/2)(I+C(h\omega_i))=2I.
\]

Consequently, exactly at every site and for every allowed `L`,

\[
 T_{R_h}(F_h)=\Theta_c(hx),\quad Q_h=g_c(hx),\quad
 \mu_{h,c}(x)=f(hx_0)^4.                                \tag{11}
\]

The temporal and spatial inverse identities compile. Their full finite
instantiations, row order and all ten Gram components are checked exactly.
This construction does not invert the full arbitrary even-grid centering
operator; its previously established kernel/cokernel remains intact.

All preparation bounds come from these formulas. `9/10<=f<=11/10`,
`cos(pi h)>=1/sqrt(2)` and the temporal raw entry is at least
`c(1-sqrt(2)/10)>4c/5`. The raw matrix is triangular with spatial
diagonal entries `-b_i f`, hence invertible. For these two values of c,
`b_i/b_0<=1` and `h|omega_i|/2<1/9` using `pi<4`; the Cayley factors
and inverses are uniformly bounded and in the proper Lorentz identity
component. Differentiating the displayed smooth interpolating formulas
gives uniform bounds of any fixed finite order. No grid inverse estimate
or compactness of arbitrary link families is assumed.

Now scale `F_h` to `sqrt(s) F_h`, with s in a fixed interval about 1,
and keep `R_h,z` fixed. The actual center is linear in F, so

\[
 Q_{h,c}(s)=s g_c(hx),\qquad \mu_{h,c}(s)=s^2 f(hx_0)^4.  \tag{12}
\]

Thus the two volume vectors are exactly equal at **both** endpoints
of every such probe. There is no small volume error for an uncontrolled
`B_h` to amplify. Constant metric scaling preserves the connection (9).
The full physical connection residual is `O(h^2)` in each of its 24 rows
by the zero first-order coefficient and bounded smooth stencil remainder.
These prepared families are not asserted to be native critical points.

## 4. Quantitative contrast obstruction, including every separate volume term

The six leading physical face densities, in the existing half-Einstein
normalization and curvature sign, are three copies of
`(f f''-(f')^2)/c^2` and three copies of `(f')^2/c^2`. Their sum is
`3 f f''/c^2`. Therefore

\[
 I(g_c)=-\frac3{c^2}\int_0^1(f')^2dy_0
       =-\frac{3\pi^2}{50c^2},\qquad
 I(g_1)-I(g_2)=-\frac{9\pi^2}{200}=:D_*\ne0.             \tag{13}
\]

This is also an explicit curvature witness. These comparison metrics
are not asserted to solve a vacuum or an independently sourced system.

For the unchanged naked-star physical action, `I_h^star=h^2 A_h`,
its exact coframe homogeneity and the pinned smooth preparation estimate
give, uniformly in the two experiments,

\[
 I_{h,c}^{\star}(s)=s I_{h,c}^{\star}(1),\qquad
 I_{h,c}^{\star}(1)=I(g_c)+O(h).
\]

Let `Delta J=(J(1+epsilon)-J(1-epsilon))/2`. The scale-invariant part
of (7) cancels separately in both native experiments. Their volume
inputs agree exactly by (12), and z agrees. Hence

\[
 \Delta I^N_{h,1}=\Delta I^N_{h,2},\qquad
 \Delta I^{\star}_{h,1}-\Delta I^{\star}_{h,2}
      =D_*\epsilon+O(\epsilon h).                         \tag{14}
\]

Take one fixed nonzero calibration a. Allow any recording/refinement
errors whose calibrated total contribution to each contrast is `O(h)`.
Writing the resulting two transfer errors as `E_{h,1}, E_{h,2}`, (14)
implies

\[
 E_{h,1}-E_{h,2}=-D_*\epsilon+O(\epsilon h+h).
\]

At `epsilon=h^(1/3)`, for sufficiently small h,

\[
 \max_c |E_{h,c}|\ \ge\ \frac{9\pi^2}{800}h^{1/3}.       \tag{15}
\]

Thus the requested `O_V(h)` unnormalized contrast error cannot hold
for the whole stated class of metrics. The normalized derivative errors
cannot both tend to zero, let alone be `O_V(h^(2/3))`. The two experiments
share the calibration; assigning them different calibrations would alter
the contract. Indeed their native contrast equality survives even a
common mesh-dependent multiplier.

**Theorem.** Every binding (7) admitting (10)--(12) fails native contrast
transfer on at least one of the two explicitly given smooth metric
families. This excludes scale-invariant coframe/connection dynamics plus
any separate volume-density functional. It includes nonpolynomial and
nonlocal functions; it does not exclude mixed scale/shape response.

## 5. Full native gates: retain weight variations and distinguish empty fibers

For the specifically tested quadratic binding (5), with weights smooth
on the nondegenerate transported-metric domain and odd curvature of the
actual links, the complete derivative contains both terms

\[
 -\sum dH_{ab}\operatorname{Tr}(C_aC_b)
 -\sum H_{ab}\operatorname{Tr}(dC_a C_b+C_a dC_b).          \tag{16}
\]

At identity links all `C_a=0`, so (16) vanishes for **every** raw and link
variation, including the link dependence of the transported metric.
These are exact full levelwise critical points of this specified
binding for every admitted raw solder. The generic variable-weight
zero-curvature derivative is compiled. Zero action at nonzero curvature
is not a substitute for this argument.

Choose the exact temporal inverse (10), the spatial rows `Theta_i`, and
identity links. Its actual metric is again exactly `g_1(hx)`, which is
curved and non-Einstein. The previously derived physical connection row
at `y_0=1/4`, in direction `(r=1,G_01)`, obeys

\[
 E_{1,G_{01}}=f(y_0)^2-f(y_0-h)^2,\qquad
 E_{1,G_{01}}/h\longrightarrow-2\pi/5.                    \tag{17}
\]

Native stationarity of the coframe-coupled quadratic binding therefore
does not imply physical `O(h^2)` preparation or Einstein soundness for
this unrestricted levelwise gate/readout class. The 24 physical rows
are retained; these flat-link native roots are distinct from (9).
Additional native/interlevel or matter equations are not assumed solved.

A separate constant volume term `lambda sum mu` changes the gate, but
does not supply a repair. Along the actual raw homothety it gives the
full action profile `constant+lambda(1+t)^2 V`, where `V=sum mu>0`.
Stationarity of even this one admitted variation forces `lambda=0`.
For nonzero lambda the source-free full gate of this scale-invariant
plus constant-volume class is empty. The derivative and implication
compile. No positive closure is inferred from empty fibers.
An arbitrary nonlinear `B_h` can have stationary volumes and is not
covered by that empty-fiber statement; it still fails (14).

For (4), the exact coframe-coupled metric variation is
`dmu=mu Tr(Q^-1 V)/2`, `d(Q^-1)=-Q^-1 V Q^-1`, followed by the ordinary
product rule in (4). The checker compares that expression with direct
differentiation in all ten symmetric components, retaining off-diagonal
packed weight 2. For `V=Q`, every `dH` is zero. This is a scale identity,
not the physical diffeomorphism Ward identity or a constructed matter
stress law. These are ten derivatives of the tested function of Q;
arbitrary independent finite Q variations are not thereby proved to lift
through the even-grid native center. Pointwise rescaling of raw rows does not in general rescale
the transported center pointwise; only the admitted uniform scaling was
used in the finite obstruction and empty-gate argument.

## 6. Evidence and retained obligations

The research capsule has 18 compiled propositions with 56 transitive
D0 source pins, standard axioms only, and printed actual owner types.
The all-mesh preparation, analytic continuum passage and no-go (15) are
proved above; they are not advertised as compiled continuum theorems.

The immutable exact checker has 103 grouped exact controls. It verifies
all Hodge grades, nondiagonal
compound scaling, real shape dependence, all ten metric derivatives
and packed weights, the exact special transported fibers, the 24
torsion and physical leading Euler rows, six physical face densities,
and the full variable-weight zero-curvature variation. It retains all
24 full native connection rows on an explicit constant curved lattice
field, including the derivative of its transported metric weights;
omitting that term changes the gate. Nine false scope ledgers and explicit exceptions protect probe admission, additive
separation, native on-shell status and global closure.

For a realization whose admitted domain contains these probes, the first
remaining native obligation is now more precise: construct an independently
owned action/variation/source/refinement realization with mixed scale/shape
response, or prove completeness of an excluded native class. A smaller
independently owned physical state domain retains its own variation,
soundness and recovery obligations. The existing curvature-linear star
insertion has that response, but equality with a selected native
functional still does not follow from its invariant classification.

Native interlevel admission, independent matter and physical Ward,
the coupled nonlinear solve, soundness/recovery, physical causal
readouts and positive GR remain open. Original #310 fixed-source/raw
owner, #202 full-affine stationary and #317 stratification terminals
are preserved. No supported Lean owner, release claim or BOOK is changed.
