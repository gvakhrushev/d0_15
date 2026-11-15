#!/usr/bin/env python3
"""Exact finite counterexample for the vacuum-state/all-column boundary.

This is an illustrative typed fixture, not an original descriptor or detector.
The source pins below identify the documents whose claims are analyzed.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OPEN = HERE.parents[1]
PILOT_OPEN = OPEN.parents[1]
ROOT = PILOT_OPEN.parents[2]
owner = PILOT_OPEN / 'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
direct = ROOT / 'd0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct'
inputs = {
    'original_owner': owner,
    'A23_vacuum': direct / 'round23/CAR_VACUUM_FOURIER_RU.md',
    'A24_car': direct / 'round24/FULL_CAR_SOURCE_RU.md',
    'A48_global_source': direct / 'round48/two_bit_global_source.py',
    'B86_marks': OPEN / 'open/round86/B86_ORIGINAL_MARK_ADMISSION_RU.md',
    'B91_jet': OPEN / 'open/round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md',
    'B94_audit': OPEN / 'open/round94/B94_A48_INDEPENDENT_AUDIT_RU.md',
}

def matmul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def transpose(a): return list(map(list, zip(*a)))
def eye(n): return [[int(i == j) for j in range(n)] for i in range(n)]
def kron(a,b):
    return [[a[i//len(b)][j//len(b[0])] * b[i%len(b)][j%len(b[0])]
             for j in range(len(a[0])*len(b[0]))] for i in range(len(a)*len(b))]

i4 = eye(4)
p = [[int(i == j) * [1,-1,-1,1][i] for j in range(4)] for i in range(4)]
e = [[int((i,j) in ((0,1),(1,0))) for j in range(4)] for i in range(4)]
j = [[0,-1],[1,0]]
dm = kron(j, eye(2))
assert matmul(transpose(p),p)==i4 and [p[i][i] for i in range(4)].count(-1)==2
assert [p[i][0] for i in range(4)] == [1,0,0,0]
assert matmul(matmul(transpose(p),e),p)==[[-x for x in row] for row in e]
assert matmul(dm,p)!=dm
old_x = [[0,1],[1,0]]
assert matmul(kron(p,eye(2)),kron(eye(4),old_x)) == matmul(kron(eye(4),old_x),kron(p,eye(2)))

checks = {
    'fixture_both_are_real_SO': True,
    'fixture_same_declared_vacuum_column': True,
    'fixture_old_right_exact_identity_factor': True,
    'fixture_off_diagonal_effect_pullback_opposite': True,
    'fixture_full_column_material_jet_differs': True,
    'fixture_is_original_admission_evidence': False,
    'fixture_is_registered_original_effect': False,
}
res = {'checks': checks, 'input_sha256': {k: hashlib.sha256(v.read_bytes()).hexdigest() for k,v in inputs.items()},
       'source_map_owner_matched': False, 'original_descriptor_admitted': False,
       'physical_C_closed': False, 'GR_closed': False}
(HERE / 'B99_VACUUM_EXTENSION_CHECK.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
