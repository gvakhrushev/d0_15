#!/usr/bin/env python3
"""B57 independent all-column interval certificate for four positive G powers.

Candidate selection is heuristic, never used as evidence. Final checks use
only integer square roots, outward-rounded integer interval multiplication,
and exact algebraic targets. No prior certificate files are written.
"""
from pathlib import Path
from math import isqrt
from hashlib import sha256
import importlib.util,json,sys,time
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
owner=D/'round14/certify_boolean_angle.py';spec=importlib.util.spec_from_file_location('b57_angle_owner',owner);o=importlib.util.module_from_spec(spec);sys.modules[spec.name]=o;spec.loader.exec_module(o)
# Independent fixed-point interval arithmetic. A component is [lo,hi]/S.
def calc(k,bits):
 S=1<<bits
 def up(n):return -((-n)//S)
 def add(x,y):return x[0]+y[0],x[1]+y[1]
 def neg(x):return -x[1],-x[0]
 def prod(x,y):
  v=[x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]]
  return min(v)//S,up(max(v))
 def clamp(x):
  r=(max(-S,x[0]),min(S,x[1]));assert r[0]<=r[1];return r
 def cmul(z,w):return (clamp(add(prod(z[0],w[0]),neg(prod(z[1],w[1])))),clamp(add(prod(z[0],w[1]),prod(z[1],w[0]))))
 sqrt5=isqrt(5*S*S);p=((sqrt5-S)//2, -((-(sqrt5+1-S))//2)); a=(isqrt(p[0]*S),isqrt(p[1]*S)+1)
 base=(a,p);val=((S,S),(0,0));n=k
 while n:
  if n&1:val=cmul(val,base)
  n//=2
  if n:base=cmul(base,base)
 z2=cmul(val,val);z4=cmul(z2,z2);z8=cmul(z4,z4);z12=cmul(z8,z4);z14=cmul(z12,z2)
 return S,{2:z2,14:z14,4:z4,12:z12}
def dist(c,target):return max(abs(c[0]-target[1]),abs(c[1]-target[0]))
def certify(k,precision,targetbits=7432):
 S,results=calc(k,precision);t=isqrt((S*S)//2);rt=(t,t+1);neg_rt=(-t-1,-t);zero=(0,0);one=(S,S);neg_one=(-S,-S)
 targets={2:(rt,rt),14:(rt,neg_rt),4:(zero,one),12:(zero,neg_one)}
 out={}
 for m,(c,s) in results.items():
  tc,ts=targets[m];err=dist(c,tc)+dist(s,ts)
  assert err*(1<<targetbits)<S,(m,err.bit_length(),precision)
  out[str(m)]={'exponent_hex':hex(m*k),'exponent_bit_length':(m*k).bit_length(),'cos_interval_hex':[hex(x) for x in c],'sin_interval_hex':[hex(x) for x in s],'denominator_pow2':precision,'target_cos':{2:'+sqrt(1/2)',14:'+sqrt(1/2)',4:'0',12:'0'}[m],'target_sin':{2:'+sqrt(1/2)',14:'-sqrt(1/2)',4:'+1',12:'-1'}[m],'operator_error_bound_num_hex':hex(err),'operator_error_bound_denominator_pow2':precision,'operator_error_strictly_less_than':'2^-7432'}
 return out
start=time.time();print('finding candidate',flush=True)
k,proposal=o.candidate(7440);assert isinstance(k,int) and k>0
print('candidate ready; bits',k.bit_length(),'certifying',flush=True)
prec=max(18000,k.bit_length()+7432+192)
results=certify(k,prec)
# Independently use the owner's direct actual-multiple interval evaluator,
# verify both paths enclose the same rotations and also satisfy strict bound.
for m,z in results.items():
 m=int(m);scale,c,s=o.phase._rotation_intervals(m*k,prec)
 assert scale==1<<prec
 c2=[int(v,16) for v in z['cos_interval_hex']];s2=[int(v,16) for v in z['sin_interval_hex']]
 assert max(c[0],c2[0])<=min(c[1],c2[1]) and max(s[0],s2[0])<=min(s[1],s2[1])
 S=1<<prec;t=isqrt((S*S)//2);tar={2:((t,t+1),(t,t+1)),14:((t,t+1),(-t-1,-t)),4:((0,0),(S,S)),12:((0,0),(-S,-S))}[m]
 E=dist(c,tar[0])+dist(s,tar[1]);assert E*(1<<7432)<S
 z['owner_direct_multiplier_operator_error_num_hex']=hex(E)
 print('direct and independent integer intervals pass multiplier',m,flush=True)
L=int(json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text())['W_primitive_call_count_decimal']);assert L.bit_length()==4188 and L*4<(1<<4190)
files=[Path(__file__).resolve(),owner,Path(o.phase.__file__),D/'round25/GLOBAL_H1_PLAN.json']
out={'status':'PASS_CERTIFIED_FOUR_POSITIVE_G_POWERS','k_hex':hex(k),'k_bit_length':k.bit_length(),'candidate_bits':7440,'candidate_metadata':proposal,'precision_bits':prec,'rotation_bounds':results,'rotation_norm_error_each_strict_lt':'2^-7432','max_four_rotation_error_strict_lt':'2^-7430','all_old_replacements_le_L_conditional_total_strict_lt':'2^-3242','old_W_L_bit_length':L.bit_length(),'proof':'Each exact G component enclosed by outward integer intervals; actual exponent m*k propagated. Matrix norm is bounded by |Δcos|+|Δsin|. Targets are exact square-root/integers, not float or pi. Candidate finder is not evidence.','independent_interval_path_and_owner_direct_agree':True,'conditional_global_error_requires_complete_macro_compiler':True,'physical_C_closed':False,'GR_closed':False,'input_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in files},'runtime_seconds':round(time.time()-start,3)}
(P/'GADGET_G_POWER_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'k_bit_length':k.bit_length(),'precision_bits':prec,'elapsed_seconds':out['runtime_seconds']}),flush=True)
