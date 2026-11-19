"""Exact branches and thermal first winding for a physical NC1/corrector composition."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import runpy


SOURCES = Path("02_REGISTRY/research/sources")
PILOT = SOURCES / "d0_two_agent_pilot_2026-11-13"
PINS = {
    PILOT / "direct/round82/device/check_prepaid_report.py": "d7bb38033ccfade7f29b76195928b18ec507c82cc633ab7e3e67f6d1a57bc99f",
    PILOT / "open/round169/B169_TERMINAL_GIBBS_BORN_RU.md": "b299d1fa7544ccb37897458458f317b6cd741a9403b0a19ede55c3f2a9a0fe13",
    SOURCES / "d0_native_execution_domain_2026-10-24/native_execution.py": "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c",
}
WIDTH = 9
T, H, N, TAIL, BAR, HELPER = 3, 4, 5, 6, 7, 8


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def mask(wire):
    return 1 << (WIDTH-1-wire)


def bit(column, wire):
    return int(bool(column & mask(wire)))


def power(value, n, one):
    result = one
    for _ in range(n):
        result *= value
    return result


def state(owner, old, factors):
    prefix = (old << (WIDTH-4)) | mask(H)
    result = {}
    for values in product((0, 1), repeat=4):
        index, amp = prefix, owner["one"]
        for wire, value, vector in zip((N, TAIL, BAR, HELPER), values, factors):
            index |= value*mask(wire)
            amp *= vector[value]
        if amp != 0:
            result[index] = amp
    return result


def apply(owner, current, calls):
    for gate in calls:
        current = owner["action"](current, gate, WIDTH)
    return current


def programs(owner):
    native = owner["ne"]
    gate = native.Gate

    def cx(control, target):
        return gate("CX", (control, target))

    def inverse(target):
        forward = native.Execution(WIDTH, (), (), (gate("G", (target,)),), native.G_CX_SOURCE_I, 2, (0, 1))
        calls = native.inverse_word(forward, max_qubits=WIDTH, max_expanded_stages=11)
        require(len(calls) == 11, "paid address inverse")
        return calls

    control = (cx(T, N),)
    nc1 = (cx(N, TAIL), gate("G", (TAIL,)), cx(N, TAIL))
    bar = (*inverse(BAR), cx(H, BAR), cx(N, BAR))
    corrector = (*inverse(TAIL), cx(BAR, TAIL), gate("G", (TAIL,)), cx(BAR, TAIL))
    require(len(corrector) == 14, "literal original corrector")
    terminal = (cx(N, HELPER), cx(N, HELPER))
    return control, nc1, bar, corrector, terminal


def verify_branches(owner, control, nc1, bar, corrector, terminal):
    v, one, p, a = owner["v"], owner["one"], owner["p"], owner["a"]
    zero = owner["Golden"]()
    basis = ((one, zero), (zero, one))
    defect = (-p, a)
    finish = (*bar, *corrector, *terminal)
    leading_short = (a*p*p*p, -p*p*p)
    for old in range(16):
        t = old % 2
        actual = apply(owner, state(owner, old, (v, v, v, v)), (*control, *nc1))
        require(not any(bit(col, N) and bit(col, TAIL) for col in actual), "genuinely dark 11 on native input")
        altered = apply(owner, state(owner, old, (defect, v, v, v)), (*control, *nc1))
        for b in (0, 1):
            def nc1_project(data):
                return {col: amp for col, amp in data.items() if bit(col, N) == b and (b == 0 or not bit(col, TAIL))}

            final_basis = state(owner, old, (basis[b], basis[0], basis[1-b], v))
            reached = apply(owner, nc1_project(actual), finish)
            require(reached == {col: v[t ^ b]*amp for col, amp in final_basis.items()}, "all-column charged real branch")
            from_early_defect = apply(owner, nc1_project(altered), finish)
            require(from_early_defect == {col: defect[t ^ b]*amp for col, amp in final_basis.items()},
                    "literal first birth defect transport")
            if b == 0:
                first = defect[b]*v[0]*v[1-b]*defect[t ^ b]
                require(first == leading_short[t], "short-leaf first winding coefficient")
            tail_defect = state(owner, old, (basis[b], defect, v, v))
            from_tail = apply(owner, nc1_project(apply(owner, tail_defect, nc1)), finish)
            require(not set(from_tail).intersection(final_basis), "latest NC1 defect cannot reach the measured terminal column")
            bar_defect = state(owner, old, (basis[b], basis[0], defect, v))
            from_bar = apply(owner, bar_defect, finish)
            require(all(bit(col, BAR) == b for col in from_bar), "orthogonal barN remains wrong at terminal")
            if b == 1:
                require(any(bit(col, TAIL) == 1 for col in from_bar), "ambient tail move is retained for the two-wrap bound")
            passive_square = v[b]*v[b]*v[0]*v[0]*v[1-b]*v[1-b]
            require(passive_square == power(p, 4, one), "same passive fixed-rank compression on both leaves")
    print_source = p-p*p
    require(print_source == power(p, 3, one), "conditional literal mean difference")
    return leading_short


def verify_heat(owner, control, nc1, bar, corrector, terminal, leading_short):
    # Depth from the child of the actual N birth. The second helper CX is the
    # wrap, not an additional forward step.
    shared = len(control) + 1 + len(nc1) + 1
    depths = (shared+1+len(bar)+len(corrector)+1+len(terminal)-1,
              shared+2+len(bar)+len(corrector)+1+len(terminal)-1)
    require(depths == (36, 37), "two physical terminal addresses")
    clock_dim = 32 + (1+len(control))*64 + (1+len(nc1)+4)*128
    clock_dim += 3*((1+len(bar)+len(corrector))*256 + len(terminal)*512)
    require(clock_dim == 25760 and 425*clock_dim == 10948000, "full typed mode dimension including dark leaf")
    after_tail_read, bar_birth_long = shared+1, shared+2
    require((after_tail_read, bar_birth_long) == (7, 8), "long-branch actual late stages")
    two_wrap = (1+depths[1]-bar_birth_long) + (1+depths[1]-after_tail_read)
    require(two_wrap == 61 and two_wrap > 37, "potential ambient late tail motion cannot create earlier winding")
    p = owner["p"]
    leading_difference = p*leading_short[0]-p*p*leading_short[1]
    require(owner["enclosure"](leading_difference)[0] > F(1, 5), "positive averaged first winding")
    y = F(1, 22)
    tail = 2*y/38/(1-y/39)
    require(tail < F(3, 1000), "thermal Fourier tail bound")
    require(2*(F(1, 5)-tail) > F(39, 100), "strict full heat gap")
    return depths, two_wrap, clock_dim


def main():
    for path, expected in PINS.items():
        require(sha256(path.read_bytes()).hexdigest() == expected, f"pinned owner {path}")
    owner = runpy.run_path(str(PILOT / "direct/round82/device/check_prepaid_report.py"))
    words = programs(owner)
    moments = verify_branches(owner, *words)
    depths, two_wrap, clock_dim = verify_heat(owner, *words, moments)
    print(json.dumps({
        "status": "PASS",
        "old_live_T_spin_port_columns": 16,
        "true_corrector_calls": 14,
        "positive_full_root_leaf_compressions": ["p^4 I", "p^4 I"],
        "full_root_cold_operator": "2 p^4 I",
        "full_clock_staged_dimension": clock_dim,
        "full_two_degree_spatial_dimension": 425*clock_dim,
        "terminal_depths_before_actual_wrap": depths,
        "short_branch_first_moments_t0_t1": ["sqrt(p) p^3", "-p^3"],
        "long_two_wrap_tail_route_at_least": two_wrap,
        "aggregate_sector_heat_difference": "k_0-k_1 > 0.39 f_37",
        "conditional_print_minus_CQ_derivative": "p^3 Dq",
        "GR_closed": False,
        "source_sha256": {str(path): value for path, value in PINS.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
