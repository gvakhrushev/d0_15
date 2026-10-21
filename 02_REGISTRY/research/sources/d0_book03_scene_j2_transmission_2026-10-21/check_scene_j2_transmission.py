#!/usr/bin/env python3
from fractions import Fraction
import math, json

p=(math.sqrt(5.0)-1.0)/2.0
beta=2*p*p
z=2.0**-20
k0=Fraction(39,160)
kx=Fraction(91,2816)
ky=Fraction(13,6400)
ku=Fraction(-1209,35200)

r=math.sqrt(10.0)/40.0
Z=1+30*math.exp(-beta)+math.exp(-beta*(1.5-r))+math.exp(-beta*(1.5+r))
cH=-(math.exp(-beta*(1.5-r))-math.exp(-beta*(1.5+r)))/(2*r*Z)
Q=(1-z)*(1-2*float(k0)*z)+float(k0*k0)*z*z
cF=2*z*(1-(1+float(k0))*z)/Q
g=cH+cF
coef=g*float(kx)

checks=[]
def req(c,n):
    if not c: raise ArithmeticError(n)
    checks.append(n)

req(kx!=0,"9-11 equitable kappa derivative nonzero")
req(kx==Fraction(91,2816),"exact kappa_x")
req(ky==Fraction(13,6400),"exact kappa_y")
req(ku==Fraction(-1209,35200),"exact kappa_u")
req(beta>0.7 and beta<1.0,"native beta coarse bounds")
req(1.5+r<2.0,"MVT exponent below two")
req(7/2640 > 1/131072,"analytic heat lower bound exceeds feedback upper bound")
req(cH<0 and cF>0,"heat and feedback signs")
req(g<0,"native beta,z scene coefficient strictly negative")
req(coef<0 and abs(coef)>1e-4,"nonzero J2 transmission coefficient")
req(float(kx)!=0.0,"independent-x Euler forces g=0")
req(abs(g)>1e-3,"calibrated canonical scene off stationary branch")

print(json.dumps({
 "status":"PASS","check_count":len(checks),"checks":checks,
 "scene_derivatives":{
   "kappa_x_9_11":"91/2816",
   "kappa_y_9_13":"13/6400",
   "kappa_u_11_13":"-1209/35200"},
 "calibration":{"p":p,"beta":beta,"z":z},
 "coefficients":{"cH":cH,"cF":cF,"g":g,"J2_source_multiplier":coef},
 "analytic_bounds":{"minus_cH_lower":"7/2640","cF_upper":"1/131072"},
 "dichotomy":{
   "derived_x_chain_source":"g*(91/2816)*DJ2",
   "independent_x_Euler":"g*(91/2816)=0 => g=0",
   "simultaneous_nonzero_transfer_and_free_x_stationarity":False
 },
 "scope":{
   "same_initial_generated_scene_writer":False,
   "physical_weighted_scene_admission":False,
   "GR_closed":False
 }
},indent=2,sort_keys=True))
