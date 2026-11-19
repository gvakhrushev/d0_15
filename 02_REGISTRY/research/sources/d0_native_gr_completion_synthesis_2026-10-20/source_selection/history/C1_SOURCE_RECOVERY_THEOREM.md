# One original Perron path: uniform recovery of the feedback value and its first source

Research derivation, 20 October 2026. Pinned scientific source:
`41582f57ce2b4bc8c9fad322e3c2d8ecaadb8b70`.
This closes the expressly open interchange-of-derivative seam in
`02_REGISTRY/research/A4D_ONE_RECORDED_SCENE_HISTORY_CONSTRUCTS_BOOK_FEEDBACK_2026_10_19.md`,
section 4.1, by adding a bounded finite-state argument. It does not select a
physical Book action, equate its price to the configured gravitational action,
or take a spacetime continuum limit.

Reconciled against the later local scientific head
`4867b6d43b262da7e0e08b9b14a7a7a20d9a2ac4`: the original one-history owner,
including its explicit open derivative-interchange sentence at line 197, is
unchanged since the pinned input. The newer
`A4D_NATIVE_RELATIVE_HISTORY_FIRST_JET_AND_MARKED_LIMIT_2026_10_20.md`
and its `sources/d0_native_relative_history_first_jet_2026-10-20/RESULT.md`
prove a different C1 limit: complete coherent Stinespring operators W_h on
the homogeneous first-shell CAR16/oldRIGHT128 programme, under fixed or
physical h^-4 clocks and supplied bounded C1 price/readout maps. Here N is
observation length on the fixed K913 scene and the nonlinear empirical
readout is reconstructed from a classical complete label path. Neither
theorem subsumes the other's carrier, limit, or still-missing physical
valuation. The present statement does not duplicate that coherent theorem.

## Statement

Let the vertex set and directed support be the original K(9,11,13), with all
33 vertices and all 718 directed edges. On an open finite-dimensional parameter
chart U, let the edge prices s_y(e) be C^1 and

    K_y(u,v) = exp[-ell s_y(u,v)],  ell = log(phi),

be strictly positive on every original edge and zero elsewhere. Let C be a
compact subset lying inside U. Normalize the positive Perron vector by
sum_v r_y(v)=1, and put

    mu_y = r_y,
    P_y(u,v) = K_y(u,v) r_y(v)/(rho_y r_y(u)),
    pi_y P_y = pi_y,     sum_v pi_y(v)=1.

The actual path starts at mu_y, not at pi_y. Define

    T_y = D_pi^(1/2) P_y D_pi^(-1/2),
    F_y = I-T_y^T T_y,
    J_y = -log det(I-z F_y),     z=2^(-20).

Suppose pi_* := inf_{y in C,v} pi_y(v) > 8z, shrinking to a compact
neighborhood inside U if necessary. Choose ONCE, independently of y and N,

    4z < a < pi_*/2.

For each complete path gamma=(Y_0,...,Y_N), N>=1, let

    L_N(u,v) = N_uv/N,
    pi_hat(u) = sum_v L_N(u,v),
    P_hat(u,v) = L_N(u,v)/pi_hat(u).

When every pi_hat(u)>=a, form the literal recorded innovation covariance

    F_hat = (1/N) sum_{t<N} eps_hat_t eps_hat_t^T,
    eps_hat_t(i) =
      [1_{Y_(t+1)=i}-P_hat(Y_t,i)]/sqrt(pi_hat(i)).

Define the fixed complete-record statistic

    O_N(gamma) =
      -log det(I-z F_hat), if min_u pi_hat(u)>=a;
      0,                   otherwise.

Keep the failure flag and every original label. The second branch is a declared
readout value, not conditioning, rejection, resetting, erasure, or deletion of
paths. It is independent of y. The determinant is strictly positive on its
first branch because ||F_hat||<=4/a and 4z/a<1.

There are finite constants C_0,C_1, independent of y in C, N, and unit parameter
direction V, for which

    |E_y O_N - J_y| <= C_0/N,                                      (A)
    |D_y E_y O_N[V] - D_y J_y[V]| <= C_1/sqrt(N).                   (B)

The derivative in (B) has the EXACT complete one-sided source representation

    D_y E_y O_N[V] = E_y[(O_N-E_y O_N) S_N[V]],                    (C)
    S_N[V] = -ell sum_(t<N) D s_y(Y_t,Y_(t+1))[V]
             -N D log rho_y[V] + D log r_y(Y_N)[V].

Thus expected empirical feedback converges to the canonical positive feedback
in C^1, uniformly on the compact original-edge chart. This is convergence of
the derivatives of expected readouts. It is not a derivative of one frozen
histogram and does not, by itself, establish consistency or bounded variance
of a one-realization score estimator.

**Extension to every compact strictly positive original-edge chart.** The
condition pi_*>8z is needed only for the particularly simple mass-only safe
rule above, not for the convergence theorem. On an arbitrary compact positive
chart pi_*>0, choose any fixed 0<a<pi_*/2 and also require
lambda_max(F_hat)<=2 in the successful readout branch; use the same fixed zero
and retained flag otherwise. Since 2z<1, this rule is uniformly bounded and
safe. At every true stationary flow F_y satisfies 0<=F_y<=I, so the additional
cutoff is uniformly inactive in a neighborhood of all m_y. The proof below
is unchanged, with bound -33 log(1-2z). Thus the general source-recovery result
requires no small-edge-imbalance hypothesis; both cutoffs are fixed functions
of the recorded counts, independent of the differentiated parameter.

## Why these hypotheses hold on an actual original-scene chart

The support has primitive square: for any two original vertices u,v there is
an original vertex w adjacent to both. If u and v lie in different zones take
w in the third zone; if they lie in the same zone take w in either other zone.
Consequently K_y is primitive and its Perron eigenvalue is simple. Standard
finite-dimensional differentiation of the simple eigenpair gives C^1 rho,r,
P,pi on U; no new stochastic mechanism is introduced.

Compactness gives p_* := min_{y in C, (u,v) edge} P_y(u,v)>0.
Every entry of P_y^2 is at least p_*^2. Hence the two-step transition has the
uniform Doeblin minorization with mass epsilon=33 p_*^2, relative to the
uniform original-vertex law. This is a proof of uniform geometric mixing for
the actual graph, including arbitrary directed, nonreversible edge prices.
It does not assume reversibility or a conveniently chosen spectral gap.

The edge chain E_t=(Y_t,Y_(t+1)), on the actual 718 edges, has transition
R_y((u,v),(v,w))=P_y(v,w). It satisfies

    R_y^3((u,v),(a,b)) = (P_y^2)(v,a) P_y(a,b) >= p_*^3,

so it also mixes uniformly geometrically. Its stationary law is
m_y(u,v)=pi_y(u)P_y(u,v). Its initial law is the actual
mu_y(u)P_y(u,v), with its complete y dependence.

At the original equal-price scene, the owned computation gives
min_v pi(v)=0.02712452984218..., whereas 8z=0.00000762939453125.
By continuity a compact neighborhood has pi_*>0.025, so a=0.01 is one
concrete fixed safe threshold. Nothing is presumed uniform under degeneration
of an edge price, vanishing pi_*, or growth of the graph.

## Proof

Write L=L_N and m=m_y. All norms below are fixed finite-dimensional norms.
Uniform mixing of the edge chain implies the following bounds, uniformly for
the actual moving initial law:

    ||E_y L-m_y|| <= B/N,
    ||D_y(E_y L-m_y)|| <= B'/N,                                   (1)
    E_y||L-m_y||^2 <= B_2/N,
    E_y||L-m_y||^4 <= B_4/N^2.                                   (2)

Here are details sufficient to derive rather than postulate these estimates.
Put Pi_y=1 m_y and Q_y=R_y-Pi_y. Uniform Doeblin mixing gives
||Q_y^t||<=A q^t with q<1. For initial edge law alpha_y,

    E_y L-m_y = (1/N) sum_(t=0)^(N-1) (alpha_y-m_y) Q_y^t.

Bound the geometric sum for the first assertion in (1). For the derivative,
use the product rule

    D Q_y^t = sum_(j=0)^(t-1) Q_y^j (D Q_y) Q_y^(t-1-j).

The resulting norm is at most A^2 ||D Q_y|| t q^(t-1).
The sums of q^t and t q^(t-1) converge, proving the second assertion,
including D alpha_y and D m_y. This is where a moving initial distribution
is retained rather than silently frozen.

For each centered edge coordinate g_y(e)=1_{e=e0}-m_y(e0), the Poisson solution

    h_y = sum_(k>=0) R_y^k g_y

is uniformly bounded. The sum of N centered observations is a sum of N
uniformly bounded martingale differences plus a uniformly bounded endpoint
term:

    sum_(t<N) g_y(E_t)
      = h_y(E_0)-h_y(E_N)
        +sum_(t<N) [h_y(E_(t+1))-(R_y h_y)(E_t)].

The continued Markov chain is used only to prove a bound on the first N
observations; no extra observed event is required by the statistic.
The martingale second moment is O(N), and its fourth moment is O(N^2).
For completeness, the latter follows directly by expanding
(M_t+Delta_t)^4, using E[Delta_t|past]=0, bounded Delta_t,
E M_t^2=O(t), and E|M_t|<=O(sqrt(t)), and summing the resulting
O(t)+O(sqrt(t))+O(1) increment bound. Adding the bounded endpoint and summing
over 718 coordinates proves (2), without stationarity at time zero.

Let f be the fixed safe-cutoff function of empirical edge flow in the
statement. In a single uniformly sized neighborhood of all m_y it equals the
ordinary smooth logdet of the recorded covariance, since each true outgoing
mass exceeds 2a. Its second derivatives there are uniformly bounded.
On its entire domain f is bounded: 0<=f<=-33 log(1-4z/a).
Although the chosen hard cutoff need not be smooth away from the true flows,
the following global Taylor estimate still holds:

    f(L) = f(m_y) + Df(m_y)(L-m_y) + R_y(L),
    |R_y(L)| <= B_f ||L-m_y||^2.                                 (3)

Inside the fixed neighborhood this is Taylor's theorem. Outside it,
||L-m_y|| has a uniform positive lower bound, while f(L),f(m_y),Df(m_y)
and L-m_y are bounded; enlarge B_f. Also f(m_y)=J_y.
Taking expectations in (3), then (1)-(2), proves (A).

The whole finite path law is

    p_y(gamma)=mu_y(Y_0) product_(t<N) P_y(Y_t,Y_(t+1))
              =rho_y^(-N) product_(t<N) K_y(Y_t,Y_(t+1)) r_y(Y_N).

There are finitely many paths for each N. Differentiating their entire
normalized probabilities proves (C) and E_y S_N=0. The equivalent expression

    S_N = D log mu_y(Y_0)+sum_(t<N) D log P_y(Y_t,Y_(t+1))

shows that its transition summands are martingale differences, with initial
score mean zero. All their cross terms, including those with the initial
score, vanish in expectation. Compact positive-edge regularity bounds each
increment, hence

    E_y |S_N[V]|^2 <= B_s (N+1) ||V||^2.                          (4)

Insert (3) into E[f(L) S_N]. The constant contributes zero, and the linear
term is exactly Df(m_y) D_y E_y L[V]. Thus

    D E_y f(L)[V] - D J_y[V]
      = Df(m_y) D_y(E_y L-m_y)[V] + E_y[R_y(L) S_N[V]].

No derivative of the remainder or cutoff has been assumed. The first term is
O(1/N) by (1). By Cauchy-Schwarz, (2)-(4), the second is bounded by

    B_f (E||L-m_y||^4)^(1/2) (E|S_N[V]|^2)^(1/2)
      <= C sqrt(N+1)/N ||V|| = O(N^(-1/2)) ||V||.

This proves (B). No O(1/N) derivative rate is claimed by this argument.

The safe convention has no limiting-source ambiguity. Two fixed bounded
conventions agreeing with the same logdet near every m_y differ only outside
a fixed neighborhood. From (2), that event has probability O(N^-2).
Their expected values therefore differ by O(N^-2), and their exact first
sources differ by at most O(N^-1/2) using (4) and Cauchy-Schwarz.
Both recover exactly the same J and DJ. A convention depending explicitly on
y would add an E[D O_N] term and is not covered by this result.

## Exact endpoint correction at finite N

Let D_out=diag(pi_hat) and
pi_hat_in(i)=N^(-1) sum_(t<N) 1_{Y_(t+1)=i}.
Directly expanding every recorded innovation gives the exact identity

    F_hat
      = D_out^(-1/2)
          [D_in-P_hat^T D_out P_hat]
        D_out^(-1/2)
      = I-T_hat^T T_hat
        +(1/N) diag_i(
          [1_{Y_N=i}-1_{Y_0=i}]/pi_hat(i)),                       (5)

where T_hat=D_out^(1/2) P_hat D_out^(-1/2).
The last term is forced by telescoping incoming minus outgoing counts.
The empirical covariance is positive and annihilates sqrt(pi_hat) exactly.
Blindly substituting I-T_hat^T T_hat at finite N omits a genuine endpoint
and generally destroys that exact zero mode. This identity also shows why
the stationary formula is recovered in the bulk without a stationary reset.

## Source composition and precise remaining seam

The recovered analytic source is the already owned original-edge source

    DJ[V] = -2z Tr[(I-zF)^(-1) T^T DT[V]],
    DT_uv[V] = sqrt(pi_u/pi_v)
      (DP_uv[V] + P_uv (Dlog pi_u[V]-Dlog pi_v[V])/2),
    Dpi = pi DP (I-P+1pi)^(-1).

If a separately derived C^1 native coframe/link/matter map x -> s(x) is given,
the chain rule transports (B) to its compact chart, with the same convergence
rate multiplied by a bound on ||Ds||. It does not invent that map.

The genuinely new removal is: a complete original one-sided history now
recovers both the declared feedback value and its full first response in
expectation, retaining all Perron and terminal normalization sources.
The remaining physical equality is still to derive the complete selected
Book Cost-Info including preparation, recording, clock, controller and work,
then compare its field variation to the all16+24+matter configured action.
The existing positive finite GR family can consume an actual equality of
those sources; statistical C^1 recovery alone is not that equality.

N is observation time on the fixed native 33-state scene. None of the uniform
bounds claimed here are bounds in mesh size h or system volume.
