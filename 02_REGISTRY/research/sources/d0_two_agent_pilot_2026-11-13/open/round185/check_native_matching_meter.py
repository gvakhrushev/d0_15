"""Compile and test simultaneous signed matching probes on supplied amplitudes."""

from collections import defaultdict
from functools import lru_cache
from itertools import product
import json
import sympy as sp
from math import comb
from pathlib import Path
import sys

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "direct/round80/price"))
sys.path.insert(0, str(PILOT / "open/round181"))
sys.path.insert(0, str(PILOT / "direct/round88/assembly"))
from check_h1_price_residual import pairs, eta, eye, generators, shift
from check_parity_price import action
from check_fixed_positive_reader import a, cx, nc1, ne, one, p, power, require


ADDRESS = (0, 1)
H, PORT, SPIN0, SPIN1, FLAG, ONE, WORK, TAIL = range(2, 10)
WIDTH = 10


def logical_ccx(a, b, target):
    # Its successful native factory must implement this all-column map.
    return ne.Gate("Toffoli", (a,b,target))


def matches(controls, target):
    """Toggle target on a conjunction of at most three literal controls."""
    invert = tuple(cx(ONE,wire) for wire, bit in controls if bit == 0)
    wires = [wire for wire, _ in controls]
    if len(wires) == 2:
        body = (logical_ccx(*wires,target),)
    else:
        require(len(wires) == 3, "The fixture lowers three-control operations")
        compute = logical_ccx(wires[0],wires[1],WORK)
        body = (compute,logical_ccx(WORK,wires[2],target),compute)
    return invert+body+invert[::-1]


def bits(value):
    return tuple((value >> (1-i)) & 1 for i in range(2))


def controlled_swap_pair(i, j):
    x, y = bits(i), bits(j)
    different = [wire for wire in ADDRESS if x[wire] != y[wire]]
    pivot = different[0]
    separate = tuple(cx(pivot,wire) for wire in different[1:])
    # Both separated words agree on every coordinate except pivot.
    anchor = list(x)
    for wire in different[1:]:
        anchor[wire] ^= x[pivot]
    controls = [(H,1)] + [(wire,anchor[wire]) for wire in ADDRESS if wire != pivot]
    return separate+matches(controls,pivot)+separate[::-1]


def phase_for_addresses(addresses):
    word = tuple(g for index in addresses
                 for g in matches([(H,1)]+list(zip(ADDRESS,bits(index))),FLAG))
    si = ne.Gate("SourceI",(PORT,SPIN0,SPIN1))
    effect = (si,si,cx(FLAG,PORT),si,si,cx(FLAG,PORT))
    return word+effect+word[::-1]


def body(kind, entries, reverse):
    negative = []
    swaps = []
    for i, j, sign in entries:
        if kind == "diagonal":
            if sign == (1 if reverse else -1):
                negative.append(i)
        else:
            swaps.extend(controlled_swap_pair(i,j))
            if sign == (1 if reverse else -1):
                negative.extend((i,j))
    return phase_for_addresses(negative)+tuple(swaps)


def local_action(state, g):
    if g.op != "Toffoli":
        return action(state,g,WIDTH)
    c0,c1,target = (1<<(WIDTH-1-wire) for wire in g.wires)
    return {(index^target if index & c0 and index & c1 else index):amp
            for index,amp in state.items()}


def overlap(x,y):
    return sum((v*y.get(i,0) for i,v in x.items()),one*0)


def fixed_state(address, old, h=0):
    return (address<<8) | (h<<7) | (old<<4) | 4


@lru_cache(None)
def effects(kind, entries, reverse):
    word = body(kind,entries,reverse)
    lookup = {i:j for i,j,_ in entries} | {j:i for i,j,_ in entries}
    sign = {i:s for i,j,s in entries} | {j:s for i,j,s in entries}
    for x,old,h in product(range(4),range(8),range(2)):
        state = {fixed_state(x,old,h):one}
        for g in word:
            state = local_action(state,g)
        if not h:
            target, coefficient = x, one
        elif kind == "diagonal":
            target = x
            coefficient = -one if sign.get(x) == (1 if reverse else -1) else one
        else:
            target = lookup.get(x,x)
            coefficient = (-sign[x] if reverse else sign[x])*one if x in sign else one
        require(state == {fixed_state(target,old,h):coefficient},
                "Controlled involution must preserve old PORT and Spin and clear both scratch bits")

    full = word+(cx(ONE,H),ne.Gate("G",(H,)),cx(ONE,H))+nc1(H,TAIL)
    columns = []
    for x in range(4):
        root = fixed_state(x,0)
        state = {root:a*a,root+1:a*p,root+(1<<7):p*a,root+(1<<7)+1:p*p}
        for g in full:
            state = local_action(state,g)
        columns.append({j:value for j,value in state.items() if (j>>7)&1})
    return tuple(tuple(overlap(x,y) for y in columns) for x in columns)


def sparse_layers(table, coefficient_index):
    """Disjoint diagonal layer plus greedily colored off-diagonal layers."""
    buckets = []
    diag = []
    for i,j,*coeffs in table:
        weight = coeffs[coefficient_index]
        if weight == 0:
            continue
        if i == j:
            diag.append((i,j,weight))
            continue
        for used, group in buckets:
            if not used.intersection((i,j)):
                used.update((i,j))
                group.append((i,j,weight))
                break
        else:
            buckets.append(({i,j},[(i,j,weight)]))
    groups = [("diagonal",diag)] if diag else []
    groups.extend(("offdiag",group) for _, group in buckets)
    for kind, group in groups:
        for threshold in range(1,1+max(abs(w) for _,_,w in group)):
            yield kind,tuple((i,j,1 if w>0 else -1) for i,j,w in group if abs(w)>=threshold)


def sparse_audit():
    # Entries (i,j,a,b) denote A_ij=a+p b, with a symmetric completion.
    table = [(0,0,0,-2),(1,1,1,0),(3,3,-2,1),(0,1,2,-1),
             (2,3,-1,1),(0,2,3,0),(1,3,-2,0),(0,3,0,-1)]
    target = defaultdict(lambda:one*0)
    for i,j,c,d in table:
        target[i,j]=target[j,i]=c*one+d*p
    observed = defaultdict(lambda:one*0)
    layers = [tuple(sparse_layers(table,k)) for k in (0,1)]
    mult = (one,p)
    for k in (0,1):
        for kind, entries in layers[k]:
            positive = effects(kind,entries,True)
            negative = effects(kind,entries,False)
            for i,j in product(range(4),repeat=2):
                observed[i,j] += mult[k]*(positive[i][j]-negative[i][j])
    gamma = 4*power(p,3)
    for i,j in product(range(4),repeat=2):
        require(observed[i,j] == gamma*target[i,j], "Wrong sparse matrix element")
    slots = 2*sum(map(len,layers))
    depth = 1
    while comb(2*depth,depth) < slots:
        depth += 1
    require(1 <= depth and slots <= comb(2*depth,depth), "Failed physical atom allocation")
    return {"matrix_dimension":4,"integer_layers":len(layers[0]),"p_layers":len(layers[1]),
            "distinct_controller_atoms_used":slots,"golden_selector_births":2*depth,
            "signal_multiplier":"4 p^(3 + 3 b) with A integral over Z[p]",
            "native_probe_CX_G_SourceI_replayed":True,
            "logical_Toffoli_factories_replaced_by_exact_success_action_in_fixture":True,
            "actual_old_port_spin_columns_per_involution":64,
            "full_H1_paid_layout_materialized":False,"GR_closed":False}


def original_compensated_secants():
    lam, t, h, x, y = sp.symbols("lambda t h x y", real=True)
    e0, e1 = sp.Rational(1,256), sp.Rational(4,256)
    base = (0,0,x,y)

    def H(z):
        return -lam*(e0+e1)*(z[2]**2+z[3]**2)/2

    def link(z, axis, sign=1):
        if axis != 0:
            return eye
        later = shift(z,0,h)
        K = sp.zeros(4)
        for j, generator in zip((2,3),generators):
            K += (H(later)-H(shift(later,j,-h)))*generator/2
        return eye+sign*K+K*K/2

    null = H(base)/2
    coframe = eye.copy()
    coframe[1,0] = null
    shear = eye.copy()
    shear[0,1] = t
    varied = coframe*shear
    require(varied.det() == 1, "The compensated shear preserves the exact volume")
    inv = varied.inv()
    guu = sp.expand((inv*eta*inv.T)[0,0])
    require(guu == sp.expand(-2*t*(1+null*t)), "Exact finite metric entry")
    gravity = 0
    for first,second in pairs:
        other = [j for j in range(4) if j not in (first,second)]
        third,fourth = other
        loop = (link(base,first)*link(shift(base,first,h),second)
                *link(shift(base,second,h),first,-1)*link(base,second,-1))
        curvature = ((loop-eta*loop.T*eta)*eta/2).applyfunc(sp.expand)
        for a,b in pairs:
            c,d = [j for j in range(4) if j not in (a,b)]
            wedge = varied[a,third]*varied[b,fourth]-varied[b,third]*varied[a,fourth]
            gravity += (sp.LeviCivita(first,second,third,fourth) *
                        sp.LeviCivita(a,b,c,d)*wedge*curvature[c,d]/h**2)

    def slope(A):
        return sp.cancel((A.expand()-A.expand().subs(t,-t))/(2*t))

    require(slope(gravity) == lam*(e0+e1), "All six original ordered plaquettes")
    answers = [slope(gravity+lam*e*guu) for e in (e0,e1)]
    require(answers == [3*lam/256,-3*lam/256], "The exact finite CAR secants")
    return {"original_EPS_PLUS_secants":[str(v) for v in answers],
            "compensated_coframe_determinant":"1", "ordered_faces":6,
            "symbolic_finite_t_without_Taylor_remainder":True}


def reciprocal_support_test():
    p_sym = (sp.sqrt(5)-1)/2
    h = sp.symbols("h", positive=True)
    alpha = (h/16,h/8)
    for i,j in product(range(2),repeat=2):
        before = sp.Matrix([alpha[i],sp.sqrt(p_sym)])
        observed = (sp.Matrix([[1,-1]]) * sp.diag(1,alpha[j])
                    * sp.diag(p_sym,sp.sqrt(p_sym)) * before)[0]/sp.sqrt(2)
        require(sp.simplify(observed-p_sym*(alpha[i]-alpha[j])/sp.sqrt(2)) == 0,
                "Wrong coherent support for the calibrated physical comparison")
    return {"equal_profile_click":"exact zero", "opposite_profile_amplitude":"+-p*h/(16 sqrt(2))"}


if __name__=="__main__":
    result = {"sparse_logical_readout":sparse_audit(),
              "actual_mathematical_H1_path":original_compensated_secants(),
              "reciprocal_support":reciprocal_support_test(),
              "native_actuator_on_full_H1_price_verified":False,
              "GR_closed":False}
    print(json.dumps(result,indent=2))
