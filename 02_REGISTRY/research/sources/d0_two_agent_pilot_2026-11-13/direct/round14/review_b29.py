#!/usr/bin/env python3
"""Replay conditional B29 and check its gain floor by a separate rational bound."""
from pathlib import Path
from tempfile import TemporaryDirectory
from fractions import Fraction as F
import hashlib,importlib.util,json,os,shutil,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[5]
BROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
BREL=Path('02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')
B=BROOT/BREL
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
receipt=json.loads((B/'round29/RECEIPT.json').read_text())
inputs={'owner':ROOT/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md',
        'B21_reference':B/'round21/REFERENCE_METADATA.json','B25_slack':B/'round25/STRICT_SLACK.json',
        'A13_counts':P.parent/'round13/CIRCUIT_COMPILATION.json','A11_norm':P.parent/'round11/SOURCE_NORM_CERTIFICATE.json'}
for name,path in inputs.items():assert sha(path)==receipt['input_sha256'][name],name
for name,value in receipt['output_sha256'].items():assert sha(B/'round29'/name)==value,name
outputs={}
with TemporaryDirectory(prefix='d0_a14_review_b29_') as temp:
    root=Path(temp);shutil.copytree(B/'round29',root/'round29',ignore=shutil.ignore_patterns('__pycache__'))
    (root/'round21').mkdir();shutil.copy2(B/'round21/REFERENCE_METADATA.json',root/'round21/REFERENCE_METADATA.json')
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    for script,name in [('certify_error_budget.py','BUDGET_CERTIFICATE.json'),('check_structural_boundary.py','STRUCTURE_HOSTILE.json')]:
        proc=subprocess.run([sys.executable,'-B','-W','error',str(root/'round29'/script)],env=env,text=True,capture_output=True)
        assert proc.returncode==0,(script,proc.stdout,proc.stderr)
        assert not proc.stderr,(script,proc.stderr)
        assert sha(root/'round29'/name)==sha(B/'round29'/name),name
        outputs[name]=sha(root/'round29'/name)
        print(script,'PASS byte-identical output',flush=True)

# Independent simplification: d=Fh/(36*(ry/rx)) implies
# 2*kappa*p^7*d*rx*ry*alpha^2 = kappa*p^7*Fh*rx^2*alpha^2/18.
# Under alpha>=1/2, use alpha^2>=1/4. All bounds below are rational;
# kappa's lower bound is independently certified by the integer native power.
owner=ROOT/'02_REGISTRY/research/sources/d0_native_readiness_amplification_2026-10-24/native_phase.py'
spec=importlib.util.spec_from_file_location('a14_budget_phase',owner);phase=importlib.util.module_from_spec(spec);sys.modules[spec.name]=phase;spec.loader.exec_module(phase)
scale,cosine,sine=phase._rotation_intervals(512,256)
assert sine[0]>0
kappa_lower=F(sine[0],scale)**2
assert kappa_lower>F(937,1000)
pmin,pmax=F(309,500),F(619,1000);z=F(1,2**20)
rx_lower=4*z*(1-z*4*pmax**3)*pmin**11
Fh=F(json.loads((B/'round21/REFERENCE_METADATA.json').read_text())['F_h_rational'])
coefficient_lower=F(937,1000)*pmin**7*Fh*rx_lower**2/72
assert coefficient_lower>F(1,2**66)
result={'status':'PASS_B29_ISOLATED_REPLAY_AND_INDEPENDENT_RATIONAL_GAIN_FLOOR',
        'input_sha256':receipt['input_sha256'],'B29_output_sha256':receipt['output_sha256'],
        'B29_receipt_sha256':sha(B/'round29/RECEIPT.json'),'byte_identical_replayed_outputs':outputs,
        'independent_gain_simplification':'g/epsilon^2=kappa*p^7*Fh*rx^2*alpha_target^2/18',
        'independent_rational_coefficient_lower_at_alpha_half':str(coefficient_lower),
        'conditional_coefficient_gt':'2^-66','conditional_g_gt':'2^-3128','conditional_gs_gt':'2^-3158',
        'required_hypothesis':'FULL IDEAL alpha_target>=1/2; this is not proved by the component count',
        'full_target_readiness_established':False,'actual_c_w_and_full_clock_computed':False,
        'physical_C_closed':False,'GR_closed':False}
(P/'ROOT_REVIEW_B29.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],flush=True)
