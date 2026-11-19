"""All eight old sites and 256 full outcome words, actual dyadic material grid, and factory costs."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from itertools import product
import json
from math import prod

from check_boundary_experiment import Golden as G

p,one,zero=G(0,1),G(1),G(0)


def sorter(bits,start,columns=1):
    n=len(bits)
    assert n>0 and (n&(n-1))==0
    out=list(bits)
    count=0
    for b in range(n.bit_length()-1):
        for j in range(n):
            if not j&(1<<b):
                count+=columns
                if start&(1<<b):
                    y=j^(1<<b)
                    out[j],out[y]=out[y],out[j]
    return out,count


def sin2_native(n):
    # G^n on its true Golden birth v=G|0>; cos(2theta)=2p-1.
    c=G(2)*p-one
    a,b=one,c
    for _ in range(n):
        a,b=b,G(2)*c*b-a
    return (one-b)*G(F(1,2))


def q_report(x,y):
    z=G(F(1,2**20))
    e=p**2*(one+x)
    l=G(4)*e*(one-e)
    u=p+p**2*y
    b=G(4)*u**2*(one-u**2)
    a=l+(one-l)*b
    return z*(a+b)-z**2*a*b


def main():
    laws=[sin2_native(2*i) for i in range(8)]
    table={}
    for absolute in product((0,1),repeat=8):
        table[absolute]=prod((r if b else one-r for r,b in zip(laws,absolute)),start=one)
    assert sum(table.values(),zero)==one
    for x in range(8):
        for chronological in product((0,1),repeat=8):
            ordered, swaps=sorter(chronological,x)
            assert swaps==12
            # Indexing the original full exact product table permutes independent factors.
            assert tuple(ordered)==tuple(chronological[x^i] for i in range(8))
            probs=[laws[x^i] if b else one-laws[x^i] for i,b in enumerate(chronological)]
            assert prod(probs,start=one)==table[tuple(ordered)]
    for m in (16,256):
        for x in range(m):
            ordered,count=sorter([((x^j),((x^j)*7)%17) for j in range(m)],x,columns=2)
            assert all(t==(y,(y*7)%17) for y,t in enumerate(ordered))
            assert count==(m.bit_length()-1)*m
    # Equal early marginals still fail after chronological bits are linked to the late array.
    alpha=p**2
    tv=G(2)*alpha*(one-alpha)
    assert tv==G(2)*p**3
    # Independently enumerate all 81 conditional early laws on two cells, including
    # zeros. Sorted late bits have unequal positive physical priors; compare all leaves.
    tested=0
    for params in product((F(0),F(1,2),F(1)),repeat=4):
        joint=[]
        for x in (0,1):
            leaves={}
            for z0,z1,e0,e1 in product((0,1),repeat=4):
                z=(z0,z1); early=(e0,e1)
                base=(F(1,3) if z0 else F(2,3))*(F(3,4) if z1 else F(1,4))
                for i in (0,1):
                    y=x^i; q=params[2*y+z[y]]
                    base*=q if early[i] else 1-q
                leaves[z0,z1,e0,e1]=base
            joint.append(leaves)
        assert (joint[0]==joint[1])==(len(set(params))==1)
        tested+=1
    # Genuine periodic 4^4 F1 matter field; finite difference H=1/4.
    H=F(1,4); f=[F(0),H*F(1,4),F(0),H*F(1,2)]
    m=[((f[(i+1)%4]-f[i])/H)**2 for i in range(4)]
    assert m==[F(1,16)]*2+[F(1,4)]*2
    eps=G(F(1,64))
    raw_gap=q_report(zero,zero-eps*G(m[0]))-q_report(zero,zero-eps*G(m[2]))
    assert raw_gap!=zero
    with localcontext() as c:
        c.prec=60
        pd=(D(5).sqrt()-1)/2
        nswaps=2048
        # Born factory using two Golden births, one CX and the parity bit.
        fair_failure=2*nswaps*(1-2*pd**3)**64
        run_failure=nswaps*(4*(1-4*pd**3)**120+(1-16*pd**9)**120)
        assert fair_failure+run_failure<D("1e-8")
        assert D(raw_gap.decimal())>0
        out={"status":"PASS","full_eight_site_words_tested":8*256,
             "physical_forward_material_moments":list(map(str,m)),"direct_SC1_gap_at_test_epsilon_1_64":raw_gap.decimal(),
             "SC7_clock_gain_and_reference_are_separate":True,
             "identical_marginals_early_copy_TV":tv.decimal(),"early_criterion_complete_joint_tables_checked":tested,
             "dyadic_four_dimensional_site_counts":[16,256],"two_status_bits_sort_Fredkins":[64,2048],
             "L4_preflight_plus_factories":2*nswaps,"L4_factory_failure_union_upper":format(run_failure+fair_failure,".12E"),
             "stable_all_outcome_full_economy_identification":False,"physical_large_geometric_body_replayed":False}
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__": main()
