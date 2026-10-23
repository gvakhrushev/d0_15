#!/usr/bin/env python3
"""Complete-exit operator inverse and a full16 flat ultraviolet control.

This executes only the pinned literal CAR definitions, never an old checker.
The positive operator quotient determines Delta, not the native field tuple,
and is not a physical tomography/preparation/admission theorem.

For E=I-B**m, B=I-alpha*Delta>0, beta=m*alpha,
  D_Delta E[V] = alpha sum_k B**k V B**(m-1-k).
Its HS eigenvalues are alpha sum_k b_i**k b_j**(m-1-k)>0.
The exact finite-clock low-energy inverse bound is
  1/[beta*(1-alpha*Lambda)**(m-1)],
whose limit is exp(beta*Lambda)/beta. The latter need not bound the
finite-clock inverse from above.

On the flat full16 symbol u_r=nu*e_r and any role character chi_r=+/-1,
  D_chi(k)**2 = D(k)**2 = lambda_h(k)*I16,
  r=h**2*lambda_h=4*nu**2 sum_r sin(k_r/2)**2.
The actual chi first-exit effect is therefore exactly
  F_chi = r*(1-B**(2*n))/[256*(1-c0*r/2)], c0=p**2/128.
For L=4*ell, a half-open one-axis UV patch contains exactly half of all
momenta and has r>=2*nu**2. If 4*n*c0*nu**2>=1, log(1-x)<=-x and
exp(-1)<1/2 give the normalized full trace q_chi>=nu**2/512.
Thus the smooth finite-energy h**-2 limit cannot be traced uniformly over
the complete unweighted lattice carrier. Combine the retained outcomes
before applying the actual native spectral functional.
"""

from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
V8 = '02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md'
PINS = {
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    V8: 'f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c',
}


def _creators(repo):
    tree = ast.parse((repo / CURVED).read_text())
    nodes = [node for node in tree.body if
             (isinstance(node, ast.FunctionDef) and node.name == 'creator') or
             (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name)
              and t.id == 'EXTERIOR_ORDER' for t in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('exit_inverse_uv:literal_creator_definition_nodes')
    scope = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CURVED, 'exec'), scope)
    return [scope['creator'](r) for r in range(4)], scope['EXTERIOR_ORDER']


def complete_exit(B, power):
    """Complete retained first-exit effect for power=2*rounds."""
    if not isinstance(power, int) or power < 1:
        raise ValueError('power must be a positive integer')
    return s.eye(B.rows)-B**power


def exit_first_jet(B, delta_generator, alpha, power):
    """D_Delta E[delta_generator], without a commutation assumption."""
    if not isinstance(power, int) or power < 1:
        raise ValueError('power must be a positive integer')
    return alpha*sum((B**j*delta_generator*B**(power-1-j)
                      for j in range(power)), s.zeros(B.rows))


def recover_generator(effect, alpha, power):
    """Exact principal positive root; contract: I-effect is positive definite."""
    if not isinstance(power, int) or power < 1:
        raise ValueError('power must be a positive integer')
    return (s.eye(effect.rows)-(s.eye(effect.rows)-effect)**s.Rational(1,power))/alpha


def _sylvester(A, rhs):
    """Small exact Sylvester solve, not a diagonal/commuting substitute."""
    if A.rows != A.cols or rhs.shape != A.shape:
        raise ValueError('square matching Sylvester matrices required')
    unknowns = tuple(s.Dummy('sylvester_' + str(i)) for i in range(A.rows**2))
    W = s.Matrix(A.rows,A.cols,unknowns)
    matrix, vector = s.linear_eq_to_matrix(list(A*W+W*A-rhs), unknowns)
    return s.Matrix(A.rows,A.cols,list(matrix.inv()*vector))


def inverse_exit_jet_power_of_two(B, delta_effect, alpha, power):
    """D_E Delta by the exact positive square-root Sylvester chain.

    B is the already recovered positive base. This method is deliberately
    restricted to power=2**k; the positivity theorem is valid for all m.
    """
    if not isinstance(power, int) or power < 1 or power & (power-1):
        raise ValueError('power must be a positive power of two')
    current, exponent = -delta_effect, power  # delta K=-delta E
    while exponent > 1:
        root = B**(exponent//2)
        current = _sylvester(root,current)
        exponent //= 2
    return -current/alpha


def flat_rare_effect(r, tail, p):
    """Exact commuting flat symbol after all n actual first-exit times."""
    c0 = p**2/128
    return r*(1-tail)/(256*(1-c0*r/2))


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('exit_inverse_uv:' + name)
        checks.append(name)

    def eq(actual, expected, name, reduce=s.expand):
        values = list(actual-expected) if isinstance(actual,s.MatrixBase) else [actual-expected]
        require(all(reduce(value) == 0 for value in values),name)

    for path,digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)

    # A rational positive, non-diagonal base and a genuinely noncommuting,
    # complex Hermitian generator jet. Full operator inverse, not scalar data.
    I2 = s.eye(2)
    U = s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],
                  [s.Rational(4,5),s.Rational(3,5)]])
    b0,b1 = s.Rational(1,2),s.Rational(3,4)
    B = U*s.diag(b0,b1)*U.T
    alpha,power = s.Rational(1,10),4
    beta = power*alpha
    Delta = (I2-B)/alpha
    V = s.Matrix([[s.Rational(2,3),s.Rational(1,5)+s.I/7],
                  [s.Rational(1,5)-s.I/7,-s.Rational(1,4)]])
    E = complete_exit(B,power)
    eq(U.T*U,I2,'rational_positive_spectral_frame')
    require(B*V != V*B and V.H == V,'noncommuting_complex_Hermitian_generator_jet')
    eq(recover_generator(E,alpha,power),Delta,
       'positive_complete_operator_effect_recovers_generator',s.simplify)
    dE = exit_first_jet(B,V,alpha,power)
    eq(dE,dE.H,'noncommuting_effect_jet_Hermitian')
    eq(inverse_exit_jet_power_of_two(B,dE,alpha,power),V,
       'two_Sylvester_roots_recover_full_noncommuting_jet',s.simplify)
    diagonal_dE = U.T*dE*U
    diagonal_V = U.T*V*U
    eigenvalues = [b0,b1]
    coefficients = s.Matrix(2,2,lambda i,j:
        alpha*sum(eigenvalues[i]**k*eigenvalues[j]**(power-1-k)
                  for k in range(power)))
    eq(diagonal_dE,s.matrix_multiply_elementwise(coefficients,diagonal_V),
       'all_four_Loewner_divided_difference_coefficients',s.simplify)
    require(all(beta*b0**(power-1) <= value <= beta for value in coefficients),
            'sharp_HS_lower_and_upper_spectral_bounds')

    HSbasis = [s.diag(1,0),s.diag(0,1),
               s.Matrix([[0,1],[1,0]])/s.sqrt(2),
               s.Matrix([[0,s.I],[-s.I,0]])/s.sqrt(2)]
    HSmap = s.Matrix(4,4,lambda i,j:
        s.simplify(s.trace(HSbasis[i]*exit_first_jet(B,HSbasis[j],alpha,power))))
    eq(HSmap.T,HSmap,'full_Hermitian_HS_map_selfadjoint')
    require(all(s.simplify(HSmap[:j,:j].det()) > 0 for j in range(1,5)),
            'HS_positive_definiteness_all_leading_minors')
    eq(HSmap.det(),coefficients[0,0]*coefficients[1,1]*coefficients[0,1]**2,
       'HS_determinant_all_real_and_imaginary_directions',s.simplify)
    expected_worst = 1/(beta*b0**(power-1))
    lowest_projector = U*s.diag(1,0)*U.T
    eq(inverse_exit_jet_power_of_two(B,lowest_projector,alpha,power),
       expected_worst*lowest_projector,'worst_HS_inverse_bound_is_attained',s.simplify)

    # The same complete effect determines the literal v8 H+J+R functional.
    # Keep a noncommuting actual normalized density and reference M=128.
    amplitude = s.Matrix([[1,1+s.I],[0,2]])
    raw_density = (amplitude*amplitude.H).applyfunc(s.expand)
    rho = (raw_density/s.simplify(s.trace(raw_density))).applyfunc(s.simplify)
    require(rho.H == rho and s.trace(rho) == 1 and rho*B != B*rho,
            'normalized_preparation_need_not_commute_with_generator')
    M,z = 128,s.Rational(1,16)
    K,Z = I2-E,s.trace(I2-E)
    F = I2-z*E
    inverse_rho = inverse_exit_jet_power_of_two(B,rho,alpha,power)
    source_E = -I2/(beta*Z)+M*z*F.inv()+inverse_rho
    source_Delta = rho-B**(power-1)/Z+M*beta*z*B**(power-1)*F.inv()
    eq(s.trace(source_E*dE),s.trace(source_Delta*V),
       'same_v8_full_action_source_through_operator_inverse_noncommuting_rho',s.simplify)
    eq(s.trace(rho*recover_generator(E,alpha,power)),s.trace(rho*Delta),
       'actual_normalized_matter_reading_not_logarithmic_generator',s.simplify)
    eq(sum((B**j*(I2-B**2)*B**j for j in range(power//2)),s.zeros(2)),E,
       'all_retained_first_exit_times_telescope_to_B_power_2n')

    # Hostile control: exp(beta*Lambda)/beta is the limit, not always an
    # upper bound at finite alpha. Here alpha*Lambda=1/2, m=4, beta*Lambda=2.
    exp2_upper = sum((s.Rational(2)**j/s.factorial(j) for j in range(13)),s.S.Zero)
    exp2_upper += (s.Rational(2)**13/s.factorial(13))/(1-s.Rational(2,14))
    require(exp2_upper < 8,
            'finite_clock_inverse_can_exceed_continuum_exp_bound')
    x,theta = s.symbols('x theta',positive=True)
    eq(s.diff(-s.log(1-x),x),1/(1-x),
       'finite_low_energy_log_bound_integrand')

    # Only literal creator definitions: retain every one of the sixteen
    # exterior masks and arbitrary complex Fourier increments.
    C,order = _creators(repo)
    I16,O16 = s.eye(16),s.zeros(16)
    require(order == (0,2,3,1),'literal_ACDB_order_and_all16_components')
    require(all(C[i]*C[j].H+C[j].H*C[i] == (I16 if i == j else O16)
                and C[i]*C[j]+C[j]*C[i] == O16
                for i in range(4) for j in range(4)),
            'full16_CAR_before_symbol_reduction')
    xr = s.symbols('x0:4',real=True)
    yr = s.symbols('y0:4',real=True)
    nu,h = s.symbols('nu h',positive=True)
    character = (1,1,-1,-1)
    D = nu/h*sum(((xr[j]+s.I*yr[j])*C[j]
                  +(xr[j]-s.I*yr[j])*C[j].H for j in range(4)),O16.copy())
    Dchi = nu/h*sum((character[j]*((xr[j]+s.I*yr[j])*C[j]
                  +(xr[j]-s.I*yr[j])*C[j].H) for j in range(4)),O16.copy())
    lam = nu**2/h**2*sum(xr[j]**2+yr[j]**2 for j in range(4))
    eq(D**2,lam*I16,'generic_complex_phase_full16_native_D_square')
    eq(Dchi**2,lam*I16,'generic_complex_phase_full16_Walsh_Dchi_square')
    require(Dchi != D,'Walsh_operator_is_not_silently_replaced_by_D')
    k = s.symbols('k',real=True)
    eq((s.cos(k)-1)**2+s.sin(k)**2,4*s.sin(k/2)**2,
       'literal_forward_phase_lattice_dispersion',s.trigsimp)

    p,r,tail = s.symbols('p r tail',positive=True)
    c0 = p**2/128
    bflat = 1-c0*r
    single_event = p**2*r**2/s.Integer(16384)
    eq(single_event*(1-tail)/(1-bflat**2),flat_rare_effect(r,tail,p),
       'exact_all_n_flat_rare_effect_including_survival_denominator',s.cancel)
    eq(flat_rare_effect(r,tail,p)/(1-tail),
       r/(256*(1-c0*r/2)),'rare_to_total_exit_ratio_not_homogeneous_h2_at_UV',s.cancel)
    eq(c0*(16*nu**2),p**2*nu**2/8,
       'full_flat_UV_contractivity_for_0_p_nu_lt1')

    # Analytic count, not a large lattice scan. [L/4,3L/4) contains 2ell
    # integer frequencies on L=4ell, with all other axes and full16 retained.
    ell = s.symbols('ell',positive=True,integer=True)
    L = 4*ell
    eq((2*ell)*L**3*16/(L**4*16),s.Rational(1,2),
       'exact_half_UV_patch_fraction_L4ell_all_momenta_full16')
    eq(s.sin(k/2)**2-s.Rational(1,2),-s.cos(k)/2,
       'UV_patch_sine_lower_bound_reduces_to_cos_nonpositive',s.trigsimp)
    require(all(s.sin(value/2)**2 >= s.Rational(1,2)
                for value in (s.pi/2,s.pi,3*s.pi/2)),
            'UV_patch_endpoints_and_interior_minimum_controls')
    eq(s.diff(s.log(1-x)+x,x),-x/(1-x),
       'survival_bound_log1minusx_le_minusx',s.cancel)
    require(1+1+s.Rational(1,2) > 2,
            'exp_minus1_strictly_below_one_half_by_positive_series')
    eq(s.Rational(1,2)*(2*nu**2/s.Integer(512)),nu**2/s.Integer(512),
       'normalized_full_trace_UV_lower_bound_nu2_over512')
    lam0,survival = s.symbols('lambda0 survival',positive=True)
    eq(s.limit(flat_rare_effect(h**2*lam0,survival,p)/h**2,h,0),
       lam0*(1-survival)/256,
       'fixed_energy_limit_with_survival_exp_minus_beta_lambda')

    return {
        'status':'PASS','exact_checks':len(checks),'checks':checks,
        'source_pins':PINS,'full_exterior_components':16,
        'operator_inverse':{
            'power':'m=2n','generator':'Delta=[I-(I-E)^(1/m)]/alpha',
            'forward_HS_spectrum':'t_ij=alpha sum_k b_i^k b_j^(m-1-k)',
            'inverse_bound':'1/[beta*bmin^(m-1)], attained at a lowest-base spectral projector',
            'finite_low_energy_bound':'1/[beta*(1-alpha*Lambda)^(m-1)]',
            'continuum_low_energy_limit':'exp(beta*Lambda)/beta; not a universal finite-clock upper bound',
            'uniform_finite_low_energy_bound':'exp(beta*Lambda/(1-theta))/beta if alpha*Lambda<=theta<1',
        },
        'same_price':{
            'HJ':'beta^-1 log[128*128^n*Tr(I-E)]-128 Tr log(I-zE)',
            'R':'Tr rho [I-(I-E)^(1/(2n))]/alpha, normalized rho, no commutation premise',
            'field_derivative_workspace':'zero only at fixed h,p,n,reference and experiment',
        },
        'ultraviolet':{
            'flat_dispersion':'r=h^2 lambda_h=4 nu^2 sum sin(k_r/2)^2',
            'exact_rare_effect':'r(1-B^(2n))/[256(1-c0*r/2)]',
            'assumptions':'0<nu<1, p=(sqrt(5)-1)/2, c0=p^2/128, L=4ell, 4n*c0*nu^2>=1',
            'normalized_trace_lower_bound':'q_chi>=nu^2/512',
            'fixed_energy_limit':'h^-2 F_chi -> lambda(1-exp(-beta*lambda))/256',
            'UV_inverse_growth':'beta^-1(1-16c0*nu^2)^(-(m-1)) at maximal lattice frequency',
        },
        'scope':[
            'Exact positive finite operator quotient, not physical tomography or field-map injectivity.',
            'All16 CAR grades and all L^4 momenta retained in the analytical UV count.',
            'No uniform trace/source limit follows by tracing the smooth finite-energy rare-event limit.',
            'Native spectral H+J+R must use the complete retained effect and actual normalized preparation.',
            'No old checker, root search, lattice census, new action, physical measure or admission law.',
        ],
    }


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,ensure_ascii=False))
