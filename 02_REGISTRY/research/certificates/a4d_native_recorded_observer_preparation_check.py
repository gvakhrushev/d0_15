#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=360
"""Replay a recorded-state observer component and its full finite heat test."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import sympy as s

ROOT = None
BASE = '02_REGISTRY/research/certificates/a4d_native_recorded_observer_preparation'
PROOF = '02_REGISTRY/research/A4D_NATIVE_RECORDED_OBSERVER_PREPARATION.md'
HEAD = '80462afde4668fc822a01a70c2e571ce36ecd64e'
NS = 'D0.Research.RecordedObserverPreparation.'
SCOPE = {
    'explicit_density_readout_full_real_faithful_sector': True,
    'actual_retained_state_sets_existing_observer_argument': True,
    'normalized_actual_gate_curve_and_nonzero_pairing_derivative': True,
    'full_sixteen_grade_heat_binding_test_analytic': True,
    'finite_high_temperature_nonstationarity_with_zero_remainder': True,
    'whole_gate_interface_faithful_or_uniformly_elliptic': False,
    'readout_null_archive_directions_discarded_or_declared_gauge': False,
    'Pauli_role_readout_or_heat_pairing_physically_admitted': False,
    'all_ten_metric_components_or_24_link_equations_solved': False,
    'high_temperature_bound_is_fixed_beta_refinement_theorem': False,
    'native_F_source_Ward_joint_stationarity_or_GR_derived': False,
    'T0_T3_44_nodes_or_original_parent_terminal_closed': False,
}
SOURCES = [
    '03_FORMALIZATION/D0/Core/DyadABCD.lean',
    '03_FORMALIZATION/D0/Core/Phi.lean',
    '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
    '03_FORMALIZATION/D0/Representation/GoldenRelativeChannel.lean',
    '03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean',
    '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
    '03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean',
    '02_REGISTRY/research/A4D_NATIVE_MODULAR_PREPARATION_BOUNDARY.md',
    '02_REGISTRY/research/A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md',
    '02_REGISTRY/research/certificates/a4d_native_positive_heat_radial_balance_results.json',
    '02_REGISTRY/research/certificates/a4d_native_positive_heat_radial_balance.lean',
    '02_REGISTRY/research/certificates/a4d_native_composed_feedback_dynamics.lean',
    '02_REGISTRY/research/certificates/a4d_native_weighted_dirac_boundary.lean',
]
TOOLCHAIN = ['03_FORMALIZATION/'+n for n in ['lean-toolchain','lakefile.lean','lake-manifest.json']]
OWNERS = [
    'D0.Representation.GoldenCoherentMemory.blank_record_evolution',
    'D0.Geometry.observerMetric_posDef',
    'D0.Geometry.observerExteriorBladeGram_pos',
]


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def simp(matrix):
    return matrix.applyfunc(s.simplify)


def mathematics():
    checks = {}

    def ck(name, condition):
        assert bool(condition), name
        checks[name] = checks.get(name, 0)+1

    p = (s.sqrt(5)-1)/2
    a = s.sqrt(p)
    eta = s.diag(1,-1,-1,-1)
    ck('golden_relations', s.simplify(p+p**2-1)==0 and s.simplify(a**2-p)==0)
    ck('quantitative_faithful_sector_brackets', s.Rational(3,5)<p<s.Rational(5,8)
       and s.Rational(3,4)<a<s.Rational(4,5))
    U = s.Matrix([[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]])
    ck('literal_full_gate', simp(U.T*U)==s.eye(4))

    def rho(psi):
        return simp(s.Matrix(2,2,lambda i,j: sum(psi[2*i+k]*psi[2*j+k] for k in range(2))))

    def current(r):
        return s.Matrix([r.trace(),2*r[0,1],0,r[0,0]-r[1,1]])

    def form(j):
        k = (j.T*eta*j)[0]
        return simp(-eta+2*(eta*j)*(eta*j).T/k)

    aa,bb,cc,dd = s.symbols('alpha beta gamma delta',real=True)
    psi = s.Matrix([aa,bb,cc,dd])
    j = current(rho(psi))
    ck('generic_full_real_state_determinant', s.expand((j.T*eta*j)[0]-4*(aa*dd-bb*cc)**2)==0)
    x,y,z,w = s.symbols('x y z w',real=True)
    jc = s.Matrix([x+y,2*z,-2*w,x-y])
    ck('complex_coordinate_identity_only', s.expand((jc.T*eta*jc)[0]-4*(x*y-z*z-w*w))==0)
    golden = simp(U*s.Matrix([1,0,0,0]))
    rg = rho(golden)
    ck('actual_tensor_reduction', simp(rg-s.diag(p,p**2))==s.zeros(2))
    jg = current(rg)
    ck('declared_role_order_current', simp(jg-s.Matrix([1,0,0,p**3]))==s.zeros(4,1))
    hg = form(jg)
    h_expected = s.Matrix([[p+s.Rational(1,2),0,0,-s.Rational(1,2)],
                          [0,1,0,0],[0,0,1,0],[-s.Rational(1,2),0,0,p+s.Rational(1,2)]])
    ck('exact_state_derived_observer_form', simp(hg-h_expected)==s.zeros(4))
    ck('exact_observer_volume', s.simplify(hg.det())==1)
    eigenvectors = [(s.Matrix([1,0,0,1]),p),(s.Matrix([1,0,0,-1]),1/p),
                    (s.Matrix([0,1,0,0]),1),(s.Matrix([0,0,1,0]),1)]
    for vec,eig in eigenvectors:
        ck('complete_positive_observer_eigenbasis', simp(hg*vec-eig*vec)==s.zeros(4,1) and eig>0)
    for degree in range(5):
        for inds in itertools.combinations(range(4),degree):
            ck('all_exterior_blade_gram_minors', s.simplify(hg.extract(inds,inds).det())>0)

    # A diagonal faithful density gives the entire same-gate curve without radicals in t.
    hx = form(s.Matrix([1,0,0,2*x-1]))
    diag = -1+1/(2*x*(1-x))
    cross = -(2*x-1)/(2*x*(1-x))
    ck('diagonal_and_mixed_coefficients', s.simplify(hx[0,0]-diag)==0 and s.simplify(hx[0,3]-cross)==0)
    ck('entire_curve_has_constant_determinant', s.simplify(hx.det())==1)
    t = s.symbols('t',real=True)
    u = (1-t*t)/(1+t*t)
    v = 2*t/(1+t*t)
    ck('entire_input_curve_normalized', s.simplify(u*u+v*v)==1)
    curve = simp(U*s.Matrix([u,0,v,0]))
    ck('actual_curve_no_output_dropped', simp(curve-s.Matrix([a*u-p*v,0,0,p*u+a*v]))==s.zeros(4,1))
    ck('actual_curve_complete_normalization', s.simplify((curve.T*curve)[0])==1)
    xprime = s.simplify(s.diff(curve[0]**2,t).subs(t,0))
    ck('actual_density_derivative', s.simplify(xprime+4*a*p)==0)
    dh = simp(hx.diff(x).subs(x,p)*xprime)
    dp = -2*a/p**2
    cp = 2*a*(1+p**2)/p**3
    expected_dh = s.Matrix([[dp,0,0,cp],[0,0,0,0],[0,0,0,0],[cp,0,0,dp]])
    ck('all_sixteen_pairing_derivative_entries', simp(dh-expected_dh)==s.zeros(4))
    ck('nonzero_volume_preserving_shape', dh!=s.zeros(4) and s.simplify(s.trace(hg.inv()*dh))==0)
    ck('explicit_interval_lower_bounds', s.Rational(3,4)*s.Rational(99,101)-s.Rational(5,8)*s.Rational(20,101)==s.Rational(247,404)
       and s.Rational(3,5)*s.Rational(99,101)-s.Rational(4,5)*s.Rational(20,101)==s.Rational(217,505))

    # Generic differentiation includes the normalization derivative.
    j0 = s.Matrix(s.symbols('j0:4',real=True))
    variation = s.Matrix(s.symbols('v0:4',real=True))
    kval = (j0.T*eta*j0)[0]
    generic = -eta+2*(eta*j0)*(eta*j0).T/kval
    direct = generic.applyfunc(lambda e: sum(s.diff(e,j0[i])*variation[i] for i in range(4)))
    normalized = 2*((eta*variation)*(eta*j0).T+(eta*j0)*(eta*variation).T)/kval
    normalized -= 4*(j0.T*eta*variation)[0]*(eta*j0)*(eta*j0).T/kval**2
    ck('complete_generic_normalization_derivative', simp(direct-normalized)==s.zeros(4))

    bad_input = s.Matrix([a,0,-p,0])
    ck('same_gate_rank_one_boundary', simp(U*bad_input)==s.Matrix([1,0,0,0]) and s.simplify((bad_input.T*bad_input)[0])==1)
    jb = current(rho(simp(U*bad_input)))
    ck('rank_one_has_no_timelike_normalization', (jb.T*eta*jb)[0]==0)
    # Actual changed full state, same reduced current: these directions stay in the domain.
    O = s.Matrix([[0,1],[-1,0]])
    amplitude = s.Matrix(2,2,list(golden))
    changed = amplitude*O
    ck('retained_record_null_directions', changed!=amplitude and simp(changed*changed.T-rg)==s.zeros(2))
    eps = s.symbols('eps',positive=True)
    hs = hx.subs(x,1-eps**2)
    ck('unbounded_faithful_shape_eigenvalue', s.simplify(hs[0,0]-hs[0,3]-(1-eps**2)/eps**2)==0)
    ck('reciprocal_faithful_shape_eigenvalue', s.simplify(hs[0,0]+hs[0,3]-eps**2/(1-eps**2))==0)

    # Full periodic L=4 Fourier grid: all 256 modes and 16 exterior copies.
    L = 4
    roots = [s.Integer(1),s.I,s.Integer(-1),-s.I]
    zvalues = [L*(r-1) for r in roots]
    pairs = []
    for zs in itertools.product(zvalues,repeat=4):
        zz = s.Matrix(zs)
        C = s.re(zz.conjugate()*zz.T)
        lam = s.simplify(s.trace(hg*C))
        vel = s.simplify(s.trace(dh*C))
        ck('full_fourier_nonnegative_spectrum', lam>=0)
        pairs.append((lam,vel))
    mean = s.simplify(sum(vel for _,vel in pairs)/len(pairs))
    ck('full_heat_mean_derivative', s.simplify(mean-4*a*p*L**2)==0)
    ck('all_exterior_modes_remain', len(pairs)*16==4096)
    ck('spectral_norm_bound', s.simplify((-dp+cp)-4*a/p**3)==0)
    ck('spectral_norm_is_maximum_absolute_eigenvalue', dp+cp>0 and s.simplify(4*a/p**3-dp-cp)>0)
    ck('all_L_mean_identity', s.simplify(4*dp+2*cp-4*a*p)==0)
    # Exact coefficient of the analytic high-temperature estimate, no sampled beta.
    ell = s.symbols('L',positive=True)
    beta_cap = p**5/(512*ell**2)
    lower = s.simplify(4*a*p*ell**2-1024*a*ell**4/p**4*beta_cap)
    ck('quantitative_high_temperature_lower_bound', s.simplify(lower-2*a*p*ell**2)==0)
    # Coordinate traces would incorrectly treat this shape as pure trace or zero.
    ck('pairing_trace_not_coordinate_trace', s.simplify(s.trace(dh))!=0)
    return {'checks':checks,'exact_control_count':sum(checks.values()),
            'finite_Fourier_L':L,'retained_mode_count':4096,
            'heat_estimate_analytic_not_Lean':True}


def declarations():
    source = (ROOT/(BASE+'.lean')).read_text()
    return [NS+n for n in re.findall(r'^theorem (\w+)',source,re.M)]


def compile_capsule():
    cmd = ['lake','env','lean','../'+BASE+'.lean']
    run = subprocess.run(cmd,cwd=ROOT/'03_FORMALIZATION',text=True,capture_output=True)
    output = run.stdout+run.stderr
    (ROOT/(BASE+'_output.txt')).write_text(output)
    assert run.returncode==0 and ': error' not in output and ': warning' not in output, output
    names = declarations()+OWNERS
    axioms = {}
    for name in names:
        m = re.search(re.escape("'"+name+"' depends on axioms: [")+r'([^\]]*)\]',output,re.S)
        assert m, name
        axioms[name] = [n.strip() for n in m[1].split(',') if n.strip()]
        assert set(axioms[name])<={'propext','Classical.choice','Quot.sound'},name
    result = {'status':'PASS','input_head':HEAD,'command':cmd,'command_cwd':'03_FORMALIZATION',
              'compiler_exit_code':run.returncode,'capsule':BASE+'.lean','capsule_sha256':sha(BASE+'.lean'),
              'output':BASE+'_output.txt','output_sha256':sha(BASE+'_output.txt'),
              'declarations':declarations(),'printed_owner_declarations':OWNERS,'axioms':axioms,
              'source_sha256':{p:sha(p) for p in SOURCES},'toolchain_sha256':{p:sha(p) for p in TOOLCHAIN},
              'physical_admission_or_complete_heat_law_formalized':False}
    (ROOT/(BASE+'_results.json')).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


def verify_lean_receipt():
    r = json.loads((ROOT/(BASE+'_results.json')).read_text())
    assert r['status']=='PASS' and r['compiler_exit_code']==0 and r['input_head']==HEAD
    assert r['declarations']==declarations() and r['printed_owner_declarations']==OWNERS
    assert r['capsule_sha256']==sha(BASE+'.lean') and r['output_sha256']==sha(BASE+'_output.txt')
    for group in ['source_sha256','toolchain_sha256']:
        for path,digest in r[group].items():
            assert sha(path)==digest,path
    out = (ROOT/(BASE+'_output.txt')).read_text()
    assert ': error' not in out and ': warning' not in out and 'sorryAx' not in out
    for name,axioms in r['axioms'].items():
        assert name in out and set(axioms)<={'propext','Classical.choice','Quot.sound'}
    assert not r['physical_admission_or_complete_heat_law_formalized']
    return {'compiled_propositions':len(declarations()),'axiom_reports':len(r['axioms']),
            'source_pins':len(SOURCES),'physical_scope_open':True}


def mutants():
    source = (ROOT/(BASE+'_check.py')).read_text()
    cases = [
        ('lost_tensor_mixing','return s.Matrix([r.trace(),2*r[0,1],0,r[0,0]-r[1,1]])',
         'return s.Matrix([r.trace(),0,0,r[0,0]-r[1,1]])'),
        ('wrong_observer_normalization','return simp(-eta+2*(eta*j)*(eta*j).T/k)',
         'return simp(-eta+2*(eta*j)*(eta*j).T)'),
        ('normalizer_derivative_missing','normalized -= 4*(j0.T*eta*variation)[0]*(eta*j0)*(eta*j0).T/kval**2',
         'normalized -= 0*(eta*j0)*(eta*j0).T'),
        ('wrong_off_diagonal_weight','cp = 2*a*(1+p**2)/p**3','cp = a*(1+p**2)/p**3'),
        ('forgot_record_and_used_pure_state','rg = rho(golden)','rg = s.diag(1,0)'),
        ('wrong_same_gate_input_curve','v = 2*t/(1+t*t)','v = t/(1+t*t)'),
    ]
    result=[]
    with tempfile.TemporaryDirectory(prefix='d0-recorded-observer-mutants-') as temp:
        for name,old,new in cases:
            # Replacements are restricted to the mathematics body, not this catalog.
            before,after=source.split('\ndef declarations():',1)
            assert before.count(old)==1,name
            path=Path(temp)/(name+'.py')
            path.write_text(before.replace(old,new)+'\ndef declarations():'+after)
            run=subprocess.run([sys.executable,str(path),'--repo',str(ROOT),'--math-only'],text=True,capture_output=True)
            assert run.returncode!=0 and 'AssertionError' in run.stderr,(name,run.stderr)
            result.append({'name':name,'rejected_by_mathematical_assertion':True})
    return result


def false_ledgers(header):
    results=[]
    with tempfile.TemporaryDirectory(prefix='d0-recorded-observer-ledgers-') as temp:
        for name in list(SCOPE)+['proof_sha256','checker_sha256','lean_receipt_sha256','input_head']:
            bad=json.loads(json.dumps(header))
            if name in SCOPE:
                bad['scope'][name]=not bad['scope'][name]
            else:
                bad[name]='0'*64
            path=Path(temp)/(name+'.json')
            path.write_text(json.dumps(bad))
            run=subprocess.run([sys.executable,str(ROOT/(BASE+'_check.py')),'--repo',str(ROOT),
                                '--expect',str(path)],text=True,capture_output=True)
            assert run.returncode!=0 and 'SOURCE_SCOPE_OR_INPUT_MISMATCH' in run.stderr,(name,run.stderr)
            results.append({'name':name,'rejected_before_mathematical_replay':True})
    return results


def main():
    global ROOT
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path)
    ap.add_argument('--compile',action='store_true')
    ap.add_argument('--math-only',action='store_true')
    ap.add_argument('--output',type=Path)
    ap.add_argument('--expect',type=Path)
    args=ap.parse_args()
    ROOT=args.repo.resolve() if args.repo else Path(__file__).resolve().parents[3]
    if args.compile:
        compile_capsule()
    if args.math_only:
        print('PASS_RECORDED_OBSERVER_MATHEMATICS',mathematics()['exact_control_count'])
        return
    header={'schema':'d0-native-recorded-observer-preparation/1','input_head':HEAD,'scope':SCOPE,
            'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
            'lean_receipt_sha256':sha(BASE+'_results.json')}
    expected=None
    if not args.output:
        expected=json.loads((args.expect or ROOT/(BASE+'_certificate.json')).read_text())
        assert all(expected.get(k)==v for k,v in header.items()),'SOURCE_SCOPE_OR_INPUT_MISMATCH'
    result={**header,**mathematics(),'lean':verify_lean_receipt(),'executed_mathematical_mutations':mutants(),
            'executed_false_ledgers':false_ledgers(header)}
    if args.output:
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        assert result==expected,'EXACT_CERTIFICATE_MISMATCH'
    print('PASS_NATIVE_RECORDED_OBSERVER_PREPARATION',result['exact_control_count'],'controls;',
          len(result['executed_mathematical_mutations']),'executed mutants')


if __name__=='__main__':
    main()
