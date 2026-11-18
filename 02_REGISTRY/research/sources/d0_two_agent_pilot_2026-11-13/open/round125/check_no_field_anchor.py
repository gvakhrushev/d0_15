"""Exact native stop flag and four-state tests for the absolute source."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round121"))
from check_book03_identity_pair import NATIVE, ne


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def verify_native_flag():
    # Port 0, flag 1, copy 2, protected Spin 3,4. Both births use v.
    def cx(i, j):
        return ne.Gate("CX", (i, j))

    swap = (cx(0, 2), cx(2, 0), cx(0, 2))
    source = ne.Gate("SourceI", (0, 3, 4))
    z = swap + (source, source) + swap
    gates = z + (ne.Gate("G", (2,)),) + z + (cx(1, 2),)
    execution = ne.Execution(5, (), (), gates, ne.G_CX_SOURCE_I, 0, (3, 4))
    applied = ne.word_matrix(execution, max_qubits=5, max_expanded_stages=18)
    p, a = ne.P, ne.A
    born = sp.Matrix([a, p])
    initial = sp.kronecker_product(sp.eye(2), born, born, sp.eye(4))
    expected = sp.kronecker_product(sp.eye(2), sp.Matrix([a, 0, 0, p]), sp.eye(4))
    require(ne.exact_matrix_equal(applied*initial, expected), "Incorrect paid flag copy")
    return {"paid_unitary_stages": len(gates), "canonical_births": 2,
            "retained_pointer_probabilities": ["p", "p^2"],
            "initialized_columns": initial.cols}


def verify_joint_late_stop():
    b0, b1, ret = sp.symbols("b0 b1 ret", positive=True)
    theta = b1/(b0+b1)
    odds = theta/(1-theta)
    require(sp.cancel(odds-b1/b0) == 0, "Wrong absolute continuation mass")
    joint_return = ret*b1/(b0+b1)
    stop = b0/(b0+b1)
    require(sp.cancel(joint_return/stop-ret*b1/b0) == 0, "Wrong relative cold mass")
    return {"absolute_active_over_stop": "theta/(1-theta)",
            "absolute_coherent_return_over_stop": "joint_return/joint_stop",
            "same_reference_mass_needed": True}


def verify_four_state_graph():
    # 0=B0, 1=E0, 2=B1, 3=E1, with the actual bipartite transition topology.
    square = ((0, 1), (1, 2), (2, 3), (3, 0))
    arcs = square + tuple((v, u) for u, v in square)
    edges = [("skip", i, i) for i in range(4)]
    edges += [("refuse", i, i) for i in range(4)]
    edges += [("success", i, j) for i, j in arcs]
    basis = {edge: sp.eye(len(edges))[:, i].T for i, edge in enumerate(edges)}
    skip = [basis["skip", i, i] for i in range(4)]
    refuse = [basis["refuse", i, i] for i in range(4)]
    succ = {(i, j): basis["success", i, j] for i, j in arcs}
    tests = [skip[i]-refuse[i] for i in range(4)]
    for i, j in square:
        tests.append(succ[i, j]+succ[j, i]-2*skip[i])
        tests.append(skip[i]-skip[j])
    tests.append(2*sum((succ[ij] for ij in square), sp.zeros(1, len(edges)))-8*skip[0])
    overlap_sign = {(0, 1): 1, (1, 2): 1, (2, 3): -1, (3, 0): 1}
    sign = sp.prod(overlap_sign.values())
    require(sign == -1 and sign**2 == 1, "Only the doubled square restores the sign")
    constraints = sp.Matrix.vstack(*tests)
    gauge = sp.Matrix([[1, *(int(j == y)-int(i == y) for y in (1, 2, 3))]
                       for _, i, j in edges])
    require(constraints.rank() == 12 and gauge.rank() == 4, "Wrong graph rigidity rank")
    require(constraints*gauge == sp.zeros(constraints.rows, gauge.cols), "Gauge must survive")

    actual = sp.Matrix(sp.symbols("c0:16", real=True))
    fix = sp.Matrix.vstack(skip[0], *(succ[ij] for ij in square[:3]))
    solve_matrix = constraints.col_join(fix)
    recovered, _ = solve_matrix.gauss_jordan_solve(
        (constraints*actual).col_join(sp.zeros(fix.rows, 1)))
    require(all(sp.expand(v) == 0 for v in constraints*(actual-recovered)),
            "Generic measured loop contrasts did not reconstruct the tariff class")
    correction, _ = gauge.gauss_jordan_solve((actual-recovered).applyfunc(sp.expand))
    require(all(sp.expand(v) == 0 for v in actual-recovered-gauge*correction),
            "Reconstruction should leave only common scale and endpoint potential")

    sigma, kappa, Q = sp.symbols("sigma kappa Q", positive=True)
    P = (1-(1-sigma)*kappa)*sp.eye(4)
    for i, j in arcs:
        mark_i, mark_j = i//2, j//2
        P[i, j] = (1-sigma)*kappa*(Q if mark_i == mark_j else 1-Q)
    require(all(sp.expand(x) == 0 for x in P*sp.ones(4, 1)-sp.ones(4, 1)),
            "Native attempts must be complete")
    return {"states": 4, "distinct_charges": len(edges), "cycle_tests": constraints.rows,
            "short_test_lengths_with_common_central_sign": [1, 2, 3, 8],
            "constraint_rank": constraints.rank(), "remaining_constant_and_potential_dimension": 4,
            "full_native_kernel_is_stochastic": True,
            "nonzero_loop_data_reconstruct_the_tariff_modulo_gauge": True}


def verify_spectral_anchor():
    # A fixed CP map can expose different rates on different unfaithful supports.
    L = sp.diag(1, 2)
    n0, n1 = sp.diag(1, 0), sp.diag(0, 1)
    require(L.T*n0*L == n0, "First closed support")
    require(L.T*n1*L == 4*n1, "Second closed support")
    return {"fixed_cp_map_can_have_distinct_rates_on_singular_sectors": [1, 4],
            "faithful_relative_bound_needed_for_common_spectral_anchor": True}


def main():
    print(json.dumps({
        "native_sha256": sha256(NATIVE.read_bytes()).hexdigest(),
        "native_stop_flag": verify_native_flag(),
        "joint_terminal": verify_joint_late_stop(),
        "four_state_path_rigidity": verify_four_state_graph(),
        "spectral_anchor_control": verify_spectral_anchor(),
        "physical_held_out_terminal_bound": False,
        "physical_C_closed": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
