# D0 → GR: global joint index, complete preparation stationarity, and the rigidity consumer

22 October 2026. Supporting mathematical composition in existing Draft PR
**#334**, task `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`native-programme-v1 / constitutive`. Read-only source snapshot:
`fcfc52064737815c75bef96f7696b473ee304061`.

**Status:** the conditional global existence theorem below is proved here.
Its actual complete Book03 boundary source and actual admissible preparation
manifold have not been constructed or verified by this note. No physical
action, input permission, information rule, coupling, acceptance flag, BOOK
claim, or universal GR conclusion is changed. `GR_closed=false`.

## Краткий итог

Существование полного решения можно доказывать глобально. Уже имеющийся
невырожденный 42-полевой корень даёт ненулевой топологический индекс. Если
полный источник при добавлении фактических членов цены не обращается в нуль
на границе выбранной области, этот индекс сохраняется. Для действительно
допустимого компактного пространства подготовки с ненулевой эйлеровой
характеристикой итоговый индекс равен произведению двух индексов. Поэтому
одновременно исчезнуть все решения полевых уравнений и уравнений подготовки
невозможно.

Это допускает седло, сдвиг старого корня, вырождение гессиана внутри области
и рождение или слияние ветвей. Малость производной по подготовке не нужна.
Для исходного сертификата ниже получен конкретный достаточный запас на
границе: при полном дополнительном полевом источнике не больше `1e-22`
остаётся строго положительная граница `1.85506724799e-21` в исходной
предобусловленной норме. Фактическое выполнение этой оценки не утверждается.

Континуальный результат получается последующим применением компактности,
согласованности нормированного полного источника и уже сформулированного
потребителя геометрической жёсткости. Конечный индекс обеспечивает
совместное существование; идентификация общего предельного закона остаётся
отдельным содержательным входом этой композиции.

## 1. The same physical object and the known degree seed

Write `z` for all independent field coordinates after any justified gauge
choice, and `u` for genuinely independent preparation coordinates. Generated
prefix states and variables already constrained by a native stationarity
law may be eliminated only with their complete adjoint source retained
(section 7). A field-dependent initial preparation is not automatically a
generated variable.

The endpoint action `S_full(z,u)` must be the complete real price of one
admitted finite execution: the actual preparation, original record and
oldRIGHT treatment, clock, work, information, heat, and return terms. The
same field chart and physical initial boundary apply to every term. The
already charged original `0/10` reporting cost must not be charged twice.

The original [unpadded root receipt](sources/d0_original_unpadded42_2026-10-22/RESULT.json)
has immutable Git blob `0ac76b58522d84f5bcc787fb6b6da0c99e1211cd`.
It supplies an isolated nonflat stationary point of the configured original
N1 action `S0(z)` with nonsingular, indefinite full 42-Hessian. The number
`h0 = 0.18380152465817944666...` is the fixed mesh parameter of that
certificate; the field root is a **42-vector**, not that scalar.

On an isolating field domain `Omega` containing just this root,

\[
d=\deg(\nabla S_0,\Omega,0)
  =\operatorname{sgn}\det D^2S_0(z_*)\in\{-1,+1\}.
\tag{1}
\]

The exact sign is unnecessary for existence. A saddle has nonzero local
degree whenever its Hessian is invertible. The older
[full-source robustness owner](A4D_ORIGINAL_UNPADDED_0_10_FULL42_SOURCE_ROBUSTNESS_2026_10_22.md)
provides the quantitative estimates consumed in section 4. This note does
not rerun its interval Hessian calculation.

## 2. Global joint existence theorem

Let `Omega` be a bounded open subset of `R^m`, and let `M` be a compact smooth
manifold without boundary. An orientation may be assumed for the standard
integer-index presentation. Equip `M` with any smooth positive Riemannian
metric. This merely converts the preparation covector into a tangent vector
field; its zeros do not depend on that metric.

Suppose `S_t`, `0 <= t <= 1`, is a family of real `C1` functions on a
neighbourhood of `closure(Omega) x M`, with jointly continuous first source

\[
E_t(z,u)=\bigl(\nabla_zS_t(z,u),\operatorname{grad}_M S_t(z,u)\bigr).
\tag{2}
\]

Assume:

1. `S_0(z,u)=S0(z)` and `deg(grad S0, Omega, 0)=d != 0`.
2. `S_1=S_full`, the unchanged complete physical endpoint action.
3. The **full** source has no boundary zero:

\[
\boxed{E_t(z,u)\ne0\quad
 (z,u,t)\in\partial\Omega\times M\times[0,1].}
\tag{3}
\]

Then the localized vector-field index satisfies

\[
\boxed{\operatorname{Ind}(E_1,\Omega\times M)=d\,\chi(M).}
\tag{4}
\]

In particular, if `chi(M) != 0`, there is a joint stationary point

\[
\boxed{\nabla_z S_{\rm full}(z_*,u_*)=0,
\qquad \operatorname{grad}_M S_{\rm full}(z_*,u_*)=0.}
\tag{5}
\]

The index is defined for a continuous tangent field with compact interior
zero set by a sufficiently small transverse approximation. Cubical field
domains cause no difficulty: the localized index is supported in the
interior, away from the boundary corners.

### Proof

By compactness, (3) has a positive uniform margin `delta`. Choose a smooth
Morse function `f` on `M` and a positive `epsilon` so small that
`epsilon sup_M |grad f| < delta/2`. For the proof only, use

\[
\widetilde S_t=S_t+\epsilon(1-t)f(u).
\tag{6}
\]

Its first source remains nonzero on the boundary. At `t=0` the field is the
product `(grad S0, epsilon grad f)`. After a permitted small approximation
of the field factor if needed, the local index at each product zero is the
product of the two local indices. Summing gives

\[
\operatorname{Ind}(\widetilde E_0)
=d\sum_{\operatorname{grad}f=0}(-1)^{\operatorname{MorseIndex}(f)}
=d\,\chi(M),
\tag{7}
\]

by Poincare–Hopf on the closed preparation manifold. Homotopy invariance of
the localized index under a boundary-zero-free homotopy gives (4), since
`widetilde E_1=E_1`. A field without zeros has index zero, proving (5).

The proof term in (6) vanishes **exactly** at the physical endpoint. It adds
no endpoint action, force, penalty, preparation rule, or adjustable coupling.
The parameter `t` is a comparison parameter, not a physical clock.

Condition (3) is weaker than requiring the field component alone to stay
nonzero. A field root may reach the boundary while a nonzero preparation
source keeps the complete boundary source away from zero. No claim that an
arbitrary boundary field has index `chi(Omega x M)` is used: the index is
computed at the reference and transported with its boundary data.

### Constant field preconditioning

For any fixed invertible real matrix `A`,

\[
\widehat E_t=(A\nabla_zS_t,\operatorname{grad}_M S_t)
\tag{8}
\]

has precisely the same zeros. A constant bundle automorphism multiplies
every local index by `sgn det A`, so

\[
\operatorname{Ind}(\widehat E_1)
=\operatorname{sgn}\det(A)\,d\,\chi(M).
\tag{9}
\]

The preconditioned field need not itself be a gradient. This is numerical
and topological preconditioning of equations, not modification of the action.

## 3. Preparation topology is an actual input

For all admitted pure rays in a `D`-dimensional complex Hilbert subspace,

\[
M=\mathbb{CP}^{D-1},\qquad \chi(M)=D.
\tag{10}
\]

There is one cell in each real dimension `0,2,...,2D-2`. Products of these
spaces have Euler characteristic `product_j D_j`, again nonzero. Complex
Grassmannians or fixed-spectrum density-matrix flag manifolds can also have
nonzero Euler characteristic.

Equation (10) is applicable only when this is the genuinely admitted
preparation space of the complete execution. A finite-word orbit does not
become a smooth manifold merely because it is dense. A phase torus, a
unitary-controller group, or a space of purifications with a protected fixed
marginal can have different topology. Normalized vectors form an odd sphere;
quotienting them to projective space is justified only if global phase is
redundant for the complete action and all retained physical data. A genuine
independent control cannot be removed to manufacture a favourable index.

No actual `M` is selected by this note. If `M` has boundary or is noncompact,
additional boundary or escape control is needed. If `chi(M)=0`, (4) is
inconclusive; the regular-sheet theorem in section 5 remains available.

## 4. A quantitative joint-existence consumer of the original certificate

Let `z0` and `A` be the original rational centre and saved preconditioner,
and write `H0=D2S0(z0)` for the Hessian at that centre. The owned strict
estimates are

\[
\begin{aligned}
\|A\|_\infty&<28.883,\\
\|I-AH_0\|_\infty&<0.036547,\\
\|A\nabla S_0(z_0)\|_\infty&<3.01\cdot10^{-52},\\
\|D^2S_0(z)-D^2S_0(z_0)\|_\infty
&\le C\|z-z_0\|_\infty,
\quad C=1.69344\cdot10^{18}.
\end{aligned}
\tag{11}
\]

The first inverse-defect estimate implies that `A` is invertible; it is not
an estimate of `||H0^-1||`. Set

\[
r=10^{-20},\qquad B=\{z:\|z-z_0\|_\infty\le r\}.
\]

The Hessian bound gives throughout this cube

\[
q:=\sup_B\|I-AD^2S_0(z)\|_\infty
<0.036547+28.883\,C\,r
=0.52566327520.
\tag{12}
\]

Integration on the segment from `z0` to `z` yields

\[
\|A\nabla S_0(z)-(z-z_0)\|_\infty
<3.01\cdot10^{-52}+q\|z-z_0\|_\infty.
\tag{13}
\]

Hence on the entire boundary of `B`,

\[
\|A\nabla S_0(z)\|_\infty
>(1-q)r-3.01\cdot10^{-52}
>4.743367248\cdot10^{-21}-3.01\cdot10^{-52}.
\tag{14}
\]

The straight comparison to `z-z0` in (13) is also boundary-zero-free, so
`deg(A grad S0, int B, 0)=+1`.

Now let `G(z,u)=S_full(z,u)-S0(z)` be the **actual remaining price** and
`R_z=partial_z G`. Suppose its complete additional field source obeys only
the following boundary bound, uniformly over the actual compact `M`:

\[
\boxed{\sup_{\partial B\times M}\|R_z\|_\infty\le10^{-22}.}
\tag{15}
\]

For `S_t=S0+tG`, the scaled correction is at most `2.8883e-21`. Therefore

\[
\boxed{\inf_{\partial B\times M\times[0,1]}
\|A\nabla_zS_t\|_\infty
>1.85506724799\cdot10^{-21}>0.}
\tag{16}
\]

If `G` has a continuous complete first source and `chi(M) != 0`, the global
theorem forces a **joint field–preparation root** in `int B x M`. There is
no smallness assumption on `partial_u G`, and no nonsingularity condition on
the endpoint joint Hessian. Unlike a contraction proof, (15) need not hold
inside the cube. The preparation equation is obtained from the product
index, not discarded by freezing the input.

Neither (15) for the actual Book03 residual nor the actual compact `M` has
been verified here. The new estimate is a precise sufficient consumer of
existing numerical bounds, not a claim that the physical execution passes
it. The `1e-20` cube is larger than the original `1e-24` root enclosure:
nonflatness and other physical-chart margins on this larger cube have not
been rechecked by this note. To conclude nonflatness of the forced root,
protect the entire chosen domain by a certified geometric witness, or
certify that witness at the new root.

Larger legitimate isolating domains can be tested. For example,
`<A grad S0, A grad S_full> > 0` on their boundary is a sufficient
zero-free interpolation test and permits large transverse corrections.
Failure of the conservative bound (15) is not a nonexistence theorem.

## 5. Regular-sheet existence when the Euler characteristic test is silent

Let `M` be compact without boundary and let

\[
Z=\{(z,u)\in\Omega\times M:\nabla_zS_{\rm full}(z,u)=0\}
\]

be nonempty, compact, and contained in the interior field chart. Suppose
`S_full` is `C2` near `Z` and `S_zz` is invertible at every point of `Z`.
Then `Z` is a `C1` embedded manifold whose projection to `M` is a local
`C1` diffeomorphism. Compactness makes this projection a covering over every
connected component of `M` that it meets. It may have multiple sheets;
a global single-valued field solution is unnecessary.

The function `W=S_full|Z` attains an extremum. Every preparation tangent
`delta u` lifts to a tangent of `Z` by

\[
\delta z=-S_{zz}^{-1}S_{zu}\delta u.
\]

At that extremum, `dW=partial_uS_full delta u=0` for every `delta u`.
Thus the complete preparation equation holds alongside the field equation.
On a local sheet `z=Y(u)`, this recovers the exact identities

\[
DW=S_u,
\qquad D^2W=S_{uu}-S_{uz}S_{zz}^{-1}S_{zu}.
\tag{17}
\]

This is an existence argument using an extremum on the field-critical
manifold. It does not claim an unconstrained minimum of the Lorentzian field
action, or derive a physical MDL selection rule. The theorem in section 2
avoids this regularity requirement when its nonzero index is available.

## 6. Continuous complete entropy sources through finite rank birth

Let `T` be a finite complex matrix and define

\[
\mathcal H(T)=-\operatorname{Tr}(TT^\dagger\log TT^\dagger),
\qquad 0\log0:=0.
\tag{18}
\]

**Lemma.** `H` is continuously differentiable in the real and imaginary
matrix entries, including matrices of deficient rank. At positive singular
values its derivative is

\[
D\mathcal H(T)[V]
=-2\operatorname{Re}\operatorname{Tr}
\bigl[((\log TT^\dagger+I)T)^\dagger V\bigr],
\tag{19}
\]

where the product is continuously defined as zero on zero singular values.

**Proof.** For the Hermitian dilation
`K(T)=[[0,T],[T^dagger,0]]`, use the scalar function
`phi(s)=s^2 log s^2`, with `phi(0)=0`. It is `C1`, since
`phi'(s)=2s(log s^2+1)` tends to zero at the origin. Finite-dimensional
trace spectral calculus gives a continuous derivative for
`Tr phi(K(T))`, which is twice `Tr TT^dagger log TT^dagger`.
Differentiation gives (19).

For a fixed finite Kraus execution with pure input amplitude, every
unnormalized branch state has the form `Omega_a=T_a T_a^dagger` with
`T_a` continuously differentiable in the actual amplitudes and fields. Its probability
`p_a=Tr Omega_a` satisfies the analogous result for `p_a log p_a`.
Consequently the complete weighted conditional entropy

\[
p_a S(\Omega_a/p_a)
=-\operatorname{Tr}\Omega_a\log\Omega_a+p_a\log p_a
\tag{20}
\]

extends with continuous first source through `p_a=0`. Finite sums and the
classical record entropy retain this property. An unweighted postselected
entropy has a different singularity question and is not substituted here.

Thus a rank-birth obstruction to a bounded entropy Hessian need not block
the continuous-source index theorem. Finite `log Tr exp` heat is smooth for
a smoothly varying finite Hermitian operator. The actual log determinant
still needs its spectral invertibility, and moving active cuts must have
their genuine derivatives. This lemma proves no permission to vary an input
outside the native writer image.

## 7. Native Poisson/Fredholm elimination of constrained preparation

There is a complementary exact reduction for an internally generated
stationary state. Suppose the native constraint is
`Psi_{z,u}(rho)=rho`, `Tr rho=1`, for the actual trace-preserving channel.
For a real scalar price `P(z,u,rho)`, let `s=D_rho P` and use the real
Hilbert–Schmidt pairing. The constrained Lagrangian is

\[
L=P+\langle Y,\Psi\rho-\rho\rangle
       +\lambda(\operatorname{Tr}\rho-1).
\]

Its internal adjoint equation is exactly

\[
(I-\Psi^*)Y=s+\lambda I.
\tag{21}
\]

If the stationary state is unique on the relevant real operator space,
Fredholm compatibility fixes `lambda=-Tr(rho s)`. On the centered
complement the Poisson equation then determines `Y` up to its harmless
identity freedom. The retained field or independent-input source is

\[
\boxed{D_{z,u}P_{\rm reduced}
=\partial_{z,u}P
 +\langle Y,(D_{z,u}\Psi)\rho\rangle.}
\tag{22}
\]

For a larger fixed-state space, compatibility requires `s` to annihilate
every trace-zero stationary variation, or its corresponding version with
the actual additional retained constraints. Protected spectators cannot be
silently removed. A spectral projection onto stationary states supplies
the exact Fredholm test; a chosen centering convention cannot manufacture
its satisfaction.

The primary [complete Poisson and Hessian owner](A4D_COMPLETE_NATIVE_FIRST_MATCH_ENTROPIC_POISSON_PREPARATION_AND_HESSIAN_2026_10_22.md)
and [oldRIGHT Fredholm owner](A4D_ORIGINAL_OLDRIGHT_ARCHIVE_FREDHOLM_INFORMATION_AND_TWO_STAGE_GATE_2026_10_22.md)
already supply the general adjoint formula and the full spectator compatibility
criterion. The existing [finite-age preparation composition](A4D_NATIVE_FINITE_AGE_CLOCK_AND_PREPARATION_SOURCE_COMPOSITION_2026_10_22.md)
and its [spectator Poisson calculation](sources/d0_native_stationary_memory_composition_2026-10-22/SPECTATOR_POISSON.md)
are native owners for applying this reduction with their actual source and
boundary terms. This note does not identify distinct information conventions
or executions. A truly independent initial preparation, input controller,
or clock parameter remains in `u` after (21)–(22). The resulting **complete**
reduced source is the object to which the global index theorem applies.

## 8. Refinement, compact solution sets, and the GR rigidity consumer

Apply the finite theorem separately at each admitted mesh `h`. It gives
nonempty complete solution sets when its native hypotheses hold. A continuum
conclusion additionally requires compactness of reconstructed fields in a
topology supporting the claimed equations and a consistent normalized source:

\[
\gamma_h^{-1}E_{h,\mathrm{field}}
=\operatorname{Res}_h E_{\mathrm{continuum}}+\mathcal R_h,
\qquad \|\mathcal R_h\|\longrightarrow0.
\tag{23}
\]

Here `gamma_h` is the actual source gain. A small unnormalized residual is
insufficient when that gain vanishes. Exact finite roots, compactness and
(23) give a subsequential solution of the identified continuum equations.
Full-sequence convergence needs an additional uniqueness or stability input.
A nonflat continuum conclusion needs a geometric margin that survives
refinement; finite nonflatness alone supplies no such margin.

If, more strongly, nonempty compact Hausdorff exact solution sets `K_n` have continuous
compatible bonding maps `p_mn:K_m -> K_n` taking **exact solutions to exact
solutions**, their inverse limit is nonempty. Indeed, in the compact product
`product_n K_n`, every finite collection of compatibility conditions can be
satisfied by choosing an element at a common finer level and taking its
images. The finite-intersection property supplies a compatible family.
Surjectivity is not needed for nonemptiness, although it is relevant to
surjectivity of the individual limit projections. Ordinary approximate
coarse-graining does not automatically give these exact bonding maps; in
that situation the compactness-and-consistency route (23) is the appropriate
consumer. Abstract inverse-limit existence still needs a physical continuum
interpretation.

The [Golden discrete rigidity owner](A4D_GOLDEN_DISCRETE_BLOWUP_CONDENSED_GR_2026_10_20.md)
already proves that the **same complete selected gravitational source** is
`E[g] = a G[g]` if it is a metric-only symmetric covariant tensor, commutes
with restriction and local diffeomorphisms, is continuously Frechet
differentiable at constant Lorentz metrics in the stated smooth metric
topology, and satisfies both the off-shell Ward identity and the actual
physical one-step scaling law

\[
\nabla_g^\mu E_{\mu\nu}[g]\equiv0,
\qquad E[\varphi^2g]=E[g].
\]

The same admitted transformation of native control, record and clock
variables must justify that scale comparison before internal elimination.
The owner's equivalent normalized-refinement version is also sufficient.
This stronger route does **not** assume a second differential order.
The separate [VSI/Lovelock two-witness owner](A4D_VSI_LOVELOVK_TWO_WITNESS_UNIVERSAL_GR_SYNTHESIS_2026_10_20.md)
uses its explicit second-jet premise and allows the corresponding calibrated
Einstein and cosmological terms. These are distinct sufficient routes.
Tomographic invertibility, the archive's Golden count, or agreement on one
Brinkmann family does not establish either route's full hypotheses. Once
they hold, the existing geometric and matter witnesses can fix the
remaining coefficients and nonzero source ratio through the actual
normalization. Matter equations and any independently retained fields remain
part of the complete system.

The complete sufficient composition is therefore:

\[
\boxed{
\begin{gathered}
\text{admitted complete source + nonzero joint index}
\\\Longrightarrow\text{finite joint solutions},\\
\text{uniform compactness + normalized consistency}
\\\Longrightarrow\text{continuum solutions},\\
\text{same-source rigidity hypotheses + coefficient witnesses}
\\\Longrightarrow\text{the asserted GR specialization}.
\end{gathered}}
\tag{24}
\]

This note proves the first mathematical index mechanism and its quantitative
consumer, including every independent preparation equation. It does not
assert that the physical boundary source, preparation topology, refinement
estimates, or general-source rigidity inputs have already been supplied.

## 9. Reproducible verification and consuming step

The new [standard-library checker](sources/d0_global_joint_index_2026-10-22/check_global_joint_index.py)
consumes the immutable original receipt, checks the exact rational boundary
budget, and evaluates an explicitly labelled analytical control on
`R^42 x S^2`. That coupled control has two joint roots before an interior
degeneracy and six afterwards, with the same total joint index `-2`.
Separate controls show why escape through the field boundary and a
preparation space with boundary cannot be omitted. These controls illustrate
the proof; they are not the physical D0 action.

The saved [result](sources/d0_global_joint_index_2026-10-22/RESULT.json)
was identical under normal Python and `python -O`. The checker uses explicit
runtime conditions, exact rational arithmetic and no third-party packages.
It does not evaluate the actual complete Book03 residual or replay the
original interval certificate. No unchanged historical numerical or Lean
suite is represented as newly run.

The consuming step remains inside the same source task and same complete
execution: identify its actual independent preparation space (or eliminate
genuinely constrained variables with their adjoint reaction), then certify
a boundary homotopy for its complete source. This proves joint existence
through one global certificate, permitting all interior folds, rather than
requiring another sequence of locally regular roots. The refinement and
same-source rigidity consumers in section 8 are part of the stated terminal
composition; this supporting theorem does not replace them.

## Sources and provenance

- Original snapshot: [fcfc52064737815c75bef96f7696b473ee304061](https://github.com/gvakhrushev/d0_15/tree/fcfc52064737815c75bef96f7696b473ee304061).
- Original numerical seed: [immutable unpadded receipt](https://github.com/gvakhrushev/d0_15/blob/fcfc52064737815c75bef96f7696b473ee304061/02_REGISTRY/research/sources/d0_original_unpadded42_2026-10-22/RESULT.json), blob `0ac76b58522d84f5bcc787fb6b6da0c99e1211cd`.
- Original [source-robustness proof](https://github.com/gvakhrushev/d0_15/blob/fcfc52064737815c75bef96f7696b473ee304061/02_REGISTRY/research/A4D_ORIGINAL_UNPADDED_0_10_FULL42_SOURCE_ROBUSTNESS_2026_10_22.md); all bounds in (11) are consumed, not regenerated.
- [Book03 finite equations](https://github.com/gvakhrushev/d0_15/blob/fcfc52064737815c75bef96f7696b473ee304061/01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md), §03.8: native finite stationarity is distinct from a freely varied field minimum.
- Victor Guillemin and Peter J. Haine, [*Differential Forms*](https://math.mit.edu/classes/18.952/2018SP/files/18.952_book.pdf), 2018 draft, §§4.7 and 4.9: degree homotopy invariance, additivity and the nondegenerate index sign.
- S. M. Gusein-Zade, [*Index of a singular point of a vector field or of a 1-form on an orbifold*](https://arxiv.org/html/1903.06978v1), introduction: the classical closed-manifold Poincare–Hopf identity used in (7).

The external topology theorems supply standard mathematical tools. They do
not certify a D0 execution or its physical interpretation. No new numerical
root, native preparation manifold, full source evaluation, interval
curvature check, Lean proof, or completed GR derivation is claimed here.
