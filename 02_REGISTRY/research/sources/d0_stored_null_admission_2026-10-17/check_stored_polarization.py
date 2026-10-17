#!/usr/bin/env python3
"""Exact linearized Minkowski Einstein null plane waves vs owned stored-adjoint tangent.
Independent vacuum GR equation, not an on-shell native Cost−Info claim.
"""
from sympy import Matrix, diag, trace, zeros, eye, simplify
from itertools import combinations
import json

eta=diag(1,-1,-1,-1)
k=Matrix([13,3,4,12])
lam=Matrix([205,144,96,72])/83
a=eta*k
pairs=list(combinations(range(4),2))

checks=0
def verify(ok,name):
    global checks
    if not bool(ok): raise RuntimeError(name)
    checks+=1

def same(A,B,name):
    if isinstance(A,Matrix):verify(A.shape==B.shape and all(simplify(x-y)==0 for x,y in zip(A,B)),name)
    else:verify(simplify(A-B)==0,name)

def sym(i,j):
    M=zeros(4);M[i,j]=1;M[j,i]=1
    return M

# H = variation of contravariant inverse metric Q at eta; h_cov = -eta H eta.
# Standard linearized Ricci/Einstein at Fourier covector k; zero iff GR vacuum mode.
def GE(H):
    h=-eta*H*eta; htrace=trace(eta*h)
    kup=eta*k;ks=(k.T*eta*k)[0]
    ric=Matrix(4,4,lambda i,j:(-k[i]*sum(kup[m]*h[m,j] for m in range(4))
                             -k[j]*sum(kup[m]*h[m,i] for m in range(4))
                             +ks*h[i,j]+k[i]*k[j]*htrace)/2)
    return ric-eta*trace(eta*ric)/2

def pack(M):return Matrix([M[i,j] for i in range(4) for j in range(i,4)])

verify((k.T*eta*k)[0]==0, 'all-support genuine null wavevector')
verify(all(a[i]!=0 for i in range(4)),'generic wavevector full a support')
# all 10 independent metric variations:
full=[sym(i,j) for i in range(4) for j in range(i,4)]
F=Matrix.hstack(*[pack(GE(H)) for H in full])
verify(F.rank()==4,'Einstein null symbol has rank 4 on ten symmetric slots')
verify(len(F.nullspace())==6,'vacuum GR solution space has dimension 6')

# Diffeomorphism gauge shifts of the inverse metric:
G=Matrix.hstack(*[pack(a*eye(4)[:,r].T+eye(4)[:,r]*a.T) for r in range(4)])
verify(G.rank()==4,'four gauge dimensions at all-support null k')
same(F*G,zeros(10,4),'all gauge waves satisfy linearized Einstein')
# Their diagonal slots fix gauge uniquely, because diag gauge=2a_r xi_r.
GA=Matrix.hstack(*[a*eye(4)[:,r].T+eye(4)[:,r]*a.T for r in range(4)]) if False else None
verify(all(a[r]!=0 for r in range(4)),'diagonal gauge-fixing unique')
# Restricted diagonal-zero null vacuum chart.
O=Matrix.hstack(*[pack(GE(sym(i,j))) for i,j in pairs])
verify(O.rank()==4,'Einstein symbol restricted to six offdiag varies')
vac=O.nullspace()
verify(len(vac)==2,'offdiag vacuum leaves two physical polarizations')
Hs=[]
for v in vac:
    H=sum((v[t]*sym(*pairs[t]) for t in range(6)),zeros(4))
    Hs.append(H)
    same(GE(H),zeros(4),'offdiag vacuum polarization Einstein zero')
    verify(all(H[i,i]==0 for i in range(4)),'polarization respects four own-edge diagonals')
    verify(pack(H) not in [pack(a*eye(4)[:,j].T+eye(4)[:,j]*a.T) for j in range(4)],'not coordinate basis gauge')
# After adding the fifth invariant lambda^T H lambda=0, only ONE physical polarization remains.
w=Matrix([ (lam.T*H*lam)[0] for H in Hs ])
verify(w.rank()==1,'observer normalization cuts physical polarization plane nontrivially')
verify(len(w.T.nullspace())==1,'one polarization remains')
S=2996*Hs[0]-3771*Hs[1]
same((lam.T*S*lam)[0],0,'surviving physical wave obeys stored observer constraint')
same(GE(S),zeros(4),'surviving wave is vacuum Einstein')
verify(S!=zeros(4),'nontrivial surviving physical wave')
# Explicit lost independent polarization Hs[0], still a genuine vacuum Einstein mode.
verify((lam.T*Hs[0]*lam)[0]!=0,'second GR polarization not stored-native admitted')
# Check no gauge equivalence can repair it after four diagonal conditions have fixed all gauge freedom.
verify(all(a[r]!=0 for r in range(4)),'no nonzero allowed gauge repair')
print(json.dumps({
    'status':'PASS','exact_controls':checks,
    'null_wave_k':[int(x) for x in k], 'null_wave_k_squared':'0',
    'Einstein_symbol_rank':F.rank(), 'vacuum_total_dim':len(F.nullspace()),
    'diffeomorphism_gauge_rank':G.rank(),
    'vacuum_physical_polarizations':2,
    'vacuum_diagonal_zero_dim':len(vac),
    'lambda_vacuum_restrictions':[str(x) for x in w],
    'vacuum_stored_adjoint_dim':1,
    'explicit_surviving_wave':[[str(S[i,j]) for j in range(4)] for i in range(4)],
    'second_gr_polarization_missing':True,
    'GR_proved':False, 'scope':'linearized null Einstein at one regular stored-adjoint flat background, not all D0'
},sort_keys=True))
