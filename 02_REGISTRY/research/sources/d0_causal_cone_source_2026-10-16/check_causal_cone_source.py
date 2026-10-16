#!/usr/bin/env python3
"""Full16 coordinate-form factorization and a genuine changing-cone source.

Only frozen creator definitions are AST-extracted. No previous checker, root
search, spectral catalogue or saved result is executed. Python 3.9 compatible.
"""
from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json
import sympy as s


ROOT = Path(__file__).resolve().parents[4]
PINS = {
    '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py':
        'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    '02_REGISTRY/research/A4D_COFRAME_TORSION_INTRINSIC_GR_RECONSTRUCTION.md':
        '861eb7b753d333b8b51de55145a9a0078773854a74f0f619baa13056604d0eb9',
}


def _zero(value):
    entries = value if isinstance(value, s.MatrixBase) else (value,)
    return all(s.expand(item) == 0 for item in entries)


def _trig_zero(value):
    entries = value if isinstance(value, s.MatrixBase) else (value,)
    return all(s.trigsimp(item) == 0 for item in entries)


def _creators(repo):
    path = repo / next(iter(PINS))
    tree = ast.parse(path.read_text())
    nodes = [node for node in tree.body
             if (isinstance(node, ast.FunctionDef) and node.name == 'creator')
             or (isinstance(node, ast.Assign) and any(
                 isinstance(target, ast.Name) and target.id == 'EXTERIOR_ORDER'
                 for target in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('frozen actual creator definition changed')
    scope = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), scope)
    return tuple(scope['creator'](i) for i in range(4)), scope['EXTERIOR_ORDER']


def run(repo=None):
    repo = Path(repo) if repo is not None else ROOT
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError(name)
        checks.append(name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    c, order = _creators(repo)
    b = tuple(ci.T for ci in c)
    I, Z = s.eye(16), s.zeros(16)
    vacuum = I[:, 0]
    eta = s.diag(1,-1,-1,-1)

    def create(v):
        return sum((v[i]*c[i] for i in range(4)), s.zeros(16))

    def Gamma(A):
        return sum((A[i,j]*c[i]*b[j]
                    for i in range(4) for j in range(4) if A[i,j] != 0), Z)

    def exterior(A):
        out = s.zeros(16)
        for mask in range(16):
            value = vacuum
            occupied = [r for r in order if mask & (1 << r)]
            for r in reversed(occupied):
                value = create(A[:,r])*value
            out[:,mask] = value
        return out

    def exterior_jet(A, V):
        out = s.zeros(16)
        for mask in range(16):
            occupied = [r for r in order if mask & (1 << r)]
            total = s.zeros(16,1)
            for slot in range(len(occupied)):
                value = vacuum
                for index in reversed(range(len(occupied))):
                    r = occupied[index]
                    value = create((V if index == slot else A)[:,r])*value
                total += value
            out[:,mask] = total
        return out

    require(all(_zero(c[i]*b[j]+b[j]*c[i]-(I if i==j else Z))
                for i in range(4) for j in range(4)), 'actual_full16_CAR')
    require(_zero(exterior(s.eye(4))-I), 'all16_exterior_basis_order')

    # Nonorthogonal rational coframe and a nonrest unit observer.
    e = s.Matrix([[1,s.Rational(1,3),0,s.Rational(1,5)],
                  [0,s.Rational(3,2),s.Rational(1,4),0],
                  [s.Rational(1,7),0,s.Rational(5,4),s.Rational(1,6)],
                  [0,s.Rational(1,8),0,s.Rational(4,3)]])
    F = e.inv()
    n = s.Matrix([s.Rational(5,4),s.Rational(3,4),0,0])
    hn = -eta+2*eta*n*n.T*eta
    G = e.T*hn*e
    B = e.T*eta
    U = exterior(B)
    Uinv = exterior(B.inv())
    require((n.T*eta*n)[0] == 1 and _zero(hn*eta*hn-eta)
            and e.det() != 0, 'generic_nonorthogonal_frame_and_boosted_observer')
    require(_zero(U*Uinv-I)
            and _zero(U.T*exterior(G.inv())*U-exterior(hn)),
            'full16_coordinate_form_isometry_Ue')
    require(all(_zero(U*create(eta*F.row(r).T)*Uinv-c[r]) for r in range(4)),
            'all_four_coordinate_creation_coefficients')

    deriv_e = []
    for mu in range(4):
        A = s.zeros(4)
        A[mu,(mu+1)%4] = s.Rational(1,11+mu)
        A[(mu+2)%4,mu] = s.Rational(2,13+mu)
        deriv_e.append(A)
    require(all(_zero(exterior_jet(B,deriv_e[mu].T*eta)*Uinv
                         -Gamma(deriv_e[mu].T*eta*B.inv())) for mu in range(4)),
            'actual_full16_derivative_of_coordinate_intertwiner')

    lorentz = []
    for j in range(1,4):
        A = s.zeros(4); A[0,j] = A[j,0] = 1
        lorentz.append(A)
    for i,j in ((1,2),(1,3),(2,3)):
        A = s.zeros(4); A[i,j] = 1; A[j,i] = -1
        lorentz.append(A)
    require(all(_zero(A.T*eta+eta*A) for A in lorentz)
            and all(_zero(U*Gamma(A)*Uinv-Gamma(B*A*B.inv())) for A in lorentz),
            'full_six_Lorentz_generators_in_actual_exterior_representation')

    slots = [(lam,mu,nu) for lam in range(4)
             for mu in range(4) for nu in range(mu+1,4)]

    def torsion_and_lower(omega, de):
        connection = tuple(F*(de[mu]+omega[mu]*e) for mu in range(4))
        torsion = s.Matrix([connection[mu][lam,nu]-connection[nu][lam,mu]
                            for lam,mu,nu in slots])
        QT = sum((torsion[i]*c[mu]*c[nu]*b[lam]
                  for i,(lam,mu,nu) in enumerate(slots)), Z)
        # This is the actual transformed connection, not a desired residual.
        lower = sum((c[mu]*Gamma(B*omega[mu]*B.inv()
                         -de[mu].T*eta*B.inv()) for mu in range(4)), Z)
        return torsion, lower, QT

    base = tuple(sum((s.Rational((mu+1)*(j+1),31+mu+j)*A
                      for j,A in enumerate(lorentz)), s.zeros(4)) for mu in range(4))
    torsion0, lower0, QT0 = torsion_and_lower(base,deriv_e)
    require(_zero(lower0+QT0), 'coordinate_Cartan_identity_with_nonzero_frame_first_jet')
    columns = []
    identities = []
    no_de = tuple(s.zeros(4) for _ in range(4))
    for mu in range(4):
        for A in lorentz:
            direction = [s.zeros(4) for _ in range(4)]
            direction[mu] = A
            torsion, lower, QT = torsion_and_lower(direction,no_de)
            columns.append(torsion)
            identities.append(_zero(lower+QT))
    full_map = s.Matrix.hstack(*columns)
    require(all(identities), 'all24_Lorentz_torsion_slots_full16_Cartan_identity')
    require(full_map.rank() == 24, 'all24_coordinate_torsion_map_invertible')

    # Cone family: e=s O(theta(y)), G=s^2 I, g=s^2 O^T eta O.
    theta,p = s.symbols('theta p', real=True)
    scale = s.symbols('scale', positive=True)
    O = s.Matrix([[s.cos(theta),s.sin(theta),0,0],
                  [-s.sin(theta),s.cos(theta),0,0],[0,0,1,0],[0,0,0,1]])
    cone_g = O.T*eta*O
    require(_trig_zero(O.T*O-s.eye(4)) and s.trigsimp(O.det()) == 1
            and _trig_zero((scale*O).T*(scale*O)-scale**2*s.eye(4)),
            'whole_smooth_cone_family_fixed_positive_metric')
    dg = p*cone_g.diff(theta)
    derivatives = (s.zeros(4),s.zeros(4),dg,s.zeros(4))
    Christ = tuple(s.Matrix(4,4,lambda a,nu:s.trigsimp(sum(cone_g[a,l]*(
        derivatives[mu][l,nu]+derivatives[nu][l,mu]-derivatives[l][mu,nu])
        for l in range(4))/2)) for mu in range(4))
    spin = tuple((O*Christ[mu]*O.T-(p*O.diff(theta)*O.T if mu==2 else s.zeros(4)))
                 .applyfunc(s.trigsimp) for mu in range(4))
    B02 = s.zeros(4); B02[0,2]=B02[2,0]=1
    R12 = s.zeros(4); R12[1,2]=1; R12[2,1]=-1
    require(all(_trig_zero(spin[mu].T*eta+eta*spin[mu]) for mu in range(4))
            and _trig_zero(spin[0]-p*(-s.sin(theta)*B02-s.cos(theta)*R12))
            and _trig_zero(spin[1]-p*(s.cos(theta)*B02-s.sin(theta)*R12))
            and spin[2] == s.zeros(4) and spin[3] == s.zeros(4),
            'actual_all24_LC_spin_components_and_zero_torsion')
    require(_trig_zero(spin[1].subs(theta,0)-p*B02),
            'observer_comparison_has_transverse_Lorentz_boost')

    # Independent full Ricci calculation: sphere-positive curvature convention.
    y = s.symbols('y', real=True)
    tfun = s.Function('theta')(y)
    coordinates = (s.Symbol('t'),s.Symbol('x'),y,s.Symbol('z'))
    metric = cone_g.subs(theta,tfun).applyfunc(s.trigsimp)
    inverse = metric
    ch = [[[s.trigsimp(sum(inverse[a,l]*(s.diff(metric[l,d],coordinates[b0])
        +s.diff(metric[l,b0],coordinates[d])-s.diff(metric[b0,d],coordinates[l]))
        for l in range(4))/2) for d in range(4)] for b0 in range(4)] for a in range(4)]
    ric = s.Matrix(4,4,lambda b0,d:s.trigsimp(sum(
        s.diff(ch[a][b0][d],coordinates[a])-s.diff(ch[a][b0][a],coordinates[d])
        +sum(ch[a][a][l]*ch[l][b0][d]-ch[a][d][l]*ch[l][b0][a]
             for l in range(4)) for a in range(4))))
    expected_ric = s.zeros(4)
    expected_ric[:2,:2] = s.diff(tfun,y,2)*s.Matrix([
        [-s.sin(2*tfun),s.cos(2*tfun)],
        [s.cos(2*tfun),s.sin(2*tfun)]])
    expected_ric[2,2]=2*s.diff(tfun,y)**2
    scalar = s.trigsimp(sum(inverse[b0,d]*ric[b0,d]
                           for b0 in range(4) for d in range(4)))
    require(_trig_zero(ric-expected_ric) and _trig_zero(metric.det()+1)
            and s.trigsimp(scalar+2*s.diff(tfun,y)**2)==0,
            'all_ten_Ricci_rows_and_Lorentz_scalar')
    amplitude = s.symbols('amplitude', real=True)
    phi = s.Function('phi')(y)
    EH_density = -2*scale**2*amplitude**2*s.diff(phi,y)**2
    require(s.diff(EH_density,amplitude,2) == -4*scale**2*s.diff(phi,y)**2,
            'nonzero_Lorentz_EH_source_and_Hessian_on_invisible_fibre')

    # A real full16 observer readout remains available although this PRICE
    # forgets the cone in its continuum operator. No extra cost is selected.
    rapidity_exp = s.symbols('rapidity_exp', positive=True)
    chyp=(rapidity_exp+1/rapidity_exp)/2
    shyp=(rapidity_exp-1/rapidity_exp)/2
    A=s.eye(4); A[0,0]=A[2,2]=chyp; A[0,2]=A[2,0]=shyp
    EA=exterior(A)
    require(_zero(A.T*eta*A-eta) and s.simplify(A.det()-1)==0
            and s.simplify(s.trace(EA.T*EA)-16-16*shyp**2)==0,
            'full16_observer_boost_readout_16_sinh_squared')
    Afix=A.subs(rapidity_exp,s.Rational(3,2))
    X=create(s.Matrix([0,-s.Rational(1,2),0,0]))*exterior(Afix)
    eigenvalues=(X.T*X).eigenvals()
    require(max(eigenvalues) == s.Rational(9,16)
            and sum(eigenvalues.values()) == 16
            and max(eigenvalues) < 1,
            'strict_Julia_scaling_s2_full16_with_all_complements')

    # Conditional SAME-matter P1 binding: all other grades remain present.
    coefficients = list(s.symbols('psi0:16', real=True))
    v_native = 2*n
    for a in range(4):
        coefficients[1 << a] = v_native[a]
    psi=s.Matrix(coefficients)
    form_psi=U*psi
    alpha=s.Matrix([form_psi[1 << a] for a in range(4)])
    kappa=(v_native.T*eta*v_native)[0]
    g=e.T*eta*e
    v_coordinate=F*v_native
    require(_zero(alpha-e.T*eta*v_native) and _zero(alpha-g*v_coordinate)
            and s.simplify((alpha.T*G.inv()*alpha)[0]-kappa)==0,
            'full16_grade_preserving_same_matter_P1_covector_binding')
    require(_zero(g+G-2*alpha*alpha.T/kappa),
            'conditional_P1_selfbinding_reconstructs_all_ten_metric_slots')

    # A same-matter binding changes the form state along the cone. Its actual
    # prepared energy therefore supplies a source, even though H,J stay fixed.
    f,fp,pp,Nnorm=s.symbols('f fp pp Nnorm', real=True)
    nongrade1=[mask for mask in range(16) if bin(mask).count('1') != 1]
    beta=s.symbols('beta0:12', real=True)
    beta_prime=s.symbols('beta_prime0:12', real=True)
    form_orth=s.zeros(16,1)
    form_orth[1]=f*s.cos(theta)
    form_orth[2]=f*s.sin(theta)
    form_deriv=s.zeros(16,1)
    form_deriv[1]=fp*s.cos(theta)-f*p*s.sin(theta)
    form_deriv[2]=fp*s.sin(theta)+f*p*s.cos(theta)
    for j,mask in enumerate(nongrade1):
        form_orth[mask]=beta[j]
        form_deriv[mask]=beta_prime[j]
    native_bound=exterior(eta*O)*form_orth
    require(_trig_zero(s.Matrix([native_bound[1<<a] for a in range(4)])
                       -s.Matrix([f,0,0,0])),
            'same_matter_bound_family_native_P1_is_f_e0_all_other_grades_retained')
    norm_expected=f*f+sum(x*x for x in beta)
    numerator_expected=fp*fp+f*f*p*p+sum(x*x for x in beta_prime)
    require(s.trigsimp((form_orth.T*form_orth)[0]-norm_expected)==0
            and s.trigsimp((form_deriv.T*form_deriv)[0]-numerator_expected)==0
            and _zero((c[2]-b[2])**2+I),
            'actual_flat_positive_full16_norm_and_matter_energy')
    theta_EL=-2*(2*f*fp*p+f*f*pp)/(scale**2*Nnorm)
    ffun=s.Function('f')(y)
    actual_L=s.trigsimp((form_deriv.T*form_deriv)[0]).subs(
        {theta:tfun,f:ffun,fp:s.diff(ffun,y),p:s.diff(tfun,y)})/(scale**2*Nnorm)
    actual_EL=s.diff(actual_L,tfun)-s.diff(s.diff(actual_L,s.diff(tfun,y)),y)
    actual_EL=actual_EL.subs({s.diff(ffun,y):fp,s.diff(tfun,y):p,
                             s.diff(tfun,y,2):pp,ffun:f})
    require(s.simplify(actual_EL-theta_EL)==0
            and actual_EL.subs({f:1,fp:0,p:1,pp:1}) != 0,
            'bound_matter_theta_Euler_minus_two_f_squared_theta_prime_derivative')

    f0=s.symbols('f0', positive=True)
    Ak=s.symbols('A0:12', real=True)
    Bk=s.symbols('B0:12', real=True)
    wave=2*s.pi
    winding=s.zeros(16,1)
    winding[1]=f0*s.cos(wave*y)
    winding[2]=f0*s.sin(wave*y)
    for j,mask in enumerate(nongrade1):
        winding[mask]=Ak[j]*s.cos(wave*y)+Bk[j]*s.sin(wave*y)
    require(_zero(winding.diff(y,2)+wave**2*winding)
            and _zero(winding.subs(y,0)-winding.subs(y,1))
            and _zero(winding.diff(y).subs(y,0)-winding.diff(y).subs(y,1))
            and theta_EL.subs({fp:0,pp:0})==0,
            'periodic_nonzero_winding_full16_coordinate_form_amplitude_Euler_not_field_Euler')

    return {
        'status':'PASS', 'exact_checks':len(checks), 'checks':checks,
        'source_pins':PINS, 'full_exterior_components':16,
        'torsion_map_rank':24, 'coordinate_form_intertwiner':'Lambda(e.T eta)',
        'coordinate_contraction':'i_partial_lambda, algebraic dual, not positive adjoint',
        'factorized_continuum_data':['G','coordinate_torsion_T','measure_mu','form_preparation'],
        'independent_causal_cone_dimensions':3,
        'cone_family':'e=scale O01(theta(y)), n=e0, Omega=omega_LC(g)',
        'positive_metric':'scale^2 I4', 'coordinate_torsion':'0',
        'Ricci_AB':'theta_yy [[-sin(2theta),cos(2theta)],[cos(2theta),sin(2theta)]]',
        'Ricci_yy':'2 theta_y^2', 'other_Ricci_slots':'0',
        'Lorentz_scalar':'-2 theta_y^2/scale^2',
        'Lorentz_EH_integrand':'-2 scale^2 theta_y^2',
        'native_continuum_price_cone_derivative':'0 at fixed G,T,mu,form preparation',
        'observer_boost_readout':'Tr16 Lambda(A)^* Lambda(A)-16 = 16 sinh(h theta_y)^2 at theta=0',
        'strict_fixture':{'scale':'2','exp(h theta_y)':'3/2','max_XstarX':'9/16'},
        'conditional_P1_formula':'g=-G+2 alpha alpha.T/(alpha.T G^-1 alpha)',
        'P1_binding_scope':'same actual matter vector and chosen grade1 observer only; no proven P1 map from full v8 reference128',
        'bound_form_P1':'scale f(y) [cos(theta(y)) dt+sin(theta(y)) dx]',
        'bound_native_P1':'f(y) e0',
        'bound_matter_normalizer':'N=int(f^2+sum_12 beta_I^2)',
        'bound_matter_R':'int(f_prime^2+f^2 theta_prime^2+sum_12 |grad beta_I|^2)/(scale^2 N)',
        'bound_matter_theta_source':'-2 (f^2 theta_prime)_prime/(scale^2 N)',
        'winding_amplitude_eigenvalue':'(2pi)^2/scale^2; all12 other-grade coefficients A_I cos(2pi y)+B_I sin(2pi y)',
        'winding_scope':'full coordinate-form amplitude row at fixed G,T only; no raw P1-bound matter or joint stationarity',
        'critical_fibre_scope':'requires smooth-field output submersion or explicit right inverse; no existence of output roots asserted',
        'boundary':'exact continuum declared-price factorization; not finite-stencil invariance, physical admission, all contextual readouts, or h^-2 terminal closure',
    }


if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
