"""Exact positive G/CX readout with a paid sharp control, and spectator-free work."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'round82' / 'device'))
import check_prepaid_report as src

ne, zero, one = src.ne, src.Golden(), src.one
p, v, a = src.p, src.v, src.a
add, sub, mul, enc = src.plus, src.minus, src.times, src.enclosure
L, Y, T, FP, FQ = range(5)


def detector(k, order=(0, 1, 2, 3)):
    def flip(control, target):
        return ne.Gate('CX', (control, target))

    def rotation(target, count, negative):
        steps = (ne.Gate('G', (target,)),) * count
        x = (flip(L, target),)
        return x + steps + x if negative else steps

    def conditional(target, inverse):
        result = []
        for mask in order:
            route = tuple(flip(ctl, target) for i, ctl in enumerate((Y, T)) if mask & (1 << i))
            sign = bool(len(route) % 2) != inverse
            result.extend(route + rotation(target, k, sign) + tuple(reversed(route)))
        return tuple(result)

    seq = (rotation(FP, 1, True) + rotation(FQ, 1, True)
           + conditional(FP, False) + rotation(FQ, 4*k, False) + conditional(FQ, True))
    # OldSpin(0,1), PORT(2), unrelated oldRIGHT(3), all physically present.
    physical = tuple(ne.Gate(g.op, tuple(4+i for i in g.wires)) for g in seq)
    ex = ne.Execution(9, (), (3,), physical, ne.G_CX_SOURCE_I, 2, (0, 1), (4+FP, 4+FQ))
    ne.execution_from_json(ne.canonical_json(ex), max_qubits=9, max_expanded_stages=len(seq))
    assert Counter(g.op for g in seq) == {'CX': 28, 'G': 12*k+2}
    return seq


def exact_run(gates, y, ts, c, s):
    psi = {(1 << 4)+(y << 3)+(t << 2)+2*i+j: ti*v[i]*v[j]
           for t, ti in enumerate(ts) if ti != 0 for i, j in product(range(2), repeat=2)}
    total = src.interval(0)
    for gate in gates:
        out = src.action(psi, gate, 5)
        overlap = sum((amp*out.get(i, zero) for i, amp in psi.items()), zero)
        total = add(total, src.trace_distance(overlap))
        psi = out
    target = {}
    for t, weight in enumerate(ts):
        if weight == 0:
            continue
        base = (1 << 4)+(y << 3)+(t << 2)
        target[base] = c*weight
        target[base+(2 if y == t == 1 else 1)] = s*weight
    assert psi == target
    return total


def mid(x):
    return float(sum(x)/2)


def rates(k, order=(0, 1, 2, 3)):
    gates = detector(k, order)
    c, s = src.rot(4*k)
    e = enc(s*s)
    r = enc(p*p)
    probs = [enc(p), r]
    inputs = [(one, zero), (zero, one), v]
    costs = {(y, idx): exact_run(gates, y, vals, c, s) for y in range(2)
             for idx, vals in enumerate(inputs)}
    weighted = add(mul(probs[0], costs[1,0]), mul(probs[1], costs[1,1]))
    # All three recorded NC1 writers, with the genuine extra copy of FP.
    parsing = mul(mul(e, r), enc(one+src.p3))
    first = add(sub(costs[1,2], costs[0,2]), parsing)
    late = add(sub(weighted, costs[0,2]), parsing)
    assert float(first[1]-first[0])<1e-8 and float(late[1]-late[0])<1e-8
    print('k', k, 'eta', mid(e), 'motion ready states', [round(mid(u),8) for u in costs.values()],
          'first/late', mid(first), mid(late))
    return e, first, late


def verify_threshold():
    eta, first, late = rates(3, (0, 2, 1, 3))
    assert first[0] > F('7.01167') and late[0] > F('2.28323')
    r = enc(p*p)
    delta = sub(1, eta)
    unresolved = src.interval(1)
    for n in range(1, 6):
        unresolved = mul(unresolved, delta)
        slope = sub(mul(n, mul(eta, r)), mul(sub(1, unresolved), add(1, r)))
        if n <= 3:
            assert slope[1] < 0
        else:
            assert slope[0] > F('.115')
    # The two original pointer confirmations have positive sector secants.
    z = mul(eta, r)
    reg = mul(2, mul(z, sub(sub(1,z), src.divide(mul(delta,delta),sub(1,z)))))
    later = src.divide(sub(eta,z),sub(1,z))
    coh = sub(add(src.lcd(z),add(z,mul(sub(1,z),src.lcd(later)))),add(1,src.lcd(eta)))
    assert reg[0] > F('.468') and coh[0] > F('.847')
    # Complete stopped preparation: rectangular powers are kept in the same ring.
    mass, earlier = zero, one
    for _ in range(8):
        mass += earlier*p*p
        earlier *= p
        assert mass + earlier == one
    print('Walsh k=3: n=4, two confirmation slopes',mid(reg),mid(coh))


if __name__ == '__main__':
    verify_threshold()
