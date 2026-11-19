"""Exact operator controls for the supplied Book return terminal E=(1-z)I+zP.

Sources report (-log det H) in natural units. Numbers below give its
differential; divide by log(phi) for golden code units. No economic weight
is assigned or inferred for an unmarked original history.
"""
import json
import sympy as s


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


def zero(expr):
    if isinstance(expr,s.MatrixBase):
        return all(s.simplify(x)==0 for x in expr)
    return s.simplify(expr)==0


def scalar(x):
    return str(s.factor(x))


def arbitrary_binary_matrix():
    # Polynomial verification for unrestricted 2x2 entries. Hermitian
    # effects and arbitrary Hermitian directions are included.
    x,y,u,v = s.symbols("x y u v")
    M=s.Matrix([[x,y],[u,v]])
    A=s.Matrix(2,2,s.symbols("k0:4"))
    z,dz,t=s.symbols("z dz t")
    I=s.eye(2)
    H=(1-z)*I+z*M
    C=M*(I-M)
    # Right-multiply N-M=z C H^{-1} by H; no inverse simplifications.
    require(zero(M-M*H-z*C),"arbitrary 2x2 mark-shift operator")
    require(zero(M*H-H*M),"right and left return resolvents coincide")
    Dt=((1-z-t*dz)*I+(z+t*dz)*(M+t*A)).det().diff(t).subs(t,0)
    Dh=z*A-dz*(I-M)
    require(zero(Dt-s.trace(H.adjugate()*Dh)),"moving determinant incl. noncommuting direction")
    return {"entry_scope":"arbitrary 2x2 algebraic matrices on det H != 0",
            "trace_determinant_source":"-z Tr(H^-1 DM) + Dz Tr(H^-1 (I-M))"}


def interior(z):
    I=s.eye(2)
    U=s.Matrix([[3,-4],[4,3]])/5
    eig=[s.Rational(1,4),s.Rational(3,4)]
    f=lambda values:U*s.diag(*values)*U.T
    M=f(eig)
    V=f([s.sqrt(a) for a in eig]).col_join(f([s.sqrt(1-a) for a in eig]))
    P=s.diag(1,1,0,0); E=(1-z)*s.eye(4)+z*P
    H=(1-z)*I+z*M
    h=[1-z+z*a for a in eig]
    sqrtH=f([s.sqrt(a) for a in h])
    invsqrtH=f([1/s.sqrt(a) for a in h])
    Ehalf=s.diag(1,1,s.sqrt(1-z),s.sqrt(1-z))
    B=Ehalf*V*invsqrtH
    N=M*H.inv()
    require(zero(V.T*V-I) and zero(V.T*P*V-M) and zero(V.T*E*V-H),"actual rectangular dilation")
    require(zero(B.T*B-I) and zero(B.T*P*B-N),"weighted projection compression")
    A=s.Matrix([[1,2],[2,-1]])/9
    require(not zero(M*A-A*M),"witness changes eigenbasis")
    C=M*(I-M); shift=N-M
    score=-s.trace(C.inv()*shift*A)
    require(zero(score+z*s.trace(H.inv()*A)),"noncommuting source comparison")
    rho=s.Matrix([[s.Rational(2,3),s.Rational(1,9)],
                  [s.Rational(1,9),s.Rational(1,3)]])
    require(rho.det()>0 and not zero(rho*M-M*rho),"faithful noncommuting original input")
    q=s.trace(rho*M); mass=s.trace(rho*H)
    q_same=s.trace(rho*N)
    rho_weighted=sqrtH*rho*sqrtH/mass
    q_new=s.trace(rho_weighted*N)
    require(zero(s.trace(rho_weighted)-1) and zero(q_new-q/mass),"reweighted input")
    require(q_new>q_same>q,"strict Jensen difference for fixed mixed preparation")
    require(zero(B*rho_weighted*B.T-Ehalf*V*rho*V.T*Ehalf/mass),
            "complete output incl. coherences")
    # The normalized mass for an input density is not log det H.
    dz=s.Rational(2,7); drho=s.diag(s.Rational(1,10),-s.Rational(1,10))
    mixed=-s.trace(drho*H+rho*(z*A-dz*(I-M)))/mass
    matrix=score+dz*s.trace(H.inv()*(I-M))
    require(not zero(mixed-matrix) and not zero(s.trace(drho*H)),"moving input source")
    return {"z":str(z),"native_q_for_fixture":scalar(q),"same_input_Doob_q":scalar(q_same),
            "reweighted_input_Doob_q":scalar(q_new),"exact_Jensen_gap":scalar(q_new-q_same),
            "fixed_z_negative_logdet_source_noncommuting":scalar(score),
            "moving_z_negative_logdet_source":scalar(matrix),
            "moving_input_and_z_negative_log_trace_mass_source":scalar(mixed)}


def boundary():
    M=s.diag(0,s.Rational(1,2),1); I=s.eye(3)
    z=s.Rational(1,3); dz=s.Rational(1,5)
    H=(1-z)*I+z*M
    K=s.Matrix([[0,-2,1],[2,0,-3],[-1,3,0]])
    # A legitimate two-sided curve: conjugate diag(t^2,1/2+t/5,1-t^2)
    # by the orthogonal Cayley transform of tK/2; its derivative at zero is K.
    A=K*M-M*K+s.diag(0,s.Rational(1,5),0)
    require(A[0,0]==A[2,2]==0 and not zero(M*A-A*M),"two-sided endpoint tangent")
    C=M*(I-M); D=M*H.inv()-M
    observed=-s.trace(C.pinv()*D*A)
    direct=-z*s.trace(H.inv()*A)
    require(zero(observed-direct),"pseudoinverse including both boundary eigenspaces")
    t=s.Symbol("t")
    e=[t**2,s.Rational(1,2)+t/5,1-t**2]
    Z=z+dz*t
    det=s.prod(1-Z+Z*ev for ev in e)
    whole=-det.diff(t).subs(t,0)/det.subs(t,0)
    correction=dz*s.trace(H.inv()*(I-M))
    require(zero(whole-direct-correction),"moving z including 0-eigenspace")
    outward=s.diag(1,0,0)
    lost=-z*s.trace(H.inv()*outward)+s.trace(C.pinv()*D*outward)
    require(lost==-z/(1-z),"one-sided incoming zero mode invalidates pseudoinverse rule")
    return {"two_sided_fixed_z":scalar(direct),"moving_z_increment":scalar(correction),
            "joint_source":scalar(whole),"one_sided_source_lost_by_pseudoinverse":scalar(lost)}


def diagonal_weights():
    # Three projected readouts of one complete rectangular isometry. On
    # its input, the compressed effects are pairwise noncommuting rank one.
    rt=s.sqrt(3); I=s.eye(2)
    V=s.sqrt(s.Rational(2,3))*s.Matrix([[1,0],[-s.Rational(1,2),rt/2],
                                         [-s.Rational(1,2),-rt/2]])
    M=[V.row(i).T*V.row(i) for i in range(3)]
    require(zero(sum(M,s.zeros(2))-I) and not zero(M[0]*M[1]-M[1]*M[0]),"genuine POVM")
    w=[s.Rational(1,3),s.Rational(1,2),s.Integer(1)]
    H=sum((a*b for a,b in zip(w,M)),s.zeros(2))
    # The 2x2 positive square root formula avoids choosing eigenvectors.
    rootdet=s.sqrt(H.det())
    sqrtH=(H+rootdet*I)/s.sqrt(s.trace(H)+2*rootdet)
    invsqrt=sqrtH.inv()
    t=s.Symbol("t")
    yields=[]
    for i,wi in enumerate(w):
        # Cyclic trace of B*P_iB; all matrices refer to this same V.
        score=s.factor(wi*s.trace(H.inv()*M[i]))
        require(zero(s.trace(wi*invsqrt*M[i]*invsqrt)-score),"normalized mark trace")
        det=(H+t*wi*M[i]).det()
        require(zero(det.diff(t).subs(t,0)/det.subs(t,0)-score),"exact weight-log derivative")
        yields.append(score)
    require(zero(sum(yields)-2),"total rank of native input cut")
    return {"input_rank":2,"marks":3,"d_logdet_per_d_log_weight":[scalar(a) for a in yields]}


if __name__=="__main__":
    result={"status":"PASS","original_owner":"PR334 0716b659d, primary 192639-192686: original full-isometry construction; original mark shift explicitly scalar",
            "source_units":"natural logarithm; divide sources by ln(phi) for golden code units",
            "symbolic":arbitrary_binary_matrix(),
            "regular_controls":[interior(s.Rational(1,3)),interior(s.Rational(1,2**20))],
            "spectral_endpoints":boundary(),"diagonal_weight_derivatives":diagonal_weights(),
            "domain":"exact matrix controls of the supplied E, not an assigned economic tariff or implementation on H.1",
            "physical_price_binding_proved":False,"GR_closed":False}
    print(json.dumps(result,indent=2))
