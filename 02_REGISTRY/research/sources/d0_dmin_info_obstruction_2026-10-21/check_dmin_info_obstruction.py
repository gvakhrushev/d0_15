#!/usr/bin/env python3
import json, math
p=(math.sqrt(5.0)-1.0)/2.0
phi=1/p
checks=[]
def req(c,n):
    if not c: raise ArithmeticError(n)
    checks.append(n)
L_F,L_R=1,2
dI_reduction=-(L_R-L_F)
dI_increase=(L_R-L_F)
req(dI_reduction==-1,"F0 reduction gain difference is -1")
req(dI_increase==1,"F0 increase convention difference is +1")
dI_amp=1.5
dI_prob=2.0
dI_extra=1.0
req(dI_reduction!=dI_amp,"code-reduction Info fails amplitude binding")
req(dI_reduction!=dI_prob,"code-reduction Info fails probability binding")
req(dI_reduction!=dI_extra,"code-reduction Info fails extra-marker binding")
req(dI_increase!=dI_amp,"reverse code difference still fails amplitude binding")
req(dI_increase!=dI_prob,"reverse code difference fails probability binding")
req(dI_increase==dI_extra,"reverse code difference matches only extra-marker type")
S_F=-math.log(p,phi)
S_R=-math.log(math.sqrt(p),phi)
req(abs(S_F-1)<1e-14 and abs(S_R-0.5)<1e-14,
    "native Kraus scalar exponents are net prices 1 and 1/2")
I_F=L_F-S_F
I_R=L_R-S_R
req(abs((I_R-I_F)-1.5)<1e-14,
    "cost minus native scalar exponent yields required 3/2 amplitude gain")
print(json.dumps({
 "status":"PASS","check_count":len(checks),"checks":checks,
 "literal_Dmin":{"F":L_F,"R":L_R,"delta_R_minus_F":1},
 "candidate_Info_delta":{
   "prior_minus_posterior":dI_reduction,
   "posterior_minus_prior":dI_increase},
 "required_delta":{"amplitude":dI_amp,"probability":dI_prob,"extra_marker":dI_extra},
 "native_scalar_exponent":{"S_F":S_F,"S_R":S_R,"I_F":I_F,"I_R":I_R},
 "scope":{"naive_Dmin_Info_rejected":True,"general_native_Info_undefined":True,"GR_closed":False}
},indent=2,sort_keys=True))
