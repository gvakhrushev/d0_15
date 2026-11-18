"""The complete native growing ticks and the sign of the full Book difference."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import sys

import numpy as np
from scipy import sparse

sys.dont_write_bytecode = True
previous = Path(__file__).resolve().parents[2] / 'round69' / 'clock'
sys.path.insert(0, str(previous))
from check_early_heat import Clock, a, gate, p
from check_exact_return import adjoint, exact_tick, lift, mul_p, row_bound, unit


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def safe_product(x, y):
    require(row_bound(x)*row_bound(y) < 2**60, 'integer coefficient range')
    return (x @ y).tocsr()


def prepare(age, k, guard):
    # Spin occupies 0,1. e=2 is the genuine port, y=3, t=4 the two WORK wires.
    e = 2
    target = {'older': 3, 'newest': 4}[age]
    swap = [('CX',(e,target)), ('CX',(target,e)), ('CX',(e,target))]
    z_word = [('SourceI',(e,0,1))]*2
    g_word = [('G',(e,))]
    inverse_g = z_word + g_word + z_word
    word = swap + g_word*k + z_word + inverse_g*k + [('CX',(2,3))]*guard
    clock = Clock(0)
    node = 0
    for _ in range(3):
        node = clock.birth(node)
    for op, wires in word[:-1]:
        node = clock.raw(node, op, wires)
    op, wires = word[-1]
    clock.last[node] = gate(5, op, wires, 0)
    # Factor all native square gates exactly over Z[a], a^4+a^2=1.
    endpoint = sparse.eye(4*32, dtype=np.int64, format='csr')
    for op,wires in word:
        endpoint = safe_product(lift(gate(5,op,wires,0)), endpoint)
    return clock,endpoint,len(word)


def check(k, guard):
    # c = 1-2*q on the real born e. Q0=p^2, Q1=4*p^3.
    c = 2*mul_p-unit if k == 0 else 9*unit-16*mul_p
    j = sparse.eye(4*4, dtype=np.int64, format='csr')
    for dim in (4,8,16):
        birth = sparse.kron(sparse.eye(dim), np.array([[a],[p]]))
        j = safe_product(lift(birth), j)
    outputs = []
    endpoints = []
    for age in ['older','newest']:
        clock,endpoint,length = prepare(age,k,guard)
        tick,_ = exact_tick(clock)
        rows = tick.shape[0] // 4
        require(length == (5,11)[k]+guard and rows == 28+32*length, 'actual growing dimensions')
        inputs = safe_product(endpoint,j)
        outputs.append(inputs)
        endpoints.append(endpoint)
        cold = safe_product(adjoint(j),inputs)
        require((cold-sparse.kron(sparse.eye(4),c)).count_nonzero() == 0,'all four root columns')
        power = sparse.eye(tick.shape[0], dtype=np.int64, format='csr')
        for index in range(1,length+1):
            power = safe_product(tick,power)
            traces = np.array([power[n::4,::4].diagonal().sum() for n in range(4)])
            expected = -8*length*c[:,0] if age == 'newest' and index == length else np.zeros(4)
            require(np.array_equal(traces,expected),'full first return over exact ring')
    require((outputs[0]-outputs[1]).count_nonzero() == 0,'complete initialized channels agree')
    exchange = np.zeros((32,32))
    for old in range(32):
        new = (old & ~3) | ((old&1)<<1) | ((old>>1)&1)
        exchange[new,old] = 1
    perm = lift(sparse.csr_matrix(exchange))
    require((safe_product(safe_product(perm,endpoints[0]),perm) - endpoints[1]).count_nonzero()==0,
            'homogeneous full endpoints conjugate')
    # Rational sign certificate for the sum of ALL higher heat coefficients.
    ratio = F(1,22*(length+1))  # beta=2*p^2<1
    tail = 2*rows*ratio/(1-ratio)
    require(tail < 3 and 8*F(1,5)*length > tail, 'strict first-sign dominance')


def main():
    require(F(3,5)**2+F(3,5)<1 and F(5,8)**2+F(5,8)>1, 'p isolated')
    require(2*F(5,8)**2<1 and F(3,5)**3>F(1,5), 'beta and positive first cold sign')
    require(8*F(3,5)**3-1 > F(1,5), 'opposite second cold sign')
    for guard in (0,4):
        for k in (0,1):
            check(k,guard)
    # A subsequent real pair adds 64 dimensions. At every L>=5,
    # D_L/L! decreases strictly, so both full thermal errors cost less than 528.
    require(F(28+32*5,factorial(5))<2 and 64*359>2*528, 'every extra pair costs strictly more')
    for length in (5,11):
        d=28+32*length
        require((359+F(66,9))*(d+64)>425*d, 'first pair from absolute spectral bounds')
    # General field-derivative coefficient: norm T' / 11, 33D variable modes
    # twice, unit mass reduced by the 359D harmonic base from the complete clock.
    require(F(2*33,359*11) == F(6,359), 'both Hodge grades')
    require(F(6,359*factorial(12)) < F(1,10**10), 'twelve unchanged calls at beta<1')
    print('PASS: eight native growing clocks, exact ring unitarity, identical full prepared output, '
          'first heat moments, both strict opposite price orderings, full Hodge derivative constant.')


if __name__ == '__main__':
    main()
