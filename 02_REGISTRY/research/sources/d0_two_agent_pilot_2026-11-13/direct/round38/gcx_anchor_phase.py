#!/usr/bin/env python3
"""Consume B74's lazy AND; lower to certified positive G/CX only.

Scope: arbitrary control/phase-rebit input, CLEAN flag and comparator work,
arbitrary distinct helper. Births and preparation of clean bits are owed by
the full caller. No measurement, discarded column or implicit allocation.
"""
from pathlib import Path
import importlib.util
import gcx_post_macros as m
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round74/lazy_anchor_phase.py')
spec=importlib.util.spec_from_file_location('a38_owned_b74_predicate',B)
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
Ranges=b.Ranges


def logical_native(op,helper,macro):
    name,*w=op
    if name=='CX':return m.gate('CX',*w)
    if name=='X':return macro.x(w[0],helper)
    assert name=='CCX'
    return macro.ccx(*w,helper)


def zero_phase_blocks(controls,flag,work,rebit,helper,*,inverse=False,reflection=False,macro=None):
    """Approximate exact F^T phase F on the CLEAN comparator slice.

    Reverse uncomputation lowers exact logical X/CCX again. It is explicitly
    not the adjoint of the approximate forward word; error is paid twice.
    Range disjointness is a caller contract for scalable range descriptors;
    emitted gates independently reject local aliasing.
    """
    assert len(controls)>=3 and len(work)>=len(controls)-2
    assert len(set((flag,rebit,helper)))==3
    macro=macro or m.Macros()
    for op in b.zero_predicate_ir(controls,flag,work):yield logical_native(op,helper,macro)
    yield macro.z(flag,helper) if reflection else macro.controlled_pi3(flag,rebit,inverse)
    for op in b.zero_predicate_ir(controls,flag,work,reverse=True):yield logical_native(op,helper,macro)


def budget(N,macro=None,reflection=False):
    assert type(N) is int and N>=3
    macro=macro or m.Macros();k=macro.ks['pi8']
    return {'G':(400*N-504)*k if reflection else (400*N-520)*k+12*macro.ks['pi6'],
            'CX':116*N-160,
            'error_units':400*N-504 if reflection else 400*N-508,
            'clean_scratch':N-2,'clean_flags':1,'arbitrary_helpers':1}
