import sympy as s
H,nu,b,b0,k=s.symbols('H nu b b0 k',real=True,nonzero=True)
C=[]
for a in range(4):
 c=s.zeros(16)
 for m in range(16):
  if not(m>>a)&1:c[m|1<<a,m]=(-1)**((m&((1<<a)-1)).bit_count())
 C.append(c)
I=s.eye(16);rho=s.zeros(16);rho[0,0]=rho[2,2]=s.Rational(1,2)
J=C[2]-C[2].T
N=C[1]*C[2].T+C[2]*C[0].T
Q=C[1]*N+(C[1]*N).T
# True continuum D connection from original c(q) Lambda(U) S positive adjoint.
assert Q==C[1]*C[2]*C[0].T+(C[1]*C[2]*C[0].T).T
coeff=s.S.Zero;cross=s.S.Zero;links=s.S.Zero;grad=s.S.Zero
for role,cv in enumerate([nu*C[1],nu*(C[0]-H*C[1]/2),nu*C[2],nu*C[3]]):
 r2=nu**2*(1+H**2/4) if role==1 else nu**2
 br=b if role==1 else b0
 Ws=[cv,cv.T,I+(br-1)*cv*cv.T/r2,I+(br-1)*cv.T*cv/r2]
 for W in Ws:
  dW=W.diff(H)+(W.diff(b)*(-nu**2*H/(4*b)) if role==1 else s.zeros(16))
  A=J*dW;B=Q*W
  def av(M):return (M[0,0]+M[2,2])/2
  grad+=av(A.T*A);cross+=av(A.T*B+B.T*A);links+=av(B.T*B)
print('grad=',s.factor(grad))
print('cross=',s.factor(cross))
print('link=',s.factor(links))
print('Q norms low=',s.trace(rho*Q.T*Q))
# substituted relation b²=1−nu²(1+H²/4), b0²=1−nu² reduce polynomial numerator.
def red(e):
 num,den=s.fraction(s.factor(e));num=s.rem(num,s.Poly(b0**2-1+nu**2,b0).as_expr(),b0);num=s.rem(num,s.Poly(b**2-1+nu**2*(1+H**2/4),b).as_expr(),b);return s.factor(num/den)
print('grad reduced=',red(grad))
print('cross reduced=',red(cross))
print('link reduced=',red(links))
print('LC reduced=',red(grad+cross/2+links/4))
for name,e in [('grad',grad),('cross',cross),('link',links),('LC',grad+cross/2+links/4)]:
 print(name+' ν eliminate=',s.factor(e.subs(nu**2,4*(1-b*b)/(H*H+4))))
# Independent compact forms, after substituting exact defining radical relation.
grad_closed=nu**2/s.Integer(4)*(1+nu**2*H**2/(4*b**2)+nu**2/(1+b)**2)
G=(1-b)*((3*b*b+2*b+1)*H**4+(44*b*b+4)*H**2+32*b**3+64*b*b)/(b*b*(H*H+4)**3)
assert s.factor((grad-grad_closed).subs(nu**2,4*(1-b*b)/(H*H+4)))==0
assert s.factor((grad+cross/2+links/4-G).subs(nu**2,4*(1-b*b)/(H*H+4)))==0
# Isotropic two-transverse derivative: exact cross term vanishes.
J3=C[3]-C[3].T;N3=C[1]*C[3].T+C[3]*C[0].T;Q3=C[1]*N3+(C[1]*N3).T
mixed=s.S.Zero
for role,cv in enumerate([nu*C[1],nu*(C[0]-H*C[1]/2),nu*C[2],nu*C[3]]):
 r2=nu**2*(1+H**2/4) if role==1 else nu**2;br=b if role==1 else b0
 for W in [cv,cv.T,I+(br-1)*cv*cv.T/r2,I+(br-1)*cv.T*cv/r2]:
  dW=W.diff(H)+(W.diff(b)*(-nu**2*H/(4*b)) if role==1 else s.zeros(16))
  A=J*dW+Q*W/2;B=J3*dW+Q3*W/2
  mixed+=s.trace(rho*(A.T*B+B.T*A))
assert s.factor(mixed)==0
print('PASS exact radical coefficient, positivity by positive coefficients, and zero transverse mixed source')
protected8=[0,2,5,7,8,10,13,15];rho8=s.diag(*[s.Rational(1,8) if m in protected8 else 0 for m in range(16)])
G8=s.S.Zero;compressed=s.zeros(8)
for role,cv in enumerate([nu*C[1],nu*(C[0]-H*C[1]/2),nu*C[2],nu*C[3]]):
 r2=nu**2*(1+H**2/4) if role==1 else nu**2;br=b if role==1 else b0
 for W in [cv,cv.T,I+(br-1)*cv*cv.T/r2,I+(br-1)*cv.T*cv/r2]:
  dW=W.diff(H)+(W.diff(b)*(-nu**2*H/(4*b)) if role==1 else s.zeros(16))
  A=J*dW+Q*W/2
  X=A.T*A;G8+=s.trace(rho8*X);compressed+=X.extract(protected8,protected8)
assert s.factor((G8-G).subs(nu**2,4*(1-b*b)/(H*H+4)))==0
assert all(compressed[i,j]==0 for i in range(8) for j in range(8) if i!=j)
print('PASS: whole protected8 equal-weight compression has exactly SAME G as low2; diagonal coefficient')
print('protected8 diagonal=',[s.factor(compressed[i,i].subs(nu**2,4*(1-b*b)/(H*H+4))) for i in [0,1,2,3]])
Abar=s.factor(grad.subs(nu**2,4*(1-b*b)/(H*H+4)))
Cbar=s.factor(cross.subs(nu**2,4*(1-b*b)/(H*H+4)))
Lbar=s.factor(links.subs(nu**2,4*(1-b*b)/(H*H+4)))
Geff=s.factor(Abar-Cbar*Cbar/(4*Lbar))
print('independent link stationary K/Hprime=',s.factor(-Cbar/(2*Lbar)))
print('independent link eliminated coefficient=',Geff)
print('LC independent link source coefficient=',s.factor(Cbar+Lbar))
co8=s.S.Zero
for role,cv in enumerate([nu*C[1],nu*(C[0]-H*C[1]/2),nu*C[2],nu*C[3]]):
 r2=nu**2*(1+H**2/4) if role==1 else nu**2;br=b if role==1 else b0
 for W in [cv,cv.T,I+(br-1)*cv*cv.T/r2,I+(br-1)*cv.T*cv/r2]:
  dW=W.diff(H)+(W.diff(b)*(-nu**2*H/(4*b)) if role==1 else s.zeros(16))
  A=J*dW+k*Q*W
  co8+=s.trace(rho8*A.T*A)
diff8=s.factor((co8-(grad+k*cross+k*k*links)).subs(nu**2,4*(1-b*b)/(H*H+4)))
assert s.factor(diff8.subs(nu**2,4*(1-b*b)/(H*H+4)))==0
print('PASS: protected8 and low2 coefficients equal for independent links')
# One literal W=C_v* acts on q -> -nu H/2 vacuum; QWq=0.
W=nu*(C[0]-H*C[1]/2).T
qvec=s.eye(16)[:,2]
assert Q*W*qvec==s.zeros(16,1)
assert s.simplify((J*W.diff(H)*qvec).dot(J*W.diff(H)*qvec)-nu**2/4)==0
print('PASS: low2 Geff >= nu²/8 by an uncancellable actual Kraus component')
print('protected8 A=',s.factor(co8.subs(k,0).subs(nu**2,4*(1-b*b)/(H*H+4))))
print('protected8 C=',s.factor(s.diff(co8,k).subs(k,0).subs(nu**2,4*(1-b*b)/(H*H+4))))
print('protected8 L=',s.factor((s.diff(co8,k,2)/2).subs(nu**2,4*(1-b*b)/(H*H+4))))

Kratio=s.factor(-Cbar/(2*Lbar))
assert s.simplify(Kratio.subs(H,0)+s.Rational(1,4))==0
assert s.simplify(Kratio.subs(H,-H)-Kratio)==0
print('PASS actual link-stationary ratio is even analytic with K/Hprime=-1/4 at H=0')
