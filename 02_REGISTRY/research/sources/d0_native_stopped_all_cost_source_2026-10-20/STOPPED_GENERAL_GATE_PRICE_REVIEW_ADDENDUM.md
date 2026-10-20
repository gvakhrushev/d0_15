# Independent addendum: arbitrary fixed Golden-gate price ell >= 1

Reviewer: `cost_variation`, bounded read-only review inside existing PR #334.
Date: 20 October 2026. No published or repository files were modified.

This extends the independently reviewed all-prefix theorem and its uniform
B bound. The previous review/addendum remain unchanged:

* `STOPPED_ALL_PREFIX_SECOND_REVIEW.md`, SHA-256
  `c9734b128e631226e37e1208adaa930ae8c2d96d28c0b35285c21b32f74c5ea0`.
* `STOPPED_ALL_PREFIX_REVIEW_ADDENDUM.md`, SHA-256
  `d1ed274cf2696fd65094b4ac398d93b8ba4f8af7f8b7cb4844695d9b7d341979`.

## Verdict and statement

**Accepted.** The unit-price hypothesis can be weakened to every finite
real constant ell>=1 while retaining the same stopped pointer model and
the actual linear per-attempt prefix T+k ell. For every real T>=5 and
ell>=1 a minimum exists, and each minimizing branch satisfies

    B_k(T,ell)>=2,
    -B_k(T,ell) q'_k/q_k^2 != 0.

For 5<=T<=50 the unique minimizing branch remains k=2 for every ell>=1.
For T>=50 the uniform estimate is stronger: each minimizing branch has
B_k(T,ell)>17. No all-T uniqueness is claimed.

Here

    S_k(T,ell) = [T+k ell+D_phi(Bern(q_k)||Bern(p^2))]/q_k,
    B_k(T,ell) = T+k ell+log_phi[(1-q_k)/p].

T and ell are fixed, field-independent costs for the first-variation
calculation. The complete stopped record and q_k are unchanged.

## 1. The extra gate-price term favours k=2 globally

Set h_k=k/q_k. The actual Golden q_k are strictly between zero and one.
The already proved q_2>12/13 gives

    h_2=2/q_2<13/6<3.

For every k>=3, h_k>k>=3>h_2. For k=1,

    h_1-h_2 = 1/p^2-2/(4p^3)
            = (2p-1)/(2p^3)>0.

Therefore k=2 is the unique global minimizer of h_k over all k>=1.
No arbitrary cap on k is involved.

The identity

    S_k(T,ell)=S_k(T,1)+(ell-1)h_k

is exact. If k minimizes S(T,ell), comparison with branch 2 gives

    S_k(T,1)-S_2(T,1)
       <= (ell-1)(h_2-h_k) <= 0.                       (A)

For ell>1 and k!=2 the final inequality is strict. Crucially, (A) says
only that k lies in the branch-2 sublevel set for the unit-price score.
It does not say that k minimizes that score. The earlier tail proof
needs precisely this weaker sublevel condition.

## 2. Minima exist, and the previous all-prefix bounds transport

Since D_phi>=0, q_k<1, and ell>=1,

    S_k(T,ell)>T+k ell>=T+k,

so S_k tends to infinity with k and a minimum is attained.

For 5<=T<=50, the inherited unit-price theorem makes S_k(T,1)>S_2(T,1)
for every k!=2. Adding (ell-1)(h_k-h_2)>=0 preserves strict ordering.
Thus k=2 remains the unique minimum, and

    B_2(T,ell)=T+2ell-5>=2.

For T>=50, (A) and the already checked bounds D_2<2, q_2>12/13 yield

    T+k<=S_k(T,1)<=S_2(T,1)<13(T+4)/12,
    k<T/12+13/3.

The algebraic norm bound r_k=1-q_k>p^(5k) gives

    B_k(T,ell)=B_k(T,1)+k(ell-1)
             >=B_k(T,1)>T-4k+1>(2T-49)/3>=17.

All relevant inequalities at the final endpoint remain strict. Together
the two ranges prove B_k(T,ell)>=2 for every minimizing branch and every
T>=5, ell>=1. The bound is sharp at T=5, ell=1, k=2.

## 3. Source and scope

For each fixed admitted branch, the original stopped first-jet identity
becomes

    D S_k = -B_k(T,ell) q'_k/q_k^2 Dt.

The already proved irrationality of theta/pi ensures q'_k!=0. Hence the
source multiplier is nonzero on every minimizing branch. In particular,
on the uniquely selected branch 2 for 5<=T<=50,

    D S_2 = -(T+2ell-5)/(2p^(3/2)) Dt.

The earlier active-branch argument at a genuine local minimum of the
complete stipulated objective applies unchanged, including ties and the
explicit full-variation/local-admissibility conditions.

This extension removes the requirement that one Golden gate cost exactly
one tick. It requires a fixed linear charge ell>=1, and does not establish
that actual compiled costs have this form, are independent of the field,
or exhaust all moving native costs. A field-dependent T or ell would add
its own source, which is outside this statement. The stopping-task and
pointer-information assumptions remain unchanged. No additional search,
claim of physical selection, or new checker execution is included.
