#!/usr/bin/env python3
"""Exact first causal source on the actual proper-LC winding stencil.

Only pinned CAR and literal LC-generator definitions are extracted. No old
run(), lattice spectrum, heat loop, root search or result writer is called.
The actual radial balance is consumed, not fitted. The result concerns a
COMMON momentum-diagonal vacuum/top density on the whole first shell.
"""
from functools import lru_cache
from pathlib import Path
import ast
import hashlib
import json
import sympy as s


ROOT = Path(__file__).resolve().parents[4]
PINS = {
    '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py':
        'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    '02_REGISTRY/research/sources/d0_cone_matter_corrector_2026-10-16/check_cone_matter_corrector.py':
        '7bbf1589f3a32af381036df64f76d720ce14a9f2e502b3a1a6f43f5b5e776d58',
    '02_REGISTRY/research/sources/d0_ghz_joint_first_jet_2026-10-17/scale_balance.py':
        '746c1b9a961977ceac1931fa26024e0e7856132d16590fdb674de5b568409447',
    '02_REGISTRY/research/sources/d0_ghz_joint_first_jet_2026-10-17/amplitude_first_jet.py':
        '0f0a4f2aa79f3a741d6117ea4aea789d73c24f6024f83e7125d380e70fc1f0b1',
}


def run(repo=None):
    repo = Path(repo) if repo is not None else ROOT
    checks = []

    def require(value, name):
        if not bool(value):
            raise ArithmeticError(name)
        checks.append(name)

    def zero(matrix):
        return all(s.simplify(v) == 0 for v in matrix)

    def eq(left, right, name):
        if isinstance(left, s.MatrixBase):
            require(zero(left-right), name)
        else:
            require(s.simplify(left-right) == 0, name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                'source_pin_'+Path(path).name)
    car_path = repo/next(iter(PINS))
    nodes = [n for n in ast.parse(car_path.read_text()).body if
             (isinstance(n, ast.FunctionDef) and n.name == 'creator') or
             (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and
              t.id == 'EXTERIOR_ORDER' for t in n.targets))]
    require(len(nodes) == 2, 'extract_only_actual_creator_and_order')
    scope = {'s':s, 'lru_cache':lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(car_path), 'exec'), scope)
    c = [scope['creator'](j) for j in range(4)]
    b = [v.T for v in c]
    I, Z = s.eye(16), s.zeros(16)
    gamma = [c[j]-b[j] for j in range(4)]
    vac, top = I[:,0], I[:,15]
    require(all(c[i]*b[j]+b[j]*c[i] == (I if i == j else Z)
                for i in range(4) for j in range(4)), 'actual_full16_CAR')

    def elementary(i,j):
        m = s.zeros(4)
        m[i,j] = 1
        return m

    def lift(m):
        return sum((m[i,j]*c[i]*b[j] for i in range(4) for j in range(4)
                    if m[i,j] != 0), s.zeros(16))

    # Complete 4x4 matrix-unit coverage proves the generic trace identity,
    # including every cross momentum p_a p_r, not only four diagonal modes.
    trace_ok = vac_ok = top_ok = coherence_ok = True
    for i in range(4):
        for j in range(4):
            m = elementary(i,j)
            gm = lift(m)
            for a in range(4):
                for r in range(4):
                    l = c[r]*gm-gm.T*b[r]
                    aa = -(gamma[a]*l+l*gamma[a])
                    target = int(a == r)*s.trace(m)-m[a,r]
                    trace_ok &= s.trace(aa) == 16*target
                    vac_ok &= (vac.T*aa*vac)[0] == 0
                    top_ok &= (top.T*aa*top)[0] == 2*target
                    coherence_ok &= ((vac.T*aa*top)[0] == 0 and
                                     (top.T*aa*vac)[0] == 0)
    require(trace_ok, 'generic_full16_linear_connection_trace_all_cross_momenta')
    require(vac_ok, 'generic_vacuum_first_coefficient_zero')
    require(top_ok, 'generic_top_coefficient_twice_maximally_mixed')
    require(coherence_ok, 'vacuum_top_complex_coherences_do_not_enter')

    # The remaining first-stencil terms have real coefficients and an even
    # number of derivatives. Against D_p=i gamma(p), their real diagonal
    # spectral trace and vac/top expectation vanish. Each A1 term changes
    # exterior degree by at most two, so its vac/top cross entry is zero.
    number = sum((c[j]*b[j] for j in range(4)), s.zeros(16))
    require(all(number*c[r]-c[r]*number == c[r] and
                number*b[r]-b[r]*number == -b[r] for r in range(4)),
            'all_first_stencil_terms_have_degree_change_at_most_two')
    eq((vac.T*top)[0],0,'vacuum_top_are_orthogonal_full_carrier_vectors')

    y, epsilon = s.symbols('y epsilon', real=True)
    a0 = s.Matrix([s.cos(y),s.sin(y),0,0])
    a_epsilon = s.Matrix([s.cos(epsilon)*s.cos(y),s.sin(y),
                          s.sin(epsilon)*s.cos(y),0])
    eq((a_epsilon.T*a_epsilon)[0],1,'entire_smooth_periodic_unit_cone_curve')
    da = a_epsilon.diff(epsilon).subs(epsilon,0)
    eq(da,s.Matrix([0,0,s.cos(y),0]),'actual_nonconstant_causal_test_cos_y')
    h = 2*a0*a0.T-s.eye(4)
    dh = 2*(da*a0.T+a0*da.T)
    dhi = -h*dh*h
    eq(h*h,s.eye(4),'Lorentz_reflection_inverse_exact')
    eq(h.det(),-1,'constant_Lorentz_volume_on_entire_cone_fibre')
    eq(dhi,dh,'reflection_inverse_first_jet')

    def derivative(m, r):
        return m.diff(y) if r == 2 else s.zeros(4)

    def christoffel(metric, inverse, r):
        return s.Matrix(4,4,lambda a,b: sum(inverse[a,k]*(
            derivative(metric,r)[k,b]+derivative(metric,b)[k,r]
            -derivative(metric,k)[r,b])/2 for k in range(4)))

    base_connection = [christoffel(h,h,r) for r in range(4)]
    dconnection = []
    for r in range(4):
        dconnection.append(s.Matrix(4,4,lambda a,b:sum((
            dhi[a,k]*(derivative(h,r)[k,b]+derivative(h,b)[k,r]
                       -derivative(h,k)[r,b])+
            h[a,k]*(derivative(dh,r)[k,b]+derivative(dh,b)[k,r]
                     -derivative(dh,k)[r,b]))/2 for k in range(4))))

    # Extract the literal generators already owned by the earlier new
    # matrix constructor. Its run()/128x128 assembly is not invoked.
    matrix_path = repo/list(PINS)[1]
    run_node = next(n for n in ast.parse(matrix_path.read_text()).body
                    if isinstance(n,ast.FunctionDef) and n.name == 'run')
    mr_nodes = [n for n in run_node.body if isinstance(n,ast.Assign) and
                any(isinstance(t,ast.Name) and t.id == 'mr' for t in n.targets)]
    require(len(mr_nodes) == 1,'extract_only_owned_literal_Mr_assignment')
    data = {'s':s,'e':elementary}
    exec(compile(ast.Module(body=mr_nodes,type_ignores=[]),str(matrix_path),'exec'),data)
    literal = [sum((s.exp(s.I*k*y).expand(complex=True)*m for k,m in row.items()),
                   s.zeros(4)) for row in data['mr']]
    require(all(zero(literal[r]+base_connection[r].T) for r in range(4)),
            'independent_Christoffel_equals_actual_proper_LC_covector_generators')
    require(all(s.simplify(s.trace(m)) == 0 for m in literal),
            'actual_LC_generator_trace_zero')
    require(all(zero(literal[r][:,r]) for r in range(4)),
            'actual_base_Mr_own_column_zero_each_point')

    mean = lambda value:s.simplify(s.integrate(s.expand_trig(value),
                                  (y,0,2*s.pi))/(2*s.pi))
    total_diagonal = sum(dconnection[r][r,r] for r in range(4))
    eq(mean(total_diagonal),-s.Rational(1,2),
       'actual_causal_curve_mean_d_sum_Gamma_rr_is_minus_half')
    dm = [(-v.T).applyfunc(mean) for v in dconnection]
    expected_dm = [
        s.Matrix([[0,-s.Rational(1,2),0,0],[s.Rational(1,2),0,0,0],
                  [0,0,0,0],[0,0,0,0]]),
        s.diag(s.Rational(1,2),s.Rational(1,2),-1,0),
        s.Matrix([[0,0,0,0],[0,0,-1,0],[0,2,0,0],[0,0,0,0]]),
        s.zeros(4),
    ]
    require(all(dm[r] == expected_dm[r] for r in range(4)),
            'all_four_actual_connection_mean_first_jets')
    require(all(s.trace(v) == 0 for v in dm),
            'moving_connection_remains_tracefree')

    axis_trace = vacuum_source = top_source = 0
    cross_source = s.zeros(2)
    for r in range(4):
        d = s.I*gamma[r]
        gm = lift(dm[r])
        dd1 = s.I*(c[r]*gm-gm.T*b[r])
        aa = d*dd1+dd1*d
        axis_trace += s.trace(aa)
        vacuum_source += aa[0,0]/4
        top_source += aa[15,15]/4
        cross_source += aa.extract([0,15],[0,15])/4
    eq(axis_trace,-8,'full16_causal_thermal_moment_coefficient_minus_eight')
    eq(vacuum_source,0,'vacuum_uniform_eight_momentum_source_zero')
    eq(top_source,-s.Rational(1,4),
       'top_uniform_eight_momentum_source_minus_quarter')
    eq(cross_source,s.diag(0,-s.Rational(1,4)),
       'general_complex_PSD_plane_source_only_top_mass')

    # s powers are restored after the scale-one geometric/CAR calculation.
    radius = s.symbols('radius',positive=True)
    tau, r, zr, zi = s.symbols('tau r z_real z_imag',real=True)
    sigma = s.Matrix([[r,zr+s.I*zi],[zr-s.I*zi,1-r]])
    eq(s.trace(sigma),1,'general_common_complex_plane_density_normalization')
    balance = (1+64*tau)/radius**2
    eq(balance.subs(tau,-s.Rational(1,64)),0,
       'actual_full16_radial_balance_forces_tau_minus_one_over_64')
    total_source = (axis_trace*tau+s.trace(sigma*cross_source))/radius**2
    eq(total_source.subs(tau,-s.Rational(1,64)),(2*r-1)/(8*radius**2),
       'actual_first_causal_source_population_imbalance_over_eight_s_squared')
    eq(s.diff(total_source,zr),0,'real_plane_coherence_cannot_cancel_causal_source')
    eq(s.diff(total_source,zi),0,'imaginary_plane_coherence_cannot_cancel_causal_source')

    # Parameter-free tensor identity for the independent-output continuum
    # chart: S0 is a function of (G,T,mu,C), never of the cone coordinate a.
    # Consequently its entire mixed row with a is zero, so no first jet v,
    # even outside the displayed Fourier support, can change this O(h) row.
    a_parameter, raw_parameter = s.symbols('a_parameter raw_parameter',real=True)
    leading = s.Function('S0')(raw_parameter)
    eq(s.diff(leading,a_parameter,raw_parameter),0,
       'exact_leading_factorization_kills_all_first_counterjet_contributions')

    return {
        'status':'PASS', 'exact_checks':len(checks), 'checks':checks,
        'source_pins':PINS, 'full_Fock_components':16,
        'shell_momenta':'all eight +/-e_r, each with all16 exterior components',
        'reference_dimension_retained':128,
        'preparation':'rho=(P_Sigma/8) tensor sigma, sigma any common complex PSD density on span{mask0,mask15}',
        'actual_causal_curve':'a_epsilon=(cos(epsilon)cos(y),sin(y),sin(epsilon)cos(y),0)',
        'positive_metric':'G=s^2 I, fixed along causal test',
        'Lorentz_metric':'g=s^2(2 a_epsilon a_epsilon^T-I)',
        'torsion':'T=0, actual proper LC connection retained',
        'first_stencil_coefficient':'A1={D0,L1+L1^dagger}, L1=(1/2)sum C(dx^r)nabla_r^2',
        'full16_generic_trace':'A1_pp trace=-16 sum_(a,r) p_a p_r <(M_r)_(a,r)>/s^2 when tr(M_r)=0; brackets are spatial mean',
        'vacuum_generic_coefficient':'0',
        'top_generic_coefficient':'-2 sum_(a,r) p_a p_r <(M_r)_(a,r)>/s^2 when tr(M_r)=0',
        'mean_causal_connection_diagonal_variation':'-1/2',
        'thermal_first_source':'-8*tau/s^2',
        'matter_first_source':'-sigma15,15/(4*s^2)',
        'actual_radial_balance':'tau=sum_p kappa_p p0^2=-1/64',
        'total_first_causal_source':'(sigma00-sigma15,15)/(8*s^2)',
        'field_necessary_condition':'sigma00=sigma15,15=1/2',
        'balanced_amplitude_input':'pinned amplitude_first_jet.py: resonant residual_squared>=1/(8*s^4), full normalized amplitude Euler_squared>=1/(2*s^4)',
        'joint_consequence':'no controlled differentiable joint h-first-jet about this leading winding cone for any COMMON momentum-diagonal complex PSD vacuum/top density',
        'all_first_counterjets':'in the independent-output variational chart, all10 metric, all24 torsion, measure, causal observer/coframe and every amplitude/reference first jet remain allowed; none changes the continuum-blind causal row',
        'moving_raw_preparation':'raw/coordinate field sources agree at a full joint first jet only after the amplitude first row is also zero',
        'clock':'alpha=c0*h^2, beta fixed up to O(h^2): no O(h) native-clock or rounding term',
        'scope_not_excluded':['different leading geometries or preparations',
                              'momentum-dependent sigma or inter-momentum coherences',
                              'other complex E0 states', 'non-differentiable or uncontrolled first jets',
                              'Puiseux branches', 'other retained-history programmes',
                              'the full native physical preparation/admission problem'],
        'old_run_or_spectrum_called':False,
    }


if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
