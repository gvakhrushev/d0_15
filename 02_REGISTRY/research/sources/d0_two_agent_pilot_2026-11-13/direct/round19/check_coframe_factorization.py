#!/usr/bin/env python3
"""Symbolic full-column CAR identities plus all local-sector source binding."""
from pathlib import Path
from itertools import product
import hashlib,importlib.util,json,sys
import numpy as np
import sympy as s
import julia_locality as loc
import coframe_factorization as f
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('a19_targets',loc.B/'round25/targets.py')
t=importlib.util.module_from_spec(spec);sys.modules[spec.name]=t;spec.loader.exec_module(t)
mm=f.mm;cat=loc.catalogue();record=json.loads((P/'JULIA_LOCAL_SECTORS.json').read_text())
assert record['banks']==cat
for path,digest in record['input_sha256'].items():assert h(Path(path))==digest
assert h(P/'julia_locality.py')==record['source_sha256']

# Independent address-locality checks: every coordinate has exactly one
# owning source group, no matter bit enters any Julia sector, all local
# assignments occur, and padded/anchor addresses remain separately typed.
coord=loc.COORD;owned=set();total=0
for bank,rows in cat.items():
    for row in rows:
        idx=row['SAM_indices'];total+=1<<len(idx)
        for j in idx:
            q=coord[j];assert q['kind']!='matter' and q['site']==row['site'] and q['role']==row['direction']
            assert (q['kind']=='coframe')==(row['kind']=='inverse_coframe_column');owned.add(j)
        assert len(idx) in (0,4,6)
        if idx and coord[idx[0]]['kind']=='coframe':assert [coord[j]['component'] for j in idx]==list(range(4))
        if idx and coord[idx[0]]['kind']=='proper_link':assert {tuple(coord[j]['generator']) for j in idx}==set(product(range(4),repeat=2)).intersection({(i,j) for i in range(4) for j in range(i+1,4)})
        if bank not in ('f','q'):assert not idx
        if bank=='q' and row['kind']=='proper_link':assert not idx
assert total==38151 and len(owned)==2560

# All local coframe target vectors. This extraction uses original B25 base
# fields and its explicit raw coordinate increment; no new field definition.
u0=t.fields('f',None)[0];ref=t.fields('0',None)[0];vectors={};sector_count=0
for bank in ('f','0'):
    for row in loc.sectors(cat[bank]):
        if row['kind']!='inverse_coframe_column':continue
        ix=t.INDEX[tuple(row['site'])];role=row['direction'];v=(u0 if bank=='f' else ref)[ix,:,role].copy()
        for j,b in zip(row['SAM_indices'],row['SAM_pattern']):v[coord[j]['component']]+=t.SAMP*(b-t.PVAL**2)
        vectors.setdefault(tuple(float(x) for x in v),[]).append((bank,row['a'],row['SAM_pattern']));sector_count+=1
assert sector_count==5888
binding_cases=0
for pattern in ((0,0,0,0),(1,1,1,1),(1,0,1,0),(0,1,1,0)):
    label=np.zeros(2688,dtype=np.int8)
    for j,q in enumerate(coord):
        if q['kind']=='coframe':label[j]=pattern[q['component']]
    actual=t.fields('f',label)[0]
    for row in cat['f']:
        if row['kind']!='inverse_coframe_column':continue
        ix=t.INDEX[tuple(row['site'])];v=u0[ix,:,row['direction']].copy()
        for j in row['SAM_indices']:v[coord[j]['component']]+=t.SAMP*(int(label[j])-t.PVAL**2)
        assert np.array_equal(v,actual[ix,:,row['direction']]);binding_cases+=1

maximum=0.;min_norm=1.;max_norm=0.;max_macro=0
for v in vectors:
    v=np.asarray(v);got,V,F,rotations=f.compiled_target(v)
    expected=t.creator_julia_cached(np.ascontiguousarray(v).tobytes())
    err=float(np.max(np.abs(got-expected)));assert err<5e-15
    assert np.max(np.abs(mm(F.T,F)-np.eye(16)))<3e-15
    assert np.max(np.abs(V[:,0]-v/np.linalg.norm(v)))<1e-15
    for j,c,si in rotations:
        exterior=t.exterior(f.plane(4,0,j,c,si));assert np.max(np.abs(exterior-f.fock_plane(j,c,si)))<4e-16
    maximum=max(maximum,err);norm=float(np.linalg.norm(v));min_norm=min(min_norm,norm);max_norm=max(max_norm,norm)
    max_macro=max(max_macro,2*4*len(rotations)+2)
assert max_macro==26

# Exact symbolic CAR covariance, including the ORDER-dependent signs and
# both occupied/empty modes. These are polynomial identities modulo c²+s²=1.
cc,ss=s.symbols('c s',real=True)
creators=[s.Matrix([[int(z) for z in row] for row in a]) for a in t.CREATORS]
def reduced(x):return s.expand(x).subs(ss**2,1-cc**2).expand()
symbolic_entries=0
for j in (1,2,3):
    V=s.eye(4);V[0,0]=V[j,j]=cc;V[j,0]=ss;V[0,j]=-ss;F=s.eye(16)
    for a,b,sign in f.fock_pairs(j):F[a,a]=F[b,b]=cc;F[b,a]=sign*ss;F[a,b]=-sign*ss
    assert all(reduced(x)==0 for x in F.T*F-s.eye(16))
    assert F[:,0]==s.eye(16)[:,0]
    for mode in range(4):
        target=sum((V[k,mode]*creators[k] for k in range(4)),s.zeros(16))
        assert all(reduced(x)==0 for x in F*creators[mode]*F.T-target)
        symbolic_entries+=256

# Exact base Julia block for C=n a0†, with defect s=sqrt(1-n²).
nn,dd=s.symbols('n d',real=True);C=nn*creators[0]
left=s.eye(16)+(dd-1)*creators[0]*creators[0].T
right=s.eye(16)+(dd-1)*creators[0].T*creators[0]
J=C.row_join(left).col_join(right.row_join(-C.T));X=s.zeros(32);R=s.eye(32)
for x in range(32):X[x^16,x]=1
for rest in range(0,16,2):
    a,b=rest|1,rest|16;R[a,a]=R[b,b]=dd;R[b,a]=-nn;R[a,b]=nn
assert R*X==J
out={'status':'PASS_ALL_COLUMN_COFRAME_JULIA_FACTORIZATION_AND_SOURCE_LOCALITY',
     'checker_sha256':h(Path(__file__)),'factorization_sha256':h(P/'coframe_factorization.py'),
     'local_sector_catalogue_sha256':h(P/'JULIA_LOCAL_SECTORS.json'),
     'all_seven_bank_local_sectors':total,'geometric_SAM_coordinates':len(owned),
     'original_B25_coframe_binding_cases':binding_cases,'coframe_sector_cases_f_and_reference':sector_count,
     'distinct_float_target_vectors':len(vectors),'full32_matrix_comparisons':len(vectors),
     'max_float_matrix_difference_diagnostic':maximum,'min_norm_float_diagnostic':min_norm,'max_norm_float_diagnostic':max_norm,
     'exact_symbolic_CAR_covariance_entries':symbolic_entries,'exact_symbolic_base_32_matrix_identity':True,
     'maximum_ideal_planar_and_X_macros_per_sector':max_macro,
     'hypothetical_native_error_if_each_macro_delta':'26 delta on each coherent address/SAM block; no multiplication by number of disjoint sectors',
     'coframe_native_angles_certified':False,'coframe_native_word_emitted':False,'proper_link_SELECT_compiled':False,
     'full_Omega_preparation_compiled':False,'physical_C_closed':False,'GR_closed':False}
(P/'COFRAME_FACTORIZATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','distinct_float_target_vectors','exact_symbolic_CAR_covariance_entries','maximum_ideal_planar_and_X_macros_per_sector']}))
