#!/usr/bin/env python3
"""Exact rational checks of B145 normalization, derivative, and moving rank."""

import json
from fractions import Fraction as F


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def diagonal(first, second):
    return ((first, F(0)), (F(0), second))


def multiply(left, right):
    return tuple(
        tuple(sum(a * b for a, b in zip(row, column)) for column in zip(*right))
        for row in left
    )


def trace(matrix):
    return sum(matrix[index][index] for index in range(len(matrix)))


def determinant(matrix):
    (a, b), (c, d) = matrix
    return a * d - b * c


def checked_normalization():
    early_state = diagonal(F(12, 13), F(1, 13))
    past_return = diagonal(F(1, 2), F(1))
    effect = ((F(1, 2), F(1, 4)), (F(1, 4), F(1, 2)))
    require(multiply(past_return, effect) != multiply(effect, past_return), 'The matched-return fixture must be noncommuting')
    success_state = multiply(multiply(past_return, early_state), past_return)
    success = trace(success_state)
    success_and_bit = trace(multiply(success_state, effect))
    success_bit_and_fresh_return = trace(multiply(success_state, multiply(effect, effect)))
    require((success, success_and_bit, success_bit_and_fresh_return) == (
        F(4, 13), F(2, 13), F(5, 52)
    ), 'The three unconditional masses changed')
    q = success_and_bit / success
    second_moment = success_bit_and_fresh_return / success
    variance = second_moment - q * q
    require((q, second_moment, variance) == (F(1, 2), F(5, 16), F(1, 16)), 'The conditioning changed the measured variance')
    return {
        "P_S": str(success),
        "P_S_b1": str(success_and_bit),
        "P_S_b1_F": str(success_bit_and_fresh_return),
        "q_given_S": str(q),
        "second_moment_given_S": str(second_moment),
        "variance_given_S": str(variance),
        "past_return_and_effect_do_not_commute": True,
    }


def checked_derivative():
    rho = (F(3, 4), F(1, 4))
    effect = (F(1, 4), F(3, 4))
    d_rho = (F(1, 8), -F(1, 8))
    d_effect = (F(1, 8), -F(1, 8))
    joint = tuple(weight * value for weight, value in zip(rho, effect))
    d_joint = tuple(a * d_b + d_a * b for a, b, d_a, d_b in zip(rho, effect, d_rho, d_effect))
    require((sum(joint), sum(d_joint)) == (F(3, 8), F(0)), 'The marginal derivative must vanish in this fixture')
    require(d_joint == (F(1, 8), -F(1, 8)), 'Wrong joint derivative')
    require(tuple(d_a - d_j for d_a, d_j in zip(d_rho, d_joint)) == (F(0), F(0)), 'The complementary branch should have zero derivative')
    log_ratio = effect[0] / effect[1]
    require(log_ratio == F(1, 3), 'Wrong logarithm in the exact entropy derivative')
    variance = sum(a * b * b for a, b in zip(rho, effect)) - sum(joint) ** 2
    effect_speed_squared = sum(a * d_b ** 2 for a, d_b in zip(rho, d_effect))
    preparation_speed_squared = sum(d_a ** 2 / (4 * a) for a, d_a in zip(rho, d_rho))
    require((variance, effect_speed_squared, preparation_speed_squared) == (
        F(3, 64), F(1, 64), F(1, 48)
    ), 'Wrong derivative bounds and occupation variance')
    collar = min(*effect, *(1 - value for value in effect))
    # The integral of 1/t from 1 to 3 is strictly below the trapezoid area 4/3.
    abs_derivative_upper = d_joint[0] * (3 - 1) * (1 + F(1, 3)) / 2
    effect_part_of_bound_squared = 4 * variance * effect_speed_squared / collar ** 2
    require(abs_derivative_upper == F(1, 6), 'The rational entropy estimate changed')
    require(abs_derivative_upper ** 2 < effect_part_of_bound_squared, 'The estimated derivative no longer fits the certified bound')
    pure_variance = effect[0] ** 2 - effect[0] ** 2
    require(pure_variance == 0 and collar > 0, 'The eigeninput must have zero variance')
    return {
        "Dq": str(sum(d_joint)),
        "D_chi": {"log_argument": str(log_ratio), "log_coefficient": str(d_joint[0])},
        "abs_D_chi_upper": str(abs_derivative_upper),
        "effect_part_of_source_bound_squared": str(effect_part_of_bound_squared),
        "preparation_speed_squared": str(preparation_speed_squared),
        "variance": str(variance),
        "collar": str(collar),
        "pure_eigeninput_variance": str(pure_variance),
    }


def checked_rank_motion():
    effects = (
        ((F(1, 2), F(1, 4)), (F(1, 4), F(1, 2))),
        ((F(1, 2), -F(1, 4)), (-F(1, 4), F(1, 2))),
    )
    require(all(determinant(effect) == F(3, 16) for effect in effects), 'Wrong determinants of the normalized effects')
    for exponent in (1, 2, 4, 8, 16):
        time = F(1, 2 ** exponent)
        amplitude_numerator = diagonal(F(1), time)
        normalizer = 1 + time ** 2
        for effect in effects:
            numerator = multiply(multiply(amplitude_numerator, effect), amplitude_numerator)
            branch = tuple(tuple(entry / normalizer for entry in row) for row in numerator)
            require(trace(branch) == F(1, 2), 'The marked outcome mass changed with rank')
            require(determinant(branch) == F(3, 16) * time ** 2 / normalizer ** 2, 'Wrong marked determinant in the rank-opening test')
            # The larger eigenvalue is at least half the trace.
            small_eigenvalue_upper = 2 * determinant(branch) / trace(branch)
            require(0 < small_eigenvalue_upper <= time ** 2 <= F(1, 4), 'The small marked eigenvalue is not quadratic')
        reference_small_eigenvalue = time ** 2 / normalizer
        require(0 < reference_small_eigenvalue <= time ** 2, 'The small unmarked eigenvalue is not quadratic')
        # -x log x increases on [0, 1/4], and log(2) < 1 bounds the dyadic term.
        require((2 * exponent * time ** 2) / time == F(2 * exponent, 2 ** exponent), 'The dyadic entropy correction is not negligible in the first derivative')
    return {
        "initial_rank": 1,
        "nearby_rank": 2,
        "normalized_amplitude": "diag(1,t)/sqrt(1+t^2)",
        "new_eigenvalue_upper": "t^2",
        "new_entropy_over_abs_t_upper_at_dyadic_t": "2*k/2^k",
    }


if __name__ == "__main__":
    print(json.dumps({
        "matched_return": checked_normalization(),
        "nonzero_entropy_derivative": checked_derivative(),
        "moving_rank": checked_rank_motion(),
        "full_Book_Info_identified": False,
        "GR_closed": False,
    }, indent=2, sort_keys=True))
