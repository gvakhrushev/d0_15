#!/usr/bin/env python3
"""Independent structural and exact-rational audit of A34; no new root search."""
from pathlib import Path
from itertools import product
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json, importlib.util, sys
import sympy as S
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
receipt=json.loads((D/'round34/FULL_SAMPLING_SOURCE_BOUND.json').read_text())
assert receipt['status']=='PASS_STRUCTURED_FULL_SAMPLING_SOURCE_UPPER_BOUND'
for file,digest in receipt['source_sha256'].items():
    assert sha256(Path(file).read_bytes()).hexdigest()==digest, file
source=D/'round11/source_operator_dag.py'
spec=importlib.util.spec_from_file_location('owner_a11',source)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);dag=m.build()
assert len(dag['faces'])==6
read=lambda f:[json.loads(v) for v in f.read_text().splitlines()]
coords=read(O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl')
assert Counter(c['kind'] for c in coords)=={'coframe':1024,'proper_link':1536,'matter':128}
free_sites={tuple(c['site']) for c in coords if c['kind']=='matter'}
assert len(free_sites)==64
sites=list(product(range(4),repeat=4))
def shift(z,k,step=1):return tuple((v+(step if i==k else 0))%4 for i,v in enumerate(z))
# Rebuild the 1536 ordered faces independently from A11's roles and L4 shifts.
addressrows=read(O/'round24/TORUS_CHOI_ADDRESSES.jsonl')
address={(tuple(q['site']),q['direction']):q['a'] for q in addressrows if q.get('kind')=='proper_link'}
stencils={tuple(q['site']):q for q in read(O/'round24/SITE_DEPENDENCIES.jsonl')}
link_counts=Counter();matter_counts=Counter();coframe_counts=Counter();max_cov=0
for z in sites:
    q=stencils[z]; matter=[z]+[shift(z,i) for i in range(4)]
    assert len(set(matter))==5 and [tuple(v) for v in q['matter_forward_torus']]==matter[1:]
    matter_counts.update(matter)
    # Incidence covariance of two components of the 4 differences. Each
    # free field bit has variance V, each fixed collar field has zero variance.
    coeff=[{w:((1 if w==shift(z,i) else 0)-(1 if w==z else 0)) for w in set(matter)&free_sites} for i in range(4)]
    for i in range(4):
        for j in range(4):
            val=sum(coeff[i][w]*coeff[j][w] for w in coeff[i])
            assert abs(2*val)<=4  # two independent matter components, in V/h² units
            max_cov=max(max_cov,abs(2*val))
    for face in dag['faces']:
        r,t=face['roles'];loc={'base':z,'plus'+str(r):shift(z,r),'plus'+str(t):shift(z,t)}
        pairs=[(loc[name],role) for name,role in face['links']]
        assert len(set(pairs))==4
        actual=next(f for f in q['faces'] if f['r']==r and f['s']==t)
        assert [address[v] for v in pairs]==actual['torus_addresses']
        link_counts.update(pairs);coframe_counts.update([(z,r),(z,t)])
assert len(link_counts)==1024 and set(link_counts.values())=={6}
assert len(coframe_counts)==1024 and set(coframe_counts.values())=={3}
assert set(matter_counts.values())=={5} and max_cov==4
for c in coords:
    if c['kind']=='proper_link':assert link_counts[(tuple(c['site']),c['role'])]==6
    if c['kind']=='matter':assert matter_counts[tuple(c['site'])]==5
# Prove the exact coframe covariance identity for generic U and the actual ETA,
# not just the eta trace: 16 distinct independent Bernoulli bits.
r,s=S.symbols('r s',real=True)
eta=S.Matrix(m.ETA);U=S.Matrix(4,4,S.symbols('u0:16'));bs=S.symbols('b0:16')
noise=S.Matrix(4,4,lambda i,j:s*(bs[4*i+j]-r))
def bern(expr):
    pp=S.Poly(S.expand(expr),*bs)
    return S.expand(sum(c*r**sum(k>0 for k in powers) for powers,c in pp.terms()))
delta=(U+noise).T*eta*(U+noise)-U.T*eta*U
average=delta.applyfunc(bern)
assert (average-s*s*r*(1-r)*S.trace(eta)*S.eye(4)).applyfunc(S.expand)==S.zeros(4)
assert S.trace(eta)==-2
# Noncommutative second-order own-coordinate link secant: cross terms remain
# in their correct order; only their expectation vanishes.
K,B=S.symbols('K B',commutative=False)
A1=B+s*(1-r)*K;A0=B-s*r*K
assert S.expand((A1**2-A0**2)/s-(B*K+K*B+s*(1-2*r)*K**2))==0
# Third-order remainder from two actual endpoint tails; inverse same bound.
t=F(1,2**30);nu=F(3,5);h=F(1,4);V=t*t/4
assert F(3,5)**2+F(3,5)<1<F(5,8)**2+F(5,8)
gold=S.symbols('gold',real=True)
assert S.rem(gold**3-(2*gold-1),gold**2+gold-1,gold)==0
assert F(2*24**3,6)==4608
own=F(4,3)*(2*t+F(4608,1)*t*t/(1-24*t));assert own<3*t
assert F(16,3)+own<6
other=F(4,3)*F(24,1)/(1-24*t);assert other<34
loop=own*F(3,2)**3+3*other*t*t*6*F(3,2)**2
assert loop<11*t
linkrow=6*h**4*F(1600,9)*loop;assert linkrow<46*t
# q coframe: own Bernoulli quadratic + metric/matter covariance.
qco=t/(4*nu**2)+32*V/(nu**2*h**2)
assert qco<t
fco=F(244800,256)*t*t
assert fco<2**10*t*t and fco+24*h**4*qco<t
# q matter: actual vector of difference signs has norm <=sqrt(4/h²)=8;
# full metric perturbation -2V I/nu² and its central norm are bounded.
dg=2*V/nu**2;assert dg<2*t*t
qmat=2*8*dg+(t/4)*13*64
assert F(4,1)/nu**2+dg<13 and qmat<209*t
assert 24*5*h**4*qmat<98*t
square=1024+1536*46**2+128*98**2
assert square==4480512<2**24
# Reference, reporter, and native/finite row-to-vector + Jacobian normalization.
assert 2**18+F(1,2**18)<2**19 # ||T_s sum h4 f|| bound
ref=F(1,2**3084)*2**19;reporter=55*F(1,2**1426)
assert ref==F(1,2**3065) and reporter<F(1,2**1420)
inv=1/(1-F(1,2**23));err=2*F(1,2**67)
C=inv*(F(1,2**18)+ref+reporter)+err
assert C<F(1,2**17) and C+F(1,2**24)<F(1,2**16)
pins=[Path(__file__),source,D/'round34/FULL_STRUCTURED_SOURCE_BOUND_RU.md',D/'round34/check_full_sampling_bound.py',D/'round34/FULL_SAMPLING_SOURCE_BOUND.json',D/'round31/RESULT.json',D/'round32/RESULT.json',D/'round33/SAMPLING_SOURCE_BIAS_CHECK.json',O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',O/'round24/TORUS_CHOI_ADDRESSES.jsonl',O/'round24/SITE_DEPENDENCIES.jsonl',O/'round24/check_current_frame.py',O/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md',O/'round65/SCALAR_HESSIAN_ENVELOPE.json',O/'round66/INDEPENDENT_A33_AUDIT.json']
out={'status':'PASS_CONDITIONAL_INDEPENDENT_A34_STRUCTURAL_AUDIT','source_faces_rebuilt':1536,'each_physical_link_six_faces':True,'each_coframe_role_three_faces':True,'each_matter_site_five_stencils':True,'matter_covariance_entry_max_units_V_over_h2':max_cov,'generic_coframe_mean_metric_shift_exact':'-2 V I / nu^2','own_link_numerator_quadratic_noncommuting_identity_checked':True,'actual_exponential_tail_two_endpoints_constant':4608,'full_L2_squared_row_coefficient':square,'corrected_finite_price_covector_norm_lt':'2^-17 conditional','difference_from_decoded_geometric_source_norm_lt':'2^-16 conditional','source_scope':'fixed raw L4 chart; inherited B24/B65 source-root, A27/A30 native, A31 Jacobian and A32/B64 R6/R11 finite-price assumptions','B65_inverse_transpose_erratum':'u_raw=nu eta (e^-1)^T; not nu eta exp(-T)','native_stationarity_proved':False,'full_Cost_Info_selection_proved':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in pins}}
(P/'INDEPENDENT_A34_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'faces':out['source_faces_rebuilt'],'C_lt':out['corrected_finite_price_covector_norm_lt']}))
