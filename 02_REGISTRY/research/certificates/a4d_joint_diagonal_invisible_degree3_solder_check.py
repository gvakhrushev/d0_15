#!/usr/bin/env python3
"""Solder response of the degree-3 orthogonal connection Euler.

The link correction does not contain this Euler. In the Gram chart
H(q)=q eta/2 the constant derivative has rank 10 and unique direction
q=-eta. Every constant root has det(I + eta q/2)=0. A solder jet of
degrees 0..3 has linear image rank 15 and does contain the forcing.
The metric Euler of that jet is not computed here.
"""

"""Exact quadratic solder response of the degree-3 orthogonal connection Euler."""
import ast
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import sympy as sp

source_path = Path(__file__).resolve().parent / "a4d_joint_diagonal_invisible_germ_check.py"
lines = source_path.read_text().splitlines()
tree = ast.parse(source_path.read_text())
needed = {"rot", "boost", "wedge_vec", "bivector_of_tangent", "complement_orientation"}
nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in needed]
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source_path), "exec"), globals())
channel = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_degree7_channel")
body = "\n".join(lines[channel.lineno - 1: channel.end_lineno])
body = body.replace(
    "        columns.append(slopes)\n"
    "        if label is not None:\n"
    "            print(\"DEGREE7\", label, direction, [str(item) for item in slopes], flush=True)\n"
    "    return columns",
    "        columns.append(slopes)\n"
    "        face_flux.append(flux)\n"
    "    return columns, face_flux",
)
body = body.replace(
    "    columns = []\n"
    "    directions = range(24) if directions is None else directions",
    "    columns = []\n"
    "    face_flux = []\n"
    "    directions = range(24) if directions is None else directions",
)
body = body.replace(
    "        slopes = [Fraction(0) for _ in range(order)]\n"
    "        for k in range(4):",
    "        slopes = [Fraction(0) for _ in range(order)]\n"
    "        flux = {deg: {face: [Fraction(0) for _ in range(6)] for face in PAIRS} for deg in range(order)}\n"
    "        for k in range(4):",
)
body = body.replace(
    "                    odd_slope = mat_add(hol[deg][1], mat_scale(-1, 1, hinv[deg][1]))\n"
    "                    slopes[deg] += Fraction(64 * sgn, 2) * slope_scalar(odd_slope, row)",
    "                    odd_slope = mat_add(hol[deg][1], mat_scale(-1, 1, hinv[deg][1]))\n"
    "                    slopes[deg] += Fraction(64 * sgn, 2) * slope_scalar(odd_slope, row)\n"
    "                    den, nums = odd_slope\n"
    "                    factor = Fraction(64 * sgn, 2)\n"
    "                    for index, (a, b) in enumerate(PAIRS):\n"
    "                        flux[deg][face][index] += factor * Fraction(nums[a * 4 + b] * eta_sign[b], den)",
)
exec(body, globals())

PAIRS = list(combinations(range(4), 2))
PINDEX = {pair: i for i, pair in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)
GEN = [boost(1), boost(2), boost(3), rot(1, 2), rot(1, 3), rot(2, 3)]
G2 = sp.zeros(6)
for i, (a, b) in enumerate(PAIRS):
    G2[i, i] = ETA[a, a] * ETA[b, b]
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1), (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), 1), (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR[PINDEX[dst], PINDEX[src]] = sign
VACUUM = [sp.eye(4)[:, r] for r in range(4)]
basis_cols = list(VACUUM)
Ms = [
    GEN[3] - GEN[4] + GEN[5],
    GEN[1] - GEN[2] + GEN[5],
    GEN[0] - GEN[2] + GEN[4],
    GEN[0] - GEN[1] + GEN[3],
]
SYM = [(a, b) for a in range(4) for b in range(a, 4)]
qs = sp.symbols("q00 q01 q02 q03 q11 q12 q13 q22 q23 q33")


def frame_matrix(values):
    q = sp.zeros(4)
    for (a, b), value in zip(SYM, values):
        q[a, b] = q[b, a] = value
    return sp.eye(4) + sp.Rational(1, 2) * ETA * q


def rows_of(frame):
    out = {}
    for face in PAIRS:
        uu, vv = [i for i in range(4) if i not in face]
        area = wedge_vec(frame[:, uu], frame[:, vv])
        row = area.T * G2 * STAR
        out[face] = [sp.expand(row[0, j]) for j in range(6)]
    return out


def contract(flux, rows, degree):
    total = []
    for direction in range(24):
        acc = Fraction(0)
        for face in PAIRS:
            acc += sum(rows[face][j] * flux[direction][degree][face][j] for j in range(6))
        total.append(acc)
    return total


def solve_image(columns, rhs):
    rows, width = 24, len(columns)
    table = [[columns[col][row] for col in range(width)] + [rhs[row]] for row in range(rows)]
    rank_row = 0
    pivots = []
    for col in range(width):
        pivot = next((i for i in range(rank_row, rows) if table[i][col] != 0), None)
        if pivot is None:
            continue
        table[rank_row], table[pivot] = table[pivot], table[rank_row]
        scale = table[rank_row][col]
        table[rank_row] = [value / scale for value in table[rank_row]]
        for i in range(rows):
            if i != rank_row and table[i][col] != 0:
                factor = table[i][col]
                table[i] = [table[i][j] - factor * table[rank_row][j] for j in range(width + 1)]
        pivots.append(col)
        rank_row += 1
        if rank_row == rows:
            break
    consistent = all(sp.expand(table[i][width]) == 0 for i in range(rank_row, rows))
    solution = [Fraction(0) for _ in range(width)]
    if consistent:
        for i, col in enumerate(pivots):
            solution[col] = table[i][width]
    return rank_row, consistent, solution


def linear_rows(a0, b0):
    def at(epsilon):
        values = [0] * 10
        values[SYM.index((a0, b0))] = epsilon
        return rows_of(frame_matrix(values))

    r0, r1, r2 = at(0), at(1), at(2)
    out = {}
    for face in PAIRS:
        out[face] = []
        for j in range(6):
            d1 = r1[face][j] - r0[face][j]
            d2 = r2[face][j] - r0[face][j]
            e2 = (d2 - 2 * d1) / 2
            out[face].append(sp.expand(d1 - e2))
    return out


def run_ray(name, dress, probe, sign):
        print("RAY", name, flush=True)
        quarter = sp.Rational(1, 4)
        minus = sp.zeros(24, 1)
        minus[0] = sign * quarter
        minus[6] = sign * quarter
        zero_corr = sp.zeros(24, 1)
        zero_corr[0] = quarter
        zero_corr[6] = quarter
        columns, flux = _degree7_channel(
            dress, minus, zero_corr, sp.zeros(24, 1), sp.zeros(24, 1), probe, None, max_degree=3,
        )
        base = [columns[row][3] for row in range(24)]
        vacuum_rows = rows_of(sp.eye(4))
        check = contract(flux, vacuum_rows, 3)
        print("MATCH_BASE", check == base, flush=True)
        jet_columns = []
        for degree in (3, 2, 1, 0):
            for a0, b0 in SYM:
                jet_columns.append(contract(flux, linear_rows(a0, b0), degree))
        rank, consistent, full_solution = solve_image(jet_columns, [-value for value in base])
        print("SOLDER_JET_IMAGE", rank, consistent, len(jet_columns), flush=True)
        minus_eta = [Fraction(item) for item in (-1, 0, 0, 0, 1, 0, 0, 1, 0, 1)]
        if rank != 15 or not consistent:
            raise SystemExit("solder jet image")

        # A perturbative solder correction around the registered flat frame
        # cannot change its degree-0 term.  The first ten columns above are
        # precisely that constant term (they multiply the degree-3 link
        # forcing).  Test the genuine positive-degree jet separately before
        # interpreting the 40-column image as a regular continuation.
        positive_rank, positive_ok, positive_solution = solve_image(
            jet_columns[10:], [-value for value in base]
        )
        print(
            "POSITIVE_DEGREE_SOLDER_JET",
            positive_rank,
            positive_ok,
            [str(value) for value in positive_solution],
            flush=True,
        )
        # Also expose each filtration stage: q_1 only, q_1+q_2, and
        # q_1+q_2+q_3.  These are the only regular formal correction spaces.
        for upto in (20, 30, 40):
            stage_rank, stage_ok, _stage_solution = solve_image(
                jet_columns[10:upto], [-value for value in base]
            )
            print(
                "POSITIVE_SOLDER_STAGE",
                upto // 10 - 1,
                stage_rank,
                stage_ok,
                flush=True,
            )

        constant_rank, constant_ok, constant_solution = solve_image(
            jet_columns[:10], [-value for value in base]
        )
        print("CONSTANT_SOLDER", constant_rank, constant_ok, [str(value) for value in constant_solution], flush=True)
        got_solution = [Fraction(sp.together(value)) for value in constant_solution]
        if constant_rank != 10 or not constant_ok or got_solution != minus_eta:
            raise SystemExit("constant solder %s" % got_solution)
        for scale in (0, 1, 2):
            values = [scale * item for item in minus_eta]
            got = contract(flux, rows_of(frame_matrix(values)), 3)
            print("LINE", scale, [str(sp.expand(value)) for value in got], flush=True)
        rows_symbolic = rows_of(frame_matrix(list(qs)))
        equations = []
        for direction in range(24):
            acc = 0
            for face in PAIRS:
                acc += sum(rows_symbolic[face][j] * flux[direction][3][face][j] for j in range(6))
            equations.append(sp.together(sp.expand(acc)))
        nonzero = [(i, equations[i]) for i in range(24) if equations[i] != 0]
        factor = sp.factor(nonzero[0][1])
        print("FIRST_NONZERO", nonzero[0][0], factor, flush=True)
        common = all(sp.expand(equations[i] * base[nonzero[0][0]] - equations[nonzero[0][0]] * base[i]) == 0 for i in range(24))
        print("COMMON_FACTOR", common, flush=True)
        import signal

        def stop(_signum, _frame):
            raise TimeoutError("groebner")

        signal.signal(signal.SIGALRM, stop)
        signal.alarm(90)
        try:
            basis = sp.groebner([sp.expand(item) for item in equations], *qs, order="lex")
            print("GROEBNER_COUNT", len(basis), flush=True)
            collapsed = {qs[i]: value for i, value in enumerate([-2, 0, 0, 0, 2, 0, 0, 2, 0, 2])}
            print("COLLAPSED_ON_BASIS", all(sp.expand(item.subs(collapsed)) == 0 for item in basis), flush=True)
            anchor = next(i for i in range(24) if base[i] != 0)
            proportional = all(
                sp.expand(equations[i] * base[anchor] - equations[anchor] * base[i]) == 0
                for i in range(24) if base[i] != 0
            )
            print("NONZERO_COMPONENTS_PROPORTIONAL", proportional, flush=True)
            print("ANCHOR_FACTOR", sp.factor(equations[anchor]), flush=True)
            frame = sp.expand(frame_matrix(list(qs)).det())
            remainder = sp.reduced(frame, list(basis), *qs)[1]
            print("DET_IN_IDEAL", sp.expand(remainder) == 0, flush=True)
            if sp.expand(remainder) != 0:
                raise SystemExit("determinant")
            print("DET_REMAINDER", sp.factor(remainder), flush=True)
        except TimeoutError:
            print("GROEBNER_TIMEOUT", flush=True)
        finally:
            signal.alarm(0)

if __name__ == "__main__":
    run_ray("COS", [1, 0, -1, 0], [0, 1, 0, -1], 1)
    run_ray("SIN", [0, 1, 0, -1], [1, 0, -1, 0], -1)
    print("PASS_DEGREE3_SOLDER", flush=True)
