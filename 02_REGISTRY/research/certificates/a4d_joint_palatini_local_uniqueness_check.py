#!/usr/bin/env python3
"""Narrow integration checks for EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS.

Research-only exact SymPy arithmetic.

This checker does NOT reproduce the delegated orbit/kernel/germ workers.
It pressure-tests only parent-level glue:
  1. the merged #227 family has a nonzero linear metric source;
  2. the abstract mixed-saddle kernel decomposition used by the parent memo;
  3. expected N0 dimensions implied by already-owned rank arithmetic, clearly
     marked as arithmetic only until the worker constructs H_QA|ker(H_AA);
  4. finite positive Hölder exponent plus a fixed polynomial loss preserves
     O(h^infty), and #226's h^-2 response loss preserves it again.

The full star-specific J1/J2/J3 results remain worker dependencies.
"""
import sympy as sp

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

# ---------------------------------------------------------------------------
# 1. #227 source-visible tangent from its exact descended metric response.
# ---------------------------------------------------------------------------
t = sp.symbols("t")
c = 4*t/(4-3*t**2)
metric_dir = sp.Matrix([0,0,0,0,-1,1,1,-1,1,-1])
check("227_C_AT_ZERO", sp.simplify(c.subs(t,0)) == 0)
check("227_C_DERIVATIVE_ONE", sp.simplify(sp.diff(c,t).subs(t,0)) == 1)
check("227_METRIC_DIRECTION_NONZERO", metric_dir != sp.zeros(10,1))
linear_metric_source = sp.simplify(sp.diff(c,t).subs(t,0)) * metric_dir
check("227_LINEAR_METRIC_SOURCE_NONZERO", linear_metric_source != sp.zeros(10,1))

# ---------------------------------------------------------------------------
# 2. Exact toy controls for the basis-independent KKT decomposition.
#    A: V->V, B: M->V, C: V->M.
#    N0 = ker A intersect ker C.
#    M0 = ker(pi B), Sigma(q)=[C v_R(q)] mod C(N).
#    The memo proves the general statement; these controls catch sign/quotient
#    implementation mistakes without pretending to be the star census.
# ---------------------------------------------------------------------------
# Example 1: V=R^3, M=R^2.
A = sp.diag(1, 1, 0)
B = sp.Matrix([[1,0],[0,0],[0,1]])
C = sp.Matrix([[0,0,1],[0,1,0]])
HJ = sp.Matrix.vstack(
    sp.Matrix.hstack(sp.zeros(2,2), C),
    sp.Matrix.hstack(B, A),
)
# N=span(e3); C(e3)=e1, so N0=0.
N = sp.Matrix.hstack(*A.nullspace())
check("KKT_TOY1_N_DIM_1", N.shape[1] == 1)
check("KKT_TOY1_N0_DIM_0", (C*N).rank() == 1)
# Direct joint nullity.
nullity1 = 5 - HJ.rank()
# Fredholm constraint pi B q=0 is third row of B: q2=0, so M0=span(q1).
# For q1, solve A v=-B q with v_R=(-1,0,0), then C v_R=0, so Sigma=0.
ker_sigma1 = 1
check("KKT_TOY1_EXTENSION_DIM", nullity1 == 0 + ker_sigma1)

# Example 2: make one pure connection invisible N0 plus one mixed null.
A2 = sp.diag(1,0,0)
B2 = sp.Matrix([[1,0],[0,1],[0,0]])
C2 = sp.Matrix([[0,0,1],[0,0,0]])
HJ2 = sp.Matrix.vstack(
    sp.Matrix.hstack(sp.zeros(2,2), C2),
    sp.Matrix.hstack(B2, A2),
)
N2 = sp.Matrix.hstack(*A2.nullspace())
# N=span(e2,e3), C|N rank1 => N0 dim1.
n0dim2 = N2.shape[1] - (C2*N2).rank()
check("KKT_TOY2_N0_DIM_1", n0dim2 == 1)
# q must satisfy pi B q=0: the e2 component forces q2=0. q1 is allowed.
# v_R=(-q1,0,0), C v_R=0, hence one mixed q direction.
ker_sigma2 = 1
nullity2 = 5 - HJ2.rank()
check("KKT_TOY2_EXTENSION_DIM", nullity2 == n0dim2 + ker_sigma2)

# ---------------------------------------------------------------------------
# 3. Already-owned rank arithmetic: provisional N0 dimensions.
#    This is not the J1 theorem; worker must construct the actual restriction.
# ---------------------------------------------------------------------------
owned = [
    # (r_H, r_aug, expected dim ker HAA, d, arithmetic N0)
    (20,24,4,4,0),
    (22,24,2,2,0),
    (22,23,2,1,1),
    (20,23,4,3,1),
    (16,20,8,4,4),
]
for rH, rA, dimN, d, dimN0 in owned:
    check(
        f"RANK_ARITH_{rH}_{rA}",
        24-rH == dimN and rA-rH == d and dimN-d == dimN0
    )

# ---------------------------------------------------------------------------
# 4. O(h^infty) survives finite Hölder rescue + polynomial losses.
# If |s_h| <= C_M h^M for every M and
# |u_h| <= C h^-p |s_h|^beta, beta>0,
# choose M > (K+p)/beta.
# Then normalized response with the #226 h^-2 loss is still O(h^K) after
# choosing two more powers in the target.
# ---------------------------------------------------------------------------
# Exact rational test battery for beta and polynomial loss.
for beta in [sp.Rational(1,2), sp.Rational(1,3), sp.Rational(2,5), sp.Rational(1,7)]:
    for p in [0,1,2,5]:
        for K in [1,2,5,10]:
            # Pick an integer M strictly above (K+p+2)/beta, where +2
            # pre-absorbs the normalized metric-response loss.
            threshold = sp.Rational(K+p+2,1)/beta
            M = int(sp.floor(threshold)) + 1
            exponent_u = sp.simplify(beta*M - p)
            exponent_resp = sp.simplify(exponent_u - 2)
            check(
                f"HOLDER_beta{beta}_p{p}_K{K}",
                exponent_resp > K
            )

print("RESULT_227_TANGENT: exact #227 metric source has nonzero first derivative.")
print("RESULT_KKT_GLUE: parent mixed-saddle quotient decomposition passes exact controls.")
print("RESULT_N0_ARITHMETIC: owned rank types give provisional 0,0,1,1,4 dimensions; J1 worker still required.")
print("RESULT_TRANSFER: finite positive Holder exponent + fixed polynomial loss + h^-2 preserves O(h^infty).")
print("SCOPE: integration checker only; no delegated orbit/germ calculation is reproduced.")
