#!/usr/bin/env python3
"""Existing full CAR correlations and their explicit reading, not a new law."""
import importlib.util
from pathlib import Path
import sys
import sympy as s

def load(stem):
    f=Path(__file__).with_name(stem+'.py')
    q=importlib.util.spec_from_file_location(stem,f)
    m=importlib.util.module_from_spec(q);sys.modules[q.name]=m;q.loader.exec_module(m)
    return m

P=load('a4d_native_reference_memory_preparation')
a,p,z=P.a,P.p,P.z
C=P.C
red,mat=P.red,P.mat
ETA=s.diag(1,-1,-1,-1)
I4,I16=s.eye(4),s.eye(16)

def car_operators():
    c=[C.creator(I4[:,i]) for i in range(4)]
    beta=c[0]+c[0].T
    gamma=[c[i]-c[i].T for i in range(1,4)]
    return c,beta,gamma,[beta*x for x in gamma]

def blank_code():
    B=s.zeros(16,2)
    B[0,0]=B[14,0]=1/s.sqrt(2)
    B[3,1]=B[13,1]=1/s.sqrt(2)
    return B

def current(F,m):
    """Basis-independent full reading, evaluated in the frame F."""
    G=(F*F.T).inv();W=C.ext(G)
    def adj(X):return W.inv()*X.T*W
    cr=C.creator(F[:,0]);beta=cr+adj(cr)
    N=(m.T*W*m)[0]
    readings=[]
    for i in range(1,4):
        cr=C.creator(F[:,i]);alpha=beta*(cr-adj(cr))
        readings.append(red((m.T*W*alpha*m)[0]/N))
    return mat(F*s.Matrix([1]+readings))

def observer_pairing(q,J):
    ell=q.inv();k=(J.T*ell*J)[0]
    return mat(-ell+2*ell*J*J.T*ell/k)

def rest_lorentz_record(h,n):
    """Literal owned formula with exact golden reduction after each product.

    This rest-Lorentz observer class has h inverse = eta h eta. Reducing
    before powers avoids expanding spurious unreduced symbolic Gram defects.
    """
    W=mat(C.ext(h));Wi=mat(C.ext(ETA*h*ETA))
    cr=C.creator(n);an=mat(Wi*cr.T*W)
    N=mat(cr*an);X=C.DEG-N
    X2=mat(X*X);X3=mat(X2*X)
    H=mat((-2*X3+9*X2-7*X)/6)
    U=mat(a*((I16-H)+H*(I16-2*N))
          +p*((I16-H)*(cr-an)-H*(cr+an)))
    return U,I16-N,W,Wi

def orbit_data():
    U=P.full_tuple()[0];B=blank_code()
    masks=[0,1,2,3,12,13,14,15]
    R=s.Matrix.hstack(*(I16[:,i] for i in masks))
    return U,B,R

def preparation_curve(t):
    u=(1-t*t)/(1+t*t);v=2*t/(1+t*t)
    return s.Matrix([a*u-p*v,p*u+a*v])

def even_chart_sequence(A,b):
    Q=mat(s.Matrix([[a,-p],[p,a]])**2)
    values=[]
    for n in range(5):
        T=mat(Q**n)
        cross=(T*A*T.T)[0,1]*s.conjugate((T*b)[0])
        cross=s.expand_complex(cross)
        values.append(red(s.re(cross)))
    return values

def fixed_beta_rational_bounds():
    off=s.Rational(16896,2**30)
    diagonal=s.Rational(1,2700)
    return dict(off_upper=off,diagonal_lower=diagonal,
                negative_margin=diagonal-off,claimed_margin=s.Rational(1,3000),
                partition_upper=s.Integer(81),source_denominator=s.Integer(486000))

if __name__=='__main__':
    print('FULL_CORRELATED_CURRENT_READING_NATIVE_ADMISSION_OPEN')
