"""Independent targeted check of the actual native-to-Palatini coframe weld.

This does not replay the CAR source calculation or any historical suite.
It resolves the concrete coframe sign discrepancy found during review.
"""
import json
import sympy as s

checks = 0


def require(condition, label):
    global checks
    if not condition:
        raise RuntimeError(label)
    checks += 1


H, Hp, nu = s.symbols("H Hp nu", real=True, nonzero=True)
eta = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                [0, 0, -1, 0], [0, 0, 0, -1]])
observer = s.Matrix([1, 1, 0, 0]) / s.sqrt(2)
observer_gram = 2 * (eta * observer) * (eta * observer).T - eta
require(observer_gram == s.eye(4), "actual observer-positive Gram")

ep = s.Matrix([[1, 0, 0, 0], [H/2, 1, 0, 0],
               [0, 0, 1, 0], [0, 0, 0, 1]]) / nu
signs = (1, 1, -1, -1)
e = s.diag(*signs) * ep
V = s.Matrix([[0, nu, 0, 0], [nu, -nu*H/2, 0, 0],
              [0, 0, nu, 0], [0, 0, 0, nu]])
require(eta * e.inv().T == V, "literal native raised inverse legs")
require(eta * ep.inv().T != V, "hostile positive-spatial coframe rejected")
require(e.T * eta * e == ep.T * eta * ep, "metric unchanged by two signs")
require(s.factor(e.det()) == nu**-4, "actual coframe volume")

pairs = [(i, j) for i in range(4) for j in range(i+1, 4)]
generators = []
for i, j in pairs:
    bivector = s.zeros(4)
    bivector[i, j] = 1
    bivector[j, i] = -1
    G = eta * bivector
    require(G.T * eta + eta * G == s.zeros(4), "Lorentz generator")
    generators.append(G)
omega = [-Hp * generators[1] / 2] + [s.zeros(4) for _ in range(3)]
for r in range(4):
    for q in range(r+1, 4):
        derivative = ((e[:, q].diff(H) * Hp if r == 2 else s.zeros(4, 1))
                      - (e[:, r].diff(H) * Hp if q == 2 else s.zeros(4, 1)))
        torsion = derivative + omega[r] * e[:, q] - omega[q] * e[:, r]
        require(s.simplify(torsion) == s.zeros(4, 1), "all LC torsion rows")

Hg = s.zeros(24)
for r in range(4):
    for j, G in enumerate(generators):
        for q in range(4):
            for l, L in enumerate(generators):
                Hg[6*r+j, 6*q+l] = 2*signs[r]*signs[q]*((G*L-L*G)*eta)[r, q]
require(Hg == Hg.T, "Palatini scalar Hessian symmetry")
require(Hg.det() == 2**32, "full geometric Hessian determinant")

# Directly contract e_a^r e_b^s F_rs^{ab}; take the H derivative of the
# inverse coframe and the mean sin(x)^2 = 1/2.  This derives the coframe
# derivative-curvature cross term independently of any LC completion.
E = e.inv() / nu
bg = s.zeros(24, 1)
for role in range(4):
    for j, G in enumerate(generators):
        coefficient = 0
        for r in range(4):
            for q in range(4):
                component = (int(r == 2 and q == role)
                             - int(q == 2 and r == role)) * G * eta
                coefficient += sum(E[r, a] * E[q, b] * component[a, b]
                                   for a in range(4) for b in range(4))
        bg[6*role+j] = s.simplify(-coefficient.diff(H).subs(H, 0)/2)
ell = s.zeros(24, 1)
ell[1] = -s.Rational(1, 2)
require(bg == -Hg * ell / 2, "direct scalar cross term equals LC completion")
require((ell.T * Hg * ell)[0] == 0, "LC pp scalar zero")
require(bg[9] == -s.Rational(1, 2) and sum(x != 0 for x in bg) == 1,
        "actual moving coframe linear term")
require(Hg.extract([1, 9], [1, 9]) == s.Matrix([[0, -2], [-2, 0]]),
        "driven geometric block remains unchanged")

print(json.dumps({
    "status": "PASS", "checks": checks,
    "native_coframe_spatial_signs": list(signs),
    "native_lc_coefficient": "-Hprime/2",
    "palatini_volume_times_scalar_prefactor": "nu^(-2)",
    "moving_coframe_linear": [[i, str(x)] for i, x in enumerate(bg) if x],
    "palatini_full_hessian_determinant": str(Hg.det()),
    "driven_geometric_block": [[str(x) for x in row]
                               for row in Hg.extract([1, 9], [1, 9]).tolist()],
    "scope": "Independent exact coframe, torsion, and scalar-curvature contraction only; no CAR replay."
}, indent=2))
