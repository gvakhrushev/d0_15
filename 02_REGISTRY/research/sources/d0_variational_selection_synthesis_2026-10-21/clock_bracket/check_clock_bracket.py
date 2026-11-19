#!/usr/bin/env python3
"""Exact CAR16 lapse-bracket test; kinematics only, no GR selection claim.

Run with sympy available. Native creator order is (0,2,3,1), matching
d0_native_preparation_closure_2026-10-21/inputs/native_input.py.
No assertion statements: python -O runs the same checks.
"""
import json
import sympy as s

x,y,z,h,b = s.symbols('x y z h b', real=True)
xs=(x,y,z)
I=s.I
eye=s.eye(16)
zero=s.zeros(16,1)
checks=[]

def check(ok, name):
    if not bool(ok):
        raise ArithmeticError(name)
    checks.append(name)

def creators():
    order=(0,2,3,1)
    out=[]
    for r in range(4):
        c=s.zeros(16)
        before=order[:order.index(r)]
        for bits in range(16):
            if not ((bits>>r)&1):
                c[bits|(1<<r),bits]=(-1)**sum((bits>>j)&1 for j in before)
        out.append(c)
    return out

cs=creators()
ca=[c.T for c in cs]
for i in range(4):
    for j in range(4):
        check(cs[i]*ca[j]+ca[j]*cs[i]==(eye if i==j else s.zeros(16)),f'CAR {i},{j}')

# Spatial subspace of the original four-mode CAR carrier: no grade removed.
cp=[cs[i] for i in (1,2,3)]
cm=[ca[i] for i in (1,2,3)]
al=[I*(a-d) for a,d in zip(cp,cm)]
for i in range(3):
    check(al[i].H==al[i],f'spatial Clifford self-adjoint {i}')
    for j in range(3):
        check(al[i]*al[j]+al[j]*al[i]==(2*eye if i==j else s.zeros(16)),f'spatial Clifford {i},{j}')

def expand(v): return v.applyfunc(s.expand)
def D(v): return expand(sum((-I*al[i]*v.diff(xs[i]) for i in range(3)),zero))
def H(n,v,a=s.Rational(1,2)):
    return expand(n*D(v)+a*(D(n*v)-n*D(v)))
def DH(v):
    return expand(sum((cp[i]*(v.subs(xs[i],xs[i]+h)-v)/h
                       +cm[i]*(v.subs(xs[i],xs[i]-h)-v)/h for i in range(3)),zero))
def HH(n,v): return expand((n*DH(v)+DH(n*v))/2)

N=1+x*y+z*z
M=2+x*z+y*y
V=[s.expand(N*s.diff(M,t)-M*s.diff(N,t)) for t in xs]
div=sum(s.diff(V[i],xs[i]) for i in range(3))
spin=sum(((al[i]*al[j]-al[j]*al[i])*s.diff(N,xs[i])*s.diff(M,xs[j])/4
          for i in range(3) for j in range(3)),s.zeros(16))
def target(v):
    return expand(-sum((V[i]*v.diff(xs[i]) for i in range(3)),zero)-div*v/2-spin*v)

# Full16 polynomial test vector excites all grades and all spatial derivatives.
f=s.Matrix([(k+1)*x*x*y+(k%3+1)*y*z*z+(k%5-2)*x*z+(k%2)*z+1 for k in range(16)])
comm=expand(H(N,H(M,f))-H(M,H(N,f)))
check(comm==target(f),'exact continuum lapse bracket on all16 polynomial components')
check(spin!=s.zeros(16),'nonzero independent spin rotation retained')
check(expand(comm+sum((V[i]*f.diff(xs[i]) for i in range(3)),zero)+div*f/2)!=zero,
      'deleting the spin rotation fails')
unsym=expand(H(N,H(M,f,0),0)-H(M,H(N,f,0),0))
check(unsym!=target(f),'unsymmetrized ND has extra bivector principal source')

# Symbolic principal coefficient for general ordering a: it is metric-only
# precisely at a=1/2, when the real-lapse operator is self-adjoint.
for j in range(3):
    principal=sum(((al[i]*al[j]-b*(al[i]*al[j]-al[j]*al[i]))*V[i] for i in range(3)),s.zeros(16))
    check(principal.subs(b,s.Rational(1,2)).applyfunc(s.expand)==eye*V[j],f'canonical metric principal coefficient {j}')
check(s.solve(s.Eq(b,1-b),b)==[s.Rational(1,2)],'true-adjoint ordering fixes one-half')

# Exact native one-sided CAR stencil, not a substituted centered derivative.
# Polynomial shift expansion exposes its nonzero O(h) defect and exact limit.
native_comm=expand(HH(N,HH(M,f))-HH(M,HH(N,f)))
defect=expand(native_comm-target(f))
check(defect.subs(h,0)==zero,'native finite stencil has exact continuum bracket limit')
check(defect.diff(h).subs(h,0)!=zero,'actual finite stencil has nonzero first-order defect')
for k in range(16):
    check(s.rem(s.Poly(defect[k],h),s.Poly(h,h))==0,f'finite defect divisible by h component {k}')

# It is a smooth-sector statement, not a uniform operator-norm convergence.
# Native 1D symbol at k=pi/h has size 2/h; the continuum derivative has pi/h.
native_grid_symbol=-2*(cp[0]+cm[0])
continuum_grid_symbol=s.pi*al[0]
check(native_grid_symbol**2==4*eye and continuum_grid_symbol**2==s.pi**2*eye,
      'native and continuum grid-scale squared symbols differ')

# Do not mistake the normal-normal identity for a whole constraint algebra:
# a fixed-frame dilation fails the required shift-normal relation.
def shift_x(v): return expand(x*v.diff(x)+v/2)
shift_defect=expand(shift_x(H(1,f))-H(1,shift_x(f)))
check(shift_defect==expand(I*al[0]*f.diff(x)) and shift_defect!=zero,
      'frozen-frame shift-normal closure fails by explicit nonzero dilation')

# A heat clock has a different differential order even after true-adjoint
# symmetrization. Independent scalar symbolic test extracts the third jet.
nx=s.Function('N')(x); mx=s.Function('M')(x); ff=s.Function('f')(x)
def heat(n,v): return -s.expand((n*s.diff(v,x,2)+s.diff(n*v,x,2))/2)
heat_comm=s.expand(heat(nx,heat(mx,ff))-heat(mx,heat(nx,ff)))
check(s.expand(heat_comm).coeff(s.diff(ff,x,3))==2*(nx*s.diff(mx,x)-mx*s.diff(nx,x)),
      'symmetrized heat clock has nonzero third-order commutator coefficient')

# A genuinely nonscalar constant frame recovers q=E^T E, not a frozen delta.
frame=s.Matrix([[2,1,0],[0,3,1],[1,0,2]])
aq=[sum((frame[a,i]*al[a] for a in range(3)),s.zeros(16)) for i in range(3)]
q=frame.T*frame
for i in range(3):
    for j in range(3):
        check(aq[i]*aq[j]+aq[j]*aq[i]==2*q[i,j]*eye,f'native constant-frame metric symbol {i},{j}')

point={x:s.Rational(1,5),y:s.Rational(2,7),z:s.Rational(-1,4)}
sample=[]
for L in (8,16,32,64):
    vals=[abs(float(t.subs(point).subs(h,s.Rational(1,L)))) for t in defect]
    sample.append({'h':str(s.Rational(1,L)),'max_component':max(vals),'max_component_over_h':L*max(vals)})
out={'scope':'flat spatial CAR16 kinematic bracket and native-stencil smooth consistency only',
     'checks':checks,'passed':len(checks),'sample_defect':sample,
     'physical_normal_clock_admission':False,'full_gravitational_constraint_algebra':False,
     'complete_Book_price_selection':False,'GR_closed':False}
print(json.dumps(out,indent=2))
