import sympy as s
import time
start=time.monotonic()
r,nu=s.symbols('r nu',real=True,nonzero=True)
I=s.eye(16); C=[]; order=(0,2,3,1)
for j in range(4):
    c=s.zeros(16)
    for b in range(16):
        if not ((b>>j)&1): c[b|(1<<j),b]=(-1)**sum((b>>k)&1 for k in order[:order.index(j)])
    C.append(c)
G=C[0]*C[1].T+C[1]*C[0].T
U=I+2*r/(1-r*r)*G+2*r*r/(1-r*r)*G**2
xs=[s.I*nu*C[0],s.I*nu*C[1]*U,-nu*C[2],-s.I*nu*C[3]]
a=sum((x+x.H-nu*(c+c.T) for x,c in zip(xs,C)), s.zeros(16))/16
A=(a*a).applyfunc(s.cancel)
P=5*r**4+r**3-8*r**2-r+5; Q=23*r**4+6*r**3-32*r**2-10*r+25
sig=nu**2*P/(64*(1-r*r)**2); tau=nu**4*Q/(16384*(1-r*r)**2)
res=A*A-sig*A+tau*I
bad=[(i,j,s.factor(res[i,j])) for i in range(16) for j in range(16) if s.cancel(res[i,j])!=0]
print('quadratic_bad_count',len(bad)); print('first_bad',bad[:2])
print('trace_difference',s.factor(s.trace(A)-8*sig))
vals={r:s.Rational(1,9),nu:s.Rational(3,5)}
print('eigenvals',A.subs(vals).eigenvals())
print('elapsed',time.monotonic()-start)
