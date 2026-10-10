#!/usr/bin/env python3
"""Exact all-rank positive jets, native background curves and source controls."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sympy as s

HEAD = '20928b17563fc1d840bbc204ced7c3fd28610175'
BASE = '02_REGISTRY/research/certificates/a4d_native_positive_source'
PROOF = '02_REGISTRY/research/A4D_NATIVE_POSITIVE_SOURCE_JETS.md'
JOINT = '02_REGISTRY/research/certificates/a4d_native_joint_field_quotient_check.py'


SCOPE={
  'homogeneous_positive_source_class':'COMPLETE_COMPILED_GENUINE_DERIVATIVES',
  'positive_first_and_second_jet_class':'ANALYTIC_ALL_RANK_EXPLICIT_RECONSTRUCTION',
  'first_jet_inverse':'COMPILED_LEAN',
  'native_kernel_binding':'SUPPLIED_INSTANCE_OF_EXISTING_OWNER_NOT_SELECTED',
  'second_jet_full_theorem_compiled':False,
  'positive_primitive_cost_implies_positive_effective_action':False,
  'one_point_positivity_suffices':False,
  'one_sided_domain_suffices':False,
  'nonzero_kernel_matter_removed':False,
  'kernel_is_gauge':False,
  'operator_jet_zero_at_kernel_root':False,
  'constant_rank_required_for_exact_source_zero':False,
  'zero_source_implies_root_recovery':False,
  'operator_value_bound_supplies_action_jet_bound':False,
  'small_residual_alone_implies_small_source':False,
  'point_source_alone_justifies_contrast_limit':False,
  'coordinate_axis_second_jets_supply_common_positive_family':False,
  'all_nonhomogeneous_matter_actions_excluded':False,
  'Lorentz_indefinite_action_is_positive':False,
  'new_native_action_or_constraint_installed':False,
  'physical_matter_source_selected':False,
  'physical_Ward_derived':False,
  'G0_closed':False,
  'positive_GR':False,
  'whole_core_no_go':False,
  'original_parent_terminals_changed':False,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
    checks = []
    if args.expect:
        assert json.loads(args.expect.read_text())['scope']==SCOPE,'PINNED_LEDGER_MISMATCH'

    def check(name, value):
        assert bool(value), name
        checks.append(name)

    receipt = json.loads((root/(BASE+'_results.json')).read_text())
    check('COMPILED_18_GENUINE_DECLARATIONS', receipt['status'] == 'PASS'
          and receipt['compiler_exit_code'] == 0 and receipt['owner_input_head'] == HEAD
          and receipt['printed_axiom_dependencies'] == 18 and not receipt['sorryAx'])
    pins = {**receipt['transitive_d0_source_sha256'], **receipt['toolchain_input_sha256'],
            receipt['capsule']: receipt['capsule_sha256'], receipt['output']: receipt['output_sha256']}
    check('ALL_NATIVE_TOOLCHAIN_CAPSULE_OUTPUT_PINS', all(sha(p) == h for p, h in pins.items()))
    out = (root/receipt['output']).read_text()
    check('CLEAN_STANDARD_AXIOMS', set(receipt['axioms']) <= {'propext','Classical.choice','Quot.sound'}
          and not any(x in out for x in ['error:', 'warning:', 'sorryAx']))
    for name in ['homogeneous_nonnegative_full_root_source','quad_full_field_gate_iff_kernel',
                 'arbitrary_positive_quadratic_source_zero','owned_source_zero',
                 'first_jet_reconstruction','two_sided_positive_source_bound']:
        check('RESOLVED_PROPOSITION_'+name, "'D0.Research.NativePositiveSource."+name+"' depends on axioms:" in out
              and '\nD0.Research.NativePositiveSource.'+name in out)
    spec = importlib.util.spec_from_file_location('native_joint', root/JOINT)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    t = s.Symbol('t', real=True)
    ranks = []
    for r in range(5):
        k = 4-r
        A = s.diag(*([s.Integer(i+1) for i in range(r)]+[s.Integer(0)]*k))
        P = s.diag(*([1]*r+[0]*k))
        G = s.diag(*([s.Rational(1,i+1) for i in range(r)]+[0]*k))
        Q = s.eye(4)-P
        B = s.Matrix(4,4,lambda i,j:s.Rational(i+j+1,7) if i<r or j<r else 0)
        X = G*B-G*B*P/2
        check('RANK_'+str(r)+'_COMPLETE_FIRST_JET_INVERSE', Q*B*Q == s.zeros(4)
              and A*X+X.T*A == B and A*G == P and G*A == P)
        T = s.Matrix(4,4,lambda i,j:s.Rational(i+j+2,11) if i<r or j<r else 0)
        S = s.diag(*([0]*r+[s.Integer(i+1) for i in range(k)]))
        C = 2*X.T*A*X+T+S
        Y = G*T-G*T*P/2
        R = s.eye(4)+t*X+t*t*Y/2
        M = R.T*A*R+t*t*S/2
        check('RANK_'+str(r)+'_ACTUAL_FIRST_AND_SECOND_DERIVATIVES',
              M.subs(t,0)==A and M.diff(t).subs(t,0)==B and M.diff(t,2).subs(t,0)==C)
        check('RANK_'+str(r)+'_COMPLETE_SECOND_JET_SCHUR_CONDITION', Q*(C-2*B*G*B)*Q == S)
        z = s.Matrix([0]*r+[1]*k)
        check('RANK_'+str(r)+'_FULL_FIELD_ROOT_AND_FIXED_FIELD_SOURCE', A*z == s.zeros(4,1)
              and (z.T*M*z)[0].diff(t).subs(t,0) == 0)
        pairs = list(itertools.combinations_with_replacement(range(4),2))
        rank_map = []
        for i in range(4):
            for j in range(4):
                Z=s.zeros(4);Z[i,j]=1
                W=A*Z+Z.T*A
                rank_map.append(s.Matrix([W[a,b] for a,b in pairs]))
        dim = s.Matrix.hstack(*rank_map).rank()
        check('RANK_'+str(r)+'_FIRST_JET_DIMENSION', dim == 10-k*(k+1)//2)
        at = M.subs(t,s.Rational(1,97))
        check('RANK_'+str(r)+'_POSITIVE_REALIZATION_AND_RANK_CHANGE', A.rank()==r
              and at.rank()==4 and all(at[:j,:j].det()>0 for j in range(1,5)))
        if k:
            badB=B+s.diag(*([0]*3+[1]))
            check('RANK_'+str(r)+'_REJECT_NONZERO_KERNEL_FIRST_JET', (z.T*badB*z)[0]>0
                  and (z.T*(A-s.Rational(1,97)*badB)*z)[0]<0)
            badM=R.T*A*R-t*t*Q/2
            witness=R.subs(t,s.Rational(1,97)).inv()*s.eye(4)[:,3]
            check('RANK_'+str(r)+'_REJECT_INVALID_SECOND_JET',
                  (witness.T*badM.subs(t,s.Rational(1,97))*witness)[0]<0)
        if r and k:
            check('RANK_'+str(r)+'_KERNEL_TO_RANGE_JET_NOT_ZERO', B*z != s.zeros(4,1))
        ranks.append({'rank':r,'kernel':k,'first_jet_dimension':dim,'realized_nearby_rank':at.rank()})

    H = s.Matrix([[-2+t,t],[t,0]])
    alpha = s.Rational(1,4)+t*t
    kernel = s.eye(2)+H+alpha*H*H
    z = s.Matrix([1,0])
    check('LITERAL_OWNER_NONZERO_QUARTER_ROOT', kernel.subs(t,0)*z==s.zeros(2,1)
          and z!=s.zeros(2,1))
    check('LITERAL_OWNER_MOVING_KERNEL_ZERO_SOURCE_NONZERO_OPERATOR_JET',
          (z.T*kernel*z)[0].diff(t).subs(t,0)==0 and kernel.diff(t).subs(t,0)*z!=s.zeros(2,1))
    v=s.Matrix([s.Symbol('v0'),s.Symbol('v1')])
    direct=(v.T*kernel*v)[0]
    square=((v+H*v/2).T*(v+H*v/2))[0]+(alpha-s.Rational(1,4))*((H*v).T*(H*v))[0]
    check('LITERAL_OWNER_COMPLETED_SQUARE',s.expand(direct-square)==0)

    # Actual joint raw/Lorentz/exterior carrier. The supplied kernel binding
    # is a test instance of the existing action, not a selected native law.
    eta=s.diag(1,-1,-1,-1)
    packed=list(itertools.combinations_with_replacement(range(4),2))
    sym16=[]
    for i,j in itertools.combinations_with_replacement(range(16),2):
        K=s.zeros(16);K[i,j]=K[j,i]=1;sym16.append(K)
    S0=s.zeros(16)
    for i in range(8):
        a,b=2*i,2*i+1
        S0[a,a]=S0[b,b]=s.Rational(1,2)
        S0[a,b]=S0[b,a]=s.Rational(-1,2)
    psi=s.ones(16,1)
    check('NONEMPTY_ALL16_NONZERO_KERNEL_MATTER',S0*psi==s.zeros(16,1)
          and all(x!=0 for x in psi) and S0.rank()==8)
    directions=[]
    for i,j in packed:
        V=s.zeros(4);V[i,j]=V[j,i]=1
        directions.append(('metric_'+str(i)+str(j),V*eta,None,None))
    for e in range(4):
        for i,j in itertools.combinations(range(4),2):
            gen=s.zeros(4);gen[i,j]=1;gen[j,i]=-eta[i,i]/eta[j,j]
            directions.append(('link_'+str(e)+'_'+str(i)+str(j),s.zeros(4),e,gen))
    check('TEN_METRIC_AND_ALL24_ACTUAL_LORENTZ_LINK_CURVES',len(directions)==34)
    for name,dF,edge,gen in directions:
        F=s.eye(4)+t*dF
        links=[s.eye(4) for _ in range(4)]
        if edge is not None:
            links[edge]=(s.eye(4)-t*gen/2).inv()*(s.eye(4)+t*gen/2)
            assert s.simplify(links[edge]*eta*links[edge].T-eta)==s.zeros(4)
        center=s.Matrix(4,4,lambda r,a:(F[r,a]+links[r][r,a])/2)
        centered_metric=center*eta*center.T
        if edge is None:
            check('ACTUAL_PHYSICAL_METRIC_NORMALIZATION_'+name,
                  centered_metric.diff(t).subs(t,0)==dF*eta)
        q=F*eta*F.T
        D=[U*F.inv() for U in links]
        assert all(s.simplify(d*q*d.T-eta)==s.zeros(4) for d in D)
        coords=[q[i,j]-eta[i,j] for i,j in packed]
        coords += [x for d in D for x in list(d-s.eye(4))]
        St=S0+sum((c*K for c,K in zip(coords,sym16)),s.zeros(16))
        mt=native.exterior(F)*psi
        residual=St*mt
        E=sum(x*x for x in residual)/2
        check('ACTUAL_JOINT_SOURCE_'+name, residual.subs(t,0)==s.zeros(16,1)
              and s.simplify(E.diff(t).subs(t,0))==0 and St.diff(t).subs(t,0)!=s.zeros(16))
    a,b=s.Rational(5,4),s.Rational(3,4)
    boost=s.Matrix([[a,b,0,0],[b,a,0,0],[0,0,1,0],[0,0,0,1]])
    offshell=s.Matrix(range(1,17))
    shifted=native.exterior(boost.inv())*offshell
    before=(offshell.T*S0*S0*offshell)[0]/2
    after=(shifted.T*native.exterior(boost).T*S0*S0*native.exterior(boost)*shifted)[0]/2
    check('NONZERO_OFFSHELL_ACTION_NATIVE_FRAME_COVARIANCE',before>0 and before==after)
    P4=s.Matrix(4,4,lambda i,j:i*j+1)
    V4=s.Matrix(4,4,lambda i,j:i+j+1)
    check('PACKED_DUAL_WEIGHTS_ALL_TEN_METRIC_COMPONENTS',s.trace(P4.T*V4)
          ==sum((1 if i==j else 2)*P4[i,j]*V4[i,j] for i,j in packed))

    g,zs=s.symbols('g z',real=True)
    for p in [2,4,6]:
        I=(1+g*g)*(zs*zs)**(p//2)
        check('DEGREE_'+str(p)+'_GENUINE_RADIAL_IDENTITY', s.expand(zs*s.diff(I,zs)-p*I)==0)
    indefinite=g*zs*zs
    check('ONE_POINT_POSITIVITY_AND_ONE_SIDED_DOMAIN_ARE_INSUFFICIENT',
          s.diff(indefinite,zs).subs({g:0,zs:1})==0 and s.diff(indefinite,g).subs({g:0,zs:1})==1)
    nonhom=(1+g)*zs*zs*((zs*zs-2)**2+1)
    check('NONHOMOGENEOUS_NONNEGATIVE_FULL_ROOT_CAN_HAVE_SOURCE',
          s.diff(nonhom,zs).subs({g:0,zs:1})==0 and nonhom.subs({g:0,zs:1})==2
          and s.diff(nonhom,g).subs({g:0,zs:1})==2)
    constrained=(1+g)*zs*zs/2
    check('NORMALIZED_FIELD_EXCLUDES_RADIAL_FULL_GATE',s.diff(constrained,zs).subs({g:0,zs:1})==1
          and s.diff(constrained,g).subs({g:0,zs:1})==s.Rational(1,2))
    u=s.Symbol('u',real=True)
    check('GLOBAL_RATIONAL_POSITIVE_WEIGHT_BOUND',s.expand((1+u*u)+2*u-(u+1)**2)==0
          and s.expand((1+u*u)-2*u-(u-1)**2)==0)
    h=s.Symbol('h',positive=True)
    w=h*h*(2+2*(g/(h*h))/(1+(g/(h*h))**2))
    fast=w*zs*zs/2
    raw_metric_curve=s.diag(s.sqrt(1+g),1,1,1)
    scalar_matter=s.eye(16)[:,0]
    native_counter_carrier=(raw_metric_curve*eta*raw_metric_curve.T==s.diag(1+g,-1,-1,-1)
        and native.exterior(raw_metric_curve)*scalar_matter==scalar_matter)
    check('BOUNDED_POSITIVE_VALUES_SMALL_FIELD_RESIDUAL_NONZERO_SOURCE',
          s.diff(fast,zs).subs({g:0,zs:1})==2*h*h and fast.subs({g:0,zs:1})==h*h
          and s.diff(fast,g).subs({g:0,zs:1})==1 and native_counter_carrier)
    check('FAILED_UNIFORM_SECOND_DERIVATIVE_BOUND',s.simplify(s.diff(fast,g,2).subs({g:h*h,zs:1}))==-1/(2*h*h))
    eps=s.Symbol('eps',positive=True)
    contrast=(fast.subs({g:eps,zs:1})-fast.subs({g:-eps,zs:1}))/2
    check('POINT_SOURCE_DOES_NOT_CONTROL_FINITE_HALF_CONTRAST',
          s.simplify(contrast-eps/(1+eps*eps/h**4))==0)
    nn=s.Symbol('n',positive=True,integer=True)
    normalized=s.simplify((contrast/eps).subs({h:nn**-3,eps:nn**-1}))
    check('EPSILON_H_ONE_THIRD_NORMALIZED_CONTRAST_VANISHES',
          normalized==1/(1+nn**10) and s.limit(normalized,nn,s.oo)==0)
    check('ONE_PARAMETER_AXIS_JETS_DO_NOT_PROVE_COMMON_SECOND_JET',
          (s.Matrix([[2,4],[4,2]])*s.Matrix([1,-1])).dot(s.Matrix([1,-1]))<0)
    E=s.Rational(1,8);K=s.Integer(1);step=s.Rational(1,2)
    check('TWO_SIDED_TAYLOR_BOUND_SHARP_CONTROL',E/step+K*step/2==s.sqrt(2*K*E)==s.Rational(1,2))

    scope=SCOPE

    payload={'status':'PASS_NATIVE_POSITIVE_SOURCE_JETS','input_head':HEAD,
      'inputs_sha256':{p:sha(p) for p in [PROOF,JOINT,
          '02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md',
          '02_REGISTRY/research/A4D_NATIVE_PARENT_SOURCE_BOUNDARY.md']},
      'checker_sha256':sha(BASE+'_check.py'),'lean_receipt_sha256':sha(BASE+'_results.json'),
      'compiled_declarations':18,'transitive_native_pins':len(receipt['transitive_d0_source_sha256']),
      'rank_strata':ranks,'checks':checks,'scope':scope}
    encoded=json.dumps(payload,sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(encoded)
    else:
        expect=args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expect.read_text())==payload,'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_POSITIVE_SOURCE_JETS',len(checks),'controls',payload['transitive_native_pins'],'D0 pins',flush=True)


if __name__=='__main__':main()
