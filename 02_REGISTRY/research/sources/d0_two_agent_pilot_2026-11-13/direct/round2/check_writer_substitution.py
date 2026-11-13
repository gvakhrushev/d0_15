"""Exact NPS/RC3 substitution identities and rational algebraic sign isolation."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib, importlib.util, json, sys
import sympy as S
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'AGENTS.md').is_file())
NATIVE=REPO/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
PIN='222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c'
if hashlib.sha256(NATIVE.read_bytes()).hexdigest()!=PIN: raise RuntimeError('native source pin mismatch')
spec=importlib.util.spec_from_file_location('writer_native',NATIVE)
nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
checks=[]
def need(x,n):
    if not bool(x): raise AssertionError(n)
    checks.append(n)
def eq(x,y,n):
    d=x-y
    need(all(S.simplify(v)==0 for v in d) if isinstance(d,S.MatrixBase) else S.simplify(d)==0,n)
p,a,G,F=nt.P,nt.A,nt.G_LOCAL,nt.GOLDEN_FIELD
v=S.Matrix([a,p]);zero=S.Matrix([1,0]);I=S.eye(2)
K=[S.diag(a,p),S.diag(p,a)]
mu0=p**8+p**12;mu1=p**12;kappa=p+2*a*p**3
def coeff(ref,tau):
    return kappa**2*sum(mu*(ref*K[f]*tau)[0]**2/((K[f]*tau).dot(K[f]*tau)) for f,mu in enumerate((mu0,mu1)))
AA=[mu0*coeff(v.T,zero),mu0*coeff(v.T,G**2*zero)]
BB=mu1*coeff(a*zero.T,G.T**2*zero)

# Rigorous rational root isolation of the positive root a^4+a^2-1.
lo,hi=Q(786151377757,10**12),Q(786151377758,10**12)
poly=lambda x:x**4+x*x-1
need(poly(lo)<0<poly(hi),'positive Golden generator lies in exact rational interval')
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y):
    z=[xx*yy for xx in x for yy in y]
    return min(z),max(z)
def bounds(expr):
    an=F.from_sympy(S.cancel(expr))
    acc=(Q(0),Q(0))
    for c in an.to_list():
        q=Q(int(c.numerator),int(c.denominator))
        acc=add(mul(acc,(lo,hi)),(q,q))
    return acc
isolation=[]
for i,A in enumerate(AA):
    low,high=bounds(A-p*BB)
    need(low>0,'exact A>pB for literal word '+str(i))
    isolation.append({'word':i,'A_minus_pB_lower':str(low),'A_minus_pB_upper':str(high)})
u,d=(a+p)/2,(a-p)/2
for name,x in [('d',d),('u-sd',u-p**3*d),('2u-sd',2*u-p**3*d)]:
    need(bounds(x)[0]>0,'positive exact '+name)

# Algebra independent of numerical Golden constants.
c,s,uu,dd,pa,Ac,Bc,q,z=S.symbols('c s u d p A B q z',positive=True)
fp=(uu*c+dd)**2/(1+s*c);fm=(uu*c-dd)**2/(1-s*c)
eq(S.diff(fp,c),(uu*c+dd)*(2*uu+uu*s*c-s*dd)/(1+s*c)**2,'first positive derivative')
eq(S.diff(fp+fm,c),4*c*(uu-s*dd)**2/(1-s*s*c*c)**2,'symmetric sum derivative is nonnegative')
hh=2*Ac*pa*fp+2*Bc*pa**2*fm
eq(hh,2*pa*(Ac-pa*Bc)*fp+2*Bc*pa**2*(fp+fm),'positive-cone decomposition of actual marked h')
alpha,beta=uu*c+dd,uu*c-dd
LW=uu*(Ac*pa*alpha/(1-q)+Bc*pa**2*beta/q)
target=2*uu*(pa*(Ac-pa*Bc)*alpha/(1+s*c)+Bc*pa**2*2*c*(uu-s*dd)/(1-s*s*c*c))
eq(LW.subs(q,(1-s*c)/2),target,'strict positive backward coefficient decomposition')

# Full independent first derivative, in an arbitrary real scalar direction.
x,y,qvar,dx,dy,dq,t=S.symbols('x y qvar dx dy dq t',real=True)
general=Ac*pa*(uu*x+dd*y)**2/(1-qvar)+Bc*pa**2*(uu*x-dd*y)**2/qvar
deriv=S.diff(general.subs({x:x+t*dx,y:y+t*dy,qvar:qvar+t*dq}),t).subs(t,0)
expected=2*uu*(Ac*pa*(uu*x+dd*y)/(1-qvar)+Bc*pa**2*(uu*x-dd*y)/qvar)*dx
expected+=2*dd*(Ac*pa*(uu*x+dd*y)/(1-qvar)-Bc*pa**2*(uu*x-dd*y)/qvar)*dy
expected+=(Ac*pa*(uu*x+dd*y)**2/(1-qvar)**2-Bc*pa**2*(uu*x-dd*y)**2/qvar**2)*dq
eq(deriv,expected,'all independent writer and probability derivatives retained')

# Actual NPS pointer compression with symbolic bank operators represented by scalar symbols.
CW,CV=S.symbols('CW CV',real=True)
Pplus=S.Matrix([[1,1],[1,1]])/2;Pminus=I-Pplus
U=CW*Pplus+CV*Pminus
eq(a*(U*v)[0],a*(u*CW+d*CV),'true born pointer multiplies first X by a')
eq(p*(U*v)[1],p*(u*CW-d*CV),'true born pointer multiplies second X by p')

theta,eta=S.symbols('theta eta',real=True)
rot=lambda w:S.Matrix([[S.cos(w),-S.sin(w)],[S.sin(w),S.cos(w)]])
Af=rot(theta);Ab=rot(theta+eta);Z=S.diag(1,-1)
cw=(zero.T*Ab.T*Z*Af*zero)[0]
cv=(zero.T*Ab.T*Af*zero)[0]
eq(S.trigsimp(cw),S.cos(2*theta+eta),'explicit independent backward bank corner')
eq(S.trigsimp(cv),S.cos(eta),'explicit overlap corner')
eq(S.diff(cw,eta).subs(eta,0),-S.sin(2*theta),'backward direction changes C_W at fixed q')
eq(S.diff(cv,eta).subs(eta,0),0,'backward overlap first variation vanishes at matched centre')

result={'status':'PASS','checks':len(checks),'check_names':checks,'exact_isolation':isolation,
        'baseline':'dc411daf01f697ec85dd22f28bfe124171796645','native_sha256':PIN,
        'proof_sha256':hashlib.sha256((HERE/'WRITER_SUBSTITUTION_RU.md').read_bytes()).hexdigest(),
        'scope':{'NPS_X_substitution':True,'matched_scalar_gain_positive':True,
                 'independent_apparatus_stationarity_proved':False,'full_H1_executed':False,
                 'physical_C_closed':False,'GR_closed':False}}
(HERE/'WRITER_CHECK.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'exact_signs':isolation},ensure_ascii=False))
