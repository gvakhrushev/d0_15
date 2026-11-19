"""Check the repeated native two-tick return on its full, unprojected 8D unitary."""
import mpmath as mp

mp.mp.dps = 70
p = (mp.sqrt(5) - 1) / 2
theta = mp.asin(p)
zeta = mp.mpf(2) ** -20
eye = mp.eye(2)
cx = mp.matrix([[1, 0, 0, 0], [0, 1, 0, 0],
                [0, 0, 0, 1], [0, 0, 1, 0]])
cut = mp.matrix(8, 2)
cut[0, 0] = cut[2, 1] = 1


def tensor(a, b):
    return mp.matrix([[a[i // b.rows, j // b.cols] * b[i % b.rows, j % b.cols]
                       for j in range(a.cols * b.cols)] for i in range(a.rows * b.rows)])


def rotate(angle):
    return mp.matrix([[mp.cos(angle), -mp.sin(angle)], [mp.sin(angle), mp.cos(angle)]])


def eigenvalues(m, geometric_angle, matter_angle):
    tick = tensor(cx * tensor(rotate(geometric_angle), eye), rotate(matter_angle))
    out = (tick ** (2*m)) * cut
    feedback = out.T * (mp.eye(8) - cut * cut.T) * out
    return list(mp.eigsy(feedback, eigvals_only=True))


def ratio(m, deriv):
    u = mp.sin(2*m*theta)**2
    v = 1-(1-u)**2
    return 2*p*(1 + deriv(u) / ((1-u)*deriv(v)))


for m in [1, 3, 33, 903, 55979]:
    for e, b in [(theta, theta), (theta + mp.mpf('0.013'), theta - mp.mpf('0.007'))]:
        u = mp.sin(2*m*b)**2
        lam = mp.sin(2*m*e)**2
        predicted = [u, u+(1-u)*lam]
        computed = eigenvalues(m, e, b)
        assert max(abs(i-j) for i, j in zip(computed, predicted)) < mp.mpf('1e-60')
    print(m, *[mp.nstr(ratio(m, d), 13) for d in
               [lambda s: 1, lambda s: zeta/(1-zeta*s), lambda s: 1+2*s]])
print("universal nondegenerate-slope limit:", mp.nstr(4*p, 16))

for denominator in (33, 903, 55979, 691805):
    center = 2 * denominator * theta
    initial_residue = abs(center - mp.pi * mp.nint(center / mp.pi))
    assert 0 < denominator * initial_residue < mp.pi
    multiple = int(mp.ceil(mp.sqrt(mp.pi / (denominator * initial_residue))))
    ticks = 2 * multiple * denominator
    residue = abs(ticks * theta - mp.pi * mp.nint(ticks * theta / mp.pi))
    assert abs(residue - multiple * initial_residue) < mp.mpf('1e-60')
    assert 2*mp.pi <= ticks*residue <= 8*mp.pi
    print("balanced duration and k*abs(delta):", ticks, mp.nstr(ticks*residue, 12))
