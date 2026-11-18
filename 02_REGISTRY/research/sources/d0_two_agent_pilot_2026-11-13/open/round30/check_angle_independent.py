#!/usr/bin/env python3
"""Certify the given k by independent MSB dyadic interval powering.
No continued fractions, floating point or owner interval routine are used.
"""
from pathlib import Path
from math import isqrt
import json,hashlib
P=Path(__file__).resolve().parent
A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round14')
path=A/'NATIVE_BOOLEAN_ANGLE.json';data=json.loads(path.read_text());k=int(data['k']);prec=data['certificate']['precision_bits'];bits=data['certificate']['certified_error_bits']
assert k.bit_length()==4111 and prec==16640 and bits==4096
S=1<<prec
# floor/ceil rational endpoints. sqrt5 in [q,q+1]/S; p=(sqrt5−1)/2.
q=isqrt(5*S*S);plo=(q-S)//2;phi=(q+1-S+1)//2
assert 0<plo<=phi<S and (q*q<=5*S*S<(q+1)*(q+1))
alo=isqrt(plo*S);ahi=isqrt(phi*S)+1
assert alo*alo<=plo*S and (ahi-1)**2<=phi*S<ahi**2
# A second independently organised interval engine: left-to-right power,
# no unit-circle clamping, and all multiplication endpoints rounded outward.
def pmul(x,y):
 z=[x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]]
 return min(z)//S,-((-max(z))//S)
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[1],-x[0])
def cmul(x,y):
 return (add(pmul(x[0],y[0]),neg(pmul(x[1],y[1]))), add(pmul(x[0],y[1]),pmul(x[1],y[0])))
def msb_power(exponent):
 result=((S,S),(0,0));base=((alo,ahi),(plo,phi))
 for bit in bin(exponent)[2:]:
  result=cmul(result,result)
  if bit=='1':result=cmul(result,base)
 return result
c2,s2=msb_power(2*k);c4,s4=cmul((c2,s2),(c2,s2));c8,s8=cmul((c4,s4),(c4,s4))
r=isqrt(S*S//2);assert 2*r*r<=S*S<2*(r+1)*(r+1)
maxdiff=lambda v,target:max(abs(v[0]-target[1]),abs(v[1]-target[0]))
e2=maxdiff(c2,(r,r+1))+maxdiff(s2,(r,r+1))
e4=max(abs(c4[0]),abs(c4[1]))+max(abs(s4[0]-S),abs(s4[1]-S))
e8=max(abs(c8[0]+S),abs(c8[1]+S))+max(abs(s8[0]),abs(s8[1]))
assert max(e2,e4,e4+e8)*(1<<bits)<=S
# Independently computed enclosures must intersect the published enclosures.
for multiple,c,s in [(2,c2,s2),(4,c4,s4),(8,c8,s8)]:
 recorded=data['certificate']['rotation_enclosures'][str(multiple)]
 for field,current in [('cosine_endpoints_hex',c),('sine_endpoints_hex',s)]:
  old=[int(x,16) for x in recorded[field]];assert max(old[0],current[0])<=min(old[1],current[1])
# Exact error budgets by integer comparison; no printed huge endpoints needed.
res={'status':'PASS_INDEPENDENT_DYADIC_MSB_POWER_CERTIFICATE','input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'k_bits':k.bit_length(),'precision_bits':prec,'error_bits':bits,'search_replayed':False,
 'method':'exact integer square roots + directed dyadic MSB power for 2k, followed by two independent interval squares; no unit-circle clamping',
 'endpoint_intersections_with_owner':True,'H_X_CCX_L1_upper_at_most_2^-4096':True,
 'error_numerator_bit_lengths':{'2k':e2.bit_length(),'4k':e4.bit_length(),'8k':e8.bit_length(),'CCX_sum':(e4+e8).bit_length()},
 'full_physical_READY_or_writer_compiled':False,'GR_closed':False}
(P/'INDEPENDENT_ANGLE_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
