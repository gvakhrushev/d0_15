"""Literal inherited M2 path settings; no admission or matching dynamics.

The bounded consumer uses AF.frame only at n=2,3.  At n=11 it consumes
counts/segments and PF weights, never the working frame or a large GNS matrix.
Pinned definitions are imported; no owner check/receipt entrypoint is run.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
AF_PATH = "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py"
FOCK_PATH = "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py"
CURRENT_PATH = "02_REGISTRY/research/certificates/a4d_native_correlated_current_transition.py"
ROLE_PATH = "02_REGISTRY/research/certificates/a4d_native_af_role_orbit_metric_check.py"
PRICE_PATH = "02_REGISTRY/research/sources/d0_jacobian_controlled_record_2026-10-16/controlled_record.py"
PREPARATION_PATH = "02_REGISTRY/research/sources/d0_native_preparation_stationary_2026-10-16/preparation.py"
PINS = {
    AF_PATH: "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
    FOCK_PATH: "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
    CURRENT_PATH: "e659733a8ab4fea30f46de56663dc344249420c7e0a3ea65b2aa1a2091b76e0d",
    ROLE_PATH: "b718a3ea3e3f47087b664cc9bb194e0e09c5ae818836efdba3e63b9c11e4f2d5",
    PRICE_PATH: "dd3b7aa6f661dbef4117b2913e62136447a14e2d08a16b08b325cb688874f4ff",
    PREPARATION_PATH: "1e3c00dc0e28503e8c9103daf6ce3583f0500d65b64ee7bc4baf8e1bf4726ffd",
}


def require(condition, name):
    if not bool(condition):
        raise AssertionError(name)


def owners(repo, checks):
    for relative, digest in PINS.items():
        require(hashlib.sha256((repo/relative).read_bytes()).hexdigest() == digest,
                "inherited_settings_pin:"+relative)
        checks.append("inherited_settings_pin:"+relative)
    result = []
    for index, relative in enumerate((AF_PATH, FOCK_PATH, CURRENT_PATH, PRICE_PATH)):
        name = "inherited_path_owned_definition_"+str(index)
        spec = importlib.util.spec_from_file_location(name, repo/relative)
        if spec is None or spec.loader is None:
            raise RuntimeError("owner_definition_unavailable:"+relative)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        result.append(module)
    return tuple(result)


def inherited_paths(AF, n):
    """All actual inherited A1=M2+M1 paths, with literal offsets retained."""
    if not isinstance(n, int) or n < 1:
        raise ValueError("inherited_A1_requires_level_at_least_one")
    return AF.segments(2, 1, n-1)


def matrix_corner(frame, block, offset):
    """HS-isometry C -> K C K*, from one literal two-row path corner."""
    index = {coordinate: i for i, coordinate in enumerate(frame["old_coordinates"])}
    return s.MutableSparseMatrix(frame["old_dimension"], 4, {
        (index[(block, offset+r, offset+c)], 2*r+c): 1
        for r in range(2) for c in range(2)
    })


def car_change(F):
    """The same Pauli/record change as the pinned actual n1 Psi owner."""
    chi = s.Matrix([[1, 0, 0, 1], [0, 1, -s.I, 0],
                    [0, 1, s.I, 0], [1, 0, 0, -1]])/s.sqrt(2)
    T = s.Matrix([[1, 0, 1, 0], [1, 0, -1, 0],
                  [0, 1, 0, 1], [0, 1, 0, -1]])/s.sqrt(2)
    return s.kronecker_product(T, chi)*F.record_basis().T


def scalar_control(r, b):
    return s.Matrix([[r, 0, -b, 0], [0, r, 0, -b],
                     [0, b, 0, r], [b, 0, r, 0]])


def run(repo=None, checks=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = [] if checks is None else checks
    start = len(checks)
    AF, F, C, price = owners(repo, checks)

    def zero(value):
        def entry_zero(x):
            if x == 0:
                return True
            numerator = s.fraction(s.cancel(s.together(x)))[0]
            return AF.red(numerator) == 0
        if isinstance(value, s.MatrixBase):
            return all(entry_zero(x) for x in value)
        return entry_zero(value)

    def check(condition, label):
        require(condition, "inherited_settings:"+label)
        checks.append("inherited_settings:"+label)

    def eq(actual, expected, label):
        check(zero(actual-expected), label)

    p, a = AF.p, AF.a
    change = car_change(F)
    eq(change.H*change, s.eye(16), "actual_Pauli_record_change_unitary")
    P4, B4 = s.diag(1, 1, 0, 0), s.diag(1, 0, 1, 0)
    Pcar = change.H*s.kronecker_product(P4, s.eye(4))*change
    Bcar = change.H*s.kronecker_product(B4, s.eye(4))*change
    samples = []
    for n in (2, 3):
        frame = AF.frame(n)  # Deliberately bounded: NEVER called at n=11.
        paths = inherited_paths(AF, n)
        sizes, d, V = frame["old_sizes"], frame["old_dimension"], frame["V"]
        roots = [[a]*size for size in sizes]
        details = [[p]*size for size in sizes]
        selected = []
        for j, block in enumerate(paths):
            for kind, path, offset in block:
                if kind == 0:
                    r, b = ((s.Rational(4, 5), s.Rational(3, 5)),
                            (s.Rational(3, 5), s.Rational(4, 5)))[len(selected) % 2]
                    for row in range(offset, offset+2):
                        roots[j][row], details[j][row] = r, b
                    selected.append((j, path, offset, r, b))
        check(all(sum((2 if kind == 0 else 1) for kind, _, _ in block) == size
                  for block, size in zip(paths, sizes)), f"all_native_paths_retained_n{n}")
        dr = s.diag(*(roots[j][row] for j, row, col in frame["old_coordinates"]))
        db = s.diag(*(details[j][row] for j, row, col in frame["old_coordinates"]))
        eq(dr*dr+db*db, s.eye(d), f"whole_left_positive_root_identity_n{n}")
        Tfull = price.controlled_matrix(dr, db)
        eq(Tfull.H*Tfull, s.eye(4*d), f"all_four_copies_unitary_n{n}")
        sectors = []
        for i, (j, path, offset, r, b) in enumerate(selected):
            corner = matrix_corner(frame, j, offset)
            Q = s.kronecker_product(s.eye(4), corner)*change
            Psi = V*Q
            eq(Psi.H*Psi, s.eye(16), f"literal_full16_isometry_n{n}_copy{i}")
            for k, previous in enumerate(sectors):
                eq(previous.H*Psi, s.zeros(16),
                   f"distinct_path_full16_orthogonality_n{n}_copies{k}_{i}")
            # Actual W_E action, INCLUDING its whole identity complement.
            pulled = V.H*Psi
            whole_action = V*(Tfull*pulled)+Psi-V*pulled
            expected = change.H*s.kronecker_product(scalar_control(r, b), s.eye(4))*change
            eq(whole_action, Psi*expected, f"literal_W_E_intertwiner_n{n}_copy{i}")
            eq(V*(s.kronecker_product(P4, s.eye(d))*pulled), Psi*Pcar,
               f"actual_price_projector_intertwiner_n{n}_copy{i}")
            eq(V*(s.kronecker_product(B4, s.eye(d))*pulled), Psi*Bcar,
               f"actual_blank_projector_intertwiner_n{n}_copy{i}")
            seed = s.Matrix([1, 0, 0, 1])
            activated = V*s.Matrix.vstack(corner*(r*seed), s.zeros(d, 1),
                                          s.zeros(d, 1), corner*(b*seed))
            m = s.zeros(16, 1)
            m[0], m[1], m[14], m[15] = r, b, r, -b
            eq(activated, Psi*m, f"actual_scalar_preparation_readout_n{n}_copy{i}")
            check(all(m[mask] == 0 for mask in (2, 3, 4, 5, 8, 9)) and b > 0,
                  f"trace_preparation_passes_named_support_pairing_n{n}_copy{i}")
            sectors.append(Psi)
        samples.append({"level": n, "working_dimension": V.rows,
                        "inherited_M2_full16_sectors": len(sectors)})

    # Every scalar trace branch has ZERO spatial CAR current, not sixteen
    # independently prepared matter directions.  This uses the actual owner.
    r, b, c = s.symbols("r b c", real=True)
    trace_m = s.zeros(16, 1)
    trace_m[0] = trace_m[14] = c*r
    trace_m[1], trace_m[15] = c*b, -c*b
    eq((trace_m.T*trace_m)[0], 2*c*c*(r*r+b*b), "full_trace_branch_norm")
    for i, alpha in enumerate(C.car_operators()[3]):
        eq((trace_m.T*alpha*trace_m)[0], 0, f"actual_trace_branch_CAR_current_{i+1}_zero")

    # Large-level front: combinatorics only.  No E11, V11 or H14 is allocated.
    previous = inherited_paths(AF, 10)
    paths = inherited_paths(AF, 11)
    counts = tuple(sum(kind == 0 for kind, _, _ in block) for block in paths)
    old_counts = tuple(sum(kind == 0 for kind, _, _ in block) for block in previous)
    check(old_counts == (55, 34) and counts == (89, 55), "minimal64_same_block_M2_settings_level11")
    check(AF.counts(11) == (233, 144), "both_complete_A11_blocks_retained")
    for j, block in enumerate(paths):
        check(sum(2 if kind == 0 else 1 for kind, _, _ in block) == AF.counts(11)[j],
              f"all_M2_M1_path_dimensions_recover_block{j}")
    selected = tuple((path, offset) for kind, path, offset in paths[0] if kind == 0)[:64]
    check(len(selected) == 64 and len({path for path, _ in selected}) == 64,
          "64_distinct_actual_M2_paths_selected")
    rowsets = [set((offset, offset+1)) for _, offset in selected]
    check(all(rowsets[i].isdisjoint(rowsets[j]) for i in range(64) for j in range(i)),
          "64_rank2_projection_supports_disjoint")
    check(233-128 == 105 and counts[0]-64 == 25,
          "all105_other_first_block_rows_and_second_block_retained")
    mu0, mu1 = p**12, p**13
    eq(233*mu0+144*mu1, 1, "full_PF_state_normalized_at_A11")
    eq(64*(2*mu0)+(233-128)*mu0+144*mu1, 1,
       "setting_weights_plus_entire_background_equal_full_PF_mass")
    eq((2*mu0)*p**2, 2*p**14, "new_canonical_linear_coefficient_prefactor")
    eq((2*p**15)*p**2, 2*p**17, "old_A14_address_linear_coefficient_prefactor")

    # ONE terminal action and ONE global preparation normalizer.  f0/f1
    # below are bound to conditional_old_price, not fitted source functions.
    e = s.Symbol("effect_eigenvalue", positive=True)
    ell = s.Symbol("log_phi", positive=True)
    f0_owned = price.conditional_old_price(AF, 0, e, ell)
    f1_owned = price.conditional_old_price(AF, 1, e, ell)
    check(f0_owned.has(s.log) and f1_owned.has(s.log), "actual_full_conditional_prices_consumed")
    f0, f1 = s.Function("owned_f0"), s.Function("owned_f1")
    e0, e1, e2 = s.symbols("blank_e setting_e1 setting_e2", positive=True)
    q0, q1, q2 = (s.exp(-ell*f0(x)) for x in (e0, e1, e2))
    qB = s.exp(-ell*f1(e0))
    Z0 = 233*mu0*q0+144*mu1*qB
    Z = Z0+2*mu0*(q1+q2-2*q0)
    eq(Z, mu0*((233-4)*q0+2*q1+2*q2)+144*mu1*qB,
       "two_moving_settings_are_one_global_Z_with62_blank_settings")
    canonical = s.Symbol("single_blank_price")+2*mu0*(f0(e1)+f0(e2)-2*f0(e0))
    eq(s.diff(canonical, e1), 2*mu0*s.diff(f0(e1), e1),
       "canonical_one_program_effect_source")
    optimized = 6-s.log(Z)/ell
    envelope1 = 2*mu0*q1*s.diff(f0(e1), e1)/Z
    eq(s.diff(optimized, e1), envelope1, "optimized_source_has_one_global_normalizer")
    eq(s.diff(optimized, e1, e2),
       ell*(2*mu0*q1*s.diff(f0(e1), e1))*(2*mu0*q2*s.diff(f0(e2), e2))/Z**2,
       "global_normalizer_cross_setting_source_not_zero")
    baseline_source = s.diff(optimized, e1).subs({e1: e0, e2: e0})
    eq(baseline_source*p**2,
       2*p**14*q0*s.diff(f0(e0), e0)/Z0,
       "optimized_linear_u_coefficient_with_preparation_response")
    # Replacing formal f by the pinned scalar expression is substitution
    # into these identities.  Its positivity interval is already owned;
    # no old interval/control suite is replayed here.
    return {
        "exact_checks": len(checks)-start,
        "small_literal_frames": samples,
        "setting_level": 11,
        "setting_count": 64,
        "available_same_block_M2_paths": 89,
        "complete_old_block_dimensions": [233, 144],
        "per_setting_PF_weight": "2*p^12",
        "canonical_linear_coefficient": "2*p^14*f0'(p^2)",
        "optimized_linear_coefficient": "2*p^14*exp(-g*f0(p^2))*f0'(p^2)/Z0",
        "large_working_frame_allocated": False,
        "full16_sectors_orthogonal_direct_sum": True,
        "trace_branch_spatial_CAR_current": "0",
        "scope": "literal_inherited_path_intertwiners_and_one_program_sources_only",
    }
