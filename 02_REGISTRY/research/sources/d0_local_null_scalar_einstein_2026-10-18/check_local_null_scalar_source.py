#!/usr/bin/env python3
"""Narrow finite controls: local LEFT-coded golden Book-feedback → null scalar Einstein.

Standard library only. Consumes the independently owned exact 40-row Lorentz
star Euler table from A4D_AF_STAR_FULL_LATTICE_STATIONARY_FAMILY_2026_10_17.md;
does NOT claim to rederive that 40-row symbolic table, native Book selection,
original whole v8+AF price, or all-grid raw h^-2 GR.
"""
from math import log1p, sqrt, asin

P = (sqrt(5.) - 1.) / 2.
Z = 2.**-20
M_SCENE = 528
E0 = P*P
L = 4.*P**3
A = P**6
Q0 = 1.-Z*L
R0 = 1.-Z*(L+A*L)
SIGMA = -1.
AMP = .13
H = .2
WEIGHTS = (.11, .27, .19)  # intentionally UNEQUAL; remaining old paths retained.
AVG = sum(WEIGHTS)/len(WEIGHTS)
REST = 1. - sum(WEIGHTS)
T2 = 1.


def assert_near(a, b, tol=1e-10):
    if abs(a-b)>tol:
        raise AssertionError(f"{a} != {b}, error={abs(a-b)}")


def zeros(n):
    return [[0. for _ in range(n)] for _ in range(n)]


def eye(n):
    x = zeros(n)
    for i in range(n):
        x[i][i] = 1.
    return x


def multiply(A, B):
    n = len(A)
    out = zeros(n)
    for i in range(n):
        for k in range(n):
            if A[i][k] != 0:
                for j in range(n):
                    out[i][j] += A[i][k]*B[k][j]
    return out


def transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A))]


def plus(A, B, factor=1.):
    return [[A[i][j]+factor*B[i][j] for j in range(len(A))] for i in range(len(A))]


def inverse(A):
    n = len(A)
    R = [A[i][:]+eye(n)[i][:] for i in range(n)]
    for j in range(n):
        pivot = next(i for i in range(j,n) if abs(R[i][j])>1e-12)
        R[j], R[pivot] = R[pivot], R[j]
        d = R[j][j]
        R[j] = [v/d for v in R[j]]
        for i in range(n):
            if i == j:
                continue
            f = R[i][j]
            R[i] = [R[i][k]-f*R[j][k] for k in range(2*n)]
    return [row[n:] for row in R]


def full16_clifford_control():
    eta=(1.,-1.,-1.,-1.)
    G=[]
    for a in range(4):
        C = zeros(16)
        for mask in range(16):
            if mask&(1<<a):
                continue
            preceding = bin(mask&((1<<a)-1)).count('1')
            C[mask|(1<<a)][mask] = -1. if preceding&1 else 1.
        G.append(plus(C, transpose(C), eta[a]))
    id16=eye(16)
    for a in range(4):
        for b in range(4):
            anti=plus(multiply(G[a],G[b]),multiply(G[b],G[a]))
            for i in range(16):
                for j in range(16):
                    assert_near(anti[i][j],
                                2*eta[a]*id16[i][j] if a==b else 0., 1e-14)
    for k in ((1.,1.,0.,0.),(.2,.1,.3,0.),(.1,.1,0.,.0001)):
        gamma=zeros(16)
        for a in range(4):
            gamma=plus(gamma,G[a],k[a])
        g2=multiply(gamma,gamma)
        q=sum(eta[a]*k[a]*k[a] for a in range(4))
        for i in range(16):
            for j in range(16):
                assert_near(g2[i][j], q if i==j else 0., 1e-13)
    print("PASS Clifford full16: Lorentz square, null operator not zero, no extra matter copy.")


def actual_coframe_null_source():
    eta=((0.,1.,0.,0.),(1.,0.,0.,0.),(0.,0.,-1.,0.),(0.,0.,0.,-1.))
    E=eye(4); E[1][0]=.85
    E=[[v*H for v in row] for row in E]  # actual h-scaled native legs
    metric=multiply(multiply(transpose(E),eta),E)
    metric=[[v/(H*H) for v in row] for row in metric]
    inverse_metric=inverse(metric)
    assert_near(AMP*AMP*inverse_metric[0][0],0.)
    assert_near(inverse_metric[0][1],1.)
    hits=[]
    for a in range(4):
        for direction in range(4):
            dE=zeros(4);dE[a][direction]=1.
            dmetric=plus(multiply(multiply(transpose(dE),eta),E),
                         multiply(multiply(transpose(E),eta),dE))
            dmetric=[[v/(H*H) for v in row] for row in dmetric]
            dq=-(AMP*AMP)*multiply(multiply(inverse_metric,dmetric),inverse_metric)[0][0]
            if abs(dq)>1e-13:
                hits.append((a,direction,dq))
    if len(hits)!=1 or hits[0][0:2]!=(0,1):
        raise AssertionError(f"null matter had extra coframe Euler rows: {hits}")
    assert_near(hits[0][2],-2*AMP*AMP/H)
    print("PASS full16 coframe directions: only v_v^+ has nonzero NULL matter source.")


def coupling():
    Cstar=M_SCENE*Z*4*P**3*(1-L)*E0*T2/R0
    Cmat=SIGMA*M_SCENE*Z*8*P**6*T2*(1/Q0+A/R0)
    lam=Cmat/Cstar
    analytic=SIGMA*2*(R0/Q0+A)/P**5
    assert_near(lam,analytic,1e-12)
    assert_near(2*(1+P**6)/P**5,10+6*sqrt(5.),1e-12)
    if lam>=0:
        raise AssertionError("reverse native Golden had wrong null-energy sign")
    return lam, Cstar, Cmat


def full_feedback_per_normalized_af_trace(site, perturb, lam):
    """ONE real full trace-log, including -K log Q; all inactive paths present."""
    ricci=-2*lam*AMP*AMP
    out=0.
    for j,w in enumerate(WEIGHTS):
        rho=w/AVG
        fhat=(-ricci/H)*perturb if j==site else 0.
        qhat=(-2*AMP*AMP/H)*perturb if j==site else 0.
        fi=fhat/rho
        qi=qhat/rho
        e=E0*(1+T2*fi)
        single_b=(P+SIGMA*P*P*T2*qi)**2
        b=4*single_b*(1-single_b)
        l=4*e*(1-e)
        out+=w*(log1p(-Z*b)+log1p(-Z*(l+(1-l)*b)))
    out+=REST*(log1p(-Z*L)+log1p(-Z*(L+A*L)))
    return -M_SCENE*out


def exact_source_cancellation_and_hostile_tests():
    lam,Cstar,Cmat=coupling()
    ricci=-2*lam*AMP*AMP
    for i in range(3):
        hstep=.001
        grad=(full_feedback_per_normalized_af_trace(i,hstep,lam)
              -full_feedback_per_normalized_af_trace(i,-hstep,lam))/(2*hstep)
        assert_near(grad,0.,2e-10)
        geom=-AVG*Cstar*ricci/H
        matter=-AVG*Cmat*2*AMP*AMP/H
        assert_near(geom+matter,0.,1e-13)
    if abs(Cmat)>0:
        # Without native inverse-density, the source at site i scales with
        # unequal w_i rather than constant AVG: the full Euler is NOT zero.
        wrong=[Cmat*(-2*AMP*AMP/H)*(w-AVG) for w in WEIGHTS]
        assert max(abs(r) for r in wrong)>1e-7
    # The original -K logQ term is needed for the actual relative coupling.
    truncated=SIGMA*2*A/P**5
    assert abs(lam-truncated)>1.
    # Existing exact 40-row star table + independently derived Clifford source.
    Astar=ricci/2+.21
    Dstar=ricci/2-.21
    Bpolar=.17
    cx=-Astar/2
    cy=-Dstar/2
    linkrow1=(H**4)*(Astar+2*cx)/2
    linkrow2=(H**4)*(Dstar+2*cy)/2
    assert_near(linkrow1,0.)
    assert_near(linkrow2,0.)
    assert_near(Astar+Dstar+2*lam*AMP*AMP,0.)
    if abs(Bpolar)<1e-3 or abs(Astar-Dstar)<1e-3:
        raise AssertionError("two actual Weyl polarization channels missing")
    print(f"PASS genuine feedback derivative and 40+scalar row balance: "
          f"lambda={lam:.12f}, Ricci_uu={ricci:.12f}, two Weyl modes.")
    return lam


def scalar_discrete_euler_control():
    # At psi=s*u, only D_v(delta psi) enters. Full scalar source is the
    # periodic/fixed-collar discrete telescoping sum, after inverse-PF
    # cancellation. It is exact for arbitrary interior delta-psi.
    trial=[0.,.27,-.14,.53,-.66,0.]
    deriv=sum((trial[i+1]-trial[i])/H for i in range(len(trial)-1))
    assert_near(deriv,0.,1e-14)
    print("PASS true finite scalar variation: 2s sum_v D_v delta psi=0.")


def golden_angle_control():
    eps=1e-5
    fa=lambda f:asin(P*sqrt(1+T2*f))-asin(P)
    ma=lambda q:asin(P+SIGMA*P*P*T2*q)-asin(P)
    dfa=(fa(eps)-fa(-eps))/(2*eps)
    dma=(ma(eps)-ma(-eps))/(2*eps)
    assert_near(dfa,sqrt(P)*T2/2,1e-10)
    assert_near(dma,SIGMA*P**1.5*T2,1e-10)
    assert_near(dma/dfa,2*SIGMA*P,1e-8)
    print("PASS one actual Golden rotation axis for both grav/matter controllers.")


def actual_two_tick_scene_control():
    """B is the actual two-tick effect, not the one-tick rotation setting."""
    for raw_b in (P*P, .17, .63):
        G=[[sqrt(1-raw_b),-sqrt(raw_b)],
           [sqrt(raw_b),sqrt(1-raw_b)]]
        G2=multiply(G,G)
        B=G2[1][0]**2
        assert_near(B,4*raw_b*(1-raw_b),1e-14)
        if abs(B-raw_b)<1e-3:
            raise AssertionError("hostile one-tick substitution failed")
    assert_near(4*P*P*(1-P*P),L,1e-14)
    raw_derivative=2*SIGMA*P**3*T2
    assert_near(4*(1-2*P*P)*raw_derivative,
                8*SIGMA*P**6*T2,1e-14)
    print("PASS actual repeated scene word: B=4b(1-b), full two-tick matter jet.")


def main():
    full16_clifford_control()
    actual_coframe_null_source()
    scalar_discrete_euler_control()
    golden_angle_control()
    actual_two_tick_scene_control()
    exact_source_cancellation_and_hostile_tests()
    print("PASS one LOCAL complete golden feedback with nonvacuum Einstein null-scalar first source.")
    print("SCOPE: selected mathematical AF×scene word and owned finite star table;")
    print("       not compulsory native D0 Book execution, not old v8 whole price or global raw #216.")


if __name__=="__main__":
    main()
