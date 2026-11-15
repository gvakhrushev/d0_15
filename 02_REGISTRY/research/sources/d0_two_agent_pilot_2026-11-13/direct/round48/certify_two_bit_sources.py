#!/usr/bin/env python3
"""Full local four-valued coframe and CAR libraries, not samples."""
from pathlib import Path
from hashlib import sha256
import json,sys
sys.dont_write_bytecode=True
import two_bit_source_targets as t
from source_angle_certifier import Certifier,save_gzip
prep=t.load('a48_old_pair_geometry',t.D/'round18/material_preparation.py')
P=Path(__file__).resolve().parent


def pin_inputs():
    files=[Path(__file__),P/'two_bit_source_targets.py',P/'source_angle_certifier.py',
      t.D/'round20/coframe_targets.py',t.D/'round18/material_targets.py',
      t.D/'round19/coframe_factorization.py',t.D/'round19/julia_locality.py',
      t.loc.COORD_PATH,t.loc.ADDR_PATH,t.cf.PF_PATH,t.loc.B/'round21/REFERENCE_METADATA.json']
    return {str(p):sha256(p.read_bytes()).hexdigest() for p in files}


def coframe():
    cert=Certifier(24);iv=cert.iv;c=cert.c;specs,templates,multiplicity=t.coframe_catalogue();families={}
    for n,(name,spec) in enumerate(specs.items(),1):
        v=t.coframe_vector(iv,c,spec);f=t.cf.factors(iv,v,spec)
        refs=[{'factor':list(key),'angle_id':cert.certify(cc,ss)} for key,cc,ss in t.cf.native_angle_targets(iv,f)]
        families[name]={'spec':spec,'chosen_elimination_order':f['chosen_elimination_order'],
          'mode_rotations':[{'mode':r['mode'],'exact_identity':r['exact_identity']} for r in f['mode_rotations']],
          'angle_bindings':refs}
        if n%64==0:print(json.dumps({'kind':'coframe','families':n,'total_families':len(specs),'angles':len(cert.records)}),flush=True)
    controlled=cert.controlled_x()
    result=cert.metadata();result.update({'status':'CERTIFIED_COMPLETE_TWO_BIT_COFRAME_TARGET_LIBRARY',
      'source_sha256':pin_inputs(),'sampler_stride':'2^-80','CODE_bits':5376,
      'families':families,'controlled_X_power':controlled,'catalogue_templates':templates,
      'family_multiplicity':{bank:dict(counts) for bank,counts in multiplicity.items()},
      'all_local_assignments_included':True,'sector_count':sum(sum(c.values()) for c in multiplicity.values()),
      'native_emitter_integrated':False,'new_full_SOURCE_compiled':False,'physical_C_closed':False,'GR_closed':False})
    path=P/'TWO_BIT_COFRAME_LIBRARY.json.gz';save_gzip(path,result)
    print(json.dumps({'status':result['status'],'families':len(families),'angles':len(cert.records),'sectors':result['sector_count'],'bytes':path.stat().st_size}),flush=True)


def material():
    cert=Certifier(15);iv=cert.iv;c=cert.c;vectors={}
    for spec in t.material_specs():
        v,psi=t.material_half_vector(iv,c,spec);rows=[]
        for r in t.mat.rotations(iv,v):
            geometry=prep.plane_geometry(r['other']);cc,ss=r['cos'],r['sin']
            if ss==(0,0):
                assert cc[0]<=iv.scale<=cc[1]
                rows.append({'other':r['other'],'angle_id':None});continue
            if geometry['orientation']==-1:ss=iv.neg(ss)
            rows.append({'other':r['other'],'angle_id':cert.certify(cc,ss)})
        vectors[spec['id']]={'spec':spec,'rotations':rows}
    result=cert.metadata();result.update({'status':'CERTIFIED_COMPLETE_TWO_BIT_CAR_HALF_VECTOR_LIBRARY',
      'source_sha256':pin_inputs(),'sampler_stride':'2^-80','CODE_bits':5376,
      'vectors':vectors,'catalogue':t.material_catalogue(),'all_local_assignments_included':True,
      'native_emitter_integrated':False,'new_full_SOURCE_compiled':False,'physical_C_closed':False,'GR_closed':False})
    path=P/'TWO_BIT_MATERIAL_LIBRARY.json.gz';save_gzip(path,result)
    print(json.dumps({'status':result['status'],'vectors':len(vectors),'angles':len(cert.records),'bytes':path.stat().st_size}),flush=True)


if __name__=='__main__':
    assert len(sys.argv)==2 and sys.argv[1] in ('coframe','material')
    globals()[sys.argv[1]]()
