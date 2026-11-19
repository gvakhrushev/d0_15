"""Independent return-instrument, stopped-word and price checks for A80."""
from fractions import Fraction
from math import log, sqrt

import numpy as np


PHI = (1 + sqrt(5)) / 2


def entropy(probabilities):
    return -sum(x * log(x, PHI) for x in probabilities if x > 0)


def return_tree(u, cap):
    probabilities = [u]
    lengths = [2]
    visits = np.array([u, 1 - u, 0., 0.])
    remaining = 1 - u
    for k in range(1, cap + 1):
        success = remaining * (1 - u)
        remaining *= u
        visits[2:] += [success, remaining]
        probabilities.append(success)
        lengths.append(k + 2)
    return probabilities + [remaining], lengths + [cap + 1], visits


def close(actual, expected, tol=2e-12):
    np.testing.assert_allclose(actual, expected, atol=tol, rtol=tol)


def test_stopping(u, cap):
    distribution, lengths, visits = return_tree(u, cap)
    lengths = np.array(lengths)
    kraft = PHI ** (-lengths)
    close(sum(distribution), 1)
    close(sum(kraft), 1)
    n = 2 - u ** cap
    h = entropy([u, 1-u])
    close(visits, [u, 1-u, (1-u)*(n-1), u*(n-1)])
    close(sum(visits), n)
    close(entropy(distribution), n*h)
    length = np.dot(distribution, lengths)
    close(length, 3 - (2-u)*u**cap)
    divergence = sum(x * log(x/y, PHI) for x, y in zip(distribution, kraft))
    close(length - entropy(distribution), divergence)
    slope = u**cap - n*log((1-u)/u, PHI)
    if cap:
        slope -= cap * u**(cap-1) * (2-u-h)
    assert slope < 0

    def ledger(t):
        ds, lens, _ = return_tree(t, cap)
        return np.dot(ds, lens) - entropy(ds)

    step = 1e-6
    close((ledger(u+step)-ledger(u-step))/(2*step), slope, 2e-8)
    if cap >= 3:
        close(distribution[3]/distribution[2], u)
        close((kraft[3]/distribution[3])/(kraft[2]/distribution[2]), (1/PHI)/u)
        assert abs(u*u - 1/PHI) > .5


def basis(rng, size):
    matrix = rng.normal(size=(size, size)) + 1j*rng.normal(size=(size, size))
    return np.linalg.qr(matrix)[0]


def test_actual_instrument(q, rng):
    # Deliberately rotate the ready and event bases independently on the full space.
    dim = 3
    left, right = basis(rng, 2*dim), basis(rng, 2*dim)
    eye = np.eye(dim)
    zero = np.zeros_like(eye)
    rotation = np.block([[sqrt(1-q)*eye, -sqrt(q)*eye],
                         [sqrt(q)*eye, sqrt(1-q)*eye]])
    V = right @ rotation @ left.conj().T
    i, hit = left[:, :dim], right[:, dim:]
    P, event = i @ i.conj().T, hit @ hit.conj().T
    R = V.conj().T @ (np.eye(2*dim)-2*event) @ V
    c, s = 1-2*q, sqrt(1-(1-2*q)**2)
    B = (R@i-c*i)/s
    close(i.conj().T @ R @ i, c*eye)
    close(i.conj().T @ B, zero)
    close(B.conj().T @ B, eye)
    close(R@B, s*i-c*B)
    # A full-Schmidt-rank complex protected input, vectorized with its external reference.
    psi = basis(rng, dim) @ np.diag(np.sqrt([.19, .27, .54])) @ basis(rng, dim)
    old = i@psi
    unnormalized = old
    for k in range(11):
        after = R@unnormalized
        restored, unnormalized = P@after, (np.eye(2*dim)-P)@after
        amplitude = c if k == 0 else s*s*(-c)**(k-1)
        close(restored, amplitude*old)
        close(V@restored, amplitude*V@old)
        close(unnormalized, s*(-c)**k*B@psi)
        close(np.linalg.norm(unnormalized)**2, (1-c*c)*(c*c)**k)


def main():
    rng = np.random.default_rng(80)
    for q in [float(Fraction(k, 1000)) for k in range(230, 381, 5)]:
        for cap in [0, 1, 2, 3, 8, 16, 32]:
            test_stopping((1-2*q)**2, cap)
        test_actual_instrument(q, rng)
    assert .3**16 < 4.31e-9
    assert log(7/3, PHI) > 1 and log(2, PHI) < 1.45
    print("PASS 31 field settings, 217 capped trees, full quantum instrument with reference")
    print("PASS exact-return amplitudes, entropy, occupation, Kraft ledger and field derivative")


if __name__ == "__main__":
    main()
