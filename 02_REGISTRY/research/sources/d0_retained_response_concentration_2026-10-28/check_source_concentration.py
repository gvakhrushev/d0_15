#!/usr/bin/env python3
"""Exact changed-input checks for retained response concentration.

No optional packages, numerical matrix differentiation, geometry replay,
or implicit asserts. Prints one deterministic JSON receipt.
"""

from fractions import Fraction as Q
from math import factorial
import hashlib
import json
from pathlib import Path


CHECKS = []


def require(name, condition):
    if not condition:
        raise ArithmeticError(name)
    CHECKS.append(name)


# Sparse polynomials in (p,x,y); coefficients are exact rational numbers.
def poly_constant(x):
    x = Q(x)
    return {(0, 0, 0): x} if x else {}


def poly_add(a, b):
    out = dict(a)
    for mon, coef in b.items():
        out[mon] = out.get(mon, Q(0)) + coef
        if not out[mon]:
            del out[mon]
    return out


def poly_scale(a, k):
    k = Q(k)
    return {mon: k * coef for mon, coef in a.items() if k * coef}


def poly_mul(a, b):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            mon = tuple(ma[i] + mb[i] for i in range(3))
            out[mon] = out.get(mon, Q(0)) + ca * cb
    return {mon: coef for mon, coef in out.items() if coef}


def poly_power(a, n):
    out = poly_constant(1)
    for _ in range(n):
        out = poly_mul(out, a)
    return out


def poly_derivative(a, coordinate):
    out = {}
    for mon, coef in a.items():
        power = mon[coordinate]
        if power:
            mm = list(mon)
            mm[coordinate] -= 1
            out[tuple(mm)] = power * coef
    return out


def poly_at(a, p, x, y):
    return sum(coef * p ** mon[0] * x ** mon[1] * y ** mon[2]
               for mon, coef in a.items())


ONE = poly_constant(1)
P = {(1, 0, 0): Q(1)}
X = {(0, 1, 0): Q(1)}
Y = {(0, 0, 1): Q(1)}
Z = Q(1, 2**20)
E = poly_mul(poly_power(P, 2), poly_add(ONE, X))
U = poly_add(P, poly_mul(poly_power(P, 2), Y))
ELL = poly_scale(poly_mul(E, poly_add(ONE, poly_scale(E, -1))), 4)
UU = poly_power(U, 2)
B = poly_scale(poly_mul(UU, poly_add(ONE, poly_scale(UU, -1))), 4)
A0 = poly_add(ELL, poly_mul(poly_add(ONE, poly_scale(ELL, -1)), B))
R = poly_add(ONE, poly_scale(poly_mul(
    poly_add(ONE, poly_scale(B, -Z)),
    poly_add(ONE, poly_scale(A0, -Z))), -1))
R0 = {mon: coef for mon, coef in R.items() if mon[1] == mon[2] == 0}
RX = poly_derivative(R, 1)
RY = poly_derivative(R, 2)
PF = poly_add(R, poly_scale(poly_add(poly_mul(X, RX), poly_mul(Y, RY)), -1))
PF_REMAINDER = poly_add(PF, poly_scale(R0, -1))
require("report has actual nonzero degree-(2,8) coefficient",
        any(mon[1:] == (2, 8) for mon in R))
require("PF source has no field-degree-one term",
        all(mon[1] + mon[2] != 1 for mon in PF))
require("normalized PF residual starts at field degree two",
        bool(PF_REMAINDER) and
        all(mon[1] + mon[2] >= 2 for mon in PF_REMAINDER))

# Two unequal cells and a genuine normalized rho tangent. Formal p is
# specialized only for this nonzero control; the degree proof above is exact
# for the whole polynomial, hence for the Golden root as well.
p_test = Q(3, 5)
eps = Q(1, 64)
cells = [(Q(1, 2), Q(1, 2), Q(1, 3), Q(-1, 7), Q(1, 5)),
         (Q(1, 2), Q(3, 2), Q(-2, 5), Q(1, 4), Q(-1, 5))]
require("actual unequal PF weights normalize",
        sum(v * rho for v, rho, f, q, drho in cells) == 1)
require("actual PF tangent preserves normalization",
        sum(v * drho for v, rho, f, q, drho in cells) == 0)
rho_row = sum(v * drho * poly_at(PF, p_test, eps * f / rho, -eps * q / rho)
              for v, rho, f, q, drho in cells)
rho_residual = sum(v * drho * poly_at(PF_REMAINDER, p_test,
                                     eps * f / rho, -eps * q / rho)
                   for v, rho, f, q, drho in cells)
require("complete rho row equals quadratic-and-higher residual",
        rho_row == rho_residual)
require("rho source was retained rather than set to zero", rho_row != 0)


# Exact dual numbers and 2x2 matrices. Determinants are differentiated
# directly, independently of the trace-resolvent concentration formula.
def dual(x, dx=0):
    return Q(x), Q(dx)


def dadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def dscale(k, a):
    return k * a[0], k * a[1]


def dmul(a, b):
    return a[0] * b[0], a[1] * b[0] + a[0] * b[1]


def dpower(a, n):
    out = dual(1)
    for _ in range(n):
        out = dmul(out, a)
    return out


def ddivide(a, b):
    return (a[0] / b[0], (a[1] * b[0] - a[0] * b[1]) / b[0]**2)


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inverse2(a):
    determinant = det2(a)
    return [[a[1][1] / determinant, -a[0][1] / determinant],
            [-a[1][0] / determinant, a[0][0] / determinant]]


def product2(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


def trproduct(a, b):
    return sum(a[i][j] * b[j][i] for i in range(2) for j in range(2))


def trace2(a):
    return a[0][0] + a[1][1]


def whole_source(a_matrix, da_matrix, r_value, dr_value, repeats, eta):
    aa = Q(1, 3)
    rf = Q(1, 7)
    rr = dual(r_value, dr_value)
    cc = dadd(dual(1), dscale(-2 * aa, rr))
    factor = dscale(Z * eta, dpower(cc, 2 * repeats))
    dm = [[dadd(dual(1 - Z if i == j else 0),
                dmul(factor, dual(a_matrix[i][j], da_matrix[i][j])))
           for j in range(2)] for i in range(2)]
    determinant = dadd(dmul(dm[0][0], dm[1][1]),
                       dscale(-1, dmul(dm[0][1], dm[1][0])))
    actual = -determinant[1] / determinant[0]
    d0 = [[dm[i][j][0] for j in range(2)] for i in range(2)]
    dinv = inverse2(d0)
    ta = trproduct(dinv, a_matrix)
    tda = trproduct(dinv, da_matrix)
    gamma = (4 * repeats * aa * Z * eta * cc[0] ** (2 * repeats - 1)
             * eps * rf * ta)
    expected = (dr_value / (eps * rf)
                - cc[0] * tda / (4 * repeats * aa * eps * rf * ta))
    return actual, gamma, expected, cc[0], dinv, ta, tda


AP = [[Q(1, 3), Q(1, 9)], [Q(1, 9), Q(1, 2)]]
DAP = [[Q(1), Q(1, 2)], [Q(1, 2), Q(-1, 3)]]
require("past positive matrix is a strict contraction",
        AP[0][0] > 0 and det2(AP) > 0 and
        1 - AP[0][0] > 0 and
        det2([[1 - AP[0][0], -AP[0][1]],
              [-AP[1][0], 1 - AP[1][1]]]) > 0)
require("past and its tangent do not commute",
        product2(AP, DAP) != product2(DAP, AP))
for repeats in (1, 3, 7):
    actual, gain, expected, cc, dinv, ta, tda = whole_source(
        AP, DAP, Q(1, 9), Q(1, 10), repeats, Q(3, 5))
    require(f"moving noncommutative full-source identity M={repeats}",
            actual / gain == expected)
    require(f"actual centre gain is positive M={repeats}", gain > 0)
    # Entrywise l1 is a rigorous upper bound for the matrix trace norm.
    da_upper = sum(abs(x) for row in DAP for x in row)
    require(f"singular-safe past trace estimate M={repeats}",
            abs(tda / ta) <= da_upper / ((1 - Z) * trace2(AP)))

AS = [[Q(1, 2), Q(0)], [Q(0), Q(0)]]
DAS = [[Q(0), Q(1, 2)], [Q(1, 2), Q(0)]]
actual, gain, expected, *_ = whole_source(
    AS, DAS, Q(1, 9), Q(1, 10), 3, Q(3, 5))
require("rank-deficient nonzero past still has positive gain", gain > 0)
require("rank-deficient moving-past identity", actual / gain == expected)

ZERO2 = [[Q(0), Q(0)], [Q(0), Q(0)]]
actual, gain_current, expected, *_ = whole_source(
    AP, ZERO2, Q(1, 8), Q(1, 10), 7, Q(3, 5))
_, gain_frozen, *_ = whole_source(
    AP, ZERO2, Q(0), Q(1, 10), 7, Q(3, 5))
require("actual gain removes the M-dependent current scalar slope",
        actual / gain_current == Q(1, 10) / (eps * Q(1, 7)))
require("freezing gain at r0 is not the same source",
        actual / gain_frozen != Q(1, 10) / (eps * Q(1, 7)))

# The centre gain itself can be computed from the actual finite scalar
# corner. Check its exact log slope by dual inversion, not by log numerics.
for repeats in (1, 3, 7):
    cdual = dual(Q(9, 10), 1)
    factor = dscale(Z * Q(3, 5), dpower(cdual, 2 * repeats))
    dd = [[dadd(dual(1 - Z if i == j else 0), dscale(AP[i][j], factor))
           for j in range(2)] for i in range(2)]
    ddet = dadd(dmul(dd[0][0], dd[1][1]), dscale(-1, dmul(dd[0][1], dd[1][0])))
    dinv = [[ddivide(dd[1][1], ddet), ddivide(dscale(-1, dd[0][1]), ddet)],
            [ddivide(dscale(-1, dd[1][0]), ddet), ddivide(dd[0][0], ddet)]]
    ta = dual(0)
    for i in range(2):
        for j in range(2):
            ta = dadd(ta, dscale(AP[j][i], dinv[i][j]))
    gamma_dual = dmul(dpower(cdual, 2 * repeats - 1), ta)
    log_slope = cdual[0] * gamma_dual[1] / gamma_dual[0]
    require(f"actual finite gain log-slope control M={repeats}",
            2 * repeats - 1 - 2 * repeats * Z <= log_slope <= 2 * repeats - 1)


# Independent current data, not merely one shared diagonal direction.
# Differentiate the determinant directly; no trace-log formula is used
# in the value named actual.
def independent_source(a_matrix, da_matrix, reports, d_reports, eta):
    aa = Q(1, 3)
    rf = Q(1, 7)
    corners = [dadd(dual(1), dscale(-2 * aa, dual(rr, dr)))
               for rr, dr in zip(reports, d_reports)]
    scalar_product = dual(1)
    for cc in corners:
        scalar_product = dmul(scalar_product, dpower(cc, 2))
    factor = dscale(Z * eta, scalar_product)
    dm = [[dadd(dual(1 - Z if i == j else 0),
                dmul(factor, dual(a_matrix[i][j], da_matrix[i][j])))
           for j in range(2)] for i in range(2)]
    determinant = dadd(dmul(dm[0][0], dm[1][1]),
                       dscale(-1, dmul(dm[0][1], dm[1][0])))
    actual = -determinant[1] / determinant[0]
    d0 = [[dm[i][j][0] for j in range(2)] for i in range(2)]
    dinv = inverse2(d0)
    ta = trproduct(dinv, a_matrix)
    tda = trproduct(dinv, da_matrix)
    ell = sum(1 / cc[0] for cc in corners)
    weights = [1 / (cc[0] * ell) for cc in corners]
    gain = 4 * aa * eps * rf * Z * eta * scalar_product[0] * ta * ell
    old = -tda / (4 * aa * eps * rf * ell * ta)
    expected = sum(w * dr / (eps * rf)
                   for w, dr in zip(weights, d_reports)) + old
    return actual, gain, expected, corners, weights, old


for independent_count in (2, 3, 7):
    reports = [Q(1, 9 + j) for j in range(independent_count)]
    d_reports = [Q((-1)**j, 10 + j) for j in range(independent_count)]
    actual, gain, expected, corners, weights, old = independent_source(
        AP, DAP, reports, d_reports, Q(3, 5))
    require(f"independent-copy noncommutative source M={independent_count}",
            actual / gain == expected)
    require(f"independent-copy actual gain and weights M={independent_count}",
            gain > 0 and all(w > 0 for w in weights) and sum(weights) == 1)
    da_upper = sum(abs(x) for row in DAP for x in row)
    require(f"independent-copy full past bound M={independent_count}",
            abs(old) <= da_upper / ((1 - Z) * trace2(AP)
                                    * 4 * Q(1, 3) * eps * Q(1, 7)
                                    * independent_count))

actual, gain, expected, *_ = independent_source(
    AS, DAS, [Q(1, 9), Q(1, 10)], [Q(1, 10), Q(-1, 11)], Q(3, 5))
require("independent-copy source includes singular nonzero past",
        gain > 0 and actual / gain == expected)

# A coordinate unit test in each independent data block. On a diagonal
# centre the max-product dual norm is the sum of these absolute rows.
for independent_count in (2, 5):
    reports = [Q(1, 9)] * independent_count
    rows = []
    for coordinate in range(independent_count):
        d_reports = [eps * Q(1, 7) if j == coordinate else Q(0)
                     for j in range(independent_count)]
        actual, gain, *_ = independent_source(
            AP, ZERO2, reports, d_reports, Q(3, 5))
        rows.append(actual / gain)
    require(f"all independent current rows survive M={independent_count}",
            rows == [Q(1, independent_count)] * independent_count)
    require(f"max-product dual norm is not diluted M={independent_count}",
            sum(abs(row) for row in rows) == 1)

opposite_rows = []
for coordinate, sign in enumerate((1, -1)):
    d_reports = [Q(0), Q(0)]
    d_reports[coordinate] = sign * eps * Q(1, 7)
    actual, gain, *_ = independent_source(
        AP, ZERO2, [Q(1, 9), Q(1, 9)], d_reports, Q(3, 5))
    opposite_rows.append(actual / gain)
require("shared test can cancel opposite current rows", sum(opposite_rows) == 0)
require("independent max tests retain opposite current rows",
        sum(abs(row) for row in opposite_rows) == 1)


# The multi-corner gain is s*L*Tr(D^-1 A) times fixed positive constants.
# Direct dual inverses verify each logarithmic partial slope separately.
def independent_gain_dual(a_matrix, corners, eta):
    scalar_product = dual(1)
    ell = dual(0)
    for cc in corners:
        scalar_product = dmul(scalar_product, dpower(cc, 2))
        ell = dadd(ell, ddivide(dual(1), cc))
    factor = dscale(Z * eta, scalar_product)
    dd = [[dadd(dual(1 - Z if i == j else 0), dscale(a_matrix[i][j], factor))
           for j in range(2)] for i in range(2)]
    ddet = dadd(dmul(dd[0][0], dd[1][1]), dscale(-1, dmul(dd[0][1], dd[1][0])))
    dinv = [[ddivide(dd[1][1], ddet), ddivide(dscale(-1, dd[0][1]), ddet)],
            [ddivide(dscale(-1, dd[1][0]), ddet), ddivide(dd[0][0], ddet)]]
    ta = dual(0)
    for i in range(2):
        for j in range(2):
            ta = dadd(ta, dscale(a_matrix[j][i], dinv[i][j]))
    return dmul(dmul(scalar_product, ell), ta)


calibration_corners = [Q(9, 10), Q(7, 8), Q(17, 20)]
scalar_product = Q(1)
for cc in calibration_corners:
    scalar_product *= cc**2
ell = sum(1 / cc for cc in calibration_corners)
dm = [[(1 - Z if i == j else 0) + Z * Q(3, 5) * scalar_product * AP[i][j]
       for j in range(2)] for i in range(2)]
dinv = inverse2(dm)
ta = trproduct(dinv, AP)
bb = (Z * Q(3, 5) * scalar_product
      * trproduct(product2(dinv, dinv), product2(AP, AP)) / ta)
require("multi-corner gain spectral average lies in original interval", 0 <= bb <= Z)
for coordinate, cc in enumerate(calibration_corners):
    cduals = [dual(value, int(j == coordinate))
              for j, value in enumerate(calibration_corners)]
    gain_dual = independent_gain_dual(AP, cduals, Q(3, 5))
    slope = cc * gain_dual[1] / gain_dual[0]
    weight = 1 / (cc * ell)
    require(f"independent actual gain exact log partial j={coordinate}",
            slope == 2 * (1 - bb) - weight)
    require(f"independent actual gain positive bounded partial j={coordinate}",
            1 - 2 * Z <= slope <= 2)


# Matrix effective-z identity, including its absolute baseline.
eta = Q(3, 5)
rr = Q(1, 9)
aa = Q(1, 3)
cc = 1 - 2 * aa * rr
D0 = [[(1 - Z if i == j else 0) + Z * eta * AP[i][j]
       for j in range(2)] for i in range(2)]
ZMAT = [[Z * eta * x for x in row] for row in product2(AP, inverse2(D0))]
remaining = [[Q(i == j) - (1 - cc**2) * ZMAT[i][j]
              for j in range(2)] for i in range(2)]
D = [[(1 - Z if i == j else 0) + Z * eta * cc**2 * AP[i][j]
      for j in range(2)] for i in range(2)]
require("whole matrix determinant retains exact baseline",
        det2(D) == det2(D0) * det2(remaining))
require("two true protected columns occur in determinant",
        det2(D) != D[0][0])


# Relative-power compiler bound. exp(1/2)<2, so the rational sufficient
# bound below consumes M*delta/c_min <=1/4 and uses no floating arithmetic.
CMIN = Q(33, 40)
for repeats in (1, 3, 17):
    cc = Q(9, 10)
    delta = CMIN / (8 * repeats)
    cold_product = Q(1)
    for index in range(repeats):
        offset = delta if index % 2 == 0 else -delta / 2
        cold_product *= (cc + offset)**2
    difference = abs(cold_product - cc ** (2 * repeats))
    upper = 4 * repeats * delta * cc ** (2 * repeats - 1)
    require(f"relative full-copy product bound M={repeats}", difference <= upper)
    require(f"literal finite copy return is nonzero M={repeats}", cold_product > 0)


for independent_count in (3, 17):
    corners = [Q(17, 20) + Q(j, 20 * independent_count)
               for j in range(independent_count)]
    delta = CMIN / (8 * independent_count)
    ell = sum(1 / cc for cc in corners)
    ideal = Q(1)
    actual = Q(1)
    for j, cc in enumerate(corners):
        offset = delta if j % 2 == 0 else -delta / 2
        ideal *= cc**2
        actual *= (cc + offset)**2
    require(f"different-corner tolerance controls full product M={independent_count}",
            delta * ell <= Q(1, 4)
            and abs(actual - ideal) <= 4 * delta * ell * ideal)
    require(f"different actual corners retain nonzero return M={independent_count}",
            actual > 0)


# A finite arithmetic scenario, not an emitted huge GR-native circuit.
# N_base includes the declared 3-copy block and old prefix in this scenario.
repeats = 3
aa = Q(1, 3)
cc = Q(9, 10)
rf = Q(1, 7)
base_length = 26
step = Q(1, 1000)
target = Q(1, 10**12)
gamma_lower = 4 * repeats * aa * Z * cc**(2*repeats-1) * eps * rf * trace2(AP)
chi = Q(2, 55)
prefactor = Q(176, 359) / (1 - chi**2)
# Golden p > 3/5 gives a rational lower bound for p^K.
p_lower = Q(3, 5)
chosen_k = None
heat_bound = None
for k in range(101):
    n = base_length + 3 * k
    qn = chi**n / factorial(n)
    a1 = prefactor * qn / (1 - qn)**2
    debt = a1 / (step * gamma_lower * p_lower**k)
    if k >= 2 and debt < target:
        chosen_k = k
        heat_bound = debt
        break
require("finite post-compilation K search terminates in declared scenario",
        chosen_k is not None)
require("full heat divided by actual exponential gain meets target",
        heat_bound is not None and heat_bound < target)
require("all added stages counted", base_length + 3 * chosen_k > base_length)


receipt = {
    "status": "PASS",
    "source_input": "c296829fc2e74d673a2a679baa1e10a49524b290",
    "arithmetic": "Python standard-library Fraction; sparse formal (p,x,y) polynomial; exact dual determinant",
    "checks_passed": len(CHECKS),
    "checks": CHECKS,
    "changed_results": {
        "pf_row": "Full normalized PF tangent has no constant or linear field source; actual residual is retained.",
        "past": "Moving noncommuting and rank-deficient nonzero past satisfy the exact pointwise-gain formula.",
        "copies": "Actual scalar WORK copies retain a relative-power error bound and nonzero return.",
        "independent_copies": "The exact weighted full-covector formula covers independent current data; max-product dual norm retains all block rows and their individual signs.",
        "independent_calibration": "Each actual gain log partial is exactly 2*(1-b)-w_j in [1-2*z,2]; different positive corners retain the relative-product bound.",
        "heat_scenario": {
            "base_length": base_length,
            "repeats": repeats,
            "chosen_retention_k": chosen_k,
            "full_clock_length": base_length + 3 * chosen_k,
            "target": str(target),
            "bound_below_target": True,
        },
    },
    "scope": "Changed algebra and finite arithmetic bounds; no huge native word emission, geometry replay, exact finite stationary roots, or universal physical GR claim.",
    "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
