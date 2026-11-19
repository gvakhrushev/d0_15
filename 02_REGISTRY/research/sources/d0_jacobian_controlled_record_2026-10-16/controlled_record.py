#!/usr/bin/env python3
"""Golden-cylinder controlled record in the literal complete AF right module.

The declared calibration C=p^-2 makes E(u)=p^2(I+u E_mixed) equal the
owned golden record at u=0.  This realizes a positive-effect control in
the actual AF algebra; primitive admission and action selection are not
inferred.  All working, apparatus and identity-complement modes remain.
Only pinned owner definitions are imported, never their checks.
"""
from __future__ import annotations

import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
AF_PATH = "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py"
CYL_PATH = "02_REGISTRY/research/sources/d0_golden_cylinder_curvature_2026-10-15/check_golden_curvature.py"
PINS = {
    AF_PATH: "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
    CYL_PATH: "2cf15a9dcffe6c24bd609d88db9825b999ec3201b0ea724ab29f11008372ed3a",
}


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def owners(repo: Path):
    modules = []
    for i, (path, digest) in enumerate(PINS.items()):
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                "source_pin:" + path)
        name = "controlled_record_owned_definition_" + str(i)
        spec = importlib.util.spec_from_file_location(name, repo/path)
        if spec is None or spec.loader is None:
            raise RuntimeError("owner_definition_unavailable:" + path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        modules.append(module)
    return tuple(modules)


def controlled_matrix(r: s.MatrixBase, b: s.MatrixBase) -> s.MatrixBase:
    """Literal golden-compatible four-copy T_E, r=sqrt(1-E), b=sqrt(E).

    Matrices act on OLD LEFT rows.  In a right-module frame this is an
    actual A_(n+6) matrix, not a tensor-factor assumption about that algebra.
    """
    if r.rows != r.cols or b.shape != r.shape:
        raise ValueError("equal_square_old_left_blocks_required")
    z = s.zeros(r.rows)
    return s.BlockMatrix([[r, z, -b, z], [z, r, z, -b],
                          [z, b, z, r], [b, z, r, z]]).as_explicit()


def native_control_blocks(AF, n: int, r_blocks, b_blocks):
    """Actual full A_(n+6) operator, with identity on the whole complement.

    For positive diagonal effects the caller supplies the ordinary positive
    roots r,b.  The right-frame construction retains old-right multiplicity.
    """
    result = []
    for info, r, b in zip(AF.right_frames(n), r_blocks, b_blocks):
        V = info["V"]
        T = controlled_matrix(r, b)
        result.append(V*T*V.H+s.eye(info["dimension"])-V*V.H)
    if len(result) != 2:
        raise ValueError("both_native_AF_blocks_required")
    return tuple(result)


def canonical_seed(AF, n: int) -> s.MatrixBase:
    """Complete normalized-HS coordinates of the canonical PF trace vector."""
    return s.Matrix([AF.root_weight(n+1+j) if r == c else 0
                     for j, size in enumerate(AF.counts(n))
                     for r in range(size) for c in range(size)])


def mixed_cylinder(AF, cylinder_owner):
    """The owned cut(4), including every ready and pending word in order."""
    blocks = cylinder_owner.cut(4)
    require(tuple(map(len, blocks)) == AF.counts(3), "literal_cut4_is_A3")
    require(all(len(w) >= 2 for block in blocks for w in block),
            "two_letters_resolved_without_postselection")
    return tuple(s.diag(*(int(w[0] != w[1]) for w in block)) for block in blocks)


def same_cost_addresses(cylinder_owner, count: int = 64, length: int = 8,
                        returns: int = 4) -> dict:
    """One native effect addressed on disjoint equal-cost actual cylinders.

    Only literal cut words and diagonal indices are materialized.  In
    particular the 64-setting construction does not allocate an A14 matrix
    or its GNS space.  Every unmarked ready/pending leaf stays present.
    """
    if not (0 <= returns <= length and count > 0):
        raise ValueError("positive_count_and_valid_return_count_required")
    positions = list(combinations(range(length), returns))
    if count > len(positions):
        raise ValueError("insufficient_equal_cost_native_addresses")
    prefixes = [tuple(i not in selected for i in range(length))
                for selected in positions[:count]]
    base_cost = length+returns
    cut_cost = base_cost+3
    ready, pending = cylinder_owner.cut(cut_cost)
    ready_index = {word: i for i, word in enumerate(ready)}
    pending_set = set(pending)
    addresses = []
    active = set()
    for prefix in prefixes:
        require(cylinder_owner.cost(prefix) == base_cost, "equal_cost_setting_prefix")
        pair = (prefix+(True, False), prefix+(False, True))
        require(all(cylinder_owner.cost(w) == cut_cost for w in pair),
                "each_active_cylinder_has_common_cut_cost")
        require(all(w in ready_index and w not in pending_set for w in pair),
                "active_cylinders_are_actual_ready_leaves")
        addresses.append(tuple(ready_index[w] for w in pair))
        active.update(pair)
    require(len(active) == 2*count, "all_setting_branches_distinct")
    require(len(ready) > len(active) and len(pending) > 0,
            "inactive_ready_and_all_pending_leaves_retained")
    return {"prefixes": tuple(prefixes), "addresses": tuple(addresses),
            "ready": tuple(ready), "pending": tuple(pending),
            "prefix_cost": base_cost, "cut_cost": cut_cost,
            "AF_level": cut_cost-1, "available_settings": len(positions)}


def addressed_effect_diagonal(p, addressing: dict, parameters):
    """Both complete diagonal blocks of the SINGLE controlled effect."""
    if len(parameters) != len(addressing["addresses"]):
        raise ValueError("one_parameter_per_setting_required")
    ready = [p**2]*len(addressing["ready"])
    pending = [p**2]*len(addressing["pending"])
    for parameter, pair in zip(parameters, addressing["addresses"]):
        for i in pair:
            ready[i] = p**2*(1+parameter)
    return tuple(ready), tuple(pending)


def conditional_probabilities(AF, old_type: int, e):
    """All native fine paths of ONE old history, not a reduced pointer state."""
    if old_type not in (0, 1):
        raise ValueError("native_old_type_0_or_1_required")
    p, a = AF.p, AF.a
    w = (a*p, p)[old_type]
    v2 = (p**4, p**3)[old_type]
    m0, m1 = ((3, 2), (2, 1))[old_type]
    r, b = s.sqrt(1-e), s.sqrt(e)
    fine_A = [(w*r+b/s.sqrt(2))**2, (w*r-b/s.sqrt(2))**2]
    fine_A += [w*w*(1-e)]*(m0-2)
    fine_B = [v2*(1-e)]*m1
    return tuple(fine_A), tuple(fine_B)


def conditional_old_price(AF, old_type: int, e, log_phi=None):
    """Exact per-history coarse D/log(phi) in its positive-spectrum domain."""
    g = s.Symbol("log_phi", positive=True) if log_phi is None else log_phi
    A, B = conditional_probabilities(AF, old_type, e)
    return 3-old_type+sum(B)+sum(q*s.log(q) for q in A+B)/g


def diagonal_coarse_factors(AF, n: int, r_blocks, b_blocks):
    """Exact coarse-left factors for V0*r*Omega + V3*b*Omega.

    The actual first/second native paths get opposite detail amplitudes;
    every other path remains.  This formula is linear, hence also evaluates
    factor jets when given dr,db.  No density matrix is squared densely.
    """
    frame = AF.frame(n)
    out = [s.zeros(size) for size in frame["fine_sizes"]]
    for v, segments in enumerate(frame["segments"]):
        seen = [0, 0]
        for j, _path, offset in segments:
            copy = seen[j]
            seen[j] += 1
            for i in range(AF.counts(n)[j]):
                value = AF.root_weight(n+4+v)*r_blocks[j][i, i]
                if v == 0 and copy < 2:
                    value += (1 if copy == 0 else -1)*AF.root_weight(n+1+j)*b_blocks[j][i, i]/s.sqrt(2)
                out[v][offset+i, offset+i] = value
    return tuple(out)


def working_blocks(AF, n: int, vector: s.MatrixBase):
    fine = AF.counts(n+3)
    if vector.shape != (sum(d*d for d in fine), 1):
        raise ValueError("whole_working_GNS_column_required")
    split = fine[0]**2
    return (s.Matrix(fine[0], fine[0], list(vector[:split])),
            s.Matrix(fine[1], fine[1], list(vector[split:])))


def operator_factors(AF, n: int, vector: s.MatrixBase):
    """Full right-label extraction, including every zero and old-right column."""
    frame = AF.frame(n)
    sizes = frame["fine_sizes"]
    starts = (0, sizes[0]**2)
    result = []
    for j, info in enumerate(AF.right_frames(n)):
        F = s.zeros(info["dimension"], info["spectator_dimension"])
        for row, (v, k, old_row) in enumerate(info["labels"]):
            kind, _path, offset = frame["segments"][v][k]
            require(kind == j, "actual_right_label_type")
            for c in range(info["spectator_dimension"]):
                F[row, c] = vector[starts[v]+old_row*sizes[v]+offset+c]
        result.append(F)
    return tuple(result)


def normalized_diagonal_jet(AF, blocks, jets):
    """Raw feature normalization, with moving tau explicitly retained."""
    values = [M[i, i] for M in blocks for i in range(M.rows)]
    dots = [M[i, i] for M in jets for i in range(M.rows)]
    tau = AF.red(sum(s.conjugate(x)*x for x in values))
    dtau = AF.red(sum(s.conjugate(dx)*x+s.conjugate(x)*dx
                       for x, dx in zip(values, dots)))
    require(tau != 0, "positive_complete_normalizer_required")
    density = [AF.red(s.conjugate(x)*x/tau) for x in values]
    derivative = [AF.red((s.conjugate(dx)*x+s.conjugate(x)*dx)/tau
                         -s.conjugate(x)*x*dtau/tau**2)
                  for x, dx in zip(values, dots)]
    return density, derivative, tau, dtau


def source_intervals() -> dict:
    """Outward log intervals for the actual all34-mode source; no cutoff."""
    from mpmath import iv
    previous = iv.dps
    iv.dps = 45
    try:
        p = (iv.sqrt(5)-1)/2
        a, g, r2 = iv.sqrt(p), -iv.log(p), iv.sqrt(2)
        b0 = [p**4+p**3/r2, p**4-p**3/r2]
        b1 = [p**4+a*p**3/r2, p**4-a*p**3/r2]
        d0 = [-p**5/2+p**3/(2*r2), -p**5/2-p**3/(2*r2)]
        d1 = [-p**5/2+a*p**3/(2*r2), -p**5/2-a*p**3/(2*r2)]
        require(all(x*x > 0 for x in b0+b1+[p**4, a*p**4]),
                "all34_coarse_eigenvalues_strictly_positive")
        dE = (2*sum(2*x*dx*iv.log(x*x) for x, dx in zip(b0+b1, d0+d1))
              -2*p**9*iv.log(p**8)-6*p**10*iv.log(p**9))
        cost, gain = -6*p**10, -dE/g
        old = cost-gain
        require(old > iv.mpf("0.18788044202330") and old < iv.mpf("0.18788044202331"),
                "actual_old_source_positive_interval")
        require(gain > iv.mpf("-0.23666415455801") and gain < iv.mpf("-0.23666415455800"),
                "actual_gain_source_negative_interval")
        conditional_sources = []
        for j in (0, 1):
            w, v2, m0, m1 = ((a*p, p**4, 3, 2), (p, p**3, 2, 1))[j]
            amplitudes = [w*a+p/r2, w*a-p/r2]
            derivatives = [-w/(2*a)+1/(2*p*r2), -w/(2*a)-1/(2*p*r2)]
            derivative_entropy_sum = sum(2*x*dx*iv.log(x*x)
                                         for x, dx in zip(amplitudes, derivatives))
            if m0 > 2:
                derivative_entropy_sum -= (m0-2)*w*w*iv.log(w*w*p)
            derivative_entropy_sum -= m1*v2*iv.log(v2*p)
            conditional_sources.append(-m1*v2+derivative_entropy_sum/g)
        require(conditional_sources[0] > iv.mpf("0.58484") and
                conditional_sources[0] < iv.mpf("0.58485"), "type0_source_strictly_positive")
        require(conditional_sources[1] > iv.mpf("1.7812") and
                conditional_sources[1] < iv.mpf("1.7813"), "type1_source_strictly_positive")
        return {"old_D_over_log_phi": str(old), "gain_entropy_over_log_phi": str(gain),
                "central_cost": str(cost), "conditional_f0_prime": str(conditional_sources[0]),
                "conditional_f1_prime": str(conditional_sources[1]),
                "single_program_64_setting_coefficient": str(2*p**17*conditional_sources[0])}
    finally:
        iv.dps = previous


def run_checks(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    AF, CYL = owners(repo)
    a, p, n = AF.a, AF.p, 3
    checks = []
    def eq(actual, expected, name):
        require(AF.zero(actual-expected), name)
        checks.append(name)
    E = mixed_cylinder(AF, CYL)
    eq(E[0], s.diag(0, 1, 1, 0, 0), "actual_ready_mixed_cylinder")
    eq(E[1], s.diag(0, 1, 1), "actual_pending_mixed_cylinder")
    e = s.Symbol("e", positive=True)
    for j in (0, 1):
        probabilities = conditional_probabilities(AF, j, e)
        eq(sum(probabilities[0]+probabilities[1]), 1,
           "every_fine_path_conditional_normalization_"+str(j))
    addressing = same_cost_addresses(CYL)
    cut_cost = addressing["cut_cost"]
    require(all(CYL.cost(w) == cut_cost for w in addressing["ready"]) and
            all(CYL.cost(w) == cut_cost+1 for w in addressing["pending"]),
            "whole_addressed_cut_has_actual_native_costs")
    eq(len(addressing["ready"])*p**cut_cost+
       len(addressing["pending"])*p**(cut_cost+1), 1, "complete_addressed_cut_PF_mass")
    parameters = s.symbols("u0:64", real=True)
    profile = addressed_effect_diagonal(p, addressing, parameters)
    require(tuple(map(len, profile)) == AF.counts(14), "single_effect_uses_whole_A14_diagonal")
    for parameter, pair in zip(parameters, addressing["addresses"]):
        require(all(profile[0][i] == p**2*(1+parameter) for i in pair),
                "single_effect_keeps_each_success_failure_address")
    require(all(x == p**2 for x in profile[1]), "all_pending_histories_remain_blank")
    require(sum(x == p**2 for x in profile[0]) == len(profile[0])-128,
            "all_inactive_ready_histories_remain_blank")
    seed = canonical_seed(AF, n)
    eq((seed.H*seed)[0], 1, "whole_canonical_seed_norm")
    sizes = AF.counts(n)
    cutseed = s.Matrix([AF.root_weight(n+1+j)*E[j][r, r] if r == c else 0
                       for j, size in enumerate(sizes)
                       for r in range(size) for c in range(size)])
    eq((cutseed.H*cutseed)[0], 2*p**3, "actual_mixed_cylinder_trace")
    frame = AF.frame(n)
    V, d = frame["V"], frame["old_dimension"]
    eq(V.H*V, s.eye(4*d), "whole136_copy_frame_isometric")
    r = tuple(a*s.eye(k) for k in sizes)
    b = tuple(p*s.eye(k) for k in sizes)
    dr, db = tuple(-a*p*M/2 for M in E), tuple(p*M/2 for M in E)
    for j, info in enumerate(AF.right_frames(n)):
        T, dT = controlled_matrix(r[j], b[j]), controlled_matrix(dr[j], db[j])
        eq(T, s.kronecker_product(AF.record(), s.eye(sizes[j])),
           "golden_control_is_literal_record_"+str(j))
        eq(T.H*T, s.eye(T.rows), "both_branches_unitary_"+str(j))
        eq(dT.H*T+T.H*dT, s.zeros(T.rows), "both_branch_jets_unitary_"+str(j))
        R = info["V"]
        eq(R.H*R, s.eye(R.cols), "actual_full_right_frame_"+str(j))
    x = AF.activate(n, seed)
    eq(x, V[:, :d]*(a*seed)+V[:, 3*d:]*(p*seed), "literal_active_controlled_point")
    dx = AF.mat(-a*p*V[:, :d]*cutseed/2+p*V[:, 3*d:]*cutseed/2)
    eq((x.H*x)[0], 1, "whole610_output_normalized")
    eq((dx.H*x+x.H*dx)[0], 0, "whole610_normalizer_jet")
    eq((dx.H*dx)[0], p**4/2, "actual_control_tangent_nonzero")
    M, dM = working_blocks(AF, n, x), working_blocks(AF, n, dx)
    expected = diagonal_coarse_factors(AF, n, r, b)
    expected_d = diagonal_coarse_factors(AF, n, dr, db)
    for j in range(2):
        eq(M[j], expected[j], "literal_coarse_factor_"+str(j))
        eq(dM[j], expected_d[j], "literal_coarse_factor_jet_"+str(j))
    rho, dotrho, tau, dtau = normalized_diagonal_jet(AF, M, dM)
    eq(sum(rho), 1, "all34_coarse_eigenvalues_normalized")
    eq(sum(dotrho), 0, "all34_density_jet_trace_zero")
    eq(sum(dotrho[21:]), -6*p**10, "actual_central_cost_source")
    shifted = tuple(dX+X for X, dX in zip(M, dM))
    _rho2, dotrho2, _tau2, dtau2 = normalized_diagonal_jet(AF, M, shifted)
    eq(dtau2, 2, "moving_raw_normalizer_not_frozen")
    eq(s.Matrix(dotrho2), s.Matrix(dotrho), "raw_radial_jet_cancels_after_normalization")
    frozen_r = AF.mat(p*V[:, 3*d:]*cutseed/2)
    require(AF.red((frozen_r.H*x+x.H*frozen_r)[0]) != 0,
            "hostile_dropped_failure_jet_rejected")
    F, dF = operator_factors(AF, n, x), operator_factors(AF, n, dx)
    for j, info in enumerate(AF.right_frames(n)):
        width, R = sizes[j], info["V"]
        R0, R3 = R[:, :width], R[:, 3*width:]
        mu = p**(n+1+j)
        eq(F[j], AF.root_weight(n+1+j)*(R0*r[j]+R3*b[j]),
           "literal_first_full_operator_factor_"+str(j))
        eq(dF[j], AF.root_weight(n+1+j)*(R0*dr[j]+R3*db[j]),
           "literal_first_full_operator_jet_"+str(j))
        eq(F[j].H*F[j], mu*s.eye(width), "first_full_spectrum_fixed_"+str(j))
        eq(dF[j].H*F[j]+F[j].H*dF[j], s.zeros(width),
           "first_full_spectrum_source_zero_"+str(j))
    # The second ACTUAL activation consumes the full first working vector.
    # Its sparse owned frame is used once; no giant dense GNS operator exists.
    next_x, next_dx = AF.activate(6, x), AF.activate(6, dx)
    next_F, next_dF = operator_factors(AF, 6, next_x), operator_factors(AF, 6, next_dx)
    for j, info in enumerate(AF.right_frames(6)):
        width, R = info["spectator_dimension"], info["V"]
        record = a*R[:, :width]+p*R[:, 3*width:]
        eq(next_F[j], record*M[j], "literal_second_active_factor_"+str(j))
        eq(next_dF[j], record*dM[j], "literal_second_active_factor_jet_"+str(j))
        eq(next_F[j].H*next_F[j], M[j].H*M[j], "second_full_Gram_transfer_"+str(j))
        eq(next_dF[j].H*next_F[j]+next_F[j].H*next_dF[j],
           dM[j].H*M[j]+M[j].H*dM[j], "second_full_source_transfer_"+str(j))
    require(CYL.CHECKS == [], "old_owner_suites_not_executed")
    return {"schema": "d0-jacobian-controlled-record/1", "source_pins_sha256": PINS,
            "exact_checks": len(checks), "calibration_C": "p^-2 (declared, not forced)",
            "effect": "E(u)=p^2*(I+u*E_mixed)", "base_level": n,
            "working_dimension": 610, "apparatus_copy_dimension": 136,
            "identity_complement_dimension": 474, "mixed_cylinder_trace": "2*p^3",
            "normalizer": "1", "normalizer_jet": "0", "tangent_norm_squared": "p^4/2",
            "first_full_operator": {"AF_level": 9, "block_dimensions": [89, 55],
                                    "nonzero_spectrum": "p^4 x5; p^5 x3", "zero_modes": 136,
                                    "old_D_over_log_phi": 6, "old_source": 0,
                                    "gate_gain_entropy_source": 0},
            "coarse_A6_and_second_active_A12_sources": source_intervals(),
            "single_program_normal_setting_aggregation": {
                "settings": 64, "equal_cost_settings_available": addressing["available_settings"],
                "setting_prefix_length": 8, "setting_return_count": 4,
                "prefix_cost": 12, "complete_cut_cost": 15, "AF_seed_level": 14,
                "ready_leaves": len(addressing["ready"]),
                "pending_leaves": len(addressing["pending"]),
                "active_ready_leaves": 128, "active_pending_leaves": 0,
                "each_active_leaf_PF_weight": "p^15",
                "one_effect": "p^2*(I+sum_i u_i E_(s_i FR + s_i RF))",
                "exact_coarse_price_delta": "sum_i 2*p^15*(f0(p^2*(1+u_i))-f0(p^2))",
                "second_complete_operator_price_shift": 6,
                "common_linear_coefficient": "2*p^17*f0'(p^2)>0",
                "refined_active_counts_per_setting": "(2*F_(l+1),2*F_l), l>=0",
                "refined_coefficient": "2*p^17*(p^l*F_(l+1)*f0'+p^(l+1)*F_l*f1')",
                "refined_weight_normalization": "p^l*F_(l+1)+p^(l+1)*F_l=1",
                "large_AF_or_GNS_matrix_allocated": False},
            "second_active": {"working_dimension": next_x.rows, "AF_operator_level": 12,
                              "block_dimensions": list(AF.counts(12)),
                              "relative_entropy_shift": 6, "literal_Gram_and_jet_transfer": True},
            "both_success_failure_and_all_AF_modes_retained": True,
            "native_algebra_implementation": True, "primitive_admission_derived": False,
            "calibrated_readout_equals_full_AF_action": False, "GR_closed": False}


if __name__ == "__main__":
    print(json.dumps(run_checks(), sort_keys=True))
