import numpy as np, sympy as sp
# suppress base prints by redirecting
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
 exec(compile(open('a4d_fugu_p1p2_check.py').read(),'base','exec'))
zs_=[z[0],z[1],z[2],z[3]]
Cl=sp.lambdify(zs_,HAQ,'numpy')
orb=np.load('orbits_ids.npy'); rt=lambda i:[1,1j,-1,-1j][i%4]
def rk(M,tol=1e-8):
 s=np.linalg.svd(M,compute_uv=False); return int((s>tol*max(1.,s.max())).sum())
def CV(v): return np.array(Cl(*[complex(x) for x in v]),complex)
out=[]
out.append('=== PHASE-TANGENT QUOTIENT: z_j -> z_j exp(i t) ===')
out.append('orb ids | rank residual map | singular values | kernel directions in character space')
for n in range(9):
 v=[rt(int(orb[n,k])) for k in range(4)]; C0=CV(v)
 U,s,Vh=np.linalg.svd(C0); r=(s>1e-9*s.max()).sum(); q=Vh[r:].conj().T[:,0]; q/=np.linalg.norm(q)
 A=np.array(np.load(f'num_{n}.npz')['A'],complex); Ua,sa,_=np.linalg.svd(A); ra=(sa>1e-9*sa.max()).sum(); L=Ua[:,ra:]
 h=1e-5; R=[]
 for j in range(4):
  vp=list(v); vm=list(v); vp[j]*=np.exp(1j*h); vm[j]*=np.exp(-1j*h)
  w=((CV(vp)-CV(vm))/(2*h))@q; R.append(L@(L.conj().T@w))
 M=np.column_stack(R); um,sm,vhm=np.linalg.svd(M,full_matrices=True); rr=rk(M); ker=vhm[rr:,:]
 # phase tangent common direction and alternating sum responses
 common=np.linalg.norm(M@np.ones(4)); alt=np.linalg.norm(M@np.array([1,-1,1,-1]))
 out.append(f'{n} {tuple(int(x) for x in orb[n])} | rank {rr} | sv {[round(float(x),6) for x in sm]} | ker {[np.round(x,3).tolist() for x in ker]} | common {common:.5g} alt {alt:.5g}')
open('phase_residual.txt','w').write('\n'.join(out)); print('\n'.join(out))
