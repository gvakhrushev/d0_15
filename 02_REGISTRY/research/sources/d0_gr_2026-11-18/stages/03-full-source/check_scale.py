"""Check the primary single-J2 scale contrast and true two-type AF trace formula."""
import sympy as s
import mpmath as mp

r, x, t, rho = s.symbols("r x t rho", nonzero=True)
A, b, D = s.symbols("A b D")
# Verify the pressure reflection without treating the mean as a local scalar.
# tr(V E)=tr Q+2<F>, and <tr Q>=<d>-<F>.
Qtrace, avgF, avgd = s.symbols("Qtrace avgF avgd")
refl_correction = avgF/2-(Qtrace+2*avgF)/2+avgd/2
assert s.expand(refl_correction.subs(Qtrace,avgd-avgF))==0
# Confirm K'(0) in independent rings where U+q=1 and lambda''/(lambda')²=-1/(2q).
M,q=s.symbols("M q", nonzero=True)
kdiff=8*(-M+(2-M*(1-q))/(2*q))
assert s.simplify(kdiff-4*(2-M*(1+q))/q)==0

mp.mp.dps=70
p=(mp.sqrt(5)-1)/2
z=mp.mpf(2)**-20
def price(r,x):
    E=p*p*(1+r)
    b=(p-p*p*x)**2
    eps=4*E*(1-E); B=4*b*(1-b); C=B+(1-B)*eps
    return -mp.log1p(-z*B)-mp.log1p(-z*C)
def K(y):
    return mp.diff(lambda x:price(y,x),0)/mp.diff(lambda r:price(r,0),y)
u=4*p**3; q0=p**6
M0=1+z*q0/(1-z*u)
assert abs(mp.diff(K,0)+4*(2-M0*(1+q0))/q0)<mp.mpf('1e-62')
y=mp.mpf(1)/1000
rho=1/p**2
v1=K(y);v2=K(y/rho)
assert -mp.mpf('23.485')<v1<-mp.mpf('23.484')
assert -mp.mpf('23.443')<v2<-mp.mpf('23.442')
print('negative orientation, finite K(y), K(y/rho), K derivative:',[mp.nstr(v,18) for v in (v1,v2,mp.diff(K,0))])
# True unweighted input trace at n=0 vs n+r, through the source owner's P.
m=s.Matrix([[1,1],[1,0]])**8
step=8; delta=4*(1-p*p); C=1-p**step*delta
P=mp.matrix([[p**(step+j-i)*(int(m[i,j])-delta*int(i==j))/C for j in range(2)] for i in range(2)])
mu=mp.matrix([[mp.mpf(1)/2,mp.mpf(1)/2]])
fine=m*s.Matrix([1,1]);w0=mp.mpf(int(fine[0])**2)/(int(fine[0])**2+int(fine[1])**2)
pi0=1/(1+p*p)
chi=(p**(2*step)-p**step*delta)/C
obs=(mu*P)[0]-w0
assert abs(obs-(chi*(mu[0]-pi0)-(w0-pi0)))<mp.mpf('1e-65')
print('actual P second eigenvalue, finite trace mismatch:', [mp.nstr(v,18) for v in (chi,obs)])
