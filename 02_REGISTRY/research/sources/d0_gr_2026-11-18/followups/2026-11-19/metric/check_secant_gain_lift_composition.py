"""Marginal failure witness, scalar composition and 2-field chart lift.

The two-dimensional inverse is mathematical; this does not compile a physical
right lift or the complete geometry/Fourier/Choi/Book03 source.
"""
import itertools
import json
import math
import mpmath as mp
import numpy as np

mp.mp.dps=100
p=(mp.sqrt(5)-1)/2
b0=1-(1-2*p**3)**16
b232=1-(1-4*p**3)**32
b332=1-(1-16*p**9)**32
b264=1-(1-4*p**3)**64
b364=1-(1-16*p**9)**64
pmat=b0**226*(b232**4*b332)**113*b332**9
pone=pmat*(1-p**40)*b264**14*(b264**6*b364)**456
m=16
assert mp.mpf(14)/16 < pone < mp.mpf(15)/16
# a: exactly one failure, 1-a: exactly two, uniformly by subset.
a=2-m*(1-pone)
assert 0<a<1
flags=[]
for nfail,group_weight in ((1,a),(2,1-a)):
    for subset in itertools.combinations(range(m),nfail):
        flags.append((subset,group_weight/mp.binomial(m,nfail)))
assert abs(sum(w for _,w in flags)-1)<mp.mpf('1e-95')
for i in range(m):
    assert abs(sum(w for s,w in flags if i not in s)-pone)<mp.mpf('1e-95')
assert not any(len(s)==0 for s,_ in flags)

# Explicit noisy, old-state dependent CP updates with scalar success effects:
# success map sqrt(p_i) U_i, arbitrary 3-level initial rho; exact chain
# probabilities depend only on p_i even though the normalized state changes.
rng=np.random.default_rng(9249)
z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
rho=z@z.conj().T;rho/=np.trace(rho)
ps=np.linspace(.51,.96,16);prob=1.0
for prob_i in ps:
    z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    u,_=np.linalg.qr(z)
    K=math.sqrt(prob_i)*u
    rho=K@rho@K.conj().T;prob*=prob_i
assert abs(np.trace(rho).real-prob)<1e-14

# Real two-component matter field averaged in the Hilbert norm
# (1/256) sum_y (v0^2+v15^2).  The 712-G amplitude is physical.
pf=float(p);theta=math.asin(pf);A=pf*math.sin(712*theta);assert A>0
r=pf*pf;coords=list(itertools.product(range(4),repeat=4));S=len(coords)
def field(u,v):
    return np.array([[math.cos(math.pi/2*(y[1]+u*y[0]+v*y[2])),
                      math.sin(math.pi/2*(y[1]+u*y[0]+v*y[2]))]
                     for y in coords])*A
a00,a10,a01,a11=field(0,0),field(1,0),field(0,1),field(1,1)
ds=(1-r)*(a10-a00)+r*(a11-a01)
dt=(1-r)*(a01-a00)+r*(a11-a10)
J=np.stack([ds.reshape(-1),dt.reshape(-1)],axis=1)/math.sqrt(S)
G=J.T@J
B=1-2*r+2*r*r;c=(2*r-1)**2
expected=A*A*np.array([[2*B,c],[c,2*B]])
assert np.max(np.abs(G-expected))<1e-13
assert np.allclose(np.linalg.eigvalsh(G)/A**2,[1,11-16*pf],atol=1e-13)
R=J@np.linalg.inv(G)
assert np.max(np.abs(J.T@R-np.eye(2)))<1e-13
assert abs(np.linalg.norm(R,2)-1/A)<1e-12

def mean(s,t):return (1-s)*(1-t)*a00+s*(1-t)*a10+(1-s)*t*a01+s*t*a11
for n in (2,8,20):
    d=pf**(n+1);base=mean(r,r)
    assert np.max(np.abs((mean(r+d,r)-base)/d-ds))<1e-10
    assert np.max(np.abs((mean(r,r+d)-base)/d-dt))<1e-10

# Seed-only floor with two independently run m=16 devices and the sixteen
# protected Fourier/CAR successes: assumes full-interface scalarity and fresh
# factories, not actual overall source gain or full apparatus readiness.
example=[]
for n in (2,8,20):
    d=p**(n+1); lower=(1-d**4)**2*pone**16
    example.append({'N':n,'seed_plus_sixteen_floor_conditional':mp.nstr(lower,20)})
print(json.dumps({'status':'PASS',
 'P_one_conditional':mp.nstr(pone,30),'P_one_power_16':mp.nstr(pone**16,30),
 'P_one_power_80_not_a_claim_of_composed_report':mp.nstr(pone**80,30),
 'marginal_zero_joint_counterexample':{'n_one_failure':16,'n_two_failures':120,
 'one_failure_subset_probability':mp.nstr(a/16,30),
 'two_failure_subset_probability':mp.nstr((1-a)/120,30),
 'total_weight_exactly_one_failure':mp.nstr(a,30),'all_success_probability':0},
 'scalar_conditional_chain_test_passed':True,
 'A_star':A,'field_norm':'sqrt((1/256) sum_y (v_0(y)^2+v_15(y)^2))',
 'field_gram_eigenvalues':np.linalg.eigvalsh(G).tolist(),
 'field_gram_eigenvalues_really_normalized':(np.linalg.eigvalsh(G)/A**2).tolist(),
 'mathematical_right_inverse_norm':float(np.linalg.norm(R,2)),
 'mathematical_right_inverse_exact_norm':'1/A_star',
 'conditional_readiness_examples':example,
 'physical_lift_or_complete_normalized_gain_established':False,'GR_closed':False},indent=2))
