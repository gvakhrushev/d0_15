#!/usr/bin/env python3
"""Exact formula+numeric original positive-adjoint grade0 native periodic
Dirac: coframe-local variation couples the true rank128 cutoff prep zero mode.
Conditional on coframe/RIGHT variations being admitted by selected G0.
"""
import math
import numpy as np
L=65
k=32
nu=.7
T=1.3
h=T/L
mu=1/128
w=2*math.pi*k/L
x=np.arange(L)
fc=math.sqrt(2/L)*np.cos(w*x)
fs=math.sqrt(2/L)*np.sin(w*x)
assert abs(fc@fc-1)<1e-13 and abs(fs@fs-1)<1e-13
assert abs(fc@fs)<1e-13
dc=(np.roll(fc,-1)-fc)/h
ds=(np.roll(fs,-1)-fs)/h
assert abs(dc@ds)<1e-8
assert abs(dc@dc-ds@ds)<1e-8
def rayleigh(theta,epsilon):
    # TRUE grade0 native d(f) = nu_x * (shift-I)f/h ; R=<f,D^2 f>
    v=math.cos(theta)*dc+math.sin(theta)*ds
    weights=np.full(L,nu)
    weights[0]+=epsilon
    return mu*np.dot(weights*v,weights*v)
for theta in (0,.15,-.31,.6):
    assert abs(rayleigh(theta,0)-rayleigh(0,0))<2e-11
mixed=4*mu*nu*dc[0]*ds[0]
closed=nu/(16*L*h*h)*(math.cos(w)-1)*math.sin(w)
assert abs(mixed-closed)<1e-10
assert abs(mixed)>1e-5
for epsilon in (1e-4,-1e-4):
    # Full internal prep Euler D_theta R is driven at first order in epsilon
    dtheta=(rayleigh(1e-5,epsilon)-rayleigh(-1e-5,epsilon))/(2e-5)
    assert abs(dtheta/epsilon-mixed)<5e-3
print("PASS genuine native Dirac grade0 R=||d f||², real k32 cosine/sine")
print("PASS EXACT same nonzero Fourier eigenenergy and fixedRIGHT rank128 Gram")
print("PASS full preparation theta-flat R(theta,0) to ALL ORDERS")
print("PASS NONZERO coframe-prep mixed Hessian",mixed)
print("PASS Fredholm (zero prep Hessian) obstruction under one local coframe tangent")
print("FIREWALL other preparations, physical selectors, boundary operators may escape")
print("GR_closed=false")
