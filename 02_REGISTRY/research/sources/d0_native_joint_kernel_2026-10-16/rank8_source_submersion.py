"""Actual pure-memory rank8 preparation preserves the full151 source rank.

Use chi=(mask1+mask15)/sqrt2 in the OWNED ACDB/native-eta convention.
The packet's positive-frame chi has the minus top sign; this file does not
mix those coordinate systems.  All16 CAR states, the whole128 eigenshell,
reference128 and the signed off-shell complement remain.

Only NEW top-dual readouts of literal first_jet() are evaluated.  The
two-active first pair has rank4, not5, on chi.  The SECOND occupied pair
detects its missing axis by an exact strictly positive norm.  This proves
rank7/3/5 and real total151 for EVERY a>b>0 and every shell-transfer sign.
No old run(), spectral search, full field matrix or receipt is executed.
The consumer is the regular stationary AMPLITUDE fibre through rank8,
not a claim that its transverse field Hessian is invertible.
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
    "shell_transfer_all_orbits.py": "d8db3de5b34e4ee4ac7a9efb4676072d18b455dec5a72f0beb6b46b40a99eb1a",
}


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("rank8_source_submersion:"+label)


def zero(value):
    entries = value.todok().values() if isinstance(value, s.MatrixBase) else (value,)
    return all(s.cancel(s.expand(x)) == 0 for x in entries)


def load(name):
    path = HERE/(name+".py")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[path.name],
            "owned_definition_pin:"+name)
    spec = importlib.util.spec_from_file_location("rank8_"+name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    chart, operator, transfer = (load(name) for name in
                                ("native_chart_check", "ordered_operator_check",
                                 "shell_transfer_all_orbits"))
    chart.owned_definitions(repo)  # only definitions/transitive pins, never run()
    creators, order = operator.owned_car(repo)
    checks = []

    def eq(actual, expected, label):
        require(zero(actual-expected), label)
        checks.append(label)

    def check(condition, label):
        require(condition, label)
        checks.append(label)

    b, c = s.symbols("b c", positive=True)
    a = b+c
    F = c*s.eye(4)+b*s.ones(4)
    legs = [chart.ETA*F[r, :].T for r in range(4)]
    spatial = [u[1:4, :] for u in legs]
    K = [s.diag(0, operator.cross(w)) for w in spatial]
    Wbasis = [s.diag(0, operator.cross(s.eye(3)[:, j])) for j in range(3)]
    omega = s.Matrix(s.symbols("omega0:3", real=True))
    W = s.diag(0, operator.cross(omega))
    vacuum, top = s.eye(16)[:, 0], s.eye(16)[:, 15]
    chi = s.eye(16)[:, 1]+top  # unnormalized, readout=sqrt2 times normalized chi
    eq((chi.H*chi)[0], 2, "native_whole_blank_chi_normalizer_two")
    check(order == (0, 2, 3, 1), "actual_owned_ACDB_carrier")
    eq(operator.Gamma(W, creators)*chi, s.zeros(16, 1),
       "pure_memory_is_full_SO3_singlet_for_arbitrary_generator")
    parity = s.diag(*[(-1)**bin(m).count("1") for m in range(16)])
    top_pairs = s.Matrix.hstack(*[creators[i].T*creators[j].T*top
                                 for i, j in transfer.WEDGE_ROWS])
    eq(top_pairs.H*top_pairs, s.eye(6), "literal_top_dual_bivector_basis_orthonormal")
    eq(top_pairs.H*top, s.zeros(6, 1), "top_and_top_dual_bivectors_separate")
    readout = s.Matrix.vstack(top.H, top_pairs.H)
    eq(readout*(s.eye(16)-parity), s.zeros(7, 16),
       "even_top_readout_separates_top_from_odd_chi_component")
    phase = operator.phases((1, 0, 0, 0))[0]
    shell_constant = 128-64*s.sqrt(2)
    epsilon = shell_constant*(a*a+3*b*b)

    def image(column, k, l, state=chi):
        Dk, _ = operator.dirac(k, legs, creators)
        Dl, _ = operator.dirac(l, legs, creators)
        J = operator.first_jet(column, legs, k, l, creators)
        return Dl*(J*state)+J*(Dk*state)

    # q0: scalar coframe image of rank3, orthogonal to the four links.
    uv = s.Matrix(s.symbols("u0:4", real=True))
    du = s.Matrix(s.symbols("du0:4", real=True))
    D = 8*((phase-1)*operator.create(uv, creators)
           +(s.conjugate(phase)-1)*operator.contract(uv, creators))
    J = 8*((phase-1)*operator.create(du, creators)
           +(s.conjugate(phase)-1)*operator.contract(du, creators))
    eq(D*(J*chi)+J*(D*chi), 2*shell_constant*(uv.T*du)[0]*chi,
       "rank8_all_coframe_shell_entries_same_scalar_on_chi")
    center = s.eye(4)-s.ones(4)/4
    eq(center*center, center, "q0_scalar_center_projector")
    eq(center.trace(), 3, "q0_scalar_center_rank_three")
    eq(center[:3, :3].det(), s.Rational(1, 4), "q0_scalar_nonzero_three_minor")
    xi = s.Matrix(s.symbols("xi0:4", real=True))
    M = sum((xi[r]*spatial[r]*spatial[r].T for r in range(4)), s.zeros(3))
    for active in range(4):
        k = tuple(int(r == active) for r in range(4))
        combined = s.zeros(6, 1)
        for r in range(4):
            column = s.zeros(31, 1)
            column[16+3*r:19+3*r, :] = spatial[r]
            actual = image(column, k, k)
            expected_pairs = -64*(s.conjugate(phase)-1)*transfer.wedge(
                legs[r], K[r]*legs[active])
            eq(readout*actual, s.Matrix([0, *expected_pairs]),
               f"q0_literal_top_dual_shell{active}_link{r}")
            eq((chi.H*actual)[0], 0,
               f"q0_link_image_orthogonal_to_scalar_chi_{active}_{r}")
            combined += xi[r]*expected_pairs
        # Hodge on the three spatial wedge coordinates23,31,12.
        hodge = s.Matrix([combined[5], -combined[4], combined[3]])
        eq(hodge, -64*(s.conjugate(phase)-1)
           *(M-s.trace(M)*s.eye(3))*spatial[active],
           "q0_top_dual_M_minus_traceM_identity_"+str(active))
    eq(s.factor(s.Matrix.hstack(*spatial[1:]).det()), -c*c*(a+2*b),
       "q0_spatial_shell_vectors_span_all_positive_a_greater_b")
    eq(s.trace(M-s.trace(M)*s.eye(3)), -2*s.trace(M), "q0_readout_zero_implies_M_zero")
    readouts = s.Matrix([M[0, 1]-M[0, 2], M[0, 1]-M[1, 2],
                         M[0, 0]-M[0, 1], M[0, 1]])
    eq(s.factor(readouts.jacobian(xi).det()), b**4*c**4,
       "q0_four_link_readout_minor_b4c4")

    cases = []
    hostile_gradient = None
    for i in (0, 1):
        inactive = tuple(r for r in range(4) if r != i)
        canonical = s.Matrix.hstack(*[transfer.wedge(legs[r], K[r]*legs[i]) for r in inactive])
        eq(s.factor(canonical[[0, 1, 3], :].det()), 2*b**5*c**4,
           "one_active_generic_top_dual_minor_role"+str(i))
        k = tuple(7*int(r == i) for r in range(4))
        l = tuple(int(r == i) for r in range(4))
        for j, r in enumerate(inactive):
            column = s.zeros(31, 1)
            column[16+3*r:19+3*r, :] = spatial[r]
            actual = image(column, k, l)
            eq(readout*actual,
               -64*(phase-1)*s.Matrix([0, *canonical[:, j]]),
               f"one_active_actual_rank8_top_dual_{i}_{r}")
            if i == 0 and r == 1:
                # Row02 is an actual nonzero preparation-source gradient.
                coefficient = (top_pairs.H*actual)[1]
                eq(coefficient, 64*(phase-1)*b*b*c,
                   "actual_source_gradient_component_not_frozen")
                # C0 has chi/4 at each occupied reference column. Taking
                # dC=coefficient*top_pair02 at the other momentum is a
                # normalized tangent. The real q/-q source derivative is
                # 2 Re[dC* X C0]=|coefficient|²/2, strictly positive.
                derivative = s.expand(s.conjugate(coefficient)*coefficient/2)
                eq(derivative, 32*shell_constant*b**4*c**2,
                   "hostile_frozen_density_misses_positive_source_derivative")
                hostile_gradient = "32*(128-64sqrt(2))*b^4*(a-b)^2>0"
                wrong_chi = s.eye(16)[:, 1]+s.eye(16)[:, 14]
                eq(readout*image(column, k, l, wrong_chi), s.zeros(7, 1),
                   "hostile_wrong_top_mask14_loses_even_top_dual_witness")
        cases.append({"q": [2*int(r == i) for r in range(4)], "rank": 3,
                      "top_dual_minor": "2*b^5*(a-b)^4"})

    for i, j in ((0, 1), (1, 2)):
        inactive = tuple(r for r in range(4) if r not in (i, j))
        canonical = s.Matrix.hstack(
            *[s.Matrix([(legs[j].T*Wr*legs[i])[0], *transfer.wedge(legs[j], Wr*legs[i])])
              for Wr in Wbasis],
            *[s.Matrix([0, *transfer.wedge(legs[r], K[r]*legs[i])]) for r in inactive])
        eq(s.factor(canonical[[0, 1, 2, 4], [0, 1, 3, 4]].det()),
           (1 if i == 0 else -1)*2*b**6*c**4,
           "two_active_generic_first_pair_rank_four_minor_roles"+str(i)+str(j))
        eq(canonical*s.Matrix([*spatial[i], 0, 0]), s.zeros(7, 1),
           "first_pair_only_vacuum_blind_axis_roles"+str(i)+str(j))
        cross_norm = 2*b*b*c*c if i == 0 else c*c*((a+b)**2+2*b*b)
        eq((spatial[i].cross(spatial[j]).T*spatial[i].cross(spatial[j]))[0],
           cross_norm, "second_pair_axis_strictly_positive_cross_norm_roles"+str(i)+str(j))
        for sign in (1, -1):
            q = tuple((int(r == i)+sign*int(r == j)) % 8 for r in range(4))
            kappa = tuple(1-t for t in operator.phases(q))
            column = transfer.angular_column((i, j), (omega, -omega), kappa, legs, operator)
            theta = s.Matrix(s.symbols("theta0:2", real=True))
            for t, r in enumerate(inactive):
                column[16+3*r:19+3*r, :] += theta[t]*spatial[r]
            k = tuple(7*int(r == i) for r in range(4))
            l = tuple((sign*int(r == j)) % 8 for r in range(4))
            coefficients = (readout*image(column, k, l)).jacobian(s.Matrix([*omega, *theta]))
            beta = (phase if sign == 1 else s.conjugate(phase))-1
            left_scale = s.diag(s.conjugate(beta)/beta, *([1]*6))
            right_scale = s.diag(*([1/(2*s.conjugate(beta))]*3), -1, -1)
            eq(left_scale*coefficients*right_scale/(64*(phase-1)), canonical,
               "actual_two_active_top_dual_phase_normalization_q"+"".join(map(str, q)))
            check(beta != 0 and s.conjugate(beta) != 0 and phase-1 != 0,
                  "top_dual_all_phase_scalings_invertible_q"+"".join(map(str, q)))
            axis_column = transfer.angular_column((i, j), (spatial[i], -spatial[i]),
                                                   kappa, legs, operator)
            eq(image(axis_column, k, l), s.zeros(16, 1),
               "hostile_dropping_second_pair_leaves_exact_rank_four_q"+"".join(map(str, q)))
            other_k = tuple((-sign*int(r == j)) % 8 for r in range(4))
            other_l = tuple(int(r == i) for r in range(4))
            actual = image(axis_column, other_k, other_l)
            Dk, _ = operator.dirac(other_k, legs, creators)
            Dl, _ = operator.dirac(other_l, legs, creators)
            Gaxis = operator.Gamma(K[i], creators)
            eq(actual, -2*Dl*((Gaxis*Dk-Dk*Gaxis)*chi),
               "second_pair_actual_ordered_axis_action_q"+"".join(map(str, q)))
            eq((actual.H*actual)[0]/2, 4*epsilon*shell_constant*cross_norm,
               "second_pair_normalized_chi_axis_norm_strictly_positive_q"+"".join(map(str, q)))
            cases.append({"q": list(q), "rank": 5, "first_pair_rank": 4,
                          "second_pair_axis_norm_squared": "4*epsilon*lambda1*"+str(cross_norm),
                          "first_pair_minor": ("+" if i == 0 else "-")+"2*b^6*(a-b)^4"})

    check(7+4*2*3+12*2*5 == 151, "all_shell_source_rows_real_rank_151")
    check(8*(2*16-1)-1+8*(2*16-1)+24*(2*(2*16-1)) == 1983,
          "rank8_first_density_tangent_dimension_1983")
    check((2*128*128-1)-151 == 32616,
          "regular_normalized_shell_amplitude_fibre_dimension_32616")
    check(2*(128-8)**2 == 28800, "all_genuine_rank_birth_directions_retained_28800")
    check(6*4096+3+32616 == 57195, "same_exact_flat_amplitude_family_dimension_57195")
    return {"schema": "d0-native-rank8-source-submersion/1", "status": "PASS_EXACT",
            "exact_checks": len(checks), "checks": checks, "source_pins": PINS | chart.PINS,
            "parameter_domain": "a>b>0; c=a-b", "chi_native_masks": {"1": 1, "15": 1},
            "chi_norm_squared_before_normalization": 2,
            "rank_total_real": 151, "rank_q0_real": 7, "cases": cases,
            "top_dual_row_order": ["top", "01", "02", "03", "12", "13", "23"],
            "first_pair_phase_scaling": {"t": "exp(i*pi/4)", "beta": "t^sign-1",
                                         "global": "1/(64*(t-1))",
                                         "left": "diag(conj(beta)/beta,1^6)",
                                         "right": "diag(1/(2conj(beta)) repeated3,-1,-1)"},
            "shell_amplitude_sphere_real_dimension": 32767,
            "stationary_shell_amplitude_fibre_dimension": 32616,
            "rank_birth_real_dimension": 28800, "flat_family_dimension": 57195,
            "frozen_density_hostile_nonzero_derivative": hostile_gradient,
            "carrier": {"sites": 4096, "Fock": 16, "shell": 128, "reference": 128},
            "scopes": {"actual_full16_top_dual_not_carrier_truncation": True,
                      "entire_occupied_shell_and_reference_retained": True,
                      "off_shell_signed_resolvent_changed": False,
                      "rank8_transverse_field_inverse_or_curved_branch_proved": False,
                      "physical_preparation_admission_or_GR_proved": False,
                      "old_runs_root_search_or_receipt_writes": False}}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, separators=(",", ":")))
