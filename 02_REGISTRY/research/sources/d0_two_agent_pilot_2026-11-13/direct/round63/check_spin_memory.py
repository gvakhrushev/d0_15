"""Exact checks for the H.1 reconstruction with the complex structure on real Spin4."""
import sympy as sp
from itertools import combinations


def clock_calibration():
    q = sp.Rational(2, 5)
    y = q*q
    # k=2 coarse words; fine flags and valid readouts marginalize for the true clock law.
    word = [(1-y)**2, y*(1-y), y*(1-y), y**2]
    survival = [sp.factorial(t) * sum(sp.prod(xs) for xs in combinations(word, t))
                for t in range(5)] + [0]
    mass = {t: survival[t-1] - survival[t] for t in range(2, 6)}
    assert sum(mass.values()) == 1 and all(v > 0 for v in mass.values())
    means = sp.zeros(2, 1)
    second = sp.zeros(2)
    for t, probability in mass.items():
        T = sp.Matrix([t, t*(t-1)//2])
        means += probability*T
        second += probability*T*T.T
    cov = second-means*means.T
    vandermonde = sum(mass[i]*mass[j]*mass[l]*((j-i)*(l-i)*(l-j))**2
                      for i, j, l in combinations(mass, 3))/4
    assert cov.det() == vandermonde >= mass[2]*mass[3]*mass[4] > 0
    s = sp.symbols("s", positive=True)
    k = 2
    absolute = {t: p * s**(24*k*t) for t, p in mass.items()}
    denominator = sum(absolute.values())
    numerator = sum(t*p for t, p in absolute.items())
    direct = numerator.diff(s).subs(s, 1) - means[0]*denominator.diff(s).subs(s, 1)
    assert denominator.subs(s, 1) == 1 and direct == 24*k*cov[0, 0]


def quaternion_test():
    I = sp.eye(4)
    Li = sp.Matrix([[0,-1,0,0], [1,0,0,0], [0,0,0,-1], [0,0,1,0]])
    Lj = sp.Matrix([[0,0,-1,0], [0,0,0,1], [1,0,0,0], [0,-1,0,0]])
    Lk = Li*Lj
    assert Lj*Li == -Lk and Lk*Lk == -I
    x, y, z, w = sp.symbols("x y z w", real=True)
    U = x*I + y*Li + z*Lj + w*Lk
    norm = x*x+y*y+z*z+w*w
    assert (U.T*U).applyfunc(sp.expand) == norm*I
    change = U - Li.T*U*Li
    assert change == 2*(z*Lj+w*Lk)
    dark = U*change
    assert (dark.T*dark - 4*norm*(z*z+w*w)*I).applyfunc(sp.expand) == sp.zeros(4)
    # Native control-J, spectator letter and inverse-J on all tail/spectator/Spin columns.
    a = sp.symbols("a", real=True)
    G = sp.Matrix([[a, -a**2], [a**2, a]])
    controlled = sp.diag(sp.eye(8), sp.kronecker_product(sp.eye(2), Li))
    spectator = sp.kronecker_product(sp.eye(2), G, I)
    assert controlled.T * spectator * controlled == spectator
    # Conjugating the test letter on the spectator gives the two predicted Spin blocks.
    weighted = sp.kronecker_product(sp.eye(2), G, U)
    expected = sp.diag(sp.kronecker_product(G, U), sp.kronecker_product(G, Li.T*U*Li))
    assert controlled.T * weighted * controlled == expected


def main():
    a, b, c, d, e = sp.symbols("a b c d e")
    K = sp.Matrix([[b, c], [d, e]])
    X = sp.Matrix([[0, 1], [1, 0]])
    v = sp.Matrix([a, a**2])
    residual = (X*K*X*K)[1, 0] * (X*K*X*v)[0]
    assert sp.expand(residual-b*(c+d)*(d*a**2+e*a)) == 0
    x, y = sp.symbols("x y", real=True)
    u = x+sp.I*y
    reduced = sp.Matrix([[1, -a], [a, u]])
    assert sp.simplify((reduced*v)[0]-a*(1-a**2)) == 0
    assert sp.simplify((reduced*v)[1]-a**2*(1+u)) == 0
    abs_u_plus_one = sp.expand_complex((1+u)*(1+sp.conjugate(u))).expand()
    assert sp.simplify(abs_u_plus_one-(1+2*x+x*x+y*y)) == 0
    # The difference of the two complex branch norms, before imposing |u|=1.
    real_a = sp.symbols("r", real=True)
    rK, rv = reduced.subs(a, real_a), v.subs(a, real_a)
    f, g = rK*rv, rK*X*rv
    assert sp.simplify((f.H*f-g.H*g)[0]-(real_a**2-real_a**4)*(1-x*x-y*y)) == 0
    # Quaternion frame on Spin4, controlled-SourceI and an entangled input.
    L = sp.diag(sp.Matrix([[0, -1], [1, 0]]), sp.Matrix([[0, -1], [1, 0]]))
    I = sp.eye(4)
    assert L.T == -L and L*L == -I
    U = (3*I+4*L)/5
    assert U.T*U == I
    Ubank = sp.diag(U, U)
    sourceI = sp.diag(I, L)
    assert Ubank*sourceI == sourceI*Ubank
    state = sp.zeros(8, 1)
    state[0], state[5] = sp.Rational(3, 5), sp.Rational(4, 5)
    pure = state*state.T
    record = sp.diag(sp.zeros(4), I)
    assert sp.trace(record*Ubank*pure*Ubank.T) == sp.trace(record*pure)
    assert Ubank*pure*Ubank.T != pure
    C0 = (I+2*L)/3
    CU = U**7 * C0
    assert CU.T*CU == C0.T*C0
    G = sp.Matrix([[a, -a**2], [a**2, a]])
    Z = sp.diag(1, -1)
    assert Z*G*Z == G.T
    assert (U**2).T * U**2 == I
    assert G.T*G == (a*a+a**4)*sp.eye(2)
    # For a=sqrt(p), a²+a⁴=1. Each G contributes one amplitude scale.
    gain = sp.symbols("gain", positive=True)
    assert (gain**2*U**2).T * (gain**2*U**2) == gain**4*I
    clock = sp.kronecker_product(G, I)
    assert clock+clock.T == 2*a*sp.eye(8)
    assert (-clock)+(-clock).T == -2*a*sp.eye(8)
    clock_calibration()
    quaternion_test()
    print("PASS: E0 and echo, Spin4, quaternion dark output, feedback, heat and stopped-clock calibration")


if __name__ == "__main__":
    main()
