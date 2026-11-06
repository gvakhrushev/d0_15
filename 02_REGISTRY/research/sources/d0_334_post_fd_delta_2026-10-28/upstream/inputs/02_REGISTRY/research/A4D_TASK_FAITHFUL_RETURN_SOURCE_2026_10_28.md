# Same-task QUERY descent and retained-history source synthesis

28 October 2026. Existing research PR #334, `gvakhrushev/d0_15`.
Input `d4c700f78572179ffb6fc98a12ca7e31fa2bc1b4` (7dh945–953).
Incoming `73816d279dc23ee62be75662bf3081013a49ad55` is consumed and preserved.

[Full Russian proof](sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md),
[executed checker](sources/d0_task_faithful_source_2026-10-28/check_task_source.py),
[observed result](sources/d0_task_faithful_source_2026-10-28/result.json),
[previous two-field analytic handoff](sources/d0_task_faithful_source_2026-10-28/TWO_FIELD_HANDOFF_RU.md).

## What is now proved

The incoming 7dh QUERY normal is a genuine nonzero source in every new block;
accumulated-history normalization cannot erase it. This packet computes exactly
what that normal changes: the full-input report effect. It then proves source
invariance for ALL implementations of the same specified effect in the existing
echo class, and controls actual finite approximations without a small-past-gap
or exponentially suppressed-gain penalty. No Einstein acceptance condition,
new action, price counterterm or independently prepared observer is introduced.

For the whole unprepared SOURCE embedding i, actual reporter T, output effect Pi
and sign Z=I-2Pi, set E_T=i* T* Pi T i. Equal report probabilities for ALL input
density operators are equivalent to E_T=E_0. Classical basis probabilities or
agreement at one chosen input are not enough. Other prescribed task marks must
also be retained; this is not equality of every possible future context.

For the genuine preparation R(Y) and full echo A(Y)* T* Z T A(Y),

    C(Y,T)=R(Y)*(I-2E_T)R(Y).

Thus E_T=E_0 implies equality of the cold operator and original return price for
EVERY Y, including all first and mixed source derivatives. Vertical same-task
variations have zero source; genuine preparation changes keep their derivatives.
The full operators may differ on unprepared work columns. No arbitrary complete
channel dilation or full heat is identified merely by its report effect.

## Exact source over the actual matrix past

Keep the original old corner K, S=K* K>=0, S!=0, scalar new corners c_j>0,
T_return=product c_j^2 and D=(1-zeta)I+zeta T_return S. With

    w=zeta T_return Tr(S D^-1),
    Pi_out=K D^-1 K*/Tr(S D^-1),

an independent reporter-effect variation gives

    delta_j J=(4w/c_j) Tr(Pi_out R_j* delta E_j R_j).

The positive dual weight is also present in incoming73816 and is not claimed
as a new discovery. The new application identifies the normal with delta E_j.
For the 7dh conjugacy orbit, delta<E_j>=sqrt(1-c_j^2), reproducing precisely
its positive row w*4sqrt(1-c_j^2)/c_j. That orbit changes the report law.
If such changes are physically allowed, its source remains; it is not gauge.

## Finite errors: a uniform relative bound, not a fictitious tangent constraint

If ||C_hat,j-c_j I||<=2epsilon_j, d_j=2epsilon_j/c_j<1, set
eta=sum_j[-log(1-d_j)]. The actual noncommuting product obeys

    exp(-2eta) T_return S <= K_hat* K_hat <= exp(2eta) T_return S.

Logdet monotonicity and the scalar logarithmic derivative w give

    |J_hat-J| <= [exp(2eta)-1] w.

There is no factor ||S^-1||, 1/T_return or the full ambient dimension. The bound
also holds for nonzero singular S. The actual source/gain and the error of that
same price are suppressed together by history. When S=0, the normalized gain
vanishes and is explicitly excluded.

For real same-task +/-t endpoints with a common old K, theta=max|log(T_±/T_0)|,
Gamma_0=w_0 Lambda_0 and the maximum endpoint eta,

    normalized return-contrast error
       <= exp(theta)[exp(2eta)-1]/(|t| Lambda_0).

This is a finite inequality; a small value tolerance is NOT used to restrict a
tangent space or bound a derivative. Actual readout error still divides by
|t|Gamma_0. Full heat is equal only on the stated fixed-clock, fixed-carrier,
fixed-signature parked echo family; otherwise its own full residual is added.

## One composition, not another geometric example

Incoming [apparatus descent](A4D_REGULAR_APPARATUS_SOURCE_DESCENT_2026_10_28.md)
gives on its actual guarded graph G_h the OFF-SHELL operator identity

    A_h(u)=DI_(tau,h)[V_h(u)]+R_h(u),
    ||R_h(u)||op<=epsilon_h ||u||raw, epsilon_h->0.

The present same-task reporter fibre S_h has zero full source under the heat
hypotheses above. On G_h+S_h use the sum-hull of the existing joint regular norm
and the actual semantic-comparison norm. Its dual is the maximum of the two
restriction norms, so adding ALL S_h directions does not worsen the incoming
bound. For the parent's real accumulated weights,

    ||DB_M/Gamma_M||ext*
       <= C_xi/Lambda_M + E_heat,M
          +sum_j theta_j(delta_j+epsilon_j).

Approximate same-task finite comparisons add the displayed relative budget.
The original C3 horizontal/raw vertical topology is preserved, not silently
strengthened to unrestricted raw gate-max refinement. All original linked field
tests remain, and persistent wrong field equations are not diluted by this
extension. Additional record-mixing, moving frame, report-law or other genuinely
independent directions outside this sum still require their own source.

The compact two-field handoff preserves the previous chat proof in Git: the
regular positive nonlinear branch gives Einstein with its own two constrained
scalar currents, lambda=mu/E, without an aligned-dust hypothesis. Its reverse
chart is generated by an existing timelike conserved material current. The
incoming source descent and this task theorem use the same open-field I_tau,
so their recovery construction applies to that whole declared regular sector
at the true decoder/collar/represented-data assumptions. The previous detailed
zip is retained unchanged in the user package; its original four-file patch is
not claimed to have been applied by this compact handoff.

## Literal native validation and actual execution

97 NEW checks executed; ordinary, python -O and repeat ordinary outputs are
byte-identical. Original Golden/CX/quaternion SourceI matrices are reconstructed
on all32 columns, with oldRIGHT never addressed.

* Two actual38-stage words (4G/24CX/10SourceI) from7dh have report-effect norm
difference p and prepared probability difference p^2. Perfect return changes
the real task; no new source normalization is fitted to that example.
* A different actual pair X;X;QUERY and X;QUERY;X, X=CX(port,query), has28 stages,
2G/20CX/6SourceI, identical ALL16 unprepared SOURCE output columns and distinct
full operators. Both preserve the original report task and reflection spectrum.
The dirty complement is retained, not projected away.
* Structural nonnormal-past source error <=6.51e-19; exact-effect error0;
full112-mode bare paired-clock heat comparison error0. Nine180-digit relative
error tests include singular past and gain as small as3.0e-75. All proved bounds
hold, with maximum actual/bound ratio below0.896. Classical-only equality,
small-tolerance/large-derivative and zero-gain controls are retained.

Checker SHA256 `ac1b5af37e848782060b8f686852729d401d7b48d7c1f7bff459075d59f0f180`;
Git blob `0947a2b924307e567d4426755a2ec0d51b5f8396`.
Proof SHA256 `9f2354817860f9024a597dba4bd14c0580cc021de5c473925740b46b0e8f96e5`;
Git blob `c99e90a8c8e96bae70e700fa88d1c2d824a1831b`.
Result SHA256 `811f14472baf715f4d0094914ef6af5f9fd049fa48ea401633109d2300faf2eb`;
Git blob `4b420d691a8f4bcd32513bd431fa7652ee6c8d52`.

Incoming79 checks and previous two-field97+10 checks are not counted or rerun.
No huge nonlinear native compiler, new all42 physical root, AF272 replay, Lean,
repository CI or independent scientific acceptance is claimed.

## Precise remaining physical implication

This proves a source/implementation theorem on an explicitly defined task fibre,
not that Book03's physical comparison domain must be that fibre plus G_h.
Book03 sections03.26.1–03.26.4 themselves leave port addressability, primitive
actuation and fresh-resource availability as implementation obligations. Closure
and finite coding alone do not prove them, nor do they license freeing generated
variables. No new external observer is required by the theorem, but actual task
selection/admission and any remaining independent physical rows still need proof.
No main merge, claim/lifecycle promotion or unconditional GR closure: GR_closed=false.
