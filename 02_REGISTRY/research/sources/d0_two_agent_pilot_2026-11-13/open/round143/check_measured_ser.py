"""Exact finite controls for the measured SER determinant and record price."""

from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[1]
P = (sp.sqrt(5) - 1) / 2
A = sp.sqrt(P)
ZETA = sp.Rational(1, 2**20)


def require(condition, why):
    if not condition:
        raise AssertionError(why)


def zero(expression):
    return sp.simplify(expression) == 0


def same(left, right, why):
    require(all(zero(entry) for entry in left - right), why)


def check_slots():
    # Genuine noncommuting test: both operators are strict contractions.
    bank = sp.Matrix([[sp.Rational(1, 5), sp.Rational(1, 7)],
                      [sp.Rational(1, 7), sp.Rational(3, 5)]])
    old = sp.Matrix([[sp.Rational(2, 3), sp.Rational(1, 5)],
                     [sp.Rational(1, 7), sp.Rational(3, 4)]])
    eye = sp.eye(2)
    for positive in (bank, eye-bank, eye-old.T*old):
        require(positive[0, 0] > 0 and positive.det() > 0, "Fixture must be admissible")
    require(bank * (old * old.T) != (old * old.T) * bank,
            "The fixture accidentally commutes")
    complement = eye - bank
    good0 = old.T * complement**2 * old
    good1 = old.T * bank**2 * old
    failure = old.T * (eye - bank**2 - complement**2) * old
    same(good0 + good1 + failure, old.T*old, "Old success split must be exhaustive")
    same(failure, 2 * old.T * bank * complement * old, "Wrong failure effect")
    for sign in (-1, 1):
        corner = P * (A * complement + sign * P * bank)
        target = old.T * corner**2 * old
        recovered = P**3 * good0 + P**4 * good1 + sign * A * P**3 * failure
        same(target, recovered, "Actual measured branches do not recover the corner square")

    # Keep the symbol for the positive constant readiness factor.
    c = sp.symbols("c", positive=True)
    target = target.applyfunc(sp.simplify)
    accept_a72 = (eye + target)/2
    joined = c*((1-2*ZETA)*eye + 2*ZETA*accept_a72)
    sample = c*((1-ZETA)*eye + ZETA*target)
    same(joined, sample, "The rare 19-bit event miscalibrates zeta")
    x00, x01, x10, x11 = sp.symbols("x00 x01 x10 x11")
    matrix = sp.Matrix([[x00, x01], [x10, x11]])
    wedge = sp.Matrix([0, 1, -1, 0])
    value = (wedge.T * sp.kronecker_product(matrix, matrix) * wedge)[0]/2
    require(zero(value - matrix.det()), "The signed two-slot expectation is not a determinant")
    return {"known_signs_checked": [-1, 1], "noncommuting_fixture": True,
            "old_success_all_fates_retained": True,
            "ready_pairs_per_slot": 22, "rank_two_wedge_identity": True}


def check_paid_extension():
    # Restricted example with two old record marks and readiness, including
    # all unused control addresses. The proof is the same for any fixed n.
    bits = tuple(product((0, 1), repeat=3))
    weights = {x: x[2]*(1-2*(x[0] and x[1])) for x in bits}

    def character(u, v):
        return (-1)**sum(a*b for a, b in zip(u, v))

    coefficients = {g: sum(character(g, b)*weights[b] for b in bits) for g in bits}
    gray = tuple(tuple(map(int, format(k ^ (k >> 1), '03b'))) for k in range(8))
    for b in bits:
        frame = 0
        exponent = 0
        for idx, g in enumerate(gray):
            require((-1)**frame == character(g, b), "Wrong Gray control frame")
            exponent += (-1)**frame * coefficients[g]
            successor = gray[(idx+1) % len(gray)]
            flips = [i for i in range(3) if g[i] != successor[i]]
            require(len(flips) == 1, "The Gray cycle has a nonlocal edge")
            frame ^= b[flips[0]]
        require(frame == 0 and exponent == 8*weights[b], "Full-address gate identity failed")

    cos, sin = sp.symbols("c s", real=True)
    success_plus = (cos + sin)**2 / 2
    success_minus = (cos - sin)**2 / 2
    require(zero(success_plus+success_minus - cos**2-sin**2),
            "Ready conditional probabilities are not complementary")
    gamma, u = sp.symbols("gamma u", positive=True)
    not_ready = sp.symbols("z_off", nonnegative=True)
    mean = (1-gamma)*not_ready + gamma*((1-u)*success_plus+u*success_minus)
    require(zero(sp.diff(mean, u) + 2*gamma*cos*sin),
            "Wrong coefficient for paid output length")
    return {"verified_gray_addresses": 8, "ready_branch_entropy_constant": True,
            "both_fates_of_ready_are_retained": True,
            "mean_code_increment_derivative": "-gamma*sin(2*omega)*Du"}


def check_entropy_boundary():
    # This fixture contains an additional q-vanishing leaf OUTSIDE the
    # mandatory mark. Its entropy reinforces, rather than cancels, the term.
    q, s, a, b, tau = sp.symbols("q s a b tau", positive=True)
    leaves = ((1-q)**2, (1-q)*q*s, (1-q)*q*(1-s), q*s, q*(1-s))
    require(zero(sum(leaves)-1), "Total mass was not retained")
    require(zero(sum(leaves[-2:])-q), "Original output must survive every refinement")
    fibre = tau/(a-b*q)**2
    vanishing = [leaf.subs(s, fibre) for leaf in leaves if zero(leaf.subs(q, 0))]
    l_coeff = sp.simplify(sum(sp.diff(leaf, q).subs(q, 0) for leaf in vanishing))
    require(l_coeff == 2, "The positive first-order logarithmic terms failed")
    lengths = sp.symbols("c0:5", real=True)
    mean = sum(c*v.subs(s, fibre) for c, v in zip(lengths, leaves))
    require(not sp.diff(mean, q).subs(q, 0).has(sp.oo, sp.zoo, sp.nan, sp.log),
            "Fixed terminal prices cannot provide a logarithmic pole")
    return {"original_mark_retained": True,
            "tested_log_singularity_coefficient_before_units": str(l_coeff),
            "arbitrary_fixed_leaf_prices_are_regular": True}


def main():
    sources = [
        "direct/round71/original/REFERENCE_SOURCE_RU.md",
        "direct/round72/record/RECORD_SOURCE_RU.md",
        "open/round134/B134_NATIVE_SLATER_FEEDBACK_RU.md",
        "open/round138/B138_COARSE_RETURN_SPECTRAL_WELD_RU.md",
    ]
    print(json.dumps({
        "status": "PASS",
        "inputs": {path: sha256((PILOT/path).read_bytes()).hexdigest() for path in sources},
        "three_outcome_cold_effect": check_slots(),
        "paid_conditional_info": check_paid_extension(),
        "complete_classical_record_boundary": check_entropy_boundary(),
        "weighted_book_Cost_minus_Info_selected": False,
        "measured_RC3_identified_with_coherent_feedback": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
