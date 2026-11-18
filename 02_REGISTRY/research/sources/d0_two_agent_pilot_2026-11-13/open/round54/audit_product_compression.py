#!/usr/bin/env python3
"""Independent A27 slot, event polynomial and conditional scalar positivity audit."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import itertools,json,sympy as s
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');files=[D/'round27/PRODUCT_SOURCE_COMPRESSION_CHECK.json',D/'round27/product_source_compression.py',D/'round25/H1_NAMESPACE_PLAN.json',O/'round25/COPY_SLOTS.jsonl',O/'round49/SC6_ACTIVE_PORT_OWNER_CHECK.json',O/'round53/READY_GAIN_INTEGER_INDEPENDENT_CHECK.json',O/'round52/GLOBAL_COUNTS_ERROR_INDEPENDENT_CHECK.json',O/'round33/ACTUAL_COMPRESSION_INPUTS_CHECK.json',O/'round34/A16_FULL_DEGREE_CHECK.json',O/'round34/A16_WALK_WIRING_CHECK.json',P/'IDEAL_SOURCE_LEAF_MOMENTS_EXACT.json',P/'REFERENCE_GEOMETRY_EXACT_CHECK.json',P/'FLAT_HF_ALL_COFRAMES_CHECK.json',P/'REPORT_BETA_EXACT_CHECK.json'];h=lambda q:sha256(q.read_bytes()).hexdigest();pins={str(f):h(f) for f in files};check=json.loads(files[0].read_text());ns=json.loads(files[2].read_text());slots=[json.loads(x) for x in files[3].read_text().splitlines()];normal=json.loads(files[4].read_text())['term_normal_forms']
for path,digest in check['source_sha256'].items():assert h(Path(path))==digest,path
# Independent exact bijection: B25's older "material" = A25's CAR.
translate={'Choi':'Choi','material':'CAR'};want={(r['bank'],r['sign'],translate[r['type']],r['copy']) for r in slots};actual={(r['bank'],r['walk'],r['kind'],r['copy']) for r in ns['source_slots']};assert len(want)==len(actual)==1372 and want==actual
terms=[(z['selector'],z['sign'],*z['call_indices']) for z in normal];assert len(terms)==8 and len({x[0] for x in terms})==8 and all(x[0].count('1')==2 for x in terms)
# Derive SC6 truth polynomial directly with Boolean event variables. Eight
# disjoint raw selectors have weight p^7; READY AND REPORT are joint event bits.
y1,y2,f,o,x1,x2,q=s.symbols('y1 y2 f o x1 x2 q');v=[y1,y2,f,o,x1,x2,q];expr=sum((v[i]*v[j] if sign==1 else 1-v[i]*v[j]) for _,sign,i,j in terms);factor=4+(y1-y2)*(f-o)+(x1-x2)*(q-o);assert s.expand(expr-factor)==0
# Exact current fixed-reference PF nuance: reference differences and P0 are
# SITE independent, so shared-site averaging happens to factor at this slice.
w=s.symbols('w0:3',nonnegative=True);Pf=s.symbols('f0:3');Pq=s.symbols('q0:3');dy,dx,P0=s.symbols('dy dx P0');
shared=sum(w[i]*(dy*(Pf[i]-P0)+dx*(Pq[i]-P0)) for i in range(3));separate=dy*(sum(w[i]*Pf[i] for i in range(3))-P0)+dx*(sum(w[i]*Pq[i] for i in range(3))-P0)
assert s.rem(s.Poly(s.expand(shared-separate),*w),s.Poly(sum(w)-1,*w)).as_expr()==0
# Strictly rational positivity improvement, conditional on exact ideal
# product law, E_READY=alpha I and subsequent actual corner eta bound.
pU=F(618034,10**6);assert (2*pU+1)**2>5;kU=F(93793197770933668,10**17);alphaU=F(74069,100000)
min_c=1-2*kU*pU**7*(4+2*alphaU**2);assert min_c>F(67,100) and F(67,100)-F(1,2**3231)>F(2,3)
# Check relevant predecessor certificates and their pinned owner code.
for index in (5,6,7,8,9,10,11,12,13):assert json.loads(files[index].read_text())['status'].startswith('PASS')
for j in (8,9):assert json.loads(files[j].read_text())['source_sha256']==h(D/'round16/source_select.py')
for path,pin in pins.items():assert h(Path(path))==pin
out={'status':'PASS_A27_IDEAL_PRODUCT_SOURCE_COMPRESSION_WITH_SCOPE','input_sha256':pins,'A27_all_source_slots_bijective':1372,'material_to_CAR_translation_explicit':True,'SC6_exact_symbolic_multilinear_identity':True,'actual_fixed_reference_PF_average_factorization':True,'PF_caveat':'For this fixed B25 reference, normalized y±/x±/0 reference inputs and ideal α are site-independent, so separate averages happen to equal the common-site expression; generic site-dependent reference or independent variations may have nonzero covariance and require the shared-site expression.','stronger_ideal_corner_lower_bound':'c_b > 67/100, conditional on the same ideal moment/product law and P_j in [0,alpha]','stronger_actual_corner_lower_bound':'c_hat_b > 67/100 - 2^-3231 > 2/3, conditional on B52 scalar structure and canonical-input error','scope':'Combines exact B54 leaf/polynomial/reference checks with B32/B33 tensor-copy induction and B34 A16 consumer; consumes B25 target regularity and A17 readiness. Physical original marked-map, births, clock, Cost-Info and GR remain unproved.','physical_C_closed':False,'GR_closed':False}
(P/'A27_PRODUCT_COMPRESSION_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'source_slots':len(actual),'ideal_corner_gt':'67/100','actual_corner_gt':'2/3'}))
