import sympy as s
C=[]
for a in range(4):
 c=s.zeros(16)
 for m in range(16):
  if not(m>>a)&1:c[m|1<<a,m]=(-1)**((m&((1<<a)-1)).bit_count())
 C.append(c)
Jq=C[1]-C[1].T;Jx=C[2]-C[2].T
Q=C[1]*C[2]*C[0].T+(C[1]*C[2]*C[0].T).T
r=s.symbols('r',real=True)
# Scale nu=q=1; k=r.  V_{+-1}=Q/4.
v=Q/4;Dzero=s.I*r*Jq;eff=2*v*v
for sign in [-1,1]:
 W=s.I*(r*Jq+sign*Jx)*v+v*Dzero
 eff-=W.H*W
print('offdiag nonzero',[(i,j,eff[i,j]) for i in range(16) for j in range(16) if i!=j and eff[i,j]!=0])
print('diag',[s.factor(eff[i,i]) for i in range(16)])
print('eig r1',eff.subs(r,1).eigenvals())

Pbad=s.diag(*[0 if m in [0,2,5,7,8,10,13,15] else 1 for m in range(16)])
assert eff == -r*r*Pbad/8
assert Pbad.rank()==8
print("PASS exact degenerate effective matrix = -r² P_bad/8, rank8")

# Actual link-stationary branch has K*=-(1/4+O(H²))Hprime.
# Its linear D perturbation is minus one half the LC perturbation, with no
# quadratic amplitude term. Recompute the full degenerate Schur matrix.
v_star=-Q/8;eff_star=2*v_star*v_star
for sign in [-1,1]:
 Wstar=s.I*(r*Jq+sign*Jx)*v_star+v_star*Dzero
 eff_star-=Wstar.H*Wstar
assert eff_star == -r*r*Pbad/32
print("PASS actual stationary-link family splitting = -r² P_bad/32")
