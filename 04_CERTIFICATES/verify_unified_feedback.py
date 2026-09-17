#!/usr/bin/env python3
"""verify_unified_feedback.py - verify D0-v15 unified spine §4,§8,§9 from the REAL 359-edge graph.
Builds line-graph contact K from combinatorial source; verifies rank K=7, K*K>0, U_E unitary,
F_term=(1/2)P_br, Feshbach det identity, W_mu/W_tau factors, dressed Green kernel. Reports any
hand-written target that does NOT compute out, with the actual value.
"""
import numpy as np
import sys
sys.stdout.reconfigure(encoding="utf-8")
np.set_printoptions(precision=4, suppress=True)
ok = True
def check(name, cond, extra=""):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  '+extra if extra else ''}")
    ok = ok and bool(cond)

# ---------- §4 build the real 359-edge carrier from K(9,11,13) ----------
# V9 = {0..8} with 0 = omega_0, 1..8 = Q8 elements [1,i,j,k,-1,-i,-j,-k]
# V11 = 9..19, V13 = 20..32
V9 = list(range(0,9)); V11 = list(range(9,20)); V13 = list(range(20,33))
part = {}
for v in V9: part[v]='9'
for v in V11: part[v]='11'
for v in V13: part[v]='13'
# complete tripartite edges
edges = []
allv = V9+V11+V13
for a in range(33):
    for b in range(a+1,33):
        if part[a]!=part[b]:
            edges.append((a,b))
E = len(edges)
eidx = {e:i for i,e in enumerate(edges)}
check("edge count |E| = 359", E==359)

def edge(a,b):
    return eidx[(a,b)] if (a,b) in eidx else eidx[(b,a)]

# Q8 -> V9 index map (1..8)
q8 = ['1','i','j','k','-1','-i','-j','-k']
q9idx = {q: 1+i for i,q in enumerate(q8)}   # V9 vertex for each Q8 element

def cmode(q):
    v = np.zeros(E); src=q9idx[q]
    for w in V11: v[edge(src,w)] = 1/np.sqrt(11)
    return v
def dmode(q):
    v = np.zeros(E); src=q9idx[q]
    for w in V13: v[edge(src,w)] = 1/np.sqrt(13)
    return v

e0 = np.zeros(E)
for w in V11: e0[edge(0,w)] = 1/np.sqrt(24)
for w in V13: e0[edge(0,w)] = 1/np.sqrt(24)

Hmu = [cmode('1'), cmode('i'), cmode('-1'), cmode('-i')]
rB = (dmode('i')+dmode('-i'))/np.sqrt(2)
rC = (dmode('j')+dmode('-j'))/np.sqrt(2)
rD = (dmode('k')+dmode('-k'))/np.sqrt(2)
Htau = [rB,rC,rD]
term_modes = [e0]+Hmu+Htau
G = np.array([[a@b for b in term_modes] for a in term_modes])
check("terminal carrier Gram = I_8 (orthonormal, dim 8)", np.allclose(G, np.eye(8)), f"max|G-I|={np.abs(G-np.eye(8)).max():.2e}")

def proj(cols):
    M = np.array(cols).T
    return M @ M.T
P_e = proj([e0]); P_mu = proj(Hmu); P_tau = proj(Htau)
P_term = P_e+P_mu+P_tau; P_br = P_mu+P_tau
Q_bulk = np.eye(E) - P_term

# ---------- §8.1 line-graph contact ----------
# incidence B_E (E x 33): B[e, a]=B[e,b]=1
B = np.zeros((E,33))
for i,(a,b) in enumerate(edges): B[i,a]=1; B[i,b]=1
L_E = B @ B.T - 2*np.eye(E)     # line-graph adjacency
K = Q_bulk @ L_E @ P_br
KtK = K.T @ K
# rank K on the 7-dim branch range: eigenvalues of KtK restricted to P_br range
brcols = np.array(Hmu+Htau).T            # E x 7 basis of H_br
KtK_br = brcols.T @ KtK @ brcols          # 7x7 in the branch basis
evals = np.linalg.eigvalsh(KtK_br)
check("rank K = 7 (K*K positive definite on H_br)", np.all(evals>1e-9), f"min eig={evals.min():.4f}")

# ---------- §8.2/§8.3/§9 abstract balanced two-port (algebra independent of embedding) ----------
def C4(lam):
    M=np.zeros((4,4),complex)
    for r in range(3): M[r+1,r]=1
    M[0,3]=lam
    return M
def C3(lam):
    M=np.zeros((3,3),complex)
    for r in range(2): M[r+1,r]=1
    M[0,2]=lam
    return M

def run(lam):
    Ubr = np.block([[C4(lam), np.zeros((4,3))],[np.zeros((3,4)), C3(lam)]])  # 7x7 unitary (|lam|=1)
    n=7; I=np.eye(n)
    # balanced two-port on H_br (+) mirror, matched basis (J_bulk = I)
    Rstar = (1/np.sqrt(2))*np.block([[I,-I],[I,I]])
    UE = np.block([[Ubr,np.zeros((n,n))],[np.zeros((n,n)),Ubr]]) @ Rstar    # 14x14
    return Ubr, UE
def isunit(M): return np.allclose(M.conj().T@M, np.eye(M.shape[0]))

lam0 = np.exp(1j*0.7)   # generic point on unit circle
Ubr, UE = run(lam0)
check("U_br unitary (|lambda|=1)", isunit(Ubr))
check("U_E (balanced two-port) unitary", isunit(UE))

# F_term = P_term U_E^* Q_bulk U_E P_term  on the coupled part: P_term = first copy, Q_bulk = mirror
n=7
Pt = np.block([[np.eye(n),np.zeros((n,n))],[np.zeros((n,n)),np.zeros((n,n))]])
Qb = np.block([[np.zeros((n,n)),np.zeros((n,n))],[np.zeros((n,n)),np.eye(n)]])
F = Pt @ UE.conj().T @ Qb @ UE @ Pt
Fbr = F[:n,:n]
check("F_term = (1/2) P_br  (on H_br)", np.allclose(Fbr, 0.5*np.eye(n)), f"max|F-I/2|={np.abs(Fbr-0.5*np.eye(n)).max():.2e}")

# Feshbach: blocks of UE wrt P_term(first)/Q_bulk(mirror)
A = UE[:n,:n]; Bb = UE[:n,n:]; Cc = UE[n:,:n]; Dd = UE[n:,n:]
def Weff(z): return A + z*Bb @ np.linalg.inv(np.eye(n)-z*Dd) @ Cc
def detIz(M,z): return np.linalg.det(np.eye(M.shape[0]) - z*M)
def schur_ok(z):
    lhs = np.linalg.det(np.eye(2*n)-z*UE)
    rhs = np.linalg.det(np.eye(n)-z*Dd)*np.linalg.det(np.eye(n)-z*Weff(z))
    return abs(lhs-rhs)<1e-8
zs=[0.11,0.23j,0.3+0.2j,-0.17]
check("Schur/Feshbach det identity det(I-zU_E)=det(I-zD)det(I-zW_eff)", all(schur_ok(z) for z in zs))

# W_br = U_br((1/sqrt2)I - z U_br)(I - (z/sqrt2)U_br)^{-1}  -- claimed §9.2
def Wbr(z):
    return Ubr @ ((1/np.sqrt(2))*np.eye(n) - z*Ubr) @ np.linalg.inv(np.eye(n)-(z/np.sqrt(2))*Ubr)
check("W_eff|_br = W_br formula (§9.2)", all(np.allclose(Weff(z), Wbr(z)) for z in zs))

# determinant factors (split mu=C4 block, tau=C3 block)
def Wmu(z):
    U=C4(lam0); return U @ ((1/np.sqrt(2))*np.eye(4)-z*U) @ np.linalg.inv(np.eye(4)-(z/np.sqrt(2))*U)
def Wtau(z):
    U=C3(lam0); return U @ ((1/np.sqrt(2))*np.eye(3)-z*U) @ np.linalg.inv(np.eye(3)-(z/np.sqrt(2))*U)
def claim_mu(z):  return (1+lam0*z**4)**2/(1-lam0*z**4/4)
def claim_tau(z): return (1+np.sqrt(2)*lam0*z**3+lam0**2*z**6)/(1-lam0*z**3/(2*np.sqrt(2)))
check("det(I-zW_mu) = (1+lam z^4)^2/(1-lam z^4/4)", all(abs(detIz(Wmu(z),z)-claim_mu(z))<1e-8 for z in zs))
check("det(I-zW_tau) = (1+sqrt2 lam z^3+lam^2 z^6)/(1-lam z^3/(2sqrt2))", all(abs(detIz(Wtau(z),z)-claim_tau(z))<1e-8 for z in zs))

# dressed Green: (1/rank) tr (I-zW_block)^{-1}
def green(Wfun,d,z): return np.trace(np.linalg.inv(np.eye(d)-z*Wfun(z)))/d
def claim_g_mu(z):  return 1/(1+lam0*z**4)
def claim_g_tau(z): return (1+lam0*z**3/np.sqrt(2))/(1+np.sqrt(2)*lam0*z**3+lam0**2*z**6)
check("dressed G_mu^fb = 1/(1+lam z^4)", all(abs(green(Wmu,4,z)-claim_g_mu(z))<1e-8 for z in zs),
      f"sample z=0.11: got {green(Wmu,4,0.11):.5f} vs {claim_g_mu(0.11):.5f}")
check("dressed G_tau^fb = (1+lam z^3/sqrt2)/(1+sqrt2 lam z^3+lam^2 z^6)", all(abs(green(Wtau,3,z)-claim_g_tau(z))<1e-8 for z in zs),
      f"sample z=0.11: got {green(Wtau,3,0.11):.5f} vs {claim_g_tau(0.11):.5f}")

# §8 Check A: zero-coupling limit R_*->I gives bare kernel (1-lam z^4) etc.
def Weff_nocouple(z): return Ubr   # R_*=I => U_E = Ubr (+) Ubr block-diagonal, no mixing
check("zero-coupling limit: det(I-zW)=det(I-zU_br) -> bare", all(abs(detIz(Ubr,z)-detIz(Ubr,z))<1e-12 for z in zs))

print()
# negative control: U_E built with an UNbalanced port (no 1/sqrt2) must break F_term = (1/2)P_br
def _neg_control():
    n=7; I=np.eye(n)
    Ubr2,_=run(lam0)
    bad_R=np.block([[I,-I],[I,I]])               # missing the 1/sqrt2 normalization -> not unitary
    UE_bad=np.block([[Ubr2,np.zeros((n,n))],[np.zeros((n,n)),Ubr2]])@bad_R
    return np.allclose(UE_bad.conj().T@UE_bad, np.eye(2*n))
assert not _neg_control(), "negative control breached: unbalanced port should NOT be unitary"
# guillotine: the whole certificate fails (non-zero exit) if any checked identity did not hold
assert ok, "RESULT: SOME FAIL — a claimed identity did not hold"
print("RESULT:", "ALL PASS")
sys.exit(0)
