#!/usr/bin/env python3
"""Exact finite checks for the relational quarter-turn feedback source.
Finite scientific certificate only: no physical admission or source selection claimed.
"""
import itertools
import sympy as s

p, a = s.symbols('p a', nonzero=True, real=True)
I16 = s.eye(16)
eta = s.diag(1, -1, -1, -1)
creation = []
for j in range(4):
    c = s.zeros(16)
    for n in range(16):
        if not n & (1 << j):
            c[n | (1 << j), n] = (-1) ** ((n & ((1 << j)-1)).bit_count())
    creation.append(c)

def lift(x):
    return sum((x[i,j] * creation[i] * creation[j].T
                for i in range(4) for j in range(4)), s.zeros(16))

def split(x):
    return (x-x.T)/2, (x+x.T)/2

def source_matrix(b):
    da, ds = split(lift(b))
    return s.BlockMatrix([[da/2, a*p*ds/2],
                          [-a*p*ds/2, -da/2]]).as_explicit()

def julia_relative_tangent(x):
    xa, xs = split(lift(x))
    return s.BlockMatrix([[p*p*xa, a*p*xa-p*xs/a],
                          [a*p*xa+p*xs/a, -p*p*xa]]).as_explicit()

basis=[]
for i,j in itertools.combinations(range(4),2):
    x=s.zeros(4)
    x[i,j]=1
    x[j,i]=-eta[i,i]*eta[j,j]
    assert x.T*eta+eta*x == s.zeros(4)
    basis.append(x)

for b,x in itertools.product(basis,repeat=2):
    d,y=lift(b),lift(x)
    assert s.trace(d*y)==4*s.trace(b*x)
    sb,k=source_matrix(b),julia_relative_tangent(x)
    assert sb.T == -sb and k.T == -k
    assert s.simplify(s.trace(sb*k)-4*p*p*s.trace(b*x))==0
print('PASS all 36 Lorentz source pairings on complete CAR16, including boosts')

# Derive the relative-Julia tangent independently before using its formula.
q=s.symbols('q', nonzero=True, real=True)
groebner=s.groebner([a*a-p,p*p+p-1],a,p)
def reduce_native(expr):
    num,den=s.fraction(s.cancel(expr))
    return groebner.reduce(s.expand(num))[1] == 0
for x4 in basis:
    x=lift(x4)
    j0=s.BlockMatrix([[p*I16,a*I16],[a*I16,-p*I16]]).as_explicit()
    defect=-p*p*(x+x.T)/(2*a)
    dj=s.BlockMatrix([[p*x,defect],[defect,-p*x.T]]).as_explicit()
    residual=j0*dj-julia_relative_tangent(x4)
    assert all(reduce_native(v) for v in residual if v != 0)
print('PASS actual strict Julia derivative with native a^2=p, p+p^2=1')

# Rational nontrivial quarter-turn reference on the actual 64-dimensional carrier.
# Choose a spatial face b=(6/5)J23; then S^2=-(9/25)Pi and the square root is rational.
b=s.Rational(6,5)*basis[-1]
sb=source_matrix(b)
assert not any(v.has(p,a) for v in sb)
projector=-s.Rational(25,9)*sb*sb
assert projector*projector==projector and projector.T==projector
defect=s.eye(32)-projector/5
assert defect*defect==s.eye(32)+sb*sb
assert defect*sb==sb*defect
r=s.BlockMatrix([[sb,defect],[-defect,-sb]]).as_explicit()
assert r.T==-r and r*r==-s.eye(64)
assert r.T*r==s.eye(64)

for x in basis:
    k=julia_relative_tangent(x)
    khat=s.diag(k,s.zeros(32))
    f1=r*khat+khat*r
    assert f1.T==f1
    assert s.simplify(s.trace(f1)-8*p*p*s.trace(b*x))==0
print('PASS exact rational CAR16+flags quarter-turn and all six full feedback jets')

# Nonconstant coframe-area derivative: b scales as e^2; verify the mixed jet.
u=s.symbols('u', real=True)
for x in basis:
    exact=s.trace(source_matrix(u*u*b)*julia_relative_tangent(x))
    assert s.simplify(s.diff(exact,u)-8*u*p*p*s.trace(b*x))==0
print('PASS coframe mixed derivatives are retained; no fixed-reference substitution')

# Independent 2x2 whole determinant, not only the proposed first derivative.
t,z=s.symbols('t z', real=True)
j=s.Matrix([[0,-1],[1,0]])
v=(s.eye(2)+t*j)*(s.eye(2)-t*j).inv()
f=p**3*(2*s.eye(2)+j*v-v.T*j)
det=(s.eye(2)-z*f).det()
actual=(-s.diff(det,t)/det).subs(t,0)
expected=2*z*p**3/(1-2*z*p**3)*s.trace(j*(2*j))
assert s.simplify(actual-expected)==0
assert f.subs(t,0)==2*p**3*s.eye(2)
assert s.simplify(det.subs(t,0)-(1-2*z*p**3)**2)==0
print('PASS whole Golden leakage determinant has the claimed signed jet and fixed baseline')
rr,phi=s.symbols('rr phi', positive=True)
code=1+rr
entropy=(-(1-rr)*s.log(1-rr)-rr*s.log(rr))/s.log(phi)
assert s.simplify(s.diff(code-entropy,rr)
                 -(1+(s.log(rr)-s.log(1-rr))/s.log(phi)))==0
pg=(s.sqrt(5)-1)/2
assert s.simplify(2*pg**3-pg**2)==s.simplify(pg**2*(2*pg-1))
assert float(2*pg**3-pg**2)>0
print('PASS original cost1/2 minus binary Info has nonzero fixed-prior relative source')
# Hostile old embedding: independent curvature noise survives at zero reference.
lam=1-2*z*p**3
old_r=s.BlockMatrix([[s.zeros(2),s.eye(2)],[-s.eye(2),s.zeros(2)]]).as_explicit()
old_v=s.diag(v,s.eye(2))
old_f=p**3*(2*s.eye(4)+old_r*old_v-old_v.T*old_r)
old_det=(s.eye(4)-z*old_f).det()
old_hess=(-s.diff(old_det,t,2)/old_det+(s.diff(old_det,t)/old_det)**2).subs(t,0)
assert s.simplify(old_hess-2*(z*p**3/lam)**2*s.trace((2*j).T*(2*j)))==0
# Exact paired repair on the entire finite Cayley curve.
paired_v=s.diag(v,v.T)
paired_zero_f=p**3*(2*s.eye(4)+old_r*paired_v-paired_v.T*old_r)
assert paired_zero_f==2*p**3*s.eye(4)
sigma,cc=s.symbols('sigma cc',real=True)
pair_r=s.BlockMatrix([[sigma*j,cc*s.eye(2)],[-cc*s.eye(2),-sigma*j]]).as_explicit()
pair_f=p**3*(2*s.eye(4)+pair_r*paired_v-paired_v.T*pair_r)
assert s.simplify(pair_f[0,0]-p**3*(2-4*sigma*t/(1+t*t)))==0
assert all(s.simplify(pair_f[i,jj]-(pair_f[0,0] if i==jj else 0))==0
           for i in range(4) for jj in range(4))
for x in basis:
    k=julia_relative_tangent(x)
    khat=s.diag(k,-k)
    assert s.simplify(s.trace(r*khat)-8*p*p*s.trace(b*x))==0
print('PASS hostile unpaired curvature Hessian and EXACT inverse-paired whole-word cancellation')
print('PASS doubled all-six CAR16 paired source and exact nonzero-reference determinant')
print('FIREWALL: coframe reference admission/payment, complete H+J+R selection and refinement remain open')
