import sympy as s
f,fx,fy,fxx,fxy,fyy,fxxx,fxxy,fxyy,fyyy=s.symbols('f fx fy fxx fxy fyy fxxx fxxy fxyy fyyy', real=True)
v=[f,fx,fy,fxx,fxy,fyy]
dx=[fx,fxx,fxy,fxxx,fxxy,fxyy];dy=[fy,fxy,fyy,fxxy,fxyy,fyyy]
def der(a,i):
 return sum(s.diff(a,z)*dz for z,dz in zip(v,dx if i==1 else dy)) if i in [1,2] else s.S.Zero
g=s.diag(1,-1,-f*f,-f*f);gi=g.inv()
G=[s.Matrix(4,4,lambda a,b:s.simplify(sum(gi[a,k]*(der(g[k,b],r)+der(g[k,r],b)-der(g[r,b],k))/2 for k in range(4)))) for r in range(4)]
Riem={(r,t):(G[t].applyfunc(lambda a:der(a,r))-G[r].applyfunc(lambda a:der(a,t))+G[r]*G[t]-G[t]*G[r]).applyfunc(s.simplify) for r in range(4) for t in range(4)}
Ric=s.Matrix(4,4,lambda b,d:sum(Riem[a,d][a,b] for a in range(4))).applyfunc(s.simplify)
R=s.simplify(s.trace(gi*Ric));Q=s.simplify(s.trace((gi*Ric)**2))
print('R',R,'\nRic',Ric,'\nQ',Q,flush=True)
a,b=s.symbols('a b',real=True)
jet={f:1,fx:-a,fy:-b,fxx:0,fxy:0,fyy:0,fxxx:a,fxxy:0,fxyy:0,fyyy:b}
J=s.Matrix([[der(R,1),der(R,2)],[der(Q,1),der(Q,2)]]).subs(jet).applyfunc(s.factor)
print('J',J,'det',s.factor(J.det()),flush=True)
print('example',s.factor(J.det().subs({a:s.Rational(1,100),b:s.Rational(1,1000)})))

expected=8*a*b*(2*a**4-3*a*a*b*b+a*a+4*b**4-b*b)
if s.expand(J.det()-expected)!=0:raise AssertionError('Ricci invariant Jacobian not verified')
if s.factor(J.det().subs({a:s.Rational(1,100),b:s.Rational(1,1000)}))!=s.Rational(12377463,1562500000000000):raise AssertionError('two-coordinate scalar invariant rank failed')
print('PASS_GENUINELY_TWO_COORDINATE_GEOMETRY')
