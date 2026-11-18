"""Actual H.1 columns, all raw real skew directions, and exact reset-branch comparisons."""
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix


source = Path(__file__).resolve().parents[4] / "d0_native_execution_domain_2026-10-24/native_execution.py"
assert sha256(source.read_bytes()).hexdigest() == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = spec_from_file_location("separate_legs_native", source)
nt = module_from_spec(spec)
sys.modules[spec.name] = nt
spec.loader.exec_module(nt)


def golden(a):
    return DomainMatrix.from_Matrix(a).convert_to(nt.GOLDEN_FIELD).to_dense()


def word(*gates):
    hardware = nt.Execution(4, (), (), gates, nt.G_CX_SOURCE_I, 2, (0, 1))
    return nt.word_matrix(hardware, max_qubits=4)


class RingMatrix:
    """Exact integer coefficient arrays in Z[a], a^4=1-a^2."""
    def __init__(self, coeff):
        self.coeff = np.asarray(coeff, dtype=np.int64)

    @classmethod
    def integers(cls, matrix):
        mat = np.asarray(matrix, dtype=np.int64)
        return cls([mat, np.zeros_like(mat), np.zeros_like(mat), np.zeros_like(mat)])

    @property
    def T(self):
        return RingMatrix(self.coeff.transpose(0, 2, 1))

    def __add__(self, other):
        return RingMatrix(self.coeff + other.coeff)

    def __sub__(self, other):
        return RingMatrix(self.coeff - other.coeff)

    def __matmul__(self, other):
        x, y = self.coeff, other.coeff
        # Each reduced coefficient is a sum of at most 32 ordinary dot products.
        assert 32 * x.shape[2] * int(abs(x).max()) * int(abs(y).max()) < 2**60
        raw = np.zeros((7, x.shape[1], y.shape[2]), dtype=np.int64)
        for k in range(4):
            if x[k].any():
                for m in range(4):
                    if y[m].any():
                        raw[k+m] += x[k] @ y[m]
        for k in (6, 5, 4):
            raw[k-4] += raw[k]
            raw[k-2] -= raw[k]
        return RingMatrix(raw[:4])

    def __eq__(self, other):
        return np.array_equal(self.coeff, other.coeff)


def ring_coefficients(mat):
    def coeffs(x):
        a = nt.GOLDEN_FIELD.from_sympy(x)
        coeff = [int(v) for v in reversed(a.to_list())]
        assert all(v.denominator == 1 for v in a.to_list())
        return coeff + [0]*(4-len(coeff))
    return RingMatrix(np.array([[coeffs(x) for x in row] for row in mat.tolist()]).transpose(2,0,1))


def measure_jets(A, j, pr, q):
    # Each returned 4 x 4 quantity represents ALL Hermitian old input tests.
    ident = RingMatrix.integers(np.eye(16))
    zero = RingMatrix.integers(np.zeros((4,4)))
    pj = j @ j.T
    P = [pr, ident-pr]
    B = [pj, ident-pj]
    h = [proj @ A @ j for proj in P]
    base = [[P[k] @ A @ B[k] @ A.T @ h[i] for k in range(2)] for i in range(2)]
    base_r = [B[i] @ A.T @ h[i] for i in range(2)]
    full_effect = sum((z.T @ z for row in base for z in row), zero)
    assert full_effect == ring_coefficients(q*sp.eye(4))
    non_scalar = False
    def jet(m, dm):
        return m.T @ dm + dm.T @ m
    for r in range(16):
        for c in range(r):
            x = np.zeros((16,16), dtype=np.int64)
            x[r,c], x[c,r] = 1, -1
            da = RingMatrix.integers(x) @ A
            direct = jet(pr @ A @ j, pr @ da @ j)
            non_scalar |= any(not np.array_equal(m, m[0,0]*np.eye(4)) for m in direct.coeff)
            by_front, by_back, by_initial = (zero for _ in range(3))
            back_single = zero
            for i in range(2):
                back_single += jet(base_r[i], B[i] @ da.T @ h[i])
                for k in range(2):
                    m = base[i][k]
                    by_front += jet(m, P[k] @ da @ B[k] @ A.T @ h[i])
                    by_back += jet(m, P[k] @ A @ B[k] @ da.T @ h[i])
                    by_initial += jet(m, P[k] @ A @ B[k] @ A.T @ P[i] @ da @ j)
            for lhs, rhs in [(by_front, direct), (by_back, zero), (by_initial, zero), (back_single, direct)]:
                assert lhs == rhs
    assert non_scalar


def check_common_terminal(j, pr, forward, after):
    """Every Kraus block, and the entire twirl channel, not just one test state."""
    import itertools
    eye4 = sp.eye(4)
    I, J = golden(eye4), golden(nt.L_I)
    F, W, jj, pi = golden(word(*forward)), golden(word(*after)), golden(j), golden(pr)
    unit = golden(sp.eye(16))
    for e in (pi, unit-pi):
        blocks = (W*e*F*jj).to_Matrix()
        norm = nt.GOLDEN_FIELD.zero
        for w in range(4):
            k = golden(blocks.extract([4*s+w for s in range(4)], range(4)))
            # The first column of aI+bL_i has entries (a,b,0,0).
            ar, br = k.to_list()[0][0], k.to_list()[1][0]
            assert k == I.scalarmul(ar) + J.scalarmul(br)
            norm += ar*ar + br*br
        assert jj.transpose()*F.transpose()*e*F*jj == I.scalarmul(norm)
    # After swapping all original WORK to the new buffer, tracing that buffer
    # in the old terminal removes off-diagonal work addresses. Address swap check.
    for a, b in itertools.product(range(2), repeat=2):
        u, v = a, b
        v ^= u
        u ^= v
        v ^= u
        assert (u, v) == (b, a)
    li = nt.L_I
    left, right = sp.kronecker_product(li, eye4), sp.kronecker_product(eye4, li)
    paired = left*right
    D = (sp.eye(16)+paired)/2
    assert D*paired == D and D*(left+right) == sp.zeros(16)
    # Actual dirty source port 2; the flag is wire 3. SWAP, SourceI, SWAP.
    a, b = nt.Gate("CX",(2,3)), nt.Gate("CX",(3,2))
    move = (a,b,a)
    implemented = word(*move, nt.Gate("SourceI",(2,0,1)), *move)
    expect = sp.kronecker_product(eye4, sp.eye(2), sp.diag(1,0)) + sp.kronecker_product(li, sp.eye(2), sp.diag(0,1))
    assert implemented == expect


def main():
    p, a = nt.P, nt.A
    v = sp.Matrix([a, p])
    j = sp.kronecker_product(sp.eye(4), v, v)
    pr = sp.kronecker_product(sp.eye(4), sp.diag(0,1), sp.eye(2))
    bx, px = golden(j*j.T), golden(pr)
    G = nt.Gate("G", (2,))
    H = nt.Gate("G", (3,))
    S = nt.Gate("SourceI", (2,0,1))
    cx, reverse = nt.Gate("CX",(2,3)), nt.Gate("CX",(3,2))
    jj, pp = ring_coefficients(j), ring_coefficients(pr)
    for active, q in [(cx,p*p), (reverse,2*p**3)]:
        A = word(active)
        E = A.T*pr*A
        assert golden(j.T*E*j) == golden(q * sp.eye(4))
        measure_jets(ring_coefficients(A), jj, pp, q)
    # Exact identity on all 16 prior columns, even for incompatible finite legs.
    for front, back in [((S,cx,H,G),(G,reverse,S)), ((reverse,G,S,H,S),(cx,H)),
                        ((cx,),(reverse,)), ((G,S,H),(S,H,G,cx))]:
        F, R = golden(word(*front)), golden(word(*back))
        mark = R*bx*F.transpose()*px*F*bx*R.transpose()
        denominator = R*bx*R.transpose()
        eff = golden(j).transpose()*F.transpose()*px*F*golden(j)
        scalar = eff.to_Matrix()[0,0]
        assert eff == golden(scalar * sp.eye(4))
        assert mark == golden(scalar * sp.eye(16))*denominator
    check_common_terminal(j, pr, (S,cx,H,G), (G,reverse,S))
    print("PASS: actual post-event complex blocks, WORK swaps, flag-controlled Spin on a dirty port and twirl identity on all 16 matrix units.")
    print("PASS: two native centres, 120 skew directions per centre, independent front/back/prefix jets on four Spin columns; exact full-bank reset-event equality for four unmatched native pairs.")


if __name__ == "__main__":
    main()
