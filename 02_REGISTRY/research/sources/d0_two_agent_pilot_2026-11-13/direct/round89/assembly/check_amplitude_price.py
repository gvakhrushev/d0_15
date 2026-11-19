"""Keep each physical initial record when comparing probability and amplitude weights."""
from itertools import product
import json
import mpmath as mp

mp.mp.dps=70
p=(mp.sqrt(5)-1)/2
theta=mp.asin(p)
ell=-mp.log(p)
pulse=2320*theta-2*mp.pi*mp.nint(2320*theta/(2*mp.pi))
amp=p*mp.sin(448*theta)
coherence=mp.mpf(5)/16
align=(mp.mpf(0),-amp**2)
q=[2*p**3*(amp**2-coherence*x) for x in align]


def check(ok,label):
    if not ok:
        raise ArithmeticError(label)


def almost(a,b):
    check(abs(a-b)<mp.mpf("3e-60"),(a,b))


def law(xs,ready,fails):
    # ready[a] is the probability of a common fine factory tape, before
    # fair J, route and phase. All failure records end before field access.
    leaves=list(fails)
    for prob in ready:
        for j,s,m,phase,b in product(range(2),repeat=5):
            pm=q[j] if m else 1-q[j]
            angle=theta+(-1)**(s^m)*xs[j^s]+phase*mp.pi/2
            pb=mp.sin(angle)**2 if b else mp.cos(angle)**2
            leaves.append(prob*pm*pb/8)
    almost(sum(leaves),1)
    return leaves


def run():
    check(0<q[0]<q[1]<1,"genuine incoming field yields a strict contrast")
    a=lambda x: mp.cos(theta+x)+mp.sin(theta+x)
    v=[mp.sqrt(1-y)-mp.sqrt(y) for y in q]
    out=[]
    for ready,fails in (([mp.mpf(1)/3],[mp.mpf(2)/3]),
                        ([mp.mpf(1)/9,mp.mpf(2)/9],[mp.mpf(1)/2,mp.mpf(1)/6])):
        kappa=2*sum(map(mp.sqrt,ready))/mp.sqrt(8)
        expected=kappa*(a(pulse)-a(-pulse))*(v[0]-v[1])
        press=[]
        for k in range(2):
            vals=[]
            for sign in (1,-1):
                x=[0,0]
                x[k]=sign*pulse
                leaves=law(x,ready,fails)
                z=sum(map(mp.sqrt,leaves))
                # True orthogonal record norm: an independent diagnostic.
                almost(mp.sqrt(sum(mp.sqrt(y)**2 for y in leaves)),1)
                # A fixed early fine leaf determines both global scales.
                anchor=mp.mpf(3)/8
                for power in (1,2):
                    scale=anchor/leaves[0]**(mp.mpf(1)/power)
                    weights=[scale*y**(mp.mpf(1)/power) for y in leaves]
                    almost(weights[0],anchor)
                    almost(sum(weights),scale*(1 if power==1 else z))
                vals.append(z)
            almost(vals[0]-vals[1],(-1)**k*expected)
            price=mp.log(vals[1]/vals[0])/ell
            press.append(price)
        almost(press[0],-press[1])
        check(press[0]<0<press[1],"absolute source sign")
        out.append([mp.nstr(x,17) for x in press])
    print(json.dumps({"material_clicks_no_background_coin":[mp.nstr(x,18) for x in q],
                      "full_example_price_changes":out, "all_fine_probabilities_retained":True,
                      "orthogonal_vector_norm_change":0, "positive_measure_price_change":0,
                      "compulsory_positive_amplitude_sum":False, "GR_closed":False}, indent=2))


if __name__=="__main__":
    run()
