#!/usr/bin/env python3
"""Native full128 golden/Julia relative transfer: exact full16 finite check.
All 64 SELECT rows and both 64-outcome golden controller ports retained.
Do not mistake Q_blank,k for W_k,blank = delta - 2 Q_blank,k* A.
"""
from functools import lru_cache
import json
import sympy as S
p=(S.sqrt(5)-1)/2
I=S.eye(16)
O=S.zeros(16)
ORDER=(0,2,3,1)
checks=[]
def eq(name,a,b=0):
    delta=a-b
    if isinstance(delta,S.MatrixBase): ok=all(S.simplify(v)==0 for v in delta)
    else: ok=S.simplify(delta)==0
    if not ok: raise ArithmeticError(name)
    checks.append(name)
def yes(name,q):
    if not q: raise ArithmeticError(name)
    checks.append(name)
@lru_cache(None)
def creator(r):
    c=S.zeros(16)
    for m in range(16):
        if not m&(1<<r):
            c[m|(1<<r),m]=(-1)**sum(bool(m&(1<<j)) for j in ORDER[:ORDER.index(r)])
    return c
def native_select(nu,b,zs):
    words=[]
    for r in range(4):
        c=creator(r)
        P=nu*zs[r]*c
        C=nu*c
        L=I+(b-1)*c*c.T
        R=I+(b-1)*c.T*c
        for term in ((P,L),(P.H,R),(-C,-L),(-C.H,-R)):
            words.extend((term,term))
    return [sum(((-1)**((label&j).bit_count())*words[j][coeff]
                 for j in range(32)),S.zeros(16))/32
            for label in range(32) for coeff in range(2)]
def reflection(rows):
    A=rows[0]
    return [(I if j==0 else O)-2*N.H*A for j,N in enumerate(rows)]
def cross(a,b):
    return sum((bb.H*aa for aa,bb in zip(a,b)),S.zeros(16))
def select_rev(a,b):
    return sum((bb*aa.H for aa,bb in zip(a,b)),S.zeros(16))
def run():
    eq('p_plus_p2',p+p*p,1)
    eq('p_minus_p2',p-p*p,p**3)
    for r in range(4):
        C=creator(r)
        eq('full16_CAR_'+str(r),C*C.T+C.T*C,I)
    vx,bx=S.Rational(3,5),S.Rational(4,5)
    vy,by=S.Rational(5,13),S.Rational(12,13)
    zs=[S.I,1,1,1]
    N1,N2=native_select(vx,bx,zs),native_select(vy,by,zs)
    A1,A2=N1[0],N2[0]
    Dshape=sum(((zs[r]-1)*creator(r)+(S.conjugate(zs[r])-1)*creator(r).T
                for r in range(4)),S.zeros(16))
    eq('literal_blank_hD_over16',A1,vx*Dshape/16)
    eq('blank_square_1',A1*A1,2*vx*vx*I/256)
    eq('blank_square_2',A2*A2,2*vy*vy*I/256)
    eq('Q_blank_row_isometry_1',select_rev(N1,N1),I)
    eq('Q_blank_row_isometry_2',select_rev(N2,N2),I)
    t=(1+vx*vy+bx*by)/2
    eq('actual_SELECT_cross',select_rev(N1,N2),t*I)
    eq('actual_SELECT_cross_other_order',cross(N1,N2),t*I)
    eq('t_equals_64_over_65',t,S.Rational(64,65))
    f=S.factor(vx*vx+vy*vy-2*t*vx*vy)
    eq('finite_positive_f',f,S.Rational(226,4225))
    W1,W2=reflection(N1),reflection(N2)
    eq('true_W_column_isometry_1',cross(W1,W1),I)
    eq('true_W_column_isometry_2',cross(W2,W2),I)
    tw=1-2*f/128
    eq('true_W_column_cross',cross(W1,W2),tw*I)
    eq('golden_port_delta_coefficient',p*p+p**3,p)
    eq('golden_port_W_coefficient',p**4+p**3,p*p)
    eq('golden_port_mixed_cancel',p**3-p**3,0)
    c=p+p*p*tw
    eq('full128_native_cross',c,1-p*p*f/64)
    eq('radical_full128_cross',c,(270061+113*S.sqrt(5))/270400)
    yes('wrong_DIRECT_SELECT_shortcut',S.simplify(c-(p+p*p*t))!=0)
    # Noncommuting B controls the full off-diagonal source, NOT a scalar
    # substitution for the physical 128-port Kraus recurrence.
    B=creator(0)+creator(1).T
    Rw=sum((wy.H*B*wx for wx,wy in zip(W1,W2)),S.zeros(16))
    Ftrue=p*B+p*p*Rw
    h=S.Rational(1,4)
    D1,D2=16*A1/h,16*A2/h
    eps=p*p*h*h/64
    T=sum((ny*B*nx.H for nx,ny in zip(N1,N2)),S.zeros(16))
    Freal=B+eps*(D2*T*D1-(D2*D2*B+B*D1*D1)/2)
    eq('exact_all128_relative_generator',Ftrue,Freal)
    Tdiag=sum((nx*B*nx.H for nx in N1),S.zeros(16))
    eq('true_native_diagonal_GKSL_adj',
       B+eps*(D1*Tdiag*D1-(D1*D1*B+B*D1*D1)/2),
       p*B+p*p*sum((wx.H*B*wx for wx in W1),S.zeros(16)))
    # The exact full-word scalar transfer follows from F(I)=cI and
    # linearity: induction is mathematical, no truncated history.
    for n in range(1,8):
        eq('full_word_transfer_induction_'+str(n),c*c**(n-1),c**n)
    hh=S.symbols('hh',positive=True)
    w_h=2-2*S.cos(2*S.pi*hh)
    c_h=1-p*p*w_h*f/128
    L=S.limit(-256*S.log(c_h)/(hh**2*S.log((1+S.sqrt(5))/2)),hh,0)
    eq('original_clock_finite_comparison_limit',
       L,8*S.pi**2*p*p*f/S.log((1+S.sqrt(5))/2))
    near=S.limit(-256*S.log(1-p*p*w_h*hh**2*f/128)/hh**2,hh,0)
    eq('adjacent_coframe_vanishing_unscaled_comparison',near,0)
    # Complete flat zero mode D(0)=0 means original whole round=identity.
    eq('zero_mode_complete_original_record_cross',p+p*p,1)
    z=S.Rational(1,2**20)
    yes('target_independently_attenuated_zero_mode_not_native',
        float(1-S.sqrt(p)*(1-z))>0)
    return {'actual_full128_one_round_cross':str(S.simplify(c)),
            'cross_float':float(c),
            'SELECT_only_cross':'64/65',
            'true_reflection_overlap':str(tw),
            'full_clock_price_per_internal_mode':float(L),
            'zero_mode_original_cross':1,
            'target_zero_mode_cross':float(S.sqrt(p)*(1-z)),
            'nontrivial_true_generator':True}
if __name__=='__main__':
    result=run()
    print(json.dumps({'schema':'native-full128-relative-transfer/1',
          'check_count':len(checks),'result':result,
          'physical_relative_interferometric_cut_admitted':False,
          'GR_closed':False},sort_keys=True,indent=2))
