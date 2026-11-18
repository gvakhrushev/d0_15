#!/usr/bin/env python3
"""Independent rational interval certification: no floats, no original interval code."""
from pathlib import Path
from hashlib import sha256
from math import isqrt
import json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round19')
f=D/'CHOI_PREFIX_CERTIFICATE.json'; raw=f.read_bytes(); c=json.loads(raw); B=20500;S=1<<B;fac=1<<(B-c['precision_bits']);assert B>c['precision_bits']
def up(a,b): return -((-a)//b)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[1],a[1]-b[0]
def mul(a,b):
 z=[x*y for x in a for y in b];return min(z)//S,up(max(z),S)
def cmul(a,b):return sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0]))
def rt_fraction(n,d):
 z=isqrt(n*S*S//d);return z,z+1
# Native G has cos=sqrt(phi^-1), sin=phi^-1; independent enclosing arithmetic.
r5=rt_fraction(5,1); p=((r5[0]-S)//2,up(r5[1]-S,2));alo=isqrt(p[0]*S);ahi=isqrt(p[1]*S);a=(alo,ahi+(ahi*ahi<p[1]*S));g=(a,p)
def power(n):
 r=((S,S),(0,0));b=g
 while n:
  if n&1:r=cmul(r,b)
  n//=2
  if n:b=cmul(b,b)
 return r
kb=int(c['boolean_common_power']['k']);ka=int(c['address_power']['k']);x=power(kb); x2=cmul(x,x);x4=cmul(x2,x2);x8=cmul(x4,x4);x16=cmul(x8,x8);v=power(ka);v2=cmul(v,v)
targs={'4':(rt_fraction(1,2),rt_fraction(1,2)), '8':((0,0),(S,S)), '16':((-S,-S),(0,0)), 'address':(rt_fraction(2048,2049),rt_fraction(1,2049))}
records={'4':c['boolean_common_power']['enclosures']['4'],'8':c['boolean_common_power']['enclosures']['8'],'16':c['boolean_common_power']['enclosures']['16'],'address':c['address_power']['enclosure']}; powers={'4':x4,'8':x8,'16':x16,'address':v2}; errs={}
for name in records:
 e=records[name]; native=powers[name];target=targs[name]
 for result,key in [(native[0],'native_cos_hex'),(native[1],'native_sin_hex'),(target[0],'target_cos_hex'),(target[1],'target_sin_hex')]:
  saved=[int(t,16) for t in e[key]];assert saved[0]*fac<=result[0] and result[1]<=saved[1]*fac,(name,key)
 err=sum(max(abs(z[0]-v[1]),abs(z[1]-v[0])) for z,v in zip(native,target));errs[name]=err
assert (errs['4']+errs['16'])*2**4096<=S and (errs['8']+errs['16'])*2**4096<=S and errs['address']*2**4096<=S
bound=errs['address']+16*(errs['4']+errs['16'])+5*(errs['8']+errs['16']);assert bound*2**4091<S
# Check the originally claimed L1 and prefix bound separately as well.
old={}
for n,e in records.items():
 pair=[[int(x,16) for x in e[k]] for k in ('native_cos_hex','native_sin_hex','target_cos_hex','target_sin_hex')];a,b,c0,d=pair
 old[n]=max(abs(a[0]-c0[1]),abs(a[1]-c0[0]))+max(abs(b[0]-d[1]),abs(b[1]-d[0]));assert old[n]==int(e['error_L1_numerator_hex'],16)
assert int(c['prefix_error_L1_numerator_hex'],16)==old['address']+16*(old['4']+old['16'])+5*(old['8']+old['16'])
assert sha256(f.read_bytes()).digest()==sha256(raw).digest()
out={'status':'PASS_INDEPENDENT_INTEGER_INTERVALS','certificate_sha256':sha256(raw).hexdigest(),'bits':B,'native_powers':['4k','8k','16k','2ka'],'all_original_target_and_native_intervals_contain_independent_intervals':True,'prefix_operator_error_lt':'2^-4091','float_used':False,'GR_closed':False}
Path(__file__).with_name('INDEPENDENT_INTERVAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
