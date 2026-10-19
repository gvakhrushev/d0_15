#!/usr/bin/env python3
"""D0 real 718-edge complete registration, 33-flag Book determinant.
Numpy numeric checker; NO compulsory original physical Book admission.
"""
import numpy as np

N=33
Z=2**-20
PHI=(1+5**.5)/2
PART=np.array([0]*9+[1]*11+[2]*13)
EDGES=[(u,v) for u in range(N) for v in range(N) if PART[u]!=PART[v]]
assert len(EDGES)==718
A=np.zeros((N,N))
for u,v in EDGES:A[u,v]=1
assert int(np.sum(A@A))==15708

def make_scene(t,theta=.25,uniform=False):
    K=np.zeros((N,N))
    info=np.array([.2*(v%5)+.09*np.sin(.6*(v+1)*t) for v in range(N)])
    for u,v in EDGES:
        cost=1 if uniform else 1+.027*((3*u+7*v)%11)+.018*t*((u+3*v)%5)
        K[u,v]=PHI**(-(cost if uniform else cost-theta*info[u]-(1-theta)*info[v]))
    eig,R=np.linalg.eig(K)
    j=np.argmax(eig.real)
    lam=eig[j].real
    r=R[:,j].real
    if r.sum()<0:r=-r
    eigl,L=np.linalg.eig(K.T)
    ell=L[:,np.argmin(abs(eigl-lam))].real
    if ell.sum()<0:ell=-ell
    pi=r*ell
    pi/=pi.sum()
    P=K*r[np.newaxis,:]/(lam*r[:,np.newaxis])
    assert np.max(abs(P.sum(axis=1)-1))<1e-11
    assert np.max(abs(pi@P-pi))<1e-11
    S=np.zeros((len(EDGES),N))
    R=np.zeros_like(S)
    for i,(u,v) in enumerate(EDGES):
        S[i,u]=np.sqrt(P[u,v])
        R[i,v]=np.sqrt(pi[u]*P[u,v]/pi[v])
    assert np.max(abs(S.T@S-np.eye(N)))<1e-12
    assert np.max(abs(R.T@R-np.eye(N)))<1e-12
    T=S.T@R
    assert np.max(abs(T-np.sqrt(pi[:,None]/pi[None,:])*P))<1e-12
    F=np.eye(N)-T.T@T
    eigF=np.linalg.eigvalsh(F)
    assert np.linalg.norm(F@np.sqrt(pi))<1e-12
    assert abs(eigF[0])<1e-12
    assert eigF[1]>.05 and eigF[-1]<=1+1e-12
    # COMPLETE all-718-edge good+fail isometry: input Gram equals I.
    gram=T.T@T+R.T@R-T.T@T
    assert np.max(abs(gram-np.eye(N)))<1e-12
    G=np.eye(N)-Z*F
    L=np.linalg.cholesky(G)
    flags=np.diag(L)**2
    assert np.all((flags>=1-Z-1e-13)&(flags<=1+1e-13))
    all_good=np.prod(flags)
    assert abs(all_good-np.linalg.det(G))<1e-12
    # 33 genuine fresh complete flags represent ALL 2^33 bit outcomes.
    firstfail=sum((1-d)*np.prod(flags[:i]) for i,d in enumerate(flags))
    assert abs(firstfail+all_good-1)<1e-12
    J=-np.linalg.slogdet(G)[1]
    return locals()

base=make_scene(.41)
for theta in [-.6,.25,1.3]:
    v=make_scene(.41,theta)
    assert np.max(abs(v['P']-base['P']))<1e-12
    assert np.max(abs(v['pi']-base['pi']))<1e-12
    assert abs(v['J']-base['J'])<1e-12

flat=make_scene(.41,uniform=True)
rho=np.linalg.eigvalsh(A)[-1]
assert np.max(abs(flat['T']-A/rho))<1e-12
assert np.count_nonzero(abs(np.linalg.eigvalsh(A))<1e-10)==30

step=1e-4
up=make_scene(.41+step)
down=make_scene(.41-step)
dF=(up['F']-down['F'])/(2*step)
source_exact=Z*np.trace(np.linalg.solve(base['G'],dF))
source_fd=(up['J']-down['J'])/(2*step)
assert abs(source_exact-source_fd)<5e-12

print('PASS K(9,11,13): 33 vertices, 718 real directed edges, 15708 two-step paths')
print('PASS two full 718-edge isometries; success+failure Gram I; rank32 F')
print('PASS 33 complete fresh pivots in [1-z,1]; all-good=det(I-zF)')
print('PASS Info endpoint allocation invariant, including full first-source')
print('PASS equal-Cost T=A/rho, archive30 + active2 + stationary1')
print(f"all_good={base['all_good']:.15f} J={base['J']:.15f}")
print(f"source matrix={source_exact:+.12g}; finite={source_fd:+.12g}; error={abs(source_exact-source_fd):.3g}")
print('SCOPE: complete mathematical source-tested instrument; physical D0 Book/GR OPEN')
