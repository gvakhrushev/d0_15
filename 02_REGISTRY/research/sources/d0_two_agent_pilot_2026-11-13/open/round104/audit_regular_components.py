#!/usr/bin/env python3
"""Independent A53 chart/mapping/grid/cost audit; never writes A."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,islice
from hashlib import sha256
from collections import Counter
import importlib.util,json,sys
import numpy as np
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
A=D/'round53';B=P.parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(A))
import regular_field_targets as t
import regular_source_components as c
import check_regular_source_components as frozen

def sha(p):return sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
plan=load(A/'REGULAR_SOURCE_COMPONENT_PLAN.json');receipt=load(A/'REGULAR_SOURCE_COMPONENT_CHECK.json')
for f,h in plan['source_sha256'].items():assert sha(Path(f))==h,f
for f,h in receipt['source_sha256'].items():assert sha(Path(f))==h,f
assert c.build_plan()==plan
zero,extreme,kinds=frozen.validate_fields()
assert kinds==receipt['coordinate_kinds']

# Read the original files directly, rebuild key->index independently, and
# inspect every one of the 7168 coframe and 1728 CAR row bindings.
coord=[json.loads(line) for line in t.old.loc.COORD_PATH.read_text().splitlines()]
assert len(coord)==2688 and all(x['sam_index']==j for j,x in enumerate(coord))
assert Counter(x['kind'] for x in coord)==Counter(coframe=1024,proper_link=1536,matter=128)
coidx={};matidx={}
for j,z in enumerate(coord):
    site=tuple(z['site'])
    if z['kind']=='coframe':coidx[(site,z['role'],z['component'])]=j
    elif z['kind']=='matter':matidx[(site,z['grade'])]=j
assert len(coidx)==1024 and len(matidx)==128
PF=[json.loads(line) for line in (B/'round21/ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()]
assert len(PF)==256
counts=Counter()
for bank in t.old.loc.BANKS:
    for row in t.coframe_rows(bank):
        site=tuple(row['site']);role=row['direction'];ids=row['coordinates']
        keys=[(site,role,k) for k in range(4)]
        present=all(key in coidx for key in keys)
        assert present or all(key not in coidx for key in keys)
        expect=[coidx[k] for k in keys] if bank in ('f','q') and present else []
        assert ids==expect
        counts['coframe']+=1
assert counts['coframe']==7168
for bank in ('q','y+','y-'):
    for row in t.material_rows(bank):
        site=tuple(row['site_coordinates']);assert site==tuple(PF[row['site']]['site'])
        keys=[(site,0),(site,15)];present=all(key in matidx for key in keys)
        assert present or all(key not in matidx for key in keys)
        expected=[q for k in keys for q in (matidx[k],2688+matidx[k])] if bank=='q' and present else []
        assert row['SAM_indices']==expected
        if expected:
            pat=row['SAM_pattern'];assert len(pat)==4
            digits=[pat[0]+2*pat[1],pat[2]+2*pat[3]]
            assert all(0<=x<4 for x in digits)
        else:assert not row['SAM_pattern']
        counts['CAR_'+bank]+=1
assert counts['CAR_q']==1216 and counts['CAR_y+']==counts['CAR_y-']==256
for ds in product(range(4),repeat=4):
    assert t.old.code_pattern(ds)==[v for d in ds for v in (d&1,d>>1)]

# Independently enclose coframe norms and *all three* elimination radii over
# the entire box (one wide interval per original row), not selected fields.
iv,const,_=c.context(256);S=iv.scale
rad=t.RADIUS+3*t.SIGMA; rmax=iv.rational(rad.numerator,rad.denominator)[1]
def sq(z):
    lo=0 if z[0]<=0<=z[1] else min(z[0]*z[0],z[1]*z[1]);hi=max(z[0]*z[0],z[1]*z[1])
    return lo//S,-((-hi)//S)
def summ(xs):
    out=iv.rational(0)
    for x in xs:out=iv.add(out,x)
    return out
wide_checks=0
for bank in t.old.loc.BANKS:
    for row in t.coframe_rows(bank):
        _,spec=t.old.coframe_spec(row,(0,)*len(row['coordinates']))
        if spec['family']=='current':
            s=dict(spec);s.pop('digits');s['bits']=None
            v=t.old.cf.vector(iv,const,s)
            if row['coordinates']:v=[(a-rmax,b+rmax) for a,b in v]
        else:v=t.old.coframe_vector(iv,const,spec)
        n=iv.sqrt(summ(sq(x) for x in v));assert 0<n[0] and n[1]<S
        dom=({0:1,1:0,2:2,3:3}[spec['role']] if spec['family']=='current' else {0:0,1:0,2:2,3:3}[spec['role']])
        first=dom if dom else 1
        order=[first]+[j for j in (1,2,3) if j!=first]
        cur=list(v)
        for j in order:
            rr=iv.sqrt(iv.add(sq(cur[0]),sq(cur[j])))
            assert 2*rr[0]>=n[1] and rr[0]>0
            cur[0]=rr;cur[j]=iv.rational(0)
        wide_checks+=1
assert wide_checks==7168
# For matter the fixed anchor v1=sqrt((1+sqrt(p))/2) bounds every
# residual radius, uniformly for the q box and unchanged y references.
v1=iv.sqrt(iv.div(iv.add(iv.rational(1),const['sqrtp']),iv.rational(2)))
assert 10*v1[0]>9*S
for x0 in range(4):
    _,psi=t.old.mat.half_vector(iv,const,{'kind':'q','x0':x0,'bits':None})
    psi=[(a-rmax,b+rmax) for a,b in psi]
    n2=summ(sq(x) for x in psi)
    assert 15*n2[1]<S
    slack=iv.sub(iv.sub(iv.rational(1),const['p']),n2)
    assert 3*slack[0]>S
assert t.RADIUS+3*t.SIGMA<F(3,8*2**30)
assert F(9,4)**2>5 and 2**2<5

# Source numerical diagnostic against the original independent B25 table.
sp=importlib.util.spec_from_file_location('b104_b25',B/'round25/targets.py')
b25=importlib.util.module_from_spec(sp);sys.modules[sp.name]=b25;sp.loader.exec_module(b25)
field=t.FieldCentre(tuple(F((j%1021)-510,2**43) for j in range(2688)))
iv,const,_=c.context(192)
maxcf=maxmat=0.0; cfcount=matcount=0
for bank in t.old.loc.BANKS:
    ub,_,_=b25.fields(bank)
    for row in t.coframe_rows(bank):
        ds=tuple((j*3+1)%4 for j in row['coordinates'])
        v,_=t.coframe_vector(field,row,ds,iv,const)
        vv=np.array([float((a+b)/(2*iv.scale)) for a,b in v])
        expect=ub[b25.INDEX[tuple(row['site'])],:,row['direction']].copy()
        for j,idx in enumerate(row['coordinates']):expect[j]+=float(field.offsets[idx])
        err=float(np.max(np.abs(vv-expect)));assert err<3e-14,(bank,row,err)
        maxcf=max(maxcf,err);cfcount+=1
for bank in ('q','y+','y-'):
    _,_,mb=b25.fields(bank)
    for row in t.material_rows(bank):
        _,psi=t.material_half_vector(field,bank,row,iv,const)
        vv=np.array([float((a+b)/(2*iv.scale)) for a,b in psi])
        expect=mb[row['site']].copy()
        if bank=='q':
            for j,idx in enumerate(row['SAM_indices'][::2]):expect[j]+=float(field.offsets[idx])
        err=float(np.max(np.abs(vv-expect)));assert err<3e-14,(bank,row,err)
        maxmat=max(maxmat,err);matcount+=1

# Independent arithmetic power checks on exact cardinal quadrants and
# rational non-cardinal points, including exact cos/sin magnitude ties.
from fractions import Fraction
bits=7168;ivh=t.old.Dyadic(bits);S=ivh.scale;consth=t.old.cf.constants(ivh)
def mul_ball(x,y):
    a,b,e=x;d,f,g=y
    return ((a*d-b*f)>>bits,(a*f+b*d)>>bits,e+g+((e*g+S-1)>>bits)+2)
a,b=consth['sqrtp'],consth['p'];powers=[(a[0],b[0],a[1]-a[0]+b[1]-b[0])]
for _ in range(3540):powers.append(mul_ball(powers[-1],powers[-1]))
def power(n):
    acc=(S,0,0);j=0
    while n:
        if n&1:acc=mul_ball(acc,powers[j])
        j+=1;n//=2
    a,b,e=acc;return (a-e,a+e),(b-e,b+e)
checks=0
circle=[(1,0),(0,1),(-1,0),(0,-1)] + [(F(a,5),F(b,5)) for a,b in ((3,4),(-3,4),(-3,-4),(3,-4),(4,3),(-4,3),(-4,-3),(4,-3))]
for K in (15,24):
    grid=c.UniformAngles(K)
    for cv,sv in circle:
        cv,sv=F(cv),F(sv)
        records,_=grid.select(lambda iv,cc:([('v',iv.rational(cv.numerator,cv.denominator),iv.rational(sv.numerator,sv.denominator))],None))
        item=records['v'];aa,bb=power(int(item['k'])*(1<<K));C=ivh.rational(cv.numerator,cv.denominator);T=ivh.rational(sv.numerator,sv.denominator)
        err=max(abs(aa[0]-C[1]),abs(aa[1]-C[0]))+max(abs(bb[0]-T[1]),abs(bb[1]-T[0]));assert err<S>>3460
        checks+=1
    iv0,_,_=c.context(4096);zz=iv0.div(iv0.sqrt(iv0.rational(2)),iv0.rational(2))
    records,_=grid.select(lambda iv,cc:([('v',iv.div(iv.sqrt(iv.rational(2)),iv.rational(2)),iv.div(iv.sqrt(iv.rational(2)),iv.rational(2)))],None))
    aa,bb=power(int(records['v']['k'])*(1<<K));T=ivh.div(ivh.sqrt(ivh.rational(2)),ivh.rational(2))
    err=max(abs(aa[0]-T[1]),abs(aa[1]-T[0]))+max(abs(bb[0]-T[1]),abs(bb[1]-T[0]));assert err<S>>3460
    checks+=1

# The controlled X emits one pi/2 rotation and a doubled-angle pi phase.
# Bound the two *actual* powers independently and their summed error.
xword=c.Components(field).controlled_x();k=int(xword['k'])
a0,b0=power(k*(1<<24));a1,b1=power(k*(1<<25))
rot_error=max(abs(a0[0]),abs(a0[1]))+max(abs(b0[0]-S),abs(b0[1]-S))
phase_error=max(abs(a1[0]+S),abs(a1[1]+S))+max(abs(b1[0]),abs(b1[1]))
assert rot_error<S>>3460 and phase_error<S>>3459
assert rot_error+phase_error<3*(S>>3460)

# Exhaust integer inequality for every possible K, all-zero or nonzero
# pattern and extreme k=q. The phase uses multiplier 25, all other coframe
# units multiplier 24, CAR multiplier 15.
def pcount(K,mult,q,nonzero):
    terms=1<<K;neg=(terms//2 if nonzero else 0);k=q*(1<<(mult-K))
    return Counter(G_port=neg*k,G_other=(terms-neg)*k,CX=K*terms+6*neg+8,SourceI=4*neg)
def inv_count(x):
    gp=x['G_port'];go=x['G_other']
    return Counter(G_port=gp+go,G_other=0,CX=x['CX']+6*go,SourceI=3*x['SourceI']+4*(gp+go))
u=c.componentwise_upper(); q24=c.UniformAngles(24).q;q15=c.UniformAngles(15).q
p24=Counter(G_port=(1<<25)*q24,G_other=(1<<25)*q24,CX=29*(1<<25)+8,SourceI=1<<26)
p15=Counter(G_port=(1<<15)*q15,G_other=(1<<15)*q15,CX=18*(1<<15)+8,SourceI=1<<16)
for mult,cap,pair,q in ((24,24,p24,q24),(25,25,p24,q24),(15,15,p15,q15)):
    for K in range(1,cap+1):
        for nonzero in (False,True):
            pc=pcount(K,mult,q,nonzero)
            assert all(pc[z]<=pair[z] for z in pc)
            assert all(inv_count(pc)[z]<=inv_count(pair)[z] for z in inv_count(pc))
assert u['coframe_per_sector']==Counter({k:27*v for k,v in (p24+inv_count(p24)).items()})
assert u['material_per_sector']==Counter({k:3*v for k,v in p15.items()})
# Reconstruct full componentwise bank upper without using the plan's sector
# counts: 64 interior sites * 4 roles, all 4^4 words; other rows fixed.
for bank in t.old.loc.BANKS:
    expected_count=256*4**4+768 if bank in ('f','q') else 1024
    assert u['coframe'][bank]['sectors']==expected_count
    expect=Counter({key:expected_count*v for key,v in u['coframe_per_sector'].items()})
    assert u['coframe'][bank]['forward']==expect
    assert u['coframe'][bank]['literal_inverse']==inv_count(expect)
    saved=plan['uniform_componentwise_inventory_upper']['coframe'][bank]
    assert saved['sectors']==expected_count
    for typ,val in (('forward',expect),('literal_inverse',inv_count(expect))):
        assert {k:int(v,16) for k,v in saved[typ].items()}==dict(val)
for bank in ('q','y+','y-'):
    expected_count=64*16+192 if bank=='q' else 256
    assert u['material'][bank]['sectors']==expected_count
    expect=Counter({key:expected_count*v for key,v in u['material_per_sector'].items()})
    assert u['material'][bank]['forward']==expect
    assert u['material'][bank]['literal_inverse']==inv_count(expect)
    saved=plan['uniform_componentwise_inventory_upper']['material'][bank]
    assert saved['sectors']==expected_count
    for typ,val in (('forward',expect),('literal_inverse',inv_count(expect))):
        assert {k:int(v,16) for k,v in saved[typ].items()}==dict(val)

# Check real emitted sectors/controls and literal inverse budgets at two
# distinct fields, several roles, both outer inverse parities.
points=[t.FieldCentre(),field]; actual=[]
for field0 in points:
    components=c.Components(field0)
    for bank in ('f','q','x-'):
        for role in (0,1,2,3):
            row=next(z for z in t.coframe_rows(bank) if z['direction']==role and bool(z['coordinates'])==(bank in ('f','q')))
            ds=(0,1,2,3) if row['coordinates'] else ()
            for depth in (0,1,2,3):
                agg=Counter()
                for bound,d in components.coframe_units(row,ds,depth=depth):
                    assert bound['K']<=25 and len(set(bound['controls']+[bound['target']]))==bound['K']+1
                    assert len(bound['permutation'])<=4
                    layout=c.local.coframe_layout(); outer=set(layout['address']+layout['SAM']+[layout['branch']])
                    assert bound['target'] not in outer
                    assert all(g['wires'][-1] not in outer for g in bound['permutation'])
                    raw=pcount(bound['K'],bound['K'],bound['k'],any(bound['pattern']))
                    raw['CX']-=8-2*len(bound['permutation'])
                    for _ in range(d):raw=inv_count(raw)
                    agg.update(raw)
                upper=u['coframe_per_sector']
                for _ in range(depth):upper=inv_count(upper)
                assert all(v<=upper[k] for k,v in agg.items())
                actual.append(('coframe',bank,role,depth))
    for bank in ('q','y+','y-'):
        row=next(z for z in t.material_rows(bank) if bool(z['SAM_indices'])==(bank=='q'))
        for depth in (0,1,2,3):
            agg=Counter()
            for bound,d in components.material_units(bank,row,depth=depth):
                assert bound['K']<=15 and len(set(bound['controls']+[bound['target']]))==bound['K']+1
                layout=c.local.material_layout();outer=set(layout['internal_SITE']+layout['SAM']+layout['RIGHT']+[layout['oldRIGHT_witness']])
                assert bound['target'] not in outer
                assert all(g['wires'][-1] not in outer for g in bound['permutation'])
                raw=pcount(bound['K'],bound['K'],bound['k'],any(bound['pattern']))
                raw['CX']-=8-2*len(bound['permutation'])
                for _ in range(d):raw=inv_count(raw)
                agg.update(raw)
            upper=u['material_per_sector']
            for _ in range(depth):upper=inv_count(upper)
            assert all(v<=upper[k] for k,v in agg.items())
            actual.append(('material',bank,depth))

# Replay every column of selected actual coframe Julia and CAR preparation
# at compressed macro boundaries. G exponents are independently evaluated
# as complex balls; no 2^K Walsh masks or gate repetitions are expanded.
def signed_power(bound,depth):
    aa,bb=power(int(bound['k'])*(1<<bound['K']))
    cv=float((aa[0]+aa[1])/(2*S));sv=float((bb[0]+bb[1])/(2*S))
    return cv,(-sv if depth%2 else sv)
def permute_rows(M,gate,basis):
    src,dst=gate['wires'];ci=basis.index(src);ti=basis.index(dst)
    assert ci!=ti
    perm=[z^(((z>>ci)&1)<<ti) for z in range(len(M))]
    return M[perm,:].copy()
def apply_unit(M,bound,depth,basis,external):
    for gate in bound['permutation']:M=permute_rows(M,gate,basis)
    c0,s0=signed_power(bound,depth);q=basis.index(bound['target']);out=M.copy()
    for z in range(len(M)):
        if (z>>q)&1:continue
        def val(w):return (z>>basis.index(w))&1 if w in basis else external[w]
        if not all(val(w)==b for w,b in zip(bound['controls'],bound['pattern'])):continue
        z1=z|(1<<q);out[z,:]=c0*M[z,:]-s0*M[z1,:];out[z1,:]=s0*M[z,:]+c0*M[z1,:]
    M=out
    for gate in reversed(bound['permutation']):M=permute_rows(M,gate,basis)
    return M

components=c.Components(field);matrix_checks=[]
for bank,role in (('f',0),('q',1),('x-',2)):
    row=next(z for z in t.coframe_rows(bank) if z['direction']==role and bool(z['coordinates'])==(bank in ('f','q')))
    ds=(0,1,2,3) if row['coordinates'] else ()
    lay=c.local.coframe_layout();basis=lay['choi_output']+[lay['aux_arbitrary']]
    external={w:(row['address']>>i)&1 for i,w in enumerate(lay['address'])}
    external[lay['branch']]=1
    for j,digit in zip(row['coordinates'],ds):
        external[lay['SAM'][j]]=digit&1;external[lay['SAM'][2688+j]]=digit>>1
    M=np.eye(64)
    for bound,depth in components.coframe_units(row,ds,lay=lay):
        M=apply_unit(M,bound,depth,basis,external)
    source_v,_=t.coframe_vector(field,row,ds,iv,const)
    vec=np.array([float((a+b)/(2*iv.scale)) for a,b in source_v])
    J=b25.creator_julia_cached(np.ascontiguousarray(vec).tobytes())
    expected=np.zeros((64,64));expected[:32,:32]=J;expected[32:,32:]=J
    err=float(np.max(np.abs(M-expected)));assert err<4e-12,(bank,role,err)
    matrix_checks.append({'kind':'coframe_Julia32_aux2','bank':bank,'role':role,'max_error':err})
for bank in ('q','y+','y-'):
    row=next(z for z in t.material_rows(bank) if bool(z['SAM_indices'])==(bank=='q'))
    lay=c.local.material_layout();basis=lay['grade']
    external={w:(row['site']>>i)&1 for i,w in enumerate(lay['internal_SITE'])}
    for j,bit in zip(row['SAM_indices'],row['SAM_pattern']):external[lay['SAM'][j]]=bit
    M=np.eye(16)
    for bound,depth in components.material_units(bank,row,lay=lay):M=apply_unit(M,bound,depth,basis,external)
    vec,_=t.material_half_vector(field,bank,row,iv,const)
    initial=np.zeros(16);initial[1]=1
    target=np.array([float((vec.get(k,(0,0))[0]+vec.get(k,(0,0))[1])/(2*iv.scale)) for k in range(16)])
    assert np.isfinite(M).all() and float(np.max(np.abs(M)))<=1+4e-12
    err=float(np.max(np.abs(M[:,1]-target)));assert err<4e-12,(bank,err)
    gram=np.einsum('ki,kj->ij',M,M)
    assert float(np.max(np.abs(gram-np.eye(16))))<4e-12
    ideal=np.eye(16)
    for rot in t.old.mat.rotations(iv,vec):
        cc=float((rot['cos'][0]+rot['cos'][1])/(2*iv.scale))
        ss=float((rot['sin'][0]+rot['sin'][1])/(2*iv.scale))
        u,v=1,rot['other'];ru=ideal[u,:].copy();rv=ideal[v,:].copy()
        ideal[u,:]=cc*ru-ss*rv;ideal[v,:]=ss*ru+cc*rv
    fullerr=float(np.max(np.abs(M-ideal)));assert fullerr<4e-12,(bank,fullerr)
    matrix_checks.append({'kind':'CAR_preparation16_all_columns','bank':bank,
                          'target_column_max_error':err,'all_columns_max_error':fullerr})

inputs=[A/'regular_field_targets.py',A/'regular_source_components.py',A/'REGULAR_SOURCE_COMPONENT_PLAN.json',A/'check_regular_source_components.py',A/'REGULAR_SOURCE_COMPONENT_CHECK.json',A/'REGULAR_FIELD_COMPONENTS_RU.md',B/'round25/targets.py',t.old.loc.COORD_PATH,t.old.loc.ADDR_PATH]
out={'status':'PASS_B104_A53_COFRAME_CAR_SCOPED_AUDIT','all_original_coframe_rows_mapped':counts['coframe'],
     'all_original_CAR_rows_mapped':dict((k,v) for k,v in counts.items() if k.startswith('CAR_')),
     'independent_wide_coframe_boxes':wide_checks,'independent_q_matter_slices':4,
     'all_B25_coframe_values_float_diagnostic_count':cfcount,'all_B25_CAR_values_float_diagnostic_count':matcount,
     'B25_coframe_float_max_error':maxcf,'B25_CAR_float_max_error':maxmat,
     'independent_native_grid_powers_checked':checks,
     'native_grid_tests_include_exact_zero_all_quadrants_and_equal_magnitudes':True,
     'actual_controlled_X_rotation_and_doubled_phase_error_lt':'3*2^-3460',
     'all_mask_widths_extremal_cost_and_inverse_bounded':True,
     'all_bank_forward_and_literal_inverse_upper_rebuilt':True,
     'actual_sector_inverse_inventory_checks':len(actual),
     'actual_native_aggregated_rotation_all_columns_diagnostics':matrix_checks,
     'new_proper_link_or_global_SOURCE_compiled_by_A53':False,
     'actual_complete_source_clock_or_physical_Cost_Info_identified':False,
     'production_word_executed':False,'physical_C_closed':False,'GR_closed':False,
     'inputs_sha256':{str(p):sha(p) for p in inputs}}
(P/'B104_A53_AUDIT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='inputs_sha256'},indent=2))
