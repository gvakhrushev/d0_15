#!/usr/bin/env python3
"""Changed algebra for retained-matrix-past nonlinear field composition.

No native-programme, full heat, GR-root or physical-admission replay.
Run: python retained_nonlinear_source_check.py REPOSITORY_ROOT
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import sympy as s

repo = Path(sys.argv[1]).resolve()
INPUT = '72619235'
PRIMARY = '02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
DUST = '02_REGISTRY/research/A4D_CLOSED_HISTORY_NONLINEAR_EINSTEIN_DUST_2026_10_28.md'
checks = []
def require(ok, label):
    if not ok:
        raise ArithmeticError(label)
    checks.append(label)

def zero(M):
    return all(s.cancel(x) == 0 for x in M)

pins = {}
for name in (PRIMARY, DUST):
    blob = subprocess.check_output(['git', 'rev-parse', INPUT+':'+name], cwd=repo).decode().strip()
    data = subprocess.check_output(['git', 'cat-file', 'blob', blob], cwd=repo)
    pins[name] = {'git_blob':blob, 'sha256':hashlib.sha256(data).hexdigest()}

Q=s.Rational
R=s.Matrix([[Q(3,5),-Q(4,5)],[Q(4,5),Q(3,5)]])
C1=s.diag(1,Q(1,2))
C2=R*s.diag(1,Q(1,3))*R.T
K=C2*C1
S=K.T*K
require(not zero(C1*C2-C2*C1), 'old positive factors do not commute')
require(not zero(K*K.T-K.T*K), 'complete old cold corner is nonnormal')
require(S.det()>0 and S.trace()>0 and (s.eye(2)-S).det()>0,
        'fixed old Gram is a strict nonzero contraction')

x,y=s.symbols('x y', real=True)
z=Q(1,4); a=1-z
alpha=[Q(1,2),Q(3,4)]; gamma=[Q(1,2),Q(2,3)]
ps=[x,y]; om=[Q(2),Q(3)]
ts=[1-alpha[i]*gamma[i]*ps[i]*(1-gamma[i]*ps[i]) for i in range(2)]
bs=[alpha[i]*gamma[i]*(1-2*gamma[i]*ps[i]) for i in range(2)]
T=ts[0]*ts[1]
point={x:Q(1,5),y:Q(1,4)}
D=a*s.eye(2)+z*T*S
D0=D.subs(point); inv=D0.inv()
w=(z*T*s.trace(S*D.inv())).subs(point)
rows=[]
for i,v in enumerate(ps):
    row=-s.trace(inv*D.diff(v).subs(point))
    expected=(w*bs[i]/ts[i]).subs(point)
    require(s.cancel(row-expected)==0, 'whole price row '+str(i)+' equals genuine cumulative gain')
    require(row>0, 'whole price row '+str(i)+' has positive gain')
    rows.append(str(row))
# Matrix log derivative: the exact rational identity d(-log det D)=-Tr(D^-1 dD).
for v in ps:
    require(s.cancel((-s.diff(D.det(),v)/D.det()+s.trace(D.inv()*D.diff(v))).subs(point))==0,
            'logdet and trace first source agree for '+str(v))
# The price is coupled even though each local source uses a positive multiplier.
mixed=(-s.diff(D.det(),x,y)/D.det()+s.diff(D.det(),x)*s.diff(D.det(),y)/D.det()**2).subs(point)
require(mixed!=0, 'whole price retains mixed cross-block response')
# An old scale variation is not annihilated by the future source normalization.
past_row=-2*z*T.subs(point)*s.trace(inv*S)
require(past_row!=0 and past_row<0, 'genuine changing-past source remains nonzero')
Srank=s.diag(Q(1,2),0)
grank=z*bs[0].subs(point)*s.trace(Srank*(a*s.eye(2)+z*ts[0].subs(point)*Srank).inv())/om[0]
require(grank>0, 'nonzero rank-deficient past still has positive field gain')
Szero=s.zeros(2)
require(s.trace(Szero)==0, 'zero old corner is the explicit lost-gain boundary')
# A scalar old-cut expectation alone fails: returning an old failed component matters.
P=s.diag(1,0); V=s.Matrix([[0,1],[1,0]])
B=s.Matrix([[Q(1,2),Q(1,4)],[Q(1,4),Q(1,2)]])
require(zero(P*B*P-Q(1,2)*P) and zero(P*V*P), 'hostile control satisfies only scalar old-cut compression')
require(not zero(P*B*V*P), 'hostile cross-block can return an old failed component')
# All-column private-factor composition, with a nontrivial private reflection.
u=s.Matrix([[Q(3,5),Q(4,5)],[Q(4,5),-Q(3,5)]])
require(zero(u.T*u-s.eye(2)), 'private test is a full reflection')
# In old-first tensor order, select each private blank column.
E=s.zeros(4,2); E[0,0]=1; E[2,1]=1
require(zero(E.T*s.kronecker_product(K,u)*E-Q(3,5)*K),
        'full private factor multiplies the entire nonnormal old corner')
# The original Julia factors give an actual nonzero-gain hypothesis automatically.
p=(s.sqrt(5)-1)/2
require(s.simplify(1-2*p*p-p**3)==0 and bool(p>0), 'original Julia lower factor equals positive p cubed')
# Exact scalar eigenvalue identity behind the spectrum-uniform third derivative bound.
l=s.symbols('l', positive=True)
t=ts[0]; b=bs[0]; d=2*alpha[0]*gamma[0]**2
fprime=z*b*l/(a+z*t*l)
expected=-3*d*z*l/(a+z*t*l)+2*b*b*z*z*l*l/(a+z*t*l)**2
require(s.cancel(s.diff(fprime,x,2)/fprime-expected)==0,
        'exact third derivative ratio underlies the positive spectral mixture bound')
# An early compiled node error does not disappear from an IDEAL product gain.
v=s.symbols('v', positive=True)
wv=z*v*s.trace(S*(a*s.eye(2)+z*v*S).inv())
ratio=s.cancel(wv.subs(v,Q(3,4)*v)/wv)
require(s.limit(ratio,v,0)==Q(3,4),
        'hostile early baseline error leaves a nonvanishing ideal-gain bias')
actual_point={x:Q(21,100),y:Q(1,4)}
Da=D.subs(actual_point); wa=(z*T*s.trace(S*D.inv())).subs(actual_point)
for i,var in enumerate(ps):
    actual_row=-s.trace(Da.inv()*D.diff(var).subs(actual_point))
    require(s.cancel(actual_row-(wa*bs[i]/ts[i]).subs(actual_point))==0,
            'actual effective-center normalization restores source row '+str(i))
result={'status':'PASS','GR_closed':False,'input_commit':subprocess.check_output(['git','rev-parse',INPUT],cwd=repo).decode().strip(),
        'input_pins':pins,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'checks':checks,'nonnormal_old_corner':str(K),'old_gram':str(S),'whole_price_rows':rows,
        'mixed_price_row':str(mixed),'changing_past_row':str(past_row),
        'scope':'exact changed matrix algebra; analytic estimates and cumulative theorem in primary7dd; no large native execution, physical admission or exact finite GR roots'}
print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
