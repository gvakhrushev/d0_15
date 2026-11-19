"""Golden feedback: exact algebraic controls and 70-decimal matrix examples.

Run with Python 3, SymPy, and mpmath. All logs are natural.
"""
import json
from fractions import Fraction
import mpmath as mp
import sympy as sp

mp.mp.dps = 70
TOL = mp.mpf("1e-55")


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def trace(x):
    return sum(x[i, i] for i in range(x.rows)).real


def log_pd(x):
    eig, u = mp.eighe(x)
    require(min(eig) > 0, "reference must be strictly positive")
    return u * mp.diag([mp.log(t) for t in eig]) * u.H


def relative_entropy(rho, sigma):
    ev = mp.eighe(rho, eigvals_only=True)
    require(min(ev) >= -TOL, "density must be positive semidefinite")
    entropy_term = sum(t * mp.log(t) for t in ev if t > TOL)
    return entropy_term - trace(rho * log_pd(sigma))


def with_flag(block, value):
    result = mp.matrix(block.rows + 1)
    for i in range(block.rows):
        for j in range(block.cols):
            result[i, j] = block[i, j]
    result[block.rows, block.cols] = value
    return result


def unitary(n, turns):
    result = mp.eye(n)
    for i, j, theta, phase in turns:
        c, s = mp.cos(theta), mp.sin(theta)
        phase_factor = mp.exp(mp.j * phase)
        rotation = mp.eye(n)
        rotation[i, i] = rotation[j, j] = c
        rotation[i, j] = -phase_factor.conjugate() * s
        rotation[j, i] = phase_factor * s
        result = rotation * result
    return result


def matrix_case(case, terminal_eigenvalues, tracial):
    k = mp.mpf(case)
    # Two actual isometric dimensional extensions and one final unitary.
    w0 = unitary(3, [(0, 2, k/4, k/6), (1, 2, k/5, -k/7)])[:, :2]
    w1 = unitary(4, [(1, 3, k/8, k/3), (0, 3, k/6, -k/4)])[:, :3]
    w2 = unitary(4, [(0, 2, k/5, k/9), (1, 3, k/7, k/5)])
    stages = [w0, w1, w2]
    v = w2 * w1 * w0
    require(mp.norm(v.H*v - mp.eye(2)) < TOL, "isometry")

    eigenbasis = unitary(4, [(0, 3, k/3, k/4), (0, 2, k/5, -k/4)])
    e = eigenbasis * mp.diag([mp.mpf(x) for x in terminal_eigenvalues]) * eigenbasis.H
    tau = mp.eye(2)/2
    if not tracial:
        basis = unitary(2, [(0, 1, k/7, -k/5)])
        tau = basis * mp.diag([mp.mpf("0.8"), mp.mpf("0.2")]) * basis.H
    h = v.H * e * v
    rho = v * tau * v.H
    sigma = e/trace(e)
    proj = v*v.H
    require(mp.norm(proj*e - e*proj) > mp.mpf("0.001"), "nonreducing example")
    require(mp.norm(rho*sigma - sigma*rho) > mp.mpf("0.001"), "noncommuting states")

    after_rho = with_flag(v.H * rho * v, 0)
    after_sigma = with_flag(v.H * sigma * v, trace((mp.eye(4)-proj)*sigma))
    require(abs(trace(after_sigma) - 1) < TOL, "failure outcome retained")
    info = relative_entropy(rho, sigma) - relative_entropy(after_rho, after_sigma)
    cost = -trace(rho*log_pd(e))
    feedback = -trace(tau*log_pd(h))
    operator_gap = log_pd(h) - v.H*log_pd(e)*v
    require(min(mp.eighe(operator_gap, eigvals_only=True)) >= -TOL, "operator Jensen positivity")
    require(abs(feedback - (cost-info)) < TOL, "unmodified complete-state identity")
    require(abs(info-trace(tau*operator_gap)) < TOL, "DPI equals Jensen gap")
    if tracial:
        require(abs(feedback + mp.log(mp.det(h)).real/2) < TOL, "root log determinant")

    terms = []
    reachable = [tau]
    for w in stages:
        reachable.append(w * reachable[-1] * w.H)
    future = e
    for j in reversed(range(len(stages))):
        w = stages[j]
        earlier = w.H * future * w
        local_gap = log_pd(earlier) - w.H*log_pd(future)*w
        terms.append(trace(reachable[j]*local_gap))
        future = earlier
    terms.reverse()
    require(min(terms) >= -TOL and abs(terms[-1]) < TOL, "nonnegative steps; unitary step zero")
    require(abs(sum(terms) - info) < TOL, "multi-birth telescoping")
    return {"case":case, "tracial":tracial, "DPI_gain":mp.nstr(info, 19),
            "absolute_identity_error":mp.nstr(abs(feedback-(cost-info)), 4),
            "stage_gains":[mp.nstr(t, 19) if abs(t)>TOL else "0" for t in terms]}


def golden_controls():
    p = (sp.sqrt(5)-1)/2
    a = sp.sqrt(p)
    field = sp.QQ.algebraic_field(a)
    v = sp.Matrix([a, p])
    g = sp.Matrix([[a, -p], [p, a]])
    both = sp.kronecker_product(v, v)
    cx = sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    expected = {"G":p, "CX":(p+2*p**3*a)**2, "GG":(2*p-1)**2}
    raw = {"G":(both.T*sp.kronecker_product(g,sp.eye(2))*both)[0]**2,
           "CX":(both.T*cx*both)[0]**2, "GG":(v.T*g*g*v)[0]**2}
    require(field.from_sympy((v.T*v)[0]-1)==field.zero, "canonical birth norm")
    for key in expected:
        require(field.from_sympy(raw[key]-expected[key])==field.zero, "exact "+key)

    # Rational enclosures imply a strict information ordering at the actual z.
    # The positive root of x*x+x-1 is p. No numerical log decides this test.
    f = Fraction
    p_lo, p_hi = f(61,100), f(62,100)
    a_lo = f(78,100)
    z = f(1,2**20)
    require(p_lo*p_lo+p_lo < 1 < p_hi*p_hi+p_hi and a_lo*a_lo < p_lo, "Golden brackets")
    var_g_lower = p_lo*(1-p_hi)
    var_cx_upper = 1-(p_lo+2*p_lo**3*a_lo)**2
    var_gg_upper = (2*p_hi-1)**2
    require(0 < var_cx_upper < (1-z)**2*var_g_lower, "strict G > CX information")
    require(0 < var_gg_upper < (1-z)**2*var_g_lower, "strict G > GG information")
    zz = mp.mpf(1)/2**20
    values = {}
    for key, exact in expected.items():
        q = mp.mpf(str(exact.evalf(73)))
        x = 1-q
        gain = mp.log1p(-zz*x)-x*mp.log1p(-zz)
        values[key] = {"q":mp.nstr(q, 26), "information_nats":mp.nstr(gain, 24)}
    return values


if __name__ == "__main__":
    matrices = [matrix_case(1, ["0.3","0.7","1.1","1.9"], True),
                matrix_case(2, ["0.2","0.6","1.2","1.6"], False),
                matrix_case(3, ["0.7","0.7","1","1"], True)]
    print(json.dumps({"status":"PASS", "matrix_controls":matrices,
                      "golden_exact_and_enclosures":golden_controls(),
                      "scope":"Finite algebra and stated examples. Physical Cost-Info binding unproved."},
                     indent=2))
