#!/usr/bin/env python3
"""Native full128 normalization -> input change -> complementary source.

Research calculation, not physical admission, a new Info law, or GR closure.
Uses the original L4 Fourier character, 16 CAR grades, 64 SELECT rows, 128
outcomes, true left/right Julia defects and a proper-link boost.  Complete
histories are contracted by CP maps, not sampled or postselected away.
"""
from __future__ import annotations
import json
import math
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from scipy.linalg import expm, solve_sylvester

P=(math.sqrt(5)-1)/2
ELL=-math.log(P)
Z=2.0**-20
REF=128
ORDER=(0,2,3,1)
INPUT_REF='5edac80c86c17014fc83e0aa608e192f43c1fdba'
GROUPS={}

def adj(a): return a.conj().T

def herm(a): return (a+adj(a))/2

def require(c,msg):
    if not bool(c): raise ArithmeticError(msg)

def err(a,b): return float(np.linalg.norm(np.asarray(a)-np.asarray(b)))

def near(a,b,msg,tol=3e-11):
    e=err(a,b)
    require(e<tol*(1+float(np.linalg.norm(b))),f'{msg}: error {e}')
    return e

def sqrt_spd(a):
    w,u=np.linalg.eigh(herm(a)); require(w.min()>1e-10,'strict positive support')
    return (u*np.sqrt(w))@adj(u)

def logdet_spd(a):
    w=np.linalg.eigvalsh(herm(a)); require(w.min()>0,'positive determinant domain')
    return float(np.log(w).sum())

def creators():
    out=[]
    for role in range(4):
        c=np.zeros((16,16),complex)
        earlier=ORDER[:ORDER.index(role)]
        for mask in range(16):
            if not ((mask>>role)&1):
                c[mask+(1<<role),mask]=(-1)**sum((mask>>j)&1 for j in earlier)
        out.append(c)
    return out

@dataclass
class Round:
    k: np.ndarray
    dk: np.ndarray
    a: np.ndarray
    da: np.ndarray
    b: np.ndarray
    db: np.ndarray
    delta: np.ndarray
    ddelta: np.ndarray
    port: np.ndarray

    def cp(self,x,t=0.,derivative=False):
        w=np.exp(-t*self.port)
        if derivative:
            return sum((wi*(adj(d)@x@k+adj(k)@x@d)
                        for wi,k,d in zip(w,self.k,self.dk)),np.zeros_like(x,dtype=complex))
        return sum((wi*adj(k)@x@k for wi,k in zip(w,self.k)),np.zeros_like(x,dtype=complex))

    def cpt(self,x,t=0.):
        w=-self.port*np.exp(-t*self.port)
        return sum((wi*adj(k)@x@k for wi,k in zip(w,self.k)),np.zeros_like(x,dtype=complex))

    def future(self,n,t):
        h=[np.eye(16,dtype=complex)]; dh=[np.zeros((16,16),complex)]; ht=[dh[0].copy()]
        for j in range(n):
            dh.append(self.cp(dh[-1],t)+self.cp(h[-1],t,True))
            ht.append(self.cp(ht[-1],t)+self.cpt(h[-1],t))
            h.append(self.cp(h[-1],t))
        return h,dh,ht


def native(theta):
    c=creators(); eye=np.eye(16,dtype=complex); nu=3/5
    phases=(1j,1j,-1.,-1j)
    x=np.zeros((4,4)); x[0,1]=x[1,0]=1.
    gx=sum((x[i,j]*c[i]@adj(c[j]) for i in range(4) for j in range(4)),np.zeros_like(eye))
    u=expm(theta*gx); du=u@gx
    words=[]; dwords=[]
    for r in range(4):
        fixed=nu*c[r]
        tr=fixed@(u if r==1 else eye)*phases[r]
        dtr=fixed@du*phases[r] if r==1 else np.zeros_like(eye)
        l=sqrt_spd(eye-tr@adj(tr)); rr=sqrt_spd(eye-adj(tr)@tr)
        dl=solve_sylvester(l,l,-dtr@adj(tr)-tr@adj(dtr))
        dr=solve_sylvester(rr,rr,-adj(dtr)@tr-adj(tr)@dtr)
        l0=sqrt_spd(eye-fixed@adj(fixed)); r0=sqrt_spd(eye-adj(fixed)@fixed)
        zero=np.zeros_like(eye)
        for pair,dpair in [((tr,l),(dtr,dl)),((adj(tr),rr),(adj(dtr),dr)),
                           ((-fixed,-l0),(zero,zero)),((-adj(fixed),-r0),(zero,zero))]:
            words.extend((pair,pair)); dwords.extend((dpair,dpair))
    rows=[]; drows=[]
    for label in range(32):
        for coefficient in range(2):
            signs=[(-1)**(bin(label&j).count('1')%2) for j in range(32)]
            rows.append(sum((s*words[j][coefficient] for j,s in enumerate(signs)),np.zeros_like(eye))/32)
            drows.append(sum((s*dwords[j][coefficient] for j,s in enumerate(signs)),np.zeros_like(eye))/32)
    a=rows[0]; da=drows[0]; ks=[]; dks=[]
    for j,(n,dn) in enumerate(zip(rows,drows)):
        share=adj(n)@a; ds=adj(dn)@a+adj(n)@da
        ks.extend(((eye if j==0 else np.zeros_like(eye))-2*P**2*share,-2*P*np.sqrt(P)*share))
        dks.extend((-2*P**2*ds,-2*P*np.sqrt(P)*ds))
    ks=np.array(ks); dks=np.array(dks)
    # A=h D/16, h=1/4. Preserve that actual calibration in the Rayleigh term.
    d=64*a; dd=64*da
    return Round(ks,dks,a,da,ks[0],dks[0],d@d,dd@d+d@dd,np.tile([0.,1.],64))


def power_jet(a,da,n):
    v=np.eye(len(a),dtype=complex); dv=np.zeros_like(v)
    for _ in range(n): dv,v=dv@a+v@da,v@a
    return v,dv


def normalized_values(run,n,t,rho,drho=None):
    h,dh,ht=run.future(n,t); h=h[-1]; dh=dh[-1]
    hs=sqrt_spd(h); his=np.linalg.inv(hs)
    dhs=solve_sylvester(hs,hs,dh); dhis=-his@dhs@his
    d,dd=power_jet(run.b,run.db,n)
    k=adj(d)@d; dk=adj(dd)@d+adj(d)@dd
    v=d@his; dv=dd@his+d@dhis
    ret=adj(v)@v; dret=adj(dv)@v+adj(v)@dv
    f=np.eye(16)-ret; df=-dret
    m=(1-Z)*h+Z*k; dm=(1-Z)*dh+Z*dk
    jf=float(-REF*np.log1p(-Z*np.linalg.eigvalsh(herm(f))).sum())
    jr=REF*(logdet_spd(h)-logdet_spd(m))
    source_direct=REF*Z*np.trace(np.linalg.solve(np.eye(16)-Z*f,df)).real
    source_ratio=REF*(np.trace(np.linalg.solve(h,dh))-np.trace(np.linalg.solve(m,dm))).real
    zz=float(np.trace(rho@h).real)
    drho=np.zeros_like(rho) if drho is None else drho
    dzz=float(np.trace(drho@h+rho@dh).real)
    rho_t=hs@rho@hs/zz
    drho_t=(dhs@rho@hs+hs@drho@hs+hs@rho@dhs)/zz-rho_t*dzz/zz
    alpha=P**2/(128*16); beta=2*n*alpha
    logc=(n+1)*math.log(128)
    zheat=float(np.trace(ret).real)
    heat=(logc+math.log(zheat))/beta
    heat_source=float(np.trace(dret).real)/(beta*zheat)
    matter=float(np.trace(rho_t@run.delta).real)
    matter_source=float(np.trace(drho_t@run.delta+rho_t@run.ddelta).real)
    return dict(h=h,dh=dh,ht=ht[-1],k=k,dk=dk,v=v,dv=dv,
                J=jf,Jratio=jr,dJ=source_direct,dJratio=source_ratio,
                normalizer=math.exp(-n*t)*zz, dlognorm=dzz/zz,
                rhot=rho_t,drhot=drho_t,H=heat,dH=heat_source,
                R=matter,dR=matter_source,S=heat+jf+matter,
                dS=heat_source+source_direct+matter_source)


def run_all():
    theta=.08; n=3; t=ELL; run=native(theta); eye=np.eye(16,dtype=complex)
    effects=sum((adj(k)@k for k in run.k),np.zeros_like(eye))
    deffects=sum((adj(d)@k+adj(k)@d for k,d in zip(run.k,run.dk)),np.zeros_like(eye))
    e1=sum((adj(k)@k for k in run.k[1::2]),np.zeros_like(eye))
    G1={'rows':len(run.k),'CAR_dimension':16,'completeness_error':near(effects,eye,'completeness'),
        'completeness_jet_error':near(deffects,0*eye,'completeness jet'),
        'port_effect_error':near(e1,4*P**3*run.a@run.a,'original port effect')}
    step=2e-5; rp=native(theta+step); rm=native(theta-step)
    G1['kraus_derivative_error']=near((rp.k-rm.k)/(2*step),run.dk,'literal full Kraus jet',tol=2e-9)
    GROUPS['literal_native_interface']=G1
    h,dh,ht=run.future(n,t)
    h1closed=eye-(1-math.exp(-t))*e1
    near(h[1],h1closed,'absolute one-round operator')
    near(run.future(n,0)[0][-1],eye,'absolute unmarked n-round norm')
    near(run.future(n,0)[1][-1],0*eye,'unmarked full field norm derivative')
    near((rp.future(n,t)[0][-1]-rm.future(n,t)[0][-1])/(2*step),dh[-1],'normalizer field jet',tol=2e-9)
    htfd=(run.future(n,t+step)[0][-1]-run.future(n,t-step)[0][-1])/(2*step)
    near(htfd,ht[-1],'normalizer cost-marker jet',tol=2e-9)
    eigen=np.linalg.eigvalsh(h[-1]); spread=float(np.ptp(eigen))
    require(spread>1e-5,'native normalizer must not be replaced by a scalar')
    comm=float(np.linalg.norm(h[-1]@run.b-run.b@h[-1]))
    jetcomm=float(np.linalg.norm(h[-1]@dh[-1]-dh[-1]@h[-1]))
    require(jetcomm>1e-8,'retain noncommuting actual normalizer derivative')
    GROUPS['absolute_operator_normalizer']={'n':n,'t':t,'spectrum_min':float(eigen.min()),
             'spectrum_max':float(eigen.max()),'spread':spread,'commutator_with_blank':comm,
             'commutator_with_field_jet':jetcomm,
             'operator_field_jet_norm':float(np.linalg.norm(dh[-1]))}
    # The finite Doob normalization is an isometry, but changes input preparation.
    normalized=[]; max_complete=0.
    for j in range(n):
        left=sqrt_spd(h[n-j-1]); right=np.linalg.inv(sqrt_spd(h[n-j]))
        kj=np.array([math.exp(-t*b/2)*left@k@right for k,b in zip(run.k,run.port)])
        sj=sum((adj(k)@k for k in kj),np.zeros_like(eye))
        max_complete=max(max_complete,near(sj,eye,'finite Doob step completeness'))
        normalized.append(kj)
    psi=np.arange(1,17,dtype=complex)+.2j*np.arange(16,0,-1); psi/=np.linalg.norm(psi)
    hs=sqrt_spd(h[-1]); norm=float(np.vdot(psi,h[-1]@psi).real)
    psi_t=hs@psi/math.sqrt(norm)
    rng=np.random.default_rng(20261021)
    histories=[(0,)*n,(1,)*n,(0,1,0)]+[tuple(map(int,rng.integers(0,128,n))) for _ in range(9)]
    max_tel=max_state=0.
    for path in histories:
        old=np.eye(16,dtype=complex); new=old.copy(); nb=0.
        for j,index in enumerate(path):
            old=run.k[index]@old; new=normalized[j][index]@new; nb+=run.port[index]
        target=math.exp(-t*nb/2)*old@np.linalg.inv(hs)
        max_tel=max(max_tel,near(new,target,'all-history operator telescoping'))
        max_state=max(max_state,near(new@psi_t,math.exp(-t*nb/2)*old@psi/math.sqrt(norm),'correct changed-input full-record equality'))
    require(np.linalg.norm(psi_t-psi)>1e-6,'unchanged input substitution must fail')
    GROUPS['normalized_channel_and_input']={'max_step_completeness_error':max_complete,
                 'sampled_word_identity_error':max_tel,'sampled_word_state_error':max_state,
                 'words_checked':len(histories),'all_word_statement':'proved by telescoping',
                 'preparation_shift_norm':float(np.linalg.norm(psi_t-psi))}
    # Same state vector on DATA x oldRIGHT; a nonzero LEFT unitary jet preserves its RIGHT Gram.
    rho=np.diag(np.arange(1,17,dtype=float));rho=rho/rho.trace()
    gen=np.zeros((16,16),complex);gen[0,15]=.31;gen[15,0]=-.31
    drho=gen@rho-rho@gen
    val=normalized_values(run,n,t,rho,drho)
    evalue=near(val['J'],val['Jratio'],'true complementary determinant ratio',tol=1e-11)
    esource=near(val['dJ'],val['dJratio'],'full complementary source incl normalizer',tol=1e-11)
    plus=normalized_values(rp,n,t,expm(step*gen)@rho@expm(-step*gen))
    minus=normalized_values(rm,n,t,expm(-step*gen)@rho@expm(step*gen))
    fd=(plus['S']-minus['S'])/(2*step)
    near(fd,val['dS'],'whole HJR complete derivative',tol=3e-6)
    near((plus['J']-minus['J'])/(2*step),val['dJ'],'complementary finite difference',tol=2e-8)
    near((plus['R']-minus['R'])/(2*step),val['dR'],'matter with normalized input derivative',tol=2e-8)
    # Derivative of the logdet-ratio normalizer is not optional.
    dropped=val['dJratio']-REF*np.trace(np.linalg.solve(val['h'],val['dh'])).real
    require(abs(dropped-val['dJ'])>1e-5,'normalizer-only deletion must fail')
    GROUPS['same_cut_complement_and_conditional_HJR']={
        'feedback_value':val['J'],'feedback_field_source':val['dJ'],
        'determinant_ratio_error':evalue,'source_ratio_error':esource,
        'raw_absolute_weight_norm':val['normalizer'],'raw_log_norm_source':val['dlognorm'],
        'H':val['H'],'J':val['J'],'R':val['R'],
        'dH':val['dH'],'dJ':val['dJ'],'dR':val['dR'],'dS':val['dS'],
        'whole_HJR_fd_error':float(abs(fd-val['dS'])),
        'source_if_logdet_normalizer_omitted':float(dropped),
        'scope':'conditional HJR evaluated on the normalized marked channel; not the original execution at t!=0'}
    # At t=0 the feedback marker derivative is fixed by actual port occupation.
    hn0=run.future(n,0)
    occ=np.zeros_like(eye); z=e1.copy()
    for _ in range(n): occ+=z;z=run.cp(z)
    near(-hn0[2][-1],occ,'original port-1 occupation effect')
    kn=np.linalg.matrix_power(run.b,2*n); mm=(1-Z)*eye+Z*kn
    predicted=-REF*Z*np.trace(np.linalg.solve(mm,kn@occ)).real
    jtplus=normalized_values(run,n,step,rho)['J']
    jtminus=normalized_values(run,n,-step,rho)['J']
    measured=(jtplus-jtminus)/(2*step)
    near(measured,predicted,'normalized complement marker derivative at zero',tol=2e-8)
    require(predicted<0,'normalization has actual signed loop response')
    GROUPS['zero_marker_exact_source']={'marker_feedback_source':float(predicted),
            'fd_error':float(abs(predicted-measured)),'port1_occupation_trace':float(np.trace(occ).real)}
    # Retained failure flag completes the raw contraction; no missing probability is erased.
    q=math.exp(-n*t)*h[-1]
    loss=eye-q;ls=sqrt_spd(loss)
    near(q+adj(ls)@ls,eye,'full retained failure completion')
    require(0<val['normalizer']<1,'positive nontrivial success and failure probabilities')
    # For a positive scalar multiplying an already-isometric full tape, completeness fixes it to 1.
    scalar=1.03
    require(np.linalg.norm(scalar**2*effects-eye)>.1,'free common scale is not a normalized complete instrument')
    # Scaling the actual return corner is not scaling its complementary effect.
    bb=np.linalg.matrix_power(run.b,n); oldf=eye-adj(bb)@bb
    scaled_true=eye-scalar**2*adj(bb)@bb
    falsef=scalar**2*oldf
    near(scaled_true-falsef,(1-scalar**2)*eye,'true complement vs multiplicative-F distinction')
    # Literal discrete Golden filtering: one fresh gate for cost 1, two for
    # cost 2. Every failure string is retained. The original outcome and
    # unexecuted blank flag slots remain distinguishable. No free filter.
    filtered=[]; filtblank=None
    import itertools
    for idx,kraus in enumerate(run.k):
        cost=1+int(run.port[idx])
        for bits in itertools.product((0,1),repeat=cost):
            amp=math.prod(math.sqrt(P) if bit==0 else P for bit in bits)
            filtered.append(amp*kraus)
            if idx==0 and all(bit==0 for bit in bits): filtblank=amp*kraus
    sum_effects=sum((adj(k)@k for k in filtered),np.zeros_like(eye))
    near(sum_effects,eye,'all Golden success/failure leaves complete')
    near(filtblank,math.sqrt(P)*run.b,'true literal filtered active blank')
    # Removing all filters' success requirement recovers the original data
    # channel, yet the new all-blank corner is not the polar-normalized one.
    trial=np.arange(256,dtype=float).reshape(16,16);trial=herm(trial.astype(complex))
    original_data=sum((k@trial@adj(k) for k in run.k),np.zeros_like(eye))
    filtered_data=sum((k@trial@adj(k) for k in filtered),np.zeros_like(eye))
    near(filtered_data,original_data,'full retained filter leaves preserve original reduced data channel')
    dblank=P**(n/2)*np.linalg.matrix_power(run.b,n)
    dblankjet=P**(n/2)*power_jet(run.b,run.db,n)[1]
    ff=eye-adj(dblank)@dblank
    dff=-(adj(dblankjet)@dblank+adj(dblank)@dblankjet)
    jphysical=-REF*np.log1p(-Z*np.linalg.eigvalsh(herm(ff))).sum()
    djphysical=REF*Z*np.trace(np.linalg.solve(eye-Z*ff,dff)).real
    GROUPS['literal_Golden_success_failure_completion']={
        'retained_one_round_outcomes':len(filtered),
        'full_completeness_error':err(sum_effects,eye),
        'unchanged_reduced_data_channel_error':err(filtered_data,original_data),
        'all_blank_amplitude_factor':'p^(n/2)',
        'true_complement_value':float(jphysical),
        'true_complement_field_source':float(djphysical),
        'polar_complement_field_source':float(val['dJ']),
        'extra_Golden_calls_per_history':'C_port(history)',
        'every_failure_retained':True,
        'gate_control_and_clock_admission_not_claimed':True}
    phase=np.exp(.17j);phase_slope=.31
    phased=phase*val['v'];dphased=phase*(val['dv']+1j*phase_slope*val['v'])
    phase_dret=adj(dphased)@phased+adj(phased)@dphased
    original_dret=adj(val['dv'])@val['v']+adj(val['v'])@val['dv']
    near(adj(phased)@phased,adj(val['v'])@val['v'],'true complement ignores common phase')
    near(phase_dret,original_dret,'common-phase first-source terms cancel exactly')
    GROUPS['negative_controls']={
        'scalar_normalizer_replacement':'REJECTED_BY_NONSCALAR_SPECTRUM',
        'unchanged_input_after_operator_normalization':'REJECTED',
        'omit_normalizer_logdet_source':'REJECTED',
        'multiply_feedback_instead_of_return_corner':'REJECTED',
        'unpaid_common_scalar_on_complete_tape':'REJECTED',
        'common_phase_complement_source':'EXACT_CANCELLATION_CHECKED',
        'retained_filter_failure_probability':float(1-val['normalizer'])}
    return {'status':'PASS','input_ref':INPUT_REF,'groups':GROUPS,
        'scope':{'native_full128_Fourier_fixture':True,'full_spatial_primary_replay':False,
                 'oldRIGHT128_tensor_action_identity':True,'normalized_tilt_may_change_RIGHT_marginal':True,'all_histories_contracted_not_enumerated':True,
                 'Doob_transform_admitted_native_gate':False,'physical_Info_derived':False,
                 'all42_Einstein_source':False,'GR_closed':False,'independent_review':False}}

if __name__=='__main__': print(json.dumps(run_all(),indent=2,ensure_ascii=False,sort_keys=True))
