import numpy as np, sympy as sp, contextlib, io
from fractions import Fraction
with contextlib.redirect_stdout(io.StringIO()):
 exec(compile(open('a4d_fugu_p1p2_check.py').read(),'base','exec'))
zs_=[z[0],z[1],z[2],z[3]]; Cl=sp.lambdify(zs_,HAQ,'numpy')
orb=np.load('orbits_ids.npy'); rt=lambda i:[1,1j,-1,-1j][i%4]
def rk(M,tol=1e-8):
 s=np.linalg.svd(M,compute_uv=False); return int((s>tol*max(1.,s.max())).sum())
def CV(v): return np.array(Cl(*[complex(x) for x in v]),complex)

rows=[]
for n in range(9):
 v=[rt(int(orb[n,k])) for k in range(4)]; C0=CV(v)
 U,s,Vh=np.linalg.svd(C0); r=(s>1e-9*s.max()).sum(); q=Vh[r:].conj().T[:,0]; q/=np.linalg.norm(q)
 A=np.array(np.load(f'num_{n}.npz')['A'],complex); Ua,sa,_=np.linalg.svd(A); ra=(sa>1e-9*sa.max()).sum(); L=Ua[:,ra:]
 h=1e-5; R=[]
 for j in range(4):
  vp=list(v); vm=list(v); vp[j]*=(1+h); vm[j]*=(1-h)
  w=((CV(vp)-CV(vm))/(2*h))@q; R.append(L@(L.conj().T@w))
 M=np.column_stack(R); sv=np.linalg.svd(M,compute_uv=False)
 sv2=[float(x**2) for x in sv if x>1e-7]
 rows.append((tuple(int(x) for x in orb[n]),rk(M),sv2))

print("orb               a_rank   squared singular values (exact-ish)")
for ids,rr,sv2 in rows:
 fr=[str(Fraction(x).limit_denominator(200)) for x in sv2]
 print(f"{str(ids):>13}   {rr:>2}    {[round(x,6) for x in sv2]}   -> {fr}")
ar=[r for _,r,_ in rows]
print("\nanomaly rank census:",ar)
print("palindromic (n <-> 8-n):",ar==ar[::-1])
