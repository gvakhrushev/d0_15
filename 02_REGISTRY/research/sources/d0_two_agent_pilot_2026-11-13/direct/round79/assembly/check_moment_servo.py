"""Finite-rank spectral calibration, Bernstein implementation and independent tangent rows."""
from fractions import Fraction as F
from math import comb, expm1, log1p, sqrt

import numpy as np
from check_old_trace import old_words


def elementary(moments):
    rank=len(moments)
    coefficients=[F(1)]
    for k in range(1,rank+1):
        coefficients.append(sum((-1)**(j-1)*coefficients[k-j]*rank*moments[j-1]
                                for j in range(1,k+1))/k)
    return coefficients


def sign_table(mu,kappa,q,alpha,rate):
    # Rank two. Outside a regular neighborhood of the true scores choose a bounded fallback.
    rhs=expm1(2*rate*(1-q))/alpha
    discriminant=mu**2+alpha*(2*mu**2-kappa)*rhs
    if discriminant <= 0:
        return .5
    denominator=mu+sqrt(discriminant)
    if denominator == 0:
        return .5
    u=rhs/denominator
    return sqrt(u) if 0 < u < 1 else .5


def distribution(m,p):
    return np.array([comb(m,k)*p**k*(1-p)**(m-k) for k in range(m+1)])


def paid_mean(m,probs,slopes,alpha,rate):
    laws=[distribution(m,x) for x in probs]
    derivatives=[law*(np.arange(m+1)-m*x)*v/(x*(1-x))
                 for law,x,v in zip(laws,probs,slopes)]
    grid=np.arange(m+1)/m
    average=derivative=0.
    bits=32
    for i,x in enumerate(grid):
        for j,y in enumerate(grid):
            values=np.array([sign_table(x,y,q,alpha,rate) for q in grid])
            # Signed expectation of a finite, binary-quantized choice of phase.
            values=2*np.floor((1+values)*2**(bits-1))/2**bits-1
            mean=values@laws[2]
            average+=laws[0][i]*laws[1][j]*mean
            derivative+=(derivatives[0][i]*laws[1][j]+laws[0][i]*derivatives[1][j])*mean
            derivative+=laws[0][i]*laws[1][j]*(values@derivatives[2])
    return average,derivative


def main():
    lambdas=[F(1,4),F(2,5),F(3,7),F(1,1)]
    moments=[sum(v**k for v in lambdas)/4 for k in range(1,5)]
    e=elementary(moments)
    for t in [F(1,4),F(1,2**20)]:
        product=F(1)
        for a in lambdas:
            product*=1+t*a
        assert sum(v*t**k for k,v in enumerate(e))==product
    alpha=1/(2**20-1)
    rate=log1p(alpha)/8
    _,corners=old_words()
    a=corners[0].T@corners[0]
    other=corners[1].T@corners[1]
    da=other-a
    mu=np.trace(a)/2
    m2=np.trace(a@a)/2
    q,dq=.31,.017
    for matrix in (a,other,np.array([[.67,.14],[.14,.41]])):
        x=np.trace(matrix)/2
        y=np.trace(matrix@matrix)/2
        u=sign_table(x,y,q,alpha,rate)**2
        logdet=sum(log1p(alpha*u*l) for l in np.linalg.eigvalsh(matrix))/2
        assert abs(logdet-rate*(1-q))<1e-18
    slopes=np.array([np.trace(da)/2,np.trace(a@da),dq])
    errors=[]
    for m in (6,18,54,128):
        s,ds=paid_mean(m,[mu,m2,q],slopes,alpha,rate)
        rhs=2*s*ds*a+s**2*da
        actual=-alpha*np.trace(np.linalg.solve(np.eye(2)+alpha*s*s*a,rhs))/(2*rate)
        err=abs(actual-dq)
        print(m,"normalized source error",err)
        errors.append(err)
    assert errors[-1] < dq/2
    # Directly differentiate the finite polynomial against an independent secant.
    m,step=8,1e-5
    probs=np.array([mu,m2,q])
    _,estimate=paid_mean(m,probs,slopes,alpha,rate)
    plus,_=paid_mean(m,probs+step*slopes,np.zeros(3),alpha,rate)
    minus,_=paid_mean(m,probs-step*slopes,np.zeros(3),alpha,rate)
    assert abs(estimate-(plus-minus)/(2*step))<1e-8
    print("native two-column prefixes and four rational moments verified")


if __name__=='__main__':
    main()
