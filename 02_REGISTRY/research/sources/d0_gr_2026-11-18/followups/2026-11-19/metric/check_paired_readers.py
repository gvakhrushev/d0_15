"""Address-resolved marginals, physical golden words and the complete two-record law."""
import json
from decimal import Decimal as D, localcontext
from itertools import product

from check_heat_history import A, ONE, P, ZERO, const

G = ((A,-P),(P,A))
INV = ((A,P),(-P,A))
LAMBDA = const(4)*P**3


def add(entries, key, value):
    entries[key] = entries.get(key, ZERO)+value


def clean(entries):
    return {k:v for k,v in entries.items() if v != ZERO}


def birth(psi, bit):
    out = {}
    for old,z in psi.items():
        out[old] = z*A
        out[old | 1<<bit] = z*P
    return out


def turn(psi, bit, op=G):
    out = {}
    mask = 1<<bit
    for old,z in psi.items():
        j = (old>>bit)&1
        for i in range(2):
            add(out,(old & ~mask)|(i<<bit),op[i][j]*z)
    return clean(out)


def cx(psi, control, target):
    return {old ^ (1<<target) if old & (1<<control) else old:z for old,z in psi.items()}


def partial(psi, bits):
    mask = sum(1<<i for i in bits)
    env = {}
    for old,z in psi.items():
        local = sum(((old>>bit)&1)<<i for i,bit in enumerate(bits))
        env.setdefault(old & ~mask,[]).append((local,z))
    out = {}
    for same in env.values():
        for i,z in same:
            for j,w in same:
                add(out,(i,j),z*w)
    return clean(out)


def final_law(psi):
    out = [ZERO]*4
    for index,z in psi.items():
        r1,t1,r2,t2 = [(index>>i)&1 for i in (4,5,6,7)]
        assert not (r1 and t1) and not (r2 and t2)
        out[2*r1+r2] = out[2*r1+r2]+z*z
    assert sum(out,ZERO)==ONE
    return tuple(out)


def experiment(t,i,j,shadows=True):
    # T is a genuinely earlier printed old label; the calculation is conditional.
    psi = {0:ONE}
    for h in (0,1):
        psi = birth(psi,h)
        if t: psi = {x^(1<<h):z for x,z in psi.items()}
        psi = turn(psi,h)
        if t: psi = {x^(1<<h):z for x,z in psi.items()}
    for h,shadow in ((0,2),(1,3)):
        psi = turn(birth(psi,shadow),shadow,INV)
        if shadows: psi = cx(psi,h,shadow)
    stages = []
    for h,r,tail in ((i,4,5),(j,6,7)):
        bits = [h]
        snapshots = [partial(psi,bits)]
        for control,target in ((h,r),(r,tail)):
            psi = birth(psi,target)
            bits.append(target)
            snapshots.append(partial(psi,bits))
            psi = cx(psi,control,target)
            snapshots.append(partial(psi,bits))
            psi = turn(psi,target)
            snapshots.append(partial(psi,bits))
            psi = cx(psi,control,target)
            snapshots.append(partial(psi,bits))
        stages.append(snapshots)
    return stages,final_law(psi),psi


def dec(z, a):
    return sum(D(c)*a**i for i,c in enumerate(z.c))


def check():
    for t in (0,1):
        runs = {(i,j):experiment(t,i,j) for i,j in product(range(2),repeat=2)}
        b = ONE-LAMBDA if t==0 else ONE
        y = b*LAMBDA
        joint = b*LAMBDA**2
        shared = (ONE-y-y+joint,y-joint,y-joint,joint)
        distinct = ((ONE-y)**2,y*(ONE-y),y*(ONE-y),y*y)
        for (i,j),(stages,law,_) in runs.items():
            assert law == (shared if i==j else distinct)
            assert stages[0]==runs[i,1-j][0][0]
            assert stages[1]==runs[1-i,j][0][1]
            # Include the complete local quantum state after the reader's own LC1.
            # Its outcome CP map is fixed; matching pre-commit states also match that output.
            assert len(stages[0])==len(stages[1])==9
        if t==0:
            for i in (0,1):
                used = experiment(t,i,i,False)[0][1][0]
                unused = experiment(t,1-i,i,False)[0][1][0]
                assert unused[0,1] != ZERO and used[0,1]==P**3*unused[0,1]
        # If both shadow values are genuinely committed, residual conditional entropy adds
        # one single-reader term for each selected seed. Check the actual full joint masses.
        for (i,j),(_,_,psi) in runs.items():
            measured = {}
            for index,z in psi.items():
                label = tuple((index>>pos)&1 for pos in (2,3,4,6))
                add(measured,label,z*z)
            for a0,a1,r0,r1 in product(range(2),repeat=4):
                hs = (a0,a1)
                expected = (b if a0==0 else ONE-b)*(b if a1==0 else ONE-b)
                for r,control in ((r0,i),(r1,j)):
                    y_cond = LAMBDA if not hs[control] else ZERO
                    expected = expected*(y_cond if r else ONE-y_cond)
                assert measured.get((a0,a1,r0,r1),ZERO)==expected
    with localcontext() as ctx:
        ctx.prec=48
        phi=(D(1)+D(5).sqrt())/2
        a=(1/phi).sqrt()
        ell=phi.ln()
        lam=dec(LAMBDA,a)
        b=1-lam
        y=b*lam
        row=(1-2*y+b*lam**2,y-b*lam**2,y-b*lam**2,b*lam**2)
        ref=((1-y)**2,y*(1-y),y*(1-y),y*y)
        mutual=sum(x*(x/z).ln() for x,z in zip(row,ref))
        gain=mutual/ell
        d=b*(1-b)*lam**2
        assert D('.3636')<gain<D('.3637') and 6*d < gain < 8*d
        return dict(arithmetic="exact Z[a], a^4+a^2=1 on all amplitudes and marginals",
                    controls=["00","01","10","11"],old_registered_T_values=[0,1],
                    exact_all_conditional_output_laws_and_invalid_zero=True,
                    exact_local_density_checks_per_reader_per_program=9,
                    dimensions=dict(new_wires=8,full_new_output=256),
                    shadow_test="unread purifications retained; registering both removes all contrasts in conditional entropy",
                    no_shadow_offdiagonal_retention="p^3",lambda_report=str(+lam),
                    shared_pair_T0=[str(+v) for v in row],independent_pair_T0=[str(+v) for v in ref],
                    mutual_information_nats=str(+mutual),price_gain_over_one_minus_q=str(+gain),
                    extra_both_one_over_one_minus_q=str(+d),
                    extra_four_mismatch_net_over_one_minus_q=str(+(gain-8*d)),
                    intrinsic_unknown_two_reader_work_unbounded=True,full_CD13=False)


if __name__ == "__main__":
    print(json.dumps(check(),indent=2,sort_keys=True))
