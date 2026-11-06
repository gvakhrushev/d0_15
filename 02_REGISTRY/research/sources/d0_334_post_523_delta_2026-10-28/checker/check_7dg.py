#!/usr/bin/env python3
"""Exact paired-port AF factorization, not native physical port admission.

Run from repository root, or pass --repo. All complements and Spin columns
are kept. The addressed AF calls below are NOT Execution/1 wire programs.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import sympy as s

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=Path.cwd())
args = parser.parse_args()
ROOT = args.repo.resolve()

def module(name, rel):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result, hashlib.sha256(path.read_bytes()).hexdigest()

AF, af_sha = module('golden_frame_owned',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py')
N, native_sha = module('golden_word_owned',
    '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py')
a, p = AF.a, AF.p
labels = []

def require(condition, label):
    if not condition:
        raise RuntimeError(label)
    labels.append(label)

def mat(A):
    return s.SparseMatrix(AF.mat(A))

def equal(A, B, label):
    require(AF.zero(A-B), label)

def paths(state, remaining, prefix=()):
    if not remaining:
        return [prefix]
    successors = (0, 1) if state == 0 else (0,)
    return [q for nxt in successors
            for q in paths(nxt, remaining-1, prefix+(nxt,))]

def pairs(state, remaining, prefix=()):
    if not remaining:
        return []
    if state == 1:
        return pairs(0, remaining-1, prefix+(0,))
    left = paths(0, remaining-1, prefix+(0,))[0]
    right = paths(1, remaining-1, prefix+(1,))[0]
    return ([(left, right)] + pairs(0, remaining-1, prefix+(0,))
            + pairs(1, remaining-1, prefix+(1,)))

def rotation(dimension, row_pairs):
    G = s.MutableSparseMatrix(s.eye(dimension))
    for i, j in row_pairs:
        G[i, i] = G[j, j] = a
        G[i, j], G[j, i] = -p, p
    return s.SparseMatrix(G)

def circuit(n):
    f = AF.frame(n)
    old, fine = f['old_coordinates'], f['fine_coordinates']
    index = {coord: i for i, coord in enumerate(fine)}
    address = {(j, path): (v, offset)
               for v, block in enumerate(f['segments'])
               for j, path, offset in block}
    def row(j, path, r, c):
        v, off = address[j, path]
        return index[v, off+r, off+c]
    operations = []
    for j in (0, 1):
        size = f['old_sizes'][j]
        for left, right in pairs(j, 3):
            row_pairs = [(row(j, left, r, c), row(j, right, r, c))
                         for r in range(size) for c in range(size)]
            operations.append({'type': j, 'left': left, 'right': right,
                               'rows': row_pairs})
    E = s.MutableSparseMatrix(len(fine), 4*len(old), {})
    for k, (j, r, c) in enumerate(old):
        first, second = [off for kind, path, off in f['segments'][0]
                         if kind == j][:2]
        selected = [row(j, paths(j, 3)[0], r, c),
                    index[0, first+r, second+c],
                    index[0, second+r, first+c],
                    row(j, pairs(j, 3)[-1][1], r, c)]
        for work, i in enumerate(selected):
            E[i, work*len(old)+k] = 1
    return f, operations, s.SparseMatrix(E)

def product(matrices, dimension):
    W = s.SparseMatrix(s.eye(dimension))
    for g in matrices:
        W = mat(g*W)
    return W

# This proof is uniform in the old matrix sizes; exercise both noncommuting
# old summands as well as the smallest and a larger AF level.
level_rows = []
for n in range(4):
    f, operations, E = circuit(n)
    d, D = f['old_dimension'], len(f['fine_coordinates'])
    V = E
    for op in operations:
        V = mat(rotation(D, op['rows'])*V)
    equal(E.T*E, s.eye(4*d), 'coordinate frame isometry n='+str(n))
    equal(V.T*V, s.eye(4*d), 'Gold-only frame isometry n='+str(n))
    equal(V[:, :d], f['V'][:, :d], 'canonical J on every old column n='+str(n))
    equal(V[:, d:3*d], E[:, d:3*d], 'off-copy frames stay fixed n='+str(n))
    require(len(operations) == 6, 'four plus two branch rotations n='+str(n))
    require(not any(x.has(s.sqrt(2)) for x in V), 'no sqrt2 frame coefficients n='+str(n))
    level_rows.append({'n': n, 'old': d, 'fine': D, 'coordinate_rank': 4*d})
    if n == 2:
        B2 = product([rotation(D, op['rows']) for op in operations], D)
        fine_index = {coord:i for i, coord in enumerate(f['fine_coordinates'])}
        for j, size in enumerate(f['old_sizes']):
            for r in range(size):
                for c in range(size):
                    L, R = (s.MutableSparseMatrix(D, D, {}) for _ in range(2))
                    for v, block in enumerate(f['segments']):
                        for kind, path, off in block:
                            if kind != j:
                                continue
                            for k in range(f['fine_sizes'][v]):
                                L[fine_index[v, off+r, k], fine_index[v, off+c, k]] = 1
                                R[fine_index[v, k, off+c], fine_index[v, k, off+r]] = 1
                    equal(B2*L, L*B2, 'left intertwining '+str((j,r,c)))
                    equal(B2*R, R*B2, 'right intertwining '+str((j,r,c)))

f, operations, E = circuit(0)
d, D = f['old_dimension'], len(f['fine_coordinates'])
B = product([rotation(D, op['rows']) for op in operations], D)
equal(B.T*B, s.eye(D), 'all-column branch unitary')
V = mat(B*E)
J = f['V'][:, :d]

# A real seven-stage native word: G; CX; SourceI; SourceI; G; SourceI; SourceI.
# The last five calls are the original full-Spin inverse of the first G.
g = N.Gate('G', (0,))
cx = N.Gate('CX', (0, 1))
si = N.Gate('SourceI', (0, 2, 3))
gates = (g, cx, si, si, g, si, si)
word = N.Execution(4, (0, 1), (), gates, N.G_CX_SOURCE_I, 0, (2, 3))
N.validate_execution(word, max_qubits=4, max_expanded_stages=7)

def symbolic(A):
    return mat(A.xreplace({N.A:a}).xreplace({s.sqrt(5):2*p+1}))

native_primitives = [symbolic(N.gate_matrix(word, gate)) for gate in gates]
W = product(native_primitives, 16)
P = symbolic(N.cut_projector(word))
equal(P, s.diag(*([1]*4+[0]*12)), 'both WORK bits only are blank')
equal(W.T, W, 'logical endpoint selfadjoint')
equal(W*W, s.eye(16), 'logical endpoint reflection')
equal(P*W*P, p*P, 'logical whole-Spin scalar corner')
equal(P*W.T*(s.eye(16)-P)*W*P, p*P, 'logical feedback p')

# Columns: (WORK, Spin, old); rows: (fineAF, Spin).
TE = s.MutableSparseMatrix(4*D, 16*d, {})
for work in range(4):
    for spin in range(4):
        for old in range(d):
            col = (4*work+spin)*d+old
            for row in range(D):
                if E[row, work*d+old]:
                    TE[4*row+spin, col] = E[row, work*d+old]
TE = s.SparseMatrix(TE)
BS = s.kronecker_product(B, s.eye(4))
T = mat(BS*TE)
I = s.SparseMatrix(s.eye(4*D))
RE = mat(TE*TE.T)
RT = mat(T*T.T)
equal(TE.T*TE, s.eye(16*d), 'coordinate logical transport all columns')
equal(T.T*T, s.eye(16*d), 'encoded logical transport all columns')
for spin in range(4):
    for old in range(d):
        equal(T[:, spin*d+old], s.kronecker_product(J[:,old],s.eye(4)[:,spin]),
              'unknown old and Spin input '+str((spin,old)))

# Expand each AF Golden inverse as Si;Si;G;Si;Si on that specified pair.
# These are paired-port matrix calls, not native_execution wire codes.
branch_gates, branch_sources = [], []
for op in operations:
    G = s.kronecker_product(rotation(D, op['rows']), s.eye(4))
    S = s.MutableSparseMatrix(I)
    for first, second in op['rows']:
        for r in range(4):
            for c in range(4):
                S[4*second+r, 4*second+c] = N.L_I[r,c]
    S = s.SparseMatrix(S)
    equal(S.T*S, I, 'all-Spin SourceI on '+str((op['type'],op['right'])))
    equal(product([S,S,G,S,S],4*D), G.T,
          'five-forward-call inverse '+str((op['type'],op['left'],op['right'])))
    branch_gates.append(mat(G))
    branch_sources.append(S)

prefix, names = [], []
for G,S in reversed(list(zip(branch_gates,branch_sources))):
    prefix.extend([S,S,G,S,S]); names.extend(['SourceI','SourceI','G','SourceI','SourceI'])
equal(product(prefix,4*D), BS.T, '30-call exact input decode')
middle = [mat(TE*s.kronecker_product(g,s.eye(d))*TE.T+I-RE)
          for g in native_primitives]
schedule = prefix+middle+branch_gates
names += [gate.op for gate in gates]+['G']*6
actual = product(schedule,4*D)
expected = mat(T*s.kronecker_product(W,s.eye(d))*T.T+I-RT)
equal(actual, expected, '43 actual calls on every column including complement')
equal(actual.T, actual, 'whole endpoint selfadjoint')
equal(actual*actual, I, 'whole endpoint reflection')
Ptrue = mat(T*s.kronecker_product(P,s.eye(d))*T.T)
equal(Ptrue, s.kronecker_product(J*J.T,s.eye(4)), 'cut is original canonical J')
equal(Ptrue*actual*Ptrue, p*Ptrue, 'true canonical corner all inputs')
F = mat(Ptrue*actual.T*(I-Ptrue)*actual*Ptrue)
equal(F,p*Ptrue,'complete canonical feedback p')
require(AF.red(s.trace(Ptrue)) == 8, 'true protected rank 8')
require(AF.red(s.trace(actual)) == 120, 'whole reflection multiplicities 128 and 8')
require(AF.red(s.trace(I-RT)) == 104, 'whole retained complement 104')
require(Counter(names) == {'G':14,'CX':1,'SourceI':28} and len(schedule)==43,
        'expanded actual paired-port inventory')

# Also execute the original two-call Golden recording step itself, not just
# a reflected diagnostic. Its fourth frame is the new Golden sibling frame.
equal(product(native_primitives[:2],16),
      s.kronecker_product(AF.record(),s.eye(4)), 'original full recording matrix')
record_schedule = prefix+middle[:2]+branch_gates
record_names = names[:30]+['G','CX']+['G']*6
record_actual = product(record_schedule,4*D)
record_expected = mat(T*s.kronecker_product(AF.record(),s.eye(4*d))*T.T+I-RT)
equal(record_actual,record_expected,'38-call original record on all columns')
equal(record_actual.T*record_actual,I,'whole original record unitary')
input_columns = T[:,:4*d]
detail_columns = T[:,12*d:16*d]
equal(record_actual*input_columns,a*input_columns+p*detail_columns,
      'unknown input produces its own Golden sibling record')
equal(input_columns.T*detail_columns,s.zeros(4*d), 'new detail orthogonal to old input')
equal(Ptrue*record_actual.T*(I-Ptrue)*record_actual*Ptrue,p**2*Ptrue,
      'original recording feedback p squared')
require(len(record_schedule)==38 and Counter(record_names)=={'G':13,'CX':1,'SourceI':24},
        'expanded actual original-record inventory')

# Hostile controls: no fake blank by changing the cut; no omitted encoding.
Pcoordinate = mat(TE*s.kronecker_product(P,s.eye(d))*TE.T)
require(not AF.zero(Ptrue-Pcoordinate), 'coordinate blank is not canonical input')
unencoded = product(middle,4*D)
require(not AF.zero(Ptrue*unencoded*Ptrue-p*Ptrue), 'missing frame calls change true corner')
bad_prefix = product(branch_gates,4*D)  # replacing inverse by forward is not valid
require(not AF.zero(bad_prefix-BS.T), 'forward branch is not a free inverse')
require(not AF.zero(f['V'][:,3*d:]-V[:,3*d:]), 'old sqrt2 fourth frame has changed')
require((4*D)&(4*D-1) != 0, '136-dimensional calls cannot be silently wire Execution/1')

result = {
    'status':'PASS', 'checks':len(labels),
    'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'frame_owner_sha256':af_sha, 'native_owner_sha256':native_sha,
    'field_relations':['a^2=p','p^2+p=1','a>0','p>0'],
    'levels':level_rows,
    'branch_pairs':[{'old_type':op['type'], 'first':list(op['left']),
                     'second':list(op['right'])} for op in operations],
    'native_middle':{'stages':7,'G':2,'CX':1,'SourceI':4,'dimension':16},
    'paired_port_schedule':{'stages':43,'G':14,'CX':1,'SourceI':28,
        'dimension':4*D,'input_rank':8,'complement_dimension':104,
        'reflection_plus':128,'reflection_minus':8,'feedback':'p Ptrue'},
    'original_record_schedule':{'stages':38,'G':13,'CX':1,'SourceI':24,
        'dimension':4*D,'input_rank':8,'feedback':'p^2 Ptrue',
        'input_action':'a J input + p V3 input'},
    'checks_executed':labels,
    'scope':'exact specified AF paired-port circuit and complete input/source transport',
    'physical_AF_port_addressability_proved':False,
    'physical_AF_growth_cost_supplied':False,
    'wire_execution_domain_membership_claimed':False,
    'GR_closed':False,
}
print(json.dumps(result,indent=2))
