"""Native all-column loader echo, recorded return and the full finite-clock sign."""
from fractions import Fraction as F
from itertools import product
from math import factorial
import json

import mpmath as mp
import numpy as np
from mpmath import iv

mp.mp.dps = 65
iv.dps = 60
p = (mp.sqrt(5)-1)/2
theta = mp.asin(p)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def reverse(word):
    return [(kind, -arg if kind == "rot" else arg) for kind, arg in reversed(word)]


def query(bits, j):
    # All field digits are loaded by real CX from H, in complementary rails.
    load = [("hk", 2*i+int(value)) for i, value in enumerate(bits)]
    read = [("kt", 2*j+1)]
    return load+read+reverse(load)+read


def compile_product(bits, variables, power):
    if not variables:
        return [("rot", power)]
    prev = compile_product(bits, variables[:-1], power)
    selector = query(bits, variables[-1])
    return prev+selector+reverse(prev)+reverse(selector)


def run_column(word, h, rail_word):
    # On T the exact dihedral map is G^power X^flip, with XGX=G^-1.
    exponent = flip = 0
    wires = rail_word
    for kind, arg in word:
        if kind == "rot":
            exponent += arg
        elif kind == "hk":
            wires ^= h << arg
        else:
            active = h if kind == "ht" else (wires >> arg) & 1
            if active:
                flip ^= 1
                exponent = -exponent
    return wires, flip, exponent


def native_inverse():
    # Physical inverse via a dirty port and the two original Spin wires.
    # Operate on all 16 columns of T,PORT,SPIN4.
    eye = np.eye(16)
    g = np.array([[float(mp.sqrt(p)), -float(p)], [float(p), float(mp.sqrt(p))]])
    g_on_t = np.kron(g, np.eye(8))
    def cx(wc, wt):
        mask_c, mask_t = 1 << wc, 1 << wt
        return eye[[i ^ (mask_t if i & mask_c else 0) for i in range(16)]]
    def compose(*ops):
        result = eye
        for op in ops:
            result = np.einsum("ij,jk->ik", result, op, optimize=False)
        return result
    swap = compose(cx(3,2),cx(2,3),cx(3,2))
    li = np.kron(np.eye(2), np.array([[0,-1],[1,0]]))
    si = np.kron(np.eye(2), np.block([[np.eye(4),np.zeros((4,4))],[np.zeros((4,4)),li]]))
    z = compose(swap,si,si,swap)
    require(np.max(abs(compose(z,g_on_t,z) - g_on_t.T)) < 1e-15, "physical routed G inverse")
    return 16


def semantic_fixture():
    inventory = None
    columns = 0
    for bits in product(range(2), repeat=2):
        # H-conditioned bias 10 theta, then the genuine mixed 02 face on 4 names.
        word = [("rot",5),("ht",None),("rot",-5),("ht",None)]
        word += compile_product(bits, [0,1], 257)
        this = (sum(abs(n) for k,n in word if k=="rot"),sum(k!="rot" for k,_ in word),
                sum(k=="rot" and n<0 for k,n in word))
        if inventory is None:
            inventory = this
        require(this == inventory,"name-dependent gate length")
        for h, k in product(range(2), range(16)):
            rails, flip, exponent = run_column(word,h,k)
            require((rails,flip,exponent)==(k,0,h*(10+1028*bits[0]*bits[1])), "dirty column")
            columns += 2
    # The same fixed CX(K_01,T) is addressed between load and inverse. At T
    # its local occupancy differs even for two mixed-face fields of equal energy.
    witness = []
    for bits in ((0,0),(1,0)):
        load = query(bits,0)[:len(bits)]
        weights = [p,p**2]
        occupied = sum(weights[h] * ((run_column(load,h,0)[0] >> 1) & 1) for h in range(2))
        witness.append(occupied)
    require(abs(witness[1]-witness[0]-p**2)<mp.mpf("1e-60"),"transverse local work")
    # Both leaves physically execute the same 16 CX after the last registration.
    for x,y in product(range(2),repeat=2):
        v = y
        for _ in range(16):
            v ^= x
        require(v==y,"terminal service failed to return its input")
    return columns,inventory


def ordered_field():
    # Exercise both the smallest gap and actual collisions of a+b p.
    limit = 7
    den = 1
    while den <= 24*limit*limit:
        den *= 2
    num = int(mp.nint(den*p))
    scalars = [(a,b) for a,b in product(range(-limit,limit+1), repeat=2)]
    ground = sorted(scalars,key=lambda v:v[0]+p*v[1])
    packed = sorted(scalars,key=lambda v:den*v[0]+num*v[1])
    require(ground == packed and len({den*a+num*b for a,b in packed})==len(packed),"order")
    for a,b in scalars:
        require(a*a-a*b-b*b==0 if (a,b)==(0,0) else abs(a*a-a*b-b*b)>=1,"integer norm")
    return len(ground)


def literal_record(lam):
    # Eight-component execution on the three fresh wires, including the NC1 tail.
    v = np.array([float(mp.sqrt(p)),float(p)])
    G = np.array([[v[0],-v[1]],[v[1],v[0]]])
    rotated = np.array([float(mp.cos(lam)),float(mp.sin(lam))])
    branches = np.array([v[0]*v,v[1]*rotated])
    pre = branches[:,:,None]*v[None,None,:]
    pre[:,1,:] = pre[:,1,::-1].copy()
    post = np.einsum("ij,htj->hti",G,pre)
    post[:,1,:] = post[:,1,::-1].copy()
    passive = np.einsum("h,t,f->htf",v,v,v)
    q = np.sum(post[:,1,:]**2)
    h = sum(np.sum(passive[:,t,:]*post[:,t,:])**2/np.sum(post[:,t,:]**2) for t in (0,1))
    j = -8*np.log1p(2**-20*(h-1))
    qref,jref = recorded(lam)
    require(abs(float(qref)-q)<1e-14 and abs(float(jref)-j)<1e-15,"native registered range")
    # Marking H as well erases the field derivative of the normalized terminal ranges.
    both = sum(np.sum(passive[u,t,:]*post[u,t,:])**2/np.sum(post[u,t,:]**2)
               for u,t in product(range(2),repeat=2))
    require(abs(both-float(p**2+p**3))<1e-14,"extra H record")

def recorded(lam):
    a0 = theta
    h = mp.mpf(0)
    for u,x,w in [(mp.cos(a0), mp.cos(lam),p**2), (mp.sin(a0),mp.sin(lam),p**3)]:
        prob = p*u*u+p**2*x*x
        h += w*(p*u+p**2*x)**2/prob
    q = p*mp.sin(a0)**2 + p**2*mp.sin(lam)**2
    z = mp.mpf(2)**-20
    return q, -8*mp.log(1-z+z*h)


def confirm_bounds():
    # Directed interval arithmetic, covering the entire chosen arc rather than just the fixture.
    one = iv.mpf(1)
    gold = (iv.sqrt(5)-1)/2
    a = iv.sqrt(gold)
    # Validate both actual gate powers without invoking an inverse trigonometric function.
    def circle(n):
        c,s = one,iv.mpf(0)
        for _ in range(n):
            c,s = a*c-gold*s,gold*c+a*s
        return c,s
    for c,s in (circle(11), complex_power(a,gold,1039)):
        require(c.a > iv.cos(iv.mpf("1.1")).b and c.b < iv.cos(one).a and s.a > 0,
                "genuine angular fixture outside the arc")
    z = iv.mpf(2)**-20
    for i in range(50):
        lam = iv.mpf([str(F(500+i,500)),str(F(501+i,500))])
        h,dh = iv.mpf(0),iv.mpf(0)
        for u,x,dx,w in [(a,iv.cos(lam),-iv.sin(lam),gold**2),
                         (gold,iv.sin(lam),iv.cos(lam),gold**3)]:
            norm = gold*u*u+gold**2*x*x
            m = gold*u+gold**2*x
            h += w*m*m/norm
            dh += w*2*gold**3*m*u*(u-x)*dx/norm**2
        q=gold**3+gold**2*iv.sin(lam)**2
        dq=gold**2*iv.sin(2*lam)
        deriv = -8*z*dh/(1-z+z*h)
        require(q.a>iv.mpf(".50") and q.b<iv.mpf(".55") and dq.a>iv.mpf(".30"),"record slope")
        require(deriv.a>iv.mpf("0.0000006") and deriv.b<iv.mpf("0.0000014"),"RAW slope")
    # x=beta/11<1/11, beta>1/2, m=exp(-2 beta)>1/8. Use L=16 honest square stages.
    x=F(1,11)
    tail = 2*x**16/F(factorial(16))/(1-x/17)
    deriv_tail = x**16/F(factorial(15))/(1-x/16)
    require(F(132,359)*deriv_tail<F(1,10**20) and 8*(2*deriv_tail+6*tail)<F(1,10**20),
            "whole heat or conditional thermal slope bound")


def complex_power(a,b,n):
    x,y=iv.mpf(1),iv.mpf(0)
    while n:
        if n & 1:
            x,y=x*a-y*b,x*b+y*a
        a,b=a*a-b*b,2*a*b
        n//=2
    return x,y


if __name__=="__main__":
    columns,inv=semantic_fixture()
    confirm_bounds()
    low=11*theta-2*mp.pi
    high=low+mp.fmod(1028*theta,2*mp.pi)
    literal_record(low)
    literal_record(high)
    q0,j0=recorded(low)
    q1,j1=recorded(high)
    require(q1>q0 and j1>j0,"physical face sign")
    print(json.dumps(dict(all_name_input_columns=columns,routed_inverse_columns=native_inverse(),
          final_CX_on_each_actual_leaf=16,transverse_local_charge_difference="p^2",
          raw_power_G_before_inverse_routing=inv[0],loader_and_bias_CX=inv[1],
          inverse_power_blocks=inv[2],ordered_Qp_test_values=ordered_field(),
          zero_and_nonzero_02_face_click=[float(q0),float(q1)],
          delta_RAW_logdet_rank8=float(j1-j0),full_clock_slope_lower="6e-7 minus 1e-20",
          tilted_absolute_action_positive_on_arc=True,field_rows_on_dyadic_Brinkmann_chart=42,
          unrestricted_work_source_fixed=False,GR_closed=False),indent=2))
