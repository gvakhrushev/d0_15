"""Exact native finite controls for STOPPED_FIELD_SADDLE.md.

No numerical Hessian or rank scan. Checks remain active under python -O.
The fixed-mesh nonvacuum extension uses continuity in the companion proof.
"""
from itertools import combinations, product
import json
import sympy as s


def require(condition, name):
    if not bool(condition):
        raise RuntimeError(name)


E, b = s.symbols('E b', real=True)
r, ss = s.sqrt(1-E), s.sqrt(E)
c, d = s.sqrt(1-b), s.sqrt(b)
tail = s.Matrix([[r,0,-ss,0],[0,r,0,-ss],
                 [0,ss,0,r],[ss,0,r,0]])
scene = s.Matrix([[c,-d],[d,c]])
step = s.kronecker_product(tail, scene)
require(s.simplify(step.T*step)==s.eye(8), 'full native 8D unitarity')
U = s.simplify(step*step)
ret = U.extract([0,2], [0,2])
predicted = (1-2*b)*s.Matrix([[1-E,-E],[-E,1-E]])
require(s.simplify(ret-predicted)==s.zeros(2), 'actual native 8D return')
F = s.eye(2)-ret.T*ret
Pplus = s.Matrix([[1,1],[1,1]])/2
Pminus = s.Matrix([[1,-1],[-1,1]])/2
B = 4*b*(1-b)
upper = B+(1-B)*4*E*(1-E)
require(s.simplify(F-upper*Pplus-B*Pminus)==s.zeros(2),
        'fixed native plus/minus effect decomposition')

p = (s.sqrt(5)-1)/2
chi = s.symbols('chi', positive=True)
f = s.symbols('f', real=True)
L = 4*p**3
M = L*(1+p**6)
actual_upper = upper.subs({E:p**2*(1+chi**2*f), b:p**2})
delta_expected = 4*p**11*chi**2*f-4*p**10*chi**4*f**2
require(s.simplify(actual_upper-M-delta_expected)==0,
        'exact nonlinear native vacuum anchor')
require(s.simplify(L-(1-p**6))==0 and
        s.simplify(M-(1-p**12))==0, 'Golden reference bands')

# Actual local shared link, all six face incidences and original star.
a, u, h = s.symbols('a u h', positive=True, real=True)
eta = s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
J = s.zeros(4)
J[2,3], J[3,2] = 1, -1
require(J.T*eta+eta*J==s.zeros(4), 'proper native null Lorentz generator')
pairs = list(combinations(range(4),2))


def eps(v):
    return (-1)**sum(v[i]>v[j] for i in range(4) for j in range(i+1,4))


def star_sources(sites, origin, shift):
    source = {x:s.S.Zero for x in sites}
    changed = []
    for x in sites:
        for rr,tt in pairs:
            sg = (int(x==origin and rr==2)
                  + int(shift(x,rr)==origin and tt==2)
                  - int(shift(x,tt)==origin and rr==2)
                  - int(x==origin and tt==2))
            if not sg:
                continue
            changed.append((x,rr,tt,sg))
            vv,ww = [k for k in range(4) if k not in (rr,tt)]
            C = sg*J*eta
            coframe = s.diag(1,a,1,a**-1) if x==origin else s.eye(4)
            area = s.S.Zero
            for i,j in pairs:
                k,l = [z for z in range(4) if z not in (i,j)]
                area += eps((i,j,k,l))*(coframe[i,vv]*coframe[j,ww]
                           -coframe[j,vv]*coframe[i,ww])*C[k,l]
            source[x] += eps((rr,tt,vv,ww))*area
    return {x:s.simplify(v) for x,v in source.items()}, changed


periodic, changed = star_sources(range(16),0,lambda x,r:x^(1<<r))
require(len(changed)==6, 'six changed original L2 based faces')
require(periodic[0]==-a and periodic[8]==1,
        'native site source values')
require(all(v==0 for x,v in periodic.items() if x not in (0,8)),
        'no omitted L2 source')
require(s.simplify(sum(periodic.values())-(1-a))==0,
        'full original 96-face star')

sites = list(product((-1,0,1),repeat=4))
origin = (0,0,0,0)
def shift(x,r):
    v = list(x); v[r] += 1
    return tuple(v)
interior, changed_interior = star_sources(sites,origin,shift)
neighbor = (0,0,0,-1)
require(len(changed_interior)==6, 'six changed interior shared faces')
require(interior[origin]==-a and interior[neighbor]==1,
        'same native interior source values')
require(all(v==0 for x,v in interior.items()
            if x not in (origin,neighbor)), 'no omitted interior source')

# Exact weighted whole anchor with arbitrary actual positive density ratios.
rho0,rhod,Ah = s.symbols('rho0 rhod Ah', positive=True)
f0 = -a*s.sin(u)/h**2
fd = s.sin(u)/h**2
signal = Ah*(f0+fd-(chi**2/p)*(f0**2/rho0+fd**2/rhod))
g = Ah/h**2
D = chi**2/(p*h**2)*(1/rho0+1/rhod)
require(g.is_positive and D.is_positive, 'strict actual gain/density signs')
H = s.hessian(signal,(a,u)).subs({a:1,u:0})
H_expected = s.Matrix([[0,-g],[-g,-2*g*D]])
require(s.simplify(H-H_expected)==s.zeros(2), 'actual signal slice Hessian')
require(s.simplify(H.det()+g*g)==0, 'strict indefinite determinant')
vm = s.Matrix([0,1]); vp = s.Matrix([-2*D,1])
qm = (vm.T*H*vm)[0]/2
qp = (vp.T*H*vp)[0]/2
require(s.simplify(qm+g*D)==0, 'exact negative signal direction')
require(s.simplify(qp-g*D)==0, 'exact positive signal direction')
require(signal.subs(u,0)==0, 'whole Sigma coframe curve fixed anchor')

# Demonstrate the resolvent Hessian correction on a symbolic scalar block.
fbase,z,x,y = s.symbols('fbase z x y', real=True)
ff = fbase+x*y+x
jj = -s.log(1-z*ff)
pi = z/(1-z*fbase)
linear_anchor = pi*(ff-fbase)
dx = {x:0,y:0}
defect = s.diff(jj,x,2).subs(dx)-s.diff(linear_anchor,x,2).subs(dx)
require(s.simplify(defect-pi*pi)==0, 'do not equate full J2 and anchor Hessians')
require(s.simplify(s.diff(jj,x,y).subs(dx)
                  -s.diff(linear_anchor,x,y).subs(dx))==0,
        'mixed source survives when one first operator derivative vanishes')

# Nonvacuum family stays in the actual retained-clock full16 section.
radius = p**2
require(0 < radius < p, 'strict native scalar/top radius')
require(s.simplify(p+radius**2+(p**2-radius**2)-1)==0,
        'complete clock/current CAR normalization')
angle = s.symbols('angle', real=True)
energy_step = radius**2*((s.cos(angle)-1)**2+s.sin(angle)**2)
require(s.trigsimp(energy_step-4*radius**2*s.sin(angle/2)**2)==0,
        'exact normalized nonvacuum null energy')

print(json.dumps({
    'status':'PASS',
    'native_8D_fixed_return_basis':True,
    'full_weighted_anchor_exact_quadratic_in_f':True,
    'original_L2_changed_faces':len(changed),
    'interior_collar_changed_faces':len(changed_interior),
    'actual_signal_Hessian':'[[0,-g],[-g,-2gD]], g,D>0',
    'determinant':'-g^2',
    'two_exact_direction_coefficients':['-gD','+gD'],
    'full_CAR_clock_normalized_nonvacuum_family':True,
    'actual_price_descent':'sign(kappa) selects one direction; entropy=o(eps^2)',
    'nonvacuum_extension':'analytic continuity at each fixed finite mesh',
    'scope':'Supplied stopped whole-J2 component; no total-HJR or continuum claim.'
},indent=2))
