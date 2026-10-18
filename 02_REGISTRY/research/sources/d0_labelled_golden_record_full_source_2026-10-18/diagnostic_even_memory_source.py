"""Single-cross-mode PURE REAL cat H+J+R Hessian at the owned root CENTER.

Portable numeric diagnostic only; default read-only, --output explicitly saves JSON. All4096 momenta/full16 CAR, full-Z dd,
rho_cat rank8 in reference128, signed off-shell inverse, actual second
Dirac jet for u linear and Lorentz links exp(Omega). No old run() is called.
--timeflip uses chi- on the two temporal shell momenta and chi+ on the six
spatial shell momenta; the default remains the original constant chi+.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
import argparse
import ast
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import time
import mpmath as mp
import numpy as np
import sympy as s
np.seterr(all='ignore')  # Every operator/result array is checked finite below.

START=time.perf_counter()
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--timeflip',action='store_true',help='reverse the top-state sign on the temporal shell axis')
parser.add_argument('--output',type=Path)
args=parser.parse_args()
BASE='02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/'
SPECTRAL=BASE+'full_symbol_diagnostic.py'
HELPER='02_REGISTRY/research/sources/d0_complete_record_channel_2026-10-17/check_flat_relaxation.py'
CURVED='02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
RECEIPT='02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/receipt.json'
WAVE='02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py'
CROSS_DATA='02_REGISTRY/research/sources/d0_labelled_golden_record_full_source_2026-10-18/EVEN_MEMORY_CROSS_LIFT_DATA.json'
cross_digest='d5f0dbeec44af8f375039a8a7bb392541bb8f8bb7a6cd0deb69d3a62c5be7e2e'
if args.timeflip:
    CROSS_DATA='02_REGISTRY/research/sources/d0_labelled_golden_record_full_source_2026-10-18/EVEN_MEMORY_TIMEFLIP_LIFT_DATA.json'
    cross_digest='64a6d796ecabe3e8a807927efcb65c23096a11460495182cd507c0ab30aba983'
PINS={CROSS_DATA:cross_digest,SPECTRAL:'6084660c02a1012a4beb619e71e61015dda0d7ebb44207bf6faa7d5281404b25',
      HELPER:'0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9',
      CURVED:'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
      RECEIPT:'da44c7393b1164ce4babcab2ea13707958364d273d2c3fa1d86d514a9ac83ae9',
      WAVE:'2b12f26d814a57cc99084e904deeac69a8f64a8d9a0eb9ee765e8104ef50bc37'}
for path,digest in PINS.items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
cross_data=json.loads((ROOT/CROSS_DATA).read_text())

# Definitions only: never import or execute the old diagnostic run().
names={'require','exact_features','_spectral_data'}
nodes=[n for n in ast.parse((ROOT/SPECTRAL).read_text()).body
       if isinstance(n,ast.FunctionDef)and n.name in names]
assert len(nodes)==3
sc={'mp':mp,'np':np,'ast':ast,'hashlib':hashlib,'ROUNDS':8192,'FOCK':16,
    'REFERENCE':128,'WAVE':WAVE,'PINS':{WAVE:PINS[WAVE]}}
exec(compile(ast.Module(body=nodes,type_ignores=[]),SPECTRAL,'exec'),sc)
root=json.loads((ROOT/RECEIPT).read_text())['interval']['root_center']
q=np.array([1,1,0,0]);L=8;ell=1/8
modes=np.array(list(itertools.product(range(8),repeat=4)),int)
lookup={tuple(k):i for i,k in enumerate(modes)}
outgoing=np.array([lookup[tuple((k+q)%8)]for k in modes])
features_of=sc['exact_features'](ROOT)
features=tuple(features_of(tuple(k))for k in modes)
sp=sc['_spectral_data'](features,outgoing,root)
a,b=float(sp['a']),float(sp['b'])

# Literal actual ACDB CAR, with an explicit signed-permutation intertwiner
# to the physical-coordinate bit basis used by the canonical cross pivots.
nd=[n for n in ast.parse((ROOT/HELPER).read_text()).body
    if isinstance(n,ast.FunctionDef)and n.name=='_creators']
cscope={'s':s,'ast':ast,'lru_cache':lru_cache,'CURVED':CURVED}
exec(compile(ast.Module(body=nd,type_ignores=[]),HELPER,'exec'),cscope)
actual,order=cscope['_creators'](ROOT);assert order==(0,2,3,1)
v=s.eye(16)[:,0];cols=[]
for mask in range(16):
    state=v
    for j in reversed(range(4)):
        if mask>>j&1:state=actual[j]*state
    cols.append(state)
intertwiner=s.Matrix.hstack(*cols)
assert intertwiner.T*intertwiner==s.eye(16)
assert intertwiner[:,0]==v and intertwiner[:,15]==s.eye(16)[:,15]
C=np.array([np.array(intertwiner.T*c*intertwiner,dtype=float)for c in actual])
for j in range(4):
    expected=np.zeros((16,16))
    for mask in range(16):
        if not(mask>>j&1):expected[mask|1<<j,mask]=(-1)**bin(mask&((1<<j)-1)).count('1')
    assert np.array_equal(C[j],expected)
eta=np.diag([1.,-1.,-1.,-1.]);F=(a-b)*np.eye(4)+b*np.ones((4,4))
U=eta@F.T;u=U.T;cu=np.einsum('ra,aij->rij',u,C)
generators=[];pairs4=[]
for i in range(4):
    for j in range(i+1,4):
        M=np.zeros((4,4));M[i,j]=1;M[j,i]=-eta[i,i]*eta[j,j]
        generators.append(M);pairs4.append((i,j))
generators=np.array(generators)
exterior=np.einsum('aij,ikm,jmn->akn',generators,C,C.transpose(0,2,1))
cat=np.zeros(16);cat[[0,15]]=1/np.sqrt(2)
roots=np.array([complex(s.N(s.exp(s.I*s.pi*j/4),18))for j in range(8)])
tk=roots[modes];tq=roots[q];D=L*(np.einsum('kr,rij->kij',tk-1,cu)
                           +np.einsum('kr,rji->kij',tk.conj()-1,cu))
lambda_error=np.max(np.abs(D@D-sp['lambda'][:,None,None]*np.eye(16)))
assert lambda_error<2e-11
shell=sp['rho']>0;assert shell.sum()==8
if args.timeflip:
    cat_by_mode=np.tile(cat,(len(modes),1))
    assert cross_data['memory_sign_by_axis']==[-1,1,1,1]
    for k in modes[shell]:
        active=np.flatnonzero(k)
        assert len(active)==1 and k[active[0]]in(1,7)
        cat_by_mode[lookup[tuple(k)],15]*=cross_data['memory_sign_by_axis'][active[0]]
    assert np.max(abs(np.sum(abs(cat_by_mode[shell])**2,axis=1)-1))<1e-15
shell_modes=[k for k in modes if shell[lookup[tuple(k)]]]
ordered=[(k,l)for k in shell_modes for l in shell_modes if np.all((l-k-q)%8==0)]
assert len(ordered)==2

def jets(field,indices):
    """field40 x nb -> all full16 J(k+q,k), X; complex-linear amplitudes."""
    nb=field.shape[1]
    du=field[:16].T.reshape(nb,4,4)
    og=np.einsum('arj,jkl->arkl',field[16:].T.reshape(nb,4,6),exterior)
    ca=np.einsum('arc,cij->arij',du,C)
    ia=ca.transpose(0,1,3,2)
    plus=ca+np.einsum('rij,arjk->arik',cu,og)
    minus=tq.conj()[None,:,None,None]*(ia+np.einsum('arji,rjk->arik',og,cu.transpose(0,2,1)))
    constant=-(ca+ia).sum(axis=1)
    phases=tk[indices]
    J=L*(np.einsum('kr,arij->akij',phases,plus)
         +np.einsum('kr,arij->akij',phases.conj(),minus)+constant[:,None])
    X=D[outgoing[indices]][None]@J+J@D[indices][None]
    return J,X

shell_in=np.array([lookup[tuple(k)]for k,l in ordered])
_,Xraw=jets(np.eye(40),shell_in)
if args.timeflip:
    Traw=np.einsum('akij,kj->kia',Xraw,cat_by_mode[shell_in]).reshape(32,40)
else:
    Traw=np.einsum('akij,j->kia',Xraw,cat).reshape(32,40)
Y=np.zeros((40,27),complex);Y[16:,:24]=np.eye(24)
for j in range(3):
    B=np.zeros((4,4));B[0,j+1]=B[j+1,0]=1
    Y[:16,24+j]=(-u@B.T).ravel()
Ty=Traw@Y
minor_source=ROOT/CROSS_DATA
minor_record=next(x for x in cross_data['cases']if x['q']==q.tolist())
rs,cs=minor_record['rows'],minor_record['columns'];free=[j for j in range(27)if j not in cs]
minor=Ty[np.ix_(rs,cs)]
N=np.zeros((27,13),complex);N[free,:]=np.eye(13)
N[cs,:]=-np.linalg.solve(minor,Ty[np.ix_(rs,free)])
N=np.linalg.qr(N,mode='reduced')[0]
I=Y@N
metric_slots=[(i,j)for i in range(4)for j in range(i,4)]
Mmetric=np.zeros((40,10),complex)
for j,(r,t)in enumerate(metric_slots):
    V=np.zeros((4,4));V[r,t]=V[t,r]=1
    Mmetric[:16,j]=(.5*eta@np.linalg.inv(U).T@V).T.ravel()
correction=np.zeros((27,10),complex)
correction[cs,:]=-np.linalg.solve(minor,(Traw@Mmetric)[rs])
Lift=Mmetric+Y@correction
G=[]
for i,j in ((1,2),(1,3),(2,3)):
    R=np.zeros((4,4));R[i,j]=1;R[j,i]=-1
    g=np.zeros(40,complex);g[:16]=(u@R.T).ravel()
    for rr in range(4):
        for z,(ii,jj)in enumerate(pairs4):g[16+6*rr+z]=(1-tq[rr])*R[ii,jj]
    G.append(g)
G=np.array(G).T
field=np.column_stack([I,Lift,G,Y[:,cs]]);nb=field.shape[1]
constraint_error=float(np.linalg.norm(Traw@field[:,:26]))
assert constraint_error<2e-9

# W_k is MATRIX-valued on shell. Precompute actual source moments for seagull.
kappa=sp['kappa'];occ=shell.astype(float)/8
if args.timeflip:
    Dcat=np.einsum('kij,kj->ki',D,cat_by_mode)
    ED=2*kappa[:,None,None]*D+occ[:,None,None]*(Dcat[:,:,None]*cat_by_mode[:,None,:]
                          +cat_by_mode[:,:,None]*Dcat[:,None,:].conj())
else:
    Dcat=np.einsum('kij,j->ki',D,cat)
    ED=2*kappa[:,None,None]*D+occ[:,None,None]*(Dcat[:,:,None]*cat[None,None,:]
                          +cat[None,:,None]*Dcat[:,None,:].conj())
assert np.isfinite(ED).all()
Kmom=np.einsum('kr,kij->rij',tk,ED);K0=ED.sum(axis=0)
Kscalar=np.einsum('kr,kij->rij',tk,2*(kappa+sp['rho'])[:,None,None]*D)
gradient=[]
for rr in range(4):
    gradient.extend(2*L*np.trace((Kmom[rr]-K0)@c).real for c in C)
for rr in range(4):
    gradient.extend(2*L*np.trace(Kmom[rr]@cu[rr]@g).real for g in exterior)

HJheat=np.zeros((nb,nb),complex);HJmatter=HJheat.copy();HXheat=HJheat.copy();HXmatter=HJheat.copy()
def gram(A,weight):
    return (A.conj()*weight[None,:,None]).reshape(nb,-1)@A.reshape(nb,-1).T
for start in range(0,len(modes),128):
    ix=np.arange(start,min(start+128,len(modes)));out=outgoing[ix]
    J,X=jets(field,ix);assert np.isfinite(J).all()and np.isfinite(X).all()
    jf,xf=J.reshape(nb,len(ix),256),X.reshape(nb,len(ix),256)
    HJheat+=gram(jf,kappa[ix]+kappa[out]);HXheat+=gram(xf,sp['dd'][ix])
    if args.timeflip:
        # Column grams use input chi_k; row grams use output chi_(k+Q).
        jc=np.einsum('akij,kj->aki',J,cat_by_mode[ix]);jr=np.einsum('ki,akij->akj',cat_by_mode[out],J)
        xc=np.einsum('akij,kj->aki',X,cat_by_mode[ix]);xr=np.einsum('ki,akij->akj',cat_by_mode[out],X)
    else:
        jc=np.einsum('akij,j->aki',J,cat);jr=np.einsum('i,akij->akj',cat,J)
        xc=np.einsum('akij,j->aki',X,cat);xr=np.einsum('i,akij->akj',cat,X)
    HJmatter+=gram(jc,occ[ix])+gram(jr,occ[out])
    HXm=gram(xc,-occ[ix]*sp['resolvent'][out])+gram(xr,-occ[out]*sp['resolvent'][ix])
    HXmatter+=HXm

du=field[:16].T.reshape(nb,4,4);ca=np.einsum('arc,cij->arij',du,C)
og=np.einsum('arj,jkl->arkl',field[16:].T.reshape(nb,4,6),exterior)
Z=np.zeros((nb,nb),complex);Zscalar=Z.copy()
for alpha in range(nb):
    for beta in range(nb):
        for rr in range(4):
            A,B=og[alpha,rr].conj(),og[beta,rr]
            mixed=ca[alpha,rr].conj()@B+ca[beta,rr]@A+.5*cu[rr]@(A@B+B@A)
            Z[alpha,beta]+=L*np.trace(Kmom[rr]@mixed)
            Zscalar[alpha,beta]+=L*np.trace(Kscalar[rr]@mixed)
Hseagull=Z+Z.conj().T
Hseagull_scalar=Zscalar+Zscalar.conj().T
Hwithout=HJheat+HJmatter+HXheat+HXmatter
H=Hwithout+Hseagull
assert np.isfinite(H).all()
hermitian_error=np.linalg.norm(H-H.conj().T)/max(1,np.linalg.norm(H))
assert hermitian_error<3e-11
H=(H+H.conj().T)/2
ward=float(np.linalg.norm(H[:,23:26])/max(1,np.linalg.norm(H)))
ward_without=float(np.linalg.norm(Hwithout[:,23:26])/max(1,np.linalg.norm(H)))
A=H[:13,:13];B=H[:13,13:23];Cmetric=H[13:23,13:23]
eig=np.linalg.eigvalsh(A);tol=1e-9*max(1,np.linalg.norm(A,2))
null=np.abs(eig)<=tol
if not np.any(null):
    solve=np.linalg.solve(A,B);reduced=Cmetric-B.conj().T@solve
    stationary_lift=Lift-I@solve
    metric_eigen=np.linalg.eigvalsh((reduced+reduced.conj().T)/2).tolist()
    compatibility=None;solve_error=float(np.linalg.norm(A@solve-B)/max(1,np.linalg.norm(B)))
else:
    val,vec=np.linalg.eigh(A);compatibility=float(np.linalg.norm(vec[:,abs(val)<=tol].conj().T@B))
    metric_eigen=None;solve_error=None
    stationary_lift=None
def inertia(e):return [int(sum(np.array(e)>tol)),int(sum(np.array(e)<-tol)),int(sum(abs(np.array(e))<=tol))]
result={'status':'NUMERIC_DIAGNOSTIC','q':q.tolist(),'root_center':root,'a':sp['a'],'b':sp['b'],
    'all4096_full16':True,'rho':'P_Omega tensor |realcat><realcat| /8',
    'spectral_shell_dimension':128,'preparation_rank':8,'reference_space':128,
    'constraint_rank':14,'internal_dimension':13,'metric_dimension':10,
    'basis_constraint_error':constraint_error,'canonical_minor_condition':float(np.linalg.cond(minor)),
    'all_mode_D_square_error':float(lambda_error),'homogeneous_source_max':float(np.max(np.abs(gradient))),
    'hermitian_error':float(hermitian_error),'normalized_Ward_error':ward,
    'Ward_max_abs':float(np.max(abs(H[:,23:26]))),
    'Ward_error_without_second_Dirac_jet':ward_without,
    'Hnorm':float(np.linalg.norm(H)),'internal_eigenvalues':eig.tolist(),'internal_inertia':inertia(eig),
    'internal_min_abs_eigenvalue':float(np.min(abs(eig))),'internal_condition':float(np.linalg.cond(A)),
    'threshold':float(tol),'metric_Schur_eigenvalues':metric_eigen,'solve_backward_error':solve_error,
    'nullspace_metric_compatibility_norm':compatibility,
    'components_norm':{k:float(np.linalg.norm(v))for k,v in dict(HJheat=HJheat,HJmatter=HJmatter,
                    HXheat=HXheat,HXmatter=HXmatter,Hseagull=Hseagull).items()},
    'quadratic_convention':'c*Hc for one complex Q; real +/-Q field has second derivative2*c*Hc',
    'all_internal_Euler_equations_solved':False,'nonlinear_metric_section_proved':False,'physical_GR_proved':False,
    'source_sha256':PINS,'canonical_pivots_sha256':hashlib.sha256(minor_source.read_bytes()).hexdigest(),
    'diagnostic_scope':'one fixed-Q source-compatible tangent; other Fourier zero modes not classified'}

# The full field basis is internal13+metric10+Ward3+transverse14, dimension40.
# Ward rows are kept, not inverted. Transverse rows pair with actual shell
# amplitude duals; neither these nor the remaining neutral amplitudes are frozen.
assert field.shape==(40,40) and np.linalg.matrix_rank(field)==40
assert np.isfinite(H).all() and ward<1e-10
assert ward_without>(1e-6 if args.timeflip else 1e-4)
assert max(abs(x)for x in gradient)<1e-9
assert np.linalg.norm(Hseagull_scalar)<1e-7
assert np.min(abs(eig))>1e-3  # Diagnostic at this CENTER, not an interval claim.
result['all40_coupled_field_source']=True
result['scalar_W_seagull_control_norm']=float(np.linalg.norm(Hseagull_scalar))
result['scalar_W_substitution_error']=float(np.linalg.norm(Hseagull-Hseagull_scalar))
result['internal_H_real']=A.real.tolist()
result['internal_H_imag']=A.imag.tolist()
result['normal14_source_coupling_norm']=float(np.linalg.norm(H[26:40,13:23]-H[26:40,:13]@solve))
result['metric_basis']=[['deltaq%d%d'%(i,j),i,j]for i,j in metric_slots]
result['field_coefficient_labels']=['u%d%d'%(r,j)for r in range(4)for j in range(4)]+['Omega%d_%d%d'%(r,i,j)for r in range(4)for i,j in pairs4]
result['stationary_field_lift_real']=stationary_lift.real.tolist()
result['stationary_field_lift_imag']=stationary_lift.imag.tolist()
observed=[]
for j in range(10):
    dU=stationary_lift[:16,j].reshape(4,4).T
    dq=dU.T@eta@U+U.T@eta@dU
    observed.append([dq[r,t]for r,t in metric_slots])
result['stationary_lift_metric_error']=float(np.linalg.norm(np.array(observed).T-np.eye(10)))
result['stationary_lift_preparation_error']=float(np.linalg.norm(Traw@stationary_lift))
result['stationary_lift_internal_source_error']=float(np.linalg.norm(-A@solve+B))
assert max(result[k]for k in ('stationary_lift_metric_error','stationary_lift_preparation_error','stationary_lift_internal_source_error'))<2e-10

# Actual real +/-Q curve: u(t)=u+t(du e^iQx+conj(du)e^-iQx),
# M_r(t)=exp(t[Omega_r e^iQx+conj(Omega_r)e^-iQx]), n=e0.
# At inactive occupied k, k+/-Q lies OFF the ENTIRE epsilon shell.
# K_k={D,D''_0}+2 sum_+/- (J*J-X*X/(lambda_(k+/-Q)-epsilon)).
# Project its action on chi to grade2, then Pi_- r=(r-star conj(r))/2.
# This fixed-tangent second residual is NOT a classification of all branches.
star=np.zeros((16,16))
for sequence in itertools.permutations(range(4)):
    i,j,k,l=sequence
    if i<j and k<l:
        parity=(-1)**sum(sequence[a]>sequence[b]for a in range(4)for b in range(a+1,4))
        star[(1<<k)+(1<<l),(1<<i)+(1<<j)]=parity
middle=[3,5,6,9,10,12]
projector=np.diag([int(j in middle)for j in range(16)])
assert np.array_equal(star@star,projector)
inactive=[np.array(k)for k in ((0,0,1,0),(0,0,-1,0),(0,0,0,1),(0,0,0,-1))]

def local_D(momentum):
    phase=roots[np.asarray(momentum)%8]
    return L*sum((phase[r]-1)*cu[r]+(phase[r].conjugate()-1)*cu[r].T for r in range(4))

def second_test(vector):
    w=vector[:16].reshape(4,4)
    omega=vector[16:].reshape(4,6)
    c=np.einsum('ra,aij->rij',w,C)
    g=np.einsum('ra,aij->rij',omega,exterior)
    def J(momentum,target,sign):
        cc,gg=(c,g)if sign==1 else(c.conj(),g.conj())
        t=roots[np.asarray(momentum)%8];tb=roots[(-np.asarray(target))%8]
        return L*sum((t[r]-1)*cc[r]+(tb[r]-1)*cc[r].T+t[r]*cu[r]@gg[r]+tb[r]*gg[r].T@cu[r].T for r in range(4))
    values=[]
    for k in inactive:
        t=roots[k%8]
        raising=L*sum(t[r]*(2*(c[r]@g[r].conj()+c[r].conj()@g[r])+cu[r]@(g[r]@g[r].conj()+g[r].conj()@g[r]))for r in range(4))
        Dsecond=raising+raising.conj().T
        d=local_D(k);K=d@Dsecond+Dsecond@d;gaps=[];adjoint_error=0.
        for sign in (-1,1):
            target=k+sign*q;dl=local_D(target);j=J(k,target,sign)
            x=dl@j+j@d;gap=np.trace(dl@dl).real/16-sp['epsilon']
            assert abs(gap)>1e-3
            gaps.append(float(gap))
            adjoint_error=max(adjoint_error,float(np.linalg.norm(J(target,k,-sign)-j.conj().T)))
            K+=2*(j.conj().T@j-x.conj().T@x/gap)
        input_cat=cat_by_mode[lookup[tuple(k%8)]]if args.timeflip else cat
        r=projector@K@input_cat
        obstruction=(r-star@r.conj())/2
        assert np.isfinite(obstruction).all()and adjoint_error<2e-10
        values.append({'k':k.tolist(),'gaps_minus_plus':gaps,'adjoint_error':adjoint_error,
                       'grade2_source_norm':float(np.linalg.norm(r)),
                       'Pi_minus_norm':float(np.linalg.norm(obstruction)),
                       'Pi_minus_components_real':obstruction[middle].real.tolist(),
                       'Pi_minus_components_imag':obstruction[middle].imag.tolist()})
    return values

metric00=second_test(stationary_lift[:,0])
control=np.zeros(40,complex);control[8]=1  # inactive role2, coframe component0.
assert np.linalg.norm(Traw@control)<1e-12
zero_control=second_test(control)
assert min(x['Pi_minus_norm']for x in metric00)>1
assert max(x['Pi_minus_norm']for x in zero_control)<1e-8
result['second_preparation_test']={'physical_metric':'deltaq00=1, all other slots0',
    'ell':ell,'D_and_first_second_Dirac_prefactor':L,'Delta_scale':L*L,
    'real_plus_minus_Q':True,'metric00_fixed_source_lift':metric00,
    'inactive_coframe_zero_control':zero_control,
    'scope':'nonzero residual of THIS source-compatible fixed-Q tangent; not all nonlinear branches',
    'other_Fourier_internal_zero_modes_excluded':False,
    'transverse14_dual_amplitudes_explicitly_recovered':False,
    'neutral_shell_and_reference_amplitudes_retained':True}
result['source_formulas']={'W':'kappa(lambda_k) I16 + 1_Omega(k)|chi><chi|/8',
    'Hred':'Tr[W({Dv,Dw}+{D,Dvw})]+Tr[Dkappa[Xv]Xw]-2ReTr[rho_cat Xw R_Q Xv]',
    'R_Q':'Q(Delta-epsilon)^-1 Q, Q excludes entire128 spectral shell, signed inverse',
    'seagull':'K_r=sum_allk t_r(k){D_k,W_k}; Z_ab=ell^-1 sum_r Tr K_r(C(conj(w_a))Gamma(Omega_b)+C(w_b)Gamma(conj(Omega_a))+.5 C(u_r){Gamma(conj(Omega_a)),Gamma(Omega_b)}); Hseagull=Z+Z*'}
if args.timeflip:
    result['rho']='sum_(k in Omega) |k,chi_k><k,chi_k| /8; temporal chi-, spatial chi+'
    result['memory_sign_by_axis']=cross_data['memory_sign_by_axis']
    result['shell_memory']=[{'k':k.tolist(),'chi_real':cat_by_mode[lookup[tuple(k)]].tolist()}
                            for k in modes[shell]]
    result['source_formulas']['W']='kappa(lambda_k) I16 + 1_Omega(k)|chi_k><chi_k|/8'
rendered=json.dumps(result,indent=2)+'\n'
if args.output is not None:
    args.output.write_text(rendered)
print(rendered,end='')
