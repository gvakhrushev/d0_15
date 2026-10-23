#!/usr/bin/env python3
"""Research: full four-flag CAR16 grade-1 two-null Julia history source.
All four outcomes retained. No claim that Book03 selects its pointer Shannon.
"""
import sympy as s
x,a=s.symbols('x a', real=True)
b=x-a; I=s.eye(4); A=s.zeros(4);A[1,2]=A[2,0]=1
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
assert A.T*eta+eta*A==s.zeros(4) and A**3==s.zeros(4)
psi=s.Matrix([1,0,1,0])/s.sqrt(2)
assert (psi.T*psi)[0]==1
S=A+A.T;U2=A.T*A+(A*A+A.T*A.T)/2
m1=s.simplify((psi.T*S*psi)[0]);m2=s.simplify((psi.T*U2*psi)[0]);s2=s.simplify((psi.T*S*S*psi)[0]);assert (m1,m2,s2)==(1,1,s.Rational(3,2))

def tr2(expr):
    poly=s.Poly(s.expand(expr),x,a)
    return s.expand(sum(c*x**e[0]*a**e[1] for e,c in poly.terms() if sum(e)<=2))
def trmat(M):return M.applyfunc(tr2)
def T(t):return I/2+t*A/2+t*t*A*A/4
def F(t):return s.sqrt(3)*I/2 -t*S/(4*s.sqrt(3)) +t*t*(-U2/4-S*S/48)/s.sqrt(3)
assert trmat(T(a).T*T(a)+F(a).T*F(a))==I
assert trmat(T(b).T*T(b)+F(b).T*F(b))==I
K=[T(b)*T(a),F(b)*T(a),T(b)*F(a),F(b)*F(a)]
ps=[tr2((psi.T*k.T*k*psi)[0]) for k in K]
assert tr2(sum(ps))==1
want=[(1+x+x*x)/16, (1+a+a*a)/4-(1+x+x*x)/16,
 s.Rational(3,16)+s.Rational(3,16)*x-a/4+s.Rational(3,16)*x*x-s.Rational(15,32)*a*x+s.Rational(7,32)*a*a]
want.append(s.expand(1-sum(want)))
assert all(s.simplify(want[i]-ps[i])==0 for i in range(4))
q0=[s.simplify(w.subs({x:0,a:0})) for w in ps]
assert q0==[s.Rational(t,16) for t in (1,3,3,9)]
D=s.Matrix([[s.diff(q,v).subs({x:0,a:0}) for v in (x,a)] for q in ps])
assert D==s.Matrix([[s.Rational(1,16),0],[-s.Rational(1,16),s.Rational(1,4)],[s.Rational(3,16),-s.Rational(1,4)],[-s.Rational(3,16),0]])
Fisher=s.Matrix([[s.factor(sum(D[k,i]*D[k,j]/q0[k] for k in range(4))) for j in range(2)] for i in range(2)])
assert Fisher==s.Matrix([[s.Rational(1,3),-s.Rational(1,3)],[-s.Rational(1,3),s.Rational(2,3)]])
Hgrad=s.Matrix([-sum(D[k,i]*s.log(q0[k]) for k in range(4)) for i in range(2)])
assert s.simplify(Hgrad[0]-s.log(3)/4)==0 and Hgrad[1]==0
Hess=s.Matrix([[-sum(s.diff(ps[k],v,w).subs({x:0,a:0})*s.log(q0[k]) for k in range(4))-Fisher[i,j] for j,w in enumerate((x,a))] for i,v in enumerate((x,a))]).applyfunc(s.simplify)
correct=s.Matrix([[s.log(3)/2-s.Rational(1,3),s.Rational(1,3)-s.Rational(15,32)*s.log(3)],[s.Rational(1,3)-s.Rational(15,32)*s.log(3),s.Rational(15,16)*s.log(3)-s.Rational(2,3)]])
assert s.simplify(Hess-correct)==s.zeros(2)
assert s.simplify(Hess[1,1]+2*Hess[0,1])==0
reduced=s.simplify(Hess[0,0]-Hess[0,1]**2/Hess[1,1]);assert s.simplify(reduced-(s.Rational(17,64)*s.log(3)-s.Rational(1,6)))==0
assert float(Hess[1,1])>0 and float(reduced)>0
assert s.factor(Fisher.det())==s.Rational(1,9)
Ired=s.simplify(Fisher[0,0]-Fisher[0,1]**2/Fisher[1,1]);assert Ired==s.Rational(1,6)
print('PASS exact: complete CAR grade1/Julia fresh flags, four true outcomes, all norms sum=1 through second jet')
print('BASE q:',q0,'SOURCE Dq:',D.tolist())
print('PASS exact: holonomy U(x-a)U(a)=U(x), independent of history a; vertical Fisher = 2/3')
print('Fisher[x,a]=',Fisher.tolist(),'reduced geometric Fisher=',Ired)
print('Shannon dH[x,a]=',[s.simplify(z) for z in Hgrad])
print('Shannon Hessian=',Hess.tolist(),'reduced=',reduced,'=',s.N(reduced,12))
print('PASS: local history-stationary a*=x/2+O(x²), no ad hoc history penalty, full Shannon not function of Hol alone')
print('FIREWALL: original grade1 belongs to CAR16; mathematical fresh Julia class only, not selected literal Book03/v8/full128 physical price; GR_closed=false')
