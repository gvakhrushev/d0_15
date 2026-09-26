# MEMO A4D — nonlinear Einstein J² bridge / upper wall

**Task:** \`EXP-A4D-NONLINEAR-EINSTEIN-J2-BRIDGE\`  
**Execution:** PR #208  
**Status:** exact structural terminal / upper-wall obstruction classified  
**Baseline:** \`4c748017c957fa335c9826b123a874c4b2b67925\`  
**Certificate:** \`02_REGISTRY/research/certificates/a4d_nonlinear_einstein_j2_bridge_check.py\`

## 0. Terminal verdict

The nonlinear Einstein J² bridge is much narrower than the older provenance
packets suggested, but it is not unconditionally closed.

The task reaches four load-bearing conclusions.

### A. The selected finite action already owns a nonlinear metric carrier

On the all-site nondegenerate solder sector, the merged nonlinear Lorentz
quotient has complete orbit coordinates

\[
Q_x=\Theta_x\eta\Theta_x^T,
\qquad
K_{x,r}=\Theta_xL_{x,r}\Theta_{x+r}^{-1}.
\tag{0.1}
\]

Thus the metric variable relevant to the star action is not an external test
field. It is an exact nonlinear quotient coordinate of the selected finite
action.

For the full-affine relative-solder branch one similarly has

\[
\widehat\Theta=\Theta-b^{\flat_n},
\qquad
\widehat Q=\widehat\Theta\eta\widehat\Theta^T,
\tag{0.2}
\]

and merged #184 proves
\(\widehat\Theta'=\widehat\Theta g^{-1}\), hence
\(\widehat Q'=\widehat Q\).

So the old E-PROV statement “finite metric provenance missing” is no longer the
first blocker for this A4D star-action lane.

### B. The #201 Einstein detector differentiates that genuine metric quotient

Let \(H\) be the \(4\times4\) matrix whose rows are the perturbations of the
four solder vectors. At flat solder,

\[
DQ_{\rm flat}[H]=H\eta+\eta H^T.
\tag{0.3}
\]

For an arbitrary symmetric metric perturbation \(q=q^T\), #201 uses exactly

\[
\boxed{
H(q)=\frac12q\eta .
}
\tag{0.4}
\]

Since \(\eta^2=I\),

\[
\boxed{
DQ_{\rm flat}[H(q)]=q.
}
\tag{0.5}
\]

Therefore the merged exact identity

\[
\boxed{
K_{\star,\mathrm{metric}}(k)=\frac14K_{E_\eta}(k),
\qquad
c_{\rm sp}=0
}
\tag{0.6}
\]

is a statement about the tangent response of the actual nonlinear metric
orbit coordinate, not a fit to an unrelated stencil carrier.

### C. Low momentum is regular, but global all-mode connection elimination fails

For a general complex Fourier character a real quadratic action pairs mode
\(z\) with mode \(z^{-1}\). The present certificate performs that polarization
explicitly.

On the diagonal character

\[
z_A=z_B=z_C=z_D=t,
\tag{0.7}
\]

the correctly polarized flat Lorentz-connection block satisfies

\[
\boxed{
\det H_{AA}^{\rm pol}(t)
=
\frac{(t^2+1)^{12}}{16t^{12}}.
}
\tag{0.8}
\]

At zero momentum,

\[
\boxed{
\det H_{AA}^{\rm pol}(1)=256,
}
\tag{0.9}
\]

so the low-momentum auxiliary connection is regular.

At the first diagonal quarter-wave,

\[
t=i,
\tag{0.10}
\]

which occurs already for side length \(L=4\) (\(N=2\)),

\[
\boxed{
\rank H_{AA}^{\rm pol}=16.
}
\tag{0.11}
\]

More strongly, if \(H_{Aq}\) denotes the connection source restricted to the
ten genuine symmetric metric directions from (0.4), then

\[
\boxed{
\rank\!\left[
(H_{AA}^{\rm pol})^T\mid H_{Aq}
\right]
=20.
}
\tag{0.12}
\]

Thus the problem is not merely nonuniqueness: some metric perturbations violate
the Fredholm compatibility condition for the linearized connection equation.

An explicit witness is supported on the three Role-A boost coordinates,

\[
\lambda_{(A,K_1)}
=
\lambda_{(A,K_2)}
=
\lambda_{(A,K_3)}
=1,
\tag{0.13}
\]

all other components zero. Exactly,

\[
H_{AA}^{\rm pol}\lambda=0,
\tag{0.14}
\]

while for the symmetric metric basis direction \(q_{11}\),

\[
\boxed{
\lambda^TH_{Aq}(q_{11})=-(1+i)\ne0.
}
\tag{0.15}
\]

The complex character is only Fourier notation. The conjugate mode \(t=-i\)
gives the corresponding real sine/cosine obstruction.

Therefore there is no single smooth **all-mode** finite section

\[
K_*(Q)
\tag{0.16}
\]

through flat that solves the connection Euler equation for every finite metric
perturbation on every refinement carrier.

The exact terminal obstruction is

\[
\boxed{
\texttt{STAR-J2-BRIDGE-BLOCKED-BY-DIAGONAL-QUARTER-WAVE-CONNECTION-RESONANCE}.
}
\tag{0.17}
\]

### D. The surviving continuum branch is sharply identified

The resonance is ultraviolet: it sits at fixed lattice phase \(\pi/2\), while
the low-momentum point \(t=1\) remains regular.

Hence this result does **not** kill the continuum Einstein route. It kills the
naive route that first integrates the connection smoothly on the entire finite
metric carrier and only then takes the continuum limit.

The surviving route is:

\[
\boxed{
\text{smooth metric sampling}
\;\to\;
\text{selected low-frequency connection branch}
\;\to\;
\text{uniform normal-stencil control}
\;\to\;
J^2\text{ metric response}.
}
\tag{0.18}
\]

The smallest missing theorem is named below as **H-J2-SMOOTH**.

---

## 1. Exact nonlinear metric/connection geometry already owned

### 1.1 Lorentz quotient

Merged nonlinear quotient work proves exact local proper-Lorentz invariance of
the star density and a free proper quotient on nondegenerate solder.

The descended action may therefore be written locally as

\[
\overline S_\star(Q,K).
\tag{1.1}
\]

No continuum manifold is used in this statement.

### 1.2 Exact metric compatibility of the dressed link

Because each linear link is Lorentz,

\[
L_{x,r}\eta L_{x,r}^T=\eta,
\tag{1.2}
\]

the dressed link obeys

\[
\begin{aligned}
K_{x,r}Q_{x+r}K_{x,r}^T
&=
\Theta_xL_{x,r}\Theta_{x+r}^{-1}
(\Theta_{x+r}\eta\Theta_{x+r}^T)
\Theta_{x+r}^{-T}L_{x,r}^T\Theta_x^T\\
&=
\Theta_xL_{x,r}\eta L_{x,r}^T\Theta_x^T\\
&=
Q_x.
\end{aligned}
\tag{1.3}
\]

Hence

\[
\boxed{
K_{x,r}Q_{x+r}K_{x,r}^T=Q_x.
}
\tag{1.4}
\]

So \(K\) is an exact finite \(Q\)-isometry transport.

This is not yet a finite Levi-Civita theorem. Merged variation pressure
explicitly disproves the shortcut that identifies the exact finite connection
Euler equation with the naive forward torsion-free equation.

### 1.3 Flat stationarity

At flat solder and flat links,

\[
Q=\eta,\qquad K=I,
\tag{1.5}
\]

and merged star-variation work proves

\[
dS_\star|_{\rm flat}=0.
\tag{1.6}
\]

Thus any continuum response of the naked star branch must vanish on the flat
metric.

### 1.4 Joint-residual completion does not change the flat J² gate

Merged #201 gives

\[
R=O(X^4t),
\qquad
Q_R=O(X^8t^2),
\tag{1.7}
\]

and, if both connection defect and translation scale as \(O(\varepsilon)\),

\[
R=O(\varepsilon^5),
\qquad
Q_R=O(\varepsilon^{10}).
\tag{1.8}
\]

Therefore

\[
\boxed{
j^2_{\rm flat}Q_R=0.
}
\tag{1.9}
\]

The affine quotient completion cannot modify the coefficient in (0.6).

---

## 2. Why the #201 metric lift is intrinsic

The owned solder vector is

\[
v_r=\eta\Theta_r^T.
\tag{2.1}
\]

If \(H\) stores \((\delta v_r)^T\) as rows, then

\[
H=\delta\Theta\,\eta,
\qquad
\delta\Theta=H\eta.
\tag{2.2}
\]

At \(\Theta=\eta\),

\[
Q=\Theta\eta\Theta^T=\eta
\tag{2.3}
\]

and

\[
\delta Q
=
\delta\Theta+\delta\Theta^T
=
H\eta+\eta H^T.
\tag{2.4}
\]

The exact section (0.4) follows.

Any two lifts of the same symmetric \(q\) differ by a tangent in the kernel of
the Gram map, i.e. by a local-Lorentz vertical direction on the nondegenerate
orbit.

Because the finite action is exactly local-Lorentz invariant, the quotient
metric Hessian is independent of this section choice.

The quarter-wave incompatibility is likewise not removed by changing section:
a Lorentz-vertical change of coframe changes the connection source only by an
image vector of the connection block, while the Fredholm pairing (0.15)
detects its cokernel class.

---

## 3. Correct Fourier polarization and the first resonance

The period-two pressure test used only \(z_r=\pm1\). Those characters are
self-conjugate.

For a general unit character, using the same-mode quadratic expression is not
valid. A real periodic quadratic action pairs \(z\) with \(z^{-1}\).

The certificate therefore introduces independent connection amplitudes
\(A(z)\) and \(B(z^{-1})\), expands each plaquette to the mixed bilinear order,
and extracts the polarized block \(H_{AA}^{\rm pol}(z)\).

This task does **not** claim a complete four-variable singular-set
classification.

The diagonal slice

\[
z_A=z_B=z_C=z_D=t
\tag{3.1}
\]

is already enough to decide the all-mode-elimination question. On that slice,

\[
\boxed{
\det H_{AA}^{\rm pol}(t)
=
\frac{(t^2+1)^{12}}{16t^{12}}.
}
\tag{3.2}
\]

Hence

\[
\det H_{AA}^{\rm pol}(1)=256,
\tag{3.3}
\]

but

\[
\det H_{AA}^{\rm pol}(i)=0.
\tag{3.4}
\]

At \(t=i\), the rank and metric-source incompatibility are exactly (0.11) and
(0.12).

Therefore:

- the Einstein low-momentum symbol is not threatened;
- the auxiliary connection is not globally eliminable on the full finite
  metric carrier;
- the first certified obstruction appears already at \(L=4\);
- the obstruction is ultraviolet in a refinement interpretation.

---

## 4. Local implicit elimination survives only in regular sectors

At a fixed regular character, invertibility of the connection derivative lets
the ordinary finite-dimensional implicit-function theorem solve

\[
E_K(Q,K)=0
\quad\Longrightarrow\quad
K=K_*(Q)
\tag{4.1}
\]

near flat.

On such a branch define

\[
S_{\star,\mathrm{eff}}(Q)
=
\overline S_\star(Q,K_*(Q)).
\tag{4.2}
\]

Its quadratic Hessian is the Schur complement.

Near zero momentum this is precisely the object used in #201 and gives

\[
D^2S_{\star,\mathrm{eff}}|_{\rm flat}
=
\frac14K_{E_\eta}.
\tag{4.3}
\]

At the diagonal quarter-wave the derivative with respect to the connection is
singular and the source is not in its image.

A pseudoinverse does not repair this, because the equation is genuinely
incompatible for some metric directions.

Nor may the new null directions simply be called gauge: the actual finite
local-Lorentz verticals involve correlated coframe and connection variations.
The Fredholm obstruction is already computed on the metric quotient.

---

## 5. Why a flat tangent can still control a full nonlinear J² limit

Let \(g\) be a fixed smooth Lorentz metric, \(x\in T^4\), and use strict
\(g\)-normal coordinates at \(x\). Then

\[
g_{ab}(x)=\eta_{ab},
\qquad
\partial_cg_{ab}(x)=0.
\tag{5.1}
\]

For mesh

\[
\varepsilon_N=(N+2)^{-1}
\tag{5.2}
\]

and any fixed radius-two offset \(k\),

\[
g_{ab}(\varepsilon_Nk)-\eta_{ab}
=
\frac12
\partial_c\partial_dg_{ab}(x)
\,\varepsilon_N^2k^ck^d
+
O(\varepsilon_N^3).
\tag{5.3}
\]

Thus

\[
\boxed{
q_N=O(\varepsilon_N^2)
}
\tag{5.4}
\]

on the shrinking normal stencil for an arbitrary finite Lorentz metric
2-jet.

No weak-field assumption on curvature is used.

This is the mechanism that can turn the exact flat derivative into a full
nonlinear continuum-center statement: on every shrinking normal stencil the
finite metric perturbation itself becomes small.

What is missing is uniform control of the **actual selected star response**
through the connection sector.

---

## 6. H-J2-SMOOTH — the single surviving upper-wall theorem

A sufficient bridge theorem is:

> **H-J2-SMOOTH.** For every smooth Lorentz metric \(g\), point \(x\), and
> admissible strict normal frame \(F\), there exists a selected finite
> connection family \(K_N[g,F]\) for the sampled star action such that:
>
> 1. its infrared component agrees with the regular connection-Euler branch
>    through \(K=I\);
> 2. the certified quarter-wave/resonant sector is either absent on the
>    selected smooth-sampling image, canonically resolved, or contributes
>    \(o(1)\) to the reconstructed normalized metric response;
> 3. after the unique \(\varepsilon_N^{-2}\) normalization that keeps the
>    quadratic Einstein response finite, the connection-reduced response is
>    uniformly \(C^2\) in the normal-stencil regime
>    \(q_N=O(\varepsilon_N^2)\);
> 4. the normalized Taylor remainder beyond the #201 derivative is
>    \(O(\varepsilon_N^2)\);
> 5. the resulting center response depends, in the limit, only on the ordinary
>    metric \(2\)-jet.

Under H-J2-SMOOTH,

\[
\mathcal E_{\star,N}(q_N)
=
\frac14E_{\eta,N}(q_N)
+
O(\varepsilon_N^2).
\tag{6.1}
\]

The already-owned E-NJET result gives

\[
E_{\eta,N}
=
-2G[g](x)
+
O(\varepsilon_N^2)
\tag{6.2}
\]

after geometric reconstruction in normal coordinates.

Therefore

\[
\boxed{
\mathcal E_{\star,N}
\longrightarrow
-\frac12G[g].
}
\tag{6.3}
\]

So if H-J2-SMOOTH is proved, the coefficient problem is already finished.

---

## 7. Why H-J2-SMOOTH is logically load-bearing

A correct flat derivative alone does not determine a nonlinear continuum
response.

As a hostile logical control, consider adding to some finite response a local
term of schematic form

\[
\Delta E_N(q)
=
\alpha\,
\varepsilon_N^{-4}
(\operatorname{tr}_\eta q)^2
q_{\rm grid}.
\tag{7.1}
\]

For each fixed \(N\),

\[
\Delta E_N(0)=0,
\qquad
D\Delta E_N(0)=0.
\tag{7.2}
\]

It is invisible to every flat linear detector.

But for \(q_N=O(\varepsilon_N^2)\),

\[
\Delta E_N(q_N)=O(1),
\tag{7.3}
\]

so it can survive in the continuum and retain grid data.

This is not proposed as a D0 action term. It is a counterexample to the
inference rule “correct flat derivative implies correct nonlinear J² limit”.

Therefore a uniform higher-order scaling theorem for the **actual** selected
star response is indispensable.

The quarter-wave result identifies a concrete place where a naive proof by
global finite implicit elimination breaks.

---

## 8. Typed T⁴ reconstruction is no longer the first blocker

The older E-FRAME packet located the first failure at missing typed sampling
and response reconstruction.

Current main already contains:

- \`D0.Bridge.T4TypedGeometry\`;
- \`D0.Bridge.T4LocalRoleFrame\`;
- \`D0.Bridge.T4ResponseReconstruction\`.

These provide:

- an actual fixed smooth \(T^4\);
- a Lorentz metric package;
- Role-labelled local frames;
- the radius-two mesh \(\varepsilon_N=(N+2)^{-1}\);
- literal sampling of a smooth metric into finite symmetric Role components;
- reconstruction of a finite symmetric response into
  \(S^2T_x^*T^4\);
- the metric-plus-frame pullback square.

These constructions do not prove frame erasure, but the type-level
reconstruction gap is no longer the earliest failure.

For the present star lane the first missing **dynamical** theorem is
H-J2-SMOOTH.

---

## 9. Frame erasure and local-Diff naturality after H-J2-SMOOTH

If (6.3) holds for every strict normal frame, then two orthonormal normal
frames \(F,F'\) reconstruct the same geometric tensor

\[
-\frac12G[g](x).
\tag{9.1}
\]

Hence

\[
\lim_N
\left(
R_x^{F,\mathrm{resp}}\mathcal E_{\star,N}
-
R_x^{F',\mathrm{resp}}\mathcal E_{\star,N}
\right)
=0.
\tag{9.2}
\]

Frame/grid data erase in the limit.

The existing T4 pullback square then promotes this frame-erased response to
ordinary local-Diff naturality:

\[
E[\phi^*g]=\phi^*E[g].
\tag{9.3}
\]

No new finite Role symmetry needs to be postulated.

The independent E-RAYSEL hostile control remains consistent with this:
a surviving \(E_{\rm sp}\) term would retain a preferred timelike projector and
fail metric-only frame erasure, while #201 already gives its finite flat
coefficient as exactly zero.

---

## 10. Full Lorentz \(J^2\), not a special normal-frame subclass

Normal coordinates remove first derivatives at the center but do not restrict
the metric second derivatives.

The previously audited fixed-T4 realization result shows that every formal
Lorentz metric \(2\)-jet at a point can be realized by a smooth Lorentz metric
on the same \(T^4\), using a bump-supported perturbation while preserving
signature.

Therefore a statement proved for every smooth metric in strict normal
coordinates covers the full Lorentz \(J^2\) fibre.

The use of normal coordinates is a proof device, not a restriction to weak
curvature.

---

## 11. Divergence has two distinct routes

### 11.1 Direct recognition

If H-J2-SMOOTH yields

\[
E[g]=-\frac12G[g],
\tag{11.1}
\]

then the external contracted Bianchi identity immediately gives

\[
\nabla^aE_{ab}=0.
\tag{11.2}
\]

This is a legitimate geometric consequence after the response has been
identified.

### 11.2 Finite Noether to covariant divergence

The star action owns an exact local-Lorentz Noether identity.

The finite linear Einstein stencil also owns an exact centered-divergence
identity.

Neither statement alone proves that a nonlinear star response satisfies

\[
\nabla^aE_{ab}=0
\tag{11.3}
\]

by an internal finite-to-continuum Noether argument.

That route requires a separate divergence/intertwining theorem and remains
OPEN.

It is not required for direct recognition of \(G\), but it would be a stronger
internal derivation.

---

## 12. Navarro/Lovelock audit

External classification used here:

- Alberto Navarro and José Navarro, *Lovelock's theorem revisited*,
  arXiv:1005.2386, J. Geom. Phys. 61 (2011), Theorem 2.6;
- José Navarro, *On second-order, divergence-free tensors*,
  arXiv:1306.4354.

For a fixed pseudo-Riemannian manifold, a symmetric divergence-free
second-order natural metric \((0,2)\)-tensor lies in the Lovelock span.

In dimension four,

\[
E[g]=aG[g]+bg.
\tag{12.1}
\]

Current status:

| Hypothesis | A4D status |
|---|---|
| fixed smooth \(T^4\) | OWNED typed bridge |
| Lorentz signature \((1,3)\) | OWNED typed bridge |
| arbitrary Lorentz metric \(2\)-jets | RESEARCH theorem / bump realization |
| finite metric carrier of selected action | **EXACT: \(Q=\Theta\eta\Theta^T\)** |
| framed sampling/reconstruction | OWNED Lean |
| flat star derivative on metric quotient | **EXACT: \(\frac14E_\eta\)** |
| \(E_{\rm sp}\) coefficient | **EXACT: 0** |
| low-momentum connection regularity | **EXACT: determinant 256 at \(t=1\)** |
| global all-mode connection elimination | **FALSE: diagonal quarter-wave witness** |
| smooth-sampling asymptotic branch | **OPEN: H-J2-SMOOTH** |
| ordinary metric \(J^2\) factorization | conditional on H-J2-SMOOTH |
| frame/grid erasure | conditional; then follows from \(G\)-recognition |
| local-Diff naturality | conditional on factorization + pullback square |
| covariant divergence | external Bianchi after recognition; internal Noether route OPEN |

Thus Navarro/Lovelock itself is not the blocker. The first missing theorem lies
before all of its hypotheses have been reached.

---

## 13. Coefficient map if the surviving bridge closes

Assume H-J2-SMOOTH and the E-NJET Ricci sign convention.

From #201,

\[
D E_\star|_\eta=\frac14E_\eta.
\tag{13.1}
\]

From E-NJET,

\[
E_\eta\longrightarrow -2G.
\tag{13.2}
\]

Therefore the naked star normalization used in #201 has

\[
\boxed{
a=-\frac12.
}
\tag{13.3}
\]

Flat star stationarity gives

\[
E_\star[\eta]=0.
\tag{13.4}
\]

If the limit is in the Lovelock class,

\[
E_\star=aG+bg,
\tag{13.5}
\]

then \(G[\eta]=0\) and \(g=\eta\ne0\), so

\[
\boxed{
b=0
}
\tag{13.6}
\]

for the naked star action.

Thus the conditional nonlinear continuum response is

\[
\boxed{
E_\star[g]=-\frac12G[g].
}
\tag{13.7}
\]

If the entire star action is multiplied by an overall coefficient \(c\),

\[
a=-\frac c2.
\tag{13.8}
\]

In particular \(c=4\) reproduces the \(-2G\) normalization used by E-NJET.

This does not determine Newton's constant in a sourced equation.

---

## 14. Independent zeroth-order \(bg\) channel

The naked star branch has \(b=0\) if the bridge closes, but that does not prove
physical \(\Lambda=0\).

Merged #184 gives

\[
\widehat\Theta'=\widehat\Theta g^{-1}.
\tag{14.1}
\]

For proper Lorentz \(g\), \(\det g=1\), hence

\[
\mathrm{Vol}_{\rm rel}
=
\det\widehat\Theta
\tag{14.2}
\]

is a full-affine scalar.

With

\[
\widehat Q
=
\widehat\Theta\eta\widehat\Theta^T,
\tag{14.3}
\]

and \(\det\eta=-1\),

\[
\det\widehat Q
=
-\det(\widehat\Theta)^2.
\tag{14.4}
\]

On a fixed orientation component,

\[
\boxed{
\mathrm{Vol}_{\rm rel}
=
\pm\sqrt{-\det\widehat Q}.
}
\tag{14.5}
\]

Its first variation is

\[
\boxed{
\delta\mathrm{Vol}_{\rm rel}
=
\frac12\mathrm{Vol}_{\rm rel}
\operatorname{tr}
(\widehat Q^{-1}\delta\widehat Q).
}
\tag{14.6}
\]

Thus the already-owned data contain a full-affine legal, metric-only
zeroth-order channel of precisely the \(bg\) type.

Its coefficient is not selected here.

The derivative and cosmological sectors remain cleanly separated:

\[
S_\star\rightsquigarrow aG,
\qquad
\lambda\mathrm{Vol}_{\rm rel}\rightsquigarrow bg.
\tag{14.7}
\]

No Holst term, \(\varphi\)-coefficient or new tensor datum is required merely
to type the cosmological ray.

---

## 15. Why the UV resonance cannot simply be ignored

The certified diagonal resonance sits at lattice phase \(\pi/2\), hence at
physical momentum of order \(1/\varepsilon_N\) under refinement.

For a fixed \(C^\infty\) continuum metric, Fourier weight at such UV momenta
decays rapidly. This makes a smooth-sector asymptotic bridge plausible.

It does not yet define an exact finite physical response:

- a sampled smooth field need not have exactly zero resonant coefficient;
- the linear connection equation is incompatible for a genuine metric
  direction at the certified mode;
- an arbitrarily small incompatible source is still incompatible;
- a nonlinear repair can be non-smooth and is not supplied by the flat IFT;
- projecting away the mode would be a new finite prescription unless derived.

Therefore the next theorem must explicitly control the resonant sector.

---

## 16. Theorem-ready statements

1. **Nonlinear metric quotient**
   \[
   Q_x=\Theta_x\eta\Theta_x^T.
   \]

2. **Dressed-link metric compatibility**
   \[
   K_{x,r}Q_{x+r}K_{x,r}^T=Q_x.
   \]

3. **Flat Gram differential**
   \[
   DQ_{\rm flat}[H]=H\eta+\eta H^T.
   \]

4. **Exact metric section**
   \[
   H(q)=\frac12q\eta
   \Longrightarrow
   DQ_{\rm flat}[H(q)]=q.
   \]

5. **Interpretation of #201**  
   The #201 Schur response is the flat Hessian of the descended action on the
   tangent space of the genuine nonlinear metric quotient.

6. **Correct polarized diagonal connection determinant**
   \[
   \det H_{AA}^{\rm pol}(t)
   =
   \frac{(t^2+1)^{12}}{16t^{12}}.
   \]

7. **Low-momentum regularity**
   \[
   \det H_{AA}^{\rm pol}(1)=256.
   \]

8. **Exact L=4 diagonal quarter-wave resonance**
   \[
   t=i
   \Longrightarrow
   \rank H_{AA}^{\rm pol}=16.
   \]

9. **Metric-source incompatibility**
   \[
   \rank[(H_{AA}^{\rm pol})^T\mid H_{Aq}]=20.
   \]

10. **Explicit Fredholm witness**
    \[
    H_{AA}^{\rm pol}\lambda=0,
    \qquad
    \lambda^TH_{Aq}(q_{11})=-(1+i).
    \]

11. **No smooth all-mode connection section**  
    No smooth \(K_*(Q)\) through flat solves the finite connection Euler
    equation for every finite metric perturbation on all refinement carriers.

12. **Normal-stencil smallness**
    \[
    q_N=O(\varepsilon_N^2)
    \]
    for every smooth metric in strict normal coordinates.

13. **Conditional Einstein recognition**
    Under H-J2-SMOOTH,
    \[
    E_{\star,N}\to-\frac12G.
    \]

14. **Conditional Lovelock coefficients for naked star**
    \[
    a=-\frac12,\qquad b=0.
    \]

15. **Full-affine metric volume channel**
    \[
    \mathrm{Vol}_{\rm rel}
    =
    \det\widehat\Theta
    =
    \pm\sqrt{-\det\widehat Q}
    \]
    on a fixed orientation component.

16. **Divergence-route separation**  
    Contracted Bianchi after \(G\)-recognition and a finite-Noether to
    Levi-Civita-divergence theorem are distinct statements.

---

## 17. Final disposition and single next task

This task does not support the unconditional terminal

\[
\texttt{STAR-ACTION-NONLINEAR-J2-RESPONSE-ENTERS-EINSTEIN-LOVELOCK-CLASS}.
\]

It does close the following pieces:

- nonlinear metric provenance from the selected finite action;
- the exact tangent weld between that metric and #201;
- pure Einstein flat ray \(c_{\rm sp}=0\);
- low-momentum auxiliary-connection regularity;
- conditional coefficient map \(a=-1/2,\ b=0\);
- a legal independent metric-only zeroth-order volume ray;
- a concrete finite obstruction to naive all-mode elimination.

The exact task terminal is

\[
\boxed{
\texttt{STAR-J2-BRIDGE-BLOCKED-BY-DIAGONAL-QUARTER-WAVE-CONNECTION-RESONANCE}.
}
\tag{17.1}
\]

There is only one surviving upper-wall research task:

\[
\boxed{
\texttt{EXP-A4D-STAR-SMOOTH-SECTOR-CONNECTION-J2-LIMIT}.
}
\tag{17.2}
\]

Its job is to prove or terminally obstruct H-J2-SMOOTH: construct a canonical
smooth-sampling/infrared connection branch and show that the certified UV
resonant sector either has no image on the selected smooth carrier or becomes
asymptotically irrelevant without introducing an arbitrary filter.

If that theorem succeeds, existing #201 + E-NJET + T4 reconstruction already
give the nonlinear Einstein-class result; no further linear coefficient
selector is required.

No result from the curved-root search #202 is used here. No Lean, claim,
release or BOOK promotion is made.
