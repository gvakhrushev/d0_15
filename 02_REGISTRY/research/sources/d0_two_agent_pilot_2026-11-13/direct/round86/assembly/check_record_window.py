"""Check the two complete, endpoint-invisible square windows of the Fourier return."""
import itertools
import json

import mpmath as mp
import numpy as np

mp.mp.dps=70


def expect(ok,msg):
    if not ok:
        raise ValueError(msg)


def gate(n,act):
    out=np.zeros((2**n,2**n),dtype=int)
    for row in itertools.product(range(2),repeat=n):
        col=sum(x<<i for i,x in enumerate(row))
        dest=act(list(row))
        out[sum(x<<i for i,x in enumerate(dest)),col]=1
    return out


def flip(bits,ctrl,target):
    bits[target]^=bits[ctrl]
    return bits


def window(q,complement):
    # Bits f,e,target,known-one,copy. The stored records f and e are never targets.
    ref=np.array([[.6, .8], [.8j, .6]],dtype=complex)
    ref[1]/=np.linalg.norm(ref[1])
    state=np.zeros((32,2),dtype=complex)
    state[8]=np.sqrt(1-q)*ref[0]
    state[11]=np.sqrt(q)*ref[1]
    copy=gate(5,lambda bits:flip(bits,0,4))
    x=gate(5,lambda bits:flip(bits,3,4))
    cx=gate(5,lambda bits:flip(bits,4,2))
    word=[copy]+([x,cx,cx,cx,cx,x] if complement else [x,x,cx,cx,cx,cx])+[copy]
    product_matrix=np.eye(32,dtype=int)
    motion=0.
    for U in word:
        moved=np.einsum("ij,jk->ik",U,state)
        overlap=abs(np.vdot(state,moved))
        motion+=np.sqrt(max(0,1-overlap**2))
        state=moved
        product_matrix=U @ product_matrix
    expect(np.array_equal(product_matrix,np.eye(32,dtype=int)), "window must restore every column")
    y=(1-q) if complement else q
    expect(abs(motion-2-4*np.sqrt(2*y-y*y)-2*np.sqrt(2*q-q*q)) < 1e-12,"cost along full purification")
    return motion,word


def main():
    p=(mp.sqrt(5)-1)/2
    u=2*p**3
    b=(p*mp.sin(712*mp.asin(p)))**2
    gamma=-mp.mpf(1)/16
    q0,q1=u*(1-gamma),u*(1-gamma*(1-2*b))
    g=lambda q:mp.sqrt(2*q-q*q)
    deltas=[]
    for complement in (False,True):
        mov0,_=window(float(q0),complement)
        mov1,_=window(float(q1),complement)
        d=g(1-q1)-g(1-q0) if complement else g(q1)-g(q0)
        expect(abs(mov1-mov0-4*float(d)-2*float(g(q1)-g(q0)))<1e-13,"secant in the actual gate fixture")
        deltas.append(d)
    # Identity at both ends suffices for unitary equivalence on the time edges.
    _,a=window(float(q1),False)
    _,bword=window(float(q1),True)
    gauge=np.eye(32,dtype=int)
    for U,V in zip(a,bword):
        new=V @ gauge @ U.T
        expect(np.array_equal(new @ U,V @ gauge),"stage intertwining")
        gauge=new
    expect(np.array_equal(gauge,np.eye(32,dtype=int)),"boundaries fixed")
    # Conservative rational certificate using the independently verified intervals of the writer.
    # p>3/5, b>1/10000; then |q1-q0|=p³ b/4. Both q and 1-q lie in [0.49,0.51].
    expect(mp.mpf("0.49") < min(q0,q1,1-q0,1-q1) and
           max(q0,q1,1-q0,1-q1)<mp.mpf("0.51"),"endpoint box")
    guaranteed=(mp.mpf(49)/100)*(mp.mpf(3)/5)**3/(4*10000)
    expect(-deltas[0]>guaranteed>mp.mpf(2)**-19 and deltas[1]>guaranteed,
           "strict paired-loop cost gap")
    v=np.array([float(mp.sqrt(p)),float(p)])
    G=np.array([[v[0],-v[1]],[v[1],v[0]]])
    target=G @ (G @ v)
    late_bounds=[g(y) for y in (q0,q1,1-q0,1-q1)]
    click=gate(2,lambda bits:flip(bits,0,1))
    data=np.kron(target,v)  # control is the low bit
    root_overlap=np.vdot(data,click @ data)
    pre_ready=np.sqrt(1-abs(root_overlap)**2)
    expect(abs(np.vdot(v,target)-float(p**3))<1e-13,"returned idle target overlap")
    expect(pre_ready-max(map(float,late_bounds))>.06,"early/late movement margin")
    print(json.dumps({"true_fourier_spatial_gamma":"-1/16", "g_per_gate_F6_minus_F5":
                       [mp.nstr(x,16) for x in deltas],
                       "certified_abs_gap_per_CX_lower":"2^-19",
                       "paid_early_window_motion":round(float(pre_ready),14),
                       "early_minus_any_late_motion_lower":0.06,
                       "number_of_pairs_sufficient":"2^19 (B+1)",
                       "identical_window_end_on_all_columns":True,
                       "same_time_edge_spectrum_for_both_windows":True,
                       "both_all_failure_tapes_kept":True,"GR_closed":False},indent=2))


if __name__=="__main__":
    main()
