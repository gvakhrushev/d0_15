#!/usr/bin/env python3
"""Independent all-column diagnostics plus exact guards and native witnesses."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import islice
from collections import Counter
from fractions import Fraction
import importlib.util,json,sys
import numpy as np
from scipy.linalg import expm
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
import regular_link_julia as r
sys.path.insert(0,str(P.parent/'round93'))
import exact_resource_inventory as inv
B=P.parent
spec=importlib.util.spec_from_file_location('b103_original_b25',B/'round25/targets.py')
b25=importlib.util.module_from_spec(spec);sys.modules[spec.name]=b25;spec.loader.exec_module(b25)

zero=(F(0),)*6
near=(F(1,2**33),F(-1,2**33),F(1,2**34),F(0),F(-1,2**36),F(1,2**37))
digits=(0,1,2,3,1,0)
cases=[('exact_identity_zero_boost',zero,None,None),
       ('two_bit_zero_centre',zero,digits,None),
       ('shifted_site_xy',near,digits,(1,2)),
       ('shifted_exact_centre',near,None,(2,1))]

def Mmid(iv,J):return np.array([[float((int(a)+int(b))/(2*int(iv.S))) for a,b in row] for row in J])
def matrix_from_angles(data):
    S=1<<data['bits'];A=np.eye(32)
    for rec in data['angle_intervals']:
        c=float((rec['cos'][0]+rec['cos'][1])/(2*S));s=float((rec['sin'][0]+rec['sin'][1])/(2*S))
        i,j=rec['i'],rec['j'];ai=A[i,:].copy();aj=A[j,:].copy()
        A[i,:]=c*ai-s*aj;A[j,:]=s*ai+c*aj
    return A

def expected_b25(offsets,ds,xy):
    theta=np.zeros((4,4));p=b25.PVAL
    for n,gen in enumerate(r.GEN):
        q=float(offsets[n])+(0 if ds is None else 2**-80*(ds[n]-3*p*p))
        theta+=q*b25.GENERATORS[gen]
    baseline=np.eye(4) if xy is None else b25.current()[1][b25.INDEX[(0,0,*xy)],0]
    U=expm(theta)@baseline
    return b25.julia(b25.exterior(U)/2)

reports=[]
for name,offsets,ds,xy in cases:
    iv,J,meta=r.target_intervals(offsets,ds,xy,224,80)
    data=r.target_rotations(offsets,ds,xy,target_bits=80)
    direct=Mmid(iv,J);replay=matrix_from_angles(data);original=expected_b25(offsets,ds,xy)
    t_err=float(np.max(np.abs(direct-original)));q_err=float(np.max(np.abs(replay-direct)))
    assert t_err<2e-12,(name,t_err)
    assert q_err<2e-12,(name,q_err)
    assert data['rotation_count']==496
    reports.append({'case':name,'all_32_column_B25_float_diagnostic_max':t_err,
                    'all_32_column_rotation_float_diagnostic_max':q_err,
                    'target_bits':80,'bits':data['bits'],'sqrt_iterations':meta['sqrt_iterations']})

# Exact SO(32) fixtures exercise ties and exact zero without h>0 or a
# largest-pivot decision. The 4x4 rational Hadamard has determinant +1.
iv=r.t.Interval(176);I=iv.eye(32);r.interval_qr(iv,I,40)
h=((1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1))
A=iv.eye(32)
for i in range(4):
    for j in range(4):A[i][j]=iv.R(h[i][j],2)
angs,res=r.interval_qr(iv,A,40);assert len(angs)==496
assert r.sqrt_iterations(3460)==16

# Strict chart: |offset| + 3 sigma < (3/8)*2^-30 < both old cube sides.
assert F(1,2**32)+F(3,2**80)<F(3,8*2**30)
assert 5<F(9,4)**2  # sqrt(5)<9/4 -> p²>3/8; sqrt(5)>2 -> 1-p²>1/2
for bad in [(F(1,2**32),)*6,(-F(1,2**32),)*6]:
    try:r.validate(bad,digits,None)
    except ValueError:pass
    else:raise AssertionError('boundary accepted')
try:r.validate((0,)*6,digits,None)
except TypeError:pass
else:raise AssertionError('non-Fraction accepted')

# Full requested accuracy at one arbitrary nonzero offset and zero-boost
# baseline, including every selected finite G exponent.
data,angles=r.native_rotations(near,digits,(1,2),target_bits=3460)
assert data['rotation_count']==len(angles)==496 and all(1<=z['k']<=r.native.Q for z in angles)
assert data['input']['digits']==list(digits) and data['input']['xy']==[1,2]
assert data['input']['offsets_fraction']==[[str(q.numerator),str(q.denominator)] for q in near]
assert len(data['angle_powers_sha256'])==64
assert 498 < 1<<9 # matrix target 2 units plus 496 grid units: <2^-3451
# Independently replay representative exact native G powers on a larger
# complex-ball precision. This is a sample; the global guarantee uses B93.
bits=7168;iv=r.t.Interval(bits);S=iv.S
def mul(x,y):
    a,b,e=x;c,d,f=y
    return ((a*c-b*d)>>bits,(a*d+b*c)>>bits,e+f+((e*f+S-1)>>bits)+2)
a,b=iv.c['sqrtp'],iv.c['p'];powers=[(a[0],b[0],a[1]-a[0]+b[1]-b[0])]
for _ in range(r.native.Q.bit_length()+30):powers.append(mul(powers[-1],powers[-1]))
def power(k):
    acc=(S,0,0);v=k<<29;j=0
    while v:
        if v&1:acc=mul(acc,powers[j])
        v//=2;j+=1
    c,s,e=acc;return (c-e,c+e),(s-e,s+e)
scale=1<<(bits-data['bits']);checked=0
for j in range(496):
    rec=data['angle_intervals'][j];item=angles[j]
    assert (rec['i'],rec['j'])==(item['i'],item['j'])
    C,T=rec['cos'],rec['sin'];diff=rec['i']^rec['j'];pivot=(diff&-diff).bit_length()-1
    if (rec['i']>>pivot)&1:T=(-T[1],-T[0])
    C=tuple(int(v)*scale for v in C);T=tuple(int(v)*scale for v in T)
    ac,at=power(item['k'])
    err=max(abs(ac[0]-C[1]),abs(ac[1]-C[0]))+max(abs(at[0]-T[1]),abs(at[1]-T[0]))
    assert err<S>>3456,(j,'power error')
    checked+=1

# Independent higher-precision repeat contains all 1024 original target
# entry intervals. This is replay of the same analytic formulas, not a
# second independently derived physical chart.
ivlo,Jlo,_=r.target_intervals(near,digits,(1,2),3588,3460)
ivhi,Jhi,_=r.target_intervals(near,digits,(1,2),3844,3460)
scale2=1<<256
assert all(a[0]*scale2<=b[0] and b[1]<=a[1]*scale2
           for x,y in zip(Jlo,Jhi) for a,b in zip(x,y))

# Pair permutation on every 5-bit pair, all other basis inputs, and signs.
for a in range(32):
    for b in range(a+1,32):
        diff=a^b;pivot=(diff&-diff).bit_length()-1
        flips=[j for j in range(5) if j!=pivot and (diff>>j)&1]
        def f(z):
            for j in flips:
                if (z>>pivot)&1:z^=1<<j
            return z
        aa,bb=f(a),f(b);assert aa^bb==1<<pivot
        assert all(f(f(z))==z for z in range(32))
        other=[j for j in range(5) if j!=pivot]
        assert [z for z in range(32) if all(((f(z)>>j)&1)==((aa>>j)&1) for j in other)]==[a,b]
        # Signed target rotation after actual pre/post CX permutation.
        c,s0=F(3,5),F(4,5)
        physical_s=-s0 if (a>>pivot)&1 else s0
        for z in range(32):
            zz=f(z)
            if z not in (a,b):
                got={f(zz):F(1)};want={z:F(1)}
            else:
                flip=zz^(1<<pivot)
                val=physical_s if not (zz>>pivot)&1 else -physical_s
                got={f(zz):c,f(flip):val}
                want={a:c,b:s0} if z==a else {a:-s0,b:c}
            assert got==want

# Check actual B93 binding and lazy forward/reverse prefixes; exact compressed
# inverse cost is derived without expanding 2^29 Walsh masks.
_,cat=r.t.catalogue();group=cat['f']['variable'][0];entry=r.variable_entry(group,digits);layout=inv.layout()
assert len(entry['SAM_indices'])==12
assert len(cat['f']['variable'])==256
patterns=set()
from itertools import product
for ds in product(range(4),repeat=6):
    e=r.variable_entry(group,ds)
    assert e['SAM_indices']==group['indices_by_generator']+[2688+j for j in group['indices_by_generator']]
    patterns.add(tuple(e['SAM_pattern']))
assert len(patterns)==4096
class FieldFixture:
    def __init__(self):self.values=tuple(F((i%7)-3,2**36) for i in range(2688))
    def selected(self,ids):return tuple(self.values[i] for i in ids)
fixture=FieldFixture()
ahead=list(islice(r.variable_bank_entries(fixture),8))
backward=list(islice(r.variable_bank_entries(fixture,True),256*4096-8,256*4096))
assert ahead==list(reversed(backward))
assert all(x['offsets']==fixture.selected(x['entry']['SAM_indices'][:6]) for x in ahead)
forward=list(islice(r.sector_blocks(layout,entry,angles),8))
back=list(islice(r.sector_blocks(layout,entry,angles,True),8))
assert len(forward)==len(back)==8
cost=r.sector_cost(layout,entry,angles);inv_cost=r.sector_cost(layout,entry,angles,True)
assert +inv_cost==+r.native.old.invert_cost(cost)
upper0=r.variable_bank_cost_upper(1,False);upper1=r.variable_bank_cost_upper(1,True)
assert all(v<=upper0[k] for k,v in cost.items())
assert all(v<=upper1[k] for k,v in inv_cost.items())
assert +upper1==+r.native.old.invert_cost(upper0)
upper256=r.variable_bank_cost_upper(256,True)

def support(tree):
    if tree['op']=='seq':return set().union(*(support(x) for x in tree['children']))
    if tree['op']=='repeat':return support(tree['child'])
    return set(tree['wires'])
assert all(support(z).isdisjoint({layout['oldRIGHT_witness'],layout['phase_rebit'],*layout['comparator_scratch']}) for z in (forward+back))

# Conditional recomposition with the A48 source recurrence: only the link
# component changes; coframe/CAR/SITE/prefix contracts must still hold.
sys.path.insert(0,str(r.t.base.D/'round48'))
import two_bit_source_native as source
x=source.inputs();pre=x['prefix'];epre=F(int(pre['prefix_error_L1_numerator_hex'],16),1<<pre['precision_bits'])
delta=F(1,1<<3456);eps=F(1,1<<4096)
select=max(26*delta,498*F(1,1<<3460));L=3**9
half=F(1,1<<9841)+L*(epre+select)+(2*L+(2*L-2)*23+1)*eps
choi=4*half+2*delta;car=24*delta+43*eps
conditional_total=1440*choi+128*car+18*delta
assert conditional_total<F(1,1<<3423)

paths=[P/'regular_link_julia.py',P/'check_regular_link_julia.py',B/'round42/proper_link_targets.py',B/'round42/proper_link_native.py',B/'round93/proper_link_two_bit_targets.py',B/'round93/proper_link_two_bit_native.py',B/'round93/SHORT_GRID_CERTIFICATE.json',B/'round25/targets.py',B/'round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md']
out={'status':'PASS_B103_REGULAR_PROPER_LINK_JULIA_CONSTRUCTIVE_SECTOR',
     'chart':'six exact Fraction offsets |offset|<2^-32; GEN order; four-valued digits',
     'all_B25_original_Julia32_columns_float_diagnostics':reports,
     'exact_identity_zero_boost_and_pivot_tie_fixtures':True,
     'analytic_sqrt_iterations_for_3460_bits':16,'target_bits':data['target_bits'],
     'actual_certified_target_work_bits':data['bits'],'actual_grid_angles':len(angles),
     'actual_grid_angles_sha256':data['angle_powers_sha256'],
     'direct_native_high_precision_powers_checked':checked,
     'all_1024_target_intervals_contain_higher_precision_replay':True,
     'conditional_A48_source_error_recurrence_lt':'2^-3423',
     'all_496_basis_pair_permutations_and_signs_exact':True,
     'sector_operator_error_strict_lt':'2^-3451',
     'literal_forward_reverse_compressed_cost_exact_for_one_selected_sector':True,
     'f_variable_sector_count':256*4096,
     'all_4096_CODE_patterns_checked_for_one_group':True,
     'forward_reverse_variable_bank_entry_order_checked':True,
     'variable_f_reverse_upper_count_bit_lengths':{k:v.bit_length() for k,v in upper256.items()},
     'variable_f_upper_is_actual_price':False,
     'SOURCEI_replacement_included':False,'whole_bank_inventory_computed':False,
     'full_program_or_2^29_masks_executed':False,'physical_C_closed':False,'GR_closed':False,
     'inputs_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in paths}}
(P/'B103_REGULAR_LINK_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
