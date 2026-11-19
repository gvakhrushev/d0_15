"""Exact rare-sector logical word and coherent versus registered secants.

This verifies ideal logical columns and finite-dimensional trace norms. It does
not compile the PVM into an actual complete NC1/factory/Book03 execution.
"""
from collections import Counter
from itertools import product
import json
import math
import numpy as np

# Exact arithmetic in Z[p], p^2=1-p.
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def mul(x,y):
    a,b=x; c,d=y
    return (a*c+b*d,a*d+b*c-b*d)
def power(x,n):
    y=(1,0)
    for _ in range(n): y=mul(y,x)
    return y

def operations(n):
    ops=[]
    def cx(c,t): ops.append(('CX',c,t))
    def tof(a,b,t): ops.append(('T',a,b,t))
    for i in range(n): cx('one',f'z{i}')
    tof('z0','z1','a0')
    for i in range(2,n): tof(f'a{i-2}',f'z{i}',f'a{i-1}')
    # E is available before touching selector k. R ^= E(1-H).
    cx(f'a{n-2}','R'); tof('H',f'a{n-2}','R')
    # A projective R instrument is inserted here, externally to this list.
    tof('k',f'a{n-2}','q')
    cx('H','U'); cx('q','U'); tof('H','q','U')
    tof('k',f'a{n-2}','q')
    for i in reversed(range(2,n)): tof(f'a{i-2}',f'z{i}',f'a{i-1}')
    tof('z0','z1','a0')
    for i in reversed(range(n)): cx('one',f'z{i}')
    return ops

def check_columns(n):
    ops=operations(n); counts=Counter(o[0] for o in ops)
    assert counts=={'T':2*n+2,'CX':2*n+3}
    num=0
    for h,z,k,u,r in product((0,1),range(1<<n),(0,1),(0,1),(0,1)):
        b={'one':1,'H':h,'k':k,'U':u,'R':r,'q':0}
        b.update({f'z{i}':(z>>i)&1 for i in range(n)})
        b.update({f'a{i}':0 for i in range(n-1)})
        for op in ops:
            if op[0]=='CX': b[op[2]]^=b[op[1]]
            else: b[op[3]]^=b[op[1]]&b[op[2]]
        rare=(1-h)*int(z==0)
        assert b['R']==(r^rare) and b['U']==(u^(h|(k*int(z==0))))
        assert b['H']==h and b['k']==k and b['one']==1 and b['q']==0
        assert all(b[f'z{i}']==((z>>i)&1) for i in range(n))
        assert all(b[f'a{i}']==0 for i in range(n-1))
        num+=1
    # Exhaustive exact event weight in Q(p).
    delta=(0,0)
    for h,z in product((0,1),range(1<<n)):
        if h==0 and z==0:
            wh=(0,1) if h==0 else (1,-1)
            zz=power((0,1),n-bin(z).count("1"))
            zo=power((1,-1),bin(z).count("1"))
            delta=add(delta,mul(wh,mul(zz,zo)))
    assert delta==power((0,1),n+1)
    return num

def check_dense(n):
    # Fixed selector omitted as a known external condition, all H/Z and U kept.
    p=(math.sqrt(5)-1)/2; delta=p**(n+1)
    v=[np.zeros((1<<(n+1))*2,dtype=float) for _ in range(2)]
    rare=np.zeros_like(v[0],dtype=bool)
    for h,z in product((0,1),range(1<<n)):
        w=(p if h==0 else p*p)*p**(n-bin(z).count("1"))*(p*p)**bin(z).count("1")
        for k in (0,1):
            u=h|(k*int(z==0)); idx=2*(h*(1<<n)+z)+u
            v[k][idx]=math.sqrt(w)
            rare[idx]=(h==0 and z==0)
    assert abs(np.dot(v[0],v[1])-(1-delta))<1e-13
    rho=[np.outer(x,x) for x in v]
    trace=lambda a: float(np.abs(np.linalg.eigvalsh(a)).sum())
    coherent=trace(rho[1]-rho[0]); expected=2*math.sqrt(2*delta-delta*delta)
    assert abs(coherent-expected)<1e-12
    # Full dephasing only of the one-bit rare predicate, not all H/Z.
    same=(rare[:,None]==rare[None,:]); cqd=[a*same for a in rho]
    measured=trace(cqd[1]-cqd[0]); assert abs(measured-2*delta)<1e-12
    # Trace H/Z: the registered and unregistered descriptor states agree
    # exactly (to numerical precision), including the conditional probabilities.
    for k in (0,1):
        red0=np.einsum('aiaj->ij',rho[k].reshape(-1,2,len(v[k])//2,2))
        red1=np.einsum('aiaj->ij',cqd[k].reshape(-1,2,len(v[k])//2,2))
        expected_u=p*p+k*delta
        assert np.allclose(red0,red1,atol=1e-13)
        assert np.allclose(red1,np.diag([1-expected_u,expected_u]),atol=1e-13)
        ev=np.linalg.eigvalsh(cqd[k]); ev=ev[ev>1e-12]
        assert np.allclose(sorted(ev),sorted([delta,1-delta]),atol=1e-12)
        assert abs(-sum(ev*np.log(ev))-(-delta*math.log(delta)-(1-delta)*math.log1p(-delta)))<1e-12
    # Readout of U alone does not in general remove seed coherence.
    uid=(np.arange(len(v[0]))%2); same_u=(uid[:,None]==uid[None,:])
    only_u=trace((rho[1]-rho[0])*same_u)
    assert only_u>2*delta+1e-8
    return {'coherent_trace_norm':coherent,'rare_registered_trace_norm':measured,
            'U_only_registered_trace_norm':only_u}

def check_union_word(m):
    # For R_0 ... R_(m-1), accumulate OR in m-1 clean wires.
    ops=[]
    for i in range(1,m):
        left='R0' if i==1 else f'S{i-1}'
        ops.extend([('CX',left,f'S{i}'),('CX',f'R{i}',f'S{i}'),
                    ('T',left,f'R{i}',f'S{i}')])
    def run(b, word):
        for op in word:
            if op[0]=='CX': b[op[2]] ^= b[op[1]]
            else: b[op[3]] ^= b[op[1]] & b[op[2]]
    for x in range(1<<m):
        b={f'R{i}':(x>>i)&1 for i in range(m)}
        b.update({f'S{i}':0 for i in range(1,m)})
        run(b,ops); flag=b[f'S{m-1}']
        assert flag==int(x!=0)
        # Measurement's classical outcome is copied outside the word.
        record=flag
        run(b,list(reversed(ops)))
        assert record==int(x!=0)
        assert all(b[f'R{i}']==((x>>i)&1) for i in range(m))
        assert all(b[f'S{i}']==0 for i in range(1,m))
    return {'input_columns':1<<m,'extra_clean_scratch':m-1,
            'Toffoli_compute_and_uncompute':2*(m-1),
            'CX_compute_and_uncompute':4*(m-1)}

def check_union_two_copies():
    n=2; p=(math.sqrt(5)-1)/2; delta=p**(n+1); d=(1<<(n+1))*2
    v=[np.zeros(d),np.zeros(d)]; rare=np.zeros(d,dtype=bool)
    for h,z in product((0,1),range(1<<n)):
        w=(p if h==0 else p*p)*p**(n-bin(z).count('1'))*(p*p)**bin(z).count('1')
        for k in (0,1):
            u=h|(k*int(z==0)); idx=2*(h*(1<<n)+z)+u
            v[k][idx]=math.sqrt(w); rare[idx]=(h==0 and z==0)
    a,b=np.kron(v[0],v[0]),np.kron(v[1],v[1])
    mask=(rare[:,None]|rare[None,:]).reshape(-1)
    q=1-(1-delta)**2
    assert np.allclose(a[~mask],b[~mask],atol=1e-14)
    assert abs(np.dot(a[mask],b[mask]))<1e-14
    assert abs(np.dot(a[mask],a[mask])-q)<1e-14
    assert abs(np.dot(b[mask],b[mask])-q)<1e-14
    # One union CQ dephasing has rank-two spectrum (1-q,q).
    assert abs(np.dot(a[~mask],a[~mask])-(1-q))<1e-14
    return {'m':2,'N':n,'union_probability':q,'registered_trace_norm':2*q}

def main():
    columns={str(n):check_columns(n) for n in range(2,9)}
    dense={str(n):check_dense(n) for n in (2,3,4)}
    union={str(m):check_union_word(m) for m in list(range(2,9))+[16]}
    union_dense=check_union_two_copies()
    p=(math.sqrt(5)-1)/2
    examples={}
    for n in (8,20,40):
        d=p**(n+1)
        # stable evaluations of 1-(1-d)^(2m) and 1-(1-d)^m
        m=16
        unregistered=2*math.sqrt(-math.expm1(2*m*math.log1p(-d)))
        registered=-2*math.expm1(m*math.log1p(-d))
        examples[str(n)]={'delta':d,'coherent_16_trace_norm':unregistered,
                          'registered_16_trace_norm':registered,
                          'registered_outcome_difference_over_delta_bound':registered/(2*d),
                          'coherent_trace_norm_over_delta':unregistered/d}
        assert registered/(2*d)<=m+1e-12
    print(json.dumps({'status':'PASS','complete_columns':columns,
      'logical_Toffoli':'2N+2','logical_CX':'2N+3',
      'additional_scratch_R_clean_zero':1,'dense_matrix_checks':dense,
      'union_OR_word_checks':union,'two_copy_union_sector_check':union_dense,
      'N_examples':examples,
      'single_coherent_trace_norm':'2 sqrt(2 delta - delta^2)',
      'm_copy_coherent_trace_norm':'2 sqrt(1 - (1-delta)^(2m))',
      'm_copy_rare_registered_trace_norm':'2 [1-(1-delta)^m]',
      'actual_NC1_PVM_and_full_clock_compiled':False,
      'actual_Book03_source_and_lift_identified':False,'GR_closed':False},indent=2))

if __name__=='__main__': main()
