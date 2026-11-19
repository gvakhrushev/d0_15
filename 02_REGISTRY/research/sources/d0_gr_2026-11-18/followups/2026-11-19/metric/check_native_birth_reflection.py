"""Reflection of canonical fresh births using an actual heralded known one.

The full-letter logical oracle is checked on each basis word and, separately,
against the dense n-qubit reflection. Marked Toffoli factory outcomes and the
full raw-source birth history are conditional, not simulated or erased.
"""
import json
import math
import numpy as np
from mpmath import iv


def phase_oracle(n, word, control):
    bits = [(word >> i) & 1 for i in range(n)]
    before = bits[:]
    scratch = [0] * (n - 1)
    assert control == 1
    bits = [b ^ control for b in bits]
    scratch[0] ^= bits[0] & bits[1]
    for i in range(2, n):
        scratch[i - 1] ^= scratch[i - 2] & bits[i]
    phase = -1 if scratch[-1] else 1
    for i in range(n - 1, 1, -1):
        scratch[i - 1] ^= scratch[i - 2] & bits[i]
    scratch[0] ^= bits[0] & bits[1]
    bits = [b ^ control for b in bits]
    assert bits == before and not any(scratch)
    return phase


def kronpower(a, n):
    out = np.array([[1.]])
    for _ in range(n):
        out = np.kron(out, a)
    return out


def main():
    p = (math.sqrt(5.) - 1.) / 2.
    v = np.array([math.sqrt(p), p])
    g = np.array([[v[0], -p], [p, v[0]]])
    x = np.array([[0., 1.], [1., 0.]])
    assert np.max(abs(x @ g @ x - g.T)) < 1e-14
    errors = {}
    cases = 0
    for n in range(2, 7):
        signs = [phase_oracle(n, k, 1) for k in range(1 << n)]
        assert signs == [-1] + [1] * ((1 << n) - 1)
        G = kronpower(g, n)
        W = kronpower(v.reshape(2, 1), n).reshape(-1)
        target = np.eye(1 << n) - 2 * np.outer(W, W)
        actual = np.einsum('ik,k,jk->ij', G, np.array(signs), G,
                           optimize=False)
        err = np.linalg.norm(actual - target, ord=2)
        assert err < 2e-14
        errors[str(n)] = round(float(err), 15)
        cases += 1 << n
    iv.dps = 60
    p_iv = (iv.sqrt(5) - 1) / 2
    b2 = 1 - p_iv ** 384
    b3 = 1 - (1 - 16 * p_iv ** 9) ** 64
    beta = b2 ** 6 * b3
    examples = []
    for n in (19, 22):
        # Qubit count excludes raw-source flags and ancillas. One can reuse
        # h=1 and these scratch zeros after success, never assume failure reset.
        scratch = n - 1
        tof = 2 * scratch
        logical_cx = 4 * n + 6  # n XGX inverses, 2n X flips, routed Z
        logical_g = 2 * n
        source_i = 2
        prep_cx, prep_g = 2 * scratch, scratch
        success = (1 - p_iv ** 40) * beta ** tof
        examples.append(dict(n=n, extra_zero_wires=scratch,
                             marked_toffoli=tof, G=logical_g, CX=logical_cx,
                             SourceI=source_i, scratch_preparation_G=prep_g,
                             scratch_preparation_CX=prep_cx,
                             conditional_success=str(success)))
    print(json.dumps(dict(status='PASS', basis_words=cases,
        max_dense_error_by_n=errors,
        operation='I - 2 |v>^n <v|^n on the fresh n-wire carrier',
        oldRIGHT_and_descriptor='identity factor; control h=1 independently heralded',
        zero_reflection_requires_clean_scratch=True,
        logical_counts_include_shared_known_one_precondition=True,
        full_raw_source_flags_and_physical_birth_schedule_compiled=False,
        success_and_failure_histories_physically_priced=False,
        total_Book03_and_GR_closed=False, examples=examples),
        indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
