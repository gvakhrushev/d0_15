"""One-copy, LEFT-only positive difference measurement on the actual real Fourier128 frame."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
import json
import math


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def character(k, x):
    return (1, 1j, -1, -1j)[dot(k,x) % 4]


def original_frame():
    unit = [tuple(int(i==j) for j in range(4)) for i in range(4)]
    stencil = unit + [tuple(x-y for x,y in zip(unit[j],unit[i])) for j in range(4) for i in range(j)]
    paired = {}
    for k in product(range(4), repeat=4):
        neg = tuple(-x % 4 for x in k)
        if k < neg:
            paired[k] = neg
    ordered = sorted(paired, key=lambda k: (-sum(character(k,s).real for s in stencil), k))[:64]
    require([int(sum(character(k,s).real for k in ordered)) for s in stencil] ==
            [20,10,10,9,8,8,6,9,5,5], 'wrong primary Fourier frame or tie rule')
    return [f for k in ordered for f in (k, paired[k])]


def walsh_row(axis, tag, node):
    # CX(tau, low-axis): the target becomes d; measure it as the given tag.
    tau, *space = node
    d = (space[axis] & 1) ^ tau
    if d != tag:
        return 0
    # On the other six free bits, measure the specified Hadamard outcome.
    exponent = (space[axis] >> 1) + sum(x for j,x in enumerate(space) if j != axis) + d*tau
    return (-1) ** (exponent % 2)


def edge_filter():
    frame = original_frame()
    groups = defaultdict(list)
    for k in frame:
        groups[k[1:]].append(k[0])
    histogram = Counter(len(v) for v in groups.values())
    histogram[0] = 64-len(groups)
    require(histogram == {0:9, 1:6, 2:29, 3:16, 4:4}, 'transverse multiplicities')
    for b, us in groups.items():
        if len(us)>1:
            # These two columns span the entire complex temporal doublet.
            require(character((us[0],),(1,)) != character((us[1],),(1,)), 'dark rank')
    singles = sorted([list(b)+u for b,u in groups.items() if len(u)==1])
    nodes = list(product(range(2),range(4),range(4),range(4)))
    coeffs = [[walsh_row(j,t,x) for x in nodes] for j,t in product(range(3),range(2))]
    require(all(dot(a,b)==(64 if i==j else 0) for i,a in enumerate(coeffs)
                for j,b in enumerate(coeffs)), 'six physical orthogonal real projectors')
    # The two possible active amplitudes s,t have norm contribution A*s+B*t.
    # Integer real/imaginary sums over the complete 128 dimensional purifying reference.
    spectra = []
    for row in coeffs:
        channels = []
        for k in frame:
            z = [sum(c*character(k,x) for c,x in zip(row,nodes) if x[0]==t) for t in (0,1)]
            require(z[0]+z[1]==0, 'a common amplitude fired on the native reference')
            channels.append(z)
        spectra.append(channels)

    # Include the row normalization 1/8 and the original 1/sqrt(128) frame.
    energy_scale = F(sum(int(v[0].real)**2+int(v[0].imag)**2 for bins in spectra for v in bins),64*128)
    require(energy_scale == F(3,2),'wrong absolute mass')
    for i, bins in enumerate(spectra):
        a = i//2
        active = [k for k,z in zip(frame,bins) if z[0]]
        expect = sorted(k for k in frame if k[0]==k[a+1] and
                        k[0] % 2 and all(x==2 for j,x in enumerate(k[1:]) if j != a))
        require(sorted(active)==expect and len(active)==2,'one conjugate pair per real row')
    def mass(left,right):
        value=F(0)
        for s,t in zip(left,right):
            for bins in spectra:
                for za,zb in bins:
                    a,b = (int(za.real)*s+int(zb.real)*t, int(za.imag)*s+int(zb.imag)*t)
                    value+=(a*a+b*b)/(64*128)
        return value
    for left,right in [((F(1,4),F(-1,9)),(F(-1,6),F(1,8))),
                       ((F(1),F(0)),(F(0),F(1))),((F(1),F(0)),(F(-1),F(0)))]:
        require(mass(left,right)==energy_scale*sum((x-y)**2 for x,y in zip(left,right)), 'two-mask Born mass')
    h, S=F(1,16),16**4
    local = [energy_scale/S*(h*k)**2 for k in (F(1,16),F(1,8))]
    require(local[1]==4*local[0], 'A88 supplied affine profiles')
    # For the native G712 input: quarter- and half-turn on the second slice only.
    physical = [mass((F(1),F(0)),x)/S for x in ((F(0),F(1)),(F(-1),F(0)))]
    require(physical==[F(3,S),F(6,S)],'physical reports after factoring out A_*^2')
    return dict(frequencies=len(frame), transverse_multiplicities={str(k):v for k,v in sorted(histogram.items())},
                singletons_b_then_k0=singles, active_real_projector_rank_per_CAR_mask=6,
                old_RIGHT_acted_on=False, local_edge_mass_times_S=str(energy_scale)+' times squared difference',
                affine_probabilities_L16=[str(x) for x in local],
                G712_quarter_and_half_probabilities_divided_by_Astar_squared_L16=[str(x) for x in physical])


def main():
    out=edge_filter()
    p=(math.sqrt(5)-1)/2
    amp=p*math.sin(712*math.asin(p))
    require(0<amp<p,'nonzero native carrier (analytic certificate is in the cited SC1 owner)')
    q0,q1=(k*amp**2/(16**4) for k in (3,6))
    overlap=1-64*amp**2/(16**4)
    # Stable form of 1-sum sqrt(P0 P1) for the classical two-result journal.
    lost=((math.sqrt(q1)-math.sqrt(q0))**2+
          ((q1-q0)/(math.sqrt(1-q0)+math.sqrt(1-q1)))**2)/2
    c=overlap*lost
    epsilon_lower=(c/(math.sqrt(1+c)+1))**2
    require(overlap>p and epsilon_lower>0,'complete pure input cannot return at both settings')
    out.update(physical_ratio=2,whole_joint_return_for_both_inputs=False,
               full_collar_exterior_block_preserved_on_supply=True,
               complete_global_H1_native_task_selected=False,GR_closed=False)
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
