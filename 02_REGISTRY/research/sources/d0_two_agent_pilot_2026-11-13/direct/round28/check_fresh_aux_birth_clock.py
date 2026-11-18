#!/usr/bin/env python3
"""Compact checks of the new input/birth contract; no huge word execution."""
from pathlib import Path
from collections import Counter
import hashlib,itertools,json
import fresh_aux_birth_clock as f
P=Path(__file__).resolve().parent
def main():
    plan=f.g.namespace();N=plan['layout']['qubits'];intervals=f.birth_blocks(plan)
    # Prove the partition via all finite endpoints and interval adjacency,
    # without expanding ten billion wire labels.
    unknown={0,1,3};bounds=sorted({0,N,*unknown,*[q+1 for q in unknown],*[v for b in intervals for v in (b['start'],b['stop'])]})
    cells=[]
    for a,b in zip(bounds,bounds[1:]):
        if a==b:continue
        covering=[z for z in intervals if z['start']<=a and b<=z['stop']]
        if a in unknown:assert b==a+1 and not covering
        else:assert len(covering)==1,(a,b,covering)
        cells.append([a,b,len(covering)])
    n,L,native=f.counts(plan);assert n==N-len(unknown)
    assert list(itertools.islice(f.births(plan),4))==[
        {'kind':'canonical_RAW_birth','wire':q,'role':role,'isometry':'psi -> psi tensor v on the new labelled factor','v':'(sqrt(p),p)'}
        for q,role in [(2705,'active_port_WORK'),(2,'fresh_aux_WORK'),(4,'SAM'),(5,'SAM')]]
    # A square unitary word of length L has L-1 square edges plus actual g.
    # Include every actual birth layer (0..n-1) and L final-sized layers.
    small=[]
    for births in range(1,9):
        for length in range(1,9):
            layer_dims=[2**k for k in range(births)]+[2**births]*length
            assert len(layer_dims)==births+length
            assert sum(layer_dims)==(length+1)*2**births-1
            small.append([births,length])
    # Iterator exercise with noncommuting actual native leaves and repeats.
    # It verifies paid closing-g selection, including one-letter word.
    old=(f.births,f.word_primitives);fixtures=[]
    def born(_):
        yield {'kind':'canonical_RAW_birth','wire':9}
        yield {'kind':'canonical_RAW_birth','wire':10}
    try:
        f.births=born
        words=[[f.g.nb.gate('G',9)],
               [f.g.nb.gate('G',9),f.g.nb.gate('CX',9,10),f.g.nb.gate('SourceI',9,0,1)]]
        for word in words:
            def primitives(_,w=word):yield from w
            f.word_primitives=primitives
            actual=list(f.execution_stages(plan))
            assert actual[:2]==list(born(plan)) and actual[-1]=={'kind':'final_unitary_g','gate':word[-1]}
            assert actual[2:-1]==[{'kind':'square_unitary_edge','gate':q} for q in word[:-1]]
            fixtures.append(len(word))
    finally:f.births,f.word_primitives=old
    tree=f.g.nb.seq(f.g.nb.repeat(3,f.g.nb.gate('G',2)),f.g.nb.gate('CX',2,2705))
    assert list(f.primitive_leaves(tree))==[f.g.nb.gate('G',2)]*3+[f.g.nb.gate('CX',2,2705)]
    pins=[Path(__file__),P/'fresh_aux_birth_clock.py',P/'FRESH_AUX_BIRTH_CLOCK_PLAN.json']
    out={'status':'PASS_COMPACT_FRESH_AUX_BIRTH_CLOCK_CONTRACT',
         'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
         'interval_partition_cells':cells,'all_numeric_wire_roles_covered_once':True,'unknown_wires_never_reborn':[0,1,3],
         'clock_layer_formula_small_exact_cases':len(small),'paid_last_gate_iterator_fixture_word_lengths':fixtures,
         'total_births':n,'word_count_consumed_from_reviewed_A25':str(L),'new_aux_birth_count':1,
         'full_giant_birth_or_unitary_stream_executed':False,'ST4_or_heat_neutrality_inferred':False,
         'physical_C_closed':False,'GR_closed':False}
    (P/'FRESH_AUX_BIRTH_CLOCK_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'partition_cells':len(cells),'clock_cases':len(small)}))
if __name__=='__main__':main()
