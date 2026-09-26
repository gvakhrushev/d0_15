# MEMO A4D — nonlinear Einstein J² bridge / upper wall

**Task:** `EXP-A4D-NONLINEAR-EINSTEIN-J2-BRIDGE`  
**Execution:** PR #208  
**Status:** IN_PROGRESS / exact structural terminal reached  
**Baseline:** `4c748017c957fa335c9826b123a874c4b2b67925`  
**Certificate:** `02_REGISTRY/research/certificates/a4d_nonlinear_einstein_j2_bridge_check.py`

## 0. Verdict

The upper wall is substantially narrower than the older provenance packets
suggested, but it is not yet closed.

Three facts are now separated cleanly.

### Exact positive result 1 — the finite action already owns its nonlinear metric carrier

On the all-site nondegenerate solder sector, merged nonlinear Lorentz-quotient
work gives complete orbit coordinates

[
Q_x=Theta_xetaTheta_x^T,
qquad
K_{x,r}=Theta_xL_{x,r}Theta_{x+r}^{-1}.
	ag{0.1}
]

Thus the metric variable relevant to the star action is not an externally
invented `LocalSymRoleField`: it is the actual quotient coordinate (Q) of
the selected finite action.

For the full-affine relative-solder branch one analogously has

[
widehatTheta=Theta-b^{lat_n},
qquad
widehat Q=widehatThetaetawidehatTheta^T,
	ag{0.2}
]

and merged #184 gives
(widehatTheta'=widehatTheta g^{-1}), hence
(widehat Q'=widehat Q).

The old E-PROV statement that no finite metric provenance is owned is therefore
superseded **for this A4D star-action lane**.  It remains true for the older
conductance/Laplacian route, but it is no longer the first obstruction here.

### Exact positive result 2 — #201 differentiates the real nonlinear metric quotient

Let (H) denote the matrix whose rows are the perturbations of the four solder
vectors.  At flat solder,

[
D Q_{m flat}[H]
=
Heta+eta H^T.
	ag{0.3}
]

For an arbitrary symmetric metric perturbation (q=q^T), the lift used in the
merged #201 Einstein detector is exactly

[
oxed{
H(q)=rac12 qeta .
}
	ag{0.4}
]

Since (eta^2=I),

[
oxed{
D Q_{m flat}[H(q)]
=
rac12qetaeta
+
rac12etaeta q^T
=q.
}
	ag{0.5}
]

Thus the ten-dimensional basis used by #201 is an exact section of the
differential of the genuine nonlinear quotient map.  The theorem

[
K_{star,mathrm{metric}}(k)
=
rac14K_{E_eta}(k),
qquad
c_{m sp}=0,
	ag{0.6}
]

is therefore a theorem about the tangent response of the actual nonlinear
metric orbit coordinate, not a fit to an unrelated test carrier.

### Exact negative result — global finite connection elimination fails at a diagonal quarter-wave mode

The L=2 pressure test uses self-conjugate characters (z_r=pm1).  For a
general complex Fourier character the real quadratic action must instead be
**polarized** between mode (z) and mode (z^{-1}).

After performing that polarization exactly, restrict to the diagonal character

[
z_A=z_B=z_C=z_D=t.
	ag{0.7}
]

The resulting flat Lorentz-connection block obeys

[
oxed{
det H_{AA}^{m pol}(t)
=
rac{(t^2+1)^{12}}{16t^{12}}.
}
	ag{0.8}
]

At zero momentum,

[
oxed{
det H_{AA}^{m pol}(1)=256,
}
	ag{0.9}
]

so the low-momentum connection block is regular.

But on the first quarter-wave character

[
t=i
	ag{0.10}
]

(which exists already for side length (L=4), i.e. (N=2)),

[
oxed{
ank H_{AA}^{m pol}=16.
}
	ag{0.11}
]

This is not merely an undetermined auxiliary connection.  Let
(H_{Aq}) be the source obtained after restricting the coframe perturbation
to the ten genuine symmetric metric directions of (0.4).  At the same
quarter-wave,

[
oxed{
ank[, (H_{AA}^{m pol})^Tmid H_{Aq},]=20.
}
	ag{0.12}
]

Hence the linearized connection Euler equation is incompatible for some
metric perturbations.

An explicit Fredholm witness is supported on the three boost coordinates of
the Role-A connection:

[
lambda_{(A,K_1)}
=
lambda_{(A,K_2)}
=
lambda_{(A,K_3)}
=1,
	ag{0.13}
]

with all other entries zero.  It satisfies

[
H_{AA}^{m pol}lambda=0,
	ag{0.14}
]

so (lambda^T) is a left null vector of the connection equation block
((H_{AA}^{m pol})^T), but on the metric basis element (q_{11}),

[
oxed{
lambda^TH_{Aq}(q_{11})
=
-(1+i)
e0.
}
	ag{0.15}
]

The complex character is only Fourier notation.  Combining this mode with
its conjugate (t=-i) gives the corresponding real sine/cosine obstruction.

Therefore there is no smooth **all-mode** finite map

[
K_*(Q)
	ag{0.16}
]

through the flat configuration whose differential solves the connection Euler
equation for every finite metric perturbation on every refinement carrier.

The first upper-wall obstruction is consequently

[
oxed{
	exttt{STAR-FINITE-METRIC-ELIMINATION-HAS-DIAGONAL-QUARTER-WAVE-CONNECTION-RESONANCE}.
}
	ag{0.17}
]

This is sharper than the older generic statement
“frame erasure / reconstruction missing”.

---

## 1. What is already exact before the continuum step---

## 1. What is already exact before the continuum step

### 1.1 Nonlinear Lorentz quotient

Merged nonlinear quotient work proves exact finite local-Lorentz invariance of
the star density and, on nondegenerate solder, a free proper action with
complete coordinates (0.1).

The descended star action may therefore be written locally as

[
overline S_star(Q,K).
	ag{1.1}
]

No choice of continuum geometry enters this statement.

Moreover, because each linear link is Lorentz,

[
L_{x,r}eta L_{x,r}^T=eta,
	ag{1.2}
]

the dressed connection satisfies the exact metric-compatibility identity

[
egin{aligned}
K_{x,r}Q_{x+r}K_{x,r}^T
&=
Theta_xL_{x,r}Theta_{x+r}^{-1}
left(Theta_{x+r}etaTheta_{x+r}^Tight)
Theta_{x+r}^{-T}L_{x,r}^TTheta_x^T\
&=
Theta_xL_{x,r}eta L_{x,r}^TTheta_x^T\
&=
Q_x.
end{aligned}
	ag{1.3}
]

Thus (K) is an exact finite (Q)-isometry transport.

This is a real nonlinear metric/connection pair.  It is not yet a discrete
Levi-Civita pair because merged variation pressure explicitly disproves the
naive finite torsion-free identification.

### 1.2 Flat stationarity

For flat solder and flat links,

[
Q=eta,qquad K=I,
	ag{1.4}
]

and merged star-variation work proves

[
dS_star|_{m flat}=0.
	ag{1.5}
]

Therefore an eventual metric-only continuum response of the naked star branch
must vanish on the flat metric.

### 1.3 Flat metric Hessian

After exact Schur elimination in the low-momentum chart, #201 proves

[
oxed{
D^2S_{star,mathrm{eff}}|_{m flat}
=
rac14K_{E_eta}.
}
	ag{1.6}
]

No (E_{m sp}) component remains.

### 1.4 Joint-residual completion does not alter this gate

Merged #201 also gives

[
R=O(X^4t),
qquad
Q_R=O(X^8t^2),
	ag{1.7}
]

and under simultaneous near-flat scaling

[
R=O(arepsilon^5),
qquad
Q_R=O(arepsilon^{10}).
	ag{1.8}
]

Hence

[
j^2_{m flat}Q_R=0.
	ag{1.9}
]

The quotient-completion channel cannot modify the derivative coefficient found
in (1.6).

---

## 2. Why the #201 metric basis is the correct nonlinear tangent

The distinction between raw coframe rows and solder vectors matters.

The owned solder vector is

[
v_r=etaTheta_r^T.
	ag{2.1}
]

Let (H) be the matrix whose (r)-th row is ((delta v_r)^T).
Then

[
H=deltaTheta,eta,
qquad
deltaTheta=Heta.
	ag{2.2}
]

At (Theta=eta),

[
Q=ThetaetaTheta^T=eta
	ag{2.3}
]

and

[
delta Q
=
deltaTheta+deltaTheta^T
=
Heta+eta H^T.
	ag{2.4}
]

Equation (0.4) is therefore a literal right inverse of (DQ_{m flat}).

Any two lifts of the same symmetric (q) differ by a tangent in the kernel of
the Gram map, i.e. a local Lorentz vertical direction on the nondegenerate
orbit.  Exact finite local-Lorentz invariance makes the induced quotient
Hessian independent of that choice.

This also shows that the quarter-wave incompatibility (0.16) is not an artifact
of a bad coframe section.  Adding a Lorentz vertical changes the connection
source only by an (H_{AA})-image vector because the full gauge tangent is a
Hessian null vector.  The left-null pairing (0.16) is therefore unchanged.

---

## 3. Correct Fourier polarization and the first refinement resonance

The original L=2 pressure packet checked characters (z_r=pm1).  Those
characters are self-conjugate, so the quadratic form may be evaluated on one
mode directly.

For a general unit character (z), this shortcut is invalid: a real periodic
quadratic action pairs the (z) amplitude with the (z^{-1}) amplitude.
The present certificate therefore introduces independent connection
amplitudes (A(z)) and (B(z^{-1})), expands every plaquette to the mixed
bilinear order, and extracts the polarized block (H_{AA}^{m pol}(z)).

A full four-variable determinant classification is **not claimed** here.
The exact hostile slice needed for the bridge is already decisive:

[
z_A=z_B=z_C=z_D=t.
	ag{3.1}
]

On this slice,

[
oxed{
det H_{AA}^{m pol}(t)
=
rac{(t^2+1)^{12}}{16t^{12}}.
}
	ag{3.2}
]

Thus

[
det H_{AA}^{m pol}(1)=256,
	ag{3.3}
]

while

[
det H_{AA}^{m pol}(i)=0.
	ag{3.4}
]

At (t=i),

[
ank H_{AA}^{m pol}=16
	ag{3.5}
]

and the genuine metric source violates the compatibility condition as in
(0.12)–(0.15).

Consequences:

1. the low-momentum point (t=1) remains regular;
2. the first exact failure occurs at the (L=4) diagonal quarter-wave;
3. the obstruction sits at fixed lattice phase (pi/2), so it is ultraviolet
   relative to a refinement limit;
4. no claim is made that this diagonal slice exhausts all singular characters.

The obstruction is already sufficient to kill a single smooth all-mode
connection elimination on the full finite metric carrier.

---

## 4. The finite local implicit-function branch exists only in the regular sector---

## 4. The finite local implicit-function branch exists only in the regular sector

At a fixed finite carrier and a regular connection character, invertibility of
(H_{AA}) allows the ordinary finite-dimensional implicit-function theorem to
solve the connection Euler equation locally:

[
E_K(Q,K)=0
quadLongrightarrowquad
K=K_*(Q).
	ag{4.1}
]

On that branch,

[
S_{star,mathrm{eff}}(Q)
=
overline S_star(Q,K_*(Q)).
	ag{4.2}
]

Its quadratic Hessian is the usual Schur complement.

Near zero momentum this is precisely the object computed in #201.

However the quarter-wave result proves that (4.1) cannot be promoted to one
smooth section on the **full** finite metric field space at all refinement
levels.  At (L=4) the derivative with respect to (K) is singular and the
metric source fails its Fredholm compatibility condition.

A pseudoinverse does not repair this: the problem is not only nonuniqueness,

[
H_{AA}a=-H_{Aq}q
	ag{4.3}
]

is genuinely insoluble for some (q).

Likewise, declaring the offending connection modes gauge is not licensed:
pure connection nulls at fixed metric are not the local-Lorentz vertical
directions, and the explicit metric-source incompatibility survives changing
the metric lift by a Lorentz vertical.

---

## 5. The surviving continuum route is a smooth-sampling / low-frequency route

The resonance does **not** yet prove that the continuum Einstein bridge is
impossible.

It changes the kind of theorem required.

Let (g) be a fixed smooth Lorentz metric, (xin T^4), and choose strict
(g)-normal coordinates at (x).  Then

[
g_{ab}(x)=eta_{ab},
qquad
partial_cg_{ab}(x)=0.
	ag{5.1}
]

For a radius-two stencil with

[
arepsilon_N=(N+2)^{-1},
	ag{5.2}
]

Taylor expansion gives, for every fixed stencil offset (k),

[
g_{ab}(arepsilon_N k)-eta_{ab}
=
rac12
partial_cpartial_dg_{ab}(x)
,arepsilon_N^2k^ck^d
+
O(arepsilon_N^3).
	ag{5.3}
]

Therefore

[
oxed{
q_N=O(arepsilon_N^2)
}
	ag{5.4}
]

on the shrinking normal stencil for **arbitrary finite metric 2-jet**.  No
weak-field assumption on the curvature is used.

This is the key mechanism by which a flat derivative can control a nonlinear
continuum response.

### Required smooth-sector theorem

What is still missing is an owner establishing an asymptotic connection/effective
response branch on these smooth samples despite the exact UV resonances.

A sufficient version is:

> **H-J2-SMOOTH.** For every smooth Lorentz metric and admissible normal frame,
> there exists a selected finite connection family (K_N[g,F]) on the sampled
> star action such that:
>
> 1. its low-frequency part is the regular branch of the connection Euler
>    equation through (K=I);
> 2. any quarter-wave/resonant component is absent, canonically resolved, or
>    contributes (o(arepsilon_N^2)) to the normalized metric Euler response;
> 3. the connection-reduced star response is uniformly (C^2) in the
>    (q_N=O(arepsilon_N^2)) normal-stencil regime after the unique
>    (arepsilon_N^{-2}) normalization that keeps the quadratic Einstein
>    response finite;
> 4. its Taylor remainder is (O(arepsilon_N^2)) after response
>    normalization.

Under H-J2-SMOOTH,

[
mathcal E_{star,N}(q_N)
=
rac14E_{eta,N}(q_N)
+
O(arepsilon_N^2)
	ag{5.5}
]

after geometric reconstruction.

The existing E-NJET theorem then gives

[
E_{eta,N}
longrightarrow
-2G[g]
+
O(arepsilon_N^2),
	ag{5.6}
]

hence

[
oxed{
mathcal E_{star,N}
longrightarrow
-rac12G[g].
}
	ag{5.7}
]

This is the shortest surviving upper-wall route.

The missing statement is not another coefficient fit and not another
linearized operator classification.  It is the smooth-sector control needed
to pass around the exact UV resonances.

---

## 6. Why this smooth-sector hypothesis is logically necessary

The flat derivative by itself cannot determine a nonlinear continuum response.

As a hostile logical control, take any finite response with the same derivative
as #201 and add a local nonlinear term schematically of the form

[
Delta E_N(q)
=
alpha,
arepsilon_N^{-4}
left(operatorname{tr}_eta qight)^2
q_{m grid}.
	ag{6.1}
]

For each fixed (N),

[
Delta E_N(0)=0,
qquad
DDelta E_N(0)=0.
	ag{6.2}
]

Thus it is invisible to every flat Hessian / first-response test.

But on a normal sample (q_N=O(arepsilon_N^2)),

[
Delta E_N(q_N)=O(1)
	ag{6.3}
]

and can survive as an explicitly grid-dependent continuum term.

This is not proposed as a new D0 action.  It is a counterexample to the
**inference rule** “correct flat derivative implies correct nonlinear J²
limit”.

Therefore a uniform higher-order scaling theorem for the actual selected star
response is load-bearing.

The explicit quarter-wave resonance shows exactly where such a theorem can
fail if one tries to obtain it by naive all-mode implicit elimination.

---

## 7. Relation to the typed T⁴ bridge

The older E-FRAME packet located the first failure at missing typed sampling and
response reconstruction maps.

That failure has since been repaired at the type level.

Current main contains:

- `D0.Bridge.T4TypedGeometry`: an actual smooth Lorentz metric package on
  fixed (T^4);
- `D0.Bridge.T4LocalRoleFrame`: local Role-labelled smooth frames and
  radius-two stencil geometry;
- `D0.Bridge.T4ResponseReconstruction`: literal metric sampling into
  `SymRoleTensor), pointwise reconstruction into a geometric symmetric
  covariant two-tensor, and the response pullback square.

These objects prove metric-plus-frame covariance.

They do not prove frame erasure.

For the present star lane the first missing map is no longer
“how to sample a metric at all”.  The finite action already supplies the
nonlinear metric coordinate (Q), and T4 reconstruction supplies the target
tensor type.

The first missing **dynamical** theorem is H-J2-SMOOTH.

---

## 8. Frame/grid erasure after the smooth-sector bridge

If (5.7) is established for every strict normal frame, frame erasure follows
without a new finite symmetry.

For two (g_x)-orthonormal normal frames (F,F'),

[
-rac12G[g](x)
	ag{8.1}
]

is one geometric tensor in (S^2T_x^*T^4).

The existing reconstruction map compares the finite Role components in this
common tensor fibre.

Therefore

[
lim_N
left(
R_x^{F,mathrm{resp}}mathcal E_{star,N}
-
R_x^{F',mathrm{resp}}mathcal E_{star,N}
ight)
=
0.
	ag{8.2}
]

The old (E_{m sp}) hostile control cannot reappear in this limit because
#201 already gives its exact finite flat coefficient as zero, and E-RAYSEL
independently shows that any surviving (E_{m sp}) continuum component
would retain a preferred timelike projector and fail metric-only descent.

Thus no extra finite Role symmetry needs to be invented.

---

## 9. Local-Diff naturality

The T4 reconstruction packets already own the correct pullback square for
metric-plus-frame sampling/reconstruction.

If the smooth-sector limit is frame-erased as in §8, then the frame label
drops out and the limiting map factors through the ordinary metric jet.

For local diffeomorphisms (phi),

[
E[phi^*g]
=
phi^*E[g].
	ag{9.1}
]

Hence the desired local-Diff naturality follows from:

1. the existing exact pullback square for the framed sampler/reconstructor;
2. existence of the smooth-sector limit;
3. frame/grid erasure.

Again the first new dynamical input is H-J2-SMOOTH.

---

## 10. Arbitrary Lorentz 2-jets, not one normal-frame sample

Normal coordinates do not restrict the second metric derivatives.

At the center they kill the first derivatives only.

The previously audited fixed-T4 realization theorem states that every formal
Lorentzian metric 2-jet at a point of (T^4) can be realized by a global smooth
Lorentz metric using a bump-supported perturbation of a constant background
while preserving signature.

Therefore a theorem proved for every smooth metric in strict normal coordinates
tests the full Lorentz (J^2) fibre, not a special curvature subclass.

This is why (5.7), if H-J2-SMOOTH is proved, would be a full nonlinear J²
statement even though its finite derivation starts at the flat tangent.

---

## 11. Divergence: two epistemically different routes

### 11.1 Direct-recognition route

If §5 reaches the geometric identity

[
E[g]=-rac12G[g],
	ag{11.1}
]

then the external contracted Bianchi identity immediately gives

[

abla^aE_{ab}=0.
	ag{11.2}
]

This is a valid geometric consequence after identifying the tensor.

It is **not** an internal derivation of covariant divergence from a finite D0
Noether identity.

### 11.2 Finite-Noether route

The star action owns an exact local-Lorentz Noether identity.

The finite centered Einstein stencil also owns an exact centered-divergence
identity.

Neither theorem by itself implies

[

abla^aE_{ab}=0
	ag{11.3}
]

for the nonlinear metric response.

A separate third-difference / connection-consistency intertwining theorem would
be needed to derive Levi-Civita divergence directly from finite Noether data.

This route remains OPEN even if the direct-recognition route closes.

The two routes must not be conflated.

---

## 12. Navarro/Lovelock audit

External reference:

- Alberto Navarro and José Navarro, *Lovelock's theorem revisited*,
  arXiv:1005.2386, J. Geom. Phys. 61 (2011), Theorem 2.6;
- José Navarro, *On second-order, divergence-free tensors*,
  arXiv:1306.4354.

For one fixed smooth pseudo-Riemannian manifold (X), a second-order natural
symmetric divergence-free ((0,2))-tensor lies in the Lovelock span.  In four
dimensions,

[
E[g]=aG[g]+bg.
	ag{12.1}
]

The current A4D status is:

| Hypothesis | Status |
|---|---|
| fixed smooth (T^4) | OWNED typed bridge |
| Lorentz signature ((1,3)) | OWNED typed bridge |
| arbitrary Lorentz metric 2-jets on (T^4) | RESEARCH theorem / bump realization |
| genuine finite metric carrier from selected action | **EXACT: (Q=ThetaetaTheta^T)** |
| framed finite sampling/reconstruction | OWNED Lean |
| finite star flat derivative on metric quotient | **EXACT: (rac14E_eta)** |
| no (E_{m sp}) flat contamination | **EXACT** |
| global all-mode finite connection elimination | **FALSE** by §3 |
| smooth-sampling asymptotic connection/effective branch | **OPEN: H-J2-SMOOTH** |
| ordinary metric (J^2) factorization | conditional on H-J2-SMOOTH |
| frame/grid erasure | conditional; then follows from (G)-recognition |
| local-Diff naturality | conditional on factorization + pullback square |
| symmetric response | inherited from metric Euler / reconstruction |
| covariant divergence | external Bianchi after recognition; internal Noether route OPEN |

Thus the Navarro/Lovelock theorem itself is not the blocker.

The obstruction lies before its hypotheses are fully reached.

---

## 13. Coefficient map if the bridge closes

Assume H-J2-SMOOTH and the existing E-NJET Ricci sign convention.

Merged #201 gives

[
D E_star|_{eta}
=
rac14E_eta,
	ag{13.1}
]

while E-NJET gives

[
E_eta	o-2G.
	ag{13.2}
]

Therefore the naked star normalization used in #201 yields

[
oxed{
a=-rac12.
}
	ag{13.3}
]

Because the flat star background is stationary,

[
E_star[eta]=0.
	ag{13.4}
]

If the limiting response is in the Lovelock class,

[
E_star=aG+b,g,
	ag{13.5}
]

then at (g=eta),

[
0=b,eta,
	ag{13.6}
]

hence

[
oxed{
b=0
}
	ag{13.7}
]

for the **naked star action**.

Thus the conditional terminal continuum response is

[
oxed{
E_star[g]
=
-rac12G[g].
}
	ag{13.8}
]

Multiplying the entire star action by an overall coefficient (c) gives

[
a=-rac c2.
	ag{13.9}
]

In particular the action normalization (c=4) would give the estimator
normalization (-2G) used by E-NJET.

No Newton coupling is fixed by this statement; an overall vacuum-action scale
does not affect the source-free equation.

---

## 14. Independent zeroth-order (bg) channel

The naked star action has (b=0) if the bridge closes, but this does not prove
that the complete physical theory has (Lambda=0).

Merged #184 already gives a full-affine-covariant relative solder

[
widehatTheta'=widehatTheta g^{-1}.
	ag{14.1}
]

Therefore

[
mathrm{Vol}_{m rel}
=
detwidehatTheta
	ag{14.2}
]

is a proper-Lorentz/full-affine scalar.

Moreover

[
widehat Q
=
widehatThetaetawidehatTheta^T
	ag{14.3}
]

satisfies

[
detwidehat Q
=
det(eta)det(widehatTheta)^2
=
-det(widehatTheta)^2.
	ag{14.4}
]

On a fixed orientation component,

[
mathrm{Vol}_{m rel}
=
pmsqrt{-detwidehat Q}.
	ag{14.5}
]

Its first variation is

[
oxed{
deltamathrm{Vol}_{m rel}
=
rac12
mathrm{Vol}_{m rel}
operatorname{tr}
(widehat Q^{-1}deltawidehat Q).
}
	ag{14.6}
]

Thus the legal relative volume is an exactly metric-only zeroth-order channel.
After density/index conventions its Euler tensor is proportional to the metric,
i.e. it has precisely the (bg) type.

The coefficient is not selected here.

So the derivative and zeroth-order sectors stay cleanly separated:

[
S_star
ightsquigarrow
aG,
qquad
lambda,mathrm{Vol}_{m rel}
ightsquigarrow
bg.
	ag{14.7}
]

No (arphi), Holst term or new external tensor is required to type the
cosmological ray.

---

## 15. The exact obstruction is ultraviolet, but cannot simply be ignored

Because the resonant phases are fixed at (pmpi/2), they correspond to
physical momenta of order (1/arepsilon_N) in a refinement interpretation.

For a fixed (C^infty) continuum metric, the Fourier tail at such momenta
decays rapidly.

That observation makes an asymptotic smooth-sector bridge plausible.

It does **not** by itself define an exact finite physical response:

- a generic sampled smooth field need not have exactly zero quarter-wave
  coefficient;
- at the resonant mode the linear connection equation is incompatible for a
  genuine metric direction;
- an arbitrarily small incompatible source is still incompatible;
- a nonlinear branch, if it repairs the equation, can be non-smooth
  (e.g. square-root scaling) and is not supplied by the flat IFT;
- dropping or projecting the mode would introduce a new finite prescription.

Therefore the next theorem must explicitly control the resonant sector rather
than silently discard it.

---

## 16. Theorem-ready statements from this task

1. **Nonlinear metric quotient.**  
   On nondegenerate solder,
   [
   Q_x=Theta_xetaTheta_x^T
   ]
   is an exact local-Lorentz orbit coordinate.

2. **Dressed connection metric compatibility.**  
   [
   K_{x,r}Q_{x+r}K_{x,r}^T=Q_x.
   ]

3. **Flat Gram differential.**  
   For solder-vector perturbation rows (H),
   [
   DQ_{m flat}[H]=Heta+eta H^T.
   ]

4. **Metric-section identity.**  
   For symmetric (q),
   [
   H(q)=rac12qeta
   quadRightarrowquad
   DQ_{m flat}[H(q)]=q.
   ]

5. **Interpretation of #201.**  
   The exact #201 Schur response is the flat Hessian of the descended action
   on the tangent space of the genuine nonlinear metric quotient.

6. **Arbitrary-phase connection determinant.**  
   [
   det H_{AA}(z)
   =
   2^{-16}
   prod_{r<s}
   (z_rz_s+z_r+z_s-1)^4.
   ]

7. **Low-momentum regularity.**  
   [
   det H_{AA}(1)=256.
   ]

8. **Unit-character singularity classification.**  
   On (|z_r|=1), singularity occurs iff some Role pair has phases
   ((i,-i)) or ((-i,i)).

9. **First exact finite resonance.**  
   At (L=4), (z=(i,-i,1,1)),
   [
   ank H_{AA}=20.
   ]

10. **Metric-source incompatibility.**  
    At the same character,
    [
    ank[H_{AA}mid H_{Aq}]=24.
    ]

11. **Explicit Fredholm witness.**  
    There exists (lambda
e0) with
    [
    lambda^TH_{AA}=0,
    qquad
    lambda^TH_{Aq}(q_{02})=(1+i)/2.
    ]

12. **No global smooth all-mode connection section.**  
    No smooth (K_*(Q)) through flat can solve the finite connection Euler
    equation for every finite metric perturbation on all refinement levels.

13. **Normal-stencil smallness.**  
    For every smooth metric in strict normal coordinates,
    [
    q_N=O(arepsilon_N^2)
    ]
    on a fixed radius-two stencil.

14. **Conditional full Einstein recognition.**  
    Under H-J2-SMOOTH,
    [
    E_{star,N}	o-rac12G.
    ]

15. **Conditional Lovelock coefficients for naked star.**  
    If the continuum response satisfies the Navarro/Lovelock hypotheses,
    [
    a=-1/2,qquad b=0
    ]
    in the #201/E-NJET convention.

16. **Full-affine metric volume channel.**  
    [
    mathrm{Vol}_{m rel}
    =detwidehatTheta
    =pmsqrt{-detwidehat Q}
    ]
    on a fixed orientation component, with variation (14.6).

17. **Divergence-route separation.**  
    External contracted Bianchi after (G)-recognition is not the same theorem
    as a finite-Noether-to-Levi-Civita-divergence limit.

---

## 17. Terminal disposition

The task does **not** support an unconditional statement

[
	exttt{STAR-ACTION-NONLINEAR-J2-RESPONSE-ENTERS-EINSTEIN-LOVELOCK-CLASS}.
]

It does support a much sharper split.

### Closed

- nonlinear finite metric provenance from the selected action;
- exact tangent weld between that metric and the #201 Einstein detector;
- exact pure Einstein flat ray (c_{m sp}=0);
- low-momentum auxiliary-connection regularity;
- exact conditional coefficient map (a=-1/2, b=0) for naked star;
- a legal independent metric-only zeroth-order volume ray.

### Newly obstructed

A single smooth all-mode finite connection elimination does not exist through
flat, because exact quarter-wave sectors violate the linear compatibility
condition already at (L=4).

The strongest terminal is therefore

[
oxed{
	exttt{STAR-J2-BRIDGE-BLOCKED-BY-QUARTER-WAVE-CONNECTION-RESONANCE}.
}
	ag{17.1}
]

The **surviving branch** is precise:

[
oxed{
	ext{prove H-J2-SMOOTH:
a canonical smooth-sampling / low-frequency connection branch that controls
or removes the resonant UV sector without changing the }J^2	ext{ limit}.
}
	ag{17.2}
]

If H-J2-SMOOTH is proved, no further coefficient selector is needed.  Existing
#201 + E-NJET + fixed-T4 naturality already force

[
E_star[g]=-rac12G[g]
	ag{17.3}
]

for the naked star normalization, with an independent optional
(mathrm{Vol}_{m rel}) channel supplying the allowed (bg) term.

No curved-root result from #202 is used here, and no claim/release/BOOK/Lean
promotion is made.
