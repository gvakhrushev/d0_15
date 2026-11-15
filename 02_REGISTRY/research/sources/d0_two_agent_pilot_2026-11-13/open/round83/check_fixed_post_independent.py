#!/usr/bin/env python3
"""Independent A42 small-clock/planes and exact symbolic-budget audit."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
from hashlib import sha256
import importlib.util,json,sys
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
owner=D/'round42/fixed_post_paid_family.py';pp=D/'round42/FIXED_POST_PAID_FAMILY_PLAN.json'
spec=importlib.util.spec_from_file_location('b83_a42',owner);p=importlib.util.module_from_spec(spec);sys.modules[spec.name]=p;spec.loader.exec_module(p)
plan=json.loads(pp.read_text());assert all(sha256(Path(f).read_bytes()).hexdigest()==h for f,h in plan['source_sha256'].items())

# Exact fixed-post derivative for a nonconstant positive 4D M, all six real
# skew planes; U is NOT varied when input varies.
chi=s.Matrix([s.Rational(1,2)]*4);M=s.diag(s.Rational(4,5),s.Rational(9,10),s.Rational(3,4),s.Rational(7,8))
r=s.sqrt((chi.T*M*M*chi)[0]);xi=M*chi/r;d=(chi.T*xi)[0];K=chi*xi.T-xi*chi.T
U=s.eye(4)+K+K*K/(1+d)
assert (U.T*chi-xi).applyfunc(s.simplify)==s.zeros(4,1)
nonzero=0
for i,j in combinations(range(4),2):
    X=s.zeros(4);X[j,i]=1;X[i,j]=-1
    cd=(chi.T*U*M*X*chi)[0]
    qd=(chi.T*(X.T*M*M+M*M*X)*chi)[0]
    assert s.simplify(2*r*cd-qd)==0
    if s.simplify(cd)!=0:nonzero+=1
assert nonzero>0

# SAM-only affine maps a→0,b→pivot, inverse restores all bits. Native DAG
# support/counts checked separately with all-column A38 X macro contracts.
ks={'pi8':1,'pi6':2,'half_theta':3,'minus_half_theta':4,'minus_theta':5,'beta':6,'minus_beta':7}
mac=p.native.Macros({'status':'PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS','error_bits':20000,
      'rotations':{name:{'exponent_hex':hex(v)} for name,v in ks.items()}})
def classical(x,op):
    name,*w=op
    return x^(1<<w[0]) if name=='X' else x^((1<<w[1]) if x>>w[0]&1 else 0)
for m in (3,4):
    sam=tuple(range(2,2+m))
    for a,b in combinations(range(1<<m),2):
        pivot,ops=p.plane_affine(a,b,tuple(range(m)))
        assert all(op[0] in ('X','CX') for op in ops)
        for x in range(1<<m):
            y=x
            for op in ops:y=classical(y,op)
            if x==a:assert y==0
            if x==b:assert y==1<<pivot
            for op in reversed(ops):y=classical(y,op)
            assert y==x
        cnt=Counter()
        for tree in p.plane_blocks(a,b,2,sam,mac):
            cnt.update(p.native.counts(tree))
            for leaf in p.a41.e.leaves(tree):assert all(q in sam for q in leaf['wires'])
        assert cnt==p.plane_counts(m,a,b,2,ks['pi8'])

# Full toy family with one fixed identical post, three independent input
# directions and separate outgoing probes, all using actual execution API.
sam=(2,3,4);n=5;core=[p.gate('G',0),p.gate('CX',sam[0],1),p.gate('G',1)]
post=[p.gate('G',sam[0]),p.gate('CX',sam[1],sam[2])]
def cc(words):
    z=Counter()
    for w in words:z.update(p.native.counts(w))
    return z
cfg=p.align(n,sam,cc(core),cc(post),(2,3),3,1);cfg['K']=2
histories=[]
for sign in ('centre','plus','minus'):
    for axis in range(3):histories.append({'incoming_sign':sign,'incoming_index':axis})
for aa,bb in ((0,1),(1,7),(3,5)):
    for k0 in (1,3):histories.append({'outgoing_plane':(aa,bb),'outgoing_power':k0})
for args in histories:
    dim=1;Dclock=0;N=0;gates=[];last=None
    for row in p.execution_stages(cfg,lambda:iter(core),lambda:iter(post),mac,**args):
        Dclock+=dim;N+=1;last=row
        if row['kind']=='canonical_RAW_birth':assert row['wire']==dim.bit_length()-1;dim*=2
        else:gates.append(row['gate'])
    assert N==cfg['Nbase']+2*cfg['K'] and dim==1<<(n+cfg['K'])
    assert Dclock==(1<<n)*(cfg['Lbase']-2+3*(1<<cfg['K']))-1
    assert len(gates)==cfg['Lbase']+cfg['K']
    assert last=={'kind':'final_unitary_g','gate':p.gate('G',n+cfg['K']-1)}
    start=cfg['preL'];assert gates[start:start+len(core)]==core
    assert gates[start+len(core):start+len(core)+len(post)]==post

# Full rational growing-clock T, P and F on independent toy construction.
def check_clock(retained):
    co,si=s.Rational(3,5),s.Rational(4,5)
    def birth(d):return (co*s.eye(d)).col_join(si*s.eye(d))
    def rot(d):return (co*s.eye(d)).row_join(-si*s.eye(d)).col_join((si*s.eye(d)).row_join(co*s.eye(d)))
    actions=[birth(1),rot(1)];passive=[birth(1),s.eye(2)];dims=[1,2];dim=2
    for _ in range(retained):
        dims.extend((dim,2*dim));actions.extend((birth(dim),rot(dim)));passive.extend((birth(dim),s.eye(2*dim)));dim*=2
    N=len(actions);Dclock=sum(dims);starts=[];pos=0
    for width in dims:starts.append(pos);pos+=width
    def inc(j):
        z=s.eye(dims[j])
        for i in range(j,N-1):z=passive[i]*z
        return z
    R=inc(0).T
    for j in range(1,N):R=R.col_join((s.eye(dims[j])-passive[j-1]*passive[j-1].T)*inc(j).T)
    assert R.T*R==s.eye(dims[-1])
    shift=s.zeros(Dclock)
    for j in range(N-1):shift[starts[j+1]:starts[j+1]+dims[j+1],starts[j]:starts[j]+dims[j]]=actions[j]
    Ef=s.zeros(dims[-1],Dclock);Ef[:,starts[-1]:]=s.eye(dims[-1]);T=shift+R*actions[-1]*Ef
    assert T.T*T==s.eye(Dclock) and T*T.T==s.eye(Dclock)
    P=s.zeros(Dclock);A=s.eye(1)
    for j in range(N):
        P[starts[j]:starts[j]+dims[j],starts[j]:starts[j]+dims[j]]=A*A.T
        if j<N-1:A=actions[j]*A
    C=(inc(0).T*actions[-1]*A)[0]
    Fmat=P*T.T*(s.eye(Dclock)-P)*T*P
    last=s.zeros(Dclock);last[starts[-1]:,starts[-1]:]=A*A.T
    assert Fmat==(1-C*C)*last and s.trace(last)==1
    assert Dclock==2*(1-2+3*(1<<retained))-1
    zz=s.Rational(1,16);assert (s.eye(Dclock)-zz*Fmat).det()==1-zz+zz*C*C
for K0 in (1,2):check_clock(K0)

# All production cardinalities and bounds are independently read/recomputed;
# no call to the production provider (which must remain guarded).
config=p.production_configuration();bounds={k:F(int(v['numerator_hex'],16),int(v['denominator_hex'],16)) for k,v in plan['bounds'].items()}
assert config['n']==10407050782 and config['Nbase'].bit_length()==25457
assert config['K']==137444 and config['dimension_debt']==4032
assert int(plan['Lbase_hex'],16)==config['Lbase'] and int(plan['Nbase_hex'],16)==config['Nbase']
assert int(plan['actual_clock_layers_N_hex'],16)==config['Nbase']+2*config['K']
assert plan['last_actual_g']==p.gate('G',config['n']+config['K']-1)
assert plan['clock_dimension']=='2^n*(Lbase-2+3*2^K)-1'
assert plan['post_moved_with_incoming_P_f'] is False
try:next(p.execution_stages(config,lambda:iter(()),lambda:iter(()),mac))
except NotImplementedError:pass
else:raise AssertionError('upper-bound counts accepted as actual production word')
coreplan=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text())
assert int(plan['original_RAW_checkpoint_layer_hex'],16)==config['n']+config['preL']+int(coreplan['joint_RAW_source_checkpoint_native_prefix_calls'])

def decode(v):return F(int(v['numerator_hex'],16),int(v['denominator_hex'],16))
z,t,gs=F(1,2**20),F(1,2**1618),F(1,2**3158)
e=F(1,2**14623);da=F(1,2**4852);d0=1-z;m=2688;half=(m+1)//2
bracket=8/d0+24*z/d0**2+16*z*z/d0**3
taylor=t*t*bracket/(16*gs);angle=da/(t*gs)
heat=F(6*config['Nbase'],359)/(t*(F(8,3)*z*gs))*F(1,2**(config['K']//4))
mu=F((1<<(m-1))+40*m,1<<20000);delta=e+mu
l2=(1<<(half+1))*delta/gs+(1<<m)*delta*delta/(2*t*gs)
dual=(1<<half)*l2;heatdual=(1<<(m+half))*heat
expected={'fixed_native_post_incoming_derivative_error':e/gs,'incoming_finite_Taylor':taylor,
          'incoming_B63_angle_error':angle,'heat_each_row':heat,
          'incoming_full_H_plus_J_vs_reduced_each_row':e/gs+taylor+angle+heat,
          'outgoing_probe_full_op_error':mu,'outgoing_state_combined_error':delta,
          'outgoing_feedback_full_finite_covector_dual':dual,'outgoing_heat_full_finite_covector_dual':heatdual,
          'outgoing_full_H_plus_J_finite_covector_dual':dual+heatdual}
for key,val in expected.items():assert bounds[key]==val
assert bounds['incoming_corrected_2688_covector_error']==55*expected['incoming_full_H_plus_J_vs_reduced_each_row']<F(1,2**70)
assert bounds['incoming_covector_norm_lower']==F(1,2**46)-bounds['incoming_corrected_2688_covector_error']>F(1,2**47)
assert bounds['incoming_covector_norm_upper']==F(1,2**16)+bounds['incoming_corrected_2688_covector_error']<F(1,2**15)
assert bounds['incoming_covector_vs_actual_mean_geometry']==F(1,2**15)+bounds['incoming_corrected_2688_covector_error']<F(1,2**14)
assert dual+heatdual<F(1,2**75)
assert all(plan[k] is False for k in ('full_original_H1_marks_and_four_slots_proved','same_prior_F_N_fibre_claimed','independent_inner_Q_rows_stationary_claimed','full_Cost_Info_binding_or_refinement_proved','physical_C_closed','GR_closed'))

out={'status':'PASS_INDEPENDENT_FIXED_POST_FINITE_FAMILY_AUDIT',
     'owner_sha256':sha256(owner.read_bytes()).hexdigest(),'plan_sha256':sha256(pp.read_bytes()).hexdigest(),
     'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
     'exact_fixed_post_vs_reduced_derivative_all_4d_planes_checked':True,
     'all_small_planes_m3_m4_affine_and_native_counts_checked':True,
     'full_toy_families_replayed':len(histories),
     'independent_full_clock_T_P_F_fixtures_K1_K2':True,
     'same_post_in_incoming_histories_checked':True,
     'production_Nbase_bits':25457,'same_K_all_endpoints':137444,
     'coefficient_of_2_to_K_in_D':3,'production_upper_counts_guarded':True,
     'all_rational_bounds_and_geometry_transfer_checked':True,
     'A42_H1_admission_or_inner_Q_stationarity_proved':False,
     'production_word_or_full_heat_trace_evaluated':False,'physical_C_closed':False,'GR_closed':False}
(HERE/'B83_FIXED_POST_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
