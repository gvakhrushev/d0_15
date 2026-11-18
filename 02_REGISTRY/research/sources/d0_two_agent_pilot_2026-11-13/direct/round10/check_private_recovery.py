#!/usr/bin/env python3
"""Literal NPS private-dilation recovery on all Spin/phase input columns.

Every emitted raw primitive is executed numerically. Exact support and
recursion are proved in the companion note; this finite fixture is not H.1.
"""
from pathlib import Path
import argparse,json,hashlib,math
import numpy as np
import mpmath as mp
import nps_private_recovery as nr

checks=[]
def ck(ok,label):
    if not bool(ok):raise ArithmeticError(label)
    checks.append(label)

def mm(a,b):return np.einsum('ij,jk->ik',a,b,optimize=False)

parser=argparse.ArgumentParser()
parser.add_argument('--spin-coupled',action='store_true')
args=parser.parse_args()
base=nr.fixture(twist_spin=args.spin_coupled);nt=nr.native
pf=float(nt.P);af=float(nt.A)
v=np.array([af,pf]);G=np.array([[af,-pf],[pf,af]])
G3=mm(mm(G,G),G);W=mm(mm(G3.T,np.diag([1.,-1.])),G3)
u,d=(af+pf)/2,(af-pf)/2
K=[u*W+d*np.eye(2),u*W-d*np.eye(2)]
branches=[mm(k,v[:,None])[:,0] for k in K]
probs=[float(np.dot(x,x)) for x in branches]
af8=np.kron(G3,np.eye(4))
ab8=mm(np.array(nt.SOURCE_I_LOCAL,dtype=float),af8) if args.spin_coupled else af8
ww=mm(mm(ab8.T,np.kron(np.diag([1.,-1.]),np.eye(4))),af8)
vv=mm(ab8.T,af8)
jbank=np.kron(v[:,None],np.eye(4))
bank_branches=[mm(u*ww+d*vv,jbank),mm(u*ww-d*vv,jbank)]
for b in (0,1):
    ck(np.linalg.norm(mm(bank_branches[b].T,bank_branches[b])-probs[b]*np.eye(4))<2e-14,
       'actual independent backward map retains full scalar effect')
if args.spin_coupled:
    Li=np.array(nt.L_I,dtype=float)
    for br in bank_branches:
        coeffI=np.array([np.trace(br[k*4:(k+1)*4])/4 for k in range(2)])
        coeffL=np.array([np.trace(mm(Li.T,br[k*4:(k+1)*4]))/4 for k in range(2)])
        determinant=np.dot(coeffI,coeffI)*np.dot(coeffL,coeffL)-np.dot(coeffI,coeffL)**2
        ck(determinant>1e-5,'Spin-coupled branch has independent I and Li bank coefficients; WORK-only recovery insufficient')
q=pf**2+pf**3*float(mm(G3,v[:,None])[1,0]**2)
ck(abs(probs[1]-q)<2e-15 and pf**2<q<.5,'literal G^3 NPS has the original nontrivial collar probability')
ck(len(base.gates)==(63 if args.spin_coupled else 60),'all original fixture NPS/encoder/echo calls retained')

N=1<<base.qubits;indices=np.arange(N)
def bit(q):return 1<<(base.qubits-1-q)
cache={}
def apply(word,states):
    states=states.copy()
    for g in word:
        if g not in cache:
            if g.op=='G':
                lo=indices[(indices&bit(g.wires[0]))==0]
                cache[g]=(lo,lo^bit(g.wires[0]))
            elif g.op=='CX':
                c,t=g.wires;cache[g]=indices^np.where(indices&bit(c),bit(t),0)
            else:
                local=np.array(nt.SOURCE_I_LOCAL,dtype=float)
                inv=np.empty(N,dtype=int);sign=np.empty(N)
                for col in range(N):
                    loc=sum(int(bool(col&bit(w)))<<(2-j) for j,w in enumerate(g.wires))
                    rowloc=int(np.flatnonzero(local[:,loc])[0]);row=col
                    for j,w in enumerate(g.wires):
                        if ((rowloc^loc)>>(2-j))&1:row^=bit(w)
                    inv[row]=col;sign[row]=local[rowloc,loc]
                cache[g]=(inv,sign)
        if g.op=='G':
            lo,hi=cache[g];a,b=states[lo].copy(),states[hi].copy()
            states[lo]=af*a-pf*b;states[hi]=pf*a+af*b
        elif g.op=='CX':states=states[cache[g]]
        else:
            inv,sign=cache[g];states=states[inv]*sign[:,None]
    return states

def ket(parts):
    out=np.array([1.])
    for p in parts:out=np.kron(out,p)
    return out
e=np.eye(2)
labels=[(b,spin,h) for b in range(2) for spin in range(4) for h in range(2)]
J=np.column_stack([ket([v,e[(s>>1)&1],e[s&1],v,v,e[b],e[0],e[h]]) for b,s,h in labels])
def branch_input(b,s,h,private_ready):
    out=np.zeros(N)
    for k in range(8):
        coefficient=bank_branches[b][k,s]/math.sqrt(probs[b])
        out+=coefficient*ket([e[k//4],e[(k>>1)&1],e[k&1],e[b] if private_ready else v,
                             e[0] if private_ready else v,e[b],e[0],e[h]])
    return out
V=np.column_stack([branch_input(b,s,h,True) for b,s,h in labels])
fresh=np.column_stack([branch_input(b,s,h,False) for b,s,h in labels])
ck(np.linalg.norm(mm(J.T,J)-np.eye(16))<1e-14,'complete Spin/record/phase input embedding is isometric')
ck(np.linalg.norm(mm(V.T,V)-np.eye(16))<1e-14,'all normalized noisy branch maps are isometries')
actual=apply(base.gates,J)
goodmask=np.array([int(bool(k&bit(3)))==int(bool(k&bit(5))) for k in indices])
expected=V*np.array([math.sqrt(probs[b]) for b,_,_ in labels])[None,:]
ck(np.linalg.norm(actual*goodmask[:,None]-expected)<2e-13,'actual square NPS word supplies the required scalar branch on every input column')

mp.mp.dps=90
rows=[]
for n in range(3):
    plan=nr.private_recovery(base,processor_blanks=(0,3,4),record=5,pointer=3,
                             tail=4,rebit=7,rounds=n,protected=(6,))
    prepared=apply(plan['private_preparation'],fresh)
    ck(np.linalg.norm(prepared-V)<2e-13,'literal fresh private preparation gives V_b without altering exterior report')
    recovered=apply(plan['recovery'],prepared)
    overlap=mm(J.T,recovered)
    cert=plan['phase_certificate']
    # atan2(p,sqrt p), independently computed from the original gate.
    pmp=(mp.sqrt(5)-1)/2;angle=int(cert['angle_multiplier'])*mp.atan2(pmp,mp.sqrt(pmp))
    t=mp.exp(1j*angle);a0=2*(1-mp.re(t));b0=2*mp.re(t)-1
    zs=[];epss=[]
    expected_corner=np.zeros((16,16))
    for b in range(2):
        eps=mp.mpf(str(1-probs[b]));z=mp.sqrt(1-eps)
        for _ in range(n):
            z=z*t*(t+a0*eps);eps=eps*(b0+a0*eps)**2
        zs.append(z);epss.append(eps)
        for spin in range(4):
            at=(b*4+spin)*2
            # A_n dagger has conjugate(z) on the retained phase rebit.
            rr,ii=float(mp.re(z)),float(mp.im(z))
            expected_corner[at:at+2,at:at+2]=[[rr,ii],[-ii,rr]]
    err=np.linalg.norm(overlap-expected_corner)
    tol=1e-11+len(plan['recovery'])*1e-14
    ck(err<tol,'literal all-input recovery corner equals conjugate(z_n(q_b))')
    ck(np.linalg.norm(mm(recovered.T,recovered)-np.eye(16))<tol,'entire failed output retained; no postselection/reset')
    failure=recovered-mm(J,overlap)
    expected_gram=np.diag([float(epss[b]) for b,_,_ in labels])
    ck(np.linalg.norm(mm(failure.T,failure)-expected_gram)<tol,'full complementary failure Gram has exactly the original recursion')
    # Record/outer tail never targeted by any literal gate in the whole new word.
    ck(all(6 not in g.wires for g in plan['private_preparation']+plan['recovery']), 'outer tail is untouched by actual recovery')
    stream='\n'.join(g.op+':'+','.join(map(str,g.wires)) for g in plan['private_preparation']+plan['recovery'])+'\n'
    rows.append({'round':n,'actual_raw_counts':nr.counts(plan['private_preparation']+plan['recovery']),
                 'amplifier_levels':plan['levels'],'stable_phase_multiplier':int(cert['angle_multiplier']),
                 'private_preparation_calls':len(plan['private_preparation']),
                 'branch_failure_probabilities':[mp.nstr(x,30) for x in epss],
                 'branch_good_coefficients':[[mp.nstr(mp.re(z),30),mp.nstr(mp.im(z),30)] for z in zs],
                 'all_input_corner_error_frobenius':float(err),'native_stream_sha256':hashlib.sha256(stream.encode()).hexdigest()})

# Negative control: omitting the private r' copy is not the normalized V_b.
no_copy=apply(plan['private_preparation'][:-1],fresh)
ck(np.linalg.norm(no_copy-V)>1,'private record re-encoding is necessary and paid')
print(json.dumps({'status':'PASS_LITERAL_NPS_PRIVATE_DILATION_RECOVERY','checks':len(checks),
 'Spin_coupled_backward_centre':args.spin_coupled,'WORK_only_recovery_assumed':False,
 'q_fixture':q,'fixture_square_NPS_calls':len(base.gates),'all_input_columns':16,
 'opaque_Spin_columns':4,'phase_input_columns':2,'exterior_report_branches':2,
 'rounds':rows,'phase_correction_and_final_bright_target_in_this_replay':False,
 'full_geometric_H1_replayed':False,'physical_C_closed':False,'GR_closed':False},indent=2))
