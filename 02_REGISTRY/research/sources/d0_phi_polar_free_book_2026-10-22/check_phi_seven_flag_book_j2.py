#!/usr/bin/env python3
"""D0 #334 scoped seven-label Golden two-turn stopped Book J2.
This is NOT a compulsory M1/G0 physical primitive/Info/whole-HJR compiler.
"""
import sympy as s
passed=[]
def check(label,cond):
    if not bool(cond):raise AssertionError(label)
    passed.append(label)
def smat(A,B):
    return A.shape==B.shape and all(s.simplify(x-y)==0 for x,y in zip(A,B))

p=(s.sqrt(5)-1)/2
z=s.Rational(1,2**20)
check('Golden fixed point p+p2=1',s.simplify(p+p*p-1)==0)
check('Golden amplitude algebraic integer quartic',
      s.minimal_polynomial(s.sqrt(p),s.Symbol('x'))==
      s.Symbol('x')**4+s.Symbol('x')**2-1)
E=s.Rational(3,10);b=s.Rational(2,5)
L=4*E*(1-E);B=4*b*(1-b);A=L+(1-L)*B
check('two turn AF and scene effects are contractions',0<L<1 and 0<B<1)
check('sequential OR has correct full complement',
      s.simplify(1-A-(1-L)*(1-B))==0)
I=s.eye(3);PA=s.diag(1,0,0);PB=s.diag(0,1,0);PD=s.diag(0,0,1)
F=A*PA+B*PB
keep=[s.sqrt(z*L)*PA,s.sqrt(z*(1-L)*B)*PA,s.sqrt(z*B)*PB]
stop=[s.sqrt(1-z)*I,s.sqrt(z*(1-L)*(1-B))*PA,
      s.sqrt(z*(1-B))*PB,s.sqrt(z)*PD]
K=sum((q.T*q for q in keep),s.zeros(3))
S=sum((q.T*q for q in stop),s.zeros(3))
check('original keep effect exactly zeta F',smat(K,z*F))
check('every stop effect exactly I-zeta F',smat(S,I-z*F))
check('ALL seven archived routes normalized',smat(K+S,I))
check('dark sector never spuriously kept',K[2,2]==0)
check('all path operators commute with true F',
      all(smat(q*F,F*q) for q in keep+stop))
rho=s.Matrix([[s.Rational(1,3),s.Rational(1,6),s.Rational(1,6)],
              [s.Rational(1,6),s.Rational(1,3),s.Rational(1,6)],
              [s.Rational(1,6),s.Rational(1,6),s.Rational(1,3)]])
check('coherent mixed input normalized',rho.trace()==1)
check('coherent sector input full rank',rho.det()>0)
active=rho
for n in range(1,10):
    active=sum((q*active*q.T for q in keep),s.zeros(3))
    check('all keep histories trace moment '+str(n),
          s.simplify(s.trace(active)-s.trace((z*F)**n*rho))==0)
    check('retained complete stop after '+str(n),
          0<float(s.trace(S*active))<1)
Bp=s.simplify(4*p**3);Ap=s.simplify(Bp*(1+p**6))
r=s.simplify(z*(Ap+Bp)-z*z*Ap*Bp)
check('original two-factor probability EXACT',
      s.simplify(1-r-(1-z*Ap)*(1-z*Bp))==0)
check('genuine original positive small click',0<float(r)<1)
check('single Book scalar F exceeds one',float(r/z)>1)
J2=-528*s.log(1-r)
unit=-s.log(1-z)
ratio=float(J2/unit)
check('original block needs >1024 Book eigenchannels',ratio>1024)
check('original Book block needs only <=1025 in theoretical bound',ratio<1025)
check('actual original 1056 channels sufficient',ratio<1056)
for n in range(1,6):
    tr=s.simplify((Ap**n+Bp**n)*528)
    chk=s.simplify((z**n)*tr/n)
    check('n='+str(n)+' exact Book harmonic positive moment',chk>0)
print('PASS',len(passed),'Golden two-turn / seven Kraus / Book J2 checks')
print('native Book click:',s.N(r,20))
print('theoretical rank boundary:',ratio,'actual native channels 1056')
print('M1/G0 physical native operator, full Book HJR/Info and GR remain OPEN')
