#!/usr/bin/env python3
"""Research-grade exact rational controls for the closed DATA source resolvent.

This is a two-outcome, strictly CPTP *diagonal/measure-and-prepare* channel.
It tests a generic theorem at full rational precision. IT DOES NOT REPLAY THE
ORIGINAL CAR16/128/256 fixture and does not license physical GR promotion.
Run: python3 02_REGISTRY/research/certificates/a4d_closed_history_intrinsic_source_test.py
"""
from fractions import Fraction as Q
import json


def require(truth, description):
    if not truth:
        raise AssertionError(description)


def probability_matrix(t):
    a = Q(1, 4) + t / 8
    b = Q(1, 2) - t / 8
    require(0 < a < 1 and 0 < b < 1, "genuine nondegenerate native test")
    return ((1 - a, b), (a, 1 - b))


def mv(P, x):
    return (
        P[0][0] * x[0] + P[0][1] * x[1],
        P[1][0] * x[0] + P[1][1] * x[1],
    )


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def norm1(x):
    return sum((abs(z) for z in x), Q(0))


def stationary(t):
    a = Q(1, 4) + t / 8
    b = Q(1, 2) - t / 8
    return (b / (a + b), a / (a + b))


def main():
    checks = 0

    def check(cond, name):
        nonlocal checks
        checks += 1
        require(cond, name)

    P0 = probability_matrix(Q(0))
    rho0 = stationary(Q(0))
    dr = (Q(-1, 6), Q(1, 6))
    dp_rho0 = (Q(-1, 8), Q(1, 8))

    check(all(sum(P0[i][j] for i in range(2)) == 1 for j in range(2)),
          "two column-stochastic original channels")
    check(mv(P0, rho0) == rho0 and rho0 == (Q(2, 3), Q(1, 3)),
          "canonical exact stationary state at original fixture")
    check(sub(dr, mv(P0, dr)) == dp_rho0,
          "fixed-point first-source resolvent exact equation")
    check(norm1(dr) == Q(1, 3), "exact moving-DATA source trace norm")

    for t in [Q(-1, 4), Q(1, 4), Q(1, 8)]:
        P1 = probability_matrix(t)
        r1 = stationary(t)
        lhs = sub(sub(r1, rho0), mv(P1, sub(r1, rho0)))
        rhs = sub(mv(P1, rho0), mv(P0, rho0))
        check(lhs == rhs, "exact two-native-execution resolvent")
        check(mv(P1, r1) == r1, "no external stationary-state preparation")
        check(all(P1[i][j] > 0 for i in range(2) for j in range(2)),
              "strict finite Choi positivity")

    # One-tick measure/prepare quantum extension:
    # K_ij=sqrt(P_ij)|i><j|, J has diagonal eigenvalues P_ij.
    # Four selected actual K_ij span M2; det(V)^2 is their product.
    choi_diag = [P0[i][j] for i in range(2) for j in range(2)]
    det_squared = Q(1)
    for x in choi_diag:
        det_squared *= x
    delta_exact = min(choi_diag)
    delta_lower = det_squared / (2 ** (2 ** 2 - 1))
    check(det_squared == Q(3, 64), "selected four actual Choi directions determinant^2")
    check(delta_exact == Q(1, 4), "true Choi strict positive gap")
    check(delta_lower == Q(3, 512) and 0 < delta_lower <= delta_exact,
          "explicit lower-bound determinant formula")
    check(sum(choi_diag) == 2, "full unnormalized quantum Choi trace")

    # Neumann expansion for the exact first source. The true CPTP contraction
    # from the Choi lower gap is c=1-2*delta; the exact diagonal decay is 1/4.
    c = 1 - 2 * delta_exact
    check(c == Q(1, 2), "derived quantum Doeblin coefficient")
    approximation = (Q(0), Q(0))
    term = dp_rho0
    rows = []
    for M in range(1, 9):
        approximation = add(approximation, term)
        term = mv(P0, term)
        remainder = sub(dr, approximation)
        bound = c ** M * norm1(dp_rho0) / (1 - c)
        check(norm1(remainder) <= bound,
              "native preparation-source truncation with actual Choi contraction")
        rows.append({"M": M, "actual_remainder": str(norm1(remainder)),
                     "certified_upper": str(bound)})

    # Complete price: B(t,rho)=t^2+(t+3)*rho_1. At t=0 the explicit-field
    # part contributes 1/3; the *endogenous* stationary preparation contributes
    # 3*(d rho_1/dt)=1/2. Freezing rho therefore fails the full source.
    frozen_state_source = rho0[1]
    moving_state_source = 3 * dr[1]
    total_source = frozen_state_source + moving_state_source
    check((frozen_state_source, moving_state_source, total_source) ==
          (Q(1, 3), Q(1, 2), Q(5, 6)),
          "independent DATA source is nonzero and necessary")

    # Negative control: the identity channel is a closed CPTP dynamics too,
    # but it has at least two different fixed states and Choi rank one.
    identity = ((Q(1), Q(0)), (Q(0), Q(1)))
    check(mv(identity, (Q(1), Q(0))) == (Q(1), Q(0)) and
          mv(identity, (Q(0), Q(1))) == (Q(0), Q(1)),
          "closedness ALONE does not select a unique stationary state")
    check(identity != P0, "negative control genuinely changes the dynamics")

    # C13-C19: the exact ORIGINAL all128 zero-marker formula has a
    # unital recycling T(I)=I. Here test its algebra on a rational
    # two-level DIAGONAL sector; it is NOT an original CAR16 replay.
    # D=diag(sqrt(x),sqrt(y)), Delta=diag(x,y), T swaps entries.
    # The resulting diagonal transition really is stochastic:
    # q_0 -> q_0 + eps*(y*q_1-x*q_0).
    x = Q(4)
    y = Q(9)
    epsilon = Q(1, 100)
    z_inv = 1 / x + 1 / y
    canonical = ((1 / x) / z_inv, (1 / y) / z_inv)
    check(z_inv == Q(13, 36) and canonical == (Q(9, 13), Q(4, 13)),
          "original-form inverse-Delta trace stationary density")
    P_recycling = ((1 - epsilon * x, epsilon * y),
                   (epsilon * x, 1 - epsilon * y))
    check(mv(P_recycling, canonical) == canonical,
          "C13 + unital recycling fixes inverse-Delta state EXACTLY")
    check(x * canonical[0] + y * canonical[1] == 2 / z_inv == Q(72, 13),
          "complete stationary first port mean moment d/Tr Delta^-1")
    # The original mean formula is n + n*p*eps*(2/Z), with p a fixed
    # Golden algebraic symbol; the coefficient of p is exactly rational.
    n = 3
    expected_port_mean_p_coefficient = n * epsilon * Q(2) / z_inv
    check(expected_port_mean_p_coefficient == Q(54, 325),
          "arbitrary-horizon actual paid port mean coefficient")
    for xx in [Q(7, 2), x, Q(9, 2)]:
        zz = 1 / xx + 1 / y
        rr = ((1 / xx) / zz, (1 / y) / zz)
        PP = ((1 - epsilon * xx, epsilon * y),
              (epsilon * xx, 1 - epsilon * y))
        check(mv(PP, rr) == rr and xx * rr[0] + y * rr[1] == 2 / zz,
              "stationary mean across three genuine finite alternatives")
    # Differentiate x -> 2/(1/x+1/y). Full source vs incorrectly
    # frozen preparation: the missing internal source is 45/169.
    complete_source = Q(2) / (x * x * z_inv * z_inv)
    frozen_prep_source = canonical[0]
    endogenous_source = complete_source - frozen_prep_source
    check((complete_source, frozen_prep_source, endogenous_source) ==
          (Q(162, 169), Q(9, 13), Q(45, 169)),
          "exact C18 moving canonical density source and hostile frozen control")

    print(json.dumps({
        "status": "PASS",
        "exact_checks": checks,
        "test": "two-outcome diagonal CPTP / internal record, NOT original CAR16",
        "rho_star": [str(x) for x in rho0],
        "full_source": str(total_source),
        "frozen_preparation_source": str(frozen_state_source),
        "endogenous_preparation_term": str(moving_state_source),
        "selected_choi_det_squared": str(det_squared),
        "delta_exact": str(delta_exact),
        "delta_det_lower": str(delta_lower),
        "contraction_c": str(c),
        "truncation": rows,
        "same_native_form_toy": {
            "inverse_trace_Z": str(z_inv),
            "stationary_marginal": [str(t) for t in canonical],
            "paid_port_mean_p_coefficient_at_n3": str(expected_port_mean_p_coefficient),
            "full_port_source_coefficient": str(complete_source),
            "frozen_source_coefficient": str(frozen_prep_source),
            "endogenous_source_correction": str(endogenous_source)
        },
        "new_physical_GR_claim": False
    }, indent=2))


if __name__ == "__main__":
    main()
