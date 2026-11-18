#!/usr/bin/env python3
"""Literal A30 old-profile -> actual G/CX stream with two typed Q cuts.

Cuts are metadata, not free physical stages.  At each cut the source-I
transducer must have no pending half pair.  Full production stream is finite
but deliberately not walked by this module's checks.
"""
from pathlib import Path
import sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round30'))
import marked_source_schedule as source


def profile_with_cuts():
    """Old-profile literal word in actual chronological order plus cut tags."""
    stages=source.stages()
    for stage in stages:
        yield from source.stage_blocks(stage,0)
        if stage=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0}:
            yield {'op':'B82_CUT','name':'Qf_dagger_after_common_RAW_mark'}
    l=source.g.namespace()['layout']
    yield source.c.nb.z_word(l['port'],l['port'],tuple(l['spin']))
    for stage in reversed(stages):
        yield from source.stage_blocks(stage,1)
        if stage=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1}:
            yield {'op':'B82_CUT','name':'Qb_before_return_bank'}


def compiled_with_cuts():
    """Produce exactly A30's physical G/CX blocks and two cut markers.

    Do not consume for production numerical enumeration.  pending=0 at cuts
    ensures any SAM gate can be inserted without crossing a half SourceI pair.
    """
    compiler=source.c.production_compiler();pending=0
    for tree in profile_with_cuts():
        if tree['op']=='B82_CUT':
            assert pending==0,'source-I pair must not cross a Q cut'
            yield tree
            continue
        compiled,pending,_=compiler.transform(tree,pending)
        if compiled['op']!='seq' or compiled['children']:
            yield source.b.physical_tree(compiled)
    assert pending==0


def with_single_sam_word(cut,word):
    """Insert an explicitly provided native SAM-only DAG at one cut.

    word must be a nonempty G/CX seq/repeat DAG on physical SAM 2..2689.
    Qf_dagger and Qb are independent choices; a caller builds/pays each
    endpoint and pads its common clock.  These markers are removed.
    """
    assert cut in ('Qf_dagger_after_common_RAW_mark','Qb_before_return_bank')
    leaves=list(source.c.nb.leaves(word))
    assert leaves and all(g['op'] in ('G','CX') and all(2<=q<2690 for q in g['wires']) for g in leaves)
    for part in compiled_with_cuts():
        if part['op']=='B82_CUT':
            if part['name']==cut:yield word
        else:yield part


def small_cross_entry(total,sam,b,c,cut,tagged_factory):
    """Exact Q(a) cross-kernel on small examples only; never a giant table.

    Insert the matrix unit |c><b| at the selected cut by switching the SAM
    branch label; contract all other retained inputs with their actual born
    vector.  The <=12-WORK guard is explicit, not an admission assertion.
    """
    sys.path.insert(0,str(D/'round41'))
    import exact_target as e
    sam=tuple(sam);n=len(sam);assert len(set(sam))==n
    assert 0<=b<(1<<n) and 0<=c<(1<<n)
    assert cut in ('Qf_dagger_after_common_RAW_mark','Qb_before_return_bank')
    if total-n>12:raise NotImplementedError('actual giant cross-kernel is specified but not materialized')
    si={q:j for j,q in enumerate(sam)};work=[q for q in range(total) if q not in si]
    wi={q:j for j,q in enumerate(work)};v=e.born(len(work));state=list(v);branch=b;seen=0
    for tree in tagged_factory():
        if tree['op']=='B82_CUT':
            if tree['name']==cut:branch=c;seen+=1
            continue
        for gate in e.leaves(tree):
            op=gate['op'];w=gate['wires'];target=w[-1]
            assert target in wi and all(0<=q<total for q in w)
            t=1<<wi[target]
            if op=='G':
                for x in range(len(state)):
                    if x&t:continue
                    y=x|t;u,vv=state[x],state[y]
                    state[x],state[y]=e.A*u-e.SIN*vv,e.SIN*u+e.A*vv
            else:
                assert op=='CX' and len(w)==2 and w[0]!=w[1]
                control=w[0]
                for x in range(len(state)):
                    if x&t:continue
                    enabled=((branch>>si[control])&1) if control in si else ((x>>wi[control])&1)
                    if enabled:state[x],state[x|t]=state[x|t],state[x]
    assert seen==1 and branch==c
    return sum((x*y for x,y in zip(v,state)),e.Q4())
