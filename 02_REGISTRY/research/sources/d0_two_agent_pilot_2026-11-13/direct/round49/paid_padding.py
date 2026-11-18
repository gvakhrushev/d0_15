#!/usr/bin/env python3
"""Actually emit counted finite padding; never rename an upper as a price."""
from collections import Counter
from pathlib import Path
import sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(D/'round42'))
import fixed_post_paid_family as old
native=old.native

def counted_pad(factory,total,sam,*,tag_ops=()):
    """One pass over DAG blocks, then paid identity of exactly total-used.

    The caller proves original length <=total-4. Actual used is computed
    from repeat multiplicities, not from a guessed price. Tags are zero
    operations and retain their actual prefix positions.
    """
    assert type(total) is int and total>=4 and len(sam)>=3
    used=0
    for tree in factory():
        if tree['op'] in tag_ops:yield tree;continue
        used+=sum(native.counts(tree).values())
        assert used<=total-4,'the promised original-word upper bound failed'
        yield tree
    yield from old.padding(total-used,tuple(sam))

def count(factory,*,tag_ops=()):
    out=Counter()
    for tree in factory():
        if tree['op'] not in tag_ops:out.update(native.counts(tree))
    return out
