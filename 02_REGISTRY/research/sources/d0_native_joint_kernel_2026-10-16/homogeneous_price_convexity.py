"""Finite-m homogeneous Gram convexity and the actual constant-SO4 orbit.

The three-mode symbolic calculation ONLY verifies an analytic identity of
the same finite B-price family. It is not substituted for the native lattice.
Native inequalities consume the immutable complete4096-mode interval owner,
with all16 Fock states, reference128, ground mode and full Z retained.

For native homogeneous coframes with identity links and observer e0, the
actual CAR square is scalar at every momentum. Thus constant SO4 rotations
of the coframes leave Delta, the declared v8 price, and the root moments
unchanged. The full16 trace identity below checks admitted stabilizer-link
sources as well; restricted price invariance alone would not prove those
rows. Local three-dimensional changes of the Lorentz Gram are retained as
additional critical directions, not newly admitted physical gauge.

No existing run(), root search, receipt writer, huge symbolic16384 power,
physical preparation selection, Morse-Bott theorem or GR claim occurs here.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PINS = {
    "full_symbol_interval_weights.py": "0d8651dae3b6b7ba2049a1c71ac47895e536f9ccc5f85bf9978c133c75ccfc18",
    "ordered_operator_check.py": "f2f9903685c2c522d4c850d335dfb9435c932182962402da499ff8a7a10a9418",
}
FOCK, REFERENCE, M_POWER = 16, 128, 16384
ETA = s.diag(1, -1, -1, -1)


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("homogeneous_price_convexity:"+label)


def load(repo, name):
    path = repo/HERE.relative_to(ROOT)/name
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[name], "definition_pin:"+name)
    spec = importlib.util.spec_from_file_location("homogeneous_convexity_"+name[:-3], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def zero(value):
    entries = value if isinstance(value, s.MatrixBase) else (value,)
    return all(s.expand(entry) == 0 for entry in entries)


def unit(i, j):
    matrix = s.zeros(4)
    matrix[i, j] = 1
    return matrix


def symbolic_price(check):
    """Direct second derivative with independent lambda_i and global Z."""
    t = s.Symbol("t", real=True)
    alpha, fugacity, multiplicity = s.symbols("alpha z M", positive=True)
    m = s.Symbol("m", integer=True, positive=True)
    lam = s.symbols("lambda0:3", real=True)
    direction = s.symbols("f0:3", real=True)
    positive_b = s.symbols("B0:3", positive=True)
    beta, c = m*alpha, (m-1)*alpha
    e_t = [(1-alpha*(lam[i]+t*direction[i]))**m for i in range(3)]
    Z_t = FOCK*sum(e_t)
    A_t = [1-fugacity+fugacity*e for e in e_t]
    price = s.log(Z_t)/beta-FOCK*multiplicity*sum(s.log(A) for A in A_t)
    # B_i=1-alpha*lambda_i are independent positive affine coordinates.
    substitution = {lam[i]: (1-positive_b[i])/alpha for i in range(3)}
    direct = s.diff(price, t, 2).subs(t, 0).subs(substitution)
    e = [B**m for B in positive_b]
    Z = FOCK*sum(e)
    weights = [FOCK*value/Z for value in e]
    y = [direction[i]/positive_b[i] for i in range(3)]
    A = [1-fugacity+fugacity*value for value in e]
    mean = sum(weights[i]*y[i] for i in range(3))
    square = sum(weights[i]*y[i]**2 for i in range(3))
    four_terms = (c*square-beta*mean**2
                  -multiplicity*beta*fugacity*c*Z*sum(weights[i]*y[i]**2/A[i] for i in range(3))
                  +multiplicity*beta**2*fugacity**2*Z
                   *sum(weights[i]*e[i]*y[i]**2/A[i]**2 for i in range(3)))
    check(s.factor(direct-four_terms) == 0, "independent_lambda_full_logZ_logdet_four_term_identity")
    check(s.factor(c-beta*(1-1/m)) == 0, "finite_m_correction_retained_exactly")
    witness = {m: 2, alpha: s.Rational(1, 8), fugacity: s.Rational(1, 5), multiplicity: REFERENCE,
               positive_b[0]: 1, positive_b[1]: s.Rational(3, 4), positive_b[2]: s.Rational(1, 2),
               direction[0]: 0, direction[1]: 1, direction[2]: 2}
    normalizer_loss = s.factor((beta*mean**2).subs(witness))
    check(normalizer_loss > 0, "dropping_negative_global_normalizer_square_is_rejected")
    return {"scope": "three-independent-mode symbolic identity test only; native bound uses all4096 modes",
            "power": "generic positive integer m, beta=m*alpha, c=(m-1)*alpha",
            "global_normalizer_term": "-beta*(E_w y)^2",
            "exact_nonzero_missing_normalizer_witness": str(normalizer_loss)}


def native_bounds(owner, spectral, check):
    bounds = owner.bounds
    Z = spectral["Z"]
    beta, fugacity = spectral["beta"], spectral["fugacity"]
    iv = spectral["iv_ctx"]
    w0 = FOCK/Z
    delta = REFERENCE*beta*fugacity*Z/(1-fugacity)
    check(bounds(Z)[1] < 50 and bounds(Z)[0] > 0, "actual_full_partition_Z_strictly_between_zero_and_50")
    check(0 < bounds(beta)[0] and bounds(beta)[1] < 1, "actual_beta_strictly_between_zero_and_one")
    check(len(spectral["modes"]) == 4096 and len(spectral["feature_data"]) == 119,
          "actual_all4096_modes_and119_exact_features_retained")
    check(spectral["metadata"]["occupied_shell_states"] == REFERENCE,
          "all128_occupied_matter_shell_states_retained")
    check(bounds(spectral["lambda"][0]) == (Fraction(0), Fraction(0)),
          "native_ground_energy_exact_zero_not_removed")
    check(bounds(w0)[0] > Fraction(8, 25), "ground_weight_w0_strictly_greater_8_over_25")
    rational_delta = Fraction(6400, 2**20-1)
    check(bounds(delta)[1] < rational_delta < Fraction(1, 100),
          "actual_feedback_delta_below_exact_rational_6400_over_2pow20_minus1")
    check(Fraction(1, M_POWER) < Fraction(1, 10000), "finite_power_inverse_strictly_less_1_over_10000")
    coarse_gap = Fraction(8, 25)-Fraction(1, 10000)-Fraction(1, 100)
    check(coarse_gap > Fraction(3, 10), "rational_Cauchy_feedback_gap_strictly_greater_3_over_10")
    coefficient = w0-iv.mpf(1)/M_POWER-(1-iv.mpf(1)/M_POWER)*delta
    check(bounds(coefficient)[0] > Fraction(3, 10), "whole_root_rectangle_actual_coercivity_coefficient")
    check(all(bounds(row["survival"])[0] > 0 for row in spectral["feature_data"].values()),
          "every_native_weight_strictly_positive_at_finite_power")
    return {"root_box": spectral["root_box"], "full_Z": owner.interval_record(Z),
            "beta": owner.interval_record(beta), "ground_weight_w0": owner.interval_record(w0),
            "feedback_delta": owner.interval_record(delta),
            "coercivity_coefficient_before_beta": owner.interval_record(coefficient),
            "exact_coarse_lower_bound": str(coarse_gap),
            "conclusion": "H >= (3*beta/10)*E_w(y^2), with strict positivity for a nonzero Gram variation",
            "Cauchy_reason": "y_ground=0 gives (E_w y)^2 <= (1-w0)*E_w(y^2)",
            "negative_feedback_bound": "A_k>=1-z; drop only the nonnegative fourth term",
            "full_normalizer_retained": True, "ground_Fock_multiplicity": FOCK,
            "shell_reference_dimension": REFERENCE, "finite_power": M_POWER}


def gram_injectivity(check):
    slots = tuple((i, j) for i in range(4) for j in range(i, 4))
    variables = s.symbols("gram0:10", real=True)
    matrix = s.zeros(4)
    for (i, j), value in zip(slots, variables):
        matrix[i, j] = matrix[j, i] = value
    gamma = s.Symbol("gamma", positive=True)
    probes = [gamma*matrix[i, i] for i in range(4)]
    probes += [gamma*(matrix[i, i]+matrix[j, j]+2*matrix[i, j])
               for i in range(4) for j in range(i+1, 4)]
    determinant = s.factor(s.Matrix(probes).jacobian(variables).det())
    check(s.factor(determinant/(2**6*gamma**10)) in (1, -1),
          "ten_axis_paired_axis_Gram_probes_are_injective")
    eighth = (1+s.I)/s.sqrt(2)
    actual_gamma = s.expand(64*(eighth-1)*(s.conjugate(eighth)-1))
    check(actual_gamma == 128-64*s.sqrt(2) and actual_gamma > 0,
          "actual_eighth_root_mode_axis_energy_coefficient_positive")
    return {"axis_modes": "e_i", "paired_axis_modes": "e_i+e_j",
            "probe_count": 10, "probe_determinant": str(determinant),
            "actual_gamma": str(actual_gamma),
            "generic_conclusion": "deltaG -> delta_lambda is injective on all10 real symmetric slots; no mode census"}


def actual_car_orbit(operator, repo, check):
    creators, order = operator.owned_car(repo)
    eye = s.eye(16)
    for i in range(4):
        for j in range(4):
            check(creators[i]*creators[j].T+creators[j].T*creators[i] == int(i == j)*eye,
                  f"owned_all16_CAR_{i}_{j}")
    x, y = s.symbols("vreal0:4", real=True), s.symbols("vimag0:4", real=True)
    v = s.Matrix([x[i]+s.I*y[i] for i in range(4)])
    D = operator.create(v, creators)+operator.contract(v.conjugate(), creators)
    norm2 = sum(x[i]**2+y[i]**2 for i in range(4))
    check(zero(D*D-norm2*eye), "arbitrary_complex_mode_vector_actual_Delta_scalar_on_all16_states")
    skew_generators = [unit(i, j)-unit(j, i) for i in range(4) for j in range(i+1, 4)]
    for h, S in enumerate(skew_generators):
        represented = operator.Gamma(S, creators)
        check(s.trace(represented) == 0, f"full16_skew_representation_trace_zero_{h}")
        for i in range(4):
            for j in range(4):
                trace = s.trace(creators[i]*creators[j].T*represented)
                check(trace == 4*S[j, i], f"full16_general_creator_contraction_generator_trace_{h}_{i}_{j}")
    # Multilinearity of the96 exact entries proves the general identity
    # Tr16(C(u)iota(v)Gamma(S))=4*v^T*S*u for every skew S and every u,v.
    tau = s.Symbol("time_leg", real=True)
    w = s.Matrix(s.symbols("spatial_leg0:3", real=True))
    u = s.Matrix([tau, *w])
    stabilizer = s.diag(0, operator.cross(w))
    check(zero(stabilizer*u), "actual_SO3_own_leg_stabilizer_annihilates_its_full_leg")
    omega = operator.Gamma(stabilizer, creators)
    for j in range(4):
        check(s.expand(s.trace(operator.create(u, creators)*creators[j].T*omega)) == 0,
              f"full16_stabilizer_link_source_vanishes_every_other_leg_component_{j}")

    t = s.Symbol("rotation_parameter", real=True)
    co, si = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    for h, (i, j) in enumerate(( (i, j) for i in range(4) for j in range(i+1, 4) )):
        R = s.eye(4)
        R[i, i] = R[j, j] = co
        R[i, j], R[j, i] = -si, si
        check(all(s.cancel(item) == 0 for item in R.T*R-s.eye(4)), f"full_parameter_SO4_plane_rotation_{h}")
        check(s.cancel(R.det()-1) == 0, f"SO4_plane_rotation_orientation_{h}")
    causal_jets = [S.T*ETA+ETA*S for S in skew_generators]
    check(s.Matrix.hstack(*(s.Matrix(H).reshape(16, 1) for H in causal_jets)).rank() == 3,
          "Lorentz_Gram_changes_have_exactly_three_independent_SO4_directions")
    check(all(zero(causal_jets[i]) for i in (3, 4, 5)),
          "three_spatial_SO3_representation_generators_preserve_Lorentz_Gram")
    return {"owned_exterior_order": list(order), "exterior_dimension": 16,
            "retained_degrees": [0, 1, 2, 3, 4],
            "coframe_orbit": "u_r -> R*u_r for the same constant R in SO4; links remain I, observer remains e0",
            "Euclidean_Gram": "G_rs=u_r^T*u_s unchanged by R^T*R=I",
            "actual_Delta": "Delta_k=lambda_k(G)*I16 exactly, at every momentum",
            "matter_and_feedback": "same Delta and same full shell density, no new action or fitted source",
            "nongauge_Lorentz_Gram_directions": 3,
            "rank_reason": "invertible coframe congruence preserves the rank3 image of S^T*eta+eta*S",
            "full_link_stationarity_reason": "own-leg S_r*u_r=0 and the actual full16 trace identity kill every stabilizer-link source",
            "remaining_stationarity_premise": "existing root has zero full10 homogeneous Gram moments; nonzero Fourier rows vanish by translation invariance",
            "Q_amplitude_Schur_on_homogeneous_coframe": "zero because X is mode-diagonal and scalar on all16 Fock states, hence QXP=0",
            "physical_gauge_or_native_preparation_selection": False}


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    owner = load(repo, "full_symbol_interval_weights.py")
    operator = load(repo, "ordered_operator_check.py")
    checks = []

    def check(condition, label):
        require(condition, label)
        checks.append(label)

    toy = symbolic_price(check)
    spectral = owner.spectral_intervals(repo)  # immutable definitions+intervals, never old run().
    native = native_bounds(owner, spectral, check)
    injectivity = gram_injectivity(check)
    orbit = actual_car_orbit(operator, repo, check)
    return {"schema": "d0-native-homogeneous-price-convexity/1",
            "status": "PASS_FINITE_M_FULL_NORMALIZER_GRAM_CONVEXITY_AND_SO4_ORBIT",
            "exact_checks": len(checks), "checks": checks,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "definition_pins": PINS, "native_scalar_source_pins": spectral["source_pins"],
            "symbolic_identity_toy": toy, "native_whole_root_rectangle_bound": native,
            "Gram_feature_injectivity": injectivity, "homogeneous_SO4_orbit": orbit,
            "all10_Gram_directions_strictly_positive": True,
            "all7_constrained_Gram_directions_positive_if_T0_split_proved": True,
            "T0_rank_or_Morse_Bott_theorem_proved_here": False,
            "old_runs_root_search_or_receipt_writes": False,
            "full_native_action_selection_or_GR_claim": False}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
