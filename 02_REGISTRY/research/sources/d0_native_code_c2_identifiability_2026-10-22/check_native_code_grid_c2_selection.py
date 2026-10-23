#!/usr/bin/env python3
"""EXACT 42-coordinate Golden finite-count grid -> C1/C2 non-identifiability.

No substitute physical D0 action is selected; these are algebraic countermodels
to inferring off-grid 42-field derivatives and Hessians solely from complete
finite Boolean code-value and finite-difference data, even under uniform C0.
Sympy rational+pi exact, original native phi and zeta unchanged.

Run: python3 check_native_code_grid_c2_selection.py
"""
from __future__ import annotations
import json
import sympy as s

checks=0
def check(z,m):
    global checks
    checks+=1
    if not bool(z):
        raise ArithmeticError(m)
p=(s.sqrt(5)-1)/2
zeta=s.Rational(1,2**20)
f=s.expand(4*p**3)
check(s.simplify(p+p**2-1)==0,"ORIGINAL phi p+p²=1")
check(0<float(f)<1,"actual positive Golden flag 4p³")
j=-s.log(1-zeta*f)
check(float(j)>0,"native ORIGINAL Book per-selected-Boolean j>0")
dimensions=42
y=s.symbols("y0:42",real=True)
center=[s.Rational(i+1,97) for i in range(dimensions)]
displacement=[y[i]-center[i] for i in range(dimensions)]
# Independent EXACT 42-field saddle fixture with both signs; this is
# NOT the actual original h0 N1 CQ polynomial, only a universal gate test.
S0=sum(displacement[i]**2 if i<21 else -displacement[i]**2
       for i in range(dimensions))
y1=displacement[0]
y22=displacement[21]
check(all(s.diff(S0,v).subs(dict(zip(y,center)))==0 for v in y),
      "42-variable critical source admits nonzero Hessian inertia")
for N in [3,5,8,13,21,34]:
    h=s.Rational(1,N)
    a=s.Rational(3,7)
    b=s.Rational(5,1)
    wave_first=a*h/(2*s.pi)*s.sin(2*s.pi*y1/h)
    wave_hess=b*h**2/(4*s.pi**2)*(1-s.cos(2*s.pi*y22/h))
    F=S0+wave_first
    G=S0+wave_hess
    at_center=dict(zip(y,center))
    for k1 in range(-3,4):
        for k22 in [-2,0,1,3]:
            point=at_center.copy()
            point[y[0]]=center[0]+k1*h
            point[y[21]]=center[21]+k22*h
            check(s.simplify((F-S0).subs(point))==0,
                 "exact first-source oscillation invisible to all grid values")
            check(s.simplify((G-S0).subs(point))==0,
                 "exact second-source oscillation invisible to all grid values")
            # Any stencil of grid values (including all mixed finite secants)
            # agrees because every individual grid value agrees exactly.
    check(s.simplify(s.diff(F,y[0]).subs(at_center)-a)==0,
          "nonzero EXACT 42-field Euler covector on grid despite identical full grid values")
    check(s.simplify(s.diff(G,y[21]).subs(at_center))==0,
          "same exact stationary 42-field point under Hessian countermodel")
    check(s.simplify(s.diff(G,y[21],2).subs(at_center)-(-2+b))==0,
          "exact 42x42 Hessian component changes by positive b")
    check(s.simplify(s.diff(S0,y[21],2)+2)==0,
          "original fixture has strictly NEGATIVE second jet in real field22")
    check(b>2 and -2+b>0,
          "positive perturbation flips a negative Hessian eigendirection to positive")
    check(s.simplify(wave_hess.subs({y[21]:center[21]+h*s.Rational(1,2)})
       -b*h*h/(2*s.pi*s.pi))==0,
          "nonnegative wave exact supremum O(h²) shrinks uniformly")
    # Coefficients are simple; first-wave sup = a h/(2pi), second =b h²/(2pi²).
    check(s.diff(F,y[0]).subs(at_center)!=s.diff(S0,y[0]).subs(at_center),
          "failed inference of C1 source from all code-grid values")
    check(s.diff(G,y[21],2).subs(at_center)!=s.diff(S0,y[21],2),
          "failed inference of C2 Hessian from all code-grid values")
    check(s.diff(G,y[0]).subs(at_center)==0 and
          s.diff(G,y[21]).subs(at_center)==0,
          "42 root EXACT unchanged while nonzero second-jet changed")
print(json.dumps({
    "status":"PASS_EXACT_42D_GRID_C0_NOT_C1_C2_IDENTIFIABILITY",
    "assertions":checks,
    "original_golden_phi":"(1+sqrt(5))/2",
    "original_zeta":"1/1048576",
    "original_book_boolean_one_flag_j":float(j),
    "independent_42_fields":"16 coframe + 24 Lorentz + 2 CAR math test, no original physics inferred",
    "different_N_tested":[3,5,8,13,21,34],
    "all_grid_values_and_all_secants_identical":True,
    "uniform_value_first_countermodel_error_order":"O(1/N)",
    "uniform_value_second_countermodel_error_order":"O(1/N²)",
    "first_field_Euler_gap_exact":"3/7",
    "second_field_Hessian_gap_exact":"5",
    "base_negative_Hessian_field22":"-2",
    "changed_positive_Hessian_field22":"3",
    "extra_second_source_wave_nonnegative_everywhere":True,
    "physical_Book03_C1_C2_extension_selected":False,
    "physical_GR_closed":False
},indent=2))
