"""A common Book clock with an occupied CAR input and a paid native supplier."""
import json
from math import factorial
import numpy as np
from mpmath import iv

iv.dps = 80
p = (iv.sqrt(5)-1)/2
a = iv.sqrt(p)
theta = iv.atan2(p,a)
t = 1160*theta - 2*123*iv.pi
z = iv.mpf(1)/2**20
beta = 2*p*p
x = beta/11
pad = 16
heat = (132/(359*beta))*2*x**pad/(factorial(pad)*(1-x/(pad+1)))


def need(ok, why):
    if not ok:
        raise ArithmeticError(why)


def bounds(value, lo, hi):
    need(value.a > iv.mpf(lo) and value.b < iv.mpf(hi), (value, lo, hi))
    return [lo,hi]


def mat(*factors):
    out = factors[0]
    for factor in factors[1:]:
        out = np.einsum("ij,j...->i...",out,factor)
    return out


def native_waves():
    """Real matrices in the original integer CAR basis; temporal bit has mask 1."""
    theta_f = float(theta.mid); p_f = float(p.mid); a_f = float(a.mid)
    def temporal(n):
        co, si = np.cos(n*theta_f), np.sin(n*theta_f)
        return np.kron(np.eye(8), [[co,-si],[si,co]])
    def cx(c, t):
        return np.eye(16)[:,[i ^ (t if (i & c) else 0) for i in range(16)]]
    x1 = np.eye(16)[:,[i^1 for i in range(16)]]
    prep = mat(x1,cx(1,8),cx(1,4),cx(1,2),temporal(1))
    base = np.eye(16)[:,0]
    want = np.zeros(16); want[1]=a_f; want[14]=p_f
    need(np.max(abs(mat(prep,base)-want))<2e-13, "native CAR blank")
    g = np.array([[a_f,-p_f],[p_f,a_f]])
    raw = np.kron(np.kron(np.kron([a_f,p_f],[a_f,p_f]),[a_f,p_f]),[a_f,p_f])
    clear = np.kron(np.kron(np.kron(g.T,g.T),g.T),g.T)
    need(np.max(abs(mat(clear,raw)-base))<2e-14,"clear four native births")
    probe = np.array([a_f,p_f])
    def rot(n):
        co,si=np.cos(n*theta_f),np.sin(n*theta_f)
        return np.array([[co,-si],[si,co]])
    cx_parity = np.eye(32)
    for mask in (1,2,4,8):
        perm = [i ^ int(bool((i//2)&mask)) for i in range(32)]
        cx_parity = mat(np.eye(32)[:,perm],cx_parity)
    result = {}
    for j in (283,1759):
        V = mat(cx(2,1),temporal(-j),cx(2,1),temporal(j),prep,clear)
        state = mat(V,raw)
        want = np.zeros(16); want[1]=a_f
        want[14]=p_f*np.cos(2*j*theta_f); want[15]=p_f*np.sin(2*j*theta_f)
        need(np.max(abs(state-want))<1e-12, "true native wave")
        q = p**2*iv.sin(2*j*theta)**2
        for sign in (1,-1):
            mid = np.kron(np.eye(16),mat(rot(sign*1160),rot(67)))
            core = mat(cx_parity,mid,cx_parity,np.kron(np.eye(16),rot(1)))
            baseline = np.kron(raw,probe)
            process = mat(np.kron(V.T,np.eye(2)),core,np.kron(V,np.eye(2)))
            cold = np.dot(baseline,mat(process,baseline))
            exact = q*iv.cos(68*theta+sign*t)+(1-q)*iv.cos(-66*theta-sign*t)
            need(abs(cold-float(exact.mid))<1e-12,"full inverse on retained wave")
        result[j]=q
    return result


def cold(q, odd, sign):
    return q*iv.cos(68*theta+sign*t)+(1-q)*iv.cos(odd-sign*t)


def secant(q, odd):
    def field_J(sign):
        c = cold(q,odd,sign)
        return -8*iv.log1p(z*(p**2+p**3*c*c-1))
    # Common rank-16 terminal constant cancels. Both true heat traces included.
    return (field_J(1)-field_J(-1)+iv.mpf([-1,1])*heat)/(2*t)


def address_tariff(q):
    # Last CX of the second parity chain has the probe as physical target.
    def occupancy(sign):
        return (q*iv.sin(69*theta+sign*t)**2
                +(1-q)*iv.sin(-65*theta-sign*t)**2)
    return p**2*(occupancy(1)-occupancy(-1))/(2*t)


def report(qpair, tuned_k, boxes):
    values = []
    for k in (1,tuned_k):
        rows=[secant(q,(2*k-68)*theta) for q in qpair]
        need(rows[0].b<0<rows[1].a,"wrong physical sign")
        # Two-component optimal symmetric calibration for target (-c,c).
        rel=abs((rows[1]+rows[0])/(rows[1]-rows[0]))
        values.append({"k":k,"j":68-k,"rows":[bounds(r,*b) for r,b in zip(rows,boxes[k])],
                       "relative_common_calibration_error":bounds(rel,*boxes[(k,"error")])})
    for angle,sign in (("0.007",1),("0.012",-1)):
        total=sum(secant(q,iv.mpf(angle)) for q in qpair)
        need((sign*total).a>0,"no bracket of shared-gain calibration")
    return values


if __name__=="__main__":
    waves=native_waves()
    need(heat.b<iv.mpf("1e-31"),"short returns near end")
    # Both NC1 head outcomes retain the tail; squared passive masses are p²,p³.
    gl = iv.matrix([[a,-p],[p,a]]); v=iv.matrix([a,p])
    for bit,tail,sq in ((0,gl*v,p**2),(1,iv.matrix([1,0]),p**3)):
        marker=v[bit]*(a*tail[0]+p*tail[1])
        need(abs(marker**2-sq)<1e-72,"honest marked root compression")
    ideal=[iv.mpf(1)/256,iv.mpf(4)/256]
    actual=[waves[283],waves[1759]]
    ibox={1:[("-2.395e-8","-2.394e-8"),("1.713e-8","1.714e-8")],
          (1,"error"):(".165",".167"),
          30538:[("-2.055e-8","-2.054e-8"),("2.045e-8","2.046e-8")],
          (30538,"error"):(".00219",".00221")}
    abox={1:[("-2.420e-8","-2.418e-8"),("1.637e-8","1.638e-8")],
          (1,"error"):(".192",".194"),
          -23345:[("-2.016e-8","-2.015e-8"),("2.031e-8","2.032e-8")],
          (-23345,"error"):(".00389",".00392")}
    tariffs=[address_tariff(q) for q in actual]
    for q,fee in zip(actual,tariffs):
        need((secant(q,-66*theta)+iv.mpf("1e-7")*fee).b<0,"tariff did not erase sign split")
    print(json.dumps({"actual_paid_readout_occupancy_rows":[bounds(s,"-.374","-.370") for s in tariffs],
        "second_native_row_break_even_tariff":bounds(-secant(actual[1],-66*theta)/tariffs[1],
                                                    "4.39e-8","4.42e-8"),
        "true_native_CAR_q":[bounds(q,*b) for q,b in zip(actual,
        [(".00383738",".00383740"),(".01540553",".01540555")])],
        "angle":bounds(t,".00594890822",".00594890824"),
        "heat_difference_upper":"1e-31","both_hodge_degrees":True,
        "root_rank":8,"full_joint_leaf_rank":16,"factory_refusal_included":True,
        "ideal_profile_rows":report(ideal,30538,ibox),
        "paid_native_rows":report(actual,-23345,abox),
        "actual_Book_price_identified":False,"GR_closed":False},indent=2,sort_keys=True))
