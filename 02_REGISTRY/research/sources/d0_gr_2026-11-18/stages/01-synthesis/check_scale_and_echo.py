"""Exact local tests for the scale minor, marked feedback, and paid echo."""

from fractions import Fraction as F
import json
import sympy as s


def scale_minor():
    x, rho, slope, curvature, cubic = s.symbols("X rho d C2 c3", nonzero=True)
    kinetic = slope*x + curvature*x**2/2 + cubic*x**3/6
    # Compare the two coefficient vectors in the basis (dpsi tensor dpsi, g).
    original = s.Matrix([kinetic.diff(x), -kinetic/2])
    scaled = s.Matrix([kinetic.diff(x).subs(x, x/rho), -rho*kinetic.subs(x, x/rho)/2])
    minor = s.expand(original.row_join(scaled).det())
    expected = slope*curvature*(1/rho-1)/4
    assert s.simplify(minor.coeff(x, 2) - expected) == 0
    assert minor.subs({curvature: 0, cubic: 0}).expand() == 0
    return str(s.factor(expected))


def single_j2_coefficient():
    """Differentiate the two-tick feedback and certify the local reduced kinetic jet."""
    r, x, p, sign = s.symbols("r x p sigma", real=True)
    z = s.Rational(1, 2**20)
    # t^2=1 here. The first and second derivatives scale as t^2 and t^4.
    golden = (s.sqrt(5)-1)/2
    at_zero = {r: 0, x: 0}
    edge = p**2*(1+r)
    born = (p+sign*p**2*x)**2
    geom = 4*edge*(1-edge)
    matter = 4*born*(1-born)
    factors = (1-z*matter, 1-z*(geom+(1-geom)*matter))
    field = s.QQ.algebraic_field(s.sqrt(5))

    def evaluate(expr, orientation):
        val = expr.subs(at_zero).subs({p: golden, sign: orientation})
        return field.from_sympy(val)

    def strictly_positive(value):
        # Exact rational comparison for A+B*sqrt(5). No floating-point sign.
        expr = s.expand(field.to_sympy(value))
        b = expr.coeff(s.sqrt(5))
        a = expr-b*s.sqrt(5)
        assert a.is_Rational and b.is_Rational
        if b == 0:
            return a > 0
        if a == 0 or (a > 0) == (b > 0):
            return b > 0
        return a*a > 5*b*b if a > 0 else 5*b*b > a*a

    cases = []
    for orientation in (-1, 1):
        def jet(coords):
            total = field.zero
            for f in factors:
                f0 = evaluate(f, orientation)
                assert strictly_positive(f0)
                first = evaluate(s.diff(f, coords[0]), orientation)
                # Derivatives of -log(f) include the complete normalizer.
                if len(coords) == 1:
                    total -= first/f0
                else:
                    other = evaluate(s.diff(f, coords[1]), orientation)
                    mixed = evaluate(s.diff(f, *coords), orientation)
                    total += first*other/f0**2-mixed/f0
            return total

        c, d = jet((r,)), jet((x,))
        assert strictly_positive(c)
        ratio = d/c
        c2 = jet((x,x)) - 2*ratio*jet((r,x)) + ratio**2*jet((r,r))
        curvature = c2/c
        characteristic = -orientation*2*c2/d
        assert strictly_positive(curvature+1479) and strictly_positive(-1478-curvature)
        assert strictly_positive(characteristic-126) and strictly_positive(127-characteristic)
        cases.append({"orientation": orientation, "C2_over_c_at_unit_t": str(field.to_sympy(curvature).evalf(16)),
                      "nonzero_cone_coefficient_at_unit_t": str(field.to_sympy(characteristic).evalf(16))})
    return cases


def mark_identity():
    q, z = s.symbols("q z", positive=True)
    h = 1-z+z*q
    tilted = q/h
    difference = tilted-q
    unit_price = -s.log(h)
    assert s.factor(difference - z*q*(1-q)/h) == 0
    assert s.factor(difference.diff(q) + (1-q-tilted)*unit_price.diff(q)) == 0
    return "d(q_tilt-q) = -(1-q-q_tilt) d[-log(1-z+zq)]"


def echo_data():
    p = (s.sqrt(5)-1)/2
    z = s.Rational(1, 2**20)
    gain = s.simplify(p**6 + 4*p**9)
    assert s.simplify(gain - (128*p-79)) == 0
    loss = 2*z*gain*(1-gain)/(1+s.sqrt(1-z))
    # Enclose both the input probability and the loss with rational arithmetic.
    lo, hi = F(6180339887498, 10**13), F(6180339887500, 10**13)
    assert lo**2+lo < 1 < hi**2+hi
    qlo, qhi = 128*lo-79, 128*hi-79
    assert 0 < qlo < qhi < F(1, 2)
    delta = F(1, 2**20)
    lower = delta*qlo*(1-qlo)
    upper = 2*delta*qhi*(1-qhi)/(2-delta)
    assert F(921,10**10) < lower < upper < F(922,10**10)
    # Direct saturation in the two sectors. Reference system is a spectator.
    v = s.Matrix([s.sqrt(gain), s.sqrt(1-gain)])
    eye = s.eye(2)
    t = s.diag(1, s.sqrt(1-z))
    fail = s.diag(0, s.sqrt(z))
    assert t*t + fail*fail == eye
    observed = (v.T*t*v)[0]**2 + (v.T*fail*v)[0]**2
    assert s.simplify(observed - (1-loss)) == 0
    return {"q": str(gain.evalf(18)), "echo_probability_loss_at_least": str(loss.evalf(18)),
            "rational_enclosure": ["921/10^10", "922/10^10"]}


def branch_comparison():
    prior, n0, n1 = s.symbols("pi n0 n1", positive=True)
    posterior = prior*n1/((1-prior)*n0+prior*n1)
    odds_change = posterior/(1-posterior) * (1-prior)/prior
    assert s.factor(odds_change - n1/n0) == 0
    return "posterior odds / prior odds = n1/n0"


if __name__ == "__main__":
    print(json.dumps({"kinetic_minor_X2": scale_minor(), "single_J2": single_j2_coefficient(), "mark_derivative": mark_identity(),
                      "native_echo_ET3_ET5": echo_data(),
                      "retained_label": branch_comparison()}, indent=2))
