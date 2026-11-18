"""Exact finite checks of the joint Palatini/matter residual and Golden bit."""
from fractions import Fraction as F
from itertools import product
from math import prod

import sympy as sp

P = (sp.sqrt(5)-1)/2
A = sp.sqrt(P)
H = F(1,4)


def reduced_row():
    # EPS_PLUS stencil: Delta_perp H + 4 lambda |D_u^+ Psi|^2.
    # Nine separate moving denominators, including two for each polarization.
    s = sp.symbols("s", real=True)
    lam = sp.symbols("lambda", nonzero=True)
    coords = [(0,0),(H,0),(-H,0),(0,H),(0,-H)]
    psi = [sp.Rational(1,8),sp.Rational(3,32),sp.Rational(-1,16),sp.Rational(-1,32)]
    velocity = sum(((psi[k+1]-psi[k])/H)**2 for k in (0,2))
    heights = [-lam*velocity*(x*x+y*y) for x,y in coords]
    heights[0] += s
    values = heights+psi
    den = [(i+2+s)/(i+13) for i in range(9)]  # strictly positive for |s|<1
    num = [d*x for x,d in zip(values,den)]
    lap_weights = [-4,1,1,1,1]
    common = prod(den[:5])*prod(den[5:])**2
    lap = sum(w*num[i]*sp.cancel(common/den[i]) for i,w in enumerate(lap_weights))
    kinetic = 0
    for i in (5,7):
        difference=num[i+1]*den[i]-num[i]*den[i+1]
        kinetic+=difference**2*sp.cancel(common/(den[i]*den[i+1])**2)
    cleared=(lap+4*lam*kinetic)/H**2
    assert sp.cancel(cleared/common+4*s/H**2)==0
    assert sp.cancel(cleared.diff(s).subs(s,0)+4*common.subs(s,0)/H**2)==0
    assert sp.cancel(common.diff(s).subs(s,0))>0
    assert sp.cancel((cleared**2).diff(s,2).subs(s,0)-2*(4*common.subs(s,0)/H**2)**2)==0
    print("Reduced Einstein row and its measured numerator agree with nine moving denominators.")


def wave_on_collar():
    sites=list(product(range(4),repeat=4))
    interior=[x for x in sites if all(x[k] in (1,2) for k in (0,2,3))]
    ix={x:j for j,x in enumerate(interior)}
    def shift(x,j,ds):
        v=list(x); v[j]=(v[j]+ds)%4
        return tuple(v)
    def row(x,read):
        total=0
        for mu,nu,sign in ((0,1,1),(1,0,1),(2,2,-1),(3,3,-1)):
            prev=shift(x,mu,-1)
            total+=sign*(read(shift(x,nu,1))-read(x)-read(shift(prev,nu,1))+read(prev))
        return total*16
    W=sp.Matrix([[row(s,lambda x:int(x==v)) for v in interior] for s in interior])
    # Match all 32x32 entries to the independent A73 owner, in the same
    # units (both include h^-2=16 and take the same Lorentz sign).
    from pathlib import Path
    import sys
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"round73/matter"))
    import check_matter_root as a73
    a73_indices=[a73.core.site_index(x) for x in interior]
    assert [a73.SITES[i] for i in a73_indices]==interior
    for k,j in enumerate(a73_indices):
        basis=[0]*len(a73.SITES)
        basis[j]=1
        assert [a73.wave_equation(basis,i) for i in a73_indices]==list(W.col(k))
    Z=sp.Matrix([[(-1)**v,(-1)**(u+v+x+y)] for u,v,x,y in interior])
    assert W==W.T and W*Z==sp.zeros(32,2) and Z.rank()==2
    def modular_rank(matrix,prime=1009):
        a=[[int(c)%prime for c in matrix.row(i)] for i in range(matrix.rows)]
        r=0
        for j in range(matrix.cols):
            k=next((k for k in range(r,len(a)) if a[k][j]),None)
            if k is None:
                continue
            a[r],a[k]=a[k],a[r]
            inv=pow(a[r][j],-1,prime)
            for k in range(r+1,len(a)):
                mult=a[k][j]*inv%prime
                a[k]=[(v-mult*u)%prime for v,u in zip(a[k],a[r])]
            r+=1
        return r
    M=sp.diag(*[i+1 for i in range(32)])
    assert modular_rank(W)==modular_rank(W.T*M*W)==30
    assert all(row(s,lambda x:F(x[0],4)*(F(x[0],4)-H))==0 for s in interior)
    # For positive weights that move along the perturbation, the Hessian at
    # a true wave root remains 2 W^T M(0) W, including both null modes.
    t=sp.symbols("t",real=True)
    d=sp.Matrix([int(i==ix[(1,1,2,2)]) for i in range(32)])
    residual=t*(W*d)
    energy=sum((i+1+t**2)*ri**2 for i,ri in enumerate(residual))
    assert energy.diff(t,2).subs(t,0)==2*(d.T*W.T*M*W*d)[0]>0
    assert (W.T*M*W)*Z==sp.zeros(32,2)
    print("Actual 32-site collar has rank 30 and both alternating modes survive positive weighting.")


def independent_reports():
    # A tested cell of the signed, normalized response; Y includes an abort.
    law={-1:F(1,5),0:F(1,2),1:F(3,10)}
    assert sum(law.values())==1
    mean=sum(y*w for y,w in law.items())
    second=sum(y*y*w for y,w in law.items())
    independent=sum(a*b*wa*wb for a,wa in law.items() for b,wb in law.items())
    assert independent==mean**2==F(1,100) and second==F(1,2)
    balanced={-1:F(1,4),0:F(1,2),1:F(1,4)}
    assert sum(a*b*wa*wb for a,wa in balanced.items() for b,wb in balanced.items())==0
    assert sum(y*y*w for y,w in balanced.items())>0
    # Given a shared hidden unbiased sign, the two deterministic reports are
    # conditionally independent, yet their unconditional mixed moment is 1.
    assert sum(F(1,2)*y*y for y in (-1,1))==1
    assert sum(F(1,2)*y for y in (-1,1))**2==0
    print("Independent signed reports square their means; duplication and a shared hidden sign fail.")


def golden_output():
    r,p,ell=sp.symbols("r p ell",positive=True)
    h=-(r*sp.log(r)+(1-r)*sp.log(1-r))/ell
    length=1+r
    # log p=-ell and log(p²)=-2ell, ell=ln(phi)>0.
    gain=((1-r)*(sp.log(1-r)+ell)+r*(sp.log(r)+2*ell))/ell
    assert sp.simplify(length-gain-h)==0
    assert sp.simplify((length-h).diff(r)-(1-sp.log((1-r)/r)/ell))==0
    assert sp.simplify(h.diff(r)-sp.log((1-r)/r)/ell)==0
    assert sp.simplify((1-P**2)/P**2-1/P)==0
    # For p²<r<1/2, the odds are strictly between 1 and phi.
    assert sp.simplify((P-P**2)-P**3)==0
    assert sp.simplify(P**2+P**3/2-sp.Rational(1,2))==0
    x=sp.symbols("x",nonnegative=True)
    assert sp.simplify((1-x)*P**2+x*P-(P**2+P**3*x))==0
    # With the event retained, it is the conditional entropy that enters the
    # increment: h_phi(p)=h_phi(p²)=1+p². Matched gain reverses which cost
    # is constant compared with the coarse marginal.
    hgold=P+2*P**2
    assert sp.simplify(1+(1-x)*P**2+x*P-hgold-P**3*x)==0
    assert sp.simplify((1-x)*hgold+x*hgold-hgold)==0

    # B135: literal 2-control Gray AND. In Gray order, parity conjugates a
    # power of G by X G X=G^-1. Walsh coefficients are never gate angles.
    G=sp.Matrix([[A,-P],[P,A]])
    X=sp.Matrix([[0,1],[1,0]])
    assert sp.simplify(X*G*X-G.T)==sp.zeros(2)
    gray=((0,0),(0,1),(1,1),(1,0))
    truth=dict((bits,int(all(bits))) for bits in product((0,1),repeat=2))
    character=lambda z,b:(-1)**sum(x*y for x,y in zip(z,b))
    coef=[sum(truth[b]*character(z,b) for b in truth) for z in gray]
    for a0,a1 in truth:
        bits=(a0,a1)
        signed=sum(k*character(z,bits) for k,z in zip(coef,gray))
        assert signed==4*truth[bits]
        # Return all controls and the orientation of the target after the
        # full cycle. For zero flag input the active conditional effect is nu.
        net=sp.eye(2); old=gray[0]
        for z,k in zip(gray,coef):
            flip=sum((b^c)*i for b,c,i in zip(old,z,bits))%2
            net=(G if k==1 else G.T)*(X if flip else sp.eye(2))*net
            old=z
        flip=sum(i*j for i,j in zip(old,bits))%2
        net=(X if flip else sp.eye(2))*net
        assert sp.simplify(net-G**signed)==sp.zeros(2)
    nu=16*P**9
    assert sp.simplify((G**4)[1,0]**2-nu)==0 and 0<nu<sp.Rational(1,2)
    # On the actual fresh v=G|0>, same two controls, choose k=3. The
    # inactive flag sees G^1|0> and the active flag G^13|0>.  An exact
    # Chebyshev polynomial at 2*cos(theta)^2-1 needs only Q(sqrt(5)).
    active=(1-sp.chebyshevt(13,2*P-1))/2
    inactive=(1-sp.chebyshevt(1,2*P-1))/2
    assert sp.simplify(inactive-P**2)==0
    assert all(3*sum(k*character(z,b) for z,k in zip(gray,coef))==12*truth[b] for b in truth)
    # Strict endpoint comparisons use integer squares, with no numeric trig.
    rational,radical=sp.expand(active).as_coeff_Add()
    coeff=sp.simplify(radical/sp.sqrt(5))
    assert coeff.is_Rational and rational.is_Rational
    def sign_exact(const,rad):
        if const>=0 and rad>=0:
            return 1 if const or rad else 0
        if const<=0 and rad<=0:
            return -1
        return sp.sign(const)*sp.sign(const**2-5*rad**2)
    low=sp.Rational(4782740,10**7)
    high=sp.Rational(4782741,10**7)
    assert sign_exact(rational-low,coeff)==sign_exact(high-rational,-coeff)==1
    assert P**2<low<high<sp.Rational(1,2)
    print("Fresh canonical v, two controls, k=3: p² < 0.4782740 < sin²(13 theta) < 0.4782741 < 1/2.")
    # A nonzero inactive-probability margin puts the marginal in the open
    # overlap even at a true residual zero.
    for base in (sp.Rational(1,4),sp.Rational(3,4)):
        q=P**2+P**3*nu*base
        assert P**2<q<sp.Rational(1,2)
    print("Both Golden price derivatives have the required sign on (p²,1/2); "
          "the finite two-control word has exact active mass 16p⁹.")


def configured_feedback():
    x,z,p,k,sign=sp.symbols("x z p k sign")
    f,q=sp.symbols("f q")
    E=p**2*(1+k*f)
    b=(p+sign*p**2*k*q)**2
    B=4*b*(1-b)
    lam=4*E*(1-E)
    Q0=1-z*B
    R0=1-z*(lam+(1-lam)*B)
    J=-528*(sp.log(Q0)+sp.log(R0))
    # Use both codirections. Off the null layer Q and R move independently;
    # no constant first-source multiplier is substituted in the two-band law.
    for v in (f,q):
        proposed=-528*(Q0.diff(v)*R0+R0.diff(v)*Q0)/(Q0*R0)
        assert sp.cancel(J.diff(v)-proposed)==0
    print("Both off-shell derivatives of the configured two-tick log feedback are rational.")


if __name__=="__main__":
    reduced_row()
    wave_on_collar()
    independent_reports()
    golden_output()
    configured_feedback()
