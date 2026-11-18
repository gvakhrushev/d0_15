#!/usr/bin/env python3
"""Integer-ball certificate of positive G powers at ±2^-1618, error <2^-4852.

Heuristic continued-fraction candidate is not evidence. Certifier uses exact
integer Euclidean balls and alternating rational trigonometric bounds.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
from hashlib import sha256
import json,mpmath as mp
P=Path(__file__).resolve().parent;n=1618;B=4852;prec=2*B+320;S=1<<prec
# Candidate proposal only; convergence is independently certified below.
def candidate(sign):
 with mp.workprec(4*B+256):
  p=(mp.sqrt(5)-1)/2;gamma=mp.asin(p)/(2*mp.pi);target=(sign*mp.power(2,-n)/(2*mp.pi))%1;x=gamma;p0,p1=0,1;q0,q1=1,0;step=0
  while True:
   a=int(mp.floor(x));pn=a*p1+p0;qn=a*q1+q0;step+=1
   if qn.bit_length()>=B+24:
    j=int(mp.floor(target*qn+mp.mpf('0.5')));k=(j*pow(pn,-1,qn))%qn
    if k>0:return k,step
   p0,p1=p1,pn;q0,q1=q1,qn;x=1/(x-a)
def taylor(start,cosine):
 t=F(1,2**n);term=start;total=F(0);i=0
 while True:
  total+=term;term=-term*t*t/((2*i+1)*(2*i+2) if cosine else (2*i+2)*(2*i+3))
  if abs(term)<F(1,2**(B+80)):
   lo,hi=sorted((total,total+term));return lo.numerator*S//lo.denominator,-((-hi.numerator*S)//hi.denominator),i+1
  i+=1
co0,co1,nc=taylor(F(1),True);si0,si1,ns=taylor(F(1,2**n),False)
root=isqrt(5*S*S);p0=(root-S)//2;p1=-((-(root+1-S))//2);a0=isqrt(p0*S);a1=isqrt(p1*S)+1;assert p1-p0<=2 and a1-a0<=3
# Exact complex rotations have norm one. Centers are floored to the lattice;
# Euclidean error radius r obeys r_new<=r1+r2+ceil(r1*r2/S)+2.
def mul(x,y):
 c1,s1,r1=x;c2,s2,r2=y
 return ((c1*c2-s1*s2)//S,(s1*c2+c1*s2)//S,r1+r2+(r1*r2+S-1)//S+2)
def power(k):
 out=(S,0,0);base=(a0,p0,4)
 while k:
  if k&1:out=mul(out,base)
  k//=2
  if k:base=mul(base,base)
 return out
rot={}
for sign,name in ((1,'plus'),(-1,'minus')):
 print('candidate',name,flush=True);k,steps=candidate(sign);print('certifying',name,'bits',k.bit_length(),flush=True);c,s,r=power(k);st=(si0,si1) if sign==1 else (-si1,-si0)
 e=max(abs(c-co0),abs(c-co1))+max(abs(s-st[0]),abs(s-st[1]))+2*r;assert e*(1<<B)<S
 rot[name]={'power_hex':hex(k),'power_bit_length':k.bit_length(),'center_cos_hex':hex(c),'center_sin_hex':hex(s),'error_ball_radius_hex':hex(r),'operator_error_bound_numerator_hex':hex(e),'norm_error_strict_lt':'2^-4852','candidate_cf_steps':steps}
 print('PASS',name,flush=True)
kp=int(rot['plus']['power_hex'],16);km=int(rot['minus']['power_hex'],16);assert kp>0 and km>0
out={'status':'PASS_SUFFICIENT_POSITIVE_ENDPOINT_G_POWERS','t':'2^-1618','each_rotation_operator_error_strict_lt':'2^-4852','integer_ball_precision_bits':prec,'target_cos_bounds_hex':[hex(co0),hex(co1)],'target_sin_bounds_hex':[hex(si0),hex(si1)],'cos_taylor_terms':nc,'sin_taylor_terms':ns,'rotations':rot,'actual_target_t_and_gram_scope':'fixed retained z=2^-20, empty old prefix rank=TrA=1 witness; also works for any r/TrA<=1','physical_C_closed':False,'GR_closed':False,'source_sha256':{str(Path(__file__).resolve()):sha256(Path(__file__).read_bytes()).hexdigest()}}
(P/'SUFFICIENT_ENDPOINT_G_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'power_bits':[kp.bit_length(),km.bit_length()],'precision_bits':prec}),flush=True)
