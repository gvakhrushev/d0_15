"""Exact CAR plane mixing by Golden gates and rational transverse-jet bounds."""

from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import runpy

PILOT = Path(__file__).resolve().parents[3]
WORK = PILOT / "open/round174/work/check_constant_action_work.py"
WIDTH = 12
OLD, SITE, CAR = (0, 1, 2), (3, 4, 5), (6, 7, 8, 9)
E, W = 10, 11


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def position(wire):
    return 1 << (WIDTH-1-wire)


def address(wires, value):
    return sum(position(wire) for j, wire in enumerate(reversed(wires)) if value & (1 << j))


def native_words(owner):
    native = owner["ne"]
    gate = native.Gate
    pivot, port = CAR[0], OLD[2]

    def cx(source, target):
        return gate("CX", (source, target))

    frame = tuple(cx(pivot, wire) for wire in CAR[1:])
    sign = cx(SITE[1], pivot)
    mixing = []
    for mask in range(8):
        path = tuple(cx(wire, pivot) for j, wire in enumerate(CAR[1:]) if mask & (1 << j))
        mixing.extend((*path, gate("G", (pivot,)), *path[::-1]))
    forward = (*frame, sign, *mixing, sign, *frame[::-1])

    route = (cx(port, pivot), cx(pivot, port), cx(port, pivot))
    physical_sign = (*route, *((gate("SourceI", (port, *OLD[:2])),)*2), *route)
    backward = (*physical_sign, *forward, *physical_sign)

    a, d = cx(pivot, E), cx(E, W)
    reference = (*forward, d, d, a, a, *backward)
    active = (*forward, a, d, d, a, *backward)
    for word in (forward, backward, reference, active):
        execution = native.Execution(WIDTH, (), (), word, native.G_CX_SOURCE_I, port, OLD[:2])
        native.validate_execution(execution, max_qubits=WIDTH, max_expanded_stages=len(word))
    inventory = lambda word: Counter((gate.op, gate.wires) for gate in word)
    require(inventory(reference) == inventory(active), "same full addressed inventory")
    require((len(forward), len(backward), len(reference)) == (40, 56, 100),
            "literal native lengths including both routers and signs")
    return forward, backward, reference, active


def check_plane_columns(owner, forward, backward):
    cosine, sine = owner["rot"](8)
    one = owner["one"]
    action = owner["action"]
    action.__globals__["gate_columns"] = lru_cache(None)(action.__globals__["gate_columns"])

    def replay(column, word):
        state = {column: one}
        for gate in word:
            state = action(state, gate, WIDTH)
        return state

    for old, site, car in product(range(8), (0, 1), range(16)):
        prefix = address(OLD, old) | (position(SITE[1]) if site else 0)
        column = prefix | address(CAR, car)
        for word, direction in ((forward, 1), (backward, -1)):
            amplitudes = {column: one}
            if car in (0, 15):
                amplitudes = {
                    column: cosine,
                    prefix | address(CAR, car ^ 15): direction*(-1)**(site+int(car == 15))*sine,
                }
            require(replay(column, word) == amplitudes, "exact native plane and old RIGHT identity")
    return 8*2*16


def check_site_mask():
    levels = (8, 16, 32, 64, 128, 256)
    for length in levels:
        quarter = length//4
        for site in range(length):
            flag = (site//quarter) & 1
            phase = site % (length//2)
            if phase not in (0, quarter):
                require(flag == int(phase > quarter), "second true SITE bit matches sin(2*phase)")
    return levels


def check_bounds(owner):
    ranges = owner["native_rotation_intervals"](16, bits=160)
    (c_low, c_high), (s_low, s_high) = [
        tuple(owner["rational"](bound) for bound in interval) for interval in ranges
    ]
    require(F("-.34") < c_low <= c_high < F("-.32"), "orientation's strictly negative affine coefficient")
    require(F("-.95") < s_low <= s_high < F("-.94"), "strict native interference coefficient")
    p_lower = F(".618")
    require(p_lower+p_lower*p_lower < 1, "Golden p lower bound")
    a_max = F(1,1024)
    require(p_lower*p_lower-2*a_max > F(".37"), "strict uniform Q lower bound")
    g_min = 2*F(".37")-F(".37")**2
    require(g_min**3 > F(2,5)**2 and F(".6")*g_min > F(1,3),
            "uniform |f''| below 5 and |f''/f'| below 3")
    require(F("1.54")*F(".225")-5*a_max > F(".34"), "uniform positive curvature")
    require(F(".34")*F(1,2560) > F(".00013"), "uniform curvature independent of mesh")
    require(F(".225")-3*a_max*F(".77")**2-F(".002")*F(".77") > F(".22"),
            "positive orientation stays above the diagonal jet")
    require(-F(".225")+F(".002")*F(".77") < -F(".22"),
            "opposite orientation stays below the diagonal jet")
    require(2*F(".16")*F(".225")-6*a_max*F(".77")**3 > F(".069"),
            "strict positive cone determinant")
    require(5*a_max/(2*F("1.54")) < F(".002"), "target diagonal slope bound")


def main():
    tools = runpy.run_path(str(WORK))
    owner = runpy.run_path(str(tools["OWNER"]))
    forward, backward, ref, active = native_words(owner)
    columns = check_plane_columns(owner, forward, backward)
    check_bounds(owner)
    print(json.dumps({
        "status": "PASS",
        "plane_columns_each_direction": columns,
        "remaining_registered_wires_are_spectators": True,
        "mixing_calls": len(forward),
        "inverse_calls": len(backward),
        "complete_calls_per_echo_arm": len(active),
        "same_address_inventory": len(active) == len(ref),
        "exact_local_orientation_lattices": check_site_mask(),
        "uniform_positive_transverse_work_hessian_lower_bound": ".00013",
        "normalized_positive_cone_determinant_lower_bound": ".069",
        "absolute_cost_tariff_derived": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
