"""Full-leaf and full-tree candidate information on one herald-free physical suffix."""
from itertools import product
from math import log, sqrt, isclose
import json

P = (sqrt(5)-1)/2
ELL = -log(P)
R = 4*P**3


def entropy(ps):
    return -sum(x*log(x)/ELL for x in ps if x)


def close(x, y):
    assert isclose(x, y, rel_tol=2e-11, abs_tol=3e-11), (x,y)


def run():
    # On a Golden head v, G and XGX have columns Gv and |0>. Sharp outcomes
    # are recorded. These local matrices are tensored with identity on previous work.
    a = sqrt(P)
    close((2*a*P)**2, R)
    close((P*P + a*a)**2, 1)
    close(-P*a+a*P, 0)
    h = entropy([1-R,R])
    examples = []
    cases = 0
    for q in (0.23, 0.31, 0.379):
        # Multiple distinguishable old words on each side move independently.
        probabilities = [(1-q)*.63,(1-q)*.37,q*.28,q*.72]
        slopes = [-.63,-.37,.28,.72]
        tariff = [3.2+q,1.4-q,2.8+q/2,.8]
        tprime = [1,-1,.5,0]
        for n in range(1,7):
            for mix in (0,.25,.75,1):
                old_h = entropy(probabilities)
                whole_h = old_h+(1-q)*n*h
                dh = -sum(v*log(px)/ELL for px,v in zip(probabilities,slopes))-n*h
                rows=[]
                prefix_gains=[]
                for i,px in enumerate(probabilities):
                    active=i<2
                    rem=n*h if active else 0
                    prefix_gains.append(mix*(whole_h-rem)-(1-mix)*log(px)/ELL)
                    for bits in product((0,1),repeat=n) if active else [(0,)*n]:
                        ones=sum(bits)
                        u=(R**ones*(1-R)**(n-ones)) if active else 1
                        total_info=mix*whole_h-(1-mix)*log(px*u)/ELL
                        extra=n+ones
                        action=tariff[i]+extra-total_info
                        dact=tprime[i]+(1-mix)*slopes[i]/(px*ELL)-mix*dh
                        rows.append((px*u,action,dact,i))
                close(sum(v[0] for v in rows),1)
                close(sum(px*gain for px,gain in zip(probabilities,prefix_gains)),old_h)
                close(entropy([v[0] for v in rows]),whole_h)
                z=sum(P**a for _,a,_,_ in rows)
                a0=P/(1-R)**(1-mix); a1=P**2/R**(1-mix)
                k=[(a0+a1)**n]*2+[P**n]*2
                m=[max(a0,a1)**n]*2+[P**n]*2
                base=[P**c*px**(mix-1) for c,px in zip(tariff,probabilities)]
                close(z,P**(-mix*whole_h)*sum(b*v for b,v in zip(base,k)))
                close(min(row[1] for row in rows),
                      -log(max(b*v for b,v in zip(base,m)))/ELL-mix*whole_h)
                # All single-branch slopes, and consequently Gibbs' convex average.
                dz=sum(P**ac/z*dc for _,ac,dc,_ in rows)
                herr=-sum(v*log(px)/ELL for px,v in zip(probabilities,slopes))
                bound=max(abs(tr+(1-mix)*dp/(px*ELL)-mix*herr)
                          for tr,dp,px in zip(tprime,slopes,probabilities))
                assert abs(dz-n*mix*h)<=bound+1e-10
                assert max(abs(row[2]-n*mix*h) for row in rows)<=bound+1e-10
                if n==6 and q==.31 and mix in (0,1):
                    examples.append(round(dz,9))
                cases+=1
        # Earliest field branch is actually debited under a suffix-dependent drop.
        assert entropy(probabilities)-100*q*h < 0
    print(json.dumps(dict(trees=cases, entropy_per_active_read=round(h,12),
                          absolute_cost_slope_at_n6_event_drop=examples,
                          negative_upstream_drop_at_n100=True),indent=2))


if __name__ == "__main__":
    run()
