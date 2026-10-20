#!/usr/bin/env python3
"""Exact narrow substitutions; no native price/physical selection is asserted."""
import sympy as s

def need(x,msg):
    if not x:
        raise RuntimeError(msg)

def eq(a,b):
    return s.simplify(a-b)==0

phi=(1+s.sqrt(5))/2
p=1/phi
u=p-p**2
d0=u/2
pi0=s.Rational(6,5)*phi**2
mu2=s.Rational(12288,5)
mu1=s.Rational(1,3)
atop=359*p**2-p**5
aalg=2048*pi0*p**8+s.Rational(2,3)*d0
need(eq(u,p**3),'owned branch bias')
need(eq(2*pi0*(2-phi),s.Rational(12,5)),'owned seam angle')
need(eq(aalg,mu2*u*u+mu1*u),'moment dictionary')
need(eq(aalg,s.Rational(49152,5)*d0*d0+s.Rational(2,3)*d0),'defect moment dictionary')
need(eq(aalg,s.Rational(159739,5)-s.Rational(294902,15)*phi),'exact alpha alg')
gap=atop-aalg
need(eq(gap,-s.Rational(156109,5)+s.Rational(289442,15)*phi),'signed seam dictionary')

# Two genuine scalar-effect repetitions; q is the exact per-trial port1 law.
q=s.symbols('q',real=True)
weights=[1-q,q]
table={(b,c):mu2*(1-2*b)*(1-2*c)+mu1*s.Rational(1,2)*((1-2*b)+(1-2*c))
       for b in (0,1) for c in (0,1)}
expect=s.expand(sum(weights[b]*weights[c]*table[b,c] for b,c in table))
need(eq(expect,mu2*(1-2*q)**2+mu1*(1-2*q)),'full four-history expectation')
need(eq(expect.subs(q,p**2),aalg),'actual cleaned-plus-G realization at Sigma')
need(table[0,1]<0 and table[1,0]<0,'observable table is not asserted positive cost')
t=s.symbols('t',real=True)
f0=1-2*t*t
f1=2*t*(1-t*t)
c=s.sqrt(p)
ss=p
q1=(ss*f0+c*f1)**2+4*c*c*t**4*(1-t*t)
q0=(c*f0-ss*f1)**2+4*ss*ss*t**4*(1-t*t)
need(eq(q0+q1,1),'native full scalar effects normalize')
need(eq(q1.subs(t,0),p*p),'native baseline port1')
need(eq(s.diff(q1,t).subs(t,0),4*p**s.Rational(3,2)),'native source of port1')
source=s.diff(expect.subs(q,q1),t).subs(t,0)
need(eq(source,-8*p**s.Rational(3,2)*(2*mu2*u+mu1)),'nonzero alpha observable source')
need(2*mu2*u+mu1>0,'source coefficient cannot vanish')

# Projective-label realLift is a set map, not an additive/probability lift.
need(eq(p+p*p+u,1+u),'three real-lift weights are not normalized')
need(not eq(u,p+p*p),'F2 plus does not intertwine ordinary real addition')

# Rational log-derivative test, general proof is Jacobi plus local valuation.
z=s.symbols('z')
W=s.diag((z-1)**2/(z-2),(z-3)/(z-4)**3,1)
trace=s.trace(W.inv()*W.diff(z))
need(eq(trace,s.diff(W.det(),z)/W.det()),'Jacobi identity exact example')
res=[s.residue(trace,z,j) for j in (1,2,3,4)]
need(res==[2,-1,1,-3],'integer local divisor orders')

# The missing archive determinant survives fixed retained Schur data.
lam,beta,sv=s.symbols('lam beta sv',positive=True)
K=s.Matrix([[sv+beta**2,beta*lam],[beta*lam,lam**2]])
Schur=K[0,0]-K[0,1]*K[1,0]/K[1,1]
need(eq(Schur,sv),'retained Schur unchanged')
need(eq(K.det(),sv*lam*lam),'archive determinant factor')
need(eq(s.diff(K.det(),lam)/K.det(),2/lam),'nonzero archive source')
print('PASS: exact two-record alpha observable/source, defect distinction, finite divisor and Schur residual controls')
