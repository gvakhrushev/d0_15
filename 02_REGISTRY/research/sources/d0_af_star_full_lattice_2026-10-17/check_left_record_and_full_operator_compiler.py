#!/usr/bin/env python3
"""Bounded exact consumer: LEFT recording and fixed-width real compilation.

The all-level/all-word theorems are proved in full-source sections 6.13-6.14.
This checks actual full A1 GNS matrices, elementary compiler identities and
the characteristic-two obstruction. It supplies no physical admission.
"""
import itertools
import json
import sympy as s


def require(value, label):
    if not value:
        raise ArithmeticError(label)


def left_record():
    # Full A1=M2 (+) M1 GNS; both matrix indices remain, not just its diagonal.
    basis = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)]
    index = {pair: i for i, pair in enumerate(basis)}
    copy = s.zeros(20)
    blank = s.zeros(20, 5)
    for i, (row, column) in enumerate(basis):
        blank[4*i, i] = 1
        for y in range(4):
            copy[4*i+(y ^ row), 4*i+y] = 1
    require(copy.T*copy == s.eye(20) and copy*copy == s.eye(20),
            'full retained LEFT-copy word is an involutive unitary')
    projectors = [s.diag(*[int(row == label) for row, _ in basis])
                  for label in range(3)]
    for label, P in enumerate(projectors):
        Y = s.diag(*[int(y == label) for y in range(4)])
        F = blank.T*copy.T*s.kronecker_product(s.eye(5), Y)*copy*blank
        require(F == P, 'exact LEFT effect on every full-GNS input')
    require(projectors[0][index[(0, 1)], index[(0, 1)]] == 1,
            'offdiagonal E01 is recorded by LEFT index zero')
    right_basis = []
    for row, col in itertools.product(range(2), repeat=2):
        A = s.zeros(5)
        for i in range(2):
            A[index[(i, col)], index[(i, row)]] = 1
        right_basis.append(A)
    right_basis.append(s.diag(0, 0, 0, 0, 1))
    for A in right_basis:
        R = s.kronecker_product(A, s.eye(4))
        require(copy*R == R*copy, 'all noncommutative right archive observables commute')
    # Positive effect mixing right-column coordinates inside a LEFT sector.
    effect = s.diag(s.Rational(2, 3), s.Rational(1, 3),
                    s.Rational(1, 4), s.Rational(3, 4), s.Rational(1, 2))
    effect[0, 1] = effect[1, 0] = s.Rational(1, 9)
    total = s.zeros(5)
    for outcome in range(4):
        Y = s.diag(*[int(y == outcome) for y in range(4)])
        for E in (effect, s.eye(5)-effect):
            F = copy.T*s.kronecker_product(E, Y)*copy
            for y, z in itertools.permutations(range(4), 2):
                require(F.extract([4*i+y for i in range(5)],
                                  [4*i+z for i in range(5)]) == s.zeros(5),
                        'all terminal effects are diagonal in INITIAL Y blocks')
            compressed = blank.T*F*blank
            expected = projectors[outcome]*E if outcome < 3 else s.zeros(5)
            require(compressed == expected, 'same full joint instrument after copying')
            total += compressed
    require(total == s.eye(5), 'all valid and invalid pointer codes retained')
    return {'actual_GNS_dimension': 5, 'record_bits': 2, 'complete_dimension': 20,
            'LEFT_effects': 'exact on full GNS, including E01 and E10',
            'RIGHT_algebra': 'all five matrix-unit generators commute',
            'offblank_pure_first_sources': 'zero by initial-Y block orthogonality',
            'invalid_codes': 'retained; zero on legal blank input',
            'not_inferred': 'faithful-density birth derivatives or C2 boundary regularity'}


def cnot(n, control, target):
    out = s.zeros(2**n)
    for x in range(2**n):
        out[x ^ (((x >> control) & 1) << target), x] = 1
    return out


def plane(n, u, v):
    out = s.zeros(2**n)
    out[v, u], out[u, v] = 1, -1
    return out


def compiler_generators():
    patterns, routed = 0, 0
    for n in (2, 3):
        size = 2**n
        for target in range(n):
            controls = [k for k in range(n) if k != target]
            J = s.zeros(size)
            for x in range(size):
                if not ((x >> target) & 1):
                    J += plane(n, x, x ^ (1 << target))
            generators = []
            for mask in range(2**len(controls)):
                subset = [bit for j, bit in enumerate(controls) if (mask >> j) & 1]
                C = s.eye(size)
                for bit in subset:
                    C = cnot(n, bit, target)*C
                Z = s.diag(*[(-1)**sum((x >> bit) & 1 for bit in subset)
                             for x in range(size)])
                require(C*J*C == Z*J, 'CNOT conjugates the real rotation generator')
                generators.append(C*J*C)
            for A, B in itertools.product(generators, repeat=2):
                require(A*B == B*A, 'Walsh rotation generators commute')
            for pattern in range(2**len(controls)):
                u = sum(((pattern >> j) & 1) << bit for j, bit in enumerate(controls))
                expected = plane(n, u, u ^ (1 << target))
                actual = s.zeros(size)
                for mask, A in enumerate(generators):
                    actual += s.Rational((-1)**(bin(pattern & mask).count('1')),
                                         2**len(controls))*A
                require(actual == expected, 'exact uniformly controlled Givens generator')
                patterns += 1
        for u, v in itertools.combinations(range(size), 2):
            different = [bit for bit in range(n) if ((u ^ v) >> bit) & 1]
            P, current = s.eye(size), v
            for bit in different[:-1]:
                after = current ^ (1 << bit)
                J = plane(n, current, after)
                P = (s.eye(size)+J+J*J)*P  # exact signed pi/2 swap
                current = after
            require(P.T*P == s.eye(size), 'Gray route is a full orthogonal signed permutation')
            require(P.T*plane(n, u, current)*P == plane(n, u, v),
                    'every two-level generator follows from adjacent rotations')
            routed += 1
    return {'control_patterns_checked': patterns, 'two_level_routes_checked': routed,
            'all_n_proof': 'commuting Walsh exponentials, Gray routing, Givens QR',
            'operator_approximation': 'full carrier; M rotations each at eta/M suffice',
            'precision_dependent_extra_registers': 0,
            'det_minus_one': 'one fixed spectator suffices',
            'physical_limits': 'requires coherent addressed wires and supplied field queries'}


def exact_gate_obstruction():
    a = s.Symbol('a')
    polynomial = s.Poly(a**4+a*a+1, a, modulus=2)
    def mod2(x):
        return s.rem(s.Poly(s.expand(x), a, modulus=2), polynomial).as_expr()
    epsilon, b = a*a+a+1, a+a*a
    require(mod2(epsilon) != 0 and mod2(epsilon*epsilon) == 0,
            'nonzero nilpotent in the actual characteristic-two quotient')
    require(mod2(b*b-1) == 0 and mod2(b-1) != 0, 'b squared is one, but b is not one')
    G = s.Matrix([[a, -a*a], [a*a, a]])
    full = s.Matrix([[a, 0, -a*a, 0], [0, a, 0, -a*a],
                     [0, a*a, 0, a], [a*a, 0, a, 0]])
    for gate in (G, G.T, full):
        require(all(mod2(sum(gate.row(j))-b) == 0 for j in range(gate.rows)),
                'all golden primitive row sums equal b modulo two')
        require(all(mod2(sum(gate.col(j))-b) == 0 for j in range(gate.cols)),
                'all golden primitive column sums equal b modulo two')
    controlled = s.diag(s.eye(2), G)
    sums = [mod2(sum(controlled.col(j))) for j in range(4)]
    require(sums == [1, 1, b, b], 'exact controlled-G has forbidden unequal column sums')
    C = cnot(2, 1, 0)
    echo = s.kronecker_product(s.eye(2), G)*C*s.kronecker_product(s.eye(2), G.T)*C
    modulus = s.Poly(a**4+a*a-1, a)
    expected = s.diag(s.eye(2), G*G)
    require(all(s.rem(s.Poly(s.expand(x), a), modulus).is_zero for x in echo-expected),
            'owned echo implements controlled-G-squared, retaining all columns')
    return {'all_word_invariant': 'all row and column sums are b^N modulo two',
            'clean_READY_PENDING': 'impossible in finite golden/permutation palette',
            'LEFT_copy': 'not excluded: it is a permutation with all sums one',
            'dirty_coarse_refinement_source': 'h(p^2) DPr(PENDING)/log(phi)',
            'approximation': 'not obstructed; mod-two reduction is not norm continuous'}


def rank_birth_first_source():
    x = s.Symbol('x', positive=True)
    entropy = -x*x*s.log(x*x)-(1-x*x)*s.log(1-x*x)
    require(s.limit(s.diff(entropy, x), x, 0, dir='+') == 0,
            'complete normalized pure rank birth has zero first source')
    require(s.limit(s.diff(entropy, x, 2), x, 0, dir='+') == s.oo,
            'the same retained zero outcome rejects an ambient C2 claim')
    return {'full_two_outcome_law': ['x^2', '1-x^2'],
            'first_source_at_zero': 0, 'second_source_at_zero': '+infinity',
            'all_outcome_C1_bound': '64*K*L*epsilon*(1+abs(log(epsilon)))/log(phi)',
            'bound_proof': 'analytic radial modulus in the owner; no probability floor'}


if __name__ == '__main__':
    print(json.dumps({'schema': 'd0-left-record-full-operator-compiler/1',
                      'status': 'PASS_SCOPED_LEFT_INSTRUMENT_AND_COMPILER',
                      'LEFT_instrument': left_record(),
                      'full_operator_compiler': compiler_generators(),
                      'exact_gate_boundary': exact_gate_obstruction(),
                      'zero_outcome_source': rank_birth_first_source()},
                     ensure_ascii=False, sort_keys=True, indent=2))
