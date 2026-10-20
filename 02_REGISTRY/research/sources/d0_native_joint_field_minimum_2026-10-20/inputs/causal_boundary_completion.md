# Causal elimination on the actual retained programme, with its actual initial boundary

20 October 2026. Existing PR #334 / `native-programme-v1`. This result
composes the new complete CAR source with the internal-state clause of
the original all40 theorem, rather than introducing a different action.
Input commit: `acfe3e19ecda5f2dbc678ec52e2f7cd0f3e639a1`.

## 1. Which variables are genuinely independent

Fix one actual finite programme, its complete initial record, its task,
its allowed field parameters `y`, and its actual clock `N`. Comparisons
between different programmes or clocks are a separate prospective problem.
The initial data preparation is a matrix `M` with the original fixed
oldRIGHT Gram constraint

    M* M = I_128 / 128.                                      (1)

Thus `Tr M*M=1`; no oldRIGHT column is dropped. Let `i` inject the
actually specified initial work/record state, and let `V_k(y)` be the
actual admitted isometry at tick `k`, with **all** its outgoing records
retained. Equivalently, use its full unitary implementation with the
specified incoming blank registers. Put

    X_0 = i M,
    X_(k+1) = V_k(y) X_k,       k=0,...,N-1.                 (2)

There are two different variations here. An intermediate executed state
is constrained by (2). A freely selectable initial preparation or physical
apparatus parameter is an independent choice, and its price/source must
be varied. The actual input blank record is fixed only when it really is
part of the complete boundary conditions of this particular task. This
does not prove that supplying that blank, its controller, or the programme
is compulsory or free.

No source is removed by calling an independently selectable variable a
boundary datum. If `i=i(y,z)` is a variable preparation circuit, its
derivative and its real price remain below; if `z` is freely selectable,
its Euler equation remains as well.

## 2. Exact elimination, including the adjoint equations

For clarity first take the actual supplied finite price to be quadratic
in the executed states,

    J(y,X,M) = sum_(k=0)^N Tr(X_k* O_k(y) X_k) + W(y,M),     (3)

where each `O_k` is Hermitian. In particular, a full per-history price
table is one diagonal terminal operator on the retained tape; failures,
work outcomes and all other records stay in that operator. `W` contains
the remaining actual boundary/work price. Equation (3) is a hypothesis
on the actual aggregation, not a claim that Book03 selects expectation
over its amplitude/feedback alternatives.

Introduce multipliers solely to calculate the price subject to the
already given physical execution constraints:

    L = J + 2 Re sum_(k=0)^(N-1)
                   Tr Lambda_(k+1)* (X_(k+1)-V_k X_k).      (4)

The added expression is identically zero on every actual execution.
It is not a new Cost-Info term, physical controller, counterterm, or
additional selection law.

**Theorem 1 (causal internal-state elimination).** For every admitted
programme (2) and price (3), all independently introduced intermediate
state Euler equations have the unique backward solution

    P_N = O_N X_N,
    P_k = O_k X_k + V_k* P_(k+1),       k=N-1,...,0,
    Lambda_k = -P_k,                  k=1,...,N.            (5)

After this solution, the remaining field source is exactly

    dJ_reduced = sum_k Tr(X_k* dO_k X_k)
       + 2 Re sum_(k=0)^(N-1) Tr P_(k+1)* (dV_k) X_k
       + 2 Re Tr P_0* (di) M + dW                          (6)

at fixed `M`. Thus differentiating the complete executed programme is
the full source after elimination of these causal states. A determinant
of an internal clock block is not used to declare the price zero.

**Proof.** The terminal variation of (4) gives
`O_N X_N+Lambda_N=0`. Each interior variation gives
`O_k X_k+Lambda_k-V_k*Lambda_(k+1)=0`, which is exactly (5).
The multiplier equations give (2). Substitution into the explicit field
variation of (4) yields (6). Alternatively, differentiate (2) forward;
the sum in the differential of (3) telescopes against (5), giving the
same formula. No inverse spectral gap, Hessian positivity,
or asymptotic expansion is required. The same backward argument works
for a differentiable nonquadratic actual price after replacing
`O_k X_k` by its actual state gradient; that gradient must be supplied.

For fixed `i`, define `U_0=I`, `U_k=V_(k-1)...V_0` and

    G(y) = i* [sum_k U_k* O_k(y) U_k] i.

Then `J_reduced=Tr M*G(y)M+W(y,M)`. For a single terminal price on a
complete instrument this is precisely

    G = sum_omega s_omega K_omega* K_omega,                  (7)

the price effect in `book_source/BOOK_SOURCE_BINDING.md`, with the
same retained record, rather than a second effective action.

## 3. The preparation equation on the admitted input fibre

**Theorem 2.** If `G=g_0 I` at the actual field point, and all additional
explicit preparation source in `G` or `W` is zero, then every `M`
satisfying (1) solves its constrained input-preparation Euler equation.

Indeed, its differential is

    2 Re Tr (delta M)* G M
       = g_0 Tr delta(M*M) = 0.                             (8)

The Gram multiplier can equivalently be chosen `-g_0 I_128`.
The derivative of `g_0` in a field direction is not removed. In particular,
on a common-null stratum one may have

    G=g_0 I,
    dG = (a_h d sum_z fhat_z + b_h d sum_z q_z) I,           (9)

on all 16+24+2 field directions, with a nonzero geometric source on
transverse variations. The geometric amplitude alone supplies the 16+24
slot; the two matter rows require their actual supplied price as well. In the
absence of remaining `dW`, equations (5), (8), (9) solve precisely the
causal-state and admitted-input-preparation part of the internal Euler
premise in all40 §5.1. They do not solve independent apparatus, observer,
code, task, clock or explicit information-gain variations by relabeling
them as causal states.

The actual new scalar coherent CAR port, with its fixed clean input work
record and complete retained output, supplies (8) for its **known port
Cost component**. For the whole Cost-Info effect the actual residual
`R`, its preparation dependence and `W` in the companion proof must
still be included. The theorem is exact at every finite clock; there is
no uniform-gap assumption hidden in a refinement limit.

## 4. Why this does not contradict full-work preparation stationarity

Let `U(y)` be a full unitary, `O` a fixed full-output price operator and
`E=U*OU`. If the **entire** input work/data state `rho` can independently
vary along its whole unitary orbit, preparation stationarity implies
`[rho,E]=0`. Writing `A=U* dU`,

    dE = [E,A],
    Tr rho dE = Tr [rho,E] A = 0.                           (10)

This genuine obstruction applies to that larger preparation problem.
It cannot be discarded when the full work preparation is truly free.
It also cannot be imposed on the different fixed-initial-record problem
(1)-(2) without changing the comparison class of histories.

For example, with a work qubit initially `|0>` and an arbitrary data
state, let `U` rotate the work qubit by angle `theta`, and let `O` read
its `|1>` outcome, retaining both outcomes. The compressed input effect
is `sin(theta)^2 I`. Every normalized data preparation is stationary,
while its field source is `sin(2 theta) dtheta`. The fixed initial work
record has not become a freely minimized work preparation. If producing
or choosing that record belongs to the task, its upstream process and
price must be included before any full physical conclusion.

## 5. Literal application, not an additional geometric campaign

Use the original all40 proof, §5.1, equation (18), and the existing
midpoint common-metric recovery. On its whole common-null Brinkmann
carrier the companion `geometric_source` proof produces an actual
CAR amplitude with

    A_rs = 0,
    dA_rs = nu^2 h^2 d fhat_rs

on all 16 coframe and 24 proper-link directions. The complete Golden
port then has the known Cost source coefficient `p^3 sigma nu^2 h^2`.
This is the literal geometry source slot, before applying the Cartan
equations; it is not just a Taylor coefficient at a flat example.

For any **actually supplied complete price** satisfying (9) with
site-independent derived coefficients, `a_h != 0`, and with every truly
independent remaining internal source solved, Theorems 1-2 remove the
causal-state and input-preparation placeholders. The owned all40 theorem
then gives, without another geometric proof,

    K_a(u,x) = [H(u+h,x)-H(u+h,x-h e_a)]/2,
    Delta_h^perp H(u+h) = -4 (b_h/a_h) |D_u^+ Psi|^2.        (11)

For `b_h/a_h=lambda_-(2^-20)` this consumes the literal configured
nonvacuum midpoint family on every mesh, and its already proved `O(h^2)`
matter recovery. A different derived ratio has its corresponding sourced
family; it is not the identical configured representative. In particular,
one must not simply add a new reporting Cost to the old action and retain
its old ratio without recalculating the total coefficients.

The remaining physical problem is now at the actual programme interface:
the complete Book amplitude/Info/work valuation, admission and prospective
selection of the same programme, and any genuinely independent upstream
preparations. Equation (11) is consumed once those conditions hold; it is
not evidence that they hold. No new claim, assembly acceptance, or physical
GR closure is asserted by this constrained-calculus completion.
