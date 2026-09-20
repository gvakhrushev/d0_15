#!/usr/bin/env python3
"""Exact certificate for the A1 compensator/Noether research result.

Scope:
- finite undirected graphs, exact rational arithmetic;
- verifies the positive C' mechanism on representative non-bipartite and bipartite graphs;
- verifies the K(9,11,13) specialization, including rank(B)=33 and dim ker(B)=326;
- verifies negative controls separating a variational gauge completion from post-hoc Laplacianization.

This certificate does NOT prove the arbitrary-graph theorems. Those remain Lean targets in
02_REGISTRY/frontier/A1_COMPENSATOR_NOETHER_RESULT.md.
"""
from fractions import Fraction as Q

def check(name, cond, detail=""):
    if not cond:
        raise SystemExit("FAIL " + name + (" | " + detail if detail else ""))
    print("PASS", name, ("| " + detail if detail else ""))

def rref(A, b=None):
    m, n = len(A), len(A[0])
    R = [row[:] + ([b[i]] if b is not None else []) for i, row in enumerate(A)]
    piv=[]; r=0
    for c in range(n):
        p=next((i for i in range(r,m) if R[i][c] != 0), None)
        if p is None: continue
        R[r],R[p]=R[p],R[r]
        z=R[r][c]
        R[r]=[x/z for x in R[r]]
        for i in range(m):
            if i != r and R[i][c] != 0:
                f=R[i][c]
                R[i]=[x-f*y for x,y in zip(R[i],R[r])]
        piv.append(c); r+=1
        if r==m: break
    return r,piv,R

def rank(A):
    return rref(A)[0]

def solve(A,b):
    m,n=len(A),len(A[0])
    r,piv,R=rref(A,b)
    for i in range(r,m):
        if R[i][n] != 0:
            return None
    x=[Q(0)]*n
    for i,c in enumerate(piv):
        x[c]=R[i][n]
    return x

def complete_multipartite(parts):
    zone=[]
    for a,k in enumerate(parts): zone += [a]*k
    n=len(zone)
    E=[(i,j) for i in range(n) for j in range(i+1,n) if zone[i] != zone[j]]
    return n,E,zone

def cycle(n):
    E=[]
    for i in range(n):
        j=(i+1)%n
        E.append((min(i,j),max(i,j)))
    return n,sorted(set(E))

def div_row(n,E,T):
    out=[Q(0)]*n
    for i,j in E:
        out[i]+=T[(i,j)]; out[j]+=T[(i,j)]
    return out

def weighted_div(n,E,T,W):
    return div_row(n,E,{e:T[e]*W[e] for e in E})

def Btranspose(E,phi):
    return {(i,j):phi[i]+phi[j] for i,j in E}

def signless_Q(n,E,W=None):
    if W is None: W={e:Q(1) for e in E}
    A=[[Q(0)]*n for _ in range(n)]
    for i,j in E:
        w=W[(i,j)]
        A[i][i]+=w; A[j][j]+=w
        A[i][j]+=w; A[j][i]+=w
    return A

def S_A2(E,h,rho):
    return 2*sum(h[e]*h[e]/(rho[e[0]]*rho[e[1]]) for e in E)

def W_of(E,rho):
    return {e:Q(1)/(rho[e[0]]*rho[e[1]]) for e in E}

def M_of(E,h,rho):
    W=W_of(E,rho)
    return {e:W[e]*h[e] for e in E}

def S_ext(E,h,eta,rho):
    w={e:h[e]-Q(1,2)*(eta[e[0]]+eta[e[1]]) for e in E}
    return S_A2(E,w,rho)

def ext_response(n,E,h,eta,rho):
    W=W_of(E,rho)
    w={e:h[e]-Q(1,2)*(eta[e[0]]+eta[e[1]]) for e in E}
    Mw={e:W[e]*w[e] for e in E}
    Te={e:4*Mw[e] for e in E}
    Tii=[-4*x for x in div_row(n,E,Mw)]
    return w,Te,Tii

def eliminate(n,E,h,rho):
    W=W_of(E,rho)
    K=signless_Q(n,E,W)
    rhs=div_row(n,E,M_of(E,h,rho))
    phi=solve(K,rhs)
    if phi is None:
        raise SystemExit("FAIL compensator system inconsistent")
    w={e:h[e]-phi[e[0]]-phi[e[1]] for e in E}
    G={e:4*w[e]*W[e] for e in E}
    return phi,w,G,W

def dot(E,A,B):
    return sum(A[e]*B[e] for e in E)

def dot_rho(E,rho,A,B):
    return sum(rho[e[0]]*rho[e[1]]*A[e]*B[e] for e in E)

# ------------------------------------------------------------------
# 1. Shift adjoint identity on an explicit irregular graph.
n=5
E=[(0,1),(0,2),(0,3),(1,2),(1,4),(2,3),(3,4)]
T={e:Q((7*e[0]+11*e[1]+3)%17-8,5) for e in E}
xi=[Q(2),Q(-3,2),Q(5,3),Q(-7,4),Q(11,6)]
lhs=sum(T[e]*(xi[e[0]]+xi[e[1]]) for e in E)
rhs=sum(xi[i]*div_row(n,E,T)[i] for i in range(n))
check("shift_adjoint_exact", lhs==rhs)

# 2. Off-shell gauge invariance + Noether identity + derivative/Hessian check.
h={e:Q(2+3*e[0]+5*e[1],7) for e in E}
rho=[Q(5,4),Q(7,5),Q(9,4),Q(11,6),Q(13,7)]
eta=[Q(1,3),Q(-2,5),Q(7,6),Q(-3,4),Q(5,8)]
shift=[Q(2,3),Q(-1,2),Q(3,5),Q(4,7),Q(-5,9)]
h2={e:h[e]+shift[e[0]]+shift[e[1]] for e in E}
eta2=[eta[i]+2*shift[i] for i in range(n)]
check("S_ext_finite_shift_invariant", S_ext(E,h,eta,rho)==S_ext(E,h2,eta2,rho))
w,Te,Tii=ext_response(n,E,h,eta,rho)
check("off_shell_matrix_divergence_zero",
      all(Tii[i]+div_row(n,E,Te)[i]==0 for i in range(n)))

eps=Q(1,17)
for i in range(n):
    ep=eta[:]; em=eta[:]
    ep[i]+=eps; em[i]-=eps
    d=(S_ext(E,h,ep,rho)-S_ext(E,h,em,rho))/(2*eps)
    check("diagonal_is_actual_derivative_v%d"%i, 2*d==Tii[i])

i,j=E[0]
ep=eta[:]; em=eta[:]
ep[i]+=eps; em[i]-=eps
dTe=(ext_response(n,E,h,ep,rho)[1][(i,j)]-ext_response(n,E,h,em,rho)[1][(i,j)])/(2*eps)
hp=dict(h); hm=dict(h); hp[(i,j)]+=eps; hm[(i,j)]-=eps
dTii=(ext_response(n,E,hp,eta,rho)[2][i]-ext_response(n,E,hm,eta,rho)[2][i])/(2*eps)
check("hessian_integrability", dTe==Q(1,2)*dTii and dTe==-2/(rho[i]*rho[j]))
check("laplacianization_negative_control", Q(0) != Q(1,2)*dTii)

# 3. Compensator elimination + envelope + weighted universal property.
phi,w,Gphys,W=eliminate(n,E,h,rho)
check("compensator_row_divergence_zero", all(x==0 for x in div_row(n,E,Gphys)))
Graw={e:4*M_of(E,h,rho)[e] for e in E}

# alternating 4-cycle delta in ker B: 0-1-2-3-0
delta={e:Q(0) for e in E}
for a,b,s in [(0,1,1),(1,2,-1),(2,3,1),(3,0,-1)]:
    e=(min(a,b),max(a,b)); delta[e]+=Q(s)
check("delta_in_ker_B", all(x==0 for x in div_row(n,E,delta)))
diff={e:Graw[e]-Gphys[e] for e in E}
check("rho_pairing_universal_property", dot_rho(E,rho,diff,delta)==0)
check("euclidean_pairing_is_not_same_projection", dot(E,diff,delta)!=0)

e=E[2]
hp=dict(h); hm=dict(h); hp[e]+=eps; hm[e]-=eps
_,wp,_,_=eliminate(n,E,hp,rho)
_,wm,_,_=eliminate(n,E,hm,rho)
Sp=S_A2(E,wp,rho); Sm=S_A2(E,wm,rho)
check("envelope_gradient_exact", (Sp-Sm)/(2*eps)==Gphys[e])

# Nonzero divergence-free response must have both signs in this instance.
vals=list(Gphys.values())
check("inhomogeneous_response_sign_indefinite",
      any(v>0 for v in vals) and any(v<0 for v in vals))

# 4. Bipartite ambiguity changes phi but not w.
n6,E6=cycle(6)
rho6=[Q(2+i,3) for i in range(6)]
h6={e:Q(3+2*e[0]+5*e[1],11) for e in E6}
phi6,w6,G6,W6=eliminate(n6,E6,h6,rho6)
alt=[Q(1 if i%2==0 else -1) for i in range(6)]
phi6b=[phi6[i]+7*alt[i] for i in range(6)]
w6b={e:h6[e]-phi6b[e[0]]-phi6b[e[1]] for e in E6}
check("bipartite_phi_nonunique_but_w_unique", w6b==w6)

# 5. K(9,11,13): exact rank, zone-constant pure gauge, inhomogeneous conserved response.
N,EK,z=complete_multipartite([9,11,13])
QK=signless_Q(N,EK)
r=rank(QK)
check("K91113_edge_count", len(EK)==359)
check("K91113_rank_B_rank_Q", r==33, "rank="+str(r))
check("K91113_kernel_dimension", len(EK)-r==326)

c={(0,1):Q(2),(0,2):Q(5),(1,2):Q(7,3)}
hz={e:c[(min(z[e[0]],z[e[1]]),max(z[e[0]],z[e[1]]))] for e in EK}
rhoz=[Q(1),Q(3,2),Q(2)]
rhoK=[rhoz[z[i]] for i in range(N)]
phiz,wz,Gz,Wz=eliminate(N,EK,hz,rhoK)
check("K91113_zone_constant_pure_gauge", all(v==0 for v in wz.values()) and all(v==0 for v in Gz.values()))

# deterministic fully inhomogeneous positive rational configuration
hi={}
for i,j in EK:
    hi[(i,j)]=Q(1+((17*i+31*j+7)%19), 1+((5*i+11*j)%7))
rhoi=[Q(2+((13*i+3)%11),1+((7*i+1)%5)) for i in range(N)]
phii,wi,Gi,Wi=eliminate(N,EK,hi,rhoi)
divi=div_row(N,EK,Gi)
pos=sum(v>0 for v in Gi.values()); neg=sum(v<0 for v in Gi.values())
check("K91113_inhomogeneous_exact_conservation", all(v==0 for v in divi))
check("K91113_inhomogeneous_sign_indefinite", pos>0 and neg>0, "(+,-)=(%d,%d)"%(pos,neg))

# 6. General positivity no-go checked exhaustively as a logical implication on this response:
# if all entries were nonnegative and row sums zero then all entries would vanish.
# Here G is nonzero, conserved, hence it must be sign-indefinite.
check("positivity_nogo_instance", any(v!=0 for v in Gi.values()) and pos>0 and neg>0)

print("RESULT PASS A1 compensator/Noether research certificate")
