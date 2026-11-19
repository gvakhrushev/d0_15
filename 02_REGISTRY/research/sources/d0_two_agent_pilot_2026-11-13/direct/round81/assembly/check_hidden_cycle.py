"""Exact hidden-memory tests for the economy of measured closed paths."""
import sympy as sp


def moments(x, transfer, y, count):
    out = []
    for _ in range(count):
        out.append((x*y)[0])
        y = transfer*y
    return out


def main():
    u, other = sp.Rational(1, 5), sp.Rational(1, 3)
    # The inaccessible mode cannot be inferred from the closed-path weights.
    M = sp.Matrix([[u, 0], [0, other]])
    y, x = sp.Matrix([1-u, 0]), sp.Matrix([[1-u, 0]])
    ts = moments(x, M, y, 8)
    assert all(t == (1-u)**2*u**n for n, t in enumerate(ts))
    a = u
    assert a+(x*(sp.eye(2)-M).inv()*y)[0] == 1
    # Reversible positive example with a genuinely mixed hidden entrance.
    H = sp.Matrix([[u, u/4], [u/4, other]])
    z = sp.Matrix([1, 2])/4
    t0, t1, t2 = moments(z.T, H, z, 3)
    residual = (H-sp.eye(2)*t1/t0)*z
    assert t0*t2-t1**2 == t0*residual.dot(residual) > 0
    # Without reciprocity a mode may be hidden for arbitrarily many finite tests.
    # All transitions are nonnegative; a length-dependent tariff starts after L repeats.
    for delay in [1, 2, 7, 19]:
        D = sp.zeros(delay+1)
        for k in range(delay):
            D[k,k+1] = u
        D[delay,delay] = other
        X = sp.eye(delay+1)[0,:]*(1-u)
        Y = sp.ones(delay+1,1)*(1-u)
        t = moments(X, D, Y, delay+3)
        assert t[:delay+1] == [(1-u)**2*u**n for n in range(delay+1)]
        assert t[delay+1] == other*t[delay] != u*t[delay]
    # A rotation away from a shared eigenline has zero linear response but a quadratic defect.
    h = sp.symbols("h", real=True)
    # Start inside the positive cone (the two eigenvectors can be mixed with opposite signs).
    T = sp.Matrix([[u+other, other-u], [other-u, u+other]])/2
    y = sp.Matrix([1, 1])
    zeta = (T*y)[0]
    E = sp.diag(1, -1)
    t = moments(y.T, T+h*E, y, 5)
    assert t[1].diff(h) == 0 and t[2].diff(h,2) > 0
    assert all(sp.expand(t[j]).diff(h).subs(h,0) == 0 for j in range(len(t)))
    inverse = (sp.eye(2)-T-h*E).inv()
    pressure = (y.T*inverse*y)[0]
    assert sp.simplify(pressure.diff(h).subs(h,0)) == 0
    assert (T*y == zeta*y)
    assert sp.simplify(pressure.diff(h,2).subs(h,0)) > 0
    # A common absolute boundary factor changes the source of -log Z while preserving every conditional law.
    assert sp.simplify((-sp.log((1+h)*(a+sum(ts)+u**8*(1-u)))).diff(h).subs(h,0)) == -1
    print("PASS finite hidden transfers, two-sided variance, delayed positive tariff, and field jets")


if __name__ == "__main__":
    main()
