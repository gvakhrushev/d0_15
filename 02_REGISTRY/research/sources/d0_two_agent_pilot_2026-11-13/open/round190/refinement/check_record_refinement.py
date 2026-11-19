"""Check one fixed native dephased-record refinement of the A89 source."""

from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys

PILOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PILOT / "direct/round80/price"))
sys.path.insert(0, str(PILOT / "direct/round89/assembly"))
sys.path.insert(0, str(PILOT / "open/round181"))

import check_amplitude_price as source
from check_fixed_positive_reader import a, cx, nc1, ne, one, p, power, require, with_births
from check_parity_price import action

PHASE, REPORT, PORT = 0, 1, 2
SPIN = (3, 4)
PARITY, HEAD, TAIL, RECORD = 5, 6, 7, 8
WIDTH = 9


def swap(first, second):
    return (cx(first, second), cx(second, first), cx(first, second))


def word():
    turn = ne.Gate("G", (PORT,))
    source_i = ne.Gate("SourceI", (PORT, *SPIN))
    z = (source_i, source_i)
    inverse = z + (turn,) + z
    clear_parity = swap(PARITY, PORT) + inverse + swap(PARITY, PORT)
    clear_record = swap(RECORD, PORT) + inverse + swap(RECORD, PORT)
    copy_parity = (cx(PHASE, PARITY), cx(REPORT, PARITY))
    c = (cx(PARITY, PORT),)
    controlled = (turn,)*3 + z + (turn,)*2 + z + c + (turn,)*2 + c
    return (
        clear_parity + clear_record + copy_parity
        + swap(HEAD, PORT) + controlled + swap(HEAD, PORT)
        + copy_parity[::-1] + nc1(HEAD, TAIL) + (cx(HEAD, RECORD),)
    )


def bit(index, wire):
    return (index >> (WIDTH - 1 - wire)) & 1


def test_native_word():
    gates = word()
    execution = ne.Execution(
        WIDTH, (), (), gates, profile=ne.G_CX_SOURCE_I,
        source_port=PORT, source_spin=SPIN, report_bits=(RECORD,),
    )
    ne.execution_from_json(ne.canonical_json(execution), max_qubits=WIDTH, max_expanded_stages=49)
    inventory = Counter(gate.op for gate in gates)
    require(inventory == {"G": 10, "CX": 27, "SourceI": 12}, "Unexpected native inventory")

    cosine = 9*one - 16*p
    sine = (8*one - 12*p)*a
    require(cosine*cosine + sine*sine == one, "Wrong exact G^4 polynomial")
    tail_zero = (p - p*p, 2*a*p)
    require(sum(x*x for x in tail_zero) == one, "Wrong NC1 zero tail")

    for old in range(32):
        state = with_births({old: one}, 4)
        for gate in gates:
            state = action(state, gate, WIDTH)
        base = old << 4
        # The parity flag is returned to zero. The physical tail for report 1
        # is exactly zero, and the fresh record is the actual orthogonal copy.
        record_zero = one if bit(base, PHASE) != bit(base, REPORT) else cosine
        expected = {
            base | (tail << 1): record_zero*coefficient
            for tail, coefficient in enumerate(tail_zero)
        }
        if bit(base, PHASE) == bit(base, REPORT):
            expected[base | 5] = sine
        require(state == expected, f"Native refinement mismatch on old column {old}")

    return {
        "old_columns_including_dirty_port_and_spin": 32,
        "fresh_Golden_births": 4,
        "actual_NC1_record": 1,
        "native_stages_excluding_births_and_readout": len(gates),
        "gate_inventory": dict(inventory),
        "G4_cos_coefficients_in_Qa": cosine.coefficients,
        "G4_sin_coefficients_in_Qa": sine.coefficients,
        "orthogonal_dilation_on_all_old_columns": True,
    }


def test_exact_sign_and_static_projection():
    # The second actual NC1 is called only on the first outcome 1.
    nc1_masses = {0: one*0, 1: one*0}
    state = with_births({0: one}, 2)
    for gate in nc1(0, 1):
        state = action(state, gate, 2)
    require(3 not in state, "The physical Golden NC1 dark outcome must be absent")
    for index, amplitude in state.items():
        nc1_masses[index >> 1] += amplitude*amplitude
    require(nc1_masses == {0: p, 1: p*p}, "Wrong physical Golden NC1 outcome masses")

    p_lo, p_hi, a_lo = Fraction(618, 1000), Fraction(619, 1000), Fraction(786, 1000)
    polynomial = lambda t: t*t+t-1
    require(polynomial(p_lo) < 0 < polynomial(p_hi) and a_lo*a_lo < p_lo,
            "Bad algebraic enclosure of p and a")
    require(9-16*p_lo < 0 and 8-12*p_hi > 0, "Bad signs for the G^4 sine/cosine")
    a_c_lower = a_lo*(16*p_lo-9)+20*p_lo-12
    require(a_c_lower > 1, "The fine cosine multiplier does not reverse the A89 sign")
    require(p+p*p == one and p+power(p, 3)+power(p, 4) == one,
            "Static three-leaf law is not normalized")
    require(power(p, 3)+power(p, 4) == p*p, "Wrong coarse Born probability")
    require(a*a == p and power(a*p, 2) == power(p, 3), "Wrong static fine amplitudes")
    require(p*(a+p)-a == p*p*(one-a), "Wrong static MDL-order reversal certificate")

    mp = source.mp
    pp, aa = source.p, mp.sqrt(source.p)
    coarse = (pp, pp**2)
    pushed = (aa, pp*(aa+pp))
    wrong = pushed[1]**2/sum(y*y for y in pushed)
    require(coarse[0] > coarse[1] and pushed[0] < pushed[1],
            "The naive positive pushforward must reverse the static Born ordering")
    return {
        "exact_lower_bound_a_times_refinement_factor": str(a_c_lower),
        "static_fine_Born_masses": ["p", "p^3", "p^4"],
        "static_coarse_Born_masses": ["p", "p^2"],
        "static_linearly_pushed_amplitude_weights": ["sqrt(p)", "p(sqrt(p)+p)"],
        "static_candidate_coarse_Born_probability_of_second_branch": mp.nstr(wrong, 17),
        "static_correct_Born_probability_of_second_branch": mp.nstr(coarse[1], 17),
        "static_positive_pushforward_reverses_MDL_order": True,
    }


def test_A89():
    mp, theta, tau = source.mp, source.theta, source.pulse
    pp, aa = source.p, mp.sqrt(source.p)
    r = ((9 - 16*pp)**2, ((8 - 12*pp)*aa)**2)
    source.almost(sum(r), 1)
    c4 = sum(map(mp.sqrt, r))
    require(c4*aa > 1 and 0 < source.q[0] < source.q[1] < 1,
            "A89 must have two ordered material clicks and an actual sign reversal")
    require(0 < tau < min(theta, mp.pi/2-theta), "A89 phase leaves its original quadrant")

    def projection(xs, ready, failures):
        coarse, refined = list(failures), list(failures)
        for root in ready:
            for j, route, m, phase, outcome in product(range(2),repeat=5):
                q_m = source.q[j] if m else 1-source.q[j]
                angle = theta + (-1)**(route^m)*xs[j^route] + phase*mp.pi/2
                q_b = mp.sin(angle)**2 if outcome else mp.cos(angle)**2
                mass = root*q_m*q_b/8
                coarse.append(mass)
                children = tuple(mass*y for y in r) if phase == outcome else (mass, mp.mpf(0))
                source.almost(sum(children), mass)
                refined.extend(children)
        owner_law = source.law(xs, ready, failures)
        require(len(coarse) == len(owner_law), "The A89 coarse law lost an original leaf")
        for actual, expected in zip(coarse, owner_law):
            source.almost(actual, expected)
        source.almost(sum(coarse), 1)
        source.almost(sum(refined), 1)
        return sum(map(mp.sqrt,coarse)), sum(map(mp.sqrt,refined))

    prices = []
    examples = [
        ([mp.mpf(1)/3], [mp.mpf(2)/3]),
        ([mp.mpf(1)/9, mp.mpf(2)/9], [mp.mpf(1)/2, mp.mpf(1)/6]),
    ]
    for ready, failures in examples:
        result = []
        for site in range(2):
            operands = []
            for sign in (1, -1):
                xs = [0,0]
                xs[site] = sign*tau
                operands.append(projection(xs, ready, failures))
            result.append(tuple(mp.log(minus/plus)/source.ell
                                for plus, minus in zip(*operands)))
        source.almost(result[0][0], -result[1][0])
        source.almost(result[0][1], -result[1][1])
        require(result[0][0] < 0 < result[1][0] and result[1][1] < 0 < result[0][1],
                "The actual fine split must reverse both A89 signs")
        prices.append({
            "coarse_price_differences": [mp.nstr(row[0], 17) for row in result],
            "fine_price_differences": [mp.nstr(row[1], 17) for row in result],
        })

    return {
        "original_A89_factory_examples": prices,
        "conditional_cosine_square_root_multiplier": mp.nstr(c4,17),
        "all_coarse_masses_and_early_stops_preserved": True,
        "two_fine_amplitude_signs_reversed": True,
    }


def main():
    print(json.dumps({
        "native_suffix": test_native_word(),
        "static_projection": test_exact_sign_and_static_projection(),
        "A89": test_A89(),
        "physical_tariff_or_Info_selected": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
