"""Native single-target cancellation of the B174 matched movement excess."""
from collections import Counter
from pathlib import Path
import json
import runpy

from mpmath import iv


PILOT = Path(__file__).resolve().parents[3]
WIDTH = 13
SITE = (0, 1, 2)
CAR = (3, 4, 5, 6)
H, E, W, PORT, S0, S1 = range(7, 13)
N = 7932


def require(result, message):
    if not result:
        raise ArithmeticError(message)


def signs(mask, section):
    return (-1) ** bin(mask & section).count("1")


def interval_rotation(p, power):
    def mul(left, right):
        c, s = left
        x, y = right
        return c*x-s*y, c*y+s*x

    result = (iv.mpf(1), iv.mpf(0))
    base = (iv.sqrt(p), p if power >= 0 else -p)
    power = abs(power)
    while power:
        if power & 1:
            result = mul(result, base)
        power >>= 1
        if power:
            base = mul(base, base)
    return result


def actual_material_predicates(p):
    b174 = json.loads((PILOT / "open/round174/material/RESULT.json").read_text())
    require(b174["field_endpoints"] == [0.375, 0.625], "B174 verified same native input")
    require(b174["certified_literal_CAR_material_jet_all_edge_signs"], "B174 material input")
    powers_x, powers_y = b174["cartesian_walsh_powers"]
    # B174's common static native ground plane, from search=8000.
    anchor = 7596
    a = iv.sqrt(p)
    target_probabilities = []

    def apply(state, i, j, k):
        c, s = interval_rotation(p, k)
        x, y = state[i], state[j]
        state[i], state[j] = c*x-s*y, s*x+c*y

    for j in range(2):
        q_minus, q_plus = iv.mpf(0), iv.mpf(0)
        for n in range(8):
            section = 8*j+n
            x = 16 * sum(k*signs(mask, section) for mask, k in enumerate(powers_x))
            y = 16 * sum(k*signs(mask, section) for mask, k in enumerate(powers_y))
            m = [iv.mpf(0), a, p, iv.mpf(0)]  # CAR 0,1,14,15
            for i, k, angle in ((1,2,-16*anchor), (2,0,-x), (2,3,-y),
                                (1,2,16*anchor), (2,3,y), (2,0,x)):
                apply(m, i, k, angle)
            q_minus += (m[2]**2+m[3]**2)/8
            s = ((n//2) ^ n) & 1
            q_plus += sum(c**2 for i, c in enumerate(m) if s ^ (i in (0,3)))/8
        target_probabilities.append((q_minus, q_plus))
    return target_probabilities


def certify_work(p):
    first, second = actual_material_predicates(p)
    q0, r0 = first
    q1, r1 = second
    require(0 < q1.a and q1.b < q0.a and q0.b < (p*p).a, "strict native decreasing predicate")
    require(iv.mpf('0.5') < r0.a and r0.b < r1.a, "strict native increasing predicate")

    def F(x):
        return 2 * iv.sqrt(2*x-x*x)

    falling = 4*(F(q1)-F(q0))
    rising = 4*(F(r1)-F(r0))
    require(falling.b < -iv.mpf(".00031") and rising.a > iv.mpf(".00019"),
            "strict movement on the actual tape")
    require((falling+rising).b < 0, "strict native centered root bracket, lambda=1")
    c, s = interval_rotation(p, N)
    require(c.a > s.b and s.a > 0, "fresh target lies in the positive octant")
    attenuation = 1-2*c*s
    new = 4*(F(attenuation*q1)-F(attenuation*q0))+rising
    require(new.a > -iv.mpf(".000000016") and new.b < -iv.mpf(".000000015"),
            "native centered residual signed outward interval")
    return {
        "native_t_endpoint_Q_minus": [float(q0.mid), float(q1.mid)],
        "native_t_endpoint_Q_plus": [float(r0.mid), float(r1.mid)],
        "native_unattenuated_secants": [float(falling.mid), float(rising.mid)],
        "native_target_attenuation": float(attenuation.mid),
        "native_compensated_secant_enclosure": ["-1.6e-8","-1.5e-8"],
        "meter_and_external_prefactor_excluded_from_receipt": True,
    }


def actual_words(native):
    def G(wire):
        return native.Gate("G", (wire,))

    def CX(a, b):
        return native.Gate("CX", (a,b))

    def run(gates):
        return native.Execution(WIDTH, (E,W), (), gates, native.G_CX_SOURCE_I, PORT, (S0,S1))

    def inverse_one(wire):
        return native.inverse_word(run((G(wire),)), max_qubits=WIDTH, max_expanded_stages=11)

    def swap(a, b):
        return (CX(a,b), CX(b,a), CX(a,b))

    def inverse_power(wire, k):
        route = swap(wire, PORT)
        sign = (native.Gate("SourceI", (PORT,S0,S1)),)*2
        return route + sign + (G(PORT),)*k + sign + route

    A_1 = (CX(CAR[0],E),)
    A_2 = tuple(CX(wire,E) for wire in (*SITE[1:], *CAR, H))
    D = (CX(E,W),)*2
    for A in (A_1, A_2):
        for order in (D + A + A[::-1], A + D + A[::-1]):
            for basis in range(1 << WIDTH):
                moved = basis
                for gate in order:
                    c,t = [1 << (WIDTH-1-w) for w in gate.wires]
                    moved ^= t if moved & c else 0
                require(moved == basis, "both literal diagnostic orders equal identity")
    clear = inverse_one(E) + inverse_one(W)
    prep = (G(W),)*N
    restore = inverse_power(W,N)
    closing = (G(E),G(W))
    out = []
    for live in (False, True):
        a1 = A_1 + D + A_1[::-1] if live else D + A_1 + A_1[::-1]
        a2 = A_2 + D + A_2[::-1] if live else D + A_2 + A_2[::-1]
        word = clear + prep + a1 + restore + a2 + closing
        native.validate_execution(run(word), max_qubits=WIDTH, max_expanded_stages=len(word))
        out.append(Counter((g.op,g.wires) for g in word))
    require(out[0] == out[1], "all actual typed gate counts agree between arms")
    return dict(Counter({op: sum(count for (name,_),count in out[0].items() if name == op)
                         for op in ("CX","G","SourceI")}))


def verify_inverse_all_columns(owner):
    native = owner["ne"]
    # Replay every column of the common PORT/Spin and target frame.
    width, target, port, spin = 4, 3, 0, (1,2)
    g = native.Gate("G",(target,))
    ex = native.Execution(width, (), (), (g,), native.G_CX_SOURCE_I, port, spin)
    inv = native.inverse_word(ex,max_qubits=width,max_expanded_stages=11)
    for col in range(1 << width):
        before = {col:owner["one"]}
        after = before
        for gate in (g,*inv):
            after = owner["action"](after,gate,width)
        require(after == before, "actual inverse returns every PORT, Spin and W column")
    return len(inv)


def main():
    owner = runpy.run_path(str(PILOT / "direct/round82/device/check_prepaid_report.py"))
    native = owner["ne"]
    iv.dps = 65
    p = (iv.sqrt(5)-1)/2
    require((3*(iv.sqrt(p)**2)).a > iv.mpf(16)/9,
            "uniform negative range strictly covers opposite slope")
    inventory = actual_words(native)
    inverse_calls = verify_inverse_all_columns(owner)
    print(json.dumps({
        "status":"PASS",
        "B174_material_trace": "open/round174/material/RESULT.json",
        "PR334_current_pin": "908e70a3c86be2c99809f1faa830c92993b117ae",
        "L":8,
        "t0":0.5,
        "half_secant_step":0.125,
        "same_full_closing_output": True,
        "B174_diagnostics_all_columns": 1 << WIDTH,
        "reference_and_live_address_inventory":inventory,
        "verified_single_G_inverse_calls":inverse_calls,
        "actual_G_power_on_one_fresh_target":N,
        **certify_work(p),
        "full_Book03_cost_cancellation_derived":False,
        "GR_closed":False,
    }, indent=2))


if __name__ == "__main__":
    main()
