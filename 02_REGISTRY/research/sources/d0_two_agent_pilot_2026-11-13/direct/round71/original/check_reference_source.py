"""Independent finite checks for the reference-return source on a protected cut."""
import numpy as np

P = (np.sqrt(5.0) - 1.0) / 2.0
A = np.sqrt(P)
ZETA = 2.0 ** -20
K = ZETA * A * P ** 3
I = np.eye(3)
SECT = np.diagflat([0.0] * 3 + [1.0] * 3)
BASIS = np.array([[1, 1, 1], [1, 0, -1], [-1, 2, -1]], float)
BASIS /= np.linalg.norm(BASIS, axis=1)[:, None]
B0 = np.array([[0.71, 0.08j, 0.01], [0.12, 0.54, -0.07], [0.02j, 0.03, 0.39]])
DIRECTION = np.array([[0, 0.03, 0], [-0.03, 0, -0.01], [0, 0.01, 0]])
QS = np.array([0.1, 0.16, 0.19])


def need(flag, message):
    if not flag:
        raise ValueError(message)


def same(left, right, message, atol=1e-12):
    need(np.allclose(left, right, rtol=0, atol=atol), message)


def sample(q, basis, old, phase):
    v = np.vstack([np.diag(np.sqrt(1-q)), np.diag(np.sqrt(q))]) @ basis
    qmat = v.conj().T @ SECT @ v
    u = np.exp(1j*phase)
    test = v.conj().T @ (np.eye(6) + (u-1)*SECT) @ v
    c0 = P * (A*(I-qmat) - P*qmat)
    cu = P * (A*(I-qmat) - P*u*qmat)
    z = (1-u) * (np.eye(6)-v@v.conj().T) @ SECT @ v @ old
    d = z.conj().T @ z
    same(d, old.conj().T @ (I-test.conj().T@test) @ old, 'effect from the actual embedding')
    w0 = (c0@old).conj().T @ (c0@old)
    wu = (cu@old).conj().T @ (cu@old)
    same(wu-w0, A * P**3 * d, 'ordered Gram identity')
    need(np.linalg.eigvalsh(w0).min() > -1e-13 and np.linalg.eigvalsh(wu).max() < 1, 'cold contractions')
    g = (1-ZETA)*I + ZETA*w0
    vals, vecs = np.linalg.eigh(g)
    ig = (vecs / np.sqrt(vals)) @ vecs.conj().T
    shift = np.linalg.eigvalsh(ig @ (K*d) @ ig)
    gap = np.log1p(shift).sum()
    tr = d.trace().real
    need(K*tr - 1e-20 <= gap <= K*tr/(1-ZETA) + 1e-20, 'absolute paid bounds')
    return gap, z, g, tr


def run():
    base = sample(QS, BASIS, B0, 1.3)
    effect = BASIS.T @ np.diag(QS) @ BASIS
    need(np.linalg.norm(effect @ B0 @ B0.conj().T - B0 @ B0.conj().T @ effect) > 0.01,
         'noncommuting old and new operators')
    need(base[0] > 0, 'strict cost ordering')
    singular = np.diag([0.5, 0.4, 0.0])
    gap, _, _, _ = sample(np.array([0., 1., 0.4]), I, singular, np.pi)
    same(gap, 0, 'nonzero phase on unreachable mixed sector')
    need(sample(QS, I, singular, np.pi)[0] > 0, 'nontrivial surviving columns')

    def path(t, offset):
        return sample(QS + t*np.array([0.013, -0.021, 0.011]), BASIS,
                      B0 + t*DIRECTION, offset + 0.8*t)

    eps = 1e-5
    zero = path(0., 0.)
    same(zero[0], 0, 'exact reference at one field')
    dgap = (path(eps, 0.)[0] - path(-eps, 0.)[0])/(2*eps)
    same(dgap, 0, 'phase source at an exactly calibrated field', atol=1e-16)
    for offset in [0.001, 0.5, 1.7]:
        dp = path(eps, offset)
        dm = path(-eps, offset)
        _, _, _, tr = path(0., offset)
        ds, dz, dg = [(dp[i]-dm[i])/(2*eps) for i in range(3)]
        bound = (2*K*np.sqrt(tr)*np.linalg.norm(dz)/(1-ZETA) +
                 K*tr*np.linalg.norm(dg, ord=2)/(1-ZETA)**2)
        need(abs(ds) <= bound + 1e-16, 'first-derivative-only error bound')

    scalar = 0.14
    h = A - (A+P)*scalar
    s = B0.conj().T @ B0
    m = (1-ZETA)*I + ZETA*P**2*h*h*s
    gain = 2*ZETA*P**2*(A+P)*h*np.trace(np.linalg.solve(m,s)).real
    need(gain > 0, 'absolute field gain on past')
    isospectral = DIRECTION @ s - s @ DIRECTION
    same(np.trace(np.linalg.solve(m, isospectral)), 0, 'isospectral old variation')
    need(np.trace(np.linalg.solve(m, 2*s)).real > 0, 'surviving change of old singular values')
    def scalar_price(q):
        old_values = np.linalg.eigvalsh(s)
        return -np.log1p(ZETA*(P**2*(A-(A+P)*q)**2*old_values-1)).sum()
    numeric = (scalar_price(scalar+eps)-scalar_price(scalar-eps))/(2*eps)
    same(numeric, gain, 'field derivative of the absolute price', atol=1e-15)

    embed = np.array([[1.], [0.]])
    history = np.array([[0.5], [np.sqrt(0.75)]])
    swap = np.array([[0., 1.], [1., 0.]])
    remainder = embed.T @ swap @ (np.eye(2)-embed@embed.T) @ history
    same(embed.T@swap@history - (embed.T@swap@embed)@(embed.T@history),
         remainder, 'exact obstruction to composing cold corners')
    need(float(remainder[0,0]) > 0.8, 'genuine prior leakage')
    print('PASS reference source: Gram order, exact and approximate field response, old spectrum and live cut')


if __name__ == '__main__':
    run()
