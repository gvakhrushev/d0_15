"""Exact early moments over Z[a], a^4=1-a^2, on the same full native clocks."""
from math import exp, factorial
from fractions import Fraction
import numpy as np
from scipy import sparse as ss
from check_early_heat import a, p, beta, build_clock

unit = np.eye(4, dtype=np.int64)
mul_a = np.array([[0,0,0,1], [1,0,0,0], [0,1,0,-1], [0,0,1,0]], dtype=np.int64)
mul_p = mul_a @ mul_a
assert np.array_equal(mul_p @ mul_p + mul_p, unit)
nodes = [(1., unit), (a,mul_a), (p,mul_p), (a*p,mul_a@mul_p), (p*p,mul_p@mul_p)]
nodes += [(-value,-operator) for value,operator in nodes[:]]


def lift(matrix):
    table = ss.coo_matrix(matrix)
    result = ss.csr_matrix((4*table.shape[0], 4*table.shape[1]), dtype=np.int64)
    counted = np.zeros(table.data.shape, dtype=int)
    for value, operator in nodes:
        use = np.abs(table.data-value)<1e-14
        if np.any(use):
            counted += use
            base = ss.csr_matrix((np.ones(np.count_nonzero(use), dtype=np.int64),
                                  (table.row[use], table.col[use])), shape=table.shape)
            result += ss.kron(base, operator, format="csr")
    assert np.all(counted[table.data != 0] == 1)
    return result


def adjoint(matrix):
    # Transpose physical indices; the four ring coordinates are algebra, not wires.
    coo = matrix.tocoo()
    rows = 4*(coo.col//4) + (coo.row % 4)
    cols = 4*(coo.row//4) + (coo.col % 4)
    return ss.csr_matrix((coo.data, (rows, cols)), shape=(matrix.shape[1],matrix.shape[0]))


def exact_tick(clock):
    def product(left, right):
        # All assembly sums have at most three terms. Reserve ample int64 headroom.
        assert row_bound(left)*row_bound(right) < 2**56
        return left @ right

    offsets = 4*np.cumsum([0]+clock.dims)
    dim = offsets[-1]
    slots = []
    for n, size in enumerate(clock.dims):
        idx = np.arange(4*size)
        slots.append(ss.csr_matrix((np.ones(len(idx), dtype=np.int64), (idx,idx+offsets[n])),
                                   shape=(len(idx),dim)))
    rows = {}
    downhill = {}
    for n in reversed(range(len(slots))):
        if n in clock.last:
            downhill[n] = product(lift(clock.last[n]), slots[n])
        else:
            entries = [(c,lift(j),lift(f)) for c,j,f in clock.children[n]]
            downhill[n] = sum(product(adjoint(j), downhill[c]) for c,j,_ in entries)
            for c,j,f in entries:
                rows[c] = product(f, slots[n]) + downhill[c] - product(j, downhill[n])
    rows[0] = downhill[0]
    t = ss.vstack([rows[i] for i in range(len(rows))], format="csr")
    assert (product(adjoint(t), t) - ss.eye(dim, dtype=np.int64)).count_nonzero() == 0
    return t,slots


def row_bound(matrix):
    return int(np.max(np.asarray(abs(matrix).sum(axis=1))))


def checked_apply(matrix, bound, columns):
    assert int(np.max(np.abs(columns))) * bound < 2**62
    return matrix @ columns


def exact_moments(reverse, guard=6):
    clock, leaf = build_clock(guard, reverse)
    t,slots = exact_tick(clock)
    j = np.kron(np.eye(4),np.kron([a,p],np.kron([1.,0.],[a,p]))[:,None])
    source = slots[leaf].T @ lift(j)
    effect = adjoint(source)
    columns = source[:,::4].toarray()
    move_bound, read_bound = row_bound(t),row_bound(effect)
    result = []
    for i in range(2*guard+21):
        result.append(checked_apply(effect, read_bound, columns).reshape(4,4,4))
        columns = checked_apply(t, move_bound, columns)
    return np.asarray(result)


if __name__ == "__main__":
    diff = exact_moments(False) - exact_moments(True)
    assert not np.any(diff[:32])
    coeff = diff[32, 0, :, 0]
    assert np.array_equal(diff[32], np.einsum("ij,k->ikj", unit, coeff))
    print("32nd scalar difference over the exact [1,a,a²,a³] basis:", coeff.tolist())
    numeric = np.dot(coeff, [1,a,p,a*p])
    x = Fraction(786151377757, 10**12)
    y = x + Fraction(1, 10**12)
    assert x**4+x**2 < 1 < y**4+y**2
    bounds = [sum(int(c)*(x if (c>0)==lower else y)**k for k,c in enumerate(coeff))
              for lower in (True,False)]
    assert Fraction(35,1000) < bounds[0] <= bounds[1] < Fraction(37,1000)
    print("native difference at degree 32:", numeric)
    ratio = beta/(22*33)
    lower = 4*4*33*exp(-beta)*(beta/26)**32/factorial(32)*(.035 - 2*ratio/(1-ratio))
    upper = 4*4*33*exp((beta/22)**2)*(beta/22)**32/factorial(32)*(.037 + 2*ratio/(1-ratio))
    print("positive absolute full thermal contrast between", lower, "and", upper)
    # Outward bounds displayed in the paper are certified in rational arithmetic.
    lo, hi = Fraction(7639,10000), Fraction(764,1000)
    assert lo < 2*x**4 <= 2*y**4 < hi
    assert sum((-hi)**i/factorial(i) for i in range(8)) > Fraction(465,1000)
    assert 1/(1-(hi/22)**2) < Fraction(1002,1000)
    t = hi/(22*33)
    low = 16*33*Fraction(465,1000)*(lo/26)**32/factorial(32)*(Fraction(35,1000)-2*t/(1-t))
    high = 16*33*Fraction(1002,1000)*(hi/22)**32/factorial(32)*(Fraction(37,1000)+2*t/(1-t))
    assert low > Fraction(29,10**85) and high < Fraction(16,10**82)
