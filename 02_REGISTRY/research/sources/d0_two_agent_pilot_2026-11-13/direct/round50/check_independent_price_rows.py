#!/usr/bin/env python3
"""Exact before-post and nonsymmetric-return checks for the A50 composition.

Small matrices test the algebra and hostile cases. The production result
uses the written norm proof and pinned component theorems, not a sample.
"""
from pathlib import Path
from hashlib import sha256
import json, sys
import sympy as s
import independent_price_rows as rows

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
R = s.Rational


def rotation(t):
    return s.Matrix([[1-t*t, -2*t], [2*t, 1-t*t]])/(1+t*t)


def exact_checks():
    chi = s.Matrix([R(3, 5), R(4, 5)])
    X = s.Matrix([[0, -1], [1, 0]])
    eye = s.eye(2)
    zero = s.Matrix([1, 0])
    embed = s.kronecker_product(eye, zero)
    B = s.diag(eye, rotation(R(1, 5)))
    cases = [
        ('exact_profile', B.T, s.kronecker_product(eye, s.diag(1, -1))),
        ('independent_native_like_return', s.diag(eye, rotation(-R(1, 6))),
         s.kronecker_product(eye, rotation(R(1, 100))*s.diag(1, -1))),
    ]
    checked = []
    for name, C, middle in cases:
        assert C.T*C == s.eye(4) and middle.T*middle == s.eye(4)
        assert middle*s.kronecker_product(X, eye) == s.kronecker_product(X, eye)*middle
        if name != 'exact_profile':
            assert C != B.T
        M = embed.T*C*middle*B*embed
        assert M.is_diagonal() and all(R(2, 3) < M[i, i] <= 1 for i in range(2))
        r = s.sqrt((chi.T*M*M*chi)[0])
        xi = M*chi/r
        cosine = (chi.T*xi)[0]
        sine = chi[1]*xi[0]-chi[0]*xi[1]
        U = s.Matrix([[cosine, -sine], [sine, cosine]])
        assert s.simplify(U.T*U) == eye and s.simplify(U*xi) == chi

        def corner(pf=eye, qf=eye, qb=eye, pb=eye, post=U):
            value = chi.T*post*pb.T*embed.T*C*s.kronecker_product(qb, eye)*middle
            value = value*s.kronecker_product(qf.T, eye)*B*embed*pf*chi
            return s.simplify(value[0])

        dpf = s.simplify((chi.T*U*M*X*chi)[0])
        dpb = s.simplify(-(chi.T*U*X*M*chi)[0])
        dqb = s.simplify((chi.T*U*embed.T*C*s.kronecker_product(X, eye)*middle*B*embed*chi)[0])
        dqf = s.simplify(-(chi.T*U*embed.T*C*middle*s.kronecker_product(X, eye)*B*embed*chi)[0])
        assert dpb == 0 and dpf != 0 and dqb != 0 and dqf == -dqb
        assert s.simplify(dpf-(chi.T*M*M*X*chi)[0]/r) == 0
        # Pb is before the fixed post. Its exact finite curve is even,
        # independently of whether actual return is B.T or S is symmetric.
        t = R(1, 70)
        plus, minus = rotation(t), rotation(-t)
        assert corner(pb=plus) == corner(pb=minus)
        assert corner(qb=plus) == corner(qf=minus)
        assert corner(qb=minus) == corner(qf=plus)
        assert s.simplify(corner(qb=plus)**2-corner(qb=minus)**2) != 0
        # The post and the two native controls each retain their own error.
        # Neither target evenness nor commutation removes those errors.
        Uhat = rotation(R(1, 1000))*U
        assert corner(pb=plus, post=Uhat) != corner(pb=minus, post=Uhat)
        wrong_minus = rotation(-t-R(1, 10000))
        assert corner(pb=plus) != corner(pb=wrong_minus)
        # A fixed intermediate CODE effect changes even when endpoint
        # swap and full clock stage conjugacy are available.
        mark = s.diag(1, 0)
        assert plus.T*mark*plus != mark
        checked.append({'case': name,
                        'actual_return_identified_with_forward_inverse': C == B.T,
                        'Pb_before_post_exact_analytic_zero_and_finite_even': True,
                        'Q_rows_nonzero_opposite': True,
                        'approximate_post_breaks_exact_Pb_evenness': True,
                        'independent_noninverse_controls_break_exact_Pb_evenness': True,
                        'endpoint_swap_does_not_identify_fixed_CODE_mark': True})
    # CODE only as control is insufficient for the INNER commutant:
    # its entire support must be disjoint from CODE.
    bad_middle = s.diag(1, 1, 1, -1)
    assert bad_middle*s.kronecker_product(X, eye) != s.kronecker_product(X, eye)*bad_middle
    return checked


def main():
    plan = rows.build()
    assert plan == rows.read(P/'INDEPENDENT_PRICE_ROWS_PLAN.json')
    for path, digest in plan['source_sha256'].items():
        assert sha256(Path(path).read_bytes()).hexdigest() == digest, path
    result = {'status': 'PASS_EXACT_FOUR_ROW_ORDER_HOSTILE_CASES_AND_NEW_BOUNDS',
              'fixtures': exact_checks(),
              'CODE_control_only_is_not_enough_for_inner_commutant': True,
              'actual_A49_middle_support_binding_checked': True,
              'all_four_2688_axis_rows_Euclidean_bound_checked': True,
              'all_controls_or_original_Vh_norm_closed': False,
              'production_kernel_or_word_executed': False,
              'source_sha256': {str(f): sha256(f.read_bytes()).hexdigest()
                                for f in [Path(__file__), P/'independent_price_rows.py',
                                          P/'INDEPENDENT_PRICE_ROWS_PLAN.json']},
              'physical_C_closed': False, 'GR_closed': False}
    (P/'INDEPENDENT_PRICE_ROWS_CHECK.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'])


if __name__ == '__main__':
    main()
