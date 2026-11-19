"""Paid finite Golden descriptor secants for the two-component CAR catalogue.

The exact logical words and finite field laws are checked; input selector
preparation, actual Book03 tariffs, complete failure clock and a uniform
physical source lift remain separate obligations.
"""
from fractions import Fraction
from itertools import product
from collections import Counter
import json
import math
import numpy as np
import sympy as sp
from mpmath import iv


def program(n):
    assert n >= 2
    ops=[]
    def cx(c,t):ops.append(('CX',c,t))
    def tof(a,b,t):ops.append(('T',a,b,t))
    for i in range(n):cx('one',f'z{i}')
    tof('z0','z1','a0')
    for i in range(2,n):tof(f'a{i-2}',f'z{i}',f'a{i-1}')
    tof('k',f'a{n-2}','q')
    cx('H','U');cx('q','U');tof('H','q','U')
    tof('k',f'a{n-2}','q')
    for i in reversed(range(2,n)):tof(f'a{i-2}',f'z{i}',f'a{i-1}')
    tof('z0','z1','a0')
    for i in reversed(range(n)):cx('one',f'z{i}')
    return ops


def add(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y):
    # (a+b p)(c+d p), p^2=1-p.
    a,b=x;c,d=y
    return (a*c+b*d,a*d+b*c-b*d)
def power(x,n):
    y=(1,0)
    for _ in range(n):y=mul(y,x)
    return y


def check_columns(n):
    # All controls, H/Z and both U columns with zero-initialized scratch.
    count=2**(n+3); ix=np.arange(count,dtype=np.uint32)
    desc=ix&1; H=(ix>>1)&1; Z=(ix>>2)&((1<<n)-1); U0=(ix>>(n+2))&1
    bits={'k':desc.astype(np.uint8),'H':H.astype(np.uint8),
          'one':np.ones(count,dtype=np.uint8),'U':U0.astype(np.uint8).copy(),
          'q':np.zeros(count,dtype=np.uint8)}
    bits.update({f'z{i}':((Z>>i)&1).astype(np.uint8) for i in range(n)})
    bits.update({f'a{i}':np.zeros(count,dtype=np.uint8) for i in range(n-1)})
    ops=program(n)
    for op in ops:
        if op[0]=='CX':bits[op[2]]^=bits[op[1]]
        else:bits[op[3]]^=bits[op[1]]&bits[op[2]]
    expected=U0 ^ (H | (desc & (Z==0)))
    assert np.array_equal(bits['U'],expected)
    assert np.array_equal(bits['k'],desc) and np.array_equal(bits['H'],H)
    for i in range(n):assert np.array_equal(bits[f'z{i}'],(Z>>i)&1)
    assert bits['one'].all() and not bits['q'].any()
    assert all(not bits[f'a{i}'].any() for i in range(n-1))
    # Exact Q(p) probability of U=1 for each fixed selector.
    pp=(0,1); rr=(1,-1)
    probs=[]
    for k in (0,1):
        total=(0,0)
        for h in (0,1):
            wh=rr if h else pp
            for z in range(2**n):
                if h or (k and z==0):
                    ones=bin(z).count('1')
                    weight=mul(wh,mul(power(rr,ones),power(pp,n-ones)))
                    total=add(total,weight)
        target=rr if k==0 else add(rr,power(pp,n+1))
        assert total==target
        probs.append(total)
    counts=Counter(op[0] for op in ops)
    assert counts=={'T':2*n+1,'CX':2*n+2}
    return count, counts


def caps(n,desc_count=32):
    T=2*n+1;L=1
    while Fraction(4,5)**L * (28*desc_count*T) > 1:L+=1
    assert Fraction(4,5)**L <= Fraction(1,28*desc_count*T)
    return T,L


def main():
    checked={}
    for n in range(2,9):
        count,counts=check_columns(n)
        checked[str(n)]={'complete_logical_columns':count,'T':counts['T'],'CX':counts['CX']}
    p=(sp.sqrt(5)-1)/2;r=p**2
    s,t,d=sp.symbols('s t d',real=True)
    B=lambda x:1-2*x+2*x*x
    Q=-((B(s)-s*s)*B(t)+t*t*B(s))
    Q0=sp.simplify(Q.subs({s:r,t:r}))
    Qs=sp.simplify(sp.diff(Q,s).subs({s:r,t:r}))
    Qt=sp.simplify(sp.diff(Q,t).subs({s:r,t:r}))
    Cs=sp.simplify(((Q.subs({s:r+d,t:r})-Q0)/d-Qs)/d)
    Ct=sp.simplify(((Q.subs({s:r,t:r+d})-Q0)/d-Qt)/d)
    assert sp.simplify(Q0-(40*p-25))==0
    assert sp.simplify(Qs-(40*p-24))==0
    assert sp.simplify(Qt-(32*p-20))==0
    assert sp.simplify(Cs-(10*p-7))==0
    assert sp.simplify(Ct-(6*p-5))==0
    diag=sp.simplify(2*B(r)); cross=sp.simplify((2*r-1)**2)
    det=sp.simplify(diag*diag-cross*cross)
    assert sp.simplify(det-(11-16*p))==0 and float(det)>0
    # For every n>=2, d=p^(n+1) <= p^3; derivative-slope signs
    # are monotone in d because Cs,Ct<0. Endpoints certified exactly.
    assert float(Qs+Cs*p**3)>0 and float(Qt)<0

    iv.dps=100;one=iv.mpf(1);pp=(iv.sqrt(5)-one)/2
    assert (one-2*pp**3)<iv.mpf('0.8')
    assert (one-4*pp**3)<iv.mpf('0.8')
    assert (one-16*pp**9)<iv.mpf('0.8')
    n=8;T,L=caps(n);Bcount=32
    assert T==17 and L==44
    b0=one-(one-2*pp**3)**L;b2=one-(one-4*pp**3)**L
    b3=one-(one-16*pp**9)**L;beta=b0**2*b2**4*b3
    P_h=one-pp**40
    assert P_h>iv.mpf('2')/3
    four=P_h*beta**(4*T);all32=P_h*beta**(Bcount*T)
    assert four>iv.mpf('.99793') and all32>iv.mpf('.98356')
    assert all32>P_h*iv.mpf('0.75')
    delta=pp**(n+1)
    # The interval-to-float output is not asserted as a proof of source/lift.
    ds=(40*pp-24)+(10*pp-7)*delta
    dt=(32*pp-20)+(6*pp-5)*delta
    assert ds>0 and dt<0
    # Only the 32 explicit H/Z and clean work births plus <=80 births for
    # the separate known-one attempt. The parity-plus/Toffoli factories,
    # their LC1 readers, routing and failure controllers are not counted.
    base_births=Bcount*2*(n+1)+80
    print(json.dumps({
      'status':'PASS','metric_signature':'+---',
      'program_columns_checked':checked,
      'seed_word_T_formula':'2N+1','seed_word_CX_formula':'2N+2',
      'seed_initial_clean_ancilla_formula':'N+1, including U',
      'seed_fresh_canonical_coins_formula':'N+1',
      'logical_word_preserves_selector_and_all_coins':True,
      'conditional_oldRIGHT_identity_by_tensor_extension':True,
      'finite_p0':'p^2','finite_p1':'p^2+p^(N+1)',
      'finite_delta':'p^(N+1)','example_N':n,'example_delta_interval':str(delta),
      'uniform_metric_Q_at_base':'40p-25',
      'secant_s_over_2A2delta':'40p-24+(10p-7)delta',
      'secant_t_over_2A2delta':'32p-20+(6p-5)delta',
      'secant_s_example_interval':str(ds),'secant_t_example_interval':str(dt),
      'field_tangent_gram_determinant_over_A4':'11-16p',
      'matter_copies_per_ten_sign_report':16,'independent_seed_modules_per_report':Bcount,
      'example_Toffoli_per_seed':T,'example_factory_cap':L,
      'example_success_four_seeds_conditional':str(four),
      'example_success_32_seeds_conditional':str(all32),
      'asymptotic_cap': 'smallest L with (4/5)^L <= 1/(28*32*(2N+1))',
      'uniform_32_seed_success_lower_bound': '3(1-p^40)/4 > 1/2',
      'example_32_seed_base_births_upper_excluding_factories':base_births,
      'physical_flags_and_codes_accounted_by_later_clock':False,
      'general_field_rank_or_full_Book03_source_identified':False,
      'uniform_lift_or_complete_Book_cost_proved':False,
      'GR_closed':False,
    },indent=2,sort_keys=True))


if __name__=='__main__':main()
