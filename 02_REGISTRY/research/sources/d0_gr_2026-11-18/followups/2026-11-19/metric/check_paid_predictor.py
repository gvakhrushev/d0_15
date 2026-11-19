"""Paid binary classifier on the actual NPS2 tail with no access to old r.

Replay with Python 3 and the two pinned sibling files. Exact gate arrays act
over Z[a], a^4+a^2=1. Entropies use rational outward-rounded logarithms.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import runpy


def pinned(name, digest):
    path = Path(__file__).with_name(name)
    if sha256(path.read_bytes()).hexdigest() != digest:
        raise ValueError("unexpected source " + name)
    return runpy.run_path(str(path))


gate = pinned("check_prefix_cx.py","433a5cfa6cb753f631cfeda9b9a8778b4d37675b9764ed7d6b57a98d43342a61")
ar = pinned("check_extra_work.py","93d93b4923062bc2aa831afbcfda84b0c2cbab1baeeca49b43538ac5090acc45")
need,zero,one,a,p = (gate[k] for k in ("need","O","I","A","P"))
add,prod,powg,scale,add_term = (gate[k] for k in ("add","times","power","scale","add_term"))
span = ar["span"]
ln2 = span(2).log_positive()


def sub(x,y):
    return add(x,scale(y,-1))


def log01(x):
    need(0 < x.lo <= x.hi < 1,"probability strictly between zero and one")
    n=0
    while x.lo<=1:
        x=2*x
        n+=1
    return x.log_positive()-n*ln2


def base(n, invert=False, flag=None):
    # For e=0: b=0 has tail G²|0>, b=1 tail |0>. If invert=True,
    # positive output is |1> after rotating, so the known-one is unnecessary.
    def cosine_squared(k):
        c,s=one,zero
        for _ in range(abs(k)):
            c,s=sub(prod(a,c),prod(p,s)),add(prod(p,c),prod(a,s))
        return prod(c,c)
    A,B=cosine_squared(2-n),cosine_squared(n)
    if invert:
        A,B=sub(one,A),sub(one,B)
    if flag is not None:
        # Independent coherent flag toggles the raw complement according
        # to its computational measurement; the flag itself is unread.
        def mix(z):
            return add(prod(flag,z),prod(sub(one,flag),sub(one,z)))
        A,B=mix(A),mix(B)
    l=powg(p,2)
    return [prod(p,sub(one,A)),prod(p,A),prod(l,sub(one,B)),prod(l,B)]


def bern(v):
    return -v*log01(v)-(1-v)*log01(1-v)


def interval(golden):
    return ar["Span"](*gate["enclosure"](golden))


def evaluate(row,q,ell):
    l=interval(powg(p,2)); gain=interval(powg(p,3))
    Q=(q-l)/gain
    m=[interval(v) for v in row]
    prob=[(1-Q)*m[i]+Q*m[3-i] for i in range(4)]
    deriv=[(m[3-i]-m[i])/gain for i in range(4)]
    y=prob[1]+prob[3]
    dy=deriv[1]+deriv[3]
    entropy=-sum((x*log01(x) for x in prob),span(0))
    price=2+q+y-entropy/ell
    slope=1+dy+sum((d*log01(x) for d,x in zip(deriv,prob)),span(0))/ell
    need(slope.lo>0,"strict source of claimed predictor")
    return {"conditional_e0_joint_exact":row,"joint_B_Y_at_qstar":[x.fmt(14) for x in prob],
            "error_probability":(prob[1]+prob[2]).fmt(15),"Pr_Y_1":y.fmt(15),
            "joint_shannon_nats":entropy.fmt(15),"two_code_cost_minus_info":price.fmt(15),
            "slope_wrt_q":slope.fmt(15)}


def cx(c,t):
    return ("CX",c,t)


def G(t):
    return ("G",t)


E, B, R, T, D, NEW_TAIL, FLAG = range(2,9)
S=("SourceI",E,0,1)


def z(t):
    if t==E:
        return [S,S]
    sw=[cx(E,t),cx(t,E),cx(E,t)]
    return sw+[S,S]+sw


def inv(t):
    return z(t)+[G(t)]+z(t)


def apply(state,word):
    # Spin axes 0,1, source e=2. Physical bit i occupies mask 1<<i.
    for op in word:
        out={}
        for k,x in state.items():
            if op[0]=="G":
                mask=1<<op[1]
                add_term(out,k,prod(a,x))
                add_term(out,k^mask,prod(scale(p,-1 if k&mask else 1),x))
            elif op[0]=="CX":
                c,t=op[1:]
                add_term(out,k^((1<<t) if k&(1<<c) else 0),x)
            else:
                need(op==S,"actual surviving gate")
                active=bool(k&(1<<E))
                add_term(out,k^(2 if active else 0),scale(x,-1 if active and k&2 else 1))
        state=out
    return state


def append(state,t,known_one=False):
    out={}
    for j,x in state.items():
        if known_one:
            out[j|(1<<t)]=x
        else:
            out[j]=prod(x,a)
            out[j|(1<<t)]=prod(x,p)
    return out


def original(spin):
    state={spin:one}
    for t in (E,B,R,T):
        state=append(state,t)
    word=[cx(B,E),cx(E,R),S,S,cx(B,E),cx(R,T),G(T),cx(R,T)]
    return apply(state,word)


def exact_native(n,mode,row):
    # d is born before moving the old controlled tail. After the two CXs the
    # old physical tail always equals zero; the potentially nonorthogonal
    # quantum signal resides in the new live d. Old r is never used again.
    transfer=inv(D)+[cx(T,D),cx(D,T)]
    bank=[cx(B,E)]
    power=1-n
    native_power=[G(D)]*power if power>=0 else inv(D)*(-power)
    classifier=[cx(E,D)]+native_power+[cx(E,D)]+inv(D)+[cx(E,D)]
    if mode=="known_one":
        classifier.append(cx(FLAG,D))
    if mode=="golden_flag":
        classifier.extend((G(FLAG),cx(FLAG,D)))
    encoder=[cx(D,NEW_TAIL),G(NEW_TAIL),cx(D,NEW_TAIL)]
    suffix=transfer+bank+classifier+bank+encoder
    need(all(R not in op[1:] for op in suffix),"no access to original registered pointer")
    # True event after A=CX(b,e) on its original v,v input.
    q_event=scale(powg(p,3),2)
    expect=[add(prod(sub(one,q_event),row[i]),prod(q_event,row[3-i])) for i in range(4)]
    # In the old PVM, b=0 leaves t unread; b=1 verifies old t=0. Even if
    # already registered, replay gives the same joint law: all suffix gates
    # commute with the stored pointer and act on its other factors.
    for spin in range(4):
        initial=original(spin)
        for t in (D,NEW_TAIL):
            initial=append(initial,t)
        if mode!="direct":
            initial=append(initial,FLAG,known_one=(mode=="known_one"))
        final=apply(initial,suffix)
        probs=[zero]*4
        for k,x in final.items():
            b,y=(k>>R)&1,(k>>D)&1
            need(not (k&(1<<T)) and not (y and (k&(1<<NEW_TAIL))),
                 "old valid code and new valid code including their physical tails")
            need(k&3==spin,"complete circuit restored all original Spin coordinates")
            probs[2*b+y]=add(probs[2*b+y],prod(x,x))
        need(probs==expect,"full exact paid branch law, every Spin column")
    return {"n":n,"expanded_square_calls_after_first_NPS2":len(suffix),
            "fixture_bank_enter_and_leave_calls":2,
            "after_first_code_inventory":{op:sum(g[0]==op for g in suffix) for op in ("CX","G","SourceI")},
            "fresh_born_work_bits":2+(mode!="direct"),
            "first_code_protected":True,"old_tail_state_transferred_to_live_d":True,
            "separate_record_E":False}


def helstrom(q,ell):
    ip=interval(p); l=ip**2; overlap=ip**3
    d=(1-4*ip*l*overlap**2).sqrt()
    e=(1-d)/2
    y=(q-e)/d
    h=bern(y)+bern(e)
    price=2+q+y-h/ell
    slope=1+(1-(log01(1-y)-log01(y))/ell)/d
    # P(guess=1|state) from the actual Helstrom projector for e=0.
    # Δ=pρ0-lρ1 has eigenvalues lambda_+,lambda_- separated by d.
    lp=(ip-l+d)/2
    yh0=(lp-ip+l*overlap**2)/d
    yh1=(lp-ip*overlap**2+l)/d
    row=[ip*(1-yh0),ip*yh0,l*(1-yh1),l*yh1]
    for wrong,total in ((row[2],row[0]+row[2]),(row[1],row[1]+row[3])):
        residual=wrong-e*total
        need(residual.lo<=0<=residual.hi,"posterior error epsilon for either guess")
    need(slope.lo>1 and e.lo>0,"ideal comparator")
    return {"error":e.fmt(15),"Pr_Y_1":y.fmt(15),"two_code_cost_minus_info":price.fmt(15),
            "slope_wrt_q":slope.fmt(15),"finite_exact_gate_claim":False}


def main():
    q,ell=ar["centre"]()
    z=powg(p,6)
    cases=(("complementary_axis_n_minus_12",-12,"direct",base(-12,True)),
           ("complementary_axis_n2",2,"direct",base(2,True)),
           ("zero_axis_n0_given_paid_one",0,"known_one",base(0)),
           ("zero_axis_n0_full_noisy_flag",0,"golden_flag",base(0,flag=sub(one,z))))
    result={}
    for title,n,mode,row in cases:
        result[title]=dict(evaluate(row,q,ell),gate_control=exact_native(n,mode,row))
    optimum=helstrom(q,ell)
    near=result["complementary_axis_n_minus_12"]
    need(F(near["slope_wrt_q"][0]) > F(optimum["slope_wrt_q"][1]) and
         F(near["error_probability"][0]) > F(optimum["error"][1]),
         "strict native-vs-ideal comparison of both objectives")
    return {"schema":"d0.paid-binary-predictor/1","status":"PASS","q_star":q.fmt(15),
            "fixed_log_unit":"ln(phi)","labels":["00","01","10","11"],
            "classifiers":result,"ideal_helstrom":optimum,
            "physical_scope":"B and Y coded lengths and Shannon gain of these two registered labels only; any additional services, retained material state, and underlying Book edge charges are separate",
            "GR_closed":False}


if __name__=="__main__":
    print(json.dumps(main(),ensure_ascii=False,indent=2))
