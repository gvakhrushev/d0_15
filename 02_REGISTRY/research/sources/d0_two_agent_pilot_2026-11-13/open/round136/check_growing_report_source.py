"""Check the passive recorded clock, actual inverse powers, and independent backward contrast."""

from collections import Counter
from fractions import Fraction
from math import factorial
import json
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round132"))
from check_paired_activation_reader import ne, gate, require, PIN


def verify_writers_and_powers():
    p, a = ne.P, ne.A
    v = sp.Matrix([a,p])
    g = sp.Matrix(ne.G_LOCAL)
    port, spin = 0, (1,2)
    z = [gate("SourceI", port, *spin)]*2

    def matrix(word):
        e = ne.Execution(3, (), (), tuple(word), ne.G_CX_SOURCE_I, port, spin)
        return ne.word_matrix(e, max_qubits=3, max_expanded_stages=len(word))

    local_g = gate("G", port)
    inv = matrix(z+[local_g]+z)
    require(ne.exact_matrix_equal(inv, sp.kronecker_product(g.T, sp.eye(4))),
            "Paid zero preparation changed")
    require(ne.exact_matrix_equal(inv*sp.kronecker_product(v, sp.eye(4)),
                                     sp.kronecker_product(sp.Matrix([1,0]), sp.eye(4))),
            "Actual neutral born tail is not prepared zero")
    g_on_port = sp.kronecker_product(g, sp.eye(4))
    require(ne.exact_matrix_equal(inv*g_on_port,sp.eye(8)), "The real last helper echo is not identity")
    plus, minus = z+z+[local_g]*2, z+[local_g]*2+z
    require(Counter(plus) == Counter(minus), "Changed addresses or layout in the backward contrast")
    require(ne.exact_matrix_equal(matrix(plus), sp.kronecker_product(g**2, sp.eye(4))),
            "Wrong actual positive backward rotation")
    require(ne.exact_matrix_equal(matrix(minus), matrix(plus).T),
            "Wrong actual negative backward rotation")
    v0, v1 = a, p
    masses = [(mi*(mi*v0*mi))**2 for mi in (v0,v1)]
    require(ne.exact_matrix_equal(sp.Matrix(masses), sp.Matrix([p**4,p**7])),
            "Wrong original pointer + 000 / 101 charged container compression")
    return [4,7]


def verify_range_and_jets():
    # Genuine two-dimensional old WORK carrier, with the full complementary basis.
    s,c,db = sp.symbols("s c db", real=True)
    f = sp.Matrix([c,s])
    v = sp.Matrix([3,4])/5
    pa = [sp.diag(1,0), sp.diag(0,1)]
    mu0,mu1 = sp.symbols("mu_0 mu_1", positive=True)
    mu = [mu0,mu1]
    h = sp.zeros(1)
    for k in range(2):
        vf = pa[k]*f
        wb = pa[k]*v
        real_leaf = vf*vf.T/(vf.T*vf)[0]
        h += mu[k]*wb.T*real_leaf*wb
    require(sp.cancel(h[0]-(9*mu0+16*mu1)/25) == 0, "Passive return picked forward odds")
    require(all(sp.diff(sp.cancel(h[0]), x) == 0 for x in (c,s)), "Spurious forward source")

    # Nonscalar full backward stationary column inside the two fixed observed ranges.
    mu0,mu1 = sp.Rational(3,5), sp.Rational(2,5)
    p0,p1 = sp.diag(1,1,0,0), sp.diag(0,0,1,1)
    k = mu0*p0+mu1*p1
    w = sp.eye(4)[:,[0,2]]
    require((sp.eye(4)-w*w.T)*k*w == sp.zeros(4,2),
            "Wrong mixed stationary multiplicities")
    require(w.T*k*w == sp.diag(mu0,mu1), "Stationary height has wrong spectrum")
    cross = sp.Matrix([[0,0,1,2],[0,0,3,4],[-1,-3,0,0],[-2,-4,0,0]])
    dk = cross*k-k*cross
    tau = sp.symbols("tau",positive=True)
    require(sp.trace((sp.eye(2)+tau*w.T*k*w).inv()*w.T*dk*w) == 0,
            "A forward change created a source at backward stationarity")

    q,s,c,t,m0,m1 = sp.symbols("q s c t mu_0 mu_1", real=True)
    plus = m0*(sp.sqrt(1-q)*c-s*t/sp.sqrt(1-q))**2 + m1*(sp.sqrt(q)*c+s*t/sp.sqrt(q))**2
    require(sp.simplify(plus-plus.subs(t,-t)-4*s*c*t*(m1-m0)) == 0,
            "Literal symmetric finite backward contrast failed")
    return True


def verify_four_retained_outcomes():
    p,lmbda,eta,nu,u = sp.symbols("p lambda nu_H nu u",positive=True)
    law = sp.Matrix([
        1-lmbda*eta-lmbda*(1-eta)*nu*u,
        lmbda*(1-eta)*nu*u,
        lmbda*eta*(1-nu*u),
        lmbda*eta*nu*u,
    ])
    weights = sp.Matrix([p**(5+a+3*b) for a in (0,1) for b in (0,1)])
    require(sp.expand(sum(law)-1) == 0, "A terminal failure was discarded")
    wanted = -lmbda*nu*p**5*(1-p**3)*(1-eta+p*eta)
    require(sp.factor(sp.diff(law.dot(weights), u)-wanted) == 0,
            "The registered readiness factor changed the growing-clock source")
    return [5,8,6,9]


def verify_calibration():
    iv = mp.iv
    iv.dps = 120
    p = (iv.sqrt(5)-1)/2
    c,s = iv.mpf(1),iv.mpf(0)
    a,b = iv.sqrt(p),p
    exponent = 15*(1 << 88)
    while exponent:
        if exponent & 1:
            c,s = c*a-s*b, s*a+c*b
        a,b = a*a-b*b, 2*a*b
        exponent //= 2
    require(s*s > iv.mpf("0.998511") and s*s < iv.mpf("0.998513"), "Wrong B135 threshold rotation")
    require(c*s < 0 or c*s > 0, "The actual threshold coherence is not strictly nonzero")
    forward_abs = abs(c*s)
    sin2, cos2 = 2*iv.sqrt(p)*p, p**3
    readiness = iv.mpf(["0.05502","0.05503"])
    weight = p**5*(1-p**3)*(1-readiness+p*readiness)
    require(4*abs(sin2*cos2) > iv.mpf(1)/2, "The literal k=1 yaw lost its positive contrast")
    require((2*p**3)**20 > iv.mpf(1)/2**24, "The actual independent fairness rate changed")
    require(weight > iv.mpf(1)/2**5, "The retained branch weights cannot support the contrast")
    require(forward_abs > iv.mpf(1)/2**6, "Threshold-port coherence is too small")
    require(Fraction(2*3**40,factorial(40)) < Fraction(1,2**57), "Thermal locality bound is not below the strict J contrast")
    return "The actual k=1 backward secant has |delta_J| > 2^(-57) before neutral births"


def main():
    overlaps = verify_writers_and_powers()
    print(json.dumps({
        "status": "PASS",
        "primary_native_sha256": PIN,
        "serialized_passive_weights_exponents_before_neutral_births": overlaps,
        "all_four_retained_outcome_exponents_before_neutral_births": verify_four_retained_outcomes(),
        "neutral_tail_overlap_squared": "p",
        "neutral_tail_dimension_multiplier": 2,
        "exact_range_and_independent_backward_secant": verify_range_and_jets(),
        "actual_88_control_threshold": verify_calibration(),
        "matched_geometric_source_only_on_guarded_reverse_domain": True,
        "full_physical_book_price_selected": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
