#!/usr/bin/env python3
"""Check target binding, all local SAM sectors, full DATA columns and counts."""
from pathlib import Path
from collections import Counter
import hashlib,importlib.util,json,sys
import numpy as np
mm=lambda a,b:np.einsum("ij,jk->ik",a,b,optimize=False)
import material_targets as t
import material_preparation as m
P=Path(__file__).resolve().parent
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
lib=json.loads((P/'MATERIAL_PREPARATION_LIBRARY.json').read_text())
for f,digest in lib['input_sha256'].items():assert h(Path(f))==digest,f
assert h(P/'certify_material_preparation.py')==lib['source_sha256']
assert lib['catalogue']==t.catalogue()
precision=lib['precision_bits'];scale=1<<precision
def midpoint(bounds):return (int(bounds[0],16)+int(bounds[1],16))/(2*scale)
def vector(vid):
    out=np.zeros(16)
    for q,v in lib['vectors'][vid]['half_vector_bounds_hex'].items():out[int(q)]=midpoint(v)
    return out

# Binding to the independently owned B25 float evaluator is a diagnostic;
# the full-SAM conclusion follows from the explicit local-coordinate formula.
sp=importlib.util.spec_from_file_location('a18_b25_targets',t.B/'round25/targets.py')
b25=importlib.util.module_from_spec(sp);sys.modules[sp.name]=b25;sp.loader.exec_module(b25)
labels=[]
for bits in ((0,0),(0,1),(1,0),(1,1)):
    label=np.zeros(2688,dtype=np.int8)
    for i,c in enumerate(b25.COORD):
        if c['kind']=='matter':label[i]=bits[0 if c['grade']==0 else 1]
    labels.append(label)
anchor=np.eye(16)[:,1];den=np.sqrt(2*(1+np.sqrt(b25.PVAL)))
matches=set();max_target_error=0.0;target_cases=0
for bank in ('q','y+','y-'):
    for label in (labels if bank=='q' else [None]):
        fields=b25.fields(bank,label)[2]
        for site,psi in enumerate(fields):
            candidates=[r for r in lib['catalogue'][bank] if r['site']==site and (not r['SAM_indices'] or [int(label[i]) for i in r['SAM_indices']]==r['SAM_pattern'])]
            assert len(candidates)==1
            row=candidates[0];v=vector(row['vector_id']);expected=(anchor+b25.local_m(psi))/den
            error=float(np.max(np.abs(v-expected)));assert error<2e-15,error
            max_target_error=max(max_target_error,error);target_cases+=1
            matches.add((bank,site,tuple(row['SAM_pattern'])))
assert len(matches)==960
for name,rows in lib['catalogue'].items():
    assert all(set(row['SAM_indices']).issubset({i for i,c in enumerate(b25.COORD) if c['kind']=='matter'}) for row in rows)
    for site in range(256):
        rr=[r for r in rows if r['site']==site]
        assert len(rr) in (1,4)
        if len(rr)==4:assert sorted(r['SAM_pattern'] for r in rr)==[[0,0],[0,1],[1,0],[1,1]]

# Each emitted planar block acts on precisely two full 4-bit grade columns.
# Multiply their actual enclosed native rotations and compare to the named
# vector. This is NOT expansion of the huge native word; angle certificates
# establish its distance to these full-matrix targets.
max_prep=0.;full_column_cases=0
for vid,data in lib['vectors'].items():
    U=np.eye(16)
    for rotation in data['rotations']:
        if rotation['angle_id'] is None:continue
        g=m.plane_geometry(rotation['other']);C=np.eye(16)
        for target in g['flips']:
            gate=np.zeros((16,16))
            for x in range(16):gate[x^(((x>>g['pivot'])&1)<<target),x]=1
            C=mm(gate,C)
        assert np.array_equal(mm(C,C),np.eye(16))
        angle=lib['angles'][rotation['angle_id']];c=midpoint(angle['native_cos_hex']);s=midpoint(angle['native_sin_hex'])
        R=np.eye(16)
        for x in range(16):
            if all(((x>>j)&1)==bit for j,bit in zip(g['grade_controls'],g['grade_pattern'])):
                y=x^(1<<g['pivot']);R[x,x]=c;R[y,x]=-s if (x>>g['pivot'])&1 else s
        U=mm(mm(mm(C.T,R),C),U)
        # The basis-conjugated support is precisely {1,other}.
        pair=mm(mm(C.T,R),C)
        for x in set(range(16))-{1,rotation['other']}:assert np.array_equal(pair[:,x],np.eye(16)[:,x])
    error=float(np.linalg.norm(U[:,1]-vector(vid)));assert error<2e-15
    assert np.max(np.abs(mm(U.T,U)-np.eye(16)))<2e-15
    max_prep=max(max_prep,error);full_column_cases+=16

# Every retained certificate is a strict rational interval inequality. Native
# powering is independently rechecked by B review, not duplicated here.
for name,a in lib['angles'].items():
    assert a['denominator_power_of_two']==precision and a['certified_error_bits']==4096
    c=[int(x,16) for x in a['target_cos_hex']];s=[int(x,16) for x in a['target_sin_hex']]
    nc=[int(x,16) for x in a['native_cos_hex']];ns=[int(x,16) for x in a['native_sin_hex']]
    assert all(x[0]<=x[1] for x in [c,s,nc,ns])
    error=max(abs(nc[0]-c[1]),abs(nc[1]-c[0]))+max(abs(ns[0]-s[1]),abs(ns[1]-s[0]))
    assert error==int(a['operator_error_L1_numerator_hex'],16) and error<=2**(precision-4096)

# Actual native grammar bindings/counts, with both all-zero and nonzero
# predicates and a real 13-control SAM/site plane. OldRIGHT and CAR RIGHT
# are protected; no SAM/SITE control becomes a target, even temporarily.
lay=lib['layout'];examples=[];immutable_controls=set(lay['SAM']+lay['internal_SITE'])
for name,row in [('q',lib['catalogue']['q'][0]),('q',next(r for r in lib['catalogue']['q'] if r['SAM_indices']))]:
    for rotation in lib['vectors'][row['vector_id']]['rotations']:
        if rotation['angle_id'] is not None:examples.append(m.bind_plane(row,rotation,lay,lib['angles']))
sampled_blocks=0;primitive_leaves=0
def resources(tree):
    if tree['op']=='seq':
        out=Counter()
        for child in tree['children']:out.update(resources(child))
        return out
    if tree['op']=='repeat':return Counter({k:int(tree['count'])*v for k,v in resources(tree['child']).items()})
    if tree['op']=='G':return Counter({'G_port' if tree['wires'][0]==lay['port'] else 'G_other':1})
    return Counter({tree['op']:1})
for bound in examples:
    forward=Counter();inverse=Counter();protected=tuple(lay['RIGHT']+[lay['oldRIGHT_witness']])
    for block in m.pair_blocks(bound,lay):
        m.nb.validate_schema(block,lay['qubits'],lay['port'],tuple(lay['spin']),protected)
        for leaf in m.nb.leaves(block):
            if leaf['op'] in ('G','CX'):assert leaf['wires'][-1] not in immutable_controls
            primitive_leaves+=1
        forward.update(resources(block));sampled_blocks+=1
    for block in m.pair_blocks(bound,lay,True):inverse.update(resources(block))
    assert +forward==+m.pair_counts(bound)
    assert +inverse==+m.raw_inverse_counts(forward)
assert m.inventory(lib)==json.loads((P/'MATERIAL_PREPARATION_INVENTORY.json').read_text())['banks']
out={'status':'PASS_MATERIAL_TARGET_BINDING_AND_NATIVE_PREPARATION_GRAMMAR',
     'library_sha256':h(P/'MATERIAL_PREPARATION_LIBRARY.json'),'checker_sha256':h(Path(__file__)),
     'all_covered_local_control_sectors':len(matches),'B25_target_comparisons':target_cases,
     'max_B25_target_error_float_diagnostic':max_target_error,'full_grade_matrix_columns_checked':full_column_cases,
     'max_compiled_rotation_preparation_error_float_diagnostic':max_prep,
     'rational_angle_certificates_checked':len(lib['angles']),'actual_native_pair_examples':len(examples),
     'actual_native_blocks_checked':sampled_blocks,'actual_primitive_leaves_checked':primitive_leaves,
     'full_native_expanded_word_executed':False,'private_quantum_work':0,
     'all_SAM_statement_reason':'the owned material formula has exactly two local matter coordinates per free site; every local assignment is covered, and all other input bits are unaddressed by this map',
     'physical_birth_admission_proved':False,'full_CAR_vacuum_Fourier_preparation_emitted':False,
     'physical_C_closed':False,'GR_closed':False}
(P/'MATERIAL_PREPARATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','all_covered_local_control_sectors','rational_angle_certificates_checked','actual_native_blocks_checked']}))
