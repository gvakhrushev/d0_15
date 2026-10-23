import sympy as s
C=[]
for a in range(4):
 c=s.zeros(16)
 for m in range(16):
  if not(m>>a)&1:c[m|1<<a,m]=(-1)**((m&((1<<a)-1)).bit_count())
 C.append(c)
H=s.symbols('H',real=True);nu=s.Rational(3,5);b=s.sqrt(1-nu**2*(1+H**2/4));b0=s.Rational(4,5)
I=s.eye(16);J=C[2]-C[2].T
Q=C[1]*C[2]*C[0].T+(C[1]*C[2]*C[0].T).T
A1=(J*Q+Q*J)/2 # Hprime=1, native LC K=1/2.
S1=s.zeros(16);TA=s.zeros(16)
for role,cv in enumerate([nu*C[1],nu*(C[0]-H*C[1]/2),nu*C[2],nu*C[3]]):
 r2=nu**2*(1+H**2/4) if role==1 else nu**2;br=b if role==1 else b0
 for W in [cv,cv.T,I+(br-1)*cv*cv.T/r2,I+(br-1)*cv.T*cv/r2]:
  W0=W.subs(H,0);Wd=W.diff(H).subs(H,0)
  S1+=W0.T*Wd/8;TA+=W0.T*A1*W0/8
M1=-2*S1+TA-A1
M3=s.simplify(nu**4*J*M1*J)
assert M1.T==-M1
assert M1!=s.zeros(16)
# Convert d^3 -> (i xi)^3: -i M3 is Hermitian odd cubic principal symbol.
principal=-s.I*M3
assert principal.H==principal
print('true LC principal cubic eigenvalues in L*Delta at H=0,Hprime=1:',principal.eigenvals())
print('nonzero entries M1:',[(i,j,M1[i,j]) for i in range(16) for j in range(16) if M1[i,j]])
# Consequently neither +L*Delta nor |L*Delta| is form bounded by C(1+Delta)
# at continuum high transverse frequency. This refutes the naive energy bound,
# not the possible existence of a corrected hypocoercive energy/semigroup.
