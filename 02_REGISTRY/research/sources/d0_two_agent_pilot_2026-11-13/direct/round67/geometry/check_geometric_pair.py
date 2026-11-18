"""Exact original PC8/JZ6 calculation for a shear at one free site."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import sympy as sp


def matrix_unit(i, j):
    return sp.eye(4)[:, i]*sp.eye(4)[:, j].T


def fock_density(n, face):
    """-Tr_Λ(dΓ(n) Λ(face))/8 over all 16 basis vectors."""
    derivative = n*face
    trace = 0
    for grade in range(1, 5):
        for subset in combinations(range(4), grade):
            base = face.extract(subset, subset)
            linear = derivative.extract(subset, subset)
            for j in range(grade):
                col = base.copy()
                col[:, j] = linear[:, j]
                trace += col.det()
    return sp.expand(-trace/8)


def verify_geometry():
    t, curvature, h, slope, b = sp.symbols("t k h a b", nonzero=True)
    eta = sp.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    coframe = sp.eye(4) + t*matrix_unit(0,1)
    assert coframe.det() == 1
    columns = eta*coframe.inv().T
    result = 0
    for i, j in combinations(range(4), 2):
        g = columns[:,i]*columns[:,j].T - columns[:,j]*columns[:,i].T
        f = -curvature*h*h*(matrix_unit(1,j)+matrix_unit(j,0)) if i == 0 and j in (2,3) else sp.zeros(4)
        assert f**3 == sp.zeros(4)
        face = sp.eye(4)+f+f**2/2
        value = sp.factor(fock_density(g*eta,face)/h**2)
        assert value == (-curvature*t if i == 0 and j in (2,3) else 0)
        result += value
    assert sp.expand(result + 2*curvature*t) == 0
    grad0 = sp.Matrix([slope, 0, 0, 0])
    grad15 = -b*sp.ones(4,1)/h
    inv_metric = (coframe.T*eta*coframe).inv()
    matter = sum((g.T*inv_metric*g)[0] for g in (grad0, grad15))
    assert sp.factor(matter+2*t*(slope**2+b**2/h**2)) == 0
    k0 = sp.symbols("k0")
    density = result.subs(curvature,k0*slope*slope) - k0*matter
    assert sp.factor(h**4*sp.diff(density,t)-2*h*h*k0*b*b) == 0


def certify_response_bounds():
    z = F(1,2**20)
    h, b, tau, eps = F(1,8), F(1,8192), F(1,4096), F(1,64)
    d = (b/h)**2
    assert d == F(1,2**20)
    # p in (3/5, 5/8); PC3 gives r_q=8 z p^6 (R_E + p^6 Q_E).
    assert 8*F(3,5)**6*(1-2*z) > F(1,4)
    mass_max = F(5,32)**2+d
    assert mass_max < F(1,16)
    y_max = 2*eps*mass_max*tau
    assert y_max < F(1,2**21)
    # For u=p+p²y in [0,1], B=4u²(1-u²), B≤1, |B'|≤24,
    # |B''|≤56, |B'''|≤96 in y (since |du/dy|<1).
    assert F(5,8)+F(5,8)**2/64 < 1
    assert F(3,5)-F(5,8)**2/64 > 0
    third = (2+3*z)*96 + 6*z*24*56  # upper bound for |r'''|/z
    assert third < 200
    assert mass_max*third*y_max**2/(6*F(1,4)*d) < F(1,2**18)
    assert F(15,16)*F(3,5)**2 > b*b


def verify_address_prices():
    forward, reverse, source = "CX(e,y)", "CX(y,e)", "SourceI(e)"
    swap = (forward, reverse, forward)
    phase = (*swap, source, source, *swap)
    identity = (*phase, *phase, forward, forward)
    signed = (*phase, forward, *phase, forward)
    assert len(identity) == len(signed) == 18 and Counter(identity) == Counter(signed)
    states = ((0, 0), (0, 1), (1, 0), (1, 1))

    def trace(word, start):
        e, y = start
        active = 0
        count = Counter()
        # In the four-dimensional Spin representation, shifts differing by 2
        # give the same conditional density, including with a reference.
        spin_count = Counter()
        for command in word:
            count[command, (e, y)] += 1
            spin_count[command, (e, y), active % 2] += 1
            if command == source:
                active += e
            elif command == forward:
                y ^= e
            else:
                e ^= y
        assert (e, y) == start
        return count, spin_count, active

    rows = {forward: (0, -2, 1, 1), reverse: (0, -1, 2, -1), source: (0, -2, 0, 2)}
    differences = {}
    for start in states:
        base, base_spin, first = trace(identity, start)
        kick, kick_spin, second = trace(signed, start)
        assert (second - first) % 4 == 2 * start[0]
        sign = start[0] * (1 - 2 * start[1])
        for command, row in rows.items():
            assert [kick[command, x] - base[command, x] for x in states] == [sign * n for n in row]
        differences[start] = {key: kick_spin[key] - base_spin[key] for key in base_spin.keys() | kick_spin.keys()}
    assert all(not any(differences[x].values()) for x in states[:2])
    both = differences[1, 0].keys() | differences[1, 1].keys()
    assert all(differences[1, 0].get(key, 0) == -differences[1, 1].get(key, 0) for key in both)

    p = (sp.sqrt(5) - 1) / 2
    for first_command, imbalance in [(reverse, 0), (forward, -p**5)]:
        probs = {}
        for e, y in states:
            new = (e ^ y, y) if first_command == reverse else (e, e ^ y)
            probs[new] = p**(1+e) * p**(1+y)
        assert sp.simplify(probs[1, 0] - probs[1, 1] - imbalance) == 0


if __name__ == "__main__":
    verify_geometry()
    certify_response_bounds()
    verify_address_prices()
    print("Pass: two paid words, twelve signed address occupations, Spin shifts, two exact preparation imbalances.")
    print("Pass: six based faces, every CAR16 grade, both gradients, positive shear slope and <2^-18 finite-pair relative error.")
