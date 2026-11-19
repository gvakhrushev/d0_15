"""Full original live output, a separately regenerated RAW word and its cold jet."""

from math import comb, sqrt
from pathlib import Path
import sys

import numpy as np

SOURCE = Path(__file__).resolve().parents[4] / "d0_native_execution_domain_2026-10-24"
sys.path.insert(0, str(SOURCE))
import native_execution as native

P = (sqrt(5) - 1) / 2
A = sqrt(P)
V = np.array([A, P])
TOL = 3e-12


def product(left, right):
    rules = {(1, 1): "i,i->", (1, 2): "i,ij->j", (2, 1): "ij,j->i", (2, 2): "ik,kj->ij"}
    return np.einsum(rules[left.ndim, right.ndim], left, right, optimize=False)


def close(actual, expected):
    np.testing.assert_allclose(actual, expected, rtol=1e-11, atol=TOL, equal_nan=False)


def raw_bank(order):
    gate = native.Gate
    bank = gate("CX", order)
    sign = gate("SourceI", (2, 0, 1))
    enc = gate("CX", (4, 5))
    gates = (bank, gate("CX", (2, 4)), sign, sign, bank, enc, gate("G", (5,)), enc)
    execution = native.Execution(6, (), (), gates, profile=native.G_CX_SOURCE_I,
                                 source_port=2, source_spin=(0, 1), report_bits=(4, 5))
    word = np.eye(64)
    for g in gates:
        op = native.gate_matrix(execution, g, max_qubits=6, max_expanded_stages=8)
        word = product(np.array(op, dtype=float), word)
    born = np.eye(4)
    for _ in range(4):
        born = np.kron(born, V[:, None])
    return word, born


def check_bell(image, test):
    m, r = image.shape
    # Pair the original output index with the conjugate regenerated isometry.
    shadow = image.conj() / sqrt(r)
    actual = np.einsum("aj,ai->ji", shadow, product(test, image)) / sqrt(m)
    close(actual, product(product(image.conj().T, test), image) / sqrt(m * r))


def compensated_output(word, born, q):
    close(word, np.kron(np.eye(4), word[:16, :16]))
    image = product(word, born)
    cold = product(born.T, image)
    c = A * (1 - (1 + 2 * A * P) * q)
    x = c * c
    close(cold, c * np.eye(4))
    all_born = product(born, born.T)
    close(product(product(image.T, all_born), image), x * np.eye(4))
    report = np.diag([float(i % 4 == 2) for i in range(64)])
    close(product(product(image.T, report), image), (P**2 + P**3 * q) * np.eye(4))
    check_bell(image, np.eye(64))
    check_bell(image, report)

    # The replica has a known, fixed input; the original unknown Spin is untouched.
    # The probe is a real all-column rotation on its new bit around the birth basis.
    replica = born[:, 0]
    f = product(word, replica)
    alpha0 = 3 * x / 4
    alpha1 = (3 * x - 1) / 4
    first = product(np.eye(64) - all_born, f)
    returned = product(all_born, f)
    chi0 = product(word.T, alpha0 * first + alpha1 * returned)
    chi1 = product(word.T, sqrt(1 - alpha0 ** 2) * first + sqrt(1 - alpha1 ** 2) * returned)
    chi = np.concatenate((chi0, chi1))
    close(product(chi, chi), 1)
    h = product(replica, chi0)
    close(h, x / 2)
    close(product((h * cold).T, h * cold), (x**3 / 4) * np.eye(4))

    old_with_right = (image / 2).reshape(-1)
    full = np.outer(old_with_right, chi)
    close(product(full, full.T), np.outer(old_with_right, old_with_right))
    for kept in (report, np.eye(64)-report):
        branch = ((product(kept, image)) / 2).reshape(-1)
        whole = np.outer(branch, chi)
        close(product(whole, whole.T), np.outer(branch, branch))

    # Derivative evaluated algebraically, including the mismatch of controls.
    hprime = alpha1 - alpha0
    close(h*h + 2*x*h*hprime, 0)
    for original, regenerated in ((1, 0), (0, 1), (1, 1)):
        close(h*h*original + 2*x*h*hprime*regenerated, h*h*(original-regenerated))
    assert x > 0
    return x, x**3 / 4


def bounded_coeff(t, delta):
    if t < delta:
        return 0.75 - t / (4 * delta)
    return 0.5 * sqrt(delta / t)


def bernstein(n, x, coefficients):
    return sum(comb(n, j)*x**j*(1-x)**(n-j)*v for j, v in enumerate(coefficients))


def collar_test():
    delta = 1 / 4
    n = 128
    coeff = [bounded_coeff(j/n, delta) for j in range(n+1)]
    assert 0 < min(coeff) <= max(coeff) <= 0.75
    for x in (0.25, 0.375, 0.6, 0.825, 1.0):
        h = bernstein(n, x, coeff)
        dh = n * bernstein(n-1, x, np.diff(coeff))
        close_bound = 1 / (8 * delta * sqrt(n))
        assert abs(h - bounded_coeff(x, delta)) <= close_bound
        bound = 3 / (8 * delta**2) * (1 / (2 * sqrt(n)) + 1/n)
        assert abs(dh + sqrt(delta)/(4*x**1.5)) <= bound
        assert abs(x*h*h - delta/4) < 0.009
        assert abs(h*h+2*x*h*dh) < 0.03


if __name__ == "__main__":
    for order, q in (((2, 3), P**2), ((3, 2), 2*P**3)):
        x, gain = compensated_output(*raw_bank(order), q)
        print("bank", order, "return probability %.12g; compensated Gram %.12g" % (x, gain))
    collar_test()
    print("original output, each retained sector and external RIGHT preserved; matched derivative zero")
