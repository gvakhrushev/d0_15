#!/usr/bin/env python3
"""Full 4-step ORIGINAL CAR16 Julia-flag Cost-CQ two-jet, not a Book03 law.

Every one of 16 fine Julia flags, the final direct0/return10 label, and
all reference/work are retained. An 8-slot fair selector has six true
Lorentz probes and two paid dummy ports. The mathematical Julia link
isometry/field access is SUPPLIED, not derived from an M1 native writer.
"""
from __future__ import annotations
import argparse, itertools, json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
import sympy as sp

P=(math.sqrt(5)-1)/2
LNPHI=math.log(1/P)
GIN=[]
CHECKS=[]

def check(ok,label):
    if not bool(ok):raise ArithmeticError(label)
    CHECKS.append(label)

def near(x,y,label,tol=1e-11):
    check(abs(complex(x-y)) <= tol, label+f': err={abs(complex(x-y)):.3g}')

def E(a,b):
    x=np.zeros((4,4),float);x[a,b]=1.;return x
G=[E(1,2)+E(2,0), E(1,3)+E(3,0),
   E(0,2)+E(2,1), E(0,3)+E(3,1),
   E(2,3)-E(3,2), E(1,1)-E(0,0)]
NAMES=['N2','N3','barN2','barN3','J','B']
ETA=np.array([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]],float)
EXTERIOR_ORDER=(0,2,3,1)
SIGN={k:(-1)**sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq))) for k in range(16) for seq in [[j for j in EXTERIOR_ORDER if k&(1<<j)]]}
SEED=np.zeros((4,16),complex)
for j in range(4):
    SEED[j,0]=1/math.sqrt(8)
    SEED[j,1<<j]=1/math.sqrt(8)
check(abs(np.vdot(SEED,SEED)-1)<1e-14,'original grade0/1 four-reference seed norm 1')


def exterior16(U):
    X=np.zeros((16,16),float)
    for i in range(16):
        rows=[a for a in range(4) if i&(1<<a)]
        for j in range(16):
            cols=[a for a in range(4) if j&(1<<a)]
            if len(rows)!=len(cols):continue
            X[i,j]=SIGN[i]*SIGN[j]*(np.linalg.det(U[np.ix_(rows,cols)]) if rows else 1)
    return X


def jpair(U):
    T=exterior16(U)/2
    A=np.eye(16)-T.T@T
    eig,V=np.linalg.eigh((A+A.T)/2)
    check(eig.min()>0.1,'original full-CAR Julia strict positive defect')
    D=(V*np.sqrt(eig))@V.T
    near(np.linalg.norm(T.T@T+D.T@D-np.eye(16)),0,'all16 CAR exact Julia effect completeness',5e-12)
    return T,D


def score_M(a):
    M=np.zeros((4,16,16),float)
    if a<6:
        g=G[a]
        for j in range(4):
            for i in range(4):
                M[j,0,1<<i]=g[i,j]
                M[j,1<<i,0]=g[i,j]
            check(float(np.sum(g[:,j]**2)) in (0.,1.), 'native null Lorentz generator column norms')
    return M


def allflag_data(units):
    pairs=[jpair(U) for U in units]
    # Return a purification for all actual chronological good/bad records.
    records=[]
    for bits in itertools.product((0,1),repeat=4):
        K=np.eye(16)
        for pair,b in zip(pairs,bits):K=pair[b]@K
        s=SEED@K.T
        q=float(np.vdot(s,s).real)
        records.append((bits,s,q))
    near(sum(q for _,_,q in records),1.,'all 16 Julia flags, all 16 CAR grades and retained REF unit mass',5e-12)
    return records


def entropy_phi(values):
    return -sum(x*math.log(x) for x in values if x>0)/LNPHI


def trial(units, select=None):
    rows=allflag_data(units)
    groups=range(8) if select is None else [select]
    results=[]
    for a in groups:
        M=score_M(a)
        joint=[]
        C=0.
        for bits,s,q in rows:
            signed=0.
            if bits==(0,0,0,0):
                signed=sum(float(np.vdot(s[j],M[j]@s[j]).real) for j in range(4))
            for b in (0,1):
                p_out=(q+(signed if b else -signed))/2
                check(p_out>-1e-13,'fine Julia failure/final report positive')
                joint.append(p_out)
                # True terminal direct0 / return10 Cost (1, 2); extra
                # status costs intentionally unequal across stages to test
                # their expected-source cancellation on the primary slice.
                paid=3+sum((1+j%2)+(2 if bit else 0) for j,bit in enumerate(bits))+(1+b)
                C+=p_out*paid
        near(sum(joint),1.,'all fine Julia/readout labels complete and normalized',4e-12)
        results.append({'entropy':entropy_phi(joint),'cost':C,'price':C-entropy_phi(joint),
                        'final_click':sum(joint[1::2])})
    if select is not None:return results[0]
    H=math.log(8)/LNPHI+sum(x['entropy'] for x in results)/8
    cost=sum(x['cost'] for x in results)/8
    return {'entropy':H,'cost':cost,'price':cost-H,
            'final_click':sum(x['final_click'] for x in results)/8}


def four_commutator(a,b,s,t):
    return [expm(-t*b),expm(-s*a),expm(t*b),expm(s*a)]


def mixed(fun,h):
    return (fun(h,h)-fun(h,-h)-fun(-h,h)+fun(-h,-h))/(4*h*h)


def tests():
    for a in range(6):
        near(np.linalg.norm(G[a].T@ETA+ETA@G[a]),0,'original null Lorentz Lie generator')
        for b in range(6):
            near(np.sum(G[a]*G[b]),2*(a==b),'six native real Frobenius Gram')
    # The original vacuum-reference trace is grade0 1/2, grade1 I4/8.
    rho=SEED.T.conj()@SEED
    near(np.linalg.norm(np.diag(np.diag(rho)[[0,1,2,4,8]])-np.diag([.5,.125,.125,.125,.125])),0,
         'reference trace has exact maxmix grade1 diagonal')
    h=.001
    baseline=trial([np.eye(4)]*4)
    near(baseline['final_click'],.5,'all flag results and eight selector final baseline is fair')
    sources=[]
    for b in range(6):
        vals=[]
        for sign in (-1,1):
            u=[np.eye(4)]*3+[expm(sign*h*G[b])]
            vals.append(trial(u))
        dc=(vals[1]['cost']-vals[0]['cost'])/(2*h)
        dh=(vals[1]['entropy']-vals[0]['entropy'])/(2*h)
        dp=(vals[1]['price']-vals[0]['price'])/(2*h)
        expected=1/(32*256)
        near(dc,expected,f'8-slot whole fine direct0/return10 first source {NAMES[b]}',2e-9)
        near(dh,0.,f'ALL fine flags and report entropy first source zero {NAMES[b]}',2e-9)
        near(dp,expected,f'complete fine-CQ Cost-minus-Info first source {NAMES[b]}',3e-9)
        sources.append(dp)
    data=[]
    for label,a,b,target in [('J',G[0],G[3],4),('B',G[0],G[2],5)]:
        f=lambda s,t:trial(four_commutator(a,b,s,t),select=target)
        out={key:mixed(lambda s,t:f(s,t)[key],h) for key in ('cost','entropy','price','final_click')}
        expected=1/1024
        near(out['final_click'],expected,f'{label} noncommuting null Lorentz mixed report source',2e-10)
        near(out['cost'],expected,f'{label} full fine status-cost plus report mixed source',2e-8)
        near(out['entropy'],0.,f'{label} full fine CQ entropy crossed-null mixed source vanishes',2e-8)
        near(out['price'],expected,f'{label} full Cost-CQ mixed source retains orientation',2e-8)
        data.append({'commutator':label,'mixed':out,'expected':expected})
    # Symbolic, rather than finite-difference, closed mixed-jet proof.
    x,y=sp.symbols('x y')
    gen={name:sp.Matrix([[int(e) for e in row] for row in z]) for name,z in zip(NAMES,G)}
    for a,b,t in [(gen['N2'],gen['barN3'],gen['J']),
                  (gen['N2'],gen['barN2'],gen['B'])]:
        Pmat=(sp.eye(4)+x*a+x*x*a*a/2)*(sp.eye(4)+y*b+y*y*b*b/2)*\
             (sp.eye(4)-x*a+x*x*a*a/2)*(sp.eye(4)-y*b+y*y*b*b/2)
        check(Pmat.diff(x).subs({x:0,y:0})==sp.zeros(4),'commutator has no first x holonomy')
        check(Pmat.diff(y).subs({x:0,y:0})==sp.zeros(4),'commutator has no first y holonomy')
        check(Pmat.diff(x).diff(y).subs({x:0,y:0})==t,'original exact crossed null commutator')
        q=sp.Rational(1,2)+sp.Rational(1,256*8)*sp.trace(t.T*Pmat)
        check(sp.factor(q.diff(x).diff(y).subs({x:0,y:0})-sp.Rational(1,1024))==0,
              'exact full-CAR first mixed signed Born coefficient')
    # ORIGINAL complete n=4 Julia flags: reconstruct the entire nonlinear
    # based Lorentz-odd curvature from SIX positive final-port differences.
    # No log odds, trace(P) division, local inverse or dropped failures.
    factors=[expm(.035*G[0]),expm(-.028*G[4]),
             expm(.031*G[2]),expm(.022*G[5])]
    Pword=np.eye(4)
    for U in factors:Pword=U@Pword
    means=[trial(factors,select=a)['final_click'] for a in range(6)]
    Rhat=4*4**4*sum(((q-.5)*G[a] for a,q in enumerate(means)),np.zeros((4,4)))
    Rexact=(Pword-np.linalg.inv(Pword))/2
    near(np.linalg.norm(Rhat-Rexact),0,
         'EXACT nonlinear original 6 signed paid-port contrasts reconstruct full Lorentz odd curvature',2e-11)
    back=[np.linalg.inv(U) for U in factors[::-1]]
    opposite=[trial(back,select=a)['final_click'] for a in range(6)]
    for a in range(6):
        near(means[a]+opposite[a],1.,
             f'full paid signed positive port probabilities reverse under P inverse {a}',4e-13)
    eight=trial(factors)
    near(eight['final_click'],(.5+sum(q-.5 for q in means)/8),
         'one genuine eight-slot fully normalized positivity experiment',3e-13)
    return {'status':'PASS_FINE_JULIA_FLAG_COST_CQ_ORIENTED_FIRST_AND_MIXED',
            'check_count':len(CHECKS),'first_six':sources,'commutators':data,
            'baseline':baseline,'scope':{
            'full16_CAR_exterior':True,'16_julia_flag_histories':True,'all_eight_selector_labels':True,
            'fine_flags_reported':True,'old_RIGHT_reference4_pure_seed':True,
            'old_RIGHT128_native_Riesz_preparation':False,
            'status_charge':'fixed prescribed per-stage flag price; not complete Book03',
            'full_native_CAR_writer':False,'Book03_Info_selected':False,
            'GR_closed':False}}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    payload=json.dumps(tests(),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    print(payload,end='')
    if args.json:args.json.write_text(payload,encoding='utf-8')
