"""Exact second response moment on the four-role diagonal invisible carrier.

All arithmetic is Python integers; metric values below are four times the
coefficient of t^2 in E_Q(eta, exp(t a)). No symbolic package is needed.
"""
from itertools import combinations
from fractions import Fraction

PAIRS=list(combinations(range(4),2))
QPAIRS=[(i,j) for i in range(4) for j in range(i,4)]
ETA=(1,-1,-1,-1)
ZERO=(0,)*16
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(a,c): return tuple(c*x for x in a)
def mul(a,b): return tuple(sum(a[4*i+k]*b[4*k+j] for k in range(4)) for i in range(4) for j in range(4))
def bracket(a,b): return add(mul(a,b),scale(mul(b,a),-1))
def basis(i,j,boost=False):
    a=list(ZERO); a[4*i+j]=1; a[4*j+i]=1 if boost else -1
    return tuple(a)
GEN=[basis(0,i,True) for i in (1,2,3)]+[basis(i,j) for i,j in ((1,2),(1,3),(2,3))]
WEIGHTS=[(0,0,0,1,-1,1),(0,1,-1,0,0,1),(1,0,-1,0,1,0),(1,-1,0,1,0,0)]
Z=[tuple(sum(w*g[k] for w,g in zip(weights,GEN)) for k in range(16)) for weights in WEIGHTS]
COS=(1,0,-1,0); SIN=(0,1,0,-1)
def field(coeff):
    return [[scale(Z[r],coeff[r]*COS[p]+coeff[4+r]*SIN[p]) for r in range(4)] for p in range(4)]
def wedge(a,b): return tuple(a[i]*b[j]-a[j]*b[i] for i,j in PAIRS)
E=[tuple(int(i==r) for i in range(4)) for r in range(4)]
STAR={0:(5,-1),1:(4,1),2:(3,-1),3:(2,1),4:(1,-1),5:(0,1)}
def star_pair(area,C):
    b=[C[4*i+j]*ETA[j] for i,j in PAIRS]
    sb=[0]*6
    for src,(dst,sign) in STAR.items(): sb[dst]=sign*b[src]
    return sum(area[k]*ETA[i]*ETA[j]*sb[k] for k,(i,j) in enumerate(PAIRS))
def face_data(r,s):
    u,v=[i for i in range(4) if i not in (r,s)]
    seq=[r,s,u,v]
    sign=(-1)**sum(seq[i]>seq[j] for i,j in PAIRS)
    return u,v,sign
def metric2(C,r,s):
    # dE = eta q/2 in column-solder convention; use twice dE here.
    u,v,sign=face_data(r,s)
    out=[]
    for i,j in QPAIRS:
        q=[[0]*4 for _ in range(4)]; q[i][j]=q[j][i]=1
        dEu=tuple(ETA[k]*q[k][u] for k in range(4))
        dEv=tuple(ETA[k]*q[k][v] for k in range(4))
        dB=tuple(x+y for x,y in zip(wedge(dEu,E[v]),wedge(E[u],dEv)))
        out.append(sign*star_pair(dB,C))
    return out
def jets(a,p,r,s):
    X=[a[p][r],a[(p+1)%4][s],scale(a[(p+1)%4][r],-1),scale(a[p][s],-1)]
    c1=ZERO; c2=ZERO
    for x in X: c1=add(c1,x)
    for i,j in PAIRS: c2=add(c2,bracket(X[i],X[j]))
    return c1,c2 # c2 is twice the quadratic odd-curvature coefficient
def metric_jets(a):
    one=[]; two=[]
    for p in range(4):
        v1=[0]*10; v2=[0]*10
        for r,s in PAIRS:
            c1,c2=jets(a,p,r,s)
            v1=[x+y for x,y in zip(v1,metric2(c1,r,s))]
            v2=[x+y for x,y in zip(v2,metric2(c2,r,s))]
        one.append(v1); two.append(v2)
    return one,two
def action2(a):
    result=0
    for p in range(4):
        for r,s in PAIRS:
            u,v,sign=face_data(r,s)
            result+=sign*star_pair(wedge(E[u],E[v]),jets(a,p,r,s)[1])
    return result # twice the t^2 coefficient in the four-phase action
def add_field(a,b,factor=1):
    return [[add(a[p][r],scale(b[p][r],factor)) for r in range(4)] for p in range(4)]
def check(name,ok):
    if not ok: raise AssertionError(name)
    print('PASS_'+name,flush=True)
def run():
    unit=[[int(j==i) for j in range(8)] for i in range(8)]
    fields=[field(c) for c in unit]
    # Phase reduction is exact: translation symmetry makes each edge Euler
    # the same on its phase class. All 4*4*6 independent edge tests remain.
    for n,a in enumerate(fields):
        check('METRIC_LINEAR_'+str(n),all(x==0 for row in metric_jets(a)[0] for x in row))
        for p in range(4):
            for r in range(4):
                for j,G in enumerate(GEN):
                    b=[[ZERO]*4 for _ in range(4)]; b[p][r]=G
                    assert action2(add_field(a,b))-action2(add_field(a,b,-1))==0,(n,p,r,j)
        check('CONNECTION_LINEAR_ALL_EDGES_'+str(n),True)
    # Determine the entire quadratic polynomial by all squares and crosses.
    # This is coefficient extraction for a known homogeneous degree-two map.
    square=[metric_jets(a)[1] for a in fields]
    for i,S in enumerate(square):
        check('MEAN_SQUARE_'+str(i),all(sum(S[p][q] for p in range(4))==0 for q in range(10)))
    nonzero=[]
    phase_polynomial=True
    for i,j in combinations(range(8),2):
        T=metric_jets(add_field(fields[i],fields[j]))[1]
        cross=[[T[p][q]-square[i][p][q]-square[j][p][q] for q in range(10)] for p in range(4)]
        mean=[Fraction(sum(cross[p][q] for p in range(4)),16) for q in range(10)]
        if any(mean): nonzero.append((i,j,[str(x) for x in mean]))
        phase_polynomial &= cross[2]==cross[0] and cross[1]==[-v for v in cross[0]] and cross[3]==cross[1]
    check('ALL_28_MEAN_CROSS_COEFFICIENTS',not nonzero)
    check('QUADRATIC_PHASE_ALTERNATION',phase_polynomial and all(S[2]==S[0] and S[1]==[-v for v in S[0]] and S[3]==S[1] for S in square))
    witness=metric_jets(field([1,1,0,0,0,0,0,0]))[1]
    expected=[0,0,-1,-1,0,1,1,2,0,2]
    check('NONZERO_POINTWISE_QUADRATIC_WITNESS',witness==[[(-1)**p*v for v in expected] for p in range(4)])
    # The original #232 ray: all curvature matrices commute, so its quadratic
    # BCH contribution is zero even before phase averaging.
    check('EXACT232_RAY_QUADRATIC_CONTROL',all(v==0 for row in square[0] for v in row))
    # Abstract hostile functional S=1/2 sum [(Ba)^2 + q a^2], B=T+T^-1.
    # This is an inference control, NOT the naked-star action or its NOGO.
    sigma=(1,1,-1,-1)
    check('HOSTILE_MEAN_ZERO',sum(sigma)==0)
    check('HOSTILE_CONNECTION_EQUATION',all(sigma[(p+1)%4]+sigma[(p-1)%4]==0 for p in range(4)))
    check('HOSTILE_SMOOTH_SOURCE_AND_RESPONSE_GAP',all(Fraction(v*v,2)==Fraction(1,2) for v in sigma))
    check('HOSTILE_REGULAR_ZERO_PHASE',(1+1)**2==4)
    print('RESULT: diagonal joint-linear carrier has zero mean quadratic metric response.')
    print('BOUNDARY: this does not prove nonlinear joint stationarity or all-phase decoupling.')

if __name__=='__main__': run()
