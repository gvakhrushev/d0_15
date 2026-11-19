"""One 8-control Gray catalogue, fixed coframe and 8 current settings.

Run lengths are recorded, NOT replayed. Numerical Julia columns are checked
using the signed idealized rotation; factory/clock/source are not simulated.
"""
import json, math, runpy
from pathlib import Path
import mpmath as mp
import numpy as np

P = Path(__file__).parent
base = runpy.run_path(str(P / 'check_site_coframe_julia.py'))
mp.mp.dps = 100
theta=base['theta']; p=base['p']; iv=mp.iv
goal=mp.mpf('1e-9'); step=goal/256

def coefficients(angles, zero):
    return [sum(((-1 if bin(g&s).count("1")%2 else 1)*angles[s]
                 for s in range(128)),zero)/256 for g in range(128)]

def make_word(qs):
    x=theta/(2*mp.pi); n0,n1,d0,d1=0,1,1,0
    while True:
        z=int(mp.floor(x)); n=z*n1+n0; d=z*d1+d0
        if d>=int(mp.ceil(3*mp.pi/step)):break
        n0,n1,d0,d1=n1,n,d1,d; x=1/(x-z)
    word=[]
    for q in qs:
        if abs(q)<step/2:
            word.append((0,0));continue
        t=int(mp.nint(q*d/(2*mp.pi))); k=(t*pow(n,-1,d))%d
        candidates=[]
        for c in (k,k-d):
            m=int(mp.nint((c*theta-q)/(2*mp.pi)))
            error=c*theta-2*mp.pi*m-q
            if abs(error)<step:candidates.append((abs(c),c,m))
        assert candidates
        _,c,m=min(candidates);word.append((c,m))
    return word

def main():
    _, current=base['target_angles']()
    th, tables=base['interval_tables']()
    angles=[]; bounds=[]
    for j in range(1,9):
        for s in range(16):
            a=mp.sin(current[s])*mp.sqrt(mp.mpf(j)/8)
            ai=iv.sin(tables[1][s])*iv.sqrt(iv.mpf(j)/8)
            angles.append(mp.asin(a))
            bounds.append(iv.atan2(ai,iv.sqrt(1-ai*ai)))
    qs=coefficients(angles,mp.mpf(0)); qi=coefficients(bounds,iv.mpf(0))
    word=make_word(qs)
    errors=[]; maxima=[]
    for (k,m),q,qiv in zip(word,qs,qi):
        e=k*th-2*iv.pi*m-qiv
        bound=math.nextafter(max(abs(float(e.a)),abs(float(e.b))),math.inf)
        assert bound < float(step)
        maxima.append(bound);errors.append(k*theta-2*mp.pi*m-q)
    total=math.nextafter(2*math.fsum(maxima),math.inf)
    assert total<float(goal)
    gray=[i^(i>>1) for i in range(256)]
    assert all(bin(gray[i]^gray[(i+1)%256]).count("1")==1 for i in range(256))
    # Exact arithmetic for every 8-bit configuration. High bit is B;
    # other seven are site[0..3], j-1[0..2].
    for control in range(256):
        got=sum((word[g&127][0]*(-1 if g&128 else 1)) *
                (-1 if bin(control&g).count("1")%2 else 1) for g in gray)
        want=(2*sum(k*(-1 if bin((control&127)&i).count("1")%2 else 1)
                    for i,(k,m) in enumerate(word)) if control&128 else 0)
        assert got==want
    maxmatrix=0.; orth=0.
    for site in range(128):
        diff=2*sum((-1 if bin(site&g).count("1")%2 else 1)*errors[g]
                   for g in range(128))
        assert abs(diff)<total
        for r in range(4):
            A=base['julia_target'](r,math.sin(float(angles[site])))
            B=base['native_julia'](r,float(angles[site]+diff))
            maxmatrix=max(maxmatrix,float(np.linalg.norm(B-A,2)))
            orth=max(orth,float(np.linalg.norm(base['mm'](B.T,B)-np.eye(32),2)))
    assert maxmatrix<total+1e-13 and orth<1e-13
    assert all(float(iv.sin(a).a)>0.044 for a in bounds)
    t=total/0.044; rel=(2*t+t*t)/(1-t)**2
    G=2*sum(abs(k) for k,m in word)
    # 4 current directions. 4 reference directions are prior catalogue.
    # Ref count taken from the underlying prior reproducible JSON output.
    prior=json.loads((P/'site_coframe_julia_result.json').read_text())
    Gref=prior['reference_G_calls_per_direction']
    gtotal=4*(G+Gref)
    cx=gtotal+4*(256+3)+4*(32+3)
    # Separate classically scheduled runs, for resource comparison only.
    # They do not implement a coherent j-controlled programme.
    num,den=base['convergent']()
    separate=[]
    for j in range(8):
        wj,_,_=base['compile_one'](angles[16*j:16*(j+1)],
                                  bounds[16*j:16*(j+1)],th,num,den)
        separate.append(2*sum(abs(k) for k,m in wj))
    b2=1-(1-4*p**3)**32
    ready=(1-p**40)*b2**36
    out={'schema':'d0.site-eight-catalogue/1','status':'PASS',
      'fixed_L':16,'rho':1,'nu':1,'base_e':'8 I','current_settings':8,
      'julia_directions':4,'current_site_j_configurations':128,
      'julia_columns_each':32,'native_angles':'signed 8-control Gray catalogue',
      'angle_error_upper':total,'relative_w_error_upper':rel,
      'observed_full_matrix_norm_error':maxmatrix,'observed_orthogonality_error':orth,
      'signed_G_exponents':[k for k,m in word], 'G_wraps':[m for k,m in word],
      'G_calls_current_per_direction':G,'G_calls_reference_per_direction':Gref,
      'G_calls_independent_classical_settings_per_direction':separate,
      'G_calls_sum_8_independent_settings_per_direction':sum(separate),
      'G_calls_four_current_and_four_reference':gtotal,
      'CX_including_inverse_and_gray_and_outer':cx,
      'Toffoli_in_catalogue':0,'CZ_factory_calls_for_JW_and_signature':36,
      'conditional_one_and_36_CZ_readiness':str(ready),
      'not_in_inventory':'CZ factory internals, preparation, site/j routing, clock, multiplexer, source, old bank',
      'run_length_words_replayed':False,'native_factory_simulated':False,
      'program_address_multiplexer_compiled':False,'general_fields_compiled':False,
      'physical_lift_or_norms_measured':False,'Book_cost_info_derived':False,'GR_closed':False}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
