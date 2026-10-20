# Actual soldered operator: ten heat components and the moving-adjoint boundary

Research result, 2026-10-13. Input SOURCE
`695ecb94abcb38590a8f3e37332969ef21e2f24d`. Original #310 and G0–G4 remain open.

The critical-path correction is substantive: BOOK_03's bootstrap takes a heat
operator and feedback, not an independently prepared Gibbs density. Its
thermal density is a derivative weight. The full preparation-fiber theorems
remain valid for their stated additional physical Gibbs interface, but that
interface is not a prerequisite of the action and leaves the critical path.

This packet differentiates a **literal owned differential operator** on its
homogeneous positive sector. It constructs all ten heat components, proves
that the full gradient responds to every nonzero affine positive-symbol jet, and
gives an exact nonadjoint witness for its variable-solder extension. A missing
identification is kept explicit: no current owner equates the bootstrap's
full heat with this moving operator square. We do not choose that equation as
a new physical law or add an action term.

## 1. Inputs and what they actually supply

| Primary input | Supplied datum | Boundary |
|---|---|---|
| BOOK_03 §03.25; `vp_master_bootstrap_and_volume_derivative.py` | `B=beta^-1 log Tr exp(-beta Delta)-log det(I-zF)`; rank step `V=rank P` | The certificate explicitly supplies heat profiles; it does not define `Delta(P)`. |
| `ArchiveAffineExteriorLink.lean`, `solderLegVector`, `archiveSolderedForwardDifferential`, `archiveSolderedCodifferential` | Moving creators, contractions and actual forward/backward site differences | No general moving-adjoint theorem or bootstrap heat identification. |
| `A4DObserverPositiveExterior.lean`, `observerMetric`, `observerMetric_posDef`, `observerExteriorPairing` | Positive induced exterior pairing for a unit timelike observer | The observer is an independent field; no physical time selection. |
| `A4DRawSolderFrameAction.lean`, `rawSolderMatrix` | Full raw solder `F=eta+e` | No replacement by a centered metric or a frozen differential. |
| `ArchiveHodgeCARDirac.lean` and `ArchiveHodgeCARDiracSquare.lean` | Counting flat Hodge operator, adjoint and scalar square | The flat equality does not select a moving constitutive extension. |
| `A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md` | Full carrier tangent and covector quotient | Kinematic tangency is not an independently derived physical preparation. |

In particular, neither M1 uniqueness nor condensed naturality creates a
joint map that has not been supplied. Equally, one must not turn a separate
physical preparation problem into an assumption of the bootstrap derivative.

## 2. Literal homogeneous square

Let `L=N+2>=2`, with actual four-role periodic sites `(Z/LZ)^4` and all sixteen
exterior/Fock components. Take identity affine links, a constant invertible
real raw solder `F`, and a constant observer `n` with `n^T eta n=1`, where
`eta=diag(1,-1,-1,-1)`. Set

\[
 h=-\eta+2\eta nn^T\eta,
 \quad v_r=\eta F_r^T,
 \quad z_r(k)=L(e^{2\pi i k_r/L}-1).
\]

The definitions in the owner give exactly

\[
 D(k)=\sum_r\{z_r C(v_r)+\bar z_r A(hv_r)\}.                 \tag{1}
\]

The sign of the second term follows from the **minus** backward difference:
`-L(1-exp(-i theta))=conj(z)`. Exterior contraction is the adjoint of creation
for the determinant pairing induced by `h`. Thus (1) is selfadjoint for the
full positive exterior Gram matrix. The CAR relations give, without deleting
any degree,

\[
 D(k)^2=\lambda_Q(k)I_{16},\qquad
 \lambda_Q(k)=z(k)^*Qz(k),\qquad Q=F\eta h\eta F^T>0.       \tag{2}
\]

This is `Q`, not `Q^-1`. The earlier frozen-differential geometric-Hodge
interface has inverse scaling and cannot be identified with (2) merely
because both agree at the flat reference.

There is one zero spatial mode and therefore **sixteen zero modes** on the
whole carrier. Every finite Gibbs density of (2) has top eigenvalue
multiplicity sixteen. It is outside the previous simple-protected-Omega
Gibbs class. This is a precise interface distinction, not a failure of either
construction.

## 3. Full metric tangent and its lift

Write `q=F eta F^T`. To keep the observer normalization explicit for an
arbitrary timelike coordinate vector `v`, put

\[
 s=v^Tq^{-1}v>0,\quad n=F^{-1}v/\sqrt{s},\quad
 Q(q,v)=-q+2vv^T/s.                                       \tag{3}
\]

This follows by substitution into (2); it is not a supplied Hodge binding.
Hold `v` fixed and let `H=delta q` be any symmetric matrix. With `w=q^-1 v`,

\[
 \delta s=-w^THw,\qquad
 T_{q,v}(H):=\delta Q=-H+2vv^T(w^THw)/s^2.                 \tag{4}
\]

At `q=eta,v=e_0`, `T(H)=-H+2H_00 E_00` is an involution on all ten symmetric
coordinates. All ten directions have an actual infinitesimal raw-solder
lift, for example

\[
 \delta F=\tfrac12H F^{-T}\eta,\qquad
 \delta n=-F^{-1}\delta F n-\frac{\delta s}{2s}n.            \tag{5}
\]

Then `delta(F eta F^T)=H` and `delta(n^T eta n)=0`. Smooth local lifts exist
by the nondegenerate symmetric congruence chart. This is a kinematic field
family, with no on-shell equation built into its definition.

For a homogeneous field, the existing carrier equation is satisfied with
coordinate links `D_e=I`: both endpoints have `q`. Its differentiated equation
`D delta q_t D^T+delta D q_t D^T+D q_t delta D^T=delta q_s` holds with
`delta D=0, delta q_t=delta q_s=H`. This proves the claimed constraint
tangency, not admission by an absent full native preparation map.

## 4. Ten components from the full heat trace

Evaluate the existing heat functional on square (2), with fixed `beta>0`:

\[
 B_H(Q)=\beta^{-1}\log\left(16\sum_k e^{-\beta\lambda_Q(k)}\right),
 \quad \pi_k=\frac{e^{-\beta\lambda_Q(k)}}{\sum_j e^{-\beta\lambda_Q(j)}},
 \quad W=\sum_k\pi_k\operatorname{Re}(z_kz_k^*).
\]

No apparatus state is chosen here. The sixteenfold multiplicity remains in
the partition function and cancels in its normalized derivative. Equations
(3)–(4) give the exact intrinsic homogeneous covector

\[
 \boxed{\delta B_H=C:H,\quad
 C=W-\frac{2v^TWv}{s^2}ww^T.}                             \tag{6}
\]

For upper-triangular coordinates `(00,01,02,03,11,12,13,22,23,33)`, the
coefficient is `C_ii` on a diagonal and **`2 C_ij`** off the diagonal. The
certificate checks each slot, its raw-solder lift, and a nontrivial boosted
and nondiagonal symbol; it does not infer the ten slots from a radial check.
The Lean kernel uses diagonal-first order `(00,11,22,33,01,02,03,12,13,23)`;
the explicit permutation from this document is `(0,4,7,9,1,2,3,5,6,8)`.

The independent observer/matter readout must also be varied. For `u=delta v`,

\[
 \delta Q=-H+\frac2s(uv^T+vu^T)
 -\frac{2(2w^Tu-w^THw)}{s^2}vv^T,
 \quad \delta B_H=C:H+J_v^Tu,
 \quad J_v=-\frac4s Wv+\frac{4v^TWv}{s^2}w.                 \tag{6a}
\]

In particular `v^T J_v=0`, as required by invariance under rescaling the
observer representative. At rest the joint derivative has rank ten out of
fourteen coordinates: `delta Q_00=H_00`, `delta Q_0i=-H_0i+2u_i`, and
`delta Q_ij=-H_ij` for spatial `i,j`. Its four-dimensional kernel has
`H_00=H_ij=0`, `H_0i=2u_i`, and free `u_0`. This is the kernel of the
positive-symbol map `(q,v)->Q`, not the kernel of the scalar `delta B_H`.
It is not declared native gauge. At rest the nonzero scalar differential
has a thirteen-dimensional kernel: for instance `H=E_11-E_22,u=0` changes
`Q` but gives `delta B_H=0`. The positive Hessian in Section 6 means that
such a direction still changes the full ten-component gradient.

The entire joint fiber is explicit. For a fixed positive `Q` and any
nonzero `v`, put `r=v^T Q^-1 v` and
`q=-Q+2vv^T/r`. This has Lorentz signature, `v^T q^-1 v=r`, and recovers
the same `Q` in (3). Conversely (3) gives this formula. Thus this heat alone
does not select a timelike ray; the remaining native terms must participate.

For a genuine coupled bootstrap family, its full derivative would be

\[
 \delta B=-\operatorname{Tr}(\rho_\beta(\Delta)\delta\Delta)
       +\operatorname{Tr}\{z(I-z\mathcal F)^{-1}\delta\mathcal F\}.
                                                               \tag{7}
\]

Here `mathcal F` denotes feedback, to distinguish it from the raw solder.
Equation (6) supplies the first term **if this square is the actual heat**.
The same native family must supply the second term, moving pairing and all
source/matter equations. Freezing it without that family does not construct
a solution.

## 5. Exact flat comparison: a visible tracefree response

At `Q=I`, the Gibbs law factors over the four momentum coordinates. Put
`w0=E|z_r|^2>0`. Reflection of a one-dimensional momentum gives
`E z_r=-w0/(2L)`, hence

\[
 W_{rr}=w_0,\quad W_{rs}=w_0^2/(4L^2)\quad(r\ne s).         \tag{8}
\]

The mixed terms of forward differences do not disappear from the finite
thermal derivative. For the entirely exact slice `L=4,beta=log(2)/32`,
`w0=64/3`, and (6) gives

\[
 \operatorname{pack}(C)=
 (-64/3,128/9,128/9,128/9,64/3,128/9,128/9,64/3,128/9,64/3).
                                                               \tag{9}
\]

All ten components of the previously designated geometric
`rho0=-1/2 sqrt(|g|) pack(G^{mu nu})` vanish on the same constant flat metric.
Consequently the heat term (9) alone equals no nonzero fixed calibration of
that comparator. The off-diagonal probe `H=E_01+E_10` is Lorentz-tracefree
and has derivative `128/9`. A pure-volume remainder cannot cancel it there.
This is a finite off-shell comparison. No total native source, failure of
Einstein dynamics, or physical stationary point is inferred.

Radial scaling gives an additional sign control: `F(t)=exp(t)F`, with `n`
fixed, implies `Delta(t)=exp(2t)Delta` and `B_H'(0)=-2 E_beta`.
The previous inverse-scaling Hodge interface gives the opposite sign. They
must remain separate until their actual carrier/readout maps are established.

## 6. No invisible affine positive-symbol direction

Let `f_ii(k)=|z_i|^2` and `f_ij(k)=2 Re(z_i conj(z_j))` for `i<j`.
For affine `Q` coordinates,

\[
 \nabla_Q^2 B_H=\beta\operatorname{Cov}_{\pi}(f)>0.           \tag{10}
\]

Proof for every `L>=2`: put `t=L(exp(2 pi i/L)-1)`, which is nonzero. Mode
zero gives feature zero; four unit modes give `|t|^2` times the four diagonal
basis vectors. Each of the six pair modes, after subtracting its two unit
features, gives `2|t|^2` times its off-diagonal basis vector. These eleven
modes affinely span all ten coordinates. All finite Gibbs weights are
strictly positive. A variance can vanish only for a linear functional
constant on every mode; the eleven witnesses force that functional to zero.

Thus the affine heat response is locally invertible and globally injective
on the convex positive cone, by strict monotonicity of the gradient. This is
an operator-coordinate response theorem, not a selected physical geometry.
It does **not** establish convexity in nonlinear Lorentz coordinates `q`:
their Hessian also contains `-W:delta^2 Q`. For a rest `H_01` variation,
`delta^2 Q_00=4`; this term is nonzero. The certificate rejects omission of it.

## 7. Moving-adjoint boundary and the forced algebraic repair

Now let one raw leg vary over sites while keeping flat internal links and
the constant rest observer. On one axis, write its scalar coefficient as
`ell_x`, shift `S`, and `M=diag(ell)`. The actual definitions restrict to

\[
 d=L M(S-I),\quad
 \delta_{owned}=-L M(I-S^T),\quad
 d^*=-L(I-S^T)M.                                          \tag{11}
\]

Their exact difference is

\[
 \delta_{owned}-d^*=L(MS^T-S^TM),
 \quad ((\delta_{owned}-d^*)u)_x
   =L(\ell_x-\ell_{x-1})u_{x-1}.                          \tag{12}
\]

At `L=2,ell=(3/2,1/2)`, both stored blocks equal
`[[-3,3],[1,-1]]`, which is not symmetric. The vacuum/one-form block of
`D_owned` is therefore not selfadjoint in the owned counting observer
pairing. The full sixteen-degree operator contains this invariant witness;
the other three spatial directions can be kept constant. The same defect is
checked independently at `L=4`.

This witness can satisfy the geometric carrier equation: with sitewise
invertible `F_x`, put coordinate link `D_xy=F_x F_y^-1` and
`q_x=F_x eta F_x^T`. Then `D_xy q_y D_xy^T=q_x` exactly. Carrier tangency
alone does not fix the moving codifferential. The internal affine links in
(11) are still identity; they are not the coordinate matrices `D_xy`.

For an actually supplied positive full pairing matrix `G`, the unique
adjoint is forced algebraically:

\[
 d^{\dagger_G}=G^{-1}d^*G,\qquad
 \delta_{required}-\delta_{owned}
      =G^{-1}d^*G-\delta_{owned}.                          \tag{13}
\]

This identifies the missing terms; it does not silently change a supported
definition. Other moving pairings might alter the witness, so (12) is a
boundary for the stated counting/rest pairing, not every native pairing.
To continue to curved fields, the actual preparation must supply its pairing
and identify (13), or prove a constraint making the difference vanish.

## 8. What is now the shortest necessary arrow

The requested joint object is
`X_native -> (Delta(X), P(X), U(X), G(X))`, not an arbitrary full Gibbs state
followed by defining a heat from it. The concrete next comparison is between
the **same full-carrier** native heat and the owned soldered differential,
including its moving-adjoint terms. The scene already binds its feedback to
`2 Delta_c-Delta_c^2` on a 33-dimensional coarse space; it does not identify
that coarse operator with heat on all 718 histories or on this role carrier.

If that binding is derived, (6) gives an immediate ten-component test and
(12)–(13) give the required curved correction. If another binding is derived,
its actual derivative must be used. Physical admission, full source/Ward,
quantitative transfer, native stationarity, curved joint roots and
soundness/recovery all remain explicit. No new selector, physical postulate,
or action has been installed.

## 9. Reproduction and proof status

Run `python3 02_REGISTRY/research/certificates/a4d_native_soldered_heat_source_check.py`.
Its immutable JSON ledger pins this proof, the implementation, checker,
primary owners and the narrow Lean receipt. All matrix/CAR/Gram/metric jets,
thermal slices, feature ranks and negative controls are exact. No floating
point evidence is used for a proof. The all-L Fourier and covariance argument
is the analytic proof above; replay at L=2,4 is an additional check.

The research Lean capsule proves its listed finite matrix/constraint kernels
and resolves the named owners with their actual propositions and axioms. It
does not claim to formalize the full analytic heat derivative, all-L Fourier
transform, bootstrap binding, or GR. Supported CORE and public claims are
unchanged.

The actual narrow compile checks twenty new propositions and six owner
closures, all with standard axioms. Its receipt separately fingerprints fifty
transitive D0 SOURCE files and the consumed compiled imports. Forty-one cache
source files match. The nine modules whose sources were absent in that cache
checkout were freshly compiled from SOURCE in dependency order in an
isolated overlay. The capsule was then successfully recompiled against that
overlay; actual import selection, commands and binary hashes are recorded.
The original cache was not modified. The printed imported definitions match
the reviewed operator formulas. A fresh rebuild of all fifty SOURCE imports,
or `D0.All`, is not claimed.
