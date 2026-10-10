# Native volume fibers do not determine the Einstein metric contrast

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input head: `ff5baf86642fca81714843b8ab48bed50939fe54`.
Status: general obstruction for a specified information class, with an
actual auxiliary-gate application. Positive GR/global closure remain OPEN.

The [preceding weighted-trace theorem](A4D_NATIVE_WEIGHTED_TRACE_LIFT_BOUNDARY.md)
left increasing degree, nonpolynomial spectral functions and nonlinear
auxiliary elimination outside its polynomial class. This result closes
those possibilities **when all geometric inputs still factor through the
physical volume density**. It does not exclude native metric-shape data.

## 1. Exact information and variation hypotheses

For a metric \(g\) on the fixed periodic four-carrier let
\(\nu_g(y)=\sqrt{|\det g(y)|}\). Consider native preparation data
\[
 d_h(g)=\mathcal D_h(\nu_g),\qquad F_h(g)=\Phi_h(d_h(g)).       \tag{1}
\]
The maps may be nonlinear, nonlocal, mesh dependent and unbounded. Their
data may include all density samples, differences, jets, spectral moments,
nonpolynomial spectral functions, density-dependent operators, lift maps,
records and refinement information. The condition is equality of inputs:
if two full density fields coincide pointwise, their native data coincide.
An encoding using only density, including a predeclared positive rational
encoding, preserves this equality. No continuity or polynomial assumption
on either map is required.

In a preparation problem with auxiliary variables, replace the second map
in (1) by the action's **unique value on its nonempty actual auxiliary
Euler fiber** over \(d_h\). Uniqueness is of the action value, not of the
state. All kernels remain. This condition is proved for the existing
positive-weight A2 compensator in Section 4, rather than postulated as
Einstein-contrast vanishing. A prescribed deterministic preparation that
itself factors through \(d_h\) is another instance of (1).

This is a fully specified candidate class. In particular:

* `archiveVolume` is the mean of \(1/\rho_i\); that global identity by
  itself does **not** establish that \(1/\rho_i\) is a physical volume
  density. A physical volume-only readout is an explicit hypothesis here.
* Additional geometric data that vary at fixed volume, such as an owned
  full coframe, anisotropic operator or shape-dependent constraint, are
  outside (1). It is not legitimate to erase them to apply this theorem.
* Multiple stationary values with a shape-dependent choice are outside
  the unique-value hypothesis. Such a choice needs its own native owner.
* Merely close densities do not imply close values for an unbounded map.
  Errors admitted below are bounded at the **action half-contrast** level,
  as required by the user's transfer criterion.

The candidate must admit the off-shell metric pencil below as a native
variation experiment. A sector that cannot represent these symmetric
metric probes has an unproved variation map; it does not satisfy that
required step by declaring its excluded fiber empty.

## 2. A curved Gram pencil with identical pointwise volume

Use the literal role order A,B,C,D, \(\eta=\operatorname{diag}(1,-1,-1,-1)\),
and the fixed covector \(n=(1,0,1,0)^T\). Put \(P=nn^T\), so
\(P\eta P=0\). On \(\mathbb T^4\), let
\[
 \Omega(y)=1+\tfrac1{10}\cos(2\pi y_2),\quad
 \Theta_s=\Omega\eta+\tfrac{s\Omega}{2}P,\quad
 e_s=\Theta_s-\eta.                                         \tag{2}
\]
The existing raw Gram owner gives exactly
\[
 g_s=\Theta_s\eta\Theta_s^T
 =\Omega^2(\eta+sP)
 =\Omega^2\begin{pmatrix}
 1+s&0&s&0\\0&-1&0&0\\s&0&s-1&0\\0&0&0&-1
 \end{pmatrix}=g_0+sV,\quad V=\Omega^2P.                    \tag{3}
\]
This is a straight metric pencil and a straight **raw** coframe pencil;
no directional centering or curved-path replacement is used. The research
Lean capsule proves the literal `a4dSiteGram` identity from symmetry and
\(P\eta P=0\); the concrete matrix satisfies both hypotheses exactly.
For the physical positive-determinant solder use the same fixed conversion
\(E_s=\Theta_s\eta=\Omega(I+(s/2)P\eta)\). Then
\[
 \det E_s=\Omega^4>0,\quad \det g_s=-\Omega^8,\quad
 \nu_{g_s}=\Omega^4\quad\hbox{for every }s.                 \tag{4}
\]
The nilpotent rank-one update has determinant one, as is also verified by
the full four-dimensional determinant. For \(|s|\le1/4\), these metrics
remain smooth Lorentz metrics, with \(g_{00}>0\) and fixed orientation.
The inverse is explicit:
\(g_s^{-1}=\Omega^{-2}(\eta-s\eta P\eta)\).
With \(\Omega\ge9/10\), this gives uniform nondegeneracy and all finite
smoothness bounds for this one compact experiment, independent of mesh.

The volume derivative has all ten symmetric slots
\[
 D\nu_g[H]=\tfrac12\nu_g\operatorname{tr}(g^{-1}H).
\]
Off-diagonal packed slots carry weight two. Its kernel has dimension nine
at every nondegenerate metric; (3) lies in that kernel at **every** \(s\).
All ten determinant derivatives and packing conventions are checked in
the certificate, not only the three nonzero entries of this probe.

## 3. Nonzero Einstein contrast on the same fiber

Write \(w=\Omega,p=\Omega',q=\Omega''\). Reconstructing all Christoffel
and Ricci components of (3) gives the standard-sign scalar
\[
 R_{\rm std}(g_s)=6(1+s)q/w^3.
\]
The literal owner's convention has \(R=-R_{\rm std}\), so its action is
\[
 I(s)=-\tfrac12\int w^4 R_{\rm std}
     =-3(1+s)\int wq
     =3(1+s)\int p^2
     =\frac{3\pi^2}{50}(1+s).                              \tag{5}
\]
Periodic integration by parts has no boundary term. An independent
Einstein-tensor variation check gives
\[
 \tfrac12\nu_g G_{\rm std}^{ij}V_{ij}=2p^2-wq,
 \qquad \int(2p^2-wq)=3\pi^2/50.                           \tag{6}
\]
Thus the sign and normalization agree with the action derivative. The
two pointwise densities differ by a periodic total derivative, not by a
discarded source. At \(y_2=0\), the owner scalar is
\(2400\pi^2(1+s)/1331\ne0\). These are genuinely curved **off-shell
probe metrics**, not claimed native Einstein solutions. Their different
action values also prevent treating this deformation as physical gauge.

The [published physical probe theorem](https://github.com/gvakhrushev/d0_15/blob/af221e2fed92821c52afc88a5500774de8cd9a93/02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md)
applies to this explicit smooth compact pencil. Its Levi-Civita midpoint
construction provides nonempty log-\(O(h)\) endpoint preparations with
**all 24 connection rows** \(O(h^2)\); it is not an exact joint/source
solution assertion. Its uniform action/contrast law yields, with
\(\epsilon_h=h^{1/3}\),
\[
 \frac{\Delta I_h}{\epsilon_h}
   =\frac{3\pi^2}{50}+O(h^{2/3}),\qquad
 \Delta I_h=\tfrac12(I_h(g_{s+\epsilon_h})-I_h(g_{s-\epsilon_h})).
                                                                    \tag{7}
\]
By (1) and (4), the native half-contrast is identically zero. In the
allowed recording/refinement-error version it is \(O(h)\), hence its
quotient by \(\epsilon_h\) tends to zero for every fixed \(a\ne0\).
It follows that
\[
 \lim_{h\to0}\frac{|a^{-1}\Delta I_h^N-\Delta I_h|}{\epsilon_h}
      =\frac{3\pi^2}{50}>0.                                \tag{8}
\]
In particular the proposed \(O(h)\) half-contrast transfer is impossible.
This conclusion does not differentiate any error estimate and does not
require a uniform inverse, a degree bound or a spectral gap.

Any cosmological volume term or independently specified source functional
that also factors through the same density has zero contrast on this
fiber. It cannot repair (8). The theorem does not exclude arbitrary
shape-sensitive native matter or a different combined action. The source
is not fitted to (6) after seeing its value.

## 4. Actual nonlinear auxiliary elimination does not recover lost shape

The existing rational `A2CompensatorNoether` owner defines
\[
 A(B,W,h,\eta)=2\sum_eW_e(h_e-\tfrac12(B^T\eta)_e)^2,
 \qquad (BWB^T)\phi=BWh,\quad\eta=2\phi.                   \tag{9}
\]
For **every** finite \(B,h\) and positive \(W\), its
`normal_equation_exists` proves nonemptiness and `physical_residual_unique`
proves the same residual for every solution \(\phi\). Therefore every
auxiliary-stationary state has the same action value. The new Lean capsule
derives both value equality and a nonempty unique-value proposition from
those literal owners. It retains all normal-operator kernel directions;
no root, inverse or gauge complement is selected.

This value can genuinely be nonlinear in the density. On the unsigned
four-cycle let \(a=1+s>0\), \(W=(a,1,1,a)\),
\(h=(1,0,0,0)\). These are the actual `rhoWeight` weights from
\(1/\rho=(a,1,1,1)\). With
\[
 t=\frac{a}{2(a+1)},\qquad
 \phi=(t/a,2t,-t,0),\qquad r=tW^{-1}(1,-1,1,-1)^T,
\]
all four normal rows vanish, and every kernel translate of \(\phi\)
has the same value
\[
 A_{\rm eff}(s)=\frac{1+s}{2+s},\qquad A_{\rm eff}'''(0)=3/8. \tag{10}
\]
This is a real exception to a polynomial-profile argument. It is not a
full edge-gate solution: its edge response is \(4t(1,-1,1,-1)\ne0\).

Nevertheless, if the geometric inputs \(B,W,h\) in (9) are functions
only of \(\nu_g\), they are identical on (3). The unique auxiliary
action value is then identical too, regardless of its nonlinearity on
other density paths. Thus this auxiliary-only mechanism satisfies (1)
under the stated data condition and is excluded by (8). A geometric
dependence of the edge field or incidence on additional metric-shape
data is deliberately left outside the class. Rational encoding of the
equal volume fields causes no type mismatch with the literal rational
owner: equal inputs have equal encodings. The theorem does not assert
that a particular encoding is already selected as physical by D0.

## 5. Scope, hostile controls and the next native obligation

The exact certificate replays **72 controls** and independently recomputes the full metric, inverse,
determinants, Christoffels, Ricci, Einstein pairing and periodic coefficient.
It checks all ten packed metric slots, the nine-dimensional volume kernel,
the explicit Lorentz spin connection and all 24 continuum torsion rows,
the actual rational four-cycle elimination and its full kernel family.
The continuum torsion check is distinct from the consumed finite
connection-Euler residual theorem. Six research Lean propositions compile
with 52 transitive D0 source pins and no `sorryAx`; one is axiom-free and
the others use only propext, Classical.choice and Quot.sound.
Hostile controls retain these distinctions:

* Equal **total** archive volume is weaker than equal pointwise density:
  two site densities \((1+s,1-s)\) have constant sum but a weighted trace
  with diagonal operator \((1,2)\) changes as \(3-s\).
* A shape-sensitive operator may vary at fixed volume; it is outside (1).
* Nonunique critical values can differ at the same fixed inputs; the
  positive-weight compensator's unique-value theorem is used, not assumed
  for arbitrary nonlinear gates.
* Small input error alone is insufficient under amplification. The
  transfer theorem requires the declared total half-contrast error bound.
* Flat \(\Omega\) gives zero Einstein contrast here. The nonconstant
  curved factor is essential and explicitly fixed before preparation.

No completeness theorem for the full core is claimed. The remaining
native route must carry metric-shape information, an actual corresponding
action/variation law, and its physical/refinement maps. Density-only
nonlinear spectral or auxiliary constructions cannot supply the missing
ten-component variational arrow on this admitted experiment. This removes
a whole information class without adding a physical selector or modifying
the original #310/#202/#317 terminals.
