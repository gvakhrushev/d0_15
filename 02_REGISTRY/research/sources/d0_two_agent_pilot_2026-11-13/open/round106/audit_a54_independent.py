#!/usr/bin/env python3
"""Independent finite structural/count audit of frozen A54, not giant execution."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from math import comb
from pathlib import Path
from unittest.mock import patch
import json, sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round54'))
import regular_global_source as g
s=g.s; old=s.old; link=s.link

# Exact field ownership and layout over every actual scheduled source copy.
field=g.t.FieldCentre(tuple(F(j-1344,1<<48) for j in range(2688)))
src=g.GlobalSource(field)
assert src.field is src.sources.field is src.sources.components.field is field
plan=g.namespace(); slots=plan['source_slots']; stages=g.schedule()
scheduled=[x['slot'] for x in stages if x['kind']=='SOURCE']
assert sorted(scheduled)==list(range(1568))
slot_counts=Counter((x['kind'],x['bank']) for x in slots)
assert sum(n for (k,_),n in slot_counts.items() if k=='Choi')==1440
assert sum(n for (k,_),n in slot_counts.items() if k=='CAR')==128
assert sum(b['stop']-b['start'] for b in g.birth_blocks())==11893774624
sam=set(plan['layout']['SAM']);assert len(sam)==5376
occupied=set(sam)
for slot in slots:
    if slot['kind']=='Choi':
        bound=g.ns.choi_layout(plan,slot);targets=old.data(bound)+old.private(bound)
    else:
        bound=g.ns.car_layout(plan,slot)
        targets=bound['internal_SITE']+bound['grade']+bound['RIGHT']+[bound['predicate_flag'],*bound['predicate_work']]
    assert set(bound['SAM'])==sam and not occupied.intersection(targets)
    assert plan['old_compiler_helper'] not in targets
    occupied.update(targets)

class RoutingProbe:
    def __init__(self):self.seen=[]
    def choi_blocks(self,bank,lay,depth):
        assert set(lay['SAM'])==sam
        self.seen.append(('Choi',bank,depth));return iter(())
    def car_blocks(self,bank,lay,depth):
        assert set(lay['SAM'])==sam
        self.seen.append(('CAR',bank,depth));return iter(())
route=RoutingProbe(); route_source=g.GlobalSource(field);route_source.sources=route
for index,slot in enumerate(slots):
    for depth in (0,1,2):
        list(route_source.stage_blocks({'kind':'SOURCE','slot':index},depth))
        assert route.seen[-1]==(slot['kind'],slot['bank'],depth)
assert len(route.seen)==4704

# Recover the binomial depth distribution from the actual level-nine emitter
# by replacing each large child with a labelled leaf.  Counts follow from
# (2+x)^9 independently of native_budget's cost recurrence.
class Probe(s.Sources):
    def omega_blocks(self,bank,lay=None,depth=0):
        yield ('omega',depth)
toy=old.choi_layout(); probe=Probe(field)
fake={'H':'H','good':['G'],'start':['S'],'correction':'C'}
with patch.object(old.old.adapter,'fixed',lambda *a,**k:fake), \
     patch.object(s.local,'invert',lambda tree,depth,lay:('leaf',tree,depth)):
    depth_distributions=[]
    for initial in (0,1,2):
        rows=list(probe.half_blocks('f',toy,9,initial))
        got=Counter(x[1] for x in rows if x[0]=='omega')
        want=Counter({initial+j:comb(9,j)*2**(9-j) for j in range(10)})
        assert got==want and sum(got.values())==3**9
        depth_distributions.append(dict(sorted(got.items())))

# Catalogue and mapping: enumerate all 256 groups and all 4096 CODE words.
_,cat=old.link.fixed_and_catalogue(); groups=cat['f']['variable']
assert len(groups)==256
for bank,section in cat.items():
    fixed=[x['address'] for x in section['fixed']]
    variable=[x['address'] for x in section['variable']]
    assert len(fixed)==len(set(fixed)) and len(variable)==len(set(variable))
    assert not set(fixed)&set(variable) and (bank=='f' or not variable)
    assert 0 not in fixed and 0 not in variable
    cf={row['address'] for row in g.t.coframe_rows(bank)}
    assert 0 not in cf and cf.isdisjoint(fixed) and cf.isdisjoint(variable)
for group in groups:
    ids=group['indices_by_generator']; assert len(set(ids))==6
    assert field.selected(ids)==tuple(field.offsets[j] for j in ids)
    for digits in product(range(4),repeat=6):
        entry=link.variable_entry(group,digits)
        assert entry['SAM_indices']==ids+[2688+j for j in ids]
        assert entry['SAM_pattern']==[d%2 for d in digits]+[d//2 for d in digits]

# Splice dispatch: record the exact order and number of literal inverse
# applications without reusing either A54 checker or its fixture implementation.
fakecat={'f':{'fixed':[{'address':11},{'address':12}],'variable':[{}]}}
def fixed_provider(lay,entry,reverse=False):
    yield ('fixed',entry['address'],int(reverse))
def variable_provider(f,lay,reverse=False):
    assert f is field
    yield ('variable',0,int(reverse))
def add_inverse(tree,depth,lay):return (tree[0],tree[1],tree[2]+depth)
with patch.object(old.link,'fixed_and_catalogue',lambda:({},fakecat)), \
     patch.object(old.link,'sector_blocks',fixed_provider), \
     patch.object(link,'variable_bank_blocks',variable_provider), \
     patch.object(s.local,'invert',add_inverse):
    for depth in range(4):
        actual=list(src.sources.link_blocks('f',{'port':0,'spin':[1,2]},depth))
        order=[('fixed',11),('fixed',12),('variable',0)]
        if depth%2:order.reverse()
        assert actual==[(kind,label,depth) for kind,label in order]

# Exercise the real 496-plane emitter with an instrumented SELECT, retaining
# actual permutation gates.  Symbolic k does not assert target approximation.
bound=old.choi_layout(); entry=link.variable_entry(groups[0],(0,1,2,3,0,1))
angles=[{'i':i,'j':j,'k':1} for i,j in combinations(range(32),2)]
protected=set(bound['SAM']); seen=[]
def select(controls,pattern,target,k,lay,common_controls=29,reverse=False):
    assert len(controls)==len(pattern)<=29 and target not in controls
    assert target not in protected and len(set(controls))==len(controls)
    seen.append((tuple(controls),tuple(pattern),target,reverse))
    yield {'op':'SELECT_FIXTURE','wires':[target]}
with patch.object(link.native.old,'selective_terms',select):
    for reverse in (False,True):
        seen.clear()
        emitted=list(link.sector_blocks(bound,entry,angles,reverse))
        assert len(seen)==496
        assert all(x['op']=='SELECT_FIXTURE' or (x['op']=='CX' and x['wires'][1] not in protected) for x in emitted)

# Rebuild per-mask Walsh inventory from arithmetic, then bound each of 496
# permutations by 8 CX.  Use explicit inverse transform, not source helpers.
Q=link.native.Q
def inv(c):
    gp=c['G_port'];go=c['G_other']
    return Counter(G_port=gp+go,G_other=0,CX=c['CX']+6*go,SourceI=3*c['SourceI']+4*(gp+go))
def select_count(width,pattern,k):
    n=1<<width; neg=n//2 if any(pattern) else 0; pos=n-neg
    power=k*(1<<(29-width))
    return Counter(G_port=neg*power,G_other=pos*power,CX=width*n+6*neg,SourceI=4*neg)
for width in range(1,30):
    for pattern in ([0]*width,[1]+[0]*(width-1)):
        c=select_count(width,pattern,Q)
        assert c==link.native.old.select_cost(list(range(width)),pattern,Q,common_controls=29)
        assert +inv(c)==+link.native.old.select_cost(list(range(width)),pattern,Q,common_controls=29,reverse=True)
one=select_count(29,[1]+[0]*28,Q);one['CX']+=8
variable=Counter({k:v*256*4096*496 for k,v in one.items()})
assert variable==link.variable_bank_cost_upper(256)

# Independent per-bank source inventory reconstruction.  In particular,
# propagate full literal inverse costs through every adapter level and keep
# CAR vacuum plus both frame preparations, rather than only the target leaf.
def multiply(c,n):return Counter({k:v*n for k,v in c.items() if v*n})
def cost_tree(tree,port):
    op=tree['op']
    if op=='seq':
        z=Counter()
        for child in tree['children']:z.update(cost_tree(child,port))
        return z
    if op=='repeat':return multiply(cost_tree(tree['child'],port),int(tree['count']))
    if op=='G':return Counter({'G_port' if tree['wires'][0]==port else 'G_other':1})
    assert op in ('CX','SourceI'),op
    return Counter({op:1})
pair=select_count(17,[1]+[0]*16,Q)
levels=[pair,inv(pair),inv(inv(pair))]
pairmax=Counter({key:max(c[key] for c in levels) for key in ('G_port','G_other','CX','SourceI')});pairmax['CX']+=2
fixed=multiply(pairmax,96)+select_count(13,[1]+[0]*12,Q)+select_count(14,[1]+[0]*13,Q)+multiply(select_count(15,[1]+[0]*14,Q),4)
upper=s.inventory_upper();component=s.component.componentwise_upper(); x=old.inputs()
for bank,section in cat.items():
    expected_link=multiply(fixed,len(section['fixed']))+multiply(one,len(section['variable'])*4096*496)
    assert +expected_link==+upper['link'][bank]
    lay=old.choi_layout();omega=Counter(expected_link)
    for tree in old.old.prefix.prefix_blocks(x['prefix'],lay,True):omega.update(cost_tree(tree,lay['port']))
    omega.update(component['coframe'][bank]['forward'])
    assert +omega==+upper['Choi'][bank]['Omega_forward_upper']
    hk=int(x['h_k']);phase=int(x['phase']['phase_k']);correction=int(x['level9']['correction_l']);N=23
    X=Counter(G_other=4*hk,CX=6,SourceI=2)
    ccx=Counter(G_port=6*hk,G_other=6*hk,CX=68,SourceI=24)
    Fcount=multiply(X,2)+Counter(CX=2*N-1)+multiply(ccx,2*N-3)
    flag=Counter(G_port=phase,G_other=phase,CX=8,SourceI=4)
    start=Fcount+flag+inv(Fcount)
    good=Counter(G_other=2*phase,CX=2)
    H=Counter(G_other=2*hk,CX=6,SourceI=2)
    half=multiply(H,2)+omega
    for _ in range(9):half=multiply(half,2)+inv(half)+good+start
    half['G_other']+=correction
    assert +half==+upper['Choi'][bank]['half_forward_upper']
    refl=old.gray.counts(46,int(x['fixed']['joint_reflection_pi']['k']))
    choi=Counter(G_port=46,CX=276,SourceI=184)+multiply(refl,2)+half+inv(half)
    assert +choi==+upper['Choi'][bank]['source_forward_upper']
    carlay=old.car_layout();U,Ui,R=s.local.car.fixed_components(carlay)
    frame=cost_tree(U,carlay['port'])+cost_tree(Ui,carlay['port'])+multiply(cost_tree(R,carlay['port']),2)
    if bank in component['material']:
        frame.update(component['material'][bank]['forward']);frame.update(component['material'][bank]['literal_inverse'])
    else:frame.update(cost_tree(U,carlay['port']));frame.update(cost_tree(Ui,carlay['port']))
    assert +frame==+upper['CAR'][bank]['frame_forward_upper']
    car=Counter(G_port=3,CX=18,SourceI=12)+old.car_inventory(bank)['vacuum_prefix_forward']+frame
    assert +car==+upper['CAR'][bank]['source_forward_upper']

# Full global arithmetic independently aggregates actual slots, site,
# all eight reports, both resource frames, SC6 and replacement.  Source
# component maxima themselves are inherited A53/B103/B104 premises.
u=g.upper_inventory_and_error()
src_total=Counter(old.site.inventory(old.inputs()['site'])['SITE_forward'])
for slot in slots: src_total.update(upper[slot['kind']][slot['bank']]['source_forward_upper'])
assert src_total==upper['all_SOURCE_forward_componentwise_upper']
report=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
rp=old.counter(report['native_forward_resources']); r=len(g.previous.previous.resource_wires());assert r==34112
A=Counter(src_total)
for k,v in rp.items():A[k]+=8*v
A.update(G_port=8,CX=48,SourceI=32)
A.update(G_other=r,G_port=r,CX=6*r,SourceI=4*r)
A.update(G_port=5889,CX=4096,SourceI=8196)
W=A+inv(A)+Counter(SourceI=2)
assert A==u['A_profile_upper'] and W==u['W_profile_upper']
units=8*W['SourceI']; native=Counter(G=W['G_port']+W['G_other']+g.compiler().k*units,CX=W['CX']+W['SourceI'])
assert native==u['W_G_CX_upper']
replacement=F(units,1<<20000);assert replacement==u['replacement_error']<F(1,1<<15800)
delta=F(1,1<<3460);deltaold=F(1,1<<3456);eps=F(1,1<<4096)
pre=old.inputs()['prefix']; epre=F(int(pre['prefix_error_L1_numerator_hex'],16),1<<pre['precision_bits'])
L=3**9; half=F(1,1<<9841)+L*(epre+498*delta)+(2*L+23*(2*L-2)+1)*eps
source_error=1440*(4*half+2*deltaold)+128*(24*deltaold+43*eps)+18*deltaold
assert source_error==u['source_error']<F(1,1<<3423)
known=report['seven_report_all_known_approximate_macros'];assert known%7==0
compressed=2*(source_error+F(8*(known//7),1<<4096))+replacement
assert compressed==u['full_canonical_compressed_error']<F(1,1<<3421)
prefix_profile=src_total+Counter(G_port=8,CX=48,SourceI=32,G_other=r)
assert source_error+F(8*prefix_profile['SourceI'],1<<20000)==u['full_SOURCE_DATA_fibre_prefix_error']<F(1,1<<3423)

files=[D/'round54'/n for n in ('regular_source_native.py','regular_global_source.py','check_regular_global_source.py','REGULAR_GLOBAL_SOURCE_PLAN.json','REGULAR_GLOBAL_SOURCE_CHECK.json','REGULAR_GLOBAL_SOURCE_RU.md')]
for receipt in (files[3],files[4]):
    for path,digest in json.loads(receipt.read_text())['source_sha256'].items():
        assert sha256(Path(path).read_bytes()).hexdigest()==digest
files += [P.parent/'round103/regular_link_julia.py',P.parent/'round103/B103_REGULAR_PROPER_LINK_CONSTRUCTOR_RU.md',
          P.parent/'round104/B104_A53_AUDIT_CHECK.json',P.parent/'round104/B104_A53_REGULAR_COMPONENT_AUDIT_RU.md',
          P.parent/'round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md',D/'round23/CAR_VACUUM_FOURIER_RU.md']
out={'status':'PASS_A54_INTEGRATION_CONDITIONAL_ON_PINNED_COMPONENTS_AND_SELECTED_A23_EXTENSION',
     'all_scheduled_source_slots':len(slots),'all_variable_group_code_assignments':len(groups)*4096,
     'adapter_level9_leaf_count_per_depth':3**9,'adapter_depth_counts':depth_distributions,
     'all_496_plane_geometries_both_orders':True,'walsh_width_classes_checked':29,
     'global_inventory_and_error_recomputed':True,'selected_A23_extension_not_universal_owner_identity':True,
     'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files+[Path(__file__)]}}
(P/'B106_A54_AUDIT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('input_sha256','adapter_depth_counts')},indent=2))
