"""Single ruled cut: the literal pointer/0-10 gates, generated cold effect, and both first variations."""
from hashlib import sha256
from pathlib import Path
import sys

import sympy as s

repo=Path(__file__).resolve().parents[7]
native=repo/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
if sha256(native.read_bytes()).hexdigest()!='222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c':
    raise RuntimeError('Unexpected primary gate alphabet')
sys.path.insert(0,str(native.parent))
import native_execution as n


def require(value, error):
    if not value:
        raise ArithmeticError(error)


def eq(a,b,why):
    require(n.exact_matrix_equal(s.Matrix(a),s.Matrix(b)),why)


def test_native_pointer():
    # Wires 0/1/2 = threshold flag, meter, tail; protected Spin occupies 3 and 4.
    ops=tuple(n.Gate(kind,tuple(wires)) for kind,wires in [
        ('CX',[0,1]),('G',[1]),('CX',[1,2]),('G',[2]),('CX',[1,2])])
    actual=n.Execution(5,(),(),ops,n.G_CX_SOURCE_I,0,(3,4))
    sfull=n.word_matrix(actual,max_qubits=5,max_expanded_stages=5)
    p,a=n.P,n.A
    v=s.Matrix([a,p])
    x=s.Matrix([[0,1],[1,0]])
    zero,one=s.eye(2)[:,0],s.eye(2)[:,1]
    g=n.G_LOCAL
    writer=s.Matrix.hstack(s.kronecker_product(zero,g*v),s.kronecker_product(one,x*g*x*v))
    eq(s.kronecker_product(s.eye(2),v.T)*writer,a*s.eye(2),'actual born tail compression')
    for b in (0,1):
        meter=g*x**b*v
        if b:
            eq(meter,one,'rotated true meter')
        omega=writer*meter
        active=s.eye(2)[:,b]
        full_in=s.kronecker_product(active,v,v,s.eye(4))
        eq(sfull*full_in,s.kronecker_product(active,omega,s.eye(4)),'full apparatus columns and protected Spin')
        eq([[meter[1]**2]], [[(4*p**3,1)[b]]], 'true readout probabilities')
        eq([[(s.kronecker_product(v.T,v.T)*omega)[0]]], [[(p,a*p)[b]]], 'full cold amplitudes')
    eq([[1-4*p**3]], [[p**6]], 'nonzero slope')
    require(s.Rational(94,100)<4*p**3<1 and p<a<1,'Golden strip')


def test_echo_and_composition():
    z,c,k,t,r,b,d=s.symbols('z c k t r b d',positive=True)
    cold=(c-k*t)**2
    j=-s.log(1-z+z*cold)
    require(s.simplify(s.diff(j,t)-2*z*k*(c-k*t)/(1-z+z*cold))==0,'native feedback first source')
    # Conditional input signs controlled by an arbitrary, not necessarily diagonal, effect.
    x,y,v=s.symbols('x y v',real=True)
    Q=s.Matrix([[x,v],[v,y]])
    I=s.eye(2)
    require(((c*I-k*Q)**2 - (c*c*I-2*c*k*Q+k*k*(Q**2))).applyfunc(s.expand)==s.zeros(2),'operator cold effect')
    # Generic unitary A mixes genuine work sectors. Reversing A leaves endpoint conjugate to the fixed middle.
    cs,sn=s.Rational(3,5),s.Rational(4,5)
    A=s.Matrix([[cs,-sn],[sn,cs]])
    mid=s.Matrix([[0,1],[1,0]])
    require((A.T*mid*A).charpoly().all_coeffs()==mid.charpoly().all_coeffs(),'fixed-size holonomy conjugacy')
    # Even failure of one true in-line measurement destroys the echo: pinching a prepared qubit is not an inverse.
    psi=s.Matrix([cs,sn])
    require((psi.T*s.diag(cs**2,sn**2)*psi)[0] < 1,'erased coherence would change the original return')
    # Split a mixed old cut: nonscalar drifts can carry a different weight in CQ and J.
    drift=s.diag(1,-1)
    require(s.trace(drift)==0 and s.trace(s.diag(s.Rational(2,3),s.Rational(1,3))*drift)==s.Rational(1,3),'old input weighted trace cannot be silently replaced')
    u=s.symbols('u',positive=True)
    meter=b+d*u
    H=-meter*s.log(meter)-(1-meter)*s.log(1-meter)
    ell=s.symbols('ell',positive=True)
    cost=1+meter-H/ell
    require(s.simplify(s.diff(cost,u)-d*(1+(s.log(meter)-s.log(1-meter))/ell))==0,'literal code minus full CQ first derivative')


def test_truthful_product():
    old,dk,w,dw,z=s.symbols('old dk w dw z',positive=True)
    for m in (1,2,5,12):
        # Different old return eigenvalues, nonzero derivative of the old trace on a sample geometric root.
        u=s.symbols('u')
        x=w+u*dw
        vals=[s.Rational(1,3)+u*dk,s.Rational(3,5)-2*u*dk]
        exact=-sum(s.log(1-z+z*(x**m)*v) for v in vals)
        delta=-(z/(1-z))*w**m
        beta=z/(1-z)
        traces=sum(v.subs(u,0)/(1+beta*w**m*v.subs(u,0)) for v in vals)
        fixed=sum(v.diff(u)/(1+beta*w**m*v.subs(u,0)) for v in vals)
        require(s.cancel(exact.diff(u).subs(u,0)/delta-(m*dw/w*traces+fixed))==0,'protected product normalized return')
    # An unchanged old mark need not survive a replacement by a monitor bit.
    true=s.kronecker_product(s.diag(0,1),s.eye(2))
    aux=s.kronecker_product(s.eye(2),s.diag(0,1))
    require((true-aux).norm(2)==1,'replace vs append')
    require(true*aux==aux*true,'retained truthful old mark')


if __name__=='__main__':
    test_native_pointer()
    test_echo_and_composition()
    test_truthful_product()
    print('PASS: five literal gates, actual birth cut and writer, joint echo sources, mixed-input boundary, truthful product and old-return derivatives.')
