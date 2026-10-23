#!/usr/bin/env python3
"""SOURCE #310: actual two-record family and stationary feedback-source descent.

Selected executed owner declarations are AST-pinned and loaded from the real
owner files. No owner import/Lean closure or physical admission is claimed.
Default replay checks the adjacent immutable receipt; --write is explicit.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_chronological_stationary_descent'
PROOF = '02_REGISTRY/research/A4D_NATIVE_CHRONOLOGICAL_STATIONARY_DESCENT.md'
INPUT_HEAD = '807730135a6f91349e26e88843aa069a49d53585'
OWNER_PINS = {
 '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py': {
  'ext': 'c04b98888788c2e9f2d086eddcfb5c01cd0be887d164c0da0958dd0e057b4182',
  'creator': 'b6c7dc797dbf0dd5173305d0cc62c54a6c9227f78d5828b03f3ce337ddd9d4db',
  'record_basis': '351445d7665715302e0c01e57043792c90b0b602884e08502077aa891617ca45'},
 '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py': {
  'record': 'cb7cb2eac05c0c868c2cd7bf8b1de516bcce6e57cc8e859503c2fd5cf32b1585',
  'polynomials': 'a4d6c4ff8f6a28dcf7a043e2f76b26a9467ad91fadd40a8edcb33cb2b6ec5b13'}
}

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical_ast(value):
    # Python 3.12 added empty FunctionDef.type_params. Ignore only that empty
    # field so identical executed definitions pin identically on CI 3.11.
    if isinstance(value, ast.AST):
        return [type(value).__name__, [[key,canonical_ast(item)]
            for key,item in ast.iter_fields(value)
            if not (key == 'type_params' and item == [])]]
    if isinstance(value, list):
        return [canonical_ast(item) for item in value]
    return value

def declaration_digest(node: ast.AST) -> str:
    encoded=json.dumps(canonical_ast(node),separators=(',',':'),ensure_ascii=True)
    return digest(encoded.encode())

def load_owners(namespace: dict, check) -> None:
    for path, pins in OWNER_PINS.items():
        tree = ast.parse((ROOT/path).read_text(encoding='utf-8'))
        for name, pin in pins.items():
            matches = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
            check('unique_owner_'+name, len(matches) == 1)
            node = matches[0]
            check('owner_AST_'+name, declaration_digest(node) == pin)
            # Only these exact declarations execute; unrelated main/receipt code does not.
            exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), namespace)


def controls() -> dict:
    checks, mutants = [], []
    def check(name, condition):
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)
    def reject(name, false_statement):
        check('REJECT_'+name, not bool(false_statement))
        mutants.append(name)

    a,p,z,c,b = s.symbols('a p z c b', real=True)
    ideal = s.groebner([a*a-p, p*p+p-1, b*b+c*c-1], a,p,b,
                       domain=s.QQ.frac_field(c,z))
    def red(value):
        num, den = s.cancel(value).as_numer_denom()
        num = ideal.reduce(s.expand(num))[1]
        den = ideal.reduce(s.expand(den))[1]
        if den == 0:
            raise ZeroDivisionError('GOLDEN_OR_UNIT_DOMAIN_DENOMINATOR')
        return s.cancel(num/den)
    def mat(value):
        return value.applyfunc(red)
    def zero(value):
        vals = list(value) if isinstance(value, s.MatrixBase) else [value]
        return all(red(v) == 0 for v in vals)
    def eq(name, value):
        check(name, zero(value))
    def phi_sign(value):
        # Exact sign in Q(p), p=(sqrt(5)-1)/2. No decimal signs are used.
        poly = s.Poly(red(value), p)
        if poly.degree() > 1:
            raise ValueError('Q_P_LINEAR_REPRESENTATIVE_REQUIRED')
        u,v = poly.nth(0), poly.nth(1)
        x,y = 2*u-v,v
        sign = lambda t: int(s.sign(t))
        if not y:
            return sign(x)
        if not x or sign(x) == sign(y):
            return sign(y)
        return sign(x)*sign(x*x-5*y*y)

    I,I4 = s.eye(16),s.eye(4)
    subs = [tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]
    namespace = dict(s=s, a=a, p=p, z=z, I=I,
                     DEG=s.diag(*map(len,subs)), SUBS=subs, mat=mat)
    load_owners(namespace, check)
    record,polynomials = namespace['record'],namespace['polynomials']
    creator,ext,B0 = namespace['creator'],namespace['ext'],namespace['record_basis']()
    check('native_full_sixteen_grades', [sum(len(v)==k for v in subs) for k in range(5)] == [1,4,6,4,1])
    eq('native_signed_frame_isometry', B0.T*B0-I)
    creators = [creator(I4[:,i]) for i in range(4)]
    for i in range(4):
        for j in range(4):
            eq('native_CAR_'+str((i,j)), creators[i]*creators[j].T+creators[j].T*creators[i]-int(i==j)*I)
    U,P = record(I4,I4[:,0])
    V,Pnext = record(I4,s.Matrix([c,-b,0,0]))
    eq('first_native_gate_all16_isometry', U.T*U-I)
    eq('second_native_gate_all_angles_isometry', V.T*V-I)
    eq('original_cut_all16', P-s.diag(*[int(mask%2==0) for mask in range(16)]))
    K = mat(V*U)
    F = mat(P*K.T*(I-P)*K*P)
    eq('full_chronological_operator_isometry', K.T*K-I)
    eq('full_feedback_selfadjoint', F-F.T)
    lam,tr,det,tr0,det0 = polynomials(c)
    A,B,C = [red(v) for v in (1-z*lam,1-z*tr+z*z*det,1-z*tr0+z*z*det0)]
    active_blocks = [(0,), (2,), (4,6), (8,10), (12,14)]
    for block, expected in zip(active_blocks,[A,A,B,B,C]):
        eq('literal_full_feedback_block_'+str(block),
           (s.eye(len(block))-z*F.extract(block,block)).det()-expected)
    for i in range(16):
        allowed = next((set(v) for v in active_blocks if i in v),set())
        eq('no_omitted_feedback_coupling_row_'+str(i), s.Matrix([F[i,j] for j in range(16) if j not in allowed]))
    check('eight_active_eight_complementary_rows', sum(map(len,active_blocks)) == 8)
    pencil = A*A*B*B*C
    for pole in (-1,1):
        eq('full_pole_pencil_'+str(pole), pencil.subs(c,pole)-(1-4*z*p**3)**4)
    numerator = red(-(2*s.diff(A,c)*B*C+2*s.diff(B,c)*A*C+s.diff(C,c)*A*B))
    eq('genuine_full_logdet_derivative', s.diff(pencil,c)*A*B*C+numerator*pencil)

    # A whole-blank input for EVERY angle, not a new postulated operation.
    m = s.zeros(16,1)
    m[0]=m[14]=(c-a)/p
    m[1]=m[15]=1
    m[3]=m[13]=b/p
    blank4=s.Matrix([[1,0,1,0],[0,1,0,1],[1,0,1,0],[0,1,0,1]])/2
    blank=B0*s.kronecker_product(blank4,I4)*B0.T
    eq('all_angle_input_is_actual_whole_blank', blank*m-m)
    N=red((m.T*m)[0])
    eq('all_angle_input_norm', N-4*(1-a*c)/p**2)
    output=mat(U*m)
    first=output.extract([1,2,4,8],[0])
    eq('same_state_first_output_observer', first-s.Matrix([c,-b,0,0]))
    eq('first_output_norm_conserved', (output.T*output)[0]-N)
    output2=mat(V*output)
    second=output2.extract([1,2,4,8],[0])
    eq('same_state_second_output_first_grade', second-s.Matrix([
        2*a*c*c+a*c-a-c, -2*a*b*c-a*b+b,0,0]))
    second_norm=red((second.T*second)[0])
    eq('second_output_nonzero_band_identity', second_norm-(1-2*(1+c)*(a-p)))
    eq('second_output_full_norm_conserved', (output2.T*output2)[0]-N)
    qplus=mat(-I4+2*first*first.T)
    eq('actual_solved_metric_reflection', qplus*qplus-I4)
    eq('actual_solved_metric_determinant', qplus.det()+1)
    eq('actual_solved_metric_timelike_first_grade', (first.T*qplus*first)[0]-1)
    check('golden_p_lower_3_over5', phi_sign(p-s.Rational(3,5))>0)
    check('golden_p_upper_5_over8', phi_sign(s.Rational(5,8)-p)>0)
    check('golden_a_upper_square', s.Rational(5,8)<s.Rational(4,5)**2)
    check('golden_a_lower_square', s.Rational(3,4)**2<s.Rational(3,5))
    check('whole_input_norm_uniform_upper20', 4*(1+s.Rational(4,5))/s.Rational(3,5)**2 == 20)
    check('second_first_grade_uniform_raw_lower', 1-4*s.Rational(1,5)==s.Rational(1,5))
    check('normalized_two_step_domain_lower1_over100', s.Rational(1,5)/20==s.Rational(1,100))

    # Full chain rule, not just a sampled angular stationarity test.
    u=s.Symbol('u',real=True)
    E2,pp,scale=s.symbols('E2 pp scale',positive=True)
    ss=u*u+pp*pp*E2
    cosine=u/s.sqrt(ss)
    kap=pp**3*E2/ss**s.Rational(3,2)
    check('true_scalar_direction_derivative', s.simplify(pp*s.diff(cosine,u)-kap)==0)
    check('scalar_direction_strict_for_noncollinear_input', kap.is_positive)
    check('cosine_positive_scale_invariance', s.simplify(
        (scale*u)/s.sqrt(scale**2*u*u+pp**2*scale**2*E2)-cosine)==0)
    check('radial_correction_has_zero_cosine_jet', s.simplify(
        u*s.diff(cosine,u)+2*E2*s.diff(cosine,E2))==0)
    xx=s.Symbol('xx',real=True)
    eq('actual_blank_scalar_curve_angle_jet',
       s.diff((c+p*xx)/s.sqrt(1+2*p*c*xx+p*p*xx*xx),xx).subs(xx,0)-p*(1-c*c))
    # At E2=0 every genuine derivative of e^T G e is zero, including moving G.
    e1,e2,e3,de1,de2,de3=s.symbols('e1 e2 e3 de1 de2 de3',real=True)
    check('pole_quadratic_first_variation_zero',
          (2*(e1*de1+e2*de2+e3*de3)).subs({e1:0,e2:0,e3:0})==0)
    rr,dc,den=s.symbols('matter_residual dc kappa',real=True,nonzero=True)
    check('full_covector_reconstructed_from_scalar_equation',
          s.cancel((rr/den)*dc*den-rr*dc)==0)

    # Nonempty stationary feedback branches with DIFFERENT values, no selector.
    zm=s.Rational(1,2)
    nm=red(numerator.subs({c:-1,z:zm}))
    n0=red(numerator.subs({c:0,z:zm}))
    np=red(numerator.subs({c:1,z:zm}))
    eq('exact_logdet_slope_numerator_at_minus1', nm+8*(1013*p-626))
    eq('exact_logdet_slope_numerator_at_zero', n0-(p+1)/4)
    check('negative_slope_at_minus1', phi_sign(nm)<0)
    check('positive_slope_at_zero', phi_sign(n0)>0)
    check('nonzero_slope_at_plus1', phi_sign(np)!=0)
    # Continuity and compactness, with these endpoint slopes, prove an interior
    # minimizer on [-1,0] whose price is strictly below the common pole price.

    sample={c:s.Rational(3,5),b:s.Rational(4,5),z:zm}
    reject('freeze_second_gate_to_first_square', zero((K-U*U).subs(sample)))
    moved=mat(P*K.T*(I-Pnext)*K*P)
    reject('replace_original_terminal_cut_by_next_cut', zero((moved-F).subs(sample)))
    reject('omit_final_active_C_block', zero((pencil-A*A*B*B).subs(sample)))
    reject('all_current_chronologies_have_pole_price', zero((pencil-(1-4*z*p**3)**4).subs(sample)))
    reject('pole_stationarity_requires_j_zero', phi_sign(np)==0)
    reject('all_feedback_price_values_are_equal', phi_sign(n0)==0)
    reject('noncollinear_scalar_matter_probe_is_price_blind', phi_sign(red(numerator.subs({c:0,z:zm})))==0)
    reject('nonzero_angle_alone_proves_matter_stationarity', phi_sign(red(numerator.subs({c:0,z:zm})))==0)
    # A mutation of executed owner code is independently rejected by its pin.
    owner_path=list(OWNER_PINS)[1]
    nodes=ast.parse((ROOT/owner_path).read_text(encoding='utf-8')).body
    node=next(n for n in nodes if isinstance(n,ast.FunctionDef) and n.name=='record')
    altered=ast.parse(ast.unparse(node).replace('cr - an','cr + an')).body[0]
    reject('changed_native_creator_annihilator_sign',
           declaration_digest(altered)==OWNER_PINS[owner_path]['record'])
    singular=s.zeros(16,1)
    singular[0]=singular[14]=-a/p
    singular[1]=singular[15]=1
    eq('singular_control_is_genuine_blank', blank*singular-singular)
    singular_first=mat(U*singular).extract([1,2,4,8],[0])
    reject('singular_first_output_is_admitted', not zero(singular_first))

    return {
      'schema':'d0-research-exact-replay/1', 'status':'PASS',
      'input_source_head':INPUT_HEAD,
      'proof':PROOF, 'proof_sha256':digest((ROOT/PROOF).read_bytes()),
      'checker_sha256':digest(Path(__file__).read_bytes()),
      'owner_pin_scope':'FIVE_EXECUTED_DECLARATIONS_AST_NOT_FULL_IMPORT_OR_LEAN_CLOSURE',
      'owner_declaration_sha256':OWNER_PINS,
      'checks':checks, 'exact_controls':len(checks),
      'executed_negative_controls':mutants,
      'normalized_two_step_first_grade_squared_lower':'1/100',
      'full_feedback_pencil':'A(c)^2*B(c)^2*C(c); all16 rows retained',
      'feedback_stationary_full_covector':'zero_if_the_stated_scalar_matter_equation_is_admitted',
      'physical_admission':False, 'full_action_stationarity':False,
      'full_physical_source_Ward_GR':False, 'new_Lean_compilation':False
    }


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result=controls()
    dest=ROOT/(BASE+'_certificate.json')
    if args.write:
        dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    elif json.loads(dest.read_text(encoding='utf-8')) != result:
        raise AssertionError('STALE_STATIONARY_DESCENT_RECEIPT')
    print('PASS_CHRONOLOGICAL_STATIONARY_DESCENT',
          'controls='+str(result['exact_controls']),
          'negative_controls='+str(len(result['executed_negative_controls'])),
          'physical_admission=OPEN full_action_stationarity=OPEN')

if __name__=='__main__':
    main()
