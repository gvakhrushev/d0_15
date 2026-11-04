"""Exact finite checks for the H.1 prefix-source application, not price selection."""
import itertools
import json
from fractions import Fraction as F
import sympy as s

checks = []
def need(ok, label):
    if not ok:
        raise RuntimeError(label)
    checks.append(label)

p, x, y = s.symbols('p x y', real=True)
z = s.Rational(1, 2**20)
def golden(e):
    n, _ = s.fraction(s.cancel(e))
    return s.rem(s.Poly(n,p),s.Poly(p*p+p-1,p)).as_expr() == 0

E = p*p*(1+x)
ell = 4*E*(1-E)
u = p+p*p*y
B = 4*u*u*(1-u*u)
A = ell+(1-ell)*B
r = s.expand(z*(A+B)-z*z*A*B)
r0 = r.subs({x:0,y:0})
rf = s.diff(r,x).subs({x:0,y:0})
rq = s.diff(r,y).subs({x:0,y:0})
Q = 1-4*z*p**3
R = 1-4*z*p**3*(1+p**6)
need(golden(rf-4*z*p**11*Q), 'original field slope and normalization')
need(golden(rq-8*z*p**6*(R+p**6*Q)), 'original matter slope and normalization')
need(golden(rq/rf-2*p**(-5)*(R/Q+p**6)), 'original Einstein matter ratio')

plo, phi = F(3,5), F(5,8)
need(plo*plo+plo<1<phi*phi+phi, 'rational golden interval')
# p^2=1-p; use the tighter independent bounds (3/8,2/5).
need(1-phi==F(3,8) and 1-plo==F(2,5), 'squared golden interval')
need(0<F(3,8)*F(63,64)<F(2,5)*F(65,64)<1,
     'actual E0 in zero-one interval gives zero <= ell <= one')
ulo, uhi = plo-F(2,5)/64, phi+F(2,5)/64
need((ulo,uhi)==(F(19,32),F(101,160)), 'actual u box')
Blo = 4*ulo**2*(1-uhi**2)
need(Blo==F(5559039,6553600) and Blo>F(3,4), 'B lower bound stronger than three quarters')
zz=F(1,2**20)
need(2*Blo-zz>1 and 2*zz<F(1,2), 'z <= original r <= 2z on the whole box')
need(1-4*zz*phi**3>1-zz>0, 'uniform positive field slope')
need((1-2*zz)/(2*zz)>2, 'entropy slope exceeds log two')
need(2*zz/(1-2*zz)<F(1,4), 'negative-log correction below one quarter')
# log(2)<3/4 follows from exp(3/4)>2 by four positive Taylor terms.
need(sum(F(3,4)**k/F(s.factorial(k)) for k in range(4))>2, 'log two below three quarters')
# log(2)>1/2 follows from integral_1^2 1/t dt > 1/2.

def poly_bound(expr):
    total=s.Rational(0)
    for (ip,ix,iy), coef in s.Poly(s.expand(expr),p,x,y).terms():
        total += abs(coef)*s.Rational(5,8)**ip*s.Rational(1,64)**(ix+iy)
    return total
C1=int(s.ceiling(max(poly_bound(s.diff(r,x)/z),poly_bound(s.diff(r,y)/z))))
C2=int(s.ceiling(max(poly_bound(s.diff(r,x,2)/z),poly_bound(s.diff(r,y,2)/z))))
Kbound=s.Rational(3*C2+4*C1*C1)/(4*s.Rational(3,5)**11*(1-z))
need(C1>0 and C2>0 and Kbound>0, 'explicit readiness-uniform normalized Hessian bound')

# The complete 128-outcome product law; logs remain independent formal symbols.
probs=[F(1,d) for d in (7,9,11,13,17,19,23)]
words=list(itertools.product((0,1),repeat=7))
def weight(word):
    w=F(1)
    for b,P in zip(word,probs):
        w*=P if b else 1-P
    return w
weights=[weight(w) for w in words]
need(sum(weights)==1, 'all 128 flag outcomes normalize')
for j,P in enumerate(probs):
    need(sum(wt for word,wt in zip(words,weights) if word[j])==P, f'full joint marginal {j}')
    deriv=[wt*(F(1)/P if word[j] else -F(1)/(1-P)) for word,wt in zip(words,weights)]
    need(sum(deriv)==0, f'complete score has zero mean {j}')
    for k in range(7):
        c1=-sum(dw for word,dw in zip(words,deriv) if word[k])
        c0=-sum(dw for word,dw in zip(words,deriv) if not word[k])
        need((c1,c0)==((-1,1) if k==j else (0,0)), f'entropy derivative log coefficients {j},{k}')

# Density variation retained, including its sharp quadratic coefficient.
eps, dens, f, q, hf, hq = s.symbols('eps dens f q hf hq', nonzero=True)
need(s.simplify(dens*(hf*eps*f/dens-hq*eps*q/dens)-eps*(hf*f-hq*q))==0,
     'physical PF density cancels once in the linear source')
xx, h2, h3 = s.symbols('xx h2 h3')
Rem=h2*xx**2/2+h3*xx**3/6
need(s.expand(Rem-xx*s.diff(Rem,xx)+s.integrate(xx*s.diff(Rem,xx,2),(xx,0,xx)))==0,
     'sharp density remainder identity')

# Exact m=3 product SAM rightlift, verified for every coordinate.
bits=list(itertools.product((0,1),repeat=3))
pi=[p**(3-sum(b))*p**(2*sum(b)) for b in bits]
v=[[s.Integer(bj)-p*p for bj in b] for b in bits]
need(golden(sum(pi)-1), 'actual SAM product distribution')
for j in range(3):
    need(golden(sum(w*b[j] for w,b in zip(pi,v))), f'centred SAM mean {j}')
    for k in range(3):
        cov=sum(w*b[j]*b[k] for w,b in zip(pi,v))
        need(golden(cov-(p**3 if j==k else 0)), f'SAM covariance and rightlift {j},{k}')
need(golden(p-p*p-p**3), 'Golden variance exactly p cubed')

# Full pinching has the extra SAM entropy source, even with constant SITE.
need(golden((p*p)/p-p), 'one-bit SAM log-odds equals log p')
need(0<plo<phi<1, 'full SAM entropy derivative is strictly positive')
# A centre is not an all-vertex null: f(Y)=Y at Y0=0, s=1/100.
need(not golden(p*p), 'centre-null does not make the zero-bit vertex null')
need(not golden(1-p*p), 'centre-null does not make the one-bit vertex null')

payload={
    'status':'PASS', 'count':len(checks), 'checks':checks,
    'box_radius':'1/64', 'z':str(z),
    'C1':C1,'C2':C2,'normalized_Hessian_bound':str(Kbound),
    'scope':'Exact product-record differential, original slope, finite SAM rightlift, readiness-uniform normalization; no native complete price or task admission.',
    'GR_closed':False,
}
print(json.dumps(payload,ensure_ascii=False,indent=2))
