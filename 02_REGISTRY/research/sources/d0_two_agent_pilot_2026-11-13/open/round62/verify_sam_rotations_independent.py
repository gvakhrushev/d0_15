#!/usr/bin/env python3
"""Independently verify both saved powers using integer Euclidean error balls."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;cert=json.loads((P/'FINITE_SAM_ROTATION_CERTIFICATE.json').read_text());assert cert['status']=='PASS_FINITE_POSITIVE_G_POWERS_SAM_ENDPOINTS'
for f,h in cert['source_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==h
bits=6856;S=1<<bits;root=isqrt(5*S*S);plow=(root-S)//2;phigh=-((-(root+1-S))//2);alow=isqrt(plow*S);ahigh=isqrt(phigh*S)+1
assert phigh-plow<=2 and ahigh-alow<=3
# Real and imaginary centres plus a rigorous Euclidean error radius in units
# 1/S. Exact rotations have modulus one. Multiplication errors obey
# r_new <= r1+r2+ceil(r1*r2/S)+2, including both rounded components.
def multiply(x,y):
 c1,s1,r1=x;c2,s2,r2=y
 return ((c1*c2-s1*s2)//S,(s1*c2+c1*s2)//S,r1+r2+(r1*r2+S-1)//S+2)
def power(k):
 x=(S,0,0);base=(alow,plow,4)
 while k:
  if k&1:x=multiply(x,base)
  k//=2
  if k:base=multiply(base,base)
 return x
def taylor(start,cosine):
 t=F(1,2**20);term=start;total=F(0);i=0
 while True:
  total+=term;term=-term*t*t/((2*i+1)*(2*i+2) if cosine else (2*i+2)*(2*i+3))
  if abs(term)<F(1,2**3360):
   l,u=sorted((total,total+term));return l.numerator*S//l.denominator,-((-u.numerator*S)//u.denominator)
  i+=1
co=taylor(F(1),True);si=taylor(F(1,2**20),False);out={}
for label,sign in (('plus',1),('minus',-1)):
 k=int(cert['rotations'][label]['power_hex'],16);assert k>0;c,s,r=power(k);target=si if sign>0 else (-si[1],-si[0]);e=max(abs(c-co[0]),abs(c-co[1]))+max(abs(s-target[0]),abs(s-target[1]))+2*r
 assert e*(1<<3300)<S
 out[label]={'power_bits':k.bit_length(),'ball_radius_bits':r.bit_length(),'certified_norm_error_lt_pow2':bits-e.bit_length()}
result={'status':'PASS_INDEPENDENT_INTEGER_BALL_SAM_ROTATIONS','precision_bits':bits,'rotations':out,'all_errors_strict_lt':'2^-3300','candidate_and_prior_rectangular_intervals_not_trusted':True,'physical_price_accuracy_proved':False,'GR_closed':False}
(P/'FINITE_SAM_ROTATIONS_INDEPENDENT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
