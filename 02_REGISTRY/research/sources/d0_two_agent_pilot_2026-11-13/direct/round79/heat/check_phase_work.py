"""Full-column primitive overlaps and certified secants on both native 18-gate words."""
from fractions import Fraction
from functools import lru_cache
from math import isqrt
from pathlib import Path
import sys

import numpy as np

from check_return_moments import Golden, identity, same

SOURCE = Path(__file__).resolve().parents[4] / 'd0_native_execution_domain_2026-10-24'
sys.path.insert(0, str(SOURCE))
import native_execution as ne

a = Golden(0, 1)
p = a*a
one = Golden(1)
v = np.array([[a], [p]], dtype=object)
spin = identity(4)
left_i = np.array(ne.L_I, dtype=int).astype(object)
N = 10**22


def interval(value):
    return value if isinstance(value, tuple) else (Fraction(value), Fraction(value))


def plus(x, y):
    x, y = interval(x), interval(y)
    return x[0]+y[0], x[1]+y[1]


def times(x, y):
    values = [s*t for s in interval(x) for t in interval(y)]
    return min(values), max(values)


def minus(x, y):
    return plus(x, times(-1, y))


def root(x):
    lower, upper = interval(x)
    assert upper >= 0
    def floor_sqrt(t):
        t = max(Fraction(0), t)
        return isqrt((t.numerator * N*N) // t.denominator)
    return Fraction(floor_sqrt(lower), N), Fraction(floor_sqrt(upper)+1, N)


p_iv = times(Fraction(1, 2), minus(root(5), 1))
a_iv = root(p_iv)


def enclosure(value):
    result = interval(0)
    for coefficient in reversed(Golden.cast(value).coefficients):
        result = plus(times(result, a_iv), coefficient)
    return result


def trace_distance(overlap):
    if overlap == 1:
        return interval(0)
    return root(minus(1, enclosure(overlap*overlap)))


def inside(value, lower, upper):
    assert Fraction(lower) < value[0] <= value[1] < Fraction(upper), value


def native_word(prep, target):
    gate = ne.Gate
    def sign(j):
        route = (gate('CX', (2,j)), gate('CX', (j,2)), gate('CX', (2,j)))
        return route + (gate('SourceI', (2,0,1)),)*2 + route
    begin = ((gate('G',(3,)), gate('G',(4,))) if prep else (gate('CX',(3,4)),)*2)
    gates = begin + sign(4) + sign(target)
    execution = ne.Execution(5, (), (), gates, profile=ne.G_CX_SOURCE_I,
                             source_port=2, source_spin=(0,1), report_bits=(3,4))
    ne.execution_from_json(ne.canonical_json(execution), max_qubits=5, max_expanded_stages=18)
    @lru_cache(None)
    def matrix(g):
        native = ne.gate_matrix(execution, g, max_qubits=5, max_expanded_stages=18)
        values = {ne.A:a, ne.P:p, -ne.P:-p, 1:1, -1:-1, 0:0}
        return np.array([[values[entry] for entry in row] for row in native.tolist()],
                        dtype=object)
    state = np.kron(spin, np.kron(v, np.kron(v, v)))
    overlaps = []
    w = (a,p) if not prep else (p-p*p, 2*a*p)
    occupancy = w[1]*w[1]
    spin_pure = np.outer(spin[:, 0], spin[:, 0])
    spin_rotated = np.outer(left_i[:, 0], left_i[:, 0])
    choi_pure = np.outer(spin.ravel(), spin.ravel())
    choi_rotated = np.outer(left_i.ravel(), left_i.ravel())
    for stage, gate in enumerate(gates, start=1):
        new = matrix(gate) @ state
        overlap = state.T @ new
        if gate.op == 'SourceI':
            same(overlap, spin*(one-occupancy) + left_i*occupancy)
        else:
            same(overlap, spin*overlap[0,0])
        t = occupancy if stage in (6, 14) else Golden(0)
        amplitudes = new.reshape(4, 8, 4)
        pure = amplitudes[:, :, 0]
        same(pure @ pure.T, spin_pure*(one-t) + spin_rotated*t)
        joint = amplitudes.transpose(0, 2, 1).reshape(16, 8)
        same(joint @ joint.T, choi_pure*(one-t) + choi_rotated*t)
        spin_with_reference_unread = amplitudes.reshape(4, 32)
        same(spin_with_reference_unread @ spin_with_reference_unread.T, spin)
        overlaps.append(overlap[0,0])
        state = new
    probabilities = []
    for outcome in range(4):
        columns = state.reshape(4,2,4,4)[:,:,outcome,:].reshape(8,4)
        effect = columns.T @ columns
        q = w[outcome//2]*w[outcome//2]*w[outcome%2]*w[outcome%2]
        same(effect, spin*q)
        probabilities.append(q)
    return overlaps, probabilities


def conditional_price(probs):
    registered = interval(2)
    coherent = interval(0)
    for q in probs:
        qi = enclosure(q)
        registered = minus(registered, enclosure(q*q))
        if qi[1] < Fraction(1,4):
            cost = interval(2)
        else:
            assert qi[0] > Fraction(1,4)
            cost = plus(root(qi), root(times(3, minus(1,qi))))
        coherent = plus(coherent, times(qi, cost))
    return registered, coherent


def main():
    totals, last, confirmation = [], [], []
    for prep in range(2):
        pos, probs = native_word(prep, 4)
        neg, other = native_word(prep, 3)
        assert probs == other
        assert pos[:10] == neg[:10]
        assert pos[10:] == list(reversed(neg[10:]))
        assert neg[10:] == neg[2:10]
        xi = 2*a*p if prep == 0 else 4*a*p*p*p*p
        assert pos[-1] == p + p*p*xi and neg[-1] == p - p*p*xi
        assert pos[10] == neg[-1] and neg[10] == pos[-1]
        total = interval(0)
        for h in pos:
            total = plus(total, trace_distance(h))
        totals.append(total)
        last.append((trace_distance(pos[-1]), trace_distance(neg[-1])))
        confirmation.append(conditional_price(probs))

    def secants(sequence):
        return [minus(hi,lo) for lo,hi in zip(*sequence)]
    total_secant = minus(totals[1],totals[0])
    inside(total_secant,'4.44925628','4.44925630')
    edge_p, edge_m = secants(last)
    inside(edge_p,'0.46231822','0.46231825')
    inside(edge_m,'-0.07242545','-0.07242542')
    rec, coh = secants(confirmation)
    inside(rec,'-0.52194618','-0.52194615')
    inside(coh,'-0.42522212','-0.42522209')

    z = Fraction(1,2**20)
    heat = Fraction(24,359*4**13)
    ds_plus = one-p*p
    x = 4*p*p-one
    ds_minus = p*p*x*x*x*x
    p12 = one
    for _ in range(12):
        p12 = p12*p
    ds_minus = ds_minus-p12
    def spectral_abs(ds):
        lower, upper = enclosure(ds)
        return 4*z*lower-heat, 4*z*upper/(1-z)+heat
    def ratio(positive, denominator):
        assert min(positive)>0 and min(denominator)>0
        return positive[0]/denominator[1], positive[1]/denominator[0]
    economic_ratio = ratio(edge_p, times(-1, edge_m))
    spectral_ratio = ratio(spectral_abs(ds_plus), spectral_abs(ds_minus))
    inside(economic_ratio,'6.38','6.39')
    inside(spectral_ratio,'23.04','23.53')
    for name, bounds in [('common trace secant',total_secant), ('edge18 plus',edge_p),
                         ('edge18 minus',edge_m), ('registered one edge',rec),
                         ('coherent one edge',coh), ('edge18 ratio', economic_ratio),
                         ('spectral ratio',spectral_ratio)]:
        print(name,tuple(round(float(x),12) for x in bounds))


if __name__=='__main__':
    main()
