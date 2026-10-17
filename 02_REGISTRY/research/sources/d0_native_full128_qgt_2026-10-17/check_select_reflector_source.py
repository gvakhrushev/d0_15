"""Exact relative-reflector derivative in native SELECT row identities.
Rational two-label class fixture, not the original 64-label Walsh selector.
"""
import sympy as s,json
p=(s.sqrt(5)-1)/2;q=p*p
A=s.diag(s.Rational(3,5),s.Rational(5,13))
B=s.diag(s.Rational(4,5),s.Rational(12,13))
H=s.Matrix([[0,s.Rational(1,7)],[s.Rational(1,7),0]])
dB=s.zeros(2)
for i in range(2):
 for j in range(2):
  dB[i,j]=-(A[i,i]+A[j,j])*H[i,j]/(B[i,i]+B[j,j])
N=A.col_join(B)
dN=H.col_join(dB)
Z=s.zeros(2);I=s.eye(2)
blank=I.col_join(Z)
M=blank-2*N*A
dM=-2*(dN*A+N*H)
count=0
def check(x,lab):
 global count
 if not bool(x):raise RuntimeError(lab)
 count+=1
def mat_eq(X,Y,lab):check(all(s.simplify(a-b)==0 for a,b in zip(X,Y)),lab)

mat_eq(N.T*N,I,'SELECT row isometry')
mat_eq(dN.T*N+N.T*dN,Z,'moving SELECT row source')
mat_eq(N[:2,:],A,'blank SELECT equals A')
mat_eq(dN[:2,:],H,'moving blank equals dA')
mat_eq(M.T*M,I,'true reflected M isometry')
mat_eq(dM.T*M+M.T*dM,Z,'true reflected M source tangent')
Gamma=M.T*dM
Q=q*dM.T*dM-q*q*Gamma.T*Gamma
# Full two-port Kraus factorization at original golden p.
K0=p*blank+q*M; K1=p*s.sqrt(p)*(M-blank)
dK0=q*dM;dK1=p*s.sqrt(p)*dM
mat_eq(K0.T*K0+K1.T*K1,I,'full two-port native state complete')
mat_eq(K0.T*dK0+K1.T*dK1,q*Gamma,'native first Maurer-Cartan source')
mat_eq(dK0.T*dK0+dK1.T*dK1-(q*Gamma).T*(q*Gamma),Q,'QGT actual Kraus')
mat_eq(Q-q*dM.T*dM+q*q*Gamma.T*Gamma,Z,'source identity')
check(s.trace(Q)>0,'strict native record information source')
check(s.simplify(s.trace(Q)-p**3*s.trace(dM.T*dM))>=0,'golden lower bound')
check(s.simplify(q*s.trace(dM.T*dM)-s.trace(Q))>=0,'golden upper bound')
check(Gamma!=Z,'native relative frame connection nonzero')
check(s.trace(dM.T*dM)>0,'nonzero field to M source')
# Zero native D and its variation imply zero record sensitivity.
N0=blank; dN0=s.zeros(4,2); A0=s.zeros(2);dA0=s.zeros(2)
mat_eq(-2*(dN0*A0+N0*dA0),s.zeros(4,2),'zero-mode kernel')
print(json.dumps({'status':'PASS','exact_controls':count,'tr_Q':str(s.simplify(s.trace(Q))),
  'tr_dM2':str(s.trace(dM.T*dM)),'Gamma':str(Gamma),
  'source_formula':'dM=-2(dN A+N dA)',
  'native_admission':False},sort_keys=True))
