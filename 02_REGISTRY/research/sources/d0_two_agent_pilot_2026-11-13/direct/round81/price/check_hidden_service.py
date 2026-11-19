"""Full RAW/conditional entropy of the finite paid return and a native service tag."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from math import asin, isclose, log, sin, sqrt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'round80' / 'price'))
from check_parity_price import action, ne, p, p3, ap, one

PHI = (1+sqrt(5))/2


def entropy(masses):
    return -sum(float(q)*log(float(q), PHI) for q in masses if q)


def binary(q):
    return entropy((q,1-q))


def tag_word_test():
    port, first, second, tag = 2,3,4,5
    gate=ne.Gate
    cx=lambda ctrl,tgt: gate('CX',(ctrl,tgt))
    route=(cx(port,tag),cx(tag,port),cx(port,tag))
    z=route+(gate('SourceI',(port,0,1)),)*2+route
    parity=cx(first,second)
    w=(parity,gate('G',(tag,)),cx(second,tag),gate('G',(tag,)),cx(second,tag),parity)
    quiet, active = w+z+w+z, w+w+z+z
    assert Counter(quiet)==Counter(active) and len(active)==28
    for gates, split in [(quiet,False),(active,True)]:
        ex=ne.Execution(6,(),(),gates,profile=ne.G_CX_SOURCE_I,source_port=port,
                        source_spin=(0,1),report_bits=(first,second,tag))
        ne.execution_from_json(ne.canonical_json(ex),max_qubits=6,max_expanded_stages=28)
        for col in range(64):
            state={col:one}
            for g in gates:
                state=action(state,g,6)
            even=(((col>>2)^(col>>1)) & 1)==0
            if split and even:
                sine=4*ap*p3
                cosine=p3*p3-4*p3
                expected={col:cosine,col^1:(-sine if col&1 else sine)}
                assert sine*sine == 16*p3*p3*p3
            else:
                expected={col:one}
            assert state==expected


def enumerate_paths(u, eta, m, N, prepare_b, r=F(0)):
    def request(sector, previous, position, preparing, macro, raw, mass, calls):
        # previous counts 00 outcomes of this single measurement request.
        for output in ('0','1','P','B'):
            erasure = output in ('0','1')  # two microscopic refinements of the genuine 00
            if erasure:
                prob = (1-eta)*(r if output=='1' else 1-r)
            else:
                prob = eta*(u if output==sector else 1-u)
            if not prob:
                continue
            branch_mass, record = mass*prob, raw+output
            if erasure:
                if previous+1==N:
                    yield macro+'!',record,branch_mass,calls
                else:
                    yield from request(sector,previous+1,position,preparing,macro,record,branch_mass,calls)
                continue
            report = macro+output
            if preparing and output=='B':
                yield from request('B',0,0,False,report,record,branch_mass,calls+1)
            elif preparing or output==('B' if prepare_b else 'P') or position==m:
                yield report,record,branch_mass,calls
            else:
                yield from request(output,0,position+1,False,report,record,branch_mass,calls+1)
    return list(request('P',0,0,prepare_b,'','',F(1),1))


def test_tree(u, eta, m, N, prepare_b, r):
    rows=enumerate_paths(u,eta,m,N,prepare_b,r)
    assert sum(q for _,_,q,_ in rows)==1
    assert len(rows)==len({raw for _,raw,_,_ in rows})
    delta=1-eta
    e=1-delta**N
    A=1+(1-u)*e*sum((e*u)**j for j in range(m))
    if prepare_b:
        A=1+e*(1-u)*A
    macro=defaultdict(F)
    untagged=defaultdict(F)
    for address,raw,q,_ in rows:
        macro[address]+=q
        untagged[raw.replace('1','0')]+=q
    calls=sum(q*k for _,_,q,k in rows)
    attempts=sum(q*len(raw) for _,raw,q,_ in rows)
    erasures=sum(q*(raw.count('0')+raw.count('1')) for _,raw,q,_ in rows)
    valid=sum(q*(raw.count('P')+raw.count('B')) for _,raw,q,_ in rows)
    ones=sum(q*raw.count('1') for _,raw,q,_ in rows)
    assert (calls,attempts,erasures,valid,ones)==(A,A*e/eta,A*delta*e/eta,A*e,erasures*r)
    full_H=entropy(q for _,_,q,_ in rows)
    macro_H=entropy(macro.values())
    unt_H=entropy(untagged.values())
    service_H=entropy(eta*delta**k/e for k in range(N))
    near=lambda x,y: isclose(float(x),float(y),abs_tol=3e-12,rel_tol=1e-12)
    assert near(unt_H-macro_H,valid*service_H)
    assert near(full_H-unt_H,erasures*binary(r))
    assert near(unt_H,attempts*(binary(eta)+eta*binary(u)))
    raw_length=2*erasures+3*valid
    lambda_eta=1+(2-binary(eta))/eta
    assert lambda_eta>=2-1e-13
    assert near(raw_length-unt_H,A*e*(lambda_eta-binary(u)))
    return len(rows)


def main():
    tag_word_test()
    leaves=0
    for u,eta in [(F(1,5),F(3,4)),(F(2,7),F(4,9)),(F(1,8),F(1))]:
        for m,N in [(0,1),(1,2),(2,3)]:
            for prepare_b in (False,True):
                for r in [F(0),F(1,3)]:
                    leaves+=test_tree(u,eta,m,N,prepare_b,r)
    pg=1/PHI
    eta=sin(16*asin(pg))**2
    r=16*pg**9
    assert abs((1+(2-binary(eta))/eta)-2.44285120425724)<1e-12
    assert abs(r-binary(r)+0.8589040446103161)<1e-12
    print(f'64 exact native columns per mark ordering; {leaves} stopped leaves, 36 trees')
    print('native eta =',eta,'service entropy per R =',binary(eta)/eta,
          'raw lambda =',1+(2-binary(eta))/eta)
    print('native mark r =',r,'entropy =',binary(r),'excess one-bit price =',r-binary(r))


if __name__=='__main__':
    main()
