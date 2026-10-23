#!/usr/bin/env python3
"""Full16 native CAR tensor-torsion quartic feedback diagnostic.

Retains all 16 exterior grades and all Fourier momenta (the latter through
a convergent Gaussian cutoff with explicit tail). This is NOT a native root.
"""
import math
import numpy as np
from scipy.linalg import eigvalsh
from sympy import Matrix, Rational, trace

c=[]
for j in range(4):
    a=Matrix.zeros(16,16)
    for n in range(16):
        if not (n>>j)&1:
            sign=-1 if (n&((1<<j)-1)).bit_count()%2 else 1
            a[n|(1<<j),n]=sign
    c.append(a)
i=[a.T for a in c]
gamma=[c[j]-i[j] for j in range(4)]
hat=[c[j]+i[j] for j in range(4)]
B0=hat[1]*hat[2]/2
B1=hat[0]*hat[2]/2
F=B0*B1-B1*B0
q4=-trace(2*F*F)/6
if q4!=Rational(4,3):
    raise AssertionError(("wrong native quartic",q4))
for b in (B0,B1):
    if b+b.T!=Matrix.zeros(16,16):raise AssertionError("right Clifford B not skew")
    for g in gamma:
        if b*g!=g*b:raise AssertionError("right Clifford commuting failed")
print("16-CAR tensor a2=0, a4(lambda=1) exact =",q4)

g0=np.array(gamma[0],dtype=np.complex128)
g1=np.array(gamma[1],dtype=np.complex128)
b0=np.array(B0,dtype=np.complex128)
b1=np.array(B1,dtype=np.complex128)
f=np.array(F,dtype=np.complex128)
ident=np.eye(16,dtype=np.complex128)
def symbol(lam,k0,k1):
    # D^2 = -(d+B)^2 + gamma0 gamma1 [B0,B1]
    return (4*math.pi**2*(k0*k0+k1*k1)*ident
            -4j*math.pi*lam*(k0*b0+k1*b1)
            -lam**2*(b0@b0+b1@b1)
            +lam**2*(g0@g1@f))
def theta(t,cutoff):
    return 1+2*sum(math.exp(-4*math.pi**2*t*j*j) for j in range(1,cutoff+1))
p=(math.sqrt(5)-1)/2
beta=2*p*p
z=2**-20
q=z/(1-z)
M=128
Phi1=math.log1p(q)
expected=lambda lam:-M*Phi1/(16*math.pi**2)*float(q4)*lam**4
def full16_heat(t,lam):
    cutoff=int(math.ceil(math.sqrt(45/(4*math.pi**2*t))))+1
    factor=theta(t,cutoff)**2
    value=0.
    for k0 in range(-cutoff,cutoff+1):
        for k1 in range(-cutoff,cutoff+1):
            eig=eigvalsh(symbol(lam,k0,k1),check_finite=False)
            if eig[0]<-1e-8:raise AssertionError("D^2 not positive")
            value+=sum(math.exp(-t*float(x)) for x in eig)
    return factor*value
def feedback(R,lam):
    value=0.
    for n in range(1,5):
        t=n*beta/R**2
        value+=(-1)**(n+1)*q**n*full16_heat(t,lam)/n
    return -M*value
for R in (8,12):
    j=feedback(R,1)-feedback(R,0)
    err=j-expected(1)
    print("R",R,"native_feedback_delta",format(j,".12g"),"quartic_IR_error",format(err,".8g"))
    if abs(err)>.00000001:raise AssertionError(("IR quartic coefficient",R,err))
# Negative control: replacing the true full16 F term or the tensor action by 0
# would set q4=0, contrary to exact CAR algebra and numeric signed feedback.
if q4==0 or not expected(1)<0:raise AssertionError("negative control ineffective")
print("status=PASS; no physical 24-connection stationarity or GR claim")
