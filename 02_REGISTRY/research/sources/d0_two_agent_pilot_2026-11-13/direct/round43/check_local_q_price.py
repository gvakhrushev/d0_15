#!/usr/bin/env python3
"""Named local derivative, paid five-arm family, and pinned source checks."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
sys.dont_write_bytecode=True
import sympy as S
import local_q_price as p
P=Path(__file__).resolve().parent


def count(factory):
    out=Counter()
    for block in factory():
        if block['op']!='B82_CUT':out.update(p.old.native.counts(block))
    return out


def matter_derivative():
    # Two real CAR components and the original Lorentz coframe contraction.
    u=S.Matrix(4,4,lambda a,r:S.Symbol('u%d%d'%(a,r)))
    d=S.Matrix(4,2,lambda r,a:S.Symbol('d%d%d'%(r,a)))
    nu=S.Rational(3,5);eta=S.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    q=sum((u[:,r].T*eta*u[:,t])[0]*(d[r,:]*d[t,:].T)[0]
          for r in range(4) for t in range(4))/nu**2
    target=-2/nu**2*sum(u[2,t]*(d[0,:]*d[t,:].T)[0] for t in range(4))
    assert S.expand(S.diff(q,u[2,0])-target)==0
    centre={u[2,t]:(nu if t==2 else 0) for t in range(4)}
    centre.update({d[t,a]:0 for t in (1,2,3) for a in range(2)})
    assert S.expand(target.subs(centre))==0


def paid_families():
    old=p.old;sam=(1,2,3);n=5;powers=(2,3)
    before=[p.gate('CX',1,0),p.gate('G',0)]
    middle=[p.gate('CX',0,4),p.gate('G',4)]
    after=[p.gate('G',0),p.gate('CX',1,0)]
    post=[p.gate('G',1),p.gate('CX',2,3)]
    def core():
        yield from before
        yield {'op':'B82_CUT','name':p.CUTS[0]}
        yield from middle
        yield {'op':'B82_CUT','name':p.CUTS[1]}
        yield from after
    assert all(set(g['wires']).isdisjoint(sam) for g in middle)
    cfg=p.extend_configuration(old.align(n,sam,count(core),count(lambda:iter(post)),powers,3,1))
    cfg['K']=2;slot=cfg['Q_slot_calls'];rows=[];common_prefix=None
    for leg,sign in [('centre','centre'),('Qf','plus'),('Qf','minus'),('Qb','plus'),('Qb','minus')]:
        factory=lambda:p.with_q_slots(core,sam,powers,slot,leg=leg,sign=sign,axis=2)
        cc=count(factory)
        power=0 if leg=='centre' else powers[(0 if sign=='plus' else 1)^(leg=='Qf')]
        expected=count(core)+Counter(G=power,CX=2*slot-power)
        assert cc==expected
        # extend_configuration's Counter is exact only for the centre. In an
        # active arm G calls replace the same number of identity CX calls.
        assert sum(cc.values())==sum(cfg['core_counts'].values())
        assert (cc==cfg['core_counts'])==(leg=='centre')
        stages=list(old.execution_stages(cfg,factory,lambda:iter(post),old.native.Macros()))
        checkpoint=n+cfg['preL']+len(before)
        prefix=stages[:checkpoint]
        if common_prefix is None:common_prefix=prefix
        else:assert prefix==common_prefix
        width=0;dim=1;D=0;calls=Counter()
        for stage in stages:
            D+=dim
            if stage['kind']=='canonical_RAW_birth':
                assert stage['wire']==width;width+=1;dim*=2
            else:
                assert max(stage['gate']['wires'])<width
                calls[stage['gate']['op']]+=1
        assert len(stages)==cfg['Nbase']+2*cfg['K']
        assert sum(calls.values())==cfg['Lbase']+cfg['K']
        assert D==(1<<n)*(cfg['Lbase']-2+3*(1<<cfg['K']))-1
        assert stages[-1]=={'kind':'final_unitary_g','gate':p.gate('G',n+cfg['K']-1)}
        assert width==n+cfg['K']
        rows.append({'leg':leg,'sign':sign,'stages':len(stages),'clock_dimension':D,
                     'core_G':cc['G'],'core_CX':cc['CX'],'original_checkpoint':checkpoint})
    assert len({(r['stages'],r['clock_dimension'],r['original_checkpoint']) for r in rows})==1
    return rows


def main():
    matter_derivative();rows=paid_families()
    plan=p.build();assert plan==json.loads((P/'LOCAL_Q_PRICE_PLAN.json').read_text())
    for file,sha in plan['source_sha256'].items():
        assert hashlib.sha256(Path(file).read_bytes()).hexdigest()==sha
    cfg=p.extend_configuration(p.old.production_configuration())
    try:
        next(p.old.execution_stages(cfg,lambda:iter(()),lambda:iter(()),p.old.native.Macros()))
        raise AssertionError('unmaterialized production word accepted')
    except NotImplementedError:pass
    pins=[Path(__file__),P/'local_q_price.py',P/'LOCAL_Q_PRICE_PLAN.json']
    result={'status':'PASS_NAMED_LOCAL_Q_BOUNDS_AND_FIVE_PAID_SMALL_HISTORIES',
      'pointwise_matter_derivative_symbolically_checked':True,
      'full_small_histories':rows,'centre_counts_distinguished_from_active_arm_counts':True,
      'original_prefix_before_first_Q_slot_identical':True,
      'production_upper_count_guard_preserved':True,
      'production_word_or_absolute_heat_trace_evaluated':False,
      'full_original_H1_or_mark_admission_proved':False,
      'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}}
    (P/'LOCAL_Q_PRICE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__=='__main__':main()
