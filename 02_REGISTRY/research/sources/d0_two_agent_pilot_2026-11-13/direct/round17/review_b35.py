#!/usr/bin/env python3
"""Root review: immutable B35 inputs, isolated replay, exact small reflections."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,os,shutil,subprocess,sys,tempfile
P=Path(__file__).resolve().parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round35')
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
receipt=json.loads((B/'RECEIPT.json').read_text())
for n,v in receipt['files'].items():assert h(B/n)==v,n
for n,v in receipt['upstream_sha256'].items():assert h(Path(n))==v,n
scripts=['certify_reflection_reduction.py','check_b25_reflection_targets.py','check_reduction_hostiles.py','check_source_derivative_identities.py']
outputs=['REFLECTION_REDUCTION_CHECK.json','B25_REFLECTION_TARGETS_CHECK.json','REDUCTION_HOSTILES_CHECK.json','SOURCE_DERIVATIVE_CHECK.json']
replays=[]
with tempfile.TemporaryDirectory(prefix='d0-root-b35-') as tmp:
    root=Path(tmp);work=root/'round35';work.mkdir()
    (root/'round25').symlink_to(B.parent/'round25',target_is_directory=True)
    for n in scripts+['anchor_reflection.py']:shutil.copyfile(B/n,work/n)
    for n in scripts:
        proc=subprocess.run([sys.executable,'-B','-W','error',str(work/n)],cwd=work,
            env=dict(os.environ,OPENBLAS_NUM_THREADS='1'),capture_output=True,text=True)
        assert proc.returncode==0,(n,proc.stdout[-2000:],proc.stderr[-2000:])
        replays.append({'script':n,'exit_code':0})
    comparisons={}
    for n in outputs:
        # Same pinned environment should reproduce both rational certificates
        # and float diagnostics. A mismatch is reported, never normalized away.
        assert (work/n).read_bytes()==(B/n).read_bytes(),n
        comparisons[n]=h(B/n)

# Independent exact rank-two identity and derivative norm in a rational chart.
import sympy as q
c=q.symbols('c',real=True,positive=True);t=q.sqrt(1-c*c)
r=q.Matrix([1,0,0]);b=q.Matrix([c,t,0]);u=(r+b)/q.sqrt(2*(1+c));I=q.eye(3)
R=lambda x:I-2*x*x.T
K=b*r.T-r*b.T
assert q.simplify(R(u)*R(r)-(I+K+K*K/(1+c)))==q.zeros(3)
# An out-of-plane unit tangent is orthogonal to r and b. D R has squared
# nonzero eigenvalues 2/(1+c); right multiplication by R_r preserves norm.
du=q.Matrix([0,0,1])/q.sqrt(2*(1+c));dR=-2*(du*u.T+u*du.T)
assert q.simplify(q.trace(dR*dR)-4/(1+c))==0
assert q.simplify(dR.det())==0
assert q.simplify(q.trace(dR))==0

# Recompute the conservative seven-report budget, including joint private
# anchors. None of these widths/accuracies are asserted to have been achieved.
Nref=218960+10080*32768+448*(32768+32768)
assert Nref<2**29
budget={}
for precision in (3224,3228,3230):
    eta=F(5936,2**precision)+F(Nref,2**4096)
    assert eta<F(1,2**(precision-14))
    assert 2**3157*eta<F(1,2**(precision-3171))
    budget[str(precision)]={'bank_error_lt':'2^-'+str(precision-14),
                           'gain_normalized_bank_error_lt':'2^-'+str(precision-3171)+'/a^2'}
out={'status':'PASS_B35_EXACT_REDUCTION_AND_ISOLATED_REPLAY',
     'B35_commit':'7675cc844910902b5b449e716fb6b02eea8d0b44',
     'B35_receipt_sha256':h(B/'RECEIPT.json'),'verified_B35_files':receipt['files'],
     'verified_upstream':receipt['upstream_sha256'],'replayed_scripts':replays,
     'byte_identical_outputs':comparisons,'independent_symbolic_reflection_identity':True,
     'independent_symbolic_derivative_norm_identity':True,'independent_conditional_budgets':budget,
     'contract':'uniform joint-anchor isometry over every SAM/site and arbitrary external entanglement; clean private work included in reflection; literal adjoint of the actual U',
     'preparation_U_compiled':False,'full_alpha_lower_bound_proved':False,
     'source_derivative_is_target_identity_not_native_discrete_compiler_derivative':True,
     'physical_C_closed':False,'GR_closed':False}
(P/'ROOT_REVIEW_B35.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'byte_identical_outputs':len(comparisons)}))
