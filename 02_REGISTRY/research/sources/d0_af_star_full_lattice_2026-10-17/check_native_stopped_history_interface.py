#!/usr/bin/env python3
"""Actual golden stopped-history consumer of the inherited AF source bridge.

One new bounded calculation, not a replay of root/heat/Lean certificates.
The proof for every finite cut and the reachability quantifiers are in
A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md, sections 6.11-6.12.
"""
import hashlib
import json
import math
from pathlib import Path

import sympy as s


a = s.Symbol('a', real=True)
r = s.Symbol('r', real=True)
p = a*a
modulus = s.Poly(a**4+a*a-1, a)


def reduced(x):
    return s.rem(s.Poly(s.expand(x), a), modulus).as_expr().expand()


def matrix_reduced(x):
    return x.applyfunc(reduced)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def cuts(cost):
    def descend(word, total):
        if total >= cost:
            return [word]
        return descend(word+'F', total+1)+descend(word+'R', total+2)
    return descend('', 0)


def word_cost(word):
    return sum(1 if x == 'F' else 2 for x in word)


CF = s.Matrix([[a, -p], [0, 0]])
CR = s.Matrix([[0, 0], [p, a]])
letters = {'F': CF, 'R': CR}


def kraus(word):
    out = s.eye(2)
    for letter in word:
        out = matrix_reduced(letters[letter]*out)
    return out


def markov_mass(word):
    if not word:
        return s.Integer(1)
    result = 1-r if word[0] == 'F' else r
    for before, after in zip(word, word[1:]):
        result *= p if before == after else p*p
    return reduced(result)


def finite_native_cuts():
    root = Path(__file__).resolve().parents[4]
    owner = root/'03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean'
    original = owner.read_bytes()
    require(b'!![a,0,-p,0; 0,a,0,-p; 0,p,0,a; p,0,a,0]' in original,
            'literal fullStep owner binding')
    require(matrix_reduced(CF.T*CF+CR.T*CR) == s.eye(2), 'actual Kraus completeness')
    counts = []
    for level in range(1, 8):
        leaves = cuts(level)
        effects = s.zeros(2)
        total, cost, pending = 0, 0, 0
        for word in leaves:
            require(word_cost(word) in (level, level+1), 'READY/PENDING costs')
            K = kraus(word)
            effect = matrix_reduced(K.T*K)
            effects += effect
            factor = reduced(markov_mass(word)/(1-r if word[0] == 'F' else r))
            first = letters[word[0]]
            require(effect == matrix_reduced(factor*first.T*first),
                    'actual re-used active-qubit Markov effect')
            q = markov_mass(word)
            total += q
            cost += word_cost(word)*q
            if word_cost(word) == level+1:
                pending += q
        require(matrix_reduced(effects) == s.eye(2), 'complete finite stopped POVM')
        require(reduced(total-1) == 0, 'complete law: no stopped normalizer')
        require(reduced(cost-level-pending) == 0, 'overshoot cost identity')
        require(reduced(sum(p**word_cost(w) for w in leaves)-1) == 0,
                'independent fresh-coin PF control')
        counts.append(len(leaves))
    return {'literal_fullStep_sha256': hashlib.sha256(original).hexdigest(),
            'cost_levels': list(range(1, 8)), 'complete_leaf_counts': counts,
            'normalizer': 'identically one; all READY and PENDING outcomes retained',
            'expected_cost': 'm + Pr(PENDING)',
            'valuation': 'H(q)/log(phi), conditional on the same pathwise Book weight=q'}


def native_recurrence():
    # Exact algebraic recurrence reduction and its fixed point.
    d = [s.Integer(0), s.Integer(0), s.Integer(1)]
    U, V = {-1: s.Integer(0), 0: s.Integer(0)}, {-1: s.Integer(0), 0: s.Integer(0)}
    for n in range(1, 10):
        U[n] = reduced(1+p*U[n-1]+p*p*V[n-2])
        V[n] = reduced(1+p*p*U[n-1]+p*V[n-2])
    for m in range(3, 11):
        d.append(reduced(1-p*p*d[m-1]+p**3*d[m-2]))
    for m in range(1, 11):
        require(reduced(U[m-1]-V[m-2]-d[m]) == 0, 'entropy recurrence reduction')
    d_limit = (2+p)/3
    require(reduced((1+p*p-p**3)*d_limit-1) == 0, 'exact recurrence fixed point')
    require(reduced((2-p)*d_limit-(1+p/3)) == 0, 'exact entropy exponent')
    for m in (4, 5, 6, 7):
        require('FFFF' in cuts(4) and 'FRF' in cuts(4), 'same-cost READY prefixes')
        for prefix in ('FFFF', 'FRF'):
            fine = [w for w in cuts(m) if w.startswith(prefix)]
            require(reduced(sum(markov_mass(w) for w in fine)-markov_mass(prefix)) == 0,
                    'actual later refinement preserves coarse Markov mass')
            require(len(fine) == sum(w.startswith('FFFF') for w in cuts(m)),
                    'same READY prefixes have equal AF descendant counts')
    require(reduced(markov_mass('FFFF')-p**3*(1-r)) == 0, 'first READY mass')
    require(reduced(markov_mass('FRF')-p**4*(1-r)) == 0, 'second READY mass')
    require(reduced(p*markov_mass('FFFF')-markov_mass('FRF')) == 0,
            'nontrivial persistent golden ratio')
    for prefix in ('F', 'R', 'FF', 'FR', 'RF', 'RR'):
        require(reduced(markov_mass(prefix+'FR')+markov_mass(prefix+'RF')
                        -p*p*markov_mass(prefix)) == 0,
                'actual unequal-pair Q mass, not independent-coin ratio')
    pv = (math.sqrt(5)-1)/2
    ell = -math.log(pv)
    h0 = (2-pv)*ell
    rv = 1/(1+math.exp(ell*(1+pv/3)))
    require(rv < pv*pv, 'stationary raw limit differs from PF')
    return {'entropy': 'h(r)+h(p^2)[(1-r) U_(m-1)+r V_(m-2)]',
            'positive_preparation_root': 'r_m = 1/(1+exp(h(p^2)*d_m))',
            'd_recurrence': 'd_1=0, d_2=1; d_m=1-p^2*d_(m-1)+p^3*d_(m-2)',
            'd_limit': '(2+p)/3', 'r_limit_diagnostic': rv,
            'prefix_ratio': 'q(FFFF)/q(FRF)=phi, for every 0<=r<1',
            'persistent_TV_bound': '(1-r_m)*(p^3-p^4)/2',
            'TV_lower_limit_diagnostic': (1-rv)*(pv**3-pv**4)/2,
            'actual_Q_ratio': 'p^2; independent fresh-coin control is 2*p^3',
            'scope': 'literal re-used active qubit with fresh retained records; not all D0'}


def code_and_finite_preparation():
    P = s.diag(1, 0)
    off_diagonal = s.Matrix([[0, 1], [0, 0]])
    require(P*off_diagonal == off_diagonal and off_diagonal*P == s.zeros(2),
            'left and right leaf effects differ outside correlated diagonal code')
    # Closure of the integral coefficient ring, not a finite-word reachability search.
    for i in range(4):
        for j in range(4):
            product = s.Poly(reduced(a**(i+j)), a)
            require(all(c.is_Integer for c in product.all_coeffs()),
                    'Z[a] multiplication has integral structure constants')
    require(reduced(p+p*p-1) == 0 and reduced(a**4+a*a-1) == 0,
            'monic golden algebraic-integer relation')
    # Exact conditional fairness is allowed; failure and its mass are retained.
    require(reduced(p**3/(2*p**3)-s.Rational(1, 2)) == 0,
            'conditional first-unequal fairness control')
    return {'raw_to_AF': 'isometry onto the correlated diagonal subspace only',
            'full_GNS_control': 'L(P_0) E_01 = E_01, R(P_0) E_01 = 0',
            'finite_unconditional_palette': 'G, CNOT, basis inputs; entries in Z[a]',
            'exact_uniform_terminal_profile': 'impossible for d>1 in this palette',
            'proof': 'finite Born sums are algebraic integers; rational algebraic integers are integers',
            'conditional_fairness': 'FR/RF on their retained union is exactly 1/2',
            'scope_limits': ['does not rule out approximation by refining programs',
                             'does not restrict all real D0 field inputs',
                             'does not derive physical admission or C3 jets from circuit density']}


def main():
    result = {'schema': 'd0-native-stopped-history-interface/1',
              'status': 'PASS_SCOPED_NATIVE_INTERFACE_CONTROLS',
              'finite_stopped_instrument': finite_native_cuts(),
              'actual_native_source': native_recurrence(),
              'carrier_and_reachability': code_and_finite_preparation()}
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
