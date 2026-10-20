#!/usr/bin/env python3
"""Narrow checks of the new note, not an all40/Q8 implementation replay."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHI = (1 + math.sqrt(5)) / 2
P = 1 / PHI
Q = 4 * P**3
M = P**6
LOGPHI = math.log(PHI)
CHECK_COUNT = 0


def require(condition, description):
    global CHECK_COUNT
    CHECK_COUNT += 1
    if not condition:
        raise RuntimeError("Check failed: " + description)


def entropy(weights):
    return -sum(x * math.log(x) / LOGPHI for x in weights if x > 0)


def binary(q):
    return entropy((q, 1-q))


def e_n(s, n):
    return sum(s**j for j in range(n))


def de_n(s, n):
    return sum(j * s**(j-1) for j in range(1, n))


def stopped_law(q, n):
    return [q*(1-q)**j for j in range(n)] + [(1-q)**n]


def mix(a, rho, b, sigma):
    return tuple(a*x+b*y for x,y in zip(rho, sigma))


def block_eigs(rho):
    # Real symmetric 2x2 block (a,b,d), possibly unnormalized or rank one.
    a,b,d = rho
    disc = math.hypot(a-d, 2*b)
    hi = (a+d+disc)/2
    if hi == 0:
        return (0, 0)
    lo = (a*d-b*b)/hi
    require(lo >= -1e-14, "positive semidefinite oldRIGHT block")
    return (max(lo, 0), hi)


def complete_info(q, n, pi, rp, rm):
    minus = stopped_law(q, n)
    s_r = entropy(block_eigs(mix(1-pi, rp, pi, rm)))
    s_xr = entropy([1-pi, pi])
    s_xr += (1-pi)*entropy(block_eigs(rp)) + pi*entropy(block_eigs(rm))
    yr_eigs = []
    xyr_eigs = []
    for j,prob in enumerate(minus):
        plus_prob = float(j == n)
        yr_eigs.extend(block_eigs(mix((1-pi)*plus_prob, rp, pi*prob, rm)))
        xyr_eigs.extend((1-pi)*plus_prob*x for x in block_eigs(rp))
        xyr_eigs.extend(pi*prob*x for x in block_eigs(rm))
    s_yr = entropy(yr_eigs)
    s_xyr = entropy(xyr_eigs)
    h_yr = s_yr-s_r
    i_xyr = s_xr+s_yr-s_r-s_xyr
    return h_yr, i_xyr


def cost(q, n, pi, t):
    return (1-pi)*(t+1)*n + pi*((t+1)*e_n(1-q,n) + 1-(1-q)**n)


checks = []
require(abs(1-Q-M) < 1e-14, "q* + p^6 = 1")
require(0 < M < 1/8 and .5 < Q < 1, "Golden probability bounds")
require(binary(Q) < 2, "binary entropy below two native units")
hp = math.log((1-Q)/Q)/LOGPHI
require(-hp < 6 and hp < 0, "Golden entropy derivative bound")
checks.append("Golden algebraic and logarithmic bounds, numerical consistency")

# Coefficientwise verification, in addition to the all-N proof in the note.
for n in (2,3,7,16):
    e_coeff = [1]*n
    de_coeff = [j+1 for j in range(n-1)] + [0]
    diff = [de_coeff[j] + (de_coeff[j-1] if j else 0) - e_coeff[j]
            for j in range(n)]
    predicted = [0] + [2*j for j in range(1,n-1)] + [n-2]
    require(diff == predicted and all(x >= 0 for x in diff),
            "exact polynomial coefficients at cap " + str(n))
checks.append("Exact finite polynomial coefficients for E <= (1+s) E'")

max_noise_error = 0
max_derivative_error = 0
for n in (2,3,8):
    direct = entropy(stopped_law(Q,n))
    formula = binary(Q)*e_n(M,n)
    max_noise_error = max(max_noise_error, abs(direct-formula))
    require(abs(direct-formula) < 2e-12, "stopped entropy chain rule")
    analytical = hp*e_n(M,n) - binary(Q)*de_n(M,n)
    step = 1e-6
    numeric = (entropy(stopped_law(Q+step,n))-
               entropy(stopped_law(Q-step,n)))/(2*step)
    max_derivative_error = max(max_derivative_error, abs(numeric-analytical))
    require(abs(numeric-analytical) < 2e-7 and analytical < 0,
            "independent numerical and analytic noise sources")
checks.append("Direct terminal-word entropy and independent finite-difference noise source")

states = [
    ((1.,0.,0.), (1.,0.,0.)),       # No side information about X.
    ((1.,0.,0.), (0.,0.,1.)),       # R knows X exactly.
    ((1.,0.,0.), (.5,.5,.5)),       # Noncommuting rank-one oldRIGHT states.
    ((.8,0.,.2), (.5,.3,.5)),       # Noncommuting mixed oldRIGHT states.
]
quantum_checks = 0
max_conditional_error = 0
max_pointer_derivative = -math.inf
for n in (2,3,8):
    for pi in (.2,.7,1.):
        for rp,rm in states:
            hy,i = complete_info(Q,n,pi,rp,rm)
            target = pi*binary(Q)*e_n(M,n)
            error = abs(hy-i-target)
            max_conditional_error = max(max_conditional_error,error)
            require(error < 2e-12, "complete conditional noise defect")
            step = 1e-6
            upper_h,upper_i = complete_info(Q+step,n,pi,rp,rm)
            lower_h,lower_i = complete_info(Q-step,n,pi,rp,rm)
            gain_d = (cost(Q+step,n,pi,14)-upper_i-
                      cost(Q-step,n,pi,14)+lower_i)/(2*step)
            pointer_d = (cost(Q+step,n,pi,14)-upper_h-
                         cost(Q-step,n,pi,14)+lower_h)/(2*step)
            require(gain_d < 0, "paid task information source sign")
            require(pointer_d < -6*pi, "paid conditional-pointer source gap")
            max_pointer_derivative = max(max_pointer_derivative,pointer_d)
            quantum_checks += 1
checks.append("Conditional entropy defect and T=14 paid source for explicit cq oldRIGHT states")

result = {
    "status": "PASS",
    "scope": "New finite conditional-noise support only; general proofs are analytic",
    "output_policy": "Read-only checker; stdout receipt only; no expected result is written",
    "active_require_calls": CHECK_COUNT,
    "checks": checks,
    "cq_examples": quantum_checks,
    "max_direct_noise_entropy_error": max_noise_error,
    "max_noise_derivative_error": max_derivative_error,
    "max_conditional_defect_error": max_conditional_error,
    "max_pointer_q_derivative_at_T14": max_pointer_derivative,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "note_sha256": hashlib.sha256((HERE/"CONDITIONAL_NOISE_SOURCE_NOTE.md").read_bytes()).hexdigest(),
}
print(json.dumps(result, indent=2))
