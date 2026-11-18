#!/usr/bin/env python3
"""Paid insertion, exact address injection, and no-free-inverse control."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
sys.dont_write_bytecode=True
import composite_processor_echo as p
P=Path(__file__).resolve().parent


def count(factory):
    out=Counter()
    for tree in factory():
        if tree['op'] not in ('B82_CUT','A45_MARK'):out.update(p.old.native.counts(tree))
    return out


def address_checks():
    plan=p.a.g.namespace();ri,swap,pairs,choi=p.address_binding();f=plan['reports'][ri]
    assert len(swap)==608 and len(pairs)==16
    lo=f['private_start'];hi=lo+f['private_width']
    moving=set(q for row in pairs for q in row['f_wires'])
    targets=set(q for row in pairs for q in row['q_wires'])
    assert len(moving)==len(targets)==304 and moving.isdisjoint(targets)
    assert all(lo<=q<hi for q in moving) and all(not lo<=q<hi for q in targets)
    # Identity on the rest of the private interval + moved points outside it
    # is an injection on ALL ~1.5 billion logical report coordinates.
    selected=Counter();phys=[]
    for si in f['source_slots']:
        slot=plan['source_slots'][si];selected[slot['kind']]+=1
        mapped=[swap.get(q,q) for q in slot['source']+slot.get('RIGHT',[])]
        if slot['kind']=='Choi':assert mapped==slot['source']
        else:
            row=next(r for r in pairs if r['f_slot']==si)
            assert mapped==row['q_wires']
        phys.extend(mapped)
    assert selected=={'Choi':180,'CAR':16} and len(phys)==len(set(phys))==4264
    assert all(p.a.b.physical_wire(q)>=0 for q in phys)
    assert all(swap.get(q,q)==q for q in plan['layout']['SITE'])
    return {'CAR_wire_pairs':304,'selected_complete_source_wires':4264,
            'full_virtual_report_coordinate_injection':True}


def toy_echo(port,spin,helper,target):
    nb=p.a.c.nb;forward=nb.gate('G',target)
    backward=nb.inverse_literal(forward,port,spin)
    compiler=p.a.c.Compiler(port,spin,helper,1)
    f,pend,_=compiler.transform(forward);assert pend==0
    b,pend,_=compiler.transform(backward);assert pend==0
    counted=count(lambda:iter((f,b)))
    original=p.a.g.native_count(forward,port)+p.a.g.native_count(backward,port)
    predicted,weight,_=p.translated_counts(original,0,0,1)
    assert counted==predicted==Counter(G=34,CX=10) and weight==32
    return [f,b]


def exact_no_free_inverse():
    e=p.old.a41.e;word=toy_echo(0,(3,4),2,1)
    gates=[g for t in word for g in e.leaves(t)]
    columns=[]
    for col in range(8):
        state=[e.Q4(int(x==col)) for x in range(8)]
        for gate in gates:
            op=gate['op'];w=gate['wires'];target=1<<w[-1]
            assert set(w).issubset({0,1,2})
            for x in range(8):
                if x&target:continue
                y=x|target
                if op=='G':
                    u,v=state[x],state[y]
                    state[x],state[y]=e.A*u-e.SIN*v,e.SIN*u+e.A*v
                elif x>>w[0]&1:state[x],state[y]=state[y],state[x]
        columns.append(state)
    for a in range(8):
        for b in range(8):
            assert sum((u*v for u,v in zip(columns[a],columns[b])),e.Q4())==int(a==b)
    assert any(columns[j][i]!=int(i==j) for j in range(8) for i in range(8))
    return {'exact_Golden_columns':8,'compiled_echo_exact_unitarity':True,
      'two_compiled_legs_not_automatically_exact_inverse':True,
      'fixture_uses_uncertified_small_k_for_negative_control_only':True}


def small_paid_families():
    n=6;sam=(1,2,3);port=0;spin=(6,7);helper=5
    nb=p.a.c.nb;echo=toy_echo(port,spin,helper,4)
    before=[nb.gate('CX',1,4),nb.gate('G',4)]
    middle=[nb.gate('CX',4,0),nb.gate('G',0)]
    after=[nb.gate('G',4),nb.gate('CX',1,4)]
    post=[nb.gate('G',1),nb.gate('CX',2,3)]
    def profile():
        yield from before
        yield {'op':'B82_CUT','name':p.p43.CUTS[0]}
        yield {'op':p.BARRIER}
        yield from middle
        yield {'op':'B82_CUT','name':p.p43.CUTS[1]}
        yield from after
    compiler=p.a.c.Compiler(port,spin,helper,1)
    tagged=lambda:p.compile_tagged(profile,compiler,lambda:iter(echo),lambda tree:tree)
    base=count(lambda:iter(before+middle+after))
    cfg=p.p43.extend_configuration(p.old.align(n,sam,base,count(lambda:iter(post)),(2,3),3,1))
    ec=count(lambda:iter(echo));cfg['core_counts']+=ec
    cfg['Lbase']+=sum(ec.values());cfg['Nbase']+=sum(ec.values());cfg['K']=2
    cases=[];same_prefix=None
    for leg,sign in [('centre','centre'),('Qf','plus'),('Qf','minus'),('Qb','plus'),('Qb','minus')]:
        core=lambda:p.p43.with_q_slots(tagged,sam,cfg['powers'],cfg['Q_slot_calls'],leg=leg,sign=sign,axis=2)
        cc=count(core);assert sum(cc.values())==sum(cfg['core_counts'].values())
        stages=list(p.old.execution_stages(cfg,core,lambda:iter(post),p.old.native.Macros()))
        mark=n+cfg['preL']+len(before);prefix=stages[:mark]
        if same_prefix is None:same_prefix=prefix
        else:assert prefix==same_prefix
        width=0;dim=1;D=0;calls=0
        for stage in stages:
            D+=dim
            if stage['kind']=='canonical_RAW_birth':
                assert stage['wire']==width;width+=1;dim*=2
            else:
                assert max(stage['gate']['wires'])<width;calls+=1
        assert len(stages)==cfg['Nbase']+2*cfg['K'] and calls==cfg['Lbase']+cfg['K']
        assert D==(1<<n)*(cfg['Lbase']-2+3*(1<<cfg['K']))-1
        assert stages[-1]=={'kind':'final_unitary_g','gate':p.old.gate('G',n+cfg['K']-1)}
        newmark=mark+cfg['Q_slot_calls']+sum(count(lambda:iter(echo[:1])).values())
        cases.append({'leg':leg,'sign':sign,'stages':len(stages),'clock_dimension':D,
                     'original_RAW_mark':mark,'new_complete_processor_mark':newmark})
    assert len({(x['stages'],x['clock_dimension'],x['new_complete_processor_mark']) for x in cases})==1
    # The guarded compiler rejects cutting a genuine unmatched SourceI.
    def invalid():
        yield nb.gate('SourceI',port,*spin)
        yield {'op':p.BARRIER}
    try:
        list(p.compile_tagged(invalid,compiler,lambda:iter(echo),lambda t:t))
        raise AssertionError('unmatched SourceI insertion accepted')
    except AssertionError as err:
        assert 'SourceI pair' in str(err)
    return cases


def main():
    address=address_checks();negative=exact_no_free_inverse();histories=small_paid_families()
    plan=p.build();assert plan==json.loads((P/'COMPOSITE_PROCESSOR_ECHO_PLAN.json').read_text())
    for f,h in plan['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h
    cfg=p.production_configuration()
    try:
        next(p.old.execution_stages(cfg,lambda:iter(()),lambda:iter(()),p.old.native.Macros()))
        raise AssertionError('production provider guard lost')
    except NotImplementedError:pass
    files=[Path(__file__),P/'composite_processor_echo.py',P/'COMPOSITE_PROCESSOR_ECHO_PLAN.json']
    out={'status':'PASS_COMPLETE_COMPOSITE_BINDING_PAID_CLOCK_AND_ECHO_ERROR_BUDGET',
      'address_checks':address,'negative_control':negative,'full_small_paid_histories':histories,
      'unmatched_SourceI_prefix_rejected':True,'new_heat_gain_and_analytic_endpoint_perturbation_paid':True,
      'production_native_history_executed':False,'independent_eighth_bank_or_stronger_FN_admission':False,
      'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
    (P/'COMPOSITE_PROCESSOR_ECHO_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'])


if __name__=='__main__':main()
