#!/usr/bin/env python3
"""Native 128 -> 65 causal CQ price/source replay. Numerical checks, not Lean.

The original port reduction is consumed, not introduced here. All fixed-window
histories have one original Kraus word; structural dark slots are retained in
alphabet accounting and only their zero arithmetic is skipped. Tests use the
original CAR16 Fourier fixture, not the full spatial 42-field writer.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from native_excerpt import native, P, EYE
ELL=math.log(1/P)
CHECKS=[]
def require(ok,name):
    if not bool(ok): raise ArithmeticError(name)
    CHECKS.append(name)
def near(a,b,tol,name):
    require(float(np.max(np.abs(np.asarray(a)-np.asarray(b))))<tol,name)
def dag(a):return a.conj().swapaxes(-1,-2)
def trace(a):return np.trace(a,axis1=-2,axis2=-1).real

def xlogx_and_jet(X,DX,rtol=1e-13,need_log=False):
    """Relative support threshold; rank-stable numerical diagnostics only."""
    ev,U=np.linalg.eigh((X+dag(X))/2)
    top=np.max(ev,axis=-1,keepdims=True)
    require(np.min(ev)>=-2e-12*max(1.,float(np.max(top))), 'PSD block within roundoff')
    keep=ev>rtol*top
    logs=np.zeros_like(ev)
    np.log(ev,out=logs,where=keep)
    val=(ev*logs).sum(axis=-1)
    diag=np.diagonal(dag(U)@DX@U,axis1=-2,axis2=-1).real
    # d Tr X log X = Tr dX(log X+I) on a constant-support family.
    src=(diag*(logs+keep)).sum(axis=-1)
    lost=np.sum(np.abs(np.where(keep,0,diag)))
    require(lost<2e-9,'excluded-kernel derivative mass is roundoff')
    logm=(U*logs[...,None,:])@dag(U) if need_log else None
    return val,src,logm

def fixture(r=1/9,nu=.6):
    k,kt=native(2*np.arctanh(r),nu)
    dk=kt*2/(1-r*r)
    Delta=(EYE-k[0])/(2*P*P)
    dDelta=-dk[0]/(2*P*P)
    inv=np.linalg.inv(Delta); dinv=-inv@dDelta@inv
    z=trace(inv);dz=trace(dinv)
    rho=inv/z; drho=dinv/z-inv*dz/z**2
    return k,dk,rho,drho

def merge(k,dk):
    return (np.concatenate((k[:2],k[2::2]/P)),
            np.concatenate((dk[:2],dk[2::2]/P)),
            np.array([1.,2.]+[P**3]*63))

def expand(L,DL,C,m,dm,c):
    # Word chronology: each new original map multiplies on the LEFT.
    Q=m[None,:,:,:]@L[:,None,:,:]
    DQ=dm[None,:,:,:]@L[:,None,:,:]+m[None,:,:,:]@DL[:,None,:,:]
    return Q.reshape(-1,16,16),DQ.reshape(-1,16,16),(C[:,None]+c[None,:]).ravel()

def eval_words(L,DL,C,rho,drho,rtol=1e-13,gradient=False):
    total=np.zeros(9)
    Grad=np.zeros((16,16),complex)
    for b in range(0,len(L),1024):
        a=L[b:b+1024];da=DL[b:b+1024];cc=C[b:b+1024]
        X=a@rho@dag(a)
        DX=da@rho@dag(a)+a@drho@dag(a)+a@rho@dag(da)
        q=trace(X);dq=trace(DX)
        pos=q>0
        lq=np.zeros_like(q);np.log(q,out=lq,where=pos)
        en,den,logX=xlogx_and_jet(X,DX,rtol,gradient)
        total+=np.array([q.sum(),dq.sum(),q@cc,dq@cc,en.sum(),den.sum(),
                         -q@lq,-dq@(lq+1),float(len(q))])
        if gradient:
            Grad+=np.sum(dag(a)@((cc[:,None,None]*EYE+logX/ELL)@a),axis=0)
    inV,inD,logrho=xlogx_and_jet(rho,drho,rtol,gradient)
    cost=total[2];dCost=total[3]
    score=cost+(total[4]-inV)/ELL
    dscore=dCost+(total[5]-inD)/ELL
    pure=cost-total[6]/ELL
    dpure=dCost-total[7]/ELL
    I=total[4]-inV+total[6]
    dI=total[5]-inD+total[7]
    if gradient:Grad-=logrho/ELL
    return dict(normalization=total[0],normalization_jet=total[1],cost=cost,d_cost=dCost,
                cq_score=score,d_cq_score=dscore,purified_score=pure,d_purified_score=dpure,
                history_entropy=total[6],d_history_entropy=total[7],reference_information=I,
                d_reference_information=dI,positive_word_count=int(total[8])),Grad

def tree(k,dk,c,rho,drho,n,rtol=1e-13,gradient=False):
    live=np.linalg.norm(k,axis=(1,2))>1e-13
    require(np.max(np.linalg.norm(dk[~live],axis=(1,2)),initial=0)<1e-12,'structural dark source zero')
    m,dm,cc=k[live],dk[live],c[live]
    L=EYE[None,:,:];DL=np.zeros_like(L);C=np.zeros(1)
    for _ in range(n):L,DL,C=expand(L,DL,C,m,dm,cc)
    return eval_words(L,DL,C,rho,drho,rtol,gradient)

def one_step_normalized(s,ds,m,dm,c):
    X=m@s@dag(m)
    DX=dm@s@dag(m)+m@ds@dag(m)+m@s@dag(dm)
    q=trace(X);dq=trace(DX)
    en,den,_=xlogx_and_jet(X,DX)
    e,de,_=xlogx_and_jet(s,ds)
    return q@c+(en.sum()-e)/ELL,dq@c+(den.sum()-de)/ELL

def causal_forward(m,dm,c,rho,drho,n):
    """Independent normalized-filter recurrence, exact finite sum."""
    live=np.linalg.norm(m,axis=(1,2))>1e-13;m=m[live];dm=dm[live];c=c[live]
    states=[(1.,0.,rho,drho)]
    total=deriv=0.
    for t in range(n):
        nxt=[]
        for w,dw,s,ds in states:
            val,dval=one_step_normalized(s,ds,m,dm,c)
            total+=w*val;deriv+=dw*val+w*dval
            if t+1<n:
                X=m@s@dag(m);DX=dm@s@dag(m)+m@ds@dag(m)+m@s@dag(dm)
                q=trace(X);dq=trace(DX)
                for a in range(len(m)):
                    if q[a]>1e-25:
                        u=X[a]/q[a];du=(DX[a]-u*dq[a])/q[a]
                        nxt.append((w*q[a],dw*q[a]+w*dq[a],u,du))
        states=nxt
    return total,deriv

def causal_backward(X,m,dm,c,n):
    """Unnormalized causal value, input covector, fixed-input field source.

    This is an exact tree recurrence, not a claimed finite-state speedup.
    Local gradients are represented on the support face of X.
    """
    if n==0:
        return 0.,np.zeros_like(X),0.
    live=np.linalg.norm(m,axis=(1,2))>1e-13
    m=m[live];dm=dm[live];c=c[live]
    Y=m@X@dag(m)
    DY=dm@X@dag(m)+m@X@dag(dm)
    val,dval,logY=xlogx_and_jet(Y,DY,need_log=True)
    inV,_,logX=xlogx_and_jet(X,np.zeros_like(X),need_log=True)
    q=trace(Y)
    value=q@c+(val.sum()-inV)/ELL
    field=trace(DY)@c+dval.sum()/ELL
    C=np.sum(dag(m)@(c[:,None,None]*m),axis=0)
    G=C+(np.sum(dag(m)@logY@m,axis=0)-logX)/ELL
    if n>1:
        for j in range(len(m)):
            if q[j]>1e-25:
                v,g,a=causal_backward(Y[j],m,dm,c,n-1)
                value+=v;G+=dag(m[j])@g@m[j]
                field+=a+trace(g@DY[j])
    ev,U=np.linalg.eigh((X+dag(X))/2)
    keep=ev>1e-13*max(ev)
    supp=(U*keep[None,:])@dag(U)
    G=supp@G@supp
    return float(value),G,float(field)


def main():
    k,dk,rho,drho=fixture();m,dm,c=merge(k,dk);finecost=1.+np.arange(128)%2
    near(sum(dag(k)@k),EYE,1e-12,'original full128 TP')
    near(sum(dag(m)@m),EYE,1e-12,'65-slot reduced efficient instrument TP')
    near(sum(k@rho@dag(k)),rho,1e-12,'actual inverse-Delta input stationary')
    near(sum(dk@rho@dag(k)+k@drho@dag(k)+k@rho@dag(dk)),drho,2e-12,'stationary input full moving jet')
    near(P**3,2*P-1,1e-15,'native Golden net pair coefficient')
    for j in range(1,64):
        near(k[2*j],P*m[j+1],2e-15,'original even pair factor')
        near(k[2*j+1],math.sqrt(P)*m[j+1],2e-15,'original odd pair factor')
    results={}
    for n in (1,2,3):
        res,_=tree(m,dm,c,rho,drho,n)
        near(res['normalization'],1.,2e-12,'all merged histories normalized')
        near(res['normalization_jet'],0.,2e-11,'all merged history source normalized')
        causal=causal_forward(m,dm,c,rho,drho,n)
        near(causal,(res['cq_score'],res['d_cq_score']),2e-10,'normalized causal filter equals direct CQ word blocks')
        near(res['cq_score']-res['purified_score'],res['reference_information']/ELL,2e-12,'complete reference-cut source value')
        near(res['d_cq_score']-res['d_purified_score'],res['d_reference_information']/ELL,2e-12,'complete reference-cut first source')
        require(-1e-12<=res['reference_information']<=math.log(16)+1e-12,'finite reference boundary bound')
        if n<=2:
            full,_=tree(k,dk,finecost,rho,drho,n)
            for key in ('cq_score','d_cq_score','purified_score','d_purified_score','reference_information','d_reference_information'):
                near(res[key],full[key],2e-10,'same ORIGINAL fine and merged '+key)
            res['fine_positive_word_count']=full['positive_word_count']
        # Same constant support checked with two stricter thresholds.
        for tol in (1e-12,1e-14):
            alt,_=tree(m,dm,c,rho,drho,n,rtol=tol)
            near((alt['cq_score'],alt['d_cq_score']),
                 (res['cq_score'],res['d_cq_score']),3e-10,'support-threshold stability')
        results[str(n)]=res
    # A genuinely independent input tangent, unlike drho_*(r).
    Z=np.diag(np.arange(16)-7.5).astype(complex);Z/=np.linalg.norm(Z)
    got,G=tree(m,np.zeros_like(dm),c,rho,Z,2,gradient=True)
    near(trace(G@Z),got['d_cq_score'],2e-11,'backward initial matrix covector independent input')
    near(G,dag(G),1e-11,'initial preparation covector Hermitian')
    bv,bg,ba=causal_backward(rho,m,dm,c,2)
    near(bg,G,3e-11,'all 256 complex input-covector entries: backward recursion vs direct words')
    near(bv,results['2']['cq_score'],2e-11,'backward whole-price value')
    near(ba+trace(bg@drho),results['2']['d_cq_score'],3e-10,'backward full source including input reaction')
    gradn=np.linalg.norm(G-trace(G)*EYE/16)
    require(gradn>1e-5,'independent mixed preparation source is NOT silently zero')
    eps=2e-5
    plus,_=tree(m,np.zeros_like(dm),c,rho+eps*Z,np.zeros_like(Z),2)
    minus,_=tree(m,np.zeros_like(dm),c,rho-eps*Z,np.zeros_like(Z),2)
    near((plus['cq_score']-minus['cq_score'])/(2*eps),got['d_cq_score'],3e-8,'independent input source finite difference')
    # Actual moving input vs frozen input. They need not agree.
    frozen,_=tree(m,dm,c,rho,np.zeros_like(drho),2)
    prep=trace(G@drho)
    near(frozen['d_cq_score']+prep,results['2']['d_cq_score'],3e-10,'field + actual preparation chain source')
    require(abs(prep)>1e-8,'physical derivative cannot freeze stationary preparation')
    # Native boost central secant, original kernels AND input re-created.
    vals=[]
    for r in (1/9-2e-5,1/9+2e-5):
        kk,dd,rr,rrd=fixture(r);mm,dmm,cc=merge(kk,dd)
        val,_=tree(mm,dmm,cc,rr,rrd,2); vals.append(val['cq_score'])
    sec=(vals[1]-vals[0])/4e-5
    near(sec,results['2']['d_cq_score'],2e-8,'true native boost source independent secant')
    # Fixed input class: stationary sequence entropy prediction defect.
    H1=results['1']['history_entropy'];dH1=results['1']['d_history_entropy']
    for n in (1,2,3):
        z=results[str(n)]
        z['predictive_defect']=n*H1-z['history_entropy']
        z['d_predictive_defect']=n*dH1-z['d_history_entropy']
        require(z['predictive_defect']>=-2e-12,'nonreset predictive relative entropy nonnegative')
    # Direct relative-entropy sum independently checks the tiny prediction gap.
    live=np.linalg.norm(m,axis=(1,2))>1e-13
    mm=m[live];dd=dm[live]
    X=mm@rho@dag(mm);DX=dd@rho@dag(mm)+mm@drho@dag(mm)+mm@rho@dag(dd)
    q=trace(X);dq=trace(DX)
    qq=trace(mm[None,:,:,:]@X[:,None,:,:]@dag(mm)[None,:,:,:])
    dqq=trace(dd[None,:,:,:]@X[:,None,:,:]@dag(mm)[None,:,:,:]
              +mm[None,:,:,:]@DX[:,None,:,:]@dag(mm)[None,:,:,:]
              +mm[None,:,:,:]@X[:,None,:,:]@dag(dd)[None,:,:,:])
    prod=q[:,None]*q[None,:]
    logratio=np.log1p((qq-prod)/prod)
    kl=float(np.sum(qq*logratio))
    dkl=float(np.sum(dqq*logratio))  # equal stationary one-step marginals
    near(kl,results['2']['predictive_defect'],2e-14,'direct joint-KL equals entropy gap')
    near(dkl,results['2']['d_predictive_defect'],2e-13,'direct joint-KL source equals entropy difference')
    require(kl>1e-12,'actual native two-step labels have nonzero predictive information')
    results['2']['predictive_defect_direct_KL']=kl
    results['2']['d_predictive_defect_direct_KL']=dkl
    output={'status':'PASS_NUMERICAL_NATIVE65_CAUSAL_CQ_SOURCE','checks':len(CHECKS),
            'source_commit':'b4a1c590ebb7c52e5be7618fa193d48a5176ad62',
            'upstream_blob':'ee8de4635d24c668949ac9a0186616ab7d59f2ed',
            'source_access':'connector-fetched excerpt, NOT full checkout/blob replay',
            'original_slots':128,'merged_slots':65,'live_original':64,'live_merged':33,
            'data_dimension':16,'boost_r':'1/9','amplitude_nu':'3/5',
            'results':results,'two_tick_independent_input':{
                'tangent_source':got['d_cq_score'],'traceless_covector_norm':float(gradn),'backward_covector_max_error':float(np.max(np.abs(bg-G))),
                'backward_full_source':float(ba+trace(bg@drho)),
                'moving_preparation_contribution':float(prep),
                'frozen_input_field_source':frozen['d_cq_score'],
                'full_field_secant':sec},
            'scope':{'all42_physical_writer_executed':False,'compulsory_Book03_price_selected':False,
                     'interval_certificate':False,'new_Lean_or_CI':False,'GR_closed':False}}
    print(json.dumps(output,indent=2))
if __name__=='__main__':main()
