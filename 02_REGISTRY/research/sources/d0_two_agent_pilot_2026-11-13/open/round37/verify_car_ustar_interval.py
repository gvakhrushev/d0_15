#!/usr/bin/env python3
"""Independent outward-integer certificate of 8kθ≈−θ/2."""
from pathlib import Path
from hashlib import sha256
from math import isqrt
import json
P=Path(__file__).resolve().parent;f=P/'CAR_USTAR_NATIVE.json';data=json.loads(f.read_text());k=int(data['k']);bits=12800;S=1<<bits
# Use different precision and independently spelled interval arithmetic, with
# no floating-point operations, and no import of the owning phase routine.
root5=isqrt(5*S*S);p=( (root5-S)//2, (root5+2-S)//2 )
a=(isqrt(p[0]*S),isqrt(p[1]*S)+1)
C=(isqrt(((S+a[0])*S)//2),isqrt(((S+a[1])*S)//2)+1)
T=(-isqrt(((S-a[0])*S)//2)-1,-isqrt(((S-a[1])*S)//2))
def neg(x):return (-x[1],-x[0])
def plus(x,y):return (x[0]+y[0],x[1]+y[1])
def product(x,y):
 v=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]);return min(v)//S,-((-max(v))//S)
def cmul(x,y):return (plus(product(x[0],y[0]),neg(product(x[1],y[1]))),plus(product(x[0],y[1]),product(x[1],y[0])))
acc=((S,S),(0,0));base=(a,p);m=8*k
while m:
 if m&1:acc=cmul(acc,base)
 m>>=1
 if m:base=cmul(base,base)
c,s=acc;error=max(abs(c[0]-C[1]),abs(c[1]-C[0]))+max(abs(s[0]-T[1]),abs(s[1]-T[0]));assert error>0 and (error<<4096)<=S
cert=data['certificate'];bits1=cert['precision_bits'];assert bits1>bits;factor=1<<(bits1-bits)
for own,name in [(c,'actual_cos_endpoints_hex'),(s,'actual_sin_endpoints_hex'),(C,'target_cos_endpoints_hex'),(T,'target_sin_endpoints_hex')]:
 other=[int(x,16) for x in cert[name]]
 assert own[0]*factor<=other[1] and other[0]<=own[1]*factor,name
out={'status':'PASS_INDEPENDENT_OUTWARD_INTEGER_HALF_ANGLE_CERTIFICATE','input_sha256':sha256(f.read_bytes()).hexdigest(),'k_binary_length':k.bit_length(),'independent_precision_bits':bits,'builder_precision_bits':bits1,'independent_L1_error_strictly_below':'2^-'+str(bits-error.bit_length()),'required_error_le':'2^-4096','rotation_operator_and_ustar_state_error_le':'2^-4096','float_used_in_certificate':False,'actual_and_target_enclosures_intersect_at_distinct_precisions':True,'GR_closed':False}
(P/'CAR_USTAR_INTERVAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
