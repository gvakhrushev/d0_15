import numpy as np, sympy as sp, json
exec(compile(open('a4d_fugu_p1p2_check.py').read(),'base','exec'))
zs_=[z[0],z[1],z[2],z[3]]
Cl=sp.lambdify(zs_,HAQ,'numpy'); Al=sp.lambdify(zs_,HAB,'numpy')
orb=np.load('orbits_ids.npy'); rtmap=lambda i:[1,1j,-1,-1j][i%4]
def rk(M,tol=1e-8):
    if M.size==0: return 0
    s=np.linalg.svd(M,compute_uv=False); return int((s>tol*max(1.0,s.max())).sum())
def Cval(vals): return np.array(Cl(*[complex(x) for x in vals]),complex)
def Aval(vals): return np.array(Al(*[complex(x) for x in vals]),complex)
def tang(n,j,h=1e-6):
    v=[rtmap(int(orb[n,k])) for k in range(4)]
    vp=list(v); vm=list(v); vp[j]=v[j]*(1+h); vm[j]=v[j]*(1-h)
    return (Cval(vp)-Cval(vm))/(2*h)

out=[]
out.append("=== GERM->ANOMALY OPERATOR (metric-only germ -> unabsorbed connection part) ===")
out.append(" orb  ids            dimkerA†  rankMG  singular values of residual family r_j")
svstore={}
for n in range(9):
    v0=[rtmap(int(orb[n,k])) for k in range(4)]
    A=Aval(v0); C0=Cval(v0)
    Ua,sa,_=np.linalg.svd(A); rA=(sa>1e-9*sa.max()).sum(); L=Ua[:,rA:]
    U,s,Vh=np.linalg.svd(C0); r=(s>1e-9*s.max()).sum(); q=Vh[r:].conj().T[:,0]; q/=np.linalg.norm(q)
    R=[L@(L.conj().T@(tang(n,j)@q)) for j in range(4)]
    MG=np.column_stack(R); sv=np.linalg.svd(MG,compute_uv=False)
    key=str(tuple(int(x) for x in orb[n])); svstore[key]=list(sv)
    out.append(f"  {n}  {key:>13}:  {L.shape[1]:>3}     {rk(MG):>2}   {['%.4f'%x for x in sv]}")
json.dump(svstore, open('germ_anomaly.json','w'), indent=1)
out.append("")
# second part: anomaly line L_anom = top left-singular of MG; compare against metric-only germ plane and F4 kernel
out.append("=== ANOMALY LINE vs OWNED OBJECTS ===")
out.append(" orb  ids            ||P_anom q|| (proj of germ back onto anomaly line)  F4-ker overlap")
F4ov=[]
for n in range(9):
    v0=[rtmap(int(orb[n,k])) for k in range(4)]
    A=Aval(v0); C0=Cval(v0)
    F4=A+1j*(C0@C0.conj().T)
    Uf,sf,_=np.linalg.svd(F4); rF=(sf>1e-9*sf.max()).sum(); KF=Uf[:,rF:]
    # anomaly line from svstore? recompute MG quickly
    Ua,sa,_=np.linalg.svd(A); rA=(sa>1e-9*sa.max()).sum(); L=Ua[:,rA:]
    U,s,Vh=np.linalg.svd(C0); r=(s>1e-9*s.max()).sum(); q=Vh[r:].conj().T[:,0]; q/=np.linalg.norm(q)
    R=[L@(L.conj().T@(tang(n,j)@q)) for j in range(4)]
    MG=np.column_stack(R)
    Um,sm,_=np.linalg.svd(MG); anom=Um[:,0]
    ov=float(np.linalg.norm(anom.conj()@(KF@ (KF.conj().T@anom)))**2) if KF.shape[1]>0 else 0.0
    # overlap of anomaly line with ker A† subspace occupied by germ tangent
    F4ov.append(ov)
    out.append(f"  {n}  {str(tuple(int(x) for x in orb[n])):>13}:  dim ker F4={KF.shape[1]:>2}  overlap(anomaly, ker F4)={ov:.4f}")
out.append("")
out.append("F4 overlap by orbit: "+str([round(x,4) for x in F4ov]))
open('deep_analysis.txt','w').write("\n".join(out))
print("\n".join(out))
print("DONE")
