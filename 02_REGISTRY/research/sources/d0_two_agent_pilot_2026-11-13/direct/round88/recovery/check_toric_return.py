"""The native Golden recovery, the true Fourier address register, and protected torus fibres."""
from itertools import product
import json
import mpmath as mp
import numpy as np


mp.iv.dps = 85
mp.mp.dps = 85
iv = mp.iv
p = (iv.sqrt(5)-1)/2
a = iv.sqrt(p)
h = p**3
eta = 4*p**3
A = p*iv.sin(712*iv.atan2(p,a))
b = A*A


def need(x, name):
    if not x:
        raise ArithmeticError(name)


def same(x,y,label):
    need(np.max(abs(x-y))<3e-13,label)


def show(x):
    return mp.nstr(mp.mpf(x.mid), 18)


def enclosed(x,lo,hi):
    need(x.a > iv.mpf(lo) and x.b < iv.mpf(hi), str(x))


def double_probe():
    P=float(p.mid); aa=float(a.mid)
    t=np.array([[0,1],[1,0]]);z=np.diag([1,-1]);eye=np.eye(2)
    g=np.array([[aa,-P],[P,aa]])
    cx=np.block([[eye, 0*eye],[0*eye,t]])
    k=np.split((np.kron(g.T,eye)@cx)@np.kron([[aa],[P]],eye),2)
    ps=[(eye+t)/2,(eye-t)/2]
    for (r,s),expected in zip(product(range(2),repeat=2),
                               (P**3*eye,-2*P*aa*ps[0],-2*P*aa*ps[1],0*eye)):
        same(z@k[s]@z@k[r],expected,"actual chronological output")
    same(sum(kj.T@kj for kj in k),eye,"instrument normalizes")
    # Actual Z_source on arbitrary protected Spin is I or L_i, with L_i^2=-I.
    li=np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    source=np.block([[np.eye(4),np.zeros((4,4))],[np.zeros((4,4)),li]])
    same(source@source,np.kron(z,np.eye(4)),"full Spin spectator on native Z")
    same(np.sort(np.linalg.eigvalsh(k[0].T@k[0])),np.array([P**6,1]),"universal return bound")
    same(np.sort(np.linalg.eigvalsh(k[1].T@k[1])),np.array([0,4*P**3]),"click has a kernel")


def fourier_states():
    sites=np.array(list(product(range(4),repeat=4)))
    units=np.eye(4,dtype=int)
    directions=[*units,*(units[i]-units[j] for i in range(4) for j in range(i))]
    cos=np.array([1,0,-1,0]);sin=np.array([0,1,0,-1])
    candidates=[tuple(k) for k in sites if tuple(k)<tuple((-k)%4)]
    chosen=sorted(candidates,key=lambda k:(-sum(cos[(d@k)%4] for d in directions),k))[:64]
    phases=sites@np.array(chosen).T%4
    # For a fixed six-bit label, keep both real quadratures and the full SITE/CAR.
    table=np.stack((cos[phases],sin[phases]),axis=-1)
    P=float(p.mid);aa=float(a.mid);amp=float(A.mid)
    waves=[];crows=[]
    for mu in range(2):
        car=np.zeros((256,16))
        car[:,0]=amp*cos[sites[:,mu]];car[:,15]=amp*sin[sites[:,mu]]
        car[:,1]=aa;car[:,14]=np.sqrt(P*P-amp**2)
        crows.append(car)
        full=table[:,:,None,:]*car[:,None,:,None]/128
        waves.append(full)
        same(np.sum(full**2,axis=(0,2,3)),np.full(64,1/64),"index is exactly field independent")
        for j,k in enumerate(chosen):
            state=full[:,j,:,:]
            for axis in range(2):
                perm=np.arange(256).reshape([4]*4).take([2,3,0,1],axis=axis).ravel()
                charge=state-(-1)**k[axis]*state[perm]
                wrong=np.vdot(charge,charge)/4
                same(wrong,amp**2/64 if axis==mu else 0.,"identifying charge in the actual Fourier state")
    same(np.vdot(waves[0],waves[1]),1-amp**2,"full input Gram")
    overlaps=np.sum(crows[0]*crows[1],axis=1)
    diff=(sites[:,0]-sites[:,1])%4
    same(overlaps,1-amp**2*(1-cos[diff]),"unknown input column Gram")
    for inds,ratio in [(diff<=3,0),(diff!=0,1),(diff==2,2)]:
        same(1-max(overlaps[inds]),ratio*amp**2,"uniform Gram upper bound on torus support")
    fiber=(sites[:,0]==0)&(sites[:,1]==2)
    need(int(sum(fiber))==16,"sixteen unknown old addresses")
    rng=np.random.default_rng(88)
    ref=rng.normal(size=(16,5))+1j*rng.normal(size=(16,5));ref/=np.linalg.norm(ref)
    # Each |chi_x> has unit norm in this isometric conditional input, independently of old RIGHT.
    target=ref[:,None,:,None]*table[fiber,:,:,None].transpose(0,1,3,2)/8
    for mu in (0,1):
        c=crows[mu][fiber];coef=P*c[:,0]+aa*c[:,1]
        prob=P*P*(1+(1-2*mu)*amp)**2
        same(coef**2,np.full(16,prob),"flag admits a scalar effect on the whole protected fibre")
        post=target*coef[:,None,None,None]
        same(post/np.sqrt(prob),target,"true Fourier plus unknown external field state is returned")
    for mu in (0,1):
        physical=crows[mu][:,[0,15]]
        gradients=[]
        for axis in range(4):
            rolled=np.roll(np.arange(256).reshape([4]*4),-1,axis=axis).ravel()
            gradients.append(np.sum((4*(physical[rolled]-physical))**2,axis=1))
        def cost(tau):
            inverse_columns=np.exp(np.array([-tau,tau,0,0]))/4
            weights=np.array([1,-1,-1,-1])*inverse_columns**2
            return np.sum(weights[:,None]*np.array(gradients),axis=0)
        same(cost(0),np.full(256,(1-2*mu)*2*amp**2),"full CAR directional stencil")
        dt=0.00001
        same((cost(dt)-cost(-dt))/(2*dt),np.full(256,-4*amp**2),"volume-preserving coframe tangent")
    return np.array(chosen)


def main():
    double_probe()
    modes=fourier_states()
    parities=np.array([1 if k[1]%2==0 else -1 for k in modes])
    need(sum(parities)==-4,"spatial Fourier expectation is -1/16")
    neutral=h*h
    enclosed(neutral,".05572809000084120",".05572809000084123")
    def entropy(q):
        return -(q*iv.ln(q)+(1-q)*iv.log1p(-q))/(-iv.ln(p))
    q5=(1+iv.mpf(1)/16)/2
    q6=(1+(1-2*b)/16)/2
    change=-eta*(entropy(q6)-entropy(q5))
    enclosed(change,"-.00000190238256655","-.00000190238256653")
    # Exact algebra per fixed T sector: independent neutral/read masks at all scheduled probes.
    for n in (1,2,4):
        for pi in (mp.mpf(".18"),mp.mpf(".72")):
            norm=mp.mpf(0); informative=mp.mpf(0);zero=mp.mpf(neutral.mid)
            for mask in product((0,1),repeat=n):
                z=zero**(n-sum(mask))*(1-zero)**sum(mask)
                norm+=z; informative+=z*bool(sum(mask))*pi
            need(abs(norm-1)<mp.mpf("1e-65") and abs(informative-pi*(1-zero**n))<mp.mpf("1e-65"),"every complete schedule mask")
    print(json.dumps({
        "four_fine_records":["p^3 I","-sqrt(eta) P+","-sqrt(eta) P-","0"],
        "sharp_unknown_return_probability":show(neutral),
        "four_axis_full_unknown_return":show(neutral**4),
        "both_readers_always_executed":True,
        "two_word_mean_length":show(2+eta),
        "registered_C_minus_H_F6_minus_F5":show(change),
        "promised_pair_USD_upper":show(b),
        "genuine_full_Fourier_one_pair_each_axis":show(eta*b),
        "two_pairs_each_axis":show((1-neutral**2)*b),
        "fibre_unrestricted_remaining_SITE_dimension":16,
        "public_CAR_event_F5":show(p**2*(1+A)**2),
        "public_CAR_event_F6":show(p**2*(1-A)**2),
        "coframe_source_slope_on_each_fixture":show(-4*b),
        "one_name_return_on_all_inputs_certified":False,
        "full_Book03_energy_identified":False,"GR_closed":False
    },indent=2))


if __name__=="__main__":
    main()
