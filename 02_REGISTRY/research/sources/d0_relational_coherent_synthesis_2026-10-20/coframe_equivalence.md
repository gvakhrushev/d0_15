# Explicit all-order coframe equivalence for the complete squared-density action

This is an exact strengthening of the existing PR #334 squared-ideal owner: its finite quadratic shear is the derivative of an explicit nonlinear coframe map.

## Theorem

Let q contain the original independent nondegenerate coframes e_i, shared links and admitted matter fields. Let Z_i=e_i·∂_{e_i} be allowed independent site radial directions. Let t_i(q) obey, on a smooth chart,

    Z_i t_j=2δ_ij t_j.

Let z be internal history/preparation/clock variables independent of those radial directions. Suppose the actual action has the existing normal form

    S(q,z)=B(z)+Σ_i w_i(z)t_i(q)+t(q)ᵀ H(q,z)t(q),

where H is any smooth real matrix, possibly signed, nonlocal, nonseparable, dependent on coframe shape, matter, links and every retained history variable. Each w_i(z) is nonzero. Replace H by its symmetric part if desired; the scalar R is unchanged. Write

    a(q,z)=H(q,z)t(q),
    s_i(q,z)=sqrt(1+a_i(q,z)/w_i(z)),
    Θ(q,z): e_i ↦ s_i(q,z)e_i,

and leave every shared link, matter coordinate and z unchanged. Set S0(q,z)=B(z)+Σ_i w_i(z)t_i(q).

Then, wherever all s_i² are positive and the coframe rescaling stays within the radial homogeneity domain,

    S(q,z)=S0(Θ(q,z))                              (A)

EXACTLY, with no asymptotic remainder. Near every point of the complete t=0 shell, Θ is a smooth local diffeomorphism and fixes that shell pointwise. No rank condition on Dt, no internal Hessian inverse, and no smallness or positivity of H are needed at the shell.

## Proof

The independent commuting radial flows imply the finite scaling law

    t_i((r_j e_j)_j,U,ψ)=r_i² t_i((e_j)_j,U,ψ)

for positive r_j in the chart. For each given q,z, the numbers s_i(q,z) are fixed during evaluation of that law, even though they depend on the original fields. Consequently

    S0(Θ(q,z))=B(z)+Σ_i w_i(z)s_i(q,z)²t_i(q)
               =B(z)+Σ_i w_i(z)t_i(q)+Σ_i a_i(q,z)t_i(q)
               =S(q,z).

At any t=0 point, all s_i=1 and Θ=id. Let L=Dt on the full q tangent, W=diag(w), and Z the radial column map. Differentiating gives

    DΘ=I+N,     N=(1/2) Z W^−1 H L,
    LZ=0,      N²=0,      (DΘ)^−1=I−N,      det DΘ=1.       (B)

Here the full Jacobian includes all q and z coordinates; the z columns of N vanish because t is independent of z and factors multiplying t have zero derivative contribution on the shell. Matter columns need not vanish. The inverse function theorem gives a local diffeomorphism at every such point, including singular-Dt Einstein roots. The factors s_i stay positive in a neighborhood, so all coframes remain nondegenerate and in the same orientation/time-orientation sector.

## Exact complete source, roots, Hessian and causal-cone consequences

For every actual tangent V, including moving internal history or matter,

    dS(q,z)[V]=dS0(Θ(q,z))[DΘ(q,z)V].                       (C)

Thus all geometry, matter and internal Euler rows are transported by one invertible Jacobian. The dependence of s_i on z and matter MUST be differentiated; holding the coframe map fixed while varying those variables is incorrect. This is an exact source relation and is stronger than matching action values only on solutions.

Every critical point of S0 obeys t_i=0 by its radial equations 2w_i t_i=0. Since Θ fixes that shell, it follows on a sufficiently small chart that

    Crit S = Crit S0

as the same configurations in the original coordinates. No isolated internal B-root or invertible D²B is necessary. Existing degenerate preparation roots and entire stationary B-moduli are retained. This does not prove that such roots exist or that the physical process selects them.

At a common full stationary point,

    D²S=DΘᵀ D²S0 DΘ.                                    (D)

This is the COMPLETE geometry+matter+history Hessian before any elimination. For symmetric H, the q-block shear in (B) is exactly the existing I+(1/4)ZW^−1(H+Hᵀ)L correction. The new result integrates it to every order and avoids assuming a regular internal Schur complement merely to establish equivalence.

All stationary solution fields are unchanged because Θ=id there. Off shell each metric is multiplied by the positive scalar s_i². Hence its pointwise conformal class/null cone is unchanged. Proper interpretation of physical clock, massive matter or arbitrary fixed external probe couplings still requires their actual pullback; unchanged pointwise null cones alone are not a theorem of continuum hyperbolicity or causal convergence.

If the t_i and H_ij are gauge-invariant scalar functions and the radial fields commute with the declared gauge action, Θ is gauge-equivariant and transports the full Ward identity and gauge quotient. Gauge invariance of the scalar S alone is not permission to presume every arbitrary coefficient decomposition H has this property; use an actual equivariant decomposition or prove the corresponding map separately.

## Uniform refinement: exact budgets, not a silent locality claim

The sharp relative budget is C_h=W_h^−1H_h. Only nonzero w_i at each finite h is necessary: a common normalization making all weights small cancels in C_h. For a site supremum norm suppose uniformly in h:

    ||C_h||∞≤A_rel,       ||t||∞≤ρ_h,

and A_rel ρ_h≤η<1. Then all radicands lie in [1−η,1+η] and

    max_i |s_i−1|≤A_rel ρ_h/(1+sqrt(1−η)).

A more restrictive sufficient version is

    min_i |w_i|≥m>0,
    sup_i Σ_j |H_ij|≤A,
    ||t||∞≤ρ_h,

which implies A_rel≤A/m. In that version the same bound reads

    max_i |s_i−1|≤(Aρ_h/m)/(1+sqrt(1−η)).

Thus on a bounded smooth family with t_i=O(h²), the coframe change is O(h²) whenever A_rel is bounded, even if the common action normalization tends to zero with h. For a bounded physical variation V,

    2s_i Ds_i[V]=((DC_h[V])t+C_h Dt[V])_i.

Bounded row sums for C_h and DC_h[V], together with Dt[V]=O(h²), give Ds_i[V]=O(h²). In terms of the unnormalized coefficients this same identity is

    2s_i Ds_i[V]=Dw_i^−1[V] a_i
                  +w_i^−1((DH[V])t+H Dt[V])_i.

The separate m,A version also works with bounded derivatives of H and w and w bounded away from zero. The relative form avoids imposing an unnecessary absolute weight floor. The same method supplies second jets when the actual second-derivative budgets hold. No such conclusion follows for arbitrary microscopic link tangents, for which Dt[V] can be O(1).

An exact Jacobian test away from the shell is also small-dimensional. Let E scale only the coframe tangent blocks by s_i, and let Ds be the N×dim(q,z) derivative matrix. Then

    DΘ=E+Z Ds,
    det DΘ=det(E) det(I_N+Ds E^−1 Z).

Since E^−1Z=Z diag(1/s_i), a sufficient uniform invertibility bound is ||Ds Z diag(1/s_i)||<1 in a consistent operator norm. These are radial derivatives; they vanish on the shell and are O(ρ_h) with bounded radial coefficient derivatives. The full inverse source norm additionally requires bounds on Z and Ds. Dense nonlocal H can violate these bounds and may destroy locality even though the finite theorem remains exact.

## Actual scope gain and remaining physical input

This removes the need to match all higher microscopic history coefficients, require S=F(t), assume Dt a submersion at an Einstein root, or demand a nondegenerate preparation Hessian before establishing full source equivalence. An arbitrary already-selected squared-ideal correction has an explicit finite nonlinear coframe dressing. The physical proof that the compulsory complete Book03 action has this normal form is still required; no formal construction can infer it from observability or the action lower bound alone.

## Decisive controls

The checker uses two site coframes, a shared-link difference, a nonlinear matter contribution and a history coordinate z with B=z^4. Thus D²B=0 at the stationary point. H depends on all these fields and is not a function of t alone. It checks exact symbolic action equality via the scaling law, complete source pullback, a singular-Dt stationary root, the nilpotent unit-determinant Jacobian, and the full coupled Hessian congruence. A term nonconstant on t=0 is a hostile failure: no shell-fixing equivalence can erase its on-shell value or source. The model is a structural regression for the theorem, not a new native D0 admission claim.
