import json
import sympy as s
D=4
N=1<<D
Z=s.zeros
I=s.eye(N)
C=[]
for j in range(D):
 M=Z(N)
 for mask in range(N):
  if not (mask>>j)&1:
   M[mask|(1<<j),mask]=(-1)**((mask&((1<<j)-1)).bit_count())
 C.append(M)
A=[m.T for m in C]
def c(v): return sum((v[j]*C[j] for j in range(D)),Z(N))
def ann(v): return sum((v[j]*A[j] for j in range(D)),Z(N))
def gamma(X): return sum((X[i,j]*C[i]*A[j] for i in range(D) for j in range(D)),Z(N))
def E(i,j):
 M=Z(D);M[i,j]=1;return M
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
Gs=[E(1,2)+E(2,0),E(1,3)+E(3,0),E(0,2)+E(2,1),E(0,3)+E(3,1),E(2,3)-E(3,2),E(1,1)-E(0,0)]
assert all(X.T*eta+eta*X==Z(D) for X in Gs)
V=[s.Matrix([0,s.Rational(1,3),0,0]),s.Matrix([s.Rational(1,4),s.Rational(2,7),s.Rational(1,5),-s.Rational(1,11)]),s.Matrix([s.Rational(1,13),s.Rational(2,17),s.Rational(1,7),s.Rational(2,19)]),s.Matrix([s.Rational(1,23),-s.Rational(2,29),s.Rational(3,31),s.Rational(1,5)])]
assert s.Matrix.hstack(*V).det()!=0
q=s.Matrix([0,1,0,0]);nu=s.Rational(1,3)
bs=[s.eye(N)[:,i] for i in [0,2,13,15]]
counts={'full16_trace_link_rows':0,'quartet_link_rows':0,'quartet_offdiagonals':0,'coframe_cancellation_rows':0,'balanced_link_cancellations':0,'low_only_nonzero_controls':0}
for ts in [[-1,s.I,-s.I,1],[s.I,1,1,1]]:
 zetas=[t-1 for t in ts]
 a=sum((zetas[r]*V[r] for r in range(D)),Z(D,1))
 DD=c(a)+ann(s.conjugate(a))
 lam=(s.conjugate(a).T*a)[0]
 assert s.simplify(DD*DD-lam*I)==Z(N)
 for r in range(D):
  for X in Gs:
   dd=ts[r]*c(V[r])*gamma(X)
   delta=dd+dd.conjugate().T
   dDelta=DD*delta+delta*DD
   expect=-16*s.re(ts[r]*(s.conjugate(a).T*X*V[r])[0])
   assert s.simplify(s.trace(dDelta)-expect)==0
   counts['full16_trace_link_rows']+=1
   if ts[1:]!=[1,1,1]:continue
   high=-2*nu*s.re(s.conjugate(ts[0]-1)*ts[r])*(q.T*X*V[r])[0]
   Q=s.Matrix(4,4,lambda i,j:(bs[i].T*dDelta*bs[j])[0])
   assert s.simplify(Q-s.diag(0,0,high,high))==Z(4)
   counts['quartet_link_rows']+=4;counts['quartet_offdiagonals']+=12
   Aenergy=s.expand_complex((ts[0]-1)*s.conjugate(ts[0]-1))
   # Conditional coframe moment Mspec=-Aenergy Euu; no invented spectral action.
   therm=(Aenergy/2 if r==0 else -Aenergy/2)*(V[0].T*X*V[r])[0]
   assert s.simplify(therm+s.Rational(1,2)*high)==0
   counts['balanced_link_cancellations']+=1
   if therm!=0:counts['low_only_nonzero_controls']+=1
 for r in range(D):
  for j in range(D):
   v=s.eye(D)[:,j]
   delta=c(zetas[r]*v)+ann(s.conjugate(zetas[r]*v))
   dDelta=DD*delta+delta*DD
   expected=2*s.re(zetas[r]*(s.conjugate(a).T*v)[0])
   assert s.simplify(dDelta-expected*I)==Z(N)
   counts['coframe_cancellation_rows']+=1
p=(s.sqrt(5)-1)/2
bound=4*s.Rational(1,2**20)/p**3
A33=s.Rational(33,16)
assert s.simplify(bound-(2+s.sqrt(5))/262144)==0
assert A33>bound
# Hodge-paired basis has half its norm on each half, even for unequal RIGHT eigenvalues.
for lo,hi in [(bs[0],bs[3]),(bs[1],bs[2])]:
 for sign in [-1,1]:
  phi=(lo+sign*hi)/s.sqrt(2)
  assert (phi.T*phi)[0]==1
  assert sum((phi.T*bs[j]*bs[j].T*phi)[0] for j in [2,3])==s.Rational(1,2)
# Analytic source-bound identities, plus rational hostile checks of every inequality.
b,z,Znormal,slack=s.symbols('b z Znormal slack', positive=True)
m=s.symbols('m',positive=True,integer=True)
F=1-z+z*b**m
t=1-z+slack
kappa=b**(m-1)*(t/F-1)/Znormal
assert s.simplify(-kappa-b**(m-1)*(z*b**m-slack)/(Znormal*F))==0
assert s.simplify(s.diff(m*(1-b)*b**(m-1),b)-m*b**(m-2)*((m-1)-m*b))==0
rational_bound_checks=0
for M in range(1,8):
 cm=s.Integer(1) if M==1 else (1-s.Rational(1,M))**(M-1)
 for bb in [s.Rational(i,8) for i in range(1,9)]:
  zz=s.Rational(1,16)
  ff=1-zz+zz*bb**M
  for tt in [1-zz,1-zz/2,1]:
   kk=bb**(M-1)*(tt/ff-1)
   assert max(0,-kk)<=zz*bb**(2*M-1)/(1-zz)
   assert M*(1-bb)*bb**(M-1)<=cm
   rational_bound_checks+=1
improved_bound=4*s.Rational(1,2**20)/(1-s.Rational(1,2**20))
assert improved_bound==s.Rational(4,1048575)
assert A33>improved_bound
print(json.dumps({'status':'PASS','counts':counts,'native_z_bound_exact':str(s.simplify(bound)),'native_z_bound_float':float(bound),'reference128_Lu33_A':str(A33),'strict_seed_obstruction':True,'improved_A_bound_exact':str(improved_bound),'improved_A_bound_float':float(improved_bound),'global_scale_bound':'beta R <= c_m z/(1-z) <= z/(1-z), c_m=(1-1/m)^(m-1) for m>1','rational_bound_checks':rational_bound_checks,'scope':'exact homogeneous coframe-to-link reduction and necessary source bound; formal substituted moment is not a physically selected spectral root'},indent=2))
