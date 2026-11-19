"""All-input native NC1 seed registration and its own complete master clock.

The isolated registration gadget is not the full seed/factory/reader clock
and does not choose physical Book Cost-Info. No known-one is postselected.
"""
from collections import Counter
import math
import numpy as np
import scipy.sparse as sparse
from scipy.linalg import eigvalsh

from check_local_gibbs_records import mm, scene
from check_source_price import load_control, need


def make_clock(stages):
    prefix, last = stages[:-1], stages[-1][0]
    dims = [stages[0][0].shape[1]] + [s[0].shape[0] for s in prefix]
    offsets = np.cumsum([0] + dims)
    clock = np.zeros((offsets[-1], offsets[-1]))
    for j, (real, _, _) in enumerate(prefix):
        clock[offsets[j+1]:offsets[j+2], offsets[j]:offsets[j+1]] = real
    emb = np.eye(last.shape[0])
    for j in range(len(prefix), -1, -1):
        if j < len(prefix):
            emb = mm(emb, prefix[j][1])
        if j == 0:
            extra = np.eye(dims[j])
        elif prefix[j-1][2] == 'birth':
            b = prefix[j-1][1]
            extra = np.eye(dims[j]) - mm(b, b.T)
        else:
            continue
        clock[offsets[j]:offsets[j+1], offsets[-2]:offsets[-1]] = mm(extra, emb.T, last)
    sc = sparse.csr_matrix(clock)
    error = sc.T @ sc - sparse.eye(len(clock), format='csr')
    need((max(abs(error.data)) if error.nnz else 0.0) < 4e-13,
         'all clock birth complements are retained')
    return clock


def main():
    ne, digest = load_control()
    p, a = float(ne.P), float(ne.A)
    exact_a, exact_p = ne.A, ne.P
    exact_identities = [exact_a**2-exact_p,
                        exact_p**2+exact_p-1,
                        exact_a**4+exact_a**2-1]
    need(all(ne.GOLDEN_FIELD.from_sympy(x) == ne.GOLDEN_FIELD.zero
             for x in exact_identities), 'exact native golden field identities')
    gate, profile = ne.Gate, ne.G_CX_SOURCE_I
    source = dict(profile=profile, source_port=1, source_spin=(2, 3))
    inv_spec = ne.Execution(6, (), (), (gate('G', (5,)),), **source)
    inv = ne.inverse_word(inv_spec, max_qubits=6, max_expanded_stages=100)
    need(Counter(g.op for g in inv) == Counter({'CX': 6, 'SourceI': 4, 'G': 1}),
         'actual routed inverse G has every original gate')
    current, stages = 4, []
    def birth():
        nonlocal current
        b = np.kron(np.eye(1 << current), np.array([[a], [p]]))
        stages.append((b, b, 'birth'))
        current += 1
    def append(g):
        spec = ne.Execution(current, (), (), (g,), **source)
        m = np.array(ne.gate_matrix(spec, g, max_qubits=6, max_expanded_stages=100), dtype=float)
        stages.append((m, np.eye(1 << current), g.op))
    birth()  # native tail on wire 4
    for g in (gate('CX', (0, 4)), gate('G', (4,)), gate('CX', (0, 4))):
        append(g)
    partial = np.eye(16)
    for real, _, _ in stages:
        partial = mm(real, partial)
    birth()  # orthogonal record environment on wire 5
    for g in inv:
        append(g)
    append(gate('CX', (0, 5)))
    need(len(stages) == 17, 'two births plus 15 square gates')
    need(Counter(t for _, _, t in stages) == Counter({'birth': 2, 'CX': 9, 'G': 2, 'SourceI': 4}),
         'full actual gate inventory')
    V = E = np.eye(16)
    for real, passive, _ in stages:
        V, E = mm(real, V), mm(passive, E)
    need(np.max(np.abs(mm(V.T,V)-np.eye(16))) < 5e-13, 'all 16 old-input columns')
    C = mm(E.T, V)
    expected = np.diag([p]*8+[a*p]*8)
    need(np.max(np.abs(C-expected)) < 5e-13, 'true passive-birth compression')
    # r=1,tail=1 is dark on every old input, including coherent references.
    bits = np.arange(32)
    r0, tail0 = (bits >> 4) & 1, bits & 1
    need(np.linalg.norm(partial[(r0 == 1) & (tail0 == 1)]) < 5e-13, 'NC1 dark 11')
    out_env = np.arange(64) & 1
    for outcome in (0, 1):
        measured = partial.copy()
        measured[r0 != outcome] = 0
        for real, _, _ in stages[4:]:
            measured = mm(real, measured)
        retained = V.copy()
        retained[out_env != outcome] = 0
        need(np.linalg.norm(measured-retained) < 1e-12,
             'actual NC1 projector equals retained orthogonal environment')
    clock = make_clock(stages)
    D = len(clock)
    need(D == 912, 'complete clock dimension')
    z = 2**-20
    J = -8*(math.log1p(-z*(1-p*p))+math.log1p(-z*(1-p**3)))
    fb = np.eye(16)-mm(C.T, C)
    actual_J = -np.linalg.slogdet(np.eye(16)-z*fb)[1]
    need(abs(J-actual_J) < 1e-13, 'full-rank native feedback determinant')
    beta = 2*p*p
    B, S = scene()
    def heat(full_clock):
        vals = eigvalsh(full_clock+full_clock.T, check_finite=False)
        # Every clock eigenvalue and both Hodge degrees are included.
        value = 359*len(full_clock)
        for lam in vals:
            eig = eigvalsh(np.eye(len(B))-B-lam*S, check_finite=False)
            value += 2*float(np.exp(-beta*eig).sum())
        return value
    zh = heat(clock)
    master = math.log(zh)/beta+J
    baseline = make_clock(stages[:4])
    need(len(baseline) == 112, 'baseline literal NC1 clock')
    base_j = -16*math.log1p(-z*(1-p))
    base_zh = heat(baseline)
    base_master = math.log(base_zh)/beta + base_j
    # Native counterexample on existing seed U=H: undo CX, apply G on H,
    # then register H. A seed measurement dephases the prior entanglement.
    psi = np.array([a, 0., 0., p])
    rho = np.outer(psi, psi)
    rho_read = np.diag(np.diag(rho))
    cx = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=float)
    g = np.array([[a,-p],[p,a]])
    after = mm(np.kron(g, np.eye(2)), cx)
    projector = np.diag([0,0,1,1])
    coherent = np.trace(mm(projector,after,rho,after.T))
    dephased = np.trace(mm(projector,after,rho_read,after.T))
    need(abs(coherent-4*p**3) < 5e-14 and abs(dephased-2*p**3) < 5e-14,
         'literal downstream native interference with and without reading')
    print('native source sha256:', digest)
    print('all-input NC1 plus physical record: 2 births, 9 CX, 2 G, 4 SourceI')
    print('all 16 input columns and both retained branches verified')
    print('full clock dimension:', D, 'two-grade modes:', 425*D)
    print('complete feedback J:', format(J, '.15g'))
    print('complete heat Z_H (floating point):', format(zh, '.15g'))
    print('master log(Z_H)/beta + J (floating point):', format(master, '.15g'))
    print('baseline NC1-only clock dimension, Z_H, J, master:',
          len(baseline), format(base_zh, '.15g'), format(base_j, '.15g'), format(base_master, '.15g'))
    print('downstream counterexample P(1), coherent vs recorded:', coherent, dephased)
    print('isolated gadget only; full factory/seed clock and Book Cost-Info remain open')


if __name__ == '__main__':
    main()
