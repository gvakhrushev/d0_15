"""Actual two-control A80 word, joint conditioning, and literal stages on fixed inputs."""
from collections import Counter
from functools import lru_cache
from itertools import permutations
from pathlib import Path
from fractions import Fraction as F
from math import sqrt, isqrt
import sys

sys.dont_write_bytecode=True
base=Path(__file__).resolve()
sys.path.insert(0,str(base.parents[2]/'round80'/'price'))
sys.path.insert(0,str(base.parents[2]/'round79'/'heat'))
sys.path.insert(0,str(base.parents[4]/'d0_native_readiness_amplification_2026-10-24'))
from check_parity_price import Golden, a, p, p3, one, ne, action, v
from check_phase_work import plus, interval, times, minus
from native_phase import phase_word, native_rotation_intervals

Y,T,PTR_P,PTR_Q=3,4,5,6


def rational(q):
    return F(int(q.p),int(q.q))


A_INTERVAL=tuple(rational(q) for q in native_rotation_intervals(1,bits=360)[0])
SCALE=10**85


def enclosure(x):
    acc=interval(0)
    for coeff in reversed(Golden.cast(x).coefficients):
        acc=plus(times(acc,A_INTERVAL),coeff)
    return acc


def trace_distance(h):
    if h==one or h==-one:
        return interval(0)
    lo,hi=minus(1,enclosure(h*h))
    assert hi>=0
    def floor_root(t):
        return isqrt(max(0,t.numerator)*SCALE*SCALE//t.denominator)
    return F(floor_root(lo),SCALE),F(floor_root(hi)+1,SCALE)


def sqrtiv(x):
    lo,hi=interval(x)
    assert lo>=0
    def lower(t):
        return isqrt(t.numerator*SCALE*SCALE//t.denominator)
    return F(lower(lo),SCALE),F(lower(hi)+1,SCALE)


def divide(x,y):
    lo,hi=interval(y)
    assert lo>0
    return times(x,(1/hi,1/lo))


def lcd(q):
    if q==(F(0),F(0)) or q==(F(1),F(1)):
        return interval(1)
    def branch(t):
        if t[1]<F(1,4):
            return interval(2)
        assert t[0]>F(1,4)
        return plus(sqrtiv(t),sqrtiv(times(3,minus(1,t))))
    return plus(times(q,branch(q)),times(minus(1,q),branch(minus(1,q))))


@lru_cache(None)
def word(k):
    G=ne.Gate
    width=7
    layout=ne.Execution(width,(PTR_P,PTR_Q),(),(),ne.G_CX_SOURCE_I,2,(0,1))
    def inverse(gs):
        tiny=ne.Execution(width,layout.blank_wires,(),gs,ne.G_CX_SOURCE_I,2,(0,1))
        return ne.inverse_word(tiny,max_qubits=width,max_expanded_stages=11*len(gs))
    def rotation(q):
        return (G('G',(q,)),)
    def conditional(q, flip):
        out=[]
        for mask in range(4):
            route=tuple(G('CX',(ctl,q)) for i,ctl in enumerate((Y,T)) if mask & (1<<i))
            negative=(len(route)%2==1) != flip
            rot=rotation(q)*k
            out.extend(route+(inverse(rot) if negative else rot)+route[::-1])
        return tuple(out)
    prep=inverse(rotation(PTR_P))+inverse(rotation(PTR_Q))
    first=conditional(PTR_P,False)
    assert first==phase_word(layout,(Y,T),(1,1),PTR_P,k,max_qubits=width,max_expanded_stages=10000)
    second=rotation(PTR_Q)*(4*k)+conditional(PTR_Q,True)
    gates=prep+first+second
    # The actual fresh inputs are Golden births: blank is achieved by prep.
    ex=ne.Execution(width,(),(),gates,ne.G_CX_SOURCE_I,2,(0,1),report_bits=(PTR_P,PTR_Q))
    ne.execution_from_json(ne.canonical_json(ex),max_qubits=7,max_expanded_stages=len(gates))
    return gates


def rot(m):
    c,s=one,Golden()
    for _ in range(m):
        c,s=a*c-p*s,p*c+a*s
    return c,s


def start(spin,ports,y,ts):
    out={}
    for port,vp in enumerate(ports):
        for t,vt in enumerate(ts):
            for f,vf in enumerate(v):
                for g,vg in enumerate(v):
                    amp=vp*vt*vf*vg
                    if amp!=0:
                        out[(((spin*2+port)*2+y)*2+t)*4+2*f+g]=amp
    return out


def check_map(k):
    gates=word(k)
    c,s=rot(4*k)
    for old in range(32):
        state={old*4+2*i+j:v[i]*v[j] for i in range(2) for j in range(2)}
        for g in gates:
            state=action(state,g,7)
        assert state=={4*old:c,4*old+(2 if old%4==3 else 1):s}
    for y in range(2):
        state=start(0,(one,Golden()),y,v)
        for gate in gates:
            state=action(state,gate,7)
        cold=Golden()
        measured=Golden()
        for out in range(4):
            psi=[state.get(y*8+t*4+out,Golden()) for t in range(2)]
            mass=sum(amp*amp for amp in psi)
            along=sum(amp*w for amp,w in zip(psi,v))
            passive=v[out//2]*v[out%2]
            cold+=along*passive
            if mass==0:
                assert out==3 or (out==2 and y==0)
                continue
            expected=one if y==0 or out==0 else (p if out==1 else p*p)
            assert along*along==mass*expected
            measured+=passive*passive*expected
        assert cold==p*c+a*p*s
        assert measured==p
    for bit in (0,1):
        start_tail={2*bit+j:w for j,w in enumerate(v)}
        tail=start_tail
        motions=[]
        for g in (ne.Gate('CX',(0,1)),ne.Gate('G',(1,)),ne.Gate('CX',(0,1))):
            after=action(tail,g,2)
            h=sum(w*after.get(i,Golden()) for i,w in tail.items())
            motions.append(one-h*h)
            tail=after
        overlap=sum(w*tail.get(i,Golden()) for i,w in start_tail.items())
        assert overlap*overlap==p
        assert motions==([0,p*p,0] if bit==0 else [p3*p3,p*p,1])
    return s*s


def checked_sum(k,y,t):
    state=start(0,v,y, t if isinstance(t,tuple) else tuple(one if j==t else Golden() for j in range(2)))
    total=interval(0)
    for g in word(k):
        after=action(state,g,7)
        overlap=sum((amp*after.get(lab,Golden()) for lab,amp in state.items()),Golden())
        total=plus(total,trace_distance(overlap))
        state=after
    assert float(total[1]-total[0])<1e-7
    return total


def scalar_bounds(b):
    return tuple(float(x) for x in b)


def numerical_data(k):
    eta=check_map(k)
    ei=enclosure(eta)
    e=float(sum(ei)/2)
    pp=float(sum(enclosure(p))/2)
    s=e*pp**2; delta=1-e
    binary=lambda q:1+2*q*(1-q)
    def coherent(q):
        def branch(t):
            return 2 if t<.25 else sqrt(t)+sqrt(3*(1-t))
        return q*branch(q)+(1-q)*branch(1-q)
    def work(f):
        return f(s)+s*f(0)+(1-s)*f((e-s)/(1-s))-f(0)-f(e)
    wr=work(binary)
    assert abs(wr-2*s*((1-s)-delta**2/(1-s)))<1e-13
    assert wr/e <= 4*e*pp**3+1e-13
    # Prefix on all outcomes, including erased service and both old controls.
    # Explicit entropy rule h(p^2)=1+p^2 follows from positive normalized
    # p,p^2 and the actual lengths. Conditional totals subtract exactly eta.
    assert p+p*p==one and (p+2*p*p)-p*p==one
    assert (one+p3)*eta*p*p == eta*p*p + p3*eta*p*p
    totals={name:checked_sum(k,y,t) for name,y,t in
            [('00',0,0),('01',0,1),('10',1,0),('11',1,1),('0v',0,v),('1v',1,v)]}
    print('k=',k,'native gate inventory:',dict(Counter(g.op for g in word(k))))
    print('stage distances:', {key:tuple(round(t,8) for t in scalar_bounds(result))
                                for key,result in totals.items()})
    # Classical-golden source: premeasuring T versus following it coherently.
    known=plus(times(enclosure(p),totals['10']),times(enclosure(p*p),totals['11']))
    whole=plus(totals['1v'],times(-1,known))
    print('1v minus premeasured mixture, distance subtotal:',scalar_bounds(whole))
    si=times(ei,enclosure(p*p))
    di=minus(1,ei)
    wi=times(2,times(si,minus(minus(1,si),divide(times(di,di),minus(1,si)))))
    later=divide(minus(ei,si),minus(1,si))
    ci=minus(plus(lcd(si),plus(si,times(minus(1,si),lcd(later)))),plus(1,lcd(ei)))
    stages=plus(minus(totals['1v'],totals['0v']),times(si,enclosure(one+p3)))
    for certified,oracle in [(wi,wr),(ci,work(coherent))]:
        assert abs(float(sum(certified)/2)-oracle)<1e-13
    return ei,wi,ci,stages


def determinant(rows):
    n=len(rows)
    accum=interval(0)
    for perm in permutations(range(n)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term=interval(sign)
        for i,j in enumerate(perm):
            term=times(term,rows[i][j])
        accum=plus(accum,term)
    return accum


if __name__=='__main__':
    slopes=[]
    for k in (1,2,3,4):
        e,wr,wc,stage=numerical_data(k)
        slopes.append((e,wr,wc,stage))
        print('eta, registered, coherent, total stage secants:',
              [round(float(sum(x)/2),9) for x in slopes[-1]])
        signed=minus(times(sqrtiv(22),wr),e)
        if k==1:
            assert F('-.028138')<signed[0]<=signed[1]<F('-.028136')
        if k==3:
            assert F('1.21483')<signed[0]<=signed[1]<F('1.21485')
            assert F('-.0100')<stage[0]<=stage[1]<F('-.0099')
    cofs=[]
    for k in range(4):
        cofs.append(times((-1)**k,determinant([row[1:] for i,row in enumerate(slopes) if i!=k])))
    dot=interval(0)
    for row,cof in zip(slopes,cofs):
        dot=plus(dot,times(row[0],cof))
    norm_bound=sum(max(abs(lo),abs(hi)) for lo,hi in cofs)
    assert dot[0]>0
    assert dot[0]/norm_bound>F('0.00393')
    print('common-price residual at least',float(dot[0]/norm_bound))
