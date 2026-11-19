"""Complete logical columns and genuine intermediate work mark for guarded LIVE.

Toffoli are successful ideal logical gates; expanded factories and Book Info
are not implemented.  All old H,T,port,Spin columns and 3 dummy bits retained.
"""
import json
from collections import Counter
from fractions import Fraction
from itertools import product
import numpy as np
import sympy as sp
from check_live_parser import controller
from check_source_price import load_control,need


def main():
    digest,words=controller();ne,d2=load_control();need(digest==d2,'native owner digest')
    ops=[(w[0],tuple(w[1:])) for w in words]
    need(len(ops)==28 and Counter(t for t,_ in ops)=={'CX':19,'G':5,'SourceI':4},'actual LIVE word')
    special=[(i,t,w) for i,(t,w) in enumerate(ops) if 3 in w]
    need(len(special)==1 and special[0][1:] == ('CX',(3,7)),'H is only unchanged control, never target')
    occ=sum(len(w) for _,w in ops if 3 not in w)
    need(occ==53,'actual non-H wire occurrences')
    # Old input (spin0,spin1,port,H,T), followed by LIVE six wires and 3 dummy.
    p=float(ne.P);a=float(ne.A); n=14
    V=np.eye(32)
    for _ in range(9):V=np.einsum('ij,k->ikj',V,np.array([a,p])).reshape(2*V.shape[0],32)
    reference=V.copy();routed=V.copy();first=None
    G=np.array(ne.G_LOCAL,dtype=float);SI=np.array(ne.SOURCE_I_LOCAL,dtype=float)
    CX=np.array([[1.,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    mats={'G':G,'SourceI':SI,'CX':CX}
    def gate(W,wires,U):
        rest=[i for i in range(n) if i not in wires];axes=list(wires)+rest+[n]
        t=W.reshape([2]*n+[32]).transpose(axes)
        u=np.einsum('ij,jk->ik',U,t.reshape(1<<len(wires),-1),optimize=False)
        return u.reshape([2]*n+[32]).transpose(np.argsort(axes)).reshape(W.shape)
    rows=np.arange(1<<n,dtype=np.uint32)
    hm=((rows>>(n-1-3))&1).astype(bool)
    def swap0(W,x,y):
        xmask=np.uint32(1<<(n-1-x));ymask=np.uint32(1<<(n-1-y))
        yes=(~hm)&(((rows&xmask)!=0)^((rows&ymask)!=0))
        return W[rows^np.where(yes,xmask|ymask,np.uint32(0))]
    # Logical CSWAP0 = SWAP followed by positive Fredkin. Check the literal
    # final CX after the first H-controlled route has dummy as one of its wires.
    for h,x,y in product(range(2),repeat=3):
        u,v=x,y;u^=v;v^=u;u^=v;u^=v;v^=h&u;u^=v
        need((u,v)==((y,x) if h==0 else (x,y)),'six-gate CSWAP0 decomposition')
    for idx,(name,wires) in enumerate(ops):
        reference=gate(reference,wires,mats[name])
        if 3 in wires:
            routed=gate(routed,wires,mats[name]);continue
        for offset,wire in enumerate(wires):
            routed=swap0(routed,wire,11+offset)
            if idx==0 and offset==0:first=routed.copy()
        routed=gate(routed,wires,mats[name])
        for offset,wire in reversed(list(enumerate(wires))):routed=swap0(routed,wire,11+offset)
    need(first is not None and ops[0]==('CX',(4,5)),'first stage carries old T into dummy0')
    err=float(np.max(np.abs((routed-reference)[hm])))
    need(err<1e-12,'H=1 equals actual LIVE on all 32 old columns')
    old=(rows>>(n-5)).astype(int);common=None
    for col in range(32):
        if (col>>1)&1:continue # old H=1; old bits are spin0,spin1,port,H,T
        need(np.max(np.abs(routed[(~hm)&(old!=col),col]))<1e-12,'H0 old T port Spin untouched')
        part=routed[(~hm)&(old==col),col]
        if common is None:common=part
        else:need(np.max(np.abs(part-common))<1e-12,'H0 dummy/output independent of old state')
    # Branch isometries are separately orthogonal and norm preserving.
    V0=routed[~hm];V1=routed[hm]
    need(np.max(np.abs(np.einsum('ki,kj->ij',V0,V0,optimize=False) - np.diag([1 if ((j>>1)&1)==0 else 0 for j in range(32)])))<1e-12,'H0 isometry')
    need(np.max(np.abs(np.einsum('ki,kj->ij',V1,V1,optimize=False) - np.diag([1 if ((j>>1)&1)==1 else 0 for j in range(32)])))<1e-12,'H1 isometry')
    # At first completed CSWAP0 the real last CX touches dummy0. Its local
    # positive mark is P_dummy or I-P_dummy, with no altered program.
    d0=((rows>>(n-1-11))&1).astype(bool)
    X=first[d0];obs=np.einsum('ki,kj->ij',X,X,optimize=False)
    expected=np.diag([(float((j&1)!=0) if ((j>>1)&1)==0 else p*p) for j in range(32)])
    errmark=float(np.max(np.abs(obs-expected)));need(errmark<1e-12,'all-column intermediate mark: H0 T, H1 born v')
    # Non-H output source on H0: both fates charged, T archive retained.
    z=sp.sqrt(5);ps=(z-1)/2;rs=ps**2;noise=ps**3
    pi=sp.symbols('pi',real=True)
    # L=4+D+(H xor D)+(T xor D)+T. Noise E=T xor D has prob r.
    def source(h):
        s=0
        for t,d in product((0,1),repeat=2):
            qt=pi if t else 1-pi
            pd=(rs if (d^t)==1 else ps)
            L=4+d+(h^d)+(t^d)+t
            s+=qt*pd*L
        return sp.simplify(s-(1+rs))
    H0=source(0);H1=source(1)
    need(sp.simplify(H1-(4+pi))==0,'actual LIVE CW5 on H1')
    need(sp.simplify(H0-(3+2*rs+(1+2*noise)*pi))==0,'H0 not CW5')
    mix=sp.simplify(ps*H0+rs*H1)
    need(sp.simplify(sp.diff(mix,pi)-(1+2*ps**4))==0,'unconditionally using random H does not satisfy CW5')
    # H0 prior p, H1 prior r; E[mark]=p*pi+r*r.
    mark=ps*pi+rs**2
    need(sp.simplify(sp.diff(mark,pi)-ps)==0,'intermediate work derivative p Dpi')
    # Combined 142 earlier guarded-pair + 106 parser Toffolis; readiness
    # only if scalar marked-success factors and independent factories hold.
    beta=(1-ps**384)**6*(1-(1-16*ps**9)**64)
    s248=beta**248
    print(json.dumps({'status':'PASS','source_sha256':digest,'old_input_columns':32,
      'live_square_gates':len(ops),'unguarded_control_H_gate':list(special[0][2]),
      'wire_occurrences_routed':occ,'dummy_wires':3,'live_births':9,
      'logical_Toffoli':2*occ,'logical_CX':19+10*occ,'logical_G':5,'logical_SourceI':4,
      'logical_total_stages':9+19+10*occ+5+4+2*occ,
      'H1_max_column_error':err,'H0_old_and_dummy_factorized':True,
      'first_route_work_mark_max_error':errmark,
      'work_mark_probability':'p*pi+p^4 (fresh H with P(H=0)=p)',
      'work_mark_source':'plus or minus lambda*p*Dpi',
      'work_mark_normalized_to_guarded_live_signal':'plus or minus lambda/p',
      'unguarded_LIVE_H0_code_CQ':'3+2*p^2+(1+2*p^3)*pi',
      'unguarded_LIVE_H1_code_CQ':'4+pi',
      'random_H_unguarded_slope':str(sp.simplify(sp.diff(mix,pi))),
      'guarded_LIVE_conditional_code_CQ':'p^2*(4+pi), with H registered and per-branch code actually issued',
      'conditional_248_factories_success':str(sp.N(s248,25)),
      'conditional_signal_factor_p2_times_248_success':str(sp.N(rs*s248,25)),
      'all_failure_fine_logs_and_route_work_physically_bound':False,
      'actual_CostInfo_lift_and_GR_closed':False},indent=2))

if __name__=='__main__':main()
