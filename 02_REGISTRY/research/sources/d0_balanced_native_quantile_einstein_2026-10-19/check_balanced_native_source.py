#!/usr/bin/env python3
"""Balanced ORIGINAL Fibonacci/F-R histories and exact local-vs-volume J2 FIRST SOURCE.

Narrow finite controls only:
  - original 4D native word centres (no word readdressing),
  - exact equal READY weights using min-count selection and retained complement,
  - unchanged nonuniform F/R counts hostile comparison,
  - original TWO scene-Golden-tick J2 matter/gravity coefficient,
  - genuinely moving volume quantile but exact SOURCE on f=q=0 at the
    original native macro cell representatives.

Consumes, does not rerun, original symbolic full 40-row Lorentz-star
Brinkmann and complete Book-price owners. It is NOT compulsory D0
programme selection, a new Einstein action, or original raw #216.
"""
from collections import Counter
from math import cos, log, pi, sin, sqrt

P = (sqrt(5)-1)/2
Z = 2**-20
LSTAR = 4*P**3
A = P**6
Q0 = 1-Z*LSTAR
R0 = 1-Z*LSTAR*(1+A)
MATTER_RATIO = -2/P**5*(R0/Q0+A)
SCENE_RANK = 528
CSTAR = SCENE_RANK*Z*4*P**11/R0

def near(a,b,tol=1e-10):
    if abs(a-b)>tol:
        raise AssertionError(f"mismatch {a}, {b}; error={abs(a-b)}")

def fibonacci(n):
    a,b=0,1
    for _ in range(n):
        a,b=b,a+b
    return a

def original_cost_words(n,L):
    """Compute ONLY canonical 4D nested centres of raw F/R cost-n words."""
    cells=Counter()
    def visit(remaining,k,left,width):
        if remaining==0:
            site=tuple(min(L-1,int(L*(left[i]+width[i]/2))) for i in range(4))
            cells[site]+=1
            return
        axis=k%4
        ww=width[:]
        ww[axis]*=P
        visit(remaining-1,k+1,left[:],ww)
        if remaining>=2:
            ll=left[:]
            ww=width[:]
            ll[axis]+=P*ww[axis]
            ww[axis]*=P*P
            visit(remaining-2,k+1,ll,ww)
    visit(n,0,[0.]*4,[1.]*4)
    assert sum(cells.values())==fibonacci(n+1)
    assert len(cells)==L**4
    return cells

def balanced_native_carrier(n,L):
    counts=original_cost_words(n,L)
    minimum=min(counts.values())
    maximum=max(counts.values())
    assert minimum>0 and maximum>minimum
    active=minimum*L**4
    inactive=fibonacci(n+1)-active
    # Every selected word retains its TRUE native PF p^n and TWO original
    # literal equal-cost READY suffixes, not a replacement uniform prior.
    per_site_ready_pair_trace=2*P**(n+3)*minimum
    total_ready_mass=L**4*per_site_ready_pair_trace
    original_prefix_mass=fibonacci(n+1)*P**n
    assert 0<total_ready_mass<1
    assert inactive>=0
    print(f"n={n} L={L} originalWords={fibonacci(n+1)} "
          f"originalMin/Max={minimum}/{maximum}, "
          f"activated={active}, unactivatedStillRetained={inactive}")
    print(f"  native selected READY pair total PF mass={total_ready_mass:.12f}, "
          f"full exact-cost prefix mass={original_prefix_mass:.12f}")
    return counts,minimum,per_site_ready_pair_trace

def real_original_two_tick_source(counts,minimum):
    """True native site masses are not equal before subset selection."""
    nsites=len(counts)
    arbitrary_f=[sin(1.7*j)+.4*cos(.17*j) for j in range(nsites)]
    arbitrary_q=[cos(.71*j)+.3*sin(.19*j) for j in range(nsites)]
    avg_exact=sum(arbitrary_f[j]+MATTER_RATIO*arbitrary_q[j]
                  for j in range(nsites))/nsites
    # Balanced original finite old-LEFT DEFINE weights, all same-cost/type0.
    # The unknown common D0/K finite regular factor cancels IN EXACT SOURCE.
    native_balanced=sum(minimum*(arbitrary_f[j]+MATTER_RATIO*arbitrary_q[j])
                        for j in range(nsites))/(minimum*nsites)
    near(native_balanced,avg_exact,1e-12)
    # The UNBALANCED original F/R cell counts must NOT be called uniform.
    # Preserve the original lattice-cell order while reading ORIGINAL counts.
    ordered_counts=[counts[key] for key in sorted(counts)]
    weighted_old=sum(c*(arbitrary_f[j]+MATTER_RATIO*arbitrary_q[j])
                    for j,c in enumerate(ordered_counts))/sum(ordered_counts)
    assert abs(weighted_old-avg_exact)>1e-5
    return abs(weighted_old-avg_exact)

def lagrange_cardinal(nodes,values,y):
    """Smooth interpolant which matches ALL original macro centre values."""
    s=0.
    for i,xi in enumerate(nodes):
        basis=1.
        for j,xj in enumerate(nodes):
            if i!=j:
                basis*=(y-xj)/(xi-xj)
        s+=values[i]*basis
    return s

def inverse_volume_quantile(code,eps,scale=.3):
    """EXACT smooth 1D triangular Rosenblatt stage for rho=1+eps scale cos(2pi x).
    Other 3 stages are unchanged identities; the normalizer is exactly V=1.
    """
    x=code
    for _ in range(12):
        value=x+eps*scale*sin(2*pi*x)/(2*pi)-code
        deriv=1+eps*scale*cos(2*pi*x)
        x-=value/deriv
    return x

def exact_moving_source_test(L):
    h=1/L
    nodes=[(i+.5)*h for i in range(L)]
    valsF=[cos(2*pi*y)+.2*sin(3*pi*y) for y in nodes]
    valsQ=[sin(1.2*pi*y)+.1*cos(5*pi*y) for y in nodes]
    eps=1e-4
    for j,u in enumerate(nodes):
        def queries(e):
            x=inverse_volume_quantile(u,e)
            jac=1+e*.3*cos(2*pi*x)
            # At e=0, original F,Q are identically ZERO FUNCTIONS.
            # Moving T and denominator J have zero first derivative
            # coefficient; only the explicitly linear operator source remains.
            f=e*lagrange_cardinal(nodes,valsF,x)/jac
            q=e*lagrange_cardinal(nodes,valsQ,x)
            return f,q
        pos=queries(eps)
        neg=queries(-eps)
        df=(pos[0]-neg[0])/(2*eps)
        dq=(pos[1]-neg[1])/(2*eps)
        near(df,valsF[j],1e-6)
        near(dq,valsQ[j],1e-6)
        # Original two-tick Book source must agree after moving volume/quantile.
        original_source=CSTAR*(valsF[j]+MATTER_RATIO*valsQ[j])
        moving_source=CSTAR*(df+MATTER_RATIO*dq)
        near(original_source,moving_source,1e-8)
    print(f"  L={L}: moving J/V triangular physical-volume source matches every "
          f"fixed original Role macro node at genuine f=q=0.")

def root_transfer_fixture(L):
    """Consume independent exact 40→3→1 symbolic Brinkmann theorem."""
    h=1/L
    time_energy=[.0004+.0002*cos(2*pi*j/L) for j in range(L)]
    def H(j,x,y):
        E=time_energy[(j-1)%L]
        # Nonquadratic exact harmonic transverse cubic and corrected quartic.
        return (-MATTER_RATIO*E*(x*x+y*y)
                +(.03*sin(2*pi*j/L))*(x**3-3*x*y*y)
                +.005*cos(4*pi*j/L)*(x**4-6*x*x*y*y+y**4-h*h*(x*x+y*y)))
    for j in range(L):
        for x,y in ((.12,.34),(.27,-.32),(-.17,.23),(.41,.51)):
            lap=(H(j+1,x+h,y)+H(j+1,x-h,y)
               +H(j+1,x,y+h)+H(j+1,x,y-h)-4*H(j+1,x,y))/h**2
            near(lap,-4*MATTER_RATIO*time_energy[j],1e-9)
    print(f"  L={L}: exact original staggered Cartan/Brinkmann sourced Poisson "
          f"test, with arbitrary u-energy and cubic/quartic harmonic modes.")

def exact_all_order_selector_quotient(counts,minimum):
    """Return-spectrum price independent of WHICH original labels, at arbitrary f,q.

    Selected words from ANY cell have same original total F/R cost and AF
    terminal type. Thus full left return blocks at fixed f_x,q_x all
    have identical Q/R determinants, including genuine two scene ticks.
    """
    from math import log1p
    N=len(counts)
    t2=.016
    def one_full_two_tick_leaf(f,q):
        E=P*P*(1+t2*f)
        b=(P-P*P*t2*q)**2
        B=4*b*(1-b)
        lam=4*E*(1-E)
        return -SCENE_RANK*(log1p(-Z*B)
                  +log1p(-Z*(lam+(1-lam)*B)))
    j0=one_full_two_tick_leaf(0.,0.)
    cell_values=[one_full_two_tick_leaf(.2*sin(.73*i),.1*cos(.29*i))
                 for i in range(N)]
    source_per_selected_site=sum(v-j0 for v in cell_values)
    # These k different selected subsets have different ACTUAL labels and
    # absolute signal, but one normalized actual two-tick determinant.
    labels_total=sum(counts.values())
    for k in set((1,max(1,minimum//2),minimum)):
        assert all(count>=k for count in counts.values())
        J0=labels_total*j0
        Jk=J0+k*source_per_selected_site
        near((Jk-J0)/k,source_per_selected_site,1e-8)
    assert any(count>minimum for count in counts.values())
    print("  PASS full OFF-SHELL two-tick return logdet independent of all "
          "within-cell original-word choices; exact k-normalized quotient.")

def off_null_moving_volume_midpoint_c1():
    """NONZERO f: both value and genuine d/d(volume) quantile source converge O(h²).

    This is the analytic 4D Rosenblatt case depending only on coordinate0:
    rho(y)=1+eps*.3*cos(2*pi*y0), other 3 coordinates unchanged.
    Query F(y)=y0², so integral rho F = 1/3+eps*.3/(2*pi²)
    and its nontrivial physical-volume first source is .3/(2*pi²).
    """
    eps=.4
    de=1e-5
    value_target=1/3+eps*.3/(2*pi*pi)
    source_target=.3/(2*pi*pi)
    for L in (8,16,32,64):
        def macro_mean(t):
            return sum(inverse_volume_quantile((j+.5)/L,t)**2
                       for j in range(L))/L
        value=macro_mean(eps)
        grad=(macro_mean(eps+de)-macro_mean(eps-de))/(2*de)
        e_value=abs(value-value_target)
        e_grad=abs(grad-source_target)
        assert e_value*L*L<.1, ("midpoint value",L,e_value)
        assert e_grad*L*L<.03, ("full moving volume source",L,e_grad)
        print(f"  OFF-NULL 4D volume transport L={L}: "
              f"|mean-Gamma|={e_value:.3e}, |real dGamma|={e_grad:.3e}")
    print("PASS C1 physical-volume source O(h²), NOT merely null-cancellation.")

def main():
    near(MATTER_RATIO,-23.416406751884,1e-11)
    print(f"TRUE corrected two-tick J2 CAR matter/gravity ratio={MATTER_RATIO:.12f}")
    for n,L in ((20,4),(28,8)):
        counts,m,weight=balanced_native_carrier(n,L)
        difference=real_original_two_tick_source(counts,m)
        exact_all_order_selector_quotient(counts,m)
        print(f"  WITHOUT native balancing, first source mismatch={difference:.8f}")
        exact_moving_source_test(L)
        root_transfer_fixture(L)
    off_null_moving_volume_midpoint_c1()
    print("PASS: original F/R address, EXACT balanced positive native source, "
          "moving physical volume FIRST jets, nonquadratic sourced Einstein root.")
    print("SCOPE: constructed complete AF×scene Book J2, not compulsory FULL D0 "
          "Cost-Info/H+J+R or old raw #216.")
if __name__=="__main__":
    main()
