#!/usr/bin/env python3
"""All eight minimum supports: joint unit-linear gate with the owned channels.

One homogeneous absolute solder and four homogeneous Lorentz links are varied
at the frozen (j,gamma,delta)=(2,0,1) link. Translations may be arbitrary on all
64 edges of the L=2 torus. The 24 Lorentz rows here are homogeneous variations,
hence necessary rows of the full sitewise Euler system. This is a linear unit
Newton correction at a NONSTATIONARY seed, not a stationary formal germ.

The first residual jet is a null-vector times the discrete curl of one affine
component. Its four-channel Hessian changes only the N2_2 and N3_3 rows/columns.
Deleting those two link rows still forces both active amplitudes to zero.
Consequently adding arbitrary coefficients of the four selected channels does
not change the solution set of this joint linear gate, on any of the eight
supports (or their twelve-normal-direction union).

No finite support-wide no-go, active-residual vacuum, or L=3 result is claimed.
"""
from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
from itertools import product
from pathlib import Path

import sympy as sp


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "frozen_joint_owner",
    here / "a4d_resolved_curved_stationary_e2_support7_joint_linear_gate_check.py",
)
joint_owner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(joint_owner)
owner = joint_owner.owner
f4_tree = ast.parse((here / "a4d_resolved_curved_stationary_f4_check.py").read_text())
f4_h_n = next(node.value for node in f4_tree.body if isinstance(node, ast.Assign)
              and any(isinstance(target, ast.Name) and target.id == "H_N" for target in node.targets))
check("OBSERVER_FORM_IS_THE_SELECTED_F4_FORM",
      ast.dump(f4_h_n) == ast.dump(ast.parse("sp.diag(1, 1, 1, 1)", mode="eval").body))

specs = [(f"{name}_{r}", r, g) for name, g in owner.COMPLEMENT for r in range(4)]
names = [name for name, _, _ in specs]
active_names = ("N2_2", "N3_3")
active_columns = [names.index(name) for name in active_names]
active_rows = [6 * 2 + 4, 6 * 3 + 5]

link_columns, solder_columns = [], []
adjugate_columns = {}
holonomies, factors = {}, {}
for face in owner.PAIRS:
    r, s = face
    holonomies[face] = owner.role0[r] * owner.role0[s] * owner.role0[r].inv() * owner.role0[s].inv()
    factors[face] = owner.I4 - holonomies[face]
    check(f"BASE_FACE_{r}_{s}_DETERMINANT_AND_ADJUGATE_ZERO",
          factors[face].det() == 0 and factors[face].adjugate() == sp.zeros(4))

for name, role, generator in specs:
    generators = [owner.MJet(a, generator if r == role else sp.zeros(4))
                  for r, a in enumerate(owner.generators0)]
    links = [owner.cayley_jet(a) for a in generators]
    link_columns.append(sp.Matrix([
        owner.d_star_jet(links, generators, r, test)[1]
        for r, test in joint_owner.TESTS
    ]))
    solder_columns.append(sp.Matrix([
        component.d[0] for component in joint_owner.solder_gradient_jet(links, owner.ETA)
    ]))
    adjugate_columns[name] = {}
    for face in owner.PAIRS:
        r, s = face
        p = links[r] * links[s] * links[r].inv() * links[s].inv()
        m = owner.constant_jet(owner.I4) - p
        check(f"{name}_FACE_{r}_{s}_DET_FIRST_JET_ZERO",
              owner.det_direction(m.v, m.d) == 0)
        adjugate_columns[name][face] = owner.adj_direction(m.v, m.d)

# The twelve internal homogeneous rows have zero first adjugate variation too.
# Checking them is needed for the channel Hessian in ALL 24 homogeneous rows.
for role in range(4):
    for name, generator in owner.INTERNAL:
        generators = [owner.MJet(a, generator if r == role else sp.zeros(4))
                      for r, a in enumerate(owner.generators0)]
        links = [owner.cayley_jet(a) for a in generators]
        for face in owner.PAIRS:
            r, s = face
            p = links[r] * links[s] * links[r].inv() * links[s].inv()
            m = owner.constant_jet(owner.I4) - p
            check(f"INTERNAL_{name}_{role}_FACE_{r}_{s}_COFACTOR_FIRST_JET_ZERO",
                  owner.det_direction(m.v, m.d) == 0
                  and owner.adj_direction(m.v, m.d) == sp.zeros(4))

null_vector = sp.Matrix([1, 1, 0, 0])
null_covector = sp.Matrix([[1, -1, 0, 0]])
check("NULL_VECTOR_IS_ETA_DUAL_TO_COVECTOR", null_vector.T * owner.ETA == null_covector)
check("NULL_VECTOR_HAS_OBSERVER_SQUARE_TWO",
      (null_vector.T * null_vector)[0] == 2 and (null_vector.T * owner.ETA * null_vector)[0] == 0)
for role, link in enumerate(owner.role0):
    check(f"ROLE_{role}_FIXES_NULL_COVECTOR", null_covector * link == null_covector)

raw_products = {}
expected_active = {
    "N2_2": [((r, 2), (s, 3)) for r in (0, 1) for s in (0, 1)],
    "N3_3": [((r, 3), (s, 2)) for r in (0, 1) for s in (0, 1)],
}
for name, _, _ in specs:
    for first in owner.PAIRS:
        for second in owner.PAIRS:
            if first == second:
                continue
            actual = factors[second] * adjugate_columns[name][first]
            expected = -8 * null_vector * null_covector if (
                name in expected_active and (first, second) in expected_active[name]
            ) else sp.zeros(4)
            raw_products[name, first, second] = actual
            check(f"RAW_PRODUCT_{name}_{first}_{second}", actual == expected)

# At the base, m*t_rs is the discrete curl of m*b. This identity uses the
# actual affine face translation, with four independently supplied edge values.
b_r, b_shift_s, b_s, b_shift_r = [sp.Matrix(sp.symbols(f"b{index}_0:4")) for index in range(4)]
for face in owner.PAIRS:
    r, s = face
    p = holonomies[face]
    translation = b_r + owner.role0[r] * b_shift_s - p * (b_s + owner.role0[s] * b_shift_r)
    check(f"FACE_{r}_{s}_NULL_COMPONENT_IS_DISCRETE_CURL",
          sp.expand(null_covector * translation - null_covector * (b_r + b_shift_s - b_s - b_shift_r))
          == sp.zeros(1, 1))
    homogeneous_map = sp.zeros(4, 16)
    homogeneous_map[:, 4*r:4*r+4] = owner.I4 - p * owner.role0[s]
    homogeneous_map[:, 4*s:4*s+4] = owner.role0[r] - p
    check(f"FACE_{r}_{s}_HOMOGENEOUS_TRANSLATIONS_HAVE_ZERO_CURL",
          null_covector * homogeneous_map == sp.zeros(1, 16))

sites = list(product(range(2), repeat=4))

def shift(x, role):
    return tuple((value + int(index == role)) % 2 for index, value in enumerate(x))


beta_symbols = sp.symbols("beta0:64")
beta = {(x, role): beta_symbols[4 * index + role]
        for index, x in enumerate(sites) for role in range(4)}


def curl(x, face):
    r, s = face
    return beta[x, r] + beta[shift(x, r), s] - beta[x, s] - beta[shift(x, s), r]


alpha, gamma = sp.symbols("alpha gamma")  # N2_2 and N3_3 amplitudes only
channel2 = {(kind, cls): sp.Integer(0) for kind in ("eta", "n") for cls in ("adj", "opp")}
for x in sites:
    for first in owner.PAIRS:
        for second in owner.PAIRS:
            if first == second:
                continue
            response = sp.zeros(4, 1)
            for name, amplitude in (("N2_2", alpha), ("N3_3", gamma)):
                if (first, second) in expected_active[name]:
                    response += 8 * amplitude * null_vector * curl(x, first)
            cls = "adj" if len(set(first) & set(second)) == 1 else "opp"
            channel2["eta", cls] += (response.T * owner.ETA * response)[0]
            channel2["n", cls] += (response.T * response)[0]
C2 = sum(curl(x, (r, 2))**2 for x in sites for r in (0, 1))
C3 = sum(curl(x, (r, 3))**2 for x in sites for r in (0, 1))
for cls in ("adj", "opp"):
    check(f"ETA_{cls}_CHANNEL_SECOND_COEFFICIENT_ZERO", sp.expand(channel2["eta", cls]) == 0)
    check(f"N_{cls}_CHANNEL_SECOND_COEFFICIENT",
          sp.expand(channel2["n", cls] - 128 * (alpha**2 * C2 + gamma**2 * C3)) == 0)

# Hostile control: a single origin role-0 translation e0 is not homogeneous.
origin = (0, 0, 0, 0)
edge_control = {value: int(key == (origin, 0)) for key, value in beta.items()}
check("SINGLE_EDGE_CONTROL_CURL_SQUARES", C2.subs(edge_control) == 2 and C3.subs(edge_control) == 2)
check("SINGLE_EDGE_CONTROL_N_CHANNEL_SECOND_COEFFICIENT",
      sp.expand(channel2["n", "adj"].subs(edge_control) - 256 * (alpha**2 + gamma**2)) == 0)
# Independent exact finite Cayley calculation of one residual at that site.
epsilon = sp.symbols("epsilon")
links = list(owner.role0)
links[2] = owner.cayley(owner.generators0[2] + epsilon * owner.N2)
p1 = links[0] * links[2] * links[0].inv() * links[2].inv()
p2 = links[0] * links[3] * links[0].inv() * links[3].inv()
e0 = sp.eye(4)[:, 0]
finite_residual = (owner.I4 - p1).det() * e0 - (owner.I4 - p2) * (owner.I4 - p1).adjugate() * e0
check("SINGLE_EDGE_RESIDUAL_BASE_ZERO", finite_residual.subs(epsilon, 0) == sp.zeros(4, 1))
check("SINGLE_EDGE_RESIDUAL_FIRST_JET_NONZERO",
      sp.simplify(sp.diff(finite_residual, epsilon).subs(epsilon, 0)) == 8 * null_vector)

J = sp.Matrix.hstack(*link_columns)
S = sp.Matrix.hstack(*solder_columns)
check("SELECTED_COLUMNS_AGREE_WITH_FROZEN_OWNER",
      J[:, [names.index(name) for name in owner.SELECTED_NAMES]] == joint_owner.j_link
      and S[:, [names.index(name) for name in owner.SELECTED_NAMES]] == joint_owner.j_solder)
for column, (_, role, generator) in enumerate(specs):
    offset = next(i for i, (_, g) in enumerate(owner.ALL_TESTS) if g == generator)
    check(f"MIXED_PARTIAL_{names[column]}",
          S[:, column] == joint_owner.m_solder[6*role+offset, :].T)

star_joint = sp.BlockMatrix([[J, joint_owner.m_solder], [S, joint_owner.hessian]]).as_explicit()
rhs = sp.Matrix.vstack(-joint_owner.E0, sp.zeros(16, 1))
particular = sp.zeros(28, 1)
particular[12:, 0] = -sp.Rational(1, 2) * joint_owner.vec_eta
check("ALL_NORMALS_JOINT_STAR_RANK_23", star_joint.shape == (40, 28) and star_joint.rank() == 23)
check("ALL_NORMALS_SCALE_PARTICULAR", star_joint * particular == rhs)
kept_rows = [row for row in range(40) if row not in active_rows]
reduced_joint = star_joint[kept_rows, :]
reduced_kernel = sp.Matrix.hstack(*reduced_joint.nullspace())
check("REMOVING_ACTIVE_ROWS_HAS_RANK_22", reduced_joint.rank() == 22)
check("REMOVING_ACTIVE_ROWS_STILL_KILLS_ACTIVE_AMPLITUDES",
      reduced_kernel[active_columns, :] == sp.zeros(2, reduced_kernel.cols))
star_kernel = sp.Matrix.hstack(*star_joint.nullspace())
amp_line = sp.zeros(12, 1)
amp_line[0] = amp_line[1] = 1
check("ALL_NORMALS_AMPLITUDE_KERNEL_IS_COMMON_K1_ON_ROLES_0_1",
      star_kernel[:12, :].rank() == 1
      and sp.Matrix.hstack(star_kernel[:12, :], amp_line).rank() == 1)

# lambda2=256*C2*(c_n_adj+c_n_opp), lambda3=256*C3*(c_n_adj+c_n_opp).
# Prove the stronger identity with BOTH lambdas independent: no coefficient
# selector or exceptional coefficient division is needed.
lambda2, lambda3 = sp.symbols("lambda2 lambda3")
channel_shift = sp.zeros(40, 28)
for row, column, value in zip(active_rows, active_columns, (lambda2, lambda3)):
    channel_shift[row, column] = value
check("ARBITRARY_CHANNEL_SHIFT_KILLS_REDUCED_KERNEL", channel_shift * reduced_kernel == sp.zeros(40, reduced_kernel.cols))
check("ARBITRARY_CHANNEL_SHIFT_KILLS_SCALE_PARTICULAR", channel_shift * particular == sp.zeros(40, 1))

expected_ranks = (18, 18, 18, 18, 18, 19, 19, 19)
expected_amp_ranks = (1, 1, 1, 1, 1, 0, 0, 0)
for index, support in enumerate(owner.MINIMUM_SUPPORTS):
    columns = [names.index(name) for name in support] + list(range(12, 28))
    matrix = star_joint[:, columns]
    base_particular = particular[columns, :]
    kernel = sp.Matrix.hstack(*matrix.nullspace())
    reduced = matrix[kept_rows, :]
    smaller_kernel = sp.Matrix.hstack(*reduced.nullspace())
    delta = channel_shift[:, columns]
    local_active = [i for i, name in enumerate(support) if name in active_names]
    missing_rows = [6*r + offset for r in range(4) for offset in (4, 5)]
    missing = J[missing_rows, [names.index(name) for name in support]]
    check(f"SUPPORT_{index}_MINIMUM_MISSING_EULER_GATE",
          missing.rank() == 7 and missing.row_join(-owner.base_missing).rank() == 7)
    check(f"SUPPORT_{index}_STAR_RANK", matrix.rank() == expected_ranks[index])
    check(f"SUPPORT_{index}_SCALE_PARTICULAR", matrix * base_particular == rhs)
    check(f"SUPPORT_{index}_AMPLITUDE_KERNEL_RANK", kernel[:7, :].rank() == expected_amp_ranks[index])
    check(f"SUPPORT_{index}_REMOVED_ROWS_STILL_KILL_ACTIVE_AMPLITUDES",
          smaller_kernel[local_active, :] == sp.zeros(len(local_active), smaller_kernel.cols))
    check(f"SUPPORT_{index}_CHANNEL_SHIFT_VANISHES_ON_REDUCED_KERNEL",
          delta * smaller_kernel == sp.zeros(40, smaller_kernel.cols))
    check(f"SUPPORT_{index}_CHANNEL_SHIFT_VANISHES_ON_PARTICULAR",
          delta * base_particular == sp.zeros(40, 1))
    print("SUPPORT", index, support, "rank", matrix.rank(), "nullity", kernel.cols,
          "amplitude_kernel_rank", kernel[:7, :].rank(), flush=True)

print("FIRST_RESIDUAL_JET", "8*n*active_amplitude*curl(m*b) on the eight declared ordered pairs")
print("FOUR_CHANNEL_HESSIAN", "eta=0; n_adj=n_opp=diag(256*C2,256*C3) on N2_2,N3_3")
print("ALL_EIGHT_UNIT_LINEAR_GATES", "channel-independent solution set; active amplitudes zero")
print("STATUS: E0!=0 blocks a base-anchored stationary germ at order zero; finite free-solder seven-support equations remain open")
