"""Literal L=4 G^89 and exact common-reference SC1 recalibration.

The current-field loader, full clock and Book valuation remain separate.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import runpy
import sys
import numpy as np
from mpmath import iv
from check_boundary_experiment import Golden as G
from check_eight_readers import inv

if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
HERE=Path(__file__).parent
loader=runpy.run_path(str(HERE/'check_dyadic_car_loader.py'))
mm=loader['mm'];mat_one=loader['mat_one'];mat_cx=loader['mat_cx']
rotation=loader['rotation'];swap=loader['swap_basis']
P=G(0,1);O=G(0);I=G(1);TWO=G(2);FOUR=G(4)
Z=G(F(1,2**20));H=G(F(1,32768))
GRID=F(16517734400,162621047169)


def report(x,y):
    E=P**2*(I+x);L=FOUR*E*(I-E);u=P+P**2*y
    B=FOUR*u*u*(I-u*u);A=L+(I-L)*B
    return Z*(A+B)-Z*Z*A*B


L0=FOUR*P**3
RF=FOUR*P**2*(I-TWO*P**2)*Z*(I-Z*L0)*(I-L0)
RQ=G(8)*P**3*(I-TWO*P**2)*(Z*(TWO-L0)-Z**2*(L0+TWO*(I-L0)*L0))
K=RQ*inv(RF)
D0=G(F(1,4096))*G(GRID/F(16))*inv(K)
DX=report(K*D0,O)-report(O-K*D0,O)
DY0=report(O,D0)-report(O,O-D0)


def cheb(n,c):
    # Exact arithmetic circuit for (T_n(c),T_(n+1)(c)).
    u,v=I,c
    for bit in bin(n)[2:]:
        a=TWO*u*u-I;b=TWO*u*v-c;d=TWO*v*v-I
        u,v=(b,d) if bit=='1' else (a,b)
    return u


def actual_mat_delta(k):
    # A_k² = p²(1-cos(16k theta))/2, cos(2theta)=p³.
    A2=P**2*(I-cheb(8*k,P**3))*G(F(1,2))
    # H_grid=1/4,s_ref=4: q_ref/rho=2 A_k².
    return G(F(1,4096))*TWO*A2


def verify_exact_interpolation(k):
    delta=actual_mat_delta(k)
    dy=report(O,delta)-report(O,O-delta)
    a=dy*inv(DX);a_old=DY0*inv(DX)
    weights=[F((-1)**(j-1)*comb(8,j),j) for j in range(1,9)]
    parts=[(I,P,G(F(2,9)),G(F(1,7))),
           (I,P**2,G(F(3,11)),G(F(-1,8)))]
    assert sum((v*rho for v,rho,_,_ in parts),O)==I
    target=sum((v*(f-K*m) for v,rho,f,m in parts),O)
    matter=sum((v*m for v,rho,f,m in parts),O)
    r0=report(O,O)
    def actual(a_value):
        total=O
        for j in range(1,9):
            jh=G(j)*H;branch=O
            for volume,rho,f,m in parts:
                u=jh*inv(rho)
                branch+=volume*rho*(dy*(report(u*f,O)-r0)
                                   +DX*(report(O,O-u*a_value*m)-r0))
            total+=G(weights[j-1])*branch
        return total
    fixed=actual(a)
    assert fixed==H*dy*RF*target
    old=actual(a_old)
    assert old-H*dy*RF*target==H*RF*K*(dy-DY0)*matter
    return {'k':k,'exact_golden_interpolation':True,
            'both_matter_components_scale_together':True,
            'unrecalibrated_mismatch_exact':True}


def verify_asymmetric_arms(k):
    # Independent scalar readiness factors are an explicitly different
    # architecture: they cannot be replaced by a common gamma^32.
    delta=actual_mat_delta(k)
    dy=report(O,delta)-report(O,O-delta)
    cy,cx,cf,cq,c0=(G(F(2,3)),G(F(3,4)),G(F(4,5)),G(F(5,6)),G(F(6,7)))
    A=cy*dy;B=cx*DX
    scale=A*cf*inv(B*cq)
    parts=[(I,P,G(F(2,9)),G(F(1,7))),
           (I,P**2,G(F(3,11)),G(F(-1,8)))]
    weights=[F((-1)**(j-1)*comb(8,j),j) for j in range(1,9)]
    target=sum((v*(f-K*m) for v,rho,f,m in parts),O)
    r0=report(O,O);total=O
    for j in range(1,9):
        branch=O;jh=G(j)*H
        for volume,rho,f,m in parts:
            u=jh*inv(rho)
            branch+=volume*rho*(A*(cf*report(u*f,O)-c0*r0)
                              +B*(cq*report(O,O-u*scale*m)-c0*r0))
        total+=G(weights[j-1])*branch
    offset=G(sum(weights))*(A*(cf-c0)+B*(cq-c0))*r0
    assert total-offset==H*A*cf*RF*target
    return {'distinct_y_x_f_q_zero_readiness':True,
            'exact_offset_and_rebalanced_source':True}


def literal_unitary(k,correct_sign):
    p=float((5**.5-1)/2);a=p**.5;gg=np.array([[a,-p],[p,a]])
    u0=mat_one(0,gg);xx=np.array([[0.,1.],[1.,0.]])
    for bit in (1,2,3):u0=mm(mat_one(bit,xx),u0)
    for bit in (1,2,3):u0=mm(mat_cx(0,bit),u0)
    # All eight G^k blocks are really multiplied, not matrix_power.
    tgt=mat_one(1,gg);ctrl=[0,2,3]
    gray=[j^(j>>1) for j in range(8)]
    word=np.eye(16);calls=0
    for j in range(8):
        for _ in range(k):word=mm(tgt,word);calls+=1
        diff=gray[j]^gray[(j+1)%8]
        word=mm(mat_cx(ctrl[diff.bit_length()-1],1),word)
    assert calls==8*k
    phase=8*k*np.arcsin(p)
    assert np.linalg.norm(word-rotation(0,2,phase),2)<2e-12
    Q=mm(swap(6,2),swap(14,6))
    out=mm(mm(mm(Q.T,word),Q),u0)
    if correct_sign:
        sign=np.eye(16)
        for q in (2,6,10,14):sign[q,q]=-1
        out=mm(sign,out)
    A=p*np.sin(phase);fill=(-p*np.cos(phase))*(-1 if correct_sign else 1)
    errors=[]
    for n in range(4):
        angle=np.pi*n/2
        U=mm(rotation(0,15,angle),out)
        target=np.zeros(16);target[1]=a;target[0]=A*np.cos(angle)
        target[14]=fill;target[15]=A*np.sin(angle)
        errors.append(float(np.linalg.norm(U[:,1]-target)))
        assert np.linalg.norm(mm(U.T,U)-np.eye(16))<5e-12
        assert abs(np.linalg.det(U)-1)<5e-12
    assert max(errors)<2e-12
    return {'k':k,'literal_G_calls_executed_in_full_matrix':calls,
            'extra_sign_correction_CZ':correct_sign,'all_16_columns':True,
            'all_four_SITE_values':True,'max_state_error':max(errors)}


def intervals(k,correct_sign):
    iv.dps=70;one=iv.mpf(1);p=(iv.sqrt(5)-one)/2;z=one/2**20
    theta=iv.atan2(p,iv.sqrt(p));Fh=iv.mpf(GRID.numerator)/GRID.denominator
    def r(x,y):
        E=p**2*(one+x);L=4*E*(one-E);u=p+p**2*y
        B=4*u*u*(one-u*u);A=L+(one-L)*B
        return z*(A+B)-z*z*A*B
    l0=4*p**3
    rf=4*p**2*(one-2*p**2)*z*(one-z*l0)*(one-l0)
    rq=8*p**3*(one-2*p**2)*(z*(2-l0)-z**2*(l0+2*(one-l0)*l0))
    k0=rq/rf;d0=(one/4096)*Fh/(16*k0)
    Ak=p*iv.sin(8*k*theta)
    filler=(-p*iv.cos(8*k*theta))*(-1 if correct_sign else 1)
    assert float(filler.a)>0
    if correct_sign:assert float(Ak.b)<0
    else:assert float(Ak.a)>0
    dm=2*Ak**2;delta=dm/4096
    dy=r(0,delta)-r(0,-delta);dy0=r(0,d0)-r(0,-d0)
    dx=r(k0*d0,0)-r(-k0*d0,0);recal=dy/dx
    c=one-2*p**2
    for _ in range(9):c=2*c**2-one
    visibility=(one-c)/2*p**7
    b2s=one-p**384;b3s=one-(one-16*p**9)**64
    beta24=(one-p**40)*(b2s**6*b3s)**1452
    b0=one-(one-2*p**3)**16
    b2=one-(one-4*p**3)**32;b3=one-(one-16*p**9)**32
    ready=b0**86*(b2**4*b3)**43*b3**3*(b2 if correct_sign else one)
    service=ready**32
    # alpha_other excludes exactly these 32 separately accounted loaders.
    gain=beta24*service*p**24*840*(one/32768)*p**3*visibility*rf*dy
    beta_bal=(one-(one-2*p**3)**16)**4
    kap=beta_bal*((one-(one-4*p**3)**32)**4*(one-(one-16*p**9)**32))**2
    return {'A':str(Ak),'filler':str(filler),'d_material':str(dm),
       'delta_material':str(delta),'old_delta_ratio':str(dy/dy0),
       'a_recalibrated':str(recal),'sqrt_a':str(iv.sqrt(recal)),
       'current_matter_amplitude_bound':str(p/iv.sqrt(recal)),
       'one_loader_success':str(ready),'32_loader_success':str(service),
       'gain_marker_per_alpha_other_squared':str(gain),
       'gain_T_plus_balanced_per_alpha_other_squared':str((one+2*p**4*kap)*gain)}


def main():
    loader['verify_routed_rotations']()
    loader['verify_exact_site_phases']()
    loader['verify_base_sign']()
    loader['gray_checks'](3)
    for u,v in ((14,6),(6,2),(0,1),(1,3),(3,7)):
        loader['verify_adjacent_swap'](u,v)
    short=literal_unitary(89,False);alt=literal_unitary(1,True)
    exact=[verify_exact_interpolation(89),verify_exact_interpolation(1)]
    asym=verify_asymmetric_arms(89)
    print(json.dumps({'schema':'d0.common-native-reference-calibration/1','status':'PASS',
       'short_literal':short,'alternative_literal':alt,'exact_Golden_SC1_checks':exact,
       'asymmetric_arm_readiness_check':asym,
       'short_intervals':intervals(89,False),'alternative_intervals':intervals(1,True),
       'short_nonfactory_inventory':{'birth':6,'G':719,'CX':71,'Toffoli':43,'CCZ':3},
       'field_dependent_current_loader_compiled':False,
       'common_bank_clock_constructed':False,'all_Book_cost_info_derived':False,
       'GR_closed':False},indent=2))


if __name__=='__main__':main()
