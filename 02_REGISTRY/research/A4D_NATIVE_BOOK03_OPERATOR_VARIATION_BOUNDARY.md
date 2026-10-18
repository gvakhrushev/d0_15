# G0: complete variation of the Book 03 feedback component

Date: 18 October 2026. Primary owners:

- `01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md`, §01.0, Git blob `87f3dbd0e5e760d46a577a275aabc16623d3f09e`, SHA-256 `668fc904b0585cc7fd5175babead5225c22051422c9c64e197d7b0d42d225342`.
- `01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md`, §§03.0 and 03.3.2, Git blob `ecdd31abb52c94e9f2a157a80c7c49a6f5ac31aa`, SHA-256 `dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d`.

**Scope.** This closes the mathematical operator-variation problem for the isolated Book 03 feedback component under Book 01's retained/archive constraint. It does not identify its operator tangents with physical metric, record, or matter variations, and it is not the full preparation/action/source stack.

## 1. Exact finite operator family and all its tangents

Book 01 fixes orthogonal projections `P_N,Q_N` with `P_N+Q_N=I` and `P_N Q_N=0`; hence `Q_N=I-P_N`. Book 03 defines the finite feedback component by

\[
 F=P U^* Q U P=P U^*(I-P)U P,
 \qquad I_{fb}=-\log\det(I-zF),\qquad 0<z<1.
\]

At fixed finite dimension and fixed projection rank, the complete mathematical operator family is therefore parameterized by a Grassmannian point `P` and a unitary `U`; `Q` is derived, not an independent projector. With `B=QUP`, `F=B^*B`, so `0\le F\le P\le I`. Thus `I-zF` is positive definite and the feedback action is smooth. The scalar fugacity `z` may be held fixed or varied as a separate input.

Every differentiable path in this constrained family has

\[
 X=\dot P=X^*,\quad XP+PX=X,
 \qquad \dot Q=-X,
 \qquad \dot U=KU,\quad K^*=-K.
\]

These conditions are also sufficient. The projector equation implies `PXP=(I-P)X(I-P)=0`; `K_P=XP-PX` is skew-adjoint with `[K_P,P]=X`, and `P(t)=e^{tK_P}Pe^{-tK_P}` realizes every such `X`. Every skew-adjoint `K` is realized by `U(t)=e^{tK}U`. The constraint then forces `Q(t)=I-P(t)` and `\dot Q=-X`. There is no independent `Q` tangent in the literal Book 01 split.

## 2. Full first source and constrained stationary equations

Put `R=U^*QU` and `\Pi=z(I-zF)^{-1}`. Differentiating the actual constrained operator gives

\[
 \dot R=U^*(-X+[Q,K])U,
 \qquad
 \dot F=XRP+P U^*(-X+[Q,K])UP+PRX.
\]

For an additional field variation `v` with `X=DP[v]`, `K=DU[v]U^*`, and `\dot z=Dz[v]`, the complete pullback source is

\[
 DI_{fb}[v]=\operatorname{Tr}(\Pi\dot F)
 +\operatorname{Tr}((I-zF)^{-1}F)\,\dot z.
\]

This includes the outer-`P` legs, the `Q=I-P` leg, the unitary leg, and the fugacity leg. For a compact stationary form define

\[
 G_P=RP\Pi+\Pi PR,
 \qquad G_Q=UP\Pi PU^*.
\]

The source can then be written

\[
 DI_{fb}=\operatorname{Tr}((G_P-G_Q)X)
       +\operatorname{Tr}(G_Q[Q,K])
       +\operatorname{Tr}((I-zF)^{-1}F)\,\dot z.
\]

With `z` fixed and `P,U` varied independently over the complete mathematical tangent family, criticality is equivalent to

\[
 [P,G_P-G_Q]=0,
 \qquad [Q,G_Q]=0.
\]

The first is the Grassmannian Euler equation after including the induced `Q` variation; the second is the unitary Euler equation. They are the equations for this isolated component, not the stationarity equations of the full D0 action. If `z` is also free, then

\[
 D_z I_{fb}=\operatorname{Tr}((I-zF)^{-1}F)>0 \quad (F\ne0),
\]

so a nonzero-return stationary point requires `z` to be fixed by another native constraint or balanced by other terms of the same full action.

The exact representation redundancy within the constrained family is the left stabilizer of `Q`: if `V` is unitary and `VQ=QV`, then `U\mapsto VU` preserves `F` and `I_{fb}`. It is not automatically a gauge symmetry of the full D0 price, whose other components may read `U` separately.

## 3. Same operator state, different field source

The Book 01 complement constraint does not determine a field lift. On `\mathbb C^2`, take

\[
 P_0=\operatorname{diag}(1,0),\qquad
 Q_0=I-P_0=\operatorname{diag}(0,1),
\]

and let `U_\theta` be the real rotation through `\theta`. Then

\[
 F_\theta=\sin^2\theta\,P_0,
 \qquad I_{fb}(\theta)=-\log(1-z\sin^2\theta).
\]

At the same base `\theta=\pi/4`, the constant lift `\theta(s)=\pi/4` and the moving lift `\theta(s)=\pi/4+cs`, `c\in\mathbb R`, have identical base `P,Q,U(0),z,F(0)` and action value, and both preserve `Q(s)=I-P(s)` (here `P` is fixed). Their field derivatives are

\[
 \frac{d}{ds}I_{fb}\big|_{s=0}=0
 \quad\hbox{and}\quad
 \frac{d}{ds}I_{fb}\big|_{s=0}=\frac{cz}{1-z/2},
\]

respectively. Since `z/(1-z/2)>0`, the unspecified smooth lift can give any real first source at the same operator base point, even while retaining the exact Book 01 complement. This proves non-identifiability of the field derivative from the feedback operator law alone. These are mathematical lifts of the interface; neither is asserted to be physically admitted by D0.

## 4. G0 disposition and exact boundary

The primary books determine the finite support split and the feedback formula. For that constrained operator component, all mathematical tangents, its complete first source, its isolated stationary equations, and its exact representation redundancy are now explicit. A separate Lean bridge also identifies the blank one-tick `fullStep` branch masses with the owned golden cylinder weights. A positive normalized two-tick control with the same gate marginals but a different joint weight proves that this first tick does not determine the multi-tick law. What remains unowned is the pullback from the common geometric/matter state `(q,D,b,m)` and its retained history to the admitted `P,U,z` variation, together with the corresponding refinement/composition law. The operator law and one-tick gate alone cannot choose that pullback or transfer its derivative to the native metric/matter source.

This is a scoped G0 boundary, not a completeness proof for every D0 primitive owner and not a no-go for all of D0. It does not establish the total cost, matter Ward identity, native stationarity, a coupled curved root, soundness/recovery, or GR. The existing parent obligations remain open.

## 5. Reproducible controls

`certificates/a4d_book03_feedback_variation_check.py` pins both primary books and checks the complement constraint and tangent, the full `P,U,z` product rule, the constrained source contraction, the `Q`-stabilizer redundancy, and the equal-base/different-source witness. The exact checker validates finite matrix controls only; the all-dimensions tangent characterization and Euler equivalence are proved analytically above. Ordinary and optimized runs must produce byte-identical output.

## 6. One-tick golden gate and the two-tick boundary

`D0.Research.GoldenCylinderOneStepBridge.blank_gate_matches_one_step_cylinders` proves that the two recorded squared amplitudes of the existing blank-input `fullStep` are exactly `cylWeight [true] = φ⁻¹` and `cylWeight [false] = φ⁻²`; `p = φ⁻¹` follows from the gate's owned equations `a²=p` and `p+p²=1`. No probability is fitted. The theorem only identifies the one-step marginal.

The same module constructs a strictly positive normalized joint table on two readouts. Each coordinate has exactly the gate marginals `(p,p²)`, yet its `true,true` mass differs from the product cylinder by `p⁴/2`. Thus one-step agreement cannot establish independent repeated refinement or the full event-history law. The table is a mathematical counterexample to that inference, not a claim that this correlated completion is physically admitted by D0. A native multi-tick record/refinement map remains necessary.
