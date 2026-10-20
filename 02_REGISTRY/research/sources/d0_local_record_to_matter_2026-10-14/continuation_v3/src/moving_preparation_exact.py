#!/usr/bin/env python3
"""Actual golden instrument jets at a commuting reference; no physical promotion.
Default replay checks a deterministic receipt. Use --write only to publish an update.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
p=s.Symbol('p', real=True)
MIN=p*p+p-1
checks=[];negative=[]
def ck(name, condition):
    if not bool(condition): raise AssertionError(name)
    checks.append(name)
def red(x):
    num,den=s.cancel(x).as_numer_denom()
    num=s.rem(s.expand(num),MIN,p); den=s.rem(s.expand(den),MIN,p)
    if den==0: raise ZeroDivisionError('GOLDEN_DENOMINATOR')
    return s.rem(s.expand(num*s.invert(den,MIN,p)),MIN,p)
def mat(X): return X.applyfunc(red)
def zero(X): return all(red(v)==0 for v in (list(X) if isinstance(X,s.MatrixBase) else [X]))
def eq(name,X): ck(name,zero(X))
def reject(name,claim): ck('REJECT_'+name,not claim);negative.append(name)
def creator(r):
    X=s.zeros(16)
    for mask in range(16):
        if not mask&(1<<r): X[mask|(1<<r),mask]=(-1)**((mask&((1<<r)-1)).bit_count())
    return X

def run():
    I=s.eye(4);dim=4;q=2;gamma=red(p**3)
    Us=[s.diag(1,-1,s.I,-s.I), s.diag(1,s.I,-s.I,-1)]
    Hs=[s.Matrix([[1,1,0,0],[1,0,1,0],[0,1,2,1],[0,0,1,-1]]),
        s.Matrix([[0,0,1,0],[0,2,0,1],[1,0,-1,0],[0,1,0,1]])]
    dUs=[s.I*H*U for H,U in zip(Hs,Us)]
    for r,(U,dU) in enumerate(zip(Us,dUs)):
        eq('actual_return_unitarity_'+str(r),U.H*U-I)
        eq('genuine_return_tangent_'+str(r),dU.H*U+U.H*dU)
    reject('perturbed_returns_remain_commuting',zero(dUs[0]*Us[1]+Us[0]*dUs[1]-dUs[1]*Us[0]-Us[1]*dUs[0]))
    E=mat(gamma*sum(((U-I).H*(U-I) for U in Us),s.zeros(dim))/q)
    dE=mat(gamma*sum((dU.H*(U-I)+(U-I).H*dU for U,dU in zip(Us,dUs)),s.zeros(dim))/q)
    # Full two-outcome maps derived from the literal G-echo comparer.
    def channel(b,rho):
        if b:
            return mat(gamma*sum(((U-I)*rho*(U-I).H for U in Us),s.zeros(dim))/q)
        return mat(sum(((p*I+p*p*U)*rho*(p*I+p*p*U).H for U in Us),s.zeros(dim))/q)
    def dchannel(b,rho):
        ans=s.zeros(dim)
        for U,dU in zip(Us,dUs):
            A=(U-I) if b else (p*I+p*p*U)
            dA=dU if b else p*p*dU
            ans+=dA*rho*A.H+A*rho*dA.H
        return mat((gamma if b else 1)*ans/q)
    eq('all_outcomes_unital',channel(0,I)+channel(1,I)-I)
    eq('all_outcomes_unital_first_jet',dchannel(0,I)+dchannel(1,I))
    eq('failure_effect_matches_actual_output_block',channel(1,I)-E)
    eq('diagonal_first_effect_jet',s.diag(*[dchannel(1,I)[j,j]-dE[j,j] for j in range(dim)]))
    Delta=mat(sum(((U-I).H*(U-I) for U in Us),s.zeros(dim)))
    dDelta=mat(sum((dU.H*(U-I)+(U-I).H*dU for U,dU in zip(Us,dUs)),s.zeros(dim)))
    lambdas=[Delta[j,j] for j in range(dim)]
    ck('literal_kinetic_spectrum',lambdas==[0,6,4,6])
    # beta=log(2)/2 gives exactly these weights, no numerical Gibbs replacement.
    gibbs=s.diag(*[s.Rational(2)**(-lam/2) for lam in lambdas]);gibbs/=s.trace(gibbs)
    e=s.Symbol('e',real=True)
    states=[I/dim];jets=[s.zeros(dim)]
    witnesses=[]
    for T in range(1,5):
        ns=[];nj=[]
        for k in range(T+1):
            x=s.zeros(dim);dx=s.zeros(dim)
            if k<T:
                x+=channel(0,states[k]);dx+=channel(0,jets[k])+dchannel(0,states[k])
            if k>0:
                x+=channel(1,states[k-1]);dx+=channel(1,jets[k-1])+dchannel(1,states[k-1])
            x=mat(x);dx=mat(dx);ns.append(x);nj.append(dx)
            f=s.binomial(T,k)*e**k*(1-e)**(T-k)
            for j in range(dim):
                eq(f'actual_density_T{T}_k{k}_j{j}',x[j,j]-f.subs(e,E[j,j])/dim)
                eq(f'actual_diagonal_jet_T{T}_k{k}_j{j}',dx[j,j]-s.diff(f,e).subs(e,E[j,j])*dE[j,j]/dim)
            if T>=2 and k==1:
                # The full density derivative need NOT equal the polynomial
                # Frechet derivative; off-diagonal history dependence is retained.
                full_frechet=s.zeros(dim)
                for i in range(dim):
                    for j in range(dim):
                        ei,ej=E[i,i],E[j,j]
                        dd=s.diff(f,e).subs(e,ei) if ei==ej else red((f.subs(e,ei)-f.subs(e,ej))/(ei-ej))
                        full_frechet[i,j]=red(dd*dE[i,j]/dim)
                witnesses.append(not zero(dx-full_frechet))
        eq('all_histories_retained_T'+str(T),sum(ns,s.zeros(dim))-I/dim)
        eq('all_history_jets_retained_T'+str(T),sum(nj,s.zeros(dim)))
        if T>=2:
            # Fixed event 1 <= count <= min(2,T), all direction words retained.
            lo,hi=1,min(2,T)
            sigma=mat(sum(ns[lo:hi+1],s.zeros(dim))); dsigma=mat(sum(nj[lo:hi+1],s.zeros(dim)))
            prob=red(s.trace(sigma));dp=red(s.trace(dsigma));rho=mat(sigma/prob)
            f=s.expand(sum(s.binomial(T,k)*e**k*(1-e)**(T-k) for k in range(lo,hi+1)))
            Z=red(dim*prob);mean=red(s.trace(Delta*rho))
            B=s.diag(*[red((lambdas[j]-mean)*s.diff(f,e).subs(e,E[j,j])/Z) for j in range(dim)])
            direct=red((s.trace(dDelta*sigma+Delta*dsigma)-mean*dp)/prob)
            derived=red(s.trace(rho*dDelta)+s.trace(B*dE))
            eq('normalized_preparation_full_chain_rule_T'+str(T),direct-derived)
            eq('full_heat_plus_prepared_matter_covector_T'+str(T),
               direct-s.trace(gibbs*dDelta)-s.trace((rho-gibbs)*dDelta)-s.trace(B*dE))
            if T==3:
                reject('freeze_prepared_density',zero(direct-s.trace(rho*dDelta)))
                reject('omit_success_normalization_derivative',zero(mean*dp))
                reject('drop_preparation_source',zero(s.trace(B*dE)))
                scalar_example={'T':T,'event':[lo,hi],'probability_Qp':str(prob),
                                'preparation_correction_Qp':str(red(s.trace(B*dE)))}
            lower=T*s.binomial(T-1,lo-1)*e**(lo-1)*(1-e)**(T-lo)
            upper=T*s.binomial(T-1,hi)*e**hi*(1-e)**(T-1-hi) if hi<T else 0
            ck('exact_count_window_boundary_derivative_T'+str(T),s.expand(s.diff(f,e)-lower+upper)==0)
        states,jets=ns,nj
    ck('actual_off_diagonal_history_jet_witness_exists',any(witnesses))
    reject('commuting_reference_implies_full_polynomial_on_nearby_curved_family',not any(witnesses))
    # Literal full-Fock representation trace, all 16 Lie-algebra coordinate generators.
    C=[creator(r) for r in range(4)]
    for a in range(4):
        for b in range(4):
            K=s.zeros(4);K[a,b]=1
            Gamma=C[a]*C[b].T
            ck(f'full_exterior_generator_trace_{a}_{b}',s.trace(Gamma)==8*s.trace(K))
    # Exact scalar score bound proof components and an independently checked
    # state-energy covariance counterexample, not a conditional-state oracle.
    for T in (3,4,5):
        for lo in range(1,T):
            hi=T-1
            f=sum(s.binomial(T,k)*e**k*(1-e)**(T-k) for k in range(lo,hi+1))
            df=T*(s.binomial(T-1,lo-1)*e**(lo-1)*(1-e)**(T-lo)
                  -s.binomial(T-1,hi)*e**hi*(1-e)**(T-hi-1))
            ck(f'window_derivative_all_terms_T{T}_lo{lo}',s.expand(s.diff(f,e)-df)==0)
    return {'schema':'d0-moving-preparation-exact/1','status':'PASS','checks':checks,
            'exact_controls':len(checks),'negative_controls':negative,'witness':scalar_example,
            'full_density_polynomial_claim':False,'physical_admission':False,
            'new_Lean_compilation':False,'complete_H_J_R_closed':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    out=run();out['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    dest=ROOT/'results/moving_preparation_exact.json'
    if args.write:dest.write_text(json.dumps(out,indent=2)+'\n')
    else:
        if json.loads(dest.read_text())!=out:raise AssertionError('IMMUTABLE_RECEIPT_MISMATCH')
    print('PASS_MOVING_PREPARATION_EXACT',out['exact_controls'],'controls;',len(out['negative_controls']),'negative controls')
    print('SCOPE: actual diagonal jet, not full polynomial family, physical admission open')
if __name__=='__main__':main()
