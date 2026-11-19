#!/usr/bin/env python3
"""Bounded native-original replay plus exact scalar algebra; NOT GR closure.
Outputs JSON, does not overwrite expected receipts. Guards remain under -O.
"""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
import numpy as np
import sympy as sp
from native_excerpt import native,adj,EYE,P,root
from scipy.linalg import solve_sylvester,expm
from native_weld import build,native_feedback
ROOT=Path(__file__).resolve().parent
checks=[];errors={}

def require(test,name):
    if not bool(test):raise RuntimeError(name)
    checks.append(name)

def close(a,b,name,tol=2e-11):
    err=float(np.max(np.abs(a-b)))
    errors[name]=err;require(err<tol,name)

def scalar_algebra():
    p,x=sp.symbols('p x',real=True)
    reduce=lambda e:sp.rem(sp.Poly(sp.expand(e),p),sp.Poly(p*p+p-1,p)).as_expr()
    require(reduce((1-2*p*p*x)**2+4*p**3*x*x+4*p*p*x*(1-x)-1)==0,'exact complete blank/orphan/nonblank identity')
    require(reduce((1-(1-2*p*p*x)**2)-4*p*p*x*(1-p*p*x))==0,'exact initialized-cut feedback')
    require(reduce(4*p*p*(1-p*p)-4*p**3)==0,'exact full-work projector feedback eigenvalue')
    require(reduce((p*p+2*p)-(2-p)-p**3)==0,'exact original nonblank Golden Cost-Info p^3')
    require(reduce(p+p*p-1)==0,'Golden normalization')
    # A genuine rational nonprojector compression, with its complete projection.
    C=sp.diag(sp.Rational(3,5),sp.Rational(5,13))
    S=sp.diag(sp.Rational(4,5),sp.Rational(12,13))
    Q=(C.col_join(S))*(C.row_join(S))
    require(Q*Q==Q,'exact rational full projection control')
    D=Q[:2,:2]
    require(D*D!=D,'exact rational initialized compression is not a projection')
    require((sp.eye(4)[:,:2].T*Q*sp.eye(4)[:,:2])==D,'exact rational compression control')


def macro_replay(m):
    """Forward-only algebraic blocks, not a physical native tick-cost claim."""
    d=1024;Icol=m['J'];Zc=m['Zc'];p=P
    B=np.vstack([Icol,np.zeros_like(Icol)]);dB=np.zeros_like(B)
    initial=B.copy();prefixes=[];dprefixes=[]
    def gate(B,dB,name):
        a,b=B[:d],B[d:];da,db=dB[:d],dB[d:]
        if name=='G':
            return (np.vstack([np.sqrt(p)*a-p*b,p*a+np.sqrt(p)*b]),
                    np.vstack([np.sqrt(p)*da-p*db,p*da+np.sqrt(p)*db]))
        if name=='W':
            return (np.vstack([m['W']@a,m['W']@b]),
                    np.vstack([m['dW']@a+m['W']@da,m['dW']@b+m['W']@db]))
        if name=='S':
            o=B.copy();do=dB.copy();o[d:d+16]*=-1;do[d:d+16]*=-1;return o,do
        if name=='Zc':return (B*np.r_[Zc,Zc][:,None],dB*np.r_[Zc,Zc][:,None])
        if name=='Zp':return np.vstack([a,-b]),np.vstack([da,-db])
        raise ValueError(name)
    names=['G','W','S','Zc','W','Zc','Zp','G','Zp']
    for name in names:
        prefixes.append(B.copy());dprefixes.append(dB.copy())
        B,dB=gate(B,dB,name)
    K=np.empty_like(m['K']);dK=np.empty_like(m['dK'])
    K[::2]=B[:d].reshape(64,16,16);K[1::2]=B[d:].reshape(64,16,16)
    dK[::2]=dB[:d].reshape(64,16,16);dK[1::2]=dB[d:].reshape(64,16,16)
    close(K,m['K'],'nine-block actual-column replay')
    close(dK,m['dK'],'nine-block moving-column derivative')
    # Each actual source stage retains all other stages in its complement.
    sums=np.zeros((16,16),complex);dsums=np.zeros_like(sums)
    for t,name in enumerate(names):
        V,dV=gate(prefixes[t],dprefixes[t],name)
        target=prefixes[t+1] if t+1<len(names) else initial
        dtarget=dprefixes[t+1] if t+1<len(names) else np.zeros_like(initial)
        overlap=adj(target)@V
        doverlap=adj(dtarget)@V+adj(target)@dV
        F=EYE-adj(overlap)@overlap
        dF=-adj(doverlap)@overlap-adj(overlap)@doverlap
        if t<len(names)-1:
            close(F,0,f'clock transported stage {t} feedback zero')
            close(dF,0,f'clock transported stage {t} source zero')
        else:
            f=native_feedback(m['D'],m['dD'])
            close(F,f['F'],'sole true clock return equals full128 Fpre')
            close(dF,f['dF'],'sole moving clock return source retained')
        sums+=F;dsums+=dF
    return names


def all_two_tick(k,dk,k2,dk2,D,dD):
    inv=np.linalg.inv(D);dinv=-inv@dD@inv
    rho=inv/np.trace(inv);drho=(dinv-rho*np.trace(dinv))/np.trace(inv)
    norm=dnorm=cost=dcost=0.0
    maxerr=maxderr=0.0
    for b in range(128):
        words=np.einsum('ij,ajk->aik',k[b],k)
        dwords=np.einsum('ij,ajk->aik',dk[b],k)+np.einsum('ij,ajk->aik',k[b],dk)
        words2=np.einsum('ij,ajk->aik',k2[b],k2)
        dwords2=np.einsum('ij,ajk->aik',dk2[b],k2)+np.einsum('ij,ajk->aik',k2[b],dk2)
        maxerr=max(maxerr,float(np.max(np.abs(words-words2))))
        maxderr=max(maxderr,float(np.max(np.abs(dwords-dwords2))))
        prob=np.einsum('aij,jk,aik->a',words,rho,words.conj()).real
        dprob=(2*np.einsum('aij,jk,aik->a',dwords,rho,words.conj()).real+
               np.einsum('aij,jk,aik->a',words,drho,words.conj()).real)
        c=2+(np.arange(128)%2)+(b%2)
        norm+=float(prob.sum());dnorm+=float(dprob.sum())
        cost+=float(prob@c);dcost+=float(dprob@c)
    require(maxerr<2e-13,'all 16384 no-reset chronological operators preserved')
    require(maxderr<2e-13,'all 16384 no-reset chronological derivatives preserved')
    require(abs(norm-1)<2e-12 and abs(dnorm)<2e-12,'full two-tick probability and moving preparation normalize')
    errors['all_two_tick_K']=maxerr;errors['all_two_tick_dK']=maxderr
    return dict(full_formal_words=16384,probability_sum=norm,derivative_sum=dnorm,
                actual_port_cost=cost,d_rapidity_port_cost=dcost)


def main():
    require(hashlib.sha256((ROOT/'native_excerpt.py').read_bytes()).hexdigest()==
            'e0952ad01abd3c54b3c083271d640374c42c2a25cf455e1937cceb3339d82e8b','pinned unchanged original constructor excerpt')
    scalar_algebra()
    r=1/9;th=2*np.arctanh(r)
    m=build(th);k,dk=native(th)
    close(adj(m['W'])@m['W'],np.eye(1024),'whole original Walsh Julia completion unitary')
    close(m['N']@adj(m['N']),EYE,'original coisometry row')
    close(m['Q']@m['Q'],m['Q'],'1024 carrier actual projector')
    close(adj(m['Q']),m['Q'],'1024 carrier selfadjoint projector')
    close(m['dQ']@m['Q']+m['Q']@m['dQ'],m['dQ'],'full moving projector tangent')
    close(adj(m['W']),m['Zc'][:,None]*m['W']*m['Zc'][None,:],'forward sign-conjugated Walsh Julia adjoint')
    close(adj(m['dW']),m['Zc'][:,None]*m['dW']*m['Zc'][None,:],'moving forward adjoint identity')
    close(k,m['K'],'all128 original Kraus matrices identical')
    close(dk,m['dK'],'all128 native rapidity derivatives identical')
    require(abs(np.trace(m['Q']).real-16)<2e-12,'true rank16 dilated projection')
    close(sum(adj(x)@x for x in k),EYE,'all128 CPTP with nonblank sectors')
    delta=m['D'];dd=m['dD'];nb=4*P**2*delta@(EYE-delta)
    close(sum(adj(x)@x for x in k[2:]),nb,'all126 nonblank effect retained')
    require(np.linalg.eigvalsh(nb).min()>0.019,'nonblank probability strictly material at native fixture')
    rho=np.linalg.inv(delta);rho/=np.trace(rho)
    qnb=float(np.trace(rho@nb).real)
    require(abs(qnb-0.0207857243508978)<1e-13,'native stationary nonblank probability owner match')
    # Consume the concurrent minimal Halmos/row-refinement owner: identify its
    # exact isometry inside the OLD 1024-dimensional native work, not new gates.
    S=root(delta@(EYE-delta))
    dS=solve_sylvester(S,S,dd-dd@delta-delta@dd)
    Sinv=np.linalg.inv(S);JJ=m['J']
    R=(m['Q']@JJ-JJ@delta)@Sinv
    dR=(m['dQ']@JJ-JJ@dd)@Sinv-R@dS@Sinv
    T=np.hstack([JJ,R]);dT=np.hstack([np.zeros_like(JJ),dR])
    Qmin=np.block([[delta,S],[S,EYE-delta]])
    dQmin=np.block([[dd,dS],[dS,-dd]])
    close(adj(T)@T,np.eye(32),'minimal doubled work embedded in original register')
    close(m['Q']@T,T@Qmin,'native projector intertwines exact minimal Halmos owner')
    close(m['dQ']@T+m['Q']@dT,dT@Qmin+T@dQmin,'moving minimal-to-native intertwiner derivative')
    close(m['Q'],T@Qmin@adj(T),'all nonzero projector range lies in doubled-work subspace')
    close(R[16:].reshape(63,16,16),-np.einsum('aij,jk->aik',k[2::2],Sinv)/(2*P**2),'all63 original row refinements exactly embedded')
    missing=-2*P**2*np.einsum('aij,jk->aik',dR[16:].reshape(63,16,16),S)
    require(np.max(np.abs(missing))>1e-4,'row-refinement field source is material, not free frozen work')
    fnow=native_feedback(delta,dd)
    zmin=32+2*np.trace(expm(-2*P**2*fnow['F'])).real
    dhmin=-2*np.trace(expm(-2*P**2*fnow['F'])@fnow['dF']).real/zmin
    require(abs(dhmin-fnow['dH_cut'])>1e-4,'same channel minimal/full carrier heat sources differ')
    minimal_comparison=dict(minimal_U_dimension=64,native_U_dimension=2048,
      exact_extra_identity_dimension=1984,minimal_paired_heat_zeros=32,
      native_paired_heat_zeros=2016,d_rapidity_H_minimal=float(dhmin),
      d_rapidity_H_native=fnow['dH_cut'],
      d_rapidity_heat_difference=float(fnow['dH_cut']-dhmin),
      nonzero_source_if_row_refinement_frozen=float(np.max(np.abs(missing))))
    seq=macro_replay(m)
    histories=all_two_tick(k,dk,m['K'],m['dK'],delta,dd)
    f=native_feedback(delta,dd)
    dJcomm=float(np.trace(f['source_D']@dd).real)
    close(dJcomm,f['dJ'],'matrix cotangent source at initialized boundary',tol=2e-13)
    # Explicit commutator pullback to original W; no frozen moving projector.
    JJ=m['J'];B=m['W']@JJ
    T=B@f['source_D']@adj(B)
    E=np.zeros((1024,1024),complex);E[:16,:16]=EYE
    Omega=m['dW']@adj(m['W'])
    comm=float(np.trace((T@E-E@T)@Omega).real)
    close(comm,f['dJ'],'all-operator boundary commutator source',tol=2e-13)
    eps=2e-5
    plus=build(th+eps);minus=build(th-eps)
    for stages in [1,9,16]:
        f0=native_feedback(delta,dd,clock_stages=stages)
        fp=native_feedback(plus['D'],plus['dD'],clock_stages=stages)
        fm=native_feedback(minus['D'],minus['dD'],clock_stages=stages)
        close((fp['J']-fm['J'])/(2*eps),f0['dJ'],f'actual initialized determinant finite difference stages={stages}',tol=3e-11)
        close((fp['H_cut']-fm['H_cut'])/(2*eps),f0['dH_cut'],f'actual paired-cut heat finite difference stages={stages}',tol=3e-10)
    # Same literal matrices away from the selected point, not just one first jet.
    for th2 in [0.0,0.08,-0.12]:
        b=build(th2);k0,dk0=native(th2)
        close(b['K'],k0,f'native all128 offpoint theta={th2}')
        close(b['dK'],dk0,f'native all128 offpoint jet theta={th2}')
    # OldRIGHT remains a tensor factor. Normalize only states, not Book trace.
    f1=native_feedback(delta,dd,right_rank=1)
    close(f['J'],128*f1['J'],'actual oldRIGHT128 unnormalized determinant multiplier')
    close(f['dH_cut'],f1['dH_cut'],'oldRIGHT128 cancels only from normalized thermal derivative')
    close(f['H_cut']-f1['H_cut'],np.log(128)/(2*P**2),'oldRIGHT128 absolute heat constant retained')
    # Rank16 full-work predicate cut, a different active algebra, is isospectral.
    wide_J=-128*16*np.log1p(-(2**-20)*4*P**3)
    wide_source=128*(2**-20)*4*P**3/(1-(2**-20)*4*P**3)*np.trace(m['dQ']).real
    require(abs(wide_source)<1e-14,'same U full-work cut has zero field determinant source')
    data={
      'status':'PASS_ORIGINAL_FULL128_FAITHFUL_DILATION_AND_BOUNDARY_SOURCE_NOT_GR',
      'source_commit':'f090c0124c389e95e163611624a0f88b921a892a',
      'concurrent_minimal_dilation_consumed_at':'52aa5274533d7fc1eaacc30f4af1cfedc175e9bf',
      'checks':len(checks),'check_names':checks,'maximum_errors':errors,
      'dimensions':{'data':16,'Julia_Walsh':1024,'original_with_Golden_port':2048,'retained_oldRIGHT':128},
      'native_boost_coordinate':{'r':r,'theta_rapidity':th,'derivative_coordinate':'theta, not r','dtheta_dr':2/(1-r*r)},
      'Delta_spectral_endpoints':np.linalg.eigvalsh(delta)[[0,-1]].tolist(),
      'nonblank_stationary_probability':qnb,
      'forward_macro_sequence':seq,'macro_count_is_not_paid_primitive_tick_count':True,
      'all_two_tick':histories,
      'minimal_native_carrier_composition':minimal_comparison,
      'initialized_Book':{a:f[a] for a in ['J','dJ','H_cut','dH_cut','dH_plus_J','zeros','Zbase']},
      'full_work_cut':{'J':float(wide_J),'dJ':float(wide_source)},
      'paired_heat_scope':'CdaggerC+CCdagger on entire declared ambient carrier; NOT identified actual scene Hodge',
      'constructor_is_excerpt':True,'full42_field_admission':False,
      'all_coordinate_transport':'exact operator theorem for any supplied smooth native word family; only original rapidity checked numerically',
      'physical_active_cut_selected':False,'GR_closed':False,
      'verification':'analytical identities and exact symbolic controls plus double-precision original matrix replay; not interval-certified or Lean'}
    print(json.dumps(data,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
