"""Reverse minimization, a native separating pair, and a single backward calibration."""
import sympy as s
from fractions import Fraction as F


def need(flag, reason):
    if not flag:
        raise ArithmeticError(reason)


def exact(matrix):
    return matrix.applyfunc(s.simplify)


def polar_fixtures():
    # A genuinely nonscalar backward mark on a two-dimensional protected input.
    A,P=s.Rational(4,5),s.Rational(3,5)
    I=s.eye(2)
    V=s.Matrix.vstack(A*I,P*I)
    D=s.diag(A,A,P,P)
    Z=D*V
    mass=(A**4+P**4)
    W=Z/s.sqrt(mass)
    need(exact(W.T*W)==I and exact(Z.T*(s.eye(4)-W*W.T)*Z)==s.zeros(2),'full polar optimum')
    need(exact(V.T*(s.eye(4)-W*W.T)*V)[0,0]>0,'matched inverse is not the free optimum')
    v=s.Matrix([1,0,0,0])
    b=s.Matrix([0,s.sqrt(1-2*P**2),0,s.sqrt(2)*P])
    B=s.Matrix.hstack(v,b)
    Q=s.diag(0,0,1,1)
    need(B.T*B==I and B.T*Q*B != P**2*I and s.trace(B.T*Q*B)==2*P**2,'only a traced backward mark agrees')
    z=s.Rational(1,2**20)
    def det(B):
        C=B.T*Z
        return s.simplify(((1-z)*I+z*(C.T*C)).det())
    need(det(W)>det(V)>det(B),'free / matched / misaligned with the correct trace')
    old=s.Matrix([[s.Rational(2,5),s.Rational(1,4)],[0,s.Rational(3,5)]])
    defect=old.T*Z.T*(s.eye(4)-B*B.T)*Z*old
    need(defect.is_positive_semidefinite and defect.trace()>0,'nonscalar old prefix retains full operator dominance')
    # Full unitary coordinate extension using the direct rotation (no missing columns).
    P0,Q0=V*V.T,W*W.T
    K=Q0*P0+(s.eye(4)-Q0)*(s.eye(4)-P0)
    need(exact(K.T*K-(s.eye(4)-(P0-Q0)**2))==s.zeros(4),'direct-rotation Gram')
    gram=s.simplify((K.T*K)[0,0])
    U=K/s.sqrt(gram)
    need(exact(U.T*U)==s.eye(4) and exact(U*P0*U.T)==Q0,'extension on the inactive complement')


def golden_reverse():
    import mpmath as mp
    iv=mp.iv
    iv.dps=50
    p=(iv.sqrt(5)-1)/2
    a=iv.sqrt(p)
    lo=iv.mpf(3)/4-iv.mpf(126506)/2**20
    hi=iv.mpf(3)/4+iv.mpf(126506)/2**20
    lam=(2*p**3)**20
    u=iv.mpf([lo.a,hi.b])
    nu=iv.mpf(['0.998511','0.998513'])
    t=nu*lam*u
    xi=lam*u*iv.sqrt(nu*(1-nu))
    z=iv.mpf(1)/2**20
    w0=a-(a-p)*t
    cold_plus=a*(a*w0+p*(a-p)*xi)
    cold_minus=a*(a*w0-p*(a-p)*xi)
    need(0<cold_minus and cold_plus<1,'cold return strip')
    # Use the product difference, avoiding interval dependency on identical base amplitudes.
    gap=4*a**2*a*p*w0*(a-p)*xi
    need(z*gap>iv.mpf('8e-16'),'strict independent-backward J gap per old column')
    need(t>0 and t<1 and 0<p<a<1,'full-rank conditioning')
    need((a-p)/(2*p)<iv.mpf('0.14'),'uniform bound on subspace angle')


def scalar_sources():
    t,z,a,p=s.symbols('t z a p',positive=True)
    d=a*a*(1-t)+p*p*t
    matched=(a*(1-t)+p*t)**2
    need(s.simplify(d-matched-(a-p)**2*t*(1-t))==0,'exact Jensen gap in the cold probability before writer')
    A=1-z
    polar=-s.log(A+z*a*a*d)
    need(s.simplify(s.diff(polar,t)-z*a**2*(a*a-p*p)/(A+z*a*a*d))==0,'reduced geometric source')
    m=s.symbols('m',nonnegative=True)
    k=z*a*a*d
    ratio=s.simplify(1-m*(A+k)/(A+k*m))
    need(s.simplify(ratio-A*(1-m)/(A+k*m))==0,'response loss of a nonpolar minimizer')
    # Check the sharp mark box with independent scalar backward probability v.
    v=s.symbols('v',positive=True)
    score=a*s.sqrt((1-t)*(1-v))+p*s.sqrt(t*v)
    optimum=p*p*t/d
    value=s.simplify((score.subs(v,optimum)**2).subs(t,s.Rational(2,5)).subs({a:s.Rational(4,5),p:s.Rational(3,5)}))
    need(value==d.subs({t:s.Rational(2,5),a:s.Rational(4,5),p:s.Rational(3,5)}),'calibration tradeoff')


if __name__=='__main__':
    polar_fixtures()
    golden_reverse()
    scalar_sources()
    print('PASS: independent native reverse gap, free full-matrix optimum, traced-backward calibration, full-column lift, reduced derivative and nonpolar loss.')
