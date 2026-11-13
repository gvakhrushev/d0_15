#!/usr/bin/env python3
"""Independent high-precision envelope and product-lift checks for A8."""
import mpmath as mp
import numpy as np

mp.mp.dps = 70
p=(mp.sqrt(5)-1)/2
ell=-mp.log(p)

def h(x):
    return -x*mp.log(x)-(1-x)*mp.log(1-x)

def opt(a):
    z=mp.exp(-ell/a)
    return z/(1+z),-a*mp.log1p(z)/ell

def F(q,a):
    _,m=opt(a)
    return 2+q+(1-q)*m-a*h(q)/ell

count=0
for aa in ('0.0001','0.01','0.2','1','7','100'):
    a=mp.mpf(aa)
    u,m=opt(a)
    for q in (p*p,(p*p+mp.mpf('.5'))/2,mp.mpf('.5')):
        dq=1-m-a*mp.log((1-q)/q)/ell
        da=-(h(q)+(1-q)*h(u))/ell
        assert abs(mp.diff(lambda x:F(x,a),q)-dq)<mp.mpf('1e-60')
        assert abs(mp.diff(lambda x:F(q,x),a)-da)<mp.mpf('1e-60')
        assert dq>=p+a*p*p-mp.mpf('1e-65')
        count+=3

# Independent controls: A_j act on separate blocks; the product lift
# duplicates the physical field direction without identifying block values.
rng=np.random.default_rng(16)
product_count=0
for _ in range(100):
    mats=[]; lifts=[]
    for j in range(4):
        A=np.eye(3)+rng.normal(size=(3,3))*0.15
        mats.append(A); lifts.append(np.linalg.inv(A))
    weights=rng.uniform(.1,2,4); weights/=sum(weights)
    v=rng.normal(size=3)
    blocks=[R@v for R in lifts]
    image=sum(w*(A@x) for w,A,x in zip(weights,mats,blocks))
    assert np.linalg.norm(image-v)<1e-12
    assert max(np.linalg.norm(blocks[i]-blocks[j]) for i in range(4) for j in range(i))>1e-6
    product_count+=1

print(f'PASS: {count} high-precision envelope/bound checks; {product_count} independent-block lift checks.')
print('Scope: ideal functional and linear algebra; no actual mark-reader admission or Book03 price.')
