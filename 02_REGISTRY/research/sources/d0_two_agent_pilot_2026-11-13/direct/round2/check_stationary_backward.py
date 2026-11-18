"""Exact stationary spectrum plus numerical full-bank hostile controls.

Numerical controls are diagnostics, not physical native admissibility proofs.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import sys
import numpy as np
import sympy as S

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
NATIVE = REPO / '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
PIN = '222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c'
if hashlib.sha256(NATIVE.read_bytes()).hexdigest() != PIN:
    raise RuntimeError('native source pin mismatch')
spec = importlib.util.spec_from_file_location('stationary_native', NATIVE)
nt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = nt
spec.loader.exec_module(nt)
checks = []

def need(ok, name, kind='exact'):
    if not bool(ok):
        raise AssertionError(name)
    checks.append({'name': name, 'kind': kind})

def eq(x, y, name):
    need(S.simplify(x-y) == 0, name)

p, a, G, field = nt.P, nt.A, nt.G_LOCAL, nt.GOLDEN_FIELD
v, zero = S.Matrix([a,p]), S.Matrix([1,0])
K = [S.diag(a,p), S.diag(p,a)]
mus = [p**8+p**12,p**12]
kappa = p+2*a*p**3
def coeff(ref, tau):
    return kappa**2 * sum(mu*(ref*K[f]*tau)[0]**2 /
                         (K[f]*tau).dot(K[f]*tau)
                         for f,mu in enumerate(mus))
H0 = [mus[0]*coeff(v.T,zero), mus[0]*coeff(v.T,G**2*zero)]
H1 = mus[1]*coeff(a*zero.T,G.T**2*zero)
u,d = (a+p)/2,(a-p)/2
eq(u*u+d*d, S.Rational(1,2), 'NPS branch norm constant')
eq(2*u*d, p**3/2, 'NPS branch norm event coefficient')
eq(u*u-d*d, a*p, 'NPS cross-Gram is ap identity')
eq(a*a*p*p, p**3, 'normalized overlap square numerator')

lo,hi = Q(786151377757,10**12),Q(786151377758,10**12)
poly = lambda x:x**4+x*x-1
need(poly(lo)<0<poly(hi), 'exact Golden root bracket')
def mul(x,y):
    products = [xx*yy for xx in x for yy in y]
    return min(products),max(products)
def bounds(expr):
    acc = Q(0),Q(0)
    for c in field.from_sympy(S.cancel(expr)).to_list():
        w = Q(int(c.numerator),int(c.denominator))
        m = mul(acc,(lo,hi))
        acc = m[0]+w,m[1]+w
    return acc
c0 = 1-12*p**7
need(bounds(c0)[0]>0, 'actual H1 collar has positive c0')
for i,h0 in enumerate(H0):
    need(bounds(p*h0-p*p*H1)[0]>0, f'word {i}: alpha > beta')
    need(bounds(1-p*h0-p*p*H1)[0]>0, f'word {i}: T < 1')

al,be,xi,q,s,z,t = S.symbols('alpha beta xi q s z t', positive=True)
M = S.Matrix([[al+be*xi**2,be*xi*S.sqrt(1-xi**2)],
              [be*xi*S.sqrt(1-xi**2),be*(1-xi**2)]])
eq(S.trace(M),al+be,'stationary block trace')
eq(M.det(),al*be*(1-xi**2),'stationary block determinant')
D = S.sqrt((al-be)**2+4*al*be*s/(q*(1-q)))
lp,lm = (al+be+D)/2,(al+be-D)/2
eq(lp+lm,al+be,'two eigenvalues trace')
eq(lp*lm,al*be*(1-s/(q*(1-q))),'two eigenvalues determinant')
dlam = -al*be*s*(1-2*q)/(D*q*q*(1-q)**2)
eq(S.diff(lp,q),dlam,'derivative of optimized upper eigenvalue')
df = z*al*be*s*(1-2*q)/((1-z+z*lp)*D*q*q*(1-q)**2)
eq(S.diff(-S.log(1-z+z*lp),q),df,'optimized marked source')
eq(dlam.subs(q,S.Rational(1,2)),0,'endpoint gain vanishes')
la,mu = S.symbols('lambda mu',positive=True)
ray = la*S.cos(t)**2+mu*S.sin(t)**2
eq(S.diff(-S.log(1-z+z*ray),t,2).subs(t,0),
   2*z*(la-mu)/(1-z+z*la),'transverse backward Hessian')

# The spectral statements above are exact; these controls keep all r=4
# columns, extra bank directions, and an off-diagonal complex E variation.
pn = float(p)
sn = pn**3
r = 4
qs = pn**2+sn*np.array([0.02,0.06,0.10,0.14])
xivals = np.sqrt(sn/(qs*(1-qs)))
V0 = np.vstack([np.eye(r),np.zeros((r,r)),np.zeros((2,r))])
V1 = np.vstack([np.diag(xivals),np.diag(np.sqrt(1-xivals*xivals)),np.zeros((2,r))])
zn = 0.6
rng = np.random.default_rng(20261113)
diagnostics = []
for i,h0 in enumerate(H0):
    an,bn = float(p*h0),float(p*p*H1)
    mat = an*V0@V0.T+bn*V1@V1.T
    vals,vecs = np.linalg.eigh(mat)
    chi = vecs[:,-r:]
    upper = (an+bn+np.sqrt((an-bn)**2+4*an*bn*sn/(qs*(1-qs))))/2
    need(np.max(abs(np.sort(upper)-vals[-r:]))<1e-17,
         f'word {i}: full bank spectrum including unused dimensions','numerical')
    need(np.linalg.norm((np.eye(10)-chi@chi.T)@mat@chi)<1e-17,
         f'word {i}: all backward tangent rows vanish','numerical')
    opt = -np.linalg.slogdet((1-zn)*np.eye(r)+zn*chi.T@mat@chi)[1]
    probe,_ = np.linalg.qr(rng.normal(size=(10,r)))
    probej = -np.linalg.slogdet((1-zn)*np.eye(r)+zn*probe.T@mat@probe)[1]
    need(probej > opt, f'word {i}: random full-bank competitor exceeds optimum','numerical')
    # Independently adjustable branch recoveries would align both ranges,
    # giving T I and a different, q-independent optimum.
    split = -r*np.log(1-zn+zn*(an+bn))
    need(split < opt, f'word {i}: split-recovery differs from common backward','numerical')
    eq0 = np.diag(qs).astype(complex)
    delta = rng.normal(size=(r,r))+1j*rng.normal(size=(r,r))
    delta = (delta+delta.conj().T)/2
    def spectral_j(e):
        w = np.linalg.eigvalsh(e)
        l = (an+bn+np.sqrt((an-bn)**2+4*an*bn*sn/(w*(1-w))))/2
        return -np.log(1-zn+zn*l).sum()
    gap = np.sqrt((an-bn)**2+4*an*bn*sn/(qs*(1-qs)))
    fp = zn*an*bn*sn*(1-2*qs)/((1-zn+zn*upper)*gap*qs**2*(1-qs)**2)
    expected = float(np.real(np.trace(np.diag(fp)@delta)))
    step = 1e-5
    finite = (spectral_j(eq0+step*delta)-spectral_j(eq0-step*delta))/(2*step)
    need(abs(finite-expected)<5e-10,
         f'word {i}: noncommuting complex source variation','numerical')
    lower = float(16*zn*p*h0*p*p*H1*p**6*c0/(p*h0+p*p*H1))
    need(fp.min()>lower>0, f'word {i}: H1 gain lower bound diagnostic','numerical')
    diagnostics.append({'word':i,'alpha':an,'beta':bn,
                        'source_lower_per_root_at_z_0_6':lower,
                        'noncommuting_source_error':abs(finite-expected)})

out = {'status':'PASS','checks':checks,
       'exact_checks':sum(c['kind']=='exact' for c in checks),
       'numerical_diagnostics':sum(c['kind']=='numerical' for c in checks),
       'diagnostics':diagnostics,'baseline':'dc411daf01f697ec85dd22f28bfe124171796645',
       'native_sha256':PIN,
       'proof_sha256':hashlib.sha256((HERE/'STATIONARY_BACKWARD_RU.md').read_bytes()).hexdigest(),
       'scope':{'mathematical_common_backward_stationarity':True,
                'physical_fibre_admissibility':False,'full_heat_stationarity':False,
                'Cost_Info_binding':False,'GR_closed':False}}
(HERE/'STATIONARY_CHECK.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','exact_checks','numerical_diagnostics','diagnostics']},ensure_ascii=False))
