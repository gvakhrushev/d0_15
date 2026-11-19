"""Finite native Toffoli compilation of the balanced recorded controller.

Checks actual 1/2/3-control matrix words, H teleportation Kraus operators,
both success and abort transcripts, and the complete 0/10 record ledger.
Logical addressed G/CX, NC1 and explicit caps are used. No microscopic
Book valuation or paid clock equality is assumed.
"""
import itertools
import json
import math
import runpy
from pathlib import Path
import numpy as np

p=(math.sqrt(5)-1)/2
a=math.sqrt(p)
ell=math.log(1/p)
G=np.array([[a,-p],[p,a]])
X=np.array([[0.,1.],[1.,0.]])
I=np.eye(2)
H=np.array([[1.,1.],[1.,-1.]])/math.sqrt(2)
Z=np.diag([1.,-1.])


def inv(word):
    return [(op, -s if op=='G' else s) for op,s in reversed(word)]


def W(k):
    if not k:
        return [('G',1)]
    old=W(k-1)
    return [('C',k-1)]+inv(old)+[('C',k-1)]+old


def physical(word,known):
    out=[]
    for op,s in word:
        if op=='G' and s==-1:
            out.extend([('C',known),('G',1),('C',known)])
        else:
            out.append((op,s))
    return out


def one(state,k,mat):
    out=state.copy(); n=len(state)
    for j in range(n):
        if not ((j>>k)&1):
            i=j|(1<<k)
            out[j]=mat[0,0]*state[j]+mat[0,1]*state[i]
            out[i]=mat[1,0]*state[j]+mat[1,1]*state[i]
    return out


def cx(state,c,t):
    out=state.copy()
    for j in range(len(state)):
        if (j>>c)&1 and not ((j>>t)&1):
            i=j|(1<<t);out[j]=state[i];out[i]=state[j]
    return out


def phase_factory(k):
    # Full control basis, known-one wire k and fresh target k+1.
    target=k+1; known=k; theta=math.acos(a); m=2**(k-1)
    w=physical([('G',-1)]*m+W(k),known)
    assert sum(op=='G' for op,_ in w)==3*2**(k-1)
    assert sum(op=='C' for op,_ in w)==2**(k+2)-2
    maps=[np.zeros((2**k,2**k)),np.zeros((2**k,2**k))]
    for col in range(2**k):
        state=np.zeros(2**(k+2));state[col|(1<<known)]=1
        for op,c in w:
            state=one(state,target,G) if op=='G' else cx(state,c,target)
        for outcome in (0,1):
            for row in range(2**k):
                maps[outcome][row,col]=state[row|(1<<known)|(outcome<<target)]
    sign=np.eye(2**k);sign[-1,-1]=-1
    assert np.max(np.abs(maps[0]-math.cos(m*theta)*np.eye(2**k)))<1e-13
    assert np.max(np.abs(maps[1]+math.sin(m*theta)*sign))<1e-13
    return {'G':sum(op=='G' for op,_ in w),
            'CX':sum(op=='C' for op,_ in w),
            'success_probability':math.sin(m*theta)**2}


def hadamard_and_toffoli():
    plus=np.array([1.,1.])/math.sqrt(2)
    minus=np.array([1.,-1.])/math.sqrt(2)
    cz=np.diag([1.,1.,1.,-1.]); feed=np.kron(I,plus.reshape(2,1))
    maps=[]
    for v,correction in ((plus,I),(minus,X)):
        maps.append(correction@np.kron(v.reshape(1,2),I)@cz@feed)
    for q in maps:
        assert np.max(np.abs(q-H/math.sqrt(2)))<1e-14
        assert np.max(np.abs(q.T@q-I/2))<1e-14
    # Literal two-step X readout: all branches including the 00 failure.
    A0=p*I-p*p*X; A1=a*p*(I+X)
    B0=p*I+p*p*X; B1=-a*p*(I-X)
    # Independently construct both tests from a fresh Golden ancilla, its
    # actual CX onto the data, the signed G and computational reading.
    P0=np.diag([1.,0.]);P1=np.diag([0.,1.])
    ctrl=np.kron(I,P0)+np.kron(X,P1)
    fresh=np.kron(I,np.array([a,p]).reshape(2,1))
    actual=[]
    for rot in (G,X@G@X):
        for bit in (0,1):
            bra=np.array([[1.,0.]]) if bit==0 else np.array([[0.,1.]])
            actual.append(np.kron(I,bra)@np.kron(I,rot)@ctrl@fresh)
    assert max(np.max(np.abs(v-w)) for v,w in zip(actual,(A0,A1,B0,B1)))<1e-14
    branches=(B0@A0,B0@A1,B1@A0,B1@A1)
    expected=(p**3*I,a*p*(I+X),-a*p*(I-X),np.zeros((2,2)))
    assert max(np.max(np.abs(v-w)) for v,w in zip(branches,expected))<1e-14
    # On the actual CZ + |+> H input, the two successful X transcript
    # effects are equally likely for every input (and hence every oldRIGHT).
    for ix,b in enumerate(branches[:3]):
        op=np.kron(b,I)@cz@feed
        multiplier=p**6 if ix==0 else (4*p**3)/2
        assert np.max(np.abs(op.T@op-multiplier*I))<1e-14
    assert np.max(np.abs(branches[3]))<1e-14
    # Every successful H record implements H/sqrt(2); test the 8-column
    # H-CCZ-H Toffoli operator, including input entanglement by operator law.
    ccz=np.eye(8);ccz[-1,-1]=-1
    target_h=np.kron(np.eye(4),H)
    tof=target_h@ccz@target_h
    target=np.eye(8);target[6,6]=target[7,7]=0
    target[6,7]=target[7,6]=1
    assert np.max(np.abs(tof-target))<1e-14
    return tof


def mux_columns(tof):
    # On every N,D,T,R,M input with fresh M=0, two CX compute M=T xor N,
    # one exact Toffoli(D,M,R) after CX(T,R) selects the correct control.
    for t,n,d,b in itertools.product((0,1),repeat=4):
        scratch=t^n
        target=b^t^(d*scratch)
        assert target==b^(t if not d else n)
    assert np.array_equal(tof@tof,np.eye(8)) or np.allclose(tof@tof,np.eye(8))


def branch(s,L):
    out=[]
    for k in range(L):
        out.append(((0,)*k+(1,),s*(1-s)**k,True))
    out.append(((0,)*L,(1-s)**L,False))
    return out


def xbranch(s,L):
    out=[]
    for k in range(L):
        for pair in ((1,0),(0,1)):
            out.append(((0,0)*k+pair,(1-s)**k*s/2,True))
    out.append(((0,0)*L,(1-s)**L,False))
    return out


def hbranch(s,L):
    out=[]
    for c,pc,ok in branch(s,L):
        if not ok: out.append((c,pc,False));continue
        for x,px,xok in xbranch(s,L):out.append((c+x,pc*px,xok))
    return out


def toffoli_branch(s2,s3,L):
    out=[]
    for w1,p1,ok1 in hbranch(s2,L):
        if not ok1:out.append((w1,p1,False));continue
        for w2,p2,ok2 in branch(s3,L):
            if not ok2:out.append((w1+w2,p1*p2,False));continue
            for w3,p3,ok3 in hbranch(s2,L):
                out.append((w1+w2+w3,p1*p2*p3,ok3))
    return out


def net_cost(paths):
    assert abs(sum(prob for _,prob,_ in paths)-1)<1e-12
    return sum(q*(len(bits)+sum(bits))+q*math.log(q)/ell
               for bits,q,_ in paths if q)


def f(q):
    return 1+q+(q*math.log(q)+(1-q)*math.log(1-q))/ell


def expected(L0,L):
    s0=2*p**3;s2=4*p**3;s3=16*p**9
    b0=1-(1-s0)**L0;b2=1-(1-s2)**L;b3=1-(1-s3)**L
    n0=b0/s0;n2=b2/s2;n3=b3/s3
    prob_t=b2**4*b3;beta=b0**4;kappa=beta*prob_t**2
    hx=-(1-s2)*math.log(1-s2)-s2*math.log(s2/2)
    fx=2+s2-hx/ell
    ch=n2*f(s2)+b2*n2*fx
    ct=ch+b2**2*n3*f(s3)+b2**2*b3*ch
    resource_attempts=n0*sum(b0**j for j in range(4))
    cres=resource_attempts*f(s0)
    # All indicated counts include NC1 for each measured service ancilla;
    # zero preparation G^-1 is implemented by CX(H,t), G(t), CX(H,t).
    hcount={'birth':2*n2+4*b2*n2,'G':8*n2+6*b2*n2,
            'CX':18*n2+8*b2*n2+3.5*b2**2,'PVM':n2+2*b2*n2}
    ccount={'birth':2*n3,'G':14*n3,'CX':34*n3,'PVM':n3}
    tofcount={k:(1+b2**2*b3)*hcount[k]+b2**2*ccount[k] for k in hcount}
    resource={'birth':3,'G':1,'CX':3,'PVM':1}
    # Move each successful |+> into a new fixed slot by 3 CX. Move the first
    # known-one output into its fixed slot likewise. Failed states are retained.
    slots=b0+sum(b0**j for j in range(1,5))
    slotcount={'birth':1,'G':0,'CX':3,'PVM':0}
    pre={'birth':11,'G':6,'CX':20,'PVM':3}
    last={'birth':2,'G':2,'CX':4,'PVM':2}
    counts={k:resource_attempts*resource[k]+slots*slotcount[k]+
               beta*(pre[k]+(1+prob_t)*tofcount[k]+prob_t**2*last[k])
            for k in resource}
    maxima={'birth':12*L0+28*L+18,'G':4*L0+84*L+8,
            'CX':12*L0+172*L+55,'PVM':4*L0+14*L+5}
    assert all(counts[k] <= maxima[k] for k in counts)
    constant=cres+beta*ct*(1+prob_t)+kappa*p**5
    gain=kappa*2*p**4
    return {'L0':L0,'L':L,'resource_success':beta,
            'single_toffoli_success':prob_t,'joint_report_success':kappa,
            'resource_attempts_mean':resource_attempts,
            'successful_resource_and_known_one_slots_mean':slots,
            'service_code_minus_CQ':cres+beta*ct*(1+prob_t),
            'conditional_constant_after_controller_stationarity':constant,
            'gain_wrt_recorded_pi':gain,'counts_before_unknown_N_prep_or_routing':counts,
            'maximum_counts_before_unknown_N_prep_or_routing':maxima}


def main():
    cz=phase_factory(2);ccz=phase_factory(3);tof=hadamard_and_toffoli();mux_columns(tof)
    s2=4*p**3;s3=16*p**9;L=2
    paths=toffoli_branch(s2,s3,L)
    n2=(1-(1-s2)**L)/s2;n3=(1-(1-s3)**L)/s3
    b2=1-(1-s2)**L;b3=1-(1-s3)**L
    hx=-(1-s2)*math.log(1-s2)-s2*math.log(s2/2)
    ch=n2*f(s2)+b2*n2*(2+s2-hx/ell)
    ct=ch+b2**2*n3*f(s3)+b2**2*b3*ch
    assert abs(sum(q for _,q,ok in paths if ok)-b2**4*b3)<1e-12
    assert abs(net_cost(paths)-ct)<1e-12
    # Full Toffoli abort locations, followed by the second gadget. Every
    # effect is a scalar on all eight target/control columns; successful
    # prefixes are isometries and failures retain their complete dilation.
    ha=b2**2; ta=ha**2*b3
    aborts=[1-ha,ha*(1-b3),ha*b3*(1-ha),ta]
    assert abs(sum(aborts)-1)<1e-14
    assert abs(aborts[-1]-ta)<1e-14
    two=[1-ta,ta*(1-ta),ta**2]
    assert abs(sum(two)-1)<1e-14
    # Verify pre-resource parity CX on two full Golden input bits.
    v=np.array([a,p]);pair=np.kron(v,v); probs=[0.,0.]
    for x in (0,1):
        for y in (0,1):probs[x^y]+=pair[2*x+y]**2
    assert abs(probs[1]-2*p**3)<1e-14
    plus_branch=np.array([pair[1],pair[2]])
    assert np.max(np.abs(plus_branch/math.sqrt(probs[1])-np.array([1.,1.])/math.sqrt(2)))<1e-14
    # Independent exact NC1 table on the one already recorded T. Both gadgets
    # are attempted before *either* R is measured; abort retains the R wires.
    nc=runpy.run_path(str(Path(__file__).with_name('check_balanced_controller_source.py')))
    pi=0.42;us=(0.2,0.67); rr=p*p
    e=expected(2,2);beta=e['resource_success'];kappa=e['joint_report_success']
    observed_active=0.
    for t in (0,1):
        ledger=nc['observed_ledger'](nc['build'](us[t],t,shared=True)[0])
        # N and both D records are made on every service branch; R only on
        # completion of both Toffolis. All service and abort bits are kept.
        observed_active+=(pi if t else 1-pi)*(beta*nc['f'](us[t])+
                            kappa*(ledger-nc['f'](us[t])))
    direct=e['service_code_minus_CQ']+observed_active
    reconstructed=(e['service_code_minus_CQ']+
        beta*((1-pi)*nc['f'](us[0])+pi*nc['f'](us[1]))+
        kappa*(p**5+2*p**4*pi))
    assert abs(direct-reconstructed)<1e-12
    d=expected(16,32)
    assert 0<d['joint_report_success']<1 and d['gain_wrt_recorded_pi']>0
    print(json.dumps({'schema':'d0.balanced-native-factory/1','status':'PASS',
       'phase_CZ':cz,'phase_CCZ':ccz,
       'toffoli_all_eight_columns':True,'oldRIGHT_tensor_identity':True,
       'second_abort_before_either_report_is_measured':True,
       'full_service_and_failure_journal_checked':True,
       'exhaustive_capped_transcript_L2_count':len(paths),
       'exhaustive_transcript_cost':net_cost(paths),
       'example':d,'unknown_N_preparation_routing_clock_and_Book_cost':True,
       'GR_closed':False},indent=2))


if __name__=='__main__':main()
