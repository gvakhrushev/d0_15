#!/usr/bin/env python3
"""Configured D0 N1 full ORIGINAL source: exact nearest-time-neighbor
block Jacobian after exact Lorentz frame gauge deflation. Implements the
actual block Schur elimination and compares it with a dense original
Jacobian solve, without adding an action, gauge-penalty or source term.

Exact nearest-neighbor support is mathematical from the actual finite
sum of original based six-face/G2STAR and CAR forward-difference local
N1 CQ contributions. Numeric 4/5-interval seed checks are only controls.
This does NOT prove mesh-uniform invertibility, interval exact roots,
or physical compulsory Book03 selection.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import solve,svdvals
from scipy.optimize._numdiff import approx_derivative
from check_full42_n1_single_internal import problem

def active_variables(n):
    assert n>=2
    active=np.array([idx for idx in range(42*(n-1))
          if not (idx//42+1<=n-2 and 16<=idx%42<22)],dtype=int)
    sizes=[36]*(n-2)+[42]
    assert sum(sizes)==len(active)==36*n-30
    return active,sizes

def check(n):
    h,base,psi,rhos,fields,euler=problem(n,[1.]*n)
    active,sizes=active_variables(n)
    def F(y):
        z=np.zeros(42*(n-1))
        z[active]=y
        return euler(z)[active]
    x=np.zeros(len(active))
    J=approx_derivative(F,x,method="3-point",abs_step=1e-6)
    ends=np.cumsum([0]+sizes)
    offband=0.
    for i in range(n-1):
        for j in range(n-1):
            if abs(i-j)>1:
                offband=max(offband,float(np.max(
                  np.abs(J[ends[i]:ends[i+1],ends[j]:ends[j+1]]))))
    if offband>2e-10:
        raise AssertionError(("original nonlocal source leaked",n,offband))
    diagonal=[J[ends[j]:ends[j+1],ends[j]:ends[j+1]]
              for j in range(n-1)]
    upper=[J[ends[j]:ends[j+1],ends[j+1]:ends[j+2]]
              for j in range(n-2)]
    lower=[J[ends[j+1]:ends[j+2],ends[j]:ends[j+1]]
              for j in range(n-2)]
    schur=[];conds=[]
    for j in range(n-1):
        cur=(diagonal[j] if j==0 else diagonal[j]-
             lower[j-1]@solve(schur[-1],upper[j-1],assume_a="gen"))
        schur.append(cur)
        conds.append(float(np.linalg.cond(cur)))
    if max(conds)>1e12:
        raise AssertionError(("block pivot ill-conditioned at seed",n,conds))
    target=np.arange(1,len(active)+1,dtype=float)/len(active)
    direct=solve(J,target,assume_a="gen")
    b=[target[ends[j]:ends[j+1]] for j in range(n-1)]
    y=[]
    for j in range(n-1):
        rhs=b[j] if j==0 else b[j]-lower[j-1]@y[-1]
        y.append(solve(schur[j],rhs,assume_a="gen"))
    recovered=y.copy()
    for j in range(n-3,-1,-1):
        recovered[j]=y[j]-solve(schur[j],upper[j]@recovered[j+1],assume_a="gen")
    diff=float(np.max(abs(np.concatenate(recovered)-direct)))
    if diff>1e-8:
        raise AssertionError(("original block Schur != full dense",n,diff))
    return {
      "intervals":n,"full_original_Euler":42*(n-1),
      "omitted_exact_Lorentz_gauge":6*(n-2),
      "gauge_source_dim":len(active),"time_block_sizes":sizes,
      "off_tridiagonal_source_Jacobian_max":offband,
      "all_block_schur_condition_numbers":conds,
      "numerical_inverse_block_vs_dense_inf_error":diff,
      "seed_jacobian_min_singular":float(svdvals(J)[-1]),
      "genuine_Schur_root_proved":False,
      "actual_G0_Book_compulsory_selected":False,
      "uniform_h_inverse_proved":False}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--json",type=Path)
    args=p.parse_args()
    rows=[check(n) for n in (4,5)]
    result={"status":"PASS_EXACT_TIME_LOCALITY_AND_BOUNDED_BLOCK_SCHUR_DIAGNOSTIC",
            "proof":"Each original N1 CQ cell uses only node j,j+1, "
                    "thus interior Euler at j uses only j-1,j,j+1.",
            "rows":rows,
            "GR_closed":False}
    output=json.dumps(result,indent=2)+"\n"
    print(output,end="")
    if args.json:args.json.write_text(output,encoding="utf-8")
if __name__=="__main__":main()
