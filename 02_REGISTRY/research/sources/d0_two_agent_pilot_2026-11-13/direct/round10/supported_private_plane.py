"""Exact r-controlled Golden planes for the small private correction arena.

Every signed plane expands into owned G/CX/SourceI calls. The completed
endpoint fixes the external record, source frame, Spin and every other
sector, including dirty helpers. No arbitrary controlled gate is primitive.
"""
from dataclasses import replace
import nps_private_recovery as nr
nt,phase=nr.native,nr.phase


def plane(layout,targets,record,value,i,j,sign=1):
    targets=tuple(targets);width=len(targets)
    if width!=3 or len(set(targets))!=3 or record in targets:
        raise nt.DomainError('three targets and a distinct external record required')
    if set(targets+(record,))&set((layout.source_port,*layout.source_spin,*layout.old_right)):
        raise nt.DomainError('target/record overlaps source or immutable support')
    if value not in (0,1) or sign not in (-1,1) or not(0<=i<8 and 0<=j<8) or i==j:
        raise nt.DomainError('bad selector or ordered plane')
    bits=lambda n:tuple((n>>(2-k))&1 for k in range(3))
    difference=bits(i^j);pivot=next(k for k in range(3) if difference[k])
    linear=tuple(nt.Gate('CX',(targets[pivot],targets[k])) for k in range(3)
                 if k!=pivot and difference[k])
    mapped=list(bits(i))
    for g in linear:mapped[targets.index(g.wires[1])]^=mapped[pivot]
    controls=(record,)+tuple(targets[k] for k in range(3) if k!=pivot)
    pattern=(value,)+tuple(mapped[k] for k in range(3) if k!=pivot)
    body=phase.phase_word(layout,controls,pattern,targets[pivot],4,
                         max_qubits=layout.qubits,max_expanded_stages=10000)
    if sign*(1 if mapped[pivot]==0 else -1)<0:
        body=nr.inverse(layout,body,10000)
    word=linear+body+tuple(reversed(linear))
    nt.validate_execution(replace(layout,gates=word),max_qubits=layout.qubits,max_expanded_stages=10000)
    if any(record in g.wires and not(g.op=='CX' and g.wires[0]==record) for g in word):
        raise ArithmeticError('external record became a target')
    return word
