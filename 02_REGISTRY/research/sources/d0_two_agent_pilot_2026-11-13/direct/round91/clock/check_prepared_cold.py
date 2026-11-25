"""Real history writers, honest failures, matched RAW cold return and two H.1 rows."""
import json
import math

import mpmath as mp
import numpy as np


mp.mp.dps = 90
P = (mp.sqrt(5)-1)/2
A = mp.sqrt(P)
Z = mp.mpf(2)**-20
TH = mp.asin(P)
G = np.array([[float(A),-float(P)],[float(P),float(A)]])
X = np.array([[0.,1.],[1.,0.]])
V = G[:,0]


def check(value, message):
    if not value:
        raise ValueError(message)


def mul(a, b):
    return np.einsum("ij,j...->i...",a,b)


def close(a, b, message):
    check(np.allclose(a,b,atol=3e-13,rtol=0),message)


def rot(g):
    return np.array([[math.cos(g),-math.sin(g)],[math.sin(g),math.cos(g)]])


def cx(n,c,t):
    u=np.zeros((1<<n,1<<n))
    for i in range(1<<n):
        u[i^(((i>>c)&1)<<t),i]=1
    return u


def equal_writer():
    states=[]
    passive=V
    for _ in range(6):
        passive=np.kron(passive,V)
    for mark in (0,1):
        flip=X if mark else np.eye(2)
        r=mul(flip,mul(G.T,V))
        t=mul(G,mul(flip,V))
        u=mul(flip,mul(G,mul(flip,mul(G,V))))
        state=r
        for _ in range(5):
            state=np.kron(state,t)
        states.append(np.kron(state,u))
    close(states[0]@states[1],0,"orthogonal physical copies")
    for state in states:
        close(passive@state,float(P**6),"all seven passive factors")
    return float(P**6)


def field_words():
    # Native 3-bit fixture; success and O=1, with a further genuinely varying failed record.
    old=np.kron(np.kron(V,V),V)
    k=3
    good=5  # 101, pattern on three real RAW wires
    n=1
    gamma=2**k*n*float(TH)
    c=math.cos(gamma)
    check(0<c<1,"one physical positive attenuation")
    wp=equal_writer()
    receipts=[]
    for sign in (-1,1):
        g=G if sign>0 else G.T
        w=mul(cx(3,1,0),mul(np.kron(np.eye(2),np.kron(g,np.eye(2))),
              mul(cx(3,0,2),np.kron(np.eye(4),G))))
        v=mul(w,old)
        q=v[good]**2
        check(0<q<1,"both ready and failed tapes present")
        actual={}
        for up in (False,True):
            weights=[]
            for y in range(2**k):
                # Character sum from the actual conditional phase word.
                e=n*sum((-1)**(bin(s&(y^good)).count("1")) for s in range(2**k))
                power=2**k*n-e if up else e
                weights.append(V@mul(rot(power*float(TH)),V))
            expected=np.array(weights)*(wp**k)
            op=mul(w.T,mul(np.diag(expected),w))
            direct=float(old@mul(op,old))
            want=wp**k*((c+(1-c)*q) if up else (1-(1-c)*q))
            close(direct,want,"all cold amplitudes incl true failed Born probabilities")
            public=sum((expected*v*v)**2)
            check(abs(direct*direct-public)>1e-11,"dephasing archive changes cold probability")
            actual["up" if up else "down"]=direct
        receipts.append((q,actual,float(v[1]**2)))
    check(abs(receipts[0][2]-receipts[1][2])>.001,"fine failed law really moves")
    check((receipts[0][1]["up"]-receipts[1][1]["up"])*
          (receipts[0][1]["down"]-receipts[1][1]["down"]) < 0,"opposite true slopes")
    return {"fixture_Q":[round(item[0],12) for item in receipts],
            "field_dependent_other_tape":[round(item[2],12) for item in receipts],
            "native_positive_cos":round(c,12),"coherent_and_measured_cold_differ":True}


def physical_rows():
    lam=-(1099527356400+824647876594*P)/68720525311
    h=mp.mpf(1)/4
    e0=2*(P*mp.sin(448*TH)/h)**2
    rows=[mp.mpf(".64")-2*lam*e0,-mp.mpf(".48")-4*lam*e0]
    g=P**3/65536*5497642024880/2**51
    # Illustrative finite prefix, independent of the exact symbolic statement for any L,alpha.
    alpha=mp.mpf(3)/17
    d=mp.mpf(1)/128
    l=3
    cold=P**(6*l)
    c=mp.cos(8*TH)
    beta=1-c
    q0=alpha/2
    results=[]
    for up in (False,True):
        u0=c+beta*q0 if up else 1-beta*q0
        k=beta if up else -beta
        b=Z*cold*cold
        den=1-Z+b*u0*u0
        gain=-2*b*u0*k/den*(alpha*g/2)
        recovered=[]
        bounds=[]
        for row in rows+[sum(rows)]:
            dq=d*alpha*g*row/2
            shift=k*dq
            dp=1-Z+b*(u0+shift)**2
            dm=1-Z+b*(u0-shift)**2
            js=(-mp.log(dp)+mp.log(dm))/(2*d)
            exact=-(dp-dm)/(2*d)
            check(abs(exact-den*gain*row) < mp.mpf("1e-80"),"exact determinant secant")
            xx=2*b*u0*shift/(den+b*shift**2)
            ratio=(mp.atanh(xx)/xx)*den/(den+b*shift**2)
            bound=b*shift**2/den+xx**2/(3*(1-xx**2))
            check(abs(js/(gain*row)-ratio)<mp.mpf("1e-53"),"raw log determinant identity")
            check(abs(ratio-1)<=bound,"two-sided finite-jet bound")
            recovered.append(mp.nstr(js/gain,12))
            bounds.append(mp.nstr(bound,5))
        results.append({"tag":"increasing cold" if up else "decreasing cold",
                        "J_gain_sign":int(mp.sign(gain)),"recovered_finite_rows":recovered,
                        "relative_J_secant_bounds_example":bounds})
    return results


if __name__=="__main__":
    print(json.dumps({"native_replay":field_words(),
                      "two_H1_rows_and_sum":physical_rows(),
                      "GR_closed":False},indent=2,sort_keys=True))
