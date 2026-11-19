"""Compress the fixed-reference 24-price selector and compare its gain.

The Boolean circuit is checked by the existing exact multi-terminal diagram,
not by enumerating all tapes.  The geometric-bank readiness and all physical
Cost-Info remain open.
"""
from fractions import Fraction
from itertools import accumulate
from math import comb, lcm
from random import Random
import json
import mpmath as mp
from check_selector36_compilation import (
    BooleanDiagram, MultiDiagram, Golden, ONE, P, expected_prefix,
    tape_of_exact_rank,
)


def main():
    cut=24
    weights=[Fraction((-1)**(j-1)*comb(8,j),j) for j in range(1,9)]
    scale=lcm(*(x.denominator for x in weights))
    sizes=[int(scale*abs(x)) for x in weights]
    assert scale==840 and sizes==[6720,11760,15680,14700,9408,3920,960,105]
    d=MultiDiagram(); root=d.compile(cut,sizes)
    expected=(ONE-Golden(sum(sizes))*P**cut,)+tuple(Golden(n)*P**cut for n in sizes)
    assert d.masses(root)==expected
    assert d.hits(24)==75025 and d.hits(23)==46368 and sum(sizes)==63253
    assert Golden(d.hits(24))*P**24+Golden(d.hits(23))*P**25==ONE
    # For integer allocation of these exact eight weights at equal leaf mass,
    # denominator 840 is minimal and the required leaves exceed F_24=46368.
    assert sum(sizes)>d.hits(23)
    for m in range(8):
        assert sum(weights[j-1]*j**(m+1) for j in range(1,9)) == (1 if m==0 else 0)
    b=BooleanDiagram(); roots=[b.from_multiroot(d,root,k) for k in range(6)]
    assert all(l<v and h<v for v,(_,l,h) in b.nodes.items())
    bounds=list(accumulate(sizes)); ranks={0,d.hits(cut)-1}
    for x in bounds:ranks.update((x-1,x))
    ranks={x for x in ranks if 0<=x<d.hits(cut)}
    tapes=[tape_of_exact_rank(cut,x) for x in sorted(ranks)]
    tapes += [[0]*cut,[1]*cut]
    rng=Random(20261119)
    tapes += [[rng.randrange(2) for _ in range(cut)] for _ in range(1000)]
    for tape in tapes:
        label=expected_prefix(tape,cut,sizes)
        assert d.output(root,tape)==label
        tag=label|(int(label!=0)<<4)|(int(label!=0 and label%2==0)<<5)
        assert b.compute_and_uncompute(tape,roots)==tag
    n=len(b.nodes); gates=4*n
    assert n==363 and gates==1452
    # Reuse the exact all-column heralded gate factory.  The Bernoulli tape,
    # arithmetic circuit and complete heralding are prepared before fields.
    mp.mp.dps=90
    p=(mp.sqrt(5)-1)/2; phi=1/p
    L=64; L0=40
    b2=1-p**(6*L); b3=1-(1-16*p**9)**L
    beta=(1-p**L0)*(b2**6*b3)**gates
    beta36=(1-p**L0)*(b2**6*b3)**2592
    z=mp.mpf(1)/2**20
    def report(x,y):
        E=p**2*(1+x); LL=4*E*(1-E)
        u=p+p**2*y; B=4*u**2*(1-u**2)
        A=LL+(1-LL)*B
        return z*(A+B)-z*z*A*B
    rf=mp.diff(lambda x:report(x,mp.mpf(0)),0)
    rq=mp.diff(lambda y:report(mp.mpf(0),y),0)
    k0=rq/rf
    F=mp.mpf(16517734400)/162621047169
    bref=F/(16*k0)
    eps=mp.mpf(1)/4096; h=eps/8; delta=eps*bref
    dy=report(0,delta)-report(0,-delta)
    dx=report(k0*delta,0)-report(-k0*delta,0)
    aa=dy/dx
    assert abs(dx-2*delta*rq)<mp.mpf('1e-80')
    lam=p**7*mp.sin(512*mp.asin(p))**2
    coeff=p**3*lam*rf
    # alpha_h is intentionally not chosen: the real F2-F6 ready probability
    # remains a physical parameter.  These are gains PER alpha_h^2.
    g24=beta*p**24*840*h*coeff*dy
    g36=beta36*p**36*705600*h*h*(2*bref*coeff*rq)
    ratio=g24/g36
    ratio_exact=(beta/beta36)*phi**12/105*(dy/(2*delta*rq))
    assert abs(ratio-ratio_exact)<mp.mpf('1e-70') and 3<ratio<4
    # Outward interval check is independent of numerical differentiation and
    # evaluates the true nonlinear y-reference without replacing it by its
    # leading term.  All intervals remain conditional on the chosen inputs.
    iv=mp.iv; iv.dps=65
    pi=(iv.sqrt(5)-1)/2; zi=iv.mpf(1)/2**20
    E0=pi**2; L0i=4*E0*(1-E0)
    Lxi=4*pi**2*(1-2*pi**2)
    Byi=8*pi**3*(1-2*pi**2)
    rfi=zi*(1-zi*L0i)*(1-L0i)*Lxi
    rqi=(zi*(2-L0i)-zi**2*(3*L0i-2*L0i**2))*Byi
    ki=rqi/rfi
    Fi=iv.mpf(16517734400)/iv.mpf(162621047169)
    bi=Fi/(16*ki); epsi=iv.mpf(1)/4096; hi=epsi/8; di=epsi*bi
    def reporti(y):
        u=pi+pi**2*y; B=4*u**2*(1-u**2)
        A=L0i+(1-L0i)*B
        return zi*(A+B)-zi**2*A*B
    dyi=reporti(di)-reporti(-di)
    b2i=1-pi**(6*L); b3i=1-(1-16*pi**9)**L
    beta24i=(1-pi**L0)*(b2i**6*b3i)**gates
    beta36i=(1-pi**L0)*(b2i**6*b3i)**2592
    ratioi=beta24i/beta36i*(1/pi)**12/105*dyi/(2*di*rqi)
    assert iv.mpf('0.99960845')<beta24i<iv.mpf('0.99960847')
    assert iv.mpf('3.06757')<ratioi<iv.mpf('3.06759')
    # Independent finite-algebra check on two arbitrary scalar operand sites;
    # it tests the interpolation, not admissibility of a physical geometry.
    mus=[mp.mpf('0.4'),mp.mpf('0.6')]
    invrho_f=[mp.mpf('0.03'),mp.mpf('-0.02')]
    invrho_m=[mp.mpf('0.01'),mp.mpf('0.025')]
    r0=report(0,0)
    vals=[]
    for j in range(1,9):
        t=j*h
        vals.append(sum(mu*(dy*(report(t*f,0)-r0)+dx*(report(0,-aa*t*m)-r0))
                        for mu,f,m in zip(mus,invrho_f,invrho_m)))
    lhs=sum(mp.mpf(w.numerator)/w.denominator*v for w,v in zip(weights,vals))
    I=sum(mu*(f-k0*m) for mu,f,m in zip(mus,invrho_f,invrho_m))
    rhs=h*dy*rf*I
    assert abs(lhs-rhs)<mp.mpf('1e-80')
    max_births=gates*(26*L+2)+2*L0+2*cut+(n+8)+1
    out={'schema':'d0.fixed-reference-selector24/1','status':'PASS',
      'cut':cut,'all_tapes':2**cut,'weights_denominator':scale,'allocations':sizes,
      'exact_hit_words':d.hits(cut),'overshoot_words':d.hits(cut-1),
      'active_words':sum(sizes),'multi_terminal_nodes':len(d.nodes),
      'binary_shared_nodes':n,'flag_output_bits':6,
      'logical_toffoli_upper_bound':gates,'logical_cnot_upper_bound':2*n+8,
      'zero_work_wires_upper_bound':n+8,'retained_random_symbols':cut,
      'tests_tapes':len(tapes),'whole_tape_argument':'BDD recursion and reversible node induction',
      'factory_success_independent_inputs':mp.nstr(beta,24),
      'factory_success_interval':str(beta24i),
      'birth_upper_bound_declared_factory_only':max_births,
      'births_exclude':'external geometry, physical routing and other unlisted apparatus',
      'early_abort_T_zero_slot':'one listed zero wire must be prepared before known-one factory; SourceI word operations and clock excluded',
      'reference_F_H_1_4':str(F),'b_reference_H_1_4':mp.nstr(bref,24),
      'epsilon_star':'1/4096','common_field_step_h':'1/32768',
      'gain24_per_alpha_squared':mp.nstr(g24,24),'gain36_per_alpha_squared':mp.nstr(g36,24),
      'gain_ratio_24_to_36':mp.nstr(ratio,24),'delta_y_to_linear_limit':mp.nstr(dy/(2*delta*rq),24),
      'gain_ratio_24_to_36_interval':str(ratioi),
      'comparison':'conditional common reference, fixed calibration and same physical alpha; not equal executions',
      'actual_alpha_geometry_and_full_price_computed':False,'GR_closed':False}
    print(json.dumps(out,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
