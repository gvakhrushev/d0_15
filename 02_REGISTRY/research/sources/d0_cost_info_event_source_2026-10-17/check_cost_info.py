#!/usr/bin/env python3
"""Finite Cost--Info synthesis for D0 #334.

No original certificate is executed or modified. The 64 Julia/Walsh row
formula and ACDB CAR order are reconstructed from the pinned native owner.
Exact finite controls support, but do not replace, the all-size proofs.
No claim of physical programme admission or of a complete GR derivation.
"""
from __future__ import annotations
import itertools
import json
from math import comb
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

REF = 'd1b76082948d5b59961b7068e1ba2c70187efb7f'
CHECKS: list[str] = []
DETAIL: dict = {}


def require(name: str, condition: bool) -> None:
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def equal(name: str, left, right=0) -> None:
    if isinstance(left, np.ndarray):
        require(name, np.array_equal(left, right))
        return
    d = left-right
    entries = list(d) if isinstance(d, sp.MatrixBase) else [d]
    require(name, all(sp.simplify(v) == 0 for v in entries))


def creators() -> list[np.ndarray]:
    order = (0, 2, 3, 1)  # actual ACDB sign order
    out = []
    for role in range(4):
        c = np.zeros((16, 16), dtype=np.int64)
        preceding = order[:order.index(role)]
        for mask in range(16):
            if not ((mask >> role) & 1):
                sign = (-1)**sum((mask >> r) & 1 for r in preceding)
                c[mask | (1 << role), mask] = sign
        out.append(c)
    return out


def native_rows_integer(C: list[np.ndarray], phases: tuple[int, ...]):
    """Exact native _native_rows at nu=3/5,b=4/5, common denominator 160.

    Tops per role: duplicated (P,L),(P*,R),(-C,-L),(-C*,-R).
    The diagonal complement roots are exact, not a spectral approximation.
    """
    eye = np.eye(16, dtype=np.int64)
    tops = []
    for r, c in enumerate(C):
        number = c @ c.T
        L = 5*eye-number
        R = 4*eye+number
        P = 3*phases[r]*c
        for pair in ((P, L), (P.T, R), (-3*c, -L), (-3*c.T, -R)):
            tops.extend((pair, pair))
    rows = []
    for label in range(32):
        for coefficient in range(2):
            row = sum(((-1)**((label & j).bit_count()) * tops[j][coefficient]
                       for j in range(32)), np.zeros((16, 16), dtype=np.int64))
            rows.append(row)
    return rows


def native_controls() -> None:
    C = creators()
    eye = np.eye(16, dtype=np.int64)
    zero = np.zeros((16, 16), dtype=np.int64)
    for r in range(4):
        for s in range(4):
            if not (np.array_equal(C[r]@C[s]+C[s]@C[r], zero) and
                    np.array_equal(C[r]@C[s].T+C[s].T@C[r], eye if r == s else zero)):
                raise ArithmeticError('full16_ACDB_CAR')
    CHECKS.append('full16_ACDB_CAR')
    d = 160
    den = d*d
    details = []
    for index, phases in enumerate(itertools.product((1,-1), repeat=4)):
        rows = native_rows_integer(C, phases)
        equal(f'native_rows_complete_momentum_{index}',
              sum((N@N.T for N in rows), zero.copy()), den*eye)
        A = rows[0]
        # A = nu/16 sum_r (phase_r-1)(c_r+c_r*)
        expected_A = sum((6*(phases[r]-1)*(C[r]+C[r].T)
                          for r in range(4)), zero.copy())
        # denominator 160: (3/5)/16 *160 = 6
        equal(f'literal_A_equals_hD_over16_{index}', A, expected_A)
        Ws = [(den*eye if k == 0 else zero)-2*N.T@A for k,N in enumerate(rows)]
        equal(f'whole_reflection_column_{index}',
              sum((W.T@W for W in Ws), zero.copy()), den*den*eye)
        # K0_k = W_k + p*(delta_k0 I-W_k); K1_k = ap*(W_k-delta_k0 I)
        # scaled by den. Reduce a^2=p,p^2=1-p,p^3=2p-1 exactly.
        effect_const, effect_p, port1 = zero.copy(), zero.copy(), zero.copy()
        for k,W in enumerate(Ws):
            R = (den*eye if k == 0 else zero)-W
            effect_const += W.T@W
            effect_p += W.T@R+R.T@W+R.T@R
            port1 += R.T@R
        equal(f'all128_complete_constant_coefficient_{index}', effect_const, den*den*eye)
        equal(f'all128_complete_golden_coefficient_{index}', effect_p, zero)
        equal(f'all_labels_port1_effect_{index}', port1, 4*den*(A.T@A))
        r = phases.count(-1)
        equal(f'whole16_D_square_momentum_{index}', A.T@A, 144*r*eye)
        if r == 0:
            equal('dark_entire16_blank_amplitude', Ws[0], den*eye)
            require('dark_all127_actual_nonblank_amplitudes_zero',
                    all(np.array_equal(W, zero) for W in Ws[1:]))
            # Full128 reference columns need not be selected: E=0 as an operator.
            require('dark_full128_reference_extension',
                    np.array_equal(np.kron(A, np.eye(128, dtype=np.int64)),
                                   np.zeros((2048,2048), dtype=np.int64)))
        details.append({'phases': phases, 'positive_roles': r})
    DETAIL['native'] = {'site_count':16, 'forms_per_site':16, 'reference':128,
                        'outcomes_per_round':128, 'literal_row_denominator':160,
                        'momenta':details}

    p = (sp.sqrt(5)-1)/2
    nu = sp.Rational(3,5)
    L = 2
    alpha = p**2/512
    n = 512
    beta = 2*n*alpha
    z = sp.Rational(1,2**20)
    M = 128
    equal('actual_fixed_beta', beta, 2*p**2)
    require('beta_strictly_less_one', bool(beta < 1))
    require('exact_complete_price_source_sign_bound', bool(M*256*z/(1-z) < 1))
    DETAIL['native']['spectral_source_ratio_upper_bound'] = str(M*256*z/(1-z))

    mp.mp.dps = 90
    pp = (mp.sqrt(5)-1)/2
    aa = pp**2/512
    bb = 2*pp**2
    vv = mp.mpf(3)/5
    zz = mp.mpf(1)/2**20
    weights = [16*comb(4,r) for r in range(5)]
    B = [1-aa*16*vv*vv*r for r in range(5)]
    lam_prime = [32*vv*r for r in range(5)]
    Z = sum(w*b**1024 for w,b in zip(weights,B))
    dH = -sum(w*b**1023*lp for w,b,lp in zip(weights,B,lam_prime))/Z
    dJ = M*bb*zz*sum(w*b**1023*lp/(1-zz+zz*b**1024)
                    for w,b,lp in zip(weights,B,lam_prime))
    exit_mass = 1-B[1]**1024
    require('numerical_full_price_source_matches_exact_negative_sign', dH+dJ < 0)
    DETAIL['native']['diagnostic_full_price_derivative'] = mp.nstr(dH+dJ,55)
    DETAIL['native']['diagnostic_dH'] = mp.nstr(dH,40)
    DETAIL['native']['diagnostic_dJ'] = mp.nstr(dJ,40)
    DETAIL['native']['exact_history_exit_mass'] = '1-(1-9*p^2/800)^1024'
    DETAIL['native']['diagnostic_history_exit_mass'] = mp.nstr(exit_mass,55)
    # Denominator above: nu^2/32 = 9/800.
    equal('history_exit_base_exact', 1-alpha*16*nu**2, 1-sp.Rational(9,800)*p**2)


def likelihood_controls() -> None:
    ell = sp.Symbol('ell', positive=True)
    N, q, mu = sp.symbols('N q mu', positive=True)
    C = -sp.log(mu)/ell
    I = (sp.log(q)-sp.log(mu)+sp.log(N))/ell
    equal('full_code_cancelled_before_variation', C-I, (-sp.log(q)-sp.log(N))/ell)
    equal('moving_code_source_cancels', sp.diff(C-I,mu),0)
    equal('raw_normalizer_source_retained', sp.diff(C-I,N),-1/(ell*N))
    c1,c2,u,v = sp.symbols('c1 c2 u v',real=True)
    x = sp.Symbol('x',positive=True)
    # Finite cut completion must use total probability, not conditional success only.
    H = -x*sp.log(x)-(1-x)*sp.log(1-x)
    equal('binary_entropy_source',sp.diff(H,x),sp.log(1-x)-sp.log(x))
    equal('branch_surprisal_source',sp.diff(-sp.log(x),x),-1/x)
    require('branch_and_average_are_distinct_sources',
            sp.simplify(sp.diff(H+sp.log(x),x).subs(x,sp.Rational(1,3))) != 0)

    t,A,r = sp.symbols('t A r',positive=True)
    q0 = 1-A*t*t
    q1 = A*r*t*t
    q2 = A*(1-r)*t*t
    require('probability_birth_normalized',sp.expand(q0+q1+q2)==1)
    entropy = -sum(qq*sp.log(qq) for qq in (q0,q1,q2))
    limit = sp.limit(entropy/(-t*t*sp.log(t*t)),t,0,dir='+')
    equal('full_pointer_rank_birth_coefficient',limit,A)
    equal('entropy_all_first_amplitude_rows_zero',sp.limit(sp.diff(entropy,t),t,0,dir='+'),0)
    require('entropy_no_finite_vacuum_Hessian',sp.limit(sp.diff(entropy,t,2),t,0,dir='+')==sp.oo)
    # Full fine law and coarse law: entropy conditional is retained, not silently free energy.
    u = sp.Symbol('u',positive=True)
    conditional = -r*sp.log(r)-(1-r)*sp.log(1-r)
    equal('fine_coarse_entropy_exact',sp.expand_log(entropy-(-q0*sp.log(q0)-A*t*t*sp.log(A*t*t))
                                                  -A*t*t*conditional,force=True),0)


def determinant_fixture(d: int):
    eye=sp.eye(d)
    c=[sp.Rational(3,5),sp.Rational(5,13),sp.Rational(8,17)][:d]
    s=[sp.Rational(4,5),sp.Rational(12,13),sp.Rational(15,17)][:d]
    vv=sp.Matrix([1,2,2][:d])
    O=eye-2*vv*vv.T/(vv.T*vv)[0]
    C=sp.diag(*c); S=sp.diag(*s)
    U=sp.BlockMatrix([[C,-S],[S,C]]).as_explicit()*sp.diag(O,O)
    J=sp.eye(2*d)[:,:d]
    P=J*J.T
    Q=sp.eye(2*d)-P
    z=sp.Rational(16,25)
    M0=(P+sp.Rational(3,5)*Q)*U*J
    M1=sp.Rational(4,5)*Q*U*J
    F=J.T*U.T*Q*U*J
    gram=eye-z*F
    equal(f'actual_one_particle_unitarity_d{d}',U.T*U,sp.eye(2*d))
    equal(f'complete_flag_isometry_d{d}',M0.T*M0+M1.T*M1,eye)
    equal(f'no_flag_gram_exact_d{d}',M0.T*M0,gram)
    minors0=sum((M0[list(ix),:].det()**2 for ix in itertools.combinations(range(2*d),d)),sp.S.Zero)
    V=M0.col_join(M1)
    allmass=sum((V[list(ix),:].det()**2 for ix in itertools.combinations(range(4*d),d)),sp.S.Zero)
    equal(f'fermionic_all_success_probability_d{d}',minors0,gram.det())
    equal(f'all_failure_sectors_retained_d{d}',allmass,1)
    require(f'discarding_exchange_terms_is_rejected_d{d}',
            sp.prod(gram[i,i] for i in range(d)) != gram.det())
    equal(f'basis_catalogue_independence_d{d}',(O.T*gram*O).det(),gram.det())
    DETAIL[f'determinant_d{d}']={'success_probability':str(minors0),
                                'complement_probability':str(1-minors0),
                                'full_exterior_output_dimension':comb(4*d,d),
                                'particle_count':d}
    return U,J,P,Q,F,gram,z


def determinant_controls() -> None:
    for d in (2,3):
        values=determinant_fixture(d)
        if d!=2: continue
        U,J,P,Q,F,gram,z=values
        X=sp.zeros(4); X[0,2]=1; X[2,0]=-1; X[0,3]=1; X[3,0]=-1
        Udot=X*U
        Fdot=J.T*(Udot.T*Q*U+U.T*Q*Udot)*J
        require('real_noncommuting_feedback_source_direction',F*Fdot-Fdot*F!=sp.zeros(2))
        r=sp.Symbol('r',real=True)
        explicit=-sp.diff((gram-r*z*Fdot).det(),r).subs(r,0)/gram.det()
        equal('same_branch_full_logdet_source',explicit,z*sp.trace(gram.inv()*Fdot))
        # Moving input/output cut: all frame and Q derivatives retained.
        T=sp.zeros(4); T[0,3]=1; T[3,0]=-1; T[0,2]=1; T[2,0]=-1
        Jdot=T*J
        Qdot=-Jdot*J.T-J*Jdot.T
        direct=(Jdot.T*U.T*Q*U*J+J.T*U.T*Q*U*Jdot+J.T*U.T*Qdot*U*J)
        Jr=J+r*Jdot
        full=Jr.T*U.T*(sp.eye(4)-Jr*Jr.T)*U*Jr
        equal('moving_cut_complete_derivative',full.diff(r).subs(r,0),direct)
        require('frozen_cut_source_is_not_full_source',sp.trace(gram.inv()*J.T*U.T*Qdot*U*J)!=0)
    f1,f2,zz=sp.symbols('f1 f2 zz',real=True)
    equal('independent_sector_multiplicativity',(sp.eye(2)-zz*sp.diag(f1,f2)).det(),(1-zz*f1)*(1-zz*f2))


def main() -> None:
    likelihood_controls()
    determinant_controls()
    native_controls()
    result={'status':'PASS_SCOPED_FINITE_IDENTITIES','checks':len(CHECKS),'check_names':CHECKS,
            'source_ref':REF,'details':DETAIL,
            'full_Cost_Info_native_selection_proved':False,
            'new_collective_fermion_preparation_physical_admission_proved':False,
            'entropy_open_record_vacuum_sector':'exactly_zero_if_admitted',
            'GR_derived':False,'original_fixed_g_tau_raw_terminal_closed':False}
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
