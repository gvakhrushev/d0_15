#!/usr/bin/env python3
"""Bounded exact controls of the full local AF/star stationary family.

1. Symbolic derivatives for arbitrary a,b,d,x,y,h,cx,cy in all 40 rows.
2. Independent original diag(+---) finite-action checks, using finite
   solder differences and an exact Cayley numerator identity for links.
3. Exact Q(phi) golden address counts, never uniform replacement weights.
4. Off-shell radial intertwiner and its full-source inverse.

No global periodic root, matter binding or physical AF admission is tested.
"""
from functools import lru_cache
from itertools import product
import json
import sympy as s
import star_euler as E


def require(value, label):
    if not value:
        raise ArithmeticError(label)


def symbolic_rows():
    z=(0,0,0,0)
    require(E.density(z)==0, 'pp-wave scalar vanishes even off vacuum')
    solder=E.solder_source(z)
    expected=s.zeros(4); expected[0,1]=-E.h**3*(E.a+E.d)
    require(solder==expected, 'all16 unrestricted symbolic solder rows')
    expected_links=[[s.Integer(0)]*6 for _ in range(4)]
    expected_links[1][1]=E.h**4*(E.a+2*E.cx)/2
    expected_links[1][2]=E.h**4*(E.d+2*E.cy)/2
    links=[E.link_source(z,j) for j in range(4)]
    require(all(s.expand(q-r)==0 for qs,rs in zip(links,expected_links)
                for q,r in zip(qs,rs)), 'all24 unrestricted symbolic link rows')
    sol={E.d:-E.a,E.cx:-E.a/2,E.cy:E.a/2}
    require(solder.subs(sol)==s.zeros(4), 'vacuum solder roots')
    require(all(s.simplify(q.subs(sol))==0 for row in links for q in row),
            'exact backward-difference link roots')
    require(links[1][1].subs({E.cx:0,E.h:1,E.a:1})!=0,
            'uncorrected smooth connection must fail')
    require(solder[0,1].subs({E.h:1,E.a:1,E.d:0})!=0,
            'scalar-zero nonharmonic pp-wave must fail')
    return {'solder_nonzero_before_solving':str(solder[0,1]),
            'link_nonzero_before_solving':[str(links[1][1]),str(links[1][2])],
            'full_rows':40}


ETA=s.diag(1,-1,-1,-1)
T=s.Matrix([[1,s.Rational(1,2),0,0],[1,-s.Rational(1,2),0,0],
            [0,0,1,0],[0,0,0,1]])
TI=T.inv()
G=s.diag(*[ETA[i,i]*ETA[j,j] for i,j in E.PAIRS])
STAR=s.zeros(6)
SM={(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
    (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
for pair,(target,sign) in SM.items():
    STAR[E.PAIRS.index(target),E.PAIRS.index(pair)]=sign
LIE=[]
for i,j in E.PAIRS:
    q=s.zeros(4); q[i,j]=1; q[j,i]=-1
    LIE.append(q*ETA)


def direct_action_controls(counts=None, rescale=True):
    """Reconstruct the original finite action, no differentiated R formula.

    A single rank2 Cayley link appears once in each affected plaquette.
    Each density has denominator q(t)=1-sign*t²/4 and numerator degree<=2.
    Hence q(1)*(S(1)-S(-1))/2 equals its EXACT derivative at zero.
    """
    require(T.T*ETA*T==E.ETA and T.det()==-1, 'null-to-owned-signature map')
    vals={E.a:s.Rational(2,3),E.b:s.Rational(3,5),E.d:s.Rational(-2,3),
          E.cx:s.Rational(-1,3),E.cy:s.Rational(1,3),E.h:s.Rational(1,7),
          E.x:s.Rational(2,5),E.y:s.Rational(-1,3)}
    if counts is not None:
        vals.update({E.h:s.Rational(1,3),E.x:s.Rational(1,3),E.y:s.Rational(1,3)})
    z=(0,0,0,0)
    @lru_cache(None)
    def weight(at):
        if counts is None: return s.Integer(1)
        return s.Rational(3**4*counts[tuple(j+1 for j in at)],sum(counts.values()))
    @lru_cache(None)
    def coframe(at):
        return T*E.coframe(at).subs(vals)/(s.sqrt(weight(at)) if rescale else 1)
    @lru_cache(None)
    def link(at,axis): return T*E.link(at,axis).subs(vals)*TI

    def face(base,r,t,change=None,solder=None):
        P=s.eye(4)
        for at,axis,iv in E.edges(base,r,t):
            U=change[2] if change and (at,axis)==change[:2] else link(at,axis)
            P=P*(ETA*U.T*ETA if iv else U)
        R=(P-ETA*P.T*ETA)/2
        C=R*ETA; cv=s.Matrix([C[i,j] for i,j in E.PAIRS])
        u,v=[j for j in range(4) if j not in (r,t)]
        e=solder if solder is not None else coframe(base)
        W=s.Matrix(E.wedge(e[:,u],e[:,v]))
        return s.simplify(weight(base)*E.EPS((r,t,u,v))*(W.T*G*STAR*cv)[0])

    base_action=sum(face(z,r,t) for r,t in E.PAIRS)
    require(base_action==0,'direct owned-star vacuum density')
    for i,j in product(range(4),repeat=2):
        ev=coframe(z).copy(); ev[i,j]+=1
        changed=sum(face(z,r,t,solder=ev) for r,t in E.PAIRS)
        require(changed-base_action==0, f'direct finite solder row {i},{j}')

    bad_links=[]
    for axis in range(4):
        for X in LIE:
            v=[]
            affected=[]
            for r,t in E.PAIRS:
                if axis in (r,t):
                    other=t if axis==r else r
                    affected.extend([(z,r,t),(E.shift(z,other,-1),r,t)])
            for sign in (1,-1):
                U=(s.eye(4)-sign*X/2).inv()*(s.eye(4)+sign*X/2)*link(z,axis)
                require(U.T*ETA*U==ETA and U.det()==1,'exact Cayley Lorentz')
                v.append(sum(face(at,r,t,change=(z,axis,U)) for at,r,t in affected))
            sign=s.trace(X*X)/2
            derivative=s.simplify((1-sign/4)*(v[0]-v[1])/2)
            if derivative!=0: bad_links.append(derivative)
    P=T*E.plaquette(z,0,2).subs(vals)*TI
    nonflat=P!=s.eye(4)
    require(nonflat,'nonidentity curvature plaquette')
    if rescale:
        require(not bad_links, 'direct finite link derivative')
    else:
        require(bool(bad_links),'untransported nonuniform weights must fail')
    return {'independent_action_rows':40,'signature':'+---','nonidentity_plaquette':nonflat,
            'actual_golden_weights':counts is not None,'weight_transport':rescale,
            'nonzero_link_rows':len(bad_links)}


def mulp(q): return (q[1],q[0]-q[1])
def add(q,r): return (q[0]+r[0],q[1]+r[1])
def sub(q,r): return (q[0]-r[0],q[1]-r[1])


def sign_qp(q):
    """Exact sign of A+B*p = ((2A-B)+B sqrt5)/2 using integers."""
    A,B=q; u=2*A-B; v=B
    if v==0: return (u>0)-(u<0)
    if u==0: return (v>0)-(v<0)
    if (u>0)==(v>0): return (u>0)-(u<0)
    if u*u>5*v*v: return (u>0)-(u<0)
    return (v>0)-(v<0)


def golden_counts(n,L):
    counts={q:0 for q in product(range(L),repeat=4)}
    def rec(rem,depth,left,width):
        if rem==0:
            pos=[]
            for l,w in zip(left,width):
                centre2=(2*l[0]+w[0],2*l[1]+w[1])
                lo,hi=0,L
                while lo+1<hi:
                    k=(lo+hi)//2
                    if sign_qp((L*centre2[0]-2*k,L*centre2[1]))>=0: lo=k
                    else: hi=k
                pos.append(lo)
            counts[tuple(pos)]+=1
            return
        j=depth%4; pw=mulp(width[j])
        ww=width.copy(); ww[j]=pw
        rec(rem-1,depth+1,left,ww)
        if rem>=2:
            ll=left.copy(); ww=width.copy()
            ll[j]=add(left[j],pw); ww[j]=sub(width[j],pw)
            rec(rem-2,depth+1,ll,ww)
    rec(n,0,[(0,0)]*4,[(1,0)]*4)
    return counts


def radial_controls():
    """Generic nonzero/off-shell f and a nilpotent f=0 rank-one block."""
    c=s.Rational(3,2)
    Z=[s.Matrix([2,0,0,0]),s.Matrix([0,3,0,0])]
    f=[s.Rational(2,5),s.Rational(-1,7)]
    df=[s.Matrix([[f[0],0,2,1]]),s.Matrix([[0,2*f[1]/3,-1,4]])]
    b=[s.Rational(1,3),s.Rational(2,5)]
    ds=[c+2*b[i]*f[i] for i in range(2)]
    M=c*s.eye(4)+sum((b[i]*Z[i]*df[i] for i in range(2)),s.zeros(4))
    Mi=s.eye(4)/c-sum((b[i]/(c*ds[i])*Z[i]*df[i] for i in range(2)),s.zeros(4))
    require(M*Mi==s.eye(4) and Mi*M==s.eye(4),'exact off-shell inverse')
    weights=[s.Rational(5,7),s.Rational(8,9)]
    dP=sum((weights[i]*df[i] for i in range(2)),s.zeros(1,4))
    dA=sum((weights[i]*ds[i]*df[i] for i in range(2)),s.zeros(1,4))
    require(dP*M==dA,'full off-shell cotangent intertwiner')
    alpha=s.Matrix([[1,2,3,4]])
    require((dA+alpha)*Mi==dP+alpha*Mi,'retain all independent extra sources')
    Z0=s.Matrix([1,0]); df0=s.Matrix([[0,1]])
    M0=c*s.eye(2)+Z0*df0
    require(M0*(s.eye(2)/c-Z0*df0/c**2)==s.eye(2),'f=0 extension')


def continuum_control():
    u,v=s.symbols('u v')
    coords=(u,v,E.x,E.y)
    H=E.a*E.x**2+2*E.b*E.x*E.y+E.d*E.y**2
    g=E.ETA.copy(); g[0,0]=H
    gi=g.inv()
    gamma=[[[s.simplify(sum(gi[r,j]*(s.diff(g[j,nu],coords[mu])
             +s.diff(g[j,mu],coords[nu])-s.diff(g[mu,nu],coords[j]))/2
             for j in range(4))) for nu in range(4)] for mu in range(4)]
             for r in range(4)]
    def R(r,sigma,mu,nu):
        return s.simplify(s.diff(gamma[r][nu][sigma],coords[mu])
              -s.diff(gamma[r][mu][sigma],coords[nu])
              +sum(gamma[r][mu][j]*gamma[j][nu][sigma]
                   -gamma[r][nu][j]*gamma[j][mu][sigma] for j in range(4)))
    ric=s.Matrix(4,4,lambda mu,nu:sum(R(r,mu,r,nu) for r in range(4)))
    expected=s.zeros(4); expected[0,0]=E.a+E.d
    require(ric==expected,'all continuum Ricci rows computed from the metric')
    for i,j,answer in [(2,2,-E.a),(2,3,-E.b),(3,3,-E.d)]:
        require(sum(g[0,r]*R(r,i,0,j) for r in range(4))==answer,
                'nonflat continuum Riemann components')
    return {'Ric_uu':'a+d','R_uxux':'-a','R_uxuy':'-b','R_uyuy':'-d'}


def main():
    result={'symbolic':symbolic_rows(),'independent':direct_action_controls()}
    radial_controls()
    samples=[]
    for n,L in [(12,2),(16,3)]:
        counts=golden_counts(n,L)
        F0,F1=0,1
        for _ in range(n+1): F0,F1=F1,F0+F1
        require(sum(counts.values())==F0,'exact-cost Fibonacci total')
        require(min(counts.values())>0,'actual positive golden coverage in fixture')
        rho=[s.Rational(L**4*k,F0) for k in counts.values()]
        require(sum(rho)==L**4,'exact normalized actual cell weights')
        require(len(set(rho))>1,'weights genuinely nonuniform')
        samples.append({'n':n,'L':L,'words':F0,'minimum_count':min(counts.values()),
                        'maximum_count':max(counts.values()),'distinct_weights':len(set(rho))})
    result['golden_counts']=samples
    result['weighted_independent']=direct_action_controls(counts)
    result['untransported_weight_control']=direct_action_controls(counts,rescale=False)
    result['radial_inverse']='exact; all extra sources retained'
    result['continuum']=continuum_control()
    result['scope']='full local vacuum coframe/link equations with fixed boundary; native admission and global periodic roots open'
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
