"""Exact bounds for any finite reference on the original stopped full128 coframe."""
from collections import defaultdict
from contextlib import redirect_stdout
from fractions import Fraction as F
from hashlib import sha256
from io import StringIO
from math import isqrt
from pathlib import Path
import json
import runpy

import sympy as sp


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def root_up(x):
    scale = 10**12
    return F(1 + isqrt(x.numerator * scale**2 // x.denominator), scale)


def geometric_bounds(lam):
    # Bracket the unique root of p^2+p=1. Each denominator stays positive.
    lo, hi = F(61803398874989,10**14), F(61803398874990,10**14)
    require(lo*lo+lo < 1 < hi*hi+hi, 'golden root')
    def increasing(p):
        b = 4*p**3*lam**2
        v = 4*p**3*lam*(1-lam)
        return b, p*v, v/(1-b)
    b0,w0,r0 = increasing(lo)
    b1,w1,r1 = increasing(hi)
    u0,u1 = (1-2*hi**2*lam)**2, (1-2*lo**2*lam)**2
    return (w0+u0*r0)/(1-b0), (w1+u1*r1)/(1-b1), r0, r1, lo, hi


def main():
    base = Path(__file__).resolve().parents[2]/'round69'/'stopped'
    script = base/'primary_section_7gb.py'
    raw = script.read_bytes().replace(b'bin(lab & j).count("1")', b'(lab & j).bit_count()').replace(
        b'bin(bits).count("1")', b'bits.bit_count()')
    require(sha256(raw).hexdigest() == '2ac8b4202c0212cf19a66c0a8940680cf94a405bdd99f2466936076faa7e9d66',
            'original section 7gb')
    with redirect_stdout(StringIO()) as out:
        src=runpy.run_path(str(script))
    require(json.loads(out.getvalue())['strictly_positive_by_integer_comparison'], 'native input')
    helpers=runpy.run_path(str(base/'check_stopped_response.py'))
    log_bounds,log_sum=helpers['log_bounds'],helpers['log_sum']
    a,da,l,ns,dns=(src[x] for x in ('a','da','kappa','ns','dns'))
    normalizer=l*(1-l)
    dim=a.rows
    all_speed=rare_speed=rare_mass=chi2=sp.S.Zero
    increments=defaultdict(lambda: sp.S.Zero)
    log_likelihood=defaultdict(lambda: sp.S.Zero)
    rare_effect=sp.zeros(dim)
    warm_square=sp.zeros(dim)
    for n,dn in zip(ns[1:],dns[1:]):
        b,db=n.H*a,dn.H*a+n.H*da
        speed=sp.expand(sp.trace(db.H*db))/(dim*normalizer)
        warm_square+=db*db.H
        all_speed += speed
        m=(n*n.H).applyfunc(sp.expand)
        eigs=[x/(1-l) for x in m.diagonal()]
        t=sum(eigs)/dim
        if t == 0:
            continue
        increments[F(t)]-=F(sp.expand(sp.trace(dn*n.H+n*dn.H))/(dim*(1-l)))
        require(max(eigs)<=4*t,'rare envelope')
        if min(eigs)==max(eigs):
            continue
        rare_mass+=t
        rare_effect+=b.H*b/normalizer
        rare_speed+=speed
        for x in eigs:
            chi2+=(x-t)**2/(dim*t)
            if x:
                log_likelihood[x/t]+=x/dim

    f=F(32,3155)
    require(rare_mass==f and src['same'](rare_effect,rare_mass*sp.eye(dim)), 'constant rare probability')
    require(rare_speed==sp.Rational(629,11358) and all_speed==sp.Rational(8005,5679), 'actual operator speeds')
    require(chi2==3*f/2, 'input quantum chi-square')
    require({k:v for k,v in log_likelihood.items() if k!=1}=={4:sp.Rational(16,3155)}, 'one-mark Holevo mass')
    h0,h1=log_sum(increments)
    p0,p1,r0,r1,pl,ph=geometric_bounds(F(l))
    # The first full128 visit can itself be the preparation. Its new reference
    # isometry has squared speed 4*p^2 times the largest eigenvalue below.
    warm_square=warm_square.applyfunc(sp.expand)
    mu=sp.trace(warm_square)/dim
    centered=warm_square-mu*sp.eye(dim)
    variance=sp.expand(sp.trace(centered*centered)/dim)
    require(src['same'](centered*centered,variance*sp.eye(dim)),'native two-point speed spectrum')
    warm_speed=root_up(4*ph**2*(F(mu)+root_up(F(variance))))
    require(warm_speed<F(19,100) and src['same'](da.H*da/l,sp.eye(dim)*sp.Rational(10,9)),
            'genuine preparation and polar-section speeds')
    center0=p0*h0/(1-r0)**2
    center1=p1*h1/(1-r1)**2
    x=r1*root_up(1+3*f)
    field_tail=2*p1*root_up(F(all_speed)*3*f/2)*((1+x)/(1-x)**3-1)
    field_error=2*p1*root_up(F(rare_speed)*F(chi2))+field_tail
    mem_tail=2*p1*f*root_up(F(3))*(1/(1-x)**2-1)
    mem_error=2*p1*root_up(f*F(chi2))+mem_tail
    low,high=center0-field_error,center1+field_error
    require(F(1488,100000)<low<high<F(1799,100000),'field range for every fixed spectator')
    require(mem_error<F(54,100000),'memory delivery speed')
    require(low>27*mem_error,'no cancellation for speed <=27')
    require(low-142*warm_speed*mem_error>0,'subsequent record after 142 complete warmup visits')
    active0,active1=(4*x*x*F(l)*(1-F(l)) for x in (pl,ph))
    zero0,zero1=1-p1/(1-r1),1-p0/(1-r0)
    one1=(1-active0)*p1+active1*zero1
    two1=p1*((1-active0)*r1+active1)
    warm_error=2*one1*root_up(F(rare_speed)*F(chi2))+two1/(p1*r0)*field_tail
    wlow=center0+active0*h0-warm_error
    whigh=center1+active1*h1+warm_error
    require(F(2938,100000)<wlow<whigh<F(3592,100000),'full warm-up and STOP entropy together')
    l2,h2=log_bounds(F(2))
    il=p0*f*l2
    ih=p1*f*h2*(1+2*(1/(1-r1)**2-1))
    require(F(1470,10**7)<il<ih<F(1549,10**7),'nonzero stopped reference information')
    hcl0,hcl1=F(1636,100000),F(1650,100000)
    hq0,hq1=F(1551,100000),F(1681,100000)
    require(102 < (hcl0+hq0)/(2*ih) and (hcl1+hq1)/(2*il)<114,'erasure slope at half disclosure')
    lp0,lp1=log_bounds(1/ph)[0],log_bounds(1/pl)[1]
    for nu,left,right in [(1,F(649,10000),F(718,10000)),(2,F(479,10000),F(546,10000))]:
        require(left < (low+hcl0/nu)/lp1 < (high+hcl1/nu)/lp0 < right,
                'disjoint extra cost on a quiet leaf')
    require(low-4*mem_error+hcl0 > high+4*mem_error+hcl1/2,
            'distinguishable even with reference speed four')
    # After six actual address readings at every visit, the expected code source
    # is the original source divided by survival. This term is in Golden units.
    q1=4*ph**3*F(l)
    reader1=F(81,12800)*ph**5/(1-q1)
    require(reader1<F(579,10**6) and low/lp1-reader1>F(303,10000),'unpaid source after pointer code')
    absolute_tv, prefix_tv = F(3677,10**6), F(5979,10**6)
    require(low/lp1-reader1 > max(8*absolute_tv,5*prefix_tv),
            'eight units per stopped record or five per visit cannot compensate any fixed spectator')
    warm_reader=reader1+F(81,12800)*ph**5
    require(wlow/lp1-warm_reader>F(599,10000),'net source of complete warm-up and STOP pointer ledger')
    print(json.dumps({'universe':'every finite quantum memory channel on the canonical reference',
                      'coframe_derivative_nats':['0.01488','0.01799'],
                      'extra_uncertainty_per_unit_of_dilation_speed_upper':'0.00054',
                      'stopped_Holevo_nats':['0.0001470','0.0001549'],
                      'zero_conditional_entropy_jet_requires_memory_speed_above':27,
                      'actual_native_warmup_reference_speed_upper':'0.19',
                      'certified_positive_after_this_many_preparatory_visits':142,
                      'whole_record_one_warmup_and_stop_nats':['0.02938','0.03592'],
                      'whole_record_after_six_readers_missing_mean_Golden_lower':'0.0599',
                      'half_disclosure_field_cancellation_slope':[102,114],
                      'quiet_leaf_cost_static_reference_Golden':{
                          'positive_price':['0.0649','0.0718'],'orthogonal_amplitude':['0.0479','0.0546']},
                      'after_six_pointer_code_missing_mean_Golden_lower':'0.0303',
                      'physical_C_closed':False,'GR_closed':False}, indent=2))


if __name__=='__main__':
    main()
