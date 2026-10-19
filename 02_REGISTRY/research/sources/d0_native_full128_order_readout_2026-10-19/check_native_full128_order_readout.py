#!/usr/bin/env python3
"""Exact first-order commutator response of one original full128 pointer event."""
from functools import lru_cache
from pathlib import Path
import ast
import hashlib
import json

import sympy as s

ROOT = Path(__file__).resolve().parents[4]
CREATORS = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
PINS = {
    "02_REGISTRY/research/A4D_RETAINED_HISTORY_CAUSAL_SOURCE.md":
        "d7f8498e30e788af43edeb2bfd6e763d429e221cea76b622198687bbf4af21db",
    "02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md":
        "2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79",
    "02_REGISTRY/research/A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md":
        "577cbc909f766468fbef8ab38a5986ae761d348b075c2f38b2e1a88b704d4b3e",
    "02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md":
        "a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915",
    "02_REGISTRY/research/sources/d0_opposite_null_julia_order_memory_2026-10-19/check_lorentz_order_memory.py":
        "48a9692675fbe46c68c4d902d3069ac2c717e2370761508983db2e3245497cb8",
    "02_REGISTRY/research/sources/d0_complete_record_channel_2026-10-17/check_record_channel.py":
        "dee7ada5cf04bf961701206f65b216e1ab9c6f45ef9f9ed3258e70bed9cb13a2",
}


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(ok, name):
        if not bool(ok):
            raise ArithmeticError("full128_order_readout:" + name)
        checks.append(name)

    def eq(left, right, name):
        diff = left - right
        values = list(diff) if isinstance(diff, s.MatrixBase) else [diff]
        require(all(s.simplify(v) == 0 for v in values), name)

    for relpath, digest in PINS.items():
        actual = hashlib.sha256((repo / relpath).read_bytes()).hexdigest()
        require(actual == digest, "pin_" + Path(relpath).name)

    tree = ast.parse((repo / CREATORS).read_text())
    nodes = [
        node for node in tree.body
        if (isinstance(node, ast.FunctionDef) and node.name == "creator")
        or (isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name)
                    and target.id == "EXTERIOR_ORDER" for target in node.targets))
    ]
    require(len(nodes) == 2, "only_owned_CAR_creator_and_order_loaded")
    scope = {"s": s, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CREATORS, "exec"), scope)
    C = [scope["creator"](r) for r in range(4)]
    I16 = s.eye(16)

    def unit(i, j):
        M = s.zeros(4)
        M[i, j] = 1
        return M

    N2 = unit(1, 2) + unit(2, 0)
    Nbar3 = unit(0, 3) + unit(3, 1)
    J23 = unit(2, 3) - unit(3, 2)
    eta = s.Matrix([
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ])
    eq(N2 * Nbar3 - Nbar3 * N2, J23, "opposite_null_commutator_is_J23")
    for name, generator in (("N2", N2), ("Nbar3", Nbar3), ("J23", J23)):
        eq(generator.T * eta + eta * generator, s.zeros(4),
           "proper_lorentz_tangent_" + name)

    for r in range(4):
        eq(C[r] * C[r].H + C[r].H * C[r], I16,
           "CAR_single_mode_" + str(r))
        require(C[r] != s.zeros(16), "nonzero_CAR_mode_" + str(r))
    GJ = sum(
        (J23[i, j] * C[i] * C[j].H
         for i in range(4) for j in range(4)),
        s.zeros(16),
    )
    for k in range(4):
        expected = sum((J23[i, k] * C[i] for i in range(4)), s.zeros(16))
        eq(GJ * C[k] - C[k] * GJ, expected,
           "full16_exterior_lift_generator_" + str(k))

    # L=4 first-shell Fourier phases: k=(0,0,0,1), so shift_3=i.
    h = s.Rational(1, 4)
    nu = s.Rational(3, 5)
    z = [s.Integer(1), s.Integer(1), s.Integer(1), s.I]
    d_h = s.zeros(16)
    for r in range(4):
        P_r = nu * C[r] * z[r]  # M_r=I at the base configuration
        d_h += (P_r - nu * C[r]) / h
    D_h = d_h + d_h.H
    A = h * D_h / 16
    require(D_h == D_h.H, "actual_true_adjoint_Dh_is_selfadjoint")
    require(A == A.H, "blank_SELECT_block_A_is_selfadjoint")
    require(nu < 1, "strict_contraction_weight")
    for r in range(4):
        projector = C[r] * C[r].H
        right_projector = C[r].H * C[r]
        eq(projector * projector, projector, "CAR_projection_" + str(r))
        eq(right_projector * right_projector, right_projector,
           "CAR_right_projection_" + str(r))

    # Vary only the proper Lorentz link M_2 by exp(t J23).
    dP = nu * C[2] * GJ * z[2]
    d_dh = dP / h
    dD_h = d_dh + d_dh.H
    dA = h * dD_h / 16

    p = (s.sqrt(5) - 1) / 2
    require(s.simplify(p + p**2 - 1) == 0, "golden_weight_normalization")
    # The original full128 port-0, blank-label Kraus block is
    # p I + p^2 (I - 2 A* A) = I - 2 p^2 A^2.
    K00 = I16 - 2 * p**2 * A**2
    dK00 = -2 * p**2 * (dA * A + A * dA)
    q0_source = s.simplify(s.trace(K00 * dK00) / 8)
    expected_source = (
        s.Rational(42633, 5120000)
        - s.Rational(14157, 5120000) * s.sqrt(5)
    )
    eq(q0_source, expected_source, "exact_full128_pointer_J23_source")
    require(q0_source.is_positive is True, "strictly_positive_order_source")

    # At zero Fourier momentum A=0, hence this same pointer has zero first jet.
    d0 = s.zeros(16)
    for r in range(4):
        d0 += (nu * C[r] - nu * C[r]
               + (nu * C[r] - nu * C[r]).H) / h
    A0 = h * d0 / 16
    dP0 = nu * C[2] * GJ
    dD0 = (dP0 + dP0.H) / h
    dA0 = h * dD0 / 16
    K000 = I16 - 2 * p**2 * A0**2
    dK000 = -2 * p**2 * (dA0 * A0 + A0 * dA0)
    q0_zero_mode_source = s.simplify(s.trace(K000 * dK000) / 8)
    eq(q0_zero_mode_source, 0, "zero_mode_order_source_control")
    eq(A0, s.zeros(16), "zero_mode_blank_SELECT_block_is_zero")

    # A well-typed algebraic diagnostic for naive same-flag Julia composition.
    # The relative unitary V(M)=J(P0)^* J(P(M)) is normalized to V(I)=I.
    # This tests that specific candidate map; it does not assume D0 executes V.
    r_link = 2
    Qleft = C[r_link] * C[r_link].H
    Qright = C[r_link].H * C[r_link]
    Pstar = nu * C[r_link]  # shift_2=1 on the mode used above
    Lstar = I16 - s.Rational(1, 5) * Qleft
    Rstar = I16 - s.Rational(1, 5) * Qright
    Jstar = Pstar.row_join(Lstar).col_join(Rstar.row_join(-Pstar.H))
    eq(Jstar.H * Jstar, s.eye(32), "base_Julia_word_is_unitary")

    def sylvester_at_base(projector, rhs):
        pieces = (
            (I16 - projector, s.Integer(1)),
            (projector, s.Rational(4, 5)),
        )
        return sum(
            (left * rhs * right / (lam_left + lam_right)
             for left, lam_left in pieces
             for right, lam_right in pieces),
            s.zeros(16),
        )

    def relative_julia_tangent(generator):
        G = sum(
            (generator[i, j] * C[i] * C[j].H
             for i in range(4) for j in range(4)),
            s.zeros(16),
        )
        dP_link = nu * C[r_link] * G
        rhs_left = -dP_link * Pstar.H - Pstar * dP_link.H
        rhs_right = -dP_link.H * Pstar - Pstar.H * dP_link
        dL_link = sylvester_at_base(Qleft, rhs_left)
        dR_link = sylvester_at_base(Qright, rhs_right)
        eq(Lstar * dL_link + dL_link * Lstar, rhs_left,
           "left_Julia_defect_root_Sylvester")
        eq(Rstar * dR_link + dR_link * Rstar, rhs_right,
           "right_Julia_defect_root_Sylvester")
        dJ_link = dP_link.row_join(dL_link).col_join(
            dR_link.row_join(-dP_link.H)
        )
        tangent = Jstar.H * dJ_link
        eq(tangent.H + tangent, s.zeros(32),
           "relative_Julia_tangent_is_skew")
        return tangent

    XN = relative_julia_tangent(N2)
    Xbar = relative_julia_tangent(Nbar3)
    XJ = relative_julia_tangent(J23)
    julia_lie_defect = s.simplify(XN * Xbar - Xbar * XN - XJ)
    eq(julia_lie_defect.H + julia_lie_defect, s.zeros(32),
       "relative_Julia_Lie_defect_is_skew")
    julia_lie_defect_norm2 = s.simplify(
        s.trace(julia_lie_defect.H * julia_lie_defect)
    )
    eq(julia_lie_defect_norm2, s.Rational(1789, 500),
       "exact_same_flag_Julia_composition_defect_norm")
    require(julia_lie_defect_norm2 > 0,
            "relative_Julia_map_is_not_a_Lorentz_representation")
    julia_lie_defect_rank = julia_lie_defect.rank()
    require(julia_lie_defect_rank == 10,
            "same_flag_Julia_defect_rank_10")
    julia_anti_defect = s.simplify(XN * Xbar - Xbar * XN + XJ)
    julia_anti_defect_norm2 = s.simplify(
        s.trace(julia_anti_defect.H * julia_anti_defect)
    )
    eq(julia_anti_defect_norm2, s.Rational(1789, 500),
       "exact_reversed_order_Julia_defect_norm")
    require(julia_anti_defect_norm2 > 0,
            "reversed_order_does_not_restore_representation")

    return {
        "status": "PASS",
        "exact_checks": len(checks),
        "checks": checks,
        "carrier": {
            "CAR": "all16 exterior components",
            "record": "original128 outcomes; selected scalar is port0/blank label",
            "reference": "reference128 retained as an untouched tensor factor",
            "preparation": "fixed system marginal I16/16",
        },
        "fixture": {
            "lattice": "L=4",
            "h": str(h),
            "Fourier_mode": "(0,0,0,1), phase i on role3",
            "moving_link": "role2: exp(a N2) exp(b Nbar3) versus reverse",
            "other_links": "identity",
            "coframe_weight": str(nu),
            "source": "full128 port0/blank-label probability",
        },
        "mixed_order_jet": str(q0_source),
        "mixed_order_jet_decimal": str(s.N(q0_source, 16)),
        "zero_mode_control": str(q0_zero_mode_source),
        "same_flag_Julia_lie_defect_norm_squared": str(julia_lie_defect_norm2),
        "same_flag_Julia_lie_defect_rank": julia_lie_defect_rank,
        "reversed_order_Julia_defect_norm_squared": str(
            julia_anti_defect_norm2
        ),
        "scope": {
            "endpoint_link_order_readout": True,
            "relative_same_flag_Julia_map_is_a_representation": False,
            "physical_admission_of_this_probe": False,
            "sequential_memory_word_execution": False,
            "Julia_dilation_composition_compatibility": False,
            "native_Cost_Info_selection": False,
            "positive_GR_closure": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
