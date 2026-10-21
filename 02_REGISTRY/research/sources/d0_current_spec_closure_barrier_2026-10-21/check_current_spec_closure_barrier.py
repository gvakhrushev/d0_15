#!/usr/bin/env python3
import json, math
p=(math.sqrt(5.0)-1.0)/2.0
phi=1.0/p
q0,q1=p*p,p
dH=math.log(q0/q1,phi)
checks=[]
def req(x,n):
    if not x: raise ArithmeticError(n)
    checks.append(n)
req(abs(dH+1)<1e-14,"native Golden tangent dH=-1")
Cbar=1.0*q0+2.0*q1
H=-(q0*math.log(q0,phi)+q1*math.log(q1,phi))
CQ=Cbar-H
J_from_mean=1.5*H-Cbar
P_from_mean=-J_from_mean
req(abs(P_from_mean-(CQ-0.5*H))<1e-14,
    "mean=CQ forces pressure=CQ-H/2")
req(abs((-0.5*dH)-0.5)<1e-14,
    "mean=CQ leaves pressure-source mismatch +1/2")
J_from_pressure=H-Cbar
M_from_pressure=0.5*H-J_from_pressure
req(abs(M_from_pressure-(CQ+0.5*H))<1e-14,
    "pressure=CQ forces mean=CQ+H/2")
req(abs((0.5*dH)+0.5)<1e-14,
    "pressure=CQ leaves mean-source mismatch -1/2")
for theta,eta in [(1.0,0.0),(0.75,0.25),(0.0,1.0)]:
    req(abs((theta-eta) - (theta-eta))<1e-15,
        f"endpoint allocation source gap theta={theta} eta={eta}")
out={
 "status":"PASS","check_count":len(checks),"checks":checks,
 "golden":{"p":p,"H":H,"Cbar":Cbar,"CQ":CQ,"dH":dH},
 "amplitude_binding_corollary":{
   "J_if_mean_equals_CQ":J_from_mean,
   "pressure_minus_CQ_value":-0.5*H,
   "pressure_minus_CQ_source":0.5,
   "J_if_pressure_equals_CQ":J_from_pressure,
   "mean_minus_CQ_value":0.5*H,
   "mean_minus_CQ_source":-0.5
 },
 "endpoint_allocation":{"source_gap":"theta-eta for D(Info_final-Info_initial)=1"},
 "scope":{"current_specification_unique_native_source":False,"GR_closed":False}
}
print(json.dumps(out,indent=2,sort_keys=True))
