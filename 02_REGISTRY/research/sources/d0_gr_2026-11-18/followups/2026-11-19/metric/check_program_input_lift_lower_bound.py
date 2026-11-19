"""Selector-only trace-norm lift: sharp one-copy and explicit product family.

This checks mathematical state families; it does not construct a native
continuous programme-state preparation or its Book03 work/clock.
"""
import itertools
import json
import math
import numpy as np
import mpmath as mp
mp.mp.dps=80
p=(mp.sqrt(5)-1)/2;r=p*p
rng=np.random.default_rng(42021)

def hermitian(n):
    z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));x=(z+z.conj().T)/2
    return x-np.trace(x)*np.eye(n)/n

def trnorm(x):return float(np.abs(np.linalg.eigvalsh(x)).sum())

def pure_vec(t):return np.array([math.sqrt(1-t),math.sqrt(t)])
def pure_der(t):return np.array([-1/(2*math.sqrt(1-t)),1/(2*math.sqrt(t))])
def kron_all(xs):
    out=np.array([1.])
    for x in xs:out=np.kron(out,x)
    return out

def prod_derivative(ts,dts):
    psi=kron_all([pure_vec(t) for t in ts]);dpsi=np.zeros_like(psi)
    for i in range(len(ts)):
        vec=[pure_der(t) if j==i else pure_vec(t) for j,t in enumerate(ts)]
        dpsi+=dts[i]*kron_all(vec)
    return psi,dpsi

# Full selector plus arbitrary 3-dimensional old RIGHT; all traceless
# Hermitian directions, not only diagonal classical programme variations.
N=8;delta=float(p**(N+1));P=np.kron(np.diag([0.,1.]),np.eye(3))
ratios=[]
for _ in range(300):
    X=hermitian(6);slope=delta*float(np.trace(P@X).real)
    ratio=abs(slope)/(delta*trnorm(X)/2);assert ratio<=1+1e-13;ratios.append(ratio)

# Two programme bits, one copy per descriptor, maximally mixed interior.
# u and v are descriptor increments; units carry 1/delta.
Xs=np.diag([-1.,-1.,1.,1.])/(2*delta)
Xt=np.diag([-1.,1.,-1.,1.])/(2*delta)
Ps=np.diag([0.,0.,1.,1.]);Pt=np.diag([0.,1.,0.,1.])
assert abs(delta*np.trace(Ps@Xs)-1)<1e-14 and abs(np.trace(Pt@Xs))<1e-14
assert abs(delta*np.trace(Pt@Xt)-1)<1e-14 and abs(np.trace(Ps@Xt))<1e-14
for angle in np.linspace(0,2*math.pi,1001):
    a,b=math.cos(angle),math.sin(angle)
    assert abs(trnorm(a*Xs+b*Xt)-2*max(abs(a),abs(b))/delta)<1e-11

# The input is a PRODUCT of independent freshly prepared pure selector
# programmes; all m programs for each material leg vary together, never by
# copying an unknown quantum input. Analytic norm 2 sqrt(m)/delta at midpoint.
for m in (1,2,3,4):
    for angle in (0.,.37,1.1):
        a,b=math.cos(angle),math.sin(angle)
        psi,dpsi=prod_derivative([.5]*(2*m),[a/delta]*m+[b/delta]*m)
        inner=np.vdot(psi,dpsi)
        pure_tangent_norm=2*math.sqrt(max(0.,np.vdot(dpsi,dpsi).real-abs(inner)**2))
        assert abs(pure_tangent_norm-(2*math.sqrt(m)/delta))<1e-10
        if m<=2:
            X=np.outer(dpsi,psi.conj())+np.outer(psi,dpsi.conj())
            assert abs(trnorm(X)-pure_tangent_norm)<1e-10

# Product selector inputs give an independent descriptor distribution when
# all programme, seed and union-record factors are subsequently traced/summed.
# At each selector t=1/2, q=r+delta/2.
q=float(r)+delta/2
for bits in itertools.product((0,1),repeat=3):
    expected=math.prod(q if bit else 1-q for bit in bits)
    matrices=[np.diag([1-float(r),1-float(r)-delta]) if bit==0
              else np.diag([float(r),float(r)+delta]) for bit in bits]
    rho=np.outer(kron_all([pure_vec(.5)]*3),kron_all([pure_vec(.5)]*3))
    joint=np.trace(kron_all(matrices)@rho).real
    assert abs(joint-expected)<1e-14

# In the site's mean-field norm, J*J/A^2 has the exact Gram of the owner.
pf=float(p);rf=float(r);z=rf+delta/2;B=1-2*z+2*z*z;c=(2*z-1)**2
A=pf*math.sin(712*math.asin(pf));G=A*A*np.array([[2*B,c],[c,2*B]])
Ginv=np.linalg.inv(G)
field_norm_lower_coefficient=2*math.sqrt(Ginv[0,0])
assert abs(field_norm_lower_coefficient-(2/A)*math.sqrt(2*B/(1+2*c)))<1e-10
assert field_norm_lower_coefficient >= (2/A)*math.sqrt(2/3)

examples=[]
for n in (2,8,20,40):
    d=p**(n+1)
    examples.append({'N':n,'delta':mp.nstr(d,20),'selector_only_lift_lower':mp.nstr(2/d,20),
        'fresh_pure_program_product_m16_lift_norm':mp.nstr(8/d,20)})
print(json.dumps({'status':'PASS','full_RIGHT_random_traceless_tests':len(ratios),
 'max_sample_inequality_ratio':max(ratios),
 'input_effect':'r I + delta P_1','selector_only_min_trace_norm_for_Dq_one':'2/delta',
 'one_copy_two_parameter_operator_norm_exact':'2/delta',
 'm_independent_pure_programs_per_parameter_midpoint_norm':'2 sqrt(m)/delta',
 'm16_product_program_norm':'8/delta',
 'mathematical_material_field_trace_lift_lower':'(2/A_star/delta)*sqrt(2B(z)/(1+2(2z-1)^2)), z=r+delta/2',
 'field_lift_lower_coefficient_before_1_over_delta':field_norm_lower_coefficient,
 'pure_selector_endpoints_two_sided_Dq':0,
 'independent_product_outputs_verified_m3':True,'examples':examples,
 'continuous_native_program_preparation_admitted_or_paid':False,
 'other_seed_or_geometry_variations_covered':False,'GR_closed':False},indent=2))
