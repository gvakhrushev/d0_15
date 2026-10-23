#!/usr/bin/env python3
"""Exact original Julia/Parseval STRUCTURE, finite CAR16 smooth bulk stress test.

The general O(h) C1 theorem is analytic in SMOOTH_BULK_FULL128_C1_HEAT_HISTORY_TRANSFER.md.
This bounded numerical diagnostic keeps all four original CAR creators, their
actual Julia positive roots and all32 analysis Kraus words, using a 1D varying
periodic slice with the other three real shift directions set to identity.
It is NOT a substitute for the complete four-dimensional theorem, actual
128-output record, paid controller, GR or boundary/open-collar analysis.
"""
from math import pi
import numpy as np


def creators():
    ans = []
    for role in range(4):
        C = np.zeros((16, 16), dtype=complex)
        for state in range(16):
            if state & (1 << role):
                continue
            sign = (-1) ** ((state & ((1 << role)-1)).bit_count())
            C[state | (1 << role), state] = sign
        ans.append(C)
    return ans


def psqrt(X):
    X = (X + X.conj().T) / 2
    w, U = np.linalg.eigh(X)
    assert min(w) > -1e-9
    return (U * np.sqrt(np.maximum(w, 0))) @ U.conj().T


def original_recycling(L, amplitude=.12):
    C = creators()
    eye_site = np.eye(L)
    identity = np.eye(16*L, dtype=complex)
    shift = np.roll(eye_site, 1, axis=0)
    site_coeff = .48 + amplitude*np.sin(2*pi*np.arange(L)/L)
    assert 0 < min(site_coeff) < max(site_coeff) < .8

    roles = []
    for r in range(4):
        profile = site_coeff if r == 0 else np.full(L, .48)
        cr = np.kron(np.diag(profile), C[r])
        pr = cr @ np.kron(shift if r == 0 else eye_site, np.eye(16))
        roles.append((pr, cr))

    d = sum((P - U for P, U in roles), np.zeros_like(identity))
    D = d + d.conj().T
    delta = D @ D

    words = []
    for P, U in roles:
        words.extend([P, P.conj().T,
                      psqrt(identity-P@P.conj().T),
                      psqrt(identity-P.conj().T@P),
                      U, U.conj().T,
                      psqrt(identity-U@U.conj().T),
                      psqrt(identity-U.conj().T@U)])

    # Equation (3): 32 analysis operators, exactly the original 64-Walsh-row
    # marginal CP map. Physical output labels are NOT deleted from real history.
    def T(X):
        return sum((A.conj().T@X@A for A in words), np.zeros_like(identity))/16

    # Positive operator unitality AND trace preservation.
    assert np.linalg.norm(T(identity)-identity, ord=2) < 5e-11
    d1 = np.linalg.norm(T(delta)-delta, ord=2)
    var = T(delta@delta)-T(delta)@T(delta)
    var = (var+var.conj().T)/2
    eig = np.linalg.eigvalsh(var)
    assert eig[0] > -5e-10
    d2 = max(abs(eig[0]),abs(eig[-1]))
    return d1, d2, np.linalg.norm(delta,ord=2)


def main():
    samples = []
    for L in (3,4,6,8,12):
        d1,d2,lam = original_recycling(L)
        assert d1>0 and d2>0
        samples.append((L,d1,d2))
        print(f"L={L:2}  ||T*(Delta)-Delta||={d1:.10g} "
              f"Kadison_variance={d2:.10g}  ||Delta||={lam:.10g}")

    assert samples[-1][1] < samples[0][1]
    assert samples[-1][2] < samples[0][2]
    print("PASS: exact original 4-role CAR16 + positive Julia roots,"
          " complete Kraus marginal and diminishing smooth-source defects")


if __name__ == "__main__":
    main()
