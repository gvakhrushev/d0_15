"""Replay the unreset alternating field comparisons and two complete record prices."""
from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from math import log
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

root = Path(__file__).resolve().parents[7]
source = root / "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
spec = spec_from_file_location("return_field_native", source)
nt = module_from_spec(spec)
sys.modules[spec.name] = nt
spec.loader.exec_module(nt)


def golden(matrix):
    return DomainMatrix.from_Matrix(matrix).convert_to(nt.GOLDEN_FIELD).to_dense()


def native_checks():
    v = sp.Matrix([nt.A, nt.P])
    j = golden(sp.kronecker_product(sp.eye(4), v, v))
    B = j*j.transpose()
    port = golden(sp.kronecker_product(sp.eye(4), sp.diag(0,1), sp.eye(2)))
    eye = golden(sp.eye(16))
    for wires, q in [((3,2), 2*nt.P**3), ((2,3), nt.P**2)]:
        gate = nt.Gate("CX", wires)
        word = nt.Execution(4, (), (), (gate,), nt.G_CX_SOURCE_I, 2, (0,1))
        a = golden(nt.word_matrix(word, max_qubits=4))
        E = a.transpose()*port*a
        assert j.transpose()*E*j == golden(q*sp.eye(4))
        # All original Spin columns, including the unmeasured complement.
        for i, first in enumerate((E, eye-E)):
            qi = q if i == 0 else 1-q
            entry = first*j
            for k, second in enumerate((B, eye-B)):
                prob = q if i == k else 1-q
                step = second*entry
                assert step.transpose()*step == golden(qi*prob*sp.eye(4))
                for last in (E, eye-E):
                    out = last*step
                    prob2 = q if (k == 0) == (last == E) else 1-q
                    assert out.transpose()*out == golden(qi*prob*prob2*sp.eye(4))


def entropy(x):
    return -x*log(x)-(1-x)*log(1-x)


def enumerate_records(n, q, efficiency, weights):
    # Start after the first real event measurement. Its clock and noisy bit are prior records.
    total = avg_cost = partition = F(0)
    conditional_entropy = 0.0
    for initial, initial_prob in enumerate((q, 1-q)):
        for record in product((-1,0,1), repeat=n):
            last = initial
            probability = F(1)
            price_weight = F(1)
            cost = 0
            for bit in record:
                cost += 3
                if bit == -1:
                    probability *= 1-efficiency
                    price_weight *= weights[0]
                else:
                    probability *= efficiency*(q if bit == last else 1-q)
                    price_weight *= weights[bit+1]
                    cost += 1+bit
                    last = bit
            mass = initial_prob*probability
            total += mass
            avg_cost += mass*cost
            partition += mass*price_weight
            conditional_entropy -= float(mass)*log(float(probability))
    assert total == 1
    return avg_cost, conditional_entropy, partition


def record_checks():
    for q in (F(1,4), F(9,25), F(12,25)):
        k = F(8,11)
        v = 2*q-1
        tau = 1-k+k*v
        for weights in ((F(1,3),F(1,4),F(1,6)), (F(1,3),F(1,4),F(1,4))):
            er, a, b = weights
            T = (1-k)*er*sp.eye(2)+k*sp.Matrix([[q*a,(1-q)*b],[(1-q)*a,q*b]])
            for n in (1,3,6):
                price, ent, Z = enumerate_records(n,q,k,weights)
                assert price == (3+3*k/2)*n-k*v*v*sum(tau**t for t in range(n))/2
                assert abs(ent-n*(entropy(float(k))+float(k)*entropy(float(q)))) < 2e-12
                assert Z == (sp.Matrix([[q,1-q]])*T**n*sp.ones(2,1))[0]
                if a == b:
                    assert Z == ((1-k)*er+k*a)**n
    assert F(1,4)+1+F(21,4) < (1+64*F(71,100))*2/F(13)
    assert 1-F(17,32)**2 > F(71,100)
    x, a, b = sp.symbols("x a b", positive=True)
    S = sp.Matrix([[x*a,(1-x)*sp.sqrt(a*b)],[(1-x)*sp.sqrt(a*b),x*b]])
    v = sp.Matrix([sp.sqrt(a),-sp.sqrt(b)])
    assert S.diff(x) == v*v.T
    perp = sp.Matrix([sp.sqrt(b),sp.sqrt(a)])
    # The Perron eigenvector can lie in v-perp only if a=b.
    assert sp.simplify(sp.Matrix.hstack(perp,S*perp).det() - sp.sqrt(a*b)*(b-a)) == 0


def two_step_calibration():
    q, k, a, b, c, d, u = sp.symbols("q k a b c d u", positive=True)
    rates = ((a,b),(c,d))
    def weight(start, path):
        old = start
        mass = sp.Integer(1)
        for new in path:
            if new == -1:
                mass *= (1-k)*u
            else:
                mass *= k*rates[old][new]*(q if old == new else 1-q)
                old = new
        return mass
    for i in (0,1):
        actual = weight(i,(i,i))/weight(i,(1-i,i))
        assert sp.cancel(actual - rates[i][i]**2/(b*c)*(q/(1-q))**2) == 0
    assert sp.cancel(weight(0,(0,0))/weight(0,(-1,-1))-(k*a*q/((1-k)*u))**2) == 0
    # After calibration every tariff, including erasure, telescopes on the full tree.
    for initial in (0,1):
        for path in product((-1,0,1),repeat=4):
            end = next((i for i in reversed(path) if i != -1), initial)
            ratio = sp.cancel(weight(initial,path)/weight(initial,path).subs({a:1,b:1,c:1,d:1,u:1}))
            assert sp.cancel(ratio.subs({a:u,d:u,c:u**2/b})-u**4*(b/u)**(end-initial)) == 0

    reference, plus, minus = sp.symbols("reference plus minus", positive=True)
    f_plus = reference/(reference+plus)
    f_minus = reference/(reference+minus)
    assert sp.cancel(f_minus/f_plus - (reference+plus)/(reference+minus)) == 0

    # RC3 after a measured Golden fork: null branch is the full old input,
    # active branch is any reached subspace after the late field word.
    j = sp.Matrix([sp.Rational(3,5),sp.Rational(4,5)])
    v = sp.Matrix([nt.A,nt.P])
    embed = sp.kronecker_product(j,v)
    h_field = (j[0])**2
    leaf0 = sp.kronecker_product(j*j.T,sp.diag(1,0))
    leaf1 = sp.kronecker_product(sp.diag(1,0),sp.diag(0,1))
    expected_h = nt.P+nt.P**2*h_field
    assert golden(embed.T*(leaf0+leaf1)*embed) == golden(sp.Matrix([[expected_h]]))
    z = F(1,2**20)
    assert (1-z)**(-4)-1 < 5*z < F(1,2)
    h = sp.symbols("h",positive=True)
    zz, pp = sp.symbols("z p",positive=True)
    alpha = zz/(1-zz)
    # L_active=2 per input column (two complete supported H.1 outcomes).
    full = (1-zz)**(-12)/(1+alpha*(pp+(1-pp)*h))**4
    no_active_fraction = (1-zz)**8*((1+alpha*(pp+(1-pp)*h))/(1+alpha*pp))**4
    assert sp.cancel(full*no_active_fraction-(1-zz*(1-pp))**(-4)) == 0


def independent_record_score():
    # Each efficient leaf may change independently of the two-projector section.
    import numpy as np

    k, q = 0.73, 0.39
    rho = np.array([[0.6,0.19],[0.19,0.4]])
    eigen, basis = np.linalg.eigh(rho)
    root_rho = (basis*np.sqrt(eigen))@basis.T
    delta = np.array([[0.09,0.13],[0.13,-0.02]])
    leaves = []
    for sequence in product((-1,0,1), repeat=2):
        old = 0
        successes = repeats = ones = 0
        prob = 1.0
        for bit in sequence:
            if bit < 0:
                prob *= 1-k
            else:
                successes += 1
                repeats += bit == old
                ones += bit
                prob *= k*(q if bit == old else 1-q)
                old = bit
        multiplier = {(-1,0):1, (1,1):-1}.get(sequence,0)
        leaves.append((prob,successes,repeats,ones,multiplier))

    def full_cq(t):
        ent = 0.
        for prob, _, _, _, multiplier in leaves:
            gram = prob*np.eye(2)+t*multiplier*delta
            vals = np.linalg.eigvalsh(root_rho@gram@root_rho)
            assert vals.min() > 0
            ent -= vals@np.log(vals)
        return ent

    dp = np.trace(rho@delta)
    dk = sum(mult*ns*dp for _,ns,_,_,mult in leaves)
    dr = sum(mult*nr*dp for _,_,nr,_,mult in leaves)
    expected = log((1-k)/(k*(1-q)))*dk+log((1-q)/q)*dr
    assert abs((full_cq(1e-5)-full_cq(-1e-5))/2e-5-expected) < 1e-9


if __name__ == "__main__":
    native_checks()
    record_checks()
    two_step_calibration()
    independent_record_score()
    print("PASS native input columns, complementary field returns, erasure histories, full CQ, finite price bound and two positive transfer laws")
