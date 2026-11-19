"""Replay the two addressed coframe secants on one marked CAR/Fourier run."""
import json
from itertools import product
import mpmath as mp

mp.mp.dps = 65
p = (mp.sqrt(5)-1)/2
ell = -mp.log(p)
theta = mp.asin(p)
h = mp.mpf(1)/4
amp = p*mp.sin(448*theta)
overlap = mp.mpf(5)/16
z = mp.mpf(2)**-20
gold_lambda = -2*p**-5*((1-4*z*p**3*(1+p**6))/(1-4*z*p**3)+p**6)
energies = (2*(amp/h)**2, 4*(amp/h)**2)
beta = 2*p**3*(1-overlap)
eta = p**3*overlap*h*h
material = tuple(beta+eta*e for e in energies)
pulse = 2320*theta - 2*mp.pi*mp.nint(2320*theta/(2*mp.pi))
step = mp.mpf(1)/128
X = mp.matrix([[0,1],[1,0]])


def check(value, message):
    if not value:
        raise ArithmeticError(message)


def close(a,b):
    check(abs(a-b) < mp.mpf("2e-55"), (str(a),str(b)))


def rot(x):
    return mp.matrix([[mp.cos(x),-mp.sin(x)],[mp.sin(x),mp.cos(x)]])


def entropy(q):
    return -(q*mp.log(q)+(1-q)*mp.log(1-q))/ell


def angle_entropy(x):
    return entropy(mp.sin(theta+x)**2)


def show(x):
    return mp.nstr(x, 19)


def tree(u, v, alpha):
    # Admissions and failed prefixes are paid; the single aggregated fail here
    # may be refined by any fixed earlier tape without changing either secant.
    values = [(1-alpha, 1, None)]
    for j, route, m, phase in product(range(2), repeat=4):
        label = j ^ route
        g = (u,v)[label]
        pm = material[j] if m else 1-material[j]
        weight = alpha*pm/8
        flip = X if route ^ m else mp.eye(2)
        op = rot(theta)*flip*rot(g)*flip*rot(phase*mp.pi/2)
        # Acting on one Bell half followed by registering parity.
        odd = (op[0,1]**2+op[1,0]**2)/2
        target = mp.sin(theta+(-1)**(route^m)*g+phase*mp.pi/2)**2
        close(odd, target)
        # Unprocessed and decoded active qubit is maximally mixed locally.
        close(mp.norm(op*op.T-mp.eye(2)),0)
        for b in range(2):
            values.append((weight*(odd if b else 1-odd), 1+b, (j,route,m,phase,b)))
    close(sum(row[0] for row in values),1)
    return values


def measure_ledger(u,v,alpha):
    rows=tree(u,v,alpha)
    code=sum(prob*cost for prob,cost,_ in rows)
    shannon=-sum(prob*mp.log(prob)/ell for prob,_,_ in rows)
    return code-shannon


def source():
    check(0 < pulse < mp.mpf(".012") and 0 < theta-pulse < theta+pulse < mp.pi/4,
          "actual signed Golden pulse stays on positive entropy arc")
    alpha=mp.mpf(3)/17  # regression weight; the theorem retains true readiness as a symbol
    finite_entropy=(angle_entropy(pulse)-angle_entropy(-pulse))/(2*step)
    gain=alpha*eta*finite_entropy/(2*abs(gold_lambda))
    targets=[gold_lambda*(energies[1-j]-energies[j]) for j in (0,1)]
    for k in (0,1):
        pos=[0,0]; pos[k]=pulse
        neg=[-x for x in pos]
        src=(measure_ledger(*pos,alpha)-measure_ledger(*neg,alpha))/(2*step)
        close(src,gain*targets[k])
    # Independent full-tape conservation: the unused marginal cannot be
    # replaced by an extra informative outcome known to the tariff.
    for j,s,m in product(range(2),repeat=3):
        mats=[]
        for phase in (0,1):
            flip=X if m^s else mp.eye(2)
            op=rot(theta)*flip*rot(pulse)*flip*rot(phase*mp.pi/2)
            vector=mp.matrix([op[0,0],op[1,0],op[0,1],op[1,1]])/mp.sqrt(2)
            mats.append(vector*vector.T)
        want=mp.matrix([[1,0,0,1],[0,1,-1,0],[0,-1,1,0],[1,0,0,1]])/4
        close(mp.norm((mats[0]+mats[1])/2-want),0)
    return {"conditional_material":list(map(show,material)),
            "energy_on_adjacent_interior_edges":list(map(show,energies)),
            "target_two_volume_rows":list(map(show,targets)),
            "native_angle":show(pulse), "fixture_coframe_step":str(step),
            "exact_positive_secant_gain_per_true_ready_mass":show(gain/alpha),
            "explicit_archive": "32 successful fine leaves plus pre-field stops"}


def first_jet_and_obstruction():
    # Exact evaluation for the finite probability law via analytic derivatives.
    pf=mp.mpf(2)/5
    P=[pf,mp.mpf(1)/5,mp.mpf(2)/5]
    A=mp.mpf(3)/7
    # Enforce common absolute weight on the pre-field stopped leaf.
    ps=[mp.mpf(0),mp.mpf(".11"),mp.mpf("-.11")]
    dpi=[ell*pf*A,0,0]
    for i in (1,2):
        dpi[i]=ps[i]-ell*pf*A*P[i]/(1-pf)
    close(sum(dpi),0)
    fisher=sum((v-w)**2/q for v,w,q in zip(ps,dpi,P))/ell
    floor=ell*pf*A**2/(1-pf)
    close(fisher,floor)
    def entropy_difference(t):
        law=[q+t*v for q,v in zip(P,ps)]
        # Guarantee the exact early weight W_F = constant at all t and A'(0)=A.
        f=pf*mp.exp(ell*A*t)
        part=[P[i]+t*dpi[i] for i in (1,2)]
        priced=[f]+[(1-f)*v/sum(part) for v in part]
        return sum(q*mp.log(q/r)/ell for q,r in zip(law,priced))
    close(mp.diff(entropy_difference,0,1),0)
    close(mp.diff(entropy_difference,0,2),floor)
    # Verify the full positive Book identity in a non-Born law with a
    # history-dependent unsigned cost and nonconstant realized Info.
    cost=[mp.mpf(1),mp.mpf(3),mp.mpf(4)]
    info=[mp.mpf(".25"),mp.mpf(".7"),mp.mpf("1.4")]
    weights=[p**(c-i) for c,i in zip(cost,info)]
    total=sum(weights)
    ent=-sum(q*mp.log(q)/ell for q in P)
    kl=sum(q*mp.log(q*total/w)/ell for q,w in zip(P,weights))
    close(-mp.log(total)/ell, sum(q*(c-i) for q,c,i in zip(P,cost,info))-ent-kl)
    delta=mp.mpf(1)/13
    deviation=pf*mp.tanh(ell*delta/2)
    shares=(pf-deviation,pf+deviation)
    close(mp.log(shares[1]/shares[0])/ell,delta)
    for shift in (mp.mpf("-.1"), mp.mpf("-.01"), mp.mpf(".03")):
        low=shares[0]+shift
        high=low*mp.exp(ell*delta)
        check(max(abs(low-pf),abs(high-pf)) >= deviation,"finite early-event bound")
    return {"sharp_finite_stop_deviation":show(deviation),
            "common_stop_fisher_bound_attained":show(floor),
            "positive_book_identity_checked":True, "baseline_KL_first_derivative":"0"}


if __name__ == "__main__":
    print(json.dumps({"one_collar_joint_secants":source(),
                      "absolute_price":first_jet_and_obstruction(),
                      "geometric_name_physically_selected":False,
                      "unconditional_original_Book03_price_identified":False,
                      "GR_closed":False},indent=2))
