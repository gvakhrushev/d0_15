#!/usr/bin/env python3
"""Original native Walsh-colour reduction and arbitrary first-source transport.

Uses the unchanged original CAR16/full128 constructor and owned entropy jet.
Physical dark slots remain. Only existing K1/K2 archives are evaluated.
"""
import argparse, ast, hashlib, json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.linalg import expm, solve_sylvester

parser=argparse.ArgumentParser(description=__doc__)
where=parser.add_mutually_exclusive_group()
where.add_argument('--repo-root',type=Path)
where.add_argument('--input-dir',type=Path)
parser.add_argument('--json',type=Path)
args=parser.parse_args()
source_dir=Path('02_REGISTRY/research/sources')
native_rel=source_dir/'d0_book_uniform_source_2026-10-21/check_uniform_book_source.py'
entropy_rel=source_dir/'d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py'
if args.input_dir:
    native_path=args.input_dir/native_rel.name;entropy_path=args.input_dir/entropy_rel.name
else:
    candidates=[args.repo_root.resolve()] if args.repo_root else []
    if not candidates:
        for start in (Path.cwd().resolve(),Path(__file__).resolve().parent):
            for p in (start,*start.parents):
                if p not in candidates:candidates.append(p)
    repo=next((p for p in candidates if (p/native_rel).is_file() and (p/entropy_rel).is_file()),None)
    if repo is None:parser.error('Original repository inputs missing; use --repo-root or --input-dir.')
    native_path=repo/native_rel;entropy_path=repo/entropy_rel
NATIVE_BLOB='ee8de4635d24c668949ac9a0186616ab7d59f2ed'
ENTROPY_BLOB='c133c6aec28e2a4068b36a6d9646bc8fb04fc2a4'
checks=[]
def require(ok,why):
    if not bool(ok):raise ArithmeticError(why)
    checks.append(why)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
raw=native_path.read_bytes();owned=entropy_path.read_bytes()
require(blob(raw)==NATIVE_BLOB,'unchanged actual original native constructor')
require(blob(owned)==ENTROPY_BLOB,'unchanged owned complete-CQ entropy checker')
P=(np.sqrt(5)-1)/2;ELL=-np.log(P);I=np.eye(16,dtype=complex);t=2*P**2
env=dict(np=np,expm=expm,solve_sylvester=solve_sylvester,P=P,EYE=I)
for node in ast.parse(raw).body:
    if isinstance(node,ast.FunctionDef) and node.name in {'adj','herm','tr','root','creators','native'}:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'pinned_native','exec'),env)
jets=dict(np=np,expm=expm,solve_sylvester=solve_sylvester,P=P,EYE=I,ENTROPY_ETA=1e-22)
for node in ast.parse(owned).body:
    if isinstance(node,ast.FunctionDef) and node.name in {'adj','herm','native_joint_jet','prepared','entropy_amplitude'}:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'pinned_entropy','exec'),jets)
adj=jets['adj'];herm=jets['herm'];entropy=jets['entropy_amplitude']

# Formal Walsh proof. Vector entries denote [Lboost,Rboost,I,aI,a n0,...,a n3],
# a=sqrt(1-nu^2)-1. No numerical matrix or square root enters these identities.
def vv(*entries):return np.array([F(x) for x in entries],dtype=object)
zero=np.array([F(0)]*8,dtype=object)
words=[]
for d in range(4):
    L0=zero.copy();L0[2]=1;L0[4+d]=1
    R0=zero.copy();R0[2]=1;R0[3]=1;R0[4+d]=-1
    L=L0.copy();R=R0.copy()
    if d==1:
        L=zero.copy();L[0]=1;R=zero.copy();R[1]=1
    for w in (L,R,-L0,-R0):words.extend((w.copy(),w.copy()))
formal=[]
for label in range(32):
    formal.append(sum(((-1)**((label&j).bit_count()&1)*words[j] for j in range(32)),zero.copy())/32)
JA=[1,17,25,33,41,49,57];SA=[1,-1,-1,1,1,-1,-1]
JB=[5,21,37,53];SB=[1,-1,1,-1]
for row,sgn in zip(JA,SA):require(np.array_equal(formal[row//2],sgn*formal[0]),f'exact open-chart seven-colour Walsh row {row}')
for row,sgn in zip(JB,SB):require(np.array_equal(formal[row//2],sgn*formal[2]),f'exact open-chart four-colour Walsh row {row}')
require(all(np.array_equal(formal[j],zero) for j in range(1,32,2)),'all 32 physical dark rows are exact duplicate-word cancellations')
Dplus=zero.copy();Dplus[0]=F(1);Dplus[1]=F(1);Dplus[2]=F(-2);Dplus[3]=F(-1)
Dminus=zero.copy();Dminus[0]=F(1);Dminus[1]=F(-1);Dminus[3]=F(1);Dminus[5]=F(-2)
require(np.array_equal(formal[0],Dplus/16),'exact representative N1=Dplus/16')
require(np.array_equal(formal[2],Dminus/16),'exact representative N5=Dminus/16')

r=1/9;nu=.6;theta=2*np.arctanh(r);dtheta=2/(1-r*r)
k,kr,rows=jets['native_joint_jet'](env,theta,nu,dtheta,0.)
native,native_theta=env['native'](theta,nu)
require(np.linalg.norm(k-native)<1e-14 and np.linalg.norm(kr-dtheta*native_theta)<1e-13,'actual unchanged native matrices and proper boost jet')
delta,delta_r,rho,rho_r,Z=jets['prepared'](k,kr)
h=16/Z;hr=np.trace(rho_r@delta+rho@delta_r).real
dnu=-nu*hr/(2*h)
_,kv,_=jets['native_joint_jet'](env,theta,nu,dtheta,dnu)
_,_,_,rho_v,_=jets['prepared'](k,kv)
def port_merge(a):return np.concatenate((a[:2],a[2::2]/P))
m=port_merge(k);mr=port_merge(kr);mv=port_merge(kv)
GA=[j+1 for j in JA];GB=[j+1 for j in JB]
used=set(GA+GB)
groups=[(GA,SA),(GB,SB)]+[([j],[1]) for j in range(65) if j not in used]
groups.sort(key=lambda g:min(g[0]))
def compress(a,da):
    out=[];dout=[]
    for labels,signs in groups:
        n=len(labels);representative=a[labels[0]]
        out.append(np.sqrt(n)*representative)
        dout.append(sum((sgn*da[j] for j,sgn in zip(labels,signs)),np.zeros_like(I))/np.sqrt(n))
    return np.asarray(out),np.asarray(dout)
for labels,signs in ((GA,SA),(GB,SB)):
    for j,sgn in zip(labels,signs):
        require(np.linalg.norm(m[j]-sgn*m[labels[0]])<2e-15,'actual Kraus scalar-colour identity')
        require(np.linalg.norm(mr[j]-sgn*mr[labels[0]])<2e-14 and np.linalg.norm(mv[j]-sgn*mv[labels[0]])<2e-14,'both actual colour source identities')
live=[j for j in range(65) if np.count_nonzero(m[j])]
c,cr=compress(m,mr);_,cv=compress(m,mv)
require(len(live)==33 and len(c)==56 and sum(np.count_nonzero(x)>0 for x in c)==24,'128 original slots,65 merged slots,56 readout classes,24 live computational branches')
require(np.linalg.norm(sum((adj(x)@x for x in c),np.zeros_like(I))-I)<2e-14,'compressed CP channel is complete at the native anchor')

def count_effect(a,da):
    D=np.zeros_like(I);dD=np.zeros_like(I)
    for labels in (GA,GB):
        for j in labels:
            D+=np.log(len(labels))*adj(a[j])@a[j]
            dD+=np.log(len(labels))*(adj(da[j])@a[j]+adj(a[j])@da[j])
    return herm(D),herm(dD)
def counter(a,da,depth):
    D,dD=count_effect(a,da);F0=np.zeros_like(I);dF0=np.zeros_like(I)
    for _ in range(depth):
        dF0=dD+sum((adj(dx)@F0@x+adj(x)@dF0@x+adj(x)@F0@dx for x,dx in zip(a,da)),np.zeros_like(I))
        F0=D+sum((adj(x)@F0@x for x in a),np.zeros_like(I))
    return F0,herm(dF0)
def archive(a,da,drho,depth):
    ev,u=np.linalg.eigh(rho);root=(u*np.sqrt(ev))@adj(u)
    droot=solve_sylvester(root,root,drho)
    nodes=[(root,droot)]
    pairs=[(x,dx) for x,dx in zip(a,da) if np.count_nonzero(x) or np.count_nonzero(dx)]
    for _ in range(depth):nodes=[(x@y,dx@y+x@dy) for y,dy in nodes for x,dx in pairs]
    s=ds=normjet2=0.
    for x,dx in nodes:
        v,dv=entropy(x,dx,1e-22);s+=v;ds+=dv;normjet2+=np.vdot(dx,dx).real
    bound=4*np.sqrt(16*len(a)**depth*1e-22)*np.sqrt(normjet2)
    return s,ds,bound

# An exact complete-amplitude tangent that deliberately breaks colour equality.
# It is a hostile ambient algebra check, not a claimed native field writer.
T=np.zeros((65,65))
T[GA[1],0]=1/7;T[0,GA[1]]=-1/7
T[GB[1],10]=1/11;T[10,GB[1]]=-1/11
ma=np.einsum('ab,bij->aij',T,m)
rho_a=np.zeros_like(I);rho_a[0,0]=.01;rho_a[1,1]=-.01;rho_a[0,1]=rho_a[1,0]=.003
require(np.linalg.norm(sum((adj(dx)@x+adj(x)@dx for x,dx in zip(m,ma)),np.zeros_like(I)))<2e-14,'hostile output-unitary amplitude jet is trace preserving')
require(np.linalg.norm(ma[GA[1]]-SA[1]*ma[GA[0]])>.1,'hostile ambient jet truly breaks the seven-colour proportionality')
cases={};per_tick={}
for name,dm,drho in [('r',mr,rho_r),('v_one_port_null',mv,rho_v),('ambient_TP_plus_preparation',ma,rho_a)]:
    cc,dcc=compress(m,dm);D,dD=count_effect(m,dm)
    # Full CP first jets, including noncommuting and odd-preparation inputs.
    sigma=rho+rho_a
    lhs=sum((dx@sigma@adj(x)+x@sigma@adj(dx) for x,dx in zip(m,dm)),np.zeros_like(I))
    rhs=sum((dx@sigma@adj(x)+x@sigma@adj(dx) for x,dx in zip(cc,dcc)),np.zeros_like(I))
    require(np.linalg.norm(lhs-rhs)<2e-14,f'actual grouped CP first jet equals averaged Kraus jet {name}')
    per_tick[name]={'colour_entropy':float(np.trace(rho@D).real),'colour_source':float(np.trace(drho@D+rho@dD).real)}
    cases[name]=[]
    for depth in (1,2):
        s,ds,bnd=archive(m,dm,drho,depth);sc,dsc,cbnd=archive(cc,dcc,drho,depth)
        F0,dF0=counter(m,dm,depth)
        expected=float(np.trace(rho@F0).real)
        source=float(np.trace(drho@F0+rho@dF0).real)
        require(abs(s-sc-expected)<3e-12 and abs(ds-dsc-source)<3e-11,
                f'actual K{depth} colour entropy and full first-source counter {name}')
        cases[name].append(dict(K=depth,merged_CQ=s,compressed_CQ=sc,colour_difference=s-sc,
                               merged_source=ds,compressed_source=dsc,colour_source=ds-dsc,
                               operator_counter=expected,operator_source=source,
                               smoothing_source_bound=bnd+cbnd))

# Closed scalar consumer: no long-history enumeration is needed for this entire
# colour source. The two Julia-defect differences have disjoint supports.
cboost=np.cosh(2*theta);dcboost=2*np.sinh(2*theta)*dtheta
sroot=np.sqrt(1-nu*nu);uroot=np.sqrt(1-nu*nu*cboost)
chi=(cboost+1)/(2*cboost);dchi=-dcboost/(2*cboost*cboost)
aa=uroot-1;bb=sroot-1
froot=aa*aa+bb*bb-aa*bb*(1+chi)
qcolour=t*h*froot/256
colour_factor=7*np.log(7)+4*np.log(4)
closed_scalar={}
for name,dn,dh in [('r',0.,hr),('v_one_port_null',dnu,0.)]:
    ds=-nu*dn/sroot
    du=-(2*nu*dn*cboost+nu*nu*dcboost)/(2*uroot)
    df=2*aa*du+2*bb*ds-(du*bb+aa*ds)*(1+chi)-aa*bb*dchi
    dq=t*(dh*froot+h*df)/256
    require(abs(qcolour*colour_factor-per_tick[name]['colour_entropy'])<2e-16 and
            abs(dq*colour_factor-per_tick[name]['colour_source'])<2e-14,
            f'closed two-mode Julia scalar value and source {name}')
    closed_scalar[name]=dict(single_colour_probability=qcolour,single_colour_probability_source=dq,
                             entropy_per_tick=qcolour*colour_factor,source_per_tick=dq*colour_factor)

# A genuine infinite family of distinguishable filters already occurs on blank words.
evals=np.linalg.eigvalsh(delta);lamlo=float(evals[0]);lamhi=float(evals[-1])
require(0<lamlo<lamhi<1/t,'native blank has two different positive strict survival eigenvalues')
blank_predictions=[]
for n in (0,1,2,4,8,16):
    X=np.linalg.matrix_power(k[0],n)@rho@np.linalg.matrix_power(k[0],n)
    blank_predictions.append(float(np.trace(k[0]@X@k[0]).real/np.trace(X).real))
require(all(a<b for a,b in zip(blank_predictions,blank_predictions[1:])),'actual blank-conditioned filters have distinct next-blank predictions')
result=dict(scope='new native seven/four Walsh colour refinement with full first-jet substitution; no finite filter claim',
            original_native_blob=NATIVE_BLOB,owned_entropy_blob=ENTROPY_BLOB,
            colour_SELECT_groups={'seven':JA,'four':JB},merged_label_groups={'seven':GA,'four':GB},
            signs={'seven':SA,'four':SB},physical_original_slots=128,physical_port_merged_slots=65,
            readout_classes_including_dark=56,live_computational_branches=24,
            exact_formal_Walsh_identities=True,arbitrary_retained_reference=True,
            cases=cases,stationary_per_tick=per_tick,
            closed_two_mode_Julia_scalar=closed_scalar,
            stationary_K4096_colour={name:{key:4096*value for key,value in data.items()} for name,data in per_tick.items() if name!='ambient_TP_plus_preparation'},
            blank_predictions=blank_predictions,
            preparation_score='F_K=sum_{n=0}^{K-1}(Phi*)^n [ln7 C7+ln4 C4]',
            physical_field_writer_selected=False,finite_filter_closure=False,
            arbitrary_jet_transport_order=1,C2_rank_birth_claim=False,
            checks_passed=len(checks),checks=checks,GR_closed=False)
output=json.dumps(result,indent=2)+'\n'
if args.json:args.json.write_text(output,encoding='utf-8')
print(output,end='')
