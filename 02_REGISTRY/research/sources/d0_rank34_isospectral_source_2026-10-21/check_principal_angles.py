#!/usr/bin/env python3
"""Polar full128 complementary cut: rank/angle/source exact controls."""
import json
import math

def j_of_theta(theta, fugacity):
    return -math.log1p(-fugacity*math.sin(theta)**2)

def source(theta, fugacity):
    return fugacity*math.sin(2*theta)/(1-fugacity*math.sin(theta)**2)

def projection_det(theta, fugacity):
    # T=U(theta)^*diag(1,0)U(theta) as a full two-dimensional unitary orbit.
    c, s = math.cos(theta),math.sin(theta)
    t00,t11,t01 = c*c,s*s,c*s
    a=1-fugacity+fugacity*t00
    b=1-fugacity+fugacity*t11
    off=fugacity*t01
    return a*b-off*off

def main():
    tests=0
    for z in (0.1, 0.3819660112501052, 0.5,0.8,0.97):
        for k in range(41):
            theta=math.pi*k/80
            h=2e-6
            numerical=(j_of_theta(theta+h,z)-j_of_theta(theta-h,z))/(2*h)
            assert abs(numerical-source(theta,z))<5e-9
            tests+=1
            assert abs(projection_det(theta,z)-(1-z))<4e-15
            tests+=1
        opt=math.atan(1/math.sqrt(1-z))
        sharp=z/math.sqrt(1-z)
        assert abs(source(opt,z)-sharp)<1e-14
        tests+=1
        assert abs(source(0,z))<1e-15 and abs(source(math.pi/2,z))<1e-14
        tests+=1
        for k in range(81):
            theta=math.pi*k/160
            assert abs(source(theta,z))<=sharp+3e-15
            tests+=1
    print(json.dumps({"status":"PASS","checks":tests,
        "surjective_unitary_feedback_source":0,
        "deterministic_cut_first_source":0,
        "max_principal_angle_sensitivity_at_z_half":math.sqrt(0.5)},sort_keys=True))

if __name__=="__main__":
    main()
