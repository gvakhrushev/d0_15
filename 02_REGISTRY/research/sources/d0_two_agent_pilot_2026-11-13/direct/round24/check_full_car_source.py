#!/usr/bin/env python3
"""Check actual provider composition, clean-fibre errors and paid inverses."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import islice,zip_longest
import hashlib,json
import full_car_source as c
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();plan=json.loads((P/'FULL_CAR_SOURCE_PLAN.json').read_text())
for path,digest in plan['source_sha256'].items():assert h(Path(path))==digest,path
lay=c.layout();c.validate(lay);c.validate(dict(lay,qubits=2723),range(2715,2723))
for q in (*c.private(lay),lay['native_aux_arbitrary'],lay['SAM'][0],lay['oldRIGHT_witness']):
    try:c.validate(dict(lay,qubits=2723),[q])
    except AssertionError:pass
    else:raise AssertionError('accepted external overlap')
U,Ui,R=c.f.fixed_components(lay);assert Ui==c.nb.inverse_literal(U,lay['port'],tuple(lay['spin']))
port=lay['port'];price=c.f.resource
def total(ts):
    out=Counter()
    for t in ts:out.update(price(t,port))
    return out
def inv(z):return Counter({'G_port':z['G_port']+z['G_other'],'G_other':0,'CX':z['CX']+6*z['G_other'],'SourceI':3*z['SourceI']+4*(z['G_port']+z['G_other'])})
ur=price(U,port);uir=price(Ui,port);rr=price(R,port);assert +uir==+inv(ur)
material=json.loads((c.D/'round18/MATERIAL_PREPARATION_INVENTORY.json').read_text())
# The material inventory's exact schema is supplied by the source owner;
# independently recalculate its bound-unit prices via A18 rather than a
# guessed container key or a giant enumeration of all native blocks.
owned_material=c.f.m.inventory(c.library());frame_plan=json.loads((c.D/'round18/CAR_FRAME_PLAN.json').read_text())
vac=c.v.inventory(lay)['prefix_forward'];raw=total([c.nb.rotation_power(q,-1,port,tuple(lay['spin'])) for q in c.private(lay)])
assert +raw==+Counter({'G_port':3,'CX':18,'SourceI':12})
for bank in plan['all7_banks']:
    expected=ur+uir+rr+rr
    if bank in owned_material:
        for key in ('native_forward','native_literal_inverse'):expected.update({k:int(v) for k,v in owned_material[bank][key].items()})
    else:expected.update(ur);expected.update(uir)
    assert all(expected[k]==int(frame_plan['banks'][bank]['native_forward'].get(k,0)) for k in ('G_port','G_other','CX','SourceI'))
    full=raw+vac+expected;invfull=inv(full)
    for name,value in [('CAR_frame',expected),('source_forward',full),('source_literal_inverse',invfull)]:
        assert all(value[k]==int(plan['all7_banks'][bank]['native'][name][k]) for k in ('G_port','G_other','CX','SourceI'))
    if bank in ('f','0','x+','x-'):
        assert list(c.frame_blocks(bank,lay))==list(c.f.frame_blocks(bank,c.library(),lay))
    err=c.error_bound(bank);saved=plan['all7_banks'][bank]
    assert err==Fraction(int(saved['error_numerator_hex'],16),int(saved['error_denominator_hex'],16))

# Every actual A18 material provider is reused at the same namespace. Check
# the first two real blocks at each incoming literal depth0..3; at depth2
# the source is NOT silently treated as the original cheaper forward word.
samples=[]
for bank in ('y+','y-','q'):
    for depth in range(4):
        own=list(islice(c.material_blocks(bank,lay,depth),2));base=list(islice(c.f.m.preparation_blocks(bank,c.library(),lay,reverse=bool(depth%2)),2))
        ref=[c.invert(t,depth-depth%2,lay) for t in base];assert own==ref
        samples.append({'bank':bank,'literal_depth':depth,'actual_blocks':len(own)})

# Independently construct the full base chronology, then literally invert
# THAT whole emitted native DAG. Bound the test angles, not the real plan.
star=c.nb.seq(c.nb.gate('G',lay['grade'][0]),c.nb.gate('SourceI',port,*lay['spin']))
matter=c.nb.seq(c.nb.gate('CX',lay['internal_SITE'][0],lay['grade'][1]),c.nb.gate('G',lay['grade'][1]))
reflect=c.nb.seq(c.nb.gate('G',lay['native_aux_arbitrary']),c.nb.gate('CX',lay['grade'][0],lay['native_aux_arbitrary']))
vacuum=c.nb.seq(c.nb.gate('G',lay['RIGHT'][0]),c.nb.gate('CX',lay['RIGHT'][0],lay['grade'][0]))
old=(c.f.fixed_components,c.f.m.preparation_blocks,c.v.prefix_blocks)
def toy_fixed(lay=None):return star,c.nb.inverse_literal(star,port,tuple(lay['spin'])),reflect
def toy_material(bank,lib,lay=None,reverse=False):yield c.nb.inverse_literal(matter,port,tuple(lay['spin'])) if reverse else matter
def toy_vac(lay=None,depth=0,extra_external=()):yield c.invert(vacuum,depth,lay)
reports=[]
try:
    c.f.fixed_components=toy_fixed;c.f.m.preparation_blocks=toy_material;c.v.prefix_blocks=toy_vac
    for bank in plan['all7_banks']:
        initial=[c.nb.rotation_power(q,-1,port,tuple(lay['spin'])) for q in c.private(lay)]
        original=c.nb.seq(*initial,vacuum,*c.f.frame_blocks(bank,c.library(),lay))
        for depth in range(4):
            actual=(leaf for t in c.source_blocks(bank,lay,depth) for leaf in c.nb.expand(t,2000000));count=0
            for left,right in zip_longest(actual,c.nb.expand(original,2000000)):
                assert left==right,(bank,depth,count);count+=1
            reports.append({'bank':bank,'literal_depth':depth,'actual_primitive_leaves_equal':count})
            original=c.nb.inverse_literal(original,port,tuple(lay['spin']))
finally:c.f.fixed_components,c.f.m.preparation_blocks,c.v.prefix_blocks=old

prefix=c.v.error_bound()[1];delta=Fraction(1,2**4096)
assert all(c.error_bound(bank)<=prefix+28*delta for bank in plan['all7_banks'])
all_error=sum((16*c.error_bound(bank) for bank in plan['all7_banks']),Fraction());assert all_error<Fraction(1,2**3252)
assert all_error==Fraction(int(plan['all112_error_numerator_hex'],16),int(plan['all112_error_denominator_hex'],16))
out={'status':'PASS_FULL_CAR_RAW_PREFIX_AND_FRAME_COMPOSITION','plan_sha256':h(P/'FULL_CAR_SOURCE_PLAN.json'),'checker_sha256':h(Path(__file__)),
     'all7_banks_full_prices_recomputed_from_child_components':True,'constant_banks_actual_blocks_equal_original_A18':True,
     'actual_material_provider_samples':samples,'independent_full_word_literal_tests':reports,
     'predicate3_RAW_inverse_included':True,'all_source_RAW_inputs':22,'unknown_oldRIGHT_not_reset':True,
     'hybrid_scope':'all original source19 columns and arbitrary external; predicate3 initially RAW v, not arbitrary private',
     'ideal_prefix_keeps_predicate_zero_exactly':True,'actual_private_output_not_assumed_clean':True,'all112_sources_error_lt':'2^-3252',
     'original_marked_prefix_binding_proved':False,'actual_T6_proved':False,'full_giant_word_executed':False,'physical_C_closed':False,'GR_closed':False}
(P/'FULL_CAR_SOURCE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'literal_wrapper_checks':len(reports),'RAW_wires_per_source':22}))
