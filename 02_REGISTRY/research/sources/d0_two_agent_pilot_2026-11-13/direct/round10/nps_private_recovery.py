#!/usr/bin/env python3
"""Actual inverse/phase words for private-dilation recovery of noisy NPS.

The constructor consumes a real square NPS word and a separately verified
scalar-effect/born-input contract. It does not choose a physical task or
declare an arbitrary supplied factory to be the full geometric H.1 writer.
"""
from dataclasses import replace
from pathlib import Path
from collections import Counter
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'inputs/d0_native_readiness_amplification_2026-10-24'))
import native_phase as phase
native=phase.native


def counts(word):
    c=Counter(g.op for g in word)
    return {'G':c['G'],'CX':c['CX'],'SourceI':c['SourceI'],'N':len(word)}


def inverse(layout,word,limit):
    return native.inverse_word(replace(layout,gates=tuple(word)),max_qubits=layout.qubits,
                               max_expanded_stages=limit)


def private_recovery(base,*,processor_blanks,record,pointer,tail,rebit,rounds,
                     protected=(),limit=2000000):
    """Return fresh-private-bit preparation and complete literal A_n dagger.

    processor_blanks are the ACTUAL canonical input of square A, including
    its private pointer and tail, excluding the exterior record/tail and
    phase helpers. P0 never tests Spin, oldRIGHT, or phase-rebit input.
    All code bounds are ordinary declared finite bounds, not admission.
    """
    bounds={'max_qubits':base.qubits,'max_expanded_stages':limit}
    native.validate_execution(base,**bounds)
    processor_blanks=tuple(processor_blanks)
    protected=set(protected)|(set((record,rebit)))
    if rounds<0 or type(rounds) is not int:
        raise native.DomainError('nonnegative integer rounds required')
    if len(set(processor_blanks))!=len(processor_blanks):
        raise native.DomainError('repeated processor blank')
    if not {pointer,tail}<=set(processor_blanks):
        raise native.DomainError('private pointer and tail must belong to actual born input')
    if set(processor_blanks)&(protected|set(base.old_right)|set(base.source_spin)):
        raise native.DomainError('P0 cannot test an external/unknown protected input')
    if not set(processor_blanks)<=set(base.blank_wires):
        raise native.DomainError('every P0 bit must be an actual canonical birth')
    if any(protected.intersection(g.wires) for g in base.gates):
        raise native.DomainError('base square word touches exterior record/tail or phase rebit')
    if record==base.source_port or record in base.source_spin or record in base.old_right:
        raise native.DomainError('external record must be a separate live WORK bit')
    Kmax=max(len(processor_blanks),2)
    cert=phase.find_stable_native_phase(Kmax,10000,bits=128)
    kin=phase.matched_phase_index(Kmax,len(processor_blanks),cert['k'])
    keq=phase.matched_phase_index(Kmax,2,cert['k'])
    # The actual P0 is born v, not zero. Both frame changes are paid.
    prepare=tuple(native.Gate('G',(q,)) for q in processor_blanks)
    unprepare=inverse(base,prepare,limit)
    initial=unprepare+phase.phase_word(base,processor_blanks,(0,)*len(processor_blanks),
                                     rebit,kin,**bounds)+prepare
    # Two disjoint matched patterns give the same phase for r'=record.
    equal=phase.phase_word(base,(pointer,record),(0,0),rebit,keq,**bounds)
    equal+=phase.phase_word(base,(pointer,record),(1,1),rebit,keq,**bounds)
    current=tuple(base.gates)
    levels=[counts(current)]
    for _ in range(rounds):
        inv=inverse(base,current,limit)
        if 2*len(current)+len(inv)+len(initial)+len(equal)>limit:
            raise native.DomainError('complete expanded amplifier exceeds declared finite limit')
        current=current+equal+inv+initial+current
        native.validate_execution(replace(base,gates=current),**bounds)
        levels.append(counts(current))
    recovery=inverse(base,current,limit)
    # These are fresh canonical private r',t', not uninitialised zero bits.
    private_pre=inverse(base,(native.Gate('G',(pointer,)),native.Gate('G',(tail,))),limit)
    private_pre+=(native.Gate('CX',(record,pointer)),)
    for g in private_pre+recovery:
        if record in g.wires and not (g.op=='CX' and g.wires[0]==record):
            raise ArithmeticError('external record is not control-only')
    return {'private_preparation':private_pre,'amplifier':current,'recovery':recovery,
            'initial_phase':initial,'equal_phase':equal,'levels':levels,
            'phase_certificate':cert,'rounds':rounds}


def fixture(twist_spin=False):
    """Literal small NPS example; a validation fixture, not the H.1 field bank.

    source/sign port0, opaque Spin1,2; private pointer3,tail4;
    existing outer record5,tail6; born phase rebit7.
    """
    layout=native.Execution(8,(0,3,4,5,6,7),(),(),native.G_CX_SOURCE_I,0,(1,2),(5,6))
    CX=lambda c,t:native.Gate('CX',(c,t))
    SI=native.Gate('SourceI',(0,1,2))
    sw=lambda q:(CX(0,q),CX(q,0),CX(0,q))
    # Preserve the exact 36-call B17 echo, rather than shorten an old prefix.
    z=sw(4)+(SI,SI)+sw(4)
    gi17=z+(native.Gate('G',(4,)),)+z
    echo=(CX(3,4),)+gi17+(CX(3,4),)+gi17
    af=(native.Gate('G',(0,)),)*3
    abinv=inverse(layout,af,10000)
    E0=(CX(3,4),native.Gate('G',(4,)),CX(3,4))
    # A_b=SourceI*A_f gives a true Spin-coupled branch without changing its
    # scalar probability. It exercises the case unavailable to WORK-only SO.
    backward=((SI,)*3 if twist_spin else ())+abinv
    word=af+(CX(0,3),SI,SI)+backward+E0+echo
    return replace(layout,gates=word)
