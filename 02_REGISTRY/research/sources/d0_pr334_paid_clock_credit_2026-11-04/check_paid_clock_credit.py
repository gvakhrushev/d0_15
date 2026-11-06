"""Actual CX padding: primitive Cost floor versus the full Book clock price.

The theorem states the credit required of Info minus additional work; it does
not select either functional or assert physical admission of all durations.
The finite lower gap additionally assumes a declared record-entropy cap.
"""
from pathlib import Path
from fractions import Fraction
from math import factorial
import argparse,hashlib,importlib.util,json,sys
import sympy as S
import numpy as np

pa=argparse.ArgumentParser();pa.add_argument('--out',type=Path);args=pa.parse_args()
checks=[];root=Path.cwd()
def require(ok,name):
    if not bool(ok):raise ArithmeticError(name)
    checks.append(name)
a=S.Symbol('a',positive=True);p=a*a;minimal=a**4+a*a-1
def red(x):
    n,d=S.fraction(S.cancel(x));n=S.rem(n,minimal,a);d=S.rem(d,minimal,a)
    if d==0:raise ArithmeticError('zero Golden denominator')
    return S.rem(S.expand(n*S.invert(d,minimal,a)),minimal,a)
def mat(M):return S.Matrix(M).applyfunc(red)
def equal(x,y,name):
    if isinstance(x,S.MatrixBase) or isinstance(y,S.MatrixBase):
        require(all(red(z)==0 for z in S.Matrix(x)-S.Matrix(y)),name)
    else:require(red(x-y)==0,name)
v=S.Matrix([a,p]);w=S.Matrix([-p,a]);G=S.Matrix([[a,-p],[p,a]])
CX=S.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
psi=S.kronecker_product(v,v);chi=mat(CX*psi)
target1=S.diag(0,1,0,1)
equal((psi.T*target1*psi)[0],p*p,'actual first Golden pair target probability')
equal((chi.T*target1*chi)[0],2*p**3,'actual copied target probability')
gap=red((chi.T*target1*chi-psi.T*target1*psi)[0])
equal(gap,5*p-3,'same native future bit test separates every adjacent padding state')
require(Fraction(3,5)+Fraction(3,5)**2<1<Fraction(5,8)+Fraction(5,8)**2,
        'strict rational Golden interval 3/5 < p < 5/8')
equal(CX*CX,S.eye(4),'second actual CX restores the entire input, not just its probability')
equal((psi.T*psi)[0],1,'canonical padding preparation is normalized')
equal((chi.T*chi)[0],1,'every failed/readable amplitude is retained')

native_path=root/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
require(hashlib.sha256(native_path.read_bytes()).hexdigest()==
        '222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c','native grammar pin')
spec=importlib.util.spec_from_file_location('clock_credit_native',native_path)
native=importlib.util.module_from_spec(spec);sys.modules[spec.name]=native;spec.loader.exec_module(native)
Gate=native.Gate
def word(m):
    return native.Execution(6,(),(3,),tuple([Gate('CX',(4,5))]*(2*m)+[Gate('G',(0,))]),
                            native.G_CX_SOURCE_I,0,(1,2))
word_payload={};inventories={}
old_end=native.word_matrix(word(0),max_qubits=6,max_expanded_stages=2049)
for m in (0,1,2,1024):
    ex=word(m);native.validate_execution(ex,max_qubits=6,max_expanded_stages=2049)
    inv=native.inventory(ex,max_qubits=6,max_expanded_stages=2049)
    require((inv.gate_count,inv.g_count,inv.cx_count,inv.source_i_count)==(2*m+1,1,2*m,0),
            'every actual forward stage counted m='+str(m))
    require(all(ex.gates[j:j+2]==(Gate('CX',(4,5)),)*2 for j in range(0,2*m,2)),
            'literal pair cancellation certificate m='+str(m))
    require(all(3 not in g.wires and not set((1,2)).intersection(g.wires) for g in ex.gates),
            'opaque Spin and immutable oldRIGHT m='+str(m))
    if m<=2:
        U=native.word_matrix(ex,max_qubits=6,max_expanded_stages=2049)
        require(native.exact_matrix_equal(U,old_end),'all 64 endpoint columns m='+str(m))
    N=2*m+3;D=16+32+64*(2*m+1)
    require(D==112+128*m==16*N+16*(N-1)+32*(N-2),'true growing-clock dimensions m='+str(m))
    inventories[str(m)]={'calls':2*m+1,'births':2,'N':N,'clock_dimension':D,
                         'full_Hodge_modes':425*D,'harmonic_modes':359*D,'input_rank':16,
                         'primitive_padding_Cost_floor':2*m}
    word_payload[str(m)]={'execution':native.execution_to_dict(ex),
       'birth_schedule':{'initial_wires':[0,1,2,3],
                         'canonical_births_before_calls':[4,5],'vector':['a','a^2']}}

J=S.kronecker_product(S.eye(16),v,v)
Usym=S.kronecker_product(G,S.eye(32))
C=mat(J.T*Usym*J)
equal(C,S.kronecker_product(G,S.eye(8)),'actual cold operator retains every old input')
equal(C.T*C,S.eye(16),'feedback is exactly zero on this probe at every paid duration')

# Direct original growing clocks, including both birth-detail layers and the
# real intermediate CX gates. No homogeneous padding clock is substituted.
for m in (0,1):
    dims=[2,4]+[8]*(2*m+1);N=len(dims);offs=np.cumsum([0]+dims).tolist();Dsmall=sum(dims)
    F0=S.kronecker_product(S.eye(2),v);F1=S.kronecker_product(S.eye(4),v)
    Fs=[F0,F1]+[S.kronecker_product(S.eye(2),CX)]*(2*m)
    T=S.zeros(Dsmall)
    for j,F in enumerate(Fs):T[offs[j+1]:offs[j+2],offs[j]:offs[j+1]]=F
    R=S.zeros(Dsmall,8)
    R[0:2,:]=(F1*F0).T
    R[2:6,:]=(S.eye(4)-F0*F0.T)*F1.T
    R[6:14,:]=S.eye(8)-F1*F1.T
    T[:,-8:]+=R*S.kronecker_product(G,S.eye(4))
    T=mat(T)
    equal(T.T*T,S.eye(Dsmall),'complete direct clock unitarity m='+str(m))
    seeds=[]
    z=S.zeros(Dsmall,2);z[:2,:]=S.eye(2);seeds.append((z,N,G))
    z=S.zeros(Dsmall,2);z[2:6,:]=S.kronecker_product(S.eye(2),w);seeds.append((z,N-1,G))
    z=S.zeros(Dsmall,4);z[6:14,:]=S.kronecker_product(S.eye(4),w)
    seeds.append((z,N-2,S.kronecker_product(G,S.eye(2))))
    basis=[]
    for k,(seed,age,old_g) in enumerate(seeds):
        now=seed
        for j in range(age):basis.append(now);now=mat(T*now)
        equal(now,seed*old_g,'exact birth-age monodromy m='+str(m)+' layer='+str(k))
    Q=S.Matrix.hstack(*basis)
    equal(Q.T*Q,S.eye(Dsmall),'all chronological modes covered, m='+str(m))

# An exact finite gap using rational inequalities only. The entropy bound is
# an EXPLICIT additional binding hypothesis, not supplied by this checker.
m=1024;D=112+128*m;M=425*D
exp_lower=sum((Fraction(18)**k/Fraction(factorial(k)) for k in range(41)),Fraction(0))
require(exp_lower>M,'positive rational exp(18) partial sum certifies log(full dimension) < 18')
require(Fraction(1,1)/(1-Fraction(1,3))==Fraction(3,2),'exp(1/3) < geometric series = 3/2 < phi')
require(2*(1-Fraction(5,8))==Fraction(3,4),'beta > 3/4 from the native Golden interval')
book_upper=Fraction(4,3)*18;info_upper=3*18
gap_lower=2*m-info_upper-book_upper
require(gap_lower==1970,'strict conditional Cost-minus-Info-minus-master gap at unit calibration')

# Full-price diagnostics use the proven birth-age decomposition. Each old G
# phase has multiplicities 8,8,16 on the three genuine birth layers.
av=float(S.sqrt((S.sqrt(5)-1)/2));beta=2*av**4;theta=float(np.arccos(av))
parts=np.array([9.,11.,13.]);co=1/(35-parts)
def scene(x):
    x=np.asarray(x);small=np.zeros((len(x),3,3))
    for i in range(3):
        small[:,i,i]=1-2*x*co[i]
        for j in range(i):small[:,i,j]=small[:,j,i]=-np.sqrt(parts[i]*parts[j]*co[i]*co[j])
    return np.exp(-beta*np.linalg.eigvalsh(small)).sum(axis=1)+np.sum((parts-1)*np.exp(-beta*(1-2*x[:,None]*co)),axis=1)
prices={}
for m in (0,1,2,1024):
    N=2*m+3;D=112+128*m;active=0.
    for age,mult in ((N,8),(N-1,8),(N-2,16)):
        angles=np.concatenate([(theta+2*np.pi*np.arange(age))/age,(-theta+2*np.pi*np.arange(age))/age])
        active+=mult*float(scene(np.cos(angles)).sum())
    Z=359*D+2*active;B=np.log(Z)/beta
    require(np.log(359*D)/beta<=B<=np.log(425*D)/beta,'entire numerical master lies in analytic enclosure m='+str(m))
    prices[str(m)]=format(B,'.15g')

wb=(json.dumps(word_payload,sort_keys=True,indent=2)+'\n').encode()
result={'status':'PASS','checks':len(checks),'native_words_sha256':hashlib.sha256(wb).hexdigest(),
 'actual_readout_gap':str(gap),'histories':inventories,'full_master_diagnostics':prices,
 'finite_conditional_gap':{'pairs':1024,'full_carrier_dimension':M,'log_dimension_strict_upper':18,
    'primitive_Cost_lower':2048,'Info_strict_upper_if_record_entropy_bound':54,
    'master_strict_upper':24,'Cost_minus_Info_minus_master_strict_lower':1970,
    'additional_hypotheses':'unit price calibration; no extra work rebate; Info <= log_phi(full carrier dimension)'},
 'required_general_credit':'Info_m - W_m >= 2m - kappa*B_m - constant - binding_error_m',
 'scope':{'Info_selected':False,'work_rebate_excluded_unconditionally':False,
          'all_durations_same_physical_task_proved':False,'clock_source_binding_proved':False,
          'new_gravity_root':False,'GR_closed':False}}
if args.out:
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'native_padding_words.json').write_bytes(wb)
print(json.dumps(result,sort_keys=True,indent=2))
