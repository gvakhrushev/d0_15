"""Physical NC1 parity and local prices on a returned field rotation. Python 3.9+."""
from itertools import product
from fractions import Fraction as Q
from math import cos, factorial, log, pi, sin, sqrt
import json


p = (sqrt(5) - 1) / 2
a = sqrt(p)
v = (a, p)
golden = ((a, -p), (p, a))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def cx(state, control, target):
    return {i ^ (((i >> control) & 1) << target): z for i, z in state.items()}


def local(state, wire, matrix):
    out = {}
    for i, z in state.items():
        old = (i >> wire) & 1
        for bit in (0, 1):
            j = (i & ~(1 << wire)) | (bit << wire)
            out[j] = out.get(j, 0.0) + matrix[bit][old] * z
    return out


def density(state, keep):
    size = 1 << len(keep)
    matrix = [[0.0] * size for _ in range(size)]
    mask = sum(1 << wire for wire in keep)
    groups = {}
    for i, z in state.items():
        j = sum(((i >> wire) & 1) << bit for bit, wire in enumerate(keep))
        groups.setdefault(i & ~mask, {})[j] = z
    for values in groups.values():
        for i, left in values.items():
            for j, right in values.items():
                matrix[i][j] += left*right
    return [x for row in matrix for x in row]


def nc1(state, head, tail):
    first = cx(state, head, tail)
    second = local(first, tail, golden)
    third = cx(second, head, tail)
    return (first, second, third)


def parity_factory():
    # A,R,F=0,tail=v with A,R born in v.
    state = {i | (j << 1) | (t << 3): v[i]*v[j]*v[t]
             for i, j, t in product(range(2), repeat=3)}
    state = nc1(cx(cx(state, 0, 2), 1, 2), 2, 3)[-1]
    good = {i: z for i, z in state.items() if i & 4}
    mass = sum(z*z for z in good.values())
    require(abs(mass-2*p**3) < 1e-14, "real herald")
    require(abs(good[5]-good[6]) < 1e-14 and abs(good[5]-p*a) < 1e-14, "odd Bell")
    phi = cx(good, 2, 1)
    require(abs(phi[4]-phi[7]) < 1e-14, "corrected pair")
    return mass


def native_cj():
    # The gate of A13 on all H,T,dirty-port,Spin columns; only port can be swapped.
    def cnot(row, x, y):
        return row ^ (((row >> x) & 1) << y)

    def swap(row, x, y):
        for c, t in ((x, y), (y, x), (x, y)):
            row = cnot(row, c, t)
        return row

    def controlled_source(row, sign, x, turns):
        row = swap(row, x, 2)
        for _ in range(turns):
            if (row >> 2) & 1:
                if (row >> 3) & 1:
                    sign = -sign
                row ^= 8  # SourceI on both Spin bits: I_2 tensor J.
        return swap(row, x, 2), sign

    for start in range(32):
        h, t = start & 1, (start >> 1) & 1
        row, sign = controlled_source(start, 1, 0, 1)
        row, sign = controlled_source(row, sign, 1, 1)
        row = cnot(row, 0, 1)
        row, sign = controlled_source(row, sign, 1, 3)
        row = cnot(row, 0, 1)
        require((row, sign) == (start, (-1)**(h*t)), "native CZ/old spin")
        require(cnot(row, 0, 1) == (start ^ (h << 1)), "native controlled quarter-turn")
    return 32


def address_average():
    # One paid fair record globally permutes both addresses of every digit.
    totals = set()
    cases = 0
    for bits in product(range(2), repeat=3):
        combined = 0
        for gauge in (0, 1):
            price = 0
            for j in range(3):
                load = [2*i + (value ^ gauge) for i, value in enumerate(bits)]
                read = 2*j + (1 ^ gauge)
                schedule = load + [read] + list(reversed(load)) + [read]
                price += sum((1 + at + 3*j)**2 * (addr+2) for at, addr in enumerate(schedule))
                for h, old in product((0, 1), range(64)):
                    k, t = old, 0
                    for forward in (True, False):
                        for addr in (load if forward else reversed(load)):
                            k ^= h << addr
                        t ^= (k >> read) & 1
                    require((k, t) == (old, h*bits[j]), "permuted dirty address")
                    cases += 1
            combined += price
        totals.add(combined)
    require(len(totals) == 1, "time-dependent fixed physical address rates")
    return cases


def decoder(angle):
    # H,H',T,T',C,C',B,F. Start after the holonomy controlled by H.
    c, s = cos(angle), sin(angle)
    rotation = ((c, -s), (s, c))
    state = {}
    for h, old, t, f in product(range(2), repeat=4):
        coeff = rotation[t][old] if h else float(t == old)
        i = h | (h << 1) | (t << 2) | (old << 3) | (f << 7)
        state[i] = coeff * v[f] / 2
    stages = []
    for control, target in ((2, 4), (3, 5), (4, 6), (5, 6), (2, 4), (3, 5)):
        state = cx(state, control, target)
        stages.append(density(state, (control, target)))
    for target in (4, 5):  # Physically return temporary wires to their true births.
        state = local(state, target, golden)
        stages.append(density(state, (target,)))
    sequence = nc1(state, 6, 7)
    for sub, wires in zip(sequence, ((6, 7), (7,), (6, 7))):
        stages.append(density(sub, wires))
    state = sequence[-1]
    masses, cold = [], []
    for record in (0, 1):
        leaf = {i: z for i, z in state.items() if (i >> 6) & 1 == record}
        mass = sum(z*z for z in leaf.values())
        contraction = 0.0
        for i, coeff in leaf.items():
            born = 1.0
            for bit in range(8):
                born *= v[(i >> bit) & 1]
            contraction += born * coeff
        masses.append(mass)
        cold.append(contraction**2/mass if mass > 1e-25 else 0.0)
    q = s*s/2
    require(abs(masses[1]-q) < 1e-14, "parity report")
    predicted = p*p*(p+p*p*c)**2/(2*(1+c*c))
    require(abs(cold[0]-predicted) < 1e-13 and cold[1] < 1e-24, "true cold cuts")
    return q, stages


def check_local_prices():
    _, left = decoder(0)
    _, right = decoder(pi/2)
    worst = 0.0
    angles = [0.0001, 0.05, 0.19, 0.37, 0.66, 1.0, 1.4]
    for angle in angles:
        q, seen = decoder(angle)
        for actual, base, end in zip(seen, left, right):
            worst = max(worst, max(abs(x-s-2*q*(t-s)) for x, s, t in zip(actual, base, end)))
    require(worst < 1e-12, "nonaffine local paid matrix")
    varying = [i+1 for i, (base, end) in enumerate(zip(left, right))
               if max(abs(x-y) for x, y in zip(base, end)) > 1e-12]
    require(varying == [4, 9, 10, 11], "field-sensitive operations")
    # Four positive operator tariffs <=1 and a terminal code contrast of one.
    threshold = 1 / (1 + (1/p)**5)
    require(log((1-threshold)/threshold)/log(1/p) > 5-1e-13, "uniform slope")
    return {"stages": len(left), "varying_stage_numbers": varying,
            "angles_checked": len(angles), "universal_upper_price_slope": 5,
            "sufficient_q_below": "1/(1+phi^5)"}


def arc_bound():
    # Alternating Taylor brackets for sin on [0,1] and 333/106 < pi < 22/7.
    def sine_partial(x, terms):
        return sum((-1)**j * x**(2*j+1) / factorial(2*j+1) for j in range(terms))
    low, high = Q(66623, 100000), Q(66624, 100000)
    low_sine, high_sine = sine_partial(low, 5), sine_partial(high, 6)
    require((1 + 2*low_sine)**2 < 5 < (1 + 2*high_sine)**2, "golden angle")
    upper = 10*high - 2*Q(333, 106) + Q(1, 32)
    require(10*low - 2*Q(22, 7) - Q(1, 32) > 0, "positive angle")
    require(sine_partial(upper, 3)**2 / 2 < Q(2, 25), "actual finite arc")
    require(1 / (1 + Q(81, 50)**5) > Q(2, 25), "economic threshold")


def reset_prepared_rail():
    # Phi+ -> (+,0); a fresh true code head D and tail F. Both results kept.
    state = {h | (h << 1) | (t << 3): v[t]/sqrt(2)
             for h, t in product(range(2), repeat=2)}
    state = cx(cx(state, 0, 1), 0, 2)
    state = nc1(state, 2, 3)[-1]
    state = local(local(cx(state, 2, 0), 0, golden), 1, golden)
    for record in (0, 1):
        leaf = {i: z for i, z in state.items() if (i >> 2) & 1 == record}
        mass = sum(z*z for z in leaf.values())
        require(abs(mass - 0.5) < 1e-14, "honest reset history")
        projection = 0.0
        for tail in (0, 1):
            amp = sum(v[k]*v[r]*leaf.get(k | r << 1 | record << 2 | tail << 3, 0.0)
                      for k, r in product(range(2), repeat=2))
            projection += amp*amp
        require(abs(projection - mass) < 1e-14, "true return on both recorded leaves")


if __name__ == "__main__":
    parity_factory()
    arc_bound()
    reset_prepared_rail()
    print(json.dumps({"a88": "Bell parity decoder", "pair_herald": "2*p^3",
                      "controlled_quarter_turn_basis_columns": native_cj(),
                      "dirty_query_address_gauge_cases": address_average(),
                      "local_work": check_local_prices(), "actual_q_below": "2/25",
                      "original_K_reset_on_two_records": True, "GR_closed": False},
                     indent=2, sort_keys=True))
