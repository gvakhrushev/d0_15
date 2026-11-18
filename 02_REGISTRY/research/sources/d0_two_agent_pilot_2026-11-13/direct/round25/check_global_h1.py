#!/usr/bin/env python3
"""Check global chronology, real bindings and literal reversal at every slot.

Opaque huge source/report providers are replaced ONLY in the whole-word
fixture by short pieces of their actual forward words and their literal
inverses. Full SC6 is kept. This tests integration, not giant-source execution.
"""
from pathlib import Path
from collections import Counter
import hashlib,itertools,json
import global_h1 as g
P=Path(__file__).resolve().parent
def take(word,n):return list(itertools.islice(word,n))
def literal(blocks,depth,plan):
    for _ in range(depth):blocks=[g.invert(t,1,plan) for t in reversed(blocks)]
    return blocks
def main():
    plan=g.namespace();l=plan['layout'];schedule=g.stages(plan)
    # Reconstruct chronology independently from the input contract.
    expected=[{'kind':'SITE'}]
    for i,bank in enumerate(g.ns.BANKS):
        expected.append({'kind':'SIGMA','report':i})
        ids=[j for j,s in enumerate(plan['source_slots']) if s['bank']==bank]
        assert ids==plan['reports'][i]['source_slots'] and len(ids)==196
        expected.extend({'kind':'SOURCE','slot':j} for j in ids)
        expected.append({'kind':'REPORT','report':i})
    expected.extend([{'kind':'PORT_ZERO'},{'kind':'SC6'}]);assert schedule==expected and len(schedule)==1389
    # Every actual namespace is accepted, not just the first copy.
    for slot in plan['source_slots']:
        if slot['kind']=='Choi':g.choi.validate(g.ns.choi_layout(plan,slot))
        else:g.car.validate(g.ns.car_layout(plan,slot))
    g.site.validate(g.ns.site_layout(plan))
    # Compare the complete real SC6 stream at its actual global binding.
    sc=list(g.stage_blocks({'kind':'SC6'},plan));assert len(sc)==18176
    sc_counts=Counter()
    for t in sc:
        sc_counts.update(g.native_count(t,l['port']))
        assert l['aux_arbitrary'] not in t['wires'] and l['oldRIGHT_witness'] not in t['wires']
        assert not set(l['SAM']).intersection(t['wires'])
    assert sc_counts==Counter({'G_port':5888,'CX':4096,'SourceI':8192})
    for depth in (1,2,3):assert list(g.stage_blocks({'kind':'SC6'},plan,depth))==literal(sc,depth,plan)
    # Provider samples use real addresses and real giant k, but bounded blocks.
    original={'choi':g.choi.raw_prepared_blocks,'car':g.car.source_blocks,
              'site':g.site.site_blocks,'report':g.report.report_blocks}
    source_cache={};source_samples=0
    for slot in plan['source_slots']:
        kind=slot['kind'];lay=g.ns.choi_layout(plan,slot) if kind=='Choi' else g.ns.car_layout(plan,slot)
        key=(kind,slot['bank'],lay['branch'] if kind=='Choi' else lay['predicate_flag'])
        provider=original['choi' if kind=='Choi' else 'car']
        source_cache[key]=take(provider(slot['bank'],lay,0),2);source_samples+=2
    site_sample=take(original['site'](g.site_library(),g.ns.site_layout(plan),0),4)
    report_sample=take(original['report'](plan['local_report'],g.boolean_k(),0),2)
    def ch(bank,lay,depth=0,extra_external=()):yield from literal(source_cache[('Choi',bank,lay['branch'])],depth,plan)
    def ca(bank,lay,depth=0,extra_external=()):yield from literal(source_cache[('CAR',bank,lay['predicate_flag'])],depth,plan)
    def si(lib,lay=None,depth=0):yield from literal(site_sample,depth,plan)
    def rp(local,k,depth=0):
        # Native inverse uses the LOCAL port before the real global remap.
        blocks=report_sample
        for _ in range(depth):blocks=[g.nb.inverse_literal(t,local['native_port'],tuple(local['native_spin'])) for t in reversed(blocks)]
        yield from blocks
    g.choi.raw_prepared_blocks=ch;g.car.source_blocks=ca;g.site.site_blocks=si;g.report.report_blocks=rp
    fixture=[]
    try:
        forward=[]
        # Independent explicit order, with the actual integration dispatcher.
        for stage in expected:forward.extend(g.stage_blocks(stage,plan))
        assert list(g.A_blocks(plan))==forward
        for depth in (1,2,3):
            assert list(g.A_blocks(plan,depth))==literal(forward,depth,plan)
            fixture.append({'A_literal_depth':depth,'native_blocks':len(forward)})
        central=g.nb.z_word(l['port'],l['port'],tuple(l['spin']))
        w=forward+[central]+literal(forward,1,plan)
        assert list(g.W_blocks(plan))==w
        for depth in (1,2):
            assert list(g.W_blocks(plan,depth))==literal(w,depth,plan)
            fixture.append({'W_literal_depth':depth,'native_blocks':len(w)})
    finally:
        g.choi.raw_prepared_blocks=original['choi'];g.car.source_blocks=original['car'];g.site.site_blocks=original['site'];g.report.report_blocks=original['report']
    components,a,ai,wc=g.inventory(plan)
    assert ai==g.inverse_counts(a) and wc==a+Counter({'SourceI':2})+ai
    for n in range(1,4):
        native=Counter()
        for t in literal(sc,n,plan):native.update(g.native_count(t,l['port']))
        expect=sc_counts
        for _ in range(n):expect=g.inverse_counts(expect)
        assert +native==+expect
    parts,error=g.canonical_input_error();assert error>0 and error<g.Fraction(1,2**3232)
    # Exact real 2x2 lemma: symmetric [[a,b],[b,d]] commuting with J
    # gives [S,J] = [[2b,d-a],[d-a,-2b]], hence b=0,d=a.
    def matmul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    J=[[0,-1],[1,0]];cases=0
    for a0,b0,d0 in itertools.product(range(-3,4),repeat=3):
        s=[[a0,b0],[b0,d0]];sj=matmul(s,J);js=matmul(J,s)
        assert [[sj[i][j]-js[i][j] for j in range(2)] for i in range(2)]==[[2*b0,d0-a0],[d0-a0,-2*b0]]
        assert (sj==js)==(b0==0 and d0==a0);cases+=1
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    pins=[Path(__file__),P/'global_h1.py',P/'GLOBAL_H1_PLAN.json',P/'h1_namespace.py',P/'H1_NAMESPACE_PLAN.json',P/'reversible_report_stream.py']
    out={'status':'PASS_GLOBAL_BINDING_CHRONOLOGY_AND_LITERAL_REVERSE',
         'source_sha256':{str(p):sha(p) for p in pins},'all1389_stages_checked':True,'all1372_source_layouts_validated':True,
         'actual_source_sample_blocks':source_samples,'actual_SITE_sample_blocks':len(site_sample),
         'actual_local_report_sample_blocks':len(report_sample),'full_SC6_forward_leaves':len(sc),
         'full_SC6_literal_depths_checked':[1,2,3],'all_slot_integration_fixture':fixture,
         'full_huge_source_and_report_providers_replaced_only_in_fixture':True,
         'all_actual_giant_provider_streams_executed':False,'exact_2x2_commutant_identity_integer_checks':cases,
         'commutant_examples_not_a_substitute_for_provider_symmetry_proofs':True,
         'conditional_canonical_input_error_lt':'2^-3232','physical_births_marks_clock_admission':False,'physical_C_closed':False,'GR_closed':False}
    (P/'GLOBAL_H1_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','actual_source_sample_blocks','full_SC6_forward_leaves']}))
if __name__=='__main__':main()
