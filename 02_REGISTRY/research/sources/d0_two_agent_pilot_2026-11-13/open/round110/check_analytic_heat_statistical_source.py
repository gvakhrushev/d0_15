#!/usr/bin/env python3
"""Full-skew analytic heat on B105 clock and conditional Book source law.

The path varies an existing padded stage by a generally NON-native
exp(tX), with identical births and length. It is not a paid full-skew
compiler or a physical Cost-Info source identification.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sys,os,math
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
np.seterr(all='ignore')
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
OWNER=D.parents[2]/'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
CLOCK=D.parents[2]/'sources/d0_retained_response_concentration_2026-10-28/GROWING_CLOCK_RU.md'
sys.path.insert(0,str(O/'round105'));import regular_paid_family as b105
sys.path.insert(0,str(D/'round54'));import regular_global_source as a54
def read(path):return json.loads(Path(path).read_text())
def digest(path):return sha256(Path(path).read_bytes()).hexdigest()
b109=read(O/'round109/B109_FULL_SKEW_RECOVERY_CHECK.json')
assert b109['status']=='PASS_ANALYTIC_FULL_CODE_SKEW_RAW_NONQUOTIENT_RECOVERY_CONDITIONAL'
for path,h in b109['input_sha256'].items():assert digest(path)==h,path
assert b109['heat_or_full_Cost_Info_dual_transferred'] is False
for name in ('REGULAR_GLOBAL_SOURCE_PLAN.json','REGULAR_GLOBAL_SOURCE_CHECK.json'):
    for path,h in read(D/'round54'/name)['source_sha256'].items():assert digest(path)==h,path

# Exact new padded clock and paid identity reserve in each of four slots.
u=a54.upper_inventory_and_error();fam=b105.RegularPaidFamily(a54,a54.t.FieldCentre(),u['W_G_CX_upper']);c=fam.cfg
assert c['n']==11893774624 and c['Nbase']==c['n']+c['Lbase']
assert c['Lbase']==c['coreL']+c['postL']+c['probeL']+4*c['controlL']
assert c['Nbase'].bit_length()==30833 and c['K']==175604 and c['K']%4==0
assert c['Nbase']!=b105.paid.production_configuration()['Nbase']
assert c['controlL']>=4 and c['Lbase']>=4
assert fam.bounds()['post_corner_lower']>F(2,3)
assert b105.paid.slot_signs('matched',1)==dict(Pf=1,Qf=-1,Qb=1,Pb=-1)
for arm,sgn in [('Pf',1),('Qf',-1),('Qb',1),('Pb',-1)]:
    assert b105.paid.slot_signs(arm,1)[arm]==sgn
assert F(5,6)**4<F(1,2)  # p>3/5 -> (2p)^-1<5/6

# New full-skew analytic heat: G16 derivative plus ONE modified edge in
# each paid slot, not the finite-catalogue heat dual of B105.
z=F(1,1<<20);gs=F(1,1<<3208);gamma=F(8,3)*z*gs
heat=F(6*4*52,359)/gamma*F(1,1<<(c['K']//4))
assert heat<F(1,1<<40672)

# Recompute the explicit B109 upper, then add H and original statistical
# source. beta=2p²<1 for p²+p=1, p>1/2, so beta*heat <=heat.
sigma=F(1,1<<80);rv=104;H2=1<<25
grad=F(1,1<<3083)+F(H2*52,1<<32)
eM=u['full_canonical_compressed_error'];eW=u['replacement_error']
eB=u['full_SOURCE_DATA_fibre_prefix_error'];eU=c['post_error']
delta=156*1748*sigma+2*eB
tau=2*grad*rv+H2*sigma*rv**2+eM/gs
assert grad<F(1,2) and tau<85 and delta<F(1,1<<61)
kernel=F(3,4)*(tau*(2*delta**2+2*eW)+eW/gs);post=eU/gs
osc=grad*sigma*rv+F(1,2)*H2*sigma**2*rv**2
weight=F(3,2)*F(1,1<<3061)*4*(1<<15)*osc/sigma
corner=F(3,2)*eM/gs
feedback=52*(2*(H2*sigma*rv**2+weight+corner)+2*kernel+4*post)
full=feedback+heat
assert feedback<F(1,1<<34) and full<F(1,1<<34)
assert F(1,2)<F(3,5) and F(3,5)**2+F(3,5)<1 # p>3/5; hence 0<2p²<1

# Independent small growing clock. Four changed source stages act on the
# same qubit; one later birth introduces an actual retained complement.
# Build the canonical closure and the REAL 33-vertex K(9,11,13) scene.
n0=2;dims=[2,2,2,2,2,4];offs=np.cumsum([0]+dims);dim=int(offs[-1])
birth=np.vstack((np.eye(2),np.zeros((2,2))))
rotation=lambda t:np.array([[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]])
g=np.zeros((4,4));g[:2,:2]=rotation(.37);g[2:,2:]=rotation(-.23)
R=np.zeros((dim,4));R[:2,:]=birth.T;R[offs[5]:offs[6],:]=np.eye(4)-birth@birth.T
assert np.allclose(R.T@R,np.eye(4),atol=1e-14)
X=np.array([[0.,-1.],[1.,0.]]); magnitudes=[1.,-.7,.3,-.2]
signs=[1,-1,1,-1]
def clock(t):
    T=np.zeros((dim,dim))
    for j in range(4):T[offs[j+1]:offs[j+2],offs[j]:offs[j+1]]=rotation(signs[j]*magnitudes[j]*t)
    T[offs[5]:offs[6],offs[4]:offs[5]]=birth
    T[:,offs[5]:offs[6]]+=R@g
    return T
T=clock(0);Tdot=np.zeros_like(T)
for j in range(4):Tdot[offs[j+1]:offs[j+2],offs[j]:offs[j+1]]=signs[j]*magnitudes[j]*X
assert np.allclose(T.T@T,np.eye(dim),atol=1e-14) and np.allclose(T@T.T,np.eye(dim),atol=1e-14)
trace_norm=np.linalg.svd(Tdot,compute_uv=False).sum()
assert abs(trace_norm-2*sum(abs(x) for x in magnitudes))<1e-12
walk_derivative=6*np.trace(np.linalg.matrix_power(T,5)@Tdot)
assert np.isfinite(walk_derivative) and abs(walk_derivative)>1
groups=[0]*9+[1]*11+[2]*13
adj=np.array([[int(groups[i]!=groups[j]) for j in range(33)] for i in range(33)],dtype=float)
assert int(adj.sum()/2)==359
degree=adj.sum(axis=1);r=1/np.sqrt(degree+2);B=r[:,None]*adj*r[None,:];C=np.diag(r*r)
assert np.trace(C)<=33/22+1e-14
Delta=np.eye(33*dim)-np.kron(B,np.eye(dim))-np.kron(C,T+T.T)
Delta_dot=-np.kron(C,Tdot+Tdot.T)
beta=2*((math.sqrt(5)-1)/2)**2
vals,vec=np.linalg.eigh(Delta);weights=np.exp(-beta*vals)
Z=359*dim+2*weights.sum()
derivative=-2*np.dot(weights,np.sum(vec*(Delta_dot@vec),axis=0))/Z
assert np.isfinite(derivative) and np.isfinite(Z) and np.all(np.isfinite(vals))
assert abs(derivative)<=6*trace_norm/(359*dim)+1e-12
def h(t):
    A=clock(t);d=np.eye(33*dim)-np.kron(B,np.eye(dim))-np.kron(C,A+A.T)
    return math.log(359*dim+2*np.exp(-beta*np.linalg.eigvalsh(d)).sum())/beta
step=1e-4;numeric=(h(step)-h(-step))/(2*step)
assert np.isfinite(numeric) and abs(numeric-derivative)<2e-8

# Independent Golden identities and full source orientation on the same
# hypothetical path; no replacement of beta or of determinant exponent.
import sympy as sp
p=sp.Symbol('p');relation=p*p+p-1
assert sp.rem(2*p*p-1+p**3,relation,p)==0
assert sp.rem(p**3-(2*p-1),relation,p)==0

paths=[Path(__file__),OWNER,CLOCK,O/'round109/B109_FULL_CODE_SKEW_RECOVERY_RU.md',
       O/'round109/B109_FULL_SKEW_RECOVERY_CHECK.json',O/'round105/regular_paid_family.py',
       O/'round105/B105_REGULAR_PAID_CHECK.json',D/'round54/regular_global_source.py',
       D/'round55/regular_comparison_task.py',D/'round55/REGULAR_COMPARISON_TASK.json']
out={'status':'PASS_CONDITIONAL_ANALYTIC_HEAT_AND_ORIENTED_STATISTICAL_SOURCE',
     'clock_n':c['n'],'new_Nbase_bits':c['Nbase'].bit_length(),'K':c['K'],
     'clock_dimension':'2^n*(Lbase-2+3*2^K)-1','clock_stages':'N=Nbase+2K',
     'path':'replace last padded primitive in each slot by exp(s_a*t*X_a)*U_last; no extra stage',
     'path_is_native_paid_arbitrary_skew_family':False,'proper_cut':'full propagated input cut, rank-one scene cut',
     'heat_modes':'all 425D; Z_H=359D+2 Tr_(33D) exp(-beta Delta0)',
     'beta':'2p^2','beta_minus_one':'-p^3','z':'2^-20','gain':'actual Gamma(Y) fixed per field',
     'analytic_heat_raw_dual_lt':'2^-40672','feedback_raw_dual_error_lt':'2^-34',
     'H_plus_J_raw_dual_error_lt':'2^-34','oriented_original_statistical_raw_dual_error_lt':'2^-34',
     'orientation':'Gamma_A=Gamma/ln(phi); -DA/Gamma_A=(DJ+beta DH)/Gamma',
     'same_graph_fixture_dimension':dim,'same_graph_fixture_33_scene_vertices_and_359_edges':True,
     'same_graph_fixture_nonzero_temporal_six_walk_derivative':True,
     'source_law_is_explicit_premise':True,'later_7fu_physical_C_withdrawal_preserved':True,
     'physical_iota_Vh_or_full_finite_skew_dual_proved':False,'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(f):digest(f) for f in paths}}
(P/'B110_ANALYTIC_HEAT_STATISTICAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))
