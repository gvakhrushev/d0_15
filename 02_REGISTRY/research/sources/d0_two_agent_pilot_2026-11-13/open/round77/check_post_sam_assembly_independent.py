#!/usr/bin/env python3
"""Independent structural/small fixtures for A39; no production expansion."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import importlib.util,json,sys
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
owner=D/'round39/post_sam_assembly.py';planpath=D/'round39/POST_SAM_ASSEMBLY_PLAN.json'
spec=importlib.util.spec_from_file_location('audit_a39',owner)
a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
plan=json.loads(planpath.read_text())
assert all(sha256(Path(p).read_bytes()).hexdigest()==h for p,h in plan['source_sha256'].items())
# A successful aggregate build is insufficient: exercise actual centre emitter.
centre_head=next(a.endpoint_blocks('centre'))
assert a.m.counts(centre_head)['CX']>0 and a.m.counts(centre_head).get('G',0)==0

# Verify chronology recursively and symbolic signed-target inverse, independently
# of expanded native powers. Levels 0..5 cover base and both nested directions.
def inv(t):
    return (t[0],not t[1]) if t[0] in ('P','W','beta') else ('phase',t[1],not t[2],t[3])
for level in range(6):
    f=list(a.amplifier_tokens(level));b=list(a.amplifier_tokens(level,True))
    assert b==[inv(t) for t in reversed(f)]
    assert sum(t[0]=='W' for t in f)==3**level
full=list(a.post_tokens(9))
assert full[0]==('clean',False) and full[-1]==('clean',True)
assert sum(t[0]=='W' for t in full)==2*3**9==39366
assert full[1:1+len(list(a.amplifier_tokens(9,True)))]==list(a.amplifier_tokens(9,True))
token_frequencies=Counter(full)

# Test the ACTUAL lowering and budget on a small valid layout, with ordinary
# positive powers chosen as sentinels. Expanded huge production words are not run.
ks={'pi8':1,'pi6':2,'half_theta':3,'minus_half_theta':4,'minus_theta':5,'beta':6,'minus_beta':7}
cert={'status':'PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS','error_bits':20000,
      'rotations':{name:{'exponent_hex':hex(v)} for name,v in ks.items()}}
m=a.m.Macros(cert);l=a.Layout(old=9,sam_count=3)
assert sorted(l.copy_wire(q) for q in range(l.old) if q not in l.sam)==list(l.copy)
assert all(l.copy_wire(q)==q for q in l.sam)
assert len(set([*range(l.old),*l.copy,l.branch,l.flag,l.rebit,l.helper,*l.scratch]))==l.total
wtrees=[a.m.seq(a.m.gate('G',2),a.m.gate('CX',0,5),a.m.repeat(2,a.m.gate('G',8)))]
wc=Counter()
for tree in wtrees:wc.update(a.m.counts(tree))
for power in (0,2,3):
    for level in (0,1,2):
        obj=a.Assembly(power,sam_index=0,level=level,layout=l,macros=m,W_factory=lambda:iter(wtrees),W_counts=wc)
        actual=Counter()
        for tree in obj.post_blocks():actual.update(a.m.counts(tree))
        expected=obj.post_budget()
        assert actual==Counter({k:expected[k] for k in ('G','CX')})
        omitted=Counter()
        for tree in obj.post_blocks(omit_final_restore=True):omitted.update(a.m.counts(tree))
        assert omitted+Counter(G=1)==actual
        clean_false=list(obj.lower(('clean',False))); clean_true=list(obj.lower(('clean',True),omit_final_restore=True))
        assert len(clean_false)==len(l.clean) and len(clean_true)==len(l.clean)-1
        assert list(obj.lower(('P',False)))==([] if power==0 else [a.m.repeat(power,a.m.gate('G',obj.sam))])

# Exercise the SAME endpoint and execution generators end-to-end with small
# layout/powers and 3 explicitly selected toy retention pairs (not production K).
toy={name:a.Assembly(power,sam_index=0,level=1,layout=l,macros=m,
        W_factory=lambda:iter(wtrees),W_counts=wc)
     for name,power in (('centre',0),('plus',2),('minus',3))}
toyconfig=list(a.align_family(toy));toyconfig[-1]=3;toyconfig=tuple(toyconfig)
_,_,toy_pre,toy_post,toy_L,toy_N,toy_K=toyconfig
for name in toy:
    dim=1;dim_sum=0; stages=0;counts=Counter();last=None
    for stage in a.execution_stages(name,sam_index=0,configuration=toyconfig):
        dim_sum+=dim;stages+=1;last=stage
        if stage['kind']=='canonical_RAW_birth': dim*=2
        else: counts[stage['gate']['op']]+=1
    assert last=={'kind':'final_unitary_g','gate':a.m.gate('G',l.scratch[-1])}
    assert stages==toy_N+2*toy_K
    assert dim==(1<<(l.total+toy_K))
    assert dim_sum==(1<<l.total)*(toy_L-3+4*(1<<toy_K))-1
    assert sum(counts.values())==toy_L+toy_K

# Padding is exactly identity on all computational columns, including odd 5.
for length in range(4,21):
    leaves=[]
    for tree in a.identity_padding(length,l):leaves.extend(a.primitive_leaves(tree))
    assert len(leaves)==length and all(x['op']=='CX' for x in leaves)
    for bits in product((0,1),repeat=3):
        state=dict(zip((l.branch,l.flag,l.helper),bits))
        for gate in leaves:
            x,y=gate['wires'];state[y]^=state[x]
        assert tuple(state[q] for q in (l.branch,l.flag,l.helper))==bits

# Clock D is sum of carrier dimensions BEFORE the final real G; check literal
# toy trajectories, not just the same closed formula in A39.
for n in range(1,8):
    for L in range(4,8):
        for K in range(5):
            dims=[1];dim=1
            for _ in range(n):dim*=2;dims.append(dim)
            for _ in range(L-1):dims.append(dim)
            for _ in range(K):dim*=2;dims.extend((dim,dim))
            # No appended terminal vertex for final G: its incoming vertex
            # is the last element already in dims.
            actual=sum(dims)
            assert actual==(1<<n)*(L-3+4*(1<<K))-1
            assert dim==(1<<(n+K))

# Price: full real vector includes all private/rebit failure. Exact overlap
# identity, and nonnegative deviations allow endpoint difference ≤ one bound.
e,r=s.symbols('e r',real=True,nonnegative=True)
c=r*(1-e**2/2)
assert s.expand(r*r-c*c-r*r*(e*e-e**4/4))==0
# Toy vector with nonzero private failure: projected overlap is 3/5, while
# e²=4/5. Ignoring its failure would falsely report zero alignment error.
x=s.Matrix([1,0]); y=s.Matrix([s.Rational(3,5),s.Rational(4,5)])
assert (y-x).dot(y-x)==s.Rational(4,5) and x.dot(y)==1-(y-x).dot(y-x)/2

# Independently check all target hashes, endpoints common clock, rational bound
# algebra and separate K-born retention. Fractions may be huge but stay exact.
aa,post,preL,postL,Lbase,Nbase,K=a.pair_configuration()
assert set(aa)==set(post)=={'centre','plus','minus'}
assert aa['centre'].power==0 and all(x.l.total==31221149661 for x in aa.values())
prod_layout=aa['centre'].l
roles=prod_layout.records()
assert roles[0]['start']==0 and roles[-1]['stop']==prod_layout.total
assert all(roles[i]['stop']==roles[i+1]['start'] for i in range(len(roles)-1))
assert prod_layout.copy_wire(0)==prod_layout.copy.start
assert prod_layout.copy_wire(1)==prod_layout.copy.start+1
assert prod_layout.copy_wire(2)==2 and prod_layout.copy_wire(2689)==2689
assert prod_layout.copy_wire(2690)==prod_layout.copy.start+2
assert prod_layout.copy_wire(prod_layout.old-1)==prod_layout.copy.stop-1
assert all(prod_layout.old<=q<prod_layout.total for q in
           (prod_layout.branch,prod_layout.flag,prod_layout.rebit,prod_layout.helper,prod_layout.scratch.start,prod_layout.scratch[-1]))
for kind in ('good','start','chi'):
    controls,born=prod_layout.controls(kind)
    assert all(prod_layout.old<=r.start<r.stop<=prod_layout.total or
               2<=r.start<r.stop<=2690 for r in controls.ranges)

assert K==146448 and Nbase.bit_length()==31740
for key,obj in aa.items():
    assert preL-obj.power>=4 and postL-post[key]['G']-post[key]['CX']>=4
    counts={k:int(v,16) for k,v in plan['actual_gate_counts_with_retention_hex'][key].items()}
    assert sum(counts.values())==Lbase+K
    assert int(plan['post_counts_and_error_units_hex'][key]['E'],16)==post[key]['E']
    explicit=Counter()
    for tok,count in token_frequencies.items():
        one=obj.token_budget(tok)
        for k,v in one.items(): explicit[k]+=count*v
    for k in ('G','CX','E'): assert explicit[k]==post[key][k]

assert int(plan['Nbase_hex'],16)==Nbase and int(plan['Lbase_hex'],16)==Lbase
assert int(plan['actual_clock_layers_N_hex'],16)==Nbase+2*K
assert plan['final_actual_g']=={'op':'G','wire':aa['centre'].l.scratch[-1]}
assert plan['final_actual_g']['wire']==aa['centre'].l.total-1
assert plan['late_retention_pairs']==K
coreplan=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text())
mark=prod_layout.total+preL+int(coreplan['joint_RAW_source_checkpoint_native_prefix_calls'])
assert int(plan['original_RAW_checkpoint_layer_hex'],16)==mark

z,t,gs=F(1,2**20),F(1,2**1618),F(1,2**3158)
assert F(3,4)*F(2,3)*2==1 # strict d0>3/4 and a>2/3 make 2*d0*a>1
for key in ('post_native_error','full_post_vector_error','native_feedback_fd_error','analytic_fd_truncation','incoming_angle_fd_error','all_mode_heat_fd_error','complete_finite_comparison_error','corrected_2688_error'):
    assert key in plan['bounds']
def dec(obj):return F(int(obj['numerator_hex'],16),int(obj['denominator_hex'],16))
bounds={key:dec(v) for key,v in plan['bounds'].items()}
assert bounds['post_native_error']==max(row['E'] for row in post.values())*F(1,2**20000)
assert bounds['full_post_vector_error']==5*F(1,2**3014)**2+4*F(1,2**6560)+bounds['post_native_error']
assert bounds['native_feedback_fd_error']==bounds['full_post_vector_error']**2/(2*t*gs)
assert bounds['incoming_angle_fd_error']==F(1,2**4852)/(t*gs)
assert bounds['post_feedback_unit_skew_row']==bounds['full_post_vector_error']/gs
bracket=8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
assert bounds['analytic_fd_truncation']==t*t*bracket/(16*gs)
gamma_under=F(8,3)*z*gs
assert bounds['all_mode_heat_fd_error']==F(6*Nbase,359)/(t*gamma_under)*F(1,2**(K//4))
assert F(5,6)**4<F(1,2) and K%4==0

assert bounds['complete_finite_comparison_error']==sum(bounds[k] for k in ('native_feedback_fd_error','analytic_fd_truncation','incoming_angle_fd_error','all_mode_heat_fd_error'))
assert bounds['complete_finite_comparison_error']<F(1,2**74)
assert bounds['corrected_2688_error']==55*bounds['complete_finite_comparison_error']<F(1,2**68)
# Componentwise finite errors may align; 55 includes sqrt(2688), the actual
# sampling factor lower bound, and the inverse mean-Jacobian norm.
assert 2688 < 52**2
assert F(52,1)/(2*F(309,500)*F(39,50)*(1-F(1,2**23)))<55
assert F(1,2**46)-F(1,2**68)>F(1,2**47)
assert F(1,2**16)+F(1,2**68)<F(1,2**15)
assert F(1,2**15)+F(1,2**68)<F(1,2**14)


out={'status':'PASS_STRUCTURE_SMALL_FIXTURES_AND_EXACT_BOUND_AUDIT',
     'A39_owner_sha256':sha256(owner.read_bytes()).hexdigest(),
     'A39_plan_sha256':sha256(planpath.read_bytes()).hexdigest(),
     'own_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
     'production_centre_emitter_first_block_checked':True,
     'token_inverse_chronology_levels_0_to_5':True,
     'controlled_W_occurrences_post':39366,
     'production_tokens_sum_matches_each_recursive_budget':True,
     'toy_layout_token_budgets_and_deferred_last_g_checked':True,
     'padding_all_columns_and_clock_toys_checked':True,
     'full_end_to_end_toy_family_centre_plus_minus_executed':True,
     'corrected_2688_factor_55_includes_sqrt_dimension':True,
     'production_layout_support_and_checkpoint_formula_checked':True,
     'same_eta_common_K':K,'early_births':31221149661,'Nbase_bit_length':31740,
     'real_full_vector_quadratic_price_identity_checked':True,
     'full_production_stream_expanded':False,'actual_heat_trace_computed':False,
     'native_smooth_family_proved':False,'physical_C_closed':False,'GR_closed':False}
(HERE/'B77_ASSEMBLY_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
