"""Minimal old-register motion for a genuine registered half-period service."""
from itertools import product
import json
import mpmath as mp
import numpy as np


iv = mp.iv
iv.dps = 85
mp.mp.dps = 85
p = (iv.sqrt(5)-1)/2
a = iv.sqrt(p)
h = p**3
amp = p*iv.sin(712*iv.atan2(p,a))


def need(truth, label):
    if not truth:
        raise ValueError(label)


def near(x, y, label):
    need(np.max(np.abs(x-y)) < 2e-13, label)


def bound(x, lower, upper):
    need(x.a > iv.mpf(lower) and x.b < iv.mpf(upper), str(x))


def digits(x):
    return mp.nstr(mp.mpf(x.mid), 18)


def nuclear(x):
    return sum(np.linalg.svd(x,compute_uv=False))


def channel():
    pp, aa = float(p.mid), float(a.mid)
    eye = np.eye(2)
    t = np.array([[0,1],[1,0]])
    g = np.array([[aa,-pp],[pp,aa]])
    cx = np.block([[eye,0*eye],[0*eye,t]])
    k0,k1 = np.split((np.kron(g.T,eye) @ cx) @ np.kron([[aa],[pp]],eye),2)
    plus, minus = (eye+t)/2, (eye-t)/2
    near(k0,plus+pp**3*minus,"no report Kraus")
    near(k1,-2*aa*pp*minus,"click Kraus")
    near(k0.T@k0+k1.T@k1,eye,"both genuine reports")
    # Conditional golden pairs and an arbitrary reference; no registration is hidden.
    ref = np.eye(3)
    T = np.kron(t,ref)
    K = [np.kron(k,ref) for k in (k0,k1)]
    rng = np.random.default_rng(86)
    for _ in range(7):
        r = rng.normal(size=(6,4)) + 1j*rng.normal(size=(6,4))
        rho = r@r.conj().T;rho /= np.trace(rho)
        reflected = T@rho@T
        delta = rho-reflected
        near(K[0]@delta@K[0].T,pp**3*delta,"all the contrast on the no-click leaf")
        near(K[1]@delta@K[1].T,0*delta,"zero contrast on the click leaf")
        old = sum(k@rho@k.T for k in K)
        near(old,pp*rho+pp**2*reflected,"old reduced state, all histories retained")
        near(nuclear(old-rho),pp**2*nuclear(delta),"achieved displacement")
        near(sum(nuclear(k@delta@k.T) for k in K),pp**3*nuclear(delta),"stopped trace bound")


def fourier():
    sites = np.array(list(product(range(4),repeat=4)),dtype=int)
    unit=np.eye(4,dtype=int)
    edges=np.array([*unit, *(unit[i]-unit[j] for i in range(4) for j in range(i))])
    cos=np.array([1,0,-1,0]); sin=np.array([0,1,0,-1])
    def key(k):
        return (-sum(cos[(edges@k)%4]),tuple(k))
    modes=sorted([tuple(k) for k in sites if tuple(k)<tuple((-k)%4)],key=key)[:64]
    phases=sites@np.array(modes).T%4
    table=np.empty((len(sites),128))
    table[:,0::2]=cos[phases];table[:,1::2]=sin[phases]
    table/=128  # sqrt(256*64)
    perm=np.arange(256).reshape([4]*4).take([2,3,0,1],axis=1).ravel()
    near(np.sum(table*table[perm],axis=1),np.full(256,-1/(16*256)),"true Fourier Gram per SITE")
    return sites,table,perm,cos,sin


def actual_inputs():
    sites,table,perm,cos,sin = fourier()
    pp, aa, A = float(p.mid),float(a.mid),float(amp.mid)
    differences=[]
    for mu in (0,1):
        car=np.zeros((256,16))
        car[:,0]=A*cos[sites[:,mu]]
        car[:,15]=A*sin[sites[:,mu]]
        car[:,1]=aa
        car[:,14]=np.sqrt(pp**2-A**2)
        psi=car[:,:,None]*table[:,None,:]
        shifted=psi[perm,:,:]
        near(np.vdot(psi,psi),1,"full CAR16 by Fourier128 state")
        near(np.vdot(psi,shifted),-(1-2*mu*A**2)/16,"preserved field orbit")
        def event(wave):
            # One actual G on the low CAR bit; direct joint Z read old x1 and CAR mask.
            row=(pp*wave[:,0,:]+aa*wave[:,1,:])[sites[:,1]==0,:]
            return np.vdot(row,row).real
        diff=event(psi)-event(shifted)
        differences.append(diff)
        after=(pp-pp**2)*diff
        near(after,pp**3*diff,"native future on the reported service")
        equal_tag = (sites[:,1]//2 == sites[perm,1]//2)
        near(np.sum(np.einsum("ijk,ijk->i",psi,shifted)*equal_tag),0,"one old address copy kills overlap")
    near(np.array(differences),np.array([0,pp**2*A]),"actual six-bit joint future")


def main():
    channel();actual_inputs()
    gamma = iv.mpf(-1)/16
    b=amp**2
    def motion(lam):
        return p**2*iv.sqrt(1-lam**2)
    w5=motion(gamma);w6=motion(gamma*(1-2*b))
    diff=w6-w5
    bound(diff,"0.0000003705485960806374","0.0000003705485960806375")
    v=p**2*amp
    bound(v,".00425247732254",".00425247732255")
    bound(h*v,".00100387372089",".00100387372090")
    s=2*p*a
    def gap(lam):
        d=iv.sqrt(1-lam**2)+iv.sqrt(1-(lam*(1-2*b))**2)
        return p**2*lam**2*4*b*(1-b)/d
    for n in (1,2,16,64,256):
        need(gap(gamma*s**n) < gap(gamma)*(4*p**3)**n, "raw golden tags uniformly suppress the slope")
    print(json.dumps({
        "full_old_site":256,"full_CAR_masks":16,"true_Fourier_dimension":128,
        "sharp_fraction_of_old_shift_contrast_remaining":digits(h),
        "native_probe_old_data_gates":1,"reachable_mean_equals_reachable_worst_case":True,
        "minimum_old_motion_F5":digits(w5),"minimum_old_motion_F6":digits(w6),
        "F6_minus_F5_strict_interval":["0.0000003705485960806374","0.0000003705485960806375"],
        "real_future_contrast_F5":0,"real_future_contrast_F6_before":digits(v),
        "real_future_contrast_F6_after":digits(h*v),
        "one_old_address_tag_secant":0,
        "canonical_tag_suppression_per_bit_upper_factor":digits(4*p**3),
        "full_generated_writer_and_clock_valued":False,"GR_closed":False
    },indent=2))


if __name__=="__main__":
    main()
