"""Two-cut calibration on the noisy H.1 reader. Python standard library."""
import json
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as F
from math import asin, cos, log, sin, sqrt


@dataclass(frozen=True)
class Golden:
    """a + b p, with p² = 1-p."""
    a: F = F(0)
    b: F = F(0)

    def __add__(self, other):
        return Golden(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return Golden(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        cross = self.b * other.b
        return Golden(self.a * other.a + cross,
                      self.a * other.b + self.b * other.a - cross)

    def __pow__(self, n):
        result = Golden(1)
        for _ in range(n):
            result = result * self
        return result

    def decimal(self):
        sizes = [len(str(abs(F(x).numerator))) + len(str(F(x).denominator))
                 for x in (self.a, self.b)]
        with localcontext() as ctx:
            ctx.prec = max(sizes) + 60
            p = (Decimal(5).sqrt() - 1) / 2

            def dec(x):
                x = F(x)
                return Decimal(x.numerator) / Decimal(x.denominator)
            return format(dec(self.a) + p * dec(self.b), '.17f')


def check(ok, name):
    if not ok:
        raise AssertionError(name)


def fixture():
    p = Golden(0, 1)
    one, two, three, four = (Golden(i) for i in (1, 2, 3, 4))
    check(p*p+p == one, "golden normalization")
    c = one - two * p**2
    for _ in range(9):
        c = two * c*c - one
    visibility = (one-c)*Golden(F(1, 2))
    field_scale = visibility * p**7
    # Prepare sin^2(3 theta) via G² v, where v=G|0>. Other wires keep v.
    report0, report2 = p**2, (three*p-four*p**3)**2
    ready = p**2
    base = [ready * report0]*7
    altered = list(base)
    altered[0] = altered[2] = ready * report2

    def event(slots):
        y_plus, y_minus, f, ref, x_plus, x_minus, q = slots
        xi = (y_plus-y_minus)*(f-ref)+(x_plus-x_minus)*(q-ref)
        return field_scale*(four+xi)

    qa, qb = event(base), event(altered)
    check(qb-qa == field_scale*(ready*(report2-report0))**2,
          "full seven-address SC7 including failures")
    check(qb != qa, "different preparations")
    # CX of e and a canonical pointer. NC1 is diagonal in pointer.
    for event_probability in (qa, qb):
        bit = (one-event_probability)*p**2 + event_probability*p
        check(bit == p**2+p**3*event_probability, "pointer and valid NC1 parser")
    return {
        "scalar_SC5_witness": "L=2, exponents 0 vs 2 only on REPORT y+ and f; real pays for forwards and inverses",
        "scope": "scalar detector fixture, not a constructed second geometric H.1 field",
        "Q_A": qa.decimal(), "Q_B": qb.decimal(),
        "q_A": (p**2+p**3*qa).decimal(), "q_B": (p**2+p**3*qb).decimal(),
        "mark_gap": (p**3*(qb-qa)).decimal()
    }


def calibration():
    a, b = F(41,100), F(47,100)
    za, zb = F(13,10), F(21,10)
    midpoint = (za*a+zb*b)/(za+zb)
    check(2*(midpoint-(a+b)/2) == (a-b)*(za-zb)/(za+zb), "midpoint identity")
    deltas = [F(-1,2000), F(1,3200), F(-1,4000)]
    a_hat,b_hat,mid_hat = (x+d for x,d in zip((a,b,midpoint),deltas))
    ea,eb,em = map(abs,deltas)
    lower = abs(a_hat-b_hat)-ea-eb
    bound = (abs(2*mid_hat-a_hat-b_hat)+2*em+ea+eb)/lower
    check(lower>0 and abs((za-zb)/(za+zb)) <= bound<1, "errors of all three reads")
    c0,c1 = F(7,4), F(11,8)

    def mixture(x,y):
        return (x*a+y*b)/(x+y)
    rab,rba = mixture(c0*za,c1*zb),mixture(c1*za,c0*zb)
    odds = lambda r: (r-b)/(a-r)
    check(odds(rab)*odds(rba)==(za/zb)**2, "unknown selector cancels")
    check(odds(rab)/odds(rba)==(c0/c1)**2, "body cancels from selector calibration")
    for prior in [F(1,10),F(1,2),F(2,3)]:
        r=prior*a+(1-prior)*b
        s=prior*b+(1-prior)*a
        check(odds(r)*odds(s)==1, "swapped Born decisions")
    # Affine Z, nonlinear W1. Reproduces Born at both ends and in the middle.
    masses = lambda q: ((1+q)*(1-q), (1+q)*q)
    r=(a+b)/2
    for q in (a,b,r):
        m0,m1=masses(q)
        check(m1/(m0+m1)==q, "unrestricted weights mimic full mixture")
    check(masses(r)[1] != (masses(a)[1]+masses(b)[1])/2, "real condition lost")
    return {"relative_mass_contrast":str(abs((za-zb)/(za+zb))),
            "three_read_error_bound":str(bound),
            "recovered_mass_ratio_squared":str(odds(rab)*odds(rba)),
            "counterexample_affine_total_nonlinear_mark":True}


def cq():
    # Two full-rank mixed states on a Bell-pair subspace, in rotated eigenbases.
    # Noncommuting positive states with a common support.
    t = [F(3,5), F(2,5)]
    s = [F(5,7), F(2,7)]
    overlap = [[F(9,25),F(16,25)],[F(16,25),F(9,25)]]
    q, r = F(41,100), F(47,100)
    px, py = (1-q,q), (1-r,r)
    def rel(la,mu,transition):
        return sum(float(x*transition[i][j])*(log(x)-log(y))
                   for i,x in enumerate(la) for j,y in enumerate(mu) if transition[i][j])
    a=[x*y for x in px for y in t]
    b=[x*y for x in py for y in s]
    orthogonal = [[overlap[i%2][j%2] if i//2==j//2 else 0
                   for j in range(4)] for i in range(4)]
    before, after = rel(t,s,overlap),rel(a,b,orthogonal)
    d_bern = rel(px,py,[[1,0],[0,1]])
    check(abs(after-before-d_bern)<2e-15, "full mixed-state entropy difference")
    def root_fidelity2(la,mu):
        trace=sum(la[i]*mu[j]*overlap[i][j] for i in range(2) for j in range(2))
        return sqrt(float(trace)+2*sqrt(float(la[0]*la[1]*mu[0]*mu[1])))
    f_in=root_fidelity2(t,s)
    f_out=sum(root_fidelity2(a[k:k+2],b[k:k+2]) for k in (0,2))
    check(abs(f_out-f_in*sum(sqrt(float(x*y)) for x,y in zip(px,py)))<2e-15,
          "root fidelity including both quantum blocks")
    for post in [[[F(1),F(0)],[F(0),F(1)]],
                 [[F(1,3),F(2,3)],[F(7,8),F(1,8)]]]:
        fisher=sum((z-y)**2/((1-q)*y+q*z) for y,z in zip(*post))
        check(fisher<=1/(q*(1-q)), "marked tester Fisher contraction")
    check(sum(abs(x-y) for x,y in zip(px,py))==2*abs(q-r),
          "complete flagged-channel diamond norm witness")
    return {"quantum_input_example":"two noncommuting mixed states on a Bell subspace",
            "relative_entropy_identity":True,"root_fidelity_product":True,
            "flagged_trace_norm_exact":str(2*abs(q-r)), "fisher_contraction":True}


def binary_entropy(x):
    return -sum(t * log(t) for t in (x,1-x) if t>0)


def dot(x,y):
    return sum(a*b for a,b in zip(x,y))


def complete(columns):
    """Complete an orthonormal real frame, retaining its input columns."""
    n = len(columns[0])
    basis = list(columns)
    for j in range(n):
        v = [float(k==j) for k in range(n)]
        for u in basis:
            c = dot(u,v)
            v = [x-c*y for x,y in zip(v,u)]
        length = sqrt(dot(v,v))
        if length>1e-10:
            basis.append([x/length for x in v])
    check(len(basis)==n, "complete supported frames")
    return basis


def active_reader():
    g = Golden(0,1)
    one = Golden(1)
    check(one-Golden(4)*g**3==g**6,"golden binary posterior span")
    p=(sqrt(5)-1)/2
    a=sqrt(p)
    theta=asin(p)
    l=p*p
    tail0,tail1=(p**3,2*a*p),(1,0)
    # U = G² Z: reflection that exchanges Gv and |0> exactly.
    reflect=lambda x:(tail0[0]*x[0]+tail0[1]*x[1],
                      tail0[1]*x[0]-tail0[0]*x[1])
    check(max(abs(x-y) for x,y in zip(reflect(tail0),tail1))<2e-15,"native tail swap")
    check(reflect(tail1)==tail0,"native tail swap on zero")
    # Helstrom matrix for B=0 minus B=1 at P(B=1|e=0)=l.
    h00=(1-l)*tail0[0]**2-l
    h01=(1-l)*tail0[0]*tail0[1]
    h11=(1-l)*tail0[1]**2
    R=sqrt(1-4*p**3*tail0[0]**2)
    hp=(1-2*l+R)/2
    vec=(h01,hp-h00)
    n=sqrt(dot(vec,vec))
    pos=tuple(x/n for x in vec)
    opt=(pos,(-pos[1],pos[0]))

    def outcomes(prior,basis):
        out=[]
        for v in basis:
            t0=(1-prior)*dot(v,tail0)**2
            t1=prior*dot(v,tail1)**2
            if t0+t1>1e-25:
                out.append((t0+t1,t1/(t0+t1)))
        return out

    def residual(info):
        return sum(w*binary_entropy(t) for w,t in info)

    optimum_error=(1-R)/2
    for e,prior in enumerate((l,1-l)):
        basis=opt if e==0 else tuple(reflect(v) for v in opt)
        post=outcomes(prior,basis)
        check(max(abs(min(t,1-t)-optimum_error) for _,t in post)<3e-15,
              "both posterior error probabilities at Helstrom optimum")
        check(abs(residual(post)-binary_entropy(optimum_error))<4e-15,
              "exact optimal tail entropy on each event")

    golden_bases=[]
    for k in (0,2,4,10):
        c,sin_k = cos(k*theta), sin(k*theta)
        base=((c,sin_k),(-sin_k,c))
        diff=residual(outcomes(l,base))-residual(outcomes(1-l,tuple(reflect(v) for v in base)))
        check(abs(diff)<3e-15,"finite decoder exact conditional entropy symmetry")
        golden_bases.append(k)

    # Nontrivial protected input surface: event branches rotate this example's Spin columns.
    Q=(3/5)**2
    V=[[4/5,0,0,3/5],[0,4/5,-3/5,0]]
    K=[]
    for b in (0,1):
        amplitudes=(a,p) if b==0 else (p,a)
        K.append([[amplitudes[i//2]*v for i,v in enumerate(col)] for col in V])
    for i in (0,1):
        for j in (0,1):
            check(abs(dot(K[0][i],K[1][j])-a*p*(i==j))<2e-15,
                  "operator crossing on all protected input columns")
    for e in (0,1):
        for b in (0,1):
            selected=[[v if i//2==e else 0 for i,v in enumerate(col)] for col in K[b]]
            pb=dot(K[b][0],K[b][0]); peb=dot(selected[0],selected[0])
            src=complete([[v/sqrt(peb) for v in col] for col in selected])
            dst=complete([[v/sqrt(pb) for v in col] for col in K[b]])
            for col,target in zip(selected,K[b]):
                actual=[sum(v[i]*dot(u,col) for u,v in zip(src,dst)) for i in range(4)]
                check(max(abs(y-sqrt(peb/pb)*x) for y,x in zip(actual,target))<3e-15,
                      "one single correction on all input columns restores reference")
    # Tensor products of joint probability tables for independent full messages.
    from itertools import product
    qs=[.40,.42,.47]
    kernels=[]
    for qj in qs:
        Qj=(qj-l)/(p**3)
        kernels.append({(e,b):(Qj if e else 1-Qj)*(l if e!=b else 1-l)
                        for e,b in product((0,1),repeat=2)})
    from math import prod
    probs={z:prod(k[pair] for k,pair in zip(kernels,z))
           for z in product(*(table.keys() for table in kernels))}
    info=0.
    for z,mass in probs.items():
        e,b=zip(*z)
        pe=prod(sum(k[(e_i,b0)] for b0 in (0,1)) for e_i,k in zip(e,kernels))
        pb=prod(qj if bj else 1-qj for bj,qj in zip(b,qs))
        info+=mass*log(mass/(pe*pb))
    check(abs(info-sum(binary_entropy(qj)-binary_entropy(l) for qj in qs))<2e-15,
          "three complete independent reports attain the sum")
    q0=.41246988056855516
    # Round displayed irrational diagnostics to avoid platform-level libm noise.
    return {"checks":"native reflection, Helstrom posterior for both events, finite mirrored readers, correction on all columns, three independent reports",
            "mark_error_without_tail":round(l,12),"mark_error_with_tail":round(optimum_error,12),
            "active_information_no_tail_nats":round(binary_entropy(q0)-binary_entropy(l),12),
            "active_information_with_tail_nats":round(binary_entropy(q0)-binary_entropy(optimum_error),12),
            "finite_golden_measurement_exponents":golden_bases,
            "price_derivative_per_q_for_both":round(1+log(q0/(1-q0))/(-log(p)),12)}


if __name__=="__main__":
    print(json.dumps({"status":"PASS","native_reader":fixture(),"affine_prices":calibration(),
                      "LC4":cq(),"single_read_accessible_information":active_reader(),
                      "physical_price_affinity_established":False},
                     indent=2,sort_keys=True))
