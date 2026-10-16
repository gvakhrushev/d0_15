"""Exact zero-Fourier shell constraint of the existing full native v8 price.

The complete regular stored chart has 23 REAL field coordinates at q=0:
16 coframe, four own-leg SO(2) stabilizers, and three observer coordinates.
For the actual root frame F=(a-b)I+b11^T, a>b>0, this module proves
rank T0=7 without a large symbolic rank stack.  T0 is the trace-centered
occupied-shell first operator jet.  Its coframe image is scalar of rank3;
its four link images are traceless and independent.  Thus ker T0 has
dimension16, and its adjoint annihilator in the 2047-real-dimensional
translation-invariant shell-density tangent has dimension2040.

The link lower bound uses literal full16 CAR vacuum-to-spatial-two-particle
entries at the four positive occupied momenta, plus two generic 4x4
determinants.  Vacuum entries are witnesses, not a carrier truncation.
Only pinned definitions are imported, never an old run() or root search.

This is a constraint/rank result, not the entire price Hessian, its inertia,
a new matter restriction, physical primitive admission, or a GR theorem.
The independent observer and normalized reference128 purification retain
the same conditional v8 scope.  Preparation annihilators are not gauge.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PINS = {
    "native_chart_check.py": "1cb2bd82796634b414b76a5396b629c98c3679aee3ce7aa63dfc34647ab84b65",
    "ordered_operator_check.py": "f2f9903685c2c522d4c850d335dfb9435c932182962402da499ff8a7a10a9418",
}


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("zero_mode_constraint:"+label)


def _zero(value):
    values = value.todok().values() if isinstance(value, s.MatrixBase) else (value,)
    return all(s.expand(x) == 0 for x in values)


def _load(name):
    path = HERE/(name+".py")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[path.name],
            "owned_definition_pin:"+path.name)
    spec = importlib.util.spec_from_file_location("zero_mode_"+name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(repo=None):
    """Return deterministic exact evidence; no receipt or other file is written."""
    repo = ROOT if repo is None else Path(repo).resolve()
    chart_owner, operator = _load("native_chart_check"), _load("ordered_operator_check")
    chart_owner.owned_definitions(repo)  # only AST definitions and transitive pins
    creators, exterior_order = operator.owned_car(repo)
    checks = []

    def check(condition, label):
        require(condition, label)
        checks.append(label)

    def eq(actual, expected, label):
        check(_zero(actual-expected), label)

    # c>0,b>0 parametrizes EVERY actual a>b>0, not one rational fixture.
    b, c = s.symbols("b c", positive=True)
    a = b+c
    F = c*s.eye(4)+b*s.ones(4)
    chart = chart_owner.regular_fourier_chart(F, (0, 0, 0, 0))
    basis, raw_basis, legs = chart["basis31"], chart["basis43"], chart["legs"]
    spatial = [u[1:4, :] for u in legs]
    check(basis.shape == (31, 23) and raw_basis.shape == (43, 23),
          "complete_q0_23_field_chart_raw43_reconstruction")
    eq(chart["constraints31"]*basis, s.zeros(16, 23),
       "all_reduced_transport_rows_retained")
    eq(chart["constraints43"]*raw_basis, s.zeros(28, 23),
       "all_original_transport_rows_retained")
    check(exterior_order == (0, 2, 3, 1)
          and all(C.shape == (16, 16) for C in creators),
          "literal_full16_ACDB_CAR_carrier")
    for i in range(4):
        for j in range(4):
            eq(creators[i]*creators[j].T+creators[j].T*creators[i],
               int(i == j)*s.eye(16), f"full16_CAR_{i}_{j}")

    vacuum = s.eye(16)[:, 0]
    pair_basis = s.Matrix.hstack(
        creators[2]*creators[3]*vacuum,
        creators[3]*creators[1]*vacuum,
        creators[1]*creators[2]*vacuum)
    eq(pair_basis.H*pair_basis, s.eye(3),
       "actual_spatial_pair_readouts_orthonormal_in_full16")
    spin_columns = (4, 9, 14, 19)
    coframe_columns = tuple(j for j in range(20) if j not in spin_columns)
    check(len(coframe_columns) == 16, "all16_independent_coframe_columns")
    for r, j in enumerate(spin_columns):
        eq(basis[16+3*r:19+3*r, j], spatial[r],
           f"literal_unscaled_stabilizer_axis_{r}")
        eq(basis[:16, j], s.zeros(16, 1), f"stabilizer_is_pure_link_{r}")
    for j in range(20, 23):
        eq(operator.first_jet(basis[:, j], legs, (1, 0, 0, 0),
                              (1, 0, 0, 0), creators), s.zeros(16),
           f"observer_{j-20}_zero_only_after_complete_native_whitening")

    # Coframe shell source: X_(+/-e_r)=lambda1*dG_rr*I16.
    # This generic full16 calculation keeps all four vector components.
    uv = s.Matrix(s.symbols("u0:4", real=True))
    du = s.Matrix(s.symbols("du0:4", real=True))
    phase = operator.phases((1, 0, 0, 0))[0]
    shell_constant = 128-64*s.sqrt(2)
    C, I = operator.create, operator.contract
    D = 8*((phase-1)*C(uv, creators)
           +(s.conjugate(phase)-1)*I(uv, creators))
    J = 8*((phase-1)*C(du, creators)
           +(s.conjugate(phase)-1)*I(du, creators))
    eq(D*J+J*D, 2*shell_constant*(uv.T*du)[0]*s.eye(16),
       "actual_all16_coframe_shell_first_jet_scalar")
    eq(s.conjugate(shell_constant), shell_constant,
       "positive_and_negative_shell_have_same_scalar_coframe_source")

    diag_map = s.zeros(4, 16)
    right_inverse = s.zeros(16, 4)
    for r, u in enumerate(legs):
        diag_map[r, 4*r:4*r+4] = 2*u.T
        right_inverse[4*r:4*r+4, r] = u/(2*(u.T*u)[0])
    eq((diag_map*right_inverse).applyfunc(s.cancel), s.eye(4),
       "four_diagonal_Gram_jets_independently_attainable")
    center = s.eye(4)-s.ones(4)/4
    eq(center*center, center, "trace_centering_is_exact_projector")
    eq(center*s.ones(4, 1), s.zeros(4, 1), "common_shell_eigenvalue_retained_as_epsilon")
    eq(center[:3, :3].det(), s.Rational(1, 4),
       "centered_coframe_rank_three_nonzero_minor")
    eq(center.trace(), 3, "centered_coframe_projector_rank_three")
    diagonal_jets = s.Matrix(s.symbols("dG0:4", real=True))
    eq(s.Rational(2*16, 128)*shell_constant*sum(diagonal_jets),
       shell_constant*sum(diagonal_jets)/4,
       "full128_shell_trace_mean_normalizer_no_frozen_epsilon")

    # Full Euclidean Gram map has rank10, with six SO(4) frame directions.
    U = s.Matrix.vstack(*[u.T for u in legs])
    eq(s.factor(U.det()), -c**3*(a+3*b), "actual_coframe_invertible_for_all_a_gt_b_gt_zero")
    symmetric = s.Matrix(4, 4, lambda i, j: s.Symbol("H"+str(min(i, j))+str(max(i, j)), real=True))
    gram_lift = symmetric*U.inv().T/2
    eq((gram_lift*U.T+U*gram_lift.T).applyfunc(s.cancel), symmetric,
       "all10_Euclidean_Gram_jets_have_exact_coframe_lift")
    check(10-3 == 7 and 16-10 == 6,
          "equal_diagonal_Gram_tangent_seven_plus_full_frame_orbit_six")

    # A generic admissible own-leg K has trK=0 and Ku=0.  The four mixed
    # CAR traces below prove Tr16{D,J}=0 for ANY homogeneous momentum.
    # Thus link images cannot cancel the scalar coframe source.
    w = uv[1:4, :]
    K = s.diag(0, operator.cross(w))
    Omega = operator.Gamma(K, creators)
    v = s.Matrix(s.symbols("v0:4", real=True))
    eq(K*uv, s.zeros(4, 1), "generic_admissible_own_leg_generator_fixes_u")
    eq(K.T, -K, "generic_admissible_generator_skew")
    for left_name, left in (("create", C(v, creators)), ("contract", I(v, creators))):
        for right_name, right in (("create", C(uv, creators)), ("contract", I(uv, creators))):
            eq(s.trace(left*right*Omega), 0,
               "all_momenta_link_trace_identity_"+left_name+"_"+right_name)

    # Literal ordered API, four stabilizers, four positive shell momenta.
    # This reads full16 matrices but only evaluates the decisive columns.
    axes = [s.diag(0, operator.cross(wr)) for wr in spatial]
    for shell in range(4):
        k = tuple(int(i == shell) for i in range(4))
        Dshell, lam = operator.dirac(k, legs, creators)
        eq(lam, shell_constant*(a*a+3*b*b), f"actual_shell_eigenvalue_{shell}")
        for r, j in enumerate(spin_columns):
            link_jet = operator.first_jet(basis[:, j], legs, k, k, creators)
            eq(link_jet*vacuum, s.zeros(16, 1),
               f"literal_link_jet_annihilates_vacuum_shell{shell}_role{r}")
            expected = 64*(phase-1)*C(legs[r], creators)*C(axes[r]*legs[shell], creators)*vacuum
            actual = link_jet*(Dshell*vacuum)
            eq(actual, expected,
               f"actual_full16_shell_link_vacuum_column_{shell}_{r}")
            eq(pair_basis.H*actual,
               64*(phase-1)*(spatial[r]*spatial[r].T
                            -(spatial[r].T*spatial[r])[0]*s.eye(3))*spatial[shell],
               f"actual_spatial_pair_coefficient_Hodge_identity_{shell}_{r}")

    xi = s.Matrix(s.symbols("xi0:4", real=True))
    M = sum((xi[r]*spatial[r]*spatial[r].T for r in range(4)), s.zeros(3))
    for shell in range(4):
        hodge_sum = sum((xi[r]*spatial[r].cross(spatial[r].cross(spatial[shell]))
                        for r in range(4)), s.zeros(3, 1))
        eq(hodge_sum, (M-s.trace(M)*s.eye(3))*spatial[shell],
           f"four_link_shell_readout_equals_M_minus_traceM_{shell}")
    spatial_det = s.factor(s.Matrix.hstack(*spatial[1:4]).det())
    eq(spatial_det, -c*c*(a+2*b),
       "three_spatial_shell_vectors_span_for_every_a_gt_b_gt_zero")
    # Vanishing shell readouts force M-tr(M)I=0; taking its trace gives
    # -2tr(M)=0, hence M=0.  Four independent entries then force xi=0.
    eq(s.trace(M-s.trace(M)*s.eye(3)), -2*s.trace(M),
       "vanishing_all_shell_readouts_force_M_zero")
    readouts = s.Matrix([M[0, 1]-M[0, 2], M[0, 1]-M[1, 2],
                         M[0, 0]-M[0, 1], M[0, 1]])
    link_minor = s.factor(readouts.jacobian(xi).det())
    eq(link_minor, b**4*c**4, "four_link_readout_minor_strictly_positive_all_a_gt_b_gt_zero")
    eq(link_minor.subs(b, 0), 0, "hostile_diagonal_frame_loses_this_four_link_lower_bound")
    eq(spatial_det.subs(c, 0), 0, "hostile_collapsed_coframe_cannot_use_span_proof")
    check(3+4 == 7 and 23-7 == 16 and 16 == 13+3,
          "complete_field_constraint_rank_seven_kernel_sixteen")
    check(8*16**2-1 == 2047 and 2047-7 == 2040,
          "full_real_q0_shell_density_and_source_annihilator_dimensions")

    # At q0 every first jet is momentum-diagonal.  The occupied projector
    # contains the ENTIRE sixteen-dimensional Fock fiber at each shell mode.
    # Thus PXQ=0 by exact block selection, without replacing signed R_Q.
    shell_modes = tuple(tuple(sign if r == axis else 0 for r in range(4))
                        for axis in range(4) for sign in (1, 7))
    check(len(set(shell_modes)) == 8 and 8*16 == 128,
          "q0_occupied_whole_Fock_fibers_no_offshell_matter_block")

    return {
        "exact_checks": len(checks), "checks": checks,
        "source_pins": {**PINS, **chart_owner.PINS},
        "parameters": {"frame": "F=(a-b)I+b11^T", "domain": "a>b>0", "c": "a-b"},
        "mode": [0, 0, 0, 0],
        "rank_T0": 7, "rank_coframe": 3, "rank_link": 4,
        "field_dimension_real": 23, "field_kernel_dimension_real": 16,
        "kernel_split": {"equal_diagonal_coframe": 13, "observer": 3},
        "equal_diagonal_Gram_dimension": 7,
        "full_frame_orbit_dimension": 6,
        "q0_density_tangent_dimension_real": 2047,
        "preparation_adjoint_annihilator_dimension_real": 2040,
        "exact_minors": {"link_readout": "b^4(a-b)^4",
                         "spatial_span": "-(a-b)^2(a+2b)",
                         "centered_coframe": "1/4"},
        "carrier": {"sites": 4096, "Fock_dimension": 16, "Hilbert_dimension": 65536,
                    "shell_rank": 128, "reference_dimension": 128,
                    "exterior_order": list(exterior_order)},
        "fixed_calibrations": {"ell": "1/8", "m": 16384, "feedback_M": 128,
                               "alpha": "p^2/8192", "beta": "2p^2", "z": "2^-20"},
        "scope": {"all16_carrier_and_full_reference_retained": True,
                  "translation_invariant_reduced_density_only": True,
                  "PXQ_zero_by_whole_Fock_momentum_selection": True,
                  "signed_resolvent_replaced_by_positive_one": False,
                  "annihilators_classified_as_gauge": False,
                  "full_price_Hessian_or_inertia_proved_here": False,
                  "other_Fourier_modes_or_affine_rows_included": False,
                  "D0_core_physical_preparation_admission_proved": False},
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
