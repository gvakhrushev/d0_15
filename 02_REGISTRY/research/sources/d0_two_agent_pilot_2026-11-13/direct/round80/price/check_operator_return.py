"""First returns, least-disturbed environment, and an exact native nonscalar example."""
from fractions import Fraction as F
from itertools import combinations_with_replacement

import sympy as s

from check_parity_price import Golden, a, p, one, p3, action, ne


def loss(x, y):
    return (x-y)**2/(1-x*y) if x*y != 1 else 0


def check_reflection():
    c = s.diag(0, s.Rational(3,5), s.Rational(5,13), s.Rational(12,13), 1)
    b = s.diag(1, s.Rational(4,5), s.Rational(12,13), s.Rational(5,13), 0)
    # Move two inequivalent old eigenspaces, without changing the old cut.
    v = s.eye(5)
    v[:2, :2] = s.Matrix([[3,-4],[4,3]]) / 5
    c, b = v*c*v.T, v*b*v.T
    eye, zero = s.eye(5), s.zeros(5)
    reflect = c.row_join(b).col_join(b.row_join(-c))
    assert reflect.T == reflect and reflect**2 == s.eye(10)
    inj = eye.col_join(zero)
    project = inj*inj.T
    u = c**2
    survives = inj
    avg = zero.copy()
    for n in range(1,9):
        avg += survives.T*survives
        assert avg == 2*eye-u**(n-1)
        applied = reflect*survives
        k = inj.T*applied
        expected = c if n == 1 else (-1)**(n-2)*(eye-u)*c**(n-2)
        assert expected == k
        survives = (s.eye(10)-project)*applied
        assert survives.T*survives == (eye-u)*u**(n-1)
    return 8


def check_kernel():
    x, y, z = s.symbols('x y z')
    factor = (y-x)*(z-y)*((1-x*x)*(1-y*z)+(1-z*z)*(1-x*y))
    assert s.cancel((loss(x,z)-loss(x,y)-loss(y,z))*(1-x*y)*(1-x*z)*(1-y*z)-factor) == 0
    assert s.cancel(x*y+(1-x*x)*(1-y*y)/(1-x*y)-(1-loss(x,y))) == 0
    values = [F(i,12) for i in range(13)]
    for x,y,z in combinations_with_replacement(values,3):
        assert loss(x,y)+loss(y,z) <= loss(x,z)
        assert (2-loss(x,y)-loss(y,z))/2 >= 1-loss(x,z)/2
        assert 0 <= loss(x,z) <= 1
    # For the extreme equal superposition the Hermitian difference has
    # eigenvalues +/-loss/2, achieving the claimed diamond norm.
    d = loss(F(1,5),F(9,10))
    diff = s.Matrix([[0,s.Rational(d.numerator,2*d.denominator)],
                     [s.Rational(d.numerator,2*d.denominator),0]])
    assert sum(abs(k)*n for k,n in diff.eigenvals().items()) == s.Rational(d.numerator,d.denominator)


def check_native():
    port, y = 2,3
    cx = ne.Gate('CX',(y,port))
    g = ne.Gate('G',(port,))
    z = (ne.Gate('SourceI',(port,0,1)),)*2
    word = (cx,)+z+(g,)+z+z+(g,cx)
    ex = ne.Execution(4, (), (), word, profile=ne.G_CX_SOURCE_I,
                      source_port=port, source_spin=(0,1), report_bits=(port,))
    ne.execution_from_json(ne.canonical_json(ex), max_qubits=4, max_expanded_stages=10)
    def run(state):
        for gate in word:
            state = action(state, gate, 4)
        return state
    matrix = [run({i:one}) for i in range(16)]
    for i, column in enumerate(matrix):
        assert run(column) == {i:one}
        assert all(column.get(j,0)==matrix[j].get(i,0) for j in range(16))
    f = p3*p3
    for spin in range(4):
        for bit in range(2):
            source = {(spin<<2)+bit:a, (spin<<2)+2+bit:p}
            out = run(source)
            assert all(i>>2 == spin and i%2 == bit for i in out)
            cold = sum(val*out.get(i,Golden()) for i,val in source.items())
            assert cold == (one-2*f if bit else one)
    assert (2*a*p)*(2*a*p)+f == one
    return len(word)


if __name__=='__main__':
    depth = check_reflection()
    check_kernel()
    stages = check_native()
    print(f'{depth} exact caps with rotating eigenspaces; Schur kernel and diamond bound verified')
    print(f'{stages} native stages on the full 16 columns: C=diag(1,1-2*p^6) on old bit')
