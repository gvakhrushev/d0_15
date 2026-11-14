#!/usr/bin/env python3
"""Actual native powers for the source-specific coframe factorization.

The candidate grid is untrusted. Outward dyadic target intervals and complex
Euclidean-ball integer powering certify every retained native rotation.
"""
from pathlib import Path
import hashlib,json,sys
import mpmath as mp
import coframe_targets as t
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def candidate_grid(bits,controls):
    p=(mp.sqrt(5)-1)/2;x=(2**controls)*mp.acos(mp.sqrt(p))/(2*mp.pi)
    p0,p1=0,1;q0,q1=1,0;steps=0
    while True:
        a=int(mp.floor(x));pn=a*p1+p0;qn=a*q1+q0;steps+=1
        if qn.bit_length()>=bits+20:return pn,qn,steps
        p0,p1=p1,pn;q0,q1=q1,qn;x=1/(x-a)
def native_power(exponent,iv,constants):
    S=iv.scale
    def mul(x,y):
        c,s,r=x;C,T,R=y
        return ((c*C-s*T)//S,(c*T+s*C)//S,r+R-((-r*R)//S)+2)
    a,p=constants['sqrtp'],constants['p'];base=(a[0],p[0],a[1]-a[0]+p[1]-p[0]);acc=(S,0,0)
    while exponent:
        if exponent&1:acc=mul(acc,base)
        exponent>>=1
        if exponent:base=mul(base,base)
    cc,ss,rr=acc;return (cc-rr,cc+rr),(ss-rr,ss+rr)
def main(bits=3264,precision=7168):
    assert precision>=2*bits+512
    iv=t.Dyadic(precision);c=t.constants(iv);specs,banks=t.catalogue();S=iv.scale
    families={};angles={};unique={};controls=20
    def enc(v):return [hex(x) for x in v]
    with mp.workprec(3*bits+256):
        pn,qn,steps=candidate_grid(bits+4,controls);inverse=pow(pn,-1,qn)
        def certify(cc,ss,multiplier=1<<controls):
            key=(multiplier,*cc,*ss)
            if key in unique:return unique[key]
            cm=mp.mpf(cc[0]+cc[1])/(2*S);sm=mp.mpf(ss[0]+ss[1])/(2*S)
            turn=(mp.atan2(sm,cm)/(2*mp.pi))%1
            target=int(mp.nint(qn*turn))%qn;k=(target*inverse)%qn;assert k>0
            nc,ns=native_power(multiplier*k,iv,c)
            err=max(abs(nc[0]-cc[1]),abs(nc[1]-cc[0]))+max(abs(ns[0]-ss[1]),abs(ns[1]-ss[0]))
            assert err<=1<<(precision-bits),('uncertified coframe angle',len(angles))
            name='coframe_angle_'+str(len(angles));unique[key]=name
            angles[name]={'k':str(k),'k_binary_length':k.bit_length(),'native_exponent_multiplier':multiplier,
                          'target_cos_hex':enc(cc),'target_sin_hex':enc(ss),'native_cos_hex':enc(nc),'native_sin_hex':enc(ns),
                          'denominator_power_of_two':precision,'operator_error_L1_numerator_hex':hex(err),'certified_error_bits':bits}
            if len(angles)%16==0:print('certified concrete coframe powers',len(angles),flush=True)
            return name
        for name,spec in specs.items():
            v=t.vector(iv,c,spec);f=t.factors(iv,v,spec)
            refs=[]
            for key,cc,ss in t.native_angle_targets(iv,f):refs.append({'factor':list(key),'angle_id':certify(cc,ss)})
            families[name]={'spec':spec,'vector_bounds_hex':[enc(x) for x in v],'norm_hex':enc(f['norm']),
                            'norm_squared_hex':enc(f['norm_squared']),'chosen_elimination_order':f['chosen_elimination_order'],
                            'mode_rotations':[{'mode':r['mode'],'cos_hex':enc(r['cos']),'sin_hex':enc(r['sin']),
                                               'radius_hex':enc(r['radius']),'exact_identity':r['exact_identity']} for r in f['mode_rotations']],
                            'angle_bindings':refs}
        # X_t will use a common pi/2 rotation and a phase with doubled actual
        # exponent. They are certified separately; existing k is not divided.
        xid=certify(iv.rational(0),iv.rational(1));x=angles[xid];k=int(x['k'])
        pc,ps=native_power((2**21)*k,iv,c);tc,ts=iv.rational(-1),iv.rational(0)
        pe=max(abs(pc[0]-tc[1]),abs(pc[1]-tc[0]))+max(abs(ps[0]-ts[1]),abs(ps[1]-ts[0]))
        combined=pe+int(x['operator_error_L1_numerator_hex'],16)
        assert combined<=1<<(precision-bits)
        xphase={'rotation_angle_id':xid,'phase_native_exponent_multiplier':2**21,'phase_cos_hex':enc(pc),'phase_sin_hex':enc(ps),
                'phase_target_cos_hex':enc(tc),'phase_target_sin_hex':enc(ts),'X_error_L1_numerator_hex':hex(combined),'certified_X_error_bits':bits}
    inputs=[P/'coframe_targets.py',t.D/'round18/material_targets.py',t.D/'round19/coframe_factorization.py',t.D/'round19/julia_locality.py',t.loc.COORD_PATH,t.loc.ADDR_PATH,t.PF_PATH,t.loc.B/'round25/precision_name.py',t.loc.B/'round25/targets.py',t.loc.B/'round21/REFERENCE_METADATA.json']
    out={'status':'CERTIFIED_SOURCE_SPECIFIC_COFRAME_NATIVE_ROTATION_POWERS','precision_bits':precision,'per_macro_error_le':'2^-'+str(bits),
         'source_sha256':h(Path(__file__)),'input_sha256':{str(p):h(p) for p in inputs},'families':families,'angles':angles,'controlled_X_power':xphase,
         'catalogue':banks,'candidate_grid_not_proof':{'numerator':str(pn),'denominator':str(qn),'steps':steps,'controls':controls},
         'all_family_denominators_interval_ge_half_norm':True,'all_family_norms_strictly_between_zero_and_one':True,
         'full_controlled_native_word_emitted':False,'proper_link_SELECT_compiled':False,'full_Omega_loader_compiled':False,
         'physical_C_closed':False,'GR_closed':False}
    (P/'COFRAME_ANGLE_LIBRARY.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
    print(json.dumps({'status':out['status'],'families':len(families),'angles':len(angles),'coframe_sectors':sum(map(len,banks.values())),'error_le':out['per_macro_error_le']}))
if __name__=='__main__':main()
