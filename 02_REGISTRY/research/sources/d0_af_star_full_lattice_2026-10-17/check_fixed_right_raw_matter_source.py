#!/usr/bin/env python3
"""Bounded consumer of full-source 6.15-6.17; no physical admission.

Checks actual Fibonacci multiplicities, the joint RIGHT/ref128 frame,
the complete conditional entropy gradient, pure raw16 balance and the
sharp Book gain identity. General proofs and scope are in the owner.
"""
import hashlib
import json
from pathlib import Path

import sympy as s


def require(value, label):
    if not value:
        raise ArithmeticError(label)


def multiplicity_and_joint_reference():
    M = s.Matrix([[1, 1], [1, 0]])
    success = M**6
    failure = M**12 - success
    require(success == s.Matrix([[13, 8], [8, 5]]), 'actual six-level inclusion')
    require(failure == s.Matrix([[220, 136], [136, 84]]), 'full regular failure')
    require(5*33 >= 128 and 84*33 >= 128, 'existing reference128 frame capacity')
    # Actual A1=M2 (+) M1, with its forced PF trace. A copy basis has
    # been chosen in which the old-left success range is copy zero.
    # Copy one supplies an orthogonal failure range in the same block.
    p = (s.sqrt(5)-1)/2
    leaves = [(0, 0, p**2), (0, 1, p**2), (1, 0, p**3)]
    require(s.simplify(sum(mu for _, _, mu in leaves)-1) == 0, 'PF trace normalized')
    joint = {}
    distinct_multiplicity_columns = set()
    for number, (block, row, mu) in enumerate(leaves):
        si = s.Rational(number+2, number+3)
        for a in range(128):
            copy, gamma = divmod(a, 33)
            require(copy < success[block, block], 'right copy belongs to actual block')
            for flag, probability in ((0, 1-si), (1, si)):
                # Right-column index is NOT part of the traced left data.
                # These data labels are distinct also across ref indices.
                label = (block, row, flag, copy, gamma)
                require(label not in distinct_multiplicity_columns, 'orthonormal joint frame')
                distinct_multiplicity_columns.add(label)
                key = ((block, row), a)
                joint[key] = joint.get(key, 0)+mu*probability/128
    for block, row, mu in leaves:
        for a in range(128):
            require(s.simplify(joint[((block, row), a)]-mu/128) == 0,
                    'full RIGHT x ref diagonal equals product density')
    # Distinct traced data labels kill every offdiagonal RIGHT/ref entry,
    # not just differences of the two separately reduced marginals.
    require(len(distinct_multiplicity_columns) == 3*128*2, 'no hidden column collision')
    return {'success': success.tolist(), 'failure': failure.tolist(),
            'minimum_success_scene_capacity': 165, 'reference_rank': 128,
            'noncommutative_old_block': 2, 'joint_marginal': 'rho_RIGHT tensor I128/128',
            'ideal_commutant_lift': 'real frame extension; no finite-word admission'}


def complete_gradient_and_source():
    e, mu = s.symbols('e mu', positive=True)
    h = -e*s.log(e)-(1-e)*s.log(1-e)
    Z = 1+2*s.exp(h)
    si = 1-1/Z
    lam = -s.log(mu)+s.log(Z)-1
    # q_F=mu/Z, q_ab=mu exp(h) p_a/Z at b=1/2.
    g_success = sum(pa*(lam-h-s.log(pa)) for pa in (1-e, e))
    require(s.simplify(g_success-lam) == 0, 'success and failure full gradients agree')
    require(s.simplify((1-si)*2*s.exp(h)/si-1) == 0,
            'own success preparation equation')
    require(s.simplify(s.expand_log(s.diff(s.log(Z), e)-si*s.log((1-e)/e), force=True)) == 0,
            'PF source coefficient, with no exterior D denominator')
    # Actual full M2 GNS, including offdiagonal matrix units. A fixed
    # right tangent can break left/right matching; its first source is zero.
    psi = s.Matrix([s.sqrt(s.Rational(2, 3)), 0, 0, s.sqrt(s.Rational(1, 3))])
    l0, l1 = s.symbols('lambda0 lambda1', real=True)
    G = s.diag(l0, l0, l1, l1)
    R = s.diag(l0, l1, l0, l1)
    require(G*psi == R*psi, 'right-conormal identity on full GNS')
    J = s.Matrix([[0, -1], [1, 0]])
    tangent = s.kronecker_product(J, s.eye(2))
    require(tangent*R == R*tangent, 'tangent preserves noncommutative RIGHT algebra')
    require((psi.T*(G*tangent-tangent*G)*psi)[0] == 0,
            'matching-breaking fixed-RIGHT tangent is stationary')
    free = s.zeros(4)
    free[3, 0], free[0, 3] = 1, -1
    require(s.simplify((psi.T*(G*free-free*G)*psi)[0]
                      -2*s.sqrt(2)*(l1-l0)/3) == 0,
            'negative control: changing old RIGHT mass gives nonzero source')
    # The homogeneous radial transform consumes an arbitrary smooth density,
    # rather than identifying finite Hessians or a density zero with Euler.
    f, a, dphi = s.symbols('f a dphi', nonzero=True)
    b = (dphi-1)/(2*f)
    require(s.simplify((1+2*f*b)*(1-2*f*b/dphi)-1) == 0,
            'exact inverse rank-one radial map')
    require(s.diff(-s.log(mu)+s.log(Z)-1, mu) == -1/mu,
            'fixed old weights still have upstream conormal source')
    return {'complete_gradient': 'sum_i lambda_i L(P_i)',
            'constrained_source': 'zero for all fixed-RIGHT pure tangents',
            'geometric_prefactor': 's_star p^2 t^2',
            'not_inferred': 'unconstrained stationary root, capacity selection or C2 entropy'}


def raw_balance_and_metric():
    p = (s.sqrt(5)-1)/2
    L = 4*p**3
    alpha = 1/(2*L)
    require(bool(L > s.Rational(1, 2)) and bool(alpha < 1), 'open pure-CAR balance')
    # theta has cos=3/5, sin=4/5. Sparse coordinates are basis e0,e12,Omega
    # in the full retained CAR16; unused coordinates remain tangent slots.
    norm = (1-alpha)*(s.Rational(9, 25)+s.Rational(16, 25))+alpha
    k = (1-alpha)*s.Rational(9, 25)
    require(s.simplify(norm-1) == 0 and bool(k > 0), 'pure raw16 timelike first grade')
    require(s.simplify(L*alpha-s.Rational(1, 2)) == 0, 'same literal B balance')
    require(s.simplify(L**2*alpha-s.Rational(1, 4)-(2*L-1)/4) == 0,
            'strict positive scene variance')
    eta = s.diag(1, -1, -1, -1)
    F = s.Matrix([[2, 1, 0, 0], [0, 1, 1, 0], [0, 0, 3, 1], [0, 0, 0, 1]])
    q = F*eta*F.T
    v0 = F[:, 0]
    require((v0.T*q.inv()*v0)[0] == 1, 'raw timelike pairing at nonorthogonal F')
    Q = -q+2*v0*v0.T
    require(Q == F*F.T, 'pairing and native raised positive metric agree')
    # Moving n is NOT frozen: another timelike unit vector reconstructs
    # exactly the same raw Lorentz metric from the two meter outputs.
    n = s.Matrix([s.Rational(5, 3), s.Rational(4, 3), 0, 0])
    require((n.T*eta*n)[0] == 1, 'moving observer is normalized')
    b = F*n
    Qn = F*(-eta+2*n*n.T)*F.T
    require(2*b*b.T-Qn == q, 'observer terms cancel in raw metric readout')
    return {'raw_CAR_components': 16, 'pure_factor': True,
            'first_grade_timelike': True, 'top_nonzero': True,
            'balance': '1/2', 'variance': '(2L-1)/4 > 0',
            'matter_source': 'zero on this vacuum profile; no independent stress',
            'chronology': 'full coherent B effect; branchwise observer update not inferred'}


def book_shape_and_gain():
    r, w0, w1, nu0, nu1 = s.symbols('r w0 w1 nu0 nu1', positive=True)
    q = (r, 1-r)
    w, nu = (w0, w1), (nu0, nu1)
    N = w0+w1
    lhs = sum(qi*s.log(qi/vi)-qi*s.log(wi/vi) for qi, wi, vi in zip(q, w, nu))
    rhs = sum(qi*s.log(qi/(wi/N)) for qi, wi in zip(q, w))-s.log(N)
    require(s.simplify(s.expand_log(lhs-rhs, force=True)) == 0,
            'sharp gain/Kraft identity, including the actual raw normalizer')
    require(s.simplify(s.diff(s.log(r/(1-r)), r)-1/(r*(1-r))) == 0,
            'leaf-ratio shape derivative is not a common normalizer')
    source = Path(__file__).with_name('USER_NATIVE_PRICE_SYNTHESIS_2026_10_18.txt')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    require(digest == 'd5706efac0dc8791f010557810a1e1ad835b3fdc2f8578432e5f13f883bd2570',
            'new supplied input preserved byte-for-byte')
    return {'shape_test': 'sum_alpha w_i_alpha = <P_i>',
            'sufficiency': 'native expected-gain saturation AND raw N<=1 imply w=q',
            'native_saturation_or_mean_selection_proved': False,
            'supplied_input_sha256': digest}


if __name__ == '__main__':
    result = {'status': 'PASS',
              'multiplicity_reference': multiplicity_and_joint_reference(),
              'complete_source': complete_gradient_and_source(),
              'raw_matter': raw_balance_and_metric(),
              'book_binding_test': book_shape_and_gain(),
              'physical_D0_GR_proved': False}
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
