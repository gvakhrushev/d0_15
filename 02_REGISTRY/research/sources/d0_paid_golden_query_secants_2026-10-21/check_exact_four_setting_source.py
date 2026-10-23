#!/usr/bin/env python3
"""Exact native parameter-shift source from four distinct equally paid report settings.

Consumes the original CQ contract and the companion Golden cell proof.
The known general parameter-shift method is specialized, not rediscovered.
This is a finite SOURCE EVALUATOR, not a physical field writer or a new action.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import mpmath as mp
import sympy as sp

INPUT_REF='086fab99d8aaed7f712e9a3d2858c516b61901fc'
COMPANION_BLOB='ddf80ddbeb2828a2e711a45862c99d69869a5684'

def require(ok,label):
    if not bool(ok):raise ArithmeticError(label)

def maxnorm(A):return max(abs(x) for x in A)

def run():
    companion=Path(__file__).with_name('check_paid_golden_query_secants.py')
    data=companion.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    require(actual==COMPANION_BLOB,'companion exact executed source pin')
    a,z=sp.symbols('a z',real=True);p=a*a
    mod=sp.Poly(a**4+a*a-1,a)
    def red(v):
        # Coefficients may include z; inversion below is only for elements Q(a).
        return sp.Poly(sp.expand(v),a,domain='EX').rem(sp.Poly(mod.as_expr(),a,domain='EX')).as_expr().expand()
    def inv(v):return sp.invert(sp.Poly(v,a),mod).as_expr()
    def mul(A,B):return (A*B).applyfunc(red)
    G=sp.Matrix([[a,-p],[p,a]])
    def power(n):
        result=sp.eye(2)
        for _ in range(abs(n)):result=mul(result,G if n>=0 else G.T)
        return result
    sins={k:power(k)[1,0] for k in (4,8,16,32)}
    determinant=red(sins[8]*sins[32]-sins[16]**2)
    require(determinant!=0,'native sine interpolation determinant nonzero in Q(a)')
    wE=red(2*inv(sins[8]))
    w1=red((2*sins[32]-4*sins[16])*inv(determinant))
    w2=red((4*sins[8]-2*sins[16])*inv(determinant))
    require(red(wE*sins[8]-2)==0,'exact geometry frequency-four stencil')
    require(red(w1*sins[8]+w2*sins[16]-2)==0,'exact matter frequency-four stencil')
    require(red(w1*sins[16]+w2*sins[32]-4)==0,'exact matter frequency-eight stencil')
    C=sp.eye(4);C[2,2]=C[3,3]=0;C[2,3]=C[3,2]=1
    P=sp.zeros(8,2);P[0,0]=P[2,1]=1
    J=sp.Matrix([[0,-1],[1,0]])
    settings=((1,1),(3,1),(-1,1),(1,3),(1,-1),(1,5),(1,-3))
    Us={};rs={}
    for e,b in settings:
        RE,Rb=power(e),power(b)
        T=mul(C,sp.kronecker_product(RE,sp.eye(2)))
        U=sp.kronecker_product(mul(T,T),mul(Rb,Rb)).applyfunc(red)
        require(all(red(v)==0 for v in mul(U.T,U)-sp.eye(8)),'all8D orthogonal at native setting')
        W=mul(mul(P.T,U),P)
        F=sp.eye(2)-mul(W.T,W)
        plus,minus=sp.Matrix([1,1]),sp.Matrix([1,-1])
        A=red((plus.T*F*plus)[0]/2);B=red((minus.T*F*minus)[0]/2)
        rr=red(z*(A+B)-z*z*A*B)
        # Exact finite Fourier structure from the TRUE original full8D cut.
        cb=red((Rb[0,0]**2-Rb[1,0]**2)**2)
        ce=red((RE[0,0]**2-RE[1,0]**2)**2)
        require(red(rr-(1-(1-z+z*cb)*(1-z+z*cb*ce)))==0,'native effect equals finite-harmonic report')
        Us[e,b]=U;rs[e,b]=rr
    L=4*p**3;M=red(L*(1+p**6));Q=1-z*L;R=1-z*M
    rx=red(4*z*Q*p**11);ry=red(-8*z*p**6*(R+Q*p**6))
    from_e=red(a*wE*(rs[3,1]-rs[-1,1])/2)
    from_b=red(-a**3*(w1*(rs[1,3]-rs[1,-1])+w2*(rs[1,5]-rs[1,-3])))
    require(red(from_e-rx)==0,'exact original geometry probability source from native words')
    require(red(from_b-ry)==0,'exact original sigma-minus material probability source from native words')
    require(red(rs[-1,1]-rs[1,1])==0 and red(rs[1,-1]-rs[1,1])==0 and red(rs[1,-3]-rs[1,3])==0,
            'exact report symmetry reduces seven operator settings to four probability contexts')
    T=mul(C,sp.kronecker_product(G,sp.eye(2)));Te=mul(C,sp.kronecker_product(J*G,sp.eye(2)))
    de=sp.kronecker_product(mul(Te,T)+mul(T,Te),mul(G,G)).applyfunc(red)
    db=sp.kronecker_product(mul(T,T),2*mul(J,mul(G,G))).applyfunc(red)
    opweight=inv(sins[4])
    require(all(red(opweight*v-w)==0 for v,w in zip(Us[3,1]-Us[-1,1],de)),'exact full8D geometry OPERATOR jet')
    require(all(red(opweight*v-w)==0 for v,w in zip(Us[1,3]-Us[1,-1],db)),'exact full8D material OPERATOR jet')
    # Three-letter primitive cells on c=0 give G in either order; on c=1
    # they give G or G^-1. Use FIVE cells in all four rotation slots.
    N=5
    counts={}
    for exponent in (-3,-1,1,3,5):
        neg=(N-exponent)//2;pos=N-neg
        require(pos>=0 and neg>=0 and pos-neg==exponent,'valid equal-inventory literal word')
        counts[str(exponent)]={'plus_cells':pos,'minus_cells':neg}
    mp.mp.dps=85
    av=mp.sqrt((mp.sqrt(5)-1)/2);pv=av*av;zv=mp.mpf(2)**-20
    def val(v):return mp.mpf(str(sp.N(v.subs({a:sp.Float(str(av),90),z:sp.Rational(1,2**20)}),82)))
    alpha=(1-(1-2*pv**3)**9)**128
    beta=((1-pv**120)**4*(1-(1-16*pv**9)**20))**43
    rv={k:val(v) for k,v in rs.items()}
    require(all(0<x<1 for x in rv.values()),'all actual measured reports positive')
    h=lambda r:-(r*mp.log(r)+(1-r)*mp.log(1-r))/mp.log(1/pv)
    hp=mp.log((1-rv[1,1])/rv[1,1])/mp.log(1/pv)
    we,ww1,ww2=val(wE),val(w1),val(w2)
    ell={k:alpha*beta*v for k,v in rv.items()}  # UNCONDITIONAL ready-and-click; no omitted aborts
    source_f=-hp*av/2*we*(ell[3,1]-ell[-1,1])
    source_q=hp*av**3*(ww1*(ell[1,3]-ell[1,-1])+ww2*(ell[1,5]-ell[1,-3]))
    expected_f=-alpha*beta*hp*val(rx);expected_q=-alpha*beta*hp*val(ry)
    require(abs(source_f-expected_f)<mp.mpf('1e-70'),'complete unconditioned CQ geometry source')
    require(abs(source_q-expected_q)<mp.mpf('1e-70'),'complete unconditioned CQ matter source')
    # Entropy itself is NOT a finite-harmonic polynomial. The chain rule is
    # essential; applying the report's shift weights to price values is wrong.
    S={k:-alpha*beta*h(v) for k,v in rv.items()}
    wrong=av/2*we*(S[3,1]-S[-1,1])
    require(abs(wrong-expected_f)>mp.mpf('1e-11'),'reject shifting nonlinear entropy with probability weights')
    # Each ell is an honest Bernoulli probability per FULL launched setting.
    # Variance coefficients assume n independent full runs PER nonbaseline setting.
    cf=hp*av/2*we
    vf=cf**2*sum(ell[k]*(1-ell[k]) for k in ((3,1),(-1,1)))
    cq1=hp*av**3*ww1;cq2=hp*av**3*ww2
    vq=(hp*av**3)**2*(ww1**2*ell[1,1]*(1-ell[1,1])+(ww1-ww2)**2*ell[1,3]*(1-ell[1,3])+ww2**2*ell[1,5]*(1-ell[1,5]))
    four_source_f=-hp*av/2*we*(ell[3,1]-ell[1,1])
    four_source_q=hp*av**3*(-ww1*ell[1,1]+(ww1-ww2)*ell[1,3]+ww2*ell[1,5])
    require(abs(four_source_f-source_f)<mp.mpf('1e-70') and abs(four_source_q-source_q)<mp.mpf('1e-70'),
            'same exact source from FOUR full report contexts')
    return {'status':'PASS_EXACT_FOUR_SETTING_NATIVE_SOURCE','input_ref':INPUT_REF,
            'companion_git_blob':actual,
            'exact':{'operator_identity_settings':[list(x) for x in settings],
                     'distinct_probability_settings':[[1,1],[3,1],[1,3],[1,5]],
                     'cell_counts_by_rotation_exponent':counts,
                     'two_query_inventory_per_setting':{'G':40,'CNOT':84,'unit_query_ticks':124},
                     'all_retained_operator_and_report_jets':'EXACT_IN_Q(a)[z]',
                     'w_geometry':str(wE),'w_matter_1':str(w1),'w_matter_2':str(w2),
                     'sine_interpolation_determinant':str(determinant),
                     'symbolic_source_error':0,
                     'native_unconditional_abort_factor_retained':True},
            'numeric':{'precision_decimal_digits':mp.mp.dps,
                       'w_geometry':mp.nstr(we,26),'w_matter_1':mp.nstr(ww1,26),'w_matter_2':mp.nstr(ww2,26),
                       'source_f':mp.nstr(source_f,32),'source_q_sigma_minus':mp.nstr(source_q,32),
                       'matter_geometry_ratio':mp.nstr(source_q/source_f,32),
                       'direct_wrong_entropy_stencil_error':mp.nstr(wrong-expected_f,26),
                       'geometry_estimator_variance_times_shots_per_setting':mp.nstr(vf,24),
                       'matter_estimator_variance_times_shots_per_setting':mp.nstr(vq,24),
                       'query_runs_for_1percent_geometry_RMS_per_setting':str(int(mp.ceil(vf/(mp.mpf('.01')*source_f)**2))),
                       'report_probabilities':{str(k):mp.nstr(v,24) for k,v in rv.items()}},
            'scope':{'known_parameter_shift_method_applied_not_new_general_theorem':True,
                     'exact_source_evaluator':True,'no_analogue_angle_primitive':True,
                     'arbitrarily_small_executable_variations':'SEPARATE_COMPANION_SECANT_THEOREM',
                     'finite_shot_error_eliminated':False,
                     'field_writer_or_autonomous_descent_proved':False,
                     'signed_postprocessing_is_physical_Book_action':False,
                     'selected_Book_Info_or_input_constraints_proved':False,
                     'complete_bank_detector_ledger_recomputed':False,
                     'GR_closed':False}}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path);args=ap.parse_args()
    text=json.dumps(run(),ensure_ascii=False,indent=2)+'\n';print(text,end='')
    if args.output:args.output.write_text(text,encoding='utf-8')
if __name__=='__main__':main()
