#!/usr/bin/env python3
"""A39 versus a paid same-layout A30 reference; passive-Spin lift fixture.

No production stream is expanded. Numerical lower bounds are conditional on
pinned A37/A39 receipts; none is asserted from a finite toy matrix alone.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import importlib.util,json,sys
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;O=HERE.parent
ROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
owner=D/'round39/post_sam_assembly.py'; planfile=D/'round39/POST_SAM_ASSEMBLY_PLAN.json'
spec=importlib.util.spec_from_file_location('b78_a39',owner);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
plan=json.loads(planfile.read_text())
assert all(sha256(Path(p).read_bytes()).hexdigest()==h for p,h in plan['source_sha256'].items())
conf=a.pair_configuration();aa,post,preL,postL,Lbase,Nbase,K=conf
assert aa['centre'].power==0 and plan['early_births']==31221149661
l=aa['centre'].l
# Reference family: A30 W with exactly the same early births, pre length,
# post length and K. Its last CX is preceded by the SAME CX before retention;
# an all-column CX identity fills the other post slots. No inverse is free.
def reference_prefix_blocks(configuration):
    family,_,pre,postlen,_,_,_=configuration; obj=family['centre']; lay=obj.l
    yield from a.identity_padding(pre,lay)
    yield from obj.W_factory()
    yield from a.identity_padding(postlen-2,lay)
    yield a.m.gate('CX',lay.branch,lay.flag)
def reference_final_gate(configuration):
    lay=configuration[0]['centre'].l
    return a.m.gate('CX',lay.branch,lay.flag)
def reference_stages(configuration):
    family,_,_,_,_,_,retained=configuration;lay=family['centre'].l
    for row in lay.records():
        for wire in range(row['start'],row['stop']):
            yield {'kind':'canonical_RAW_birth','wire':wire,'role':row['role'],
                   'carrier_qubits_after':wire+1}
    for block in reference_prefix_blocks(configuration):
        for gate in a.primitive_leaves(block):yield {'kind':'square_unitary_edge','gate':gate}
    for j in range(retained):
        wire=lay.total+j
        yield {'kind':'canonical_RAW_birth','wire':wire,'role':'late_retention','carrier_qubits_after':wire+1}
        yield {'kind':'square_unitary_edge','gate':a.m.gate('G',wire)}
    yield {'kind':'final_unitary_g','gate':reference_final_gate(configuration)}
assert postL-2>=4 and preL>=4
pre_count=sum(sum(a.m.counts(x).values()) for x in a.identity_padding(preL,l))
post_count=sum(sum(a.m.counts(x).values()) for x in a.identity_padding(postL-2,l))+2
assert pre_count==preL and post_count==postL
assert reference_final_gate(conf)==a.m.gate('CX',l.branch,l.flag)
assert l.branch<l.total and l.flag<l.total and l.branch!=l.flag
# The two branch/flag CX are exact involutions, and the K intervening Gs
# address only new q>=total: hence they commute and post is exactly I.
assert K==146448 and plan['final_actual_g']['wire']==l.scratch[-1]

# Explicit product-vector example checks the nonconstant-M variance identity
# and a real born-private alignment (not used as proof of production size).
chi=s.Matrix([s.Rational(3,5),s.Rational(4,5)])
M=s.diag(s.Rational(4,5),s.Rational(12,13))
c=(chi.T*M*chi)[0];r2=(chi.T*M*M*chi)[0]
var=((M-c*s.eye(2))*chi).dot((M-c*s.eye(2))*chi)
assert s.simplify(r2-c*c-var)==0 and var>0

# Rigorous consequence of pinned A37/A39 bounds, no numerical float:
# ||C_red||>2^-46 and ||R||<55/s imply a unit X with |d_red(X)|>2^-46/55.
# |Dq|=4a(gs)|d_red|, a>2/3, gs>2^-3158. Cauchy gives
# |Dq|<=4 sqrt(Var_chi M) since ||M+cI||<=2 and ||X||<=1.
dred_lb=F(1,55*2**46);assert dred_lb>F(1,2**52)
dq_lb=4*F(2,3)*F(1,2**3158)*dred_lb
assert dq_lb>F(1,2**3209)
var_lb=dq_lb*dq_lb/16
assert var_lb>F(1,2**6422)
# A39 full-vector error e<2^-6024 => loss in r² at most e².
err2=F(1,2**12048)
assert var_lb-err2>F(1,2**6423)
assert (var_lb-err2)/2>F(1,2**6424)
assert F(1,2**6423)>err2
# p=(sqrt5-1)/2>1/2, so after K real retained pairs the difference
# in squared complete cold-return amplitude is >2^-(K+6423).
assert K+6423==152871

# Lazy passive Spin extension: H0=C^4, all original q shifted by 2 and
# every untouched SourceSpin bit 0,1 remains outside all gate supports.
# It is a new supplied input cut, never a claim to create an unknown spin.
def passive_spin_stages(sign,configuration):
    for stage in a.execution_stages(sign,sam_index=0,configuration=configuration):
        z=dict(stage)
        if z['kind']=='canonical_RAW_birth':
            z['wire']+=2;z['carrier_qubits_after']+=2
        else:
            g=z['gate'];z['gate']={'op':g['op'],'wires':[q+2 for q in g['wires']]}
        yield z
# Same actual execution generator on a bounded valid physical layout.
ks={'pi8':1,'pi6':2,'half_theta':3,'minus_half_theta':4,'minus_theta':5,'beta':6,'minus_beta':7}
cert={'status':'PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS','error_bits':20000,
      'rotations':{name:{'exponent_hex':hex(v)} for name,v in ks.items()}}
mac=a.m.Macros(cert);small=a.Layout(old=9,sam_count=3)
wtrees=[a.m.seq(a.m.gate('G',2),a.m.gate('CX',0,5))];wc=Counter()
for tree in wtrees:wc.update(a.m.counts(tree))
toy={name:a.Assembly(power,sam_index=0,level=0,layout=small,macros=mac,
      W_factory=lambda:iter(wtrees),W_counts=wc)
      for name,power in (('centre',0),('plus',2),('minus',3))}
toyconf=list(a.align_family(toy));toyconf[-1]=2;toyconf=tuple(toyconf)
# End-to-end reference has the same toy N,D as the genuine A39 centre.
ref_dim=1;ref_D=0;ref_N=0;ref_last=None
for stage in reference_stages(toyconf):
    ref_D+=ref_dim;ref_N+=1;ref_last=stage
    if stage['kind']=='canonical_RAW_birth':ref_dim*=2
assert ref_N==toyconf[-2]+2*toyconf[-1]
assert ref_D==(1<<small.total)*(toyconf[4]-3+4*(1<<toyconf[-1]))-1
assert ref_last=={'kind':'final_unitary_g','gate':reference_final_gate(toyconf)}
for name in toy:
    src=a.execution_stages(name,sam_index=0,configuration=toyconf)
    dst=passive_spin_stages(name,toyconf)
    n=0
    for old,new in zip(src,dst):
        n+=1;assert old['kind']==new['kind']
        if old['kind']=='canonical_RAW_birth':
            assert new['wire']==old['wire']+2 and new['carrier_qubits_after']==old['carrier_qubits_after']+2
        else:
            assert new['gate']['op']==old['gate']['op']
            assert new['gate']['wires']==[q+2 for q in old['gate']['wires']]
            assert all(q>=2 for q in new['gate']['wires'])
    assert n==toyconf[-2]+2*toyconf[-1]
# Tensor-identity lift: D, Z, C* C multiply by 4 as typed, while H gains
# log(4)/beta and J/gain multiply by 4. This does not identify full Cost-Info.
lam,bet,Z=s.symbols('lam bet Z',positive=True)
assert s.simplify(s.log(4*Z)/bet-s.log(Z)/bet-s.log(4)/bet)==0
assert s.det(s.eye(4)*lam)==lam**4

pinned=[Path(__file__),owner,planfile,D/'round37/ACTUAL_POST_SAM_STATIONARY_REDUCTION_RU.md',
        D/'round31/ACTUAL_MEAN_GEOMETRY_LIFT_RU.md',
        O/'round69/B69_ACTUAL_TASK_INPUTS_AND_ADMISSION_RU.md',
        O/'round72/B72_BACKWARD_MARKED_OUTPUT_SUBSYSTEM_RU.md',
        O/'round77/B77_A39_COMPOSITION_CLOCK_AUDIT_RU.md',
        ROOT/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md',
        ROOT/'02_REGISTRY/research/A4D_SCOPED_NATIVE_KAPPA_CONTRACT_2026_11_03.md',O/'inputs/correction_7fu.txt']
out={'status':'PROVED_CONDITIONAL_FIXED_OUTPUT_MISMATCH_AND_PASSIVE_SPIN_LIFT_NOT_FULL_ADMISSION',
     'same_layout_paid_reference_extension_constructed':True,
     'reference_post_gate_count_equals_A39_post_length':True,
     'reference_last_g':'CX(branch,flag), paid separately, not the A39 last G',
     'centre_cold_squared_gap_gt':'2^-6423 before common retained factor',
     'centre_post_is_not_identity_on_canonical_new_input_sector_norm_gt':'2^-6424',
     'centre_full_cold_squared_gap_gt':'2^-152871 using p>1/2 and K=146448',
     'gap_consumes_A37_reduced_covector_lower_bound':True,
     'gap_consumes_A39_full_vector_error_bound':True,
     'H1_demands_WJ_or_born_terminal_reader':False,
     'original_fixed_layout_FN_membership':False,
     'original_H1_partial_membership_proved':False,
     'passive_spin_lift_generator_constructed':True,
     'passive_spin_lift_same_complete_task_membership_proved':False,
     'independent_four_preparation_occurrences_proved':False,
     'full_giant_native_word_expanded_or_run':False,'Cost_Info_binding_proved':False,
     'physical_C_closed':False,'GR_closed':False,
     'source_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in pinned}}
(HERE/'B78_FIBRE_BOUNDARY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
