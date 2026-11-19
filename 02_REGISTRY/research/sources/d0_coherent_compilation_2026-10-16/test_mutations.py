#!/usr/bin/env python3
"""Run genuinely altered calculations; no output-file or hash-only rejections."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
HERE=Path(__file__).resolve().parent
MUTATIONS=[
 ('wrong_completion_direction','R[base:base+2,base:base+2]=env.T','R[base:base+2,base:base+2]=env','coherent_completion_all_input_vectors'),
 ('frozen_completion_jet','completed_jet=mat(R1*C0+R0*C1)','completed_jet=mat(R0*C1)','same_comparator_metric_after_compilation'),
 ('wrong_AF_path_carry','for old,j,path in b[0]]]','for old,j,path in b[1]]]','AF_dimensions_2'),
 ('unequal_cost_code_block','CN=s.diag(*([6]*13+[7]*8))','CN=s.diag(*([6]*13+[8]*8))','exact_full_code_shift'),
 ('frozen_probability_denominator','shifted=sum(w*(l+b) for w,l in zip(weights,prices))/Z','shifted=sum(w*(l+b) for w,l in zip(weights,prices))/Z.subs(x,0)','normalized_complete_price_constant_shift')]
def main():
    source=(HERE/'check_coherent_compilation.py').read_text()
    result=[]
    with tempfile.TemporaryDirectory(prefix='d0-compilation-mutants-') as directory:
        for name,old,new,label in MUTATIONS:
            if source.count(old)!=1:raise ValueError('mutation not unique: '+name)
            path=Path(directory)/(name+'.py')
            path.write_text(source.replace(old,new))
            run=subprocess.run([sys.executable,str(path)],capture_output=True,text=True,timeout=100)
            if run.returncode==0 or 'ArithmeticError: '+label not in run.stderr:
                raise ArithmeticError('wrong mutation outcome: '+name+'\n'+run.stderr)
            result.append({'name':name,'result':'REJECTED_BY_MATHEMATICS','check':label})
    return {'schema':'d0-coherent-compilation-mutations/1','mutations':result}
if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
