"""Perturbed registered-controller Euler equations and source error bound.

The test consumes the previously verified finite NC1 program. It constructs a
nonnegative mathematical W for two recorded sectors; no Book valuation is
identified with this illustrative tariff.
"""
import json
import math
import runpy
from pathlib import Path

root=Path(__file__).parent
base=runpy.run_path(str(root/'check_balanced_controller_source.py'))
p,r,s,ell=(base[k] for k in ('p','r','s','ell'))
f,fp,build,observed=(base[k] for k in ('f','fp','build','observed_ledger'))
pi=0.42
weights=(1-pi,pi)
coeff=(0.01,-0.008)
eta=0.1
u=tuple(1/(1+math.exp(ell*(1+x/r))) for x in coeff)
assert all(eta < x < 1-eta for x in u)
assert max(abs(r*fp(x)+a) for x,a in zip(u,coeff))<1e-13
epsilon=math.sqrt(sum(w*a*a for w,a in zip(weights,coeff)))
displacement=math.sqrt(sum(w*(x-r)**2 for w,x in zip(weights,u)))
m=4*r/ell
assert displacement<=epsilon/m
score=max(1/pi,1/(1-pi))
entropy_error=abs(r*(f(u[1])-f(u[0])))
entropy_bound=ell*score*epsilon**2/(32*r*eta*(1-eta))
assert entropy_error<=entropy_bound
fisher=1/(pi*(1-pi))
moment4=sum(w*a**4 for w,a in zip(weights,coeff))
fisher_bound=ell/(8*r)*math.sqrt(fisher*moment4)
assert entropy_error<=fisher_bound
assert all(f(x)<=ell*fp(x)**2/8+1e-15 for x in u)
supscore_bound=ell*score*epsilon**2/(8*r)
assert entropy_error<=supscore_bound
# A retained pure flag sqrt(1-pi)|0>+sqrt(pi)|1> saturates the
# elementary Cauchy bound I <= 4||D psi||^2 for this chart.
amplitude_derivative_norm=math.sqrt(1/(4*(1-pi))+1/(4*pi))
assert abs(fisher-4*amplitude_derivative_norm**2)<1e-12
for t in (0,1):
    observed_result=observed(build(u[t],t,shared=True)[0])
    assert abs(observed_result-(f(u[t])+r*s+2*p*s*t))<1e-12

# Keep both T sectors. The additive constant 0.02 makes W nonnegative on
# the whole unit square; it does not change any derivative.
def full(x):
    active=(1-x)*(f(u[0])+r*s)+x*(f(u[1])+r*s+2*p*s)
    extra=0.02+(1-x)*coeff[0]*(u[0]-r)+x*coeff[1]*(u[1]-r)
    return r*active+extra
direct_w=coeff[1]*(u[1]-r)-coeff[0]*(u[0]-r)
analytic=2*p**6+r*(f(u[1])-f(u[0]))+direct_w
eps=1e-6
assert abs((full(pi+eps)-full(pi-eps))/(2*eps)-analytic)<1e-9
assert min(full(0),full(1))>=0
print(json.dumps({
 'schema':'d0.controller-stability-bound/1','status':'PASS',
 'tested_recorded_sectors':2,'stationary_u':u,
 'gradient_L2':epsilon,'displacement_L2':displacement,
 'displacement_bound':epsilon/m,'score_bound':score,
 'registered_entropy_source_error':entropy_error,
 'registered_entropy_source_bound':entropy_bound,
 'fisher_information_for_pi':fisher,
 'fourth_moment_of_weighted_controller_gradient':moment4,
 'fisher_source_bound_without_min_probability':fisher_bound,
 'bounded_score_source_bound_without_compact_u':supscore_bound,
 'retained_amplitude_derivative_norm':amplitude_derivative_norm,
 'direct_physical_tariff_source':direct_w,
 'source_baseline':2*p**6,'full_reduced_source':analytic,
 'physical_tariff_is_illustrative_only':True,'GR_closed':False
},indent=2))
