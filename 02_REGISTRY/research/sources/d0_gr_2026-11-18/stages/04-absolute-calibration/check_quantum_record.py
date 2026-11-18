"""Verify the universal reference, record pinching and Golden word costs on finite models."""
import itertools
import json
import math
import numpy as np
import sympy as sp

p = (math.sqrt(5) - 1) / 2
log_phi = -math.log(p)


def reference(d, m, labels):
    strings = list(itertools.product(range(d), repeat=m))
    index = {word: i for i, word in enumerate(strings)}
    dim = math.comb(m + d*d - 1, m)
    sigma = sp.zeros(len(strings))
    for perm in itertools.permutations(range(m)):
        seen = set()
        cycles = 0
        for j in range(m):
            if j in seen:
                continue
            cycles += 1
            while j not in seen:
                seen.add(j)
                j = perm[j]
        for i, word in enumerate(strings):
            other = tuple(word[k] for k in perm)
            if all(labels[x] == labels[y] for x, y in zip(word, other)):
                sigma[index[other], i] += d**cycles
    sigma /= math.factorial(m) * dim
    assert sigma.trace() == 1
    return dim, sigma


def golden_code(values):
    # All inputs to interval comparisons are rational or in Q(sqrt(5)).
    phi_inverse = (sp.sqrt(5)-1)/2
    words = []
    costs = []
    start = sp.S.Zero
    for size in values:
        mid = start + size/2
        lo, width = sp.S.Zero, sp.S.One
        word = ''
        cost = 0
        while width > size/2:
            split = sp.radsimp(sp.expand(lo + width*phi_inverse))
            if mid < split:
                width = sp.radsimp(sp.expand(split-lo))
                word += '0'
                cost += 1
            else:
                width = sp.radsimp(sp.expand(lo+width-split))
                lo = split
                word += '1'
                cost += 2
        assert lo >= start and lo+width <= start+size
        assert width > phi_inverse**2*size/2
        words.append(word)
        costs.append(cost)
        start += size
    assert start == 1
    assert all(i == j or not b.startswith(a) for i,a in enumerate(words)
               for j,b in enumerate(words))
    return costs


def entropy(eigs):
    return -sum(x * math.log(x) for x in eigs if x > 1e-14)


def run(d, m, labels, densities):
    D, sigma = reference(d,m,labels)
    blocks = {}
    for i, word in enumerate(itertools.product(range(d), repeat=m)):
        blocks.setdefault(tuple(labels[k] for k in word), []).append(i)
    svals, basis = [], []
    for indices in blocks.values():
        pairs = sigma.extract(indices, indices).eigenvects()
        for value, _, vecs in sorted(pairs, key=lambda pair: pair[0], reverse=True):
            assert value > 0
            for small_vector in sp.GramSchmidt(vecs, True):
                vector = sp.zeros(d**m, 1)
                for i, component in zip(indices, small_vector):
                    vector[i] = component
                svals.append(value)
                basis.append(vector)
    U = sp.Matrix.hstack(*basis)
    assert U.H*U == sp.eye(U.cols)
    assert U*sp.diag(*svals)*U.H == sigma
    costs = golden_code(svals)
    max_cost = math.ceil((m*math.log(d)+math.log(2*D/p**2))/log_phi)
    assert max(costs) <= max_cost
    cases = []
    for single in densities:
        assert single.trace() == 1 and single.is_positive_semidefinite
        assert all(single[i,j] == 0 or labels[i] == labels[j]
                   for i in range(d) for j in range(d))
        product = sp.kronecker_product(*([single]*m))
        assert (D*sigma-product).is_positive_semidefinite
        law = (U.H*product*U).diagonal()
        assert sum(law) == 1
        occupied = [i for i,prob in enumerate(law) if prob>0]
        assert sum(svals[i] for i in occupied) >= sp.Rational(1,D)
        z = sum(p**costs[i] for i in occupied)
        target = m*entropy(np.linalg.eigvalsh(np.array(single.evalf(),dtype=complex)))
        observed = entropy([float(x) for x in law])
        charge = log_phi*sum(float(x)*n for x,n in zip(law,costs))
        assert target <= observed + 1e-12 and observed <= charge+1e-12
        assert charge <= target + math.log(2*D/p**2) + 1e-12
        assert p**2/(2*D) < z <= 0.5+1e-12
        mark = sum(float(x)*n/max_cost for x,n in zip(law,costs))
        assert abs(max_cost*log_phi*mark-charge) < 1e-12
        cases.append(dict(binary_entropy_mark=mark,support=len(occupied),entropy_input_block=target,
                          entropy_after_measuring_code=observed,
                          expected_charge_nats=charge,absolute_mass=z))
    return dict(d=d,m=m,pointer=labels,D=D,reference_spectrum=list(map(str,svals)),
                word_costs=costs,cases=cases)


R=sp.Rational
coherent=sp.Matrix([[R(1,2),sp.I/2],[-sp.I/2,R(1,2)]])
rho=sp.Matrix([[R(2,3),R(1,5)],[R(1,5),R(1,3)]])
models=[run(2,2,[0,0],[coherent,rho,sp.eye(2)/2]),
        run(2,3,[0,1],[sp.diag(1,0),sp.diag(R(2,3),R(1,3))]),
        run(3,2,[0,0,1],[sp.diag(coherent,R(0)),sp.diag(rho/2,R(1,2)),sp.eye(3)/3])]
print(json.dumps(dict(status='PASS',models=models,field_independent_code=True,
                    microscopic_Book03_charge_selected=False),indent=2))
