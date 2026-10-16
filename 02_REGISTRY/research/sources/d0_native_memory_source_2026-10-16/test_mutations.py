#!/usr/bin/env python3
"""Execute four altered mathematics programs, not changed expected receipts."""
from pathlib import Path
import json, subprocess, sys, tempfile
HERE=Path(__file__).resolve().parent
CASES=[
 ("erase_spatial_grade_memory",
  "H=s.diag(*[int(mask.bit_count()-int(bool(mask&(1<<r)))>=2) for mask in range(16)])",
  "H=s.zeros(16)", "complete_order_01_connection_source"),
 ("change_the_ordered_process",
  "m01=matrix_red(U[1]*U[0]*seed);m10=matrix_red(U[0]*U[1]*seed)",
  "m01=matrix_red(U[0]*U[1]*seed);m10=matrix_red(U[0]*U[1]*seed)",
  "owned_two_path_full_state_difference"),
 ("delete_actual_link_transport_jet",
  "dD=8*G*(phases[r]*creator(legs[r])-s.conjugate(phases[r])*annihilator(legs[r]))",
  "dD=s.zeros(16)", "exact_complete_link_source_1"),
 ("impose_full_shell_rank_on_the_new_branch",
  "C0=s.diag(s.Rational(3,5),0);Psi=J*C0",
  "C0=s.diag(s.Rational(3,5),1);Psi=J*C0", "rank_free_matter_equation")
]
def run():
    text=(HERE/'check_memory_source.py').read_text()
    outcomes=[]
    with tempfile.TemporaryDirectory(prefix='d0-memory-source-mutant-') as folder:
        for name,old,new,label in CASES:
            if text.count(old)!=1:raise ValueError('Nonunique mutation '+name)
            path=Path(folder)/(name+'.py')
            path.write_text(text.replace(old,new))
            proc=subprocess.run([sys.executable,str(path)],capture_output=True,text=True,timeout=45)
            if proc.returncode==0 or ('ArithmeticError: '+label) not in proc.stderr:
                raise ArithmeticError('Unexpected rejection '+name+'\n'+proc.stderr)
            outcomes.append({'name':name,'verdict':'REJECTED_BY_MATHEMATICS','failed_check':label})
    return {'mutations':outcomes,'expected_receipt_changed':False}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
