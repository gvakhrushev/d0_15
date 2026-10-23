"""Independent finite noncommuting control of the age/oldRIGHT source weld.

Uses the parent's rational two-Kraus fixture, not the original full128.
No external physical price is selected: 1+bit is the declared fixture charge.
"""
import itertools
import json
import numpy as np

ell = np.log((1 + np.sqrt(5)) / 2)
I2 = np.eye(2, dtype=complex)
I4 = np.eye(4, dtype=complex)
pauli = [I2, np.array([[0, 1], [1, 0]], complex),
         np.array([[0, -1j], [1j, 0]], complex), np.diag([1, -1]).astype(complex)]
basis = [np.kron(a, b) / 2 for a in pauli for b in pauli]
checks = []


def check(name, ok, value=None):
    checks.append(dict(name=name, passed=bool(ok), value=None if value is None else float(value)))
    assert ok, (name, value)


def inner(a, b):
    return np.trace(a.conj().T @ b).real


def coords(a):
    return np.array([inner(b, a) for b in basis])


def matrix(v):
    return sum((x * b for x, b in zip(v, basis)), np.zeros((4, 4), complex))


def logm(a):
    vals, vec = np.linalg.eigh(a)
    assert vals.min() > 0
    return (vec * np.log(vals)) @ vec.conj().T


def entropy(a):
    return -inner(a, logm(a))


def ptr_d(a):
    return np.einsum('iaib->ab', a.reshape(2, 2, 2, 2))


def setup(a=.6, b=.8):
    k = [np.diag([a, b]).astype(complex),
         np.array([[0, np.sqrt(1 - b*b)], [np.sqrt(1 - a*a), 0]], complex)]
    rho = np.diag([(1-b*b)/(2-a*a-b*b), (1-a*a)/(2-a*a-b*b)]).astype(complex)
    return k, rho


def channel(k, x, adjoint=False):
    if adjoint:
        return sum(np.kron(v.conj().T, I2) @ x @ np.kron(v, I2) for v in k)
    return sum(np.kron(v, I2) @ x @ np.kron(v.conj().T, I2) for v in k)


def iterate(k, x, n, adjoint=False):
    for _ in range(n):
        x = channel(k, x, adjoint)
    return x


def complete_age(k, cap):
    groups = [[] for _ in range(cap + 1)]
    for word in itertools.product((0, 1), repeat=cap):
        l = I2.copy()
        for bit in word:
            l = k[bit] @ l
        age = 0
        for bit in reversed(word):
            if bit:
                break
            age += 1
        groups[age].append((np.kron(l, I2), sum(1 + bit for bit in word)))
    return groups


def score_grad(k, omega, cap, true_gain):
    groups = complete_age(k, cap)
    blocks = [sum(v @ omega @ v.conj().T for v, _ in group) for group in groups]
    output = sum(blocks)
    cost = sum(c * np.trace(v @ omega @ v.conj().T).real for group in groups for v, c in group)
    val = cost - sum(entropy(block) for block in blocks) / ell
    m = np.zeros((4, 4), complex)
    for group, block in zip(groups, blocks):
        for v, c in group:
            m += c * v.conj().T @ v + v.conj().T @ (logm(block) + I4) @ v / ell
    if true_gain:
        val += entropy(omega) / ell
        m -= (logm(omega) + I4) / ell
    else:
        val += entropy(output) / ell
        m -= iterate(k, logm(output) + I4, cap, True) / ell
    return val, m, output, blocks


k, rho = setup()
right = np.array([[.6, .10 + .03j], [.10 - .03j, .4]], complex)
omega = np.kron(rho, right)


def project(m):
    return np.kron(I2, ptr_d(np.kron(rho, I2) @ m))


T = np.column_stack([coords(channel(k, b, True)) for b in basis])
P = np.column_stack([coords(project(b)) for b in basis])
green = np.linalg.inv(np.eye(16) - T + P) @ (np.eye(16) - P)
check('DATA mixing inherited, joint invariant dimension four', np.linalg.matrix_rank(np.eye(16) - T, tol=1e-10) == 12)
check('native-type fixture genuinely noncommuting', np.linalg.norm(k[0] @ k[1] - k[1] @ k[0]) > .01)

for cap in (1, 2, 3, 6):
    conditional, mc, output, blocks = score_grad(k, omega, cap, False)
    gain, mg, _, _ = score_grad(k, omega, cap, True)
    check(f'cap{cap} actual complete grouped output', np.linalg.norm(output - iterate(k, omega, cap)) < 2e-13)
    check(f'cap{cap} stationary values exactly agree numerically', abs(gain - conditional) < 2e-13, abs(gain - conditional))
    expected = (iterate(k, logm(omega), cap, True) - logm(omega)) / ell
    check(f'cap{cap} full ambient score difference', np.linalg.norm(mg - mc - expected) < 2e-12, np.linalg.norm(mg - mc - expected))
    bk = sum((iterate(k, logm(omega), j, True) for j in range(cap)), np.zeros((4, 4), complex)) / ell
    check(f'cap{cap} exact Poisson coboundary', np.linalg.norm(expected + bk - channel(k, bk, True)) < 2e-12)
    yc = matrix(green @ coords(mc))
    yg = matrix(green @ coords(mg))
    check(f'cap{cap} centered joint adjoint shift', np.linalg.norm(yg - yc + bk - project(bk)) < 2e-11, np.linalg.norm(yg - yc + bk - project(bk)))
    for label, score, yy in [('conditional', mc, yc), ('gain', mg, yg)]:
        scalar = inner(omega, score)
        res = score + channel(k, yy, True) - yy - scalar * I4
        check(f'cap{cap} {label} all joint Euler rows', np.linalg.norm(res) < 2e-11, np.linalg.norm(res))
    # This derivative varies the actual Kraus maps, preserving their completeness.
    eps = 1e-5
    kp, rp = setup(.6 + eps)
    km, rm = setup(.6 - eps)
    fixed_c = (score_grad(kp, omega, cap, False)[0] - score_grad(km, omega, cap, False)[0]) / (2*eps)
    fixed_g = (score_grad(kp, omega, cap, True)[0] - score_grad(km, omega, cap, True)[0]) / (2*eps)
    dphi = (channel(kp, omega) - channel(km, omega)) / (2*eps)
    correction = inner(bk, dphi)
    check(f'cap{cap} actual fixed-input residual retained', abs(fixed_g - fixed_c - correction) < 3e-8, abs(fixed_g - fixed_c - correction))
    full_c = fixed_c + inner(yc, dphi)
    full_g = fixed_g + inner(yg, dphi)
    check(f'cap{cap} full native source equality after shift', abs(full_c - full_g) < 3e-8, abs(full_c - full_g))
    total = (score_grad(kp, np.kron(rp, right), cap, True)[0] - score_grad(km, np.kron(rm, right), cap, True)[0]) / (2*eps)
    check(f'cap{cap} independent stationary curve derivative', abs(total - full_g) < 3e-8, abs(total - full_g))
    check(f'cap{cap} unshifted adjoint genuinely fails', abs(correction) > .01, abs(correction))
    # Arbitrary correlated, trace-zero preparation variation is not discarded.
    corr = np.kron(pauli[1], pauli[2]) + .3*np.kron(pauli[3], pauli[1])
    corr += .2*np.kron(pauli[3], I2)  # Gives the boundary correction a nonzero pairing.
    eps_in = 1e-6
    for label, is_gain, score in [('conditional', False, mc), ('gain', True, mg)]:
        fd = (score_grad(k, omega + eps_in*corr, cap, is_gain)[0] - score_grad(k, omega - eps_in*corr, cap, is_gain)[0]) / (2*eps_in)
        check(f'cap{cap} {label} ambient preparation jet', abs(fd - inner(score, corr)) < 2e-7, abs(fd - inner(score, corr)))

print(json.dumps(dict(fixture='parent rational two-Kraus noncommuting example, DATA2 x RIGHT2; not original full128',
                     caps=[1, 2, 3, 6], pass_count=len(checks), checks=checks,
                     scope='floating diagnostics of exact finite algebraic source identities; no physical Book selection'),
                 ensure_ascii=False, indent=2))
