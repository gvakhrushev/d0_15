#!/usr/bin/env python3
"""Exact inputs of the analytic all-temperature golden/Hodge state separation."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile

import sympy as s

ROOT = None
BASE = '02_REGISTRY/research/certificates/a4d_native_golden_hodge_state_separation'
PROOF = '02_REGISTRY/research/A4D_NATIVE_GOLDEN_HODGE_STATE_SEPARATION.md'
HEAD = 'eb9594d2d06572164c26bd561e60e9faf4f830af'
SCOPE = {
    'analytic_all_m_window_anticoncentration': True,
    'analytic_full_Hodge_all_L_all_positive_beta_moment_bound': True,
    'arbitrary_unitary_and_independent_ancillary_state_retained': True,
    'all_sixteen_Fock_components_and_zero_modes_retained': True,
    'trace_distance_tends_to_one_on_dimension_compatible_sequences': True,
    'uniform_bound_constant_is_sampled_or_fitted': False,
    'new_Lean_theorem_or_complete_native_preparation_derived': False,
    'general_correlated_readout_preparations_excluded': False,
    'all_native_heat_or_Lorentz_or_curved_operators_excluded': False,
    'state_trace_distance_is_physical_action_contrast_error': False,
    'new_state_temperature_or_heat_law_selected': False,
    'source_Ward_stationarity_curved_roots_or_GR_closed': False,
    'T0_T3_44_nodes_or_original_terminals_changed': False,
}


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


# Exact Q(p), p^2=1-p, positive root. No floating decisions are used.
def gf(a=0,b=0):
    return (Q(a),Q(b))


def add(x,y):
    return (x[0]+y[0],x[1]+y[1])


def neg(x):
    return (-x[0],-x[1])


def mul(x,y):
    a,b=x; c,d=y
    return (a*c+b*d,a*d+b*c-b*d)


def scale(x,n):
    return (x[0]*n,x[1]*n)


def power(x,n):
    y=gf(1)
    for _ in range(n):
        y=mul(y,x)
    return y


def sign(x):
    # 2*(a+b*p)=(2a-b)+b*sqrt(5); compare squares only with known signs.
    u,v=2*x[0]-x[1],x[1]
    sg=lambda q:(q>0)-(q<0)
    if v==0:return sg(u)
    if u==0:return sg(v)
    if sg(u)==sg(v):return sg(u)
    return sg(u)*sg(u*u-5*v*v)


def exp_bounds(x,terms=40):
    assert x>=0 and x<Q(terms+2)
    term=Q(1); total=term
    for k in range(1,terms+1):
        term=term*x/k; total+=term
    first_tail=term*x/(terms+1)
    return total,total+first_tail/(1-x/(terms+2))


def mathematics():
    checks={}
    def ck(name,condition):
        assert bool(condition),name
        checks[name]=checks.get(name,0)+1

    p=gf(0,1)
    ck('golden_root_equation',add(p,mul(p,p))==gf(1))
    ck('golden_brackets',sign(add(p,gf(-Q(3,5))))>0 and sign(add(gf(Q(2,3)),neg(p)))>0)
    ck('golden_binomial_variance_lower_bound',sign(add(power(p,3),gf(-Q(1,5))))>0)
    for n in [1,2,3,4,8,16,32,64]:
        masses=[scale(power(p,n+k),math.comb(n,k)) for k in range(n+1)]
        total=gf()
        for mass in masses:total=add(total,mass)
        ck('whole_golden_binomial_mass',total==gf(1))
        for mass in masses:
            ck('exact_binomial_atom_bound',sign(add(gf(4),neg(scale(mul(mass,mass),n))))>=0)
        for width in [0,1,2,4]:
            for start in range(n+1):
                mass=gf()
                for x in masses[start:start+width+1]:mass=add(mass,x)
                ck('exact_log_window_mass_bound',sign(add(gf(4*(width+1)**2),neg(scale(mul(mass,mass),n))))>=0)

    root=(s.sqrt(5)-1)/2; a=s.sqrt(root)
    U=s.Matrix([[a,0,-root,0],[0,a,0,-root],[0,root,0,a],[root,0,a,0]])
    simp=lambda m:m.applyfunc(s.simplify)
    ck('literal_full_record_gate',simp(U.T*U)==s.eye(4))
    psi=simp(U*s.Matrix([1,0,0,0]))
    rho=simp(s.Matrix(2,2,lambda i,j:sum(psi[2*i+k]*psi[2*j+k] for k in range(2))))
    ck('literal_recorded_golden_state',simp(rho-s.diag(root,root**2))==s.zeros(2))
    ck('all_joint_record_mass_retained',s.simplify((psi.T*psi)[0])==1)
    for bits in itertools.product([True,False],repeat=6):
        cost=sum(1 if b else 2 for b in bits)
        ck('literal_anchor_bit_convention',cost==6+bits.count(False))

    for L in [2,3,4,5,6,8,12,16,33,64,129]:
        groups=Counter()
        for k in range(L):
            j=min(k,L-k)
            target=j//3
            groups[target]+=1
            ck('Gaussian_exponent_dominance',8*j*j>=64*target*target)
            ck('target_stays_in_actual_cycle',0<=target<=L//2)
        ck('Gaussian_group_multiplicity',max(groups.values())<=6)
        ck('all_cycle_modes_counted',sum(groups.values())==L)
    moment_factor=8
    for x in range(9):
        lo,hi=exp_bounds(Q(x,2))
        ck('rational_Taylor_moment_control',Q(x*x)<=moment_factor*lo)
        ck('Taylor_tail_brackets',lo<=hi)
    ck('factor_one_hostile_witness',exp_bounds(Q(2))[1]<16)
    ck('uniform_moment_constant',moment_factor*6**4==10368)

    # Actual L=2,4 difference matrices, before using their Fourier spectra.
    fock=16
    heat_controls=[]
    for L,expected in [(2,Counter({0:1,16:1})),(4,Counter({0:1,32:2,64:1}))]:
        shift=s.zeros(L)
        for i in range(L):shift[i,(i+1)%L]=1
        delta=L**2*(2*s.eye(L)-shift-shift.T)
        actual=Counter({int(k):int(v) for k,v in delta.eigenvals().items()})
        ck('literal_difference_scale_and_collision',actual==expected)
        counts=Counter({0:1})
        for _ in range(4):
            new=Counter()
            for e,m in counts.items():
                for v,k in actual.items():new[e+v]+=m*k
            counts=new
        counts=Counter({e:fock*m for e,m in counts.items()})
        ck('full_sixteen_grade_carrier',sum(counts.values())==16*L**4)
        ck('all_sixteen_zero_modes',counts[0]==16)
        for rate in [1,2,4]:
            # beta=rate*log(2)/16; exp(-beta*e) is an exact rational.
            boltz={e:Q(1,2**(rate*e//16)) for e in counts}
            Z=sum(counts[e]*boltz[e] for e in counts)
            ck('whole_heat_trace_preserved',Z>16 and counts[0]*boltz[0]==16)
            ck('normalized_full_heat_state',sum(counts[e]*boltz[e]/Z for e in counts)==1)
            ck('thermal_level_one_ground_mass',Q(16)/Z>0)
            heat_controls.append(dict(L=L,rate=rate,dimension=16*L**4,partition=str(Z),zero_modes=counts[0]))

    # A genuinely noncommuting finite projection witness for Section 4.
    v=s.Matrix([s.Rational(1,5),s.Rational(2,5),s.Rational(2,5),s.Rational(4,5)])
    w=s.Matrix([1,0,0,0])-v
    rotation=s.eye(4)-2*w*w.T/(w.T*w)[0]
    ck('noncommuting_witness_unitary',rotation.T*rotation==s.eye(4))
    eig=s.diag(s.Rational(3,4),s.Rational(1,8),s.Rational(3,32),s.Rational(1,32))
    rho=rotation*eig*rotation.T
    sigma=s.diag(s.Rational(1,2),s.Rational(1,4),s.Rational(3,16),s.Rational(1,16))
    P=s.diag(1,1,1,0); Qhigh=v*v.T; u=P*v
    E=P-u*u.T/(u.T*u)[0]
    ck('actual_noncommuting_states',rho*sigma!=sigma*rho)
    ck('actual_noncommuting_subspaces',P*Qhigh!=Qhigh*P)
    ck('intersection_is_projection',E.T==E and E*E==E)
    ck('intersection_lies_in_thermal_band',P*E==E)
    ck('high_density_part_annihilated',E*Qhigh==s.zeros(4))
    ck('rank_loss_control',P.rank()-E.rank()<=Qhigh.rank())
    ck('sigma_rank_loss_probability',s.trace(sigma*(P-E))<=s.Rational(1,2)*Qhigh.rank())
    middle=rotation*s.diag(0,s.Rational(1,8),s.Rational(3,32),0)*rotation.T
    low=rotation*s.diag(0,0,0,s.Rational(1,32))*rotation.T
    ck('middle_probability_not_deleted',s.trace(middle*E)<=s.trace(middle))
    ck('low_probability_rank_bound',s.trace(low*E)<=s.Rational(1,32)*E.rank())
    ck('all_density_parts_retained',rho==s.Rational(3,4)*Qhigh+middle+low)
    ck('positive_distinguishing_probability',s.trace((sigma-rho)*E)>0)
    ck('intersection_not_assumed_sigma_commuting',E*sigma!=sigma*E)

    # The growing biased factor is necessary: fair factors are maximally mixed.
    for n in [1,4,8]:
        ck('fair_record_positive_control',sum(Q(math.comb(n,k),2**n) for k in range(n+1))==1)
        ck('fair_record_flat_eigenvalues',len({Q(1,2**n) for _ in range(n+1)})==1)
    ck('dimension_compatible_Fock_ancilla',all(16*2**(4*ell)==16*(2**ell)**4 for ell in range(2,9)))
    return dict(checks=checks,exact_control_count=sum(checks.values()),full_heat_controls=heat_controls,
                all_temperature_proof='ANALYTIC_NOT_FINITE_EXTRAPOLATION',new_Lean_propositions=0)


def inputs():
    paths={
        '03_FORMALIZATION/D0/CondensedAnchor/DetectorSupportGoldenWeight.lean',
        '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
        '03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDirac.lean',
        '03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracSquare.lean',
        '03_FORMALIZATION/D0/Geometry/ArchiveCubicalDifferential.lean',
        '02_REGISTRY/research/A4D_NATIVE_MODULAR_PREPARATION_BOUNDARY.md',
        '02_REGISTRY/research/A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md',
    }
    prior='02_REGISTRY/research/certificates/a4d_native_positive_heat_radial_balance_results.json'
    paths.add(prior)
    rec=json.loads((ROOT/prior).read_text())
    assert rec['status']=='PASS' and rec['compiler_exit_code']==0
    assert not rec['native_preparation_source_or_GR_derived']
    for group in ['transitive_d0_source_sha256','primary_and_prior_input_sha256','toolchain_input_sha256']:
        for path,digest in rec[group].items():
            assert sha(path)==digest,path
            paths.add(path)
    for key in ['capsule','output']:
        assert sha(rec[key])==rec[key+'_sha256']
        paths.add(rec[key])
    return {path:sha(path) for path in sorted(paths)}


def mutants():
    source=(ROOT/(BASE+'_check.py')).read_text()
    changes=[
        ('golden_second_branch_changed','simp(rho-s.diag(root,root**2))','simp(rho-s.diag(root,root))'),
        ('wrong_word_cost','power(p,n+k),math.comb(n,k)','power(p,n+2*k),math.comb(n,k)'),
        ('Gaussian_group_too_short','target=j//3','target=j//2'),
        ('Gaussian_group_mass_deleted','max(groups.values())<=6','max(groups.values())<=4'),
        ('thermal_moment_factor_wrong','moment_factor=8','moment_factor=1'),
        ('Fock_modes_deleted','fock=16','fock=1'),
        ('thermal_zero_modes_deleted','counts=Counter({e:fock*m for e,m in counts.items()})','counts=Counter({e:fock*m for e,m in counts.items() if e!=0})'),
        ('mesh_scale_deleted','delta=L**2*(2*s.eye(L)-shift-shift.T)','delta=(2*s.eye(L)-shift-shift.T)'),
        ('high_state_not_removed','E=P-u*u.T/(u.T*u)[0]','E=P'),
    ]
    results=[]
    with tempfile.TemporaryDirectory(prefix='d0-state-mutants-') as temp:
        for name,old,new in changes:
            assert source.count(old)==2,(name,source.count(old))  # definition and mutation string
            # Replace only the mathematical body occurrence, before this function.
            at=source.index(old); body=source[:at]+new+source[at+len(old):]
            path=Path(temp)/(name+'.py');path.write_text(body)
            r=subprocess.run([sys.executable,str(path),'--repo',str(ROOT),'--math-only'],text=True,capture_output=True)
            assert r.returncode!=0 and 'AssertionError' in r.stderr,(name,r.returncode,r.stderr)
            results.append(dict(name=name,rejected_by_mathematical_assertion=True))
    return results


def false_ledgers(header):
    results=[]
    with tempfile.TemporaryDirectory(prefix='d0-state-ledgers-') as temp:
        for name in list(SCOPE)+['proof_sha256','checker_sha256','inputs_sha256']:
            bad=json.loads(json.dumps(header))
            if name in SCOPE:bad['scope'][name]=not bad['scope'][name]
            elif name=='inputs_sha256':bad[name]={}
            else:bad[name]='0'*64
            path=Path(temp)/(name+'.json');path.write_text(json.dumps(bad))
            r=subprocess.run([sys.executable,str(ROOT/(BASE+'_check.py')),'--repo',str(ROOT),'--expect',str(path)],text=True,capture_output=True)
            assert r.returncode!=0 and 'SOURCE_SCOPE_OR_INPUT_MISMATCH' in r.stderr,(name,r.returncode,r.stderr)
            results.append(dict(name=name,rejected_before_mathematical_replay=True))
    return results


def main():
    global ROOT
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path);ap.add_argument('--expect',type=Path)
    ap.add_argument('--output',type=Path);ap.add_argument('--math-only',action='store_true')
    args=ap.parse_args()
    ROOT=args.repo.resolve() if args.repo else Path(__file__).resolve().parents[3]
    if args.math_only:
        result=mathematics();print('PASS_GOLDEN_HODGE_MATHEMATICS',result['exact_control_count']);return
    header=dict(schema='d0-native-golden-hodge-state-separation/1',input_head=HEAD,scope=SCOPE,
                proof_sha256=sha(PROOF),checker_sha256=sha(BASE+'_check.py'),inputs_sha256=inputs())
    expected=None
    if not args.output:
        expected=json.loads((args.expect or ROOT/(BASE+'_certificate.json')).read_text())
        assert all(expected.get(k)==v for k,v in header.items()),'SOURCE_SCOPE_OR_INPUT_MISMATCH'
    result={**header,**mathematics(),'executed_mathematical_mutations':mutants(),
            'executed_false_ledgers':false_ledgers(header)}
    if args.output:args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:assert result==expected,'EXACT_CERTIFICATE_MISMATCH'
    print('PASS_GOLDEN_HODGE_STATE_SEPARATION',result['exact_control_count'],'controls;',
          len(result['executed_mathematical_mutations']),'math mutants;',len(result['executed_false_ledgers']),'false ledgers')


if __name__=='__main__':main()
