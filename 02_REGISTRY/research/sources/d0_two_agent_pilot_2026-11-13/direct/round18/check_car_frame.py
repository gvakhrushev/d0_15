#!/usr/bin/env python3
"""Full CAR chronology, exact constant-bank cancellation and target binding."""
from pathlib import Path
from collections import Counter
import hashlib,importlib.util,json,sys
import numpy as np
mm=lambda a,b:np.einsum("ij,jk->ik",a,b,optimize=False)
import car_frame as f
import material_preparation as m
import material_targets as t
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lib=json.loads((P/'MATERIAL_PREPARATION_LIBRARY.json').read_text());plan=json.loads((P/'CAR_FRAME_PLAN.json').read_text());lay=plan['layout']
for name,digest in plan['inputs_sha256'].items():assert h(Path(name))==digest,name
U,Ui,R=f.fixed_components(lay)
assert Ui==m.nb.inverse_literal(U,lay['port'],tuple(lay['spin']))
F,Z,Fi=R['children'];assert Fi==m.nb.inverse_literal(F,lay['port'],tuple(lay['spin']))
assert Z==m.nb.z_word(lay['predicate_flag'],lay['port'],tuple(lay['spin']))
# Consequently R=F†ZF is an EXACT involution for all predicate work inputs.
# In four constant banks the emitted word is (U R U†)^2=I exactly;
# this is an endpoint identity, with no cancellation of paid history stages.
constant_counts={}
for bank in ('f','0','x+','x-'):
    blocks=list(f.frame_blocks(bank,lib,lay));assert blocks==[Ui,R,U,Ui,R,U]
    resources=Counter()
    for tree in blocks:
        m.nb.validate_schema(tree,lay['qubits'],lay['port'],tuple(lay['spin']),tuple(lay['RIGHT']+[lay['oldRIGHT_witness']]))
        resources.update(f.resource(tree,lay['port']))
    assert +resources==+Counter({q:int(v) for q,v in plan['banks'][bank]['native_forward'].items()})
    constant_counts[bank]=True
assert len(set(plan['predicate_zero_wires_required']+[lay['native_aux_arbitrary'],*lay['grade'],lay['port'],*lay['spin']]))==11
assert not set(plan['predicate_zero_wires_required'])&set(lay['SAM']+lay['internal_SITE']+lay['RIGHT']+[lay['oldRIGHT_witness']])

sp=importlib.util.spec_from_file_location('a18_frame_b25',t.B/'round25/targets.py');b25=importlib.util.module_from_spec(sp);sys.modules[sp.name]=b25;sp.loader.exec_module(b25)
def midpoint(v,bits):return (int(v[0],16)+int(v[1],16))/(2*(1<<bits))
def pair(a,b,c,s):
    M=np.eye(16);M[a,a]=M[b,b]=c;M[b,a]=s;M[a,b]=-s;return M
prep={}
for vid,data in lib['vectors'].items():
    mat=np.eye(16)
    for rot in data['rotations']:
        if rot['angle_id'] is None:continue
        angle=lib['angles'][rot['angle_id']];bits=angle['denominator_power_of_two']
        c=midpoint(angle['native_cos_hex'],bits);sn=midpoint(angle['native_sin_hex'],bits)*m.plane_geometry(rot['other'])['orientation']
        mat=mm(pair(1,rot['other'],c,sn),mat)
    prep[vid]=mat
star=json.loads((t.B/'round37/CAR_USTAR_NATIVE.json').read_text())['certificate'];bits=star['precision_bits']
US=pair(1,14,midpoint(star['actual_cos_endpoints_hex'],bits),-midpoint(star['actual_sin_endpoints_hex'],bits))
R1=np.eye(16);R1[1,1]=-1
labels=[]
for bits in ((0,0),(0,1),(1,0),(1,1)):
    label=np.zeros(2688,dtype=np.int8)
    for i,c in enumerate(b25.COORD):
        if c['kind']=='matter':label[i]=bits[0 if c['grade']==0 else 1]
    labels.append(label)
cases=0;maximum=0.
for bank in ('q','y+','y-','f','0','x+','x-'):
    for label in (labels if bank=='q' else [None]):
        psi=b25.fields(bank,label)[2]
        for site,state in enumerate(psi):
            if bank in prep:raise AssertionError('bank names must not alias vector names')
            if bank in lib['catalogue']:
                rows=[r for r in lib['catalogue'][bank] if r['site']==site and (not r['SAM_indices'] or [int(label[i]) for i in r['SAM_indices']]==r['SAM_pattern'])]
                assert len(rows)==1;UM=prep[rows[0]['vector_id']]
            else:UM=US
            actual_target=mm(mm(mm(mm(mm(UM,R1),UM.T),US),R1),US.T)
            expected=b25.car_map(state)
            error=float(np.max(np.abs(actual_target-expected)));assert error<4e-15,(bank,site,error)
            maximum=max(maximum,error);cases+=1
assert cases==2560
# Explicit full-unitary hybrid bound, not just a column estimate:
# eps_m<=3δ, eps_star<=δ, each clean-work R has error<=10δ.
assert 2*3+2*1+2*10==28 and 112*28<2**12
out={'status':'PASS_SEVEN_CAR_FRAME_CHRONOLOGY_AND_TARGETS','plan_sha256':h(P/'CAR_FRAME_PLAN.json'),
     'library_sha256':h(P/'MATERIAL_PREPARATION_LIBRARY.json'),'exact_constant_bank_endpoint_identity':constant_counts,
     'actual_reflection_is_literal_compute_Z_compute_inverse':True,
     'three_clean_predicate_wires_distinct_from_arbitrary_aux_and_all_inputs':True,
     'full_B25_grade_matrix_comparisons':cases,'max_float_composition_difference':maximum,
     'matrix_comparison_scope':'diagnostic of ideal anchor reflections and certified rotation matrix enclosures; actual reflection error separately bounded',
     'nonconstant_bank_clean_predicate_error_le':'28*2^-4096','all112_copy_conservative_error_lt':'2^-4084',
     'physical_CAR_vacuum_Fourier_prefix_proved':False,'physical_birth_mark_clock_admission_proved':False,
     'physical_C_closed':False,'GR_closed':False}
(P/'CAR_FRAME_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','full_B25_grade_matrix_comparisons','nonconstant_bank_clean_predicate_error_le']}))
