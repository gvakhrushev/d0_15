#!/usr/bin/env python3
"""Find and independently certify π/3 and final phase compensation powers."""
from pathlib import Path
from hashlib import sha256
from math import isqrt,gcd
import json,mpmath as mp
P=Path(__file__).resolve().parent;BITS=4096;PREC=8448;S=1<<PREC

def propose(K,turn_fn):
 # Numerical CF proposal only. Integer complex-ball certificate below is the
 # sole source of the advertised bound; the turn function may be inexact.
 with mp.workprec(3*BITS+512):
  p=(mp.sqrt(5)-1)/2;gam=mp.acos(mp.sqrt(p))/(2*mp.pi);turn=turn_fn();x=gam
  p0,p1,q0,q1=0,1,1,0;steps=0
  while True:
   ai=int(mp.floor(x));pn=ai*p1+p0;qn=ai*q1+q0;steps+=1
   if qn.bit_length()>=BITS+48 and gcd((1<<K)*pn,qn)==1:
    target=int(mp.nint(turn*qn));inv=pow((1<<K)*pn,-1,qn);k=(target*inv)%qn
    if not k:target+=1;k=(target*inv)%qn
    if k:return k,{'steps':steps,'denominator_bits':qn.bit_length(),'proposal_only':True}
   p0,p1=p1,pn;q0,q1=q1,qn;x=1/(x-ai)

def correction_turn():
 t=mp.mpc(mp.mpf('0.5'),mp.sqrt(3)/2);e=(1-1/mp.sqrt(65568))/2;z=mp.mpc(1)
 for _ in range(8):z*=t*t+t*e;e=e**3
 z=mp.conj(z)/abs(z);return mp.arg(z)/(2*mp.pi)

class I:
 def q(self,n,d=1):assert d>0;return (n*S//d,-((-n*S)//d))
 def add(self,x,y):return (x[0]+y[0],x[1]+y[1])
 def neg(self,x):return (-x[1],-x[0])
 def sub(self,x,y):return self.add(x,self.neg(y))
 def mul(self,x,y):
  z=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]);return (min(z)//S,-((-max(z))//S))
 def div(self,x,y):
  assert y[0]>0;return (min(a*S//b for a in x for b in y),max(-((-a*S)//b) for a in x for b in y))
 def sq(self,x):
  return (0 if x[0]<=0<=x[1] else min(x[0]*x[0],x[1]*x[1])//S, -((-max(x[0]*x[0],x[1]*x[1]))//S))
 def sqrt(self,x):
  assert x[0]>=0;lo=isqrt(x[0]*S);hi=isqrt(x[1]*S);return lo,hi+(hi*hi<x[1]*S)
I=I();one=I.q(1);half=I.q(1,2);s3=I.div(I.sqrt(I.q(3)),I.q(2));c_anchor=I.sqrt(I.q(1,65568));eps=I.div(I.sub(one,c_anchor),I.q(2));assert 0<eps[0]<=eps[1]<S//2
# z=prod_j(t²+t eps_j), eps_{j+1}=eps_j^3. Each g_j has
# Re=(-1+eps_j)/2 and Im=sqrt(3)(1+eps_j)/2.
z=(one,I.q(0));e=eps
for _ in range(8):
 g=(I.div(I.sub(e,one),I.q(2)),I.mul(s3,I.add(one,e)))
 z=(I.sub(I.mul(z[0],g[0]),I.mul(z[1],g[1])),I.add(I.mul(z[0],g[1]),I.mul(z[1],g[0])))
 e=I.mul(I.mul(e,e),e)
assert e[1] < (S >> 6561)
norm=I.sqrt(I.add(I.sq(z[0]),I.sq(z[1])));assert norm[0]>0
corr=(I.div(z[0],norm),I.neg(I.div(z[1],norm))); target_phase=(half,s3)
# Compute certified ball around exact native G^n. Powers have unit modulus;
# one complex multiplication incurs <2/S Euclidean rounding.
s5=isqrt(5*S*S);pp=((s5-S)//2,(s5+2-S)//2);aa=(isqrt(pp[0]*S),isqrt(pp[1]*S)+1)
def mul_ball(x,y):
 c,s,r=x;d,t,u=y;return (c*d-s*t)//S,(c*t+s*d)//S,r+u-((-r*u)//S)+2
def power_ball(n):
 assert n>0;acc=(S,0,0);base=(aa[0],pp[0],aa[1]-aa[0]+pp[1]-pp[0])
 while n:
  if n&1:acc=mul_ball(acc,base)
  n>>=1
  if n:base=mul_ball(base,base)
 c,s,r=acc;return (c-r,c+r),(s-r,s+r)
def check(k,K,target):
 c,s=power_ball((1<<K)*k);tc,ts=target
 err=max(abs(c[0]-tc[1]),abs(c[1]-tc[0]))+max(abs(s[0]-ts[1]),abs(s[1]-ts[0]));assert err>0 and (err<<BITS)<=S
 return {'angle_multiplier':1<<K,'native_cos_hex':[hex(x) for x in c],'native_sin_hex':[hex(x) for x in s],
         'target_cos_hex':[hex(x) for x in tc],'target_sin_hex':[hex(x) for x in ts],
         'L1_error_numerator_hex':hex(err),'strict_error_bits':PREC-err.bit_length()}
k,pk=propose(1,lambda:mp.mpf(1)/6);phase=check(k,1,target_phase)
l,pl=propose(0,correction_turn);correction=check(l,0,corr)
# eps0<1/2 -> eps8<2^-6561; vector residual <2^-3280.
out={'status':'CERTIFIED_FIXED_POINT_ADAPTER_PHASES','precision_bits':PREC,'certified_error_le':'2^-4096','phase_k':str(k),'phase_k_bits':k.bit_length(),'phase_proposal':pk,'phase_certificate':phase,'correction_l':str(l),'correction_l_bits':l.bit_length(),'correction_proposal':pl,'correction_certificate':correction,
     'anchor_overlap':'1/sqrt(65568)','levels':8,'ideal_failure_lt':'2^-6561','ideal_uncorrected_failure_amplitude_lt':'2^-3280',
     'correction_target':'conjugate(product_{j=0..7}(t^2+t eps_j)) / absolute(product), t=exp(i*pi/3), eps_0=(1-c)/2, eps_(j+1)=eps_j^3',
     'proof_arithmetic':'outward dyadic targets and exact integer complex balls; float only in untrusted CF proposals','physical_C_closed':False,'GR_closed':False}
(P/'ADAPTER_PHASE_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'phase_k_bits':k.bit_length(),'phase_error_strict_bits':phase['strict_error_bits'],'correction_l_bits':l.bit_length(),'correction_error_strict_bits':correction['strict_error_bits'],'ideal_failure_lt':out['ideal_failure_lt']},indent=2))
