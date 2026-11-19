#!/usr/bin/env python3
"""Execute changed formulae; committed expected receipts are not edited."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
MUTATIONS=[
 ('omit_left_normalization',
  'C=G1root.inv()*(kappa*A)*G0root.inv()',
  'C=G1root.inv()*(kappa*A)',
  'full_jets','moving_noncommutative_determinants'),
 ('freeze_right_endpoint_source',
  'rjet=logdet_jet(E,order)-logdet_jet(G0,order)-logdet_jet(G1,order)',
  'rjet=logdet_jet(E,order)-logdet_jet(G0,order)',
  'full_jets','all_endpoint_source_jet_1'),
 ('discard_lapse_curvature',
  'gh=S.diag(N*N,1,S.exp(2*x),S.exp(4*x))',
  'gh=S.diag(1,1,S.exp(2*x),S.exp(4*x))',
  'spatial_reference','frozen_lapse_reference_scalar'),
 ('treat_reference_volume_as_constant',
  'raw=-lam*V+c*A4;reference=-lam*V+c*A3',
  'raw=-lam*V+c*A4;reference=c*A3',
  'adm_ir','full_volume_source_kept')]

def main():
    src=(HERE/'check_two_sided.py').read_text()
    result=[]
    with tempfile.TemporaryDirectory(prefix='d0-two-sided-negative-') as directory:
        for name,old,new,function,label in MUTATIONS:
            if src.count(old)!=1: raise ValueError('Nonunique target: '+name)
            p=Path(directory)/(name+'.py');p.write_text(src.replace(old,new))
            driver='import runpy; m=runpy.run_path('+repr(str(p))+');m['+repr(function)+']()'
            cp=subprocess.run([sys.executable,'-c',driver],capture_output=True,text=True,timeout=40)
            if cp.returncode==0 or 'ArithmeticError: '+label not in cp.stderr:
                raise ArithmeticError('Unexpected rejection: '+name+'\n'+cp.stderr)
            result.append({'mutation':name,'failed_check':label,'result':'REJECTED_BY_MATHEMATICS'})
    return {'mutations':result,'expected_receipts_changed':False}

if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
