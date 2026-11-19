"""Replay A82 defect columns, the four physical W3 blocks, and the thermal sign bound."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import runpy


SOURCES = Path("02_REGISTRY/research/sources")
PILOT = SOURCES / "d0_two_agent_pilot_2026-11-13"
PINS = {
    PILOT / "direct/round82/device/check_prepaid_report.py": "d7bb38033ccfade7f29b76195928b18ec507c82cc633ab7e3e67f6d1a57bc99f",
    PILOT / "direct/round82/assembly/REUSED_BIT_RU.md": "d3a3d58e7eb85a956ac20489c28ee6b8c3d18f5da3163d0875829ac6f9e78188",
    PILOT / "open/round169/B169_TERMINAL_GIBBS_BORN_RU.md": "b299d1fa7544ccb37897458458f317b6cd741a9403b0a19ede55c3f2a9a0fe13",
    SOURCES / "d0_native_terminal_code_writer_2026-10-25/WRITER_PROOF.md": "9c513067559c9cd89ac4c911d01a21e06c9b4d2cd962d5d568b51459ae3d0866",
    SOURCES / "d0_native_execution_domain_2026-10-24/native_execution.py": "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c",
}


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def power(value, exponent, one):
    out = one
    for _ in range(exponent):
        out = out * value
    return out


def apply_word(owner, state, word, width):
    apply = owner["action"]
    for gate in word:
        state = apply(state, gate, width)
    return state


def projected(state, mark):
    return {basis // 4: amplitude for basis, amplitude in state.items() if basis % 4 == mark}


def verify_detector(owner):
    word = owner["word"](3)
    require(Counter(gate.op for gate in word) == {"CX": 100, "SourceI": 56, "G": 38}, "literal detector inventory")
    c, s = owner["rot"](12)
    a, p = owner["a"], owner["p"]
    require(c.coefficients == (46921, 0, -75920, 0), "exact cosine")
    require(s.coefficients == (0, 36888, 0, -59684), "exact sine")
    for old in range(32):
        # Actual second-born defect v_perp, with the first pointer supplied
        # in the basis value carried by the terminal mark under passive pullback.
        zero = apply_word(owner, {4*old: -p, 4*old + 1: a}, word, 7)
        one = apply_word(owner, {4*old + 2: -p, 4*old + 3: a}, word, 7)
        if old % 4 == 3:
            require(projected(zero, 0) == {}, "00 kills the defect in P")
            require(projected(one, 2) == {}, "10 kills the defect in P")
        else:
            require(projected(zero, 0) == {old: -a*s}, "00 defect is -sqrt(p) sin(12theta) in Q")
            require(projected(zero, 1) == {old: a*c}, "01 defect is sqrt(p) cos(12theta) in Q")
    return len(word), c, s


def writer_words(owner, index, head):
    native = owner["ne"]
    targets = tuple(range(index, index + 3))
    width = index + 3
    inverse = []
    for wire in targets:
        forward = native.Execution(width, (), (), (native.Gate("G", (wire,)),), native.G_CX_SOURCE_I, 2, (0, 1))
        inversion = native.inverse_word(forward, max_qubits=width, max_expanded_stages=11)
        require(len(inversion) == 11, "every fresh writer route has eleven physical inverse calls")
        inverse.extend(inversion)
    actions = (*inverse, native.Gate("CX", (head, targets[0])), native.Gate("CX", (head, targets[2])))
    return targets, actions, width


def verify_writers(owner):
    a, p, one = owner["a"], owner["p"], owner["one"]
    v, defect = (a, p), (-p, a)
    stage_count = 0
    for slot, head in enumerate((5, 6, 5, 6)):
        targets, word, _ = writer_words(owner, 7 + 3 * slot, head)
        stage_count += len(targets) + len(word) + len(targets)  # births, gates, and physical Z reads

    # W3 uses the same addressed route for each new triple. Check both source
    # heads and every old computational column, plus each actual fresh direction.
    for head in (5, 6):
        _, word, width = writer_words(owner, 7, head)
        for old in range(128):
            b = (old >> (6 - head)) & 1
            for changed in (None, 0, 1, 2):
                state = {}
                for digits in product((0, 1), repeat=3):
                    amplitude = one
                    for wire, digit in enumerate(digits):
                        amplitude *= (defect if wire == changed else v)[digit]
                    code = 4*digits[0] + 2*digits[1] + digits[2]
                    state[8*old + code] = amplitude
                actual = apply_word(owner, state, word, width)
                expected = 5*b
                if changed is not None:
                    expected ^= 1 << (2 - changed)
                require(actual == {8*old + expected: one}, "all-column W3 and its orthogonal newborn")
    return stage_count


def verify_sign(owner, detector, writers, c, s):
    a, p, one = owner["a"], owner["p"], owner["one"]
    # The final closing CX is the first (wrap) step from the pre-last-gate leaf.
    winding = detector + 2 + writers + 1 + 1 + 1
    require(winding == 363, "first possible differing power for the fully read layout")
    weights = (p, p*p)
    eta = s*s
    born_M = tuple(weight * eta * eta for weight in weights)
    born_N = tuple(weight * eta * (one - eta) for weight in weights)
    require(born_M[1] * born_N[0] == born_M[0] * born_N[1], "actual Born cross ratio is one")
    success_lengths = [sum(1 + bit for bit in (b, 1-b, b, 1-b)) for b in (0, 1)]
    require(success_lengths == [6, 6] and sum(1 + bit for bit in (0, 0, 0, 0)) == 4,
            "literal printed cross ratio is one")
    passive_one, passive_zero = p*a*p, a*a*a
    passive_success = passive_one * passive_zero * passive_one * passive_zero
    passive_service = power(passive_zero, 4, one)
    require(passive_success == power(p, 8, one), "two printed ones and two zeros")
    require(passive_service == power(p, 6, one), "four printed zeros")
    moment_M0 = passive_success * p * c
    moment_N0 = passive_service * p * a * s
    require(moment_M0.coefficients == (-3566621, 0, 5770914, 0), "literal success moment")
    require(moment_N0.coefficients == (1732908, 0, -2803904, 0), "literal service moment")
    require(owner["enclosure"](moment_M0)[1] < -Fraction(18, 10000), "negative success margin")
    require(owner["enclosure"](moment_N0)[0] > Fraction(26, 1000), "positive service margin")
    y = Fraction(1, 22)  # exact strict upper bound for the actual 2p²/22
    tail = 2 * y / (winding + 1) / (1 - y / (winding + 2))
    require(tail < Fraction(3, 10000), "factorial Fourier tail")
    require(2 * (Fraction(18, 10000) + Fraction(26, 1000) - 2*tail) > Fraction(1, 20),
            "strict lower bound for log thermal cross ratio")
    return winding


def main():
    for path, expected in PINS.items():
        require(sha256(path.read_bytes()).hexdigest() == expected, f"pinned input {path}")
    owner = runpy.run_path(str(PILOT / "direct/round82/device/check_prepaid_report.py"))
    length, c, s = verify_detector(owner)
    writers = verify_writers(owner)
    winding = verify_sign(owner, length, writers, c, s)
    print(json.dumps({
        "status": "PASS",
        "detector_native_calls": length,
        "detector_basis_columns_per_defect": 32,
        "writer_basis_columns_per_head_and_birth_choice": 128,
        "writer_stages_including_twelve_births_and_twelve_reads": writers,
        "first_differing_winding": winding,
        "leading_moments_b0_b1": {"success": ["p^9 cos(12theta)", "0"],
                                  "service": ["p^7 sqrt(p) sin(12theta)", "0"]},
        "born_cross_ratio": "1",
        "literal_code_cross_ratio": "1",
        "log_thermal_cross_ratio": "> f_363/20 > 0",
        "GR_closed": False,
        "source_sha256": {str(path): value for path, value in PINS.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
