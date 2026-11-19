"""Finite SITE-controlled Julia32 words for the fixed L=16 coframe fixture.

Every one of 32 Julia columns is checked. Gray G powers are finite run-length
words, not replayed. rho=nu=1, current e=8I, j=8; arbitrary-field loading,
the Choi programme address multiplexer and complete Book price remain open.
"""
import itertools,json,math,runpy
from pathlib import Path
import numpy as np
import mpmath as mp

mp.mp.dps=110
HERE=Path(__file__).parent
carry=runpy.run_path(str(HERE/'check_carry_compensated_geometry.py'))
p=carry['p'];theta=carry['theta'];rf=carry['rf'];Fh=carry['Fh']
eps=carry['eps'];d0=carry['d0'];report=carry['report'];b=carry['b_for_n']
ref=report(0,d0)-report(0,-d0)
goal=mp.mpf('1e-9');step=goal/64


def target_angles():
    f=[];w=[]
    for site in range(16):
        n0=site&3;n1=(site>>2)&3
        dy=report(0,d0*b(n1))-report(0,-d0*b(n0))
        ww=dy/ref;sf2=2*eps*rf*Fh/dy
        f.append(mp.asin(1/mp.sqrt(sf2)))
        w.append(mp.asin(1/(8*mp.sqrt(ww))))
    return f,w


def qtable(angles):
    return [sum((-1 if bin(g&s).count('1')%2 else 1)*angles[s]
                for s in range(16))/32 for g in range(16)]


def convergent():
    qmin=int(mp.ceil(3*mp.pi/step));x=theta/(2*mp.pi)
    n0,n1,d0,d1=0,1,1,0
    while True:
        a=int(mp.floor(x));n=a*n1+n0;d=a*d1+d0
        if d>=qmin:return n,d
        n0,n1,d0,d1=n1,n,d1,d;x=1/(x-a)


def words(qs,num,den):
    out=[]
    for q in qs:
        if abs(q)<step/2:
            out.append((0,0));continue
        t=int(mp.nint(q*den/(2*mp.pi)))
        k=(t*pow(num,-1,den))%den
        options=[]
        for c in (k,k-den):
            wraps=int(mp.nint((c*theta-q)/(2*mp.pi)))
            err=c*theta-q-2*mp.pi*wraps
            if abs(err)<step:options.append((abs(c),c,wraps))
        assert options
        _,k,wraps=min(options);out.append((k,wraps))
    return out


def interval_tables():
    iv=mp.iv;iv.dps=80;one=iv.mpf(1);pi=iv.pi;pp=(iv.sqrt(5)-one)/2
    th=iv.atan2(pp,iv.sqrt(pp));zz=one/2**20;hh=one/16;ep=one/4096
    ff=iv.mpf(carry['Fexact'].numerator)/carry['Fexact'].denominator
    L0=4*pp**3
    r_f=4*pp**2*(one-2*pp**2)*zz*(one-zz*L0)*(one-L0)
    aa=pp*iv.sin(712*th)
    dd=ep*4*aa**2*iv.sin(pi/16)**2/(hh**2*64)
    d0i=16*12624688*th-pi/8-2*pi*21418601
    d1i=16*(-4421679)*th-pi/4-2*pi*(-7501665)
    def bb(n):
        kind=n&3
        eta=d0i if kind in (0,2) else d1i-d0i if kind==1 else -d0i-d1i
        return iv.sin(pi/16+eta/2)**2/iv.sin(pi/16)**2
    def r(y):
        u=pp+pp**2*y;B=4*u*u*(one-u*u);A=L0+(one-L0)*B
        return zz*(A+B)-zz**2*A*B
    base=r(dd)-r(-dd);tables=[[],[]]
    for site in range(16):
        dy=r(dd*bb((site>>2)&3))-r(-dd*bb(site&3))
        w=dy/base;sf2=2*ep*r_f*ff/dy
        af=one/iv.sqrt(sf2);aw=one/(8*iv.sqrt(w))
        tables[0].append(iv.atan2(af,iv.sqrt(one-af**2)))
        tables[1].append(iv.atan2(aw,iv.sqrt(one-aw**2)))
    return th,tables


def compile_one(angles,intervals,th,num,den):
    qs=qtable(angles);word=words(qs,num,den)
    qi=[sum(((-1 if bin(g&s).count('1')%2 else 1)*intervals[s]
             for s in range(16)),mp.iv.mpf(0))/32 for g in range(16)]
    upper=[];errors=[]
    for (k,turn),qq in zip(word,qi):
        err=k*th-2*mp.iv.pi*turn-qq
        bound=math.nextafter(max(abs(float(err.a)),abs(float(err.b))),math.inf)
        assert bound<float(step)
        upper.append(bound)
        errors.append(k*theta-2*mp.pi*turn-qs[len(errors)])
    overall=math.nextafter(2*math.fsum(upper),math.inf)
    assert overall<float(goal)
    actual=[]
    for s in range(16):
        diff=2*sum((-1 if bin(g&s).count('1')%2 else 1)*errors[g]
                   for g in range(16))
        actual.append(angles[s]+diff)
        assert abs(diff)<overall
    return word,actual,overall


def verify_gray_word(word):
    # Controls 0..3 are SITE and control 4 is the Julia block B. The
    # coefficient of g_B=1 is exactly the negative integer of g_B=0.
    gray=[j^(j>>1) for j in range(32)]
    for b in range(32):
        total=0
        for g in gray:
            k=word[g&15][0]*(-1 if g&16 else 1)
            total+=k*(-1 if bin(b&g).count('1')%2 else 1)
        expected=(2*sum(k*(-1 if bin((b&15)&s).count('1')%2 else 1)
                          for s,(k,turn) in enumerate(word)) if b&16 else 0)
        assert total==expected


def mm(A,B):return np.einsum('ij,jk->ik',A,B,optimize=False)


def julia_target(r,mag):
    C=np.zeros((16,16));eta=1 if r==0 else -1
    for n in range(16):
        if not ((n>>r)&1):
            sign=-1 if bin(n&((1<<r)-1)).count('1')%2 else 1
            C[n|(1<<r),n]=eta*mag*sign
    lower=np.eye(16);upper=np.eye(16)
    for n in range(16):
        if (n>>r)&1:upper[n,n]=math.sqrt(1-mag*mag)
        else:lower[n,n]=math.sqrt(1-mag*mag)
    return np.block([[C,upper],[lower,-C.T]])


def native_julia(r,gamma):
    XB=np.zeros((32,32));CNOT=np.zeros((32,32));R=np.eye(32)
    for c in range(32):
        XB[c^16,c]=1
        CNOT[c^(16 if (c>>r)&1 else 0),c]=1
    for n in range(16):
        if not ((n>>r)&1):
            sign=(-1 if bin(n&((1<<r)-1)).count('1')%2 else 1)
            sign*=1 if r==0 else -1
            c=math.cos(gamma);s=sign*math.sin(gamma)
            i=16+n;j=i+(1<<r)
            R[i,i]=c;R[j,j]=c;R[j,i]=s;R[i,j]=-s
    return mm(mm(mm(CNOT,R),CNOT),XB)


def main():
    ref_angles,current_angles=target_angles()
    th,tables=interval_tables();num,den=convergent()
    wf,af,ef=compile_one(ref_angles,tables[0],th,num,den)
    ww,aw,ew=compile_one(current_angles,tables[1],th,num,den)
    verify_gray_word(wf);verify_gray_word(ww)
    maxerr=[0.,0.];orth=0.
    for kind,(targets,actual,bound) in enumerate(((ref_angles,af,ef),(current_angles,aw,ew))):
     for site in range(16):
      for r in range(4):
       ideal=julia_target(r,math.sin(float(targets[site])))
       native=native_julia(r,float(actual[site]))
       err=float(np.linalg.norm(native-ideal,2));maxerr[kind]=max(maxerr[kind],err)
       orth=max(orth,float(np.linalg.norm(mm(native.T,native)-np.eye(32),2)))
       assert err<bound+1e-13 and orth<1e-13
    # Simple certified lower bounds, not rounded numerical minima.
    assert all(float(mp.iv.sin(x).a)>0.13 for x in tables[0])
    assert all(float(mp.iv.sin(x).a)>0.12 for x in tables[1])
    minf=.13;minw=.12
    xf=ef/minf;xw=ew/minw
    relf=(2*xf+xf*xf)/(1-xf)**2
    relw=(2*xw+xw*xw)/(1-xw)**2
    e=max(relf,relw)
    coeff_f=e/(1-e)
    coeff_q=float(carry['k0'])*(2*e+e*e)/(1-e)**2
    # Full 5-bit Gray cycle, every control projector and signed exponent.
    gray=[j^(j>>1) for j in range(32)]
    assert all((gray[j]^gray[(j+1)%32]) and
               ((gray[j]^gray[(j+1)%32])&((gray[j]^gray[(j+1)%32])-1))==0
               for j in range(32))
    b2=1-(1-4*p**3)**32
    readiness=(1-p**40)*b2**36
    output={'schema':'d0.site-coframe-julia/1','status':'PASS',
      'fixed_rho_nu':1,'fixed_current_coframe':'8 I','current_setting_j':8,
      'site_bits_used':4,'site_patterns_checked':16,'directions_checked':4,
      'julia_columns_each':32,'oldRIGHT_is_identity_factor':True,
      'ref_error_bound':ef,'current_error_bound':ew,
      'all_column_observed_error_ref':maxerr[0],
      'all_column_observed_error_current':maxerr[1],
      'orthogonality_error':orth,'relative_sF_squared_bound':relf,
      'relative_w_bound':relw,'lift_Jf_coefficient':coeff_f,
      'lift_Jq_coefficient':coeff_q,
      'reference_signed_G_exponents':[k for k,t in wf],
      'reference_wraps':[t for k,t in wf],
      'current_signed_G_exponents':[k for k,t in ww],
      'current_wraps':[t for k,t in ww],
      'reference_G_calls_per_direction':2*sum(abs(k) for k,t in wf),
      'current_G_calls_per_direction':2*sum(abs(k) for k,t in ww),
      'signed_run_lengths_not_replayed':True,
      'known_one_and_36_CZ_success_conditional':str(readiness),
      'program_address_multiplexer_compiled':False,
      'other_seven_settings_compiled':False,'general_field_variations_compiled':False,
      'full_Choi_bank_built':False,'full_clock_built':False,
      'physical_lift_or_norms_measured':False,'Book_cost_info_derived':False,
      'GR_closed':False}
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
