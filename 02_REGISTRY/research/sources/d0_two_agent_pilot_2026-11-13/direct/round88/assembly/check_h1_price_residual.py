"""Check the full six-face coframe response and a complete positive history sum."""
from itertools import combinations, product
import json
import sympy as sp


def require(test, reason):
    if not test:
        raise ArithmeticError(reason)


pairs = list(combinations(range(4), 2))
eye = sp.eye(4)
eta = eye.copy()
eta[0, 0] = eta[1, 1] = 0
eta[0, 1] = eta[1, 0] = 1
eta[2, 2] = eta[3, 3] = -1
generators = []
for axis in (2, 3):
    generator = sp.zeros(4)
    generator[1, axis] = generator[axis, 0] = 1
    generators.append(generator)


def shift(site, axis, step):
    return tuple(x + (step if j == axis else 0) for j, x in enumerate(site))


def trace_test():
    # lam is the typed EPS_PLUS matter coefficient, with no imposed magnitude.
    lam, tilt = sp.symbols("lambda t", real=True)
    e0, e1 = sp.Rational(1, 256), sp.Rational(4, 256)
    h = sp.symbols("h", positive=True)
    x, y = sp.symbols("x y", real=True)
    base = (0, 0, x, y)

    def profile(site):
        return -lam * (e0 + e1) * (site[2]**2 + site[3]**2) / 2

    def link(site, axis, sign=1):
        if axis != 0:
            return eye
        later = shift(site, 0, h)
        k = sp.zeros(4)
        for transverse, generator in zip((2, 3), generators):
            k += (profile(later) - profile(shift(later, transverse, -h))) * generator / 2
        return eye + sign*k + k*k/2

    frame = eye.copy()
    frame[1, 0] = profile(base)/2
    frame[0, 1] = tilt
    leg = h*frame
    geometric = 0
    for first, second in pairs:
        third, fourth = (j for j in range(4) if j not in (first, second))
        holonomy = (link(base, first)*link(shift(base, first, h), second)
                    * link(shift(base, second, h), first, -1)*link(base, second, -1))
        curvature = ((holonomy - eta*holonomy.T*eta)*eta/2).applyfunc(sp.expand)
        for a, b in pairs:
            c, d = (j for j in range(4) if j not in (a, b))
            area = leg[a, third]*leg[b, fourth] - leg[b, third]*leg[a, fourth]
            geometric += (sp.LeviCivita(first, second, third, fourth)
                          * sp.LeviCivita(a, b, c, d)*area*curvature[c, d])
    grav = sp.simplify(sp.diff(geometric, tilt).subs(tilt, 0)/h**4)
    require(grav == lam*(e0+e1), "six original based plaquettes")
    inverse = frame.inv()
    guu = (inverse*eta*inverse.T)[0, 0]
    require(guu.subs(tilt, 0) == 0, "matter value on unperturbed coframe")
    material = sp.simplify(sp.diff(guu, tilt).subs(tilt, 0))
    require(material == -2, "actual inverse coframe response")
    responses = [sp.simplify(grav + lam*material*e) for e in (e0, e1)]
    require(responses == [3*lam/256, -3*lam/256], "finite response including matter")
    # The mirrored signs survive arbitrary positive and unequal gains.
    for g0, g1, current in product((sp.Rational(1, 5), 1, 8), repeat=3):
        for obs in (current, -current, 0):
            err = [abs(sp.sympify(obs)/g - target.subs(lam, -1))
                   for g, target in zip((g0, g1), responses)]
            require(max(err) >= sp.Rational(3,256), "gain independent lower bound")
    p = (sp.sqrt(5)-1)/2
    z = sp.Rational(1, 2**20)
    Q = 1-4*z*p**3
    R = 1-4*z*p**3*(1+p**6)
    lam_owner = -2*p**(-5)*(R/Q+p**6)
    return {"typed_EPS_PLUS_sources": [str(v) for v in responses],
            "floor_in_volume_normalization": str(sp.N(abs(lam_owner)*3/256, 15)),
            "verified": "six faces at symbolic h,x,y; full inverse coframe; two nonvacuum inputs"}


def complete_positive_examples():
    # Positive weights depend on coframe tilt t through exp(-a*t) etc.
    # Natural-log units in this fixture; the identity is unchanged in base phi.
    t = sp.symbols("t", real=True)
    geom = [2*sp.exp(-2*t), 3*sp.exp(4*t)]
    rows = [[(1,0), (4,2)], [(3,-1), (1,1)]]
    posterior = []
    slopes = []
    conditional = []
    for row in rows:
        tails = [mass*sp.exp(-cost*t) for mass, cost in row]
        z = sum(a*b for a,b in zip(geom, tails))
        slopes.append(sp.simplify((-sp.diff(z,t)/z).subs(t, 0)))
        pi = [(a*b/z).subs(t,0) for a,b in zip(geom,tails)]
        posterior.append(pi)
        conditional.append(sum(prob*c for prob,(_,c) in zip(pi,row)))
    tv = sum(abs(a-b) for a,b in zip(*posterior))/2
    prefix = [2, -4]
    contrast = slopes[1] - slopes[0]
    prefix_contrast = sum(a*(u-v) for a,u,v in zip(prefix,posterior[1],posterior[0]))
    require(contrast == prefix_contrast + conditional[1] - conditional[0], "full score")
    require(abs(prefix_contrast) <= (max(prefix)-min(prefix))*tv, "economic posterior bound")
    for scale in (1,7):
        z = sp.expand(scale*sum(geom))
        require(sp.simplify((-sp.diff(z,t)/z).subs(t,0)) == -sp.Rational(8,5),
                "separate material factor leaves same geometric response")
    return {"coupled_raw_contrast": str(contrast), "posterior_TV": str(tv),
            "separable_slope_on_both_histories": "-8/5"}


def stationary_rectangle_and_anchor():
    # A common five-point Dirichlet stencil, with all incident links free.
    lap = sp.Matrix([[-4,1,1,0], [1,-4,0,1], [1,0,-4,1], [0,1,1,-4]])
    h = sp.Rational(1,3)
    unit = sp.ones(4,1)
    potential = lap.inv()*unit*h**2
    lam = sp.Symbol("lambda", nonzero=True)
    energies = (sp.Rational(1,256), sp.Rational(4,256))
    matrix = []
    for eg in energies:
        grav = -lap*(-4*lam*eg*potential)/(2*h**2)
        row = []
        for em in energies:
            source = grav-2*lam*em*unit
            require(source == 2*lam*(eg-em)*unit, "common Dirichlet source")
            row.append(str(source[0]))
        matrix.append(row)
    x0,x1 = sp.Rational(3,4), sp.Rational(-5,8)
    gain0,gain1 = sp.Rational(2,5), sp.Rational(7,3)
    d0,d1 = -sp.Rational(3,256), sp.Rational(3,256)
    center0,center1 = gain0*d0-x0, gain1*d1-x1
    minimizer = (gain1*center0+gain0*center1)/(gain0+gain1)
    errors = [abs((minimizer+x)/g-d) for x,g,d in ((x0,gain0,d0),(x1,gain1,d1))]
    optimum = abs((x1-x0)-(gain1*d1-gain0*d0))/(gain0+gain1)
    require(errors == [optimum,optimum], "optimal common prefix bound is attained")
    t = sp.Symbol("t", real=True)
    weight = 3*sp.exp(-2*t)
    prices = (weight+2*sp.exp(4*t), weight+7*sp.exp(-t))
    shares = [weight/z for z in prices]
    logdiff = lambda z: sp.diff(z,t)/z
    require(sp.simplify(logdiff(shares[1]/shares[0])-logdiff(prices[0]/prices[1])) == 0,
            "early economic share ratio cancels the physical prefix derivative")
    return {"stationary_rectangle":matrix, "minimax_example":str(optimum),
            "economic_anchor_ratio_identity": True}


if __name__ == "__main__":
    print(json.dumps({"all40_test": trace_test(), "positive_history_sum": complete_positive_examples(),
                      "stationary_set_and_prefix": stationary_rectangle_and_anchor(),\n                      "original_Book03_covector_measured": False, "GR_closed": False},
                     indent=2, ensure_ascii=False))
