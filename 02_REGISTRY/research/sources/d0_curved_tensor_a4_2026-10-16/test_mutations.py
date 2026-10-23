#!/usr/bin/env python3
"""Actually execute changed formulas, not modified expected-output files."""
from pathlib import Path
import json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
MUTATIONS=[
 ('lost_trace_constraint','v.col_join(cyc).nullspace()','cyc.nullspace()', 'build', 'actual_tensor_dimension'),
 ('half_tensor_derivative_price','P=s.Matrix(16,16,lambda a,b:sum(traceprod(Bs[a][i].T,Bs[b][i]) for i in (1,2,3))/3)','P=s.Matrix(16,16,lambda a,b:sum(traceprod(Bs[a][i].T,Bs[b][i]) for i in (1,2,3))/6)', 'symbol', 'tensor_symbol_exact_eigenvalues'),
 ('discard_Hodge_background','fr={ij:right0[ij]+tau*extra[ij] for ij in PAIRS}','fr={ij:tau*extra[ij] for ij in PAIRS}', 'curved', 'actual_Hodge_a4_baseline'),
 ('wrong_full_connection_curvature_weight','+60*sum(traceprod(A,A) for A in Om.values())','+30*sum(traceprod(A,A) for A in Om.values())', 'curved', 'full_curved_a4_not_flat_substitution')
]
def run():
 source=(HERE/'check_curved_tensor.py').read_text(); verdicts=[]
 with tempfile.TemporaryDirectory(prefix='d0-curved-tensor-mutants-') as d:
  for name,old,new,part,label in MUTATIONS:
   if source.count(old)!=1:raise ValueError('mutation not unique: '+name)
   path=Path(d)/(name+'.py');path.write_text(source.replace(old,new))
   driver='import runpy; m=runpy.run_path('+repr(str(path))+'); C,g,h,N,B=m["build"]();'
   if part=='symbol':driver+='m["principal_symbol"](N,B,g)'
   if part=='curved':driver+='m["curved_heat"](g,h)'
   r=subprocess.run([sys.executable,'-c',driver],capture_output=True,text=True,timeout=35)
   if r.returncode==0 or 'ArithmeticError: '+label not in r.stderr:
    raise ArithmeticError('wrong mutant result: '+name+'\n'+r.stderr)
   verdicts.append({'mutation':name,'failed_at':label,'verdict':'REJECTED_MATHEMATICALLY'})
 return {'schema':'d0-curved-tensor-mutations/1','changed_programs':verdicts,'expected_evidence_modified':False}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
