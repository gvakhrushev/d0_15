#!/usr/bin/env python3
"""Narrow current calculation only. Numerical tables are not interval proofs."""
import json
from check_exact import main as exact
from finite_symbol import curvature
from continuum_oblique import limit
from dense_check import actual

def run():
 report=exact();finite=[];independent=[]
 for L in [4,8,16,32,64,128,256,512]:
  cutoff=None if L<=16 else 6
  row=curvature(L,(0,1,1,0),(1.,1.,0.),cutoff=cutoff)
  if row['rescaled']<=0:raise ArithmeticError('finite numerical source diagnostic')
  finite.append(row)
 lim=limit(6)
 if abs(finite[-1]['rescaled']-lim['source'])>0.001:raise ArithmeticError('continuum diagnostic convergence')
 for L in [4,6]:
  baseline=actual(L,0);pred=curvature(L,(0,1,1,0),(1.,1.,0.),cutoff=None)['Spp']
  for eps in [.002,.001]:
   pos=actual(L,eps);neg=actual(L,-eps)
   fd=(pos[0]+neg[0]-2*baseline[0])/eps**2
   if abs(fd-pred)>2e-5:raise ArithmeticError('independent true-link finite-difference check')
   if pos[4]>1e-9 or neg[4]>1e-9:raise ArithmeticError('proper Lorentz link check')
   if pos[2]>1e-10:raise ArithmeticError('complete scalar vacuum')
   independent.append(dict(L=L,epsilon=eps,analytic_second_jet=pred,independent_finite_difference=fd,
      proper_link_max_residual=max(pos[4],neg[4]),scalar_vacuum_residual=pos[2],actual_P1_matter_price=pos[3]))
 return {'schema':'d0-finite-causal-validation-run/1','exact':report,
 'finite_second_jets':finite,'infinite_series_numeric':lim,'independent_actual_proper_links':independent,
 'proof_scope':'specific second epsilon jet; series sign proved analytically, decimal values floating-point',
 'all_modes_note':'all L^4 modes for L<=16; named cutoff for larger-L diagnostics, analytic Gaussian majorant in proof',
 'full_first_source_uniform_remainder':False,'native_action_admission':False,'GR_closed':False}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
