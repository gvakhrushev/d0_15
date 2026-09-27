import numpy as np, sympy as sp, json
exec(compile(open('a4d_fugu_p1p2_check.py').read(),'base','exec'))
zs_=[z[0],z[1],z[2],z[3]]; Cl=sp.lambdify(zs_,HAQ,'numpy')
orb=np.load('orbits_ids.npy'); rt=lambda i:[1,1j,-1,-1j][i%4]
def rk(M,tol=1e-8):
 s=np.linalg.svd(M,compute_uv=False); return int((s>tol*max(1.,s.max())).sum()) if M.size else 0
def CV(v): return np.array(Cl(*[complex(x) for x in v]),complex)
out=["=== СВОДНАЯ ТАБЛИЦА АНОМАЛЬНОГО ОПЕРАТОРА (все 9 орбит) ==="]
out.append("orb  ids          real-scaling-rank  phase-rank  maxSV(real)  maxSV(phase)  absorbed?")
tab=[]
for n in range(9):
 v=[rt(int(orb[n,k])) for k in range(4)]
 C0=CV(v); U,s,Vh=np.linalg.svd(C0); r=(s>1e-9*s.max()).sum(); q=Vh[r:].conj().T[:,0]; q/=np.linalg.norm(q)
 A=np.array(np.load(f'num_{n}.npz')['A'],complex)
 Ua,sa,_=np.linalg.svd(A); ra=(sa>1e-9*sa.max()).sum(); L=Ua[:,ra:]
 h=1e-6; Rr=[]; Rp=[]
 for j in range(4):
  vp=list(v); vm=list(v); vp[j]=v[j]*(1+h); vm[j]=v[j]*(1-h)
  wr=((CV(vp)-CV(vm))/(2*h))@q; Rr.append(L@(L.conj().T@wr))
  vp=list(v); vm=list(v); vp[j]=v[j]*np.exp(1j*h); vm[j]=v[j]*np.exp(-1j*h)
  wp=((CV(vp)-CV(vm))/(2*h))@q; Rp.append(L@(L.conj().T@wp))
 Mr=np.column_stack(Rr); Mp=np.column_stack(Rp)
 rr=rk(Mr); rp=rk(Mp); sr=np.linalg.svd(Mr,compute_uv=False)[0]; spv=np.linalg.svd(Mp,compute_uv=False)[0]
 tab.append((rr,rp))
 out.append(f"{n}  {str(tuple(int(x) for x in orb[n])):>11}:   {rr:>2}                {rp:>2}         {sr:.4f}       {spv:.4f}       {'YES' if rr==0 else 'no'}")
out.append("")
out.append("аномальный ранг (real-scaling) по орбитам: "+str([t[0] for t in tab]))
out.append("аномальный ранг (phase)        по орбитам: "+str([t[1] for t in tab]))
out.append("ПОЛНОЕ СОВПАДЕНИЕ ДВУХ НЕЗАВИСИМЫХ СЕМЕЙСТВ: " + str([t[0] for t in tab]==[t[1] for t in tab]))
open('consolidate.txt','w').write("\n".join(out)); print("\n".join(out))
