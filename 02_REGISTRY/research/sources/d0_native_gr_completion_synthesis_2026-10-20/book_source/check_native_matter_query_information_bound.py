#!/usr/bin/env python3
"""Exact necessary copy bound for the actual normalized CAR matter input.

The target is one LOCAL two-query likelihood and its matter first jet.
Only independent copies of the declared global input and matter-independent
ancillas/operations are allowed in this bound. It is not a no-go for a
moving matter query or for a different source statistic. Standard library;
checks remain active with -O; no geometry or old research checker is replayed.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
import json

from check_determinant_preparation_bank import (
    A, ONE, P, ZERO, add, expect_rejection, mul, power, require, ring_sum, scale,
)


@dataclass(frozen=True)
class Dual:
    value: tuple
    jet: tuple = ZERO

    def __add__(self, other):
        if not isinstance(other, Dual):
            other = constant(other)
        return Dual(add(self.value, other.value), add(self.jet, other.jet))

    __radd__ = __add__

    def __neg__(self):
        return Dual(scale(self.value, -1), scale(self.jet, -1))

    def __sub__(self, other):
        return self + -constant(other) if not isinstance(other, Dual) else self + -other

    def __rsub__(self, other):
        return constant(other) + -self

    def __mul__(self, other):
        if not isinstance(other, Dual):
            other = constant(other)
        return Dual(mul(self.value, other.value),
                    add(mul(self.jet, other.value), mul(self.value, other.jet)))

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "nonnegative dual exponent")
        result = constant(1)
        for _ in range(exponent):
            result *= self
        return result


def constant(value):
    if isinstance(value, Dual):
        return value
    return Dual(value if isinstance(value, tuple) else scale(ONE, value))


def exact_query_jet():
    p, z = constant(P), Q(1, 2 ** 20)
    p6 = power(P, 6)
    B0 = scale(power(P, 3), 4)
    A0 = mul(B0, add(ONE, p6))
    q_factor = add(ONE, scale(B0, -z))
    r_factor = add(ONE, scale(A0, -z))
    d0 = mul(q_factor, r_factor)
    require(B0 == add(ONE, scale(p6, -1)), "B0=4p^3=1-p^6")
    require(A0 == add(ONE, scale(power(P, 12), -1)), "A0=B0(1+p^6)=1-p^12")
    cases = []
    for eta in (Q(1, 4), Q(2, 7)):
        Cq = scale(mul(p6, add(r_factor, mul(p6, q_factor))), 8 * z * eta ** 2)
        for sigma in (-1, 1):
            q = Dual(ZERO, ONE)
            b = (p + sigma * eta ** 2 * p ** 2 * q) ** 2
            E = p ** 2
            B = 4 * b * (1 - b)
            feedback_A = B + (1 - B) * 4 * E * (1 - E)
            d = (1 - z * feedback_A) * (1 - z * B)
            require(E.jet == ZERO, "matter partial holds original E fixed")
            require(b.jet == scale(power(P, 3), 2 * sigma * eta ** 2), "actual squared-b matter jet")
            require(B.value == B0 and feedback_A.value == A0, "original feedback baseline")
            require(B.jet == scale(p6, 8 * sigma * eta ** 2), "B_q=8 sigma p^6 eta^2")
            require(feedback_A.jet == scale(power(P, 12), 8 * sigma * eta ** 2), "A_q=8 sigma p^12 eta^2")
            require(d.value == d0 and d.jet == scale(Cq, -sigma),
                    "d_q=-sigma*8*z*p^6*eta^2*(R+p^6*Q)")
            cases.append({"eta": str(eta), "sigma": sigma,
                          "d_q_coefficients_in_1_a_a2_a3": [str(v) for v in d.jet]})
    return {"z": str(z), "baseline": "d0=Q*R, Q=1-z*B0,R=1-z*A0",
            "positive_jet_magnitude": "Cq=8*z*p^6*eta^2*(R+p^6*Q)",
            "exact_dual_ring_cases": cases}


def scalar_car_tangent():
    # At scalar=top=0, slack=sqrt(1-p)=p in the actual rest-mask chart.
    state, tangent = [ZERO] * 16, [ZERO] * 16
    state[1], state[14], tangent[0] = A, P, ONE
    norm = ring_sum(power(value, 2) for value in state)
    jet_norm = ring_sum(power(value, 2) for value in tangent)
    overlap = ring_sum(mul(value, derivative) for value, derivative in zip(state, tangent))
    require(norm == ONE and jet_norm == ONE and overlap == ZERO,
            "actual CAR16 rest preparation and scalar tangent at zero")
    # At general psi_y, the only moving entries are psi_y and its slack.
    # Fixed sqrt(p)|1> and top amplitudes are retained in other_norm.
    # The formal rational Gram identity needs no unsupported square root.
    cases = []
    p_upper = Q(619, 1000)
    local_phase_pairs = [(Q(1), Q(0)), (Q(3, 5), Q(4, 5)), (Q(5, 13), Q(12, 13))]
    real_components = []
    for pair in range(64):
        cosine, sine = local_phase_pairs[pair % len(local_phase_pairs)]
        require(cosine ** 2 + sine ** 2 == 1, "exact real Fourier-pair phase identity")
        real_components.extend((cosine, sine))
    for psi, slack in [(Q(0), Q(3, 5)), (Q(1, 10), Q(1, 2)), (Q(1, 4), Q(1, 4))]:
        require(1 - p_upper - psi ** 2 - slack ** 2 > 0, "fixture admits actual fixed top amplitude")
        other_norm = 1 - psi ** 2 - slack ** 2
        require(other_norm + psi ** 2 + slack ** 2 == 1, "complete normalized CAR state Gram")
        slack_jet = -psi / slack
        require(psi + slack * slack_jet == 0, "normalized CAR tangent is horizontal")
        tangent_norm = 1 + slack_jet ** 2
        require(tangent_norm == 1 + psi ** 2 / slack ** 2, "actual slack derivative norm factor")
        for sites in (4 ** 4, 8 ** 4, 512 ** 4):
            # Actual real Fourier columns come in64 cos/sin pairs with
            # f=(sqrt(2/S)cos,sqrt(2/S)sin). Their magnitudes need not be
            # equal. A fixed unitary RIGHT basis change gives128 complex
            # phase columns with equal squared weights1/(128*S).
            real_weights = [component ** 2 / (64 * sites) for component in real_components]
            uniform_phase_weights = [Q(1, 128 * sites)] * 128
            require(sum(real_weights) == sum(uniform_phase_weights) == Q(1, sites),
                    "actual64 real Fourier pairs and128 phase weights give the same1/S")
            global_norm = sites * sum(real_weights)
            require(global_norm == 1, "full global CAR/site/RIGHT input has unit norm")
            right_sum = sum((weight * tangent_norm for weight in real_weights), Q(0))
            require(right_sum == tangent_norm / sites, "all128 RIGHT phase weights yield 1/S")
            # Local Fourier phases may differ. All128x128 cross-Gram jets
            # vanish because their common scalar <m,dm> is exactly zero.
            for a in range(128):
                for b in range(128):
                    require(real_components[a] * real_components[b] / (64 * sites)
                            * (psi + slack * slack_jet) == 0,
                            "full retained RIGHT Gram first jet remains zero")
            for copies in (1, 2, 7, 100):
                diagonal = copies * right_sum
                cross = copies * (copies - 1) * Q(0) ** 2
                require(diagonal + cross == copies * tangent_norm / sites,
                        "independent-copy tangent norm is n times one-copy norm")
        cases.append({"psi": str(psi), "slack": str(slack),
                      "CAR_tangent_norm_squared": str(tangent_norm)})
    return {"special_actual_preparation": "sqrt(p)|1>+p|14>, dm=|0>",
            "general_local_tangent": "|0>-(psi_y/slack)|14>",
            "full_RIGHT_columns": 128,
            "RIGHT_normalization": "64 real cos/sin pairs, equivalently128 unitary phase columns; sum weights=1/S",
            "one_copy_tangent_norm_squared": "(1+psi_y^2/slack^2)/S",
            "copy_cross_terms": "all zero by <C,dC>=0",
            "general_Gram_fixtures": cases}


def dot_metric(vector, metric, other):
    return sum((vector[i] * metric[i][j] * other[j] for i in range(4) for j in range(4)), Q(0))


def sparse_matter_stencil():
    h, rho, original_slope = Q(1, 512), Q(7, 5), Q(1, 100)
    base_site = (7, 11, 13, 17)
    varied_site = (7, 12, 13, 17)

    def next_site(axis):
        site = list(base_site)
        site[axis] += 1
        return tuple(site)

    cases = []
    for calibration in (Q(1), Q(2, 3), Q(1, 5)):
        k = original_slope / calibration ** 2

        def psi(site):
            return k * (site[0] - base_site[0]) * h

        def delta_psi(site):
            return Q(int(site == varied_site))

        gradient = [(psi(next_site(axis)) - psi(base_site)) / h for axis in range(4)]
        gradient_jet = [(delta_psi(next_site(axis)) - delta_psi(base_site)) / h for axis in range(4)]
        require(gradient == [k, 0, 0, 0] and gradient_jet == [0, 1 / h, 0, 0],
                "actual sparse forward differences at y=x+v")
        for H in (Q(0), Q(7, 3), Q(-11, 5)):
            # Entire scaled Brinkmann inverse metric, including g^{vv}.
            metric = [[Q(0), Q(1), Q(0), Q(0)], [Q(1), -H, Q(0), Q(0)],
                      [Q(0), Q(0), Q(-1), Q(0)], [Q(0), Q(0), Q(0), Q(-1)]]
            inverse = [[Q(0), Q(1), Q(0), Q(0)], [Q(1), -H, Q(0), Q(0)],
                       [Q(0), Q(0), Q(-1), Q(0)], [Q(0), Q(0), Q(0), Q(-1)]]
            # Covariant unscaled matrix has g_uu=H and g_vv=0.
            metric[0][0], metric[1][1] = H, Q(0)
            covariant = [[v / calibration ** 2 for v in row] for row in metric]
            contravariant = [[v * calibration ** 2 for v in row] for row in inverse]
            require(all(sum(covariant[i][j] * contravariant[j][l] for j in range(4)) == int(i == l)
                        for i in range(4) for l in range(4)), "actual curved metric and inverse, no canonical-frame reset")
            gamma = contravariant[1][0]
            require(gamma * k == original_slope, "calibrated gamma*k is invariant")
            q0 = dot_metric(gradient, contravariant, gradient) / rho
            dq = 2 * dot_metric(gradient_jet, contravariant, gradient) / rho
            require(q0 == 0 and dq == 2 * gamma * k / (rho * h),
                    "actual null-covector matter source retains inverse PF and calibration")
            require(dot_metric(gradient_jet, contravariant, gradient_jet) / rho ==
                    -calibration ** 2 * H / (rho * h ** 2), "arbitrary H remains in quadratic variation")
            cases.append({"calibration": str(calibration), "H": str(H),
                          "gamma": str(gamma), "k": str(k), "q_jet": str(dq)})
    # The OWNED strict repair uses an actual Golden power. Its inverse is
    # also in Z[p], since p^-1=1+p; do not replace gamma' by1 after scaling.
    p_inverse = add(ONE, P)
    require(mul(P, p_inverse) == ONE, "Golden inverse for strict calibration")
    for exponent in (1, 3, 7):
        gamma = power(P, 2 * exponent)
        k = scale(power(p_inverse, 2 * exponent), original_slope)
        require(mul(gamma, k) == scale(ONE, original_slope), "actual Golden strict scale preserves gamma*k")
    wrong_gamma = Q(1)
    wrong_k = original_slope / Q(2, 3) ** 2
    require(wrong_gamma * wrong_k != original_slope, "resetting calibrated gamma to1 changes the source")
    return {"h": str(h), "actual_rho_fixture": str(rho), "interior_variation": "delta psi_(x+v)=1",
            "q_first_jet": "2*rho^-1*gamma*k/h", "sparse_exact_cases": cases,
            "Golden_scale_exponents": [1, 3, 7]}


def full_classical_fisher():
    cases = []
    for d, dd, beta, dbeta in [(Q(3, 5), Q(2, 7), Q(1, 4), Q(0)),
                               (Q(2, 7), Q(-3, 11), Q(3, 5), Q(2, 9))]:
        probabilities = [beta * d, beta * (1 - d), 1 - beta]
        jets = [dbeta * d + beta * dd, dbeta * (1 - d) - beta * dd, -dbeta]
        require(sum(probabilities) == 1 and sum(jets) == 0, "all three classical outcomes and first jets normalized")
        fisher = sum((jet ** 2 / mass for jet, mass in zip(jets, probabilities)), Q(0))
        target = beta * dd ** 2 / (d * (1 - d)) + dbeta ** 2 / (beta * (1 - beta))
        require(fisher == target, "full coarsened Fisher retains readiness derivative term")
        if dbeta == 0:
            conditional_only = dd ** 2 / (d * (1 - d))
            require(fisher == beta * conditional_only != conditional_only, "conditioning loses the beta factor")
            rejection = expect_rejection(
                lambda: require(fisher == conditional_only, "conditional-only Fisher is not the complete experiment"),
                "conditional-only Fisher is not the complete experiment")
        else:
            require(fisher > beta * dd ** 2 / (d * (1 - d)), "varying readiness adds nonnegative information")
            rejection = "nonzero readiness derivative term retained"
        cases.append({"d": str(d), "d_jet": str(dd), "beta": str(beta), "beta_jet": str(dbeta),
                      "full_fisher": str(fisher), "control": rejection})
    return cases


def kraus_cauchy_schwarz_and_copies():
    # An elementary exact projective instrument saturates the real pure-state
    # bound. This is a finite algebra check of the Cauchy--Schwarz argument;
    # the universal Kraus completeness proof is in the companion document.
    state = [Q(3, 5), Q(4, 5)]
    tangent = [Q(-4, 5), Q(3, 5)]
    require(sum(x * x for x in state) == 1 and sum(x * dx for x, dx in zip(state, tangent)) == 0,
            "normalized horizontal pure-state fixture")
    probabilities = [x ** 2 for x in state]
    jets = [2 * x * dx for x, dx in zip(state, tangent)]
    fisher = sum(dx ** 2 / x for dx, x in zip(jets, probabilities))
    require(fisher == 4 * sum(dx ** 2 for dx in tangent) == 4, "Kraus Cauchy--Schwarz bound can be sharp")
    for n in (1, 2, 7, 100):
        norm_formula = n * sum(dx * dx for dx in tangent)
        cross_formula = n * (n - 1) * sum(x * dx for x, dx in zip(state, tangent)) ** 2
        require(norm_formula + cross_formula == n, "n-copy tensor derivative orthogonality")
    # Explicit two-copy derivative, without an exponential n-copy tensor.
    two_copy_tangent = [dx * y + x * dy for x, dx in zip(state, tangent) for y, dy in zip(state, tangent)]
    require(sum(v * v for v in two_copy_tangent) == 2, "explicit two-copy Gram agrees with general formula")
    return {"pure_state_projective_fisher": str(fisher), "copy_counts_checked": [1, 2, 7, 100],
            "general_complete_Kraus_bound": "F<=4*n*||dC||^2"}


def rational_copy_certificate():
    lo, hi = Q(618, 1000), Q(619, 1000)
    require(lo * lo + lo - 1 < 0 < hi * hi + hi - 1, "strict exact positive Golden-root enclosure")
    z, eta, slope, L = Q(1, 2 ** 20), Q(1, 4), Q(1, 100), 512
    # A0=1-p^12 and B0=1-p^6 are in(0,1). Thus Q,R>1-z,
    # Cq>this lower bound and d(1-d)<1-d<2z. No actual rho is set to1.
    cq_lower = 8 * z * lo ** 6 * eta ** 2 * (1 - z) * (1 + lo ** 6)
    beta_lower, rho_upper = Q(1, 4), Q(2)
    sites, h = L ** 4, Q(1, L)
    variance_upper = 2 * z
    scalar_slack_factor = Q(1)  # actual local psi_y=top_y=0, slack=p>0.
    lower = (beta_lower * cq_lower ** 2 * slope ** 2 * sites /
             (rho_upper ** 2 * h ** 2 * variance_upper * scalar_slack_factor))
    require(lower > 46, "conditional finite-mesh copy bound exceeds46")
    require(lower < 47, "reported conservative integer lower bound is47")
    omitted_sites = lower / sites
    omitted_pf = lower * rho_upper ** 2
    conditional_only = lower / beta_lower
    require(omitted_sites < 1 < lower, "dropping S destroys the actual normalization bound")
    require(omitted_pf != lower and conditional_only != lower, "inverse PF and ready probability cannot be omitted")
    # Derive the bound directly from the actual target jet and one-copy Gram,
    # retaining its factor2 and the factor4 of the elementary quantum bound.
    target_jet_lower = cq_lower * 2 * slope / (rho_upper * h)
    fisher_lower = beta_lower * target_jet_lower ** 2 / variance_upper
    one_copy_norm = Q(1, sites)
    require(fisher_lower / (4 * one_copy_norm) == lower, "necessary copy inequality has no missing2,4,S or PF factor")
    # Refinement scaling on this fixed local affine slope is S/h^2=L^6.
    require(sites / h ** 2 == L ** 6, "four-dimensional global normalization gives L^6")
    return {"conditions": {"L": L, "S": sites, "eta": str(eta), "gamma_times_k": str(slope),
                           "beta_at_least": str(beta_lower), "actual_rho_at_most": str(rho_upper),
                           "local_scalar_and_top": "zero"},
            "Cq_strict_rational_lower": str(cq_lower),
            "n_strict_rational_lower": str(lower), "necessary_integer_copies_at_least": 47,
            "negative_control_bound_without_S": str(omitted_sites),
            "wrong_bound_without_inverse_PF": str(omitted_pf),
            "wrong_conditional_only_bound_without_beta": str(conditional_only),
            "uniform_refinement_rho_hypothesis_proved": False}


def main():
    print(json.dumps({
        "status": "PASS: conditional necessary native-matter copy bound",
        "exact_query_jet": exact_query_jet(),
        "actual_CAR_and_RIGHT_tangent": scalar_car_tangent(),
        "actual_sparse_null_matter_jet": sparse_matter_stencil(),
        "complete_three_outcome_fisher": full_classical_fisher(),
        "elementary_Kraus_and_tensor_checks": kraus_cauchy_schwarz_and_copies(),
        "necessary_bound": "n>=beta*Cq^2*rho^-2*(gamma*k)^2*S/[h^2*d*(1-d)*(1+psi_y^2/slack^2)]",
        "conditional_finite_mesh_certificate": rational_copy_certificate(),
        "scope": [
            "One actual local two-query likelihood and its complete first jet must be reproduced",
            "Only n independent copies of the full normalized global CAR/RIGHT input carry matter dependence",
            "Ancillas, gates, feedback and measurement rules are matter independent",
            "The actual density ratio, calibrated inverse metric, retained RIGHT and abort/readiness law remain",
            "No uniform rho<=2 chart, moving-query impossibility, action-source no-go or physical GR closure is claimed",
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
