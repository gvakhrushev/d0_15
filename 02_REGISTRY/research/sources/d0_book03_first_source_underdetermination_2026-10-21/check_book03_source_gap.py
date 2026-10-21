#!/usr/bin/env python3
import json, math

SQRT5 = math.sqrt(5.0)
p = (SQRT5 - 1.0)/2.0
phi = 1.0/p

checks=[]
def req(cond,name):
    if not cond:
        raise ArithmeticError(name)
    checks.append(name)

q0=p*p
q1=p
req(abs(q0+q1-1.0)<1e-15,"golden probabilities normalize")
req(abs(math.log(q0,phi)+2.0)<1e-14,"log_phi q0=-2")
req(abs(math.log(q1,phi)+1.0)<1e-14,"log_phi q1=-1")

S0=-0.5*math.log(q0,phi)
S1=-0.5*math.log(q1,phi)
I0=1.0-S0
I1=2.0-S1
req(abs(S0-1.0)<1e-14 and abs(S1-0.5)<1e-14,"amplitude-bound branch prices")
req(abs(I0)<1e-14 and abs(I1-1.5)<1e-14,"nonnegative native Golden gains at J=0")

dH=math.log(q0/q1,phi)
req(abs(dH+1.0)<1e-14,"exact Golden entropy tangent dH=-1")

for dJ in [0.0, 1.0, -math.sqrt(2.0)]:
    d_mean=0.5*dH-dJ
    d_pressure=-dJ
    req(abs((d_mean-d_pressure)+0.5)<1e-14,
        f"first-source gap independent of common mode dJ={dJ}")

d_mean_prob=dH
d_pressure_prob=0.0
req(abs((d_mean_prob-d_pressure_prob)+1.0)<1e-14,
    "probability-binding first-source gap=-1")

def H(e):
    a=q0-e
    b=q1+e
    return -(a*math.log(a,phi)+b*math.log(b,phi))
for h in [1e-5,3e-6,1e-6]:
    sec=(0.5*H(h)-0.5*H(-h))/(2*h)
    req(abs(sec+0.5)<2e-9,"finite-difference mean-source control "+str(h))

out={
 "status":"PASS",
 "check_count":len(checks),
 "checks":checks,
 "native_pair":{"q0":q0,"q1":q1,"C0":1,"C1":2},
 "amplitude_binding":{"I0":I0,"I1":I1,"S0":S0,"S1":S1},
 "tangent":{"dq0":-1,"dq1":1,"dH_phi":dH},
 "first_source_gap":{
   "mean_minus_amplitude_pressure":-0.5,
   "probability_mean_minus_pressure":-1.0,
   "common_mode_derivative_cancels_from_gap":True
 },
 "scope":{
   "same_execution_amplitude_binding_assumed":True,
   "book03_aggregation_selected":False,
   "book03_branch_info_law_selected":False,
   "GR_closed":False
 }
}
print(json.dumps(out,indent=2,sort_keys=True))
