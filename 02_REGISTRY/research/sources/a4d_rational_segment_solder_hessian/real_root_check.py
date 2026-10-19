#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=900
"""Real roots of the degree-70 cofactor on one Cayley segment.

The segment is the straight generator line already used by check.py. This
script does not reopen the rational classification. It decides, by exact
arithmetic, whether the primitive cofactor q has a real root in an interval
on which all four Cayley charts stay open. Descartes' rule on one rational
interval is the witness. A root is not a stationary witness, its kernel is
not computed, and this segment is not the full-affine family.

Status of the result is candidate.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
from fractions import Fraction
from math import gcd
from pathlib import Path

import sympy as sp


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


ROOT = Path(__file__).resolve().parents[4]
OWNER_PATH = ROOT / (
    "02_REGISTRY/research/certificates/"
    "a4d_resolved_curved_stationary_e2_support7_order1_check.py"
)
C_PUBLISHED = 3117343613342156762592422345852808301028220510142464
EXPECTED_DET_S1 = sp.Rational(
    40765604576726345069227791532913732955215768490597607321403042878734640884143996245433663881216,
    1043809895872838655329569143133917752420140067322792752999568729,
)
DISC = 33808
S = sp.symbols("s")


def trim(cs):
    out = list(cs)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def sign_variations(cs):
    last = 0
    count = 0
    for coeff in reversed(cs):
        if coeff == 0:
            continue
        sign = 1 if coeff > 0 else -1
        if last and sign != last:
            count += 1
        last = sign
    return count


def mul(left, right):
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if b:
                out[i + j] += a * b
    return out


def transformed(cs, a, b):
    """Cleared pullback whose positive roots are the roots of cs in (a, b)."""
    a = Fraction(a)
    b = Fraction(b)
    if not a < b:
        raise ValueError((a, b))
    den = a.denominator * b.denominator // gcd(a.denominator, b.denominator)
    width_a = a.numerator * (den // a.denominator)
    width_b = b.numerator * (den // b.denominator)
    degree = len(cs) - 1
    pow_one = [[1]]
    pow_lin = [[1]]
    cur_one = [1]
    cur_lin = [1]
    one_plus = [1, 1]
    linear = [width_b, width_a]
    for _ in range(degree):
        cur_one = mul(cur_one, one_plus)
        cur_lin = mul(cur_lin, linear)
        pow_one.append(cur_one)
        pow_lin.append(cur_lin)
    den_pow = [1]
    for _ in range(degree):
        den_pow.append(den_pow[-1] * den)
    image = [0] * (degree + 1)
    for k, coeff in enumerate(cs):
        if not coeff:
            continue
        term = mul(pow_lin[k], pow_one[degree - k])
        scale = coeff * den_pow[degree - k]
        for i, value in enumerate(term):
            image[i] += scale * value
    return trim(image)


def eval_at(cs, point):
    point = Fraction(point)
    acc = Fraction(0)
    for coeff in reversed(cs):
        acc = acc * point + coeff
    return acc


def isolate_interval(cs, left, right, found=None, depth=0):
    if found is None:
        found = []
    if depth > 10000:
        raise AssertionError("BISECTION_DID_NOT_SEPARATE")
    image = transformed(cs, left, right)
    variations = sign_variations(image)
    if variations == 0:
        return found
    if variations == 1:
        if len(image) - 1 != len(cs) - 1:
            raise AssertionError("ENDPOINT_ROOT_DROPPED_DEGREE")
        found.append((Fraction(left), Fraction(right)))
        return found
    mid = (Fraction(left) + Fraction(right)) / 2
    if eval_at(cs, mid) == 0:
        found.append((mid, mid))
    isolate_interval(cs, left, mid, found, depth + 1)
    isolate_interval(cs, mid, right, found, depth + 1)
    return found


def cauchy_bound(cs):
    lead = abs(cs[-1])
    height = max((abs(coeff) for coeff in cs[:-1]), default=1)
    return 2 + (height + lead - 1) // lead


def cmp_quad_root(point, sign):
    """Sign of point minus (-16 + sign*sqrt(DISC))/466."""
    left = 466 * Fraction(point) + 16
    square = left.numerator ** 2 - DISC * left.denominator ** 2
    if sign > 0:
        if left <= 0:
            return -1
        if square < 0:
            return -1
        if square > 0:
            return 1
        return 0
    if left >= 0:
        return 1
    if square > 0:
        return -1
    if square < 0:
        return 1
    return 0


LINEAR_WALLS = (Fraction(-2), Fraction(-1, 2), Fraction(1, 2), Fraction(2))


def on_linear_wall(point):
    return Fraction(point) in LINEAR_WALLS


def on_quad_wall(point):
    return cmp_quad_root(point, 1) == 0 or cmp_quad_root(point, -1) == 0


def component(point):
    point = Fraction(point)
    if on_linear_wall(point) or on_quad_wall(point):
        return None
    if point < -2:
        return "(-inf,-2)"
    if point < Fraction(-1, 2):
        return "(-2,-1/2)"
    if cmp_quad_root(point, -1) < 0:
        return "(-1/2,s-)"
    if cmp_quad_root(point, 1) < 0:
        return "(s-,s+)"
    if point < Fraction(1, 2):
        return "(s+,1/2)"
    if point < 2:
        return "(1/2,2)"
    return "(2,inf)"


def shrink_to_component(cs, left, right, depth=0):
    left, right = Fraction(left), Fraction(right)
    if depth > 128:
        raise AssertionError(("SHRINK_DEPTH", str(left), str(right)))
    if left == right:
        return left, right
    for wall in LINEAR_WALLS:
        if left < wall < right and eval_at(cs, wall) == 0:
            return wall, wall
    left_value = eval_at(cs, left)
    right_value = eval_at(cs, right)
    if left_value == 0:
        return left, left
    if right_value == 0:
        return right, right
    left_component = component(left)
    right_component = component(right)
    if left_component and left_component == right_component and left_value * right_value < 0:
        return left, right
    mid = (left + right) / 2
    mid_value = eval_at(cs, mid)
    if mid_value == 0:
        return mid, mid
    if sign_variations(transformed(cs, left, mid)) == 1:
        return shrink_to_component(cs, left, mid, depth + 1)
    if sign_variations(transformed(cs, mid, right)) == 1:
        return shrink_to_component(cs, mid, right, depth + 1)
    if left_value * mid_value < 0:
        return shrink_to_component(cs, left, mid, depth + 1)
    return shrink_to_component(cs, mid, right, depth + 1)


def classify_real_roots(cs, bound):
    cs = trim(cs)
    roots = []
    if eval_at(cs, 0) == 0:
        roots.append((Fraction(0), Fraction(0)))
    roots.extend(isolate_interval(cs, Fraction(-bound), Fraction(0)))
    roots.extend(isolate_interval(cs, Fraction(0), Fraction(bound)))
    open_roots = []
    wall_roots = []
    for left, right in roots:
        left, right = shrink_to_component(cs, left, right)
        if left == right:
            if on_linear_wall(left) or on_quad_wall(left):
                wall_roots.append(left)
            else:
                open_roots.append((left, right, component(left)))
            continue
        open_roots.append((left, right, component(left)))
    return open_roots, wall_roots


def binom_shift(cs, shift):
    degree = len(cs) - 1
    rows = [[1]]
    for k in range(1, degree + 1):
        previous = rows[-1]
        row = [1]
        for j in range(1, k):
            row.append(previous[j - 1] + previous[j])
        row.append(1)
        rows.append(row)
    powers = [1]
    for _ in range(degree):
        powers.append(powers[-1] * shift)
    out = [0] * (degree + 1)
    for k, coeff in enumerate(cs):
        if not coeff:
            continue
        for j in range(k + 1):
            out[j] += coeff * rows[k][j] * powers[k - j]
    return out


def run_controls():
    no_real, walls = classify_real_roots([1, 0, 1], 2)
    check("CONTROL_NO_REAL_ROOT", no_real == [] and walls == [])
    wall_open, wall_hits = classify_real_roots([-1, 2], 3)
    check("CONTROL_WALL_ROOT_NOT_OPEN", wall_open == [] and wall_hits == [Fraction(1, 2)])
    open_roots, open_walls = classify_real_roots([-2, 0, 1], 4)
    check(
        "CONTROL_OPEN_ROOTS_CAN_BE_SEEN",
        open_walls == []
        and len(open_roots) == 2
        and {item[2] for item in open_roots} == {"(-2,-1/2)", "(1/2,2)"},
    )
    shifted = binom_shift([-300, 1], 256)
    check("CONTROL_BOUND_CAN_FAIL", sign_variations(shifted) > 0)
    check(
        "CONTROL_COMPONENT_BETWEEN_QUAD_ROOTS",
        component(0) == "(s-,s+)" and component(Fraction(-1, 3)) == "(s-,s+)",
    )
    check("CONTROL_COMPONENT_BEFORE_NEGATIVE_QUAD_ROOT", component(Fraction(-9, 20)) == "(-1/2,s-)")
    check("CONTROL_COMPONENT_AFTER_POSITIVE_QUAD_ROOT", component(Fraction(3, 8)) == "(s+,1/2)")


def eval_poly(cs, point):
    acc = 0
    for coeff in reversed(cs):
        acc = acc * point + coeff
    return acc


def det_mod(rows, prime):
    size = len(rows)
    matrix = [row[:] for row in rows]
    det = 1
    for col in range(size):
        pivot = next((r for r in range(col, size) if matrix[r][col] % prime), None)
        if pivot is None:
            return 0
        if pivot != col:
            matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
            det = -det
        piv = matrix[col][col] % prime
        det = (det * piv) % prime
        inv = pow(piv, -1, prime)
        for row in range(col + 1, size):
            factor = (matrix[row][col] * inv) % prime
            if not factor:
                continue
            for entry in range(col, size):
                matrix[row][entry] = (matrix[row][entry] - factor * matrix[col][entry]) % prime
    return det % prime


def crt_symmetric(residues, mods):
    value = residues[0]
    modulus = mods[0]
    for residue, prime in zip(residues[1:], mods[1:]):
        inv = pow(modulus % prime, -1, prime)
        value += modulus * (((residue - value) % prime) * inv % prime)
        modulus *= prime
    if value * 2 > modulus:
        value -= modulus
    return value


def det_at(matrix, point, primes):
    rows = []
    for row in matrix:
        rows.append([eval_poly(cs, point) for cs in row])
    bound = 1
    for row in rows:
        bound *= sum(abs(value) for value in row) or 1
    if bound == 0:
        return 0
    residues = []
    mods = []
    produced = 1
    for prime in primes:
        residues.append(det_mod([[value % prime for value in row] for row in rows], prime))
        mods.append(prime)
        produced *= prime
        if produced > 2 * bound:
            return crt_symmetric(residues, mods)
    raise AssertionError("PRIME_POOL_TOO_SMALL")


def newton_monomial(values, nodes):
    coeff = [Fraction(value) for value in values]
    width = len(nodes)
    for order in range(1, width):
        for index in range(width - 1, order - 1, -1):
            coeff[index] = (coeff[index] - coeff[index - 1]) / (nodes[index] - nodes[index - order])
    poly = [coeff[-1]]
    for index in range(width - 2, -1, -1):
        node = nodes[index]
        nxt = [Fraction(0)] * (len(poly) + 1)
        for power, term in enumerate(poly):
            nxt[power] -= node * term
            nxt[power + 1] += term
        nxt[0] += coeff[index]
        poly = nxt
    out = []
    for term in poly:
        if term.denominator != 1:
            raise AssertionError("NON_INTEGER_DETERMINANT_COEFFICIENT")
        out.append(term.numerator)
    return trim(out)


def prime_pool(count):
    primes = []
    candidate = 100003
    while len(primes) < count:
        if sp.isprime(candidate):
            primes.append(candidate)
        candidate += 2
    return primes


def build_cleared_matrix(owner):
    rho, translation, link = sp.Rational(1), sp.Rational(0), sp.Rational(8, 3)
    amplitude = (
        sp.Rational(0),
        sp.Rational(0),
        sp.Rational(-10, 3),
        sp.Rational(-8, 3),
        sp.Rational(0),
        sp.Rational(4, 9),
        sp.Rational(0),
    )
    velocities = [
        -4 * rho * owner.K1 + translation * owner.N3,
        translation * owner.N3,
        link * owner.K1 - owner.N2,
        owner.N3,
    ]
    increments = [sp.zeros(4) for _ in range(4)]
    for coeff, (_, role, generator) in zip(amplitude, owner.SELECTED_SPECS):
        increments[role] += coeff * generator
    chart = [sp.Matrix(owner.generators0[r] + velocities[r] + increments[r]) for r in range(4)]
    seed = [sp.Matrix(block) for block in owner.generators0]
    generators = [sp.expand(seed[r] + S * (chart[r] - seed[r])) for r in range(4)]
    chart_polys = [
        sp.Poly(sp.expand((owner.I4 - block / 2).det()), S, domain=sp.QQ) for block in generators
    ]
    expected = [
        sp.Poly(sp.together(-2 * (2 * S - 1) * (2 * S + 1)), S, domain=sp.QQ),
        sp.Poly(2, S, domain=sp.QQ),
        sp.Poly(sp.together(-(233 * S ** 2 + 16 * S - 36) / 36), S, domain=sp.QQ),
        sp.Poly(sp.together(-(S - 2) * (S + 2) / 4), S, domain=sp.QQ),
    ]
    check("CHART_DENOMINATORS", chart_polys == expected)
    quad = sp.Poly(233 * S ** 2 + 16 * S - 36, S, domain=sp.ZZ)
    check("ROLE2_DISCRIMINANT", sp.discriminant(quad.as_expr(), S) == DISC)
    check("ROLE2_DISCRIMINANT_NOT_SQUARE", sp.integer_nthroot(DISC, 2)[1] is False)
    # -2 < -1/2 < s- < s+ < 1/2 < 2, with s± = (-16 ± sqrt(DISC))/466.
    check("WALL_ORDER_LEFT", 217 ** 2 > DISC)
    check("WALL_ORDER_RIGHT", 249 ** 2 > DISC)

    def face_response(roles, left, right):
        holonomy = roles[left] * roles[right] * roles[left].inv() * roles[right].inv()
        curvature = (holonomy - holonomy.inv()) / 2
        return owner.orientation((left, right)) * (
            owner.G2 * owner.STAR * owner.bivector_of_tangent(curvature)
        )

    roles = [sp.together(owner.cayley(block)) for block in generators]
    rows = [[sp.Integer(0) for _ in range(16)] for _ in range(16)]
    for left, right in owner.PAIRS:
        response = face_response(roles, left, right)
        untouched = [index for index in range(4) if index not in (left, right)]
        for slot, (a, b) in enumerate(owner.PAIRS):
            for i, j, value in ((a, b, response[slot]), (b, a, -response[slot])):
                rows[4 * i + untouched[0]][4 * j + untouched[1]] += 16 * value
                rows[4 * j + untouched[1]][4 * i + untouched[0]] += 16 * value

    reduced = []
    den_lcm = sp.Poly(1, S, domain=sp.ZZ)
    max_degree = 0
    for i in range(16):
        for j in range(i, 16):
            value = sp.together(sp.expand(rows[i][j]))
            if value == 0:
                reduced.append((i, j, sp.Poly(0, S, domain=sp.ZZ), sp.Poly(1, S, domain=sp.ZZ)))
                continue
            numerator, denominator = sp.fraction(value)
            num_poly = sp.Poly(sp.expand(numerator), S, domain=sp.ZZ)
            den_poly = sp.Poly(sp.expand(denominator), S, domain=sp.ZZ)
            common = sp.gcd(num_poly, den_poly)
            num_poly = sp.div(num_poly, common, domain=sp.ZZ)[0]
            den_poly = sp.div(den_poly, common, domain=sp.ZZ)[0]
            den_lcm = sp.lcm(den_lcm, den_poly)
            max_degree = max(max_degree, num_poly.degree())
            reduced.append((i, j, num_poly, den_poly))
    delta = sp.Poly(
        sp.expand(
            81
            * (S - 2) ** 2
            * (S + 2) ** 2
            * (2 * S - 1) ** 2
            * (2 * S + 1) ** 2
            * (233 * S ** 2 + 16 * S - 36) ** 2
        ),
        S,
        domain=sp.ZZ,
    )
    check("DENOMINATOR_IS_DELTA", den_lcm == delta)
    matrix = [[sp.Poly(0, S, domain=sp.ZZ) for _ in range(16)] for _ in range(16)]
    cleared_degree = 0
    for i, j, num_poly, den_poly in reduced:
        quot, rem = sp.div(den_lcm, den_poly, domain=sp.QQ)
        if rem != 0:
            raise AssertionError("DENOMINATOR_DOES_NOT_DIVIDE_DELTA")
        cleared = sp.Poly(sp.expand(quot.as_expr() * num_poly.as_expr()), S, domain=sp.ZZ)
        if cleared.degree() >= 0:
            cleared_degree = max(cleared_degree, cleared.degree())
        matrix[i][j] = cleared
        matrix[j][i] = cleared
    check("CLEARED_DEGREE_AT_MOST_12", cleared_degree <= 12)
    coeff_rows = []
    for i in range(16):
        coeff_rows.append([[int(c) for c in matrix[i][j].all_coeffs()[::-1]] for j in range(16)])
    return coeff_rows, cleared_degree, quad


def cofactor_from_determinant(det_poly, quad):
    factors = [
        sp.Poly(S, S, domain=sp.ZZ),
        sp.Poly(S - 2, S, domain=sp.ZZ),
        sp.Poly(S + 2, S, domain=sp.ZZ),
        sp.Poly(2 * S - 1, S, domain=sp.ZZ),
        sp.Poly(2 * S + 1, S, domain=sp.ZZ),
        quad,
    ]
    remaining = det_poly
    exponents = []
    for factor in factors:
        exponent = 0
        while True:
            quot, rem = sp.div(remaining, factor, domain=sp.ZZ)
            if rem != 0:
                break
            remaining = quot
            exponent += 1
        exponents.append(exponent)
    check("VALUATIONS", exponents == [12, 16, 16, 18, 18, 16])
    content = sp.Integer(sp.content(remaining))
    check("CONTENT", content == C_PUBLISHED)
    primitive = sp.Poly(
        sp.div(remaining, sp.Poly(content, S, domain=sp.ZZ), domain=sp.ZZ)[0].as_expr(),
        S,
        domain=sp.ZZ,
    )
    check("COFACTOR_DEGREE_70", primitive.degree() == 70)
    check("COFACTOR_CONTENT_ONE", sp.content(primitive) == 1)
    check("COFACTOR_CONSTANT_TERM_NONZERO", primitive.TC() != 0)
    check("COFACTOR_SQUARE_FREE", sp.gcd(primitive, sp.diff(primitive, S)).degree() == 0)
    for factor in factors:
        check("COFACTOR_COPRIME_" + str(factor.degree()) + "_" + str(int(factor.TC())), sp.gcd(primitive, factor).degree() == 0)
    prime = 104729
    check("MODULUS_PRIME", sp.isprime(prime))
    check("LEADING_SURVIVES_MODULUS", int(primitive.LC()) % prime != 0)
    factored = sp.factor_list(primitive, modulus=prime)
    degrees = sorted(factor.degree() for factor, mult in factored[1] for _ in range(mult))
    check("NO_RATIONAL_ROOT_MOD_104729", degrees == [7, 10, 11, 42])
    rebuilt = (
        sp.Poly(content, S, domain=sp.ZZ)
        * sp.Poly(S ** 12, S, domain=sp.ZZ)
        * sp.Poly((S - 2) ** 16, S, domain=sp.ZZ)
        * sp.Poly((S + 2) ** 16, S, domain=sp.ZZ)
        * sp.Poly((2 * S - 1) ** 18, S, domain=sp.ZZ)
        * sp.Poly((2 * S + 1) ** 18, S, domain=sp.ZZ)
        * sp.Poly(quad.as_expr() ** 16, S, domain=sp.ZZ)
        * primitive
    )
    check("DETERMINANT_IDENTITY", rebuilt == det_poly)
    check("PERTURBED_IDENTITY_FAILS", rebuilt + 1 != det_poly)
    return [int(coeff) for coeff in primitive.all_coeffs()[::-1]]


def main():
    run_controls()
    spec = importlib.util.spec_from_file_location("support7_order1_owner", OWNER_PATH)
    owner = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(owner)
    matrix, cleared_degree, quad = build_cleared_matrix(owner)
    degree_bound = 16 * cleared_degree
    primes = prime_pool(400)
    nodes = list(range(degree_bound + 1))
    values = [det_at(matrix, node, primes) for node in nodes]
    det_coeffs = newton_monomial(values, nodes)
    for extra in (-1, 6, 8, degree_bound + 2):
        check(f"DET_INTERPOLATION_{extra}", eval_poly(det_coeffs, extra) == det_at(matrix, extra, primes))
    direct = sp.Matrix(16, 16, lambda i, j: eval_poly(matrix[i][j], 1)).det()
    check("DIRECT_DET_AT_1", direct == eval_poly(det_coeffs, 1))
    den_at_1 = int(
        (
            81
            * (1 - 2) ** 2
            * (1 + 2) ** 2
            * (2 - 1) ** 2
            * (2 + 1) ** 2
            * (233 + 16 - 36) ** 2
        )
    )
    check(
        "CHART_POINT_DETERMINANT_MATCHES_9_38",
        sp.Rational(eval_poly(det_coeffs, 1), den_at_1 ** 16) == EXPECTED_DET_S1,
    )
    det_poly = sp.Poly.from_list(list(reversed(det_coeffs)), S, domain=sp.ZZ)
    q_coeffs = cofactor_from_determinant(det_poly, quad)
    above = binom_shift(q_coeffs, 256)
    reflected = [coeff if index % 2 == 0 else -coeff for index, coeff in enumerate(q_coeffs)]
    below = binom_shift(reflected, 8)
    check("NO_ROOT_AT_OR_ABOVE_256", all(coeff > 0 for coeff in above))
    check("NO_ROOT_AT_OR_BELOW_MINUS_8", all(coeff > 0 for coeff in below))
    check("BOUND_ENDPOINTS_NONZERO", eval_at(q_coeffs, 256) != 0 and eval_at(q_coeffs, -8) != 0)
    open_roots, wall_roots = classify_real_roots(q_coeffs, 256)
    # The Cauchy search interval is larger than (-8, 256). The Taylor shifts
    # already exclude roots outside that range, and 256 is inside the Cauchy
    # interval used here, so every surviving root was offered to Descartes.
    check("WALL_REAL_ROOT_COUNT_0", wall_roots == [])
    check("OPEN_CHART_REAL_ROOT_COUNT_18", len(open_roots) == 18)
    seen = []
    for index, (left, right, name) in enumerate(open_roots):
        if left == right:
            raise AssertionError("RATIONAL_OPEN_ROOT")
        variations = sign_variations(transformed(q_coeffs, left, right))
        left_value = eval_at(q_coeffs, left)
        right_value = eval_at(q_coeffs, right)
        check(
            f"ROOT_{index}",
            variations == 1
            and left_value * right_value < 0
            and component(left) == name
            and component(right) == name
            and name is not None,
        )
        seen.append(name)
        print(f"ISOLATING_{index} {left} {right} {name}", flush=True)
    check("COMPONENTS_MATCH_COUNT", len(seen) == 18)
    print("REAL_ROOT_COUNT 18", flush=True)
    print("OPEN_CHART_REAL_ROOT_COUNT 18", flush=True)
    print("WALL_REAL_ROOT_COUNT 0", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
