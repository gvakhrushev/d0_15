"""Exact leaf maxima with real aborts, strict H.1 bounds, native angle certificates."""
from fractions import Fraction as F
from pathlib import Path
import sys

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[4] /
                      'd0_native_readiness_amplification_2026-10-24'))
from native_phase import native_rotation_intervals


def leaves(u, eta, m, J, prepare_b):
    target = 'B' if prepare_b else 'P'
    def visit(current, remaining, prep, prefix, mass):
        delta=1-eta
        yield prefix+'0'*J, mass*delta**J
        for zeros in range(J):
            for sector in ('P','B'):
                branch=mass*delta**zeros*eta*(u if sector==current else 1-u)
                word=prefix+'0'*zeros+sector
                if prep and sector=='B':
                    yield from visit('B',m+1,False,word,branch)
                elif prep or sector==target or remaining==1:
                    yield word,branch
                else:
                    yield from visit(sector,remaining-1,False,word,branch)
    return dict(visit('P',m+1,prepare_b,'',F(1)))


def find_modes():
    count=0
    for u in (F(1,14),F(2,7),F(4,9)):
        for eta in (F(1,3),F(4,5),F(19,20)):
            a,b=eta*u,eta*(1-u)
            for m in (1,2,3):
                for J in (1,2,3):
                    for prepare_b in (False,True):
                        values=leaves(u,eta,m,J,prepare_b)
                        assert sum(values.values())==1
                        peak=b**(3 if prepare_b else 2)
                        champion='BPB' if prepare_b else 'BP'
                        assert values[champion]==peak
                        assert values['P']==a and values['0'*J]==(1-eta)**J
                        assert max(values.values())==max(a,peak,(1-eta)**J)
                        others=[q for w,q in values.items() if w!=champion]
                        assert max(others)<=max(a,(1-eta)**J,peak*max(a,1-eta))
                        if prepare_b:
                            prefix = 'B'+'P'*m
                            hit, overflow = prefix+'B', prefix+'P'
                            assert values[hit] == b**3*a**(m-1)
                            assert values[overflow] == b**2*a**m
                            assert values[hit]/values[overflow] == (1-u)/u
                            assert len(hit)==len(overflow)==m+2
                        count+=1
    return count


def rational_endpoints(symbolic):
    return tuple(F(int(x.p),int(x.q)) for x in symbolic)


def physical_bounds():
    _, sine=native_rotation_intervals(1,bits=112)
    plo,phi=rational_endpoints(sine)  # real Golden p = sin(theta)
    _, sine=native_rotation_intervals(16,bits=112)
    slo,shi=rational_endpoints(sine)
    assert shi<0
    elo,ehi=shi**2,slo**2
    qlo,qhi=20316969*plo**38,20316969*phi**37
    assert 0<qlo<qhi<F(1,2)
    lo,hi=(1-2*qhi)**2,(1-2*qlo)**2
    # Outward bounds hold simultaneously over the physical interval.
    amin,amax=elo*lo,ehi*hi
    bmin,bmax=elo*(1-hi),ehi*(1-lo)
    dmax=1-elo
    gap=bmin**3-amax
    assert gap>F('0.00224786')
    assert bmin**3-dmax>F('.14894794')
    assert bmin**3*(1-max(amax,dmax))>F('.19177216')
    assert bmin**3/amax>F('1.0088064')
    assert F('1.0088064')**5000 > F('1.618034')**91
    assert 1/plo<F('1.618034')  # log_phi(b^3/a)>91/5000
    assert amin-phi**5*bmax**3>F('.00190905')
    assert phi**5*bmax**3<F('.05282036') and amin>F('.05472939')
    rough=(1-2*F('.23'))**2
    assert ehi**3*(1-rough)**3-elo*rough < F('-.00810')
    # The sufficient efficiency 8/9 is independent of field and cap.
    bound=F(8,9)
    assert bound**2*(1-hi)**3>hi
    assert bound**3*(1-hi)**3>1-bound
    return float(lo),float(hi),float(elo),float(gap)


def certificate_examples():
    examples={}
    for width in [1,2,3,4,5,6,7,8,16,32,64,128]:
        for k in range(1,100):
            c,_=native_rotation_intervals(2**width*k,bits=4*width+112)
            if 3*max(abs(c[0]),abs(c[1]))<1:
                examples[width]=k
                break
        assert width in examples
    return examples


if __name__=='__main__':
    print('exact finite trees:',find_modes())
    print('enclosed u_low, u_high, eta, lower modal gap:',physical_bounds())
    print('predicate width and certified k:',certificate_examples())
