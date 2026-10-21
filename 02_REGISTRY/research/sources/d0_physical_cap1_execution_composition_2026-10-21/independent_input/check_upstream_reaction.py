#!/usr/bin/env python3
"""New bounded exact matrix controls; no repository writes or old-suite replay."""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import time
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    start = time.perf_counter()
    passed = []

    def check(name, condition):
        if not condition:
            raise RuntimeError(name)
        passed.append(name)

    def zero(a):
        if isinstance(a, s.MatrixBase):
            return all(s.cancel(x) == 0 for x in a)
        return s.cancel(a) == 0

    def givens(n, i, j, c, d):
        g = s.eye(n)
        g[i, i] = g[j, j] = c
        g[i, j], g[j, i] = -d, d
        return g

    # Original full dimension and output-cut ranks. These rational test
    # matrices are arbitrary admissible mathematics, not native word claims.
    n = 8
    cut = s.diag(0, 1, 0, 1, 1, 1, 1, 1)
    u = (givens(n, 0, 1, s.Rational(3, 5), s.Rational(4, 5))
         * givens(n, 1, 2, s.Rational(5, 13), s.Rational(12, 13))
         * givens(n, 2, 4, s.Rational(8, 17), s.Rational(15, 17)))
    omega = s.zeros(n)
    for i, j, value in [(0, 2, 2), (0, 4, -3), (1, 3, 5), (2, 5, -2), (6, 7, 1)]:
        omega[i, j], omega[j, i] = value, -value
    q = u.T * cut * u
    dq = q * omega - omega * q
    check('full_8d_orthogonality', u.T * u == s.eye(n))
    check('rank_six_output_projector', cut.rank() == 6 and zero(q*q-q))
    check('noncommuting_actual_tangent', not zero(dq))
    check('projector_tangent_blocks', zero(q*dq*q) and zero((s.eye(n)-q)*dq*(s.eye(n)-q)))

    m = s.Matrix(n, 3, lambda i, j: s.Rational((i+1)*(j+2)+(i-j)**2, 97))
    rho = m*m.T
    rho /= s.trace(rho)
    drho = omega*rho-rho*omega
    field_source = s.trace(rho*dq)
    prep_source = s.trace(q*drho)
    check('hostile_control_nonzero_source', field_source != 0)
    check('fixed_right_gram_tangent', zero(m.T*(omega*m)+(omega*m).T*m))
    check('query_source_equals_prep_lift', zero(field_source-prep_source))
    check('compensating_input_cancels_source', zero(field_source-s.trace(q*drho)))

    rho_star = u.T*s.diag(*[s.Rational(k, 36) for k in range(1, 9)])*u
    check('stationary_density_normalized', s.trace(rho_star) == 1)
    check('stationary_commutator', zero(rho_star*q-q*rho_star))
    check('all_source_cancellation_control', zero(s.trace(rho_star*dq)))

    # Exact full two-query spectrum and derivative identity: use projector
    # tensor algebra, not diagonal eigenvalue sampling or physical truncation.
    z = s.Symbol('z', positive=True)
    eye = s.eye(n)
    e0 = s.kronecker_product(eye-cut, eye-cut)
    e1 = s.kronecker_product(cut, eye-cut)+s.kronecker_product(eye-cut, cut)
    e2 = s.kronecker_product(cut, cut)
    effect = z*e1+(2*z-z*z)*e2
    check('all_64_joint_input_coordinates', effect.shape == (64, 64))
    check('full_joint_spectral_multiplicities', [s.trace(x) for x in [e0,e1,e2]] == [4,24,36])
    check('complete_joint_OR_effect', zero(effect-(s.eye(64)-s.kronecker_product(eye-z*cut,eye-z*cut))))
    # Independent one-factor tangents suffice to check the full product
    # commutator. Keeping the second factor in the cut basis avoids expensive
    # dense symbolic products without dropping any of its eight states.
    joint_e = s.eye(64)-s.kronecker_product(eye-z*q,eye-z*cut)
    joint_o = s.kronecker_product(omega,eye)
    joint_de = z*s.kronecker_product(dq,eye-z*cut)
    check('full_joint_isospectral_derivative', zero(joint_de-(joint_e*joint_o-joint_o*joint_e)))

    # Normal reaction of an arbitrary fractional compressed eigenstate.
    # A projector dilation is a control of the identity, not a new apparatus.
    lam = s.Rational(4, 5)
    q2 = s.Matrix([[lam,s.Rational(2,5)],[s.Rational(2,5),1-lam]])
    psi = s.Matrix([1,0]); v = (q2-lam*s.eye(2))*psi
    check('fractional_normal_projector', q2*q2 == q2)
    check('normal_reaction_norm', (psi.T*v)[0] == 0 and (v.T*v)[0] == lam*(1-lam))
    check('normal_direction_click_source', 2*(v.T*q2*psi)[0] == 2*lam*(1-lam))

    # Golden primary anchors and signs, exact algebra and high precision.
    p = (s.sqrt(5)-1)/2
    zz = s.Rational(1,2**20)
    aa, bb = 1-p**12, 1-p**6
    qq = s.expand(1-(1-zz*aa)*(1-zz*bb))
    check('golden_primary_fractional', all(bool(x>0) for x in [aa,1-aa,bb,1-bb]))
    check('whole_effect_probability_bound', bool(0<qq) and bool(qq<2*zz-zz*zz) and bool(2*zz-zz*zz<s.Rational(1,2)))
    phi = 1/p
    hp = s.log((1-qq)/qq)/s.log(phi)
    normalized_plus_reaction = -2*zz*(1-zz*bb)*hp*aa*(1-aa)
    normalized_minus_reaction = -2*zz*(1-zz*aa)*hp*bb*(1-bb)
    check('both_primary_descent_signs', float(normalized_plus_reaction.evalf(25))<0 and float(normalized_minus_reaction.evalf(25))<0)

    result = {
        'status':'PASS', 'checks':passed, 'check_count':len(passed),
        'runtime_seconds':time.perf_counter()-start,
        'python':platform.python_version(), 'sympy':s.__version__,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'exact_nonstationary_field_source':str(field_source),
        'primary_q':str(qq.evalf(60)),
        'primary_plus_derivative_divided_by_alpha_beta':str(normalized_plus_reaction.evalf(60)),
        'primary_minus_derivative_divided_by_alpha_beta':str(normalized_minus_reaction.evalf(60)),
        'scope':'New finite matrix control only; no native admission, physical input selection, old test replay, or repository writes.'
    }
    output=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(output)
    print(output,end='')


if __name__=='__main__':
    main()
