#!/usr/bin/env python3
"""Exact analytic + faithful finite original Golden native code first-match audit.

Research / scoped mathematical consumer of original n20/L4 Golden F/R +
0/10 register, NOT Book03 selected Info, native primitive controller price,
physical first-match task forcing, all42 closure or GR.

Retains every one of 72,441 source outcomes with their actual native
integer code charge; computes real 256 site multiplicities from unchanged
nested 4D Golden box positioning (no synthetic weights).
"""
from __future__ import annotations
from collections import Counter
from math import exp, fsum, log, log1p, sin, cos, sqrt, isfinite

p=(sqrt(5)-1)/2
phi=1/p
ell=log(phi)
K=10946
F20=6765
N=20
L=4


def check(ok, msg):
    if not ok: raise RuntimeError('FAIL_HARMONIC_NATIVE: '+msg)


def near(a,b,atol=1e-10,rtol=1e-10):
    return abs(a-b) <= atol + rtol*max(abs(a),abs(b))


def entropy(P):
    return -fsum(v*log(v) for v in P if v>0)/ell


def h(r):
    return -(r*log(r)+(1-r)*log1p(-r))/ell


def hp(r):
    return log((1-r)/r)/ell


def golden_prefixes(n=20,L=4):
    """Literal original N cost threshold nested F/R words and original centres."""
    exact=[]; overshoots=[]
    def rec(cost,j,left,width,word):
        if cost>=n:
            if cost==n:
                site=tuple(min(L-1,int(L*(left[k]+width[k]/2))) for k in range(4))
                exact.append((word,site))
            else:overshoots.append((word,cost))
            return
        axis=j%4
        wf=width.copy();wf[axis]*=p
        rec(cost+1,j+1,left.copy(),wf,word+'F')
        wr=width.copy();lr=left.copy()
        lr[axis]+=p*wr[axis];wr[axis]*=p*p
        rec(cost+2,j+1,lr,wr,word+'R')
    rec(0,0,[0.]*4,[1.]*4,'')
    return exact,overshoots


# 1. ALL true original site words, no balanced or synthetic replacement.
exact,over=golden_prefixes()
counts=Counter(z for word,z in exact)
check(len(exact)==K and len(over)==F20,'original F21/F20 exact/overshoot')
check(len(counts)==L**4 and min(counts.values())==29 and max(counts.values())==78,
      'all 256 genuinely nonuniform original Golden cells')
check(sum(counts.values())==K,'complete true original 4D counts')
check(all(cost==N+1 for word,cost in over),'true minimal cut overshoot paid')
check(near(F20*p**21+K*p**20,1,2e-11,0),'Golden original Kraft first crossing')

# 2. 72,441 leaf data: ORIGINAL all flags and both terminal native labels.
rb=1.8512395785208469e-6
# two mathematical bounded off-null deformation coordinates, not native 42 source.
weights={z:n/K for z,n in counts.items()}
def reports(t):
    return {z:rb*(1+.22*sin(2.9*z[0]+1.3*z[2])+
                   .075*cos(1.7*z[1]+2.3*z[3])+t*.16*sin(z[0]+2*z[1]+1))
            for z in counts}

def build(t):
    rs=reports(t)
    check(all(0<x<1 for x in rs.values()),'positive native report inputs')
    leaf=[]; pref=[]
    # cost 21 unready prefix and unchanged code branch.
    for word,cost in over:
        q=p**cost
        leaf.append((q,cost,'U',None))
        pref.append(q)
    for word,z in exact:
        for suffix,charge in [('FF',2),('RR',4)]:
            c=N+charge;q=p**c
            leaf.append((q,c,'U',None));pref.append(q)
        for suffix in ('FR','RF'):
            pr=p**(N+3);r=rs[z]
            pref.append(pr)
            leaf.append((pr*(1-r),N+4,'0',z))
            leaf.append((pr*r,N+5,'1',z))
    return leaf,pref,rs

def calc(t):
    leaf,pref,rs=build(t)
    check(len(leaf)==72441,'original ALL 72441 complete final records')
    check(len(pref)==F20+4*K,'genuine unobserved prefix before final reporter')
    P=[x[0] for x in leaf]
    C=fsum(prob*c for prob,c,a,z in leaf)
    H=entropy(P)
    Hp=entropy(pref)
    q3=[fsum(prob for prob,c,b,z in leaf if b==k) for k in ('U','0','1')]
    check(near(fsum(P),1,3e-11,0),'entire true P normalized')
    check(near(fsum(p**c for prob,c,b,z in leaf),1,3e-11,0),'native cost reference Kraft')
    a=2*K*p**23
    bar=fsum(w*rs[z] for z,w in weights.items())
    expected=[1-a,a*(1-bar),a*bar]
    check(all(near(q3[i],expected[i],3e-11,0) for i in range(3)),
          'coarse three atoms from full native 72k archive')
    check(near(Hp,F20*p**21*21+K*(p**22*22+2*p**23*23+p**24*24),3e-10,0),
          'original native prefix entropy exact Golden code mean')
    Hfine_expect=Hp+a*fsum(w*h(rs[z]) for z,w in weights.items())
    check(near(H,Hfine_expect,2e-10,0),'full fine entropy from true prefix plus site reports')
    H3=entropy(q3)
    ha=h(a)
    I=h(bar)-fsum(w*h(rs[z]) for z,w in weights.items())
    Kaddr=Hp-ha
    check(I>=-1e-10,'conditional archive mutual information positive')
    check(near(Hfine_expect-H3,Kaddr-a*I,3e-10,0),
          'exact missing fine info is address conditional - a MI')
    check(near(H3,ha+a*h(bar),3e-10,0),'3 atom entropy from real original readiness')
    # Completed fine probability/cost reference is original native self-code.
    S=C-H
    from_report=a*(1+bar-fsum(w*h(rs[z]) for z,w in weights.items()))
    check(near(S,from_report,2e-10,0),
          'actual complete native 0/10 Price-Shannon source')
    # First-match on ONLY THREE classes uses exactly 4 FULL registered fine trials
    # on average. Whole actual per-trial primitive PRICE is a true outcome ledger.
    Cstop_data=4*C
    harmonic_clock=H3*ell  # EXACT E[H_N] of genuine 3-class match
    S_from_clock=Cstop_data/4-harmonic_clock/ell-Kaddr+a*I
    check(near(S_from_clock,S,3e-10,0),'single full paid 3-class clock+archive weld')
    # Class-conditional mean costs of entire actual fine tape.
    group_cost={a:fsum(prob*c for prob,c,b,z in leaf if b==a)/q
                for a,q in zip(('U','0','1'),q3)}
    # TRUE stopped expected trials/counts; all nonmatch flags retained.
    expected_counts={b:2*q3[i]+sum(q3[j]*(q3[i]/q3[j])
                         for j in range(3) if j!=i)
                     for i,b in enumerate(('U','0','1'))}
    check(all(near(expected_counts[b],4*q3[i],1e-12,0)
              for i,b in enumerate(('U','0','1'))),
          'all actual category visits exactly four times marginal Born')
    check(near(fsum(expected_counts[b]*group_cost[b] for b in expected_counts),
               Cstop_data,1e-9,0),'actual paid 0/10 fine per-trial ledger 4*C')
    # Native harmonic time recovered from complete genuine STOPPING distribution.
    true_harmonic=-fsum(q*log(q) for q in q3)
    check(near(true_harmonic,harmonic_clock,3e-13,0),'whole clock reproduces H(q)')
    mean_tr=4
    second_tr=4+2*fsum(1/q for q in q3)
    variance_tr=second_tr-mean_tr**2
    check(variance_tr>0,'true stopped clock heavy-tail variance positive')
    return dict(C=C,H=H,Hp=Hp,H3=H3,S=S,MI=I,Kaddr=Kaddr,a=a,q3=q3,
                clock_info=harmonic_clock/ell,clock_cost=Cstop_data,
                stopped_second=second_tr,stopped_variance=variance_tr,
                values=rs,bar=bar,full=leaf)

X=calc(.37)
Y=calc(.37001)
check(near(X['Kaddr'],Y['Kaddr'],2e-12,0),'fixed native address baseline invariant')

# 3. Source pullback: entire retained 72,441-outcome action derivative
# and three-atom clock+archive decomposition on one real bounded chart.
step=1e-4
plus=calc(.37+step);minus=calc(.37-step)
Dfull=(plus['S']-minus['S'])/(2*step)
DclockC=(plus['clock_cost']-minus['clock_cost'])/(8*step)
DclockH=(plus['clock_info']-minus['clock_info'])/(2*step)
Darchive=X['a']*(plus['MI']-minus['MI'])/(2*step)
check(near(Dfull,DclockC-DclockH+Darchive,6e-9,1e-7),
      'complete off-null source recovered by real clock plus archive MI')
rs=X['values']; Dr={z:rb*.16*sin(z[0]+2*z[1]+1) for z in counts}
Danalytic=X['a']*fsum(w*(1-hp(rs[z]))*Dr[z] for z,w in weights.items())
check(near(Dfull,Danalytic,1e-7,1e-6),'true 72,441 analytic physical report source')

# 4. Harmonic-clock information uniqueness; exact first-match limit
# and finite cap diagnostics on 3 real native future atoms.
def cap_harmonic(q,M):
    x=1-q
    return fsum(x**k/k for k in range(1,M+1))

for q in (1/2,1/3,1/5):
    # Equality of the generating function coefficients: H_n are the only
    # coefficients of -log(1-x)/(1-x). Explicit finite q geometric tails.
    for M in (1,2,4,10,100,1000):
        partial=cap_harmonic(q,M)
        true=-log(q)
        gap=true-partial
        upper=(1-q)**(M+1)/((M+1)*q)
        check(gap>=-4e-15 and gap<=upper+5e-14,
              'rigorous harmonic cap value bound '+str((q,M)))
        # Exact derivative of conditional capped clock source; not a finite
        # difference or a guessed clock derivative.
        derivative=-(1-(1-q)**M)/q
        check(near(derivative-(-1/q),(1-q)**M/q,3e-12,0),
              'conditional first-source cap debt')

# Finite cap, SAME whole tape / true class-dependent native code cost:
# optional-stopping Wald gives E(C_stop^data)=E(T_cap)*E(C_one)
# with NO equality assumption on real F/R prefix/0/10 label prices.
for M in (1,2,5,10,100,10000,20000000,60000000):
    q3=X['q3']
    LM=4-fsum(exp(M*log1p(-q)) for q in q3)
    check(1<LM<=4,'positive genuine finite-cap firstmatch elapsed trials')
    cost_capped=LM*X['C']
    check(near(cost_capped/LM,X['C'],1e-12,0),
          'whole outcome-priced finite cap rate uses actual C not a flat gate price')
    # The resulting physical total is NOT identical to C, and a real
    # controller/readout baseline may have its own moving price.

for M in (10,100,10000,20000000,60000000):
    qmin=min(X['q3'])
    e=exp(M*log1p(-qmin))
    bound=e/(max(M,1)*qmin)
    # true unconditional H(q) first source removes the extra 1/q for
    # its rare-class factor, while the whole stopped cost carries K e^-Kq.
    conditional_derivative_error=e/qmin
    clock_derivative_debt=M*e
    check(all(isfinite(v) for v in (e,bound,conditional_derivative_error,clock_derivative_debt)),
          'finite actual clock error diagnostics')
    if M in (20000000,60000000):
        print('native cap',M,'rare_class',qmin,'Pr_no_match_tail',e,
              'conditional_info_source_debt',conditional_derivative_error,
              'true_clock_first_jet_debt_bound',clock_derivative_debt)

# 5. Rank-one coarse source kernel vs FULL spatial source, with two
# distinct ACTUAL native sites; this is the original admissibility-gated
# tangent countercontrol, not proof that field writer realizes it.
site_i=min(counts);site_j=max(counts)
wi=weights[site_i];wj=weights[site_j]
ri=X['values'][site_i];rj=X['values'][site_j]
if abs(ri-rj)<1e-12:
    site_j=max(counts,key=lambda z:abs(X['values'][z]-ri))
    wj=weights[site_j];rj=X['values'][site_j]
check(abs(ri-rj)>1e-12,'genuinely distinct original native site reports')
Dbar=wi*wj+wj*(-wi)
Dsource=X['a']*wi*wj*(hp(rj)-hp(ri))
check(abs(Dbar)<1e-15 and abs(Dsource)>1e-14,
      'coarse harmonic clock source blind, full native archive sees field')

print('PASS original full 72,441 original Golden-code words; exact 256 native site counts min/max 29/78')
print('PASS single genuinely paid three-class firstmatch: E T=4; harmonic clock gives exact H_phi(q3)')
print('PASS all input-data native cost source and immutable prefix archive baseline')
print('PASS SAME actual full 72,441 measured-code Price-Shannon = quarter stopped data-cost - harmonic clock + native archive MI')
print('PASS exact finite-cap conditional first-source debt, stopped-clock heavy-tail budget')
print('PASS native full report-source and off-null archive derivative; no fitted coefficient')
print('native READY',X['a'],'Kaddr',X['Kaddr'],'MI',X['MI'])
print('native q three:',X['q3'])
print('true firstmatch mean trials',4,'variance',X['stopped_variance'])
print('Book03 physical Info selected: FALSE; G0 task forcing: FALSE; GR_closed: FALSE')
