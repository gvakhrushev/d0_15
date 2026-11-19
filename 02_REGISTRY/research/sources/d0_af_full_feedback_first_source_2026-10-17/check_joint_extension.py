#!/usr/bin/env python3
"""Exact controls for the analytic joint-critical factorization in RESULT_RU.md.
These tests do not claim physical D0 admission or existence of curved roots.
"""
import json
import sympy as s

def run():
    names = []
    def eq(name, expr):
        if s.cancel(expr) != 0:
            raise ArithmeticError(name)
        names.append(name)
    e, b, z, c, x = s.symbols('e b z c x')
    K = 1-z+z*(1-e)*(1-b)
    zp = z*(1-e)/(1-z*e)
    eq('exact_same_program_refactorization', K-(1-z*e)*(1-zp*b))
    eq('derived_fugacity_jet', s.diff(zp,e)+z*(1-z)/(1-z*e)**2)
    eq('hidden_compensation_preserves_joint_price',
       K.subs(b,1-c/(1-e))-(1-z+z*c))
    eq('hidden_compensation_removes_source',
       s.diff(K.subs(b,1-c/(1-e)),e))
    # A genuinely mixed smooth price; its coefficient varies along scene state.
    # f(q)=r^2*k with an independent radial direction 2r*d/dr / 2.
    r,k,y,t = s.symbols('r k y t', real=True)
    f=r*r*k
    Phi = (1+y*y)*f + t*t*f*f
    # Keep the actual baseline as one independent scene functional K0(y).
    K0=(y-2)**2
    total = Phi+K0
    eq('local_radial_equation',r*s.diff(total,r)-2*f*(1+y*y+2*t*t*f))
    eq('joint_scene_row_at_vacuum',s.diff(total,y).subs(k,0)-s.diff(K0,y))
    eq('joint_link_row_at_vacuum',s.diff(total,k).subs(k,0)-(1+y*y)*r*r)
    # Nonzero f=0 alone is not sufficient: the link row stays nonzero.
    if s.diff(total,k).subs({k:0,r:1,y:2}) != 5:
        raise ArithmeticError('remaining_link_row_was_deleted')
    names.append('remaining_link_row_cannot_be_deleted')
    # Distinct illustration with actual nonempty critical geometry f=r^2*k^2.
    ff=r*r*k*k
    AA=(1+y*y)*ff+t*t*ff*ff+K0
    for var in (r,k,y):
        eq('nonempty_product_control_'+str(var),s.diff(AA,var).subs({k:0,y:2}))
    print(json.dumps({'status':'PASS_SCOPED_JOINT_EXTENSION','checks':len(names),
                      'check_names':names,'physical_GR_closed':False},sort_keys=True,indent=2))

if __name__ == '__main__':
    run()
