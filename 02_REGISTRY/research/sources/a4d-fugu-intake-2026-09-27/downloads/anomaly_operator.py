import numpy as np, sympy as sp, contextlib, io, json
with contextlib.redirect_stdout(io.StringIO()):
 exec(compile(open('a4d_fugu_p1p2_check.py').read(),'base','exec'))
zs_=[z[0],z[1],z[2],z[3]]; Cl=sp.lambdify(zs_,HAQ,'numpy')
orb=np.load('orbits_ids.npy'); rt=lambda i:[1,1j,-1,-1j][i%4]
def rk(M,tol=1e-8):
 s=np.linalg.svd(M,compute_uv=False); return int((s>tol*max(1.,s.max())).sum())
def CV(v): return np.array(Cl(*[complex(x) for x in v]),complex)

# Two tangent families of the character z_j: radial (scale) and phase (rotate by quarter turn).
# Build the germ->anomaly operator G (4 character-directions x residual), for BOTH families.
res={}
for fam in ('radial','phase'):
 row=[]
 for n in range(9):
  v=[rt(int(orb[n,k])) for k in range(4)]; C0=CV(v)
  U,s,Vh=np.linalg.svd(C0); r=(s>1e-9*s.max()).sum(); q=Vh[r:].conj().T[:,0]; q/=np.linalg.norm(q)
  A=np.array(np.load(f'num_{n}.npz')['A'],complex); Ua,sa,_=np.linalg.svd(A); ra=(sa>1e-9*sa.max()).sum(); L=Ua[:,ra:]
  h=1e-5; R=[]
  for j in range(4):
   vp=list(v); vm=list(v)
   if fam=='radial': vp[j]*=(1+h); vm[j]*=(1-h)
   else: vp[j]*=np.exp(1j*h); vm[j]*=np.exp(-1j*h)
   w=((CV(vp)-CV(vm))/(2*h))@q; R.append(L@(L.conj().T@w))
  M=np.column_stack(R); sv=np.linalg.svd(M,compute_uv=False)
  row.append((tuple(int(x) for x in orb[n]),rk(M),[round(float(x),5) for x in sv]))
 res[fam]=row

out=[]
for fam in ('radial','phase'):
 out.append(f'=== family={fam} ===')
 for ids,r,sv in res[fam]:
  out.append(f'  {str(ids):>13}: rank={r}  sv={sv}')
open('anomaly_operator.txt','w').write('\n'.join(out)); print('\n'.join(out))
# cross-family selection matrix: does radial rank + phase rank track owned rank A_real deficiency?
print()
print('orb               rankA_real  radial_rank phase_rank')
AR=[44,44,40,40,32,40,40,44,44]
for i,(ids,r,sv) in enumerate(res['radial']):
 print(f'{str(ids):>13}   {AR[i]:>3}        {r:>2}          {res["phase"][i][1]:>2}')
