# Fixed-source amplitude escape on the cosine warp

Repository: `gvakhrushev/d0_15`
Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`
Working PR: #310, Draft / IN_PROGRESS.
Input owner snapshot: `c55a78aa1dcd6aae0641084e20e29d2d9fb4cb3d`.
Status: analytic corollary of the two pinned owners below; no Lean or parent-task promotion.

## Publication provenance

This text was reconstructed on 2026-10-06 after the previous execution's local worktree and unpublished commits were unavailable. It is not a publication of the unavailable local commit `5026a87a`, and does not reuse that execution's validation claims. The argument below was checked again against the published input owners. The separate 96-variable Y horizontal-solvability checker reported in chat was not recovered and is not certified by this document.

## Pinned inputs

1. [Conformal forward-source bridge, Section 8](https://github.com/gvakhrushev/d0_15/blob/c55a78aa1dcd6aae0641084e20e29d2d9fb4cb3d/02_REGISTRY/research/A4D_CONFORMAL_FORWARD_SOURCE_BRIDGE.md#8-a-legal-amplitude-enlargement-and-exact-scope-owner): exact full connection-stationary roots with logarithms bounded by `r_h >= h` and `r_h^3/h^2 -> 0`, satisfying one fixed sampled source, force `g:(tau-rho0[g])=0` pointwise. No unknown-field spatial derivative bound is used.
2. [Fixed-source algebraic compatibility, Sections 1-4](https://github.com/gvakhrushev/d0_15/blob/c55a78aa1dcd6aae0641084e20e29d2d9fb4cb3d/02_REGISTRY/research/A4D_FIXED_SOURCE_ALGEBRAIC_COMPATIBILITY.md): on the sampled cosine warp, every exact connection-stationary action value is real algebraic, whereas the sampled Einstein radial source forces `pi^2 L^2/1250`.

All physical-link, solder, Gram-packing and normalization conventions are those of these owners. No source is chosen from a computed connection response.

## 1. Fixed setting and statement

Fix once and for all

\[
f(y_1)=1+\frac{1-\cos(2\pi y_1)}{50},\qquad
S=\operatorname{diag}(1,1,f,f),\qquad
g=S^T\eta S=\operatorname{diag}(1,-1,-f^2,-f^2).
\]

Let `tau` be any one fixed smooth ten-slot metric covector density, declared before the links and meshes. For `L in 4 N`, `h=1/L`, retain the original samples `Q_h(x)=g(hx)`, `tau_h(x)=tau(hx)`, the original sufficiently small logarithmic chart, and every literal connection and metric Euler row:

\[
E_K(Q_h,K_h)=0,\qquad \Xi(Q_h,K_h)_x=h^2\tau(hx).
\tag{A1}
\]

**Corollary.** No refining sequence of (A1) can satisfy

\[
\|\log K_h\|_\infty=o(h^{2/3}).
\tag{A2}
\]

Equivalently, for every such fixed `tau` there exist positive constants `c_tau` and `h_tau` such that every exact root in the original chart at an allowed `h<h_tau` obeys

\[
\boxed{\|\log K_h\|_\infty\ge c_\tau h^{2/3}.}
\tag{A3}
\]

This is a necessary amplitude condition, not an existence theorem or a claim of a sharp threshold. The constants may depend on the fixed source. In particular it excludes the entire `O(h)` amplitude class for every fixed smooth source on this specific curved background, without imposing spatial regularity on the unknown links.

## 2. The arithmetic obstruction depends only on the trace

The second pinned owner gives, in the packed covector order
`(00,01,02,03,11,12,13,22,23,33)`,

\[
\rho_0=(-ff''-(f')^2/2,0,0,0,(f')^2/2,0,0,f''/(2f),0,f''/(2f)).
\]

Consequently

\[
g:\rho_0=-2ff''-(f')^2
=\frac{\pi^2}{625}(3c^2-102c-1),\qquad c=\cos(2\pi y_1).
\tag{A4}
\]

For every `L>=3`, roots-of-unity sums give `sum c_n=0` and `sum c_n^2=L/2`. With all `L^3` transverse copies included,

\[
\sum_xg(hx):\rho_0(hx)=\frac{\pi^2L^4}{1250}.
\tag{A5}
\]

Now suppose merely that `g:(tau-rho0)=0` pointwise; the nine traceless source components are unrestricted. The full-field radial action identity on exact roots gives

\[
\mathscr A_h=\sum_xQ_h:\Xi_x
=h^2\sum_xg(hx):\tau(hx)
=\frac{\pi^2L^2}{1250}.
\tag{A6}
\]

The sampled solder coefficients are real algebraic. The finite action is polynomial in the physical Lorentz-link entries, and the vanishing of all full connection Euler rows makes its critical value real algebraic by the second pinned owner's field-derivation lemma. Equation (A6) is transcendental, a contradiction.

Thus every fixed source with the Einstein trace is excluded on every allowed mesh, at any amplitude where the literal physical equations are defined. No algebraicity of the unknown links or of the source's traceless components is assumed. This strengthens the sampled-Einstein-source exclusion by allowing arbitrary trace-free additions to that source.

## 3. Amplitude escape

Suppose a sequence of exact roots satisfies (A2). On that sequence set

\[
r_h=\max\{h,\|\log K_h\|_\infty\}.
\]

Then `r_h>=h` and

\[
\frac{r_h^3}{h^2}
=\max\left\{h,\left(\frac{\|\log K_h\|_\infty}{h^{2/3}}\right)^3\right\}
\longrightarrow0.
\]

The first pinned owner therefore applies to this same sequence of retained exact roots. For every fixed smooth scalar probe `psi`, substituting (A1) in its forward-response estimate and passing through the smooth Riemann sum yields

\[
\int\psi\,g:(\tau-\rho_0)=0.
\]

The source and background are fixed and smooth, so the fundamental lemma gives `g:(tau-rho0)=0` pointwise. Section 2 then excludes every member of the sequence. This proves (A2) is impossible.

To obtain the quantified form (A3), suppose it fails for one fixed `tau`. For each positive integer `n`, choose an allowed mesh `h_n<1/n` and an exact root with

\[
\|\log K_{h_n}\|_\infty<h_n^{2/3}/n.
\]

These roots constitute exactly a prohibited sequence (A2). Hence some positive `c_tau,h_tau` exist. If there are eventually no roots, (A3) holds vacuously; it does not assert nonemptiness.

## 4. Scope and validation

The original fixed-small-chart/raw-owner task remains **PARTIAL / OPEN**. Fixed-amplitude roots with a different trace, or amplitudes comparable to or larger than `h^(2/3)`, are not excluded by this argument. It neither establishes their existence nor supplies an admissible separated-gap counterexample. No source, norm, comparator, action, claim status or task lifecycle is changed.

During reconstruction, the trace polynomial (A4) and exact mean coefficient in (A5) were independently recomputed with symbolic rational arithmetic. The analytic implication is the proof above, based on the two pinned input theorems; this is not a new full-owner numerical replay, a Lean build, or a claim that CI on this new commit has passed. The unavailable Y-rank certificate is explicitly outside this validation record.
