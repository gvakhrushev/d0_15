#!/usr/bin/env python3
"""Original CAR16+positive Julia success/failure vacuum-reference signed curvature check.

Research on the *supplied* original Lorentz/Julia link interface.
The entire 16-branch, four-step Julia flag tape is retained. The new tester
uses a field-independent four-label vacuum/grade-one seed and a fixed
three-eigenvalue PVM, and reads one final bit. No Choi programme writer, new
Info law, or assumed GR closure. Full output prices are a declared measured
CQ/port-cost cut, NOT the compulsory Book03 algebra-valued action.
"""
from __future__ import annotations
import argparse, itertools, json, math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import scipy.linalg as la
import sympy as sp

ORDER=(0,2,3,1)
PHI=(1+math.sqrt(5))/2
P_GOLDEN=1/PHI
LN_PHI=math.log(PHI)
CHECKS=[]

def require(x,label):
    if not bool(x): raise AssertionError(label)
    CHECKS.append(label)

def near(x,y,label,tol=1.e-10):
    if abs(complex(x-y))>tol:
        raise AssertionError(f'{label}: {x} != {y}, error {abs(complex(x-y))}')
    CHECKS.append(label)

def unit(i,j):
    A=sp.zeros(4); A[i,j]=1; return A
N2=unit(1,2)+unit(2,0)
N3=unit(1,3)+unit(3,0)
M2=unit(0,2)+unit(2,1)
M3=unit(0,3)+unit(3,1)
J=unit(2,3)-unit(3,2)
B=unit(1,1)-unit(0,0)
G=[N2,N3,M2,M3,J,B]
NAMES=['N2','N3','barN2','barN3','J','B']
ETA=sp.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])

def signs():
    result={}
    for mask in range(16):
        seq=[k for k in ORDER if mask & (1<<k)]
        result[mask]=(-1)**sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))
    return result
SIGN=signs()

def exterior16(A):
    # Original 0,2,3,1 CAR wedge ordering. The grade-0/1 entries are unchanged.
    arr=np.zeros((16,16),dtype=float)
    for out in range(16):
        rows=[i for i in range(4) if out&(1<<i)]
        for inn in range(16):
            cols=[i for i in range(4) if inn&(1<<i)]
            if len(rows)!=len(cols):continue
            if len(rows)==0:v=1.
            else:v=float(np.linalg.det(A[np.ix_(rows,cols)]))
            arr[out,inn]=SIGN[out]*SIGN[inn]*v
    return arr

def input_seed():
    psi=np.zeros((4,16),dtype=float)
    for j in range(4):
        psi[j,0]=1/math.sqrt(8)
        psi[j,1<<j]=1/math.sqrt(8)
    require(abs(float(np.vdot(psi,psi))-1)<1e-14,'full fixed reference4/CAR16 seed normalized')
    return psi
PSI=input_seed()

def projector_M(a):
    """One fixed PVM for a real original proper-Lorentz G_a.

    M_j=|vac><G e_j|+|G e_j><vac| on reference label j.
    All original six G columns have squared norm either zero or one.
    """
    M=np.zeros((4,16,16),float)
    a=np.asarray(a,dtype=float)
    for j in range(4):
        for i in range(4):
            M[j,0,1<<i]=a[i,j]
            M[j,1<<i,0]=a[i,j]
        n2=sum(a[i,j]*a[i,j] for i in range(4))
        require(n2 in (0.,1.),f'original generator column projector norm {j}')
    return M

def analytic_signed(P,g,n=4):
    return 4.0**(-n)/4 * float(np.sum(g*P))

def marked_probabilities(P,g,n=4):
    E=exterior16(P)
    state=4.0**(-n/2)*PSI@E.T
    M=projector_M(g)
    good=float(np.vdot(state,state).real)
    odd=sum(float(state[j]@M[j]@state[j]) for j in range(4))
    q_pm=[]
    rests=[]
    for sign in (1,-1):
        result=0.
        for j in range(4):
            M2=M[j]@M[j]
            effect=(M2+sign*M[j])/2
            require(np.linalg.norm(effect@effect-effect)<1e-12,
                    f'fixed signed eigenspace a projective POVM')
            result+=float(state[j]@effect@state[j])
        q_pm.append(result)
    qrest=good-sum(q_pm)
    near(q_pm[0]-q_pm[1],odd,'PVM odd expectation',tol=3e-13)
    near(odd,analytic_signed(P,g,n),'linear proper Lorentz CAR vacuum cross',tol=3e-13)
    require(min(q_pm+[qrest,1-good])>-1e-13,'positive completed all-good PVM and failed Julia histories')
    near(sum(q_pm)+qrest+(1-good),1.,'all good + all failures normalization',tol=3e-12)
    return {'plus':q_pm[0],'minus':q_pm[1],'success_rest':qrest,'failed':1-good,
            'odd':odd,'good':good}

def sqrt_positive(A):
    e,V=np.linalg.eigh((A+A.T)/2)
    require(min(e)>0.50,'original Julia strict positive defect')
    return (V*np.sqrt(e))@V.T

def Julia_K(U):
    T=.5*exterior16(U)
    D=sqrt_positive(np.eye(16)-T.T@T)
    near(np.linalg.norm(T.T@T+D.T@D),np.linalg.norm(np.eye(16)),
         'original fullCAR16 Julia complement trace',tol=5e-13)
    require(np.linalg.norm(T.T@T+D.T@D-np.eye(16))<2e-13,
            'original fullCAR16 Julia complete positive Kraus pair')
    return [T,D]

def flag_histories(factors):
    ks=[Julia_K(np.asarray(U,dtype=float)) for U in factors]
    results={}
    for bits in itertools.product((0,1),repeat=len(factors)):
        K=np.eye(16)
        for k,bit in zip(ks,bits):
            K=k[bit]@K
        results[bits]=K
    complete=sum((K.T@K for K in results.values()),np.zeros((16,16)))
    require(np.linalg.norm(complete-np.eye(16))<1e-12,
            'all 16 ORIGINAL ordered four-Julia outcomes trace preserving')
    return results

def report_full(factors,g):
    n=len(factors)
    histories=flag_histories(factors)
    M=projector_M(g)
    record=[]
    signed_good=0.
    for bits,K in histories.items():
        state=PSI@K.T
        mass=float(np.vdot(state,state).real)
        signed=0.
        if bits==(0,)*n:
            signed=sum(float(state[j]@M[j]@state[j]) for j in range(4))
            signed_good=signed
        qp=(mass+signed)/2
        qm=(mass-signed)/2
        require(qp>-1e-13 and qm>-1e-13,'positive original Julia flag/final bit joint outcomes')
        record.append((bits,qp,qm))
    near(sum(qp+qm for _,qp,qm in record),1.,'all16 flags + both final labels retain complete probability',tol=5e-12)
    r=sum(qp for _,qp,_ in record)
    near(r,.5+signed_good/2,'full binary report source including all failed flags',tol=3e-12)
    # The only measured classical pointer may be the final bit. If flags
    # are additionally measured, their complete CQ entropy is separate.
    hbit=-(r*math.log(r)+(1-r)*math.log(1-r))/LN_PHI
    hflagsbit=-sum(q*math.log(q) for _,u,v in record for q in (u,v) if q>0)/LN_PHI
    # Actual direct0/return10 cost: C0=1, C1=2; n Julia calls always paid.
    cost=n+1+r
    return {'r':r,'odd':signed_good,'flag_entropy':hflagsbit,
            'bit_entropy':hbit,'price_bit_cq':cost-hbit,
            'price_flags_cq':cost-hflagsbit,'report_cost':1+r,
            'all_histories':len(record)*2}

def formula_exact():
    require(ETA.T==ETA and ETA*ETA==sp.eye(4),'literal original REST-null eta symmetric involution')
    for j,g in enumerate(G):
        require(g.T*ETA+ETA*g==sp.zeros(4),f'{NAMES[j]} actual Lorentz Lie equation')
        require(sp.trace(g)==0,f'{NAMES[j]} traceless')
        for k,h in enumerate(G):
            require(sp.trace(g.T*h)==(2 if j==k else 0),f'original six trace Gram {j},{k}')
        require(ETA*g.T*ETA==-g,f'{NAMES[j]} inverse antiadjoint Frobenius test')
    for a,b,target in [(N2,M3,J),(N2,M2,B)]:
        require(a*b-b*a==target,'original null commutator exact J/B')
    x,y=sp.symbols('x y')
    for a,b,target in [(N2,M3,J),(N2,M2,B)]:
        P=(sp.eye(4)+x*a+x*x*a*a/2)*(sp.eye(4)+y*b+y*y*b*b/2)*\
          (sp.eye(4)-x*a+x*x*a*a/2)*(sp.eye(4)-y*b+y*y*b*b/2)
        require(P.diff(x).subs({x:0,y:0})==sp.zeros(4),'crossed null has zero first x P jet')
        require(P.diff(y).subs({x:0,y:0})==sp.zeros(4),'crossed null has zero first y P jet')
        require(P.diff(x).diff(y).subs({x:0,y:0})==target,'crossed null original exact mixed P jet')
        g=target
        signed=(sp.Rational(1,256)/4)*sp.trace(g.T*P)
        require(sp.simplify(signed.diff(x).diff(y).subs({x:0,y:0})-sp.Rational(1,512))==0,
                'same original Julia all-good signed mixed source 1/512')
        r=sp.Rational(1,2)+signed/2
        require(sp.simplify(r.diff(x).diff(y).subs({x:0,y:0})-sp.Rational(1,1024))==0,
                'same native complete binary report mixed source 1/1024')
    return {'original_null_gram':'2I6','analytic_ratio':'q_plus-q_minus=4^{-n} Tr(G^T R(P))/4',
            'one_link_derivative_n4':'1/512 signed, 1/1024 final reported probability',
            'crossed_null_J_and_B_mixed_derivative':'1/512 signed, 1/1024 final report'}

def run_numerical():
    from scipy.linalg import expm
    v=0.10; u=0.07
    out=[]
    for idx,g in enumerate(G):
        P=np.asarray(expm(v*np.asarray(g,float)),float)
        em=marked_probabilities(P,np.asarray(g,float),4)
        pinv=np.linalg.inv(P)
        R=(P-pinv)/2
        near(float(np.sum(np.asarray(g,float)*R)),float(np.sum(np.asarray(g,float)*P)),
             'exact Lie Frobenius orientation-odd contraction',tol=1e-12)
        out.append({'mode':NAMES[idx],'allgood_q_plus':em['plus'],'allgood_q_minus':em['minus'],
                    'odd':em['odd'],'failed_mass':em['failed']})
    results=[]
    for kind,a,b,target in [('rotation',N2,M3,J),('boost',N2,M2,B)]:
        A=np.asarray(a,float); B0=np.asarray(b,float);G0=np.asarray(target,float)
        def factors(s,t):
            return [expm(-t*B0),expm(-s*A),expm(t*B0),expm(s*A)]
        fac=factors(v,u)
        P=fac[3]@fac[2]@fac[1]@fac[0]
        nominal=marked_probabilities(P,G0,4)
        full=report_full(fac,G0)
        near(full['odd'],nominal['odd'],'full 16 Julia Kraus flags reproduce good signed all-grade PVM',tol=2e-12)
        require(full['all_histories']==32,'all16 Julia flags times two readout outcomes')
        h=1.2e-3
        vals={}
        for (ds,dt) in ((1,1),(1,-1),(-1,1),(-1,-1)):
            vals[ds,dt]=report_full(factors(ds*h,dt*h),G0)
        def mixed(key):return (vals[1,1][key]-vals[1,-1][key]-vals[-1,1][key]+vals[-1,-1][key])/(4*h*h)
        qmix=mixed('r'); bit_mix=mixed('price_bit_cq'); fine_mix=mixed('price_flags_cq')
        near(qmix,1/1024,f'{kind}: actual four-Julia crossed-null complete bit source',tol=3e-6)
        near(bit_mix,1/1024,f'{kind}: true cost minus final-bit CQ mixed source',tol=4e-6)
        results.append({'kind':kind,'actual_16flag_2pointer_records':full['all_histories'],
                        'relative_signed_odd':full['odd'],
                        'target_linear_formula_odd':nominal['odd'],
                        'mixed_report_source':qmix,'mixed_complete_final_bit_CQ_price':bit_mix,
                        'mixed_flags_also_classically_reported_CQ_price':fine_mix,
                        'full_flag_entropy_at_probe':full['flag_entropy'],
                        'full_coherent_bit_entropy_at_probe':full['bit_entropy'],
                        'report_cost':full['report_cost']})
    return {'one_link':out,'crossed_null':results}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    exact=formula_exact()
    numeric=run_numerical()
    result={'status':'PASS_NATIVE_FULLCAR_VACUUM_REFERENCE_SIGNED_SOURCE',
            'analytic':exact,'checks':len(CHECKS),'check_labels':CHECKS,
            'numeric':numeric,
            'scope':{'original_full16_exterior':True,'all_16_julia_flags_retained':True,
                     'original_NULL_Lorentz_six_generators':True,
                     'oldRIGHT128':'untouched spectator (not original Riesz input)',
                     'final_report_cost':'original direct0/return10 price1/2, fixed scheduled gate inventory',
                     'strict_Julia_chart':True,'coherent_flags_final_only_CQ':True,
                     'Book03_original_branch_Info_selected':False,
                     'native_field_to_U_writer_admitted':False,
                     'Palatini_area_coframe_source_equality':False,
                     'GR_closed':False}}
    payload=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.json:args.json.write_text(payload,encoding='utf-8')
    print(payload,end='')
if __name__=='__main__':main()
