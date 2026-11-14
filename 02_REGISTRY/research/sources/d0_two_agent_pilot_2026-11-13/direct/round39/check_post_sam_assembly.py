#!/usr/bin/env python3
"""Replay full small histories through production emitter plus exact budgets.

Sentinel exponents test syntax/clock, not physical angle precision.  Actual
production exponents and inequalities are consumed from pinned A38/B75.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from itertools import islice
import hashlib,json
import post_sam_assembly as a
P=Path(__file__).resolve().parent


def inverted(t):
    if t[0]=='phase':return (t[0],t[1],not t[2],t[3])
    return t[0],not t[1]


def main():
    # Chronological adjoints must reverse order AND phase signs.
    for level in range(5):
        f=list(a.amplifier_tokens(level));b=list(a.amplifier_tokens(level,True))
        assert b==[inverted(t) for t in reversed(f)]
        assert sum(t[0]=='W' for t in f)==3**level
        assert Counter(t[1] for t in f+b if t[0]=='P')=={False:3**level,True:3**level}
    tokens=list(a.post_tokens(9))
    assert sum(t[0]=='W' for t in tokens)==39366
    assert tokens[0]==('clean',False) and tokens[-1]==('clean',True)
    assert Counter(t[1] for t in tokens if t[0]=='P')=={False:19683,True:19684}
    # Finite test values intentionally are NOT certified angles.
    ks={'pi8':1,'pi6':2,'half_theta':3,'minus_half_theta':2,'minus_theta':4,'beta':5,'minus_beta':7}
    macro=a.m.Macros({'status':'PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS','error_bits':20000,
                      'rotations':{k:{'exponent_hex':hex(v)} for k,v in ks.items()}})
    layout=a.Layout(old=8,sam_count=3)
    word=[a.m.seq(a.m.gate('G',0),a.m.gate('CX',2,1)),a.m.gate('G',7)]
    wc=Counter(G=2,CX=1)
    factory=lambda:iter(word)
    def obj(power,level):return a.Assembly(power,sam_index=0,level=level,layout=layout,
                                         macros=macro,W_factory=factory,W_counts=wc)
    # Count emitted complete post words; preserve leaked registers in every
    # full unitary and include all separate inverse constructions.
    cases=0
    for level in range(3):
        for power in (0,1,3):
            q=obj(power,level); emitted=Counter()
            for block in q.post_blocks():emitted.update(a.m.counts(block))
            budget=q.post_budget()
            assert emitted=={'G':budget['G'],'CX':budget['CX']}
            stream=sum((q.token_budget(t) for t in a.post_tokens(level)),Counter())
            assert stream==budget
            without=Counter()
            for block in q.post_blocks(True):without.update(a.m.counts(block))
            assert without==emitted-Counter(G=1)
            # Every post gate addresses only SAM or fresh private.
            def syntactic(t):
                if t['op']=='seq':
                    for c in t['children']:yield from syntactic(c)
                elif t['op']=='repeat':yield from syntactic(t['child'])
                else:yield t
            for block in q.post_blocks():
                for leaf in syntactic(block):
                    assert all(w in layout.sam or layout.old<=w<layout.total for w in leaf['wires'])
            cases+=1
    # The five-CX padding is an identity on ALL three input bits.
    for length in (4,5,6,7,11):
        for bits in range(8):
            reg={layout.branch:bits&1,layout.flag:(bits>>1)&1,layout.helper:(bits>>2)&1}
            before=dict(reg);count=0
            for block in a.identity_padding(length,layout):
                for g in a.primitive_leaves(block):
                    assert g['op']=='CX';c,t=g['wires'];reg[t]^=reg[c];count+=1
            assert reg==before and count==length
    # Actual common-clock emitter including centre, split restore G,
    # late births/G and final gate.  This is a full toy execution census.
    aa={n:obj(p,0) for n,p in [('centre',0),('plus',1),('minus',3)]}
    config=list(a.align_family(aa));config[-1]=3;config=tuple(config)
    _,post,preL,postL,Lbase,Nbase,K=config
    totals={}
    for name in aa:
        width=0;D=0;stages=0;calls=Counter();births=0
        final=None
        for stage in a.execution_stages(name,configuration=config):
            assert final is None,'a stage follows final g'
            D+=1<<width;stages+=1
            if stage['kind']=='canonical_RAW_birth':
                assert stage['wire']==width and stage['carrier_qubits_after']==width+1
                width+=1;births+=1
            else:
                g=stage['gate'];assert max(g['wires'])<width
                calls[g['op']]+=1
                if stage['kind']=='final_unitary_g':final=g
        assert final==a.m.gate('G',layout.final_wire)
        assert width==layout.total+K and births==width
        assert sum(calls.values())==Lbase+K and stages==Nbase+2*K
        assert D==(1<<layout.total)*(Lbase-3+4*(1<<K))-1
        totals[name]=(D,stages,width)
    assert len(set(totals.values()))==1
    # A real production centre must start emitting: catches repeat(0),
    # which a successful algebraic build alone would fail to detect.
    first=next(a.endpoint_blocks('centre'))
    assert set(a.m.counts(first))=={'CX'}
    plan=a.build()
    assert plan==json.loads((P/'POST_SAM_ASSEMBLY_PLAN.json').read_text())
    assert plan['early_births']==31221149661 and plan['late_retention_pairs']==146448
    for p,h in plan['source_sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
    l=a.Layout();records=l.records()
    assert records[0]['start']==0 and records[-1]['stop']==l.total
    assert all(x['stop']==y['start'] for x,y in zip(records,records[1:]))
    assert len(l.scratch)==max(len(l.controls(n)[0]) for n in ('good','start','chi'))-2
    assert l.final_wire==l.clean[-1]
    assert l.total==3*l.old-l.sam_count+3
    # Independently re-derive the nontrivial P count coefficient in the
    # combined pre+post family, not just recurrence mirroring.
    aa,post,*_=a.pair_configuration()
    c=3**9;k=aa['plus'].m.ks['minus_theta']
    for name in ('plus','minus'):
        p=aa[name].power
        assert post[name]['G']-post['centre']['G']+p==(c+1)*p*(1+k)
        assert post[name]['E']-post['centre']['E']==(c+1)*p
    # Full vector loss identity is real-unitary; no discarded private.
    e=F(1,1<<6024)
    assert e*e*F(1<<4776,2)==F(1,1<<7273)
    assert e*(1<<3158)==F(1,1<<2866)
    pins=[Path(__file__),P/'post_sam_assembly.py',P/'POST_SAM_ASSEMBLY_PLAN.json']
    out={'status':'PASS_COMPLETE_SMALL_HISTORY_REPLAY_AND_PRODUCTION_BUDGETS',
         'post_emitter_exact_count_fixtures':cases,'full_clock_centre_and_both_endpoints_replayed':True,
         'real_production_centre_emits_without_repeat_zero':True,
         'separate_adjoint_chronology_checked_levels_0_through_4':True,
         'production_39366_controlled_calls_and_P_counts_checked':True,
         'final_g_after_retention_and_dimension_formula_checked':True,
         'toy_angles_are_not_production_precision_evidence':True,
         'giant_production_stream_executed':False,
         'physical_task_admission_or_GR_proved':False,'physical_C_closed':False,'GR_closed':False,
         'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins}}
    (P/'POST_SAM_ASSEMBLY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','post_emitter_exact_count_fixtures',
          'full_clock_centre_and_both_endpoints_replayed')}))


if __name__=='__main__':main()
