#!/usr/bin/env python3
"""Replay high-precision grid and audit actual A42 CODE-only plane grammar."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
from itertools import combinations
import json,math,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(P));import certify_grid_32768 as certifier
import plane_grid_32768 as grid
sys.path.insert(0,str(D/'round49'));import paid_padding as pad
old=pad.old;native=pad.native;e=old.a41.e

# Rebuild the entire dyadic theta/pi enclosure and integer CF certificate.
saved=(P/'GRID_32768_CERTIFICATE.json').read_bytes()
rebuilt=(json.dumps(certifier.build(),indent=2)+'\n').encode()
assert rebuilt==saved
pn,q,cert=grid.uniform_grid();assert q.bit_length()==32773
assert 16*(1<<32768)<q and cert['proof_uses_floating_point'] is False
macro=grid.Macros();k8=macro.ks['pi8'];assert 1<=k8<=q

# Actual macro methods and exact compact inventory, without expansion of k8.
for a,b in ((0,1),(7,11),(4000,10000)):
    tree=macro.x(a,b);assert native.counts(tree)==Counter(G=20*k8,CX=2)
    def audit_tree(t):
        op=t['op']
        if op=='seq':
            for v in t['children']:audit_tree(v)
        elif op=='repeat':audit_tree(t['child'])
        else:assert op in ('G','CX') and set(t['wires'])<={a,b}
    audit_tree(tree)

# Endpoint inputs are interval-certified at full scale. Independent integer
# inequalities confirm the selected rational cell is within 3/(4q) of every
# target angle in the outward interval; B80 orbit contributes <1/q more.
selections={}
for sign in (-1,1):
    s=grid._select(sign,5376,6000);S=1<<s['precision_bits'];j=s['cell'];k=s['k']
    assert k==grid.plane_power(sign,5376,6000) and 1<=k<=q
    assert (k*pn-j)%q==0 and 2*q*(s['interval_high']-s['interval_low'])<=S
    assert 4*abs(q*s['interval_low']-j*S)<=3*S
    assert 4*abs(q*s['interval_high']-j*S)<=3*S
    selections[str(sign)]={'exponent_hex':hex(k),'cell_hex':hex(j),
                           'series_terms':s['series_terms']}
assert grid.plane_power(1)+grid.plane_power(-1)==q
for args in ((0,5376,6000),(1,2,6000),(1,5377,6000),(1,5376,0)):
    try:grid.plane_power(*args)
    except ValueError:pass
    else:raise AssertionError('invalid endpoint input accepted')

# Exact count of the existing A42 grammar, independently over all small
# pairs. Its support is SAM only and no borrowed WORK/helper is introduced.
class FixtureMacros:
    power=native.Macros.power;pi8=native.Macros.pi8;z=native.Macros.z;x=native.Macros.x
    def __init__(self):self.ks={'pi8':1}
fixture=FixtureMacros();cases=columns=0
theta=math.pi/8;cc=math.cos(theta);ss=math.sin(theta)
for m in (3,4):
    for a,b in combinations(range(1<<m),2):
        trees=list(old.plane_blocks(a,b,1,tuple(range(m)),fixture))
        counts=Counter()
        for tree in trees:counts.update(native.counts(tree))
        assert counts==old.plane_counts(m,a,b,1,1)
        assert all(set(op['wires'])<=set(range(m)) for tree in trees for op in e.leaves(tree))
        L=1<<(m-1);c=math.cos(L*theta);s=math.sin(L*theta)
        for col in range(1<<m):
            v=[float(j==col) for j in range(1<<m)]
            for tree in trees:
                for op in e.leaves(tree):
                    wires=op['wires'];bit=1<<wires[-1]
                    for x in range(1<<m):
                        if x&bit:continue
                        y=x|bit
                        if op['op']=='G':v[x],v[y]=cc*v[x]-ss*v[y],ss*v[x]+cc*v[y]
                        elif (x>>wires[0])&1:v[x],v[y]=v[y],v[x]
            target=[float(j==col) for j in range(1<<m)]
            if col==a:target[a],target[b]=c,s
            if col==b:target[a],target[b]=-s,c
            assert max(abs(x-y) for x,y in zip(v,target))<1e-12
            columns+=1
        cases+=1
assert cases==148 and columns==2144

# Exact upper for actual 5376 CODE wires, both signs and ANY plane a<b.
m=5376;L=1<<(m-1);upper=old.plane_upper(m,q,k8)
assert upper==Counter(G=L*q+40*m*k8,CX=(m-1)*L+2*(m-1)+4*m)
assert old.plane_counts(m,0,(1<<m)-1,q,k8)['G']<=upper['G']
assert old.plane_counts(m,(1<<m)-2,(1<<m)-1,q,k8)['CX']<=upper['CX']
mu=F(L+40*m,1<<32768);assert mu<F(1,1<<27392)
paths=[Path(__file__),P/'certify_grid_32768.py',P/'plane_grid_32768.py',P/'GRID_32768_CERTIFICATE.json',
       O/'round80/certify_uniform_golden_grid.py',D/'round49/paid_padding.py',
       D/'round42/fixed_post_paid_family.py',D/'round41/sam_only_compiler.py',
       D/'round38/gcx_post_macros.py',O/'round111/B111_A56_INDEPENDENT_REVIEW_RU.md']
plan={'status':'PASS_32768_GRID_AND_PAID_CODE_ONLY_PLANE_PRECISION',
      'public_module':'plane_grid_32768.py',
      'public_api':['uniform_grid()->(pn,q,certificate)','Macros().ks[pi8]','Macros().x(q,helper)',
                    'plane_power(sign,m=5376,step_bits=6000)->positive integer'],
      'uniform_power_upper_q_hex':hex(q),'uniform_power_upper_q_bits':q.bit_length(),
      'pi8_power_hex':hex(k8),'pi8_power_bits':k8.bit_length(),
      'positive_negative_plane_endpoint_powers':selections,
      'small_plane_words_checked':cases,'all_small_columns_checked':columns,
      'small_fixture_is_numeric_diagnostic_not_global_proof':True,
      'exact_uniform_plane_counts_upper':{k:hex(v) for k,v in upper.items()},
      'G_upper_bit_length':upper['G'].bit_length(),'CX_upper_bit_length':upper['CX'].bit_length(),
      'all_column_error':'(2^5375+40*5376)*2^-32768 < 2^-27392',
      'new_full_clock_or_family_constructed':False,'physical_C_closed':False,'GR_closed':False,
      'input_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths}}
(P/'B112_PLANE_PRECISION_CHECK.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps({k:v for k,v in plan.items() if k not in ('input_sha256','uniform_power_upper_q_hex','pi8_power_hex','positive_negative_plane_endpoint_powers','exact_uniform_plane_counts_upper')},indent=2))
