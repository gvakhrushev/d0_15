#!/usr/bin/env python3
"""Exact rational first-jet check of the complete source, using only stdlib.

No native-admission or actual Book-selection claim. The general operator
identity is proved separately; these are independent complete-matrix controls.
Every failure is explicit and remains active under python -O.
"""
from fractions import Fraction as F
import json

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

class J:
    def __init__(self, x=0, dx=(0,0,0)):
        self.x=F(x); self.dx=tuple(F(v) for v in dx)
    @staticmethod
    def of(x): return x if isinstance(x,J) else J(x)
    def __add__(self,y):
        y=J.of(y); return J(self.x+y.x,tuple(a+b for a,b in zip(self.dx,y.dx)))
    __radd__=__add__
    def __neg__(self): return J(-self.x,tuple(-a for a in self.dx))
    def __sub__(self,y): return self+-J.of(y)
    def __rsub__(self,y): return J.of(y)+-self
    def __mul__(self,y):
        y=J.of(y); return J(self.x*y.x,tuple(a*y.x+self.x*b for a,b in zip(self.dx,y.dx)))
    __rmul__=__mul__
    def __truediv__(self,y):
        y=J.of(y); return J(self.x/y.x,tuple((a*y.x-self.x*b)/(y.x*y.x) for a,b in zip(self.dx,y.dx)))
    def __rtruediv__(self,y): return J.of(y)/self
    def __pow__(self,n):
        if n==0:return J(1)
        require(n>0, 'jet exponent must be nonnegative')
        return self*(self**(n-1))
    def __eq__(self,y):
        y=J.of(y); return self.x==y.x and self.dx==y.dx

def zero(n,m):return [[J() for _ in range(m)] for _ in range(n)]
def eye(n):return [[J(i==j) for j in range(n)] for i in range(n)]
def tr(A):return [list(row) for row in zip(*A)]
def add(A,B):return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]
def sc(a,A):return [[a*x for x in row] for row in A]
def mm(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def cat(A,B):return [a+b for a,b in zip(A,B)]
def block(A,B,C,D):return cat(A,B)+cat(C,D)
def eq(A,B,label):require(A==B,label)

count=0
for u0 in [F(1,3),F(2,3),F(1),F(4,3),F(2)]:
    u=J(u0,(1,0,0)); a=J(F(2,5),(0,1,0)); b=J(F(3,7),(0,0,1))
    t=(1-u*u)/(1+u*u); r=2*u/(1+u*u)
    A=sc(1/(1+a*a),[[1-a*a,-2*a],[2*a,1-a*a]])
    B=sc(1/(1+b*b),[[1-b*b,2*b],[2*b,b*b-1]])
    I=eye(2); Z=zero(2,2)
    W=block(sc(t,I),sc(r,A),sc(r,B),sc(-t,mm(B,A)))
    P=block(I,Z,Z,Z); Q=add(eye(4),sc(-1,P)); R=add(P,sc(-1,Q)); i=I+Z
    eq(mm(tr(W),W),eye(4),'complete W orthogonal, all jets')
    eq(mm(mm(tr(i),W),i),sc(t,I),'exact scalar compression, all jets')
    V=mm(mm(mm(R,tr(W)),R),W)
    controlled=block(eye(4),zero(4,4),zero(4,4),W)
    T=mm(mm(mm(controlled,P+Q),V),i)
    expected=sc(2*t*t-1,i)+add(sc(-2*t,i),sc(2*t*t,mm(W,i)))
    eq(T,expected,'full eight-row cleanup identity, all jets')
    eq(mm(tr(T),T),I,'complete output norm, all jets')
    garb=block(Q,zero(4,4),zero(4,4),Q)
    eq(mm(mm(tr(T),garb),T),sc(4*t**4*(1-t*t),I),'quartic all-work garbage mass')
    # Independent exact rational port rotation (3/5,4/5).
    c,d=F(3,5),F(4,5)
    mix=block(sc(c,eye(4)),sc(-d,eye(4)),sc(d,eye(4)),sc(c,eye(4)))
    Y=sc(-1,mm(mix,T))
    clean0=c*(1-2*t*t)-2*d*t*(1-t*t)
    clean1=d*(1-2*t*t)+2*c*t*(1-t*t)
    QWi=mm(mm(Q,W),i)
    eq(Y,add(sc(clean0,i),sc(2*d*t*t,QWi))+add(sc(clean1,i),sc(-2*c*t*t,QWi)),
       'all mixed output rows including moving garbage')
    q1=clean1**2+4*c*c*t**4*(1-t*t)
    eq(mm(tr(Y[4:]),Y[4:]),sc(q1,I),'full port effect, all jets')
    if u0==1:
        base=sc(-1,i)+zero(4,2)
        deriv=zero(4,2)+sc(-2*t.dx[0],i)
        for k,row in enumerate(T):
            for j,z in enumerate(row):
                require(z.x==base[k][j].x, 'null complete output value')
                require(z.dx[0]==deriv[k][j].x, 'null complete transverse jet')
                require(z.dx[1:]==(F(0),F(0)), 'noncommuting vertical jets vanish')
        require(q1.x==d*d and q1.dx[0]==4*c*d*t.dx[0], 'null full port jet')
    count+=1

# Q(a), a^4+a^2-1=0; p=a^2. Exact Golden-square arithmetic.
class K:
    def __init__(self,v):self.v=tuple(F(x) for x in (v if isinstance(v,(list,tuple)) else [v,0,0,0]))
    @staticmethod
    def of(x):return x if isinstance(x,K) else K(x)
    def __add__(self,y):return K([a+b for a,b in zip(self.v,K.of(y).v)])
    __radd__=__add__
    def __neg__(self):return K([-a for a in self.v])
    def __sub__(self,y):return self+-K.of(y)
    def __rsub__(self,y):return K.of(y)+-self
    def __mul__(self,y):
        y=K.of(y); z=[F(0)]*7
        for i,a in enumerate(self.v):
            for j,b in enumerate(y.v):z[i+j]+=a*b
        for k in range(6,3,-1):z[k-4]+=z[k];z[k-2]-=z[k];z[k]=0
        return K(z[:4])
    __rmul__=__mul__
    def __pow__(self,n):return K(1) if n==0 else self*(self**(n-1))
    def __eq__(self,y):return self.v==K.of(y).v
    def inverse(self):
        columns=[(self*K([int(i==j) for i in range(4)])).v for j in range(4)]
        rows=[[columns[j][i] for j in range(4)]+[F(i==0)] for i in range(4)]
        for j in range(4):
            pivot=next((i for i in range(j,4) if rows[i][j]),None)
            require(pivot is not None, 'invertible Golden field element')
            rows[j],rows[pivot]=rows[pivot],rows[j]
            a=rows[j][j]
            rows[j]=[v/a for v in rows[j]]
            for i in range(4):
                if i==j:continue
                a=rows[i][j]
                rows[i]=[x-a*y for x,y in zip(rows[i],rows[j])]
        return K([row[-1] for row in rows])
    def __truediv__(self,y):return self*K.of(y).inverse()
    def __rtruediv__(self,y):return K.of(y)*self.inverse()

aa=K([0,1,0,0]); p=aa*aa; cg=p**3; sg=2*p*aa
require(p+p*p==1 and cg*cg+sg*sg==1, 'Golden-square normalization')
require(aa*aa-p*p==cg and 2*aa*p==sg, 'actual square of the Golden rotation')
require(cg*cg==p**6 and sg*sg==4*p**3, 'Golden-square port baselines')
require(4*cg*sg==8*p**4*aa, 'Golden-square complete source coefficient')
require((aa*aa)/(p*p)==1/p, 'single-Golden matched code ratio')

# Original local J2 at f=q=0, sigma=-1 and the same original z.
# The query scale tau^2, scene multiplicities and site weights are common
# factors, so the dimensionless two-band derivative suffices for this ratio.
z=K(F(1,2**20))
L=4*p**3; M=L*(1+p**6)
Q0=1-z*L; R0=1-z*M
require(L==1-p**6 and M==1-p**12, 'literal original two-tick bands')
weight_minus=z*(1-z*(1-p**12))
weight_plus=z*(1-z*(1-p**6))
require(weight_minus==z*R0 and weight_plus==z*Q0, 'retained finite-coin anchor')

# Original E=p^2(1+tau^2 f), b=(p-p^2 tau^2 q)^2,
# lambda_AF=4E(1-E), B=4b(1-b), upper band=lambda_AF+(1-lambda_AF)B.
d_lambda_f=4*(1-2*p*p)*p*p
d_B_q=4*(1-2*p*p)*(-2*p**3)
d_upper_f=(1-L)*d_lambda_f
d_upper_q=(1-L)*d_B_q
require(d_upper_f==4*p**11 and d_B_q==-8*p**6,
        'actual AF/scene independent derivatives')
geo_J=z*d_upper_f/R0
mat_J=z*d_B_q/Q0+z*d_upper_q/R0
geo_anchor=weight_plus*d_upper_f
mat_anchor=weight_minus*d_B_q+weight_plus*d_upper_q
require(geo_anchor==Q0*R0*geo_J, 'whole geometric source transport')
require(mat_anchor==Q0*R0*mat_J, 'whole material source transport')
lambda_old=-2/(p**5)*(R0/Q0+p**6)
require(mat_J/geo_J==lambda_old, 'original finite-z coupling')
require(mat_anchor/geo_anchor==lambda_old, 'same coupling after full anchor')

print(json.dumps({
    'status':'PASS',
    'exact_complete_matrix_jet_fixtures':count,
    'vertical_noncommuting_directions':2,
    'complete_output_and_port_effect':True,
    'quartic_all_work_probability':True,
    'golden_square_baseline_and_source':True,
    'original_two_band_finite_coin_anchor':True,
    'same_original_finite_z_matter_coupling':True,
    'arithmetic':'exact rational jets and Q(a), a^4+a^2-1=0',
    'scope':'Supplied coherent-query interface and declared terminal prices.',
    'native_primitive_admission_proved':False,
    'global_minimum_selection_proved':False,
    'GR_closed':False
},indent=2))
