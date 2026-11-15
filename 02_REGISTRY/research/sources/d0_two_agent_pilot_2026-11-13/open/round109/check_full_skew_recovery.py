#!/usr/bin/env python3
"""A54/B105 full-CODE-skew analytical feedback recovery in a raw norm.

Consumes fixed-y fibre, source/post/kernel and B65/A47 theorems. No new
finite compiler, physical lift, all-control admission or Cost-Info proof.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
OWNER=D.parents[2]/'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
sys.path.insert(0,str(O/'round105'));import regular_paid_family as b105
sys.path.insert(0,str(D/'round54'));import regular_global_source as a54
sys.path.insert(0,str(D/'round47'));import full_vector_controls as ctl
def read(path):return json.loads(Path(path).read_text())
def digest(path):return sha256(Path(path).read_bytes()).hexdigest()
for file,key in [(O/'round107/B107_REGULAR_SOURCE_RECOVERY_CHECK.json','input_sha256'),
                 (O/'round108/B108_A55_AUDIT_CHECK.json','input_sha256'),
                 (D/'round54/REGULAR_GLOBAL_SOURCE_PLAN.json','source_sha256'),
                 (D/'round54/REGULAR_GLOBAL_SOURCE_CHECK.json','source_sha256'),
                 (O/'round65/SCALAR_HESSIAN_ENVELOPE.json','source_sha256')]:
    for name,h in read(file)[key].items():assert digest(name)==h,name
assert read(O/'round107/B107_REGULAR_SOURCE_RECOVERY_CHECK.json')['status'].startswith('PASS_OFF_SHELL_FOUR_AXIS')
assert read(O/'round108/B108_A55_AUDIT_CHECK.json')['status'].startswith('PASS_A55_BINDING')
assert read(O/'round65/SCALAR_HESSIAN_ENVELOPE.json')['I_tau_Hessian_raw_chart_norm_lt']=='2^25'

# Exact MG2 response and strict norm for the actual 4-state local block.
Q=ctl.e.Q4;p=ctl.e.SIN;zero=Q();one=Q(1)
phi,probs,lambdas=ctl.mg2(); V=[Q(i)-3*p*p for i in range(4)]
X=[[zero for _ in range(4)] for _ in range(4)]
for (i,j),lam in lambdas.items():X[i][j]=-lam;X[j][i]=lam
H=[[(V[i]-V[j])*X[i][j] for j in range(4)] for i in range(4)]
assert all(sum((H[i][j]*phi[j] for j in range(4)),zero)==phi[i] for i in range(4))
assert sum((v*v for v in phi),zero)==one
frob=sum((X[i][j]*X[i][j] for i in range(4) for j in range(4)),zero)
iv=ctl.e.Dyadic(256);lo,hi=iv.evaluate((ctl.e.expr(frob),))[0]
assert 0<lo<=hi<iv.S
assert 2688<52**2 and 4*2688<104**2 and 9*2688<156**2

# Explicit nonzero L-kernel direction on TWO actual four-state coordinate
# blocks. It has zero linear response in every coordinate but a nonzero
# response to the quadratic sampled observable V1*V2. Other coordinates are
# spectators. This is a counterexample to extending B95's axis cancellation.
chi=[phi[i]*phi[j] for i in range(4) for j in range(4)]
v1=[V[i] for i in range(4) for j in range(4)]
v2=[V[j] for i in range(4) for j in range(4)]
K=[[zero for _ in range(16)] for _ in range(16)]
for i,j,sign in ((0,1,1),(0,4,1),(0,5,-1)):
    value=F(sign,1000)*ctl.inverse(chi[i]*chi[j]);K[i][j]=value;K[j][i]=-value
def comm(values):
    return sum((chi[i]*(values[i]-values[j])*K[i][j]*chi[j] for i in range(16) for j in range(16)),zero)
assert comm(v1)==zero and comm(v2)==zero
quadratic=comm([x*y for x,y in zip(v1,v2)])
assert quadratic==Q(F(1,500))
kf=sum((K[i][j]*K[i][j] for i in range(16) for j in range(16)),zero)
klo,khi=iv.evaluate((ctl.e.expr(kf),))[0];assert 0<klo<=khi<iv.S

# Full-skew bound. B97's tighter sigma^2 cubic cancellation applies ONLY to
# its axes, so derive the all-skew sampled-Hessian and weight bounds afresh.
u=a54.upper_inventory_and_error();fam=b105.RegularPaidFamily(a54,a54.t.FieldCentre(),u['W_G_CX_upper'])
assert fam.bounds()['post_corner_lower']>F(2,3)
sigma,gs=F(1,1<<80),F(1,1<<3208)
grad=F(1,1<<3083)+F((1<<25)*52,1<<32);assert grad<F(1,2)
hessian=1<<25;rv=104
eM=u['full_canonical_compressed_error'];eW=u['replacement_error']
eB=u['full_SOURCE_DATA_fibre_prefix_error'];eU=fam.cfg['post_error']
delta=156*1748*sigma+2*eB
tau=2*grad*rv+hessian*sigma*rv**2+eM/gs
assert tau<85 and F(1,1<<62)<delta<F(1,1<<61)
kernel=F(3,4)*(tau*(2*delta**2+2*eW)+eW/gs)
post=eU/gs
assert kernel<F(1,1<<116) and post<F(1,1<<6039)
# ||[R,X]|| <= 2||R||||X||, ||R|| <= .5 H sigma² Rv².
scalar=hessian*sigma*rv**2
# Full-label oscillation of I, not B97's single-axis commutator estimate.
osc=grad*sigma*rv+F(1,2)*hessian*sigma**2*rv**2
gupper=F(1,1<<3061);value_upper=1<<15
weight=F(3,2)*gupper*4*value_upper*osc/sigma
corner=F(3,2)*eM/gs
reduced=scalar+weight+corner
assert scalar<F(1,1<<41) and weight<F(1,1<<3021) and corner<F(1,1<<212)
# Pf reduced error r; Qf/Qb each r/2+kernel+post; Pb post;
# actual Pf itself adds post. max ||X_a|| <=52*||X||raw.
dual=52*(2*reduced+2*kernel+4*post)
assert dual<F(1,1<<34)
assert fam.cfg['Nbase']!=b105.paid.production_configuration()['Nbase']
assert fam.cfg['Nbase'].bit_length()==30833 and fam.cfg['K']==175604

paths=[Path(__file__),OWNER,O/'round107/B107_OFF_SHELL_FOUR_AXIS_SOURCE_RECOVERY_RU.md',
       O/'round107/B107_REGULAR_SOURCE_RECOVERY_CHECK.json',O/'round108/B108_A55_AUDIT_CHECK.json',
       O/'round65/SCALAR_HESSIAN_ENVELOPE.json',O/'round95/QUADRATIC_LIFT_CHECK.json',
       D/'round44/JOINT_SOURCE_REDUCTION_RU.md',D/'round47/full_vector_controls.py',
       D/'round47/FULL_VECTOR_REPAIR_RU.md',D/'round50/FOUR_INDEPENDENT_PRICE_ROWS_RU.md',
       D/'round54/REGULAR_GLOBAL_SOURCE_PLAN.json',O/'round105/regular_paid_family.py']
out={'status':'PASS_ANALYTIC_FULL_CODE_SKEW_RAW_NONQUOTIENT_RECOVERY_CONDITIONAL',
     'fixed_y_selected_A23_B25_canonical_fibre':True,'field_coordinates':2688,
     'decoder':'ell_j(X)=<chi,[V_j,X]chi>; L=ell(Pf)-ell(Qf)/2+ell(Qb)/2',
     'raw_norm':'max(||L(X)||_2,max_a||X_a||op/52)',
     'right_lift':'R(v)=(sum_j v_j X_j,0,0,0); ||R(v)||raw=||v||_2',
     'nonzero_kernel_direction_with_quadratic_response_verified':True,
     'scalar_all_skew_remainder_lt':'2^-41','Q_kernel_lt':'2^-116',
     'full_four_slot_analytic_feedback_dual_error_lt':'2^-34',
     'analytic_feedback_norm_and_DI_coordinate_norm_differ_lt':'2^-34',
     'kinematic_scale':'sigma L; unscaled right lift R/sigma',
     'finite_native_full_skew_comparisons_provided':False,
     'physical_iota_Vh_or_all_control_admission_proved':False,
     'heat_or_full_Cost_Info_dual_transferred':False,
     'production_word_executed':False,'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(f):digest(f) for f in paths}}
(P/'B109_FULL_SKEW_RECOVERY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))
