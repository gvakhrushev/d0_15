"""Forward F5/F6 at L=4, exact finite record recursion and actual gate contrasts."""
from itertools import product
import json
import math

import mpmath as mp
import numpy as np


mp.mp.dps = 65
p = (mp.sqrt(5)-1)/2
a = mp.sqrt(p)
theta = mp.asin(p)
A = p*mp.sin(712*theta)
u = 2*p**3
logphi = mp.log(1/p)
D = ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
     (-1,1,0,0),(-1,0,1,0),(0,-1,1,0),(-1,0,0,1),
     (0,-1,0,1),(0,0,-1,1))
C = (1,0,-1,0)


def require(ok, description):
    if not ok:
        raise AssertionError(description)


def same(x, y, tol=1e-12):
    require(np.allclose(x, y, rtol=0., atol=tol), "numeric identity")


def output(x):
    return float(mp.nstr(mp.mpf(x), 13))


def entropy(weights):
    return -sum(z*mp.log(z) for z in weights if z)/logphi


def factory_records():
    """A subroutine is (chance to finish, expected printed length, full H).
    Each later subroutine physically runs only on a completed former one.
    """
    def unit(probs, marks, success):
        return success, sum(w*l for w,l in zip(probs, marks)), entropy(probs)

    def after(first, second):
        s, cost, info = first
        v, c, i = second
        return s*v, cost+s*c, info+s*i

    def repeat(op, n):
        result = (1, 0, 0)
        for _ in range(n):
            result = after(result, op)
        return result

    def capped(s, cycles, is_x=False):
        if is_x:
            probs, costs = (1-s, s/2, s/2), (2,3,3)
        else:
            probs, costs = (1-s, s), (1,2)
        _, cost, info = unit(probs, costs, s)
        visits = sum((1-s)**i for i in range(cycles))
        return 1-(1-s)**cycles, visits*cost, visits*info

    resource = capped(2*p**3, 16)
    cz = capped(4*p**3, 32)
    ccz = capped(16*p**9, 32)
    had = after(cz, capped(4*p**3, 32, True))
    tof = after(after(had, ccz), had)
    # 12 Toffoli for the base (4 Gray swaps). 9 before/after the low rotation.
    # Five Toffoli and a CCZ in the central low-word, then 2 high signs.
    units = [tof]*12 + [tof]*9 + [tof,tof,ccz,tof,tof,tof] + [tof]*9
    units += ([tof,tof,ccz,tof,tof])*2
    require(sum(x is tof for x in units)==43 and sum(x is ccz for x in units)==3,
            "source factory order/count")
    ready, length, info = repeat(resource, 86)
    # Sum first-abort masses on the entire ordered resource / square-gate tree.
    survival, abort_mass = mp.mpf(1), mp.mpf(0)
    for op in [resource]*86 + units:
        abort_mass += survival*(1-op[0])
        survival *= op[0]
    for op in units:
        ready, length, info = after((ready, length, info), op)
    require(abs(survival-ready)<mp.mpf('1e-60') and
            abs(survival+abort_mass-1)<mp.mpf('1e-60'), "full stopped mass")
    require(abs(ready-mp.mpf('0.97334116981598111827611478021477781006060427421787145'))
            <mp.mpf('1e-53'), "source short readiness")
    return ready, length, info


def fourier_reference():
    sites = list(product(range(4),repeat=4))
    pairs = [k for k in sites if k<tuple(-x%4 for x in k)]
    dot = lambda x, y: sum(i*j for i,j in zip(x,y))
    pairs.sort(key=lambda k:(-sum(C[dot(k,d)%4] for d in D),k))
    selected = pairs[:64]
    ref = np.zeros((256,128),dtype=np.int32)
    for row,site in enumerate(sites):
        for j,k in enumerate(selected):
            phase=dot(k,site)%4
            ref[row,2*j+(phase%2)]=1 if phase<2 else -1
    same(ref.T@ref,128*np.eye(128))
    chars = [sum((-1)**k[axis] for k in selected) for axis in range(4)]
    require(chars==[-16,-4,-4,-6], "original Fourier half-translation")
    t = [sites.index((x[0],(x[1]+2)%4,x[2],x[3])) for x in sites]
    require(np.all(np.einsum('ij,ij->i',ref,ref[t])==chars[1]), "all local overlaps")
    # Both original CAR/Fourier test amplitudes before the square sensor.
    for mu in (0,1):
        car = np.zeros((256,16))
        for j,site in enumerate(sites):
            n=site[mu]
            car[j,1]=float(a)
            car[j,14]=-float(p*mp.cos(712*theta))
            car[j,0]=float(A)*C[n]
            car[j,15]=float(A)*C[(n-1)%4]
        prod=np.einsum('ij,ij->i',ref,ref[t])*np.einsum('ij,ij->i',car,car[t])
        same(np.sum(prod)/(256*64), float(mp.mpf(chars[1])/64*(1-2*A**2*mu)))
    return chars


def inverse(word):
    return [(gate, -v if gate=="G" else v) for gate,v in reversed(word)]


def factory_word(k):
    if k==0:
        return [("G",1)]
    w = factory_word(k-1)
    return [("C",k-1)]+inverse(w)+[("C",k-1)]+w


def early_microstep():
    G = np.array([[float(a),-float(p)],[float(p),float(a)]])
    X = np.array([[0.,1.],[1.,0.]])
    # H(b=0) generates a balanced b. c is the middle CAR bit after the swaps.
    # Factory control slots 0=c, 1=SITE low bit, 2=b, 3=known unit.
    raw=[("G",-1)]*4 + factory_word(3)
    word=[]
    for gate,value in raw:
        word.extend([("C",3),("G",1),("C",3)] if (gate,value)==("G",-1)
                    else [(gate,value)])
    onset=word.index(("C",1))
    require(onset+1==20, "first actual changed SITE address")
    proj = np.diag([1.,-1.])
    basismoves, xx, zz = {},0.,0.
    for c,b in product(range(2),repeat=2):
        w=(float(p) if c==0 else float(p**2))/2
        psi=np.array([1.,0.])
        for gate,q in word[:onset]:
            if gate=="G": psi=G@psi
            elif {0:c,2:b,3:1}[q]: psi=X@psi
        xx+=w*float(psi@X@psi)
        zz+=w*float(psi@proj@psi)
        basismoves[c,b]=psi
    same(xx,float(-mp.sin(8*theta)*(p+p**2*mp.cos(4*theta))))
    same(zz,float(-p**2*mp.sin(8*theta)*mp.sin(4*theta)))
    vectors=[]
    for mu in (0,1):
        state=np.zeros((2,2,2,2,2))
        for s0,s1,c,b in product(range(2),repeat=4):
            amp=math.sqrt((float(p) if c==0 else float(p**2))/8)
            psi=basismoves[c,b]
            state[s0,s1,c,b]=amp*((X@psi) if (s0,s1)[mu] else psi)
        vectors.append(state)
        diag=(np.array([1.,-1.])[:,None,None,None,None]*
              np.array([1.,-1.])[None,None,None,None,:])
        same(np.sum(diag*state**2), zz if mu==0 else 0)
    overlap=float(np.vdot(*vectors).real)
    same(overlap,(1+xx)/2)
    return onset+1, zz, overlap


def probe_motion(lam):
    # Full two-dimensional occupied subspace of SITE,CAR,oldRIGHT in eigenbasis
    # of the physical spatial X. Probe before NC1, with a true Golden tail.
    g = np.array([[float(a),-float(p)],[float(p),float(a)]])
    x = np.array([[0.,1.],[1.,0.]])
    v=np.array([float(a),float(p)])
    ket=np.einsum('i,j,k->ijk',
        np.sqrt([(1+float(lam))/2,(1-float(lam))/2]),v,v)
    steps=[]
    def act(new):
        nonlocal ket
        ov=np.vdot(ket,new).real
        steps.append(math.sqrt(max(0.,1-ov**2)))
        ket=new
    state=ket.copy()
    state[1,1]*=-1  # controlled SITE shift
    act(state)
    for matrix in [x,g,x]:
        act(np.einsum('hi,aij->ahj',matrix,ket))
    for gate in ('CX','G','CX'):
        if gate=="CX":
            new=ket.copy()
            new[:,1,:]=ket[:,1,::-1]
        else:
            new=np.einsum('ti,aji->ajt',g,ket)
        act(new)
    same(ket[:,1,1],0)
    prob=float(np.sum(ket[:,1]**2))
    same(prob,float(u*(1-lam)))
    return steps, prob


def main():
    gamma, length, info = factory_records()
    chars = fourier_reference()
    pos, zz, overlap = early_microstep()
    kappa = mp.mpf(chars[1])/64
    q0,q1=(u*(1-kappa*(1-2*A**2*mu)) for mu in (0,1))
    motion0,_=probe_motion(kappa)
    motion1,_=probe_motion(kappa*(1-2*A**2))
    delta_code = gamma*(q1-q0)
    delta_info = gamma*(entropy((q1,1-q1))-entropy((q0,1-q0)))
    def motion_list(lam):
        q=u*(1-lam)
        ox=2*a*p
        overlaps=[p+p**2*lam, ox*lam, a, ox*p**3*(lam-1),
                  1-q+q*ox, a, 1-q]
        return [mp.sqrt(1-v**2) for v in overlaps]

    def pvm_motion(q):
        return (1-q)*mp.sqrt(q)+q*mp.sqrt(1-q)

    exact0=motion_list(kappa)
    exact1=motion_list(kappa*(1-2*A**2))
    same(motion0,list(map(float,exact0)))
    same(motion1,list(map(float,exact1)))
    diff=[y-x for x,y in zip(exact0,exact1)]
    pvm_delta=gamma*(pvm_motion(q1)-pvm_motion(q0))
    # Certify the sign without trusting the point evaluation or cancellation.
    iv=mp.iv
    iv.dps=60
    pv=(iv.sqrt(5)-1)/2
    av=iv.sqrt(pv)
    amp=pv*iv.sin(712*iv.atan2(pv,av))
    rv=1-(1-2*pv**3)**16
    czv=1-(1-4*pv**3)**32
    ccv=1-(1-16*pv**9)**32
    gv=rv**86*(czv**4*ccv)**43*ccv**3
    lv0=-iv.mpf(1)/16
    lv1=lv0*(1-2*amp**2)
    def certified(lam):
        q=2*pv**3*(1-lam)
        x=2*av*pv
        overlaps=(pv+pv**2*lam, x*lam, av, x*pv**3*(lam-1),
                  1-q+q*x, av, 1-q)
        motion=sum(iv.sqrt(1-v**2) for v in overlaps)
        measure=(1-q)*iv.sqrt(q)+q*iv.sqrt(1-q)
        ent=-(q*iv.log(q)+(1-q)*iv.log(1-q))/iv.log(1/pv)
        return q-ent, motion, measure
    costs0=certified(lv0)
    costs1=certified(lv1)
    delta_abs, delta_work, delta_measure=(gv*(y-x) for x,y in zip(costs0,costs1))
    require(iv.mpf('-7.218e-6')<delta_abs<iv.mpf('-7.216e-6'), "interval price")
    require(iv.mpf('-7.770e-6')<delta_work<iv.mpf('-7.768e-6'), "interval gate motion")
    require(delta_work+delta_measure<0, "gate and projected-branch motion sign")
    receipt={
      "status": "PASS", "L":4, "true_Fourier_half_shift_numerators_over_64":chars,
      "short_writer_one_success":output(gamma),
      "source_factory_expected_printed_symbols":output(length),
      "source_factory_full_record_entropy_base_phi":output(info),
      "first_axis_addressed_CX_in_CCZ_attempt":pos,
      "first_gate_fixed_address_ZZ_contrast":output(zz),
      "first_gate_F5_F6_root_overlap":output(overlap),
      "first_gate_F5_F6_root_trace_distance":output(math.sqrt(1-overlap**2)),
      "F5_conditional_click_original_Fourier128":output(q0),
      "F6_conditional_click_original_Fourier128":output(q1),
      "full_forward_delta_printed_length_F6_minus_F5":output(delta_code),
      "full_forward_delta_record_entropy_F6_minus_F5":output(delta_info),
      "full_forward_delta_printed_length_minus_CQ":output(delta_code-delta_info),
      "paid_square_trace_distances_delta_given_success":[output(z) for z in diff],
      "all_forward_delta_sum_observed_square_trace_distances":output(gamma*sum(diff)),
      "extra_conditional_PVM_trace_distance_delta":output(pvm_delta),
      "full_square_plus_terminal_PVM_trace_distance_delta":output(gamma*sum(diff)+pvm_delta),
      "all_failures_retained":True, "full_Book03_selected":False, "GR_closed":False,
    }
    print(json.dumps(receipt,indent=2))


if __name__=="__main__":
    main()

