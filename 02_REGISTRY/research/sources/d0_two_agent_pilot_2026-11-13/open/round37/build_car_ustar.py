#!/usr/bin/env python3
"""CAR U_star: certified owned native word, arbitrary external columns."""
from pathlib import Path
from hashlib import sha256
from math import gcd,isqrt
from fractions import Fraction
import importlib.util,sys,json
import mpmath as mp
P=Path(__file__).resolve().parent
ROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13')
S=ROOT/'02_REGISTRY/research/sources';D=S/'d0_two_agent_pilot_2026-11-13/direct'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
nb=load('b37_native_boolean',D/'round14/native_boolean.py');phase=load('b37_native_phase',S/'d0_native_readiness_amplification_2026-10-24/native_phase.py')

def candidate(bits):
 # Inhomogeneous target 8k*theta/(2pi) = -theta/(4pi) mod 1.
 # This CF calculation only proposes k; no float participates in certificate.
 with mp.workprec(3*bits+512):
  p=(mp.sqrt(5)-1)/2;gamma=mp.acos(mp.sqrt(p))/(2*mp.pi);x=gamma
  p0,p1,q0,q1=0,1,1,0;steps=0
  while True:
   c=int(mp.floor(x));pn=c*p1+p0;qn=c*q1+q0;steps+=1
   if qn.bit_length()>=bits+48 and gcd(8*pn,qn)==1:
    nearest=int(mp.nint(-gamma*qn/2));k=(nearest*pow(8*pn,-1,qn))%qn
    if k>0:return k,{'method':'CF inhomogeneous proposal; untrusted floating point','steps':steps,'denominator_bits':qn.bit_length(),'numerator_hex':hex(pn),'denominator_hex':hex(qn),'nearest_integer_hex':('-0x'+hex(-nearest)[2:] if nearest<0 else hex(nearest))}
   p0,p1=p1,pn;q0,q1=q1,qn;x=1/(x-c)

def propose_target(bits, controls, target_turn_fn):
    """Untrusted CF proposal for target angle/(2*pi) at caller precision.

    target_turn_fn is invoked inside mp.workprec and must return an mpmath
    expression.  It may approximate any desired signed angle.  The result is
    only a proposal: certify_target MUST separately verify caller-certified
    target intervals, using exact integer powering and no numerical trust.
    """
    assert bits>0 and controls>=1 and callable(target_turn_fn)
    with mp.workprec(3*bits+512):
        p=(mp.sqrt(5)-1)/2;gamma=mp.acos(mp.sqrt(p))/(2*mp.pi);turn=target_turn_fn();x=gamma
        p0,p1,q0,q1=0,1,1,0;steps=0
        while True:
            ai=int(mp.floor(x));pn=ai*p1+p0;qn=ai*q1+q0;steps+=1
            if qn.bit_length()>=bits+48 and gcd((1<<controls)*pn,qn)==1:
                nearest=int(mp.nint(turn*qn));inverse=pow((1<<controls)*pn,-1,qn);k=(nearest*inverse)%qn
                # Target 0 (or another grid hit) otherwise proposes k=0
                # forever; the adjacent grid point is still O(1/q) away.
                if k==0:nearest+=1;k=(nearest*inverse)%qn
                if k>0:return k,{'steps':steps,'denominator_bits':qn.bit_length(),'proposal_only':True}
            p0,p1=p1,pn;q0,q1=q1,qn;x=1/(x-ai)


def target_intervals(precision):
 # Outward dyadic enclosures of p,a=sqrt(p), cos(theta/2), -sin(theta/2).
 S=1<<precision;s5=isqrt(5*S*S);pL=(s5-S)//2;pU=(s5+1-S+1)//2
 aL=isqrt(pL*S);aU=isqrt(pU*S)+1
 cL=isqrt(((S+aL)*S)//2);cU=isqrt(((S+aU)*S)//2)+1
 nL= -isqrt(((S-aL)*S)//2)-1;nU= -isqrt(((S-aU)*S)//2)
 assert 0<pL<=pU<S and 0<aL<=aU<S and 0<cL<=cU<S and -S<nL<=nU<0
 return (cL,cU),(nL,nU)

def certify(k,bits=4096,precision=16640):
 S,cc,ss=phase._rotation_intervals(8*k,precision);assert S==1<<precision
 tc,ts=target_intervals(precision)
 err=max(abs(cc[0]-tc[1]),abs(cc[1]-tc[0]))+max(abs(ss[0]-ts[1]),abs(ss[1]-ts[0]))
 assert (err<<bits)<=S, 'candidate not certified, increase precision or seek candidate'
 return {'method':'owned outward dyadic integer powering plus integer square-root targets; no float in proof','precision_bits':precision,'target_error_bound_bits':bits,'L1_error_upper_numerator_hex':hex(err),'denominator':'2^'+str(precision),
         'actual_cos_endpoints_hex':[hex(x) for x in cc],'actual_sin_endpoints_hex':[hex(x) for x in ss],
         'target_cos_endpoints_hex':[hex(x) for x in tc],'target_sin_endpoints_hex':[hex(x) for x in ts]}

def pair_word(k, a_label, b_label, grade=(0,1,2,3), port=4, spin=(5,6), extra_controls=(), extra_pattern=(), protected=()):
    """Emit pair rotation, optionally coherently enabled by extra input bits.

    The caller must certify its own target cosine/sine and actual 2^K*k*theta,
    K=3+len(extra_controls); no arbitrary-angle gate is assumed.  Return the
    native DAG and structural metadata, including the sign on |a> -> |b>.
    Extra controls are read-only; all registers and port/spin must be disjoint.
    The caller must explicitly list RIGHT/oldRIGHT and any other factors that
    must remain identity in protected; none may be used even as a control.
    """
    assert k>0 and 0<=a_label<16 and 0<=b_label<16 and a_label!=b_label
    grade=tuple(grade);spin=tuple(spin);extra_controls=tuple(extra_controls);extra_pattern=tuple(extra_pattern)
    assert len(grade)==4 and len(spin)==2 and len(extra_controls)==len(extra_pattern)
    assert all(v in (0,1) for v in extra_pattern)
    assert len(set([*grade,*extra_controls,port,*spin]))==len(grade)+len(extra_controls)+3
    assert not set(protected).intersection([*grade,*extra_controls,port,*spin])
    delta=a_label^b_label;pivot=next(i for i in range(4) if (delta>>i)&1)
    flips=[i for i in range(4) if i!=pivot and (delta>>i)&1]
    def transform(x):
        for i in flips:x^=((x>>pivot)&1)<<i
        return x
    aa=transform(a_label);bb=transform(b_label);assert aa^bb==1<<pivot
    other=[i for i in range(4) if i!=pivot];pattern=[(aa>>i)&1 for i in other]+list(extra_pattern)
    C=[nb.gate('CX',grade[pivot],grade[i]) for i in flips]
    controls=[grade[i] for i in other]+list(extra_controls)
    body=nb.selective_rotation(controls,pattern,grade[pivot],k,port,spin)
    return nb.seq(*C,body,*reversed(C)),{'a':a_label,'b':b_label,'pivot':pivot,'C_target_bits':flips,'predicate_pattern':pattern,
       'predicate_control_count':len(controls),'source_a_pivot_bit':(aa>>pivot)&1,
       'angle':'2^K * k * theta','coefficient_on_b_for_input_a':'(-1)^source_a_pivot_bit * sin(angle)',
       'extra_controls_unchanged':True,'off_predicate_exact_identity':True}


def certify_target(k,controls,target_cos,target_sin,bits,precision):
    """Certify a caller-supplied target via outward dyadic interval endpoints.

    target_cos and target_sin are (low,high) integer bounds with common
    denominator 2^precision.  Their own certification is the caller's explicit
    obligation; this function uses integer arithmetic only and raises if the
    requested inequality cannot be proved.
    """
    assert k>0 and controls>=1 and precision>=16 and bits>0
    S,c,s=phase._rotation_intervals((1<<controls)*k,precision)
    for target in (target_cos,target_sin):assert -S<=target[0]<=target[1]<=S
    err=max(abs(c[0]-target_cos[1]),abs(c[1]-target_cos[0]))+max(abs(s[0]-target_sin[1]),abs(s[1]-target_sin[0]))
    assert (err<<bits)<=S
    return {'precision_bits':precision,'target_error_bits':bits,'controls':controls,'actual_angle_multiplier_hex':hex((1<<controls)*k),
            'cos_interval_hex':[hex(v) for v in c],'sin_interval_hex':[hex(v) for v in s],
            'target_cos_interval_hex':[hex(v) for v in target_cos],'target_sin_interval_hex':[hex(v) for v in target_sin],
            'L1_error_numerator_hex':hex(err),'target_interval_certification':'required from caller; not checked by this function'}


def word(k,grade=(0,1,2,3),port=4,spin=(5,6)):
    # C maps grade 1 to15, grade14 to14; target G^(8k).
    return pair_word(k,1,14,grade,port,spin)[0]


def resources(tree,port):
 from collections import Counter
 op=tree['op']
 if op=='seq':
  c=Counter()
  for child in tree['children']:c.update(resources(child,port))
  return c
 if op=='repeat':return Counter({x:int(tree['count'])*v for x,v in resources(tree['child'],port).items()})
 if op=='G':return Counter({'G_port' if tree['wires'][0]==port else 'G_other':1})
 return Counter({op:1})

def main():
 k,proposal=candidate(4096);cert=certify(k);port=4;spin=(5,6);old=7;tree=word(k,port=port,spin=spin);nb.validate_schema(tree,8,port,spin,(old,));rev=nb.inverse_literal(tree,port,spin);nb.validate_schema(rev,8,port,spin,(old,));f=resources(tree,port);r=resources(rev,port)
 assert f['G_port']==4*k and f['G_other']==4*k and f['CX']==54 and f['SourceI']==16
 assert r['G_port']==8*k and r['G_other']==0 and r['CX']==24*k+54 and r['SourceI']==32*k+48
 out={'status':'CERTIFIED_ACTUAL_CAR_USTAR_NATIVE_DAG','k':str(k),'k_binary_length':k.bit_length(),'proposal':proposal,'certificate':cert,'layout':{'grade_little_endian':[0,1,2,3],'port':port,'spin':list(spin),'oldRIGHT':[old]},
      'forward_DAG':tree,'literal_raw_inverse_DAG':rev,'forward_counts':{x:str(f[x]) for x in ('G_port','G_other','CX','SourceI')},'literal_inverse_counts':{x:str(r[x]) for x in ('G_port','G_other','CX','SourceI')},
      'target':'C† exp[-J theta/2 * P(grade1,2,3=111)] C; maps grade1 to u_star, full SO(16)',
      'off_predicate_exact_identity':True,'operator_error_lt_or_equal':'2^-4096','no_private_clean_wires':True,'preserves_SAM_SITE_RIGHT_oldRIGHT_exactly':True,'arbitrary_port_spin_allowed':True,
      'optimized_negative_powers':'Z G^k Z routed once, not literal repeated G^-1; marked stages distinct and fully counted','native_boolean_sha256':sha256((D/'round14/native_boolean.py').read_bytes()).hexdigest(),'native_phase_sha256':sha256((S/'d0_native_readiness_amplification_2026-10-24/native_phase.py').read_bytes()).hexdigest(),
      'full_native_gigantic_word_executed':False,'CAR_bank_and_global_admission_proved':False,'physical_C_closed':False,'GR_closed':False}
 (P/'CAR_USTAR_NATIVE.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'k_binary_length':k.bit_length(),'bits':4096,'interval_precision':cert['precision_bits'],'forward_counts_symbolic':'G_port=4k,G_other=4k,CX=54,SourceI=16','literal_inverse_counts_symbolic':'G_port=8k,CX=24k+54,SourceI=32k+48'}),flush=True)
if __name__=='__main__':main()
