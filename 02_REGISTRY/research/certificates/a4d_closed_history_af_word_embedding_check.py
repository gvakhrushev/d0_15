#!/usr/bin/env python3
"""Bounded exact full-column check of the generic AF whole-word lemma.

The native eight-stage word has an arbitrary four-dimensional Spin input.
Only its one WORK bit is born in an actual Fibonacci frame. This does not
establish physical addressability of the transported alphabet.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sympy as sp

REPO = Path(__file__).resolve().parents[3]

def module(name, rel):
    path = REPO / rel
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result, hashlib.sha256(path.read_bytes()).hexdigest()

AF, af_sha = module('af_frame_owned', '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py')
N, native_sha = module('native_word_owned', '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py')

checks = 0
def require(condition, label):
    global checks
    if not condition:
        raise RuntimeError(label)
    checks += 1

def equal(A, B, label):
    require(AF.zero(A-B), label)

# The original chronological inverse of G is SourceI^2;G;SourceI^2.
# Middle SourceI^2 is the literal fixed reflection; it is not a new gate.
g = N.Gate('G', (0,))
si = N.Gate('SourceI', (0, 1, 2))
gates = (g, si, si, si, si, g, si, si)
word = N.Execution(3, (0,), (), gates, N.G_CX_SOURCE_I, 0, (1, 2))
N.validate_execution(word, max_qubits=3, max_expanded_stages=8)
require(len(gates) == 8, 'full actual chronology')

def native_symbolic(matrix):
    # Replace the amplitude first, then the expanded +/- golden root entries.
    # Canonical SymPy -P is an expanded Add and does not contain P as a node.
    result = matrix.xreplace({N.A: AF.a})
    result = result.xreplace({sp.sqrt(5): 2*AF.p+1})
    return sp.SparseMatrix(AF.mat(result))

primitives = [native_symbolic(N.gate_matrix(word, gate)) for gate in gates]
W = sp.eye(8)
for matrix in primitives:
    W = AF.mat(matrix * W)
P = native_symbolic(N.cut_projector(word))
equal(P, sp.diag(1,1,1,1,0,0,0,0), 'arbitrary entire Spin input')
equal(W.T, W, 'native endpoint selfadjoint')
equal(W*W, sp.eye(8), 'native endpoint reflection')
equal(P*W*P, AF.p**3*P, 'true scalar corner on all Spin columns')
F = AF.mat(P*W.T*(sp.eye(8)-P)*W*P)
equal(F, 4*AF.p**3*P, 'complete endpoint feedback')

frame = AF.frame(0)
old = frame['old_dimension']
fine = len(frame['fine_coordinates'])
V = frame['V'][:, :2*old]  # fixed first two actual frame paths, not all four
equal(V.T*V, sp.eye(2*old), 'selected whole-work frame isometry')
J = frame['V'][:, :old]

# Columns have order (work,Spin,oldAF), rows (fineAF,Spin).
T = sp.MutableSparseMatrix(4*fine, 8*old, {})
for work in range(2):
    for spin in range(4):
        for old_index in range(old):
            col = (4*work+spin)*old+old_index
            for row in range(fine):
                value = V[row,work*old+old_index]
                if value != 0:
                    T[4*row+spin,col] = value
equal(T.T*T, sp.eye(8*old), 'full old-state and Spin isometry')

# Compare every arbitrary input column; no Spin basis vector is prepared.
for spin in range(4):
    for old_index in range(old):
        actual = T[:,spin*old+old_index]
        expected = sp.kronecker_product(J[:,old_index],sp.eye(4)[:,spin])
        equal(actual,expected,'canonical initial image on arbitrary Spin')

R = AF.mat(T*T.T)
I = sp.eye(4*fine)
lifted = [AF.mat(T*sp.kronecker_product(a,sp.eye(old))*T.T+I-R)
          for a in primitives]
# Test the actual chronological product on ALL columns, including complement.
Wp = sp.eye(4*fine)
for a in lifted:
    Wp = AF.mat(a*Wp)
expected = AF.mat(T*sp.kronecker_product(W,sp.eye(old))*T.T+I-R)
equal(Wp,expected,'full primitive product and identity complement')
Pp = AF.mat(T*sp.kronecker_product(P,sp.eye(old))*T.T)
equal(Pp*Pp,Pp,'true lifted cut')
Fp = AF.mat(Pp*Wp.T*(I-Pp)*Wp*Pp)
equal(Fp,T*sp.kronecker_product(F,sp.eye(old))*T.T,'complete source multiplicity')
equal(Wp*Wp,I,'all-column reflected heat hypothesis')
equal(Wp.T,Wp,'all-column Hermitian reflected heat hypothesis')
require(AF.red(sp.trace(Pp)) == 8,'true protected rank')
require(AF.red(sp.trace(Wp)) == 120,'retained whole complement spectrum')
require(fine == 34 and old == 2,'actual AF carrier sizes')

result = {
    'status':'PASS', 'checks':checks,
    'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'native_owner_sha256':native_sha,
    'frame_owner_sha256':af_sha,
    'native_word':{'G':2,'CX':0,'SourceI':6,'stages':8,
                   'dimension':8,'arbitrary_spin_dimension':4},
    'full_working_lift':{'dimension':4*fine,'input_rank':8,
                         'old_AF_multiplicity':old,
                         'complement_dimension':4*fine-8*old,
                         'reflection_plus_dimension':128,
                         'reflection_minus_dimension':8},
    'scope':'exact full-column primitive and input transport; no physical frame-addressability assertion',
}
print(json.dumps(result,indent=2))
