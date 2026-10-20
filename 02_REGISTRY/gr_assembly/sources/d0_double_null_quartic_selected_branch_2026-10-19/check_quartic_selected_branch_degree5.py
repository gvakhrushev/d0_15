import importlib.util
import re
from pathlib import Path

import sympy as s
from sympy.polys.matrices import DomainMatrix


SOURCE_ROOT = Path(__file__).resolve().parent.parent
BASE = SOURCE_ROOT / "d0_double_null_cubic_uniform_control_2026-10-19" / "check_cubic_uniform_control.py"
CUBIC = SOURCE_ROOT / "d0_double_null_cubic_polynomial_chart_2026-10-19" / "degree3_output.txt"
x, y = s.symbols("x y")
orders = ((2, 1), (1, 2))
mons = tuple((i, degree - i) for degree in range(6) for i in range(degree, -1, -1))


def load(name):
    spec = importlib.util.spec_from_file_location(name, BASE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_cubic(module):
    links = {order: [s.zeros(4) for _ in range(4)] for order in orders}
    coframes = {order: s.zeros(4) for order in orders}
    for line in CUBIC.read_text().splitlines():
        match = re.match(r"\s*([we])_(\d)_(\d)_(\d+)_(\d+)_(\d+)_(\d+)\s*=\s*(.+)$", line)
        if not match:
            continue
        kind, p, t, a, b, ix, iy, value = match.groups()
        order = int(p), int(t)
        a, b, ix, iy = map(int, (a, b, ix, iy))
        coefficient = s.sympify(value)
        if kind == "w":
            links[order][a] += coefficient * x**ix * y**iy * module.G[b]
        else:
            coframes[order][a, b] += coefficient * x**ix * y**iy
    return links, coframes


def at(expr, site):
    return expr.subs({x: site[2], y: site[3]}, simultaneous=True)


# Reuse the published six-plaquette action and its exact Euler-row builders.
base = load("selected_quartic_source")
cubic_links, cubic_frames = read_cubic(base)
old_link, old_frame = base.link, base.coframe
old_high = [dict(corrections) for corrections in base.CORR_HIGH]


def cubic_link(site, axis, back=False):
    previous = base.CORR_HIGH
    base.CORR_HIGH = [dict(corrections) for corrections in old_high]
    for component in range(4):
        for order in orders:
            base.CORR_HIGH[component][order] = at(cubic_links[order][component], site)
    try:
        return old_link(site, axis, back)
    finally:
        base.CORR_HIGH = previous


def cubic_frame(site):
    frame = old_frame(site)
    for order in orders:
        frame += base.Jet.co(*order, at(cubic_frames[order], site))
    return frame


base.link, base.coframe = cubic_link, cubic_frame
source_rows = base.link_rows((0, 0, x, y)) + base.solder_rows((0, 0, x, y))
source = [s.expand(row.coeff(2, 2)) for row in source_rows]
assert len(source) == 40
assert all(s.Poly(row, x, y).total_degree() <= 3 for row in source)
print("source coefficient [a^2*b^2]: 40 rows, max spatial degree 3")

# Linear response of all 40 rows to arbitrary degree-at-most-five quartic fields.
response = load("selected_quartic_response")
link_variables = []
link_polynomials = []
for axis in range(4):
    matrix = s.zeros(4)
    for generator_index, generator in enumerate(response.G):
        for ix, iy in mons:
            coefficient = s.symbols(f"w_{axis}_{generator_index}_{ix}_{iy}")
            link_variables.append(coefficient)
            matrix += coefficient * x**ix * y**iy * generator
    link_polynomials.append(matrix)

frame_variables = []
frame_polynomial = s.zeros(4)
for row in range(4):
    for column in range(4):
        for ix, iy in mons:
            coefficient = s.symbols(f"e_{row}_{column}_{ix}_{iy}")
            frame_variables.append(coefficient)
            frame_polynomial[row, column] += coefficient * x**ix * y**iy
variables = link_variables + frame_variables


def response_link(site, axis, back=False):
    link = response.Jet(response.I) + response.Jet.co(2, 2, at(link_polynomials[axis], site))
    return link.l_inv() if back else link


def response_frame(site):
    return response.Jet(response.I) + response.Jet.co(2, 2, at(frame_polynomial, site))


response.link, response.coframe = response_link, response_frame
response_rows = response.link_rows((0, 0, x, y)) + response.solder_rows((0, 0, x, y))
assert len(response_rows) == 40
equations = []
for source_row, response_row in zip(source, response_rows):
    polynomial = s.Poly(s.expand(source_row + response_row.coeff(2, 2)), x, y)
    assert polynomial.total_degree() <= 5
    equations.extend(polynomial.coeff_monomial(x**ix * y**iy) for ix, iy in mons)

assert len(variables) == len(equations) == 840
matrix, rhs = s.linear_eq_to_matrix(equations, variables)
print("matrix assembled; starting fraction-free exact ranks", flush=True)


def exact_rank(domain_matrix):
    _, integer_matrix = domain_matrix.clear_denoms(convert=True)
    _, _, pivots = integer_matrix.rref_den(method="FF")
    return len(pivots)


coefficient_rank = exact_rank(DomainMatrix.from_Matrix(matrix))
augmented_rank = exact_rank(DomainMatrix.from_Matrix(matrix.row_join(rhs)))
print(
    f"quartic system: {matrix.rows} equations, {matrix.cols} unknowns, "
    f"rank {coefficient_rank}, augmented rank {augmented_rank}"
)
assert coefficient_rank == 580
assert augmented_rank == 581
print(
    "INCONSISTENT for quartic corrections of spatial degree at most five "
    "with the selected cubic representative."
)
