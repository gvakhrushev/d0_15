#!/usr/bin/env python3
"""Exact finite cubic-source/range probe for the crossed-null Cartan system.

The probe continues the exact [a*b] saddle on the original six based
plaquettes. It retains proper Lorentz links by exponentiating a Lorentz
algebra jet, includes all amplitude monomials through total degree 3, and
uses the actual 24 link and 16 coframe first variations. It constructs a
symbolic local polynomial response that closes all 40 finite Euler rows
through degree 3 for arbitrary orthogonal affine gradients. It does not
assert a periodic carrier root, an all-order finite solution, or physical GR.
"""
import itertools
import math
import sympy as s

import check_mixed_cartan_exact as mixed


MAX_DEGREE = 3
AMPLITUDES = ((0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2),
              (3, 0), (2, 1), (1, 2), (0, 3))
SPATIAL = tuple((i, d - i) for d in range(4) for i in range(d, -1, -1))
X, Y = s.symbols("x y", real=True)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


class Jet:
    """Scalar polynomial in a,b, truncated only above total degree three."""
    __slots__ = ("c",)

    def __init__(self, terms=None):
        self.c = {}
        if isinstance(terms, Jet):
            self.c = dict(terms.c)
        elif isinstance(terms, dict):
            for key, value in terms.items():
                if sum(key) <= MAX_DEGREE and value != 0:
                    self.c[key] = s.expand(value)
        elif terms is not None and terms != 0:
            self.c[(0, 0)] = s.sympify(terms)

    def __add__(self, other):
        other = Jet(other)
        result = dict(self.c)
        for key, value in other.c.items():
            result[key] = s.expand(result.get(key, 0) + value)
        return Jet(result)

    __radd__ = __add__

    def __neg__(self):
        return Jet({key: -value for key, value in self.c.items()})

    def __sub__(self, other):
        return self + (-Jet(other))

    def __rsub__(self, other):
        return Jet(other) - self

    def __mul__(self, other):
        other = Jet(other)
        result = {}
        for (i, j), left in self.c.items():
            for (k, ell), right in other.c.items():
                if i + j + k + ell <= MAX_DEGREE:
                    key = (i + k, j + ell)
                    result[key] = s.expand(result.get(key, 0) + left * right)
        return Jet(result)

    __rmul__ = __mul__

    def scale(self, value):
        return Jet({key: s.expand(value * coeff)
                    for key, coeff in self.c.items()})

    def diff(self, variable):
        return Jet({key: s.diff(value, variable)
                    for key, value in self.c.items()})

    def coeff(self, key):
        return self.c.get(key, s.Integer(0))


def zmat(rows=4, cols=4):
    return [[Jet() for _ in range(cols)] for _ in range(rows)]


def mat_from_sympy(value):
    return [[Jet(value[i, j]) for j in range(value.cols)]
            for i in range(value.rows)]


def mat_add(left, right):
    return [[left[i][j] + right[i][j] for j in range(len(left[0]))]
            for i in range(len(left))]


def mat_scale(matrix, value):
    return [[entry.scale(value) for entry in row] for row in matrix]


def mat_mul(left, right):
    out = zmat(len(left), len(right[0]))
    for i in range(len(left)):
        for k in range(len(right)):
            if not left[i][k].c:
                continue
            for j in range(len(right[0])):
                if right[k][j].c:
                    out[i][j] = out[i][j] + left[i][k] * right[k][j]
    return out


def mat_transpose(matrix):
    return [[matrix[i][j] for i in range(len(matrix))]
            for j in range(len(matrix[0]))]


def mat_coeff(matrix, amplitude):
    return s.Matrix([[entry.coeff(amplitude) for entry in row]
                     for row in matrix])


def mat_replace_coeff(matrix, amplitude, value):
    result = [[Jet(entry) for entry in row] for row in matrix]
    for i in range(len(result)):
        for j in range(len(result[0])):
            terms = dict(result[i][j].c)
            if value[i, j] == 0:
                terms.pop(amplitude, None)
            else:
                terms[amplitude] = s.expand(value[i, j])
            result[i][j] = Jet(terms)
    return result


def exp_lorentz(logarithm):
    identity = mat_from_sympy(s.eye(4))
    square = mat_mul(logarithm, logarithm)
    cube = mat_mul(square, logarithm)
    return mat_add(mat_add(mat_add(identity, logarithm),
                           mat_scale(square, s.Rational(1, 2))),
                   mat_scale(cube, s.Rational(1, 6)))


def check_lorentz_links(logs):
    """Verify the log and its cubic exponential obey the Lorentz constraint."""
    eta = mat_from_sympy(ETA)
    for direction, logarithm in enumerate(logs):
        for amplitude in AMPLITUDES:
            coefficient = mat_coeff(logarithm, amplitude)
            defect = coefficient.T * ETA + ETA * coefficient
            require(all(exact_zero(defect[i, j])
                        for i in range(4) for j in range(4)),
                    f"link log {direction} is not Lorentz at {amplitude}")
        link_value = exp_lorentz(logarithm)
        metric = mat_mul(mat_mul(mat_transpose(link_value), eta), link_value)
        for amplitude in AMPLITUDES:
            value = mat_coeff(metric, amplitude)
            expected = ETA if amplitude == (0, 0) else s.zeros(4)
            require(all(exact_zero(value[i, j] - expected[i, j])
                        for i in range(4) for j in range(4)),
                    f"exponentiated link {direction} is not proper Lorentz at {amplitude}")


I = s.eye(4)
ETA = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                [0, 0, -1, 0], [0, 0, 0, -1]])
E = lambda i, j: s.Matrix(4, 4,
                          lambda k, ell: int(i == k and j == ell))
NPLUS = (E(1, 2) + E(2, 0), E(1, 3) + E(3, 0))
NMINUS = (E(0, 2) + E(2, 1), E(0, 3) + E(3, 1))
BOOST = E(1, 1) - E(0, 0)
PAIRS = list(itertools.combinations(range(4), 2))
GENERATORS = [(E(i, j) - E(j, i)) * ETA for i, j in PAIRS]


def epsilon(*indices):
    if len(set(indices)) != 4:
        return 0
    sign = 1
    for i in range(4):
        for j in range(i + 1, 4):
            if indices[i] > indices[j]:
                sign = -sign
    return sign


def shift(point, axis, amount=1):
    result = list(point)
    result[axis] += amount
    return tuple(result)


def profiles(point, A, B, cubic=True, hcoef=s.Rational(-1, 32),
             jcoef=s.Rational(-1, 32)):
    x, y = point[2], point[3]
    ax, ay = A
    bx, by = B
    aa, bb = ax**2 + ay**2, bx**2 + by**2
    Alinear, Blinear = ax*x + ay*y, bx*x + by*y
    radius = x*x + y*y
    H = Jet({(1, 0): Alinear})
    J = Jet({(0, 1): Blinear})
    if cubic:
        H += Jet({(2, 1): hcoef * aa * Blinear * radius})
        J += Jet({(1, 2): jcoef * bb * Alinear * radius})
    return H, J


def coframe(point, A, B, cubic=True, hcoef=s.Rational(-1, 32),
            jcoef=s.Rational(-1, 32), coframe_modes=None):
    H, J = profiles(point, A, B, cubic, hcoef, jcoef)
    result = mat_from_sympy(I)
    result[1][0] = result[1][0] + H.scale(s.Rational(1, 2))
    result[0][1] = result[0][1] + J.scale(s.Rational(1, 2))
    if coframe_modes is not None:
        for (amplitude, row, col), value in coframe_modes(point).items():
            result[row][col] = result[row][col] + Jet({amplitude: value})
    return result


def lc_log(point, A, B, cubic=True, hcoef=s.Rational(-1, 32),
           jcoef=s.Rational(-1, 32)):
    """Full double-null continuum LC one-form through amplitude degree 3."""
    H, J = profiles(point, A, B, cubic, hcoef, jcoef)
    x, y = point[2], point[3]
    inv_omega = Jet(1) + (H * J).scale(s.Rational(1, 4))
    frame = coframe(point, A, B, cubic, hcoef, jcoef)
    wb = [zmat() for _ in range(4)]
    for i, variable in enumerate((X, Y)):
        dH, dJ = H.diff(variable), J.diff(variable)
        alpha = (dH * inv_omega).scale(s.Rational(1, 2))
        beta = (dJ * inv_omega).scale(s.Rational(1, 2))
        cross = ((H * dJ) + (J * dH)) * inv_omega
        cross = cross.scale(-s.Rational(1, 8))
        drift = ((J * dH) - (H * dJ)) * inv_omega
        drift = drift.scale(s.Rational(1, 8))
        for row in range(4):
            for col in range(4):
                wb[0][row][col] = wb[0][row][col] + alpha.scale(NPLUS[i][row, col]) + cross.scale(NMINUS[i][row, col])
                wb[1][row][col] = wb[1][row][col] + cross.scale(NPLUS[i][row, col]) + beta.scale(NMINUS[i][row, col])
                wb[i + 2][row][col] = wb[i + 2][row][col] + drift.scale(BOOST[row, col])
    result = [zmat() for _ in range(4)]
    for mu in range(4):
        for frame_index in range(4):
            for row in range(4):
                for col in range(4):
                    result[mu][row][col] = result[mu][row][col] + wb[frame_index][row][col] * frame[frame_index][mu]
    return result


def build_log_cache(A, B, cubic=True, gamma=None,
                    hcoef=s.Rational(-1, 32),
                    jcoef=s.Rational(-1, 32)):
    """LC log with the established exact finite mixed [a*b] coefficient."""
    cache = {}
    mixed.AA, mixed.BB = A, B
    mixed.x, mixed.y = X, Y
    mixed.CORR = mixed.correction(A, B)

    def get(point):
        if point not in cache:
            logs = lc_log(point, A, B, cubic, hcoef, jcoef)
            for axis in range(4):
                target = mixed.link(point, axis).c
                first_a, first_b, target_ab = target[1], target[2], target[3]
                group_cross = (first_a * first_b + first_b * first_a) / 2
                log_ab = target_ab - group_cross
                logs[axis] = mat_replace_coeff(logs[axis], (1, 1), log_ab)
                if gamma is not None:
                    add = gamma(point, axis)
                    for (added_axis, amplitude, row, col), coeff in add.items():
                        if added_axis != axis or coeff == 0:
                            continue
                        terms = dict(logs[axis][row][col].c)
                        terms[amplitude] = s.expand(terms.get(amplitude, 0) + coeff)
                        logs[axis][row][col] = Jet(terms)
            cache[point] = logs
        return cache[point]
    return get


def lorentz_inverse(matrix):
    eta = mat_from_sympy(ETA)
    return mat_mul(mat_mul(eta, mat_transpose(matrix)), eta)


def oriented_link(log_cache, point, axis, back=False):
    result = exp_lorentz(log_cache(point)[axis])
    return lorentz_inverse(result) if back else result


def edge_list(point, r, t):
    return ((point, r, False), (shift(point, r), t, False),
            (shift(point, t), r, True), (point, t, True))


def plaquette(point, r, t, log_cache, variation=None):
    product = mat_from_sympy(I)
    dproduct = zmat()
    for at, axis, back in edge_list(point, r, t):
        link_value = oriented_link(log_cache, at, axis, back)
        hit = variation is not None and at == variation[0] and axis == variation[1]
        if hit:
            Xmat = mat_from_sympy(variation[2])
            dlink = mat_mul(link_value, mat_scale(Xmat, -1)) if back else mat_mul(Xmat, link_value)
        else:
            dlink = zmat()
        dproduct = mat_add(mat_mul(dproduct, link_value),
                           mat_mul(product, dlink))
        product = mat_mul(product, link_value)
    return product, dproduct


def scalar_pair(frame, u, v, curvature):
    curvature_eta = mat_mul(curvature, mat_from_sympy(ETA))
    out = Jet()
    for a, b in PAIRS:
        c, d = [k for k in range(4) if k not in (a, b)]
        area = frame[a][u] * frame[b][v] - frame[b][u] * frame[a][v]
        out = out + (area * curvature_eta[c][d]).scale(epsilon(a, b, c, d))
    return out


def curvature_variation(point, r, t, log_cache, variation):
    P, dP = plaquette(point, r, t, log_cache, variation)
    Pinv = lorentz_inverse(P)
    dR = mat_scale(mat_add(dP, mat_mul(mat_mul(Pinv, dP), Pinv)),
                   s.Rational(1, 2))
    return P, dR


def link_rows(point, log_cache, A, B, cubic=True,
              hcoef=s.Rational(-1, 32), jcoef=s.Rational(-1, 32),
              coframe_modes=None):
    result = []
    for axis in range(4):
        for Xgen in GENERATORS:
            value = Jet()
            for r, t in PAIRS:
                if axis not in (r, t):
                    continue
                other = t if axis == r else r
                u, v = [k for k in range(4) if k not in (r, t)]
                for base in (point, shift(point, other, -1)):
                    _, dR = curvature_variation(base, r, t, log_cache,
                                                 (point, axis, Xgen))
                    value = value + scalar_pair(coframe(base, A, B, cubic,
                                                        hcoef, jcoef,
                                                        coframe_modes),
                                                u, v, dR).scale(epsilon(r, t, u, v))
            result.append(value)
    return result


def replace_coframe_column(frame, column, internal):
    result = [[Jet(entry) for entry in row] for row in frame]
    for row in range(4):
        result[row][column] = Jet(int(row == internal))
    return result


def solder_rows(point, log_cache, A, B, cubic=True,
                hcoef=s.Rational(-1, 32), jcoef=s.Rational(-1, 32),
                coframe_modes=None):
    result = [Jet() for _ in range(16)]
    frame = coframe(point, A, B, cubic, hcoef, jcoef, coframe_modes)
    for r, t in PAIRS:
        u, v = [k for k in range(4) if k not in (r, t)]
        sign = epsilon(r, t, u, v)
        P, _ = plaquette(point, r, t, log_cache)
        curvature = mat_scale(mat_add(P, mat_scale(lorentz_inverse(P), -1)),
                              s.Rational(1, 2))
        for internal in range(4):
            result[4 * internal + u] = result[4 * internal + u] + scalar_pair(
                replace_coframe_column(frame, u, internal), u, v,
                curvature).scale(sign)
            result[4 * internal + v] = result[4 * internal + v] + scalar_pair(
                replace_coframe_column(frame, v, internal), u, v,
                curvature).scale(sign)
    return result


def exact_zero(value):
    return s.simplify(s.expand(value)) == 0


def gamma_field(solutions, spatial_monomials=None):
    """Turn coefficient vectors into site-varying Lie-algebra link jets."""
    def get(point, axis):
        result = {}
        for amplitude, vector in solutions.items():
            for generator_index, generator in enumerate(GENERATORS):
                if spatial_monomials is None:
                    coefficient = vector[6 * axis + generator_index].subs(
                        {X: point[2], Y: point[3]})
                else:
                    count = len(spatial_monomials)
                    offset = (axis * 6 + generator_index) * count
                    coefficient = sum(
                        vector[offset + n] * point[2]**i * point[3]**j
                        for n, (i, j) in enumerate(spatial_monomials))
                coefficient = s.expand(coefficient)
                if coefficient == 0:
                    continue
                for row in range(4):
                    for col in range(4):
                        value = coefficient * generator[row, col]
                        if value != 0:
                            key = (axis, amplitude, row, col)
                            result[key] = s.expand(result.get(key, 0) + value)
        return result
    return get


def coframe_field(solutions, spatial_monomials):
    """Turn 16 coframe coefficient polynomials into site-varying matrix jets."""
    def get(point):
        result = {}
        monomial_count = len(spatial_monomials)
        for amplitude, vector in solutions.items():
            for row in range(4):
                for col in range(4):
                    entry = row * 4 + col
                    expression = 0
                    for spatial_index, (i, j) in enumerate(spatial_monomials):
                        coefficient = vector[entry * monomial_count + spatial_index]
                        expression += coefficient * point[2]**i * point[3]**j
                    expression = s.expand(expression)
                    if expression != 0:
                        result[(amplitude, row, col)] = expression
        return result
    return get


def poly_degree(expr):
    if exact_zero(expr):
        return -1
    return s.Poly(s.expand(expr), X, Y).total_degree()


def solve_cubic_link_rows(A, B, hcoef=s.Rational(-1, 32),
                          jcoef=s.Rational(-1, 32),
                          coframe_modes=None):
    """Solve full affine-polynomial cubic link rows using the exact flat Hessian."""
    point = (0, 0, X, Y)
    base = build_log_cache(A, B, cubic=True,
                           hcoef=hcoef, jcoef=jcoef)
    source = link_rows(point, base, A, B, True, hcoef, jcoef,
                       coframe_modes)
    M = mixed.flat_hessian()
    require(M.rank() == 24 and M.det() == 256,
            "flat link Hessian is not the proved nonsingular 24x24 block")
    inverse = M.inv()
    solutions = {
        amplitude: -inverse * s.Matrix([row.coeff(amplitude) for row in source])
        for amplitude in ((2, 1), (1, 2))
    }
    for amplitude, vector in solutions.items():
        require(max(poly_degree(entry) for entry in vector) <= 1,
                "cubic link source exceeded the affine polynomial ansatz")

    # A pointwise inverse leaves only a constant neighbor-stencil defect for
    # this affine source. Cancel that exact defect with the same zero-mode M.
    first_cache = build_log_cache(A, B, cubic=True,
                                  gamma=gamma_field(solutions),
                                  hcoef=hcoef, jcoef=jcoef)
    first_rows = link_rows(point, first_cache, A, B, True, hcoef, jcoef,
                           coframe_modes)
    for amplitude in ((2, 1), (1, 2)):
        residual = [s.expand(row.coeff(amplitude)) for row in first_rows]
        require(max(poly_degree(entry) for entry in residual) <= 0,
                "neighbor stencil leaves a nonconstant cubic link residual")
        constant = s.Matrix([s.expand(entry).subs({X: 0, Y: 0})
                             for entry in residual])
        solutions[amplitude] += -inverse * constant

    final_cache = build_log_cache(A, B, cubic=True,
                                  gamma=gamma_field(solutions),
                                  hcoef=hcoef, jcoef=jcoef)
    final_rows = link_rows(point, final_cache, A, B, True, hcoef, jcoef,
                           coframe_modes)
    for amplitude in ((1, 1), (2, 1), (1, 2)):
        require(all(exact_zero(row.coeff(amplitude)) for row in final_rows),
                "full cubic 24-link system did not close")
    return final_cache, source, solutions, final_rows


def monomials(max_degree):
    return tuple((i, degree - i) for degree in range(max_degree + 1)
                 for i in range(degree, -1, -1))


def polynomial_coefficient(expression, monomial):
    expression = s.expand(expression)
    if exact_zero(expression):
        return s.Integer(0)
    polynomial = s.Poly(expression, X, Y)
    return polynomial.coeff_monomial(X**monomial[0] * Y**monomial[1])


def response_vector(link_equations, coframe_equations, amplitude,
                    link_output_monomials, coframe_output_monomials):
    result = []
    for row in link_equations:
        expression = row.coeff(amplitude)
        for monomial in link_output_monomials:
            result.append(polynomial_coefficient(expression, monomial))
    for row in coframe_equations:
        expression = row.coeff(amplitude)
        for monomial in coframe_output_monomials:
            result.append(polynomial_coefficient(expression, monomial))
    return s.Matrix(result)


def merge_gamma_fields(*fields):
    def get(point, axis):
        result = {}
        for field in fields:
            if field is None:
                continue
            for key, value in field(point, axis).items():
                result[key] = s.expand(result.get(key, 0) + value)
        return result
    return get


def solve_full_cubic_40(A, B):
    """Solve the coupled flat-Hessian correction to all 40 cubic Euler rows.

    The finite source is first evaluated on the source-forced H/J profile and
    its exact cubic 24-link lift. We then solve for an additional quadratic
    spatial polynomial in the original 16 coframe components and degree<=2
    Lorentz-link jets. The flat response is evaluated from the same six
    plaquettes, not a continuum Einstein operator.
    """
    amplitude_aab, amplitude_abb = (2, 1), (1, 2)
    base_cache, _, base_link_solutions, base_link_rows = solve_cubic_link_rows(A, B)
    point = (0, 0, X, Y)
    base_coframe_rows = solder_rows(point, base_cache, A, B)
    require(all(exact_zero(row.coeff((1, 1))) for row in base_coframe_rows),
            "mixed quadratic coframe source is nonzero on orthogonal input")

    link_monos = monomials(2)
    coframe_monos = monomials(2)
    link_output_monos = monomials(2)
    coframe_output_monos = monomials(1)
    amplitudes = (amplitude_aab, amplitude_abb)
    flat_A, flat_B = (0, 0), (0, 0)
    n_link_coeffs = 24 * len(link_monos)
    n_coframe_coeffs = 16 * len(coframe_monos)
    variables = s.symbols(f"u0:{n_link_coeffs + n_coframe_coeffs}")
    gamma = gamma_field({amplitude_aab:
                         s.Matrix(variables[:n_link_coeffs])}, link_monos)
    modes = coframe_field({amplitude_aab:
                           s.Matrix(variables[n_link_coeffs:])}, coframe_monos)
    cache = build_log_cache(flat_A, flat_B, cubic=False, gamma=gamma,
                            hcoef=0, jcoef=0)
    link_eq = link_rows(point, cache, flat_A, flat_B, cubic=False,
                        hcoef=0, jcoef=0, coframe_modes=modes)
    coframe_eq = solder_rows(point, cache, flat_A, flat_B, cubic=False,
                             hcoef=0, jcoef=0, coframe_modes=modes)
    symbolic_response = response_vector(link_eq, coframe_eq, amplitude_aab,
                                        link_output_monos,
                                        coframe_output_monos)
    operator = symbolic_response.jacobian(variables)
    require(all(exact_zero(symbolic_response[i] -
                           sum(operator[i, j] * variables[j]
                               for j in range(len(variables))))
                for i in range(symbolic_response.rows)),
            "flat cubic Euler response is not linear in correction modes")
    require(operator.rows == 24 * len(link_output_monos) +
            16 * len(coframe_output_monos) and
            operator.cols == n_link_coeffs + n_coframe_coeffs,
            "coupled cubic polynomial operator has wrong dimensions")
    extra = {}
    for amplitude in amplitudes:
        rhs = -response_vector(base_link_rows, base_coframe_rows, amplitude,
                               link_output_monos, coframe_output_monos)
        solution, parameters = operator.gauss_jordan_solve(rhs)
        if parameters.rows:
            solution = solution.subs({parameter: 0 for parameter in parameters})
        link_solution = solution[:n_link_coeffs, :]
        coframe_solution = solution[n_link_coeffs:, :]
        extra[amplitude] = (link_solution, coframe_solution)

    gamma_parts = [gamma_field(base_link_solutions)]
    coframe_solutions = {}
    for amplitude, (link_solution, coframe_solution) in extra.items():
        gamma_parts.append(gamma_field({amplitude: link_solution}, link_monos))
        coframe_solutions[amplitude] = coframe_solution
    total_gamma = merge_gamma_fields(*gamma_parts)
    modes = coframe_field(coframe_solutions, coframe_monos)
    final_cache = build_log_cache(A, B, cubic=True, gamma=total_gamma)
    final_link = link_rows(point, final_cache, A, B, True,
                           coframe_modes=modes)
    final_coframe = solder_rows(point, final_cache, A, B, True,
                                coframe_modes=modes)
    for amplitude in ((1, 1), amplitude_aab, amplitude_abb):
        require(all(exact_zero(row.coeff(amplitude)) for row in final_link),
                "coupled cubic solve leaves a finite link Euler source")
        require(all(exact_zero(row.coeff(amplitude)) for row in final_coframe),
                "coupled cubic solve leaves a finite coframe Euler source")
    return operator, extra, final_cache, final_link, final_coframe


def main():
    A, B = (1, 0), (0, 1)
    point = (0, 0, X, Y)
    cache, source, corrections, rows = solve_cubic_link_rows(A, B)
    check_lorentz_links(cache(point))
    require(all(exact_zero(row.coeff((1, 1))) for row in rows),
            "the established exact mixed [a*b] link root regressed")
    for amplitude in ((2, 1), (1, 2)):
        before = [s.factor(row.coeff(amplitude)) for row in source]
        nonzero = [(i, value) for i, value in enumerate(before) if value != 0]
        print("PASS source-forced cubic link coefficient", amplitude,
              "nonzero rows", len(nonzero))
    print("PASS exact site-varying proper-Lorentz cubic correction solves all 24 links")
    solder = solder_rows(point, cache, A, B)
    require(all(exact_zero(row.coeff((1, 1))) for row in solder),
            "the established exact mixed [a*b] coframe root regressed")
    expected_aab = [s.Integer(0)] * 16
    expected_aab[3], expected_aab[13] = -s.Rational(5, 32), s.Rational(5, 32)
    expected_abb = [s.Integer(0)] * 16
    expected_abb[6], expected_abb[8] = -s.Rational(5, 32), s.Rational(5, 32)
    require(all(exact_zero(solder[i].coeff((2, 1)) - expected_aab[i])
                for i in range(16)), "unit orthogonal cubic coframe source changed")
    require(all(exact_zero(solder[i].coeff((1, 2)) - expected_abb[i])
                for i in range(16)), "unit orthogonal cubic coframe source changed")
    print("Before the coupled coframe response, the link-only lift leaves this",
          "16-row source at A=(1,0), B=(0,1):",
          "[a^2*b] rows 3=-5/32,13=5/32;",
          "[a*b^2] rows 6=-5/32,8=5/32.")

    c, d = s.symbols("c d", real=True)
    tuned, _, _, _ = solve_cubic_link_rows(A=(1, 0), B=(0, 1),
                                           hcoef=c, jcoef=d)
    tuned_solder = solder_rows(point, tuned, (1, 0), (0, 1),
                               hcoef=c, jcoef=d)
    require(exact_zero(tuned_solder[1].coeff((2, 1)) +
                       Y * (32*c + 1) / 8) and
            exact_zero(tuned_solder[3].coeff((2, 1)) + s.Rational(5, 32)) and
            exact_zero(tuned_solder[13].coeff((2, 1)) - s.Rational(5, 32)),
            "H cubic radial tuning must leave two independent a^2*b coframe rows")
    require(exact_zero(tuned_solder[4].coeff((1, 2)) +
                       X * (32*d + 1) / 8) and
            exact_zero(tuned_solder[6].coeff((1, 2)) + s.Rational(5, 32)) and
            exact_zero(tuned_solder[8].coeff((1, 2)) - s.Rational(5, 32)),
            "J cubic radial tuning must leave two independent a*b^2 coframe rows")
    print("PASS hostile radial H/J tuning: four mixed coframe rows remain")

    mesh, r, q, k = s.symbols("mesh r q k", real=True)
    # At lattice sites n, these are the samples of the fixed physical
    # affine profiles at x=mesh*n. This makes the mesh scaling explicit.
    A, B = (mesh * r, mesh * q), (-mesh * k * q, mesh * k * r)
    cache, _, _, rows = solve_cubic_link_rows(A, B)
    check_lorentz_links(cache(point))
    require(all(exact_zero(row.coeff((2, 1))) and
                exact_zero(row.coeff((1, 2))) for row in rows),
            "arbitrary orthogonal cubic 24-link source did not close")
    solder = solder_rows(point, cache, A, B)
    norm_a = r*r + q*q
    expected_aab = [s.Integer(0)] * 16
    expected_aab[2] = 5*mesh**3*k*q*norm_a/32
    expected_aab[3] = -5*mesh**3*k*r*norm_a/32
    expected_aab[9] = -5*mesh**3*k*q*norm_a/32
    expected_aab[13] = 5*mesh**3*k*r*norm_a/32
    expected_abb = [s.Integer(0)] * 16
    expected_abb[6] = -5*mesh**3*k*k*r*norm_a/32
    expected_abb[7] = -5*mesh**3*k*k*q*norm_a/32
    expected_abb[8] = 5*mesh**3*k*k*r*norm_a/32
    expected_abb[12] = 5*mesh**3*k*k*q*norm_a/32
    require(all(exact_zero(solder[i].coeff((2, 1)) - expected_aab[i])
                for i in range(16)), "symbolic cubic coframe source mismatch")
    require(all(exact_zero(solder[i].coeff((1, 2)) - expected_abb[i])
                for i in range(16)), "symbolic cubic coframe source mismatch")
    print("PASS symbolic arbitrary orthogonal cubic 24-link closure for mesh h")
    print("PASS exact cubic coframe residual scales as h^3 on fixed physical profiles")

    # The 24-link lift leaves a coframe source when H_3,J_3 are the only
    # allowed corrections. Release every original coframe component and solve
    # the coupled finite 24+16 response at both mixed cubic amplitudes.
    # Keeping A,B symbolic proves this for the full orthogonal affine family,
    # not just the preferred coordinate axes.
    r, q, scale = s.symbols("r q scale", real=True)
    A, B = (r, q), (-scale*q, scale*r)
    operator, extra, complete_cache, complete_link, complete_coframe = \
        solve_full_cubic_40(A, B)
    require(operator.shape == (192, 240),
            "coupled cubic response operator has changed dimension")
    check_lorentz_links(complete_cache(point))
    cubic_amplitudes = monomials(MAX_DEGREE)
    for amplitude in cubic_amplitudes:
        require(all(exact_zero(row.coeff(amplitude))
                    for row in complete_link),
                f"coupled cubic lift leaves a link row at {amplitude}")
        require(all(exact_zero(row.coeff(amplitude))
                    for row in complete_coframe),
                f"coupled cubic lift leaves a coframe row at {amplitude}")
    print("PASS symbolic coupled original 24-link + 16-coframe cubic lift")
    print("PASS all 400 Euler coefficient identities through total degree 3")
    print("PASS proper-Lorentz link constraint through total degree 3")
    print("SCOPE: a local polynomial finite-stencil perturbative jet on the")
    print("unwrapped transverse lattice; no periodic-carrier root, all-order")
    print("solution, same-programme Cost-Info selection, or physical GR closure.")


if __name__ == "__main__":
    main()
