"""Adaptive frontiers, paid padding and signed field contrast on the native scene.

Python 3 standard library. Run beside the pinned check_prefix_cx.py, which owns
the exact Golden arithmetic and the six-wire NPS2 realization used here.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import factorial
from pathlib import Path
import json
import runpy


def need(ok, msg):
    if not ok:
        raise ArithmeticError(msg)


owner = Path(__file__).with_name("check_prefix_cx.py")
need(sha256(owner.read_bytes()).hexdigest() ==
     "433a5cfa6cb753f631cfeda9b9a8778b4d37675b9764ed7d6b57a98d43342a61",
     "pinned six-wire and interval arithmetic")
g = runpy.run_path(str(owner))
O, I, a, p = (g[k] for k in ("O","I","A","P"))
add, times, power, scale = (g[k] for k in ("add","times","power","scale"))
box, mul, plus, minus, ratio = (g[k] for k in ("box","mul","plus","minus","ratio"))
enclosure, fmt = (g[k] for k in ("enclosure","endpoints"))
Z = g["Z"]


def ae(v):
    return box(*enclosure(v))


def frontiers():
    # Price at an actual leaf may depend on its entire history and depth.
    # A common price is factored out of that same leaf only, never across
    # different leaves. Any two positive decompositions give identical sums.
    q, short_total, long_total = F(2,5), F(7,13), F(17,8)
    short = {"0": short_total*(1-q), "1": short_total*q}
    long = {"00":long_total*(1-q)/7, "01":long_total*(1-q)*6/7,
            "10":long_total*q*2/3, "11":long_total*q/3}
    prices = {"0":F(3,4), "1":F(7,11), "00":F(4,9), "01":F(7,19),
              "10":F(12,17), "11":F(2,15)}
    core = {s:w/prices[s] for s,w in dict(short, **long).items()}
    def mass(leaves):
        return sum(core[h]*prices[h] for h in leaves)
    retained = ("0","10","11")
    true = mass(("10","11"))/mass(retained)
    R = long_total/short_total
    need(true == q*R/(1-q+q*R) and true != q, "hybrid front on actual leaf masses")
    # Allow positive, context-dependent terminal accommodation. To restore the
    # original Born law one must pay the exact relative factor 1/R.
    compensate = 1/R
    corrected = compensate*mass(("10","11"))/(mass(("0",))+compensate*mass(("10","11")))
    need(corrected == q, "necessary boundary payment")
    return {"demonstration_q":str(q),"unequal_inclusive_totals_ratio":str(R),
            "forced_hybrid_probability":str(true),
            "relative_hybrid_long_vs_short_correction":str(compensate)}


def graph_padding():
    size=(9,11,13)
    space_edges=sum(size[i]*size[j] for i in range(3) for j in range(i+1,3))
    V=sum(size); grade1=space_edges+V; full=V+grade1
    need((V,grade1,space_edges,full)==(33,392,359,425), "all spatial and temporal modes")
    # Four true canonical births from rank four, then eight 64-column square
    # operations. The final square is the closing gate, not an extra stage.
    initial_stages=[4,8,16,32]+[64]*8
    D=sum(initial_stages); live=64
    q=ae(add(power(p,2),scale(power(p,6),2)))
    def padded(m):
        R=F(space_edges*(D+2*m*live),full*D)
        need(R>1,"positive raw growth margin")
        qmix=ratio(mul(q,box(R)),plus(minus(box(1),q),mul(q,box(R))))
        tv=minus(qmix,q)
        need(tv[0]>0,"positive hybrid probability defect")
        return {"D":D+2*m*live,"lower_Z_H_ratio":str(R),
                "lower_hybrid_P1":fmt(qmix,14)[0],"lower_TV":fmt(tv,14)[0]}
    return {"D_unpadded":D,"true_full_modes":full*D,"true_q":fmt(q,17),
            "padding_pairs":{"1":padded(1),"32":padded(32),"256":padded(256)}}


def late_cold(seq):
    initial=[power(a,2),times(a,p),times(a,p),power(p,2)]
    state=initial.copy()
    for gate in seq:
        if gate=="G":
            new=[]
            for i in (0,2):
                x,y=state[i:i+2]
                new.extend((add(times(a,x),scale(times(p,y),-1)),
                            add(times(p,x),times(a,y))))
            state=new
        else:
            state=[state[i] for i in (0,1,3,2)]
    return sum_g([times(x,y) for x,y in zip(initial,state)])


def sum_g(values):
    out=O
    for x in values:
        out=add(out,x)
    return out


def early_comparison():
    # Two six-call cells on actual source e. Z_e is two SourceI operations.
    # Write G_e explicitly (native G on wire 2); all other calls reuse the
    # pinned six-wire core. Match front and rear legs to retain NPS6.
    s = g["S"]; ge=("G_e",)
    idle=[ge,s,s,ge,s,s]; pos=[ge,ge,s,s,s,s]; neg=[s,s,ge,ge,s,s]
    raw=[g["BANK"],g["C"],s,s,g["BANK"]]; enc=g["original_suffix"][-3:]
    def run(state, word):
        for gate in word:
            if gate==ge:
                out={}
                for idx,x in state.items():
                    g["add_term"](out,idx,times(a,x))
                    g["add_term"](out,idx^8,scale(times(p,x),-1 if idx&8 else 1))
                state=out
            else:
                state=g["execute"](state,[gate])
        return state
    def dot(l,r):
        return sum_g([times(x,r.get(i,O)) for i,x in l.items()])
    outcomes=[]
    for front,rear in ((idle*2,idle*2),(pos*2,neg*2)):
        word=front+raw+rear+enc
        values=[]
        for spin,born in enumerate(g["BIRTH"]):
            entered=run(born,front+[g["BANK"]])
            q=sum_g([times(x,x) for i,x in entered.items() if i&8])
            final=run(born,word)
            c=dot(born,final)
            need(all(dot(b,final)==O for i,b in enumerate(g["BIRTH"]) if i!=spin),
                 "proper scalar corner on every actual Spin column")
            eta=scale(times(a,p),2)
            expect=times(a,add(I,scale(times(add(I,eta),q),-1)))
            need(c==expect,"NPS6 directly on the matched preparations")
            values.append((q,c))
        need(len(set(values))==1,"all four protected inputs agree")
        outcomes.append((word,*values[0]))
    need(Counter(outcomes[0][0])==Counter(outcomes[1][0]),"equal-literal-price inventory only")
    need(outcomes[0][1]==scale(power(p,3),2),"original six-wire event")
    qdiff=ae(add(outcomes[0][1],scale(outcomes[1][1],-1)))
    need(0<qdiff[0] and max(ae(o[1])[1] for o in outcomes)<F(1,2),"two different true events in collar")
    return [(q,c) for _,q,c in outcomes],qdiff


def heat_bound(L):
    x=F(2,55)
    return F(176,359)*x**L/(factorial(L)*(1-x*x)*(1-x/L))


def normalized():
    high=late_cold(("G","CX")); low=late_cold(("CX","G"))
    centre=add(times(a,p),scale(power(p,4),2))
    need(high==add(centre,power(p,6)) and low==add(centre,scale(power(p,6),-1)),
         "two literal, equally long spectator words on the newborn pair")
    mu_hi,mu_lo=times(high,high),times(low,low)
    gap=ae(add(mu_hi,scale(mu_lo,-1)))
    need(gap[0]>0,"distinct fresh born masses")
    R=mul(box(F(1,2)),plus(box(1),ae(scale(times(a,p),2))))
    # dQ(J_plus-J_minus) = 16 z(1-z) p R (1-2RQ) Δmu/(h_plus h_minus).
    # All h<=1, so substitute Q<=1/2 to obtain a uniform lower bound.
    Jfloor=mul(box(16*Z*(1-Z)),mul(mul(ae(p),R),mul(minus(box(1),R),gap)))
    rows,dq=early_comparison()
    L=8
    # two late square calls + three literal CX;CX pairs after last birth.
    pairs=(L-2)//2
    need(L==2+2*pairs,"true youngest suffix age")
    heaterr=4*heat_bound(L)
    Jcontrast=mul(Jfloor,dq)
    lower=Jcontrast[0]-heaterr
    need(lower>0 and heaterr<Jcontrast[0]/2,"double difference after full unnormalized/normalized heat")
    first=rows[0][1]
    Jvalue=mul(box(4*Z),mul(ae(times(first,first)),gap))
    need(Jvalue[0]>2*heat_bound(L),"nonzero at one fixed early word")
    return {"late_words":["G1;CX01","CX01;G1"],"exact_late_cold_power_basis":[high,low],
            "early_Q_native": [fmt(ae(q),18) for q,_ in rows],
            "early_cold_native":[fmt(ae(c),18) for _,c in rows],
            "equal_early_square_calls":32, "late_square_calls_before_common_pairs":2,
            "paid_pairs":pairs,"youngest_suffix_age":L,"CL8_A_L_exact":str(heat_bound(L)),
            "lower_uniform_dJ_dQ":fmt(Jfloor,21)[0],"upper_double_heat_error":fmt((heaterr,heaterr),24)[1],
            "strict_lower_double_change_of_B":fmt((lower,lower),21)[0],
            "short_vs_late_controller":"the conditional dispatcher and any extra dephasing/clock must have a common-leaf embedding and be paid separately",
            "physical_field":"same inequality for matched geometric NPS2 endpoints with their true nonzero Delta Q and current native cold NPS6. Choose common padding after Delta Q is established; do not treat a change of native preparation as a spacetime field by declaration."}


if __name__=="__main__":
    print(json.dumps({"schema":"d0.optional-clock-frontiers/1","status":"PASS",
          "frontiers":frontiers(),"true_raw_padding":graph_padding(),
          "normalized_native_comparison":normalized(),
          "original_positive_economic_measure_with_shared_stop_prices_identified":False,
          "GR_closed":False}, indent=2))
