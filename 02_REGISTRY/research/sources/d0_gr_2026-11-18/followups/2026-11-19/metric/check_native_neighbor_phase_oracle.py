"""Literal reversible L=4 neighbor equality phase oracle, exhaustive inputs."""
import json
from collections import Counter
from itertools import product
import numpy as np
from mpmath import iv

# Register x/y are immutable data; t,d are 8 fresh bits, a 7 fresh bits;
# z is a paid known 1. port is arbitrary and restored. gate list is executable.
def program(r):
    ops=[]
    def cx(a,b): ops.append(('cx',a,b))
    def ccx(a,b,c): ops.append(('ccx',a,b,c))
    for i in range(8): cx(f'x{i}',f't{i}')
    if r is not None:
        cx(f't{2*r}',f't{2*r+1}')
        cx('z',f't{2*r}')
    for i in range(8):
        cx(f't{i}',f'd{i}');cx(f'y{i}',f'd{i}');cx('z',f'd{i}')
    ccx('d0','d1','a0')
    for i in range(2,8): ccx(f'a{i-2}',f'd{i}',f'a{i-1}')
    fwd=ops.copy()
    # Route target a6 to full SourceI port, apply SourceI twice, restore.
    cx('a6','port');cx('port','a6');cx('a6','port')
    ops.append(('sourcei',));ops.append(('sourcei',))
    cx('a6','port');cx('port','a6');cx('a6','port')
    ops.extend(reversed(fwd))
    return ops

def run(r,port_value):
    xy=np.arange(256*256,dtype=np.uint32)
    x=xy>>8;y=xy&255
    bits={f'x{i}':((x>>i)&1).astype(np.uint8) for i in range(8)}
    bits.update({f'y{i}':((y>>i)&1).astype(np.uint8) for i in range(8)})
    bits.update({f'{name}{i}':np.zeros(len(xy),dtype=np.uint8) for name,n in [('t',8),('d',8),('a',7)] for i in range(n)})
    bits['z']=np.ones(len(xy),dtype=np.uint8)
    bits['port']=np.full(len(xy),port_value,dtype=np.uint8)
    sign=np.ones(len(xy),dtype=np.int8)
    pending=False
    for op in program(r):
        if op[0]=='cx': bits[op[2]] ^= bits[op[1]]
        elif op[0]=='ccx': bits[op[3]] ^= bits[op[1]] & bits[op[2]]
        else:
            # Full 8x8 SourceI squared separately certified below; these two
            # adjacent calls implement (-1)^port and identity on all Spin.
            if pending: sign *= (1-2*bits['port'].astype(np.int8));pending=False
            else: pending=True
    assert not pending
    for i in range(8):
        assert np.all(bits[f'x{i}']==((x>>i)&1))
        assert np.all(bits[f'y{i}']==((y>>i)&1))
    for n,k in [('t',8),('d',8),('a',7)]:
        for i in range(k): assert not bits[f'{n}{i}'].any()
    assert np.all(bits['port']==port_value) and np.all(bits['z']==1)
    expected=x.copy()
    if r is not None:
        shift=2*r; coord=(x>>shift)&3
        expected=(x & ~(np.uint32(3)<<np.uint32(shift))) | (((coord+1)&3)<<shift)
    assert np.array_equal(sign,np.where(y==expected,-1,1))
    return int(np.count_nonzero(sign==-1))

def source_full_matrix():
    li=np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]],dtype=np.int8)
    src=np.zeros((8,8),dtype=np.int8);src[:4,:4]=np.eye(4,dtype=np.int8);src[4:,4:]=li
    assert np.array_equal(src@src,np.diag([1]*4+[-1]*4))
    # Explicit 3-CX SWAP around the two SourceI calls, all port,a6,Spin columns.
    swap=np.zeros((16,16),dtype=np.int8);big=np.zeros((16,16),dtype=np.int8)
    expected=np.zeros((16,16),dtype=np.int8)
    for p,a,s in product(range(2),range(2),range(4)):
        j=(p*2+a)*4+s;swap[(a*2+p)*4+s,j]=1
        expected[j,j]=(-1)**a
        for t in range(4): big[(p*2+a)*4+t,j]=src[p*4+t,p*4+s]
    assert np.array_equal(swap@big@big@swap,expected)

def main():
    source_full_matrix();results=[]
    for r in (None,0,1,2,3):
        ops=program(r);counts=Counter(o[0] for o in ops)
        assert counts['ccx']==14 and counts['sourcei']==2
        assert counts['cx']==(70 if r is None else 74)
        for port in (0,1): assert run(r,port)==256
        results.append(dict(neighbor='zero' if r is None else f'e{r}',CX=counts['cx'],Toffoli=14,SourceI=2,
                            site_y_pairs=65536,port_basis_values=2,negative_phase_pairs=256))
    iv.dps=60;p=(iv.sqrt(5)-1)/2;b2=1-p**384;b3=1-(1-16*p**9)**64
    beta=b2**6*b3;all_to=beta**14;full=(1-p**40)*all_to
    births=14*(26*64+2)+80+23
    assert births==23427
    print(json.dumps(dict(status='PASS',fresh_zero_bits=23,known_one_bits=1,
        cases=results,full_sourcei_and_spin_matrix_columns=16,
        inverse_returns_all_scratch_and_data=True,oldRIGHT_identity_by_tensor_extension=True,
        single_Toffoli_success=str(beta),all_14_Toffoli_success=str(all_to),
        fourier_960_equality_oracles_shared_known_one_success=str((1-p**40)*beta**(14*960)),
        fourier_960_equality_oracles_independent_known_one_success=str(full**960),
        fourier_960_scope='80 Fourier copies times 12 equalities; excludes 1260 Choi projectors and all other devices',
        known_one_and_14_Toffoli_success=str(full),max_listed_births=births,
        scratch_preparation=dict(G=23,CX=46),
        failure_log='first failure at each of 14 Toffolis or known-one failure; no assumption of input restoration on failure',
        ready_and_address_oracle_compiled=False,blank_reflection_compiled=False,
        full_source_ready_and_book03_cost_proved=False),indent=2,sort_keys=True))

if __name__=='__main__':main()
