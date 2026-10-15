#!/usr/bin/env python3
"""Exact asymptotic coefficient and floating diagnostics; not interval certificates."""
import json
import numpy as np
from fractions import Fraction

def shape_response(L, beta):
    k=np.arange(L,dtype=np.float64)
    a=4*L**2*np.sin(np.pi*k/L)**2
    ans=[]
    for q in (4.,.25):
        e=a/q
        w=np.exp(-beta*e)
        ans.append(float(np.dot(e,w)/np.sum(w)))
    return 2*(ans[0]-ans[1])

# log I0(x) = x - 1/2 log(2 pi x) + 1/(8x) + O(x^-2)
# x=2 beta/(h^2 q), hence d_shape H = (q1-q2)h^2/(8 beta^2)+...
coefficient=(Fraction(4)-Fraction(1,4))/8
if coefficient!=Fraction(15,32):raise ValueError('wrong coefficient')
rows=[]
for L in (128,256,512,1024,2048,4096):
    f=shape_response(L,1/L)
    rows.append({'L':L,'beta':1/L,'shape_source':f,'limit':float(coefficient)})
if abs(rows[-1]['shape_source']-float(coefficient))>.001:raise ValueError('diagnostic convergence failure')
print(json.dumps({'scope':'exact_coefficient_plus_floating_diagnostic_not_interval',
 'analytic_result':'beta=h gives nonzero limiting shape source 15/32',
 'coefficient':str(coefficient),'rows':rows,'native_temperature_law':False},indent=2,sort_keys=True))
