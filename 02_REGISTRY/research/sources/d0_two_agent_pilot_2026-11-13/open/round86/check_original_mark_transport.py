#!/usr/bin/env python3
"""B86 typed-prefix identities, original mark witnesses, exact budgets."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import json,sys
import sympy as sp
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent.parent
REPO=O.parents[4]
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
OWNER=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md')
sys.path.insert(0,str(D/'round30'));import source_mark_registry as reg
sys.path.insert(0,str(O/'round25'));import targets
owner=OWNER.read_text()
for fragment in ('The canonical bank checkpoint fixes WORK/SITE at the writer\'s entry;',
 'The free logical controls p are the separate CODE/protected preparation',
 'Their complete marked',
 'an additional unsplit',
 'MG\'s full prepared-isometry marks are',
 'The FOUR MG12 occurrences remain independent.',
 'All new births precede the variable square body;'):
 assert fragment in owner,fragment
source=reg.s;slots=source.g.namespace()['source_slots']
assert len(slots)==1372
assert set(x['bank'] for x in slots)=={'y+','y-','f','0','x+','x-','q'}
assert Counter(x['bank'] for x in slots)==Counter({x:196 for x in targets.BANKS})
assert 'current_mark' not in {x['bank'] for x in slots}
stages=source.stages();assert sum(x['kind']=='SOURCE' for x in stages)==1372
binding=reg.original_binding();assert binding['site_bindings'][5]['site']==[0,0,1,1]
assert binding['leaf_templates'][2]['name']=='u/0/2'
assert binding['leaf_templates'][22]['name']=='M/base/0/1/2'
assert binding['leaf_templates'][272]['name']=='X/base/0'
u=reg.leaf_mark(5,2);link=reg.leaf_mark(5,22,choi_bank='q');car=reg.leaf_mark(5,272)
assert (u['source_slot'],u['original_Julia_address_input_output'])==(392,[21,0,4])
assert (link['source_slot'],link['operator_norm_upper']['integer'])==(1340,65568)
assert (car['source_slot'],car['original_CAR_internal_site_and_grade'])==(1342,[5,0])
assert reg.choose_slot('f','CAR','T1')==558
coord=json.loads((O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()[2])
assert coord=={'site':[0,0,1,1],'kind':'coframe','role':0,'component':2,'sam_index':2}
# Exact inequalities; pi>3 and sqrt(2)<3/2 imply psi_ref>1/100.
s=F(1,2**30);t=F(1,2**1618);erru=F(1,2**3215);errl=F(1,2**3214);errcar=F(1,2**3223);ang=F(1,2**4852)
assert F(3,200)/F(3,2)==F(1,100)
assert F(1,100)-s>F(9,1000)
assert F(17,16)*6/(1-6*s)<7
assert F(3,3200)-7*s>F(9,10000)
assert (F(9,1000)-errcar)/(2*256)>F(1,2**16)
assert (F(9,10000)-errl)/(2*65568)>F(1,2**28)
# For R(t), ||R^T E R−E||=s|sin t|. Rigorous Taylor lower.
assert s*(t-t**3/6)-2*erru-2*s*ang>F(1,2**1650)
# For physical positive G power, ||G−I||≥||R(t)−I||−ang>t/2.
assert t-t**3/24-ang>t/2
# Confirm the source-declared fields and centre values as diagnostics only;
# quantitative conclusions use the rational inequalities above.
site=targets.INDEX[(0,0,1,1)]
for bank in ('f','x+','x-'):
 assert list(targets.fields(bank)[2][site])==[0.0,0.0]
for bank in ('y+','y-','0','q'):
 assert targets.fields(bank)[1][site,0,1,2]==0.0
_,links,psi=targets.fields('current_mark')
assert psi[site,0]>0.01 and abs(links[site,0,1,2])>0.0009
# Real exact algebra: Q on SAM, a controlled bank, and work-only D.
# This fixture tests the universal identity, it is not the original mark.
R=sp.Rational;G=sp.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]])
I=sp.eye;Q=sp.kronecker_product(G,I(2));rot=sp.Matrix([[R(5,13),-R(12,13)],[R(12,13),R(5,13)]])
B=sp.diag(I(2),rot);Dfix=sp.kronecker_product(I(2),rot)
J=sp.Matrix([[1,0],[0,0],[0,1],[0,0]]) # canonical WORK |0>
V=Dfix*B*J;assert V.T*V==I(2) and Q*Dfix==Dfix*Q
c=sp.simplify(((G-I(2)).T*(G-I(2)))[0,0]);assert (Q-I(4)).T*(Q-I(4))==c*I(4)
delta=(Q-I(4))*V;assert delta.T*delta==c*I(2) and delta!=sp.zeros(4,2)
# Logical-mark target must follow controls: conjugated effect is not frozen.
E=sp.diag(R(1,7),R(2,7));assert G.T*E*G!=E
# At a basis vector the mean and full-vector geometric commutator conditions
# both fail for every real skew generator; displayed 3D generic variables.
x,y,z=sp.symbols('x y z',real=True);X=sp.Matrix([[0,-x,-y],[x,0,-z],[y,z,0]])
Vfield=sp.diag(2,5,9);basis=sp.Matrix([1,0,0]);comm=Vfield*X-X*Vfield
assert (basis.T*comm*basis)[0]==0 and (comm*basis)[0]==0
assert comm*basis!=basis
# Composite f-Choi/q-CAR target retains the other source factors. A small
# exact fixture shows that replacing a branch-dependent remainder by one
# fixed state changes full coherent marked operators.
f0=sp.Matrix([1,0]);f1=sp.Matrix([R(3,5),R(4,5)]);q0=sp.Matrix([1,0]);q1=sp.Matrix([R(5,13),R(12,13)])
r0=sp.Matrix([1,0]);r1=sp.Matrix([R(3,5),R(4,5)])
comp0=sp.kronecker_product(f0,q0,r0);comp1=sp.kronecker_product(f1,q1,r1)
s0=sp.Matrix([1,0]);s1=sp.Matrix([0,1]);CV=sp.kronecker_product(s0,comp0).row_join(sp.kronecker_product(s1,comp1))
assert CV.T*CV==I(2)
flip=sp.kronecker_product(sp.Matrix([[0,1],[1,0]]),I(8));cross=(CV.T*flip*CV)[0,1]
assert cross==(f0.T*f1)[0]*(q0.T*q1)[0]*(r0.T*r1)[0]
assert cross!=(f0.T*f1)[0]*(q0.T*q1)[0] # no silent deletion of remainder
# Degenerate M makes every vector outer-stationary, but a nonsymmetric
# inner kernel still supplies a nonzero independent Q direction.
M=sp.diag(R(4,5),R(4,5));yy=sp.Matrix([R(3,5),R(4,5)]);LL=sp.Matrix([[R(4,5),R(1,10)],[-R(1,10),R(4,5)]])
assert M*yy==R(4,5)*yy
assert yy[0]*yy[1]*(LL[0,1]-LL[1,0])==R(12,125)
files=[Path(__file__),OWNER,D/'round43/LOCAL_Q_PRICE_RU.md',D/'round43/local_q_price.py',
 D/'round43/LOCAL_Q_PRICE_CHECK.json',D/'round30/COMMON_RAW_SOURCE_MARKS_RU.md',
 D/'round30/marked_source_schedule.py',D/'round30/source_mark_registry.py',
 D/'round11/PERIODIC_SOURCE_BINDING.json',D/'round25/h1_namespace.py',
 O/'round25/targets.py',O/'round25/TARGETS_RU.md',O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',
 O/'round82/B82_FOUR_SLOT_Q_KERNEL_RU.md',O/'round84/B84_UNIFORM_ADJACENT_SOURCE_RU.md',
 O/'round85/B85_LOCAL_Q_PRICE_AUDIT_RU.md']
out={'status':'ORIGINAL_MARK_TRANSPORT_PARTIAL_WITH_CONCRETE_UNSPLIT_CONSUMER_GAP',
 'logical_preparations_four_independent_not_identified':True,
 'A43_early_vs_late_Q_same_p_full_presign_map_difference_gt':'2^-1619',
 'A42_Pf_plus_vs_identity_registered_u_effect_difference_gt':'2^-1650',
 'u_witness':'site_index=5, source_slot=392, leaf u/0/2, Julia address=21',
 'literal_seven_report_banks':7,'additional_unsplit_paid_bank_found':False,
 'each_report_bank_matches_unsplit_current_map':False,
 'missing_unsplit_bank_disproves_every_weaker_H1_variant':False,
 'separate_f_q_marks_automatically_equal_full_joint_prepared_map':False,
 'conditional_ideal_f_choi_q_car_composite_requires_full_remainder':True,
 'full_original_H1_FN_admission':False,'basis_vector_excluded_as_arbitrary_offcentre_Pf':False,
 'all_real_skews_admitted_as_A43_paid_rows':False,
 'original_t1_centre_is_born_interior':True,'basis_state_existing_mean_decoder_first_jet_zero':True,
 'physical_C_closed':False,'GR_closed':False,
 'source_sha256':{str(f.resolve()):sha256(f.read_bytes()).hexdigest() for f in files}}
Path(__file__).with_name('B86_MARK_TRANSPORT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
