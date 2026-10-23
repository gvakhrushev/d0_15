"""Actual ordered native CAR first-jet API on the complete q3300 chart.

The coefficient fixture F=(a-b)I+b11^T, a=1/4,b=1/125, is rational and is
NOT the certified stationary root. All sixteen occupation states (degrees
zero through four) are retained. No old certificate run, Hessian interval
replay, stationary search, or claim of the full Euler kernel is made here.

first_jet() is the literal stored-backward expression, including its incoming
momentum l on the rightmost ordered contraction/link term. run() independently
checks it against A_v(k)+A_conjugate(v)(l)^dagger on all nineteen chart columns.
The three observer columns vanish only after native whitening; their original
leg, observer and link jets are retained by the complete raw43 reconstruction.
"""
from __future__ import annotations

import ast
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
HELPER = Path(__file__).with_name("native_chart_check.py")
CURVED = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
CURVED_SHA256 = "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da"
L = 8
SQRT2 = s.sqrt(2)
ROOTS8 = (1, (1+s.I)/SQRT2, s.I, (-1+s.I)/SQRT2,
          -1, (-1-s.I)/SQRT2, -s.I, (1-s.I)/SQRT2)


def normalized(matrix):
    return matrix.applyfunc(s.expand)


def is_zero(value):
    entries = value.todok().values() if isinstance(value, s.MatrixBase) else (value,)
    return all(s.expand(s.expand_complex(item)) == 0 for item in entries)


def require(condition, name):
    if not bool(condition):
        raise ArithmeticError("ordered_operator:" + name)


def chart_helper():
    spec = importlib.util.spec_from_file_location("ordered_operator_native_chart", HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def owned_car(repo):
    """Load only the literal owned creator definition and its occupation order."""
    data = (Path(repo)/CURVED).read_bytes()
    require(hashlib.sha256(data).hexdigest() == CURVED_SHA256, "owned_creator_source_pin")
    tree = ast.parse(data)
    nodes = [node for node in tree.body
             if (isinstance(node, ast.FunctionDef) and node.name == "creator")
             or (isinstance(node, ast.Assign)
                 and any(isinstance(target, ast.Name) and target.id == "EXTERIOR_ORDER"
                         for target in node.targets))]
    require(len(nodes) == 2, "exact_creator_and_exterior_order_nodes")
    scope = {"s": s, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CURVED, "exec"), scope)
    return tuple(scope["creator"](i) for i in range(4)), scope["EXTERIOR_ORDER"]


def create(vector, creators):
    return sum((vector[i]*creators[i] for i in range(4) if vector[i] != 0), s.zeros(16))


def contract(vector, creators):
    """Complex-linear contraction: coefficients are NOT conjugated here."""
    return sum((vector[i]*creators[i].T for i in range(4) if vector[i] != 0), s.zeros(16))


def Gamma(matrix, creators):
    """Actual second exterior representation in the owned occupation order."""
    return sum((matrix[i, j]*creators[i]*creators[j].T
                for i in range(4) for j in range(4) if matrix[i, j] != 0), s.zeros(16))


def phases(momentum):
    return tuple(ROOTS8[int(k) % L] for k in momentum)


def cross(vector):
    return s.Matrix([[0, -vector[2], vector[1]],
                     [vector[2], 0, -vector[0]], [-vector[1], vector[0], 0]])


def unpack(column, creators):
    require(column.shape == (31, 1), "complete_31_component_reduced_jet")
    legs = [column[4*r:4*r+4, :] for r in range(4)]
    omega = [Gamma(s.diag(0, cross(column[16+3*r:19+3*r, :])), creators)
             for r in range(4)]
    return legs, omega


def forward_jet(column, legs, k, creators):
    """Forward stored operator derivative on incoming mode k."""
    a, omega = unpack(column, creators)
    tk = phases(k)
    return normalized(L*sum(((tk[r]-1)*create(a[r], creators)
                             + tk[r]*create(legs[r], creators)*omega[r]
                             for r in range(4)), s.zeros(16)))


def first_jet(column, legs, k, l, creators):
    """Full literal stored first jet; column must satisfy own-leg transport.

    k is incoming and l=k+q outgoing. In particular the last backward term
    is -conjugate(t_l)*iota(u)*Omega, with that exact ordering and momentum.
    """
    a, omega = unpack(column, creators)
    tk, tl = phases(k), phases(l)
    return normalized(L*sum(((tk[r]-1)*create(a[r], creators)
                             + tk[r]*create(legs[r], creators)*omega[r]
                             + (s.conjugate(tk[r])-1)*contract(a[r], creators)
                             - s.conjugate(tl[r])*contract(legs[r], creators)*omega[r]
                             for r in range(4)), s.zeros(16)))


def dirac(momentum, legs, creators):
    t = phases(momentum)
    vector = normalized(L*sum(((t[r]-1)*legs[r] for r in range(4)), s.zeros(4, 1)))
    operator = normalized(create(vector, creators) + contract(vector.conjugate(), creators))
    eigenvalue = s.expand((vector.conjugate().T*vector)[0])
    return operator, eigenvalue


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    helper = chart_helper()
    owner = helper.owned_definitions(repo)  # AST definitions only; never helper.run().
    creators, order = owned_car(repo)
    checks = []

    def eq(actual, expected, name):
        require(is_zero(actual-expected), name)
        checks.append(name)

    def yes(condition, name):
        require(condition, name)
        checks.append(name)

    for i in range(4):
        for j in range(4):
            eq(creators[i]*creators[j].T+creators[j].T*creators[i],
               int(i == j)*s.eye(16), f"owned_full16_CAR_{i}_{j}")
    yes(order == (0, 2, 3, 1), "owned_ACDB_exterior_order")
    number = s.diag(*[bin(mask).count("1") for mask in range(16)])
    parameter = s.Symbol("exterior_parameter", real=True)
    spatial_generators = [s.diag(0, cross(s.eye(3)[:, j])) for j in range(3)]
    for j, generator in enumerate(spatial_generators):
        represented = Gamma(generator, creators)
        derivative = owner.exterior(s.eye(4)+parameter*generator).diff(parameter).subs(parameter, 0)
        eq(represented, derivative, f"Gamma_is_owned_exterior_derivative_rotation_{j}")
        eq(represented.H, -represented, f"Gamma_rotation_antiHermitian_{j}")
        eq(represented*number, number*represented, f"Gamma_keeps_all_degrees_{j}")

    a, b = s.Rational(1, 4), s.Rational(1, 125)
    F = (a-b)*s.eye(4)+b*s.ones(4)
    q = (3, 3, 0, 0)
    k = (1, 2, 3, 5)
    l = tuple((k[r]+q[r]) % L for r in range(4))
    differences = tuple(1-t for t in phases(q))
    chart = helper.regular_fourier_chart(F, differences)
    basis, raw_basis, legs = chart["basis31"], chart["basis43"], chart["legs"]
    yes(basis.shape == (31, 19) and raw_basis.shape == (43, 19),
        "complete_q3300_basis_19_not_selected_directions")
    eq(chart["constraints31"]*basis, s.zeros(16, 19), "all_reduced_transport_rows")
    eq(chart["constraints43"]*raw_basis, s.zeros(28, 19), "all_raw43_transport_rows")
    Dk, lambda_k = dirac(k, legs, creators)
    Dl, lambda_l = dirac(l, legs, creators)
    eq(Dk.H, Dk, "full16_Dk_selfadjoint")
    eq(Dl.H, Dl, "full16_Dl_selfadjoint")
    eq(Dk*Dk, lambda_k*s.eye(16), "nonroot_CAR_Delta_k_scalar_all_grades")
    eq(Dl*Dl, lambda_l*s.eye(16), "nonroot_CAR_Delta_l_scalar_all_grades")
    yes(not is_zero(lambda_k-lambda_l), "gauge_spectral_gap_is_nonzero")
    wrong_momentum, wrong_order = [], []
    observer_columns = []
    for j in range(basis.cols):
        column = basis[:, j]
        stored = first_jet(column, legs, k, l, creators)
        independent = forward_jet(column, legs, k, creators) \
            + forward_jet(column.conjugate(), legs, l, creators).H
        eq(stored, independent, f"literal_stored_equals_full_forward_adjoint_column_{j}")
        av, omega = unpack(column, creators)
        tk, tl = phases(k), phases(l)
        incoming_error = normalized(L*sum(((s.conjugate(tl[r])-s.conjugate(tk[r]))
                                          *contract(legs[r], creators)*omega[r]
                                          for r in range(4)), s.zeros(16)))
        ordering_error = normalized(L*sum((tk[r]*(omega[r]*create(legs[r], creators)
                                                 - create(legs[r], creators)*omega[r])
                                          for r in range(4)), s.zeros(16)))
        if not is_zero(incoming_error):
            wrong_momentum.append(j)
        if not is_zero(ordering_error):
            wrong_order.append(j)
        if j >= basis.cols-3:
            eq(stored, s.zeros(16), f"whitened_observer_operator_column_zero_{j}")
            yes(not is_zero(raw_basis[:, j]), f"observer_raw43_column_retained_{j}")
            yes(not is_zero(raw_basis[:16, j]) and not is_zero(raw_basis[19:, j]),
                f"observer_original_legs_and_links_not_frozen_{j}")
            observer_columns.append(j)
    yes(bool(wrong_momentum), "reject_incoming_k_in_place_of_outgoing_l_in_backward_link")
    yes(bool(wrong_order), "reject_swapped_Cu_Omega_order")

    for j, generator in enumerate(spatial_generators):
        gamma = Gamma(generator, creators)
        column = s.zeros(31, 1)
        for r in range(4):
            column[4*r:4*r+4, :] = generator*legs[r]
            column[16+3*r:19+3*r, :] = differences[r]*s.eye(3)[:, j]
        eq(chart["constraints31"]*column, s.zeros(16, 1),
           f"spatial_Lorentz_gauge_is_in_complete_native_tangent_{j}")
        J = first_jet(column, legs, k, l, creators)
        yes(not is_zero(J), f"spatial_Lorentz_gauge_jet_nonzero_{j}")
        eq(J, gamma*Dk-Dl*gamma, f"ordered_gauge_J_intertwiner_{j}")
        eq(Dl*J+J*Dk, (lambda_k-lambda_l)*gamma,
           f"ordered_gauge_X_scalar_spectral_gap_{j}")

    return {"schema": "d0-native-ordered-operator-first-jet/1",
            "exact_checks": len(checks), "checks": checks, "source_pins": helper.PINS,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "nonroot_rational_fixture": {"a": str(a), "b": str(b)},
            "q": list(q), "incoming_k": list(k), "outgoing_l": list(l),
            "lambda_k": str(lambda_k), "lambda_l": str(lambda_l),
            "complete_first_jet_columns": basis.cols, "exterior_dimension": 16,
            "retained_exterior_degrees": [0, 1, 2, 3, 4],
            "rejected_wrong_incoming_momentum_columns": wrong_momentum,
            "rejected_swapped_order_columns": wrong_order,
            "whitened_zero_observer_columns_with_nonzero_raw43_jets": observer_columns,
            "ordered_first_jet_API_available": True,
            "full_joint_Euler_matrix_assembled_or_kernel_solved": False,
            "native_physical_admission_or_GR_claim": False}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
