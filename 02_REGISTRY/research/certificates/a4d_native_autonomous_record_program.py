#!/usr/bin/env python3
"""One fixed forward word for the retained-record engine, with its controller.

Coordinates are (constant record c, alternating record f, Fock mask).
The word never reads the sign of an amplitude. Its actual constant-one input
is retained. Both values of both records remain in the full 64-row operator.
The degree flag of the actual scene gives 359 copies of this block on all
718 directed edges. This is an exact construction in the explicitly addressed
golden/CNOT palette; physical admission and metric/refinement coupling remain
separate obligations.
"""
import argparse
from dataclasses import dataclass
import importlib.util
import json
from pathlib import Path
import sys

_path = Path(__file__).with_name('a4d_native_closed_record_engine.py')
_spec = importlib.util.spec_from_file_location('d0_retained_record_arithmetic', _path)
E = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = E
_spec.loader.exec_module(E)


@dataclass(frozen=True)
class ProgramState:
    coordinates: tuple

    def __post_init__(self):
        if not isinstance(self.coordinates, tuple) or len(self.coordinates) != 64:
            raise TypeError('ALL_64_CONTROLLER_AND_MATTER_COORDINATES_REQUIRED')
        if any(not isinstance(x,E.Golden) for x in self.coordinates):
            raise TypeError('EXACT_GOLDEN_COORDINATES_REQUIRED')


def cnot(state, control, target):
    if control == target or control not in range(6) or target not in range(6):
        raise ValueError('TWO_DISTINCT_DECLARED_BITS_REQUIRED')
    out = [E.ZERO]*64
    for index,value in enumerate(state.coordinates):
        destination = index ^ (1 << target) if index & (1 << control) else index
        out[destination] = value
    return ProgramState(tuple(out))


def occupancy_golden(state):
    out = [E.ZERO]*64
    for base in range(0,64,2):
        x,y = state.coordinates[base:base+2]
        out[base] = E.A*x-E.P*y
        out[base+1] = E.P*x+E.A*y
    return ProgramState(tuple(out))


def whole_positive_record(state):
    out = []
    for offset in range(0,64,16):
        block = E.State(state.coordinates[offset:offset+16])
        out.extend(E.literal_axis_gate(block,1).matter)
    return ProgramState(tuple(out))


def step(state):
    # Chronological order. The only tests inside CNOT concern fixed basis
    # labels; no sign, phase, norm, tick number or previous state is read.
    state = cnot(state,4,0)
    state = occupancy_golden(state)
    state = cnot(state,4,0)
    state = cnot(state,5,0)
    state = occupancy_golden(state)
    state = cnot(state,5,0)
    state = whole_positive_record(state)
    return cnot(state,5,4)


def seed(*, both_orientations=False):
    # The two fixed positive-record preparation operations are explicit.
    # No ongoing controller/reset depends on this preparation ordinal.
    astate = E.literal_axis_gate(E.literal_axis_gate(E.seed(),1),1)
    out = [E.ZERO]*64
    out[32:48] = astate.matter
    if both_orientations:
        out[48:64] = E.literal_axis_gate(astate,1).matter
    return ProgramState(tuple(out))


def norm_squared(state):
    return sum((v*v for v in state.coordinates),E.ZERO)


def persistent_bits(state):
    # Reuse exactly the prior self-delimiting signed-integer code. No free
    # real coordinates or metadata carrying a phase schedule are omitted.
    return sum(len(E.encode(E.State(state.coordinates[offset:offset+16])))
               for offset in range(0,64,16))


def scene_zone(vertex):
    if not 0 <= vertex < 33:
        raise ValueError('OUTSIDE_NATIVE_SCENE')
    return 0 if vertex < 9 else (1 if vertex < 20 else 2)


def scene_degree(vertex):
    return (24,22,20)[scene_zone(vertex)]


SCENE_EDGES = tuple((u,v) for u in range(33) for v in range(33) if scene_zone(u)!=scene_zone(v))


def edge_flag(edge):
    u,v = edge
    if (u,v) not in SCENE_EDGES:
        raise ValueError('NOT_AN_OWNED_SCENE_HISTORY')
    return int(scene_degree(u)>scene_degree(v))


BASE_EDGES = tuple(edge for edge in SCENE_EDGES if edge_flag(edge)==0)


def scene_seed():
    # All 718 edges have a nonzero first grade in the c=1 field.
    # Grouping reversal pairs is a reversible encoding, not edge deletion.
    return tuple(seed(both_orientations=True) for _ in BASE_EDGES)


def scene_step(state):
    if not isinstance(state,tuple) or len(state)!=len(BASE_EDGES):
        raise TypeError('ALL_359_NATIVE_REVERSAL_PAIRS_REQUIRED')
    return tuple(step(pair) for pair in state)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--steps',type=int,default=256)
    parser.add_argument('--scene',action='store_true')
    args = parser.parse_args()
    if args.steps < 0:
        parser.error('nonnegative steps required')
    state = scene_seed() if args.scene else seed()
    rows = []
    for ordinal in range(args.steps+1):
        if ordinal in {0,1,2,4,16,64,256,args.steps}:
            blocks = state if args.scene else (state,)
            rows.append({'diagnostic_iteration_not_program_input':ordinal,
                         'stored_coordinates':64*len(blocks),
                         'persistent_code_bits':sum(persistent_bits(v) for v in blocks)})
        if ordinal != args.steps:
            state = scene_step(state) if args.scene else step(state)
    print(json.dumps({'scope':'EXACT_ADDRESSED_FORWARD_WORD_NOT_PHYSICAL_ADMISSION',
                      'primitive_word_length':9,
                      'native_scene_vertices':33 if args.scene else None,
                      'native_scene_directed_edges':718 if args.scene else None,
                      'controller_records_retained':True,
                      'amplitude_sign_or_external_clock_read_by_program':False,
                      'rows':rows},indent=2))


if __name__=='__main__':
    main()
