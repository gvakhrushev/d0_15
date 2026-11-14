#!/usr/bin/env python3
"""Concrete finite A and A;Z;A-dagger streams on the reviewed A25 binding.

Every inverse is a literal inverse of the emitted primitives, including
already-inverted internal words. Giant repeats/streams are not materialized.
This defines a native word, not its physical admission or old marked-history
equivalence. The namespace plan is a separately frozen upstream artifact.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib,importlib.util,json,sys
import h1_namespace as ns
import reversible_report_stream as report
P=Path(__file__).resolve().parent;D=P.parent;B=ns.B
sys.path.insert(0,str(D/'round22'));sys.path.insert(0,str(D/'round24'))
import full_choi_bank as choi
import full_car_source as car
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
site=load('a25_site',B/'round45/site_native.py');nb=report.nb
AXES=('G_port','G_other','CX','SourceI')
@lru_cache(maxsize=1)
def namespace():return json.loads((P/'H1_NAMESPACE_PLAN.json').read_text())
@lru_cache(maxsize=1)
def site_library():return site.library()
@lru_cache(maxsize=1)
def boolean_k():return int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k'])
@lru_cache(maxsize=1)
def sc6_word():
    word=[json.loads(line) for line in (B/'round21/SC6_FORWARD.jsonl').read_text().splitlines()]
    assert len(word)==18176 and Counter(z['op'] for z in word)=={'G':5888,'CX':4096,'SourceI':8192}
    return word
def stages(plan):
    """Actual forward chronology, including port conversion AFTER R_load."""
    out=[{'kind':'SITE'}]
    for ri,r in enumerate(plan['reports']):
        out.append({'kind':'SIGMA','report':ri})
        out.extend({'kind':'SOURCE','slot':si} for si in r['source_slots'])
        out.append({'kind':'REPORT','report':ri})
    out.extend([{'kind':'PORT_ZERO'},{'kind':'SC6'}]);return out
def invert(t,depth,plan):
    for _ in range(depth):t=nb.inverse_literal(t,plan['layout']['port'],tuple(plan['layout']['spin']))
    return t
def stage_blocks(stage,plan,depth=0):
    assert type(depth) is int and depth>=0
    kind=stage['kind'];g=plan['layout'];port=g['port'];spin=tuple(g['spin'])
    if kind=='SITE':yield from site.site_blocks(site_library(),ns.site_layout(plan),depth)
    elif kind=='SIGMA':
        r=plan['reports'][stage['report']];assert r['sigma_bit']==0 and r['sigma_sign']==-1
        yield invert(nb.rotation_power(r['sigma'],-1,port,spin),depth,plan)
    elif kind=='SOURCE':
        slot=plan['source_slots'][stage['slot']]
        if slot['kind']=='Choi':yield from choi.raw_prepared_blocks(slot['bank'],ns.choi_layout(plan,slot),depth)
        else:
            assert slot['kind']=='CAR';yield from car.source_blocks(slot['bank'],ns.car_layout(plan,slot),depth)
    elif kind=='REPORT':
        r=plan['reports'][stage['report']]
        for t in report.report_blocks(plan['local_report'],boolean_k(),depth):
            yield report.a.remap_native(t,lambda q:ns.report_wire(plan,r,q))
    elif kind=='PORT_ZERO':yield invert(nb.rotation_power(port,-1,port,spin),depth,plan)
    else:
        assert kind=='SC6';mapping=plan['SC6_local_to_global'];word=sc6_word()
        for t in (reversed(word) if depth%2 else word):
            yield invert(nb.gate(t['op'],*(mapping[q] for q in t['wires'])),depth,plan)
def A_blocks(plan=None,depth=0):
    plan=namespace() if plan is None else plan
    assert type(depth) is int and depth>=0
    schedule=stages(plan)
    for stage in (reversed(schedule) if depth%2 else schedule):yield from stage_blocks(stage,plan,depth)
def W_blocks(plan=None,depth=0):
    """Chronological A;Z_port;actual literal inverse A, with paid outer depth."""
    plan=namespace() if plan is None else plan
    assert type(depth) is int and depth>=0
    parts=[('A',0),('Z',0),('A',1)]
    for kind,intrinsic in (reversed(parts) if depth%2 else parts):
        if kind=='A':yield from A_blocks(plan,depth+intrinsic)
        else:yield invert(nb.z_word(plan['layout']['port'],plan['layout']['port'],tuple(plan['layout']['spin'])),depth,plan)
def inverse_counts(c):
    return Counter({'G_port':c['G_port']+c['G_other'],'G_other':0,'CX':c['CX']+6*c['G_other'],
                    'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
def times(c,n):return Counter({k:n*v for k,v in c.items()})
def native_count(t,port):
    op=t['op']
    if op=='seq':
        c=Counter()
        for z in t['children']:c.update(native_count(z,port))
        return c
    if op=='repeat':return times(native_count(t['child'],port),int(t['count']))
    return Counter({'G_port' if t['wires'][0]==port else 'G_other':1}) if op=='G' else Counter({op:1})
def inventory(plan):
    compilation=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
    components={'SITE':site.inventory(site_library(),ns.site_layout(plan))['SITE_forward'],
                'SIGMA7':Counter({'G_port':7,'CX':42,'SourceI':28}),
                'Choi1260':Counter(),'CAR112':Counter(),
                'REPORT7':times(Counter({k:int(v) for k,v in compilation['native_forward_resources'].items()}),7),
                'PORT_ZERO':Counter({'G_port':1,'SourceI':4}),'SC6':Counter({'G_port':5888,'CX':4096,'SourceI':8192})}
    for bank in ns.BANKS:
        components['Choi1260'].update(times(choi.inventory(bank)['RAW_prepared_forward'],180))
        components['CAR112'].update(times(car.inventory(bank)['source_forward'],16))
    total=Counter()
    for c in components.values():total.update(c)
    rev=inverse_counts(total);central=Counter({'SourceI':2})
    return components,total,rev,total+central+rev
def upper_power(e):
    assert e>0;n=e.denominator.bit_length()-e.numerator.bit_length()
    while e>=Fraction(1,2**n):n-=1
    while e<Fraction(1,2**(n+1)):n+=1
    return n
def encode_error(e):return {'numerator_hex':hex(e.numerator),'denominator_hex':hex(e.denominator),'strict_upper_bound':'2^-'+str(upper_power(e))}
def canonical_input_error():
    compilation=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
    parts={'Choi1260':1260*choi.errors()[2],
           'CAR112':sum((16*car.error_bound(bank) for bank in ns.BANKS),Fraction()),
           'SITE_once':18*Fraction(1,2**3264),
           'REPORT7':int(compilation['seven_report_all_known_approximate_macros'])*Fraction(1,2**4096),
           'SIGMA_PORT_SC6':Fraction(0)}
    return parts,sum(parts.values(),Fraction())
def main():
    plan=namespace();schedule=stages(plan);components,a,ai,w=inventory(plan);parts,error=canonical_input_error()
    encode=lambda c:{k:str(c[k]) for k in AXES};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    pins=[Path(__file__),P/'h1_namespace.py',P/'H1_NAMESPACE_PLAN.json',P/'reversible_report_stream.py',
          D/'round14/native_boolean.py',D/'round17/GLOBAL_REPORT_COMPILATION.json',D/'round22/FULL_CHOI_BANK_PLAN.json',
          D/'round24/FULL_CAR_SOURCE_PLAN.json',B/'round45/site_native.py',B/'round45/SITE_NATIVE_PLAN.json',B/'round21/SC6_FORWARD.jsonl']
    out={'status':'FINITE_GLOBAL_A_AND_LITERAL_W_NATIVE_GENERATOR',
         'source_sha256':{str(p):sha(p) for p in pins},'forward_stage_schedule':schedule,
         'forward_stage_counts':dict(Counter(s['kind'] for s in schedule)),
         'global_native_counts':{'components':{k:encode(c) for k,c in components.items()},'A_forward':encode(a),'A_literal_inverse':encode(ai),'W_literal_echo':encode(w)},
         'W_primitive_call_count_decimal':str(sum(w.values())),
         'W_primitive_call_count_bit_length':sum(w.values()).bit_length(),
         'WORK_RAW_birth_count':plan['WORK_RAW_birth_count'],'separate_SAM_RAW_births':2688,
         'birth_operations_are_declared_inputs_not_emitted_by_unitary_generator':True,
         'central_event_location':'after complete A, immediately before central Z on canonical active-port WORK',
         'port_G_inverse_after_all_R_load':True,'SITE_forward_occurrences':1,
         'all_required_original_source_mark_prefixes_transported':False,
         'literal_inverse_preserves_integer_depth':True,'giant_native_stream_enumerated':False,
         'error_scope':'canonical product RAW WORK input, all SAM labels/coherences and arbitrary protected external factor; not an all-helper-column estimate against the original T2 target',
         'conditional_canonical_input_error_components':{k:encode_error(v) if v else {'exact_zero':True} for k,v in parts.items()},
         'canonical_input_error_bound':encode_error(error),'compressed_reflection_error_bound':encode_error(2*error),
         'error_needs_ideal_product_source_and_A17_law_binding_review':True,
         'physical_T2_marked_map_identification':False,'physical_birth_stage_admission_proved':False,
         'complete_Book03_clock_work_source_computed':False,'physical_C_closed':False,'GR_closed':False}
    (P/'GLOBAL_H1_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'stage_count':len(schedule),'WORK_RAW_births':out['WORK_RAW_birth_count'],
                      'W_call_count_bits':out['W_primitive_call_count_bit_length'],'conditional_input_error':encode_error(error)['strict_upper_bound']}))
if __name__=='__main__':main()
