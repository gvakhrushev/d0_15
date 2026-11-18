#!/usr/bin/env python3
"""Check exact-source names, actual pair bindings and paid inverse depths."""
from pathlib import Path
from collections import Counter
from itertools import islice
import hashlib,importlib.util,json,sys
import mpmath as mp
import numpy as np
import coframe_targets as t
import coframe_native as n
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lib=json.loads((P/'COFRAME_ANGLE_LIBRARY.json').read_text());plan=json.loads((P/'COFRAME_NATIVE_PLAN.json').read_text())
for source,digest in lib['input_sha256'].items():assert h(Path(source))==digest,source
assert h(P/'certify_coframe_angles.py')==lib['source_sha256']
assert h(P/'coframe_native.py')==plan['source_sha256'] and h(P/'COFRAME_ANGLE_LIBRARY.json')==plan['library_sha256']
specs,banks=t.catalogue();assert banks==lib['catalogue'] and set(specs)==set(lib['families'])
precision=lib['precision_bits'];S=1<<precision
def mid(v):return (int(v[0],16)+int(v[1],16))/(2*S)
def mpmid(v):return mp.mpf(int(v[0],16)+int(v[1],16))/(2*S)
sys.path.insert(0,str(t.loc.B/'round25'));b25=t.load('a20_precision_name',t.loc.B/'round25/precision_name.py')
target_checks=0
with mp.workprec(1000):
    for name,spec in specs.items():
        family=lib['families'][name];assert family['spec']==spec
        if spec['family']=='reference':
            site=next(tuple(r['site']) for r in t.PF if r['N']==spec['PF_count']);bank='0';label=None
        else:
            bank='f';label=None
            if spec['bits'] is None:site=(0,0,spec['x2'],spec['x3'])
            else:
                site=(0,0,spec['x2'],spec['x3']) if spec['role']==1 else (0,0,1,1)
                label=np.zeros(2688,dtype=np.int8)
                for i,c in enumerate(t.loc.COORD):
                    if c['kind']=='coframe' and tuple(c['site'])==site and c['role']==spec['role']:label[i]=spec['bits'][c['component']]
        u=b25.at_site(bank,site,label)[0]
        for j in range(4):assert abs(u[j,spec['role']]-mpmid(family['vector_bounds_hex'][j]))<mp.mpf(2)**-960,(name,j)
        target_checks+=1
print('source formula diagnostics checked',target_checks,flush=True)

# Full 32-column chronology with the certified actual rotation enclosures.
# Tiny native errors are established by interval bounds, not float tolerance.
mm=t.fact.mm;maximum=0.;matrix_checks=0
for name,family in lib['families'].items():
    bindings={tuple(x['factor']):x['angle_id'] for x in family['angle_bindings']};F=np.eye(16)
    for i,r in enumerate(family['mode_rotations']):
        if r['exact_identity']:continue
        for a,b,sign in t.fact.fock_pairs(r['mode']):
            angle=lib['angles'][bindings[('mode',i,sign)]];cc=mid(angle['native_cos_hex']);ss=-mid(angle['native_sin_hex'])
            F=mm(t.fact.plane(16,a,b,cc,ss),F)
    W=np.zeros((32,32));W[:16,:16]=W[16:,16:]=F
    base=lib['angles'][bindings[('base',0,0)]];cc=mid(base['native_cos_hex']);ss=-mid(base['native_sin_hex'])
    X=np.zeros((32,32));R=np.eye(32)
    for x in range(32):X[x^16,x]=1
    for rest in range(0,16,2):
        a,b=rest|1,rest|16;R[a,a]=R[b,b]=cc;R[b,a]=ss;R[a,b]=-ss
    got=mm(mm(mm(W,R),X),W.T);v=np.array([mid(x) for x in family['vector_bounds_hex']])
    expected=b25.t.creator_julia_cached(np.ascontiguousarray(v).tobytes())
    err=float(np.max(np.abs(got-expected)));assert err<5e-15,(name,err)
    maximum=max(maximum,err);matrix_checks+=1

# Every saved native angle inequality, including the two-part controlled X.
for entry in lib['angles'].values():
    nc,ns,tc,ts=[[int(z,16) for z in entry[k]] for k in ('native_cos_hex','native_sin_hex','target_cos_hex','target_sin_hex')]
    error=max(abs(nc[0]-tc[1]),abs(nc[1]-tc[0]))+max(abs(ns[0]-ts[1]),abs(ns[1]-ts[0]))
    assert error==int(entry['operator_error_L1_numerator_hex'],16) and error<=1<<(precision-3264)
X=lib['controlled_X_power'];assert int(X['X_error_L1_numerator_hex'],16)<=1<<(precision-3264)

# Audit every emitted sector binding without traversing billions of masks.
lay=n.layout();readonly=set(lay['SAM']+lay['address']+[lay['branch']]);protected=set(lay['choi_input']+[lay['oldRIGHT_witness']])
sector_checks=0;units_checked=0;maxK=0;examples=[]
for bank,rows in lib['catalogue'].items():
    for row in rows:
        units=n.sector_units(row,lib,lay);rev=n.sector_units(row,lib,lay,reverse=True)
        assert rev==[(b,depth+1) for b,depth in reversed(units)]
        assert len(units)-1<=26
        for bound,depth in units:
            wires={*bound['controls'],bound['target'],lay['port'],*lay['spin']}
            assert len(wires)==bound['K']+4 and not wires&protected
            assert bound['target'] not in readonly
            assert not any(g['wires'][-1] in readonly or set(g['wires'])&protected for g in bound['permutation'])
            assert lay['branch'] in bound['controls'] and bound['pattern'][bound['controls'].index(lay['branch'])]==1
            assert bound['K']<=20;maxK=max(maxK,bound['K']);units_checked+=1
        if len(examples)<2 and (not examples or bool(row['SAM_indices'])):examples.append(row)
        sector_checks+=1
assert sector_checks==14848 and maxK==20
assert n.inventory(lib)==plan['banks']

# Independent leaf-by-leaf inverse, including inverse of a previously paid
# inverse. Small k is for exact word structure; actual k remains certified.
def inverse_word(word,port,spin):
    out=[]
    def cx(a,b):return {'op':'CX','wires':[a,b]}
    src={'op':'SourceI','wires':[port,*spin]}
    for g in reversed(word):
        if g['op']=='CX':out.append(g)
        elif g['op']=='SourceI':out.extend([g,g,g])
        else:
            q=g['wires'][0];swap=[] if q==port else [cx(q,port),cx(port,q),cx(q,port)]
            out.extend([*swap,src,src,{'op':'G','wires':[port]},src,src,*swap])
    return out
small={'K':3,'controls':[1,2,3],'pattern':[1,0,1],'target':0,'k':1,'permutation':[n.nb.gate('CX',0,1)]}
slay={'port':4,'spin':[5,6]};previous=None;depths=[]
for depth in range(3):
    blocks=list(n.unit_blocks(small,depth,slay));word=[g for b in blocks for g in n.nb.expand(b,100000)]
    if previous is not None:assert word==inverse_word(previous,4,[5,6])
    counter=Counter()
    for b in blocks:counter.update(n.prefix.resource(b,4))
    assert +counter==+n.unit_counts(small,depth)
    previous=word;depths.append({'literal_inverse_depth':depth,'actual_small_word_leaves':len(word)})
# First masks of genuinely bound large powers, with original protected wires.
large_blocks=0
for row in examples:
    for bound,depth in n.sector_units(row,lib,lay):
        for block in islice(n.unit_blocks(bound,depth,lay),5):
            n.nb.validate_schema(block,lay['qubits'],lay['port'],tuple(lay['spin']),tuple(protected))
            for leaf in n.nb.leaves(block):
                if leaf['op'] in ('G','CX'):assert leaf['wires'][-1] not in readonly
            large_blocks+=1
out={'status':'PASS_SOURCE_BOUND_NATIVE_COFRAME_SELECT','library_sha256':h(P/'COFRAME_ANGLE_LIBRARY.json'),'plan_sha256':h(P/'COFRAME_NATIVE_PLAN.json'),
     'checker_sha256':h(Path(__file__)),'B25_arbitrary_precision_source_diagnostics':target_checks,'full32_matrix_diagnostics':matrix_checks,
     'max_float_matrix_difference':maximum,'all_sectors_checked':sector_checks,'all_bound_units_checked':units_checked,
     'maximum_controls':maxK,'literal_inverse_depth_checks':depths,'sampled_actual_large_power_blocks':large_blocks,
     'per_macro_error_le':'2^-3264','full_coframe_SELECT_error_lt':'2^-3259','private_clean_work':0,
     'full_huge_native_word_executed':False,'proper_link_SELECT_compiled':False,'full_Omega_loader_compiled':False,
     'physical_C_closed':False,'GR_closed':False}
(P/'COFRAME_NATIVE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','all_sectors_checked','all_bound_units_checked','maximum_controls']}))
