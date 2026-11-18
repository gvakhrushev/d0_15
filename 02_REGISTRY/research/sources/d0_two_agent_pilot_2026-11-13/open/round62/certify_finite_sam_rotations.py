#!/usr/bin/env python3
"""Find positive G powers near R(±2^-20); exact integer certification.

The 3300-bit certificate is an example. Its sufficiency for a physical
normalized price depends on actual old Gram, z, displacement and gain.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import importlib.util,json,math,sys,time
import mpmath as mp
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');owner=D/'round14/certify_boolean_angle.py';spec=importlib.util.spec_from_file_location('b62_owner',owner);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
def candidate(bits,t_power,sign):
 with mp.workprec(4*bits+256):
  p=(mp.sqrt(5)-1)/2;gamma=mp.asin(p)/(2*mp.pi);target=(sign*mp.power(2,-t_power)/(2*mp.pi))%1;x=gamma;p0,p1=0,1;q0,q1=1,0;step=0
  while True:
   a=int(mp.floor(x));pn=a*p1+p0;qn=a*q1+q0;step+=1
   if qn.bit_length()>=bits+24:
    j=int(mp.floor(target*qn+mp.mpf('0.5')));k=(j*pow(pn,-1,qn))%qn
    if k>0:return k,step
   p0,p1=p1,pn;q0,q1=q1,qn;x=1/(x-a)
def trig_intervals(t_power,bits,precision):
 t=F(1,2**t_power);z=t*t
 def series(start,cosine):
  term=start;total=F(0);n=0
  while True:
   total+=term
   term=-term*z/((2*n+1)*(2*n+2) if cosine else (2*n+2)*(2*n+3))
   if abs(term)<F(1,2**(bits+60)):
    a,b=sorted((total,total+term));scale=1<<precision
    return (a.numerator*scale//a.denominator,-((-b.numerator*scale)//b.denominator)),n+1
   n+=1
 cos,nc=series(F(1),True);sin,ns=series(t,False);return cos,sin,nc,ns
def distance(x,y):return max(abs(x[0]-y[1]),abs(x[1]-y[0]))
bits=3300;t_power=20;prec=4*bits+256;targets=trig_intervals(t_power,bits,prec);cos,sin,nc,ns=targets;out={}
for sign,label in ((1,'plus'),(-1,'minus')):
 print('searching',label,flush=True);k,steps=candidate(bits,t_power,sign);print('certifying',label,'bits',k.bit_length(),flush=True)
 scale,c,s=mod.phase._rotation_intervals(k,prec);assert scale==1<<prec;target_s=sin if sign==1 else (-sin[1],-sin[0]);error=distance(c,cos)+distance(s,target_s);assert error*(1<<bits)<scale
 out[label]={'power_hex':hex(k),'power_bit_length':k.bit_length(),'positive':k>0,'cos_endpoints_hex':[hex(x) for x in c],'sin_endpoints_hex':[hex(x) for x in s],'operator_error_bound_numerator_hex':hex(error),'denominator_power_of_two':prec,'strict_error_lt':'2^-3300','candidate_cf_steps':steps}
 print('PASS',label,flush=True)
np=int(out['plus']['power_hex'],16);nm=int(out['minus']['power_hex'],16);assert np>0 and nm>0
paths=[Path(__file__).resolve(),owner,Path(mod.phase.__file__)]
result={'status':'PASS_FINITE_POSITIVE_G_POWERS_SAM_ENDPOINTS','rotation_angle_t':'2^-20','strict_error_per_rotation_lt':'2^-3300','integer_interval_precision_bits':prec,'cos_target_endpoints_hex':[hex(x) for x in cos],'sin_positive_target_endpoints_hex':[hex(x) for x in sin],'target_certification':'Alternating exact rational Taylor enclosures, no pi/float in certification','cos_terms':nc,'sin_terms':ns,'rotations':out,'both_endpoints_same_pre_plus_post_gate_count_hex':hex(np+nm),'operator_error_per_conjugated_endpoint_lt':'2^-3299','sample_not_a_complete_physical_price_certificate':True,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'GR_closed':False}
(P/'FINITE_SAM_ROTATION_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'power_bits':[np.bit_length(),nm.bit_length()],'precision':prec}),flush=True)
