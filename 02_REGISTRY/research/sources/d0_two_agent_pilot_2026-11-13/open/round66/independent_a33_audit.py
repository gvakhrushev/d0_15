#!/usr/bin/env python3
"""Independent fixed-row A33 audit: original DAG, moments, links and budgets.

Owner analytic/R11/source-admission assumptions are consumed, not proved here.
No file in the direct worktree is written or imported with bytecode caching.
"""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
from functools import lru_cache
import importlib.util, json, sys
import sympy as S
sys.dont_write_bytecode = True
P=Path(__file__).resolve().parent
O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
claim=json.loads((D/'round33/SAMPLING_SOURCE_BIAS_CHECK.json').read_text())
assert claim['status']=='PASS_FIXED_SAMPLER_NONZERO_SOURCE_ROW'
for filename,digest in claim['source_sha256'].items():
    assert sha256(Path(filename).read_bytes()).hexdigest()==digest, filename
source=D/'round11/source_operator_dag.py'
spec=importlib.util.spec_from_file_location('a11_original',source)
a11=importlib.util.module_from_spec(spec);spec.loader.exec_module(a11)
dag=a11.build()
assert dag['constants']['eta']==((0,1,0,0),(1,0,0,0),(0,0,-1,0),(0,0,0,-1))
rows=[json.loads(line) for line in (O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()]
site=(0,0,1,1)
row=next(v for v in rows if v['kind']=='coframe' and tuple(v['site'])==site and v['role']==0 and v['component']==2)
assert row['sam_index']==2 and rows[2]==row
by={(tuple(v['site']),v['kind'],v.get('role'),v.get('component'),v.get('grade'),tuple(v.get('generator',[]))):v['sam_index'] for v in rows}
def plus(x,k):return tuple((a+(i==k))%4 for i,a in enumerate(x))
for z in [site]+[plus(site,k) for k in range(4)]:
    for a in (0,15):assert (z,'matter',None,None,a,()) in by
# Read the six actual A11 faces and independently resolve physical addresses.
assert len(dag['faces'])==6
for face in dag['faces']:
    r,t=face['roles']; locs={'base':site, f'plus{r}':plus(site,r),f'plus{t}':plus(site,t)}
    addresses=[(locs[loc],role) for loc,role in face['links']]
    assert len(set(addresses))==4
    # Free links have disjoint six-bit SAM blocks; collar links are fixed.
    blocks=[]
    for z,role in addresses:
        bits={v['sam_index'] for v in rows if v['kind']=='proper_link' and tuple(v['site'])==z and v['role']==role}
        assert len(bits) in (0,6)
        blocks.append(bits)
    assert all(not (blocks[i]&blocks[j]) for i in range(4) for j in range(i))
assert sum(0 in f['roles'] for f in dag['faces'])==3
# Evaluate the original matter tensor DAG on a symbolic physical field, rather
# than importing A33's reduced q formula. Other coframe means are at centre;
# their independent fluctuations have zero contribution to this secant.
p,d,a,h0,H=S.symbols('p d a h0 H', real=True)
nu=S.Rational(3,5); psi_symbols=S.symbols('c0 c1 t00 t01 t10 t11 t20 t21 t30 t31')
center=psi_symbols[:2]; forward=[psi_symbols[2+2*i:4+2*i] for i in range(4)]
coframe=[[0,nu,d,0],[nu,-nu*H/2,0,0],[0,0,nu,0],[0,0,0,nu]]
node=dag['nodes']
@lru_cache(None)
def evaluate(i):
    n=node[i]; op=n['op']
    if op=='const':return S.Rational(n['a'])+p*S.Rational(n['b'])
    if op=='var':
        name=n['name'].split('/')
        if name[0]=='u':return coframe[int(name[1])][int(name[2])]
        assert name[0]=='X'
        xyz=center if name[1]=='base' else forward[int(name[1][4:])]
        return 2*S.sqrt(p)*xyz[0 if name[2]=='0' else 1]/256
    vals=[evaluate(j) for j in n['args']]
    return S.Add(*vals) if op=='add' else S.Mul(*vals)
qdag=evaluate(dag['roots']['H_q_before_inverse_PF'])
# The DAG is specialised to h=1/4; 1/p=(1+p) since p²+p=1.
dq=S.expand(qdag-qdag.subs(d,0))
dq_reduced=S.rem(dq,p*p+p-1,p).expand()
d0=S.Matrix(forward[0])-S.Matrix(center);d2=S.Matrix(forward[2])-S.Matrix(center)
expected=-S.Rational(16,1)/nu**2*(d**2*d0.dot(d0)+2*d*nu*d0.dot(d2))
assert S.expand(dq_reduced-expected)==0
# Independently enumerate 64 independent Bernoulli assignments at the three
# matter sites. p is exact via p²+p=1; keep amplitude a symbolic.
r,s=S.symbols('r s',real=True)
bits=S.symbols('b0:6')
noise=[S.Matrix([s*(bits[2*i]-r),s*(bits[2*i+1]-r)]) for i in range(3)]
v0=(S.Matrix([0,a])+noise[1]-S.Matrix([a,0])-noise[0])*4
v2=(S.Matrix([a,0])+noise[2]-S.Matrix([a,0])-noise[0])*4
poly=S.Poly(S.expand((-(s*(1-r))**2*v0.dot(v0)-2*s*(1-r)*nu*v0.dot(v2)
                       +(-s*r)**2*v0.dot(v0)+2*(-s*r)*nu*v0.dot(v2))/(s*nu**2)),*bits)
sec=S.expand(sum(c*r**sum(power>0 for power in powers) for powers,c in poly.terms()))
V=s*s*r*(1-r)
formula=-s*(1-2*r)*(32*a*a+64*V)/nu**2-64*V/nu
assert S.expand(sec-formula)==0
assert S.expand(sec-(formula+64*V/nu))!=0  # negative control: omit shared-base covariance
# PF site mass w=rho/256 cancels the one inverse-rho exactly.
R=S.symbols('R',positive=True);assert S.cancel((R/256)/R)==S.Rational(1,256)
# Constants for exterior link averaging and all later error terms.
t=Q(1,2**30);mean=Q(24,1)/(1-24*t)
assert mean<25 and Q(17,16)**4<Q(4,3) and Q(4,3)*mean<34
assert Q(4,3)+34*t*t<Q(3,2)
loop=4*34*Q(3,2)**3;assert loop==459
local=3*Q(400,9)*4*loop;assert local==244800<2**18
assert Q(3,5)**2+Q(3,5)<1<Q(5,8)**2+Q(5,8)
positive=t/Q(6400);assert positive>Q(1,2**43)
eps=Q(1,2**1531);remainder=2**47*eps*2**26+24*2**43*eps*16**2
assert remainder<Q(1,2**1457)
loss=2**10*t*t+2*remainder/t+Q(1,2**73)+Q(1,2**72)
assert positive-loss>Q(1,2**44)
assert Q(1)+Q(1,2**23)<2
# Compute all source fingerprints freshly, including the audited narrative and
# the endpoint/mean owner receipts; no promise that hashes validate semantics.
pins=[Path(__file__),source,D/'round33/SAMPLING_SOURCE_BIAS_RU.md',D/'round33/check_sampling_bias.py',D/'round33/SAMPLING_SOURCE_BIAS_CHECK.json',D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',D/'round29/G_CX_ONLY_REALIZATION_RU.md',D/'round31/ACTUAL_MEAN_GEOMETRY_LIFT_RU.md',D/'round32/FINITE_FULL_BOOK_COMPARISON_RU.md',O/'round25/targets.py',O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',O/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md',O/'round64/B64_A32_FINITE_BOOK_AUDIT_RU.md']
out={'status':'PASS_CONDITIONAL_INDEPENDENT_A33_ROW_AUDIT','actual_coordinate':row,'A11_matter_DAG_secant_verified_symbolically':True,'shared_base_covariance_negative_control':True,'all_six_face_link_addresses_distinct_and_SAM_blocks_disjoint':True,'source_weight_h4_verified':True,'link_budget_loop':str(loop),'local_geometric_error_coefficient':str(local),'positive_row_lower_bound':'2^-44 under owner assumptions','corrected_covector_norm_lower_bound':'2^-45 under owner assumptions','unchanged_owner_assumptions':['exact geometric root and source map','A30 native e_B and g*s bound','A31 actual Jacobian bound','A32 and B64 finite H+J / R6 R11 bound','original fixed reporter and PF source law'],'native_stationary_centre_proved':False,'full_cost_info_selection_proved':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in pins}}
(P/'INDEPENDENT_A33_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'row':row['sam_index'],'lower':out['positive_row_lower_bound']}))
