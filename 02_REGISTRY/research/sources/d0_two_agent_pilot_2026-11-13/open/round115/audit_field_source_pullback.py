#!/usr/bin/env python3
"""Independent typed audit of A58 plane readout and fixed-slice pullback."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json,sys
import sympy as sp
import mpmath as mp
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round58'));import field_source_pullback as a
def read(path):return json.loads(Path(path).read_text())
def digest(path):return sha256(Path(path).read_bytes()).hexdigest()
owner_files=[D/'round58'/n for n in ('field_source_pullback.py','check_field_source_pullback.py',
  'FIELD_SOURCE_PULLBACK_RU.md','FIELD_SOURCE_PULLBACK_PLAN.json','FIELD_SOURCE_PULLBACK_CHECK.json')]
assert all(p.is_file() for p in owner_files)
assert read(owner_files[3])==a.plan()
receipt=read(owner_files[4]);assert receipt['status']=='PASS_EXACT_MG2_PLANE_READOUT_AND_FORWARD_PULLBACK'
for path,h in receipt['input_sha256'].items():assert digest(path)==h,path
b114=read(O/'round114/B114_PHYSICAL_CHART_CHECK.json')
for path,h in b114['input_sha256'].items():assert digest(path)==h,path

# Independently form each plane support from bit masks rather than using the
# owner's insertion algorithm. Compare all a<b, axes and m=1..4, including
# every spectator column. Digit order is low_j + 2*high_j.
_,_,weights=a.mg.mg2();Q=a.mg.e.Q4
assert len(weights)==6
iv=a.mg.e.Dyadic(256)
for weight in weights.values():
    lo,hi=iv.evaluate((a.mg.e.expr(weight),))[0];assert 0<lo<=hi
cases=terms=0
for m in range(1,5):
    d=1<<(2*m)
    for axis in range(m):
        active=(1<<axis)|(1<<(m+axis))
        got=list(a.plane_terms(axis,m)); table={t.pair:t.coefficient for t in got}
        assert len(got)==len(table)==6*(1<<(2*m-2))
        want={(x,y) for x,y in combinations(range(d),2) if not ((x^y)&~active)}
        assert set(table)==want
        def digit(x):return ((x>>axis)&1)+2*((x>>(m+axis))&1)
        for (x,y),value in table.items():
            i,j=digit(x),digit(y);assert i<j and value==weights[i,j]
        # A separate exact-Q4 test functional fixes the plane sign and weight.
        row=lambda x,y:F(((x+5)*(y+11))%97-48,113)
        direct=sum((weights[digit(x),digit(y)]*row(x,y) for x,y in want),Q())
        assert a.bounded_raw_row(row,axis,m,max_terms=6*(1<<(2*m-2)))==direct
        terms+=len(table);cases+=1
assert cases==10

# Every production bit-pair address; direct independent bit insertion on
# diverse spectator patterns for representative extreme/middle axes.
source=a.family.prior.source;sam=source.namespace()['layout']['SAM']
for j in range(2688):
    assert (source.physical_wire(sam[j]),source.physical_wire(sam[2688+j]))==(2+j,11893771936+j)
for axis in (0,1,1344,2687):
    positions=[j for j in range(5376) if j not in (axis,2688+axis)]
    for spectator in (0,1,(1<<5374)-1,int('a5'*671,16)):
        expected=sum(((spectator>>i)&1)<<bit for i,bit in enumerate(positions))
        base=a.embed_spectator(spectator,axis);assert base==expected
        for digit in range(4):
            assert a.local_index(base,digit,axis)==base|((digit&1)<<axis)|((digit>>1)<<(2688+axis))
assert 2688*6*2==32256

# A57 request pairs are the actual Pf signed plane family, same exact field,
# plane and original real skew E_ab[a,b]=-1. No sum is materialised at m=2688.
v=[F((j%17)-8,1<<38) for j in range(2688)];field=a.family.FieldCentre(tuple(v))
pair_count=0
for axis in (0,1344,2687):
    import itertools
    for coefficient,plus,minus in itertools.islice(a.signed_requests(field,axis),12):
        assert plus.label.arm==minus.label.arm=='Pf'
        assert plus.label.sign==1 and minus.label.sign==-1
        assert plus.label.plane==minus.label.plane and plus.field==minus.field==field
        assert a.family.Request.decode(plus.encode())==plus and a.family.Request.decode(minus.encode())==minus
        assert coefficient in weights.values();pair_count+=1
assert pair_count==36
try:a.bounded_raw_row(lambda x,y:1.1,0,1,max_terms=6)
except TypeError:pass
else:raise AssertionError('float accepted as exact Q4 price')
try:a.bounded_raw_row(lambda x,y:F(0),0)
except ValueError:pass
else:raise AssertionError('giant production sum not refused')

# Direct centre-name check: no rounded B21 export and no sampled CODE digits.
# All 64 sites, four roles and four components: compare 128/192 intervals,
# verify every coframe offset and all link coefficients in their own indices.
zero=a.family.FieldCentre();p0=a.bound_chart_point(zero,128);p1=a.bound_chart_point(field,128)
p2=a.bound_chart_point(field,192)
assert p1['field_sha256']==sha256(field.encode()).hexdigest()!=p0['field_sha256']
sites0=[tuple(r['site']) for r in p1['sites']];assert sites0==sorted(sites0) and len(sites0)==64
lookup={site:i for i,site in enumerate(sites0)}
target=a.family.prior.source.t;coords=target.COORD
for idx,c in enumerate(coords):
    si=lookup[tuple(c['site'])];pt0=p0['sites'][si];pt1=p1['sites'][si];pt2=p2['sites'][si]
    if c['kind']=='coframe':
        a0,b0=pt0['u_intervals'][c['component']][c['role']]
        a1,b1=pt1['u_intervals'][c['component']][c['role']]
        a2,b2=pt2['u_intervals'][c['component']][c['role']]
        shift=field.offsets[idx]*(1<<128)
        assert a1-b0<=shift<=b1-a0
        assert a0<=b0 and a1<=b1 and (a1<<64)<=a2<=b2<=(b1<<64)
    elif c['kind']=='proper_link':
        order=list(combinations(range(4),2));k=order.index(tuple(c['generator']))
        assert pt1['theta'][c['role']][k]==pt2['theta'][c['role']][k]==field.offsets[idx]
    else:assert c['kind']=='matter'

# Matter values are not returned by bound_chart_point because the local
# Jacobian is the identity. Verify directly in the actual A53 q-provider
# that all 128 grade-0/15 field offsets enter psi once; use the same CODE
# digits on both sides, so their sampled shift cancels rather than being
# silently treated as a centre offset.
one_row={}
for row in target.material_rows('q'):
    if row['SAM_indices']:one_row.setdefault(tuple(row['site_coordinates']),row)
assert set(one_row)==set(sites0)
ctx=target.old.Dyadic(192);const=target.old.cf.constants(ctx)
for site,row in one_row.items():
    _,a0=target.material_half_vector(zero,'q',row,ctx,const)
    _,a1=target.material_half_vector(field,'q',row,ctx,const)
    ids=row['SAM_indices'][::2]
    for index,before,after in zip(ids,a0,a1):
        shift=field.offsets[index]*(1<<192)
        assert after[0]-before[1]<=shift<=after[1]-before[0]

# Independent high-precision centre-value diagnostic from B21 formula.
# It supplements exact interval/source ownership, not a floating proof.
with mp.workdps(110):
    p=(mp.sqrt(5)-1)/2;z=mp.mpf(1)/2**20;L0=4*p**3
    Q0=1-z*L0;R0=1-z*L0*(1+p**6);k0=2*p**(-5)*(R0/Q0+p**6);nu=mp.mpf(3)/5
    bysite={(tuple(c['site']),c['role'],c['component']):i for i,c in enumerate(coords) if c['kind']=='coframe'}
    for pt in p1['sites']:
        site=tuple(pt['site']);xx,yy=site[2],site[3]
        H=k0*mp.pi**2*(xx*xx+yy*yy)/40000+mp.mpf(3)*(xx*xx-yy*yy)/1600
        base=[[0,nu,0,0],[nu,-nu*H/2,0,0],[0,0,nu,0],[0,0,0,nu]]
        for i in range(4):
            for j in range(4):
                off=field.offsets[bysite[site,j,i]];actual=base[i][j]+mp.mpf(off.numerator)/off.denominator
                low,high=pt['u_intervals'][i][j]
                assert mp.mpf(int(low))/2**128<=actual<=mp.mpf(int(high))/2**128

# Forward transpose works with a kernel, no physical norm/inverse fabricated.
matrix=[[F(1),F(2),F(0)],[F(-2),F(3),F(0)]];lam=[F(3,7),F(-4,11)]
result=a.pullback(lam,matrix);assert result[2]==0
for v0 in ([F(1),F(3),F(11)],[F(0),F(0),F(1)]):
    assert sum(lam[i]*sum(matrix[i][j]*v0[j] for j in range(3)) for i in range(2))==sum(result[j]*v0[j] for j in range(3))
assert a.norm_budget(F(7,3))==F(7,3*(1<<34))

# Exact three-state Cayley counterexample: a finite nonlinear feedback
# difference for X+Y need not equal the sum of separate plane differences.
R=sp.Rational;I=sp.eye(3);X=sp.Matrix([[0,-1,0],[1,0,0],[0,0,0]])
Y=sp.Matrix([[0,0,0],[0,0,-1],[0,1,0]]);chi=sp.Matrix([R(1,3),R(2,3),R(2,3)])
M=sp.diag(R(7,10),R(9,10),1);z=R(1,3);t=R(1,2)
def feedback_denom(generator,step):
    U=(I-step*generator/2).inv()*(I+step*generator/2)
    corner=(chi.T*M*U*chi)[0]
    return 1-z+z*corner*corner
def ratio(generator):return feedback_denom(generator,-t)/feedback_denom(generator,t)
assert ratio(X+Y)!=ratio(X)*ratio(Y)

inputs=[Path(__file__),*owner_files,O/'round114/physical_chart_l4.py',
        O/'round114/B114_PHYSICAL_CHART_CHECK.json',D/'round57/full_plane_family.py',
        D/'round53/regular_field_targets.py',O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl']
out={'status':'PASS_A58_EXACT_PLANE_SUM_AND_TYPED_FORWARD_PULLBACK',
     'all_small_support_pairs_tested':cases,'all_small_plane_terms_checked':terms,
     'all_2688_production_CODE_pairs_checked':True,'actual_signed_request_pairs_checked':pair_count,
     'signed_requests_per_all_raw_rows':'32256*2^5374',
     'all_64_A53_field_centres_128_192_interval_binding_checked':True,
     'all_128_A53_matter_offsets_checked_on_matching_CODE_digits':True,
     'independent_high_precision_coframe_diagnostic_columns':1024,
     'Q4_diagnostic_rejects_general_price':True,'nonlinear_finite_joint_X_counterexample':True,
     'raw_to_physical_error':'alpha_h*2^-34; original V_h unchanged',
     'physical_iota_inverse_required':False,'physical_reader_or_production_sum_executed':False,
     'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(f):digest(f) for f in inputs}}
(P/'B115_A58_AUDIT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))
