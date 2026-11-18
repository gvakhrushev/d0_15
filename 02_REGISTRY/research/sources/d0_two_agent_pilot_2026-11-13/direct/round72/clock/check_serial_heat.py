"""Actual SER1 resets, the newest birth trace, and the silent early-field moments."""
from collections import Counter
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import sys

import numpy as np
from scipy import sparse

sys.dont_write_bytecode = True
previous = Path(__file__).resolve().parents[2] / 'round71' / 'clock'
sys.path.insert(0, str(previous))
from check_chronology import safe_product, require
from check_early_heat import Clock, gate
from check_exact_return import lift


E, R, C, T = 2, 3, 4, 5
source = ('SourceI',(E,0,1))
port_z = [source]*2
cx = lambda left,right: ('CX',(left,right))


def reset(wire, twisted):
    fwd = cx(E,wire)
    rev = cx(wire,E)
    swap = [fwd,rev,fwd]
    z = swap + port_z + swap
    # Three repeats of rev on each side still compute and undo the parity.
    parity = [rev]*3 + port_z + [rev]*3
    return z + [('G',(wire,))] + (parity if twisted else z)


def port_rotation(n):
    # Two G and four genuine SourceI for n in {-2,0,2}.
    return [('G',(E,))]*(1+n//2) + port_z + [('G',(E,))]*(1-n//2) + port_z


def states(twisted, field=0, reverse=None):
    # The stars below reflect square gates. Every birth remains in the clock.
    if reverse is None:
        reverse = -field
    cursor = reset(C,twisted)
    tail = reset(T,twisted)
    steps = ([None] + port_rotation(field) + [None] + reset(R,False) + [cx(E,R)] +
             port_z + port_rotation(reverse) + [None] + cursor + [cx(R,C)] +
             [None] + tail + [cx(R,C)])
    writer = [None]+reset(R,False)+[cx(E,R), None]+cursor+[cx(R,C),None]+tail+[cx(R,C)]
    inventory = Counter('birth' if step is None else step[0] for step in writer)
    require(inventory=={'birth':3,'G':3,'SourceI':12,'CX':39} and len(writer)==57,
            'exact published chronological inventory')
    return steps


def endpoint(steps, bits):
    result = sparse.eye(4*2**bits,format='csr',dtype=np.int64)
    for step in steps:
        if step is not None:
            op,wires = step
            result=safe_product(lift(gate(bits,op,wires,0)),result)
    return result


def moments(steps, degree=38, bits=6):
    # Exact homomorphism Z[a] -> F_11 (a->5, p=a^2->3).
    clock=Clock(11)
    node=0
    for step in steps[:-1]:
        node=clock.birth(node) if step is None else clock.raw(node,*step)
    op,wires=steps[-1]
    clock.last[node]=gate(bits,op,wires,11)
    tick,_=clock.close()  # also checks full T^*T, including the physical closure.
    current=sparse.eye(tick.shape[0],format='csr',dtype=np.int64)
    result=[]
    for _ in range(degree):
        current=(tick@current).tocsr()
        current.data %=11
        current.eliminate_zeros()
        result.append(int(current.diagonal().sum())%11)
    return result


def spectator_states(n):
    # A_f=A_b on y, living before the writer. The actual fixed port is e.
    y,r,c,t=3,4,5,6
    swap=[cx(E,y),cx(y,E),cx(E,y)]
    z_y=swap+port_z+swap
    def rotate(k):
        return [('G',(y,))]*(1+k//2)+z_y+[('G',(y,))]*(1-k//2)+z_y
    return ([None,None]+rotate(n)+[None]+reset(r,False)+[cx(E,r)]+port_z+rotate(-n)+
            [None]+reset(c,False)+[cx(r,c),None]+reset(t,False)+[cx(r,c)])


def main():
    e_phase=endpoint(port_z,6)
    ordinary=states(False)
    alternate=states(True)
    for wire in (C,T):
        macro=endpoint(reset(wire,False),6)
        other=endpoint(reset(wire,True),6)
        require((other-safe_product(e_phase,macro)).count_nonzero()==0,'twisted reset on every input')
    require((endpoint(ordinary,6)-endpoint(alternate,6)).count_nonzero()==0,'all-column equality')
    for twisted in (False,True):
        low=moments(states(twisted,0))
        high=moments(states(twisted,2))
        require(low==high,'38 shortest moments independent of earlier actual preparation')
        require(not any(low[:17]) and low[17] == (0 if twisted else (18*5*16)%11),'youngest full wrap')
    # Independent real e-field forwards and backwards, L_r=64 for these
    # six-call real port slots. The first varying coefficient sees only A_b.
    general_age=17+1+2+6+38
    base=moments(states(False,0,0),general_age)
    forward=moments(states(False,2,0),general_age)
    backward=moments(states(False,0,-2),general_age)
    require(base==forward and base[:-1]==backward[:-1], 'full forward is invisible at the r-age')
    # p Tr[(A_b*-I)(a Pi_0+p Pi_1)], exact residual for four old Spin columns.
    expected=general_age*3*4*(5+3)*(5-1)
    require((backward[-1]-base[-1]-expected)%11==0 and expected%11!=0,
            'absolute reverse-sector trace for the original serial writer')
    spectator0,spectator2=spectator_states(0),spectator_states(2)
    require((endpoint(spectator0,7)-endpoint(spectator2,7)).count_nonzero()==0,
            'matched native bank inputs have identical entire terminal square maps')
    age=17+1+2+18+38
    d=16
    low=moments(spectator0,age,bits=7)
    high=moments(spectator2,age,bits=7)
    require(low[:-1]==high[:-1], 'every moment younger than the r return, including two-wrap paths')
    # p=3, a=5, cos(2*theta)=2p-1=5 mod 11, and division by two is 6.
    expected=age*d*3*(5+3)*6*(5-1)
    require((high[-1]-low[-1]-expected)%11==0 and expected%11!=0,'true r-return coefficient')
    # Rigorous bounds for every previously assembled full bank and exact beta.
    # The late-field horizon starts strictly AFTER the last earlier square step.
    early=F(352,359)*F(2,55)**39/factorial(38)
    require(early<F(138,10**103),'geometric thermal sensitivity below 1.38e-101')
    x=F(2,55)
    # Only four square instructions differ at each of the two reset sites.
    finite_tail=24*x*2/18
    require(finite_tail<F(1,10) and F(3,8)-finite_tail>F(1,4),'strict finite sign without long padding')
    tangent_tail=3*x*2/age
    require(108*x*2/age<F(3,5)**3*(F(3,4)+F(3,5)),'two literal equal-endpoint bank words strictly differ in full heat')
    native_slope=F(3,5)**2*(F(3,5)+F(3,4)*F(3,5))
    require(native_slope-tangent_tail>F(1,3),'nonzero first thermal derivative at a native gate centre')
    print('PASS: unchanged 57-call inventory, exact native reset and full endpoint, original and twisted '
          'growing clocks, all 38 field-insensitive moments, signed finite heat and the diagnostic first jet.')


if __name__=='__main__':
    main()
