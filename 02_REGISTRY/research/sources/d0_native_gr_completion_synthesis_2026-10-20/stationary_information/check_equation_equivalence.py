#!/usr/bin/env python3
"""Narrow exact algebra for equation-equivalence and the actual CAR record test."""
import sympy as s

def require(condition, label):
    if not condition:
        raise RuntimeError(label)

def zero(expr):
    return s.simplify(expr) == 0

x,u,z,C,r = s.symbols('x u z C r', real=True)
v=s.Matrix([x,u])
J=-x*u-u*u
j=s.Matrix([s.diff(J,x),s.diff(J,u)])
H=s.hessian(J,(x,u))
S=J+(j.dot(j))/2
M=s.eye(2)+H
HS=s.hessian(S,(x,u))
require(H.det()==-1,'target is indefinite')
require(M.det()==-2,'multiplier invertible and not SPD')
require(HS==s.Matrix([[1,1],[1,3]]),'new Hessian')
require(HS[0,0]>0 and HS.det()>0,'strict minimum')
require(s.Matrix([s.diff(S,x),s.diff(S,u)])==M*j,'exact source factorization')
require(s.solve(list(M*j),(x,u))=={x:0,u:0},'same unique root')

# Pointwise invertibility alone fails the closed-oneform test.
P=s.Matrix([[1,x],[0,1]])
alpha=P*v
require(P.det()==1,'curl control invertibility')
require(s.diff(alpha[0],u)-s.diff(alpha[1],x)==x,'curl obstruction')

# An invertible multiplier cannot lift the target kernel.
H0=s.diag(1,0)
K=s.diag(0,1)
a,b,c,d=s.symbols('a b c d')
N=s.Matrix([[a,b],[c,d]])
require(s.solve(list(N*H0-(H0+K)),(a,b,c,d))==[],'kernel lift forbidden')

# Actual null curve has nonzero transverse source; cancellation gives extra roots.
g,D,kappa,cc=s.symbols('g D kappa cc', nonzero=True, real=True)
t=-g*x*u-g*D*u*u
dt=s.Matrix([s.diff(t,x),s.diff(t,u)])
require(dt.subs(u,0)==s.Matrix([0,-g*x]),'ridge transverse source')
require(s.hessian(t,(x,u)).det()==-g*g,'ridge saddle')
require(((kappa+cc)*dt).subs(cc,-kappa)==s.zeros(2,1),'cancelled source everywhere')

# A weighted exact Schur projection, including an untouched mismatch direction.
Dmat=s.diag(2,3,5)
B=s.Matrix([[1,0],[0,1],[0,0]])
Proj=Dmat-Dmat*B*(B.T*Dmat*B).inv()*B.T*Dmat
require(Proj==s.diag(0,0,5),'weighted Schur residual')
require(Proj*B==s.zeros(3,2),'free reference tangent cancels')
require(Dmat-Dmat*s.eye(3)*(Dmat.inv())*Dmat==s.zeros(3),'full matching cancels')

# Original live-CAR scene response: d zeta/dH=-C, full readiness/abort retained.
prob=4*z*z*(1-z*z)
dBH=-C*s.diff(prob,z)
require(zero(dBH+8*C*z*(1-2*z*z)),'actual metric response')
law=s.Matrix([r*prob,r*(1-prob),1-r])
dLaw=s.Matrix([r*dBH,-r*dBH,0])
FI=s.factor(sum(dLaw[i]**2/law[i] for i in range(2)))
require(zero(FI-r*dBH*dBH/(prob*(1-prob))),'complete readiness Fisher')
# z in (1/2,2/3) gives 1-2z²>1/9 and B strictly between 0 and 1.
require(1-2*s.Rational(2,3)**2==s.Rational(1,9),'chart positivity margin')
require(prob.subs(z,s.Rational(1,2))==s.Rational(3,4),'lower chart endpoint')
require(prob.subs(z,s.Rational(2,3))==s.Rational(80,81),'upper chart endpoint')

# Same original coframe/shared-link slice, now with an actually actuated top.
a,sc,delta,rho,h=s.symbols('a sc delta rho h', positive=True)
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
T=s.Matrix([[1,s.Rational(1,2),0,0],[1,-s.Rational(1,2),0,0],[0,0,1,0],[0,0,0,1]])
eta_rest=s.diag(1,-1,-1,-1)
require(T.T*eta_rest*T==eta,'native null-to-rest metric transport')
require(T.det()==-1,'orientation pullback cannot be silently dropped')
ef=s.diag(1,a,1,1/a)/sc
raw=T*ef/s.sqrt(rho)
require(s.simplify(rho*raw.T*eta_rest*raw)==ef.T*eta*ef,'actual density dictionary')
ginv=(ef.T*eta*ef).inv()
grad=s.ones(4,1)*(-delta/h)
query=(grad.T*ginv*grad)[0]/rho
require(zero(query-sc**2*delta**2/(rho*h**2)*(2/a-1-a*a)),'actual inverse metric contraction')
require(zero(query.subs(a,1)),'central actuated query remains null at a=1')
require(zero(s.diff(query,a).subs(a,1)+4*sc**2*delta**2/(rho*h*h)),'nonzero metric query derivative')

# The fixed native minus rail depends on b and not on E.
E,b=s.symbols('E b', real=True)
retained=(1-2*b)*s.Matrix([[1-E,-E],[-E,1-E]])
minus=s.Matrix([1,-1])
require(all(zero(entry) for entry in retained*minus-(1-2*b)*minus),'native fixed minus compression')
require(zero(1-(1-2*b)**2-4*b*(1-b)),'native minus cut probability')

p=(s.sqrt(5)-1)/2
sig,gain=s.symbols('sig gain', nonzero=True, real=True)
scene=p+sig*p**2*gain**2*query
Bscene=4*scene**2*(1-scene**2)
require(zero(Bscene.subs(a,1)-4*p**3),'native baseline L')
Ba=s.diff(Bscene,a).subs(a,1)
require(zero(Ba+32*sig*p**6*gain**2*sc**2*delta**2/(rho*h*h)),'native same-slice B_a')
ka,kap,gg,dd=s.symbols('ka kap gg dd', positive=True)
# kappa=-kap: one coframe Fisher term stabilizes iff determinant >= 0.
total=s.Matrix([[ka,kap*gg],[kap*gg,2*kap*gg*dd]])
require(zero(total.det()-kap*gg*(2*dd*ka-kap*gg)),'exact one-probe threshold')
require(zero(total.det().subs(ka,kap*gg/(2*dd))),'threshold equality')
print('PASS: exact matrix equivalence, curl/kernel, ridge cancellation, Schur, same-slice native CAR information and threshold')
