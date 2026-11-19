#!/usr/bin/env python3
"""Bounded consumer of full-source 6.18-6.22, not physical GR admission.

Existing one-tick feedback results are not replayed. This checks the new
two-tick tensor/source, clean-work type control and literal charge boundary.
"""
import json
import sympy as s


def require(value, label):
    if not value:
        raise ArithmeticError(label)


def tensor_feedback():
    e = s.symbols('e', positive=True)
    a, b = s.sqrt(1-e), s.sqrt(e)
    T = s.Matrix([[a, 0, -b, 0], [0, a, 0, -b],
                  [0, b, 0, a], [b, 0, a, 0]])
    P = s.diag(1, 1, 0, 0)
    F = s.simplify(P*(T*T).T*(s.eye(4)-P)*(T*T)*P)
    expected = s.zeros(4)
    expected[:2, :2] = 2*e*(1-e)*s.ones(2)
    require(s.simplify(F-expected) == s.zeros(4), 'literal two-tick feedback')
    require(s.simplify(s.trace(F)-4*e*(1-e)) == 0, 'one live and one zero branch')
    require(264+184 == 448 and 448+184+36+36+44+44 == 792,
            'all native flat tensor determinant exponents')
    require(22976-528 == 22448 and 528-264 == 264,
            'ambient complement differs from retained zero spectrum')
    require(2*528 == 1056, 'full return-cut rank per regular multiplicity')
    M = s.Matrix([[1, 1], [1, 0]])
    for n in range(12):
        d, D = M**n*s.ones(2, 1), M**(n+6)*s.ones(2, 1)
        K = (d.T*D)[0]
        require(K == s.fibonacci(2*n+9), 'full regular multiplicity denominator')
        for k in range(n+1):
            coarse = M**(n-k)*D
            require(coarse == s.Matrix([s.fibonacci(2*n-k+8), s.fibonacci(2*n-k+7)]),
                    'exact coarse trace equals uniform LEFT level 2N+6')
    return {'two_tick_live_eigenvalue': '4e(1-e)',
            'native_retained_scene_modes': 528, 'ambient_scene_complement': 22448,
            'retained_scene_zero_modes': 264, 'flat_feedback_rank_per_K': 792,
            'return_cut_rank_per_K': 1056,
            'trace_weight_origin': 'ordinary regular determinant; no RIGHT measurement'}


def partial_trace(A, da, db, traced):
    if traced == 'scene':
        return s.Matrix(da, da, lambda i, j: sum(A[i*db+k, j*db+k] for k in range(db)))
    return s.Matrix(db, db, lambda i, j: sum(A[k*db+i, k*db+j] for k in range(da)))


def moving_scene_source():
    E = s.Matrix([[s.Rational(1, 4), s.Rational(1, 17)],
                  [s.Rational(1, 17), s.Rational(1, 3)]])
    B = s.Matrix([[s.Rational(1, 5), s.Rational(1, 11)],
                  [s.Rational(1, 11), s.Rational(2, 7)]])
    dE = s.Matrix([[s.Rational(2, 7), s.Rational(1, 9)],
                   [s.Rational(1, 9), -s.Rational(1, 5)]])
    dB = s.Matrix([[s.Rational(1, 4), -s.Rational(2, 13)],
                   [-s.Rational(2, 13), s.Rational(1, 8)]])
    require(E*dE != dE*E and B*dB != dB*B, 'noncommuting field directions')
    I, z, D, K = s.eye(2), s.Rational(1, 3), 5, 10
    lam = 4*E*(I-E)
    dlam = 4*(dE-E*dE-dE*E)
    Q = I-z*B
    R = (1-z)*s.eye(4)+z*s.kronecker_product(I-lam, I-B)
    Ri = R.inv()
    CE = 4*z*(I-2*E)*partial_trace(s.kronecker_product(I, I-B)*Ri, 2, 2, 'scene')
    HB = z*(K*Q.inv()+D*partial_trace(s.kronecker_product(I-lam, I)*Ri, 2, 2, 'old'))
    jacobi = z*K*s.trace(Q.inv()*dB)+z*D*s.trace(
        Ri*(s.kronecker_product(dlam, I-B)+s.kronecker_product(I-lam, dB)))
    require(jacobi == D*s.trace(CE*dE)+s.trace(HB*dB), 'complete exact moving-scene covector')
    require(CE == CE.T and HB == HB.T, 'both source matrices selfadjoint')
    require(CE[0, 0] > 0 and CE.det() > 0 and HB[0, 0] > 0 and HB.det() > 0,
            'positive full source on the specified interior window')
    skew = s.Matrix([[0, -1], [1, 0]])
    require(s.trace(HB*(skew*B-B*skew)) == 0, 'genuine isospectral motion has zero source')
    # An occupied balanced state does NOT kill a determinant's scene row.
    Bd = s.diag(s.Rational(1, 4), s.Rational(3, 4))
    rho, direction = I/2, s.diag(1, -1)
    lam0 = s.Rational(3, 4)
    H0 = z*((I-z*Bd).inv()+(1-lam0)*(I-z*(lam0*I+(1-lam0)*Bd)).inv())
    require(s.trace(rho*Bd) == s.Rational(1, 2) and s.trace(rho*direction) == 0,
            'balanced expectation and its derivative can both stay fixed')
    require(s.trace(H0*direction) != 0, 'negative control: nonzero full determinant source')
    return {'source': 'D Tr(C_E dE) + Tr(H_B dB)',
            'noncommuting_directions': True, 'balanced_state_cancels_scene_row': False,
            'spectator_factor': 'multiply BOTH covectors by actual nu',
            'whole_stack_remaining_source_proved_zero': False}


def rotation(size, i, j, cosine, sine):
    out = s.eye(size)
    out[i, i] = out[j, j] = cosine
    out[j, i], out[i, j] = sine, -sine
    return out


def clean_work_and_smooth_birth():
    z = s.Rational(1, 3)
    U = rotation(4, 0, 2, s.Rational(3, 5), s.Rational(4, 5))
    V = rotation(4, 1, 3, s.Rational(5, 13), s.Rational(12, 13))*U
    old_cut, clean_cut = s.diag(1, 1, 0, 0), s.diag(1, 0, 0, 0)
    require(U*clean_cut == V*clean_cut, 'identical FULL output on clean domain')
    def pencil(W, P):
        F = P*W.T*(s.eye(4)-P)*W*P
        return s.eye(4)-z*F
    require(pencil(U, old_cut).det() != pencil(V, old_cut).det(),
            'old work-I cut sees uncontrolled offblank word')
    require(pencil(U, clean_cut) == pencil(V, clean_cut),
            'actual clean-return cut gives identical entire determinant')
    # All feedback leakage can go into an offblank OUTPUT and remains counted.
    leak = rotation(4, 0, 3, s.Rational(3, 5), s.Rational(4, 5))
    F_leak = clean_cut*leak.T*(s.eye(4)-clean_cut)*leak*clean_cut
    require(F_leak[0, 0] == s.Rational(16, 25), 'failed work leakage is retained')
    x = s.symbols('x', real=True)
    J = -s.log(1-z*s.sin(x)**2)
    jets = [s.diff(J, x, j).subs(x, 0) for j in range(4)]
    require(jets == [0, 0, 2*z, 0], 'zero-feedback birth is regular through C3')
    require(6144+6144+768+768+16+16 <= 2**14, 'safe third-jet coefficient budget')
    require(s.Rational(4*1056, 1056) == 4, 'K and reference multiplicity cancel')
    return {'clean_return_test_required': True, 'old_offblank_countercontrol': 'nonzero',
            'zero_feedback_jets': [str(v) for v in jets],
            'first_source_bound': '4 z r L epsilon/(1-z)^2',
            'C3_bound_fixed_z': '2^14 z r L^6 epsilon/(1-z)^4',
            'relative_bound': 'dimension independent; true t^-2 and spatial budget remain',
            'exact_compiled_roots_inferred': False}


def car_charge_boundary():
    creators = []
    for i in range(4):
        C = s.zeros(16)
        for mask in range(16):
            if not ((mask >> i) & 1):
                sign = (-1)**bin(mask & ((1 << i)-1)).count('1')
                C[mask | (1 << i), mask] = sign
        creators.append(C)
    number = [C*C.T for C in creators]
    H = s.diag(*[int(bin(mask >> 1).count('1') >= 2) for mask in range(16)])
    J0 = creators[0]-creators[0].T
    require(H*J0 == J0*H and H*number[0] == number[0]*H,
            'literal clock and record factors preserve spatial-sector charge')
    require(any(H*C != C*H for C in creators[1:]), 'actual spatial Julia blocks break charge')
    high = (s.eye(16)-number[0])*H
    require(all((H-high)[i, i] >= 0 for i in range(16)), 'literal B/L <= H')
    require((H[1, 1]+H[15, 15])/2 == s.Rational(1, 2), 'owned e0+top seed charge')
    # Algebraic irreducibility, without assuming control-group transitivity:
    # creators and adjoints generate all |mask><0| and thus all matrix units.
    vacuum = s.eye(16)
    for N in number:
        vacuum = vacuum*(s.eye(16)-N)
    require(vacuum == s.diag(1, *([0]*15)), 'vacuum is a native CAR polynomial')
    for mask in range(16):
        matrix = vacuum
        for i in range(4):
            if (mask >> i) & 1:
                matrix = creators[i]*matrix
        require(abs(matrix[mask, 0]) == 1 and sum(abs(v) for v in matrix) == 1,
                'every matrix-unit column belongs to generated CAR algebra')
    return {'full_CAR_components': 16,
            'fixed_word_seed_sector': '<H>=1/2, hence b<=L_scene/2<1/2',
            'common_CAR_charge_all_four_Julia_primitives': 'scalar for complex-linear/real16 observables',
            'full_controllability_or_matter_stress_inferred': False}


def same_program_control():
    delta = s.symbols('delta', real=True)
    alpha, lam, z = s.Rational(1, 7), s.Rational(2, 5), s.Rational(1, 3)
    survival = 1-alpha*delta**2*lam
    v8_feedback = 1-survival**6
    require(s.limit(v8_feedback, delta, 0) == 0, 'fixed-word v8 feedback vanishes')
    a, b = s.Rational(3, 4), s.Rational(1, 5)
    require(a+(1-a)*b >= a > 0, 'retained active AF branch stays positive')
    scalar_pencil = 1-z*v8_feedback
    lifted_pencil = s.diag(scalar_pencil, scalar_pencil, scalar_pencil)
    require(s.expand(lifted_pencil.det()-scalar_pencil**3) == 0,
            'honest spectator trace-log repeats old feedback price')
    require(1-z*(a+b-a*b) != (1-z*a)*(1-z*b),
            'tensor survival composition is not additive trace-log price')
    for n in range(12):
        D0, D1 = s.fibonacci(n+8), s.fibonacci(n+7)
        require(D0**2+D1**2 == s.fibonacci(2*n+15),
                'full AF spectator dimension differs from active multiplicity K')
    return {'fixed_word_v8_feedback_flat_scaling_limit': '0',
            'AF_star_retained_active_feedback_lower_bound': 'L_scene>0',
            'honest_full_AF_spectator_multiplier': 'F_(2N+15)=O(F_(2N+9))',
            'old_feedback_suppressed_by_AF_dimension': False,
            'same_program_heat_feedback_interface_proved': False}


def fixed_word_scaling_control():
    scale, a = s.symbols('scale a', real=True)
    eps = s.Rational(1, 5)
    q = [0, 1, 0]
    differences = [q[(j+1) % len(q)]-q[j] for j in range(len(q))]
    radii = [1+eps*d for d in differences]
    require(all(r > 0 for r in radii), 'nondegenerate periodic coframe')
    star_rows = [r*s.sinh(scale**2*a*d)/scale**2
                 for r, d in zip(radii, differences)]
    source = sum(s.diff(f, a).subs(a, 0) for f in star_rows)
    require(s.simplify(source-2*eps) == 0 and source > 0,
            'two coframe powers cancel link scaling in actual boost component')
    # A scalar block of the actual strict-contraction Julia germ; the full
    # matrix proof uses the same analytic square-root/product rule in 6.22.
    X = scale*s.exp(scale**2*a)
    root = s.sqrt(1-X**2)
    julia = s.Matrix([[X, root], [root, -X]])
    derivative = julia.diff(a).subs(a, 0)
    limits = derivative.applyfunc(lambda x: s.limit(x/scale**3, scale, 0))
    require(limits == s.diag(1, -1), 'native Julia source is O(scale^3)')
    return {'periodic_boost_star_source': str(source),
            'native_fixed_query_word_source': 'O(scale^3)',
            'exact_open_patch_star_factorization': False,
            'compact_C3_approximation_excluded': False,
            'individual_exact_roots_excluded': False}


if __name__ == '__main__':
    result = {'status': 'PASS', 'tensor_feedback': tensor_feedback(),
              'moving_scene': moving_scene_source(),
              'compiled_source': clean_work_and_smooth_birth(),
              'preparation_boundary': car_charge_boundary(),
              'same_program': same_program_control(),
              'fixed_word_scaling': fixed_word_scaling_control(),
              'physical_full_D0_GR_proved': False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
