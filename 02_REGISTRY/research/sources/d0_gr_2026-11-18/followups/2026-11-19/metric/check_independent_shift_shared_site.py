"""Native L4 shifted equality, shared-site twirl, and genuine local-report gap."""
from itertools import product
from collections import Counter
from fractions import Fraction
import json, math
import numpy as np
import mpmath as mp


def need(a,msg):
    if not a: raise AssertionError(msg)


def add_mod4(x,t):
    result=np.zeros_like(x,dtype=np.uint32)
    for j in range(4):result|=((((x>>(2*j))&3)+((t>>(2*j))&3))&3)<<(2*j)
    return result


def prefix(r):
    ops=[]
    def cx(a,b):ops.append(('cx',a,b))
    def ccx(a,b,c):ops.append(('ccx',a,b,c))
    # X and independently generated shift U stay untouched.
    for i in range(8):cx(f'x{i}',f't{i}');cx(f'u{i}',f't{i}')
    for j in range(4):ccx(f'x{2*j}',f'u{2*j}',f't{2*j+1}')
    if r is not None:
        cx(f't{2*r}',f't{2*r+1}');cx('h',f't{2*r}')
    for i in range(8):cx(f't{i}',f'd{i}');cx(f'y{i}',f'd{i}');cx('h',f'd{i}')
    ccx('d0','d1','a0')
    for i in range(2,8):ccx(f'a{i-2}',f'd{i}',f'a{i-1}')
    return ops


def simulate(r,x,u,y):
    N=len(x);bits={}
    for n,v in [('x',x),('u',u),('y',y)]:
        bits.update({f'{n}{i}':((v>>i)&1).astype(np.uint8) for i in range(8)})
    for n,k in [('t',8),('d',8),('a',7)]:bits.update({f'{n}{i}':np.zeros(N,dtype=np.uint8) for i in range(k)})
    bits['h']=np.ones(N,dtype=np.uint8)
    def apply(op):
        if op[0]=='cx':bits[op[2]]^=bits[op[1]]
        else:bits[op[3]]^=bits[op[1]]&bits[op[2]]
    ops=prefix(r)
    for op in ops:apply(op)
    a=bits['a6'].copy(); exp=add_mod4(x,u)
    if r is not None:
        digit=(exp>>(2*r))&3
        exp=(exp&~(np.uint32(3)<<(2*r)))|(((digit+1)&3)<<(2*r))
    need(np.array_equal(a,(y==exp).astype(np.uint8)),'shifted comparator')
    for op in reversed(ops):apply(op)
    for n,k in [('t',8),('d',8),('a',7)]:
        for i in range(k):need(not bits[f'{n}{i}'].any(),'scratch restored')
    for n,v in [('x',x),('u',u),('y',y)]:
        for i in range(8):need(np.array_equal(bits[f'{n}{i}'],(v>>i)&1),'old data restored')
    counts=Counter(op[0] for op in ops)
    need(counts['ccx']==11 and counts['cx']==(40 if r is None else 42),'literal count')
    return {'sampled_columns':N,'compute_uncompute_Toffoli':22,
            'compute_uncompute_CX':80 if r is None else 84,'NC1_extra_birth_G_CX':[1,1,2]}


def algebra_checks():
    # Exact translation of all 256 X x all 256 shifts: bijection separately
    # for every X and every U. This plus every (shifted X,Y) comparator column
    # proves the combined 2^24 truth table without allocating it.
    pair=np.arange(65536,dtype=np.uint32);X=pair>>8;U=pair&255
    T=add_mod4(X,U)
    for xx in range(256):need(len(set(map(int,T[X==xx])))==256,'each X uniform translation')
    for uu in range(256):need(len(set(map(int,T[U==uu])))==256,'each shift permutation')
    cases={}
    for r in (None,0,1,2,3):
        z=T.copy()
        if r is not None:
            digit=(z>>(2*r))&3;z=(z&~(np.uint32(3)<<(2*r)))|(((digit+1)&3)<<(2*r))
        # matching and deliberately different Y for every X,U pair
        first=simulate(r,X,U,z)
        bad=z^np.uint32(1);simulate(r,X,U,bad)
        # Every target/Y pair on raw comparator; canonical X=0,U=z.
        zz=pair>>8;Y=pair&255
        simulate(r,np.zeros_like(zz),zz,Y)
        cases['zero' if r is None else f'e{r}']=first
    return cases


def correlation_checks():
    # The locally bilinear original L4 field pair d=00,e=01 on 256 sites.
    # Lexicographic site->byte uses coordinate j at bit 2j.
    unit=((1,0),(0,1),(-1,0),(0,-1))
    def psi(u,v,x):
        q=[(x>>(2*i))&3 for i in range(4)]
        return unit[(q[1]+u*q[0]+v*q[2])%4]
    field=[]
    for x in range(256):
        f=Fraction(0)
        for mu in range(4):
            q=(x>>(2*mu))&3;y=(x&~(3<<(2*mu)))|(((q+1)&3)<<(2*mu))
            da=[psi(0,0,y)[i]-psi(0,0,x)[i] for i in range(2)]
            db=[psi(0,1,y)[i]-psi(0,1,x)[i] for i in range(2)]
            f+=Fraction((1 if mu==0 else -1)*sum(a*b for a,b in zip(da,db)),2)
        field.append(f)
    need(Counter(field)=={Fraction(-1):64,Fraction(0):128,Fraction(1):64},'local field signed counts')
    # Retain the common old X, select fresh independent uniform shifts U_j.
    # Effect conditional on specific U is NOT scalar; sum over the retained
    # new shift output to obtain a scalar marginal sign effect on arbitrary XR.
    vals=np.asarray([float(x) for x in field]);xs=np.arange(256,dtype=np.uint32)
    U=np.tile(xs,(256,1));X=np.tile(xs[:,None],(1,256));loc=vals[add_mod4(X,U)]
    means=loc.mean(axis=1);need(np.max(np.abs(means))==0,'uniform scalar sign marginal')
    # Toy coefficient k=1/2 is solely an effect normalization test.
    k=.5;fine=(1+k*loc)/2
    need(np.max(np.abs(fine.mean(axis=1)-.5))<1e-16,'sum over shift scalar effect')
    need(float(np.max(fine[:,0])-np.min(fine[:,0]))>0,'fine retained shift is not scalar')
    # For shared shift this joint model explicitly retains the very same
    # computational X (QND); effects alone cannot imply the product below.
    # Fresh independent shifts instead give scalar conditional effects even
    # when prior channels have otherwise modified the protected input.
    cov_shared=float(np.mean(vals*vals)*k*k);cov_ind=float(k*k*means[0]*means[0])
    need(abs(cov_shared-1/8)<1e-15 and cov_ind==0,'independent vs shared sign flag')
    # Retained shift+sign reveals X-dependent information even though the
    # sign alone is independent of X; do not identify CQ histories.
    h=lambda x:-x*math.log(x)-(1-x)*math.log(1-x)
    mi=.5*(math.log(2)-h((1+k)/2))
    need(mi>0,'retained shift reveals information about old SITE')
    return {'local_F_histogram':{'-1':64,'0':128,'1':64},
       'one_sign_marginal_over_uniform_shift':.5,'conditional_sign_effect_toy_k':k,
       'shared_shift_two_sign_correlation':cov_shared,'fresh_independent_shifts_correlation':cov_ind,
       'shared_shift_example_assumes_QND_Site_and_same_shift':True,
       'fine_shift_conditional_effect_not_scalar':True,
       'measuring_shift_and_sign_reveals_site_mutual_information_nats':mi}


def numerical():
    mp.mp.dps=100;p=(mp.sqrt(5)-1)/2;A=p*mp.sin(712*mp.asin(p));z=mp.mpf(2)**-20;L=4*p**3
    def report(y):
      u=p+p*p*y;B=4*u*u*(1-u*u);AA=L+(1-L)*B
      return 1-(1-z*B)*(1-z*AA)
    y=A*A/32 # Lambda=1 only for a numerical illustration
    shared=(report(-y)+2*report(0)+report(y))/4
    independent=report(0);gap=shared-independent
    need(gap<0,'strict Jensen gap')
    b1=1-p**40;b2=1-p**384;b3=1-(1-16*p**9)**64;bt=b2**6*b3
    ready=b1*b2**64*bt**1760
    return {'illustrative_Lambda_one_not_certified':True,
      'true_report_local_shared_minus_independent_shift':mp.nstr(gap,35),
      'shared_h_64_plus_1760_Toffoli_conditional_ready':mp.nstr(ready,35),
      'shared_h_64_plus_ready':mp.nstr(b1*b2**64,35),
      'beta_to_1760':mp.nstr(bt**1760,35)}


if __name__=='__main__':
 out={'status':'PASS','literal_shift_and_equality':algebra_checks(),
      'SITE_shift_bijection_cases':65536,
      'full_X_tau_Y_truth_table_proved_by_factorization':256**3,
      'correlation':correlation_checks(),'numerics':numerical(),
      'eight_signs_independent_shift_bits':64,'Toffoli_for_80_localizers':1760,
      'CX_for_80_localizers_including_NC1':6816,
      'fresh_L4_fourier_resources_still_needed':80,
      'choi_hq_final_report_full_factory_and_clock_compiled':False,
      'fixed_Rule_Book03_cost_information_proved':False,'GR_closed':False}
 print(json.dumps(out,indent=2,sort_keys=True))
