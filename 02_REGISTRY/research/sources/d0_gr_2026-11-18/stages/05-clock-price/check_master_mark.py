"""Complete mark, true native chronological order control and finite-horizon receipts."""
import json
import math
from fractions import Fraction

import numpy as np
import sympy as sp


def mul(left, right):
    return np.einsum("ij,jk->ik", left, right, optimize=False)


def clock(word, golden, controlled_x):
    # Two independent born WORK bits; an untouched four-dimensional Spin is factored out.
    dims = [1, 2] + [4] * len(word)
    offsets = np.cumsum([0] + dims)
    size = sum(dims)
    basis = np.kron(golden, golden)
    rotated_g = mul(mul(basis.T,np.kron(golden,np.eye(2))),basis)
    rotated_cx = mul(mul(basis.T,controlled_x),basis)
    actions = {"A": rotated_g, "C": rotated_cx}
    shift = np.zeros((size, size))
    shift[1, 0] = 1
    for old_bit in range(2):
        shift[offsets[2] + 2*old_bit, offsets[1]+old_bit] = 1
    cold = np.eye(4)
    for j, letter in enumerate(word, start=2):
        gate = actions[letter]
        cold = mul(gate,cold)
        if j+1 < len(dims):
            shift[offsets[j+1]:offsets[j+2], offsets[j]:offsets[j+1]] = gate
        else:
            # Orthogonal detail closes at the most recent w in the passive basis.
            for bits in range(4):
                destination = offsets[2]+bits if bits&1 else (offsets[1]+1 if bits&2 else 0)
                shift[destination, offsets[j]:offsets[j+1]] = gate[bits, :]
    assert np.max(abs(mul(shift.T,shift)-np.eye(size))) < 1e-13
    return shift, cold[0,0]**2


def scene_heat(shift, beta, envelope, time_cap):
    color = np.repeat(np.arange(3), [9,11,13])
    adjacency = np.asarray(color[:,None] != color[None,:], dtype=float)
    degree = adjacency.sum(axis=0)+2
    temporal = np.diag(1/degree)
    normalized_scene = adjacency/np.sqrt(degree[:,None]*degree[None,:])
    clock_levels = np.linalg.eigvalsh(shift+shift.T)
    levels = np.concatenate([np.linalg.eigvalsh(np.eye(33)-normalized_scene-x*temporal)
                             for x in clock_levels])
    h = np.exp(-beta*levels).mean()
    # Explicit chronological sum of all closed scene walks by their signed temporal winding.
    # Each multiplication appends one move of the real stochastic program.
    route = adjacency/degree
    walks = {0:np.eye(33)}
    trace = {0:1.0}
    power = np.eye(len(shift))
    for n in range(1,time_cap+1):
        power = mul(power,shift)
        trace[n] = np.trace(power)/len(shift)
    expected = 0.
    rate = math.exp(-beta*envelope)
    for k in range(time_cap+1):
        expected += rate * sum(np.trace(ds)*trace[abs(n)] for n,ds in walks.items())/33
        if k == time_cap:
            break
        nxt = {}
        for n,ds in walks.items():
            for addr,mat in [(n,route),(n-1,temporal),(n+1,temporal)]:
                if addr not in nxt: nxt[addr] = np.zeros((33,33))
                nxt[addr] += mul(mat,ds)
        walks = nxt
        rate *= beta/(k+1)
    tail_bound = (beta*envelope)**(time_cap+1)/math.factorial(time_cap+1)/(1-beta*envelope/(time_cap+2))
    assert abs(expected - math.exp(-beta*(envelope-1))*h) <= tail_bound+3e-15
    return h, (1+expected)/2, float(tail_bound)


def fractional_coin(b, alpha, cap):
    # The threshold is read before a new recursive round. Unresolved histories get a success mark.
    n = math.floor(alpha)
    delta = alpha-n
    active, success = 1.,0.
    if delta == 0:
        return b**n
    for k in range(1, cap+1):
        success += active*b
        active *= (1-b)*(1-delta/k)
    return b**n*(success+active)


def model(word):
    p=(math.sqrt(5)-1)/2
    golden=np.array([[math.sqrt(p),-p],[p,math.sqrt(p)]])
    cx=np.eye(4)[[0,1,3,2]]
    shift,s=clock(word,golden,cx)
    rank, beta, z, envelope = 4, 2*p*p, 2.**-20, 6/5
    D=rank*len(shift)
    h,u,tail=scene_heat(shift,beta,envelope,17)
    a=359-66*math.exp(beta*(envelope-1))
    d=132*math.exp(beta*(envelope-1))
    anchor=a/(a+d)
    Q=(1-anchor)*(1-u)
    heat_race_mark=anchor*sum(Q**j for j in range(30))
    b=1-z+z*s
    feedback=fractional_coin(b,rank*beta,3)
    master=heat_race_mark*feedback
    Z=D*(359+66*h)
    action=math.log(Z)/beta-rank*math.log(b)
    ell=-math.log(p)
    normalized_truth=a*D*math.exp(-beta*action)
    assert abs(master-normalized_truth) < 3e-14
    golden_weight=(a*D)**(-ell/beta)*fractional_coin(master,ell/beta,60)
    assert abs(golden_weight-math.exp(-ell*action)) < 2e-16
    q=p*p+p**3*(1-master)
    gain=p**3*beta*master*(1-math.log((1-q)/q)/ell)
    assert p*p<q<.5 and gain>0
    return dict(native_word=word,clock_dimension=D,full_Hodge_dimension=425*D,s=s,
                H=math.log(Z)/beta,J=-rank*math.log(b),B=action,absolute_heat=Z,
                marked_probability_finite=master,marked_probability_identity=normalized_truth,
                golden_weight=golden_weight,readout_probability=q,terminal_to_B_gain=gain,
                poisson_tail_bound=tail)


def certified_contrast():
    p=(sp.sqrt(5)-1)/2
    a=sp.sqrt(p)
    G=sp.Matrix([[a,-p],[p,a]])
    A=sp.kronecker_product(G,sp.eye(2))
    C=sp.eye(4)[:,[0,1,3,2]]
    vv=sp.kronecker_product(G[:,0],G[:,0])
    diff=[]
    for w in ["AACCCC","ACACCC"]:
        out=vv
        for letter in w: out=(A if letter=="A" else C)*out
        diff.append(sp.simplify((vv.T*out)[0]**2))
    assert sp.simplify(diff[0]-p**6)==0
    assert sp.simplify(diff[1]-(p-2*a*p**3)**2)==0
    # Positive roots of x*x+x-1 and a*a-p enclosed by rational inequalities.
    low=Fraction(618033988749,10**12)
    high=Fraction(618033988750,10**12)
    au=Fraction(786151377759,10**12)
    assert low*low+low<1<high*high+high and au*au>high
    cold_lower=low-2*au*high**3
    assert cold_lower>0 and cold_lower**2-high**6>Fraction(1,200)
    # Common L=6 (last birth followed by six actual gates). Primary CL8/CT heat bounds.
    x=Fraction(2,55)
    L=6
    eta=Fraction(132,359)*x**L/(math.factorial(L)*(1-x*x)*(1-x/(L+1)))
    heat_diff=2*Fraction(4,3)*eta/(1-eta)
    feedback_floor=Fraction(4,200*2**20)
    assert heat_diff<Fraction(1,10**11) and feedback_floor-heat_diff>Fraction(19,10**9)
    return dict(delta_s_gt="1/200",heat_difference_lt=str(heat_diff),
                absolute_master_difference_gt="19/1000000000",true_Born_early_odds_ratio=1)


if __name__=="__main__":
    first,second=[model(w) for w in ["AACCCC","ACACCC"]]
    check=certified_contrast()
    assert first["B"]-second["B"] > 19e-9
    print(json.dumps(dict(result="PASS",models=[first,second],strict_causal_witness=check,
                    physical_price_binding_proved=False,GR_closed=False),indent=2))
