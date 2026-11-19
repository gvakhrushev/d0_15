#!/usr/bin/env python3
"""Original Golden site-address Kac clock: rare-branch first-source cap scaling.

No entire mesh enumeration: consumes published original n20 multiplicity maximum
78 of N10946, genuine PF regular bounds, and first-match complete occupation.
Exact Fraction source controls for tiny addressed alphabets, then strict
native Golden numerical diagnostics. No native Book03 cut/Info selection.
"""
from fractions import Fraction as F
import math,json
checks=0
def require(ok,label):
 global checks
 checks+=1
 if not ok:raise ArithmeticError(label)

def lcap(q,k): return len(q)+1-sum((1-x)**k for x in q)

for w in [(F(1,3),F(2,3)),(F(1,5),F(1,3),F(7,15))]:
 W=len(w)
 for a in (F(1,4),F(1,3)):
  for r in (F(1,7),F(2,7)):
   q=[1-a]+[a*v*(1-r) for v in w]+[a*v*r for v in w]
   require(sum(q)==1,'complete actual U + addressed 0/1 normalized')
   for K in (1,2,3,4,5):
    L=lcap(q,K)
    tail=sum((1-x)**K for x in q)
    require(L==2*W+2-tail,'exact finite K stopped whole-count tail')
    rare=sum(q[W+1:])
    rare_visits=rare*L
    separate=sum(qi*L for qi in q[W+1:])
    require(rare_visits==separate,'exact individual addressed rare visit occupation')
    dq=a*F(1) # derivative of total click mass
    h=F(1,10000)
    q_plus=[1-a]+[a*v*(1-(r+h)) for v in w]+[a*v*(r+h) for v in w]
    q_minus=[1-a]+[a*v*(1-(r-h)) for v in w]+[a*v*(r-h) for v in w]
    finite=(sum((1-x)**K for x in q_plus)-sum((1-x)**K for x in q_minus))/(2*h)
    exact=K*a*sum(v*((1-a*v*(1-r))**(K-1)-(1-a*v*r)**(K-1)) for v in w)
    require(abs(float(finite-exact)) < 1e-4,'complete source finite-difference vs exact clock derivative')

p=(math.sqrt(5)-1)/2
a=2*10946*p**23
r=1.8512395785208469e-6
W=256
wmax=78/10946
K=100000000
qmax=a*wmax*r
qmax_native=qmax
lower=W*math.exp(K*math.log1p(-qmax))
require(.3416<a<.3417,'literal original n20 Golden READY mass')
require(0<qmax<4.64e-9,'original n20 actual worst rare label')
require(lower>160,'strict genuine n20 K100M mean-round deficiency >160')
# Independent rational comparison, no reliance on log/exponential decimal to certify >160:
p_lo=F(6180339887,10**10);p_hi=F(6180339888,10**10)
require((2*p_lo+1)**2<5<(2*p_hi+1)**2,'exact rational enclosure of native Golden p')
a_hi=2*10946*p_hi**23
z=F(1,2**20);l_hi=4*p_hi**3
r_hi=1-(1-z*l_hi)*(1-z*l_hi*(1+p_hi**6))
q_hi=a_hi*F(78,10946)*r_hi
q_bound=F(464,10**11)
require(q_hi<q_bound,'exact rational native n20 Golden rare-anchor probability bound')
y=F(K)*q_bound/(1-q_bound)
poly=1-y+y*y/2-y**3/6
require(y<F(465,1000) and W*poly>160,'EXACT rational Taylor alternating enclosure >160')

mesh=[]
for L in (4,8,16,32):
 W=L**4
 delta=9/L**3
 # Exactly owned refinement n(L), and genuine a(n) Binet limit.
 n=64*math.ceil(math.log(L,1/p))+128
 a2=2*p**3*((1/p)-(-1)**(n+1)*p**(2*n+1))/math.sqrt(5)
 require(.34<a2<.35 and delta<.15,'original PF C2 schedule and positivity')
 km=W/(a2*r)*math.log(W)
 # A near-regular max-probability click envelope bounds all W rare terms.
 qmax=a2*(1+delta)*r/W
 for frac in (.1,.5,1.0):
  kk=max(1,round(frac*km))
  lo=W*math.exp(kk*math.log1p(-qmax))
  ub=(2*W+1)*math.exp(-kk*a2*(1-delta)*r/W)
  require(lo>=0 and ub>=lo,'genuine PF lower/upper native expected-clock gap')
 mesh.append(dict(L=L,W=W,n=n,a=a2,
   K_mean_clock_logW_threshold=km,
   K_C1_sufficient_with_loglog_plus5=W/(a2*r)*(math.log(W)+math.log(math.log(W))+5)))

# Sharp uniform PF scaling on a pure equal-weight original report chart:
for W in (256,4096,65536):
 aa=.34164078649987384
 rr=r
 for c in (0,1,2,5):
  kk=round(W/(aa*rr)*(math.log(W)+c))
  x=aa*rr/W
  gap=W*math.exp(kk*math.log1p(-x))
  derivative=kk*aa*math.exp((kk-1)*math.log1p(-x))
  if W>=4096:
   require(abs(gap-math.exp(-c))/math.exp(-c)<1e-3,
           'absolute native clock error coupon-cover threshold')
   require(abs(derivative/((math.log(W)+c)*math.exp(-c)/rr)-1)<1e-3,
           'native CLOCK FIRST SOURCE has an extra loglogW requirement')

print(json.dumps(dict(status='PASS',checks=checks,exact_scope='Fraction addressed occupation/capped source',
 native_n20=dict(a=a,K=K,max_site_count=78,N=10946,rare_q_max=qmax_native,
 lower_bound_expected_trials_missing=lower,rigorous_rational_lower=160),
 native_mesh_thresholds=mesh,
 physical_Book03_selected=False,GR_closed=False),indent=2))
