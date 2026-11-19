"""Mathematical 3-stop A2 selector check on scalar flat 4-torus; no GR certificate."""
import math

def torus_scalar_heat(t, m2):
    kmax=math.ceil(math.sqrt(40/(4*math.pi**2*t)))
    z=1+2*sum(math.exp(-4*math.pi**2*t*k*k) for k in range(1,kmax+1))
    return math.exp(-m2*t)*z**4

def selector(t,m2):
    return -2*(4*math.pi)**2*t*(torus_scalar_heat(t,m2)-5*torus_scalar_heat(2*t,m2)+4*torus_scalar_heat(4*t,m2))

def checker():
    weights=[1,-5,4]
    scales=[1,2,4]
    assert sum(w/(s*s) for w,s in zip(weights,scales))==0
    assert sum(weights)==0
    assert sum(w/s for w,s in zip(weights,scales))==-0.5
    for m2 in (0.0,2.5):
        print('mass2=',m2)
        for t in (.04,.02,.01,.005,.0025):
            got=selector(t,m2)
            print(f't={t:.4f} select={got:.10f} err={got+m2:+.3e}')
        if abs(selector(.0025,m2)+m2)>0.00035:
            raise AssertionError('A2 selector limit mismatch')
    print('status=PASS')

if __name__=='__main__':checker()
