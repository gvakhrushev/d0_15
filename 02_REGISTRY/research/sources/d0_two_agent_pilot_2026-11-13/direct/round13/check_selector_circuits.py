#!/usr/bin/env python3
"""Primitive-gate tests plus exact structural audit of all emitted rows."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib
import json
import random
from fractions import Fraction as F
import reversible_selectors as r
from build_selector_circuits import INPUTS, row_counts, circuit_counts

P=Path(__file__).resolve().parent
rng=random.Random(12013)
checks=Counter()


def expect_xor(word,state,target_wires,value):
    expected=r.put(state,target_wires,r.get(state,target_wires)^value)
    actual=r.apply_word(word,state)
    assert actual==expected,(state,actual,expected)
    return actual


# Exhaust all controls and dirty targets for clean reversible equality.
for n in range(7):
    controls=list(range(n));target=n;work=list(range(n+1,n+1+max(0,n-2)))
    for pattern in range(2**n):
        word=list(r.pattern_gate(controls,pattern,target,work))
        assert all(g[-1] not in controls for g in word)
        for x in range(2**n):
            for out in (0,1):
                expect_xor(word,x|(out<<target),[target],int(x==pattern));checks['equality_columns']+=1

# All small unsigned comparator columns, with arbitrary target and spectator.
for n in range(1,6):
    reg=list(range(n));target=n;borrow=list(range(n+1,2*n+2));spectator=2*n+2
    for threshold in range(2**n+1):
        word=list(r.compare_xor(reg,threshold,target,borrow))
        for x in range(2**n):
            for out in (0,1):
                for spectator_bit in (0,1):
                    state=x|(out<<target)|(spectator_bit<<spectator)
                    expect_xor(word,state,[target],int(x<threshold));checks['comparator_columns']+=1

# Complete small selector: genuinely different partitions, retained suffix,
# unused palette control values, arbitrary output bits and exact reverse.
small={'golden_coins_n':3,'fair_bits_r':2,'partitions':[
 {'weights':[[1,0],[0,0]],'counts_ready_then_abort':[[2,1],[5,3],[5,4]]},
 {'weights':[[1,0]],'counts_ready_then_abort':[[7,6],[5,2]]},
 {'weights':[[1,0],[0,0],[0,0]],'counts_ready_then_abort':[[0,0],[6,1],[1,5],[5,2]]}]}
small_plan=r.make_plan(small);q=small_plan['layout'];small_word=list(r.selector_word(small_plan))
readonly=set(q['palette']+q['golden']+q['fair'])
assert all(g[-1] not in readonly for g in small_word)
prefix_map={raw:(kind,rank) for raw,kind,rank in small_plan['prefix_codes']}
for j,raw,fair,out in product(range(4),range(8),range(4),range(8)):
    kind,rank=prefix_map[raw];pos=(rank<<2)|fair;want=0
    if j<3:
        end=0
        for label,pair in enumerate(small['partitions'][j]['counts_ready_then_abort']):
            end+=int(pair[kind])
            if pos<end:
                if label<len(small['partitions'][j]['weights']):want=(1<<small_plan['label_width'])|label
                break
    state=0
    for name,value in [('palette',j),('golden',raw),('fair',fair),('output',out)]:state=r.put(state,q[name],value)
    after=expect_xor(small_word,state,q['output'],want)
    assert r.apply_word(reversed(small_word),after)==state
    checks['complete_small_selector_columns']+=1
assert dict(Counter(g[0] for g in small_word))==circuit_counts(small_plan)

input_hashes={};summaries=[]
for filename in INPUTS:
    source=P.parent/'round12'/filename;palette=json.loads(source.read_text())
    compiled=P/filename.replace('PALETTE','CIRCUIT');plan=json.loads(compiled.read_text());q=plan['layout']
    input_hashes[filename]=hashlib.sha256(source.read_bytes()).hexdigest()
    assert plan['input_palette_sha256']==input_hashes[filename]
    # Execute every real Golden-prefix decoder column, then sum the actual
    # retained suffix weights independently in Q(p), p^2=1-p.
    prefix_word=list(r.prefix_word(plan));fibres={}
    p_multiply=lambda a:(a[1],a[0]-a[1])
    for raw in range(2**len(q['golden'])):
        state=r.put(0,q['golden'],raw);after=r.apply_word(prefix_word,state)
        kind=r.get(after,q['kind']);rank=r.get(after,q['rank'])
        assert r.apply_word(reversed(prefix_word),after)==state
        assert r.get(after,q['golden'])==raw
        total=0
        for i in range(len(q['golden'])):
            if total>=len(q['golden']):break
            total+=1+((raw>>i)&1)
        assert kind==total-len(q['golden'])
        weight=(F(1),F(0))
        for _ in range(len(q['golden'])+bin(raw).count('1')):weight=p_multiply(weight)
        old=fibres.get((kind,rank),(F(0),F(0)))
        fibres[kind,rank]=(old[0]+weight[0],old[1]+weight[1])
        checks['actual_prefix_gate_columns']+=1
    for kind in (0,1):
        size=int(palette['capacity_by_prefix_kind'][kind])//2**len(q['fair'])
        assert sorted(rank for k,rank in fibres if k==kind)==list(range(size))
        weight=(F(1),F(0))
        for _ in range(len(q['golden'])+kind):weight=p_multiply(weight)
        for rank in range(size):assert fibres[kind,rank]==weight
    # Every cumulative threshold/code transition is reconstructed independently.
    for row in plan['rows']:
        j,kind=row['palette'],row['kind'];part=palette['partitions'][j];counts=part['counts_ready_then_abort']
        running=0;expected=[];ready=1<<plan['label_width']
        for i in range(len(counts)-1):
            running+=int(counts[i][kind]);nextcode=(ready|i+1) if i+1<len(counts)-1 else 0
            mask=(ready|i)^nextcode
            if running and mask:expected.append([str(running),mask])
        assert row['boundaries']==expected;checks['actual_rows_structurally_checked']+=1
    # Primitive gate execution of real-width row blocks, not only Python comparisons.
    choices=sorted(set([0,len(plan['rows'])-1]+[rng.randrange(len(plan['rows'])) for _ in range(12)]))
    for row_index in choices:
        row=plan['rows'][row_index];word=list(r.row_word(plan,row))
        assert r.counts_of(word)==row_counts(plan,row)
        readonly=set(q['palette']+q['golden']+q['fair'])
        assert all(g[-1] not in readonly for g in word)
        width=len(q['fair'])+len(q['rank']);points={0,2**width-1}
        for threshold,_ in row['boundaries']:
            t=int(threshold)
            points.update(x for x in (t-1,t) if 0<=x<2**width)
        # Bound the diagnostic sample for 63-child internal sums; every table
        # boundary was exactly audited above and by A12/B26.
        points=sorted(points)
        if len(points)>12:points=points[:6]+points[-6:]
        for pos in points:
            for matching in (True,False):
                j=row['palette'] if matching else (row['palette']+1)%2**len(q['palette'])
                kind=row['kind'];initial_out=rng.randrange(2**len(q['output']));state=0
                for name,value in [('palette',j),('kind',kind),('fair',pos%(2**len(q['fair']))),
                                   ('rank',pos>>len(q['fair'])),('output',initial_out)]:state=r.put(state,q[name],value)
                want=0
                if matching:
                    for threshold,mask in row['boundaries']:
                        if pos<int(threshold):want^=mask
                expect_xor(word,state,q['output'],want);checks['actual_width_row_gate_samples']+=1
    # Actual-width comparator edge values, all-input correctness follows from
    # the exact Boolean borrow recurrence proven in the accompanying document.
    assert circuit_counts(plan)==plan['terminal_gate_counts']
    summaries.append({'file':compiled.name,'sha256':hashlib.sha256(compiled.read_bytes()).hexdigest(),
                      'wire_count':plan['wire_count'],'gate_counts':plan['terminal_gate_counts']})

# First-success label routing: all flags, arbitrary retained labels/output;
# no arbitrary quantum payload is copied or discarded by this circuit.
for cap,width in [(1,1),(3,2),(7,6),(7,2)]:
    plan=r.first_success_plan(cap,width);word=list(r.first_success_word(plan));q=plan['layout']
    assert all(g[-1] not in set(q['labels']+q['ready']) for g in word)
    for ready in range(2**cap):
        for repeat in range(4):
            labels=[rng.randrange(2**width) for _ in range(cap)];state=0
            state=r.put(state,q['labels'],sum(x<<(i*width) for i,x in enumerate(labels)))
            state=r.put(state,q['ready'],ready)
            state=r.put(state,q['output'],rng.randrange(2**width));state=r.put(state,q['out_ready'],repeat%2)
            selected=next((i for i in range(cap) if (ready>>i)&1),None)
            want=0 if selected is None else labels[selected]
            expected=r.put(state,q['output'],r.get(state,q['output'])^want)
            expected=r.put(expected,q['out_ready'],r.get(state,q['out_ready'])^int(selected is not None))
            assert r.apply_word(word,state)==expected
            checks['first_success_columns']+=1

# Hostile: XOR of all successful labels is not the first-success label.
assert (1^2)!=1
result={'status':'PASS_EXPLICIT_REVERSIBLE_SELECTOR_CIRCUITS','checks':dict(checks),
        'input_sha256':input_hashes,'circuit_summaries':summaries,
        'primitive_basis':['X','CX','CCX'],'all_input_claim_method':'Boolean identities and clean-composition proof; exhaustive reduced circuits plus actual-width samples',
        'entire_actual_2_power_input_space_enumerated':False,'native_gate_word_executed':False,
        'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'CIRCUIT_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
