#!/usr/bin/env python3
"""Run changed mathematical formulae. Never change an expected receipt to pass."""
from pathlib import Path
import json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CASES=[
 ('wrong_seed_covariance',"off=A*A-4*A*B-B*B","off=A*A-3*A*B-B*B",'source_capacity','actual_source_seed_covariance'),
 ('missing_normalization',"want=2*Gf*hf/(1+(hf.T*Gf*hf)[0])","want=2*Gf*hf",'source_capacity','nonzero_exact_pure_source_witness'),
 ('freeze_empty_shell',"Tk=occupied*X*occupied-ek*occupied+perp*X*occupied+occupied*X*perp","Tk=occupied*X*occupied-ek*occupied+perp*X*occupied+occupied*X*perp+perp*X*perp",'rank_geometry','true_shell_constraint_trace'),
 ('freeze_preparation_jet',"E2*C0+2*E1*C1,s.zeros(2,1)","E2*C0,s.zeros(2,1)",'obstruction','complete_rankfree_second_eigen_jet'),
 ('wrong_resolvent_sign',"P.T*(Y-2*X*Rq*X)*P","P.T*(Y+2*X*Rq*X)*P",'obstruction','actual_second_Feshbach_curvature')]
def run():
    source=(HERE/'check_rank_continuation.py').read_text()
    # Preserve the exact original input, irrespective of temporary mutant directory.
    source=source.replace('ROOT=Path(__file__).resolve().parents[4]','ROOT=Path('+repr(str(ROOT))+')')
    out=[]
    with tempfile.TemporaryDirectory(prefix='d0-memory-rank-mutants-') as directory:
        for name,old,new,entry,failed in CASES:
            if source.count(old)!=1:raise ValueError('nonunique mutation: '+name)
            path=Path(directory)/(name+'.py');path.write_text(source.replace(old,new))
            cmd='import runpy;m=runpy.run_path('+repr(str(path))+');m['+repr(entry)+']()'
            p=subprocess.run([sys.executable,'-c',cmd],capture_output=True,text=True,timeout=40)
            if p.returncode==0 or 'ArithmeticError: '+failed not in p.stderr:
                raise ArithmeticError('wrong mutation outcome: '+name+'\n'+p.stderr)
            out.append({'name':name,'outcome':'REJECTED_BY_MATHEMATICS','failed_check':failed})
    return {'schema':'d0-memory-rank-mutations/1','mutations':out,'old_expected_evidence_changed':False}
if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
