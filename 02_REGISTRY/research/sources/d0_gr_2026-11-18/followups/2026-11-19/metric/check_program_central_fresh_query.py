#!/usr/bin/env python3
"""Finite-dimensional checks, not a physical realization of the hypotheses."""
import json
from pathlib import Path
import numpy as np

p=(5**0.5-1)/2
a0=p**3+p**5
a1=2*p**5
af=0.17                       # declared toy failure weight, NOT a measured tariff
q=np.array([[.20,.60],[.40,.75],[.30,.55]])
dq=np.array([[.07,-.03],[-.04,.05],[.02,.06]])
gamma=np.array([[.82,.91],[.87,.79],[.90,.86]])
I=np.eye(4,dtype=complex)
rng=np.random.default_rng(291119)

def unitary():
    x=rng.standard_normal((2,2))+1j*rng.standard_normal((2,2))
    u,r=np.linalg.qr(x)
    return u @ np.diag(np.diag(r)/abs(np.diag(r))).conj()

# P_k is the first tensor factor. Every branch acts by a separate unitary
# on the memory, so the same quantum memory is reused and becomes correlated.
us=[[[unitary() for k in range(2)] for branch in range(3)] for i in range(3)]
def block(mats):
    out=np.zeros((4,4),dtype=complex)
    out[:2,:2]=mats[0]
    out[2:,2:]=mats[1]
    return out

def diagprogram(x): return block([x[0]*np.eye(2),x[1]*np.eye(2)])
def maps(theta,weighted=True):
    result=[]
    for i in range(3):
        qi=q[i]+theta*dq[i]
        vals=np.stack([gamma[i]*(1-qi),gamma[i]*qi,1-gamma[i]])
        if weighted: vals=vals*np.array([a0,a1,af])[:,None]
        result.append([block([np.sqrt(vals[t,k])*us[i][t][k] for k in range(2)]) for t in range(3)])
    return result

def apply(ks,rho): return sum(K@rho@K.conj().T for K in ks)
def effect(ks): return sum(K.conj().T@K for K in ks)
def full(ms,rho):
    for ks in ms: rho=apply(ks,rho)
    return rho

def zvals(theta):
    v=q+theta*dq
    return gamma*(a0*(1-v)+a1*v)+(1-gamma)*af

psi=np.array([1,0,0,1],dtype=complex)/np.sqrt(2)
rho=np.outer(psi,psi.conj())
ms=maps(0)
z=zvals(0)
Z=diagprogram(np.prod(z,axis=0))
Zhalf=diagprogram(np.sqrt(np.prod(z,axis=0)))
Zs=[diagprogram(v) for v in z]
assert max(np.linalg.norm(effect(x)-I) for x in maps(0,False))<1e-12
assert max(np.linalg.norm(effect(x)-zz) for x,zz in zip(ms,Zs))<1e-12
normmaps=[[K@diagprogram(1/np.sqrt(z[i])) for K in ks] for i,ks in enumerate(ms)]
assert max(np.linalg.norm(effect(x)-I) for x in normmaps)<1e-12
lhs=full(ms,rho)
rhs=full(normmaps,Zhalf@rho@Zhalf)
assert np.linalg.norm(lhs-rhs)<1e-12
mass=np.trace(lhs).real
assert abs(mass-np.trace(Z@rho).real)<1e-12
assert abs((Zhalf@rho@Zhalf)[0,3])>1e-5
weights=np.array([.5,.5])
wrong=np.prod(z@weights)
correct=np.prod(z,axis=0)@weights
assert abs(correct-wrong)>1e-8

# Compare two fresh queries with the same retained, unobserved program.
qtoy=np.array([.2,.8])
cov=(qtoy*qtoy)@weights-(qtoy@weights)**2
assert abs(cov-.09)<1e-12

# Fixed input: derivative of normalized central tilt has no inverse product.
def tilt(theta):
    zz=np.prod(zvals(theta),axis=0)
    R=diagprogram(np.sqrt(zz))
    r=R@rho@R
    return r/np.trace(r).real
r=tilt(0)
score=np.sum(gamma*(a1-a0)*dq/z,axis=0)
A=diagprogram(score)
center=A-np.trace(A@r).real*I
analytic=(center@r+r@center)/2
h=1e-6
numeric=(tilt(h)-tilt(-h))/(2*h)
error=np.linalg.norm(numeric-analytic)
assert error<1e-9
singular=np.linalg.svd(analytic,compute_uv=False)
norm1=float(sum(singular))
bound=float(np.sum(np.ptp(gamma*(a1-a0)*dq/z,axis=1)))
assert norm1<=bound+1e-12

# A separately varied program preparation contributes its own score.
dp=np.array([.12,-.12])
def total_weight(theta):
    return (weights+theta*dp) @ np.prod(zvals(theta),axis=0)
post=weights*np.prod(z,axis=0)/correct
score_total=float(post@(dp/weights+score))
score_numeric=float((np.log(total_weight(h))-np.log(total_weight(-h)))/(2*h))
assert abs(score_total-score_numeric)<1e-9
assert abs(float(post@(dp/weights)))>1e-4

# Crossing effects are a positive Gram matrix, but need not preserve the
# magnitude of program coherence. Both recorded outcomes are traced out.
u=np.array([[p,p*p],[p*p,p]])
gram=np.sqrt(u)@np.sqrt(u).T
eig=np.linalg.eigvalsh(gram)
coherence=2*p**1.5
assert min(eig)>-1e-14
assert np.allclose(np.diag(gram),1)
assert abs(gram[0,1]-coherence)<1e-14 and coherence<1
rho_program=np.ones((2,2),dtype=complex)/2
repeated=rho_program.copy()
for _ in range(12): repeated=gram*repeated
assert abs(repeated[0,1]-0.5*coherence**12)<1e-14

result={
 'status':'conditional central-instrument algebra; toy example only',
 'actual_fresh_reader_kappa':(a0-a1)/a0,
 'target_kappa':1/5**0.5,
 'toy_failure_weight_declared_not_physical':af,
 'input_program_memory_entangled':True,
 'unweighted_instruments_trace_preserving':True,
 'weighted_effect_is_program_central':True,
 'normalized_instruments_trace_preserving':True,
 'factorization_error_frobenius':float(np.linalg.norm(lhs-rhs)),
 'correct_shared_program_weight':correct,
 'incorrect_product_of_means':wrong,
 'retained_cross_program_coherence_magnitude':float(abs((Zhalf@rho@Zhalf)[0,3])),
 'two_query_hidden_program_covariance':cov,
 'normalized_tilt_derivative_error_frobenius':float(error),
 'normalized_tilt_derivative_trace_norm':norm1,
 'linear_score_range_bound':bound,
 'moving_program_preparation_score':float(post@(dp/weights)),
 'total_log_weight_score_error':abs(score_total-score_numeric),
 'cross_branch_gram_eigenvalues':eig.tolist(),
 'single_query_off_diagonal_multiplier':coherence,
 'twelve_query_off_diagonal_multiplier':coherence**12,
 'formal_inverse_is_a_free_physical_filter':False,
 'physical_book_cost_information_bound':False,
 'physical_full_factory_and_query_centrality_verified':False,
 'GR_closed':False,
}
assert abs(result['actual_fresh_reader_kappa']-result['target_kappa'])<1e-12
out=Path(__file__).with_name('program_central_fresh_query_result.json')
out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result,indent=2,ensure_ascii=False))
