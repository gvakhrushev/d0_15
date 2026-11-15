#!/usr/bin/env python3
"""Independent finite A52 audit; reads frozen A, writes only round102."""
from pathlib import Path
from itertools import islice, chain
from hashlib import sha256
from fractions import Fraction
import sys,json
import sympy as S
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
A=D/'round52';sys.path.insert(0,str(A))
import scoped_comparison_task as task
import check_scoped_comparison_task as frozen
paid=task.paid;nb=paid.native

def sha(p):return sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
plan=load(A/'FINITE_COMPARISON_TASK.json')
receipt=load(A/'FINITE_COMPARISON_TASK_CHECK.json')
for f,digest in plan['source_sha256'].items():assert sha(Path(f))==digest,f
for f,digest in receipt['source_sha256'].items():assert sha(Path(f))==digest,f
assert task.build()==plan
assert frozen.labels()==receipt['label_checks']
assert json.loads(json.dumps(frozen.placement()))==receipt['independent_prefix_fixtures']
assert frozen.instrument()==receipt['mathematical_label_instrument']

# Exhaust *all* ordinary names, comparing canonical packets to an
# independent specification and each actual A49 control-sign tuple.
expected_names={('centre',0,0)}
for arm in ('matched','Pf','Qf','Qb','Pb'):
    for axis in range(2688):
        for sign in (-1,1):expected_names.add((arm,axis,sign))
seen=set();packets=set()
for label in task.catalogue():
    key=(label.arm,label.axis,label.sign);assert key in expected_names and key not in seen
    expected=json.dumps({'arm':label.arm,'axis':label.axis,'plane':None,'sign':label.sign},sort_keys=True,separators=(',',':')).encode()
    assert task.encode(label)==expected and task.decode(expected)==label
    seen.add(key);packets.add(expected)
    s=label.sign
    want=({'Pf':s,'Qf':-s,'Qb':s,'Pb':-s} if label.arm=='matched' else
          {n:((-s if n in ('Qf','Pb') else s) if n==label.arm else 0) for n in ('Pf','Qf','Qb','Pb')})
    assert paid.slot_signs(label.arm,s)==want
assert seen==expected_names and len(packets)==26881
m=5376;N=1<<m
assert int(plan['request_labels']['post_probe_label_count_hex'],16)==N*(N-1)
for a,b in [(0,1),(1,2),(3,N-1),(N-2,N-1)]:
    for sign in (-1,1):
        label=task.Label('post_probe',sign,plane=(a,b))
        assert task.decode(task.encode(label))==label
        assert paid.slot_signs('post_probe',sign)==dict(Pf=0,Qf=0,Qb=0,Pb=0)
invalid=[b'{"arm":"centre","axis":0,"plane":null,"sign":true}',
         b'{"arm":"centre","axis":0,"plane":null,"sign":0,"Y":1}',
         b'{"arm":"Pf","axis":2688,"plane":null,"sign":1}',
         b'{"arm":"post_probe","axis":0,"plane":[1,1],"sign":1}',
         b'{"arm":"centre","arm":"centre","axis":0,"plane":null,"sign":0}',
         b'{ "arm":"centre","axis":0,"plane":null,"sign":0}']
for packet in invalid:
    try:task.decode(packet)
    except (ValueError,TypeError):pass
    else:raise AssertionError(packet)

# Independently shaped, padded small histories: 33 labels x 13 marks.
sam=(0,1,2); cfg={'sam':sam,'controlL':8,'coreL':60,'postL':8,'probeL':8}
before=[nb.gate('CX',0,3),nb.gate('G',4),nb.gate('CX',2,4)]
mid=[[nb.gate('CX',3,4),nb.gate('G',4)] if j%3==0 else [nb.gate('G',3)] for j in range(11)]
ret=[nb.gate('CX',4,3),nb.gate('G',4)]
def core():
    yield from before;yield {'op':'B82_CUT','name':paid.CUTS[0]}
    for x in mid:yield from x
    yield {'op':'B82_CUT','name':paid.CUTS[1]};yield from ret
def ctr(axis,sign):
    if sign:yield nb.repeat(1 if sign==1 else 3,nb.gate('G',sam[axis]))
def proc(name):
    n=task.prefixes.descriptor(name)['processor_stage_count']
    for x in mid[:n]:yield from x
def post():yield nb.gate('G',4);yield nb.gate('CX',3,4)
def probe(plane,sign):yield from ctr(1,sign)
def leaves(stream):return [q for tree in stream for q in paid.target.e.leaves(tree)]
labels=[task.Label()]+[task.Label(arm,s,j) for arm in task.ARMS for s in (-1,1) for j in (0,1,2)]
labels += [task.Label('post_probe',s,plane=(0,1)) for s in (-1,1)]
marks=['SOURCE_before_Qf']+[x['name'] for x in task.prefixes.registry()]
assert len(labels)==33 and len(marks)==13
for label in labels:
    full=leaves(paid.family_blocks(cfg,core,post,ctr,probe,**task.asdict(label)))
    assert len(full)==4*cfg['controlL']+cfg['coreL']+cfg['postL']+cfg['probeL']
    for mark in marks:
        got=leaves(task.assembled_prefix(label,mark,cfg,lambda:iter(before),proc,ctr))
        assert got==full[:len(got)]
        expected=cfg['controlL']+len(before)
        if mark!='SOURCE_before_Qf':expected+=cfg['controlL']+sum(len(x) for x in mid[:task.prefixes.descriptor(mark)['processor_stage_count']])
        assert len(got)==expected

# Inspect the actual A49-start trees, not flattened enormous words. Compare
# the production provider against a separately assembled paid Pf + SOURCE.
prod_cfg=paid.production_configuration()
actual_cases=[task.Label(),task.Label('matched',1,0),task.Label('Pf',-1,2687),
              task.Label('Qf',1,0),task.Label('Qb',-1,2687),task.Label('Pb',1,0),
              task.Label('post_probe',1,plane=(0,N-1))]
for label in actual_cases:
    pfs=paid.slot_signs(label.arm,label.sign)['Pf']
    expected=chain(paid.pad.counted_pad(lambda:paid.raw_control_factory(label.axis,pfs),prod_cfg['controlL'],prod_cfg['sam']),paid.source.source_prefix_blocks())
    assert list(islice(task.word_blocks(label),8))==list(islice(expected,8))

# Every wire pair is independently obtained from actual namespace report
# fields (rather than invoking A52.report_labels as the reference).
g=paid.source; ns=g.namespace(); flags=plan['available_report_label_tests']; actual=[]
for j,r in enumerate(ns['reports']):
    got=(g.physical_wire(r['REPORT']),g.physical_wire(r['all_READY']))
    assert (flags[j]['report_wire'],flags[j]['ready_wire'])==got
    assert flags[j]['outcomes']==[[0,0],[0,1],[1,0],[1,1]]
    assert flags[j]['frontier']==f'REPORT_{j}_complete'
    assert all(0<=q<prod_cfg['n'] and q not in prod_cfg['sam'] for q in got)
    actual.extend(got)
assert len(set(actual))==16

# Exact CP normalisation with complex, entangled input/reference; four
# outcomes retain the complete output and the external reference.
R=S.Rational;ket0=S.Matrix([1,0]);i=S.I
q=S.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]])
phase=S.diag(1,i);I2=S.eye(2)
U=S.kronecker_product(phase,q,q)
J=S.kronecker_product(I2,ket0,ket0)
F=U*J;assert F.conjugate().T*F==I2
bell=S.Matrix([1,0,0,1])/S.sqrt(2)
rho=bell*bell.conjugate().T; total=S.zeros(16);effects=[]
for r in range(2):
    for k in range(2):
        P=S.diag(*[int(((j>>1)&1)==r and (j&1)==k) for j in range(8)])
        K=P*F;E=K.conjugate().T*K;effects.append(E)
        KR=S.kronecker_product(K,I2);total+=KR*rho*KR.conjugate().T
assert sum(effects,S.zeros(2))==I2 and S.trace(total)==1
assert S.trace(S.kronecker_product(effects[0]+effects[2],I2)*rho)>0
# Unread coherent suffix detects the insertion of a physical dephasing.
plus=S.Matrix([1,1])/S.sqrt(2);projector=plus*plus.T
assert S.trace(projector*projector)==1 and S.trace(projector*S.eye(2)/2)==R(1,2)

# Independent exact A37-style envelope check on a smooth real family. It
# verifies the field and independent-post derivatives, not a native chart
# compiler or the full heat source.
y,theta=S.symbols('y theta',real=True)
d0,eta=S.symbols('d0 eta',positive=True)
rv=S.sqrt(9+y*y)/5
U=S.Matrix([[3,y],[-y,3]])/S.sqrt(9+y*y)
v=S.Matrix([S.Rational(3,5),y/5]);chi=S.Matrix([1,0])
assert S.simplify(U.T*U-S.eye(2))==S.zeros(2)
assert S.simplify(U*v-rv*chi)==S.zeros(2,1)
rot=S.Matrix([[S.cos(theta),-S.sin(theta)],[S.sin(theta),S.cos(theta)]])
c=(chi.T*rot*U*v)[0]
price=-S.log(d0+eta*c*c)
red=-S.log(d0+eta*(9+y*y)/25)
assert S.simplify(S.diff(price,theta).subs(theta,0))==0
assert S.simplify(S.diff(price,y).subs(theta,0)-S.diff(red,y))==0
# Exact sample of unitary-alignment quadratic defect, with no assumed DU*.
t=S.Rational(1,3);costheta=(1-t*t)/(1+t*t)
epsilon_sq=4*t*t/(1+t*t)
assert 0<=1-costheta**2<=epsilon_sq

assert plan['regular_field_argument_implemented'] is False
assert plan['actual_registered_fine_instrument_identified'] is False
assert plan['measurement_or_free_readback_inserted'] is False
assert plan['physical_C_closed'] is False and plan['GR_closed'] is False
inputs=[A/'scoped_comparison_task.py',A/'FINITE_COMPARISON_TASK.json',A/'check_scoped_comparison_task.py',A/'FINITE_COMPARISON_TASK_CHECK.json',A/'SCOPED_COMPARISON_TASK_RU.md',D/'round49/two_bit_paid_family.py',D/'round49/paid_padding.py',D/'round51/completed_marked_prefixes.py',D/'round37/ACTUAL_POST_SAM_STATIONARY_REDUCTION_RU.md',HERE.parent/'round73/B73_POST_SAM_REDUCTION_AUDIT_RU.md']
out={'status':'PASS_B102_SCOPED_A52_WITH_EXPLICIT_PHYSICAL_BOUNDARIES',
     'ordinary_labels_independently_exhausted':len(seen),'distinct_canonical_packets':len(packets),
     'post_probe_count_formula_verified_without_enumeration':True,
     'all_ordinary_slot_signs_independently_checked':True,
     'frozen_299_literal_fixture_replayed':True,'additional_literal_prefix_fixtures':len(labels)*len(marks),
     'actual_A49_start_trees_sampled':len(actual_cases)*8,
     'actual_REPORT_READY_physical_address_pairs':[(flags[j]['report_wire'],flags[j]['ready_wire']) for j in range(8)],
     'CP_normalization_and_Bell_reference_checked':True,'dephasing_suffix_counterexample_checked':True,
     'A37_envelope_independent_field_and_post_derivatives_checked':True,
     'alignment_quadratic_defect_exact_example_checked':True,
     'all_production_words_executed':False,'actual_registered_fine_instrument_identified':False,
     'regular_field_argument_implemented':False,'same_execution_physical_cost_info_identified':False,
     'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(f):sha(f) for f in inputs}}
(HERE/'B102_A52_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))
