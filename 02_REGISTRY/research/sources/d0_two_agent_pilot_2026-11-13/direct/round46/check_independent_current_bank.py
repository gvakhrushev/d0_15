#!/usr/bin/env python3
"""Check fresh address ownership, literal depth, paid families and budgets."""
from pathlib import Path
from collections import Counter
from itertools import islice
import hashlib,json,sys
sys.dont_write_bytecode=True
import independent_current_bank as p
P=Path(__file__).resolve().parent


def wire_set(tree):
    if tree['op']=='seq':return set().union(*(wire_set(t) for t in tree['children']))
    if tree['op']=='repeat':return wire_set(tree['child'])
    return set(tree['wires'])


def address_checks():
    plan=p.namespace();base=p.g.namespace();r=plan['reports'][7]
    lo,hi=plan['fresh_logical_interval'];helper=plan['old_compiler_helper']
    assert lo==helper+1 and hi-lo==1486721154
    assert p.physical_wire(2)==1 and p.physical_wire(helper)==10407050781
    assert p.physical_wire(lo)==10407050782 and p.physical_wire(hi-1)==11893771935
    # On the entire virtual fresh interval the affine map q -> q-3 is
    # injective and starts immediately after the OLD helper. No enumeration.
    blocks=p.birth_blocks();last=0
    for block in blocks:
        assert p.physical_wire(block['start'])==last
        last+=block['stop']-block['start']
        assert p.physical_wire(block['stop']-1)==last-1
    assert last==11893771936
    assert plan['reports'][:7]==base['reports'] and plan['source_slots'][:1372]==base['source_slots']
    assert plan['SC6_local_to_global']==base['SC6_local_to_global']
    assert not any(lo<=q<hi for q in plan['SC6_local_to_global'])
    fresh=[plan['source_slots'][i] for i in r['source_slots']]
    assert Counter((s['kind'],s['bank']) for s in fresh)=={('Choi','f'):180,('CAR','q'):16}
    data=[q for s in fresh for q in s['source']+s.get('RIGHT',[])]
    private=[q for s in fresh for q in s['private']]
    assert len(data)==len(set(data))==4264 and len(private)==len(set(private))==4368
    assert set(data).isdisjoint(private)
    assert all(lo<=q<r['source_private_start'] for q in data)
    assert set(private)==set(range(r['source_private_start'],hi))
    assert set(data).issubset(p.resource_wires()) and set(private).isdisjoint(p.resource_wires())
    # Actual provider layouts retain little-endian DATA order and whole R.
    for s in fresh:
        if s['kind']=='Choi':
            layout=p.g.ns.choi_layout(plan,s)
            assert layout['choi_output']==s['source'][:5] and layout['choi_input']==s['source'][5:10]
        else:
            layout=p.g.ns.car_layout(plan,s)
            assert layout['grade']==s['source'][:4] and layout['internal_SITE']==s['source'][4:]
        assert layout['SAM']==base['layout']['SAM']
    return {'fresh_source_DATA_RIGHT':4264,'fresh_source_private':4368,
      'fresh_virtual_interval_width':hi-lo,'total_births':last,'old_helper_and_aux_preserved':True}


def chronology_and_templates():
    plan=p.namespace();schedule=p.stages();reports=[s for s in schedule if s['kind']=='REPORT']
    assert [s['report'] for s in reports]==list(range(8))
    assert Counter(s['kind'] for s in schedule)=={'SITE':1,'SIGMA':8,'SOURCE':1568,'RAW_RESOURCE_FRAME':2,'REPORT':8,'PORT_ZERO':1,'SC6':1}
    first_report=next(i for i,s in enumerate(schedule) if s['kind']=='REPORT')
    assert all(s['kind'] not in ('SOURCE','SIGMA') for s in schedule[first_report:])
    # Logical report injection fixes all shared roles; all local DATA and
    # processor coordinates are a single translated virtual interval.
    N=plan['local_report']['logical_wire_count'];r=plan['reports'][7]
    for q in (0,7,8,N-1,N,N+1,N+2,N+3,N+4):
        got=p.g.ns.report_wire(plan,r,q)
        if q<8:assert got==plan['layout']['SITE'][q]
        elif q<N:assert got==r['private_start']+q-8
        else:assert got==[2705,0,1,2,3][q-N]
    # The actual repeated literal inversion, including depth TWO, gives
    # the four-frame census. Compiling a fresh-wire inverse uses OLD helper.
    q=r['private_start'];gate=p.a.c.nb.gate('G',q);counts=Counter()
    for depth in (0,1,2,1):counts+=p.g.native_count(p.g.invert(gate,depth,plan),2705)
    assert counts==Counter(G_port=3,G_other=1,CX=18,SourceI=24)
    compiled,pending,_=p.a.c.production_compiler().transform(p.g.invert(gate,1,plan))
    assert pending==0
    assert plan['old_compiler_helper'] in wire_set(compiled)
    assert plan['layout']['qubits'] not in wire_set(compiled)
    assert max(wire_set(p.physical_tree(compiled)))<11893771936
    # Sample emitted blocks, not production enumeration; full coverage is
    # inherited through the proved injective substitution from A25/A29/B58.
    seen=0
    for kind in ('Choi','CAR'):
        si=next(i for i in r['source_slots'] if plan['source_slots'][i]['kind']==kind)
        for depth in (0,1):
            for tree in islice(p.stage_blocks({'kind':'SOURCE','slot':si},depth),2):
                assert all(0<=q<plan['layout']['qubits'] for q in wire_set(tree));seen+=1
    return {'sampled_actual_source_blocks':seen,'four_literal_RAW_frame_counts':dict(counts),
      'full_PROVIDER_coverage_inherited_by_injective_address_substitution':True}


def count(factory):
    out=Counter()
    for tree in factory():
        if tree['op'] not in ('B82_CUT','A46_MARK'):out.update(p.old.native.counts(tree))
    return out


def paid_fixtures():
    nb=p.a.c.nb;n=7;sam=(1,2,3);port=0;spin=(7,8);helper=5;fresh=6
    before=[nb.gate('CX',sam[0],fresh),nb.gate('G',fresh)]
    # Two original/full current logical REPORT representatives on WORK;
    # all three native inverse depths are still emitted literally.
    middle=[nb.gate('G',4),nb.gate('CX',4,fresh),nb.gate('G',port)]
    def profile():
        yield from before;yield {'op':'B82_CUT','name':p.p43.CUTS[0]}
        yield from middle;yield {'op':'B82_CUT','name':p.p43.CUTS[1]}
        for tree in reversed(before):yield nb.inverse_literal(tree,port,spin)
    compiler=p.a.c.Compiler(port,spin,helper,1)
    tagged=lambda:p.compile_tagged(profile,compiler,lambda x:x)
    post=[nb.gate('G',sam[0])];cfg=p.p43.extend_configuration(p.old.align(n,sam,count(tagged),count(lambda:iter(post)),(2,3),3,1));cfg['K']=2
    rows=[]
    for leg,sign in [('centre','centre'),('Qf','plus'),('Qf','minus'),('Qb','plus'),('Qb','minus')]:
        core=lambda:p.p43.with_q_slots(tagged,sam,cfg['powers'],cfg['Q_slot_calls'],leg=leg,sign=sign)
        assert sum(count(core).values())==sum(cfg['core_counts'].values())
        stages=list(p.old.execution_stages(cfg,core,lambda:iter(post),p.old.native.Macros()))
        width=0;dimension=1;clockdim=0;calls=0
        for row in stages:
            clockdim+=dimension
            if row['kind']=='canonical_RAW_birth':
                assert row['wire']==width;width+=1;dimension*=2
            else:assert max(row['gate']['wires'])<width;calls+=1
        assert clockdim==(1<<n)*(cfg['Lbase']-2+3*(1<<cfg['K']))-1
        assert calls==cfg['Lbase']+cfg['K'] and len(stages)==cfg['Nbase']+2*cfg['K']
        assert stages[-1]['gate']==nb.gate('G',n+cfg['K']-1)
        rows.append({'leg':leg,'sign':sign,'calls':calls,'clock_dimension':clockdim})
    def broken():
        yield nb.gate('SourceI',port,*spin)
        yield {'op':'A46_MARK','kind':'invalid_half_pair'}
    try:list(p.compile_tagged(broken,compiler,lambda t:t));raise RuntimeError('accepted split SourceI')
    except AssertionError as e:assert 'SourceI pair' in str(e)
    return rows


def main():
    checks={'addresses':address_checks(),'chronology':chronology_and_templates(),'paid_fixtures':paid_fixtures()}
    plan=p.build();assert plan==json.loads((P/'INDEPENDENT_CURRENT_BANK_PLAN.json').read_text())
    for f,sha in plan['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==sha
    try:next(p.old.execution_stages(p.production_configuration(),lambda:iter(()),lambda:iter(()),p.old.native.Macros()));raise RuntimeError('production guard lost')
    except NotImplementedError:pass
    checks.update({'status':'PASS_INDEPENDENT_CURRENT_BANK_ADDRESS_CLOCK_AND_ERROR_CHECKS',
      'production_word_executed':False,'original_full_mark_admission_proved':False,
      'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in (Path(__file__),P/'independent_current_bank.py',P/'INDEPENDENT_CURRENT_BANK_PLAN.json')}})
    (P/'INDEPENDENT_CURRENT_BANK_CHECK.json').write_text(json.dumps(checks,indent=2)+'\n');print(checks['status'])


if __name__=='__main__':main()
