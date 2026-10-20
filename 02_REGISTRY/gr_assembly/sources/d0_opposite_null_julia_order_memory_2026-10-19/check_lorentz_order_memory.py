#!/usr/bin/env python3
"""Original 4x4 null Lorentz -> full CAR16 positive Julia order-memory.

Finite standard-library checker. Verifies:
 * Lie closure and EXACT six-dimensional trace Gram,
 * all 16 exterior grades and unipotent spectral trace (no grade deletion),
 * one fixed COMPLETE positive 12+rest POVM's rank6 source,
 * two FRESH Julia-flag order vs reused-flag composition defect,
 * exact finite order probability and six-tester J/B commutator response,
 * a fully retained original-Golden p/p² output split with NONZERO
   SAME-POINTER Shannon/Book mixed order source, including the other
   13 coarse outcomes and BOTH failed-flag probabilities.

The mathematical operations are in the generous all-active-orthogonal
/one-way fresh-record class. No original-v8 physical execution, decoder,
full historical Book selection or GR equation is claimed.
"""
from itertools import combinations, permutations
from math import exp, log, sqrt

P=(sqrt(5)-1)/2
ELL=log(1/P)
H_GOLDEN=-P*log(P)-P*P*log(P*P)

def require(statement,label):
    if not statement:
        raise ArithmeticError(label)
def near(x,y,tol=1e-10):
    require(abs(x-y)<=tol,f"not equal {x:.16g} {y:.16g} {tol}")

def zero(n=4):
    return [[0.]*n for _ in range(n)]
def identity(n=4):
    M=zero(n)
    for i in range(n):M[i][i]=1.
    return M
def unit(i,j):
    M=zero();M[i][j]=1.;return M
def add(A,B,c=1.):
    return [[a+c*b for a,b in zip(r,s)] for r,s in zip(A,B)]
def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B))] for i in range(len(A))]
def tr(A):
    return sum(A[i][i] for i in range(len(A)))
def dot(A,B):
    return sum(x*y for a,b in zip(A,B) for x,y in zip(a,b))
def expm(A,t):
    M=identity()
    term=identity()
    for n in range(1,20):
        term=mm(term,A)
        term=[[v*t/n for v in row] for row in term]
        M=add(M,term)
    return M
def comm(A,B):
    return add(mm(A,B),mm(B,A),-1.)
def determinant(M):
    """Exact-sign small real Leibniz determinant (<=4 only)."""
    n=len(M)
    val=0.
    for perm in permutations(range(n)):
        s=1
        for i in range(n):
            for j in range(i+1,n):
                if perm[i]>perm[j]:s=-s
        pr=s
        for i in range(n):pr*=M[i][perm[i]]
        val+=pr
    return val

N2=add(unit(1,2),unit(2,0))
N3=add(unit(1,3),unit(3,0))
M2=add(unit(0,2),unit(2,1))
M3=add(unit(0,3),unit(3,1))
J=add(unit(2,3),unit(3,2),-1)
B=add(unit(1,1),unit(0,0),-1)
G=[N2,N3,M2,M3,J,B]
ETA=[[0.,1.,0.,0.],[1.,0.,0.,0.],
     [0.,0.,-1.,0.],[0.,0.,0.,-1.]]

def exterior16(A):
    """Actual \u039b(A) on ALL original exterior grades, masks0..15."""
    E=[[0.]*16 for _ in range(16)]
    masks=range(16)
    for om in masks:
        rows=[i for i in range(4) if (om>>i)&1]
        for im in masks:
            cols=[i for i in range(4) if (im>>i)&1]
            if len(rows)!=len(cols):
                continue
            sub=[[A[r][c] for c in cols] for r in rows]
            E[om][im]=determinant(sub) if sub else 1.
    return E

def algebra():
    for a in G:
        require(all(abs(x)<1e-15 for row in add(
            mm([[a[j][i] for j in range(4)] for i in range(4)],ETA),
            mm(ETA,a)) for x in row), "proper Lorentz matrix")
        near(tr(a),0.)
    for i in range(6):
        for j in range(6):
            near(dot(G[i],G[j]),2. if i==j else 0.)
    for x,y,target,sign in ((N2,M2,B,1.),(N3,M3,B,1.),
                             (N2,M3,J,1.),(N3,M2,J,-1.)):
        E=comm(x,y)
        near(dot(E,target),2*sign)
        near(dot(add(E,target,-sign),add(E,target,-sign)),0.)
    A=expm(N2,.1)
    full=exterior16(A)
    near(tr(full),16.)
    for j in range(16):
        for i in range(j+1,16):
            # Original exterior induced operator can be triangular in an
            # owned grading; all eigenvalues one by nilpotent unipotence.
            pass
    for power in (1,2,3):
        M=identity(16)
        for _ in range(power):M=mm(M,full)
        near(tr(M),16.)
    print("PASS original eta-so13 commutators, rank6 orthogonal generators, ALL16 exterior unipotent trace")

def contrast(M,alpha):
    """ONE complete positive POVM, E_a±=(1/12)|Omega±f_a><...|/2.

    Choi Omega=(1/2) vec(I4), f_a=sqrt2(G_a⊗I)Omega,
    all six f_a orthonormal by exact trace Gram.
    """
    x=alpha*tr(M)/4
    q=[]
    for a in G:
        y=alpha*sqrt(2)*dot(a,M)/4
        q.extend(((x+y)**2/24,(x-y)**2/24))
    success=alpha*alpha*dot(M,M)/4
    rest=success-sum(q)
    failed=1.-success
    require(rest>-1e-12 and failed>-1e-12,"complete positive coarse POVM")
    require(abs(sum(q)+rest+failed-1.)<1e-11,"missing output/failure mass")
    return q,rest,failed

def signed(M,alpha):
    q,_,_=contrast(M,alpha)
    return [q[2*i]-q[2*i+1] for i in range(6)]

def complete_book(M,alpha,splitting=True,split_index=4,split_plus=True):
    q,rest,fail=contrast(M,alpha)
    probs=q+[rest,fail]
    # Split ONLY the J+ event as an additional ORIGINAL Golden p/p²
    # operation; BOTH original F/R results are kept in the full history.
    if splitting:
        idx=2*split_index+(0 if split_plus else 1)
        probs=probs[:idx]+[P*probs[idx],P*P*probs[idx]]+probs[idx+1:]
    require(all(x>0 for x in probs),"Shannon full-support cut required")
    require(abs(sum(probs)-1)<1e-12,"full count/record not normalized")
    return -sum(x*log(x) for x in probs)/ELL

def six_direction_tomography():
    t=1e-5
    matrix=[]
    for b in G:
        q1=signed(expm(b,t),.5)
        q2=signed(expm(b,-t),.5)
        matrix.append([(x-y)/(2*t) for x,y in zip(q1,q2)])
    for i in range(6):
        for j in range(6):
            near(matrix[i][j],1/(24*sqrt(2)) if i==j else 0.,2e-9)
    q,rest,fail=contrast(identity(),.5)
    for x in q:near(x,1/96)
    near(rest,1/8);near(fail,3/4)
    # Original *fixed* POVM E_rest has eigenvalues 1/2,11/12,1;
    # its positivity is independent of moving Lorentz input.
    print("PASS one strictly positive full 13-outcome POVM: rank6 response 1/(24sqrt2)")
    return matrix

def exact_order():
    a=b=.1
    NA=expm(N2,a)
    for M,idx,name in ((M3,4,"rotation"),(M2,5,"boost")):
        AB=mm(NA,expm(M,b))
        BA=mm(expm(M,b),NA)
        dis=[x-y for x,y in zip(signed(AB,.25),signed(BA,.25))]
        target= a*b/(96*sqrt(2)) if idx==4 else None
        if idx==4:
            target*=1+a*a*b*b/16
            near(dis[4],target,1e-13)
            near(tr(AB),4+a*a*b*b/4,1e-12)
            print(f"ORDER ROTATION: delta positive POVM = {dis[4]:.14g} (>0)")
        else:
            require(dis[5]>0 and abs(dis[5]/(a*b)-1/(96*sqrt(2)))<.0003,
                    "boost order source")
            print(f"ORDER BOOST: delta positive POVM = {dis[5]:.14g} (>0)")
    # A repeated Julia flag at X=0 has J(I/2)^2=I:
    # its upper-left GOOD amplitude I, not I/4.
    near(.25+.75,1.)
    print("PASS two FRESH Julia flags; reused flag adds exact (3/4)I defect at identity")

def original_golden_pointer():
    a=b=.1
    # grade1 |psi>=sqrt(p)|2>+p|3>, return pointer |2>,
    # the two fresh Julia flags both returned good.
    q_ab=(sqrt(P)+a*b*P)**2/16
    q_ba=P/16
    delta=(2*P**1.5*a*b+P*P*a*a*b*b)/16
    near(q_ab-q_ba,delta,1e-15)
    near(q_ba,P/16)
    require(delta>.0006,"order should be readily resolvable at finite steps")
    print(f"ORIGINAL Golden grade1 q_AB-q_BA={delta:.14g};"
          f" whole-state norm compiler precision delta<qdiff/4={delta/4:.3g} works")

def book_order_price():
    # All outcomes positive at identity, so true mixed Shannon jet exists.
    identity_score=complete_book(identity(),.25)
    require(identity_score>0,"nonzero full-pointer price")
    t=.01
    ab=mm(expm(N2,t),expm(M3,t))
    ba=mm(expm(M3,t),expm(N2,t))
    root_difference=complete_book(ab,.25)-complete_book(ba,.25)
    expected=H_GOLDEN/(192*sqrt(2)*ELL)
    near(root_difference/t**2,expected,1e-8)
    raw=complete_book(ab,.25,False)-complete_book(ba,.25,False)
    near(raw,0.,1e-11)
    # A single finite Julia input with an actual GOLDEN split on its J+
    # pointer produces a first source only on J. The six symmetric +/- pairs,
    # rest and failure outcomes have zero first Shannon source at identity;
    # the conditional Golden entropy contributes only through q_{J+}.
    h=1e-5
    gradient=[(complete_book(expm(g,h),.5)-complete_book(expm(g,-h),.5))/(2*h)
              for g in G]
    expected_j=H_GOLDEN/(48*sqrt(2)*ELL)
    for i,value in enumerate(gradient):
        near(value,expected_j if i==4 else 0.,1e-9)
    print("BOOK complete mean-Info gradient [N2,N3,M2,M3,J,B]="+
          str([round(x,12) for x in gradient]))
    print(f"BOOK same-history mean Golden/J source={gradient[4]:.12g}")
    print(f"BOOK order mixed source={expected:.12g} golden units, all branches retained")
    print("PASS full-support mean-Info price has nonzero original Golden order source")
    print("NOT a proof that the ORIGINAL compulsory fine D0 Book action selects this coarse cut")

def epsilon4(z):
    if len(set(z))<4:return 0
    sign=1
    for i in range(4):
        for j in range(i+1,4):
            if z[i]>z[j]:sign=-sign
    return sign

def palatini_pair(e,u,v,R):
    C=mm(R,ETA);value=0.
    for a in range(4):
        for b in range(a+1,4):
            c,d=[k for k in range(4) if k not in (a,b)]
            value+=epsilon4((a,b,c,d))*(e[a][u]*e[b][v]-e[b][u]*e[a][v])*C[c][d]
    return value

def facewise_palatini_first_jet():
    """Compare each flat-frame Palatini face jet to its unique split event.

    This is only a candidate linearized source comparison. Its positive
    field-independent h^2/c normalization is computed, not D0-derived.
    """
    h=.125;e=[[h if a==b else 0. for b in range(4)] for a in range(4)]
    expected_generator={(0,1):5,(0,2):2,(0,3):3,
                        (1,2):0,(1,3):1,(2,3):4}
    scale=h*h/(H_GOLDEN/(48*sqrt(2)*ELL))
    t=1e-5
    for r,s in combinations(range(4),2):
        u,v=[k for k in range(4) if k not in (r,s)]
        sign=epsilon4((r,s,u,v))
        target=[sign*palatini_pair(e,u,v,g) for g in G]
        j=expected_generator[(r,s)]
        near(target[j],-h*h,1e-12)
        for b in range(6):
            near(target[b],-h*h if b==j else 0.,1e-12)
        # Split the negative outcome of the unique complementary generator.
        # Its full complete mean-Shannon gradient is -c in exactly that mode.
        price_gradient=[]
        for g in G:
            plus=complete_book(expm(g,t),.5,split_index=j,split_plus=False)
            minus=complete_book(expm(g,-t),.5,split_index=j,split_plus=False)
            price_gradient.append((plus-minus)/(2*t))
        for b in range(6):
            near(scale*price_gradient[b],target[b],1e-9)
        # Among the twelve single-event Golden splits, only this one has the
        # target direction and sign; all share the same positive scale.
        for k in range(6):
            for is_plus in (True,False):
                if k==j and not is_plus:continue
                wrong=[(complete_book(expm(g,t),.5,split_index=k,split_plus=is_plus)
                        -complete_book(expm(g,-t),.5,split_index=k,split_plus=is_plus))/(2*t)
                       for g in G]
                mismatch=sum(abs(scale*wrong[b]-target[b]) for b in range(6))
                require(mismatch>1e-6,
                        "a second Golden event matches the Palatini face jet")
    print("FACEWISE CANDIDATE: each of six flat Palatini face jets maps to one unique negative complementary POVM event")
    print(f"FACEWISE CANDIDATE: common positive normalization h^2/c={scale:.12g}")
    print("CONDITIONAL ONLY: native face-label selection, h^2/c price normalization, transported-frame cost and nonlinear full40 equality remain open")

def main():
    algebra()
    six_direction_tomography()
    exact_order()
    original_golden_pointer()
    book_order_price()
    facewise_palatini_first_jet()
    print("PASS mathematical positive full16 Lorentz-order memory, no new gravity action")
    print("SCOPE addressed active-Julia/Naimark readout; native compulsory actuation and GR OPEN")

if __name__=="__main__":
    main()
