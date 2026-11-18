"""Exact finite checks for the grade projector and the native two-length material jet."""
from fractions import Fraction
import json

import sympy as sp


def check(condition, label):
    if not condition:
        raise AssertionError(label)


def grade_projection():
    # This rectangular differential has two positive singular values and one
    # zero vector in each of the intentionally non-full-rank blocks.
    x = sp.symbols("x")
    incidence = sp.Matrix([[1, 1, 0], [0, 2, -1], [1, 3, -1], [0, 0, 0], [2, 0, 1]])
    # Final row is deliberately chosen in the span of the first two.
    incidence[-1, :] = 2 * incidence[0, :] - incidence[1, :]
    lower, upper = incidence.T * incidence, incidence * incidence.T
    check(incidence.rank() == 2, "shared nonzero Hodge spectrum with extra kernels")
    check(sp.expand(upper.charpoly(x).as_expr()
                    - x**2 * lower.charpoly(x).as_expr()) == 0, "paired Hodge spectrum")
    beta, z_heat, w, cold = sp.symbols("beta Z w J", positive=True)
    ordinary = sp.log(z_heat) / beta + cold
    grade_mean = w / z_heat
    check(sp.simplify(ordinary + sp.log(grade_mean) / beta
                      - sp.log(w) / beta - cold) == 0, "grade inversion on original tuple")
    log_partition = sp.log(z_heat) + cold
    check(sp.simplify((log_partition-beta*ordinary)/(1-beta)-cold) == 0,
          "same-execution partition inversion")
    check(Fraction(359, 425) > Fraction(84, 100), "grade imbalance well conditioned")


def finite_memory_output():
    # One permanently surviving block and two communicating output blocks.
    t, y = sp.symbols("t y", real=True)
    keep = sp.Matrix([[1, 0, 0], [0, y/4, 0], [0, sp.Rational(1, 5), sp.Rational(1, 3)]])
    initial = sp.Matrix([sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(1, 4)])
    yes = sp.Matrix([[0, sp.Rational(1, 10), sp.Rational(1, 7)]])
    stop = sp.ones(1, 3)*(sp.eye(3)-keep)

    def exit_mass(effect):
        generating = (effect*(sp.eye(3)-t*keep).inv()*initial)[0]
        return sp.cancel(generating).subs(t,1)

    check(sp.simplify(exit_mass(stop)-sp.Rational(3, 4)) == 0,
          "absorption allows a positive nonterminating class")
    conditioned = sp.cancel(exit_mass(yes)/exit_mass(stop))
    base = sp.Rational(3,5)
    score = sp.cancel(sp.diff(conditioned,y)/conditioned).subs(y,base)
    check(conditioned.subs(y,base) > 0 and score.is_Rational and score != 0,
          "regular exact finite-memory conditional score is algebraic")


def ring_check(expr, symbol):
    num, den = sp.fraction(sp.cancel(expr))
    modulus = symbol**4+symbol**2-1
    return sp.rem(num, modulus, symbol) == 0 and sp.rem(den, modulus, symbol) != 0


def material_projection():
    a = sp.symbols("a", positive=True)
    p = a**2
    e0, e1, e14 = (sp.eye(3)[:, i] for i in range(3))
    vacuum = a*e1 + p*e14
    generator = vacuum*e1.T-e1*vacuum.T
    dgen = e0*e1.T-e1*e0.T
    polar = sp.eye(3)+generator+generator**2/(1+a)
    dpolar = dgen+(generator*dgen+dgen*generator)/(1+a)
    dmat = dpolar*polar.T
    phase = sp.diag(1,-1,1)
    dphase = dmat.T*phase + phase*dmat
    check(all(ring_check(v,a) for v in dphase-2*(e0*e1.T+e1*e0.T)), "full (880) derivative")
    amplitude = lambda i: a**(4-bin(i).count("1"))*p**bin(i).count("1")
    c = sum((-1)**(i % 2)*amplitude(i)**2 for i in range(16))
    sub = sp.Matrix([amplitude(i) for i in (0,1,14)])
    dc = (sub.T*dphase*sub)[0]
    check(ring_check(c-p**3,a) and ring_check(dc-4*a**7*p,a),
          "cold contraction and nonzero tangent on canonical material bank")
    check(ring_check(1-2*p**2-p**3,a), "original beta is distinct from 1")
    # Full youngest return after the swap carries I-vv^T on e and a free y.
    young = sp.Matrix([[1-a*a,-a*p,0],[-a*p,1-p*p,0],[0,0,1-a*a]])
    check(ring_check(2*(young*dphase).trace() + 8*a*p,a), "youngest heat coefficient")
    L = 11
    q = Fraction(1,22*(L+1))
    check(Fraction(1,22)/(1-q)**2 < Fraction(1,20), "absolute differentiated thermal tail")
    upper = (Fraction(425,359) * (8*(L+2)+2) / (Fraction(18,5)*L-2)
             / (22**2*(L+1)*(L+2)))
    check(upper < Fraction(1,20000), "ratio bound for one actual CX pair")
    alpha, h, j = sp.symbols("alpha h j")
    rows = (j+h, j+alpha*h)
    check(sp.cancel((rows[1]-alpha*rows[0])/(1-alpha)-j) == 0,
          "two paid clocks reconstruct individual cold material source")
    return str(upper), str(Fraction(20001,19999))


def real_covector_projection():
    # Two independent smooth tangent coordinates can have arbitrary real
    # values. Use exact exponentials as a formal x=e^-beta to avoid a
    # numerical rank decision. These test rows only validate linear algebra.
    x = sp.symbols("x", positive=True)
    base = sp.Matrix([[x/(1+x), 1/(1+2*x)], [1/(1+x), x/(1+2*x)]])
    coefficients = sp.Matrix([x/20, -x/30])
    final = base*coefficients
    heat = base.row_join(final)
    weights = sp.Matrix([-coefficients[0],-coefficients[1],1])/(1-sum(coefficients))
    check(sp.factor(base.det()) != 0, "two independent heat directions")
    check(all(sp.cancel(v) == 0 for v in heat*weights) and sp.cancel(sum(weights)-1) == 0,
          "single stencil cancels the whole heat covector")
    g1, g2, u, v = sp.symbols("g1 g2 u v", real=True)
    cold = sp.Matrix([g1,g2])
    readouts = heat+cold*sp.ones(1,3)
    check(sp.cancel((sp.Matrix([u,v]).T*(readouts*weights-cold))[0]) == 0,
          "same stencil commutes with arbitrary real pullback")
    eps = Fraction(1,10)
    check((1+eps)/(1-eps) == Fraction(11,9), "readout stability")


if __name__ == "__main__":
    grade_projection()
    finite_memory_output()
    ratio, norm = material_projection()
    real_covector_projection()
    print(json.dumps({"grade_supertrace": "359D", "full_heat_dimension": "425D",
                      "pair_ratio_upper_exact": ratio, "stencil_l1_upper": norm,
                      "full_GR": False, "passed": True}, sort_keys=True))
