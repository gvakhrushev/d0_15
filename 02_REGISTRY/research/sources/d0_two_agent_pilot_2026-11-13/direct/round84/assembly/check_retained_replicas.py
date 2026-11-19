"""Check a native read-only programme, complete retained repeats, and interacting leaf costs."""
from itertools import product
from math import exp, log, sqrt
from pathlib import Path
import json
import sys

from mpmath import iv, mp

base = Path(__file__).resolve()
sys.path[:0] = [str(base.parents[2] / "round80" / "price"),
                str(base.parents[4] / "d0_native_readiness_amplification_2026-10-24")]
from check_parity_price import a, p, one, Golden, action, ne
from native_phase import phase_word


def run(gates, width, state):
    for gate in gates:
        state = action(state, gate, width)
    return state


def rotation(m):
    x, y = one, Golden()
    for _ in range(4*m):
        x, y = a*x-p*y, p*x+a*y
    return x, y


def decimal(value):
    mp.dps = 85
    alpha = mp.sqrt((mp.sqrt(5)-1)/2)
    return float(sum(v*alpha**j for j,v in enumerate(value.coefficients)))


def native_trials():
    # Spin 0,1; SourceI 2; one read-only programme 3. Each trial has its
    # own golden selector and clean pointer. The approved inverse on a born
    # pointer is accounted for separately; this word tests the joint readout.
    modes = ((1,5),(1,2))
    def word(width, selector, target):
        layout = ne.Execution(width,(target,),(),(),ne.G_CX_SOURCE_I,2,(0,1))
        return tuple(g for k,j in product(range(2),repeat=2)
                     for g in phase_word(layout,(3,selector),(k,j),target,modes[k][j],
                                         max_qubits=width,max_expanded_stages=400))
    gates = word(6,4,5)
    for column in range(64):
        k,j,b = (column>>2)&1,(column>>1)&1,column&1
        c,d = rotation(modes[k][j])
        assert run(gates,6,{column:one}) == {column:c,column^1:(-d if b else d)}
    s = [p*rotation(modes[k][0])[1]*rotation(modes[k][0])[1]+
         p*p*rotation(modes[k][1])[1]*rotation(modes[k][1])[1] for k in range(2)]
    gates2 = word(8,4,5)+word(8,6,7)
    for k in range(2):
        old = 7  # arbitrary occupied Spin and SourceI bits
        start = {old<<5|k<<4|j<<3|l<<1:(a,p)[j]*(a,p)[l]
                 for j,l in product(range(2),repeat=2)}
        state = run(gates2,8,start)
        for b,c in product(range(2),repeat=2):
            mass = sum((coef*coef for i,coef in state.items() if
                        ((i>>2)&1)==b and (i&1)==c),Golden())
            assert mass==(one-s[k],s[k])[b]*(one-s[k],s[k])[c]
        assert all(i>>5==old and ((i>>4)&1)==k for i in state)
    assert all(.2<decimal(x)<.4 for x in s) and s[0]!=s[1]
    # State-only alternative: the native pair v and Gv have strictly
    # positive real amplitudes and their one-read affinity equals overlap.
    gv = (p-p*p,2*a*p)
    overlap = a*gv[0]+p*gv[1]
    assert overlap==a and overlap*overlap==p
    assert decimal(p)<decimal(a)<1
    return dict(gates_per_native_word=len(gates),all_native_columns=64,
                two_run_joint_weights_checked=8, probabilities=[round(decimal(x),12) for x in s],
                single_specimen_affinity=round(decimal(a),12),
                iid_two_read_affinity=round(decimal(p),12))


def test_interacting_prices():
    iv.dps = 60
    ip = (iv.sqrt(5)-1)/2
    il = -iv.log(ip)
    assert (1-16*ip**6)/(il*(1+4*ip**6))>iv.mpf(".18")
    assert iv.log(iv.mpf(3)/2)/il>iv.mpf(".84")
    ell = log((1+sqrt(5))/2)
    n = 6
    def full(s,alpha,source):
        # A moving three-valued original record plus genuine multi-bit interactions.
        old = (.12+source,.37-source,.51)
        def H(ps):
            return -sum(x*log(x)/ell for x in ps)
        entropy = H(old)+n*H((1-s,s))
        vals = []
        for z in range(3):
            for bits in product((0,1),repeat=n):
                m = sum(bits)
                multi = (z+.45)*sum(bits[j]*bits[j-1] for j in range(1,n))
                cost = (-1,7,4)[z]+(z+1)*source+6*(n+m)+multi+.07*m*(m-1)
                joint = log(old[z])+m*log(s)+(n-m)*log(1-s)
                vals.append((cost-alpha*entropy+(1-alpha)*joint/ell,m))
        mincost=min(v[0] for v in vals)
        weights=[exp(-ell*(v[0]-mincost)) for v in vals]
        assert all(m==0 for v,m in vals if v==mincost)
        return mincost-log(sum(weights))/ell,mincost
    for s,alpha in product((.21,.27,.38),(0,.25,.6,1)):
        h=1e-6
        l,r=full(s-h,alpha,0),full(s+h,alpha,0)
        assert all((y-x)/(2*h*n)<-.18 for x,y in zip(l,r))
        # The full derivative along a moving old prefix differs by precisely
        # the old-source term. It must not be set to zero on each finite n.
        l2,r2=full(s-h,alpha,-h),full(s+h,alpha,h)
        l3,r3=full(s,alpha,-h),full(s,alpha,h)
        assert all(abs((r2[i]-l2[i])-(r3[i]-l3[i])-(r[i]-l[i]))<2e-9 for i in range(2))
    return dict(histories_per_evaluation=3*2**n,interacting_costs=True,
                rigorous_negative_slope_per_copy=">.18 in magnitude",
                old_source_may_be_transverse=True)

if __name__=="__main__":
    print(json.dumps(dict(native=native_trials(),full_record=test_interacting_prices(),
                          full_geometry_loader_executed=False,GR_closed=False),indent=2))
