#!/usr/bin/env python3
"""Exact small actual-circuit reference, paid clocks and production bounds."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
from collections import Counter
import json,sys
sys.dont_write_bytecode=True
import two_bit_paid_family as p
t=p.target;e=t.e;native=p.native;P=Path(__file__).resolve().parent

def encloses(x,y):return x[0]<=y[0]<=y[1]<=x[1]

def kernels():
    rows=[]
    fixtures=[(3,(0,2),[native.gate('CX',0,1)]),
      (3,(0,2),[native.gate('G',1),native.gate('CX',2,1),native.gate('G',1)]),
      (4,(0,2),[native.gate('CX',0,3),native.gate('G',1),native.gate('CX',1,3),native.gate('G',3)]),
      (4,(0,1,2),[native.gate('CX',0,3)])]
    for n,sam,word in fixtures:
        core=t.ActualDiagonal(n,sam,lambda word=word:iter(word),path_limit=10000)
        lo=e.Dyadic(160);hi=e.Dyadic(256)
        for b in range(1<<len(sam)):
            ref=e.compressed_entry(n,sam,b,lambda word=word:iter(word))
            got=core.entry(b,lo);precise=hi.field(ref)
            scaled=(precise[0]>>96,-((-precise[1])>>96))
            assert encloses(got,scaled),(n,b)
            assert got[1]-got[0]<1<<24
        rows.append({'n':n,'CODE_bits':len(sam),'labels':1<<len(sam),'G_calls':core.g_calls()})
    # Read-only CODE is enforced by actual primitive semantics, not metadata.
    bad=t.ActualDiagonal(3,(0,2),lambda:iter([native.gate('G',0)]),path_limit=100)
    try:bad.entry(0,e.Dyadic(128));raise AssertionError('CODE target accepted')
    except AssertionError as err:assert 'CODE control-only' in str(err)
    return rows

def targets():
    sam=(0,1,2);word=[native.gate('CX',0,3)]
    core=t.ActualDiagonal(4,sam,lambda:iter(word),path_limit=1000)
    actual=t.PositiveTarget(core)
    table=[e.compressed_entry(4,sam,b,lambda:iter(word)) for b in range(8)]
    chi,_,h,_=e.target_vectors(table,3)
    ref={}
    for kind,vector in [('chi',chi),('h',h)]:
        for j,c,s in t.a41.elimination(vector):
            ref[kind,j]=t.a41.divided_angle(c,s,3)
    checked=0
    for kind in ('chi','h'):
        for j in range(1,8):
            got=actual.star(kind,j,256);exact=e.Dyadic(384).evaluate(ref[kind,j])
            for a,b in zip(got,exact):
                lower=b[0]>>128;upper=-((-b[1])>>128)
                assert a[0]<=lower<=upper<=a[1],(kind,j)
            checked+=1
    # Execute the real certified positive-power selector once on this
    # computed actual-circuit target, not a supplied angle table.
    k=t.select_from_intervals(lambda bits:actual.star('h',3,bits))
    _,q,_=t.a41.uniform_grid();assert 1<=k<=q
    # Structural native support and counts for all four lists. Selector=1
    # here is a grammar test, explicitly not a target approximation claim.
    calls=[]
    def selector(fn):
        c,s=fn(128);assert c[0]>0;calls.append((c,s));return 1
    counts=Counter()
    for block in t.post_blocks(core,selector=selector):
        counts.update(native.counts(block))
        for gate in e.leaves(block):assert set(gate['wires'])<=set(sam)
    assert len(calls)==28 and counts=={'G':112,'CX':264}
    return {'star_ratios_vs_exact_algebraic_reference':checked,
      'actual_target_selected_k_hex':hex(k),'four_star_list_grammar_counts':dict(counts),
      'grammar_selector_one_is_not_accuracy_test':True}

def histories():
    sam=(0,1,2);n=5
    before=[native.gate('G',3),native.gate('CX',0,3)]
    middle=[native.gate('CX',3,4)]
    after=[native.gate('CX',0,3),native.gate('G',3)]
    def core():
        yield from before;yield {'op':'B82_CUT','name':p.CUTS[0]}
        yield from middle;yield {'op':'B82_CUT','name':p.CUTS[1]};yield from after
    post=[native.gate('CX',0,1),native.gate('G',2)]
    def ctr(axis,sign):
        if sign:yield native.repeat(1 if sign==1 else 2,native.gate('G',sam[axis]))
    def probe(plane,sign):
        yield native.repeat(3 if sign==1 else 4,native.gate('G',sam[0]))
    cfg={'n':n,'sam':sam,'K':3,'coreL':9,'postL':6,'controlL':6,'probeL':8}
    cfg['Lbase']=cfg['coreL']+cfg['postL']+cfg['probeL']+4*cfg['controlL'];cfg['Nbase']=n+cfg['Lbase']
    rows=[];marks=None;clocks=set()
    for arm,sign in [('centre',0)]+[(a,s) for a in ('matched','Pf','Qf','Qb','Pb','post_probe') for s in (-1,1)]:
        factory=lambda:p.family_blocks(cfg,core,lambda:iter(post),ctr,probe,
          arm=arm,sign=sign,axis=1,plane=(0,1),keep_marks=True)
        c=p.pad.count(factory,tag_ops=('B82_CUT',));assert sum(c.values())==cfg['Lbase']
        width=0;dimension=0;layers=0;loc=[];calls=Counter();last=None
        for st in p.execution_stages(cfg,factory):
            if st['kind']=='source_mark':loc.append((st['name'],layers));continue
            dimension+=1<<width;layers+=1;last=st
            if st['kind']=='canonical_RAW_birth':assert st['wire']==width;width+=1
            else:
                assert max(st['gate']['wires'])<width;calls[st['gate']['op']]+=1
        assert layers==cfg['Nbase']+2*cfg['K']
        assert dimension==(1<<n)*(cfg['Lbase']-2+3*(1<<cfg['K']))-1
        assert sum(calls.values())==cfg['Lbase']+cfg['K']
        assert last=={'kind':'final_unitary_g','gate':native.gate('G',n+cfg['K']-1)}
        if marks is None:marks=loc
        else:assert marks==loc
        clocks.add((layers,dimension));rows.append({'arm':arm,'sign':sign,'G':calls['G'],'CX':calls['CX']})
    assert len(clocks)==1 and len({(x['G'],x['CX']) for x in rows})>1
    # Slot conventions and matched signs are structural, not assumed from
    # a comparison of total call counts.
    assert p.slot_signs('matched',1)==dict(Pf=1,Qf=-1,Qb=1,Pb=-1)
    return {'histories':rows,'common_mark_layers':marks,'common_clock':list(clocks)[0]}

def main():
    ks=kernels();ts=targets();hs=histories();cfg=p.production_configuration();b=p.bounds(cfg)
    assert cfg['Nbase'].bit_length()==30833 and cfg['K']==175604
    assert all(x<F(1,1<<75) for x in (b['heat_full_skew_dual'],b['post_independent_skew_dual_finite_feedback_error']))
    out={'status':'PASS_ACTUAL_TARGET_SMALL_KERNELS_PADDED_FOUR_SLOT_CLOCKS_AND_BOUNDS',
      'exact_Q4_kernel_fixtures':ks,'target_checks':ts,'paid_clock_checks':hs,
      'production_Nbase_bit_length':cfg['Nbase'].bit_length(),'production_K':cfg['K'],
      'original_upper_not_promoted_to_actual_unpadded_price':True,
      'production_target_or_full_word_evaluated':False,
      'original_admission_or_physical_price_stationarity_proved':False,
      'physical_C_closed':False,'GR_closed':False}
    (P/'TWO_BIT_PAID_FAMILY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'exact_kernel_labels':sum(x['labels'] for x in ks),
      'paid_small_histories':len(hs['histories'])}))

if __name__=='__main__':main()
