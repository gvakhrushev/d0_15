# Independent mathematical review for the existing #334 synthesis

Reviewer: metric-source synthesis subagent. Date: 20 October 2026.
Read-only review; no repository changes or physical scope promotion.

## 1. C1 source recovery from one complete moving Perron law — accepted

Reviewed:
`../history/C1_SOURCE_RECOVERY_THEOREM.md`.
Its pinned source is `41582f57ce2b4bc8c9fad322e3c2d8ecaadb8b70`; the source
owner's Section 4.1 was inspected directly. That section indeed leaves
convergence of derivatives of expected finite-history estimators open.
The new theorem addresses that particular mathematical seam.

No load-bearing defect was found.

The moving initial law mu_y=r_y is kept. Telescoping the true Doob
transitions gives the exact complete path law

    p_y(gamma)=rho_y^-N product_edges K_y(e) r_y(Y_N),

with sum r_y=1. Its score includes both Perron pressure and the terminal
Perron-vector derivative. The equivalent initial-score plus transition-score
representation gives martingale increments; all cross expectations vanish,
including those with the initial score. The O(N) second-moment score bound
therefore holds for the actual moving start.

The positive complete tripartite support has P² uniformly positive on each
compact positive-edge chart, and the 718-edge chain has a uniformly positive
third power. Differentiation of its geometric powers is legitimate with C1
native prices: DQ^t is bounded by a constant times t q^(t-1). The resulting
derivative of the empirical-flow mean bias is O(N^-1). No native second
derivatives are needed.

The fixed hard cutoff is not a differentiation defect. Each finite complete
path has a parameter-independent reported statistic, and the finite law is
differentiable. A uniformly safe neighborhood of the true stationary flows
has the smooth logdet readout; outside it the statistic is bounded and the
distance is bounded below. These two facts give the stated global quadratic
Taylor remainder without differentiating a discontinuous cutoff.

The bounded Poisson solution and martingale decomposition justify the fourth
moment O(N^-2) for the empirical-flow deviation, including the nonstationary
initial endpoint. Cauchy–Schwarz with the O(N) score second moment yields
the claimed O(N^-1/2) source error. The proof does not claim a faster rate.

The exact empirical innovation endpoint correction is correct:

    Fhat=I-That^T That
       +(1/N)diag((1_YN-1_Y0)/pihat).

It preserves the exact sqrt(pihat) zero mode. Omitting it can destroy that
mode. The additional lambda_max(Fhat)<=2 cutoff proposed for arbitrary
compact positive charts is uniformly inactive near F_y<=I and is safe
because 2z<1.

Acceptance is for uniform C1 convergence of **expected readouts** on the
declared fixed finite graph. It does not establish consistent estimation of
the derivative from one realized path, identify the actual selected price,
construct the coframe/clock source map, or supply an h/volume-uniform limit.

## 2. Full-price repartition and moving conditional averages — accepted with typing boundary

For the fixed operator G and price

    G=s_c I+delta E+R,             S=Tr(rho G)+W,

the transformation

    s_c'=s_c+a, delta'=delta+b, R'=R-aI-bE

leaves G, S and the complete differential exactly unchanged pointwise. In
particular,

    dS=Tr((d rho)G)+Tr(rho dG)+dW,
    dR'=dR-(da)I-(db)E-b dE

in a fixed local trivialization. Every term is required. The operator
identity does not require Tr rho=1; rewriting the scalar contribution as
just s_c does require normalized rho.

Its force is a freedom of describing one operator, not evidence for several
physically admitted prices. If the native construction already fixes the
components separately, repartitioning them is not a new physical operation.
Tests on R alone require that fixed split and its full moving source.

For a linear idempotent M, Mr=c is solvable exactly when Mc=c, and the
complete mathematical solution set is c+ker M. Nonuniqueness requires a
nonzero kernel and additional physical constraints must not already exclude
it. With moving M_y, differentiation gives

    (D M_y)r_y+M_y D r_y=D c_y.

Equivalently, a conditional average has

    d sum_gamma w_gamma r_gamma
       =sum_gamma w_gamma dr_gamma+sum_gamma r_gamma dw_gamma.

The second term cannot be omitted. For r=(1,-1) and w=(p,1-p), dr=0 but
d E_w r=2 dp. Conversely, if the complete average equality holds throughout
a neighborhood, its full source equality does follow; one must not claim
an ambiguity after that stronger identity has been proved.

## 3. Prospective G^k selection theorem — accepted in its stated programme family

Reviewed:
`../records/PROSPECTIVE_SELECTION_4867.md`
and its `check_prospective_selection.py`; also the actual
`book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md` at
`4867b6d43b262da7e0e08b9b14a7a7a20d9a2ac4`.

The simultaneous pointer conditions are correctly characterized by

    delta_star < delta < A,
    delta_star=(1+D2)/(q2-q1), A=4+log_phi4,

when the actual primitive cost per G is one tick. The lower endpoint ties
k=1 and k=2; at the upper endpoint k=2 remains the unique programme minimum
but its complete first source vanishes.

The all-k proof is sound: the binary Gibbs bound holds for every q in [0,1],
and q_*(A)=q2 makes g'(delta)=q2-q_*(delta)>=0 below A. The exact estimates
delta_star>4 and g(4)>1/2 then exclude every k>=3. The exact threshold
inequalities give precisely the integer opportunities delta=5,6.

The coherent-cut proof is also correct: beating k=0 forces delta>1+2/q2,
and therefore reverses the sign of its first-source factor 1-delta.
At delta=4 the uniform all-k>=3 bound 1-3p^6 is strictly positive.

The continuation source must be included:

    dS_ptr,2=kappa(A-delta)dt.

If actual conditional prices move with fields, their additional weighted
derivatives remain. A common programme-independent extra price cannot alter
selection. The fixed bit-only task/conditional-information accounting is a
hypothesis, not a constructed native obligation.

One wording clarification was requested from the author: put ell_G=1
directly in the sharp theorem and integer-cost consequence, since the earlier
comparison table allows general ell_G. The stronger exact compiler
consequence is proved in `COMPILER_TICK_COROLLARY.md`: under actual integer
compiler and deterministic integer continuation costs, ell_G=1 is necessary;
for ell_G>=2 no positive-source integer opportunity survives.

## 4. Precisely permitted Einstein–CAR consumption

Under the unchanged full original J2 query, fixed F*, full trace
multiplicities, actual fixed primitive compiler/clock, prescribed clean work,
fixed oldRIGHT marginal, and stated conditional future-price contract,

    dS_selected|Sigma
        =kappa(A-delta) gamma_h dJ2|Sigma.

The original independent 16+24+2 stationary equations and coupling ratio
lambda=b_J/a_J are preserved. Actual source terms of the intermediate J2
query are not replaced with a standalone gravitational reporter. Generated
intermediate state/adjoint equations use the existing causal elimination;
independent upstream preparation, apparatus/observer, boundary and clock
variables keep their own equations.

The theorem compares discrete programme labels at fixed fields. It does not
prove a minimum in physical fields, identify the unrestricted transverse
Hessian, select a global minimum over other programmes, or establish the
physical source normalization as h varies. Source equality only on Sigma
does not suffice for those stronger claims.

The fixed-prefix theorem above is a different task from the stopped reporter.
The adaptive extension of the latter is independently reviewed in Section 6;
its fixed-k minimum on T0 in [5,50] is an input from the stopped owner.

## 5. Narrow reproducibility

`check_compiler_ticks.py` checks the exact Golden algebra and rational/surd
inequality certificates used in the compiler corollary. It does not enumerate
an unbounded programme set or stand in for the Gibbs proof.

## 6. Exact scalar ports and adaptive stopped price — accepted conditionally

Reviewed the final
`../records/STOPPED_ADAPTIVE_EXTENSION.md`
and its `check_adaptive_stopping.py`. The document SHA-256 at review was
`b63198714ca89df194ff0effe7b821ce402c886a4def2fb0342ffe7d4ab17d9e`;
the checker SHA-256 was
`0bdb656577f437afcf49f86688915ebff62ea541882872bdc8117cbee3d5be9c`.
No load-bearing defect remains in this extension under its declared contract.
The review takes the owner's strict fixed-k minimum on 5<=T0<=50 as input;
the full all-k stopped minimum is not independently reproved here.

The complete port effects are scalar at every point of the real compression
chart, not just to first order at Sigma. Orthogonality of J and QWJ eliminates
the cross terms, and (QWJ)*(QWJ)=(1-t²)I gives

    K_b* K_b=q_b(t)I,
    q_1=(s f0+c f1)²+4c²t⁴(1-t²),
    r=4t⁴(1-t²).

These identities hold for arbitrary normalized logical inputs entangled with
oldRIGHT and retained earlier work. Fresh repetitions therefore have the
stated conditional port probability even though the conditional logical
state and the fine work-address distribution can change. The scalar port
identity does not imply scalarization of the complete fine-pointer value.

The entropy correction is bounded uniformly in k, reached history and input:

    0<=beta_h<=B(t)=h_phi(r)+r log_phi N_g
                   =O(t⁴ |log|t||).

For the optional oldRIGHT information cut, its initial marginal is fixed and
its entropy is a common baseline. At each history scalar port effects make
the port independent of the conditional reference state. The remaining
increment is classical conditional quantum entropy H(w|b,h,R), which lies
between zero and H(w|b,h). Thus the same bound applies. It would be incorrect
to apply this argument to an arbitrary coherent information algebra, a
moving reference baseline, or an additional independently charged ledger.

For the permitted deterministic history-adaptive policies, almost-sure
stopping gives sum_h s_h q_h=1. Hence the coarse nonentropy cost obeys

    sum_h s_h a_k >= min_{k:q_k>0} a_k/q_k = R(t),
    a_k=T0+k+D_phi(Bern(q_k)||Bern(p²)) >= T0.

At t=0 there is no fine-work entropy and every k=0 node has positive cost
without termination probability. The fixed-k strict minimum at k=2 therefore
extends to every allowed adaptive policy. Equality forces k=2 at every
positive-probability reached node and zero additional scheduler cost.
Policies may still differ on impossible fine-work histories.

The important envelope step does not require a uniform policy gap or uniform
bound on expected running time over policies:

    S_policy >= (1-B(t)/T0) sum_h s_h a_k
             >= (1-B(t)/T0)R(t).

Finite expected actual cost for each admitted policy is enough to justify its
tree entropy chain rule. Nonnegative extra scheduler costs preserve this
lower bound. Near zero, the ratio lower bound a_k/q_k>=T0+k reduces the
possible fixed-action competitors to finitely many. Their strict gaps
persist, and the k=0 ratio diverges. Thus R(t)=R_2(t) locally. The fixed
k=2 controller, fully included in T0, supplies the complementary upper bound.

The author incorporated the requested notation correction: the complete
optimized value is V(y,rho), not V(t). Fine work can depend on the full query
and logical preparation beyond t. The conclusion is the uniform estimate

    (1-B(t(y))/T0)R_2(t(y)) <= V(y,rho) <= R_2(t(y)).

For smooth t(y) vanishing at y0 this remainder is o(||(y,rho)-(y0,rho0)||).
Consequently the optimized value has a genuine full Frechet derivative at
Sigma, even if the infimum is unattained nearby and rare-garbage policies
improve the exact price away from Sigma:

    dV|Sigma=-(T0-3)/(2p^(3/2)) dt
            =-(T0-3)/(2p^(3/2)) gamma_h dJ2.

The narrow checker was independently run successfully. Its T0=5 derivative
is -2.058171027271492; a central difference gives -2.0581710273859244.
The source coefficient in the original stopped document is therefore
consistent; the cited original checker target -2/p^(3/2) is a factor-two
expected-value error at T0=5, where the target is -1/p^(3/2).
Finite-schedule checks support the algebra, while the infinite-policy and
optimized-value statements rely on the proof above.

This is conditional on the same primitive, prefix, fixed reference, fresh
work and complete classical-pointer/cq information contract; unit G cost;
5<=T0<=50; first-port1 stopping; and deterministic policies choosing only k.
No other controls, changed query, abort, outcome selection, reset, free
unrecorded randomness, unpriced scheduler computation or extra entropy
rebates are included. The actual complete physical compiler and T0 interval
remain unbound. The task is prospective rather than derived as compulsory.
The full original J2 first source and stationary 16+24+2 equations transport
only with their existing remaining-ledger hypotheses; neither field Hessian,
field minimum, physical h-normalization nor positive GR selection follows.
