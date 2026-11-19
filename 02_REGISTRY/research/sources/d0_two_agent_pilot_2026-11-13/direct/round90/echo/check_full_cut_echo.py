"""The actual passive closure, its birth complements and both Hodge degrees."""
import json
import math

import numpy as np


P = (math.sqrt(5)-1)/2
V = np.array([[math.sqrt(P)], [P]])
Z = 2**-20


def mul(a, b):
    return np.einsum("ij,j...->i...", a, b)


def check(ok, message):
    if not ok:
        raise ValueError(message)


def equal(a, b, message):
    check(np.allclose(a, b, atol=2e-12, rtol=0), message)


def birth(d):
    return np.kron(np.eye(d), V)


def cx(bits, control, target):
    out = np.zeros((2**bits, 2**bits))
    for x in range(2**bits):
        out[x ^ ((((x >> (bits-control-1)) & 1) << (bits-target-1))), x] = 1
    return out


def clock(stages):
    dims = [f.shape[1] for f in stages]
    offs = list(np.cumsum([0]+dims))
    embedded = [np.eye(dims[-1])]
    projectors = [np.eye(dims[0])]
    passive = []
    for i, f in enumerate(stages[:-1]):
        passive.append(np.eye(dims[i]) if dims[i]==dims[i+1] else birth(dims[i]))
        projectors.append(np.eye(dims[i+1])-mul(passive[-1],passive[-1].T))
    for inc in reversed(passive):
        embedded.insert(0, mul(embedded[0],inc))
    r = np.vstack([mul(proj,inc.T) for proj,inc in zip(projectors, embedded)])
    equal(mul(r.T,r),np.eye(dims[-1]),"terminal packing on every final column")
    t = np.zeros((offs[-1],offs[-1]))
    for j, f in enumerate(stages[:-1]):
        t[offs[j+1]:offs[j+2],offs[j]:offs[j+1]] = f
    t[:,offs[-2]:] += mul(r,stages[-1])
    equal(mul(t.T,t),np.eye(offs[-1]),"complete G5")
    full = np.eye(dims[0])
    for f in stages:
        full=mul(f,full)
    return t,mul(embedded[0].T,full),full


def heat(t):
    # G13/G14 on K(9,11,13), summing both Hodge degrees and null modes.
    group = np.repeat(np.arange(3), [9,11,13])
    adjacency = (group[:,None]!=group[None,:]).astype(float)
    cs = 1/(2+adjacency.sum(axis=1))
    bs = adjacency*np.sqrt(cs[:,None]*cs[None,:])
    total = 359*len(t)
    for cosine in np.linalg.eigvalsh(t+t.T):
        eigenvalues = np.linalg.eigvalsh(np.eye(33)-bs-np.diag(cs*cosine))
        total += 2*sum(np.exp(-2*P*P*eigenvalues))
    return math.log(total)/(2*P*P)


def determinant(c):
    fac = (1-Z)*np.eye(len(c))+Z*mul(c.T,c)
    return -np.linalg.slogdet(fac)[1]


def fixed_square():
    ua, ub = cx(2,0,1), cx(2,1,0)
    q = mul(ua.T,ub)
    plus, minus = [], []
    for stages, drive in ((plus,ua),(minus,ub)):
        # True early Golden birth, a noncommuting meter, real inverse, late pointer service.
        u = np.kron(drive,np.eye(2))
        stages.extend([birth(4),u,cx(3,0,2),u.T,birth(8),cx(4,2,3)])
    tp, cp, fp = clock(plus)
    tm, cm, fm = clock(minus)
    # Layer changes of coordinates map the minus clock into the plus clock.
    gauges = [q,np.kron(q,np.eye(2)),np.eye(8),np.eye(8),
              np.kron(q,np.eye(2)),np.kron(q,np.eye(4))]
    cuts = np.cumsum([0]+[len(x) for x in gauges])
    g = np.zeros(tm.shape)
    for i, block in enumerate(gauges):
        g[cuts[i]:cuts[i+1],cuts[i]:cuts[i+1]]=block
    equal(mul(g,tm),mul(tp,g),"intertwines entire closed clock")
    equal(cm,mul(mul(q.T,cp),q),"cold contraction on all old columns")
    hp,hm = heat(tp),heat(tm)
    equal(hp,hm,"both Hodge terms jointly")
    equal(determinant(cp),determinant(cm),"full determinant")
    # Literal old input |01>, not the full cut. Late archive is a genuine born head.
    omega = np.eye(4)[:,1]
    prob = [sum(mul(full,omega)[1::2]**2) for full in (fp,fm)]
    jp,jm = [determinant(np.array([[float(omega@mul(c,omega))]])) for c in (cp,cm)]
    check(abs(prob[0]-prob[1])>0.01 and abs(jp-jm)>1e-9,
          "protected terminal report moves; preparation changes determinant")
    return {"full_clock_dimension":len(tp), "archive_probabilities":[round(x,10) for x in prob],
            "prepared_rank_one_J_difference":round(jp-jm,14)}


def inside_birth():
    ua,ub = cx(2,0,1),cx(2,1,0)
    ts,cs = [],[]
    for u in (ua,ub):
        t,c,_ = clock([u,birth(4),np.kron(ua,np.eye(2)),np.kron(u.T,np.eye(2))])
        ts.append(t)
        cs.append(c)
    equal(determinant(cs[0]),determinant(cs[1]),"old root determinant invariant")
    powers = [np.eye(len(t)) for t in ts]
    for n in range(1,13):
        powers = [mul(a,b) for a,b in zip(powers,ts)]
        value=np.trace(powers[0])-np.trace(powers[1])
        equal(value,6 if n%2==0 and (n//2)%3 else 0,"all short complement moments")
    delta = heat(ts[0])-heat(ts[1])
    check(delta>1e-7,"concrete positive complete Hodge difference")
    return {"actual_CX_clock_dimension":len(ts[0]), "trace_square_gap":6,
            "both_degrees_H_difference":round(delta,12)}


def teleport_meter():
    # Registers after bitwise CX and two SWAPs: original physical A now
    # holds output, B holds the Z flags, C holds the spent X flags.
    r = 4
    g = np.array([[math.sqrt(P),-P],[P,math.sqrt(P)]])
    meter = cx(2,0,1)
    omega = np.kron(V[:,0],V[:,0])
    clicks = []
    for move in (g,g.T):
        drive = np.kron(move,np.eye(2))
        state = np.zeros((r,r,r))
        data = mul(drive,omega)
        for a in range(r):
            for b in range(r):
                for out in range(r):
                    state[out,b^a,a] += data[a]*meter[out,b]/math.sqrt(r)
        state = np.einsum("ij,jbc->ibc",drive.T,state)
        for z in range(r):
            for x in range(r):
                row=np.array([(-1)**bin(x&a).count("1") for a in range(r)])/math.sqrt(r)
                branch = mul(state[:,z,:],row)
                equal(branch@branch,1/r**2,"all actual joint Bell labels are uniform")
                if not (z or x):
                    exact = mul(drive.T,mul(meter,data))
                    equal(branch, exact/r,"literal physical output after echo")
                    clicks.append(float(sum(exact[1::2]**2)))
    check(abs(clicks[1]-clicks[0])>0.1,"retained report on echo teleporter")
    # Certified two-test X signs with an independent uninformative abort.
    s = 4*P**3
    equal(1-s,P**6,"reported abort of the true two-test X")
    return {"success_given_offline_resource":round(s*s/(r*r),12),
            "unconditioned_bell_label_masses":1/r**2,
            "conditional_meter_probabilities":[round(x,10) for x in clicks]}


def cut_mismatch():
    # A90's two opposite full Julia outputs have the following exact protected slots.
    lower = [math.sqrt(2)*.5*32*math.sqrt(n)/math.sqrt(65536) for n in (8,16)]
    equal(lower,[.25,1/(2*math.sqrt(2))],"actual prepared-input leakage lower bounds")
    return [round(x,10) for x in lower]


print(json.dumps({"early_and_late_births":fixed_square(),
                  "deferred_physical_teleporter":teleport_meter(),
                  "A90_ray_mismatch_per_step_on_8_or_16_sites":cut_mismatch(),
                  "birth_inside_echo":inside_birth(),
                  "GR_closed":False},indent=2,sort_keys=True))
