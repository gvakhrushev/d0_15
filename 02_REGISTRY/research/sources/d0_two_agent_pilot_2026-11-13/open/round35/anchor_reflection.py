#!/usr/bin/env python3
"""Explicit paid native joint-anchor reflection from owned A16/A14.

The caller supplies all addressed wires and computational-zero flag/work.
The returned DAG is finite; no gate acts directly on protected spectators.
"""
from pathlib import Path
import importlib.util,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
spec=importlib.util.spec_from_file_location('b35_anchor_a16',D/'round16/source_select.py');a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)

def build(controls,pattern,flag,work,port,spin,aux,k,protected=()):
    """Return actual G/CX/SourceI DAG for F† Z_flag F; caller pays F and F†.

    controls include DATA and any U-private clean work. The tested anchor is
    `pattern`; flag/work start 0. A separate native port and arbitrary Spin,
    auxiliary and protected external factors follow owned A14 semantics.
    """
    controls=list(controls);work=list(work);spin=tuple(spin);protected=set(protected)
    n=len(controls);assert n>=2 and len(work)>=n-2 and len(spin)==2
    all_roles=controls+[flag]+work+[port,*spin,aux]
    assert len(all_roles)==len(set(all_roles)) and not protected.intersection(all_roles)
    predicate=list(a.logic.pattern_gate(controls,pattern,flag,work))
    ideal=a.conjugate(a.primitive_word(predicate),a.gate('Z',flag))
    native=a.lower(ideal,k,port,spin,aux)
    for leaf in a.nb.leaves(native):
        assert not protected.intersection(leaf['wires'])
        if leaf['op'] in ('G','CX'):assert leaf['wires'][-1] not in controls
    return {'ideal_IR':ideal,'native_DAG':native,'predicate_counts':dict(__import__('collections').Counter(g[0] for g in predicate)),
            'approximate_macro_occurrences':sum(2 for op,*_ in predicate if op in ('X','CCX')),
            'literal_inverse_DAG':a.nb.inverse_literal(native,port,spin)}
