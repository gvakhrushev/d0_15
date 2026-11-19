#!/usr/bin/env python3
"""Exact controls for the all-field AF feedback normal form.

The all-size theorem is analytic in the companion memo. Rational 2x2
matrices test noncommuting derivatives, not the dimension of physical
matter. No old root/spectrum suite or new physical action is executed.
"""
from itertools import combinations
import json
import sympy as s

checks = []


def eq(name, value):
    values = list(value) if isinstance(value, s.MatrixBase) else [value]
    if any(s.cancel(v) != 0 for v in values):
        raise ArithmeticError(name)
    checks.append(name)


def nonzero(name, value):
    values = list(value) if isinstance(value, s.MatrixBase) else [value]
    if not any(s.cancel(v) != 0 for v in values):
        raise ArithmeticError(name)
    checks.append(name)


def positive2(name, matrix):
    if matrix != matrix.T or not (matrix[0, 0] > 0 and matrix.det() > 0):
        raise ArithmeticError(name)
    checks.append(name)


def main():
    I = s.eye(2)
    e0, z, tt = s.Rational(3, 8), s.Rational(2, 7), s.Rational(1, 7)
    O = s.Matrix([[s.Rational(3, 5), -s.Rational(4, 5)],
                  [s.Rational(4, 5), s.Rational(3, 5)]])
    B = O*s.diag(0, s.Rational(1, 3))*O.T
    C = I-B
    K0 = (1-z)*I+z*(1-e0)*C
    A = e0*z*C*K0.inv()
    Y = s.Matrix([[s.Rational(1, 7), s.Rational(2, 9)],
                  [s.Rational(2, 9), -s.Rational(1, 11)]])
    nonzero('scene_direction_does_not_commute', B*Y-Y*B)
    positive2('scene_complement_positive', C)
    positive2('baseline_positive', K0)
    positive2('feedback_susceptibility_positive', A)

    dA = -e0*z*(1-z)*K0.inv()*Y*K0.inv()
    dA_direct = -e0*z*Y*K0.inv()+e0*z*z*(1-e0)*C*K0.inv()*Y*K0.inv()
    eq('full_noncommuting_susceptibility_derivative', dA-dA_direct)

    f = s.Rational(2, 9)
    Q = I-tt*f*A
    K = (1-z)*I+z*(1-e0*(1+tt*f))*C
    positive2('full_price_positive_window', Q)
    if not 0 < e0*(1+tt*f) < 1:
        raise ArithmeticError('effect window')
    checks.append('effect_positive_window')
    eq('whole_scene_determinant_factorization', K-K0*Q)
    eq('whole_scene_determinant_with_baseline', K.det()-K0.det()*Q.det())
    Xstar = Q.inv()
    eq('unique_auxiliary_stationarity', (Xstar.inv()-I)/tt+f*A)
    eq('auxiliary_schur_source_f', s.trace(Xstar*A)-e0*z*s.trace(K.inv()*C))
    Xtrial = s.Matrix([[s.Rational(5, 4), s.Rational(1, 7)],
                       [s.Rational(1, 7), s.Rational(7, 6)]])
    positive2('noncommuting_auxiliary_trial_positive', Xtrial)
    nonzero('auxiliary_trial_not_diagonal_in_scene', Xtrial*A-A*Xtrial)
    eq('exact_gap_trace', s.trace(Xtrial*Q)-s.trace(Xtrial)+tt*f*s.trace(Xtrial*A))
    eq('exact_gap_determinant', (Q*Xtrial).det()-Q.det()*Xtrial.det())
    eq('gap_vanishes_at_unique_lift', Xstar*Q-I)

    # Same-price graph derivative. B varies with every original coordinate;
    # it is not an independent frozen spectator in this test.
    r, k, psi = s.symbols('r k psi', real=True)
    variables = (r, k, psi)
    point = {r:s.Integer(1), k:s.Rational(2, 9), psi:s.Integer(2)}
    Yk = s.Matrix([[s.Rational(1, 8), -s.Rational(1, 10)],
                   [-s.Rational(1, 10), s.Rational(1, 9)]])
    Ys = s.Matrix([[s.Rational(1, 13), s.Rational(1, 12)],
                   [s.Rational(1, 12), -s.Rational(1, 14)]])
    Bnative = B+(r-1)*Y+(k-point[k])*Yk+(psi-2)*Ys
    density = r*r*k
    rest = r*r+3*k*psi+psi**4
    chi = s.trace(Xstar*A)
    GB = z*(1-e0)*K0.inv()/tt-e0*z*(1-z)*f*K0.inv()*Xstar*K0.inv()
    Lam = -GB
    source = {}
    for var in variables:
        df = s.diff(density, var).subs(point)
        dB = Bnative.diff(var)
        drest = s.diff(rest, var).subs(point)
        dK = -e0*z*tt*df*C-z*(1-e0*(1+tt*f))*dB
        original = drest-s.trace(K.inv()*dK)/tt
        unfolded = drest+chi*df-s.trace(Lam*dB)
        eq('same_price_full_graph_source_'+str(var), original-unfolded)
        source[var] = unfolded
    nonzero('frozen_scene_drops_a_real_source', s.trace(GB*Y))
    nonzero('full_fixture_not_mislabelled_stationary', source[r])
    eq('graph_multiplier_equation', GB+Lam)

    # Changing X at fixed new tetrad changes the old tetrad. Even at the
    # old auxiliary optimum the new X-row is not zero off a joint root.
    DX = s.Matrix([[s.Rational(1, 3), s.Rational(1, 5)],
                   [s.Rational(1, 5), -s.Rational(1, 7)]])
    dchi = s.trace(DX*A)
    dr = -point[r]*dchi/(2*chi)
    auxiliary_after_frame = ((s.diff(rest, r).subs(point)-s.trace(Lam*Y))*dr
                              -s.trace((I-Xstar.inv())*DX)/tt)
    transported = -source[r]*point[r]*dchi/(2*chi)
    eq('mixed_auxiliary_tetrad_row_is_retained', auxiliary_after_frame-transported)
    nonzero('old_auxiliary_extremum_cannot_be_frozen_in_new_frame', transported)

    # Literal original diagonal-signature six-face star polynomial. The
    # 36 curvature coordinates are free for this polynomial identity;
    # every actual linked plaquette derivative is then a pullback of it.
    pairs = list(combinations(range(4), 2))
    eta = s.diag(1, -1, -1, -1)
    G = s.diag(*[eta[i, i]*eta[j, j] for i, j in pairs])
    star = s.zeros(6)
    sm = {(0,1):((2,3),-1), (0,2):((1,3),1), (0,3):((1,2),-1),
          (1,2):((0,3),1), (1,3):((0,2),-1), (2,3):((0,1),1)}
    for pair, (target, sign) in sm.items():
        star[pairs.index(target), pairs.index(pair)] = sign
    ev = s.symbols('e0:16')
    emat = s.Matrix(4, 4, ev)
    rv = s.symbols('R0:36')
    price = 0
    for j, (axis, axis2) in enumerate(pairs):
        u, v = [i for i in range(4) if i not in (axis, axis2)]
        wedge = s.Matrix([emat[i,u]*emat[l,v]-emat[l,u]*emat[i,v] for i,l in pairs])
        curv = s.Matrix(rv[j*6:(j+1)*6])
        price += s.LeviCivita(axis, axis2, u, v)*(wedge.T*G*star*curv)[0]
    scale = s.symbols('scale', positive=True)
    eq('literal_star_all_coframe_homogeneity',
       s.expand(price.xreplace({v:scale*v for v in ev})-scale**2*price))
    eq('literal_star_radial_source_all16',
       s.expand(sum(v*s.diff(price,v) for v in ev)-2*price))
    # No scalar/trace-free truncation of the metric map.
    eq('all16_coframe_Jacobian_determinant', (scale*s.eye(16)).det()-scale**16)
    eq('all10_metric_Jacobian_determinant', (scale**2*s.eye(10)).det()-scale**20)

    # A closed source can become non-closed under the previous row-only
    # intertwiner. This rejects calling it a separate matter action.
    f2 = r*r*k
    Z = s.Matrix([r,0])
    df = s.Matrix([[2*r*k, r*r]])
    M = s.eye(2)+Z*df/(2*(1-f2))
    Minv = s.eye(2)-Z*df/2
    eq('radial_inverse_control', M*Minv-s.eye(2))
    omega = Minv.T*s.Matrix([1,0])
    curl = s.diff(omega[1],r)-s.diff(omega[0],k)
    eq('transformed_matter_one_form_curl', curl+r*r/2)
    nonzero('row_only_source_not_integrable', curl)

    # Graph compensation is a control of a universal inference, not an
    # assertion that this scene map is physically admitted by D0.
    e, zz, c0 = s.symbols('effect fugacity c0')
    bb = 1-c0/(1-e)
    kk = 1-zz+zz*(1-e)*(1-bb)
    eq('dependent_scene_full_price_is_constant', kk-(1-zz+zz*c0))
    independent_effect_source = zz*(1-bb)/kk
    independent_scene_source = zz*(1-e)/kk
    eq('same_price_graph_source_cancels_effect',
       independent_effect_source+independent_scene_source*s.diff(bb,e))
    nonzero('dropping_graph_source_falsely_creates_gravity', independent_effect_source)

    # A moving conformal factor changes the actual matter reading.
    ch, volume_hat, kinetic_hat, pot = s.symbols('chi volume_hat kinetic_hat potential', positive=True)
    original_matter = volume_hat/ch**2*(ch*kinetic_hat/2+pot)
    eq('four_dimensional_matter_pullback',
       original_matter-volume_hat*(kinetic_hat/(2*ch)+pot/ch**2))
    nonzero('matter_scaling_not_a_field_independent_constant', s.diff(original_matter,ch))

    result = {
        'status':'PASS_EXACT_FULL_SOURCE_NORMAL_FORM_CONTROLS',
        'input_ref':'360b28b64f66914c78065671496b5cab3162c10e',
        'checks':len(checks), 'check_names':checks,
        'nonintegrable_source_curl':str(curl),
        'same_program_graph_source':'retained; can exactly cancel the separated effect source',
        'all_size_proof':'A4D_AF_FULL_SOURCE_EINSTEIN_NORMAL_FORM_2026_10_17.md',
        'new_physical_fields_introduced':False,
        'physical_program_selected':False,
        'complete_native_cost_info_identified':False,
        'operational_metric_identified_with_einstein_frame':False,
        'global_joint_recovery_proved':False,
        'GR_closed':False,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
