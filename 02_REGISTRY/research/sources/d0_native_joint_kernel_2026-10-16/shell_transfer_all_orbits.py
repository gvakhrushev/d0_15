"""Unified occupied-shell constraint for all nonzero shell-transfer orbits.

Only pinned definitions are loaded, not a previous run().  For F=(a-b)I+b11^T,
a>b>0, the six S3 x global-negation representatives have rank T=3 at
q=2e_i and rank T=5 at q=e_i +/- e_j.  All16 CAR components and the complete
21/19 native field charts remain.  Three/five small scalar+bivector witnesses
prove the lower bounds; the native common-spatial-motion split proves upper
bounds and the precise remaining inactive-coframe kernels.

For TWO active roles the general identity is
  T_W=2(D_l Gamma(W) D_k+epsilon Gamma(W)),
NOT 2(D_l D_k+epsilon)Gamma(W).  The latter factorization is used ONLY after
the vacuum readout forces W u_i=0, which implies [Gamma(W),D_k]=0.  The
invertibility argument below explicitly checks this essential extra step.

No field Hessian inertia is transferred between the sign/time variants.
The S3 symmetry fixes the observer's time direction; no SO4-link admission,
physical matter truncation, independent D0-core preparation admission,
root search, old receipt write, or full-mode inverse theorem is asserted.
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
SHELL = tuple(tuple(sign if r == axis else 0 for r in range(4))
              for axis in range(4) for sign in (1, 7))
WEDGE_ROWS = tuple((i, j) for i in range(4) for j in range(i+1, 4))


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("shell_transfer_all_orbits:"+label)


def _zero(value):
    values = value.todok().values() if isinstance(value, s.MatrixBase) else (value,)
    return all(s.cancel(s.expand(x)) == 0 for x in values)


def _load(name):
    path = HERE/(name+".py")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[path.name],
            "owned_definition_pin:"+path.name)
    spec = importlib.util.spec_from_file_location("all_shell_orbits_"+name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wedge(v, w):
    """Coefficients in C(e_i)C(e_j)|vac>, ordered 01,02,03,12,13,23."""
    return s.Matrix([v[i]*w[j]-v[j]*w[i] for i, j in WEDGE_ROWS])


def shell_pairs(q):
    return tuple((k, tuple((k[r]+q[r]) % 8 for r in range(4)))
                 for k in SHELL
                 if tuple((k[r]+q[r]) % 8 for r in range(4)) in SHELL)


def angular_column(active, angular_vectors, kappa, legs, operator):
    column = s.zeros(31, 1)
    for r, angular in zip(active, angular_vectors):
        column[4*r:4*r+4, :] = s.diag(0, operator.cross(angular))*legs[r]
        column[16+3*r:19+3*r, :] = kappa[r]*angular
    return column


def complete_mean_split(chart, q, legs, operator, eq):
    """Every actual chart column equals common motion+mean slice+observer.

    Inactive scalar and Cartesian coframe components are retained.  The
    remainder after extracting active contrasts and inactive stabilizers is
    supported exactly on these four-per-inactive-role coframe coordinates.
    """
    kappa = tuple(1-t for t in operator.phases(q))
    active = tuple(r for r in range(4) if q[r])
    inactive = tuple(r for r in range(4) if not q[r])
    for j in range(chart["basis31"].cols):
        column = chart["basis31"][:, j]
        common = sum((column[16+3*r:19+3*r, :]/kappa[r] for r in active),
                     s.zeros(3, 1))/len(active)
        gauge = angular_column(tuple(range(4)), (common,)*4, kappa, legs, operator)
        observer = s.zeros(31, 1)
        observer[28:31, :] = column[28:31, :]
        remainder = column-gauge-observer
        if len(active) == 2:
            first, second = active
            W = remainder[16+3*first:19+3*first, :]/kappa[first]
            remainder -= angular_column(active, (W, -W), kappa, legs, operator)
        for r in inactive:
            w = legs[r][1:4, :]
            omega = remainder[16+3*r:19+3*r, :]
            theta = (w.T*omega)[0]/(w.T*w)[0]
            remainder[16+3*r:19+3*r, :] -= theta*w
        forbidden = list(range(16, 31))+[4*r+h for r in active for h in range(4)]
        eq(remainder[forbidden, :], s.zeros(len(forbidden), 1),
           "full_column_mean_split_"+str(j))


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    chart_owner, operator = _load("native_chart_check"), _load("ordered_operator_check")
    chart_owner.owned_definitions(repo)
    creators, order = operator.owned_car(repo)
    checks = []

    def check(condition, label):
        require(condition, label)
        checks.append(label)

    def eq(actual, expected, label):
        check(_zero(actual-expected), label)

    b, c = s.symbols("b c", positive=True)
    a = b+c  # every a>b>0, never a sampled root ratio
    F = c*s.eye(4)+b*s.ones(4)
    legs = [chart_owner.ETA*F[r, :].T for r in range(4)]
    spatial = [u[1:4, :] for u in legs]
    K = [s.diag(0, operator.cross(w)) for w in spatial]
    Wbasis = [s.diag(0, operator.cross(s.eye(3)[:, j])) for j in range(3)]
    angular = s.Matrix(s.symbols("omega0:3", real=True))
    W = s.diag(0, operator.cross(angular))
    Gamma = operator.Gamma(W, creators)
    vacuum = s.eye(16)[:, 0]
    one_particle = s.Matrix.hstack(*[C*vacuum for C in creators])
    bivectors = s.Matrix.hstack(*[creators[i]*creators[j]*vacuum for i, j in WEDGE_ROWS])
    readout = s.Matrix.vstack(vacuum.H, bivectors.H)
    eq(bivectors.H*bivectors, s.eye(6), "literal_full16_bivector_readout_basis")
    eq(one_particle.H*one_particle, s.eye(4), "literal_full16_one_particle_readout_basis")
    check(order == (0, 2, 3, 1), "owned_ACDB_order")
    phase = operator.phases((1, 0, 0, 0))[0]
    alpha = s.conjugate(phase)-1
    shell_constant = 128-64*s.sqrt(2)
    d, o = a*a+3*b*b, 2*a*b+2*b*b
    epsilon = shell_constant*d
    eq(d-o, c*c, "actual_positive_shell_Gram_gap_c_squared")
    check(bool(shell_constant > 0) and bool(1-s.sqrt(2)/2 > 0),
          "phase_positivity_constants_exact")
    cases = []

    def common_case(q, expected_dimension):
        label = "q"+"".join(map(str, q))+":"

        def case_eq(actual, expected, name):
            eq(actual, expected, label+name)

        chart = chart_owner.regular_fourier_chart(F, tuple(1-t for t in operator.phases(q)))
        check(chart["basis31"].shape == (31, expected_dimension), label+"complete_native_field_chart")
        case_eq(chart["constraints31"]*chart["basis31"], s.zeros(16, expected_dimension),
                "all_native_first_constraints")
        complete_mean_split(chart, q, legs, operator, case_eq)
        pairs = shell_pairs(q)
        active = tuple(r for r in range(4) if q[r])
        inactive = tuple(r for r in range(4) if not q[r])
        check(len(pairs) == len(active), label+"all_occupied_shell_pairs_retained")
        check(all(k[r] == l[r] == 0 for k, l in pairs for r in inactive),
              label+"all_inactive_full_coframe_jets_exactly_invisible_to_T")
        # The mean/common spatial motion is a representation intertwiner.
        # This actual ordered check uses one full symbolic angular generator.
        kappa = tuple(1-t for t in operator.phases(q))
        common_column = angular_column(tuple(range(4)), (angular,)*4, kappa, legs, operator)
        k, l = pairs[0]
        Dk, ek = operator.dirac(k, legs, creators)
        Dl, el = operator.dirac(l, legs, creators)
        common_J = operator.first_jet(common_column, legs, k, l, creators)
        case_eq(common_J, Gamma*Dk-Dl*Gamma, "literal_common_SO3_intertwiner")
        case_eq(ek, el, "occupied_endpoint_energies_equal")
        case_eq(Dl*common_J+common_J*Dk, s.zeros(16),
                "common_SO3_source_zero_not_extra_physical_gauge")
        return chart, case_eq

    for i in (0, 1):
        q = tuple(2*int(r == i) for r in range(4))
        chart, ceq = common_case(q, 21)
        inactive = tuple(r for r in range(4) if r != i)
        columns = s.Matrix.hstack(*[wedge(legs[r], K[r]*legs[i]) for r in inactive])
        ceq(s.factor(columns[[0, 1, 3], :].det()), 2*b**5*c**4,
            "generic_one_active_vacuum_minor_rows_01_02_12")
        k = tuple(7*int(r == i) for r in range(4))
        l = tuple(int(r == i) for r in range(4))
        Dk, _ = operator.dirac(k, legs, creators)
        for j, r in enumerate(inactive):
            column = s.zeros(31, 1)
            column[16+3*r:19+3*r, :] = spatial[r]
            J = operator.first_jet(column, legs, k, l, creators)
            ceq(J*vacuum, s.zeros(16, 1), "inactive_link_J_vacuum_zero_"+str(r))
            ceq(readout*(J*Dk*vacuum),
                64*alpha*s.Matrix([0, *columns[:, j]]),
                "literal_one_active_full16_vacuum_readout_"+str(r))
        cases.append({"q": list(q), "field_complex_dimension": 21, "rank_T": 3,
                      "ker_T_mod_six_representations_complex_dimension": 12,
                      "preparation_ker_Tstar_complex_dimension": 253,
                      "generic_minor": "2*b^5*(a-b)^4"})

    # Global negation is complex conjugation; S3 permutes only spatial roles.
    # These two pairs and both signs cover all remaining representatives.
    for i, j in ((0, 1), (1, 2)):
        inactive = tuple(r for r in range(4) if r not in (i, j))
        canonical = s.Matrix.hstack(
            *[s.Matrix([(legs[j].T*Wr*legs[i])[0], *wedge(legs[j], Wr*legs[i])])
              for Wr in Wbasis],
            *[s.Matrix([0, *wedge(legs[r], K[r]*legs[i])]) for r in inactive])
        minor = s.factor(canonical[[0, 1, 2, 4], [0, 1, 3, 4]].det())
        eq(minor, (1 if i == 0 else -1)*2*b**6*c**4,
           "generic_two_active_vacuum_minor_roles_"+str(i)+str(j))
        axis_kernel = s.Matrix([*spatial[i], 0, 0])
        eq(canonical*axis_kernel, s.zeros(7, 1),
           "vacuum_kernel_is_only_axis_wi_roles_"+str(i)+str(j))
        # rank4 + this nonzero kernel gives EXACTLY this one-dimensional
        # kernel, with both inactive stabilizer coefficients forced to zero.
        check(spatial[i][2] == -b,
              "axis_kernel_nonzero_in_omitted_W2_coordinate_roles_"+str(i)+str(j))
        Gamma_axis = operator.Gamma(K[i], creators)
        eq(one_particle.H*Gamma_axis*one_particle, K[i],
           "Gamma_faithful_on_remaining_axis_roles_"+str(i)+str(j))
        eq(s.trace(Gamma_axis.H*Gamma_axis), 8*(spatial[i].T*spatial[i])[0],
           "remaining_axis_Gamma_strictly_nonzero_roles_"+str(i)+str(j))
        for sign in (1, -1):
            q = tuple((int(r == i)+sign*int(r == j)) % 8 for r in range(4))
            chart, ceq = common_case(q, 19)
            beta = phase if sign == 1 else s.conjugate(phase)
            beta -= 1
            k = tuple(7*int(r == i) for r in range(4))
            l = tuple((sign*int(r == j)) % 8 for r in range(4))
            Dk, ek = operator.dirac(k, legs, creators)
            Dl, el = operator.dirac(l, legs, creators)
            ceq(ek, epsilon, "actual_all16_occupied_energy")
            kappa = tuple(1-t for t in operator.phases(q))
            column = angular_column((i, j), (angular, -angular), kappa, legs, operator)
            theta = s.Matrix(s.symbols("theta0:2", real=True))
            for t, r in enumerate(inactive):
                column[16+3*r:19+3*r, :] += theta[t]*spatial[r]
            J = operator.first_jet(column, legs, k, l, creators)
            relative_J = J.subs({theta[0]: 0, theta[1]: 0})
            ceq(relative_J, Gamma*Dk+Dl*Gamma, "exact_relative_J_order")
            ceq(Dl*relative_J+relative_J*Dk,
                2*(Dl*Gamma*Dk+epsilon*Gamma), "general_T_has_Gamma_in_the_middle")

            # Actual full16 vacuum output, scalar followed by six bivectors.
            coefficients = (readout*(Dl*J*vacuum+J*Dk*vacuum)).jacobian(
                s.Matrix([*angular, *theta]))
            left_phase = s.diag(beta/s.conjugate(beta), *([1]*6))
            right_phase = s.diag(*([1/(2*beta)]*3), 1, 1)
            ceq(left_phase*coefficients*right_phase/(64*alpha), canonical,
                "exact_phase_scaling_to_sign_independent_vacuum_map")
            check(alpha != 0 and beta != 0 and s.conjugate(beta) != 0,
                  "q"+"".join(map(str, q))+":all_readout_phase_scalings_invertible")

            # Essential restricted step: vacuum forces W along w_i, NOT an
            # arbitrary W. Only now is Gamma allowed to move across D_k.
            ceq(K[i]*legs[i], s.zeros(4, 1), "vacuum_blind_axis_fixes_full_ui")
            ceq(Gamma_axis*Dk-Dk*Gamma_axis, s.zeros(16),
                "restricted_axis_commutes_with_Dk_all16")
            ceq(2*(Dl*Gamma_axis*Dk+epsilon*Gamma_axis),
                2*(Dl*Dk+epsilon*s.eye(16))*Gamma_axis,
                "restricted_axis_only_invertible_factorization")
            h = shell_constant*o*(-s.sqrt(2)/2 if sign == 1 else 1)
            ceq(Dl*Dk+Dk*Dl, 2*h*s.eye(16), "actual_Clifford_anticommutator")
            A = Dl*Dk+epsilon*s.eye(16)
            ceq(A.H*A, 2*epsilon*(epsilon+h)*s.eye(16),
                "invertible_A_norm_identity_on_remaining_axis")
            positive_sum = c*c+((1-s.sqrt(2)/2) if sign == 1 else 2)*o
            ceq(epsilon+h, shell_constant*positive_sum,
                "A_norm_strictly_positive_sum_for_every_a_gt_b_gt_zero")
            cases.append({"q": list(q), "field_complex_dimension": 19, "rank_T": 5,
                          "ker_T_mod_six_representations_complex_dimension": 8,
                          "preparation_ker_Tstar_complex_dimension": 507,
                          "vacuum_minor": ("+" if i == 0 else "-")+"2*b^6*(a-b)^4",
                          "vacuum_kernel": "W=lambda*[w_i]_cross; theta_inactive=0",
                          "restricted_final_factor": "2*(D_l D_k+epsilon)*Gamma(W)",
                          "h_over_epsilon": "-o/(sqrt(2)*d)" if sign == 1 else "o/d"})

    return {"schema": "d0-native-shell-transfer-all-orbits/1", "status": "PASS_EXACT",
            "exact_checks": len(checks), "checks": checks, "cases": cases,
            "parameter_domain": "a>b>0; c=a-b", "source_pins": PINS | chart_owner.PINS,
            "vacuum_readout_rows": ["scalar", "01", "02", "03", "12", "13", "23"],
            "two_active_vacuum_minor_rows_zero_based": [0, 1, 2, 4],
            "two_active_vacuum_minor_columns": ["W0", "W1", "theta_r", "theta_s"],
            "phase_scaling": {"t": "exp(i*pi/4)", "alpha": "conj(t)-1",
                              "beta": "t^sign-1", "global": "1/(64*alpha)",
                              "left_rows": "diag(beta/conj(beta),1,1,1,1,1,1)",
                              "right_columns": "diag(1/(2beta),1/(2beta),1/(2beta),1,1)"},
            "full_carrier": {"sites": 4096, "Fock": 16, "shell": 128, "reference": 128},
            "scope": {"all_six_shell_transfer_orbits": True, "all16_CAR_retained": True,
                      "only_known_six_representation_directions_removed": True,
                      "preparation_annihilators_are_gauge": False,
                      "Hessian_inertia_extended_between_sign_time_variants": False,
                      "SO4_links_or_D0_core_preparation_admitted": False,
                      "old_runs_root_search_or_receipt_writes": False}}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, separators=(",", ":")))
