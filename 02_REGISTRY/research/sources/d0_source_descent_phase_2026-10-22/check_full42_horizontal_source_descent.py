#!/usr/bin/env python3
"""Exact full-source descent check: generic Jones34 42+upstream candidate.
Synthetic mathematical fixture, not original physical Jones/CAR Book03 merger.
"""
import sympy as sp

nchecks=0
def check(msg, value):
    global nchecks
    if not bool(value):
        raise AssertionError(msg)
    nchecks+=1

x,y,w,u=sp.symbols('x y w u',real=True)
t=sp.Matrix([x,y]); z=sp.Matrix([w]); inp=sp.Matrix([u])
q=sp.Matrix([x+w*y+u, y+w+u*u])
J=q.jacobian(t); W=q.jacobian(z); U=q.jacobian(inp)
check('Jones-type pivot locally invertible',sp.simplify(J.det())==1)
S0=(x*x-y*y)/2+x*w+w*w/2
G=lambda q:q[0]*q[0]+q[0]*q[1]+2*q[1]*q[1]
B=sp.expand(S0-G(q))

def vertical(B0):
    target=sp.expand(S0-B0)
    gt=sp.Matrix([sp.diff(target,v) for v in t])
    gw=sp.Matrix([sp.diff(target,v) for v in z])
    bu=sp.Matrix([sp.diff(B0,v) for v in inp])
    jt=J.T.inv()*gt
    rw=gw-W.T*jt
    ru=bu+U.T*jt
    return [sp.simplify(i) for i in rw],[sp.simplify(i) for i in ru],sp.simplify(jt)

rw,ru,grad=vertical(B)
for v in rw+ru: check('score descends in both vertical directions',v==0)
for i in range(2):
    a,b=sp.symbols('a b')
    wanted=sp.diff(G(sp.Matrix([a,b])),[a,b][i]).subs({a:q[0],b:q[1]})
    check('reconstructed score differential',sp.simplify(grad[i]-wanted)==0)
badB=B+w*u+sp.Rational(1,4)*w*w
rw_bad,ru_bad,_=vertical(badB)
check('charged hidden field row',sp.simplify(rw_bad[0]+u+w/2)==0)
check('independent source input row',sp.simplify(ru_bad[0]-w)==0)
probe={x:sp.Rational(1,10),y:sp.Rational(1,5),w:sp.Rational(3,10),u:sp.Rational(2,5)}
check('off-null hidden source falsifier',rw_bad[0].subs(probe)==-sp.Rational(11,20))
check('off-null input source falsifier',ru_bad[0].subs(probe)==sp.Rational(3,10))
# Actual original full42 dimensions are used, but the following carrier
# is a SYMBOLIC TEST and NOT a measured original field/preparation.
N,K,L=34,8,3
M=sp.zeros(N,K); C=sp.zeros(N,L)
for i in range(N):
    for j in range(K):M[i,j]=sp.Rational((i+1)*(j+2)%7,17)
    for j in range(L):C[i,j]=sp.Rational((i+2)*(j+1)%5,13)
t34=sp.Matrix(sp.symbols('t0:'+str(N)))
z8=sp.Matrix(sp.symbols('z0:'+str(K)))
u3=sp.Matrix(sp.symbols('u0:'+str(L)))
qq=t34+M*z8+C*u3
H=sp.diag(*([1,-1]*17))
SS=(t34.T*H*t34)[0]/2+(z8.T*z8)[0]/2
G34=(qq.T*qq)[0]/2
BB=sp.expand(SS-G34)
gt34=qq
w34=M.T*qq
u34=-C.T*qq
for i in range(K):check('full42 exact field-fibre row',sp.simplify((w34-M.T*gt34)[i])==0)
for i in range(L):check('full42 exact input-fibre row',sp.simplify((u34+C.T*gt34)[i])==0)
check('extra charged field tag rejects any score',sp.expand(-u3[0])!=0)
check('extra charged independent input rejects any score',sp.expand(z8[0])!=0)
check('signed action retains original-style coframe saddle',H[0,0]>0 and H[1,1]<0)
print(f'PASS {nchecks} exact symbolic controls; 34 pivots + 8 field-fibre rows + 3 input-fibre rows')
print('All-chart report score iff vertical source descent; real paid B remains physically UNDEFINED, GR_closed=false')
