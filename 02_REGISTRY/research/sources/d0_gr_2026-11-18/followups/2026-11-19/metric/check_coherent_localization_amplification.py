"""Exact two-plane amplification of full coherent source+address readiness."""
from fractions import Fraction
from math import comb
from itertools import product
import json
import mpmath as mp
from mpmath import iv
import sympy as sp
from check_fourier_fresh_localization import original_reference,global_choi_labels


def grover_rational(a,k):
    # Coefficients relative to sin(theta) and cos(theta), respectively.
    g=b=Fraction(1)
    for _ in range(k):
        g,b=(1-2*a)*g+2*(1-a)*b, -2*a*g+(1-2*a)*b
    success=a*g*g
    failure=(1-a)*b*b
    assert success+failure==1
    return success,failure,g,b


def nearest_k(a):
    mp.mp.dps=100
    val=mp.mpf(a.numerator)/a.denominator
    theta=mp.asin(mp.sqrt(val))
    x=mp.pi/(4*theta)-mp.mpf(1)/2
    k=max(0,int(mp.floor(x+mp.mpf(1)/2)))
    success,*_=grover_rational(a,k)
    # This exact rational certificate proves the advertised elementary bound
    # without relying on numerical angle rounding.
    assert success>=1-a
    return k,success


def to_iv(frac):
    return iv.mpf(frac.numerator)/frac.denominator


def two_plane_and_oldright():
    # Arbitrary T/reference state; two test sites share one X and carry no
    # address information to the measured yes/no flag.
    a=sp.Rational(1,4); u=sp.sqrt(a);v=sp.sqrt(1-a)
    C=sp.Matrix([u,v]); RP=sp.diag(-1,1)
    RC=sp.eye(2)-2*C*C.T
    Q=-RC*RP
    assert Q.T*Q==sp.eye(2)
    got=sp.simplify(Q**1*C)
    assert sp.simplify(got[0]-sp.sin(3*sp.pi/6))==0
    # Distinct conditional isometries: kept X controls output m_x.
    m0=sp.Matrix([1,0]);m1=sp.Matrix([sp.Rational(3,5),sp.Rational(4,5)])
    V=sp.zeros(4,2)
    V[0,0]=m0[0];V[1,0]=m0[1]
    V[2,1]=m1[0];V[3,1]=m1[1]
    assert V.T*V==sp.eye(2)
    # The amplitude is a scalar I on X tensor arbitrary old RIGHT.
    K=sp.Rational(1,2)*sp.kronecker_product(V,sp.eye(2))
    assert K.T*K==sp.eye(4)/4
    # New data can reduce the X/RIGHT marginal coherence; it is retained.
    return True


def main():
    pairs,outside,S=original_reference()
    s,A,count=global_choi_labels(4)
    assert S==s==count==256 and A==2049 and len(pairs)==64
    assert two_plane_and_oldright()
    tests=[]
    iv.dps=60
    for S in (256,4096,65536):
        A=8*S+1
        af=Fraction(1,S);aj=Fraction(21,A)
        kf,pf=nearest_k(af);kj,pj=nearest_k(aj)
        ready=to_iv(pf)**80 * to_iv(pj)**180
        lower=to_iv(1-af)**80*to_iv(1-aj)**180
        assert ready>=lower
        queries=80*(2*kf+1)+180*(2*kj+1)
        tests.append(dict(S=S,k_fourier=kf,k_choi=kj,
            per_fourier_success=str(to_iv(pf)),per_choi_success=str(to_iv(pj)),
            bank_all_success=str(ready),universal_lower_bound=str(lower),
            U_and_Uadjoint_calls=queries))
    assert tests[0]['k_fourier']==12 and tests[0]['k_choi']==7
    assert tests[0]['U_and_Uadjoint_calls']==4700
    # Explicit complete coherent raw seed with independent, fixed readiness.
    S=256
    af=Fraction(1,4*S);aj=Fraction(21,9*(8*S+1))
    kf,pf=nearest_k(af);kj,pj=nearest_k(aj)
    assert (kf,kj)==(25,23)
    ready=to_iv(pf)**80*to_iv(pj)**180
    assert ready>iv.mpf('.9170') and ready<iv.mpf('.9171')
    # Unverified equality oracle sketch using XORs + clean AND chain:
    # n=4ell bits, +e_mu requires reversible increment scratch.
    ell=2;n=4*ell
    nof=2*(n-1)+4*(ell-2)
    ncx=8*n+4*ell+6
    assert nof==14 and ncx==78
    # Gate-factory flags may be measured only when their outcomes are independent
    # of protected data; raw-source and address flags must remain coherent.
    print(json.dumps(dict(status='PASS',
      original_fourier_pairs=64,assumed_L4_global_choi_addresses=2049,
      local_choi_addresses=21,two_plane_exact_and_oldright_isometry=True,
      tests=tests,
      example_raw_source_readiness=dict(gamma_fourier='1/4',gamma_choi='1/9',
         k_fourier=kf,k_choi=kj,bank_success=str(ready),
         U_and_Uadjoint_calls=80*(2*kf+1)+180*(2*kj+1)),
      unverified_equality_oracle_L4_resource_estimate=dict(
         controlled_Toffoli=nof,CX_including_known_one_NOT=ncx,SourceI=2,
         notes='arithmetic sketch only; no explicit circuit or exhaustive simulation; excludes readiness intersection and U_raw'),
      actual_native_source_and_inverse_word_replayed=False,
      heralded_source_requires_coherent_full_dilation_and_ready_flags=True,
      oldright_ever_measured=False,
      total_Book03_work_and_GR_closed=False),indent=2,sort_keys=True))

if __name__=='__main__':main()
