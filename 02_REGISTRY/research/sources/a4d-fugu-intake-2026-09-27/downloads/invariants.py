import numpy as np, sympy as sp, contextlib, io, json
with contextlib.redirect_stdout(io.StringIO()):
 exec(compile(open('a4d_fugu_p1p2_check.py').read(),'base','exec'))
zs_=[z[0],z[1],z[2],z[3]]; Cl=sp.lambdify(zs_,HAQ,'numpy')
orb=np.load('orbits_ids.npy'); rt=lambda i:[1,1j,-1,-1j][i%4]
def rk(M,tol=1e-8):
 s=np.linalg.svd(M,compute_uv=False); return int((s>tol*max(1.,s.max())).sum()) if M.size else 0
def CV(v): return np.array(Cl(*[complex(x) for x in v]),complex)

out=["=== [I] ЯДРО ОПЕРАТОРА G В ПРОСТРАНСТВЕ ХАРАКТЕРОВ (какие комбинации наклонов поглощены) ==="]
out.append("orb  ids          rankG  dimkerG  kerG-направления (в базисе сдвигов z0..z3)")
spec=[]
for n in range(9):
 v=[rt(int(orb[n,k])) for k in range(4)]; C0=CV(v)
 U,s,Vh=np.linalg.svd(C0); r=(s>1e-9*s.max()).sum(); q=Vh[r:].conj().T[:,0]; q/=np.linalg.norm(q)
 A=np.array(np.load(f'num_{n}.npz')['A'],complex); Ua,sa,_=np.linalg.svd(A); ra=(sa>1e-9*sa.max()).sum(); L=Ua[:,ra:]
 h=1e-6; R=[]
 for j in range(4):
  vp=list(v); vm=list(v); vp[j]=v[j]*(1+h); vm[j]=v[j]*(1-h)
  R.append(L@(L.conj().T@((CV(vp)-CV(vm))/(2*h))@q))
 M=np.column_stack(R); um,sm,vhm=np.linalg.svd(M,full_matrices=True); rr=rk(M); ker=vhm[rr:,:]
 spec.append(rr)
 out.append(f"{n}  {str(tuple(int(x) for x in orb[n])):>11}:   {rr:>2}      {4-rr:>2}     {[np.round(k,3).tolist() for k in ker] if rr<4 else '—'}")
out.append("")
out.append("спектр rankG: "+str(spec)+"   сумма="+str(sum(spec)))
# check relation: rankG vs number of distinct characters
out.append("")
out.append("=== [II] СВЯЗЬ rankG С СТРУКТУРОЙ ОРБИТЫ ===")
for n in range(9):
 ch=[rt(int(orb[n,k])) for k in range(4)]
 distinct=len(set(ch))
 # conj pairs
 mult={}
 for c in ch: mult[c]=mult.get(c,0)+1
 rep=len([c for c in mult if c in (1j,-1j)])
 out.append(f"{n} {str(tuple(int(x) for x in orb[n])):>11}: distinct={distinct} mult={ {str(k):v for k,v in mult.items()} } rankG={spec[n]}")
open('invariants.txt','w').write("\n".join(out)); print("\n".join(out))
