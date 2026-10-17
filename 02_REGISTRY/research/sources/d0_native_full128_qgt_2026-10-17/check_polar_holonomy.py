"""Exact degree-2 polar holonomy of golden native-comparison isometry.
3x3 SO(3) fixture is generic isometry class, not physical native SELECT.
"""
import sympy as s, json
p=(s.sqrt(5)-1)/2; q=p*p; t=s.symbols('t'); I=s.eye(3)
X=s.Matrix([[0,-1,0],[1,0,0],[0,0,0]])
Y=s.Matrix([[0,0,0],[0,0,-1],[0,1,0]])
comm=X*Y-Y*X
count=0
def check(ok,label):
 global count
 if not bool(ok): raise RuntimeError(label)
 count+=1
def eq(A,B,label):check(all(s.simplify(a-b)==0 for a,b in zip(A,B)),label)

def coeff(mat,n):return mat.applyfunc(lambda f:s.expand(f).coeff(t,n))

def clip(M):return coeff(M,0)+t*coeff(M,1)+t*t*coeff(M,2)

def product(a,b):return clip(a*b)

# M(x,y)=exp(xX)exp(yY) chart through full second jet.
def frame(x,y):
 A=I+x*t*X+(x*x*t*t/2)*X**2
 B=I+y*t*Y+(y*y*t*t/2)*Y**2
 return product(A,B)

vertices=[frame(0,0),frame(1,0),frame(1,1),frame(0,1)]
for v in vertices:
 eq(clip(v.T*v),I,'orthogonal frame 2-jet')

def overlap(i,j):
 return clip(p*I+q*product(vertices[i].T,vertices[j]))

def polar_jet(C):
 C0=coeff(C,0); eq(C0,I,'identity overlap at collapsed loop')
 A=coeff(C,1);B=coeff(C,2)
 T1=A.T+A
 T2=B.T+B+A.T*A
 # polynomial expansion of (C.T C)^-1/2 at I, preserving matrix order.
 invroot=I-t*T1/2+t*t*(-T2/2+s.Rational(3,8)*T1*T1)
 U=product(C,invroot)
 eq(clip(U.T*U),I,'unitary polar 2-jet')
 return U

loop=I
for idx in range(4):
 fr=idx;to=(idx+1)%4
 E=polar_jet(overlap(to,fr))
 loop=product(E,loop)

C1=coeff(loop,1); C2=coeff(loop,2)
eq(C1,s.zeros(3),'first loop jet cancels')
print('coef ratio simplified',s.simplify(C2[0,2]/comm[0,2]))
check(C2!=s.zeros(3),'nonzero loop curvature')
eq(C2,p**3*comm,'golden Berry-polar holonomy (minus Berry F)')
check(s.trace(C2)==0,'non-Abelian curvature invisible to logdet trace')
# Full golden V(x)=(sqrt(p)I; p M(x)): metric Q(v,v)=p^3 dM.T*dM.
# These vials X,Y are independent, positive info length. Berry F=-p^3[X,Y].
for A in (X,Y,X+Y):
 metric=p**3*A.T*A
 check(s.trace(metric)>0,'native record positive quadratic cost')
 eq(metric,p**2*A.T*A-p**4*A.T*A,'coercive metric exact')
print(json.dumps({'status':'PASS','exact_controls':count,'holonomy_coefficient':'+p^3 [X,Y] for forward transport; Berry F=-p^3 [X,Y]', 'p_cubed':str(s.simplify(p**3)),'curvature_rank':C2.rank(),'native_lorentz_selected':False},sort_keys=True))
