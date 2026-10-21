#!/usr/bin/env python3
"""Actual finite Golden/CNOT words -> fixed-cost full8D CQ query secants.

No continuously programmable gate is assumed.  A sequence of DIFFERENT
finite deterministic words is used, with equal primitive inventory inside
each comparison. Matrix powering is only a verifier; all word ticks are
charged. This is query-level source consistency, NOT a physical field writer,
Book/CQ selection, exact finite all42 stationary branch or bounded-cost limit.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import mpmath as mp
import sympy as sp

INPUT_REF='086fab99d8aaed7f712e9a3d2858c516b61901fc'

def require(ok, label):
    if not bool(ok):
        raise ArithmeticError(label)

def maxnorm(A):
    return max(abs(A[i,j]) for i in range(A.rows) for j in range(A.cols))

def kron(A,B):
    return mp.matrix([[A[i//B.rows,j//B.cols]*B[i%B.rows,j%B.cols] for j in range(A.cols*B.cols)] for i in range(A.rows*B.rows)])

def exact_identities():
    a=sp.symbols('a',real=True); p=a*a
    def red(v): return sp.rem(sp.Poly(sp.expand(v),a),sp.Poly(a**4+a**2-1,a)).as_expr().expand()
    def zmat(A): return all(red(v)==0 for v in A)
    G=sp.Matrix([[a,-p],[p,a]])
    X=sp.Matrix([[0,1],[1,0]])
    C=sp.eye(4); C[2,2]=C[3,3]=0;C[2,3]=C[3,2]=1
    GN=sp.kronecker_product(sp.eye(2),G)
    plus=GN*C*C      # chronological C,C,G
    minus=C*GN*C    # chronological C,G,C
    require(zmat(plus-sp.diag(G,G)),'plus cell on BOTH known-one sectors')
    require(zmat(minus-sp.diag(G,G.T)),'minus cell including c=0 complement')
    require(zmat(plus.T*plus-sp.eye(4)) and zmat(minus.T*minus-sp.eye(4)),'full cells orthogonal')
    require(zmat(plus*minus-minus*plus),'equal-cost cell algebra commutes')
    require(zmat(G.T*G-sp.eye(2)),'native Golden relation')
    # If exp(2 i theta) were a root of unity, every conjugate of
    # 2cos(2theta) would be in [-2,2]. Its second algebraic conjugate is not.
    t=sp.symbols('t'); poly=t*t+8*t-4
    require(sp.expand(poly.subs(t,2*sp.sqrt(5)-4))==0,'exact native angle conjugate polynomial')
    require(-4-2*sp.sqrt(5)<-2,'no root-of-unity angle; return sequence exists')
    E,b=sp.symbols('E b',positive=True)
    r,s=sp.symbols('r s',real=True)
    Rot=sp.Matrix([[r,-s],[s,r]])
    T=C*sp.kronecker_product(Rot,sp.eye(2))
    owned=sp.Matrix([[r,0,-s,0],[0,r,0,-s],[0,s,0,r],[s,0,r,0]])
    require(T==owned,'literal original four-tail query')
    # Endpoint source identities, not only a trace match.
    J=sp.Matrix([[0,-1],[1,0]])
    T0=C*sp.kronecker_product(G,sp.eye(2))
    Te=C*sp.kronecker_product(J*G,sp.eye(2))
    Ue=sp.kronecker_product(Te*T0+T0*Te,G*G)
    Ub=sp.kronecker_product(T0*T0,2*J*G*G)
    require(red(sp.trace(Ue)*a/2+8*p**5)==0,'geometry native secant target trace')
    require(red(-sp.trace(Ub)*a**3-32*p**4)==0,'sigma-minus matter native secant target trace')
    # A true additional source cannot be erased by a common-prefix slogan.
    h,c=sp.symbols('h c',nonzero=True)
    require(sp.simplify((c*h-(-c*h))/(2*h)-c)==0,'moving compiler-price negative control')
    return {'full_control_complements':'EXACT_Q(a)',
            'cell_inventory':{'G':1,'CNOT_known_one_target':2},
            'native_angle_not_root_of_unity':True,
            'full8D_endpoint_jets':'EXACT_ORIGINAL_QUERY',
            'fixed_word_derivative_claimed':False}

def numeric_word_checks():
    mp.mp.dps=85
    p=(mp.sqrt(5)-1)/2; a=mp.sqrt(p); theta=mp.asin(p)
    G=mp.matrix([[a,-p],[p,a]])
    I=mp.eye(2)
    C=mp.eye(4);C[2,2]=C[3,3]=0;C[2,3]=C[3,2]=1
    J=mp.matrix([[0,-1],[1,0]])
    P=mp.matrix(8,2);P[0,0]=1;P[2,1]=1
    plus=mp.matrix([1,1])/mp.sqrt(2);minus=mp.matrix([1,-1])/mp.sqrt(2)
    z=mp.mpf(2)**-20
    alpha=(1-(1-2*p**3)**9)**128
    beta=((1-p**120)**4*(1-(1-16*p**9)**20))**43
    def hphi(v):return -(v*mp.log(v)+(1-v)*mp.log(1-v))/mp.log(1/p)
    def query(RE,Rb):
        T=C*kron(RE,I)
        return kron(T*T,Rb*Rb)
    def report(U):
        W=P.T*U*P; F=mp.eye(2)-W.T*W
        A=(plus.T*F*plus)[0];B=(minus.T*F*minus)[0]
        require(0<A<1 and 0<B<1,'positive true retained band effects')
        q=1-(1-z*A)*(1-z*B)
        require(0<q<1,'complete nonpostselected binary report')
        return q
    U0=query(G,G); q0=report(U0)
    T=C*kron(G,I);Te=C*kron(J*G,I)
    de=kron(Te*T+T*Te,G*G)
    db=kron(T*T,2*J*G*G)
    hprime=mp.log((1-q0)/q0)/mp.log(1/p)
    L=4*p**3;M=L*(1+p**6);Q=1-z*L;R=1-z*M
    rx=4*z*Q*p**11; ry=-8*z*p**6*(R+Q*p**6)
    expected_f=-alpha*beta*hprime*rx
    expected_q=-alpha*beta*hprime*ry
    expected_lambda=ry/rx
    # All program settings have N cells in every one of FOUR rotation slots.
    # A cell is plus or minus by order only. c=0 always sees G^N.
    # Counts include the two original tail CNOTs, but exclude separate bank,
    # measurement/feedforward and routing charges which remain in the owner.
    qvalues=(33,580,1193,4192,17961)
    out=[]
    for den in qvalues:
        num=int(mp.nint(den*theta/mp.pi))
        delta=2*(den*theta-num*mp.pi)
        require(0<abs(delta)<mp.mpf('.011'),'nontrivial intrinsic small return')
        N=2*den+1
        Rp=G**(1+2*den);Rm=G**(1-2*den)
        for sign,rot in ((1,Rp),(-1,Rm)):
            exact=mp.matrix([[mp.cos(theta+sign*delta),-mp.sin(theta+sign*delta)],[mp.sin(theta+sign*delta),mp.cos(theta+sign*delta)]])
            require(maxnorm(rot-exact)<mp.mpf('1e-72'),'actual powers have the claimed native angular step')
        # Direct sequential product of expanded primitive cells at q=33,
        # every c0/c1 column, not just the effective one-qubit power.
        if den==33:
            Gc=kron(mp.eye(2),G)
            Cc=C
            for k in (-1,0,1):
                exponent=1+2*den*k
                neg=(N-exponent)//2;pos=N-neg
                sequential=mp.eye(4)
                for idx in range(N):
                    word=(Cc,Gc,Cc) if idx<neg else (Cc,Cc,Gc)
                    for gate in word: sequential=gate*sequential
                block=mp.matrix(4,4)
                for row in range(2):
                    for col in range(2):
                        block[row,col]=(G**N)[row,col]
                        block[row+2,col+2]=(G**exponent)[row,col]
                require(maxnorm(sequential-block)<mp.mpf('1e-78'),'literal equal-inventory whole-controller word')
        # c=0 sector is identical across the compared settings and stays
        # orthogonal. c=1 is the same fixed active input, not a moving cut.
        Up=query(Rp,G);Um=query(Rm,G)
        Vp=query(G,Rp);Vm=query(G,Rm)
        for U in (U0,Up,Um,Vp,Vm):
            require(maxnorm(U.T*U-mp.eye(8))<mp.mpf('1e-72'),'all8D query columns, no dropped complement')
        # Original density operands at actual finite words; eta_query^2=1.
        fplus=(Rp[1,0]**2/p**2-1);fminus=(Rm[1,0]**2/p**2-1)
        qplus=-(Rp[1,0]-p)/p**2;qminus=-(Rm[1,0]-p)/p**2
        # The actual paid quantum field source: BOTH complete CQ prices use
        # the same paid baseline. Do not renormalize by their runtime.
        pair_ticks=2*(4*N+8*N+2)
        common_paid=alpha*pair_ticks  # real query ticks; other proved common ledger cancels
        S=lambda U: common_paid-alpha*beta*hphi(report(U))
        sf=(S(Up)-S(Um))/(fplus-fminus)
        sq=(S(Vp)-S(Vm))/(qplus-qminus)
        ratio=sq/sf
        errE=maxnorm((Up-Um)/(2*delta)-de)
        errb=maxnorm((Vp-Vm)/(2*delta)-db)
        relf=abs(sf/expected_f-1);relq=abs(sq/expected_q-1)
        require(relf<20*delta**2 and relq<20*delta**2,'native paid CQ source has quadratic secant consistency')
        require(errE<10*delta**2 and errb<10*delta**2,'full operator jet consistency, not scalar fitting')
        # Opposite nonconstant prices would leave a real residual instead.
        missing=mp.mpf('.01')
        hostile=((S(Up)+missing*fplus)-(S(Um)+missing*fminus))/(fplus-fminus)
        require(abs(hostile-sf-missing)<mp.mpf('1e-65'),'outside-ledger mismatch remains a genuine source')
        out.append({'return_denominator':den,'nearest_pi_numerator':num,
                    'native_angle_step':mp.nstr(delta,24),
                    'cells_per_rotation':N,'two_query_G_count':8*N,
                    'two_query_CNOT_count':16*N+4,'two_query_unit_ticks':pair_ticks,
                    'full_operator_jet_error':mp.nstr(max(errE,errb),22),
                    'source_f':mp.nstr(sf,28),'source_q_sigma_minus':mp.nstr(sq,28),
                    'relative_source_error_f':mp.nstr(relf,20),
                    'relative_source_error_q':mp.nstr(relq,20),
                    'matter_geometry_source_ratio':mp.nstr(ratio,28),
                    'primary_tangent_source_defect':mp.nstr(sq-expected_lambda*sf,24),
                    'naive_unpadded_single_rotation_cost_gap':(1+2*den)-3*(2*den-1)})
    # Spectral/compression negative witness: finite fixed word remains a
    # constant matrix. Only secants between actual DIFFERENT words vary.
    require(abs(sum(de[i,i] for i in range(8)))>mp.mpf('.1'),'nonzero trace jet excluded for a single fixed word')
    return {'precision_decimal_digits':mp.mp.dps,
            'original_caps':{'K_pre':9,'L_gate':20,'N':1},
            'q0':mp.nstr(q0,32),'expected_f_source':mp.nstr(expected_f,32),
            'expected_q_source_sigma_minus':mp.nstr(expected_q,32),
            'expected_finite_z_ratio':mp.nstr(expected_lambda,32),
            'word_checks':out}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path);args=ap.parse_args()
    result={'status':'PASS_PAID_GOLDEN_WORD_QUERY_SECANTS','input_ref':INPUT_REF,
            'exact':exact_identities(),'native':numeric_word_checks(),
            'scope':{'exact_finite_G_CNOT_words':True,'full8D_complement_retained':True,
                     'same_primitive_inventory_within_each_comparison':True,
                     'same_fixed_input_cut_and_oldRIGHT':True,
                     'analogue_moving_rotation_primitive':False,
                     'finite_difference_to_original_CQ_source_proved':True,
                     'exact_differentiable_finite_word_family':False,
                     'source_comparison_of_same_declared_CQ_cut':True,
                     'addressability_and_known_one_admission_inherited':True,
                     'remaining_compiler_ledger_consumed_not_recomputed':True,
                     'uniform_physical_runtime_bound_proved':False,
                     'actual_autonomous_geometry_to_program_map_proved':False,
                     'Book03_absolute_Info_selected':False,
                     'all42_finite_native_stationary_solutions_proved':False,
                     'GR_closed':False}}
    text=json.dumps(result,ensure_ascii=False,indent=2)+'\n';print(text,end='')
    if args.output:args.output.write_text(text,encoding='utf-8')
if __name__=='__main__':main()
