"""Narrow exact controls for the general adaptive stopped envelope.

The all-policy and local-minimum statements are analytical in the companion
document. This check does not scan a finite set and label it an all-k proof.
"""
import json
import sympy as sp


def require(condition, name):
    if not bool(condition):
        raise RuntimeError(name)


p = (sp.sqrt(5) - 1) / 2
phi = 1 / p
q2 = 4 * p**3
require(sp.simplify(p * p + p - 1) == 0, "Golden polynomial")
require(sp.simplify(1 - q2 - p**6) == 0, "branch-2 failure probability")
require(sp.simplify(p + 4 * phi**2 - phi**5) == 0, "Gibbs partition phi^5")
require(sp.simplify(4 * phi**2 / phi**5 - q2) == 0, "Gibbs minimizer q2")
require(phi**3 > 4, "A0=4+log_phi4<7")
require(p**2 < sp.Rational(1, 2), "q1<1/2")

# General fixed-cost derivative identity, using positive symbolic reference.
q = sp.symbols("q", positive=True)
ref = sp.symbols("p_ref", positive=True)
log_phi = sp.symbols("log_phi", positive=True)
T, ell, k = sp.symbols("T ell k", positive=True)
D = ((1 - q) * sp.log((1 - q) / ref)
     + q * sp.log(q / ref**2)) / log_phi
derivative_residual = sp.diff((T + k * ell + D) / q, q)
derivative_residual += (T + k * ell + sp.log((1 - q) / ref) / log_phi) / q**2
require(sp.simplify(derivative_residual) == 0, "general stopped derivative")

# Finite active bound: if the fixed-2 comparison is bounded by C, any
# k>(C-T)/ell has a_k/q_k>=T+k*ell>C, since D>=0 and 0<q_k<=1.
C = sp.symbols("C", positive=True)
excess_k = sp.symbols("excess_k", positive=True)
candidate_cutoff = (C - T) / ell
tail_gap = sp.expand(T + ell * (candidate_cutoff + excess_k) - C)
require(tail_gap == ell * excess_k, "finite candidate cutoff gap")
tt = sp.symbols("t", real=True)
q0 = 4 * tt**2 * (1 - tt**2)
require(sp.limit(T / q0, tt, 0, dir="+") == sp.oo,
        "k0 ratio diverges near Sigma")
# Per-node multiplicative bound with a=T+A, beta=B-b.
B, A_surplus, b_slack = sp.symbols("B A_surplus b_slack", nonnegative=True)
a = T + A_surplus
beta = B - b_slack
residual = sp.expand(a - beta - (1 - B / T) * a)
require(sp.simplify(residual - b_slack - B * A_surplus / T) == 0,
        "multiplicative entropy lower bound")

# Exact zero-source optimizer control T=3, ell=1, k=2.
B2 = T + 2 * ell - 5
require(B2.subs({T: 3, ell: 1}) == 0, "source zero at positive costs")
L = sp.symbols("L", real=True)  # L=log_phi4.
D2 = q2 * (4 + L) - 5
R2_at_control = (5 + D2) / q2
require(sp.simplify(R2_at_control - (4 + L)) == 0, "R2=A0")
# The companion Gibbs proof bounds every k>=3 by (k-2)/q_k>0.
require(sp.simplify(3 + k - 5 - (k - 2)) == 0, "all-k Gibbs cost difference")

# Why a convex hull is not deterministic schedule realizability:
# with two success probabilities 9/10 and slopes -1,+1, the first action
# restricts every schedule to [-1,-4/5] or [4/5,1].
q_a = sp.Rational(9, 10)
kappa_a, kappa_b = -sp.S.One, sp.S.One
negative_upper = q_a * kappa_a + (1 - q_a) * kappa_b
positive_lower = q_a * kappa_b + (1 - q_a) * kappa_a
require(negative_upper == -sp.Rational(4, 5), "negative first-action bound")
require(positive_lower == sp.Rational(4, 5), "positive first-action bound")

print(json.dumps({
    "status": "PASS",
    "general_cost_derivative": True,
    "finite_candidate_bound": "k>(C-T)/ell implies score>C",
    "zero_action_divergence": True,
    "multiplicative_entropy_bound": True,
    "exact_positive_cost_zero_source_unique_optimizer": {
        "T": 3, "ell": 1, "optimizer": 2,
        "all_k_proof": "Gibbs inequality in companion section 5",
    },
    "abstract_deterministic_hull_control": {
        "negative_upper": str(negative_upper),
        "positive_lower": str(positive_lower),
        "not_claimed_as_Golden_tie": True,
    },
    "scope": "Narrow symbolic controls; no physical task/price selection.",
}, indent=2))
