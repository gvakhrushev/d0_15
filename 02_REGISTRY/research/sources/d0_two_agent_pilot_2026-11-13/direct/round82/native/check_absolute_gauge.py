"""Four fully addressed native programs on the growing clock, with different stage motion."""
from collections import Counter
from importlib import util
from pathlib import Path
import sys
from fractions import Fraction
from itertools import combinations

from mpmath import iv
import numpy as np

source = (Path(__file__).resolve().parents[7] / "02_REGISTRY/research/sources"
          / "d0_native_execution_domain_2026-10-24/native_execution.py")
spec = util.spec_from_file_location("a82_native_execution", source)
nt = util.module_from_spec(spec)
sys.modules[spec.name] = nt
sys.dont_write_bytecode = True
spec.loader.exec_module(nt)

iv.dps = 70
p = (iv.sqrt(5) - 1) / 2
a = iv.sqrt(p)
t = 2 * a * p
birth = np.array([[float(a.mid)], [float(p.mid)]])
identity = np.eye(16, dtype=int)
gates = {name: nt.Gate("CX", bits) for name, bits in
         (("U", (0, 1)), ("V", (1, 0)), ("X", (0, 2)), ("Y", (2, 3)))}
execution = nt.Execution(4, tuple(range(4)), (), tuple(gates.values()))
operators = {name: np.asarray(nt.gate_matrix(execution, g), dtype=int)
             for name, g in gates.items()}


def motion(q):
    return iv.sqrt(1 - (1 - (1 - t) * q)**2)


def extra(q):
    return 2 * (motion(p**2 + p**3 * q) - motion(p**2))


def between(x, lo, hi):
    assert x.a > iv.mpf(lo) and x.b < iv.mpf(hi), (x, lo, hi)


def mm(left, right):
    return np.einsum("ij,jk->ik", left, right, optimize=False)


def native_clock(word):
    """G1, G3, G5, including every birth complement and the final real gate."""
    births = [np.kron(np.eye(2**j), birth) for j in range(4)]
    ops = births + [operators[k] for k in word]
    dims = [op.shape[1] for op in ops]
    offsets = np.cumsum([0] + dims).tolist()
    stages = [slice(x, y) for x, y in zip(offsets, offsets[1:])]
    passive = births + [identity] * (len(word) - 1)
    back = np.eye(16)
    close = np.zeros((offsets[-1], 16))
    for j in reversed(range(len(stages))):
        if j == 0:
            close[stages[j]] = back.T
        elif j <= 4:
            detail = np.eye(dims[j]) - mm(passive[j - 1], passive[j - 1].T)
            close[stages[j]] = mm(detail, back.T)
        if j:
            back = mm(back, passive[j - 1])
    matrix = np.zeros((offsets[-1], offsets[-1]))
    for j, op in enumerate(ops[:-1]):
        matrix[stages[j + 1], stages[j]] = op
    matrix[:, stages[-1]] += mm(close, ops[-1])
    np.testing.assert_allclose(mm(matrix.T, matrix), np.eye(offsets[-1]), atol=1e-13)
    # Permutation of each fixed-size stage from cumulative actual gates; the
    # first 4 blocks precede the four genuine births. Last gate common.
    changes = [np.arange(d) for d in dims[:4]]
    partial = identity
    for op in [operators[k] for k in word]:
        changes.append(np.argmax(partial, axis=0))
        partial = mm(op, partial)
    assert np.array_equal(partial, identity)
    permutation = np.concatenate([base + c for base, c in zip(offsets, changes)])
    return matrix[np.ix_(permutation, permutation)]


def event_sources(delta):
    # The protected classical flag is read before the suffix. Test actual
    # positive CX on both sharp sectors with an unrelated fourth old wire.
    sharp = []
    for flag in (0, 1):
        head = np.eye(2)[flag]
        state = np.kron(np.kron(head, head), np.kron(birth.ravel(), birth.ravel()))
        totals = []
        for word in ("XXYY", "XYYX"):
            y = state.copy()
            costs = []
            for gate in word:
                z = np.einsum("ij,j->i", operators[gate], y)
                overlap = np.dot(y, z) / (np.linalg.norm(y) * np.linalg.norm(z))
                # On an unchanged column the exact distance is zero.
                costs.append(0. if np.array_equal(y, z) else np.sqrt(1-overlap**2))
                y = z
            assert np.array_equal(y, state)
            totals.append(sum(costs))
        sharp.append(totals[1] - totals[0])
    between(extra(1), "0.07909932276708", "0.07909932276710")
    np.testing.assert_allclose(sharp, [0., float(extra(1).mid)], atol=2e-14, rtol=0.)
    # Rational witness tests cancellation of all prefix probabilities on the
    # simplex, all observed events including the empty event and total variation.
    base = [Fraction(i, 15) for i in (1, 2, 3, 4, 5)]
    score = [Fraction(i, 31) for i in (-7, 2, 0, -1, 6)]
    assert sum(base) == 1 and sum(score) == 0
    max_derivative = 0
    for size in range(len(base) + 1):
        for event in combinations(range(len(base)), size):
            signed = sum((d for i, d in enumerate(score) if i in event), Fraction(0))
            eps = Fraction(1, 100)
            costs = []
            for direction in (-1, 1):
                masses = [b + direction*eps*d for b,d in zip(base,score)]
                assert min(masses) > 0
                costs.append(sum((iv.mpf(c.numerator)/c.denominator) *
                                 extra((p**2, 2*p**3)[i in event])
                                 for i,c in enumerate(masses)))
            derivative = (costs[1] - costs[0]) * eps.denominator / (2*eps.numerator)
            rem = derivative - delta * signed.numerator / signed.denominator
            assert iv.mpf(0) in rem and rem.delta.b < iv.mpf("1e-62")
            max_derivative = max(max_derivative,abs(signed))
    assert 2*max_derivative == sum(map(abs, score))


def main():
    baseline = None
    actual = {}
    start = birth.ravel()
    for _ in range(3):
        start = np.kron(start, birth.ravel())
    for b, bank in enumerate(("UV", "VU")):
        for label, block in (("S", "XXYY"), ("L", "XYYX")):
            main_word = bank + block + bank[::-1]
            assert Counter(main_word) == dict.fromkeys("UVXY", 2)
            mapped = identity
            state = start.copy()
            distances = []
            for name in main_word:
                matrix = operators[name]
                mapped = mm(matrix, mapped)
                previous = state
                state = np.einsum("ij,j->i", matrix, previous)
                distances.append(np.sqrt(max(0., 1. - np.dot(previous, state)**2)))
            assert np.array_equal(mapped, identity)
            np.testing.assert_allclose(state, start, atol=0.)
            actual[b, label] = sum(distances)
            clock = native_clock(main_word + "UU")
            if baseline is None:
                baseline = clock
            else:
                np.testing.assert_allclose(clock, baseline, atol=1e-13)
        expected = extra((p**2, 2*p**3)[b])
        np.testing.assert_allclose(actual[b, "L"] - actual[b, "S"],
                                   float(expected.mid), atol=5e-14, rtol=0.)
    delta = extra(2*p**3) - extra(p**2)
    between(delta, "0.0072093956270", "0.0072093956273")
    event_sources(delta)
    x = p**2 + p**5
    slope = 4*a*p*p**3*(1-t)*(1-(1-t)*x)/motion(x)
    between(slope, "0.0785776560225", "0.0785776560228")
    theta = iv.atan2(p, a)
    # Select a true positive power with a small signed residual mod 2*pi.
    k = 93997
    nearest = round(float((k*theta/(2*iv.pi)).mid))
    eps = k*theta - nearest*2*iv.pi
    between(abs(eps), "0.0000206", "0.0000208")
    secant = (extra(iv.sin(theta + eps)**2) - extra(iv.sin(theta - eps)**2))/(2*eps)
    between(secant, "0.07857765", "0.07857767")
    print("all columns and addressed calls checked; dimension", len(baseline),
          "full scene modes", 425*len(baseline))
    print("crossed physical distances", float(delta.mid), "limiting slope", float(slope.mid),
          "native k", k, "secant", float(secant.mid))


if __name__ == "__main__":
    main()
