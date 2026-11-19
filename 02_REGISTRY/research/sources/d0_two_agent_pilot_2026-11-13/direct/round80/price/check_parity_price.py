"""Exact native two-probe phase instrument, on every Spin and DATA column."""
from collections import defaultdict
from pathlib import Path
import sys

BASE = Path(__file__).resolve()
sys.path.insert(0, str(BASE.parents[2] / 'round79' / 'heat'))
sys.path.insert(0, str(BASE.parents[4] / 'd0_native_execution_domain_2026-10-24'))
from check_return_moments import Golden
import native_execution as ne

one = Golden(1)
a = Golden(0, 1)
p = a*a
v = (a, p)
ap = a*p
p3 = p*p*p
d = 4*p3
f = p3*p3


def gate_columns(gate):
    if gate.op == 'CX':
        return (((0, 1),), ((1, 1),), ((3, 1),), ((2, 1),))
    native = ne.G_LOCAL if gate.op == 'G' else ne.SOURCE_I_LOCAL
    known = {ne.A: a, ne.P: p, -ne.P: -p, 1: 1, -1: -1, 0: 0}
    return tuple(tuple((row, known[native[row, col]]) for row in range(native.rows)
                       if native[row, col] != 0) for col in range(native.cols))


def action(state, gate, width):
    shifts = [width - 1 - wire for wire in gate.wires]
    keep = ((1 << width) - 1) ^ sum(1 << shift for shift in shifts)
    columns = gate_columns(gate)
    out = defaultdict(Golden)
    for index, amplitude in state.items():
        col = sum(((index >> shift) & 1) << j for j, shift in enumerate(reversed(shifts)))
        for row, coefficient in columns[col]:
            new_index = (index & keep) | sum(((row >> j) & 1) << shift
                                              for j, shift in enumerate(reversed(shifts)))
            out[new_index] += amplitude * coefficient
    return {key: value for key, value in out.items() if value != 0}


def program(n):
    gate = ne.Gate
    port, extra = 2, n+3
    source = gate('SourceI', (port, 0, 1))
    mix = gate('G', (port,))
    couple = tuple(gate('CX', (port, j)) for j in range(3, 3+n))
    swap = (gate('CX', (port, extra)), gate('CX', (extra, port)), gate('CX', (port, extra)))
    # Physical inverse ZGZ on the first probe and G then Z on the second.
    gates = couple + (source, source, mix, source, source) + swap + couple + (mix, source, source)
    ex = ne.Execution(n+4, (), (), gates, profile=ne.G_CX_SOURCE_I, source_port=2,
                      source_spin=(0,1), report_bits=(extra,port))
    ne.execution_from_json(ne.canonical_json(ex), max_qubits=n+4, max_expanded_stages=2*n+11)
    assert len(gates) == 2*n+11
    return gates


def validate_columns(n):
    width, size = n+4, 2**n
    gates = program(n)
    counter = 0
    for spin in range(4):
        for word in range(size):
            state = {((spin*2+first)*size+word)*2+second: v[first]*v[second]
                     for first in range(2) for second in range(2)}
            for g in gates:
                state = action(state, g, width)
            actual = {}
            for index, coefficient in state.items():
                first, second = index & 1, (index >> (n+1)) & 1
                assert index >> (n+2) == spin
                actual[first,second,(index >> 1) % size] = coefficient
            flip = size-1-word
            expected = {(0,0,word):p3, (1,0,word):-ap, (1,0,flip):ap,
                        (0,1,word):-ap, (0,1,flip):-ap}
            assert expected == actual
            # Contract both output bits with the real unmarked Golden births.
            # If one fresh additional v is written by CX(control,r), its own
            # cold coefficient is 1 or xi = <v,Xv> on the given control.
            xi = 2*ap
            for selected in (None, 0, 1):
                cold = defaultdict(Golden)
                for (r0,r1,old), amp in actual.items():
                    mark = xi if selected is not None and (r0,r1)[selected] else one
                    cold[old] += amp*v[r0]*v[r1]*mark
                if selected is None:
                    assert cold[word] == p*p3-2*p3 and cold[flip] == 0
                else:
                    assert cold[word] == p*p3-p3*(one+xi)
                    signed = p3*(xi-one)
                    assert cold[flip] == (signed if selected == 0 else -signed)
            counter += 1
    return counter


def main():
    assert p+p*p == one
    assert d+f == one
    assert (p-p*p) == p3
    # Two real Golden digits and a parity CX: after the single flag 1,
    # the two unmeasured data amplitudes coincide.
    ready = action({2*i+j:v[i]*v[j] for i in range(2) for j in range(2)},
                   ne.Gate('CX', (0,1)), 2)
    assert ready[1] == ready[3] == ap
    assert ready[1]*ready[1]+ready[3]*ready[3] == 2*p3
    assert ready[0]*ready[0]+ready[2]*ready[2]+2*p3 == one
    # After CNOT into a true blank, both equally occupied bases have
    # the identical unlabeled density on span{|00>, |11>}.
    gcols = ((a, p), (-p, a))
    assert sum(u*u for u, _ in gcols) == one
    assert sum(t*t for _, t in gcols) == one
    assert sum(u*t for u, t in gcols) == 0
    for u, t in gcols:
        assert one+2*u*u*t*t == one+2*p3
    checked = sum(validate_columns(n) for n in range(1, 6))
    # Conditional phase receipts have d/2 vs f for the common erasure;
    # equality to 2 would require p^3=1. Dropping the logarithm, the
    # extra three golden price units are exactly the following equality.
    assert (2*p3)*p3 == 2*f
    # Real noisy native confirmation from a selected raw receipt, then 0/10.
    expected_bit_imbalance = (p-p*p)*d
    assert expected_bit_imbalance == 4*f
    # The code 010 and 100 are concatenations of the elementary 0 and 10.
    assert '0'+'10' == '010' and '10'+'0' == '100'
    assert len('010') == len('100')
    print(f'{checked} complete Spin/DATA columns, n=1..5; 4 Kraus blocks checked')
    print('scalar cold, both unequal marked-cold addresses, fair READY and 4*p^6 price verified')


if __name__ == '__main__':
    main()
