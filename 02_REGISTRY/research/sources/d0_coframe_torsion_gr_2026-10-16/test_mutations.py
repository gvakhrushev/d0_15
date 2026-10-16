#!/usr/bin/env python3
"""Actually execute altered mathematics; do not weaken input expectations."""
from pathlib import Path
import json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
M=[
 ('wrong_cyclic_contorsion_sign','TT[a][b][c]+TT[b][c][a]-TT[c][a][b]',
  'TT[a][b][c]+TT[b][c][a]+TT[c][a][b]','all24_torsion_inverse_001'),
 ('freeze_moving_coframe_term','return absorb(e,torsion(delta_e,delta_de,w))',
  'return absorb(e,torsion(delta_e,delta_de,zero_connection()))','complete_connection_jet_0'),
 ('drop_boundary_density','get(stored)+get(quadratic)+get(boundary)',
  'get(stored)+get(quadratic)','complete_geometric_density_with_boundary'),
 ('drop_torsion_cross_term','scale(-1,wedge(covSigma(c,d),Cup))',
  'scale(0,wedge(covSigma(c,d),Cup))','complete_geometric_density_with_boundary')]
def run():
    src=(HERE/'check_reconstruction.py').read_text();results=[]
    with tempfile.TemporaryDirectory(prefix='d0-torsion-negative-') as td:
        for name,old,new,expected in M:
            if src.count(old)!=1:raise ValueError('nonunique mutation '+name)
            p=Path(td)/(name+'.py');p.write_text(src.replace(old,new))
            r=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,timeout=30)
            if r.returncode==0 or 'ArithmeticError: '+expected not in r.stderr:
                raise ArithmeticError('wrong mutation outcome '+name+'\n'+r.stderr)
            results.append({'mutation':name,'failure':expected,'verdict':'REJECTED_MATHEMATICALLY'})
    return {'schema':'d0-coframe-torsion-mutations/1','mutations':results,'expected_output_modified':False}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
