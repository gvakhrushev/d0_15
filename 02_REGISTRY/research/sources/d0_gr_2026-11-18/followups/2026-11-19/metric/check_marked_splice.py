"""Conditional CQ source at a common marked SITE; native mark and operator inequalities."""
import json
import mpmath as mp
import sympy as sp

from check_golden_work_gauge import load_owner

mp.mp.dps = 65
p = (mp.sqrt(5)-1)/2
ell = -mp.log(p)
z = mp.mpf(2)**-20
l,u = mp.mpf("1.8436921336215986e-6"),mp.mpf("1.8587082004008725e-6")
I = mp.eye(2)


def report(x,y):
    E=p*p*(1+x)
    L=4*E*(1-E)
    v=p+p*p*y
    b=4*v*v*(1-v*v)
    a=L+(1-L)*b
    return z*(a+b)-z*z*a*b


def tr(A):
    return sum(A[k,k] for k in range(A.rows))


def spectral(A, fn):
    eig,U=mp.eigsy(A)
    return U*mp.diag([fn(x) for x in eig])*U.T


def entropy(A):
    return -tr(A*spectral(A,mp.log))


def h(q):
    return -q*mp.log(q)-(1-q)*mp.log(1-q)


def K(F,rho):
    root=spectral(rho,mp.sqrt)
    T=root*F*root
    return 28*tr(T)-(entropy(T)+entropy(rho-T)-entropy(rho))/ell


def check_native():
    n,_=load_owner()
    C=n.Gate("CX",(2,3))
    G=n.Gate("G",(3,))
    ex=n.Execution(4,(),(),(C,G,C),profile=n.G_CX_SOURCE_I,source_port=2,source_spin=(0,1))
    Cmat=n.gate_matrix(ex,C)
    Gmat=n.gate_matrix(ex,G)
    v=sp.Matrix([n.A,n.P])
    J=sp.kronecker_product(sp.eye(8),v)
    native=0
    for y1 in (0,1):
        P1=sp.kronecker_product(sp.eye(8),sp.diag(1-y1,y1))
        for y2 in (0,1):
            P2=sp.kronecker_product(sp.eye(8),sp.diag(1-y2,y2))
            Kb=P2*Cmat*Gmat*P1*Cmat*J
            diag=[]
            for x in (0,1):
                first=n.P if y1==x else n.P**2
                second=n.P if y2==(x^y1) else n.P**2
                diag.append(first*second)
            assert n.exact_matrix_equal(Kb.T*Kb,sp.kronecker_product(sp.eye(4),sp.diag(*diag)))
            native+=1
    # Recording at the dark echo's intermediate port changes its actual final mark.
    g=sp.Matrix(n.G_LOCAL);zz=sp.diag(1,-1)
    invg=zz*g*zz;e0,e1=sp.eye(2)[:,0],sp.eye(2)[:,1]
    assert n.exact_matrix_equal(invg*g,sp.eye(2))
    prob=sum(((e1.T*invg*(e*e.T)*g*e0)[0])**2 for e in (e0,e1))
    assert n.exact_matrix_equal(sp.Matrix([prob]),sp.Matrix([2*n.P**3]))
    return native


def main():
    r0=report(0,0)
    d0=28-mp.log((1-r0)/r0)/ell
    low=28-mp.log((1-l)/l)/ell;high=28-mp.log((1-u)/u)/ell
    rho=mp.matrix([[mp.mpf(7)/12,mp.mpf(1)/5],[mp.mpf(1)/5,mp.mpf(5)/12]])
    A=mp.matrix([[1,2],[2,-1]])
    F=l*I+(u-l)*mp.mpf(".36")*I+(u-l)*A/20
    B=mp.matrix([[1,-2],[-2,4]])/5
    D=(u-l)*B/8
    assert mp.norm(F*rho-rho*F)>0 and mp.norm(D*F-F*D)>0
    eq=tr(rho*D)
    diff=K(F+D,rho)-K(F,rho)
    assert low*eq<diff<high*eq
    root=spectral(rho,mp.sqrt)
    T=root*F*root
    gradient=28*I-(spectral(rho-T,mp.log)-spectral(T,mp.log))/ell
    ge,_=mp.eigsy(gradient)
    assert low<ge[0]<ge[1]<high
    F0=r0*I
    gap=K(F,rho)-K(F0,rho)-d0*tr(rho*(F-F0))
    eig,_=mp.eigsy(F-F0)
    delta=max(map(abs,eig))
    assert 0<gap<delta**2/(2*ell*l*(1-u))
    # Literal two consecutive marks on one side-WORK register. Their kernels need
    # not commute. A common SITE is a control. All four physical leaves remain.
    hs=mp.mpf(1)/4096
    qs=[report(hs/5,0),report(-hs/7,0)]
    mu=[mp.mpf(3)/7,mp.mpf(4)/7]
    joint=[]
    for a in (0,1):
        for b in (0,1):
            m=[mu[x]*(p if a==x else p*p)*(p if b==(x^a) else p*p) for x in (0,1)]
            pi=sum(m)
            joint.append((pi,sum(m[x]*qs[x] for x in (0,1))/pi))
    q=sum(s*t for s,t in zip(mu,qs))
    assert abs(sum(w for w,r in joint)-1)<mp.mpf("1e-60")
    assert abs(sum(w*r for w,r in joint)-q)<mp.mpf("1e-60")
    h_cond=sum(w*h(r) for w,r in joint)
    assert sum(s*h(t) for s,t in zip(mu,qs))<h_cond<h(q)
    mark_diff=28*(q-r0)-(h_cond-h(r0))/ell
    delta=max(abs(x-r0) for x in qs)
    assert 0<mark_diff-d0*(q-r0)<delta**2/(2*ell*l*(1-u))
    print(json.dumps({"status":"PASS","native_side_mark_leaves_all_spin_columns":check_native(),
        "true_CX_noncommuting_prefix_counter_wrong_probability":mp.nstr(2*p**3,15),
        "uniform_cost_gradient_range":[mp.nstr(low,15),mp.nstr(high,15)],
        "noncommuting_positive_effect_secant_per_probability":mp.nstr(diff/eq,16),
        "conditional_side_record_mutual_information_nats":mp.nstr(h(q)-h_cond,14),
        "field_tangent_remainder_bound_dimension_independent":True,
        "full_book_cost_and_GR_closed":False},indent=2,sort_keys=True))


if __name__=="__main__":
    main()
