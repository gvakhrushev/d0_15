#!/usr/bin/env python3
"""Execute altered mathematical programs, without modifying expected output."""
from pathlib import Path
import subprocess,sys,tempfile,json
P=Path(__file__).resolve().parent
M=[
('frozen_partition_derivative','rho1=K1/Z-K*Z1/Z**2','rho1=K1/Z','thermal_normalizer_jet'),
('wrong_inverse_jet','X1=-X*A1*X','X1=X*A1*X','feedback_inverse_jet'),
('freeze_thermal_auxiliary_at_second_order','corrH=tr(rho1*dlog_at_diagonal(rho,rho1))/beta','corrH=s.Integer(0)','heat_exact_Schur_second_response'),
('identify_Delta_with_heat_generator','W=rhoM-B**(m-1)/Z+','W=rhoM-K/Z+','complete_native_source_operator')
]
def run():
    text=(P/'check_unfolding.py').read_text();results=[]
    with tempfile.TemporaryDirectory(prefix='d0-price-unfolding-') as td:
        for label,old,new,failed in M:
            if text.count(old)!=1: raise ValueError('nonunique mutation '+label)
            file=Path(td)/(label+'.py'); file.write_text(text.replace(old,new))
            proc=subprocess.run([sys.executable,str(file)],text=True,capture_output=True,timeout=30)
            if proc.returncode==0 or ('ArithmeticError: '+failed) not in proc.stderr:
                raise ArithmeticError('unexpected mutation result '+label+'\n'+proc.stderr)
            results.append({'mutation':label,'failed_check':failed,'verdict':'REJECTED_MATHEMATICALLY'})
    return {'mutations':results,'expected_receipt_mutated':False}
if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
