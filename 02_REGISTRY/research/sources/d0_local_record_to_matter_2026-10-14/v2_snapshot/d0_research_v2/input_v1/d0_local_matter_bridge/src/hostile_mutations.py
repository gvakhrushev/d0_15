"""Run actual corrupted algebra programs and demand a nonzero exit.
The mutant source is executed in an isolated temporary copy of the local package.
"""
from __future__ import annotations
import json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'src/exact_algebra.py').read_text()
mutations=[
 ('wrong_pi0_normalization','pi0=s.Rational(6,5)*phi**2','pi0=s.Rational(7,5)*phi**2','pi0_exact_seam_identity'),
 ('omit_density_normalization','return rho(A)-s.trace(A)*I/2','return rho(A)','full_density_pairing_normalization'),
 ('wrong_metric_horizontal_scale','A=v*eta/2;T=lift(A)','A=v*eta/3;T=lift(A)','metric_lift'),
 ('discard_half_the_Fock_trace','expected=4*(G[i,r]*s.trace(K)-(G*K)[i,r])','expected=8*(G[i,r]*s.trace(K)-(G*K)[i,r])','full_Fock_link_trace'),
 ('omit_archive_phase','Btheta=P+(x+s.I*y)*Q','Btheta=I','seam_full_feedback'),
 ('reverse_thermal_variance_sign','Eprime=-2*E+2*beta*var','Eprime=-2*E-2*beta*var','radial_second_derivative_at_balance'),
]
rows=[]
for name,old,new,expected in mutations:
    if source.count(old)!=1:raise AssertionError(('MUTATION_ANCHOR',name,source.count(old)))
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);(root/'src').mkdir();(root/'results').mkdir()
        p=root/'src/exact_algebra.py';p.write_text(source.replace(old,new))
        cp=subprocess.run([sys.executable,str(p)],text=True,capture_output=True,timeout=40,
                          env={**os.environ,'OPENBLAS_NUM_THREADS':'1'})
        if cp.returncode==0 or expected not in cp.stderr:
            raise AssertionError(('MUTANT_NOT_REJECTED',name,cp.stdout,cp.stderr))
        rows.append({'mutation':name,'exit_code':cp.returncode,'expected_failed_check_prefix':expected,
                     'last_error_line':cp.stderr.strip().splitlines()[-1]})
        print('REJECTED_ACTUAL_MUTANT',name)
(ROOT/'results/hostile_mutations.json').write_text(json.dumps({'status':'PASS','executed_mutants':rows},indent=2)+'\n')
