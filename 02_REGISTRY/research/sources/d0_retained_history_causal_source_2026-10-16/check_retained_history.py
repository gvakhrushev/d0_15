#!/usr/bin/env python3
"""Exact retained Julia-label/first-exit and full16 cone identities.

Only frozen creator definitions are executed. This does not execute old
checkers, add a price, or establish physical admission of the matrix gates.
"""
from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s

ROOT = Path(__file__).resolve().parents[4]
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS = {
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    '02_REGISTRY/research/sources/d0_cone_matter_corrector_2026-10-16/check_cone_matter_corrector.py':
        '7bbf1589f3a32af381036df64f76d720ce14a9f2e502b3a1a6f43f5b5e776d58',
    '02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md':
        'a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915',
    '02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md':
        'f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c',
}


def _creators(repo):
    tree = ast.parse((repo / CURVED).read_text())
    nodes = [node for node in tree.body if
             (isinstance(node, ast.FunctionDef) and node.name == 'creator') or
             (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name)
              and t.id == 'EXTERIOR_ORDER' for t in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('retained_history:creator_definition_nodes')
    scope = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CURVED, 'exec'), scope)
    return [scope['creator'](j) for j in range(4)], scope['EXTERIOR_ORDER']


def first_exit_effect(B, effect, rounds):
    """Actual disjoint event: blank j rounds, then effect, later unrestricted."""
    if not isinstance(rounds, int) or rounds < 0:
        raise ValueError('rounds must be a nonnegative integer')
    total, power = s.zeros(B.rows), s.eye(B.rows)
    for _ in range(rounds):
        total += power.H * effect * power
        power = B * power
    return total


def normalized_source(rho, drho, effect, deffect):
    """Full unnormalized preparation and moving effect, including dTr rho."""
    normalizer = s.trace(rho)
    if normalizer == 0:
        raise ValueError('zero preparation normalizer')
    value = s.trace(rho * effect) / normalizer
    return (s.trace(drho * effect + rho * deffect)
            - value * s.trace(drho)) / normalizer


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('retained_history:' + name)
        checks.append(name)

    def eq(actual, expected, name, reduce=None):
        values = list(actual - expected) if isinstance(actual, s.MatrixBase) else [actual - expected]
        f = s.expand if reduce is None else reduce
        require(all(f(x) == 0 for x in values), name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    C, order = _creators(repo)
    I, O = s.eye(16), s.zeros(16)
    require(order == (0, 2, 3, 1), 'literal_ACDB_all16_order')
    require(all(C[i]*C[j].H+C[j].H*C[i] == (I if i == j else O)
                for i in range(4) for j in range(4)), 'full16_CAR')

    def lift(M):
        return sum((M[i,j]*C[i]*C[j].H for i in range(4) for j in range(4)), O.copy())

    def elementary(i, j):
        M = s.zeros(4)
        M[i,j] = 1
        return M

    def rotation(i, j):
        generator = lift(elementary(i,j)-elementary(j,i))
        return I+s.Rational(4,5)*generator+s.Rational(2,5)*generator**2

    # Noncommuting, nonnormal full16 actual creator/return fixture. Identity
    # bare shifts suffice for this local compiler/order test, not for the cone.
    scale, defect = s.Rational(3,5), s.Rational(4,5)
    returns = [rotation(1,2), rotation(2,3), rotation(1,3), I]
    cs = [scale*c for c in C]
    xs = [cs[r]*returns[r] for r in range(4)]

    def julia(X):
        left_root = I+(defect-1)*X*X.H/scale**2
        right_root = I+(defect-1)*X.H*X/scale**2
        return s.BlockMatrix([[X,left_root],[right_root,-X.H]]).as_explicit()

    words = []
    for r in range(4):
        require(returns[r].H*returns[r] == I, 'proper_spatial_exterior_return_' + str(r))
        jp, jc = julia(xs[r]), julia(cs[r])
        eq(jp.H*jp, s.eye(32), 'literal_Julia_P_unitarity_' + str(r))
        eq(jc.H*jc, s.eye(32), 'literal_Julia_C_unitarity_' + str(r))
        for word in (jp, jp.H, -jc, -jc.H):
            words.extend([word, word])
    require(len(words) == 32, 'four_roles_four_words_two_duplicates')
    H32 = s.Matrix(32,32,lambda i,j: (-1)**bin(i & j).count('1'))
    eq(H32*H32.T, 32*s.eye(32), 'literal_32label_Walsh_orthogonality')
    d = sum((xs[r]-cs[r] for r in range(4)), O.copy())
    D = d+d.H
    contrasts = [(1,1,1,1), (1,1,-1,-1), (1,-1,1,-1), (1,-1,-1,1)]
    Ms, Ds = [], []
    for index, chi in enumerate(contrasts):
        row = (0,16,8,24)[index]
        block = sum((H32[row,j]*words[j] for j in range(32)), s.zeros(32))/32
        M = block[:16,:16]
        Dc = sum((chi[r]*(xs[r]-cs[r]+xs[r].H-cs[r].H)
                  for r in range(4)), O.copy())
        eq(M, Dc/16, 'actual_Walsh_role_top_block_' + str(index))
        eq(M.H, M, 'role_block_Hermitian_' + str(index))
        Ms.append(M)
        Ds.append(Dc)
    A, M = Ms[0], Ms[1]
    eq(A, D/16, 'same_actual_blank_D_block')
    require(A*M != M*A, 'noncommuting_actual_blank_and_role_blocks')
    require(sum((xs[r]-cs[r]+xs[r].H-cs[r].H for r in range(4)), O.copy()) != Ds[1],
            'hostile_role_contrast_not_blank_compression')

    p = s.Symbol('p', real=True)
    def red(x):
        return s.rem(s.expand(x), p*p+p-1, p)
    effect = 4*p**2*A.H*M*M.H*A
    # Sum both actual golden ports. The second coefficient is (ap)^2=p^3.
    from_ports = 4*(p**4+p**3)*A.H*M*M.H*A
    eq(from_ports, effect, 'golden_port_union_coefficient_4p_squared', red)
    eq(effect, p**2*D*Ds[1]**2*D/16384,
       'actual_final_role_effect_h4_coefficient', red)
    require(effect != 4*p**2*M*M.H*A*A.H,
            'hostile_incoming_A_order_is_not_commuted')
    # All 128 outcomes remain, including blank/port1 and all other labels.
    b = s.Symbol('blank_A', real=True)
    eq((1-2*p**2*b*b)**2+4*p**3*b**4
       +4*(p**4+p**3)*b*b*(1-b*b), 1,
       'all128_completeness_from_unitary_Q_row', red)
    eq(4*(p**4+p**3),4*p**2,'hostile_single_golden_port_not_union',red)
    require(red(4*p**4-4*p**2) != 0, 'omit_second_port_changes_actual_effect')

    # Exact noncommuting finite first-exit sum independently from composed
    # chronological event amplitudes; no reset or power-of-effect shortcut.
    B2 = s.diag(s.Rational(4,5),s.Rational(3,5))
    K2 = s.Matrix([[s.Rational(1,5),s.Rational(1,10)],
                   [s.Rational(1,20),s.Rational(1,5)]])
    E2 = K2.H*K2
    F2 = first_exit_effect(B2,E2,3)
    chronological = sum(((K2*B2**j).H*(K2*B2**j) for j in range(3)),s.zeros(2))
    eq(F2,chronological,'three_disjoint_history_events_exact_chronological_sum')
    require(B2*E2 != E2*B2 and F2 != 3*E2,
            'hostile_reset_and_commuting_shortcuts_rejected')
    eq(first_exit_effect(B2,E2,0),s.zeros(2),'no_round_has_no_first_exit')
    r = s.Matrix([[2,1],[1,3]])
    dr = s.Matrix([[1,2],[2,-1]])+r
    de = s.Matrix([[1,2],[2,0]])/100
    t = s.Symbol('variation', real=True)
    independent = s.diff(s.trace((r+t*dr)*(F2+t*de))/s.trace(r+t*dr),t).subs(t,0)
    eq(normalized_source(r,dr,F2,de),independent,'full_moving_preparation_and_event_normalizer')
    require(normalized_source(r,dr,F2,de) != s.trace(dr*F2+r*de)/s.trace(r),
            'hostile_frozen_normalizer_rejected')
    eq(normalized_source(r,r,F2,s.zeros(2)),0,'radial_preparation_source_cancels')

    h, lam, tail = s.symbols('h lambda survival_power', positive=True)
    c0 = p**2/128
    scalar_finite = p**2*h*h*lam*(1-tail)/(16384*(1-(1-c0*h*h*lam)**2))
    eq(s.cancel(scalar_finite), (1-tail)/(256*(1-c0*h*h*lam/2)),
       'exact_scalar_first_exit_clock_factor',s.simplify)
    eq(p**2/(32768*c0),s.Rational(1,256),'operator_Riemann_clock_coefficient_1_over256',s.simplify)

    # Exact all-angle coordinate LC coframe. q=theta', x=sin(2theta),
    # y=cos(2theta); no trigonometric numerical substitution or grade cut.
    x,y,q = s.symbols('sin2theta cos2theta theta_prime',real=True)
    e = elementary
    mr = [q*(x*e(0,2)-y*e(1,2)+e(2,1)),
          q*(-y*e(0,2)-x*e(1,2)-e(2,0)),
          q*(e(0,1)-e(1,0)),s.zeros(4)]
    hr = [lift(m) for m in mr]
    jr = [C[r]*hr[r]+hr[r].H*C[r].H for r in range(4)]
    eq(sum((C[r]*hr[r] for r in range(4)),O.copy()),O,'actual_cone_full16_Cartan_identity')
    eq(sum(jr,O.copy()),O,'actual_continuum_D_cancels_connection')
    jc = jr[0]+jr[1]-jr[2]-jr[3]
    eq(jc,-2*jr[2],'one_existing_Walsh_contrast_retains_exact_connection')
    eq(s.trace(jc.H*jc),32*q*q,'all_angle_full16_role_contrast_norm_32')
    for i in range(3):
        for j in range(i,3):
            expected = ([[4*(1+y*y),-4*y*y,-4],
                         [-4*y*y,4*(1+y*y),-4],[-4,-4,8]][i][j])*q*q
            expr=s.expand(s.trace(jr[i]*jr[j])-expected)
            eq(s.rem(expr,x*x+y*y-1,x),0,'all_angle_Gram_' + str(i)+str(j))
    for r0 in range(4):
        eq(s.trace((C[r0]-C[r0].H)*jc),0,'full16_kinetic_potential_trace_' + str(r0))
    eq(s.trace(jc.H*jc)/16,2*q*q,'isotropic_Fock_cone_signal')
    require(jc != O and sum(jr,O.copy()) == O,
            'hostile_sum_before_label_readout_erases_nonzero_signal')
    eq(s.diff(s.Rational(1,256)*2*q*q,q),q/64,
       'first_exit_cone_gradient_before_integration_by_parts')
    survival, radius = s.symbols('one_minus_exp_beta_lambda radius',positive=True)
    readout_contrast = survival*q*q/(128*radius**2)
    eh_cone = -2*radius**2*q*q
    eq(readout_contrast,-survival*eh_cone/(256*radius**4),
       'actual_history_curvature_comparison_one_cone_family',s.cancel)
    eq(s.diff(readout_contrast,q),
       s.diff(-survival*eh_cone/(256*radius**4),q),
       'same_fixed_scale_cone_source_not_all_metric_rows',s.cancel)

    return {
        'status':'PASS','exact_checks':len(checks),'checks':checks,'source_pins':PINS,
        'carrier':{'Fock':16,'role_Walsh_contrasts':3,'labels':32,
                   'coefficient_qubit':2,'golden_ports':2,'outcomes_per_round':128,
                   'reference_retained':128,'fresh_round_workspace':'128^n'},
        'actual_event':'j all-blank rounds; nonblank chi label/coefficient0 at next; both ports; all later outcomes',
        'finite_effect':'sum_j B^j [p^2 h^4 D D_chi^2 D / 16384] B^j',
        'limit_operator':'integral_0^beta exp(-t Delta/2) D D_chi^2 D exp(-t Delta/2) dt / 256',
        'cone_chi':[1,1,-1,-1],
        'cone_full_shell_reading':'(1-exp(-beta/s^2)) [1+2 mean(theta_prime^2)] / (256 s^2)',
        'curvature_comparison':'L_chi(theta)-L_chi(const) = -(1-exp(-beta/s^2)) I_EH(theta)/(256 s^4); only this cone family, fixed scale/source',
        'scope':{'old_entrypoints_executed':False,'new_price_added':False,
                 'reference_pointer_selected':False,'physical_matrix_gate_admission':False,
                 'all10_Einstein_or_full_joint_stationarity':False,
                 'smooth_C1_matrix_element_limit_proved_in_memo':True,
                 'uniform_raw_C0_history_source_limit_claimed':False},
    }


if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
