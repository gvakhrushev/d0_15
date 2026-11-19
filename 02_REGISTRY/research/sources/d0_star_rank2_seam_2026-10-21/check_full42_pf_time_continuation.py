#!/usr/bin/env python3
"""Numerical CONTINUATION of one genuinely configured N1 CQ original
16+24+2 short-collar source root through spatially homogeneous positive
time-slice PF weights [1,rho], rho=1,1.25,1.5,1.75,2.

This is a five-setting NUMERICAL continuation with a free interior node,
not a uniform theorem in rho or any h->0 refinement. Sources are computed
from the actual original G2STAR/P-P^-1 native faces and full N1 derivative.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import svdvals
from scipy.optimize import least_squares
from scipy.optimize._numdiff import approx_derivative
from check_full42_n1_single_internal import problem
from full_n1_euler_analytic import unit_test

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json",type=Path)
    args=parser.parse_args()
    unit_test()
    continuation=[]
    prev=None
    for w in (1.,1.25,1.5,1.75,2.):
        h,base,psi,weights,fields,euler=problem(2,[1.,w])
        init=np.zeros(42) if prev is None else prev
        initial_source=float(np.max(abs(euler(init))))
        sol=least_squares(euler,init,method='trf',x_scale='jac',
                          max_nfev=45,ftol=1e-12,xtol=1e-12,gtol=1e-12)
        residual,src,nodes=euler(sol.x,True)
        source_inf=float(np.max(abs(residual)))
        if source_inf>2e-11:raise ArithmeticError((w,source_inf))
        spectrum=svdvals(approx_derivative(euler,sol.x,method='3-point',abs_step=5e-6))
        if spectrum[-1]<.043:raise ArithmeticError((w,spectrum[-1]))
        if any(np.linalg.matrix_rank(sum(np.outer(v,v) for v in nd['v']))!=2 for nd in nodes[:-1]):
            raise ArithmeticError("lost both independent REAL material gradients")
        continuation.append(dict(time_PF_ratio=w,source_before=initial_source,
              source_after=source_inf,
              numerical_min_singular=float(spectrum[-1]),
              max_field_change=float(max(abs(sol.x))),
              max_original_f=float(max(abs(src['f']))),
              max_two_CAR_q=float(max(abs(src['q']))),
              full42_numerical_root=True))
        prev=sol.x.copy()
    content=json.dumps(dict(
      status="PASS_FIVE_POINT_NUMERICAL_NATIVE_N1_FULL42_PF_TIME_CONTINUATION",
      source="same original complete cap-one Golden CQ and full six-face STAR",
      original_site_weights="positive time-slice PF [1,rho], constant in each spatial slice",
      points=continuation,
      scope=dict(continuous_interval_root_theorem=False,
                actual_four_dimensional_AF_descendant_weights=False,
                uniform_refinement=False,
                validated_interval_Newton=False,
                physical_Book03_selected=False,GR_closed=False)),indent=2)+"\n"
    print(content,end="")
    if args.json:args.json.write_text(content,encoding="utf-8")
if __name__=="__main__":main()
